#!/usr/bin/env python3
"""Build the deterministic manifest for the active Stage-1A survey layer."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


REPO = Path(__file__).resolve().parents[2]
CHECKS_DIR = REPO / "scripts" / "checks"
if str(CHECKS_DIR) not in sys.path:
    sys.path.insert(0, str(CHECKS_DIR))

from ai_context_surface_check import ContextSurfaceError, TrustedRepoReader  # noqa: E402
from build_ai_context_manifest import (  # noqa: E402
    ACTIVE_REVIEW_TRANSACTION,
    AUDIT_CAMPAIGN_INDEX_PATH,
)
from sf_current_path_contract import (  # noqa: E402
    TrustedCurrentPathError,
    read_fixed_bytes,
    resolve_fixed_output,
)
from sf_query_compiler import atomic_write_bytes  # noqa: E402


OUTPUT_RELATIVE_PATH = "wiki/survey/current/manifest.json"
OUTPUT_PATH = REPO.joinpath(*OUTPUT_RELATIVE_PATH.split("/"))


class CurrentManifestError(RuntimeError):
    """The current manifest could not be built or verified."""


@dataclass(frozen=True)
class FileSpec:
    role: str
    path: str
    mutability: str
    load_policy: str


@dataclass(frozen=True)
class GitIndexEntry:
    mode: str
    blob: str


_SIDECAR_NAMES = (
    "2026.findings-acl.1243.sidecar.json",
    "2026.findings-acl.1724.sidecar.json",
    "2026.findings-acl.511.sidecar.json",
    "2602.16485.sidecar.json",
    "2604.16529.sidecar.json",
    "2605.08083.sidecar.json",
    "2606.01667.sidecar.json",
    "2606.03054.sidecar.json",
)


BASE_FILE_SPECS = (
    FileSpec(
        "v6_opening_report",
        "docs/checks/system-first-stage1a/evidence-v6/identity-taxonomy-v6-test.json",
        "release-scoped-immutable",
        "targeted",
    ),
    FileSpec(
        "v6_report_windows",
        "docs/checks/system-first-stage1a/evidence-v6/identity-taxonomy-v6-test.nt.json",
        "release-scoped-immutable",
        "targeted",
    ),
    FileSpec(
        "v6_report_wsl",
        "docs/checks/system-first-stage1a/evidence-v6/identity-taxonomy-v6-test.posix.json",
        "release-scoped-immutable",
        "targeted",
    ),
    FileSpec(
        "dual_platform_aggregate_checker",
        "scripts/survey/sf_dual_platform_check.py",
        "normal-code-lifecycle",
        "machine-only",
    ),
    FileSpec(
        "frozen_queries",
        "wiki/survey/2026-07-15-sf-queries.jsonl",
        "frozen",
        "targeted",
    ),
    FileSpec(
        "seed_manifest",
        "wiki/survey/2026-07-15-sf-seed-manifest.jsonl",
        "controlled-append-only",
        "targeted",
    ),
    FileSpec(
        "canon_registry",
        "wiki/survey/2026-07-17-sf-canon.json",
        "controlled-append-only",
        "targeted",
    ),
    FileSpec(
        "fulltext_ledger",
        "wiki/survey/2026-07-17-sf-fulltext-ledger.jsonl",
        "controlled-append-only",
        "targeted",
    ),
    FileSpec(
        "current_router",
        "wiki/survey/current/README.md",
        "supersede-in-place",
        "targeted",
    ),
    FileSpec(
        "protocol_v2",
        "wiki/survey/current/protocol.md",
        "supersede-in-place",
        "targeted",
    ),
    FileSpec(
        "identity_taxonomy_v6",
        "wiki/survey/current/data/identity-taxonomy-v6.json",
        "generated",
        "targeted",
    ),
    FileSpec(
        "known_item_coding_v7",
        "wiki/survey/current/data/known-item-coding-v7.json",
        "generated",
        "targeted",
    ),
    FileSpec(
        "schema_v3_adjudication",
        "wiki/survey/current/data/schema-v3-adjudication.json",
        "controlled-append-only",
        "targeted",
    ),
    *tuple(
        FileSpec(
            f"schema_v3_sidecar:{name}",
            f"wiki/survey/current/data/schema-v3/sidecars/{name}",
            "generated",
            "machine-only",
        )
        for name in _SIDECAR_NAMES
    ),
    FileSpec(
        "current_status",
        "wiki/survey/current/status.md",
        "supersede-in-place",
        "targeted",
    ),
    FileSpec(
        "current_opening_table",
        "wiki/survey/current/tables/opening-guarantees.md",
        "generated",
        "targeted",
    ),
)


_AUDIT_FILE_SPECS = (
    FileSpec(
        "campaign_audit_index",
        AUDIT_CAMPAIGN_INDEX_PATH,
        "append-only",
        "cold-audit",
    ),
    FileSpec(
        "active_review_transaction",
        ACTIVE_REVIEW_TRANSACTION,
        "immutable-after-first-commit",
        "targeted",
    ),
)

_BASE_RELEASE_BOUND = (
    "wiki/survey/current/tables/opening-guarantees.md",
)
_BASE_PROSE_SCAN = (
    "wiki/survey/current/README.md",
    "wiki/survey/current/protocol.md",
    "wiki/survey/current/status.md",
    "wiki/survey/current/tables/opening-guarantees.md",
)


def _active_audit_specs(index_inventory: dict[str, GitIndexEntry]) -> tuple[FileSpec, ...]:
    index_tracked = AUDIT_CAMPAIGN_INDEX_PATH in index_inventory
    correction_tracked = ACTIVE_REVIEW_TRANSACTION in index_inventory
    if index_tracked != correction_tracked:
        raise CurrentManifestError(
            "audit-activation-incomplete: "
            f"index tracked={index_tracked}, correction tracked={correction_tracked}"
        )
    if not index_tracked:
        return ()
    return _AUDIT_FILE_SPECS


def _validate_index_entry(path: str, entry: GitIndexEntry) -> GitIndexEntry:
    if not isinstance(entry, GitIndexEntry):
        raise CurrentManifestError(f"manifest index entry malformed: {path}")
    if entry.mode not in {"100644", "100755"}:
        raise CurrentManifestError(
            f"manifest input is not a regular Git mode: {path}: {entry.mode}"
        )
    if re.fullmatch(r"[0-9a-f]{40}", entry.blob) is None:
        raise CurrentManifestError(
            f"manifest input has malformed blob: {path}: {entry.blob!r}"
        )
    return entry


def _file_entry(
    spec: FileSpec,
    read_bytes: Callable[[str], bytes],
    index_inventory: dict[str, GitIndexEntry],
    read_blob: Callable[[str], bytes],
) -> dict:
    index_entry = index_inventory.get(spec.path)
    if index_entry is None:
        raise CurrentManifestError(f"manifest-input-untracked: {spec.path}")
    index_entry = _validate_index_entry(spec.path, index_entry)
    try:
        raw = read_bytes(spec.path)
    except (OSError, ContextSurfaceError) as error:
        raise CurrentManifestError(f"manifest input missing: {spec.path}: {error}") from error
    if not isinstance(raw, bytes):
        raise CurrentManifestError(f"manifest reader returned non-bytes: {spec.path}")
    try:
        staged_raw = read_blob(index_entry.blob)
    except (OSError, CurrentManifestError) as error:
        raise CurrentManifestError(
            f"manifest staged blob unavailable: {spec.path}: {error}"
        ) from error
    if not isinstance(staged_raw, bytes):
        raise CurrentManifestError(f"Git blob reader returned non-bytes: {spec.path}")
    if raw != staged_raw:
        raise CurrentManifestError(
            "staged-worktree-byte-mismatch: "
            f"{spec.path}: index={index_entry.blob}, "
            f"staged_sha256={hashlib.sha256(staged_raw).hexdigest()}, "
            f"worktree_sha256={hashlib.sha256(raw).hexdigest()}"
        )
    return {
        "role": spec.role,
        "path": spec.path,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "mutability": spec.mutability,
        "load_policy": spec.load_policy,
    }


def build_manifest(
    read_bytes: Callable[[str], bytes],
    index_inventory: dict[str, GitIndexEntry],
    read_blob: Callable[[str], bytes],
) -> dict:
    if not isinstance(index_inventory, dict):
        raise CurrentManifestError("Git index inventory must be a path map")
    audit_specs = _active_audit_specs(index_inventory)
    specs = (*BASE_FILE_SPECS, *audit_specs)
    paths = [spec.path for spec in specs]
    roles = [spec.role for spec in specs]
    if len(paths) != len(set(paths)) or len(roles) != len(set(roles)):
        raise CurrentManifestError("duplicate role or path in current manifest constants")
    if OUTPUT_RELATIVE_PATH in paths:
        raise CurrentManifestError("current manifest must not hash itself")

    entries = sorted(
        (
            _file_entry(spec, read_bytes, index_inventory, read_blob)
            for spec in specs
        ),
        key=lambda entry: entry["path"],
    )
    release_bound = list(_BASE_RELEASE_BOUND)
    prose_scan = list(_BASE_PROSE_SCAN)
    if audit_specs:
        release_bound.append(ACTIVE_REVIEW_TRANSACTION)
        prose_scan.append(ACTIVE_REVIEW_TRANSACTION)
    return {
        "schema": "sf-current-manifest-v1",
        "files": entries,
        "release_bound_artifacts": release_bound,
        "prose_scan_paths": prose_scan,
    }


def render_manifest(
    read_bytes: Callable[[str], bytes],
    index_inventory: dict[str, GitIndexEntry],
    read_blob: Callable[[str], bytes],
) -> bytes:
    document = build_manifest(read_bytes, index_inventory, read_blob)
    return (
        json.dumps(
            document,
            ensure_ascii=False,
            indent=2,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def _canonical_git_path(path: str) -> str:
    if (
        not path
        or "\\" in path
        or path.startswith("/")
        or re.match(r"^[A-Za-z]:", path)
    ):
        raise CurrentManifestError(f"Git index path is not canonical: {path!r}")
    parts = path.split("/")
    if any(part in ("", ".", "..") for part in parts):
        raise CurrentManifestError(f"Git index path has unsafe component: {path!r}")
    return path


def _parse_git_index(raw: bytes) -> dict[str, GitIndexEntry]:
    inventory: dict[str, GitIndexEntry] = {}
    try:
        for record in (item for item in raw.split(b"\0") if item):
            metadata, raw_path = record.split(b"\t", 1)
            raw_mode, raw_blob, stage = metadata.split(b" ", 2)
            if stage != b"0":
                raise CurrentManifestError("git inventory contains non-stage-0 entry")
            mode = raw_mode.decode("ascii")
            blob = raw_blob.decode("ascii")
            if re.fullmatch(r"[0-7]{6}", mode) is None:
                raise CurrentManifestError(f"git inventory contains malformed mode: {mode!r}")
            if re.fullmatch(r"[0-9a-f]{40}", blob) is None:
                raise CurrentManifestError(f"git inventory contains malformed blob: {blob!r}")
            path = _canonical_git_path(raw_path.decode("utf-8"))
            if path in inventory:
                raise CurrentManifestError(f"git inventory duplicates path: {path}")
            inventory[path] = GitIndexEntry(mode, blob)
    except (ValueError, UnicodeDecodeError, UnicodeEncodeError) as error:
        raise CurrentManifestError(f"git inventory output is malformed: {error}") from error
    return inventory


def _resolved_gitdir(dot_git: Path, platform: str = os.name) -> Path:
    """Resolve a native-Windows worktree pointer under Windows or WSL."""

    try:
        pointer = dot_git.read_text(encoding="utf-8").strip()
    except OSError as error:
        raise CurrentManifestError(f"cannot read worktree git pointer: {error}") from error
    prefix = "gitdir: "
    if not pointer.startswith(prefix) or "\n" in pointer or "\r" in pointer:
        raise CurrentManifestError(f"malformed worktree git pointer: {dot_git}")
    raw = pointer[len(prefix) :]
    windows_absolute = re.fullmatch(r"([A-Za-z]):[\\/](.*)", raw)
    if windows_absolute:
        if platform == "posix":
            drive, remainder = windows_absolute.groups()
            return Path(f"/mnt/{drive.lower()}/{remainder.replace('\\', '/')}")
        return Path(raw)
    candidate = Path(raw)
    return candidate if candidate.is_absolute() else dot_git.parent / candidate


def _git_command_prefix(repo: Path) -> list[str]:
    command = ["git"]
    dot_git = repo / ".git"
    if dot_git.is_file():
        command.extend(
            [
                f"--git-dir={_resolved_gitdir(dot_git)}",
                f"--work-tree={repo}",
            ]
        )
    return command


def _run_git(repo: Path, arguments: list[str], *, label: str) -> bytes:
    command = [*_git_command_prefix(repo), *arguments]
    try:
        result = subprocess.run(
            command,
            cwd=repo,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as error:
        raise CurrentManifestError(f"git inventory failed: {error}") from error
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise CurrentManifestError(f"{label} failed: {detail}")
    return result.stdout


def _git_release_context(
    repo: Path,
) -> tuple[dict[str, GitIndexEntry], Callable[[str], bytes]]:
    inventory = _parse_git_index(
        _run_git(repo, ["ls-files", "-s", "-z"], label="git inventory")
    )
    cache: dict[str, bytes] = {}

    def read_blob(blob: str) -> bytes:
        if re.fullmatch(r"[0-9a-f]{40}", blob) is None:
            raise CurrentManifestError(f"malformed staged blob id: {blob!r}")
        if blob not in cache:
            cache[blob] = _run_git(
                repo, ["cat-file", "blob", blob], label=f"git cat-file {blob}"
            )
        return cache[blob]

    return inventory, read_blob


def _repo_reader(repo: Path = REPO) -> Callable[[str], bytes]:
    try:
        reader = TrustedRepoReader(repo)
    except ContextSurfaceError as error:
        raise CurrentManifestError(f"repository root is untrusted: {error}") from error
    return reader.read_bytes


def expected_bytes() -> bytes:
    inventory, read_blob = _git_release_context(REPO)
    return render_manifest(_repo_reader(), inventory, read_blob)


def _resolve_output_path(
    repo: Path, target: Path, *, allow_missing_leaf: bool
) -> Path:
    return resolve_fixed_output(
        repo,
        target,
        OUTPUT_RELATIVE_PATH,
        allow_missing_leaf=allow_missing_leaf,
    )


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
            raise CurrentManifestError(f"current manifest missing: {error}") from error
        if actual != expected:
            raise CurrentManifestError(
                "current manifest byte mismatch: "
                f"expected {hashlib.sha256(expected).hexdigest()}, "
                f"found {hashlib.sha256(actual).hexdigest()}"
            )
    except (
        CurrentManifestError,
        TrustedCurrentPathError,
        ContextSurfaceError,
        OSError,
        ValueError,
    ) as error:
        print(f"[CURRENT-MANIFEST] {error}")
        print("current survey manifest: FAIL")
        return 1
    print("current survey manifest: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
