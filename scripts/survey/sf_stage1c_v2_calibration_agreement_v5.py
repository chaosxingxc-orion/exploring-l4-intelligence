#!/usr/bin/env python3
"""Fail-closed pre-adjudication agreement for Agentic RC2R3."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, ValidationError

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import sf_stage1c_v2_calibration_agreement_v4 as v4
    import sf_stage1c_v2_precalibration_rc2r3 as rc2r3
else:
    from scripts.survey import sf_stage1c_v2_calibration_agreement_v4 as v4
    from scripts.survey import sf_stage1c_v2_precalibration_rc2r3 as rc2r3


# Patched from the deterministic RC2R3 build before the release commit.
FROZEN_CONTRACT_SHA256 = "5c7b864adbde92c66d2230437fa5a09d1a6c5da5c9939afb4a7132279c2e8696"
AGREEMENT_MINIMUM = 0.85

OBJECT_ARRAYS = v4.OBJECT_ARRAYS
SINGLE_LABEL_FIELDS = v4.SINGLE_LABEL_FIELDS
MULTILABEL_FIELDS = v4.MULTILABEL_FIELDS
CRITICAL_OBJECT_FIELDS = v4.CRITICAL_OBJECT_FIELDS


class AgreementError(ValueError):
    """Raised when frozen provenance or agreement intake is invalid."""


def _artifact_sha(value: object) -> str:
    return rc2r3.sha256_bytes(rc2r3.json_bytes(value))


def _validate_minimum(minimum: float) -> float:
    if isinstance(minimum, bool) or minimum != AGREEMENT_MINIMUM:
        raise AgreementError(f"frozen agreement minimum is exactly {AGREEMENT_MINIMUM}")
    return AGREEMENT_MINIMUM


def _validate_static_artifacts(
    *, frozen: dict[str, Any], runtime_intake: dict[str, Any],
    response_schema: dict[str, Any], source_manifest: dict[str, Any],
    distribution_manifest: dict[str, Any], delivery_receipt_schema: dict[str, Any],
) -> None:
    if _artifact_sha(frozen) != FROZEN_CONTRACT_SHA256:
        raise AgreementError("caller input differs from compiled RC2R3 frozen contract")
    if frozen.get("agreement_minimum") != AGREEMENT_MINIMUM:
        raise AgreementError("compiled contract differs from frozen agreement minimum")
    exact = (
        ("response schema SHA", response_schema, "response_schema_sha256"),
        ("source manifest SHA", source_manifest, "source_manifest_sha256"),
        ("distribution manifest SHA", distribution_manifest, "distribution_manifest_sha256"),
        ("delivery receipt schema SHA", delivery_receipt_schema, "delivery_receipt_schema_sha256"),
    )
    for label, artifact, key in exact:
        if _artifact_sha(artifact) != frozen.get(key):
            raise AgreementError(f"{label} differs from frozen RC2R3 package")
    try:
        projection = rc2r3.static_intake_projection(runtime_intake)
    except rc2r3.ContractError as error:
        raise AgreementError(str(error)) from error
    if _artifact_sha(projection) != frozen.get("base_intake_static_sha256"):
        raise AgreementError("runtime agreement differs from frozen RC2R3 base intake")
    if runtime_intake.get("agreement_minimum") != AGREEMENT_MINIMUM:
        raise AgreementError("runtime intake differs from frozen agreement minimum")
    if _artifact_sha(rc2r3._rendition_map(source_manifest)) != frozen.get("paper_rendition_map_sha256"):
        raise AgreementError("source manifest differs from frozen rendition map")
    if distribution_manifest.get("content_bundle_sha256") != frozen.get("content_bundle_sha256"):
        raise AgreementError("distribution content bundle differs from frozen package")
    if distribution_manifest.get("coder_prompt_sha256") != frozen.get("prompt_sha256"):
        raise AgreementError("distribution prompt differs from frozen package")


def _validate_runtime_intake(intake: dict[str, Any]) -> tuple[list[str], list[dict[str, Any]]]:
    if intake.get("schema") != "sf-stage1c-v2-agreement-intake-contract-v5":
        raise AgreementError("unknown RC2R3 runtime agreement intake schema")
    if intake.get("status") != "BOUND_FOR_PRE_ADJUDICATION_AGREEMENT":
        raise AgreementError("agreement intake is not bound for pre-adjudication comparison")
    if intake.get("agreement_minimum") != AGREEMENT_MINIMUM:
        raise AgreementError("runtime intake differs from frozen agreement minimum")
    paper_ids, items = intake.get("canonical_paper_ids"), intake.get("items")
    if (
        intake.get("N") != 56 or not isinstance(paper_ids, list) or len(paper_ids) != 56
        or len(set(paper_ids)) != 56 or not isinstance(items, list) or len(items) != 56
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


def _receipt_digest(receipt: dict[str, Any]) -> str:
    return _artifact_sha(rc2r3._receipt_projection(receipt))


def _validate_delivery_receipts(
    *, receipts: list[dict[str, Any]], slots: list[dict[str, Any]],
    schema: dict[str, Any], distribution: dict[str, Any], intake: dict[str, Any],
) -> None:
    if len(receipts) != 2 or {row.get("coder_slot") for row in receipts} != {"A", "B"}:
        raise AgreementError("exactly two A/B delivery receipts are required")
    by_slot = {row["coder_slot"]: row for row in receipts}
    expected_artifacts = [{key: row[key] for key in ("artifact_name", "bytes", "sha256")} for row in distribution["artifacts"]]
    for slot in slots:
        receipt = by_slot[slot["coder_slot"]]
        try:
            Draft202012Validator(schema).validate(receipt)
        except ValidationError as error:
            raise AgreementError(f"invalid delivery receipt: {error.message}") from error
        if receipt.get("receipt_sha256") != _receipt_digest(receipt):
            raise AgreementError("delivery receipt self-digest differs")
        for receipt_key, slot_key in (
            ("coder_id", "coder_id"), ("coder_transaction_id", "coder_transaction_id"),
            ("process_id", "process_id"), ("task_id", "task_id"), ("model", "model"),
        ):
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
        for key in ("delivery_receipt_id", "distribution_receipt_id"):
            if slot.get(key) != receipt.get("receipt_id"):
                raise AgreementError(f"runtime slot {key} differs")
        if slot.get("delivery_receipt_sha256") != receipt.get("receipt_sha256"):
            raise AgreementError("runtime slot delivery receipt digest differs")
        if slot.get("received_content_bundle_sha256") != receipt.get("received_content_bundle_sha256"):
            raise AgreementError("runtime slot actual content bundle differs")
        if slot.get("received_prompt_sha256") != receipt.get("received_prompt_sha256"):
            raise AgreementError("runtime slot actual prompt differs")


def compute_agreement(
    coder_a: list[dict[str, Any]], coder_b: list[dict[str, Any]], *,
    runtime_intake: dict[str, Any], frozen_contract: dict[str, Any],
    response_schema: dict[str, Any], source_manifest: dict[str, Any],
    distribution_manifest: dict[str, Any], delivery_receipt_schema: dict[str, Any],
    delivery_receipts: list[dict[str, Any]], minimum: float = AGREEMENT_MINIMUM,
) -> dict[str, Any]:
    minimum = _validate_minimum(minimum)
    _validate_static_artifacts(
        frozen=frozen_contract, runtime_intake=runtime_intake,
        response_schema=response_schema, source_manifest=source_manifest,
        distribution_manifest=distribution_manifest, delivery_receipt_schema=delivery_receipt_schema,
    )
    paper_ids, slots = _validate_runtime_intake(runtime_intake)
    _validate_delivery_receipts(
        receipts=delivery_receipts, slots=slots, schema=delivery_receipt_schema,
        distribution=distribution_manifest, intake=runtime_intake,
    )
    packet_by_paper = {row["paper_id"]: row["packet_item_id"] for row in runtime_intake["items"]}
    expected_ids = set(paper_ids)
    try:
        left = v4._validate_response_set(
            coder_a, slot=slots[0], expected_ids=expected_ids, packet_by_paper=packet_by_paper,
            intake=runtime_intake, response_schema=response_schema, source_manifest=source_manifest,
        )
        right = v4._validate_response_set(
            coder_b, slot=slots[1], expected_ids=expected_ids, packet_by_paper=packet_by_paper,
            intake=runtime_intake, response_schema=response_schema, source_manifest=source_manifest,
        )
        metrics = v4._compute_metrics(left, right, paper_ids, AGREEMENT_MINIMUM)
    except v4.AgreementError as error:
        raise AgreementError(str(error)) from error
    return {
        "schema": "sf-stage1c-v2-calibration-agreement-result-v5",
        "agreement_intake_contract_id": runtime_intake["artifact_id"],
        "paper_count": len(paper_ids), "minimum": AGREEMENT_MINIMUM,
        **metrics, "frozen_provenance_validated": True, "adjudication_applied": False,
    }


if __name__ == "__main__":
    raise SystemExit("Import compute_agreement with two frozen coder response sets.")
