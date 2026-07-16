#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Offline synthetic replay test for the child-query splitter (correction #4 / C4-5).

Acceptance (doctoral review C4-5): given the same parent query and the same totalResults
inputs, the splitter must generate byte-identical child query lists and hashes. No network.

Scenario (synthetic, frozen; C4A/P0-R2 ladder ROOT->YEAR->MONTH->DAY):
  parent window 2024-01-01..2024-03-31, totalResults 7000 -> YEAR split (single 2024 window,
  clipped to the parent range) -> 7000 again -> MONTH split (Jan/Feb/Mar);
  Jan = 2500 -> DAY split (31 days); Jan-15 = 2400 -> STOP_API_LIMIT_SINGLE_DAY (registered,
  not truncated); every other day = 80; Feb = 1800, Mar = 900 -> executed as single windows.

Persists results to docs/checks/2026-07-16-sf-child-query-replay-test.json.
Run from repo root:  python scripts/survey/sf_child_query_replay_test.py   (exit 0 iff PASS)
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sf_child_query_split import DATE_RE, sha256_text, split_query  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, "docs", "checks", "2026-07-16-sf-child-query-replay-test.json")

PARENT_DECODED = ('(cat:cs.CL OR cat:cs.AI) AND submittedDate:[202401010000 TO 202403312359] '
                  'AND (abs:"language agent" AND abs:"test-time")')
PARENT = {"query_id": "SF-SYN-Q1", "decoded_search_query": PARENT_DECODED,
          "query_sha256": sha256_text(PARENT_DECODED)}


def synthetic_totalresults(decoded):
    m = DATE_RE.search(decoded)
    f_, t_ = m.group(1), m.group(2)
    if (f_, t_) == ("202401010000", "202403312359"):
        return 7000
    if f_.startswith("202401") and f_[6:8] != t_[6:8]:
        return 2500          # January month window -> needs DAY split
    if f_.startswith("202402"):
        return 1800          # February month window -> executable
    if f_.startswith("202403"):
        return 900           # March month window -> executable
    if f_[:8] == "20240115":
        return 2400          # single-day overflow -> STOP case
    return 80                # every other day window


def run_once():
    terminals, events = split_query(PARENT, synthetic_totalresults)
    return json.dumps({"terminals": terminals, "events": events},
                      ensure_ascii=False, sort_keys=True, indent=1)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    run1, run2 = run_once(), run_once()
    obj = json.loads(run1)
    terminals, events = obj["terminals"], obj["events"]

    checks = []

    def check(cid, desc, ok, detail=""):
        checks.append({"id": cid, "check": desc, "result": "PASS" if ok else "FAIL", "detail": detail})

    check("R1", "确定性：同父查询+同计数两次生成逐字相同", run1 == run2)
    check("R2", "第一 overflow event = SPLIT_YEAR（P0-R2 验收：ROOT 首次超限必拆年层）",
          bool(events) and events[0]["action"] == "SPLIT_YEAR" and events[0]["children"] == 1,
          json.dumps(events[0] if events else None, ensure_ascii=False))
    check("R2b", "年→月→日逐级：终端窗口 = 31 天 + 2 月 + 3 月 = 33",
          len(terminals) == 33, f"got={len(terminals)}")
    jan15 = [t for t in terminals if t["date_from"].startswith("20240115")]
    check("R3", "单日超限 STOP：Jan-15 标 API_LIMIT_SINGLE_DAY_OVER_2000、登记不静默截断",
          len(jan15) == 1 and jan15[0].get("api_limit") == "API_LIMIT_SINGLE_DAY_OVER_2000",
          json.dumps(jan15[0].get("api_limit") if jan15 else None))
    ids_ok = all(t["query_id"].startswith("SF-SYN-Q1-W") for t in terminals)
    day_ids = [t["query_id"] for t in terminals if t["split_level"] == "DAY"]
    check("R4", "ID 递归规则：<父ID>-W<n> 逐级适用（日窗口在年/月两层之下，形如 SF-SYN-Q1-W1-W1-W<j>）",
          ids_ok and all(i.startswith("SF-SYN-Q1-W1-W1-W") for i in day_ids),
          f"sample={day_ids[:2]}")
    fields = ["date_from", "date_to", "timezone", "boundary_semantics", "decoded_search_query",
              "url_encoded_search_query", "query_sha256", "record_sha256",
              "parent_query_sha256", "split_level", "split_ordinal", "trigger_totalresults"]
    missing = [f for t in terminals for f in fields if f not in t]
    check("R5", "评审 §8.2 字段逐窗口齐备（窗口边界/时区/decoded/encoded/子 hash/父 hash/层级/序号/触发计数）",
          not missing, f"missing={sorted(set(missing))}")
    check("R6", "边界语义：GMT + 闭区间分钟粒度声明在每条记录内",
          all(t["timezone"] == "GMT" and "closed interval" in t["boundary_semantics"] for t in terminals))
    hash_ok = all(t["query_sha256"] == sha256_text(t["decoded_search_query"]) for t in terminals)
    check("R7", "子查询 sha256 = decoded 字符串哈希，可独立复算", hash_ok)
    chrono = [t["date_from"] for t in terminals]
    check("R8", "终端窗口时间序单调不减（确定性排序）", chrono == sorted(chrono))
    year_decoded = PARENT_DECODED  # 单年窗口 clip 后与根窗口逐字相同（本场景特例，检验链条而非巧合）
    jan_decoded = year_decoded.replace("[202401010000 TO 202403312359]",
                                       "[202401010000 TO 202401312359]")
    month_links = all(t["parent_query_sha256"] == sha256_text(year_decoded)
                      for t in terminals if t["split_level"] == "MONTH")
    day_links = all(t["parent_query_sha256"] == sha256_text(jan_decoded)
                    for t in terminals if t["split_level"] == "DAY")
    check("R9", "父 hash 链：月窗口回指年窗口、日窗口回指 1 月窗口（逐级可追溯）",
          month_links and day_links)

    n_pass = sum(1 for c in checks if c["result"] == "PASS")
    report = {
        "artifact_id": "SF-CHILD-QUERY-REPLAY-2026-07-16-01",
        "normative_impl": "scripts/survey/sf_child_query_split.py",
        "test": "scripts/survey/sf_child_query_replay_test.py",
        "scenario": {"parent": PARENT, "synthetic_counts": "见本文件 synthetic_totalresults（冻结）"},
        "checks": checks,
        "summary": f"{n_pass}/{len(checks)} PASS",
        "verdict": "PASS" if n_pass == len(checks) else "FAIL",
        "events_digest": {"n_events": len(events),
                          "splits": [e for e in events if e["action"].startswith("SPLIT")],
                          "stops": [e for e in events if e["action"].startswith("STOP")]},
        "run_sha256": sha256_text(run1),
        "note": "无网合成 oracle；执行期以 arXiv API totalResults 为 oracle 调用同一 split_query，"
                "节流≥3s/指数退避/断点续跑由执行器按 amendment-4 纪律实施并入 REC-1。",
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "wb") as f:
        f.write((json.dumps(report, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    print(report["summary"], report["verdict"], "run_sha256:", report["run_sha256"][:16])
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
