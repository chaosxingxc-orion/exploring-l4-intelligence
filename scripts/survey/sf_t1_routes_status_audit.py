#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Live external-status audit for the 50 T1 proceedings routes (correction #4A / P0-R4).

This is an EVIDENCE COLLECTOR, deliberately separate from the static structural validator
(sf_t1_routes_validate.py): the validator proves schema, this audit gathers same-day
external facts (URL / UTC time / HTTP or explicit failure code / body sha256). It never
adjudicates status by itself — adjudication lives in the dated amendment that cites this
output, combining tier-A rows here with tier-B/C evidence (proxy fetches / web-search
corroboration) where the direct network path is regionally blocked.

Network behaviour: GET with UA, 25s timeout, up to 3 attempts on connection-level errors
(regional resets are per-connection random), >=3s throttle between accesses. Reads at most
400 KB per body (hash is over the read prefix; length recorded).

Writes docs/checks/2026-07-16-sf-t1-routes-status-audit.json (evidence rows only).
Run from repo root:  python scripts/survey/sf_t1_routes_status_audit.py
"""
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROUTES = os.path.join(REPO, "wiki", "survey", "2026-07-16-sf-t1-routes.jsonl")
OUT = os.path.join(REPO, "docs", "checks", "2026-07-16-sf-t1-routes-status-audit.json")
UA = "Mozilla/5.0 (Gate-S1 route status audit; contact: repo owner)"
READ_CAP = 400_000

# Family probe URLs for routes whose entry is a pattern (ENTRY_TO_RESOLVE) or whose
# status needs a hub-level check. Keys are route_id prefixes.
EXTRA_PROBES = {
    "SF-T1R-ICML-2025": "https://proceedings.mlr.press/v267/",
    "SF-T1R-ICML-2026": "https://proceedings.mlr.press/",
    "SF-T1R-MM-2022": "https://dl.acm.org/conference/mm",
    "SF-T1R-ICASSP-2022": "https://ieeexplore.ieee.org/xpl/conhome/1000002/all-proceedings",
}


def fetch(url):
    last = None
    for attempt in range(1, 4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            r = urllib.request.urlopen(req, timeout=25)
            body = r.read(READ_CAP)
            title = ""
            m = re.search(rb"<title[^>]*>(.*?)</title>", body, re.S | re.I)
            if m:
                title = m.group(1).decode("utf-8", "replace").strip()[:160]
            return {"attempts": attempt, "http_status": r.status,
                    "body_bytes_read": len(body),
                    "body_sha256_prefix400k": hashlib.sha256(body).hexdigest(),
                    "title_tag": title}
        except urllib.error.HTTPError as e:
            return {"attempts": attempt, "http_status": e.code,
                    "failure_code": f"HTTP_{e.code}"}
        except Exception as e:  # noqa: BLE001 — record explicit failure code
            last = f"{type(e).__name__}: {str(e)[:100]}"
            time.sleep(2 * attempt)
    return {"attempts": 3, "http_status": None, "failure_code": f"CONN_FAIL: {last}"}


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    routes = [json.loads(l) for l in open(ROUTES, encoding="utf-8") if l.strip()]
    rows = []
    for r in routes:
        url = r.get("entry_url") or EXTRA_PROBES.get(r["route_id"])
        row = {"route_id": r["route_id"], "frozen_status": r["status"],
               "frozen_entry_status": r["entry_status"], "url": url,
               "time_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
        if not url:
            row["evidence"] = {"failure_code": "NO_CONCRETE_URL",
                               "note": "NOT_APPLICABLE entry (NOT_HELD) or pattern-only; "
                                       "status evidence = tier-B/C in amendment adjudication"}
        else:
            row["evidence"] = fetch(url)
            time.sleep(3)
        rows.append(row)
        ev = row["evidence"]
        print(f"{r['route_id']:22s} {str(ev.get('http_status')):5s} "
              f"{ev.get('failure_code','')} {ev.get('title_tag','')[:60]}")

    report = {
        "artifact_id": "SF-T1R-STATUS-AUDIT-2026-07-16-01",
        "collector": "scripts/survey/sf_t1_routes_status_audit.py",
        "routes_input": "wiki/survey/2026-07-16-sf-t1-routes.jsonl (frozen v1)",
        "tier": "A(direct fetch) rows only — B(proxy)/C(search) evidence and the status "
                "adjudication table live in the dated amendment citing this artifact",
        "network_caveat": "regional per-connection resets observed (same host may succeed "
                          "and fail across attempts); failure codes are explicit, never "
                          "silently treated as venue-side truth",
        "n_routes": len(rows),
        "rows": rows,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "wb") as f:
        f.write((json.dumps(report, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    ok = sum(1 for x in rows if x["evidence"].get("http_status") == 200)
    print(f"done: {len(rows)} routes probed, {ok} direct HTTP 200")
    return 0


if __name__ == "__main__":
    sys.exit(main())
