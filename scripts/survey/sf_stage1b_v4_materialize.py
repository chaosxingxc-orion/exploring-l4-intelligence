#!/usr/bin/env python3
"""Materialize the bounded Stage-1B v4 speech supplement and control-basis view."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


BASE_PATH = Path("wiki/survey/current/data/stage1b-speech-direct-prior-supplement-v1.json")
RECONCILIATION_PATH = Path("wiki/survey/current/data/stage1b-known-prior-reconciliation-v1.json")
SUPPLEMENT_PATH = Path("wiki/survey/current/data/stage1b-speech-direct-prior-supplement-v2.json")
CONTROL_BASIS_PATH = Path("wiki/survey/current/data/stage1b-direct-control-basis-v1.json")
LEDGER = "wiki/survey/2026-07-17-sf-fulltext-ledger.jsonl"

ALLOWED_CONTROL_BASES = {
    "EXTERNAL_ORCHESTRATION_ONLY",
    "STATE_OR_EVENT_GATED",
    "EVALUATOR_OR_VERIFIER_GATED",
    "REWARD_GUIDED_SELECTION",
    "TRAINED_POLICY_BOUNDARY",
    "MEASUREMENT_ONLY",
}


def _fulltext(paper_id: str, sha256: str) -> dict[str, Any]:
    return {"ledger": LEDGER, "id": paper_id, "kind": "pdf", "sha256": sha256}


ADDITIONAL_SUPPLEMENT_ROWS: dict[str, dict[str, Any]] = {
    "2407.09886": {
        "evidence_id": "DP-2407.09886",
        "paper_work_id": "2407.09886",
        "method_path_id": "2407.09886#program-generated-speech-tool-orchestration",
        "title": "Speech-Copilot: Leveraging Large Language Models for Speech Processing via Task Decomposition, Modularization, and Program Generation",
        "analysis_role": "DIRECT_CONTROL_METHOD",
        "eligible_input_families": ["interactive_full_duplex"],
        "bundle_load_bearing": True,
        "core_topology": "multi_model_federation",
        "core_native_modality": "text_coordinator_over_speech_modules",
        "includes_speech_audio": True,
        "speech_audio_role": "load_bearing_speech_task_input_and_module_output",
        "internal_visibility": "api_only",
        "core_weight_update": False,
        "external_component_weight_update": False,
        "controller_program_or_config_optimized_on_labels": False,
        "signals": [{"signal_id": "program_state", "form": "generated program and module observations", "source": "LLM agent and modular speech tools"}],
        "decision_rights": ["route", "tool_call", "stop"],
        "control_edges": [{"signal_id": "program_state", "signal_use": "execute the next generated speech-tool operation or return the result", "decision_right": "tool_call"}],
        "selection_object": "tool_agent",
        "terminal_operator": "synthesize",
        "stop_repair_semantics": "The generated program terminates after the required speech modules execute; no reward-driven stopping policy is claimed.",
        "load_bearing": True,
        "fulltext_ref": _fulltext("2407.09886", "364044abf7644e32e18ec3606a03da50ff7c61e8dbfd6aadeeb0ee598d483483"),
        "source_locator": "p1 anchor='flexible agent that performs tasks through program generation'",
        "limitation": "Program generation demonstrates orchestration, but it does not establish evaluator- or reward-guided inference control.",
    },
    "2304.12995": {
        "evidence_id": "DP-2304.12995",
        "paper_work_id": "2304.12995",
        "method_path_id": "2304.12995#audio-foundation-model-orchestration",
        "title": "AudioGPT: Understanding and Generating Speech, Music, Sound, and Talking Head",
        "analysis_role": "DIRECT_CONTROL_METHOD",
        "eligible_input_families": ["interactive_full_duplex"],
        "bundle_load_bearing": True,
        "core_topology": "multi_model_federation",
        "core_native_modality": "text_coordinator_over_audio_foundation_models",
        "includes_speech_audio": True,
        "speech_audio_role": "load_bearing_input_output_interface",
        "internal_visibility": "api_only",
        "core_weight_update": False,
        "external_component_weight_update": False,
        "controller_program_or_config_optimized_on_labels": False,
        "signals": [{"signal_id": "task_state", "form": "task plan and model outputs", "source": "ChatGPT coordinator and audio foundation models"}],
        "decision_rights": ["route", "tool_call", "synthesize"],
        "control_edges": [{"signal_id": "task_state", "signal_use": "select an audio model and compose its output", "decision_right": "route"}],
        "selection_object": "tool_agent",
        "terminal_operator": "synthesize",
        "stop_repair_semantics": "The fixed four-stage pipeline ends after response generation; no adaptive reward-guided repair rule is claimed.",
        "load_bearing": True,
        "fulltext_ref": _fulltext("2304.12995", "5bac5d915b43943ff301bb601583821c541fb94e1ed3c4833c1935720ba2296e"),
        "source_locator": "p2 anchor='whole process of AudioGPT can be divided into four stages'",
        "limitation": "The cascade is historically important but depends on external models and does not define a learned or reward-guided controller.",
    },
    "2604.16456": {
        "evidence_id": "DP-2604.16456",
        "paper_work_id": "2604.16456",
        "method_path_id": "2604.16456#measurement-instrument",
        "title": "EchoChain: A Full-Duplex Benchmark for State-Update Reasoning Under Interruptions",
        "analysis_role": "MEASUREMENT_INSTRUMENT",
        "eligible_input_families": ["interactive_full_duplex"],
        "bundle_load_bearing": True,
        "core_topology": "evaluation_harness",
        "core_native_modality": "speech_audio",
        "includes_speech_audio": True,
        "speech_audio_role": "interruption_and_state_update_evaluation_input",
        "internal_visibility": "api_only",
        "core_weight_update": False,
        "external_component_weight_update": False,
        "controller_program_or_config_optimized_on_labels": False,
        "signals": [{"signal_id": "state_update_outcome", "form": "full-duplex and paired half-duplex correctness", "source": "benchmark evaluator"}],
        "decision_rights": [],
        "control_edges": [],
        "selection_object": "none",
        "terminal_operator": "none",
        "stop_repair_semantics": "Measurement instrument only; it measures state revision under interruption.",
        "load_bearing": False,
        "fulltext_ref": _fulltext("2604.16456", "4d0df21eeea17f1567224f5f2fc8b29dce043580a995c76ebc217f10c83156de"),
        "source_locator": "p1 anchor='controlled benchmark for evaluating full-duplex state-update reasoning'",
        "limitation": "No public author code or dataset release was verified, so exact local reproduction remains blocked.",
    },
    "2605.15104": {
        "evidence_id": "DP-2605.15104",
        "paper_work_id": "2605.15104",
        "method_path_id": "2605.15104#measurement-instrument",
        "title": "From Text to Voice: A Reproducible and Verifiable Framework for Evaluating Tool Calling LLM Agents",
        "analysis_role": "MEASUREMENT_INSTRUMENT",
        "eligible_input_families": ["evaluator_reliability", "interactive_full_duplex"],
        "bundle_load_bearing": True,
        "core_topology": "evaluation_harness",
        "core_native_modality": "speech_audio",
        "includes_speech_audio": True,
        "speech_audio_role": "paired_voice_tool_task_input",
        "internal_visibility": "api_only",
        "core_weight_update": False,
        "external_component_weight_update": False,
        "controller_program_or_config_optimized_on_labels": False,
        "signals": [{"signal_id": "gold_tool_outcome", "form": "preserved task annotations and tool-call correctness", "source": "paired text-audio benchmark"}],
        "decision_rights": [],
        "control_edges": [],
        "selection_object": "none",
        "terminal_operator": "none",
        "stop_repair_semantics": "Measurement instrument only; preserved annotations provide verifiable outcomes.",
        "load_bearing": False,
        "fulltext_ref": _fulltext("2605.15104", "e0638bda7ae0dbd8f14f342829c358c1bfb4252558468aad03aaa29a32049e47"),
        "source_locator": "p1 anchor='paired text-audio instances while preserving the original dataset annotations'",
        "limitation": "The released repository supports dataset construction, but the exact generated audio corpus is not packaged as a pinned dataset.",
    },
    "2505.09558": {
        "evidence_id": "DP-2505.09558",
        "paper_work_id": "2505.09558",
        "method_path_id": "2505.09558#trained-reward-measurement-boundary",
        "title": "WavReward: Spoken Dialogue Models With Generalist Reward Evaluators",
        "analysis_role": "MEASUREMENT_INSTRUMENT",
        "eligible_input_families": ["evaluator_reliability"],
        "bundle_load_bearing": True,
        "core_topology": "trained_evaluator",
        "core_native_modality": "speech_audio",
        "includes_speech_audio": True,
        "speech_audio_role": "spoken_dialogue_reward_input",
        "internal_visibility": "api_only",
        "core_weight_update": False,
        "external_component_weight_update": True,
        "controller_program_or_config_optimized_on_labels": False,
        "signals": [{"signal_id": "wavreward_score", "form": "IQ and EQ reward", "source": "trained speech reward evaluator"}],
        "decision_rights": [],
        "control_edges": [],
        "selection_object": "none",
        "terminal_operator": "none",
        "stop_repair_semantics": "Measurement boundary only; the trained reward model does not enter TF-Strict occupancy.",
        "load_bearing": False,
        "fulltext_ref": _fulltext("2505.09558", "3584f57899303eebb4689611077b9bddd65f5617c6affc72a229228b3ac4a599"),
        "source_locator": "p1 anchor='evaluate both the IQ and EQ of spoken dialogue systems with speech input'",
        "limitation": "The evaluator is trained and may inherit preference, artifact and distribution-shift risks.",
    },
    "2603.14889": {
        "evidence_id": "DP-2603.14889",
        "paper_work_id": "2603.14889",
        "method_path_id": "2603.14889#trained-reward-measurement-boundary",
        "title": "SDiaReward: Modeling and Benchmarking Spoken Dialogue Rewards with Modality and Colloquialness",
        "analysis_role": "MEASUREMENT_INSTRUMENT",
        "eligible_input_families": ["evaluator_reliability"],
        "bundle_load_bearing": True,
        "core_topology": "trained_evaluator",
        "core_native_modality": "speech_audio",
        "includes_speech_audio": True,
        "speech_audio_role": "multi_turn_spoken_dialogue_reward_input",
        "internal_visibility": "api_only",
        "core_weight_update": False,
        "external_component_weight_update": True,
        "controller_program_or_config_optimized_on_labels": False,
        "signals": [{"signal_id": "sdiareward_score", "form": "episode-level spoken-dialogue preference reward", "source": "trained reward model"}],
        "decision_rights": [],
        "control_edges": [],
        "selection_object": "none",
        "terminal_operator": "none",
        "stop_repair_semantics": "Measurement boundary only; the trained reward model does not enter TF-Strict occupancy.",
        "load_bearing": False,
        "fulltext_ref": _fulltext("2603.14889", "1e538783eb3f211e6d6b5679f83f21fb1a4eb3c8b6f935f0b8df7fed46205d5a"),
        "source_locator": "p1 anchor='end-to-end multi-turn reward model trained on SDiaReward-Dataset'",
        "limitation": "Preference labels and colloquialness coverage are training-dependent and may not transfer to a selected Stage-1C task.",
    },
    "2602.13891": {
        "evidence_id": "DP-2602.13891",
        "paper_work_id": "2602.13891",
        "method_path_id": "2602.13891#trained-reward-measurement-boundary",
        "title": "GSRM: Generative Speech Reward Model for Speech RLHF",
        "analysis_role": "MEASUREMENT_INSTRUMENT",
        "eligible_input_families": ["evaluator_reliability"],
        "bundle_load_bearing": True,
        "core_topology": "trained_evaluator",
        "core_native_modality": "speech_audio",
        "includes_speech_audio": True,
        "speech_audio_role": "speech_reward_and_naturalness_input",
        "internal_visibility": "api_only",
        "core_weight_update": False,
        "external_component_weight_update": True,
        "controller_program_or_config_optimized_on_labels": False,
        "signals": [{"signal_id": "gsrm_score", "form": "generative reasoning-centric speech reward", "source": "trained reward model and human ratings"}],
        "decision_rights": [],
        "control_edges": [],
        "selection_object": "none",
        "terminal_operator": "none",
        "stop_repair_semantics": "Measurement boundary only; the trained reward model does not enter TF-Strict occupancy.",
        "load_bearing": False,
        "fulltext_ref": _fulltext("2602.13891", "9b5e9e5e747544e70a6c095c251735736304fea7bef38b61774a947653f9840f"),
        "source_locator": "p1 anchor='reasoning-centric reward model tailored for speech'",
        "limitation": "The evaluator is trained on large-scale human ratings and cannot be treated as a training-free control method.",
    },
}


CONTROL_BASIS_BY_ID = {
    "2305.13738": "EXTERNAL_ORCHESTRATION_ONLY",
    "2304.12995": "EXTERNAL_ORCHESTRATION_ONLY",
    "2407.09886": "EXTERNAL_ORCHESTRATION_ONLY",
    "2503.16492": "EXTERNAL_ORCHESTRATION_ONLY",
    "2506.23049": "STATE_OR_EVENT_GATED",
    "2509.16971": "EVALUATOR_OR_VERIFIER_GATED",
    "2509.21749": "STATE_OR_EVENT_GATED",
    "2510.02995": "EXTERNAL_ORCHESTRATION_ONLY",
    "2510.06223": "EXTERNAL_ORCHESTRATION_ONLY",
    "2510.11454": "EXTERNAL_ORCHESTRATION_ONLY",
    "2511.02834": "EXTERNAL_ORCHESTRATION_ONLY",
    "2512.16978": "EVALUATOR_OR_VERIFIER_GATED",
    "2512.23646": "STATE_OR_EVENT_GATED",
    "2601.20230": "STATE_OR_EVENT_GATED",
    "2602.10656": "STATE_OR_EVENT_GATED",
    "2603.02206": "STATE_OR_EVENT_GATED",
    "2603.05413": "EXTERNAL_ORCHESTRATION_ONLY",
    "2603.21013": "STATE_OR_EVENT_GATED",
    "2604.09121": "EVALUATOR_OR_VERIFIER_GATED",
    "2605.28192": "STATE_OR_EVENT_GATED",
    "2605.28480": "STATE_OR_EVENT_GATED",
    "2605.29430": "EVALUATOR_OR_VERIFIER_GATED",
    "2606.07264": "EVALUATOR_OR_VERIFIER_GATED",
    "2606.15141": "EVALUATOR_OR_VERIFIER_GATED",
    "2607.11433": "EVALUATOR_OR_VERIFIER_GATED",
}


def build_supplement(base: dict[str, Any], reconciliation: dict[str, Any]) -> dict[str, Any]:
    included = {
        row["paper_work_id"]
        for row in reconciliation["rows"]
        if row["supplement_status"] == "INCLUDED"
    }
    if included != set(ADDITIONAL_SUPPLEMENT_ROWS):
        raise ValueError("reconciliation INCLUDED set does not match bounded v4 additions")
    rows = [*base["rows"], *(ADDITIONAL_SUPPLEMENT_ROWS[paper_id] for paper_id in sorted(included))]
    ids = [row["paper_work_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate paper_work_id in v4 supplement")
    return {
        **{key: value for key, value in base.items() if key != "rows"},
        "schema": "sf-stage1b-speech-direct-prior-supplement-v2",
        "artifact_id": "SF-STAGE1B-SPEECH-DIRECT-PRIOR-SUPPLEMENT-V2",
        "reconciliation_ref": RECONCILIATION_PATH.as_posix(),
        "rows": rows,
    }


def build_control_basis(supplement: dict[str, Any]) -> dict[str, Any]:
    direct_rows = [
        row for row in supplement["rows"] if row["analysis_role"] == "DIRECT_CONTROL_METHOD"
    ]
    direct_ids = {row["paper_work_id"] for row in direct_rows}
    missing = sorted(direct_ids - set(CONTROL_BASIS_BY_ID))
    extra = sorted(set(CONTROL_BASIS_BY_ID) - direct_ids)
    if missing:
        raise ValueError(f"missing control_basis for: {', '.join(missing)}")
    if extra:
        raise ValueError(f"control_basis has non-direct rows: {', '.join(extra)}")
    rows = []
    for source in sorted(direct_rows, key=lambda row: row["paper_work_id"]):
        signals = source["signals"]
        rows.append(
            {
                "paper_work_id": source["paper_work_id"],
                "evidence_id": source["evidence_id"],
                "control_basis": CONTROL_BASIS_BY_ID[source["paper_work_id"]],
                "reward_or_evaluator_identity": [signal["source"] for signal in signals],
                "signal_forms": [signal["form"] for signal in signals],
                "signal_changes_next_action": bool(source["control_edges"]),
                "next_action_effect": source["decision_rights"],
                "controller_program_or_config_optimized_on_labels": source[
                    "controller_program_or_config_optimized_on_labels"
                ],
                "core_weight_update": source["core_weight_update"],
                "external_component_weight_update": source["external_component_weight_update"],
                "boundary_note": (
                    "Classification describes the load-bearing inference path only; "
                    "DIRECT_CONTROL_METHOD does not imply reward-guided selection."
                ),
            }
        )
    return {
        "schema": "sf-stage1b-direct-control-basis-v1",
        "artifact_id": "SF-STAGE1B-DIRECT-CONTROL-BASIS-V1",
        "source_supplement": SUPPLEMENT_PATH.as_posix(),
        "classification_axis": sorted(ALLOWED_CONTROL_BASES),
        "claim_limit": "A control-basis class is a mechanism-path description, not a novelty or effectiveness verdict.",
        "rows": rows,
    }


def _write_json(path: Path, document: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    repo = Path(__file__).resolve().parents[2]
    base = json.loads((repo / BASE_PATH).read_text(encoding="utf-8"))
    reconciliation = json.loads((repo / RECONCILIATION_PATH).read_text(encoding="utf-8"))
    supplement = build_supplement(base, reconciliation)
    control_basis = build_control_basis(supplement)
    _write_json(repo / SUPPLEMENT_PATH, supplement)
    _write_json(repo / CONTROL_BASIS_PATH, control_basis)
    print(f"wrote {SUPPLEMENT_PATH} ({len(supplement['rows'])} rows)")
    print(f"wrote {CONTROL_BASIS_PATH} ({len(control_basis['rows'])} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
