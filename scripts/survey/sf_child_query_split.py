#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deterministic child-query splitter for arXiv API pagination overflow (correction #4 / C4-5).

Normative implementation of protocol amendment-4 §G6: when a query window's totalResults
exceeds SLICE_LIMIT (2000, arXiv API slice max), split the window YEAR->MONTH->DAY
deterministically. A single DAY still over the limit is a hard STOP (API_LIMIT_SINGLE_DAY
registered, never silently truncated).

Frozen semantics:
  - Windows are CLOSED intervals [date_from, date_to] at minute granularity, GMT
    (arXiv API `submittedDate:[YYYYMMDDHHMM TO YYYYMMDDHHMM]`, both endpoints inclusive).
  - Split ladder ROOT->YEAR->MONTH->DAY: the first overflow of a root window always
    splits into calendar-YEAR windows (clipped to the root window), an overflowing year
    into MONTH windows, an overflowing month into DAY windows.
  - Child windows are chronological, numbered 1..n within one split;
    `query_id = <parent_id>-W<n>` applies recursively (a day window under a month window
    is `<parent>-W<k>-W<j>`).
  - Child records carry: date_from/date_to, boundary semantics, timezone, decoded and
    URL-encoded query strings, query_sha256 (decoded string), record_sha256,
    parent_query_sha256, split_level, split_ordinal, trigger_totalresults.
  - Real frozen compiler rows (2026-07-15-sf-queries.jsonl) carry `record_sha256` (hash of
    the whole compiler record) and NO `query_sha256`; executors MUST adapt them through
    `parent_from_frozen_row`, which computes query_sha256 = sha256(decoded string) and
    keeps the two hash kinds strictly apart.
  - Throttle >=3s between calls, exponential backoff on failure, resume from the last
    fully-logged window (execution discipline; logged in REC-1; `remaining_after` is the
    normative resume slice, `assert_unique_ids` the pre-write duplicate gate).

