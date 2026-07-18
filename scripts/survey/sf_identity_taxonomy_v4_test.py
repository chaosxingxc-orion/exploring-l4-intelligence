#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Identity taxonomy v4 contract test (v7 doctoral review Gate MAJOR-1/-2 remediation).

V1  generic validator: fields/enums/lineage/edge-shape; unique method paths;
    pool consistency; NO hard-coded row count (accepts Stage-1B batches)
V2  unknown never satisfies the conjunction
V3  killer fixtures under the causal-edge derivation:
    K1 native-audio-no-reward not candidate; K2 evidenced tool/stop edges no-pool
    IS candidate; K3 online binary verifiable counts as reward;
    K4 disjoint select+memory_write with NO edge must be False (MAJOR-1 refuting
    construction); K5 fabricated select->memory_write edge is invalid (outside
    allowed_relations); K6 terminal-only final-answer selection + unrelated
    sequential right must be False; P1 revise->retry and P2 stop_budget->stop
    positive controls must be True
V3b author expectation set on the real rows (incl. edges-without-reward-form
    cases: ATLAS consensus, ToolGate gate)
V4  negative controls: STTS renaming breaks; PDR miscode re-inheritance breaks
V5  independent counterexamples (alias mapping); V5b CE-1b topology sensitivity
    non-vacuous
V6  occupancy: dual denominators derived from len(rows) and paper_work_id
    (never hard-coded); recompute-twice identity; policy A + strict sensitivity
V7  TRUE lineage reconciliation (fail-closed), single-write:
    coding v5 byte-identical to generator(sidecars); ledger row binds
    id+kind+sha256 on the SAME row; canonical_record_id resolves to a real
    section heading; locator grammar + canon/tex quote verification (canon
    quotes must appear inside the work's own canonical section; tex quotes
    inside the pinned eprint); paper_work_id == anchor == method-path prefix;
    actor discipline (stable ids, coder != adjudicator on load-bearing rows,
    load-bearing rows must be adjudicated_agree)
V8  semantic-mutation harness: six sidecar-side mutations (wrong work / wrong
    modality / wrong signal / nonsense locator / wrong sha / wrong kind) plus
    one coding-side hand edit — each MUST produce >=1 reconciliation failure
V9  scale: a synthetic 12th row changes denominators to /12; duplicate
    method_path_id is rejected

