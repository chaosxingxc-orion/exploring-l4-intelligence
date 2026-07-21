#!/usr/bin/env python3
"""Contracts for the exact pre-review proposal source manifest."""
from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import sf_proposal_source_manifest as manifest  # noqa: E402


class ProposalSourceManifestTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = manifest.load_manifest()

    def test_manifest_binds_every_declared_source_once(self):
        rows = self.document["files"]
        self.assertEqual(len(rows), len({row["path"] for row in rows}))
        self.assertEqual(len(rows), len({row["role"] for row in rows}))
        self.assertEqual([], manifest.validate_manifest(self.document))

    def test_required_design_surfaces_are_bound(self):
        paths = {row["path"] for row in self.document["files"]}
        required = {
            "wiki/survey/current/README.md",
            "wiki/survey/current/status.md",
            "wiki/survey/current/protocol.md",
            "scripts/survey/sf_query_compiler.py",
            "wiki/survey/2026-07-15-sf-queries.jsonl",
            "wiki/survey/2026-07-17-sf-t1-routes-v3.jsonl",
            "wiki/survey/2026-07-16-sf-t1-wordlist-v1.json",
            "wiki/survey/2026-07-15-sf-blank-templates.md",
            "wiki/survey/current/data/absence-evidence-adjudication-v3.json",
            "wiki/survey/current/data/negative-evidence-semantic-corrections-v2.json",
            "wiki/survey/current/mapping-methods-adaptation.md",
            "wiki/survey/current/modality-specificity-codebook.md",
            "wiki/survey/current/data/modality-specificity-calibration-v1.json",
            "wiki/survey/current/data/modality-specificity-blind-packet-v1.json",
            "wiki/survey/current/core-prior-routing.md",
            "wiki/survey/current/data/pdf-extractor-environment-v1.json",
            "wiki/survey/current/data/reviewer-known-items-v3.json",
            "wiki/audit/external-reviews/2026-07-21-round16-precheck-rereview-of-stage1a-research-proposal.md",
            "wiki/audit/external-reviews/2026-07-21-independent-doctoral-review-of-stage1a-working-brief.md",
        }
        self.assertTrue(required <= paths)

    def test_deferred_release_artifacts_are_explicit_not_fabricated(self):
        deferred = self.document["deferred_release_artifacts"]
        self.assertEqual(4, len(deferred))
        self.assertTrue(all(row["state"] == "REQUIRED_AFTER_INDEPENDENT_REVIEW" for row in deferred))
        self.assertFalse(self.document["release_eligible"])
        self.assertEqual("22 = 4 + 18", self.document["semantic_gate"]["inventory_identity"])
        self.assertEqual(18, self.document["semantic_gate"]["active_absence_reviews_recorded"])
        self.assertEqual(
            "PENDING_BLIND_CODER_B", self.document["h5_gate"]["status"]
        )
        self.assertEqual("EXACT_MATCH_FAIL_CLOSED", self.document["pdf_extractor_gate"]["version_policy"])

    def test_tampered_hash_or_duplicate_role_fails_closed(self):
        mutated = copy.deepcopy(self.document)
        mutated["files"][0]["sha256"] = "0" * 64
        self.assertIn("SOURCE_SHA256_MISMATCH", manifest.validate_manifest(mutated))
        duplicate = copy.deepcopy(self.document)
        duplicate["files"][1]["role"] = duplicate["files"][0]["role"]
        self.assertIn("DUPLICATE_SOURCE_ROLE", manifest.validate_manifest(duplicate))

    def test_write_check_and_drift(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "manifest.json"
            document = manifest.build_manifest()
            manifest.write_manifest(document, output)
            self.assertEqual([], manifest.check_manifest(document, output))
            output.write_text("{}\n", encoding="utf-8")
            self.assertEqual(["PROPOSAL_SOURCE_MANIFEST_DRIFT"], manifest.check_manifest(document, output))

    def test_cli_check_validates_the_frozen_commit_instead_of_rebasing_to_head(self):
        self.assertEqual(0, manifest.main(["--check"]))


if __name__ == "__main__":
    unittest.main()
