#!/usr/bin/env python3
"""Tests for the deterministic consolidated Stage-1A package gate."""

from __future__ import annotations

import importlib.util
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).with_name("sf_current_package_check.py")
SPEC = importlib.util.spec_from_file_location("sf_current_package_check", SCRIPT)
assert SPEC and SPEC.loader
package_check = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(package_check)


EXPECTED_COMMANDS = (
    "python scripts/survey/test_sf_evidence_contract.py",
    "python scripts/survey/sf_absence_provenance_migrate.py --check",
    "python scripts/survey/sf_coding_generator.py --check",
    "python scripts/survey/test_sf_identity_taxonomy_v7_harness.py",
    "python scripts/survey/test_sf_h5_calibration_contract.py",
    "python scripts/survey/test_sf_pdf_extractor_contract.py",
    "python scripts/survey/test_sf_evidence_v7_aggregate.py",
    "python scripts/survey/test_sf_query_compiler_profiles.py",
    "python scripts/survey/sf_query_compiler.py --check --check-against wiki/survey/2026-07-15-sf-queries.jsonl",
    "python scripts/survey/test_sf_existing_corpus_disposition.py",
    "python scripts/survey/test_sf_bibliography_generator.py",
    "python scripts/survey/sf_current_manifest.py --check",
    "python scripts/survey/sf_release_binding_check.py",
    "python scripts/survey/sf_quantifier_scan.py",
    "python scripts/survey/sf_archive_candidates.py --check-applied",
    "python scripts/survey/sf_audit_immutability_check.py --check",
    "python scripts/checks/build_ai_context_manifest.py --check",
    "python scripts/checks/ai_context_surface_check.py",
)
TEST_GRAPH = {
    "policy": "fixture-stage0-code-graph",
    "nodes": [],
    "sha256": "0" * 64,
}


class CurrentPackageReportTests(unittest.TestCase):
    def test_real_command_order_is_the_plan_contract(self) -> None:
        self.assertEqual(EXPECTED_COMMANDS, package_check.COMMANDS)

    def test_nonzero_fixture_makes_complete_report_fail(self) -> None:
        calls: list[str] = []

        def runner(command: str, _repo: Path):
            calls.append(command)
            index = len(calls)
            return package_check.CommandExecution(
                7 if index == 2 else 0,
                f"stdout {index}\nRan 3 tests in 9.876s\n",
                f"stderr {index}\n",
            )

        raw, report = package_check.build_report(
            Path.cwd(), code_graph=TEST_GRAPH,
            commands=("python one.py", "python two.py", "python three.py"),
            command_runner=runner,
        )

        self.assertEqual(["python one.py", "python two.py", "python three.py"], calls)
        self.assertEqual("FAIL", report["verdict"])
        self.assertEqual([0, 7, 0], [row["exit_code"] for row in report["commands"]])
        self.assertEqual("Ran 3 tests", report["commands"][0]["stdout_tail"].splitlines()[-1])
        self.assertNotIn("9.876", raw.decode("utf-8"))

    def test_report_bytes_are_deterministic_and_hide_repo_absolute_path(self) -> None:
        repo = Path.cwd().resolve()

        def runner(command: str, _repo: Path):
            return package_check.CommandExecution(
                0,
                f"checked {repo / 'wiki' / 'survey'}\r\n",
                "",
            )

        first, _ = package_check.build_report(
            repo, code_graph=TEST_GRAPH,
            commands=("python check.py",), command_runner=runner
        )
        second, _ = package_check.build_report(
            repo, code_graph=TEST_GRAPH,
            commands=("python check.py",), command_runner=runner
        )
        self.assertEqual(first, second)
        self.assertTrue(first.endswith(b"\n"))
        self.assertNotIn(str(repo).encode("utf-8"), first)
        self.assertNotIn(repo.as_posix().encode("utf-8"), first)
        for forbidden in (b"generated_at", b"duration", b"head", b"self_sha"):
            self.assertNotIn(forbidden, first.lower())

    def test_runtime_platform_json_is_normalized_across_windows_and_posix(self) -> None:
        windows = (
            '{\n "verdict": "PASS",\n "platform": {\n'
            '  "os": "nt",\n  "python": "3.14.3"\n }\n}\n'
        )
        posix = (
            '{\n "verdict": "PASS",\n "platform": {\n'
            '  "os": "posix",\n  "python": "3.12.3"\n }\n}\n'
        )
        normalized_windows = package_check._normalized_tail(windows, Path.cwd())
        normalized_posix = package_check._normalized_tail(posix, Path.cwd())
        self.assertEqual(normalized_windows, normalized_posix)
        self.assertIn('"os": "<OS>"', normalized_windows)
        self.assertIn('"python": "<PYTHON>"', normalized_windows)

    def test_module_import_preserves_callers_sys_path_zero(self) -> None:
        marker = str(SCRIPT.parent)
        sys.path.insert(0, marker)
        try:
            spec = importlib.util.spec_from_file_location(
                "sf_current_package_check_import_contract", SCRIPT
            )
            assert spec and spec.loader
            imported = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(imported)
            self.assertEqual(marker, sys.path[0])
        finally:
            if sys.path and sys.path[0] == marker:
                del sys.path[0]


