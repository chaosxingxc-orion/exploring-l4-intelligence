#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Offline sentinel-recall test for the frozen query family (correction #4 / C4-6b).

For each verified sentinel paper (title/abstract/categories captured via the logged
ID_DEREFERENCE pass), evaluates every frozen query in
wiki/survey/2026-07-15-sf-queries.jsonl offline:
  category filter  = paper categories ∩ query categories ≠ ∅
  date filter      = v1 submission month within [date_from, date_to] (month granularity;
                     boundary cases carry an exact-date note in the sentinel data file)
  term expression  = recursive-descent evaluation of the ti:/abs: boolean expression
                     against normalized title/abstract text

Matching is an offline APPROXIMATION of the arXiv API (no stemming; hyphen/slash/underscore
folded to spaces on both sides; word-boundary phrase matching). It is conservative in the
HIT direction: an offline HIT implies the API almost certainly returns the paper; an offline
term-MISS could still hit via API stemming. Verdicts feed C4-6 (HIT or EXPLAINED_MISS —
never an unexplained miss). No network. Exit 0 iff every sentinel is HIT or carries an
explanation. Persists docs/checks/2026-07-16-sf-sentinel-recall.json.

Run from repo root:
  python scripts/survey/sf_sentinel_recall_test.py wiki/survey/2026-07-16-sf-sentinel-data.json
