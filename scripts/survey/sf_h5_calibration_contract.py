#!/usr/bin/env python3
"""Validate the frozen three-paper, seven-field H5 calibration artifact."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CALIBRATION_PATH = (
    ROOT / "wiki/survey/current/data/modality-specificity-calibration-v1.json"
)
LEDGER_PATH = ROOT / "wiki/survey/2026-07-17-sf-fulltext-ledger.jsonl"
CODEBOOK_PATH = "wiki/survey/current/modality-specificity-codebook.md"
CALIBRATION_PAPER_IDS = ("2510.02995", "2509.19676", "2606.19341")

FIELD_VALUES = {
    "modality_topology": {
        "text_only", "audio_native_single", "audio_native_multi",
        "omni_native_joint", "asr_then_text", "text_then_tts",
        "multimodal_parallel", "mixed", "UNKNOWN", "NOT_APPLICABLE",
    },
    "temporal_regime": {
        "offline_batch", "turn_based", "streaming_unidirectional",
        "streaming_duplex", "event_driven_async", "mixed", "UNKNOWN",
        "NOT_APPLICABLE",
    },
    "observation_granularity": {
        "whole_clip", "utterance", "turn", "segment_or_chunk",
        "frame_or_audio_token", "tool_or_environment_event", "trajectory",
        "mixed", "UNKNOWN", "NOT_APPLICABLE",
    },
    "acoustic_evidence_provenance": {
        "raw_waveform", "learned_audio_representation",
        "task_provided_audio_tool_readout", "transcript_only", "metadata_only",
        "external_new_audio", "mixed", "UNKNOWN", "NOT_APPLICABLE",
    },
    "latency_action_timing": {
        "pre_inference", "intra_utterance_online", "post_utterance",
        "inter_turn", "post_trajectory", "asynchronous", "mixed", "UNKNOWN",
        "NOT_APPLICABLE",
    },
    "output_action_modality": {
        "text", "speech", "non_speech_audio", "multimodal_content",
        "tool_action", "environment_action", "composite", "UNKNOWN",
        "NOT_APPLICABLE",
    },
    "state_persistence": {
        "stateless", "within_utterance", "within_turn", "cross_turn_session",
        "cross_session_external", "environment_persistent", "mixed", "UNKNOWN",
        "NOT_APPLICABLE",
    },
}


def load_calibration(path: Path = CALIBRATION_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _ledger_index() -> dict[tuple[str, str], dict[str, Any]]:
    rows = {}
    for line in LEDGER_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        key = (row.get("arxiv_id"), row.get("kind"))
        if key[0] in CALIBRATION_PAPER_IDS and row.get("http_status") == 200:
            rows[key] = row
    return rows


def validate_structure(document: dict[str, Any]) -> list[str]:
    failures: set[str] = set()
    if document.get("schema") != "sf-modality-specificity-calibration-v1":
        failures.add("H5_SCHEMA_MISMATCH")
    if document.get("codebook") != CODEBOOK_PATH:
        failures.add("H5_CODEBOOK_BINDING_MISMATCH")
    if document.get("load_bearing") is not False:
        failures.add("H5_PRECALIBRATION_LOAD_BEARING_FORBIDDEN")

    papers = document.get("papers")
    if not isinstance(papers, list):
        return sorted(failures | {"H5_PAPER_INVENTORY_INVALID"})
    paper_ids = tuple(
        row.get("identity", {}).get("id") for row in papers if isinstance(row, dict)
    )
    if paper_ids != CALIBRATION_PAPER_IDS or len(papers) != 3:
        failures.add("H5_PAPER_INVENTORY_MISMATCH")
    ledger = _ledger_index()
    for paper in papers:
        if not isinstance(paper, dict):
            failures.add("H5_PAPER_ROW_INVALID")
            continue
        paper_id = paper.get("identity", {}).get("id")
        fulltext = paper.get("fulltext", {})
        pdf = ledger.get((paper_id, "pdf"), {})
        eprint = ledger.get((paper_id, "eprint"), {})
        if (
            fulltext.get("ledger") != LEDGER_PATH.relative_to(ROOT).as_posix()
            or fulltext.get("pdf_sha256") != pdf.get("sha256")
            or fulltext.get("eprint_sha256") != eprint.get("sha256")
        ):
            failures.add(f"H5_FULLTEXT_LEDGER_BINDING_MISMATCH:{paper_id}")

    coders = document.get("coders")
    if not isinstance(coders, list) or not coders:
        return sorted(failures | {"H5_CODER_INVENTORY_INVALID"})
    coder_ids = [row.get("coder_id") for row in coders if isinstance(row, dict)]
    if len(coder_ids) != len(coders) or None in coder_ids:
        failures.add("H5_CODER_ID_MISSING")
    if len(coder_ids) != len(set(coder_ids)):
        failures.add("H5_DUPLICATE_CODER_ID")
    expected_keys = {
        (paper_id, field)
        for paper_id in CALIBRATION_PAPER_IDS
        for field in FIELD_VALUES
    }
    for coder in coders:
        if not isinstance(coder, dict):
            failures.add("H5_CODER_ROW_INVALID")
            continue
        coder_id = coder.get("coder_id")
        assignments = coder.get("assignments")
        if not isinstance(assignments, list) or len(assignments) != 21:
            failures.add(f"H5_ASSIGNMENT_DENOMINATOR:{coder_id}")
            assignments = assignments if isinstance(assignments, list) else []
        keys = [
            (row.get("paper_id"), row.get("field"))
            for row in assignments
            if isinstance(row, dict)
        ]
        if set(keys) != expected_keys or any(
            count != 1 for count in Counter(keys).values()
        ):
            failures.add(f"H5_ASSIGNMENT_COVERAGE:{coder_id}")
        for row in assignments:
            if not isinstance(row, dict):
                failures.add(f"H5_ASSIGNMENT_ROW_INVALID:{coder_id}")
                continue
            field = row.get("field")
            value = row.get("value")
            if field not in FIELD_VALUES or value not in FIELD_VALUES.get(field, set()):
                failures.add(
                    f"H5_ASSIGNMENT_VALUE_INVALID:{coder_id}:{row.get('paper_id')}:{field}"
                )
            locators = row.get("locators")
            if not isinstance(locators, list) or not locators or any(
                not isinstance(locator, dict)
                or locator.get("kind") != "pdf_page"
                or not isinstance(locator.get("page"), int)
                or not locator.get("anchor")
                for locator in locators
            ):
                failures.add(
                    f"H5_ASSIGNMENT_LOCATOR_INVALID:{coder_id}:{row.get('paper_id')}:{field}"
                )
    report = document.get("agreement_report", {})
    if report.get("planned_denominator") != 21:
        failures.add("H5_PLANNED_DENOMINATOR_MISMATCH")
    return sorted(failures)

def validate_completion(document: dict[str, Any]) -> list[str]:
    failures = set(validate_structure(document))
    coders = document.get("coders") if isinstance(document.get("coders"), list) else []
    if len(coders) != 2 or len({row.get("coder_id") for row in coders}) != 2:
        failures.add("H5_SECOND_INDEPENDENT_CODER_MISSING")
    elif sum(bool(row.get("independent_of_implementer")) for row in coders) < 1:
        failures.add("H5_SECOND_INDEPENDENT_CODER_MISSING")

    report = document.get("agreement_report", {})
    if (
        report.get("observed_comparable_denominator") != 21
        or not isinstance(report.get("exact_agreement_numerator"), int)
        or not 0 <= report.get("exact_agreement_numerator", -1) <= 21
    ):
        failures.add("H5_PAIRWISE_AGREEMENT_INCOMPLETE")
    else:
        expected_rate = report["exact_agreement_numerator"] / 21
        if report.get("exact_agreement_rate") != expected_rate:
            failures.add("H5_AGREEMENT_RATE_MISMATCH")

    disagreements = report.get("disagreements")
    if not isinstance(disagreements, list):
        failures.add("H5_DISAGREEMENT_INVENTORY_INVALID")
        disagreements = []
    for row in disagreements:
        if not isinstance(row, dict):
            failures.add("H5_DISAGREEMENT_ROW_INVALID")
            continue
        adjudication = row.get("adjudication")
        code = f"{row.get('paper_id')}:{row.get('field')}"
        if not isinstance(adjudication, dict) or not all(
            adjudication.get(key)
            for key in ("adjudicator_id", "final_value", "rationale")
        ):
            failures.add(f"H5_DISAGREEMENT_UNADJUDICATED:{code}")
    if document.get("status") != "COMPLETE":
        failures.add("H5_CALIBRATION_STATUS_NOT_COMPLETE")
    return sorted(failures)
