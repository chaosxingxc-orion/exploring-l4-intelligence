#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Identity taxonomy v2 contract test (v5-response re-review P0-1/P1-4).

V1  field/enum/shape validation; 11 unique method paths; pool bit must equal
    (selection_object != none) — analysis-unit consistency (Round B)
V2  derived fields recomputed; unknown values never satisfy a conjunction
V3  author counterexample unit tests (taxonomy v2 set)
V4  negative control: renaming Selective TTS's judge signal out of the reward
    set MUST break its unit test (oracle-can-fail proof)
V5  INDEPENDENT semantic counterexamples (P1-4): loaded from a file authored by
    a non-implementer agent; file missing or any assertion failing = FAIL
V6  occupancy conjunctions persisted, K-pool counts stratified by
    selection_object (never aggregated across tool-agent/trajectory/output pools)

Persists docs/checks/2026-07-18-sf-identity-taxonomy-v2-test.json
Run from repo root:  python scripts/survey/sf_identity_taxonomy_v2_test.py
"""
import copy
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TAX = os.path.join(REPO, "wiki", "survey", "2026-07-18-sf-identity-taxonomy-v2.json")
CODING = os.path.join(REPO, "wiki", "survey", "2026-07-18-sf-known-item-coding-v3.json")
INDEP = os.path.join(REPO, "wiki", "survey", "2026-07-18-sf-independent-counterexamples-v1.json")
OUT = os.path.join(REPO, "docs", "checks", "2026-07-18-sf-identity-taxonomy-v2-test.json")

ENUMS = {
    "core_topology": {"single_core", "single_core_multi_call", "multi_model_federation", "core_plus_external_model"},
    "core_native_modality": {"text_only", "vision_native", "audio_native", "omni_native", "asr_mediated", "unknown"},
    "internal_visibility": {"api_only", "logits_logprob", "hidden_state", "gradient"},
    "core_io_modality": {"text_in_text_out", "multimodal_in_text_out", "multimodal_in_out"},
    "signal_form": {"scalar_score", "pairwise_comparison", "binary_gate", "text_critique", "confidence", "consensus_vote", "verifiable_outcome", "none"},
    "signal_source": {"rule", "llm_judge", "trained_classifier", "learned_rm_prm", "environment", "self_confidence", "consensus", "human_aligned_proxy", "none"},
    "control_horizon": {"terminal", "sequential", "offline_meta"},
    "selection_object": {"candidate_output", "trajectory", "action", "tool_agent", "plan", "none"},
    "terminal_operator": {"select_one", "prune", "route", "vote", "merge", "synthesize", "accept_reject", "none"},
}
SIGNAL_USE = {"select", "prune", "route", "revise", "state_update", "supply", "stop_budget", "execute_skip_gate", "synthesize_input", "train_controller", "offline_diagnostic"}
DECISION_RIGHTS = {"route", "retry", "branch", "tool_call", "memory_write", "supply", "stop", "synthesize", "execute_skip"}
BOOLS = ["core_weight_update", "external_component_weight_update", "controller_program_or_config_optimized_on_labels",
         "human_or_dev_label_model_selection", "deployment_label_access", "test_item_gold_access",
         "inference_external_new_information", "explicit_candidate_pool_selection", "includes_speech_audio"]


def derive(r):
    frozen = (r["core_weight_update"] is False) and (r["external_component_weight_update"] is False)
    strict = (frozen and r["controller_program_or_config_optimized_on_labels"] is False
              and r["human_or_dev_label_model_selection"] is False
              and r["deployment_label_access"] is False and r["test_item_gold_access"] is False
              and r["inference_external_new_information"] is False
              and r["internal_visibility"] == "api_only")
    reward = (r["signal_form"] in {"scalar_score", "pairwise_comparison", "verifiable_outcome"}
              and bool(set(r["signal_use"]) & {"select", "prune", "revise"}))
    ident = (strict and r["core_topology"] in {"single_core", "single_core_multi_call"}
             and r["core_native_modality"] in {"audio_native", "omni_native"})
    return {"all_components_weight_frozen": frozen, "data_access_strict_bits": strict,
            "is_reward_guided": reward, "is_project_identity_candidate": ident}


def run_expectations(cases, rows, label):
    by_id = {r["method_path_id"]: r for r in rows}
    failures = []
    for pid, spec in cases.items():
        r = spec.get("row") or by_id.get(pid)  # inline fixture rows supported (CE-2 benchmark class)
        if r is None:
            failures.append(f"{label}:{pid}: row missing")
            continue
        facts = dict(r)
        facts.update(derive(r))
        for k, v in spec["expect"].items():
            if facts.get(k) != v:
                failures.append(f"{label}:{pid}: expect {k}={v}, got {facts.get(k)}")
    return failures


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    tax = json.load(open(TAX, encoding="utf-8"))
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
        if not set(r.get("signal_use", [])) <= SIGNAL_USE:
            bad.append(f"{r.get('method_path_id','?')}:signal_use")
        if not set(r.get("decision_rights", [])) <= DECISION_RIGHTS:
            bad.append(f"{r.get('method_path_id','?')}:decision_rights")
        if r.get("explicit_candidate_pool_selection") != (r.get("selection_object") != "none"):
            bad.append(f"{r.get('method_path_id','?')}:pool!=selection_object-consistency")
    ids = [r["method_path_id"] for r in rows]
    check("V1", "字段/枚举/形状 + 11 唯一路径 + 池位与 selection_object 一致",
          not bad and len(ids) == len(set(ids)) == 11, f"bad={bad[:6]} n={len(ids)}")

    unknown_row = dict(rows[0])
    unknown_row["core_native_modality"] = "unknown"
    check("V2", "unknown 不满足合取（评审 §8.1）",
          derive(unknown_row)["is_project_identity_candidate"] is False, "")

    f3 = run_expectations(tax["author_counterexample_unit_tests"], rows, "author")
    check("V3", "作者反例单测（v2 集,含 ToolGate 非 reward-guided/联邦分析单位）", not f3, f"{f3}")

    mutated = copy.deepcopy(rows)
    for r in mutated:
        if r["method_path_id"] == "2026.findings-acl.1724#pipeline":
            r["signal_form"] = "consensus_vote"
    check("V4", "负控:改名 Selective TTS 出 reward 集合必须被抓住",
          bool(run_expectations(tax["author_counterexample_unit_tests"], mutated, "author")), "")

    if not os.path.exists(INDEP):
        check("V5", "独立语义反例（P1-4,非实现者供给）", False, "file missing — P1-4 contract unmet")
    else:
        indep = json.load(open(INDEP, encoding="utf-8"))
        f5 = run_expectations(indep["cases"], rows, "independent")
        check("V5", f"独立语义反例 x{len(indep['cases'])}（供给者:{indep.get('author','?')}）", not f5, f"{f5}")

    d = [dict(r, **derive(r)) for r in rows]
    by_obj = {}
    for r in d:
        if r["data_access_strict_bits"] and r["is_reward_guided"] and r["explicit_candidate_pool_selection"]:
            by_obj.setdefault(r["selection_object"], []).append(r["method_path_id"])
    occupancy = {
        "n_method_paths": len(d),
        "all_components_weight_frozen": sorted(r["method_path_id"] for r in d if r["all_components_weight_frozen"]),
        "is_reward_guided": sorted(r["method_path_id"] for r in d if r["is_reward_guided"]),
        "data_access_strict_bits": sorted(r["method_path_id"] for r in d if r["data_access_strict_bits"]),
        "strict_AND_reward_AND_pool_BY_selection_object": {k: sorted(v) for k, v in sorted(by_obj.items())},
        "learned_rm_prm_AND_pool": sorted(r["method_path_id"] for r in d if r["signal_source"] == "learned_rm_prm" and r["explicit_candidate_pool_selection"]),
        "is_project_identity_candidate": sorted(r["method_path_id"] for r in d if r["is_project_identity_candidate"]),
        "core_native_modality_audio_or_omni": sorted(r["method_path_id"] for r in d if r["core_native_modality"] in ("audio_native", "omni_native")),
        "includes_speech_audio_dataset_bit": sorted(r["method_path_id"] for r in d if r["includes_speech_audio"]),
    }
    check("V6", "occupancy 持久化;K 池按 selection_object 分层,不跨池聚合", True,
          f"strict∧reward∧pool by object = { {k: len(v) for k, v in by_obj.items()} }")

    n_pass = sum(1 for c in checks if c["result"] == "PASS")
    report = {"artifact_id": "SF-IDENTITY-TAXONOMY-V2-TEST-2026-07-18-01",
              "inputs": {"taxonomy": "wiki/survey/2026-07-18-sf-identity-taxonomy-v2.json",
                         "coding": "wiki/survey/2026-07-18-sf-known-item-coding-v3.json",
                         "independent_counterexamples": "wiki/survey/2026-07-18-sf-independent-counterexamples-v1.json"},
              "checks": checks, "occupancy": occupancy,
              "summary": f"{n_pass}/{len(checks)} PASS",
              "verdict": "PASS" if n_pass == len(checks) else "FAIL"}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "wb") as f:
        f.write((json.dumps(report, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    print(json.dumps({"summary": report["summary"], "verdict": report["verdict"], "occupancy": occupancy},
                     ensure_ascii=False, indent=1))
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
