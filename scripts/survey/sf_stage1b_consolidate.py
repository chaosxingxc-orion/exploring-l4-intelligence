#!/usr/bin/env python3
"""Consolidate audited Stage-1B full-text decisions into the capped retained roster."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any


KEEP_LABELS = ("KEEP_CORE", "KEEP_TRANSFER", "KEEP_INSTRUMENT", "KEEP_NEGATIVE")
DECISION_WEIGHT = {
    "KEEP_CORE": 100,
    "KEEP_TRANSFER": 90,
    "KEEP_INSTRUMENT": 80,
    "KEEP_NEGATIVE": 70,
}


def apply_overrides(rows: list[dict[str, Any]], overrides: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result = [copy.deepcopy(row) for row in rows]
    by_id = {str(row["arxiv_id"]): row for row in result}
    seen = set()
    for override in overrides:
        aid = str(override.get("arxiv_id"))
        if aid in seen:
            raise ValueError(f"duplicate audit override: {aid}")
        seen.add(aid)
        if aid not in by_id:
            raise ValueError(f"audit override targets missing ID: {aid}")
        row = by_id[aid]
        if row.get("final_decision") != override.get("from_decision"):
            raise ValueError(f"from_decision mismatch for {aid}")
        target = override.get("to_decision")
        if target not in set(KEEP_LABELS) | {"DROP"}:
            raise ValueError(f"invalid to_decision for {aid}: {target}")
        if not str(override.get("reason") or "").strip() or not override.get("evidence_pages"):
            raise ValueError(f"audit override lacks reason/evidence pages: {aid}")
        row["preaudit_decision"] = row["final_decision"]
        row["final_decision"] = target
        row["audit_override_reason"] = override["reason"]
        row["audit_override_evidence_pages"] = override["evidence_pages"]
        row["decision_origin"] = "BOUNDED_FULLTEXT_AUDIT_OVERRIDE"
        if "speech_primary_object" in override:
            speech_primary = override["speech_primary_object"]
            if not isinstance(speech_primary, bool):
                raise ValueError(f"speech_primary_object override must be boolean for {aid}")
            row["speech_primary_object"] = speech_primary
        if "dataset_local_status" in override:
            local_status = str(override["dataset_local_status"])
            allowed_local_statuses = {
                "LOCAL_MATCH",
                "LOCK_MATCH_NOT_PRESENT",
                "NAMED_DATASET_NOT_IN_LOCK",
                "NOT_STATED_IN_FULLTEXT",
                "NOT_APPLICABLE_NON_SPEECH",
            }
            if local_status not in allowed_local_statuses:
                raise ValueError(f"invalid dataset_local_status override for {aid}: {local_status}")
            row["dataset_local_status"] = local_status
        if "speech_task_tags" in override:
            tags = sorted({str(tag).strip() for tag in override["speech_task_tags"] if str(tag).strip()})
            row["speech_task_tags"] = tags
            for field in ("dataset_mentions", "speech_dataset_mentions"):
                for dataset in row.get(field) or []:
                    dataset_task = str(dataset.get("task") or "").lower()
                    by_tag = {
                        tag: (
                            "TASK_MATCH"
                            if dataset_task and (tag in dataset_task or dataset_task in tag)
                            else "REQUIRES_SPLIT_REVIEW"
                        )
                        for tag in tags
                    }
                    dataset["task_suitability_by_tag"] = by_tag
                    dataset["task_suitability"] = (
                        "TASK_MATCH"
                        if "TASK_MATCH" in by_tag.values()
                        else "REQUIRES_SPLIT_REVIEW"
                    )
    return result


def _score(row: dict[str, Any]) -> int:
    return (
        DECISION_WEIGHT[row["final_decision"]]
        + 20 * (bool(row.get("speech_primary_object")) and row.get("dataset_local_status") == "LOCAL_MATCH")
        + 10 * (row.get("repo_status") == "OPEN_SOURCE_VERIFIED")
        + min(8, len(row.get("evidence_locators") or []))
        + min(5, len(row.get("speech_task_tags") or []))
    )


def consolidate(rows: list[dict[str, Any]], cap: int = 1000) -> list[dict[str, Any]]:
    if cap < 1:
        raise ValueError("cap must be positive")
    ids = [str(row.get("arxiv_id")) for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate canonical arXiv ID in full-text ledger")
    candidates = [dict(row) for row in rows if row.get("final_decision") in KEEP_LABELS]
    candidates.sort(key=lambda row: (-_score(row), str(row["arxiv_id"])))
    retained = []
    for rank, row in enumerate(candidates[:cap], start=1):
        row["retained_rank"] = rank
        row["retained_priority_score"] = _score(row)
        row["retained_schema"] = "sf-stage1b-retained-paper-v1"
        retained.append(row)
    return retained


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line.strip()]


def run(
    input_path: Path | list[Path],
    output_dir: Path,
    cap: int,
    overrides_path: Path | list[Path] | None = None,
) -> dict[str, Any]:
    input_paths = [input_path] if isinstance(input_path, Path) else list(input_path)
    if not input_paths:
        raise ValueError("at least one input ledger is required")
    rows = [row for path in input_paths for row in _read_jsonl(path)]
    override_count = 0
    override_paths: list[Path] = []
    if overrides_path:
        override_paths = [overrides_path] if isinstance(overrides_path, Path) else list(overrides_path)
        overrides = [
            override
            for path in override_paths
            for override in json.loads(path.read_text("utf-8"))
        ]
        rows = apply_overrides(rows, overrides)
        override_count = len(overrides)
    retained = consolidate(rows, cap)
    output_dir.mkdir(parents=True, exist_ok=True)
    roster_path = output_dir / "retained-papers.jsonl"
    payload = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in retained)
    roster_path.write_text(payload, encoding="utf-8", newline="\n")

    decision_counts = {label: sum(row["final_decision"] == label for row in retained) for label in KEEP_LABELS}
    task_counts: dict[str, int] = {}
    dataset_counts: dict[str, int] = {}
    task_dataset_counts: dict[str, int] = {}
    for row in retained:
        for task in row.get("speech_task_tags") or []:
            task_counts[task] = task_counts.get(task, 0) + 1
        for dataset in row.get("speech_dataset_mentions") or []:
            name = dataset["canonical_name"]
            dataset_counts[name] = dataset_counts.get(name, 0) + 1
            if row.get("speech_primary_object"):
                for task in row.get("speech_task_tags") or ["unclassified_speech"]:
                    suitability = (dataset.get("task_suitability_by_tag") or {}).get(
                        task, dataset.get("task_suitability", "UNKNOWN")
                    )
                    key = f"{task}|{name}|{suitability}"
                    task_dataset_counts[key] = task_dataset_counts.get(key, 0) + 1
    unresolved = sum(
        row.get("final_decision") in {"DEFER_DOWNLOAD", "DEFER_EXTRACTION", "DEFER_REPO_VERIFY"}
        for row in rows
    )
    sample_rounds = [
        int(row["sample_round"])
        for row in rows
        if str(row.get("sample_round", "")).isdigit()
    ]
    maximum_sample_round = max(sample_rounds, default=None)
    summary = {
        "schema": "sf-stage1b-retained-roster-summary-v1",
        "source_input_count": len(input_paths),
        "source_inputs": [
            {
                "path": path.as_posix(),
                "bytes": path.stat().st_size,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
            for path in input_paths
        ],
        "source_rows": len(rows),
        "retained_unique": len(retained),
        "retained_cap": cap,
        "cap_is_maximum_not_quota": True,
        "scan_stop_after_round_3": maximum_sample_round == 3,
        "scan_stop_after_bounded_batch": True,
        "maximum_sample_round_seen": maximum_sample_round,
        "unresolved_rows_at_consolidation": unresolved,
        "audit_override_receipt_count": len(override_paths),
        "audit_override_count": override_count,
        "decision_counts": decision_counts,
        "speech_task_counts": dict(sorted(task_counts.items())),
        "dataset_counts": dict(sorted(dataset_counts.items())),
        "speech_task_dataset_suitability_counts": dict(sorted(task_dataset_counts.items())),
        "retained_primary_speech_local_match": sum(
            bool(row.get("speech_primary_object")) and row.get("dataset_local_status") == "LOCAL_MATCH"
            for row in retained
        ),
        "roster_path": roster_path.as_posix(),
        "roster_bytes": len(payload.encode("utf-8")),
        "roster_sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
    }
    (output_dir / "retained-roster-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, action="append", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--cap", type=int, default=1000)
    parser.add_argument("--overrides", type=Path, action="append")
    args = parser.parse_args()
    print(json.dumps(run(args.input, args.output_dir, args.cap, args.overrides), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
