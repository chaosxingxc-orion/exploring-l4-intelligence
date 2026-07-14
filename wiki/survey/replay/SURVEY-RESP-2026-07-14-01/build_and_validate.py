#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_and_validate.py

Deterministic, honest "replay bundle" builder for Survey v2, response id
SURVEY-RESP-2026-07-14-01, under the doctoral-review remediation P0.

Regenerates every other file in this directory from the two canonical
inputs (A = search-query log, B = scout ledger round 2) plus a small set
of literal, task-supplied correction facts (five-lens verification /
coordinator corrections) that are not mechanically derivable from A/B and
are therefore hardcoded as clearly-labeled constants below, never invented.

Hard rules honoured here (see wiki/2026-07-14-survey-response-replayability-template.md):
  - No invented timestamps: A only has date-level granularity, so
    timestamp_utc is always null; timestamp_date_only carries the date.
  - No invented raw responses / screening decisions: fields that do not
    exist in the source data are written literally as "RAW_EVENT_UNAVAILABLE".
  - Stdlib only, no network. No datetime.now() / random. Generation date is
    hardcoded. Deterministic on every rerun against the same inputs.
  - UTF-8, no BOM, LF line endings on every text file this script writes.
  - Exits non-zero if any validation check fails.

Run:
    C:\\Python314\\python.exe build_and_validate.py
