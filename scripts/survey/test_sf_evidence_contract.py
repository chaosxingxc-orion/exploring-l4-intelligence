#!/usr/bin/env python3
"""Anchor-policy contract tests for survey PDF page locators."""
import os
import sys
import unittest
from copy import deepcopy


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sf_evidence_contract import (  # noqa: E402
    ROW_REQUIRED_FIELDS,
    check_page_locator,
    normalized_tokens,
    validate_bound_values,
    values_equal,
)


def binding(value):
    return {"kind": "canon", "value": value, "quote": "claim-bearing quote"}


def generic_row():
    row = {
        "method_path_id": "__fx12__#path",
        "core_weight_update": False,
        "external_component_weight_update": False,
        "controller_program_or_config_optimized_on_labels": False,
        "human_or_dev_label_model_selection": False,
        "deployment_label_access": False,
        "test_item_gold_access": False,
        "inference_external_new_information": False,
        "internal_visibility": "api_only",
        "core_topology": "single_core",
        "core_native_modality": "omni_native",
        "control_horizon": "sequential",
        "decision_rights": ["branch"],
        "candidate_pool_exists": True,
        "selection_policy": "scored_select",
        "selection_object": "candidate_output",
        "explicit_candidate_pool_selection": True,
    }
    row["claim_evidence"] = {
        field: binding(row[field]) for field in ROW_REQUIRED_FIELDS
    }
    signal = {
        "signal_id": "s1",
        "form": "scalar_score",
        "source": "llm_judge",
        "lifecycle": "online_step",
        "uses": ["prune"],
        "claim_evidence": {},
    }
    signal["claim_evidence"] = {
        field: binding(signal[field])
        for field in ("form", "source", "lifecycle", "uses")
    }
    edge = {
        "signal_id": "s1",
        "signal_use": "prune",
        "decision_right": "branch",
        "claim_evidence": {},
    }
    edge["claim_evidence"] = {
        field: binding(edge[field]) for field in ("signal_use", "decision_right")
    }
    row["signals"] = [signal]
    row["control_edges"] = [edge]
    return row


class FakePage:
    def __init__(self, text):
        self.text = text

    def extract_text(self):
        return self.text


class FakeReader:
    def __init__(self, page_texts):
        self.pages = [FakePage(text) for text in page_texts]


class RaisingPage:
    def extract_text(self):
        raise RuntimeError("unreadable PDF page")


class CountingPage(FakePage):
    def __init__(self, text):
        super().__init__(text)
        self.calls = 0

    def extract_text(self):
        self.calls += 1
        return super().extract_text()


