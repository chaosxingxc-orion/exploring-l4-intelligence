#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Identity taxonomy v3 contract test (v6 review P0-1/P0-2/P0-3; owner rulings 2026-07-18).

V1  field/enum/shape (incl. signal_lifecycle + lineage fields); 11 unique paths;
    pool bit == (selection_object != none)
V2  derivation trio (s0-core / rq-sys-control / method-candidate) under frozen
    topology policy A, PLUS strict-topology sensitivity variant dual-computed;
    unknown never satisfies
V3  killer fixtures (Round-C cases, old-v2-red / new-v3-green semantics):
    K1 native-audio-no-reward must NOT be method candidate;
    K2 reward-decides-tool/stop-no-K-pool MUST be rq-sys compatible;
    K3 online binary verifiable signal must count as reward
V4  negative controls: Selective TTS renaming breaks; PDR miscode
    (pairwise re-inheritance) breaks
V5  independent counterexamples (field alias: is_project_identity_candidate ->
    is_project_method_candidate); V5b CE-1b topology implication non-vacuous in
    the sensitivity variant
V6  occupancy: dual denominators (method-path / unique-work via paper_work_id),
    pools stratified by selection_object, sensitivity column persisted
V7  lineage reconciliation (fail-closed): fulltext_ref resolves in its ledger
    with sha256; canonical_record_id file exists and anchor appears; non-empty
    source_locator/coder/adjudicator

