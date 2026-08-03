from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "scripts" / "data" / "materialize_lfs_pointers.py"

spec = importlib.util.spec_from_file_location("materialize_lfs_pointers", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class MaterializeLfsPointersTest(unittest.TestCase):
    def test_pointer_identity_is_parsed(self) -> None:
        oid = "a" * 64
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary).resolve()
            (repo / ".git").mkdir()
            target = repo / "dataset" / "audio.mp3"
            target.parent.mkdir()
            target.write_bytes(
                (
                    "version https://git-lfs.github.com/spec/v1\n"
                    f"oid sha256:{oid}\n"
                    "size 1234\n"
                ).encode("ascii")
            )
            pointers = module.find_pointers(repo, ["dataset"])
            self.assertEqual(1, len(pointers))
            self.assertEqual("dataset/audio.mp3", pointers[0].relative)
            self.assertEqual(oid, pointers[0].oid)
            self.assertEqual(1234, pointers[0].size)

    def test_non_pointer_is_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary).resolve()
            (repo / ".git").mkdir()
            target = repo / "dataset" / "audio.mp3"
            target.parent.mkdir()
            target.write_bytes(b"not a pointer")
            self.assertEqual([], module.find_pointers(repo, ["dataset"]))


if __name__ == "__main__":
    unittest.main()
