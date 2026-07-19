#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fail-closed dual-platform aggregator for identity-taxonomy evidence."""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path, PurePosixPath


REPO = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from sf_json_contract import (  # noqa: E402
    JsonContractError,
    canonical_bytes,
    read as read_strict_json,
)
from sf_schema_v3_release_contract import (  # noqa: E402
    ReleaseContractError,
    resolve_trusted_repo_path,
)
from sf_v6_report_contract import validate_v6_report_semantics  # noqa: E402
from sf_v6_snapshot_contract import (  # noqa: E402
    CURRENT_INPUT_SNAPSHOT_SHA256,
    load_v6_input_snapshot,
)


DEFAULT_BASE_RELATIVE = (
    "docs/checks/system-first-stage1a/evidence-v6/"
    "identity-taxonomy-v6-test"
)
LEGACY_BASE_RELATIVE = (
    "docs/checks/2026-07-19-sf-identity-taxonomy-v5-test"
)
DEFAULT_BASE = REPO.joinpath(*DEFAULT_BASE_RELATIVE.split("/"))
LEGACY_BASE = REPO.joinpath(*LEGACY_BASE_RELATIVE.split("/"))
PLATFORMS = ("nt", "posix")
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
PROVENANCE_SINGLETONS = (
    "taxonomy_v5",
    "taxonomy",
    "coding",
    "adjudication",
)


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
    parser.add_argument(
        "--legacy-regression",
        action="store_true",
        help="allow only the exact declared frozen v5 regression base",
    )
    return parser


def _portable_base_relative(raw):
    """Return one literal, canonical base path below REPO without resolving."""
    if not isinstance(raw, str) or not raw:
        raise ValueError("base path must be a nonempty string")
    path = Path(raw)
    if path.is_absolute():
        try:
            relative = path.relative_to(REPO)
        except ValueError as error:
            raise ValueError(
                "absolute base path must be below the repository"
            ) from error
        canonical = REPO.joinpath(*relative.parts)
        if raw != str(canonical):
            raise ValueError(
                "absolute base path must be its literal canonical spelling"
            )
        parts = relative.parts
    else:
        if "\\" in raw or re.match(r"^[A-Za-z]:", raw):
            raise ValueError("relative base path must use portable POSIX spelling")
        pieces = raw.split("/")
        if any(piece in ("", ".", "..") for piece in pieces):
            raise ValueError("relative base path contains an unsafe component")
        pure = PurePosixPath(raw)
        if pure.is_absolute():
            raise ValueError("relative base path must not be absolute")
        parts = pure.parts
    if any(part in ("", ".", "..") for part in parts):
        raise ValueError("base path contains an unsafe component")
    return PurePosixPath(*parts).as_posix()


def _select_base(raw, legacy_regression):
    if legacy_regression:
        allowed = {LEGACY_BASE_RELATIVE, str(LEGACY_BASE)}
        if raw not in allowed:
            raise ValueError(
                "legacy regression requires the exact declared v5 base literal"
            )
        return LEGACY_BASE_RELATIVE, True
    return _portable_base_relative(raw), False


def _snapshot_path(base_relative, platform):
    relative = f"{base_relative}.{platform}.json"
    target = REPO.joinpath(*relative.split("/"))
    return resolve_trusted_repo_path(
        REPO,
        target,
        expected_relative=relative,
        expected_kind="file",
    )


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


def _validate_provenance(report, platform, current_snapshot):
    failures = []
    provenance = report.get("input_provenance")
    expected_keys = set(PROVENANCE_SINGLETONS) | {"sidecars"}
    if not isinstance(provenance, dict) or set(provenance) != expected_keys:
        return [
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
    else:
        try:
            recomputed = hashlib.sha256(canonical_bytes(provenance)).hexdigest()
        except JsonContractError as error:
            failures.append(f"{platform}: provenance is not canonical JSON: {error}")
        else:
            if snapshot != recomputed:
                failures.append(
                    f"{platform}: input_snapshot_sha256 does not recompute "
                    "from provenance"
                )
    if current_snapshot is not None:
        if provenance != current_snapshot["input_provenance"]:
            failures.append(
                f"{platform}: provenance does not match current release bytes"
            )
        if snapshot != current_snapshot["input_snapshot_sha256"]:
            failures.append(
                f"{platform}: snapshot does not match current release bytes"
            )
    return failures


def _validate_report(report, suffix, legacy, current_snapshot):
    failures = []
    if not isinstance(report, dict):
        return [f"{suffix}: report root must be an object"]
    platform = report.get("platform")
    if not isinstance(platform, dict):
        failures.append(f"{suffix}: platform must be an object")
    else:
        if platform.get("os") != suffix:
            failures.append(
                f"{suffix}: platform.os {platform.get('os')} "
                f"does not match suffix {suffix}"
            )
        if not isinstance(platform.get("python"), str) or not platform.get(
            "python"
        ):
            failures.append(f"{suffix}: platform.python must be nonempty")
    if report.get("verdict") != "PASS":
        failures.append(f"{suffix}: verdict {report.get('verdict')}")
    if not isinstance(report.get("occupancy"), dict):
        failures.append(f"{suffix}: occupancy must be an object")
    if not legacy:
        failures.extend(_validate_provenance(report, suffix, current_snapshot))
        failures.extend(
            f"{suffix}: frozen report: {failure}"
            for failure in validate_v6_report_semantics(report)
        )
    return failures


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = _parser().parse_args(argv)
    try:
        base_relative, legacy = _select_base(
            args.base, args.legacy_regression
        )
    except ValueError as error:
        print(f"[DUAL] base/legacy path rejected: {error}")
        print("dual-platform check: FAIL (1 failures)")
        return 1

    failures = []
    current_snapshot = None
    if legacy:
        print("legacy provenance compatibility: ENABLED")
    else:
        try:
            current_snapshot = load_v6_input_snapshot(
                REPO,
                expected_snapshot_sha256=CURRENT_INPUT_SNAPSHOT_SHA256,
            )
        except Exception as error:
            failures.append(
                f"current release snapshot failed: {type(error).__name__}: {error}"
            )

    reports = {}
    report_failures = {}
    for platform in PLATFORMS:
        try:
            path = _snapshot_path(base_relative, platform)
            report, _ = read_strict_json(path)
        except (ReleaseContractError, JsonContractError, OSError) as error:
            failures.append(f"{platform}: strict trusted snapshot load failed: {error}")
            continue
        reports[platform] = report
        report_failures[platform] = _validate_report(
            report, platform, legacy, current_snapshot
        )
        failures.extend(report_failures[platform])

    if len(reports) == len(PLATFORMS):
        nt_report = reports["nt"]
        posix_report = reports["posix"]
        pair_valid = (
            isinstance(nt_report, dict)
            and isinstance(posix_report, dict)
            and not report_failures["nt"]
            and not report_failures["posix"]
        )
        if isinstance(nt_report, dict) and isinstance(posix_report, dict):
            if not legacy:
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
                if pair_valid and current_snapshot is not None:
                    print("current release binding: CONFIRMED")
                    print("frozen report semantics: CONFIRMED")
                    print("input snapshot equality: CONFIRMED")
                    print("input provenance equality: CONFIRMED")
            if nt_report.get("occupancy") != posix_report.get("occupancy"):
                failures.append("occupancy blocks differ between platforms")
            elif pair_valid:
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
