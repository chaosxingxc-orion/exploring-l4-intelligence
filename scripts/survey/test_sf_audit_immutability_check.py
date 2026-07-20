from __future__ import annotations

import hashlib
import json
import os
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
        report = audit.OUT_RELATIVE
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

    def make_lineage_fixture(
        self, root: Path
    ) -> tuple[str, str, str, list[dict[str, str]], dict[str, str]]:
        run_git(root, "init", "-q")
        registry = "wiki/survey/sf-audit-artifact-registry.json"
        anchor = "scripts/checks/ai_context_inventory.py"
        report = audit.OUT_RELATIVE
        registered_paths = [
            "wiki/audit/example/round-1/review.md",
            "wiki/audit/example/round-2/review.md",
        ]
        replacement_path = "wiki/audit/example/unregistered-replacement.md"
        for relative in [*registered_paths, replacement_path, registry, anchor, report]:
            (root / relative).parent.mkdir(parents=True, exist_ok=True)
        for index, relative in enumerate([*registered_paths, replacement_path], start=1):
            (root / relative).write_bytes(f"immutable review {index}\n".encode())
            run_git(root, "add", relative)
        rows = [
            {
                "path": relative,
                "git_blob": run_git(root, "hash-object", relative).stdout.strip(),
            }
            for relative in registered_paths
        ]
        replacement = {
            "path": replacement_path,
            "git_blob": run_git(root, "hash-object", replacement_path).stdout.strip(),
        }
        self.stage_registry_transaction(root, registry, anchor, rows)
        (root / report).write_bytes(b"{}\n")
        run_git(root, "add", report)
        run_git(
            root,
            "-c",
            "user.name=Audit Fixture",
            "-c",
            "user.email=audit@example.invalid",
            "commit",
            "-q",
            "-m",
            "lineage fixture",
        )
        return registry, anchor, report, rows, replacement

    def stage_registry_transaction(
        self,
        root: Path,
        registry: str,
        anchor: str,
        rows: list[dict[str, str]],
    ) -> None:
        (root / registry).write_text(
            json.dumps({"artifacts": rows}, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        (root / anchor).write_text(
            f"REGISTRY_BASELINE_COUNT = {len(rows)}\n"
            f'REGISTRY_BASELINE_PREFIX_SHA256 = "{registry_prefix_sha256(rows)}"\n',
            encoding="utf-8",
            newline="\n",
        )
        run_git(root, "add", registry, anchor)

    def commit_new_artifacts(
        self, root: Path, count: int
    ) -> list[dict[str, str]]:
        rows: list[dict[str, str]] = []
        for index in range(count):
            relative = f"wiki/audit/example/new-{index + 1}.md"
            (root / relative).parent.mkdir(parents=True, exist_ok=True)
            (root / relative).write_bytes(f"new immutable {index + 1}\n".encode())
            run_git(root, "add", relative)
            rows.append(
                {
                    "path": relative,
                    "git_blob": run_git(root, "hash-object", relative).stdout.strip(),
                }
            )
        run_git(
            root,
            "-c",
            "user.name=Audit Fixture",
            "-c",
            "user.email=audit@example.invalid",
            "commit",
            "-q",
            "-m",
            "add immutable artifacts",
        )
        return rows

    def assert_write_rejected_without_report_change(
        self, root: Path, registry: str, anchor: str, report: str
    ) -> None:
        before = (root / report).read_bytes()
        self.assertEqual(
            1,
            audit.run(
                "write",
                repo=root,
                registry_relative=registry,
                anchor_relative=anchor,
            ),
        )
        self.assertEqual(before, (root / report).read_bytes())

    def test_registry_rejects_coordinated_deletion_and_reanchor(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            registry, anchor, report, rows, _ = self.make_lineage_fixture(root)
            self.stage_registry_transaction(root, registry, anchor, rows[:1])
            self.assert_write_rejected_without_report_change(
                root, registry, anchor, report
            )

    def test_registry_rejects_rewriting_an_old_row_to_another_head_artifact(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            registry, anchor, report, rows, replacement = self.make_lineage_fixture(
                root
            )
            self.stage_registry_transaction(
                root, registry, anchor, [replacement, rows[1]]
            )
            self.assert_write_rejected_without_report_change(
                root, registry, anchor, report
            )

    def test_registry_rejects_reordering_unchanged_rows(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            registry, anchor, report, rows, _ = self.make_lineage_fixture(root)
            self.stage_registry_transaction(root, registry, anchor, list(reversed(rows)))
            self.assert_write_rejected_without_report_change(
                root, registry, anchor, report
            )

    def test_registry_rejects_growth_by_two(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            registry, anchor, report, rows, _ = self.make_lineage_fixture(root)
            additions = self.commit_new_artifacts(root, 2)
            self.stage_registry_transaction(root, registry, anchor, rows + additions)
            self.assert_write_rejected_without_report_change(
                root, registry, anchor, report
            )

    def test_registry_accepts_unchanged_transaction(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            registry, anchor, report, _, _ = self.make_lineage_fixture(root)
            self.assertEqual(
                0,
                audit.run(
                    "write",
                    repo=root,
                    registry_relative=registry,
                    anchor_relative=anchor,
                ),
            )

    def test_registry_accepts_one_atomic_append_with_anchor_sync(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            registry, anchor, report, rows, _ = self.make_lineage_fixture(root)
            addition = self.commit_new_artifacts(root, 1)
            self.stage_registry_transaction(root, registry, anchor, rows + addition)
            self.assertEqual(
                0,
                audit.run(
                    "write",
                    repo=root,
                    registry_relative=registry,
                    anchor_relative=anchor,
                ),
            )
            run_git(root, "add", report)
            self.assertEqual(
                0,
                audit.run(
                    "check",
                    repo=root,
                    registry_relative=registry,
                    anchor_relative=anchor,
                ),
            )
            run_git(
                root,
                "-c",
                "user.name=Audit Fixture",
                "-c",
                "user.email=audit@example.invalid",
                "commit",
                "-q",
                "-m",
                "commit one-row registry transaction",
            )
            self.assertEqual(
                0,
                audit.run(
                    "check",
                    repo=root,
                    registry_relative=registry,
                    anchor_relative=anchor,
                ),
            )

    def test_write_rejects_dirty_report_without_overwriting_it(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            registry, anchor, report = self.make_fixture(root)
            dirty = b"uncommitted human notes\n"
            (root / report).write_bytes(dirty)
            self.assert_write_rejected_without_report_change(
                root, registry, anchor, report
            )

    @unittest.skipUnless(os.name == "posix", "requires WSL/POSIX symlinks")
    def test_write_rejects_report_symlink_and_preserves_external_sentinel(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = base / "repo"
            root.mkdir()
            registry, anchor, report = self.make_fixture(root)
            sentinel = base / "outside-report.json"
            sentinel.write_bytes(b"external sentinel\n")
            (root / report).unlink()
            (root / report).symlink_to(sentinel)
            before = sentinel.read_bytes()
            self.assertEqual(
                1,
                audit.run(
                    "write",
                    repo=root,
                    registry_relative=registry,
                    anchor_relative=anchor,
                ),
            )
            self.assertTrue((root / report).is_symlink())
            self.assertEqual(before, sentinel.read_bytes())

    @unittest.skipUnless(os.name == "posix", "requires WSL/POSIX symlinks")
    def test_write_rejects_symlink_ancestor_and_preserves_external_sentinel(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = base / "repo"
            root.mkdir()
            registry, anchor, report = self.make_fixture(root)
            checks = (root / report).parent
            (root / report).unlink()
            checks.rmdir()
            outside = base / "outside-checks"
            outside.mkdir()
            sentinel = outside / Path(report).name
            sentinel.write_bytes(b"external sentinel\n")
            checks.symlink_to(outside, target_is_directory=True)
            before = sentinel.read_bytes()
            self.assertEqual(
                1,
                audit.run(
                    "write",
                    repo=root,
                    registry_relative=registry,
                    anchor_relative=anchor,
                ),
            )
            self.assertEqual(before, sentinel.read_bytes())

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
                ),
            )
            run_git(
                root,
                "-c",
                "user.name=Audit Fixture",
                "-c",
                "user.email=audit@example.invalid",
                "commit",
                "-q",
                "-m",
                "record generated report",
            )
            status_before = run_git(root, "status", "--porcelain=v1").stdout
            self.assertEqual(
                0,
                audit.run(
                    "write",
                    repo=root,
                    registry_relative=registry,
                    anchor_relative=anchor,
                ),
            )
            self.assertEqual(first, (root / report).read_bytes())
            self.assertEqual(
                status_before, run_git(root, "status", "--porcelain=v1").stdout
            )


if __name__ == "__main__":
    unittest.main()
