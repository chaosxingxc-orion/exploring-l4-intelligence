#!/usr/bin/env python3
"""Trusted fixed-path helpers for generated current-layer artifacts."""

from __future__ import annotations

import os
import re
import stat
import sys
from pathlib import Path, PurePosixPath


REPO = Path(__file__).resolve().parents[2]
CHECKS_DIR = REPO / "scripts" / "checks"
if str(CHECKS_DIR) not in sys.path:
    sys.path.insert(0, str(CHECKS_DIR))

from ai_context_surface_check import ContextSurfaceError, TrustedRepoReader  # noqa: E402
from sf_schema_v3_release_contract import (  # noqa: E402
    ReleaseContractError,
    resolve_trusted_repo_path,
)


class TrustedCurrentPathError(ValueError):
    """A prescribed current-layer path is missing, unsafe, or redirected."""


def _portable_relative(value: str) -> PurePosixPath:
    if not isinstance(value, str) or not value:
        raise TrustedCurrentPathError("expected path must be a nonempty string")
    if "\\" in value or value.startswith("/") or re.match(r"^[A-Za-z]:", value):
        raise TrustedCurrentPathError(f"expected path is not portable: {value!r}")
    parts = value.split("/")
    if any(part in ("", ".", "..") for part in parts):
        raise TrustedCurrentPathError(f"expected path has unsafe component: {value!r}")
    return PurePosixPath(*parts)


def _trusted_root(repo: Path) -> tuple[Path, Path]:
    lexical = Path(os.path.abspath(repo))
    try:
        metadata = os.lstat(lexical)
    except OSError as error:
        raise TrustedCurrentPathError(f"repository root unavailable: {repo}: {error}") from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise TrustedCurrentPathError(f"repository root is not a trusted directory: {repo}")
    try:
        resolved = lexical.resolve(strict=True)
    except OSError as error:
        raise TrustedCurrentPathError(f"repository root does not resolve: {error}") from error
    return lexical, resolved


def _prescribed_target(repo: Path, target: Path, expected_relative: str):
    expected = _portable_relative(expected_relative)
    root_lexical, root_resolved = _trusted_root(Path(repo))
    requested = Path(target)
    if any(part in (".", "..") for part in requested.parts):
        raise TrustedCurrentPathError(f"target contains unsafe component: {target}")
    if not requested.is_absolute():
        requested = root_lexical / requested
    requested = Path(os.path.abspath(requested))
    prescribed = root_lexical.joinpath(*expected.parts)
    if os.path.normcase(str(requested)) != os.path.normcase(str(prescribed)):
        raise TrustedCurrentPathError(
            f"target is not prescribed path {expected_relative}: {target}"
        )
    return expected, root_lexical, root_resolved, prescribed


def resolve_fixed_input(repo: Path, target: Path, expected_relative: str) -> Path:
    """Resolve one existing prescribed regular file without following links."""

    _expected, _lexical, _resolved, prescribed = _prescribed_target(
        repo, target, expected_relative
    )
    try:
        return resolve_trusted_repo_path(
            repo,
            prescribed,
            expected_relative=expected_relative,
            expected_kind="file",
        )
    except ReleaseContractError as error:
        raise TrustedCurrentPathError(str(error)) from error


def resolve_fixed_output(
    repo: Path,
    target: Path,
    expected_relative: str,
    *,
    allow_missing_leaf: bool,
) -> Path:
    """Validate an exact output target and every component without links.

    Write mode may omit only the final leaf.  Every parent must already exist
    as a real directory; check mode also requires a regular existing leaf.
    """

    expected, root, root_resolved, prescribed = _prescribed_target(
        repo, target, expected_relative
    )
    current = root
    for part in expected.parts[:-1]:
        current /= part
        try:
            metadata = os.lstat(current)
        except OSError as error:
            raise TrustedCurrentPathError(
                f"output parent unavailable: {current}: {error}"
            ) from error
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise TrustedCurrentPathError(f"output parent is untrusted: {current}")
        try:
            resolved = current.resolve(strict=True)
            resolved.relative_to(root_resolved)
        except (OSError, ValueError) as error:
            raise TrustedCurrentPathError(
                f"output parent escapes repository: {current}"
            ) from error

    try:
        metadata = os.lstat(prescribed)
    except FileNotFoundError:
        if allow_missing_leaf:
            return prescribed
        raise TrustedCurrentPathError(f"output leaf missing: {expected_relative}")
    except OSError as error:
        raise TrustedCurrentPathError(f"output leaf unavailable: {prescribed}: {error}") from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise TrustedCurrentPathError(f"output leaf is not a trusted regular file: {prescribed}")
    try:
        resolved = prescribed.resolve(strict=True)
        resolved.relative_to(root_resolved)
    except (OSError, ValueError) as error:
        raise TrustedCurrentPathError(f"output leaf escapes repository: {prescribed}") from error
    return prescribed


def read_fixed_bytes(repo: Path, target: Path, expected_relative: str) -> bytes:
    """Read exact prescribed bytes through the race-aware trusted reader."""

    resolve_fixed_input(repo, target, expected_relative)
    try:
        return TrustedRepoReader(repo).read_bytes(expected_relative)
    except ContextSurfaceError as error:
        raise TrustedCurrentPathError(str(error)) from error
