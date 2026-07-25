#!/usr/bin/env python3
"""Build the bounded Agentic calibration R2R1 method-repair contract.

R2R1 is an immutable successor to R2.  It repairs only the three defects
authorized on 2026-07-25: typed local-object identity, affirmative paper-side
reproduction closure, and exact raw-response byte binding before agreement.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator, ValidationError

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import sf_stage1c_v2_precalibration_r2 as r2
else:
    from scripts.survey import sf_stage1c_v2_precalibration_r2 as r2


REPO = Path(__file__).resolve().parents[2]
WORKBENCH = REPO / "wiki/survey/workbench/system-first-stage1c-v2-precalibration-r2r1"
CHECK_DIR = REPO / "docs/checks/stage1c-v2-precalibration/2026-07-25-r2r1"
REPORT_PATH = CHECK_DIR / "contract-report.json"
VERIFICATION_PATH = CHECK_DIR / "verification-summary.json"
REVIEW_MANIFEST_PATH = WORKBENCH / "review-package-manifest-r2r1.json"

OWNER_AUTHORIZATION = REPO / (
    "wiki/audit/system-first-stage1c-v2-calibration/"
    "round-06-owner-r2r1-bounded-method-repair-authorization/"
    "2026-07-25-stage1c-v2-agentic-calibration-r2r1-bounded-method-repair-authorization.md"
)
R2_REVIEW = REPO / (
    "wiki/audit/system-first-stage1c-v2-calibration/"
    "round-05-r2-independent-method-review/"
    "2026-07-25-stage1c-v2-agentic-calibration-r2-independent-method-review.md"
)

RESPONSE_SCHEMA_ID = "sf-stage1c-v2-calibration-response-schema-v6"
RESPONSE_SCHEMA_CONST = "sf-stage1c-v2-calibration-response-v6"
CALIBRATION_MANIFEST_ID = "SF-STAGE1C-V2-CALIBRATION-PACKET-56-R2R1"
DISTRIBUTION_MANIFEST_ID = "SF-STAGE1C-V2-CALIBRATION-DISTRIBUTION-R2R1"
AGREEMENT_INTAKE_ID = "SF-STAGE1C-V2-AGREEMENT-INTAKE-R2R1"
DELIVERY_RECEIPT_SCHEMA_ID = "sf-stage1c-v2-delivery-receipt-schema-v4"
SUBMISSION_RECEIPT_SCHEMA_ID = "sf-stage1c-v2-response-submission-receipt-schema-v1"
AGREEMENT_MINIMUM = 0.85

OBJECT_ARRAYS = r2.OBJECT_ARRAYS
OBJECT_DEFINITION_BY_ARRAY = r2.OBJECT_DEFINITION_BY_ARRAY
CODER_DISTRIBUTION_ALLOWED_ARTIFACTS = r2.CODER_DISTRIBUTION_ALLOWED_ARTIFACTS
CODER_DISTRIBUTION_FORBIDDEN_KEYS = r2.CODER_DISTRIBUTION_FORBIDDEN_KEYS
CODER_VIEW_FORBIDDEN_NAMED_EXPECTATIONS = r2.CODER_VIEW_FORBIDDEN_NAMED_EXPECTATIONS

REPRODUCTION_FACT_FIELDS = (
    "task",
    "dataset",
    "dataset_revision",
    "split",
    "official_repo",
    "pinned_revision",
    "entrypoint",
    "model_access",
    "license_terms",
    "evaluator_or_ground_truth",
)
EVIDENCE_STATES = (
    "OBSERVED_IN_SOURCE",
    "NOT_STATED_IN_SOURCE",
    "AMBIGUOUS_IN_SOURCE",
    "NOT_APPLICABLE_IN_SOURCE",
)
TARGETABLE_OBJECT_TYPES = (
    "dataset_nodes",
    "run_cells",
    "observations",
    "paired_comparisons",
    "dataset_edges",
    "claim_decisions",
    "protocol_transfer_evidence",
    "paper_reproduction_support",
)
PLACEHOLDER_VALUES = {
    "not stated in source",
    "not stated",
    "unknown",
    "unspecified",
    "unclear",
    "n/a",
    "na",
    "none",
    "not applicable",
}
DYNAMIC_REVISION_VALUES = {
    "main", "master", "head", "latest", "default", "default branch", "not pinned",
}

ARTIFACT_PATHS = {
    "response_schema": WORKBENCH / "calibration-response-schema-v6.json",
    "schema_bundle": WORKBENCH / "schema-bundle-v6.json",
    "source_manifest": WORKBENCH / "calibration-source-byte-manifest-v4-inherited.json",
    "acl_acquisition_receipts": WORKBENCH / "acl-acquisition-receipts-v2-inherited.json",
    "calibration_manifest": WORKBENCH / "calibration-manifest-v7.json",
    "blind_packet": WORKBENCH / "calibration-blind-packet-v6.json",
    "assignment_manifest": WORKBENCH / "calibration-assignment-manifest-v4-inherited.json",
    "claim_templates": WORKBENCH / "claim-template-registry-v4-inherited.json",
    "claim_template_coder_view": WORKBENCH / "claim-template-coder-view-v4-inherited.json",
    "coder_codebook": WORKBENCH / "coder-codebook-v6.json",
    "coder_prompt": WORKBENCH / "coder-prompt-v6.json",
    "agreement": WORKBENCH / "agreement-contract-v7.json",
    "agreement_intake_contract": WORKBENCH / "agreement-intake-contract-v7.json",
    "delivery_receipt_schema": WORKBENCH / "delivery-receipt-schema-v4.json",
    "delivery_receipt_template": WORKBENCH / "delivery-receipt-template-v4.json",
    "submission_receipt_schema": WORKBENCH / "submission-receipt-schema-v1.json",
    "submission_receipt_template": WORKBENCH / "submission-receipt-template-v1.json",
    "frozen_package_contract": WORKBENCH / "frozen-package-contract-v4.json",
    "coder_transaction": WORKBENCH / "coder-transaction-contract-v7.json",
    "local_reproduction_readiness": WORKBENCH / "local-reproduction-readiness-v1-inherited.json",
    "distribution_manifest": WORKBENCH / "calibration-distribution-manifest-v7.json",
    "positive_support_ledger": WORKBENCH / "positive-support-ledger-r2r1.json",
    "positive_support_preflight": WORKBENCH / "positive-support-preflight-r2r1.json",
}


class ContractError(RuntimeError):
    """Raised when the bounded R2R1 contract cannot prove a gate."""


json_bytes = r2.json_bytes
sha256_bytes = r2.sha256_bytes
sha256_path = r2.sha256_path
load_json = r2.load_json
write_json = r2.write_json
scan_coder_bundle_leaks = r2.scan_coder_bundle_leaks
coder_bundle_sha256_from_raw = r2.coder_bundle_sha256_from_raw


def _strict_object(required: list[str], properties: dict[str, Any]) -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": required,
        "properties": properties,
    }


def build_response_schema() -> dict[str, Any]:
    schema = copy.deepcopy(r2.build_response_schema())
    schema["$id"] = RESPONSE_SCHEMA_ID
    schema["properties"]["schema"] = {"const": RESPONSE_SCHEMA_CONST}

    compatibility = schema["$defs"]["compatibility_decision"]
    compatibility["properties"]["target_object_type"] = {
        "type": "string",
        "enum": list(TARGETABLE_OBJECT_TYPES),
    }
    target_index = compatibility["required"].index("target_object_id")
    compatibility["required"].insert(target_index, "target_object_type")

    support = schema["$defs"]["paper_reproduction_support"]
    support["properties"]["field_evidence_states"] = _strict_object(
        list(REPRODUCTION_FACT_FIELDS),
        {
            field: {"type": "string", "enum": list(EVIDENCE_STATES)}
            for field in REPRODUCTION_FACT_FIELDS
        },
    )
    locator_index = support["required"].index("source_locator_ids")
    support["required"].insert(locator_index, "field_evidence_states")
    return schema


def build_coder_codebook() -> dict[str, Any]:
    codebook = copy.deepcopy(r2.build_coder_codebook())
    codebook.update({
        "schema": "sf-stage1c-v2-coder-codebook-v6",
        "artifact_id": "SF-STAGE1C-V2-CODER-CODEBOOK-R2R1",
        "response_schema_id": RESPONSE_SCHEMA_ID,
        "version": "R2R1_TYPED_ID_AND_PAPER_CLOSURE",
    })
    codebook["typed_object_reference_rule"] = {
        "local_ids_unique_within_object_type": True,
        "compatibility_target_requires_object_type": True,
        "unknown_or_ambiguous_target_action": "REJECT_RESPONSE",
    }
    codebook["paper_reproduction_closure_rule"] = {
        "required_fact_fields": list(REPRODUCTION_FACT_FIELDS),
        "evidence_states": list(EVIDENCE_STATES),
        "closed_requires_all": "OBSERVED_IN_SOURCE",
        "mixed_or_unclear_access_closes": False,
        "placeholder_text_closes": False,
        "pinned_revision_must_be_immutable": True,
    }
    rows = codebook["decision_tables"]["reference_borrow_reproduce"]
    rows[-1] = {
        "when": "every paper-side fact is affirmatively OBSERVED_IN_SOURCE",
        "code": "REPRODUCTION_CANDIDATE",
        "counterexample": "a non-observed revision, entrypoint, access, terms or evaluator fact",
    }
    return codebook


def build_coder_prompt() -> dict[str, Any]:
    prompt = copy.deepcopy(r2.build_coder_prompt())
    prompt.update({
        "schema": "sf-stage1c-v2-coder-prompt-v6",
        "artifact_id": "SF-STAGE1C-V2-NEUTRAL-CODER-PROMPT-R2R1",
        "prompt_seed": "R2R1_TYPED_ID_CLOSURE_NEUTRAL_V1",
    })
    prompt["instructions"] = [
        *prompt["instructions"],
        "Keep coder-local IDs unique within each object type and type every compatibility target.",
        "For each reproduction fact, distinguish observed, not stated, ambiguous and not applicable.",
    ]
    return prompt


def build_agreement_contract() -> dict[str, Any]:
    contract = copy.deepcopy(r2.build_agreement_contract())
    contract.update({
        "schema": "sf-stage1c-v2-agreement-contract-v7",
        "artifact_id": "SF-STAGE1C-V2-AGREEMENT-CONTRACT-R2R1",
        "calibration_response_schema_id": RESPONSE_SCHEMA_ID,
        "agreement_intake_contract_id": AGREEMENT_INTAKE_ID,
        "typed_local_object_maps_required": True,
        "affirmative_reproduction_closure_required": True,
        "submission_receipts_bind_exact_response_bytes": True,
        "frozen_response_root_required": True,
    })
    return contract


def build_schema_bundle(response_schema: dict[str, Any]) -> dict[str, Any]:
    bundle = copy.deepcopy(r2.build_schema_bundle(response_schema))
    bundle.update({
        "$id": "sf-stage1c-v2-schema-bundle-v6",
        "typed_local_object_maps_required": True,
        "paper_fact_observability_states_required": True,
    })
    return bundle


def build_distribution_manifest(package: dict[str, Any]) -> dict[str, Any]:
    names = CODER_DISTRIBUTION_ALLOWED_ARTIFACTS
    raw = {name: json_bytes(package[name]) for name in names}
    return {
        "schema": "sf-stage1c-v2-calibration-distribution-manifest-v7",
        "artifact_id": DISTRIBUTION_MANIFEST_ID,
        "status": "FROZEN_INPUT_BYTES_PREPARED_NOT_DISTRIBUTED",
        "scope": "CODER_VISIBLE_SHARED_CONTENT",
        "artifacts": [
            {
                "artifact_name": name,
                "path": ARTIFACT_PATHS[name].relative_to(REPO).as_posix(),
                "bytes": len(raw[name]),
                "sha256": sha256_bytes(raw[name]),
            }
            for name in names
        ],
        "content_bundle_sha256": coder_bundle_sha256_from_raw(raw, names),
        "coder_prompt_sha256": sha256_bytes(raw["coder_prompt"]),
        "receiver_must_hash_actual_artifact_bytes": True,
        "receiver_must_hash_actual_prompt_bytes": True,
        "both_coders_must_receive_byte_identical_content": True,
        "distribution_authorized": False,
        "independent_method_accept_required": True,
    }


def build_delivery_receipt_schema() -> dict[str, Any]:
    schema = copy.deepcopy(r2.build_delivery_receipt_schema())
    schema["$id"] = DELIVERY_RECEIPT_SCHEMA_ID
    schema["properties"]["schema"] = {"const": "sf-stage1c-v2-delivery-receipt-v3"}
    schema["properties"]["receipt_id"] = {
        "type": "string",
        "pattern": r"^R2R1-DELIVERY-[AB]-[A-Za-z0-9._:-]+-[A-Za-z0-9._:-]+$",
    }
    schema["properties"]["distribution_manifest_id"] = {"const": DISTRIBUTION_MANIFEST_ID}
    return schema


def build_delivery_receipt_template() -> dict[str, Any]:
    template = copy.deepcopy(r2.build_delivery_receipt_template())
    template.update({
        "schema": "sf-stage1c-v2-delivery-receipt-template-v4",
        "artifact_id": "SF-STAGE1C-V2-DELIVERY-RECEIPT-TEMPLATE-R2R1",
        "delivery_receipt_schema_id": DELIVERY_RECEIPT_SCHEMA_ID,
    })
    return template


def build_delivery_receipt(
    package: dict[str, Any], *, received_artifacts: dict[str, bytes],
    received_prompt_bytes: bytes, slot: str, coder_id: str, transaction_id: str,
    process_id: str, task_id: str, model: str, delivered_at: str, submitted_at: str,
) -> dict[str, Any]:
    names = CODER_DISTRIBUTION_ALLOWED_ARTIFACTS
    if not isinstance(received_artifacts, dict) or set(received_artifacts) != set(names):
        raise ContractError("delivery receipt requires exact actual received artifact set")
    if not isinstance(received_prompt_bytes, bytes):
        raise ContractError("actual received prompt must be bytes")
    if any(not isinstance(received_artifacts[name], bytes) for name in names):
        raise ContractError("every actual received artifact must be bytes")
    distribution = package["distribution_manifest"]
    expected = {row["artifact_name"]: row for row in distribution["artifacts"]}
    actual_rows = [
        {
            "artifact_name": name,
            "bytes": len(received_artifacts[name]),
            "sha256": sha256_bytes(received_artifacts[name]),
        }
        for name in names
    ]
    for row in actual_rows:
        expected_row = {
            key: expected[row["artifact_name"]][key]
            for key in ("artifact_name", "bytes", "sha256")
        }
        if row != expected_row:
            raise ContractError(f"actual received artifact differs: {row['artifact_name']}")
    actual_bundle = coder_bundle_sha256_from_raw(received_artifacts, names)
    actual_prompt = sha256_bytes(received_prompt_bytes)
    if actual_bundle != distribution["content_bundle_sha256"]:
        raise ContractError("actual received artifact bundle differs")
    if actual_prompt != distribution["coder_prompt_sha256"]:
        raise ContractError("actual received prompt differs")
    if received_prompt_bytes != received_artifacts["coder_prompt"]:
        raise ContractError("actual received prompt differs from coder_prompt artifact")
    receipt = {
        "schema": "sf-stage1c-v2-delivery-receipt-v3",
        "receipt_id": f"R2R1-DELIVERY-{slot}-{transaction_id}-{task_id}",
        "coder_slot": slot,
        "coder_id": coder_id,
        "coder_transaction_id": transaction_id,
        "process_id": process_id,
        "task_id": task_id,
        "model": model,
        "distribution_manifest_id": distribution["artifact_id"],
        "received_content_bundle_sha256": actual_bundle,
        "received_prompt_sha256": actual_prompt,
        "received_artifacts": actual_rows,
        "delivered_at": delivered_at,
        "submitted_at": submitted_at,
        "status": "FROZEN_SUBMITTED",
    }
    receipt["receipt_sha256"] = sha256_bytes(json_bytes(r2._receipt_projection(receipt)))
    try:
        Draft202012Validator(package["delivery_receipt_schema"]).validate(receipt)
    except ValidationError as error:
        raise ContractError(f"invalid actual-byte delivery receipt: {error.message}") from error
    return receipt


def build_submission_receipt_schema(source_manifest_id: str) -> dict[str, Any]:
    hex64 = {"type": "string", "pattern": r"^[0-9a-f]{64}$"}
    properties = {
        "schema": {"const": "sf-stage1c-v2-response-submission-receipt-v1"},
        "receipt_id": {"type": "string", "pattern": r"^R2R1-SUBMISSION-[AB]-[0-9a-f]{16}$"},
        "coder_slot": {"type": "string", "enum": ["A", "B"]},
        "coder_id": {"type": "string", "minLength": 1},
        "coder_transaction_id": {"type": "string", "minLength": 1},
        "process_id": {"type": "string", "minLength": 1},
        "task_id": {"type": "string", "minLength": 1},
        "model": {"type": "string", "minLength": 1},
        "delivery_receipt_id": {"type": "string", "minLength": 1},
        "delivery_receipt_sha256": hex64,
        "response_schema_id": {"const": RESPONSE_SCHEMA_ID},
        "source_manifest_id": {"const": source_manifest_id},
        "response_count": {"const": 56},
        "response_bytes": {"type": "integer", "minimum": 1},
        "response_sha256": hex64,
        "canonical_paper_ids_sha256": hex64,
        "submitted_at": {"type": "string", "minLength": 1},
        "status": {"const": "FROZEN_SUBMITTED"},
        "receipt_sha256": hex64,
    }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": SUBMISSION_RECEIPT_SCHEMA_ID,
        **_strict_object(list(properties), properties),
    }


def build_submission_receipt_template() -> dict[str, Any]:
    return {
        "schema": "sf-stage1c-v2-response-submission-receipt-template-v1",
        "artifact_id": "SF-STAGE1C-V2-RESPONSE-SUBMISSION-RECEIPT-TEMPLATE-R2R1",
        "submission_receipt_schema_id": SUBMISSION_RECEIPT_SCHEMA_ID,
        "status": "TEMPLATE_NOT_A_SUBMISSION",
        "exact_canonical_raw_bytes_required": True,
        "freeze_before_agreement_required": True,
    }


def _submission_receipt_projection(receipt: dict[str, Any]) -> dict[str, Any]:
    return {key: copy.deepcopy(value) for key, value in receipt.items() if key != "receipt_sha256"}


def canonical_response_bytes(rows: list[dict[str, Any]]) -> bytes:
    return json_bytes(rows)


def _decode_canonical_responses(raw_response_bytes: bytes) -> list[dict[str, Any]]:
    if not isinstance(raw_response_bytes, bytes):
        raise ContractError("canonical raw response bytes must be bytes")
    try:
        rows = json.loads(raw_response_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ContractError("canonical raw response bytes are not valid UTF-8 JSON") from error
    if not isinstance(rows, list) or canonical_response_bytes(rows) != raw_response_bytes:
        raise ContractError("canonical raw response bytes differ from the required serialization")
    return rows


def build_submission_receipt(
    package: dict[str, Any], *, delivery_receipt: dict[str, Any], raw_response_bytes: bytes,
) -> dict[str, Any]:
    rows = _decode_canonical_responses(raw_response_bytes)
    expected_ids = package["calibration_manifest"]["canonical_ids"]
    actual_ids = [row.get("paper_id") for row in rows]
    if len(rows) == 56 and len(set(actual_ids)) != 56:
        raise ContractError("submission responses contain duplicate paper IDs")
    if len(rows) != 56 or actual_ids != expected_ids:
        raise ContractError("submission responses differ from exact N=56 canonical paper order")
    response_ids = [row.get("response_id") for row in rows]
    if any(not isinstance(value, str) or not value for value in response_ids) or len(set(response_ids)) != 56:
        raise ContractError("submission responses require 56 unique response IDs")
    slot = delivery_receipt.get("coder_slot")
    for response in rows:
        if response.get("coder_id") != delivery_receipt.get("coder_id"):
            raise ContractError("submission response coder differs from delivery receipt")
        if response.get("coder_transaction_id") != delivery_receipt.get("coder_transaction_id"):
            raise ContractError("submission response transaction differs from delivery receipt")
        validate_completed_response(
            response, package["response_schema"], package["source_manifest"]
        )
    response_sha = sha256_bytes(raw_response_bytes)
    receipt = {
        "schema": "sf-stage1c-v2-response-submission-receipt-v1",
        "receipt_id": f"R2R1-SUBMISSION-{slot}-{response_sha[:16]}",
        "coder_slot": slot,
        "coder_id": delivery_receipt["coder_id"],
        "coder_transaction_id": delivery_receipt["coder_transaction_id"],
        "process_id": delivery_receipt["process_id"],
        "task_id": delivery_receipt["task_id"],
        "model": delivery_receipt["model"],
        "delivery_receipt_id": delivery_receipt["receipt_id"],
        "delivery_receipt_sha256": delivery_receipt["receipt_sha256"],
        "response_schema_id": RESPONSE_SCHEMA_ID,
        "source_manifest_id": package["source_manifest"]["artifact_id"],
        "response_count": len(rows),
        "response_bytes": len(raw_response_bytes),
        "response_sha256": response_sha,
        "canonical_paper_ids_sha256": sha256_bytes(json_bytes(actual_ids)),
        "submitted_at": delivery_receipt["submitted_at"],
        "status": "FROZEN_SUBMITTED",
    }
    receipt["receipt_sha256"] = sha256_bytes(json_bytes(_submission_receipt_projection(receipt)))
    try:
        Draft202012Validator(package["submission_receipt_schema"]).validate(receipt)
    except ValidationError as error:
        raise ContractError(f"invalid response submission receipt: {error.message}") from error
    return receipt


def build_agreement_intake_contract(package: dict[str, Any]) -> dict[str, Any]:
    intake = copy.deepcopy(r2.build_agreement_intake_contract(package))
    intake.update({
        "schema": "sf-stage1c-v2-agreement-intake-contract-v7",
        "artifact_id": AGREEMENT_INTAKE_ID,
        "calibration_manifest_id": CALIBRATION_MANIFEST_ID,
        "response_schema_id": RESPONSE_SCHEMA_ID,
        "distribution_manifest_id": DISTRIBUTION_MANIFEST_ID,
        "delivery_receipt_schema_id": DELIVERY_RECEIPT_SCHEMA_ID,
        "submission_receipt_schema_id": SUBMISSION_RECEIPT_SCHEMA_ID,
        "typed_local_object_maps_required": True,
        "affirmative_reproduction_closure_required": True,
        "exact_response_bytes_bound_before_agreement": True,
    })
    for slot in intake["coder_slots"]:
        slot.update({
            "submission_receipt_sha256": None,
            "response_sha256": None,
            "response_bytes": None,
            "response_count": None,
        })
    return intake


def static_intake_projection(intake: dict[str, Any]) -> dict[str, Any]:
    fixed = (
        "schema", "artifact_id", "calibration_manifest_id", "response_schema_id",
        "source_manifest_id", "distribution_manifest_id", "delivery_receipt_schema_id",
        "submission_receipt_schema_id", "content_bundle_sha256", "prompt_hash",
        "agreement_minimum", "N", "canonical_paper_ids", "items",
        "completed_response_validator_required", "raw_outputs_frozen_before_agreement",
        "compiler_owned_object_identity_required",
        "unmatched_objects_enter_critical_field_denominators",
        "typed_local_object_maps_required", "affirmative_reproduction_closure_required",
        "exact_response_bytes_bound_before_agreement",
    )
    try:
        projection = {key: copy.deepcopy(intake[key]) for key in fixed}
        projection["coder_slots"] = [
            {
                "coder_slot": slot["coder_slot"],
                "planned_model": slot["planned_model"],
                "expected_content_bundle_sha256": slot["expected_content_bundle_sha256"],
                "expected_prompt_hash": slot["expected_prompt_hash"],
            }
            for slot in intake["coder_slots"]
        ]
    except (KeyError, TypeError) as error:
        raise ContractError("agreement intake lacks frozen R2R1 base fields") from error
    return projection


def _frozen_response_root(
    package: dict[str, Any], submissions: list[dict[str, Any]]
) -> dict[str, Any]:
    rows = [
        {
            "coder_slot": receipt["coder_slot"],
            "submission_receipt_id": receipt["receipt_id"],
            "submission_receipt_sha256": receipt["receipt_sha256"],
            "response_sha256": receipt["response_sha256"],
            "response_bytes": receipt["response_bytes"],
            "response_count": receipt["response_count"],
            "canonical_paper_ids_sha256": receipt["canonical_paper_ids_sha256"],
        }
        for receipt in sorted(submissions, key=lambda row: row["coder_slot"])
    ]
    root = {
        "schema": "sf-stage1c-v2-frozen-response-root-v1",
        "status": "FROZEN_RESPONSES_BOUND",
        "frozen_package_contract_sha256": sha256_bytes(
            json_bytes(package["frozen_package_contract"])
        ),
        "submission_receipts": rows,
    }
    root["root_sha256"] = sha256_bytes(json_bytes(root))
    return root


def bind_runtime_intake(
    package: dict[str, Any], bindings: Iterable[dict[str, str]],
    delivery_receipts: list[dict[str, Any]], submission_receipts: list[dict[str, Any]],
) -> dict[str, Any]:
    intake = copy.deepcopy(package["agreement_intake_contract"])
    binding_by_slot = {row["slot"]: row for row in bindings}
    delivery_by_slot = {row["coder_slot"]: row for row in delivery_receipts}
    submission_by_slot = {row["coder_slot"]: row for row in submission_receipts}
    if any(set(mapping) != {"A", "B"} for mapping in (
        binding_by_slot, delivery_by_slot, submission_by_slot
    )):
        raise ContractError("runtime intake requires exact A/B bindings and both receipt types")
    for receipt in submission_receipts:
        try:
            Draft202012Validator(package["submission_receipt_schema"]).validate(receipt)
        except ValidationError as error:
            raise ContractError(f"invalid response submission receipt: {error.message}") from error
        if receipt["receipt_sha256"] != sha256_bytes(
            json_bytes(_submission_receipt_projection(receipt))
        ):
            raise ContractError("response submission receipt hash differs")
    intake["status"] = "BOUND_FOR_PRE_ADJUDICATION_AGREEMENT"
    expected_paper_digest = sha256_bytes(json_bytes(intake["canonical_paper_ids"]))
    for target in intake["coder_slots"]:
        slot = target["coder_slot"]
        binding = binding_by_slot[slot]
        delivery = delivery_by_slot[slot]
        submission = submission_by_slot[slot]
        for receipt_key, binding_key in (
            ("coder_id", "coder_id"),
            ("coder_transaction_id", "transaction_id"),
            ("process_id", "process_id"),
            ("task_id", "task_id"),
            ("model", "model"),
        ):
            if delivery.get(receipt_key) != binding.get(binding_key):
                raise ContractError(f"runtime binding differs from delivery {receipt_key}")
            if submission.get(receipt_key) != binding.get(binding_key):
                raise ContractError(f"runtime binding differs from submission {receipt_key}")
        if (
            submission["delivery_receipt_id"] != delivery["receipt_id"]
            or submission["delivery_receipt_sha256"] != delivery["receipt_sha256"]
        ):
            raise ContractError("submission receipt is not bound to delivery receipt")
        if submission["canonical_paper_ids_sha256"] != expected_paper_digest:
            raise ContractError("submission receipt paper-ID digest differs from runtime intake")
        target.update({
            "model": binding["model"],
            "coder_id": binding["coder_id"],
            "coder_transaction_id": binding["transaction_id"],
            "process_id": binding["process_id"],
            "task_id": binding["task_id"],
            "assignment_status": "FROZEN_SUBMITTED",
            "distribution_receipt_id": delivery["receipt_id"],
            "delivery_receipt_id": delivery["receipt_id"],
            "delivery_receipt_sha256": delivery["receipt_sha256"],
            "received_content_bundle_sha256": delivery["received_content_bundle_sha256"],
            "received_prompt_sha256": delivery["received_prompt_sha256"],
            "submission_receipt_id": submission["receipt_id"],
            "submission_receipt_sha256": submission["receipt_sha256"],
            "response_sha256": submission["response_sha256"],
            "response_bytes": submission["response_bytes"],
            "response_count": submission["response_count"],
        })
    intake["frozen_response_root"] = _frozen_response_root(package, submission_receipts)
    return intake


def build_frozen_package_contract(package: dict[str, Any]) -> dict[str, Any]:
    intake = package["agreement_intake_contract"]
    return {
        "schema": "sf-stage1c-v2-frozen-package-contract-v4",
        "artifact_id": "SF-STAGE1C-V2-FROZEN-PACKAGE-CONTRACT-R2R1",
        "status": "COMPILED_ROOT_OF_TRUST_INPUT",
        "agreement_minimum": AGREEMENT_MINIMUM,
        "calibration_manifest_id": CALIBRATION_MANIFEST_ID,
        "calibration_manifest_sha256": sha256_bytes(json_bytes(package["calibration_manifest"])),
        "source_manifest_id": package["source_manifest"]["artifact_id"],
        "source_manifest_sha256": sha256_bytes(json_bytes(package["source_manifest"])),
        "distribution_manifest_id": DISTRIBUTION_MANIFEST_ID,
        "distribution_manifest_sha256": sha256_bytes(json_bytes(package["distribution_manifest"])),
        "response_schema_id": RESPONSE_SCHEMA_ID,
        "response_schema_sha256": sha256_bytes(json_bytes(package["response_schema"])),
        "delivery_receipt_schema_id": DELIVERY_RECEIPT_SCHEMA_ID,
        "delivery_receipt_schema_sha256": sha256_bytes(json_bytes(package["delivery_receipt_schema"])),
        "submission_receipt_schema_id": SUBMISSION_RECEIPT_SCHEMA_ID,
        "submission_receipt_schema_sha256": sha256_bytes(json_bytes(package["submission_receipt_schema"])),
        "base_intake_static_sha256": sha256_bytes(json_bytes(static_intake_projection(intake))),
        "paper_rendition_map_sha256": sha256_bytes(json_bytes(r2._rendition_map(package["source_manifest"]))),
        "positive_support_preflight_sha256": sha256_bytes(json_bytes(package["positive_support_preflight"])),
        "content_bundle_sha256": package["distribution_manifest"]["content_bundle_sha256"],
        "prompt_sha256": package["distribution_manifest"]["coder_prompt_sha256"],
        "N": 56,
        "canonical_paper_ids_sha256": sha256_bytes(json_bytes(intake["canonical_paper_ids"])),
        "compiled_into_agreement_engine": True,
    }


def compile_response_objects(
    response: dict[str, Any], source_manifest: dict[str, Any]
) -> dict[str, Any]:
    """Compile using per-type local-ID maps and exact typed references."""

    compiled = copy.deepcopy(response)
    locator_to_anchor, anchors = r2._anchor_index(compiled, source_manifest)
    compiled["compiled_source_anchors"] = anchors
    paper_id = compiled["paper_id"]
    typed_maps: dict[str, dict[str, str]] = {name: {} for name in OBJECT_ARRAYS}

    def compile_array(array_name: str, id_field: str, identity_builder: Any) -> None:
        seen_signatures: set[str] = set()
        local_map = typed_maps[array_name]
        for obj in compiled[array_name]:
            source_id = obj[id_field]
            if source_id in local_map:
                raise ContractError(f"duplicate coder-local {array_name} ID: {source_id}")
            anchors_for_object = r2._replace_locator_ids(obj, locator_to_anchor)
            key = r2._object_key(
                paper_id, array_name, anchors_for_object, identity_builder(obj)
            )
            if key in seen_signatures:
                raise ContractError(
                    f"duplicate compiler-derived {array_name} segmentation signature"
                )
            seen_signatures.add(key)
            local_map[source_id] = key
            obj["object_match_key"] = key

    compile_array("dataset_nodes", "dataset_node_id", lambda obj: {"name": obj["name"]})
    for obj in compiled["run_cells"]:
        try:
            obj["dataset_node_ids"] = sorted(
                typed_maps["dataset_nodes"][value] for value in obj["dataset_node_ids"]
            )
        except KeyError as error:
            raise ContractError("run cell references an undeclared dataset node") from error
    compile_array(
        "run_cells", "run_cell_id",
        lambda obj: {
            "datasets": obj["dataset_node_ids"], "model": obj["model"],
            "access": obj["access_regime"], "input": obj["input_condition"],
            "baseline_role": obj["baseline_role"],
        },
    )
    for obj in compiled["observations"]:
        try:
            obj["run_cell_id"] = typed_maps["run_cells"][obj["run_cell_id"]]
        except KeyError as error:
            raise ContractError("observation references an undeclared run cell") from error
    compile_array(
        "observations", "observation_id",
        lambda obj: {
            "run": obj["run_cell_id"], "metric": obj["metric_or_evaluator"],
            "role": obj["observation_role"],
        },
    )
    for obj in compiled["paired_comparisons"]:
        try:
            obj["baseline_cell_id"] = typed_maps["run_cells"][obj["baseline_cell_id"]]
            obj["intervention_cell_id"] = typed_maps["run_cells"][obj["intervention_cell_id"]]
        except KeyError as error:
            raise ContractError("paired comparison references an undeclared run cell") from error
    compile_array(
        "paired_comparisons", "comparison_id",
        lambda obj: {
            "baseline": obj["baseline_cell_id"],
            "intervention": obj["intervention_cell_id"],
        },
    )
    for obj in compiled["dataset_edges"]:
        try:
            obj["source_dataset_id"] = typed_maps["dataset_nodes"][obj["source_dataset_id"]]
            obj["target_dataset_id"] = typed_maps["dataset_nodes"][obj["target_dataset_id"]]
        except KeyError as error:
            raise ContractError("dataset edge references an undeclared dataset node") from error
    compile_array(
        "dataset_edges", "dataset_edge_id",
        lambda obj: {
            "edge_type": obj["edge_type"], "source": obj["source_dataset_id"],
            "target": obj["target_dataset_id"],
        },
    )
    compile_array(
        "claim_decisions", "claim_decision_id",
        lambda obj: {"template": obj["claim_template_id"], "scope": obj["scope"]},
    )
    compile_array(
        "protocol_transfer_evidence", "transfer_evidence_id",
        lambda obj: {
            "source_domain": obj["source_domain"], "source_protocol": obj["source_protocol"],
            "target_variables": obj["target_speech_omni_variables"],
        },
    )
    compile_array(
        "paper_reproduction_support", "reproduction_support_id",
        lambda obj: {
            "task": obj["task"], "dataset": obj["dataset"],
            "official_repo": obj["official_repo"],
        },
    )
    for obj in compiled["translation_or_compatibility_decisions"]:
        target_type = obj.get("target_object_type")
        target_id = obj.get("target_object_id")
        if target_type not in typed_maps or target_id not in typed_maps[target_type]:
            raise ContractError(
                f"compatibility decision references an undeclared typed target: {target_type}:{target_id}"
            )
        obj["target_object_id"] = typed_maps[target_type][target_id]
    compile_array(
        "translation_or_compatibility_decisions", "decision_id",
        lambda obj: {
            "type": obj["decision_type"], "target_type": obj["target_object_type"],
            "target": obj["target_object_id"],
        },
    )
    return compiled


def _normalized_placeholder(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    normalized = " ".join(value.casefold().replace("_", " ").split())
    return normalized in PLACEHOLDER_VALUES


def _support_is_affirmatively_closed(row: dict[str, Any]) -> bool:
    states = row.get("field_evidence_states", {})
    revision = " ".join(row.get("pinned_revision", "").casefold().split())
    return (
        set(states) == set(REPRODUCTION_FACT_FIELDS)
        and all(states[field] == "OBSERVED_IN_SOURCE" for field in REPRODUCTION_FACT_FIELDS)
        and all(not _normalized_placeholder(row[field]) for field in REPRODUCTION_FACT_FIELDS)
        and row["model_access"] != "MIXED_OR_UNCLEAR"
        and revision not in DYNAMIC_REVISION_VALUES
        and row["closure_status"] == "CLOSED_PAPER_SUPPORT"
        and not row["blockers"]
    )


def validate_completed_response(
    response: dict[str, Any], response_schema: dict[str, Any], source_manifest: dict[str, Any]
) -> None:
    try:
        r2.validate_completed_response(response, response_schema, source_manifest)
    except r2.ContractError as error:
        raise ContractError(str(error)) from error
    support = response["paper_reproduction_support"]
    for row in support:
        states = row["field_evidence_states"]
        for field in REPRODUCTION_FACT_FIELDS:
            if states[field] == "OBSERVED_IN_SOURCE" and _normalized_placeholder(row[field]):
                if row["closure_status"] == "CLOSED_PAPER_SUPPORT":
                    raise ContractError("closed paper support cannot use a placeholder value")
                raise ContractError("observed reproduction fact cannot use a placeholder value")
        if row["closure_status"] == "CLOSED_PAPER_SUPPORT":
            if not _support_is_affirmatively_closed(row):
                raise ContractError("closed paper support requires every fact affirmatively observed")
        else:
            if not any(states[field] != "OBSERVED_IN_SOURCE" for field in REPRODUCTION_FACT_FIELDS):
                raise ContractError("open paper support requires at least one non-observed fact")
            if not row["blockers"]:
                raise ContractError("OPEN_WITH_BLOCKERS requires at least one blocker")
    if response["paper_labels"]["reference_borrow_reproduce"] == "REPRODUCTION_CANDIDATE":
        if not any(_support_is_affirmatively_closed(row) for row in support):
            raise ContractError("REPRODUCTION_CANDIDATE requires every fact affirmatively observed")
    compile_response_objects(response, source_manifest)


def build_positive_support_ledger(package: dict[str, Any]) -> dict[str, Any]:
    ledger = copy.deepcopy(r2.build_positive_support_ledger(package))
    ledger.update({
        "schema": "sf-stage1c-v2-positive-support-ledger-v3",
        "artifact_id": "SF-STAGE1C-V2-POSITIVE-SUPPORT-LEDGER-R2R1",
    })
    row = ledger["evidence"]["paper_reproduction_support"][0]["object"]
    row["field_evidence_states"] = {
        field: "OBSERVED_IN_SOURCE" for field in REPRODUCTION_FACT_FIELDS
    }
    row["field_evidence_states"].update({
        "pinned_revision": "NOT_STATED_IN_SOURCE",
        "entrypoint": "NOT_STATED_IN_SOURCE",
        "model_access": "AMBIGUOUS_IN_SOURCE",
        "license_terms": "NOT_STATED_IN_SOURCE",
    })
    return ledger


def validate_positive_support(
    ledger: dict[str, Any], package: dict[str, Any]
) -> dict[str, Any]:
    try:
        report = r2.validate_positive_support(ledger, package)
    except r2.ContractError as error:
        raise ContractError(str(error)) from error
    report.update({
        "schema": "sf-stage1c-v2-positive-support-preflight-v3",
        "artifact_id": "SF-STAGE1C-V2-POSITIVE-SUPPORT-PREFLIGHT-R2R1",
    })
    return report


def build_package() -> dict[str, Any]:
    predecessor = r2.build_package()
    package = copy.deepcopy(predecessor)
    package["response_schema"] = build_response_schema()
    package["schema_bundle"] = build_schema_bundle(package["response_schema"])
    package["calibration_manifest"].update({
        "schema": "sf-stage1c-v2-calibration-manifest-v7",
        "artifact_id": CALIBRATION_MANIFEST_ID,
        "status": "AGENTIC_CALIBRATION_R2R1_METHOD_READY_NOT_DISTRIBUTED",
        "calibration_response_schema_id": RESPONSE_SCHEMA_ID,
        "r2_artifacts_immutable": True,
    })
    package["blind_packet"].update({
        "schema": "sf-stage1c-v2-calibration-blind-packet-v6",
        "artifact_id": "SF-STAGE1C-V2-LABEL-HIDDEN-PACKET-56-R2R1",
        "calibration_response_schema_id": RESPONSE_SCHEMA_ID,
    })
    for item in package["blind_packet"]["items"]:
        item["blank_response"]["schema"] = RESPONSE_SCHEMA_CONST
    package["coder_codebook"] = build_coder_codebook()
    package["coder_prompt"] = build_coder_prompt()
    package["agreement"] = build_agreement_contract()
    package["local_reproduction_readiness"] = copy.deepcopy(
        predecessor["local_reproduction_readiness"]
    )
    package["local_reproduction_readiness"]["artifact_id"] = (
        "SF-STAGE1C-V2-LOCAL-REPRODUCTION-READINESS-R2R1"
    )
    package["delivery_receipt_schema"] = build_delivery_receipt_schema()
    package["delivery_receipt_template"] = build_delivery_receipt_template()
    package["submission_receipt_schema"] = build_submission_receipt_schema(
        package["source_manifest"]["artifact_id"]
    )
    package["submission_receipt_template"] = build_submission_receipt_template()
    package["distribution_manifest"] = build_distribution_manifest(package)
    package["coder_transaction"].update({
        "schema": "sf-stage1c-v2-coder-transaction-contract-v7",
        "artifact_id": "SF-STAGE1C-V2-CODER-INTAKE-R2R1",
        "distribution_manifest_id": DISTRIBUTION_MANIFEST_ID,
        "delivery_receipt_schema_id": DELIVERY_RECEIPT_SCHEMA_ID,
        "submission_receipt_schema_id": SUBMISSION_RECEIPT_SCHEMA_ID,
        "calibration_response_schema_id": RESPONSE_SCHEMA_ID,
        "shared_content_bundle_sha256": package["distribution_manifest"]["content_bundle_sha256"],
        "independent_method_accept_required": True,
    })
    for slot in package["coder_transaction"]["coder_slots"]:
        slot["expected_content_bundle_sha256"] = package["distribution_manifest"]["content_bundle_sha256"]
        slot["expected_prompt_hash"] = package["distribution_manifest"]["coder_prompt_sha256"]
        slot["task_id"] = None
    package["agreement_intake_contract"] = build_agreement_intake_contract(package)
    package["positive_support_ledger"] = build_positive_support_ledger(package)
    package["positive_support_preflight"] = validate_positive_support(
        package["positive_support_ledger"], package
    )
    package["frozen_package_contract"] = build_frozen_package_contract(package)
    return package


def validate_package(package: dict[str, Any]) -> None:
    predecessor = r2.build_package()
    calibration = package["calibration_manifest"]
    if (
        calibration.get("N") != 56
        or calibration.get("canonical_ids") != predecessor["calibration_manifest"]["canonical_ids"]
        or package["source_manifest"] != predecessor["source_manifest"]
    ):
        raise ContractError("R2R1 must preserve exact N=56 source identities and bytes")
    if calibration.get("overlay_count") != 38 or calibration.get("sentinel_count") != 18:
        raise ContractError("R2R1 must preserve 38 overlays plus 18 sentinels")
    if package["response_schema"].get("$id") != RESPONSE_SCHEMA_ID:
        raise ContractError("R2R1 response schema identity differs")
    compatibility = package["response_schema"]["$defs"]["compatibility_decision"]
    if "target_object_type" not in compatibility["required"]:
        raise ContractError("R2R1 compatibility targets are not typed")
    support = package["response_schema"]["$defs"]["paper_reproduction_support"]
    if "field_evidence_states" not in support["required"]:
        raise ContractError("R2R1 paper reproduction facts are not typed")
    validator = Draft202012Validator(package["response_schema"])
    for item in package["blind_packet"]["items"]:
        validator.validate(item["blank_response"])
    names = tuple(row["artifact_name"] for row in package["distribution_manifest"]["artifacts"])
    if names != CODER_DISTRIBUTION_ALLOWED_ARTIFACTS:
        raise ContractError("R2R1 coder-visible artifact set changed")
    leaks = scan_coder_bundle_leaks(package, names)
    if leaks:
        raise ContractError(f"coder-visible leakage detected: {leaks}")
    if package["distribution_manifest"].get("distribution_authorized"):
        raise ContractError("R2R1 coder distribution occurred before independent ACCEPT")
    raw = {name: json_bytes(package[name]) for name in names}
    if package["distribution_manifest"]["content_bundle_sha256"] != coder_bundle_sha256_from_raw(raw, names):
        raise ContractError("R2R1 coder bundle hash is stale")
    for row in package["distribution_manifest"]["artifacts"]:
        actual = raw[row["artifact_name"]]
        if row["bytes"] != len(actual) or row["sha256"] != sha256_bytes(actual):
            raise ContractError(f"R2R1 distribution artifact is stale: {row['artifact_name']}")
    if package["agreement"].get("agreement_minimum") != AGREEMENT_MINIMUM:
        raise ContractError("R2R1 agreement threshold differs from 0.85")
    if package["positive_support_preflight"].get("status") != "PASS":
        raise ContractError("R2R1 mandatory positive-support preflight did not pass")
    if validate_positive_support(package["positive_support_ledger"], package) != package["positive_support_preflight"]:
        raise ContractError("R2R1 positive-support preflight is stale")
    if any(
        row.get("anchor_status") == "REPRODUCTION_ANCHOR"
        for row in package["local_reproduction_readiness"]["candidates"]
    ):
        raise ContractError("R2R1 promoted a reproduction anchor")
    if package["frozen_package_contract"] != build_frozen_package_contract(package):
        raise ContractError("R2R1 frozen package contract is stale")


def build_report(package: dict[str, Any]) -> dict[str, Any]:
    validate_package(package)
    return {
        "schema": "sf-stage1c-v2-precalibration-contract-report-v7",
        "artifact_id": "SF-STAGE1C-V2-PRECALIBRATION-CONTRACT-REPORT-R2R1",
        "as_of": "2026-07-25",
        "status": "AGENTIC_CALIBRATION_R2R1_METHOD_READY_NOT_DISTRIBUTED",
        "predecessor": {
            "release": "AGENTIC_CALIBRATION_R2_WITHHELD",
            "r1_and_r2_immutable": True,
            "sample_unchanged": True,
        },
        "authority": {
            "bounded_r2r1_repair_authorized": True,
            "independent_method_accept_obtained": False,
            "coder_distributed": False,
            "agreement_computed": False,
            "owner_adjudication_applied": False,
            "full_mapping_signed": False,
            "research_model_called": False,
            "benchmark_metric_run": False,
            "paper_reproduction_run": False,
            "prototype_created": False,
            "novelty_verdict_made": False,
            "push_authorized": False,
        },
        "bounded_defect_closure": {
            "duplicate_local_ids_rejected": True,
            "typed_cross_object_references": True,
            "affirmative_paper_reproduction_closure": True,
            "canonical_raw_response_submission_receipts": True,
            "frozen_response_root": True,
            "agreement_recomputes_response_bindings": True,
        },
        "surface": {
            "calibration_N": 56,
            "overlay_count": 38,
            "sentinel_count": 18,
            "coder_visible_artifacts": len(CODER_DISTRIBUTION_ALLOWED_ARTIFACTS),
            "agreement_minimum": AGREEMENT_MINIMUM,
            "mandatory_positive_classes": 2,
            "reproduction_anchors": 0,
            "frozen_contract_sha256": sha256_bytes(json_bytes(package["frozen_package_contract"])),
        },
        "remaining_before_distribution": [
            "FREEZE_EXACT_R2R1_REVIEW_PACKAGE_IN_LOCAL_COMMIT",
            "OBTAIN_ACCEPT_AGENTIC_CALIBRATION_R2R1_METHOD_CONTRACT_FOR_CODER_INTAKE",
        ],
    }


def load_package() -> dict[str, Any]:
    return {name: load_json(path) for name, path in ARTIFACT_PATHS.items()}


def build_review_manifest(report: dict[str, Any]) -> dict[str, Any]:
    paths = [
        OWNER_AUTHORIZATION,
        R2_REVIEW,
        WORKBENCH / "README.md",
        WORKBENCH / "codebook-v7.md",
        WORKBENCH / "stage1c-v2-precalibration-contract-r2r1-zh.md",
        REPO / "scripts/survey/sf_stage1c_v2_precalibration_r2r1.py",
        REPO / "scripts/survey/sf_stage1c_v2_calibration_agreement_v7.py",
        REPO / "scripts/survey/test_sf_stage1c_v2_precalibration_r2r1.py",
        *ARTIFACT_PATHS.values(),
        REPORT_PATH,
        VERIFICATION_PATH,
    ]
    missing = [path for path in paths if not path.is_file()]
    if missing:
        raise ContractError(f"R2R1 review inputs missing: {missing}")
    return {
        "schema": "sf-stage1c-v2-precalibration-review-manifest-v7",
        "artifact_id": "SF-STAGE1C-V2-PRECALIBRATION-REVIEW-PACKAGE-R2R1",
        "status": report["status"],
        "artifact_count": len(paths),
        "compiled_frozen_contract_sha256": report["surface"]["frozen_contract_sha256"],
        "artifacts": [
            {
                "path": path.relative_to(REPO).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256_path(path),
            }
            for path in paths
        ],
        "requested_review_verdict": (
            "ACCEPT_AGENTIC_CALIBRATION_R2R1_METHOD_CONTRACT_FOR_CODER_INTAKE_"
            "OR_WITHHOLD_WITH_BOUNDED_DEFECTS"
        ),
        "authority_withheld": [
            "CODER_DISTRIBUTION_BEFORE_ACCEPT",
            "AGREEMENT_BEFORE_TWO_RAW_OUTPUTS_FROZEN",
            "OWNER_ADJUDICATION",
            "SIGN_STAGE1C_V2_EXPERIMENT_MAPPING",
            "320_PAPER_FULL_MAPPING",
            "RESEARCH_EXECUTION",
            "STAGE2A",
            "PUSH",
        ],
    }


def run(*, write: bool) -> dict[str, Any]:
    expected = build_package()
    validate_package(expected)
    report = build_report(expected)
    if write:
        for name, path in ARTIFACT_PATHS.items():
            write_json(path, expected[name])
        write_json(REPORT_PATH, report)
        if VERIFICATION_PATH.is_file():
            write_json(REVIEW_MANIFEST_PATH, build_review_manifest(report))
    else:
        actual = load_package()
        validate_package(actual)
        for name in ARTIFACT_PATHS:
            if actual[name] != expected[name]:
                raise ContractError(f"materialized R2R1 artifact is stale: {ARTIFACT_PATHS[name]}")
        if load_json(REPORT_PATH) != report:
            raise ContractError("R2R1 contract report is stale")
        if load_json(REVIEW_MANIFEST_PATH) != build_review_manifest(report):
            raise ContractError("R2R1 review manifest is stale")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    try:
        report = run(write=args.write)
    except (ContractError, OSError, ValueError, ValidationError) as error:
        print(f"FAIL: {error}")
        return 1
    print(json.dumps({"status": report["status"], **report["surface"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
