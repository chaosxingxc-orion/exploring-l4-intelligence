from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import sf_audit_immutability_check as audit


def run_git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def registry_prefix_sha256(rows: list[dict[str, str]]) -> str:
    raw = json.dumps(
        [{"path": row["path"], "git_blob": row["git_blob"]} for row in rows],
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


class AuditImmutabilityGitTests(unittest.TestCase):
    def test_live_git_read_works_from_native_or_linked_worktree(self) -> None:
        completed = audit.git("rev-parse", "--show-toplevel")
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertTrue(completed.stdout.strip())
        self.assertEqual(
            Path(audit.REPO).resolve(),
            Path(completed.stdout.strip()).resolve(),
        )

    def test_git_failure_is_rejected_instead_of_becoming_empty_evidence(self) -> None:
        failed = subprocess.CompletedProcess(
            ["git", "rev-parse", "HEAD"],
            128,
            stdout="",
            stderr="fatal: invalid worktree pointer",
        )
        with mock.patch.object(audit.subprocess, "run", return_value=failed):
            with self.assertRaises(subprocess.CalledProcessError):
                audit.git("rev-parse", "HEAD")


class AuditImmutabilityModeTests(unittest.TestCase):
    def test_default_and_explicit_check_are_zero_write_in_real_repo(self) -> None:
        for arguments in ([], ["--check"]):
            with self.subTest(arguments=arguments):
                report_before = audit.OUT.read_bytes()
                status_before = audit.git("status", "--porcelain=v1").stdout
                config_before = audit.git(
                    "config", "--local", "--list", "--show-origin"
                ).stdout
                try:
                    completed = subprocess.run(
                        [sys.executable, str(Path(audit.__file__).resolve()), *arguments],
                        cwd=audit.REPO,
                        capture_output=True,
                        text=True,
                        encoding="utf-8",
                    )
                    report_after = audit.OUT.read_bytes()
                    status_after = audit.git("status", "--porcelain=v1").stdout
                    config_after = audit.git(
                        "config", "--local", "--list", "--show-origin"
                    ).stdout
                finally:
                    if audit.OUT.read_bytes() != report_before:
                        audit.OUT.write_bytes(report_before)
                self.assertEqual(
                    0, completed.returncode, completed.stdout + completed.stderr
                )
                self.assertEqual(report_before, report_after)
                self.assertEqual(status_before, status_after)
                self.assertEqual(config_before, config_after)

    def make_fixture(self, root: Path) -> tuple[str, str, str]:
        run_git(root, "init", "-q")
        artifact = "wiki/audit/example/round-1/review.md"
        registry = "wiki/survey/sf-audit-artifact-registry.json"
        anchor = "scripts/checks/ai_context_inventory.py"
        report = "docs/checks/audit-immutability.json"
        for relative in (artifact, registry, anchor, report):
            (root / relative).parent.mkdir(parents=True, exist_ok=True)
        (root / artifact).write_bytes(b"immutable review\n")
        run_git(root, "add", artifact)
        blob = run_git(root, "hash-object", artifact).stdout.strip()
        rows = [{"path": artifact, "git_blob": blob}]
        (root / registry).write_text(
            json.dumps({"artifacts": rows}, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        (root / anchor).write_text(
            "REGISTRY_BASELINE_COUNT = 1\n"
            f'REGISTRY_BASELINE_PREFIX_SHA256 = "{registry_prefix_sha256(rows)}"\n',
            encoding="utf-8",
            newline="\n",
        )
        (root / report).write_bytes(b"{}\n")
        run_git(root, "add", artifact, registry, anchor, report)
        run_git(
            root,
            "-c",
            "user.name=Audit Fixture",
            "-c",
            "user.email=audit@example.invalid",
            "commit",
            "-q",
            "-m",
            "fixture",
        )
        return registry, anchor, report

    def test_stale_report_fails_without_side_effects(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            registry, anchor, report = self.make_fixture(root)
            self.assertEqual(
                0,
                audit.run(
                    "write",
                    repo=root,
                    registry_relative=registry,
                    anchor_relative=anchor,
                    output_relative=report,
                ),
            )
            run_git(root, "add", report)
            (root / report).write_bytes(b'{"status":"STALE"}\n')
            run_git(root, "add", report)
            bytes_before = (root / report).read_bytes()
            status_before = run_git(root, "status", "--porcelain=v1").stdout
            config_before = run_git(
                root, "config", "--local", "--list", "--show-origin"
            ).stdout
            self.assertEqual(
                1,
                audit.run(
                    "check",
                    repo=root,
                    registry_relative=registry,
                    anchor_relative=anchor,
                    output_relative=report,
                ),
            )
            self.assertEqual(bytes_before, (root / report).read_bytes())
            self.assertEqual(
                status_before, run_git(root, "status", "--porcelain=v1").stdout
            )
            self.assertEqual(
                config_before,
                run_git(root, "config", "--local", "--list", "--show-origin").stdout,
            )

    def test_write_is_deterministic_and_check_accepts_staged_report(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            registry, anchor, report = self.make_fixture(root)
            self.assertEqual(
                0,
                audit.run(
                    "write",
                    repo=root,
                    registry_relative=registry,
                    anchor_relative=anchor,
                    output_relative=report,
                ),
            )
            first = (root / report).read_bytes()
            run_git(root, "add", report)
            self.assertEqual(
                0,
                audit.run(
                    "check",
                    repo=root,
                    registry_relative=registry,
                    anchor_relative=anchor,
                    output_relative=report,
                ),
            )
            status_before = run_git(root, "status", "--porcelain=v1").stdout
            self.assertEqual(
                0,
                audit.run(
                    "write",
                    repo=root,
                    registry_relative=registry,
                    anchor_relative=anchor,
                    output_relative=report,
                ),
            )
            self.assertEqual(first, (root / report).read_bytes())
            self.assertEqual(
                status_before, run_git(root, "status", "--porcelain=v1").stdout
            )


if __name__ == "__main__":
    unittest.main()
