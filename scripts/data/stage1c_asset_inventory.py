#!/usr/bin/env python3
"""Build the honest three-layer speechrl-data inventory used by Stage-1C review."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any


SOURCE_CATALOG = {
    "audio2tool": ("hf:RVtech/Audio2Tool", "f1388da9a3189541ab82adac88824a0661670c43"),
    "audiocaps-qa": ("hf:AudioLLMs/audiocaps_qa_test", "LOCAL_REVISION_UNRESOLVED"),
    "auditorybench-plusplus": ("hf:HJOK/AuditoryBenchpp", "LOCAL_REVISION_UNRESOLVED"),
    "full-duplex-bench-v3": ("gdrive:1SO_4MTazWQ_jvCx0dtmpQ-t40bdd07yz", "sha256:37545bd896f81718136598cf5be25d42ea9aa22efcd91f58370938d05d7d672f"),
    "ihbench": ("hf:bosonai/IHBench", "cbd8280ab59bc4a50c48cbe0511a307fba9945cf"),
    "omni-deepsearch": ("hf:Kirito-Lab/Omni-DeepSearch", "f6fafcd1ee9e5d370379b684bee3957c27dc25ac"),
    "squtr": ("hf:SLLMCommunity/SQuTR", "LOCAL_REVISION_UNRESOLVED"),
    "voiceagentbench": ("hf:krutrim-ai-labs/VoiceAgentBench", "5ec6b7fcdaf25a1ffd5f538214d91dcf653c9ea4"),
}
AUXILIARY_PATHS = (
    "survey-fulltext",
    "repos",
    "logs",
    "mlruns",
    "outputs",
)


def _locked_paths(lock: dict[str, Any]) -> set[str]:
    return {
        str(row["local_subdir"]).replace("\\", "/")
        for key in ("datasets", "models")
        for row in lock.get(key, [])
    }


def _observed_relative_path(row: dict[str, Any]) -> str:
    """Return the recorded path identity without reconstructing it from the leaf name."""
    explicit = row.get("relative_path")
    if explicit:
        return str(explicit).replace("\\", "/").strip("/")
    local_path = str(row.get("local_path", "")).replace("\\", "/")
    prefix = "${SPEECHRL_DATA_DIR}/"
    if local_path.startswith(prefix):
        return local_path[len(prefix) :].strip("/")
    return f"{row['kind']}s/{row['name']}"


def build_inventory(
    lock: dict[str, Any], observed: list[dict[str, Any]], *, data_root: str
) -> dict[str, Any]:
    locked = _locked_paths(lock)
    by_path = {_observed_relative_path(row): row for row in observed}
    baseline_entries = [
        {**by_path[path], "layer_status": "LOCAL_BASELINE_LOCKED"}
        for path in sorted(locked & set(by_path))
    ]
    candidate_entries = [
        {**row, "layer_status": "LOCAL_CANDIDATE_UNFROZEN"}
        for path, row in sorted(by_path.items())
        if path not in locked
    ]
    return {
        "schema": "speechrl-data-layered-inventory-v1",
        "data_root": data_root,
        "claim_limit": (
            "Directory presence, file counts and byte totals only. FROZEN_BASELINE semantics come "
            "from docs/datasets.lock.json; no whole-disk content hash was recomputed."
        ),
        "layers": [
            {
                "layer_id": "FROZEN_BASELINE",
                "manifest": "docs/datasets.lock.json",
                "locked_entries": len(locked),
                "observed_entries": len(baseline_entries),
                "missing_locked_paths": sorted(locked - set(by_path)),
                "entries": baseline_entries,
            },
            {
                "layer_id": "LOCAL_CANDIDATE_UNFROZEN",
                "observed_entries": len(candidate_entries),
                "entries": candidate_entries,
            },
            {
                "layer_id": "SURVEY_AND_REPRO_AUXILIARY",
                "counting_rule": "Kept outside dataset/model totals; presence only in this inventory.",
                "entries": [],
            },
        ],
    }


def _source_metadata(path: Path, name: str) -> dict[str, str]:
    if name in SOURCE_CATALOG:
        identity, revision = SOURCE_CATALOG[name]
        return {
            "source_identity": identity,
            "revision_or_fingerprint": revision,
            "source_status": "EXACT_CATALOG_ENTRY" if "UNRESOLVED" not in revision else "SOURCE_ID_KNOWN_REVISION_UNRESOLVED",
        }
    metadata_path = path / ".hfd" / "repo_metadata.json"
    if metadata_path.is_file():
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            return {
                "source_identity": f"hf:{metadata.get('id', 'UNKNOWN')}",
                "revision_or_fingerprint": str(metadata.get("sha") or "LOCAL_REVISION_UNRESOLVED"),
                "source_status": "LOCAL_METADATA_OBSERVED",
            }
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            pass
    return {
        "source_identity": "UNRESOLVED_LOCAL_SOURCE",
        "revision_or_fingerprint": "UNRESOLVED_LOCAL_REVISION",
        "source_status": "UNRESOLVED_LOCAL_PROVENANCE",
    }


def scan_entry(path: Path, kind: str) -> dict[str, Any]:
    files = 0
    bytes_total = 0
    for root, _, names in os.walk(path, followlinks=False):
        for name in names:
            candidate = Path(root, name)
            try:
                stat = candidate.stat()
            except OSError:
                continue
            files += 1
            bytes_total += stat.st_size
    return {
        "kind": kind,
        "name": path.name,
        "local_path": f"${{SPEECHRL_DATA_DIR}}/{kind}s/{path.name}",
        "files": files,
        "bytes": bytes_total,
        **_source_metadata(path, path.name),
    }


def scan_data_root(data_root: Path, lock: dict[str, Any]) -> list[dict[str, Any]]:
    observed: list[dict[str, Any]] = []
    locked = _locked_paths(lock)
    for key, kind in (("datasets", "dataset"), ("models", "model")):
        for row in lock.get(key, []):
            relative = str(row["local_subdir"]).replace("\\", "/")
            path = data_root / relative
            if not path.is_dir():
                continue
            source = row.get("source", {})
            observed.append(
                {
                    "kind": kind,
                    "name": path.name,
                    "local_path": f"${{SPEECHRL_DATA_DIR}}/{relative}",
                    "files": row.get("files"),
                    "bytes": row.get("size_bytes"),
                    "source_identity": str(source.get("id") or source.get("hf_id") or "LOCK_SOURCE_UNRECORDED"),
                    "revision_or_fingerprint": str(row.get("revision") or "LOCK_REVISION_UNRECORDED"),
                    "source_status": "FROZEN_LOCK_RECORD",
                }
            )
    for kind in ("dataset", "model"):
        parent = data_root / f"{kind}s"
        if not parent.is_dir():
            continue
        for path in sorted((item for item in parent.iterdir() if item.is_dir()), key=lambda item: item.name):
            if f"{kind}s/{path.name}" in locked:
                continue
            observed.append(scan_entry(path, kind))
    return observed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--lock", type=Path, default=Path("docs/datasets.lock.json"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--snapshot-date", default="2026-07-22")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    lock = json.loads(args.lock.read_text(encoding="utf-8"))
    document = build_inventory(
        lock,
        scan_data_root(args.data_root, lock),
        data_root="${SPEECHRL_DATA_DIR}",
    )
    document["snapshot_date"] = args.snapshot_date
    document["layers"][2]["entries"] = [
        {
            "local_path": f"${{SPEECHRL_DATA_DIR}}/{name}",
            "present": (args.data_root / name).exists(),
        }
        for name in AUXILIARY_PATHS
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for layer in document["layers"]:
        print(f"{layer['layer_id']}: {len(layer['entries'])} entries")
    return 1 if document["layers"][0]["missing_locked_paths"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
