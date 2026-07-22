#!/usr/bin/env python3
"""Tests for deterministic Stage-1B registry views."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import sf_stage1b_registry_views as views


def _record(
    aid: str,
    role: str,
    *,
    speech: bool = False,
    tasks: list[str] | None = None,
    datasets: list[dict] | None = None,
    repo_status: str = "NO_REPOSITORY_EVIDENCE",
) -> dict:
    return {
        "schema": "sf-paper-registry-record-v1",
        "canonical_id": f"arxiv:{aid}",
        "arxiv_id": aid,
        "title": f"Paper {aid}",
        "role": role,
        "speech_primary_object": speech,
        "speech_task_tags": tasks or [],
        "datasets": datasets or [],
        "method_path": {
            "signals": ["reward"],
            "actions": ["select"],
            "adverse_evidence": ["failure"] if role == "KEEP_NEGATIVE" else [],
        },
        "repository_status": repo_status,
        "repositories": [],
        "links": {"abstract": f"https://arxiv.org/abs/{aid}"},
    }


class RegistryViewTests(unittest.TestCase):
    def test_build_views_separates_local_speech_transfer_negative_and_instrument(self):
        local = _record(
            "2601.00001",
            "KEEP_CORE",
            speech=True,
            tasks=["asr", "ser"],
            datasets=[
                {
                    "canonical_name": "librispeech",
                    "local_present": True,
                    "task_suitability_by_tag": {
                        "asr": "TASK_MATCH",
                        "ser": "REQUIRES_SPLIT_REVIEW",
                    },
                }
            ],
        )
        transfer = _record("2601.00002", "KEEP_TRANSFER", repo_status="OPEN_SOURCE_VERIFIED")
        negative = _record("2601.00003", "KEEP_NEGATIVE")
        instrument = _record("2601.00004", "KEEP_INSTRUMENT", speech=True, tasks=["tts"])

        result = views.build_views([local, transfer, negative, instrument])

        self.assertEqual(result["summary"]["records"], 4)
        self.assertEqual(result["summary"]["local_task_match_facets"], 1)
        self.assertEqual(result["local_speech_task_match"][0]["task"], "asr")
        self.assertEqual(result["open_transfer"][0]["arxiv_id"], "2601.00002")
        self.assertEqual(result["negative_falsifiers"][0]["adverse_evidence"], ["failure"])
        self.assertEqual(result["instruments"][0]["arxiv_id"], "2601.00004")

    def test_duplicate_canonical_ids_fail_closed(self):
        row = _record("2601.00001", "KEEP_CORE")
        with self.assertRaisesRegex(ValueError, "duplicate canonical ID"):
            views.build_views([row, row])

    def test_run_is_deterministic_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "papers.jsonl"
            source.write_text(json.dumps(_record("2601.00001", "KEEP_NEGATIVE")) + "\n", encoding="utf-8")
            output = root / "views.json"
            summary = views.run(source, output)
            self.assertEqual(summary["records"], 1)
            payload = output.read_text(encoding="utf-8")
            self.assertNotIn("local_path", payload)
            with self.assertRaises(FileExistsError):
                views.run(source, output)

    def test_run_merges_disjoint_registry_shards(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            first = root / "first.jsonl"
            second = root / "second.jsonl"
            first.write_text(json.dumps(_record("2601.00001", "KEEP_CORE")) + "\n", encoding="utf-8")
            second.write_text(json.dumps(_record("2601.00002", "KEEP_TRANSFER", repo_status="OPEN_SOURCE_VERIFIED")) + "\n", encoding="utf-8")
            output = root / "views.json"
            summary = views.run([first, second], output)
            self.assertEqual(summary["source_registry_count"], 2)
            self.assertEqual(summary["records"], 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
