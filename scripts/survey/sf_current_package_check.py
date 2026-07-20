#!/usr/bin/env python3
"""Run the deterministic, offline gate for the consolidated Stage-1A package.

The default and explicit ``--check`` modes are zero-write: they execute the
fixed local checks, rebuild the expected report in memory, and require the
stage-0 report blob, trusted worktree bytes, and expected bytes to be equal.
Only explicit ``--write`` may atomically replace the fixed report path.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import stat
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Callable, NamedTuple, Sequence


REPO = Path(__file__).resolve().parents[2]
CHECKS_DIR = REPO / "scripts" / "checks"
if str(CHECKS_DIR) not in sys.path:
    sys.path.insert(0, str(CHECKS_DIR))

from ai_context_surface_check import git_command_prefix  # noqa: E402
from sf_current_path_contract import (  # noqa: E402
    TrustedCurrentPathError,
    read_fixed_bytes,
    resolve_fixed_output,
)
from sf_query_compiler import atomic_write_bytes  # noqa: E402


REPORT_RELATIVE = (
    "docs/checks/system-first-stage1a/context-v1/current-package-check.json"
)
REGULAR_MODES = {"100644", "100755"}
TAIL_LINES = 40
TAIL_CHARACTERS = 4096

COMMANDS = (
    "python scripts/survey/test_sf_evidence_contract.py",
    "python scripts/survey/sf_schema_v3_migrate.py --check",
    "python scripts/survey/sf_coding_generator.py --check",
    "python scripts/survey/sf_identity_taxonomy_v6_test.py",
    "python scripts/survey/sf_dual_platform_check.py",
    "python scripts/survey/test_sf_query_compiler_profiles.py",
    "python scripts/survey/sf_query_compiler.py --check --check-against wiki/survey/2026-07-15-sf-queries.jsonl",
    "python scripts/survey/sf_current_tables.py --check",
    "python scripts/survey/sf_current_manifest.py --check",
    "python scripts/survey/sf_release_binding_check.py",
    "python scripts/survey/sf_quantifier_scan.py",
    "python scripts/survey/sf_archive_candidates.py --check-applied",
    "python scripts/survey/sf_audit_immutability_check.py --check",
    "python scripts/checks/build_ai_context_manifest.py --check",
    "python scripts/checks/ai_context_surface_check.py",
)
STAGED_SANDBOX_COMMANDS = {COMMANDS[3]}


class CurrentPackageError(RuntimeError):
    """The report transaction or command contract is unsafe or malformed."""


class CommandExecution(NamedTuple):
    exit_code: int
    stdout: str
    stderr: str


CommandRunner = Callable[[str, Path], CommandExecution]


def _execute_python_command(command: str, cwd: Path) -> CommandExecution:
    tokens = shlex.split(command, posix=True)
    if not tokens or tokens[0] != "python":
        raise CurrentPackageError(f"unsupported package-check command: {command!r}")
    environment = os.environ.copy()
    environment.update(
        {
            "PYTHONIOENCODING": "utf-8",
            "PYTHONUTF8": "1",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    try:
        completed = subprocess.run(
            [sys.executable, *tokens[1:]],
            cwd=cwd,
            env=environment,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except OSError as error:
        return CommandExecution(127, "", f"subprocess launch failed: {error}\n")
    return CommandExecution(completed.returncode, completed.stdout, completed.stderr)


def _replace_sandbox_path(value: str, sandbox: Path, repo: Path) -> str:
    result = value
    variants = sorted(
        {str(sandbox), sandbox.as_posix()}, key=len, reverse=True
    )
    for variant in variants:
        result = re.sub(
            re.escape(variant), lambda _match: str(repo), result, flags=re.IGNORECASE
        )
    return result


def _default_command_runner(command: str, repo: Path) -> CommandExecution:
    """Execute one fixed command; isolate its one legacy writing harness."""

    if command not in STAGED_SANDBOX_COMMANDS:
        return _execute_python_command(command, repo)

    with tempfile.TemporaryDirectory(prefix="sf-current-package-") as temporary:
        sandbox = Path(temporary) / "stage0"
        sandbox.mkdir()
        prefix = sandbox.as_posix().rstrip("/") + "/"
        _git(repo, "checkout-index", "--all", "--force", f"--prefix={prefix}")
        execution = _execute_python_command(command, sandbox)
        return CommandExecution(
            execution.exit_code,
            _replace_sandbox_path(execution.stdout, sandbox, repo),
            _replace_sandbox_path(execution.stderr, sandbox, repo),
        )


def _normalized_tail(value: str, repo: Path) -> str:
    """Return a bounded, stable tail without timing or repository absolutes."""

    text = value.replace("\r\n", "\n").replace("\r", "\n")
    try:
        resolved = repo.resolve(strict=True)
    except OSError:
        resolved = repo.absolute()
    variants = sorted(
        {
            str(repo.absolute()),
            repo.absolute().as_posix(),
            str(resolved),
            resolved.as_posix(),
        },
        key=len,
        reverse=True,
    )
    for variant in variants:
        if variant:
            text = re.sub(re.escape(variant), "<REPO>", text, flags=re.IGNORECASE)
    text = re.sub(
        r"(Ran\s+\d+\s+tests?)\s+in\s+\d+(?:\.\d+)?s\b",
        r"\1",
        text,
    )
    lines = text.splitlines()[-TAIL_LINES:]
    tail = "\n".join(lines)
    if len(tail) > TAIL_CHARACTERS:
        tail = tail[-TAIL_CHARACTERS:]
    return tail


def build_report(
    repo: Path,
    *,
    commands: Sequence[str] = COMMANDS,
    command_runner: CommandRunner = _default_command_runner,
) -> tuple[bytes, dict]:
    """Execute all commands in order and render one deterministic result row each."""

    rows = []
    for command in commands:
        execution = command_runner(command, repo)
        if isinstance(execution.exit_code, bool) or not isinstance(
            execution.exit_code, int
        ):
            raise CurrentPackageError(
                f"command runner returned an invalid exit code for {command!r}"
            )
        rows.append(
            {
                "command": command,
                "exit_code": execution.exit_code,
                "stdout_tail": _normalized_tail(execution.stdout, repo),
                "stderr_tail": _normalized_tail(execution.stderr, repo),
            }
        )
    verdict = "PASS" if all(row["exit_code"] == 0 for row in rows) else "FAIL"
    report = {
        "schema": "sf-current-package-check-v1",
        "check": "sf-current-package",
        "commands": rows,
        "verdict": verdict,
    }
    raw = (json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    return raw, report


def _git(repo: Path, *arguments: str) -> bytes:
    try:
        completed = subprocess.run(
            [*git_command_prefix(repo), *arguments],
            cwd=repo,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as error:
        raise CurrentPackageError(f"git {' '.join(arguments)} failed: {error}") from error
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise CurrentPackageError(f"git {' '.join(arguments)} failed: {detail}")
    return completed.stdout


def _git_entry(repo: Path, source: str) -> tuple[str, str] | None:
    if source == "stage0":
        raw = _git(repo, "ls-files", "-s", "-z", "--", REPORT_RELATIVE)
        records = [record for record in raw.split(b"\0") if record]
        if not records:
            return None
        if len(records) != 1:
            raise CurrentPackageError("report has multiple Git index entries")
        try:
            metadata, raw_path = records[0].split(b"\t", 1)
            mode, blob, stage = metadata.decode("ascii").split(" ")
            path = raw_path.decode("utf-8")
        except (UnicodeDecodeError, ValueError) as error:
            raise CurrentPackageError(f"malformed report stage-0 entry: {error}") from error
        if stage != "0" or path != REPORT_RELATIVE:
            raise CurrentPackageError("report does not have one canonical stage-0 entry")
        return mode, blob

    if source != "HEAD":
        raise ValueError(f"unsupported Git source: {source}")
    raw = _git(repo, "ls-tree", "-z", "HEAD", "--", REPORT_RELATIVE)
    records = [record for record in raw.split(b"\0") if record]
    if not records:
        return None
    if len(records) != 1:
        raise CurrentPackageError("report has multiple HEAD entries")
    try:
        metadata, raw_path = records[0].split(b"\t", 1)
        mode, kind, blob = metadata.decode("ascii").split(" ")
        path = raw_path.decode("utf-8")
    except (UnicodeDecodeError, ValueError) as error:
        raise CurrentPackageError(f"malformed report HEAD entry: {error}") from error
    if kind != "blob" or path != REPORT_RELATIVE:
        raise CurrentPackageError("report does not have one canonical HEAD blob")
    return mode, blob


def _regular_entry(entry: tuple[str, str] | None, label: str) -> tuple[str, str]:
    if entry is None:
        raise CurrentPackageError(f"{label} is missing")
    mode, blob = entry
    if mode not in REGULAR_MODES or re.fullmatch(r"[0-9a-f]{40}", blob) is None:
        raise CurrentPackageError(f"{label} is not a regular Git blob")
    return mode, blob


def _blob_bytes(repo: Path, blob: str) -> bytes:
    return _git(repo, "cat-file", "blob", blob)


def _write_preflight(repo: Path) -> Path:
    target = repo.joinpath(*REPORT_RELATIVE.split("/"))
    try:
        metadata = os.lstat(target)
    except FileNotFoundError:
        if _git_entry(repo, "stage0") is not None or _git_entry(repo, "HEAD") is not None:
            raise CurrentPackageError("tracked report is missing from the worktree")
        return resolve_fixed_output(
            repo, target, REPORT_RELATIVE, allow_missing_leaf=True
        )
    except OSError as error:
        raise CurrentPackageError(f"report path unavailable: {error}") from error

    reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    attributes = getattr(metadata, "st_file_attributes", 0)
    if stat.S_ISLNK(metadata.st_mode) or bool(attributes & reparse):
        raise CurrentPackageError("report path is a symlink or reparse point")
    output = resolve_fixed_output(repo, target, REPORT_RELATIVE, allow_missing_leaf=False)
    staged = _regular_entry(_git_entry(repo, "stage0"), "stage-0 report")
    head = _regular_entry(_git_entry(repo, "HEAD"), "HEAD report")
    if staged != head:
        raise CurrentPackageError("report has an uncommitted stage-0 change")
    staged_raw = _blob_bytes(repo, staged[1])
    if read_fixed_bytes(repo, output, REPORT_RELATIVE) != staged_raw:
        raise CurrentPackageError("report worktree bytes differ from clean stage-0 report")
    return output


def _check_report(repo: Path, expected: bytes) -> None:
    target = repo.joinpath(*REPORT_RELATIVE.split("/"))
    output = resolve_fixed_output(repo, target, REPORT_RELATIVE, allow_missing_leaf=False)
    _mode, blob = _regular_entry(_git_entry(repo, "stage0"), "stage-0 report")
    staged_raw = _blob_bytes(repo, blob)
    worktree_raw = read_fixed_bytes(repo, output, REPORT_RELATIVE)
    if staged_raw != expected:
        raise CurrentPackageError("tracked stage-0 report is stale")
    if worktree_raw != staged_raw:
        raise CurrentPackageError("report worktree bytes differ from tracked stage-0 report")


def run(
    mode: str,
    *,
    repo: Path = REPO,
    commands: Sequence[str] = COMMANDS,
    command_runner: CommandRunner = _default_command_runner,
) -> int:
    """Run explicit write or strict zero-write check mode."""

    if mode not in {"write", "check"}:
        raise ValueError(f"unsupported mode: {mode}")
    try:
        output = _write_preflight(repo) if mode == "write" else None
        expected, report = build_report(
            repo, commands=commands, command_runner=command_runner
        )
        if mode == "write":
            assert output is not None
            atomic_write_bytes(output, expected)
            if read_fixed_bytes(repo, output, REPORT_RELATIVE) != expected:
                raise CurrentPackageError("written report failed byte verification")
        else:
            _check_report(repo, expected)
    except (CurrentPackageError, TrustedCurrentPathError, OSError, ValueError) as error:
        print(f"[CURRENT-PACKAGE] {error}")
        print("current package: FAIL")
        return 1

    failed = [row for row in report["commands"] if row["exit_code"] != 0]
    for row in failed:
        print(f"[CURRENT-PACKAGE] exit {row['exit_code']}: {row['command']}")
    print(f"current package: {report['verdict']}")
    return 0 if report["verdict"] == "PASS" else 1


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--write", action="store_true", help="write the fixed report")
    modes.add_argument(
        "--check", action="store_true", help="zero-write staged check (default)"
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    mode = "write" if arguments.write else "check"
    return run(mode)


if __name__ == "__main__":
    sys.exit(main())
