#!/usr/bin/env python3
"""Export the capped retained roster into metadata-only long-lived paper records."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def to_registry_record(row: dict[str, Any], source_sha256: str, dataset_lock_sha256: str) -> dict[str, Any]:
    aid = str(row["arxiv_id"])
    locators = [
        {
            key: locator.get(key)
            for key in ("page", "evidence_type", "matched_term")
            if locator.get(key) is not None
        }
        for locator in (row.get("evidence_locators") or [])
    ]
    datasets = [
        {
            key: item.get(key)
            for key in (
                "canonical_name", "task", "factor_family", "lock_status", "local_present",
                "task_suitability",
                "task_suitability_by_tag",
            )
            if item.get(key) is not None
        }
        for item in (row.get("speech_dataset_mentions") or [])
    ]
    repositories = [
        {
            key: item.get(key)
            for key in (
                "canonical_url", "paper_link_url", "status", "license_spdx", "code_present",
                "environment_present", "config_present", "weights_or_download_present",
                "evaluation_entrypoint_present", "reproduction_scope",
            )
            if item.get(key) is not None
        }
        for item in (row.get("repo_details") or [])
    ]
    decision = str(row["final_decision"])
    audit_reason = str(row.get("audit_override_reason") or "").strip()
    reasoning_summary = [audit_reason] if audit_reason else (row.get("final_reason_codes") or [])
    provenance = {
        "bounded_sampling_source_sha256": source_sha256,
        "dataset_lock_sha256": dataset_lock_sha256,
        "pdf_sha256": row.get("pdf_sha256"),
        "decision_origin": row.get("decision_origin"),
        "sample_round": row.get("sample_round"),
    }
    if row.get("preaudit_decision") is not None:
        provenance["preaudit_decision"] = row.get("preaudit_decision")
    if row.get("audit_override_evidence_pages") is not None:
        provenance["audit_override_evidence_pages"] = row.get("audit_override_evidence_pages")
    return {
        "schema": "sf-paper-registry-record-v1",
        "canonical_id": f"arxiv:{aid}",
        "arxiv_id": aid,
        "title": row.get("title"),
        "links": {
            "abstract": f"https://arxiv.org/abs/{aid}",
            "pdf": f"https://arxiv.org/pdf/{aid}",
            "eprint": f"https://arxiv.org/e-print/{aid}",
        },
        "conclusion": f"{decision}: retained in the bounded Stage-1B evidence portfolio.",
        "reasoning_summary": reasoning_summary,
        "purpose_chain": (
            "Stage-1B method-path/data/reproducibility map -> Stage-1C problem selection -> "
            "reproduction-first experiment environment"
        ),
        "role": decision,
        "speech_primary_object": bool(row.get("speech_primary_object")),
        "speech_task_tags": row.get("speech_task_tags") or [],
        "datasets": datasets,
        "method_path": {
            "signals": row.get("control_signal_terms") or [],
            "actions": row.get("decision_action_terms") or [],
            "no_update_evidence": row.get("no_update_terms") or [],
            "transfer_objects": row.get("transfer_object_terms") or [],
            "adverse_evidence": row.get("adverse_terms") or [],
        },
        "repository_status": row.get("repo_status"),
        "repositories": repositories,
        "evidence_locators": locators,
        "provenance": provenance,
        "invalidation_conditions": [
            "A later paper version changes the coded method path or experiment contract.",
            "Repository reachability, license, or artifact structure changes.",
            "The dataset lock or local task/split suitability assessment changes.",
            "A later audit supersedes the full-text decision with an explicit token.",
        ],
    }


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line.strip()]


def run(input_path: Path, output_path: Path, source_sha256: str, dataset_lock_sha256: str) -> dict[str, Any]:
    if output_path.exists():
        raise FileExistsError(f"registry is append-only; refusing to replace {output_path}")
    rows = _read_jsonl(input_path)
    records = [to_registry_record(row, source_sha256, dataset_lock_sha256) for row in rows]
    ids = [record["canonical_id"] for record in records]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate canonical ID in retained roster")
    payload = "".join(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(payload, encoding="utf-8", newline="\n")
    return {
        "schema": "sf-paper-registry-export-summary-v1",
        "records": len(records),
        "output_path": output_path.as_posix(),
        "output_bytes": len(payload.encode("utf-8")),
        "output_sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-sha256", required=True)
    parser.add_argument("--dataset-lock-sha256", required=True)
    args = parser.parse_args()
    print(
        json.dumps(
            run(args.input, args.output, args.source_sha256, args.dataset_lock_sha256),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
