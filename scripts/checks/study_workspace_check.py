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
RESOLUTION_PATH = "docs/integrity/legacy-asset-resolution.json"
RESEARCH_OBJECTIVE_PATH = "wiki/Research-Objective.md"
REGISTRY_SCHEMA = "study-repository-registry-v2"
INVENTORY_SCHEMA = "experiment-asset-inventory-v3"
PAPER_REGISTRY_PATH = "papers/registry.json"
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
    "default_branch",
    "package_name",
    "created_at",
    "experiment_namespace",
    "lifecycle",
    "decision_record",
    "decision_record_blob",
    "experiment_index",
}
ADMITTED_LIFECYCLES = {"engineering", "validation", "paused", "complete", "sunset"}
INSTALL_REQUIRED_LIFECYCLES = {"engineering", "validation"}
SEMANTIC_SLUG = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
CANDIDATE_TOKEN = re.compile(r"(?:^|-)r\d+(?:-|$)", flags=re.IGNORECASE)
DATE_FIELD = re.compile(r"\d{4}-\d{2}-\d{2}\Z")
BLOB_ID = re.compile(r"[0-9a-f]{40}\Z")
EXPERIMENT_NAMESPACE = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*$")
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
    "shared code revision",
    "split role",
    "split identity hash",
    "consumed",
    "deviations",
    "decision",
)
REQUIRED_LEDGER_COLUMNS = ("split role", "split identity hash", "consumed")


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

    if not SEMANTIC_SLUG.fullmatch(entry["default_branch"] or "") and entry[
        "default_branch"
    ] not in {"master", "main"}:
        raise StudyWorkspaceError(f"{label}.default_branch is not a plausible branch name")
    if CANDIDATE_TOKEN.search(entry["package_name"]):
        raise StudyWorkspaceError(f"{label}.package_name must not embed candidate IDs")
    if DATE_FIELD.fullmatch(entry["created_at"]) is None:
        raise StudyWorkspaceError(f"{label}.created_at must be YYYY-MM-DD")
    namespace = entry["experiment_namespace"]
    if not EXPERIMENT_NAMESPACE.fullmatch(namespace) or re.search(
        r"(?:^|-)R\d+(?:-|$)", namespace
    ):
        raise StudyWorkspaceError(
            f"{label}.experiment_namespace must be an uppercase namespace without candidate IDs"
        )
    if BLOB_ID.fullmatch(entry["decision_record_blob"]) is None:
        raise StudyWorkspaceError(f"{label}.decision_record_blob is not a Git blob id")

    expected_index = f"wiki/experiments/{slug}/README.md"
    if entry["experiment_index"] != expected_index:
        raise StudyWorkspaceError(f"{label}.experiment_index must equal {expected_index!r}")
    if not entry["decision_record"].startswith("wiki/"):
        raise StudyWorkspaceError(f"{label}.decision_record must live under wiki/")
    _require_file(root, entry["decision_record"], f"{label}.decision_record")
    _require_file(root, entry["experiment_index"], f"{label}.experiment_index")

    decision_raw = _repo_path(root, entry["decision_record"]).read_bytes().replace(b"\r\n", b"\n")
    actual_blob = hashlib.sha1(
        f"blob {len(decision_raw)}\0".encode("ascii") + decision_raw
    ).hexdigest()
    if actual_blob != entry["decision_record_blob"]:
        raise StudyWorkspaceError(
            f"{label}.decision_record_blob drift: registry pins "
            f"{entry['decision_record_blob']}, worktree is {actual_blob}"
        )
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


def _study_git(checkout: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(checkout), *arguments],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if completed.returncode != 0:
        raise StudyWorkspaceError(
            f"git {' '.join(arguments)} failed in {checkout.name}: "
            f"{completed.stderr.strip() or 'nonzero exit'}"
        )
    return completed.stdout.strip()


def _validate_installed_checkout(
    studies_root: Path, entry: dict, *, require_installed: bool
) -> None:
    checkout = studies_root / entry["slug"]
    if not checkout.is_dir():
        if require_installed and entry["lifecycle"] in INSTALL_REQUIRED_LIFECYCLES:
            raise StudyWorkspaceError(
                f"registered study {entry['slug']} ({entry['lifecycle']}) is not installed"
            )
        return
    if not (checkout / ".git").exists():
        raise StudyWorkspaceError(
            f"studies/{entry['slug']} must be an independent Git repository with .git metadata"
        )
    toplevel = Path(_study_git(checkout, "rev-parse", "--show-toplevel"))
    if toplevel.resolve() != checkout.resolve():
        raise StudyWorkspaceError(
            f"studies/{entry['slug']}/.git is not a real repository root "
            f"(git resolves to {toplevel})"
        )
    if require_installed:
        origin = _study_git(checkout, "remote", "get-url", "origin")
        if origin != entry["github_repo"]:
            raise StudyWorkspaceError(
                f"studies/{entry['slug']} origin {origin!r} does not match registry "
                f"{entry['github_repo']!r}"
            )
        branch = _study_git(checkout, "symbolic-ref", "--short", "HEAD")
        if branch != entry["default_branch"]:
            raise StudyWorkspaceError(
                f"studies/{entry['slug']} is on branch {branch!r}, registry default is "
                f"{entry['default_branch']!r}"
            )


