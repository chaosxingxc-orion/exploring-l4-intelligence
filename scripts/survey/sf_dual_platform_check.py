#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fail-closed dual-platform aggregator for identity-taxonomy evidence."""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from sf_json_contract import (  # noqa: E402
    JsonContractError,
    canonical_bytes,
    read as read_strict_json,
)


DEFAULT_BASE_RELATIVE = (
    "docs/checks/system-first-stage1a/evidence-v6/"
    "identity-taxonomy-v6-test"
)
DEFAULT_BASE = REPO / DEFAULT_BASE_RELATIVE
LEGACY_BASE = REPO / "docs/checks/2026-07-19-sf-identity-taxonomy-v5-test"
PLATFORMS = ("nt", "posix")
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
PROVENANCE_SINGLETONS = (
    "taxonomy_v5",
    "taxonomy",
    "coding",
    "adjudication",
)


def _resolve_base(value):
    path = Path(value)
    if not path.is_absolute():
        path = REPO / path
    return path.resolve(strict=False)


def _parser():
    parser = argparse.ArgumentParser(
        description="Aggregate strict nt and posix identity-taxonomy snapshots."
    )
    parser.add_argument(
        "--base",
        default=DEFAULT_BASE_RELATIVE,
        help=(
            "report base path without .<platform>.json "
            f"(default: {DEFAULT_BASE_RELATIVE})"
        ),
    )
    return parser


def _provenance_entry_failures(entry, label):
    failures = []
    if not isinstance(entry, dict) or set(entry) != {"path", "sha256"}:
        return [f"{label}: expected exact path/sha256 provenance entry"]
    if not isinstance(entry["path"], str) or not entry["path"]:
        failures.append(f"{label}: provenance path must be a nonempty string")
    if not isinstance(entry["sha256"], str) or not SHA256_RE.fullmatch(
        entry["sha256"]
    ):
        failures.append(f"{label}: provenance sha256 must be lowercase hex")
    return failures


def _validate_provenance(report, platform):
    failures = []
    provenance = report.get("input_provenance")
    expected_keys = set(PROVENANCE_SINGLETONS) | {"sidecars"}
    if not isinstance(provenance, dict) or set(provenance) != expected_keys:
        return None, None, [
            f"{platform}: input_provenance must contain the exact v6 inputs"
        ]
    for key in PROVENANCE_SINGLETONS:
        failures.extend(
            _provenance_entry_failures(provenance[key], f"{platform}:{key}")
        )
    sidecars = provenance["sidecars"]
    if not isinstance(sidecars, list) or len(sidecars) != 8:
        failures.append(f"{platform}: provenance must contain exactly 8 sidecars")
    else:
        for index, entry in enumerate(sidecars):
            failures.extend(
                _provenance_entry_failures(
                    entry, f"{platform}:sidecars[{index}]"
                )
            )
        paths = [
            entry.get("path") for entry in sidecars if isinstance(entry, dict)
        ]
        if len(paths) != len(set(paths)):
            failures.append(f"{platform}: sidecar provenance paths are duplicated")
    snapshot = report.get("input_snapshot_sha256")
    if not isinstance(snapshot, str) or not SHA256_RE.fullmatch(snapshot):
        failures.append(
            f"{platform}: input_snapshot_sha256 must be lowercase hex"
        )
        return provenance, snapshot, failures
    try:
        recomputed = hashlib.sha256(canonical_bytes(provenance)).hexdigest()
    except JsonContractError as error:
        failures.append(f"{platform}: provenance is not canonical JSON: {error}")
    else:
        if snapshot != recomputed:
            failures.append(
                f"{platform}: input_snapshot_sha256 does not recompute from provenance"
            )
    return provenance, snapshot, failures


def _validate_report(report, suffix, require_provenance):
    failures = []
    if not isinstance(report, dict):
        return [f"{suffix}: report root must be an object"]
    platform = report.get("platform")
    if not isinstance(platform, dict):
        failures.append(f"{suffix}: platform must be an object")
    else:
        if platform.get("os") != suffix:
            failures.append(
                f"{suffix}: platform.os {platform.get('os')} does not match suffix {suffix}"
            )
        if not isinstance(platform.get("python"), str) or not platform.get(
            "python"
        ):
            failures.append(f"{suffix}: platform.python must be nonempty")
    if report.get("verdict") != "PASS":
        failures.append(f"{suffix}: verdict {report.get('verdict')}")
    if not isinstance(report.get("occupancy"), dict):
        failures.append(f"{suffix}: occupancy must be an object")
    if require_provenance:
        _, _, provenance_failures = _validate_provenance(report, suffix)
        failures.extend(provenance_failures)
    return failures


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = _parser().parse_args(argv)
    base = _resolve_base(args.base)
    legacy = base == LEGACY_BASE.resolve(strict=False)
    reports = {}
    report_failures = {}
    failures = []
    if legacy:
        print("legacy provenance compatibility: ENABLED")
    for platform in PLATFORMS:
        path = Path(f"{base}.{platform}.json")
        if not path.is_file():
            failures.append(f"missing platform snapshot: {path.name}")
            continue
        try:
            report, _ = read_strict_json(path)
        except (JsonContractError, OSError) as error:
            failures.append(f"{platform}: strict snapshot load failed: {error}")
            continue
        reports[platform] = report
        report_failures[platform] = _validate_report(
            report, platform, not legacy
        )
        failures.extend(report_failures[platform])

    if len(reports) == len(PLATFORMS):
        nt_report = reports["nt"]
        posix_report = reports["posix"]
        if isinstance(nt_report, dict) and isinstance(posix_report, dict):
            if not legacy:
                nt_provenance_failures = _validate_provenance(
                    nt_report, "nt"
                )[2]
                posix_provenance_failures = _validate_provenance(
                    posix_report, "posix"
                )[2]
                snapshots_equal = (
                    nt_report.get("input_snapshot_sha256")
                    == posix_report.get("input_snapshot_sha256")
                )
                provenance_equal = (
                    nt_report.get("input_provenance")
                    == posix_report.get("input_provenance")
                )
                if not snapshots_equal:
                    failures.append("input snapshot hashes differ between platforms")
                if not provenance_equal:
                    failures.append("input provenance differs between platforms")
                if (
                    snapshots_equal
                    and provenance_equal
                    and not nt_provenance_failures
                    and not posix_provenance_failures
                    and not report_failures["nt"]
                    and not report_failures["posix"]
                ):
                    print("input snapshot equality: CONFIRMED")
                    print("input provenance equality: CONFIRMED")
            if nt_report.get("occupancy") != posix_report.get("occupancy"):
                failures.append("occupancy blocks differ between platforms")
            elif (
                isinstance(nt_report.get("occupancy"), dict)
                and not report_failures["nt"]
                and not report_failures["posix"]
            ):
                print(
                    f"nt: {nt_report.get('platform')}  "
                    f"posix: {posix_report.get('platform')}"
                )
                print("occupancy equality: CONFIRMED")

    for failure in failures:
        print(f"[DUAL] {failure}")
    print(
        f"dual-platform check: {'FAIL' if failures else 'PASS'} "
        f"({len(failures)} failures)"
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
