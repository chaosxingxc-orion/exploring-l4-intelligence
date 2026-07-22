#!/usr/bin/env python3
"""Close a bounded arXiv delta at REC-0 without creating duplicate work seeds."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line.strip()]


def build_decisions(
    candidates: list[dict[str, Any]],
    selections: dict[str, dict[str, Any]],
    known_ids: set[str],
) -> list[dict[str, Any]]:
    ids = [str(row.get("arxiv_id", "")).strip() for row in candidates]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate candidate arXiv ID")
    missing = sorted(set(selections) - set(ids))
    if missing:
        raise ValueError(f"selection ids absent from candidate ledger: {missing}")

    rows = []
    for source in sorted(candidates, key=lambda row: str(row["arxiv_id"])):
        aid = str(source["arxiv_id"])
        base = {
            "schema": "sf-stage1b-delta-rec0-v1",
            "arxiv_id": aid,
            "title": source.get("title"),
            "published": source.get("published"),
            "source_query_ids": source.get("source_query_ids", []),
            "manual_abstract_review": True,
            "query_recall_credit": bool(source.get("query_recall_credit")),
        }
        if aid in known_ids:
            row = {
                **base,
                "abstract_disposition": "DUPLICATE_KNOWN_WORK",
                "decision_reason": "Canonical arXiv identity already exists in the retained registry.",
                "creates_seed": False,
                "unresolved": False,
            }
        elif aid in selections:
            choice = selections[aid]
            row = {
                **base,
                "abstract": source.get("abstract"),
                "abstract_disposition": "SELECT_FULLTEXT",
                "provisional_role": choice["role"],
                "eligible_input_family": choice["family"],
                "decision_reason": choice["reason"],
                "creates_seed": True,
                "unresolved": False,
            }
        else:
            row = {
                **base,
                "abstract_disposition": "EXCLUDE_STAGE1B_LOAD_BEARING",
                "decision_reason": (
                    "Manual title/abstract review found no change to the five current method-path "
                    "families; retained in the external candidate ledger for future targeted use."
                ),
                "creates_seed": False,
                "unresolved": False,
            }
        rows.append(row)
    return rows


def run(
    candidate_path: Path,
    config_path: Path,
    known_paths: list[Path],
    output_path: Path,
    summary_path: Path,
) -> dict[str, Any]:
    candidates = _read_jsonl(candidate_path)
    config = json.loads(config_path.read_text("utf-8"))
    selection_rows = config.get("selections", [])
    selections = {str(row["arxiv_id"]): row for row in selection_rows}
    if len(selections) != len(selection_rows):
        raise ValueError("duplicate selection arXiv ID")
    known_ids = {
        str(row["arxiv_id"])
        for path in known_paths
        for row in _read_jsonl(path)
        if row.get("arxiv_id")
    }
    rows = build_decisions(candidates, selections, known_ids)
    payload = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(payload, encoding="utf-8", newline="\n")
    counts: dict[str, int] = {}
    for row in rows:
        key = str(row["abstract_disposition"])
        counts[key] = counts.get(key, 0) + 1
    summary = {
        "schema": "sf-stage1b-delta-rec0-summary-v1",
        "candidate_rows": len(rows),
        "unique_work_ids": len({row["arxiv_id"] for row in rows}),
        "selected_fulltext": counts.get("SELECT_FULLTEXT", 0),
        "duplicate_known_work": counts.get("DUPLICATE_KNOWN_WORK", 0),
        "excluded_load_bearing": counts.get("EXCLUDE_STAGE1B_LOAD_BEARING", 0),
        "unresolved": sum(bool(row["unresolved"]) for row in rows),
        "duplicate_seed_creation": 0,
        "decision_counts": dict(sorted(counts.items())),
        "candidate_ledger": candidate_path.as_posix(),
        "selection_config": config_path.as_posix(),
        "decision_ledger": output_path.as_posix(),
        "decision_ledger_bytes": len(payload.encode("utf-8")),
        "decision_ledger_sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
        "scope_statement": (
            "Bounded 2026-07-16..2026-07-21 arXiv delta only; exclusion means no current "
            "Stage-1B load-bearing map change, not literature irrelevance."
        ),
    }
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--known", type=Path, action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.candidates, args.config, args.known, args.output, args.summary)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