Pure function of (parent record, totalresults oracle) — no network, no clock, no randomness.
"""
import calendar
import hashlib
import json
import re
from urllib.parse import quote

SLICE_LIMIT = 2000
DATE_RE = re.compile(r"submittedDate:\[(\d{12}) TO (\d{12})\]")
BOUNDARY_SEMANTICS = ("closed interval [date_from, date_to], minute granularity, GMT; "
                      "arXiv API submittedDate, both endpoints inclusive")


def sha256_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _rewrite_window(decoded, date_from, date_to):
    new, n = DATE_RE.subn(f"submittedDate:[{date_from} TO {date_to}]", decoded)
    if n != 1:
        raise ValueError(f"expected exactly one submittedDate range, found {n}")
    return new


def _year_windows(date_from, date_to):
    """Chronological calendar-year windows clipped to the closed parent window."""
    y, ye = int(date_from[:4]), int(date_to[:4])
    out = []
    for yy in range(y, ye + 1):
        start = f"{yy:04d}01010000"
        end = f"{yy:04d}12312359"
        out.append((max(start, date_from), min(end, date_to)))
    return out


def _month_windows(date_from, date_to):
    """Chronological calendar-month windows clipped to the closed parent window."""
    y, m = int(date_from[:4]), int(date_from[4:6])
    ye, me = int(date_to[:4]), int(date_to[4:6])
    out = []
    while (y, m) <= (ye, me):
        last = calendar.monthrange(y, m)[1]
        start = f"{y:04d}{m:02d}010000"
        end = f"{y:04d}{m:02d}{last:02d}2359"
        out.append((max(start, date_from), min(end, date_to)))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


def _day_windows(date_from, date_to):
    y, m = int(date_from[:4]), int(date_from[4:6])
    d, de = int(date_from[6:8]), int(date_to[6:8])
    out = []
    for day in range(d, de + 1):
        start = f"{y:04d}{m:02d}{day:02d}0000"
        end = f"{y:04d}{m:02d}{day:02d}2359"
        out.append((max(start, date_from), min(end, date_to)))
    return out


def _child_record(parent, ordinal, date_from, date_to, level, trigger_total):
    decoded = _rewrite_window(parent["decoded_search_query"], date_from, date_to)
    rec = {
        "query_id": f"{parent['query_id']}-W{ordinal}",
        "parent_query_id": parent["query_id"],
        "parent_query_sha256": parent["query_sha256"],
        "split_level": level,
        "split_ordinal": ordinal,
        "trigger_totalresults": trigger_total,
        "date_from": date_from,
        "date_to": date_to,
        "timezone": "GMT",
        "boundary_semantics": BOUNDARY_SEMANTICS,
        "decoded_search_query": decoded,
        "url_encoded_search_query": quote(decoded, safe=""),
        "query_sha256": sha256_text(decoded),
    }
    body = json.dumps(rec, ensure_ascii=False, sort_keys=True)
    rec["record_sha256"] = sha256_text(body)
    return rec


def parent_from_frozen_row(row):
    """Adapt a frozen compiler row into the splitter's parent contract.

    Frozen rows (2026-07-15-sf-queries.jsonl) carry `record_sha256` — the hash of the whole
    compiler record — and no `query_sha256`. The splitter's parent hash is the hash of the
    DECODED QUERY STRING only; it is computed here. The two hash kinds are never mixed: a
    row-declared query_sha256 (compiler vNext) is verified against sha256(decoded) and a
    mismatch is a hard error; record_sha256 is retained only as provenance under the
    distinct key `frozen_record_sha256` and never used as a query hash.
    """
    decoded = row.get("decoded_search_query")
    if not decoded:
        raise ValueError("frozen row has no decoded_search_query")
    if not DATE_RE.search(decoded):
        raise ValueError("frozen row query has no submittedDate range")
    if "query_id" not in row:
        raise ValueError("frozen row has no query_id")
    qhash = sha256_text(decoded)
    declared = row.get("query_sha256")
    if declared is not None and declared != qhash:
        raise ValueError("declared query_sha256 does not match sha256(decoded_search_query)")
    parent = {"query_id": row["query_id"], "decoded_search_query": decoded, "query_sha256": qhash}
    if "record_sha256" in row:
        parent["frozen_record_sha256"] = row["record_sha256"]
    return parent


def assert_unique_ids(records):
    """Pre-write gate: raise if any query_id repeats across the terminal records."""
    seen = set()
    for r in records:
        qid = r["query_id"]
        if qid in seen:
            raise ValueError(f"duplicate child query_id: {qid}")
        seen.add(qid)
    return len(seen)


def remaining_after(terminals, last_completed_query_id):
    """Normative resume slice: terminals strictly after the last fully-logged window.

    Terminals are already in chronological order; an unknown id is a hard error (a resume
    point must exist in the frozen expansion, never be guessed).
    """
    ids = [t["query_id"] for t in terminals]
    if last_completed_query_id not in ids:
        raise ValueError(f"resume point not in terminal expansion: {last_completed_query_id}")
    return terminals[ids.index(last_completed_query_id) + 1:]


def split_query(parent, totalresults_of):
    """Expand `parent` into terminal child windows using the totalresults oracle.

    parent: dict with query_id, decoded_search_query (one submittedDate range), query_sha256
            (= sha256 of the decoded string; adapt frozen rows via parent_from_frozen_row).
    totalresults_of: callable (decoded_query_string) -> int, the API count oracle
                     (live executor queries arXiv with max_results=0; replay tests inject
                     a synthetic deterministic oracle).
    Returns (terminal_records, events). Terminal records are executable child windows in
    chronological order; events log every split decision and any API_LIMIT_SINGLE_DAY stop.
    """
    events = []

    def expand(rec, level):
        total = totalresults_of(rec["decoded_search_query"])
        if total <= SLICE_LIMIT:
            events.append({"query_id": rec["query_id"], "totalresults": total, "action": "EXECUTE"})
            return [dict(rec, observed_totalresults=total)]
        if level == "DAY":
            events.append({"query_id": rec["query_id"], "totalresults": total,
                           "action": "STOP_API_LIMIT_SINGLE_DAY",
                           "note": "single GMT day exceeds arXiv slice limit; registered, not truncated"})
            return [dict(rec, observed_totalresults=total, api_limit="API_LIMIT_SINGLE_DAY_OVER_2000")]
        next_level = {"ROOT": "YEAR", "YEAR": "MONTH", "MONTH": "DAY"}[level]
        maker = {"YEAR": _year_windows, "MONTH": _month_windows, "DAY": _day_windows}[next_level]
        windows = maker(rec["date_from"], rec["date_to"])
        events.append({"query_id": rec["query_id"], "totalresults": total,
                       "action": f"SPLIT_{next_level}", "children": len(windows)})
        out = []
        for i, (f_, t_) in enumerate(windows, 1):
            child = _child_record(rec, i, f_, t_, next_level, total)
            out.extend(expand(child, next_level))
        return out

    m = DATE_RE.search(parent["decoded_search_query"])
    if not m:
        raise ValueError("parent query has no submittedDate range")
    root = {
        "query_id": parent["query_id"],
        "parent_query_id": None,
        "parent_query_sha256": None,
        "date_from": m.group(1),
        "date_to": m.group(2),
        "decoded_search_query": parent["decoded_search_query"],
        "query_sha256": parent["query_sha256"],
    }
    return expand(root, "ROOT"), events
