#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Real-row integration dry-run for the child-query splitter (correction #4A / P0-R2).

Doctoral-review acceptance being closed here:
  - every REAL frozen query row (2026-07-15-sf-queries.jsonl) must enter the normative
    split function without KeyError, via the `parent_from_frozen_row` adapter;
  - `record_sha256` (whole-record hash) and query_sha256 (decoded-string hash) must never
    be conflated;
  - on a real multi-year root overflow the FIRST split event must be `SPLIT_YEAR`;
  - negative tests: missing submittedDate, missing/wrong hash, year/month/single-day
    overflow, closed-interval boundaries, duplicate child ID, resume-point continuation;
  - two runs must be byte-identical.

No network. Persists docs/checks/2026-07-16-sf-child-query-realrow-dryrun.json.
Run from repo root:  python scripts/survey/sf_child_query_realrow_dryrun.py   (exit 0 iff PASS)
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sf_child_query_split import (DATE_RE, assert_unique_ids, parent_from_frozen_row,  # noqa: E402
                                  remaining_after, sha256_text, split_query)

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
QUERIES = os.path.join(REPO, "wiki", "survey", "2026-07-15-sf-queries.jsonl")
OUT = os.path.join(REPO, "docs", "checks", "2026-07-16-sf-child-query-realrow-dryrun.json")


