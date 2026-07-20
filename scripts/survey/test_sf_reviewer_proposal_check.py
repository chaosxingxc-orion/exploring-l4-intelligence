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

    def test_release_fails_until_independent_review_and_v7_exist(self):
        failures = checker.validate_release(self.proposal, self.inputs)
        self.assertIn("ABSENCE_REVIEW_PENDING", failures)
        self.assertIn("EVIDENCE_V7_LEAVES_OR_AGGREGATE_MISSING", failures)
        self.assertIn("PROPOSAL_NOT_PROMOTED_TO_ROUND15", failures)

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
            ("479 个物理 source rows", "UNION_NUMERIC_DRIFT"),
            ("241 个 canonical work nodes", "UNION_NUMERIC_DRIFT"),
            ("77 个 unique works", "BIBLIOGRAPHY_NUMERIC_DRIFT"),
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
