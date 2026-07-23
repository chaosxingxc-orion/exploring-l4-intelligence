#!/usr/bin/env python3
"""Verify and materialize the authorized Stage-1B capability-delta release candidate.

The checker is intentionally incapable of signing the release, activating Stage-1C,
running a research model, or reporting project novelty.  It verifies exact identities,
external full-text bindings, bounded citation promotions, capability contracts, and the
canonical census while preserving the frozen Stage-1B v5 release.
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
WORKBENCH = REPO / "wiki/survey/workbench/system-first-stage1b-capability-delta"
DATA = WORKBENCH / "data"
RECORDS_PATH = DATA / "capability-delta-records-v1.json"
PROMOTIONS_PATH = DATA / "one-hop-promotions-v1.json"
CITATION_LEDGER_PATH = DATA / "backward-citation-ledger-v1.jsonl"
CITATION_SUMMARY_PATH = DATA / "backward-citation-summary-v1.json"
FULLTEXT_LEDGER_PATH = REPO / "wiki/survey/2026-07-17-sf-fulltext-ledger.jsonl"
APPENDIX_PATH = REPO / "wiki/survey/current/stage1b-transition-reference-appendix.md"
PRIORITY_PATH = REPO / "wiki/survey/current/data/stage1c-common-rubric-comparison-v1.json"
REGISTRY_DIR = REPO / "wiki/survey/registry"
DEFAULT_CHECK_DIR = REPO / "docs/checks/stage1b-capability-delta/2026-07-23-rc1"
DEFAULT_CENSUS_PATH = DATA / "canonical-census-v1.json"
REVIEW_MANIFEST_PATH = WORKBENCH / "review-package-manifest.json"

AUTHORIZATION = "AUTHORIZE_STAGE1B_CAPABILITY_DELTA_MAPPING"
FROZEN_RELEASE = "38fb9435d0c35e226ad62b16015a6dbee054e6c2"
REQUESTED_REVIEW_VERDICT = "SIGN_STAGE1B_CAPABILITY_DELTA_RELEASE"
EXPECTED_SEEDS = {
    "2405.20834",
    "2602.07624",
    "2603.12056",
    "2603.28088",
    "2604.24594",
    "2605.13527",
    "2606.09316",
    "2606.29538",
}
EXPECTED_PROMOTIONS = {
    "2402.17753",
    "2508.19828",
    "2602.12670",
    "2603.01145",
    "2604.03964",
    "2604.17308",
}
PATH_IDS = {
    "D0_SYSTEM_HARNESS",
    "D1_MULTIMODAL_KNOWLEDGE",
    "D2_MULTIMODAL_SKILL",
    "D3_MULTIMODAL_MEMORY",
    "D4_TF_RL_ORCHESTRATION",
}
PRIMARY_DIRECTIONS = {"SYSTEM", "KNOWLEDGE", "SKILL", "MEMORY", "CONTROL"}
ROLES = {
    "DIRECT_PATH",
    "COMPONENT_PATH",
    "INSTRUMENT",
    "NEGATIVE_OR_FALSIFIER",
    "BOUNDARY",
    "REFERENCE_ONLY",
}
DISPOSITIONS = {
    "EMPIRICAL_LOAD_BEARING",
    "EMPIRICAL_RELATION_ONLY",
    "NON_EMPIRICAL_EVIDENCE_NODE",
    "BOUNDARY_OR_FALSIFIER",
    "EXCLUDE_WITH_REASON",
}
USE_RELATIONS = {
    "REFERENCE_CONTEXT",
    "BORROWED_PROTOCOL_ANALOGUE",
    "REPRODUCTION_ANCHOR",
}
REPRODUCTION_SUBTYPES = {
    "EXACT_REPRODUCTION",
    "CLOSE_REPRODUCTION_WITH_DECLARED_DEVIATIONS",
    "TASK_MATCHED_METHOD_TRANSFER",
}
MM_LEVELS = {
    "MM0_TEXT_ONLY",
    "MM1_MULTIMODAL_TASK_ONLY",
    "MM2_MULTIMODAL_ASSET",
    "MM3_CAUSALLY_MULTIMODAL",
}


class ContractError(RuntimeError):
    """Raised when the candidate would overclaim or break a frozen contract."""


def canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ContractError(f"expected JSON object: {path}")
    return value


def load_jsonl(path: Path, *, tolerate_legacy_notes: bool = False) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as error:
            if tolerate_legacy_notes and '"record_type": "NOTE"' in line:
                continue
            raise ContractError(f"invalid JSONL at {path}:{line_number}: {error}") from error
        if not isinstance(value, dict):
            raise ContractError(f"non-object JSONL row at {path}:{line_number}")
        rows.append(value)
    return rows


def registry_shards() -> list[Path]:
    paths = sorted(REGISTRY_DIR.glob("stage1b-bounded-*-papers.jsonl"))
    direct = REGISTRY_DIR / "stage1b-bounded-2026-07-22-papers.jsonl"
    paths = sorted({*paths, direct}) if direct.exists() else paths
    if len(paths) != 4:
        raise ContractError(f"expected four frozen registry shards; found {len(paths)}")
    return paths


def canonical_from_work_id(work_id: str) -> str:
    if work_id.startswith("CW-ARXIV-"):
        return "arxiv:" + work_id.removeprefix("CW-ARXIV-")
    if work_id.startswith("CW-ACL-"):
        return "acl:" + work_id.removeprefix("CW-ACL-")
    raise ContractError(f"unsupported canonical work ID: {work_id}")


def external_root() -> Path:
    configured = os.environ.get("SPEECHRL_DATA_DIR")
    if configured:
        wsl_match = re.fullmatch(r"/mnt/([a-zA-Z])/(.*)", configured.rstrip("/"))
        if os.name == "nt" and wsl_match:
            return Path(f"{wsl_match.group(1).upper()}:/{wsl_match.group(2)}")
        return Path(configured)
    return Path("E:/chao_workspace/exploring-l4-intelligence/speechrl-data")


def resolve_external_path(template: str) -> Path:
    prefix = "${SPEECHRL_DATA_DIR}/"
    if not template.startswith(prefix):
        raise ContractError(f"external path must use {prefix}: {template}")
    relative = template.removeprefix(prefix)
    if ".." in Path(relative).parts:
        raise ContractError(f"external path escapes data root: {template}")
    return external_root() / Path(relative)


def validate_records() -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    package = load_json(RECORDS_PATH)
    if package.get("authorization") != AUTHORIZATION:
        raise ContractError("authorization token mismatch")
    if package.get("frozen_stage1b_v5_release") != FROZEN_RELEASE:
        raise ContractError("frozen Stage-1B v5 release mismatch")
    if package.get("frozen_stage1b_v5_mutated") is not False:
        raise ContractError("candidate must state that Stage-1B v5 was not mutated")
    if package.get("literature_universe_closed") is not False:
        raise ContractError("capability delta may not claim literature closure")

    records = package.get("records")
    if not isinstance(records, list) or len(records) != 14:
        raise ContractError(f"expected 14 delta records; found {len(records or [])}")
    identities = [row.get("primary_identity") for row in records]
    duplicates = sorted(k for k, n in Counter(identities).items() if n > 1)
    if duplicates:
        raise ContractError(f"duplicate delta identities: {duplicates}")
    if set(identities) != EXPECTED_SEEDS | EXPECTED_PROMOTIONS:
        raise ContractError("delta record identity set differs from the authorized 8+6 surface")

    bindings: list[dict[str, Any]] = []
    relation_counts: Counter[str] = Counter()
    for row in records:
        identity = row["primary_identity"]
        expected_work_id = f"CW-ARXIV-{identity}"
        if row.get("canonical_work_id") != expected_work_id:
            raise ContractError(f"canonical ID mismatch for {identity}")
        discovery = row.get("discovery", {})
        expected_mode = "OWNER_APPROVED_SEED" if identity in EXPECTED_SEEDS else "CITATION_EXPANSION"
        if discovery.get("mode") != expected_mode:
            raise ContractError(f"discovery mode mismatch for {identity}")
        if expected_mode == "CITATION_EXPANSION" and not discovery.get("parent_work_ids"):
            raise ContractError(f"citation promotion lacks parent for {identity}")

        if row.get("stage1b_role") not in ROLES:
            raise ContractError(f"invalid Stage-1B role for {identity}")
        if row.get("paper_disposition") not in DISPOSITIONS:
            raise ContractError(f"invalid paper disposition for {identity}")
        mapping = row.get("capability_mapping", {})
        paths = mapping.get("path_ids")
        if not isinstance(paths, list) or not paths or not set(paths) <= PATH_IDS:
            raise ContractError(f"invalid D0-D4 path mapping for {identity}")
        if mapping.get("primary_direction") not in PRIMARY_DIRECTIONS:
            raise ContractError(f"invalid primary direction for {identity}")
        if mapping.get("multimodality_level") not in MM_LEVELS:
            raise ContractError(f"invalid multimodality level for {identity}")
        for field in ("asset_content_type", "persistence_scope", "system_carrier", "control_status", "causal_attribution"):
            if not mapping.get(field):
                raise ContractError(f"missing capability field {field} for {identity}")

        use = row.get("project_use_contract", {})
        relation = use.get("primary_relation")
        if relation not in USE_RELATIONS:
            raise ContractError(f"invalid reference/borrow/reproduce relation for {identity}")
        relation_counts[relation] += 1
        subtype = use.get("reproduction_subtype")
        if relation == "REPRODUCTION_ANCHOR":
            if subtype not in REPRODUCTION_SUBTYPES:
                raise ContractError(f"reproduction anchor lacks subtype for {identity}")
        elif subtype is not None:
            raise ContractError(f"non-reproduction record has reproduction subtype for {identity}")
        if use.get("stage1c_eligible_before_delta_signature") is not False:
            raise ContractError(f"unsigned delta record marked Stage-1C eligible: {identity}")

        experiment = row.get("paper_reported_experiment", {})
        if not experiment.get("status") or not experiment.get("source_locators"):
            raise ContractError(f"paper-reported experiment lacks status/locators for {identity}")
        if not row.get("strongest_boundary_or_falsifier"):
            raise ContractError(f"record lacks strongest boundary/falsifier for {identity}")
        serialized = canonical_json(row).lower()
        if '"novelty_verdict"' in serialized or '"project_result"' in serialized:
            raise ContractError(f"unauthorized project verdict/result field for {identity}")

        fulltext = row.get("fulltext", {})
        for kind in ("pdf", "eprint"):
            item = fulltext.get(kind, {})
            path = resolve_external_path(item.get("path", ""))
            if not path.is_file():
                raise ContractError(f"missing external {kind} for {identity}: {path}")
            actual = sha256_path(path)
            if actual != item.get("sha256"):
                raise ContractError(f"external {kind} hash mismatch for {identity}")
            bindings.append({
                "primary_identity": identity,
                "kind": kind,
                "path_template": item["path"],
                "resolved_windows_path": path.as_posix(),
                "bytes": path.stat().st_size,
                "sha256": actual,
            })
        bucket = "seeds" if identity in EXPECTED_SEEDS else "one-hop"
        text_path = external_root() / f"survey-capability-delta/stage1b-2026-07-23/{bucket}/{identity}/paper.txt"
        if not text_path.is_file():
            raise ContractError(f"missing extracted text for {identity}: {text_path}")
        actual_text_hash = sha256_path(text_path)
        if actual_text_hash != fulltext.get("extracted_text_sha256"):
            raise ContractError(f"extracted text hash mismatch for {identity}")
        bindings.append({
            "primary_identity": identity,
            "kind": "extracted_text",
            "resolved_windows_path": text_path.as_posix(),
            "bytes": text_path.stat().st_size,
            "sha256": actual_text_hash,
        })

    if relation_counts["REPRODUCTION_ANCHOR"] != 0:
        raise ContractError("no delta work is task-matched enough to be a target reproduction anchor")
    return package, sorted(records, key=lambda row: row["primary_identity"]), sorted(
        bindings, key=lambda row: (row["primary_identity"], row["kind"])
    )


def validate_fulltext_ledger(records: list[dict[str, Any]]) -> dict[str, Any]:
    target_ids = {row["primary_identity"] for row in records}
    rows = load_jsonl(FULLTEXT_LEDGER_PATH, tolerate_legacy_notes=True)
    observed: dict[tuple[str, str], set[str]] = defaultdict(set)
    event_counts: Counter[tuple[str, str]] = Counter()
    for row in rows:
        identity = row.get("arxiv_id")
        kind = row.get("kind")
        digest = row.get("sha256")
        if identity in target_ids and kind in {"pdf", "eprint"} and digest:
            observed[(identity, kind)].add(digest)
            event_counts[(identity, kind)] += 1
    expected = {
        (row["primary_identity"], kind): row["fulltext"][kind]["sha256"]
        for row in records
        for kind in ("pdf", "eprint")
    }
    for key, expected_hash in expected.items():
        hashes = observed.get(key, set())
        if hashes != {expected_hash}:
            raise ContractError(f"fulltext ledger mismatch/conflict for {key}: {sorted(hashes)}")
    identical_duplicate_events = {
        f"{identity}:{kind}": count
        for (identity, kind), count in sorted(event_counts.items())
        if count > 1
    }
    return {
        "ledger": FULLTEXT_LEDGER_PATH.relative_to(REPO).as_posix(),
        "ledger_sha256": sha256_path(FULLTEXT_LEDGER_PATH),
        "target_renditions_verified": len(expected),
        "conflicting_hashes": 0,
        "identical_duplicate_events_retained": identical_duplicate_events,
        "append_only_rows_mutated_or_removed": false_value(),
    }


def false_value() -> bool:
    """Make negative state explicit without truthy string serialization."""

    return False


def validate_promotions(records: list[dict[str, Any]]) -> dict[str, Any]:
    package = load_json(PROMOTIONS_PATH)
    summary = load_json(CITATION_SUMMARY_PATH)
    if sha256_path(CITATION_LEDGER_PATH) != package.get("source_ledger_sha256"):
        raise ContractError("citation ledger hash differs from the promotion package")
    if package.get("promoted_count") != 6 or package.get("not_promoted_count") != 297:
        raise ContractError("promotion/seen-not-promoted counts are not 6/297")
    if package.get("seen_unique_arxiv_ids") != 303:
        raise ContractError("one-hop unique arXiv-ID subset is not 303")
    if summary.get("unique_backward_arxiv_ids") != 303:
        raise ContractError("citation summary unique count differs from promotion package")
    if summary.get("forward_waived") != 8 or summary.get("backward_executed") != 8:
        raise ContractError("citation execution/waiver counts differ from the bounded protocol")

    source_rows = {row["arxiv_id"]: row for row in load_jsonl(CITATION_LEDGER_PATH)}
    record_by_id = {row["primary_identity"]: row for row in records}
    promotion_ids: set[str] = set()
    for promotion in package.get("promotions", []):
        identity = promotion["canonical_work_id"].removeprefix("CW-ARXIV-")
        promotion_ids.add(identity)
        if identity not in EXPECTED_PROMOTIONS or identity not in record_by_id:
            raise ContractError(f"unrecognized promotion: {identity}")
        parents = [value.removeprefix("CW-ARXIV-") for value in promotion["parent_work_ids"]]
        record_parents = [value.removeprefix("CW-ARXIV-") for value in record_by_id[identity]["discovery"]["parent_work_ids"]]
        if sorted(parents) != sorted(record_parents):
            raise ContractError(f"promotion/record parent mismatch for {identity}")
        for parent in parents:
            if parent not in source_rows or identity not in source_rows[parent]["backward_arxiv_ids"]:
                raise ContractError(f"citation edge absent for {parent} -> {identity}")
    if promotion_ids != EXPECTED_PROMOTIONS:
        raise ContractError("promotion identity set differs from expected six")
    return {
        "backward_targets": summary["targets"],
        "backward_executed": summary["backward_executed"],
        "forward_waived": summary["forward_waived"],
        "seen_unique_arxiv_ids": package["seen_unique_arxiv_ids"],
        "promoted": package["promoted_count"],
        "seen_not_promoted": package["not_promoted_count"],
        "citation_ledger_sha256": package["source_ledger_sha256"],
        "scope_limitation": summary["limitation"],
    }


def build_census(records: list[dict[str, Any]]) -> dict[str, Any]:
    registry_ids: list[str] = []
    shard_bindings: list[dict[str, Any]] = []
    for path in registry_shards():
        rows = load_jsonl(path)
        ids = [row.get("canonical_id") for row in rows]
        if any(not value for value in ids):
            raise ContractError(f"registry row lacks canonical ID: {path}")
        registry_ids.extend(ids)
        shard_bindings.append({
            "path": path.relative_to(REPO).as_posix(),
            "rows": len(rows),
            "sha256": sha256_path(path),
        })
    if len(registry_ids) != 226 or len(set(registry_ids)) != 226:
        raise ContractError("frozen registry is not exactly 226 unique records")

    appendix_text = APPENDIX_PATH.read_text(encoding="utf-8")
    appendix_arxiv = re.findall(r"<!-- work:(\d{4}\.\d{4,5}) -->", appendix_text)
    appendix_ids = {f"arxiv:{value}" for value in appendix_arxiv}
    if len(appendix_arxiv) != 59 or len(appendix_ids) != 59:
        raise ContractError("CURRENT reference appendix is not exactly 59 unique routes")

    priority_package = load_json(PRIORITY_PATH)
    priority_ids = {canonical_from_work_id(row["canonical_work_id"]) for row in priority_package.get("priority_intake", [])}
    if len(priority_ids) != 4:
        raise ContractError("CURRENT priority intake is not exactly four unique works")

    base = set(registry_ids)
    inherited = base | appendix_ids | priority_ids
    delta = {canonical_from_work_id(row["canonical_work_id"]) for row in records}
    checks = {
        "base_unique": len(base) == 226,
        "appendix_unique": len(appendix_ids) == 59,
        "base_appendix_overlap": len(base & appendix_ids) == 7,
        "priority_unique": len(priority_ids) == 4,
        "priority_disjoint_from_base_appendix": not (priority_ids & (base | appendix_ids)),
        "inherited_union": len(inherited) == 282,
        "delta_unique": len(delta) == 14,
        "delta_disjoint_from_inherited": not (delta & inherited),
        "release_candidate_surface": len(inherited | delta) == 296,
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise ContractError(f"canonical census checks failed: {failed}")
    return {
        "schema": "sf-stage1b-capability-delta-canonical-census-v1",
        "artifact_id": "SF-STAGE1B-CAPABILITY-DELTA-CANONICAL-CENSUS-V1",
        "as_of": "2026-07-23",
        "frozen_stage1b_v5_release": FROZEN_RELEASE,
        "frozen_base": {"count": 226, "shards": shard_bindings},
        "current_reference_appendix": {
            "count": 59,
            "overlap_with_frozen_base": len(base & appendix_ids),
            "outside_frozen_base": len(appendix_ids - base),
            "path": APPENDIX_PATH.relative_to(REPO).as_posix(),
            "sha256": sha256_path(APPENDIX_PATH),
        },
        "current_priority_intake": {
            "count": 4,
            "overlap_with_base_or_appendix": len(priority_ids & (base | appendix_ids)),
            "path": PRIORITY_PATH.relative_to(REPO).as_posix(),
            "sha256": sha256_path(PRIORITY_PATH),
        },
        "inherited_canonical_union": 282,
        "capability_delta": {
            "count": 14,
            "overlap_with_inherited_union": len(delta & inherited),
            "seed_count": len(EXPECTED_SEEDS),
            "citation_promotion_count": len(EXPECTED_PROMOTIONS),
        },
        "release_candidate_surface": 296,
        "counting_exclusions": {
            "seen_not_promoted_citation_ids": 297,
            "reason": "Seen-not-promoted identities were not paper-audited and do not enter the canonical delta denominator."
        },
        "checks": checks,
        "stage1b_v5_mutated": False,
        "signed_release": False,
    }


def build_report(
    records: list[dict[str, Any]],
    bindings: list[dict[str, Any]],
    ledger_report: dict[str, Any],
    citation_report: dict[str, Any],
    census: dict[str, Any],
) -> dict[str, Any]:
    role_counts = Counter(row["stage1b_role"] for row in records)
    direction_counts = Counter(row["capability_mapping"]["primary_direction"] for row in records)
    relation_counts = Counter(row["project_use_contract"]["primary_relation"] for row in records)
    return {
        "schema": "sf-stage1b-capability-delta-contract-report-v1",
        "artifact_id": "SF-STAGE1B-CAPABILITY-DELTA-CONTRACT-REPORT-RC1",
        "as_of": "2026-07-23",
        "authorization": AUTHORIZATION,
        "status": "RELEASE_CANDIDATE_AWAITING_INDEPENDENT_REVIEW",
        "requested_review_verdict": REQUESTED_REVIEW_VERDICT,
        "self_signed": False,
        "stage1b_v5": {"release": FROZEN_RELEASE, "mutated": False},
        "surface": {
            "delta_records": len(records),
            "role_counts": dict(sorted(role_counts.items())),
            "primary_direction_counts": dict(sorted(direction_counts.items())),
            "project_use_relation_counts": dict(sorted(relation_counts.items())),
            "reproduction_anchors_in_delta": relation_counts["REPRODUCTION_ANCHOR"],
            "release_candidate_canonical_surface": census["release_candidate_surface"],
        },
        "external_bindings": {
            "verified": len(bindings),
            "expected": 42,
            "ledger": ledger_report,
        },
        "citation_expansion": citation_report,
        "acceptance_checks": {
            "exact_8_seed_plus_6_promotion_surface": len(records) == 14,
            "all_pdf_eprint_and_extracted_text_hashes_verified": len(bindings) == 42,
            "citation_promotions_have_parent_edges": citation_report["promoted"] == 6,
            "seen_not_promoted_does_not_inflate_denominator": citation_report["seen_not_promoted"] == 297,
            "reference_borrow_reproduce_contract_complete": sum(relation_counts.values()) == 14,
            "no_false_reproduction_anchor": relation_counts["REPRODUCTION_ANCHOR"] == 0,
            "canonical_surface_296": census["release_candidate_surface"] == 296,
            "frozen_stage1b_v5_preserved": True,
            "no_stage1c_activation": True,
            "no_model_benchmark_reproduction_or_prototype_run": True,
            "no_project_novelty_verdict": True,
            "independent_signature_pending": True,
        },
        "limitations": [
            "Backward citation expansion covers only regex-resolvable arXiv IDs in the eight local eprints.",
            "Forward citation checks were waived after public unauthenticated index requests were rate-limited.",
            "No promoted delta work is sufficiently task-matched to be a speech/omni reproduction anchor.",
            "Paper-reported numbers remain within-paper evidence and are not cross-paper aggregates or project results."
        ],
    }


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def build_review_manifest(check_dir: Path = DEFAULT_CHECK_DIR) -> dict[str, Any]:
    artifact_paths = [
        WORKBENCH / "README.md",
        WORKBENCH / "capability-delta-contract.md",
        WORKBENCH / "capability-path-map.md",
        WORKBENCH / "stage1c-v2-capability-research-program-zh.md",
        DATA / "seed-targets-v1.json",
        RECORDS_PATH,
        PROMOTIONS_PATH,
        CITATION_LEDGER_PATH,
        CITATION_SUMMARY_PATH,
        DEFAULT_CENSUS_PATH,
        REPO / "scripts/survey/sf_stage1b_capability_delta.py",
        REPO / "scripts/survey/test_sf_stage1b_capability_delta.py",
        check_dir / "canonical-census.json",
        check_dir / "external-fulltext-bindings.json",
        check_dir / "contract-report.json",
    ]
    missing = [path for path in artifact_paths if not path.is_file()]
    if missing:
        raise ContractError(f"review manifest inputs are missing: {missing}")
    return {
        "schema": "sf-stage1b-capability-delta-review-package-manifest-v1",
        "artifact_id": "SF-STAGE1B-CAPABILITY-DELTA-REVIEW-PACKAGE-RC1",
        "as_of": "2026-07-23",
        "status": "RELEASE_CANDIDATE_AWAITING_INDEPENDENT_REVIEW",
        "authorization": AUTHORIZATION,
        "requested_review_verdict": REQUESTED_REVIEW_VERDICT,
        "self_signed": False,
        "frozen_stage1b_v5_release": FROZEN_RELEASE,
        "frozen_stage1b_v5_mutated": False,
        "artifact_count": len(artifact_paths),
        "artifacts": [
            {
                "path": path.relative_to(REPO).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256_path(path),
            }
            for path in artifact_paths
        ],
        "external_binding_report": (check_dir / "external-fulltext-bindings.json").relative_to(REPO).as_posix(),
        "authority_withheld": [
            "stage1c_activation_or_scaleout",
            "research_model_or_api_execution",
            "benchmark_metric_run",
            "paper_reproduction",
            "prototype",
            "ranking_or_selection",
            "project_novelty_verdict",
            "stage2a",
        ],
    }


def run(*, write: bool, check_dir: Path = DEFAULT_CHECK_DIR) -> dict[str, Any]:
    _package, records, bindings = validate_records()
    ledger_report = validate_fulltext_ledger(records)
    citation_report = validate_promotions(records)
    census = build_census(records)
    report = build_report(records, bindings, ledger_report, citation_report, census)
    failed = [name for name, passed in report["acceptance_checks"].items() if not passed]
    if failed:
        raise ContractError(f"acceptance checks failed: {failed}")
    if write:
        write_json(DEFAULT_CENSUS_PATH, census)
        write_json(check_dir / "canonical-census.json", census)
        write_json(check_dir / "external-fulltext-bindings.json", {
            "schema": "sf-stage1b-capability-delta-external-bindings-v1",
            "artifact_id": "SF-STAGE1B-CAPABILITY-DELTA-EXTERNAL-BINDINGS-RC1",
            "as_of": "2026-07-23",
            "data_root_source": "SPEECHRL_DATA_DIR_OR_PINNED_WORKSPACE_DEFAULT",
            "binding_count": len(bindings),
            "bindings": bindings,
        })
        write_json(check_dir / "contract-report.json", report)
        write_json(REVIEW_MANIFEST_PATH, build_review_manifest(check_dir))
    elif REVIEW_MANIFEST_PATH.exists():
        expected_manifest = build_review_manifest(check_dir)
        if load_json(REVIEW_MANIFEST_PATH) != expected_manifest:
            raise ContractError("review-package manifest is stale or not reproducible")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="materialize census and release-candidate check reports")
    parser.add_argument("--check-dir", type=Path, default=DEFAULT_CHECK_DIR)
    arguments = parser.parse_args()
    try:
        report = run(write=arguments.write, check_dir=arguments.check_dir)
    except ContractError as error:
        print(f"FAIL: {error}")
        return 1
    print(canonical_json({
        "status": report["status"],
        "delta_records": report["surface"]["delta_records"],
        "canonical_surface": report["surface"]["release_candidate_canonical_surface"],
        "requested_review_verdict": report["requested_review_verdict"],
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
