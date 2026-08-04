"""Fault-injection tests for the legacy-asset resolution contract (G1 closure).

Builds a tiny retired repository + offline bundle in a temp root, then proves that the
default validator rejects path/remote/URI tampering and that ``--verify-bundles``
disproves blob, commit and bundle-hash tampering.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("legacy_asset_resolution_check.py")
SPEC = importlib.util.spec_from_file_location("legacy_asset_resolution_check", SCRIPT)
assert SPEC and SPEC.loader
legacy = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(legacy)


def _git(*args: str) -> str:
    completed = subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t.invalid", *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return completed.stdout.strip()


class LegacyResolutionContractTests(unittest.TestCase):
    REPO_ID = "retired-work"
    PREFIX = "projects/retired-work"
    REMOTE = "https://github.com/example/retired-work.git"

    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / "docs" / "integrity").mkdir(parents=True)
        tombstone = self.root / "wiki" / "tombstone.md"
        tombstone.parent.mkdir(parents=True)
        tombstone.write_text("retired\n", encoding="utf-8")

        # a tiny history: commit1 has kept.txt + deleted.txt; commit2 removes deleted.txt
        source = self.root / "source"
        source.mkdir()
        _git("init", "--quiet", "--initial-branch=master", str(source))
        (source / "kept.txt").write_text("kept\n", encoding="utf-8")
        (source / "deleted.txt").write_text("gone later\n", encoding="utf-8")
        _git("-C", str(source), "add", "-A")
        _git("-C", str(source), "commit", "--quiet", "-m", "one")
        self.commit1 = _git("-C", str(source), "rev-parse", "HEAD")
        (source / "deleted.txt").unlink()
        _git("-C", str(source), "add", "-A")
        _git("-C", str(source), "commit", "--quiet", "-m", "two")
        self.commit2 = _git("-C", str(source), "rev-parse", "HEAD")
        self.kept_blob = _git("-C", str(source), "rev-parse", f"{self.commit2}:kept.txt")
        self.deleted_blob = _git("-C", str(source), "rev-parse", f"{self.commit1}:deleted.txt")

        self.data_root = self.root / "data"
        bundle = self.data_root / "program-archives" / f"{self.REPO_ID}.bundle"
        bundle.parent.mkdir(parents=True)
        _git("-C", str(source), "bundle", "create", str(bundle), "--all")
        self.bundle = bundle

        rows = [
            {"path": f"{self.PREFIX}/kept.txt"},
            {"path": f"{self.PREFIX}/deleted.txt"},
        ]
        (self.root / legacy.LEGACY_INVENTORY_PATH).write_text(
            "".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8"
        )
        self.write_registry()
        self.resolution = {
            "schema": legacy.RESOLUTION_SCHEMA,
            "legacy_inventory": {"path": legacy.LEGACY_INVENTORY_PATH, "sha256": ""},
            "retired_repository_registry": {
                "path": legacy.RETIRED_REGISTRY_PATH,
                "sha256": "",
            },
            "summary": {
                "WORKTREE_PRESENT": 0,
                "LOCAL_GIT_HISTORY": 0,
                "COLD_BACKUP_RESOLVED": 2,
                "UNRESOLVED": 0,
                "waived": 0,
            },
            "resolutions": [
                self.entry("deleted.txt", self.commit1, self.deleted_blob),
                self.entry("kept.txt", self.commit2, self.kept_blob),
            ],
        }
        self.write_resolution()

    def entry(self, repo_path: str, commit: str, blob: str) -> dict:
        return {
            "path": f"{self.PREFIX}/{repo_path}",
            "state": "COLD_BACKUP_RESOLVED",
            "repo_id": self.REPO_ID,
            "commit": commit,
            "repo_path": repo_path,
            "git_blob": blob,
            "uri": f"git+{self.REMOTE}@{commit}#path={repo_path}",
        }

    def write_registry(self) -> None:
        registry = {
            "schema": legacy.RETIRED_REGISTRY_SCHEMA,
            "retirement_ruling": "test ruling",
            "repositories": [
                {
                    "repo_id": self.REPO_ID,
                    "work_label": "W9",
                    "remote": self.REMOTE,
                    "final_branch": "master",
                    "final_commit": self.commit2,
                    "local_state": "RETIRED_NO_WORKTREE",
                    "retention_policy": "COLD_BACKUP_REMOTE_RETAINED_PLUS_OFFLINE_BUNDLE",
                    "verified_at": "2026-08-04",
                    "tombstone": "wiki/tombstone.md",
                    "legacy_path_prefix": self.PREFIX,
                    "offline_bundle": {
                        "path": f"SPEECHRL_DATA_DIR/program-archives/{self.REPO_ID}.bundle",
                        "sha256": hashlib.sha256(self.bundle.read_bytes()).hexdigest(),
                    },
                }
            ],
        }
        (self.root / legacy.RETIRED_REGISTRY_PATH).write_text(
            json.dumps(registry), encoding="utf-8"
        )

    def write_resolution(self) -> None:
        self.resolution["legacy_inventory"]["sha256"] = hashlib.sha256(
            (self.root / legacy.LEGACY_INVENTORY_PATH).read_bytes()
        ).hexdigest()
        self.resolution["retired_repository_registry"]["sha256"] = hashlib.sha256(
            (self.root / legacy.RETIRED_REGISTRY_PATH).read_bytes()
        ).hexdigest()
        (self.root / legacy.RESOLUTION_PATH).write_text(
            json.dumps(self.resolution), encoding="utf-8"
        )

    def verify_bundles(self) -> dict:
        document = legacy.load_and_validate_resolution(self.root)
        return legacy.verify_bundles(self.root, self.data_root, document)

    def test_valid_world_passes_both_modes(self) -> None:
        proof = self.verify_bundles()
        self.assertEqual({"bindings": 2, "bundle_hashes": 1}, proof)

    def test_default_mode_rejects_prefix_remote_and_uri_path_tampering(self) -> None:
        kept = self.resolution["resolutions"][1]
        tampering = (
            ("path", "projects/other-repo/kept.txt", "prefix"),
            ("uri", f"git+https://example.invalid/x.git@{self.commit2}#path=kept.txt", "remote"),
            ("uri", f"git+{self.REMOTE}@{self.commit2}#path=wrong.txt", "uri"),
        )
        for field, value, _label in tampering:
            with self.subTest(field=field, value=value):
                original = kept[field]
                kept[field] = value
                self.write_resolution()
                with self.assertRaises(legacy.LegacyResolutionError):
                    legacy.load_and_validate_resolution(self.root)
                kept[field] = original
        self.write_resolution()
        legacy.load_and_validate_resolution(self.root)

    def test_bundle_mode_disproves_blob_tampering(self) -> None:
        self.resolution["resolutions"][1]["git_blob"] = "0" * 40
        self.write_resolution()
        with self.assertRaisesRegex(legacy.LegacyResolutionError, "disproves"):
            self.verify_bundles()

    def test_bundle_mode_rejects_unreachable_commit(self) -> None:
        kept = self.resolution["resolutions"][1]
        kept["commit"] = "f" * 40
        kept["uri"] = f"git+{self.REMOTE}@{'f' * 40}#path=kept.txt"
        self.write_resolution()
        with self.assertRaisesRegex(legacy.LegacyResolutionError, "unreachable"):
            self.verify_bundles()

    def test_bundle_mode_rejects_bundle_hash_drift(self) -> None:
        with self.bundle.open("ab") as handle:
            handle.write(b"tamper")
        with self.assertRaisesRegex(legacy.LegacyResolutionError, "SHA-256 drift"):
            self.verify_bundles()

    def test_bundle_mode_rejects_missing_bundle_and_final_commit_absence(self) -> None:
        self.bundle.unlink()
        with self.assertRaisesRegex(legacy.LegacyResolutionError, "bundle missing"):
            self.verify_bundles()

        _git("-C", str(self.root / "source"), "branch", "old-only", self.commit1)
        _git("-C", str(self.root / "source"), "bundle", "create", str(self.bundle), "old-only")
        self.write_registry()
        self.write_resolution()
        with self.assertRaisesRegex(legacy.LegacyResolutionError, "final commit"):
            self.verify_bundles()

    def test_reviewer_combined_injection_is_rejected(self) -> None:
        first = self.resolution["resolutions"][0]
        first["git_blob"] = "0" * 40
        first["uri"] = f"git+https://example.invalid/w.git@{first['commit']}#path=wrong.txt"
        self.write_resolution()
        with self.assertRaises(legacy.LegacyResolutionError):
            legacy.load_and_validate_resolution(self.root)


if __name__ == "__main__":
    unittest.main()
