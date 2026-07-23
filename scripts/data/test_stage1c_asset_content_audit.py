#!/usr/bin/env python3
"""Contracts for remote, auxiliary, and extraneous asset content accounting."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path


import stage1c_asset_content_audit as audit


class Stage1CAssetContentAuditTests(unittest.TestCase):
    def test_hfd_manifest_content_is_split_from_auxiliary_and_extraneous_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / ".hfd").mkdir()
            (root / "remote").mkdir()
            (root / "remote" / "a.csv").write_bytes(b"abc")
            (root / "remote" / "b.wav").write_bytes(b"12345")
            (root / ".hfd" / "manifest").write_text(
                "3\tremote/a.csv\n5\tremote/b.wav\n", encoding="utf-8"
            )
            (root / ".hfd" / "download.log").write_bytes(b"log!")
            (root / "remote" / "a.1.csv").write_bytes(b"duplicate")

            row = audit.audit_hfd_asset(root, asset_id="fixture", revision="abc")

        self.assertEqual({"files": 2, "bytes": 8, "missing": 0}, row["remote_content"])
        self.assertEqual({"files": 2, "bytes": 34}, row["auxiliary_content"])
        self.assertEqual({"files": 1, "bytes": 9}, row["extraneous_content"])
        self.assertEqual("DO_NOT_DELETE; STAGE2_LOADER_MUST_USE_REVISION_BOUND_ALLOWLIST", row["hygiene_action"])

    def test_cli_writes_schema_without_deleting_any_file(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            dataset = root / "datasets" / "audio2tool"
            (dataset / ".hfd").mkdir(parents=True)
            (dataset / "x").write_bytes(b"x")
            (dataset / ".hfd" / "manifest").write_text("1\tx\n", encoding="utf-8")
            output = root / "receipt.json"
            self.assertEqual(0, audit.main(["--data-root", str(root), "--output", str(output)]))
            document = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual("speechrl-stage1c-asset-content-accounting-v1", document["schema"])
            self.assertTrue((dataset / "x").is_file())


if __name__ == "__main__":
    unittest.main()
