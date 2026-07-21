"""Exact active schema-v3 release inventory and safe lineage-path contract."""
from __future__ import annotations

import hashlib
import os
import re
import stat
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from sf_json_contract import JsonContractError, loads


FINAL_SIDECAR_NAMES = (
    "2026.findings-acl.1243.sidecar.json",
    "2026.findings-acl.1724.sidecar.json",
    "2026.findings-acl.511.sidecar.json",
    "2602.16485.sidecar.json",
    "2604.16529.sidecar.json",
    "2605.08083.sidecar.json",
    "2606.01667.sidecar.json",
    "2606.03054.sidecar.json",
)
FINAL_SIDECAR_SHA256 = {
    "2026.findings-acl.1243.sidecar.json": (
        "d246b46102c9ed4256046cd1ec7476defd349826cee151171f19a954a5933064"
    ),
    "2026.findings-acl.1724.sidecar.json": (
        "f8527bf82b35681e7747de1ffb333c745b6f61ad71744a98b80d2f40cf835653"
    ),
    "2026.findings-acl.511.sidecar.json": (
        "7b4c5951abbb1840ba55df2fee0cac6ff44eed331e94f83b403c0ee5e4d04cbc"
    ),
    "2602.16485.sidecar.json": (
        "b4201e535f7dbea0cee9f92d506c9e8ecd80b031d7f9aa3608e8e5085a68950f"
    ),
    "2604.16529.sidecar.json": (
        "5644117d98d79f2ce114ad85eb96e5c5bda3d9a3102d45ce0c57fde275a818e5"
    ),
    "2605.08083.sidecar.json": (
        "be8245101d06dd8d881381dabda719259264e3ab5e031fd1057e5ba3c156d602"
    ),
    "2606.01667.sidecar.json": (
        "82056e0957c85d95c1bf4d772af82a2db3ba3d2017f607ae9309bd7c83099d69"
    ),
    "2606.03054.sidecar.json": (
        "49e25753ed7e8ef8b35cf1dd6ebe90a5d2915ae4f1f8e70fbc6d034b052ff616"
    ),
}
EXPECTED_WORK_IDS = (
    "2026.findings-acl.1243",
    "2026.findings-acl.1724",
    "2026.findings-acl.511",
    "2602.16485",
    "2604.16529",
    "2605.08083",
    "2606.01667",
    "2606.03054",
)
EXPECTED_METHOD_PATH_IDS = (
    "2026.findings-acl.1243#closed-prompt-only",
    "2026.findings-acl.1243#open-sft-variant",
    "2026.findings-acl.1724#pipeline",
    "2026.findings-acl.511#prm-guided-search",
    "2602.16485#calibrated-orchestration",
    "2604.16529#pdr-random-k",
    "2604.16529#rtv",
    "2604.16529#rtv-pdr-pipeline",
    "2605.08083#discovered-controller",
    "2606.01667#agentic-orchestration",
    "2606.03054#trained-gate",
)
ADJUDICATION_RELATIVE_PATH = (
    "wiki/survey/current/data/schema-v3-adjudication.json"
)
SIDECAR_DIRECTORY_RELATIVE_PATH = (
    "wiki/survey/current/data/schema-v3/sidecars"
)
ADJUDICATION_SHA256 = (
    "3e08d7a3c1c6db53a31ad0e023f9957e8f1b604a0e3c4e91b1b525c7400acd5f"
)


class ReleaseContractError(ValueError):
    """Raised when active release bytes, inventory, or lineage drift."""


@dataclass(frozen=True)
class ActiveReleaseSnapshot:
    sidecars: tuple
    adjudication: object
    adjudication_raw: bytes
    method_path_ids: tuple


def _within(path, root):
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _portable_relative(value, label):
    if isinstance(value, PurePosixPath):
        value = value.as_posix()
    elif isinstance(value, Path):
        value = value.as_posix()
    if not isinstance(value, str) or not value:
        raise ReleaseContractError(f"{label} must be a non-empty string")
    if "\\" in value or re.match(r"^[A-Za-z]:", value):
        raise ReleaseContractError(f"{label} is not portable POSIX: {value!r}")
    parts = value.split("/")
    if any(part in ("", ".", "..") for part in parts):
        raise ReleaseContractError(f"{label} contains unsafe component: {value!r}")
    pure = PurePosixPath(value)
    if pure.is_absolute():
        raise ReleaseContractError(f"{label} must be repo-relative: {value!r}")
    return pure


