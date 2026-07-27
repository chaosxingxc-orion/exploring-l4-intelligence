#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deterministic, zero-write audit-artifact immutability check.

Default mode and explicit ``--check`` recompute the report from the stage-0
registry/anchor graph and compare it byte-for-byte with the tracked report.
They never write.  ``--write`` is reserved for an explicit transaction that
has already staged a legal registry/anchor change; after writing, callers must
stage the report and run ``--check``.

Registered artifacts must simultaneously match their pinned Git blob at HEAD,
their stage-0 blob, and their trusted worktree bytes.  The deterministic report
binds the stage-0 registry and anchor modes/blobs plus the complete registry
prefix count/hash.  It deliberately contains no current-HEAD or self hash, so a
later unrelated commit cannot make a clean check dirty or stale.
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import stat
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Callable


REPO = Path(__file__).resolve().parents[2]
CHECKS_DIR = REPO / "scripts" / "checks"
if str(CHECKS_DIR) not in sys.path:
    sys.path.insert(0, str(CHECKS_DIR))

from ai_context_inventory import registry_prefix_sha256  # noqa: E402
from ai_context_surface_check import (  # noqa: E402
    ContextSurfaceError,
    TrustedRepoReader,
    git_command_prefix,
    loads_json_strict,
)
from sf_query_compiler import atomic_write_bytes  # noqa: E402


REGISTRY_RELATIVE = "wiki/survey/sf-audit-artifact-registry.json"
ANCHOR_RELATIVE = "scripts/checks/ai_context_inventory.py"
OUT_RELATIVE = "docs/checks/2026-07-19-sf-audit-immutability-check.json"
OUT = REPO.joinpath(*OUT_RELATIVE.split("/"))
REGULAR_MODES = {"100644", "100755"}
HEX40 = re.compile(r"[0-9a-f]{40}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")


class AuditCheckError(RuntimeError):
    """The Git graph or deterministic report contract is malformed."""


@dataclass(frozen=True)
class GitEntry:
    mode: str
    blob: str


