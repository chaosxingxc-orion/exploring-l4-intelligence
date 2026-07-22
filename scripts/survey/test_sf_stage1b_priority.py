#!/usr/bin/env python3
"""Tests for the Stage-1B abstract-review priority queue builder."""

from __future__ import annotations

import json
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))

import sf_stage1b_priority as priority


def candidate(
    arxiv_id: str,
    title: str,
    abstract: str,
    queries: list[str] | None = None,
    published: str = "2026-01-01T00:00:00Z",
) -> dict:
    return {
        "arxiv_id": arxiv_id,
        "title": title,
        "abstract": abstract,
        "published": published,
        "source_query_ids": queries or ["SF-L1-Q1"],
        "screening_decision": "PENDING",
        "coding_depth": "D0",
    }


class PriorityQueueTests(unittest.TestCase):
    def test_score_exposes_lexical_evidence_and_trigger_suggestions(self):
        row = candidate(
            "2601.00001",
            "Training-Free Reward-Guided Decoding for Omni Models",
            "A frozen model uses verifier feedback to select and stop. Failure cases remain.",
            ["SF-L14-Q2", "SF-L15-Q1"],
        )
        scored = priority.score_candidate(row)
        self.assertGreater(scored["priority_score"], 0)
        self.assertIn("T-a", scored["trigger_suggestions"])
        self.assertIn("T-b", scored["trigger_suggestions"])
        self.assertIn("T-c", scored["trigger_suggestions"])
        self.assertIn("T-d", scored["trigger_suggestions"])
        self.assertIn("reward", scored["lexical_evidence"]["control_signal"])
        self.assertEqual(scored["review_state"], "ABSTRACT_REVIEW_PENDING")
        self.assertTrue(scored["not_a_screening_decision"])
        self.assertNotIn("screening_decision", scored)

    def test_rank_excludes_seen_and_is_deterministic_for_ties(self):
        rows = [
            candidate("2601.00002", "Audio agent", "Uses search and feedback."),
            candidate("2601.00001", "Audio agent", "Uses search and feedback."),
            candidate("2601.00003", "Audio agent", "Uses search and feedback."),
        ]
        ranked = priority.rank_candidates(rows, excluded_ids={"2601.00003"})
        self.assertEqual([row["arxiv_id"] for row in ranked], ["2601.00001", "2601.00002"])
        self.assertEqual(ranked, priority.rank_candidates(list(reversed(rows)), {"2601.00003"}))

    def test_forced_known_item_enters_queue_without_query_recall_credit(self):
        rows = [
            candidate("2601.00001", "Generic paper", "Unrelated abstract."),
            candidate("2601.00002", "Audio reward search", "Verifier-guided selection."),
        ]
        ranked = priority.rank_candidates(
            rows,
            excluded_ids=set(),
            forced_ids={"2601.00001": "protocol blind-spot counterexample"},
        )
        self.assertEqual(ranked[0]["arxiv_id"], "2601.00001")
        self.assertTrue(ranked[0]["forced_entry"])
        self.assertFalse(ranked[0]["query_recall_credit_for_forced_entry"])
        self.assertEqual(ranked[0]["forced_reason"], "protocol blind-spot counterexample")

    def test_loader_fails_closed_on_duplicate_ids_and_missing_fields(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "candidates.jsonl"
            row = candidate("2601.00001", "Title", "Abstract")
            path.write_text(json.dumps(row) + "\n" + json.dumps(row) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(priority.PriorityBuildError, "duplicate arXiv ID"):
                priority.load_candidates(path)
            path.write_text(json.dumps({"arxiv_id": "2601.00002"}) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(priority.PriorityBuildError, "missing required fields"):
                priority.load_candidates(path)

    def test_writer_emits_bounded_jsonl_and_summary(self):
        rows = [
            candidate("2601.00001", "Audio reward search", "Verifier selection."),
            candidate("2601.00002", "Vision reward search", "Critic selection."),
        ]
        ranked = priority.rank_candidates(rows, set())
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / "queue.jsonl"
            summary = priority.write_queue(out, ranked, limit=1)
            payload = [json.loads(line) for line in out.read_text("utf-8").splitlines()]
            self.assertEqual(len(payload), 1)
            self.assertEqual(summary["eligible_candidates"], 2)
            self.assertEqual(summary["queue_rows_written"], 1)
            self.assertEqual(summary["screening_decisions_made"], 0)

    def test_invalid_json_limit_and_forced_value_fail_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "bad.jsonl"
            path.write_text("{not-json}\n", encoding="utf-8")
            with self.assertRaisesRegex(priority.PriorityBuildError, "invalid JSON"):
                priority.load_candidates(path)
            with self.assertRaisesRegex(priority.PriorityBuildError, "limit"):
                priority.write_queue(Path(temp) / "out.jsonl", [], limit=0)
            with self.assertRaisesRegex(priority.PriorityBuildError, "ARXIV_ID"):
                priority._parse_forced(["2601.00001="])

    def test_cli_writes_queue_and_summary_from_notes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "input.jsonl"
            output = root / "queue.jsonl"
            summary_path = root / "summary.json"
            notes = root / "notes.md"
            rows = [
                candidate("2601.00001", "Audio reward search", "Verifier selection."),
                candidate("2601.00002", "Generic", "No control signal."),
            ]
            source.write_text(
                "".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8"
            )
            notes.write_text("Previously handled: 2601.00002\n", encoding="utf-8")
            argv = [
                "sf_stage1b_priority.py",
                "--input", str(source),
                "--output", str(output),
                "--summary", str(summary_path),
                "--exclude-notes", str(notes),
                "--force-id", "2601.00001=sentinel",
                "--limit", "1",
            ]
            with patch.object(sys, "argv", argv), redirect_stdout(io.StringIO()):
                self.assertEqual(priority.main(), 0)
            summary = json.loads(summary_path.read_text("utf-8"))
            queued = json.loads(output.read_text("utf-8"))
            self.assertEqual(summary["eligible_candidates"], 1)
            self.assertEqual(summary["excluded_ids"], 1)
            self.assertTrue(queued["forced_entry"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
