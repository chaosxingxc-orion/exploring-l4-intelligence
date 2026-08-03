#!/usr/bin/env python3
"""Fail-closed trusted code-graph gate.

Carries forward the cross-cutting protections of the retired Stage-1
sf_current_package_check (2026-08-03): every loadable code file under the
code roots must be identical across HEAD, stage-0 and the worktree; no
untracked loadable code may shadow tracked modules; no symlink/reparse
point may sit anywhere on a trusted path.
"""

from __future__ import annotations

import argparse
import os
import re
import stat
import subprocess
from pathlib import Path, PurePosixPath
from typing import NamedTuple


REPO = Path(__file__).resolve().parents[2]
CODE_ROOTS = ("scripts/survey", "scripts/checks")
CODE_GRAPH_EXTRA_PATHS = ("scripts/wiki-sync.sh",)
LOADABLE_CODE_SUFFIXES = (".py", ".pyw", ".pyi", ".pyd", ".so", ".pyc")


class CodeGraphError(RuntimeError):
    """The trusted code graph is inconsistent or compromised."""


class GitEntry(NamedTuple):
    mode: str
    blob: str


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
        raise CodeGraphError(f"{label} is not a canonical repository path: {value!r}")
    return value


def _trusted_path(repo: Path, relative: str, *, expected_kind: str) -> Path:
    relative = _canonical_path(relative, "trusted path")
    root = Path(os.path.abspath(repo))
    try:
        root_metadata = os.lstat(root)
    except OSError as error:
        raise CodeGraphError(f"repository root unavailable: {error}") from error
    if _is_link_or_reparse(root_metadata) or not stat.S_ISDIR(root_metadata.st_mode):
        raise CodeGraphError("repository root is not a trusted directory")
    try:
        root_resolved = root.resolve(strict=True)
    except OSError as error:
        raise CodeGraphError(f"repository root does not resolve: {error}") from error

    current = root
    parts = PurePosixPath(relative).parts
    for index, part in enumerate(parts):
        current /= part
        final = index == len(parts) - 1
        try:
            metadata = os.lstat(current)
        except FileNotFoundError:
            raise CodeGraphError(f"trusted path is missing: {relative}")
        except OSError as error:
            raise CodeGraphError(f"trusted path unavailable: {relative}: {error}") from error
        if _is_link_or_reparse(metadata):
            raise CodeGraphError(f"trusted path contains symlink/reparse point: {relative}")
        if final:
            expected = stat.S_ISREG if expected_kind == "file" else stat.S_ISDIR
            if not expected(metadata.st_mode):
                raise CodeGraphError(
                    f"trusted path is not a regular {expected_kind}: {relative}"
                )
        elif not stat.S_ISDIR(metadata.st_mode):
            raise CodeGraphError(f"trusted path ancestor is not a directory: {relative}")
        try:
            current.resolve(strict=True).relative_to(root_resolved)
        except (OSError, ValueError) as error:
            raise CodeGraphError(f"trusted path escapes repository: {relative}") from error
    return current


def _trusted_bytes(repo: Path, relative: str) -> bytes:
    path = _trusted_path(repo, relative, expected_kind="file")
    before = os.lstat(path)
    with path.open("rb") as handle:
        opened = os.fstat(handle.fileno())
        if not stat.S_ISREG(opened.st_mode):
            raise CodeGraphError(f"trusted path changed kind while opening: {relative}")
        raw = handle.read()
    after = os.lstat(path)
    identity_before = (before.st_dev, before.st_ino, before.st_size)
    identity_opened = (opened.st_dev, opened.st_ino, opened.st_size)
    identity_after = (after.st_dev, after.st_ino, after.st_size)
    if identity_before != identity_opened or identity_opened != identity_after:
        raise CodeGraphError(f"trusted path changed while reading: {relative}")
    if _is_link_or_reparse(after):
        raise CodeGraphError(f"trusted path became a link while reading: {relative}")
    return raw


def _resolved_gitdir(dot_git: Path) -> Path:
    try:
        pointer = dot_git.read_text(encoding="utf-8").strip()
    except OSError as error:
        raise CodeGraphError(f"cannot read worktree git pointer: {error}") from error
    if not pointer.startswith("gitdir: ") or "\n" in pointer or "\r" in pointer:
        raise CodeGraphError("malformed worktree git pointer")
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
        command.extend([f"--git-dir={_resolved_gitdir(dot_git)}", f"--work-tree={repo}"])
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
        raise CodeGraphError(f"git {' '.join(arguments)} failed: {error}") from error
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise CodeGraphError(f"git {' '.join(arguments)} failed: {detail}")
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
                    raise CodeGraphError(f"non-stage-0 Git entry: {path}")
            else:
                mode, kind, blob = fields
                if kind != "blob":
                    continue
            if path in inventory or re.fullmatch(r"[0-9a-f]{40}", blob) is None:
                raise CodeGraphError(f"malformed or duplicate {source} entry: {path}")
            inventory[path] = GitEntry(mode, blob)
    except CodeGraphError:
        raise
    except (UnicodeDecodeError, ValueError) as error:
        raise CodeGraphError(f"malformed {source} Git inventory: {error}") from error
    return inventory


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
                raise CodeGraphError(
                    f"cannot scan trusted code directory {directory_relative}: {error}"
                ) from error
            for entry in entries:
                relative = f"{directory_relative}/{entry.name}"
                metadata = entry.stat(follow_symlinks=False)
                if _is_link_or_reparse(metadata):
                    raise CodeGraphError(f"code graph contains symlink/reparse: {relative}")
                if stat.S_ISDIR(metadata.st_mode):
                    if entry.name != "__pycache__":
                        pending.append((Path(entry.path), relative))
                    continue
                if not stat.S_ISREG(metadata.st_mode):
                    raise CodeGraphError(f"code graph contains special file: {relative}")
                if relative.lower().endswith(LOADABLE_CODE_SUFFIXES):
                    if relative not in tracked_graph_paths:
                        raise CodeGraphError(f"untracked local code is forbidden: {relative}")


def check_code_graph(repo: Path = REPO) -> int:
    """Require stage0 == HEAD == worktree for every trusted code node."""

    stage = _git_inventory(repo, "stage0")
    head = _git_inventory(repo, "HEAD")
    missing_extras = sorted(set(CODE_GRAPH_EXTRA_PATHS) - set(stage))
    if missing_extras:
        raise CodeGraphError(f"required shell helper missing from stage0: {missing_extras}")
    stage_paths = sorted(path for path in stage if _is_graph_path(path))
    head_paths = sorted(path for path in head if _is_graph_path(path))
    if not stage_paths:
        raise CodeGraphError("trusted code graph is empty")
    if stage_paths != head_paths:
        raise CodeGraphError("trusted code graph path set differs between HEAD and stage0")
    for path in stage_paths:
        entry = stage[path]
        if entry.mode not in {"100644", "100755"}:
            raise CodeGraphError(f"code node has non-regular mode: {path}")
        if _trusted_bytes(repo, path) != _blob_bytes(repo, entry.blob):
            raise CodeGraphError(f"code node stage0/worktree mismatch: {path}")
        if head.get(path) != entry:
            raise CodeGraphError(f"code node HEAD/stage0 mismatch: {path}")
    _scan_for_untracked_code(repo, set(stage_paths))
    return len(stage_paths)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)
    try:
        count = check_code_graph(REPO)
    except CodeGraphError as error:
        print(f"code graph: FAIL: {error}")
        return 1
    print(f"code graph: PASS ({count} trusted nodes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
