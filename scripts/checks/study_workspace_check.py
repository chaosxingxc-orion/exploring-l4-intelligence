#!/usr/bin/env python3
"""Validate semantic study repositories and the umbrella experiment asset graph."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Callable


REPO = Path(__file__).resolve().parents[2]
REGISTRY_PATH = "studies/registry.json"
CONTROL_PLANE_PATH = "wiki/Experiment-Assets.md"
INVENTORY_PATH = "docs/integrity/experiment-asset-inventory.json"
LEGACY_INVENTORY_PATH = "docs/integrity/experiment_attempt_registry.jsonl"
REGISTRY_SCHEMA = "study-repository-registry-v1"
INVENTORY_SCHEMA = "experiment-asset-inventory-v1"
FIXED_REGISTRY_FIELDS = {
    "schema": REGISTRY_SCHEMA,
    "local_root": "studies",
    "repo_creation_gate": "OWNER_GO_AND_EXECUTION_CONTRACT",
    "candidate_id_policy": "AUDIT_ONLY_NEVER_ENGINEERING_IDENTITY",
    "experiment_control_plane": CONTROL_PLANE_PATH,
}
REGISTRY_KEYS = {*FIXED_REGISTRY_FIELDS, "studies"}
STUDY_KEYS = {
    "name",
    "slug",
    "local_path",
    "github_repo",
    "lifecycle",
    "decision_record",
    "experiment_index",
}
ADMITTED_LIFECYCLES = {"engineering", "validation", "paused", "complete", "sunset"}
SEMANTIC_SLUG = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
CANDIDATE_TOKEN = re.compile(r"(?:^|-)r\d+(?:-|$)", flags=re.IGNORECASE)
CONTROL_PLANE_TERMS = (
    "experiment_id",
    "study commit",
    "config hash",
    "protocol hash",
    "model revision",
    "dataset revision",
    "mlflow run",
    "artifact location",
    "artifact hashes",
    "result summary",
    "deviations",
    "decision",
)


class StudyWorkspaceError(RuntimeError):
    """The workspace violates the admitted-study or experiment-asset contract."""


def _strict_object(pairs: list[tuple[str, object]]) -> dict:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise StudyWorkspaceError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_strict_object)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise StudyWorkspaceError(f"cannot load strict JSON {path}: {error}") from error


def _repo_path(root: Path, relative: str) -> Path:
    pure = PurePosixPath(relative)
    if pure.is_absolute() or ".." in pure.parts or "\\" in relative:
        raise StudyWorkspaceError(f"non-canonical repository path: {relative!r}")
    return root.joinpath(*pure.parts)


def _require_file(root: Path, relative: str, field: str) -> None:
    if not _repo_path(root, relative).is_file():
        raise StudyWorkspaceError(f"{field} does not name an existing file: {relative}")


def _validate_study_entry(root: Path, entry: object, index: int) -> dict:
    label = f"studies[{index}]"
    if not isinstance(entry, dict) or set(entry) != STUDY_KEYS:
        raise StudyWorkspaceError(f"{label} must have exact keys {sorted(STUDY_KEYS)}")
    if any(not isinstance(entry[key], str) or not entry[key].strip() for key in STUDY_KEYS):
        raise StudyWorkspaceError(f"{label} fields must be non-empty strings")

    slug = entry["slug"]
    if not SEMANTIC_SLUG.fullmatch(slug) or CANDIDATE_TOKEN.search(slug):
        raise StudyWorkspaceError(
            f"{label}.slug must be semantic kebab-case without candidate IDs: {slug!r}"
        )
    if entry["lifecycle"] not in ADMITTED_LIFECYCLES:
        raise StudyWorkspaceError(
            f"{label}.lifecycle is not an admitted engineering lifecycle: "
            f"{entry['lifecycle']!r}"
        )
    expected_local = f"studies/{slug}"
    if entry["local_path"] != expected_local:
        raise StudyWorkspaceError(f"{label}.local_path must equal {expected_local!r}")
    if not re.fullmatch(
        rf"https://github\.com/[^/]+/{re.escape(slug)}\.git", entry["github_repo"]
    ):
        raise StudyWorkspaceError(
            f"{label}.github_repo must be an HTTPS GitHub repository named {slug!r}"
        )

    expected_index = f"wiki/experiments/{slug}/README.md"
    if entry["experiment_index"] != expected_index:
        raise StudyWorkspaceError(f"{label}.experiment_index must equal {expected_index!r}")
    if not entry["decision_record"].startswith("wiki/"):
        raise StudyWorkspaceError(f"{label}.decision_record must live under wiki/")
    _require_file(root, entry["decision_record"], f"{label}.decision_record")
    _require_file(root, entry["experiment_index"], f"{label}.experiment_index")
    return entry


def _validate_ignore_policy(root: Path) -> None:
    try:
        lines = {
            line.strip()
            for line in (root / ".gitignore").read_text(encoding="utf-8").splitlines()
        }
    except (OSError, UnicodeError) as error:
        raise StudyWorkspaceError(f"cannot read .gitignore: {error}") from error
    if "studies/*/" not in lines:
        raise StudyWorkspaceError(".gitignore must contain exact independent-repo rule studies/*/")


def load_and_validate_registry(root: Path = REPO) -> dict:
    """Load and validate the admitted study registry and installed checkouts."""

    document = _load_json(root / REGISTRY_PATH)
    if not isinstance(document, dict) or set(document) != REGISTRY_KEYS:
        raise StudyWorkspaceError(f"{REGISTRY_PATH} has an unexpected top-level schema")
    for key, expected in FIXED_REGISTRY_FIELDS.items():
        if document[key] != expected:
            raise StudyWorkspaceError(
                f"{REGISTRY_PATH}.{key} must equal {expected!r}, found {document[key]!r}"
            )
    if not isinstance(document["studies"], list):
        raise StudyWorkspaceError(f"{REGISTRY_PATH}.studies must be a list")

    entries = [
        _validate_study_entry(root, entry, index)
        for index, entry in enumerate(document["studies"])
    ]
    for key in ("name", "slug", "local_path", "github_repo"):
        values = [entry[key] for entry in entries]
        if len(values) != len(set(values)):
            raise StudyWorkspaceError(f"duplicate admitted study {key}")

    studies_root = root / FIXED_REGISTRY_FIELDS["local_root"]
    registered = {entry["slug"] for entry in entries}
    installed = {path.name for path in studies_root.iterdir() if path.is_dir()}
    unexpected = sorted(installed - registered)
    if unexpected:
        raise StudyWorkspaceError(f"unregistered study directory: {unexpected[0]}")
    for slug in sorted(installed):
        if not (studies_root / slug / ".git").exists():
            raise StudyWorkspaceError(
                f"studies/{slug} must be an independent Git repository with .git metadata"
            )

    _validate_ignore_policy(root)
    return document


def validate_experiment_control_plane(root: Path = REPO) -> None:
    """Require the Wiki asset graph to carry every reproducibility binding."""

    try:
        text = (root / CONTROL_PLANE_PATH).read_text(encoding="utf-8").lower()
    except (OSError, UnicodeError) as error:
        raise StudyWorkspaceError(f"cannot read experiment control plane: {error}") from error
    missing = [term for term in CONTROL_PLANE_TERMS if term not in text]
    if missing:
        raise StudyWorkspaceError(
            "experiment control plane is missing required asset keys: " + ", ".join(missing)
        )


def _git_history_lookup(root: Path, recorded_path: str) -> str | None:
    parts = PurePosixPath(recorded_path).parts
    if len(parts) < 3 or parts[0] != "projects":
        return None
    owner = root / parts[0] / parts[1]
    relative = str(PurePosixPath(*parts[2:]))
    if not (owner / ".git").exists():
        return None
    completed = subprocess.run(
        ["git", "-C", str(owner), "log", "--all", "-1", "--format=%H", "--", relative],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    commit = completed.stdout.strip()
    return commit if completed.returncode == 0 and commit else None


def _load_legacy_rows(path: Path) -> list[dict]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        raise StudyWorkspaceError(f"cannot read legacy experiment inventory: {error}") from error
    rows = []
    for number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line, object_pairs_hook=_strict_object)
        except json.JSONDecodeError as error:
            raise StudyWorkspaceError(f"invalid legacy inventory line {number}: {error}") from error
        if not isinstance(row, dict) or not isinstance(row.get("path"), str):
            raise StudyWorkspaceError(f"legacy inventory line {number} lacks a string path")
        rows.append(row)
    return rows


def build_experiment_asset_inventory(
    root: Path = REPO,
    history_lookup: Callable[[str], str | None] | None = None,
) -> dict:
    """Build a deterministic summary without rewriting legacy experiment rows."""

    lookup = history_lookup or (lambda path: _git_history_lookup(root, path))
    legacy_path = root / LEGACY_INVENTORY_PATH
    rows = _load_legacy_rows(legacy_path)
    present = 0
    history_only: list[dict[str, str]] = []
    unresolved: list[str] = []
    for row in rows:
        recorded_path = row["path"]
        if _repo_path(root, recorded_path).exists():
            present += 1
            continue
        commit = lookup(recorded_path)
        if commit:
            history_only.append({"path": recorded_path, "latest_path_commit": commit})
        else:
            unresolved.append(recorded_path)

    registry_path = root / REGISTRY_PATH
    registry_sha = hashlib.sha256(registry_path.read_bytes()).hexdigest()
    legacy_sha = hashlib.sha256(legacy_path.read_bytes()).hexdigest()
    return {
        "schema": INVENTORY_SCHEMA,
        "study_registry": {
            "path": REGISTRY_PATH,
            "sha256": registry_sha,
        },
        "experiment_control_plane": CONTROL_PLANE_PATH,
        "asset_authorities": {
            "lifecycle_and_index": "umbrella-wiki",
            "code_and_config": "independent-study-git-repository",
            "large_artifacts": "SPEECHRL_DATA_DIR",
            "run_tracking": "MLflow",
        },
        "legacy_experiment_attempts": {
            "path": LEGACY_INVENTORY_PATH,
            "sha256": legacy_sha,
            "classification": "PRE_STAGE2_LEGACY_INVENTORY",
            "recorded_entries": len(rows),
            "worktree_present": present,
            "history_only": len(history_only),
            "unresolved": len(unresolved),
            "history_only_assets": history_only,
            "unresolved_assets": unresolved,
        },
    }


def _render_json(document: dict) -> str:
    return json.dumps(document, ensure_ascii=False, indent=2) + "\n"


def validate_inventory_file(root: Path = REPO) -> None:
    expected = build_experiment_asset_inventory(root)
    actual = _load_json(root / INVENTORY_PATH)
    if actual != expected:
        raise StudyWorkspaceError(
            f"{INVENTORY_PATH} is stale; run this checker with --render-inventory and apply the output"
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--render-inventory",
        action="store_true",
        help="render the deterministic experiment asset inventory to stdout",
    )
    args = parser.parse_args(argv)
    try:
        load_and_validate_registry(REPO)
        validate_experiment_control_plane(REPO)
        if args.render_inventory:
            sys.stdout.write(_render_json(build_experiment_asset_inventory(REPO)))
        else:
            validate_inventory_file(REPO)
            print("study workspace and experiment assets: PASS")
    except StudyWorkspaceError as error:
        print(f"study workspace and experiment assets: FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
