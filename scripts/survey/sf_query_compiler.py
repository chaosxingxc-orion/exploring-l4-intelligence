#!/usr/bin/env python3
"""sf_query_compiler.py — offline arXiv query compiler for Gate S1 (P0-B).

Parses the 48 pre-registered exact-query fragments (SF-L1..SF-L8, Q1..Q6) out
of the frozen protocol document

    wiki/survey/2026-07-15-system-first-survey-protocol-v1.md (§4)

and deterministically assembles each into the final arXiv `search_query`
string per the compiled assembly spec (P0-B revision — category expressions
widened for SF-L1/L2/L4/L5, date-window exceptions, per-lane pagination cap
exception for SF-L7-Q3). Writes the frozen JSONL artifact

    wiki/survey/2026-07-15-sf-queries.jsonl

This is a pure protocol *compiler*, not a retrieval executor: it does no
network I/O of any kind. Only the Python standard library is imported, and
none of the imports below are capable of making a network request (no
urllib.request, no socket, no http.client, no requests, no ftplib, etc. —
only urllib.parse, which is a pure string-manipulation module).

Usage (from the umbrella repo root, any Python 3.x with only the stdlib):

    python scripts/survey/sf_query_compiler.py

Exit code 0 = 48/48 records compiled and all static validations passed.
Exit code 1 = parse failure or a static validation failure (details printed).
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import OrderedDict, defaultdict
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

COMPILER_VERSION = "sfqc-1.0.0"

REPO_ROOT = Path(__file__).resolve().parents[2]
PROTOCOL_MD = REPO_ROOT / "wiki" / "survey" / "2026-07-15-system-first-survey-protocol-v1.md"
OUTPUT_JSONL = REPO_ROOT / "wiki" / "survey" / "2026-07-15-sf-queries.jsonl"

EXPECTED_LANES = [f"SF-L{n}" for n in range(1, 9)]
EXPECTED_Q_NUMS = list(range(1, 7))  # Q1..Q6

# ---------------------------------------------------------------------------
# §4 compiled assembly spec (P0-B revision — deterministic, no placeholders)
# ---------------------------------------------------------------------------

CATEGORY_MAP = {
    "SF-L1": ["cs.CL", "cs.AI", "cs.LG", "cs.CV", "cs.RO"],
    "SF-L2": ["cs.CL", "cs.AI", "cs.LG", "cs.CV", "cs.RO"],
    "SF-L4": ["cs.CL", "cs.AI", "cs.LG", "cs.CV", "cs.RO"],
    "SF-L5": ["cs.CL", "cs.AI", "cs.LG", "cs.CV", "cs.RO"],
    "SF-L3": ["cs.CL", "cs.AI", "cs.LG", "cs.CV", "cs.RO", "cs.SD", "eess.AS"],
    "SF-L6": ["cs.CL", "cs.AI", "cs.LG"],
    "SF-L7": ["cs.CL", "cs.AI", "cs.LG"],
    "SF-L8": ["cs.CL", "cs.AI", "cs.LG"],
}

DEFAULT_DATE_FROM = "202210010000"
DEFAULT_DATE_TO = "202607152359"

DATE_FROM_EXCEPTIONS = {
    "SF-L2-Q3": "202301010000",
    "SF-L3-Q3": "202301010000",
    "SF-L7-Q3": "202001010000",
}

DEFAULT_MAX_RESULTS = 75
MAX_RESULTS_EXCEPTIONS = {
    "SF-L7-Q3": 50,
}

START = 0
SORT_BY = "relevance"
SORT_ORDER = "descending"

DATE_FMT = "%Y%m%d%H%M"


class ParseError(SystemExit):
    """Raised (as SystemExit) on any structural parse failure — never
    silently skip a malformed line."""

    def __init__(self, message: str):
        super().__init__(f"[sf_query_compiler] PARSE FAILURE: {message}")


# ---------------------------------------------------------------------------
# Parsing §4
# ---------------------------------------------------------------------------

def load_protocol_text() -> str:
    if not PROTOCOL_MD.is_file():
        raise ParseError(f"protocol file not found: {PROTOCOL_MD}")
    return PROTOCOL_MD.read_text(encoding="utf-8")


def extract_section_4(full_text: str) -> str:
    m = re.search(r"^## §4.*?(?=^## §5)", full_text, flags=re.MULTILINE | re.DOTALL)
    if not m:
        raise ParseError("could not locate '## §4 ... ## §5' bounded section in protocol md")
    return m.group(0)


LANE_HEADER_RE = re.compile(r"^### (SF-L\d+)\b", flags=re.MULTILINE)


def split_lane_blocks(section4_text: str) -> "OrderedDict[str, str]":
    headers = list(LANE_HEADER_RE.finditer(section4_text))
    if not headers:
        raise ParseError("no '### SF-Lx' lane headers found inside §4")

    blocks: "OrderedDict[str, str]" = OrderedDict()
    for i, hm in enumerate(headers):
        lane_id = hm.group(1)
        start = hm.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(section4_text)
        block_text = section4_text[start:end]
        if lane_id in blocks:
            raise ParseError(f"duplicate lane header encountered: {lane_id}")
        blocks[lane_id] = block_text
    return blocks


def parse_q_fragments(lane_id: str, block_text: str) -> "OrderedDict[int, str]":
    fragments: "OrderedDict[int, str]" = OrderedDict()
    for line in block_text.splitlines():
        line_stripped = line.strip()
        if not line_stripped.startswith("- Q"):
            continue
        m = re.match(r"^-\s*Q(\d+)\s*`(.*)`", line_stripped)
        if not m:
            raise ParseError(
                f"{lane_id}: line starts with '- Q' but does not match the "
                f"expected '- Q<n> `<fragment>`' shape: {line_stripped!r}"
            )
        q_num = int(m.group(1))
        fragment = m.group(2)
        if not fragment.strip():
            raise ParseError(f"{lane_id} Q{q_num}: empty backtick-delimited fragment")
        if q_num in fragments:
            raise ParseError(f"{lane_id}: duplicate Q{q_num} line")
        fragments[q_num] = fragment
    return fragments


def parse_all_queries(full_text: str) -> "tuple[OrderedDict[str, str], list[str]]":
    """Returns (query_id -> raw decoded Q fragment, list of out-of-scope lane
    ids found in §4 but not compiled). Compilation scope is fixed to
    SF-L1..SF-L8 (48 Boolean arXiv queries) per the task spec. Any other lane
    subsection encountered in §4 (e.g. an amendment-added lane that is
    documented as carrying zero pre-registered Boolean queries, such as a
    chaining-only 'foundational lineage' lane) is recorded as out-of-scope
    and skipped rather than treated as a structural parse failure — but ONLY
    if it genuinely has zero '- Q<n> `...`' lines; if it has any, that is a
    real structural surprise and must hard-fail rather than be silently
    dropped."""
    section4 = extract_section_4(full_text)
    lane_blocks = split_lane_blocks(section4)

    out_of_scope = []
    for lane_id in lane_blocks:
        if lane_id in EXPECTED_LANES:
            continue
        stray_fragments = parse_q_fragments(lane_id, lane_blocks[lane_id])
        if stray_fragments:
            raise ParseError(
                f"{lane_id}: out-of-scope lane (not in {EXPECTED_LANES}) but "
                f"contains {len(stray_fragments)} '- Q<n>' Boolean query line(s) "
                f"{sorted(stray_fragments.keys())} — refusing to silently drop "
                f"real query content; compiler scope must be revisited"
            )
        out_of_scope.append(lane_id)

    missing_lanes = [lane_id for lane_id in EXPECTED_LANES if lane_id not in lane_blocks]
    if missing_lanes:
        raise ParseError(f"expected lanes missing from §4: {missing_lanes}")

    all_queries: "OrderedDict[str, str]" = OrderedDict()
    for lane_id in EXPECTED_LANES:
        fragments = parse_q_fragments(lane_id, lane_blocks[lane_id])
        found_nums = sorted(fragments.keys())
        if found_nums != EXPECTED_Q_NUMS:
            raise ParseError(
                f"{lane_id}: expected Q-numbers {EXPECTED_Q_NUMS}, found {found_nums}"
            )
        for q_num in EXPECTED_Q_NUMS:
            query_id = f"{lane_id}-Q{q_num}"
            all_queries[query_id] = fragments[q_num]

    if len(all_queries) != 48:
        raise ParseError(f"expected 48 total Q fragments, parsed {len(all_queries)}")

    return all_queries, out_of_scope


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------

def lane_of(query_id: str) -> str:
    return query_id.rsplit("-Q", 1)[0]


def compute_record_hash(record_wo_hash: dict) -> str:
    compact = json.dumps(record_wo_hash, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(compact.encode("utf-8")).hexdigest()


def assemble_record(query_id: str, q_fragment: str) -> dict:
    lane = lane_of(query_id)
    categories = CATEGORY_MAP[lane]
    cat_expr = " OR ".join(f"cat:{c}" for c in categories)

    date_from = DATE_FROM_EXCEPTIONS.get(query_id, DEFAULT_DATE_FROM)
    date_to = DEFAULT_DATE_TO
    max_results = MAX_RESULTS_EXCEPTIONS.get(query_id, DEFAULT_MAX_RESULTS)

    decoded = f"({cat_expr}) AND submittedDate:[{date_from} TO {date_to}] AND ({q_fragment})"
    encoded = quote(decoded)

    record = OrderedDict()
    record["query_id"] = query_id
    record["lane"] = lane
    record["decoded_search_query"] = decoded
    record["url_encoded_search_query"] = encoded
    record["categories"] = categories
    record["date_from"] = date_from
    record["date_to"] = date_to
    record["start"] = START
    record["max_results"] = max_results
    record["sortBy"] = SORT_BY
    record["sortOrder"] = SORT_ORDER
    record["compiler_version"] = COMPILER_VERSION
    record["record_sha256"] = compute_record_hash(dict(record))
    return record


def compile_records(all_queries: "OrderedDict[str, str]") -> list:
    return [assemble_record(qid, frag) for qid, frag in all_queries.items()]


# ---------------------------------------------------------------------------
# Static validation
# ---------------------------------------------------------------------------

CJK_RANGES = (
    (0x3400, 0x4DBF), (0x4E00, 0x9FFF), (0xF900, 0xFAFF),
    (0x3000, 0x303F),  # CJK punctuation (includes full-width parens etc.)
    (0xFF00, 0xFFEF),  # full-width forms
)


def has_cjk(s: str) -> bool:
    for ch in s:
        cp = ord(ch)
        if any(lo <= cp <= hi for lo, hi in CJK_RANGES):
            return True
    return False


BOOL_OP_RE = re.compile(r"\b(?:ANDNOT|andnot|AND|and|OR|or)\b")
QUOTED_SPAN_RE = re.compile(r'"[^"]*"')


def run_validations(records: list) -> "tuple[list, bool]":
    results = []  # list of (check_name, passed_bool, details_str)
    all_ok = True

    def record_check(name, passed, details=""):
        nonlocal all_ok
        results.append((name, passed, details))
        if not passed:
            all_ok = False

    # 1. row count == 48
    record_check("row_count_equals_48", len(records) == 48, f"got {len(records)}")

    # 2. query_id uniqueness
    ids = [r["query_id"] for r in records]
    dupes = sorted({q for q in ids if ids.count(q) > 1})
    record_check("query_id_unique", len(set(ids)) == len(ids), f"duplicates={dupes}" if dupes else f"n_unique={len(set(ids))}")

    # 3. no residual Chinese-conditional-placeholder / ellipsis / '<' '>' stubs
    placeholder_bad = []
    for r in records:
        d = r["decoded_search_query"]
        if has_cjk(d):
            placeholder_bad.append((r["query_id"], "CJK characters present"))
            continue
        if "…" in d or "..." in d:
            placeholder_bad.append((r["query_id"], "ellipsis present"))
            continue
        if "<" in d or ">" in d:
            placeholder_bad.append((r["query_id"], "angle-bracket placeholder residue"))
            continue
    record_check(
        "no_placeholder_or_ellipsis_or_angle_bracket_residue",
        len(placeholder_bad) == 0,
        f"failures={placeholder_bad}" if placeholder_bad else "clean",
    )

    # 4. no stray '[' / ']' outside the legitimate submittedDate:[...] token
    stray_bracket_bad = []
    submitted_date_re = re.compile(r"submittedDate:\[[^\]]*\]")
    for r in records:
        d = r["decoded_search_query"]
        stripped = submitted_date_re.sub("", d)
        if "[" in stripped or "]" in stripped:
            stray_bracket_bad.append(r["query_id"])
    record_check(
        "no_stray_brackets_outside_submittedDate",
        len(stray_bracket_bad) == 0,
        f"failures={stray_bracket_bad}" if stray_bracket_bad else "clean",
    )

    # 5. balanced parentheses and double quotes
    unbalanced = []
    for r in records:
        d = r["decoded_search_query"]
        if d.count("(") != d.count(")"):
            unbalanced.append((r["query_id"], "parens"))
        if d.count('"') % 2 != 0:
            unbalanced.append((r["query_id"], "quotes"))
    record_check(
        "balanced_parens_and_quotes",
        len(unbalanced) == 0,
        f"failures={unbalanced}" if unbalanced else "clean",
    )

    # 6. AND/OR/ANDNOT are fully uppercase wherever they occur as *operators*
    # (quoted natural-language phrases like abs:"reasoning and acting" are
    # masked out first — "and" inside a phrase literal is not an operator).
    bad_case = []
    for r in records:
        d = r["decoded_search_query"]
        structural = QUOTED_SPAN_RE.sub(lambda m: '"' + ("#" * (len(m.group(0)) - 2)) + '"', d)
        for m in BOOL_OP_RE.finditer(structural):
            token = m.group(0)
            if token not in ("AND", "OR", "ANDNOT"):
                bad_case.append((r["query_id"], token))
    record_check(
        "boolean_operators_fully_uppercase",
        len(bad_case) == 0,
        f"failures={bad_case}" if bad_case else "clean",
    )

    # 7. dates are well-formed and from <= to
    bad_dates = []
    for r in records:
        try:
            dt_from = datetime.strptime(r["date_from"], DATE_FMT)
            dt_to = datetime.strptime(r["date_to"], DATE_FMT)
        except ValueError as e:
            bad_dates.append((r["query_id"], f"unparseable: {e}"))
            continue
        if dt_from > dt_to:
            bad_dates.append((r["query_id"], "date_from > date_to"))
    record_check(
        "dates_well_formed_and_ordered",
        len(bad_dates) == 0,
        f"failures={bad_dates}" if bad_dates else "clean",
    )

    # 8. each lane has exactly 6 records
    per_lane = defaultdict(int)
    for r in records:
        per_lane[r["lane"]] += 1
    lane_mismatch = {lane: per_lane.get(lane, 0) for lane in EXPECTED_LANES if per_lane.get(lane, 0) != 6}
    record_check(
        "each_lane_has_exactly_6_queries",
        len(lane_mismatch) == 0,
        f"mismatch={lane_mismatch}" if lane_mismatch else "all lanes=6",
    )

    # --- bonus sanity checks (not requested verbatim, cheap and strictly additive) ---

    # categories match the frozen mapping
    cat_bad = []
    for r in records:
        expected = CATEGORY_MAP[r["lane"]]
        if r["categories"] != expected:
            cat_bad.append(r["query_id"])
    record_check(
        "bonus_categories_match_frozen_mapping",
        len(cat_bad) == 0,
        f"failures={cat_bad}" if cat_bad else "clean",
    )

    # date/max_results exceptions applied exactly where specified, nowhere else
    exc_bad = []
    for r in records:
        qid = r["query_id"]
        expected_from = DATE_FROM_EXCEPTIONS.get(qid, DEFAULT_DATE_FROM)
        expected_max = MAX_RESULTS_EXCEPTIONS.get(qid, DEFAULT_MAX_RESULTS)
        if r["date_from"] != expected_from or r["date_to"] != DEFAULT_DATE_TO:
            exc_bad.append((qid, "date"))
        if r["max_results"] != expected_max:
            exc_bad.append((qid, "max_results"))
    record_check(
        "bonus_exceptions_applied_correctly",
        len(exc_bad) == 0,
        f"failures={exc_bad}" if exc_bad else "clean",
    )

    # record_sha256 recomputation matches stored value (self-consistency)
    hash_bad = []
    for r in records:
        wo_hash = {k: v for k, v in r.items() if k != "record_sha256"}
        recomputed = compute_record_hash(wo_hash)
        if recomputed != r["record_sha256"]:
            hash_bad.append(r["query_id"])
    record_check(
        "bonus_record_sha256_recomputes_identically",
        len(hash_bad) == 0,
        f"failures={hash_bad}" if hash_bad else "clean",
    )

    return results, all_ok


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main() -> int:
    full_text = load_protocol_text()
    all_queries, out_of_scope_lanes = parse_all_queries(full_text)

    print(f"[sf_query_compiler] parsed {len(all_queries)} Q fragments from §4 "
          f"({len(EXPECTED_LANES)} lanes x {len(EXPECTED_Q_NUMS)} each)")
    if out_of_scope_lanes:
        print(f"[sf_query_compiler] NOTE: found {len(out_of_scope_lanes)} lane subsection(s) "
              f"in §4 outside compiler scope (SF-L1..SF-L8), each verified to carry ZERO "
              f"'- Q<n>' Boolean query lines, so excluded from compilation without loss: "
              f"{out_of_scope_lanes}")

    records = compile_records(all_queries)

    OUTPUT_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSONL, "w", encoding="utf-8", newline="\n") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False))
            f.write("\n")
    print(f"[sf_query_compiler] wrote {len(records)} records -> {OUTPUT_JSONL}")

    results, all_ok = run_validations(records)

    print("\n[sf_query_compiler] static validation report")
    print("=" * 72)
    for name, passed, details in results:
        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] {name} :: {details}")
    print("=" * 72)
    print(f"OVERALL: {'PASS' if all_ok else 'FAIL'}")

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
