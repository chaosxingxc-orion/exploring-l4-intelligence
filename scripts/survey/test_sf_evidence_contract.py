#!/usr/bin/env python3
"""Anchor-policy contract tests for survey PDF page locators."""
import os
import sys
import unittest


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sf_evidence_contract import check_page_locator  # noqa: E402


class FakePage:
    def __init__(self, text):
        self.text = text

    def extract_text(self):
        return self.text


class FakeReader:
    def __init__(self, page_texts):
        self.pages = [FakePage(text) for text in page_texts]


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


if __name__ == "__main__":
    unittest.main()
