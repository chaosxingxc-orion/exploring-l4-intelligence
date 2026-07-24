#!/usr/bin/env python3
"""Deterministic paper/object agreement for Stage-1C v2 calibration.

This module only compares completed coder responses.  It never calls a model,
computes a benchmark metric, adjudicates a disagreement, or changes authority.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any


OBJECT_ARRAYS = (
    "run_cells",
    "observations",
    "paired_comparisons",
    "dataset_nodes",
    "dataset_edges",
    "claim_decisions",
    "translation_or_compatibility_decisions",
)

SINGLE_LABEL_FIELDS = (
    "paper_disposition",
    "paper_role",
    "mm_level",
    "reference_borrow_reproduce",
    "access_regime",
    "empirical_experiment_present",
    "agentic_scope.scope_status",
    "agentic_scope.core_dependency",
    "agentic_scope.control_role",
)

MULTILABEL_FIELDS = (
    "problem_nodes", "intervention_axes", "agentic_scope.loop_components",
    "agentic_scope.capability_assets",
)


class AgreementError(ValueError):
    """Raised when coder response sets cannot be compared deterministically."""


def _index_responses(rows: Iterable[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for row in rows:
        paper_id = row.get("paper_id")
        if not isinstance(paper_id, str) or not paper_id:
            raise AgreementError("every response requires a non-empty paper_id")
        if paper_id in indexed:
            raise AgreementError(f"duplicate paper response: {paper_id}")
        indexed[paper_id] = row
    return indexed


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


def _ratio(numerator: int, denominator: int) -> float | None:
    return numerator / denominator if denominator else None


def _gate(value: float | None, minimum: float) -> str:
    if value is None:
        return "NOT_CALIBRATED"
    return "PASS" if value >= minimum else "FAIL"


def _field_agreement(
    pairs: Iterable[tuple[dict[str, Any], dict[str, Any]]],
    field: str,
    *,
    multilabel: bool = False,
) -> dict[str, Any]:
    agreements = 0
    denominator = 0
    jaccard_total = 0.0
    for left, right in pairs:
        left_value: Any = left["paper_labels"]
        right_value: Any = right["paper_labels"]
        for part in field.split("."):
            try:
                left_value = left_value[part]
                right_value = right_value[part]
            except (KeyError, TypeError) as error:
                raise AgreementError(f"missing paper-level agreement field: {field}") from error
        left_na = left_value == "NOT_APPLICABLE" or left_value == ["NOT_APPLICABLE"]
        right_na = right_value == "NOT_APPLICABLE" or right_value == ["NOT_APPLICABLE"]
        if left_na and right_na:
            continue
        denominator += 1
        if multilabel:
            left_set, right_set = set(left_value), set(right_value)
            agreements += left_set == right_set
            union = left_set | right_set
            jaccard_total += len(left_set & right_set) / len(union) if union else 1.0
        else:
            agreements += left_value == right_value
    result = {"exact_agreement": _ratio(agreements, denominator), "denominator": denominator}
    if multilabel:
        result["mean_jaccard_diagnostic"] = jaccard_total / denominator if denominator else None
    return result


def _comparable_object_fields(left: dict[str, Any], right: dict[str, Any]) -> list[str]:
    excluded = {
        "object_match_key", "run_cell_id", "observation_id", "comparison_id",
        "dataset_node_id", "dataset_edge_id", "claim_decision_id", "decision_id",
        "source_locator_ids",
    }
    return sorted((set(left) & set(right)) - excluded)


def compute_agreement(
    coder_a: list[dict[str, Any]],
    coder_b: list[dict[str, Any]],
    *,
    minimum: float = 0.85,
) -> dict[str, Any]:
    """Compute pre-adjudication agreement with exact, source-anchored object matching."""
    if not 0 < minimum <= 1:
        raise AgreementError("minimum must be in (0, 1]")
    left = _index_responses(coder_a)
    right = _index_responses(coder_b)
    if set(left) != set(right):
        raise AgreementError("coder response paper sets differ")
    paper_ids = sorted(left)
    pairs = [(left[paper_id], right[paper_id]) for paper_id in paper_ids]

    paper_level: dict[str, Any] = {}
    for field in SINGLE_LABEL_FIELDS:
        metric = _field_agreement(pairs, field)
        metric["gate_status"] = _gate(metric["exact_agreement"], minimum)
        paper_level[field] = metric
    for field in MULTILABEL_FIELDS:
        metric = _field_agreement(pairs, field, multilabel=True)
        metric["gate_status"] = _gate(metric["exact_agreement"], minimum)
        paper_level[field] = metric

    object_level: dict[str, Any] = {}
    for array_name in OBJECT_ARRAYS:
        matches = left_total = right_total = 0
        field_equal = field_total = 0
        for paper_id in paper_ids:
            left_objects = _object_index(left[paper_id], array_name)
            right_objects = _object_index(right[paper_id], array_name)
            left_total += len(left_objects)
            right_total += len(right_objects)
            common = sorted(set(left_objects) & set(right_objects))
            matches += len(common)
            for key in common:
                left_obj, right_obj = left_objects[key], right_objects[key]
                for field in _comparable_object_fields(left_obj, right_obj):
                    field_total += 1
                    field_equal += left_obj[field] == right_obj[field]
        precision = _ratio(matches, right_total)
        recall = _ratio(matches, left_total)
        if precision is None and recall is None:
            f1 = None
        elif not precision or not recall:
            f1 = 0.0
        else:
            f1 = 2 * precision * recall / (precision + recall)
        field_raw = _ratio(field_equal, field_total)
        segmentation_gate = _gate(f1, minimum)
        field_gate = _gate(field_raw, minimum)
        if segmentation_gate == "NOT_CALIBRATED":
            gate_status = "NOT_CALIBRATED"
        elif segmentation_gate == "FAIL" or field_gate == "FAIL":
            gate_status = "FAIL"
        else:
            gate_status = "PASS"
        object_level[array_name] = {
            "coder_a_objects": left_total,
            "coder_b_objects": right_total,
            "matched_objects": matches,
            "segmentation_precision": precision,
            "segmentation_recall": recall,
            "segmentation_f1": f1,
            "matched_field_raw_agreement": field_raw,
            "matched_field_denominator": field_total,
            "gate_status": gate_status,
        }

    calibrated_gates = [
        metric["gate_status"]
        for metric in [*paper_level.values(), *object_level.values()]
        if metric["gate_status"] != "NOT_CALIBRATED"
    ]
    return {
        "schema": "sf-stage1c-v2-calibration-agreement-result-v2",
        "paper_count": len(paper_ids),
        "minimum": minimum,
        "paper_level": paper_level,
        "object_level": object_level,
        "overall_gate_status": "PASS" if calibrated_gates and all(g == "PASS" for g in calibrated_gates) else "FAIL",
        "adjudication_applied": False,
    }


def synthetic_response(*, run_cell_keys: list[str] | None = None) -> dict[str, Any]:
    """Small deterministic fixture used to prove object matching and zero-positive behavior."""
    return {
        "paper_id": "arxiv:fixture",
        "paper_labels": {
            "paper_disposition": "EMPIRICAL_EXTRACTABLE",
            "paper_role": "DIRECT_METHOD",
            "problem_nodes": ["BUDGET_STOP_REPAIR"],
            "intervention_axes": ["D4_TF_RL_ORCHESTRATION"],
            "mm_level": "MM2_MULTIMODAL_ASSET",
            "reference_borrow_reproduce": "REFERENCE",
            "access_regime": "TF_STRICT_BLACK_BOX",
            "empirical_experiment_present": True,
            "agentic_scope": {
                "scope_status": "DIRECT_AGENTIC",
                "loop_components": ["OBSERVE", "DECIDE", "ACT_OR_TOOL", "STOP_OR_BUDGET"],
                "core_dependency": "GENERIC_FROZEN_CORE",
                "capability_assets": ["SKILL"],
                "control_role": "TRAINING_FREE_NON_REWARD_AGENTIC",
                "scope_reason": "Synthetic direct-agentic fixture.",
            },
        },
        "run_cells": [
            {"object_match_key": key, "model": "fixture-model"}
            for key in (run_cell_keys or [])
        ],
        "observations": [],
        "paired_comparisons": [],
        "dataset_nodes": [],
        "dataset_edges": [],
        "claim_decisions": [],
        "translation_or_compatibility_decisions": [],
    }


if __name__ == "__main__":
    raise SystemExit("Use the RC2 checker or import compute_agreement; no coder inputs were supplied.")
