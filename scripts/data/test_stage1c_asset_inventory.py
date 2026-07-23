#!/usr/bin/env python3
"""Unit contracts for layered local asset inventory generation."""

from __future__ import annotations

import json
import os
import subprocess
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

    def test_nonstandard_locked_path_keeps_identity_next_to_same_leaf_candidate(self):
        lock = {
            "datasets": [
                {
                    "name": "slurp",
                    "local_subdir": "repos/slurp/scripts/audio",
                    "files": 7,
                    "size_bytes": 11,
                    "revision": "slurp-revision",
                    "source": {"id": "slurp/source"},
                }
            ],
            "models": [],
        }
        observed = [
            {
                "kind": "dataset",
                "name": "audio",
                "local_path": "${SPEECHRL_DATA_DIR}/repos/slurp/scripts/audio",
                "files": 7,
                "bytes": 11,
            },
            {
                "kind": "dataset",
                "name": "audio",
                "local_path": "${SPEECHRL_DATA_DIR}/datasets/audio",
                "files": 1,
                "bytes": 2,
            },
        ]

        document = inventory.build_inventory(lock, observed, data_root="${SPEECHRL_DATA_DIR}")
        baseline, candidate = document["layers"][:2]
        self.assertEqual([], baseline["missing_locked_paths"])
        self.assertEqual(
            ["${SPEECHRL_DATA_DIR}/repos/slurp/scripts/audio"],
            [row["local_path"] for row in baseline["entries"]],
        )
        self.assertEqual(
            ["${SPEECHRL_DATA_DIR}/datasets/audio"],
            [row["local_path"] for row in candidate["entries"]],
        )

    def test_cli_preserves_nonstandard_lock_path_and_auxiliary_presence(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            locked = root / "repos" / "slurp" / "scripts" / "audio"
            locked.mkdir(parents=True)
            conventional = root / "datasets" / "locked"
            conventional.mkdir(parents=True)
            mirror = root / "datasets" / "audio"
            mirror.mkdir(parents=True)
            (mirror / "candidate.bin").write_bytes(b"12")
            (root / "survey-fulltext").mkdir()
            lock_path = root / "lock.json"
            lock_path.write_text(
                json.dumps(
                    {
                        "datasets": [
                            {
                                "name": "slurp",
                                "local_subdir": "repos/slurp/scripts/audio",
                                "files": 7,
                                "size_bytes": 11,
                                "revision": "slurp-revision",
                                "source": {"id": "slurp/source"},
                            },
                            {
                                "name": "locked",
                                "local_subdir": "datasets/locked",
                                "files": 3,
                                "size_bytes": 5,
                                "revision": "locked-revision",
                                "source": {"id": "locked/source"},
                            },
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

            layers = {
                row["layer_id"]: row
                for row in json.loads(output.read_text(encoding="utf-8"))["layers"]
            }
            self.assertEqual(2, layers["FROZEN_BASELINE"]["observed_entries"])
            self.assertEqual([], layers["FROZEN_BASELINE"]["missing_locked_paths"])
            self.assertEqual(
                "${SPEECHRL_DATA_DIR}/repos/slurp/scripts/audio",
                next(
                    row["local_path"]
                    for row in layers["FROZEN_BASELINE"]["entries"]
                    if row["name"] == "audio"
                ),
            )
            self.assertEqual(1, layers["LOCAL_CANDIDATE_UNFROZEN"]["observed_entries"])
            auxiliary = {
                row["local_path"]: row["present"]
                for row in layers["SURVEY_AND_REPRO_AUXILIARY"]["entries"]
            }
            self.assertTrue(auxiliary["${SPEECHRL_DATA_DIR}/survey-fulltext"])

    @unittest.skipUnless(os.name != "nt", "WSL-to-Windows producer parity test")
    def test_wsl_python_and_windows_powershell_are_semantically_equivalent(self):
        powershell = Path("/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe")
        if not powershell.is_file():
            self.skipTest("Windows PowerShell interop is unavailable")
        repo = Path(__file__).resolve().parents[2]
        with tempfile.TemporaryDirectory(dir=repo / "scripts" / "data") as temporary:
            root = Path(temporary)
            (root / "repos" / "slurp" / "scripts" / "audio").mkdir(parents=True)
            (root / "datasets" / "locked").mkdir(parents=True)
            mirror = root / "datasets" / "audio"
            mirror.mkdir(parents=True)
            (mirror / "candidate.bin").write_bytes(b"12")
            (root / "survey-fulltext").mkdir()
            lock_path = root / "lock.json"
            lock_path.write_text(
                json.dumps(
                    {
                        "datasets": [
                            {
                                "name": "slurp",
                                "local_subdir": "repos/slurp/scripts/audio",
                                "files": 7,
                                "size_bytes": 11,
                                "revision": "slurp-revision",
                                "source": {"id": "slurp/source"},
                            },
                            {
                                "name": "locked",
                                "local_subdir": "datasets/locked",
                                "files": 3,
                                "size_bytes": 5,
                                "revision": "locked-revision",
                                "source": {"id": "locked/source"},
                            },
                        ],
                        "models": [],
                    }
                ),
                encoding="utf-8",
            )
            python_output = root / "python.json"
            powershell_output = root / "powershell.json"
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
                    str(python_output),
                    "--snapshot-date",
                    "2026-07-23",
                ],
            ):
                self.assertEqual(0, inventory.main())

            def windows_path(path: Path) -> str:
                return subprocess.run(
                    ["wslpath", "-w", str(path)],
                    check=True,
                    capture_output=True,
                    text=True,
                ).stdout.strip()

            completed = subprocess.run(
                [
                    str(powershell),
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    windows_path(repo / "scripts" / "data" / "stage1c-asset-inventory.ps1"),
                    "-DataRoot",
                    windows_path(root),
                    "-LockPath",
                    windows_path(lock_path),
                    "-OutputPath",
                    windows_path(powershell_output),
                    "-SnapshotDate",
                    "2026-07-23",
                ],
                check=False,
                capture_output=True,
            )
            stderr = completed.stderr.decode("utf-8", errors="replace")
            self.assertEqual(0, completed.returncode, stderr)

            def semantic_projection(path: Path) -> dict:
                document = json.loads(path.read_text(encoding="utf-8-sig"))
                for layer in document["layers"]:
                    layer["entries"] = sorted(
                        layer["entries"], key=lambda row: row["local_path"]
                    )
                return document

            self.assertEqual(
                semantic_projection(python_output),
                semantic_projection(powershell_output),
            )


if __name__ == "__main__":
    unittest.main()
