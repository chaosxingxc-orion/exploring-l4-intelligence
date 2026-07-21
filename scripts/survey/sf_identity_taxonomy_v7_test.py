#!/usr/bin/env python3
"""Evidence-v7 platform-leaf runner for the Stage-1A release gate."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import sys
import tempfile
from collections import Counter
from pathlib import Path

from sf_coding_generator import render
from sf_evidence_contract import (
    validate_absence_cross_bindings,
    validate_bound_values,
)
from sf_identity_taxonomy_v6_test import (
    EvidenceCache,
    occupancy,
    reconcile_v6,
    validate,
)
from sf_json_contract import canonical_bytes, read as read_strict_json
from sf_h5_calibration_contract import validate_completion as validate_h5_completion
from sf_pdf_extractor_contract import (
    replay_toolgate_probe,
    runtime_stamp as pdf_runtime_stamp,
    validate_contract as validate_pdf_contract,
    validate_runtime as validate_pdf_runtime,
)
from sf_schema_v3_release_contract import (
    FINAL_SIDECAR_NAMES,
    SIDECAR_DIRECTORY_RELATIVE_PATH,
    resolve_trusted_repo_path,
    validate_coding_lineage,
)


REPO = Path(__file__).resolve().parents[2]
ARTIFACT_ID = "SF-IDENTITY-TAXONOMY-V7-TEST-2026-07-21-03"
CONTRACT_VERSION = "SF-EVIDENCE-V7-CONTRACT-4"
IMPLEMENTATION_FREEZE = "d4ec803417e1e9cfe9120afbce97c676cebbe6ee"
RUNNER_RELATIVE_PATH = "scripts/survey/sf_identity_taxonomy_v7_test.py"
TAXONOMY_V5_RELATIVE_PATH = "wiki/survey/2026-07-19-sf-identity-taxonomy-v5.json"
TAXONOMY_V6_RELATIVE_PATH = "wiki/survey/current/data/identity-taxonomy-v6.json"
CODING_RELATIVE_PATH = "wiki/survey/current/data/known-item-coding-v7.json"
SCHEMA_V3_ADJUDICATION_RELATIVE_PATH = (
    "wiki/survey/current/data/schema-v3-adjudication.json"
)
ABSENCE_ADJUDICATION_RELATIVE_PATH = (
    "wiki/survey/current/data/absence-evidence-adjudication-v3.json"
)
SEMANTIC_CORRECTIONS_RELATIVE_PATH = (
    "wiki/survey/current/data/negative-evidence-semantic-corrections-v2.json"
)
H5_CALIBRATION_RELATIVE_PATH = (
    "wiki/survey/current/data/modality-specificity-calibration-v1.json"
)
PDF_EXTRACTOR_CONTRACT_RELATIVE_PATH = (
    "wiki/survey/current/data/pdf-extractor-environment-v1.json"
)
ACTIVE_TAXONOMY = TAXONOMY_V6_RELATIVE_PATH


def _repo_path(relative):
    return REPO.joinpath(*relative.split("/"))


def _read_repo_json(relative):
    resolved = resolve_trusted_repo_path(
        REPO,
        _repo_path(relative),
        expected_relative=relative,
        expected_kind="file",
    )
    return read_strict_json(resolved)


def _provenance(relative, raw):
    return {"path": relative, "sha256": hashlib.sha256(raw).hexdigest()}


def load_current_inputs():
    """Strict-load the current v7 candidate without a circular fixed hash."""
    taxonomy_v5, taxonomy_v5_raw = _read_repo_json(TAXONOMY_V5_RELATIVE_PATH)
    taxonomy_v6, taxonomy_v6_raw = _read_repo_json(TAXONOMY_V6_RELATIVE_PATH)
    coding, coding_raw = _read_repo_json(CODING_RELATIVE_PATH)
    schema_adjudication, schema_adjudication_raw = _read_repo_json(
        SCHEMA_V3_ADJUDICATION_RELATIVE_PATH
    )
    absence_adjudication, absence_adjudication_raw = _read_repo_json(
        ABSENCE_ADJUDICATION_RELATIVE_PATH
    )
    semantic_corrections, semantic_corrections_raw = _read_repo_json(
        SEMANTIC_CORRECTIONS_RELATIVE_PATH
    )
    h5_calibration, h5_calibration_raw = _read_repo_json(
        H5_CALIBRATION_RELATIVE_PATH
    )
    pdf_extractor_contract, pdf_extractor_contract_raw = _read_repo_json(
        PDF_EXTRACTOR_CONTRACT_RELATIVE_PATH
    )

    sidecar_dir = resolve_trusted_repo_path(
        REPO,
        _repo_path(SIDECAR_DIRECTORY_RELATIVE_PATH),
        expected_relative=SIDECAR_DIRECTORY_RELATIVE_PATH,
        expected_kind="dir",
    )
    names = tuple(sorted(path.name for path in sidecar_dir.iterdir()))
    if names != FINAL_SIDECAR_NAMES:
        raise ValueError(
            f"active sidecar inventory mismatch expected={FINAL_SIDECAR_NAMES} "
            f"found={names}"
        )
    sidecars = []
    sidecar_provenance = []
    for name in names:
        relative = f"{SIDECAR_DIRECTORY_RELATIVE_PATH}/{name}"
        document, raw = _read_repo_json(relative)
        sidecars.append((name, document))
        sidecar_provenance.append(_provenance(relative, raw))

    try:
        coding_text = coding_raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError(f"coding UTF-8 decode failed: {error}") from error
    expected_coding = render(
        sidecars, taxonomy=ACTIVE_TAXONOMY, profile="v7"
    )
    if coding_text != expected_coding:
        raise ValueError("active coding is not byte-identical to sidecar projection")
    validate_coding_lineage(coding, REPO)
    rows = coding.get("rows") if isinstance(coding, dict) else None
    if not isinstance(rows, list):
        raise ValueError("active coding rows container invalid")

    provenance = {
        "taxonomy_v5": _provenance(TAXONOMY_V5_RELATIVE_PATH, taxonomy_v5_raw),
        "taxonomy": _provenance(TAXONOMY_V6_RELATIVE_PATH, taxonomy_v6_raw),
        "coding": _provenance(CODING_RELATIVE_PATH, coding_raw),
        "schema_v3_adjudication": _provenance(
            SCHEMA_V3_ADJUDICATION_RELATIVE_PATH, schema_adjudication_raw
        ),
        "absence_adjudication": _provenance(
            ABSENCE_ADJUDICATION_RELATIVE_PATH, absence_adjudication_raw
        ),
        "semantic_corrections": _provenance(
            SEMANTIC_CORRECTIONS_RELATIVE_PATH, semantic_corrections_raw
        ),
        "h5_calibration": _provenance(
            H5_CALIBRATION_RELATIVE_PATH, h5_calibration_raw
        ),
        "pdf_extractor_contract": _provenance(
            PDF_EXTRACTOR_CONTRACT_RELATIVE_PATH, pdf_extractor_contract_raw
        ),
        "sidecars": sidecar_provenance,
    }
    return {
        "taxonomy_v5": taxonomy_v5,
        "taxonomy_v6": taxonomy_v6,
        "coding": coding,
        "coding_text": coding_text,
        "rows": rows,
        "sidecars": sidecars,
        "schema_v3_adjudication": schema_adjudication,
        "absence_adjudication": absence_adjudication,
        "semantic_corrections": semantic_corrections,
        "h5_calibration": h5_calibration,
        "pdf_extractor_contract": pdf_extractor_contract,
        "input_provenance": provenance,
        "input_snapshot_sha256": hashlib.sha256(
            canonical_bytes(provenance)
        ).hexdigest(),
    }


def run_absence_mutation_suite(rows):
    """Prove an allowed negative control and the reviewer's positive mutation."""
    source = next(
        row
        for row in rows
        if row.get("claim_evidence", {})
        .get("human_or_dev_label_model_selection", {})
        .get("kind")
        == "absence"
    )
    negative = copy.deepcopy(source)
    positive = copy.deepcopy(source)
    positive["human_or_dev_label_model_selection"] = True
    positive["claim_evidence"]["human_or_dev_label_model_selection"]["value"] = True
    return {
        "legitimate_field_specific_negative_control": validate_bound_values(negative),
        "positive_categorical_absence": validate_bound_values(positive),
    }


