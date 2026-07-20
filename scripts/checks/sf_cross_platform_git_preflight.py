#!/usr/bin/env python3
"""Build/check the Windows+WSL Git-substrate receipt for Stage-1A."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath


REPO = Path(__file__).resolve().parents[2]
PLAN_PATH = (
    "docs/superpowers/plans/"
    "2026-07-20-stage1a-final-gates-and-reviewer-proposal.md"
)
EVIDENCE_V6_RELEASE_ANCHOR = "2f16b23bdcda18b2a8d1c79f708d4197f9c51c5f"
PLAN_REVIEW_ANCHOR = "17e230f673ee27efb5e74f6fbfab15c7061d22da"
IMPLEMENTATION_FREEZE = "d4ec803417e1e9cfe9120afbce97c676cebbe6ee"
IMPLEMENTATION_PLAN_BLOB = "a3ba7e862cac559fcce70d92b935745a662bbdc8"
LEAF_SCHEMA = "sf-cross-platform-git-preflight-leaf-v1"
REPORT_SCHEMA = "sf-cross-platform-git-preflight-v1"
DEFAULT_NT = REPO / "docs/checks/system-first-stage1a/context-v2/git-preflight.nt.json"
DEFAULT_POSIX = (
    REPO / "docs/checks/system-first-stage1a/context-v2/git-preflight.posix.json"
)
DEFAULT_REPORT = (
    REPO / "docs/checks/system-first-stage1a/context-v2/git-anchor-receipt.json"
)


class PreflightError(RuntimeError):
    """Git preflight could not produce trustworthy evidence."""


def _git(*args: str, cwd: Path = REPO, allow_missing: bool = False) -> str | None:
    completed = subprocess.run(
        ["git", *args],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if allow_missing and completed.returncode == 1:
        return None
    if completed.returncode != 0:
        raise PreflightError(
            f"git {' '.join(args)} failed ({completed.returncode}): "
            f"{completed.stderr.strip()}"
        )
    return completed.stdout.strip()


def validate_gitfile_text(text: str) -> list[str]:
    """Require one cross-platform relative gitdir directive."""

    lines = text.splitlines()
    if len(lines) != 1 or not lines[0].startswith("gitdir: "):
        return ["gitfile-shape-invalid"]
    value = lines[0][len("gitdir: ") :]
    if (
        PureWindowsPath(value).is_absolute()
        or PurePosixPath(value).is_absolute()
        or re.match(r"^[A-Za-z]:[/\\]", value)
    ):
        return ["gitfile-gitdir-must-be-relative"]
    if "\\" in value or any(part in ("", ".") for part in PurePosixPath(value).parts):
        return ["gitfile-relative-path-invalid"]
    return []


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def collect_observation(repo: Path = REPO) -> dict:
    platform = "nt" if os.name == "nt" else "posix"
    gitfile = repo / ".git"
    if not gitfile.is_file():
        raise PreflightError(f"linked-worktree gitfile missing: {gitfile}")
    gitfile_failures = validate_gitfile_text(gitfile.read_text(encoding="utf-8"))
    if gitfile_failures:
        raise PreflightError(",".join(gitfile_failures))

    common_dir_raw = _git("rev-parse", "--path-format=absolute", "--git-common-dir", cwd=repo)
    if common_dir_raw is None:
        raise PreflightError("git common directory missing")
    common_dir = Path(common_dir_raw)
    primary = common_dir.parent
    resolved_root = Path(_git("rev-parse", "--show-toplevel", cwd=repo) or "")
    primary_root = Path(_git("rev-parse", "--show-toplevel", cwd=primary) or "")
    head = _git("rev-parse", "HEAD", cwd=repo)
    plan_blob = _git("rev-parse", f"{IMPLEMENTATION_FREEZE}:{PLAN_PATH}", cwd=repo)
    core_worktree = _git(
        "--git-dir", str(common_dir), "config", "--get", "core.worktree",
        cwd=repo,
        allow_missing=True,
    )
    return {
        "schema": LEAF_SCHEMA,
        "platform": platform,
        "implementation_freeze": IMPLEMENTATION_FREEZE,
        "resolved_head": head,
        "plan_blob": plan_blob,
        "primary_root_identity": primary_root.name,
        "worktree_root_identity": resolved_root.name,
        "primary_clean": _git("status", "--porcelain=v1", cwd=primary) == "",
        "worktree_clean": _git("status", "--porcelain=v1", cwd=repo) == "",
        "shared_core_worktree": core_worktree,
        "gitfile_policy": "RELATIVE",
    }


def aggregate_observations(nt: dict, posix: dict) -> dict:
    failures: list[str] = []
    observations = {"nt": nt, "posix": posix}
    for platform, leaf in observations.items():
        if leaf.get("schema") != LEAF_SCHEMA:
            failures.append(f"{platform}-leaf-schema-mismatch")
        if leaf.get("platform") != platform:
            failures.append(f"{platform}-platform-stamp-mismatch")
        if leaf.get("implementation_freeze") != IMPLEMENTATION_FREEZE:
            failures.append(f"{platform}-implementation-freeze-mismatch")
        if leaf.get("primary_root_identity") != "exploring-l4-intelligence":
            failures.append(f"{platform}-primary-root-mismatch")
        if leaf.get("worktree_root_identity") != "stage1b-readiness-remediation":
            failures.append(f"{platform}-worktree-root-mismatch")
        if leaf.get("primary_clean") is not True:
            failures.append(f"{platform}-primary-dirty")
        if leaf.get("worktree_clean") is not True:
            failures.append(f"{platform}-worktree-dirty")
        if leaf.get("shared_core_worktree") is not None:
            failures.append(f"{platform}-shared-core-worktree-present")
        if leaf.get("gitfile_policy") != "RELATIVE":
            failures.append(f"{platform}-gitfile-policy-mismatch")
    if nt.get("resolved_head") != posix.get("resolved_head"):
        failures.append("platform-head-mismatch")
    if nt.get("plan_blob") != posix.get("plan_blob"):
        failures.append("platform-plan-blob-mismatch")
    if nt.get("plan_blob") != IMPLEMENTATION_PLAN_BLOB:
        failures.append("implementation-plan-blob-mismatch")
    return {
        "schema": REPORT_SCHEMA,
        "verdict": "PASS" if not failures else "FAIL",
        "failures": failures,
        "anchors": {
            "evidence_v6_release_anchor": EVIDENCE_V6_RELEASE_ANCHOR,
            "plan_review_anchor": PLAN_REVIEW_ANCHOR,
            "implementation_freeze": IMPLEMENTATION_FREEZE,
            "pre_merge_master": None,
            "merge_head": None,
        },
        "observations": observations,
    }


def _render(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def write_leaf(path: Path) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(_render(collect_observation()))
    print(f"git preflight leaf: wrote {path}")
    return 0


def build_report(nt_path: Path, posix_path: Path) -> dict:
    nt_raw = nt_path.read_bytes()
    posix_raw = posix_path.read_bytes()
    nt = json.loads(nt_raw)
    posix = json.loads(posix_raw)
    report = aggregate_observations(nt, posix)
    report["leaf_sha256"] = {"nt": _sha256(nt_raw), "posix": _sha256(posix_raw)}
    return report


def aggregate(nt_path: Path, posix_path: Path, output: Path, write: bool) -> int:
    report = build_report(nt_path, posix_path)
    expected = _render(report)
    if report["verdict"] != "PASS":
        print("git preflight aggregate: FAIL " + ",".join(report["failures"]))
        return 1
    if write:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(expected)
    elif not output.is_file() or output.read_bytes() != expected:
        print("git preflight aggregate: FAIL stale-or-missing-report")
        return 1
    print("git preflight aggregate: PASS")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--leaf", action="store_true")
    modes.add_argument("--write", action="store_true")
    modes.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--nt", type=Path, default=DEFAULT_NT)
    parser.add_argument("--posix", type=Path, default=DEFAULT_POSIX)
    args = parser.parse_args(argv)
    try:
        if args.leaf:
            if args.output is None:
                parser.error("--leaf requires --output")
            return write_leaf(args.output)
        return aggregate(args.nt, args.posix, args.output or DEFAULT_REPORT, args.write)
    except (OSError, ValueError, json.JSONDecodeError, PreflightError) as error:
        print(f"git preflight: FAIL {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
