#!/usr/bin/env python3
"""Build the deterministic, bounded AI context manifest.

This builder intentionally owns exact paths.  It has no wildcard or directory
grandfathering mechanism: additions require a reviewed constant change.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath

from ai_context_inventory import (
    ARCHIVE_TRANSITIONS,
    REGISTRY_BASELINE_COUNT,
    REGISTRY_BASELINE_PREFIX_SHA256,
    registry_prefix_sha256,
)
from ai_context_surface_check import (
    MANIFEST_RELATIVE_PATH,
    MANIFEST_SCHEMA,
    PENDING_ARCHIVE_PATHS,
    ContextSurfaceError,
    TrustedRepoReader,
    classify_path,
    git_command_prefix,
    loads_json_strict,
    validate_audit_epoch_state,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = REPO_ROOT / MANIFEST_RELATIVE_PATH
AUDIT_CAMPAIGN_INDEX_PATH = "wiki/audit/system-first-stage1a/INDEX.md"
ACTIVE_REVIEW_TRANSACTION = (
    "wiki/audit/system-first-stage1a/round-12/stage1a-readiness-correction.md"
)
ENTRY_SPECS_DATA_PATH = REPO_ROOT / "docs" / "integrity" / "ai-context-entry-specs.json"
ENTRY_SPECS_DATA_SCHEMA = "ai-context-entry-specs-v1"


def _entry(path: str, path_class: str, load_policy: str, purpose: str):
    return {
        "path": path,
        "class": path_class,
        "load_policy": load_policy,
        "purpose": purpose,
    }


class EntrySpecsDataError(ValueError):
    """Raised when the externalized active-entry/budget table is missing or malformed."""


def _require_nonempty_str(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise EntrySpecsDataError(f"{label} must be a non-empty string")
    return value


def load_entry_specs_data(
    path: Path = ENTRY_SPECS_DATA_PATH,
) -> tuple[tuple[dict, ...], dict]:
    """Strict-load the externalized ACTIVE_ENTRY_SPECS / BUDGETS_BYTES tables.

    Fails closed: any missing file, invalid strict-JSON bytes, schema
    mismatch, or wrong-shaped row raises ``EntrySpecsDataError`` rather than
    silently returning a partial or empty table.
    """
    try:
        raw = path.read_bytes()
    except OSError as error:
        raise EntrySpecsDataError(f"cannot read {path}: {error}") from error
    try:
        document = loads_json_strict(raw, str(path))
    except ContextSurfaceError as error:
        raise EntrySpecsDataError(f"{path}: {error}") from error
    if not isinstance(document, dict) or set(document) != {
        "schema",
        "active_entries",
        "budgets_bytes",
    }:
        raise EntrySpecsDataError(f"{path}: unexpected top-level schema")
    if document["schema"] != ENTRY_SPECS_DATA_SCHEMA:
        raise EntrySpecsDataError(
            f"{path}: expected schema {ENTRY_SPECS_DATA_SCHEMA!r}, "
            f"found {document['schema']!r}"
        )

    entries_raw = document["active_entries"]
    if not isinstance(entries_raw, list) or not entries_raw:
        raise EntrySpecsDataError(f"{path}: active_entries must be a non-empty list")
    entries = []
    for index, item in enumerate(entries_raw):
        label = f"{path}: active_entries[{index}]"
        if not isinstance(item, dict) or set(item) != {
            "path",
            "class",
            "load_policy",
            "purpose",
        }:
            raise EntrySpecsDataError(
                f"{label} must have exact path/class/load_policy/purpose fields"
            )
        entries.append(
            _entry(
                _require_nonempty_str(item["path"], f"{label}.path"),
                _require_nonempty_str(item["class"], f"{label}.class"),
                _require_nonempty_str(item["load_policy"], f"{label}.load_policy"),
                _require_nonempty_str(item["purpose"], f"{label}.purpose"),
            )
        )
    if entries[-1]["path"] != MANIFEST_RELATIVE_PATH:
        raise EntrySpecsDataError(
            f"{path}: final active_entries row must be the self manifest entry "
            f"{MANIFEST_RELATIVE_PATH!r}, found {entries[-1]['path']!r}"
        )

    budgets_raw = document["budgets_bytes"]
    if not isinstance(budgets_raw, dict) or not budgets_raw:
        raise EntrySpecsDataError(f"{path}: budgets_bytes must be a non-empty object")
    budgets: dict[str, int] = {}
    for raw_key, limit in budgets_raw.items():
        key_label = f"{path}: budgets_bytes key {raw_key!r}"
        key = _require_nonempty_str(raw_key, key_label)
        if isinstance(limit, bool) or not isinstance(limit, int) or limit <= 0:
            raise EntrySpecsDataError(f"{path}: budgets_bytes[{key!r}] must be a positive integer")
        budgets[key] = limit

    return tuple(entries), budgets


ACTIVE_ENTRY_SPECS, BUDGETS_BYTES = load_entry_specs_data()


AUDIT_CAMPAIGN_ENTRY_SPEC = _entry(
    AUDIT_CAMPAIGN_INDEX_PATH,
    "HOT",
    "targeted",
    "append-only campaign audit index",
)


def _legacy(path: str, path_class: str):
    return {"path": path, "class": path_class}


# Emptied 2026-07-29: legacy cold layer retired under the owner delete-to-the-maximum
# ruling; rows and recovery commands live in
# wiki/audit/md-script-consolidation-2026-07-29/sunset-ledger.jsonl.
EXACT_NAMED_LEGACY_EXCEPTIONS = ()


# Emptied 2026-08-03: the Stage-1 survey package closed. The two gate-bound
# survivors (protocol-v1, bibliography-v1) and amendments 1-8 moved to
# wiki/archive/working/system-first-stage1a/ with their consumers retired;
# resolution notes live in the closure digest at
# wiki/archive/working/system-first-survey-current/.
RETAINED_LEGACY_PATHS = ()


# Emptied 2026-07-29 (same ruling; registered files went through registry sunset rows).
_PREEXISTING_AUDIT_DOC_PATHS = ()

_PREEXISTING_REGISTRY_DOC_PATHS = (
    # Sole retained legacy document (owner ruling 2026-07-18(2): historical
    # experiments are never deleted, downgraded, or pretended away). This is the
    # canonical carrier of the inherited-prior-exposure union that every future
    # held-out/preregistration design must consult.
    "wiki/2026-07-18-inherited-prior-exposure-union.md",
)

# Fixed inventory only: no filesystem scan contributes paths to this tuple.
EXACT_PREEXISTING_LEGACY_DOCS = tuple(
    {
        "path": path,
        "class": "AUDIT_LEGACY",
        "reason": "pre-routing dated audit/report document retained cold at its tracked path",
    }
    for path in _PREEXISTING_AUDIT_DOC_PATHS
) + tuple(
    {
        "path": path,
        "class": "REGISTRY_LEGACY",
        "reason": "pre-routing research/survey document retained cold pending lifecycle cleanup",
    }
    for path in _PREEXISTING_REGISTRY_DOC_PATHS
)

BLOB_RE = re.compile(r"[0-9a-f]{40}\Z")
REGULAR_INDEX_MODES = {"100644", "100755"}
DEFAULT_PATHS = {
    "AGENTS.md",
    "wiki/Research-Objective.md",
    "wiki/Project-Thesis.md",
}


class ManifestBuildError(RuntimeError):
    """Controlled manifest builder failure."""


def _fail(code: str, detail: str):
    raise ManifestBuildError(f"{code}: {detail}")


def _canonical_path(value, label: str) -> str:
    if not isinstance(value, str) or not value or value in {".", ".."}:
        _fail("invalid-path", f"{label} must be a non-empty path")
    if "\\" in value or value.startswith("/") or re.match(r"^[A-Za-z]:", value):
        _fail("invalid-path", f"{label} must be repo-relative POSIX: {value!r}")
    path = PurePosixPath(value)
    if any(part in {"", ".", ".."} for part in path.parts) or path.as_posix() != value:
        _fail("invalid-path", f"{label} must be canonical repo-relative POSIX: {value!r}")
    return value


AUDIT_REGISTRY_RELATIVE_PATH = "wiki/survey/sf-audit-artifact-registry.json"
INVENTORY_ANCHOR_RELATIVE_PATH = "scripts/checks/ai_context_inventory.py"


def _validate_inventory_anchor(graph: Stage0Graph) -> None:
    """Bind the imported registry constants to the exact staged source bytes."""

    raw = graph.raw(INVENTORY_ANCHOR_RELATIVE_PATH, "inventory-anchor-untracked")
    try:
        text = raw.decode("utf-8")
        module = ast.parse(text, filename=INVENTORY_ANCHOR_RELATIVE_PATH)
    except (UnicodeDecodeError, SyntaxError) as exc:
        _fail("inventory-anchor-invalid", str(exc))
    names = {
        "REGISTRY_BASELINE_COUNT",
        "REGISTRY_BASELINE_PREFIX_SHA256",
    }
    values: dict[str, object] = {}
    for node in module.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Name) or target.id not in names:
            continue
        if target.id in values or not isinstance(node.value, ast.Constant):
            _fail("inventory-anchor-invalid", f"{target.id}: one literal assignment required")
        values[target.id] = node.value.value
    if set(values) != names:
        _fail("inventory-anchor-invalid", f"missing exact constants: {sorted(names - set(values))}")
    count = values["REGISTRY_BASELINE_COUNT"]
    prefix_sha256 = values["REGISTRY_BASELINE_PREFIX_SHA256"]
    if (
        isinstance(count, bool)
        or not isinstance(count, int)
        or count <= 0
        or not isinstance(prefix_sha256, str)
        or re.fullmatch(r"[0-9a-f]{64}", prefix_sha256) is None
    ):
        _fail("inventory-anchor-invalid", "count/hash literal types or values")
    if count != REGISTRY_BASELINE_COUNT or prefix_sha256 != REGISTRY_BASELINE_PREFIX_SHA256:
        _fail(
            "inventory-anchor-constant-mismatch",
            f"staged source ({count}, {prefix_sha256}) != imported "
            f"({REGISTRY_BASELINE_COUNT}, {REGISTRY_BASELINE_PREFIX_SHA256})",
        )


def _load_audit_inventory(
    graph: Stage0Graph,
    registry_path: str,
) -> tuple[list[dict[str, str]], dict[str, str]]:
    try:
        registry_raw = graph.raw(registry_path, "audit-registry-untracked")
        registry = loads_json_strict(registry_raw, registry_path)
    except ContextSurfaceError as exc:
        _fail("audit-registry-invalid", str(exc))
    if not isinstance(registry, dict) or not isinstance(registry.get("artifacts"), list):
        _fail("audit-registry-invalid", "artifacts must be a list")
    artifacts = registry["artifacts"]
    if len(artifacts) < REGISTRY_BASELINE_COUNT:
        _fail(
            "audit-registry-baseline-short",
            f"expected at least {REGISTRY_BASELINE_COUNT} artifacts, found {len(artifacts)}",
        )
    seen: set[str] = set()
    validated: list[tuple[str, str]] = []
    for index, artifact in enumerate(artifacts):
        if not isinstance(artifact, dict) or set(artifact) != {"path", "git_blob"}:
            _fail(
                "audit-registry-entry",
                f"artifacts[{index}] must have exact path/git_blob fields",
            )
        path = _canonical_path(artifact["path"], f"artifacts[{index}].path")
        blob = artifact["git_blob"]
        if not isinstance(blob, str) or BLOB_RE.fullmatch(blob) is None:
            _fail("audit-registry-entry", f"artifacts[{index}].git_blob is not a Git blob id")
        if path in seen:
            _fail("duplicate-path", f"audit registry path {path}")
        if index >= REGISTRY_BASELINE_COUNT and not path.startswith("wiki/audit/"):
            _fail("audit-registry-extra-path", path)
        seen.add(path)
        validated.append((path, blob))

    if len(artifacts) > REGISTRY_BASELINE_COUNT:
        _fail(
            "audit-registry-unanchored-append",
            f"found {len(artifacts)} rows but immutable anchor covers "
            f"{REGISTRY_BASELINE_COUNT}",
        )
    actual_prefix_hash = registry_prefix_sha256(artifacts, REGISTRY_BASELINE_COUNT)
    if actual_prefix_hash != REGISTRY_BASELINE_PREFIX_SHA256:
        _fail(
            "audit-registry-prefix-mismatch",
            f"{actual_prefix_hash} != {REGISTRY_BASELINE_PREFIX_SHA256}",
        )

    sunset_map = _load_registry_sunset(registry, dict(validated), registry_path)

    legacy: list[dict[str, str]] = []
    for path, blob in validated:
        if path in sunset_map:
            # Working-tree deletion recorded by a sunset ledger row: the
            # registered pin is intentionally no longer present at this path,
            # so it is exempt from the presence check and does not surface as
            # a legacy_cold_path (it is gone, not cold-retained).
            continue
        graph.raw(path, "audit-registry-path-untracked")
        if graph.blobs.get(path) != blob:
            _fail(
                "audit-registry-blob-mismatch",
                f"{path}: inventory {graph.blobs.get(path)!r} != pinned {blob!r}",
            )
        if not path.startswith("wiki/audit/"):
            legacy.append(_legacy(path, "AUDIT_LEGACY"))
    return legacy, dict(validated)


def _load_registry_sunset(
    registry: dict,
    pins: dict[str, str],
    registry_path: str,
) -> dict[str, str]:
    """Parse append-only sunset exemptions and bind each to its registered pin.

    A sunset row records that a registered artifact's bytes were deleted from
    the working tree with its history preserved (`git show <last_commit>:
    <path>`).  It never mutates the original `artifacts` row; it only exempts
    that path from the disk-presence requirement below.
    """

    raw_sunset = registry.get("sunset", [])
    if not isinstance(raw_sunset, list):
        _fail("audit-registry-sunset-invalid", f"{registry_path}: sunset must be a list")
    sunset_map: dict[str, str] = {}
    for index, entry in enumerate(raw_sunset):
        label = f"{registry_path} sunset[{index}]"
        if not isinstance(entry, dict) or set(entry) != {"path", "git_blob", "last_commit"}:
            _fail(
                "audit-registry-sunset-entry",
                f"{label} must have exact path/git_blob/last_commit fields",
            )
        path = _canonical_path(entry["path"], f"{label}.path")
        blob = entry["git_blob"]
        commit = entry["last_commit"]
        if not isinstance(blob, str) or BLOB_RE.fullmatch(blob) is None:
            _fail("audit-registry-sunset-entry", f"{label}.git_blob is not a Git blob id")
        if not isinstance(commit, str) or BLOB_RE.fullmatch(commit) is None:
            _fail("audit-registry-sunset-entry", f"{label}.last_commit is not a Git commit id")
        if path not in pins:
            _fail("audit-registry-sunset-unregistered", f"{label}: {path}")
        if pins[path] != blob:
            _fail("audit-registry-sunset-blob-mismatch", f"{label}: {path}")
        if path in sunset_map:
            _fail("duplicate-path", f"sunset path {path}")
        sunset_map[path] = blob
    return sunset_map


def _validate_constants(specs, *legacy_groups, budgets, active_review):
    if len(specs) > 30:
        _fail("active-entry-budget-exceeded", f"{len(specs)} active entries exceeds 30")
    active_seen: set[str] = set()
    defaults: set[str] = set()
    for index, spec in enumerate(specs):
        if not isinstance(spec, dict) or set(spec) != {
            "path",
            "class",
            "load_policy",
            "purpose",
        }:
            _fail("manifest-entry-invalid", f"ACTIVE_ENTRY_SPECS[{index}] has wrong keys")
        path = _canonical_path(spec["path"], f"ACTIVE_ENTRY_SPECS[{index}].path")
        if any(token in path for token in "*?["):
            _fail("manifest-entry-invalid", f"{path}: wildcard forbidden")
        if path in active_seen:
            _fail("duplicate-path", f"active constant {path}")
        active_seen.add(path)
        if spec["load_policy"] not in {"default", "targeted"}:
            _fail("manifest-entry-invalid", f"{path}: invalid load_policy")
        if not isinstance(spec["purpose"], str) or not spec["purpose"].strip():
            _fail("manifest-entry-invalid", f"{path}: empty purpose")
        if spec["load_policy"] == "default":
            defaults.add(path)
    if defaults != DEFAULT_PATHS:
        _fail(
            "default-load-surface-invalid",
            f"expected {sorted(DEFAULT_PATHS)}, found {sorted(defaults)}",
        )

    retained_seen: set[str] = set()
    legacy_entries = [entry for group in legacy_groups for entry in group]
    for index, entry in enumerate(legacy_entries):
        if not isinstance(entry, dict):
            _fail("legacy-entry-invalid", f"legacy constant [{index}] must be an object")
        allowed_keys = (
            {"path", "class", "reason"} if "reason" in entry else {"path", "class"}
        )
        if not isinstance(entry, dict) or set(entry) != allowed_keys:
            _fail("legacy-entry-invalid", f"legacy constant [{index}] has wrong keys")
        path = _canonical_path(entry["path"], f"legacy constant [{index}].path")
        if entry["class"] not in {
            "AUDIT_LEGACY",
            "REGISTRY_LEGACY",
            "PENDING_ARCHIVE",
        }:
            _fail("legacy-entry-invalid", f"{path}: invalid class")
        if "reason" in entry and (
            not isinstance(entry["reason"], str) or not entry["reason"].strip()
        ):
            _fail("legacy-entry-invalid", f"{path}: empty reason")
        if any(token in path for token in "*?["):
            _fail("legacy-entry-invalid", f"{path}: wildcard forbidden")
        if path in active_seen:
            _fail("active-legacy-overlap", path)
        try:
            actual_class = classify_path(
                path, [{"path": path, "class": entry["class"]}]
            )
        except ContextSurfaceError as exc:
            _fail("legacy-class-mismatch", str(exc))
        if actual_class != entry["class"]:
            _fail(
                "legacy-class-mismatch",
                f"{path}: declared {entry['class']}, classified {actual_class}",
            )
        if path in retained_seen:
            _fail("duplicate-path", f"retained legacy constant {path}")
        retained_seen.add(path)

    if not isinstance(budgets, dict):
        _fail("budget-constant-invalid", "BUDGETS_BYTES must be an object")
    for raw_path, limit in budgets.items():
        path = _canonical_path(raw_path, "BUDGETS_BYTES path")
        if any(token in path for token in "*?["):
            _fail("budget-constant-invalid", f"{path}: wildcard forbidden")
        if isinstance(limit, bool) or not isinstance(limit, int) or limit <= 0:
            _fail("budget-constant-invalid", f"{path}: limit must be a positive integer")

    if active_review is not None:
        path = _canonical_path(active_review, "ACTIVE_REVIEW_TRANSACTION")
        if any(token in path for token in "*?["):
            _fail("active-review-constant-invalid", f"{path}: wildcard forbidden")


def _git_blob_id(raw: bytes) -> str:
    header = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(header + raw).hexdigest()


class Stage0Graph:
    """Trusted stage-0 graph whose relevant blobs equal trusted worktree bytes."""

    def __init__(self, repo: Path, index_inventory, read_blob):
        if not isinstance(index_inventory, dict):
            _fail("index-inventory-invalid", "index_inventory must be an object")
        if not callable(read_blob):
            _fail("index-blob-reader-invalid", "read_blob must be callable")
        try:
            self.reader = TrustedRepoReader(repo)
        except ContextSurfaceError as exc:
            _fail("repo-root-invalid", str(exc))
        self.index: dict[str, dict[str, object]] = {}
        for raw_path, entry in index_inventory.items():
            path = _canonical_path(raw_path, "index_inventory key")
            if path in self.index:
                _fail("duplicate-path", f"index path {path}")
            if not isinstance(entry, dict) or set(entry) != {"mode", "blob", "stage"}:
                _fail(
                    "index-entry-invalid",
                    f"{path}: expected exact mode/blob/stage fields",
                )
            mode = entry["mode"]
            blob = entry["blob"]
            stage = entry["stage"]
            if stage != 0:
                _fail("index-entry-not-stage-0", f"{path}: stage={stage!r}")
            if mode not in REGULAR_INDEX_MODES:
                _fail("index-entry-not-regular", f"{path}: mode={mode!r}")
            if not isinstance(blob, str) or BLOB_RE.fullmatch(blob) is None:
                _fail("index-entry-invalid", f"{path}: invalid blob {blob!r}")
            self.index[path] = {"mode": mode, "blob": blob, "stage": 0}
        self._read_blob = read_blob
        self._blob_cache: dict[str, bytes] = {}
        self._path_cache: dict[str, bytes] = {}

    @property
    def tracked(self) -> set[str]:
        return set(self.index)

    @property
    def blobs(self) -> dict[str, str]:
        return {path: str(entry["blob"]) for path, entry in self.index.items()}

    def raw(self, path: str, untracked_code: str) -> bytes:
        path = _canonical_path(path, "stage-0 graph path")
        if path in self._path_cache:
            return self._path_cache[path]
        entry = self.index.get(path)
        if entry is None:
            _fail(untracked_code, path)
        blob = str(entry["blob"])
        if blob not in self._blob_cache:
            try:
                raw = self._read_blob(blob)
            except Exception as exc:
                _fail("index-blob-read-failed", f"{path}: {blob}: {exc}")
            if not isinstance(raw, bytes):
                _fail("index-blob-invalid", f"{path}: read_blob did not return bytes")
            actual_blob = _git_blob_id(raw)
            if actual_blob != blob:
                _fail(
                    "index-blob-id-mismatch",
                    f"{path}: cat-file bytes hash {actual_blob} != {blob}",
                )
            self._blob_cache[blob] = raw
        staged_raw = self._blob_cache[blob]
        try:
            worktree_raw = self.reader.read_bytes(path)
        except ContextSurfaceError as exc:
            if str(exc).startswith("repo-path-missing:"):
                _fail("index-worktree-missing", path)
            _fail("index-worktree-invalid", str(exc))
        if worktree_raw != staged_raw:
            _fail(
                "index-worktree-mismatch",
                f"{path}: staged {hashlib.sha256(staged_raw).hexdigest()} != "
                f"worktree {hashlib.sha256(worktree_raw).hexdigest()}",
            )
        self._path_cache[path] = staged_raw
        return staged_raw


def _audit_activation(graph: Stage0Graph):
    """Activate the audit pointer only from the complete tracked path pair."""

    if ACTIVE_REVIEW_TRANSACTION is None:
        return (), None
    index_tracked = AUDIT_CAMPAIGN_INDEX_PATH in graph.tracked
    correction_tracked = ACTIVE_REVIEW_TRANSACTION in graph.tracked
    if index_tracked != correction_tracked:
        _fail(
            "audit-activation-incomplete",
            f"index tracked={index_tracked}, correction tracked={correction_tracked}",
        )
    if not index_tracked:
        return (), None
    graph.raw(AUDIT_CAMPAIGN_INDEX_PATH, "audit-activation-untracked")
    graph.raw(ACTIVE_REVIEW_TRANSACTION, "audit-activation-untracked")
    return (AUDIT_CAMPAIGN_ENTRY_SPEC,), ACTIVE_REVIEW_TRANSACTION


def _archive_transition(
    graph: Stage0Graph,
):
    """Resolve the seven-file archive lifecycle from one complete Git state."""

    if not ARCHIVE_TRANSITIONS:
        return ()
    if len(ARCHIVE_TRANSITIONS) != 7:
        _fail("archive-transition-constant-invalid", "expected exactly seven transitions")
    sources: set[str] = set()
    destinations: set[str] = set()
    for index, transition in enumerate(ARCHIVE_TRANSITIONS):
        if not isinstance(transition, dict) or set(transition) != {
            "source",
            "destination",
            "git_blob",
        }:
            _fail("archive-transition-constant-invalid", f"transition[{index}] fields")
        source = _canonical_path(transition["source"], f"transition[{index}].source")
        destination = _canonical_path(
            transition["destination"], f"transition[{index}].destination"
        )
        blob = transition["git_blob"]
        if source not in PENDING_ARCHIVE_PATHS:
            _fail("archive-transition-constant-invalid", f"unexpected source {source}")
        if not destination.startswith(
            "wiki/archive/working/system-first-stage1a/amendments/"
        ):
            _fail(
                "archive-transition-constant-invalid",
                f"unexpected destination {destination}",
            )
        if not isinstance(blob, str) or BLOB_RE.fullmatch(blob) is None:
            _fail("archive-transition-constant-invalid", f"invalid blob for {source}")
        if source in sources or destination in destinations:
            _fail("archive-transition-constant-invalid", "duplicate source/destination")
        sources.add(source)
        destinations.add(destination)

    tracked_sources = sources & graph.tracked
    tracked_destinations = destinations & graph.tracked
    prearchive = tracked_sources == sources and not tracked_destinations
    archived = not tracked_sources and tracked_destinations == destinations
    if not (prearchive or archived):
        _fail(
            "archive-transition-incomplete",
            f"sources={len(tracked_sources)}/7, destinations={len(tracked_destinations)}/7",
        )

    selected_key = "source" if prearchive else "destination"
    for transition in ARCHIVE_TRANSITIONS:
        path = transition[selected_key]
        expected_blob = transition["git_blob"]
        if graph.blobs.get(path) != expected_blob:
            _fail(
                "archive-transition-blob-mismatch",
                f"{path}: {graph.blobs.get(path)!r} != {expected_blob!r}",
            )
        graph.raw(path, "archive-transition-path-untracked")

    if archived:
        return ()
    return tuple(
        {
            "path": transition["source"],
            "class": "PENDING_ARCHIVE",
            "reason": (
                "Task 6 exact amendment move candidate; remove after byte-preserving "
                "archive move"
            ),
        }
        for transition in ARCHIVE_TRANSITIONS
    )


def _manifest_target(repo: Path, target: Path) -> Path:
    """Require the one canonical manifest target; never follow a target symlink."""

    try:
        root = Path(repo).resolve(strict=True)
    except OSError as exc:
        _fail("manifest-target-invalid", str(exc))
    candidate = Path(target)
    if not candidate.is_absolute():
        candidate = root / candidate
    candidate = Path(os.path.abspath(candidate))
    expected = root.joinpath(*PurePosixPath(MANIFEST_RELATIVE_PATH).parts)
    if os.path.normcase(str(candidate)) != os.path.normcase(str(expected)):
        _fail("manifest-target-invalid", f"expected {expected}, found {candidate}")
    current = root
    try:
        for part in PurePosixPath(MANIFEST_RELATIVE_PATH).parts[:-1]:
            current /= part
            metadata = os.lstat(current)
            if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
                _fail("manifest-target-invalid", f"untrusted parent {current}")
        try:
            metadata = os.lstat(expected)
        except FileNotFoundError:
            pass
        else:
            if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
                _fail("manifest-target-invalid", f"untrusted target {expected}")
    except FileNotFoundError:
        pass
    except OSError as exc:
        _fail("manifest-target-invalid", str(exc))
    return expected


def build_manifest(
    repo: Path,
    index_inventory,
    read_blob,
    registry_path: str = AUDIT_REGISTRY_RELATIVE_PATH,
    *,
    allow_untracked_self: bool = False,
    verify_tracked_self: bool = True,
) -> dict:
    graph = Stage0Graph(Path(repo), index_inventory, read_blob)
    _validate_inventory_anchor(graph)
    audit_specs, active_review_transaction = _audit_activation(graph)
    archive_legacy = _archive_transition(graph)
    _validate_constants(
        (*ACTIVE_ENTRY_SPECS, AUDIT_CAMPAIGN_ENTRY_SPEC),
        RETAINED_LEGACY_PATHS,
        EXACT_NAMED_LEGACY_EXCEPTIONS,
        EXACT_PREEXISTING_LEGACY_DOCS,
        archive_legacy,
        budgets=BUDGETS_BYTES,
        active_review=ACTIVE_REVIEW_TRANSACTION,
    )
    registry_legacy, registered_audit_blobs = _load_audit_inventory(
        graph,
        _canonical_path(registry_path, "registry_path"),
    )
    legacy_by_path: dict[str, dict[str, str]] = {}
    for entry in (
        *registry_legacy,
        *RETAINED_LEGACY_PATHS,
        *EXACT_NAMED_LEGACY_EXCEPTIONS,
        *EXACT_PREEXISTING_LEGACY_DOCS,
        *archive_legacy,
    ):
        path = entry["path"]
        if path in legacy_by_path:
            _fail("duplicate-path", f"legacy inventory overlap {path}")
        graph.raw(path, "legacy-path-untracked")
        legacy_by_path[path] = {"path": path, "class": entry["class"]}
    legacy = [legacy_by_path[path] for path in sorted(legacy_by_path)]
    effective_specs = (*ACTIVE_ENTRY_SPECS, *audit_specs)
    active_paths = {entry["path"] for entry in effective_specs}
    overlap = sorted(active_paths & set(legacy_by_path))
    if overlap:
        _fail("active-legacy-overlap", overlap[0])
    for entry in legacy:
        try:
            actual_class = classify_path(entry["path"], [entry])
        except ContextSurfaceError as exc:
            _fail("legacy-class-mismatch", str(exc))
        if actual_class != entry["class"]:
            _fail(
                "legacy-class-mismatch",
                f"{entry['path']}: declared {entry['class']}, classified {actual_class}",
            )

    entries: list[dict] = []
    for spec in effective_specs:
        entry = dict(spec)
        path = entry["path"]
        actual_class = classify_path(path, legacy)
        if actual_class != entry["class"]:
            _fail(
                "active-class-mismatch",
                f"{path}: declared {entry['class']}, classified {actual_class}",
            )
        is_untracked_self = path == MANIFEST_RELATIVE_PATH and path not in graph.tracked
        if is_untracked_self and not allow_untracked_self:
            _fail("active-path-untracked", path)
        if path != MANIFEST_RELATIVE_PATH:
            raw = graph.raw(path, "active-path-untracked")
            entry["sha256"] = hashlib.sha256(raw).hexdigest()
        elif path in graph.tracked and verify_tracked_self:
            graph.raw(path, "active-path-untracked")
        elif path in graph.tracked:
            try:
                graph.reader.read_bytes(path)
            except ContextSurfaceError as exc:
                _fail("active-path-invalid", str(exc))
        entries.append(entry)

    for path in BUDGETS_BYTES:
        graph.raw(path, "budget-path-untracked")

    # Both guides affect the normalized client surface even though only the
    # current client's guide is a default manifest entry.
    for path in ("AGENTS.md", "CLAUDE.md"):
        graph.raw(path, "agent-guide-untracked")

    document = {
        "schema": MANIFEST_SCHEMA,
        "active_entries": entries,
        "budgets_bytes": dict(sorted(BUDGETS_BYTES.items())),
        "legacy_cold_paths": legacy,
        "active_review_transaction": active_review_transaction,
    }
    epoch_failures = validate_audit_epoch_state(
        document,
        sorted(graph.tracked),
        registered_audit_blobs,
        lambda path: graph.raw(path, "audit-epoch-path-untracked"),
    )
    if epoch_failures:
        code, separator, detail = epoch_failures[0].partition(": ")
        _fail(code, detail if separator else epoch_failures[0])
    return document


def render_manifest(
    repo: Path,
    index_inventory,
    read_blob,
    registry_path: str = AUDIT_REGISTRY_RELATIVE_PATH,
    *,
    allow_untracked_self: bool = False,
    verify_tracked_self: bool = True,
) -> bytes:
    document = build_manifest(
        Path(repo),
        index_inventory,
        read_blob,
        registry_path,
        allow_untracked_self=allow_untracked_self,
        verify_tracked_self=verify_tracked_self,
    )
    raw = (json.dumps(document, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if b"\\" in raw:
        _fail("manifest-render-invalid", "backslash found in rendered bytes")
    return raw


def write_manifest(
    repo: Path,
    target: Path,
    index_inventory,
    read_blob,
    registry_path: str = AUDIT_REGISTRY_RELATIVE_PATH,
) -> None:
    target = _manifest_target(Path(repo), Path(target))
    raw = render_manifest(
        repo,
        index_inventory,
        read_blob,
        registry_path,
        # Bootstrap only: the builder is about to create the exact self file
        # before the caller can add it to the Git index.
        allow_untracked_self=True,
        # Write mode intentionally replaces a dirty/tracked self; the caller
        # must stage the generated bytes before --check can pass.
        verify_tracked_self=False,
    )
    file_descriptor: int | None = None
    temporary_name: str | None = None
    failure: OSError | None = None
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        file_descriptor, temporary_name = tempfile.mkstemp(
            dir=target.parent, prefix=f".{target.name}."
        )
        remaining = memoryview(raw)
        while remaining:
            written = os.write(file_descriptor, remaining)
            if written <= 0:
                raise OSError("short temporary manifest write")
            remaining = remaining[written:]
        os.fsync(file_descriptor)
        os.close(file_descriptor)
        file_descriptor = None
        os.replace(temporary_name, target)
        temporary_name = None
    except OSError as exc:
        failure = exc
    finally:
        cleanup_failure: OSError | None = None
        if file_descriptor is not None:
            try:
                os.close(file_descriptor)
            except OSError as exc:
                cleanup_failure = exc
        if temporary_name is not None:
            try:
                os.unlink(temporary_name)
            except FileNotFoundError:
                pass
            except OSError as exc:
                cleanup_failure = cleanup_failure or exc
        if failure is not None:
            detail = f"{target}: {failure}"
            if cleanup_failure is not None:
                detail += f"; cleanup failed: {cleanup_failure}"
            _fail("manifest-write-failed", detail)
        if cleanup_failure is not None:
            _fail("manifest-write-failed", f"{target}: cleanup failed: {cleanup_failure}")
    try:
        TrustedRepoReader(repo).read_bytes(MANIFEST_RELATIVE_PATH)
    except ContextSurfaceError as exc:
        _fail("manifest-write-failed", str(exc))


def check_manifest(
    repo: Path,
    target: Path,
    index_inventory,
    read_blob,
    registry_path: str = AUDIT_REGISTRY_RELATIVE_PATH,
) -> list[str]:
    target = _manifest_target(Path(repo), Path(target))
    expected = render_manifest(
        repo,
        index_inventory,
        read_blob,
        registry_path,
        # Bootstrap only: the exact target was validated above and the trusted
        # read below proves it is a regular non-symlink before comparison.
        allow_untracked_self=True,
        verify_tracked_self=True,
    )
    try:
        actual = TrustedRepoReader(repo).read_bytes(MANIFEST_RELATIVE_PATH)
    except ContextSurfaceError as exc:
        return [f"manifest-missing: {target}: {exc}"]
    if actual != expected:
        return [
            "manifest-byte-mismatch: "
            f"expected {hashlib.sha256(expected).hexdigest()}, "
            f"found {hashlib.sha256(actual).hexdigest()}"
        ]
    return []


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="atomically write the manifest")
    mode.add_argument("--check", action="store_true", help="check exact deterministic bytes")
    return parser


def _git_inventory(repo: Path):
    try:
        completed = subprocess.run(
            [*git_command_prefix(repo), "ls-files", "-s", "-z"],
            cwd=repo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except (OSError, ContextSurfaceError) as exc:
        _fail("git-inventory-failed", str(exc))
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        _fail("git-inventory-failed", detail)
    inventory = {}
    try:
        records = [record for record in completed.stdout.split(b"\0") if record]
        for record in records:
            metadata, raw_path = record.split(b"\t", 1)
            mode, raw_blob, stage = metadata.split(b" ", 2)
            path = raw_path.decode("utf-8")
            blob = raw_blob.decode("ascii")
            try:
                stage_number = int(stage.decode("ascii"))
                mode_text = mode.decode("ascii")
            except (ValueError, UnicodeDecodeError) as exc:
                _fail("git-inventory-failed", f"malformed metadata for {path}: {exc}")
            if path in inventory:
                _fail("git-inventory-failed", f"duplicate index path {path}")
            inventory[path] = {
                "mode": mode_text,
                "blob": blob,
                "stage": stage_number,
            }
    except (ValueError, UnicodeDecodeError) as exc:
        _fail("git-inventory-failed", f"malformed git index output: {exc}")
    return inventory


def _git_read_blob(repo: Path, blob: str) -> bytes:
    if not isinstance(blob, str) or BLOB_RE.fullmatch(blob) is None:
        _fail("index-blob-read-failed", f"invalid blob id {blob!r}")
    try:
        completed = subprocess.run(
            [*git_command_prefix(repo), "cat-file", "blob", blob],
            cwd=repo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except (OSError, ContextSurfaceError) as exc:
        _fail("index-blob-read-failed", str(exc))
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        _fail("index-blob-read-failed", f"{blob}: {detail}")
    return completed.stdout


def main(argv=None) -> int:
    args = _parser().parse_args(argv)
    try:
        inventory = _git_inventory(REPO_ROOT)

        def read_blob(blob: str) -> bytes:
            return _git_read_blob(REPO_ROOT, blob)

        if args.write:
            write_manifest(REPO_ROOT, MANIFEST_PATH, inventory, read_blob)
            print(f"wrote {MANIFEST_RELATIVE_PATH}")
            return 0
        failures = check_manifest(REPO_ROOT, MANIFEST_PATH, inventory, read_blob)
    except ManifestBuildError as exc:
        failures = [str(exc)]
    for failure in failures:
        print(failure)
    print(f"AI context manifest: {'FAIL' if failures else 'PASS'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
