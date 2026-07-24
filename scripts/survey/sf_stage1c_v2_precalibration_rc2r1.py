#!/usr/bin/env python3
"""Build and verify the immutable-successor Agentic RC2R1 method contract.

RC2R1 repairs only the defects identified by the commit-bound RC2 review.  It
does not rewrite RC2, distribute coders, compute agreement, map 320 papers, or
execute any research model, benchmark, reproduction, or prototype.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, ValidationError

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import sf_stage1c_v2_precalibration_rc2 as rc2
else:
    from scripts.survey import sf_stage1c_v2_precalibration_rc2 as rc2


REPO = Path(__file__).resolve().parents[2]
WORKBENCH = REPO / "wiki/survey/workbench/system-first-stage1c-v2-precalibration-rc2r1"
CHECK_DIR = REPO / "docs/checks/stage1c-v2-precalibration/2026-07-24-rc2r1"
REPORT_PATH = CHECK_DIR / "contract-report.json"
REVIEW_MANIFEST_PATH = WORKBENCH / "review-package-manifest-rc2r1.json"
OWNER_AUTHORIZATION = REPO / (
    "wiki/audit/system-first-stage1c-v2-precalibration/"
    "owner-rc2r1-continuation-authorization/"
    "2026-07-24-owner-rc2r1-continuation-authorization.md"
)
RC2_REVIEW = REPO / (
    "wiki/audit/system-first-stage1c-v2-precalibration/"
    "agentic-rc2-independent-method-review/"
    "2026-07-24-stage1c-v2-agentic-rc2-independent-method-review.md"
)
RC2_REVIEW_MANIFEST = (
    REPO / "wiki/survey/workbench/system-first-stage1c-v2-precalibration/review-package-manifest-rc2.json"
)

BASE_CALIBRATED_OBJECT_ARRAYS = rc2.CALIBRATED_OBJECT_ARRAYS
V3_EVIDENCE_ARRAYS = ("protocol_transfer_evidence", "reproduction_evidence")

ARTIFACT_PATHS = {
    "response_schema": WORKBENCH / "calibration-response-schema-v3.json",
    "schema_bundle": WORKBENCH / "schema-bundle-v3.json",
    "source_manifest": WORKBENCH / "calibration-source-byte-manifest-v3.json",
    "acl_acquisition_receipts": WORKBENCH / "acl-acquisition-receipts-v1.json",
    "calibration_manifest": WORKBENCH / "calibration-manifest-v3.json",
    "blind_packet": WORKBENCH / "calibration-blind-packet-v3.json",
    "assignment_manifest": WORKBENCH / "calibration-assignment-manifest-v3.json",
    "claim_templates": WORKBENCH / "claim-template-registry-v3.json",
    "claim_template_coder_view": WORKBENCH / "claim-template-coder-view-v3.json",
    "coder_codebook": WORKBENCH / "coder-codebook-v3.json",
    "coder_prompt": WORKBENCH / "coder-prompt-v3.json",
    "agreement": WORKBENCH / "agreement-contract-v3.json",
    "agreement_intake_contract": WORKBENCH / "agreement-intake-contract-v3.json",
    "coder_transaction": WORKBENCH / "coder-transaction-contract-v3.json",
    "reproduction_readiness": WORKBENCH / "reproduction-readiness-v3.json",
    "distribution_manifest": WORKBENCH / "calibration-distribution-manifest-v3.json",
}

CODER_DISTRIBUTION_ALLOWED_ARTIFACTS = (
    "response_schema", "source_manifest", "assignment_manifest", "blind_packet",
    "coder_codebook", "claim_template_coder_view", "agreement", "coder_prompt",
)
CODER_DISTRIBUTION_FORBIDDEN_KEYS = rc2.CODER_DISTRIBUTION_FORBIDDEN_KEYS | frozenset({
    "prior_label", "expected_label", "named_expectation", "anchor_readiness",
    "paper_to_claim_links", "reproduction_role",
})
CODER_VIEW_FORBIDDEN_NAMED_EXPECTATIONS = rc2.CODER_VIEW_FORBIDDEN_NAMED_EXPECTATIONS

RESPONSE_SCHEMA_ID = "sf-stage1c-v2-calibration-response-schema-v3"
RESPONSE_SCHEMA_CONST = "sf-stage1c-v2-calibration-response-v3"
SOURCE_MANIFEST_ID = "SF-STAGE1C-V2-CALIBRATION-SOURCE-BYTES-56-RC2R1"
CALIBRATION_MANIFEST_ID = "SF-STAGE1C-V2-CALIBRATION-PACKET-56-RC2R1"
DISTRIBUTION_MANIFEST_ID = "SF-STAGE1C-V2-CALIBRATION-DISTRIBUTION-RC2R1"
AGREEMENT_INTAKE_ID = "SF-STAGE1C-V2-AGREEMENT-INTAKE-RC2R1"
PROMPT_HASH_SEED = "RC2R1_NEUTRAL_CODER_PROMPT_V1"


class ContractError(RuntimeError):
    """Raised whenever RC2R1 cannot prove a fail-closed contract."""


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


def _nonempty_array(item: dict[str, Any]) -> dict[str, Any]:
    return {"type": "array", "items": item, "minItems": 1, "uniqueItems": True}


def _text(pattern: str | None = None) -> dict[str, Any]:
    value: dict[str, Any] = {"type": "string", "minLength": 1}
    if pattern:
        value["pattern"] = pattern
    return value


def _strict_object(required: list[str], properties: dict[str, Any]) -> dict[str, Any]:
    return {
        "type": "object", "additionalProperties": False,
        "required": required, "properties": properties,
    }


def build_response_schema() -> dict[str, Any]:
    schema = copy.deepcopy(rc2.build_response_schema())
    schema["$id"] = RESPONSE_SCHEMA_ID
    schema["properties"]["schema"] = {"const": RESPONSE_SCHEMA_CONST}
    locator_ids = _nonempty_array(_text(r"^LOC-[A-Za-z0-9._:-]+$"))
    match_key = _text(r"^[A-Za-z0-9][A-Za-z0-9._:/+-]{2,159}$")

    transfer_properties = {
        "object_match_key": match_key,
        "transfer_evidence_id": _text(r"^TR-EVID-[A-Za-z0-9._:-]+$"),
        "source_domain": {"type": "string", "enum": [
            "VISION_MULTIMODAL_AGENT", "TEXT_AGENT", "OTHER_DOMAIN",
        ]},
        "source_protocol": _text(),
        "target_speech_omni_variables": _nonempty_array(_text()),
        "preserved_decision_structure": _text(),
        "source_locator_ids": locator_ids,
        "rejection_condition": _text(),
        "rejection_observable": _text(),
        "evidence_status": {"const": "COMPLETE"},
    }
    reproduction_properties = {
        "object_match_key": match_key,
        "reproduction_evidence_id": _text(r"^REPRO-EVID-[A-Za-z0-9._:-]+$"),
        "task": _text(), "dataset": _text(), "dataset_revision": _text(), "split": _text(),
        "official_repo": _text(r"^https://"), "pinned_revision": _text(), "entrypoint": _text(),
        "model_access": {"type": "string", "enum": [
            "TF_STRICT_BLACK_BOX", "TF_STRICT_GRAY_BOX", "INSTRUMENT_ONLY", "MIXED_OR_UNCLEAR",
        ]},
        "license_terms": _text(), "evaluator_or_ground_truth": _text(),
        "local_asset_state": {"type": "string", "enum": [
            "LOCAL_READY", "LOCAL_ADAPTABLE", "BLOCKED_ASSET_OR_TERMS",
        ]},
        "source_locator_ids": locator_ids,
        "closure_status": {"const": "CLOSED"},
        "blockers": {"type": "array", "items": _text(), "maxItems": 0},
    }
    schema["$defs"]["protocol_transfer_evidence"] = _strict_object(
        list(transfer_properties), transfer_properties,
    )
    schema["$defs"]["reproduction_evidence"] = _strict_object(
        list(reproduction_properties), reproduction_properties,
    )
    schema["properties"]["protocol_transfer_evidence"] = {
        "type": "array", "items": {"$ref": "#/$defs/protocol_transfer_evidence"},
        "uniqueItems": True,
    }
    schema["properties"]["reproduction_evidence"] = {
        "type": "array", "items": {"$ref": "#/$defs/reproduction_evidence"},
        "uniqueItems": True,
    }
    schema["required"].extend(V3_EVIDENCE_ARRAYS)
    return schema


def build_schema_bundle(response_schema: dict[str, Any]) -> dict[str, Any]:
    bundle = copy.deepcopy(rc2.build_schema_bundle(response_schema))
    bundle["$id"] = "sf-stage1c-v2-schema-bundle-v3"
    bundle["calibration_response_schema_id"] = response_schema["$id"]
    bundle["$defs"]["protocol_transfer_evidence"] = copy.deepcopy(
        response_schema["$defs"]["protocol_transfer_evidence"]
    )
    bundle["$defs"]["reproduction_evidence"] = copy.deepcopy(
        response_schema["$defs"]["reproduction_evidence"]
    )
    bundle["reference_borrow_reproduce_guards"] = {
        "REFERENCE": "NO_TRANSFER_OR_REPRODUCTION_EVIDENCE",
        "BORROW_PROTOCOL": "COMPLETE_SOURCE_TARGET_TRANSLATION_AND_REJECTION_EVIDENCE_REQUIRED",
        "REPRODUCTION_CANDIDATE": "TASK_DATA_REVISION_SPLIT_REPO_REVISION_ENTRYPOINT_ACCESS_LICENSE_EVALUATOR_AND_LOCAL_STATE_CLOSED",
    }
    return bundle


def build_acl_receipts(source_manifest: dict[str, Any]) -> dict[str, Any]:
    official = {
        "acl:2026.acl-long.1615": {
            "title": "S2S-Arena: Evaluating Paralinguistic Instruction Following in Speech-to-Speech Models",
            "official_record_url": "https://aclanthology.org/2026.acl-long.1615/",
            "official_pdf_url": "https://aclanthology.org/2026.acl-long.1615.pdf",
            "publication_revision": "ACL_ANTHOLOGY_PUBLICATION_VERSION:2026.acl-long.1615",
            "publisher": "Association for Computational Linguistics",
        },
        "acl:2026.findings-eacl.151": {
            "title": "Hearing Between the Lines: Unlocking the Reasoning Power of LLMs for Speech Evaluation",
            "official_record_url": "https://aclanthology.org/2026.findings-eacl.151/",
            "official_pdf_url": "https://aclanthology.org/2026.findings-eacl.151.pdf",
            "publication_revision": "ACL_ANTHOLOGY_PUBLICATION_VERSION:2026.findings-eacl.151",
            "publisher": "Association for Computational Linguistics",
        },
    }
    by_id = {row["canonical_id"]: row for row in source_manifest["items"]}
    receipts = []
    for index, canonical_id in enumerate(sorted(official), start=1):
        source = by_id[canonical_id]
        metadata = official[canonical_id]
        receipt = {
            "receipt_id": f"ACL-OFFICIAL-RECEIPT-{index:02d}-RC2R1",
            "canonical_id": canonical_id,
            **metadata,
            "verified_at": "2026-07-24T18:45:00+08:00",
            "verification_method": "OFFICIAL_ACL_ANTHOLOGY_RECORD_INSPECTED_AND_LOCAL_BYTES_REHASHED",
            "local_pdf_bytes": source["primary_rendition"]["bytes"],
            "local_pdf_sha256": source["primary_rendition"]["sha256"],
            "independent_of_fulltext_ledger": True,
        }
        receipts.append(receipt)
        source["ledger_binding"] = {
            "receipt_type": "RC2R1_ACL_OFFICIAL_ACQUISITION_RECEIPT",
            "source_url": metadata["official_pdf_url"],
            "receipt_basis": "OFFICIAL_PUBLICATION_RECORD_PLUS_EXACT_LOCAL_PDF_BYTES",
            "independent_receipt_id": receipt["receipt_id"],
            "verified_at": receipt["verified_at"],
        }
    return {
        "schema": "sf-stage1c-v2-acl-acquisition-receipts-v1",
        "artifact_id": "SF-STAGE1C-V2-ACL-ACQUISITION-RECEIPTS-RC2R1",
        "status": "TWO_KNOWN_ACL_SOURCES_OFFICIALLY_VERIFIED_NO_DISCOVERY",
        "N": len(receipts), "receipts": receipts,
    }


def build_coder_prompt() -> dict[str, Any]:
    return {
        "schema": "sf-stage1c-v2-neutral-coder-prompt-v3",
        "artifact_id": "SF-STAGE1C-V2-NEUTRAL-CODER-PROMPT-RC2R1",
        "status": "PREPARED_NOT_DISTRIBUTED",
        "prompt_seed": PROMPT_HASH_SEED,
        "instructions": [
            "Code every assigned source independently using only the shared source bytes and contract.",
            "Do not infer expected labels from paper identity, selection, prior discussion or project preference.",
            "Use exact source locators for every evidence-bearing object.",
            "Distinguish reference, protocol transfer and reproduction candidacy using their structured evidence contracts.",
            "Submit all 56 responses before any agreement or adjudication is revealed.",
        ],
        "network_discovery_allowed": False,
        "repository_access_allowed": False,
        "other_coder_output_allowed": False,
    }


def build_agreement_contract() -> dict[str, Any]:
    if __package__ in {None, ""}:
        from sf_stage1c_v2_calibration_agreement_v3 import CRITICAL_OBJECT_FIELDS
    else:
        from scripts.survey.sf_stage1c_v2_calibration_agreement_v3 import CRITICAL_OBJECT_FIELDS

    return {
        "schema": "sf-stage1c-v2-agreement-contract-v3",
        "artifact_id": "SF-STAGE1C-V2-AGREEMENT-CONTRACT-RC2R1",
        "calibration_response_schema_id": RESPONSE_SCHEMA_ID,
        "agreement_intake_contract_id": AGREEMENT_INTAKE_ID,
        "minimum_gate_value": 0.85,
        "exact_intake_rule": "EXACT_N56_CANONICAL_IDS_COMPLETED_SCHEMA_VALID_AND_PROVENANCE_BOUND",
        "paper_critical_fields": [
            *[f"paper_labels.{field}" for field in (
                "paper_disposition", "paper_role", "problem_nodes", "intervention_axes",
                "mm_level", "reference_borrow_reproduce", "access_regime",
                "empirical_experiment_present", "agentic_scope.scope_status",
                "agentic_scope.loop_components", "agentic_scope.core_dependency",
                "agentic_scope.capability_assets", "agentic_scope.control_role",
            )]
        ],
        "object_segmentation_gate_metric": "MICRO_F1_PER_OBJECT_TYPE",
        "critical_object_fields": {key: list(value) for key, value in CRITICAL_OBJECT_FIELDS.items()},
        "critical_object_field_gate_metric": "EXACT_RAW_AGREEMENT_PER_FIELD_PATH",
        "aggregate_matched_field_gate_prohibited": True,
        "zero_positive_category_status": "NOT_CALIBRATED",
        "not_calibrated_rule": "FAIL_OVERALL_AND_REQUIRE_TARGETED_CALIBRATION_OR_100_PERCENT_SECOND_REVIEW",
        "maximum_codebook_consolidations": 1,
        "second_round_failure_action": "STOP_AND_RETURN_TO_INDEPENDENT_REVIEW",
        "adjudication_after_raw_freeze_only": True,
    }


def coder_bundle_sha256(package: dict[str, Any], names: tuple[str, ...]) -> str:
    digest = hashlib.sha256()
    for name in names:
        raw = json_bytes(package[name])
        digest.update(name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(len(raw).to_bytes(8, "big"))
        digest.update(raw)
    return digest.hexdigest()


def _identity_value_allowed(artifact: str, path: str) -> bool:
    leaf = path.rsplit(".", 1)[-1]
    allowed_by_artifact = {
        "source_manifest": {
            "canonical_id", "source_item_id", "source_revision", "rendition_id", "locator",
            "source_url", "independent_receipt_id",
        },
        "assignment_manifest": {"source_item_id", "source_revision", "packet_item_id"},
        "blind_packet": {
            "canonical_id", "source_item_id", "source_revision", "paper_id", "packet_item_id",
            "source_manifest_id", "rendition_id", "title",
        },
    }
    return leaf in allowed_by_artifact.get(artifact, set())


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
        "schema": "sf-stage1c-v2-calibration-distribution-manifest-v3",
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
        "coder_prompt_sha256": sha256_bytes(json_bytes(package["coder_prompt"])),
        "distribution_authorized": False,
        "post_accept_owner_authorization_recorded": True,
    }


def build_agreement_intake_contract(package: dict[str, Any]) -> dict[str, Any]:
    paper_ids = package["calibration_manifest"]["canonical_ids"]
    prompt_hash = package["distribution_manifest"]["coder_prompt_sha256"]
    bundle_hash = package["distribution_manifest"]["content_bundle_sha256"]
    return {
        "schema": "sf-stage1c-v2-agreement-intake-contract-v3",
        "artifact_id": AGREEMENT_INTAKE_ID,
        "status": "PREPARED_NOT_DISTRIBUTED",
        "calibration_manifest_id": CALIBRATION_MANIFEST_ID,
        "response_schema_id": RESPONSE_SCHEMA_ID,
        "source_manifest_id": SOURCE_MANIFEST_ID,
        "distribution_manifest_id": DISTRIBUTION_MANIFEST_ID,
        "content_bundle_sha256": bundle_hash,
        "prompt_hash": prompt_hash,
        "N": 56,
        "canonical_paper_ids": paper_ids,
        "items": [{
            "paper_id": item["canonical_id"], "packet_item_id": item["packet_item_id"],
        } for item in package["blind_packet"]["items"]],
        "coder_slots": [{
            "coder_slot": slot,
            "planned_model": model,
            "model": None, "coder_id": None, "coder_transaction_id": None,
            "process_id": None, "assignment_status": "UNASSIGNED",
            "distribution_receipt_id": None, "submission_receipt_id": None,
            "expected_content_bundle_sha256": bundle_hash,
            "expected_prompt_hash": prompt_hash,
        } for slot, model in (("A", "gpt-5.6-sol"), ("B", "gpt-5.6-terra"))],
        "completed_response_validator_required": True,
        "raw_outputs_frozen_before_agreement": True,
    }


def build_package() -> dict[str, Any]:
    base = copy.deepcopy(rc2.build_package())
    response_schema = build_response_schema()
    source_manifest = base["source_manifest"]
    source_manifest.update({
        "schema": "sf-stage1c-v2-calibration-source-byte-manifest-v3",
        "artifact_id": SOURCE_MANIFEST_ID,
    })
    acl_receipts = build_acl_receipts(source_manifest)

    calibration = base["calibration_manifest"]
    calibration.update({
        "schema": "sf-stage1c-v2-calibration-manifest-v3",
        "artifact_id": CALIBRATION_MANIFEST_ID,
        "status": "AGENTIC_RC2R1_CODER_READY_NOT_DISTRIBUTED",
        "source_byte_manifest_id": SOURCE_MANIFEST_ID,
        "calibration_response_schema_id": RESPONSE_SCHEMA_ID,
        "rc2_predecessor_immutable": True,
    })
    blind = base["blind_packet"]
    blind.update({
        "schema": "sf-stage1c-v2-calibration-blind-packet-v3",
        "artifact_id": "SF-STAGE1C-V2-LABEL-HIDDEN-PACKET-56-RC2R1",
        "calibration_response_schema_id": RESPONSE_SCHEMA_ID,
        "source_byte_manifest_id": SOURCE_MANIFEST_ID,
    })
    for item in blind["items"]:
        response = item["blank_response"]
        response["schema"] = RESPONSE_SCHEMA_CONST
        response["source_manifest_id"] = SOURCE_MANIFEST_ID
        response["protocol_transfer_evidence"] = []
        response["reproduction_evidence"] = []

    assignment = base["assignment_manifest"]
    assignment.update({
        "schema": "sf-stage1c-v2-calibration-assignment-manifest-v3",
        "artifact_id": "SF-STAGE1C-V2-LABEL-HIDDEN-ASSIGNMENT-56-RC2R1",
    })
    claim_templates = base["claim_templates"]
    claim_templates.update({
        "schema": "sf-stage1c-v2-claim-template-registry-v3",
        "artifact_id": "SF-STAGE1C-V2-CLAIM-TEMPLATES-13-RC2R1",
    })
    coder_view = base["claim_template_coder_view"]
    coder_view.update({
        "schema": "sf-stage1c-v2-claim-template-coder-view-v3",
        "artifact_id": "SF-STAGE1C-V2-CLAIM-TEMPLATE-CODER-VIEW-13-RC2R1",
    })
    codebook = base["coder_codebook"]
    codebook.update({
        "schema": "sf-stage1c-v2-coder-codebook-v3",
        "artifact_id": "SF-STAGE1C-V2-NEUTRAL-CODER-CODEBOOK-RC2R1",
        "calibration_response_schema_id": RESPONSE_SCHEMA_ID,
    })
    codebook["rules"].extend([
        "BORROW_PROTOCOL requires structured source-to-target variables, preserved decision structure, source locators, and a rejection condition with observable evidence.",
        "REPRODUCTION_CANDIDATE requires one fully closed structured record for task, dataset revision and split, official repository revision, entrypoint, access, terms, evaluator, local state, and source locators.",
        "REFERENCE responses must not carry transfer or reproduction evidence objects.",
    ])
    readiness = base["reproduction_readiness"]
    readiness.update({
        "schema": "sf-stage1c-v2-reproduction-readiness-v3",
        "artifact_id": "SF-STAGE1C-V2-REPRODUCTION-READINESS-RC2R1",
    })
    package = {
        "response_schema": response_schema,
        "schema_bundle": build_schema_bundle(response_schema),
        "source_manifest": source_manifest,
        "acl_acquisition_receipts": acl_receipts,
        "calibration_manifest": calibration,
        "blind_packet": blind,
        "assignment_manifest": assignment,
        "claim_templates": claim_templates,
        "claim_template_coder_view": coder_view,
        "coder_codebook": codebook,
        "coder_prompt": build_coder_prompt(),
        "agreement": build_agreement_contract(),
        "reproduction_readiness": readiness,
    }
    package["distribution_manifest"] = build_distribution_manifest(package)
    transaction = base["coder_transaction"]
    transaction.update({
        "schema": "sf-stage1c-v2-coder-transaction-contract-v3",
        "artifact_id": "SF-STAGE1C-V2-CODER-INTAKE-RC2R1",
        "distribution_manifest_id": DISTRIBUTION_MANIFEST_ID,
        "calibration_response_schema_id": RESPONSE_SCHEMA_ID,
        "shared_content_bundle_sha256": package["distribution_manifest"]["content_bundle_sha256"],
        "post_accept_owner_distribution_authorization_recorded": True,
    })
    for slot in transaction["coder_slots"]:
        slot["expected_content_bundle_sha256"] = package["distribution_manifest"]["content_bundle_sha256"]
        slot["expected_prompt_hash"] = package["distribution_manifest"]["coder_prompt_sha256"]
    package["coder_transaction"] = transaction
    package["agreement_intake_contract"] = build_agreement_intake_contract(package)
    return package


def _contains_not_coded(value: Any) -> bool:
    if value == "NOT_CODED":
        return True
    if isinstance(value, list):
        return any(_contains_not_coded(child) for child in value)
    if isinstance(value, dict):
        return any(_contains_not_coded(child) for child in value.values())
    return False


def validate_completed_response(response: dict[str, Any], schema: dict[str, Any]) -> None:
    try:
        Draft202012Validator(schema).validate(response)
    except ValidationError as error:
        raise ContractError(f"response schema validation failed: {error.message}") from error
    if response.get("response_status") != "CODER_SUBMITTED":
        raise ContractError("completed response must be CODER_SUBMITTED")
    if _contains_not_coded(response.get("paper_labels")):
        raise ContractError("completed response retains NOT_CODED paper labels")

    base = copy.deepcopy(response)
    base.pop("protocol_transfer_evidence")
    base.pop("reproduction_evidence")
    base["schema"] = "sf-stage1c-v2-calibration-response-v2"
    try:
        rc2.validate_completed_response(base, rc2.build_response_schema())
    except rc2.ContractError as error:
        raise ContractError(str(error)) from error

    locator_ids = {row["locator_id"] for row in response["source_locators"]}
    for array_name in V3_EVIDENCE_ARRAYS:
        for evidence in response[array_name]:
            if not set(evidence["source_locator_ids"]).issubset(locator_ids):
                raise ContractError(f"{array_name} references an undeclared source locator")

    label = response["paper_labels"]["reference_borrow_reproduce"]
    transfers = response["protocol_transfer_evidence"]
    reproductions = response["reproduction_evidence"]
    if label == "BORROW_PROTOCOL":
        if not transfers or reproductions:
            raise ContractError("BORROW_PROTOCOL requires complete transfer evidence only")
    elif label == "REPRODUCTION_CANDIDATE":
        if not reproductions or transfers:
            raise ContractError("REPRODUCTION_CANDIDATE requires one or more fully closed records only")
        if any(row["closure_status"] != "CLOSED" or row["blockers"] for row in reproductions):
            raise ContractError("REPRODUCTION_CANDIDATE contains an unclosed prerequisite")
    elif transfers or reproductions:
        raise ContractError("REFERENCE/NOT_APPLICABLE cannot carry implicit transfer or reproduction evidence")


def verify_rc2_immutable() -> None:
    manifest = load_json(RC2_REVIEW_MANIFEST)
    for row in manifest["artifacts"]:
        path = REPO / row["path"]
        if not path.is_file() or path.stat().st_size != row["bytes"] or sha256_path(path) != row["sha256"]:
            raise ContractError(f"committed RC2 review input changed: {row['path']}")


def validate_package(package: dict[str, Any]) -> None:
    verify_rc2_immutable()
    calibration = package["calibration_manifest"]
    if calibration["N"] != 56 or len(calibration["canonical_ids"]) != 56:
        raise ContractError("RC2R1 calibration set is not exact N=56")
    if len(set(calibration["canonical_ids"])) != 56:
        raise ContractError("RC2R1 calibration set contains duplicate canonical IDs")
    if package["source_manifest"]["N"] != 56 or not rc2.verify_source_manifest(package["source_manifest"]):
        raise ContractError("RC2R1 source bytes are not exact and locally verifiable")
    if package["acl_acquisition_receipts"]["N"] != 2:
        raise ContractError("RC2R1 must contain exactly two ACL official receipts")
    source_by_id = {row["canonical_id"]: row for row in package["source_manifest"]["items"]}
    for receipt in package["acl_acquisition_receipts"]["receipts"]:
        source = source_by_id[receipt["canonical_id"]]
        if (
            receipt["local_pdf_sha256"] != source["primary_rendition"]["sha256"]
            or receipt["local_pdf_bytes"] != source["primary_rendition"]["bytes"]
            or source["ledger_binding"].get("independent_receipt_id") != receipt["receipt_id"]
        ):
            raise ContractError("ACL acquisition receipt is not bound to exact local bytes")
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
        raise ContractError("RC2R1 distributed coders before independent acceptance")
    if distribution["content_bundle_sha256"] != coder_bundle_sha256(package, distributed_names):
        raise ContractError("RC2R1 coder bundle hash is stale")
    for row in distribution["artifacts"]:
        raw = json_bytes(package[row["artifact_name"]])
        if row["bytes"] != len(raw) or row["sha256"] != sha256_bytes(raw):
            raise ContractError(f"RC2R1 distribution artifact is stale: {row['artifact_name']}")
    intake = package["agreement_intake_contract"]
    if (
        intake["status"] != "PREPARED_NOT_DISTRIBUTED"
        or intake["N"] != 56
        or set(intake["canonical_paper_ids"]) != set(calibration["canonical_ids"])
        or any(slot["assignment_status"] != "UNASSIGNED" for slot in intake["coder_slots"])
    ):
        raise ContractError("agreement intake escaped its prepared-not-distributed gate")
    transaction = package["coder_transaction"]
    if transaction["distribution_authorized"] or any(
        slot["assignment_status"] != "UNASSIGNED" for slot in transaction["coder_slots"]
    ):
        raise ContractError("coder transaction escaped its unassigned gate")
    readiness = package["reproduction_readiness"]
    if any(row["method_anchor_eligible"] or row["reproduction_eligible"] for row in readiness["candidates"]):
        raise ContractError("RC2R1 read-only closure promoted a reproduction anchor")
    by_id = {row["canonical_work_id"]: row for row in readiness["candidates"]}
    if by_id["CW-ARXIV-2510.07838"]["status"] != "REFERENCE_ONLY":
        raise ContractError("specialized Duplex boundary escaped exclusion")
    if any(row["research_execution_performed"] for row in readiness["candidates"]):
        raise ContractError("research execution was recorded during RC2R1")


def build_report(package: dict[str, Any]) -> dict[str, Any]:
    validate_package(package)
    return {
        "schema": "sf-stage1c-v2-precalibration-contract-report-v3",
        "artifact_id": "SF-STAGE1C-V2-PRECALIBRATION-CONTRACT-REPORT-RC2R1",
        "as_of": "2026-07-24",
        "status": "AGENTIC_RC2R1_CODER_READY_NOT_DISTRIBUTED",
        "predecessor": {
            "release": "AGENTIC_RC2", "commit": "74cf8e4b565a9e53ff40f9dbc34961ede853dd57",
            "immutable_verified": True,
        },
        "authority": {
            "bounded_repair_authorized": True,
            "post_accept_calibration_distribution_authorized": True,
            "coder_distributed": False, "agreement_computed": False,
            "research_model_called": False, "benchmark_metric_run": False,
            "paper_reproduction_run": False, "prototype_created": False,
            "novelty_verdict_made": False, "full_mapping_signed": False,
            "push_authorized": False,
        },
        "bounded_defect_closure": {
            "exact_n56_completed_provenance_bound_intake": True,
            "per_critical_object_field_gates": True,
            "borrow_protocol_semantic_guard": True,
            "reproduction_candidate_semantic_guard": True,
            "two_acl_official_receipts": True,
            "all_coder_metadata_key_and_value_leakage_scanned": True,
        },
        "surface": {
            "calibration_N": 56,
            "acl_receipts": package["acl_acquisition_receipts"]["N"],
            "coder_visible_artifacts": len(CODER_DISTRIBUTION_ALLOWED_ARTIFACTS),
            "reproduction_anchors": 0,
        },
        "remaining_before_distribution": [
            "CREATE_LOCAL_COMMIT_WITHOUT_PUSH",
            "OBTAIN_ACCEPT_AGENTIC_RC2R1_METHOD_CONTRACT_FOR_CODER_INTAKE",
            "BIND_TWO_ISOLATED_CODER_TRANSACTIONS_AND_OWNER_ADJUDICATOR",
        ],
    }


def build_review_manifest(report: dict[str, Any]) -> dict[str, Any]:
    paths = [
        OWNER_AUTHORIZATION, RC2_REVIEW, RC2_REVIEW_MANIFEST,
        WORKBENCH / "README.md", WORKBENCH / "codebook-v3.md",
        WORKBENCH / "stage1c-v2-precalibration-contract-rc2r1-zh.md",
        REPO / "scripts/survey/sf_stage1c_v2_precalibration_rc2r1.py",
        REPO / "scripts/survey/sf_stage1c_v2_calibration_agreement_v3.py",
        REPO / "scripts/survey/test_sf_stage1c_v2_precalibration_rc2r1.py",
        *ARTIFACT_PATHS.values(), REPORT_PATH,
    ]
    missing = [path for path in paths if not path.is_file()]
    if missing:
        raise ContractError(f"RC2R1 review inputs missing: {missing}")
    return {
        "schema": "sf-stage1c-v2-precalibration-review-manifest-v3",
        "artifact_id": "SF-STAGE1C-V2-PRECALIBRATION-REVIEW-PACKAGE-RC2R1",
        "status": report["status"], "artifact_count": len(paths),
        "predecessor_rc2_commit": "74cf8e4b565a9e53ff40f9dbc34961ede853dd57",
        "artifacts": [{
            "path": path.relative_to(REPO).as_posix(),
            "bytes": path.stat().st_size, "sha256": sha256_path(path),
        } for path in paths],
        "requested_review_verdict": "ACCEPT_AGENTIC_RC2R1_METHOD_CONTRACT_FOR_CODER_INTAKE_OR_WITHHOLD_WITH_BOUNDED_DEFECTS",
        "authority_withheld": [
            "AGREEMENT_BEFORE_TWO_RAW_OUTPUTS_FROZEN", "HUMAN_ADJUDICATION",
            "SIGN_STAGE1C_V2_EXPERIMENT_MAPPING", "320_PAPER_FULL_MAPPING",
            "RESEARCH_EXECUTION", "SIGN_STAGE1C_V2_FAMILY_BRANCH_PORTFOLIO", "STAGE2A",
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
                raise ContractError(f"materialized RC2R1 artifact is stale: {ARTIFACT_PATHS[name]}")
        if load_json(REPORT_PATH) != report:
            raise ContractError("RC2R1 contract report is stale")
        if load_json(REVIEW_MANIFEST_PATH) != build_review_manifest(report):
            raise ContractError("RC2R1 review manifest is stale")
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