def _expected_proof_rows(bundle):
    expected = {}
    for filename, sidecar in bundle["sidecars"]:
        sidecar_path = f"{SIDECAR_DIRECTORY_RELATIVE_PATH}/{filename}"
        for row in sidecar.get("method_paths", []):
            pid = row.get("method_path_id")
            for field, entry in row.get("claim_evidence", {}).items():
                if not isinstance(entry, dict) or entry.get("kind") != "absence":
                    continue
                row_id = entry.get("adjudication_row_id")
                expected[row_id] = {
                    "adjudication_row_id": row_id,
                    "source_tuple": [
                        pid,
                        "row",
                        field,
                        "absence",
                        json.dumps(
                            entry.get("value"),
                            ensure_ascii=False,
                            sort_keys=True,
                            separators=(",", ":"),
                        ),
                    ],
                    "method_path_id": pid,
                    "owner_kind": "row",
                    "field": field,
                    "value": entry.get("value"),
                    "proof_obligation_id": entry.get("proof_obligation_id"),
                    "inspected_locators": entry.get("inspected_locators"),
                    "reason": entry.get("reason"),
                    "counterevidence_search_scope": entry.get(
                        "counterevidence_search_scope"
                    ),
                    "counterevidence_locators": entry.get(
                        "counterevidence_locators"
                    ),
                    "temporal_order_resolved": entry.get(
                        "temporal_order_resolved"
                    ),
                    "why_counterevidence_does_not_change_verdict": entry.get(
                        "why_counterevidence_does_not_change_verdict"
                    ),
                    "owner_sidecar": sidecar_path,
                    "fulltext": entry.get("fulltext"),
                    "coder_identity": entry.get("coder_identity"),
                    "owner_row_sha256": entry.get("owner_row_sha256"),
                }
    return expected


