#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""arXiv full-text fetcher (correction #4B / amendment-7 — owner full-text doctrine
2026-07-16: 承重阅读对象 = 论文全文,不是 abs 摘要页).

Per arXiv ID fetches BOTH renditions and persists them OUTSIDE git (data drive):
  <data-dir>/<id>/<id>.pdf      — PDF rendition   (export.arxiv.org/pdf/<id>)
  <data-dir>/<id>/<id>.eprint   — e-print source  (export.arxiv.org/e-print/<id>;
                                   tar.gz or gzipped TeX — the bibliography source
                                   for offline citation-closure checks, exit
                                   mechanism E2 backward edges)

Git carries only the append-only ledger (hash-pinned provenance):
  wiki/survey/2026-07-17-sf-fulltext-ledger.jsonl
  rows: id, kind, url, utc, http_status, bytes, sha256, stored_at, attempts,
        access_class = ID_DEREFERENCE/FULLTEXT_FETCH (known-ID, NOT discovery)

Data dir resolution: --data-dir > $SPEECHRL_DATA_DIR/survey-fulltext >
E:/chao_workspace/exploring-l4-intelligence/speechrl-data/survey-fulltext.
Politeness: >=3s spacing, exponential backoff, max 4 attempts.

Usage (repo root):
  python scripts/survey/sf_fulltext_fetch.py <id> [<id> ...]
  python scripts/survey/sf_fulltext_fetch.py --sentinel-data
Exit 0 iff every requested (id, rendition) persisted.
"""
import hashlib
import json
import os
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEDGER = os.path.join(REPO, "wiki", "survey", "2026-07-17-sf-fulltext-ledger.jsonl")
SENTINEL_DATA = os.path.join(REPO, "wiki", "survey", "2026-07-16-sf-sentinel-data.json")
def _normalize_data_root(p):
    """SPEECHRL_DATA_DIR is persisted as a WSL path (/mnt/e/...); under Windows
    Python it arrives either verbatim or MSYS-mangled to <git-root>/mnt/e/...
    (caught 2026-07-17, see fulltext-ledger NOTE row) — translate any
    .../mnt/<drive>/ tail to <DRIVE>:/ instead."""
    m = re.search(r"[/\\]mnt[/\\]([a-z])[/\\](.*)$", p or "")
    return f"{m.group(1).upper()}:/{m.group(2)}" if m else p


DEFAULT_DATA_DIR = _normalize_data_root(os.environ.get(
    "SPEECHRL_DATA_DIR",
    "E:/chao_workspace/exploring-l4-intelligence/speechrl-data"))
RENDITIONS = (("pdf", "https://export.arxiv.org/pdf/{aid}"),
              ("eprint", "https://export.arxiv.org/e-print/{aid}"))
UA = "speech-mllm-training-free-rl survey fulltext fetcher (stdlib urllib)"
SPACING_S = 3.0
MAX_ATTEMPTS = 4


def fetch(url):
    last_err = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as resp:
                return resp.status, resp.read(), attempt, None
        except Exception as e:  # noqa: BLE001 — retried, then reported in ledger
            last_err = f"{type(e).__name__}: {e}"
            time.sleep(SPACING_S * (2 ** (attempt - 1)))
    return None, b"", MAX_ATTEMPTS, last_err


def main(argv):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = [a for a in argv[1:]]
    data_dir = os.path.join(DEFAULT_DATA_DIR, "survey-fulltext")
    if "--data-dir" in args:
        i = args.index("--data-dir")
        data_dir = args[i + 1]
        del args[i:i + 2]
    if args == ["--sentinel-data"]:
        with open(SENTINEL_DATA, encoding="utf-8") as f:
            args = sorted(json.load(f)["papers"].keys())
    if not args:
        print("usage: sf_fulltext_fetch.py [--data-dir DIR] <arxiv-id>... | --sentinel-data")
        return 2

    failures = []
    first = True
    for aid in args:
        for kind, tpl in RENDITIONS:
            dest = os.path.join(data_dir, aid, f"{aid}.{'pdf' if kind == 'pdf' else 'eprint'}")
            if os.path.exists(dest) and os.path.getsize(dest) > 0:
                print(f"  [SKIP] {aid} {kind} already present")
                continue
            if not first:
                time.sleep(SPACING_S)
            first = False
            url = tpl.format(aid=aid)
            status, body, attempts, err = fetch(url)
            utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            ok = err is None and status == 200 and len(body) > 1024
            row = {"arxiv_id": aid, "kind": kind, "url": url, "time_utc": utc,
                   "http_status": status, "attempts": attempts, "bytes": len(body),
                   "sha256": hashlib.sha256(body).hexdigest() if body else None,
                   "error": err,
                   "stored_at": None,
                   "access_class": "ID_DEREFERENCE/FULLTEXT_FETCH"}
            if ok:
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                with open(dest, "wb") as f:
                    f.write(body)
                row["stored_at"] = dest.replace("\\", "/")
            else:
                failures.append((aid, kind, err or f"http {status} / {len(body)} bytes"))
            with open(LEDGER, "ab") as f:
                f.write((json.dumps(row, ensure_ascii=False) + "\n").encode("utf-8"))
            print(f"  [{'OK  ' if ok else 'FAIL'}] {aid} {kind} status={status} bytes={len(body)}")

    print(f"failures: {len(failures)}")
    for aid, kind, why in failures:
        print(f"  FAILED {aid} {kind}: {why}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
