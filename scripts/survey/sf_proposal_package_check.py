#!/usr/bin/env python3
"""Build the honest pre-review package report without upgrading it to release."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import sf_bibliography_generator as bibliography  # noqa: E402
import sf_existing_corpus_disposition as corpus  # noqa: E402
import sf_identity_taxonomy_v7_test as v7  # noqa: E402
import sf_proposal_source_manifest as source_manifest  # noqa: E402
import sf_reviewer_proposal_check as proposal  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_PATH = (
    ROOT
    / "docs/checks/system-first-stage1a/context-v3/"
    "proposal-package-check.json"
)
EXPECTED_RELEASE_BLOCKERS = {
    "EVIDENCE_V7_LEAVES_OR_AGGREGATE_MISSING",
    "H5_CALIBRATION_PENDING",
    "PROPOSAL_NOT_PROMOTED_TO_ROUND16",
}
EXPECTED_V7_FAILURES = {"H5_CALIBRATION"}


def component(component_id: str, failures: list[str]) -> dict[str, Any]:
    return {
        "id": component_id,
        "result": "PASS" if not failures else "FAIL",
        "failure_codes": failures,
    }


def build_report() -> dict[str, Any]:
    manifest = source_manifest.load_manifest()
    manifest_failures = source_manifest.validate_manifest(manifest)
    manifest_failures.extend(source_manifest.check_manifest(manifest))

    proposal_inputs = proposal.load_inputs()
    proposal_text = proposal.PROPOSAL_PATH.read_text(encoding="utf-8")
    draft_failures = proposal.validate_draft(proposal_text, proposal_inputs)
    release_blockers = proposal.validate_release(proposal_text, proposal_inputs)
    release_guard_failures = []
    if set(release_blockers) != EXPECTED_RELEASE_BLOCKERS:
        release_guard_failures.append("UNEXPECTED_RELEASE_BLOCKER_SET")

    sources = corpus.load_source_rows()
    union = corpus.build_union(sources)
    union_failures = corpus.validate_union(union, sources)
    union_failures.extend(corpus.check_outputs(union))

    receipts = bibliography.load_receipts()
    bibliography_failures = bibliography.validate_receipts(receipts)
    bibliography_failures.extend(bibliography.check_output(receipts))
    selection = bibliography.build_selection_receipt(union)
    if (
        not bibliography.SELECTION_PATH.is_file()
        or bibliography.SELECTION_PATH.read_bytes()
        != bibliography.render_selection_bytes(selection)
    ):
        bibliography_failures.append("BIBLIOGRAPHY_SELECTION_DRIFT")

    v7_report = v7.build_report(platform_os="nt")
    v7_guard_failures = []
    if v7_report.get("verdict") != "FAIL":
        v7_guard_failures.append("PRE_REVIEW_V7_MUST_FAIL")
    if set(v7_report.get("failure_codes", [])) != EXPECTED_V7_FAILURES:
        v7_guard_failures.append("UNEXPECTED_V7_PRE_REVIEW_FAILURE_SET")

    components = [
        component("PROPOSAL_SOURCE_MANIFEST", sorted(set(manifest_failures))),
        component("REVIEWER_PROPOSAL_DRAFT", sorted(set(draft_failures))),
        component("FORMAL_RELEASE_GUARD", release_guard_failures),
        component("ACTIVE_CORPUS_UNION", sorted(set(union_failures))),
        component("BIBLIOGRAPHY_AND_SELECTION", sorted(set(bibliography_failures))),
        component("V7_EXPECTED_PRE_REVIEW_RED_GATE", v7_guard_failures),
    ]
    construction_failures = [
        row["id"] for row in components if row["result"] != "PASS"
    ]
    manifest_raw = source_manifest.OUTPUT_PATH.read_bytes()
    return {
        "artifact_id": "SF-PROPOSAL-PACKAGE-CHECK-2026-07-21-01",
        "schema": "sf-proposal-package-check-v1",
        "package_kind": "PRE_REVIEW_FAIL_CLOSED_PACKAGE",
        "source_manifest": {
            "path": source_manifest.OUTPUT_PATH.relative_to(ROOT).as_posix(),
            "source_commit": manifest["source_commit"],
            "sha256": hashlib.sha256(manifest_raw).hexdigest(),
        },
        "components": components,
        "construction_failure_codes": construction_failures,
        "construction_verdict": "PASS" if not construction_failures else "FAIL",
        "v7_expected_pre_review_failures": sorted(EXPECTED_V7_FAILURES),
        "release_blockers": sorted(release_blockers),
        "release_eligible": False,
        "release_verdict": "BLOCKED",
        "interpretation_guard": "Construction PASS means the frozen pre-review package is internally consistent and honestly blocked. It is not reviewer sign-off, owner authorization, or Stage-1B readiness.",
    }


def validate_report(report: dict[str, Any]) -> list[str]:
    failures: set[str] = set()
    if report.get("schema") != "sf-proposal-package-check-v1":
        failures.add("PACKAGE_REPORT_SCHEMA_MISMATCH")
    components = report.get("components")
    if not isinstance(components, list) or any(
        row.get("result") != "PASS" for row in components if isinstance(row, dict)
    ):
        failures.add("CONSTRUCTION_COMPONENT_FAILED")
    if report.get("construction_verdict") != "PASS" or report.get(
        "construction_failure_codes"
    ) != []:
        failures.add("CONSTRUCTION_VERDICT_MISMATCH")
    if report.get("release_eligible") is not False:
        failures.add("PRE_REVIEW_RELEASE_ELIGIBILITY_FORBIDDEN")
    if report.get("release_verdict") != "BLOCKED":
        failures.add("PRE_REVIEW_RELEASE_VERDICT_MUST_BE_BLOCKED")
    if set(report.get("release_blockers", [])) != EXPECTED_RELEASE_BLOCKERS:
        failures.add("RELEASE_BLOCKER_SET_MISMATCH")
    if set(report.get("v7_expected_pre_review_failures", [])) != EXPECTED_V7_FAILURES:
        failures.add("V7_FAILURE_SET_MISMATCH")
    return sorted(failures)


def render_report(report: dict[str, Any]) -> bytes:
    return (json.dumps(report, ensure_ascii=False, indent=1) + "\n").encode("utf-8")


def write_report(report: dict[str, Any], path: Path = OUTPUT_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(render_report(report))


def check_report(report: dict[str, Any], path: Path = OUTPUT_PATH) -> list[str]:
    if not path.is_file() or path.read_bytes() != render_report(report):
        return ["PROPOSAL_PACKAGE_REPORT_DRIFT"]
    return []


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args(argv)
    output = args.output if args.output.is_absolute() else ROOT / args.output
    report = build_report()
    failures = validate_report(report)
    if failures:
        print(json.dumps({"construction_verdict": "FAIL", "failure_codes": failures}))
        return 1
    if args.write:
        write_report(report, output)
        print(
            "construction=PASS release=BLOCKED wrote "
            + (output.relative_to(ROOT).as_posix() if output.is_relative_to(ROOT) else str(output))
        )
        return 0
    drift = check_report(report, output)
    print(
        json.dumps(
            {
                "construction_verdict": "PASS" if not drift else "FAIL",
                "release_verdict": "BLOCKED",
                "failure_codes": drift,
            }
        )
    )
    return 0 if not drift else 1


if __name__ == "__main__":
    sys.exit(main())
