#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""REC-0 / REC-2 / claim-lineage validator (correction #4A / P0-R3).

Executable enforcement of the amendment-4 §2 record contract (previously only promised):
  V1  REC-0 canonical_id unique
  V2  REC-0 source_hits non-empty, each source parseable, hit_ref non-empty
  V3  REC-0 enums: screening_stage / decision (drift = FAIL)
  V4  INCLUDED  => extraction.rec2_backref resolves to an existing REC-2 row; reason_code null
  V5  EXCLUDED/UNOBTAINABLE => reason_code in enum AND reason_text non-empty;
      DUPLICATE => reason_code = DUPLICATE_OF:<id>
  V6  coding_depth in {D0,D1,D2}; INCLUDED => {D1,D2}; REC-0.coding_depth == REC-2.coding_depth
  V7  REC-2 id unique; rec0_backref resolves to an INCLUDED REC-0 row
  V8  D2 trigger: topic_relevance=core OR initial_tag contains DIRECT_THREAT OR referenced
      by any claim  => coding_depth must be D2 (owner-accepted reviewer expansion: core)
  V9  D2 contract: required blocks present as objects (matrix/tf_audit/source_axes/
      extraction/evidence_axes); optional blocks NA only as type-stable object;
      study_quality all 7 dims (verdict enum + reason; locator required unless NA) + coder;
      claim_locators non-empty with claim+locator filled
  V10 D1 contract: minimal required set present; collapsed blocks ONLY as
      {"status":"NA","reason":"<non-empty>"} — bare "NA:<...>" strings and empty strings FAIL
  V11 claims: every bearing claim's rec2_backref resolves to a REC-2 row with depth D2
  V12 flow_report numbers recomputed from REC-0; any hand-tallied mismatch FAILs
  V13 DIRECT_THREAT rows: dual coding block (extractor_A != extractor_B, rec5_ref,
      adjudicator non-null when disagreements > 0)

CLI:
  python sf_record_validator.py --package <pkg.json>
  python sf_record_validator.py --rec0 a.jsonl --rec2 b.jsonl --claims c.jsonl --flow f.json
