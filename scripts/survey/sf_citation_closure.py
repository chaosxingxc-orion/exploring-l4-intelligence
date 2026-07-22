#!/usr/bin/env python3
"""Build a bounded direct/core citation ledger from local arXiv e-print sources."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import re
import tarfile
from pathlib import Path
from typing import Any


ARXIV_ID = re.compile(r"\b(\d{4}\.\d{4,5})(?:v\d+)?\b")


def _text_members(blob: bytes) -> dict[str, str]:
    members: dict[str, str] = {}
    try:
        with tarfile.open(fileobj=io.BytesIO(blob), mode="r:*") as archive:
            for member in archive.getmembers():
                if member.isfile() and re.search(r"\.(?:tex|bbl|bib)$", member.name, re.I):
                    source = archive.extractfile(member)
                    if source is not None:
                        members[member.name] = source.read().decode("utf-8", "replace")
        return members
    except tarfile.TarError:
        pass
    try:
        members["(gzipped-single-file).tex"] = gzip.decompress(blob).decode("utf-8", "replace")
    except OSError:
        members["(raw-bytes-as-text).tex"] = blob.decode("utf-8", "replace")
    return members


def extract_backward_arxiv_ids(blob: bytes, target_id: str) -> dict[str, Any]:
    members = _text_members(blob)
    bibliography = {
        name: text for name, text in members.items() if re.search(r"\.(?:bbl|bib)$", name, re.I)
    }
    selected = bibliography or members
    scope = "bbl/bib members" if bibliography else "all text members (no bbl/bib found)"
    text = "\n".join(selected[name] for name in sorted(selected))
    ids = sorted(set(ARXIV_ID.findall(text)) - {target_id})
    return {
        "scope": scope,
        "text_members": len(members),
        "bibliography_members": len(bibliography),
        "bibliography_entries_approx": len(re.findall(r"\\bibitem\b|@\w+\s*\{", text)),
        "arxiv_ids": ids,
    }


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line.strip()]


def run(
    targets_path: Path,
    eprint_root: Path,
    known_paths: list[Path],
    output_path: Path,
    summary_path: Path,
) -> dict[str, Any]:
    targets = json.loads(targets_path.read_text("utf-8")).get("targets", [])
    ids = [str(row["arxiv_id"]) for row in targets]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate citation-closure target")
    known_ids = {
        str(row["arxiv_id"])
        for path in known_paths
        for row in _read_jsonl(path)
        if row.get("arxiv_id")
    }
    rows = []
    for target in sorted(targets, key=lambda row: str(row["arxiv_id"])):
        aid = str(target["arxiv_id"])
        path = eprint_root / aid / f"{aid}.eprint"
        if not path.is_file():
            rows.append({
                "schema": "sf-stage1b-citation-closure-v1",
                **target,
                "backward_status": "EPRINT_MISSING",
                "forward_status": "WAIVED_PUBLIC_INDEX_RATE_LIMITED",
                "unresolved": True,
            })
            continue
        blob = path.read_bytes()
        extracted = extract_backward_arxiv_ids(blob, aid)
        cited = extracted.pop("arxiv_ids")
        rows.append({
            "schema": "sf-stage1b-citation-closure-v1",
            **target,
            "eprint_bytes": len(blob),
            "eprint_sha256": hashlib.sha256(blob).hexdigest(),
            "backward_status": "EXECUTED_ARXIV_ID_SUBSET",
            "backward_extraction": extracted,
            "backward_arxiv_ids": cited,
            "known_backward_ids": sorted(set(cited) & known_ids),
            "new_backward_ids": sorted(set(cited) - known_ids),
            "forward_status": "WAIVED_PUBLIC_INDEX_RATE_LIMITED",
            "forward_attempt": {
                "provider": "Semantic Scholar Graph API",
                "access": "public unauthenticated known-ID request",
                "observed_http_status": 429,
                "date": "2026-07-22",
            },
            "forward_waiver_impact": (
                "Forward-citation omissions may remain, especially for venue-only identities; no "
                "zero-new-citation or literature-closure claim is permitted."
            ),
            "unresolved": False,
        })
    payload = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(payload, encoding="utf-8", newline="\n")
    summary = {
        "schema": "sf-stage1b-citation-closure-summary-v1",
        "targets": len(rows),
        "backward_executed": sum(row["backward_status"] == "EXECUTED_ARXIV_ID_SUBSET" for row in rows),
        "forward_waived": sum(row["forward_status"] == "WAIVED_PUBLIC_INDEX_RATE_LIMITED" for row in rows),
        "unresolved_targets": sum(bool(row["unresolved"]) for row in rows),
        "unique_backward_arxiv_ids": len({
            cited for row in rows for cited in row.get("backward_arxiv_ids", [])
        }),
        "unique_new_backward_arxiv_ids": len({
            cited for row in rows for cited in row.get("new_backward_ids", [])
        }),
        "ledger": output_path.as_posix(),
        "ledger_bytes": len(payload.encode("utf-8")),
        "ledger_sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
        "limitation": (
            "Backward closure covers regex-resolvable arXiv IDs in local e-print bibliography "
            "members. DOI/title-only edges and all forward edges are not closed; those omissions "
            "prohibit a universal no-neighbor claim."
        ),
    }
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--targets", type=Path, required=True)
    parser.add_argument("--eprint-root", type=Path, required=True)
    parser.add_argument("--known", type=Path, action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.targets, args.eprint_root, args.known, args.output, args.summary),
                     ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
