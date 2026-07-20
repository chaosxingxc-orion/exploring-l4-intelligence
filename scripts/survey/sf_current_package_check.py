#!/usr/bin/env python3
"""Run the deterministic, offline gate for the consolidated Stage-1A package.

The default and explicit ``--check`` modes are zero-write: they execute the
fixed local checks, rebuild the expected report in memory, and require the
stage-0 report blob, trusted worktree bytes, and expected bytes to be equal.
Only explicit ``--write`` may atomically replace the fixed report path.
"""

from __future__ import annotations

import sys

# When invoked as ``python scripts/survey/...``, prevent that directory from
# shadowing the standard library before the trusted code graph is checked.
_INITIAL_IMPORT_PATH = sys.path[0].replace("\\", "/").rstrip("/") if sys.path else ""
if _INITIAL_IMPORT_PATH.endswith("/scripts/survey"):
    del sys.path[0]
sys.dont_write_bytecode = True

import argparse
import hashlib
import json
import os
import re
import shlex
import stat
import subprocess
import tempfile
from pathlib import Path, PurePosixPath
from typing import Callable, NamedTuple, Sequence


REPO = Path(__file__).resolve().parents[2]
REPORT_RELATIVE = (
    "docs/checks/system-first-stage1a/context-v1/current-package-check.json"
)
REGULAR_MODES = {"100644", "100755"}
REPORT_GIT_MODE = "100644"
REPORT_POSIX_MODE = 0o644
CODE_ROOTS = ("scripts/survey", "scripts/checks")
CODE_GRAPH_EXTRA_PATHS = ("scripts/wiki-sync.sh",)
LOADABLE_CODE_SUFFIXES = (".py", ".pyw", ".pyi", ".pyd", ".so", ".pyc")
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


class GitEntry(NamedTuple):
    mode: str
    blob: str


CommandRunner = Callable[[str, Path], CommandExecution]


