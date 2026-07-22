#!/usr/bin/env python3
"""Build deterministic, metadata-only working views from the Stage-1B paper registry."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


def _paper(record: dict[str, Any]) -> dict[str, Any]:
    method = record.get("method_path") or {}
    return {
        "arxiv_id": record["arxiv_id"],
        "title": record.get("title"),
        "role": record["role"],
        "speech_task_tags": record.get("speech_task_tags") or [],
        "signals": method.get("signals") or [],
        "actions": method.get("actions") or [],
        "repository_status": record.get("repository_status"),
        "abstract_url": (record.get("links") or {}).get("abstract"),
    }


def build_views(records: list[dict[str, Any]]) -> dict[str, Any]:
    canonical_ids = [str(record["canonical_id"]) for record in records]
    if len(canonical_ids) != len(set(canonical_ids)):
        raise ValueError("duplicate canonical ID in registry")
    if any(record.get("schema") != "sf-paper-registry-record-v1" for record in records):
        raise ValueError("unsupported registry record schema")

    local_facets: list[dict[str, Any]] = []
    transfers: list[dict[str, Any]] = []
    negatives: list[dict[str, Any]] = []
    instruments: list[dict[str, Any]] = []

    for record in records:
        paper = _paper(record)
        role = record["role"]
        if role == "KEEP_TRANSFER" and record.get("repository_status") == "OPEN_SOURCE_VERIFIED":
            transfers.append(paper)
        if role == "KEEP_NEGATIVE":
            negative = dict(paper)
            negative["adverse_evidence"] = (record.get("method_path") or {}).get("adverse_evidence") or []
            negatives.append(negative)
        if role == "KEEP_INSTRUMENT":
            instruments.append(paper)

        if not record.get("speech_primary_object"):
            continue
        for dataset in record.get("datasets") or []:
            if not dataset.get("local_present"):
                continue
            by_task = dataset.get("task_suitability_by_tag") or {}
            for task in record.get("speech_task_tags") or []:
                if by_task.get(task) != "TASK_MATCH":
                    continue
                local_facets.append(
                    {
                        **paper,
                        "task": task,
                        "dataset": dataset.get("canonical_name"),
                        "task_suitability": "TASK_MATCH",
                    }
                )

    key = lambda item: (str(item.get("arxiv_id")), str(item.get("task", "")), str(item.get("dataset", "")))
    local_facets.sort(key=key)
    transfers.sort(key=key)
    negatives.sort(key=key)
    instruments.sort(key=key)
    role_counts = dict(sorted(Counter(record["role"] for record in records).items()))
    return {
        "schema": "sf-stage1b-registry-views-v1",
        "summary": {
            "records": len(records),
            "role_counts": role_counts,
            "local_task_match_facets": len(local_facets),
            "open_transfer_records": len(transfers),
            "negative_falsifier_records": len(negatives),
            "instrument_records": len(instruments),
        },
        "local_speech_task_match": local_facets,
        "open_transfer": transfers,
        "negative_falsifiers": negatives,
        "instruments": instruments,
    }


def run(input_path: Path | list[Path], output_path: Path) -> dict[str, Any]:
    if output_path.exists():
        raise FileExistsError(f"derived view is immutable; refusing to replace {output_path}")
    input_paths = [input_path] if isinstance(input_path, Path) else list(input_path)
    if not input_paths:
        raise ValueError("at least one registry shard is required")
    records = [
        json.loads(line)
        for path in input_paths
        for line in path.read_text("utf-8").splitlines()
        if line.strip()
    ]
    views = build_views(records)
    payload = json.dumps(views, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(payload, encoding="utf-8", newline="\n")
    return {
        **views["summary"],
        "source_registry_count": len(input_paths),
        "output_path": output_path.as_posix(),
        "output_bytes": len(payload.encode("utf-8")),
        "output_sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.input, args.output), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
