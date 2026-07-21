#!/usr/bin/env python3
"""Build the exact, committed pre-review source set for the round-16 proposal."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_PATH = ROOT / "wiki/survey/current/data/proposal-source-manifest-v1.json"

SOURCE_SPECS = (
    ("project_thesis", "wiki/Project-Thesis.md", "north_star"),
    ("current_research_state", "wiki/Research-Objective.md", "current_state"),
    ("current_router", "wiki/survey/current/README.md", "search_design"),
    ("current_status", "wiki/survey/current/status.md", "search_design"),
    ("current_protocol", "wiki/survey/current/protocol.md", "search_design"),
    ("legacy_current_manifest", "wiki/survey/current/manifest.json", "legacy_release_context"),
    ("mapping_methods_adaptation", "wiki/survey/current/mapping-methods-adaptation.md", "methods"),
    ("modality_specificity_codebook", "wiki/survey/current/modality-specificity-codebook.md", "codebook"),
    ("h5_calibration", "wiki/survey/current/data/modality-specificity-calibration-v1.json", "calibration"),
    ("h5_calibration_validator", "scripts/survey/sf_h5_calibration_contract.py", "release_gate"),
    ("pdf_extractor_environment", "wiki/survey/current/data/pdf-extractor-environment-v1.json", "environment"),
    ("pdf_extractor_validator", "scripts/survey/sf_pdf_extractor_contract.py", "release_gate"),
    ("query_compiler", "scripts/survey/sf_query_compiler.py", "search_execution"),
    ("query_compiler_profile_test", "scripts/survey/test_sf_query_compiler_profiles.py", "search_execution"),
    ("frozen_queries", "wiki/survey/2026-07-15-sf-queries.jsonl", "search_execution"),
    ("t1_routes", "wiki/survey/2026-07-17-sf-t1-routes-v3.jsonl", "search_execution"),
    ("t1_wordlist", "wiki/survey/2026-07-16-sf-t1-wordlist-v1.json", "search_execution"),
    ("t1_route_design", "wiki/survey/2026-07-16-sf-t1-proceedings-routes.md", "search_execution"),
    ("t1_route_validator", "scripts/survey/sf_t1_routes_validate.py", "search_execution"),
    ("rec_templates", "wiki/survey/2026-07-15-sf-blank-templates.md", "screening_and_coding"),
    ("record_validator", "scripts/survey/sf_record_validator.py", "screening_and_coding"),
    ("record_validator_test", "scripts/survey/sf_record_validator_test.py", "screening_and_coding"),
    ("schema_adjudication", "wiki/survey/current/data/schema-v3-adjudication.json", "adjudication"),
    ("known_item_coding", "wiki/survey/current/data/known-item-coding-v7.json", "adjudication"),
    ("sidecar_deepverifier", "wiki/survey/current/data/schema-v3/sidecars/2026.findings-acl.1243.sidecar.json", "adjudication"),
    ("sidecar_coder_1724", "wiki/survey/current/data/schema-v3/sidecars/2026.findings-acl.1724.sidecar.json", "adjudication"),
    ("sidecar_dream", "wiki/survey/current/data/schema-v3/sidecars/2026.findings-acl.511.sidecar.json", "adjudication"),
    ("sidecar_2602_16485", "wiki/survey/current/data/schema-v3/sidecars/2602.16485.sidecar.json", "adjudication"),
    ("sidecar_2604_16529", "wiki/survey/current/data/schema-v3/sidecars/2604.16529.sidecar.json", "adjudication"),
    ("sidecar_2605_08083", "wiki/survey/current/data/schema-v3/sidecars/2605.08083.sidecar.json", "adjudication"),
    ("sidecar_2606_01667", "wiki/survey/current/data/schema-v3/sidecars/2606.01667.sidecar.json", "adjudication"),
    ("sidecar_2606_03054", "wiki/survey/current/data/schema-v3/sidecars/2606.03054.sidecar.json", "adjudication"),
    ("absence_adjudication", "wiki/survey/current/data/absence-evidence-adjudication-v3.json", "adjudication"),
    ("semantic_corrections", "wiki/survey/current/data/negative-evidence-semantic-corrections-v2.json", "adjudication"),
    ("v7_leaf_runner", "scripts/survey/sf_identity_taxonomy_v7_test.py", "release_gate"),
    ("v7_aggregator", "scripts/survey/sf_evidence_v7_aggregate.py", "release_gate"),
    ("dual_platform_checker", "scripts/survey/sf_dual_platform_check.py", "release_gate"),
    ("active_union", "wiki/survey/current/data/existing-corpus-disposition-v1.json", "corpus"),
    ("active_union_check", "docs/checks/system-first-stage1a/context-v2/existing-corpus-disposition-check.json", "corpus"),
    ("reviewer_known_items", "wiki/survey/current/data/reviewer-known-items-v3.json", "corpus"),
    ("seed_manifest", "wiki/survey/2026-07-15-sf-seed-manifest.jsonl", "corpus"),
    ("fulltext_ledger", "wiki/survey/2026-07-17-sf-fulltext-ledger.jsonl", "corpus"),
    ("official_metadata_receipts", "wiki/survey/current/data/official-metadata-receipts-v1.jsonl", "bibliography"),
    ("reviewer_bibliography", "wiki/survey/current/bibliography.md", "bibliography"),
    ("bibliography_selection", "wiki/survey/current/data/reviewer-bibliography-selection-v1.json", "bibliography"),
    ("bibliography_generator", "scripts/survey/sf_bibliography_generator.py", "bibliography"),
    ("metadata_fetcher", "scripts/survey/sf_official_metadata_fetch.py", "bibliography"),
    ("attempt_registry", "docs/integrity/experiment_attempt_registry.jsonl", "integrity"),
    ("round15_review", "wiki/audit/system-first-stage1a/pre-round-15/2026-07-21-independent-doctoral-review-of-stage1a-research-proposal.md", "review"),
    ("round16_precheck_review", "wiki/audit/external-reviews/2026-07-21-round16-precheck-rereview-of-stage1a-research-proposal.md", "review"),
    ("proposal_draft", "wiki/survey/workbench/system-first-stage1a/2026-07-21-stage1a-working-brief.md", "proposal"),
    ("proposal_checker", "scripts/survey/sf_reviewer_proposal_check.py", "proposal"),
)

DEFERRED_RELEASE_ARTIFACTS = (
    ("evidence_v7_windows_leaf", "docs/checks/system-first-stage1a/evidence-v7/identity-taxonomy-v7-test.nt.json", "H5 dual-coder calibration complete, 4/4 correction decisions, 18/18 active absence decisions, and exact NT extractor match"),
    ("evidence_v7_wsl_leaf", "docs/checks/system-first-stage1a/evidence-v7/identity-taxonomy-v7-test.posix.json", "H5 dual-coder calibration complete, 4/4 correction decisions, 18/18 active absence decisions, and exact POSIX extractor match"),
    ("evidence_v7_aggregate", "docs/checks/system-first-stage1a/evidence-v7/identity-taxonomy-v7-test.json", "both platform leaves PASS on identical inputs"),
    ("formal_round16_proposal", "wiki/audit/system-first-stage1a/round-16/research-proposal-and-stage1b-signoff-request.md", "fresh v7 aggregate PASS and hostile pre-release review"),
)


def git(*args: str, raw: bool = False) -> str | bytes:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=not raw,
    )
    return result.stdout if raw else result.stdout.strip()


def committed_bytes(commit: str, path: str) -> bytes:
    return git("show", f"{commit}:{path}", raw=True)  # type: ignore[return-value]


def source_row(commit: str, role: str, path: str, surface: str) -> dict[str, Any]:
    raw = committed_bytes(commit, path)
    return {
        "role": role,
        "path": path,
        "surface": surface,
        "git_blob": git("rev-parse", f"{commit}:{path}"),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }


def build_manifest(commit: str | None = None) -> dict[str, Any]:
    commit = commit or str(git("rev-parse", "HEAD"))
    absence = json.loads(
        committed_bytes(
            commit, "wiki/survey/current/data/absence-evidence-adjudication-v3.json"
        )
    )
    corrections = json.loads(
        committed_bytes(
            commit,
            "wiki/survey/current/data/negative-evidence-semantic-corrections-v2.json",
        )
    )
    h5 = json.loads(
        committed_bytes(
            commit, "wiki/survey/current/data/modality-specificity-calibration-v1.json"
        )
    )
    pdf_extractor = json.loads(
        committed_bytes(
            commit, "wiki/survey/current/data/pdf-extractor-environment-v1.json"
        )
    )
    reviewer_known = json.loads(
        committed_bytes(
            commit, "wiki/survey/current/data/reviewer-known-items-v3.json"
        )
    )
    return {
        "artifact_id": "SF-PROPOSAL-SOURCE-MANIFEST-V1-2026-07-21-01",
        "schema": "sf-proposal-source-manifest-v1",
        "lifecycle": "PRE_REVIEW_FROZEN_SOURCE_SET",
        "source_commit": commit,
        "scope": "Exact committed inputs for the round-16 reviewer proposal; this is not the legacy current manifest and is not a Stage-1B authorization.",
        "files": [source_row(commit, *spec) for spec in SOURCE_SPECS],
        "semantic_gate": {
            "inventory_identity": corrections["inventory_reconciliation"]["identity"],
            "correction_inventory": len(corrections["corrections"]),
            "correction_reviews_recorded": len(corrections["review_rows"]),
            "active_absence_inventory": len(absence["proof_rows"]),
            "active_absence_reviews_recorded": len(absence["rows"]),
        },
        "h5_gate": {
            "status": h5.get("status"),
            "paper_inventory": len(h5.get("papers", [])),
            "coder_inventory": len(h5.get("coders", [])),
            "planned_denominator": h5.get("agreement_report", {}).get("planned_denominator"),
            "observed_comparable_denominator": h5.get("agreement_report", {}).get("observed_comparable_denominator"),
        },
        "pdf_extractor_gate": {
            "version_policy": pdf_extractor.get("version_policy"),
            "platform_roles": sorted(pdf_extractor.get("canonical_environments", {})),
            "toolgate_probe_page": pdf_extractor.get("toolgate_probe", {}).get("page"),
        },
        "reviewer_known_gate": {
            "item_inventory": len(reviewer_known.get("items", [])),
            "round16_new_item_ids": [
                row.get("arxiv_id") for row in reviewer_known.get("items", [])[-5:]
            ],
            "query_recall_credit": reviewer_known.get("query_recall_credit"),
        },
        "deferred_release_artifacts": [
            {
                "role": role,
                "path": path,
                "state": "REQUIRED_AFTER_INDEPENDENT_REVIEW",
                "trigger": trigger,
            }
            for role, path, trigger in DEFERRED_RELEASE_ARTIFACTS
        ],
        "release_eligible": False,
        "release_blockers": [
            "H5_SECOND_INDEPENDENT_CODER_AND_ADJUDICATION_PENDING",
            "FRESH_V7_DUAL_PLATFORM_EVIDENCE_MISSING",
            "FORMAL_ROUND16_PROPOSAL_NOT_CREATED",
            "INDEPENDENT_SEARCH_DESIGN_SIGNOFF_MISSING",
            "OWNER_SAME_PACKAGE_AUTHORIZATION_MISSING",
        ],
    }


def validate_manifest(document: dict[str, Any]) -> list[str]:
    failures: set[str] = set()
    if document.get("schema") != "sf-proposal-source-manifest-v1":
        failures.add("MANIFEST_SCHEMA_MISMATCH")
    commit = document.get("source_commit")
    rows = document.get("files")
    if not isinstance(commit, str) or not isinstance(rows, list):
        return sorted(failures | {"MANIFEST_STRUCTURE_INVALID"})
    roles = [row.get("role") for row in rows if isinstance(row, dict)]
    paths = [row.get("path") for row in rows if isinstance(row, dict)]
    if len(roles) != len(set(roles)):
        failures.add("DUPLICATE_SOURCE_ROLE")
    if len(paths) != len(set(paths)):
        failures.add("DUPLICATE_SOURCE_PATH")
    expected_paths = {path for _, path, _ in SOURCE_SPECS}
    if set(paths) != expected_paths:
        failures.add("SOURCE_DENOMINATOR_MISMATCH")
    for row in rows:
        if not isinstance(row, dict):
            failures.add("SOURCE_ROW_INVALID")
            continue
        path = row.get("path")
        try:
            raw = committed_bytes(commit, path)
            blob = git("rev-parse", f"{commit}:{path}")
            head_blob = git("rev-parse", f"HEAD:{path}")
        except (subprocess.CalledProcessError, TypeError):
            failures.add("SOURCE_UNAVAILABLE")
            continue
        if row.get("git_blob") != blob or head_blob != blob:
            failures.add("SOURCE_GIT_BLOB_MISMATCH")
        if row.get("sha256") != hashlib.sha256(raw).hexdigest():
            failures.add("SOURCE_SHA256_MISMATCH")
    deferred = document.get("deferred_release_artifacts")
    if not isinstance(deferred, list) or len(deferred) != len(DEFERRED_RELEASE_ARTIFACTS):
        failures.add("DEFERRED_RELEASE_INVENTORY_MISMATCH")
    if document.get("release_eligible") is not False:
        failures.add("PRE_REVIEW_RELEASE_ELIGIBILITY_FORBIDDEN")
    semantic = document.get("semantic_gate", {})
    if semantic != {
        "inventory_identity": "22 = 4 + 18",
        "correction_inventory": 4,
        "correction_reviews_recorded": 4,
        "active_absence_inventory": 18,
        "active_absence_reviews_recorded": 18,
    }:
        failures.add("SEMANTIC_GATE_STATE_MISMATCH")
    if document.get("h5_gate") != {
        "status": "PENDING_SECOND_INDEPENDENT_CODER",
        "paper_inventory": 3,
        "coder_inventory": 1,
        "planned_denominator": 21,
        "observed_comparable_denominator": 0,
    }:
        failures.add("H5_GATE_STATE_MISMATCH")
    if document.get("pdf_extractor_gate") != {
        "version_policy": "EXACT_MATCH_FAIL_CLOSED",
        "platform_roles": ["nt", "posix"],
        "toolgate_probe_page": 11,
    }:
        failures.add("PDF_EXTRACTOR_GATE_STATE_MISMATCH")
    reviewer_known = document.get("reviewer_known_gate", {})
    if (
        reviewer_known.get("item_inventory") != 15
        or reviewer_known.get("round16_new_item_ids")
        != ["2606.00579", "2606.03183", "2502.19328", "2605.10344", "2508.00890"]
        or reviewer_known.get("query_recall_credit") is not False
    ):
        failures.add("REVIEWER_KNOWN_GATE_STATE_MISMATCH")
    return sorted(failures)


def render_manifest(document: dict[str, Any]) -> bytes:
    return (json.dumps(document, ensure_ascii=False, indent=1) + "\n").encode("utf-8")


def load_manifest(path: Path = OUTPUT_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_manifest(document: dict[str, Any], path: Path = OUTPUT_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(render_manifest(document))


def check_manifest(document: dict[str, Any], path: Path = OUTPUT_PATH) -> list[str]:
    if not path.is_file() or path.read_bytes() != render_manifest(document):
        return ["PROPOSAL_SOURCE_MANIFEST_DRIFT"]
    return []


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args(argv)
    output = args.output if args.output.is_absolute() else ROOT / args.output
    document = build_manifest() if args.write else load_manifest(output)
    failures = validate_manifest(document)
    if failures:
        print(json.dumps({"verdict": "FAIL", "failure_codes": failures}, indent=2))
        return 1
    if args.write:
        write_manifest(document, output)
        print(f"PASS wrote {output.relative_to(ROOT).as_posix() if output.is_relative_to(ROOT) else output}")
        return 0
    drift = check_manifest(document, output)
    print(json.dumps({"verdict": "PASS" if not drift else "FAIL", "failure_codes": drift}))
    return 0 if not drift else 1


if __name__ == "__main__":
    sys.exit(main())