def load_and_validate_registry(root: Path = REPO, *, require_installed: bool = False) -> dict:
    """Load and validate the admitted study registry and installed checkouts.

    Default mode tolerates a registered-but-uninstalled private study while still
    validating registry, wiki bindings and any installed checkout's Git reality.
    ``require_installed`` additionally demands every engineering/validation study
    be installed with matching origin and default branch.
    """

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
    for entry in entries:
        _validate_installed_checkout(studies_root, entry, require_installed=require_installed)

    _validate_ignore_policy(root)
    return document


def _parse_frontmatter(text: str, label: str) -> dict[str, str]:
    match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", text, flags=re.DOTALL)
    if match is None:
        raise StudyWorkspaceError(f"{label} lacks a YAML frontmatter block")
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip():
            continue
        key, separator, value = line.partition(":")
        if not separator:
            continue
        fields[key.strip()] = value.strip().strip('"')
    return fields


def validate_cross_source_truth(root: Path = REPO) -> None:
    """Assert registry, Experiment-Assets, HOT endpoint and index frontmatter agree."""

    document = _load_json(root / REGISTRY_PATH)
    entries = document["studies"] if isinstance(document, dict) else []
    if not isinstance(entries, list):
        raise StudyWorkspaceError(f"{REGISTRY_PATH}.studies must be a list")

    try:
        control_plane = (root / CONTROL_PLANE_PATH).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise StudyWorkspaceError(f"cannot read experiment control plane: {error}") from error
    count_match = re.search(r"Admitted study repositories: \*\*(\d+)\*\*", control_plane)
    if count_match is None:
        raise StudyWorkspaceError(
            f"{CONTROL_PLANE_PATH} must state the admitted study count as "
            "'Admitted study repositories: **N**'"
        )
    if int(count_match.group(1)) != len(entries):
        raise StudyWorkspaceError(
            f"admitted-count drift: {CONTROL_PLANE_PATH} says {count_match.group(1)}, "
            f"registry has {len(entries)}"
        )

    try:
        hot = (root / RESEARCH_OBJECTIVE_PATH).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise StudyWorkspaceError(f"cannot read HOT endpoint page: {error}") from error

    for entry in entries:
        if not isinstance(entry, dict):
            continue
        slug = entry.get("slug", "")
        if entry.get("lifecycle") in INSTALL_REQUIRED_LIFECYCLES and slug not in hot:
            raise StudyWorkspaceError(
                f"HOT endpoint {RESEARCH_OBJECTIVE_PATH} does not mention active study {slug}"
            )
        index_path = _repo_path(root, entry.get("experiment_index", ""))
        frontmatter = _parse_frontmatter(
            index_path.read_text(encoding="utf-8"), entry.get("experiment_index", "")
        )
        expectations = (
            ("study_slug", slug, lambda actual, expected: actual == expected),
            (
                "study_repo",
                entry.get("github_repo", ""),
                lambda actual, expected: actual == expected,
            ),
            (
                "local_checkout",
                entry.get("local_path", ""),
                lambda actual, expected: actual == expected,
            ),
            (
                "experiment_id_namespace",
                entry.get("experiment_namespace", ""),
                lambda actual, expected: actual.startswith(expected),
            ),
        )
        for key, expected, accept in expectations:
            actual = frontmatter.get(key)
            if actual is None or not accept(actual, expected):
                raise StudyWorkspaceError(
                    f"experiment index frontmatter drift for {slug}: {key}={actual!r} "
                    f"does not match registry {expected!r}"
                )
        index_text = index_path.read_text(encoding="utf-8").lower()
        missing_columns = [
            column for column in REQUIRED_LEDGER_COLUMNS if column not in index_text
        ]
        if missing_columns:
            raise StudyWorkspaceError(
                f"experiment index for {slug} lacks required exposure ledger columns "
                f"{missing_columns}; formal records must carry split role, split identity "
                "hash and a consumed marker from the first row (2026-08-03 visibility rule)"
            )


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


def _load_cold_backup_resolution(root: Path) -> tuple[dict[str, dict], str | None]:
    """Load the retired-remote resolution map produced by legacy_asset_resolution_check."""

    resolution_path = root / RESOLUTION_PATH
    if not resolution_path.is_file():
        return {}, None
    document = _load_json(resolution_path)
    if not isinstance(document, dict) or not isinstance(document.get("resolutions"), list):
        raise StudyWorkspaceError(f"{RESOLUTION_PATH} has an unexpected schema")
    resolution_map: dict[str, dict] = {}
    for entry in document["resolutions"]:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            raise StudyWorkspaceError(f"{RESOLUTION_PATH} contains a malformed entry")
        resolution_map[entry["path"]] = entry
    return resolution_map, hashlib.sha256(resolution_path.read_bytes()).hexdigest()


