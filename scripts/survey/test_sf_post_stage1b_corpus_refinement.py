#!/usr/bin/env python3
"""Tests for exhaustive post-Stage-1B local full-text refinement."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import sf_post_stage1b_corpus_refinement as refinement


class FakeDatasetCatalog:
    def match(self, text: str) -> list[dict]:
        if "librispeech" not in text.lower():
            return []
        return [
            {
                "canonical_name": "librispeech",
                "task": "asr",
                "local_present": True,
                "lock_status": "COMPLETE",
            }
        ]


class CorpusDiscoveryTests(unittest.TestCase):
    def test_discovery_accounts_for_every_artifact_and_every_unique_pdf(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for aid in ("2501.00001", "2501.00002"):
                paper = root / aid
                paper.mkdir()
                (paper / f"{aid}.pdf").write_bytes(b"%PDF" + aid.encode())
            (root / "2501.00001" / "2501.00001.eprint").write_bytes(b"source")
            (root / "fetch.log").write_text("ok", encoding="utf-8")

            artifacts, papers = refinement.discover_artifacts(root)

            self.assertEqual(len(artifacts), 4)
            self.assertEqual(sorted(papers), ["2501.00001", "2501.00002"])
            self.assertEqual(papers["2501.00001"].eprint_relative_path, "2501.00001/2501.00001.eprint")
            self.assertEqual(sum(item.artifact_kind == "CONTROL_OR_LOG" for item in artifacts), 1)

    def test_duplicate_pdf_identity_fails_closed_even_at_different_paths(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for parent in (root / "a", root / "b"):
                parent.mkdir()
                (parent / "2501.00001.pdf").write_bytes(b"%PDF")

            with self.assertRaisesRegex(ValueError, "duplicate PDF identity"):
                refinement.discover_artifacts(root)


class RefinementDecisionTests(unittest.TestCase):
    def test_black_box_reward_control_with_local_data_is_direct_candidate(self):
        pages = [
            "A training-free black-box omni model uses reward feedback to select the next tool "
            "action and stop. We evaluate ASR on LibriSpeech."
        ]
        row = refinement.analyze_pages(
            "2501.00001", pages, {"title": "Frozen Omni Control", "speech_primary_object": True},
            FakeDatasetCatalog(),
        )

        self.assertEqual(row["execution_disposition"], "PRIORITY_DIRECT")
        self.assertEqual(row["model_operability"], "BLACK_BOX_COMPATIBLE")
        self.assertEqual(row["data_feasibility"], "LOCAL_MATCH")
        self.assertTrue(row["external_control_path"])

    def test_load_bearing_finetuning_and_architecture_change_are_excluded_from_execution(self):
        pages = [
            "Our method fine-tunes the backbone with LoRA and adds a learnable cross-attention "
            "adapter. Gradients update the model weights during training."
        ]
        row = refinement.analyze_pages("2501.00002", pages, {}, FakeDatasetCatalog())

        self.assertEqual(row["execution_disposition"], "EXCLUDE_MODEL_OPERABLE")
        self.assertEqual(row["model_operability"], "MODEL_OR_COMPONENT_OPERABLE")
        self.assertIn("LOAD_BEARING_TRAINING", row["reason_codes"])
        self.assertIn("ARCHITECTURE_MODIFICATION", row["reason_codes"])

    def test_private_vertical_data_is_separate_from_black_box_compatibility(self):
        pages = [
            "We call a frozen black-box API and use reward feedback to revise the diagnosis. "
            "Experiments use private patient EHR records from our hospital that cannot be released."
        ]
        row = refinement.analyze_pages("2501.00003", pages, {}, FakeDatasetCatalog())

        self.assertEqual(row["model_operability"], "BLACK_BOX_COMPATIBLE")
        self.assertEqual(row["vertical_domains"], ["medical"])
        self.assertEqual(row["data_feasibility"], "RESTRICTED_VERTICAL_DATA")
        self.assertEqual(row["execution_disposition"], "EXCLUDE_VERTICAL_DATA_BARRIER")

    def test_training_free_nonlocal_control_mechanism_remains_transfer_only(self):
        pages = [
            "We use a training-free API-only language model. Verifier reward chooses among candidate "
            "plans and decides whether to continue the search."
        ]
        row = refinement.analyze_pages("2501.00004", pages, {}, FakeDatasetCatalog())

        self.assertEqual(row["execution_disposition"], "TRANSFER_ONLY")
        self.assertEqual(row["data_feasibility"], "NO_MATCHING_LOCAL_DATA_EVIDENCE")

    def test_related_work_training_mentions_do_not_make_the_method_operable(self):
        pages = [
            "Our training-free black-box method uses verifier reward to select the next search action.",
            "Related work often relies on supervised fine-tuning. Several baseline models are trained "
            "with LoRA adapters.",
        ]
        row = refinement.analyze_pages("2501.00005", pages, {}, FakeDatasetCatalog())

        self.assertEqual(row["model_operability"], "BLACK_BOX_COMPATIBLE")
        self.assertEqual(row["execution_disposition"], "TRANSFER_ONLY")
        self.assertEqual(row["training_evidence"], [])

    def test_external_agent_architecture_is_not_a_model_architecture_modification(self):
        pages = [
            "We introduce a training-free black-box multi-agent architecture with an evidence memory "
            "module. Reward feedback chooses whether to search or stop."
        ]
        row = refinement.analyze_pages("2501.00006", pages, {}, FakeDatasetCatalog())

        self.assertEqual(row["model_operability"], "BLACK_BOX_COMPATIBLE")
        self.assertNotIn("ARCHITECTURE_MODIFICATION", row["reason_codes"])

    def test_vertical_domain_comes_from_title_or_abstract_not_late_comparison_text(self):
        pages = [
            "A training-free black-box planning method. Reward feedback chooses the next tool action.",
            "Method details without a vertical deployment.",
            "In a later comparison we cite medical diagnosis, educational tutoring, and robot navigation.",
        ]
        row = refinement.analyze_pages("2501.00007", pages, {}, FakeDatasetCatalog())

        self.assertEqual(row["vertical_domains"], [])

    def test_generic_benchmark_reporting_does_not_turn_a_method_into_an_instrument(self):
        pages = [
            "We propose a new planning method and report accuracy on a benchmark. The reward score "
            "chooses the next search action."
        ]
        row = refinement.analyze_pages("2501.00008", pages, {}, FakeDatasetCatalog())

        self.assertNotIn("MEASUREMENT_INSTRUMENT_SIGNAL", row["reason_codes"])

    def test_negated_gradient_and_finetuning_claims_are_black_box_evidence_not_training(self):
        pages = [
            "Our frozen framework requires no gradient updates and does not fine-tune the model. "
            "Verifier feedback selects the next action without modifying model weights."
        ]
        row = refinement.analyze_pages("2501.00009", pages, {}, FakeDatasetCatalog())

        self.assertEqual(row["model_operability"], "BLACK_BOX_COMPATIBLE")
        self.assertEqual(row["training_evidence"], [])
        self.assertEqual(row["internal_access_terms"], [])

    def test_pomdp_hidden_state_is_not_model_internal_access(self):
        pages = [
            "We model the environment as a POMDP with a hidden state. Reward feedback selects the "
            "next tool action for a frozen black-box agent."
        ]
        row = refinement.analyze_pages("2501.00010", pages, {}, FakeDatasetCatalog())

        self.assertEqual(row["model_operability"], "BLACK_BOX_COMPATIBLE")
        self.assertEqual(row["internal_access_terms"], [])

    def test_decoder_hidden_state_used_by_method_is_internal_access(self):
        pages = [
            "Our method computes confidence from the decoder hidden state and uses the score to "
            "select the next token."
        ]
        row = refinement.analyze_pages("2501.00011", pages, {}, FakeDatasetCatalog())

        self.assertEqual(row["model_operability"], "INTERNAL_ACCESS_REQUIRED_OR_AMBIGUOUS")
        self.assertEqual(row["execution_disposition"], "EXCLUDE_MODEL_INTERNAL_ACCESS")

    def test_registry_no_update_evidence_can_resolve_access_for_a_registered_path(self):
        pages = ["Verifier reward selects the next search action."]
        registry = {
            "role": "KEEP_TRANSFER",
            "method_path": {"no_update_evidence": ["frozen", "training-free"]},
        }
        row = refinement.analyze_pages("2501.00012", pages, registry, FakeDatasetCatalog())

        self.assertEqual(row["model_operability"], "BLACK_BOX_COMPATIBLE")
        self.assertEqual(row["execution_disposition"], "TRANSFER_ONLY")
        self.assertEqual(row["black_box_evidence_source"], "STAGE1B_REGISTRY")

    def test_short_speech_acronym_does_not_match_inside_autotts_name(self):
        pages = [
            "AutoTTS is a training-free black-box test-time scaling controller. Reward feedback "
            "selects whether to branch or stop on LibriSpeech."
        ]
        row = refinement.analyze_pages("2501.00013", pages, {}, FakeDatasetCatalog())

        self.assertFalse(row["speech_primary_signal"])
        self.assertEqual(row["execution_disposition"], "TRANSFER_ONLY")

    def test_registered_negative_cannot_enter_direct_or_transfer_execution_queue(self):
        pages = [
            "A training-free black-box audio method uses reward feedback to select the next action "
            "on LibriSpeech."
        ]
        row = refinement.analyze_pages(
            "2501.00014", pages, {"role": "KEEP_NEGATIVE", "speech_primary_object": True},
            FakeDatasetCatalog(),
        )

        self.assertEqual(row["execution_disposition"], "BOUNDARY_OR_NEGATIVE_ONLY")

    def test_public_patient_record_benchmark_is_not_restricted_data(self):
        pages = [
            "We evaluate clinical reasoning on the public RareBench benchmark. Each instance contains "
            "a patient record and ranked diagnosis labels."
        ]
        row = refinement.analyze_pages("2501.00015", pages, {}, FakeDatasetCatalog())

        self.assertNotEqual(row["data_feasibility"], "RESTRICTED_VERTICAL_DATA")

    def test_proprietary_pretraining_data_is_not_an_execution_dataset_barrier(self):
        pages = [
            "The target black-box model was pretrained on proprietary data. Our prompt optimizer is "
            "evaluated on publicly available image benchmarks."
        ]
        row = refinement.analyze_pages("2501.00016", pages, {}, FakeDatasetCatalog())

        self.assertEqual(row["data_feasibility"], "PUBLIC_OR_RELEASED_NOT_LOCAL")

    def test_clinical_participant_data_on_private_servers_is_restricted(self):
        pages = [
            "We study clinical audio diaries collected from participants under IRB approval.",
            "All transcripts were securely hosted on private servers behind an institutional firewall.",
        ]
        row = refinement.analyze_pages("2501.00017", pages, {}, FakeDatasetCatalog())

        self.assertEqual(row["data_feasibility"], "RESTRICTED_VERTICAL_DATA")

    def test_decoder_attention_policy_is_internal_even_without_hidden_state_wording(self):
        pages = [
            "We propose a training-free decoder-only attention policy. Decoder self-attention "
            "provides the signal that decides when to read and when to write."
        ]
        row = refinement.analyze_pages("2501.00018", pages, {}, FakeDatasetCatalog())

        self.assertEqual(row["execution_disposition"], "EXCLUDE_MODEL_INTERNAL_ACCESS")


class EndToEndCoverageTests(unittest.TestCase):
    def test_run_keeps_failed_extraction_in_ledger_and_proves_complete_accounting(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source"
            output = root / "output"
            for aid in ("2501.00001", "2501.00002"):
                paper = source / aid
                paper.mkdir(parents=True)
                (paper / f"{aid}.pdf").write_bytes(b"%PDF" + aid.encode())
            (source / "2501.00001" / "2501.00001.eprint").write_bytes(b"source")
            (source / "fetch.log").write_text("ok", encoding="utf-8")
            registry = root / "registry.jsonl"
            registry.write_text(
                json.dumps(
                    {
                        "schema": "sf-paper-registry-record-v1",
                        "canonical_id": "arxiv:2501.00001",
                        "arxiv_id": "2501.00001",
                        "title": "Known paper",
                        "role": "KEEP_CORE",
                        "speech_primary_object": True,
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            def extract(path: Path) -> list[str]:
                if path.stem == "2501.00002":
                    raise RuntimeError("broken xref")
                return ["Frozen black-box reward feedback selects a tool action on LibriSpeech."]

            summary = refinement.run(
                source,
                output,
                [registry],
                FakeDatasetCatalog(),
                extract_pdf=extract,
            )

            self.assertEqual(summary["source_artifacts"], 4)
            self.assertEqual(summary["discovered_unique_pdfs"], 2)
            self.assertEqual(summary["processed_paper_rows"], 2)
            self.assertEqual(summary["extracted_pdfs"], 1)
            self.assertEqual(summary["extraction_failed_pdfs"], 1)
            self.assertEqual(summary["registry_matched_pdfs"], 1)
            self.assertTrue(summary["coverage_complete"])
            rows = [json.loads(line) for line in (output / "paper-analysis.jsonl").read_text("utf-8").splitlines()]
            failed = next(row for row in rows if row["arxiv_id"] == "2501.00002")
            self.assertEqual(failed["execution_disposition"], "MANUAL_REVIEW_EXTRACTION_FAILED")
            self.assertTrue((output / "source-artifacts.jsonl").is_file())
            self.assertTrue((output / "extracted-text" / "2501.00001.txt").is_file())


if __name__ == "__main__":
    unittest.main(verbosity=2)
