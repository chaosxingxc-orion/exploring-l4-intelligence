#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Machine package summary + stale-token scan + evidence-derived signature checklist
(correction #4A / P0-R1; owner-approved "mechanized status verbs" discipline).

Three jobs, all machine-derived — no hand-written ✅ anywhere:
  1. Recount every signature-package number from the machine artifacts themselves
     (seeds / queries / routes / sentinels), with uniqueness checks and prefix hashes.
  2. Stale-token scan over the ACTIVE signature files: legacy canon tokens (74-seed,
     REC-1..REC-7, amendments 1–3, "(51 rows", 53-query totals) must not appear outside
     lines explicitly marked as historical. Any hit = FAIL.
  3. Signature checklist: each item's status verb is DERIVED from a persisted evidence
     file and a machine criterion (PASS verdicts, counts). If evidence is missing or
     failing, the item says so — a human can no longer type a ✅ the evidence doesn't back.

Run from repo root:  python scripts/survey/sf_package_summary.py   (exit 0 iff all green)
Persists docs/checks/2026-07-16-sf-package-summary.json.
"""
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W = os.path.join(REPO, "wiki", "survey")
C = os.path.join(REPO, "docs", "checks")
OUT = os.path.join(C, "2026-07-16-sf-package-summary.json")

ACTIVE_FILES = [
    "wiki/survey/2026-07-15-system-first-survey-protocol-v1.md",
    "wiki/survey/README.md",
    "wiki/survey/2026-07-15-sf-blank-templates.md",
    "wiki/survey/2026-07-16-sf-protocol-amendment-4.md",
    "wiki/survey/2026-07-16-sf-protocol-amendment-5.md",
    "scripts/survey/sf_sentinel_recall_test.py",
    "scripts/survey/sf_query_compiler.py",
]
FORBIDDEN_TOKENS = ["74 列名种子", "74 条列名", "REC-1..REC-7", "amendments 1–3",
                    "amendments 1-3", "(51 rows", "= **53 条预注册查询**"]
HISTORICAL_MARKERS = ["历史口径", "HISTORICAL_SUPERSEDED", "历史件", "历史数字", "废止"]


def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def jload(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    # ---- 1. machine recounts ----
    seeds = jsonl(os.path.join(W, "2026-07-15-sf-seed-manifest.jsonl"))
    queries = jsonl(os.path.join(W, "2026-07-15-sf-queries.jsonl"))
    routes_path = os.path.join(W, "2026-07-16-sf-t1-routes-v2.jsonl")
    if not os.path.exists(routes_path):
        routes_path = os.path.join(W, "2026-07-16-sf-t1-routes.jsonl")
    routes = jsonl(routes_path)
    sentinels = jload(os.path.join(W, "2026-07-16-sf-sentinel-data.json"))["papers"]

    with open(os.path.join(W, "2026-07-15-sf-queries.jsonl"), "rb") as f:
        qlines = f.read().split(b"\n")
    prefix53 = hashlib.sha256(b"\n".join(qlines[:53]) + b"\n").hexdigest()

    counts = {
        "seeds": {"rows": len(seeds), "unique_ids": len({s["id"] for s in seeds})},
        "queries": {"rows": len(queries),
                    "unique_ids": len({q["query_id"] for q in queries}),
                    "prefix53_sha256": prefix53,
                    "categories_union": sorted({c for q in queries for c in q["categories"]})},
        "routes": {"file": os.path.relpath(routes_path, REPO).replace("\\", "/"),
                   "rows": len(routes),
                   "unique_ids": len({r["route_id"] for r in routes}),
                   "status_distribution": {s: sum(1 for r in routes if r["status"] == s)
                                           for s in sorted({r["status"] for r in routes})}},
        "sentinels": {"papers": len(sentinels),
                      "held_out": sum(1 for m in sentinels.values() if m.get("held_out"))},
    }
    counts_ok = (counts["seeds"]["rows"] == counts["seeds"]["unique_ids"]
                 and counts["queries"]["rows"] == counts["queries"]["unique_ids"]
                 and counts["routes"]["rows"] == counts["routes"]["unique_ids"] == 50)

    # ---- 2. stale-token scan ----
    stale_hits = []
    for rel in ACTIVE_FILES:
        path = os.path.join(REPO, rel)
        if not os.path.exists(path):
            continue
        for i, line in enumerate(open(path, encoding="utf-8"), 1):
            if any(m in line for m in HISTORICAL_MARKERS):
                continue
            for tok in FORBIDDEN_TOKENS:
                if tok in line:
                    stale_hits.append({"file": rel, "line": i, "token": tok})

    # ---- 3. evidence-derived signature checklist ----
    def evid(fname, criterion):
        path = os.path.join(C, fname)
        if not os.path.exists(path):
            return "EVIDENCE_MISSING", f"docs/checks/{fname} not found"
        rep = jload(path)
        ok, detail = criterion(rep)
        return ("PASS" if ok else "FAIL"), detail

    checklist = []

    def item(name, evidence, status, detail):
        checklist.append({"item": name, "evidence": evidence,
                          "status": status, "detail": detail})

    s, d = evid("2026-07-16-sf-child-query-replay-test.json",
                lambda r: (r["verdict"] == "PASS", r["summary"]))
    item("child splitter 合成回放（首 overflow=SPLIT_YEAR）",
         "docs/checks/2026-07-16-sf-child-query-replay-test.json", s, d)

    s, d = evid("2026-07-16-sf-child-query-realrow-dryrun.json",
                lambda r: (r["verdict"] == "PASS" and r["input"]["n_rows_read"] == len(queries),
                           f"{r['summary']}; real rows read={r['input']['n_rows_read']}"))
    item("child splitter 真实冻结行集成 dry-run + 负测试",
         "docs/checks/2026-07-16-sf-child-query-realrow-dryrun.json", s, d)

    s, d = evid("2026-07-16-sf-record-validator-test.json",
                lambda r: (r["verdict"] == "PASS", r["summary"]))
    item("REC-0/REC-2/claim-lineage validator（正例0退出+全负例非零退出）",
         "docs/checks/2026-07-16-sf-record-validator-test.json", s, d)

    s, d = evid("2026-07-16-sf-t1-routes-validation.json",
                lambda r: (r["verdict"] == "PASS",
                           f"{r['summary']}; input={r['inputs']['routes_jsonl']['path']}"))
    item("routes 结构 validator（schema 层,与外部状态审计分立）",
         "docs/checks/2026-07-16-sf-t1-routes-validation.json", s, d)

    s, d = evid("2026-07-16-sf-t1-routes-status-audit.json",
                lambda r: (r["n_routes"] == 50,
                           f"{r['n_routes']} routes probed (evidence collector; "
                           f"adjudication = amendment-5)"))
    item("routes 外部状态审计证据件（tier-A 直连行,B/C 层证据见 amendment-5）",
         "docs/checks/2026-07-16-sf-t1-routes-status-audit.json", s, d)

    s, d = evid("2026-07-16-sf-sentinel-recall.json",
                lambda r: (r["verdict"] == "PASS"
                           and r["outcome_counts"]["UNRESOLVED_MISS"] == 0
                           and len(r["held_out_outcomes"]) >= 2,
                           f"outcomes={r['outcome_counts']}; held_out={r['held_out_outcomes']}"))
    item("sentinel 四分法（零 UNRESOLVED、held-out 存在且未被种子污染）",
         "docs/checks/2026-07-16-sf-sentinel-recall.json", s, d)

    item("陈旧口径扫描（active 签署面零命中）", "本文件 stale_token_scan 段",
         "PASS" if not stale_hits else "FAIL", f"hits={len(stale_hits)}")
    item("机器重数一致（seeds/queries/routes 唯一性 + routes=50）",
         "本文件 counts 段", "PASS" if counts_ok else "FAIL",
         json.dumps({k: v for k, v in counts.items() if k != 'queries'}, ensure_ascii=False)[:200])

    all_green = all(c["status"] == "PASS" for c in checklist)
    report = {
        "artifact_id": "SF-PACKAGE-SUMMARY-2026-07-16-01",
        "generator": "scripts/survey/sf_package_summary.py",
        "discipline": "机械化状态动词（owner 2026-07-16 批准）：签署清单状态一律由本脚本从持久化"
                      "证据文件推导,人工不得手填完成态;EVIDENCE_MISSING/FAIL 如实显示",
        "counts": counts,
        "stale_token_scan": {"files_scanned": ACTIVE_FILES,
                             "forbidden_tokens": FORBIDDEN_TOKENS,
                             "historical_line_markers": HISTORICAL_MARKERS,
                             "hits": stale_hits},
        "signature_checklist": checklist,
        "verdict": "PASS" if all_green else "FAIL",
    }
    os.makedirs(C, exist_ok=True)
    with open(OUT, "wb") as f:
        f.write((json.dumps(report, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    print(f"package summary: {report['verdict']}")
    for c in checklist:
        print(f"  [{c['status']:16s}] {c['item']}")
    return 0 if all_green else 1


if __name__ == "__main__":
    sys.exit(main())
