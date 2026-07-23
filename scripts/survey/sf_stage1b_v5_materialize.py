#!/usr/bin/env python3
"""Materialize the closed Stage-1B v5 corpus-to-current reconciliation."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
CORPUS_PATH = Path("wiki/survey/current/data/existing-corpus-disposition-v1.json")
RECEIPTS_PATH = Path("wiki/survey/current/data/official-metadata-receipts-v1.jsonl")
LEDGER_PATH = Path("wiki/survey/2026-07-17-sf-fulltext-ledger.jsonl")
BASE_SUPPLEMENT_PATH = Path("wiki/survey/current/data/stage1b-speech-direct-prior-supplement-v2.json")
BASE_CONTROL_PATH = Path("wiki/survey/current/data/stage1b-direct-control-basis-v1.json")
KNOWN_RECONCILIATION_PATH = Path("wiki/survey/current/data/stage1b-known-prior-reconciliation-v1.json")
PREVIOUS_APPENDIX_PATH = Path("wiki/survey/current/stage1b-transition-reference-appendix.md")
RECONCILIATION_PATH = Path("wiki/survey/current/data/stage1b-eligible-bundle-reconciliation-v1.json")
SUPPLEMENT_PATH = Path("wiki/survey/current/data/stage1b-speech-direct-prior-supplement-v3.json")
CONTROL_PATH = Path("wiki/survey/current/data/stage1b-direct-control-basis-v2.json")
APPENDIX_PATH = PREVIOUS_APPENDIX_PATH

REVIEW_PATH = (
    "wiki/audit/system-first-stage1b/stage1c-transition-rereview-v4-independent-review/"
    "2026-07-23-stage1b-v4-independent-doctoral-rereview.md"
)
GATE_IDS = {
    "2506.05984",
    "2507.12705",
    "2601.04029",
    "2605.23261",
    "2605.30256",
    "2606.24648",
}
NAMED_ROUTE_IDS = {
    "2306.12577",
    "2410.21485",
    "2411.00321",
    "2510.00743",
    "2510.14664",
    "2511.07931",
    "2512.10403",
    "2603.09714",
    "2603.19615",
}
SAME_LANE_CLOSURE_IDS = {"2512.10170", "2603.12520", "2604.24278"}
CLOSED_RECONCILIATION_IDS = GATE_IDS | NAMED_ROUTE_IDS | SAME_LANE_CLOSURE_IDS
ASSET_STATUSES = {"PAPER_FULLTEXT_LOCAL"}
GATE_ASSET_DETAILS = {
    "2507.12705": {
        "code_data_status": "NO_DEDICATED_PUBLIC_RELEASE_VERIFIED; PAPER_USES_EXISTING_DATASETS",
        "exact_asset_ref": None,
    },
    "2506.05984": {
        "code_data_status": "STYLESET_ANNOUNCED_FOR_MIT_RELEASE_NO_VERIFIED_ENDPOINT",
        "exact_asset_ref": "docs/stage1b-v5-gate-assets.lock.json#audio-aware-styleset",
    },
    "2601.04029": {
        "code_data_status": "PINNED_REPOSITORY_IS_PROJECT_PAGE_ONLY; CLAIMED_CODE_DATA_NOT_PRESENT",
        "exact_asset_ref": "docs/stage1b-v5-gate-assets.lock.json#speakersleuth",
    },
    "2606.24648": {
        "code_data_status": "PUBLIC_REPO_AND_THREE_BENCHMARK_METADATA_ROUTES_PINNED; SVC_AUDIO_MANUAL_REVIEW_REQUIRED",
        "exact_asset_ref": "docs/stage1b-v5-gate-assets.lock.json#parapair-audio-bench",
    },
    "2605.23261": {
        "code_data_status": "PUBLIC_REPO_AND_UNISRM_BENCH_REVISION_PINNED",
        "exact_asset_ref": "docs/stage1b-v5-gate-assets.lock.json#unisrm-bench",
    },
    "2605.30256": {
        "code_data_status": "TERMS_ACCEPTANCE_AND_ACCESS_PASSWORD_REQUIRED; NOT_DOWNLOADED",
        "exact_asset_ref": "docs/stage1b-v5-gate-assets.lock.json#videofdb-evaluation-data",
    },
}

DECISIONS: dict[str, dict[str, Any]] = {
    "2507.12705": {
        "analysis_role": "MEASUREMENT_INSTRUMENT",
        "control_basis": "PROMPTED_FROZEN_JUDGE_NO_NEXT_ACTION",
        "bundle_impacts": ["evaluator_reward_reliability"],
        "route_reason": "Prompted frozen audio judges expose pairwise-versus-pointwise reliability plus position and verbosity bias; no judge score is wired to a next action here.",
        "source_locator": "abstract and full text: pairwise evaluation is more reliable than pointwise scoring",
    },
    "2506.05984": {
        "analysis_role": "MEASUREMENT_INSTRUMENT",
        "control_basis": "PROMPTED_FROZEN_JUDGE_NO_NEXT_ACTION",
        "bundle_impacts": ["evaluator_reward_reliability"],
        "route_reason": "Human-machine agreement on speaking style supplies a paralinguistic judge axis absent from the prior current layer.",
        "source_locator": "abstract: audio-aware LLMs judge speaking styles and role-playing speech",
    },
    "2601.04029": {
        "analysis_role": "MEASUREMENT_INSTRUMENT",
        "control_basis": "PROMPTED_FROZEN_JUDGE_NO_NEXT_ACTION",
        "bundle_impacts": ["evaluator_reward_reliability"],
        "route_reason": "Multi-turn speaker consistency and K-variant discrimination expose text-over-acoustics bias in frozen LALM judges.",
        "source_locator": "full text: Discrimination task uses K=3 acoustic variants",
    },
    "2606.24648": {
        "analysis_role": "MEASUREMENT_INSTRUMENT",
        "control_basis": "BENCHMARK_INSTRUMENT_NO_NEXT_ACTION",
        "bundle_impacts": ["evaluator_reward_reliability"],
        "route_reason": "Pairwise and tie cases directly constrain calibration and abstention assumptions for audio judges.",
        "source_locator": "abstract: 5,175 pairs, five paralinguistic dimensions, and severe Tie-case calibration failures",
    },
    "2605.23261": {
        "analysis_role": "MEASUREMENT_INSTRUMENT",
        "control_basis": "TRAINED_REWARD_MODEL_NO_NEXT_ACTION",
        "bundle_impacts": ["evaluator_reward_reliability"],
        "route_reason": "UniSRM is a trained multidimensional speech-reward boundary; prior omission came from promotion loss, not a relevance exclusion.",
        "source_locator": "abstract: unified multidimensional speech reward modeling and reasoning consistency",
    },
    "2605.30256": {
        "analysis_role": "BOUNDARY_COMPARATOR",
        "control_basis": "MULTIMODAL_BENCHMARK_NO_NEXT_ACTION",
        "bundle_impacts": ["interactive_full_duplex"],
        "route_reason": "VideoFDB supplies the AV2AV full-duplex boundary while operational Stage-1 scope remains speech/audio/text/tool plus this explicit visual comparator.",
        "source_locator": "abstract: full-duplex audio-visual-to-audio-visual benchmark",
    },
    "2511.07931": {
        "analysis_role": "MEASUREMENT_INSTRUMENT",
        "control_basis": "TRAINED_REWARD_MODEL_NO_NEXT_ACTION",
        "bundle_impacts": ["evaluator_reward_reliability"],
        "route_reason": "SpeechJudge provides a trained naturalness preference benchmark and reward-model boundary, not a frozen direct controller.",
        "source_locator": "abstract: SpeechJudge-Data, SpeechJudge-Eval, and trained SpeechJudge-GRM",
    },
    "2510.14664": {
        "analysis_role": "MEASUREMENT_INSTRUMENT",
        "control_basis": "TRAINED_REWARD_MODEL_NO_NEXT_ACTION",
        "bundle_impacts": ["evaluator_reward_reliability"],
        "route_reason": "SpeechLLM-as-Judges supplies structured speech-quality evaluation and a trained judge boundary.",
        "source_locator": "abstract: quality, pairwise comparison, improvement suggestion, and deepfake detection",
    },
    "2510.00743": {
        "analysis_role": "MEASUREMENT_INSTRUMENT",
        "control_basis": "TRAINED_REWARD_MODEL_NO_NEXT_ACTION",
        "bundle_impacts": ["evaluator_reward_reliability"],
        "route_reason": "MOS-RMBench turns scalar scores into preference comparisons and exposes small-difference failure for speech reward models.",
        "source_locator": "abstract: scalar, semi-scalar, and generative reward models on MOS-RMBench",
    },
    "2306.12577": {
        "analysis_role": "MEASUREMENT_INSTRUMENT",
        "control_basis": "TRAINED_QUALITY_METRIC_NO_NEXT_ACTION",
        "bundle_impacts": ["evaluator_reward_reliability", "budget_stop_repair"],
        "route_reason": "NoRefER is a trained reference-free ASR quality metric and reranking boundary; it is not a frozen audio-native judge.",
        "source_locator": "abstract: referenceless ASR quality metric with contrastive learning",
    },
    "2410.21485": {
        "analysis_role": "MEASUREMENT_INSTRUMENT",
        "control_basis": "TRAINED_QUALITY_METRIC_NO_NEXT_ACTION",
        "bundle_impacts": ["evaluator_reward_reliability"],
        "route_reason": "SpeechQE provides audio-grounded direct-speech-translation quality estimation but does not itself implement selection.",
        "source_locator": "abstract: estimating quality of direct speech translation",
    },
    "2411.00321": {
        "analysis_role": "MEASUREMENT_INSTRUMENT",
        "control_basis": "FROZEN_AUDIO_TEXT_METRIC_NO_NEXT_ACTION",
        "bundle_impacts": ["evaluator_reward_reliability"],
        "route_reason": "MACE uses audio in reference-free caption evaluation and supplies a metric boundary rather than an action controller.",
        "source_locator": "abstract: leveraging audio for evaluating audio captioning systems",
    },
    "2512.10403": {
        "analysis_role": "MEASUREMENT_INSTRUMENT",
        "control_basis": "BENCHMARK_INSTRUMENT_NO_NEXT_ACTION",
        "bundle_impacts": ["evaluator_reward_reliability"],
        "route_reason": "BRACE is the robust audio-caption quality benchmark needed to audit reference-free metric behavior.",
        "source_locator": "abstract: benchmark for robust audio caption quality evaluation",
    },
    "2603.19615": {
        "analysis_role": "MEASUREMENT_INSTRUMENT",
        "control_basis": "FROZEN_AUDIO_TEXT_METRIC_NO_NEXT_ACTION",
        "bundle_impacts": ["evaluator_reward_reliability"],
        "route_reason": "CAF-Score calibrates frozen CLAP with LALM judgments for reference-free caption evaluation; it remains a metric path.",
        "source_locator": "abstract: calibrating CLAP with LALMs for reference-free evaluation",
    },
    "2603.09714": {
        "analysis_role": "DIRECT_CONTROL_METHOD",
        "control_basis": "EVALUATOR_OR_VERIFIER_GATED",
        "bundle_impacts": ["budget_stop_repair", "evaluator_reward_reliability"],
        "route_reason": "MUGEN's training-free audio-permutational self-consistency aggregates K reordered inferences to change the final answer, so it enters direct occupancy without becoming reward-guided selection.",
        "source_locator": "full text: K=10 Audio-Permutational Self-Consistency aggregation",
    },
    "2512.10170": {
        "analysis_role": "MEASUREMENT_INSTRUMENT",
        "control_basis": "CALIBRATION_METHOD_NO_NEXT_ACTION",
        "bundle_impacts": ["evaluator_reward_reliability"],
        "route_reason": "Semantic-aware confidence calibration is a same-lane captioning reliability comparator retained to prevent silent queue loss.",
        "source_locator": "abstract: semantic-aware confidence calibration for automated audio captioning",
    },
    "2603.12520": {
        "analysis_role": "BOUNDARY_COMPARATOR",
        "control_basis": "DECISION_UTILITY_DIAGNOSTIC_NO_NEXT_ACTION",
        "bundle_impacts": ["evaluator_reward_reliability", "budget_stop_repair"],
        "route_reason": "This diagnostic separates attractive judge scores from Best-of-N decision utility and blocks correlation-to-control inference.",
        "source_locator": "abstract: judge scores can look good while Best-of-N decisions fail",
    },
    "2604.24278": {
        "analysis_role": "MEASUREMENT_INSTRUMENT",
        "control_basis": "RELIABILITY_METRIC_NO_NEXT_ACTION",
        "bundle_impacts": ["evaluator_reward_reliability"],
        "route_reason": "RAS is a same-lane ASR reliability metric retained as an explicit measurement route rather than a controller.",
        "source_locator": "abstract: reliability-oriented metric for automatic speech recognition",
    },
}


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_inputs(repo: Path = REPO) -> dict[str, Any]:
    return {
        "corpus": _load_json(repo / CORPUS_PATH),
        "receipts": _load_jsonl(repo / RECEIPTS_PATH),
        "ledger": _load_jsonl(repo / LEDGER_PATH),
        "base_supplement": _load_json(repo / BASE_SUPPLEMENT_PATH),
        "base_control": _load_json(repo / BASE_CONTROL_PATH),
        "known_reconciliation": _load_json(repo / KNOWN_RECONCILIATION_PATH),
    }


def _canonical_by_arxiv(corpus: dict[str, Any]) -> dict[str, str]:
    result = {}
    for node in corpus["canonical_work_nodes"]:
        for identity in node.get("identities", []):
            source_id = str(identity.get("source_id", ""))
            if re.fullmatch(r"\d{4}\.\d{4,5}", source_id):
                result[source_id] = node["canonical_work_id"]
    return result


def _successful_pdfs(ledger: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    rows = {}
    for event in ledger:
        if (
            event.get("kind") == "pdf"
            and event.get("http_status") == 200
            and event.get("error") is None
            and event.get("sha256")
            and event.get("stored_at")
        ):
            rows[str(event["arxiv_id"])] = event
    return rows


def build_reconciliation(inputs: dict[str, Any]) -> dict[str, Any]:
    if set(DECISIONS) != CLOSED_RECONCILIATION_IDS:
        raise ValueError("decision table does not match the closed reconciliation identity set")
    receipts = {row["identity"]["id"]: row for row in inputs["receipts"]}
    pdfs = _successful_pdfs(inputs["ledger"])
    canonical = _canonical_by_arxiv(inputs["corpus"])
    rows = []
    for paper_id in sorted(CLOSED_RECONCILIATION_IDS):
        if paper_id not in receipts:
            raise ValueError(f"official metadata receipt missing: {paper_id}")
        if paper_id not in pdfs:
            raise ValueError(f"local PDF ledger success missing: {paper_id}")
        receipt = receipts[paper_id]
        event = pdfs[paper_id]
        decision = DECISIONS[paper_id]
        rows.append(
            {
                "paper_work_id": paper_id,
                "canonical_work_id": canonical.get(paper_id, f"CW-ARXIV-{paper_id}"),
                "canonical_union_status": (
                    "REUSED_EXISTING_CANONICAL_ID"
                    if paper_id in canonical
                    else "REVIEWER_DIRECTED_OUTSIDE_UNION_IDENTITY"
                ),
                "gate_work": paper_id in GATE_IDS,
                "selection_source": (
                    "REVIEW_GATE_SET"
                    if paper_id in GATE_IDS
                    else "REVIEW_NAMED_ROUTE_SET"
                    if paper_id in NAMED_ROUTE_IDS
                    else "CANONICAL_SAME_LANE_CLOSURE"
                ),
                "official_metadata": receipt["normalized"],
                "analysis_role": decision["analysis_role"],
                "control_basis": decision["control_basis"],
                "bundle_impacts": decision["bundle_impacts"],
                "supplement_status": (
                    "INCLUDED" if paper_id in GATE_IDS or paper_id == "2603.09714" else "ROUTED_ONLY"
                ),
                "route_reason": decision["route_reason"],
                "source_locator": decision["source_locator"],
                "asset_availability": {
                    "status": "PAPER_FULLTEXT_LOCAL",
                    "pdf_and_eprint_requested": True,
                    **GATE_ASSET_DETAILS.get(
                        paper_id,
                        {
                            "code_data_status": "NOT_PINNED_BY_THIS_LITERATURE_GATE",
                            "exact_asset_ref": None,
                        },
                    ),
                    "stage1c_effect": "NONBLOCKING_FOR_LITERATURE_COMPARISON; NO_STAGE2_EXECUTION_AUTHORITY",
                },
                "fulltext_ref": {
                    "ledger": LEDGER_PATH.as_posix(),
                    "id": paper_id,
                    "kind": "pdf",
                    "bytes": event["bytes"],
                    "sha256": event["sha256"],
                    "stored_at": event["stored_at"],
                },
                "seed_action": "REUSE_CANONICAL_WORK_ID_NO_DUPLICATE_CLAIM_WORK",
            }
        )
    return {
        "schema": "sf-stage1b-eligible-bundle-reconciliation-v1",
        "artifact_id": "SF-STAGE1B-ELIGIBLE-BUNDLE-RECONCILIATION-V1",
        "scope": "CLOSED_6_GATE_PLUS_12_ROUTE_CORPUS_TO_CURRENT_RECONCILIATION",
        "source_surfaces": [
            CORPUS_PATH.as_posix(),
            "wiki/survey/replay/SURVEY-RESP-2026-07-14-01/search_events.jsonl",
            REVIEW_PATH,
        ],
        "closure_rule": "Six reviewer gate identities, nine reviewer-named route identities, and three same-lane canonical reliability/decision-utility identities; no discovery query expansion.",
        "claim_limit": "Route closure for Stage-1C inputs, not literature-universe closure, novelty, effectiveness, or reproduction evidence.",
        "rows": rows,
    }


def _measurement_row(row: dict[str, Any]) -> dict[str, Any]:
    paper_id = row["paper_work_id"]
    return {
        "evidence_id": f"DP-{paper_id}",
        "paper_work_id": paper_id,
        "method_path_id": f"{paper_id}#measurement-or-boundary",
        "title": row["official_metadata"]["title"],
        "analysis_role": row["analysis_role"],
        "eligible_input_families": row["bundle_impacts"],
        "bundle_load_bearing": True,
        "core_topology": "evaluation_harness",
        "core_native_modality": "audio_visual" if paper_id == "2605.30256" else "speech_audio",
        "includes_speech_audio": True,
        "speech_audio_role": "measurement_or_reward_input",
        "internal_visibility": "api_only",
        "core_weight_update": False,
        "external_component_weight_update": row["control_basis"].startswith("TRAINED_"),
        "controller_program_or_config_optimized_on_labels": False,
        "signals": [
            {
                "signal_id": "reported_measurement",
                "form": row["control_basis"],
                "source": row["official_metadata"]["title"],
            }
        ],
        "decision_rights": [],
        "control_edges": [],
        "selection_object": "none",
        "terminal_operator": "none",
        "stop_repair_semantics": "Measurement or boundary route only; no evaluator output is connected to a next action in this coded path.",
        "load_bearing": False,
        "fulltext_ref": row["fulltext_ref"],
        "source_locator": row["source_locator"],
        "limitation": row["route_reason"],
    }


def _mugen_row(row: dict[str, Any]) -> dict[str, Any]:
    paper_id = row["paper_work_id"]
    return {
        "evidence_id": f"DP-{paper_id}",
        "paper_work_id": paper_id,
        "method_path_id": f"{paper_id}#audio-permutational-self-consistency",
        "title": row["official_metadata"]["title"],
        "analysis_role": "DIRECT_CONTROL_METHOD",
        "eligible_input_families": row["bundle_impacts"],
        "bundle_load_bearing": True,
        "core_topology": "single_core_multi_call",
        "core_native_modality": "audio_language_model",
        "includes_speech_audio": True,
        "speech_audio_role": "load_bearing_multi_audio_input",
        "internal_visibility": "api_only",
        "core_weight_update": False,
        "external_component_weight_update": False,
        "controller_program_or_config_optimized_on_labels": False,
        "signals": [
            {
                "signal_id": "apsc_consensus",
                "form": "agreement over answers from K audio-order permutations",
                "source": "frozen LALM multi-call outputs",
            }
        ],
        "decision_rights": ["select", "stop"],
        "control_edges": [
            {
                "signal_id": "apsc_consensus",
                "signal_use": "aggregate permuted inferences and select the final answer",
                "decision_right": "select",
            }
        ],
        "selection_object": "candidate_answer",
        "terminal_operator": "majority_vote",
        "stop_repair_semantics": "The fixed K=10 permutation budget ends in consensus aggregation; no adaptive reward threshold is claimed.",
        "load_bearing": True,
        "fulltext_ref": row["fulltext_ref"],
        "source_locator": row["source_locator"],
        "limitation": "Consensus may amplify correlated lexical or order biases and is not evidence of calibrated reward-guided control.",
    }


def build_supplement(base: dict[str, Any], reconciliation: dict[str, Any]) -> dict[str, Any]:
    included = [row for row in reconciliation["rows"] if row["supplement_status"] == "INCLUDED"]
    if {row["paper_work_id"] for row in included} != GATE_IDS | {"2603.09714"}:
        raise ValueError("supplement inclusion does not match the v5 closed decision")
    additions = [
        _mugen_row(row) if row["paper_work_id"] == "2603.09714" else _measurement_row(row)
        for row in included
    ]
    rows = [*base["rows"], *sorted(additions, key=lambda row: row["paper_work_id"])]
    ids = [row["paper_work_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate paper_work_id in v5 supplement")
    return {
        **{key: value for key, value in base.items() if key != "rows"},
        "schema": "sf-stage1b-speech-direct-prior-supplement-v3",
        "artifact_id": "SF-STAGE1B-SPEECH-DIRECT-PRIOR-SUPPLEMENT-V3",
        "reconciliation_ref": RECONCILIATION_PATH.as_posix(),
        "coverage_limit": "46 routed rows support bounded Stage-1C inputs; only DIRECT_CONTROL_METHOD rows enter occupancy.",
        "rows": rows,
    }


def build_control_basis(supplement: dict[str, Any], base: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for source in base["rows"]:
        row = dict(source)
        row["control_signal_or_decision_component_identity"] = row.pop("reward_or_evaluator_identity")
        rows.append(row)
    rows.append(
        {
            "paper_work_id": "2603.09714",
            "evidence_id": "DP-2603.09714",
            "control_basis": "EVALUATOR_OR_VERIFIER_GATED",
            "control_signal_or_decision_component_identity": ["audio-permutational self-consistency consensus"],
            "signal_forms": ["agreement over K=10 reordered-audio inferences"],
            "signal_changes_next_action": True,
            "next_action_effect": ["select", "stop"],
            "controller_program_or_config_optimized_on_labels": False,
            "core_weight_update": False,
            "external_component_weight_update": False,
            "boundary_note": "Consensus changes the final answer, but it is not a scalar reward and does not establish calibrated selection utility.",
        }
    )
    direct_ids = {
        row["paper_work_id"] for row in supplement["rows"] if row["analysis_role"] == "DIRECT_CONTROL_METHOD"
    }
    if direct_ids != {row["paper_work_id"] for row in rows}:
        raise ValueError("control-basis rows do not cover direct supplement occupancy exactly")
    summary = {
        name: sum(row["control_basis"] == name for row in rows)
        for name in (
            "EXTERNAL_ORCHESTRATION_ONLY",
            "STATE_OR_EVENT_GATED",
            "EVALUATOR_OR_VERIFIER_GATED",
        )
    }
    summary["REWARD_GUIDED_SELECTION"] = 0
    return {
        "schema": "sf-stage1b-direct-control-basis-v2",
        "artifact_id": "SF-STAGE1B-DIRECT-CONTROL-BASIS-V2",
        "source_supplement": SUPPLEMENT_PATH.as_posix(),
        "field_migration": "reward_or_evaluator_identity renamed to control_signal_or_decision_component_identity because orchestration components need not be rewards or evaluators.",
        "claim_limit": "Mechanism-path occupancy only; no novelty, effectiveness, or reward-guided verdict follows from direct-control status.",
        "summary": summary,
        "rows": sorted(rows, key=lambda row: row["paper_work_id"]),
    }


def _receipt_map() -> dict[str, dict[str, Any]]:
    return {row["identity"]["id"]: row for row in _load_jsonl(REPO / RECEIPTS_PATH)}


def _role_label(role: str) -> str:
    return role.replace("_", " ").title()


def _appendix_row(row: dict[str, Any], metadata: dict[str, Any], route: str) -> str:
    paper_id = row["paper_work_id"]
    evidence_id = row.get("evidence_id", f"ROUTE-{paper_id}")
    authors = metadata["authors"]
    author_label = authors[0] + (" et al." if len(authors) > 1 else "")
    return (
        f"| <!-- work:{paper_id} -->{evidence_id} | {metadata['title']} | "
        f"{author_label}, {metadata['year']} | [arXiv]({metadata['stable_url']}) | "
        f"{_role_label(row['analysis_role'])} | `{route}` |"
    )


def render_reference_appendix(
    supplement: dict[str, Any],
    known_reconciliation: dict[str, Any],
    reconciliation: dict[str, Any],
) -> str:
    receipts = _receipt_map()
    new_by_id = {row["paper_work_id"]: row for row in reconciliation["rows"]}
    lines = [
        "---",
        'artifact_id: "SF-STAGE1B-TRANSITION-REFERENCE-APPENDIX-V3"',
        'scope: "46 supplement rows plus 13 routed-only reconciliation rows"',
        'novelty_verdict: "NOT_PERMITTED_IN_STAGE_1B"',
        "---",
        "",
        "# Stage-1B transition reference appendix",
        "",
        "Every row is a route, not an effectiveness or novelty verdict. Prompted frozen judges, trained reward models, benchmarks/metrics and direct evaluator-to-action controllers remain distinct. Paper-reported correlation, accuracy or ranking is not treated as selection utility. Local hash locators bind the newly reconciled works; no paper result has been reproduced by this project.",
        "",
        "| Evidence ID | Work | Authors / year | Stable link | Analysis role | Evidence route |",
        "|---|---|---|---|---|---|",
    ]
    emitted = set()
    for row in supplement["rows"]:
        paper_id = row["paper_work_id"]
        if paper_id in new_by_id:
            source = new_by_id[paper_id]
            route = f"{source['source_locator']}; sha256:{source['fulltext_ref']['sha256']}"
            lines.append(_appendix_row(row, source["official_metadata"], route))
        else:
            metadata = receipts[paper_id]["normalized"]
            lines.append(_appendix_row(row, metadata, row["source_locator"]))
        emitted.add(paper_id)
    for source in [*known_reconciliation["rows"], *reconciliation["rows"]]:
        paper_id = source["paper_work_id"]
        if paper_id in emitted:
            continue
        metadata = (
            source["official_metadata"]
            if "official_metadata" in source
            else receipts[paper_id]["normalized"]
        )
        route = source["route_reason"]
        if "fulltext_ref" in source:
            route += f"; sha256:{source['fulltext_ref']['sha256']}"
        lines.append(_appendix_row(source, metadata, route))
        emitted.add(paper_id)
    lines.extend(
        [
            "",
            f"Unique routed works: {len(emitted)}. Direct-control occupancy: 26. Reward-guided selection occupancy: 0.",
            "",
            "The original four-source 81-work audit, this 18-work closed promotion repair and the 46-row supplement retain different denominators. None is a claim of literature-universe closure.",
            "",
        ]
    )
    return "\n".join(lines)


def resolve_local_pdf(repo: Path, fulltext_ref: dict[str, Any]) -> Path:
    stored = str(fulltext_ref["stored_at"]).replace("\\", "/")
    marker = "/speechrl-data/"
    root_value = os.environ.get(
        "SPEECHRL_DATA_DIR",
        "/mnt/e/chao_workspace/exploring-l4-intelligence/speechrl-data",
    )
    if marker in stored:
        return Path(root_value) / stored.split(marker, 1)[1]
    return Path(stored)


def _write_json(path: Path, document: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    inputs = load_inputs(REPO)
    reconciliation = build_reconciliation(inputs)
    supplement = build_supplement(inputs["base_supplement"], reconciliation)
    control = build_control_basis(supplement, inputs["base_control"])
    appendix = render_reference_appendix(supplement, inputs["known_reconciliation"], reconciliation)
    outputs = {
        RECONCILIATION_PATH: json.dumps(reconciliation, indent=2, ensure_ascii=False) + "\n",
        SUPPLEMENT_PATH: json.dumps(supplement, indent=2, ensure_ascii=False) + "\n",
        CONTROL_PATH: json.dumps(control, indent=2, ensure_ascii=False) + "\n",
        APPENDIX_PATH: appendix,
    }
    if args.check:
        drift = [path.as_posix() for path, content in outputs.items() if not (REPO / path).is_file() or (REPO / path).read_text(encoding="utf-8") != content]
        if drift:
            print(json.dumps({"verdict": "FAIL", "drift": drift}, indent=2))
            return 1
        print("PASS v5 corpus-to-current materialization is deterministic")
        return 0
    for path, content in outputs.items():
        target = REPO / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")
        print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