def validate_review_inventory(bundle):
    """Validate exact proof/review coverage before semantic cross-binding."""
    failures = []
    artifact = bundle.get("absence_adjudication")
    if not isinstance(artifact, dict):
        return ["absence-review-artifact-invalid"]
    proof_rows = artifact.get("proof_rows")
    review_rows = artifact.get("rows")
    if not isinstance(proof_rows, list):
        failures.append("absence-review-proof-rows-invalid")
        proof_rows = []
    if not isinstance(review_rows, list):
        failures.append("absence-review-rows-invalid")
        review_rows = []

    expected = _expected_proof_rows(bundle)
    corrections = bundle.get("semantic_corrections", {}).get("corrections", [])
    if (
        artifact.get("original_proof_inventory_count") != 22
        or artifact.get("retired_by_semantic_correction_count") != len(corrections)
        or artifact.get("active_proof_inventory_count") != len(expected)
        or artifact.get("inventory_identity")
        != f"22 = {len(corrections)} + {len(expected)}"
        or len(corrections) + len(expected) != 22
    ):
        failures.append("absence-review-versioned-inventory-reconciliation-mismatch")
    proof_ids = [
        row.get("adjudication_row_id")
        for row in proof_rows
        if isinstance(row, dict)
    ]
    duplicate_proofs = sorted(
        row_id for row_id, count in Counter(proof_ids).items() if count > 1
    )
    for row_id in duplicate_proofs:
        failures.append(f"absence-review-duplicate-proof-id:{row_id}")
    proof_index = {
        row.get("adjudication_row_id"): row
        for row in proof_rows
        if isinstance(row, dict)
    }
    for row_id, expected_row in expected.items():
        actual = proof_index.get(row_id)
        if actual is None:
            failures.append(f"absence-review-proof-row-missing:{row_id}")
            continue
        actual_binding = {key: actual.get(key) for key in expected_row}
        if actual_binding != expected_row:
            failures.append(f"absence-review-proof-row-binding-mismatch:{row_id}")
        assessment = actual.get("implementer_assessment")
        if not isinstance(assessment, dict) or assessment.get("status") not in {
            "READY_FOR_REVIEW",
            "IMPLEMENTER_CONCERN",
        }:
            failures.append(f"absence-review-implementer-assessment-invalid:{row_id}")
        elif assessment["status"] == "IMPLEMENTER_CONCERN" and not assessment.get(
            "concern"
        ):
            failures.append(f"absence-review-implementer-concern-missing:{row_id}")
    for row_id in sorted(set(proof_index) - set(expected)):
        failures.append(f"absence-review-extra-proof-row:{row_id}")

    review_ids = [
        row.get("adjudication_row_id")
        for row in review_rows
        if isinstance(row, dict)
    ]
    for row_id, count in Counter(review_ids).items():
        if count > 1:
            failures.append(f"absence-review-duplicate-review-id:{row_id}")
    if len(review_rows) != len(expected) or set(review_ids) != set(expected):
        failures.append(
            f"absence-review-coverage-mismatch:expected={len(expected)}:"
            f"found={len(review_rows)}"
        )
    for row_id in sorted(set(review_ids) - set(expected)):
        failures.append(f"absence-review-extra-review-row:{row_id}")
    expected_status = (
        "INDEPENDENT_REVIEW_RECORDED_UNVALIDATED"
        if review_rows
        else "PENDING_INDEPENDENT_REVIEW"
    )
    if artifact.get("status") != expected_status:
        failures.append(
            f"absence-review-status-mismatch:{artifact.get('status')}:{expected_status}"
        )
    return failures


