#!/usr/bin/env python3
"""Reconcile matched T1 proceedings titles against existing arXiv/registry work identities.

This is an offline work-level deduplication step.  It performs no discovery request and never creates
multiple seeds for the same normalized title or arXiv identity.  Unmatched titles remain explicit
``UNRESOLVED_TITLE`` records for bounded title screening.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


def title_key(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).lower()
    characters = [
        character if (character.isalnum() or character.isspace()) else " "
        for character in normalized
    ]
    return " ".join("".join(characters).split())


def build_known_index(records: Iterable[dict[str, Any]]) -> dict[str, set[str]]:
    index: dict[str, set[str]] = {}
    for record in records:
        title = str(record.get("title") or "").strip()
        arxiv_id = str(record.get("arxiv_id") or "").strip()
        if not title or not arxiv_id:
            continue
        index.setdefault(title_key(title), set()).add(arxiv_id)
    return index


def reconcile_titles(
    t1_report: dict[str, Any], known_index: dict[str, set[str]]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    grouped: dict[str, dict[str, set[str]]] = {}
    events = 0
    for route in t1_report.get("rows") or []:
        if route.get("disposition") != "EXECUTED":
            continue
        for match in route.get("matched_titles") or []:
            title = str(match.get("title") or "").strip()
            if not title:
                continue
            events += 1
            key = title_key(title)
            item = grouped.setdefault(key, {"titles": set(), "route_ids": set()})
            item["titles"].add(title)
            item["route_ids"].add(str(route["route_id"]))

    rows = []
    for key in sorted(grouped):
        known_ids = sorted(known_index.get(key, set()))
        if len(known_ids) == 1:
            resolution = "KNOWN_WORK_UNIQUE"
        elif len(known_ids) > 1:
            resolution = "KNOWN_WORK_AMBIGUOUS"
        else:
            resolution = "UNRESOLVED_TITLE"
        rows.append(
            {
                "canonical_title_key": key,
                "observed_titles": sorted(grouped[key]["titles"]),
                "route_ids": sorted(grouped[key]["route_ids"]),
                "known_arxiv_ids": known_ids,
                "resolution": resolution,
                "creates_new_seed": False,
            }
        )
    counts = Counter(row["resolution"] for row in rows)
    summary = {
        "matched_title_events": events,
        "unique_title_keys": len(rows),
        "known_unique": counts["KNOWN_WORK_UNIQUE"],
        "known_ambiguous": counts["KNOWN_WORK_AMBIGUOUS"],
        "unresolved_titles": counts["UNRESOLVED_TITLE"],
        "duplicate_seed_creation": 0,
    }
    return rows, summary


def _read_jsonl(paths: list[Path]) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for path in paths
        for line in path.read_text("utf-8").splitlines()
        if line.strip()
    ]


def _receipt(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    return {
        "path": path.as_posix(),
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }


def run(t1_path: Path, known_paths: list[Path], output_path: Path) -> dict[str, Any]:
    t1_raw = t1_path.read_bytes()
    t1_report = json.loads(t1_raw)
    known_index = build_known_index(_read_jsonl(known_paths))
    rows, summary = reconcile_titles(t1_report, known_index)
    document = {
        "schema": "sf-stage1b-t1-title-reconciliation-v1",
        "inputs": {
            "t1_report": t1_path.as_posix(),
            "t1_report_sha256": hashlib.sha256(t1_raw).hexdigest(),
            "known_jsonl": [_receipt(path) for path in known_paths],
        },
        "summary": summary,
        "rows": rows,
    }
    payload = json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(payload, encoding="utf-8", newline="\n")
    return document


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--t1-report", type=Path, required=True)
    parser.add_argument("--known-jsonl", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    document = run(args.t1_report, args.known_jsonl, args.output)
    print(json.dumps(document["summary"], ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