def _execute_python_command(command: str, cwd: Path) -> CommandExecution:
    tokens = shlex.split(command, posix=True)
    if not tokens or tokens[0] != "python":
        raise CurrentPackageError(f"unsupported package-check command: {command!r}")
    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    environment.update(
        {
            "PYTHONIOENCODING": "utf-8",
            "PYTHONUTF8": "1",
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONNOUSERSITE": "1",
        }
    )
    try:
        with tempfile.TemporaryDirectory(prefix="sf-package-pycache-") as pycache:
            environment["PYTHONPYCACHEPREFIX"] = pycache
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
        r'("platform"\s*:\s*\{\s*"os"\s*:\s*)"(?:nt|posix)"'
        r'(\s*,\s*"python"\s*:\s*)"[^"\r\n]+"(\s*\})',
        lambda match: (
            f'{match.group(1)}"<OS>"{match.group(2)}'
            f'"<PYTHON>"{match.group(3)}'
        ),
        text,
    )
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
    code_graph: dict,
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
        "code_graph": code_graph,
        "commands": rows,
        "verdict": verdict,
    }
    raw = (json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    return raw, report


def _is_link_or_reparse(metadata: os.stat_result) -> bool:
    reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    attributes = getattr(metadata, "st_file_attributes", 0)
    return stat.S_ISLNK(metadata.st_mode) or bool(attributes & reparse)


def _canonical_path(value: str, label: str) -> str:
    path = PurePosixPath(value)
    if (
        not value
        or "\\" in value
        or path.is_absolute()
        or value != path.as_posix()
        or any(part in ("", ".", "..") for part in path.parts)
    ):
        raise CurrentPackageError(f"{label} is not a canonical repository path: {value!r}")
    return value


def _trusted_path(
    repo: Path,
    relative: str,
    *,
    expected_kind: str,
    allow_missing_leaf: bool = False,
) -> Path:
    relative = _canonical_path(relative, "trusted path")
    root = Path(os.path.abspath(repo))
    try:
        root_metadata = os.lstat(root)
    except OSError as error:
        raise CurrentPackageError(f"repository root unavailable: {error}") from error
    if _is_link_or_reparse(root_metadata) or not stat.S_ISDIR(root_metadata.st_mode):
        raise CurrentPackageError("repository root is not a trusted directory")
    try:
        root_resolved = root.resolve(strict=True)
    except OSError as error:
        raise CurrentPackageError(f"repository root does not resolve: {error}") from error

    current = root
    parts = PurePosixPath(relative).parts
    for index, part in enumerate(parts):
        current /= part
        final = index == len(parts) - 1
        try:
            metadata = os.lstat(current)
        except FileNotFoundError:
            if final and allow_missing_leaf:
                return current
            raise CurrentPackageError(f"trusted path is missing: {relative}")
        except OSError as error:
            raise CurrentPackageError(f"trusted path unavailable: {relative}: {error}") from error
        if _is_link_or_reparse(metadata):
            raise CurrentPackageError(f"trusted path contains symlink/reparse point: {relative}")
        if final:
            expected = stat.S_ISREG if expected_kind == "file" else stat.S_ISDIR
            if not expected(metadata.st_mode):
                raise CurrentPackageError(
                    f"trusted path is not a regular {expected_kind}: {relative}"
                )
        elif not stat.S_ISDIR(metadata.st_mode):
            raise CurrentPackageError(f"trusted path ancestor is not a directory: {relative}")
        try:
            current.resolve(strict=True).relative_to(root_resolved)
        except (OSError, ValueError) as error:
            raise CurrentPackageError(f"trusted path escapes repository: {relative}") from error
    return current


def _trusted_bytes(repo: Path, relative: str) -> bytes:
    path = _trusted_path(repo, relative, expected_kind="file")
    before = os.lstat(path)
    with path.open("rb") as handle:
        opened = os.fstat(handle.fileno())
        if not stat.S_ISREG(opened.st_mode):
            raise CurrentPackageError(f"trusted path changed kind while opening: {relative}")
        raw = handle.read()
    after = os.lstat(path)
    identity_before = (before.st_dev, before.st_ino, before.st_size)
    identity_opened = (opened.st_dev, opened.st_ino, opened.st_size)
    identity_after = (after.st_dev, after.st_ino, after.st_size)
    if identity_before != identity_opened or identity_opened != identity_after:
        raise CurrentPackageError(f"trusted path changed while reading: {relative}")
    if _is_link_or_reparse(after):
        raise CurrentPackageError(f"trusted path became a link while reading: {relative}")
    return raw


def _resolved_gitdir(dot_git: Path) -> Path:
    try:
        pointer = dot_git.read_text(encoding="utf-8").strip()
    except OSError as error:
        raise CurrentPackageError(f"cannot read worktree git pointer: {error}") from error
    if not pointer.startswith("gitdir: ") or "\n" in pointer or "\r" in pointer:
        raise CurrentPackageError("malformed worktree git pointer")
    raw = pointer[len("gitdir: ") :]
    windows = re.fullmatch(r"([A-Za-z]):[\\/](.*)", raw)
    if windows and os.name == "posix":
        drive, remainder = windows.groups()
        return Path(f"/mnt/{drive.lower()}/{remainder.replace('\\', '/')}")
    candidate = Path(raw)
    return candidate if candidate.is_absolute() else dot_git.parent / candidate


def _git_command_prefix(repo: Path) -> list[str]:
    command = ["git"]
    dot_git = repo / ".git"
    if dot_git.is_file():
        command.extend(
            [f"--git-dir={_resolved_gitdir(dot_git)}", f"--work-tree={repo}"]
        )
    return command


def _git(repo: Path, *arguments: str) -> bytes:
    try:
        completed = subprocess.run(
            [*_git_command_prefix(repo), *arguments],
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


def _git_inventory(repo: Path, source: str) -> dict[str, GitEntry]:
    if source == "stage0":
        raw = _git(repo, "ls-files", "-s", "-z", "--")
    elif source == "HEAD":
        raw = _git(repo, "ls-tree", "-r", "-z", "HEAD", "--")
    else:
        raise ValueError(f"unsupported Git source: {source}")
    inventory: dict[str, GitEntry] = {}
    try:
        for record in (item for item in raw.split(b"\0") if item):
            metadata, raw_path = record.split(b"\t", 1)
            fields = metadata.decode("ascii").split(" ")
            path = _canonical_path(raw_path.decode("utf-8"), f"{source} path")
            if source == "stage0":
                mode, blob, stage = fields
                if stage != "0":
                    raise CurrentPackageError(f"non-stage-0 Git entry: {path}")
            else:
                mode, kind, blob = fields
                if kind != "blob":
                    continue
            if path in inventory or re.fullmatch(r"[0-9a-f]{40}", blob) is None:
                raise CurrentPackageError(f"malformed or duplicate {source} entry: {path}")
            inventory[path] = GitEntry(mode, blob)
    except CurrentPackageError:
        raise
    except (UnicodeDecodeError, ValueError) as error:
        raise CurrentPackageError(f"malformed {source} Git inventory: {error}") from error
    return inventory


def _git_entry(repo: Path, source: str) -> GitEntry | None:
    return _git_inventory(repo, source).get(REPORT_RELATIVE)


def _regular_entry(entry: GitEntry | None, label: str) -> GitEntry:
    if entry is None:
        raise CurrentPackageError(f"{label} is missing")
    mode, blob = entry
    if mode not in REGULAR_MODES or re.fullmatch(r"[0-9a-f]{40}", blob) is None:
        raise CurrentPackageError(f"{label} is not a regular Git blob")
    return GitEntry(mode, blob)


def _report_entry(entry: GitEntry | None, label: str) -> GitEntry:
    regular = _regular_entry(entry, label)
    if regular.mode != REPORT_GIT_MODE:
        raise CurrentPackageError(
            f"{label} must have Git mode {REPORT_GIT_MODE}, found {regular.mode}"
        )
    return regular


def _blob_bytes(repo: Path, blob: str) -> bytes:
    return _git(repo, "cat-file", "blob", blob)


def _is_graph_path(path: str) -> bool:
    return path in CODE_GRAPH_EXTRA_PATHS or any(
        path.startswith(f"{root}/") for root in CODE_ROOTS
    )


def _scan_for_untracked_code(repo: Path, tracked_graph_paths: set[str]) -> None:
    for root_relative in CODE_ROOTS:
        root = _trusted_path(repo, root_relative, expected_kind="directory")
        pending = [(root, root_relative)]
        while pending:
            directory, directory_relative = pending.pop()
            try:
                entries = sorted(os.scandir(directory), key=lambda item: item.name)
            except OSError as error:
                raise CurrentPackageError(
                    f"cannot scan trusted code directory {directory_relative}: {error}"
                ) from error
            for entry in entries:
                relative = f"{directory_relative}/{entry.name}"
                metadata = entry.stat(follow_symlinks=False)
                if _is_link_or_reparse(metadata):
                    raise CurrentPackageError(f"code graph contains symlink/reparse: {relative}")
                if stat.S_ISDIR(metadata.st_mode):
                    if entry.name != "__pycache__":
                        pending.append((Path(entry.path), relative))
                    continue
                if not stat.S_ISREG(metadata.st_mode):
                    raise CurrentPackageError(f"code graph contains special file: {relative}")
                if relative.lower().endswith(LOADABLE_CODE_SUFFIXES):
                    if relative not in tracked_graph_paths:
                        raise CurrentPackageError(f"untracked local code is forbidden: {relative}")


def _trusted_code_graph(
    repo: Path, mode: str, commands: Sequence[str]
) -> dict:
    stage = _git_inventory(repo, "stage0")
    head = _git_inventory(repo, "HEAD")
    missing_extras = sorted(set(CODE_GRAPH_EXTRA_PATHS) - set(stage))
    if missing_extras:
        raise CurrentPackageError(
            f"required shell helper missing from stage0: {missing_extras}"
        )
    stage_paths = sorted(path for path in stage if _is_graph_path(path))
    head_paths = sorted(path for path in head if _is_graph_path(path))
    if not stage_paths:
        raise CurrentPackageError("trusted code graph is empty")
    if mode == "check" and stage_paths != head_paths:
        raise CurrentPackageError("trusted code graph path set differs between HEAD and stage0")

    nodes = []
    for path in stage_paths:
        entry = _regular_entry(stage[path], f"stage-0 code node {path}")
        worktree_raw = _trusted_bytes(repo, path)
        staged_raw = _blob_bytes(repo, entry.blob)
        if worktree_raw != staged_raw:
            raise CurrentPackageError(f"code node stage0/worktree mismatch: {path}")
        if mode == "check" and head.get(path) != entry:
            raise CurrentPackageError(f"code node HEAD/stage0 mismatch: {path}")
        nodes.append({"path": path, "mode": entry.mode, "git_blob": entry.blob})

    graph_paths = set(stage_paths)
    _scan_for_untracked_code(repo, graph_paths)
    for command in commands:
        tokens = shlex.split(command, posix=True)
        if len(tokens) < 2 or tokens[0] != "python":
            raise CurrentPackageError(f"unsupported direct command: {command!r}")
        direct = _canonical_path(tokens[1], "direct command script")
        if direct not in graph_paths:
            raise CurrentPackageError(f"direct command is outside trusted code graph: {direct}")

    canonical = json.dumps(
        nodes, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return {
        "policy": "stage0 regular graph; stage0=worktree; check additionally HEAD=stage0",
        "roots": [*CODE_ROOTS, *CODE_GRAPH_EXTRA_PATHS],
        "nodes": nodes,
        "sha256": hashlib.sha256(canonical).hexdigest(),
    }


def _mountinfo_unescape(value: str) -> str:
    return re.sub(
        r"\\([0-7]{3})",
        lambda match: chr(int(match.group(1), 8)),
        value,
    )


def _mountinfo_exposes_posix_mode(path: str, mountinfo: str) -> bool:
    """Return false only for a matched DrvFS mount without metadata support."""

    matches: list[tuple[int, list[str], list[str]]] = []
    for line in mountinfo.splitlines():
        fields = line.split()
        try:
            separator = fields.index("-")
        except ValueError:
            continue
        if separator < 6 or len(fields) <= separator + 3:
            continue
        mountpoint = _mountinfo_unescape(fields[4]).rstrip("/") or "/"
        within = path == mountpoint or (
            mountpoint == "/" or path.startswith(mountpoint + "/")
        )
        if within:
            matches.append((len(mountpoint), fields[:separator], fields[separator + 1 :]))
    if not matches:
        return True

    _length, left, right = max(matches, key=lambda item: item[0])
    filesystem = right[0]
    mount_options = set(left[5].split(","))
    super_options = set(right[2].split(","))
    drvfs = filesystem == "9p" and any(
        option == "aname=drvfs" or option.startswith("aname=drvfs;")
        for option in super_options
    )
    metadata = "metadata" in mount_options or "metadata" in super_options
    return not (drvfs and not metadata)


def _filesystem_exposes_posix_mode(path: Path) -> bool:
    if os.name != "posix":
        return False
    try:
        mountinfo = Path("/proc/self/mountinfo").read_text(encoding="utf-8")
    except OSError:
        # Unknown POSIX filesystems remain strict. Only a positively identified
        # mode-incapable DrvFS mount receives the Git-mode fallback.
        return True
    return _mountinfo_exposes_posix_mode(path.resolve().as_posix(), mountinfo)


def _verify_posix_report_mode(path: Path) -> None:
    if os.name == "posix" and _filesystem_exposes_posix_mode(path):
        mode = stat.S_IMODE(os.lstat(path).st_mode)
        if mode != REPORT_POSIX_MODE:
            raise CurrentPackageError(
                f"report POSIX mode must be 0644, found {mode:04o}"
            )


def _write_preflight(repo: Path) -> Path:
    target = repo.joinpath(*REPORT_RELATIVE.split("/"))
    try:
        metadata = os.lstat(target)
    except FileNotFoundError:
        if _git_entry(repo, "stage0") is not None or _git_entry(repo, "HEAD") is not None:
            raise CurrentPackageError("tracked report is missing from the worktree")
        return _trusted_path(
            repo, REPORT_RELATIVE, expected_kind="file", allow_missing_leaf=True
        )
    except OSError as error:
        raise CurrentPackageError(f"report path unavailable: {error}") from error

    if _is_link_or_reparse(metadata):
        raise CurrentPackageError("report path is a symlink or reparse point")
    output = _trusted_path(repo, REPORT_RELATIVE, expected_kind="file")
    staged = _report_entry(_git_entry(repo, "stage0"), "stage-0 report")
    head = _report_entry(_git_entry(repo, "HEAD"), "HEAD report")
    if staged != head:
        raise CurrentPackageError("report has an uncommitted stage-0 change")
    staged_raw = _blob_bytes(repo, staged.blob)
    if _trusted_bytes(repo, REPORT_RELATIVE) != staged_raw:
        raise CurrentPackageError("report worktree bytes differ from clean stage-0 report")
    return output


def _check_report_preflight(repo: Path) -> bytes:
    output = _trusted_path(repo, REPORT_RELATIVE, expected_kind="file")
    entry = _report_entry(_git_entry(repo, "stage0"), "stage-0 report")
    staged_raw = _blob_bytes(repo, entry.blob)
    worktree_raw = _trusted_bytes(repo, REPORT_RELATIVE)
    if worktree_raw != staged_raw:
        raise CurrentPackageError("report worktree bytes differ from tracked stage-0 report")
    _verify_posix_report_mode(output)
    return staged_raw


def _check_report(expected: bytes, staged_raw: bytes) -> None:
    if staged_raw != expected:
        raise CurrentPackageError("tracked stage-0 report is stale")


def _fsync_parent(path: Path) -> None:
    if os.name != "posix":
        return
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _atomic_write_report(repo: Path, output: Path, payload: bytes) -> None:
    old_exists = output.exists()
    old_bytes = output.read_bytes() if old_exists else None
    old_mode = stat.S_IMODE(output.stat().st_mode) if old_exists else None
    temporary: Path | None = None
    backup: Path | None = None
    published = False
    try:
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{output.name}.", suffix=".tmp", dir=output.parent
        )
        temporary = Path(temporary_name)
        with os.fdopen(descriptor, "wb") as handle:
            if os.name == "posix":
                os.fchmod(handle.fileno(), REPORT_POSIX_MODE)
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        if temporary.read_bytes() != payload:
            raise CurrentPackageError("staged report bytes failed verification")
        _verify_posix_report_mode(temporary)

        if old_exists:
            backup_descriptor, backup_name = tempfile.mkstemp(
                prefix=f".{output.name}.", suffix=".bak", dir=output.parent
            )
            backup = Path(backup_name)
            with os.fdopen(backup_descriptor, "wb") as handle:
                assert old_bytes is not None and old_mode is not None
                if os.name == "posix":
                    os.fchmod(handle.fileno(), old_mode)
                handle.write(old_bytes)
                handle.flush()
                os.fsync(handle.fileno())
            _fsync_parent(output.parent)

        os.replace(temporary, output)
        temporary = None
        published = True
        _fsync_parent(output.parent)
        if _trusted_bytes(repo, REPORT_RELATIVE) != payload:
            raise CurrentPackageError("published report bytes failed verification")
        _verify_posix_report_mode(output)
    except BaseException:
        if published:
            try:
                if backup is not None:
                    os.replace(backup, output)
                    backup = None
                else:
                    output.unlink(missing_ok=True)
                _fsync_parent(output.parent)
            except OSError as rollback_error:
                raise CurrentPackageError(
                    f"report publish rollback failed: {rollback_error}"
                )
        raise
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
        if backup is not None:
            backup.unlink(missing_ok=True)


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
        code_graph = _trusted_code_graph(repo, mode, commands)
        output = _write_preflight(repo) if mode == "write" else None
        staged_report = _check_report_preflight(repo) if mode == "check" else None
        expected, report = build_report(
            repo,
            code_graph=code_graph,
            commands=commands,
            command_runner=command_runner,
        )
        if mode == "write":
            assert output is not None
            _atomic_write_report(repo, output, expected)
        else:
            assert staged_report is not None
            _check_report(expected, staged_report)
    except (CurrentPackageError, OSError, ValueError) as error:
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
