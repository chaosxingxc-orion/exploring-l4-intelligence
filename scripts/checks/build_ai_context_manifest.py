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
    loads_json_strict,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = REPO_ROOT / MANIFEST_RELATIVE_PATH
AUDIT_CAMPAIGN_INDEX_PATH = "wiki/audit/system-first-stage1a/INDEX.md"
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


AUDIT_CAMPAIGN_ENTRY_SPEC = _entry(
    AUDIT_CAMPAIGN_INDEX_PATH,
    "HOT",
    "targeted",
    "append-only campaign audit index",
)


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
    _entry(
        "wiki/AI-Collaboration.md",
        "HOT",
        "targeted",
        "canonical AI document placement and lifecycle policy",
    ),
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


_PREEXISTING_AUDIT_DOC_PATHS = (
    "wiki/2026-07-11-overnight-remediation-report.md",
    "wiki/2026-07-13-precheck-provenance-correction.md",
    "wiki/2026-07-15-s0-program-identity-signoff.md",
    "wiki/survey/2026-07-14-canonical-census-v2/census_report_v2.md",
    "wiki/survey/2026-07-14-canonical-census/census_report.md",
    "wiki/survey/2026-07-14-claim-ledger-v1/ledger_report.md",
    "wiki/survey/2026-07-14-claim-ledger-v2/ledger_v2_report.md",
    "wiki/survey/2026-07-15-sf-seed-manifest-report.md",
)

_PREEXISTING_REGISTRY_DOC_PATHS = (
    "wiki/2026-06-23-omni-embed-speech-disentanglement-1.2.1.md",
    "wiki/2026-07-03-omni-agentic-tfrl-go-no-go-decision.md",
    "wiki/2026-07-04-stage1-problem-definition.md",
    "wiki/2026-07-04-stage1-semantic-tfrl-survey.md",
    "wiki/2026-07-11-group-split-statistics-design.md",
    "wiki/2026-07-11-survey-full-verification.md",
    "wiki/2026-07-12-omni-hotword-biasing-survey.md",
    "wiki/2026-07-12-omni-lm-rescoring-survey.md",
    "wiki/2026-07-12-retrieve-discover-use-analysis.md",
    "wiki/2026-07-14-1b-probe-protocol-v1.md",
    "wiki/2026-07-14-ai-assisted-survey-knowledge-stack-open-source-evaluation.md",
    "wiki/2026-07-14-identity-contracts-v1.md",
    "wiki/2026-07-14-resp04-gate-a-execution.md",
    "wiki/2026-07-14-round2-search-protocol-v1.md",
    "wiki/2026-07-14-stage1c-decision-package.md",
    "wiki/2026-07-15-replayability-template-token-overlay.md",
    "wiki/2026-07-18-inherited-prior-exposure-union.md",
    "wiki/Omni-Embed-Model-Dossier.md",
    "wiki/Paralinguistic-Suppression-Survey.md",
    "wiki/Speech-Semantic-Task-Datasets.md",
    "wiki/Theory-Convergence-and-Constraints.md",
    "wiki/W4-Research-Plan.md",
    "wiki/W4-Training-Free-RL-Feasibility.md",
    "wiki/survey/2026-07-04-stage1-3w-crossdomain-comparisons.md",
    "wiki/survey/2026-07-04-stage1-L1-asr-st.md",
    "wiki/survey/2026-07-04-stage1-L2-slu.md",
    "wiki/survey/2026-07-04-stage1-L3-sqa-reasoning.md",
    "wiki/survey/2026-07-04-stage1-L4-speech-agentic.md",
    "wiki/survey/2026-07-04-stage1-X1-prompt-space-quantification.md",
    "wiki/survey/2026-07-04-stage1-X2-paralinguistic-delta.md",
    "wiki/survey/2026-07-04-stage1-X3-llm-vlm-testtime-map.md",
    "wiki/survey/2026-07-07-multimodal-knowledge-systems-alignment.md",
    "wiki/survey/2026-07-08-speech2vec-dims-1-4.md",
    "wiki/survey/2026-07-08-speech2vec-dims-5-8.md",
    "wiki/survey/2026-07-09-datasets-lock-first14.md",
    "wiki/survey/2026-07-09-datasets-lock-second14.md",
    "wiki/survey/2026-07-09-embedder-selection-matrix-full.md",
    "wiki/survey/2026-07-09-theory-scheme-coverage-appendix.md",
    "wiki/survey/2026-07-09-verifier-backbones-beyond-local.md",
    "wiki/survey/2026-07-14-coverage-and-kill-matrix-v2.md",
    "wiki/survey/2026-07-14-neighbor-matrix-v2.md",
    "wiki/survey/2026-07-14-sota-cards-v2.md",
    "wiki/survey/2026-07-15-gate-s1-own-library-sweep.md",
    "wiki/survey/2026-07-15-round2-protocol-v2-instantiated.md",
    "wiki/survey/2026-07-15-sf-blank-templates.md",
    "wiki/survey/2026-07-15-sf-secondary-routes.md",
    "wiki/survey/2026-07-16-sf-t1-proceedings-routes.md",
    "wiki/survey/2026-07-18-sf-heldout-l12-prereg-c4c.md",
    "wiki/survey/2026-07-18-sf-known-item-dfs-systemcontrol.md",
    "wiki/survey/2026-07-18-sf-p0r9-seven-papers-dfs.md",
    "wiki/survey/2026-07-18-sf-v4-claim-evidence-matrix.md",
    "wiki/survey/2026-07-18-sf-v5-claim-evidence-matrix.md",
    "wiki/survey/2026-07-19-sf-bibliography-v1.md",
    "wiki/survey/replay/SURVEY-RESP-2026-07-14-01/README.md",
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


def _load_audit_inventory(
    graph: Stage0Graph,
    registry_path: str,
) -> list[dict[str, str]]:
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

    actual_prefix_hash = registry_prefix_sha256(artifacts)
    if actual_prefix_hash != REGISTRY_BASELINE_PREFIX_SHA256:
        _fail(
            "audit-registry-prefix-mismatch",
            f"{actual_prefix_hash} != {REGISTRY_BASELINE_PREFIX_SHA256}",
        )

    legacy: list[dict[str, str]] = []
    for path, blob in validated:
        graph.raw(path, "audit-registry-path-untracked")
        if graph.blobs.get(path) != blob:
            _fail(
                "audit-registry-blob-mismatch",
                f"{path}: inventory {graph.blobs.get(path)!r} != pinned {blob!r}",
            )
        if not path.startswith("wiki/audit/"):
            legacy.append(_legacy(path, "AUDIT_LEGACY"))
    return legacy


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
) -> dict:
    graph = Stage0Graph(Path(repo), index_inventory, read_blob)
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
    registry_legacy = _load_audit_inventory(
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
    return document


def render_manifest(
    repo: Path,
    index_inventory,
    read_blob,
    registry_path: str = AUDIT_REGISTRY_RELATIVE_PATH,
    *,
    allow_untracked_self: bool = False,
) -> bytes:
    document = build_manifest(
        Path(repo),
        index_inventory,
        read_blob,
        registry_path,
        allow_untracked_self=allow_untracked_self,
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
            ["git", "ls-files", "-s", "-z"],
            cwd=repo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as exc:
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
            ["git", "cat-file", "blob", blob],
            cwd=repo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as exc:
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
