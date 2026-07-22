#!/usr/bin/env python3
"""Replay a Stage-1B manifest against Git blob bytes and frozen external files."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from sf_stage1b_release_manifest import normalize_external_path


def _resolve_commit(repo: Path, commit: str) -> str:
    resolved = subprocess.check_output(
        ["git", "-C", str(repo), "rev-parse", "--verify", f"{commit}^{{commit}}"],
        text=True,
    ).strip()
    if len(commit) != 40 or resolved != commit:
        raise ValueError(f"declared commit is not the exact resolved full SHA: {commit} -> {resolved}")
    return resolved


def _artifact_bytes(entry: dict[str, Any], repo: Path, commit: str) -> bytes:
    if entry.get("location") == "git":
        path = str(entry.get("path", ""))
        if not path or Path(path).is_absolute() or ".." in Path(path).parts:
            raise ValueError(f"unsafe Git artifact path: {path}")
        return subprocess.check_output(["git", "-C", str(repo), "show", f"{commit}:{path}"])
    if entry.get("location") == "external":
        return normalize_external_path(str(entry.get("path", ""))).read_bytes()
    raise ValueError(f"invalid artifact location: {entry.get('location')!r}")


def verify_manifest(manifest: dict[str, Any], repo: Path, commit: str) -> dict[str, Any]:
    resolved = _resolve_commit(repo, commit)
    failures: list[str] = []
    verified = 0
    git_artifacts = 0
    external_artifacts = 0
    for entry in manifest.get("artifacts", []):
        role = str(entry.get("role", "UNKNOWN"))
        if entry.get("location") == "git":
            git_artifacts += 1
        elif entry.get("location") == "external":
            external_artifacts += 1
        try:
            raw = _artifact_bytes(entry, repo, resolved)
        except (OSError, subprocess.CalledProcessError, ValueError) as error:
            failures.append(f"READ_FAILED:{role}:{error}")
            continue
        if len(raw) != entry.get("bytes"):
            failures.append(f"BYTES_MISMATCH:{role}")
            continue
        if hashlib.sha256(raw).hexdigest() != entry.get("sha256"):
            failures.append(f"SHA_MISMATCH:{role}")
            continue
        verified += 1
    return {
        "schema": "sf-stage1b-release-replay-v1",
        "release_id": manifest.get("release_id"),
        "declared_full_sha": commit,
        "resolved_full_sha": resolved,
        "total_artifacts": len(manifest.get("artifacts", [])),
        "git_artifacts": git_artifacts,
        "external_artifacts": external_artifacts,
        "verified": verified,
        "failures": failures,
        "status": "PASS" if not failures else "FAIL",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--commit", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    result = verify_manifest(manifest, args.repo, args.commit)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
