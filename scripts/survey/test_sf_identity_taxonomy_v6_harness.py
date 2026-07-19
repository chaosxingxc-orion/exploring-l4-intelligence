#!/usr/bin/env python3
"""Focused unit and integration tests for the active taxonomy-v6 harness."""
from __future__ import annotations

import copy
import inspect
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

import sf_evidence_contract as evidence  # noqa: E402
import sf_identity_taxonomy_v5_test as legacy  # noqa: E402
import sf_identity_taxonomy_v6_test as harness  # noqa: E402
import sf_row_hash as shared_hash  # noqa: E402


class HarnessContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sidecars, cls.coding_text, cls.rows = harness.load_current_inputs()

    def test_v5_derivation_and_structure_remain_the_single_source(self):
        self.assertIs(harness.derive, legacy.derive)
        self.assertIs(harness.run_expectations, legacy.run_expectations)
        self.assertIs(harness.validate, legacy.validate)
        self.assertIs(harness.row_hash, shared_hash.row_hash)
        self.assertIsNot(harness.row_hash, getattr(harness, "derive", None))

    def test_active_paths_are_v6_v7_schema_v3_only(self):
        self.assertEqual(
            Path(harness.TAX).relative_to(REPO).as_posix(),
            "wiki/survey/current/data/identity-taxonomy-v6.json",
        )
        self.assertEqual(
            Path(harness.CODING).relative_to(REPO).as_posix(),
            "wiki/survey/current/data/known-item-coding-v7.json",
        )
        self.assertEqual(
            Path(harness.SIDECAR_DIR).relative_to(REPO).as_posix(),
            "wiki/survey/current/data/schema-v3/sidecars",
        )
        self.assertEqual(
            Path(harness.OUT).relative_to(REPO).as_posix(),
            "docs/checks/system-first-stage1a/evidence-v6/"
            "identity-taxonomy-v6-test.json",
        )

    def test_contract_validation_calls_structure_then_bindings_then_source(self):
        calls = []

        def structure(rows):
            calls.append(("structure", rows))
            return ["structure-failure"]

        def binding(row):
            calls.append(("binding", row))
            return [f"binding-{row}"]

        def source(sidecars, coding_text):
            calls.append(("source", sidecars, coding_text))
            return ["source-failure"]

        with (
            mock.patch.object(harness, "validate", side_effect=structure),
            mock.patch.object(
                harness, "validate_bound_values", side_effect=binding
            ),
            mock.patch.object(harness, "reconcile_v6", side_effect=source),
        ):
            result = harness.validate_load_bearing_contract(
                ["row-a", "row-b"], [("sidecar", {})], "coding"
            )

        self.assertEqual(
            [entry[0] for entry in calls],
            ["structure", "binding", "binding", "source"],
        )
        self.assertEqual(result["structure"], ["structure-failure"])
        self.assertEqual(result["bindings"], ["binding-row-a", "binding-row-b"])
        self.assertEqual(result["source"], ["source-failure"])

    def test_reconcile_renders_the_active_v7_profile(self):
        with mock.patch.object(harness, "render", return_value="coding") as render:
            self.assertEqual(harness.reconcile_v6([], "coding"), [])
        render.assert_called_once_with(
            [], taxonomy=harness.ACTIVE_TAXONOMY, profile="v7"
        )

    def test_schema_v3_status_is_fail_closed(self):
        sidecars = copy.deepcopy(self.sidecars)
        sidecars[0][1]["schema_v3_binding_status"] = "PENDING_INDEPENDENT_ADJUDICATION"
        failures = harness.reconcile_v6(sidecars, harness.render_v7(sidecars))
        self.assertIn(
            f"{sidecars[0][1]['paper_work_id']}:"
            "schema-v3-binding-status:PENDING_INDEPENDENT_ADJUDICATION",
            failures,
        )

    def test_every_pdf_page_binding_scope_reaches_strong_locator_checker(self):
        calls = []

        def record(locator, reader, pid, what, failures):
            calls.append((locator, pid, what))

        with mock.patch.object(harness, "check_page_locator", side_effect=record):
            failures = harness.reconcile_v6(self.sidecars, self.coding_text)

        self.assertEqual(failures, [])
        whats = {what for _, _, what in calls}
        self.assertTrue(any(what == "row-locator" for what in whats))
        self.assertTrue(any(what.startswith("signal:") for what in whats))
        self.assertTrue(any(what == "edge-locator" for what in whats))
        self.assertTrue(any(what.startswith("row-binding:") for what in whats))
        self.assertTrue(any(what.startswith("signal-binding:") for what in whats))
        self.assertTrue(any(what.startswith("edge-binding:") for what in whats))

        expected_pdf_bindings = sum(
            entry.get("kind") == "pdf_page"
            for row in self.rows
            for entry in row["claim_evidence"].values()
        ) + sum(
            entry.get("kind") == "pdf_page"
            for row in self.rows
            for signal in row["signals"]
            for entry in signal["claim_evidence"].values()
        ) + sum(
            entry.get("kind") == "pdf_page"
            for row in self.rows
            for edge in row["control_edges"]
            for entry in edge["claim_evidence"].values()
        )
        binding_calls = [call for call in calls if "-binding:" in call[2]]
        self.assertEqual(len(binding_calls), expected_pdf_bindings)

    def test_generic_twelfth_row_is_structurally_and_evidentially_clean(self):
        row = harness.generic_row()
        self.assertEqual(legacy.validate([row]), [])
        self.assertEqual(evidence.validate_bound_values(row), [])

    def test_generic_twelfth_row_mutations_fail_for_generic_binding_codes(self):
        cases = []

        source = harness.generic_row()
        source["signals"][0]["source"] = "learned_rm_prm"
        cases.append((source, "signal:s1:source:evidence-value-mismatch"))

        use = harness.generic_row()
        use["signals"][0]["uses"] = ["select"]
        use["signals"][0]["claim_evidence"]["uses"]["value"] = ["select"]
        use["control_edges"][0]["signal_use"] = "select"
        cases.append((use, "edge:0:signal_use:evidence-value-mismatch"))

        selection = harness.generic_row()
        selection["selection_object"] = "trajectory"
        cases.append((selection, "row:selection_object:evidence-value-mismatch"))

        missing = harness.generic_row()
        del missing["control_edges"][0]["claim_evidence"]["decision_right"]
        cases.append((missing, "edge:0:decision_right:required-evidence-missing"))

        for row, expected in cases:
            with self.subTest(expected=expected):
                self.assertTrue(
                    any(
                        expected in failure
                        for failure in evidence.validate_bound_values(row)
                    )
                )

    def test_twelfth_row_id_occurs_only_in_the_fixture(self):
        source = inspect.getsource(harness)
        self.assertEqual(source.count("__fx12__#path"), 1)

    def test_occupancy_is_the_frozen_v5_shape_and_exact_baseline(self):
        occ = harness.occupancy(
            ("single_core", "single_core_multi_call"), self.rows
        )
        self.assertEqual(occ["is_reward_guided"]["n_paths"], "6/11")
        self.assertEqual(
            occ["is_rq_sys_control_compatible"]["n_paths"], "5/11"
        )
        self.assertEqual(occ["is_project_method_candidate"]["n_paths"], "0/11")
        self.assertEqual(occ["reward_guided_selection"]["n_paths"], "4/11")
        trajectory = occ[
            "strict_AND_reward_AND_pool_BY_selection_object(mechanism)"
        ]["trajectory"]
        self.assertEqual(trajectory["n_paths"], "2/11")

    def test_report_serialization_is_strict_deterministic_utf8_lf(self):
        report = {
            "artifact_id": "fixture",
            "platform": {"os": "nt", "python": "3.14.3"},
            "verdict": "PASS",
        }
        first = harness.encode_report(report)
        second = harness.encode_report(copy.deepcopy(report))
        self.assertEqual(first, second)
        self.assertTrue(first.endswith(b"\n"))
        self.assertNotIn(b"\r", first)
        self.assertEqual(json.loads(first.decode("utf-8")), report)

        with self.assertRaises(ValueError):
            harness.encode_report({"not_finite": float("nan")})

        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "report.json"
            harness.write_report(report, output)
            initial = output.read_bytes()
            harness.write_report(report, output)
            self.assertEqual(output.read_bytes(), initial)
            self.assertEqual(list(Path(temporary).iterdir()), [output])


class MutationIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sidecars, coding_text, _ = harness.load_current_inputs()
        cls.clean, cls.results, cls.ok = harness.run_mutation_suite(
            sidecars, coding_text
        )

    def test_mutation_baseline_is_clean_and_all_cases_are_red(self):
        self.assertEqual(self.clean, {"source": [], "structure": [], "bindings": []})
        self.assertTrue(self.ok)

    def test_mutation_names_include_frozen_and_schema_v3_cases(self):
        required = {
            "E1_edge_use_flip",
            "E2_signal_evidence_p9999",
            "E3_bare_in_range_page",
            "E3b_generic_anchor_the",
            "E3c_frequent_phrase",
            "E4_signal_form_flip",
            "E5_coding_hand_edit",
            "E6_signal_source_flip",
            "E7_edge_use_coherent_flip",
            "E8_edge_right_coherent_flip",
            "E9_selection_object_flip",
            "E10_explicit_selection_flip",
            "E11_missing_signal_source_binding",
            "E12_missing_edge_right_binding",
            "wrong_horizon",
            "double_flip_horizon_plus_evidence",
        }
        self.assertTrue(required <= set(self.results))

    def test_new_legitimate_rehash_mutations_fail_for_specific_contracts(self):
        expected = {
            "E3b_generic_anchor_the": "page-anchor-too-weak",
            "E3c_frequent_phrase": "page-anchor-not-discriminative",
            "E6_signal_source_flip": "signal:s_stage_judge:source:evidence-value-mismatch",
            "E7_edge_use_coherent_flip": "edge:0:signal_use:evidence-value-mismatch",
            "E8_edge_right_coherent_flip": "edge:0:decision_right:evidence-value-mismatch",
            "E9_selection_object_flip": "row:selection_object:evidence-value-mismatch",
            "E10_explicit_selection_flip": (
                "row:explicit_candidate_pool_selection:evidence-value-mismatch"
            ),
            "E11_missing_signal_source_binding": (
                "signal:s_stage_judge:source:required-evidence-missing"
            ),
            "E12_missing_edge_right_binding": (
                "edge:0:decision_right:required-evidence-missing"
            ),
        }
        for name, code in expected.items():
            with self.subTest(name=name):
                failures = self.results[name]
                self.assertTrue(any(code in failure for failure in failures), failures)
                self.assertFalse(any("row-hash" in failure for failure in failures))


if __name__ == "__main__":
    unittest.main()
