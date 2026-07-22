import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import sf_stage1b_release_manifest as target


class Stage1BReleaseManifestTests(unittest.TestCase):
    def test_git_artifacts_hash_index_blob_bytes_after_clean_filters(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / ".gitattributes").write_text("*.txt text eol=lf\n", encoding="utf-8")
            (root / "a.txt").write_bytes(b"a\r\n")
            subprocess.run(["git", "-C", str(root), "add", ".gitattributes", "a.txt"], check=True)
            manifest = target.materialize(
                {
                    "release_id": "r",
                    "artifacts": [{"role": "a", "path": "a.txt", "location": "git"}],
                },
                root,
            )
            self.assertEqual(2, manifest["artifacts"][0]["bytes"])
            self.assertEqual(target.hashlib.sha256(b"a\n").hexdigest(), manifest["artifacts"][0]["sha256"])

    def test_windows_external_path_translates_under_wsl(self):
        self.assertEqual(
            Path("/mnt/e/chao/data.bin"),
            target.normalize_external_path("E:/chao/data.bin", is_wsl=True),
        )
        self.assertEqual(
            Path("E:/chao/data.bin"),
            target.normalize_external_path("E:/chao/data.bin", is_wsl=False),
        )

    def test_materializes_hashes_and_declared_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.txt").write_text("alpha\n", encoding="utf-8")
            external = root / "outside.bin"
            external.write_bytes(b"beta")
            spec = {
                "release_id": "r1",
                "declared_counts": {"works": 2},
                "artifacts": [
                    {"role": "local", "path": "a.txt", "location": "git"},
                    {"role": "external", "path": str(external), "location": "external"},
                ],
            }
            manifest = target.materialize(spec, root)
            self.assertEqual(manifest["release_id"], "r1")
            self.assertEqual(manifest["declared_counts"]["works"], 2)
            self.assertEqual(len(manifest["artifacts"]), 2)
            self.assertEqual(len(manifest["artifacts"][0]["sha256"]), 64)
            self.assertEqual(manifest["commit_binding"]["mode"], "CONTAINING_GIT_COMMIT")

    def test_duplicate_role_or_path_and_missing_file_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a").write_text("x", encoding="utf-8")
            base = {"release_id": "r", "artifacts": [
                {"role": "same", "path": "a", "location": "git"},
                {"role": "same", "path": "a", "location": "git"},
            ]}
            with self.assertRaisesRegex(ValueError, "duplicate"):
                target.materialize(base, root)
            missing = {"release_id": "r", "artifacts": [
                {"role": "missing", "path": "none", "location": "git"}
            ]}
            with self.assertRaises(FileNotFoundError):
                target.materialize(missing, root)

    def test_invalid_release_and_paths_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaisesRegex(ValueError, "release_id"):
                target.materialize({"artifacts": []}, root)
            for entry in (
                {"role": "absolute", "path": str(root / "x"), "location": "git"},
                {"role": "parent", "path": "../x", "location": "git"},
                {"role": "bad-location", "path": "x", "location": "other"},
            ):
                with self.subTest(entry=entry), self.assertRaises(ValueError):
                    target.materialize({"release_id": "r", "artifacts": [entry]}, root)

    def test_write_is_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a").write_text("x", encoding="utf-8")
            spec_path = root / "spec.json"
            spec_path.write_text(json.dumps({"release_id": "r", "artifacts": [
                {"role": "a", "path": "a", "location": "git"}
            ]}), encoding="utf-8")
            out = root / "manifest.json"
            first = target.run(spec_path, root, out)
            first_bytes = out.read_bytes()
            second = target.run(spec_path, root, out)
            self.assertEqual(first, second)
            self.assertEqual(first_bytes, out.read_bytes())

    def test_cli_reports_artifact_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a").write_text("x", encoding="utf-8")
            spec = root / "spec.json"
            spec.write_text(json.dumps({"release_id": "r", "artifacts": [
                {"role": "a", "path": "a", "location": "git"}
            ]}), encoding="utf-8")
            output = root / "out.json"
            with mock.patch("sys.argv", [
                "sf_stage1b_release_manifest.py", "--spec", str(spec),
                "--repo", str(root), "--output", str(output)
            ]):
                self.assertEqual(target.main(), 0)
            self.assertTrue(output.is_file())


if __name__ == "__main__":
    unittest.main()
