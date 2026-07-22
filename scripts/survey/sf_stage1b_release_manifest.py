#!/usr/bin/env python3
"""Materialize a deterministic hash manifest for the Stage-1B closeout release."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import subprocess
from pathlib import Path
from typing import Any


WINDOWS_DRIVE_RE = re.compile(r"^([A-Za-z]):[\\/](.*)$")


def normalize_external_path(raw: str | Path, *, is_wsl: bool | None = None) -> Path:
    text = str(raw)
    if is_wsl is None:
        is_wsl = bool(os.environ.get("WSL_DISTRO_NAME")) or "microsoft" in platform.release().casefold()
    match = WINDOWS_DRIVE_RE.match(text)
    if is_wsl and match:
        drive, remainder = match.groups()
        return Path("/mnt") / drive.casefold() / remainder.replace("\\", "/")
    return Path(text)


def _artifact_path(entry: dict[str, Any], root: Path) -> Path:
    location = entry.get("location")
    raw = Path(str(entry["path"]))
    if location == "git":
        if raw.is_absolute() or ".." in raw.parts:
            raise ValueError(f"unsafe Git artifact path: {raw}")
        path = root.joinpath(raw)
        try:
            path.resolve().relative_to(root.resolve())
        except ValueError as exc:
            raise ValueError(f"Git artifact escapes repository: {raw}") from exc
        return path
    if location == "external":
        return normalize_external_path(str(entry["path"]))
    raise ValueError(f"invalid artifact location: {location!r}")


def _artifact_bytes(entry: dict[str, Any], root: Path, path: Path) -> bytes:
    if entry.get("location") == "git":
        relative = str(entry["path"]).replace("\\", "/")
        indexed = subprocess.run(
            ["git", "-C", str(root), "show", f":{relative}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if indexed.returncode == 0:
            return indexed.stdout
    return path.read_bytes()


def materialize(spec: dict[str, Any], root: Path) -> dict[str, Any]:
    entries = list(spec.get("artifacts", []))
    roles = [str(entry.get("role", "")) for entry in entries]
    paths = [str(entry.get("path", "")) for entry in entries]
    if not spec.get("release_id"):
        raise ValueError("release_id is required")
    if len(roles) != len(set(roles)) or len(paths) != len(set(paths)):
        raise ValueError("duplicate artifact role or path")
    artifacts = []
    for entry in sorted(entries, key=lambda value: (str(value["location"]), str(value["path"]))):
        path = _artifact_path(entry, root)
        if not path.is_file():
            raise FileNotFoundError(path)
        raw = _artifact_bytes(entry, root, path)
        artifacts.append({
            **entry,
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
        })
    passthrough = {
        key: value for key, value in spec.items()
        if key not in {"artifacts", "commit_binding", "schema"}
    }
    return {
        "schema": "sf-stage1b-release-manifest-v1",
        **passthrough,
        "commit_binding": {
            "mode": "CONTAINING_GIT_COMMIT",
            "resolution": (
                "Use the Git commit containing this manifest; verify every location=git entry "
                "with git show <commit>:<path> and the recorded SHA-256."
            ),
            "correction_policy": "DATED_SUPERSEDING_RELEASE_ONLY",
        },
        "artifacts": artifacts,
    }


def run(spec_path: Path, root: Path, output_path: Path) -> dict[str, Any]:
    spec = json.loads(spec_path.read_text("utf-8"))
    document = materialize(spec, root)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return document


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    document = run(args.spec, args.repo, args.output)
    print(json.dumps({
        "release_id": document["release_id"],
        "artifacts": len(document["artifacts"]),
        "git_artifacts": sum(row["location"] == "git" for row in document["artifacts"]),
        "external_artifacts": sum(row["location"] == "external" for row in document["artifacts"]),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
