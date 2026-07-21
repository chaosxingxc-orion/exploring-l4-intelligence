#!/usr/bin/env python3
"""Focused contracts for the evidence-v7 platform leaf runner."""
from __future__ import annotations

import contextlib
import copy
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import sf_identity_taxonomy_v7_test as harness  # noqa: E402


class V7HarnessTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle = harness.load_current_inputs()

    def test_contract_names_the_new_absence_artifact_and_freeze(self):
        self.assertEqual("SF-EVIDENCE-V7-CONTRACT-2", harness.CONTRACT_VERSION)
        self.assertEqual(
            "d4ec803417e1e9cfe9120afbce97c676cebbe6ee",
            harness.IMPLEMENTATION_FREEZE,
        )
        self.assertEqual(
            "wiki/survey/current/data/absence-evidence-adjudication-v2.json",
            harness.ABSENCE_ADJUDICATION_RELATIVE_PATH,
        )
        self.assertEqual(
            "wiki/survey/current/data/negative-evidence-semantic-corrections-v1.json",
            harness.SEMANTIC_CORRECTIONS_RELATIVE_PATH,
        )

    def test_current_input_bundle_binds_sidecars_coding_and_absence_review(self):
        bundle = self.bundle
        self.assertEqual(8, len(bundle["sidecars"]))
        self.assertEqual(11, len(bundle["rows"]))
        self.assertEqual(19, len(bundle["absence_adjudication"]["proof_rows"]))
        self.assertEqual([], bundle["absence_adjudication"]["rows"])
        self.assertEqual(3, len(bundle["semantic_corrections"]["corrections"]))
        self.assertEqual([], bundle["semantic_corrections"]["review_rows"])
        paths = {
            entry["path"]
            for value in bundle["input_provenance"].values()
            for entry in (value if isinstance(value, list) else [value])
        }
        self.assertIn(harness.ABSENCE_ADJUDICATION_RELATIVE_PATH, paths)
        self.assertIn(harness.SEMANTIC_CORRECTIONS_RELATIVE_PATH, paths)

    def test_current_pending_review_blocks_all_three_semantic_corrections(self):
        failures = harness.validate_semantic_correction_review(self.bundle)
        self.assertIn(
            "semantic-correction-review-coverage-mismatch:expected=3:found=0",
            failures,
        )

    def test_positive_absence_mutation_is_red_and_legitimate_negative_is_clean(self):
        results = harness.run_absence_mutation_suite(self.bundle["rows"])
        self.assertEqual(
            [], results["legitimate_field_specific_negative_control"]
        )
        self.assertTrue(
            any(
                "absence-field-value-not-allowed" in failure
                for failure in results["positive_categorical_absence"]
            ),
            results,
        )

    def test_current_pending_review_blocks_all_19_cross_bindings(self):
        failures = harness.validate_absence_review(self.bundle)
        self.assertIn(
            "absence-review-coverage-mismatch:expected=19:found=0", failures
        )
        self.assertEqual(
            19,
            sum("absence-adjudication-row-missing" in failure for failure in failures),
        )

    def test_duplicate_review_ids_and_tampered_proof_rows_fail_inventory(self):
        bundle = copy.deepcopy(self.bundle)
        row_id = bundle["absence_adjudication"]["proof_rows"][0][
            "adjudication_row_id"
        ]
        bundle["absence_adjudication"]["rows"] = [
            {"adjudication_row_id": row_id},
            {"adjudication_row_id": row_id},
        ]
        bundle["absence_adjudication"]["proof_rows"][0]["owner_row_sha256"] = (
            "0" * 64
        )
        failures = harness.validate_review_inventory(bundle)
        self.assertTrue(any("duplicate-review-id" in failure for failure in failures))
        self.assertTrue(any("proof-row-binding-mismatch" in failure for failure in failures))

    def test_current_report_is_honest_fail_with_full_binding_metadata(self):
        report = harness.build_report(bundle=self.bundle, platform_os="nt")
        self.assertEqual("FAIL", report["verdict"])
        self.assertIn("ABSENCE_REVIEW", report["failure_codes"])
        self.assertIn("SEMANTIC_CORRECTION_REVIEW", report["failure_codes"])
        self.assertEqual(harness.CONTRACT_VERSION, report["contract_version"])
        self.assertEqual(harness.IMPLEMENTATION_FREEZE, report["implementation_freeze"])
        self.assertRegex(report["runner"]["sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual("nt", report["platform"]["os"])

    def test_leaf_writer_writes_only_the_requested_output(self):
        report = {
            "artifact_id": harness.ARTIFACT_ID,
            "contract_version": harness.CONTRACT_VERSION,
            "implementation_freeze": harness.IMPLEMENTATION_FREEZE,
            "runner": {"path": harness.RUNNER_RELATIVE_PATH, "sha256": "a" * 64},
            "input_provenance": {},
            "input_snapshot_sha256": "b" * 64,
            "platform": {"os": "nt", "sys_platform": "win32", "python": "3.14.3"},
            "checks": [],
            "occupancy": {},
            "mutation_results": {},
            "failure_codes": [],
            "summary": "0/0 PASS",
            "verdict": "PASS",
        }
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "leaf.json"
            with (
                mock.patch.object(harness, "build_report", return_value=report),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                self.assertEqual(
                    0,
                    harness.main(["--leaf", "--output", os.fspath(output)]),
                )
            self.assertEqual([output], list(Path(temporary).iterdir()))
            self.assertEqual(report, json.loads(output.read_text(encoding="utf-8")))

    def test_leaf_mode_and_output_are_required(self):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                harness.parse_args([])
            with self.assertRaises(SystemExit):
                harness.parse_args(["--leaf"])

    def test_report_encoding_is_deterministic_strict_utf8_lf(self):
        report = harness.build_report(bundle=self.bundle, platform_os="nt")
        first = harness.encode_report(report)
        second = harness.encode_report(copy.deepcopy(report))
        self.assertEqual(first, second)
        self.assertTrue(first.endswith(b"\n"))
        self.assertNotIn(b"\r", first)


if __name__ == "__main__":
    unittest.main()
