#!/usr/bin/env python3
"""Tests for the Stage-1B arXiv BFS candidate snapshot builder."""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))

import sf_bfs_candidate_builder as builder


ATOM = b"""<?xml version='1.0' encoding='UTF-8'?>
<feed xmlns='http://www.w3.org/2005/Atom'
      xmlns:arxiv='http://arxiv.org/schemas/atom'>
  <entry>
    <id>https://arxiv.org/abs/2601.00002v2</id>
    <updated>2026-02-01T00:00:00Z</updated>
    <published>2026-01-01T00:00:00Z</published>
    <title>  Second   Paper </title>
    <summary>Second abstract.</summary>
    <author><name>Beta Author</name></author>
    <category term='cs.AI'/>
  </entry>
  <entry>
    <id>https://arxiv.org/abs/2601.00001v1</id>
    <updated>2026-01-02T00:00:00Z</updated>
    <published>2026-01-01T00:00:00Z</published>
    <title>First Paper</title>
    <summary> First abstract. </summary>
    <author><name>Alpha Author</name></author>
    <category term='cs.CL'/>
  </entry>
</feed>
"""


def row(raw: Path, query_id: str = "SF-L1-Q1") -> dict:
    return {
        "query_id": query_id,
        "query_ref": "frozen-row-hash",
        "request_role": "RESULT_PAGE",
        "page_start": 0,
        "timestamp": "2026-07-21T00:00:00Z",
        "raw_response_ref": raw.as_posix(),
        "response_sha256": hashlib.sha256(ATOM).hexdigest(),
        "included": ["2601.00002", "2601.00001"],
        "failed_request": None,
    }


class CandidateBuilderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.raw = self.root / "page.atom"
        self.raw.write_bytes(ATOM)
        self.rec1 = self.root / "rec1.jsonl"

    def tearDown(self):
        self.temp.cleanup()

    def write_rows(self, rows: list[dict]) -> None:
        self.rec1.write_text(
            "".join(json.dumps(item) + "\n" for item in rows), encoding="utf-8"
        )

    def test_collects_sorted_candidates_and_normalizes_metadata(self):
        self.write_rows([row(self.raw)])
        candidates, stats = builder.collect_candidates(self.rec1)
        self.assertEqual([item["arxiv_id"] for item in candidates], ["2601.00001", "2601.00002"])
        self.assertEqual(candidates[1]["versions"], ["v2"])
        self.assertEqual(candidates[1]["title"], "Second Paper")
        self.assertEqual(candidates[1]["authors"], ["Beta Author"])
        self.assertEqual(candidates[1]["categories"], ["cs.AI"])
        self.assertEqual(candidates[1]["screening_decision"], "PENDING")
        self.assertEqual(stats["unique_candidates"], 2)
        self.assertEqual(stats["active_failures"], 0)

    def test_deduplicates_work_but_preserves_query_lineage(self):
        self.write_rows([row(self.raw), row(self.raw, "SF-L3-Q2")])
        candidates, stats = builder.collect_candidates(self.rec1)
        self.assertEqual(len(candidates), 2)
        self.assertEqual(len(candidates[0]["source_events"]), 2)
        self.assertEqual(candidates[0]["source_query_ids"], ["SF-L1-Q1", "SF-L3-Q2"])
        self.assertEqual(stats["successful_pages"], 2)

    def test_fails_closed_on_raw_hash_mismatch(self):
        bad = row(self.raw)
        bad["response_sha256"] = "0" * 64
        self.write_rows([bad])
        with self.assertRaisesRegex(builder.CandidateBuildError, "hash mismatch"):
            builder.collect_candidates(self.rec1)

    def test_fails_closed_when_logged_ids_differ_from_atom(self):
        bad = row(self.raw)
        bad["included"] = ["2601.00001"]
        self.write_rows([bad])
        with self.assertRaisesRegex(builder.CandidateBuildError, "included IDs differ"):
            builder.collect_candidates(self.rec1)

    def test_writer_is_deterministic_jsonl(self):
        self.write_rows([row(self.raw)])
        candidates, _ = builder.collect_candidates(self.rec1)
        out1 = self.root / "one.jsonl"
        out2 = self.root / "two.jsonl"
        builder.write_candidates(out1, candidates)
        builder.write_candidates(out2, candidates)
        self.assertEqual(out1.read_bytes(), out2.read_bytes())
        self.assertTrue(out1.read_bytes().endswith(b"\n"))

    def test_parser_rejects_invalid_xml_and_unrecognized_entry_id(self):
        with self.assertRaisesRegex(builder.CandidateBuildError, "invalid Atom XML"):
            builder._parse_atom(b"<feed>")
        bad_id = ATOM.replace(
            b"https://arxiv.org/abs/2601.00002v2", b"https://example.org/not-arxiv"
        )
        with self.assertRaisesRegex(builder.CandidateBuildError, "unrecognized arXiv entry id"):
            builder._parse_atom(bad_id)

    def test_reader_and_provenance_fail_closed_before_candidate_creation(self):
        self.rec1.write_text("{not json}\n", encoding="utf-8")
        with self.assertRaisesRegex(builder.CandidateBuildError, "invalid JSON"):
            builder.collect_candidates(self.rec1)

        missing_ref = row(self.raw)
        missing_ref["raw_response_ref"] = None
        self.write_rows([missing_ref])
        with self.assertRaisesRegex(builder.CandidateBuildError, "lacks raw/hash"):
            builder.collect_candidates(self.rec1)

        absent = row(self.root / "absent.atom")
        self.write_rows([absent])
        with self.assertRaisesRegex(builder.CandidateBuildError, "raw response missing"):
            builder.collect_candidates(self.rec1)

    def test_failure_and_probe_accounting_retains_but_supersedes_failure(self):
        failed = row(self.raw)
        failed.update(
            {
                "timestamp": "2026-07-21T00:00:00Z",
                "failed_request": "TimeoutError",
                "raw_response_ref": None,
                "response_sha256": None,
                "included": [],
            }
        )
        probe = row(self.raw, "SF-L1-Q1-probe")
        probe.update(
            {
                "request_role": "SPLIT_COUNT_PROBE",
                "timestamp": "2026-07-21T00:01:00Z",
                "retry_of_timestamp": failed["timestamp"],
            }
        )
        self.write_rows([failed, probe])
        candidates, stats = builder.collect_candidates(self.rec1)
        self.assertEqual(candidates, [])
        self.assertEqual(stats["failed_rows_retained"], 1)
        self.assertEqual(stats["split_count_probes_skipped"], 1)
        self.assertEqual(stats["active_failures"], 0)

    def test_main_writes_candidate_and_stats_artifacts(self):
        self.write_rows([row(self.raw)])
        output = self.root / "nested" / "candidates.jsonl"
        stats_path = self.root / "stats" / "summary.json"
        argv = [
            "sf_bfs_candidate_builder.py",
            "--rec1",
            str(self.rec1),
            "--output",
            str(output),
            "--stats",
            str(stats_path),
        ]
        with mock.patch.object(sys, "argv", argv):
            self.assertEqual(builder.main(), 0)
        self.assertTrue(output.is_file())
        stats = json.loads(stats_path.read_text("utf-8"))
        self.assertEqual(stats["unique_candidates"], 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