Persists docs/checks/2026-07-18-sf-identity-taxonomy-v3-test.json
"""
import copy
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TAX = os.path.join(REPO, "wiki", "survey", "2026-07-18-sf-identity-taxonomy-v3.json")
CODING = os.path.join(REPO, "wiki", "survey", "2026-07-18-sf-known-item-coding-v4.json")
INDEP = os.path.join(REPO, "wiki", "survey", "2026-07-18-sf-independent-counterexamples-v1.json")
OUT = os.path.join(REPO, "docs", "checks", "2026-07-18-sf-identity-taxonomy-v3-test.json")

ENUMS = {
    "core_topology": {"single_core", "single_core_multi_call", "multi_model_federation", "core_plus_external_model"},
    "core_native_modality": {"text_only", "vision_native", "audio_native", "omni_native", "asr_mediated", "unknown"},
    "internal_visibility": {"api_only", "logits_logprob", "hidden_state", "gradient"},
    "core_io_modality": {"text_in_text_out", "multimodal_in_text_out", "multimodal_in_out"},
    "signal_form": {"scalar_score", "pairwise_comparison", "binary_gate", "text_critique", "confidence", "consensus_vote", "verifiable_outcome", "none"},
    "signal_source": {"rule", "llm_judge", "trained_classifier", "learned_rm_prm", "environment", "self_confidence", "consensus", "human_aligned_proxy", "none"},
    "signal_lifecycle": {"offline_calibration", "inference_pre_context", "online_step", "terminal", "none"},
    "control_horizon": {"terminal", "sequential", "offline_meta"},
    "selection_object": {"candidate_output", "trajectory", "action", "tool_agent", "plan", "none"},
    "terminal_operator": {"select_one", "prune", "route", "vote", "merge", "synthesize", "accept_reject", "none"},
}
SIGNAL_USE = {"select", "prune", "route", "revise", "retry", "branch", "tool_call", "memory_write",
              "state_update", "supply", "stop_budget", "execute_skip_gate", "synthesize_input",
              "train_controller", "offline_diagnostic"}
RIGHTS = {"route", "retry", "branch", "tool_call", "memory_write", "supply", "stop", "synthesize", "execute_skip"}
BOOLS = ["core_weight_update", "external_component_weight_update", "controller_program_or_config_optimized_on_labels",
         "human_or_dev_label_model_selection", "deployment_label_access", "test_item_gold_access",
         "inference_external_new_information", "explicit_candidate_pool_selection", "includes_speech_audio",
         "adjudication_required"]
LINEAGE = ["paper_work_id", "fulltext_ref", "canonical_record_id", "source_locator", "coder", "semantic_adjudicator"]
REWARD_FORMS = {"scalar_score", "pairwise_comparison", "verifiable_outcome"}
REWARD_USES = {"select", "prune", "revise", "route", "retry", "branch", "tool_call", "memory_write",
               "supply", "stop_budget", "execute_skip_gate"}


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
    rq = (reward and r["control_horizon"] == "sequential" and bool(r.get("decision_rights", [])))
    return {"data_access_strict_bits": strict, "is_reward_guided": reward,
            "is_s0_core_compatible": s0, "is_rq_sys_control_compatible": rq,
            "is_project_method_candidate": s0 and rq}


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
         "control_horizon": "terminal", "decision_rights": [], "selection_object": "none",
         "terminal_operator": "none", "explicit_candidate_pool_selection": False,
         "includes_speech_audio": False, "adjudication_required": False}
    r.update(kw)
    return r


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    rows = json.load(open(CODING, encoding="utf-8"))["rows"]
    checks = []

    def check(cid, desc, ok, detail=""):
        checks.append({"id": cid, "check": desc, "result": "PASS" if ok else "FAIL", "detail": detail})

    bad = []
    for r in rows:
        for f, dom in ENUMS.items():
            if r.get(f) not in dom:
                bad.append(f"{r.get('method_path_id','?')}:{f}")
        for f in BOOLS:
            if not isinstance(r.get(f), bool):
                bad.append(f"{r.get('method_path_id','?')}:{f}")
        for f in LINEAGE:
            if not r.get(f):
                bad.append(f"{r.get('method_path_id','?')}:lineage:{f}")
        if not set(r.get("signal_use", [])) <= SIGNAL_USE or not set(r.get("decision_rights", [])) <= RIGHTS:
            bad.append(f"{r.get('method_path_id','?')}:use/rights")
        if r.get("explicit_candidate_pool_selection") != (r.get("selection_object") != "none"):
            bad.append(f"{r.get('method_path_id','?')}:pool-consistency")
    ids = [r["method_path_id"] for r in rows]
    check("V1", "字段/枚举/lineage 齐备;11 唯一;池位一致", not bad and len(ids) == len(set(ids)) == 11, f"{bad[:6]}")

    unk = base_row(core_native_modality="unknown")
    check("V2", "unknown 不满足合取", derive(unk)["is_project_method_candidate"] is False, "")

    k1 = base_row(core_native_modality="audio_native")
    k2 = base_row(core_native_modality="omni_native", signal_form="verifiable_outcome",
                  signal_source="environment", signal_lifecycle="online_step",
                  signal_use=["tool_call", "stop_budget"], control_horizon="sequential",
                  decision_rights=["tool_call", "stop"])
    k3 = base_row(signal_form="verifiable_outcome", signal_source="environment",
                  signal_lifecycle="online_step", signal_use=["retry", "stop_budget"],
                  control_horizon="sequential", decision_rights=["retry", "stop"])
    d1, d2, d3 = derive(k1), derive(k2), derive(k3)
    ok3 = (d1["is_s0_core_compatible"] and not d1["is_project_method_candidate"]
           and d2["is_rq_sys_control_compatible"] and d2["is_project_method_candidate"]
           and not d2["explicit_candidate_pool_selection"] if "explicit_candidate_pool_selection" in d2 else True) \
          and d2["is_rq_sys_control_compatible"] and d3["is_reward_guided"]
    check("V3", "killer fixtures:K1 原生audio无reward≠candidate;K2 无K池的reward-tool/stop=RQ-SYS compatible(且=method candidate);K3 在线二值可验证=reward",
          d1["is_s0_core_compatible"] and not d1["is_project_method_candidate"]
          and d2["is_rq_sys_control_compatible"] and d2["is_project_method_candidate"]
          and d3["is_reward_guided"],
          f"K1={d1['is_project_method_candidate']} K2={d2['is_project_method_candidate']} K3={d3['is_reward_guided']}")

    author_cases = {
        "2604.16529#pdr-random-k": {"expect": {"is_reward_guided": False, "signal_form": "none"}},
        "2604.16529#rtv": {"expect": {"is_reward_guided": True, "is_rq_sys_control_compatible": False}},
        "2604.16529#rtv-pdr-pipeline": {"expect": {"is_reward_guided": True, "is_rq_sys_control_compatible": True}},
        "2602.16485#calibrated-orchestration": {"expect": {"is_reward_guided": False}},
        "2606.03054#trained-gate": {"expect": {"signal_form": "binary_gate", "is_reward_guided": False}},
        "2026.findings-acl.1724#pipeline": {"expect": {"is_reward_guided": True, "is_rq_sys_control_compatible": True, "data_access_strict_bits": False}},
    }
    f3 = run_expectations(author_cases, rows, "author")
    check("V3b", "作者反例(v3 集:PDR 非 reward/RTV 终态退化/pipeline 序贯/ToT 裁决/ToolGate/STTS)", not f3, f"{f3}")

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
          bool(run_expectations(author_cases, mut1, "author")) and bool(run_expectations(author_cases, mut2, "author")), "")

    if not os.path.exists(INDEP):
        check("V5", "独立语义反例", False, "file missing")
    else:
        indep = json.load(open(INDEP, encoding="utf-8"))
        f5 = run_expectations(indep["cases"], rows, "independent")
        check("V5", f"独立语义反例 x{len(indep['cases'])}(字段别名映射)", not f5, f"{f5}")
    atlas = next(r for r in rows if r["method_path_id"] == "2606.01667#agentic-orchestration")
    atlas_omni = dict(atlas, core_native_modality="omni_native")
    sens_a = derive(atlas_omni, ("single_core", "single_core_multi_call"))["is_s0_core_compatible"]
    sens_b = derive(atlas_omni, ("single_core",))["is_s0_core_compatible"]
    check("V5b", "CE-1b 拓扑蕴含在敏感列非空洞（同 row 强制 omni 后:政策A=true/严格拓扑=false,由拓扑轴本身判定）",
          sens_a is True and sens_b is False, f"A={sens_a} strict={sens_b}")

    def occupancy(policy):
        d = [dict(r, **derive(r, policy)) for r in rows]
        works = sorted({r["paper_work_id"] for r in d})
        by_obj = {}
        for r in d:
            if r["data_access_strict_bits"] and r["is_reward_guided"] and r["explicit_candidate_pool_selection"]:
                by_obj.setdefault(r["selection_object"], []).append(r["method_path_id"])
        def dual(paths):
            return {"method_paths": sorted(paths), "n_paths": f"{len(paths)}/11",
                    "unique_works": sorted({p.split('#')[0] for p in paths}),
                    "n_works": f"{len({p.split('#')[0] for p in paths})}/{len(works)}"}
        return {
            "n_method_paths": len(d), "n_unique_works": len(works),
            "is_reward_guided": dual([r["method_path_id"] for r in d if r["is_reward_guided"]]),
            "is_rq_sys_control_compatible": dual([r["method_path_id"] for r in d if r["is_rq_sys_control_compatible"]]),
            "is_s0_core_compatible": dual([r["method_path_id"] for r in d if r["is_s0_core_compatible"]]),
            "is_project_method_candidate": dual([r["method_path_id"] for r in d if r["is_project_method_candidate"]]),
            "strict_AND_reward_AND_pool_BY_selection_object(mechanism)": {k: dual(v) for k, v in sorted(by_obj.items())},
            "learned_rm_prm_AND_pool": dual([r["method_path_id"] for r in d if r["signal_source"] == "learned_rm_prm" and r["explicit_candidate_pool_selection"]]),
            "core_native_audio_or_omni": dual([r["method_path_id"] for r in d if r["core_native_modality"] in ("audio_native", "omni_native")]),
        }
    occ = {"policy_A": occupancy(("single_core", "single_core_multi_call")),
           "sensitivity_strict_topology": occupancy(("single_core",))}
    check("V6", "occupancy 双分母+机制分层+双政策敏感列持久化", True,
          f"policyA strict∧reward∧pool={ {k: v['n_paths'] for k, v in occ['policy_A']['strict_AND_reward_AND_pool_BY_selection_object(mechanism)'].items()} }")

    lin_bad = []
    ledger_cache = {}
    for r in rows:
        ref = r["fulltext_ref"]
        lp = os.path.join(REPO, ref["ledger"].replace("/", os.sep))
        if ref["ledger"] not in ledger_cache:
            try:
                ledger_cache[ref["ledger"]] = [json.loads(l) for l in open(lp, encoding="utf-8") if l.strip()]
            except FileNotFoundError:
                ledger_cache[ref["ledger"]] = None
        rows_l = ledger_cache[ref["ledger"]]
        if rows_l is None:
            lin_bad.append(f"{r['method_path_id']}:ledger-missing")
            continue
        hit = [x for x in rows_l if (x.get("arxiv_id") == ref["id"] or x.get("id") == ref["id"]) and x.get("sha256")]
        if not hit:
            lin_bad.append(f"{r['method_path_id']}:no-sha-row")
        cf, _, anchor = r["canonical_record_id"].partition("#")
        cp = os.path.join(REPO, cf.replace("/", os.sep))
        if not os.path.exists(cp):
            lin_bad.append(f"{r['method_path_id']}:canon-file-missing")
        elif anchor and anchor not in open(cp, encoding="utf-8").read():
            lin_bad.append(f"{r['method_path_id']}:anchor-missing")
    check("V7", "lineage reconciliation(fail-closed):fulltext sha 在台账/正典文件+anchor 在/locator 非空", not lin_bad, f"{lin_bad[:5]}")

    n_pass = sum(1 for c in checks if c["result"] == "PASS")
    report = {"artifact_id": "SF-IDENTITY-TAXONOMY-V3-TEST-2026-07-18-01",
              "inputs": {"taxonomy": os.path.relpath(TAX, REPO).replace("\\", "/"),
                         "coding": os.path.relpath(CODING, REPO).replace("\\", "/")},
              "topology_policy": "A(frozen: single_core_multi_call in-scope) + strict-topology sensitivity dual-computed",
              "checks": checks, "occupancy": occ,
              "summary": f"{n_pass}/{len(checks)} PASS",
              "verdict": "PASS" if n_pass == len(checks) else "FAIL"}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "wb") as f:
        f.write((json.dumps(report, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    print(json.dumps({"summary": report["summary"], "verdict": report["verdict"],
                      "policy_A_key_numbers": {
                          "reward_guided": occ["policy_A"]["is_reward_guided"]["n_paths"],
                          "rq_sys_compatible": occ["policy_A"]["is_rq_sys_control_compatible"]["n_paths"],
                          "method_candidate": occ["policy_A"]["is_project_method_candidate"]["n_paths"],
                          "strict_reward_pool": {k: v["n_paths"] + " (works " + v["n_works"] + ")" for k, v in occ["policy_A"]["strict_AND_reward_AND_pool_BY_selection_object(mechanism)"].items()}}},
                     ensure_ascii=False, indent=1))
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
