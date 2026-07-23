#!/usr/bin/env python3
"""Contracts for reproducible Stage-1B v5 gate-asset acquisition."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
LOCK = REPO / "docs" / "stage1b-v5-gate-assets.lock.json"
WRAPPER = REPO / "scripts" / "data" / "fetch-stage1b-v5-gate-assets.sh"


class Stage1BV5GateAssetLockTests(unittest.TestCase):
    def test_downloadable_assets_are_exactly_revision_pinned_outside_git(self):
        document = json.loads(LOCK.read_text(encoding="utf-8"))
        downloadable = [*document["datasets"], *document["ref_repos"]]
        self.assertEqual(4, len(downloadable))
        self.assertTrue(all(len(row["revision"]) == 40 for row in downloadable))
        self.assertTrue(
            all(row["local_subdir"].startswith("repos/") for row in downloadable)
        )
        self.assertEqual(
            {"speakersleuth", "parapair-audio-bench", "unisrm", "unisrm-bench"},
            {row["name"] for row in downloadable},
        )

    def test_gated_or_unreleased_assets_are_recorded_not_silently_substituted(self):
        document = json.loads(LOCK.read_text(encoding="utf-8"))
        unavailable = {row["asset_id"]: row for row in document["unavailable_assets"]}
        self.assertEqual(
            {
                "speakersleuth-code-data",
                "parapair-svc-audio",
                "audio-aware-styleset",
                "videofdb-evaluation-data",
            },
            set(unavailable),
        )
        self.assertTrue(all(row["substitute"] is None for row in unavailable.values()))
        self.assertTrue(all(row["stage1c_effect"] == "NONBLOCKING" for row in unavailable.values()))

    def test_wrapper_reuses_unified_lock_driven_downloader(self):
        source = WRAPPER.read_text(encoding="utf-8")
        self.assertIn("stage1b-v5-gate-assets.lock.json", source)
        self.assertIn("fetch-data.sh", source)
        self.assertNotIn("git clone", source)
        self.assertNotIn("huggingface-cli", source)

    def test_unified_downloader_never_treats_partial_hfd_directory_as_complete(self):
        source = (REPO / "scripts/data/fetch-data.sh").read_text(encoding="utf-8")
        self.assertIn("hf_completion_marker_matches", source)
        self.assertIn("hfd_manifest_complete", source)
        self.assertIn("mark_hf_complete", source)
        self.assertIn('elif [ "$method" = hf ]', source)
        self.assertNotIn('elif [ "$method" = hf ]; then\n    has_data', source)


if __name__ == "__main__":
    unittest.main()
