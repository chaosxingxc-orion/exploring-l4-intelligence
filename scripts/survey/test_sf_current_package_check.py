#!/usr/bin/env python3
"""Tests for the deterministic consolidated Stage-1A package gate."""

from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("sf_current_package_check.py")
SPEC = importlib.util.spec_from_file_location("sf_current_package_check", SCRIPT)
assert SPEC and SPEC.loader
package_check = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(package_check)


EXPECTED_COMMANDS = (
    "python scripts/survey/test_sf_evidence_contract.py",
    "python scripts/survey/sf_schema_v3_migrate.py --check",
    "python scripts/survey/sf_coding_generator.py --check",
    "python scripts/survey/sf_identity_taxonomy_v6_test.py",
    "python scripts/survey/sf_dual_platform_check.py",
    "python scripts/survey/test_sf_query_compiler_profiles.py",
    "python scripts/survey/sf_query_compiler.py --check --check-against wiki/survey/2026-07-15-sf-queries.jsonl",
    "python scripts/survey/sf_current_tables.py --check",
    "python scripts/survey/sf_current_manifest.py --check",
    "python scripts/survey/sf_release_binding_check.py",
    "python scripts/survey/sf_quantifier_scan.py",
    "python scripts/survey/sf_archive_candidates.py --check-applied",
    "python scripts/survey/sf_audit_immutability_check.py --check",
    "python scripts/checks/build_ai_context_manifest.py --check",
    "python scripts/checks/ai_context_surface_check.py",
)


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
            Path.cwd(), commands=("python one.py", "python two.py", "python three.py"),
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
            repo, commands=("python check.py",), command_runner=runner
        )
        second, _ = package_check.build_report(
            repo, commands=("python check.py",), command_runner=runner
        )
        self.assertEqual(first, second)
        self.assertTrue(first.endswith(b"\n"))
        self.assertNotIn(str(repo).encode("utf-8"), first)
        self.assertNotIn(repo.as_posix().encode("utf-8"), first)
        for forbidden in (b"generated_at", b"duration", b"head", b"self_sha"):
            self.assertNotIn(forbidden, first.lower())


class CurrentPackageTransactionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name) / "repo"
        self.repo.mkdir()
        self.git("init", "-q")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "user.name", "Current Package Test")
        (self.repo / "README.md").write_text("fixture\n", encoding="utf-8")
        self.git("add", "README.md")
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

    def write_stage_commit(self) -> Path:
        result = package_check.run(
            "write", repo=self.repo, commands=("python fixture.py",),
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
                "write", repo=self.repo, commands=("python fixture.py",),
                command_runner=self.passing_runner,
            ),
        )
        self.assertEqual(expected, report.read_bytes())
        before_check_mtime = report.stat().st_mtime_ns
        self.assertEqual(
            0,
            package_check.run(
                "check", repo=self.repo, commands=("python fixture.py",),
                command_runner=self.passing_runner,
            ),
        )
        self.assertEqual(expected, report.read_bytes())
        self.assertEqual(before_status, self.git("status", "--porcelain=v1").stdout)
        self.assertEqual(before_check_mtime, report.stat().st_mtime_ns)

    def test_stale_staged_report_fails_without_rewriting_it(self) -> None:
        report = self.write_stage_commit()
        before = report.read_bytes()

        def changed_runner(command: str, _repo: Path):
            return package_check.CommandExecution(0, f"{command}: CHANGED\n", "")

        self.assertEqual(
            1,
            package_check.run(
                "check", repo=self.repo, commands=("python fixture.py",),
                command_runner=changed_runner,
            ),
        )
        self.assertEqual(before, report.read_bytes())

    def test_known_mutating_v6_command_runs_only_in_staged_sandbox(self) -> None:
        script = self.repo / "scripts/survey/sf_identity_taxonomy_v6_test.py"
        script.parent.mkdir(parents=True)
        script.write_text(
            "from pathlib import Path\n"
            "Path('mutated.txt').write_text('bad', encoding='utf-8')\n"
            "print(Path.cwd())\n",
            encoding="utf-8",
        )
        self.git("add", "scripts/survey/sf_identity_taxonomy_v6_test.py")
        self.git("commit", "-qm", "mutating fixture")

        execution = package_check._default_command_runner(
            package_check.COMMANDS[3], self.repo
        )

        self.assertEqual(0, execution.exit_code)
        self.assertFalse((self.repo / "mutated.txt").exists())
        self.assertIn(str(self.repo), execution.stdout)

    def test_write_refuses_dirty_or_untracked_existing_report(self) -> None:
        report = self.write_stage_commit()
        report.write_bytes(b"dirty\n")
        self.assertEqual(
            1,
            package_check.run(
                "write", repo=self.repo, commands=("python fixture.py",),
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
                "write", repo=self.repo, commands=("python fixture.py",),
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
                "write", repo=self.repo, commands=("python fixture.py",),
                command_runner=self.passing_runner,
            ),
        )
        self.assertEqual([], list(outside.iterdir()))


if __name__ == "__main__":
    unittest.main()
