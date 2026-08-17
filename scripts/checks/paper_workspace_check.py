#!/usr/bin/env python3
"""Admission-mode gate for the paper workspace (fail-closed).

Until 2026-08-17 this checker froze the paper surface at zero state. The first
admission (`meeting-minutes-agent`, direct owner order recorded in its
authorization record) fired the continuation-entry-92 trigger, so the checker
now validates admitted entries: exact per-entry schema, kebab-case name policy
with candidate-ID rejection, checkout existence (git repo with CLAUDE.md and
README.md), authorization-record existence, the umbrella ignore rule, and
control-plane count consistency. Unregistered checkouts and stray surface files
still fail closed. Candidate-bundle and promotion-receipt machinery remains
deferred until the first promotion-path admission.

Helpers are intentionally local: the shared workspace-registry library remains
part of the deferred promotion machinery.
"""

from __future__ import annotations

import argparse
import re
import sys
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
REGISTRY_PATH = "papers/registry.json"
README_PATH = "papers/README.md"
CONTROL_PLANE_PATH = "wiki/Experiment-Assets.md"
REGISTRY_SCHEMA = "paper-repository-registry-v1"
FIXED_REGISTRY_FIELDS = {
    "schema": REGISTRY_SCHEMA,
    "local_root": "papers",
    "repo_creation_gate": "OWNER_GO_AND_PAPER_EXECUTION_CONTRACT",
    "candidate_id_policy": "AUDIT_ONLY_NEVER_ENGINEERING_IDENTITY",
    "promotion_control_plane": CONTROL_PLANE_PATH,
}
REGISTRY_KEYS = {*FIXED_REGISTRY_FIELDS, "papers"}
ALLOWED_SURFACE_ENTRIES = {"README.md", "registry.json"}
ADMITTED_COUNT_PATTERN = re.compile(r"Admitted paper repositories: \*\*(\d+)\*\*")
ENTRY_KEYS = {"name", "local_path", "admitted", "status", "authorization"}
AUTHORIZATION_KEYS = {"kind", "record"}
AUTHORIZATION_KIND = "OWNER_GO_AND_PAPER_EXECUTION_CONTRACT"
NAME_PATTERN = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
CANDIDATE_ID_TOKEN = re.compile(r"(^|-)r\d+(-|$)")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ENTRY_STATUSES = {"PROVISIONAL", "ACTIVE", "CLOSED"}
REQUIRED_CHECKOUT_FILES = ("CLAUDE.md", "README.md")


class PaperWorkspaceError(RuntimeError):
    """The paper workspace violates the admission contract."""


def _strict_object(pairs: list[tuple[str, object]]) -> dict:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise PaperWorkspaceError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_strict_object)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise PaperWorkspaceError(f"cannot load strict JSON {path}: {error}") from error


def _validate_entry(root: Path, entry: object, position: int) -> str:
    label = f"{REGISTRY_PATH}.papers[{position}]"
    if not isinstance(entry, dict) or set(entry) != ENTRY_KEYS:
        raise PaperWorkspaceError(f"{label} must have exact keys {sorted(ENTRY_KEYS)}")
    name = entry["name"]
    if not isinstance(name, str) or not NAME_PATTERN.fullmatch(name):
        raise PaperWorkspaceError(f"{label}.name must be a kebab-case slug, found {name!r}")
    if CANDIDATE_ID_TOKEN.search(name):
        raise PaperWorkspaceError(
            f"{label}.name {name!r} contains a candidate-ID token; candidate IDs are "
            "audit-only and never an engineering identity"
        )
    if entry["local_path"] != f"papers/{name}":
        raise PaperWorkspaceError(f"{label}.local_path must equal 'papers/{name}'")
    if not isinstance(entry["admitted"], str) or not DATE_PATTERN.fullmatch(entry["admitted"]):
        raise PaperWorkspaceError(f"{label}.admitted must be a YYYY-MM-DD date")
    if entry["status"] not in ENTRY_STATUSES:
        raise PaperWorkspaceError(f"{label}.status must be one of {sorted(ENTRY_STATUSES)}")
    authorization = entry["authorization"]
    if not isinstance(authorization, dict) or set(authorization) != AUTHORIZATION_KEYS:
        raise PaperWorkspaceError(
            f"{label}.authorization must have exact keys {sorted(AUTHORIZATION_KEYS)}"
        )
    if authorization["kind"] != AUTHORIZATION_KIND:
        raise PaperWorkspaceError(
            f"{label}.authorization.kind must equal {AUTHORIZATION_KIND!r}"
        )
    record = authorization["record"]
    if not isinstance(record, str) or not (root / record).is_file():
        raise PaperWorkspaceError(
            f"{label}.authorization.record {record!r} does not exist in the umbrella"
        )
    checkout = root / "papers" / name
    if not checkout.is_dir():
        raise PaperWorkspaceError(f"papers/{name}/ is registered but has no checkout")
    if not (checkout / ".git").exists():
        raise PaperWorkspaceError(f"papers/{name}/ is not an independent git repository")
    for required in REQUIRED_CHECKOUT_FILES:
        if not (checkout / required).is_file():
            raise PaperWorkspaceError(f"papers/{name}/ is missing required file {required}")
    return name


