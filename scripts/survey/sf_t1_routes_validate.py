#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read-only validator for the T1 proceedings route manifest (correction #4 / C4-3).

Validates:
  wiki/survey/2026-07-16-sf-t1-routes.jsonl      (50 individually serialized routes)
  wiki/survey/2026-07-16-sf-t1-wordlist-v1.json  (filter wordlist, dual-side normalization canon)

Checks V1..V12 (route uniqueness/coverage, status & entry-state machine, ICCV constraint,
wordlist hash pinning, dual-side same-function normalization + effective term count,
per-row record_sha256 integrity, pre-execution null state).

No network. Exit 0 iff all checks PASS. Persists machine-readable results to
  docs/checks/2026-07-16-sf-t1-routes-validation.json
Run from repo root:  python scripts/survey/sf_t1_routes_validate.py
"""
import hashlib
import json
import os
import re
import sys
import unicodedata

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_ROUTES_V3 = os.path.join(REPO, "wiki", "survey", "2026-07-17-sf-t1-routes-v3.jsonl")
_ROUTES_V2 = os.path.join(REPO, "wiki", "survey", "2026-07-16-sf-t1-routes-v2.jsonl")
_ROUTES_V1 = os.path.join(REPO, "wiki", "survey", "2026-07-16-sf-t1-routes.jsonl")
# C4A/P0-R4: the newest dated supersession is the active canon when present;
# earlier versions stay as frozen historical artifacts and are never rewritten
# (C4B: v3 corrects four ICASSP evidence_tier labels, see sf_t1_routes_v3_gen.py).
ROUTES = next(p for p in (_ROUTES_V3, _ROUTES_V2, _ROUTES_V1) if os.path.exists(p))
WORDLIST = os.path.join(REPO, "wiki", "survey", "2026-07-16-sf-t1-wordlist-v1.json")
OUT = os.path.join(REPO, "docs", "checks", "2026-07-16-sf-t1-routes-validation.json")

VENUES = ["ACL", "EMNLP", "NEURIPS", "ICML", "ICLR", "CVPR", "ICCV", "MM", "ICASSP", "IS"]
YEARS = [2022, 2023, 2024, 2025, 2026]
STATUS_ENUM = {"READY", "NOT_YET_PUBLISHED", "NOT_HELD"}
ENTRY_ENUM = {"EXACT_URL", "ENTRY_TO_RESOLVE", "NOT_APPLICABLE"}
COUNT_FIELDS = ["n_titles_total", "n_matched", "n_resolved_arxiv", "n_rescued_oa", "n_paywalled_removed"]
NOT_HELD_EXPECTED = {"SF-T1R-ICCV-2022", "SF-T1R-ICCV-2024", "SF-T1R-ICCV-2026"}


def normalize(s):
    """norm-v1 (canonical, dual-side): lowercase -> NFKC -> [-_/]->space -> collapse ws."""
    s = s.lower()
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"[-_/]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    results = []

    def check(cid, desc, ok, detail=""):
        results.append({"id": cid, "check": desc, "result": "PASS" if ok else "FAIL", "detail": detail})
        return ok

    wl_bytes = open(WORDLIST, "rb").read()
    wl_sha = sha256_bytes(wl_bytes)
    wl = json.loads(wl_bytes.decode("utf-8"))

    routes_bytes = open(ROUTES, "rb").read()
    rows = [json.loads(line) for line in routes_bytes.decode("utf-8").splitlines() if line.strip()]

    ids = [r["route_id"] for r in rows]
    check("V1", "50 条记录且 route_id 全唯一", len(rows) == 50 and len(set(ids)) == 50,
          f"rows={len(rows)} unique={len(set(ids))}")

    vy = {(r["venue_code"], r["year"]) for r in rows}
    expected = {(v, y) for v in VENUES for y in YEARS}
    check("V2", "venue-year 覆盖恰为 10 会 × 2022–2026 且无重复",
          vy == expected and len(rows) == len(vy), f"missing={sorted(expected - vy)} extra={sorted(vy - expected)}")

    bad = [r["route_id"] for r in rows if r["status"] not in STATUS_ENUM or r["entry_status"] not in ENTRY_ENUM]
    check("V3", "status / entry_status 枚举合法", not bad, f"bad={bad}")

    bad = []
    for r in rows:
        es, url, pat, rule = r["entry_status"], r["entry_url"], r["entry_pattern"], r["entry_resolve_rule"]
        if es == "EXACT_URL":
            ok = isinstance(url, str) and url.startswith("https://") and pat is None and rule is None
        elif es == "ENTRY_TO_RESOLVE":
            ok = url is None and isinstance(pat, str) and pat and isinstance(rule, str) and rule
        else:  # NOT_APPLICABLE
            ok = url is None and pat is None and rule is None and r["status"] == "NOT_HELD"
        if not ok:
            bad.append(r["route_id"])
    check("V4", "入口互斥状态机：EXACT_URL=完整 https URL；ENTRY_TO_RESOLVE=模式+确定性解析规则；NOT_APPLICABLE⇔NOT_HELD",
          not bad, f"bad={bad}")

    nh = {r["route_id"] for r in rows if r["status"] == "NOT_HELD"}
    check("V5", "NOT_HELD 恰为 ICCV 偶数年三条，无其他 venue 出现 NOT_HELD", nh == NOT_HELD_EXPECTED,
          f"got={sorted(nh)}")

    bad = [r["route_id"] for r in rows
           if r["wordlist"]["sha256"] != wl_sha or r["wordlist"]["version"] != wl.get("version")]
    check("V6", "全部行钉定的词表 sha256/version 与实际词表文件一致", not bad,
          f"file_sha={wl_sha[:12]} bad={bad}")

    g = wl["groups"]
    raw_ok = (len(g["A"]), len(g["B"]), len(g["C"])) == (
        wl["counts_raw"]["A"], wl["counts_raw"]["B"], wl["counts_raw"]["C"])
    wild = [it for grp in g.values() for it in grp if "*" in it or "?" in it]
    idem = all(normalize(normalize(it)) == normalize(it) for grp in g.values() for it in grp)

    def eff_set(grp):
        return {normalize(it) for it in grp}
    eff = {k: len(eff_set(v)) for k, v in g.items()}
    eff_ok = all(eff[k] == wl["counts_effective_after_normalization"][k] for k in ("A", "B", "C"))
    merges = []
    for name, grp in g.items():
        byn = {}
        for it in grp:
            byn.setdefault(normalize(it), []).append(it)
        merges += [{"group": name, "normalized": n, "raw_items": items}
                   for n, items in byn.items() if len(items) > 1]
    merges_ok = sorted(map(json.dumps, merges)) == sorted(map(json.dumps, wl["normalization_merges"]))
    check("V7", "词表内检：raw 计数一致 / 零通配符 / 归一化幂等 / 有效词项计数与合并对复算一致",
          raw_ok and not wild and idem and eff_ok and merges_ok,
          f"raw={wl['counts_raw']} eff_recomputed={eff} wild={wild} merges_recomputed={len(merges)}")

    both = wl["normalization"].get("applies_to", [])
    check("V8", "双侧同函数归一化为正典（applies_to 含 title 与 wordlist_item）",
          "title" in both and "wordlist_item" in both, f"applies_to={both}")

    bad = [r["route_id"] for r in rows if r["count_fields_spec"] != COUNT_FIELDS]
    check("V9", "五计数字段 spec 逐行齐备且顺序一致", not bad, f"bad={bad}")

    bad = []
    for r in rows:
        body = {k: v for k, v in r.items() if k != "record_sha256"}
        h = sha256_bytes(json.dumps(body, ensure_ascii=False, sort_keys=True).encode("utf-8"))
        if h != r["record_sha256"]:
            bad.append(r["route_id"])
    check("V10", "逐行 record_sha256 完整性复算一致", not bad, f"bad={bad}")

    bad = [r["route_id"] for r in rows
           if any(v is not None for v in r["execution_fields"].values())]
    check("V11", "执行期字段（raw_toc_sha256/rec7_log/resolved_entry_url/status_reverified）全 null = 签署前零扫描态",
          not bad, f"bad={bad}")

    bad = [r["route_id"] for r in rows
           if (r["status"] == "NOT_HELD") != (r["tracks"] == [])]
    check("V12", "tracks：NOT_HELD 行为空、其余非空", not bad, f"bad={bad}")

    n_pass = sum(1 for r in results if r["result"] == "PASS")
    report = {
        "artifact_id": "SF-T1-ROUTES-VALIDATION-2026-07-16-01",
        "validator": "scripts/survey/sf_t1_routes_validate.py",
        "inputs": {
            "routes_jsonl": {"path": os.path.relpath(ROUTES, REPO).replace("\\", "/"),
                             "sha256": sha256_bytes(routes_bytes)},
            "wordlist_json": {"path": "wiki/survey/2026-07-16-sf-t1-wordlist-v1.json", "sha256": wl_sha},
        },
        "status_distribution": {s: sum(1 for r in rows if r["status"] == s) for s in sorted(STATUS_ENUM)},
        "entry_distribution": {s: sum(1 for r in rows if r["entry_status"] == s) for s in sorted(ENTRY_ENUM)},
        "wordlist_counts": {"raw": wl["counts_raw"],
                            "effective_after_normalization": wl["counts_effective_after_normalization"]},
        "checks": results,
        "summary": f"{n_pass}/{len(results)} PASS",
        "verdict": "PASS" if n_pass == len(results) else "FAIL",
        "note": "无网静态验证；执行期状态核验（READY 是否仍真、ENTRY_TO_RESOLVE 解析）归执行首步 + REC-7。",
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "wb") as f:
        f.write((json.dumps(report, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    print(json.dumps(report, ensure_ascii=False, indent=1))
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