def validate_absence_review(bundle):
    failures = validate_review_inventory(bundle)
    adjudication = bundle["absence_adjudication"]
    for filename, sidecar in bundle["sidecars"]:
        sidecar_path = f"{SIDECAR_DIRECTORY_RELATIVE_PATH}/{filename}"
        for row in sidecar.get("method_paths", []):
            failures.extend(
                validate_absence_cross_bindings(
                    row, sidecar_path, sidecar, adjudication
                )
            )
    return failures


def validate_semantic_correction_review(bundle):
    """Validate confirmed corrections and reviewer-mandated recodes."""
    artifact = bundle.get("semantic_corrections")
    if not isinstance(artifact, dict):
        return ["semantic-correction-artifact-invalid"]
    corrections = artifact.get("corrections")
    review_rows = artifact.get("review_rows")
    failures = []
    if not isinstance(corrections, list):
        corrections = []
        failures.append("semantic-correction-inventory-invalid")
    if not isinstance(review_rows, list):
        review_rows = []
        failures.append("semantic-correction-review-rows-invalid")
    active_count = len(bundle.get("absence_adjudication", {}).get("proof_rows", []))
    reconciliation = artifact.get("inventory_reconciliation", {})
    if reconciliation != {
        "original_negative_claims": 22,
        "retired_by_correction": len(corrections),
        "active_negative_claims": active_count,
        "identity": f"22 = {len(corrections)} + {active_count}",
    } or len(corrections) + active_count != 22:
        failures.append("semantic-correction-reconciliation-mismatch")
    correction_ids = [
        row.get("retired_adjudication_row_id")
        for row in corrections
        if isinstance(row, dict)
    ]
    if len(corrections) != 4 or len(set(correction_ids)) != 4 or None in correction_ids:
        failures.append("semantic-correction-inventory-mismatch")
    review_ids = [
        row.get("retired_adjudication_row_id")
        for row in review_rows
        if isinstance(row, dict)
    ]
    if len(review_ids) != len(set(review_ids)):
        failures.append("semantic-correction-duplicate-review-id")
    if len(review_rows) != len(corrections) or set(review_ids) != set(correction_ids):
        failures.append(
            "semantic-correction-review-coverage-mismatch:"
            f"expected={len(corrections)}:found={len(review_rows)}"
        )
    correction_index = {
        row.get("retired_adjudication_row_id"): row
        for row in corrections
        if isinstance(row, dict)
    }
    for row in review_rows:
        if not isinstance(row, dict):
            failures.append("semantic-correction-review-row-invalid")
            continue
        row_id = row.get("retired_adjudication_row_id")
        verdict = row.get("verdict")
        correction = correction_index.get(row_id, {})
        if verdict == "DISAGREE_RECODE_REQUIRED":
            if (
                row.get("required_recode") != correction.get("corrected_value")
                or correction.get("originating_review_verdict") != verdict
            ):
                failures.append(f"semantic-correction-required-recode-mismatch:{row_id}")
        elif verdict != "AGREE":
            failures.append(f"semantic-correction-review-not-agree:{row_id}")
        if not row.get("reviewer_identity") or not row.get("review_reason"):
            failures.append(f"semantic-correction-review-attribution-missing:{row_id}")
        independence = row.get("independence")
        if not isinstance(independence, dict) or not all(
            independence.get(field)
            for field in ("nonparticipation_scope", "conflict_declaration")
        ) or not (independence.get("timestamp_utc") or independence.get("review_date")):
            failures.append(f"semantic-correction-review-independence-missing:{row_id}")
    expected_status = (
        "INDEPENDENT_REVIEW_RECORDED_UNVALIDATED"
        if review_rows
        else "PENDING_INDEPENDENT_REVIEW"
    )
    if artifact.get("review_status") != expected_status:
        failures.append("semantic-correction-review-status-mismatch")
    if artifact.get("reviewer_rows_created") != len(review_rows):
        failures.append("semantic-correction-review-count-mismatch")
    return failures