class AnchorPolicyTest(unittest.TestCase):
    def setUp(self):
        self.reader = FakeReader(
            [
                "the method introduction",
                "the orchestrator decides every explore and stop action in context",
                "the appendix repeats common words but not the claim-bearing phrase",
            ]
        )

    def failures(self, locator):
        out = []
        check_page_locator(locator, self.reader, "fx#row", "row-locator", out)
        return out

    def test_page_token_without_anchor_fails(self):
        failures = self.failures("p1")
        self.assertTrue(any("page-token-without-anchor" in failure for failure in failures))

    def test_weak_anchor_fails(self):
        failures = self.failures("p1 anchor='the'")
        self.assertTrue(any("page-anchor-too-weak" in failure for failure in failures))

    def test_non_discriminative_anchor_fails(self):
        reader = FakeReader(["common method description"] * 4)
        out = []
        check_page_locator(
            "p2 anchor='common method description'",
            reader,
            "fx#row",
            "row-locator",
            out,
        )
        self.assertTrue(
            any("page-anchor-not-discriminative" in failure for failure in out)
        )

    def test_claim_bearing_anchor_passes(self):
        self.assertEqual(
            self.failures("p2 anchor='decides every explore and stop action'"), []
        )

    def test_missing_anchor_fails(self):
        failures = self.failures("p2 anchor='candidate majority controls termination'")
        self.assertTrue(any("page-anchor-missing" in failure for failure in failures))

    def test_row_required_fields_are_ordered_contract_list(self):
        self.assertEqual(
            ROW_REQUIRED_FIELDS,
            [
                "core_weight_update",
                "external_component_weight_update",
                "controller_program_or_config_optimized_on_labels",
                "human_or_dev_label_model_selection",
                "deployment_label_access",
                "test_item_gold_access",
                "inference_external_new_information",
                "internal_visibility",
                "core_topology",
                "core_native_modality",
                "control_horizon",
                "decision_rights",
                "candidate_pool_exists",
                "selection_policy",
                "selection_object",
                "explicit_candidate_pool_selection",
            ],
        )

    def test_normalized_tokens_accepts_none(self):
        self.assertEqual(normalized_tokens(None), [])

    def test_none_locator_is_empty(self):
        self.assertEqual(self.failures(None), [])

    def test_leading_zero_page_errors_use_canonical_page_number(self):
        self.assertEqual(
            self.failures("p01"),
            ["fx#row:row-locator:page-token-without-anchor:p1"],
        )
        self.assertEqual(
            self.failures("p01 anchor='the'"),
            ["fx#row:row-locator:page-anchor-too-weak:p1:the"],
        )

    def test_anchor_cannot_match_across_page_boundary(self):
        reader = FakeReader(["distinctive orchestrator", "controls"])
        out = []
        check_page_locator(
            "p1 anchor='distinctive orchestrator controls'",
            reader,
            "fx#row",
            "row-locator",
            out,
        )
        self.assertEqual(
            out,
            [
                "fx#row:row-locator:page-anchor-missing:"
                "p1:distinctive orchestrator controls"
            ],
        )

    def test_anchor_requires_exact_token_sequence_at_suffix_and_prefix(self):
        for page_text in (
            "candidate majority controls terminations",
            "uncandidate majority controls termination",
        ):
            reader = FakeReader([page_text])
            out = []
            check_page_locator(
                "p1 anchor='candidate majority controls termination'",
                reader,
                "fx#row",
                "row-locator",
                out,
            )
            self.assertEqual(
                out,
                [
                    "fx#row:row-locator:page-anchor-missing:"
                    "p1:candidate majority controls termination"
                ],
            )

    def test_page_tokens_inside_strong_anchor_are_not_extra_locators(self):
        reader = FakeReader(["method compares p2 outcome"])
        out = []
        check_page_locator(
            "p1 anchor='method compares p2 outcome'",
            reader,
            "fx#row",
            "row-locator",
            out,
        )
        self.assertEqual(out, [])

    def test_extraction_error_fails_closed(self):
        reader = FakeReader([])
        reader.pages = [FakePage("decides every explore and stop action"), RaisingPage()]
        out = []
        check_page_locator(
            "p1 anchor='decides every explore and stop action'",
            reader,
            "fx#row",
            "row-locator",
            out,
        )
        self.assertEqual(out, ["fx#row:row-locator:pdf-unreadable-for-page-check"])

    def test_document_is_extracted_once_for_multiple_strong_locators(self):
        pages = [
            CountingPage("decides every explore and stop action"),
            CountingPage("candidate majority controls termination"),
        ]
        reader = FakeReader([])
        reader.pages = pages
        out = []
        check_page_locator(
            "p1 anchor='decides every explore and stop action'; "
            "p2 anchor='candidate majority controls termination'",
            reader,
            "fx#row",
            "row-locator",
            out,
        )
        self.assertEqual(out, [])
        self.assertEqual([page.calls for page in pages], [1, 1])


