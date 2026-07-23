#!/usr/bin/env python3
"""Focused contracts for the Stage-1B v5 transition repair."""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

import sf_stage1b_v5_evidence_contract as contract  # noqa: E402


class Stage1BV5EvidenceContractTests(unittest.TestCase):
    def test_repository_v5_contract(self):
        raw = os.environ.get("SPEECHRL_DATA_DIR")
        if raw:
            data_root = Path(raw)
        elif os.name == "nt":
            data_root = Path(r"E:\chao_workspace\exploring-l4-intelligence\speechrl-data")
        else:
            data_root = Path("/mnt/e/chao_workspace/exploring-l4-intelligence/speechrl-data")
        receipt = contract.validate_repository(REPO, data_root=data_root)
        self.assertEqual("PASS", receipt["status"], receipt["failures"])
        self.assertEqual(18, receipt["facts"]["closed_reconciliation_works"])
        self.assertEqual({"direct": 26, "instrument": 18, "boundary": 2}, receipt["facts"]["supplement_roles"])
        self.assertEqual({"orchestration": 9, "state_event": 9, "evaluator_verifier": 8, "reward_guided": 0}, receipt["facts"]["control_basis"])
        self.assertTrue(receipt["facts"]["inventory_semantic_parity"])


if __name__ == "__main__":
    unittest.main()
