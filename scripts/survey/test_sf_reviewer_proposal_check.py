#!/usr/bin/env python3
"""Contracts for the reviewer proposal draft and its release boundary."""
from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import sf_reviewer_proposal_check as checker  # noqa: E402


class ReviewerProposalCheckTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proposal = checker.PROPOSAL_PATH.read_text(encoding="utf-8")
        cls.inputs = checker.load_inputs()

    def test_current_workbench_draft_is_complete_and_honest(self):
        self.assertEqual([], checker.validate_draft(self.proposal, self.inputs))

    def test_rqs_separate_mapping_products_from_later_empirical_tests(self):
        required = (
            "answering_stage",
            "Stage-1B evidence product",
            "later empirical test",
            "falsifier",
            "Stage-1B eligible inputs",
            "Stage-1C owns the final 3–5 candidate cards",
        )
        for token in required:
            with self.subTest(token=token):
                self.assertIn(token, self.proposal)

    def test_proposal_discloses_exact_negative_inventory_reconciliation(self):
        for token in (
            "exactly 3/22 implementer concerns",
            "19 个 proof rows、0 个 reviewer rows",
            "22 = 3 + 19",
            "negative-evidence-semantic-corrections-v1.json",
        ):
            self.assertIn(token, self.proposal)

    def test_methods_and_speech_omni_codebooks_are_current_inputs(self):
        methods = checker.MAPPING_METHODS_PATH.read_text(encoding="utf-8")
        modality = checker.MODALITY_CODEBOOK_PATH.read_text(encoding="utf-8")
        for token in (
            "Petersen",
            "Wohlin",
            "PRISMA 2020",
            "PRESS 2015",
            "adopted element",
            "deviation/rationale",
        ):
            self.assertIn(token, methods)
        for token in (
            "modality topology",
            "temporal regime",
            "observation granularity",
            "acoustic evidence provenance",
            "latency/action timing",
            "output/action modality",
            "state persistence",
            "UNKNOWN",
            "NOT_APPLICABLE",
            "dual disagreement",
        ):
            self.assertIn(token, modality)

    def test_bibliography_scope_selection_and_year_policy_are_explicit(self):
        for token in (
            "seven registered active corpora",
            "reviewer-bibliography-selection-v1.json",
            "NOT_SELECTED_NONPRIORITY_KNOWN_QUEUE",
            "initial_preprint",
            "formal_venue",
            "current_version",
            "Llasa",
            "OmniGAIA",
            "Omni-RRM",
            "Multimodal RewardBench 2",
        ):
            self.assertIn(token, self.proposal)

    def test_proposal_names_the_exact_source_manifest_and_honest_package_report(self):
        for token in (
            "proposal-source-manifest-v1.json",
            "proposal-package-check.json",
            "construction=PASS",
            "release=BLOCKED",
        ):
            self.assertIn(token, self.proposal)

    def test_release_fails_until_independent_review_and_v7_exist(self):
        failures = checker.validate_release(self.proposal, self.inputs)
        self.assertIn("ABSENCE_REVIEW_PENDING", failures)
        self.assertIn("SEMANTIC_CORRECTION_REVIEW_PENDING", failures)
        self.assertIn("EVIDENCE_V7_LEAVES_OR_AGGREGATE_MISSING", failures)
        self.assertIn("PROPOSAL_NOT_PROMOTED_TO_ROUND16", failures)

    def test_release_requires_19_active_plus_3_correction_reviews(self):
        mutated_inputs = copy.deepcopy(self.inputs)
        absence = mutated_inputs["absence"]
        absence["status"] = "INDEPENDENT_REVIEW_RECORDED_UNVALIDATED"
        absence["rows"] = [
            {
                "adjudication_row_id": row["adjudication_row_id"],
                "verdict": "AGREE",
            }
            for row in absence["proof_rows"]
        ]
        corrections = mutated_inputs["corrections"]
        corrections["review_rows"] = [
            {
                "retired_adjudication_row_id": row["retired_adjudication_row_id"],
                "verdict": "AGREE",
            }
            for row in corrections["corrections"]
        ]
        failures = checker.validate_release(self.proposal, mutated_inputs)
        self.assertNotIn("ABSENCE_REVIEW_PENDING", failures)
        self.assertNotIn("SEMANTIC_CORRECTION_REVIEW_PENDING", failures)

    def test_missing_track_response_schema_or_falsifier_fails(self):
        for token, code in (
            ("## Track A", "TRACK_A_MISSING"),
            ("## Track B", "TRACK_B_MISSING"),
            (
                "SCIENTIFIC_RATIONALE_FOR_CONTINUING_MAPPING = ADEQUATE|REVISE|INADEQUATE",
                "RESPONSE_SCHEMA_MISSING",
            ),
            ("## 8. 证伪条件", "FALSIFIERS_MISSING"),
        ):
            with self.subTest(token=token):
                mutated = self.proposal.replace(token, "REMOVED", 1)
                self.assertIn(code, checker.validate_draft(mutated, self.inputs))

    def test_actual_verdict_or_authorization_claim_fails(self):
        for injected, code in (
            (
                "\nSCIENTIFIC_RATIONALE_FOR_CONTINUING_MAPPING = ADEQUATE\n",
                "ACTUAL_REVIEWER_VERDICT_FORBIDDEN",
            ),
            ("\nSEARCH_DESIGN_SIGNOFF = SIGN\n", "ACTUAL_REVIEWER_VERDICT_FORBIDDEN"),
            ("\nexecution_authorized=true\n", "STAGE1B_AUTHORIZATION_FORBIDDEN"),
            ("\nSTAGE1B_READY\n", "STAGE1B_AUTHORIZATION_FORBIDDEN"),
            (
                "\nFOUR_IMPLEMENTATION_FINDINGS_REMEDIATED\n",
                "FOUR_FINDINGS_CLOSURE_FORBIDDEN_WHILE_PENDING",
            ),
        ):
            with self.subTest(injected=injected.strip()):
                self.assertIn(
                    code,
                    checker.validate_draft(self.proposal + injected, self.inputs),
                )

    def test_pending_counts_are_derived_from_absence_artifact(self):
        mutated_inputs = copy.deepcopy(self.inputs)
        proof = mutated_inputs["absence"]["proof_rows"][0]
        mutated_inputs["absence"]["rows"] = [
            {
                "adjudication_row_id": proof["adjudication_row_id"],
                "verdict": "AGREE",
            }
        ]
        self.assertIn(
            "ABSENCE_COUNT_DRIFT",
            checker.validate_draft(self.proposal, mutated_inputs),
        )

    def test_union_and_bibliography_numbers_are_derived(self):
        for old, code in (
            ("483 个物理 source rows", "UNION_NUMERIC_DRIFT"),
            ("245 个 canonical work nodes", "UNION_NUMERIC_DRIFT"),
            ("85 个 unique works", "BIBLIOGRAPHY_NUMERIC_DRIFT"),
        ):
            with self.subTest(old=old):
                mutated = self.proposal.replace(old, old.replace(old.split()[0], "999"), 1)
                self.assertIn(code, checker.validate_draft(mutated, self.inputs))

    def test_git_blob_evidence_table_rejects_wrong_hash(self):
        mutated = self.proposal.replace(
            "5aafddb9d32d085462f619e739cb3d1f8b47740d39d88b0cfc6b38f99e7f9623",
            "0" * 64,
            1,
        )
        self.assertIn("EVIDENCE_BINDING_MISMATCH", checker.validate_draft(mutated, self.inputs))

    def test_cli_draft_passes_and_release_fails(self):
        self.assertEqual(0, checker.main(["--mode", "draft"]))
        self.assertEqual(1, checker.main(["--mode", "release"]))

    def test_machine_report_can_be_written_outside_repo(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "proposal-check.json"
            self.assertEqual(
                0,
                checker.main(["--mode", "draft", "--output", str(output)]),
            )
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual("PASS", report["verdict"])
            self.assertEqual("draft", report["mode"])


if __name__ == "__main__":
    unittest.main()
