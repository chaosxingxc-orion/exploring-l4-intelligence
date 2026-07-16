#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""routes v3 generator (correction #4B — dated supersession, v2 stays frozen).

Trigger: the new adjudication validator (P0-1.3) caught a real claim–evidence
inconsistency inside the C4A bundle: SF-T1R-ICASSP-2023/2024/2025/2026 carry
`status_audit_c4a.evidence_tier: "A"` (direct probe) while their own collector
rows say NO_CONCRETE_URL / tier-B/C — the one direct probe (ieeexplore conhome
all-proceedings hub, HTTP 200) is recorded on the SF-T1R-ICASSP-2022 row only.

v3 = v2 with exactly these four rows corrected to evidence_tier "C" and the
correction annotated inside evidence_ref (dated, non-destructive); per-row
record_sha256 recomputed under the frozen hash rule (sorted-keys JSON, all
fields except record_sha256). v2 bytes are never rewritten — same discipline
as the v1→v2 supersession.

Run from repo root:  python scripts/survey/sf_t1_routes_v3_gen.py
Writes wiki/survey/2026-07-17-sf-t1-routes-v3.jsonl. Exit 0 iff 50 rows written
and only the four registered rows differ from v2.
"""
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
V2 = os.path.join(REPO, "wiki", "survey", "2026-07-16-sf-t1-routes-v2.jsonl")
V3 = os.path.join(REPO, "wiki", "survey", "2026-07-17-sf-t1-routes-v3.jsonl")

CORRECTIONS = {
    "SF-T1R-ICASSP-2023": "C",
    "SF-T1R-ICASSP-2024": "C",
    "SF-T1R-ICASSP-2025": "C",
    "SF-T1R-ICASSP-2026": "C",
}
NOTE = ("〔C4B 更正 2026-07-17:per-year evidence_tier A→C——本行无独立直连探针,"
        "共享 hub 探针(ieeexplore all-proceedings,HTTP 200)记录于 SF-T1R-ICASSP-2022 "
        "collector 行;per-year 状态依据 = tier-C 裁定,与 collector 行自述一致〕")


def rehash(rec):
    body = {k: v for k, v in rec.items() if k != "record_sha256"}
    compact = json.dumps(body, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(compact.encode("utf-8")).hexdigest()


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    rows = [json.loads(l) for l in open(V2, encoding="utf-8") if l.strip()]
    changed = []
    for r in rows:
        rid = r["route_id"]
        if rid in CORRECTIONS:
            sac = r["status_audit_c4a"]
            old = sac["evidence_tier"]
            sac["evidence_tier"] = CORRECTIONS[rid]
            sac["evidence_ref"] = f"{sac['evidence_ref']} {NOTE}"
            r["record_sha256"] = rehash(r)
            changed.append((rid, old, CORRECTIONS[rid]))
    if len(changed) != len(CORRECTIONS):
        print(f"FAIL: expected {len(CORRECTIONS)} corrections, applied {len(changed)}")
        return 1
    for r in rows:
        if rehash(r) != r["record_sha256"]:
            print(f"FAIL: record_sha256 stale for {r['route_id']}")
            return 1
    with open(V3, "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"wrote {len(rows)} rows -> {os.path.relpath(V3, REPO)}")
    for rid, old, new in changed:
        print(f"  corrected {rid}: evidence_tier {old} -> {new}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
