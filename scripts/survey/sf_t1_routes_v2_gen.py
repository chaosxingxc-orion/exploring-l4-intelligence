#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deterministic routes v2 generator (correction #4A / P0-R4 supersession).

Reads the frozen v1 routes JSONL (never rewritten) and emits
wiki/survey/2026-07-16-sf-t1-routes-v2.jsonl with:
  - SF-T1R-ACL-2026: status NOT_YET_PUBLISHED -> READY (wrong-at-freeze fact corrected:
    conference ended 2026-07-07; ACL Anthology 2026 volumes published);
  - SF-T1R-ICML-2025: entry ENTRY_TO_RESOLVE -> EXACT_URL https://proceedings.mlr.press/v267/
    (official volume resolved; V4 state machine: pattern/rule nulled, v1 keeps the history);
  - every row: appended `status_audit_c4a` block (date / adjudicated status / evidence tier /
    evidence ref) — the adjudication table's machine form; execution_fields stay all-null
    (V11 pre-scan zero-state untouched);
  - record_sha256 recomputed per the frozen hash rule (sorted-keys compact JSON, all fields
    except record_sha256).

Adjudication evidence lives in: docs/checks/2026-07-16-sf-t1-routes-status-audit.json
(tier A rows), wiki/survey/2026-07-16-sf-access-log-c4a-review-verification.jsonl
(tier B/C, seq refs below), amendment-5 §5 (the human-readable table).

Run from repo root:  python scripts/survey/sf_t1_routes_v2_gen.py
"""
import hashlib
import json
import os
import sys
from collections import OrderedDict

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
V1 = os.path.join(REPO, "wiki", "survey", "2026-07-16-sf-t1-routes.jsonl")
V2 = os.path.join(REPO, "wiki", "survey", "2026-07-16-sf-t1-routes-v2.jsonl")
AUDIT = "docs/checks/2026-07-16-sf-t1-routes-status-audit.json"
ACCLOG = "wiki/survey/2026-07-16-sf-access-log-c4a-review-verification.jsonl"

# evidence tier per venue family (see amendment-5 §5 for the full table):
#   A = direct fetch HTTP evidence in the audit artifact
#   B = proxy-fetch signal (e.g. ACL-2026 event page exceeded the 10 MB proxy content cap —
#       impossible for a 404; consistent with six published volumes)
#   C = web-search corroboration of official pages (access log seq refs)
#   D = direct path blocked with explicit failure code; status rests on family C evidence
FAMILY_EVIDENCE = {
    "ACL":     ("A+C", f"直连 200 ×5(含 acl-2026 title=64th Annual Meeting)见 {AUDIT}; 佐证 {ACCLOG} seq11/seq12(会期已过+2026.acl-long 出版)"),
    "EMNLP":   ("A+C", f"直连 200 ×4(2022-25) + emnlp-2026 HTTP 404 当日实证 NOT_YET,见 {AUDIT}; 会期佐证 {ACCLOG} seq21(2026-10-24~29 布达佩斯)"),
    "NEURIPS": ("A+C", f"直连 200 ×4(2022-25) + paper/2026 HTTP 404 当日实证 NOT_YET,见 {AUDIT}; 会期佐证 {ACCLOG} seq20(2026-12-06~12 悉尼)"),
    "ICML":    ("A",   f"直连 200 ×5(卷页+索引)见 {AUDIT}; 索引无 2026 卷 → NOT_YET 实证; v267=ICML2025 佐证 {ACCLOG} seq9"),
    "ICLR":    ("A",   f"openreview group 直连 200 ×5(含 ICLR 2026)见 {AUDIT}"),
    "CVPR":    ("D+C", f"CVF 域 TLS 握手超时(区域性),失败码逐行留痕见 {AUDIT}; 状态依托 {ACCLOG} seq24(CVPR2026 proceedings 2026-05-23 出版,4090 篇)"),
    "ICCV":    ("D+C", f"held 年直连被 reset(失败码留痕见 {AUDIT}); {ACCLOG} seq25(双年制奇数年,2026 无会) → NOT_HELD ×3 为真"),
    "MM":      ("D+C", f"dl.acm.org HTTP 403(bot 拦截,失败码留痕见 {AUDIT}); {ACCLOG} seq23(MM2026=2026-11-10~14 里约) → NOT_YET 为真; 入口仍 ENTRY_TO_RESOLVE 属预注册合同"),
    "ICASSP":  ("A",   f"ieeexplore conhome hub 直连 200 见 {AUDIT} (per-year punumber 仍 ENTRY_TO_RESOLVE,合同不变)"),
    "IS":      ("A+C", f"直连 200 ×4(2022-25) + interspeech_2026 HTTP 404 当日实证 NOT_YET,见 {AUDIT}; 会期佐证 {ACCLOG} seq22(2026-09-28~10-01 悉尼)"),
}


def rehash(rec):
    body = {k: v for k, v in rec.items() if k != "record_sha256"}
    compact = json.dumps(body, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(compact.encode("utf-8")).hexdigest()


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    rows = [json.loads(l, object_pairs_hook=OrderedDict)
            for l in open(V1, encoding="utf-8") if l.strip()]
    changed = []
    for r in rows:
        rid = r["route_id"]
        if rid == "SF-T1R-ACL-2026":
            r["status"] = "READY"
            r["status_basis"] = ("会期 2026-07-02~07 已过;ACL Anthology 2026 卷已出版"
                                 "（2026.acl-long 等六卷)——C4A P0-R4 当日核验更正 v1 的"
                                 "冻结期静态误判(wrong-at-freeze,在案)")
            r["status_determined"] = {"date": "2026-07-16", "by": "coordinator",
                                      "method": "LIVE_STATUS_AUDIT(C4A P0-R4)——差异走本 v2 "
                                                "dated supersession,v1 原件不改写"}
            changed.append(rid + ": status NOT_YET_PUBLISHED->READY")
        if rid == "SF-T1R-ICML-2025":
            r["entry_status"] = "EXACT_URL"
            r["entry_url"] = "https://proceedings.mlr.press/v267/"
            r["entry_pattern"] = None
            r["entry_resolve_rule"] = None
            r["status_basis"] = ("会期已过;PMLR Volume 267 (42nd ICML, 2025-10-06 出版) 已于 "
                                 "C4A P0-R4 直连解析为确定入口——原 ENTRY_TO_RESOLVE 规则见 v1")
            r["status_determined"] = {"date": "2026-07-16", "by": "coordinator",
                                      "method": "LIVE_STATUS_AUDIT(C4A P0-R4)"}
            changed.append(rid + ": entry ENTRY_TO_RESOLVE->EXACT_URL v267")
        venue = r["venue_code"]
        tier, ref = FAMILY_EVIDENCE[venue]
        r["status_audit_c4a"] = {"date": "2026-07-16",
                                 "adjudicated_status": r["status"],
                                 "evidence_tier": tier, "evidence_ref": ref}
        r["record_sha256"] = rehash(r)

    with open(V2, "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"wrote {len(rows)} rows -> {V2}")
    for c in changed:
        print(" ", c)
    dist = {}
    for r in rows:
        dist[r["status"]] = dist.get(r["status"], 0) + 1
    print("status distribution:", json.dumps(dist, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
