#!/usr/bin/env python3
"""Fail-closed AI context-surface and persistent-document routing oracle.

The evaluator is deliberately pure with respect to Git: callers supply the
tracked path inventory.  Only ``main`` shells out to obtain that inventory.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from itertools import chain
from pathlib import Path, PurePosixPath
from urllib.parse import unquote


MANIFEST_RELATIVE_PATH = "docs/integrity/ai-context-manifest.json"
MANIFEST_SCHEMA = "ai-context-manifest-v1"
MANIFEST_KEYS = {
    "schema",
    "active_entries",
    "budgets_bytes",
    "legacy_cold_paths",
    "active_review_transaction",
}
ENTRY_KEYS = {"path", "class", "load_policy", "purpose", "sha256"}
SELF_ENTRY_KEYS = ENTRY_KEYS - {"sha256"}
LEGACY_KEYS = {"path", "class"}
LEGACY_CLASSES = {"AUDIT_LEGACY", "REGISTRY_LEGACY"}
COLD_ACTIVE_CLASSES = {
    "AUDIT",
    "ARCHIVE",
    "WORKBENCH",
    "AUDIT_LEGACY",
    "REGISTRY_LEGACY",
}
HOT_FILES = frozenset(
    {
        "AGENTS.md",
        "CLAUDE.md",
        "CONTRIBUTING.md",
        MANIFEST_RELATIVE_PATH,
        "wiki/AI-Collaboration.md",
        "wiki/Per-Work-Status.md",
        "wiki/Project-Thesis.md",
        "wiki/Research-Methodology.md",
        "wiki/Research-Objective.md",
        "wiki/audit/system-first-stage1a/INDEX.md",
        "wiki/survey/2026-07-15-sf-queries.jsonl",
        "wiki/survey/README.md",
        "docs/checks/system-first-stage1a/evidence-v6/identity-taxonomy-v6-test.json",
        "docs/checks/system-first-stage1a/evidence-v6/identity-taxonomy-v6-test.nt.json",
        "docs/checks/system-first-stage1a/evidence-v6/identity-taxonomy-v6-test.posix.json",
    }
)
AUDIT_NAME_RE = re.compile(
    r"(?:^|[-_.])(?:(?:re)?review(?:er)?|response|proposal|amendment)(?:[-_.]|$)",
    re.IGNORECASE,
)
AMENDMENT_RE = re.compile(r"(?:^|[-_.])amendment(?:[-_.]|$)", re.IGNORECASE)
INLINE_LINK_RE = re.compile(
    r"(?<!!)\[[^\]\n]*\]\(\s*(?:<([^>\n]+)>|([^\s)]+))(?:\s+[^)]*)?\s*\)"
)
REFERENCE_DEFINITION_RE = re.compile(
    r"^[ ]{0,3}\[((?:\\.|[^\[\]\n])+)\]:[ \t]*"
    r"(?:<([^>\n]*)>|([^ \t\n]+))"
    r"(?:[ \t]+(?:\"[^\"\n]*\"|'[^'\n]*'|\([^\)\n]*\)))?[ \t]*$"
)
REFERENCE_DEFINITION_HEAD_RE = re.compile(
    r"^[ ]{0,3}\[((?:\\.|[^\[\]\n])+)\]:[ \t]*$"
)
REFERENCE_DESTINATION_RE = re.compile(
    r"^[ ]{1,3}(?:<([^>\n]*)>|([^ \t\n]+))"
    r"(?:[ \t]+(?:\"[^\"\n]*\"|'[^'\n]*'|\([^\)\n]*\)))?[ \t]*$"
)
FENCE_OPEN_RE = re.compile(r"^[ ]{0,3}(?:(`{3,})[^`\n]*|(~{3,})[^\n]*)$")
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
CLIENT_NORMALIZATIONS = (
    ("# AGENTS.md", "# CLIENT-GUIDE.md"),
    ("# CLAUDE.md", "# CLIENT-GUIDE.md"),
    (
        "This file provides guidance to Codex (Codex.ai/code) "
        "when working with code in this repository.",
        "This file provides guidance to CLIENT when working with code in this repository.",
    ),
    (
        "This file provides guidance to Claude Code (claude.ai/code) "
        "when working with code in this repository.",
        "This file provides guidance to CLIENT when working with code in this repository.",
    ),
    (
        "Installed via the Windows Codex plugin marketplace (see `docs/setup.md`):",
        "Installed via the Windows CLIENT plugin marketplace (see `docs/setup.md`):",
    ),
    (
        "Installed via the Windows Claude Code plugin marketplace (see `docs/setup.md`):",
        "Installed via the Windows CLIENT plugin marketplace (see `docs/setup.md`):",
    ),
)


class ContextSurfaceError(ValueError):
    """Controlled policy/schema error."""


def _failure(code: str, detail: str) -> str:
    return f"{code}: {detail}"


def _canonical_path(value: object, label: str = "path") -> str:
    if not isinstance(value, str):
        raise ContextSurfaceError(_failure("invalid-path", f"{label} must be a string"))
    if not value or value in {".", ".."}:
        raise ContextSurfaceError(_failure("invalid-path", f"{label} is empty or dot-only"))
    if "\\" in value:
        raise ContextSurfaceError(_failure("invalid-path", f"{label} uses a backslash: {value!r}"))
    if value.startswith("/") or re.match(r"^[A-Za-z]:", value):
        raise ContextSurfaceError(_failure("invalid-path", f"{label} is absolute: {value!r}"))
    path = PurePosixPath(value)
    if any(part in {"", ".", ".."} for part in path.parts):
        raise ContextSurfaceError(
            _failure("invalid-path", f"{label} is not canonical repo-relative POSIX: {value!r}")
        )
    canonical = path.as_posix()
    if canonical != value:
        raise ContextSurfaceError(
            _failure("invalid-path", f"{label} is not canonical repo-relative POSIX: {value!r}")
        )
    return canonical


def _legacy_map(legacy_cold_paths: object) -> dict[str, str]:
    if not isinstance(legacy_cold_paths, list):
        raise ContextSurfaceError(
            _failure("manifest-schema-invalid", "legacy_cold_paths must be a list")
        )
    result: dict[str, str] = {}
    for index, entry in enumerate(legacy_cold_paths):
        if not isinstance(entry, dict) or set(entry) != LEGACY_KEYS:
            raise ContextSurfaceError(
                _failure(
                    "manifest-schema-invalid",
                    f"legacy_cold_paths[{index}] must have exact keys {sorted(LEGACY_KEYS)}",
                )
            )
        path = _canonical_path(entry["path"], f"legacy_cold_paths[{index}].path")
        path_class = entry["class"]
        if not isinstance(path_class, str) or path_class not in LEGACY_CLASSES:
            raise ContextSurfaceError(
                _failure(
                    "manifest-schema-invalid",
                    f"legacy_cold_paths[{index}].class is invalid: {path_class!r}",
                )
            )
        if path in result:
            raise ContextSurfaceError(_failure("duplicate-path", f"legacy path {path}"))
        result[path] = path_class
    return result


def classify_path(path, legacy_cold_paths):
    """Classify one canonical repository path using the policy precedence."""

    canonical = _canonical_path(path)
    legacy = _legacy_map(legacy_cold_paths)
    if canonical in HOT_FILES:
        return "HOT"
    if canonical.startswith("wiki/survey/current/"):
        return "CURRENT"
    if canonical.startswith("wiki/survey/registry/") or canonical.startswith(
        "wiki/survey/sidecars/"
    ):
        return "REGISTRY"
    if canonical.startswith("wiki/audit/"):
        return "AUDIT"
    if canonical.startswith("wiki/archive/"):
        return "ARCHIVE"
    if canonical.startswith("wiki/survey/workbench/"):
        return "WORKBENCH"
    if canonical in legacy:
        return legacy[canonical]
    return "UNCLASSIFIED"


def normalize_agent_guide(text):
    """Normalize only the three intentional Codex/Claude guide differences."""

    if not isinstance(text, str):
        raise TypeError("agent guide must be text")
    lines = text.splitlines(keepends=True)
    normalized: list[str] = []
    for line in lines:
        ending = ""
        body = line
        if line.endswith("\r\n"):
            body, ending = line[:-2], "\r\n"
        elif line.endswith("\n") or line.endswith("\r"):
            body, ending = line[:-1], line[-1]
        for source, target in CLIENT_NORMALIZATIONS:
            if body == source:
                body = target
                break
        normalized.append(body + ending)
    return "".join(normalized)


def _strict_json_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ContextSurfaceError(_failure("manifest-json-invalid", f"duplicate key {key!r}"))
        result[key] = value
    return result


def _reject_nonfinite(value: str):
    raise ContextSurfaceError(_failure("manifest-json-invalid", f"non-finite number {value}"))


def load_json_strict(path: Path):
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise ContextSurfaceError(_failure("manifest-missing", f"{path}: {exc}")) from exc
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ContextSurfaceError(
            _failure("manifest-json-invalid", f"invalid UTF-8: {exc}")
        ) from exc
    try:
        return json.loads(
            text,
            object_pairs_hook=_strict_json_object,
            parse_constant=_reject_nonfinite,
        )
    except ContextSurfaceError:
        raise
    except (json.JSONDecodeError, ValueError) as exc:
        raise ContextSurfaceError(_failure("manifest-json-invalid", str(exc))) from exc


def _join_repo(repo: Path, relative_path: str) -> Path:
    return repo.joinpath(*PurePosixPath(relative_path).parts)


def _normalize_link_target(source_path: str, raw_target: str) -> str | None:
    target = unquote(raw_target).strip()
    if not target or target.startswith("#"):
        return None
    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target) or target.startswith("//"):
        return None
    target = target.split("#", 1)[0].split("?", 1)[0]
    if not target:
        return None
    if "\\" in target or target.startswith("/") or re.match(r"^[A-Za-z]:", target):
        raise ContextSurfaceError(_failure("invalid-link-path", f"{source_path} -> {raw_target}"))
    target_path = PurePosixPath(target)
    if target.startswith(("wiki/", "docs/", "scripts/")) or target in HOT_FILES:
        components: list[str] = []
    else:
        components = list(PurePosixPath(source_path).parent.parts)
    for part in target_path.parts:
        if part in {"", "."}:
            continue
        if part == "..":
            if not components:
                raise ContextSurfaceError(
                    _failure(
                        "invalid-link-path",
                        f"link escapes repository: {source_path} -> {raw_target}",
                    )
                )
            components.pop()
        else:
            components.append(part)
    if not components:
        return None
    return _canonical_path(PurePosixPath(*components).as_posix(), "link target")


def _is_direct_audit_round_link(path: str) -> bool:
    parts = PurePosixPath(path).parts
    if len(parts) < 4 or parts[:2] != ("wiki", "audit"):
        return False
    return not (len(parts) == 4 and parts[-1] == "INDEX.md")


def _blank_except_newlines(text: str) -> str:
    return "".join(character if character in "\r\n" else " " for character in text)


def _backtick_is_escaped(text: str, position: int) -> bool:
    backslashes = 0
    cursor = position - 1
    while cursor >= 0 and text[cursor] == "\\":
        backslashes += 1
        cursor -= 1
    return backslashes % 2 == 1


def _mask_inline_code_spans(text: str) -> str:
    characters = list(text)
    cursor = 0
    while cursor < len(text):
        opening = text.find("`", cursor)
        if opening < 0:
            break
        if _backtick_is_escaped(text, opening):
            cursor = opening + 1
            continue
        opening_end = opening
        while opening_end < len(text) and text[opening_end] == "`":
            opening_end += 1
        delimiter_length = opening_end - opening
        search = opening_end
        closing_end = None
        while search < len(text):
            closing = text.find("`", search)
            if closing < 0:
                break
            if _backtick_is_escaped(text, closing):
                search = closing + 1
                continue
            run_end = closing
            while run_end < len(text) and text[run_end] == "`":
                run_end += 1
            if run_end - closing == delimiter_length:
                closing_end = run_end
                break
            search = run_end
        if closing_end is None:
            cursor = opening_end
            continue
        for index in range(opening, closing_end):
            if characters[index] not in "\r\n":
                characters[index] = " "
        cursor = closing_end
    return "".join(characters)


def _mask_markdown_code(text: str) -> str:
    """Mask block and inline Markdown code while preserving line structure."""

    masked_lines: list[str] = []
    fence_character: str | None = None
    fence_length = 0
    for line in text.splitlines(keepends=True):
        content = line.rstrip("\r\n")
        if fence_character is not None:
            close = re.match(
                rf"^[ ]{{0,3}}{re.escape(fence_character)}{{{fence_length},}}[ \t]*$",
                content,
            )
            masked_lines.append(_blank_except_newlines(line))
            if close:
                fence_character = None
                fence_length = 0
            continue
        opener = FENCE_OPEN_RE.match(content)
        if opener:
            marker = opener.group(1) or opener.group(2)
            fence_character = marker[0]
            fence_length = len(marker)
            masked_lines.append(_blank_except_newlines(line))
            continue
        if re.match(r"^(?: {4}| {0,3}\t)", content):
            masked_lines.append(_blank_except_newlines(line))
            continue
        masked_lines.append(line)
    return _mask_inline_code_spans("".join(masked_lines))


def _reference_definition_targets(text: str):
    """Yield valid one- or two-line Markdown reference destinations.

    Definitions are scanned even when no usage is present.  That conservative
    choice prevents a later reference usage from silently activating a cold
    audit dependency.  The caller supplies shared code-masked text; footnote
    definitions are not link definitions for this policy and are ignored.
    """

    lines = text.splitlines()
    for index, line in enumerate(lines):
        definition = REFERENCE_DEFINITION_RE.match(line)
        if definition:
            raw_label = definition.group(1)
            if raw_label.strip() and not raw_label.startswith("^"):
                yield (
                    definition.group(2)
                    if definition.group(2) is not None
                    else definition.group(3)
                )
            continue
        head = REFERENCE_DEFINITION_HEAD_RE.match(line)
        if not head or index + 1 >= len(lines):
            continue
        raw_label = head.group(1)
        if not raw_label.strip() or raw_label.startswith("^"):
            continue
        destination = REFERENCE_DESTINATION_RE.match(lines[index + 1])
        if destination:
            yield (
                destination.group(1)
                if destination.group(1) is not None
                else destination.group(2)
            )


def _validate_manifest_shape(manifest: object, failures: list[str]):
    if not isinstance(manifest, dict):
        failures.append(_failure("manifest-schema-invalid", "manifest must be an object"))
        return {}, [], {}, [], None
    if set(manifest) != MANIFEST_KEYS:
        failures.append(
            _failure(
                "manifest-schema-invalid",
                f"top-level keys must be exactly {sorted(MANIFEST_KEYS)}",
            )
        )
    if manifest.get("schema") != MANIFEST_SCHEMA:
        failures.append(
            _failure("manifest-schema-invalid", f"schema must be {MANIFEST_SCHEMA!r}")
        )
    active = manifest.get("active_entries", [])
    budgets = manifest.get("budgets_bytes", {})
    legacy = manifest.get("legacy_cold_paths", [])
    active_review = manifest.get("active_review_transaction")
    if not isinstance(active, list):
        failures.append(_failure("manifest-schema-invalid", "active_entries must be a list"))
        active = []
    if not isinstance(budgets, dict):
        failures.append(_failure("manifest-schema-invalid", "budgets_bytes must be an object"))
        budgets = {}
    if active_review is not None and not isinstance(active_review, str):
        failures.append(
            _failure("manifest-schema-invalid", "active_review_transaction must be null or a path")
        )
        active_review = None
    return manifest, active, budgets, legacy, active_review


def evaluate_manifest(repo, manifest, tracked_paths):
    """Evaluate a parsed manifest against an explicit tracked-path inventory."""

    repo = Path(repo)
    failures: list[str] = []
    _, active, budgets, legacy_entries, active_review = _validate_manifest_shape(manifest, failures)

    try:
        legacy = _legacy_map(legacy_entries)
    except ContextSurfaceError as exc:
        failures.append(str(exc))
        legacy = {}
        legacy_entries = []

    canonical_review: str | None = None
    if active_review is not None:
        try:
            canonical_review = _canonical_path(active_review, "active_review_transaction")
            if not canonical_review.startswith(
                "wiki/audit/"
            ) or canonical_review.endswith("/INDEX.md"):
                failures.append(
                    _failure(
                        "manifest-schema-invalid",
                        "active_review_transaction must be one exact audit-round artifact",
                    )
                )
        except ContextSurfaceError as exc:
            failures.append(str(exc))

    canonical_tracked: list[str] = []
    tracked_seen: set[str] = set()
    if not isinstance(tracked_paths, (list, tuple)):
        failures.append(
            _failure("manifest-schema-invalid", "tracked_paths must be an explicit list")
        )
        tracked_paths = []
    for index, path in enumerate(tracked_paths):
        try:
            canonical = _canonical_path(path, f"tracked_paths[{index}]")
        except ContextSurfaceError as exc:
            failures.append(str(exc))
            continue
        if canonical in tracked_seen:
            failures.append(_failure("duplicate-path", f"tracked path {canonical}"))
            continue
        tracked_seen.add(canonical)
        canonical_tracked.append(canonical)

    if len(active) > 30:
        failures.append(
            _failure("active-entry-budget-exceeded", f"{len(active)} active entries exceeds 30")
        )

    active_seen: set[str] = set()
    for index, entry in enumerate(active):
        if not isinstance(entry, dict):
            failures.append(
                _failure("manifest-entry-invalid", f"active_entries[{index}] must be an object")
            )
            continue
        raw_path = entry.get("path")
        is_self = raw_path == MANIFEST_RELATIVE_PATH
        expected_keys = SELF_ENTRY_KEYS if is_self else ENTRY_KEYS
        if set(entry) != expected_keys:
            failures.append(
                _failure(
                    "manifest-entry-invalid",
                    f"active_entries[{index}] keys must be exactly {sorted(expected_keys)}",
                )
            )
        try:
            path = _canonical_path(raw_path, f"active_entries[{index}].path")
        except ContextSurfaceError as exc:
            failures.append(str(exc))
            continue
        if path in active_seen:
            failures.append(_failure("duplicate-path", f"active path {path}"))
            continue
        active_seen.add(path)
        try:
            actual_class = classify_path(path, legacy_entries)
        except ContextSurfaceError as exc:
            failures.append(str(exc))
            actual_class = "UNCLASSIFIED"
        declared_class = entry.get("class")
        if not isinstance(declared_class, str):
            failures.append(_failure("manifest-entry-invalid", f"{path}: class must be a string"))
        if declared_class != actual_class:
            failures.append(
                _failure(
                    "active-class-mismatch",
                    f"{path}: declared {declared_class!r}, classified {actual_class!r}",
                )
            )
        if actual_class in COLD_ACTIVE_CLASSES or (
            isinstance(declared_class, str) and declared_class in COLD_ACTIVE_CLASSES
        ):
            failures.append(
                _failure("cold-path-on-active-surface", f"{path}: {actual_class}")
            )
        if not isinstance(entry.get("load_policy"), str) or entry.get("load_policy") not in {
            "default",
            "targeted",
        }:
            failures.append(
                _failure("manifest-entry-invalid", f"{path}: invalid load_policy")
            )
        if not isinstance(entry.get("purpose"), str) or not entry.get("purpose", "").strip():
            failures.append(
                _failure("manifest-entry-invalid", f"{path}: purpose must be non-empty")
            )
        sha256 = entry.get("sha256")
        if not is_self and (not isinstance(sha256, str) or SHA256_RE.fullmatch(sha256) is None):
            failures.append(_failure("manifest-entry-invalid", f"{path}: invalid sha256"))
        disk_path = _join_repo(repo, path)
        if not disk_path.is_file():
            failures.append(_failure("active-path-missing", path))
            continue
        try:
            raw = disk_path.read_bytes()
        except OSError as exc:
            failures.append(_failure("active-path-missing", f"{path}: {exc}"))
            continue
        if not is_self and isinstance(sha256, str) and SHA256_RE.fullmatch(sha256):
            actual_hash = hashlib.sha256(raw).hexdigest()
            if actual_hash != sha256:
                failures.append(
                    _failure("active-hash-mismatch", f"{path}: {actual_hash} != {sha256}")
                )

    budget_seen: set[str] = set()
    for raw_path, limit in budgets.items():
        try:
            path = _canonical_path(raw_path, "budgets_bytes key")
        except ContextSurfaceError as exc:
            failures.append(str(exc))
            continue
        if path in budget_seen:
            failures.append(_failure("duplicate-path", f"budget path {path}"))
            continue
        budget_seen.add(path)
        if isinstance(limit, bool) or not isinstance(limit, int) or limit < 0:
            failures.append(
                _failure(
                    "manifest-schema-invalid",
                    f"budget for {path} must be a non-negative integer",
                )
            )
            continue
        disk_path = _join_repo(repo, path)
        if disk_path.is_file():
            try:
                actual_size = len(disk_path.read_bytes())
            except OSError as exc:
                failures.append(_failure("active-path-missing", f"{path}: {exc}"))
                continue
            if actual_size > limit:
                failures.append(
                    _failure("file-budget-exceeded", f"{path}: {actual_size} > {limit} raw bytes")
                )

    for path in canonical_tracked:
        path_class = (
            classify_path(path, legacy_entries)
            if legacy_entries
            else classify_path(path, [])
        )
        basename = PurePosixPath(path).name
        is_legacy = path in legacy
        if (
            path.startswith("wiki/")
            and path.lower().endswith(".md")
            and AUDIT_NAME_RE.search(basename)
            and not path.startswith(("wiki/audit/", "wiki/archive/"))
            and not is_legacy
        ):
            failures.append(_failure("new-audit-artifact-outside-audit-root", path))
        if (
            path.startswith("wiki/")
            and path.lower().endswith(".md")
            and AMENDMENT_RE.search(basename)
            and not path.startswith("wiki/archive/")
            and not is_legacy
        ):
            failures.append(_failure("unconsolidated-amendment-forbidden", path))
        if path_class not in {"HOT", "CURRENT"} or not path.lower().endswith(".md"):
            continue
        disk_path = _join_repo(repo, path)
        if not disk_path.is_file():
            continue
        try:
            text = disk_path.read_bytes().decode("utf-8")
        except UnicodeDecodeError as exc:
            failures.append(_failure("active-file-invalid-utf8", f"{path}: {exc}"))
            continue
        link_text = _mask_markdown_code(text)
        inline_targets = (
            match.group(1) or match.group(2)
            for match in INLINE_LINK_RE.finditer(link_text)
        )
        reference_targets = _reference_definition_targets(link_text)
        for raw_target in chain(inline_targets, reference_targets):
            try:
                target = _normalize_link_target(path, raw_target)
            except ContextSurfaceError as exc:
                failures.append(str(exc))
                continue
            if (
                target is not None
                and _is_direct_audit_round_link(target)
                and target != canonical_review
            ):
                failures.append(_failure("direct-audit-round-link", f"{path} -> {target}"))

    guide_paths = {"AGENTS.md", "CLAUDE.md"}
    if guide_paths.issubset(tracked_seen):
        try:
            agents = _join_repo(repo, "AGENTS.md").read_bytes().decode("utf-8")
            claude = _join_repo(repo, "CLAUDE.md").read_bytes().decode("utf-8")
            if normalize_agent_guide(agents) != normalize_agent_guide(claude):
                failures.append(
                    _failure(
                        "agent-guides-not-mirrored",
                        "shared guidance differs beyond 3 client lines",
                    )
                )
        except (OSError, UnicodeDecodeError) as exc:
            failures.append(_failure("agent-guides-not-mirrored", str(exc)))

    return failures


def _git_tracked_paths(repo: Path) -> list[str]:
    completed = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise ContextSurfaceError(_failure("git-ls-files-failed", detail))
    try:
        return [part.decode("utf-8") for part in completed.stdout.split(b"\0") if part]
    except UnicodeDecodeError as exc:
        raise ContextSurfaceError(
            _failure("git-ls-files-failed", f"non-UTF-8 path: {exc}")
        ) from exc


def main() -> int:
    repo = Path(__file__).resolve().parents[2]
    try:
        document = load_json_strict(_join_repo(repo, MANIFEST_RELATIVE_PATH))
        failures = evaluate_manifest(repo, document, _git_tracked_paths(repo))
    except ContextSurfaceError as exc:
        failures = [str(exc)]
    for failure in failures:
        print(failure)
    print(f"AI context surface: {'FAIL' if failures else 'PASS'} ({len(failures)} failures)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