def _platform_stamp(platform_os=None):
    stamp = pdf_runtime_stamp()
    role = platform_os or stamp["os"]
    if role != stamp["os"]:
        return {
            "os": role,
            "sys_platform": "win32" if role == "nt" else "linux",
            "python_version": stamp["python_version"],
            "pypdf_version": stamp["pypdf_version"],
            "extractor_identity": stamp["extractor_identity"],
        }
    return stamp


def validate_h5_calibration(bundle):
    return validate_h5_completion(bundle.get("h5_calibration", {}))


def validate_pdf_extractor(bundle, platform_os=None):
    document = bundle.get("pdf_extractor_contract", {})
    stamp = _platform_stamp(platform_os)
    failures = validate_pdf_contract(document)
    failures.extend(validate_pdf_runtime(document, stamp))
    replay = replay_toolgate_probe(document) if not failures else {
        "result": "FAIL",
        "anchor_found": False,
        "runtime": stamp,
        "failure": "environment contract failed before replay",
    }
    return sorted(set(failures)), replay


def _exact_occupancy(occupancy_block):
    policy = occupancy_block["policy_A"]
    mechanism = policy[
        "strict_AND_reward_AND_pool_BY_selection_object(mechanism)"
    ]
    return (
        policy["n_method_paths"] == 11
        and policy["is_reward_guided"]["n_paths"] == "6/11"
        and policy["is_rq_sys_control_compatible"]["n_paths"] == "5/11"
        and policy["is_project_method_candidate"]["n_paths"] == "0/11"
        and policy["reward_guided_selection"]["n_paths"] == "4/11"
        and mechanism["trajectory"]["n_paths"] == "2/11"
    )