Exit 0 iff zero violations; JSON report on stdout.
"""
import json
import re
import sys

REC0_DECISIONS = ("INCLUDED", "EXCLUDED", "DUPLICATE", "UNOBTAINABLE")
REC0_STAGES = ("TITLE", "ABSTRACT", "FULLTEXT")
REASON_CODES = ("NOT_RELEVANT", "WRONG_OBJECT", "REMOVED_PAYWALLED_UNOBTAINABLE",
                "REMOVED_UNOBTAINABLE", "INFO_BOUNDARY_FAIL")
DEPTHS = ("D0", "D1", "D2")
SOURCE_RE = re.compile(r"^(query:SF-|route:SF-T1R-|citation_graph:.+|seed:.+)")
SQ_DIMS = ("data_boundary", "control_fairness", "uncertainty_reporting",
           "ablation_attribution", "reproducibility", "artifact_availability",
           "claim_evidence_match")
SQ_VERDICTS = ("PASS", "PARTIAL", "FAIL", "UNCLEAR", "NA")
D2_REQUIRED_BLOCKS = ("matrix", "tf_audit", "source_axes", "extraction", "evidence_axes")
D2_NA_OK_BLOCKS = ("omni_axes", "rl_identity", "resource_axes", "method_occupation", "proximity")
D1_REQUIRED = ("id", "name", "version_pin", "topic_relevance", "proximity",
               "publication_status", "venue_tier", "dfs_trigger")


def is_na_object(v):
    return isinstance(v, dict) and v.get("status") == "NA" and bool(str(v.get("reason", "")).strip())


def is_block_object(v):
    return isinstance(v, dict) and v.get("status") != "NA"


def validate(rec0_rows, rec2_rows, claims, flow_report):
    v = []

    def bad(rule, where, msg):
        v.append({"rule": rule, "where": where, "violation": msg})

    # ---- REC-0 ----
    seen_c = {}
    rec2_by_id = {}
    for i, r in enumerate(rec2_rows):
        rid = r.get("id")
        if rid in rec2_by_id:
            bad("V7", f"rec2[{i}]", f"duplicate REC-2 id: {rid}")
        else:
            rec2_by_id[rid] = r

    for i, r in enumerate(rec0_rows):
        w = f"rec0[{i}]:{r.get('canonical_id')}"
        cid = r.get("canonical_id")
        if not cid or not str(cid).strip():
            bad("V1", w, "canonical_id missing/empty")
        elif cid in seen_c:
            bad("V1", w, f"duplicate canonical_id (first at rec0[{seen_c[cid]}])")
        else:
            seen_c[cid] = i
        hits = r.get("source_hits")
        if not isinstance(hits, list) or not hits:
            bad("V2", w, "source_hits missing/empty")
        else:
            for j, h in enumerate(hits):
                if not SOURCE_RE.match(str(h.get("source", ""))):
                    bad("V2", w, f"source_hits[{j}].source unparseable: {h.get('source')!r}")
                if not str(h.get("hit_ref", "")).strip():
                    bad("V2", w, f"source_hits[{j}].hit_ref empty")
        if r.get("screening_stage") not in REC0_STAGES:
            bad("V3", w, f"screening_stage enum drift: {r.get('screening_stage')!r}")
        dec = r.get("decision")
        if dec not in REC0_DECISIONS:
            bad("V3", w, f"decision enum drift: {dec!r}")
        rc = r.get("reason_code")
        if dec == "INCLUDED":
            if rc is not None:
                bad("V4", w, f"INCLUDED must carry reason_code null (got {rc!r}) — "
                             "机器强制,替代模板歧义")
            backref = (r.get("extraction") or {}).get("rec2_backref")
            if not backref or not str(backref).strip():
                bad("V4", w, "INCLUDED without extraction.rec2_backref")
            elif backref not in rec2_by_id:
                bad("V4", w, f"rec2_backref dangling: {backref!r}")
            elif rec2_by_id[backref].get("coding_depth") != r.get("coding_depth"):
                bad("V6", w, "coding_depth mismatch between REC-0 and REC-2 row")
        elif dec in ("EXCLUDED", "UNOBTAINABLE"):
            ok_code = rc in REASON_CODES or (isinstance(rc, str) and rc.startswith("OTHER:"))
            if not ok_code:
                bad("V5", w, f"reason_code missing/not in enum: {rc!r}")
            if not str(r.get("reason_text", "") or "").strip():
                bad("V5", w, "reason_text empty for EXCLUDED/UNOBTAINABLE")
        elif dec == "DUPLICATE":
            if not (isinstance(rc, str) and rc.startswith("DUPLICATE_OF:")):
                bad("V5", w, f"DUPLICATE requires reason_code DUPLICATE_OF:<id>, got {rc!r}")
        depth = r.get("coding_depth")
        if depth not in DEPTHS:
            bad("V6", w, f"coding_depth enum drift: {depth!r}")
        elif dec == "INCLUDED" and depth == "D0":
            bad("V6", w, "INCLUDED row cannot stay at D0")
        if not str(r.get("screener", "") or "").strip():
            bad("V10", w, "screener empty string — 空字符串伪装完成")

    # ---- REC-2 ----
    rec0_included = {r.get("canonical_id"): r for r in rec0_rows if r.get("decision") == "INCLUDED"}
    claim_refs = {c.get("rec2_backref") for c in claims}
    for i, r in enumerate(rec2_rows):
        w = f"rec2[{i}]:{r.get('id')}"
        if not str(r.get("rec0_backref", "") or "").strip():
            bad("V7", w, "rec0_backref missing")
        elif r["rec0_backref"] not in rec0_included:
            bad("V7", w, f"rec0_backref does not resolve to an INCLUDED REC-0 row: "
                         f"{r['rec0_backref']!r}")
        depth = r.get("coding_depth")
        tags = r.get("initial_tag") or []
        is_threat = "DIRECT_THREAT" in (tags if isinstance(tags, list) else [tags])
        trigger = (r.get("topic_relevance") == "core" or is_threat or r.get("id") in claim_refs)
        if trigger and depth != "D2":
            why = ("topic_relevance=core" if r.get("topic_relevance") == "core"
                   else "DIRECT_THREAT" if is_threat else "referenced by bearing claim")
            bad("V8", w, f"D2 trigger unmet ({why}) but coding_depth={depth!r}")
        if depth == "D2":
            for b in D2_REQUIRED_BLOCKS:
                if not is_block_object(r.get(b)):
                    bad("V9", w, f"D2 required block missing/collapsed: {b}")
            for b in D2_NA_OK_BLOCKS:
                val = r.get(b)
                if not (is_block_object(val) or is_na_object(val)):
                    bad("V9", w, f"D2 block {b} must be object or type-stable NA object")
            sq = ((r.get("evidence_axes") or {}).get("study_quality")) or {}
            for d in SQ_DIMS:
                dim = sq.get(d)
                if not isinstance(dim, dict):
                    bad("V9", w, f"study_quality dim missing: {d}")
                    continue
                if dim.get("verdict") not in SQ_VERDICTS:
                    bad("V9", w, f"study_quality.{d}.verdict enum drift: {dim.get('verdict')!r}")
                if not str(dim.get("reason", "") or "").strip():
                    bad("V9", w, f"study_quality.{d}.reason empty")
                if dim.get("verdict") != "NA" and not str(dim.get("locator", "") or "").strip():
                    bad("V9", w, f"study_quality.{d}.locator empty for non-NA verdict")
            if not str(sq.get("coder", "") or "").strip():
                bad("V9", w, "study_quality.coder empty")
            locs = r.get("claim_locators")
            if not isinstance(locs, list) or not locs or not all(
                    str(x.get("claim", "")).strip() and str(x.get("locator", "")).strip()
                    for x in locs):
                bad("V9", w, "claim_locators missing/empty at D2")
        elif depth == "D1":
            for f_ in D1_REQUIRED:
                val = r.get(f_)
                if val is None or (isinstance(val, str) and not val.strip()):
                    bad("V10", w, f"D1 required field missing/empty: {f_}")
            for b in ("matrix", "tf_audit", "source_axes", "omni_axes", "rl_identity",
                      "resource_axes", "method_occupation", "extraction", "evidence_axes"):
                val = r.get(b)
                if val is None:
                    continue
                if isinstance(val, str):
                    bad("V10", w, f"block {b} collapsed as bare string {val!r} — "
                                  "must be type-stable {{\"status\":\"NA\",\"reason\":...}}")
                elif not (is_block_object(val) or is_na_object(val)):
                    bad("V10", w, f"block {b} NA object missing non-empty reason")
        if is_threat:
            dc = r.get("threat_dual_coding")
            if not isinstance(dc, dict):
                bad("V13", w, "DIRECT_THREAT without threat_dual_coding block")
            else:
                if not dc.get("extractor_A") or not dc.get("extractor_B") \
                        or dc.get("extractor_A") == dc.get("extractor_B"):
                    bad("V13", w, "dual coding requires two distinct extractors")
                if not str(dc.get("rec5_ref", "") or "").strip():
                    bad("V13", w, "dual coding missing rec5_ref")
                if int(dc.get("disagreements", 0)) > 0 and not dc.get("adjudicator"):
                    bad("V13", w, "disagreements > 0 but adjudicator null")

    # ---- claims ----
    for i, c in enumerate(claims):
        w = f"claims[{i}]:{c.get('claim_id')}"
        ref = c.get("rec2_backref")
        if not ref or ref not in rec2_by_id:
            bad("V11", w, f"bearing claim backref dangling: {ref!r}")
        elif rec2_by_id[ref].get("coding_depth") != "D2":
            bad("V11", w, f"bearing claim must backref a D2 row "
                          f"(got {rec2_by_id[ref].get('coding_depth')!r})")
        if not str(c.get("claim_text", "") or "").strip():
            bad("V11", w, "claim_text empty")

    # ---- flow report derived from REC-0, never hand-tallied ----
    derived = {"n_hits": len(rec0_rows)}
    for dec in REC0_DECISIONS:
        derived[f"n_{dec.lower()}"] = sum(1 for r in rec0_rows if r.get("decision") == dec)
    if flow_report is None:
        bad("V12", "flow_report", "flow_report missing (must be present and derived)")
    else:
        for k, want in derived.items():
            got = flow_report.get(k)
            if got != want:
                bad("V12", "flow_report", f"{k} hand-tallied {got!r} != derived {want}")

    v.sort(key=lambda x: (x["rule"], x["where"], x["violation"]))
    return v, derived


def _load_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def main(argv):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = dict(zip(argv[1::2], argv[2::2]))
    if "--package" in args:
        with open(args["--package"], "r", encoding="utf-8") as f:
            pkg = json.load(f)
        rec0, rec2 = pkg.get("rec0", []), pkg.get("rec2", [])
        claims, flow = pkg.get("claims", []), pkg.get("flow_report")
    else:
        rec0 = _load_jsonl(args["--rec0"]) if "--rec0" in args else []
        rec2 = _load_jsonl(args["--rec2"]) if "--rec2" in args else []
        claims = _load_jsonl(args["--claims"]) if "--claims" in args else []
        flow = None
        if "--flow" in args:
            with open(args["--flow"], "r", encoding="utf-8") as f:
                flow = json.load(f)
    violations, derived = validate(rec0, rec2, claims, flow)
    report = {"n_rec0": len(rec0), "n_rec2": len(rec2), "n_claims": len(claims),
              "derived_flow": derived, "n_violations": len(violations),
              "violations": violations,
              "verdict": "PASS" if not violations else "FAIL"}
    print(json.dumps(report, ensure_ascii=False, indent=1))
    return 0 if not violations else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
