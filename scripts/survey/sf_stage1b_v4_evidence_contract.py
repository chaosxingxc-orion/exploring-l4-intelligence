#!/usr/bin/env python3
"""Validate the bounded Stage-1B v4 repairs requested by the independent rereview."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import sf_stage1b_evidence_release_contract as v3_contract


COVERAGE_PATH = Path("wiki/survey/current/data/stage1b-speech-omni-prior-coverage-v1.json")
RECONCILIATION_PATH = Path("wiki/survey/current/data/stage1b-known-prior-reconciliation-v1.json")
SUPPLEMENT_PATH = Path("wiki/survey/current/data/stage1b-speech-direct-prior-supplement-v2.json")
CONTROL_BASIS_PATH = Path("wiki/survey/current/data/stage1b-direct-control-basis-v1.json")
REFERENCE_PATH = Path("wiki/survey/current/stage1b-transition-reference-appendix.md")
MAPPING_PATH = Path("wiki/survey/current/tables/stage1b-mapping-release.md")
ELIGIBLE_PATH = Path("wiki/survey/current/tables/stage1c-eligible-inputs.md")
LEDGER_PATH = Path("wiki/survey/2026-07-17-sf-fulltext-ledger.jsonl")
ASSET_MATRIX_PATH = Path("docs/checks/stage1b-closeout/2026-07-22-v4/stage1c-asset-acquisition-matrix.json")
LAYERED_INVENTORY_PATH = Path("docs/checks/stage1b-closeout/2026-07-22-v4/speechrl-data-layered-inventory.json")
RELEASE_SPEC_PATH = Path("wiki/survey/workbench/system-first-stage1b/2026-07-22-stage1b-release-v4-spec.json")

REQUIRED_RECONCILIATION_ROLES = {
    "2407.09886": "DIRECT_CONTROL_METHOD",
    "2304.12995": "DIRECT_CONTROL_METHOD",
    "2303.11381": "BOUNDARY_COMPARATOR",
    "2604.16456": "MEASUREMENT_INSTRUMENT",
    "2605.15104": "MEASUREMENT_INSTRUMENT",
    "2602.13685": "TRAINED_BOUNDARY",
    "2505.09558": "MEASUREMENT_INSTRUMENT",
    "2603.14889": "MEASUREMENT_INSTRUMENT",
    "2602.13891": "MEASUREMENT_INSTRUMENT",
}
ALLOWED_CONTROL_BASES = {
    "EXTERNAL_ORCHESTRATION_ONLY",
    "STATE_OR_EVENT_GATED",
    "EVALUATOR_OR_VERIFIER_GATED",
    "REWARD_GUIDED_SELECTION",
    "TRAINED_POLICY_BOUNDARY",
    "MEASUREMENT_ONLY",
}
CONTROL_REQUIRED_FIELDS = {
    "paper_work_id",
    "evidence_id",
    "control_basis",
    "reward_or_evaluator_identity",
    "signal_forms",
    "signal_changes_next_action",
    "next_action_effect",
    "controller_program_or_config_optimized_on_labels",
    "core_weight_update",
    "external_component_weight_update",
    "boundary_note",
}
REQUIRED_ASSETS = {
    "voiceagentbench",
    "tau-voice",
    "full-duplex-bench-v3",
    "audio2tool",
    "omni-deepsearch",
    "eva-bench",
    "ihbench",
    "lalm-audio-judge-reliability",
    "mmar",
    "mmau-mini",
    "soulx-duplug",
    "echochain",
    "from-text-to-voice",
}
REQUIRED_RELEASE_ROLES = {
    "strict_method_path_coding",
    "speech_prior_coverage",
    "known_prior_reconciliation",
    "speech_direct_prior_supplement",
    "direct_control_basis",
    "transition_reference_appendix",
    "mapping_release",
    "eligible_inputs",
    "stage1c_asset_matrix",
    "layered_asset_inventory",
    "fulltext_access_ledger",
}
RELEASE_ROLE_PATHS = {
    "strict_method_path_coding": "wiki/survey/current/data/known-item-coding-v7.json",
    "speech_prior_coverage": COVERAGE_PATH.as_posix(),
    "known_prior_reconciliation": RECONCILIATION_PATH.as_posix(),
    "speech_direct_prior_supplement": SUPPLEMENT_PATH.as_posix(),
    "direct_control_basis": CONTROL_BASIS_PATH.as_posix(),
    "transition_reference_appendix": REFERENCE_PATH.as_posix(),
    "mapping_release": MAPPING_PATH.as_posix(),
    "eligible_inputs": ELIGIBLE_PATH.as_posix(),
    "stage1c_asset_matrix": ASSET_MATRIX_PATH.as_posix(),
    "layered_asset_inventory": LAYERED_INVENTORY_PATH.as_posix(),
    "fulltext_access_ledger": LEDGER_PATH.as_posix(),
}


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def validate_reconciliation(document: Any) -> list[str]:
    if not isinstance(document, dict):
        return ["RECONCILIATION_DOCUMENT_NOT_OBJECT"]
    failures: list[str] = []
    if document.get("schema") != "sf-stage1b-known-prior-reconciliation-v1":
        failures.append("RECONCILIATION_SCHEMA_INVALID")
    if document.get("identity_policy") != "REUSE_CANONICAL_WORK_ID_NO_DUPLICATE_SEED_OR_CLAIM_WORK":
        failures.append("RECONCILIATION_IDENTITY_POLICY_INVALID")
    rows = document.get("rows")
    if not isinstance(rows, list):
        return [*failures, "RECONCILIATION_ROWS_NOT_ARRAY"]
    ids = [str(row.get("paper_work_id")) for row in rows if isinstance(row, dict)]
    if len(ids) != len(set(ids)):
        failures.append("RECONCILIATION_DUPLICATE_ID")
    if set(ids) != set(REQUIRED_RECONCILIATION_ROLES):
        failures.append("RECONCILIATION_REQUIRED_ID_MISMATCH")
    for row in rows:
        if not isinstance(row, dict):
            failures.append("RECONCILIATION_ROW_NOT_OBJECT")
            continue
        paper_id = str(row.get("paper_work_id"))
        if row.get("analysis_role") != REQUIRED_RECONCILIATION_ROLES.get(paper_id):
            failures.append(f"RECONCILIATION_ROLE_INVALID:{paper_id}")
        if row.get("seed_action") != "REUSE_CANONICAL_WORK_ID":
            failures.append(f"RECONCILIATION_SEED_ACTION_INVALID:{paper_id}")
        if row.get("depth") != "FULLTEXT_ROUTED":
            failures.append(f"RECONCILIATION_DEPTH_INVALID:{paper_id}")
        fulltext = row.get("fulltext_ref")
        if not isinstance(fulltext, dict) or len(str(fulltext.get("sha256", ""))) != 64:
            failures.append(f"RECONCILIATION_FULLTEXT_INVALID:{paper_id}")
    return failures


def validate_control_basis(control: Any, supplement: Any) -> list[str]:
    if not isinstance(control, dict) or not isinstance(supplement, dict):
        return ["CONTROL_BASIS_DOCUMENT_INVALID"]
    failures: list[str] = []
    if control.get("schema") != "sf-stage1b-direct-control-basis-v1":
        failures.append("CONTROL_BASIS_SCHEMA_INVALID")
    direct_ids = {
        row.get("paper_work_id")
        for row in supplement.get("rows", [])
        if isinstance(row, dict) and row.get("analysis_role") == "DIRECT_CONTROL_METHOD"
    }
    rows = control.get("rows")
    if not isinstance(rows, list):
        return [*failures, "CONTROL_BASIS_ROWS_NOT_ARRAY"]
    control_ids = [row.get("paper_work_id") for row in rows if isinstance(row, dict)]
    if set(control_ids) != direct_ids or len(control_ids) != len(set(control_ids)):
        failures.append("CONTROL_BASIS_DIRECT_ID_MISMATCH")
    for position, row in enumerate(rows):
        if not isinstance(row, dict):
            failures.append(f"CONTROL_BASIS_ROW_NOT_OBJECT:{position}")
            continue
        paper_id = str(row.get("paper_work_id"))
        for field in sorted(CONTROL_REQUIRED_FIELDS - set(row)):
            failures.append(f"CONTROL_BASIS_FIELD_MISSING:{paper_id}:{field}")
        if row.get("control_basis") not in ALLOWED_CONTROL_BASES:
            failures.append(f"CONTROL_BASIS_CLASS_INVALID:{paper_id}")
        if row.get("signal_changes_next_action") is not True:
            failures.append(f"CONTROL_BASIS_NO_ACTION_EFFECT:{paper_id}")
    return failures


def validate_supplement_sources(coverage: Any, reconciliation: Any, supplement: Any) -> list[str]:
    coverage_ids = {
        row.get("paper_work_id")
        for row in coverage.get("rows", [])
        if isinstance(row, dict) and row.get("supplement_status") == "INCLUDED"
    }
    reconciliation_ids = {
        row.get("paper_work_id")
        for row in reconciliation.get("rows", [])
        if isinstance(row, dict) and row.get("supplement_status") == "INCLUDED"
    }
    supplement_ids = [
        row.get("paper_work_id")
        for row in supplement.get("rows", [])
        if isinstance(row, dict)
    ]
    if set(supplement_ids) != coverage_ids | reconciliation_ids or len(supplement_ids) != len(set(supplement_ids)):
        return ["SUPPLEMENT_SOURCE_ID_MISMATCH"]
    return []


def validate_asset_matrix(document: Any) -> list[str]:
    if not isinstance(document, dict):
        return ["ASSET_MATRIX_DOCUMENT_NOT_OBJECT"]
    failures: list[str] = []
    policy = str(document.get("data_policy", "")).casefold()
    if "never committed" not in policy or "git" not in policy:
        failures.append("ASSET_NO_GIT_DATA_POLICY_MISSING")
    assets = document.get("assets")
    if not isinstance(assets, list):
        return [*failures, "ASSET_MATRIX_ROWS_NOT_ARRAY"]
    by_id = {row.get("asset_id"): row for row in assets if isinstance(row, dict)}
    if set(by_id) != REQUIRED_ASSETS or len(by_id) != len(assets):
        failures.append("ASSET_REQUIRED_ID_MISMATCH")
    for asset_id, row in by_id.items():
        for field in (
            "paper_pdf_status",
            "author_repo_status",
            "dataset_status",
            "license_access",
            "stage2_reproduction_blocker",
        ):
            if field not in row:
                failures.append(f"ASSET_FIELD_MISSING:{asset_id}:{field}")
        dataset = row.get("dataset_status", {})
        local_path = dataset.get("local_path") if isinstance(dataset, dict) else None
        if local_path is not None and not str(local_path).startswith("${SPEECHRL_DATA_DIR}/"):
            failures.append(f"ASSET_LOCAL_PATH_ESCAPES_DATA_ROOT:{asset_id}")
    voice = by_id.get("voiceagentbench", {}).get("dataset_status", {})
    if "different dataset" not in str(voice.get("identity_warning", "")).casefold():
        failures.append("ASSET_VOICE_IDENTITY_WARNING_MISSING")
    tau = by_id.get("tau-voice", {}).get("dataset_status", {})
    if "not by itself" not in str(tau.get("identity_warning", "")).casefold():
        failures.append("ASSET_TAU_IDENTITY_WARNING_MISSING")
    if by_id.get("audio2tool", {}).get("dataset_status", {}).get("status") != "LOCAL_REVISION_PINNED_COMPLETE":
        failures.append("ASSET_AUDIO2TOOL_STATUS_INVALID")
    if by_id.get("eva-bench", {}).get("dataset_status", {}).get("status") != "LOCAL_BASELINE_LOCKED":
        failures.append("ASSET_EVA_STATUS_INVALID")
    return failures


def validate_fulltext_bindings(
    rows: list[dict[str, Any]],
    ledger: list[dict[str, Any]],
    *,
    data_root: Path | None = None,
) -> list[str]:
    failures: list[str] = []
    successful: dict[str, dict[str, Any]] = {}
    for event in ledger:
        if (
            event.get("kind") == "pdf"
            and event.get("http_status") == 200
            and event.get("error") is None
            and isinstance(event.get("sha256"), str)
        ):
            successful[str(event.get("arxiv_id"))] = event
    expected: dict[str, set[str]] = {}
    for row in rows:
        if row.get("depth") != "FULLTEXT_ROUTED":
            continue
        paper_id = str(row.get("paper_work_id"))
        ref = row.get("fulltext_ref")
        sha = ref.get("sha256") if isinstance(ref, dict) else None
        if isinstance(sha, str):
            expected.setdefault(paper_id, set()).add(sha)
        event = successful.get(paper_id)
        if event is None:
            failures.append(f"FULLTEXT_LEDGER_SUCCESS_MISSING:{paper_id}")
            continue
        if sha is not None and sha != event.get("sha256"):
            failures.append(f"FULLTEXT_LEDGER_SHA_MISMATCH:{paper_id}")
        if data_root is not None:
            stored_at = event.get("stored_at")
            if not isinstance(stored_at, str) or not stored_at:
                failures.append(f"FULLTEXT_LEDGER_PATH_MISSING:{paper_id}")
                continue
            normalized = stored_at.replace("\\", "/")
            marker = "/speechrl-data/"
            if marker in normalized:
                pdf = data_root / normalized.split(marker, 1)[1]
            else:
                pdf = Path(stored_at)
            if not pdf.is_file():
                failures.append(f"FULLTEXT_LOCAL_PDF_MISSING:{paper_id}")
                continue
            if pdf.stat().st_size != event.get("bytes"):
                failures.append(f"FULLTEXT_LOCAL_BYTES_MISMATCH:{paper_id}")
            actual_sha = hashlib.sha256(pdf.read_bytes()).hexdigest()
            if actual_sha != event.get("sha256"):
                failures.append(f"FULLTEXT_LOCAL_SHA_MISMATCH:{paper_id}")
    for paper_id, hashes in expected.items():
        if len(hashes) > 1:
            failures.append(f"FULLTEXT_CONFLICTING_EXPECTED_SHA:{paper_id}")
    return sorted(set(failures))


def validate_release_spec(spec: Any) -> list[str]:
    if not isinstance(spec, dict):
        return ["RELEASE_SPEC_NOT_OBJECT"]
    failures: list[str] = []
    if spec.get("release_id") != "system-first-stage1b-2026-07-22-v4":
        failures.append("RELEASE_ID_INVALID")
    if spec.get("scientific_release_scope") != "EXCLUDES_MUTABLE_HOT_AND_STATUS_ROUTERS":
        failures.append("RELEASE_SCIENTIFIC_SCOPE_INVALID")
    artifacts = spec.get("artifacts")
    if not isinstance(artifacts, list):
        return [*failures, "RELEASE_ARTIFACTS_NOT_ARRAY"]
    roles = [row.get("role") for row in artifacts if isinstance(row, dict)]
    if not REQUIRED_RELEASE_ROLES.issubset(set(roles)) or len(roles) != len(set(roles)):
        failures.append("RELEASE_REQUIRED_ROLE_MISMATCH")
    if {"hot_state", "current_status", "current_router"} & set(roles):
        failures.append("RELEASE_MUTABLE_ROUTER_INCLUDED")
    for row in artifacts:
        if (
            isinstance(row, dict)
            and row.get("role") in RELEASE_ROLE_PATHS
            and RELEASE_ROLE_PATHS[row["role"]] != row.get("path")
        ):
            failures.append(f"RELEASE_ROLE_PATH_MISMATCH:{row.get('role')}")
    return failures


def _fulltext_rows(coverage: Any, reconciliation: Any, supplement: Any) -> list[dict[str, Any]]:
    rows = []
    rows.extend(row for row in coverage.get("rows", []) if isinstance(row, dict))
    rows.extend(row for row in reconciliation.get("rows", []) if isinstance(row, dict))
    rows.extend(
        {**row, "depth": "FULLTEXT_ROUTED"}
        for row in supplement.get("rows", [])
        if isinstance(row, dict)
    )
    return rows


def validate_repository(repo: Path, *, require_local: bool, data_root: Path | None = None) -> list[str]:
    repo = Path(repo)
    required_paths = (
        COVERAGE_PATH,
        RECONCILIATION_PATH,
        SUPPLEMENT_PATH,
        CONTROL_BASIS_PATH,
        REFERENCE_PATH,
        MAPPING_PATH,
        ELIGIBLE_PATH,
        LEDGER_PATH,
        ASSET_MATRIX_PATH,
        LAYERED_INVENTORY_PATH,
        RELEASE_SPEC_PATH,
    )
    missing = [f"REPOSITORY_ARTIFACT_MISSING:{path.as_posix()}" for path in required_paths if not (repo / path).is_file()]
    if missing:
        return missing
    try:
        coverage = _load_json(repo / COVERAGE_PATH)
        reconciliation = _load_json(repo / RECONCILIATION_PATH)
        supplement = _load_json(repo / SUPPLEMENT_PATH)
        control = _load_json(repo / CONTROL_BASIS_PATH)
        assets = _load_json(repo / ASSET_MATRIX_PATH)
        layered = _load_json(repo / LAYERED_INVENTORY_PATH)
        release = _load_json(repo / RELEASE_SPEC_PATH)
        ledger = _load_jsonl(repo / LEDGER_PATH)
        references = (repo / REFERENCE_PATH).read_text(encoding="utf-8")
        mapping = (repo / MAPPING_PATH).read_text(encoding="utf-8")
        eligible = (repo / ELIGIBLE_PATH).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        return [f"REPOSITORY_JSON_INVALID:{error}"]
    failures = validate_reconciliation(reconciliation)
    failures.extend(v3_contract.validate_coverage(coverage))
    v3_shape = {**supplement, "schema": v3_contract.SUPPLEMENT_SCHEMA}
    failures.extend(v3_contract.validate_supplement(v3_shape))
    failures.extend(validate_supplement_sources(coverage, reconciliation, supplement))
    failures.extend(v3_contract.validate_reference_appendix(references, supplement))
    failures.extend(v3_contract.validate_reference_tokens([mapping, eligible], supplement))
    failures.extend(validate_control_basis(control, supplement))
    failures.extend(validate_asset_matrix(assets))
    if layered.get("layers", [{}])[0].get("missing_locked_paths"):
        failures.append("LAYERED_INVENTORY_BASELINE_MISSING")
    local_root = data_root if require_local else None
    failures.extend(validate_fulltext_bindings(_fulltext_rows(coverage, reconciliation, supplement), ledger, data_root=local_root))
    failures.extend(validate_release_spec(release))
    return failures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path)
    parser.add_argument("--require-local", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = Path(__file__).resolve().parents[2]
    failures = validate_repository(repo, require_local=args.require_local, data_root=args.data_root)
    for failure in failures:
        print(f"[STAGE1B-V4] {failure}")
    print(f"Stage-1B v4 evidence contract: {'FAIL' if failures else 'PASS'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
