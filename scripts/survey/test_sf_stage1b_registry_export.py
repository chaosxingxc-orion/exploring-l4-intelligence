#!/usr/bin/env python3
"""Tests for long-lived Stage-1B paper registry export."""

from __future__ import annotations

import sys
import json
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import sf_stage1b_registry_export as registry


class RegistryExportTests(unittest.TestCase):
    def test_registry_record_keeps_locators_but_not_fulltext_or_snippets(self):
        source = {
            "arxiv_id": "2601.00001",
            "title": "Speech Search",
            "final_decision": "KEEP_CORE",
            "final_reason_codes": ["PRIMARY_SPEECH_CONTROL_PATH"],
            "speech_task_tags": ["asr"],
            "speech_dataset_mentions": [{"canonical_name": "librispeech", "local_present": True}],
            "control_signal_terms": ["verifier"],
            "decision_action_terms": ["search"],
            "no_update_terms": ["frozen"],
            "repo_details": [{"canonical_url": "https://github.com/acme/x", "status": "OPEN_SOURCE_VERIFIED"}],
            "repo_status": "OPEN_SOURCE_VERIFIED",
            "pdf_sha256": "a" * 64,
            "pdf_path": "E:/private/paper.pdf",
            "extracted_text_path": "E:/private/paper.txt",
            "evidence_locators": [
                {"page": 3, "evidence_type": "CONTROL_SIGNAL", "matched_term": "verifier", "snippet": "copyrighted text"}
            ],
            "preaudit_decision": "DROP",
            "audit_override_reason": "Human audit found a direct frozen speech control path.",
            "audit_override_evidence_pages": [3],
        }
        record = registry.to_registry_record(source, "source-sha", "dataset-sha")
        self.assertEqual(record["canonical_id"], "arxiv:2601.00001")
        self.assertEqual(record["evidence_locators"], [{"page": 3, "evidence_type": "CONTROL_SIGNAL", "matched_term": "verifier"}])
        self.assertNotIn("pdf_path", record)
        self.assertNotIn("extracted_text_path", record)
        self.assertNotIn("snippet", str(record["evidence_locators"]))
        self.assertIn("conclusion", record)
        self.assertIn("purpose_chain", record)
        self.assertIn("invalidation_conditions", record)
        self.assertEqual(record["reasoning_summary"], ["Human audit found a direct frozen speech control path."])
        self.assertEqual(record["provenance"]["preaudit_decision"], "DROP")
        self.assertEqual(record["provenance"]["audit_override_evidence_pages"], [3])

    def test_run_creates_initial_append_only_registry(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "retained.jsonl"
            source.write_text(
                json.dumps(
                    {
                        "arxiv_id": "2601.00001",
                        "title": "Speech Search",
                        "final_decision": "KEEP_CORE",
                        "final_reason_codes": ["CORE"],
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            output = root / "registry" / "papers.jsonl"
            summary = registry.run(source, output, "s" * 64, "d" * 64)
            self.assertEqual(summary["records"], 1)
            self.assertTrue(output.is_file())
            with self.assertRaises(FileExistsError):
                registry.run(source, output, "s" * 64, "d" * 64)


if __name__ == "__main__":
    unittest.main(verbosity=2)
