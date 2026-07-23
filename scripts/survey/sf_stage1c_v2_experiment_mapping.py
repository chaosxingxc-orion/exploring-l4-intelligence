#!/usr/bin/env python3
"""Build and verify the pre-sign Stage-1C v2 experiment-mapping package.

This module is deliberately unable to activate CURRENT or claim experiment-level
recoding.  It inventories the frozen Stage-1B registry, exposes deterministic
contracts for the post-sign work, and prepares an independently reviewable gate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable


REPO = Path(__file__).resolve().parents[2]
REGISTRY_DIR = REPO / "wiki" / "survey" / "registry"
WORKBENCH_DIR = (
    REPO / "wiki" / "survey" / "workbench" / "system-first-stage1c-v2"
)
CONTRACT_PATH = WORKBENCH_DIR / "experiment-mapping-contract-v2.json"
BOOTSTRAP_PATH = WORKBENCH_DIR / "paper-audit-bootstrap-v2.json"
PROTOCOL_PATH = WORKBENCH_DIR / "protocol-v2.md"
REVIEW_REQUEST_PATH = WORKBENCH_DIR / "package-guide.md"
REVIEW_MANIFEST_PATH = WORKBENCH_DIR / "review-package-manifest.json"
DEFAULT_REPORT_PATH = (
    REPO
    / "docs"
    / "checks"
    / "stage1c-v2"
    / "pre-sign-2026-07-23"
    / "contract-report.json"
)
FROZEN_STAGE1B_RELEASE = "38fb9435d0c35e226ad62b16015a6dbee054e6c2"
REQUESTED_VERDICT = "SIGN_STAGE1C_V2_EXPERIMENT_MAPPING"


DATASET_LINEAGE_TYPES = {
    "SAME_REVISION",
    "DERIVED_FROM",
    "SUBSET_OF",
    "TRANSLATED_FROM",
    "AUDIO_RENDERING_OF",
    "REANNOTATED_FROM",
    "SPLIT_OF",
}
DATASET_RELATION_TYPES = {
    "INDEPENDENT_SAME_TASK",
    "CROSS_DATASET_VALIDATION",
    "DISTRIBUTION_SHIFT_TEST",
    "PROTOCOL_ANALOGUE",
}
FAMILY_MEMBERSHIP_TYPES = {
    "CORE_MEMBER",
    "VALIDATION_MEMBER",
    "TRANSFER_ANALOGUE",
    "FALSIFIER",
    "INSTRUMENT_SUPPORT",
}
FAMILY_EVIDENCE_STATES = {
    "CONSISTENT_SUPPORT",
    "MIXED",
    "NULL_OR_NEGATIVE",
    "INSUFFICIENT_EVIDENCE",
}
LOCAL_READINESS_STATES = {
    "LOCAL_READY",
    "LOCAL_ADAPTABLE",
    "BLOCKED_ASSET_OR_TERMS",
    "TRANSFER_ONLY",
}
TASK_FAMILIES = {
    "PERCEPTION_RECOGNITION",
    "SEMANTIC_UNDERSTANDING_REASONING",
    "TRANSFORMATION_GENERATION",
    "TOOL_ENVIRONMENT_ACTION",
    "INTERACTIVE_DIALOGUE",
    "META_EVALUATION",
}
CAPABILITY_TAGS = {
    "OBSERVATION_EVIDENCE",
    "STATE_MEMORY",
    "CANDIDATE_SUPPLY",
    "EVALUATOR_SIGNAL",
    "SELECTION_ROUTING",
    "BUDGET_STOP",
    "REPAIR_ROLLBACK",
    "TOOL_ENVIRONMENT",
    "INTERACTION_RECOVERY",
}
FAMILY_SIGNATURE_FIELDS = (
    "problem_id",
    "evaluation_object",
    "outcome_semantics",
    "environment_mode",
    "access_protocol",
    "comparison_interpretability",
)
CELL_IDENTITY_FIELDS = (
    "paper_work_id",
    "dataset",
    "core",
    "input_condition",
    "intervention",
    "budget_horizon",
)


class ContractError(RuntimeError):
    """Raised when a Stage-1C v2 contract would make an unsafe claim."""


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def registry_shards(registry_dir: Path = REGISTRY_DIR) -> list[Path]:
    """Return the four immutable Stage-1B registry shards in name order."""

    paths = sorted(registry_dir.glob("stage1b-bounded-*-papers.jsonl"))
    direct = registry_dir / "stage1b-bounded-2026-07-22-papers.jsonl"
    if direct.exists():
        paths = sorted({direct, *paths})
    if len(paths) != 4:
        raise ContractError(f"expected four Stage-1B registry shards; found {len(paths)}")
    return paths


def load_registry_records(registry_dir: Path = REGISTRY_DIR) -> list[dict]:
    """Load exactly one canonical record from each JSONL registry row."""

    records: list[dict] = []
    for path in registry_shards(registry_dir):
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as error:
                raise ContractError(f"invalid JSON at {path}:{line_number}: {error}") from error
            if not isinstance(row, dict) or not row.get("canonical_id"):
                raise ContractError(
                    f"registry row lacks canonical_id at {path}:{line_number}"
                )
            row = dict(row)
            row["_registry_path"] = path.relative_to(REPO).as_posix()
            row["_registry_line"] = line_number
            records.append(row)

    identifiers = [row["canonical_id"] for row in records]
    duplicates = sorted(
        identifier for identifier, count in Counter(identifiers).items() if count > 1
    )
    if duplicates:
        raise ContractError(f"duplicate canonical registry IDs: {duplicates}")
    if len(records) != 226:
        raise ContractError(f"expected 226 frozen registry records; found {len(records)}")
    return sorted(records, key=lambda row: row["canonical_id"])


def experiment_cell_id(cell: dict) -> str:
    """Return a stable ID from run configuration; observations are intentionally excluded."""

    missing = [field for field in CELL_IDENTITY_FIELDS if field not in cell]
    if missing:
        raise ContractError(f"experiment cell identity is missing fields: {missing}")
    identity = {field: cell[field] for field in CELL_IDENTITY_FIELDS}
    digest = hashlib.sha256(_canonical_json(identity).encode("utf-8")).hexdigest()[:16]
    return f"EC-{digest}"


def comparability_key(cell: dict, observation: dict) -> tuple[str, ...]:
    """Return the exact key required before any cross-paper numeric comparison."""

    dataset = cell.get("dataset", {})
    core = cell.get("core", {})
    required = {
        "dataset.canonical_name": dataset.get("canonical_name"),
        "dataset.revision": dataset.get("revision"),
        "dataset.split": dataset.get("split"),
        "core.model_id": core.get("model_id"),
        "core.revision": core.get("revision"),
        "core.access_protocol": core.get("access_protocol"),
        "input_condition": cell.get("input_condition"),
        "metric": observation.get("metric"),
        "budget_horizon": cell.get("budget_horizon"),
    }
    missing = [name for name, value in required.items() if value in (None, "")]
    if missing:
        raise ContractError(f"comparability key is missing fields: {missing}")
    return tuple(str(required[name]) for name in required)


def core_membership_compatible(left: dict, right: dict) -> bool:
    """Return whether two cells can be direct CORE_MEMBER comparators."""

    for field in FAMILY_SIGNATURE_FIELDS:
        if left.get(field) in (None, "") or right.get(field) in (None, ""):
            raise ContractError(f"family signature is missing required field {field}")
    return all(left[field] == right[field] for field in FAMILY_SIGNATURE_FIELDS)


def validate_dataset_edge(edge: dict) -> str:
    """Validate one factual lineage edge or one explicitly non-lineage relation."""

    edge_type = edge.get("edge_type")
    for field in ("source_dataset", "target_dataset", "evidence_mode"):
        if edge.get(field) in (None, ""):
            raise ContractError(f"dataset edge is missing {field}")
    if edge_type in DATASET_LINEAGE_TYPES:
        if edge.get("source_locator") in (None, ""):
            raise ContractError("dataset lineage requires a traceable source_locator")
        return "lineage"
    if edge_type in DATASET_RELATION_TYPES:
        if edge.get("rationale") in (None, ""):
            raise ContractError("dataset relation requires a bounded rationale")
        return "relation"
    raise ContractError(f"unsupported dataset edge_type: {edge_type!r}")


def branch_readiness(branch: dict) -> tuple[bool, list[str]]:
    """Evaluate the five evidence gates and the common four-arm contract."""

    missing: list[str] = []
    if branch.get("local_readiness") not in {"LOCAL_READY", "LOCAL_ADAPTABLE"}:
        missing.append("local_readiness")
    for field in (
        "residual_hypothesis",
        "nearest_prior",
        "outcome_contract",
        "strongest_falsifier",
        "kill_criterion",
    ):
        if branch.get(field) in (None, ""):
            missing.append(field)

    arms = branch.get("arms")
    if not isinstance(arms, dict):
        missing.append("arms")
    else:
        if arms.get("frozen_baseline") in (None, ""):
            missing.append("arms.frozen_baseline")
        if arms.get("nearest_prior_reproduction") in (None, ""):
            missing.append("arms.nearest_prior_reproduction")
        candidates = arms.get("candidate_strategy")
        if not isinstance(candidates, list) or not candidates:
            missing.append("arms.candidate_strategy")
        if arms.get("oracle_upper_bound") in (None, "") and arms.get(
            "oracle_not_definable_reason"
        ) in (None, ""):
            missing.append("arms.oracle_upper_bound_or_reason")
    return not missing, missing


def _source_domain(row: dict) -> str:
    if row.get("speech_primary_object"):
        return "SPEECH_AUDIO_PRIMARY"
    transfer_objects = set(row.get("method_path", {}).get("transfer_objects", []))
    if {"multimodal", "video", "vision"} & transfer_objects:
        return "VISION_OR_MULTIMODAL_TRANSFER"
    if {"agent", "gui", "robot"} & transfer_objects:
        return "TEXT_OR_AGENT_TRANSFER"
    return "NON_SPEECH_OR_BOUNDARY"


def build_pre_sign_bootstrap(records: Iterable[dict]) -> dict:
    """Build a metadata-only inventory that makes no experiment-level claim."""

    rows = list(records)
    identifiers = [row["canonical_id"] for row in rows]
    if len(identifiers) != len(set(identifiers)):
        raise ContractError("pre-sign source records contain duplicate canonical IDs")
    role_counts = Counter(row.get("role", "MISSING_ROLE") for row in rows)
    shards = []
    seen_paths = sorted({row["_registry_path"] for row in rows})
    for relative in seen_paths:
        path = REPO / relative
        shards.append(
            {
                "path": relative,
                "sha256": _sha256_bytes(path.read_bytes()),
            }
        )

    audit_rows = []
    for row in sorted(rows, key=lambda item: item["canonical_id"]):
        datasets = sorted(
            {
                dataset.get("canonical_name")
                for dataset in row.get("datasets", [])
                if dataset.get("canonical_name")
            }
        )
        audit_rows.append(
            {
                "paper_work_id": row["canonical_id"],
                "title": row.get("title", ""),
                "stage1b_role": row.get("role", "MISSING_ROLE"),
                "source_domain": _source_domain(row),
                "registry_locator": {
                    "path": row["_registry_path"],
                    "line": row["_registry_line"],
                },
                "fulltext_evidence_locator_count": len(
                    row.get("evidence_locators", [])
                ),
                "speech_task_tags": sorted(row.get("speech_task_tags", [])),
                "dataset_names": datasets,
                "repository_status": row.get(
                    "repository_status", "MISSING_REPOSITORY_STATUS"
                ),
                "pre_sign_disposition": "AWAITING_AUTHORIZED_EXPERIMENT_RECODE",
                "experiment_cell_ids": [],
                "load_bearing_status": "NOT_YET_ADJUDICATED",
                "adjudication_status": "NOT_STARTED",
                "claim_limit": (
                    "Metadata bootstrap only; no experiment cell, empirical-status, "
                    "family-membership, branch-readiness or novelty claim is made."
                ),
            }
        )

    return {
        "schema": "sf-stage1c-v2-paper-audit-bootstrap-v1",
        "artifact_id": "SF-STAGE1C-V2-PRE-SIGN-PAPER-AUDIT-2026-07-23",
        "stage": "STAGE_1C_V2_PRE_SIGN",
        "authority": {
            "state": "AWAITING_INDEPENDENT_SIGNATURE",
            "requested_verdict": REQUESTED_VERDICT,
            "granted": "METADATA_BOOTSTRAP_AND_REVIEW_PREPARATION_ONLY",
            "withheld": [
                "EXPERIMENT_LEVEL_RECODING",
                "FAMILY_ADJUDICATION",
                "BRANCH_FORMATION",
                "CURRENT_ACTIVATION",
                "MODEL_OR_API_EXECUTION",
                "DATASET_OR_BENCHMARK_METRICS",
                "PAPER_REPRODUCTION",
                "PROTOTYPE_IMPLEMENTATION",
                "NOVELTY_VERDICT",
            ],
        },
        "frozen_stage1b_release": FROZEN_STAGE1B_RELEASE,
        "source_registry_shards": shards,
        "paper_census": {
            "unique_records": len(audit_rows),
            "role_counts": dict(sorted(role_counts.items())),
        },
        "paper_audit_bootstrap": audit_rows,
    }


def validate_pre_sign_bootstrap(package: dict, records: Iterable[dict]) -> None:
    """Fail closed if the bootstrap overclaims or misses a frozen paper."""

    rows = list(records)
    expected_ids = {row["canonical_id"] for row in rows}
    if package.get("schema") != "sf-stage1c-v2-paper-audit-bootstrap-v1":
        raise ContractError("unsupported pre-sign bootstrap schema")
    authority = package.get("authority", {})
    if authority.get("state") != "AWAITING_INDEPENDENT_SIGNATURE":
        raise ContractError("pre-sign bootstrap must await independent signature")
    if authority.get("requested_verdict") != REQUESTED_VERDICT:
        raise ContractError("pre-sign bootstrap requests the wrong verdict")
    audit_rows = package.get("paper_audit_bootstrap")
    if not isinstance(audit_rows, list):
        raise ContractError("paper_audit_bootstrap must be a list")
    actual_ids = [row.get("paper_work_id") for row in audit_rows]
    if len(actual_ids) != len(set(actual_ids)):
        raise ContractError("paper audit bootstrap contains duplicate paper IDs")
    if set(actual_ids) != expected_ids:
        missing = sorted(expected_ids - set(actual_ids))
        extra = sorted(set(actual_ids) - expected_ids)
        raise ContractError(f"paper audit census mismatch; missing={missing}, extra={extra}")
    if len(audit_rows) != 226:
        raise ContractError(f"paper audit bootstrap must contain 226 rows; found {len(audit_rows)}")
    for row in audit_rows:
        if row.get("pre_sign_disposition") != "AWAITING_AUTHORIZED_EXPERIMENT_RECODE":
            raise ContractError("pre-sign row makes an unauthorized disposition")
        if row.get("experiment_cell_ids") != []:
            raise ContractError("pre-sign row must not claim experiment cells")
        if row.get("adjudication_status") != "NOT_STARTED":
            raise ContractError("pre-sign row must not claim adjudication")


def _load_contract() -> dict:
    try:
        return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ContractError(f"cannot load contract {CONTRACT_PATH}: {error}") from error


def validate_contract_artifact(contract: dict) -> None:
    """Verify the persisted controlled vocabularies and pre-sign authority."""

    if contract.get("schema") != "sf-stage1c-v2-experiment-mapping-contract-v1":
        raise ContractError("unsupported Stage-1C v2 contract schema")
    authority = contract.get("authority", {})
    if authority.get("state") != "AWAITING_INDEPENDENT_SIGNATURE":
        raise ContractError("contract must remain pre-sign")
    if authority.get("requested_verdict") != REQUESTED_VERDICT:
        raise ContractError("contract requests the wrong independent verdict")
    if "CURRENT_ACTIVATION" not in authority.get("withheld_before_signature", []):
        raise ContractError("contract does not withhold CURRENT activation")
    expected = {
        "dataset_lineage": DATASET_LINEAGE_TYPES,
        "dataset_relation": DATASET_RELATION_TYPES,
        "family_membership": FAMILY_MEMBERSHIP_TYPES,
        "family_evidence_state": FAMILY_EVIDENCE_STATES,
        "local_readiness": LOCAL_READINESS_STATES,
        "task_family": TASK_FAMILIES,
        "capability_tag": CAPABILITY_TAGS,
    }
    actual = contract.get("controlled_vocabularies", {})
    for name, values in expected.items():
        if set(actual.get(name, [])) != values:
            raise ContractError(f"controlled vocabulary mismatch for {name}")


def build_report(package: dict) -> dict:
    """Create a machine-readable, non-authoritative verification receipt."""

    return {
        "schema": "sf-stage1c-v2-pre-sign-contract-report-v1",
        "status": "PASS_PRE_SIGN_CONTRACT_ONLY",
        "authority_effect": "NONE",
        "requested_verdict": REQUESTED_VERDICT,
        "frozen_stage1b_release": FROZEN_STAGE1B_RELEASE,
        "checks": {
            "paper_census_226_unique": package["paper_census"]["unique_records"]
            == 226,
            "experiment_cells_claimed": 0,
            "family_memberships_claimed": 0,
            "branches_claimed": 0,
            "current_activation_withheld": True,
            "model_or_metric_execution": 0,
        },
        "next_gate": REQUESTED_VERDICT,
    }


def build_review_manifest() -> dict:
    """Bind exact pre-sign objects without including any CURRENT or HOT carrier."""

    artifacts = (
        ("protocol", PROTOCOL_PATH),
        ("machine_contract", CONTRACT_PATH),
        ("paper_audit_bootstrap", BOOTSTRAP_PATH),
        ("reviewer_brief", REVIEW_REQUEST_PATH),
        (
            "generator_checker",
            REPO / "scripts" / "survey" / "sf_stage1c_v2_experiment_mapping.py",
        ),
        (
            "contract_tests",
            REPO / "scripts" / "survey" / "test_sf_stage1c_v2_experiment_mapping.py",
        ),
        ("pre_sign_report", DEFAULT_REPORT_PATH),
    )
    rows = []
    for role, path in artifacts:
        if not path.is_file():
            raise ContractError(f"review-package artifact is missing: {path}")
        relative = path.relative_to(REPO).as_posix()
        if relative.startswith("wiki/survey/current/") or relative == (
            "wiki/Research-Objective.md"
        ):
            raise ContractError(f"review package may not bind CURRENT/HOT: {relative}")
        raw = path.read_bytes()
        rows.append(
            {
                "role": role,
                "path": relative,
                "bytes": len(raw),
                "sha256": _sha256_bytes(raw),
            }
        )
    return {
        "schema": "sf-stage1c-v2-pre-sign-review-manifest-v1",
        "artifact_id": "SF-STAGE1C-V2-PRE-SIGN-REVIEW-PACKAGE-2026-07-23",
        "status": "READY_FOR_INDEPENDENT_REVIEW_SUBMISSION",
        "authority_effect": "NONE",
        "requested_verdict": REQUESTED_VERDICT,
        "frozen_stage1b_release": FROZEN_STAGE1B_RELEASE,
        "artifacts": rows,
        "exclusions": [
            "wiki/survey/current/",
            "wiki/Research-Objective.md",
            "research model/API outputs",
            "dataset or benchmark metrics",
            "reproduction or prototype outputs",
        ],
    }


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )


def verify_persisted() -> tuple[dict, dict]:
    records = load_registry_records()
    expected = build_pre_sign_bootstrap(records)
    validate_pre_sign_bootstrap(expected, records)
    contract = _load_contract()
    validate_contract_artifact(contract)
    actual = json.loads(BOOTSTRAP_PATH.read_text(encoding="utf-8"))
    validate_pre_sign_bootstrap(actual, records)
    if actual != expected:
        raise ContractError("persisted paper-audit bootstrap is not reproducible")
    for path in (PROTOCOL_PATH, REVIEW_REQUEST_PATH):
        if not path.is_file():
            raise ContractError(f"required pre-sign artifact is missing: {path}")
    return expected, build_report(expected)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write-bootstrap",
        action="store_true",
        help="write only the metadata bootstrap; never writes CURRENT",
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="write a pre-sign verification report after validation",
    )
    parser.add_argument(
        "--write-review-manifest",
        action="store_true",
        help="bind exact pre-sign review objects; never includes CURRENT or HOT",
    )
    args = parser.parse_args(argv)

    try:
        records = load_registry_records()
        package = build_pre_sign_bootstrap(records)
        validate_pre_sign_bootstrap(package, records)
        if args.write_bootstrap:
            write_json(BOOTSTRAP_PATH, package)
        persisted, report = verify_persisted()
        if persisted != package:
            raise ContractError("generated and persisted packages differ")
        if args.report:
            write_json(args.report, report)
        if args.write_review_manifest:
            write_json(REVIEW_MANIFEST_PATH, build_review_manifest())
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    except (ContractError, OSError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