"""

import hashlib
import json
import re
import sys
from pathlib import Path

# --------------------------------------------------------------------------
# 0. Constants (hardcoded, never computed from wall-clock time)
# --------------------------------------------------------------------------

GENERATION_DATE = "2026-07-14"
RESPONSE_ID = "SURVEY-RESP-2026-07-14-01"
RUN_ID = "RUN-SURVEYV2-01"
AGENT_ID = ("survey-v2-workflow wf_c6ed06f2 "
            "(session agents; per-query agent identity RAW_EVENT_UNAVAILABLE)")
GENERATED_BY_CMD = "C:\\Python314\\python.exe build_and_validate.py"
CORRECTION_VERIFICATION_STATUS = (
    "AI fulltext recompute, single-pass (wf_2c70bfda facts-lens); "
    "human double-review pending (P1)"
)
DOWNGRADE_REASON = (
    "P0-5: machine label exceeded verification depth (headers: WebSearch "
    "cite-check, not fulltext); template §2.6 requires locator for "
    "CLAIM_VERIFIED — none present"
)

BUNDLE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BUNDLE_DIR.parent.parent.parent.parent  # .../wiki/survey/replay/<id> -> repo root

INPUT_A_REL = "wiki/survey/2026-07-14-search-query-log.jsonl"
INPUT_B_REL = "wiki/survey/2026-07-14-scout-ledger-round2.json"
INPUT_TEMPLATE_REL = "wiki/2026-07-14-survey-response-replayability-template.md"

INPUT_A = REPO_ROOT / INPUT_A_REL
INPUT_B = REPO_ROOT / INPUT_B_REL
INPUT_TEMPLATE = REPO_ROOT / INPUT_TEMPLATE_REL

# Provenance, established by manual `git show <commit>:<path> | sha256sum`
# cross-checks performed once, by hand, before this script was written
# (recorded here as a fixed historical fact, not recomputed by the script,
# since the script has no git/network dependency). The script INDEPENDENTLY
# recomputes sha256 of the on-disk bytes below and does not rely on these
# strings for anything except the honesty note in manifest.yaml.
INPUT_PROVENANCE = {
    INPUT_A_REL: {
        "role": "A: search query log",
        "claimed_canonical_commit": "233dc7eb9224b5d7bc8df7bfd81a616ab15c6917",
        "verified": True,
        "note": "git blob at 233dc7eb matches on-disk bytes exactly (manually "
                "verified 2026-07-14 via `git show 233dc7eb:<path> | sha256sum`).",
    },
    INPUT_B_REL: {
        "role": "B: scout ledger round 2",
        "claimed_canonical_commit": "233dc7eb9224b5d7bc8df7bfd81a616ab15c6917",
        "verified": True,
        "note": "git blob at 233dc7eb matches on-disk bytes exactly (manually "
                "verified 2026-07-14 via `git show 233dc7eb:<path> | sha256sum`).",
    },
    INPUT_TEMPLATE_REL: {
        "role": "template spec (replayability template)",
        "claimed_canonical_commit": "233dc7eb9224b5d7bc8df7bfd81a616ab15c6917",
        "verified": False,
        "note": "TASK PREMISE WAS FALSE, RECORDED HONESTLY RATHER THAN SILENTLY "
                "ACCEPTED: this file does NOT exist at 233dc7eb "
                "(`git show 233dc7eb:<path>` fails with 'exists on disk, but "
                "not in 233dc7eb'). It was introduced 2 commits later at "
                "b41f9f85db359fa5b13cadbcb4024c130d43542e "
                "(2026-07-14T10:38:41+08:00, 'docs(review): check in three "
                "received 2026-07-14 review artifacts') and is byte-identical "
                "from that commit through current HEAD "
                "58ebc7707c736fe0d8cd01bfcb3af3a7564d002f. The true canonical "
                "commit for this input is b41f9f85db359fa5b13cadbcb4024c130d43542e.",
    },
}

# --------------------------------------------------------------------------
# 1. Small IO / hashing helpers
# --------------------------------------------------------------------------


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def write_text_utf8_lf(path, text):
    """UTF-8, no BOM, LF only. `text` must already end with a single trailing
    newline (or not); we normalize to end with exactly one trailing '\n'."""
    if not text.endswith("\n"):
        text = text + "\n"
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    with open(path, "wb") as f:
        f.write(text.encode("utf-8"))


def write_jsonl(path, rows):
    lines = [json.dumps(r, ensure_ascii=False) for r in rows]
    write_text_utf8_lf(path, "\n".join(lines) + "\n" if lines else "")


def write_json(path, obj):
    write_text_utf8_lf(path, json.dumps(obj, ensure_ascii=False, indent=2))


def file_stats(path):
    raw = path.read_bytes()
    lines = raw.decode("utf-8").split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    return {"bytes": len(raw), "lines": len(lines), "sha256": sha256_bytes(raw)}


# --------------------------------------------------------------------------
# 2. Minimal, restricted YAML dump/load (stdlib only; no PyYAML available)
#
# Restricted grammar this supports (sufficient for flow_report.yaml and
# manifest.yaml, both authored by this script, nothing else):
#   - top level: dict
#   - dict values: scalar (str/int/bool/None) | dict | list
#   - list values: all-scalar, OR all-dict-with-only-scalar-values
#   - dicts nest to arbitrary depth; lists do not nest inside list items
#   - strings are always emitted double-quoted via json.dumps() escaping,
#     which is also valid YAML double-quoted-scalar syntax
# --------------------------------------------------------------------------


def _y_is_scalar(v):
    return v is None or isinstance(v, (bool, int, str))


def _y_scalar(v):
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, str):
        return json.dumps(v, ensure_ascii=False)
    raise TypeError("unsupported scalar type: %r" % (type(v),))


def _y_dump_dict(d, indent):
    pad = "  " * indent
    lines = []
    for k, v in d.items():
        if _y_is_scalar(v):
            lines.append("%s%s: %s" % (pad, k, _y_scalar(v)))
        elif isinstance(v, list):
            if not v:
                lines.append("%s%s: []" % (pad, k))
            else:
                lines.append("%s%s:" % (pad, k))
                lines.extend(_y_dump_list(v, indent + 1))
        elif isinstance(v, dict):
            if not v:
                lines.append("%s%s: {}" % (pad, k))
            else:
                lines.append("%s%s:" % (pad, k))
                lines.extend(_y_dump_dict(v, indent + 1))
        else:
            raise TypeError("unsupported dict-value type: %r" % (type(v),))
    return lines


def _y_dump_list(items, indent):
    pad = "  " * indent
    lines = []
    for item in items:
        if _y_is_scalar(item):
            lines.append("%s- %s" % (pad, _y_scalar(item)))
        elif isinstance(item, dict):
            entries = list(item.items())
            if not entries:
                lines.append("%s- {}" % (pad,))
                continue
            k0, v0 = entries[0]
            if not _y_is_scalar(v0):
                raise TypeError("list-item dict values must be scalar (restricted grammar)")
            lines.append("%s- %s: %s" % (pad, k0, _y_scalar(v0)))
            for k, v in entries[1:]:
                if not _y_is_scalar(v):
                    raise TypeError("list-item dict values must be scalar (restricted grammar)")
                lines.append("%s  %s: %s" % (pad, k, _y_scalar(v)))
        else:
            raise TypeError("unsupported list-item type: %r" % (type(item),))
    return lines


def yaml_dump(obj):
    if not isinstance(obj, dict):
        raise TypeError("top level must be a dict")
    return "\n".join(_y_dump_dict(obj, 0)) + "\n"


def yaml_load(text):
    raw_lines = text.split("\n")
    lines = []
    for l in raw_lines:
        if l.strip() == "":
            continue
        stripped = l.lstrip(" ")
        spaces = len(l) - len(stripped)
        if spaces % 2 != 0:
            raise ValueError("odd indentation not supported: %r" % (l,))
        lines.append((spaces // 2, stripped))
    n = len(lines)
    pos = 0

    def parse_scalar(s):
        s = s.strip()
        if s == "null":
            return None
        if s == "true":
            return True
        if s == "false":
            return False
        if s == "[]":
            return []
        if s == "{}":
            return {}
        if s.startswith('"'):
            return json.loads(s)
        return int(s)

    def parse_list(indent):
        nonlocal pos
        items = []
        while pos < n and lines[pos][0] == indent and lines[pos][1].startswith("- "):
            content = lines[pos][1][2:]
            if ": " in content:
                k0, v0 = content.split(": ", 1)
                item = {k0: parse_scalar(v0)}
                pos += 1
                while pos < n and lines[pos][0] == indent + 1 and not lines[pos][1].startswith("- "):
                    content2 = lines[pos][1]
                    if ": " not in content2:
                        raise ValueError("expected flat key: value in list-item dict, got %r" % (content2,))
                    k, v = content2.split(": ", 1)
                    item[k] = parse_scalar(v)
                    pos += 1
                items.append(item)
            else:
                items.append(parse_scalar(content))
                pos += 1
        return items

    def parse_dict(indent):
        nonlocal pos
        d = {}
        while pos < n and lines[pos][0] == indent:
            content = lines[pos][1]
            if content.startswith("- "):
                raise ValueError("expected dict key, found list item at this level: %r" % (content,))
            if ": " in content:
                key, val = content.split(": ", 1)
                d[key] = parse_scalar(val)
                pos += 1
            elif content.endswith(":"):
                key = content[:-1]
                pos += 1
                if pos < n and lines[pos][0] == indent + 1 and lines[pos][1].startswith("- "):
                    d[key] = parse_list(indent + 1)
                elif pos < n and lines[pos][0] == indent + 1:
                    d[key] = parse_dict(indent + 1)
                else:
                    raise ValueError("expected nested block after %r:" % (key,))
            else:
                raise ValueError("cannot parse dict line: %r" % (content,))
        return d

    return parse_dict(0)


# --------------------------------------------------------------------------
# 3. Load inputs A and B
# --------------------------------------------------------------------------


def load_input_a():
    raw = INPUT_A.read_bytes().decode("utf-8")
    events = []
    for line in raw.split("\n"):
        if line.strip() == "":
            continue
        events.append(json.loads(line))
    return events


def load_input_b():
    data = json.loads(INPUT_B.read_bytes().decode("utf-8"))
    fams = data["families"]
    rows = []
    idx = 0
    for fam in fams:
        for p in fam["papers"]:
            idx += 1
            row = dict(p)
            row["_lane"] = fam["lane"]
            row["_row_index"] = idx  # 1-based, file order
            rows.append(row)
    return data, rows


# --------------------------------------------------------------------------
# 4. search_events.jsonl (file a)
# --------------------------------------------------------------------------

_FAILURE_PATTERNS = [
    (re.compile(r"\bFAILED\b"), "FAILED"),
    (re.compile(r"\bBLOCKED\b"), "BLOCKED"),
    (re.compile(r"\bBlocked\b"), "Blocked"),
    (re.compile(r"NOT_RESOLVED"), "NOT_RESOLVED"),
    (re.compile(r"socket-failed"), "socket-failed"),
    (re.compile(r"\bdenied\b", re.IGNORECASE), "denied"),
]


def classify_status(note):
    matched = [name for pat, name in _FAILURE_PATTERNS if pat.search(note or "")]
    status = "FAILED" if matched else "OUTCOME_UNVERIFIED_RAW_UNAVAILABLE"
    return status, matched


def build_search_events(a_events):
    rows = []
    failed_substr_counts = {}
    n_failed = 0
    for i, ev in enumerate(a_events, start=1):
        status, matched = classify_status(ev.get("note", ""))
        if status == "FAILED":
            n_failed += 1
            for m in matched:
                failed_substr_counts[m] = failed_substr_counts.get(m, 0) + 1
        row = {
            "event_id": "SE-%06d" % i,
            "run_id": RUN_ID,
            "agent_id": AGENT_ID,
            "timestamp_utc": None,
            "timestamp_date_only": ev["date"],
            "lane_id": ev["lane"],
            "operation": "SEARCH" if ev["engine"] == "WebSearch" else "FETCH",
            "engine": ev["engine"],
            "exact_query": ev["query"],
            "requested_limit_raw": ev["result_cap"],
            "note": ev["note"],
            "raw_response_path": None,
            "raw_response_sha256": "RAW_EVENT_UNAVAILABLE",
            "status": status,
        }
        rows.append(row)
    stats = {
        "total": len(rows),
        "search": sum(1 for r in rows if r["operation"] == "SEARCH"),
        "fetch": sum(1 for r in rows if r["operation"] == "FETCH"),
        "failed": n_failed,
        "outcome_unverified": sum(1 for r in rows if r["status"] == "OUTCOME_UNVERIFIED_RAW_UNAVAILABLE"),
        "failed_substr_counts": failed_substr_counts,
    }
    return rows, stats


# --------------------------------------------------------------------------
# 5. papers.jsonl + dedup_report.json (files b, e)
# --------------------------------------------------------------------------

ARXIV_RE = re.compile(r"(\d{4}\.\d{4,5})")

# Explicit ALIAS_CLUSTERS table (Stage 3). Each entry: member id-strings
# (verbatim, exact match against B's `id` field) known/verified to denote
# the SAME underlying work despite different id spellings, PLUS the basis
# for that claim. The first 5 entries were named in the task; the last two
# (aqa-ttrl-2510.05478, mbr-asr-2025) were flagged uncertain from bare
# id-string inspection alone and PROMOTED to confirmed merges only after
# corroboration was found inside B itself: B's own "dedup_rule" field
# states explicit lane-recurrence counts ("aqa-ttrl-2510.05478 (3)",
# "mbr-asr-2510.19471 (4)") that are reproduced EXACTLY by these merges,
# and the `our_data` benchmark-tuple fields match cleanly and exclusively
# across the merged rows (verified by inspection, not fabricated).
ALIAS_CLUSTERS = [
    {
        "members": [
            "scaling-auditory-cognition-2025", "AuditoryTTC-2503.23395",
            "auditory-ttc-2503.23395", "dang2025-auditory-cognition-ttc",
            "ttc-audio-2025",
        ],
        "basis": "task-specified cluster to verify+include; VERIFIED: B's own "
                 "dedup_rule field states 'scaling-auditory-cognition-2503.23395 "
                 "(6 lanes)' — these 5 id-strings (6 rows, since "
                 "auditory-ttc-2503.23395 itself is an exact-string duplicate "
                 "across kill-I1/kill-UMBRELLA) span exactly the 6 distinct "
                 "lanes audio-understanding-ttc, audio-judge-multi, "
                 "candidate-support-diversity, kill-I1, kill-I2, kill-UMBRELLA.",
    },
    {
        "members": [
            "walking-through-uncertainty-2026", "kuan2026-allm-uncertainty",
            "I3-01 (2604.25591)",
        ],
        "basis": "task-specified cluster to verify+include; VERIFIED: B's own "
                 "dedup_rule field states 'walking-through-uncertainty-2604.25591 "
                 "(3)' — matches exactly 3 distinct lanes "
                 "(audio-understanding-ttc, selective-prediction-conformal, "
                 "kill-I3); all 3 rows also share identical our_data = "
                 "['mmau-mini','mmar','mmsu'], a tuple otherwise unique to "
                 "this cluster (5 rows total in B carry that tuple, and they "
                 "split cleanly 3/2 into this cluster and the aqa-ttrl cluster "
                 "below, with no stray rows).",
    },
    {
        "members": ["audio-mind-agentic-2026", "AudioMind-2605.28480"],
        "basis": "task-specified cluster to verify+include; cross-lane xlane "
                 "tags point at each other's lane (row35 agentic-lane->xlane "
                 "L5=audio-understanding-ttc; row73 audio-understanding-ttc "
                 "paper AudioMind-2605.28480 in the agentic lane with "
                 "xlane L5); same grade (FT) and strength (PARTIAL).",
    },
    {
        "members": ["coverageguaranteed2025conformalSER", "I3-03 (2503.22712)"],
        "basis": "task-specified cluster (coverageguaranteed/I3-03) to "
                 "verify+include; xlane cross-references match "
                 "(row4 ser-selection-abstention -> xlane L13=kill-I3; "
                 "row92 kill-I3 'I3-03 (2503.22712)' -> xlane L1="
                 "ser-selection-abstention, i.e. row4's own lane).",
    },
    {
        "members": ["ernez2023-conformal-asr", "I3-04 ernez-conformal"],
        "basis": "task-specified cluster (ernez/I3-04) to verify+include; "
                 "xlane cross-references match (row65 "
                 "selective-prediction-conformal -> xlane L13=kill-I3; "
                 "row93 kill-I3 'I3-04 ernez-conformal' -> xlane "
                 "L9=selective-prediction-conformal, row65's own lane); "
                 "identical grade (AB) and strength (DIRECT).",
    },
    {
        "members": ["aqa-ttrl-2025", "AQA-TTRL-2510.05478"],
        "basis": "task named this 'aqa-ttrl x2' (the exact-string duplicate "
                 "of 'aqa-ttrl-2025' alone, rows 33 & 88, already caught by "
                 "Stage 1 exact-id dedup). On inspection this understates the "
                 "cluster: B's own dedup_rule field states "
                 "'aqa-ttrl-2510.05478 (3)' lanes, which only reconciles if "
                 "'AQA-TTRL-2510.05478' (row 39, audio-judge-multi) is the "
                 "SAME work — confirmed: rows 33/39/88 share identical "
                 "our_data=['mmau-mini','mmar','mmsu'] (row88's our_data is "
                 "empty but its xlane L5,L6 cross-references both other "
                 "rows' lanes), and 33+39+88 span exactly 3 lanes "
                 "(audio-understanding-ttc, audio-judge-multi, kill-I2), "
                 "matching the '(3)' count exactly. Promoted from an initial "
                 "'uncertain pair' (bare id strings alone would not justify "
                 "this) to a confirmed merge on this corroborating evidence.",
    },
    {
        "members": ["mbr-asr-2510.19471", "mbr-asr-2025"],
        "basis": "task named this 'mbr-asr-2510.19471 duplicates' (the "
                 "arXiv-id-regex-caught pair mbr-asr-2510.19471 / "
                 "MBR-ASR-2510.19471, rows 76+113 / 99, already merged by "
                 "Stage 2). On inspection this understates the cluster: B's "
                 "own dedup_rule field states 'mbr-asr-2510.19471 (4)' "
                 "lanes, which only reconciles if 'mbr-asr-2025' (row 85, "
                 "kill-I2, note 'text-only, I1 boundary') is the SAME work "
                 "— confirmed: row85's our_data=['librispeech','fleurs-r'] "
                 "is a strict subset shared exactly with row99's identical "
                 "tuple, and rows 76/85/99/113 span exactly 4 lanes "
                 "(kill-I1, kill-I2, kill-I4, kill-UMBRELLA), matching the "
                 "'(4)' count exactly. Promoted from an initial 'uncertain "
                 "pair' to a confirmed merge on this corroborating evidence; "
                 "the row's own cautionary note ('text-only, I1 boundary') "
                 "is preserved verbatim in this paper's strength_conflict "
                 "(strengths include 'NONE' alongside 'DIRECT'/'PARTIAL').",
    },
]


def build_papers_and_dedup(b_rows):
    n_raw = len(b_rows)

    # Stage 1: exact id-string dedup
    stage1 = {}
    for r in b_rows:
        stage1.setdefault(r["id"], []).append(r)
    stage1_ids = sorted(stage1.keys(), key=lambda k: stage1[k][0]["_row_index"])
    n_stage1 = len(stage1_ids)

    parent = {k: k for k in stage1_ids}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    # Stage 2: arXiv-id regex grouping
    arxiv_groups = {}
    for k in stage1_ids:
        m = ARXIV_RE.search(k)
        if m:
            arxiv_groups.setdefault(m.group(1), []).append(k)
    stage2_group_report = []
    n_stage2_merges = 0
    for aid, members in sorted(arxiv_groups.items()):
        if len(members) > 1:
            for m in members[1:]:
                if find(members[0]) != find(m):
                    n_stage2_merges += 1
                union(members[0], m)
            stage2_group_report.append({"arxiv_id": aid, "members": members})
    n_stage2 = len(set(find(k) for k in stage1_ids))

    # Stage 3: explicit alias clusters
    n_stage3_merges = 0
    missing_alias_members = []
    for cluster in ALIAS_CLUSTERS:
        present = [m for m in cluster["members"] if m in stage1]
        missing = [m for m in cluster["members"] if m not in stage1]
        if missing:
            missing_alias_members.extend(missing)
        for m in present[1:]:
            if find(present[0]) != find(m):
                n_stage3_merges += 1
            union(present[0], m)
    if missing_alias_members:
        raise RuntimeError("ALIAS_CLUSTERS references ids not found in B: %r" % (missing_alias_members,))
    n_stage3 = len(set(find(k) for k in stage1_ids))

    # Assemble final clusters, in order of first appearance (row index)
    cluster_map = {}
    for k in stage1_ids:
        cluster_map.setdefault(find(k), []).append(k)
    roots_in_order = sorted(
        cluster_map.keys(),
        key=lambda root: min(stage1[m][0]["_row_index"] for m in cluster_map[root]),
    )

    basis_by_first_member = {c["members"][0]: c["basis"] for c in ALIAS_CLUSTERS}
    arxiv_basis_by_id = {g["arxiv_id"]: g["members"] for g in stage2_group_report}

    papers = []
    paper_id_by_source_row_index = {}
    for i, root in enumerate(roots_in_order, start=1):
        member_ids = sorted(cluster_map[root], key=lambda m: stage1[m][0]["_row_index"])
        all_rows = []
        for m in member_ids:
            all_rows.extend(stage1[m])
        all_rows = sorted(all_rows, key=lambda r: r["_row_index"])

        # canonical_key: first arXiv id found among member id-strings
        # (deterministic order = first-appearance order), else the
        # first-appearing member id-string as a slug.
        canonical_key = None
        for m in member_ids:
            am = ARXIV_RE.search(m)
            if am:
                canonical_key = am.group(1)
                break
        if canonical_key is None:
            canonical_key = member_ids[0]

        lanes = sorted(set(r["_lane"] for r in all_rows))
        grades_claimed = [
            {"row_index": r["_row_index"], "lane": r["_lane"], "id": r["id"], "grade": r["grade"]}
            for r in all_rows
        ]
        strengths = [
            {"row_index": r["_row_index"], "lane": r["_lane"], "id": r["id"], "strength": r["strength"]}
            for r in all_rows
        ]
        kills = sorted(set(k for r in all_rows for k in r.get("kills", [])))
        distinct_grades = set(g["grade"] for g in grades_claimed)
        distinct_strengths = set(s["strength"] for s in strengths)
        grade_effective = "ABSTRACT_VERIFIED" if (distinct_grades & {"FT", "AB"}) else "DISCOVERED"

        # merge_basis
        if len(member_ids) == 1:
            merge_basis = ("singleton (no exact-id duplicate, no shared embedded "
                            "arXiv id, not named in any alias cluster)")
        elif member_ids[0] in basis_by_first_member:
            merge_basis = basis_by_first_member[member_ids[0]]
        else:
            am = ARXIV_RE.search(member_ids[0])
            aid = am.group(1) if am else "?"
            merge_basis = ("arxiv_id_regex(%s): id-strings %r share the embedded "
                            "arXiv id %s" % (aid, member_ids, aid))
            if len(member_ids) < len(all_rows):
                merge_basis += ("; plus exact_id_string_dedup absorbing %d "
                                 "same-string row(s) across lanes"
                                 % (len(all_rows) - len(member_ids)))

        paper = {
            "paper_id": "P-%04d" % i,
            "canonical_key": canonical_key,
            "aliases": member_ids,
            "lanes": lanes,
            "source_rows": [
                {"row_index": r["_row_index"], "lane": r["_lane"], "id": r["id"]} for r in all_rows
            ],
            "grades_claimed": grades_claimed,
            "grade_effective": grade_effective,
            "kills": kills,
            "strengths": strengths,
            "strength_conflict": len(distinct_strengths) > 1,
            "grade_conflict": len(distinct_grades) > 1,
            "merge_basis": merge_basis,
        }
        papers.append(paper)
        for r in all_rows:
            paper_id_by_source_row_index[r["_row_index"]] = paper["paper_id"]

    n_final = len(papers)

    # dedup_report.json content
    multi_member = [p for p in papers if len(p["aliases"]) > 1]
    stage1_dup_ids = sorted([k for k, v in stage1.items() if len(v) > 1])

    hist_est = None  # filled by caller from B's own counts block

    dedup_report = {
        "generation_date": GENERATION_DATE,
        "source_file": INPUT_B_REL,
        "pipeline": [
            {
                "stage": 1,
                "name": "exact_id_string_dedup",
                "input_count": n_raw,
                "output_count": n_stage1,
                "rows_absorbed": n_raw - n_stage1,
                "detail": "id-strings appearing more than once across different "
                          "lane-family rows: " + "; ".join(
                              "%s (rows %s)" % (
                                  dup_id,
                                  ",".join(str(r["_row_index"]) for r in stage1[dup_id]),
                              )
                              for dup_id in stage1_dup_ids
                          ),
            },
            {
                "stage": 2,
                "name": "arxiv_id_regex_grouping",
                "regex": r"\d{4}\.\d{4,5}",
                "input_count": n_stage1,
                "output_count": n_stage2,
                "records_absorbed": n_stage1 - n_stage2,
                "groups": stage2_group_report,
            },
            {
                "stage": 3,
                "name": "explicit_alias_clusters",
                "input_count": n_stage2,
                "output_count": n_stage3,
                "records_absorbed": n_stage2 - n_stage3,
                "clusters_applied": len(ALIAS_CLUSTERS),
            },
        ],
        "final_unique_works": n_final,
        "multi_member_clusters": [
            {
                "paper_id": p["paper_id"],
                "canonical_key": p["canonical_key"],
                "aliases": p["aliases"],
                "source_row_indices": [sr["row_index"] for sr in p["source_rows"]],
                "lanes": p["lanes"],
                "n_lanes": len(p["lanes"]),
                "grade_conflict": p["grade_conflict"],
                "strength_conflict": p["strength_conflict"],
                "grades_seen": sorted(set(g["grade"] for g in p["grades_claimed"])),
                "strengths_seen": sorted(set(s["strength"] for s in p["strengths"])),
                "merge_basis": p["merge_basis"],
            }
            for p in multi_member
        ],
        "uncertain_pairs": [],
        "uncertain_pairs_resolution_note": (
            "Two candidate pairs were initially flagged uncertain from bare "
            "id-string/arXiv-id inspection alone: (1) 'AQA-TTRL-2510.05478' "
            "(row 39) vs the 'aqa-ttrl-2025' exact-dup pair (rows 33, 88); "
            "(2) 'mbr-asr-2025' (row 85) vs the 'mbr-asr-2510.19471' cluster "
            "(rows 76, 99, 113). Per the no-merge-when-in-doubt rule, both "
            "were NOT silently merged; both were instead cross-checked "
            "against B's own dedup_rule field (which states explicit "
            "lane-recurrence counts for these two canonical works: "
            "'aqa-ttrl-2510.05478 (3)' and 'mbr-asr-2510.19471 (4)') and "
            "against the our_data benchmark-tuple field for corroboration. "
            "Both counts and both tuple patterns reconcile exactly only if "
            "the merge is made, so both were promoted from uncertain to "
            "confirmed (see ALIAS_CLUSTERS entries in this script / "
            "multi_member_clusters aqa-ttrl-2025 and mbr-asr-2510.19471 "
            "above for the full evidence trail). No pairs remain uncertain "
            "after this cross-check."
        ),
        "historical_estimate_reproducibility": {
            "historical_value": "~93 (_est)",
            "source": "B: counts.unique_papers_after_cross_lane_dedup_est",
            "reproducible_by_any_mechanical_path_tested": False,
            "nearest_mechanical_values_actually_computed": {
                "stage1_exact_id_dedup": n_stage1,
                "stage2_plus_arxiv_id_regex": n_stage2,
                "stage3_final_plus_explicit_alias_clusters": n_stage3,
            },
            "note": ("None of the three mechanically-reproducible checkpoints "
                     "(%d / %d / %d) equals the historical estimate of ~93. "
                     "The nearest is the Stage-3 final count (%d), off by 1. "
                     "No further candidate merge was found in B (id strings, "
                     "embedded arXiv ids, dedup_rule lane-recurrence counts, "
                     "and our_data tuple cross-checks) that would close this "
                     "1-paper gap without fabricating a justification; it is "
                     "recorded as unexplained rather than silently rounded "
                     "away." % (n_stage1, n_stage2, n_stage3, n_stage3)),
        },
    }

    return papers, paper_id_by_source_row_index, dedup_report, {
        "n_raw": n_raw, "n_stage1": n_stage1, "n_stage2": n_stage2, "n_stage3": n_stage3,
    }


# --------------------------------------------------------------------------
# 6. claim_evidence.jsonl (file c)
# --------------------------------------------------------------------------


def cap_grade(raw_grade):
    if raw_grade in ("FT", "AB"):
        return "ABSTRACT_VERIFIED"
    if raw_grade in ("SC", "UNVERIFIED-CITATION"):
        return "DISCOVERED"
    raise ValueError("unknown grade %r" % (raw_grade,))


def build_claim_evidence(b_rows, paper_id_by_row_index):
    rows = []
    for r in sorted(b_rows, key=lambda x: x["_row_index"]):
        rows.append({
            "claim_id": "CL-%04d" % r["_row_index"],
            "source_row_id": r["id"],
            "ledger_row_index": r["_row_index"],
            "lane": r["_lane"],
            "paper_id": paper_id_by_row_index[r["_row_index"]],
            "original_grade": r["grade"],
            "effective_grade": cap_grade(r["grade"]),
            "downgrade_reason": DOWNGRADE_REASON,
        })
    n_base = len(rows)

    def resolve(id_str, papers_by_alias):
        return papers_by_alias[id_str]

    return rows, n_base


def find_row(b_rows, id_str):
    for r in b_rows:
        if r["id"] == id_str:
            return r
    raise KeyError(id_str)


def build_corrections(b_rows, papers, next_claim_start):
    alias_to_paper = {}
    for p in papers:
        for a in p["aliases"]:
            alias_to_paper[a] = p["paper_id"]

    def pid(alias):
        return alias_to_paper[alias]

    def ref(row_id):
        r = find_row(b_rows, row_id)
        return {"row_index": r["_row_index"], "lane": r["_lane"], "id": r["id"]}

    n = next_claim_start
    rows = []

    # 1. READ 2606.04680
    row_read = find_row(b_rows, "read-2026")
    rows.append({
        "claim_id": "CL-%04d" % n,
        "correction": True,
        "topic": "READ (arXiv 2606.04680) oracle-realization numbers",
        "paper_ids": [pid("read-2026")],
        "source_row_refs": [ref("read-2026")],
        "superseded_claim": ("~70-85% oracle (neighbor-matrix-v2.md L147, "
                              "coverage-and-kill-matrix-v2.md L24, "
                              "scout-ledger-round2.json L1223)"),
        "corrected": (
            "per Table 1 realized fraction (greedy−READ)/(greedy−oracle): "
            "LS-clean 16.5% (2.06/1.91/1.15), LS-other 11.9% (3.66/3.48/2.15), "
            "VCTK-noisy 17.3% (7.41/7.19/6.14), ASRU 7.7% (9.96/9.67/6.20), "
            "TALCS 67.5% (18.94/14.98/13.07), SWBD 68.5% (15.02/11.93/10.51), "
            "TEDLIUM3 54.3% (4.22/3.40/2.71), SPGI 43.5% (4.24/3.33/2.15); "
            "max 68.5%, LibriSpeech only 11.9–16.5%"
        ),
        "locator": "arXiv 2606.04680 Table 1",
        "paper_real_title": ("Read What You Hear: Reference-Free Hypotheses "
                              "Evaluation with Acoustic Discrepancy"),
        "verification_status": CORRECTION_VERIFICATION_STATUS,
    })
    n += 1

    # 2. mbr-asr 2510.19471
    rows.append({
        "claim_id": "CL-%04d" % n,
        "correction": True,
        "topic": "mbr-asr (arXiv 2510.19471) MBR scorer identity",
        "paper_ids": [pid("mbr-asr-2510.19471")],
        "source_row_refs": [ref("mbr-asr-2510.19471"), ref("MBR-ASR-2510.19471")],
        "superseded_claim": ("sota-cards-v2.md L20 F2 system column "
                              "'Whisper-lv3 + Llama-3 scorer' welded to MBR numbers"),
        "corrected": (
            "MBR utility = pairwise BLEU via sacrebleu, O(N²), no LLM in the "
            "MBR pipeline; 0.042 beam → 0.033 MBR (Tables 6/7, "
            "whisper-large-v3, LibriSpeech no-noise), oracle 0.013 (Table 1); "
            "Llama-3-8B-Instruct only scores the ProGRes comparator, which at "
            "0.043 LOSES to plain MBR 0.033 (Table 9) — correction "
            "strengthens the I1 kill."
        ),
        "locator": "arXiv 2510.19471 Tables 1, 6, 7, 9",
        "verification_status": CORRECTION_VERIFICATION_STATUS,
    })
    n += 1

    # 3. TAP-GER 2309.15649
    rows.append({
        "claim_id": "CL-%04d" % n,
        "correction": True,
        "topic": "TAP-GER (arXiv 2309.15649) in-pool-selector reclassification",
        "paper_ids": [pid("tap-ger-2309.15649")],
        "source_row_refs": [ref("tap-ger-2309.15649")],
        "superseded_claim": ("kill-I1 DIRECT (in-pool selector beats oracle): "
                              "8.72 < oracle 9.78 (Table 3, WSJ, frozen "
                              "InstructGPT w/ TAP, no fine-tuning)"),
        "corrected": (
            "the 8.72 < 9.78 number is real, BUT the operator is generative "
            "error correction producing out-of-pool text (Table 1: correction "
            "moves pool oracle 9.78→8.41; frozen GPT-2 gets 29.56 vs "
            "first-pass 11.87 — impossible for in-pool selection)."
        ),
        "reclassification": ("kill-I1 DIRECT (in-pool selector beats oracle) "
                              "→ pool-expansion/revision operator; contests "
                              "oracle-anchor semantics; NOT direct occupation "
                              "of in-pool selector identity"),
        "locator": "arXiv 2309.15649 Table 3 (WSJ, frozen InstructGPT+TAP), Table 1 (pool-oracle shift)",
        "verification_status": CORRECTION_VERIFICATION_STATUS,
    })
    n += 1

    # 4. ProGRes 2409.00217
    rows.append({
        "claim_id": "CL-%04d" % n,
        "correction": True,
        "topic": "ProGRes (arXiv 2409.00217) in-pool-selector reclassification "
                 "+ ledger internal inconsistency",
        "paper_ids": [pid("ProGRes-2409.00217")],
        "source_row_refs": [ref("ProGRes-2409.00217"), ref("progres-2409.00217")],
        "superseded_claim": "kill-I1 DIRECT (in-pool selector)",
        "corrected": ("expands n-best with LLM-generated hypotheses then "
                      "scores (Llama-3/GPT); not in-pool selection"),
        "reclassification": "kill-I1 DIRECT → candidate-expansion operator",
        "internal_inconsistency_note": (
            "ledger records strength=PARTIAL in one lane row (row 44, lane "
            "audio-judge-multi, id='ProGRes-2409.00217') and strength=DIRECT "
            "in another (row 78, lane kill-I1, id='progres-2409.00217') for "
            "the same paper; both source rows flagged here."
        ),
        "flagged_source_rows": [44, 78],
        "locator": "arXiv 2409.00217",
        "verification_status": CORRECTION_VERIFICATION_STATUS,
    })
    n += 1

    # 5. 5 coordinator-verified kills -> verification-depth cap
    coord_verified = [
        ("mbr-asr-2510.19471", "mbr-asr 2510.19471"),
        ("read-2026", "READ 2606.04680"),
        ("scaling-auditory-cognition-2025", "scaling-auditory 2503.23395"),
        ("AudioToolAgent-2510.02995", "AudioToolAgent 2510.02995"),
        ("jia2602decodingambiguous", "jia-SER 2602.03873"),
    ]
    rows.append({
        "claim_id": "CL-%04d" % n,
        "correction": True,
        "topic": "coordinator-verified-kills verification-depth cap",
        "paper_ids": [pid(a) for a, _ in coord_verified],
        "source_row_refs": [ref(a) for a, _ in coord_verified],
        "labels": [label for _, label in coord_verified],
        "superseded_claim": (
            "B._coordinator_note_2026_07_14: 'COORDINATOR-VERIFIED = "
            "mbr-asr 2510.19471, READ 2606.04680, scaling-auditory 2503.23395, "
            "AudioToolAgent 2510.02995, jia-SER 2602.03873' (implying a "
            "verification level at or above claim-verified)"
        ),
        "corrected": (
            "recorded depth = 'personal WebSearch existence check' → "
            "effective grade ABSTRACT_VERIFIED at best; double review with "
            "fixed version + locator scheduled (P1)."
        ),
        "locator": "RAW_EVENT_UNAVAILABLE (no page/section/table locator was "
                   "recorded for the coordinator-verification pass itself)",
        "verification_status": CORRECTION_VERIFICATION_STATUS,
    })
    n += 1

    return rows, n


# --------------------------------------------------------------------------
# 7. round2_new_targets.jsonl (file d)
# --------------------------------------------------------------------------

TITLE_AS_GIVEN_NOTE = "AS_GIVEN_BY_REVIEW_NOT_INDEPENDENTLY_VERIFIED"


def build_round2_new_targets():
    rows = [
        {
            "arxiv_or_venue_id": "2408.03314",
            "title": "Snell compute-optimal TTS",
            "title_verification": TITLE_AS_GIVEN_NOTE,
            "why_it_matters": ("in round-1 ledger & one v2 query note but "
                                "absent from v2 matrices — promote to "
                                "matrix-level"),
            "threatens": "RAW_EVENT_UNAVAILABLE",
            "required_action": "round-2 kill-matrix entry + abstract/fulltext grade",
        },
        {
            "arxiv_or_venue_id": "2505.11730",
            "title": "VG-Search: Rethinking Optimal Verification Granularity",
            "title_verification": TITLE_AS_GIVEN_NOTE,
            "why_it_matters": "RAW_EVENT_UNAVAILABLE",
            "threatens": "RAW_EVENT_UNAVAILABLE",
            "required_action": "round-2 kill-matrix entry + abstract/fulltext grade",
        },
        {
            "arxiv_or_venue_id": "2605.10991",
            "title": ("Test-Time Personalization: A Diagnostic Framework and "
                       "Probabilistic Fix for Scaling Failures"),
            "title_verification": TITLE_AS_GIVEN_NOTE,
            "why_it_matters": "closest methodology: BoN curve decomposition, oracle-vs-realized",
            "threatens": "RAW_EVENT_UNAVAILABLE",
            "required_action": "round-2 kill-matrix entry + abstract/fulltext grade",
        },
        {
            "arxiv_or_venue_id": "2512.02008",
            "title": "The Art of Scaling Test-Time Compute for Large Language Models",
            "title_verification": TITLE_AS_GIVEN_NOTE,
            "why_it_matters": "RAW_EVENT_UNAVAILABLE",
            "threatens": "RAW_EVENT_UNAVAILABLE",
            "required_action": "round-2 kill-matrix entry + abstract/fulltext grade",
        },
        {
            "arxiv_or_venue_id": "2506.17811",
            "title": "RoboMonkey",
            "title_verification": TITLE_AS_GIVEN_NOTE,
            "venue": "CoRL 2025, PMLR v305 pp.3200-3217",
            "why_it_matters": "VLA inference scaling law",
            "threatens": "RAW_EVENT_UNAVAILABLE",
            "required_action": "round-2 kill-matrix entry + abstract/fulltext grade",
        },
        {
            "arxiv_or_venue_id": "2606.02981",
            "title": ("Predicting Inference-Time Scaling Gains from Labeled "
                       "Validation-Set Output Statistics"),
            "title_verification": TITLE_AS_GIVEN_NOTE,
            "why_it_matters": ("label-assisted predictor — near the review's "
                                "own upgrade prescription"),
            "threatens": "I4 (differentiation must be label-free + supply axis + audio)",
            "required_action": "round-2 kill-matrix entry + abstract/fulltext grade",
        },
        {
            "arxiv_or_venue_id": "2607.05391",
            "title": "LLM-as-a-Verifier",
            "title_verification": TITLE_AS_GIVEN_NOTE,
            "why_it_matters": "recovers oracle headroom, text agents",
            "threatens": "RAW_EVENT_UNAVAILABLE",
            "required_action": "round-2 kill-matrix entry + abstract/fulltext grade",
        },
        {
            "arxiv_or_venue_id": "2602.12281",
            "title": "CoVer",
            "title_verification": TITLE_AS_GIVEN_NOTE,
            "why_it_matters": ("verifier selects rephrased instruction + action "
                                "chunks — supply-side selection"),
            "threatens": "Proposal E (NEAREST NEIGHBOR THREAT)",
            "required_action": "round-2 kill-matrix entry + abstract/fulltext grade",
        },
    ]
    return rows


# --------------------------------------------------------------------------
# 8. flow_report.yaml (file f)
# --------------------------------------------------------------------------


def build_flow_report(search_stats, dedup_counts, claim_rows_base, claim_rows_corr, unverified_citation_ids):
    n_abstract_verified = sum(1 for r in claim_rows_base if r["effective_grade"] == "ABSTRACT_VERIFIED")
    n_discovered = sum(1 for r in claim_rows_base if r["effective_grade"] == "DISCOVERED")
    flow = {
        "generated_by": GENERATED_BY_CMD,
        "generation_date": GENERATION_DATE,
        "events": {
            "search": search_stats["search"],
            "fetch": search_stats["fetch"],
            "failed": search_stats["failed"],
            "outcome_unverified_raw_unavailable": search_stats["outcome_unverified"],
            "failed_matching_substrings": sorted(search_stats["failed_substr_counts"].keys()),
        },
        "papers": {
            "rows": dedup_counts["n_raw"],
            "exact_unique_ids": dedup_counts["n_stage1"],
            "final_works": dedup_counts["n_stage3"],
        },
        "evidence": {
            "claim_verified": 0,
            "fulltext_opened": 0,
            "abstract_verified": n_abstract_verified,
            "discovered": n_discovered,
            "corrections": len(claim_rows_corr),
        },
        "unresolved": {
            "unverified_citations": {
                "count": len(unverified_citation_ids),
                "ids": unverified_citation_ids,
            },
            "screening_decisions": "RAW_EVENT_UNAVAILABLE",
            "search_results_universe": "RAW_EVENT_UNAVAILABLE",
        },
    }
    return flow


# --------------------------------------------------------------------------
# 9. README.md (file i)
# --------------------------------------------------------------------------

BUNDLE_STATUS_TOKEN = "ROUND1_SCOUT_COMPLETE"


def build_readme(search_stats, dedup_counts, n_papers, n_claim_base, n_claim_corr,
                  unverified_citation_ids, file_line_counts):
    lines = []
    lines.append("# %s — Survey v2 replay bundle" % RESPONSE_ID)
    lines.append("")
    lines.append("## What this is")
    lines.append("")
    lines.append(
        "This is a machine-regenerated **replay bundle** for Survey v2 "
        "(Stage-1A, workflow `wf_c6ed06f2`), built under the doctoral-review "
        "remediation P0 opened against the 2026-07-14 review of Survey v2. "
        "It exists to answer one question mechanically, not by assertion: "
        "*given the two artifacts the survey actually produced — the "
        "305-line search/fetch query log and the 113-row scout ledger — "
        "what can be reconstructed, and what honestly cannot?*"
    )
    lines.append("")
    lines.append(
        "Every file in this directory except `build_and_validate.py` itself "
        "is generated output. Nothing here was hand-edited after generation. "
        "The single generating script is committed alongside its output so "
        "any reviewer can rerun it and diff the result."
    )
    lines.append("")
    lines.append("Bundle status token for this round: **`%s`**." % BUNDLE_STATUS_TOKEN)
    lines.append("")
    lines.append("BUNDLE_STATUS_TOKEN: %s" % BUNDLE_STATUS_TOKEN)
    lines.append(
        "Per the replayability template §4 this permits forming a "
        "candidate map; it explicitly does **not** permit claiming "
        "saturated / unique / complete / decision-ready for Survey v2 as a "
        "whole — those claims require `LOCALLY_SATURATED_WITHIN_PROTOCOL` "
        "or `STAGE1C_DECISION_READY`, which this bundle does not establish."
    )
    lines.append("")
    lines.append("The formal point-by-point response letter to the review lives at")
    lines.append(
        "`wiki/2026-07-14-survey-v2-response-and-p0-remediation.md` "
        "(authored separately by the coordinator; not part of this bundle)."
    )
    lines.append("")
    lines.append("## Headline numbers (all machine-recomputed — see `flow_report.yaml`)")
    lines.append("")
    lines.append("| Quantity | Value |")
    lines.append("|---|---|")
    lines.append("| Search/fetch events logged (A) | %d (SEARCH=%d, FETCH=%d) |"
                  % (search_stats["total"], search_stats["search"], search_stats["fetch"]))
    lines.append("| Events classified FAILED | %d |" % search_stats["failed"])
    lines.append("| Events OUTCOME_UNVERIFIED_RAW_UNAVAILABLE | %d |" % search_stats["outcome_unverified"])
    lines.append("| Ledger paper-rows (B) | %d |" % dedup_counts["n_raw"])
    lines.append("| → after exact-id dedup (Stage 1) | %d |" % dedup_counts["n_stage1"])
    lines.append("| → after arXiv-id regex grouping (Stage 2) | %d |" % dedup_counts["n_stage2"])
    lines.append("| → after explicit alias clusters (Stage 3, final) | %d |" % dedup_counts["n_stage3"])
    lines.append("| Historical estimate in B (`_est`) | ~93 — **not reproducible**, see `dedup_report.json` |")
    lines.append("| claim_evidence rows | %d base + %d corrections = %d |"
                  % (n_claim_base, n_claim_corr, n_claim_base + n_claim_corr))
    lines.append("| UNVERIFIED-CITATION rows | %d (%s) |"
                  % (len(unverified_citation_ids), ", ".join(unverified_citation_ids)))
    lines.append("")
    lines.append("## FAILED-event classification method (search_events.jsonl `status`)")
    lines.append("")
    lines.append(
        "A `note` is classified `FAILED` only if it contains one of these "
        "substrings (word-boundary matched, case as shown except `denied` "
        "which is matched case-insensitively): `FAILED`, `BLOCKED`, "
        "`Blocked`, `NOT_RESOLVED`, `socket-failed`, `denied`. This is "
        "narrower than a bare case-insensitive `fail`/`block` search on "
        "purpose — lower-case `fail`/`block` inside running prose "
        "(e.g. row 116 'First attempt **failed** (socket closed); retried "
        "later successfully', or notes describing some *other* paper's "
        "name/finding, e.g. 'judge-BoN-**fail**') do not mark this event's "
        "own outcome as failed; only the deliberate ALL-CAPS/marker-style "
        "annotations the log author actually used for that purpose do. "
        "Every event that is not classified FAILED is honestly marked "
        "`OUTCOME_UNVERIFIED_RAW_UNAVAILABLE` — the log records what was "
        "learned, not a raw HTTP/tool status code, so \"not FAILED\" is not "
        "the same claim as \"succeeded\"."
    )
    lines.append("")
    lines.append("Matched-substring counts across the %d classified FAILED events:" % search_stats["failed"])
    lines.append("")
    for k in sorted(search_stats["failed_substr_counts"].keys()):
        lines.append("- `%s`: %d event(s)" % (k, search_stats["failed_substr_counts"][k]))
    lines.append("")
    lines.append("## What is honestly missing forever (`RAW_EVENT_UNAVAILABLE`)")
    lines.append("")
    lines.append(
        "The following are **not reconstructable** from A/B and are not "
        "guessed at anywhere in this bundle:"
    )
    lines.append("")
    lines.append("- Raw request/response bodies for all %d search/fetch events "
                  "(A records only the query, engine, date, result_cap and a "
                  "human-written note, never the raw payload)." % search_stats["total"])
    lines.append("- The search-results universe (ranked candidate lists actually "
                  "returned per query) — A logs the query, not the result set.")
    lines.append("- Any screening/include-exclude decision trail (B records a final "
                  "grade per row, not the reasoning steps that produced it).")
    lines.append("- Intra-day timestamps — A carries date-only granularity "
                  "(`%s` for every row); `timestamp_utc` is `null` throughout, "
                  "never fabricated." % GENERATION_DATE)
    lines.append("- Per-query agent identity — only the workflow-level "
                  "`agent_id` (`wf_c6ed06f2`) is known; which of possibly "
                  "several session agents ran any individual query is unrecorded.")
    lines.append("- A pre-registered search protocol (`protocol.yaml` in the "
                  "template's suggested layout) — none was frozen before "
                  "searching, so this bundle does not include one rather than "
                  "backfill a retrospective one and call it preregistered.")
    lines.append("- `search_results.jsonl` / `screening_decisions.jsonl` from the "
                  "template's suggested layout — both require raw data this "
                  "round never captured; omitted rather than faked.")
    lines.append("")
    lines.append("## Input provenance note (found during the build, recorded honestly)")
    lines.append("")
    lines.append(
        "The build task specified all three inputs as \"canonical at commit "
        "233dc7eb\". This is **verified true** for A "
        "(`wiki/survey/2026-07-14-search-query-log.jsonl`) and B "
        "(`wiki/survey/2026-07-14-scout-ledger-round2.json`) — their "
        "on-disk bytes are byte-identical to the git blob at 233dc7eb. It "
        "is **verified false** for the template spec "
        "(`wiki/2026-07-14-survey-response-replayability-template.md`): that "
        "file does not exist at commit 233dc7eb at all "
        "(`git show 233dc7eb:<path>` fails); it was introduced two commits "
        "later at `b41f9f85db359fa5b13cadbcb4024c130d43542e` and is "
        "unchanged through current HEAD. See `manifest.yaml` → `inputs` "
        "for the full detail. This is reported rather than silently "
        "assumed correct, consistent with this bundle's own no-fabrication rule."
    )
    lines.append("")
    lines.append("## How to rebuild")
    lines.append("")
    lines.append("From this directory:")
    lines.append("")
    lines.append("```")
    lines.append(GENERATED_BY_CMD)
    lines.append("```")
    lines.append("")
    lines.append(
        "The script is deterministic (no network, no wall-clock, stdlib "
        "only) and regenerates every other file in this directory byte-for-"
        "byte from the two canonical inputs plus the literal, clearly-"
        "labeled correction facts hardcoded near the top of the script. It "
        "exits 0 iff every check in `validation_report.txt` passes, "
        "non-zero otherwise."
    )
    lines.append("")
    lines.append("## Files in this bundle")
    lines.append("")
    lines.append("| File | Lines | Purpose |")
    lines.append("|---|---|---|")
    lines.append("| `build_and_validate.py` | %d | the one generator/validator script (this is the only file not itself generated) |"
                  % file_line_counts.get("build_and_validate.py", 0))
    lines.append("| `search_events.jsonl` | %d | one row per query-log event in A, honestly graded |" % file_line_counts.get("search_events.jsonl", 0))
    lines.append("| `papers.jsonl` | %d | %d deduplicated canonical works, full merge evidence trail |" % (file_line_counts.get("papers.jsonl", 0), n_papers))
    lines.append("| `claim_evidence.jsonl` | %d | %d base rows (1 per B row) + %d correction rows |" % (file_line_counts.get("claim_evidence.jsonl", 0), n_claim_base, n_claim_corr))
    lines.append("| `round2_new_targets.jsonl` | %d | 8 round-2 candidates surfaced by five-lens verification, not yet graded |" % file_line_counts.get("round2_new_targets.jsonl", 0))
    lines.append("| `dedup_report.json` | — (JSON, not JSONL) | full 3-stage dedup pipeline trace + historical-estimate reconciliation attempt |")
    lines.append("| `flow_report.yaml` | — | machine-recomputed flow counts only |")
    lines.append("| `manifest.yaml` | — | bytes/lines/sha256 for every generated file + input provenance |")
    lines.append("| `validation_report.txt` | — | the actual check run, PASS/FAIL, exit code |")
    lines.append("| `README.md` | — | this file |")
    lines.append("")
    lines.append(
        "`survey_response.md` is intentionally **not** in this bundle; per "
        "the task it is added after the build by the coordinator and lives "
        "at `wiki/2026-07-14-survey-v2-response-and-p0-remediation.md`."
    )
    lines.append("")
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------
# 10. Validation
# --------------------------------------------------------------------------

_BANNED_EMPTY_RE = re.compile(r"(?<![A-Za-z0-9_])EMPTY(?![A-Za-z0-9_])")
_BANNED_NDM_RE = re.compile(r"NO_DIRECT_MATCH(?!_WITHIN_LOGGED_SCOPE)")


def run_validation(ctx):
    checks = []

    def check(name, ok, detail=""):
        checks.append((name, ok, detail))

    # V1: all JSONL / JSON files parse
    jsonl_files = ["search_events.jsonl", "papers.jsonl", "claim_evidence.jsonl", "round2_new_targets.jsonl"]
    all_parse_ok = True
    parse_detail = []
    for fn in jsonl_files:
        p = BUNDLE_DIR / fn
        try:
            with open(p, "rb") as f:
                text = f.read().decode("utf-8")
            n = 0
            for line in text.split("\n"):
                if line.strip() == "":
                    continue
                json.loads(line)
                n += 1
            parse_detail.append("%s: %d lines OK" % (fn, n))
        except Exception as e:
            all_parse_ok = False
            parse_detail.append("%s: PARSE ERROR %r" % (fn, e))
    try:
        json.loads((BUNDLE_DIR / "dedup_report.json").read_bytes().decode("utf-8"))
        parse_detail.append("dedup_report.json: OK")
    except Exception as e:
        all_parse_ok = False
        parse_detail.append("dedup_report.json: PARSE ERROR %r" % (e,))
    check("V1 all JSON/JSONL bundle files parse", all_parse_ok, "; ".join(parse_detail))

    # V2: event_id uniqueness + count
    se = ctx["search_events"]
    ids = [r["event_id"] for r in se]
    ok = len(ids) == len(set(ids)) and len(ids) == 305
    check("V2 search_events event_id unique and count==305", ok,
          "n=%d unique=%d" % (len(ids), len(set(ids))))

    # V3: paper_id uniqueness + count
    papers = ctx["papers"]
    pids = [p["paper_id"] for p in papers]
    ok = len(pids) == len(set(pids)) and len(pids) == ctx["dedup_counts"]["n_stage3"]
    check("V3 papers.jsonl paper_id unique and count matches Stage-3 final", ok,
          "n=%d unique=%d expected=%d" % (len(pids), len(set(pids)), ctx["dedup_counts"]["n_stage3"]))

    # V4: claim_id uniqueness + count
    claim_all = ctx["claim_base"] + ctx["claim_corr"]
    cids = [r["claim_id"] for r in claim_all]
    expected_n = 113 + len(ctx["claim_corr"])
    ok = len(cids) == len(set(cids)) and len(cids) == expected_n
    check("V4 claim_evidence.jsonl claim_id unique and count==113+corrections", ok,
          "n=%d unique=%d expected=%d" % (len(cids), len(set(cids)), expected_n))

    # V5: FK claim -> paper resolves
    paper_id_set = set(pids)
    fk_bad = []
    for r in claim_all:
        targets = r.get("paper_ids") if "paper_ids" in r else [r.get("paper_id")]
        for t in targets:
            if t not in paper_id_set:
                fk_bad.append((r["claim_id"], t))
    check("V5 every claim_evidence paper_id/paper_ids FK resolves into papers.jsonl",
          len(fk_bad) == 0, "unresolved=%r" % (fk_bad,))

    # V6: recounts match flow_report.yaml (re-parsed from disk)
    flow_on_disk = yaml_load((BUNDLE_DIR / "flow_report.yaml").read_bytes().decode("utf-8"))
    recompute_search = sum(1 for r in se if r["operation"] == "SEARCH")
    recompute_fetch = sum(1 for r in se if r["operation"] == "FETCH")
    recompute_failed = sum(1 for r in se if r["status"] == "FAILED")
    ok6a = (flow_on_disk["events"]["search"] == recompute_search
            and flow_on_disk["events"]["fetch"] == recompute_fetch
            and flow_on_disk["events"]["failed"] == recompute_failed)
    recompute_rows = 113
    recompute_final = len(papers)
    ok6b = (flow_on_disk["papers"]["rows"] == recompute_rows
            and flow_on_disk["papers"]["final_works"] == recompute_final)
    recompute_av = sum(1 for r in ctx["claim_base"] if r["effective_grade"] == "ABSTRACT_VERIFIED")
    recompute_disc = sum(1 for r in ctx["claim_base"] if r["effective_grade"] == "DISCOVERED")
    ok6c = (flow_on_disk["evidence"]["abstract_verified"] == recompute_av
            and flow_on_disk["evidence"]["discovered"] == recompute_disc
            and flow_on_disk["evidence"]["corrections"] == len(ctx["claim_corr"]))
    check("V6 recounts (search/fetch/failed, papers rows/final, evidence "
          "abstract_verified/discovered/corrections) match flow_report.yaml on disk",
          ok6a and ok6b and ok6c,
          "events_ok=%s papers_ok=%s evidence_ok=%s" % (ok6a, ok6b, ok6c))

    # V7: no effective grade above ABSTRACT_VERIFIED
    allowed = {"ABSTRACT_VERIFIED", "DISCOVERED"}
    bad = [p["paper_id"] for p in papers if p["grade_effective"] not in allowed]
    bad += [r["claim_id"] for r in ctx["claim_base"] if r["effective_grade"] not in allowed]
    check("V7 no effective grade above ABSTRACT_VERIFIED anywhere", len(bad) == 0, "offenders=%r" % (bad,))

    # V8: banned-token scan on status-like fields only
    status_like_values = []
    for r in se:
        status_like_values.append(("search_events.%s.status" % r["event_id"], r["status"]))
    for p in papers:
        status_like_values.append(("papers.%s.grade_effective" % p["paper_id"], p["grade_effective"]))
    for r in claim_all:
        status_like_values.append(("claim_evidence.%s.effective_grade" % r["claim_id"], r.get("effective_grade", "")))
        status_like_values.append(("claim_evidence.%s.original_grade" % r["claim_id"], r.get("original_grade", "")))
    for r in ctx["round2_targets"]:
        status_like_values.append(("round2_new_targets.%s.required_action" % r["arxiv_or_venue_id"], r["required_action"]))
    status_like_values.append(("README.bundle_status_token", BUNDLE_STATUS_TOKEN))
    banned_hits = []
    for field, val in status_like_values:
        if val is None:
            continue
        if _BANNED_EMPTY_RE.search(val):
            banned_hits.append((field, "EMPTY"))
        if _BANNED_NDM_RE.search(val):
            banned_hits.append((field, "NO_DIRECT_MATCH(_not_scoped)"))
    check("V8 banned-token scan (standalone EMPTY; unscoped NO_DIRECT_MATCH) on status-like fields",
          len(banned_hits) == 0, "hits=%r" % (banned_hits,))

    # V9: final status token check. README.md carries a dedicated
    # machine-parseable anchor line "BUNDLE_STATUS_TOKEN: <token>" (distinct
    # from the surrounding prose, which may legitimately *mention* stronger
    # status tokens while explaining that they are NOT being claimed). The
    # check is: exactly one such anchor line exists, and its value is
    # exactly ROUND1_SCOUT_COMPLETE.
    readme_text = (BUNDLE_DIR / "README.md").read_bytes().decode("utf-8")
    anchor_re = re.compile(r"^BUNDLE_STATUS_TOKEN: (.+)$", re.MULTILINE)
    anchors = anchor_re.findall(readme_text)
    ok9 = len(anchors) == 1 and anchors[0] == BUNDLE_STATUS_TOKEN
    check("V9 final status token check (README anchor line BUNDLE_STATUS_TOKEN "
          "is exactly ROUND1_SCOUT_COMPLETE, declared exactly once)", ok9,
          "anchors_found=%r" % (anchors,))

    # V10: manifest.yaml round-trips and matches on-disk files
    manifest_on_disk = yaml_load((BUNDLE_DIR / "manifest.yaml").read_bytes().decode("utf-8"))
    mismatches = []
    for entry in manifest_on_disk.get("files", []):
        fp = BUNDLE_DIR / entry["name"]
        if not fp.exists():
            mismatches.append((entry["name"], "MISSING"))
            continue
        stats = file_stats(fp)
        if (stats["bytes"] != entry["bytes"] or stats["lines"] != entry["lines"]
                or stats["sha256"] != entry["sha256"]):
            mismatches.append((entry["name"], stats, entry))
    check("V10 manifest.yaml round-trips (mini-YAML loader) and every listed "
          "file's bytes/lines/sha256 match on-disk state", len(mismatches) == 0,
          "mismatches=%r" % (mismatches,))

    # V11: flow_report.yaml round-trips and structurally matches source dict
    ok11 = flow_on_disk == ctx["flow_report_dict"]
    check("V11 flow_report.yaml round-trips (mini-YAML loader) and equals the "
          "in-memory dict it was generated from", ok11, "")

    # V12: UTF-8 / no BOM / LF check on every generated text file
    text_files = ["search_events.jsonl", "papers.jsonl", "claim_evidence.jsonl",
                  "round2_new_targets.jsonl", "dedup_report.json", "flow_report.yaml",
                  "manifest.yaml", "README.md"]
    bad_encoding = []
    for fn in text_files:
        raw = (BUNDLE_DIR / fn).read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            bad_encoding.append((fn, "BOM present"))
            continue
        if b"\r" in raw:
            bad_encoding.append((fn, "CR byte present (not pure LF)"))
            continue
        try:
            raw.decode("utf-8")
        except UnicodeDecodeError as e:
            bad_encoding.append((fn, "not valid UTF-8: %r" % (e,)))
    check("V12 every generated text file is UTF-8, no BOM, LF-only", len(bad_encoding) == 0,
          "offenders=%r" % (bad_encoding,))

    return checks


def write_validation_report(checks, ctx):
    lines = []
    lines.append("VALIDATION REPORT")
    lines.append("Bundle: %s" % RESPONSE_ID)
    lines.append("Command: %s" % GENERATED_BY_CMD)
    lines.append("Generation date: %s" % GENERATION_DATE)
    lines.append("")
    n_pass = sum(1 for _, ok, _ in checks if ok)
    n_fail = sum(1 for _, ok, _ in checks if not ok)
    for name, ok, detail in checks:
        lines.append("[%s] %s" % ("PASS" if ok else "FAIL", name))
        if detail:
            lines.append("    detail: %s" % detail)
    lines.append("")
    lines.append("SUMMARY: %d/%d checks passed, %d failed" % (n_pass, n_pass + n_fail, n_fail))
    overall = "PASS" if n_fail == 0 else "FAIL"
    lines.append("OVERALL: %s" % overall)
    lines.append("")
    lines.append("BUNDLE_STATUS_TOKEN: %s" % BUNDLE_STATUS_TOKEN)
    lines.append("")
    lines.append("Exit code: %d" % (0 if n_fail == 0 else 1))
    return "\n".join(lines) + "\n", (0 if n_fail == 0 else 1)


# --------------------------------------------------------------------------
# 11. Manifest (file g) -- written after data files + README, before
#     validation_report.txt (so validation can genuinely re-check it)
# --------------------------------------------------------------------------


def build_manifest(generated_file_names):
    files_entries = []
    for fn in generated_file_names:
        stats = file_stats(BUNDLE_DIR / fn)
        files_entries.append({
            "name": fn,
            "bytes": stats["bytes"],
            "lines": stats["lines"],
            "sha256": stats["sha256"],
            "generated_by": GENERATED_BY_CMD,
        })

    inputs_entries = []
    for rel, meta in INPUT_PROVENANCE.items():
        p = REPO_ROOT / rel
        stats = file_stats(p)
        inputs_entries.append({
            "path": rel,
            "role": meta["role"],
            "bytes": stats["bytes"],
            "lines": stats["lines"],
            "sha256": stats["sha256"],
            "claimed_canonical_commit": meta["claimed_canonical_commit"],
            "claim_verified": meta["verified"],
            "note": meta["note"],
        })

    manifest = {
        "bundle_id": RESPONSE_ID,
        "generation_date": GENERATION_DATE,
        "generated_by": GENERATED_BY_CMD,
        "inputs": inputs_entries,
        "files": files_entries,
        "known_missing_raw_events": [
            "raw search/fetch response bodies x305 (no response payload was ever captured; A logs query/engine/date/result_cap/note only)",
            "search results universe (ranked candidate lists actually returned per query)",
            "screening decision trail (include/exclude reasoning per candidate result)",
            "intra-day timestamps (A has date-only granularity; timestamp_utc is null throughout)",
            "per-query agent identity (only the workflow-level agent_id wf_c6ed06f2 is known)",
        ],
        "survey_response_md": {
            "status": "added-after-build",
            "path": "wiki/2026-07-14-survey-v2-response-and-p0-remediation.md",
            "note": ("the formal response letter is authored separately by the "
                     "coordinator after this bundle validates; intentionally "
                     "not part of this manifest or this directory"),
        },
        "self_reference_note": ("manifest.yaml does not list its own bytes/lines/"
                                 "sha256 (self-reference paradox: its own hash "
                                 "would change the moment it is written); compute "
                                 "independently after generation, e.g. "
                                 "`sha256sum manifest.yaml`. validation_report.txt "
                                 "is generated after manifest.yaml for the same "
                                 "reason and is likewise excluded from the files list."),
    }
    return manifest


# --------------------------------------------------------------------------
# 12. Main
# --------------------------------------------------------------------------


def main():
    a_events = load_input_a()
    b_data, b_rows = load_input_b()
    assert len(a_events) == 305, "expected 305 events in A, got %d" % len(a_events)
    assert len(b_rows) == 113, "expected 113 rows in B, got %d" % len(b_rows)

    # -- self-test the mini-YAML round trip before relying on it anywhere --
    _self_test_obj = {
        "a": "x:y \"z\"",
        "b": 3,
        "c": True,
        "d": None,
        "e": {"f": ["g", "h"], "i": []},
        "j": [{"k": 1, "l": "m"}, {"k": 2, "l": "n"}],
    }
    _rt = yaml_load(yaml_dump(_self_test_obj))
    assert _rt == _self_test_obj, "mini-YAML self-test round-trip FAILED: %r != %r" % (_rt, _self_test_obj)

    # -- a) search_events.jsonl --
    search_events, search_stats = build_search_events(a_events)
    write_jsonl(BUNDLE_DIR / "search_events.jsonl", search_events)

    # -- b) papers.jsonl + e) dedup_report.json --
    papers, paper_id_by_row, dedup_report, dedup_counts = build_papers_and_dedup(b_rows)
    write_jsonl(BUNDLE_DIR / "papers.jsonl", papers)
    write_json(BUNDLE_DIR / "dedup_report.json", dedup_report)

    # -- c) claim_evidence.jsonl --
    claim_base, n_base = build_claim_evidence(b_rows, paper_id_by_row)
    claim_corr, _ = build_corrections(b_rows, papers, n_base + 1)
    write_jsonl(BUNDLE_DIR / "claim_evidence.jsonl", claim_base + claim_corr)

    # -- d) round2_new_targets.jsonl --
    round2_targets = build_round2_new_targets()
    write_jsonl(BUNDLE_DIR / "round2_new_targets.jsonl", round2_targets)

    # -- unverified citations (for flow_report + README) --
    unverified_citation_ids = sorted(
        ARXIV_RE.search(r["id"]).group(1)
        for r in b_rows if r["grade"] == "UNVERIFIED-CITATION"
    )

    # -- f) flow_report.yaml --
    flow_report_dict = build_flow_report(search_stats, dedup_counts, claim_base, claim_corr, unverified_citation_ids)
    write_text_utf8_lf(BUNDLE_DIR / "flow_report.yaml", yaml_dump(flow_report_dict))

    # -- i) README.md --
    # (line counts filled in after all data files are on disk; README's own
    # line count obviously can't be included in itself, that's fine.)
    prelim_line_counts = {}
    for fn in ["search_events.jsonl", "papers.jsonl", "claim_evidence.jsonl", "round2_new_targets.jsonl"]:
        prelim_line_counts[fn] = file_stats(BUNDLE_DIR / fn)["lines"]
    prelim_line_counts["build_and_validate.py"] = file_stats(BUNDLE_DIR / "build_and_validate.py")["lines"]
    readme_text = build_readme(search_stats, dedup_counts, len(papers), len(claim_base), len(claim_corr),
                                unverified_citation_ids, prelim_line_counts)
    write_text_utf8_lf(BUNDLE_DIR / "README.md", readme_text)

    # -- g) manifest.yaml (covers build_and_validate.py + all data files + README.md) --
    generated_file_names = [
        "build_and_validate.py",
        "search_events.jsonl",
        "papers.jsonl",
        "claim_evidence.jsonl",
        "round2_new_targets.jsonl",
        "dedup_report.json",
        "flow_report.yaml",
        "README.md",
    ]
    manifest_dict = build_manifest(generated_file_names)
    write_text_utf8_lf(BUNDLE_DIR / "manifest.yaml", yaml_dump(manifest_dict))

    # -- h) validation_report.txt (written last) --
    ctx = {
        "search_events": search_events,
        "papers": papers,
        "claim_base": claim_base,
        "claim_corr": claim_corr,
        "dedup_counts": dedup_counts,
        "round2_targets": round2_targets,
        "flow_report_dict": flow_report_dict,
    }
    checks = run_validation(ctx)
    report_text, exit_code = write_validation_report(checks, ctx)
    write_text_utf8_lf(BUNDLE_DIR / "validation_report.txt", report_text)

    # -- console summary --
    for name, ok, detail in checks:
        print("[%s] %s" % ("PASS" if ok else "FAIL", name))
    print("")
    print("search events: %d (search=%d fetch=%d failed=%d)"
          % (search_stats["total"], search_stats["search"], search_stats["fetch"], search_stats["failed"]))
    print("papers: raw=%d stage1=%d stage2=%d final=%d"
          % (dedup_counts["n_raw"], dedup_counts["n_stage1"], dedup_counts["n_stage2"], dedup_counts["n_stage3"]))
    print("claim_evidence: base=%d corrections=%d total=%d" % (len(claim_base), len(claim_corr), len(claim_base) + len(claim_corr)))
    print("EXIT CODE: %d" % exit_code)

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
