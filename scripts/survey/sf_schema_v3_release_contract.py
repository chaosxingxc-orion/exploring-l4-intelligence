"""Exact active schema-v3 release inventory and safe lineage-path contract."""
from __future__ import annotations

import hashlib
import re
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
        "9d60a55dffc0112a4c8eb38aeebe7ea5daf3815d035aaa558812fc86e57911bb"
    ),
    "2026.findings-acl.1724.sidecar.json": (
        "eb96a83e2eadea96db2af2b1690feb1cfd2792354758adb127649892689839f9"
    ),
    "2026.findings-acl.511.sidecar.json": (
        "2d97b5ca3d441189d8d8c57eb43b47c09b36c7860f16e54dae6daac2dc957404"
    ),
    "2602.16485.sidecar.json": (
        "b4201e535f7dbea0cee9f92d506c9e8ecd80b031d7f9aa3608e8e5085a68950f"
    ),
    "2604.16529.sidecar.json": (
        "f946ebd1c50bb117bd787641679e0031a468b8c4c6a46712fd735360e0ce3de9"
    ),
    "2605.08083.sidecar.json": (
        "c9afb44081e80182c00194f18ffda8c79706075043c711aa8d1219145367bc6e"
    ),
    "2606.01667.sidecar.json": (
        "82056e0957c85d95c1bf4d772af82a2db3ba3d2017f607ae9309bd7c83099d69"
    ),
    "2606.03054.sidecar.json": (
        "f5ba2c5c68e72b4f1737fc79d63f0a61423ae5cd2a4886d54e79f1d8a00c1e1b"
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


def validate_repo_relative_path(
    value,
    repo_root,
    *,
    allowed_root=Path("wiki/survey"),
):
    """Resolve one POSIX repo-relative, existing, non-symlink file path."""
    if not isinstance(value, str) or not value:
        raise ReleaseContractError("lineage path must be a non-empty string")
    if "\\" in value or re.match(r"^[A-Za-z]:", value):
        raise ReleaseContractError(f"lineage path is not portable POSIX: {value!r}")
    raw_parts = value.split("/")
    if any(part in ("", ".", "..") for part in raw_parts):
        raise ReleaseContractError(f"lineage path contains unsafe component: {value!r}")
    pure = PurePosixPath(value)
    if pure.is_absolute():
        raise ReleaseContractError(f"lineage path must be repo-relative: {value!r}")

    allowed_pure = PurePosixPath(allowed_root.as_posix())
    try:
        pure.relative_to(allowed_pure)
    except ValueError as error:
        raise ReleaseContractError(
            f"lineage path is outside allowed root {allowed_pure}: {value!r}"
        ) from error

    repo_root = Path(repo_root).resolve()
    candidate = repo_root
    for part in pure.parts:
        candidate = candidate / part
        if candidate.is_symlink():
            raise ReleaseContractError(
                f"lineage path contains symlink component: {value!r}"
            )
    try:
        resolved = candidate.resolve(strict=True)
        allowed_resolved = (repo_root / Path(*allowed_pure.parts)).resolve(strict=True)
    except OSError as error:
        raise ReleaseContractError(
            f"lineage path does not resolve to an existing file: {value!r}: {error}"
        ) from error
    if not _within(resolved, allowed_resolved) or not resolved.is_file():
        raise ReleaseContractError(
            f"lineage path escapes allowed root or is not a file: {value!r}"
        )
    return resolved


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


def _read_exact_json(path, expected_sha256, label):
    path = Path(path)
    if path.is_symlink():
        raise ReleaseContractError(f"{label}: symlink input is forbidden: {path}")
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
    sidecar_dir = Path(sidecar_dir)
    if sidecar_dir.is_symlink() or not sidecar_dir.is_dir():
        raise ReleaseContractError(
            f"active sidecar directory invalid or symlinked: {sidecar_dir}"
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
        document, raw = _read_exact_json(
            sidecar_dir / name,
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
        adjudication_path,
        ADJUDICATION_SHA256,
        "active adjudication",
    )
    return ActiveReleaseSnapshot(
        sidecars=tuple(loaded),
        adjudication=adjudication,
        adjudication_raw=adjudication_raw,
        method_path_ids=tuple(sorted(method_ids)),
    )
