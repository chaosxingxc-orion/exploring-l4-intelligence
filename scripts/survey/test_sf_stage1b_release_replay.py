#!/usr/bin/env python3
"""Contracts for commit-bound Stage-1B release replay."""

from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import sf_stage1b_release_replay as replay  # noqa: E402


class Stage1BReleaseReplayTests(unittest.TestCase):
    def test_git_blob_and_external_bytes_replay(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.email", "test@example.com"], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.name", "Test"], check=True)
            tracked = repo / "tracked.txt"
            tracked.write_bytes(b"tracked\n")
            subprocess.run(["git", "-C", str(repo), "add", "tracked.txt"], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-qm", "fixture"], check=True)
            commit = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
            external = repo / "external.bin"
            external.write_bytes(b"external")
            manifest = {
                "release_id": "fixture",
                "artifacts": [
                    {"role": "git", "location": "git", "path": "tracked.txt", "bytes": 8, "sha256": hashlib.sha256(b"tracked\n").hexdigest()},
                    {"role": "external", "location": "external", "path": str(external), "bytes": 8, "sha256": hashlib.sha256(b"external").hexdigest()},
                ],
            }
            result = replay.verify_manifest(manifest, repo, commit)
            self.assertEqual(2, result["verified"])
            self.assertEqual([], result["failures"])

    def test_hash_mismatch_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.email", "test@example.com"], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.name", "Test"], check=True)
            (repo / "tracked.txt").write_text("x", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "tracked.txt"], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-qm", "fixture"], check=True)
            commit = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
            manifest = {"release_id": "fixture", "artifacts": [{"role": "git", "location": "git", "path": "tracked.txt", "bytes": 1, "sha256": "0" * 64}]}
            result = replay.verify_manifest(manifest, repo, commit)
            self.assertIn("SHA_MISMATCH:git", result["failures"])


if __name__ == "__main__":
    unittest.main()
