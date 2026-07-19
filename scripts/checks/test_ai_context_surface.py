#!/usr/bin/env python3
"""Contract tests for the AI context-surface and document-routing oracle."""

from __future__ import annotations

import hashlib
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath


sys.path.insert(0, str(Path(__file__).resolve().parent))

from ai_context_surface_check import classify_path, evaluate_manifest


def manifest(active, budgets=None, legacy=None, active_review=None):
    return {
        "schema": "ai-context-manifest-v1",
        "active_entries": active,
        "budgets_bytes": budgets or {},
        "legacy_cold_paths": legacy or [],
        "active_review_transaction": active_review,
    }


def raw_sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


class AiContextSurfaceTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.repo = Path(temporary.name)

    def write(self, relative_path: str, raw: bytes) -> None:
        path = self.repo.joinpath(*PurePosixPath(relative_path).parts)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)

    @staticmethod
    def active_entry(relative_path: str, raw: bytes, path_class: str) -> dict[str, str]:
        return {
            "path": relative_path,
            "class": path_class,
            "load_policy": "targeted",
            "purpose": "fixture",
            "sha256": raw_sha256(raw),
        }

    @staticmethod
    def failure_text(failures) -> str:
        return "\n".join(str(failure) for failure in failures)

    def assert_failure(self, failures, expected_code: str) -> None:
        self.assertIn(expected_code, self.failure_text(failures), failures)

    def test_one_hot_file_within_budget_passes(self) -> None:
        relative_path = "wiki/Project-Thesis.md"
        raw = b"# Project thesis\n"
        self.write(relative_path, raw)

        failures = evaluate_manifest(
            self.repo,
            manifest(
                [self.active_entry(relative_path, raw, "HOT")],
                budgets={relative_path: len(raw)},
            ),
            tracked_paths=[relative_path],
        )

        self.assertEqual([], failures)

    def test_thirty_one_active_entries_exceed_budget(self) -> None:
        active = []
        tracked_paths = []
        for index in range(31):
            relative_path = f"wiki/survey/current/item-{index:02d}.md"
            raw = f"item {index}\n".encode("utf-8")
            self.write(relative_path, raw)
            active.append(self.active_entry(relative_path, raw, "CURRENT"))
            tracked_paths.append(relative_path)

        failures = evaluate_manifest(
            self.repo,
            manifest(active),
            tracked_paths=tracked_paths,
        )

        self.assert_failure(failures, "active-entry-budget-exceeded")

    def test_archive_path_cannot_be_active(self) -> None:
        relative_path = "wiki/archive/working/campaign/old-note.md"
        raw = b"archived\n"
        self.write(relative_path, raw)

        failures = evaluate_manifest(
            self.repo,
            manifest([self.active_entry(relative_path, raw, "ARCHIVE")]),
            tracked_paths=[relative_path],
        )

        self.assert_failure(failures, "cold-path-on-active-surface")

    def test_oversized_file_fails_its_configured_budget(self) -> None:
        relative_path = "wiki/Research-Objective.md"
        raw = b"0123456789"
        self.write(relative_path, raw)

        failures = evaluate_manifest(
            self.repo,
            manifest(
                [self.active_entry(relative_path, raw, "HOT")],
                budgets={relative_path: len(raw) - 1},
            ),
            tracked_paths=[relative_path],
        )

        self.assert_failure(failures, "file-budget-exceeded")

    def test_hot_file_cannot_link_directly_to_audit_round(self) -> None:
        relative_path = "wiki/Research-Objective.md"
        raw = b"[review](wiki/audit/campaign/round-1/review.md)\n"
        self.write(relative_path, raw)

        failures = evaluate_manifest(
            self.repo,
            manifest([self.active_entry(relative_path, raw, "HOT")]),
            tracked_paths=[relative_path],
        )

        self.assert_failure(failures, "direct-audit-round-link")

    def test_hot_file_may_link_to_campaign_audit_index(self) -> None:
        relative_path = "wiki/Research-Objective.md"
        raw = b"[audit index](wiki/audit/campaign/INDEX.md)\n"
        self.write(relative_path, raw)

        failures = evaluate_manifest(
            self.repo,
            manifest([self.active_entry(relative_path, raw, "HOT")]),
            tracked_paths=[relative_path],
        )

        self.assertEqual([], failures)

    def test_new_review_artifact_outside_audit_root_fails(self) -> None:
        relative_path = "wiki/2026-07-19-stage1a-doctoral-review.md"
        self.write(relative_path, b"review\n")

        failures = evaluate_manifest(
            self.repo,
            manifest([]),
            tracked_paths=[relative_path],
        )

        self.assert_failure(failures, "new-audit-artifact-outside-audit-root")

    def test_legacy_review_artifact_passes_as_audit_legacy(self) -> None:
        relative_path = "wiki/2026-07-19-stage1a-doctoral-review.md"
        legacy = [{"path": relative_path, "class": "AUDIT_LEGACY"}]
        self.write(relative_path, b"review\n")

        self.assertEqual("AUDIT_LEGACY", classify_path(relative_path, legacy))
        failures = evaluate_manifest(
            self.repo,
            manifest([], legacy=legacy),
            tracked_paths=[relative_path],
        )

        self.assertEqual([], failures)

    def test_fourth_unconsolidated_amendment_is_forbidden(self) -> None:
        legacy = []
        tracked_paths = []
        for number in range(1, 4):
            relative_path = f"wiki/survey/campaign-protocol-amendment-{number}.md"
            self.write(relative_path, f"amendment {number}\n".encode("utf-8"))
            legacy.append({"path": relative_path, "class": "AUDIT_LEGACY"})
            tracked_paths.append(relative_path)

        fourth_path = "wiki/survey/campaign-protocol-amendment-4.md"
        self.write(fourth_path, b"amendment 4\n")
        tracked_paths.append(fourth_path)

        failures = evaluate_manifest(
            self.repo,
            manifest([], legacy=legacy),
            tracked_paths=tracked_paths,
        )

        self.assert_failure(failures, "unconsolidated-amendment-forbidden")

    def test_missing_active_path_fails(self) -> None:
        relative_path = "wiki/survey/current/status.md"
        expected_raw = b"expected status\n"

        failures = evaluate_manifest(
            self.repo,
            manifest([self.active_entry(relative_path, expected_raw, "CURRENT")]),
            tracked_paths=[relative_path],
        )

        self.assert_failure(failures, "active-path-missing")

    def test_active_hash_mismatch_fails(self) -> None:
        relative_path = "wiki/survey/current/status.md"
        self.write(relative_path, b"actual status\n")
        entry = self.active_entry(relative_path, b"expected status\n", "CURRENT")

        failures = evaluate_manifest(
            self.repo,
            manifest([entry]),
            tracked_paths=[relative_path],
        )

        self.assert_failure(failures, "active-hash-mismatch")


if __name__ == "__main__":
    unittest.main()
