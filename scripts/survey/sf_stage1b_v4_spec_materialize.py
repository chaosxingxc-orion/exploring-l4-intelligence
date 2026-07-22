#!/usr/bin/env python3
"""Materialize the self-contained v4 release spec from the registered v3 release."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


BASE_SPEC = Path("wiki/survey/workbench/system-first-stage1b/2026-07-22-stage1b-release-v3-spec.json")
OUTPUT_SPEC = Path("wiki/survey/workbench/system-first-stage1b/2026-07-22-stage1b-release-v4-spec.json")

REPLACEMENTS = {
    "speech_direct_prior_supplement": {
        "path": "wiki/survey/current/data/stage1b-speech-direct-prior-supplement-v2.json",
        "producer": "scripts/survey/sf_stage1b_v4_materialize.py",
    },
    "speech_evidence_contract_checker": {
        "path": "scripts/survey/sf_stage1b_v4_evidence_contract.py",
        "producer": "Stage-1B v4 executable evidence-depth and reconciliation contract",
    },
}

ADDITIONS = [
    ("known_prior_reconciliation", "wiki/survey/current/data/stage1b-known-prior-reconciliation-v1.json", "bounded nine-work seed/bibliography/registry reconciliation"),
    ("direct_control_basis", "wiki/survey/current/data/stage1b-direct-control-basis-v1.json", "scripts/survey/sf_stage1b_v4_materialize.py"),
    ("stage1c_asset_matrix", "docs/checks/stage1b-closeout/2026-07-22-v4/stage1c-asset-acquisition-matrix.json", "exact paper/code/data acquisition audit"),
    ("v4_evidence_contract_receipt", "docs/checks/stage1b-closeout/2026-07-22-v4/stage1b-v4-evidence-contract.json", "local fulltext, reconciliation, control-basis and asset-layer contract receipt"),
    ("layered_asset_inventory", "docs/checks/stage1b-closeout/2026-07-22-v4/speechrl-data-layered-inventory.json", "scripts/data/stage1c-asset-inventory.ps1"),
    ("frozen_baseline_lock", "docs/datasets.lock.json", "baseline-scope correction; asset rows unchanged"),
    ("stage1c_candidate_downloader", "scripts/data/fetch-candidates.sh", "revision/size verified public candidate downloader"),
    ("hf_completeness_checker", "scripts/data/hf_complete.py", "resolved-revision remote/local file checker"),
    ("layered_inventory_python", "scripts/data/stage1c_asset_inventory.py", "portable layered inventory implementation"),
    ("layered_inventory_windows", "scripts/data/stage1c-asset-inventory.ps1", "native NTFS layered inventory implementation"),
    ("v4_supplement_materializer", "scripts/survey/sf_stage1b_v4_materialize.py", "deterministic supplement/control-basis materializer"),
    ("v4_release_spec_materializer", "scripts/survey/sf_stage1b_v4_spec_materialize.py", "self-contained v4 spec materialized from the registered v3 release"),
    ("v3_compatibility_contract", "scripts/survey/sf_stage1b_evidence_release_contract.py", "forward-compatible validation of original v3 coverage and supplement"),
    ("release_manifest_materializer", "scripts/survey/sf_stage1b_release_manifest.py", "cross-platform deterministic release-manifest materializer"),
    ("release_replay_checker", "scripts/survey/sf_stage1b_release_replay.py", "commit-bound Git blob and external-asset replay checker"),
]


def materialize(base: dict[str, Any]) -> dict[str, Any]:
    artifacts = []
    for source in base["artifacts"]:
        row = dict(source)
        row.update(REPLACEMENTS.get(row["role"], {}))
        artifacts.append(row)
    artifacts.extend(
        {"role": role, "path": path, "location": "git", "producer": producer}
        for role, path, producer in ADDITIONS
    )
    roles = [row["role"] for row in artifacts]
    paths = [row["path"] for row in artifacts]
    if len(roles) != len(set(roles)) or len(paths) != len(set(paths)):
        raise ValueError("v4 release contains duplicate role or path")
    return {
        "release_id": "system-first-stage1b-2026-07-22-v4",
        "stage": "STAGE_1B_LATE_CLOSEOUT",
        "scientific_release_scope": "EXCLUDES_MUTABLE_HOT_AND_STATUS_ROUTERS",
        "claim_limit": "Bounded method-path, known-prior, evidence-depth and asset-feasibility release; no ranking, novelty verdict, model execution or reproduction authority.",
        "supersedes_release_id": base["release_id"],
        "denominators": {
            "original_four_source_identity_audit": 81,
            "known_prior_reconciliation": 9,
            "strict_speech_omni_supplement": 39,
            "direct_control_paths_in_supplement": 25,
            "legacy_schema_v7_paths": 11,
        },
        "artifacts": artifacts,
    }


def main() -> int:
    repo = Path(__file__).resolve().parents[2]
    base = json.loads((repo / BASE_SPEC).read_text(encoding="utf-8"))
    document = materialize(base)
    (repo / OUTPUT_SPEC).write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote {OUTPUT_SPEC} ({len(document['artifacts'])} artifacts)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
