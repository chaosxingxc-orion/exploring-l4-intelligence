from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import sf_audit_immutability_check as audit


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


if __name__ == "__main__":
    unittest.main()
