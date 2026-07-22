#!/usr/bin/env python3
"""Build a replayable Stage-1B arXiv BFS candidate snapshot from REC-1.

The builder performs no network access and makes no inclusion/exclusion decision. It verifies every
successful result-page raw hash, checks that the Atom entry IDs match the REC-1 row, merges repeated
hits by canonical arXiv ID, and preserves all query-page lineage. Output rows remain D0/PENDING until
human or independently checked abstract screening creates canonical REC-0 decisions.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from sf_asset_path import resolve_asset_path


ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV = "{http://arxiv.org/schemas/atom}"
ARXIV_ID = re.compile(r"/abs/(.+?)(v\d+)?$")
VERSION = re.compile(r"(v\d+)$")


class CandidateBuildError(RuntimeError):
    """Fail-closed provenance or Atom/ledger consistency error."""


def _compact(text: str | None) -> str:
    return " ".join((text or "").split())


def _entry_id(entry: ET.Element) -> tuple[str, str | None]:
    value = _compact(entry.findtext(f"{ATOM}id"))
    match = ARXIV_ID.search(value)
    if not match:
        raise CandidateBuildError(f"unrecognized arXiv entry id: {value!r}")
    return match.group(1), match.group(2)


def _parse_atom(body: bytes) -> list[dict[str, Any]]:
    try:
        root = ET.fromstring(body)
    except ET.ParseError as exc:
        raise CandidateBuildError(f"invalid Atom XML: {exc}") from exc
    records = []
    for entry in root.findall(f"{ATOM}entry"):
        arxiv_id, version = _entry_id(entry)
        records.append(
            {
                "arxiv_id": arxiv_id,
                "version": version,
                "title": _compact(entry.findtext(f"{ATOM}title")),
                "abstract": _compact(entry.findtext(f"{ATOM}summary")),
                "authors": [
                    _compact(author.findtext(f"{ATOM}name"))
                    for author in entry.findall(f"{ATOM}author")
                    if _compact(author.findtext(f"{ATOM}name"))
                ],
                "published": _compact(entry.findtext(f"{ATOM}published")),
                "updated": _compact(entry.findtext(f"{ATOM}updated")),
                "categories": sorted(
                    {
                        category.attrib.get("term", "").strip()
                        for category in entry.findall(f"{ATOM}category")
                        if category.attrib.get("term", "").strip()
                    }
                ),
                "primary_category": (
                    entry.find(f"{ARXIV}primary_category").attrib.get("term", "").strip()
                    if entry.find(f"{ARXIV}primary_category") is not None
                    else ""
                ),
            }
        )
    return records


def _read_rec1(path: Path) -> list[dict[str, Any]]:
    rows = []
    for line_no, line in enumerate(path.read_text("utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise CandidateBuildError(f"REC-1 line {line_no}: invalid JSON: {exc}") from exc
    return rows


def collect_candidates(rec1_path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = _read_rec1(rec1_path)
    superseded_failure_timestamps = {
        row["retry_of_timestamp"] for row in rows if row.get("retry_of_timestamp")
    }
    works: dict[str, dict[str, Any]] = {}
    successful_pages = 0
    failed_rows = 0
    probes_skipped = 0
    raw_bytes = 0
    timestamps = []

    for row_no, row in enumerate(rows, start=1):
        timestamps.append(row.get("timestamp", ""))
        if row.get("failed_request"):
            failed_rows += 1
            continue
        if not str(row.get("request_role", "")).startswith("RESULT_PAGE"):
            probes_skipped += 1
            continue
        raw_ref = row.get("raw_response_ref")
        expected_hash = row.get("response_sha256")
        if not raw_ref or not expected_hash:
            raise CandidateBuildError(f"REC-1 line {row_no}: successful page lacks raw/hash")
        raw_path = Path(resolve_asset_path(raw_ref))
        if not raw_path.is_file():
            raise CandidateBuildError(f"REC-1 line {row_no}: raw response missing: {raw_path}")
        body = raw_path.read_bytes()
        actual_hash = hashlib.sha256(body).hexdigest()
        if actual_hash != expected_hash:
            raise CandidateBuildError(
                f"REC-1 line {row_no}: raw hash mismatch ({actual_hash} != {expected_hash})"
            )
        parsed = _parse_atom(body)
        parsed_ids = [item["arxiv_id"] for item in parsed]
        logged_ids = list(row.get("included", []))
        if parsed_ids != logged_ids:
            raise CandidateBuildError(
                f"REC-1 line {row_no}: included IDs differ from Atom entries"
            )
        successful_pages += 1
        raw_bytes += len(body)

        event = {
            "query_id": row["query_id"],
            "query_ref": row.get("query_ref"),
            "request_role": row["request_role"],
            "page_start": row.get("page_start"),
            "timestamp": row.get("timestamp"),
            "response_sha256": expected_hash,
            "raw_response_ref": raw_ref,
        }
        for metadata in parsed:
            arxiv_id = metadata.pop("arxiv_id")
            version = metadata.pop("version")
            item = works.setdefault(
                arxiv_id,
                {
                    "record_type": "BFS_CANDIDATE_SNAPSHOT",
                    "arxiv_id": arxiv_id,
                    "versions": [],
                    **metadata,
                    "source_query_ids": [],
                    "source_events": [],
                    "query_recall_credit": True,
                    "coding_depth": "D0",
                    "screening_decision": "PENDING",
                },
            )
            if version and version not in item["versions"]:
                item["versions"].append(version)
            if metadata.get("updated", "") > item.get("updated", ""):
                for key, value in metadata.items():
                    item[key] = value
            if event not in item["source_events"]:
                item["source_events"].append(dict(event))

    candidates = []
    for arxiv_id in sorted(works):
        item = works[arxiv_id]
        item["versions"] = sorted(
            item["versions"], key=lambda value: int(VERSION.fullmatch(value).group(1)[1:])
        )
        item["source_events"] = sorted(
            item["source_events"],
            key=lambda event: (
                event["query_id"],
                int(event.get("page_start") or 0),
                event.get("timestamp") or "",
            ),
        )
        item["source_query_ids"] = sorted(
            {event["query_id"] for event in item["source_events"]}
        )
        candidates.append(item)

    stats = {
        "schema": "sf-stage1b-bfs-snapshot-v1",
        "rec1": rec1_path.as_posix(),
        "ledger_rows": len(rows),
        "successful_pages": successful_pages,
        "failed_rows_retained": failed_rows,
        "active_failures": sum(
            1
            for row in rows
            if row.get("failed_request")
            and row.get("timestamp") not in superseded_failure_timestamps
        ),
        "split_count_probes_skipped": probes_skipped,
        "source_events": sum(len(item["source_events"]) for item in candidates),
        "unique_candidates": len(candidates),
        "raw_bytes_verified": raw_bytes,
        "first_rec1_timestamp": min((value for value in timestamps if value), default=None),
        "last_rec1_timestamp": max((value for value in timestamps if value), default=None),
        "screening_state": "D0_PENDING",
    }
    return candidates, stats


def write_candidates(path: Path, candidates: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = "".join(
        json.dumps(item, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
        for item in candidates
    )
    path.write_text(payload, encoding="utf-8", newline="\n")


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--rec1", type=Path, required=True)
    cli.add_argument("--output", type=Path, required=True)
    cli.add_argument("--stats", type=Path, required=True)
    args = cli.parse_args()
    candidates, stats = collect_candidates(args.rec1)
    write_candidates(args.output, candidates)
    args.stats.parent.mkdir(parents=True, exist_ok=True)
    args.stats.write_text(
        json.dumps(stats, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(stats, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