class BoundValueTest(unittest.TestCase):
    def failures(self, row):
        return validate_bound_values(row)

    def test_complete_generic_row_passes(self):
        self.assertEqual(self.failures(generic_row()), [])

    def test_signal_source_must_match_its_evidence_value(self):
        row = deepcopy(generic_row())
        row["signals"][0]["source"] = "learned_rm_prm"
        failures = self.failures(row)
        self.assertTrue(
            any(
                "signal:s1:source:evidence-value-mismatch" in failure
                for failure in failures
            )
        )

    def test_edge_signal_use_must_match_its_evidence_value(self):
        row = deepcopy(generic_row())
        row["signals"][0]["uses"] = ["select"]
        row["signals"][0]["claim_evidence"]["uses"]["value"] = ["select"]
        row["control_edges"][0]["signal_use"] = "select"
        failures = self.failures(row)
        self.assertTrue(
            any(
                "edge:0:signal_use:evidence-value-mismatch" in failure
                for failure in failures
            )
        )

    def test_edge_decision_right_must_match_its_evidence_value(self):
        row = deepcopy(generic_row())
        row["control_edges"][0]["decision_right"] = "supply"
        failures = self.failures(row)
        self.assertTrue(
            any(
                "edge:0:decision_right:evidence-value-mismatch" in failure
                for failure in failures
            )
        )

    def test_selection_object_must_match_its_evidence_value(self):
        row = deepcopy(generic_row())
        row["selection_object"] = "trajectory"
        failures = self.failures(row)
        self.assertTrue(
            any(
                "row:selection_object:evidence-value-mismatch" in failure
                for failure in failures
            )
        )

    def test_explicit_pool_selection_must_match_its_evidence_value(self):
        row = deepcopy(generic_row())
        row["explicit_candidate_pool_selection"] = False
        failures = self.failures(row)
        self.assertTrue(
            any(
                "row:explicit_candidate_pool_selection:evidence-value-mismatch"
                in failure
                for failure in failures
            )
        )

    def test_edge_decision_right_requires_evidence(self):
        row = deepcopy(generic_row())
        del row["control_edges"][0]["claim_evidence"]["decision_right"]
        failures = self.failures(row)
        self.assertTrue(
            any(
                "edge:0:decision_right:required-evidence-missing" in failure
                for failure in failures
            )
        )

    def test_boolean_evidence_integer_value_is_a_mismatch(self):
        row = deepcopy(generic_row())
        row["claim_evidence"]["core_weight_update"]["value"] = 1
        self.assertIn(
            "__fx12__#path:row:core_weight_update:evidence-value-mismatch",
            self.failures(row),
        )

    def test_values_equal_requires_identical_concrete_types(self):
        self.assertFalse(values_equal(True, 1))
        self.assertFalse(values_equal(1, True))

    def test_absent_row_field_with_null_evidence_is_encoded_field_missing(self):
        row = deepcopy(generic_row())
        del row["selection_object"]
        row["claim_evidence"]["selection_object"]["value"] = None
        self.assertIn(
            "__fx12__#path:row:selection_object:encoded-field-missing",
            self.failures(row),
        )

    def test_list_claim_evidence_is_invalid_container(self):
        row = deepcopy(generic_row())
        row["claim_evidence"] = []
        self.assertIn(
            "__fx12__#path:row:core_weight_update:evidence-container-invalid",
            self.failures(row),
        )

    def test_string_evidence_entry_is_invalid(self):
        row = deepcopy(generic_row())
        row["claim_evidence"]["selection_object"] = "not a mapping"
        self.assertIn(
            "__fx12__#path:row:selection_object:evidence-entry-invalid",
            self.failures(row),
        )

    def test_none_signals_is_invalid_container(self):
        row = deepcopy(generic_row())
        row["signals"] = None
        self.assertIn(
            "__fx12__#path:signals:container-invalid", self.failures(row)
        )

    def test_invalid_evidence_kind_fails(self):
        row = deepcopy(generic_row())
        row["claim_evidence"]["selection_object"]["kind"] = "unsupported"
        self.assertIn(
            "__fx12__#path:row:selection_object:evidence-kind-invalid",
            self.failures(row),
        )

    def test_unhashable_list_items_mismatch_without_exception(self):
        row = deepcopy(generic_row())
        row["decision_rights"] = [{"branch": True}]
        row["claim_evidence"]["decision_rights"]["value"] = [{"branch": True}]
        self.assertIn(
            "__fx12__#path:row:decision_rights:evidence-value-mismatch",
            self.failures(row),
        )

    def test_non_mapping_row_is_invalid_container(self):
        self.assertEqual(self.failures([]), ["?:row:container-invalid"])

    def test_non_mapping_signal_and_edge_entries_are_invalid(self):
        row = deepcopy(generic_row())
        row["signals"] = [None]
        row["control_edges"] = [None]
        self.assertEqual(
            self.failures(row),
            [
                "__fx12__#path:signal:0:entry-invalid",
                "__fx12__#path:edge:0:entry-invalid",
            ],
        )


if __name__ == "__main__":
    unittest.main()
