"""Frozen semantic contract for dual-platform evidence-v6 reports."""
from __future__ import annotations

import hashlib

from sf_json_contract import JsonContractError, canonical_bytes
from sf_schema_v3_release_contract import FINAL_SIDECAR_NAMES
from sf_v6_snapshot_contract import (
    ADJUDICATION_RELATIVE_PATH,
    CODING_V7_RELATIVE_PATH,
    TAXONOMY_V6_RELATIVE_PATH,
)


ARTIFACT_ID = "SF-IDENTITY-TAXONOMY-V6-TEST-2026-07-19-01"
SUMMARY = "14/14 PASS"
TOPOLOGY_POLICY = "A(frozen) + strict-topology sensitivity dual-computed"
TOP_LEVEL_KEYS = frozenset(
    {
        "artifact_id",
        "inputs",
        "input_provenance",
        "input_snapshot_sha256",
        "platform",
        "topology_policy",
        "checks",
        "occupancy",
        "mutation_results",
        "summary",
        "verdict",
    }
)
CHECK_IDS = (
    "V0",
    "V1",
    "V2",
    "V3",
    "V3a",
    "V3b",
    "V4",
    "V5",
    "V5b",
    "V6",
    "V7",
    "V8",
    "V9",
    "V10",
)
MUTATION_NAMES = frozenset(
    {
        "E1_edge_use_flip",
        "E2_signal_evidence_p9999",
        "E3_bare_in_range_page",
        "E3b_generic_anchor_the",
        "E3c_frequent_phrase",
        "E4_signal_form_flip",
        "E5_coding_hand_edit",
        "E6_signal_source_flip",
        "E7_edge_use_coherent_flip",
        "E8_edge_right_coherent_flip",
        "E9_selection_object_flip",
        "E10_explicit_selection_flip",
        "E11_missing_signal_source_binding",
        "E12_missing_edge_right_binding",
        "wrong_horizon",
        "double_flip_horizon_plus_evidence",
        "fake_page_p9999",
        "edge_signal_lifecycle_mismatch",
        "edge_signal_identity_mismatch",
        "wrong_decision_right",
        "wrong_selection_policy",
        "wrong_work",
        "wrong_modality",
        "wrong_sha",
        "wrong_kind",
        "nonsense_locator",
    }
)
EXPECTED_INPUTS = {
    "taxonomy": TAXONOMY_V6_RELATIVE_PATH,
    "coding": CODING_V7_RELATIVE_PATH,
    "adjudication": ADJUDICATION_RELATIVE_PATH,
    "sidecars": list(FINAL_SIDECAR_NAMES),
}
BLOCK_SHA256 = {
    "checks": "8ebe93f9cc8a8dbea88c7134a48c31aee82ef3b11f163fa0166e376e9848e6aa",
    "occupancy": "81eaf5424059e7f40dde794e0f8063650604afffcdaa02d699b62eeafff72292",
    "mutation_results": (
        "11c1e21842c86fc959870d546805047cce69cd3dd34854c97399d43a7b98b15d"
    ),
}


def _block_hash(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _occupancy_failures(occupancy):
    if not isinstance(occupancy, dict):
        return ["occupancy must be an object"]
    try:
        policy = occupancy["policy_A"]
        mechanism = policy[
            "strict_AND_reward_AND_pool_BY_selection_object(mechanism)"
        ]
        actual = (
            policy["n_method_paths"],
            policy["is_reward_guided"]["n_paths"],
            policy["is_rq_sys_control_compatible"]["n_paths"],
            policy["is_project_method_candidate"]["n_paths"],
            policy["reward_guided_selection"]["n_paths"],
            mechanism["trajectory"]["n_paths"],
        )
    except (KeyError, TypeError):
        return ["occupancy is missing frozen policy-A keys"]
    expected = (11, "6/11", "5/11", "0/11", "4/11", "2/11")
    return [] if actual == expected else [f"frozen occupancy mismatch: {actual!r}"]


def validate_v6_report_semantics(report):
    """Return stable failures for drift from the frozen 14-check report."""
    if not isinstance(report, dict):
        return ["report root must be an object"]
    failures = []
    if set(report) != TOP_LEVEL_KEYS:
        failures.append("top-level report keys differ from frozen v6 contract")
    if report.get("artifact_id") != ARTIFACT_ID:
        failures.append("artifact_id differs from frozen v6 contract")
    if report.get("inputs") != EXPECTED_INPUTS:
        failures.append("inputs differ from frozen v6 contract")
    if report.get("topology_policy") != TOPOLOGY_POLICY:
        failures.append("topology policy differs from frozen v6 contract")
    if report.get("summary") != SUMMARY:
        failures.append("summary differs from frozen 14/14 PASS")
    if report.get("verdict") != "PASS":
        failures.append(f"verdict is not PASS: {report.get('verdict')!r}")
    platform = report.get("platform")
    if not isinstance(platform, dict) or set(platform) != {"os", "python"}:
        failures.append("platform must contain exact os/python keys")

    checks = report.get("checks")
    if not isinstance(checks, list):
        failures.append("checks must be a list")
    else:
        check_ids = tuple(
            check.get("id") if isinstance(check, dict) else None
            for check in checks
        )
        if check_ids != CHECK_IDS:
            failures.append("check IDs differ from frozen 14-check inventory")
        if any(
            not isinstance(check, dict) or check.get("result") != "PASS"
            for check in checks
        ):
            failures.append("one or more internal checks are not PASS")

    mutations = report.get("mutation_results")
    if not isinstance(mutations, dict):
        failures.append("mutation_results must be an object")
    else:
        if set(mutations) != MUTATION_NAMES:
            failures.append("mutation names differ from frozen inventory")
        if any(
            not isinstance(caught, list) or not caught
            for caught in mutations.values()
        ):
            failures.append("one or more frozen mutations were not caught")

    failures.extend(_occupancy_failures(report.get("occupancy")))
    for key, expected_sha256 in BLOCK_SHA256.items():
        try:
            actual_sha256 = _block_hash(report.get(key))
        except JsonContractError as error:
            failures.append(f"{key} is not canonical JSON: {error}")
            continue
        if actual_sha256 != expected_sha256:
            failures.append(f"{key} differs from frozen block hash")
    return failures
