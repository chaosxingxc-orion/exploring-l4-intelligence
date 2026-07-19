#!/usr/bin/env python3
"""Anchor-policy contract tests for survey PDF page locators."""
import os
import sys
import unittest


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sf_evidence_contract import (  # noqa: E402
    ROW_REQUIRED_FIELDS,
    check_page_locator,
    normalized_tokens,
)


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


if __name__ == "__main__":
    unittest.main()