def build_experiment_asset_inventory(
    root: Path = REPO,
    history_lookup: Callable[[str], str | None] | None = None,
    resolution_lookup: dict[str, dict] | None = None,
) -> dict:
    """Build a deterministic summary without rewriting legacy experiment rows.

    Resolution is four-state: WORKTREE_PRESENT, LOCAL_GIT_HISTORY, COLD_BACKUP_RESOLVED
    (via the retired-repository resolution file) and UNRESOLVED (fail-closed downstream
    unless the resolution entry carries a dated waiver).
    """

    lookup = history_lookup or (lambda path: _git_history_lookup(root, path))
    if resolution_lookup is None:
        resolution_map, resolution_sha = _load_cold_backup_resolution(root)
    else:
        resolution_map, resolution_sha = resolution_lookup, None
    legacy_path = root / LEGACY_INVENTORY_PATH
    rows = _load_legacy_rows(legacy_path)
    present = 0
    local_history: list[dict[str, str]] = []
    cold_backup = 0
    waived: list[str] = []
    unresolved: list[str] = []
    for row in rows:
        recorded_path = row["path"]
        if _repo_path(root, recorded_path).exists():
            present += 1
            continue
        commit = lookup(recorded_path)
        if commit:
            local_history.append({"path": recorded_path, "latest_path_commit": commit})
            continue
        resolution = resolution_map.get(recorded_path)
        if resolution is not None and resolution.get("state") == "COLD_BACKUP_RESOLVED":
            cold_backup += 1
        elif (
            resolution is not None
            and resolution.get("state") == "UNRESOLVED"
            and isinstance(resolution.get("waiver"), dict)
        ):
            waived.append(recorded_path)
        else:
            unresolved.append(recorded_path)

    registry_path = root / REGISTRY_PATH
    registry_sha = hashlib.sha256(registry_path.read_bytes()).hexdigest()
    paper_registry_path = root / PAPER_REGISTRY_PATH
    try:
        paper_registry_sha = hashlib.sha256(paper_registry_path.read_bytes()).hexdigest()
    except OSError as error:
        raise StudyWorkspaceError(
            f"cannot read paper registry {PAPER_REGISTRY_PATH}: {error}"
        ) from error
    legacy_sha = hashlib.sha256(legacy_path.read_bytes()).hexdigest()
    return {
        "schema": INVENTORY_SCHEMA,
        "study_registry": {
            "path": REGISTRY_PATH,
            "sha256": registry_sha,
        },
        "paper_registry": {
            "path": PAPER_REGISTRY_PATH,
            "sha256": paper_registry_sha,
        },
        "experiment_control_plane": CONTROL_PLANE_PATH,
        "asset_authorities": {
            "lifecycle_and_index": "umbrella-wiki",
            "code_and_config": "independent-study-git-repository",
            "stage3_confirmatory_and_publication": (
                "independent-paper-git-repository (promotion-gated; none admitted)"
            ),
            "large_artifacts": "SPEECHRL_DATA_DIR",
            "run_tracking": "MLflow",
        },
        "legacy_experiment_attempts": {
            "path": LEGACY_INVENTORY_PATH,
            "sha256": legacy_sha,
            "classification": "PRE_STAGE2_LEGACY_INVENTORY",
            "resolution_source": {
                "path": RESOLUTION_PATH,
                "sha256": resolution_sha,
            },
            "recorded_entries": len(rows),
            "worktree_present": present,
            "local_git_history": len(local_history),
            "cold_backup_resolved": cold_backup,
            "waived_unresolved": len(waived),
            "unresolved": len(unresolved),
            "local_git_history_assets": local_history,
            "waived_unresolved_assets": waived,
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


def enforce_legacy_fail_closed(root: Path = REPO) -> None:
    """Fail when any legacy row is unresolved without a dated waiver (P0-2 rule)."""

    summary = build_experiment_asset_inventory(root)["legacy_experiment_attempts"]
    if summary["unresolved"] > 0:
        sample = summary["unresolved_assets"][:3]
        raise StudyWorkspaceError(
            f"{summary['unresolved']} legacy assets are UNRESOLVED without a waiver "
            f"(fail-closed); first offenders: {sample}. Regenerate or waive via "
            f"{RESOLUTION_PATH} (scripts/checks/legacy_asset_resolution_check.py)."
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--render-inventory",
        action="store_true",
        help="render the deterministic experiment asset inventory to stdout",
    )
    parser.add_argument(
        "--require-installed",
        action="store_true",
        help=(
            "require every engineering/validation study to be installed with matching "
            "origin and default branch (primary development machine mode)"
        ),
    )
    args = parser.parse_args(argv)
    try:
        load_and_validate_registry(REPO, require_installed=args.require_installed)
        validate_experiment_control_plane(REPO)
        validate_cross_source_truth(REPO)
        if args.render_inventory:
            sys.stdout.write(_render_json(build_experiment_asset_inventory(REPO)))
        else:
            validate_inventory_file(REPO)
            enforce_legacy_fail_closed(REPO)
            print("study workspace and experiment assets: PASS")
    except StudyWorkspaceError as error:
        print(f"study workspace and experiment assets: FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
