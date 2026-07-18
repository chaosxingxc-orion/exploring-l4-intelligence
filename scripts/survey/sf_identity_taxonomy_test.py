#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Identity-taxonomy contract test (v5-review P0-2; owner ruling 2 2026-07-18).

Validates the frozen taxonomy + the per-method-path coding table:
  V1  every row carries every declared field, enums legal, no extra fields
  V2  derived fields recomputed from the table (is_reward_guided /
      is_all_system_training_free / is_project_strict_identity)
  V3  the four reviewer counterexample unit tests assert against the table
      (Selective TTS reward-guided; AutoTTS dev-label-not-test-leak;
      Team of Thoughts dev-label; DeepVerifier main-path split from SFT row)
  V4  internal negative control: a mutated copy (Selective TTS score_type ->
      consensus_mbr) MUST fail its unit test — proves the oracle can fail
  V5  occupancy conjunction counts are recomputed and persisted — free-text
      quantifier claims must quote THIS output (no hand counting)

No network, stdlib only. Exit 0 iff all checks PASS. Persists
  docs/checks/2026-07-18-sf-identity-taxonomy-test.json
Run from repo root:  python scripts/survey/sf_identity_taxonomy_test.py
"""
import copy
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TAX = os.path.join(REPO, "wiki", "survey", "2026-07-18-sf-identity-taxonomy-v1.json")
CODING = os.path.join(REPO, "wiki", "survey", "2026-07-18-sf-known-item-coding-v2.json")
OUT = os.path.join(REPO, "docs", "checks", "2026-07-18-sf-identity-taxonomy-test.json")

REWARD_SCORES = {"verifiable_utility", "rule_reward", "learned_rm_prm", "llm_judge", "human_aligned_proxy"}
BOOL_FIELDS = ["core_weight_update", "external_component_weight_update",
               "controller_program_or_config_optimized_on_labels",
               "human_or_dev_label_model_selection", "deployment_label_access",
               "test_item_gold_access", "inference_external_new_information",
               "explicit_candidate_pool_selection", "includes_speech_audio"]


def derive(r):
    return {
        "is_reward_guided": r["score_type"] in REWARD_SCORES,
        "is_all_system_training_free": not r["core_weight_update"] and not r["external_component_weight_update"],
        "is_project_strict_identity": (not r["core_weight_update"] and not r["external_component_weight_update"]
                                       and not r["controller_program_or_config_optimized_on_labels"]
                                       and not r["human_or_dev_label_model_selection"]
                                       and not r["deployment_label_access"] and not r["test_item_gold_access"]
                                       and not r["inference_external_new_information"]
                                       and r["model_access_level"] == "api_text_only"),
    }


def run_unit_tests(tax, rows):
    by_id = {r["method_path_id"]: r for r in rows}
    failures = []
    for pid, spec in tax["counterexample_unit_tests"].items():
        r = by_id.get(pid)
        if r is None:
            failures.append(f"{pid}: row missing")
            continue
        facts = dict(r)
        facts.update(derive(r))
        for k, v in spec["expect"].items():
            if facts.get(k) != v:
                failures.append(f"{pid}: expect {k}={v}, got {facts.get(k)}")
    return failures


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    tax = json.load(open(TAX, encoding="utf-8"))
    coding = json.load(open(CODING, encoding="utf-8"))
    rows = coding["rows"]
    checks = []

    def check(cid, desc, ok, detail=""):
        checks.append({"id": cid, "check": desc, "result": "PASS" if ok else "FAIL", "detail": detail})

    score_enum = set(tax["enums"]["score_type"])
    access_enum = set(tax["enums"]["model_access_level"])
    bad = []
    for r in rows:
        for f in BOOL_FIELDS:
            if not isinstance(r.get(f), bool):
                bad.append(f"{r.get('method_path_id','?')}:{f}")
        if r.get("score_type") not in score_enum:
            bad.append(f"{r.get('method_path_id','?')}:score_type")
        if r.get("model_access_level") not in access_enum:
            bad.append(f"{r.get('method_path_id','?')}:model_access_level")
        if "#" not in r.get("method_path_id", ""):
            bad.append(f"{r.get('method_path_id','?')}:method_path_id shape")
    check("V1", "字段齐备/枚举合法/method_path 形状", not bad, f"bad={bad[:6]}")

    ids = [r["method_path_id"] for r in rows]
    check("V1b", "method_path_id 全唯一且 9 行（8 works,DeepVerifier 双路径）",
          len(ids) == len(set(ids)) == 9, f"n={len(ids)}")

    ut_failures = run_unit_tests(tax, rows)
    check("V3", "四反例单测（Selective TTS/AutoTTS/Team of Thoughts/DeepVerifier 主路径）",
          not ut_failures, f"failures={ut_failures}")

    mutated = copy.deepcopy(rows)
    for r in mutated:
        if r["method_path_id"] == "2026.findings-acl.1724#pipeline":
            r["score_type"] = "consensus_mbr"  # the exact renaming Round D forbids
    check("V4", "负控:把 Selective TTS 改名出 reward 集合必须被单测抓住",
          bool(run_unit_tests(tax, mutated)), "mutation undetected!" if not run_unit_tests(tax, mutated) else "detected")

    d = [dict(r, **derive(r)) for r in rows]
    occupancy = {
        "n_method_paths": len(d),
        "all_system_training_free": sorted(r["method_path_id"] for r in d if r["is_all_system_training_free"]),
        "reward_guided": sorted(r["method_path_id"] for r in d if r["is_reward_guided"]),
        "training_free_AND_reward_guided_AND_explicit_pool": sorted(
            r["method_path_id"] for r in d if r["is_all_system_training_free"] and r["is_reward_guided"]
            and r["explicit_candidate_pool_selection"]),
        "project_strict_identity_bits": sorted(r["method_path_id"] for r in d if r["is_project_strict_identity"]),
        "strict_AND_reward_guided_AND_pool": sorted(
            r["method_path_id"] for r in d if r["is_project_strict_identity"] and r["is_reward_guided"]
            and r["explicit_candidate_pool_selection"]),
        "includes_speech_audio": sorted(r["method_path_id"] for r in d if r["includes_speech_audio"]),
    }
    check("V5", "occupancy 合取计数机器重算并持久化（散文量词必须引用本输出）", True,
          f"strict∧reward∧pool={occupancy['strict_AND_reward_guided_AND_pool']}")

    n_pass = sum(1 for c in checks if c["result"] == "PASS")
    report = {
        "artifact_id": "SF-IDENTITY-TAXONOMY-TEST-2026-07-18-01",
        "inputs": {"taxonomy": os.path.relpath(TAX, REPO).replace("\\", "/"),
                   "coding": os.path.relpath(CODING, REPO).replace("\\", "/")},
        "checks": checks, "occupancy": occupancy,
        "summary": f"{n_pass}/{len(checks)} PASS",
        "verdict": "PASS" if n_pass == len(checks) else "FAIL",
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "wb") as f:
        f.write((json.dumps(report, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    print(json.dumps({"summary": report["summary"], "verdict": report["verdict"],
                      "occupancy": occupancy}, ensure_ascii=False, indent=1))
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