"""
import json
import os
import re
import sys
import unicodedata

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
QUERIES = os.path.join(REPO, "wiki", "survey", "2026-07-15-sf-queries.jsonl")
OUT = os.path.join(REPO, "docs", "checks", "2026-07-16-sf-sentinel-recall.json")
SHAPE = re.compile(r"^\(.*?\) AND submittedDate:\[\d{12} TO \d{12}\] AND (.*)$", re.S)
TOKEN = re.compile(r'\(|\)|ANDNOT\b|AND\b|OR\b|(ti|abs|all):"([^"]+)"|(ti|abs|all):([\w.\-]+)')


def normalize(s):
    s = unicodedata.normalize("NFKC", s.lower())
    s = re.sub(r"[-_/]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def word_pattern(w):
    """Light plural tolerance approximating arXiv API stemming: a query word matches its
    singular/plural surface forms (model<->models); no deeper stemming."""
    forms = {re.escape(w)}
    if w.endswith("s") and not w.endswith("ss") and len(w) > 3:
        forms.add(re.escape(w[:-1]))
    return "(?:" + "|".join(sorted(forms)) + r")(?:e?s)?"


def phrase_match(phrase, text):
    words = [word_pattern(w) for w in normalize(phrase).split()]
    return re.search(r"\b" + r"\s+".join(words) + r"\b", text) is not None


def tokenize(expr):
    out, i = [], 0
    while i < len(expr):
        if expr[i].isspace():
            i += 1
            continue
        m = TOKEN.match(expr, i)
        if not m:
            raise ValueError(f"unparseable at: {expr[i:i+40]!r}")
        if m.group(0) in ("(", ")", "AND", "OR", "ANDNOT"):
            out.append((m.group(0), None, None))
        else:
            field = m.group(1) or m.group(3)
            val = m.group(2) or m.group(4)
            out.append(("ATOM", field, val))
        i = m.end()
    return out


class Parser:
    def __init__(self, tokens, fields):
        self.t, self.i, self.fields = tokens, 0, fields

    def peek(self):
        return self.t[self.i][0] if self.i < len(self.t) else None

    def parse_or(self):
        v = self.parse_and()
        while self.peek() == "OR":
            self.i += 1
            v = self.parse_and() or v
        return v

    def parse_and(self):
        v = self.parse_unit()
        while self.peek() in ("AND", "ANDNOT"):
            neg = self.peek() == "ANDNOT"
            self.i += 1
            u = self.parse_unit()
            v = v and (not u if neg else u)
        return v

    def parse_unit(self):
        kind, field, val = self.t[self.i]
        if kind == "(":
            self.i += 1
            v = self.parse_or()
            assert self.peek() == ")", "unbalanced parens"
            self.i += 1
            return v
        assert kind == "ATOM", f"unexpected {kind}"
        self.i += 1
        return phrase_match(val, self.fields[field])


def month_of_id(arxiv_id):
    yymm = arxiv_id.split(".")[0]
    return f"20{yymm[:2]}{yymm[2:]}"


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sentinel_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        REPO, "wiki", "survey", "2026-07-16-sf-sentinel-data.json")
    sentinels = json.load(open(sentinel_file, encoding="utf-8"))
    queries = [json.loads(l) for l in open(QUERIES, encoding="utf-8") if l.strip()]

    unparsed = []
    results = {}
    for aid, meta in sentinels["papers"].items():
        title_n = normalize(meta["title"])
        abs_n = normalize(meta["abstract"] or "")
        fields = {"ti": title_n, "abs": abs_n, "all": title_n + " " + abs_n}
        month = month_of_id(aid)
        hits, cat_blocked, term_missed = [], 0, 0
        for q in queries:
            m = SHAPE.match(q["decoded_search_query"])
            if not m:
                unparsed.append(q["query_id"])
                continue
            in_cat = bool(set(meta["categories"]) & set(q["categories"]))
            in_date = q["date_from"][:6] <= month <= q["date_to"][:6]
            try:
                term_ok = Parser(tokenize(m.group(1)), fields).parse_or()
            except Exception as e:
                unparsed.append(f"{q['query_id']}:{e}")
                continue
            if in_cat and in_date and term_ok:
                hits.append(q["query_id"])
            elif in_date and term_ok and not in_cat:
                cat_blocked += 1
            elif in_cat and in_date:
                term_missed += 1
        results[aid] = {
            "title": meta["title"],
            "categories": meta["categories"],
            "reviewer_role": meta.get("reviewer_role"),
            "query_hits": hits,
            "n_term_match_but_category_blocked": cat_blocked,
            "verdict": "HIT" if hits else "MISS",
            "explanation": None if hits else meta.get("miss_explanation"),
        }

    unexplained = [a for a, r in results.items() if r["verdict"] == "MISS" and not r["explanation"]]
    report = {
        "artifact_id": "SF-SENTINEL-RECALL-2026-07-16-01",
        "test": "scripts/survey/sf_sentinel_recall_test.py",
        "inputs": {"queries": "wiki/survey/2026-07-15-sf-queries.jsonl (51 rows, frozen)",
                   "sentinel_data": os.path.relpath(sentinel_file, REPO).replace("\\", "/")},
        "matching_caveat": "offline approximation：无词干化、连字符折叠、词边界短语匹配；"
                           "HIT 方向保守可信，term-MISS 仍可能被 API 词干化召回——终证以执行期实测为准",
        "unparsed_queries": sorted(set(unparsed)),
        "sentinels": results,
        "n_hit": sum(1 for r in results.values() if r["verdict"] == "HIT"),
        "n_explained_miss": sum(1 for r in results.values() if r["verdict"] == "MISS" and r["explanation"]),
        "n_unexplained_miss": len(unexplained),
        "verdict": "PASS" if not unexplained and not unparsed else "FAIL",
        "gate_rule": "每个 sentinel 必须 HIT 或 EXPLAINED_MISS；unexplained miss / 查询不可解析 = FAIL",
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "wb") as f:
        f.write((json.dumps(report, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    print(f"HIT={report['n_hit']} EXPLAINED_MISS={report['n_explained_miss']} "
          f"UNEXPLAINED={report['n_unexplained_miss']} verdict={report['verdict']}")
    for a, r in results.items():
        print(f"  {a} {r['verdict']:4s} hits={len(r['query_hits'])} cat_blocked={r['n_term_match_but_category_blocked']} {r['title'][:50]}")
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
