#!/usr/bin/env python3
"""Contracts for the three-paper H5 dual-coder calibration gate."""
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import sf_h5_calibration_contract as contract  # noqa: E402


class H5CalibrationContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = contract.load_calibration()

    def test_current_scaffold_is_structurally_bound_but_not_complete(self):
        self.assertEqual([], contract.validate_structure(self.document))
        self.assertEqual([], contract.validate_locators(self.document))
        failures = contract.validate_completion(self.document)
        self.assertIn("H5_SECOND_INDEPENDENT_CODER_MISSING", failures)
        self.assertIn("H5_PAIRWISE_AGREEMENT_INCOMPLETE", failures)
        self.assertEqual(
            "PENDING_BLIND_CODER_B", self.document["status"]
        )

    def test_exact_three_paper_and_twenty_one_field_denominators(self):
        self.assertEqual(contract.CALIBRATION_PAPER_IDS, tuple(
            row["identity"]["id"] for row in self.document["papers"]
        ))
        coder = self.document["coders"][0]
        self.assertEqual(21, len(coder["assignments"]))
        self.assertEqual(21, self.document["agreement_report"]["planned_denominator"])

    def test_tampered_fulltext_hash_fails_closed(self):
        mutated = copy.deepcopy(self.document)
        mutated["papers"][0]["fulltext"]["pdf_sha256"] = "0" * 64
        self.assertIn(
            "H5_FULLTEXT_LEDGER_BINDING_MISMATCH:2510.02995",
            contract.validate_structure(mutated),
        )

    def test_duplicate_or_partial_coder_fails_closed(self):
        mutated = copy.deepcopy(self.document)
        duplicate = copy.deepcopy(mutated["coders"][0])
        duplicate["assignments"] = duplicate["assignments"][:-1]
        mutated["coders"].append(duplicate)
        failures = contract.validate_structure(mutated)
        self.assertIn("H5_DUPLICATE_CODER_ID", failures)
        self.assertTrue(any("H5_ASSIGNMENT_DENOMINATOR" in item for item in failures))

    def test_complete_state_requires_adjudication_for_every_disagreement(self):
        mutated = copy.deepcopy(self.document)
        second = copy.deepcopy(mutated["coders"][0])
        second["coder_id"] = "independent-coder-b"
        second["independent_of_implementer"] = True
        mutated["coders"].append(second)
        mutated["status"] = "COMPLETE"
        mutated["agreement_report"].update(
            {
                "observed_comparable_denominator": 21,
                "exact_agreement_numerator": 20,
                "exact_agreement_rate": 20 / 21,
                "disagreements": [
                    {
                        "paper_id": "2510.02995",
                        "field": "modality_topology",
                        "coder_values": {
                            "codex-primary-round17-v2-recode": "text_only",
                            "independent-coder-b": "audio_native_single",
                        },
                        "adjudication": None,
                    }
                ],
            }
        )
        self.assertIn(
            "H5_DISAGREEMENT_UNADJUDICATED:2510.02995:modality_topology",
            contract.validate_completion(mutated),
        )

    def _completed_pair(self):
        mutated = copy.deepcopy(self.document)
        second = copy.deepcopy(mutated["coders"][0])
        second["coder_id"] = "independent-coder-b"
        second["independent_of_implementer"] = True
        mutated["coders"].append(second)
        mutated["status"] = "COMPLETE"
        mutated["agreement_report"].update(
            {
                "observed_comparable_denominator": 21,
                "exact_agreement_numerator": 21,
                "exact_agreement_rate": 1.0,
                "disagreements": [],
            }
        )
        return mutated

    def test_reported_full_agreement_is_rejected_when_all_values_disagree(self):
        mutated = self._completed_pair()
        for assignment in mutated["coders"][1]["assignments"]:
            current = assignment["value"]
            assignment["value"] = next(
                value
                for value in sorted(contract.FIELD_VALUES[assignment["field"]])
                if value != current
            )

        self.assertIn(
            "H5_AGREEMENT_DERIVATION_MISMATCH",
            contract.validate_completion(mutated),
        )

    def test_illegal_adjudication_is_rejected(self):
        mutated = self._completed_pair()
        second_assignment = mutated["coders"][1]["assignments"][0]
        second_assignment["value"] = "audio_native_single"
        mutated["agreement_report"].update(
            {
                "exact_agreement_numerator": 20,
                "exact_agreement_rate": 20 / 21,
                "disagreements": [
                    {
                        "paper_id": "2510.02995",
                        "field": "modality_topology",
                        "coder_values": {
                            "codex-primary-round16-remediation": "text_only",
                            "independent-coder-b": "audio_native_single",
                        },
                        "adjudication": {
                            "adjudicator_id": "independent-coder-b",
                            "final_value": "not-an-allowed-value",
                            "rationale": "invalid mutation",
                        },
                    }
                ],
            }
        )

        failures = contract.validate_completion(mutated)
        self.assertIn(
            "H5_ADJUDICATOR_NOT_INDEPENDENT:2510.02995:modality_topology",
            failures,
        )
        self.assertIn(
            "H5_ADJUDICATION_VALUE_INVALID:2510.02995:modality_topology",
            failures,
        )


if __name__ == "__main__":
    unittest.main()
