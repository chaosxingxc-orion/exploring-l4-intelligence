#!/usr/bin/env python3
"""Fail-closed resolver for legacy experiment assets recorded against retired repositories.

The 574-row pre-Stage-2 inventory (`docs/integrity/experiment_attempt_registry.jsonl`) records
paths under the retired W1-W4 checkouts. Retirement deleted those worktrees, so a two-state
worktree/history resolver reports every row unresolved. This checker upgrades resolution to four
states -- WORKTREE_PRESENT, LOCAL_GIT_HISTORY, COLD_BACKUP_RESOLVED, UNRESOLVED -- by consulting
`docs/integrity/retired-repository-registry.json` (the machine registry of retired remotes and
their frozen final commits) and binding every row to `remote@commit:path` in
`docs/integrity/legacy-asset-resolution.json`.

Default mode is offline and fail-closed: every inventory row must carry a resolution entry, and
`UNRESOLVED` entries are forbidden unless they carry a dated owner waiver. `--write` regenerates
the resolution file from local mirrors of the cold-backup remotes; `--verify-remote` additionally
checks that the registered remotes are still reachable.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath


REPO = Path(__file__).resolve().parents[2]
RETIRED_REGISTRY_PATH = "docs/integrity/retired-repository-registry.json"
RESOLUTION_PATH = "docs/integrity/legacy-asset-resolution.json"
LEGACY_INVENTORY_PATH = "docs/integrity/experiment_attempt_registry.jsonl"
RETIRED_REGISTRY_SCHEMA = "retired-repository-registry-v1"
RESOLUTION_SCHEMA = "legacy-asset-resolution-v1"
STATES = (
    "WORKTREE_PRESENT",
    "LOCAL_GIT_HISTORY",
    "COLD_BACKUP_RESOLVED",
    "UNRESOLVED",
)
COMMIT_RE = re.compile(r"[0-9a-f]{40}\Z")
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}\Z")


class LegacyResolutionError(RuntimeError):
    """The legacy-asset resolution contract is violated."""


def _strict_object(pairs: list[tuple[str, object]]) -> dict:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise LegacyResolutionError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_strict_object)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise LegacyResolutionError(f"cannot load strict JSON {path}: {error}") from error


def _require_str(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise LegacyResolutionError(f"{label} must be a non-empty string")
    return value


def _sha256(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as error:
        raise LegacyResolutionError(f"cannot hash {path}: {error}") from error


def load_retired_registry(root: Path = REPO) -> dict:
    """Load and validate the retired-repository registry."""

    document = _load_json(root / RETIRED_REGISTRY_PATH)
    if not isinstance(document, dict) or set(document) != {
        "schema",
        "retirement_ruling",
        "repositories",
    }:
        raise LegacyResolutionError(f"{RETIRED_REGISTRY_PATH} has an unexpected top-level schema")
    if document["schema"] != RETIRED_REGISTRY_SCHEMA:
        raise LegacyResolutionError(
            f"{RETIRED_REGISTRY_PATH}.schema must equal {RETIRED_REGISTRY_SCHEMA!r}"
        )
    _require_str(document["retirement_ruling"], "retirement_ruling")
    repositories = document["repositories"]
    if not isinstance(repositories, list) or not repositories:
        raise LegacyResolutionError("repositories must be a non-empty list")
    required = {
        "repo_id",
        "work_label",
        "remote",
        "final_branch",
        "final_commit",
        "local_state",
        "retention_policy",
        "verified_at",
        "tombstone",
        "legacy_path_prefix",
        "offline_bundle",
    }
    seen: set[str] = set()
    for index, entry in enumerate(repositories):
        label = f"repositories[{index}]"
        if not isinstance(entry, dict) or set(entry) != required:
            raise LegacyResolutionError(f"{label} must have exact keys {sorted(required)}")
        repo_id = _require_str(entry["repo_id"], f"{label}.repo_id")
        if repo_id in seen:
            raise LegacyResolutionError(f"duplicate repo_id {repo_id}")
        seen.add(repo_id)
        if not _require_str(entry["remote"], f"{label}.remote").startswith("https://"):
            raise LegacyResolutionError(f"{label}.remote must be an HTTPS URL")
        commit = _require_str(entry["final_commit"], f"{label}.final_commit")
        if COMMIT_RE.fullmatch(commit) is None:
            raise LegacyResolutionError(f"{label}.final_commit is not a Git commit id")
        if DATE_RE.fullmatch(_require_str(entry["verified_at"], f"{label}.verified_at")) is None:
            raise LegacyResolutionError(f"{label}.verified_at must be YYYY-MM-DD")
        tombstone = _require_str(entry["tombstone"], f"{label}.tombstone")
        if not (root / PurePosixPath(tombstone)).is_file():
            raise LegacyResolutionError(f"{label}.tombstone does not name an existing file")
        prefix = _require_str(entry["legacy_path_prefix"], f"{label}.legacy_path_prefix")
        if not prefix.startswith("projects/") or prefix.endswith("/"):
            raise LegacyResolutionError(
                f"{label}.legacy_path_prefix must look like projects/<repo> without trailing slash"
            )
        bundle = entry["offline_bundle"]
        if not isinstance(bundle, dict) or set(bundle) != {"path", "sha256"}:
            raise LegacyResolutionError(f"{label}.offline_bundle must have exact path/sha256")
        _require_str(bundle["path"], f"{label}.offline_bundle.path")
        digest = _require_str(bundle["sha256"], f"{label}.offline_bundle.sha256")
        if re.fullmatch(r"[0-9a-f]{64}", digest) is None:
            raise LegacyResolutionError(f"{label}.offline_bundle.sha256 is not SHA-256")
    return document


def _load_legacy_paths(root: Path) -> list[str]:
    path = root / LEGACY_INVENTORY_PATH
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        raise LegacyResolutionError(f"cannot read legacy inventory: {error}") from error
    paths: list[str] = []
    for number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line, object_pairs_hook=_strict_object)
        except json.JSONDecodeError as error:
            raise LegacyResolutionError(f"invalid legacy inventory line {number}: {error}") from error
        if not isinstance(row, dict) or not isinstance(row.get("path"), str):
            raise LegacyResolutionError(f"legacy inventory line {number} lacks a string path")
        paths.append(row["path"])
    return paths


def _validate_entry(entry: object, index: int, by_id: dict[str, dict]) -> dict:
    label = f"resolutions[{index}]"
    if not isinstance(entry, dict):
        raise LegacyResolutionError(f"{label} must be an object")
    state = entry.get("state")
    if state not in STATES:
        raise LegacyResolutionError(f"{label}.state must be one of {STATES}")
    _require_str(entry.get("path"), f"{label}.path")
    if state == "WORKTREE_PRESENT":
        expected = {"path", "state"}
    elif state == "UNRESOLVED":
        expected = {"path", "state", "waiver"} if "waiver" in entry else {"path", "state"}
        if "waiver" in entry:
            waiver = entry["waiver"]
            if not isinstance(waiver, dict) or set(waiver) != {
                "waived_by",
                "waived_on",
                "reason",
            }:
                raise LegacyResolutionError(
                    f"{label}: waiver must have exact waived_by/waived_on/reason"
                )
            _require_str(waiver["waived_by"], f"{label}.waiver.waived_by")
            _require_str(waiver["reason"], f"{label}.waiver.reason")
            if (
                DATE_RE.fullmatch(
                    _require_str(waiver["waived_on"], f"{label}.waiver.waived_on")
                )
                is None
            ):
                raise LegacyResolutionError(f"{label}.waiver.waived_on must be YYYY-MM-DD")
    else:
        expected = {"path", "state", "repo_id", "commit", "repo_path", "git_blob", "uri"}
        repo_id = _require_str(entry.get("repo_id"), f"{label}.repo_id")
        if repo_id not in by_id:
            raise LegacyResolutionError(f"{label}.repo_id is not a registered retired repository")
        owner = by_id[repo_id]
        commit = _require_str(entry.get("commit"), f"{label}.commit")
        if COMMIT_RE.fullmatch(commit) is None:
            raise LegacyResolutionError(f"{label}.commit is not a Git commit id")
        repo_path = _require_str(entry.get("repo_path"), f"{label}.repo_path")
        blob = _require_str(entry.get("git_blob"), f"{label}.git_blob")
        if COMMIT_RE.fullmatch(blob) is None:
            raise LegacyResolutionError(f"{label}.git_blob is not a Git blob id")
        uri = _require_str(entry.get("uri"), f"{label}.uri")
        expected_path = f"{owner['legacy_path_prefix']}/{repo_path}"
        if entry["path"] != expected_path:
            raise LegacyResolutionError(
                f"{label}: path {entry['path']!r} does not equal registered prefix + repo_path "
                f"({expected_path!r})"
            )
        expected_uri = f"git+{owner['remote']}@{commit}#path={repo_path}"
        if uri != expected_uri:
            raise LegacyResolutionError(
                f"{label}: uri {uri!r} does not equal the registered remote binding "
                f"({expected_uri!r})"
            )
    if set(entry) != expected:
        raise LegacyResolutionError(f"{label} must have exact keys {sorted(expected)}")
    return entry


def load_and_validate_resolution(root: Path = REPO) -> dict:
    """Validate coverage, schema and the fail-closed unresolved rule; return the document."""

    registry = load_retired_registry(root)
    by_id = {entry["repo_id"]: entry for entry in registry["repositories"]}
    document = _load_json(root / RESOLUTION_PATH)
    if not isinstance(document, dict) or set(document) != {
        "schema",
        "legacy_inventory",
        "retired_repository_registry",
        "summary",
        "resolutions",
    }:
        raise LegacyResolutionError(f"{RESOLUTION_PATH} has an unexpected top-level schema")
    if document["schema"] != RESOLUTION_SCHEMA:
        raise LegacyResolutionError(f"{RESOLUTION_PATH}.schema must equal {RESOLUTION_SCHEMA!r}")

    provenance = document["legacy_inventory"]
    if not isinstance(provenance, dict) or set(provenance) != {"path", "sha256"}:
        raise LegacyResolutionError("legacy_inventory must have exact path/sha256")
    if provenance["path"] != LEGACY_INVENTORY_PATH:
        raise LegacyResolutionError(f"legacy_inventory.path must equal {LEGACY_INVENTORY_PATH!r}")
    actual_inventory_sha = _sha256(root / LEGACY_INVENTORY_PATH)
    if provenance["sha256"] != actual_inventory_sha:
        raise LegacyResolutionError(
            "legacy inventory changed since resolution was generated; regenerate with --write"
        )

    registry_ref = document["retired_repository_registry"]
    if not isinstance(registry_ref, dict) or set(registry_ref) != {"path", "sha256"}:
        raise LegacyResolutionError("retired_repository_registry must have exact path/sha256")
    if registry_ref["path"] != RETIRED_REGISTRY_PATH:
        raise LegacyResolutionError(
            f"retired_repository_registry.path must equal {RETIRED_REGISTRY_PATH!r}"
        )
    if registry_ref["sha256"] != _sha256(root / RETIRED_REGISTRY_PATH):
        raise LegacyResolutionError(
            "retired repository registry changed since resolution was generated; "
            "regenerate with --write"
        )

    entries = document["resolutions"]
    if not isinstance(entries, list):
        raise LegacyResolutionError("resolutions must be a list")
    validated = [_validate_entry(entry, index, by_id) for index, entry in enumerate(entries)]
    resolved_paths = [entry["path"] for entry in validated]
    if len(resolved_paths) != len(set(resolved_paths)):
        raise LegacyResolutionError("duplicate resolution path")
    legacy_paths = _load_legacy_paths(root)
    if sorted(set(legacy_paths)) != sorted(resolved_paths):
        missing = sorted(set(legacy_paths) - set(resolved_paths))[:3]
        extra = sorted(set(resolved_paths) - set(legacy_paths))[:3]
        raise LegacyResolutionError(
            f"resolution coverage mismatch: missing={missing} extra={extra}"
        )

    summary = document["summary"]
    expected_summary = {state: 0 for state in STATES}
    expected_summary["waived"] = 0
    for entry in validated:
        expected_summary[entry["state"]] += 1
        if entry["state"] == "UNRESOLVED" and "waiver" in entry:
            expected_summary["waived"] += 1
    if summary != expected_summary:
        raise LegacyResolutionError(
            f"summary does not match entries: recorded {summary}, actual {expected_summary}"
        )

    unwaived = [
        entry["path"]
        for entry in validated
        if entry["state"] == "UNRESOLVED" and "waiver" not in entry
    ]
    if unwaived:
        raise LegacyResolutionError(f"unwaived UNRESOLVED entries: {unwaived[:3]}")
    return document


def _git(arguments: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *arguments],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def _resolve_in_mirror(mirror: Path, final_commit: str, repo_path: str) -> tuple[str, str] | None:
    """Return (commit, blob) binding repo_path to the freshest commit containing it."""

    probe = _git(["-C", str(mirror), "rev-parse", f"{final_commit}:{repo_path}"])
    if probe.returncode == 0:
        return final_commit, probe.stdout.strip()
    listing = _git(["-C", str(mirror), "rev-list", "--all", "--", repo_path])
    if listing.returncode != 0:
        return None
    for commit in listing.stdout.split():
        probe = _git(["-C", str(mirror), "rev-parse", f"{commit}:{repo_path}"])
        if probe.returncode == 0:
            return commit, probe.stdout.strip()
    return None


def build_resolution(root: Path, mirrors: Path) -> dict:
    """Regenerate the resolution document from local mirrors of the retired remotes."""

    registry = load_retired_registry(root)
    by_prefix = {entry["legacy_path_prefix"]: entry for entry in registry["repositories"]}
    entries: list[dict] = []
    summary = {state: 0 for state in STATES}
    summary["waived"] = 0
    for recorded_path in sorted(set(_load_legacy_paths(root))):
        pure = PurePosixPath(recorded_path)
        if not pure.is_absolute() and ".." not in pure.parts and (root / pure).exists():
            entries.append({"path": recorded_path, "state": "WORKTREE_PRESENT"})
            summary["WORKTREE_PRESENT"] += 1
            continue
        owner = None
        for prefix, candidate in by_prefix.items():
            if recorded_path.startswith(prefix + "/"):
                owner = candidate
                repo_path = recorded_path[len(prefix) + 1 :]
                break
        resolved = None
        if owner is not None:
            local_git = root / PurePosixPath(owner["legacy_path_prefix"]) / ".git"
            mirror = mirrors / f"{owner['repo_id']}.git"
            if local_git.exists():
                state = "LOCAL_GIT_HISTORY"
                resolved = _resolve_in_mirror(
                    root / PurePosixPath(owner["legacy_path_prefix"]),
                    owner["final_commit"],
                    repo_path,
                )
            elif mirror.is_dir():
                state = "COLD_BACKUP_RESOLVED"
                resolved = _resolve_in_mirror(mirror, owner["final_commit"], repo_path)
        if resolved is None:
            entries.append({"path": recorded_path, "state": "UNRESOLVED"})
            summary["UNRESOLVED"] += 1
            continue
        commit, blob = resolved
        entries.append(
            {
                "path": recorded_path,
                "state": state,
                "repo_id": owner["repo_id"],
                "commit": commit,
                "repo_path": repo_path,
                "git_blob": blob,
                "uri": f"git+{owner['remote']}@{commit}#path={repo_path}",
            }
        )
        summary[state] += 1
    return {
        "schema": RESOLUTION_SCHEMA,
        "legacy_inventory": {
            "path": LEGACY_INVENTORY_PATH,
            "sha256": _sha256(root / LEGACY_INVENTORY_PATH),
        },
        "retired_repository_registry": {
            "path": RETIRED_REGISTRY_PATH,
            "sha256": _sha256(root / RETIRED_REGISTRY_PATH),
        },
        "summary": summary,
        "resolutions": entries,
    }


DATA_ROOT_TOKEN = "SPEECHRL_DATA_DIR"


def _bundle_file(entry: dict, data_root: Path) -> Path:
    recorded = entry["offline_bundle"]["path"]
    if not recorded.startswith(DATA_ROOT_TOKEN + "/"):
        raise LegacyResolutionError(
            f"{entry['repo_id']}: offline_bundle.path must start with {DATA_ROOT_TOKEN}/"
        )
    return data_root / PurePosixPath(recorded[len(DATA_ROOT_TOKEN) + 1 :])


def verify_bundles(root: Path, data_root: Path, document: dict) -> dict[str, int]:
    """Prove every resolution binding from the offline bundles (no network, no trust).

    Re-hashes each registered bundle against the registry SHA-256, clones it into a
    temporary bare repository, then proves ``commit:repo_path -> git_blob`` for every
    resolved entry via ``git ls-tree`` of the recorded commit.
    """

    import tempfile

    registry = load_retired_registry(root)
    by_id = {entry["repo_id"]: entry for entry in registry["repositories"]}

    bundle_hashes = 0
    bundles: dict[str, Path] = {}
    for entry in registry["repositories"]:
        bundle = _bundle_file(entry, data_root)
        if not bundle.is_file():
            raise LegacyResolutionError(f"{entry['repo_id']}: offline bundle missing: {bundle}")
        actual = hashlib.sha256(bundle.read_bytes()).hexdigest()
        if actual != entry["offline_bundle"]["sha256"]:
            raise LegacyResolutionError(
                f"{entry['repo_id']}: offline bundle SHA-256 drift "
                f"(registry {entry['offline_bundle']['sha256'][:12]}..., actual {actual[:12]}...)"
            )
        bundles[entry["repo_id"]] = bundle
        bundle_hashes += 1

    groups: dict[tuple[str, str], list[dict]] = {}
    for entry in document["resolutions"]:
        if entry["state"] in {"COLD_BACKUP_RESOLVED", "LOCAL_GIT_HISTORY"}:
            groups.setdefault((entry["repo_id"], entry["commit"]), []).append(entry)

    bindings = 0
    needed_repos = {repo_id for repo_id, _ in groups}
    with tempfile.TemporaryDirectory(prefix="legacy-bundle-verify-") as scratch:
        clones: dict[str, Path] = {}
        for repo_id in sorted(needed_repos):
            clone = Path(scratch) / f"{repo_id}.git"
            completed = _git(
                ["clone", "--bare", "--quiet", str(bundles[repo_id]), str(clone)]
            )
            if completed.returncode != 0:
                raise LegacyResolutionError(
                    f"{repo_id}: cannot clone offline bundle: {completed.stderr.strip()}"
                )
            probe = _git(
                ["-C", str(clone), "cat-file", "-e", by_id[repo_id]["final_commit"] + "^{commit}"]
            )
            if probe.returncode != 0:
                raise LegacyResolutionError(
                    f"{repo_id}: registered final commit is not contained in the offline bundle"
                )
            clones[repo_id] = clone

        for (repo_id, commit), members in sorted(groups.items()):
            listing = _git(["-C", str(clones[repo_id]), "ls-tree", "-r", "-z", commit])
            if listing.returncode != 0:
                raise LegacyResolutionError(
                    f"{repo_id}: commit {commit[:12]}... is unreachable in the offline bundle"
                )
            tree: dict[str, str] = {}
            for record in listing.stdout.split("\0"):
                if not record:
                    continue
                metadata, _, path = record.partition("\t")
                fields = metadata.split(" ")
                if len(fields) == 3 and fields[1] == "blob":
                    tree[path] = fields[2]
            for member in members:
                actual_blob = tree.get(member["repo_path"])
                if actual_blob != member["git_blob"]:
                    raise LegacyResolutionError(
                        f"{member['path']}: bundle disproves the binding "
                        f"(recorded blob {member['git_blob'][:12]}..., "
                        f"bundle has {str(actual_blob)[:12]}... at "
                        f"{commit[:12]}...:{member['repo_path']})"
                    )
                bindings += 1

    return {"bindings": bindings, "bundle_hashes": bundle_hashes}


def verify_remote(root: Path = REPO) -> list[str]:
    """Best-effort network verification that registered remotes are still reachable."""

    problems: list[str] = []
    registry = load_retired_registry(root)
    for entry in registry["repositories"]:
        listing = _git(["ls-remote", entry["remote"], f"refs/heads/{entry['final_branch']}"])
        if listing.returncode != 0:
            problems.append(f"{entry['repo_id']}: remote unreachable: {listing.stderr.strip()}")
            continue
        tip = listing.stdout.split("\t", 1)[0].strip()
        if tip != entry["final_commit"]:
            print(
                f"note: {entry['repo_id']} branch tip {tip[:12]} drifted from frozen "
                f"final commit {entry['final_commit'][:12]} (frozen commit still authoritative)"
            )
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        action="store_true",
        help="regenerate the resolution file from local cold-backup mirrors",
    )
    parser.add_argument(
        "--mirrors",
        type=Path,
        default=None,
        help="directory containing <repo_id>.git mirrors (required with --write)",
    )
    parser.add_argument(
        "--verify-remote",
        action="store_true",
        help="additionally verify the registered remotes are reachable (network)",
    )
    parser.add_argument(
        "--verify-bundles",
        action="store_true",
        help=(
            "offline semantic proof: re-hash the registered bundles and prove every "
            "commit:repo_path -> git_blob binding from them (primary dev machine default)"
        ),
    )
    parser.add_argument(
        "--data-root",
        type=Path,
        default=None,
        help=(
            f"root that the {'SPEECHRL_DATA_DIR'} token in bundle paths resolves against "
            "(default: the SPEECHRL_DATA_DIR environment variable)"
        ),
    )
    args = parser.parse_args(argv)
    try:
        if args.write:
            if args.mirrors is None:
                raise LegacyResolutionError("--write requires --mirrors <dir>")
            document = build_resolution(REPO, args.mirrors)
            target = REPO / RESOLUTION_PATH
            target.write_text(
                json.dumps(document, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
                newline="\n",
            )
            print(f"wrote {RESOLUTION_PATH}: {document['summary']}")
        document = load_and_validate_resolution(REPO)
        if args.verify_bundles:
            data_root = args.data_root or (
                Path(os.environ["SPEECHRL_DATA_DIR"])
                if os.environ.get("SPEECHRL_DATA_DIR")
                else None
            )
            if data_root is None:
                raise LegacyResolutionError(
                    "--verify-bundles needs --data-root or the SPEECHRL_DATA_DIR environment "
                    "variable to locate the offline bundles"
                )
            proof = verify_bundles(REPO, data_root, document)
            print(f"{proof['bindings']} bindings verified")
            print(f"{document['summary']['UNRESOLVED']} unresolved")
            print(f"{document['summary']['waived']} waived")
            print(f"{proof['bundle_hashes']} bundle hashes verified")
        if args.verify_remote:
            problems = verify_remote(REPO)
            if problems:
                raise LegacyResolutionError("; ".join(problems))
        print(f"legacy asset resolution: PASS {document['summary']}")
    except LegacyResolutionError as error:
        print(f"legacy asset resolution: FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
