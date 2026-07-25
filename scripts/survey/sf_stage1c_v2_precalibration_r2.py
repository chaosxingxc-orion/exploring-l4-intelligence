#!/usr/bin/env python3
"""Build the bounded Agentic calibration R2 consolidation contract.

R2 is the single authorized successor to the failed R1 calibration.  It keeps
the exact N=56 source packet, removes coder-authored agreement identities,
splits paper-visible reproduction support from reviewer-only local readiness,
and proves mandatory positive support before any new coder distribution.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator, ValidationError

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import sf_stage1c_v2_precalibration_rc2r3 as rc2r3
    import sf_stage1c_v2_r2_guards as r2_guards
else:
    from scripts.survey import sf_stage1c_v2_precalibration_rc2r3 as rc2r3
    from scripts.survey import sf_stage1c_v2_r2_guards as r2_guards


REPO = Path(__file__).resolve().parents[2]
WORKBENCH = REPO / "wiki/survey/workbench/system-first-stage1c-v2-precalibration-r2"
CHECK_DIR = REPO / "docs/checks/stage1c-v2-precalibration/2026-07-25-r2"
REPORT_PATH = CHECK_DIR / "contract-report.json"
VERIFICATION_PATH = CHECK_DIR / "verification-summary.json"
REVIEW_MANIFEST_PATH = WORKBENCH / "review-package-manifest-r2.json"

OWNER_AUTHORIZATION = REPO / (
    "wiki/audit/system-first-stage1c-v2-calibration/"
    "round-04-owner-codebook-consolidation-authorization/"
    "2026-07-25-stage1c-v2-agentic-calibration-r1-codebook-consolidation-authorization.md"
)
R1_PRE_ADJUDICATION = REPO / (
    "wiki/audit/system-first-stage1c-v2-calibration/round-02-pre-adjudication/"
    "2026-07-25-stage1c-v2-agentic-calibration-r1-pre-adjudication.md"
)
R1_POSITIVE_PREFLIGHT = REPO / (
    "wiki/audit/system-first-stage1c-v2-calibration/round-03-positive-support-preflight/"
    "2026-07-25-stage1c-v2-agentic-calibration-r1-positive-support-preflight.md"
)
RC2R3_REVIEW = REPO / (
    "wiki/audit/system-first-stage1c-v2-precalibration/"
    "agentic-rc2r3-independent-method-review/"
    "2026-07-24-stage1c-v2-agentic-rc2r3-independent-method-review.md"
)

RESPONSE_SCHEMA_ID = "sf-stage1c-v2-calibration-response-schema-v5"
RESPONSE_SCHEMA_CONST = "sf-stage1c-v2-calibration-response-v5"
CALIBRATION_MANIFEST_ID = "SF-STAGE1C-V2-CALIBRATION-PACKET-56-R2"
DISTRIBUTION_MANIFEST_ID = "SF-STAGE1C-V2-CALIBRATION-DISTRIBUTION-R2"
AGREEMENT_INTAKE_ID = "SF-STAGE1C-V2-AGREEMENT-INTAKE-R2"
DELIVERY_RECEIPT_SCHEMA_ID = "sf-stage1c-v2-delivery-receipt-schema-v3"
AGREEMENT_MINIMUM = 0.85

BASE_OBJECT_ARRAYS = rc2r3.BASE_CALIBRATED_OBJECT_ARRAYS
OBJECT_ARRAYS = (*BASE_OBJECT_ARRAYS, "protocol_transfer_evidence", "paper_reproduction_support")
OBJECT_DEFINITION_BY_ARRAY = {
    "run_cells": "run_cell",
    "observations": "observation",
    "paired_comparisons": "paired_comparison",
    "dataset_nodes": "dataset_node",
    "dataset_edges": "dataset_edge",
    "claim_decisions": "claim_decision",
    "translation_or_compatibility_decisions": "compatibility_decision",
    "protocol_transfer_evidence": "protocol_transfer_evidence",
    "paper_reproduction_support": "paper_reproduction_support",
}

CODER_DISTRIBUTION_ALLOWED_ARTIFACTS = rc2r3.CODER_DISTRIBUTION_ALLOWED_ARTIFACTS
CODER_DISTRIBUTION_FORBIDDEN_KEYS = rc2r3.CODER_DISTRIBUTION_FORBIDDEN_KEYS
CODER_VIEW_FORBIDDEN_NAMED_EXPECTATIONS = rc2r3.CODER_VIEW_FORBIDDEN_NAMED_EXPECTATIONS

ARTIFACT_PATHS = {
    "response_schema": WORKBENCH / "calibration-response-schema-v5.json",
    "schema_bundle": WORKBENCH / "schema-bundle-v5.json",
    "source_manifest": WORKBENCH / "calibration-source-byte-manifest-v4-inherited.json",
    "acl_acquisition_receipts": WORKBENCH / "acl-acquisition-receipts-v2-inherited.json",
    "calibration_manifest": WORKBENCH / "calibration-manifest-v6.json",
    "blind_packet": WORKBENCH / "calibration-blind-packet-v5.json",
    "assignment_manifest": WORKBENCH / "calibration-assignment-manifest-v4-inherited.json",
    "claim_templates": WORKBENCH / "claim-template-registry-v4-inherited.json",
    "claim_template_coder_view": WORKBENCH / "claim-template-coder-view-v4-inherited.json",
    "coder_codebook": WORKBENCH / "coder-codebook-v5.json",
    "coder_prompt": WORKBENCH / "coder-prompt-v5.json",
    "agreement": WORKBENCH / "agreement-contract-v6.json",
    "agreement_intake_contract": WORKBENCH / "agreement-intake-contract-v6.json",
    "delivery_receipt_schema": WORKBENCH / "delivery-receipt-schema-v3.json",
    "delivery_receipt_template": WORKBENCH / "delivery-receipt-template-v3.json",
    "frozen_package_contract": WORKBENCH / "frozen-package-contract-v3.json",
    "coder_transaction": WORKBENCH / "coder-transaction-contract-v6.json",
    "local_reproduction_readiness": WORKBENCH / "local-reproduction-readiness-v1.json",
    "distribution_manifest": WORKBENCH / "calibration-distribution-manifest-v6.json",
    "positive_support_ledger": WORKBENCH / "positive-support-ledger-r2.json",
    "positive_support_preflight": WORKBENCH / "positive-support-preflight-r2.json",
}


class ContractError(RuntimeError):
    """Raised when the R2 method contract cannot prove a fail-closed gate."""


json_bytes = rc2r3.json_bytes
sha256_bytes = rc2r3.sha256_bytes
sha256_path = rc2r3.sha256_path
load_json = rc2r3.load_json
write_json = rc2r3.write_json
scan_coder_bundle_leaks = rc2r3.scan_coder_bundle_leaks
coder_bundle_sha256_from_raw = rc2r3.coder_bundle_sha256_from_raw


def _text(pattern: str | None = None) -> dict[str, Any]:
    value: dict[str, Any] = {"type": "string", "minLength": 1}
    if pattern:
        value["pattern"] = pattern
    return value


def _array(item: dict[str, Any], *, min_items: int | None = None) -> dict[str, Any]:
    value: dict[str, Any] = {"type": "array", "items": item, "uniqueItems": True}
    if min_items is not None:
        value["minItems"] = min_items
    return value


def _strict_object(required: list[str], properties: dict[str, Any]) -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": required,
        "properties": properties,
    }


def build_response_schema() -> dict[str, Any]:
    schema = copy.deepcopy(rc2r3.build_package()["response_schema"])
    schema["$id"] = RESPONSE_SCHEMA_ID
    schema["properties"]["schema"] = {"const": RESPONSE_SCHEMA_CONST}

    for definition_name in OBJECT_DEFINITION_BY_ARRAY.values():
        if definition_name == "paper_reproduction_support":
            continue
        definition = schema["$defs"][definition_name]
        definition["properties"].pop("object_match_key", None)
        definition["required"] = [
            field for field in definition["required"] if field != "object_match_key"
        ]

    previous = schema["$defs"].pop("reproduction_evidence")
    previous_properties = previous["properties"]
    support_properties = {
        "reproduction_support_id": _text(r"^PRS-[A-Za-z0-9._:-]+$"),
        "task": copy.deepcopy(previous_properties["task"]),
        "dataset": copy.deepcopy(previous_properties["dataset"]),
        "dataset_revision": copy.deepcopy(previous_properties["dataset_revision"]),
        "split": copy.deepcopy(previous_properties["split"]),
        "official_repo": copy.deepcopy(previous_properties["official_repo"]),
        "pinned_revision": copy.deepcopy(previous_properties["pinned_revision"]),
        "entrypoint": copy.deepcopy(previous_properties["entrypoint"]),
        "model_access": copy.deepcopy(previous_properties["model_access"]),
        "license_terms": copy.deepcopy(previous_properties["license_terms"]),
        "evaluator_or_ground_truth": copy.deepcopy(previous_properties["evaluator_or_ground_truth"]),
        "source_locator_ids": copy.deepcopy(previous_properties["source_locator_ids"]),
        "closure_status": {
            "type": "string",
            "enum": ["CLOSED_PAPER_SUPPORT", "OPEN_WITH_BLOCKERS"],
        },
        "blockers": _array(_text()),
    }
    schema["$defs"]["paper_reproduction_support"] = _strict_object(
        list(support_properties), support_properties
    )
    schema["properties"].pop("reproduction_evidence")
    schema["properties"]["paper_reproduction_support"] = {
        "type": "array",
        "items": {"$ref": "#/$defs/paper_reproduction_support"},
        "uniqueItems": True,
    }
    schema["required"] = [
        "paper_reproduction_support" if field == "reproduction_evidence" else field
        for field in schema["required"]
    ]

    absence = schema["properties"]["object_absence_reasons"]
    absence_values = {
        "type": "string",
        "enum": [
            "OBJECTS_PRESENT",
            "NONE_REPORTED",
            "NOT_APPLICABLE_NON_EMPIRICAL",
            "WITHHELD_INSUFFICIENT_SOURCE",
            "NOT_CODED",
        ],
    }
    absence["required"] = list(OBJECT_ARRAYS)
    absence["properties"] = {
        name: copy.deepcopy(absence_values) for name in OBJECT_ARRAYS
    }
    schema["properties"]["paired_comparison_absence_reason"] = {
        "type": "string",
        "enum": [
            "OBJECTS_PRESENT",
            "NO_BASELINE_INTERVENTION_PAIR",
            "NO_CLOSED_COMPARABILITY_KEY",
            "NOT_APPLICABLE_NON_EMPIRICAL",
            "WITHHELD_INSUFFICIENT_SOURCE",
            "NOT_CODED",
        ],
    }
    if "paired_comparison_absence_reason" not in schema["required"]:
        schema["required"].append("paired_comparison_absence_reason")
    return schema


def _decision_row(when: str, code: str, counterexample: str) -> dict[str, str]:
    return {"when": when, "code": code, "counterexample": counterexample}


def build_coder_codebook() -> dict[str, Any]:
    base = copy.deepcopy(rc2r3.build_package()["coder_codebook"])
    base.update({
        "schema": "sf-stage1c-v2-coder-codebook-v5",
        "artifact_id": "SF-STAGE1C-V2-NEUTRAL-CODER-CODEBOOK-R2",
        "calibration_response_schema_id": RESPONSE_SCHEMA_ID,
        "status": "CONSOLIDATED_DEIDENTIFIED_RULES_PREPARED_NOT_DISTRIBUTED",
    })
    base["rules"] = [
        "Code every material object supported by the supplied source; one-object-per-paper shortcuts are prohibited.",
        "Coders provide semantic fields and source locators but never object agreement keys; the compiler derives source anchors and segmentation signatures.",
        "A changed dataset revision/split, model/access, input condition, intervention, or budget creates a new run cell; multiple metrics remain observations of one run.",
        "An empirical extractable paper requires material run cells, observations and dataset nodes.",
        "A paired comparison is required when baseline, intervention and comparability close; otherwise select the typed absence reason.",
        "A source-backed dataset lineage or relation creates an edge; semantic similarity alone is not lineage.",
        "REFERENCE transfers neither protocol nor result; BORROW_PROTOCOL requires explicit translation and rejection evidence.",
        "Paper-visible reproduction support may be OPEN_WITH_BLOCKERS. REPRODUCTION_CANDIDATE requires CLOSED_PAPER_SUPPORT; local anchor readiness is reviewer-only.",
        "Use precise page/section/table/row locators for objects; title-only or abstract-only locators do not support empirical objects.",
        "Specialized Duplex systems and trained controllers cannot produce direct Agentic cells, reproduction anchors or branch primaries.",
    ]
    base["decision_tables"] = {
        "paper_disposition": [
            _decision_row("material empirical runs are extractable", "EMPIRICAL_EXTRACTABLE", "a conceptual position paper"),
            _decision_row("claims or boundaries exist but no run is extractable", "NON_EMPIRICAL_EVIDENCE_ONLY", "a paper with source-located tables of runs"),
        ],
        "paper_role": [
            _decision_row("the intervention is the paper's evaluated method", "DIRECT_METHOD", "a benchmark that only supplies an evaluator"),
            _decision_row("the work supplies measurement or evaluator contracts", "INSTRUMENT", "a system intervention evaluated against baselines"),
        ],
        "reference_borrow_reproduce": [
            _decision_row("no protocol or result is transferred", "REFERENCE", "a source-to-target decision mapping"),
            _decision_row("a decision structure is translated with a rejection observation", "BORROW_PROTOCOL", "general inspiration without target variables"),
            _decision_row("paper support closes task/data/repo/entrypoint/access/terms/evaluator", "REPRODUCTION_CANDIDATE", "only a repository URL is present"),
        ],
        "access_and_dependency": [
            _decision_row("the foundation core is frozen and only input/output access is used", "TF_STRICT_BLACK_BOX", "controller weights are trained"),
            _decision_row("success depends on a specialized task core", "SPECIALIZED_MODEL_REQUIRED", "a generic frozen core calling external tools"),
        ],
        "agentic_scope": [
            _decision_row("both decision and action/tool components are observable", "DIRECT_AGENTIC", "a passive scorer with no action"),
            _decision_row("the work only measures or calibrates", "INSTRUMENT_SUPPORT", "an evaluated decide-act loop"),
        ],
        "primary_intervention": [
            _decision_row("one manipulated asset/control explains the comparison", "select exactly one primary axis", "crediting every system component without ablation"),
        ],
        "loop_and_capability_assets": [
            _decision_row("the loop reads/writes/retrieves persistent state", "MEMORY", "a static prompt containing facts"),
            _decision_row("reusable procedural competence is supplied or routed", "SKILL", "one-off factual retrieval"),
            _decision_row("external facts or evidence are acquired", "KNOWLEDGE", "persistent episodic state only"),
        ],
        "object_extraction_triggers": [
            _decision_row("a material run condition changes", "create a distinct run cell", "a second metric from the same run"),
            _decision_row("the source states dataset provenance or validation relation", "create a dataset edge", "task similarity without provenance"),
            _decision_row("baseline/intervention comparability closes", "create a paired comparison", "different model and budget with no controlled pair"),
        ],
    }
    base["compiler_owned_identity"] = {
        "source_anchor": "rendition SHA256 + typed anchor + normalized coordinate",
        "segmentation_signature": "paper + object type + source anchors + typed identity tuple",
        "caller_object_match_key_allowed": False,
        "fuzzy_or_post_hoc_matching_allowed": False,
    }
    base["named_paper_expectations_included"] = False
    base["prior_labels_included"] = False
    return base


def build_coder_prompt() -> dict[str, Any]:
    prompt = copy.deepcopy(rc2r3.build_package()["coder_prompt"])
    prompt.update({
        "schema": "sf-stage1c-v2-neutral-coder-prompt-v5",
        "artifact_id": "SF-STAGE1C-V2-NEUTRAL-CODER-PROMPT-R2",
        "prompt_seed": "R2_CODEBOOK_CONSOLIDATION_NEUTRAL_V1",
        "status": "PREPARED_NOT_DISTRIBUTED",
    })
    prompt["instructions"] = [
        "Code every assigned source independently using only the supplied bytes and neutral contract.",
        "Extract all material runs, observations and dataset objects; do not target one object per paper.",
        "Use supplied rendition IDs and precise typed coordinates; never invent object agreement keys.",
        "Record paper-visible reproduction support even when it remains open with source-stated blockers.",
        "Submit all 56 responses before agreement, another coder output or adjudication is revealed.",
    ]
    prompt["network_discovery_allowed"] = False
    prompt["repository_access_allowed"] = False
    prompt["other_coder_output_allowed"] = False
    return prompt


def build_agreement_contract() -> dict[str, Any]:
    return {
        "schema": "sf-stage1c-v2-agreement-contract-v6",
        "artifact_id": "SF-STAGE1C-V2-AGREEMENT-CONTRACT-R2",
        "calibration_response_schema_id": RESPONSE_SCHEMA_ID,
        "agreement_intake_contract_id": AGREEMENT_INTAKE_ID,
        "minimum_gate_value": AGREEMENT_MINIMUM,
        "agreement_minimum": AGREEMENT_MINIMUM,
        "threshold_override_prohibited": True,
        "compiler_owned_object_identity_required": True,
        "fuzzy_or_post_hoc_matching_prohibited": True,
        "unmatched_object_denominator_rule": "UNION_OBJECT_COUNT_FOR_EVERY_APPLICABLE_CRITICAL_FIELD",
        "not_calibrated_rule": "ONLY_WHEN_BOTH_CODERS_EMIT_ZERO_OBJECTS_FOR_THE_CLASS",
        "positive_support_preflight_required": True,
        "maximum_codebook_consolidations": 1,
        "second_round_failure_action": "STOP_AND_RETURN_TO_INDEPENDENT_METHOD_REVIEW",
        "adjudication_after_raw_freeze_only": True,
    }


def build_schema_bundle(response_schema: dict[str, Any]) -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "sf-stage1c-v2-schema-bundle-v5",
        "calibration_response_schema_id": response_schema["$id"],
        "$defs": copy.deepcopy(response_schema["$defs"]),
        "compiler_owned_identity_required": True,
        "paper_reproduction_support_is_blind_visible": True,
        "local_reproduction_readiness_is_reviewer_only": True,
    }


def build_local_reproduction_readiness(base: dict[str, Any]) -> dict[str, Any]:
    candidates = []
    for row in base["candidates"]:
        candidate = copy.deepcopy(row)
        candidate["anchor_status"] = "CANDIDATE_NOT_ANCHOR"
        candidate["paper_support_required"] = True
        candidate["local_closure_requires_100_percent_review"] = True
        candidates.append(candidate)
    return {
        "schema": "sf-stage1c-v2-local-reproduction-readiness-v1",
        "artifact_id": "SF-STAGE1C-V2-LOCAL-REPRODUCTION-READINESS-R2",
        "visibility": "REVIEWER_ONLY_NOT_DISTRIBUTED",
        "status": "READINESS_ONLY_NO_REPRODUCTION_ANCHOR",
        "candidates": candidates,
    }


def build_distribution_manifest(package: dict[str, Any]) -> dict[str, Any]:
    names = CODER_DISTRIBUTION_ALLOWED_ARTIFACTS
    raw = {name: json_bytes(package[name]) for name in names}
    return {
        "schema": "sf-stage1c-v2-calibration-distribution-manifest-v6",
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
    schema = copy.deepcopy(rc2r3.build_delivery_receipt_schema())
    schema["$id"] = DELIVERY_RECEIPT_SCHEMA_ID
    schema["properties"]["distribution_manifest_id"] = {"const": DISTRIBUTION_MANIFEST_ID}
    return schema


def build_delivery_receipt_template() -> dict[str, Any]:
    template = copy.deepcopy(rc2r3.build_delivery_receipt_template())
    template.update({
        "schema": "sf-stage1c-v2-delivery-receipt-template-v3",
        "artifact_id": "SF-STAGE1C-V2-DELIVERY-RECEIPT-TEMPLATE-R2",
        "delivery_receipt_schema_id": DELIVERY_RECEIPT_SCHEMA_ID,
    })
    return template


def _receipt_projection(receipt: dict[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(receipt)
    value.pop("receipt_sha256", None)
    return value


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
    for name in names:
        if not isinstance(received_artifacts[name], bytes):
            raise ContractError(f"actual received artifact {name} must be bytes")
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
    if actual_bundle != distribution["content_bundle_sha256"]:
        raise ContractError("actual received artifact bundle differs")
    actual_prompt = sha256_bytes(received_prompt_bytes)
    if actual_prompt != distribution["coder_prompt_sha256"]:
        raise ContractError("actual received prompt differs")
    if received_prompt_bytes != received_artifacts["coder_prompt"]:
        raise ContractError("actual received prompt differs from coder_prompt artifact")
    receipt = {
        "schema": "sf-stage1c-v2-delivery-receipt-v2",
        "receipt_id": f"R2-DELIVERY-{slot}-{transaction_id}-{task_id}",
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
    receipt["receipt_sha256"] = sha256_bytes(json_bytes(_receipt_projection(receipt)))
    try:
        Draft202012Validator(package["delivery_receipt_schema"]).validate(receipt)
    except ValidationError as error:
        raise ContractError(f"invalid actual-byte delivery receipt: {error.message}") from error
    return receipt


def bind_runtime_intake(
    package: dict[str, Any], bindings: Iterable[dict[str, str]], receipts: list[dict[str, Any]],
) -> dict[str, Any]:
    intake = copy.deepcopy(package["agreement_intake_contract"])
    binding_by_slot = {row["slot"]: row for row in bindings}
    receipt_by_slot = {row["coder_slot"]: row for row in receipts}
    if set(binding_by_slot) != {"A", "B"} or set(receipt_by_slot) != {"A", "B"}:
        raise ContractError("runtime intake requires exact A/B bindings and actual-byte receipts")
    intake["status"] = "BOUND_FOR_PRE_ADJUDICATION_AGREEMENT"
    for target in intake["coder_slots"]:
        slot = target["coder_slot"]
        binding, receipt = binding_by_slot[slot], receipt_by_slot[slot]
        for receipt_key, binding_key in (
            ("coder_id", "coder_id"),
            ("coder_transaction_id", "transaction_id"),
            ("process_id", "process_id"),
            ("task_id", "task_id"),
            ("model", "model"),
        ):
            if receipt.get(receipt_key) != binding.get(binding_key):
                raise ContractError(f"runtime binding differs from receipt {receipt_key}")
        target.update({
            "model": binding["model"],
            "coder_id": binding["coder_id"],
            "coder_transaction_id": binding["transaction_id"],
            "process_id": binding["process_id"],
            "task_id": binding["task_id"],
            "assignment_status": "FROZEN_SUBMITTED",
            "distribution_receipt_id": receipt["receipt_id"],
            "submission_receipt_id": f"SUBMISSION-{receipt['receipt_id']}",
            "delivery_receipt_id": receipt["receipt_id"],
            "delivery_receipt_sha256": receipt["receipt_sha256"],
            "received_content_bundle_sha256": receipt["received_content_bundle_sha256"],
            "received_prompt_sha256": receipt["received_prompt_sha256"],
        })
    return intake


def build_agreement_intake_contract(package: dict[str, Any]) -> dict[str, Any]:
    intake = copy.deepcopy(rc2r3.build_package()["agreement_intake_contract"])
    intake.update({
        "schema": "sf-stage1c-v2-agreement-intake-contract-v6",
        "artifact_id": AGREEMENT_INTAKE_ID,
        "calibration_manifest_id": CALIBRATION_MANIFEST_ID,
        "response_schema_id": RESPONSE_SCHEMA_ID,
        "distribution_manifest_id": DISTRIBUTION_MANIFEST_ID,
        "delivery_receipt_schema_id": DELIVERY_RECEIPT_SCHEMA_ID,
        "content_bundle_sha256": package["distribution_manifest"]["content_bundle_sha256"],
        "prompt_hash": package["distribution_manifest"]["coder_prompt_sha256"],
        "agreement_minimum": AGREEMENT_MINIMUM,
        "compiler_owned_object_identity_required": True,
        "unmatched_objects_enter_critical_field_denominators": True,
    })
    for slot in intake["coder_slots"]:
        slot["expected_content_bundle_sha256"] = intake["content_bundle_sha256"]
        slot["expected_prompt_hash"] = intake["prompt_hash"]
        slot["task_id"] = None
    return intake


def static_intake_projection(intake: dict[str, Any]) -> dict[str, Any]:
    fixed = (
        "schema", "artifact_id", "calibration_manifest_id", "response_schema_id",
        "source_manifest_id", "distribution_manifest_id", "delivery_receipt_schema_id",
        "content_bundle_sha256", "prompt_hash", "agreement_minimum", "N",
        "canonical_paper_ids", "items", "completed_response_validator_required",
        "raw_outputs_frozen_before_agreement", "compiler_owned_object_identity_required",
        "unmatched_objects_enter_critical_field_denominators",
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
        raise ContractError("agreement intake lacks frozen R2 base fields") from error
    return projection


def _rendition_map(source_manifest: dict[str, Any]) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for item in source_manifest["items"]:
        result[item["canonical_id"]] = {
            rendition["rendition_id"]: rendition["sha256"]
            for rendition in [item["primary_rendition"], *item["alternate_renditions"]]
        }
    return result


def build_frozen_package_contract(package: dict[str, Any]) -> dict[str, Any]:
    intake = package["agreement_intake_contract"]
    return {
        "schema": "sf-stage1c-v2-frozen-package-contract-v3",
        "artifact_id": "SF-STAGE1C-V2-FROZEN-PACKAGE-CONTRACT-R2",
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
        "base_intake_static_sha256": sha256_bytes(json_bytes(static_intake_projection(intake))),
        "paper_rendition_map_sha256": sha256_bytes(json_bytes(_rendition_map(package["source_manifest"]))),
        "positive_support_preflight_sha256": sha256_bytes(json_bytes(package["positive_support_preflight"])),
        "content_bundle_sha256": package["distribution_manifest"]["content_bundle_sha256"],
        "prompt_sha256": package["distribution_manifest"]["coder_prompt_sha256"],
        "N": 56,
        "canonical_paper_ids_sha256": sha256_bytes(json_bytes(intake["canonical_paper_ids"])),
        "compiled_into_agreement_engine": True,
    }


def _canonical_text(value: Any) -> Any:
    if isinstance(value, str):
        return " ".join(unicodedata.normalize("NFKC", value).casefold().split())
    if isinstance(value, list):
        return sorted((_canonical_text(item) for item in value), key=lambda item: json.dumps(item, sort_keys=True))
    if isinstance(value, dict):
        return {key: _canonical_text(value[key]) for key in sorted(value)}
    return value


def _digest(prefix: str, value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return f"{prefix}-{hashlib.sha256(raw).hexdigest()[:24]}"


def _anchor_index(response: dict[str, Any], source_manifest: dict[str, Any]) -> tuple[dict[str, str], list[dict[str, Any]]]:
    paper_id = response["paper_id"]
    renditions = _rendition_map(source_manifest).get(paper_id)
    if renditions is None:
        raise ContractError(f"paper is absent from source manifest: {paper_id}")
    locator_to_anchor: dict[str, str] = {}
    anchors: dict[str, dict[str, Any]] = {}
    for locator in response["source_locators"]:
        rendition_id = locator["rendition_id"]
        if rendition_id not in renditions:
            raise ContractError("source locator rendition is not supplied for this paper")
        identity = {
            "rendition_sha256": renditions[rendition_id],
            "anchor_type": locator["anchor_type"],
            "anchor_value": _canonical_text(locator["anchor_value"]),
        }
        anchor_id = _digest("SA", identity)
        locator_to_anchor[locator["locator_id"]] = anchor_id
        anchors[anchor_id] = {"source_anchor_id": anchor_id, **identity}
    return locator_to_anchor, [anchors[key] for key in sorted(anchors)]


def _replace_locator_ids(obj: dict[str, Any], locator_to_anchor: dict[str, str]) -> list[str]:
    try:
        anchors = sorted({locator_to_anchor[locator_id] for locator_id in obj["source_locator_ids"]})
    except KeyError as error:
        raise ContractError("object references an undeclared source locator") from error
    if not anchors:
        raise ContractError("evidence-bearing object requires a source anchor")
    obj["source_locator_ids"] = anchors
    return anchors


def _object_key(paper_id: str, array_name: str, anchors: list[str], identity: Any) -> str:
    return _digest("OBJ", {
        "paper_id": paper_id,
        "object_type": array_name,
        "source_anchors": anchors,
        "identity_tuple": _canonical_text(identity),
    })


def compile_response_objects(response: dict[str, Any], source_manifest: dict[str, Any]) -> dict[str, Any]:
    """Compile raw coder objects into deterministic exact-comparison identities."""

    compiled = copy.deepcopy(response)
    locator_to_anchor, anchors = _anchor_index(compiled, source_manifest)
    compiled["compiled_source_anchors"] = anchors
    paper_id = compiled["paper_id"]
    id_maps: dict[str, str] = {}

    def compile_array(array_name: str, id_field: str, identity_builder: Any) -> None:
        seen: set[str] = set()
        for obj in compiled[array_name]:
            source_id = obj[id_field]
            anchors_for_object = _replace_locator_ids(obj, locator_to_anchor)
            identity = identity_builder(obj)
            key = _object_key(paper_id, array_name, anchors_for_object, identity)
            if key in seen:
                raise ContractError(f"duplicate compiler-derived {array_name} segmentation signature")
            seen.add(key)
            obj["object_match_key"] = key
            id_maps[source_id] = key

    compile_array(
        "dataset_nodes", "dataset_node_id",
        lambda obj: {"name": obj["name"]},
    )

    for obj in compiled["run_cells"]:
        try:
            obj["dataset_node_ids"] = sorted(id_maps[value] for value in obj["dataset_node_ids"])
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
            obj["run_cell_id"] = id_maps[obj["run_cell_id"]]
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
            obj["baseline_cell_id"] = id_maps[obj["baseline_cell_id"]]
            obj["intervention_cell_id"] = id_maps[obj["intervention_cell_id"]]
        except KeyError as error:
            raise ContractError("paired comparison references an undeclared run cell") from error
    compile_array(
        "paired_comparisons", "comparison_id",
        lambda obj: {"baseline": obj["baseline_cell_id"], "intervention": obj["intervention_cell_id"]},
    )

    for obj in compiled["dataset_edges"]:
        try:
            obj["source_dataset_id"] = id_maps[obj["source_dataset_id"]]
            obj["target_dataset_id"] = id_maps[obj["target_dataset_id"]]
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

    for obj in compiled["translation_or_compatibility_decisions"]:
        obj["target_object_id"] = id_maps.get(obj["target_object_id"], obj["target_object_id"])
    compile_array(
        "translation_or_compatibility_decisions", "decision_id",
        lambda obj: {"type": obj["decision_type"], "target": obj["target_object_id"]},
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
    return compiled


_GENERIC_LOCATORS = {"abstract", "title", "paper", "full paper", "entire paper"}


def _contains_not_coded(value: Any) -> bool:
    if value == "NOT_CODED":
        return True
    if isinstance(value, dict):
        return any(_contains_not_coded(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_not_coded(item) for item in value)
    return False


def validate_completed_response(
    response: dict[str, Any], response_schema: dict[str, Any], source_manifest: dict[str, Any]
) -> None:
    try:
        Draft202012Validator(response_schema).validate(response)
    except ValidationError as error:
        raise ContractError(f"response schema validation failed: {error.message}") from error
    if response.get("response_status") != "CODER_SUBMITTED":
        raise ContractError("completed response must be CODER_SUBMITTED")
    if _contains_not_coded(response["paper_labels"]):
        raise ContractError("completed response retains NOT_CODED paper labels")
    if response["paired_comparison_absence_reason"] == "NOT_CODED":
        raise ContractError("completed response retains NOT_CODED paired-comparison reason")

    locator_by_id = {row["locator_id"]: row for row in response["source_locators"]}
    if len(locator_by_id) != len(response["source_locators"]):
        raise ContractError("duplicate source locator ID")
    _anchor_index(response, source_manifest)
    for array_name in OBJECT_ARRAYS:
        objects = response[array_name]
        reason = response["object_absence_reasons"][array_name]
        if objects and reason != "OBJECTS_PRESENT":
            raise ContractError(f"{array_name} objects require OBJECTS_PRESENT")
        if not objects and reason == "OBJECTS_PRESENT":
            raise ContractError(f"{array_name} empty array cannot claim OBJECTS_PRESENT")
        for obj in objects:
            for locator_id in obj["source_locator_ids"]:
                if locator_id not in locator_by_id:
                    raise ContractError(f"{array_name} references an undeclared source locator")
                locator = locator_by_id[locator_id]
                if (
                    _canonical_text(locator["anchor_value"]) in _GENERIC_LOCATORS
                    or _canonical_text(locator["precise_locator"]) in _GENERIC_LOCATORS
                ):
                    raise ContractError("evidence-bearing object uses a title/abstract-only locator")

    pairs = response["paired_comparisons"]
    pair_reason = response["paired_comparison_absence_reason"]
    if pairs and pair_reason != "OBJECTS_PRESENT":
        raise ContractError("paired comparison objects require OBJECTS_PRESENT")
    if not pairs and pair_reason == "OBJECTS_PRESENT":
        raise ContractError("empty paired comparison array cannot claim OBJECTS_PRESENT")

    labels = response["paper_labels"]
    if labels["paper_disposition"] == "EMPIRICAL_EXTRACTABLE":
        if not response["run_cells"] or not response["observations"] or not response["dataset_nodes"]:
            raise ContractError("EMPIRICAL_EXTRACTABLE requires material run cells, observations and dataset nodes")
    if labels["empirical_experiment_present"] is True and not response["run_cells"]:
        raise ContractError("empirical experiment present requires material run cells")

    scope = labels["agentic_scope"]
    if (
        scope["scope_status"] == "OUT_OF_SCOPE_SPECIALIZED_SYSTEM"
        or scope["core_dependency"] == "SPECIALIZED_MODEL_REQUIRED"
        or labels["access_regime"] == "TRAINED_PARAMETER_UPDATE"
    ) and any(response[name] for name in ("run_cells", "observations", "paired_comparisons")):
        raise ContractError("specialized/trained exclusion cannot produce Agentic experiment cells")

    label = labels["reference_borrow_reproduce"]
    transfers = response["protocol_transfer_evidence"]
    support = response["paper_reproduction_support"]
    if label == "BORROW_PROTOCOL" and not transfers:
        raise ContractError("BORROW_PROTOCOL requires complete transfer evidence")
    if label != "BORROW_PROTOCOL" and transfers:
        raise ContractError("only BORROW_PROTOCOL may carry protocol transfer evidence")
    if label == "REPRODUCTION_CANDIDATE":
        closed = [
            row for row in support
            if row["closure_status"] == "CLOSED_PAPER_SUPPORT" and not row["blockers"]
        ]
        if not closed:
            raise ContractError("REPRODUCTION_CANDIDATE requires closed paper support")
    for row in support:
        if row["closure_status"] == "OPEN_WITH_BLOCKERS" and not row["blockers"]:
            raise ContractError("OPEN_WITH_BLOCKERS requires at least one blocker")
        if row["closure_status"] == "CLOSED_PAPER_SUPPORT" and row["blockers"]:
            raise ContractError("CLOSED_PAPER_SUPPORT cannot retain blockers")

    compile_response_objects(response, source_manifest)


def build_positive_support_ledger(package: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "sf-stage1c-v2-positive-support-ledger-v2",
        "artifact_id": "SF-STAGE1C-V2-POSITIVE-SUPPORT-LEDGER-R2",
        "visibility": "REVIEWER_ONLY_NOT_DISTRIBUTED",
        "mandatory_object_classes": ["dataset_edges", "paper_reproduction_support"],
        "evidence": {
            "dataset_edges": [
                {
                    "paper_id": "acl:2026.findings-eacl.151",
                    "source_locators": [{
                        "locator_id": "LOC-POS-TRACE-P3",
                        "rendition_id": "SRC-2026.findings-eacl.151-PDF",
                        "anchor_type": "PAGE",
                        "anchor_value": "3",
                        "precise_locator": "Page 3, Section 3.1 Existing Benchmark Pitfalls.",
                    }],
                    "object": {
                        "dataset_edge_id": "DE-POS-TRACE-SUBSET",
                        "edge_type": "LINEAGE",
                        "source_dataset_id": "DS-S2S-ARENA",
                        "relation": "SUBSET_OF",
                        "target_dataset_id": "DS-S2S-ARENA-ENGLISH",
                        "reason": "The evaluation explicitly uses the English subset of S2S-Arena.",
                        "source_locator_ids": ["LOC-POS-TRACE-P3"],
                    },
                },
                {
                    "paper_id": "acl:2026.findings-eacl.151",
                    "source_locators": [{
                        "locator_id": "LOC-POS-TRACE-P3-R",
                        "rendition_id": "SRC-2026.findings-eacl.151-PDF",
                        "anchor_type": "PAGE",
                        "anchor_value": "3",
                        "precise_locator": "Page 3, Section 3.1 re-annotation statement.",
                    }],
                    "object": {
                        "dataset_edge_id": "DE-POS-TRACE-REANNOTATION",
                        "edge_type": "LINEAGE",
                        "source_dataset_id": "DS-S2S-ARENA",
                        "relation": "REANNOTATED_FROM",
                        "target_dataset_id": "DS-TRACE-S2S-ARENA",
                        "reason": "The work explicitly re-annotates existing benchmark data.",
                        "source_locator_ids": ["LOC-POS-TRACE-P3-R"],
                    },
                },
            ],
            "paper_reproduction_support": [
                {
                    "paper_id": "arxiv:2510.02995",
                    "source_locators": [{
                        "locator_id": "LOC-POS-AUDIOTOOL-P1",
                        "rendition_id": "SRC-2510.02995-PDF",
                        "anchor_type": "PAGE",
                        "anchor_value": "1",
                        "precise_locator": "Page 1, abstract and contribution statement with official repository URL.",
                    }],
                    "object": {
                        "reproduction_support_id": "PRS-AUDIOTOOLAGENT-PAPER",
                        "task": "audio question answering and reasoning",
                        "dataset": "MMAU; MMAR; MMAU-Pro",
                        "dataset_revision": "paper-reported",
                        "split": "MMAU test-mini; MMAR; MMAU-Pro",
                        "official_repo": "https://github.com/GLJS/AudioToolAgent",
                        "pinned_revision": "NOT_STATED_IN_SOURCE",
                        "entrypoint": "NOT_STATED_IN_SOURCE",
                        "model_access": "MIXED_OR_UNCLEAR",
                        "license_terms": "NOT_STATED_IN_SOURCE",
                        "evaluator_or_ground_truth": "benchmark accuracy",
                        "source_locator_ids": ["LOC-POS-AUDIOTOOL-P1"],
                        "closure_status": "OPEN_WITH_BLOCKERS",
                        "blockers": [
                            "The supplied paper states the repository but not a pinned revision, entrypoint or license terms."
                        ],
                    },
                }
            ],
        },
    }


def validate_positive_support(ledger: dict[str, Any], package: dict[str, Any]) -> dict[str, Any]:
    mandatory = ledger.get("mandatory_object_classes")
    try:
        r2_guards.require_exact_positive_classes(mandatory, ledger.get("evidence", {}))
    except r2_guards.GuardError as error:
        raise ContractError(str(error)) from error
    source_by_paper = {row["canonical_id"]: row for row in package["source_manifest"]["items"]}
    class_gates: dict[str, Any] = {}
    for array_name in mandatory:
        rows = ledger.get("evidence", {}).get(array_name, [])
        definition_name = OBJECT_DEFINITION_BY_ARRAY[array_name]
        definition = package["response_schema"]["$defs"][definition_name]
        schema_expressible = True
        for row in rows:
            paper_id = row.get("paper_id")
            source = source_by_paper.get(paper_id)
            if source is None:
                raise ContractError(f"positive support paper is outside unchanged N=56: {paper_id}")
            rendition_ids = {
                rendition["rendition_id"]
                for rendition in [source["primary_rendition"], *source["alternate_renditions"]]
            }
            if any(locator["rendition_id"] not in rendition_ids for locator in row["source_locators"]):
                raise ContractError("positive support locator is outside frozen paper renditions")
            locator_ids = {locator["locator_id"] for locator in row["source_locators"]}
            if not set(row["object"]["source_locator_ids"]).issubset(locator_ids):
                raise ContractError("positive support object references an undeclared locator")
            try:
                Draft202012Validator(definition).validate(row["object"])
            except ValidationError as error:
                schema_expressible = False
                raise ContractError(f"positive support is not schema-expressible: {error.message}") from error
        status = "PASS" if rows and schema_expressible else "FAIL"
        class_gates[array_name] = {
            "source_supported_positive_count": len(rows),
            "schema_expressible": schema_expressible,
            "status": status,
        }
    return {
        "schema": "sf-stage1c-v2-positive-support-preflight-v2",
        "artifact_id": "SF-STAGE1C-V2-POSITIVE-SUPPORT-PREFLIGHT-R2",
        "status": "PASS" if all(row["status"] == "PASS" for row in class_gates.values()) else "FAIL",
        "visibility": "REVIEWER_ONLY_NOT_DISTRIBUTED",
        "mandatory_object_classes": mandatory,
        "class_gates": class_gates,
        "sample_changed": False,
        "expected_labels_distributed": False,
    }


def build_package() -> dict[str, Any]:
    predecessor = rc2r3.build_package()
    response_schema = build_response_schema()
    package: dict[str, Any] = copy.deepcopy(predecessor)
    package["response_schema"] = response_schema
    package["schema_bundle"] = build_schema_bundle(response_schema)

    package["calibration_manifest"].update({
        "schema": "sf-stage1c-v2-calibration-manifest-v6",
        "artifact_id": CALIBRATION_MANIFEST_ID,
        "status": "AGENTIC_CALIBRATION_R2_METHOD_READY_NOT_DISTRIBUTED",
        "calibration_response_schema_id": RESPONSE_SCHEMA_ID,
        "overlay_count": package["calibration_manifest"]["overlay_record_count"],
        "sentinel_count": package["calibration_manifest"]["inherited_sentinel_count"],
        "r1_raw_outputs_immutable": True,
        "single_recode_round_remaining": True,
    })
    package["blind_packet"].update({
        "schema": "sf-stage1c-v2-calibration-blind-packet-v5",
        "artifact_id": "SF-STAGE1C-V2-LABEL-HIDDEN-PACKET-56-R2",
        "calibration_response_schema_id": RESPONSE_SCHEMA_ID,
    })
    for item in package["blind_packet"]["items"]:
        response = item["blank_response"]
        response["schema"] = RESPONSE_SCHEMA_CONST
        response.pop("reproduction_evidence", None)
        response["paper_reproduction_support"] = []
        response["paired_comparison_absence_reason"] = "NOT_CODED"
        response["object_absence_reasons"] = {name: "NOT_CODED" for name in OBJECT_ARRAYS}

    package["coder_codebook"] = build_coder_codebook()
    package["coder_prompt"] = build_coder_prompt()
    package["agreement"] = build_agreement_contract()
    package["local_reproduction_readiness"] = build_local_reproduction_readiness(
        predecessor["reproduction_readiness"]
    )
    package.pop("reproduction_readiness", None)
    package["delivery_receipt_schema"] = build_delivery_receipt_schema()
    package["delivery_receipt_template"] = build_delivery_receipt_template()
    package["distribution_manifest"] = build_distribution_manifest(package)
    package["coder_transaction"].update({
        "schema": "sf-stage1c-v2-coder-transaction-contract-v6",
        "artifact_id": "SF-STAGE1C-V2-CODER-INTAKE-R2",
        "distribution_manifest_id": DISTRIBUTION_MANIFEST_ID,
        "delivery_receipt_schema_id": DELIVERY_RECEIPT_SCHEMA_ID,
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
    predecessor = rc2r3.build_package()
    expected_ids = predecessor["calibration_manifest"]["canonical_ids"]
    calibration = package["calibration_manifest"]
    if (
        calibration.get("N") != 56
        or calibration.get("canonical_ids") != expected_ids
        or package["source_manifest"].get("N") != 56
    ):
        raise ContractError("R2 must preserve the unchanged N=56 sample and order")
    if calibration.get("overlay_count") != 38 or calibration.get("sentinel_count") != 18:
        raise ContractError("R2 must preserve 38 overlays plus 18 sentinels")
    if package["response_schema"].get("$id") != RESPONSE_SCHEMA_ID:
        raise ContractError("R2 response schema identity differs")
    for definition_name in OBJECT_DEFINITION_BY_ARRAY.values():
        if "object_match_key" in package["response_schema"]["$defs"][definition_name]["properties"]:
            raise ContractError("R2 raw schema permits caller-authored object_match_key")
    try:
        r2_guards.require_paper_local_observability_split(
            package["response_schema"],
            CODER_DISTRIBUTION_ALLOWED_ARTIFACTS,
            "local_reproduction_readiness",
        )
    except r2_guards.GuardError as error:
        raise ContractError(str(error)) from error

    validator = Draft202012Validator(package["response_schema"])
    for item in package["blind_packet"]["items"]:
        validator.validate(item["blank_response"])
    names = tuple(row["artifact_name"] for row in package["distribution_manifest"]["artifacts"])
    leaks = scan_coder_bundle_leaks(package, names)
    if leaks:
        raise ContractError(f"coder-visible leakage detected: {leaks}")
    if package["distribution_manifest"].get("distribution_authorized"):
        raise ContractError("R2 coder distribution occurred before independent method acceptance")
    raw = {name: json_bytes(package[name]) for name in names}
    if package["distribution_manifest"]["content_bundle_sha256"] != coder_bundle_sha256_from_raw(raw, names):
        raise ContractError("R2 coder bundle hash is stale")
    for row in package["distribution_manifest"]["artifacts"]:
        actual = raw[row["artifact_name"]]
        if row["bytes"] != len(actual) or row["sha256"] != sha256_bytes(actual):
            raise ContractError(f"R2 distribution artifact is stale: {row['artifact_name']}")
    if package["agreement"].get("agreement_minimum") != AGREEMENT_MINIMUM:
        raise ContractError("R2 agreement threshold differs from 0.85")
    if package["positive_support_preflight"].get("status") != "PASS":
        raise ContractError("R2 mandatory positive-support preflight did not pass")
    validate_positive_support(package["positive_support_ledger"], package)
    if any(
        row.get("anchor_status") == "REPRODUCTION_ANCHOR"
        for row in package["local_reproduction_readiness"]["candidates"]
    ):
        raise ContractError("R2 promoted a reproduction anchor")
    if package["frozen_package_contract"] != build_frozen_package_contract(package):
        raise ContractError("R2 frozen package contract is stale")


def build_report(package: dict[str, Any]) -> dict[str, Any]:
    validate_package(package)
    return {
        "schema": "sf-stage1c-v2-precalibration-contract-report-v6",
        "artifact_id": "SF-STAGE1C-V2-PRECALIBRATION-CONTRACT-REPORT-R2",
        "as_of": "2026-07-25",
        "status": "AGENTIC_CALIBRATION_R2_METHOD_READY_NOT_DISTRIBUTED",
        "predecessor": {
            "release": "AGENTIC_RC2R3_PLUS_FAILED_CALIBRATION_R1",
            "r1_raw_outputs_immutable": True,
            "sample_unchanged": True,
        },
        "authority": {
            "codebook_consolidation_authorized": True,
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
            "compiler_owned_object_identity": True,
            "unmatched_union_field_denominators": True,
            "paper_support_local_readiness_split": True,
            "typed_extraction_triggers": True,
            "mandatory_positive_support_preflight": True,
            "paper_decision_tables": True,
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
            "FREEZE_EXACT_REVIEW_PACKAGE_IN_LOCAL_COMMIT",
            "OBTAIN_ACCEPT_AGENTIC_CALIBRATION_R2_METHOD_CONTRACT_FOR_CODER_INTAKE",
            "MATERIALIZE_TWO_NEW_ISOLATED_RECEIVER_SIDE_RECEIPTS",
        ],
    }


def load_package() -> dict[str, Any]:
    return {name: load_json(path) for name, path in ARTIFACT_PATHS.items()}


def build_review_manifest(report: dict[str, Any]) -> dict[str, Any]:
    paths = [
        OWNER_AUTHORIZATION,
        R1_PRE_ADJUDICATION,
        R1_POSITIVE_PREFLIGHT,
        RC2R3_REVIEW,
        WORKBENCH / "README.md",
        WORKBENCH / "codebook-v6.md",
        WORKBENCH / "stage1c-v2-precalibration-contract-r2-zh.md",
        REPO / "scripts/survey/sf_stage1c_v2_r2_guards.py",
        REPO / "scripts/survey/sf_stage1c_v2_precalibration_r2.py",
        REPO / "scripts/survey/sf_stage1c_v2_calibration_agreement_v6.py",
        REPO / "scripts/survey/test_sf_stage1c_v2_precalibration_r2.py",
        *ARTIFACT_PATHS.values(),
        REPORT_PATH,
        VERIFICATION_PATH,
    ]
    missing = [path for path in paths if not path.is_file()]
    if missing:
        raise ContractError(f"R2 review inputs missing: {missing}")
    return {
        "schema": "sf-stage1c-v2-precalibration-review-manifest-v6",
        "artifact_id": "SF-STAGE1C-V2-PRECALIBRATION-REVIEW-PACKAGE-R2",
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
        "requested_review_verdict": "ACCEPT_AGENTIC_CALIBRATION_R2_METHOD_CONTRACT_FOR_CODER_INTAKE_OR_WITHHOLD_WITH_BOUNDED_DEFECTS",
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
                raise ContractError(f"materialized R2 artifact is stale: {ARTIFACT_PATHS[name]}")
        if load_json(REPORT_PATH) != report:
            raise ContractError("R2 contract report is stale")
        if load_json(REVIEW_MANIFEST_PATH) != build_review_manifest(report):
            raise ContractError("R2 review manifest is stale")
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
