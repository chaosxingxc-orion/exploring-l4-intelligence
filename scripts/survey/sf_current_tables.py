#!/usr/bin/env python3
"""Generate the bounded Stage-1A current opening-guarantees table."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from sf_current_path_contract import (
    TrustedCurrentPathError,
    read_fixed_bytes,
    resolve_fixed_output,
)
from sf_json_contract import JsonContractError, loads as strict_json_loads
from sf_query_compiler import atomic_write_bytes
from sf_release_binding_check import KEYMAP, render_headline
from sf_v6_report_contract import validate_v6_report_semantics
from sf_v6_snapshot_contract import (
    CURRENT_INPUT_SNAPSHOT_SHA256,
    load_v6_input_snapshot,
)


REPO = Path(__file__).resolve().parents[2]
REPORT_RELATIVE_PATH = (
    "docs/checks/system-first-stage1a/evidence-v6/"
    "identity-taxonomy-v6-test.json"
)
REPORT_PATH = REPO.joinpath(*REPORT_RELATIVE_PATH.split("/"))
OUTPUT_RELATIVE_PATH = "wiki/survey/current/tables/opening-guarantees.md"
OUTPUT_PATH = REPO.joinpath(*OUTPUT_RELATIVE_PATH.split("/"))


class CurrentTableError(RuntimeError):
    """A current-table input or byte check failed."""


def _json_compact(value: dict) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=False,
        separators=(",", ":"),
        allow_nan=False,
    )


def _release_binding(report: dict, source: str) -> dict:
    if report.get("verdict") != "PASS":
        raise CurrentTableError("v6 source report verdict must be PASS")
    occupancy = report.get("occupancy")
    if not isinstance(occupancy, dict):
        raise CurrentTableError("v6 source report lacks occupancy")
    binding = {"source": source}
    try:
        for key, accessor in KEYMAP.items():
            binding[key] = accessor(occupancy)
    except (KeyError, TypeError) as error:
        raise CurrentTableError(f"v6 occupancy contract incomplete: {error}") from error
    return binding


def render_opening_table(
    report: dict,
    report_relative_path: str,
    report_raw: bytes,
) -> bytes:
    """Render deterministic Markdown from one exact persisted v6 report."""

    binding = _release_binding(report, report_relative_path)
    policy = report["occupancy"]["policy_A"]
    method_paths = policy.get("n_method_paths")
    unique_works = policy.get("n_unique_works")
    if type(method_paths) is not int or type(unique_works) is not int:
        raise CurrentTableError("v6 report denominators must be integers")

    source_binding = {
        "path": report_relative_path,
        "sha256": hashlib.sha256(report_raw).hexdigest(),
    }
    lines = [
        "# Stage-1A Opening Guarantees",
        "",
        f"<!-- source_binding: {_json_compact(source_binding)} -->",
        f"<!-- release_binding: {_json_compact(binding)} -->",
        "",
        "- Evidence grade: **directional-only / hypothesis-grade** Stage-1A evidence.",
        f"- Denominators: **method-path = {method_paths}**; "
        f"**unique-work = {unique_works}**.",
        "- Execution boundary: **zero Stage-1B executions in this repair**.",
        "- Authority boundary: this is **not a readiness determination**, "
        "**not a reviewer signature**, and **not owner Stage-1B execution approval**.",
        "",
        "<!-- generated_headline_begin -->",
        render_headline(report),
        "<!-- generated_headline_end -->",
        "",
    ]
    return "\n".join(lines).encode("utf-8")


def parse_validated_report(report_raw: bytes, current_snapshot: dict) -> dict:
    """Strict-load and bind one base report to the current frozen release."""

    try:
        report = strict_json_loads(report_raw, "current v6 opening report")
    except JsonContractError as error:
        raise CurrentTableError(str(error)) from error
    if not isinstance(report, dict):
        raise CurrentTableError("v6 report root must be an object")
    failures = validate_v6_report_semantics(report)
    if failures:
        raise CurrentTableError("frozen v6 report semantics failed: " + "; ".join(failures))
    if not isinstance(current_snapshot, dict):
        raise CurrentTableError("current release snapshot must be an object")
    if report.get("input_provenance") != current_snapshot.get("input_provenance"):
        raise CurrentTableError("current release snapshot provenance mismatch")
    if report.get("input_snapshot_sha256") != current_snapshot.get(
        "input_snapshot_sha256"
    ):
        raise CurrentTableError("current release snapshot SHA-256 mismatch")
    try:
        policy = report["occupancy"]["policy_A"]
        method_paths = policy["n_method_paths"]
        unique_works = policy["n_unique_works"]
    except (KeyError, TypeError) as error:
        raise CurrentTableError(f"v6 denominators missing: {error}") from error
    if type(method_paths) is not int or type(unique_works) is not int:
        raise CurrentTableError("v6 report denominators must be non-boolean integers")
    return report


def _resolve_output_path(
    repo: Path, target: Path, *, allow_missing_leaf: bool
) -> Path:
    return resolve_fixed_output(
        repo,
        target,
        OUTPUT_RELATIVE_PATH,
        allow_missing_leaf=allow_missing_leaf,
    )


def _read_report_bytes(repo: Path, target: Path) -> bytes:
    return read_fixed_bytes(repo, target, REPORT_RELATIVE_PATH)


def expected_bytes() -> bytes:
    try:
        report_raw = _read_report_bytes(REPO, REPORT_PATH)
        current_snapshot = load_v6_input_snapshot(
            REPO,
            expected_snapshot_sha256=CURRENT_INPUT_SNAPSHOT_SHA256,
        )
        report = parse_validated_report(report_raw, current_snapshot)
    except CurrentTableError:
        raise
    except (TrustedCurrentPathError, JsonContractError, ValueError, OSError) as error:
        raise CurrentTableError(f"cannot read v6 report: {error}") from error
    return render_opening_table(report, REPORT_RELATIVE_PATH, report_raw)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    return parser


def main(argv=None) -> int:
    args = _parser().parse_args(argv)
    try:
        expected = expected_bytes()
        if args.write:
            output = _resolve_output_path(REPO, OUTPUT_PATH, allow_missing_leaf=True)
            atomic_write_bytes(output, expected)
            print(f"wrote {OUTPUT_RELATIVE_PATH}")
            return 0
        try:
            _resolve_output_path(REPO, OUTPUT_PATH, allow_missing_leaf=False)
            actual = read_fixed_bytes(REPO, OUTPUT_PATH, OUTPUT_RELATIVE_PATH)
        except (OSError, TrustedCurrentPathError) as error:
            raise CurrentTableError(f"current table missing: {error}") from error
        if actual != expected:
            raise CurrentTableError(
                "current table byte mismatch: "
                f"expected {hashlib.sha256(expected).hexdigest()}, "
                f"found {hashlib.sha256(actual).hexdigest()}"
            )
    except (CurrentTableError, TrustedCurrentPathError, OSError, ValueError) as error:
        print(f"[CURRENT-TABLE] {error}")
        print("current opening table: FAIL")
        return 1
    print("current opening table: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
