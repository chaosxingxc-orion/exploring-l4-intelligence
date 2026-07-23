#!/usr/bin/env python3
"""Split a revision-bound HF asset into remote, auxiliary, and extraneous bytes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


AUDIO2TOOL_REVISION = "f1388da9a3189541ab82adac88824a0661670c43"


def _manifest_rows(path: Path) -> list[tuple[int, str]]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        size, relative = line.split("\t", 1)
        rows.append((int(size), relative.replace("\\", "/")))
    return rows


def audit_hfd_asset(root: Path, *, asset_id: str, revision: str) -> dict[str, Any]:
    root = Path(root)
    manifest = root / ".hfd" / "manifest"
    rows = _manifest_rows(manifest)
    remote_paths = {relative for _, relative in rows}
    files = [path for path in root.rglob("*") if path.is_file()]
    auxiliary = [
        path for path in files if path.relative_to(root).as_posix().startswith(".hfd/")
    ]
    extraneous = [
        path
        for path in files
        if path not in auxiliary and path.relative_to(root).as_posix() not in remote_paths
    ]
    missing = sum(not (root / relative).is_file() for relative in remote_paths)
    return {
        "asset_id": asset_id,
        "revision": revision,
        "local_path": f"${{SPEECHRL_DATA_DIR}}/{root.name if asset_id == 'fixture' else 'datasets/' + root.name}",
        "remote_manifest": "${SPEECHRL_DATA_DIR}/datasets/audio2tool/.hfd/manifest",
        "remote_content": {
            "files": len(rows),
            "bytes": sum(size for size, _ in rows),
            "missing": missing,
        },
        "auxiliary_content": {
            "files": len(auxiliary),
            "bytes": sum(path.stat().st_size for path in auxiliary),
        },
        "extraneous_content": {
            "files": len(extraneous),
            "bytes": sum(path.stat().st_size for path in extraneous),
        },
        "hygiene_action": "DO_NOT_DELETE; STAGE2_LOADER_MUST_USE_REVISION_BOUND_ALLOWLIST",
        "claim_limit": "Counts only. Extraneous files remain user assets and are not treated as remote dataset content.",
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--snapshot-date", default="2026-07-23")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    row = audit_hfd_asset(
        args.data_root / "datasets" / "audio2tool",
        asset_id="audio2tool",
        revision=AUDIO2TOOL_REVISION,
    )
    document = {
        "schema": "speechrl-stage1c-asset-content-accounting-v1",
        "snapshot_date": args.snapshot_date,
        "entries": [row],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(document, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        f"audio2tool remote={row['remote_content']['files']} "
        f"auxiliary={row['auxiliary_content']['files']} "
        f"extraneous={row['extraneous_content']['files']}"
    )
    return 1 if row["remote_content"]["missing"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