def load_rows():
    with open(QUERIES, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def overflow_oracle_for(root_from, root_to):
    """Deterministic synthetic oracle over a REAL root window (no network):
    root -> 5000; year 2024 -> 3000, other years -> 500; month 2024-03 -> 2500,
    other months -> 100; day 2024-03-15 -> 2600 (single-day STOP), other days -> 50."""
    def oracle(decoded):
        f_, t_ = DATE_RE.search(decoded).groups()
        if (f_, t_) == (root_from, root_to):
            return 5000
        if f_[:4] == t_[:4] and f_[4:6] != t_[4:6]:      # calendar-year window
            return 3000 if f_[:4] == "2024" else 500
        if f_[:6] == t_[:6] and f_[6:8] != t_[6:8]:      # calendar-month window
            return 2500 if f_[:6] == "202403" else 100
        if f_[:8] == t_[:8]:                              # single-day window
            return 2600 if f_[:8] == "20240315" else 50
        return 50
    return oracle


def expect_raises(fn, *args):
    try:
        fn(*args)
        return False
    except ValueError:
        return True


def run_once(rows):
    checks = []

    def check(cid, desc, ok, detail=""):
        checks.append({"id": cid, "check": desc, "result": "PASS" if ok else "FAIL",
                       "detail": detail})

    # --- A. every real frozen row enters the normative function (EXECUTE path) ---
    n_ok, first_err = 0, ""
    for row in rows:
        try:
            parent = parent_from_frozen_row(row)
            terminals, events = split_query(parent, lambda _d: 100)
            assert len(terminals) == 1
            assert terminals[0]["query_id"] == row["query_id"]
            assert terminals[0]["observed_totalresults"] == 100
            assert parent["query_sha256"] == sha256_text(row["decoded_search_query"])
            n_ok += 1
        except Exception as exc:  # noqa: BLE001 — any real-row failure is the finding
            if not first_err:
                first_err = f"{row.get('query_id')}: {type(exc).__name__}: {exc}"
    check("A1", "全部真实冻结行经 adapter 进入同一 normative split 函数，无 KeyError（EXECUTE 路径）",
          n_ok == len(rows), f"{n_ok}/{len(rows)} rows; first_err={first_err or 'none'}")
    check("A2", "输入行数从 JSONL 实时读取（不硬编码）", len(rows) > 0, f"n_rows={len(rows)}")

    # --- B. hash-kind separation on a real row ---
    row0 = rows[0]
    p0 = parent_from_frozen_row(row0)
    check("B1", "query_sha256 = sha256(decoded)，与 record_sha256（整记录哈希）值不同、字段名不同",
          p0["query_sha256"] == sha256_text(row0["decoded_search_query"])
          and p0["query_sha256"] != row0["record_sha256"]
          and p0["frozen_record_sha256"] == row0["record_sha256"])

    # --- C. real multi-year root overflow: YEAR -> MONTH -> DAY ladder ---
    m = DATE_RE.search(row0["decoded_search_query"])
    root_from, root_to = m.group(1), m.group(2)
    terminals, events = split_query(p0, overflow_oracle_for(root_from, root_to))
    check("C1", "真实跨多年 root 的第一个 overflow event = SPLIT_YEAR（P0-R2 验收原文）",
          bool(events) and events[0]["action"] == "SPLIT_YEAR",
          json.dumps(events[0] if events else None, ensure_ascii=False))
    n_years = events[0]["children"] if events else 0
    check("C2", "年窗口数 = root 跨越的日历年数（2022–2026 → 5）", n_years == 5, f"children={n_years}")
    year_events = [e for e in events if e["action"] == "SPLIT_MONTH"]
    day_events = [e for e in events if e["action"] == "SPLIT_DAY"]
    stops = [e for e in events if e["action"].startswith("STOP")]
    check("C3", "超限年（2024）拆月、超限月（2024-03）拆日、超限单日（03-15）硬停止登记",
          len(year_events) == 1 and year_events[0]["children"] == 12
          and len(day_events) == 1 and day_events[0]["children"] == 31
          and len(stops) == 1 and "SINGLE_DAY" in stops[0]["action"],
          f"month_children={[e['children'] for e in year_events]}, "
          f"day_children={[e['children'] for e in day_events]}, stops={len(stops)}")
    check("C4", "终端窗口结构：4 个整年 + 11 个 2024 月 + 31 个 2024-03 日 = 46",
          len(terminals) == 46, f"got={len(terminals)}")
    firsts = [t for t in terminals if t["split_level"] == "YEAR"]
    check("C5", "闭区间边界：首个年窗口起点 = root 起点、末个年窗口终点 = root 终点（clip 保界）",
          bool(firsts) and firsts[0]["date_from"] == root_from
          and terminals[-1]["date_to"] == root_to,
          f"first_from={firsts[0]['date_from'] if firsts else None}, last_to={terminals[-1]['date_to']}")
    check("C6", "终端 ID 全局唯一（assert_unique_ids 前置闸）",
          assert_unique_ids(terminals) == len(terminals))
    chrono = [t["date_from"] for t in terminals]
    check("C7", "终端窗口时间序单调不减", chrono == sorted(chrono))

    # --- D. resume-point continuation ---
    anchor = terminals[10]["query_id"]
    rest = remaining_after(terminals, anchor)
    check("D1", "断点续跑：remaining_after 返回恢复点之后的精确后缀",
          len(rest) == len(terminals) - 11 and rest[0]["query_id"] == terminals[11]["query_id"],
          f"anchor={anchor}, remaining={len(rest)}")
    check("D2", "断点续跑：未知恢复点 = 硬错误（不得猜测）",
          expect_raises(remaining_after, terminals, "SF-NOT-A-WINDOW"))

    # --- E. negative fixtures (each must raise) ---
    check("E1", "负例：decoded 缺 submittedDate → ValueError",
          expect_raises(parent_from_frozen_row,
                        {"query_id": "SF-NEG-1", "decoded_search_query": "cat:cs.CL AND abs:agent",
                         "record_sha256": "00"}))
    bad = dict(row0)
    bad["query_sha256"] = "deadbeef" * 8
    check("E2", "负例：声明的 query_sha256 与 sha256(decoded) 不符 → ValueError",
          expect_raises(parent_from_frozen_row, bad))
    check("E3", "负例：缺 decoded_search_query → ValueError",
          expect_raises(parent_from_frozen_row, {"query_id": "SF-NEG-3", "record_sha256": "00"}))
    check("E4", "负例：重复 child ID → ValueError",
          expect_raises(assert_unique_ids, terminals + [terminals[0]]))

    return checks, terminals, events


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    rows = load_rows()
    checks1, terminals, events = run_once(rows)
    checks2, _, _ = run_once(rows)
    dump1 = json.dumps(checks1, ensure_ascii=False, sort_keys=True)
    dump2 = json.dumps(checks2, ensure_ascii=False, sort_keys=True)
    checks = checks1 + [{"id": "F1", "check": "确定性：全套 dry-run 两次运行逐字相同",
                         "result": "PASS" if dump1 == dump2 else "FAIL", "detail": ""}]

    n_pass = sum(1 for c in checks if c["result"] == "PASS")
    report = {
        "artifact_id": "SF-CHILD-QUERY-REALROW-DRYRUN-2026-07-16-01",
        "normative_impl": "scripts/survey/sf_child_query_split.py",
        "test": "scripts/survey/sf_child_query_realrow_dryrun.py",
        "input": {"file": "wiki/survey/2026-07-15-sf-queries.jsonl", "n_rows_read": len(rows)},
        "checks": checks,
        "summary": f"{n_pass}/{len(checks)} PASS",
        "verdict": "PASS" if n_pass == len(checks) else "FAIL",
        "events_digest": {"n_events": len(events),
                          "first_event": events[0] if events else None,
                          "n_terminals": len(terminals)},
        "run_sha256": sha256_text(dump1),
        "note": "全负例真实触发非零语义（ValueError）；oracle 为冻结合成函数，无网、无时钟、无随机。",
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "wb") as f:
        f.write((json.dumps(report, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    print(report["summary"], report["verdict"], "run_sha256:", report["run_sha256"][:16])
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
