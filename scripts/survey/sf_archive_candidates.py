#!/usr/bin/env python3
"""Fail-closed safety oracle for the seven approved legacy archive moves.

This command plans or verifies moves; it never performs a move and never
rewrites references.  The exact transition inventory is shared with the AI
context builder so a partial archive state is invalid everywhere.
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
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable, Sequence


REPO = Path(__file__).resolve().parents[2]
CHECKS_DIR = REPO / "scripts" / "checks"
if str(CHECKS_DIR) not in sys.path:
    sys.path.insert(0, str(CHECKS_DIR))

from ai_context_inventory import ARCHIVE_TRANSITIONS  # noqa: E402
from ai_context_surface_check import (  # noqa: E402
    ContextSurfaceError,
    TrustedRepoReader,
    _canonical_path,
    classify_path,
    loads_json_strict,
)
from sf_query_compiler import atomic_write_bytes  # noqa: E402
from sf_current_manifest import _git_command_prefix as git_command_prefix  # noqa: E402


PLAN_RELATIVE_PATH = (
    "wiki/archive/working/system-first-stage1a/archive-plan.json"
)
REGISTRY_RELATIVE_PATH = "wiki/survey/sf-audit-artifact-registry.json"
CURRENT_MANIFEST_RELATIVE_PATH = "wiki/survey/current/manifest.json"
PLAN_SCHEMA = "sf-archive-plan-v1"
BLOB_RE = re.compile(r"[0-9a-f]{40}\Z")
REGULAR_GIT_MODES = {"100644", "100755"}


@dataclass(frozen=True)
class Failure:
    code: str
    detail: str

    def __str__(self) -> str:
        return f"{self.code}: {self.detail}"


class ArchiveSafetyError(RuntimeError):
    """One or more archive preconditions failed."""

    def __init__(self, code: str | None = None, detail: str = "", *, failures=None):
        collected = tuple(failures or ())
        if not collected:
            if code is None:
                raise ValueError("ArchiveSafetyError requires a failure")
            collected = (Failure(code, detail),)
        self.failures = collected
        self.code = collected[0].code
        super().__init__("; ".join(str(item) for item in collected))


@dataclass(frozen=True)
class GitEntry:
    mode: str
    blob: str


@dataclass(frozen=True)
class Inspection:
    state: str
    transitions: tuple[dict[str, str], ...]


def _fail(code: str, detail: str) -> None:
    raise ArchiveSafetyError(code, detail)


def _canonical(value: object, label: str) -> str:
    try:
        return _canonical_path(value, label)
    except ContextSurfaceError as error:
        _fail("archive-path-invalid", str(error))


def validate_transitions(
    transitions: Sequence[dict[str, str]], *, require_shared_exact: bool = False
) -> tuple[dict[str, str], ...]:
    if not isinstance(transitions, (tuple, list)) or not transitions:
        _fail("archive-transition-constant-invalid", "transition inventory is empty")
    if require_shared_exact and transitions is not ARCHIVE_TRANSITIONS:
        _fail(
            "archive-transition-constant-invalid",
            "production inventory must be imported from ai_context_inventory",
        )
    if require_shared_exact and len(transitions) != 7:
        _fail("archive-transition-constant-invalid", "expected exactly seven transitions")

    normalized: list[dict[str, str]] = []
    sources: set[str] = set()
    destinations: set[str] = set()
    for index, transition in enumerate(transitions):
        if not isinstance(transition, dict) or set(transition) != {
            "source",
            "destination",
            "git_blob",
        }:
            _fail(
                "archive-transition-constant-invalid",
                f"transition[{index}] must have source/destination/git_blob",
            )
        source = _canonical(transition["source"], f"transition[{index}].source")
        destination = _canonical(
            transition["destination"], f"transition[{index}].destination"
        )
        blob = transition["git_blob"]
        if not isinstance(blob, str) or BLOB_RE.fullmatch(blob) is None:
            _fail(
                "archive-transition-constant-invalid",
                f"transition[{index}] has invalid Git blob",
            )
        if source in sources or destination in destinations or source == destination:
            _fail(
                "archive-transition-constant-invalid",
                f"transition[{index}] duplicates a source or destination",
            )
        if not destination.startswith("wiki/archive/"):
            _fail(
                "archive-transition-constant-invalid",
                f"destination is outside wiki/archive: {destination}",
            )
        sources.add(source)
        destinations.add(destination)
        normalized.append(
            {"source": source, "destination": destination, "git_blob": blob}
        )
    return tuple(normalized)


def parse_index(raw: bytes) -> dict[str, GitEntry]:
    inventory: dict[str, GitEntry] = {}
    try:
        records = (record for record in raw.split(b"\0") if record)
        for record in records:
            metadata, raw_path = record.split(b"\t", 1)
            raw_mode, raw_blob, raw_stage = metadata.split(b" ", 2)
            mode = raw_mode.decode("ascii")
            blob = raw_blob.decode("ascii")
            stage = raw_stage.decode("ascii")
            path = raw_path.decode("utf-8")
            if stage != "0":
                _fail("archive-git-index-invalid", f"non-stage-0 entry: {path}")
            if mode not in REGULAR_GIT_MODES:
                _fail("archive-git-index-invalid", f"non-regular Git mode {mode}: {path}")
            if BLOB_RE.fullmatch(blob) is None:
                _fail("archive-git-index-invalid", f"invalid Git blob: {path}")
            try:
                canonical = _canonical_path(path, "Git index path")
            except ContextSurfaceError as error:
                _fail("archive-git-index-invalid", str(error))
            if canonical in inventory:
                _fail("archive-git-index-invalid", f"duplicate Git path: {canonical}")
            inventory[canonical] = GitEntry(mode, blob)
    except ArchiveSafetyError:
        raise
    except (ValueError, UnicodeDecodeError) as error:
        _fail("archive-git-index-invalid", f"malformed ls-files output: {error}")
    return inventory


def _parse_head(raw: bytes) -> dict[str, GitEntry]:
    inventory: dict[str, GitEntry] = {}
    try:
        for record in (record for record in raw.split(b"\0") if record):
            metadata, raw_path = record.split(b"\t", 1)
            raw_mode, raw_type, raw_blob = metadata.split(b" ", 2)
            if raw_type != b"blob":
                continue
            mode = raw_mode.decode("ascii")
            blob = raw_blob.decode("ascii")
            path = _canonical_path(raw_path.decode("utf-8"), "HEAD path")
            if mode not in REGULAR_GIT_MODES or BLOB_RE.fullmatch(blob) is None:
                _fail("archive-git-head-invalid", f"invalid HEAD entry: {path}")
            if path in inventory:
                _fail("archive-git-head-invalid", f"duplicate HEAD path: {path}")
            inventory[path] = GitEntry(mode, blob)
    except ArchiveSafetyError:
        raise
    except (ValueError, UnicodeDecodeError, ContextSurfaceError) as error:
        _fail("archive-git-head-invalid", f"malformed ls-tree output: {error}")
    return inventory


def resolve_transition_state(
    transitions: Sequence[dict[str, str]], tracked_blobs: dict[str, str]
) -> str:
    normalized = validate_transitions(transitions)
    sources = {entry["source"] for entry in normalized}
    destinations = {entry["destination"] for entry in normalized}
    tracked = set(tracked_blobs)
    tracked_sources = sources & tracked
    tracked_destinations = destinations & tracked
    pre = tracked_sources == sources and not tracked_destinations
    post = not tracked_sources and tracked_destinations == destinations
    if not (pre or post):
        _fail(
            "archive-transition-incomplete",
            f"sources={len(tracked_sources)}/{len(sources)}, "
            f"destinations={len(tracked_destinations)}/{len(destinations)}",
        )
    selected = "source" if pre else "destination"
    for entry in normalized:
        path = entry[selected]
        actual = tracked_blobs.get(path)
        if actual != entry["git_blob"]:
            _fail(
                "archive-transition-blob-mismatch",
                f"{path}: {actual!r} != {entry['git_blob']!r}",
            )
    return "pre" if pre else "post"


def _git(repo: Path, arguments: list[str], *, allow_no_match: bool = False) -> bytes:
    try:
        result = subprocess.run(
            [*git_command_prefix(repo), *arguments],
            cwd=repo,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as error:
        _fail("archive-git-failed", str(error))
    allowed = {0, 1} if allow_no_match else {0}
    if result.returncode not in allowed:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        _fail("archive-git-failed", f"git {' '.join(arguments)}: {detail}")
    return result.stdout


def _git_inventory(repo: Path) -> tuple[dict[str, GitEntry], dict[str, GitEntry]]:
    index = parse_index(_git(repo, ["ls-files", "-s", "-z"]))
    head = _parse_head(_git(repo, ["ls-tree", "-r", "-z", "HEAD"]))
    return index, head


def _hash_object(repo: Path, relative: str) -> str:
    raw = _git(repo, ["hash-object", "--", relative])
    try:
        blob = raw.decode("ascii").strip()
    except UnicodeDecodeError as error:
        _fail("archive-git-failed", f"hash-object output: {error}")
    if BLOB_RE.fullmatch(blob) is None:
        _fail("archive-git-failed", f"hash-object returned invalid blob for {relative}")
    return blob


def _secure_path_state(repo: Path, relative: str) -> str:
    """Return file/missing while rejecting every symlink or non-directory ancestor."""

    canonical = _canonical(relative, "repository path")
    root = repo.resolve(strict=True)
    current = root
    parts = PurePosixPath(canonical).parts
    for position, part in enumerate(parts):
        current = current / part
        try:
            metadata = os.lstat(current)
        except FileNotFoundError:
            return "missing"
        if stat.S_ISLNK(metadata.st_mode):
            _fail("archive-path-untrusted", f"symlink component: {canonical}")
        final = position == len(parts) - 1
        if final:
            if not stat.S_ISREG(metadata.st_mode):
                _fail("archive-path-untrusted", f"not a regular file: {canonical}")
            return "file"
        if not stat.S_ISDIR(metadata.st_mode):
            _fail("archive-path-untrusted", f"non-directory ancestor: {canonical}")
    return "missing"


def _read_trusted(reader: TrustedRepoReader, relative: str, code: str) -> bytes:
    try:
        return reader.read_bytes(relative)
    except ContextSurfaceError as error:
        _fail(code, str(error))


def _assert_input_clean(
    repo: Path,
    reader: TrustedRepoReader,
    relative: str,
    index: dict[str, GitEntry],
    head: dict[str, GitEntry],
    *,
    code: str = "archive-input-dirty",
    require_head_match: bool = False,
) -> bytes:
    index_entry = index.get(relative)
    head_entry = head.get(relative)
    if index_entry is None:
        _fail(code, f"critical input is not tracked at stage 0: {relative}")
    if require_head_match and index_entry != head_entry:
        _fail(code, f"immutable critical input differs from HEAD: {relative}")
    raw = _read_trusted(reader, relative, "archive-path-untrusted")
    actual = _hash_object(repo, relative)
    if actual != index_entry.blob:
        _fail(code, f"critical input has working-tree drift: {relative}")
    return raw


def _load_registry(
    repo: Path,
    reader: TrustedRepoReader,
    index: dict[str, GitEntry],
    head: dict[str, GitEntry],
) -> tuple[set[str], dict[str, str]]:
    raw = _assert_input_clean(
        repo,
        reader,
        REGISTRY_RELATIVE_PATH,
        index,
        head,
        require_head_match=True,
    )
    try:
        document = loads_json_strict(raw, REGISTRY_RELATIVE_PATH)
    except ContextSurfaceError as error:
        _fail("archive-registry-invalid", str(error))
    if not isinstance(document, dict) or not isinstance(document.get("artifacts"), list):
        _fail("archive-registry-invalid", "artifacts must be a list")
    paths: set[str] = set()
    pins: dict[str, str] = {}
    for position, entry in enumerate(document["artifacts"]):
        if not isinstance(entry, dict) or set(entry) != {"path", "git_blob"}:
            _fail("archive-registry-invalid", f"artifacts[{position}] schema")
        path = _canonical(entry["path"], f"artifacts[{position}].path")
        blob = entry["git_blob"]
        if not isinstance(blob, str) or BLOB_RE.fullmatch(blob) is None:
            _fail("archive-registry-invalid", f"artifacts[{position}].git_blob")
        if path in paths:
            _fail("archive-registry-invalid", f"duplicate path: {path}")
        paths.add(path)
        pins[path] = blob
    for path, pin in pins.items():
        _assert_input_clean(
            repo, reader, path, index, head, require_head_match=True
        )
        if index[path].blob != pin:
            _fail(
                "archive-registry-invalid",
                f"registered artifact blob differs from pin: {path}",
            )
    return paths, pins


def _load_current_manifest_paths(
    repo: Path,
    reader: TrustedRepoReader,
    index: dict[str, GitEntry],
    head: dict[str, GitEntry],
) -> set[str]:
    raw = _assert_input_clean(
        repo, reader, CURRENT_MANIFEST_RELATIVE_PATH, index, head
    )
    try:
        document = loads_json_strict(raw, CURRENT_MANIFEST_RELATIVE_PATH)
    except ContextSurfaceError as error:
        _fail("archive-current-manifest-invalid", str(error))
    if not isinstance(document, dict) or not isinstance(document.get("files"), list):
        _fail("archive-current-manifest-invalid", "files must be a list")
    paths: set[str] = set()
    for position, entry in enumerate(document["files"]):
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            _fail("archive-current-manifest-invalid", f"files[{position}].path")
        path = _canonical(entry["path"], f"files[{position}].path")
        if path in paths:
            _fail("archive-current-manifest-invalid", f"duplicate path: {path}")
        paths.add(path)
    return paths


def _reference_paths(repo: Path, needle: str) -> tuple[str, ...]:
    raw = _git(
        repo,
        ["grep", "-l", "-z", "-F", "--", needle, "--"],
        allow_no_match=True,
    )
    paths: list[str] = []
    try:
        for encoded in (item for item in raw.split(b"\0") if item):
            paths.append(_canonical_path(encoded.decode("utf-8"), "git grep path"))
    except (UnicodeDecodeError, ContextSurfaceError) as error:
        _fail("archive-git-grep-invalid", str(error))
    return tuple(sorted(set(paths)))


def _critical_references(
    repo: Path,
    reader: TrustedRepoReader,
    transitions: Sequence[dict[str, str]],
    registered_paths: set[str],
    index: dict[str, GitEntry],
    head: dict[str, GitEntry],
) -> list[Failure]:
    failures: list[Failure] = []
    verified: set[str] = set()
    for transition in transitions:
        source = transition["source"]
        for referrer in _reference_paths(repo, source):
            path_class = classify_path(referrer, [])
            critical_code = None
            if path_class in {"HOT", "CURRENT"}:
                critical_code = "archive-inbound-active"
            elif referrer in registered_paths:
                critical_code = "archive-inbound-registered-audit"
            if critical_code is None:
                continue
            if referrer not in verified:
                _assert_input_clean(repo, reader, referrer, index, head)
                verified.add(referrer)
            failures.append(Failure(critical_code, f"{source} <- {referrer}"))
    return failures


def _inspect(
    repo: Path,
    transitions: Sequence[dict[str, str]],
    *,
    required_state: str,
    require_shared_exact: bool,
) -> Inspection:
    normalized = validate_transitions(
        transitions, require_shared_exact=require_shared_exact
    )
    try:
        repo = Path(repo).resolve(strict=True)
        reader = TrustedRepoReader(repo)
    except (OSError, ContextSurfaceError) as error:
        _fail("archive-repo-untrusted", str(error))
    index, head = _git_inventory(repo)
    tracked_blobs = {path: entry.blob for path, entry in index.items()}
    state = resolve_transition_state(normalized, tracked_blobs)
    if state != required_state:
        _fail(
            "archive-transition-state-mismatch",
            f"expected {required_state}, found {state}",
        )

    registered_paths, _ = _load_registry(repo, reader, index, head)
    current_paths = _load_current_manifest_paths(repo, reader, index, head)

    failures: list[Failure] = []
    for transition in normalized:
        source = transition["source"]
        destination = transition["destination"]
        expected_blob = transition["git_blob"]
        if required_state == "pre":
            if _secure_path_state(repo, source) != "file":
                failures.append(Failure("archive-source-missing", source))
                continue
            if _secure_path_state(repo, destination) != "missing":
                failures.append(Failure("archive-destination-present", destination))
            head_entry = head.get(source)
            if head_entry is None or head_entry.blob != expected_blob:
                failures.append(
                    Failure("archive-source-dirty", f"HEAD blob changed: {source}")
                )
            elif _hash_object(repo, source) != expected_blob:
                failures.append(
                    Failure("archive-source-dirty", f"working bytes changed: {source}")
                )
            if source in registered_paths:
                failures.append(Failure("archive-source-registered-audit", source))
            if source in current_paths:
                failures.append(Failure("archive-source-current-manifest", source))
        else:
            if _secure_path_state(repo, source) != "missing":
                failures.append(Failure("archive-source-still-present", source))
            if _secure_path_state(repo, destination) != "file":
                failures.append(Failure("archive-destination-missing", destination))
                continue
            if _hash_object(repo, destination) != expected_blob:
                failures.append(
                    Failure("archive-destination-dirty", destination)
                )
            index_entry = index.get(destination)
            if index_entry is None or index_entry.blob != expected_blob:
                failures.append(
                    Failure("archive-destination-dirty", f"index blob changed: {destination}")
                )

    try:
        failures.extend(
            _critical_references(
                repo, reader, normalized, registered_paths, index, head
            )
        )
    except ArchiveSafetyError as error:
        failures.extend(error.failures)
    if failures:
        raise ArchiveSafetyError(failures=failures)
    return Inspection(state=state, transitions=normalized)


def inspect_pre_move(
    repo: Path = REPO,
    transitions: Sequence[dict[str, str]] = ARCHIVE_TRANSITIONS,
) -> Inspection:
    return _inspect(
        repo,
        transitions,
        required_state="pre",
        require_shared_exact=transitions is ARCHIVE_TRANSITIONS,
    )


def inspect_applied(
    repo: Path = REPO,
    transitions: Sequence[dict[str, str]] = ARCHIVE_TRANSITIONS,
) -> Inspection:
    return _inspect(
        repo,
        transitions,
        required_state="post",
        require_shared_exact=transitions is ARCHIVE_TRANSITIONS,
    )


def resolve_transition_read_paths(
    repo: Path = REPO,
    transitions: Sequence[dict[str, str]] = ARCHIVE_TRANSITIONS,
) -> tuple[str, ...]:
    """Resolve content readers to exactly one complete pre/post archive state."""

    normalized = validate_transitions(
        transitions, require_shared_exact=transitions is ARCHIVE_TRANSITIONS
    )
    try:
        repo = Path(repo).resolve(strict=True)
    except OSError as error:
        _fail("archive-repo-untrusted", str(error))
    index, _ = _git_inventory(repo)
    state = resolve_transition_state(
        normalized, {path: entry.blob for path, entry in index.items()}
    )
    selected = "source" if state == "pre" else "destination"
    paths: list[str] = []
    for transition in normalized:
        path = transition[selected]
        if _secure_path_state(repo, path) != "file":
            _fail("archive-path-untrusted", f"selected content path missing: {path}")
        if _hash_object(repo, path) != transition["git_blob"]:
            _fail("archive-transition-blob-mismatch", f"working bytes changed: {path}")
        paths.append(path)
    return tuple(paths)


def render_plan(transitions: Sequence[dict[str, str]]) -> bytes:
    normalized = validate_transitions(transitions)
    document = {
        "schema": PLAN_SCHEMA,
        "transitions": [
            {
                "source": entry["source"],
                "destination": entry["destination"],
                "pre_move_git_blob": entry["git_blob"],
            }
            for entry in normalized
        ],
    }
    return (
        json.dumps(document, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    ).encode("utf-8")


def _plan_target(repo: Path) -> Path:
    repo = Path(repo).resolve(strict=True)
    target = repo.joinpath(*PLAN_RELATIVE_PATH.split("/"))
    state = _secure_path_state(repo, PLAN_RELATIVE_PATH)
    if state not in {"missing", "file"}:
        _fail("archive-plan-path-untrusted", PLAN_RELATIVE_PATH)
    return target


def write_plan(
    repo: Path = REPO,
    transitions: Sequence[dict[str, str]] = ARCHIVE_TRANSITIONS,
) -> None:
    inspection = inspect_pre_move(repo, transitions)
    target = _plan_target(repo)
    atomic_write_bytes(target, render_plan(inspection.transitions))


def _read_plan(repo: Path) -> bytes:
    target = _plan_target(repo)
    if not target.is_file():
        _fail("archive-plan-missing", PLAN_RELATIVE_PATH)
    try:
        return TrustedRepoReader(repo).read_bytes(PLAN_RELATIVE_PATH)
    except ContextSurfaceError as error:
        _fail("archive-plan-path-untrusted", str(error))


def check_plan(
    repo: Path = REPO,
    transitions: Sequence[dict[str, str]] = ARCHIVE_TRANSITIONS,
) -> None:
    inspection = inspect_pre_move(repo, transitions)
    expected = render_plan(inspection.transitions)
    actual = _read_plan(repo)
    if actual != expected:
        _fail(
            "archive-plan-mismatch",
            f"expected {hashlib.sha256(expected).hexdigest()}, "
            f"found {hashlib.sha256(actual).hexdigest()}",
        )


def check_applied(
    repo: Path = REPO,
    transitions: Sequence[dict[str, str]] = ARCHIVE_TRANSITIONS,
) -> None:
    expected = render_plan(transitions)
    actual = _read_plan(repo)
    if actual != expected:
        _fail("archive-plan-mismatch", "applied transition differs from frozen plan")
    inspect_applied(repo, transitions)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write-plan", action="store_true")
    mode.add_argument("--check-plan", action="store_true")
    mode.add_argument("--check-applied", action="store_true")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.write_plan:
            write_plan()
            print(f"archive plan: PASS (wrote {PLAN_RELATIVE_PATH}; 7 safe candidates)")
        elif args.check_plan:
            check_plan()
            print("archive plan: PASS (7 safe candidates; check-only)")
        else:
            check_applied()
            print("archive applied: PASS (7 byte-identical moves; check-only)")
    except (ArchiveSafetyError, OSError, ValueError) as error:
        failures = (
            error.failures
            if isinstance(error, ArchiveSafetyError)
            else (Failure("archive-unhandled-error", str(error)),)
        )
        for failure in failures:
            print(f"[ARCHIVE] {failure}")
        label = "archive applied" if args.check_applied else "archive plan"
        print(f"{label}: FAIL ({len(failures)} blocker(s))")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
