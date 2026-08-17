from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
LOCK_PATH = ROOT / "docs" / "datasets.lock.json"
MODULE_PATH = ROOT / "scripts" / "data" / "asset_lock.py"

spec = importlib.util.spec_from_file_location("asset_lock", MODULE_PATH)
assert spec and spec.loader
asset_lock = importlib.util.module_from_spec(spec)
spec.loader.exec_module(asset_lock)


class AssetLockTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))

    def test_lock_is_valid(self) -> None:
        self.assertEqual([], asset_lock.validate(self.lock))

    def test_hf_bundle_members_require_full_revisions(self) -> None:
        import copy

        lock = copy.deepcopy(self.lock)
        bundle = next(
            item
            for item in asset_lock.assets(lock)
            if item.get("source", {}).get("kind") == "hf-bundle"
        )
        bundle["members"][0]["revision"] = bundle["members"][0]["revision"][:8]
        errors = asset_lock.validate(lock)
        self.assertTrue(
            any("hf-bundle member needs a 40-hex revision" in error for error in errors)
        )
        bundle["members"].clear()
        errors = asset_lock.validate(lock)
        self.assertTrue(
            any("non-empty members" in error for error in errors)
        )

    def test_speech_aware_core_is_exactly_the_minimum_carrier(self) -> None:
        names = {
            item["name"]
            for item in asset_lock.selected_assets(self.lock, [], "speech-aware-core")
        }
        self.assertEqual(
            {"earnings21-original", "earnings22-original", "conec"}, names
        )

    def test_nonfetchable_assets_are_not_in_active_fetch_profiles(self) -> None:
        active = {
            "speech-aware-core",
            "speech-aware-diagnostics",
            "speech-aware-secondary",
            "speech-aware-annotations",
            "speech-aware-small-public",
        }
        for item in asset_lock.assets(self.lock):
            if active.intersection(item.get("profiles", [])):
                self.assertNotIn(
                    (item.get("source") or {}).get("kind"),
                    {"restricted", "source-unstable", "unavailable"},
                    item["name"],
                )

    def test_legacy_candidate_manifests_are_not_operational_sources(self) -> None:
        engine = (ROOT / "scripts" / "data" / "fetch-assets.sh").read_text(encoding="utf-8")
        self.assertNotIn("AudioLLMs/audiocaps_qa_test|", engine)
        self.assertNotIn("gdrive:1SO_4MT", engine)

    def test_direct_files_are_verified_by_size_and_hash(self) -> None:
        payload = b"canonical-asset"
        with tempfile.TemporaryDirectory() as temporary:
            data_root = Path(temporary)
            target = data_root / "datasets" / "direct-test"
            target.mkdir(parents=True)
            (target / "payload.bin").write_bytes(payload)
            item = {
                "name": "direct-test",
                "kind": "dataset",
                "local_subdir": "datasets/direct-test",
                "source": {
                    "kind": "direct",
                    "files": [
                        {
                            "filename": "payload.bin",
                            "size_bytes": len(payload),
                            "sha256": hashlib.sha256(payload).hexdigest(),
                        }
                    ],
                },
                "revision": "fixture",
                "status": "COMPLETE",
            }
            observed, _ = asset_lock.verify_item(data_root, item, full=True)
            self.assertEqual("COMPLETE", observed)

            (target / "payload.bin").write_bytes(b"canonical-asseu")
            observed, detail = asset_lock.verify_item(data_root, item, full=True)
            self.assertEqual("PARTIAL", observed)
            self.assertIn("hash mismatch", detail)

    def test_direct_files_accept_official_md5_receipts(self) -> None:
        payload = b"zenodo-multipart"
        with tempfile.TemporaryDirectory() as temporary:
            data_root = Path(temporary)
            target = data_root / "datasets" / "direct-md5"
            target.mkdir(parents=True)
            (target / "part.z01").write_bytes(payload)
            item = {
                "name": "direct-md5",
                "kind": "dataset",
                "local_subdir": "datasets/direct-md5",
                "source": {
                    "kind": "direct",
                    "files": [
                        {
                            "filename": "part.z01",
                            "size_bytes": len(payload),
                            "md5": hashlib.md5(
                                payload, usedforsecurity=False
                            ).hexdigest(),
                        }
                    ],
                },
                "revision": "fixture",
                "status": "COMPLETE",
            }
            observed, _ = asset_lock.verify_item(data_root, item, full=True)
            self.assertEqual("COMPLETE", observed)

    def test_hf_aria2_is_anchored_to_the_governed_target(self) -> None:
        item = {
            "name": "hf-test",
            "kind": "dataset",
            "local_subdir": "datasets/hf-test",
            "source": {"kind": "hf", "id": "owner/repo"},
            "revision": "a" * 40,
            "status": "PARTIAL",
        }
        with tempfile.TemporaryDirectory() as temporary:
            data_root = Path(temporary)
            target = data_root / item["local_subdir"]
            rounds = 0
            observed_aria2_cwds: list[Path | None] = []

            def fake_run(command, dry_run=False, env=None, cwd=None):
                nonlocal rounds
                if command[0].endswith("hf_complete.py") or "hf_complete.py" in command[1]:
                    manifest = Path(command[4])
                    manifest.parent.mkdir(parents=True, exist_ok=True)
                    manifest.write_text(
                        "https://example.invalid/payload\n  dir=nested\n  out=x.bin\n"
                        if rounds == 0
                        else "",
                        encoding="utf-8",
                    )
                    rounds += 1
                elif command[0] == "aria2c":
                    observed_aria2_cwds.append(cwd)

            with (
                mock.patch.object(asset_lock.shutil, "which", return_value="aria2c"),
                mock.patch.object(asset_lock, "run", side_effect=fake_run),
            ):
                asset_lock.fetch_hf(data_root, item, dry_run=False)

            self.assertEqual([target], observed_aria2_cwds)


if __name__ == "__main__":
    unittest.main()
