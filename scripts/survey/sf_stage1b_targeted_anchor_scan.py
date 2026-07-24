#!/usr/bin/env python3
"""Verify the unsigned Stage-1B targeted-anchor literature-scan overlay.

This transaction records primary-source reading and paper-reported evidence only.  It
cannot sign either Stage-1B overlay, activate Stage-1C, execute a model/benchmark, or
turn a reference/protocol analogue into a reproduction anchor.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
WORKBENCH = REPO / "wiki/survey/workbench/system-first-stage1b-targeted-anchor-scan"
RECORDS_PATH = WORKBENCH / "targeted-anchor-scan-records-v1.json"
REGISTRY_PATH = REPO / "wiki/survey/registry/stage1b-targeted-anchor-scan-2026-07-24-papers.jsonl"
FULLTEXT_LEDGER_PATH = REPO / "wiki/survey/2026-07-17-sf-fulltext-ledger.jsonl"
APPENDIX_PATH = REPO / "wiki/survey/current/stage1b-transition-reference-appendix.md"
PRIORITY_PATH = REPO / "wiki/survey/current/data/stage1c-common-rubric-comparison-v1.json"
CAPABILITY_RECORDS_PATH = (
    REPO
    / "wiki/survey/workbench/system-first-stage1b-capability-delta/data/capability-delta-records-v1.json"
)
CAPABILITY_MANIFEST_PATH = (
    REPO
    / "wiki/survey/workbench/system-first-stage1b-capability-delta/review-package-manifest.json"
)
DEFAULT_CHECK_DIR = REPO / "docs/checks/stage1b-targeted-anchor-scan/2026-07-24-rc1"
REVIEW_MANIFEST_PATH = WORKBENCH / "review-package-manifest.json"

FROZEN_RELEASE = "38fb9435d0c35e226ad62b16015a6dbee054e6c2"
REQUESTED_REVIEW_VERDICT = "SIGN_STAGE1B_TARGETED_ANCHOR_SCAN_RELEASE"
EXPECTED_SCAN_IDS = {
    "2505.00684", "2507.10859", "2508.10015", "2510.07838", "2510.11098",
    "2510.15421", "2510.20867", "2512.11109", "2512.14865", "2601.01885",
    "2601.03515", "2601.07470", "2601.09413", "2601.19935", "2602.03707",
    "2604.08064", "2604.15383", "2604.25122", "2605.13277", "2605.13716",
    "2605.15019", "2605.28020", "2606.01414", "2606.06915", "2606.18448",
    "2606.19341",
}
EXPECTED_NOT_PROMOTED = {"2601.07470", "2606.01414"}
EXPECTED_PROMOTED = EXPECTED_SCAN_IDS - EXPECTED_NOT_PROMOTED
PRIMARY_DIRECTIONS = {"SYSTEM", "KNOWLEDGE", "SKILL", "MEMORY", "CONTROL"}
PATH_IDS = {
    "D0_SYSTEM_HARNESS", "D1_MULTIMODAL_KNOWLEDGE", "D2_MULTIMODAL_SKILL",
    "D3_MULTIMODAL_MEMORY", "D4_TF_RL_ORCHESTRATION",
}
MM_LEVELS = {
    "MM0_TEXT_ONLY", "MM1_MULTIMODAL_TASK_ONLY", "MM2_MULTIMODAL_ASSET",
    "MM3_CAUSALLY_MULTIMODAL",
}
USE_RELATIONS = {"REFERENCE_CONTEXT", "BORROWED_PROTOCOL_ANALOGUE", "REPRODUCTION_ANCHOR"}


class ContractError(RuntimeError):
    """Raised when the scan overlay violates a frozen or evidence contract."""


def canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ContractError(f"expected JSON object: {path}")
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as error:
            # The old global fetch ledger contains one explicitly marked legacy NOTE row.
            if path == FULLTEXT_LEDGER_PATH and '"record_type": "NOTE"' in line:
                continue
            raise ContractError(f"invalid JSONL at {path}:{line_number}: {error}") from error
        if not isinstance(value, dict):
            raise ContractError(f"non-object JSONL row at {path}:{line_number}")
        rows.append(value)
    return rows


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def external_root() -> Path:
    configured = os.environ.get("SPEECHRL_DATA_DIR")
    if configured:
        wsl_match = re.fullmatch(r"/mnt/([a-zA-Z])/(.*)", configured.rstrip("/"))
        if os.name == "nt" and wsl_match:
            return Path(f"{wsl_match.group(1).upper()}:/{wsl_match.group(2)}")
        return Path(configured)
    return Path("E:/chao_workspace/exploring-l4-intelligence/speechrl-data")


def frozen_registry_paths() -> list[Path]:
    paths = sorted((REPO / "wiki/survey/registry").glob("stage1b-bounded-*-papers.jsonl"))
    direct = REPO / "wiki/survey/registry/stage1b-bounded-2026-07-22-papers.jsonl"
    if direct.exists():
        paths = sorted({*paths, direct})
    if len(paths) != 4:
        raise ContractError(f"expected four frozen Stage-1B v5 shards; found {len(paths)}")
    return paths


def validate_records() -> tuple[
    dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]
]:
    package = load_json(RECORDS_PATH)
    if package.get("frozen_stage1b_v5_release") != FROZEN_RELEASE:
        raise ContractError("frozen Stage-1B v5 release mismatch")
    for flag in ("frozen_stage1b_v5_mutated", "capability_delta_rc1_mutated", "stage1c_activated"):
        if package.get(flag) is not False:
            raise ContractError(f"{flag} must remain false")
    if package.get("literature_universe_closed") is not False:
        raise ContractError("targeted scan may not claim literature-universe closure")

    scan_contract = package.get("scan_contract", {})
    if (
        scan_contract.get("candidate_count") != 26
        or scan_contract.get("promotion_count") != 24
        or scan_contract.get("not_promoted_count") != 2
        or scan_contract.get("dedup_reference_surface") != 296
        or scan_contract.get("primary_sources_only") is not True
        or scan_contract.get("fulltext_required") is not True
    ):
        raise ContractError("scan contract counts, reference surface or evidence requirements changed")

    scan_items = package.get("scan_items")
    records = package.get("records")
    if not isinstance(scan_items, list) or not isinstance(records, list):
        raise ContractError("scan_items and records must be arrays")
    scan_ids = [row.get("arxiv_id") for row in scan_items]
    promoted_ids = {row.get("arxiv_id") for row in scan_items if row.get("disposition") == "PROMOTED"}
    not_promoted_ids = {
        row.get("arxiv_id") for row in scan_items if row.get("disposition") == "SCANNED_NOT_PROMOTED"
    }
    if len(scan_ids) != len(set(scan_ids)) or set(scan_ids) != EXPECTED_SCAN_IDS:
        raise ContractError("scan surface must be exactly 26 unique expected IDs")
    if {row.get("disposition") for row in scan_items} != {"PROMOTED", "SCANNED_NOT_PROMOTED"}:
        raise ContractError("scan dispositions must be promoted or explicitly scanned-not-promoted")
    if promoted_ids != EXPECTED_PROMOTED or not_promoted_ids != EXPECTED_NOT_PROMOTED:
        raise ContractError("promotion and scanned-not-promoted sets differ from the frozen scan decision")
    record_ids = [row.get("primary_identity") for row in records]
    if len(record_ids) != 24 or len(record_ids) != len(set(record_ids)) or set(record_ids) != EXPECTED_PROMOTED:
        raise ContractError("Stage-1B targeted records must be exactly the 24 promoted works")

    scan_by_id = {row["arxiv_id"]: row for row in scan_items}
    relations: Counter[str] = Counter()
    bindings: list[dict[str, Any]] = []
    for row in records:
        identity = row["primary_identity"]
        if row.get("canonical_work_id") != f"CW-ARXIV-{identity}":
            raise ContractError(f"canonical work ID mismatch for {identity}")
        mapping = row.get("capability_mapping", {})
        if mapping.get("primary_direction") not in PRIMARY_DIRECTIONS:
            raise ContractError(f"invalid primary capability direction for {identity}")
        path_ids = set(row.get("intervention_axis", []))
        if not path_ids or not path_ids <= PATH_IDS:
            raise ContractError(f"invalid D0-D4 intervention axis for {identity}")
        if mapping.get("multimodality_level") not in MM_LEVELS:
            raise ContractError(f"invalid MM0-MM3 level for {identity}")
        for field in (
            "asset_content_type", "persistence_scope", "system_carrier", "control_status",
            "causal_attribution",
        ):
            if not mapping.get(field):
                raise ContractError(f"missing capability contract field {field} for {identity}")
        use = row.get("project_use_contract", {})
        relation = use.get("primary_relation")
        if relation not in USE_RELATIONS:
            raise ContractError(f"invalid reference/borrow/reproduce relation for {identity}")
        relations[relation] += 1
        if not use.get("reproduction_candidate_status") or not use.get("reason"):
            raise ContractError(f"missing reproduction-candidate boundary for {identity}")
        if row.get("stage1c_eligible_before_signature") is not False:
            raise ContractError(f"unsigned scan record marked Stage-1C eligible: {identity}")
        experiment = row.get("paper_reported_experiment", {})
        if not experiment.get("setting") or not experiment.get("comparisons") or not experiment.get("source_locators"):
            raise ContractError(f"paper-reported experiment lacks setting/comparison/locator for {identity}")
        if not row.get("strongest_boundary_or_falsifier"):
            raise ContractError(f"missing strongest boundary/falsifier for {identity}")
        serialized = canonical_json(row).lower()
        if '"novelty_verdict"' in serialized or '"project_result"' in serialized:
            raise ContractError(f"unauthorized project conclusion field for {identity}")

    if relations["REPRODUCTION_ANCHOR"]:
        raise ContractError("the targeted scan closes no reproduction anchor")

    for identity, item in sorted(scan_by_id.items()):
        directory = external_root() / "survey-fulltext" / identity
        for kind, suffix, hash_field in (
            ("pdf", ".pdf", "pdf_sha256"),
            ("eprint", ".eprint", "eprint_sha256"),
            ("extracted_text", ".txt", "extracted_text_sha256"),
        ):
            path = directory / f"{identity}{suffix}"
            if not path.is_file():
                raise ContractError(f"missing {kind} for {identity}: {path}")
            actual = sha256_path(path)
            if actual != item.get(hash_field):
                raise ContractError(f"{kind} hash mismatch for {identity}")
            bindings.append({
                "primary_identity": identity,
                "disposition": item["disposition"],
                "kind": kind,
                "resolved_windows_path": path.as_posix(),
                "bytes": path.stat().st_size,
                "sha256": actual,
            })
    return package, sorted(scan_items, key=lambda row: row["arxiv_id"]), sorted(
        records, key=lambda row: row["primary_identity"]
    ), sorted(bindings, key=lambda row: (row["primary_identity"], row["kind"]))


def validate_fulltext_ledger(scan_items: list[dict[str, Any]]) -> dict[str, Any]:
    target_ids = {row["arxiv_id"] for row in scan_items}
    expected = {
        (row["arxiv_id"], kind): row[f"{kind}_sha256"]
        for row in scan_items
        for kind in ("pdf", "eprint")
    }
    observed: dict[tuple[str, str], set[str]] = defaultdict(set)
    event_counts: Counter[tuple[str, str]] = Counter()
    for row in load_jsonl(FULLTEXT_LEDGER_PATH):
        key = (row.get("arxiv_id"), row.get("kind"))
        if key[0] in target_ids and key[1] in {"pdf", "eprint"} and row.get("sha256"):
            observed[key].add(row["sha256"])
            event_counts[key] += 1
    for key, expected_hash in expected.items():
        if observed.get(key, set()) != {expected_hash}:
            raise ContractError(f"fulltext ledger mismatch/conflict for {key}: {sorted(observed.get(key, set()))}")
    return {
        "path": FULLTEXT_LEDGER_PATH.relative_to(REPO).as_posix(),
        "sha256": sha256_path(FULLTEXT_LEDGER_PATH),
        "target_renditions_verified": len(expected),
        "conflicting_hashes": 0,
        "identical_retry_counts": {
            f"{identity}:{kind}": count
            for (identity, kind), count in sorted(event_counts.items()) if count > 1
        },
    }


def validate_capability_delta_rc1() -> dict[str, Any]:
    """Verify every byte-bound artifact in the already reviewed RC1 manifest."""

    manifest = load_json(CAPABILITY_MANIFEST_PATH)
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or len(artifacts) != manifest.get("artifact_count"):
        raise ContractError("capability-delta RC1 manifest artifact count is invalid")
    for item in artifacts:
        path = REPO / item["path"]
        if not path.is_file():
            raise ContractError(f"capability-delta RC1 artifact is missing: {path}")
        if path.stat().st_size != item.get("bytes") or sha256_path(path) != item.get("sha256"):
            raise ContractError(f"capability-delta RC1 artifact bytes changed: {path}")
    return {
        "path": CAPABILITY_MANIFEST_PATH.relative_to(REPO).as_posix(),
        "sha256": sha256_path(CAPABILITY_MANIFEST_PATH),
        "artifact_count": len(artifacts),
        "all_manifest_artifacts_byte_verified": True,
    }


def canonical_from_work_id(work_id: str) -> str:
    if work_id.startswith("CW-ARXIV-"):
        return "arxiv:" + work_id.removeprefix("CW-ARXIV-")
    if work_id.startswith("CW-ACL-"):
        return "acl:" + work_id.removeprefix("CW-ACL-")
    raise ContractError(f"unsupported canonical work ID: {work_id}")


def build_census(records: list[dict[str, Any]]) -> dict[str, Any]:
    frozen_ids: list[str] = []
    frozen_shards: list[dict[str, Any]] = []
    for path in frozen_registry_paths():
        rows = load_jsonl(path)
        frozen_ids.extend(row["canonical_id"] for row in rows)
        frozen_shards.append({
            "path": path.relative_to(REPO).as_posix(), "rows": len(rows), "sha256": sha256_path(path)
        })
    if len(frozen_ids) != 226 or len(set(frozen_ids)) != 226:
        raise ContractError("frozen Stage-1B v5 registry is not exactly 226 unique works")

    appendix_matches = re.findall(
        r"<!-- work:(\d{4}\.\d{4,5}) -->", APPENDIX_PATH.read_text(encoding="utf-8")
    )
    appendix = {f"arxiv:{value}" for value in appendix_matches}
    priority_package = load_json(PRIORITY_PATH)
    priority = {
        canonical_from_work_id(row["canonical_work_id"])
        for row in priority_package.get("priority_intake", [])
    }
    capability_package = load_json(CAPABILITY_RECORDS_PATH)
    capability = {
        canonical_from_work_id(row["canonical_work_id"])
        for row in capability_package.get("records", [])
    }
    targeted = {canonical_from_work_id(row["canonical_work_id"]) for row in records}
    frozen = set(frozen_ids)
    inherited = frozen | appendix | priority
    checks = {
        "frozen_226": len(frozen) == 226,
        "appendix_59": len(appendix_matches) == 59 and len(appendix) == 59,
        "base_appendix_overlap_7": len(frozen & appendix) == 7,
        "priority_4": len(priority) == 4,
        "inherited_union_282": len(inherited) == 282,
        "capability_delta_14": len(capability) == 14,
        "targeted_overlay_24": len(targeted) == 24,
        "targeted_disjoint_from_inherited": not targeted & inherited,
        "targeted_disjoint_from_capability_delta": not targeted & capability,
        "independent_targeted_surface_306": len(inherited | targeted) == 306,
        "combined_unsigned_candidate_union_320": len(inherited | capability | targeted) == 320,
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise ContractError(f"canonical census checks failed: {failed}")
    return {
        "schema": "sf-stage1b-targeted-anchor-scan-canonical-census-v1",
        "artifact_id": "SF-STAGE1B-TARGETED-ANCHOR-SCAN-CANONICAL-CENSUS-RC1",
        "as_of": "2026-07-24",
        "frozen_stage1b_v5_release": FROZEN_RELEASE,
        "frozen_base": {"count": 226, "shards": frozen_shards},
        "inherited_current_union": 282,
        "capability_delta_rc1": {"count": 14, "mutated": False, "signed": False},
        "input_bindings": {
            "current_reference_appendix": {
                "path": APPENDIX_PATH.relative_to(REPO).as_posix(),
                "sha256": sha256_path(APPENDIX_PATH),
            },
            "current_priority_intake": {
                "path": PRIORITY_PATH.relative_to(REPO).as_posix(),
                "sha256": sha256_path(PRIORITY_PATH),
            },
            "capability_delta_records": {
                "path": CAPABILITY_RECORDS_PATH.relative_to(REPO).as_posix(),
                "sha256": sha256_path(CAPABILITY_RECORDS_PATH),
            },
        },
        "targeted_anchor_scan": {
            "fulltext_scanned": 26,
            "promoted": 24,
            "scanned_not_promoted": 2,
            "overlap_with_inherited": 0,
            "overlap_with_capability_delta": 0,
        },
        "independent_targeted_overlay_surface": 306,
        "combined_unsigned_candidate_union": 320,
        "checks": checks,
        "signed_release": False,
        "stage1c_input": False,
    }


def registry_rows(records: list[dict[str, Any]], scan_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    scans = {row["arxiv_id"]: row for row in scan_items}
    rows: list[dict[str, Any]] = []
    for record in records:
        identity = record["primary_identity"]
        scan = scans[identity]
        rows.append({
            "schema": "sf-paper-registry-record-v1",
            "canonical_id": f"arxiv:{identity}",
            "arxiv_id": identity,
            "title": record["title"],
            "role": record["stage1b_role"],
            "conclusion": "TARGETED_STAGE1B_OVERLAY_RETAINED_UNSIGNED",
            "links": {
                "abstract": f"https://arxiv.org/abs/{identity}",
                "pdf": f"https://arxiv.org/pdf/{identity}",
                "eprint": f"https://arxiv.org/e-print/{identity}",
            },
            "method_path": {
                "intervention_axes": record["intervention_axis"],
                "primary_direction": record["capability_mapping"]["primary_direction"],
                "multimodality_level": record["capability_mapping"]["multimodality_level"],
            },
            "project_use_contract": record["project_use_contract"],
            "evidence_locators": record["paper_reported_experiment"]["source_locators"],
            "strongest_boundary_or_falsifier": record["strongest_boundary_or_falsifier"],
            "provenance": {
                "decision_origin": "OWNER_AUTHORIZED_TARGETED_FULLTEXT_SCAN",
                "scan_record": RECORDS_PATH.relative_to(REPO).as_posix(),
                "pdf_sha256": scan["pdf_sha256"],
                "eprint_sha256": scan["eprint_sha256"],
                "extracted_text_sha256": scan["extracted_text_sha256"],
            },
            "purpose_chain": "Stage-1B evidence overlay -> independent review -> possible later Stage-1C evidence mapping",
            "stage1c_eligible_before_signature": False,
        })
    return sorted(rows, key=lambda row: row["arxiv_id"])


def render_jsonl(rows: list[dict[str, Any]]) -> str:
    return "".join(canonical_json(row) + "\n" for row in rows)


def validate_registry(expected_rows: list[dict[str, Any]], *, allow_missing: bool) -> None:
    if not REGISTRY_PATH.exists():
        if allow_missing:
            return
        raise ContractError(f"missing targeted registry shard: {REGISTRY_PATH}")
    actual = REGISTRY_PATH.read_text(encoding="utf-8")
    expected = render_jsonl(expected_rows)
    if actual != expected:
        raise ContractError("targeted registry shard differs from deterministic 24-record projection")


def build_report(
    records: list[dict[str, Any]], bindings: list[dict[str, Any]], ledger: dict[str, Any],
    census: dict[str, Any], capability_rc1: dict[str, Any],
) -> dict[str, Any]:
    role_counts = Counter(row["stage1b_role"] for row in records)
    direction_counts = Counter(row["capability_mapping"]["primary_direction"] for row in records)
    relation_counts = Counter(row["project_use_contract"]["primary_relation"] for row in records)
    return {
        "schema": "sf-stage1b-targeted-anchor-scan-contract-report-v1",
        "artifact_id": "SF-STAGE1B-TARGETED-ANCHOR-SCAN-CONTRACT-REPORT-RC1",
        "as_of": "2026-07-24",
        "status": "UNSIGNED_STAGE1B_OVERLAY_AWAITING_INDEPENDENT_REVIEW",
        "requested_review_verdict": REQUESTED_REVIEW_VERDICT,
        "self_signed": False,
        "surface": {
            "fulltext_scanned": 26,
            "promoted_records": 24,
            "scanned_not_promoted": 2,
            "role_counts": dict(sorted(role_counts.items())),
            "primary_direction_counts": dict(sorted(direction_counts.items())),
            "use_relation_counts": dict(sorted(relation_counts.items())),
            "reproduction_anchors": relation_counts["REPRODUCTION_ANCHOR"],
            "independent_targeted_overlay_surface": census["independent_targeted_overlay_surface"],
            "combined_unsigned_candidate_union": census["combined_unsigned_candidate_union"],
        },
        "external_bindings": {
            "verified": len(bindings), "expected": 78, "ledger": ledger,
        },
        "preserved_capability_delta_rc1": capability_rc1,
        "acceptance_checks": {
            "exact_26_scan_surface": True,
            "exact_24_promoted_and_2_not_promoted": True,
            "all_pdf_eprint_and_text_hashes_verified": len(bindings) == 78,
            "all_pdf_eprint_ledger_bindings_verified": ledger["target_renditions_verified"] == 52,
            "targeted_overlay_disjoint_from_inherited_and_capability_delta": True,
            "reference_borrow_reproduce_contract_complete": sum(relation_counts.values()) == 24,
            "no_false_reproduction_anchor": relation_counts["REPRODUCTION_ANCHOR"] == 0,
            "frozen_stage1b_v5_preserved": True,
            "capability_delta_rc1_preserved": capability_rc1["all_manifest_artifacts_byte_verified"],
            "no_stage1c_activation": True,
            "no_model_benchmark_reproduction_or_prototype_run": True,
            "no_project_novelty_or_direction_selection": True,
            "independent_signature_pending": True,
        },
        "limitations": [
            "This is a targeted primary-source scan, not closure of the literature universe.",
            "Paper-reported results are retained within their original experiment strata and are not cross-paper aggregates.",
            "REFERENCE_CONTEXT and BORROWED_PROTOCOL_ANALOGUE do not imply reproducibility, local readiness, or a reproduction anchor.",
            "The 320-work number is a combined unsigned candidate union, not a signed Stage-1C denominator.",
        ],
    }


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def build_manifest(check_dir: Path) -> dict[str, Any]:
    paths = [
        WORKBENCH / "README.md",
        WORKBENCH / "targeted-anchor-scan-contract.md",
        WORKBENCH / "targeted-anchor-map.md",
        RECORDS_PATH,
        REGISTRY_PATH,
        REPO / "scripts/survey/sf_stage1b_targeted_anchor_scan.py",
        REPO / "scripts/survey/test_sf_stage1b_targeted_anchor_scan.py",
        check_dir / "canonical-census.json",
        check_dir / "external-fulltext-bindings.json",
        check_dir / "contract-report.json",
    ]
    missing = [path for path in paths if not path.is_file()]
    if missing:
        raise ContractError(f"review-package artifacts are missing: {missing}")
    return {
        "schema": "sf-stage1b-targeted-anchor-scan-review-manifest-v1",
        "artifact_id": "SF-STAGE1B-TARGETED-ANCHOR-SCAN-REVIEW-PACKAGE-RC1",
        "as_of": "2026-07-24",
        "status": "UNSIGNED_STAGE1B_OVERLAY_AWAITING_INDEPENDENT_REVIEW",
        "requested_review_verdict": REQUESTED_REVIEW_VERDICT,
        "self_signed": False,
        "frozen_stage1b_v5_release": FROZEN_RELEASE,
        "artifact_count": len(paths),
        "artifacts": [
            {
                "path": path.relative_to(REPO).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256_path(path),
            }
            for path in paths
        ],
        "authority_withheld": [
            "stage1c_activation_or_scaleout", "research_model_or_api_execution",
            "benchmark_metric_run", "paper_reproduction", "prototype",
            "direction_ranking_or_selection", "project_novelty_verdict", "stage2a",
        ],
    }


def run(*, write: bool, check_dir: Path = DEFAULT_CHECK_DIR) -> dict[str, Any]:
    _package, scan_items, records, bindings = validate_records()
    ledger = validate_fulltext_ledger(scan_items)
    capability_rc1 = validate_capability_delta_rc1()
    census = build_census(records)
    rows = registry_rows(records, scan_items)
    validate_registry(rows, allow_missing=write)
    report = build_report(records, bindings, ledger, census, capability_rc1)
    failed = [name for name, passed in report["acceptance_checks"].items() if not passed]
    if failed:
        raise ContractError(f"acceptance checks failed: {failed}")
    if write:
        if REGISTRY_PATH.exists():
            validate_registry(rows, allow_missing=False)
        else:
            REGISTRY_PATH.write_text(render_jsonl(rows), encoding="utf-8", newline="\n")
        write_json(check_dir / "canonical-census.json", census)
        write_json(check_dir / "external-fulltext-bindings.json", {
            "schema": "sf-stage1b-targeted-anchor-scan-external-bindings-v1",
            "artifact_id": "SF-STAGE1B-TARGETED-ANCHOR-SCAN-EXTERNAL-BINDINGS-RC1",
            "as_of": "2026-07-24",
            "binding_count": len(bindings),
            "bindings": bindings,
        })
        write_json(check_dir / "contract-report.json", report)
        write_json(REVIEW_MANIFEST_PATH, build_manifest(check_dir))
    else:
        validate_registry(rows, allow_missing=False)
        expected_manifest = build_manifest(check_dir)
        if load_json(REVIEW_MANIFEST_PATH) != expected_manifest:
            raise ContractError("review-package manifest is stale or not reproducible")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="materialize deterministic registry/check artifacts")
    parser.add_argument("--check-dir", type=Path, default=DEFAULT_CHECK_DIR)
    arguments = parser.parse_args()
    try:
        report = run(write=arguments.write, check_dir=arguments.check_dir)
    except ContractError as error:
        print(f"FAIL: {error}")
        return 1
    print(canonical_json({
        "status": report["status"],
        "fulltext_scanned": report["surface"]["fulltext_scanned"],
        "promoted_records": report["surface"]["promoted_records"],
        "combined_unsigned_candidate_union": report["surface"]["combined_unsigned_candidate_union"],
        "requested_review_verdict": report["requested_review_verdict"],
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
