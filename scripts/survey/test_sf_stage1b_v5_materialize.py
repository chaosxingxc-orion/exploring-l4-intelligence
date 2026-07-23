#!/usr/bin/env python3
"""Contracts for the closed Stage-1B v5 corpus-to-current materialization."""

from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

import sf_stage1b_v5_materialize as materialize  # noqa: E402


class Stage1BV5MaterializeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputs = materialize.load_inputs(REPO)
        cls.reconciliation = materialize.build_reconciliation(cls.inputs)

    def test_closed_reconciliation_has_six_gate_and_twelve_route_works_once(self):
        rows = self.reconciliation["rows"]
        ids = [row["paper_work_id"] for row in rows]
        self.assertEqual(18, len(ids))
        self.assertEqual(18, len(set(ids)))
        self.assertEqual(materialize.CLOSED_RECONCILIATION_IDS, set(ids))
        self.assertEqual(materialize.GATE_IDS, {row["paper_work_id"] for row in rows if row["gate_work"]})
        self.assertEqual(6, len(materialize.GATE_IDS))
        self.assertEqual(12, len(materialize.CLOSED_RECONCILIATION_IDS - materialize.GATE_IDS))

    def test_every_reconciliation_row_has_official_metadata_and_local_hash(self):
        for row in self.reconciliation["rows"]:
            with self.subTest(paper=row["paper_work_id"]):
                self.assertTrue(row["official_metadata"]["authors"])
                self.assertEqual(
                    f"https://arxiv.org/abs/{row['paper_work_id']}",
                    row["official_metadata"]["stable_url"],
                )
                path = materialize.resolve_local_pdf(REPO, row["fulltext_ref"])
                self.assertTrue(path.is_file())
                self.assertEqual(row["fulltext_ref"]["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
                self.assertIn(row["asset_availability"]["status"], materialize.ASSET_STATUSES)
                self.assertTrue(row["route_reason"])

    def test_strict_supplement_adds_six_gate_rows_and_mugen(self):
        supplement = materialize.build_supplement(self.inputs["base_supplement"], self.reconciliation)
        ids = [row["paper_work_id"] for row in supplement["rows"]]
        self.assertEqual(46, len(ids))
        self.assertEqual(46, len(set(ids)))
        added = set(ids) - {
            row["paper_work_id"] for row in self.inputs["base_supplement"]["rows"]
        }
        self.assertEqual(materialize.GATE_IDS | {"2603.09714"}, added)
        self.assertEqual(26, sum(row["analysis_role"] == "DIRECT_CONTROL_METHOD" for row in supplement["rows"]))

    def test_control_basis_is_neutral_and_reward_guided_count_stays_zero(self):
        supplement = materialize.build_supplement(self.inputs["base_supplement"], self.reconciliation)
        control = materialize.build_control_basis(supplement, self.inputs["base_control"])
        self.assertEqual(26, len(control["rows"]))
        self.assertEqual(0, control["summary"]["REWARD_GUIDED_SELECTION"])
        self.assertEqual(8, control["summary"]["EVALUATOR_OR_VERIFIER_GATED"])
        self.assertTrue(
            all("control_signal_or_decision_component_identity" in row for row in control["rows"])
        )
        self.assertTrue(all("reward_or_evaluator_identity" not in row for row in control["rows"]))

    def test_appendix_covers_supplement_and_all_routed_only_rows(self):
        supplement = materialize.build_supplement(self.inputs["base_supplement"], self.reconciliation)
        appendix = materialize.render_reference_appendix(
            supplement,
            self.inputs["known_reconciliation"],
            self.reconciliation,
        )
        expected_ids = {
            row["paper_work_id"] for row in supplement["rows"]
        } | {
            row["paper_work_id"]
            for row in self.inputs["known_reconciliation"]["rows"]
        } | materialize.CLOSED_RECONCILIATION_IDS
        self.assertEqual(59, len(expected_ids))
        for paper_id in expected_ids:
            self.assertEqual(1, appendix.count(f"<!-- work:{paper_id} -->"), paper_id)


if __name__ == "__main__":
    unittest.main()
