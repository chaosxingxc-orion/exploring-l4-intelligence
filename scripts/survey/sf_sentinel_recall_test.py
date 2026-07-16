#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Offline sentinel-coverage test, four-way falsifiable taxonomy (correction #4A / P0-R5).

Outcome domain per sentinel paper (priority order; free-text can NEVER convert an outcome):
  QUERY_HIT               — a frozen query's category+date+term expression matches offline;
  SEED_GUARANTEED         — not query-recalled, but guaranteed by an exact ID in the frozen
                            seed manifest (never available to held-out sentinels);
  EXACT_ROUTE_GUARANTEED  — guaranteed by a READY venue route with an exact entry URL;
  REGISTERED_BOUNDARY     — an accepted coverage boundary registered in a dated amendment
                            (machine-checked pointer, not an inline explanation);
  UNRESOLVED_MISS         — none of the above; the test FAILS.

`coverage_note` fields in the sentinel data are annotations only — the old EXPLAINED_MISS
mechanism (any free text converts a miss into a pass) is retired as unfalsifiable
(doctoral review P0-R5). Held-out sentinels (held_out=true) additionally must not appear
in the seed manifest — a seeded held-out is a design contamination and FAILS.

C4B hardening (correction #4B):
  - matching text = `source_normalized_abstract` (renamed from `abstract`; the word
    "verbatim" now refers ONLY to the raw Atom bytes pinned per entry);
  - every sentinel must carry `atom_xml` + `atom_sha256`, the file must exist and its
    sha256 must match (tampered/absent provenance = FAIL);
  - REGISTERED_BOUNDARY no longer means "some file exists" (re-review #4A MINOR-2):
    the registered file must contain a machine-readable line
    `BOUNDARY_REG {"paper":"<id>","boundary":"<CODE>","reason":"...",
    "adjudicator":"...","date":"YYYY-MM-DD"}` for THIS paper with all fields
    non-empty, else the channel does not fire;
  - held-out sentinels must be agent-era papers (v1 >= 2025-01, owner doctrine
    2026-07-16) — an older held-out = FAIL.

Offline matcher unchanged from C4-6: category ∩, month-granularity window, recursive-descent
ti:/abs: boolean evaluation, hyphen folding, word-boundary phrases, light plural tolerance;
conservative in the HIT direction. Input counts are read live from the JSONL, never
hardcoded. No network. Persists docs/checks/2026-07-16-sf-sentinel-recall.json.

Run from repo root:
  python scripts/survey/sf_sentinel_recall_test.py wiki/survey/2026-07-16-sf-sentinel-data.json
"""
import hashlib
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


def boundary_registered(reg_path, aid):
    """P0-4.2: the registration file must exist AND carry a complete
    machine-readable BOUNDARY_REG line for THIS paper; mere existence never fires
    the channel."""
    if not os.path.exists(reg_path):
        return False
    for line in open(reg_path, encoding="utf-8", errors="replace"):
        idx = line.find("BOUNDARY_REG ")
        if idx < 0:
            continue
        try:
            reg = json.loads(line[idx + len("BOUNDARY_REG "):].strip())
        except json.JSONDecodeError:
            continue
        if (reg.get("paper") == aid
                and str(reg.get("boundary", "")).strip()
                and str(reg.get("reason", "")).strip()
                and str(reg.get("adjudicator", "")).strip()
                and re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(reg.get("date", "")))):
            return True
    return False


SEEDS = os.path.join(REPO, "wiki", "survey", "2026-07-15-sf-seed-manifest.jsonl")
ROUTES_V3 = os.path.join(REPO, "wiki", "survey", "2026-07-17-sf-t1-routes-v3.jsonl")
ROUTES_V2 = os.path.join(REPO, "wiki", "survey", "2026-07-16-sf-t1-routes-v2.jsonl")
ROUTES_V1 = os.path.join(REPO, "wiki", "survey", "2026-07-16-sf-t1-routes.jsonl")
OUTCOME_ORDER = ("QUERY_HIT", "SEED_GUARANTEED", "EXACT_ROUTE_GUARANTEED",
                 "REGISTERED_BOUNDARY", "UNRESOLVED_MISS")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sentinel_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        REPO, "wiki", "survey", "2026-07-16-sf-sentinel-data.json")
    sentinels = json.load(open(sentinel_file, encoding="utf-8"))
    queries = [json.loads(l) for l in open(QUERIES, encoding="utf-8") if l.strip()]
    seed_ids = {json.loads(l)["id"] for l in open(SEEDS, encoding="utf-8") if l.strip()}
    routes_file = next(p for p in (ROUTES_V3, ROUTES_V2, ROUTES_V1) if os.path.exists(p))
    routes = {r["route_id"]: r for r in
              (json.loads(l) for l in open(routes_file, encoding="utf-8") if l.strip())}

    unparsed = []
    results = {}
    contaminated_holdouts = []
    provenance_failures = []
    stale_holdouts = []
    for aid, meta in sentinels["papers"].items():
        title_n = normalize(meta["title"])
        abs_n = normalize(meta["source_normalized_abstract"] or "")
        fields = {"ti": title_n, "abs": abs_n, "all": title_n + " " + abs_n}

        atom_rel = meta.get("atom_xml")
        atom_path = os.path.join(REPO, atom_rel) if atom_rel else None
        if not atom_rel or not os.path.exists(atom_path):
            provenance_failures.append(f"{aid}: atom_xml missing")
        else:
            digest = hashlib.sha256(open(atom_path, "rb").read()).hexdigest()
            if digest != meta.get("atom_sha256"):
                provenance_failures.append(f"{aid}: atom_sha256 mismatch")
        month = month_of_id(aid)
        hits, cat_blocked = [], 0
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

        held_out = bool(meta.get("held_out"))
        in_seed = aid in seed_ids
        if held_out and in_seed:
            contaminated_holdouts.append(aid)
        if held_out and month < "202501":
            stale_holdouts.append(aid)

        route_ok = False
        vr = meta.get("venue_route")
        if vr and vr in routes:
            r = routes[vr]
            route_ok = (r.get("status") == "READY" and r.get("entry_status") == "EXACT_URL")

        boundary_ok = False
        ab = meta.get("accepted_boundary")
        if isinstance(ab, dict) and ab.get("registered_in"):
            boundary_ok = boundary_registered(os.path.join(REPO, ab["registered_in"]), aid)

        channels = {"QUERY_HIT": bool(hits),
                    "SEED_GUARANTEED": in_seed and not held_out,
                    "EXACT_ROUTE_GUARANTEED": route_ok,
                    "REGISTERED_BOUNDARY": boundary_ok,
                    "UNRESOLVED_MISS": True}
        outcome = next(o for o in OUTCOME_ORDER if channels[o])
        results[aid] = {
            "title": meta["title"],
            "categories": meta["categories"],
            "reviewer_role": meta.get("reviewer_role"),
            "held_out": held_out,
            "query_hits": hits,
            "n_term_match_but_category_blocked": cat_blocked,
            "channels": {k: v for k, v in channels.items() if k != "UNRESOLVED_MISS"},
            "outcome": outcome,
            "coverage_note": meta.get("coverage_note"),
        }

    unresolved = sorted(a for a, r in results.items() if r["outcome"] == "UNRESOLVED_MISS")
    holdouts = {a: r["outcome"] for a, r in results.items() if r["held_out"]}
    counts = {o: sum(1 for r in results.values() if r["outcome"] == o) for o in OUTCOME_ORDER}
    fail_reasons = []
    if unresolved:
        fail_reasons.append(f"UNRESOLVED_MISS: {unresolved}")
    if unparsed:
        fail_reasons.append(f"unparsed queries: {sorted(set(unparsed))[:5]}")
    if not holdouts:
        fail_reasons.append("no held-out sentinels present")
    if contaminated_holdouts:
        fail_reasons.append(f"held-out contaminated by seed manifest: {contaminated_holdouts}")
    if provenance_failures:
        fail_reasons.append(f"raw Atom provenance failures: {provenance_failures}")
    if stale_holdouts:
        fail_reasons.append(f"held-out older than agent era (owner doctrine v1>=2025-01): "
                            f"{stale_holdouts}")

    report = {
        "artifact_id": "SF-SENTINEL-RECALL-2026-07-16-03",
        "test": "scripts/survey/sf_sentinel_recall_test.py",
        "inputs": {"queries": f"wiki/survey/2026-07-15-sf-queries.jsonl "
                              f"({len(queries)} rows, auto-read, frozen)",
                   "seed_manifest": f"wiki/survey/2026-07-15-sf-seed-manifest.jsonl "
                                    f"({len(seed_ids)} ids, auto-read)",
                   "routes": os.path.relpath(routes_file, REPO).replace("\\", "/"),
                   "sentinel_data": os.path.relpath(sentinel_file, REPO).replace("\\", "/")},
        "matching_caveat": "offline approximation：无词干化、连字符折叠、词边界短语匹配；"
                           "HIT 方向保守可信，term-MISS 仍可能被 API 词干化召回——终证以执行期实测为准",
        "unparsed_queries": sorted(set(unparsed)),
        "sentinels": results,
        "outcome_counts": counts,
        "held_out_outcomes": holdouts,
        "verdict": "PASS" if not fail_reasons else "FAIL",
        "fail_reasons": fail_reasons,
        "gate_rule": "四分法：QUERY_HIT / SEED_GUARANTEED / EXACT_ROUTE_GUARANTEED / "
                     "REGISTERED_BOUNDARY(须回指 dated amendment) 之一；UNRESOLVED_MISS、"
                     "查询不可解析、无 held-out、held-out 被种子污染 = FAIL；"
                     "coverage_note 仅注释，绝不转换 outcome",
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "wb") as f:
        f.write((json.dumps(report, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    print(" ".join(f"{k}={v}" for k, v in counts.items()), f"verdict={report['verdict']}")
    for a, r in sorted(results.items()):
        ho = " HELD-OUT" if r["held_out"] else ""
        print(f"  {a} {r['outcome']:22s} qhits={len(r['query_hits'])}{ho} {r['title'][:46]}")
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
