#!/usr/bin/env python3
"""Build and verify the authorized Stage-1C v2 calibration-input package.

The package is deliberately pre-scale.  It binds two independently signed Stage-1B
overlays into a 320-work calibration input plus a blank 56-work packet while keeping
full mapping and research execution explicitly gated.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
WORKBENCH = REPO / "wiki/survey/workbench/system-first-stage1c-v2-precalibration"
CHECK_DIR = REPO / "docs/checks/stage1c-v2-precalibration/2026-07-24-rc1"
AUTH_PATH = REPO / "wiki/audit/system-first-stage1c-v2-precalibration/owner-authorization/2026-07-24-owner-authorization.md"
FROZEN_REGISTRY_DIR = REPO / "wiki/survey/registry"
APPENDIX_PATH = REPO / "wiki/survey/current/stage1b-transition-reference-appendix.md"
PRIORITY_PATH = REPO / "wiki/survey/current/data/stage1c-common-rubric-comparison-v1.json"
CAPABILITY_PATH = REPO / "wiki/survey/workbench/system-first-stage1b-capability-delta/data/capability-delta-records-v1.json"
CAPABILITY_MANIFEST = REPO / "wiki/survey/workbench/system-first-stage1b-capability-delta/review-package-manifest.json"
TARGETED_PATH = REPO / "wiki/survey/workbench/system-first-stage1b-targeted-anchor-scan/targeted-anchor-scan-records-v1.json"
TARGETED_MANIFEST = REPO / "wiki/survey/workbench/system-first-stage1b-targeted-anchor-scan/review-package-manifest.json"
CAPABILITY_SIGNATURE_PATH = REPO / "wiki/audit/system-first-stage1b-capability-delta/release-signature/2026-07-24-stage1b-capability-delta-release-signature.md"
TARGETED_SIGNATURE_PATH = REPO / "wiki/audit/system-first-stage1b-targeted-anchor-scan/release-signature/2026-07-24-stage1b-targeted-anchor-scan-release-signature.md"
CAPABILITY_RELEASE_MANIFEST = REPO / "docs/checks/stage1b-capability-delta/2026-07-24-release/release-manifest.json"
TARGETED_RELEASE_MANIFEST = REPO / "docs/checks/stage1b-targeted-anchor-scan/2026-07-24-release/release-manifest.json"

OWNER_TOKEN = "AUTHORIZE_STAGE1C_V2_CALIBRATION_PREPARATION"
FROZEN_RELEASE = "38fb9435d0c35e226ad62b16015a6dbee054e6c2"
AUTH_BLOB = "f3c93d8a8f117167e6e56855125ba615b0c9706f"
CAPABILITY_MANIFEST_SHA256 = "ee8f0564069475f58f9be313a7978db662665d1d379b213d3005507c59dea3a6"
TARGETED_MANIFEST_SHA256 = "d70de83e36b4d2c07ae0ab02506b60269620bd5d5768d6ca7b8366d11818e0e6"
CAPABILITY_MANIFEST_GIT_BLOB = "a1c40548dc72a6d94859ce43efbeca65a0cf9366"
TARGETED_MANIFEST_GIT_BLOB = "af396aea51446c7cd7ac544aea5714090bdd5014"
CAPABILITY_SIGNATURE = "SIGN_STAGE1B_CAPABILITY_DELTA_RELEASE"
TARGETED_SIGNATURE = "SIGN_STAGE1B_TARGETED_ANCHOR_SCAN_RELEASE"
CAPABILITY_SIGNATURE_BLOB = "a5af670aacbb5194f42947150440cd022b16c652"
TARGETED_SIGNATURE_BLOB = "e5a039a9297fac3ce84ed981449f085d6bb79378"
FULL_MAPPING_SIGNATURE = "SIGN_STAGE1C_V2_EXPERIMENT_MAPPING"
FROZEN_RC1_COMMIT = "4eecb37440ecdf096b8a5e66fbeb7b698f54b633"

ARTIFACT_PATHS = {
    "bootstrap": WORKBENCH / "release-merge-manifest-v1.json",
    "crosswalk": WORKBENCH / "problem-intervention-crosswalk-v1.json",
    "pending_problem_routing": WORKBENCH / "pending-problem-routing-v1.json",
    "claims": WORKBENCH / "claim-registry-v1.json",
    "protocol_templates": WORKBENCH / "candidate-protocol-templates-v1.json",
    "translation_queue": WORKBENCH / "translation-contract-queue-v1.json",
    "schemas": WORKBENCH / "schema-bundle-v1.json",
    "calibration": WORKBENCH / "calibration-manifest-v1.json",
    "blind_packet": WORKBENCH / "calibration-blind-packet-v1.json",
    "agreement": WORKBENCH / "agreement-contract-v1.json",
    "reproduction_readiness": WORKBENCH / "reproduction-readiness-v1.json",
    "discovery_provenance": WORKBENCH / "discovery-provenance-v1.json",
    "release_receipts": WORKBENCH / "stage1b-overlay-release-receipts-v1.json",
}
REVIEW_MANIFEST_PATH = WORKBENCH / "review-package-manifest.json"

INTERVENTION_AXES = {
    "D0_SYSTEM_HARNESS", "D1_MULTIMODAL_KNOWLEDGE", "D2_MULTIMODAL_SKILL",
    "D3_MULTIMODAL_MEMORY", "D4_TF_RL_ORCHESTRATION",
}
CLAIM_SCOPE_FIELDS = (
    "problem_outcome", "task", "dataset_revision_split", "model", "access",
    "input_condition", "intervention", "budget_horizon", "evaluator",
)

SENTINELS: dict[str, str] = {
    "arxiv:2509.16971": "budget/stop direct speech control",
    "arxiv:2510.02995": "audio tool-use direct control",
    "arxiv:2512.16978": "training-free omni evidence seeking",
    "arxiv:2605.08762": "audio-driven search instrument",
    "arxiv:2607.07985": "audio-judge reliability instrument",
    "arxiv:2506.05984": "audio-aware judge instrument",
    "arxiv:2507.12705": "audio-judge boundary and evaluator disagreement",
    "arxiv:2305.13738": "earlier direct multimodal system path",
    "arxiv:2506.23049": "direct voice tool agent path",
    "arxiv:2510.07978": "voice-agent measurement instrument",
    "arxiv:2604.04847": "Full-Duplex-Bench v3 lineage and anchor hard case",
    "arxiv:2604.22821": "speech tool-use instrument with local assets",
    "arxiv:2606.19595": "interruption-recovery instrument",
    "acl:2026.findings-eacl.151": "TRACE evaluator decomposition",
    "acl:2026.acl-long.1615": "speech-native pairwise MM3/evaluator case",
    "arxiv:2508.18240": "multi-turn judge-bias instrument",
    "arxiv:2603.16924": "gray-box/model-internal boundary",
    "arxiv:2505.17862": "H5 withheld sentinel",
}
CALIBRATION_ONLY_TITLES = {
    "arxiv:2505.17862": "Daily-Omni: Towards Audio-Visual Reasoning with Temporal Alignment",
}

PENDING_ROUTES: dict[str, tuple[str, str]] = {
    "2512.14865": ("MEMORY_RETRIEVAL_TO_USE_AND_ACTION_GAP", "CANDIDATE_PROBLEM_NODE"),
    "2601.03515": ("MEMORY_RETRIEVAL_TO_USE_AND_ACTION_GAP", "CANDIDATE_PROBLEM_NODE"),
    "2601.19935": ("MEMORY_RETRIEVAL_TO_USE_AND_ACTION_GAP", "CANDIDATE_PROBLEM_NODE"),
    "2507.10859": ("ACTIVE_MULTIMODAL_EVIDENCE_ACQUISITION_UNDER_BUDGET", "CANDIDATE_PROBLEM_NODE"),
    "2604.15383": ("BUDGET_STOP_REPAIR", "BOUNDARY_TO_INHERITED_PROBLEM"),
    "2606.19341": ("ACTIVE_MULTIMODAL_EVIDENCE_ACQUISITION_UNDER_BUDGET", "CANDIDATE_PROBLEM_NODE"),
    "2602.03707": ("ACTIVE_MULTIMODAL_EVIDENCE_ACQUISITION_UNDER_BUDGET", "CANDIDATE_PROBLEM_NODE"),
    "2606.18448": ("SKILL_ACCESS_MAINTENANCE_AND_NEGATIVE_TRANSFER", "CANDIDATE_PROBLEM_NODE"),
    "2605.13716": ("SKILL_ACCESS_MAINTENANCE_AND_NEGATIVE_TRANSFER", "CANDIDATE_PROBLEM_NODE"),
    "2510.15421": ("ACTIVE_MULTIMODAL_EVIDENCE_ACQUISITION_UNDER_BUDGET", "CANDIDATE_PROBLEM_NODE"),
    "2604.25122": ("ACTIVE_MULTIMODAL_EVIDENCE_ACQUISITION_UNDER_BUDGET", "CANDIDATE_PROBLEM_NODE"),
    "2605.15019": ("ACTIVE_MULTIMODAL_EVIDENCE_ACQUISITION_UNDER_BUDGET", "CANDIDATE_PROBLEM_NODE"),
    "2605.13277": ("ACTIVE_MULTIMODAL_EVIDENCE_ACQUISITION_UNDER_BUDGET", "CANDIDATE_PROBLEM_NODE"),
    "2604.08064": ("MEMORY_RETRIEVAL_TO_USE_AND_ACTION_GAP", "CANDIDATE_PROBLEM_NODE"),
    "2601.01885": ("MEMORY_RETRIEVAL_TO_USE_AND_ACTION_GAP", "TRAINED_BOUNDARY_TO_CANDIDATE_PROBLEM"),
}

CLAIM_DEFINITIONS: dict[str, str] = {
    "CLM-MODALITY-NECESSITY": "Multimodal input presence does not establish that the non-text modality is causally necessary.",
    "CLM-RELEVANCE-UTILITY": "Evidence relevance and retrieval success do not guarantee decision utility or grounded use.",
    "CLM-ACTIVE-EVIDENCE": "Active evidence acquisition requires an observable acquire/select/stop decision under budget.",
    "CLM-SKILL-ACCESS": "Skill content, representation, retrieval, loading and use must be separated by matched controls.",
    "CLM-SKILL-LIFECYCLE": "Skill-library growth can create duplication, staleness and negative transfer unless maintenance is measured.",
    "CLM-MEMORY-USE": "Memory storage or retrieval does not establish that retrieved evidence changed the final action.",
    "CLM-MEMORY-UPDATE": "Memory update, conflict, deletion and refusal are distinct from stronger retrieval.",
    "CLM-TTS-NONMONOTONIC": "Additional inference-time sampling or refinement budget does not guarantee task improvement.",
    "CLM-EVALUATOR-DISAGREEMENT": "Online reward, primary task outcome and diagnostic judge must be independently identified.",
    "CLM-INTERACTION-OBJECTIVES": "Turn-taking quality, content correctness and terminal task success are distinct outcomes.",
    "CLM-ACCESS-BOUNDARY": "Black-box external control, gray-box decoding and parameter-trained policies are non-equivalent regimes.",
    "CLM-SYSTEM-ATTRIBUTION": "Bundled system gains cannot be assigned to K/S/M or control without component-matched comparisons.",
    "CLM-KNOWLEDGE-TO-SKILL": "Reusable skill value must be separated from raw-source retrieval and answer-bearing compression.",
}

CLAIM_LINKS: dict[str, tuple[str, ...]] = {
    "2405.20834": ("CLM-RELEVANCE-UTILITY", "CLM-ACTIVE-EVIDENCE"),
    "2602.07624": ("CLM-MEMORY-USE", "CLM-MEMORY-UPDATE", "CLM-MODALITY-NECESSITY"),
    "2603.12056": ("CLM-SKILL-ACCESS", "CLM-SKILL-LIFECYCLE"),
    "2603.28088": ("CLM-SYSTEM-ATTRIBUTION",),
    "2604.24594": ("CLM-SKILL-ACCESS",),
    "2605.13527": ("CLM-MODALITY-NECESSITY", "CLM-SKILL-ACCESS"),
    "2606.09316": ("CLM-KNOWLEDGE-TO-SKILL", "CLM-SKILL-ACCESS"),
    "2606.29538": ("CLM-KNOWLEDGE-TO-SKILL", "CLM-MODALITY-NECESSITY"),
    "2603.01145": ("CLM-SKILL-LIFECYCLE", "CLM-MEMORY-UPDATE"),
    "2604.03964": ("CLM-SKILL-LIFECYCLE", "CLM-KNOWLEDGE-TO-SKILL"),
    "2604.17308": ("CLM-SKILL-LIFECYCLE",),
    "2602.12670": ("CLM-SKILL-ACCESS", "CLM-SKILL-LIFECYCLE"),
    "2402.17753": ("CLM-MEMORY-USE", "CLM-MEMORY-UPDATE"),
    "2508.19828": ("CLM-MEMORY-UPDATE", "CLM-ACCESS-BOUNDARY"),
    "2512.14865": ("CLM-MEMORY-USE", "CLM-INTERACTION-OBJECTIVES", "CLM-EVALUATOR-DISAGREEMENT"),
    "2601.03515": ("CLM-MEMORY-USE", "CLM-MODALITY-NECESSITY"),
    "2601.19935": ("CLM-MEMORY-USE",),
    "2507.10859": ("CLM-MODALITY-NECESSITY",),
    "2510.11098": ("CLM-EVALUATOR-DISAGREEMENT", "CLM-INTERACTION-OBJECTIVES"),
    "2508.10015": ("CLM-INTERACTION-OBJECTIVES", "CLM-MODALITY-NECESSITY"),
    "2510.07838": ("CLM-INTERACTION-OBJECTIVES", "CLM-EVALUATOR-DISAGREEMENT"),
    "2601.09413": ("CLM-ACCESS-BOUNDARY", "CLM-TTS-NONMONOTONIC"),
    "2604.15383": ("CLM-ACCESS-BOUNDARY", "CLM-TTS-NONMONOTONIC"),
    "2510.20867": ("CLM-ACCESS-BOUNDARY", "CLM-EVALUATOR-DISAGREEMENT"),
    "2606.19341": ("CLM-ACTIVE-EVIDENCE", "CLM-SYSTEM-ATTRIBUTION", "CLM-MEMORY-UPDATE"),
    "2602.03707": ("CLM-ACTIVE-EVIDENCE", "CLM-ACCESS-BOUNDARY"),
    "2605.28020": ("CLM-TTS-NONMONOTONIC", "CLM-ACCESS-BOUNDARY"),
    "2606.06915": ("CLM-TTS-NONMONOTONIC", "CLM-ACCESS-BOUNDARY"),
    "2512.11109": ("CLM-TTS-NONMONOTONIC", "CLM-EVALUATOR-DISAGREEMENT"),
    "2505.00684": ("CLM-ACTIVE-EVIDENCE", "CLM-TTS-NONMONOTONIC"),
    "2606.18448": ("CLM-SKILL-ACCESS", "CLM-MODALITY-NECESSITY"),
    "2605.13716": ("CLM-SKILL-LIFECYCLE", "CLM-SKILL-ACCESS"),
    "2510.15421": ("CLM-ACTIVE-EVIDENCE", "CLM-TTS-NONMONOTONIC"),
    "2604.25122": ("CLM-ACTIVE-EVIDENCE", "CLM-RELEVANCE-UTILITY"),
    "2605.15019": ("CLM-RELEVANCE-UTILITY", "CLM-ACTIVE-EVIDENCE"),
    "2605.13277": ("CLM-RELEVANCE-UTILITY", "CLM-EVALUATOR-DISAGREEMENT"),
    "2604.08064": ("CLM-MEMORY-USE", "CLM-SKILL-ACCESS"),
    "2601.01885": ("CLM-MEMORY-UPDATE", "CLM-ACCESS-BOUNDARY"),
}

REMOTE_TARGETED = {
    "2601.03515", "2601.19935", "2605.28020", "2606.06915", "2512.11109",
    "2505.00684", "2606.18448", "2605.13716", "2510.15421", "2604.25122",
    "2605.15019", "2605.13277", "2604.08064",
}


class ContractError(RuntimeError):
    """Raised when a pre-calibration artifact violates the authorized contract."""


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ContractError(f"expected JSON object: {path}")
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob_id(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()


def canonical_from_work_id(work_id: str) -> str:
    if work_id.startswith("CW-ARXIV-"):
        return "arxiv:" + work_id.removeprefix("CW-ARXIV-")
    if work_id.startswith("CW-ACL-"):
        return "acl:" + work_id.removeprefix("CW-ACL-")
    raise ContractError(f"unsupported canonical work ID: {work_id}")


def frozen_registry_paths() -> list[Path]:
    paths = sorted(FROZEN_REGISTRY_DIR.glob("stage1b-bounded-*-papers.jsonl"))
    direct = FROZEN_REGISTRY_DIR / "stage1b-bounded-2026-07-22-papers.jsonl"
    if direct.exists():
        paths = sorted({*paths, direct})
    if len(paths) != 4:
        raise ContractError(f"expected four frozen registry shards; found {len(paths)}")
    return paths


def source_surfaces() -> dict[str, Any]:
    frozen_rows = [row for path in frozen_registry_paths() for row in load_jsonl(path)]
    frozen = {row["canonical_id"]: row.get("title", row["canonical_id"]) for row in frozen_rows}
    if len(frozen_rows) != 226 or len(frozen) != 226:
        raise ContractError("frozen registry is not exactly 226 unique works")

    appendix_text = APPENDIX_PATH.read_text(encoding="utf-8")
    appendix: dict[str, str] = {}
    for match in re.finditer(r"\|\s*<!-- work:(\d{4}\.\d{4,5}) -->[^|]*\|\s*([^|]+?)\s*\|", appendix_text):
        appendix[f"arxiv:{match.group(1)}"] = match.group(2).strip()
    if len(appendix) != 59:
        raise ContractError(f"CURRENT appendix is not 59 unique works: {len(appendix)}")

    priority_rows = load_json(PRIORITY_PATH)["priority_intake"]
    priority = {canonical_from_work_id(row["canonical_work_id"]): row["title"] for row in priority_rows}
    capability_package = load_json(CAPABILITY_PATH)
    capability = {
        canonical_from_work_id(row["canonical_work_id"]): row for row in capability_package["records"]
    }
    targeted_package = load_json(TARGETED_PATH)
    targeted = {
        canonical_from_work_id(row["canonical_work_id"]): row for row in targeted_package["records"]
    }
    return {
        "frozen": frozen, "appendix": appendix, "priority": priority,
        "capability": capability, "targeted": targeted,
        "capability_package": capability_package, "targeted_package": targeted_package,
    }


def build_release_receipts() -> dict[str, Any]:
    releases = [
        {
            "layer": "CAPABILITY_DELTA_14",
            "released_work_count": 14,
            "signature": CAPABILITY_SIGNATURE,
            "signature_artifact": CAPABILITY_SIGNATURE_PATH.relative_to(REPO).as_posix(),
            "signature_artifact_git_blob": CAPABILITY_SIGNATURE_BLOB,
            "review_manifest": CAPABILITY_MANIFEST.relative_to(REPO).as_posix(),
            "review_manifest_sha256": CAPABILITY_MANIFEST_SHA256,
            "review_manifest_git_blob": CAPABILITY_MANIFEST_GIT_BLOB,
            "release_manifest": CAPABILITY_RELEASE_MANIFEST.relative_to(REPO).as_posix(),
        },
        {
            "layer": "TARGETED_OVERLAY_24",
            "released_work_count": 24,
            "signature": TARGETED_SIGNATURE,
            "signature_artifact": TARGETED_SIGNATURE_PATH.relative_to(REPO).as_posix(),
            "signature_artifact_git_blob": TARGETED_SIGNATURE_BLOB,
            "review_manifest": TARGETED_MANIFEST.relative_to(REPO).as_posix(),
            "review_manifest_sha256": TARGETED_MANIFEST_SHA256,
            "review_manifest_git_blob": TARGETED_MANIFEST_GIT_BLOB,
            "release_manifest": TARGETED_RELEASE_MANIFEST.relative_to(REPO).as_posix(),
        },
    ]
    for release in releases:
        release.update({
            "signature_effective": True,
            "release_scope": "STAGE1C_CALIBRATION_INPUT_ONLY",
            "full_mapping_authorized": False,
            "research_execution_authorized": False,
        })
    return {
        "schema": "sf-stage1b-overlay-release-receipts-v1",
        "artifact_id": "SF-STAGE1B-TWO-OVERLAY-RELEASE-RECEIPTS-R1",
        "as_of": "2026-07-24",
        "status": "TWO_STAGE1B_OVERLAYS_SIGNED",
        "frozen_stage1b_v5_release": FROZEN_RELEASE,
        "releases": releases,
        "deterministic_merge": {
            "combined_unique_works": 320,
            "stage1c_calibration_input": True,
            "stage1c_full_mapping_input": False,
            "third_stage1b_scientific_signature_required": False,
        },
    }


def build_stage1b_release_manifests(receipts: dict[str, Any]) -> dict[Path, dict[str, Any]]:
    manifests: dict[Path, dict[str, Any]] = {}
    paths = {
        "CAPABILITY_DELTA_14": CAPABILITY_RELEASE_MANIFEST,
        "TARGETED_OVERLAY_24": TARGETED_RELEASE_MANIFEST,
    }
    for release in receipts["releases"]:
        layer = release["layer"]
        manifests[paths[layer]] = {
            "schema": "sf-stage1b-overlay-signed-release-manifest-v1",
            "artifact_id": f"SF-STAGE1B-{layer}-SIGNED-RELEASE-R1",
            "as_of": "2026-07-24",
            "status": "SIGNED_STAGE1B_OVERLAY_RELEASE",
            "layer": layer,
            "released_work_count": release["released_work_count"],
            "frozen_stage1b_v5_release": FROZEN_RELEASE,
            "review_manifest": release["review_manifest"],
            "review_manifest_sha256": release["review_manifest_sha256"],
            "review_manifest_git_blob": release["review_manifest_git_blob"],
            "signature": release["signature"],
            "signature_artifact": release["signature_artifact"],
            "signature_artifact_git_blob": release["signature_artifact_git_blob"],
            "authority_effect": "RELEASE_OVERLAY_TO_STAGE1C_CALIBRATION_INPUT_ONLY",
            "stage1c_full_mapping_authorized": False,
            "research_execution_authorized": False,
            "rc1_bytes_rewritten": False,
        }
    return manifests


def build_bootstrap(surfaces: dict[str, Any]) -> dict[str, Any]:
    frozen = set(surfaces["frozen"])
    appendix = set(surfaces["appendix"])
    priority = set(surfaces["priority"])
    capability = set(surfaces["capability"])
    targeted = set(surfaces["targeted"])
    inherited = frozen | appendix | priority
    candidate = inherited | capability | targeted
    checks = {
        "frozen_226": len(frozen) == 226,
        "appendix_59": len(appendix) == 59,
        "base_appendix_overlap_7": len(frozen & appendix) == 7,
        "priority_4_disjoint": len(priority) == 4 and not priority & (frozen | appendix),
        "inherited_282": len(inherited) == 282,
        "capability_14_disjoint": len(capability) == 14 and not capability & inherited,
        "targeted_24_disjoint": len(targeted) == 24 and not targeted & (inherited | capability),
        "candidate_320": len(candidate) == 320,
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise ContractError(f"bootstrap census failed: {failed}")
    titles: dict[str, str] = {}
    for layer in ("frozen", "appendix", "priority"):
        titles.update(surfaces[layer])
    titles.update({key: row["title"] for key, row in surfaces["capability"].items()})
    titles.update({key: row["title"] for key, row in surfaces["targeted"].items()})
    works = []
    for canonical_id in sorted(candidate):
        layers = []
        if canonical_id in frozen:
            layers.append("FROZEN_226")
        if canonical_id in appendix:
            layers.append("CURRENT_APPENDIX_59")
        if canonical_id in priority:
            layers.append("CURRENT_PRIORITY_4")
        if canonical_id in capability:
            layers.append("CAPABILITY_DELTA_14_SIGNED")
        if canonical_id in targeted:
            layers.append("TARGETED_OVERLAY_24_SIGNED")
        works.append({"canonical_id": canonical_id, "title": titles[canonical_id], "source_layers": layers})
    return {
        "schema": "sf-stage1c-v2-release-merge-manifest-v1",
        "artifact_id": "SF-STAGE1C-V2-SIGNED-CALIBRATION-INPUT-320-R1",
        "as_of": "2026-07-24",
        "status": "SIGNED_CALIBRATION_INPUT_AWAITING_INDEPENDENT_CODERS",
        "stage1c_calibration_input": True,
        "stage1c_mapping_input": False,
        "counts": {
            "frozen_base": 226, "inherited_union": 282, "capability_delta": 14,
            "targeted_overlay": 24, "candidate_union": 320,
        },
        "release_layers": [
            {"layer": "FROZEN_226", "identity": FROZEN_RELEASE, "signed": True},
            {"layer": "INHERITED_282", "identity": "CURRENT_DEDUPLICATED_UNION", "signed": True},
            {"layer": "CAPABILITY_DELTA_14", "manifest_sha256": CAPABILITY_MANIFEST_SHA256,
             "signature": CAPABILITY_SIGNATURE, "signature_artifact_git_blob": CAPABILITY_SIGNATURE_BLOB,
             "signed": True},
            {"layer": "TARGETED_OVERLAY_24", "manifest_sha256": TARGETED_MANIFEST_SHA256,
             "signature": TARGETED_SIGNATURE, "signature_artifact_git_blob": TARGETED_SIGNATURE_BLOB,
             "signed": True},
        ],
        "merge_requires_third_stage1b_scientific_signature": False,
        "checks": checks,
        "works": works,
    }


def build_crosswalk() -> dict[str, Any]:
    nodes = [
        ("BUDGET_STOP_REPAIR", "INHERITED_CANDIDATE", ["D0_SYSTEM_HARNESS", "D1_MULTIMODAL_KNOWLEDGE", "D3_MULTIMODAL_MEMORY", "D4_TF_RL_ORCHESTRATION"]),
        ("EVALUATOR_REWARD_RELIABILITY", "INHERITED_CANDIDATE", ["D0_SYSTEM_HARNESS", "D1_MULTIMODAL_KNOWLEDGE", "D4_TF_RL_ORCHESTRATION"]),
        ("INTERACTIVE_FULL_DUPLEX_OBJECTIVES", "INHERITED_CANDIDATE", ["D0_SYSTEM_HARNESS", "D3_MULTIMODAL_MEMORY", "D4_TF_RL_ORCHESTRATION"]),
        ("ACTIVE_MULTIMODAL_EVIDENCE_ACQUISITION_UNDER_BUDGET", "UNRANKED_CANDIDATE", ["D0_SYSTEM_HARNESS", "D1_MULTIMODAL_KNOWLEDGE", "D3_MULTIMODAL_MEMORY", "D4_TF_RL_ORCHESTRATION"]),
        ("SKILL_ACCESS_MAINTENANCE_AND_NEGATIVE_TRANSFER", "UNRANKED_CANDIDATE", ["D0_SYSTEM_HARNESS", "D2_MULTIMODAL_SKILL", "D3_MULTIMODAL_MEMORY", "D4_TF_RL_ORCHESTRATION"]),
        ("MEMORY_RETRIEVAL_TO_USE_AND_ACTION_GAP", "UNRANKED_CANDIDATE", ["D0_SYSTEM_HARNESS", "D3_MULTIMODAL_MEMORY", "D4_TF_RL_ORCHESTRATION"]),
    ]
    return {
        "schema": "sf-stage1c-v2-problem-intervention-crosswalk-v1",
        "problem_nodes_are_primary_organization_axis": False,
        "organization_rule": "EXPERIMENT_AND_CLAIM_EVIDENCE_LED_FAMILIES",
        "intervention_axes": [
            {"axis_id": axis, "type": "INTERVENTION_NOT_PROBLEM"} for axis in sorted(INTERVENTION_AXES)
        ],
        "problem_nodes": [
            {"problem_id": problem, "problem_status": status, "ranked": False,
             "allowed_intervention_axes": axes, "family_count_pre_registered": 0}
            for problem, status, axes in nodes
        ],
    }


def build_pending_routing(surfaces: dict[str, Any]) -> dict[str, Any]:
    targeted = surfaces["targeted"]
    pending = {
        key.removeprefix("arxiv:") for key, row in targeted.items()
        if "NEW_PROBLEM_HYPOTHESIS_PENDING_OWNER" in row["problem_axis"]
    }
    if pending != set(PENDING_ROUTES):
        raise ContractError("pending-problem source set changed")
    routes = []
    for identity, (problem, disposition) in sorted(PENDING_ROUTES.items()):
        routes.append({
            "canonical_work_id": f"CW-ARXIV-{identity}", "target_problem_id": problem,
            "route_disposition": disposition, "candidate_problem_promoted": False,
            "ranking_or_selection_performed": False,
        })
    return {"schema": "sf-stage1c-v2-pending-problem-routing-v1", "routes": routes}


def overlay_records(surfaces: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        **{key.removeprefix("arxiv:"): value for key, value in surfaces["capability"].items()},
        **{key.removeprefix("arxiv:"): value for key, value in surfaces["targeted"].items()},
    }


def build_claim_registry(surfaces: dict[str, Any]) -> dict[str, Any]:
    records = overlay_records(surfaces)
    if set(records) != set(CLAIM_LINKS):
        raise ContractError("claim-link overlay identity set changed")
    claims = []
    for claim_id, text in sorted(CLAIM_DEFINITIONS.items()):
        claims.append({
            "claim_id": claim_id,
            "claim_text": text,
            "claim_origin": "CROSS_PAPER_SYNTHESIS",
            "primary_owner_work_id": None,
            "origin_work_ids": sorted(identity for identity, ids in CLAIM_LINKS.items() if claim_id in ids),
            "scope": {field: "DECLARED_HETEROGENEOUS_STRATA_NO_NUMERIC_POOLING" for field in CLAIM_SCOPE_FIELDS},
            "evidence_level": "CALIBRATION_REQUIRED",
            "transfer_status": "WITHHELD_PENDING_SCOPE_AND_TRANSLATION_REVIEW",
            "decision_impact": "DEDUPE_SEEDS_AND_ROUTE_SUPPORT_BOUNDARY_FALSIFIER",
        })
    links = []
    for identity, claim_ids in sorted(CLAIM_LINKS.items()):
        record = records[identity]
        role = record["stage1b_role"]
        relation = (
            "BOUNDARY_OR_FALSIFIER" if role in {"BOUNDARY", "NEGATIVE_OR_FALSIFIER"}
            else "INSTRUMENT_SUPPORT" if role == "INSTRUMENT"
            else "SUPPORT"
        )
        for claim_id in claim_ids:
            links.append({
                "canonical_work_id": f"CW-ARXIV-{identity}", "claim_id": claim_id,
                "evidence_relation": relation, "load_bearing_before_calibration": False,
            })
    package = {
        "schema": "sf-stage1c-v2-claim-registry-v1", "claims": claims,
        "paper_to_claim_links": links,
        "dedupe_rule": "ONE_CANONICAL_CLAIM_ID_PER_SCOPE_COMPATIBLE_PROPOSITION",
    }
    validate_claim_registry(package, {f"CW-ARXIV-{identity}" for identity in records})
    return package


def validate_claim_registry(package: dict[str, Any], expected_overlay_ids: set[str]) -> None:
    claims = package.get("claims", [])
    claim_ids = [row.get("claim_id") for row in claims]
    if len(claim_ids) != len(set(claim_ids)):
        raise ContractError("duplicate canonical claim IDs")
    if any(set(CLAIM_SCOPE_FIELDS) - set(row.get("scope", {})) for row in claims):
        raise ContractError("claim scope is incomplete")
    known = set(claim_ids)
    links = package.get("paper_to_claim_links", [])
    if any(row.get("claim_id") not in known for row in links):
        raise ContractError("paper-to-claim link references unknown claim")
    linked = {row.get("canonical_work_id") for row in links}
    if linked != expected_overlay_ids:
        raise ContractError("claim registry does not cover exactly all overlay records")


def build_protocol_templates() -> dict[str, Any]:
    templates = [
        ("F0", "Frozen-core system harness isolation", "D0_SYSTEM_HARNESS"),
        ("FK1", "Speech/omni evidence necessity", "D1_MULTIMODAL_KNOWLEDGE"),
        ("FK2", "Declarative knowledge to reusable skill compilation", "D1_MULTIMODAL_KNOWLEDGE"),
        ("FS1", "Multimodal skill package factorial", "D2_MULTIMODAL_SKILL"),
        ("FS2", "Skill lifecycle, repair and negative transfer", "D2_MULTIMODAL_SKILL"),
        ("FM1", "Evidence-preserving multimodal memory carrier", "D3_MULTIMODAL_MEMORY"),
        ("FM2", "Memory update, conflict, decay and refusal", "D3_MULTIMODAL_MEMORY"),
        ("FR1", "Training-free reward-guided K/S/M orchestration", "D4_TF_RL_ORCHESTRATION"),
    ]
    return {
        "schema": "sf-stage1c-v2-candidate-protocol-templates-v1",
        "templates": [
            {"template_id": key, "title": title, "intervention_axis": axis,
             "status": "CANDIDATE_PROTOCOL_TEMPLATE", "branch_created": False,
             "family_membership_claimed": False, "may_merge_split_or_remain_unrouted": True}
            for key, title, axis in templates
        ],
    }


def build_translation_queue(surfaces: dict[str, Any]) -> dict[str, Any]:
    capability_borrowed = {
        key.removeprefix("arxiv:") for key, row in surfaces["capability"].items()
        if row["project_use_contract"]["primary_relation"] == "BORROWED_PROTOCOL_ANALOGUE"
    }
    identities = sorted(capability_borrowed | REMOTE_TARGETED)
    records = overlay_records(surfaces)
    contracts = []
    for identity in identities:
        record = records[identity]
        direction = record["capability_mapping"]["primary_direction"]
        contracts.append({
            "translation_id": f"TR-{identity}", "source_work_id": f"CW-ARXIV-{identity}",
            "borrowed_decision_structure": record["project_use_contract"]["reason"],
            "source_to_target_changes": ["task/data", "speech_or_omni_modality", "model/access", "evaluator/budget"],
            "speech_omni_corresponding_variable": f"{direction}_INTERVENTION_WITH_MATCHED_ACCESS_AND_BUDGET",
            "strongest_transfer_failure": record["strongest_boundary_or_falsifier"],
            "rejection_observation": "Matched speech/omni arm shows no task-grounded effect or violates the declared access contract.",
            "load_bearing_status": "WITHHELD_PENDING_TRANSLATION",
        })
    return {"schema": "sf-stage1c-v2-translation-contract-queue-v1", "contracts": contracts}


def object_schema(required: list[str], properties: dict[str, Any]) -> dict[str, Any]:
    return {"type": "object", "additionalProperties": False, "required": required, "properties": properties}


def string_prop() -> dict[str, str]:
    return {"type": "string", "minLength": 1}


def build_schemas() -> dict[str, Any]:
    s = string_prop()
    defs = {
        "paper_audit": object_schema(
            ["paper_id", "disposition", "role", "source_locators", "coder_id", "review_status"],
            {"paper_id": s, "disposition": s, "role": s, "source_locators": {"type": "array", "items": s}, "coder_id": s, "review_status": s},
        ),
        "run_cell": object_schema(
            ["run_cell_id", "paper_id", "dataset_revision_split", "model_access", "input_condition", "intervention", "budget_horizon", "source_locator"],
            {key: s for key in ["run_cell_id", "paper_id", "dataset_revision_split", "model_access", "input_condition", "intervention", "budget_horizon", "source_locator"]},
        ),
        "observation": object_schema(
            ["observation_id", "run_cell_id", "metric_evaluator", "raw_result", "source_locator"],
            {key: s for key in ["observation_id", "run_cell_id", "metric_evaluator", "raw_result", "source_locator"]},
        ),
        "paired_comparison": object_schema(
            ["comparison_id", "baseline_cell_id", "intervention_cell_id", "paired_status", "comparability_key"],
            {key: s for key in ["comparison_id", "baseline_cell_id", "intervention_cell_id", "paired_status", "comparability_key"]},
        ),
        "dataset_node": object_schema(
            ["dataset_id", "name", "revision", "split", "source_locator"],
            {key: s for key in ["dataset_id", "name", "revision", "split", "source_locator"]},
        ),
        "dataset_lineage_edge": object_schema(
            ["edge_id", "source_dataset_id", "relation", "target_dataset_id", "source_locator"],
            {key: s for key in ["edge_id", "source_dataset_id", "relation", "target_dataset_id", "source_locator"]},
        ),
        "dataset_relation_edge": object_schema(
            ["edge_id", "source_dataset_id", "relation", "target_dataset_id", "reason"],
            {key: s for key in ["edge_id", "source_dataset_id", "relation", "target_dataset_id", "reason"]},
        ),
        "claim_record": object_schema(
            ["claim_id", "claim_text", "claim_origin", "scope", "evidence_level", "transfer_status"],
            {"claim_id": s, "claim_text": s, "claim_origin": s, "scope": {"type": "object"}, "evidence_level": s, "transfer_status": s},
        ),
        "family_record": object_schema(
            ["family_id", "problem_statement", "protocol_signature", "evidence_state", "strongest_contradiction", "uncertainty"],
            {key: s for key in ["family_id", "problem_statement", "protocol_signature", "evidence_state", "strongest_contradiction", "uncertainty"]},
        ),
        "family_membership": object_schema(
            ["membership_id", "family_id", "evidence_object_id", "membership_type", "compatibility_decision"],
            {key: s for key in ["membership_id", "family_id", "evidence_object_id", "membership_type", "compatibility_decision"]},
        ),
        "review_event": object_schema(
            ["event_id", "object_id", "coder_id", "event_type", "timestamp", "prior_event_id"],
            {key: s for key in ["event_id", "object_id", "coder_id", "event_type", "timestamp", "prior_event_id"]},
        ),
        "translation_contract": object_schema(
            ["translation_id", "source_work_id", "borrowed_decision_structure", "source_to_target_changes", "speech_omni_corresponding_variable", "strongest_transfer_failure", "rejection_observation"],
            {"translation_id": s, "source_work_id": s, "borrowed_decision_structure": s, "source_to_target_changes": {"type": "array", "items": s}, "speech_omni_corresponding_variable": s, "strongest_transfer_failure": s, "rejection_observation": s},
        ),
    }
    return {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "sf-stage1c-v2-schema-bundle-v1", "$defs": defs}


def build_calibration(bootstrap: dict[str, Any], surfaces: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    overlay_ids = sorted(
        [f"CW-ARXIV-{key.removeprefix('arxiv:')}" for key in surfaces["capability"]]
        + [f"CW-ARXIV-{key.removeprefix('arxiv:')}" for key in surfaces["targeted"]]
    )
    sentinel_ids = sorted(SENTINELS)
    bootstrap_ids = {row["canonical_id"] for row in bootstrap["works"]}
    outside_candidate = sorted(set(sentinel_ids) - bootstrap_ids)
    if outside_candidate != ["arxiv:2505.17862"]:
        raise ContractError(f"unexpected calibration-only identities outside bootstrap: {outside_candidate}")
    canonical_ids = sorted(
        [canonical_from_work_id(value) for value in overlay_ids] + sentinel_ids
    )
    if len(canonical_ids) != 56 or len(set(canonical_ids)) != 56:
        raise ContractError("calibration packet must be exactly 56 unique works")
    calibration = {
        "schema": "sf-stage1c-v2-calibration-manifest-v1",
        "artifact_id": "SF-STAGE1C-V2-CALIBRATION-PACKET-56-RC1",
        "status": "READY_FOR_INDEPENDENT_CODERS_NOT_EXECUTED",
        "two_stage1b_release_signatures_effective": True,
        "N": 56, "overlay_record_count": 38, "inherited_sentinel_count": 18,
        "canonical_ids": canonical_ids,
        "overlay_ids": overlay_ids,
        "outside_candidate_union_calibration_only": outside_candidate,
        "inherited_sentinels": [
            {"canonical_id": key, "selection_rationale": value} for key, value in sorted(SENTINELS.items())
        ],
        "coder_a_completed": False, "coder_b_completed": False, "adjudication_completed": False,
        "agreement_computed": False,
    }
    title_map = {row["canonical_id"]: row["title"] for row in bootstrap["works"]}
    title_map.update(CALIBRATION_ONLY_TITLES)
    items = []
    for canonical_id in canonical_ids:
        identity = canonical_id.split(":", 1)[1]
        items.append({
            "packet_item_id": f"CAL-{identity}", "canonical_id": canonical_id,
            "title": title_map[canonical_id],
            "fulltext_locator": f"${{SPEECHRL_DATA_DIR}}/survey-fulltext/{identity}/{identity}.pdf",
            "blank_response": {
                "paper_disposition": None, "paper_role": None, "problem_nodes": [],
                "intervention_axes": [], "mm_level": None, "run_cell_boundary": None,
                "paired_status": None, "claim_links": [], "protocol_template_links": [],
                "reference_borrow_reproduce": None, "notes_with_source_locators": [],
            },
        })
    blind = {
        "schema": "sf-stage1c-v2-calibration-blind-packet-v1",
        "purpose": "LABEL_HIDDEN_SECONDARY_CODER_INPUT",
        "contains_prior_labels": False,
        "repository_access_should_be_withheld": True,
        "items": items,
    }
    return calibration, blind


def build_agreement() -> dict[str, Any]:
    return {
        "schema": "sf-stage1c-v2-agreement-contract-v1",
        "minimum_raw_agreement": 0.85,
        "agreement_is_per_critical_field_not_global_only": True,
        "metrics": {
            "nominal_single_label": ["RAW_AGREEMENT", "GWET_AC1"],
            "ordinal": ["RAW_AGREEMENT", "WEIGHTED_GWET_AC2"],
            "multilabel": ["EXACT_MATCH", "JACCARD", "MICRO_AND_MACRO_F1"],
        },
        "critical_fields": [
            "paper_disposition", "paper_role", "problem_nodes", "intervention_axes", "mm_level",
            "reference_borrow_reproduce", "run_cell_boundary", "paired_status", "lineage_relation",
            "core_member_compatibility",
        ],
        "maximum_codebook_consolidations": 1,
        "full_packet_recode_after_consolidation": True,
        "all_disagreements_adjudicated": True,
        "calibration_records_may_not_count_as_later_blind_review": True,
        "later_full_mapping_blind_review": {
            "minimum_unique_works": 64,
            "sampling_seed": 20260724,
            "algorithm": "SOURCE_ROLE_PROBLEM_MM_STRATIFIED_SHA256_ORDER_WITHOUT_REPLACEMENT",
            "exclude_calibration_records": True,
            "materialization_status": "WITHHELD_UNTIL_SIGNED_320_INPUT_AND_MAPPING_SIGNATURE",
        },
    }


def build_reproduction_readiness() -> dict[str, Any]:
    ordered = [
        ("CW-ARXIV-2510.07838", "Full-Duplex-Bench-v2", ["v2/v3 lineage", "WebRTC examiner", "data revision", "code entrypoint", "evaluator independence"]),
        ("CW-ARXIV-2512.14865", "Audio MultiChallenge", ["data revision", "rubric/judge", "license/terms", "fixed-context final-turn protocol", "loader slice"]),
        ("CW-ARXIV-2507.10859", "MultiVox", ["paired assets", "speech/visual matching", "license/terms", "loader slice", "MM3 evaluator"]),
        ("CW-ARXIV-2510.11098", "VCB Bench", ["data revision", "judge implementation", "license/terms", "robustness slice", "outcome independence"]),
        ("CW-ARXIV-2508.10015", "RealTalk-CN", ["data revision", "Chinese domain fit", "license/terms", "loader", "modality-switch evaluator"]),
    ]
    return {
        "schema": "sf-stage1c-v2-reproduction-readiness-v1",
        "primary_selection": "WITHHELD_PENDING_READ_ONLY_CLOSURE",
        "fallback_selection": "WITHHELD_PENDING_READ_ONLY_CLOSURE",
        "selection_rule": "SELECT_ONE_PRIMARY_AND_ONE_FALLBACK_ONLY_AFTER_ALL_CHECKLISTS_ARE_EVIDENCE_BOUND",
        "candidates": [
            {"closure_order": index, "canonical_work_id": work_id, "title": title,
             "status": "CANDIDATE_NOT_ANCHOR", "required_read_only_closure": checklist,
             "deviation_ledger_required_before_stage2a": True}
            for index, (work_id, title, checklist) in enumerate(ordered, 1)
        ],
    }


def build_discovery_provenance() -> dict[str, Any]:
    return {
        "schema": "sf-stage1b-targeted-discovery-provenance-v1",
        "status": "PARTIAL_RECONSTRUCTION_NOT_SYSTEMATIC_REVIEW",
        "date_local": "2026-07-24",
        "source_surfaces": ["web search discovery", "official arXiv abstract/PDF/e-print pages", "existing corpus exact-ID dedupe"],
        "query_families": [
            "speech/omni multimodal agent memory benchmark", "multimodal skill and visual skill agent",
            "active multimodal evidence acquisition", "training-free reward-guided decoding and test-time scaling",
            "full-duplex voice-agent benchmark", "memory retrieval-to-action agent benchmark",
        ],
        "exact_query_log_retained": False,
        "candidate_pool_size_retained": False,
        "auditable_surface": "26_EXACT_IDS_ONLY",
        "promotion_rule": "TASK_MATCHED_ANCHOR_OR_PATH_CHANGING_METHOD_OR_PROTOCOL_INSTRUMENT_OR_MATERIAL_FALSIFIER",
        "stop_rule": "STOP_BROAD_EXPANSION_AFTER_DIRECT_SPEECH_OMNI_AND_KSM_PROTOCOL_GAPS_BECAME_BOUNDED",
        "future_trigger_rule": "SEARCH_ONLY_IF_NEW_WORK_CHANGES_METHOD_PATH_FALSIFIES_LOAD_BEARING_PREMISE_OR_CLOSES_DIRECT_REPRODUCTION_ANCHOR",
        "literature_universe_closed": False,
    }


def build_package() -> dict[str, Any]:
    if git_blob_id(AUTH_PATH) != AUTH_BLOB:
        raise ContractError("owner authorization artifact bytes changed")
    if sha256_path(CAPABILITY_MANIFEST) != CAPABILITY_MANIFEST_SHA256:
        raise ContractError("capability-delta manifest bytes changed")
    if sha256_path(TARGETED_MANIFEST) != TARGETED_MANIFEST_SHA256:
        raise ContractError("targeted-anchor manifest bytes changed")
    if git_blob_id(CAPABILITY_MANIFEST) != CAPABILITY_MANIFEST_GIT_BLOB:
        raise ContractError("capability-delta reviewed manifest Git blob changed")
    if git_blob_id(TARGETED_MANIFEST) != TARGETED_MANIFEST_GIT_BLOB:
        raise ContractError("targeted-anchor reviewed manifest Git blob changed")
    if git_blob_id(CAPABILITY_SIGNATURE_PATH) != CAPABILITY_SIGNATURE_BLOB:
        raise ContractError("capability-delta release signature artifact bytes changed")
    if git_blob_id(TARGETED_SIGNATURE_PATH) != TARGETED_SIGNATURE_BLOB:
        raise ContractError("targeted-anchor release signature artifact bytes changed")
    surfaces = source_surfaces()
    bootstrap = build_bootstrap(surfaces)
    calibration, blind = build_calibration(bootstrap, surfaces)
    overlay_ids = sorted(
        [row["canonical_work_id"] for row in surfaces["capability"].values()]
        + [row["canonical_work_id"] for row in surfaces["targeted"].values()]
    )
    return {
        "bootstrap": bootstrap,
        "crosswalk": build_crosswalk(),
        "pending_problem_routing": build_pending_routing(surfaces),
        "claims": build_claim_registry(surfaces),
        "protocol_templates": build_protocol_templates(),
        "translation_queue": build_translation_queue(surfaces),
        "schemas": build_schemas(),
        "calibration": calibration,
        "blind_packet": blind,
        "agreement": build_agreement(),
        "reproduction_readiness": build_reproduction_readiness(),
        "discovery_provenance": build_discovery_provenance(),
        "release_receipts": build_release_receipts(),
        "overlay_ids": overlay_ids,
    }


def load_package() -> dict[str, Any]:
    values = {name: load_json(path) for name, path in ARTIFACT_PATHS.items()}
    values["overlay_ids"] = sorted(values["calibration"]["overlay_ids"])
    return values


def validate_package(package: dict[str, Any]) -> None:
    bootstrap = package["bootstrap"]
    if (
        bootstrap["status"] != "SIGNED_CALIBRATION_INPUT_AWAITING_INDEPENDENT_CODERS"
        or not bootstrap["stage1c_calibration_input"]
        or bootstrap["stage1c_mapping_input"]
    ):
        raise ContractError("signed calibration input/full-mapping boundary changed")
    if not all(row["signed"] for row in bootstrap["release_layers"]):
        raise ContractError("a Stage-1B release layer is not signed")
    receipts = package["release_receipts"]
    if receipts["status"] != "TWO_STAGE1B_OVERLAYS_SIGNED" or len(receipts["releases"]) != 2:
        raise ContractError("two independent Stage-1B release receipts are not present")
    if any(
        not row["signature_effective"]
        or row["full_mapping_authorized"]
        or row["research_execution_authorized"]
        for row in receipts["releases"]
    ):
        raise ContractError("Stage-1B release receipt authority boundary changed")
    validate_claim_registry(package["claims"], set(package["overlay_ids"]))
    schema_names = set(package["schemas"].get("$defs", {}))
    expected_schema_names = {
        "paper_audit", "run_cell", "observation", "paired_comparison", "dataset_node",
        "dataset_lineage_edge", "dataset_relation_edge", "claim_record", "family_record",
        "family_membership", "review_event", "translation_contract",
    }
    if schema_names != expected_schema_names:
        raise ContractError("whole-package schema surface changed")
    calibration = package["calibration"]
    if calibration["N"] != 56 or calibration["coder_a_completed"] or calibration["coder_b_completed"]:
        raise ContractError("calibration packet count/status invalid")
    if calibration["agreement_computed"] or calibration["adjudication_completed"]:
        raise ContractError("unexecuted calibration claims a result")
    if set(calibration["canonical_ids"]) != {row["canonical_id"] for row in package["blind_packet"]["items"]}:
        raise ContractError("blind packet differs from calibration manifest")
    if any(row["load_bearing_status"] != "WITHHELD_PENDING_TRANSLATION" for row in package["translation_queue"]["contracts"]):
        raise ContractError("remote analogue became load-bearing before translation")
    if any(row["status"] != "CANDIDATE_NOT_ANCHOR" for row in package["reproduction_readiness"]["candidates"]):
        raise ContractError("reproduction candidate was promoted without closure")


def build_report(package: dict[str, Any]) -> dict[str, Any]:
    validate_package(package)
    return {
        "schema": "sf-stage1c-v2-precalibration-contract-report-v1",
        "artifact_id": "SF-STAGE1C-V2-PRECALIBRATION-CONTRACT-REPORT-RC1",
        "as_of": "2026-07-24",
        "status": "SIGNED_320_CALIBRATION_INPUT_AWAITING_INDEPENDENT_CODERS",
        "authority": {
            "owner_token": OWNER_TOKEN,
            "owner_authorization_git_blob": AUTH_BLOB,
            "capability_delta_signed": True,
            "targeted_anchor_signed": True,
            "full_mapping_signed": False,
            "research_execution_authorized": False,
        },
        "surface": {
            "candidate_union": package["bootstrap"]["counts"]["candidate_union"],
            "claims": len(package["claims"]["claims"]),
            "claim_links": len(package["claims"]["paper_to_claim_links"]),
            "translation_contracts_pending": len(package["translation_queue"]["contracts"]),
            "candidate_protocol_templates": len(package["protocol_templates"]["templates"]),
            "pending_problem_routes_closed": len(package["pending_problem_routing"]["routes"]),
            "calibration_N": package["calibration"]["N"],
            "reproduction_anchors": 0,
        },
        "acceptance_checks": {
            "owner_authority_byte_bound": True,
            "two_stage1b_release_signatures_byte_bound_and_effective": True,
            "signed_320_limited_to_calibration_input": True,
            "full_320_mapping_still_withheld": True,
            "all_38_overlay_records_claim_linked": True,
            "all_15_pending_problem_labels_routed_without_promotion": True,
            "old_eight_families_demoted_to_templates": True,
            "remote_analogues_withheld_pending_translation": True,
            "whole_package_schemas_present": True,
            "exact_56_work_calibration_packet_prepared": True,
            "calibration_not_fabricated_or_executed": True,
            "five_reproduction_candidates_remain_non_anchors": True,
            "no_model_metric_reproduction_prototype_or_novelty_verdict": True,
        },
    }


def canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def build_review_manifest(report: dict[str, Any]) -> dict[str, Any]:
    paths = [
        WORKBENCH / "README.md", WORKBENCH / "stage1c-v2-precalibration-contract-zh.md",
        WORKBENCH / "codebook-v1.md", AUTH_PATH, CAPABILITY_SIGNATURE_PATH,
        TARGETED_SIGNATURE_PATH, CAPABILITY_RELEASE_MANIFEST, TARGETED_RELEASE_MANIFEST,
        REPO / "scripts/survey/sf_stage1c_v2_precalibration.py",
        REPO / "scripts/survey/test_sf_stage1c_v2_precalibration.py",
        *ARTIFACT_PATHS.values(), CHECK_DIR / "contract-report.json",
    ]
    missing = [path for path in paths if not path.is_file()]
    if missing:
        raise ContractError(f"review-package inputs missing: {missing}")
    return {
        "schema": "sf-stage1c-v2-precalibration-review-manifest-v1",
        "artifact_id": "SF-STAGE1C-V2-PRECALIBRATION-REVIEW-PACKAGE-RC1",
        "status": report["status"],
        "owner_token": OWNER_TOKEN,
        "artifact_count": len(paths),
        "artifacts": [
            {"path": path.relative_to(REPO).as_posix(), "bytes": path.stat().st_size, "sha256": sha256_path(path)}
            for path in paths
        ],
        "authority_withheld": [
            FULL_MAPPING_SIGNATURE,
            "320_paper_full_mapping", "research_execution", "problem_selection", "novelty_verdict",
        ],
    }


def validate_superseded_rc1_review_manifest() -> None:
    """Verify RC1 without making its historical manifest follow the mutable RC2 router.

    RC1 included the workbench README in its exact review package.  Once RC2 supersedes the
    active README, RC1 must verify that one path at its original commit rather than rewriting
    the registered RC1 manifest.  All other RC1 artifact paths remain present and byte-stable.
    """
    manifest = load_json(REVIEW_MANIFEST_PATH)
    for artifact in manifest["artifacts"]:
        relative = artifact["path"]
        path = REPO / relative
        raw = path.read_bytes() if path.is_file() else b""
        matches = len(raw) == artifact["bytes"] and hashlib.sha256(raw).hexdigest() == artifact["sha256"]
        if not matches:
            completed = subprocess.run(
                ["git", "show", f"{FROZEN_RC1_COMMIT}:{relative}"], cwd=REPO,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
            if completed.returncode == 0:
                raw = completed.stdout
                matches = len(raw) == artifact["bytes"] and hashlib.sha256(raw).hexdigest() == artifact["sha256"]
        if not matches:
            raise ContractError(f"frozen RC1 review artifact cannot be reproduced: {relative}")


def run(*, write: bool) -> dict[str, Any]:
    expected = build_package()
    validate_package(expected)
    report = build_report(expected)
    release_manifests = build_stage1b_release_manifests(expected["release_receipts"])
    if write:
        for name, path in ARTIFACT_PATHS.items():
            write_json(path, expected[name])
        for path, release_manifest in release_manifests.items():
            write_json(path, release_manifest)
        write_json(CHECK_DIR / "contract-report.json", report)
        write_json(REVIEW_MANIFEST_PATH, build_review_manifest(report))
    else:
        actual = load_package()
        validate_package(actual)
        for name in ARTIFACT_PATHS:
            if actual[name] != expected[name]:
                raise ContractError(f"materialized artifact is stale: {ARTIFACT_PATHS[name]}")
        if load_json(CHECK_DIR / "contract-report.json") != report:
            raise ContractError("contract report is stale")
        for path, release_manifest in release_manifests.items():
            if load_json(path) != release_manifest:
                raise ContractError(f"signed Stage-1B release manifest is stale: {path}")
        if (WORKBENCH / "review-package-manifest-rc2.json").is_file():
            validate_superseded_rc1_review_manifest()
        elif load_json(REVIEW_MANIFEST_PATH) != build_review_manifest(report):
            raise ContractError("review-package manifest is stale")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    try:
        report = run(write=args.write)
    except ContractError as error:
        print(f"FAIL: {error}")
        return 1
    print(canonical_json({
        "status": report["status"], "candidate_union": report["surface"]["candidate_union"],
        "calibration_N": report["surface"]["calibration_N"],
        "full_mapping_signed": report["authority"]["full_mapping_signed"],
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