def validate_workspace(root: Path = REPO) -> dict:
    """Validate the paper surface: fixed registry fields, admitted entries, hygiene."""

    document = _load_json(root / REGISTRY_PATH)
    if not isinstance(document, dict) or set(document) != REGISTRY_KEYS:
        raise PaperWorkspaceError(f"{REGISTRY_PATH} must have exact keys {sorted(REGISTRY_KEYS)}")
    for key, expected in FIXED_REGISTRY_FIELDS.items():
        if document[key] != expected:
            raise PaperWorkspaceError(
                f"{REGISTRY_PATH}.{key} must equal {expected!r}, found {document[key]!r}"
            )
    papers = document["papers"]
    if not isinstance(papers, list):
        raise PaperWorkspaceError(f"{REGISTRY_PATH}.papers must be a list")
    names: list[str] = []
    for position, entry in enumerate(papers):
        names.append(_validate_entry(root, entry, position))
    if len(set(names)) != len(names):
        raise PaperWorkspaceError(f"{REGISTRY_PATH}.papers contains duplicate names")

    if not (root / README_PATH).is_file():
        raise PaperWorkspaceError(f"{README_PATH} is missing from the umbrella surface")

    registered = set(names)
    papers_root = root / "papers"
    for child in sorted(papers_root.iterdir()):
        if child.is_dir():
            if child.name not in registered:
                raise PaperWorkspaceError(
                    f"papers/{child.name}/ is not a registered paper repository; "
                    "unregistered or pre-created paper checkouts are refused"
                )
        elif child.name not in ALLOWED_SURFACE_ENTRIES:
            raise PaperWorkspaceError(
                f"papers/{child.name} is not part of the tracked workspace surface "
                f"({sorted(ALLOWED_SURFACE_ENTRIES)})"
            )

    try:
        ignore_lines = {
            line.strip()
            for line in (root / ".gitignore").read_text(encoding="utf-8").splitlines()
        }
    except (OSError, UnicodeError) as error:
        raise PaperWorkspaceError(f"cannot read .gitignore: {error}") from error
    if "papers/*/" not in ignore_lines:
        raise PaperWorkspaceError(".gitignore must contain exact independent-repo rule papers/*/")

    try:
        control_plane = (root / CONTROL_PLANE_PATH).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise PaperWorkspaceError(f"cannot read promotion control plane: {error}") from error
    count_match = ADMITTED_COUNT_PATTERN.search(control_plane)
    if count_match is None:
        raise PaperWorkspaceError(
            f"{CONTROL_PLANE_PATH} must state the admitted paper count as "
            "'Admitted paper repositories: **N**'"
        )
    if int(count_match.group(1)) != len(papers):
        raise PaperWorkspaceError(
            f"admitted-paper-count drift: {CONTROL_PLANE_PATH} says {count_match.group(1)}, "
            f"registry has {len(papers)}"
        )
    return document


def main(argv: list[str] | None = None) -> int:
    argparse.ArgumentParser(description=__doc__).parse_args(argv)
    try:
        document = validate_workspace(REPO)
        print(f"paper workspace: PASS ({len(document['papers'])} admitted)")
    except PaperWorkspaceError as error:
        print(f"paper workspace: FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