class CurrentPackageTransactionTests(unittest.TestCase):
    FIXTURE_COMMAND = "python scripts/survey/checker.py"

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name) / "repo"
        self.repo.mkdir()
        self.git("init", "-q")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "user.name", "Current Package Test")
        self.git("config", "core.autocrlf", "false")
        (self.repo / "README.md").write_text("fixture\n", encoding="utf-8")
        (self.repo / "scripts/survey").mkdir(parents=True)
        (self.repo / "scripts/checks").mkdir(parents=True)
        (self.repo / "scripts/survey/checker.py").write_text(
            "print('PASS')\n", encoding="utf-8"
        )
        shutil.copy2(SCRIPT, self.repo / "scripts/survey/sf_current_package_check.py")
        (self.repo / "scripts/checks/helper.py").write_text(
            "VALUE = 'trusted'\n", encoding="utf-8"
        )
        (self.repo / "scripts/wiki-sync.sh").write_text(
            "#!/bin/sh\nexit 0\n", encoding="utf-8"
        )
        self.git(
            "add", "README.md", "scripts/survey/checker.py",
            "scripts/survey/sf_current_package_check.py",
            "scripts/checks/helper.py", "scripts/wiki-sync.sh",
        )
        self.git("commit", "-qm", "fixture")
        (self.repo / package_check.REPORT_RELATIVE).parent.mkdir(parents=True)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def git(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *args], cwd=self.repo, check=True,
            capture_output=True, text=True, encoding="utf-8",
        )

    @staticmethod
    def passing_runner(command: str, _repo: Path):
        return package_check.CommandExecution(0, f"{command}: PASS\n", "")

    def assert_shadow_safe_cli(self, script: Path) -> None:
        sentinel = self.repo / "shadow-sentinel.txt"
        environment = os.environ.copy()
        environment["SF_PACKAGE_SHADOW_SENTINEL"] = str(sentinel)
        completed = subprocess.run(
            [sys.executable, str(script), "--check"],
            cwd=self.repo,
            env=environment,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        combined = completed.stdout + completed.stderr
        self.assertEqual(1, completed.returncode, combined)
        self.assertFalse(sentinel.exists(), combined)
        self.assertNotIn("SHADOW_SENTINEL_EXECUTED", combined)
        self.assertIn("untracked local code is forbidden: scripts/survey/json.py", combined)

    def install_shadow_sentinel(self, directory: Path) -> None:
        (directory / "json.py").write_text(
            "import os\n"
            "with open(os.environ['SF_PACKAGE_SHADOW_SENTINEL'], 'w', "
            "encoding='utf-8') as handle:\n"
            "    handle.write('SHADOW_SENTINEL_EXECUTED')\n"
            "print('SHADOW_SENTINEL_EXECUTED')\n",
            encoding="utf-8",
        )

    def write_stage_commit(self) -> Path:
        result = package_check.run(
            "write", repo=self.repo, commands=(self.FIXTURE_COMMAND,),
            command_runner=self.passing_runner,
        )
        self.assertEqual(0, result)
        report = self.repo / package_check.REPORT_RELATIVE
        self.git("add", package_check.REPORT_RELATIVE)
        self.git("commit", "-qm", "report")
        return report

    def test_write_is_deterministic_and_check_has_zero_side_effects(self) -> None:
        report = self.write_stage_commit()
        expected = report.read_bytes()
        before_status = self.git("status", "--porcelain=v1").stdout

        self.assertEqual(
            0,
            package_check.run(
                "write", repo=self.repo, commands=(self.FIXTURE_COMMAND,),
                command_runner=self.passing_runner,
            ),
        )
        self.assertEqual(expected, report.read_bytes())
        before_check_mtime = report.stat().st_mtime_ns
        self.assertEqual(
            0,
            package_check.run(
                "check", repo=self.repo, commands=(self.FIXTURE_COMMAND,),
                command_runner=self.passing_runner,
            ),
        )
        self.assertEqual(expected, report.read_bytes())
        self.assertEqual(before_status, self.git("status", "--porcelain=v1").stdout)
        self.assertEqual(before_check_mtime, report.stat().st_mtime_ns)
        self.assertEqual([], list(report.parent.glob(f".{report.name}.*.bak")))

    def test_postpublish_failure_rolls_back_without_backup_debris(self) -> None:
        report = self.write_stage_commit()
        old_bytes = report.read_bytes()
        old_mode = stat.S_IMODE(report.stat().st_mode)

        with mock.patch.object(
            package_check, "_trusted_bytes", return_value=b"injected mismatch"
        ):
            with self.assertRaisesRegex(
                package_check.CurrentPackageError,
                "published report bytes failed verification",
            ):
                package_check._atomic_write_report(
                    self.repo, report, b"replacement report\n"
                )

        self.assertEqual(old_bytes, report.read_bytes())
        if os.name == "posix":
            self.assertEqual(old_mode, stat.S_IMODE(report.stat().st_mode))
        self.assertEqual([], list(report.parent.glob(f".{report.name}.*.bak")))

    def test_failed_restore_preserves_the_only_recovery_backup(self) -> None:
        report = self.write_stage_commit()
        old_bytes = report.read_bytes()
        old_mode = stat.S_IMODE(report.stat().st_mode)
        real_replace = os.replace
        replace_count = 0

        def fail_restore(source: str | os.PathLike[str], target: str | os.PathLike[str]):
            nonlocal replace_count
            replace_count += 1
            if replace_count == 2:
                raise OSError("injected restore failure")
            return real_replace(source, target)

        with mock.patch.object(package_check.os, "replace", side_effect=fail_restore):
            with mock.patch.object(
                package_check, "_trusted_bytes", return_value=b"injected mismatch"
            ):
                with self.assertRaises(package_check.CurrentPackageError) as raised:
                    package_check._atomic_write_report(
                        self.repo, report, b"replacement report\n"
                    )

        backups = list(report.parent.glob(f".{report.name}.*.bak"))
        self.assertEqual(1, len(backups))
        backup = backups[0]
        self.assertEqual(old_bytes, backup.read_bytes())
        if os.name == "posix":
            self.assertEqual(old_mode, stat.S_IMODE(backup.stat().st_mode))
        self.assertEqual(b"replacement report\n", report.read_bytes())
        message = str(raised.exception)
        self.assertIn(backup.name, message)
        self.assertNotIn(str(report.parent), message)

        calls: list[str] = []

        def runner(command: str, _repo: Path):
            calls.append(command)
            return package_check.CommandExecution(0, "PASS\n", "")

        self.assertEqual(
            1,
            package_check.run(
                "write", repo=self.repo, commands=(self.FIXTURE_COMMAND,),
                command_runner=runner,
            ),
        )
        self.assertEqual([], calls)

    def test_stale_staged_report_fails_without_rewriting_it(self) -> None:
        report = self.write_stage_commit()
        before = report.read_bytes()

        def changed_runner(command: str, _repo: Path):
            return package_check.CommandExecution(0, f"{command}: CHANGED\n", "")

        self.assertEqual(
            1,
            package_check.run(
                "check", repo=self.repo, commands=(self.FIXTURE_COMMAND,),
                command_runner=changed_runner,
            ),
        )
        self.assertEqual(before, report.read_bytes())

    def test_dirty_checker_fails_before_identical_pass_runner(self) -> None:
        checker = self.repo / "scripts/survey/checker.py"
        checker.write_text("print('PASS')\n# dirty no-op\n", encoding="utf-8")
        calls: list[str] = []

        def runner(command: str, _repo: Path):
            calls.append(command)
            return package_check.CommandExecution(0, "PASS\n", "")

        self.assertEqual(
            1,
            package_check.run(
                "check", repo=self.repo, commands=(self.FIXTURE_COMMAND,),
                command_runner=runner,
            ),
        )
        self.assertEqual([], calls)

    def test_staged_checker_change_fails_check_but_write_may_run(self) -> None:
        checker = self.repo / "scripts/survey/checker.py"
        checker.write_text("print('PASS')\n# staged implementation\n", encoding="utf-8")
        self.git("add", "scripts/survey/checker.py")
        calls: list[str] = []

        def runner(command: str, _repo: Path):
            calls.append(command)
            return package_check.CommandExecution(0, "PASS\n", "")

        self.assertEqual(
            1,
            package_check.run(
                "check", repo=self.repo, commands=(self.FIXTURE_COMMAND,),
                command_runner=runner,
            ),
        )
        self.assertEqual([], calls)
        self.assertEqual(
            0,
            package_check.run(
                "write", repo=self.repo, commands=(self.FIXTURE_COMMAND,),
                command_runner=runner,
            ),
        )
        self.assertEqual([self.FIXTURE_COMMAND], calls)

    def test_untracked_shadow_fails_before_subprocess(self) -> None:
        (self.repo / "scripts/survey/json.py").write_text(
            "raise RuntimeError('shadow')\n", encoding="utf-8"
        )
        calls: list[str] = []

        def runner(command: str, _repo: Path):
            calls.append(command)
            return package_check.CommandExecution(0, "PASS\n", "")

        self.assertEqual(
            1,
            package_check.run(
                "write", repo=self.repo, commands=(self.FIXTURE_COMMAND,),
                command_runner=runner,
            ),
        )
        self.assertEqual([], calls)

    def test_cli_bootstrap_direct_path_does_not_import_untracked_json(self) -> None:
        self.install_shadow_sentinel(self.repo / "scripts/survey")
        self.assert_shadow_safe_cli(
            self.repo / "scripts/survey/sf_current_package_check.py"
        )

    def test_cli_bootstrap_mixed_case_path_does_not_import_untracked_json(self) -> None:
        self.install_shadow_sentinel(self.repo / "scripts/survey")
        if os.name == "nt":
            script = self.repo / "ScRiPtS/SuRvEy/sf_current_package_check.py"
        else:
            mixed = self.repo / "ScRiPtS/SuRvEy"
            mixed.mkdir(parents=True)
            shutil.copy2(SCRIPT, mixed / "sf_current_package_check.py")
            self.install_shadow_sentinel(mixed)
            script = mixed / "sf_current_package_check.py"
        self.assert_shadow_safe_cli(script)

    @unittest.skipUnless(os.name == "posix", "symlink alias launch contract")
    def test_cli_bootstrap_symlink_alias_does_not_import_untracked_json(self) -> None:
        self.install_shadow_sentinel(self.repo / "scripts/survey")
        alias = self.repo / "bootstrap-alias"
        alias.symlink_to(self.repo / "scripts/survey", target_is_directory=True)
        self.assert_shadow_safe_cli(alias / "sf_current_package_check.py")

    def test_untracked_checks_module_fails_before_subprocess(self) -> None:
        (self.repo / "scripts/checks/local_module.py").write_text(
            "VALUE = 'untracked'\n", encoding="utf-8"
        )
        calls: list[str] = []

        def runner(command: str, _repo: Path):
            calls.append(command)
            return package_check.CommandExecution(0, "PASS\n", "")

        self.assertEqual(
            1,
            package_check.run(
                "write", repo=self.repo, commands=(self.FIXTURE_COMMAND,),
                command_runner=runner,
            ),
        )
        self.assertEqual([], calls)

    @unittest.skipUnless(os.name == "posix", "real code symlink contract")
    def test_symlinked_code_fails_before_subprocess(self) -> None:
        outside = Path(self.temp.name) / "outside.py"
        outside.write_text("raise RuntimeError('outside')\n", encoding="utf-8")
        (self.repo / "scripts/survey/link.py").symlink_to(outside)
        calls: list[str] = []

        def runner(command: str, _repo: Path):
            calls.append(command)
            return package_check.CommandExecution(0, "PASS\n", "")

        self.assertEqual(
            1,
            package_check.run(
                "write", repo=self.repo, commands=(self.FIXTURE_COMMAND,),
                command_runner=runner,
            ),
        )
        self.assertEqual([], calls)

    def test_report_git_mode_must_be_100644_before_subprocess(self) -> None:
        self.write_stage_commit()
        self.git("update-index", "--chmod=+x", package_check.REPORT_RELATIVE)
        calls: list[str] = []

        def runner(command: str, _repo: Path):
            calls.append(command)
            return package_check.CommandExecution(0, "PASS\n", "")

        self.assertEqual(
            1,
            package_check.run(
                "check", repo=self.repo, commands=(self.FIXTURE_COMMAND,),
                command_runner=runner,
            ),
        )
        self.assertEqual([], calls)

    @unittest.skipUnless(os.name == "posix", "POSIX mode contract")
    def test_write_fixes_report_mode_to_0644(self) -> None:
        report = self.write_stage_commit()
        report.chmod(0o600)

        self.assertEqual(
            0,
            package_check.run(
                "write", repo=self.repo, commands=(self.FIXTURE_COMMAND,),
                command_runner=self.passing_runner,
            ),
        )
        self.assertEqual(0o644, stat.S_IMODE(report.stat().st_mode))

    def test_mountinfo_identifies_drvfs_without_metadata_as_mode_incapable(self) -> None:
        mountinfo = (
            "10 1 8:1 / / rw,relatime - ext4 /dev/sda rw\n"
            "11 10 0:42 / /mnt/d rw,noatime - 9p D:\\\\ rw,"
            "aname=drvfs;path=D:\\\\;uid=1000\n"
        )
        self.assertFalse(
            package_check._mountinfo_exposes_posix_mode(
                "/mnt/d/repo/report.json", mountinfo
            )
        )
        self.assertTrue(
            package_check._mountinfo_exposes_posix_mode(
                "/repo/report.json", mountinfo
            )
        )

    def test_mountinfo_accepts_drvfs_when_metadata_is_enabled(self) -> None:
        mountinfo = (
            "11 10 0:42 / /mnt/d rw,noatime,metadata - 9p D:\\\\ rw,"
            "aname=drvfs;path=D:\\\\;uid=1000\n"
        )
        self.assertTrue(
            package_check._mountinfo_exposes_posix_mode(
                "/mnt/d/repo/report.json", mountinfo
            )
        )

    def test_current_commands_have_no_legacy_writing_harness(self) -> None:
        self.assertEqual(set(), package_check.STAGED_SANDBOX_COMMANDS)
        self.assertFalse(
            any("sf_identity_taxonomy_v6_test.py" in row for row in package_check.COMMANDS)
        )

    def test_write_refuses_dirty_or_untracked_existing_report(self) -> None:
        report = self.write_stage_commit()
        report.write_bytes(b"dirty\n")
        self.assertEqual(
            1,
            package_check.run(
                "write", repo=self.repo, commands=(self.FIXTURE_COMMAND,),
                command_runner=self.passing_runner,
            ),
        )
        self.assertEqual(b"dirty\n", report.read_bytes())

        self.git("restore", package_check.REPORT_RELATIVE)
        self.git("rm", "-q", package_check.REPORT_RELATIVE)
        self.git("commit", "-qm", "remove report")
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_bytes(b"untracked sentinel\n")
        self.assertEqual(
            1,
            package_check.run(
                "write", repo=self.repo, commands=(self.FIXTURE_COMMAND,),
                command_runner=self.passing_runner,
            ),
        )
        self.assertEqual(b"untracked sentinel\n", report.read_bytes())

    @unittest.skipUnless(hasattr(os, "symlink"), "symlink unavailable")
    def test_write_rejects_symlinked_output_ancestor(self) -> None:
        checks = self.repo / "docs" / "checks"
        shutil.rmtree(self.repo / "docs")
        checks.parent.mkdir(exist_ok=True)
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        try:
            checks.symlink_to(outside, target_is_directory=True)
        except OSError as error:
            self.skipTest(f"symlink creation unavailable: {error}")

        self.assertEqual(
            1,
            package_check.run(
                "write", repo=self.repo, commands=(self.FIXTURE_COMMAND,),
                command_runner=self.passing_runner,
            ),
        )
        self.assertEqual([], list(outside.iterdir()))


if __name__ == "__main__":
    unittest.main()