def git(*args: str, repo: Path = REPO) -> subprocess.CompletedProcess:
    """Run one UTF-8 Git command, including linked-worktree translation."""

    completed = subprocess.run(
        [*git_command_prefix(repo), *args],
        cwd=repo,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    completed.check_returncode()
    return completed


def _git_bytes(repo: Path, *args: str) -> bytes:
    completed = subprocess.run(
        [*git_command_prefix(repo), *args],
        cwd=repo,
        capture_output=True,
    )
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise AuditCheckError(f"git {' '.join(args)} failed: {detail}")
    return completed.stdout


def _canonical_path(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise AuditCheckError(f"{label} must be a nonempty repository path")
    path = PurePosixPath(value)
    if (
        "\\" in value
        or path.is_absolute()
        or value != path.as_posix()
        or any(part in ("", ".", "..") for part in path.parts)
    ):
        raise AuditCheckError(f"{label} is not canonical: {value!r}")
    return value


def _parse_stage0(raw: bytes) -> dict[str, GitEntry]:
    entries: dict[str, GitEntry] = {}
    try:
        for record in (item for item in raw.split(b"\0") if item):
            metadata, raw_path = record.split(b"\t", 1)
            raw_mode, raw_blob, raw_stage = metadata.split(b" ", 2)
            path = _canonical_path(raw_path.decode("utf-8"), "Git index path")
            mode = raw_mode.decode("ascii")
            blob = raw_blob.decode("ascii")
            stage = raw_stage.decode("ascii")
            if stage != "0":
                raise AuditCheckError(f"non-stage-0 Git index entry: {path}")
            if path in entries:
                raise AuditCheckError(f"duplicate Git index path: {path}")
            if HEX40.fullmatch(blob) is None:
                raise AuditCheckError(f"invalid staged Git blob for {path}")
            entries[path] = GitEntry(mode, blob)
    except AuditCheckError:
        raise
    except (UnicodeDecodeError, ValueError) as error:
        raise AuditCheckError(f"malformed stage-0 Git inventory: {error}") from error
    return entries


def _parse_head(raw: bytes) -> dict[str, GitEntry]:
    entries: dict[str, GitEntry] = {}
    try:
        for record in (item for item in raw.split(b"\0") if item):
            metadata, raw_path = record.split(b"\t", 1)
            raw_mode, raw_type, raw_blob = metadata.split(b" ", 2)
            if raw_type != b"blob":
                continue
            path = _canonical_path(raw_path.decode("utf-8"), "HEAD path")
            mode = raw_mode.decode("ascii")
            blob = raw_blob.decode("ascii")
            if path in entries:
                raise AuditCheckError(f"duplicate HEAD path: {path}")
            if HEX40.fullmatch(blob) is None:
                raise AuditCheckError(f"invalid HEAD Git blob for {path}")
            entries[path] = GitEntry(mode, blob)
    except AuditCheckError:
        raise
    except (UnicodeDecodeError, ValueError) as error:
        raise AuditCheckError(f"malformed HEAD Git inventory: {error}") from error
    return entries


def _stage_graph(repo: Path) -> tuple[dict[str, GitEntry], Callable[[str], bytes]]:
    inventory = _parse_stage0(_git_bytes(repo, "ls-files", "-s", "-z"))
    cache: dict[str, bytes] = {}

    def read_blob(blob: str) -> bytes:
        if HEX40.fullmatch(blob) is None:
            raise AuditCheckError(f"invalid Git blob request: {blob!r}")
        if blob not in cache:
            cache[blob] = _git_bytes(repo, "cat-file", "blob", blob)
        return cache[blob]

    return inventory, read_blob


def _require_regular(
    inventory: dict[str, GitEntry], path: str, label: str
) -> GitEntry:
    entry = inventory.get(path)
    if entry is None:
        raise AuditCheckError(f"{label} is not tracked at stage 0: {path}")
    if entry.mode not in REGULAR_MODES:
        raise AuditCheckError(f"{label} has non-regular Git mode {entry.mode}: {path}")
    return entry


def _anchor_values(raw: bytes, label: str = "staged anchor") -> tuple[int, str]:
    try:
        tree = ast.parse(raw.decode("utf-8"), filename=ANCHOR_RELATIVE)
    except (UnicodeDecodeError, SyntaxError) as error:
        raise AuditCheckError(f"invalid {label} source: {error}") from error
    values: dict[str, object] = {}
    wanted = {"REGISTRY_BASELINE_COUNT", "REGISTRY_BASELINE_PREFIX_SHA256"}
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        value_node = node.value
        for target in targets:
            if isinstance(target, ast.Name) and target.id in wanted:
                if target.id in values:
                    raise AuditCheckError(f"duplicate {label} {target.id}")
                try:
                    values[target.id] = ast.literal_eval(value_node)
                except (ValueError, TypeError) as error:
                    raise AuditCheckError(
                        f"{label} {target.id} must be a literal"
                    ) from error
    if set(values) != wanted:
        raise AuditCheckError(
            f"{label} must define exactly the required literals; found {sorted(values)}"
        )
    count = values["REGISTRY_BASELINE_COUNT"]
    prefix = values["REGISTRY_BASELINE_PREFIX_SHA256"]
    if isinstance(count, bool) or not isinstance(count, int) or count <= 0:
        raise AuditCheckError("REGISTRY_BASELINE_COUNT must be a positive integer")
    if not isinstance(prefix, str) or HEX64.fullmatch(prefix) is None:
        raise AuditCheckError("REGISTRY_BASELINE_PREFIX_SHA256 must be 64 lowercase hex")
    return count, prefix


def _registry_artifacts(
    raw: bytes, label: str = "staged registry"
) -> list[dict[str, str]]:
    try:
        document = loads_json_strict(raw, REGISTRY_RELATIVE)
    except ContextSurfaceError as error:
        raise AuditCheckError(str(error)) from error
    if not isinstance(document, dict) or not isinstance(document.get("artifacts"), list):
        raise AuditCheckError(f"{label} must be an object containing an artifacts list")
    artifacts: list[dict[str, str]] = []
    for index, artifact in enumerate(document["artifacts"]):
        if not isinstance(artifact, dict) or set(artifact) != {"path", "git_blob"}:
            raise AuditCheckError(
                f"{label} artifacts[{index}] must contain exactly path/git_blob"
            )
        path = _canonical_path(
            artifact["path"], f"{label} artifacts[{index}].path"
        )
        pin = artifact["git_blob"]
        if not isinstance(pin, str) or HEX40.fullmatch(pin) is None:
            raise AuditCheckError(f"{label} artifacts[{index}] has invalid Git blob")
        artifacts.append({"path": path, "git_blob": pin})
    return artifacts


def _registry_sunset(
    raw: bytes,
    artifacts: list[dict[str, str]],
    label: str = "staged registry",
) -> dict[str, tuple[str, str]]:
    """Parse append-only sunset exemptions bound to their registered pins.

    A sunset row records that a registered artifact's working-tree bytes were
    deleted, with `last_commit` naming the last commit whose tree still
    contains that exact blob at that path (verified in ``evaluate`` via
    ``git ls-tree``).  It never edits the original ``artifacts`` row.
    """

    try:
        document = loads_json_strict(raw, REGISTRY_RELATIVE)
    except ContextSurfaceError as error:
        raise AuditCheckError(str(error)) from error
    if not isinstance(document, dict):
        raise AuditCheckError(f"{label} must be an object")
    raw_sunset = document.get("sunset", [])
    if not isinstance(raw_sunset, list):
        raise AuditCheckError(f"{label} sunset must be a list")
    pins = {entry["path"]: entry["git_blob"] for entry in artifacts}
    sunset: dict[str, tuple[str, str]] = {}
    for index, entry in enumerate(raw_sunset):
        if not isinstance(entry, dict) or set(entry) != {
            "path",
            "git_blob",
            "last_commit",
        }:
            raise AuditCheckError(
                f"{label} sunset[{index}] must contain exactly "
                "path/git_blob/last_commit"
            )
        path = _canonical_path(entry["path"], f"{label} sunset[{index}].path")
        blob = entry["git_blob"]
        commit = entry["last_commit"]
        if not isinstance(blob, str) or HEX40.fullmatch(blob) is None:
            raise AuditCheckError(f"{label} sunset[{index}] has invalid Git blob")
        if not isinstance(commit, str) or HEX40.fullmatch(commit) is None:
            raise AuditCheckError(f"{label} sunset[{index}] has invalid last_commit")
        if path not in pins:
            raise AuditCheckError(
                f"{label} sunset[{index}] path is not a registered artifact: {path}"
            )
        if pins[path] != blob:
            raise AuditCheckError(
                f"{label} sunset[{index}] blob does not match registered pin: {path}"
            )
        if path in sunset:
            raise AuditCheckError(f"{label} sunset[{index}] duplicate path: {path}")
        sunset[path] = (blob, commit)
    return sunset


def _history_blob_matches(repo: Path, path: str, blob: str, commit: str) -> bool:
    """Prove ``git show <commit>:<path>`` still resolves to exactly ``blob``."""

    completed = subprocess.run(
        [*git_command_prefix(repo), "ls-tree", commit, "--", path],
        cwd=repo,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if completed.returncode != 0:
        return False
    line = completed.stdout.strip("\n")
    if not line:
        return False
    meta, sep, tail = line.partition("\t")
    if not sep or tail != path:
        return False
    parts = meta.split(" ")
    if len(parts) != 3:
        return False
    _mode, object_type, sha = parts
    return object_type == "blob" and sha == blob


def evaluate(
    artifacts: list[dict[str, str]],
    head: dict[str, GitEntry],
    staged: dict[str, GitEntry],
    read_blob: Callable[[str], bytes],
    read_worktree: Callable[[str], bytes],
    allow_staged_only_paths: set[str] | None = None,
    sunset: dict[str, tuple[str, str]] | None = None,
    verify_sunset_history: Callable[[str, str, str], bool] | None = None,
) -> list[str]:
    """Evaluate committed rows and an explicitly allowed atomic staged append."""

    failures: list[str] = []
    seen: set[str] = set()
    allowed_staged_only = allow_staged_only_paths or set()
    sunset = sunset or {}
    for artifact in artifacts:
        path, pin = artifact["path"], artifact["git_blob"]
        if path in seen:
            failures.append(f"{path}: duplicate registry row (append-only violated)")
        seen.add(path)
        if path in sunset:
            sunset_blob, sunset_commit = sunset[path]
            if sunset_blob != pin:
                failures.append(
                    f"{path}: sunset blob {sunset_blob[:12]} != pinned {pin[:12]}"
                )
            elif verify_sunset_history is None or not verify_sunset_history(
                path, pin, sunset_commit
            ):
                failures.append(
                    f"{path}: sunset record unrecoverable at "
                    f"{sunset_commit[:12]}:{path}"
                )
            continue
        head_entry = head.get(path)
        staged_entry = staged.get(path)
        if head_entry is None and path not in allowed_staged_only:
            failures.append(f"{path}: missing at HEAD (registered artifact not committed)")
        elif head_entry is not None and head_entry.mode not in REGULAR_MODES:
            failures.append(f"{path}: non-regular HEAD mode {head_entry.mode}")
        elif head_entry is not None and head_entry.blob != pin:
            failures.append(
                f"{path}: HEAD blob {head_entry.blob[:12]} != pinned {pin[:12]}"
            )
        if staged_entry is None:
            failures.append(f"{path}: missing at stage 0")
            continue
        if staged_entry.mode not in REGULAR_MODES:
            failures.append(f"{path}: non-regular stage-0 mode {staged_entry.mode}")
            continue
        if staged_entry.blob != pin:
            failures.append(
                f"{path}: stage-0 blob {staged_entry.blob[:12]} != pinned {pin[:12]}"
            )
        try:
            staged_raw = read_blob(staged_entry.blob)
            worktree_raw = read_worktree(path)
        except (AuditCheckError, ContextSurfaceError, OSError) as error:
            failures.append(f"{path}: trusted byte read failed: {error}")
            continue
        if worktree_raw != staged_raw:
            failures.append(f"{path}: worktree bytes differ from stage-0 Git blob")
    return failures


def _render_report(
    *,
    registry_entry: GitEntry,
    anchor_entry: GitEntry,
    registered: int,
    prefix_count: int,
    prefix_sha256: str,
    sunset_registered: int,
    failures: list[str],
    registry_relative: str,
    anchor_relative: str,
) -> bytes:
    result = {
        "schema": "sf-audit-immutability-report-v4",
        "check": "sf-audit-immutability",
        "registry": registry_relative,
        "registry_stage0": {
            "mode": registry_entry.mode,
            "git_blob": registry_entry.blob,
        },
        "anchor_stage0": {
            "path": anchor_relative,
            "mode": anchor_entry.mode,
            "git_blob": anchor_entry.blob,
        },
        "registered": registered,
        "registry_prefix": {
            "count": prefix_count,
            "sha256": prefix_sha256,
        },
        "sunset_registered": sunset_registered,
        "registry_lineage_contract": "stage0 preserves the exact HEAD prefix; count is HEAD or HEAD+1",
        "artifact_binding_contract": (
            "HEAD=pin; stage0=pin; worktree-bytes=stage0-blob; sunset-exempt: "
            "history(last_commit,path)=pin, HEAD/stage0/worktree presence not required"
        ),
        "sunset_lineage_contract": (
            "sunset is append-only: every HEAD sunset row must be preserved unchanged in stage0"
        ),
        "failures": failures,
        "status": "FAIL" if failures else "PASS",
    }
    return (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def expected_report(
    *,
    repo: Path,
    registry_relative: str,
    anchor_relative: str,
) -> tuple[bytes, list[str], int]:
    registry_relative = _canonical_path(registry_relative, "registry path")
    anchor_relative = _canonical_path(anchor_relative, "anchor path")
    staged, read_blob = _stage_graph(repo)
    head = _parse_head(_git_bytes(repo, "ls-tree", "-r", "-z", "HEAD", "--"))
    reader = TrustedRepoReader(repo)
    registry_entry = _require_regular(staged, registry_relative, "registry")
    anchor_entry = _require_regular(staged, anchor_relative, "anchor")
    head_registry_entry = _require_regular(head, registry_relative, "HEAD registry")
    head_anchor_entry = _require_regular(head, anchor_relative, "HEAD anchor")
    registry_raw = read_blob(registry_entry.blob)
    anchor_raw = read_blob(anchor_entry.blob)
    head_registry_raw = read_blob(head_registry_entry.blob)
    head_anchor_raw = read_blob(head_anchor_entry.blob)
    if reader.read_bytes(registry_relative) != registry_raw:
        raise AuditCheckError("registry worktree bytes differ from stage-0 Git blob")
    if reader.read_bytes(anchor_relative) != anchor_raw:
        raise AuditCheckError("anchor worktree bytes differ from stage-0 Git blob")
    artifacts = _registry_artifacts(registry_raw)
    count, expected_prefix = _anchor_values(anchor_raw)
    head_artifacts = _registry_artifacts(head_registry_raw, "HEAD registry")
    head_count, head_expected_prefix = _anchor_values(head_anchor_raw, "HEAD anchor")
    if len(head_artifacts) != head_count:
        raise AuditCheckError(
            "HEAD registry/anchor count mismatch: "
            f"registry={len(head_artifacts)}, anchor={head_count}"
        )
    head_actual_prefix = registry_prefix_sha256(head_artifacts, head_count)
    if head_actual_prefix != head_expected_prefix:
        raise AuditCheckError(
            f"HEAD registry prefix mismatch: {head_actual_prefix} != {head_expected_prefix}"
        )
    if len(artifacts) != count:
        raise AuditCheckError(
            f"registry/anchor count mismatch: registry={len(artifacts)}, anchor={count}"
        )
    actual_prefix = registry_prefix_sha256(artifacts, count)
    if actual_prefix != expected_prefix:
        raise AuditCheckError(
            f"registry prefix mismatch: {actual_prefix} != {expected_prefix}"
        )
    failures: list[str] = []
    if len(artifacts) not in {head_count, head_count + 1}:
        failures.append(
            "registry transaction must preserve the exact HEAD count or append exactly "
            f"one row: HEAD={head_count}, stage0={len(artifacts)}"
        )
    if artifacts[:head_count] != head_artifacts:
        failures.append("stage-0 registry does not preserve the complete HEAD artifact prefix")
    if len(artifacts) == head_count and (
        count != head_count or actual_prefix != head_actual_prefix
    ):
        failures.append("unchanged registry transaction does not preserve the HEAD anchor")
    staged_only_paths: set[str] = set()
    if len(artifacts) == head_count + 1 and artifacts[:head_count] == head_artifacts:
        staged_only_paths.add(artifacts[-1]["path"])

    # Sunset exemptions: append-only records that let a registered artifact's
    # working-tree bytes be absent iff history still proves the exact pinned
    # blob at its last committed path (evaluated below, not merely declared).
    sunset = _registry_sunset(registry_raw, artifacts)
    head_sunset = _registry_sunset(head_registry_raw, head_artifacts, "HEAD registry")
    for sunset_path, sunset_value in head_sunset.items():
        if sunset.get(sunset_path) != sunset_value:
            failures.append(
                f"{sunset_path}: sunset record must be preserved from HEAD (append-only)"
            )

    def _verify_sunset_history(path: str, blob: str, commit: str) -> bool:
        return _history_blob_matches(repo, path, blob, commit)

    failures.extend(
        evaluate(
            artifacts,
            head,
            staged,
            read_blob,
            reader.read_bytes,
            allow_staged_only_paths=staged_only_paths,
            sunset=sunset,
            verify_sunset_history=_verify_sunset_history,
        )
    )

    # Oracle-can-fail proof uses the same binding evaluator.
    wrong = [{"path": artifacts[0]["path"], "git_blob": "0" * 40}]
    if not evaluate(wrong, head, staged, read_blob, reader.read_bytes):
        raise AuditCheckError("negative fixture was not rejected")

    report = _render_report(
        registry_entry=registry_entry,
        anchor_entry=anchor_entry,
        registered=len(artifacts),
        prefix_count=count,
        prefix_sha256=actual_prefix,
        sunset_registered=len(sunset),
        failures=failures,
        registry_relative=registry_relative,
        anchor_relative=anchor_relative,
    )
    return report, failures, len(artifacts)


def _is_link_or_reparse(metadata: os.stat_result) -> bool:
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    attributes = getattr(metadata, "st_file_attributes", 0)
    return stat.S_ISLNK(metadata.st_mode) or bool(attributes & reparse_flag)


def _validate_report_path(repo: Path, output_relative: str) -> Path:
    """Reject a report path containing a symlink/reparse point or escaping repo."""

    try:
        root = Path(repo).resolve(strict=True)
        candidate = root.joinpath(*PurePosixPath(output_relative).parts)
        current = root
        for part in PurePosixPath(output_relative).parts:
            current = current / part
            metadata = os.lstat(current)
            if _is_link_or_reparse(metadata):
                raise AuditCheckError(
                    f"untrusted report path: symlink/reparse component {part}"
                )
        resolved = candidate.resolve(strict=True)
        try:
            resolved.relative_to(root)
        except ValueError as error:
            raise AuditCheckError("report path resolves outside repository") from error
        metadata = os.lstat(candidate)
        if _is_link_or_reparse(metadata) or not stat.S_ISREG(metadata.st_mode):
            raise AuditCheckError("report path is not a trusted regular file")
        return candidate
    except AuditCheckError:
        raise
    except OSError as error:
        raise AuditCheckError(f"untrusted report path: {error}") from error


def _write_preflight(repo: Path, output_relative: str) -> Path:
    staged, read_blob = _stage_graph(repo)
    head = _parse_head(_git_bytes(repo, "ls-tree", "-r", "-z", "HEAD", "--"))
    report_entry = _require_regular(staged, output_relative, "stage-0 report")
    head_report_entry = _require_regular(head, output_relative, "HEAD report")
    if report_entry != head_report_entry:
        raise AuditCheckError(
            "report has an uncommitted stage-0 change; commit it before --write"
        )
    output = _validate_report_path(repo, output_relative)
    try:
        worktree_report = TrustedRepoReader(repo).read_bytes(output_relative)
    except ContextSurfaceError as error:
        raise AuditCheckError(str(error)) from error
    if worktree_report != read_blob(report_entry.blob):
        raise AuditCheckError(
            "report worktree bytes differ from clean HEAD/stage-0 report; refusing overwrite"
        )
    return output


def _verify_written_report(repo: Path, output_relative: str, expected: bytes) -> None:
    _validate_report_path(repo, output_relative)
    try:
        actual = TrustedRepoReader(repo).read_bytes(output_relative)
    except ContextSurfaceError as error:
        raise AuditCheckError(str(error)) from error
    if actual != expected:
        raise AuditCheckError("written report failed post-write byte verification")


def run(
    mode: str,
    *,
    repo: Path = REPO,
    registry_relative: str = REGISTRY_RELATIVE,
    anchor_relative: str = ANCHOR_RELATIVE,
) -> int:
    """Run deterministic write or zero-write check mode."""

    if mode not in {"check", "write"}:
        raise ValueError(f"unsupported mode: {mode}")
    repo = Path(repo)
    output_relative = OUT_RELATIVE
    expected, failures, registered = expected_report(
        repo=repo,
        registry_relative=registry_relative,
        anchor_relative=anchor_relative,
    )
    output = repo.joinpath(*output_relative.split("/"))
    report_failure: str | None = None
    if mode == "write":
        if not failures:
            try:
                output = _write_preflight(repo, output_relative)
                atomic_write_bytes(output, expected)
                _verify_written_report(repo, output_relative, expected)
            except AuditCheckError as error:
                report_failure = str(error)
    else:
        staged, read_blob = _stage_graph(repo)
        report_entry = _require_regular(staged, output_relative, "tracked report")
        staged_report = read_blob(report_entry.blob)
        try:
            worktree_report = TrustedRepoReader(repo).read_bytes(output_relative)
        except ContextSurfaceError as error:
            raise AuditCheckError(str(error)) from error
        if staged_report != expected:
            report_failure = "tracked stage-0 report is stale"
        elif worktree_report != staged_report:
            report_failure = "report worktree bytes differ from tracked stage-0 report"

    for failure in failures:
        print(f"[IMMUTABILITY] {failure}")
    if report_failure is not None:
        print(f"[IMMUTABILITY] {report_failure}")
    status = "PASS" if not failures and report_failure is None else "FAIL"
    print(
        f"audit immutability: {status} "
        f"({registered} registered, {len(failures)} artifact failures)"
    )
    return 0 if status == "PASS" else 1


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--check", action="store_true", help="zero-write check (default)")
    modes.add_argument("--write", action="store_true", help="write deterministic report")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    arguments = _parse_args(argv)
    mode = "write" if arguments.write else "check"
    try:
        return run(mode)
    except (AuditCheckError, ContextSurfaceError, OSError, subprocess.CalledProcessError) as error:
        print(f"[IMMUTABILITY] {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
