#!/usr/bin/env python3
"""Build and verify the bounded Stage-1C v2 pre-calibration RC2 package.

RC2 repairs the response/agreement unit, binds the exact 56 source byte streams,
separates synthesis templates from scoped claims, and operationalizes coder
intake.  It prepares no coder output and grants no mapping or research authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import sf_stage1c_v2_precalibration as rc1
    from sf_asset_path import resolve_asset_path
else:
    from scripts.survey import sf_stage1c_v2_precalibration as rc1
    from scripts.survey.sf_asset_path import resolve_asset_path


REPO = Path(__file__).resolve().parents[2]
WORKBENCH = REPO / "wiki/survey/workbench/system-first-stage1c-v2-precalibration"
CHECK_DIR = REPO / "docs/checks/stage1c-v2-precalibration/2026-07-24-rc2"
LEDGER = REPO / "wiki/survey/2026-07-17-sf-fulltext-ledger.jsonl"
OWNER_DIRECTION = REPO / "wiki/audit/system-first-stage1c-v2-precalibration/owner-rc2-direction/2026-07-24-owner-rc2-direction.md"
REVIEW = REPO / "wiki/audit/system-first-stage1c-v2-precalibration/doctoral-supervisor-review/2026-07-24-stage1c-v2-precalibration-doctoral-supervisor-review.md"
OWNER_AGENTIC_RULING = (
    "Duplex这种任务需要专用模型，这类任务我们不考虑了，我们更多的聚焦在agentic的技术演进路径上，"
    "不要在无关方向上耗散自己的精力了。"
)

ARTIFACT_PATHS = {
    "response_schema": WORKBENCH / "calibration-response-schema-v2.json",
    "schema_bundle": WORKBENCH / "schema-bundle-v2.json",
    "source_manifest": WORKBENCH / "calibration-source-byte-manifest-v2.json",
    "calibration_manifest": WORKBENCH / "calibration-manifest-v2.json",
    "blind_packet": WORKBENCH / "calibration-blind-packet-v2.json",
    "assignment_manifest": WORKBENCH / "calibration-assignment-manifest-v2.json",
    "claim_templates": WORKBENCH / "claim-template-registry-v2.json",
    "claim_template_coder_view": WORKBENCH / "claim-template-coder-view-v2.json",
    "coder_codebook": WORKBENCH / "coder-codebook-v2.json",
    "agreement": WORKBENCH / "agreement-contract-v2.json",
    "coder_transaction": WORKBENCH / "coder-transaction-contract-v2.json",
    "reproduction_readiness": WORKBENCH / "reproduction-readiness-v2.json",
    "distribution_manifest": WORKBENCH / "calibration-distribution-manifest-v2.json",
}
REPORT_PATH = CHECK_DIR / "contract-report.json"
REVIEW_MANIFEST_PATH = WORKBENCH / "review-package-manifest-rc2.json"

CALIBRATED_OBJECT_ARRAYS = (
    "run_cells", "observations", "paired_comparisons", "dataset_nodes",
    "dataset_edges", "claim_decisions", "translation_or_compatibility_decisions",
)
PROBLEM_NODES = (
    "BUDGET_STOP_REPAIR", "EVALUATOR_REWARD_RELIABILITY",
    "ACTIVE_MULTIMODAL_EVIDENCE_ACQUISITION_UNDER_BUDGET",
    "SKILL_ACCESS_MAINTENANCE_AND_NEGATIVE_TRANSFER",
    "MEMORY_RETRIEVAL_TO_USE_AND_ACTION_GAP", "UNROUTED", "NOT_CODED",
)
INTERVENTION_AXES = (*sorted(rc1.INTERVENTION_AXES), "NOT_APPLICABLE", "NOT_CODED")
PRIMARY_INTERVENTION_AXES = (*sorted(rc1.INTERVENTION_AXES), "NOT_APPLICABLE")
AGENTIC_SCOPE_STATUS = (
    "DIRECT_AGENTIC", "INSTRUMENT_SUPPORT", "TRANSFER_ANALOGUE",
    "REFERENCE_ONLY_BOUNDARY", "OUT_OF_SCOPE_SPECIALIZED_SYSTEM", "NOT_CODED",
)
LOOP_COMPONENTS = (
    "OBSERVE", "STATE_OR_MEMORY", "DECIDE", "ACT_OR_TOOL", "EVALUATE",
    "UPDATE_OR_REPAIR", "STOP_OR_BUDGET", "NONE", "NOT_CODED",
)
CORE_DEPENDENCY = (
    "GENERIC_FROZEN_CORE", "SPECIALIZED_MODEL_REQUIRED",
    "TRAINED_CONTROLLER_REQUIRED", "MIXED_OR_UNCLEAR", "NOT_CODED",
)
CAPABILITY_ASSETS = ("KNOWLEDGE", "SKILL", "MEMORY", "NONE", "NOT_CODED")
CONTROL_ROLES = (
    "TRAINING_FREE_REWARD_GUIDED", "TRAINING_FREE_NON_REWARD_AGENTIC",
    "TRAINED_CONTROL", "INSTRUMENT_ONLY", "NONE", "NOT_CODED",
)
CODER_DISTRIBUTION_ALLOWED_ARTIFACTS = (
    "response_schema", "source_manifest", "assignment_manifest", "blind_packet",
    "coder_codebook", "claim_template_coder_view", "agreement",
)
CODER_DISTRIBUTION_FORBIDDEN_KEYS = frozenset({
    "selection_rationale", "origin_work_ids", "paper_to_template_links",
    "stage1b_role", "problem_routes", "eligible_input_families",
    "project_relation", "candidate_priority", "primary_selection",
    "fallback_selection", "overlay_ids", "inherited_sentinels",
    "agentic_scope_correction", "reproduction_readiness",
})
CODER_VIEW_FORBIDDEN_NAMED_EXPECTATIONS = (
    "Full-Duplex", "FDB-v2", "Audio MultiChallenge", "AudioGenie-Reasoner",
    "AudioToolAgent", "Audio2Tool", "2510.07838", "2512.14865",
    "2509.16971", "2510.02995", "2604.22821",
)


class ContractError(RuntimeError):
    """Raised when RC2 fails closed."""


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ContractError(f"expected JSON object: {path}")
    return value


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(json_bytes(value))


def _enum(*values: str) -> dict[str, Any]:
    return {"type": "string", "enum": list(values)}


def _text(*, nullable: bool = False, pattern: str | None = None) -> dict[str, Any]:
    value: dict[str, Any] = {"type": ["string", "null"] if nullable else "string"}
    if not nullable:
        value["minLength"] = 1
    if pattern:
        value["pattern"] = pattern
    return value


def _array(items: dict[str, Any], *, unique: bool = True) -> dict[str, Any]:
    return {"type": "array", "items": items, "uniqueItems": unique}


def _object(required: list[str], properties: dict[str, Any]) -> dict[str, Any]:
    return {
        "type": "object", "additionalProperties": False,
        "required": required, "properties": properties,
    }


def build_response_schema() -> dict[str, Any]:
    source_ids = _array(_text(pattern=r"^LOC-[A-Za-z0-9._:-]+$"))
    match_key = _text(pattern=r"^[A-Za-z0-9][A-Za-z0-9._:/+-]{2,159}$")
    scope = _object(
        list(rc1.CLAIM_SCOPE_FIELDS),
        {field: _text() for field in rc1.CLAIM_SCOPE_FIELDS},
    )
    defs: dict[str, Any] = {
        "paper_labels": _object(
            [
                "paper_disposition", "paper_role", "problem_nodes", "intervention_axes",
                "mm_level", "reference_borrow_reproduce", "access_regime",
                "empirical_experiment_present", "agentic_scope",
            ],
            {
                "paper_disposition": _enum(
                    "EMPIRICAL_EXTRACTABLE", "NON_EMPIRICAL_EVIDENCE_ONLY",
                    "INSUFFICIENT_FULLTEXT", "OUT_OF_SCOPE_WITH_REASON", "NOT_CODED",
                ),
                "paper_role": _enum(
                    "DIRECT_METHOD", "INSTRUMENT", "BOUNDARY", "NEGATIVE_OR_FALSIFIER",
                    "TRANSFER_ANALOGUE", "NON_LOAD_BEARING", "NOT_CODED",
                ),
                "problem_nodes": _array(_enum(*PROBLEM_NODES)),
                "intervention_axes": _array(_enum(*INTERVENTION_AXES)),
                "mm_level": _enum(
                    "MM0_TEXT_ONLY", "MM1_MULTIMODAL_CONTEXT", "MM2_MULTIMODAL_ASSET",
                    "MM3_MODALITY_NECESSARY", "UNKNOWN", "NOT_CODED",
                ),
                "reference_borrow_reproduce": _enum(
                    "REFERENCE", "BORROW_PROTOCOL", "REPRODUCTION_CANDIDATE",
                    "NOT_APPLICABLE", "NOT_CODED",
                ),
                "access_regime": _enum(
                    "TF_STRICT_BLACK_BOX", "TF_STRICT_GRAY_BOX", "TRAINED_PARAMETER_UPDATE",
                    "INSTRUMENT_ONLY", "MIXED_OR_UNCLEAR", "NOT_CODED",
                ),
                "empirical_experiment_present": {"type": ["boolean", "null"]},
                "agentic_scope": _object(
                    [
                        "scope_status", "loop_components", "core_dependency",
                        "capability_assets", "control_role", "scope_reason",
                    ],
                    {
                        "scope_status": _enum(*AGENTIC_SCOPE_STATUS),
                        "loop_components": _array(_enum(*LOOP_COMPONENTS)),
                        "core_dependency": _enum(*CORE_DEPENDENCY),
                        "capability_assets": _array(_enum(*CAPABILITY_ASSETS)),
                        "control_role": _enum(*CONTROL_ROLES),
                        "scope_reason": _text(),
                    },
                ),
            },
        ),
        "source_locator": _object(
            ["locator_id", "rendition_id", "anchor_type", "anchor_value", "precise_locator"],
            {
                "locator_id": _text(pattern=r"^LOC-[A-Za-z0-9._:-]+$"),
                "rendition_id": _text(pattern=r"^SRC-[A-Za-z0-9._:-]+$"),
                "anchor_type": _enum("PAGE", "SECTION", "TABLE", "FIGURE", "APPENDIX", "REPOSITORY_FILE"),
                "anchor_value": _text(), "precise_locator": _text(),
            },
        ),
        "run_cell": _object(
            [
                "object_match_key", "run_cell_id", "dataset_node_ids", "model",
                "access_regime", "input_condition", "intervention", "control_signal",
                "primary_intervention_axis", "decision_or_action", "budget_horizon",
                "baseline_role", "source_locator_ids",
            ],
            {
                "object_match_key": match_key, "run_cell_id": _text(pattern=r"^RC-[A-Za-z0-9._:-]+$"),
                "dataset_node_ids": _array(_text(pattern=r"^DS-[A-Za-z0-9._:-]+$")),
                "model": _text(),
                "access_regime": _enum(
                    "TF_STRICT_BLACK_BOX", "TF_STRICT_GRAY_BOX", "TRAINED_PARAMETER_UPDATE",
                    "INSTRUMENT_ONLY", "MIXED_OR_UNCLEAR",
                ),
                "input_condition": _text(), "intervention": _text(),
                "primary_intervention_axis": _enum(*PRIMARY_INTERVENTION_AXES),
                "control_signal": _text(),
                "decision_or_action": _text(), "budget_horizon": _text(),
                "baseline_role": _enum("BASELINE", "INTERVENTION", "ABLATION", "ORACLE_OR_UPPER_BOUND", "OTHER"),
                "source_locator_ids": source_ids,
            },
        ),
        "observation": _object(
            [
                "object_match_key", "observation_id", "run_cell_id", "metric_or_evaluator",
                "outcome_semantics", "raw_result", "observation_role", "source_locator_ids",
            ],
            {
                "object_match_key": match_key,
                "observation_id": _text(pattern=r"^OBS-[A-Za-z0-9._:-]+$"),
                "run_cell_id": _text(pattern=r"^RC-[A-Za-z0-9._:-]+$"),
                "metric_or_evaluator": _text(), "outcome_semantics": _text(), "raw_result": _text(),
                "observation_role": _enum("PRIMARY_OUTCOME", "SECONDARY_OUTCOME", "COST_LATENCY", "DIAGNOSTIC"),
                "source_locator_ids": source_ids,
            },
        ),
        "paired_comparison": _object(
            [
                "object_match_key", "comparison_id", "baseline_cell_id", "intervention_cell_id",
                "paired_status", "comparability_key", "source_locator_ids",
            ],
            {
                "object_match_key": match_key,
                "comparison_id": _text(pattern=r"^PC-[A-Za-z0-9._:-]+$"),
                "baseline_cell_id": _text(pattern=r"^RC-[A-Za-z0-9._:-]+$"),
                "intervention_cell_id": _text(pattern=r"^RC-[A-Za-z0-9._:-]+$"),
                "paired_status": _enum("EXACT_PAIRED", "PARTIAL_PAIRED", "UNPAIRED", "NOT_COMPARABLE"),
                "comparability_key": _object(
                    ["dataset_revision_split", "core_model", "access", "input_condition", "metric", "budget_horizon"],
                    {key: _text() for key in ["dataset_revision_split", "core_model", "access", "input_condition", "metric", "budget_horizon"]},
                ),
                "source_locator_ids": source_ids,
            },
        ),
        "dataset_node": _object(
            ["object_match_key", "dataset_node_id", "name", "revision", "split", "source_locator_ids"],
            {
                "object_match_key": match_key,
                "dataset_node_id": _text(pattern=r"^DS-[A-Za-z0-9._:-]+$"),
                "name": _text(), "revision": _text(), "split": _text(), "source_locator_ids": source_ids,
            },
        ),
        "dataset_edge": _object(
            [
                "object_match_key", "dataset_edge_id", "edge_type", "source_dataset_id",
                "relation", "target_dataset_id", "reason", "source_locator_ids",
            ],
            {
                "object_match_key": match_key,
                "dataset_edge_id": _text(pattern=r"^DE-[A-Za-z0-9._:-]+$"),
                "edge_type": _enum("LINEAGE", "RELATION"),
                "source_dataset_id": _text(pattern=r"^DS-[A-Za-z0-9._:-]+$"),
                "relation": _enum(
                    "SAME_REVISION", "DERIVED_FROM", "SUBSET_OF", "TRANSLATED_FROM",
                    "AUDIO_RENDERING_OF", "REANNOTATED_FROM", "SPLIT_OF",
                    "INDEPENDENT_SAME_TASK", "CROSS_DATASET_VALIDATION",
                    "DISTRIBUTION_SHIFT_TEST", "PROTOCOL_ANALOGUE",
                ),
                "target_dataset_id": _text(pattern=r"^DS-[A-Za-z0-9._:-]+$"),
                "reason": _text(), "source_locator_ids": source_ids,
            },
        ),
        "claim_decision": _object(
            [
                "object_match_key", "claim_decision_id", "claim_template_id",
                "merge_split_decision", "scope", "evidence_relation", "source_locator_ids",
            ],
            {
                "object_match_key": match_key,
                "claim_decision_id": _text(pattern=r"^CD-[A-Za-z0-9._:-]+$"),
                "claim_template_id": _text(pattern=r"^CLM-[A-Z0-9-]+$"),
                "merge_split_decision": _enum(
                    "CREATE_SCOPED_INSTANCE", "LINK_EXISTING_SCOPE_COMPATIBLE_INSTANCE",
                    "SPLIT_REQUIRED", "NO_LINK", "WITHHOLD_UNRESOLVED",
                ),
                "scope": scope,
                "evidence_relation": _enum("SUPPORT", "BOUNDARY", "FALSIFIER", "INSTRUMENT_SUPPORT", "TRANSFER_ANALOGUE", "NONE"),
                "source_locator_ids": source_ids,
            },
        ),
        "compatibility_decision": _object(
            [
                "object_match_key", "decision_id", "decision_type", "target_object_id",
                "compatibility_decision", "reason", "source_locator_ids",
            ],
            {
                "object_match_key": match_key,
                "decision_id": _text(pattern=r"^DEC-[A-Za-z0-9._:-]+$"),
                "decision_type": _enum(
                    "TRANSFER_TRANSLATION", "CORE_MEMBER_COMPATIBILITY",
                    "ACCESS_REGIME_COMPATIBILITY", "CLAIM_EQUIVALENCE",
                ),
                "target_object_id": _text(),
                "compatibility_decision": _enum("COMPATIBLE", "INCOMPATIBLE", "WITHHELD", "NOT_APPLICABLE"),
                "reason": _text(), "source_locator_ids": source_ids,
            },
        ),
        "review_event": _object(
            ["event_id", "event_type", "timestamp", "prior_event_id"],
            {
                "event_id": _text(pattern=r"^REV-[A-Za-z0-9._:-]+$"),
                "event_type": _enum("CODER_SUBMISSION", "ADJUDICATION", "CORRECTION"),
                "timestamp": _text(), "prior_event_id": _text(nullable=True),
            },
        ),
    }
    absence = _object(
        list(CALIBRATED_OBJECT_ARRAYS),
        {
            name: _enum(
                "OBJECTS_PRESENT", "NONE_REPORTED", "NOT_APPLICABLE_NON_EMPIRICAL",
                "WITHHELD_INSUFFICIENT_SOURCE", "NOT_CODED",
            )
            for name in CALIBRATED_OBJECT_ARRAYS
        },
    )
    properties = {
        "schema": {"const": "sf-stage1c-v2-calibration-response-v2"},
        "response_status": _enum("BLANK_NOT_DISTRIBUTED", "CODER_SUBMITTED"),
        "response_id": _text(), "paper_id": _text(), "packet_item_id": _text(),
        "source_manifest_id": _text(), "coder_transaction_id": _text(), "coder_id": _text(),
        "paper_labels": {"$ref": "#/$defs/paper_labels"},
        "run_cells": _array({"$ref": "#/$defs/run_cell"}),
        "observations": _array({"$ref": "#/$defs/observation"}),
        "paired_comparisons": _array({"$ref": "#/$defs/paired_comparison"}),
        "dataset_nodes": _array({"$ref": "#/$defs/dataset_node"}),
        "dataset_edges": _array({"$ref": "#/$defs/dataset_edge"}),
        "claim_decisions": _array({"$ref": "#/$defs/claim_decision"}),
        "translation_or_compatibility_decisions": _array({"$ref": "#/$defs/compatibility_decision"}),
        "source_locators": _array({"$ref": "#/$defs/source_locator"}),
        "object_absence_reasons": absence,
        "review_events": _array({"$ref": "#/$defs/review_event"}),
        "notes": _array(_text()),
    }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "sf-stage1c-v2-calibration-response-schema-v2",
        **_object(list(properties), properties), "$defs": defs,
    }


def count_enum_values(value: Any) -> int:
    if isinstance(value, dict):
        return len(value.get("enum", [])) + sum(count_enum_values(child) for child in value.values())
    if isinstance(value, list):
        return sum(count_enum_values(child) for child in value)
    return 0


def schema_path_exists(schema: dict[str, Any], dotted_path: str) -> bool:
    current: dict[str, Any] = schema
    for part in dotted_path.split("."):
        is_array = part.endswith("[]")
        name = part[:-2] if is_array else part
        properties = current.get("properties", {})
        if name not in properties:
            return False
        current = properties[name]
        if "$ref" in current:
            current = schema["$defs"][current["$ref"].rsplit("/", 1)[1]]
        if is_array:
            current = current.get("items", {})
            if "$ref" in current:
                current = schema["$defs"][current["$ref"].rsplit("/", 1)[1]]
    return True


def build_schema_bundle(response_schema: dict[str, Any]) -> dict[str, Any]:
    paper_id = _text(pattern=r"^(arxiv|acl):[A-Za-z0-9._:-]+$")
    locator_ids = {
        **_array(_text(pattern=r"^LOC-[A-Za-z0-9._:-]+$")),
        "minItems": 1,
    }
    run_cell_id = _text(pattern=r"^RC-[A-Za-z0-9._:-]+$")
    dataset_id = _text(pattern=r"^DS-[A-Za-z0-9._:-]+$")
    claim_scope = _object(
        list(rc1.CLAIM_SCOPE_FIELDS),
        {field: _text() for field in rc1.CLAIM_SCOPE_FIELDS},
    )
    protocol_signature = _object(
        [
            "target_problem_or_failure", "evaluation_object", "outcome_semantics",
            "environment", "interaction_protocol", "access_protocol",
            "baseline_intervention_interpretable",
        ],
        {
            "target_problem_or_failure": _text(),
            "evaluation_object": _text(),
            "outcome_semantics": _text(),
            "environment": _text(),
            "interaction_protocol": _text(),
            "access_protocol": _enum(
                "TF_STRICT_BLACK_BOX", "TF_STRICT_GRAY_BOX", "TRAINED_PARAMETER_UPDATE",
                "INSTRUMENT_ONLY", "MIXED_OR_UNCLEAR",
            ),
            "baseline_intervention_interpretable": {"type": "boolean"},
        },
    )
    defs: dict[str, Any] = {
        "paper_audit": _object(
            [
                "paper_id", "paper_disposition", "paper_role", "source_domain",
                "fulltext_status", "source_locator_ids", "empirical_experiment_present",
                "agentic_scope_status", "agentic_loop_components", "core_dependency",
                "capability_assets", "control_role", "agentic_scope_reason",
                "branch_eligibility", "run_cell_ids", "load_bearing_status",
                "load_bearing_reason", "coder_id", "reviewer_id", "adjudication_status",
            ],
            {
                "paper_id": paper_id,
                "paper_disposition": _enum(
                    "EMPIRICAL_EXTRACTABLE", "NON_EMPIRICAL_EVIDENCE_ONLY",
                    "INSUFFICIENT_FULLTEXT", "OUT_OF_SCOPE_WITH_REASON",
                ),
                "paper_role": _enum(
                    "DIRECT_METHOD", "INSTRUMENT", "BOUNDARY", "NEGATIVE_OR_FALSIFIER",
                    "TRANSFER_ANALOGUE", "NON_LOAD_BEARING",
                ),
                "source_domain": _enum(
                    "SPEECH", "OMNI", "VISION_MULTIMODAL", "TEXT_AGENT", "OTHER_TRANSFER",
                ),
                "fulltext_status": _enum(
                    "PRIMARY_FULLTEXT_VERIFIED", "ALTERNATE_RENDITION_VERIFIED",
                    "INSUFFICIENT_OR_BLOCKED",
                ),
                "source_locator_ids": locator_ids,
                "empirical_experiment_present": {"type": "boolean"},
                "agentic_scope_status": _enum(*AGENTIC_SCOPE_STATUS[:-1]),
                "agentic_loop_components": _array(_enum(*LOOP_COMPONENTS[:-1])),
                "core_dependency": _enum(*CORE_DEPENDENCY[:-1]),
                "capability_assets": _array(_enum(*CAPABILITY_ASSETS[:-1])),
                "control_role": _enum(*CONTROL_ROLES[:-1]),
                "agentic_scope_reason": _text(),
                "branch_eligibility": _enum(
                    "ELIGIBLE_FOR_FAMILY_REVIEW", "REFERENCE_ONLY",
                    "INELIGIBLE_SPECIALIZED_SYSTEM", "INELIGIBLE_TRAINED_CONTROLLER",
                ),
                "run_cell_ids": _array(run_cell_id),
                "load_bearing_status": _enum(
                    "LOAD_BEARING", "RELATION_EVIDENCE", "NON_LOAD_BEARING",
                ),
                "load_bearing_reason": _text(), "coder_id": _text(), "reviewer_id": _text(),
                "adjudication_status": _enum(
                    "NOT_REQUIRED", "PENDING", "ADJUDICATED_ACCEPTED", "ADJUDICATED_REVISED",
                ),
            },
        ),
        "run_cell": _object(
            [
                "run_cell_id", "paper_id", "dataset_node_ids", "model", "access_regime",
                "input_condition", "intervention", "primary_intervention_axis",
                "control_signal", "decision_or_action", "budget_horizon", "baseline_role",
                "source_locator_ids",
            ],
            {
                "run_cell_id": run_cell_id, "paper_id": paper_id,
                "dataset_node_ids": {**_array(dataset_id), "minItems": 1}, "model": _text(),
                "access_regime": _enum(
                    "TF_STRICT_BLACK_BOX", "TF_STRICT_GRAY_BOX", "TRAINED_PARAMETER_UPDATE",
                    "INSTRUMENT_ONLY", "MIXED_OR_UNCLEAR",
                ),
                "input_condition": _text(), "intervention": _text(),
                "primary_intervention_axis": _enum(*PRIMARY_INTERVENTION_AXES),
                "control_signal": _text(),
                "decision_or_action": _text(), "budget_horizon": _text(),
                "baseline_role": _enum(
                    "BASELINE", "INTERVENTION", "ABLATION", "ORACLE_OR_UPPER_BOUND", "OTHER",
                ),
                "source_locator_ids": locator_ids,
            },
        ),
        "observation": _object(
            [
                "observation_id", "run_cell_id", "metric_or_evaluator", "outcome_semantics",
                "raw_result", "observation_role", "source_locator_ids",
            ],
            {
                "observation_id": _text(pattern=r"^OBS-[A-Za-z0-9._:-]+$"),
                "run_cell_id": run_cell_id, "metric_or_evaluator": _text(),
                "outcome_semantics": _text(), "raw_result": _text(),
                "observation_role": _enum(
                    "PRIMARY_OUTCOME", "SECONDARY_OUTCOME", "COST_LATENCY", "DIAGNOSTIC",
                ),
                "source_locator_ids": locator_ids,
            },
        ),
        "paired_comparison": _object(
            [
                "comparison_id", "baseline_cell_id", "intervention_cell_id", "paired_status",
                "comparability_key", "source_locator_ids",
            ],
            {
                "comparison_id": _text(pattern=r"^PC-[A-Za-z0-9._:-]+$"),
                "baseline_cell_id": run_cell_id, "intervention_cell_id": run_cell_id,
                "paired_status": _enum(
                    "EXACT_PAIRED", "PARTIAL_PAIRED", "UNPAIRED", "NOT_COMPARABLE",
                ),
                "comparability_key": _object(
                    [
                        "dataset_revision_split", "core_model", "access", "input_condition",
                        "metric", "budget_horizon",
                    ],
                    {
                        key: _text() for key in [
                            "dataset_revision_split", "core_model", "access", "input_condition",
                            "metric", "budget_horizon",
                        ]
                    },
                ),
                "source_locator_ids": locator_ids,
            },
        ),
        "dataset_node": _object(
            ["dataset_id", "name", "revision", "split", "source_locator_ids"],
            {
                "dataset_id": dataset_id, "name": _text(), "revision": _text(),
                "split": _text(), "source_locator_ids": locator_ids,
            },
        ),
        "dataset_lineage_edge": _object(
            [
                "edge_id", "source_dataset_id", "relation", "target_dataset_id",
                "source_locator_ids",
            ],
            {
                "edge_id": _text(pattern=r"^DL-[A-Za-z0-9._:-]+$"),
                "source_dataset_id": dataset_id,
                "relation": _enum(
                    "SAME_REVISION", "DERIVED_FROM", "SUBSET_OF", "TRANSLATED_FROM",
                    "AUDIO_RENDERING_OF", "REANNOTATED_FROM", "SPLIT_OF",
                ),
                "target_dataset_id": dataset_id, "source_locator_ids": locator_ids,
            },
        ),
        "dataset_relation_edge": _object(
            [
                "edge_id", "source_dataset_id", "relation", "target_dataset_id", "reason",
                "source_locator_ids",
            ],
            {
                "edge_id": _text(pattern=r"^DR-[A-Za-z0-9._:-]+$"),
                "source_dataset_id": dataset_id,
                "relation": _enum(
                    "INDEPENDENT_SAME_TASK", "CROSS_DATASET_VALIDATION",
                    "DISTRIBUTION_SHIFT_TEST", "PROTOCOL_ANALOGUE",
                ),
                "target_dataset_id": dataset_id, "reason": _text(),
                "source_locator_ids": locator_ids,
            },
        ),
        "claim_record": _object(
            [
                "claim_id", "object_type", "claim_text", "claim_origin", "scope",
                "evidence_relation", "evidence_state", "project_status", "source_locator_ids",
            ],
            {
                "claim_id": _text(pattern=r"^CLM-[A-Za-z0-9._:-]+$"),
                "object_type": _enum("SCOPED_CLAIM_INSTANCE"), "claim_text": _text(),
                "claim_origin": _enum(
                    "PAPER_STATED", "FAMILY_SYNTHESIS", "BOUNDARY_OR_FALSIFIER",
                    "MEASUREMENT_CONTRACT",
                ),
                "scope": claim_scope,
                "evidence_relation": _enum(
                    "SUPPORT", "BOUNDARY", "FALSIFIER", "INSTRUMENT_SUPPORT",
                    "TRANSFER_ANALOGUE",
                ),
                "evidence_state": _enum(
                    "DIRECTLY_SUPPORTED", "PARTIALLY_SUPPORTED", "CONTRADICTED",
                    "INSUFFICIENT_EVIDENCE",
                ),
                "project_status": _enum(
                    "PAPER_CLAIM_ONLY", "RESIDUAL_HYPOTHESIS_NOT_NOVELTY_VERDICT",
                ),
                "source_locator_ids": locator_ids,
            },
        ),
        "family_record": _object(
            [
                "family_id", "problem_statement", "protocol_signature", "evidence_state",
                "strongest_contradiction", "uncertainty", "residual_hypothesis",
                "alternative_explanation", "kill_criterion", "local_readiness", "h5_status",
            ],
            {
                "family_id": _text(pattern=r"^FAM-[A-Za-z0-9._:-]+$"),
                "problem_statement": _text(), "protocol_signature": protocol_signature,
                "evidence_state": _enum(
                    "CONSISTENT_SUPPORT", "MIXED", "NULL_OR_NEGATIVE",
                    "INSUFFICIENT_EVIDENCE",
                ),
                "strongest_contradiction": _text(), "uncertainty": _text(),
                "residual_hypothesis": _text(), "alternative_explanation": _text(),
                "kill_criterion": _text(),
                "local_readiness": _enum(
                    "LOCAL_READY", "LOCAL_ADAPTABLE", "BLOCKED_ASSET_OR_TERMS",
                    "TRANSFER_ONLY",
                ),
                "h5_status": _enum(
                    "NOT_H5_DEPENDENT", "H5_DEPENDENT_WITHHELD", "H5_CLOSED_EVIDENCE_BOUND",
                ),
            },
        ),
        "family_membership": _object(
            [
                "membership_id", "family_id", "evidence_object_id", "membership_type",
                "compatibility_decision", "compatibility_reason", "review_status",
            ],
            {
                "membership_id": _text(pattern=r"^FM-[A-Za-z0-9._:-]+$"),
                "family_id": _text(pattern=r"^FAM-[A-Za-z0-9._:-]+$"),
                "evidence_object_id": _text(),
                "membership_type": _enum(
                    "CORE_MEMBER", "VALIDATION_MEMBER", "TRANSFER_ANALOGUE", "FALSIFIER",
                    "INSTRUMENT_SUPPORT",
                ),
                "compatibility_decision": _enum(
                    "COMPATIBLE", "INCOMPATIBLE_RELATION_ONLY", "WITHHELD_PENDING_ADJUDICATION",
                ),
                "compatibility_reason": _text(),
                "review_status": _enum("PENDING_REVIEW", "REVIEWED_ACCEPTED", "ADJUDICATED"),
            },
        ),
        "review_event": _object(
            ["event_id", "object_id", "actor_id", "event_type", "timestamp", "prior_event_id"],
            {
                "event_id": _text(pattern=r"^REV-[A-Za-z0-9._:-]+$"), "object_id": _text(),
                "actor_id": _text(),
                "event_type": _enum(
                    "CODER_SUBMISSION", "BLIND_REVIEW", "ADJUDICATION", "CORRECTION",
                ),
                "timestamp": _text(), "prior_event_id": _text(nullable=True),
            },
        ),
        "translation_contract": _object(
            [
                "translation_id", "source_work_id", "source_domain", "borrowed_decision_structure",
                "source_to_target_changes", "speech_omni_corresponding_variable",
                "strongest_transfer_failure", "rejection_observation", "transfer_status",
                "source_locator_ids",
            ],
            {
                "translation_id": _text(pattern=r"^TR-[A-Za-z0-9._:-]+$"),
                "source_work_id": _text(pattern=r"^CW-[A-Za-z0-9._:-]+$"),
                "source_domain": _enum("VISION_MULTIMODAL_AGENT", "TEXT_AGENT", "OTHER_DOMAIN"),
                "borrowed_decision_structure": _text(),
                "source_to_target_changes": {**_array(_text()), "minItems": 1},
                "speech_omni_corresponding_variable": _text(),
                "strongest_transfer_failure": _text(), "rejection_observation": _text(),
                "transfer_status": _enum(
                    "WITHHELD_PENDING_TRANSLATION", "TRANSLATED_FOR_FAMILY_REVIEW",
                    "REJECTED_NON_ISOMORPHIC",
                ),
                "source_locator_ids": locator_ids,
            },
        ),
    }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "sf-stage1c-v2-schema-bundle-v2",
        "calibration_response_schema_id": response_schema["$id"],
        "specialized_system_branch_gate": "SPECIALIZED_SYSTEM_EXCLUSION_CANNOT_ENTER_CORE_MEMBER_OR_BRANCH_PRIMARY",
        "$defs": defs,
        "note": "Typed full-mapping schemas remain pre-execution; the response schema is the sole calibration coder contract.",
    }


def _data_root() -> Path:
    raw = os.environ.get(
        "SPEECHRL_DATA_DIR", "E:/chao_workspace/exploring-l4-intelligence/speechrl-data"
    )
    return Path(resolve_asset_path(raw, "nt" if os.name == "nt" else "posix"))


def _portable(identity: str, suffix: str) -> str:
    return f"${{SPEECHRL_DATA_DIR}}/survey-fulltext/{identity}/{identity}.{suffix}"


def _resolve_portable(locator: str) -> Path:
    prefix = "${SPEECHRL_DATA_DIR}/"
    if not locator.startswith(prefix):
        raise ContractError(f"non-portable source locator: {locator}")
    return _data_root() / locator.removeprefix(prefix)


def _ledger_rows() -> tuple[list[dict[str, Any]], dict[tuple[str, str, str], tuple[int, dict[str, Any]]]]:
    rows = [json.loads(line) for line in LEDGER.read_text(encoding="utf-8").splitlines() if line.strip()]
    indexed = {
        (str(row.get("arxiv_id")), str(row.get("kind")), str(row.get("sha256"))): (line_no, row)
        for line_no, row in enumerate(rows, 1) if row.get("sha256")
    }
    return rows, indexed


def _source_revision(canonical_id: str, pdf_path: Path, text_path: Path | None) -> str:
    if canonical_id.startswith("arxiv:"):
        identity = canonical_id.split(":", 1)[1]
        if text_path and text_path.is_file():
            text = text_path.read_text(encoding="utf-8", errors="replace")[:12000]
        else:
            from pypdf import PdfReader

            text = (PdfReader(str(pdf_path)).pages[0].extract_text() or "")[:12000]
        match = re.search(rf"arXiv:{re.escape(identity)}v(\d+)", text, re.IGNORECASE)
        if not match:
            raise ContractError(f"arXiv version missing from extracted text: {canonical_id}")
        return f"arXiv:{identity}v{match.group(1)}"
    return f"ACL_ANTHOLOGY_PUBLICATION_VERSION:{canonical_id.split(':', 1)[1]}"


def build_source_manifest(calibration_ids: list[str]) -> dict[str, Any]:
    _, ledger = _ledger_rows()
    items = []
    for canonical_id in calibration_ids:
        identity = canonical_id.split(":", 1)[1]
        base = _data_root() / "survey-fulltext" / identity
        pdf, text = base / f"{identity}.pdf", base / f"{identity}.txt"
        if not pdf.is_file():
            raise ContractError(f"missing primary source bytes: {canonical_id}")
        pdf_hash = sha256_path(pdf)
        ledger_key = (identity, "pdf", pdf_hash)
        if ledger_key in ledger:
            line_no, row = ledger[ledger_key]
            binding: dict[str, Any] = {
                "receipt_type": "FULLTEXT_LEDGER_ROW", "ledger_path": LEDGER.relative_to(REPO).as_posix(),
                "line": line_no, "fetched_at": row["time_utc"], "source_url": row["url"],
            }
        elif canonical_id.startswith("acl:"):
            binding = {
                "receipt_type": "RC2_LOCAL_SOURCE_RECEIPT",
                "source_url": f"https://aclanthology.org/{identity}.pdf",
                "receipt_basis": "EXACT_LOCAL_BYTES_AND_OFFICIAL_PUBLICATION_ID",
            }
        else:
            raise ContractError(f"PDF has no matching source receipt: {canonical_id}")
        alternates = []
        if text.is_file():
            alternates.append({
                "rendition_id": f"SRC-{identity}-TXT", "kind": "EXTRACTED_TEXT",
                "locator": _portable(identity, "txt"), "bytes": text.stat().st_size,
                "sha256": sha256_path(text), "derived_from_sha256": pdf_hash,
            })
        eprint = base / f"{identity}.eprint"
        if eprint.is_file():
            eprint_hash = sha256_path(eprint)
            eprint_binding = ledger.get((identity, "eprint", eprint_hash))
            alternate = {
                "rendition_id": f"SRC-{identity}-EPRINT", "kind": "EPRINT_SOURCE",
                "locator": _portable(identity, "eprint"), "bytes": eprint.stat().st_size,
                "sha256": eprint_hash,
            }
            if eprint_binding:
                alternate["ledger_line"] = eprint_binding[0]
            alternates.append(alternate)
        available_priority = ["PDF"] + [
            kind for kind in ("EPRINT_SOURCE", "EXTRACTED_TEXT")
            if any(row["kind"] == kind for row in alternates)
        ]
        items.append({
            "source_item_id": f"SRC-{identity}", "canonical_id": canonical_id,
            "source_revision": _source_revision(canonical_id, pdf, text if text.is_file() else None), "primary_rendition": {
                "rendition_id": f"SRC-{identity}-PDF", "kind": "PDF",
                "locator": _portable(identity, "pdf"), "bytes": pdf.stat().st_size, "sha256": pdf_hash,
            },
            "alternate_renditions": alternates, "ledger_binding": binding,
            "rendition_priority": available_priority,
        })
    return {
        "schema": "sf-stage1c-v2-calibration-source-byte-manifest-v2",
        "artifact_id": "SF-STAGE1C-V2-CALIBRATION-SOURCE-BYTES-56-RC2",
        "N": len(items), "status": "EXACT_BYTES_BOUND_NOT_DISTRIBUTED", "items": items,
    }


def verify_source_manifest(manifest: dict[str, Any]) -> bool:
    for item in manifest["items"]:
        for rendition in [item["primary_rendition"], *item["alternate_renditions"]]:
            path = _resolve_portable(rendition["locator"])
            if not path.is_file() or path.stat().st_size != rendition["bytes"]:
                return False
            if sha256_path(path) != rendition["sha256"]:
                return False
    return True


def _blank_response(canonical_id: str, packet_item_id: str, source_manifest_id: str) -> dict[str, Any]:
    return {
        "schema": "sf-stage1c-v2-calibration-response-v2",
        "response_status": "BLANK_NOT_DISTRIBUTED", "response_id": "PENDING",
        "paper_id": canonical_id, "packet_item_id": packet_item_id,
        "source_manifest_id": source_manifest_id,
        "coder_transaction_id": "PENDING", "coder_id": "PENDING",
        "paper_labels": {
            "paper_disposition": "NOT_CODED", "paper_role": "NOT_CODED",
            "problem_nodes": ["NOT_CODED"], "intervention_axes": ["NOT_CODED"],
            "mm_level": "NOT_CODED", "reference_borrow_reproduce": "NOT_CODED",
            "access_regime": "NOT_CODED", "empirical_experiment_present": None,
            "agentic_scope": {
                "scope_status": "NOT_CODED", "loop_components": ["NOT_CODED"],
                "core_dependency": "NOT_CODED", "capability_assets": ["NOT_CODED"],
                "control_role": "NOT_CODED", "scope_reason": "PENDING",
            },
        },
        **{name: [] for name in CALIBRATED_OBJECT_ARRAYS},
        "source_locators": [],
        "object_absence_reasons": {name: "NOT_CODED" for name in CALIBRATED_OBJECT_ARRAYS},
        "review_events": [], "notes": [],
    }


def build_agentic_calibration(
    bootstrap: dict[str, Any], surfaces: dict[str, Any],
) -> dict[str, Any]:
    calibration, _ = rc1.build_calibration(bootstrap, surfaces)
    removed_id = "arxiv:2604.04847"
    replacement = {
        "canonical_id": "arxiv:2512.23646",
        "selection_rationale": "active-perception observe-memory-reflect-replan-act calibration coverage",
    }
    if removed_id not in calibration["canonical_ids"]:
        raise ContractError("FDB-v3 sentinel is missing from the inherited RC1 calibration")
    if replacement["canonical_id"] in calibration["canonical_ids"]:
        raise ContractError("Active Perception Agent unexpectedly overlaps the inherited sample")
    canonical_ids = [
        replacement["canonical_id"] if canonical_id == removed_id else canonical_id
        for canonical_id in calibration["canonical_ids"]
    ]
    sentinels = [
        replacement if row["canonical_id"] == removed_id else row
        for row in calibration["inherited_sentinels"]
    ]
    if len(canonical_ids) != 56 or len(set(canonical_ids)) != 56:
        raise ContractError("agentic calibration replacement changed N or introduced a duplicate")
    if len(calibration["overlay_ids"]) != 38 or len(sentinels) != 18:
        raise ContractError("agentic calibration replacement changed overlay/sentinel denominators")
    return {
        **calibration,
        "canonical_ids": canonical_ids,
        "inherited_sentinels": sentinels,
        "agentic_scope_correction": {
            "removed_sentinel": removed_id,
            "replacement_sentinel": replacement["canonical_id"],
            "duplex_boundary_retained": "arxiv:2510.07838",
        },
    }


def build_calibration_artifacts(
    bootstrap: dict[str, Any], source_manifest: dict[str, Any], response_schema: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    surfaces = rc1.source_surfaces()
    rc1_calibration = build_agentic_calibration(bootstrap, surfaces)
    titles = {row["canonical_id"]: row["title"] for row in bootstrap["works"]}
    titles.update(rc1.CALIBRATION_ONLY_TITLES)
    source_by_id = {row["canonical_id"]: row for row in source_manifest["items"]}
    items = []
    for canonical_id in rc1_calibration["canonical_ids"]:
        identity = canonical_id.split(":", 1)[1]
        packet_id = f"CAL-{identity}"
        source = source_by_id[canonical_id]
        items.append({
            "packet_item_id": packet_id, "canonical_id": canonical_id, "title": titles[canonical_id],
            "source_item_id": source["source_item_id"],
            "source_revision": source["source_revision"],
            "primary_rendition_sha256": source["primary_rendition"]["sha256"],
            "blank_response": _blank_response(canonical_id, packet_id, source_manifest["artifact_id"]),
        })
    calibration = {
        **rc1_calibration,
        "schema": "sf-stage1c-v2-calibration-manifest-v2",
        "artifact_id": "SF-STAGE1C-V2-CALIBRATION-PACKET-56-RC2",
        "status": "AGENTIC_RC2_CODER_READY_NOT_DISTRIBUTED",
        "source_byte_manifest_id": source_manifest["artifact_id"],
        "calibration_response_schema_id": response_schema["$id"],
        "object_level_extraction_required_for_empirical_works": True,
        "empty_object_arrays_require_reason": True,
    }
    packet = {
        "schema": "sf-stage1c-v2-calibration-blind-packet-v2",
        "artifact_id": "SF-STAGE1C-V2-LABEL-HIDDEN-PACKET-56-RC2",
        "purpose": "LABEL_HIDDEN_PAPER_AND_OBJECT_LEVEL_CALIBRATION_INPUT",
        "status": "PREPARED_NOT_DISTRIBUTED", "contains_prior_labels": False,
        "repository_access_should_be_withheld": True,
        "calibration_response_schema_id": response_schema["$id"],
        "source_byte_manifest_id": source_manifest["artifact_id"], "items": items,
    }
    return calibration, packet


def build_claim_templates() -> dict[str, Any]:
    prior = rc1.build_claim_registry(rc1.source_surfaces())
    templates = []
    for row in prior["claims"]:
        templates.append({
            "claim_template_id": row["claim_id"], "object_type": "CLAIM_TEMPLATE",
            "synthesis_question": row["claim_text"], "origin_work_ids": row["origin_work_ids"],
            "template_scope": row["scope"], "load_bearing": False,
            "scoped_instance_creation_status": "CALIBRATION_NOT_EXECUTED",
        })
    links = [
        {
            "canonical_work_id": row["canonical_work_id"],
            "claim_template_id": row["claim_id"], "evidence_relation": row["evidence_relation"],
            "load_bearing_before_scoped_instance_review": False,
        }
        for row in prior["paper_to_claim_links"]
    ]
    return {
        "schema": "sf-stage1c-v2-claim-template-registry-v2",
        "artifact_id": "SF-STAGE1C-V2-CLAIM-TEMPLATES-13-RC2",
        "claim_templates": templates, "scoped_claim_instances": [],
        "paper_to_template_links": links,
        "scoped_instance_merge_rule": "MERGE_ONLY_SCOPE_COMPATIBLE_AND_PROPOSITION_EQUIVALENT_INSTANCES",
        "paper_link_counts_are_support_votes": False,
    }


def build_assignment_manifest(
    calibration: dict[str, Any], blind_packet: dict[str, Any],
) -> dict[str, Any]:
    """Build the label-hidden assignment view without sampling provenance."""
    return {
        "schema": "sf-stage1c-v2-calibration-assignment-manifest-v2",
        "artifact_id": "SF-STAGE1C-V2-LABEL-HIDDEN-ASSIGNMENT-56-RC2",
        "status": "LABEL_HIDDEN_ASSIGNMENT_BYTES_PREPARED_NOT_DISTRIBUTED",
        "N": calibration["N"],
        "sample_role_hidden": True,
        "items": [
            {
                "packet_item_id": row["packet_item_id"],
                "source_item_id": row["source_item_id"],
                "source_revision": row["source_revision"],
                "primary_rendition_sha256": row["primary_rendition_sha256"],
            }
            for row in blind_packet["items"]
        ],
    }


def build_claim_template_coder_view(claim_templates: dict[str, Any]) -> dict[str, Any]:
    """Expose neutral synthesis questions without prior paper-to-claim bindings."""
    return {
        "schema": "sf-stage1c-v2-claim-template-coder-view-v2",
        "artifact_id": "SF-STAGE1C-V2-CLAIM-TEMPLATE-CODER-VIEW-13-RC2",
        "status": "NEUTRAL_TEMPLATE_VIEW_PREPARED_NOT_DISTRIBUTED",
        "claim_templates": [
            {
                "claim_template_id": row["claim_template_id"],
                "object_type": row["object_type"],
                "synthesis_question": row["synthesis_question"],
                "template_scope": row["template_scope"],
            }
            for row in claim_templates["claim_templates"]
        ],
        "paper_links_included": False,
        "prior_support_labels_included": False,
    }


def build_coder_codebook(response_schema: dict[str, Any]) -> dict[str, Any]:
    """Build a paper-neutral codebook; named adjudication guidance stays reviewer-only."""
    return {
        "schema": "sf-stage1c-v2-coder-codebook-v2",
        "artifact_id": "SF-STAGE1C-V2-NEUTRAL-CODER-CODEBOOK-RC2",
        "status": "DEIDENTIFIED_RULES_PREPARED_NOT_DISTRIBUTED",
        "calibration_response_schema_id": response_schema["$id"],
        "rules": [
            "Code only from the supplied source bytes and record an exact source locator.",
            "DIRECT_AGENTIC requires both DECIDE and ACT_OR_TOOL in an observable loop using a GENERIC_FROZEN_CORE.",
            "A specialized-model dependency is an out-of-scope specialized-system reference, not a direct method.",
            "A trained controller cannot pass the direct training-free agentic gate.",
            "Create a run cell only for an empirical run configuration; do not fabricate cells for non-empirical evidence.",
            "Treat multiple metrics from one run as observations, not duplicate run cells.",
            "Assert dataset lineage only with provenance evidence; otherwise use a non-lineage dataset relation.",
            "REFERENCE transfers neither protocol nor result; BORROW_PROTOCOL requires translation and a rejection observation.",
            "REPRODUCTION requires task, dataset revision, entrypoint, access, license, and evaluator closure.",
            "Use final absence reasons for empty object arrays and retain UNKNOWN when the source does not resolve a field.",
        ],
        "named_paper_expectations_included": False,
        "prior_labels_included": False,
    }


def _scan_forbidden_keys(value: Any, *, path: str = "$") -> list[str]:
    leaks: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key in CODER_DISTRIBUTION_FORBIDDEN_KEYS:
                leaks.append(f"FORBIDDEN_KEY:{child_path}")
            leaks.extend(_scan_forbidden_keys(child, path=child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            leaks.extend(_scan_forbidden_keys(child, path=f"{path}[{index}]"))
    return leaks


def scan_coder_bundle_leaks(
    package: dict[str, Any], artifact_names: tuple[str, ...] | list[str],
) -> list[str]:
    """Recursively reject prior labels, governance links, and named expectations."""
    leaks: list[str] = []
    names = tuple(artifact_names)
    if names != CODER_DISTRIBUTION_ALLOWED_ARTIFACTS:
        leaks.append(f"ARTIFACT_ALLOWLIST_MISMATCH:{names!r}")
    for name in names:
        if name not in package:
            leaks.append(f"MISSING_ARTIFACT:{name}")
            continue
        leaks.extend(
            f"{name}:{finding}" for finding in _scan_forbidden_keys(package[name])
        )
    for name in ("coder_codebook", "claim_template_coder_view"):
        if name not in package:
            continue
        text = json_bytes(package[name]).decode("utf-8").casefold()
        for forbidden in CODER_VIEW_FORBIDDEN_NAMED_EXPECTATIONS:
            if forbidden.casefold() in text:
                leaks.append(f"NAMED_EXPECTATION:{name}:{forbidden}")
    return leaks


def build_agreement(response_schema: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "sf-stage1c-v2-agreement-contract-v2",
        "artifact_id": "SF-STAGE1C-V2-AGREEMENT-CONTRACT-RC2",
        "calibration_response_schema_id": response_schema["$id"],
        "minimum_gate_value": 0.85,
        "critical_response_paths": [
            "paper_labels.paper_disposition", "paper_labels.paper_role",
            "paper_labels.problem_nodes", "paper_labels.intervention_axes",
            "paper_labels.mm_level", "paper_labels.reference_borrow_reproduce",
            "paper_labels.access_regime", "paper_labels.empirical_experiment_present",
            "paper_labels.agentic_scope.scope_status",
            "paper_labels.agentic_scope.loop_components",
            "paper_labels.agentic_scope.core_dependency",
            "paper_labels.agentic_scope.capability_assets",
            "paper_labels.agentic_scope.control_role",
            "run_cells[].object_match_key", "run_cells[].access_regime",
            "run_cells[].primary_intervention_axis",
            "paired_comparisons[].paired_status", "dataset_edges[].relation",
            "claim_decisions[].merge_split_decision",
            "translation_or_compatibility_decisions[].compatibility_decision",
        ],
        "single_label_gate_metric": "EXACT_RAW_AGREEMENT_PER_FIELD",
        "multilabel_gate_metric": "EXACT_SET_MATCH",
        "multilabel_diagnostics": ["JACCARD", "MICRO_F1", "MACRO_F1"],
        "object_matching_rule": "EXACT_OBJECT_MATCH_KEY_WITHIN_PAPER_AND_TYPE",
        "object_segmentation_gate_metric": "MICRO_F1",
        "matched_object_field_gate_metric": "RAW_AGREEMENT_PER_CRITICAL_FIELD",
        "unknown_denominator_rule": "INCLUDE_AS_VALID_LABEL",
        "not_applicable_denominator_rule": "EXCLUDE_ONLY_WHEN_BOTH_CODERS_SELECT_NOT_APPLICABLE",
        "unilateral_not_applicable_rule": "INCLUDE_AS_DISAGREEMENT",
        "zero_positive_category_status": "NOT_CALIBRATED",
        "not_calibrated_full_mapping_rule": "TARGETED_CALIBRATION_OR_100_PERCENT_SECOND_REVIEW",
        "pre_adjudication_results_must_be_published": True,
        "all_disagreements_adjudicated": True,
        "maximum_codebook_consolidations": 1,
        "full_packet_recode_after_consolidation": True,
        "second_round_failure_action": "STOP_AND_RETURN_TO_INDEPENDENT_REVIEW",
        "later_full_mapping_blind_review": {
            "minimum_unique_works": 64, "exclude_calibration_records": True,
            "status": "WITHHELD_UNTIL_FRESH_FULL_MAPPING_SIGNATURE",
        },
    }


def build_coder_transaction(response_schema: dict[str, Any]) -> dict[str, Any]:
    slot = {
        "assignment_status": "UNASSIGNED", "actor_type": None, "actor_identity": None,
        "model_provider": None, "model_name": None, "model_version": None,
        "sampling_configuration": None, "prior_exposure_declaration": None,
        "start_time": None, "submit_time": None, "process_or_task_id": None,
        "expected_content_bundle_sha256": None,
    }
    return {
        "schema": "sf-stage1c-v2-coder-transaction-contract-v2",
        "artifact_id": "SF-STAGE1C-V2-CODER-INTAKE-RC2",
        "status": "PREPARED_NOT_DISTRIBUTED", "distribution_authorized": False,
        "distribution_manifest_id": "SF-STAGE1C-V2-CALIBRATION-DISTRIBUTION-RC2",
        "calibration_response_schema_id": response_schema["$id"],
        "coder_slots": [
            {
                "coder_slot": "A", "planned_model": "gpt-5.6-sol",
                "planned_execution_mode": "INDEPENDENT_CODEX_PROCESS",
                "planned_context": "FRESH_NO_FORK",
                "planned_workspace": "CODER_ONLY_NO_GIT",
                **slot,
            },
            {
                "coder_slot": "B", "planned_model": "gpt-5.6-terra",
                "planned_execution_mode": "INDEPENDENT_CODEX_PROCESS",
                "planned_context": "FRESH_NO_FORK",
                "planned_workspace": "CODER_ONLY_NO_GIT",
                **slot,
            },
        ],
        "required_exposure_declaration": [
            "prior_records", "claim_links", "problem_routes", "repository", "prior_discussion",
            "foundation_model_training_corpus_unknown",
        ],
        "isolation": {
            "same_label_hidden_packet": True, "repository_access_withheld": True,
            "network_discovery_withheld": True, "prior_label_access_withheld": True,
            "coder_communication_prohibited_from_distribution_until_both_submissions": True,
        },
        "same_model_runs_are_not_automatically_independent": True,
        "independence_acceptance_rule": "DISTINCT_PLANNED_MODEL_CONFIGS_PLUS_ISOLATED_CONTEXT_PROCESS_WORKSPACE_AND_EXPOSURE_DISCLOSURE",
        "independence_claim_scope": "TWO_ISOLATED_MODEL_CODERS_NOT_PROVIDER_INDEPENDENT_OR_HUMAN_INTERRATER_INDEPENDENCE",
        "provider_independent_claim": False,
        "human_interrater_independence_claim": False,
        "adjudicator": {
            "requirement": "HUMAN_DOMAIN_EXPERT_REQUIRED", "assignment_status": "UNASSIGNED",
            "identity": None, "planned_role": "OWNER_HUMAN_DOMAIN_EXPERT",
            "blind_adjudication_claim_prohibited": True,
            "full_prior_exposure_disclosure_required": True,
            "visible_information_must_be_declared": True,
            "load_bearing_disagreements": [
                "REPRODUCTION", "DATASET_LINEAGE", "MM3", "EXACT_PAIRED",
                "TF_STRICT_ACCESS", "CORE_MEMBER", "CLAIM_MERGE_SPLIT",
                "AGENTIC_SCOPE", "PRIMARY_INTERVENTION_ATTRIBUTION",
            ],
        },
        "distribution_preconditions": [
            "TWO_CODER_SLOTS_ASSIGNED", "HUMAN_DOMAIN_EXPERT_ADJUDICATOR_ASSIGNED",
            "EXPOSURE_DECLARATIONS_COMPLETE", "EXACT_DISTRIBUTION_MANIFEST_HASH_FROZEN",
            "INDEPENDENT_RC2_REVIEW_ACCEPTS_METHOD_CONTRACT",
        ],
    }


def _paper_source_revision(work_id: str) -> str:
    identity = work_id.removeprefix("CW-ARXIV-")
    base = _data_root() / "survey-fulltext" / identity
    pdf, text = base / f"{identity}.pdf", base / f"{identity}.txt"
    return _source_revision(
        f"arxiv:{identity}", pdf, text if text.is_file() else None,
    )


def _readiness_row(
    *, order: int, work_id: str, title: str, status: str, relation: str,
    capability_assets: list[str], official_sources: list[str], license_status: str,
    dataset_or_protocol: str, entrypoints: list[str], access_state: str,
    evaluator_contract: str, local_state: str, specialized_model_dependency: str,
    strongest_blocker: str, deviation_ledger: list[str],
    source_to_target_translation: str, rejection_condition: str,
    official_repo_revision: str | None = None,
    read_only_closure_status: str = "EVIDENCE_BOUND_WITH_BLOCKERS",
    method_anchor_eligible: bool = False,
) -> dict[str, Any]:
    return {
        "closure_order": order, "canonical_work_id": work_id, "title": title,
        "status": status, "project_relation": relation,
        "capability_assets": capability_assets,
        "read_only_closure_status": read_only_closure_status,
        "method_anchor_eligible": method_anchor_eligible,
        "reproduction_eligible": method_anchor_eligible,
        "official_sources": official_sources,
        "source_revision": _paper_source_revision(work_id),
        "official_repo_revision": official_repo_revision,
        "license": license_status, "dataset_or_protocol": dataset_or_protocol,
        "entrypoints": entrypoints, "access_state": access_state,
        "evaluator_contract": evaluator_contract, "local_state": local_state,
        "specialized_model_dependency": specialized_model_dependency,
        "strongest_blocker": strongest_blocker, "deviation_ledger": deviation_ledger,
        "source_to_target_translation": source_to_target_translation,
        "rejection_condition": rejection_condition,
        "research_execution_performed": False,
    }


def build_reproduction_readiness() -> dict[str, Any]:
    candidates = [
        _readiness_row(
            order=1, work_id="CW-ARXIV-2509.16971",
            title="AudioGenie-Reasoner", status="CANDIDATE_NOT_ANCHOR",
            relation="DIRECT_METHOD_PRIMARY_CANDIDATE",
            capability_assets=["KNOWLEDGE", "SKILL", "MEMORY"],
            official_sources=[
                "https://github.com/ryysayhi/AudioGenie-Reasoner",
                "https://arxiv.org/abs/2509.16971",
            ],
            official_repo_revision="b80c9ce80b3f7f93241f4d8805ad84f8fbc76e73",
            license_status="MIT", dataset_or_protocol="MMAU-mini and MMAR audio reasoning",
            entrypoints=[
                "scripts/run_reasoner.py", "audio_reasoner/orchestration/orchestrator.py",
                "audio_reasoner/augmentation/runner.py",
            ],
            access_state="LOCAL_PINNED_CODE; REMOTE_OPENAI_COMPATIBLE_PLANNER_AND_MODEL_ASSETS_REQUIRED",
            evaluator_contract="TASK_ANSWER_EXACTNESS_OR_ACCURACY_PER_DATASET; NOT_RUN",
            local_state="LOCAL_REPO_PINNED; MMAU_MINI_AND_MMAR_REVISION_PINNED",
            specialized_model_dependency="NO_DUPLEX_CORE; AUDIO_CAPTIONER_WHISPER_AND_REMOTE_PLANNER_REQUIRED",
            strongest_blocker="Dependency/model/tool revisions and remote planner endpoint are not fully locked; dataset adapters and evaluator invocation are not yet closed.",
            deviation_ledger=[
                "Candidate closure is source inspection only.",
                "Sufficiency/retry/stop is training-free non-reward control unless an explicit reward is coded.",
                "A candidate is not an anchor and no reported result was reproduced.",
            ],
            source_to_target_translation="DIRECT_SPEECH_AUDIO_METHOD; NO_CROSS_DOMAIN_TRANSLATION_REQUIRED",
            rejection_condition="Reject as anchor if the task-matched entrypoint, frozen access, evaluator, or dependency lock cannot be closed without method redesign.",
        ),
        _readiness_row(
            order=2, work_id="CW-ARXIV-2510.02995", title="AudioToolAgent",
            status="CANDIDATE_NOT_ANCHOR", relation="TASK_MATCHED_NEAREST_PRIOR",
            capability_assets=["SKILL"],
            official_sources=[
                "https://github.com/GLJS/AudioToolAgent",
                "https://arxiv.org/abs/2510.02995",
            ],
            official_repo_revision="00e1bdcbd646202b42409cc4c1524ead2680dcb7",
            license_status="NO_LICENSE_FILE_DETECTED_AT_OFFICIAL_HEAD",
            dataset_or_protocol="MMAU, MMAR and MMAU-Pro; closed/open agent configurations",
            entrypoints=[
                "main.py", "scripts/launch_closed.sh", "scripts/launch_open.sh",
                "Evaluation/MMAR_Closed.py", "Evaluation/MMAU_Closed.py",
                "audiotoolagent/agent.py",
            ],
            access_state="PUBLIC_CODE; MIXED_LOCAL_MODELS_AND_VENDOR_APIS; CONFIG_SPECIFIC",
            evaluator_contract="GROUND_TRUTH_OPTION_EXACTNESS_AND_ACCURACY_IN_EVALUATION_SCRIPTS; NOT_RUN",
            local_state="OFFICIAL_REPO_REMOTE_INSPECTED_NOT_MATERIALIZED; DATA_CARRIERS_LOCAL",
            specialized_model_dependency="NO_DUPLEX_CORE; EXTERNAL_TEXT_ORCHESTRATOR_OVER_AUDIO_TOOLS",
            strongest_blocker="No repository license was detected, the repo is not locally pinned, and exact tool/API/model versions plus benchmark setup remain unclosed.",
            deviation_ledger=[
                "Nearest prior is external orchestration, not automatically reward-guided control.",
                "The text coordinator does not directly observe raw audio.",
                "Official-source inspection did not execute an entrypoint or metric.",
            ],
            source_to_target_translation="DIRECT_SPEECH_TOOL_ROUTING_PRIOR; COMPARE_ROUTING_AND_CONFLICT_ARBITRATION_ONLY",
            rejection_condition="Reject as reproduction anchor if license, exact environment, benchmark entrypoint, or task-matched frozen-core access remains unresolved.",
        ),
        _readiness_row(
            order=3, work_id="CW-ARXIV-2604.22821", title="Audio2Tool",
            status="INSTRUMENT_SUPPORT", relation="LOCAL_SPEECH_TOOL_ACTION_EVALUATOR_CARRIER",
            capability_assets=["SKILL"],
            official_sources=[
                "https://audio2tool.github.io/",
                "https://huggingface.co/datasets/RVtech/Audio2Tool",
                "https://arxiv.org/abs/2604.22821",
            ],
            license_status="CC-BY-NC-4.0",
            dataset_or_protocol="16,843 queries, 36,421 audio files, 152 tools across eight tiers; expected_tool_call and parameters",
            entrypoints=["REVISION_BOUND_HF_ALLOWLIST_LOADER_REQUIRED"],
            access_state="LOCAL_COMPLETE_DATA; TERMS_REVIEW_AND_ADAPTER_REQUIRED",
            evaluator_contract="TOOL_NAME_AND_ARGUMENT_EXACTNESS_FROM_GOLD_FIELDS; NOT_RUN",
            local_state="LOCAL_REVISION_f1388da9a3189541ab82adac88824a0661670c43; 71441_REMOTE_FILES; 10410773494_BYTES",
            specialized_model_dependency="NONE_IN_DATASET; INSTRUMENT_ONLY",
            strongest_blocker="The dataset is non-commercial, no project adapter is frozen, and 610 retained extras require a revision-bound allowlist.",
            deviation_ledger=[
                "Measurement carrier only; never a method reproduction anchor.",
                "Physical-directory enumeration is forbidden for the future loader.",
                "No benchmark was run.",
            ],
            source_to_target_translation="DIRECT_SPEECH_INSTRUMENT_FOR_TOOL_SELECTION_AND_ARGUMENT_FIDELITY",
            rejection_condition="Reject a proposed arm if its outcome cannot be scored from revision-bound gold tool/argument fields without leakage.",
        ),
        _readiness_row(
            order=4, work_id="CW-ARXIV-2510.07838", title="Full-Duplex-Bench-v2",
            status="REFERENCE_ONLY", relation="REFERENCE_ONLY_OUT_OF_SCOPE_SPECIALIZED_SYSTEM",
            capability_assets=["NONE"],
            official_sources=[
                "https://github.com/DanielLin94144/Full-Duplex-Bench",
                "https://arxiv.org/abs/2510.07838",
            ],
            official_repo_revision="3e799c45a045256f47d5f1c9cda90157e2d2ec9e",
            license_status="CC-BY-NC-4.0", dataset_or_protocol="Specialized realtime duplex interaction benchmark",
            entrypoints=["REFERENCE_BOUNDARY_ONLY_NO_PROJECT_ENTRYPOINT"],
            access_state="PUBLIC_REFERENCE; SPECIALIZED_REALTIME_SYSTEM_REQUIRED",
            evaluator_contract="REFERENCE_ONLY; NO_PROJECT_EVALUATOR_ADOPTION",
            local_state="SIGNED_OVERLAY_RETAINED_AS_ONE_BLIND_EXCLUSION_BOUNDARY",
            specialized_model_dependency="REQUIRED",
            strongest_blocker="The task requires a specialized duplex model/system and is outside the agentic research route.",
            deviation_ledger=[
                "Retained only because it is a signed overlay and calibrates exclusion.",
                "Cannot be reproduction candidate, CORE_MEMBER, or branch primary.",
            ],
            source_to_target_translation="NONE_OUT_OF_SCOPE_SPECIALIZED_SYSTEM",
            rejection_condition="Always reject from branch promotion under the owner scope ruling.",
        ),
        _readiness_row(
            order=5, work_id="CW-ARXIV-2512.14865", title="Audio MultiChallenge",
            status="INSTRUMENT_SUPPORT_REFERENCE_ONLY",
            relation="INSTRUMENT_SUPPORT_REFERENCE_ONLY",
            capability_assets=["MEMORY"],
            official_sources=[
                "https://huggingface.co/datasets/ScaleAI/audiomc",
                "https://arxiv.org/abs/2512.14865",
            ],
            official_repo_revision="90ea11040fd05f41cf433b90f97ada45d847c500",
            license_status="MIT", dataset_or_protocol="452 conversations, 47 speakers and 1,712 atomic rubrics",
            entrypoints=["HUGGINGFACE_PARQUET_LOADER", "DATASET_CARD_CONVERSATION_HISTORY_BUILDER"],
            access_state="LOCAL_DATA_COMPLETE; EXTERNAL_JUDGE_REQUIRED",
            evaluator_contract="FIXED_CONTEXT_FINAL_TURN_ATOMIC_RUBRIC_JUDGE; NOT_RUN",
            local_state="LOCAL_DATASET_PINNED_5283214702_BYTES",
            specialized_model_dependency="NONE_IN_DATASET; INSTRUMENT_ONLY",
            strongest_blocker="Fixed-context final-turn judging does not reproduce interactive recovery and depends on an external judge proxy.",
            deviation_ledger=[
                "Fallback reproduction identity revoked.",
                "May support memory measurement only after family compatibility review.",
            ],
            source_to_target_translation="SPEECH_MEMORY_INSTRUMENT_ONLY",
            rejection_condition="Reject if the proposed memory claim requires interactive repair or outcome-independent evaluation absent from this protocol.",
        ),
    ]

    analogue_specs = [
        (6, "2512.16978", "LongShOTAgent", "KNOWLEDGE"),
        (7, "2512.23646", "Active Perception Agent", "KNOWLEDGE"),
        (8, "2606.18448", "VISUALSKILL", "SKILL"),
        (9, "2603.12056", "XSkill", "SKILL"),
        (10, "2605.13527", "MMSkills", "SKILL"),
        (11, "2606.09316", "Anything2Skill", "SKILL"),
        (12, "2606.29538", "RESOURCE2SKILL", "SKILL"),
        (13, "2602.07624", "M2A", "MEMORY"),
        (14, "2601.03515", "Mem-Gallery", "MEMORY"),
        (15, "2601.19935", "Mem2ActBench", "MEMORY"),
    ]
    for order, identity, title, capability in analogue_specs:
        candidates.append(_readiness_row(
            order=order, work_id=f"CW-ARXIV-{identity}", title=title,
            status="TRANSFER_ANALOGUE", relation=f"{capability}_CAPABILITY_FAMILY_ANALOGUE",
            capability_assets=[capability], official_sources=[f"https://arxiv.org/abs/{identity}"],
            license_status="CODE_OR_ASSET_LICENSE_NOT_CLOSED_TRANSFER_REFERENCE_ONLY",
            dataset_or_protocol="SOURCE_DOMAIN_PROTOCOL_REQUIRES_CELL_LEVEL_TRANSLATION_REVIEW",
            entrypoints=["NO_SPEECH_REPRODUCTION_ENTRYPOINT_CLAIMED"],
            access_state="SOURCE_FULLTEXT_BOUND; TARGET_HARNESS_NOT_IMPLEMENTED",
            evaluator_contract="SOURCE_EVALUATOR_REFERENCE_ONLY; TARGET_EVALUATOR_MUST_BE_REDEFINED",
            local_state="LOCAL_FULLTEXT_BOUND_IN_STAGE1B_320_UNION",
            specialized_model_dependency="NO_DUPLEX_DEPENDENCY_ASSERTED; SOURCE_DOMAIN_SYSTEM_MAY_DIFFER",
            strongest_blocker="No speech/omni task-matched reproduction contract is closed; source-domain gains cannot be transferred numerically.",
            deviation_ledger=[
                "Default role is TRANSFER_ANALOGUE, not reference-equivalent evidence.",
                "Each future use requires source-to-target variable mapping and a rejection observation.",
                "No code, model, metric, or prototype was run.",
            ],
            source_to_target_translation=f"Translate only the {capability.lower()} decision structure into the shared observation-state-signal-decision-action-feedback-update-stop interface.",
            rejection_condition="Reject transfer if the target speech variable is not interventionally corresponding, the outcome semantics differ, or the effect depends on source-only perception/training.",
        ))
    return {
        "schema": "sf-stage1c-v2-reproduction-readiness-v2",
        "artifact_id": "SF-STAGE1C-V2-REPRODUCTION-READINESS-RC2",
        "status": "KNOWN_CANDIDATE_READ_ONLY_CLOSURE_NO_ANCHOR_SELECTED",
        "shared_agent_protocol": [
            "OBSERVATION", "EXTERNAL_STATE", "SIGNAL_OR_EVALUATOR", "DECISION_RIGHT",
            "ACTION_OR_TOOL", "FEEDBACK", "UPDATE_OR_REPAIR_OR_STOP",
        ],
        "primary_selection": "WITHHELD_PENDING_POST_CALIBRATION_ANCHOR_PROMOTION",
        "fallback_selection": "WITHHELD_NO_FORCED_FALLBACK",
        "candidate_priority": [
            "CW-ARXIV-2509.16971", "CW-ARXIV-2510.02995", "CW-ARXIV-2604.22821",
        ],
        "validation_carriers": [
            {
                "asset_id": "MMAU-mini", "role": "VALIDATION_CARRIER",
                "revision": "42bd874593a0beed966e505411e896a808f9931f",
                "license": "UNDECLARED_REQUIRES_REVIEW", "local_state": "COMPLETE_2843372907_BYTES",
                "task_split_evaluator_status": "TASK_AND_DATA_BOUND; EXACT_PROTOCOL_NOT_RUN",
            },
            {
                "asset_id": "MMAR", "role": "VALIDATION_CARRIER",
                "revision": "3bd051123480e80d273ae9e8e9f1653f49010ac7",
                "license": "CC-BY-NC-4.0", "local_state": "COMPLETE_2994099985_BYTES",
                "task_split_evaluator_status": "TASK_DATA_AND_ACCURACY_SCRIPT_BOUND; NOT_RUN",
            },
        ],
        "selection_basis": "FAIL_CLOSED_UNTIL_TASK_MATCHED_METHOD_ENTRYPOINT_ACCESS_EVALUATOR_AND_LICENSE_ARE_ALL_CLOSED",
        "selection_is_problem_or_branch_ranking": False,
        "no_reproduction_executed": True, "candidates": candidates,
    }


def coder_bundle_sha256(
    package: dict[str, Any], artifact_names: tuple[str, ...] | list[str],
) -> str:
    """Hash the ordered shared content independently of coder identity or receipt."""
    digest = hashlib.sha256()
    for name in artifact_names:
        digest.update(name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(json_bytes(package[name]))
        digest.update(b"\0")
    return digest.hexdigest()


def build_distribution_manifest(package: dict[str, Any]) -> dict[str, Any]:
    names = CODER_DISTRIBUTION_ALLOWED_ARTIFACTS
    artifacts = [
        {
            "artifact_name": name,
            "path": ARTIFACT_PATHS[name].relative_to(REPO).as_posix(),
            "bytes": len(json_bytes(package[name])),
            "sha256": sha256_bytes(json_bytes(package[name])),
        }
        for name in names
    ]
    return {
        "schema": "sf-stage1c-v2-calibration-distribution-manifest-v2",
        "artifact_id": "SF-STAGE1C-V2-CALIBRATION-DISTRIBUTION-RC2",
        "status": "FROZEN_INPUT_BYTES_PREPARED_NOT_DISTRIBUTED",
        "scope": "CODER_VISIBLE_SHARED_CONTENT",
        "artifacts": artifacts,
        "content_bundle_sha256": coder_bundle_sha256(package, names),
        "identity_binding_separate": True,
        "submission_receipt_binding_separate": True,
        "both_coders_must_receive_byte_identical_content": True,
        "reviewer_only_artifacts_excluded": [
            "schema_bundle", "calibration_manifest", "claim_templates",
            "coder_transaction", "reproduction_readiness",
        ],
        "coder_prompt_status": "MUST_BE_ADDED_AND_HASHED_AT_ACTOR_ASSIGNMENT",
        "distribution_authorized": False,
    }


def build_package() -> dict[str, Any]:
    owner_text = OWNER_DIRECTION.read_text(encoding="utf-8")
    if "按你的建议执行" not in owner_text or OWNER_AGENTIC_RULING not in owner_text:
        raise ContractError("owner RC2 and agentic scope directions are not exact-message bound")
    if "AUTHORIZE_STAGE1C_V2_AGENTIC_RC2_REVIEW_SUBMISSION" not in owner_text:
        raise ContractError("exact RC2 review-submission authorization is not bound")
    response_schema = build_response_schema()
    Draft202012Validator.check_schema(response_schema)
    surfaces = rc1.source_surfaces()
    bootstrap = rc1.build_bootstrap(surfaces)
    calibration_ids = build_agentic_calibration(bootstrap, surfaces)["canonical_ids"]
    source_manifest = build_source_manifest(calibration_ids)
    calibration, packet = build_calibration_artifacts(bootstrap, source_manifest, response_schema)
    claim_templates = build_claim_templates()
    package = {
        "response_schema": response_schema,
        "schema_bundle": build_schema_bundle(response_schema),
        "source_manifest": source_manifest,
        "calibration_manifest": calibration,
        "blind_packet": packet,
        "assignment_manifest": build_assignment_manifest(calibration, packet),
        "claim_templates": claim_templates,
        "claim_template_coder_view": build_claim_template_coder_view(claim_templates),
        "coder_codebook": build_coder_codebook(response_schema),
        "agreement": build_agreement(response_schema),
        "coder_transaction": build_coder_transaction(response_schema),
        "reproduction_readiness": build_reproduction_readiness(),
    }
    package["distribution_manifest"] = build_distribution_manifest(package)
    bundle_hash = package["distribution_manifest"]["content_bundle_sha256"]
    package["coder_transaction"]["shared_content_bundle_sha256"] = bundle_hash
    for slot in package["coder_transaction"]["coder_slots"]:
        slot["expected_content_bundle_sha256"] = bundle_hash
    return package


def _contains_not_coded(value: Any) -> bool:
    if isinstance(value, dict):
        return any(_contains_not_coded(child) for child in value.values())
    if isinstance(value, list):
        return any(_contains_not_coded(child) for child in value)
    return value == "NOT_CODED"


def validate_completed_response(response: dict[str, Any], schema: dict[str, Any]) -> None:
    Draft202012Validator(schema).validate(response)
    if response["response_status"] != "CODER_SUBMITTED":
        raise ContractError("response is not a coder submission")
    if response["paper_labels"]["empirical_experiment_present"] is None:
        raise ContractError("empirical_experiment_present is not coded")
    if _contains_not_coded(response["paper_labels"]):
        raise ContractError("paper labels retain NOT_CODED")
    scope = response["paper_labels"]["agentic_scope"]
    if scope["scope_reason"] == "PENDING":
        raise ContractError("agentic scope reason is not final")
    components = set(scope["loop_components"])
    if scope["scope_status"] == "DIRECT_AGENTIC":
        if not {"DECIDE", "ACT_OR_TOOL"} <= components:
            raise ContractError("direct agentic scope requires decide and act/tool")
        if scope["core_dependency"] != "GENERIC_FROZEN_CORE":
            raise ContractError("direct agentic scope requires a generic frozen core")
        if scope["control_role"] == "TRAINED_CONTROL":
            raise ContractError("trained control cannot pass the direct agentic gate")
    if scope["scope_status"] == "OUT_OF_SCOPE_SPECIALIZED_SYSTEM":
        if scope["core_dependency"] != "SPECIALIZED_MODEL_REQUIRED":
            raise ContractError("specialized-system exclusion requires specialized dependency")
        if response["paper_labels"]["paper_disposition"] != "OUT_OF_SCOPE_WITH_REASON":
            raise ContractError("specialized-system exclusion must be out of scope")
        if response["paper_labels"]["reference_borrow_reproduce"] != "REFERENCE":
            raise ContractError("specialized-system exclusion can only be a reference")
    for name in CALIBRATED_OBJECT_ARRAYS:
        objects, reason = response[name], response["object_absence_reasons"][name]
        if objects and reason != "OBJECTS_PRESENT":
            raise ContractError(f"{name} has objects without OBJECTS_PRESENT")
        if not objects and reason in {"OBJECTS_PRESENT", "NOT_CODED"}:
            raise ContractError(f"{name} empty without a final absence reason")
    if not response["source_locators"] or not response["review_events"]:
        raise ContractError("submitted response requires source locators and a review event")


def validate_package(package: dict[str, Any]) -> None:
    Draft202012Validator.check_schema(package["response_schema"])
    Draft202012Validator.check_schema(package["schema_bundle"])
    if count_enum_values(package["schema_bundle"]) <= 35:
        raise ContractError("full-mapping schema bundle is not categorically typed")
    claim_scope = package["schema_bundle"]["$defs"]["claim_record"]["properties"]["scope"]
    if set(claim_scope.get("required", [])) != set(rc1.CLAIM_SCOPE_FIELDS):
        raise ContractError("full-mapping claim scope is incomplete")
    if len(package["blind_packet"]["items"]) != 56 or package["source_manifest"]["N"] != 56:
        raise ContractError("RC2 calibration/source packet is not N=56")
    calibration_ids = set(package["calibration_manifest"]["canonical_ids"])
    if "arxiv:2604.04847" in calibration_ids or "arxiv:2512.23646" not in calibration_ids:
        raise ContractError("agentic sentinel replacement is not exact")
    if len(package["calibration_manifest"]["overlay_ids"]) != 38:
        raise ContractError("agentic calibration overlay denominator changed")
    if len(package["calibration_manifest"]["inherited_sentinels"]) != 18:
        raise ContractError("agentic calibration sentinel denominator changed")
    problem_enum = package["response_schema"]["$defs"]["paper_labels"]["properties"]["problem_nodes"]["items"]["enum"]
    if "INTERACTIVE_FULL_DUPLEX_OBJECTIVES" in problem_enum:
        raise ContractError("duplex objective remains active in the RC2 coder contract")
    if package["schema_bundle"].get("specialized_system_branch_gate") != "SPECIALIZED_SYSTEM_EXCLUSION_CANNOT_ENTER_CORE_MEMBER_OR_BRANCH_PRIMARY":
        raise ContractError("full-mapping specialized-system branch gate is missing")
    if not verify_source_manifest(package["source_manifest"]):
        raise ContractError("source byte verification failed")
    schema_id = package["response_schema"]["$id"]
    if package["blind_packet"]["calibration_response_schema_id"] != schema_id:
        raise ContractError("packet response schema mismatch")
    if package["agreement"]["calibration_response_schema_id"] != schema_id:
        raise ContractError("agreement response schema mismatch")
    for path in package["agreement"]["critical_response_paths"]:
        if not schema_path_exists(package["response_schema"], path):
            raise ContractError(f"agreement critical path missing from schema: {path}")
    validator = Draft202012Validator(package["response_schema"])
    for item in package["blind_packet"]["items"]:
        validator.validate(item["blank_response"])
    if any(row["object_type"] != "CLAIM_TEMPLATE" or row["load_bearing"] for row in package["claim_templates"]["claim_templates"]):
        raise ContractError("heterogeneous synthesis centre promoted to claim")
    assignment = package["assignment_manifest"]
    if assignment["N"] != 56 or not assignment["sample_role_hidden"]:
        raise ContractError("coder assignment view exposes or changes calibration roles")
    expected_assignment_items = [
        {
            "packet_item_id": row["packet_item_id"],
            "source_item_id": row["source_item_id"],
            "source_revision": row["source_revision"],
            "primary_rendition_sha256": row["primary_rendition_sha256"],
        }
        for row in package["blind_packet"]["items"]
    ]
    if assignment["items"] != expected_assignment_items:
        raise ContractError("coder assignment view is not byte-source aligned")
    full_claim_ids = {
        row["claim_template_id"] for row in package["claim_templates"]["claim_templates"]
    }
    coder_claim_ids = {
        row["claim_template_id"]
        for row in package["claim_template_coder_view"]["claim_templates"]
    }
    if coder_claim_ids != full_claim_ids or len(coder_claim_ids) != 13:
        raise ContractError("neutral claim-template view is incomplete")
    distribution = package["distribution_manifest"]
    distributed_names = tuple(row["artifact_name"] for row in distribution["artifacts"])
    leaks = scan_coder_bundle_leaks(package, distributed_names)
    if leaks:
        raise ContractError(f"coder-visible leakage detected: {leaks}")
    if (
        distribution["status"] != "FROZEN_INPUT_BYTES_PREPARED_NOT_DISTRIBUTED"
        or distribution["scope"] != "CODER_VISIBLE_SHARED_CONTENT"
        or distribution["distribution_authorized"]
    ):
        raise ContractError("coder distribution escaped the prepared-not-distributed gate")
    if not (
        distribution["identity_binding_separate"]
        and distribution["submission_receipt_binding_separate"]
        and distribution["both_coders_must_receive_byte_identical_content"]
    ):
        raise ContractError("coder identity or receipt binding can mutate shared content")
    if distribution["content_bundle_sha256"] != coder_bundle_sha256(package, distributed_names):
        raise ContractError("coder shared-content bundle hash is stale")
    for row in distribution["artifacts"]:
        name = row["artifact_name"]
        expected_bytes = json_bytes(package[name])
        if row["bytes"] != len(expected_bytes) or row["sha256"] != sha256_bytes(expected_bytes):
            raise ContractError(f"coder distribution artifact hash is stale: {name}")
    if package["coder_transaction"]["distribution_authorized"]:
        raise ContractError("coder distribution activated during RC2 preparation")
    coder = package["coder_transaction"]
    if coder["adjudicator"]["assignment_status"] != "UNASSIGNED":
        raise ContractError("adjudicator was bound before distribution authorization")
    if coder["shared_content_bundle_sha256"] != distribution["content_bundle_sha256"]:
        raise ContractError("coder transaction is not bound to the shared content bundle")
    if any(
        slot["expected_content_bundle_sha256"] != distribution["content_bundle_sha256"]
        or slot["assignment_status"] != "UNASSIGNED"
        for slot in coder["coder_slots"]
    ):
        raise ContractError("coder identity binding changed or content hashes diverged")
    readiness = package["reproduction_readiness"]
    if readiness["primary_selection"] != "WITHHELD_PENDING_POST_CALIBRATION_ANCHOR_PROMOTION":
        raise ContractError("read-only closure promoted a primary anchor")
    if readiness["fallback_selection"] != "WITHHELD_NO_FORCED_FALLBACK":
        raise ContractError("read-only closure forced a fallback anchor")
    if any(row["method_anchor_eligible"] or row["reproduction_eligible"] for row in readiness["candidates"]):
        raise ContractError("read-only candidate closure promoted an anchor")
    by_id = {row["canonical_work_id"]: row for row in readiness["candidates"]}
    if by_id["CW-ARXIV-2510.07838"]["status"] != "REFERENCE_ONLY":
        raise ContractError("FDB-v2 escaped its exclusion-boundary role")
    if by_id["CW-ARXIV-2512.14865"]["status"] != "INSTRUMENT_SUPPORT_REFERENCE_ONLY":
        raise ContractError("Audio MultiChallenge escaped its instrument-only role")
    if by_id["CW-ARXIV-2604.22821"]["status"] != "INSTRUMENT_SUPPORT":
        raise ContractError("Audio2Tool escaped its instrument-only role")
    if any(row["research_execution_performed"] for row in readiness["candidates"]):
        raise ContractError("research execution was recorded during read-only closure")


def build_report(package: dict[str, Any]) -> dict[str, Any]:
    validate_package(package)
    return {
        "schema": "sf-stage1c-v2-precalibration-contract-report-v2",
        "artifact_id": "SF-STAGE1C-V2-PRECALIBRATION-CONTRACT-REPORT-RC2",
        "as_of": "2026-07-24", "status": "AGENTIC_RC2_CODER_READY_NOT_DISTRIBUTED",
        "authority": {
            "owner_direction": "按你的建议执行",
            "owner_agentic_scope_ruling": OWNER_AGENTIC_RULING,
            "specialized_duplex_route": "EXCLUDED_FROM_RESEARCH_REPRODUCTION_AND_BRANCH_ROUTE",
            "governance": "INDEPENDENT_ADVISORY_REVIEW + OWNER_ACCEPTED_AUTHORIZATION",
            "historical_mapping_token_interpretation": "DESIGN_AND_CALIBRATION_PREPARATION_ONLY",
            "calibration_execution_started": False, "coder_distributed": False,
            "review_submission_authorized": True,
            "local_commit_created": False, "independent_review_submitted": False,
            "agreement_computed": False, "full_mapping_signed": False,
            "research_execution_authorized": False,
        },
        "reviewer_p0_closure": {
            "response_agreement_isomorphic": True, "object_level_mapping_in_response": True,
            "source_bytes_version_and_hash_bound": True,
            "claim_template_scoped_instance_separated": True,
            "reviewer_and_coder_artifacts_separated": True,
            "coder_visible_recursive_leakage_scan_passed": True,
            "coder_identity_and_receipt_binding_separate": True,
            "two_coder_content_bundle_byte_identity_bound": True,
        },
        "reviewer_p1_closure": {
            "full_mapping_schema_categorical_and_closed": True,
            "claim_scope_nine_dimensions_required": True,
            "known_agentic_candidate_assets_terms_protocols_evidence_bound": True,
            "reference_borrow_reproduce_distinction_operationalized": True,
        },
        "surface": {
            "calibration_N": 56, "claim_templates": 13, "scoped_claim_instances": 0,
            "known_candidate_records": len(package["reproduction_readiness"]["candidates"]),
            "reproduction_anchors": 0,
        },
        "remaining_before_distribution": [
            "CREATE_LOCAL_COMMIT_WITHOUT_PUSH",
            "OBTAIN_INDEPENDENT_RC2_METHOD_REVIEW_ACCEPT",
            "OBTAIN_AUTHORIZE_STAGE1C_V2_AGENTIC_CALIBRATION_DISTRIBUTION",
            "ASSIGN_TWO_PROVENANCE_DISTINCT_ISOLATED_CODERS",
            "ASSIGN_HUMAN_DOMAIN_EXPERT_ADJUDICATOR", "HASH_CODER_PROMPT",
        ],
    }


def build_review_manifest(report: dict[str, Any]) -> dict[str, Any]:
    paths = [
        OWNER_DIRECTION, REVIEW,
        WORKBENCH / "README.md", WORKBENCH / "codebook-v2.md",
        WORKBENCH / "stage1c-v2-precalibration-contract-rc2-zh.md",
        REPO / "scripts/survey/sf_stage1c_v2_precalibration_rc2.py",
        REPO / "scripts/survey/sf_stage1c_v2_calibration_agreement.py",
        REPO / "scripts/survey/test_sf_stage1c_v2_precalibration_rc2.py",
        *ARTIFACT_PATHS.values(), REPORT_PATH,
    ]
    missing = [path for path in paths if not path.is_file()]
    if missing:
        raise ContractError(f"RC2 review inputs missing: {missing}")
    return {
        "schema": "sf-stage1c-v2-precalibration-review-manifest-v2",
        "artifact_id": "SF-STAGE1C-V2-PRECALIBRATION-REVIEW-PACKAGE-RC2",
        "status": report["status"], "artifact_count": len(paths),
        "artifacts": [
            {"path": path.relative_to(REPO).as_posix(), "bytes": path.stat().st_size, "sha256": sha256_path(path)}
            for path in paths
        ],
        "requested_review_verdict": "ACCEPT_AGENTIC_RC2_METHOD_CONTRACT_FOR_CODER_INTAKE_OR_WITHHOLD_WITH_BOUNDED_DEFECTS",
        "authority_withheld": [
            "CALIBRATION_DISTRIBUTION", "SIGN_STAGE1C_V2_EXPERIMENT_MAPPING",
            "320_PAPER_FULL_MAPPING", "RESEARCH_EXECUTION", "PROBLEM_OR_BRANCH_SELECTION", "NOVELTY_VERDICT",
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
                raise ContractError(f"materialized RC2 artifact is stale: {ARTIFACT_PATHS[name]}")
        if load_json(REPORT_PATH) != report:
            raise ContractError("RC2 contract report is stale")
        if load_json(REVIEW_MANIFEST_PATH) != build_review_manifest(report):
            raise ContractError("RC2 review manifest is stale")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    try:
        report = run(write=args.write)
    except (ContractError, OSError, ValueError) as error:
        print(f"FAIL: {error}")
        return 1
    print(json.dumps({"status": report["status"], **report["surface"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
