#!/usr/bin/env python3
"""Fail-closed pre-adjudication agreement for Agentic RC2R1.

The engine accepts only two complete, provenance-bound N=56 response sets.  It
computes paper gates, object segmentation gates and one independent gate for
every declared critical object field.  It never adjudicates disagreements.
"""

from __future__ import annotations

import json
import re
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import sf_stage1c_v2_precalibration_rc2r1 as rc2r1
else:
    from scripts.survey import sf_stage1c_v2_precalibration_rc2r1 as rc2r1


OBJECT_ARRAYS = (
    *rc2r1.BASE_CALIBRATED_OBJECT_ARRAYS,
    "protocol_transfer_evidence",
    "reproduction_evidence",
)

SINGLE_LABEL_FIELDS = (
    "paper_disposition", "paper_role", "mm_level", "reference_borrow_reproduce",
    "access_regime", "empirical_experiment_present", "agentic_scope.scope_status",
    "agentic_scope.core_dependency", "agentic_scope.control_role",
)

MULTILABEL_FIELDS = (
    "problem_nodes", "intervention_axes", "agentic_scope.loop_components",
    "agentic_scope.capability_assets",
)

CRITICAL_OBJECT_FIELDS: dict[str, tuple[str, ...]] = {
    "run_cells": (
        "dataset_node_ids", "model", "access_regime", "input_condition", "intervention",
        "control_signal", "primary_intervention_axis", "decision_or_action", "budget_horizon",
        "baseline_role", "source_locator_ids",
    ),
    "observations": (
        "run_cell_id", "metric_or_evaluator", "outcome_semantics", "raw_result",
        "observation_role", "source_locator_ids",
    ),
    "paired_comparisons": (
        "baseline_cell_id", "intervention_cell_id", "paired_status",
        "comparability_key.dataset_revision_split", "comparability_key.core_model",
        "comparability_key.access", "comparability_key.input_condition",
        "comparability_key.metric", "comparability_key.budget_horizon", "source_locator_ids",
    ),
    "dataset_nodes": ("name", "revision", "split", "source_locator_ids"),
    "dataset_edges": (
        "edge_type", "source_dataset_id", "relation", "target_dataset_id", "reason",
        "source_locator_ids",
    ),
    "claim_decisions": (
        "claim_template_id", "merge_split_decision", "scope.problem_outcome", "scope.task",
        "scope.dataset_revision_split", "scope.model", "scope.access", "scope.input_condition",
        "scope.intervention", "scope.budget_horizon", "scope.evaluator", "evidence_relation",
        "source_locator_ids",
    ),
    "translation_or_compatibility_decisions": (
        "decision_type", "target_object_id", "compatibility_decision", "reason",
        "source_locator_ids",
    ),
    "protocol_transfer_evidence": (
        "source_domain", "source_protocol", "target_speech_omni_variables",
        "preserved_decision_structure", "source_locator_ids", "rejection_condition",
        "rejection_observable", "evidence_status",
    ),
    "reproduction_evidence": (
        "task", "dataset", "dataset_revision", "split", "official_repo", "pinned_revision",
        "entrypoint", "model_access", "license_terms", "evaluator_or_ground_truth",
        "local_asset_state", "source_locator_ids", "closure_status", "blockers",
    ),
}


class AgreementError(ValueError):
    """Raised when an agreement intake is incomplete or provenance-ambiguous."""


