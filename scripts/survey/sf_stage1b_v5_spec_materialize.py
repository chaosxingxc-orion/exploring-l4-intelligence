#!/usr/bin/env python3
"""Materialize the self-contained Stage-1B v5 release specification."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


BASE_SPEC = Path("wiki/survey/workbench/system-first-stage1b/2026-07-22-stage1b-release-v4-spec.json")
OUTPUT_SPEC = Path("wiki/survey/workbench/system-first-stage1b/2026-07-23-stage1b-release-v5-spec.json")

REPLACEMENTS = {
    "speech_direct_prior_supplement": {
        "path": "wiki/survey/current/data/stage1b-speech-direct-prior-supplement-v3.json",
        "producer": "scripts/survey/sf_stage1b_v5_materialize.py",
    },
    "speech_evidence_contract_checker": {
        "path": "scripts/survey/sf_stage1b_v5_evidence_contract.py",
        "producer": "Stage-1B v5 literature, inventory and asset contract",
    },
    "direct_control_basis": {
        "path": "wiki/survey/current/data/stage1b-direct-control-basis-v2.json",
        "producer": "scripts/survey/sf_stage1b_v5_materialize.py",
    },
    "stage1c_asset_matrix": {
        "role": "stage1b_v5_gate_asset_lock",
        "path": "docs/stage1b-v5-gate-assets.lock.json",
        "producer": "bounded official asset availability and revision lock",
    },
    "v4_evidence_contract_receipt": {
        "role": "v5_evidence_contract_receipt",
        "path": "docs/checks/stage1b-closeout/2026-07-23-v5/stage1b-v5-evidence-contract.json",
        "producer": "scripts/survey/sf_stage1b_v5_evidence_contract.py",
    },
    "layered_asset_inventory": {
        "role": "layered_asset_inventory_python",
        "path": "docs/checks/stage1b-closeout/2026-07-23-v5/speechrl-data-layered-inventory-python.json",
        "producer": "scripts/data/stage1c_asset_inventory.py",
    },
    "v4_supplement_materializer": {
        "role": "v5_supplement_materializer",
        "path": "scripts/survey/sf_stage1b_v5_materialize.py",
        "producer": "deterministic 18-work promotion and supplement materializer",
    },
    "v4_release_spec_materializer": {
        "role": "v5_release_spec_materializer",
        "path": "scripts/survey/sf_stage1b_v5_spec_materialize.py",
        "producer": "self-contained v5 spec materialized from the registered v4 release",
    },
}

ADDITIONS = [
    ("eligible_bundle_reconciliation", "wiki/survey/current/data/stage1b-eligible-bundle-reconciliation-v1.json", "closed six-gate plus 12-route canonical-ID reconciliation"),
    ("official_metadata_receipts", "wiki/survey/current/data/official-metadata-receipts-v1.jsonl", "official metadata provenance and raw-payload hashes"),
    ("reviewer_bibliography_selection", "wiki/survey/current/data/reviewer-bibliography-selection-v1.json", "135-work bibliography selection accounting"),
    ("current_bibliography", "wiki/survey/current/bibliography.md", "official-metadata bibliography generator"),
    ("v5_gate_fetcher", "scripts/data/fetch-stage1b-v5-gate-assets.sh", "unified lock-driven public asset acquisition"),
    ("unified_asset_downloader", "scripts/data/fetch-data.sh", "revision-pinned resumable downloader with verified HF completion markers"),
    ("layered_asset_inventory_powershell", "docs/checks/stage1b-closeout/2026-07-23-v5/speechrl-data-layered-inventory-powershell.json", "native NTFS inventory implementation"),
    ("audio2tool_content_accounting", "docs/checks/stage1b-closeout/2026-07-23-v5/speechrl-data-content-accounting.json", "remote, auxiliary and extraneous content split"),
    ("asset_content_auditor", "scripts/data/stage1c_asset_content_audit.py", "non-destructive revision-bound content accounting"),
    ("official_metadata_fetcher", "scripts/survey/sf_official_metadata_fetch.py", "exact-identity official metadata fetch and offline replay"),
    ("bibliography_generator", "scripts/survey/sf_bibliography_generator.py", "deterministic official-metadata bibliography generator"),
    ("fulltext_fetcher", "scripts/survey/sf_fulltext_fetch.py", "exact-ID PDF/e-print acquisition"),
]

CLOSED_IDS = (
    "2306.12577", "2410.21485", "2411.00321", "2506.05984", "2507.12705",
    "2510.00743", "2510.14664", "2511.07931", "2512.10170", "2512.10403",
    "2601.04029", "2603.09714", "2603.12520", "2603.19615", "2604.24278",
    "2605.23261", "2605.30256", "2606.24648",
)


def materialize(base: dict[str, Any]) -> dict[str, Any]:
    artifacts: list[dict[str, Any]] = []
    for source in base["artifacts"]:
        row = dict(source)
        row.update(REPLACEMENTS.get(str(row["role"]), {}))
        artifacts.append(row)
    artifacts.extend(
        {"role": role, "path": path, "location": "git", "producer": producer}
        for role, path, producer in ADDITIONS
    )
    for paper_id in CLOSED_IDS:
        for rendition in ("pdf", "eprint"):
            artifacts.append({
                "role": f"external_v5_fulltext_{paper_id}_{rendition}",
                "path": f"E:/chao_workspace/exploring-l4-intelligence/speechrl-data/survey-fulltext/{paper_id}/{paper_id}.{rendition}",
                "location": "external",
                "producer": "scripts/survey/sf_fulltext_fetch.py exact-ID acquisition",
            })
    roles = [str(row["role"]) for row in artifacts]
    paths = [str(row["path"]) for row in artifacts]
    if len(roles) != len(set(roles)) or len(paths) != len(set(paths)):
        raise ValueError("v5 release contains duplicate artifact role or path")
    return {
        "release_id": "system-first-stage1b-2026-07-23-v5",
        "stage": "STAGE_1B_LATE_CLOSEOUT",
        "scientific_release_scope": "EXCLUDES_MUTABLE_HOT_AND_STATUS_ROUTERS",
        "claim_limit": "Bounded literature-promotion, method-path, evidence-depth and asset-feasibility repair; no ranking, novelty verdict, model execution or reproduction authority.",
        "supersedes_release_id": base["release_id"],
        "denominators": {
            "original_four_source_identity_audit": 81,
            "known_prior_reconciliation": 9,
            "eligible_bundle_reconciliation": 18,
            "strict_speech_omni_supplement": 46,
            "direct_control_paths_in_supplement": 26,
            "legacy_schema_v7_paths": 11,
        },
        "artifacts": artifacts,
    }


def main() -> int:
    repo = Path(__file__).resolve().parents[2]
    base = json.loads((repo / BASE_SPEC).read_text(encoding="utf-8"))
    document = materialize(base)
    (repo / OUTPUT_SPEC).write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT_SPEC} ({len(document['artifacts'])} artifacts)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