def build_report(bundle=None, platform_os=None):
    bundle = bundle or load_current_inputs()
    rows = bundle["rows"]
    sidecars = bundle["sidecars"]
    coding_text = bundle["coding_text"]
    structure_failures = validate(rows)
    binding_failures = [
        failure for row in rows for failure in validate_bound_values(row)
    ]
    source_failures = reconcile_v6(
        sidecars, coding_text, evidence_cache=EvidenceCache()
    )
    absence_failures = validate_absence_review(bundle)
    semantic_correction_failures = validate_semantic_correction_review(bundle)
    h5_failures = validate_h5_calibration(bundle)
    pdf_extractor_failures, toolgate_probe = validate_pdf_extractor(
        bundle, platform_os=platform_os
    )
    mutation_results = run_absence_mutation_suite(rows)
    mutation_ok = (
        not mutation_results["legitimate_field_specific_negative_control"]
        and any(
            "absence-field-value-not-allowed" in failure
            for failure in mutation_results["positive_categorical_absence"]
        )
    )
    policy = ("single_core", "single_core_multi_call")
    occupancy_block = {
        "policy_A": occupancy(policy, rows),
        "sensitivity_strict_topology": occupancy(("single_core",), rows),
    }
    checks = [
        {
            "id": "LOAD_BEARING_CONTRACT",
            "check": "structure, local bindings, and frozen-source resolution",
            "result": "PASS"
            if not structure_failures and not binding_failures and not source_failures
            else "FAIL",
            "detail": {
                "structure": structure_failures[:8],
                "bindings": binding_failures[:8],
                "source": source_failures[:8],
            },
        },
        {
            "id": "ABSENCE_REVIEW",
            "check": "all absence rows cross-bind to independent AGREE review rows",
            "result": "PASS" if not absence_failures else "FAIL",
            "detail": absence_failures[:24],
        },
        {
            "id": "SEMANTIC_CORRECTION_REVIEW",
            "check": "all retired negative claims cross-bind to independent AGREE correction reviews",
            "result": "PASS" if not semantic_correction_failures else "FAIL",
            "detail": semantic_correction_failures[:24],
        },
        {
            "id": "H5_CALIBRATION",
            "check": "three frozen papers have two independent seven-field codings and complete disagreement adjudication",
            "result": "PASS" if not h5_failures else "FAIL",
            "detail": h5_failures[:24],
        },
        {
            "id": "PDF_EXTRACTOR_ENVIRONMENT",
            "check": "runtime exactly matches the frozen platform-specific Python and pypdf identity",
            "result": "PASS" if not pdf_extractor_failures else "FAIL",
            "detail": pdf_extractor_failures,
        },
        {
            "id": "TOOLGATE_P11_REPLAY",
            "check": "the frozen ToolGate PDF page-11 discriminative anchor resolves under this exact extractor",
            "result": "PASS" if toolgate_probe.get("result") == "PASS" else "FAIL",
            "detail": toolgate_probe,
        },
        {
            "id": "ABSENCE_MUTATIONS",
            "check": "positive categorical absence is red and allowed negative is clean",
            "result": "PASS" if mutation_ok else "FAIL",
            "detail": mutation_results,
        },
        {
            "id": "OCCUPANCY",
            "check": "occupancy remains the exact frozen 11-path semantic baseline",
            "result": "PASS" if _exact_occupancy(occupancy_block) else "FAIL",
            "detail": {
                "n_method_paths": occupancy_block["policy_A"]["n_method_paths"]
            },
        },
    ]
    failure_codes = [check["id"] for check in checks if check["result"] != "PASS"]
    n_pass = len(checks) - len(failure_codes)
    runner_raw = _repo_path(RUNNER_RELATIVE_PATH).read_bytes()
    return {
        "artifact_id": ARTIFACT_ID,
        "contract_version": CONTRACT_VERSION,
        "implementation_freeze": IMPLEMENTATION_FREEZE,
        "runner": {
            "path": RUNNER_RELATIVE_PATH,
            "sha256": hashlib.sha256(runner_raw).hexdigest(),
        },
        "input_provenance": bundle["input_provenance"],
        "input_snapshot_sha256": bundle["input_snapshot_sha256"],
        "platform": _platform_stamp(platform_os),
        "toolgate_p11_replay": toolgate_probe,
        "checks": checks,
        "occupancy": occupancy_block,
        "mutation_results": mutation_results,
        "failure_codes": failure_codes,
        "summary": f"{n_pass}/{len(checks)} PASS",
        "verdict": "PASS" if not failure_codes else "FAIL",
    }


def encode_report(report):
    return (
        json.dumps(report, ensure_ascii=False, indent=1, allow_nan=False) + "\n"
    ).encode("utf-8")


def write_report(report, output):
    output = Path(output)
    payload = encode_report(report)
    output.parent.mkdir(parents=True, exist_ok=True)
    descriptor, staging_name = tempfile.mkstemp(
        prefix=f".{output.name}.", suffix=".tmp", dir=output.parent
    )
    staging = Path(staging_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        if staging.read_bytes() != payload:
            raise OSError("staged leaf bytes differ from deterministic payload")
        os.replace(staging, output)
        staging = None
    finally:
        if staging is not None:
            try:
                staging.unlink()
            except FileNotFoundError:
                pass


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--leaf", action="store_true", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    try:
        report = build_report()
    except Exception as error:
        runner_raw = _repo_path(RUNNER_RELATIVE_PATH).read_bytes()
        report = {
            "artifact_id": ARTIFACT_ID,
            "contract_version": CONTRACT_VERSION,
            "implementation_freeze": IMPLEMENTATION_FREEZE,
            "runner": {
                "path": RUNNER_RELATIVE_PATH,
                "sha256": hashlib.sha256(runner_raw).hexdigest(),
            },
            "input_provenance": {},
            "input_snapshot_sha256": "",
            "platform": _platform_stamp(),
            "checks": [
                {
                    "id": "INPUT_CONTRACT",
                    "check": "strict current input load",
                    "result": "FAIL",
                    "detail": f"{type(error).__name__}: {error}",
                }
            ],
            "occupancy": {},
            "mutation_results": {},
            "failure_codes": ["INPUT_CONTRACT"],
            "summary": "0/1 PASS",
            "verdict": "FAIL",
        }
    write_report(report, args.output)
    print(
        json.dumps(
            {
                "output": args.output,
                "platform": report["platform"],
                "summary": report["summary"],
                "verdict": report["verdict"],
                "failure_codes": report["failure_codes"],
            },
            ensure_ascii=False,
            indent=1,
        )
    )
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
