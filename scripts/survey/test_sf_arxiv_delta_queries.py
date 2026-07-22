#!/usr/bin/env python3
"""Tests for append-only Stage-1B arXiv date-delta query generation."""

from __future__ import annotations

import copy
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))

import sf_arxiv_delta_queries as delta


def frozen_row() -> dict:
    body = {
        "query_id": "SF-L1-Q1",
        "lane": "SF-L1",
        "decoded_search_query": "(cat:cs.AI) AND submittedDate:[202210010000 TO 202607152359] AND abs:agent",
        "url_encoded_search_query": "old-encoded-value",
        "categories": ["cs.AI"],
        "date_from": "202210010000",
        "date_to": "202607152359",
        "start": 0,
        "max_results": 75,
        "sortBy": "relevance",
        "sortOrder": "descending",
        "compiler_version": "sfqc-test",
    }
    body["record_sha256"] = delta.record_hash(body)
    return body


class DeltaQueryTests(unittest.TestCase):
    def test_builds_closed_increment_without_mutating_parent(self):
        parent = frozen_row()
        before = copy.deepcopy(parent)
        child = delta.make_delta_row(parent, "202607160000", "202607212359")
        self.assertEqual(parent, before)
        self.assertEqual(child["query_id"], "SF-L1-Q1-D20260716-20260721")
        self.assertIn("submittedDate:[202607160000 TO 202607212359]", child["decoded_search_query"])
        self.assertEqual(child["date_from"], "202607160000")
        self.assertEqual(child["date_to"], "202607212359")
        self.assertEqual(child["parent_record_sha256"], parent["record_sha256"])
        self.assertEqual(child["delta_semantics"], "APPEND_ONLY_CLOSED_INTERVAL")
        self.assertEqual(delta.record_hash({k: v for k, v in child.items() if k != "record_sha256"}), child["record_sha256"])

    def test_rejects_invalid_range_hash_and_ambiguous_date_clause(self):
        with self.assertRaisesRegex(delta.DeltaQueryError, "date range"):
            delta.make_delta_row(frozen_row(), "202607220000", "202607212359")
        bad_hash = frozen_row()
        bad_hash["record_sha256"] = "0" * 64
        with self.assertRaisesRegex(delta.DeltaQueryError, "parent hash"):
            delta.make_delta_row(bad_hash, "202607160000", "202607212359")
        ambiguous = frozen_row()
        ambiguous["decoded_search_query"] += " OR submittedDate:[202001010000 TO 202101010000]"
        ambiguous["record_sha256"] = delta.record_hash(
            {k: v for k, v in ambiguous.items() if k != "record_sha256"}
        )
        with self.assertRaisesRegex(delta.DeltaQueryError, "exactly one"):
            delta.make_delta_row(ambiguous, "202607160000", "202607212359")

    def test_manifest_is_deterministic_and_parent_prefix_remains_byte_identical(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            parent_path = root / "frozen.jsonl"
            output1 = root / "delta1.jsonl"
            output2 = root / "delta2.jsonl"
            payload = json.dumps(frozen_row(), ensure_ascii=False) + "\n"
            parent_path.write_text(payload, encoding="utf-8", newline="\n")
            original = parent_path.read_bytes()
            summary1 = delta.generate_manifest(parent_path, output1, "202607160000", "202607212359")
            summary2 = delta.generate_manifest(parent_path, output2, "202607160000", "202607212359")
            self.assertEqual(parent_path.read_bytes(), original)
            self.assertEqual(output1.read_bytes(), output2.read_bytes())
            self.assertEqual(summary1["delta_rows"], 1)
            self.assertEqual(summary1["output_sha256"], summary2["output_sha256"])

    def test_manifest_rejects_invalid_json_and_duplicate_child_ids(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            parent = root / "parent.jsonl"
            parent.write_text("{bad-json}\n", encoding="utf-8")
            with self.assertRaisesRegex(delta.DeltaQueryError, "invalid JSON"):
                delta.generate_manifest(parent, root / "out.jsonl", "202607160000", "202607212359")

            row = frozen_row()
            parent.write_text(
                json.dumps(row) + "\n" + json.dumps(row) + "\n", encoding="utf-8"
            )
            with self.assertRaisesRegex(delta.DeltaQueryError, "duplicate delta query IDs"):
                delta.generate_manifest(parent, root / "out.jsonl", "202607160000", "202607212359")

    def test_cli_writes_manifest_and_summary(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            parent = root / "parent.jsonl"
            output = root / "delta.jsonl"
            summary_path = root / "summary.json"
            parent.write_text(json.dumps(frozen_row()) + "\n", encoding="utf-8")
            argv = [
                "sf_arxiv_delta_queries.py",
                "--parent", str(parent),
                "--output", str(output),
                "--date-from", "202607160000",
                "--date-to", "202607212359",
                "--summary", str(summary_path),
            ]
            with patch.object(sys, "argv", argv), redirect_stdout(io.StringIO()):
                self.assertEqual(delta.main(), 0)
            self.assertTrue(output.exists())
            self.assertEqual(json.loads(summary_path.read_text("utf-8"))["delta_rows"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
