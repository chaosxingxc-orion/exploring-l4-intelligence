#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fixture test for sf_record_validator.py (correction #4A / P0-R3).

Materializes one positive package and 14 deliberately-broken negative packages under
wiki/survey/fixtures-c4a/, then runs the validator AS A SUBPROCESS on every file so the
acceptance criterion "负例必须真的使 validator 非零退出" is tested at the exit-code level,
not inside the same interpreter. Persists docs/checks/2026-07-16-sf-record-validator-test.json.

Run from repo root:  python scripts/survey/sf_record_validator_test.py   (exit 0 iff PASS)
"""
import copy
import hashlib
import json
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VALIDATOR = os.path.join(REPO, "scripts", "survey", "sf_record_validator.py")
FIXDIR = os.path.join(REPO, "wiki", "survey", "fixtures-c4a")
OUT = os.path.join(REPO, "docs", "checks", "2026-07-16-sf-record-validator-test.json")


def sq_dim(verdict="PASS", reason="reported in paper", locator="§4/Table 2"):
    return {"verdict": verdict, "reason": reason, "locator": locator}


def positive_package():
    rec2_d2 = {
        "id": "REC2-AMC", "name": "Agentic Monte Carlo", "version_pin": "v1",
        "lanes": ["SF-L1"], "coding_depth": "D2", "rec0_backref": "2606.05296",
        "initial_tag": ["DIRECT_THREAT"], "topic_relevance": "core",
        "matrix": {"core_access": "API-text", "parameter_update": "none",
                   "external_state_update": "none", "reward_type": "verifier",
                   "policy_update": "none", "modality_path": "text", "tool_use": "fixed",
                   "budget_horizon": "多轮", "task": "agent benchmarks",
                   "trained_comparator": "Y"},
        "tf_audit": {"base_model_updated": "N", "external_component_trained": "Y:value-fn",
                     "component_pretrained": "N", "method_specific_parameter_training": "Y:value-fn",
                     "test_time_parameter_update": "N", "nonparametric_persistence": "none",
                     "ground_truth_used": "开发集", "learned_object": "value-fn",
                     "learning_time": "test前", "test_time_readonly": "Y"},
        "source_axes": {"information_source_classes": ["PRETRAINED_READOUT",
                                                       "ENDOGENOUS_ENV_FEEDBACK"],
                        "answer_bearing_external_info": "N",
                        "gold_path_audit": "no gold in selection path per §3.2",
                        "activation_attribution": "readout"},
        "omni_axes": {"status": "NA", "reason": "text-only agent system, no omni claims"},
        "rl_identity": {"state_definition": "env obs", "action_definition": "agent actions",
                        "feedback_definition": "return estimate", "transition_or_controller": "SMC",
                        "policy_representation": "frozen LLM prior + value reweighting",
                        "cross_step_update_object": "particle set", "credit_assignment": "value fn",
                        "stopping_rule": "budget", "authors_call_it_rl": "Y"},
        "proximity": {"system_level_proximity": "high", "component_level_proximity": "high",
                      "modality_proximity": "text-only", "tf_strict_compliance": "partial",
                      "black_box_compliance": "yes", "reward_control_proximity": "high",
                      "persistence_state_proximity": "none"},
        "extraction": {"core_access": "API-text", "modality_path": "text",
                       "external_components": "learned value fn", "feedback_type": "verifier",
                       "what_changes_at_test_time": "particle set", "persistence_scope": "none",
                       "compute_scaling": "K particles", "claimed_mechanism": "posterior sampling",
                       "strongest_result": "beats GRPO on AgentGym", "failure_mode": "value bias",
                       "reusable_implementation": "code released"},
        "resource_axes": {"status": "NA", "reason": "resource table not reported in v1"},
        "most_threatened_rq": ["RQ-SYS"],
        "venue_tier": "T3", "topic_relevance_note": "core: same problem identity",
        "evidence_axes": {"verification_depth": "FULLTEXT_OPENED",
                          "publication_status": "preprint",
                          "study_quality": {"data_boundary": sq_dim(),
                                            "control_fairness": sq_dim("PARTIAL",
                                                                       "GRPO baseline budget unclear",
                                                                       "§5.1"),
                                            "uncertainty_reporting": sq_dim("FAIL", "single seed",
                                                                            "§5"),
                                            "ablation_attribution": sq_dim(),
                                            "reproducibility": sq_dim(),
                                            "artifact_availability": sq_dim(),
                                            "claim_evidence_match": sq_dim(),
                                            "summary_rating": "MEDIUM", "coder": "coordinator"}},
        "dfs_trigger": ["T-a对象"],
        "method_occupation": {"method_gist": "SMC over frozen agent prior",
                              "method_limitations": "trained value fn breaks TFStrict",
                              "improvement_space": "①black-box value ②needs dev labels ③RQ-SYS",
                              "borrowable": "particle reweighting"},
        "claim_locators": [{"claim": "beats prompting and GRPO on AgentGym",
                            "locator": "v1 §5 Table 1", "span": "rows 3-5"}],
        "threat_dual_coding": {"extractor_A": "coder-1", "extractor_B": "coder-2",
                               "disagreements": 1, "adjudicator": "coordinator",
                               "rec5_ref": "REC5-2606.05296"},
    }
    rec2_d1 = {
        "id": "REC2-EVOLIB", "name": "EvoLib", "version_pin": "v1",
        "lanes": ["SF-L4"], "coding_depth": "D1", "rec0_backref": "2605.14477",
        "topic_relevance": "element",
        "proximity": {"system_level_proximity": "medium", "component_level_proximity": "high",
                      "modality_proximity": "text-only", "tf_strict_compliance": "yes",
                      "black_box_compliance": "yes", "reward_control_proximity": "medium",
                      "persistence_state_proximity": "across_items"},
        "publication_status": "preprint", "venue_tier": "T3",
        "dfs_trigger": [], "evidence_axes": {"verification_depth": "ABSTRACT_VERIFIED",
                                             "publication_status": "preprint",
                                             "study_quality": None},
        "matrix": {"status": "NA", "reason": "D1 minimal core; matrix coded on use"},
        "tf_audit": {"status": "NA", "reason": "D1 minimal core; audited on use"},
        "source_axes": {"status": "NA", "reason": "D1 minimal core"},
        "omni_axes": {"status": "NA", "reason": "text-only"},
        "rl_identity": {"status": "NA", "reason": "no RL claim in abstract"},
        "resource_axes": {"status": "NA", "reason": "D1 minimal core"},
        "method_occupation": {"status": "NA", "reason": "coded on use"},
        "extraction": {"status": "NA", "reason": "D1 minimal core"},
    }
    rec0 = [
        {"canonical_id": "2606.05296", "title": "Agentic Monte Carlo",
         "source_hits": [{"source": "seed:manifest#88", "hit_ref": "seed-manifest row 88"}],
         "dedup": {"merged_from": [], "merge_basis": "same_arxiv_id"},
         "screening_stage": "FULLTEXT", "decision": "INCLUDED", "reason_code": None,
         "reason_text": None, "screener": "coordinator",
         "screened_at": "2026-07-16T00:00:00Z", "second_reviewer": None,
         "adjudicator": None, "adjudication_note": None, "fulltext_version_ref": "v1",
         "extraction": {"rec2_backref": "REC2-AMC", "extractor": "coordinator",
                        "extracted_at": "2026-07-16T00:00:00Z"},
         "coding_depth": "D2"},
        {"canonical_id": "2605.14477", "title": "EvoLib",
         "source_hits": [{"source": "seed:manifest#90", "hit_ref": "seed-manifest row 90"}],
         "dedup": {"merged_from": [], "merge_basis": "same_arxiv_id"},
         "screening_stage": "ABSTRACT", "decision": "INCLUDED", "reason_code": None,
         "reason_text": None, "screener": "coordinator",
         "screened_at": "2026-07-16T00:00:00Z", "second_reviewer": None,
         "adjudicator": None, "adjudication_note": None, "fulltext_version_ref": "v1",
         "extraction": {"rec2_backref": "REC2-EVOLIB", "extractor": "coordinator",
                        "extracted_at": "2026-07-16T00:00:00Z"},
         "coding_depth": "D1"},
        {"canonical_id": "2401.00001", "title": "Unrelated diffusion paper",
         "source_hits": [{"source": "query:SF-L1-Q1", "hit_ref": "REC1 line 12"}],
         "dedup": {"merged_from": [], "merge_basis": "same_arxiv_id"},
         "screening_stage": "TITLE", "decision": "EXCLUDED", "reason_code": "NOT_RELEVANT",
         "reason_text": "image diffusion training, no inference-time optimization",
         "screener": "coordinator", "screened_at": "2026-07-16T00:00:00Z",
         "second_reviewer": None, "adjudicator": None, "adjudication_note": None,
         "fulltext_version_ref": None,
         "extraction": {"rec2_backref": None, "extractor": None, "extracted_at": None},
         "coding_depth": "D0"},
        {"canonical_id": "2401.00002", "title": "Same work under variant title",
         "source_hits": [{"source": "route:SF-T1R-ACL-2025", "hit_ref": "REC7 resolution 4"}],
         "dedup": {"merged_from": ["2401.00002"], "merge_basis": "title_normalized_exact"},
         "screening_stage": "TITLE", "decision": "DUPLICATE",
         "reason_code": "DUPLICATE_OF:2606.05296", "reason_text": "same canonical work",
         "screener": "coordinator", "screened_at": "2026-07-16T00:00:00Z",
         "second_reviewer": None, "adjudicator": None, "adjudication_note": None,
         "fulltext_version_ref": None,
         "extraction": {"rec2_backref": None, "extractor": None, "extracted_at": None},
         "coding_depth": "D0"},
        {"canonical_id": "10.1000/paywalled.1", "title": "Paywalled venue paper",
         "source_hits": [{"source": "route:SF-T1R-ICASSP-2025", "hit_ref": "REC7 resolution 9"}],
         "dedup": {"merged_from": [], "merge_basis": "doi_match"},
         "screening_stage": "ABSTRACT", "decision": "UNOBTAINABLE",
         "reason_code": "REMOVED_PAYWALLED_UNOBTAINABLE",
         "reason_text": "no OA copy; removal registered per flow-report duty",
         "screener": "coordinator", "screened_at": "2026-07-16T00:00:00Z",
         "second_reviewer": None, "adjudicator": None, "adjudication_note": None,
         "fulltext_version_ref": None,
         "extraction": {"rec2_backref": None, "extractor": None, "extracted_at": None},
         "coding_depth": "D0"},
    ]
    claims = [{"claim_id": "CLAIM-1",
               "claim_text": "AMC-type SMC selectors report gains over GRPO on AgentGym",
               "rec2_backref": "REC2-AMC"}]
    flow = {"n_hits": 5, "n_included": 2, "n_excluded": 1, "n_duplicate": 1,
            "n_unobtainable": 1}
    return {"rec0": rec0, "rec2": [rec2_d2, rec2_d1], "claims": claims, "flow_report": flow}


def negatives(pos):
    cases = []

    def case(name, mutate):
        pkg = copy.deepcopy(pos)
        mutate(pkg)
        cases.append((name, pkg))

    case("N01_included_missing_rec2_backref",
         lambda p: p["rec0"][0]["extraction"].update(rec2_backref=""))
    case("N02_excluded_missing_reason_code",
         lambda p: p["rec0"][2].update(reason_code=None))
    case("N03_claim_backref_to_d1_row",
         lambda p: p["claims"][0].update(rec2_backref="REC2-EVOLIB"))
    case("N04_core_row_stuck_at_d1",
         lambda p: p["rec2"][1].update(topic_relevance="core"))
    case("N05_duplicate_canonical_id",
         lambda p: p["rec0"].append(copy.deepcopy(p["rec0"][1])))
    case("N06_na_as_bare_string",
         lambda p: p["rec2"][1].update(rl_identity="NA:no rl claims"))
    case("N07_empty_screener_string",
         lambda p: p["rec0"][0].update(screener=""))
    case("N08_decision_enum_drift",
         lambda p: p["rec0"][2].update(decision="MAYBE"))
    case("N09_flow_report_hand_tallied_mismatch",
         lambda p: p["flow_report"].update(n_included=99))
    case("N10_dangling_rec0_backref",
         lambda p: p["rec2"][1].update(rec0_backref="9999.99999"))
    case("N11_missing_study_quality_dim",
         lambda p: p["rec2"][0]["evidence_axes"]["study_quality"].pop("reproducibility"))
    case("N12_threat_without_dual_coding",
         lambda p: p["rec2"][0].pop("threat_dual_coding"))
    case("N13_included_with_reason_code",
         lambda p: p["rec0"][0].update(reason_code="NOT_RELEVANT"))
    case("N14_unparseable_source",
         lambda p: p["rec0"][1]["source_hits"][0].update(source="somewhere on the web"))
    return cases


def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def write_fixture(name, pkg):
    path = os.path.join(FIXDIR, f"{name}.json")
    with open(path, "wb") as f:
        f.write((json.dumps(pkg, ensure_ascii=False, sort_keys=True, indent=1) + "\n")
                .encode("utf-8"))
    return path


def run_validator(path):
    proc = subprocess.run([sys.executable, VALIDATOR, "--package", path],
                          capture_output=True, text=True, encoding="utf-8")
    return proc.returncode, proc.stdout


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    os.makedirs(FIXDIR, exist_ok=True)
    pos = positive_package()
    results, fixtures = [], {}

    p_path = write_fixture("positive_package", pos)
    fixtures["positive_package"] = sha256_file(p_path)
    rc1, out1 = run_validator(p_path)
    rc2, out2 = run_validator(p_path)
    results.append({"case": "positive_package", "expected_exit": 0, "actual_exit": rc1,
                    "result": "PASS" if rc1 == 0 else "FAIL",
                    "detail": "" if rc1 == 0 else out1[-800:]})
    results.append({"case": "determinism_two_runs_identical", "expected_exit": 0,
                    "actual_exit": rc2,
                    "result": "PASS" if (out1 == out2 and rc1 == rc2) else "FAIL",
                    "detail": ""})

    for name, pkg in negatives(pos):
        path = write_fixture(name, pkg)
        fixtures[name] = sha256_file(path)
        rc, out = run_validator(path)
        first = ""
        try:
            first = json.loads(out)["violations"][0]["rule"] if rc != 0 else ""
        except Exception:  # noqa: BLE001
            first = "unparseable validator output"
        results.append({"case": name, "expected_exit": "nonzero", "actual_exit": rc,
                        "result": "PASS" if rc != 0 else "FAIL",
                        "detail": f"first_violation_rule={first}"})

    n_pass = sum(1 for r in results if r["result"] == "PASS")
    report = {
        "artifact_id": "SF-RECORD-VALIDATOR-TEST-2026-07-16-01",
        "validator": "scripts/survey/sf_record_validator.py",
        "test": "scripts/survey/sf_record_validator_test.py",
        "fixture_dir": "wiki/survey/fixtures-c4a/",
        "fixture_sha256": fixtures,
        "results": results,
        "summary": f"{n_pass}/{len(results)} PASS",
        "verdict": "PASS" if n_pass == len(results) else "FAIL",
        "note": "负例经子进程运行,非零退出在进程级验证;fixtures 全部落盘可查,不藏在测试代码里。",
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "wb") as f:
        f.write((json.dumps(report, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    print(report["summary"], report["verdict"])
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
