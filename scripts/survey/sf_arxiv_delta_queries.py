#!/usr/bin/env python3
"""Generate append-only arXiv date-delta queries from the frozen Stage-1B manifest.

The parent manifest is read and hash-verified but never rewritten.  Each child keeps the Boolean query
body and execution settings, replaces the single submittedDate interval, and records its parent hash.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import quote


DATE_CLAUSE = re.compile(r"submittedDate:\[(\d{12}) TO (\d{12})\]")
STAMP = re.compile(r"^\d{12}$")


class DeltaQueryError(RuntimeError):
    """Fail-closed frozen-parent or date-delta construction error."""


def record_hash(payload: dict[str, Any]) -> str:
    compact = json.dumps(
        payload,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
        allow_nan=False,
    )
    return hashlib.sha256(compact.encode("utf-8")).hexdigest()


def _valid_range(date_from: str, date_to: str) -> bool:
    return bool(STAMP.fullmatch(date_from) and STAMP.fullmatch(date_to) and date_from <= date_to)


def make_delta_row(parent: dict[str, Any], date_from: str, date_to: str) -> dict[str, Any]:
    if not _valid_range(date_from, date_to):
        raise DeltaQueryError(f"invalid date range: {date_from}..{date_to}")
    declared = parent.get("record_sha256")
    actual = record_hash({key: value for key, value in parent.items() if key != "record_sha256"})
    if declared != actual:
        raise DeltaQueryError(
            f"{parent.get('query_id', '<unknown>')}: parent hash mismatch ({declared} != {actual})"
        )
    decoded = str(parent.get("decoded_search_query", ""))
    matches = list(DATE_CLAUSE.finditer(decoded))
    if len(matches) != 1:
        raise DeltaQueryError(
            f"{parent.get('query_id', '<unknown>')}: expected exactly one submittedDate clause, "
            f"found {len(matches)}"
        )
    rewritten = DATE_CLAUSE.sub(f"submittedDate:[{date_from} TO {date_to}]", decoded)
    child = {
        key: value for key, value in parent.items() if key != "record_sha256"
    }
    child.update(
        {
            "query_id": (
                f"{parent['query_id']}-D{date_from[:8]}-{date_to[:8]}"
            ),
            "decoded_search_query": rewritten,
            "url_encoded_search_query": quote(rewritten, safe=""),
            "date_from": date_from,
            "date_to": date_to,
            "parent_query_id": parent["query_id"],
            "parent_record_sha256": declared,
            "delta_semantics": "APPEND_ONLY_CLOSED_INTERVAL",
        }
    )
    child["record_sha256"] = record_hash(child)
    return child


def generate_manifest(
    parent_path: Path,
    output_path: Path,
    date_from: str,
    date_to: str,
) -> dict[str, Any]:
    parent_bytes = parent_path.read_bytes()
    rows = []
    for line_no, line in enumerate(parent_bytes.decode("utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise DeltaQueryError(f"parent line {line_no}: invalid JSON: {exc}") from exc
    children = [make_delta_row(row, date_from, date_to) for row in rows]
    if len({row["query_id"] for row in children}) != len(children):
        raise DeltaQueryError("duplicate delta query IDs")
    payload = "".join(
        json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
        for row in children
    ).encode("utf-8")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(payload)
    return {
        "schema": "sf-arxiv-date-delta-v1",
        "parent": parent_path.as_posix(),
        "parent_sha256": hashlib.sha256(parent_bytes).hexdigest(),
        "date_from": date_from,
        "date_to": date_to,
        "delta_rows": len(children),
        "output": output_path.as_posix(),
        "output_bytes": len(payload),
        "output_sha256": hashlib.sha256(payload).hexdigest(),
        "parent_rewritten": False,
    }


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--parent", type=Path, required=True)
    cli.add_argument("--output", type=Path, required=True)
    cli.add_argument("--date-from", required=True)
    cli.add_argument("--date-to", required=True)
    cli.add_argument("--summary", type=Path)
    args = cli.parse_args()
    summary = generate_manifest(args.parent, args.output, args.date_from, args.date_to)
    if args.summary:
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        args.summary.write_text(
            json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
