#!/usr/bin/env python3
"""Fail-closed pre-adjudication agreement for Agentic RC2R2."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, ValidationError

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import sf_stage1c_v2_calibration_agreement_v3 as v3
    import sf_stage1c_v2_precalibration_rc2r2 as rc2r2
else:
    from scripts.survey import sf_stage1c_v2_calibration_agreement_v3 as v3
    from scripts.survey import sf_stage1c_v2_precalibration_rc2r2 as rc2r2


# This literal is intentionally not derived from caller-supplied artifacts.  It
# is patched once from the deterministic RC2R2 build before the release commit.
FROZEN_CONTRACT_SHA256 = "e039074f5897c43fb6a26dc2bdb58bb41e52426c87c7631adec54dbe461e262f"

OBJECT_ARRAYS = v3.OBJECT_ARRAYS
SINGLE_LABEL_FIELDS = v3.SINGLE_LABEL_FIELDS
MULTILABEL_FIELDS = v3.MULTILABEL_FIELDS
CRITICAL_OBJECT_FIELDS = v3.CRITICAL_OBJECT_FIELDS


class AgreementError(ValueError):
    """Raised when frozen provenance or agreement intake is invalid."""


def _artifact_sha(value: object) -> str:
    return rc2r2.sha256_bytes(rc2r2.json_bytes(value))


def _validate_compiled_root(frozen: dict[str, Any]) -> None:
    if _artifact_sha(frozen) != FROZEN_CONTRACT_SHA256:
        raise AgreementError("caller input differs from compiled frozen contract")


def _validate_static_artifacts(
    *, frozen: dict[str, Any], runtime_intake: dict[str, Any],
    response_schema: dict[str, Any], source_manifest: dict[str, Any],
    distribution_manifest: dict[str, Any], delivery_receipt_schema: dict[str, Any],
) -> None:
    _validate_compiled_root(frozen)
    exact = (
        ("response schema SHA", response_schema, "response_schema_sha256"),
        ("source manifest SHA", source_manifest, "source_manifest_sha256"),
        ("distribution manifest SHA", distribution_manifest, "distribution_manifest_sha256"),
        ("delivery receipt schema SHA", delivery_receipt_schema, "delivery_receipt_schema_sha256"),
    )
    for label, artifact, key in exact:
        if _artifact_sha(artifact) != frozen.get(key):
            raise AgreementError(f"{label} differs from frozen package")
    try:
        projection = rc2r2.static_intake_projection(runtime_intake)
    except rc2r2.ContractError as error:
        raise AgreementError(str(error)) from error
    if _artifact_sha(projection) != frozen.get("base_intake_static_sha256"):
        raise AgreementError("runtime agreement differs from frozen base intake")
    if _artifact_sha(rc2r2._rendition_map(source_manifest)) != frozen.get("paper_rendition_map_sha256"):
        raise AgreementError("source manifest differs from frozen rendition map")
    if distribution_manifest.get("content_bundle_sha256") != frozen.get("content_bundle_sha256"):
        raise AgreementError("distribution content bundle differs from frozen package")
    if distribution_manifest.get("coder_prompt_sha256") != frozen.get("prompt_sha256"):
        raise AgreementError("distribution prompt differs from frozen package")


def _validate_runtime_intake(intake: dict[str, Any]) -> tuple[list[str], list[dict[str, Any]]]:
    if intake.get("schema") != "sf-stage1c-v2-agreement-intake-contract-v4":
        raise AgreementError("unknown runtime agreement intake schema")
    if intake.get("status") != "BOUND_FOR_PRE_ADJUDICATION_AGREEMENT":
        raise AgreementError("agreement intake is not bound for pre-adjudication comparison")
    paper_ids = intake.get("canonical_paper_ids")
    items = intake.get("items")
    if (
        intake.get("N") != 56 or not isinstance(paper_ids, list) or len(paper_ids) != 56
        or len(set(paper_ids)) != 56 or not isinstance(items, list) or len(items) != 56
        or {row.get("paper_id") for row in items} != set(paper_ids)
    ):
        raise AgreementError("agreement intake requires exact N=56 frozen paper bindings")
    slots = intake.get("coder_slots")
    if not isinstance(slots, list) or len(slots) != 2 or {slot.get("coder_slot") for slot in slots} != {"A", "B"}:
        raise AgreementError("agreement intake requires exact coder slots A/B")
    expected_models = {"A": "gpt-5.6-sol", "B": "gpt-5.6-terra"}
    for field in ("coder_id", "coder_transaction_id", "process_id"):
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


def _receipt_digest(receipt: dict[str, Any]) -> str:
    return _artifact_sha(rc2r2._receipt_projection(receipt))


def _validate_delivery_receipts(
    *, receipts: list[dict[str, Any]], slots: list[dict[str, Any]],
    schema: dict[str, Any], distribution: dict[str, Any], intake: dict[str, Any],
) -> None:
    if len(receipts) != 2 or {row.get("coder_slot") for row in receipts} != {"A", "B"}:
        raise AgreementError("exactly two A/B delivery receipts are required")
    by_slot = {row["coder_slot"]: row for row in receipts}
    expected_artifacts = [{
        key: row[key] for key in ("artifact_name", "bytes", "sha256")
    } for row in distribution["artifacts"]]
    for slot in slots:
        receipt = by_slot[slot["coder_slot"]]
        try:
            Draft202012Validator(schema).validate(receipt)
        except ValidationError as error:
            raise AgreementError(f"invalid delivery receipt: {error.message}") from error
        if receipt.get("receipt_sha256") != _receipt_digest(receipt):
            raise AgreementError("delivery receipt self-digest differs")
        bindings = {
            "coder_id": "coder_id", "coder_transaction_id": "coder_transaction_id",
            "process_id": "process_id", "model": "model",
        }
        for receipt_key, slot_key in bindings.items():
            if receipt.get(receipt_key) != slot.get(slot_key):
                raise AgreementError(f"delivery receipt {receipt_key} differs from runtime slot")
        if receipt.get("distribution_manifest_id") != distribution.get("artifact_id"):
            raise AgreementError("delivery receipt distribution manifest differs")
        if receipt.get("received_content_bundle_sha256") != distribution.get("content_bundle_sha256"):
            raise AgreementError("delivery receipt actual content bundle differs")
        if receipt.get("received_prompt_sha256") != distribution.get("coder_prompt_sha256"):
            raise AgreementError("delivery receipt actual prompt differs")
        if receipt.get("received_artifacts") != expected_artifacts:
            raise AgreementError("delivery receipt actual artifact bytes differ")
        if slot.get("delivery_receipt_id") != receipt.get("receipt_id"):
            raise AgreementError("runtime slot delivery receipt ID differs")
        if slot.get("delivery_receipt_sha256") != receipt.get("receipt_sha256"):
            raise AgreementError("runtime slot delivery receipt digest differs")
        if slot.get("received_content_bundle_sha256") != receipt.get("received_content_bundle_sha256"):
            raise AgreementError("runtime slot actual content bundle differs")
        if slot.get("received_prompt_sha256") != receipt.get("received_prompt_sha256"):
            raise AgreementError("runtime slot actual prompt differs")
        for field in ("distribution_receipt_id", "submission_receipt_id"):
            if not isinstance(slot.get(field), str) or not slot[field]:
                raise AgreementError(f"runtime slot lacks {field}")
    if intake.get("content_bundle_sha256") != distribution.get("content_bundle_sha256"):
        raise AgreementError("runtime intake content bundle differs")
    if intake.get("prompt_hash") != distribution.get("coder_prompt_sha256"):
        raise AgreementError("runtime intake prompt differs")


def _index_responses(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    try:
        return v3._index_responses(rows)
    except v3.AgreementError as error:
        raise AgreementError(str(error)) from error


def _validate_response_set(
    rows: list[dict[str, Any]], *, slot: dict[str, Any], expected_ids: set[str],
    packet_by_paper: dict[str, str], intake: dict[str, Any],
    response_schema: dict[str, Any], source_manifest: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    indexed = _index_responses(rows)
    if len(indexed) != 56 or set(indexed) != expected_ids:
        raise AgreementError("coder response set differs from exact frozen N=56")
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
            rc2r2.validate_completed_response(response, response_schema, source_manifest)
        except (rc2r2.ContractError, ValueError) as error:
            raise AgreementError(f"invalid completed response for {paper_id}: {error}") from error
    return indexed


def _compute_metrics(
    left: dict[str, dict[str, Any]], right: dict[str, dict[str, Any]],
    paper_ids: list[str], minimum: float,
) -> dict[str, Any]:
    pairs = [(left[paper_id], right[paper_id]) for paper_id in sorted(paper_ids)]
    paper_level: dict[str, Any] = {}
    try:
        for field in SINGLE_LABEL_FIELDS:
            paper_level[field] = v3._paper_field_gate(pairs, field, minimum=minimum, multilabel=False)
        for field in MULTILABEL_FIELDS:
            paper_level[field] = v3._paper_field_gate(pairs, field, minimum=minimum, multilabel=True)
    except v3.AgreementError as error:
        raise AgreementError(str(error)) from error

    object_level: dict[str, Any] = {}
    all_statuses = [gate["gate_status"] for gate in paper_level.values()]
    for array_name in OBJECT_ARRAYS:
        matches = left_total = right_total = 0
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
            common = sorted(set(left_objects) & set(right_objects))
            matches += len(common)
            for key in common:
                for field, counts in field_counts.items():
                    try:
                        left_value = v3._get_path(left_objects[key], field)
                        right_value = v3._get_path(right_objects[key], field)
                    except v3.AgreementError as error:
                        raise AgreementError(str(error)) from error
                    counts["denominator"] += 1
                    counts["numerator"] += v3._canonical_value(left_value) == v3._canonical_value(right_value)
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
                **counts, "exact_agreement": exact, "gate_status": v3._gate(exact, minimum),
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
        all_statuses.extend(statuses)
    return {
        "paper_level": paper_level, "object_level": object_level,
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
    delivery_receipts: list[dict[str, Any]], minimum: float = 0.85,
) -> dict[str, Any]:
    """Validate the compiled trust chain, then compute raw agreement."""
    if not 0 < minimum <= 1:
        raise AgreementError("minimum must be in (0, 1]")
    _validate_static_artifacts(
        frozen=frozen_contract, runtime_intake=runtime_intake,
        response_schema=response_schema, source_manifest=source_manifest,
        distribution_manifest=distribution_manifest,
        delivery_receipt_schema=delivery_receipt_schema,
    )
    paper_ids, slots = _validate_runtime_intake(runtime_intake)
    _validate_delivery_receipts(
        receipts=delivery_receipts, slots=slots, schema=delivery_receipt_schema,
        distribution=distribution_manifest, intake=runtime_intake,
    )
    packet_by_paper = {row["paper_id"]: row["packet_item_id"] for row in runtime_intake["items"]}
    expected_ids = set(paper_ids)
    left = _validate_response_set(
        coder_a, slot=slots[0], expected_ids=expected_ids, packet_by_paper=packet_by_paper,
        intake=runtime_intake, response_schema=response_schema, source_manifest=source_manifest,
    )
    right = _validate_response_set(
        coder_b, slot=slots[1], expected_ids=expected_ids, packet_by_paper=packet_by_paper,
        intake=runtime_intake, response_schema=response_schema, source_manifest=source_manifest,
    )
    metrics = _compute_metrics(left, right, paper_ids, minimum)
    return {
        "schema": "sf-stage1c-v2-calibration-agreement-result-v4",
        "agreement_intake_contract_id": runtime_intake["artifact_id"],
        "paper_count": len(paper_ids), "minimum": minimum,
        **metrics, "frozen_provenance_validated": True, "adjudication_applied": False,
    }


if __name__ == "__main__":
    raise SystemExit("Import compute_agreement with two frozen coder response sets.")
