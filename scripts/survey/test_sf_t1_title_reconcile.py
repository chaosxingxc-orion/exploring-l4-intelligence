#!/usr/bin/env python3
"""Tests for work-level reconciliation of matched T1 proceedings titles."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import sf_t1_title_reconcile as reconcile


class ReconciliationTests(unittest.TestCase):
    def test_title_key_collapses_punctuation_case_and_spacing(self):
        self.assertEqual(
            reconcile.title_key("Training-Free:  Agent/Control"),
            reconcile.title_key("training free agent control"),
        )

    def test_known_index_deduplicates_same_work_across_sources(self):
        records = [
            {"arxiv_id": "2601.00001", "title": "Agent Control"},
            {"arxiv_id": "2601.00001", "title": "Agent Control"},
        ]
        index = reconcile.build_known_index(records)
        self.assertEqual(index[reconcile.title_key("Agent Control")], {"2601.00001"})

    def test_reconcile_aggregates_route_provenance_and_marks_ambiguity(self):
        report = {
            "rows": [
                {
                    "route_id": "R1",
                    "disposition": "EXECUTED",
                    "matched_titles": [{"title": "Agent Control"}, {"title": "Venue Only"}],
                },
                {
                    "route_id": "R2",
                    "disposition": "EXECUTED",
                    "matched_titles": [{"title": "Agent Control"}],
                },
            ]
        }
        index = reconcile.build_known_index(
            [
                {"arxiv_id": "2601.00001", "title": "Agent Control"},
                {"arxiv_id": "2601.00002", "title": "Agent-Control"},
            ]
        )
        rows, summary = reconcile.reconcile_titles(report, index)
        by_title = {row["canonical_title_key"]: row for row in rows}
        agent = by_title[reconcile.title_key("Agent Control")]
        venue = by_title[reconcile.title_key("Venue Only")]
        self.assertEqual(agent["route_ids"], ["R1", "R2"])
        self.assertEqual(agent["resolution"], "KNOWN_WORK_AMBIGUOUS")
        self.assertEqual(venue["resolution"], "UNRESOLVED_TITLE")
        self.assertEqual(summary["matched_title_events"], 3)
        self.assertEqual(summary["unique_title_keys"], 2)

    def test_cli_writes_hash_bound_report(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            t1 = root / "t1.json"
            known = root / "known.jsonl"
            output = root / "out.json"
            t1.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "route_id": "R1",
                                "disposition": "EXECUTED",
                                "matched_titles": [{"title": "Agent Control"}],
                            }
                        ]
                    }
                ),
                "utf-8",
            )
            known.write_text(
                json.dumps({"arxiv_id": "2601.00001", "title": "Agent Control"}) + "\n",
                "utf-8",
            )
            result = reconcile.run(t1, [known], output)
            persisted = json.loads(output.read_text("utf-8"))
        self.assertEqual(result["summary"]["known_unique"], 1)
        self.assertEqual(len(persisted["inputs"]["known_jsonl"]), 1)
        self.assertRegex(persisted["inputs"]["t1_report_sha256"], r"^[0-9a-f]{64}$")


if __name__ == "__main__":
    unittest.main(verbosity=2)
