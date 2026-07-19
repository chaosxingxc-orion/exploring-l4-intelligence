#!/usr/bin/env python3
"""Build the deterministic, bounded AI context manifest.

This builder intentionally owns exact paths.  It has no wildcard or directory
grandfathering mechanism: additions require a reviewed constant change.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path, PurePosixPath

from ai_context_surface_check import (
    MANIFEST_RELATIVE_PATH,
    MANIFEST_SCHEMA,
    ContextSurfaceError,
    classify_path,
    load_json_strict,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = REPO_ROOT / MANIFEST_RELATIVE_PATH
AUDIT_REGISTRY_PATH = REPO_ROOT / "wiki/survey/sf-audit-artifact-registry.json"
ACTIVE_REVIEW_TRANSACTION = (
    "wiki/audit/system-first-stage1a/round-12/stage1a-readiness-correction.md"
)
BUDGETS_BYTES = {
    "AGENTS.md": 12288,
    "CLAUDE.md": 12288,
    "wiki/Research-Objective.md": 5120,
    "wiki/Per-Work-Status.md": 8192,
    "wiki/survey/README.md": 4096,
    "wiki/survey/current/README.md": 4096,
}


def _entry(path: str, path_class: str, load_policy: str, purpose: str):
    return {
        "path": path,
        "class": path_class,
        "load_policy": load_policy,
        "purpose": purpose,
    }


ACTIVE_ENTRY_SPECS = (
    _entry("AGENTS.md", "HOT", "default", "Codex repository operating guidance"),
    _entry(
        "wiki/Research-Objective.md",
        "HOT",
        "default",
        "single current research-state entry",
    ),
    _entry("wiki/Project-Thesis.md", "HOT", "default", "program north star"),
    _entry("wiki/Per-Work-Status.md", "HOT", "targeted", "current W1-W4 state"),
    _entry("wiki/survey/current/README.md", "CURRENT", "targeted", "current survey router"),
    _entry("wiki/survey/current/protocol.md", "CURRENT", "targeted", "effective protocol v2"),
    _entry("wiki/survey/current/status.md", "CURRENT", "targeted", "short current survey gate"),
    _entry(
        "wiki/survey/current/manifest.json",
        "CURRENT",
        "targeted",
        "machine current-survey asset router",
    ),
    _entry(
        "wiki/survey/current/data/identity-taxonomy-v6.json",
        "CURRENT",
        "targeted",
        "current identity taxonomy",
    ),
    _entry(
        "wiki/survey/current/data/known-item-coding-v7.json",
        "CURRENT",
        "targeted",
        "generated schema-v3 known-item coding",
    ),
    _entry(
        "wiki/survey/current/data/schema-v3-adjudication.json",
        "CURRENT",
        "targeted",
        "independent schema-v3 adjudication record",
    ),
    _entry(
        "wiki/survey/2026-07-15-sf-queries.jsonl",
        "HOT",
        "targeted",
        "frozen 65-query bytes",
    ),
    _entry(
        "wiki/survey/current/tables/opening-guarantees.md",
        "CURRENT",
        "targeted",
        "generated current opening guarantees",
    ),
    _entry(
        "docs/checks/system-first-stage1a/evidence-v6/identity-taxonomy-v6-test.json",
        "HOT",
        "targeted",
        "canonical v6 evidence report",
    ),
    _entry(
        "docs/checks/system-first-stage1a/evidence-v6/identity-taxonomy-v6-test.nt.json",
        "HOT",
        "targeted",
        "Windows v6 evidence report",
    ),
    _entry(
        "docs/checks/system-first-stage1a/evidence-v6/identity-taxonomy-v6-test.posix.json",
        "HOT",
        "targeted",
        "WSL/POSIX v6 evidence report",
    ),
    _entry(
        "wiki/audit/system-first-stage1a/INDEX.md",
        "HOT",
        "targeted",
        "append-only campaign audit index",
    ),
    _entry(
        MANIFEST_RELATIVE_PATH,
        "HOT",
        "targeted",
        "AI context manifest metadata (self-hash intentionally omitted)",
    ),
)


def _legacy(path: str, path_class: str):
    return {"path": path, "class": path_class}


EXACT_NAMED_LEGACY_EXCEPTIONS = (
    # Pre-routing W4 working proposal draft; retained at its historical path.
    _legacy("wiki/2026-07-11-W4-fresh-proposal-draft.md", "AUDIT_LEGACY"),
    # Pre-routing R preregistration draft; retained at its historical path.
    _legacy("wiki/2026-07-11-proposal-R-prereg-draft.md", "AUDIT_LEGACY"),
    # Historical identity-contract amendment from a separate contract chain.
    _legacy("wiki/2026-07-14-identity-contracts-amendment-1.md", "AUDIT_LEGACY"),
    # Historical response-replay template predating permanent audit routing.
    _legacy(
        "wiki/2026-07-14-survey-response-replayability-template.md",
        "AUDIT_LEGACY",
    ),
    # Historical record-denoise survey proposal predating permanent routing.
    _legacy(
        "wiki/2026-07-15-record-system-denoise-and-rationale-survey-proposal.md",
        "AUDIT_LEGACY",
    ),
    # Historical C4 preparation proposal predating permanent routing.
    _legacy(
        "wiki/2026-07-16-c4-prep-owner-rulings-and-coding-depth-proposal.md",
        "AUDIT_LEGACY",
    ),
    # Generic English proposal template retained as cold legacy documentation.
    _legacy("wiki/Research-Proposal-Template.md", "AUDIT_LEGACY"),
    # Generic Chinese proposal template retained as cold legacy documentation.
    _legacy("wiki/Research-Proposal-Template_CN.md", "AUDIT_LEGACY"),
)


RETAINED_LEGACY_PATHS = (
    _legacy("wiki/survey/2026-07-15-sf-bundle-manifest.md", "REGISTRY_LEGACY"),
    _legacy(
        "wiki/survey/2026-07-15-system-first-survey-protocol-v1.md",
        "REGISTRY_LEGACY",
    ),
    _legacy("wiki/survey/2026-07-15-sf-protocol-amendment-1.md", "AUDIT_LEGACY"),
    _legacy("wiki/survey/2026-07-16-sf-protocol-amendment-3.md", "AUDIT_LEGACY"),
    _legacy("wiki/survey/2026-07-16-sf-protocol-amendment-4.md", "AUDIT_LEGACY"),
    _legacy("wiki/survey/2026-07-16-sf-protocol-amendment-5.md", "AUDIT_LEGACY"),
    _legacy("wiki/survey/2026-07-17-sf-protocol-amendment-6.md", "AUDIT_LEGACY"),
    _legacy("wiki/survey/2026-07-17-sf-protocol-amendment-7.md", "AUDIT_LEGACY"),
    _legacy("wiki/survey/2026-07-18-sf-protocol-amendment-8.md", "AUDIT_LEGACY"),
    _legacy("wiki/survey/2026-07-18-sf-stage1b-opening-tables.md", "REGISTRY_LEGACY"),
    _legacy("wiki/survey/2026-07-19-sf-stage1b-opening-tables-v2.md", "REGISTRY_LEGACY"),
    _legacy("wiki/survey/2026-07-19-sf-stage1b-opening-tables-v3.md", "REGISTRY_LEGACY"),
    _legacy("wiki/survey/2026-07-19-sf-stage1b-opening-tables-v4.md", "REGISTRY_LEGACY"),
    # The taxonomy-v5 replay chain generated coding v6; there is no coding-v5
    # artifact.  These are the exact three platform reports and inputs it used.
    _legacy("wiki/survey/2026-07-19-sf-identity-taxonomy-v5.json", "REGISTRY_LEGACY"),
    _legacy("wiki/survey/2026-07-19-sf-known-item-coding-v6.json", "REGISTRY_LEGACY"),
    _legacy("docs/checks/2026-07-19-sf-identity-taxonomy-v5-test.json", "REGISTRY_LEGACY"),
    _legacy(
        "docs/checks/2026-07-19-sf-identity-taxonomy-v5-test.nt.json",
        "REGISTRY_LEGACY",
    ),
    _legacy(
        "docs/checks/2026-07-19-sf-identity-taxonomy-v5-test.posix.json",
        "REGISTRY_LEGACY",
    ),
)

BLOB_RE = re.compile(r"[0-9a-f]{40}\Z")
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


def _repo_file(repo: Path, path: str) -> Path:
    return repo.joinpath(*PurePosixPath(path).parts)


def _load_audit_inventory(registry_path: Path) -> list[dict[str, str]]:
    try:
        registry = load_json_strict(registry_path)
    except ContextSurfaceError as exc:
        _fail("audit-registry-invalid", str(exc))
    if not isinstance(registry, dict) or not isinstance(registry.get("artifacts"), list):
        _fail("audit-registry-invalid", "artifacts must be a list")
    artifacts = registry["artifacts"]
    if len(artifacts) != 77:
        _fail("audit-registry-count", f"expected 77 artifacts, found {len(artifacts)}")
    seen: set[str] = set()
    legacy: list[dict[str, str]] = []
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
        seen.add(path)
        legacy.append(_legacy(path, "AUDIT_LEGACY"))
    return legacy


def _validate_constants(specs, retained, named_exceptions):
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
    for index, entry in enumerate((*retained, *named_exceptions)):
        if not isinstance(entry, dict) or set(entry) != {"path", "class"}:
            _fail("legacy-entry-invalid", f"legacy constant [{index}] has wrong keys")
        path = _canonical_path(entry["path"], f"legacy constant [{index}].path")
        if entry["class"] not in {"AUDIT_LEGACY", "REGISTRY_LEGACY"}:
            _fail("legacy-entry-invalid", f"{path}: invalid class")
        if path in retained_seen:
            _fail("duplicate-path", f"retained legacy constant {path}")
        retained_seen.add(path)


def build_manifest(repo: Path, registry_path: Path) -> dict:
    repo = Path(repo)
    _validate_constants(
        ACTIVE_ENTRY_SPECS,
        RETAINED_LEGACY_PATHS,
        EXACT_NAMED_LEGACY_EXCEPTIONS,
    )
    registry_legacy = _load_audit_inventory(Path(registry_path))
    legacy_by_path: dict[str, dict[str, str]] = {}
    for entry in (
        *registry_legacy,
        *RETAINED_LEGACY_PATHS,
        *EXACT_NAMED_LEGACY_EXCEPTIONS,
    ):
        path = entry["path"]
        if path in legacy_by_path:
            _fail("duplicate-path", f"legacy inventory overlap {path}")
        legacy_by_path[path] = dict(entry)
    legacy = [legacy_by_path[path] for path in sorted(legacy_by_path)]

    entries: list[dict] = []
    for spec in ACTIVE_ENTRY_SPECS:
        entry = dict(spec)
        path = entry["path"]
        actual_class = classify_path(path, legacy)
        if actual_class != entry["class"]:
            _fail(
                "active-class-mismatch",
                f"{path}: declared {entry['class']}, classified {actual_class}",
            )
        if path != MANIFEST_RELATIVE_PATH:
            disk_path = _repo_file(repo, path)
            if not disk_path.is_file():
                _fail("active-path-missing", path)
            try:
                raw = disk_path.read_bytes()
            except OSError as exc:
                _fail("active-path-missing", f"{path}: {exc}")
            entry["sha256"] = hashlib.sha256(raw).hexdigest()
        entries.append(entry)

    document = {
        "schema": MANIFEST_SCHEMA,
        "active_entries": entries,
        "budgets_bytes": dict(sorted(BUDGETS_BYTES.items())),
        "legacy_cold_paths": legacy,
        "active_review_transaction": ACTIVE_REVIEW_TRANSACTION,
    }
    return document


def render_manifest(repo: Path = REPO_ROOT, registry_path: Path = AUDIT_REGISTRY_PATH) -> bytes:
    document = build_manifest(Path(repo), Path(registry_path))
    raw = (json.dumps(document, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if b"\\" in raw:
        _fail("manifest-render-invalid", "backslash found in rendered bytes")
    return raw


def write_manifest(
    repo: Path = REPO_ROOT,
    target: Path = MANIFEST_PATH,
    registry_path: Path = AUDIT_REGISTRY_PATH,
) -> None:
    raw = render_manifest(repo, registry_path)
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", dir=target.parent, prefix=f".{target.name}.", delete=False
        ) as temporary:
            temporary.write(raw)
            temporary.flush()
            os.fsync(temporary.fileno())
            temporary_name = temporary.name
        os.replace(temporary_name, target)
        temporary_name = None
    finally:
        if temporary_name is not None:
            try:
                os.unlink(temporary_name)
            except FileNotFoundError:
                pass


def check_manifest(
    repo: Path = REPO_ROOT,
    target: Path = MANIFEST_PATH,
    registry_path: Path = AUDIT_REGISTRY_PATH,
) -> list[str]:
    expected = render_manifest(repo, registry_path)
    try:
        actual = Path(target).read_bytes()
    except OSError as exc:
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


def main(argv=None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.write:
            write_manifest()
            print(f"wrote {MANIFEST_RELATIVE_PATH}")
            return 0
        failures = check_manifest()
    except ManifestBuildError as exc:
        failures = [str(exc)]
    for failure in failures:
        print(failure)
    print(f"AI context manifest: {'FAIL' if failures else 'PASS'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
