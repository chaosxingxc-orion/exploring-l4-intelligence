#!/usr/bin/env python3
"""Unit contracts for resilient, revision-pinned HF completeness listing."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import hf_complete


class HfCompleteTests(unittest.TestCase):
    def test_main_writes_manifest_with_mocked_remote_metadata(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            destination = root / "data"
            output = root / "missing.txt"
            api = Mock()
            with patch.object(hf_complete, "HfApi", return_value=api), patch.object(
                hf_complete,
                "list_remote_files",
                return_value=("abc123", [("data.bin", 4)]),
            ):
                result = hf_complete.main(
                    ["org/data", str(destination), str(output), "dataset"]
                )
            self.assertEqual(0, result)
            self.assertIn("resolve/abc123/data.bin", output.read_text(encoding="utf-8"))

    def test_dataset_info_fallback_survives_tree_api_failure(self):
        api = Mock()
        api.list_repo_tree.side_effect = OSError("transient TLS EOF")
        api.dataset_info.return_value = SimpleNamespace(
            sha="abc123",
            siblings=[
                SimpleNamespace(rfilename="README.md", size=12),
                SimpleNamespace(rfilename="audio/x.wav", size=20),
            ],
        )
        revision, files = hf_complete.list_remote_files(api, "org/data", "dataset")
        self.assertEqual("abc123", revision)
        self.assertEqual([("README.md", 12), ("audio/x.wav", 20)], files)
        api.dataset_info.assert_called_once_with("org/data", files_metadata=True)

    def test_metadata_fallback_retries_one_transient_tls_failure(self):
        api = Mock()
        api.list_repo_tree.side_effect = OSError("tree TLS EOF")
        resolved = SimpleNamespace(
            sha="abc123",
            siblings=[SimpleNamespace(rfilename="README.md", size=12)],
        )
        api.dataset_info.side_effect = [OSError("info TLS EOF"), resolved]
        revision, files = hf_complete.list_remote_files(
            api,
            "org/data",
            "dataset",
            retry_delays=(0,),
        )
        self.assertEqual("abc123", revision)
        self.assertEqual([("README.md", 12)], files)
        self.assertEqual(2, api.dataset_info.call_count)

    def test_manifest_uses_resolved_revision_and_single_connection(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            destination = root / "data"
            destination.mkdir()
            (destination / "present.txt").write_bytes(b"1234")
            output = root / "missing.txt"
            summary = hf_complete.write_missing_manifest(
                repo="org/data",
                repo_type="dataset",
                endpoint="https://hf.example",
                revision="deadbeef",
                remote_files=[("present.txt", 4), ("nested/missing.bin", 9)],
                destination=destination,
                output=output,
            )
            manifest = output.read_text(encoding="utf-8")
        self.assertEqual(2, summary["total_files"])
        self.assertEqual(1, summary["missing_files"])
        self.assertIn("/resolve/deadbeef/nested/missing.bin", manifest)
        self.assertIn("split=1", manifest)
        self.assertIn("max-connection-per-server=1", manifest)


if __name__ == "__main__":
    unittest.main()