def _index_responses(rows: Iterable[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    response_ids: set[str] = set()
    for row in rows:
        paper_id = row.get("paper_id")
        if not isinstance(paper_id, str) or not paper_id:
            raise AgreementError("every response requires a non-empty paper_id")
        if paper_id in indexed:
            raise AgreementError(f"duplicate paper response: {paper_id}")
        response_id = row.get("response_id")
        if not isinstance(response_id, str) or not response_id or response_id in response_ids:
            raise AgreementError("every completed response requires a unique response_id")
        response_ids.add(response_id)
        indexed[paper_id] = row
    return indexed


def _validate_hex(value: Any, field: str) -> str:
    if not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{64}", value) is None:
        raise AgreementError(f"{field} must be lowercase SHA-256")
    return value


def _validate_intake(contract: dict[str, Any]) -> tuple[list[str], list[dict[str, Any]]]:
    if contract.get("schema") != "sf-stage1c-v2-agreement-intake-contract-v3":
        raise AgreementError("unknown agreement intake contract schema")
    if contract.get("status") != "BOUND_FOR_PRE_ADJUDICATION_AGREEMENT":
        raise AgreementError("agreement intake is not bound for pre-adjudication comparison")
    if contract.get("N") != 56:
        raise AgreementError("agreement intake requires exact N=56")
    paper_ids = contract.get("canonical_paper_ids")
    if not isinstance(paper_ids, list) or len(paper_ids) != 56 or len(set(paper_ids)) != 56:
        raise AgreementError("agreement intake requires exact N=56 unique canonical IDs")
    items = contract.get("items")
    if not isinstance(items, list) or len(items) != 56:
        raise AgreementError("agreement intake requires exact N=56 packet bindings")
    if {row.get("paper_id") for row in items} != set(paper_ids):
        raise AgreementError("agreement intake packet bindings differ from canonical paper set")
    _validate_hex(contract.get("content_bundle_sha256"), "content_bundle_sha256")
    _validate_hex(contract.get("prompt_hash"), "prompt_hash")
    slots = contract.get("coder_slots")
    if not isinstance(slots, list) or len(slots) != 2:
        raise AgreementError("agreement intake requires exactly two coder slots")
    distinct_fields = ("coder_id", "coder_transaction_id", "process_id")
    for field in distinct_fields:
        values = [slot.get(field) for slot in slots]
        if any(not isinstance(value, str) or not value for value in values) or len(set(values)) != 2:
            raise AgreementError(f"coder slots require distinct non-empty {field}")
    for slot in slots:
        if slot.get("assignment_status") != "FROZEN_SUBMITTED":
            raise AgreementError("both coder slots must be frozen before agreement")
        if slot.get("model") != slot.get("planned_model"):
            raise AgreementError("bound coder model differs from planned isolated model")
        if slot.get("expected_content_bundle_sha256") != contract["content_bundle_sha256"]:
            raise AgreementError("coder slot content bundle binding differs")
        if slot.get("expected_prompt_hash") != contract["prompt_hash"]:
            raise AgreementError("coder slot prompt hash binding differs")
        for receipt in ("distribution_receipt_id", "submission_receipt_id"):
            if not isinstance(slot.get(receipt), str) or not slot[receipt]:
                raise AgreementError(f"coder slot lacks {receipt}")
    return paper_ids, slots


def _validate_response_set(
    rows: list[dict[str, Any]], *, slot: dict[str, Any], expected_ids: set[str],
    packet_by_paper: dict[str, str], contract: dict[str, Any], response_schema: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    indexed = _index_responses(rows)
    if len(indexed) != 56:
        raise AgreementError("each coder response set requires exact N=56")
    if set(indexed) != expected_ids:
        raise AgreementError("coder response canonical paper set differs from agreement intake")
    for paper_id, response in indexed.items():
        if response.get("coder_id") != slot["coder_id"]:
            raise AgreementError("response coder_id differs from bound slot")
        if response.get("coder_transaction_id") != slot["coder_transaction_id"]:
            raise AgreementError("response coder transaction differs from bound slot")
        if response.get("source_manifest_id") != contract["source_manifest_id"]:
            raise AgreementError("response source manifest binding differs")
        if response.get("packet_item_id") != packet_by_paper[paper_id]:
            raise AgreementError("response packet item binding differs")
        try:
            rc2r1.validate_completed_response(response, response_schema)
        except (rc2r1.ContractError, ValueError) as error:
            raise AgreementError(f"invalid completed response for {paper_id}: {error}") from error
    return indexed


def _ratio(numerator: int, denominator: int) -> float | None:
    return numerator / denominator if denominator else None


def _gate(value: float | None, minimum: float) -> str:
    if value is None:
        return "NOT_CALIBRATED"
    return "PASS" if value >= minimum else "FAIL"


def _get_path(value: dict[str, Any], path: str) -> Any:
    current: Any = value
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            raise AgreementError(f"missing critical agreement path: {path}")
        current = current[part]
    return current


def _canonical_value(value: Any) -> str:
    if isinstance(value, list):
        value = sorted(value, key=lambda item: json.dumps(item, ensure_ascii=False, sort_keys=True))
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _paper_field_gate(
    pairs: list[tuple[dict[str, Any], dict[str, Any]]], field: str, *,
    minimum: float, multilabel: bool,
) -> dict[str, Any]:
    matches = denominator = 0
    jaccard_total = 0.0
    for left, right in pairs:
        left_value = _get_path(left["paper_labels"], field)
        right_value = _get_path(right["paper_labels"], field)
        left_na = left_value == "NOT_APPLICABLE" or left_value == ["NOT_APPLICABLE"]
        right_na = right_value == "NOT_APPLICABLE" or right_value == ["NOT_APPLICABLE"]
        if left_na and right_na:
            continue
        denominator += 1
        if multilabel:
            left_set, right_set = set(left_value), set(right_value)
            matches += left_set == right_set
            union = left_set | right_set
            jaccard_total += len(left_set & right_set) / len(union) if union else 1.0
        else:
            matches += left_value == right_value
    exact = _ratio(matches, denominator)
    result = {
        "numerator": matches, "denominator": denominator, "exact_agreement": exact,
        "gate_status": _gate(exact, minimum),
    }
    if multilabel:
        result["mean_jaccard_diagnostic"] = _ratio(round(jaccard_total * 1_000_000), denominator * 1_000_000)
    return result


def _object_index(row: dict[str, Any], array_name: str) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for obj in row.get(array_name, []):
        key = obj.get("object_match_key")
        if not isinstance(key, str) or not key:
            raise AgreementError(f"{array_name} object requires object_match_key")
        if key in indexed:
            raise AgreementError(f"duplicate {array_name} object_match_key: {key}")
        indexed[key] = obj
    return indexed


def compute_agreement(
    coder_a: list[dict[str, Any]], coder_b: list[dict[str, Any]], *,
    intake_contract: dict[str, Any], response_schema: dict[str, Any], minimum: float = 0.85,
) -> dict[str, Any]:
    """Compute pre-adjudication agreement after exact intake validation."""
    if not 0 < minimum <= 1:
        raise AgreementError("minimum must be in (0, 1]")
    paper_ids, slots = _validate_intake(intake_contract)
    if response_schema.get("$id") != intake_contract.get("response_schema_id"):
        raise AgreementError("response schema differs from agreement intake binding")
    packet_by_paper = {row["paper_id"]: row["packet_item_id"] for row in intake_contract["items"]}
    expected_ids = set(paper_ids)
    left = _validate_response_set(
        coder_a, slot=slots[0], expected_ids=expected_ids, packet_by_paper=packet_by_paper,
        contract=intake_contract, response_schema=response_schema,
    )
    right = _validate_response_set(
        coder_b, slot=slots[1], expected_ids=expected_ids, packet_by_paper=packet_by_paper,
        contract=intake_contract, response_schema=response_schema,
    )
    pairs = [(left[paper_id], right[paper_id]) for paper_id in sorted(paper_ids)]

    paper_level: dict[str, Any] = {}
    for field in SINGLE_LABEL_FIELDS:
        paper_level[field] = _paper_field_gate(pairs, field, minimum=minimum, multilabel=False)
    for field in MULTILABEL_FIELDS:
        paper_level[field] = _paper_field_gate(pairs, field, minimum=minimum, multilabel=True)

    object_level: dict[str, Any] = {}
    all_gate_statuses = [gate["gate_status"] for gate in paper_level.values()]
    for array_name in OBJECT_ARRAYS:
        matches = left_total = right_total = 0
        field_counts = {
            field: {"numerator": 0, "denominator": 0}
            for field in CRITICAL_OBJECT_FIELDS[array_name]
        }
        for paper_id in sorted(paper_ids):
            left_objects = _object_index(left[paper_id], array_name)
            right_objects = _object_index(right[paper_id], array_name)
            left_total += len(left_objects)
            right_total += len(right_objects)
            common = sorted(set(left_objects) & set(right_objects))
            matches += len(common)
            for key in common:
                for field, counts in field_counts.items():
                    left_value = _get_path(left_objects[key], field)
                    right_value = _get_path(right_objects[key], field)
                    counts["denominator"] += 1
                    counts["numerator"] += _canonical_value(left_value) == _canonical_value(right_value)
        precision = _ratio(matches, right_total)
        recall = _ratio(matches, left_total)
        if precision is None and recall is None:
            f1 = None
        elif not precision or not recall:
            f1 = 0.0
        else:
            f1 = 2 * precision * recall / (precision + recall)
        segmentation_status = _gate(f1, minimum)
        critical_gates: dict[str, Any] = {}
        for field, counts in field_counts.items():
            exact = _ratio(counts["numerator"], counts["denominator"])
            critical_gates[field] = {
                **counts, "exact_agreement": exact, "gate_status": _gate(exact, minimum),
            }
        statuses = [segmentation_status, *(gate["gate_status"] for gate in critical_gates.values())]
        combined = "PASS" if statuses and all(status == "PASS" for status in statuses) else "FAIL"
        if all(status == "NOT_CALIBRATED" for status in statuses):
            combined = "NOT_CALIBRATED"
        object_level[array_name] = {
            "coder_a_objects": left_total, "coder_b_objects": right_total,
            "matched_objects": matches, "segmentation_precision": precision,
            "segmentation_recall": recall, "segmentation_f1": f1,
            "segmentation_gate_status": segmentation_status,
            "critical_field_gates": critical_gates, "gate_status": combined,
        }
        all_gate_statuses.extend(statuses)

    return {
        "schema": "sf-stage1c-v2-calibration-agreement-result-v3",
        "agreement_intake_contract_id": intake_contract["artifact_id"],
        "paper_count": len(paper_ids), "minimum": minimum,
        "paper_level": paper_level, "object_level": object_level,
        "critical_path_gate_count": len(all_gate_statuses),
        "overall_gate_status": (
            "PASS" if all_gate_statuses and all(status == "PASS" for status in all_gate_statuses)
            else "FAIL"
        ),
        "adjudication_applied": False,
    }


if __name__ == "__main__":
    raise SystemExit("Import compute_agreement with two frozen coder response sets.")
