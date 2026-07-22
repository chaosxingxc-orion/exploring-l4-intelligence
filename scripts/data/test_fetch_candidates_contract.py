#!/usr/bin/env python3
"""Behavioral contracts for the Stage-1C candidate downloader."""

from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts" / "data" / "fetch-candidates.sh"


class FetchCandidatesContractTests(unittest.TestCase):
    def test_remote_failure_propagates_to_process_exit(self):
        with tempfile.TemporaryDirectory() as data_dir:
            env = os.environ.copy()
            env.update(
                {
                    "SPEECHRL_DATA_DIR": data_dir,
                    "SPEECHRL_HF_ENDPOINT": "http://127.0.0.1:9",
                    "SPEECHRL_HFD_JOBS": "1",
                    "HF_COMPLETE_RETRY_DELAYS": "0",
                }
            )
            completed = subprocess.run(
                ["bash", str(SCRIPT), "ihbench"],
                cwd=REPO,
                env=env,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
        self.assertNotEqual(0, completed.returncode, completed.stdout + completed.stderr)
        self.assertIn("download failure(s)", completed.stderr)

    def test_exact_stage1c_assets_are_listed_without_writes(self):
        completed = subprocess.run(
            [
                "bash",
                str(SCRIPT),
                "--list",
                "voiceagentbench",
                "omni-deepsearch",
                "ihbench",
                "full-duplex-bench-v3",
            ],
            cwd=REPO,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
        self.assertIn("krutrim-ai-labs/VoiceAgentBench", completed.stdout)
        self.assertIn("Kirito-Lab/Omni-DeepSearch", completed.stdout)
        self.assertIn("bosonai/IHBench", completed.stdout)
        self.assertIn("1SO_4MTazWQ_jvCx0dtmpQ-t40bdd07yz", completed.stdout)
        self.assertIn("736136419 bytes", completed.stdout)


if __name__ == "__main__":
    unittest.main()
