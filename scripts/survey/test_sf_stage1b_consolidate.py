#!/usr/bin/env python3
"""Tests for the bounded Stage-1B retained-paper consolidation."""

from __future__ import annotations

import sys
import json
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import sf_stage1b_consolidate as consolidate


def row(aid: str, decision: str, local: str = "NOT_STATED_IN_FULLTEXT") -> dict:
    return {
        "arxiv_id": aid,
        "title": aid,
        "final_decision": decision,
        "dataset_local_status": local,
        "control_signal_terms": ["verifier"],
        "decision_action_terms": ["search"],
        "speech_task_tags": ["asr"] if decision == "KEEP_CORE" else [],
        "evidence_locators": [{"page": 1}],
    }


class ConsolidationTests(unittest.TestCase):
    def test_keeps_only_final_keep_labels_and_respects_cap(self):
        rows = [
            row("2601.00001", "KEEP_CORE", "LOCAL_MATCH"),
            row("2601.00002", "KEEP_TRANSFER"),
            row("2601.00003", "DROP"),
            row("2601.00004", "KEEP_NEGATIVE"),
        ]
        kept = consolidate.consolidate(rows, cap=2)
        self.assertEqual([item["arxiv_id"] for item in kept], ["2601.00001", "2601.00002"])
        self.assertTrue(all(item["retained_rank"] <= 2 for item in kept))

    def test_cap_is_maximum_not_quota(self):
        kept = consolidate.consolidate([row("2601.00001", "KEEP_INSTRUMENT")], cap=1000)
        self.assertEqual(len(kept), 1)

    def test_non_speech_local_math_dataset_does_not_raise_transfer_priority(self):
        first = row("2601.00001", "KEEP_TRANSFER", "LOCAL_MATCH")
        first["speech_primary_object"] = False
        second = row("2601.00002", "KEEP_TRANSFER")
        second["speech_primary_object"] = False
        self.assertEqual(consolidate._score(first), consolidate._score(second))

    def test_duplicate_canonical_id_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            consolidate.consolidate(
                [row("2601.00001", "KEEP_CORE"), row("2601.00001", "KEEP_TRANSFER")],
                cap=1000,
            )

    def test_audit_override_requires_matching_prior_decision_and_reason(self):
        source_row = row("2601.00001", "KEEP_CORE")
        source_row["dataset_mentions"] = [{"canonical_name": "librispeech", "task": "asr"}]
        source_row["speech_dataset_mentions"] = [{"canonical_name": "librispeech", "task": "asr"}]
        rows = [source_row]
        changed = consolidate.apply_overrides(
            rows,
            [
                {
                    "arxiv_id": "2601.00001",
                    "from_decision": "KEEP_CORE",
                    "to_decision": "KEEP_INSTRUMENT",
                    "reason": "Method updates weights at test time; retain only as a direct comparator.",
                    "evidence_pages": [3, 5],
                    "speech_task_tags": ["asr", "ser"],
                    "speech_primary_object": True,
                    "dataset_local_status": "LOCAL_MATCH",
                }
            ],
        )
        self.assertEqual(changed[0]["final_decision"], "KEEP_INSTRUMENT")
        self.assertEqual(changed[0]["decision_origin"], "BOUNDED_FULLTEXT_AUDIT_OVERRIDE")
        self.assertEqual(changed[0]["speech_task_tags"], ["asr", "ser"])
        self.assertTrue(changed[0]["speech_primary_object"])
        self.assertEqual(changed[0]["dataset_local_status"], "LOCAL_MATCH")
        suitability = changed[0]["speech_dataset_mentions"][0]
        self.assertEqual(suitability["task_suitability_by_tag"], {"asr": "TASK_MATCH", "ser": "REQUIRES_SPLIT_REVIEW"})
        with self.assertRaisesRegex(ValueError, "from_decision"):
            consolidate.apply_overrides(rows, [{"arxiv_id": "2601.00001", "from_decision": "DROP", "to_decision": "KEEP_CORE", "reason": "x", "evidence_pages": [1]}])

    def test_audit_override_can_record_named_dataset_absent_from_local_lock(self):
        changed = consolidate.apply_overrides(
            [row("2601.00001", "DROP")],
            [
                {
                    "arxiv_id": "2601.00001",
                    "from_decision": "DROP",
                    "to_decision": "KEEP_INSTRUMENT",
                    "reason": "The speech task is relevant, but its named corpus is not in the local lock.",
                    "evidence_pages": [1, 3],
                    "speech_primary_object": True,
                    "dataset_local_status": "NAMED_DATASET_NOT_IN_LOCK",
                }
            ],
        )
        self.assertEqual(changed[0]["dataset_local_status"], "NAMED_DATASET_NOT_IN_LOCK")

    def test_run_writes_hash_bound_roster_and_summary(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            kept_row = row("2601.00001", "KEEP_CORE")
            kept_row["sample_round"] = 5
            source = root / "triage.jsonl"
            source.write_text(
                "\n".join(json.dumps(item) for item in [kept_row, row("2601.00002", "DROP")])
                + "\n",
                encoding="utf-8",
            )
            summary = consolidate.run(source, root / "out", cap=1000)
            self.assertEqual(summary["retained_unique"], 1)
            self.assertEqual(summary["unresolved_rows_at_consolidation"], 0)
            self.assertEqual(summary["maximum_sample_round_seen"], 5)
            self.assertFalse(summary["scan_stop_after_round_3"])
            self.assertTrue(summary["scan_stop_after_bounded_batch"])
            self.assertTrue((root / "out" / "retained-papers.jsonl").is_file())
            self.assertTrue((root / "out" / "retained-roster-summary.json").is_file())

    def test_run_merges_multiple_ledgers_before_capping(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            first = root / "first.jsonl"
            second = root / "second.jsonl"
            first.write_text(json.dumps(row("2601.00001", "KEEP_CORE")) + "\n", encoding="utf-8")
            second.write_text(json.dumps(row("2601.00002", "KEEP_TRANSFER")) + "\n", encoding="utf-8")
            summary = consolidate.run([first, second], root / "out", cap=1000)
            self.assertEqual(summary["source_input_count"], 2)
            self.assertEqual(summary["source_rows"], 2)
            self.assertEqual(summary["retained_unique"], 2)

    def test_run_applies_multiple_override_receipts(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source.jsonl"
            source.write_text(
                json.dumps(row("2601.00001", "DROP")) + "\n" + json.dumps(row("2601.00002", "DROP")) + "\n",
                encoding="utf-8",
            )
            override_paths = []
            for index, aid in enumerate(("2601.00001", "2601.00002"), start=1):
                path = root / f"override-{index}.json"
                path.write_text(
                    json.dumps(
                        [
                            {
                                "arxiv_id": aid,
                                "from_decision": "DROP",
                                "to_decision": "KEEP_TRANSFER",
                                "reason": "Human full-text audit found a reproducible transfer path.",
                                "evidence_pages": [1],
                            }
                        ]
                    ),
                    encoding="utf-8",
                )
                override_paths.append(path)
            summary = consolidate.run(source, root / "out", cap=1000, overrides_path=override_paths)
            self.assertEqual(summary["audit_override_receipt_count"], 2)
            self.assertEqual(summary["audit_override_count"], 2)
            self.assertEqual(summary["retained_unique"], 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
