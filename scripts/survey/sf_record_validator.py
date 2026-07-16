#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""REC-0 / REC-2 / claim-lineage validator, v2 (correction #4B / P0-2).

Executable enforcement of the amendment-4 §2 record contract. v2 supersedes the
C4A validator whose oracle was weaker than the prose contract (doctoral re-review
#4A MAJOR-2): bidirectional lineage, seed-manifest threat join, and inner block
schemas are now machine-checked, and malformed types yield structured violations
instead of crashes.

  V1  REC-0 canonical_id unique, non-empty
  V2  REC-0 source_hits non-empty, each source parseable, hit_ref non-empty
  V3  REC-0 enums: screening_stage / decision (drift = FAIL)
  V4  INCLUDED => extraction.rec2_backref resolves to an existing REC-2 row,
      reason_code null, AND the lineage is bidirectional one-to-one:
      REC2[backref].rec0_backref == REC0.canonical_id (cross-wire = FAIL);
      two REC-0 rows sharing one REC-2 (many-to-one) = FAIL
  V5  EXCLUDED/UNOBTAINABLE => reason_code in enum or OTHER:<non-empty>;
      reason_text non-empty; DUPLICATE => DUPLICATE_OF:<id> with non-empty id
      that resolves to a known REC-0 canonical_id
  V6  coding_depth in {D0,D1,D2}; INCLUDED => {D1,D2}; REC-0 == REC-2 depth
  V7  REC-2 id unique; rec0_backref resolves to an INCLUDED REC-0 row;
      REC-2 rows referenced by no INCLUDED REC-0 (orphans) = FAIL
  V8  D2 trigger: topic_relevance=core OR DIRECT_THREAT (REC-2 tag OR frozen
      seed-manifest tag) OR referenced by any claim => coding_depth D2
  V9  D2 contract: required blocks (matrix/tf_audit/source_axes/extraction/
      evidence_axes/proximity) present with FULL inner schema (enums + non-empty,
      see BLOCK_SCHEMAS — an empty {} is NOT a block); optional blocks
      (omni_axes/rl_identity/resource_axes/method_occupation) either full valid
      block or type-stable NA object; study_quality all 7 dims + coder;
      claim_locators non-empty; venue_tier/topic_relevance/most_threatened_rq/
      dfs_trigger enum-checked
  V10 D1 contract: minimal required set; proximity full; evidence_axes carries
      verification_depth + publication_status; partially-filled blocks must
      satisfy the inner schema on the keys they do carry; bare-string collapse
      = FAIL
  V11 claims: every bearing claim's rec2_backref resolves to a REC-2 row with
      depth D2; claim_text non-empty
  V12 flow_report numbers recomputed from REC-0; hand-tallied mismatch = FAIL
  V13 DIRECT_THREAT rows: dual coding block (distinct extractors, rec5_ref,
      adjudicator when disagreements > 0); malformed disagreements type is a
      structured violation, never a crash
  V14 frozen seed manifest MUST be bound (fail-closed); a seed row's
      DIRECT_THREAT initial_tag must survive REC-2 transcription
  V15 publication_status has exactly one canonical location
      (evidence_axes.publication_status); a top-level copy = FAIL

CLI:
  python sf_record_validator.py --package <pkg.json> [--seeds <manifest.jsonl>]
  python sf_record_validator.py --rec0 a.jsonl --rec2 b.jsonl --claims c.jsonl \
      --flow f.json --seeds seeds.jsonl
Package mode also accepts inline "seed_manifest": [{"id":..,"initial_tag":[..]}].
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
VERIFICATION_DEPTHS = ("DISCOVERED", "ABSTRACT_VERIFIED", "FULLTEXT_OPENED",
                       "CLAIM_VERIFIED", "REPRODUCED")
PUBLICATION_STATUSES = ("preprint", "peer-reviewed", "withdrawn", "retracted")
VENUE_TIERS = ("T1", "T2", "T3")
TOPIC_RELEVANCE = ("core", "element")
RQ_SET = ("RQ-SYS", "RQ-CTRL", "RQ-OMNI", "RQ-SAFE", "RQ-MEASURE")
DFS_PREFIXES = ("T-a", "T-b", "T-c", "T-d")
YN = ("Y", "N")
ISC = ("TASK_NATIVE", "PRETRAINED_READOUT", "DETERMINISTIC_COMPUTE",
       "ENDOGENOUS_ENV_FEEDBACK", "EXOGENOUS_ANSWER_BEARING", "EVALUATION_GOLD")
LEARNED_OBJECTS = ("token-prior", "value-fn", "verifier", "prompt", "memory",
                   "skill", "tool", "code", "workflow", "graph", "index",
                   "exemplar", "none")

# inner block schemas (blank-templates REC-2 = schema canon; enum drift = FAIL)
BLOCK_SCHEMAS = {
    "matrix": {
        "core_access": ("enum", ("weights", "logits", "hidden-state", "attention",
                                 "API-text", "API-multimodal")),
        "parameter_update": ("enum", ("none", "prompt", "adapter", "full")),
        "external_state_update": ("enum", ("none", "memory", "skill", "tree")),
        "reward_type": ("enum", ("gold", "verifier", "self", "env", "none")),
        "policy_update": ("enum", ("none", "nonparametric", "trained")),
        "modality_path": ("enum", ("text", "audio-native", "audio-tool", "vision", "omni")),
        "tool_use": ("enum", ("none", "fixed", "routed", "learned")),
        "budget_horizon": ("enum", ("单步", "固定K", "多轮", "任意")),
        "task": ("nonempty",),
        "trained_comparator": ("enum", YN),
    },
    "tf_audit": {
        "base_model_updated": ("enum", YN),
        "external_component_trained": ("yn_detail",),
        "component_pretrained": ("yn_detail",),
        "method_specific_parameter_training": ("yn_detail",),
        "test_time_parameter_update": ("enum", YN),
        "nonparametric_persistence": ("enum", ("within_item", "across_items", "none")),
        "ground_truth_used": ("enum", ("无", "预先", "开发集", "测试时")),
        "learned_object": ("enum_or_prefix", LEARNED_OBJECTS, "other:"),
        "learning_time": ("enum", ("test前", "test中")),
        "test_time_readonly": ("enum", YN),
    },
    "source_axes": {
        "information_source_classes": ("subset_array", ISC),
        "answer_bearing_external_info": ("enum", ("Y", "N", "UNCLEAR")),
        "gold_path_audit": ("nonempty",),
        "activation_attribution": ("enum", ("readout", "new_info", "mixed", "not_claimed")),
    },
    "omni_axes": {k: ("nonempty",) for k in (
        "core_model_modal_capability", "observation_seen_by_core",
        "tool_input_output_modalities", "action_modality",
        "multimodal_causal_grounding_evidence")},
    "rl_identity": {**{k: ("nonempty",) for k in (
        "state_definition", "action_definition", "feedback_definition",
        "transition_or_controller", "policy_representation",
        "cross_step_update_object", "credit_assignment", "stopping_rule")},
        "authors_call_it_rl": ("enum", YN)},
    "proximity": {k: ("nonempty",) for k in (
        "system_level_proximity", "component_level_proximity", "modality_proximity",
        "tf_strict_compliance", "black_box_compliance", "reward_control_proximity",
        "persistence_state_proximity")},
    "extraction": {k: ("nonempty",) for k in (
        "core_access", "modality_path", "external_components", "feedback_type",
        "what_changes_at_test_time", "persistence_scope", "compute_scaling",
        "claimed_mechanism", "strongest_result", "failure_mode",
        "reusable_implementation")},
    "resource_axes": {k: ("nonempty",) for k in (
        "model_calls", "tool_calls", "tokens", "latency_cost", "horizon", "stopping")},
    "method_occupation": {k: ("nonempty",) for k in (
        "method_gist", "method_limitations", "improvement_space", "borrowable")},
}
D2_REQUIRED_BLOCKS = ("matrix", "tf_audit", "source_axes", "extraction", "proximity")
D2_NA_OK_BLOCKS = ("omni_axes", "rl_identity", "resource_axes", "method_occupation")
D1_REQUIRED = ("id", "name", "version_pin", "topic_relevance", "venue_tier", "dfs_trigger")


def is_na_object(v):
    return isinstance(v, dict) and v.get("status") == "NA" and bool(str(v.get("reason", "")).strip())


def is_block_object(v):
    return isinstance(v, dict) and v.get("status") != "NA"


def _spec_ok(spec, val):
    kind = spec[0]
    if kind == "enum":
        return val in spec[1], f"must be one of {list(spec[1])}, got {val!r}"
    if kind == "nonempty":
        return bool(isinstance(val, str) and val.strip()), f"must be non-empty string, got {val!r}"
    if kind == "yn_detail":
        if not isinstance(val, str):
            return False, f"must be 'Y'/'N' or 'Y:<detail>'/'N:<detail>', got {val!r}"
        head, sep, detail = val.partition(":")
        ok = head in YN and (not sep or bool(detail.strip()))
        return ok, f"must be 'Y'/'N' or with non-empty ':<detail>', got {val!r}"
    if kind == "enum_or_prefix":
        if val in spec[1]:
            return True, ""
        if isinstance(val, str) and val.startswith(spec[2]) and val[len(spec[2]):].strip():
            return True, ""
        return False, f"must be one of {list(spec[1])} or {spec[2]}<non-empty>, got {val!r}"
    if kind == "subset_array":
        if not isinstance(val, list) or not val:
            return False, f"must be non-empty array, got {val!r}"
        bad = [x for x in val if x not in spec[1]]
        return not bad, f"unknown members {bad}" if bad else ""
    raise AssertionError(f"unknown spec kind {kind}")


def check_block(bad, where, bname, obj, require_all):
    """Validate one inner block against BLOCK_SCHEMAS[bname].

    require_all=True (D2): every declared key must be present and valid.
    require_all=False (D1 partial fill): only present keys are validated."""
    schema = BLOCK_SCHEMAS[bname]
    for key, spec in schema.items():
        if key not in obj or obj.get(key) is None:
            if require_all:
                bad("V9", where, f"{bname}.{key} missing (D2 requires full block)")
            continue
        ok, why = _spec_ok(spec, obj.get(key))
        if not ok:
            rule = "V9" if require_all else "V10"
            bad(rule, where, f"{bname}.{key}: {why}")


def check_evidence_axes(bad, where, r, depth):
    ea = r.get("evidence_axes")
    if not is_block_object(ea):
        bad("V9" if depth == "D2" else "V10", where,
            "evidence_axes missing/collapsed (canonical home of "
            "verification_depth + publication_status)")
        return
    vd = ea.get("verification_depth")
    if vd not in VERIFICATION_DEPTHS:
        bad("V9", where, f"evidence_axes.verification_depth enum drift: {vd!r}")
    ps = ea.get("publication_status")
    if ps not in PUBLICATION_STATUSES:
        bad("V15", where, f"evidence_axes.publication_status enum drift: {ps!r}")
    if "publication_status" in r:
        bad("V15", where, "publication_status duplicated at top level — canonical "
                          "location is evidence_axes.publication_status only")
    if depth != "D2":
        return
    sq = ea.get("study_quality") or {}
    if not isinstance(sq, dict):
        bad("V9", where, "study_quality must be an object at D2")
        return
    for d in SQ_DIMS:
        dim = sq.get(d)
        if not isinstance(dim, dict):
            bad("V9", where, f"study_quality dim missing: {d}")
            continue
        if dim.get("verdict") not in SQ_VERDICTS:
            bad("V9", where, f"study_quality.{d}.verdict enum drift: {dim.get('verdict')!r}")
        if not str(dim.get("reason", "") or "").strip():
            bad("V9", where, f"study_quality.{d}.reason empty")
        if dim.get("verdict") != "NA" and not str(dim.get("locator", "") or "").strip():
            bad("V9", where, f"study_quality.{d}.locator empty for non-NA verdict")
    if not str(sq.get("coder", "") or "").strip():
        bad("V9", where, "study_quality.coder empty")
    rating = str(sq.get("summary_rating", "") or "")
    if not rating.startswith(("HIGH", "MEDIUM", "LOW")):
        bad("V9", where, f"study_quality.summary_rating must start with HIGH/MEDIUM/LOW, "
                         f"got {rating!r}")


def validate(rec0_rows, rec2_rows, claims, flow_report, seed_rows=None):
    v = []

    def bad(rule, where, msg):
        v.append({"rule": rule, "where": where, "violation": msg})

    # ---- V14: frozen seed manifest binding (fail-closed) ----
    seed_tags = {}
    if seed_rows is None:
        bad("V14", "seed_manifest", "frozen seed manifest not bound — validator "
            "cannot certify threat-tag preservation without it")
    else:
        for s in seed_rows:
            tags = s.get("initial_tag") or []
            seed_tags[s.get("id")] = tags if isinstance(tags, list) else [tags]

    # ---- REC-2 index ----
    rec2_by_id = {}
    for i, r in enumerate(rec2_rows):
        rid = r.get("id")
        if rid in rec2_by_id:
            bad("V7", f"rec2[{i}]", f"duplicate REC-2 id: {rid}")
        else:
            rec2_by_id[rid] = r

    # ---- REC-0 ----
    seen_c = {}
    backref_owner = {}  # REC-2 id -> canonical_id of the INCLUDED REC-0 that claims it
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
                h = h if isinstance(h, dict) else {}
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
            else:
                if backref in backref_owner:
                    bad("V4", w, f"many-to-one lineage: REC-2 {backref!r} already "
                                 f"claimed by REC-0 {backref_owner[backref]!r}")
                else:
                    backref_owner[backref] = cid
                r2 = rec2_by_id[backref]
                if r2.get("rec0_backref") != cid:
                    bad("V4", w, f"cross-wired lineage: REC-2 {backref!r}.rec0_backref "
                                 f"is {r2.get('rec0_backref')!r}, expected {cid!r} — "
                                 "bidirectional one-to-one is required")
                if r2.get("coding_depth") != r.get("coding_depth"):
                    bad("V6", w, "coding_depth mismatch between REC-0 and REC-2 row")
        elif dec in ("EXCLUDED", "UNOBTAINABLE"):
            ok_code = rc in REASON_CODES or (isinstance(rc, str) and rc.startswith("OTHER:")
                                             and rc[len("OTHER:"):].strip())
            if not ok_code:
                bad("V5", w, f"reason_code missing/not in enum/empty OTHER suffix: {rc!r}")
            if not str(r.get("reason_text", "") or "").strip():
                bad("V5", w, "reason_text empty for EXCLUDED/UNOBTAINABLE")
        elif dec == "DUPLICATE":
            target = rc[len("DUPLICATE_OF:"):] if isinstance(rc, str) and \
                rc.startswith("DUPLICATE_OF:") else ""
            if not target.strip():
                bad("V5", w, f"DUPLICATE requires reason_code DUPLICATE_OF:<non-empty id>, "
                             f"got {rc!r}")
        depth = r.get("coding_depth")
        if depth not in DEPTHS:
            bad("V6", w, f"coding_depth enum drift: {depth!r}")
        elif dec == "INCLUDED" and depth == "D0":
            bad("V6", w, "INCLUDED row cannot stay at D0")
        if not str(r.get("screener", "") or "").strip():
            bad("V10", w, "screener empty string — 空字符串伪装完成")

    # duplicate targets must resolve to known canonical ids (second pass — the
    # target row may appear later in the file than the DUPLICATE row)
    for i, r in enumerate(rec0_rows):
        rc = r.get("reason_code")
        if r.get("decision") == "DUPLICATE" and isinstance(rc, str) \
                and rc.startswith("DUPLICATE_OF:"):
            target = rc[len("DUPLICATE_OF:"):].strip()
            if target and target not in seen_c:
                bad("V5", f"rec0[{i}]:{r.get('canonical_id')}",
                    f"DUPLICATE_OF target {target!r} does not resolve to any "
                    "REC-0 canonical_id")

    # ---- REC-2 ----
    rec0_included = {r.get("canonical_id"): r for r in rec0_rows
                     if r.get("decision") == "INCLUDED"}
    claim_refs = {c.get("rec2_backref") for c in claims}
    for i, r in enumerate(rec2_rows):
        w = f"rec2[{i}]:{r.get('id')}"
        cid = r.get("rec0_backref")
        if not str(cid or "").strip():
            bad("V7", w, "rec0_backref missing")
        elif cid not in rec0_included:
            bad("V7", w, f"rec0_backref does not resolve to an INCLUDED REC-0 row: {cid!r}")
        if r.get("id") not in backref_owner:
            bad("V7", w, "orphan REC-2 row — no INCLUDED REC-0 claims it via "
                         "extraction.rec2_backref")

        depth = r.get("coding_depth")
        tags = r.get("initial_tag") or []
        tags = tags if isinstance(tags, list) else [tags]
        inherited = seed_tags.get(cid, [])
        if "DIRECT_THREAT" in inherited and "DIRECT_THREAT" not in tags:
            bad("V14", w, "seed manifest tags this work DIRECT_THREAT but the tag "
                          "was lost in REC-2 transcription")
        is_threat = "DIRECT_THREAT" in tags or "DIRECT_THREAT" in inherited
        trigger = (r.get("topic_relevance") == "core" or is_threat
                   or r.get("id") in claim_refs)
        if trigger and depth != "D2":
            why = ("topic_relevance=core" if r.get("topic_relevance") == "core"
                   else "DIRECT_THREAT" if is_threat else "referenced by bearing claim")
            bad("V8", w, f"D2 trigger unmet ({why}) but coding_depth={depth!r}")

        if r.get("venue_tier") not in VENUE_TIERS:
            bad("V10", w, f"venue_tier enum drift: {r.get('venue_tier')!r}")
        if r.get("topic_relevance") not in TOPIC_RELEVANCE:
            bad("V10", w, f"topic_relevance enum drift: {r.get('topic_relevance')!r}")
        dfs = r.get("dfs_trigger")
        if not isinstance(dfs, list):
            bad("V10", w, f"dfs_trigger must be an array (empty = BFS only), got {dfs!r}")
        else:
            for t in dfs:
                if not str(t).startswith(DFS_PREFIXES):
                    bad("V10", w, f"dfs_trigger item outside T-a..T-d: {t!r}")

        if depth == "D2":
            for b in D2_REQUIRED_BLOCKS:
                val = r.get(b)
                if not is_block_object(val):
                    bad("V9", w, f"D2 required block missing/collapsed: {b}")
                else:
                    check_block(bad, w, b, val, require_all=True)
            for b in D2_NA_OK_BLOCKS:
                val = r.get(b)
                if is_na_object(val):
                    continue
                if not is_block_object(val):
                    bad("V9", w, f"D2 block {b} must be full object or type-stable NA object")
                else:
                    check_block(bad, w, b, val, require_all=True)
            check_evidence_axes(bad, w, r, "D2")
            rq = r.get("most_threatened_rq")
            if not isinstance(rq, list) or not rq:
                bad("V9", w, "most_threatened_rq missing/empty at D2")
            else:
                for x in rq:
                    if x not in RQ_SET and not (isinstance(x, str) and x.startswith("none(")):
                        bad("V9", w, f"most_threatened_rq item outside enum: {x!r}")
            locs = r.get("claim_locators")
            if not isinstance(locs, list) or not locs or not all(
                    isinstance(x, dict) and str(x.get("claim", "")).strip()
                    and str(x.get("locator", "")).strip() for x in locs):
                bad("V9", w, "claim_locators missing/empty at D2")
        elif depth == "D1":
            for f_ in D1_REQUIRED:
                val = r.get(f_)
                if val is None or (isinstance(val, str) and not val.strip()):
                    bad("V10", w, f"D1 required field missing/empty: {f_}")
            prox = r.get("proximity")
            if not is_block_object(prox):
                bad("V10", w, "D1 requires the full proximity block (7 axes)")
            else:
                check_block(bad, w, "proximity", prox, require_all=True)
            check_evidence_axes(bad, w, r, "D1")
            for b in ("matrix", "tf_audit", "source_axes", "omni_axes", "rl_identity",
                      "resource_axes", "method_occupation", "extraction"):
                val = r.get(b)
                if val is None:
                    continue
                if isinstance(val, str):
                    bad("V10", w, f"block {b} collapsed as bare string {val!r} — "
                                  "must be type-stable {{\"status\":\"NA\",\"reason\":...}}")
                elif is_na_object(val):
                    continue
                elif is_block_object(val):
                    check_block(bad, w, b, val, require_all=False)
                else:
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
                dis = dc.get("disagreements", 0)
                try:
                    dis_n = int(dis)
                except (TypeError, ValueError):
                    bad("V13", w, f"disagreements must be an integer, got {dis!r} — "
                                  "structured violation, not a crash")
                else:
                    if dis_n > 0 and not dc.get("adjudicator"):
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
    seeds = None
    if "--seeds" in args:
        seeds = _load_jsonl(args["--seeds"])
    if "--package" in args:
        with open(args["--package"], "r", encoding="utf-8") as f:
            pkg = json.load(f)
        rec0, rec2 = pkg.get("rec0", []), pkg.get("rec2", [])
        claims, flow = pkg.get("claims", []), pkg.get("flow_report")
        if seeds is None and "seed_manifest" in pkg:
            seeds = pkg["seed_manifest"]
        if seeds is None and "seed_manifest_path" in pkg:
            seeds = _load_jsonl(pkg["seed_manifest_path"])
    else:
        rec0 = _load_jsonl(args["--rec0"]) if "--rec0" in args else []
        rec2 = _load_jsonl(args["--rec2"]) if "--rec2" in args else []
        claims = _load_jsonl(args["--claims"]) if "--claims" in args else []
        flow = None
        if "--flow" in args:
            with open(args["--flow"], "r", encoding="utf-8") as f:
                flow = json.load(f)
    violations, derived = validate(rec0, rec2, claims, flow, seeds)
    report = {"validator_version": "v2-c4b", "n_rec0": len(rec0), "n_rec2": len(rec2),
              "n_claims": len(claims), "seed_manifest_bound": seeds is not None,
              "derived_flow": derived, "n_violations": len(violations),
              "violations": violations,
              "verdict": "PASS" if not violations else "FAIL"}
    print(json.dumps(report, ensure_ascii=False, indent=1))
    return 0 if not violations else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
