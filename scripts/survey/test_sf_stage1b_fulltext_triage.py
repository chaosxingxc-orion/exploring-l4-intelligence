#!/usr/bin/env python3
"""Tests for bounded Stage-1B local full-text triage."""

from __future__ import annotations

import sys
import argparse
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))

import sf_stage1b_bounded_sampling as sampling
import sf_stage1b_fulltext_triage as triage


class FulltextTriageTests(unittest.TestCase):
    def test_load_repo_verifications_merges_multiple_receipts(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            first = root / "first.json"
            second = root / "second.json"
            first.write_text(json.dumps({"https://github.com/a/x": {"status": "OPEN_SOURCE_VERIFIED"}}), encoding="utf-8")
            second.write_text(json.dumps({"https://github.com/b/y": {"status": "OPEN_SOURCE_VERIFIED"}}), encoding="utf-8")
            merged = triage._load_repo_verifications([first, second])
            self.assertEqual(set(merged), {"https://github.com/a/x", "https://github.com/b/y"})

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
                    "name": "aime24",
                    "task": "text-reasoning-eval",
                    "factor_family": "text-reasoning-eval",
                    "status": "COMPLETE",
                    "local_subdir": "datasets/aime24",
                    "source": {"id": "HuggingFaceH4/aime_2024"},
                },
            ],
            present_names={"librispeech", "aime24"},
        )

    def test_invalid_pdf_surrogate_is_replaced_for_utf8_artifacts(self):
        self.assertEqual(triage._safe_utf8("page \ud83c text"), "page ? text")

    def test_training_free_speech_control_path_with_local_data_is_core(self):
        row = {
            "arxiv_id": "2601.00001",
            "title": "Training-Free Speech Recognition",
            "speech_primary_object": True,
            "speech_task_tags": ["asr"],
        }
        pages = [
            "We keep the speech model frozen and use verifier feedback to search and select transcripts.",
            "Experiments use LibriSpeech test-clean. Code: https://github.com/acme/speech-search",
        ]
        result = triage.analyze_pages(row, pages, self.datasets)
        self.assertEqual(result["final_decision"], "KEEP_CORE")
        self.assertEqual(result["dataset_local_status"], "LOCAL_MATCH")
        self.assertEqual(result["dataset_mentions"][0]["canonical_name"], "librispeech")
        self.assertIn("frozen", result["no_update_terms"])
        self.assertTrue(result["evidence_locators"])
        self.assertEqual(result["dataset_mentions"][0]["task_suitability_by_tag"]["asr"], "TASK_MATCH")

    def test_non_speech_transfer_waits_for_repository_verification(self):
        row = {
            "arxiv_id": "2601.00002",
            "title": "Verifier Search for Vision Agents",
            "speech_primary_object": False,
            "speech_task_tags": [],
        }
        pages = [
            "Our frozen VLM agent uses reward feedback and tree search at inference time. "
            "Implementation: https://github.com/acme/vision-search"
        ]
        pending = triage.analyze_pages(row, pages, self.datasets)
        verified = triage.analyze_pages(
            row,
            pages,
            self.datasets,
            repo_verification={"https://github.com/acme/vision-search": "OPEN_SOURCE_VERIFIED"},
        )
        self.assertEqual(pending["final_decision"], "DEFER_REPO_VERIFY")
        self.assertEqual(verified["final_decision"], "KEEP_TRANSFER")
        failed_gate = triage.analyze_pages(
            row,
            pages,
            self.datasets,
            repo_verification={
                "https://github.com/acme/vision-search": "REPOSITORY_REACHABLE_LICENSE_UNRESOLVED"
            },
        )
        self.assertEqual(failed_gate["final_decision"], "DROP")
        self.assertIn("REPRODUCIBILITY_GATE_FAILED", failed_gate["final_reason_codes"])

    def test_non_speech_closed_trained_method_is_dropped(self):
        row = {
            "arxiv_id": "2601.00003",
            "title": "A Trained Vision Classifier",
            "speech_primary_object": False,
            "speech_task_tags": [],
        }
        result = triage.analyze_pages(
            row,
            ["We fine-tune a vision model for classification and report accuracy."],
            self.datasets,
        )
        self.assertEqual(result["final_decision"], "DROP")
        self.assertEqual(result["repo_status"], "NO_REPOSITORY_EVIDENCE")

    def test_non_speech_local_text_dataset_is_not_reported_as_speech_local(self):
        row = {
            "arxiv_id": "2601.00010",
            "title": "Frozen Math Agent Search",
            "speech_primary_object": False,
            "speech_task_tags": [],
        }
        result = triage.analyze_pages(
            row,
            ["A frozen agent uses verifier feedback and search on AIME24."],
            self.datasets,
        )
        self.assertEqual(result["dataset_local_status"], "NOT_APPLICABLE_NON_SPEECH")
        self.assertEqual(result["speech_dataset_mentions"], [])

    def test_reference_list_repository_is_not_treated_as_official_code(self):
        row = {
            "arxiv_id": "2601.00006",
            "title": "Frozen Vision Search",
            "speech_primary_object": False,
            "speech_task_tags": [],
        }
        pages = ["A frozen VLM uses verifier feedback and search at inference time."] + ["body"] * 7 + [
            "References: an unrelated implementation https://github.com/other/prior-work"
        ]
        result = triage.analyze_pages(row, pages, self.datasets)
        self.assertEqual(result["repo_urls"], [])
        self.assertEqual(result["final_decision"], "DROP")

    def test_dependency_repository_in_front_matter_is_not_treated_as_paper_code(self):
        row = {
            "arxiv_id": "2601.00008",
            "title": "Frozen Speech Search",
            "speech_primary_object": True,
            "speech_task_tags": ["asr"],
        }
        result = triage.analyze_pages(
            row,
            [
                "We use a frozen speech model with verifier feedback and search. "
                "Our implementation builds on https://github.com/facebookresearch/fairseq as a dependency."
            ],
            self.datasets,
        )
        self.assertEqual(result["repo_urls"], [])

    def test_scattered_vocabulary_does_not_fabricate_a_control_path(self):
        row = {
            "arxiv_id": "2601.00007",
            "title": "Vision Model Survey",
            "speech_primary_object": False,
            "speech_task_tags": [],
        }
        pages = [
            "We study a frozen VLM at inference time.",
            "Prior reward models provide feedback.",
            "Unrelated systems use tree search for planning.",
        ]
        result = triage.analyze_pages(
            row,
            pages,
            self.datasets,
            repo_verification={"https://github.com/acme/x": "OPEN_SOURCE_VERIFIED"},
        )
        self.assertFalse(result["control_path_page_cooccurrence"])
        self.assertEqual(result["final_decision"], "DROP")

    def test_speech_benchmark_on_local_data_can_be_kept_as_instrument(self):
        row = {
            "arxiv_id": "2601.00004",
            "title": "A Speech Recognition Evaluation Benchmark",
            "speech_primary_object": True,
            "speech_task_tags": ["asr"],
        }
        result = triage.analyze_pages(
            row,
            ["We evaluate word error rate on the LibriSpeech benchmark and release an evaluation toolkit."],
            self.datasets,
        )
        self.assertEqual(result["final_decision"], "KEEP_INSTRUMENT")

    def test_frozen_inference_path_is_not_rejected_for_trained_baseline_mentions(self):
        row = {
            "arxiv_id": "2601.00005",
            "title": "Frozen Audio Model Search",
            "speech_primary_object": True,
            "speech_task_tags": ["asr"],
        }
        result = triage.analyze_pages(
            row,
            [
                "At inference time the frozen speech model uses verifier feedback to select outputs. "
                "A separately trained baseline is included for comparison."
            ],
            self.datasets,
        )
        self.assertEqual(result["final_decision"], "KEEP_CORE")
        self.assertTrue(result["training_conflict_requires_audit"])

    def test_inference_time_label_alone_does_not_prove_frozen_core(self):
        row = {
            "arxiv_id": "2601.00009",
            "title": "Speech Search at Inference Time",
            "speech_primary_object": True,
            "speech_task_tags": ["asr"],
        }
        result = triage.analyze_pages(
            row,
            ["At inference time a reward model guides search. We evaluate the method as an ASR benchmark."],
            self.datasets,
        )
        self.assertFalse(result["strong_no_weight_update_evidence"])
        self.assertEqual(result["final_decision"], "KEEP_INSTRUMENT")

    def test_run_records_extracted_missing_and_failed_pdfs(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            data_root = root / "data"
            (data_root / "datasets" / "librispeech").mkdir(parents=True)
            lock = root / "datasets.lock.json"
            lock.write_text(
                json.dumps(
                    {
                        "datasets": [
                            {
                                "name": "librispeech",
                                "task": "asr",
                                "factor_family": "content",
                                "status": "COMPLETE",
                                "local_subdir": "datasets/librispeech",
                                "source": {"id": "openslr/librispeech_asr"},
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            manifest = root / "manifest.jsonl"
            rows = []
            for suffix in range(1, 4):
                rows.append(
                    {
                        "arxiv_id": f"2601.0000{suffix}",
                        "title": "Speech search",
                        "abstract_disposition": "SELECT_FULLTEXT",
                        "speech_primary_object": True,
                        "speech_task_tags": ["asr"],
                    }
                )
            manifest.write_text("".join(json.dumps(item) + "\n" for item in rows), encoding="utf-8")
            pdf_root = root / "pdf"
            for aid in ("2601.00001", "2601.00003"):
                path = pdf_root / aid / f"{aid}.pdf"
                path.parent.mkdir(parents=True)
                path.write_bytes(b"%PDF" + b"x" * 2048)
            verification = root / "repos.json"
            verification.write_text("{}", encoding="utf-8")
            args = argparse.Namespace(
                manifest=[manifest],
                dataset_lock=lock,
                data_root=data_root,
                pdf_root=pdf_root,
                output_dir=root / "out",
                repo_verification=verification,
            )
            with mock.patch.object(
                triage,
                "_extract_pdf",
                side_effect=[
                    ["Frozen speech verifier feedback search on LibriSpeech."],
                    ValueError("bad pdf"),
                ],
            ):
                summary = triage.run(args)
            self.assertEqual(summary["processed_rows"], 3)
            results = [json.loads(line) for line in (root / "out" / "fulltext-triage.jsonl").read_text("utf-8").splitlines()]
            statuses = {item["fulltext_status"] for item in results}
            self.assertEqual(statuses, {"PDF_EXTRACTED", "PDF_MISSING", "EXTRACTION_FAILED"})

    def test_run_selects_explicit_audit_promotions_and_records_provenance(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            data_root = root / "data"
            (data_root / "datasets" / "dummy").mkdir(parents=True)
            lock = root / "datasets.lock.json"
            lock.write_text(
                json.dumps(
                    {
                        "datasets": [
                            {
                                "name": "dummy",
                                "task": "other",
                                "factor_family": "other",
                                "status": "COMPLETE",
                                "local_subdir": "datasets/dummy",
                                "source": {"id": "local/dummy"},
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            manifest = root / "manifest.jsonl"
            manifest.write_text(
                json.dumps(
                    {
                        "arxiv_id": "2605.31432",
                        "title": "Training-free speech policy",
                        "abstract_disposition": "DEFER_ABSTRACT",
                        "speech_primary_object": True,
                        "speech_task_tags": ["st"],
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            promotions = root / "promotions.json"
            promotions.write_text(
                json.dumps(
                    [
                        {
                            "arxiv_id": "2605.31432",
                            "from_disposition": "DEFER_ABSTRACT",
                            "to_disposition": "AUDIT_SELECT_FULLTEXT",
                            "reason": "Direct frozen speech control path.",
                        }
                    ]
                ),
                encoding="utf-8",
            )
            pdf = root / "pdf" / "2605.31432" / "2605.31432.pdf"
            pdf.parent.mkdir(parents=True)
            pdf.write_bytes(b"%PDF" + b"x" * 2048)
            args = argparse.Namespace(
                manifest=[manifest],
                audit_promotions=promotions,
                dataset_lock=lock,
                data_root=data_root,
                pdf_root=root / "pdf",
                output_dir=root / "out",
                repo_verification=None,
            )
            with mock.patch.object(
                triage,
                "_extract_pdf",
                return_value=["A frozen speech model uses verifier-guided candidate selection."],
            ):
                summary = triage.run(args)
            self.assertEqual(summary["selected_unique"], 1)
            self.assertEqual(summary["audit_promotions_selected"], 1)
            row = json.loads((root / "out" / "fulltext-triage.jsonl").read_text("utf-8"))
            self.assertEqual(row["fulltext_selection_origin"], "AUDIT_PROMOTION")
            self.assertEqual(row["source_abstract_disposition"], "DEFER_ABSTRACT")
            self.assertEqual(row["audit_promotion_reason"], "Direct frozen speech control path.")


if __name__ == "__main__":
    unittest.main(verbosity=2)
