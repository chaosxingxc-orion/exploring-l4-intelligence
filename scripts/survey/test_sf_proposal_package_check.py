#!/usr/bin/env python3
"""Contracts for the honest pre-review proposal package report."""
from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import sf_proposal_package_check as package  # noqa: E402


class ProposalPackageCheckTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = package.build_report()

    def test_pre_review_construction_passes_without_claiming_release(self):
        self.assertEqual("PASS", self.report["construction_verdict"])
        self.assertEqual("BLOCKED", self.report["release_verdict"])
        self.assertFalse(self.report["release_eligible"])
        self.assertEqual([], self.report["construction_failure_codes"])

    def test_release_blockers_are_exact_and_honest(self):
        self.assertEqual(
            {
                "EVIDENCE_V7_LEAVES_OR_AGGREGATE_MISSING",
                "H5_CALIBRATION_PENDING",
                "PROPOSAL_NOT_PROMOTED_TO_ROUND16",
            },
            set(self.report["release_blockers"]),
        )
        self.assertEqual(
            {"H5_CALIBRATION"},
            set(self.report["v7_expected_pre_review_failures"]),
        )

    def test_all_construction_components_pass(self):
        self.assertTrue(self.report["components"])
        self.assertTrue(all(row["result"] == "PASS" for row in self.report["components"]))

    def test_unexpected_green_release_or_component_failure_is_rejected(self):
        mutated = copy.deepcopy(self.report)
        mutated["release_eligible"] = True
        self.assertIn("PRE_REVIEW_RELEASE_ELIGIBILITY_FORBIDDEN", package.validate_report(mutated))
        mutated = copy.deepcopy(self.report)
        mutated["components"][0]["result"] = "FAIL"
        self.assertIn("CONSTRUCTION_COMPONENT_FAILED", package.validate_report(mutated))

    def test_write_check_and_drift(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "package.json"
            package.write_report(self.report, output)
            self.assertEqual([], package.check_report(self.report, output))
            output.write_text("{}\n", encoding="utf-8")
            self.assertEqual(["PROPOSAL_PACKAGE_REPORT_DRIFT"], package.check_report(self.report, output))


if __name__ == "__main__":
    unittest.main()
