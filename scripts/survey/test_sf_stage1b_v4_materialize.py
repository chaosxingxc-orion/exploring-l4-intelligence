#!/usr/bin/env python3
"""Contracts for deterministic Stage-1B v4 supplement materialization."""

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

import sf_stage1b_v4_materialize as materialize  # noqa: E402


class Stage1BV4MaterializeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = json.loads((REPO / materialize.BASE_PATH).read_text(encoding="utf-8"))
        cls.reconciliation = json.loads(
            (REPO / materialize.RECONCILIATION_PATH).read_text(encoding="utf-8")
        )

    def test_supplement_adds_only_seven_reconciled_rows(self):
        document = materialize.build_supplement(self.base, self.reconciliation)
        ids = [row["paper_work_id"] for row in document["rows"]]
        self.assertEqual(39, len(ids))
        self.assertEqual(39, len(set(ids)))
        self.assertEqual(25, sum(row["analysis_role"] == "DIRECT_CONTROL_METHOD" for row in document["rows"]))
        self.assertEqual(set(materialize.ADDITIONAL_SUPPLEMENT_ROWS), set(ids) - {row["paper_work_id"] for row in self.base["rows"]})

    def test_cli_materialization_is_deterministic(self):
        before_supplement = (REPO / materialize.SUPPLEMENT_PATH).read_bytes()
        before_control = (REPO / materialize.CONTROL_BASIS_PATH).read_bytes()
        self.assertEqual(0, materialize.main())
        self.assertEqual(before_supplement, (REPO / materialize.SUPPLEMENT_PATH).read_bytes())
        self.assertEqual(before_control, (REPO / materialize.CONTROL_BASIS_PATH).read_bytes())

    def test_control_basis_covers_every_direct_row_once(self):
        supplement = materialize.build_supplement(self.base, self.reconciliation)
        control = materialize.build_control_basis(supplement)
        direct_ids = {
            row["paper_work_id"]
            for row in supplement["rows"]
            if row["analysis_role"] == "DIRECT_CONTROL_METHOD"
        }
        control_ids = [row["paper_work_id"] for row in control["rows"]]
        self.assertEqual(direct_ids, set(control_ids))
        self.assertEqual(len(direct_ids), len(control_ids))
        self.assertTrue(
            all(row["control_basis"] in materialize.ALLOWED_CONTROL_BASES for row in control["rows"])
        )

    def test_missing_control_classification_fails_closed(self):
        supplement = materialize.build_supplement(self.base, self.reconciliation)
        broken = copy.deepcopy(supplement)
        broken["rows"].append(
            {
                **next(row for row in broken["rows"] if row["analysis_role"] == "DIRECT_CONTROL_METHOD"),
                "paper_work_id": "9999.99999",
                "evidence_id": "DP-9999.99999",
            }
        )
        with self.assertRaisesRegex(ValueError, "missing control_basis"):
            materialize.build_control_basis(broken)


if __name__ == "__main__":
    unittest.main()