Persists docs/checks/2026-07-19-sf-identity-taxonomy-v4-test.json
"""
import copy
import glob
import gzip
import io
import json
import os
import re
import sys
import tarfile

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sf_coding_generator import render, ROW_KEY_ORDER  # noqa: E402

TAX = os.path.join(REPO, "wiki", "survey", "2026-07-19-sf-identity-taxonomy-v4.json")
CODING = os.path.join(REPO, "wiki", "survey", "2026-07-19-sf-known-item-coding-v5.json")
SIDECAR_DIR = os.path.join(REPO, "wiki", "survey", "sidecars")
INDEP = os.path.join(REPO, "wiki", "survey", "2026-07-18-sf-independent-counterexamples-v1.json")
INDEP2 = os.path.join(REPO, "wiki", "survey", "2026-07-19-sf-independent-counterexamples-v2.json")
OUT = os.path.join(REPO, "docs", "checks", "2026-07-19-sf-identity-taxonomy-v4-test.json")

_tax = json.load(io.open(TAX, encoding="utf-8"))
ENUMS = {k: set(v) if not isinstance(v[0], bool) else set()
         for k, v in _tax["enums"].items() if k not in ("candidate_pool_exists", "adjudication_status")}
ADJ_STATUS = set(_tax["enums"]["adjudication_status"])
SIGNAL_USE = set(_tax["signal_use"])
RIGHTS = set(_tax["decision_rights"])
REWARD_FORMS = set(_tax["reward_forms"])
ALLOWED = {k: set(v) for k, v in _tax["allowed_relations"].items()}
REWARD_USES = {"select", "prune", "revise", "route", "retry", "branch", "tool_call", "memory_write",
               "supply", "stop_budget", "execute_skip_gate"}
BOOLS = ["core_weight_update", "external_component_weight_update", "controller_program_or_config_optimized_on_labels",
         "human_or_dev_label_model_selection", "deployment_label_access", "test_item_gold_access",
         "inference_external_new_information", "explicit_candidate_pool_selection", "includes_speech_audio",
         "adjudication_required"]
LINEAGE = ["paper_work_id", "fulltext_ref", "canonical_record_id", "source_locator", "coder", "semantic_adjudicator"]
STRUCT_TOKEN = re.compile(r"p\d+|Fig\s?\d|Table\s?\d|Algorithm\s?\d|Eq\.?\s?\d|§|Iter\s?\d|rubric|阈值|轴")
QUOTE_PAT = re.compile(r"(canon|tex):\s*'([^']+)'")


def valid_edges(r):
    out = []
    for e in r.get("control_edges", []):
        if (e.get("signal_use") in r.get("signal_use", [])
                and e.get("decision_right") in r.get("decision_rights", [])
                and e.get("decision_right") in ALLOWED.get(e.get("signal_use"), ())
                and e.get("source_locator") and e.get("edge_semantics")):
            out.append(e)
    return out


def derive(r, topology_policy=("single_core", "single_core_multi_call")):
    strict = ((r["core_weight_update"] is False) and (r["external_component_weight_update"] is False)
              and r["controller_program_or_config_optimized_on_labels"] is False
              and r["human_or_dev_label_model_selection"] is False
              and r["deployment_label_access"] is False and r["test_item_gold_access"] is False
              and r["inference_external_new_information"] is False
              and r["internal_visibility"] == "api_only")
    reward = (r.get("signal_lifecycle", "none") in {"online_step", "terminal"}
              and r["signal_form"] in REWARD_FORMS
              and bool(set(r.get("signal_use", [])) & REWARD_USES))
    s0 = (strict and r["core_topology"] in topology_policy
          and r["core_native_modality"] in {"audio_native", "omni_native"})
    # CE-v2 patch (isolated non-implementer finding): a terminal-lifecycle edge
    # may only target a terminal-appropriate right — never a forward-step right
    # (branch/retry/tool_call/supply/...). Blocks the whitelisted-relation
    # terminal final-answer smuggle (__fixture__terminal_select_branch_miscat).
    live_edges = [e for e in valid_edges(r)
                  if e.get("signal_lifecycle") == "online_step"
                  or (e.get("signal_lifecycle") == "terminal"
                      and e.get("decision_right") in {"synthesize", "stop"})]
    rq = (reward and r["control_horizon"] == "sequential" and len(live_edges) >= 1)
    rgs = (r.get("selection_policy") in {"scored_select", "tournament_select"}
           and r["signal_form"] in REWARD_FORMS)
    return {"data_access_strict_bits": strict, "is_reward_guided": reward,
            "is_s0_core_compatible": s0, "is_rq_sys_control_compatible": rq,
            "is_project_method_candidate": s0 and rq, "reward_guided_selection": rgs,
            "n_valid_live_edges": len(live_edges)}


ALIAS = {"is_project_identity_candidate": "is_project_method_candidate"}


def run_expectations(cases, rows, label, policy=("single_core", "single_core_multi_call")):
    by_id = {r["method_path_id"]: r for r in rows}
    failures = []
    for pid, spec in cases.items():
        r = spec.get("row") or by_id.get(pid)
        if r is None:
            failures.append(f"{label}:{pid}: row missing")
            continue
        facts = dict(r)
        facts.update(derive(r, policy))
        for k, v in spec["expect"].items():
            k2 = ALIAS.get(k, k)
            if facts.get(k2) != v:
                failures.append(f"{label}:{pid}: expect {k2}={v}, got {facts.get(k2)}")
    return failures


def base_row(**kw):
    r = {"method_path_id": "__fixture__", "paper_work_id": "__fx__", "core_topology": "single_core",
         "core_native_modality": "text_only", "internal_visibility": "api_only",
         "core_io_modality": "text_in_text_out", "core_weight_update": False,
         "external_component_weight_update": False, "controller_program_or_config_optimized_on_labels": False,
         "human_or_dev_label_model_selection": False, "deployment_label_access": False,
         "test_item_gold_access": False, "inference_external_new_information": False,
         "signal_form": "none", "signal_source": "none", "signal_lifecycle": "none", "signal_use": [],
         "control_horizon": "terminal", "decision_rights": [], "control_edges": [],
         "selection_object": "none", "terminal_operator": "none",
         "explicit_candidate_pool_selection": False, "candidate_pool_exists": False,
         "selection_policy": "none", "includes_speech_audio": False, "adjudication_required": False}
    r.update(kw)
    return r


def fx_edge(u, d, lc="online_step"):
    return {"signal_use": u, "decision_right": d, "signal_lifecycle": lc,
            "source_locator": "fixture-locator", "edge_semantics": "fixture edge"}


def validate(rows):
    bad = []
    for r in rows:
        pid = r.get("method_path_id", "?")
        for f, dom in ENUMS.items():
            if dom and r.get(f) not in dom:
                bad.append(f"{pid}:{f}")
        for f in BOOLS:
            if not isinstance(r.get(f), bool):
                bad.append(f"{pid}:{f}")
        for f in LINEAGE:
            if not r.get(f):
                bad.append(f"{pid}:lineage:{f}")
        if r.get("candidate_pool_exists") not in (True, False, "unknown"):
            bad.append(f"{pid}:candidate_pool_exists")
        if r.get("adjudication_status") not in ADJ_STATUS:
            bad.append(f"{pid}:adjudication_status")
        if not set(r.get("signal_use", [])) <= SIGNAL_USE or not set(r.get("decision_rights", [])) <= RIGHTS:
            bad.append(f"{pid}:use/rights")
        if r.get("explicit_candidate_pool_selection") != (r.get("selection_object") != "none"):
            bad.append(f"{pid}:pool-consistency")
        if r.get("candidate_pool_exists") is False and r.get("selection_policy") != "none":
            bad.append(f"{pid}:policy-without-pool")
        for e in r.get("control_edges", []):
            if not (isinstance(e, dict) and e.get("signal_use") and e.get("decision_right")
                    and e.get("signal_lifecycle") and e.get("source_locator") and e.get("edge_semantics")):
                bad.append(f"{pid}:edge-shape")
    ids = [r.get("method_path_id") for r in rows]
    if len(ids) != len(set(ids)):
        bad.append("duplicate-method-path-id")
    return bad


# ---------- reconciliation machinery ----------

def load_sidecar_docs():
    paths = sorted(glob.glob(os.path.join(SIDECAR_DIR, "*.sidecar.json")))
    return [(os.path.basename(p), json.load(io.open(p, encoding="utf-8"))) for p in paths]


def ledger_index(rel):
    p = os.path.join(REPO, rel.replace("/", os.sep))
    if not os.path.exists(p):
        return None
    rows = [json.loads(l) for l in io.open(p, encoding="utf-8") if l.strip()]
    idx = []
    for x in rows:
        xid = x.get("arxiv_id") or x.get("id")
        kind = x.get("kind") or ("pdf" if str(x.get("url", "")).endswith(".pdf") else None)
        idx.append({"id": xid, "kind": kind, "sha256": x.get("sha256"), "stored_at": x.get("stored_at")})
    return idx


def canon_sections(path):
    text = io.open(os.path.join(REPO, path.replace("/", os.sep)), encoding="utf-8").read()
    sections = {}
    cur_key, cur = None, []
    for line in text.splitlines():
        m = re.match(r"^##\s+(\S+)", line)
        if m and not line.startswith("###"):
            if cur_key:
                sections[cur_key] = "\n".join(cur)
            cur_key, cur = m.group(1), [line]
        elif cur_key:
            cur.append(line)
    if cur_key:
        sections[cur_key] = "\n".join(cur)
    return sections


def _norm(s):
    s = re.sub(r"\\[a-zA-Z]+", " ", s)  # strip TeX command tokens before de-escaping
    return re.sub(r"\s+", " ", re.sub(r"[\\${}~]", "", s)).strip().lower()


_tex_cache = {}


def tex_text(stored_at):
    if stored_at in _tex_cache:
        return _tex_cache[stored_at]
    p = stored_at.replace("/", os.sep)
    text = ""
    if os.path.exists(p):
        try:
            with tarfile.open(p, "r:gz") as tf:
                for m in tf.getmembers():
                    if m.name.endswith(".tex"):
                        text += tf.extractfile(m).read().decode("utf-8", errors="replace")
        except tarfile.ReadError:
            with gzip.open(p, "rb") as f:
                text = f.read().decode("utf-8", errors="replace")
    _tex_cache[stored_at] = _norm(text)
    return _tex_cache[stored_at]


def check_quotes(locator, section_text, tex_norm, pid, what, fails):
    """Verify every canon/tex quote in a locator string; require at least one
    machine-verifiable component (quote or structural token)."""
    quotes = QUOTE_PAT.findall(locator or "")
    verified = False
    for kind, q in quotes:
        if kind == "canon":
            if section_text and q in section_text:
                verified = True
            else:
                fails.append(f"{pid}:{what}:canon-quote-missing:'{q[:30]}'")
        else:
            if tex_norm and _norm(q) in tex_norm:
                verified = True
            else:
                fails.append(f"{pid}:{what}:tex-quote-missing:'{q[:30]}'")
    if not quotes and not STRUCT_TOKEN.search(locator or ""):
        fails.append(f"{pid}:{what}:locator-unverifiable:'{(locator or '')[:30]}'")
        return
    if quotes and not verified:
        pass  # individual misses already recorded above


def reconcile(sidecars, coding_text):
    fails = []
    # single-write: coding must be byte-identical to generator projection
    try:
        expected = render(sidecars)
    except SystemExit as e:
        return [f"generator:{e}"]
    if coding_text != expected:
        fails.append("single-write:coding-not-byte-identical-to-generator-output")
    ledgers = {}
    sections_cache = {}
    for name, sc in sidecars:
        wid = sc.get("paper_work_id")
        ft = sc.get("fulltext", {})
        lref = ft.get("ledger")
        if lref not in ledgers:
            ledgers[lref] = ledger_index(lref) if lref else None
        idx = ledgers[lref]
        row_hit = None
        if idx is None:
            fails.append(f"{wid}:ledger-missing:{lref}")
        else:
            row_hit = next((x for x in idx if x["id"] == ft.get("id") and x["kind"] == ft.get("kind")
                            and x["sha256"] == ft.get("sha256") and x["sha256"]), None)
            if row_hit is None:
                fails.append(f"{wid}:ledger-row-binding-failed:id+kind+sha256")
        if ft.get("id") != wid:
            fails.append(f"{wid}:fulltext-id-mismatch:{ft.get('id')}")
        cfile, _, anchor = (sc.get("canonical_record_id") or "").partition("#")
        if cfile not in sections_cache:
            try:
                sections_cache[cfile] = canon_sections(cfile)
            except FileNotFoundError:
                sections_cache[cfile] = None
        secs = sections_cache[cfile]
        section_text = None
        if secs is None:
            fails.append(f"{wid}:canon-file-missing:{cfile}")
        elif anchor not in secs:
            fails.append(f"{wid}:canon-heading-unresolved:#{anchor}")
        else:
            section_text = secs[anchor]
        if anchor != wid:
            fails.append(f"{wid}:anchor-vs-work-id:{anchor}")
        tex_norm = ""
        if ft.get("kind") == "eprint" and row_hit and row_hit.get("stored_at"):
            tex_norm = tex_text(row_hit["stored_at"])
            if not tex_norm:
                fails.append(f"{wid}:eprint-unreadable:{row_hit['stored_at']}")
        for mp in sc.get("method_paths", []):
            pid = mp.get("method_path_id", "?")
            if not pid.startswith(wid + "#"):
                fails.append(f"{pid}:method-path-prefix-vs-work-id:{wid}")
            check_quotes(mp.get("source_locator"), section_text, tex_norm, pid, "row-locator", fails)
            for e in mp.get("control_edges", []):
                check_quotes(e.get("source_locator"), section_text, tex_norm, pid, "edge-locator", fails)
            for fe in mp.get("field_evidence", []):
                if mp.get(fe.get("field")) != fe.get("value"):
                    fails.append(f"{pid}:field-evidence-value-mismatch:{fe.get('field')}")
                q = fe.get("quote", "")
                if fe.get("kind") == "canon":
                    if not (section_text and q in section_text):
                        fails.append(f"{pid}:field-evidence-quote-missing:{fe.get('field')}")
                elif fe.get("kind") == "tex":
                    if not (tex_norm and _norm(q) in tex_norm):
                        fails.append(f"{pid}:field-evidence-tex-quote-missing:{fe.get('field')}")
            coder = mp.get("coder") or sc.get("coder")
            adj = mp.get("semantic_adjudicator")
            if coder in (None, "", "W1") or adj in (None, "", "W1"):
                fails.append(f"{pid}:actor-id-invalid (W1/empty forbidden)")
            if mp.get("load_bearing"):
                if mp.get("adjudication_status") != "adjudicated_agree":
                    fails.append(f"{pid}:load-bearing-not-adjudicated:{mp.get('adjudication_status')}")
                if coder == adj:
                    fails.append(f"{pid}:coder==adjudicator on load-bearing row")
    return fails


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    coding_text = io.open(CODING, encoding="utf-8").read()
    rows = json.loads(coding_text)["rows"]
    sidecars = load_sidecar_docs()
    checks = []

    def check(cid, desc, ok, detail=""):
        checks.append({"id": cid, "check": desc, "result": "PASS" if ok else "FAIL", "detail": str(detail)})

    bad = validate(rows)
    check("V1", f"通用 validator(无硬编码行数;当前 {len(rows)} 行/{len(sidecars)} sidecar)", not bad, f"{bad[:6]}")

    check("V2", "unknown 不满足合取",
          derive(base_row(core_native_modality="unknown"))["is_project_method_candidate"] is False)

    k1 = base_row(core_native_modality="audio_native")
    k2 = base_row(core_native_modality="omni_native", signal_form="verifiable_outcome",
                  signal_source="environment", signal_lifecycle="online_step",
                  signal_use=["tool_call", "stop_budget"], control_horizon="sequential",
                  decision_rights=["tool_call", "stop"],
                  control_edges=[fx_edge("tool_call", "tool_call"), fx_edge("stop_budget", "stop")])
    k3 = base_row(signal_form="verifiable_outcome", signal_source="environment",
                  signal_lifecycle="online_step", signal_use=["retry", "stop_budget"],
                  control_horizon="sequential", decision_rights=["retry", "stop"],
                  control_edges=[fx_edge("retry", "retry")])
    k4 = base_row(signal_form="scalar_score", signal_source="llm_judge", signal_lifecycle="online_step",
                  signal_use=["select"], control_horizon="sequential", decision_rights=["memory_write"])
    k5 = base_row(signal_form="scalar_score", signal_source="llm_judge", signal_lifecycle="online_step",
                  signal_use=["select"], control_horizon="sequential", decision_rights=["memory_write"],
                  control_edges=[fx_edge("select", "memory_write")])
    k6 = base_row(signal_form="pairwise_comparison", signal_source="llm_judge", signal_lifecycle="terminal",
                  signal_use=["select"], control_horizon="sequential", decision_rights=["memory_write"])
    p1 = base_row(signal_form="scalar_score", signal_source="llm_judge", signal_lifecycle="online_step",
                  signal_use=["revise"], control_horizon="sequential", decision_rights=["retry"],
                  control_edges=[fx_edge("revise", "retry")])
    p2 = base_row(signal_form="verifiable_outcome", signal_source="rule", signal_lifecycle="online_step",
                  signal_use=["stop_budget"], control_horizon="sequential", decision_rights=["stop"],
                  control_edges=[fx_edge("stop_budget", "stop")])
    d = {k: derive(v) for k, v in
         dict(k1=k1, k2=k2, k3=k3, k4=k4, k5=k5, k6=k6, p1=p1, p2=p2).items()}
    check("V3", "killers:K1 audio无reward≠cand;K2 有边无池=cand;K3 在线二值=reward;"
          "K4 disjoint无边=False;K5 伪造edge越白名单=False;K6 terminal-only+无关right=False;P1/P2 正控=True",
          (d["k1"]["is_s0_core_compatible"] and not d["k1"]["is_project_method_candidate"]
           and d["k2"]["is_rq_sys_control_compatible"] and d["k2"]["is_project_method_candidate"]
           and d["k3"]["is_reward_guided"]
           and not d["k4"]["is_rq_sys_control_compatible"]
           and not d["k5"]["is_rq_sys_control_compatible"]
           and not d["k6"]["is_rq_sys_control_compatible"]
           and d["p1"]["is_rq_sys_control_compatible"] and d["p2"]["is_rq_sys_control_compatible"]),
          {k: v["is_rq_sys_control_compatible"] for k, v in d.items()})

    author_cases = {
        "2604.16529#pdr-random-k": {"expect": {"is_reward_guided": False, "signal_form": "none",
                                               "candidate_pool_exists": True, "reward_guided_selection": False}},
        "2604.16529#rtv": {"expect": {"is_reward_guided": True, "is_rq_sys_control_compatible": False}},
        "2604.16529#rtv-pdr-pipeline": {"expect": {"is_reward_guided": True, "is_rq_sys_control_compatible": True}},
        "2602.16485#calibrated-orchestration": {"expect": {"is_reward_guided": False, "is_rq_sys_control_compatible": False}},
        "2606.03054#trained-gate": {"expect": {"signal_form": "binary_gate", "is_reward_guided": False,
                                               "is_rq_sys_control_compatible": False, "n_valid_live_edges": 1}},
        "2606.01667#agentic-orchestration": {"expect": {"is_reward_guided": False, "is_rq_sys_control_compatible": False}},
        "2026.findings-acl.1724#pipeline": {"expect": {"is_reward_guided": True, "is_rq_sys_control_compatible": True,
                                                        "data_access_strict_bits": False}},
        "2026.findings-acl.1243#closed-prompt-only": {"expect": {"is_rq_sys_control_compatible": True}},
        "2026.findings-acl.511#prm-guided-search": {"expect": {"is_rq_sys_control_compatible": True}},
    }
    f3 = run_expectations(author_cases, rows, "author")
    check("V3b", "作者反例集(含『有边但非 reward 形式不升格』两例:ATLAS/ToolGate)", not f3, f"{f3}")

    mut1 = copy.deepcopy(rows)
    for r in mut1:
        if r["method_path_id"] == "2026.findings-acl.1724#pipeline":
            r["signal_form"] = "consensus_vote"
    mut2 = copy.deepcopy(rows)
    for r in mut2:
        if r["method_path_id"] == "2604.16529#pdr-random-k":
            r["signal_form"], r["signal_source"], r["signal_lifecycle"] = "pairwise_comparison", "llm_judge", "online_step"
            r["signal_use"] = ["prune", "supply"]
    check("V4", "负控:STTS 改名必须红;PDR 错码回填必须红",
          bool(run_expectations(author_cases, mut1, "author")) and bool(run_expectations(author_cases, mut2, "author")))

    f5all = []
    n_ce = 0
    for pth in (INDEP, INDEP2):
        if os.path.exists(pth):
            indep = json.load(io.open(pth, encoding="utf-8"))
            f5all += run_expectations(indep["cases"], rows, os.path.basename(pth))
            n_ce += len(indep["cases"])
    check("V5", f"独立语义反例 x{n_ce}(v1+v2,字段别名映射)", n_ce > 0 and not f5all, f"{f5all}")

    atlas = next(r for r in rows if r["method_path_id"] == "2606.01667#agentic-orchestration")
    atlas_omni = dict(atlas, core_native_modality="omni_native")
    sens_a = derive(atlas_omni, ("single_core", "single_core_multi_call"))["is_s0_core_compatible"]
    sens_b = derive(atlas_omni, ("single_core",))["is_s0_core_compatible"]
    check("V5b", "CE-1b 拓扑蕴含敏感列非空洞", sens_a is True and sens_b is False, f"A={sens_a} strict={sens_b}")

    def occupancy(policy, rws):
        dd = [dict(r, **derive(r, policy)) for r in rws]
        works = sorted({r["paper_work_id"] for r in dd})
        n, w = len(dd), len(works)
        by_obj = {}
        for r in dd:
            if r["data_access_strict_bits"] and r["is_reward_guided"] and r["explicit_candidate_pool_selection"]:
                by_obj.setdefault(r["selection_object"], []).append(r["method_path_id"])
        by_work = {}
        for r in dd:
            by_work.setdefault(r["paper_work_id"], []).append(r)
        def dual(paths):
            uw = sorted({next(r["paper_work_id"] for r in dd if r["method_path_id"] == p) for p in paths})
            return {"method_paths": sorted(paths), "n_paths": f"{len(paths)}/{n}",
                    "unique_works": uw, "n_works": f"{len(uw)}/{w}"}
        return {
            "n_method_paths": n, "n_unique_works": w,
            "is_reward_guided": dual([r["method_path_id"] for r in dd if r["is_reward_guided"]]),
            "is_rq_sys_control_compatible": dual([r["method_path_id"] for r in dd if r["is_rq_sys_control_compatible"]]),
            "is_s0_core_compatible": dual([r["method_path_id"] for r in dd if r["is_s0_core_compatible"]]),
            "is_project_method_candidate": dual([r["method_path_id"] for r in dd if r["is_project_method_candidate"]]),
            "strict_AND_reward_AND_pool_BY_selection_object(mechanism)": {k: dual(v) for k, v in sorted(by_obj.items())},
            "reward_guided_selection": dual([r["method_path_id"] for r in dd if r["reward_guided_selection"]]),
            "learned_rm_prm_AND_pool": dual([r["method_path_id"] for r in dd
                                             if r["signal_source"] == "learned_rm_prm" and r["explicit_candidate_pool_selection"]]),
            "core_native_audio_or_omni": dual([r["method_path_id"] for r in dd
                                               if r["core_native_modality"] in ("audio_native", "omni_native")]),
        }

    occ = {"policy_A": occupancy(("single_core", "single_core_multi_call"), rows),
           "sensitivity_strict_topology": occupancy(("single_core",), rows)}
    occ2 = {"policy_A": occupancy(("single_core", "single_core_multi_call"), rows),
            "sensitivity_strict_topology": occupancy(("single_core",), rows)}
    n_rows, n_works = len(rows), len({r["paper_work_id"] for r in rows})
    v6_ok = (occ == occ2
             and occ["policy_A"]["n_method_paths"] == n_rows
             and occ["policy_A"]["n_unique_works"] == n_works
             and occ["policy_A"]["is_reward_guided"]["n_paths"].endswith(f"/{n_rows}")
             and occ["policy_A"]["is_reward_guided"]["n_works"].endswith(f"/{n_works}")
             and "sensitivity_strict_topology" in occ)
    check("V6", "occupancy 真断言:重算两次同构;分母=len(rows)/unique(paper_work_id);双政策持久化",
          v6_ok, f"paths={n_rows} works={n_works}")

    f7 = reconcile(sidecars, coding_text)
    check("V7", "真 reconciliation(单写字节等同/ledger id+kind+sha 同行绑定/正典节标题解析/"
          "locator 语法+canon|tex 引文核验/work-id 三向一致/actor 纪律+承重行独立裁决)", not f7, f"{f7[:8]}")

    baseline_fails = set(f7)
    mut_results = {}
    def mutate(tag, fn_sc=None, fn_coding=None):
        scs = copy.deepcopy(sidecars)
        ct = coding_text
        if fn_sc:
            fn_sc(scs)
            ct = render(scs) if fn_coding is None else ct
        if fn_coding:
            ct = fn_coding(ct)
        new = set(reconcile(scs, ct)) - baseline_fails
        mut_results[tag] = sorted(new)[:3]
        return bool(new)  # must produce NEW failures beyond baseline (anti-vacuous)

    def sc_atlas(scs):
        return next(sc for _, sc in scs if sc["paper_work_id"] == "2606.01667")

    def mut_wrong_work(scs):
        sc = sc_atlas(scs)
        sc["paper_work_id"] = "bogus-work"
        sc["fulltext"]["id"] = "bogus-work"

    m_ok = all([
        mutate("wrong_work", mut_wrong_work),
        mutate("wrong_modality", lambda scs: sc_atlas(scs)["method_paths"][0].update(core_native_modality="text_only")),
        mutate("wrong_signal", lambda scs: next(sc for _, sc in scs if sc["paper_work_id"] == "2026.findings-acl.1724")
               ["method_paths"][0].update(signal_form="consensus_vote")),
        mutate("nonsense_locator", lambda scs: sc_atlas(scs)["method_paths"][0].update(source_locator="nonsense")),
        mutate("wrong_sha", lambda scs: sc_atlas(scs)["fulltext"].update(sha256="0" * 64)),
        mutate("wrong_kind", lambda scs: sc_atlas(scs)["fulltext"].update(kind="eprint")),
        mutate("coding_hand_edit", fn_coding=lambda ct: ct.replace(
            '"core_io_modality": "multimodal_in_text_out"', '"core_io_modality": "text_in_text_out"', 1)),
    ])
    check("V8", "六类语义突变+编码手改 全部 fail-closed(每类须产生基线之外的新失败——防空洞闭合)", m_ok, mut_results)

    fixture12 = base_row(method_path_id="__fx12__#path", paper_work_id="__fx12__",
                         signal_form="scalar_score", signal_source="llm_judge",
                         signal_lifecycle="online_step", signal_use=["revise"],
                         control_horizon="sequential", decision_rights=["retry"],
                         control_edges=[fx_edge("revise", "retry")],
                         fulltext_ref={"ledger": "x", "id": "__fx12__", "kind": "pdf", "sha256": "x"},
                         canonical_record_id="x#__fx12__", source_locator="fixture p1",
                         coder="fx-coder", semantic_adjudicator="fx-adj",
                         adjudication_status="adjudicated_agree", load_bearing=False)
    occ12 = occupancy(("single_core", "single_core_multi_call"), rows + [fixture12])
    dup_bad = validate(rows + [dict(rows[0])])
    check("V9", "扩容:第12行→分母自动 /12;重复 method_path_id 被拒",
          occ12["n_method_paths"] == n_rows + 1
          and occ12["is_reward_guided"]["n_paths"].endswith(f"/{n_rows + 1}")
          and "duplicate-method-path-id" in dup_bad,
          f"n12={occ12['n_method_paths']}")

    n_pass = sum(1 for c in checks if c["result"] == "PASS")
    report = {"artifact_id": "SF-IDENTITY-TAXONOMY-V4-TEST-2026-07-19-01",
              "inputs": {"taxonomy": os.path.relpath(TAX, REPO).replace("\\", "/"),
                         "coding": os.path.relpath(CODING, REPO).replace("\\", "/"),
                         "sidecars": [n for n, _ in sidecars]},
              "topology_policy": "A(frozen) + strict-topology sensitivity dual-computed",
              "checks": checks, "occupancy": occ, "mutation_results": mut_results,
              "summary": f"{n_pass}/{len(checks)} PASS",
              "verdict": "PASS" if n_pass == len(checks) else "FAIL"}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "wb") as f:
        f.write((json.dumps(report, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    print(json.dumps({"summary": report["summary"], "verdict": report["verdict"],
                      "policy_A_key_numbers": {
                          "reward_guided": occ["policy_A"]["is_reward_guided"]["n_paths"],
                          "rq_sys_compatible": occ["policy_A"]["is_rq_sys_control_compatible"]["n_paths"]
                          + " (works " + occ["policy_A"]["is_rq_sys_control_compatible"]["n_works"] + ")",
                          "method_candidate": occ["policy_A"]["is_project_method_candidate"]["n_paths"],
                          "reward_guided_selection": occ["policy_A"]["reward_guided_selection"]["n_paths"],
                          "strict_reward_pool": {k: v["n_paths"] + " (works " + v["n_works"] + ")"
                                                 for k, v in occ["policy_A"]["strict_AND_reward_AND_pool_BY_selection_object(mechanism)"].items()}}},
                     ensure_ascii=False, indent=1))
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
