from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO = Path(__file__).resolve().parents[2]
CHECKS = REPO / "scripts" / "checks"
if str(CHECKS) not in sys.path:
    sys.path.insert(0, str(CHECKS))

import sf_cross_platform_git_preflight as preflight


class GitfilePolicyTests(unittest.TestCase):
    def test_windows_absolute_gitdir_fails(self) -> None:
        failures = preflight.validate_gitfile_text(
            "gitdir: D:/repo/.git/worktrees/feature\n"
        )
        self.assertIn("gitfile-gitdir-must-be-relative", failures)

    def test_cross_platform_relative_gitdir_passes(self) -> None:
        self.assertEqual(
            [],
            preflight.validate_gitfile_text(
                "gitdir: ../../.git/worktrees/stage1b-readiness-remediation\n"
            ),
        )

    def test_extra_gitfile_content_fails(self) -> None:
        failures = preflight.validate_gitfile_text(
            "gitdir: ../../.git/worktrees/feature\nextra=true\n"
        )
        self.assertIn("gitfile-shape-invalid", failures)


class ObservationAggregationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.nt = {
            "schema": preflight.LEAF_SCHEMA,
            "platform": "nt",
            "implementation_freeze": preflight.IMPLEMENTATION_FREEZE,
            "resolved_head": preflight.IMPLEMENTATION_FREEZE,
            "plan_blob": preflight.IMPLEMENTATION_PLAN_BLOB,
            "primary_root_identity": "exploring-l4-intelligence",
            "worktree_root_identity": "stage1b-readiness-remediation",
            "primary_clean": True,
            "worktree_clean": True,
            "shared_core_worktree": None,
            "gitfile_policy": "RELATIVE",
        }
        self.posix = dict(self.nt, platform="posix")

    def test_exact_two_platforms_pass(self) -> None:
        report = preflight.aggregate_observations(self.nt, self.posix)
        self.assertEqual("PASS", report["verdict"])
        self.assertEqual([], report["failures"])

    def test_changed_head_fails(self) -> None:
        changed = copy.deepcopy(self.posix)
        changed["resolved_head"] = "b" * 40
        report = preflight.aggregate_observations(self.nt, changed)
        self.assertIn("platform-head-mismatch", report["failures"])

    def test_changed_plan_blob_fails(self) -> None:
        changed = copy.deepcopy(self.posix)
        changed["plan_blob"] = "b" * 40
        report = preflight.aggregate_observations(self.nt, changed)
        self.assertIn("platform-plan-blob-mismatch", report["failures"])

    def test_dirty_or_redirected_context_fails(self) -> None:
        changed = copy.deepcopy(self.posix)
        changed["worktree_clean"] = False
        changed["shared_core_worktree"] = "/wrong/worktree"
        report = preflight.aggregate_observations(self.nt, changed)
        self.assertIn("posix-worktree-dirty", report["failures"])
        self.assertIn("posix-shared-core-worktree-present", report["failures"])

    def test_missing_named_anchor_fails(self) -> None:
        changed = copy.deepcopy(self.posix)
        changed["implementation_freeze"] = ""
        report = preflight.aggregate_observations(self.nt, changed)
        self.assertIn("posix-implementation-freeze-mismatch", report["failures"])

    def test_build_report_binds_exact_leaf_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            nt_path = root / "nt.json"
            posix_path = root / "posix.json"
            nt_path.write_text(json.dumps(self.nt) + "\n", encoding="utf-8")
            posix_path.write_text(json.dumps(self.posix) + "\n", encoding="utf-8")
            report = preflight.build_report(nt_path, posix_path)
            self.assertEqual("PASS", report["verdict"])
            self.assertEqual(64, len(report["leaf_sha256"]["nt"]))
            self.assertNotEqual(
                report["leaf_sha256"]["nt"], report["leaf_sha256"]["posix"]
            )

    def test_aggregate_write_then_check_and_stale_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            nt_path = root / "nt.json"
            posix_path = root / "posix.json"
            output = root / "report.json"
            nt_path.write_text(json.dumps(self.nt) + "\n", encoding="utf-8")
            posix_path.write_text(json.dumps(self.posix) + "\n", encoding="utf-8")
            self.assertEqual(0, preflight.aggregate(nt_path, posix_path, output, True))
            self.assertEqual(0, preflight.aggregate(nt_path, posix_path, output, False))
            output.write_text("{}\n", encoding="utf-8")
            self.assertEqual(1, preflight.aggregate(nt_path, posix_path, output, False))

    def test_failed_leaf_pair_is_not_written_as_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            nt_path = root / "nt.json"
            posix_path = root / "posix.json"
            output = root / "report.json"
            changed = dict(self.posix, resolved_head="b" * 40)
            nt_path.write_text(json.dumps(self.nt) + "\n", encoding="utf-8")
            posix_path.write_text(json.dumps(changed) + "\n", encoding="utf-8")
            self.assertEqual(1, preflight.aggregate(nt_path, posix_path, output, True))
            self.assertFalse(output.exists())


class ObservationCollectionTests(unittest.TestCase):
    def test_collect_observation_binds_roots_head_blob_and_clean_state(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            primary = Path(temporary) / "exploring-l4-intelligence"
            repo = primary / ".worktrees" / "stage1b-readiness-remediation"
            common = primary / ".git"
            repo.mkdir(parents=True)
            common.mkdir()
            (repo / ".git").write_text(
                "gitdir: ../../.git/worktrees/stage1b-readiness-remediation\n",
                encoding="utf-8",
            )

            def fake_git(*args, cwd, allow_missing=False):
                if args[:3] == (
                    "rev-parse",
                    "--path-format=absolute",
                    "--git-common-dir",
                ):
                    return str(common)
                if args == ("rev-parse", "--show-toplevel"):
                    return str(repo if cwd == repo else primary)
                if args == ("rev-parse", "HEAD"):
                    return "c" * 40
                if args == (
                    "rev-parse",
                    f"{preflight.IMPLEMENTATION_FREEZE}:{preflight.PLAN_PATH}",
                ):
                    return preflight.IMPLEMENTATION_PLAN_BLOB
                if args[0] == "--git-dir":
                    return None
                if args == ("status", "--porcelain=v1"):
                    return ""
                raise AssertionError((args, cwd, allow_missing))

            with mock.patch.object(preflight, "_git", side_effect=fake_git):
                observed = preflight.collect_observation(repo)
            self.assertEqual("c" * 40, observed["resolved_head"])
            self.assertEqual(preflight.IMPLEMENTATION_PLAN_BLOB, observed["plan_blob"])
            self.assertTrue(observed["primary_clean"])
            self.assertTrue(observed["worktree_clean"])

    def test_collect_rejects_absolute_gitfile_before_git_calls(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            (repo / ".git").write_text("gitdir: D:/repo/.git/worktrees/x\n")
            with self.assertRaisesRegex(
                preflight.PreflightError, "gitfile-gitdir-must-be-relative"
            ):
                preflight.collect_observation(repo)


class CommandTests(unittest.TestCase):
    def test_leaf_mode_requires_output(self) -> None:
        with self.assertRaises(SystemExit):
            preflight.main(["--leaf"])

    def test_leaf_mode_delegates_to_writer(self) -> None:
        with mock.patch.object(preflight, "write_leaf", return_value=0) as writer:
            self.assertEqual(0, preflight.main(["--leaf", "--output", "leaf.json"]))
        writer.assert_called_once_with(Path("leaf.json"))


if __name__ == "__main__":
    unittest.main()
