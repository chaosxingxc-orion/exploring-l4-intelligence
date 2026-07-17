#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Full-text ledger machine status + per-object locator supersession (C4C / P0-R9 MINOR-1).

The 2026-07-17 Git-Bash path-mangling incident left rows whose `stored_at`
points at C:/Program Files/Git/mnt/e/... although the bytes were relocated to
the E: data drive. A single blanket NOTE row let humans infer the new location
but machines could not dereference row-by-row (P0-R9 MINOR-1). This tool:

  --relocate   for every (arxiv_id, kind) whose LATEST successful row still
               carries a stale locator: verify the canonical E: path exists and
               its sha256 equals the ledger row's, then append one machine-
               readable supersession row
                 {"kind_of_row":"RELOCATION_SUPERSESSION", arxiv_id, kind,
                   sha256, bytes, stored_at:<canonical>, supersedes_stored_at:
                   <stale>, verified:"sha256-match", utc, access_class:
                   "LEDGER_BOOKKEEPING/NO_NETWORK"}
               Idempotent: objects whose latest row already resolves are skipped.

  (default)    emit the machine status JSON (counts NEVER hand-written again —
               commit messages must quote this file):
                 docs/checks/2026-07-18-sf-fulltext-status.json

Resolution rule: latest row per (arxiv_id, kind) by file order wins; a
RELOCATION_SUPERSESSION row counts as that object's locator authority.
No network. Exit 0 iff (default) all successful objects dereference on disk
with matching byte length, and no stale locator remains unresolved.
"""
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEDGER = os.path.join(REPO, "wiki", "survey", "2026-07-17-sf-fulltext-ledger.jsonl")
OUT = os.path.join(REPO, "docs", "checks", "2026-07-18-sf-fulltext-status.json")
STALE_PAT = re.compile(r"Program Files[/\\]Git[/\\]mnt[/\\]([a-z])[/\\]", re.I)


def canonicalize(path):
    m = STALE_PAT.search(path or "")
    if not m:
        return path
    tail = path[m.end():]
    return f"{m.group(1).upper()}:/{tail}".replace("\\", "/")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_rows():
    with open(LEDGER, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def latest_objects(rows):
    """(arxiv_id, kind) -> authoritative row (last successful fetch or
    relocation supersession, in file order)."""
    latest = {}
    for r in rows:
        aid, kind = r.get("arxiv_id"), r.get("kind")
        if not aid or not kind:
            continue
        if r.get("kind_of_row") == "RELOCATION_SUPERSESSION" or (
                r.get("http_status") == 200 and r.get("sha256")):
            latest[(aid, kind)] = r
    return latest


def relocate():
    rows = load_rows()
    latest = latest_objects(rows)
    appended, failures = [], []
    for (aid, kind), r in sorted(latest.items()):
        stored = r.get("stored_at") or ""
        if not STALE_PAT.search(stored):
            continue
        canon = canonicalize(stored)
        if not os.path.exists(canon):
            failures.append({"arxiv_id": aid, "kind": kind, "reason": f"canonical path missing: {canon}"})
            continue
        actual = sha256_file(canon)
        if actual != r["sha256"]:
            failures.append({"arxiv_id": aid, "kind": kind, "reason": "sha256 mismatch at canonical path"})
            continue
        appended.append({
            "kind_of_row": "RELOCATION_SUPERSESSION",
            "arxiv_id": aid, "kind": kind,
            "sha256": r["sha256"], "bytes": r.get("bytes"),
            "stored_at": canon, "supersedes_stored_at": stored,
            "verified": "sha256-match",
            "utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "access_class": "LEDGER_BOOKKEEPING/NO_NETWORK",
            "note": "P0-R9 MINOR-1: per-object supersession for the 2026-07-17 path-mangling incident (blanket NOTE row insufficient for machine dereference)",
        })
    if appended:
        with open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
            for row in appended:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"[relocate] appended {len(appended)} supersession rows; {len(failures)} failures")
    for x in failures:
        print("  [FAIL]", x)
    return 1 if failures else 0


def status():
    rows = load_rows()
    latest = latest_objects(rows)
    objects, missing_on_disk, stale_left = [], [], []
    for (aid, kind), r in sorted(latest.items()):
        stored = r.get("stored_at") or ""
        entry = {"arxiv_id": aid, "kind": kind, "sha256": r["sha256"],
                 "bytes": r.get("bytes"), "stored_at": stored}
        if STALE_PAT.search(stored):
            stale_left.append(entry)
        if os.path.exists(stored):
            entry["on_disk"] = os.path.getsize(stored) == r.get("bytes")
            if not entry["on_disk"]:
                missing_on_disk.append(entry)
        else:
            entry["on_disk"] = False
            missing_on_disk.append(entry)
        objects.append(entry)
    ids = sorted({aid for aid, _ in latest})
    expected = {(i, k) for i in ids for k in ("pdf", "eprint")}
    unresolved = sorted(set(expected) - set(latest))
    report = {
        "artifact_id": "SF-FULLTEXT-STATUS-2026-07-18-01",
        "generator": "scripts/survey/sf_fulltext_ledger_status.py",
        "ledger": "wiki/survey/2026-07-17-sf-fulltext-ledger.jsonl",
        "ledger_rows": len(rows),
        "distinct_ids": len(ids),
        "expected_renditions": len(expected),
        "persisted_renditions": len(latest),
        "unresolved_renditions": [{"arxiv_id": a, "kind": k} for a, k in unresolved],
        "stale_locators_remaining": stale_left,
        "on_disk_failures": missing_on_disk,
        "verdict": "PASS" if not stale_left and not missing_on_disk else "FAIL",
        "note": "counts in commit messages / prose MUST quote this machine output (P0-R9 MINOR-1: no hand-counted ledger claims)",
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "wb") as f:
        f.write((json.dumps(report, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    print(json.dumps({k: report[k] for k in ("ledger_rows", "distinct_ids", "persisted_renditions",
                                             "unresolved_renditions", "verdict")}, ensure_ascii=False))
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(relocate() if "--relocate" in sys.argv else status())
