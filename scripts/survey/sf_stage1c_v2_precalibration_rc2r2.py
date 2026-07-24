#!/usr/bin/env python3
"""Build and verify the immutable-successor Agentic RC2R2 contract.

RC2R2 closes only the frozen-provenance defects identified by the independent
RC2R1 review.  It does not rewrite RC2R1, distribute coders, compute agreement,
map papers, or execute research models, benchmarks, reproductions or prototypes.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator, ValidationError

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import sf_stage1c_v2_precalibration_rc2r1 as rc2r1
else:
    from scripts.survey import sf_stage1c_v2_precalibration_rc2r1 as rc2r1


REPO = Path(__file__).resolve().parents[2]
WORKBENCH = REPO / "wiki/survey/workbench/system-first-stage1c-v2-precalibration-rc2r2"
CHECK_DIR = REPO / "docs/checks/stage1c-v2-precalibration/2026-07-24-rc2r2"
REPORT_PATH = CHECK_DIR / "contract-report.json"
REVIEW_MANIFEST_PATH = WORKBENCH / "review-package-manifest-rc2r2.json"
OWNER_AUTHORIZATION = REPO / (
    "wiki/audit/system-first-stage1c-v2-precalibration/"
    "owner-rc2r2-provenance-repair-authorization/"
    "2026-07-24-owner-rc2r2-provenance-repair-authorization.md"
)
RC2R1_REVIEW = REPO / (
    "wiki/audit/system-first-stage1c-v2-precalibration/"
    "agentic-rc2r1-independent-method-review/"
    "2026-07-24-stage1c-v2-agentic-rc2r1-independent-method-review.md"
)
RC2R1_REVIEW_MANIFEST = (
    REPO / "wiki/survey/workbench/system-first-stage1c-v2-precalibration-rc2r1/"
    "review-package-manifest-rc2r1.json"
)

BASE_CALIBRATED_OBJECT_ARRAYS = rc2r1.BASE_CALIBRATED_OBJECT_ARRAYS
V4_EVIDENCE_ARRAYS = rc2r1.V3_EVIDENCE_ARRAYS

ARTIFACT_PATHS = {
    "response_schema": WORKBENCH / "calibration-response-schema-v4.json",
    "schema_bundle": WORKBENCH / "schema-bundle-v4.json",
    "source_manifest": WORKBENCH / "calibration-source-byte-manifest-v4.json",
    "acl_acquisition_receipts": WORKBENCH / "acl-acquisition-receipts-v2.json",
    "calibration_manifest": WORKBENCH / "calibration-manifest-v4.json",
    "blind_packet": WORKBENCH / "calibration-blind-packet-v4.json",
    "assignment_manifest": WORKBENCH / "calibration-assignment-manifest-v4.json",
    "claim_templates": WORKBENCH / "claim-template-registry-v4.json",
    "claim_template_coder_view": WORKBENCH / "claim-template-coder-view-v4.json",
    "coder_codebook": WORKBENCH / "coder-codebook-v4.json",
    "coder_prompt": WORKBENCH / "coder-prompt-v4.json",
    "agreement": WORKBENCH / "agreement-contract-v4.json",
    "agreement_intake_contract": WORKBENCH / "agreement-intake-contract-v4.json",
    "delivery_receipt_schema": WORKBENCH / "delivery-receipt-schema-v1.json",
    "delivery_receipt_template": WORKBENCH / "delivery-receipt-template-v1.json",
    "frozen_package_contract": WORKBENCH / "frozen-package-contract-v1.json",
    "coder_transaction": WORKBENCH / "coder-transaction-contract-v4.json",
    "reproduction_readiness": WORKBENCH / "reproduction-readiness-v4.json",
    "distribution_manifest": WORKBENCH / "calibration-distribution-manifest-v4.json",
}

CODER_DISTRIBUTION_ALLOWED_ARTIFACTS = rc2r1.CODER_DISTRIBUTION_ALLOWED_ARTIFACTS
CODER_DISTRIBUTION_FORBIDDEN_KEYS = rc2r1.CODER_DISTRIBUTION_FORBIDDEN_KEYS
CODER_VIEW_FORBIDDEN_NAMED_EXPECTATIONS = rc2r1.CODER_VIEW_FORBIDDEN_NAMED_EXPECTATIONS

RESPONSE_SCHEMA_ID = "sf-stage1c-v2-calibration-response-schema-v4"
RESPONSE_SCHEMA_CONST = "sf-stage1c-v2-calibration-response-v4"
SOURCE_MANIFEST_ID = "SF-STAGE1C-V2-CALIBRATION-SOURCE-BYTES-56-RC2R2"
CALIBRATION_MANIFEST_ID = "SF-STAGE1C-V2-CALIBRATION-PACKET-56-RC2R2"
DISTRIBUTION_MANIFEST_ID = "SF-STAGE1C-V2-CALIBRATION-DISTRIBUTION-RC2R2"
AGREEMENT_INTAKE_ID = "SF-STAGE1C-V2-AGREEMENT-INTAKE-RC2R2"
PROMPT_HASH_SEED = "RC2R2_NEUTRAL_CODER_PROMPT_V1"


class ContractError(RuntimeError):
    """Raised whenever RC2R2 cannot prove a fail-closed contract."""


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ContractError(f"expected JSON object: {path}")
    return value


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(json_bytes(value))


def build_response_schema() -> dict[str, Any]:
    schema = copy.deepcopy(rc2r1.build_response_schema())
    schema["$id"] = RESPONSE_SCHEMA_ID
    schema["properties"]["schema"] = {"const": RESPONSE_SCHEMA_CONST}
    return schema


def build_schema_bundle(response_schema: dict[str, Any]) -> dict[str, Any]:
    bundle = copy.deepcopy(rc2r1.build_schema_bundle(response_schema))
    bundle["$id"] = "sf-stage1c-v2-schema-bundle-v4"
    bundle["calibration_response_schema_id"] = response_schema["$id"]
    bundle["frozen_provenance_contract_required"] = True
    return bundle


def build_coder_prompt() -> dict[str, Any]:
    prompt = copy.deepcopy(rc2r1.build_coder_prompt())
    prompt.update({
        "schema": "sf-stage1c-v2-neutral-coder-prompt-v4",
        "artifact_id": "SF-STAGE1C-V2-NEUTRAL-CODER-PROMPT-RC2R2",
        "prompt_seed": PROMPT_HASH_SEED,
    })
    prompt["instructions"].append(
        "Retain the supplied paper and source bindings; never introduce a rendition not supplied for that paper."
    )
    return prompt


def build_agreement_contract() -> dict[str, Any]:
    agreement = copy.deepcopy(rc2r1.build_agreement_contract())
    agreement.update({
        "schema": "sf-stage1c-v2-agreement-contract-v4",
        "artifact_id": "SF-STAGE1C-V2-AGREEMENT-CONTRACT-RC2R2",
        "calibration_response_schema_id": RESPONSE_SCHEMA_ID,
        "agreement_intake_contract_id": AGREEMENT_INTAKE_ID,
        "exact_intake_rule": "COMPILED_ROOT_PLUS_EXACT_STATIC_N56_PLUS_HASHED_DELIVERY_RECEIPTS",
        "compiled_frozen_package_contract_required": True,
        "exact_response_schema_sha_required": True,
        "paper_scoped_frozen_rendition_validation_required": True,
        "actual_received_bundle_prompt_and_artifact_hashes_required": True,
    })
    return agreement


def coder_bundle_sha256(package: dict[str, Any], names: tuple[str, ...]) -> str:
    return rc2r1.coder_bundle_sha256(package, names)


# Identity values are exempt only at these complete JSON paths.  A field named
# ``title`` anywhere else remains subject to the named-expectation scan.
_IDENTITY_PATH_PATTERNS: dict[str, tuple[re.Pattern[str], ...]] = {
    "source_manifest": tuple(re.compile(pattern) for pattern in (
        r"^\$\.source_manifest\.items\[\d+\]\.(canonical_id|source_item_id|source_revision)$",
        r"^\$\.source_manifest\.items\[\d+\]\.primary_rendition\.(rendition_id|locator)$",
        r"^\$\.source_manifest\.items\[\d+\]\.alternate_renditions\[\d+\]\.(rendition_id|locator)$",
        r"^\$\.source_manifest\.items\[\d+\]\.ledger_binding\.(source_url|independent_receipt_id)$",
    )),
    "assignment_manifest": tuple(re.compile(pattern) for pattern in (
        r"^\$\.assignment_manifest\.items\[\d+\]\.(source_item_id|source_revision|packet_item_id)$",
    )),
    "blind_packet": tuple(re.compile(pattern) for pattern in (
        r"^\$\.blind_packet\.items\[\d+\]\.(canonical_id|source_item_id|source_revision|packet_item_id|title)$",
        r"^\$\.blind_packet\.items\[\d+\]\.blank_response\.(paper_id|packet_item_id|source_manifest_id)$",
    )),
}


def _identity_value_allowed(artifact: str, path: str) -> bool:
    return any(pattern.fullmatch(path) for pattern in _IDENTITY_PATH_PATTERNS.get(artifact, ()))


def _scan_value(value: Any, *, artifact: str, path: str) -> list[str]:
    leaks: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key in CODER_DISTRIBUTION_FORBIDDEN_KEYS:
                leaks.append(f"FORBIDDEN_KEY:{artifact}:{child_path}")
            leaks.extend(_scan_value(child, artifact=artifact, path=child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            leaks.extend(_scan_value(child, artifact=artifact, path=f"{path}[{index}]"))
    elif isinstance(value, str) and not _identity_value_allowed(artifact, path):
        folded = value.casefold()
        for forbidden in CODER_VIEW_FORBIDDEN_NAMED_EXPECTATIONS:
            if forbidden.casefold() in folded:
                leaks.append(f"FORBIDDEN_VALUE:{artifact}:{path}:{forbidden}")
    return leaks


def scan_coder_bundle_leaks(
    package: dict[str, Any], names: tuple[str, ...] | list[str],
) -> list[str]:
    names = tuple(names)
    leaks: list[str] = []
    if names != CODER_DISTRIBUTION_ALLOWED_ARTIFACTS:
        leaks.append(f"ARTIFACT_ALLOWLIST_MISMATCH:{names!r}")
    for name in names:
        if name not in package:
            leaks.append(f"MISSING_ARTIFACT:{name}")
            continue
        leaks.extend(_scan_value(package[name], artifact=name, path=f"$.{name}"))
    return sorted(set(leaks))


def build_distribution_manifest(package: dict[str, Any]) -> dict[str, Any]:
    names = CODER_DISTRIBUTION_ALLOWED_ARTIFACTS
    return {
        "schema": "sf-stage1c-v2-calibration-distribution-manifest-v4",
        "artifact_id": DISTRIBUTION_MANIFEST_ID,
        "status": "FROZEN_INPUT_BYTES_PREPARED_NOT_DISTRIBUTED",
        "scope": "CODER_VISIBLE_SHARED_CONTENT",
        "artifacts": [{
            "artifact_name": name,
            "path": ARTIFACT_PATHS[name].relative_to(REPO).as_posix(),
            "bytes": len(json_bytes(package[name])),
            "sha256": sha256_bytes(json_bytes(package[name])),
        } for name in names],
        "content_bundle_sha256": coder_bundle_sha256(package, names),
        "identity_binding_separate": True,
        "submission_receipt_binding_separate": True,
        "both_coders_must_receive_byte_identical_content": True,
        "recursive_key_and_value_leakage_scan_required": True,
        "exact_path_identity_allowlist_required": True,
        "coder_prompt_sha256": sha256_bytes(json_bytes(package["coder_prompt"])),
        "distribution_authorized": False,
        "post_accept_owner_authorization_recorded": True,
    }


def build_agreement_intake_contract(package: dict[str, Any]) -> dict[str, Any]:
    paper_ids = package["calibration_manifest"]["canonical_ids"]
    distribution = package["distribution_manifest"]
    return {
        "schema": "sf-stage1c-v2-agreement-intake-contract-v4",
        "artifact_id": AGREEMENT_INTAKE_ID,
        "status": "PREPARED_NOT_DISTRIBUTED",
        "calibration_manifest_id": CALIBRATION_MANIFEST_ID,
        "response_schema_id": RESPONSE_SCHEMA_ID,
        "source_manifest_id": SOURCE_MANIFEST_ID,
        "distribution_manifest_id": DISTRIBUTION_MANIFEST_ID,
        "delivery_receipt_schema_id": "sf-stage1c-v2-delivery-receipt-schema-v1",
        "content_bundle_sha256": distribution["content_bundle_sha256"],
        "prompt_hash": distribution["coder_prompt_sha256"],
        "N": 56,
        "canonical_paper_ids": paper_ids,
        "items": [{
            "paper_id": item["canonical_id"], "packet_item_id": item["packet_item_id"],
            "source_item_id": item["source_item_id"],
            "primary_rendition_sha256": item["primary_rendition_sha256"],
        } for item in package["blind_packet"]["items"]],
        "coder_slots": [{
            "coder_slot": slot,
            "planned_model": model,
            "model": None,
            "coder_id": None,
            "coder_transaction_id": None,
            "process_id": None,
            "assignment_status": "UNASSIGNED",
            "distribution_receipt_id": None,
            "submission_receipt_id": None,
            "delivery_receipt_id": None,
            "delivery_receipt_sha256": None,
            "received_content_bundle_sha256": None,
            "received_prompt_sha256": None,
            "expected_content_bundle_sha256": distribution["content_bundle_sha256"],
            "expected_prompt_hash": distribution["coder_prompt_sha256"],
        } for slot, model in (("A", "gpt-5.6-sol"), ("B", "gpt-5.6-terra"))],
        "completed_response_validator_required": True,
        "raw_outputs_frozen_before_agreement": True,
    }


def static_intake_projection(intake: dict[str, Any]) -> dict[str, Any]:
    """Return exactly the immutable portion of prepared or runtime intake."""
    fixed = (
        "schema", "artifact_id", "calibration_manifest_id", "response_schema_id",
        "source_manifest_id", "distribution_manifest_id", "delivery_receipt_schema_id",
        "content_bundle_sha256", "prompt_hash", "N", "canonical_paper_ids", "items",
        "completed_response_validator_required", "raw_outputs_frozen_before_agreement",
    )
    try:
        projection = {key: copy.deepcopy(intake[key]) for key in fixed}
        projection["coder_slots"] = [{
            "coder_slot": slot["coder_slot"],
            "planned_model": slot["planned_model"],
            "expected_content_bundle_sha256": slot["expected_content_bundle_sha256"],
            "expected_prompt_hash": slot["expected_prompt_hash"],
        } for slot in intake["coder_slots"]]
    except (KeyError, TypeError) as error:
        raise ContractError("agreement intake lacks frozen base intake fields") from error
    return projection


def _strict_object(required: list[str], properties: dict[str, Any]) -> dict[str, Any]:
    return {
        "type": "object", "additionalProperties": False,
        "required": required, "properties": properties,
    }


def build_delivery_receipt_schema() -> dict[str, Any]:
    text = {"type": "string", "minLength": 1}
    sha = {"type": "string", "pattern": "^[0-9a-f]{64}$"}
    artifact = _strict_object(
        ["artifact_name", "bytes", "sha256"],
        {"artifact_name": text, "bytes": {"type": "integer", "minimum": 1}, "sha256": sha},
    )
    properties = {
        "schema": {"const": "sf-stage1c-v2-delivery-receipt-v1"},
        "receipt_id": text, "coder_slot": {"enum": ["A", "B"]},
        "coder_id": text, "coder_transaction_id": text, "process_id": text,
        "model": {"enum": ["gpt-5.6-sol", "gpt-5.6-terra"]},
        "distribution_manifest_id": {"const": DISTRIBUTION_MANIFEST_ID},
        "received_content_bundle_sha256": sha, "received_prompt_sha256": sha,
        "received_artifacts": {"type": "array", "items": artifact, "minItems": 8, "maxItems": 8},
        "delivered_at": text, "submitted_at": text,
        "status": {"const": "FROZEN_SUBMITTED"}, "receipt_sha256": sha,
    }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "sf-stage1c-v2-delivery-receipt-schema-v1",
        **_strict_object(list(properties), properties),
    }


def _receipt_projection(receipt: dict[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(receipt)
    value.pop("receipt_sha256", None)
    return value


def build_delivery_receipt_template() -> dict[str, Any]:
    return {
        "schema": "sf-stage1c-v2-delivery-receipt-template-v1",
        "artifact_id": "SF-STAGE1C-V2-DELIVERY-RECEIPT-TEMPLATE-RC2R2",
        "status": "TEMPLATE_ONLY_NOT_A_RECEIPT",
        "delivery_receipt_schema_id": "sf-stage1c-v2-delivery-receipt-schema-v1",
        "runtime_required_fields": [
            "receipt_id", "coder_slot", "coder_id", "coder_transaction_id", "process_id",
            "model", "distribution_manifest_id", "received_content_bundle_sha256",
            "received_prompt_sha256", "received_artifacts", "delivered_at", "submitted_at",
            "status", "receipt_sha256",
        ],
        "receipt_digest_rule": "SHA256_OF_CANONICAL_PRETTY_JSON_WITHOUT_RECEIPT_SHA256",
    }


def _rendition_map(source_manifest: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {}
    for item in source_manifest["items"]:
        renditions = [item["primary_rendition"], *item.get("alternate_renditions", [])]
        result[item["canonical_id"]] = [{
            key: rendition[key] for key in ("rendition_id", "bytes", "sha256")
        } for rendition in renditions]
    return result


def build_frozen_package_contract(package: dict[str, Any]) -> dict[str, Any]:
    distribution = package["distribution_manifest"]
    intake = package["agreement_intake_contract"]
    return {
        "schema": "sf-stage1c-v2-frozen-package-contract-v1",
        "artifact_id": "SF-STAGE1C-V2-FROZEN-PACKAGE-CONTRACT-RC2R2",
        "status": "COMPILED_ROOT_OF_TRUST_INPUT",
        "calibration_manifest_id": CALIBRATION_MANIFEST_ID,
        "calibration_manifest_sha256": sha256_bytes(json_bytes(package["calibration_manifest"])),
        "source_manifest_id": SOURCE_MANIFEST_ID,
        "source_manifest_sha256": sha256_bytes(json_bytes(package["source_manifest"])),
        "distribution_manifest_id": DISTRIBUTION_MANIFEST_ID,
        "distribution_manifest_sha256": sha256_bytes(json_bytes(distribution)),
        "response_schema_id": RESPONSE_SCHEMA_ID,
        "response_schema_sha256": sha256_bytes(json_bytes(package["response_schema"])),
        "delivery_receipt_schema_id": package["delivery_receipt_schema"]["$id"],
        "delivery_receipt_schema_sha256": sha256_bytes(json_bytes(package["delivery_receipt_schema"])),
        "base_intake_static_sha256": sha256_bytes(json_bytes(static_intake_projection(intake))),
        "paper_rendition_map_sha256": sha256_bytes(json_bytes(_rendition_map(package["source_manifest"]))),
        "content_bundle_sha256": distribution["content_bundle_sha256"],
        "prompt_sha256": distribution["coder_prompt_sha256"],
        "N": 56,
        "canonical_paper_ids_sha256": sha256_bytes(json_bytes(intake["canonical_paper_ids"])),
        "compiled_into_agreement_engine": True,
    }


def build_package() -> dict[str, Any]:
    predecessor = copy.deepcopy(rc2r1.build_package())
    response_schema = build_response_schema()
    source = predecessor["source_manifest"]
    source.update({
        "schema": "sf-stage1c-v2-calibration-source-byte-manifest-v4",
        "artifact_id": SOURCE_MANIFEST_ID,
        "predecessor_source_manifest_id": rc2r1.SOURCE_MANIFEST_ID,
    })
    calibration = predecessor["calibration_manifest"]
    calibration.update({
        "schema": "sf-stage1c-v2-calibration-manifest-v4",
        "artifact_id": CALIBRATION_MANIFEST_ID,
        "status": "AGENTIC_RC2R2_CODER_READY_NOT_DISTRIBUTED",
        "source_byte_manifest_id": SOURCE_MANIFEST_ID,
        "calibration_response_schema_id": RESPONSE_SCHEMA_ID,
        "rc2r1_predecessor_immutable": True,
    })
    blind = predecessor["blind_packet"]
    blind.update({
        "schema": "sf-stage1c-v2-calibration-blind-packet-v4",
        "artifact_id": "SF-STAGE1C-V2-LABEL-HIDDEN-PACKET-56-RC2R2",
        "calibration_response_schema_id": RESPONSE_SCHEMA_ID,
        "source_byte_manifest_id": SOURCE_MANIFEST_ID,
    })
    for item in blind["items"]:
        response = item["blank_response"]
        response["schema"] = RESPONSE_SCHEMA_CONST
        response["source_manifest_id"] = SOURCE_MANIFEST_ID
    assignment = predecessor["assignment_manifest"]
    assignment.update({
        "schema": "sf-stage1c-v2-calibration-assignment-manifest-v4",
        "artifact_id": "SF-STAGE1C-V2-LABEL-HIDDEN-ASSIGNMENT-56-RC2R2",
    })
    claim_templates = predecessor["claim_templates"]
    claim_templates.update({
        "schema": "sf-stage1c-v2-claim-template-registry-v4",
        "artifact_id": "SF-STAGE1C-V2-CLAIM-TEMPLATES-13-RC2R2",
    })
    coder_view = predecessor["claim_template_coder_view"]
    coder_view.update({
        "schema": "sf-stage1c-v2-claim-template-coder-view-v4",
        "artifact_id": "SF-STAGE1C-V2-CLAIM-TEMPLATE-CODER-VIEW-13-RC2R2",
    })
    codebook = predecessor["coder_codebook"]
    codebook.update({
        "schema": "sf-stage1c-v2-coder-codebook-v4",
        "artifact_id": "SF-STAGE1C-V2-NEUTRAL-CODER-CODEBOOK-RC2R2",
        "calibration_response_schema_id": RESPONSE_SCHEMA_ID,
    })
    codebook["rules"].append(
        "Every locator rendition must be one of the frozen renditions supplied for the same paper."
    )
    receipts = predecessor["acl_acquisition_receipts"]
    receipts.update({
        "schema": "sf-stage1c-v2-acl-acquisition-receipts-v2",
        "artifact_id": "SF-STAGE1C-V2-ACL-ACQUISITION-RECEIPTS-RC2R2",
        "rc2r1_receipt_bytes_inherited_without_new_discovery": True,
    })
    readiness = predecessor["reproduction_readiness"]
    readiness.update({
        "schema": "sf-stage1c-v2-reproduction-readiness-v4",
        "artifact_id": "SF-STAGE1C-V2-REPRODUCTION-READINESS-RC2R2",
    })
    package: dict[str, Any] = {
        "response_schema": response_schema,
        "schema_bundle": build_schema_bundle(response_schema),
        "source_manifest": source,
        "acl_acquisition_receipts": receipts,
        "calibration_manifest": calibration,
        "blind_packet": blind,
        "assignment_manifest": assignment,
        "claim_templates": claim_templates,
        "claim_template_coder_view": coder_view,
        "coder_codebook": codebook,
        "coder_prompt": build_coder_prompt(),
        "agreement": build_agreement_contract(),
        "reproduction_readiness": readiness,
        "delivery_receipt_schema": build_delivery_receipt_schema(),
        "delivery_receipt_template": build_delivery_receipt_template(),
    }
    package["distribution_manifest"] = build_distribution_manifest(package)
    transaction = predecessor["coder_transaction"]
    transaction.update({
        "schema": "sf-stage1c-v2-coder-transaction-contract-v4",
        "artifact_id": "SF-STAGE1C-V2-CODER-INTAKE-RC2R2",
        "distribution_manifest_id": DISTRIBUTION_MANIFEST_ID,
        "calibration_response_schema_id": RESPONSE_SCHEMA_ID,
        "shared_content_bundle_sha256": package["distribution_manifest"]["content_bundle_sha256"],
        "delivery_receipt_schema_id": package["delivery_receipt_schema"]["$id"],
        "post_accept_owner_distribution_authorization_recorded": True,
    })
    for slot in transaction["coder_slots"]:
        slot["expected_content_bundle_sha256"] = package["distribution_manifest"]["content_bundle_sha256"]
        slot["expected_prompt_hash"] = package["distribution_manifest"]["coder_prompt_sha256"]
    package["coder_transaction"] = transaction
    package["agreement_intake_contract"] = build_agreement_intake_contract(package)
    package["frozen_package_contract"] = build_frozen_package_contract(package)
    return package


def validate_completed_response(
    response: dict[str, Any], schema: dict[str, Any], source_manifest: dict[str, Any],
) -> None:
    try:
        Draft202012Validator(schema).validate(response)
    except ValidationError as error:
        raise ContractError(f"response schema validation failed: {error.message}") from error
    if schema.get("$id") != RESPONSE_SCHEMA_ID:
        raise ContractError("completed response did not use the exact RC2R2 response schema")

    predecessor = copy.deepcopy(response)
    predecessor["schema"] = rc2r1.RESPONSE_SCHEMA_CONST
    predecessor["source_manifest_id"] = rc2r1.SOURCE_MANIFEST_ID
    try:
        rc2r1.validate_completed_response(predecessor, rc2r1.build_response_schema())
    except rc2r1.ContractError as error:
        raise ContractError(str(error)) from error

    allowed = {
        paper_id: {row["rendition_id"] for row in rows}
        for paper_id, rows in _rendition_map(source_manifest).items()
    }
    paper_id = response.get("paper_id")
    if paper_id not in allowed:
        raise ContractError("paper is absent from the frozen rendition map")
    for locator in response["source_locators"]:
        if locator["rendition_id"] not in allowed[paper_id]:
            raise ContractError("source locator uses a fake or cross-paper frozen rendition")


def build_delivery_receipt(
    package: dict[str, Any], *, slot: str, coder_id: str, transaction_id: str,
    process_id: str, model: str, delivered_at: str, submitted_at: str,
) -> dict[str, Any]:
    distribution = package["distribution_manifest"]
    receipt = {
        "schema": "sf-stage1c-v2-delivery-receipt-v1",
        "receipt_id": f"RC2R2-DELIVERY-{slot}-{transaction_id}",
        "coder_slot": slot, "coder_id": coder_id,
        "coder_transaction_id": transaction_id, "process_id": process_id, "model": model,
        "distribution_manifest_id": distribution["artifact_id"],
        "received_content_bundle_sha256": distribution["content_bundle_sha256"],
        "received_prompt_sha256": distribution["coder_prompt_sha256"],
        "received_artifacts": [{
            key: row[key] for key in ("artifact_name", "bytes", "sha256")
        } for row in distribution["artifacts"]],
        "delivered_at": delivered_at, "submitted_at": submitted_at,
        "status": "FROZEN_SUBMITTED",
    }
    receipt["receipt_sha256"] = sha256_bytes(json_bytes(_receipt_projection(receipt)))
    Draft202012Validator(package["delivery_receipt_schema"]).validate(receipt)
    return receipt


def bind_runtime_intake(
    package: dict[str, Any], bindings: Iterable[dict[str, str]], receipts: list[dict[str, Any]],
) -> dict[str, Any]:
    intake = copy.deepcopy(package["agreement_intake_contract"])
    binding_by_slot = {row["slot"]: row for row in bindings}
    receipt_by_slot = {row["coder_slot"]: row for row in receipts}
    if set(binding_by_slot) != {"A", "B"} or set(receipt_by_slot) != {"A", "B"}:
        raise ContractError("runtime intake requires exact A/B bindings and delivery receipts")
    intake["status"] = "BOUND_FOR_PRE_ADJUDICATION_AGREEMENT"
    for target in intake["coder_slots"]:
        slot = target["coder_slot"]
        binding = binding_by_slot[slot]
        receipt = receipt_by_slot[slot]
        target.update({
            "model": binding["model"], "coder_id": binding["coder_id"],
            "coder_transaction_id": binding["transaction_id"],
            "process_id": binding["process_id"], "assignment_status": "FROZEN_SUBMITTED",
            "distribution_receipt_id": receipt["receipt_id"],
            "submission_receipt_id": f"SUBMISSION-{receipt['receipt_id']}",
            "delivery_receipt_id": receipt["receipt_id"],
            "delivery_receipt_sha256": receipt["receipt_sha256"],
            "received_content_bundle_sha256": receipt["received_content_bundle_sha256"],
            "received_prompt_sha256": receipt["received_prompt_sha256"],
        })
    return intake


def verify_rc2r1_immutable() -> None:
    commit = "8d0a7c62a99cc93ff394881f20ad793e308f3342"
    manifest_rel = RC2R1_REVIEW_MANIFEST.relative_to(REPO).as_posix()
    try:
        manifest_raw = subprocess.check_output(
            ["git", "show", f"{commit}:{manifest_rel}"], cwd=REPO,
        )
        manifest = json.loads(manifest_raw.decode("utf-8"))
    except (subprocess.CalledProcessError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ContractError("cannot load the commit-bound RC2R1 review manifest") from error
    for row in manifest["artifacts"]:
        path = REPO / row["path"]
        try:
            blob = subprocess.check_output(
                ["git", "show", f"{commit}:{row['path']}"], cwd=REPO,
            )
        except subprocess.CalledProcessError as error:
            raise ContractError(f"missing commit-bound RC2R1 artifact: {row['path']}") from error
        if len(blob) != row["bytes"] or sha256_bytes(blob) != row["sha256"]:
            raise ContractError(f"commit-bound RC2R1 artifact differs: {row['path']}")
        if not path.is_file() or path.read_bytes() != blob:
            raise ContractError(f"committed RC2R1 review input changed: {row['path']}")


def validate_package(package: dict[str, Any]) -> None:
    verify_rc2r1_immutable()
    calibration = package["calibration_manifest"]
    if calibration["N"] != 56 or len(calibration["canonical_ids"]) != 56:
        raise ContractError("RC2R2 calibration set is not exact N=56")
    if len(set(calibration["canonical_ids"])) != 56:
        raise ContractError("RC2R2 calibration set contains duplicate canonical IDs")
    if package["source_manifest"]["N"] != 56 or not rc2r1.rc2.verify_source_manifest(package["source_manifest"]):
        raise ContractError("RC2R2 source bytes are not exact and locally verifiable")
    validator = Draft202012Validator(package["response_schema"])
    for item in package["blind_packet"]["items"]:
        validator.validate(item["blank_response"])
    distributed_names = tuple(
        row["artifact_name"] for row in package["distribution_manifest"]["artifacts"]
    )
    leaks = scan_coder_bundle_leaks(package, distributed_names)
    if leaks:
        raise ContractError(f"coder-visible leakage detected: {leaks}")
    distribution = package["distribution_manifest"]
    if distribution["distribution_authorized"]:
        raise ContractError("RC2R2 distributed coders before independent acceptance")
    if distribution["content_bundle_sha256"] != coder_bundle_sha256(package, distributed_names):
        raise ContractError("RC2R2 coder bundle hash is stale")
    for row in distribution["artifacts"]:
        raw = json_bytes(package[row["artifact_name"]])
        if row["bytes"] != len(raw) or row["sha256"] != sha256_bytes(raw):
            raise ContractError(f"RC2R2 distribution artifact is stale: {row['artifact_name']}")
    intake = package["agreement_intake_contract"]
    if intake["status"] != "PREPARED_NOT_DISTRIBUTED" or any(
        slot["assignment_status"] != "UNASSIGNED" for slot in intake["coder_slots"]
    ):
        raise ContractError("RC2R2 intake escaped the prepared-not-distributed gate")
    frozen = package["frozen_package_contract"]
    expected = build_frozen_package_contract(package)
    if frozen != expected:
        raise ContractError("RC2R2 frozen package contract is stale")
    if frozen["paper_rendition_map_sha256"] != sha256_bytes(json_bytes(_rendition_map(package["source_manifest"]))):
        raise ContractError("RC2R2 frozen rendition map is stale")
    readiness = package["reproduction_readiness"]
    if any(row["method_anchor_eligible"] or row["reproduction_eligible"] for row in readiness["candidates"]):
        raise ContractError("RC2R2 read-only closure promoted a reproduction anchor")
    if any(row["research_execution_performed"] for row in readiness["candidates"]):
        raise ContractError("research execution was recorded during RC2R2")


def build_report(package: dict[str, Any]) -> dict[str, Any]:
    validate_package(package)
    return {
        "schema": "sf-stage1c-v2-precalibration-contract-report-v4",
        "artifact_id": "SF-STAGE1C-V2-PRECALIBRATION-CONTRACT-REPORT-RC2R2",
        "as_of": "2026-07-24", "status": "AGENTIC_RC2R2_CODER_READY_NOT_DISTRIBUTED",
        "predecessor": {
            "release": "AGENTIC_RC2R1", "commit": "8d0a7c62a99cc93ff394881f20ad793e308f3342",
            "immutable_verified": True,
        },
        "authority": {
            "provenance_repair_authorized": True,
            "post_accept_calibration_distribution_authorized": True,
            "coder_distributed": False, "agreement_computed": False,
            "research_model_called": False, "benchmark_metric_run": False,
            "paper_reproduction_run": False, "prototype_created": False,
            "novelty_verdict_made": False, "full_mapping_signed": False,
            "push_authorized": False,
        },
        "bounded_defect_closure": {
            "compiled_frozen_package_root": True,
            "exact_static_n56_runtime_projection": True,
            "exact_response_schema_hash": True,
            "paper_scoped_frozen_renditions": True,
            "hashed_actual_delivery_receipts": True,
            "exact_path_leakage_exceptions": True,
        },
        "surface": {
            "calibration_N": 56,
            "coder_visible_artifacts": len(CODER_DISTRIBUTION_ALLOWED_ARTIFACTS),
            "frozen_contract_sha256": sha256_bytes(json_bytes(package["frozen_package_contract"])),
            "reproduction_anchors": 0,
        },
        "remaining_before_distribution": [
            "CREATE_LOCAL_COMMIT_WITHOUT_PUSH",
            "OBTAIN_ACCEPT_AGENTIC_RC2R2_METHOD_CONTRACT_FOR_CODER_INTAKE",
            "BIND_TWO_ISOLATED_CODER_TRANSACTIONS_AND_HASHED_DELIVERY_RECEIPTS",
        ],
    }


def build_review_manifest(report: dict[str, Any]) -> dict[str, Any]:
    paths = [
        OWNER_AUTHORIZATION, RC2R1_REVIEW, RC2R1_REVIEW_MANIFEST,
        WORKBENCH / "README.md", WORKBENCH / "codebook-v4.md",
        WORKBENCH / "stage1c-v2-precalibration-contract-rc2r2-zh.md",
        REPO / "scripts/survey/sf_stage1c_v2_precalibration_rc2r2.py",
        REPO / "scripts/survey/sf_stage1c_v2_calibration_agreement_v4.py",
        REPO / "scripts/survey/test_sf_stage1c_v2_precalibration_rc2r2.py",
        *ARTIFACT_PATHS.values(), REPORT_PATH, CHECK_DIR / "verification-summary.json",
    ]
    missing = [path for path in paths if not path.is_file()]
    if missing:
        raise ContractError(f"RC2R2 review inputs missing: {missing}")
    return {
        "schema": "sf-stage1c-v2-precalibration-review-manifest-v4",
        "artifact_id": "SF-STAGE1C-V2-PRECALIBRATION-REVIEW-PACKAGE-RC2R2",
        "status": report["status"], "artifact_count": len(paths),
        "predecessor_rc2r1_commit": "8d0a7c62a99cc93ff394881f20ad793e308f3342",
        "compiled_frozen_contract_sha256": report["surface"]["frozen_contract_sha256"],
        "artifacts": [{
            "path": path.relative_to(REPO).as_posix(),
            "bytes": path.stat().st_size, "sha256": sha256_path(path),
        } for path in paths],
        "requested_review_verdict": "ACCEPT_AGENTIC_RC2R2_METHOD_CONTRACT_FOR_CODER_INTAKE_OR_WITHHOLD_WITH_BOUNDED_DEFECTS",
        "authority_withheld": [
            "AGREEMENT_BEFORE_TWO_RAW_OUTPUTS_FROZEN", "HUMAN_ADJUDICATION",
            "SIGN_STAGE1C_V2_EXPERIMENT_MAPPING", "320_PAPER_FULL_MAPPING",
            "RESEARCH_EXECUTION", "SIGN_STAGE1C_V2_FAMILY_BRANCH_PORTFOLIO", "STAGE2A", "PUSH",
        ],
    }


def load_package() -> dict[str, Any]:
    return {name: load_json(path) for name, path in ARTIFACT_PATHS.items()}


def run(*, write: bool) -> dict[str, Any]:
    expected = build_package()
    validate_package(expected)
    report = build_report(expected)
    if write:
        for name, path in ARTIFACT_PATHS.items():
            write_json(path, expected[name])
        write_json(REPORT_PATH, report)
        write_json(REVIEW_MANIFEST_PATH, build_review_manifest(report))
    else:
        actual = load_package()
        validate_package(actual)
        for name in ARTIFACT_PATHS:
            if actual[name] != expected[name]:
                raise ContractError(f"materialized RC2R2 artifact is stale: {ARTIFACT_PATHS[name]}")
        if load_json(REPORT_PATH) != report:
            raise ContractError("RC2R2 contract report is stale")
        if load_json(REVIEW_MANIFEST_PATH) != build_review_manifest(report):
            raise ContractError("RC2R2 review manifest is stale")
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
