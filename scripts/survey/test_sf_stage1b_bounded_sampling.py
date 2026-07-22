#!/usr/bin/env python3
"""Tests for the bounded three-round Stage-1B sampling workflow."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import sf_stage1b_bounded_sampling as sampling


def paper(arxiv_id: str, title: str, abstract: str, queries: list[str] | None = None) -> dict:
    return {
        "arxiv_id": arxiv_id,
        "title": title,
        "abstract": abstract,
        "authors": ["A. Author"],
        "published": "2026-01-01T00:00:00Z",
        "source_query_ids": queries or ["SF-L1-Q1"],
        "categories": ["cs.AI"],
    }


class BoundedSamplingTests(unittest.TestCase):
    def setUp(self):
        self.datasets = sampling.DatasetCatalog.from_rows(
            [
                {
                    "name": "librispeech",
                    "task": "asr",
                    "factor_family": "content",
                    "status": "COMPLETE",
                    "local_subdir": "datasets/librispeech",
                    "source": {"id": "openslr/librispeech_asr"},
                },
                {
                    "name": "voicebench",
                    "task": "intent",
                    "factor_family": "spoken-qa/agentic",
                    "status": "COMPLETE",
                    "local_subdir": "datasets/voicebench",
                    "source": {"id": "lmms-lab/voicebench"},
                },
                {
                    "name": "aime24",
                    "task": "text-reasoning-eval",
                    "factor_family": "text-reasoning-eval",
                    "status": "COMPLETE",
                    "local_subdir": "datasets/aime24",
                    "source": {"id": "HuggingFaceH4/aime_2024"},
                },
                {
                    "name": "tau2-bench",
                    "task": "intent",
                    "factor_family": "spoken-agent",
                    "status": "COMPLETE",
                    "local_subdir": "datasets/tau2-bench",
                    "source": {"id": "sierra-research/tau2-bench"},
                },
            ],
            present_names={"librispeech", "voicebench", "aime24", "tau2-bench"},
        )

    def test_speech_abstract_records_task_and_local_dataset_match(self):
        row = paper(
            "2601.00001",
            "Training-Free Speech Recognition with Reward-Guided Search",
            "We use a frozen audio language model and verifier feedback on LibriSpeech. Code is open source.",
        )
        analyzed = sampling.analyze_abstract(row, self.datasets)
        self.assertEqual(analyzed["abstract_policy_version"], "sf-stage1b-abstract-policy-v6")
        self.assertTrue(analyzed["speech_related"])
        self.assertIn("asr", analyzed["speech_task_tags"])
        self.assertEqual(analyzed["dataset_local_status"], "LOCAL_MATCH")
        self.assertEqual(analyzed["dataset_mentions"][0]["canonical_name"], "librispeech")
        self.assertEqual(analyzed["abstract_disposition"], "SELECT_FULLTEXT")

    def test_speech_without_named_dataset_is_not_misreported_as_missing(self):
        row = paper(
            "2601.00002",
            "Audio Agent with Adaptive Verification",
            "A frozen audio model uses feedback to select tools and stop.",
        )
        analyzed = sampling.analyze_abstract(row, self.datasets)
        self.assertTrue(analyzed["speech_related"])
        self.assertEqual(analyzed["dataset_local_status"], "NOT_STATED_IN_ABSTRACT")

    def test_incidental_asr_mention_does_not_authorize_fulltext(self):
        row = paper(
            "2601.00008",
            "Verifier-Guided Search for Visual Reasoning",
            "We improve image reasoning with verifier feedback and best-of-n selection. "
            "The broader multimodal literature also includes audio and ASR systems.",
        )
        analyzed = sampling.analyze_abstract(row, self.datasets)
        self.assertTrue(analyzed["speech_related"])
        self.assertFalse(analyzed["speech_primary_object"])
        self.assertNotEqual(analyzed["abstract_disposition"], "SELECT_FULLTEXT")
        self.assertIn("INCIDENTAL_SPEECH_MENTION", analyzed["abstract_reason_codes"])

    def test_named_speech_dataset_is_primary_evidence_even_with_generic_title(self):
        row = paper(
            "2601.00009",
            "Adaptive Verification for Multimodal Models",
            "We use reward feedback and search on LibriSpeech for speech recognition.",
        )
        analyzed = sampling.analyze_abstract(row, self.datasets)
        self.assertTrue(analyzed["speech_primary_object"])
        self.assertEqual(analyzed["abstract_disposition"], "SELECT_FULLTEXT")

    def test_hate_speech_text_task_is_not_an_acoustic_speech_primary(self):
        row = paper(
            "2601.00010",
            "Verifier-Guided Hate Speech Classification",
            "We use feedback and search to classify hateful text without fine-tuning.",
        )
        analyzed = sampling.analyze_abstract(row, self.datasets)
        self.assertTrue(analyzed["speech_related"])
        self.assertFalse(analyzed["speech_primary_object"])
        self.assertIn("NON_ACOUSTIC_SPEECH_SENSE", analyzed["abstract_reason_codes"])

    def test_hate_speech_corpus_does_not_become_acoustic_via_contribution_sentence(self):
        row = paper(
            "2601.00018",
            "Enterprise NLP Benchmark",
            "We evaluate text classifiers on the Measuring Hate Speech corpus and report inference time.",
        )
        analyzed = sampling.analyze_abstract(row, self.datasets)
        self.assertFalse(analyzed["speech_primary_object"])

    def test_attack_success_rate_acronym_is_not_asr_speech_evidence(self):
        row = paper(
            "2601.00019",
            "Prompt Injection against Agents",
            "We evaluate attacks and obtain ASR = 0.68 with critic feedback and planning.",
        )
        analyzed = sampling.analyze_abstract(row, self.datasets)
        self.assertFalse(analyzed["speech_primary_object"])

    def test_similarity_alone_is_not_a_strong_transfer_control_signal(self):
        row = paper(
            "2601.00020",
            "Zero-shot Video Captioning",
            "A frozen VLM uses cosine similarity for decoding and selection. "
            "Code: https://github.com/acme/video-captioning",
        )
        analyzed = sampling.analyze_abstract(row, self.datasets)
        self.assertEqual(analyzed["abstract_disposition"], "DEFER_REPRO_CHECK")

    def test_speech_enhancement_remains_an_acoustic_primary(self):
        row = paper(
            "2601.00011",
            "Training-Free Speech Enhancement with Verifier Search",
            "A frozen model uses acoustic feedback to select enhanced waveforms.",
        )
        analyzed = sampling.analyze_abstract(row, self.datasets)
        self.assertTrue(analyzed["speech_primary_object"])
        self.assertEqual(analyzed["abstract_disposition"], "SELECT_FULLTEXT")

    def test_speech_source_separation_phrase_is_not_missed(self):
        row = paper(
            "2601.00014",
            "Flow Matching-Based Speech Source Separation with Best-of-N Sampling",
            "A frozen speaker encoder provides biometric feedback for best-of-N candidate selection at inference time.",
        )
        analyzed = sampling.analyze_abstract(row, self.datasets)
        self.assertTrue(analyzed["speech_primary_object"])
        self.assertEqual(analyzed["abstract_disposition"], "SELECT_FULLTEXT")

    def test_speechllm_translation_and_speech_understanding_are_acoustic_primary(self):
        translation = paper(
            "2601.00015",
            "Training-Free Simultaneous Translation with SpeechLLMs",
            "We derive an inference-time decoding policy from a frozen model.",
        )
        understanding = paper(
            "2601.00016",
            "A Reproducible Framework for Speech Understanding",
            "We standardize evaluation and scoring for acoustic systems.",
        )
        self.assertTrue(sampling.analyze_abstract(translation, self.datasets)["speech_primary_object"])
        self.assertTrue(sampling.analyze_abstract(understanding, self.datasets)["speech_primary_object"])

    def test_audio_language_technical_report_contribution_is_speech_primary(self):
        row = paper(
            "2601.00017",
            "StepAudio Technical Report",
            "This report presents a unified audio-language foundation model for ASR and TTS. "
            "We evaluate speech recognition and synthesis benchmarks.",
        )
        analyzed = sampling.analyze_abstract(row, self.datasets)
        self.assertTrue(analyzed["speech_primary_object"])
        self.assertIn("SPEECH_IN_CONTRIBUTION_STATEMENT", analyzed["speech_primary_reasons"])

    def test_local_text_reasoning_dataset_does_not_create_speech_primary(self):
        row = paper(
            "2601.00012",
            "Training-Free Agent Verifier Search for Mathematical Reasoning",
            "A frozen LLM agent uses feedback and search on AIME24. Code: https://github.com/acme/math-search",
        )
        analyzed = sampling.analyze_abstract(row, self.datasets)
        self.assertFalse(analyzed["speech_primary_object"])
        self.assertEqual(analyzed["speech_dataset_mentions"], [])
        self.assertEqual(analyzed["dataset_local_status"], "NOT_APPLICABLE_NON_SPEECH")
        self.assertEqual(analyzed["abstract_disposition"], "SELECT_FULLTEXT")

    def test_spoken_capable_agent_benchmark_without_acoustic_task_does_not_create_speech_primary(self):
        row = paper(
            "2601.00013",
            "Training-Free Skill Injection for Tool Agents",
            "A frozen agent uses feedback and search on tau2-bench. Code: https://github.com/acme/skills",
        )
        analyzed = sampling.analyze_abstract(row, self.datasets)
        self.assertFalse(analyzed["speech_primary_object"])
        self.assertEqual(analyzed["dataset_local_status"], "NOT_APPLICABLE_NON_SPEECH")

    def test_non_speech_requires_transfer_path_and_reproducibility_evidence(self):
        open_row = paper(
            "2601.00003",
            "Open-Source Vision Agent Search",
            "A frozen VLM uses uncertainty feedback to select actions at test time. Code is available at https://github.com/x/y.",
        )
        closed_row = paper(
            "2601.00004",
            "Vision Classification",
            "We train a classifier and report accuracy.",
        )
        selected = sampling.analyze_abstract(open_row, self.datasets)
        excluded = sampling.analyze_abstract(closed_row, self.datasets)
        self.assertFalse(selected["speech_related"])
        self.assertEqual(selected["reproducibility_abstract_status"], "EXPLICIT_REPO_URL")
        self.assertEqual(selected["abstract_disposition"], "SELECT_FULLTEXT")
        self.assertEqual(excluded["abstract_disposition"], "EXCLUDE_ABSTRACT")

    def test_test_time_scaling_acronym_does_not_create_a_tts_speech_task(self):
        row = paper(
            "2601.00005",
            "Test-Time Scaling for Vision Models",
            "We study TTS for image generation with a verifier and search.",
        )
        analyzed = sampling.analyze_abstract(row, self.datasets)
        self.assertFalse(analyzed["speech_related"])
        self.assertNotIn("tts", analyzed["speech_task_tags"])

    def test_non_speech_project_page_or_trained_open_claim_is_deferred(self):
        project_page = paper(
            "2601.00006",
            "Vision Agent Search",
            "A VLM uses reward feedback to select actions. See https://example.org/project.",
        )
        trained_open = paper(
            "2601.00007",
            "Open-Source Trained Vision Agent",
            "We train a VLM agent with reward feedback and search. Code is open source.",
        )
        self.assertEqual(
            sampling.analyze_abstract(project_page, self.datasets)["abstract_disposition"],
            "DEFER_REPRO_CHECK",
        )
        self.assertEqual(
            sampling.analyze_abstract(trained_open, self.datasets)["abstract_disposition"],
            "DEFER_REPRO_CHECK",
        )

    def test_sampling_is_deterministic_non_overlapping_and_excludes_handled(self):
        rows = []
        for index in range(18):
            aid = f"2601.{index:05d}"
            if index % 3 == 0:
                rows.append(paper(aid, "Speech verifier search", "Frozen audio feedback selection on VoiceBench."))
            elif index % 3 == 1:
                rows.append(paper(aid, "Open vision agent", "Open-source VLM feedback search with code available."))
            else:
                rows.append(paper(aid, "Generic learning", "A trained model for classification."))
        handled = {"2601.00000", "2601.00001"}
        first = sampling.build_rounds(rows, self.datasets, handled, round_size=4, seed="fixed")
        second = sampling.build_rounds(list(reversed(rows)), self.datasets, handled, round_size=4, seed="fixed")
        self.assertEqual(first, second)
        self.assertEqual([len(batch) for batch in first], [4, 4, 4])
        ids = [row["arxiv_id"] for batch in first for row in batch]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertFalse(set(ids) & handled)
        self.assertEqual({row["sample_round"] for row in first[0]}, {1})
        self.assertEqual({row["sampling_lane"] for row in first[1]}, {"TRANSFER_REPRODUCIBLE"})
        self.assertEqual({row["sampling_lane"] for row in first[2]}, {"TAIL_CALIBRATION"})

    def test_build_fails_when_unique_pool_cannot_fill_all_rounds(self):
        rows = [paper(f"2601.{index:05d}", "Audio", "Speech feedback search.") for index in range(5)]
        with self.assertRaisesRegex(sampling.SamplingError, "cannot fill"):
            sampling.build_rounds(rows, self.datasets, set(), round_size=2, seed="fixed")

    def test_exhaust_remaining_emits_a_partial_tail_and_proves_exhaustion(self):
        rows = [
            paper(f"2601.{index:05d}", "Audio verifier search", "Frozen speech feedback selection.")
            for index in range(10)
        ]
        rounds = sampling.build_rounds(
            rows,
            self.datasets,
            set(),
            round_size=4,
            exhaust_remaining=True,
            seed="fixed-exhaustive",
        )
        self.assertEqual([len(batch) for batch in rounds], [4, 4, 2])
        self.assertEqual(len({row["arxiv_id"] for batch in rounds for row in batch}), 10)

        with tempfile.TemporaryDirectory() as temp:
            summary = sampling.write_rounds(
                Path(temp),
                rounds,
                "source-sha",
                "dataset-sha",
                sampling_seed="fixed-exhaustive",
                handled_ids=set(),
                eligible_unhandled_count=10,
            )
            self.assertEqual(summary["schema"], "sf-stage1b-bounded-sampling-summary-v7")
            self.assertEqual(summary["eligible_unhandled_before_sampling"], 10)
            self.assertEqual(summary["remaining_unhandled_after_sampling"], 0)
            self.assertTrue(summary["corpus_exhausted_within_frozen_source"])
            self.assertTrue((Path(temp) / "bounded-sampling-summary.json").is_file())

    def test_five_round_extension_reuses_frozen_lane_cycle_without_overlap(self):
        rows = []
        for index in range(30):
            aid = f"2601.{index:05d}"
            if index % 3 == 0:
                rows.append(paper(aid, "Speech verifier search", "Frozen audio feedback selection on VoiceBench."))
            elif index % 3 == 1:
                rows.append(
                    paper(
                        aid,
                        "Open vision agent",
                        "A frozen VLM uses feedback search. Code: https://github.com/acme/repo.",
                    )
                )
            else:
                rows.append(paper(aid, "Generic learning", "A trained classifier."))
        rounds = sampling.build_rounds(
            rows,
            self.datasets,
            set(),
            round_size=4,
            round_count=5,
            seed="fixed-five",
        )
        self.assertEqual([len(batch) for batch in rounds], [4, 4, 4, 4, 4])
        ids = [row["arxiv_id"] for batch in rounds for row in batch]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(
            [batch[0]["sampling_lane"] for batch in rounds],
            [
                "SPEECH_TASK_AND_DATASET",
                "TRANSFER_REPRODUCIBLE",
                "TAIL_CALIBRATION",
                "SPEECH_TASK_AND_DATASET",
                "TRANSFER_REPRODUCIBLE",
            ],
        )

        with tempfile.TemporaryDirectory() as temp:
            summary = sampling.write_rounds(
                Path(temp),
                rounds,
                "source-sha",
                "dataset-sha",
                sampling_seed="fixed-five",
                handled_ids=set(),
            )
            self.assertEqual(summary["round_count"], 5)
            self.assertEqual(summary["sampled_unique"], 20)
            self.assertTrue((Path(temp) / "bounded-sampling-summary.json").is_file())

    def test_jsonl_writer_emits_three_manifests_and_summary(self):
        rows = [
            paper(f"2601.{index:05d}", "Speech reward search", "Frozen audio feedback selection on LibriSpeech.")
            for index in range(9)
        ]
        handled = {"2501.00001", "2501.00002"}
        rounds = sampling.build_rounds(rows, self.datasets, handled, round_size=2, seed="fixed")
        with tempfile.TemporaryDirectory() as temp:
            summary = sampling.write_rounds(
                Path(temp),
                rounds,
                "source-sha",
                "dataset-sha",
                sampling_seed="fixed",
                handled_ids=handled,
            )
            self.assertEqual(summary["schema"], "sf-stage1b-bounded-sampling-summary-v6")
            self.assertEqual(summary["round_sizes"], [2, 2, 2])
            self.assertEqual(summary["sampled_unique"], 6)
            self.assertEqual(summary["sampling_seed"], "fixed")
            self.assertEqual(summary["handled_ids_count"], 2)
            expected_handled = sampling.id_set_sha256(handled)
            self.assertEqual(summary["handled_ids_sha256"], expected_handled)
            handled_path = Path(temp) / "handled-ids.txt"
            self.assertEqual(handled_path.read_text("utf-8"), "2501.00001\n2501.00002\n")
            self.assertEqual(summary["handled_ids_artifact"]["sha256"], expected_handled)
            for index in range(1, 4):
                path = Path(temp) / f"round-{index}-abstract-sample.jsonl"
                payload = [json.loads(line) for line in path.read_text("utf-8").splitlines()]
                self.assertEqual(len(payload), 2)
                self.assertTrue(all(row["sample_round"] == index for row in payload))
                self.assertTrue(all(row["sampling_schema"] == "sf-stage1b-bounded-sample-v6" for row in payload))

    def test_handled_notes_and_explicit_ids_form_one_canonical_set(self):
        with tempfile.TemporaryDirectory() as temp:
            note = Path(temp) / "handled.txt"
            note.write_text("paper 2501.00001v2 and 2501.00002\n", encoding="utf-8")
            handled = sampling._handled_ids([note], ["2501.00003", "2501.00001"])
            self.assertEqual(handled, {"2501.00001", "2501.00002", "2501.00003"})
            self.assertEqual(sampling.id_set_sha256(handled), sampling.id_set_sha256(reversed(sorted(handled))))

    def test_handled_jsonl_uses_record_identity_not_ids_cited_in_abstract(self):
        with tempfile.TemporaryDirectory() as temp:
            ledger = Path(temp) / "sample.jsonl"
            ledger.write_text(
                json.dumps(
                    {
                        "arxiv_id": "2501.00001",
                        "abstract": "We compare with arXiv:2401.99999 and https://arxiv.org/abs/2301.88888.",
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            handled = sampling._handled_ids([ledger], [])
            self.assertEqual(handled, {"2501.00001"})

    def test_jsonl_reader_reports_line_number_on_invalid_input(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "bad.jsonl"
            source.write_text('{"ok": 1}\nnot-json\n', encoding="utf-8")
            with self.assertRaisesRegex(sampling.SamplingError, "line 2"):
                sampling._read_jsonl(source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
