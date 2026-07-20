#!/usr/bin/env python3
"""Aggregate one Windows and one POSIX evidence-v7 leaf into a receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
from pathlib import Path

from sf_json_contract import canonical_bytes, read as read_strict_json
from sf_identity_taxonomy_v7_test import (
    ARTIFACT_ID as LEAF_ARTIFACT_ID,
    CONTRACT_VERSION,
    IMPLEMENTATION_FREEZE,
    RUNNER_RELATIVE_PATH,
)


REPO = Path(__file__).resolve().parents[2]
AGGREGATE_ARTIFACT_ID = "SF-EVIDENCE-V7-AGGREGATE-2026-07-20-01"
DEFAULT_DIRECTORY = REPO / "docs/checks/system-first-stage1a/evidence-v7"
DEFAULT_NT_LEAF = DEFAULT_DIRECTORY / "identity-taxonomy-v7-test.nt.json"
DEFAULT_POSIX_LEAF = DEFAULT_DIRECTORY / "identity-taxonomy-v7-test.posix.json"
DEFAULT_OUTPUT = DEFAULT_DIRECTORY / "identity-taxonomy-v7-test.json"
DEFAULT_RUNNER = REPO.joinpath(*RUNNER_RELATIVE_PATH.split("/"))
SUMMARY_RE = re.compile(r"^(\d+)/(\d+) PASS$")


class AggregationError(ValueError):
    pass


def _load_leaf(path, role):
    path = Path(path)
    if not path.is_file():
        raise AggregationError(f"{role} leaf missing: {path}")
    try:
        document, raw = read_strict_json(path)
    except Exception as error:
        raise AggregationError(f"{role} leaf invalid: {error}") from error
    if not isinstance(document, dict):
        raise AggregationError(f"{role} leaf container invalid")
    return document, raw


def _validate_platform(leaf, role):
    platform = leaf.get("platform")
    if not isinstance(platform, dict) or platform.get("os") != role:
        raise AggregationError(f"{role} platform role mismatch")
    sys_platform = platform.get("sys_platform")
    if not isinstance(sys_platform, str):
        raise AggregationError(f"{role} platform stamp invalid")
    if role == "nt" and not sys_platform.startswith("win"):
        raise AggregationError("nt platform sys_platform is not Windows")
    if role == "posix" and sys_platform.startswith("win"):
        raise AggregationError("posix platform sys_platform is Windows")
    if not isinstance(platform.get("python"), str) or not platform["python"]:
        raise AggregationError(f"{role} Python platform stamp invalid")


def _validate_leaf(leaf, role, runner_sha256):
    _validate_platform(leaf, role)
    if leaf.get("artifact_id") != LEAF_ARTIFACT_ID:
        raise AggregationError(f"{role} leaf artifact id mismatch")
    if leaf.get("contract_version") != CONTRACT_VERSION:
        raise AggregationError(f"{role} contract version mismatch")
    if leaf.get("implementation_freeze") != IMPLEMENTATION_FREEZE:
        raise AggregationError(f"{role} implementation freeze mismatch")
    runner = leaf.get("runner")
    if not isinstance(runner, dict) or runner.get("path") != RUNNER_RELATIVE_PATH:
        raise AggregationError(f"{role} runner path mismatch")
    if runner.get("sha256") != runner_sha256:
        raise AggregationError(f"{role} runner blob mismatch")
    if leaf.get("verdict") != "PASS":
        raise AggregationError(f"{role} verdict is not PASS")
    if leaf.get("failure_codes") != []:
        raise AggregationError(f"{role} contains named failures")
    checks = leaf.get("checks")
    if not isinstance(checks, list) or not checks:
        raise AggregationError(f"{role} checks missing")
    if any(
        not isinstance(check, dict) or check.get("result") != "PASS"
        for check in checks
    ):
        raise AggregationError(f"{role} check result is not PASS")
    summary = leaf.get("summary")
    match = SUMMARY_RE.fullmatch(summary or "")
    if not match or int(match.group(1)) != len(checks) or int(match.group(2)) != len(checks):
        raise AggregationError(f"{role} summary semantics mismatch")
    if not isinstance(leaf.get("input_provenance"), dict):
        raise AggregationError(f"{role} input provenance invalid")
    if not re.fullmatch(r"[0-9a-f]{64}", leaf.get("input_snapshot_sha256", "")):
        raise AggregationError(f"{role} input snapshot hash invalid")
    if not isinstance(leaf.get("occupancy"), dict) or not leaf["occupancy"]:
        raise AggregationError(f"{role} occupancy missing")
    if not isinstance(leaf.get("mutation_results"), dict):
        raise AggregationError(f"{role} mutation results invalid")


def _display_path(path):
    path = Path(path)
    try:
        return path.resolve().relative_to(REPO.resolve()).as_posix()
    except (OSError, ValueError):
        return path.as_posix()


def aggregate_leaves(nt_leaf, posix_leaf, runner_path=DEFAULT_RUNNER):
    runner_path = Path(runner_path)
    if not runner_path.is_file():
        raise AggregationError(f"runner missing: {runner_path}")
    runner_sha256 = hashlib.sha256(runner_path.read_bytes()).hexdigest()
    nt, nt_raw = _load_leaf(nt_leaf, "nt")
    posix, posix_raw = _load_leaf(posix_leaf, "posix")
    _validate_leaf(nt, "nt", runner_sha256)
    _validate_leaf(posix, "posix", runner_sha256)

    shared_fields = (
        "artifact_id",
        "contract_version",
        "implementation_freeze",
        "runner",
        "input_provenance",
        "input_snapshot_sha256",
        "checks",
        "occupancy",
        "mutation_results",
        "failure_codes",
        "summary",
        "verdict",
    )
    differences = [field for field in shared_fields if nt.get(field) != posix.get(field)]
    if differences:
        raise AggregationError(
            "platform leaf output semantics differ: " + ", ".join(differences)
        )
    if nt_raw == posix_raw:
        raise AggregationError("platform leaves are byte-identical replacement copies")

    semantic_payload = {field: nt[field] for field in shared_fields}
    leaves = [
        {
            "platform_os": "nt",
            "path": _display_path(nt_leaf),
            "sha256": hashlib.sha256(nt_raw).hexdigest(),
        },
        {
            "platform_os": "posix",
            "path": _display_path(posix_leaf),
            "sha256": hashlib.sha256(posix_raw).hexdigest(),
        },
    ]
    return {
        "artifact_id": AGGREGATE_ARTIFACT_ID,
        "contract_version": CONTRACT_VERSION,
        "implementation_freeze": IMPLEMENTATION_FREEZE,
        "runner": nt["runner"],
        "input_provenance": nt["input_provenance"],
        "input_snapshot_sha256": nt["input_snapshot_sha256"],
        "output_semantics_sha256": hashlib.sha256(
            canonical_bytes(semantic_payload)
        ).hexdigest(),
        "leaves": leaves,
        "occupancy": nt["occupancy"],
        "summary": "2/2 platform leaves PASS and byte-bound",
        "verdict": "PASS",
    }


def encode_report(report):
    return (
        json.dumps(report, ensure_ascii=False, indent=1, allow_nan=False) + "\n"
    ).encode("utf-8")


def _atomic_write(path, payload):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, staging_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    staging = Path(staging_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        if staging.read_bytes() != payload:
            raise OSError("staged aggregate bytes differ")
        os.replace(staging, path)
        staging = None
    finally:
        if staging is not None:
            try:
                staging.unlink()
            except FileNotFoundError:
                pass


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--nt-leaf", default=os.fspath(DEFAULT_NT_LEAF))
    parser.add_argument("--posix-leaf", default=os.fspath(DEFAULT_POSIX_LEAF))
    parser.add_argument("--runner", default=os.fspath(DEFAULT_RUNNER))
    parser.add_argument("--output", default=os.fspath(DEFAULT_OUTPUT))
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    report = aggregate_leaves(
        args.nt_leaf, args.posix_leaf, runner_path=args.runner
    )
    payload = encode_report(report)
    output = Path(args.output)
    if args.check:
        if not output.is_file() or output.read_bytes() != payload:
            print("[FAIL] evidence-v7 aggregate missing or stale")
            return 1
        print("[OK] evidence-v7 aggregate exact")
        return 0
    _atomic_write(output, payload)
    print(f"wrote {output}: {report['summary']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
