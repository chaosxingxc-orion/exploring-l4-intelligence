#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Raw arXiv Atom provenance fetcher (correction #4B / P0-4.1).

Fetches the RAW Atom API response for each requested arXiv ID and persists the
exact bytes — this is the artifact that makes the word "verbatim" legitimate in
the evidence chain (doctoral re-review #4A MINOR-1: rendered abs-page text had
been called "verbatim"; raw bytes + hash are the only defensible referent).

Per ID:
  docs/survey-provenance/atom/<id>.xml       — exact response bytes, untouched
  docs/survey-provenance/atom-ledger.jsonl   — append-only row: id, url, utc,
      http_status, bytes, sha256, attempts   (access class: ID_DEREFERENCE /
      PROVENANCE_FETCH — known-ID dereference, NOT a discovery query)

Politeness: export.arxiv.org, >=3s between requests, exponential backoff on
failure (max 4 attempts). Network script — run deliberately, never from the
package summary; downstream validators only verify the persisted bytes.

Usage (from repo root):
  python scripts/survey/sf_atom_provenance_fetch.py <id> [<id> ...]
  python scripts/survey/sf_atom_provenance_fetch.py --sentinel-data   # all IDs
Exit 0 iff every requested ID yielded a persisted, non-empty, parseable entry.
"""
import hashlib
import json
import os
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_DIR = os.path.join(REPO, "docs", "survey-provenance", "atom")
LEDGER = os.path.join(REPO, "docs", "survey-provenance", "atom-ledger.jsonl")
SENTINEL_DATA = os.path.join(REPO, "wiki", "survey", "2026-07-16-sf-sentinel-data.json")
API = "https://export.arxiv.org/api/query?id_list={aid}&max_results=1"
UA = "speech-mllm-training-free-rl survey provenance fetcher (stdlib urllib)"
SPACING_S = 3.0
MAX_ATTEMPTS = 4
ATOM_NS = "{http://www.w3.org/2005/Atom}"


def fetch_one(aid):
    url = API.format(aid=aid)
    last_err = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as resp:
                body = resp.read()
                return url, resp.status, body, attempt, None
        except Exception as e:  # noqa: BLE001 — retried, then reported in ledger
            last_err = f"{type(e).__name__}: {e}"
            time.sleep(SPACING_S * (2 ** (attempt - 1)))
    return url, None, b"", MAX_ATTEMPTS, last_err


def atom_entry_ok(body, aid):
    """Parseable Atom feed containing exactly one entry whose id ends with the
    requested arXiv id (any version suffix)."""
    try:
        root = ET.fromstring(body)
    except ET.ParseError:
        return False, "unparseable XML"
    entries = root.findall(f"{ATOM_NS}entry")
    if len(entries) != 1:
        return False, f"expected 1 entry, got {len(entries)}"
    id_el = entries[0].find(f"{ATOM_NS}id")
    id_text = (id_el.text or "") if id_el is not None else ""
    if aid not in id_text:
        return False, f"entry id {id_text!r} does not contain {aid!r}"
    title_el = entries[0].find(f"{ATOM_NS}title")
    if title_el is None or not (title_el.text or "").strip():
        return False, "entry has no title"
    return True, "ok"


def main(argv):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = argv[1:]
    if not args:
        print("usage: sf_atom_provenance_fetch.py <arxiv-id>... | --sentinel-data")
        return 2
    if args == ["--sentinel-data"]:
        with open(SENTINEL_DATA, encoding="utf-8") as f:
            args = sorted(json.load(f)["papers"].keys())

    os.makedirs(OUT_DIR, exist_ok=True)
    failures = []
    for i, aid in enumerate(args):
        if i:
            time.sleep(SPACING_S)
        url, status, body, attempts, err = fetch_one(aid)
        utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        ok, why = (False, err) if err else atom_entry_ok(body, aid)
        row = {
            "arxiv_id": aid,
            "url": url,
            "time_utc": utc,
            "http_status": status,
            "attempts": attempts,
            "bytes": len(body),
            "sha256": hashlib.sha256(body).hexdigest() if body else None,
            "entry_check": why,
            "access_class": "ID_DEREFERENCE/PROVENANCE_FETCH",
            "persisted": None,
        }
        if ok:
            path = os.path.join(OUT_DIR, f"{aid}.xml")
            with open(path, "wb") as f:
                f.write(body)
            row["persisted"] = os.path.relpath(path, REPO).replace("\\", "/")
        else:
            failures.append((aid, why))
        with open(LEDGER, "ab") as f:
            f.write((json.dumps(row, ensure_ascii=False) + "\n").encode("utf-8"))
        print(f"  [{'OK  ' if ok else 'FAIL'}] {aid} status={status} bytes={len(body)} ({why})")

    print(f"fetched {len(args) - len(failures)}/{len(args)}; ledger appended -> {os.path.relpath(LEDGER, REPO)}")
    if failures:
        for aid, why in failures:
            print(f"  FAILED: {aid}: {why}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
