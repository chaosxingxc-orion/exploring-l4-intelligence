#!/usr/bin/env python3
"""Contract tests for the manifest-driven Stage-1A current survey layer."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
SURVEY_SCRIPTS = REPO / "scripts" / "survey"
CURRENT = REPO / "wiki" / "survey" / "current"
REPORT_PATH = (
    "docs/checks/system-first-stage1a/evidence-v6/"
    "identity-taxonomy-v6-test.json"
)


def load_module(name: str):
    path = SURVEY_SCRIPTS / f"{name}.py"
    if not path.is_file():
        raise AssertionError(f"implementation module missing: {path}")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load implementation module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def current_report():
    raw = (REPO / REPORT_PATH).read_bytes()
    return json.loads(raw), raw


class OpeningTableContractTests(unittest.TestCase):
    def setUp(self):
        self.tables = load_module("sf_current_tables")
        self.release = load_module("sf_release_binding_check")
        self.report, self.report_raw = current_report()

    def test_table_is_bound_to_exact_report_bytes_and_canonical_headline(self):
        raw = self.tables.render_opening_table(
            self.report, REPORT_PATH, self.report_raw
        )
        text = raw.decode("utf-8")
        expected_sha = hashlib.sha256(self.report_raw).hexdigest()
        self.assertIn(
            f'<!-- source_binding: {{"path":"{REPORT_PATH}",'
            f'"sha256":"{expected_sha}"}} -->',
            text,
        )
        self.assertIn(self.release.render_headline(self.report), text)
        self.assertEqual(1, text.count("<!-- generated_headline_begin -->"))
        self.assertEqual(1, text.count("<!-- generated_headline_end -->"))

    def test_table_states_bounded_stage_and_both_denominators(self):
        text = self.tables.render_opening_table(
            self.report, REPORT_PATH, self.report_raw
        ).decode("utf-8")
        self.assertIn("Stage-1A", text)
        self.assertIn("directional-only / hypothesis-grade", text)
        self.assertRegex(text, r"method-path[^\n]*11")
        self.assertRegex(text, r"unique-work[^\n]*8")
        self.assertIn("zero Stage-1B executions in this repair", text)
        self.assertIn("not a readiness determination", text)
        self.assertIn("not a reviewer signature", text)
        self.assertIn("not owner Stage-1B execution approval", text)

    def test_table_render_is_deterministic_and_timestamp_free(self):
        first = self.tables.render_opening_table(
            self.report, REPORT_PATH, self.report_raw
        )
        second = self.tables.render_opening_table(
            self.report, REPORT_PATH, self.report_raw
        )
        self.assertEqual(first, second)
        self.assertNotIn(b"generated_at", first)
        self.assertTrue(first.endswith(b"\n"))

    def test_report_sha_changes_when_source_bytes_change(self):
        first = self.tables.render_opening_table(
            self.report, REPORT_PATH, self.report_raw
        )
        changed = self.tables.render_opening_table(
            self.report, REPORT_PATH, self.report_raw + b" ",
        )
        self.assertNotEqual(first, changed)


class CurrentManifestContractTests(unittest.TestCase):
    def setUp(self):
        self.manifest = load_module("sf_current_manifest")
        self.payloads = {
            spec.path: f"payload:{spec.path}\n".encode("utf-8")
            for spec in self.manifest.BASE_FILE_SPECS
        }

    def read_bytes(self, path: str) -> bytes:
        try:
            return self.payloads[path]
        except KeyError as error:
            raise FileNotFoundError(path) from error

    def build(self, tracked=()):
        return self.manifest.build_manifest(self.read_bytes, set(tracked))

    def test_manifest_entries_have_exact_contract_and_real_dual_checker(self):
        document = self.build()
        entries = document["files"]
        self.assertTrue(entries)
        for entry in entries:
            self.assertEqual(
                {"role", "path", "sha256", "mutability", "load_policy"},
                set(entry),
            )
            self.assertRegex(entry["sha256"], r"^[0-9a-f]{64}$")
            self.assertNotEqual("wiki/survey/current/manifest.json", entry["path"])
        dual = [
            entry
            for entry in entries
            if entry["role"] == "dual_platform_aggregate_checker"
        ]
        self.assertEqual(1, len(dual))
        self.assertEqual("scripts/survey/sf_dual_platform_check.py", dual[0]["path"])

    def test_manifest_expands_exactly_eight_sidecars(self):
        sidecars = [
            entry
            for entry in self.build()["files"]
            if entry["role"].startswith("schema_v3_sidecar:")
        ]
        self.assertEqual(8, len(sidecars))
        self.assertEqual(sorted(entry["path"] for entry in sidecars), [
            entry["path"] for entry in sidecars
        ])

    def test_release_and_prose_arrays_are_current_only(self):
        document = self.build()
        self.assertEqual(
            ["wiki/survey/current/tables/opening-guarantees.md"],
            document["release_bound_artifacts"],
        )
        self.assertEqual(
            [
                "wiki/survey/current/README.md",
                "wiki/survey/current/protocol.md",
                "wiki/survey/current/status.md",
                "wiki/survey/current/tables/opening-guarantees.md",
            ],
            document["prose_scan_paths"],
        )
        for path in (
            document["release_bound_artifacts"] + document["prose_scan_paths"]
        ):
            self.assertTrue(path.startswith("wiki/survey/current/"))
            self.assertNotRegex(path, r"amendment|review|response")

    def test_audit_pair_lifecycle_is_absent_complete_or_fail_closed(self):
        index = self.manifest.AUDIT_CAMPAIGN_INDEX_PATH
        correction = self.manifest.ACTIVE_REVIEW_TRANSACTION
        before = self.build()
        self.assertNotIn(index, [entry["path"] for entry in before["files"]])
        self.assertNotIn(correction, before["release_bound_artifacts"])

        for half in ({index}, {correction}):
            with self.assertRaisesRegex(
                self.manifest.CurrentManifestError,
                "audit-activation-incomplete",
            ):
                self.build(half)

        self.payloads[index] = b"audit index\n"
        self.payloads[correction] = b"correction\n"
        after = self.build({index, correction})
        paths = [entry["path"] for entry in after["files"]]
        self.assertIn(index, paths)
        self.assertIn(correction, paths)
        self.assertIn(correction, after["release_bound_artifacts"])
        self.assertIn(correction, after["prose_scan_paths"])

    def test_manifest_render_is_deterministic_canonical_and_timestamp_free(self):
        first = self.manifest.render_manifest(self.read_bytes, set())
        second = self.manifest.render_manifest(self.read_bytes, set())
        self.assertEqual(first, second)
        self.assertTrue(first.endswith(b"\n"))
        self.assertNotIn(b"generated_at", first)
        parsed = json.loads(first)
        self.assertEqual(parsed, self.build())
        self.assertEqual(first, (
            json.dumps(parsed, ensure_ascii=False, indent=2, allow_nan=False)
            + "\n"
        ).encode("utf-8"))

    def test_git_index_inventory_requires_stage_zero_entries(self):
        self.assertTrue(
            hasattr(self.manifest, "_parse_git_index"),
            "Git index parser is missing",
        )
        good = (
            b"100644 0123456789012345678901234567890123456789 0\t"
            b"wiki/audit/system-first-stage1a/INDEX.md\0"
        )
        self.assertEqual(
            {"wiki/audit/system-first-stage1a/INDEX.md"},
            self.manifest._parse_git_index(good),
        )
        bad = good.replace(b" 0\t", b" 1\t")
        with self.assertRaisesRegex(
            self.manifest.CurrentManifestError, "non-stage-0"
        ):
            self.manifest._parse_git_index(bad)

    def test_windows_worktree_gitdir_pointer_translates_for_wsl(self):
        self.assertTrue(
            hasattr(self.manifest, "_resolved_gitdir"),
            "worktree gitdir resolver is missing",
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            dot_git = Path(temp_dir) / ".git"
            dot_git.write_text(
                "gitdir: D:/repo/.git/worktrees/review\n", encoding="utf-8"
            )
            self.assertEqual(
                Path("/mnt/d/repo/.git/worktrees/review"),
                self.manifest._resolved_gitdir(dot_git, platform="posix"),
            )
            self.assertEqual(
                Path("D:/repo/.git/worktrees/review"),
                self.manifest._resolved_gitdir(dot_git, platform="nt"),
            )


class RouterContentContractTests(unittest.TestCase):
    def test_readme_is_short_and_contains_only_required_routing_content(self):
        path = CURRENT / "README.md"
        self.assertTrue(path.is_file(), f"missing router: {path}")
        raw = path.read_bytes()
        text = raw.decode("utf-8")
        self.assertLessEqual(len(raw), 4096)
        for required in (
            "Stage-1A",
            "status.md",
            "protocol.md",
            "manifest.json",
            "targeted",
            "wiki/audit/system-first-stage1a/INDEX.md",
            "Legacy files are not default context",
        ):
            self.assertIn(required, text)
        self.assertNotRegex(text, r"sf-protocol-amendment-\d+|gate-s1-v\d+-response")
        self.assertLessEqual(len(text.splitlines()), 14)

    def test_status_is_short_and_preserves_no_execution_boundary(self):
        path = CURRENT / "status.md"
        self.assertTrue(path.is_file(), f"missing status: {path}")
        raw = path.read_bytes()
        text = raw.decode("utf-8")
        self.assertLessEqual(len(raw), 4096)
        for required in (
            "Stage-1A",
            "owner authorization",
            "independent reviewer sign-off",
            "zero Stage-1B executions in this repair",
            REPORT_PATH,
            "PASS",
            "Current blockers",
            "Next action",
        ):
            self.assertIn(required, text)
        self.assertNotRegex(text, r"Stage-1B (?:has )?(?:begun|started|approved)")
        self.assertLessEqual(len(text.splitlines()), 16)


if __name__ == "__main__":
    unittest.main(verbosity=2)