def resolve_trusted_repo_path(
    repo_root,
    target,
    *,
    expected_relative,
    expected_kind="file",
):
    """Resolve one prescribed path below a trusted root without following links.

    The root itself is trusted by the caller.  Every component below it is
    inspected with lstat before resolution; the resolved result must still be
    the exact prescribed repo-relative path below the trusted root.
    """
    expected = _portable_relative(expected_relative, "expected repo path")
    root = Path(repo_root)
    try:
        root_resolved = root.resolve(strict=True)
    except OSError as error:
        raise ReleaseContractError(
            f"trusted repo root does not resolve: {repo_root}: {error}"
        ) from error
    if not root_resolved.is_dir():
        raise ReleaseContractError(f"trusted repo root is not a directory: {repo_root}")

    root_lexical = Path(os.path.abspath(root))
    requested = Path(target)
    requested_parts = requested.parts
    if any(part in (".", "..") for part in requested_parts):
        raise ReleaseContractError(f"target path contains unsafe component: {target}")
    if not requested.is_absolute():
        requested = root_lexical / requested
    requested_lexical = Path(os.path.abspath(requested))
    prescribed_lexical = root_lexical.joinpath(*expected.parts)
    if os.path.normcase(str(requested_lexical)) != os.path.normcase(
        str(prescribed_lexical)
    ):
        raise ReleaseContractError(
            "target is not the prescribed repo-relative path "
            f"{expected.as_posix()}: {target}"
        )

    candidate = root
    for part in expected.parts:
        candidate = candidate / part
        try:
            mode = candidate.lstat().st_mode
        except OSError as error:
            raise ReleaseContractError(
                f"repo path component is unavailable: {candidate}: {error}"
            ) from error
        if stat.S_ISLNK(mode):
            raise ReleaseContractError(
                f"repo path contains symlink component: {expected.as_posix()}"
            )

    try:
        resolved = candidate.resolve(strict=True)
    except OSError as error:
        raise ReleaseContractError(
            f"repo path does not resolve: {expected.as_posix()}: {error}"
        ) from error
    prescribed_resolved = root_resolved.joinpath(*expected.parts)
    if resolved != prescribed_resolved or not _within(resolved, root_resolved):
        raise ReleaseContractError(
            f"repo path escapes or resolves away from prescribed path: {expected.as_posix()}"
        )
    if expected_kind == "file" and not resolved.is_file():
        raise ReleaseContractError(f"repo path is not a file: {expected.as_posix()}")
    if expected_kind == "dir" and not resolved.is_dir():
        raise ReleaseContractError(f"repo path is not a directory: {expected.as_posix()}")
    if expected_kind not in ("file", "dir"):
        raise ReleaseContractError(f"unknown expected path kind: {expected_kind}")
    return resolved


def validate_repo_relative_path(
    value,
    repo_root,
    *,
    allowed_root=Path("wiki/survey"),
):
    """Resolve one POSIX repo-relative, existing, non-symlink file path."""
    pure = _portable_relative(value, "lineage path")
    allowed_pure = _portable_relative(allowed_root, "allowed lineage root")
    try:
        pure.relative_to(allowed_pure)
    except ValueError as error:
        raise ReleaseContractError(
            f"lineage path is outside allowed root {allowed_pure}: {value!r}"
        ) from error

    return resolve_trusted_repo_path(
        repo_root,
        Path(repo_root).joinpath(*pure.parts),
        expected_relative=pure,
        expected_kind="file",
    )


def validate_canonical_record_id(value, repo_root):
    if not isinstance(value, str):
        raise ReleaseContractError("canonical_record_id must be a string")
    path, marker, fragment = value.partition("#")
    if marker != "#" or not fragment:
        raise ReleaseContractError(
            "canonical_record_id requires a safe path and non-empty fragment"
        )
    resolved = validate_repo_relative_path(path, repo_root)
    return resolved, fragment


def _validate_sidecar_lineage(sidecar, repo_root, name):
    fulltext = sidecar.get("fulltext")
    if not isinstance(fulltext, dict):
        raise ReleaseContractError(f"{name}: fulltext container invalid")
    validate_repo_relative_path(fulltext.get("ledger"), repo_root)
    validate_canonical_record_id(sidecar.get("canonical_record_id"), repo_root)


