#!/usr/bin/env python3
"""Execute frozen Stage-1B arXiv queries and append replayable REC-1 rows.

The runner is deliberately limited to bibliographic retrieval. It never calls a
research model. Raw Atom bytes live outside Git; the append-only REC-1 ledger
stores their paths and SHA-256 hashes. Existing complete page rows are reused so
an interrupted run can resume without repeating a request.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
from urllib.parse import quote

from sf_child_query_split import SLICE_LIMIT, parent_from_frozen_row, split_query


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_QUERIES = ROOT / "wiki" / "survey" / "2026-07-15-sf-queries.jsonl"
DEFAULT_DATA_ROOT = Path(
    os.environ.get(
        "SPEECHRL_DATA_DIR",
        "E:/chao_workspace/exploring-l4-intelligence/speechrl-data",
    )
)
API = "https://export.arxiv.org/api/query"
USER_AGENT = "exploring-l4-intelligence Stage-1B systematic mapping"
SPACING_SECONDS = 3.0
MAX_ATTEMPTS = 4
ARXIV_ID = re.compile(r"/abs/([^/?#]+?)(?:v\d+)?$")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_bytes(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def compute_record_hash(record_without_hash: dict[str, Any]) -> str:
    compact = json.dumps(
        record_without_hash,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
        allow_nan=False,
    )
    return hashlib.sha256(compact.encode("utf-8")).hexdigest()


def validate_frozen_row(row: dict[str, Any]) -> None:
    declared = row.get("record_sha256")
    if not declared:
        raise ValueError(f"{row.get('query_id', '<unknown>')}: missing record_sha256")
    payload = {key: value for key, value in row.items() if key != "record_sha256"}
    actual = compute_record_hash(payload)
    if actual != declared:
        raise ValueError(
            f"{row.get('query_id', '<unknown>')}: record_sha256 mismatch "
            f"({declared} != {actual})"
        )
    required = {
        "query_id",
        "decoded_search_query",
        "url_encoded_search_query",
        "start",
        "max_results",
        "sortBy",
        "sortOrder",
    }
    missing = sorted(required - row.keys())
    if missing:
        raise ValueError(f"{row['query_id']}: missing required keys {missing}")


def load_frozen_rows(path: Path) -> list[dict[str, Any]]:
    rows = [json.loads(line) for line in path.read_text("utf-8").splitlines() if line.strip()]
    seen: set[str] = set()
    for row in rows:
        validate_frozen_row(row)
        query_id = row["query_id"]
        if query_id in seen:
            raise ValueError(f"duplicate frozen query_id: {query_id}")
        seen.add(query_id)
    return rows


def parse_atom_page(body: bytes) -> dict[str, Any]:
    root = ET.fromstring(body)
    atom = "{http://www.w3.org/2005/Atom}"
    opensearch = "{http://a9.com/-/spec/opensearch/1.1/}"

    def integer(name: str) -> int:
        value = root.findtext(opensearch + name)
        if value is None:
            raise ValueError(f"Atom response missing opensearch:{name}")
        return int(value)

    ids: list[str] = []
    for entry in root.findall(atom + "entry"):
        raw_id = (entry.findtext(atom + "id") or "").strip()
        match = ARXIV_ID.search(raw_id)
        if not match:
            raise ValueError(f"unparseable arXiv entry id: {raw_id!r}")
        ids.append(match.group(1))
    return {
        "total_results": integer("totalResults"),
        "start_index": integer("startIndex"),
        "items_per_page": integer("itemsPerPage"),
        "ids": ids,
    }


def build_url(decoded_query: str, start: int, max_results: int, sort_by: str, sort_order: str) -> str:
    return (
        f"{API}?search_query={quote(decoded_query, safe='')}"
        f"&start={start}&max_results={max_results}"
        f"&sortBy={quote(sort_by, safe='')}&sortOrder={quote(sort_order, safe='')}"
    )


def network_transport(url: str) -> tuple[int | None, bytes, int, str | None]:
    last_error: str | None = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=120) as response:
                return response.status, response.read(), attempt, None
        except Exception as error:  # noqa: BLE001 - failure is logged after bounded retries.
            last_error = f"{type(error).__name__}: {error}"
            if attempt < MAX_ATTEMPTS:
                time.sleep(SPACING_SECONDS * (2 ** (attempt - 1)))
    return None, b"", MAX_ATTEMPTS, last_error


def _safe_query_id(query_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]", "_", query_id)


def _load_existing(rec1_path: Path) -> dict[tuple[str, int, str], dict[str, Any]]:
    if not rec1_path.exists():
        return {}
    rows: dict[tuple[str, int, str], dict[str, Any]] = {}
    for line_number, line in enumerate(rec1_path.read_text("utf-8").splitlines(), 1):
        if not line.strip():
            continue
        row = json.loads(line)
        key = (row["query_id"], int(row["page_start"]), row.get("request_role", "RESULT_PAGE"))
        if key in rows:
            raise ValueError(f"duplicate REC-1 key at line {line_number}: {key}")
        rows[key] = row
    return rows


def _append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def _raw_path(raw_dir: Path, query_id: str, start: int, role: str) -> Path:
    suffix = "probe" if role == "SPLIT_COUNT_PROBE" else "start"
    return raw_dir / _safe_query_id(query_id) / f"{suffix}-{start:06d}.atom"


def _record_page(
    *,
    rec1_path: Path,
    raw_dir: Path,
    query: dict[str, Any],
    start: int,
    max_results: int,
    transport: Callable[[str], tuple[int | None, bytes, int, str | None]],
    role: str = "RESULT_PAGE",
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    url = build_url(
        query["decoded_search_query"], start, max_results,
        query.get("sortBy", "relevance"), query.get("sortOrder", "descending"),
    )
    http_status, body, attempts, error = transport(url)
    timestamp = utc_now()
    parsed: dict[str, Any] | None = None
    response_hash: str | None = None
    raw_ref: str | None = None
    if http_status == 200 and body:
        parsed = parse_atom_page(body)
        path = _raw_path(raw_dir, query["query_id"], start, role)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)
        response_hash = sha256_bytes(body)
        raw_ref = path.as_posix()
    elif not error:
        error = f"HTTP_STATUS_{http_status}"

    row = {
        "query_id": query["query_id"],
        "engine": "arxiv_api",
        "query_ref": query.get("record_sha256") or query.get("frozen_record_sha256"),
        "request_role": role,
        "page_start": start,
        "max_results": max_results,
        "totalResults": parsed["total_results"] if parsed else None,
        "sortBy": query.get("sortBy", "relevance"),
        "sortOrder": query.get("sortOrder", "descending"),
        "timestamp": timestamp,
        "request_url": url,
        "raw_response_ref": raw_ref,
        "response_sha256": response_hash,
        "http_status": http_status,
        "attempts": attempts,
        "n_hits_page": len(parsed["ids"]) if parsed else 0,
        "included": parsed["ids"] if parsed else [],
        "excluded": [],
        "failed_request": error,
        "access_class": "SYSTEMATIC_DISCOVERY_QUERY",
    }
    for key in (
        "parent_query_id", "parent_query_sha256", "query_sha256", "split_level",
        "split_ordinal", "trigger_totalresults", "date_from", "date_to", "timezone",
        "boundary_semantics", "observed_totalresults",
    ):
        if key in query:
            row[key] = query[key]
    _append_jsonl(rec1_path, row)
    return row, parsed


def execute_rows(
    rows: list[dict[str, Any]],
    rec1_path: Path,
    raw_dir: Path,
    *,
    transport: Callable[[str], tuple[int | None, bytes, int, str | None]] = network_transport,
    sleep: Callable[[float], None] = time.sleep,
) -> dict[str, Any]:
    """Execute rows in order, logging all result pages and split count probes."""
    existing = _load_existing(rec1_path)
    summary: dict[str, Any] = {
        "queries_selected": len(rows),
        "pages_written": 0,
        "pages_skipped": 0,
        "failed_requests": 0,
        "split_probes_written": 0,
        "unique_hits": 0,
    }
    unique_hits: set[str] = set()
    network_calls = 0

    def throttle() -> None:
        nonlocal network_calls
        if network_calls:
            sleep(SPACING_SECONDS)
        network_calls += 1

    def get_or_fetch(query: dict[str, Any], start: int, page_size: int, role: str):
        key = (query["query_id"], start, role)
        old = existing.get(key)
        if old is not None:
            summary["pages_skipped"] += 1
            unique_hits.update(old.get("included", []))
            return old, None
        throttle()
        record, parsed = _record_page(
            rec1_path=rec1_path,
            raw_dir=raw_dir,
            query=query,
            start=start,
            max_results=page_size,
            transport=transport,
            role=role,
        )
        existing[key] = record
        summary["pages_written"] += 1
        if role == "SPLIT_COUNT_PROBE":
            summary["split_probes_written"] += 1
        if record["failed_request"]:
            summary["failed_requests"] += 1
        unique_hits.update(record["included"])
        return record, parsed

    def execute_terminal(query: dict[str, Any], root_first=None) -> None:
        page_size = int(query.get("max_results", 75))
        if root_first is None:
            first_record, first_parsed = get_or_fetch(query, 0, page_size, "RESULT_PAGE")
        else:
            first_record, first_parsed = root_first
        if first_record.get("failed_request"):
            return
        total = int(first_record["totalResults"])
        start = page_size
        while start < total:
            page_record, _ = get_or_fetch(query, start, page_size, "RESULT_PAGE")
            if page_record.get("failed_request"):
                return
            start += page_size

    for frozen in rows:
        validate_frozen_row(frozen)
        first_key = (frozen["query_id"], int(frozen["start"]), "RESULT_PAGE")
        if first_key in existing:
            old = existing[first_key]
            summary["pages_skipped"] += 1
            unique_hits.update(old.get("included", []))
            if old.get("failed_request"):
                continue
            total = int(old["totalResults"])
            first = (old, None)
        else:
            throttle()
            first = _record_page(
                rec1_path=rec1_path,
                raw_dir=raw_dir,
                query=frozen,
                start=int(frozen["start"]),
                max_results=int(frozen["max_results"]),
                transport=transport,
            )
            existing[first_key] = first[0]
            summary["pages_written"] += 1
            unique_hits.update(first[0]["included"])
            if first[0]["failed_request"]:
                summary["failed_requests"] += 1
                continue
            total = int(first[0]["totalResults"])

        if total <= SLICE_LIMIT:
            execute_terminal(frozen, first)
            continue

        parent = parent_from_frozen_row(frozen)
        parent.update({"date_from": frozen["date_from"], "date_to": frozen["date_to"]})

        def totalresults_of(decoded: str) -> int:
            if decoded == frozen["decoded_search_query"]:
                return total
            probe_id = "probe-" + hashlib.sha256(decoded.encode("utf-8")).hexdigest()[:16]
            probe = {
                "query_id": f"{frozen['query_id']}-{probe_id}",
                "decoded_search_query": decoded,
                "sortBy": frozen["sortBy"],
                "sortOrder": frozen["sortOrder"],
                "frozen_record_sha256": frozen["record_sha256"],
            }
            record, parsed = get_or_fetch(probe, 0, 1, "SPLIT_COUNT_PROBE")
            if record.get("failed_request"):
                raise RuntimeError(f"split count probe failed for {probe['query_id']}")
            if parsed is not None:
                return int(parsed["total_results"])
            return int(record["totalResults"])

        terminals, _events = split_query(parent, totalresults_of)
        for terminal in terminals:
            if terminal.get("api_limit"):
                raise RuntimeError(
                    f"{terminal['query_id']}: API_LIMIT_SINGLE_DAY_OVER_2000"
                )
            terminal.update(
                {
                    "sortBy": frozen["sortBy"],
                    "sortOrder": frozen["sortOrder"],
                    "max_results": frozen["max_results"],
                    "frozen_record_sha256": frozen["record_sha256"],
                }
            )
            execute_terminal(terminal)

    summary["unique_hits"] = len(unique_hits)
    return summary


def _replace_url_start(url: str, start: int) -> str:
    replaced, count = re.subn(r"([?&]start=)\d+", rf"\g<1>{start}", url, count=1)
    if count != 1:
        raise ValueError("request_url has no unique start parameter")
    return replaced


def retry_failed_pages(
    rec1_path: Path,
    raw_dir: Path,
    *,
    transport: Callable[[str], tuple[int | None, bytes, int, str | None]] = network_transport,
    sleep: Callable[[float], None] = time.sleep,
) -> dict[str, Any]:
    """Append retry rows for terminal failures and continue their missing pages.

    Original failure rows remain immutable. A retry binds the failed row timestamp;
    another invocation is a no-op after a successful superseding row exists.
    """
    rows = [
        json.loads(line)
        for line in rec1_path.read_text("utf-8").splitlines()
        if line.strip()
    ]
    superseded_timestamps = {
        row["retry_of_timestamp"]
        for row in rows
        if row.get("retry_of_timestamp")
    }
    failures = [
        row for row in rows
        if row.get("failed_request") and row["timestamp"] not in superseded_timestamps
    ]
    summary = {
        "failures_selected": len(failures),
        "pages_written": 0,
        "failed_requests": 0,
        "unique_hits": 0,
    }
    unique_hits: set[str] = set()
    calls = 0

    def fetch_and_append(source: dict[str, Any], start: int, ordinal: int, retry_of: str | None):
        nonlocal calls
        if calls:
            sleep(SPACING_SECONDS)
        calls += 1
        url = _replace_url_start(source["request_url"], start)
        status, body, attempts, error = transport(url)
        timestamp = utc_now()
        parsed = None
        raw_ref = None
        response_hash = None
        if status == 200 and body:
            parsed = parse_atom_page(body)
            path = (
                raw_dir / _safe_query_id(source["query_id"])
                / f"retry-{ordinal:03d}-start-{start:06d}.atom"
            )
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)
            raw_ref = path.as_posix()
            response_hash = sha256_bytes(body)
        elif not error:
            error = f"HTTP_STATUS_{status}"
        record = dict(source)
        record.update(
            {
                "request_role": f"RESULT_PAGE_RETRY_{ordinal}",
                "page_start": start,
                "timestamp": timestamp,
                "request_url": url,
                "raw_response_ref": raw_ref,
                "response_sha256": response_hash,
                "http_status": status,
                "attempts": attempts,
                "totalResults": parsed["total_results"] if parsed else None,
                "n_hits_page": len(parsed["ids"]) if parsed else 0,
                "included": parsed["ids"] if parsed else [],
                "excluded": [],
                "failed_request": error,
                "retry_of_timestamp": retry_of,
            }
        )
        _append_jsonl(rec1_path, record)
        rows.append(record)
        summary["pages_written"] += 1
        if error:
            summary["failed_requests"] += 1
        unique_hits.update(record["included"])
        return record

    for failure in failures:
        same_query = [row for row in rows if row["query_id"] == failure["query_id"]]
        ordinal = 1 + max(
            [
                int(match.group(1))
                for row in same_query
                if (match := re.fullmatch(r"RESULT_PAGE_RETRY_(\d+)", row.get("request_role", "")))
            ]
            or [0]
        )
        start = int(failure["page_start"])
        recovered = fetch_and_append(failure, start, ordinal, failure["timestamp"])
        if recovered.get("failed_request"):
            continue
        total = int(recovered["totalResults"])
        page_size = int(recovered["max_results"])
        successful_starts = {
            int(row["page_start"])
            for row in rows
            if row["query_id"] == failure["query_id"] and not row.get("failed_request")
        }
        start += page_size
        while start < total:
            if start not in successful_starts:
                page = fetch_and_append(failure, start, ordinal, None)
                if page.get("failed_request"):
                    break
                successful_starts.add(start)
            start += page_size

    summary["unique_hits"] = len(unique_hits)
    return summary


def _git_head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()


def write_execution_metadata(
    path: Path, query_path: Path, selected_rows: list[dict[str, Any]], actor: str
) -> None:
    metadata = {
        "schema": "sf-stage1b-execution-v1",
        "current_activity_stage": "STAGE_1B_SYSTEMATIC_MAPPING",
        "execution_commit": _git_head(),
        "started_at_utc": utc_now(),
        "actor": actor,
        "platform": {"system": platform.system(), "release": platform.release(), "python": sys.version},
        "protocol": "wiki/survey/current/protocol.md",
        "protocol_sha256": sha256_bytes((ROOT / "wiki/survey/current/protocol.md").read_bytes()),
        "queries": query_path.as_posix(),
        "queries_sha256": sha256_bytes(query_path.read_bytes()),
        "selected_query_ids": [row["query_id"] for row in selected_rows],
        "new_model_touches_since_gate_freeze": 0,
        "research_model_or_smoke_executions": 0,
        "dataset_metric_or_prototype_executions": 0,
        "legacy_experiments": "INHERITED_PRIOR_EXPOSURE",
        "h5_load_bearing_use": "WITHHOLD",
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", "utf-8", newline="\n")


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--queries", type=Path, default=DEFAULT_QUERIES)
    cli.add_argument("--rec1", type=Path, required=True)
    cli.add_argument("--raw-dir", type=Path)
    cli.add_argument("--metadata", type=Path)
    cli.add_argument("--actor", default="Codex acting under owner authorization")
    cli.add_argument("--query-id", action="append", default=[])
    cli.add_argument("--limit", type=int)
    cli.add_argument("--retry-failed", action="store_true")
    return cli


def main() -> int:
    args = parser().parse_args()
    raw_dir = args.raw_dir or DEFAULT_DATA_ROOT / "survey-query-raw" / "stage1b-2026-07-21"
    if args.retry_failed:
        summary = retry_failed_pages(args.rec1, raw_dir)
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 1 if summary["failed_requests"] else 0
    rows = load_frozen_rows(args.queries)
    if args.query_id:
        wanted = set(args.query_id)
        rows = [row for row in rows if row["query_id"] in wanted]
        missing = wanted - {row["query_id"] for row in rows}
        if missing:
            raise SystemExit(f"unknown query ids: {sorted(missing)}")
    if args.limit is not None:
        if args.limit < 1:
            raise SystemExit("--limit must be >= 1")
        rows = rows[: args.limit]
    if not rows:
        raise SystemExit("no frozen query rows selected")

    metadata = args.metadata or args.rec1.with_name("execution-metadata.json")
    if not metadata.exists():
        write_execution_metadata(metadata, args.queries, rows, args.actor)
    summary = execute_rows(rows, args.rec1, raw_dir)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if summary["failed_requests"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
