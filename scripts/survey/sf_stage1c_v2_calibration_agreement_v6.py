#!/usr/bin/env python3
"""Fail-closed pre-adjudication agreement for Agentic calibration R2."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import sf_stage1c_v2_calibration_agreement_v3 as v3
    import sf_stage1c_v2_calibration_agreement_v5 as v5
    import sf_stage1c_v2_precalibration_r2 as r2
    import sf_stage1c_v2_r2_guards as r2_guards
else:
    from scripts.survey import sf_stage1c_v2_calibration_agreement_v3 as v3
    from scripts.survey import sf_stage1c_v2_calibration_agreement_v5 as v5
    from scripts.survey import sf_stage1c_v2_precalibration_r2 as r2
    from scripts.survey import sf_stage1c_v2_r2_guards as r2_guards


# Patched from the deterministic R2 build before the method-review commit.
FROZEN_CONTRACT_SHA256 = "eaf2e3ca095a2d4fbe303e68c6fa273b73b26cd7a68476eaae9848ef16e1fa47"
AGREEMENT_MINIMUM = 0.85

OBJECT_ARRAYS = r2.OBJECT_ARRAYS
SINGLE_LABEL_FIELDS = v3.SINGLE_LABEL_FIELDS
MULTILABEL_FIELDS = v3.MULTILABEL_FIELDS
CRITICAL_OBJECT_FIELDS: dict[str, tuple[str, ...]] = {
    **{key: value for key, value in v3.CRITICAL_OBJECT_FIELDS.items() if key != "reproduction_evidence"},
    "paper_reproduction_support": (
        "task", "dataset", "dataset_revision", "split", "official_repo",
        "pinned_revision", "entrypoint", "model_access", "license_terms",
        "evaluator_or_ground_truth", "source_locator_ids", "closure_status", "blockers",
    ),
}


class AgreementError(ValueError):
    """Raised when the frozen R2 provenance or agreement intake is invalid."""


def _artifact_sha(value: object) -> str:
    return r2.sha256_bytes(r2.json_bytes(value))


def _validate_minimum(minimum: float) -> float:
    if isinstance(minimum, bool) or minimum != AGREEMENT_MINIMUM:
        raise AgreementError(f"frozen agreement minimum is exactly {AGREEMENT_MINIMUM}")
    return AGREEMENT_MINIMUM


def _validate_static_artifacts(
    *, frozen: dict[str, Any], runtime_intake: dict[str, Any],
    response_schema: dict[str, Any], source_manifest: dict[str, Any],
    distribution_manifest: dict[str, Any], delivery_receipt_schema: dict[str, Any],
    positive_support_preflight: dict[str, Any],
) -> None:
    if _artifact_sha(frozen) != FROZEN_CONTRACT_SHA256:
        raise AgreementError("caller input differs from compiled R2 frozen contract")
    if frozen.get("agreement_minimum") != AGREEMENT_MINIMUM:
        raise AgreementError("compiled contract differs from frozen agreement minimum")
    exact = (
        ("response schema SHA", response_schema, "response_schema_sha256"),
        ("source manifest SHA", source_manifest, "source_manifest_sha256"),
        ("distribution manifest SHA", distribution_manifest, "distribution_manifest_sha256"),
        ("delivery receipt schema SHA", delivery_receipt_schema, "delivery_receipt_schema_sha256"),
        ("positive support preflight SHA", positive_support_preflight, "positive_support_preflight_sha256"),
    )
    for label, artifact, key in exact:
        if _artifact_sha(artifact) != frozen.get(key):
            raise AgreementError(f"{label} differs from frozen R2 package")
    try:
        projection = r2.static_intake_projection(runtime_intake)
    except r2.ContractError as error:
        raise AgreementError(str(error)) from error
    if _artifact_sha(projection) != frozen.get("base_intake_static_sha256"):
        raise AgreementError("runtime agreement differs from frozen R2 base intake")
    if _artifact_sha(r2._rendition_map(source_manifest)) != frozen.get("paper_rendition_map_sha256"):
        raise AgreementError("source manifest differs from frozen R2 rendition map")
    if distribution_manifest.get("content_bundle_sha256") != frozen.get("content_bundle_sha256"):
        raise AgreementError("distribution content bundle differs from frozen R2 package")
    if distribution_manifest.get("coder_prompt_sha256") != frozen.get("prompt_sha256"):
        raise AgreementError("distribution prompt differs from frozen R2 package")
    if positive_support_preflight.get("status") != "PASS":
        raise AgreementError("mandatory positive-support preflight is not PASS")


def _validate_runtime_intake(intake: dict[str, Any]) -> tuple[list[str], list[dict[str, Any]]]:
    if intake.get("schema") != "sf-stage1c-v2-agreement-intake-contract-v6":
        raise AgreementError("unknown R2 runtime agreement intake schema")
    if intake.get("status") != "BOUND_FOR_PRE_ADJUDICATION_AGREEMENT":
        raise AgreementError("agreement intake is not bound for pre-adjudication comparison")
    if intake.get("agreement_minimum") != AGREEMENT_MINIMUM:
        raise AgreementError("runtime intake differs from frozen agreement minimum")
    if not intake.get("compiler_owned_object_identity_required"):
        raise AgreementError("runtime intake does not require compiler-owned object identity")
    if not intake.get("unmatched_objects_enter_critical_field_denominators"):
        raise AgreementError("runtime intake drops unmatched objects from field denominators")
    paper_ids, items = intake.get("canonical_paper_ids"), intake.get("items")
    if (
        intake.get("N") != 56
        or not isinstance(paper_ids, list)
        or len(paper_ids) != 56
        or len(set(paper_ids)) != 56
        or not isinstance(items, list)
        or len(items) != 56
        or {row.get("paper_id") for row in items} != set(paper_ids)
    ):
        raise AgreementError("agreement intake requires exact N=56 frozen paper bindings")
    slots = intake.get("coder_slots")
    if not isinstance(slots, list) or len(slots) != 2 or {row.get("coder_slot") for row in slots} != {"A", "B"}:
        raise AgreementError("agreement intake requires exact coder slots A/B")
    expected_models = {"A": "gpt-5.6-sol", "B": "gpt-5.6-terra"}
    for field in ("coder_id", "coder_transaction_id", "process_id", "task_id"):
        values = [slot.get(field) for slot in slots]
        if any(not isinstance(value, str) or not value for value in values) or len(set(values)) != 2:
            raise AgreementError(f"coder slots require distinct non-empty {field}")
    for slot in slots:
        if slot.get("assignment_status") != "FROZEN_SUBMITTED":
            raise AgreementError("both coder slots must be frozen before agreement")
        expected_model = expected_models[slot["coder_slot"]]
        if slot.get("planned_model") != expected_model or slot.get("model") != expected_model:
            raise AgreementError("bound coder model differs from frozen isolated-model plan")
        if slot.get("expected_content_bundle_sha256") != intake.get("content_bundle_sha256"):
            raise AgreementError("coder slot expected content bundle differs")
        if slot.get("expected_prompt_hash") != intake.get("prompt_hash"):
            raise AgreementError("coder slot expected prompt differs")
    return paper_ids, sorted(slots, key=lambda row: row["coder_slot"])


def _validate_delivery_receipts(
    *, receipts: list[dict[str, Any]], slots: list[dict[str, Any]],
    schema: dict[str, Any], distribution: dict[str, Any], intake: dict[str, Any],
) -> None:
    try:
        v5._validate_delivery_receipts(
            receipts=receipts,
            slots=slots,
            schema=schema,
            distribution=distribution,
            intake=intake,
        )
    except v5.AgreementError as error:
        raise AgreementError(str(error)) from error


def _validate_response_set(
    rows: list[dict[str, Any]], *, slot: dict[str, Any], expected_ids: set[str],
    packet_by_paper: dict[str, str], intake: dict[str, Any],
    response_schema: dict[str, Any], source_manifest: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    try:
        indexed = v3._index_responses(rows)
    except v3.AgreementError as error:
        raise AgreementError(str(error)) from error
    if len(indexed) != 56 or set(indexed) != expected_ids:
        raise AgreementError("coder response set differs from exact frozen N=56")
    compiled: dict[str, dict[str, Any]] = {}
    for paper_id, response in indexed.items():
        if response.get("coder_id") != slot["coder_id"]:
            raise AgreementError("response coder_id differs from runtime slot")
        if response.get("coder_transaction_id") != slot["coder_transaction_id"]:
            raise AgreementError("response coder transaction differs from runtime slot")
        if response.get("source_manifest_id") != intake["source_manifest_id"]:
            raise AgreementError("response source manifest binding differs")
        if response.get("packet_item_id") != packet_by_paper[paper_id]:
            raise AgreementError("response packet item binding differs")
        try:
            r2.validate_completed_response(response, response_schema, source_manifest)
            compiled[paper_id] = r2.compile_response_objects(response, source_manifest)
        except (r2.ContractError, ValueError) as error:
            raise AgreementError(f"invalid completed response for {paper_id}: {error}") from error
    return compiled


def _compute_metrics(
    left: dict[str, dict[str, Any]], right: dict[str, dict[str, Any]],
    paper_ids: list[str], minimum: float,
) -> dict[str, Any]:
    pairs = [(left[paper_id], right[paper_id]) for paper_id in sorted(paper_ids)]
    paper_level: dict[str, Any] = {}
    for field in SINGLE_LABEL_FIELDS:
        paper_level[field] = v3._paper_field_gate(pairs, field, minimum=minimum, multilabel=False)
    for field in MULTILABEL_FIELDS:
        paper_level[field] = v3._paper_field_gate(pairs, field, minimum=minimum, multilabel=True)

    object_level: dict[str, Any] = {}
    all_statuses = [gate["gate_status"] for gate in paper_level.values()]
    for array_name in OBJECT_ARRAYS:
        matches = left_total = right_total = union_total = 0
        field_counts = {
            field: {"numerator": 0, "denominator": 0}
            for field in CRITICAL_OBJECT_FIELDS[array_name]
        }
        for paper_id in sorted(paper_ids):
            try:
                left_objects = v3._object_index(left[paper_id], array_name)
                right_objects = v3._object_index(right[paper_id], array_name)
            except v3.AgreementError as error:
                raise AgreementError(str(error)) from error
            left_total += len(left_objects)
            right_total += len(right_objects)
            common = set(left_objects) & set(right_objects)
            union = sorted(set(left_objects) | set(right_objects))
            matches += len(common)
            union_total += len(union)
            for key in union:
                for field, counts in field_counts.items():
                    counts["denominator"] += 1
                    if key not in common:
                        continue
                    try:
                        left_value = v3._get_path(left_objects[key], field)
                        right_value = v3._get_path(right_objects[key], field)
                    except v3.AgreementError as error:
                        raise AgreementError(str(error)) from error
                    counts["numerator"] += (
                        v3._canonical_value(left_value) == v3._canonical_value(right_value)
                    )
        precision = v3._ratio(matches, right_total)
        recall = v3._ratio(matches, left_total)
        if precision is None and recall is None:
            f1 = None
        elif not precision or not recall:
            f1 = 0.0
        else:
            f1 = 2 * precision * recall / (precision + recall)
        segmentation_status = v3._gate(f1, minimum)
        critical_gates: dict[str, Any] = {}
        for field, counts in field_counts.items():
            exact = v3._ratio(counts["numerator"], counts["denominator"])
            critical_gates[field] = {
                **counts,
                "exact_agreement": exact,
                "gate_status": v3._gate(exact, minimum),
            }
        statuses = [segmentation_status, *(gate["gate_status"] for gate in critical_gates.values())]
        combined = r2_guards.object_gate_status(left_total, right_total, statuses)
        object_level[array_name] = {
            "coder_a_objects": left_total,
            "coder_b_objects": right_total,
            "matched_objects": matches,
            "union_objects": union_total,
            "segmentation_precision": precision,
            "segmentation_recall": recall,
            "segmentation_f1": f1,
            "segmentation_gate_status": segmentation_status,
            "critical_field_gates": critical_gates,
            "gate_status": combined,
        }
        all_statuses.extend(statuses)
    return {
        "paper_level": paper_level,
        "object_level": object_level,
        "critical_path_gate_count": len(all_statuses),
        "overall_gate_status": (
            "PASS" if all_statuses and all(status == "PASS" for status in all_statuses) else "FAIL"
        ),
    }


def compute_agreement(
    coder_a: list[dict[str, Any]], coder_b: list[dict[str, Any]], *,
    runtime_intake: dict[str, Any], frozen_contract: dict[str, Any],
    response_schema: dict[str, Any], source_manifest: dict[str, Any],
    distribution_manifest: dict[str, Any], delivery_receipt_schema: dict[str, Any],
    delivery_receipts: list[dict[str, Any]], positive_support_preflight: dict[str, Any],
    minimum: float = AGREEMENT_MINIMUM,
) -> dict[str, Any]:
    minimum = _validate_minimum(minimum)
    _validate_static_artifacts(
        frozen=frozen_contract,
        runtime_intake=runtime_intake,
        response_schema=response_schema,
        source_manifest=source_manifest,
        distribution_manifest=distribution_manifest,
        delivery_receipt_schema=delivery_receipt_schema,
        positive_support_preflight=positive_support_preflight,
    )
    paper_ids, slots = _validate_runtime_intake(runtime_intake)
    _validate_delivery_receipts(
        receipts=delivery_receipts,
        slots=slots,
        schema=delivery_receipt_schema,
        distribution=distribution_manifest,
        intake=runtime_intake,
    )
    packet_by_paper = {row["paper_id"]: row["packet_item_id"] for row in runtime_intake["items"]}
    expected_ids = set(paper_ids)
    left = _validate_response_set(
        coder_a,
        slot=slots[0],
        expected_ids=expected_ids,
        packet_by_paper=packet_by_paper,
        intake=runtime_intake,
        response_schema=response_schema,
        source_manifest=source_manifest,
    )
    right = _validate_response_set(
        coder_b,
        slot=slots[1],
        expected_ids=expected_ids,
        packet_by_paper=packet_by_paper,
        intake=runtime_intake,
        response_schema=response_schema,
        source_manifest=source_manifest,
    )
    metrics = _compute_metrics(left, right, paper_ids, AGREEMENT_MINIMUM)
    return {
        "schema": "sf-stage1c-v2-calibration-agreement-result-v6",
        "agreement_intake_contract_id": runtime_intake["artifact_id"],
        "paper_count": len(paper_ids),
        "minimum": AGREEMENT_MINIMUM,
        **metrics,
        "compiler_owned_identity_validated": True,
        "unmatched_union_denominators_applied": True,
        "frozen_provenance_validated": True,
        "adjudication_applied": False,
    }


if __name__ == "__main__":
    raise SystemExit("Import compute_agreement with two frozen R2 coder response sets.")