def validate_coding_lineage(coding, repo_root):
    rows = coding.get("rows") if isinstance(coding, dict) else None
    if not isinstance(rows, list):
        raise ReleaseContractError("coding rows container invalid")
    for row in rows:
        if not isinstance(row, dict):
            raise ReleaseContractError("coding row container invalid")
        fulltext = row.get("fulltext_ref")
        if not isinstance(fulltext, dict):
            raise ReleaseContractError(
                f"{row.get('method_path_id', '?')}: fulltext_ref invalid"
            )
        validate_repo_relative_path(fulltext.get("ledger"), repo_root)
        validate_canonical_record_id(row.get("canonical_record_id"), repo_root)


def _read_exact_json(
    repo_root, path, expected_relative, expected_sha256, label
):
    path = resolve_trusted_repo_path(
        repo_root,
        path,
        expected_relative=expected_relative,
        expected_kind="file",
    )
    try:
        raw = path.read_bytes()
    except OSError as error:
        raise ReleaseContractError(f"{label}: cannot read {path}: {error}") from error
    actual = hashlib.sha256(raw).hexdigest()
    if actual != expected_sha256:
        raise ReleaseContractError(
            f"{label}: SHA-256 mismatch (expected={expected_sha256}, found={actual})"
        )
    try:
        return loads(raw, str(path)), raw
    except JsonContractError as error:
        raise ReleaseContractError(str(error)) from error


def load_active_release(repo_root, sidecar_dir, adjudication_path):
    """Strict-load the exact eight final sidecars and fixed adjudication bytes."""
    repo_root = Path(repo_root)
    sidecar_dir = resolve_trusted_repo_path(
        repo_root,
        sidecar_dir,
        expected_relative=SIDECAR_DIRECTORY_RELATIVE_PATH,
        expected_kind="dir",
    )
    actual_names = tuple(sorted(path.name for path in sidecar_dir.iterdir()))
    if actual_names != FINAL_SIDECAR_NAMES:
        raise ReleaseContractError(
            "active sidecar inventory mismatch "
            f"(expected={list(FINAL_SIDECAR_NAMES)}, found={list(actual_names)})"
        )

    loaded = []
    work_ids = []
    method_ids = []
    for name, expected_work_id in zip(
        FINAL_SIDECAR_NAMES, EXPECTED_WORK_IDS, strict=True
    ):
        sidecar_relative = f"{SIDECAR_DIRECTORY_RELATIVE_PATH}/{name}"
        document, raw = _read_exact_json(
            repo_root,
            sidecar_dir / name,
            sidecar_relative,
            FINAL_SIDECAR_SHA256[name],
            f"active sidecar {name}",
        )
        if not isinstance(document, dict):
            raise ReleaseContractError(f"{name}: sidecar container invalid")
        work_id = document.get("paper_work_id")
        if work_id != expected_work_id:
            raise ReleaseContractError(
                f"{name}: work id mismatch: {work_id!r}"
            )
        rows = document.get("method_paths")
        if not isinstance(rows, list):
            raise ReleaseContractError(f"{name}: method_paths container invalid")
        work_ids.append(work_id)
        method_ids.extend(row.get("method_path_id") for row in rows if isinstance(row, dict))
        _validate_sidecar_lineage(document, repo_root, name)
        loaded.append((name, document, raw))

    if tuple(work_ids) != EXPECTED_WORK_IDS or len(set(work_ids)) != len(work_ids):
        raise ReleaseContractError("active work-id inventory mismatch or duplicate")
    if tuple(sorted(method_ids)) != EXPECTED_METHOD_PATH_IDS or len(set(method_ids)) != len(method_ids):
        raise ReleaseContractError("active method-path inventory mismatch or duplicate")

    adjudication, adjudication_raw = _read_exact_json(
        repo_root,
        adjudication_path,
        ADJUDICATION_RELATIVE_PATH,
        ADJUDICATION_SHA256,
        "active adjudication",
    )
    return ActiveReleaseSnapshot(
        sidecars=tuple(loaded),
        adjudication=adjudication,
        adjudication_raw=adjudication_raw,
        method_path_ids=tuple(sorted(method_ids)),
    )
