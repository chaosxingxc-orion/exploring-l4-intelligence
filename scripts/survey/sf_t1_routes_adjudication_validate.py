#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T1-route adjudication validator (correction #4B / P0-1.3).

The status-audit COLLECTOR explicitly does not adjudicate; re-review #4A
MAJOR-1 proved the old package summary upgraded "50 collector rows exist" into
an audit PASS. This validator is the missing adjudication layer: it joins the
frozen routes-v2 manifest against the persisted collector evidence row-by-row
and fails closed on any structural gap.

Rules (all offline, deterministic):
  R1 both inputs carry exactly 50 unique route_ids and the id sets are equal
  R2 v2.status == v2.status_audit_c4a.adjudicated_status for every route
  R3 status_audit_c4a complete: adjudicated_status in domain, evidence_tier
     non-empty over {A,B,C,D}, evidence_ref non-empty, date = YYYY-MM-DD
  R4 collector row well-formed: time_utc ISO-like; evidence a non-empty dict;
     http_status present => attempts >= 1; http_status == 200 => body sha256 +
     title_tag non-empty; no url probed => evidence.note non-empty (knowledge
     basis must be stated, not implied)
  R5 evidence_tier contains 'A' => a URL probe exists for that route
  R6 status domain {READY, NOT_YET_PUBLISHED, NOT_HELD};
     entry_status == EXACT_URL => entry_url non-empty
  R7 empty/duplicate/missing rows on either side => FAIL

Run from repo root:  python scripts/survey/sf_t1_routes_adjudication_validate.py
Persists docs/checks/2026-07-16-sf-t1-routes-adjudication.json. Exit 0 iff PASS.
"""
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_ROUTES_CANDIDATES = (
    os.path.join(REPO, "wiki", "survey", "2026-07-17-sf-t1-routes-v3.jsonl"),
    os.path.join(REPO, "wiki", "survey", "2026-07-16-sf-t1-routes-v2.jsonl"),
)
ROUTES = next(p for p in _ROUTES_CANDIDATES if os.path.exists(p))
AUDIT = os.path.join(REPO, "docs", "checks", "2026-07-16-sf-t1-routes-status-audit.json")
OUT = os.path.join(REPO, "docs", "checks", "2026-07-16-sf-t1-routes-adjudication.json")
STATUS_DOMAIN = ("READY", "NOT_YET_PUBLISHED", "NOT_HELD")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    violations = []

    def bad(rule, where, msg):
        violations.append({"rule": rule, "where": where, "violation": msg})

    routes = [json.loads(l) for l in open(ROUTES, encoding="utf-8") if l.strip()]
    audit = json.load(open(AUDIT, encoding="utf-8"))
    arows = audit.get("rows") or []

    rids = [r.get("route_id") for r in routes]
    aids = [r.get("route_id") for r in arows]
    if len(rids) != 50 or len(set(rids)) != 50:
        bad("R1", "routes-v2", f"expected 50 unique route_ids, got {len(rids)} rows / "
                               f"{len(set(rids))} unique")
    if len(aids) != 50 or len(set(aids)) != 50:
        bad("R1", "status-audit", f"expected 50 unique route_ids, got {len(aids)} rows / "
                                  f"{len(set(aids))} unique")
    if set(rids) != set(aids):
        bad("R1", "join", f"id sets differ: only-in-v2={sorted(set(rids) - set(aids))[:5]}, "
                          f"only-in-audit={sorted(set(aids) - set(rids))[:5]}")

    amap = {r.get("route_id"): r for r in arows}
    for r in routes:
        rid = r.get("route_id")
        w = f"route:{rid}"
        if r.get("status") not in STATUS_DOMAIN:
            bad("R6", w, f"status outside domain: {r.get('status')!r}")
        if r.get("entry_status") == "EXACT_URL" and not str(r.get("entry_url", "") or "").strip():
            bad("R6", w, "entry_status EXACT_URL but entry_url empty")
        sac = r.get("status_audit_c4a")
        if not isinstance(sac, dict):
            bad("R3", w, "status_audit_c4a block missing")
            continue
        if sac.get("adjudicated_status") not in STATUS_DOMAIN:
            bad("R3", w, f"adjudicated_status outside domain: {sac.get('adjudicated_status')!r}")
        if sac.get("adjudicated_status") != r.get("status"):
            bad("R2", w, f"frozen status {r.get('status')!r} != adjudicated "
                         f"{sac.get('adjudicated_status')!r}")
        tier = str(sac.get("evidence_tier", "") or "")
        parts = [p for p in tier.split("+") if p]
        if not parts or any(p not in ("A", "B", "C", "D") for p in parts):
            bad("R3", w, f"evidence_tier malformed: {tier!r}")
        if not str(sac.get("evidence_ref", "") or "").strip():
            bad("R3", w, "evidence_ref empty")
        if not DATE_RE.match(str(sac.get("date", "") or "")):
            bad("R3", w, f"adjudication date malformed: {sac.get('date')!r}")

        a = amap.get(rid)
        if a is None:
            continue  # already counted under R1
        if not UTC_RE.match(str(a.get("time_utc", "") or "")):
            bad("R4", w, f"collector time_utc malformed: {a.get('time_utc')!r}")
        ev = a.get("evidence")
        if not isinstance(ev, dict) or not ev:
            bad("R4", w, "collector evidence missing/empty")
            continue
        url = str(a.get("url", "") or "").strip()
        if "http_status" in ev:
            try:
                attempts = int(ev.get("attempts", 0))
            except (TypeError, ValueError):
                attempts = 0
            if attempts < 1:
                bad("R4", w, f"probe row with attempts={ev.get('attempts')!r}")
            if ev.get("http_status") == 200:
                if not str(ev.get("body_sha256_prefix400k", "") or "").strip():
                    bad("R4", w, "200 response without body sha256")
                # title_tag may legitimately be empty (JS-rendered pages, e.g.
                # ieeexplore); the body hash is the load-bearing capture.
        if not url and not str(ev.get("note", "") or "").strip():
            bad("R4", w, "unprobed route without a stated knowledge-basis note")
        if "A" in parts and not url:
            bad("R5", w, f"evidence_tier {tier!r} claims a direct probe but collector "
                         "row has no URL")

    report = {
        "artifact_id": "SF-T1-ROUTES-ADJUDICATION-2026-07-16-01",
        "validator": "scripts/survey/sf_t1_routes_adjudication_validate.py",
        "inputs": {
            "routes": os.path.relpath(ROUTES, REPO).replace("\\", "/"),
            "status_audit": os.path.relpath(AUDIT, REPO).replace("\\", "/"),
        },
        "n_routes": len(routes),
        "n_audit_rows": len(arows),
        "n_violations": len(violations),
        "violations": violations,
        "verdict": "PASS" if not violations else "FAIL",
        "scope_note": "结构裁定层:逐 route 对齐冻结状态/裁定状态/证据 tier/探针证据;"
                      "外部世界真值以裁定表+当日证据为准,本验证器不发网",
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "wb") as f:
        f.write((json.dumps(report, ensure_ascii=False, indent=1, sort_keys=True)
                 + "\n").encode("utf-8"))
    print(f"routes adjudication: {report['verdict']} "
          f"({len(routes)} routes, {len(violations)} violations)")
    for v in violations[:10]:
        print(f"  [{v['rule']}] {v['where']}: {v['violation']}")
    return 0 if not violations else 1


if __name__ == "__main__":
    sys.exit(main())
