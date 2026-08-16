#!/usr/bin/env python3
"""Zero-state gate for the Stage-3 paper workspace (fail-closed).

The full promotion machinery (candidate bundles, promotion receipts, per-entry
schema, ``--require-installed`` checkout proof) is intentionally deferred until
the first real paper admission (Decision-Log-2026-08 continuation entries 91/92). Until that
machinery extends this checker, the paper surface is machine-frozen at zero
state: a strict empty registry, no child checkouts or stray files, the ignore
rule present, and the control-plane count equal to zero. Any registered paper
entry fails closed here, so an admission cannot bypass the promotion machinery.

Helpers are intentionally local: the shared workspace-registry library is part
of the deferred promotion machinery and must not be half-extracted for a
zero-state gate.
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


class PaperWorkspaceError(RuntimeError):
    """The paper workspace violates the zero-state promotion contract."""


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


def validate_zero_state(root: Path = REPO) -> dict:
    """Validate the machine-frozen zero state of the paper surface."""

    document = _load_json(root / REGISTRY_PATH)
    if not isinstance(document, dict) or set(document) != REGISTRY_KEYS:
        raise PaperWorkspaceError(f"{REGISTRY_PATH} must have exact keys {sorted(REGISTRY_KEYS)}")
    for key, expected in FIXED_REGISTRY_FIELDS.items():
        if document[key] != expected:
            raise PaperWorkspaceError(
                f"{REGISTRY_PATH}.{key} must equal {expected!r}, found {document[key]!r}"
            )
    if document["papers"] != []:
        raise PaperWorkspaceError(
            f"{REGISTRY_PATH}.papers must be empty: a paper admission requires the full "
            "promotion machinery (candidate bundle, receipt, per-entry schema) to extend "
            "this checker first — zero state is fail-closed"
        )

    if not (root / README_PATH).is_file():
        raise PaperWorkspaceError(f"{README_PATH} is missing from the umbrella surface")

    papers_root = root / "papers"
    for child in sorted(papers_root.iterdir()):
        if child.is_dir():
            raise PaperWorkspaceError(
                f"papers/{child.name}/ exists but no paper is admitted; unregistered or "
                "pre-created paper checkouts are refused"
            )
        if child.name not in ALLOWED_SURFACE_ENTRIES:
            raise PaperWorkspaceError(
                f"papers/{child.name} is not part of the tracked zero-state surface "
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
    if int(count_match.group(1)) != len(document["papers"]):
        raise PaperWorkspaceError(
            f"admitted-paper-count drift: {CONTROL_PLANE_PATH} says {count_match.group(1)}, "
            f"registry has {len(document['papers'])}"
        )
    return document


def main(argv: list[str] | None = None) -> int:
    argparse.ArgumentParser(description=__doc__).parse_args(argv)
    try:
        validate_zero_state(REPO)
        print("paper workspace (zero state): PASS")
    except PaperWorkspaceError as error:
        print(f"paper workspace (zero state): FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
