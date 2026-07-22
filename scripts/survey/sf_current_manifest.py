#!/usr/bin/env python3
"""Build the deterministic manifest for the active Stage-1A survey layer."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
import unicodedata
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
from sf_json_contract import JsonContractError, loads as strict_json_loads  # noqa: E402
from sf_query_compiler import atomic_write_bytes  # noqa: E402
import sf_campaign_audit_index as campaign_audit_index  # noqa: E402


OUTPUT_RELATIVE_PATH = "wiki/survey/current/manifest.json"
OUTPUT_PATH = REPO.joinpath(*OUTPUT_RELATIVE_PATH.split("/"))
CAMPAIGN_SEMANTIC_ANCHOR_PATH = "scripts/checks/ai_context_inventory.py"
CURRENT_PACKAGE_REPORT_PATH = (
    "docs/checks/system-first-stage1a/context-v1/current-package-check.json"
)
WIKI_SYNC_INCIDENT_PATH = (
    "docs/checks/system-first-stage1a/context-v1/wiki-sync-dry-run-incident.json"
)
_INTEGRATION_EVIDENCE_SCHEMAS = {
    WIKI_SYNC_INCIDENT_PATH: "wiki-sync-dry-run-incident-v1",
}


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


@dataclass(frozen=True)
class ConsumerManifest:
    """One strict manifest plus the exact hash-verified bytes it names."""

    document: dict
    artifacts: dict[str, bytes]

    def paths(self, key: str) -> tuple[str, ...]:
        return tuple(self.document[key])

    def read_bytes(self, path: str) -> bytes:
        try:
            return self.artifacts[path]
        except KeyError as error:
            raise CurrentManifestError(
                f"manifest artifact is not available: {path}"
            ) from error


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
        "wiki_sync_dry_run_incident",
        WIKI_SYNC_INCIDENT_PATH,
        "immutable-after-first-commit",
        "targeted",
    ),
    FileSpec(
        "dual_platform_aggregate_checker",
        "scripts/survey/sf_dual_platform_check.py",
        "normal-code-lifecycle",
        "machine-only",
    ),
    FileSpec(
        "campaign_audit_semantic_anchor",
        CAMPAIGN_SEMANTIC_ANCHOR_PATH,
        "normal-code-lifecycle",
        "machine-only",
    ),
    FileSpec(
        "campaign_audit_index_checker",
        "scripts/survey/sf_campaign_audit_index.py",
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
    FileSpec(
        "stage1b_mapping_release",
        "wiki/survey/current/tables/stage1b-mapping-release.md",
        "release-scoped-immutable",
        "targeted",
    ),
    FileSpec(
        "stage1c_eligible_inputs",
        "wiki/survey/current/tables/stage1c-eligible-inputs.md",
        "release-scoped-immutable",
        "targeted",
    ),
    FileSpec(
        "stage1b_release_manifest",
        "docs/checks/stage1b-closeout/2026-07-22/release-manifest.json",
        "release-scoped-immutable",
        "targeted",
    ),
)


_AUDIT_FILE_SPECS = (
    FileSpec(
        "audit_artifact_registry",
        "wiki/survey/sf-audit-artifact-registry.json",
        "append-only",
        "machine-only",
    ),
    FileSpec(
        "campaign_audit_contract",
        campaign_audit_index.CONTRACT_PATH.relative_to(REPO).as_posix(),
        "append-only",
        "cold-audit",
    ),
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
    "wiki/survey/current/tables/stage1b-mapping-release.md",
    "wiki/survey/current/tables/stage1c-eligible-inputs.md",
    "docs/checks/stage1b-closeout/2026-07-22/release-manifest.json",
)
_BASE_PROSE_SCAN = (
    "wiki/survey/current/README.md",
    "wiki/survey/current/protocol.md",
    "wiki/survey/current/status.md",
    "wiki/survey/current/tables/opening-guarantees.md",
    "wiki/survey/current/tables/stage1b-mapping-release.md",
    "wiki/survey/current/tables/stage1c-eligible-inputs.md",
)

_CONSUMER_MANIFEST_KEYS = {
    "schema",
    "files",
    "release_bound_artifacts",
    "prose_scan_paths",
}
_CONSUMER_FILE_KEYS = {
    "role",
    "path",
    "sha256",
    "mutability",
    "load_policy",
}
_CONSUMER_ARRAY_KEYS = ("release_bound_artifacts", "prose_scan_paths")


def canonical_consumer_path(value: object, *, label: str = "manifest path") -> str:
    """Return one portable repository-relative path or fail closed."""

    if not isinstance(value, str) or not value:
        raise CurrentManifestError(f"{label} is not a nonempty string")
    if (
        "\\" in value
        or any(character in '<>:"|?*' for character in value)
        or value.startswith("/")
        or re.match(r"^[A-Za-z]:", value)
        or unicodedata.normalize("NFC", value) != value
        or any(
            unicodedata.category(character).startswith("C")
            or unicodedata.category(character) in {"Zl", "Zp"}
            for character in value
        )
    ):
        raise CurrentManifestError(
            f"{label} is not canonical; not portable repo-relative POSIX: {value!r}"
        )
    parts = value.split("/")
    if any(part in ("", ".", "..") for part in parts):
        raise CurrentManifestError(
            f"{label} is not canonical; not portable repo-relative POSIX: {value!r}"
        )
    reserved = re.compile(
        r"(?:CON|PRN|AUX|NUL|CONIN\$|CONOUT\$|COM[1-9¹²³]|LPT[1-9¹²³])",
        re.IGNORECASE,
    )
    for part in parts:
        device_stem = part.partition(".")[0].rstrip(" ")
        if part.endswith((" ", ".")) or reserved.fullmatch(device_stem):
            raise CurrentManifestError(
                f"{label} is not canonical; not portable repo-relative POSIX: {value!r}"
            )
    return value


def _consumer_string(entry: dict, key: str, *, label: str) -> str:
    value = entry.get(key)
    if not isinstance(value, str) or not value:
        raise CurrentManifestError(f"{label}.{key} must be a nonempty string")
    return value


def _validate_consumer_document(document: object) -> dict[str, dict]:
    if not isinstance(document, dict):
        raise CurrentManifestError("current manifest root must be an object")
    if set(document) != _CONSUMER_MANIFEST_KEYS:
        raise CurrentManifestError(
            "current manifest schema keys mismatch: "
            f"expected {sorted(_CONSUMER_MANIFEST_KEYS)}, found {sorted(document)}"
        )
    if document.get("schema") != "sf-current-manifest-v1":
        raise CurrentManifestError(
            "current manifest schema must be sf-current-manifest-v1"
        )
    files = document.get("files")
    if not isinstance(files, list) or not files:
        raise CurrentManifestError("current manifest files must be a nonempty array")

    files_by_path: dict[str, dict] = {}
    roles: set[str] = set()
    for index, entry in enumerate(files):
        label = f"files[{index}]"
        if not isinstance(entry, dict) or set(entry) != _CONSUMER_FILE_KEYS:
            keys = sorted(entry) if isinstance(entry, dict) else type(entry).__name__
            raise CurrentManifestError(
                f"{label} schema keys mismatch: {keys}"
            )
        role = _consumer_string(entry, "role", label=label)
        path = canonical_consumer_path(
            _consumer_string(entry, "path", label=label),
            label=f"{label}.path",
        )
        digest = _consumer_string(entry, "sha256", label=label)
        _consumer_string(entry, "mutability", label=label)
        _consumer_string(entry, "load_policy", label=label)
        if re.fullmatch(r"[0-9a-f]{64}", digest) is None:
            raise CurrentManifestError(f"{label}.sha256 is not lowercase SHA-256")
        if path.startswith("wiki/archive/"):
            raise CurrentManifestError(f"current manifest contains archive path: {path}")
        if path in files_by_path:
            raise CurrentManifestError(f"current manifest files duplicates path: {path}")
        if role in roles:
            raise CurrentManifestError(f"current manifest files duplicates role: {role}")
        files_by_path[path] = entry
        roles.add(role)

    for key in _CONSUMER_ARRAY_KEYS:
        values = document.get(key)
        if not isinstance(values, list) or not values:
            raise CurrentManifestError(
                f"current manifest {key} must be a nonempty array"
            )
        seen: set[str] = set()
        for index, value in enumerate(values):
            path = canonical_consumer_path(value, label=f"{key}[{index}]")
            if path.startswith("wiki/archive/"):
                raise CurrentManifestError(f"{key} contains archive path: {path}")
            if path in seen:
                raise CurrentManifestError(f"{key} duplicates path: {path}")
            if path not in files_by_path:
                raise CurrentManifestError(
                    f"{key} path is not present in files: {path}"
                )
            seen.add(path)
    return files_by_path


def load_consumer_manifest(
    repo: Path, manifest_relative_path: str = OUTPUT_RELATIVE_PATH
) -> ConsumerManifest:
    """Strict-load a manifest and freeze every named file at its declared hash."""

    manifest_path = canonical_consumer_path(
        manifest_relative_path, label="current manifest path"
    )
    if manifest_path.startswith("wiki/archive/"):
        raise CurrentManifestError(
            f"current manifest path points to archive path: {manifest_path}"
        )
    try:
        reader = TrustedRepoReader(Path(repo))
        raw = reader.read_bytes(manifest_path)
        document = strict_json_loads(raw, manifest_path)
    except (ContextSurfaceError, JsonContractError, OSError) as error:
        raise CurrentManifestError(
            f"current manifest missing, invalid, or untrusted: {manifest_path}: {error}"
        ) from error

    files_by_path = _validate_consumer_document(document)
    artifacts: dict[str, bytes] = {}
    for path, entry in files_by_path.items():
        try:
            artifact = reader.read_bytes(path)
        except (ContextSurfaceError, OSError) as error:
            raise CurrentManifestError(
                f"manifest artifact missing or untrusted: {path}: {error}"
            ) from error
        actual = hashlib.sha256(artifact).hexdigest()
        if actual != entry["sha256"]:
            raise CurrentManifestError(
                f"manifest artifact SHA-256 mismatch: {path}: "
                f"declared {entry['sha256']}, found {actual}"
            )
        artifacts[path] = artifact
    return ConsumerManifest(document=document, artifacts=artifacts)


def _active_audit_specs(index_inventory: dict[str, GitIndexEntry]) -> tuple[FileSpec, ...]:
    tracked = {
        spec.path: spec.path in index_inventory for spec in _AUDIT_FILE_SPECS
    }
    active = tracked[AUDIT_CAMPAIGN_INDEX_PATH]
    if active and not all(tracked.values()):
        raise CurrentManifestError(
            "audit-activation-incomplete: "
            + ", ".join(f"{path} tracked={present}" for path, present in tracked.items())
        )
    if not active:
        unexpected = {
            path: present
            for path, present in tracked.items()
            if path != "wiki/survey/sf-audit-artifact-registry.json" and present
        }
        if unexpected:
            raise CurrentManifestError(
                "audit-activation-incomplete: "
                + ", ".join(
                    f"{path} tracked={present}" for path, present in tracked.items()
                )
            )
        return ()
    return _AUDIT_FILE_SPECS


def _staged_bytes(
    path: str,
    index_inventory: dict[str, GitIndexEntry],
    read_blob: Callable[[str], bytes],
) -> bytes:
    entry = index_inventory.get(path)
    if entry is None:
        raise CurrentManifestError(f"campaign gate input is untracked: {path}")
    entry = _validate_index_entry(path, entry)
    try:
        raw = read_blob(entry.blob)
    except (OSError, CurrentManifestError) as error:
        raise CurrentManifestError(f"campaign gate cannot read {path}: {error}") from error
    if not isinstance(raw, bytes):
        raise CurrentManifestError(f"campaign gate blob reader returned non-bytes: {path}")
    return raw


def _campaign_semantic_anchor_from_source(raw: bytes) -> tuple[int, str]:
    """Extract one module-level literal baseline pair from exact staged source."""

    try:
        source = raw.decode("utf-8")
        tree = ast.parse(source, filename=CAMPAIGN_SEMANTIC_ANCHOR_PATH)
    except (UnicodeDecodeError, SyntaxError) as error:
        raise CurrentManifestError(f"campaign-anchor-invalid: {error}") from error

    names = {
        "CAMPAIGN_INDEX_BASELINE_COUNT": [],
        "CAMPAIGN_INDEX_BASELINE_PREFIX_SHA256": [],
    }
    module_nodes = set(tree.body)
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            targets = [target.id for target in node.targets if isinstance(target, ast.Name)]
            value = node.value
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            targets = [node.target.id]
            value = node.value
        else:
            continue
        for name in targets:
            if name in names:
                names[name].append((node, value))

    values: dict[str, object] = {}
    for name, assignments in names.items():
        if len(assignments) != 1:
            raise CurrentManifestError(
                f"campaign-anchor-invalid: {name} must have exactly one assignment"
            )
        node, value_node = assignments[0]
        if node not in module_nodes or not isinstance(value_node, ast.Constant):
            raise CurrentManifestError(
                f"campaign-anchor-invalid: {name} must be one module-level literal"
            )
        values[name] = value_node.value

    count = values["CAMPAIGN_INDEX_BASELINE_COUNT"]
    prefix = values["CAMPAIGN_INDEX_BASELINE_PREFIX_SHA256"]
    if isinstance(count, bool) or not isinstance(count, int) or count <= 0:
        raise CurrentManifestError(
            "campaign-anchor-invalid: baseline count must be a positive integer"
        )
    if not isinstance(prefix, str) or re.fullmatch(r"[0-9a-f]{64}", prefix) is None:
        raise CurrentManifestError(
            "campaign-anchor-invalid: baseline prefix must be lowercase SHA-256"
        )
    return count, prefix


def _validate_campaign_anchor_lineage(
    rounds: list[dict],
    head_count: int,
    head_prefix: str,
    staged_count: int,
    staged_prefix: str,
) -> None:
    """Allow either an unchanged HEAD anchor or one fully anchored appended event."""

    for label, count, prefix in (
        ("HEAD", head_count, head_prefix),
        ("staged", staged_count, staged_prefix),
    ):
        if isinstance(count, bool) or not isinstance(count, int) or count <= 0:
            raise CurrentManifestError(
                f"campaign-anchor-lineage-invalid: {label} count"
            )
        if not isinstance(prefix, str) or re.fullmatch(r"[0-9a-f]{64}", prefix) is None:
            raise CurrentManifestError(
                f"campaign-anchor-lineage-invalid: {label} prefix"
            )

    try:
        entries = campaign_audit_index.semantic_entries(rounds)
    except (KeyError, TypeError) as error:
        raise CurrentManifestError(
            f"campaign contract cannot form semantic entries: {error}"
        ) from error
    total = len(entries)
    if staged_count < head_count:
        raise CurrentManifestError("campaign anchor count rollback is forbidden")
    if head_count > total:
        raise CurrentManifestError(
            f"campaign contract is shorter than HEAD anchor: {total} < {head_count}"
        )

    if staged_count == head_count:
        if staged_prefix != head_prefix:
            raise CurrentManifestError(
                "campaign same-count anchor restamp is forbidden"
            )
        if total != staged_count:
            raise CurrentManifestError(
                f"campaign unanchored semantic tail: {total} rows, anchor {staged_count}"
            )
    else:
        old_actual = campaign_audit_index.semantic_prefix_sha256(rounds, head_count)
        if old_actual != head_prefix:
            raise CurrentManifestError(
                "campaign contract HEAD-anchored prefix changed before append"
            )
        if staged_count != head_count + 1:
            raise CurrentManifestError(
                "campaign anchor growth must add exactly one semantic event per transaction"
            )
        if staged_count != total:
            raise CurrentManifestError(
                f"campaign unanchored semantic tail: {total} rows, anchor {staged_count}"
            )
        if entries[head_count]["round"] <= entries[head_count - 1]["round"]:
            raise CurrentManifestError(
                "campaign anchor growth must append its semantic event in a new round"
            )

    staged_actual = campaign_audit_index.semantic_prefix_sha256(rounds, staged_count)
    if staged_actual != staged_prefix:
        raise CurrentManifestError(
            "campaign staged anchor SHA does not match its protected prefix"
        )
    head_actual = campaign_audit_index.semantic_prefix_sha256(rounds, head_count)
    if head_actual != head_prefix:
        raise CurrentManifestError("campaign contract does not preserve the HEAD anchor")


def _head_bytes(
    path: str,
    read_head_path: Callable[[str], bytes],
) -> bytes:
    if not callable(read_head_path):
        raise CurrentManifestError("campaign HEAD-path reader is required")
    try:
        raw = read_head_path(path)
    except (OSError, CurrentManifestError, KeyError) as error:
        raise CurrentManifestError(
            f"campaign gate cannot read HEAD:{path}: {error}"
        ) from error
    if not isinstance(raw, bytes):
        raise CurrentManifestError(
            f"campaign HEAD-path reader returned non-bytes: {path}"
        )
    return raw


def _validate_campaign_gate(
    index_inventory: dict[str, GitIndexEntry],
    read_blob: Callable[[str], bytes],
    read_head_path: Callable[[str], bytes],
) -> None:
    registry_path = "wiki/survey/sf-audit-artifact-registry.json"
    contract_path = campaign_audit_index.CONTRACT_PATH.relative_to(REPO).as_posix()
    try:
        registry = strict_json_loads(
            _staged_bytes(registry_path, index_inventory, read_blob), registry_path
        )
        contract = strict_json_loads(
            _staged_bytes(contract_path, index_inventory, read_blob), contract_path
        )
        staged_count, staged_prefix = _campaign_semantic_anchor_from_source(
            _staged_bytes(CAMPAIGN_SEMANTIC_ANCHOR_PATH, index_inventory, read_blob)
        )
        head_count, head_prefix = _campaign_semantic_anchor_from_source(
            _head_bytes(CAMPAIGN_SEMANTIC_ANCHOR_PATH, read_head_path)
        )
        _validate_campaign_anchor_lineage(
            contract["rounds"],
            head_count,
            head_prefix,
            staged_count,
            staged_prefix,
        )
        carrier_documents = {
            path: _staged_bytes(path, index_inventory, read_blob)
            for path in campaign_audit_index.EXPECTED_CARRIERS.values()
        }
        campaign_audit_index.validate_contract(
            registry,
            contract,
            carrier_documents,
            baseline_count=head_count,
            baseline_prefix_sha256=head_prefix,
        )
    except (JsonContractError, campaign_audit_index.CampaignIndexError) as error:
        raise CurrentManifestError(f"campaign-audit-index-invalid: {error}") from error
    actual_index = _staged_bytes(
        AUDIT_CAMPAIGN_INDEX_PATH, index_inventory, read_blob
    )
    expected_index = campaign_audit_index.render_index(contract)
    if actual_index != expected_index:
        raise CurrentManifestError(
            "campaign-audit-index-stale: staged INDEX does not match staged contract"
        )


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
    expected_schema = _INTEGRATION_EVIDENCE_SCHEMAS.get(spec.path)
    if expected_schema is not None:
        try:
            document = strict_json_loads(raw, spec.path)
        except JsonContractError as error:
            raise CurrentManifestError(
                f"integration-evidence-schema-invalid: {spec.path}: {error}"
            ) from error
        if not isinstance(document, dict) or document.get("schema") != expected_schema:
            actual_schema = document.get("schema") if isinstance(document, dict) else None
            raise CurrentManifestError(
                "integration-evidence-schema-invalid: "
                f"{spec.path}: expected {expected_schema!r}, found {actual_schema!r}"
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
    read_head_path: Callable[[str], bytes],
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
    if audit_specs:
        _validate_campaign_gate(index_inventory, read_blob, read_head_path)
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
    read_head_path: Callable[[str], bytes],
) -> bytes:
    document = build_manifest(
        read_bytes, index_inventory, read_blob, read_head_path
    )
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


def _git_head_path_reader(repo: Path) -> Callable[[str], bytes]:
    cache: dict[str, bytes] = {}

    def read_head_path(path: str) -> bytes:
        canonical = _canonical_git_path(path)
        if canonical not in cache:
            cache[canonical] = _run_git(
                repo,
                ["show", f"HEAD:{canonical}"],
                label=f"git show HEAD:{canonical}",
            )
        return cache[canonical]

    return read_head_path


def _repo_reader(repo: Path = REPO) -> Callable[[str], bytes]:
    try:
        reader = TrustedRepoReader(repo)
    except ContextSurfaceError as error:
        raise CurrentManifestError(f"repository root is untrusted: {error}") from error
    return reader.read_bytes


def expected_bytes() -> bytes:
    inventory, read_blob = _git_release_context(REPO)
    return render_manifest(
        _repo_reader(),
        inventory,
        read_blob,
        _git_head_path_reader(REPO),
    )


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
