#!/usr/bin/env python3
"""Contracts for the frozen dual-platform PDF extractor environment."""
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import sf_pdf_extractor_contract as contract  # noqa: E402


class PdfExtractorContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = contract.load_contract()

    def test_contract_binds_both_canonical_environments_and_probe(self):
        self.assertEqual([], contract.validate_contract(self.document))
        self.assertEqual({"nt", "posix"}, set(self.document["canonical_environments"]))
        self.assertEqual(11, self.document["toolgate_probe"]["page"])
        self.assertEqual(
            "8025d9126a14e6a07dab30fa93183bf1aa25fa9df2b753d18653549b50caa857",
            self.document["toolgate_probe"]["pdf_sha256"],
        )

    def test_exact_runtime_version_is_required(self):
        stamp = copy.deepcopy(self.document["canonical_environments"]["nt"])
        self.assertEqual([], contract.validate_runtime(self.document, stamp))
        stamp["pypdf_version"] = "6.14.1"
        self.assertEqual(
            ["PDF_EXTRACTOR_RUNTIME_MISMATCH"],
            contract.validate_runtime(self.document, stamp),
        )

    def test_tampered_probe_or_environment_fails_closed(self):
        mutated = copy.deepcopy(self.document)
        mutated["toolgate_probe"]["anchor"] = "too short"
        mutated["canonical_environments"]["posix"]["extractor_identity"] = "wrong"
        failures = contract.validate_contract(mutated)
        self.assertIn("PDF_EXTRACTOR_IDENTITY_MISMATCH:posix", failures)
        self.assertIn("PDF_EXTRACTOR_PROBE_CONTRACT_MISMATCH", failures)

    def test_current_platform_replays_toolgate_page_11(self):
        stamp = contract.runtime_stamp()
        self.assertEqual([], contract.validate_runtime(self.document, stamp))
        result = contract.replay_toolgate_probe(self.document)
        self.assertEqual("PASS", result["result"])
        self.assertTrue(result["anchor_found"])


if __name__ == "__main__":
    unittest.main()
