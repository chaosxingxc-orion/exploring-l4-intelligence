#!/usr/bin/env python3
"""Unit contracts for layered local asset inventory generation."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import stage1c_asset_inventory as inventory


class Stage1CAssetInventoryTests(unittest.TestCase):
    def test_cli_scans_only_unlocked_directory_and_writes_layers(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "datasets" / "locked").mkdir(parents=True)
            candidate = root / "datasets" / "candidate"
            candidate.mkdir()
            (candidate / "data.bin").write_bytes(b"1234")
            lock_path = root / "lock.json"
            lock_path.write_text(
                json.dumps(
                    {
                        "datasets": [
                            {
                                "name": "locked",
                                "local_subdir": "datasets/locked",
                                "files": 7,
                                "size_bytes": 11,
                                "revision": "abc",
                                "source": {"id": "org/locked"},
                            }
                        ],
                        "models": [],
                    }
                ),
                encoding="utf-8",
            )
            output = root / "inventory.json"
            with mock.patch.object(
                sys,
                "argv",
                [
                    "stage1c_asset_inventory.py",
                    "--data-root",
                    str(root),
                    "--lock",
                    str(lock_path),
                    "--output",
                    str(output),
                ],
            ):
                self.assertEqual(0, inventory.main())
            document = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(1, document["layers"][0]["observed_entries"])
            self.assertEqual(4, document["layers"][1]["entries"][0]["bytes"])

    def test_baseline_and_unfrozen_candidates_are_separate(self):
        lock = {
            "datasets": [{"name": "locked-data", "local_subdir": "datasets/locked-data"}],
            "models": [{"name": "locked-model", "local_subdir": "models/locked-model"}],
        }
        observed = [
            {"kind": "dataset", "name": "locked-data", "files": 2, "bytes": 10},
            {"kind": "dataset", "name": "new-data", "files": 3, "bytes": 20},
            {"kind": "model", "name": "locked-model", "files": 4, "bytes": 30},
            {"kind": "model", "name": "new-model", "files": 5, "bytes": 40},
        ]
        document = inventory.build_inventory(lock, observed, data_root="${SPEECHRL_DATA_DIR}")
        layers = {layer["layer_id"]: layer for layer in document["layers"]}
        self.assertEqual(2, layers["FROZEN_BASELINE"]["observed_entries"])
        self.assertEqual(2, layers["LOCAL_CANDIDATE_UNFROZEN"]["observed_entries"])
        self.assertEqual(
            {"new-data", "new-model"},
            {row["name"] for row in layers["LOCAL_CANDIDATE_UNFROZEN"]["entries"]},
        )

    def test_missing_baseline_is_reported_not_silently_dropped(self):
        lock = {
            "datasets": [{"name": "missing", "local_subdir": "datasets/missing"}],
            "models": [],
        }
        document = inventory.build_inventory(lock, [], data_root="${SPEECHRL_DATA_DIR}")
        baseline = document["layers"][0]
        self.assertEqual(["datasets/missing"], baseline["missing_locked_paths"])


if __name__ == "__main__":
    unittest.main()
