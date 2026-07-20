#!/usr/bin/env python3
"""Offline integration tests for the wiki-sync publication boundary."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts/wiki-sync.sh"
REAL_GIT = shutil.which("git") or "/usr/bin/git"


@unittest.skipUnless(os.name == "posix", "linked-worktree shell contract runs in WSL/POSIX")
class WikiSyncBoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix=".wiki-sync-fixture-", dir=REPO)
        self.root = Path(self.temp.name)
        self.source = self.root / "source"
        self.linked = self.root / "linked"
        self.remotes = self.root / "remotes"
        self.remotes.mkdir()
        self.project_remote = self.remotes / "project.git"
        self.wiki_remote = self.remotes / "project.wiki.git"

        self.git("init", "-q", "-b", "master", str(self.source), cwd=self.root)
        self.git("-C", str(self.source), "config", "user.name", "Wiki Sync Test")
        self.git("-C", str(self.source), "config", "user.email", "test@example.invalid")
        (self.source / "scripts").mkdir()
        shutil.copy2(SCRIPT, self.source / "scripts/wiki-sync.sh")
        (self.source / "wiki").mkdir()
        (self.source / "wiki/Page.md").write_text("source v1\n", encoding="utf-8")
        self.git("-C", str(self.source), "add", "scripts/wiki-sync.sh", "wiki/Page.md")
        self.git("-C", str(self.source), "commit", "-qm", "source")
        self.git("-C", str(self.source), "remote", "add", "origin", str(self.project_remote))
        self.git("-C", str(self.source), "worktree", "add", "-q", "-b", "task", str(self.linked))

        pointer = (self.linked / ".git").read_text(encoding="utf-8").strip()
        match = re.fullmatch(r"gitdir: /mnt/([a-zA-Z])/(.+)", pointer)
        if match is None:
            self.skipTest(f"fixture is not on a WSL-mounted drive: {pointer}")
        drive, remainder = match.groups()
        (self.linked / ".git").write_text(
            f"gitdir: {drive.upper()}:/{remainder}\n", encoding="utf-8", newline="\n"
        )
        (self.linked / "wiki/Page.md").write_text("source v2\n", encoding="utf-8")

        seed = self.root / "wiki-seed"
        self.git("init", "-q", "-b", "master", str(seed), cwd=self.root)
        self.git("-C", str(seed), "config", "user.name", "Wiki Sync Test")
        self.git("-C", str(seed), "config", "user.email", "test@example.invalid")
        (seed / "Page.md").write_text("remote v1\n", encoding="utf-8")
        self.git("-C", str(seed), "add", "Page.md")
        self.git("-C", str(seed), "commit", "-qm", "wiki seed")
        self.git("init", "-q", "--bare", str(self.wiki_remote), cwd=self.root)
        self.git("-C", str(seed), "remote", "add", "origin", str(self.wiki_remote))
        self.git("-C", str(seed), "push", "-q", "-u", "origin", "master")
        self.git("--git-dir", str(self.wiki_remote), "symbolic-ref", "HEAD", "refs/heads/master")

        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.git_log = self.root / "git.log"
        shim = self.bin / "git"
        shim.write_text(
            "#!/bin/sh\n"
            "printf '%s\\n' \"$*\" >> \"$GIT_LOG\"\n"
            f"exec {REAL_GIT} \"$@\"\n",
            encoding="utf-8",
            newline="\n",
        )
        shim.chmod(0o755)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def git(self, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [REAL_GIT, *args], cwd=cwd, check=True, capture_output=True,
            text=True, encoding="utf-8",
        )

    def ref(self, repository: Path, ref: str = "refs/heads/master") -> str:
        return self.git("--git-dir", str(repository), "rev-parse", ref).stdout.strip()

    def run_sync(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["PATH"] = f"{self.bin}:{environment['PATH']}"
        environment["GIT_LOG"] = str(self.git_log)
        return subprocess.run(
            ["bash", str(self.linked / "scripts/wiki-sync.sh"), *arguments],
            cwd=self.linked,
            env=environment,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

    def logged_git_commands(self) -> list[str]:
        if not self.git_log.exists():
            return []
        return self.git_log.read_text(encoding="utf-8").splitlines()

    def assert_no_commit_or_push(self) -> None:
        for command in self.logged_git_commands():
            tokens = command.split()
            self.assertNotIn("commit", tokens, command)
            self.assertNotIn("push", tokens, command)

    def test_linked_worktree_dry_run_never_commits_or_pushes(self) -> None:
        remote_before = self.ref(self.wiki_remote)
        source_before = self.git("-C", str(self.source), "rev-parse", "task").stdout.strip()

        completed = self.run_sync("--dry-run")

        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
        self.assertTrue(
            completed.stdout.rstrip().endswith("[dry-run] not committing or pushing."),
            completed.stdout,
        )
        self.assertEqual(remote_before, self.ref(self.wiki_remote))
        self.assertEqual(
            source_before,
            self.git("-C", str(self.source), "rev-parse", "task").stdout.strip(),
        )
        self.assertFalse((self.linked / ".wiki-tmp").exists())
        self.assert_no_commit_or_push()

    def test_cr_suffixed_and_unknown_arguments_fail_before_git(self) -> None:
        for argument in ("--dry-run\r", "--unknown"):
            with self.subTest(argument=repr(argument)):
                self.git_log.unlink(missing_ok=True)
                remote_before = self.ref(self.wiki_remote)
                completed = self.run_sync(argument)
                self.assertNotEqual(0, completed.returncode)
                self.assertIn("unsupported argument", completed.stderr)
                self.assertEqual([], self.logged_git_commands())
                self.assertEqual(remote_before, self.ref(self.wiki_remote))


if __name__ == "__main__":
    unittest.main()
