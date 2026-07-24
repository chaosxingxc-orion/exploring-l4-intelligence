#!/usr/bin/env python3
"""Contract tests for the AI context-surface and document-routing oracle."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path, PurePosixPath
from urllib.parse import quote
from unittest import mock


sys.path.insert(0, str(Path(__file__).resolve().parent))

from ai_context_surface_check import (
    ContextSurfaceError,
    TrustedRepoReader,
    _git_tracked_paths,
    classify_path,
    evaluate_manifest,
    load_json_strict,
    normalize_agent_guide,
)
import build_ai_context_manifest as builder
import ai_context_surface_check as surface


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


def git_blob_id(raw: bytes) -> str:
    header = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(header + raw).hexdigest()


def failure_code(failure) -> str:
    if isinstance(failure, str):
        return failure.split(":", 1)[0].strip()
    if isinstance(failure, dict) and "code" in failure:
        return str(failure["code"])
    code = getattr(failure, "code", None)
    if code is not None:
        return str(code)
    raise AssertionError(f"failure has no structured code: {failure!r}")


def failure_codes(failures) -> list[str]:
    return [failure_code(failure) for failure in failures]


EXPECTED_ARCHIVE_TRANSITIONS = (
    (
        "wiki/survey/2026-07-18-sf-protocol-amendment-9.md",
        "wiki/archive/working/system-first-stage1a/amendments/"
        "2026-07-18-sf-protocol-amendment-9.md",
        "c786137a5628d963156229b6407cb8eb955e3a4c",
    ),
    (
        "wiki/survey/2026-07-18-sf-protocol-amendment-10.md",
        "wiki/archive/working/system-first-stage1a/amendments/"
        "2026-07-18-sf-protocol-amendment-10.md",
        "8c6df6a092e327b2327242a1b2a47ad4f6b941e2",
    ),
    (
        "wiki/survey/2026-07-18-sf-protocol-amendment-11.md",
        "wiki/archive/working/system-first-stage1a/amendments/"
        "2026-07-18-sf-protocol-amendment-11.md",
        "31c714d582f6188440da4397df05d6950aa9ba33",
    ),
    (
        "wiki/survey/2026-07-18-sf-protocol-amendment-12.md",
        "wiki/archive/working/system-first-stage1a/amendments/"
        "2026-07-18-sf-protocol-amendment-12.md",
        "73c96fc47c05941d76532b3e46fa47b659004cf5",
    ),
    (
        "wiki/survey/2026-07-19-sf-protocol-amendment-13.md",
        "wiki/archive/working/system-first-stage1a/amendments/"
        "2026-07-19-sf-protocol-amendment-13.md",
        "126c4dc93d1f323ba0ca5e9d3de86cc44e513045",
    ),
    (
        "wiki/survey/2026-07-19-sf-protocol-amendment-14.md",
        "wiki/archive/working/system-first-stage1a/amendments/"
        "2026-07-19-sf-protocol-amendment-14.md",
        "f4c4f6490e8cc03d9103e7c4d212cd5d1dd61834",
    ),
    (
        "wiki/survey/2026-07-19-sf-protocol-amendment-15.md",
        "wiki/archive/working/system-first-stage1a/amendments/"
        "2026-07-19-sf-protocol-amendment-15.md",
        "5586d6f840927f975e18a500cef74a11d9e3a48a",
    ),
)

INTEGRATION_EVIDENCE_PATHS = (
    "docs/checks/system-first-stage1a/context-v1/wiki-sync-dry-run-incident.json",
)
SELF_REFERENTIAL_PACKAGE_REPORT = (
    "docs/checks/system-first-stage1a/context-v1/current-package-check.json"
)


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

    def assert_failure(self, failures, expected_code: str) -> None:
        self.assertIn(expected_code, failure_codes(failures), failures)

    def test_failure_codes_do_not_match_by_substring(self) -> None:
        failures = ["not-active-hash-mismatch-disabled: fixture"]

        self.assertNotIn("active-hash-mismatch", failure_codes(failures))

    def test_one_hot_file_within_budget_passes(self) -> None:
        relative_path = "wiki/Project-Thesis.md"
        raw = "# 项目论文\r\n".encode("utf-8")
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

    def test_thirty_active_entries_are_within_budget(self) -> None:
        active = []
        tracked_paths = []
        for index in range(30):
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

    def test_integration_evidence_is_exact_hot_targeted_and_hash_checked(self) -> None:
        for relative_path in INTEGRATION_EVIDENCE_PATHS:
            with self.subTest(path=relative_path, condition="classification"):
                self.assertEqual("HOT", classify_path(relative_path, []))

            expected_raw = b"expected evidence\n"
            entry = self.active_entry(relative_path, expected_raw, "HOT")
            failures = evaluate_manifest(
                self.repo,
                manifest([entry]),
                tracked_paths=[relative_path],
            )
            self.assert_failure(failures, "active-path-missing")

            self.write(relative_path, b"different evidence\n")
            failures = evaluate_manifest(
                self.repo,
                manifest([entry]),
                tracked_paths=[relative_path],
            )
            self.assert_failure(failures, "active-hash-mismatch")

    def test_classification_precedence_is_exact(self) -> None:
        legacy = [
            {"path": "wiki/survey/current/legacy.md", "class": "REGISTRY_LEGACY"},
            {"path": "wiki/old-review.md", "class": "AUDIT_LEGACY"},
        ]

        self.assertEqual("HOT", classify_path("wiki/Project-Thesis.md", legacy))
        self.assertEqual("CURRENT", classify_path("wiki/survey/current/legacy.md", legacy))
        self.assertEqual("REGISTRY", classify_path("wiki/survey/sidecars/a.json", legacy))
        self.assertEqual("AUDIT", classify_path("wiki/audit/campaign/round/review.md", legacy))
        self.assertEqual("ARCHIVE", classify_path("wiki/archive/review.md", legacy))
        self.assertEqual("WORKBENCH", classify_path("wiki/survey/workbench/x/note.md", legacy))
        self.assertEqual("AUDIT_LEGACY", classify_path("wiki/old-review.md", legacy))
        self.assertEqual("UNCLASSIFIED", classify_path("docs/ordinary.md", legacy))

    def test_paths_must_be_canonical_repo_relative_posix(self) -> None:
        invalid_paths = [
            "",
            ".",
            "../escape.md",
            "wiki/../escape.md",
            "/wiki/Research-Objective.md",
            "C:/wiki/Research-Objective.md",
            r"wiki\Research-Objective.md",
        ]
        for invalid_path in invalid_paths:
            with self.subTest(path=invalid_path):
                failures = evaluate_manifest(
                    self.repo,
                    manifest([]),
                    tracked_paths=[invalid_path],
                )
                self.assert_failure(failures, "invalid-path")

    def test_duplicate_tracked_and_manifest_paths_fail(self) -> None:
        relative_path = "wiki/Project-Thesis.md"
        raw = b"thesis\n"
        self.write(relative_path, raw)
        entry = self.active_entry(relative_path, raw, "HOT")

        tracked_failures = evaluate_manifest(
            self.repo,
            manifest([entry]),
            tracked_paths=[relative_path, relative_path],
        )
        entry_failures = evaluate_manifest(
            self.repo,
            manifest([entry, dict(entry)]),
            tracked_paths=[relative_path],
        )

        self.assert_failure(tracked_failures, "duplicate-path")
        self.assert_failure(entry_failures, "duplicate-path")

    def test_tracked_inventory_is_authoritative_for_all_manifest_surfaces(self) -> None:
        active_path = "wiki/Project-Thesis.md"
        legacy_path = "wiki/old-review.md"
        review_path = "wiki/audit/campaign/round-12/correction.md"
        active_raw = b"thesis\n"
        self.write(active_path, active_raw)
        self.write(legacy_path, b"legacy\n")
        self.write(review_path, b"review\n")
        failures = evaluate_manifest(
            self.repo,
            manifest(
                [self.active_entry(active_path, active_raw, "HOT")],
                budgets={active_path: 1024},
                legacy=[{"path": legacy_path, "class": "AUDIT_LEGACY"}],
                active_review=review_path,
            ),
            tracked_paths=[],
        )

        self.assert_failure(failures, "active-path-untracked")
        self.assert_failure(failures, "legacy-path-untracked")
        self.assert_failure(failures, "budget-path-untracked")
        self.assert_failure(failures, "active-review-transaction-untracked")

    def test_legacy_class_cannot_be_forged_and_active_cannot_overlap_legacy(self) -> None:
        forged_path = "wiki/old-review.md"
        self.write(forged_path, b"legacy\n")
        forged = evaluate_manifest(
            self.repo,
            manifest(
                [],
                legacy=[{"path": forged_path, "class": "REGISTRY_LEGACY"}],
            ),
            tracked_paths=[forged_path],
        )
        self.assert_failure(forged, "legacy-class-mismatch")

        overlap_path = "wiki/Project-Thesis.md"
        raw = b"thesis\n"
        self.write(overlap_path, raw)
        overlap = evaluate_manifest(
            self.repo,
            manifest(
                [self.active_entry(overlap_path, raw, "HOT")],
                legacy=[{"path": overlap_path, "class": "REGISTRY_LEGACY"}],
            ),
            tracked_paths=[overlap_path],
        )
        self.assert_failure(overlap, "active-legacy-overlap")

    def test_unclassified_tracked_wiki_markdown_fails(self) -> None:
        path = "wiki/future-working-note.md"
        self.write(path, b"future\n")

        failures = evaluate_manifest(self.repo, manifest([]), tracked_paths=[path])

        self.assert_failure(failures, "unclassified-persistent-document")

    def test_trusted_reader_rejects_mocked_windows_symlink_leaf(self) -> None:
        path = "wiki/Project-Thesis.md"
        self.write(path, b"thesis\n")
        real_lstat = os.lstat

        def mocked_lstat(candidate):
            if Path(candidate).name == "Project-Thesis.md":
                return mock.Mock(st_mode=stat.S_IFLNK)
            return real_lstat(candidate)

        with mock.patch(
            "ai_context_surface_check.os.lstat", side_effect=mocked_lstat
        ), self.assertRaises(ContextSurfaceError) as raised:
            TrustedRepoReader(self.repo).read_bytes(path)

        self.assertIn("untrusted-repo-path", str(raised.exception))

    @unittest.skipIf(os.name == "nt", "real symlink attack runs in WSL/POSIX")
    def test_trusted_reader_rejects_real_leaf_and_ancestor_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as outside_name:
            outside = Path(outside_name)
            outside_file = outside / "outside.md"
            outside_file.write_bytes(b"outside\n")
            (self.repo / "wiki").mkdir()
            os.symlink(outside_file, self.repo / "wiki/Project-Thesis.md")
            with self.assertRaises(ContextSurfaceError) as leaf:
                TrustedRepoReader(self.repo).read_bytes("wiki/Project-Thesis.md")
            self.assertIn("untrusted-repo-path", str(leaf.exception))

        with tempfile.TemporaryDirectory() as repo_name, tempfile.TemporaryDirectory() as outside_name:
            repo = Path(repo_name)
            outside = Path(outside_name)
            (outside / "wiki").mkdir()
            (outside / "wiki/Project-Thesis.md").write_bytes(b"outside\n")
            os.symlink(outside / "wiki", repo / "wiki")
            with self.assertRaises(ContextSurfaceError) as ancestor:
                TrustedRepoReader(repo).read_bytes("wiki/Project-Thesis.md")
            self.assertIn("untrusted-repo-path", str(ancestor.exception))

    def test_manifest_schema_and_entry_keys_are_strict(self) -> None:
        relative_path = "wiki/Project-Thesis.md"
        raw = b"thesis\n"
        self.write(relative_path, raw)
        entry = self.active_entry(relative_path, raw, "HOT")
        entry["surprise"] = "not allowed"
        bad_manifest = manifest([entry])
        bad_manifest["surprise"] = []

        failures = evaluate_manifest(
            self.repo,
            bad_manifest,
            tracked_paths=[relative_path],
        )

        self.assert_failure(failures, "manifest-schema-invalid")
        self.assert_failure(failures, "manifest-entry-invalid")

    def test_declared_class_and_load_policy_are_enforced(self) -> None:
        relative_path = "wiki/Project-Thesis.md"
        raw = b"thesis\n"
        self.write(relative_path, raw)
        wrong_class = self.active_entry(relative_path, raw, "CURRENT")
        wrong_policy = self.active_entry(relative_path, raw, "HOT")
        wrong_policy["load_policy"] = "sometimes"

        class_failures = evaluate_manifest(
            self.repo, manifest([wrong_class]), tracked_paths=[relative_path]
        )
        policy_failures = evaluate_manifest(
            self.repo, manifest([wrong_policy]), tracked_paths=[relative_path]
        )

        self.assert_failure(class_failures, "active-class-mismatch")
        self.assert_failure(policy_failures, "manifest-entry-invalid")

    def test_unhashable_manifest_values_fail_closed(self) -> None:
        relative_path = "wiki/Project-Thesis.md"
        raw = b"thesis\n"
        self.write(relative_path, raw)
        entry = self.active_entry(relative_path, raw, "HOT")
        entry["class"] = []
        entry["load_policy"] = []

        failures = evaluate_manifest(
            self.repo,
            manifest([entry]),
            tracked_paths=[relative_path],
        )

        self.assert_failure(failures, "manifest-entry-invalid")
        self.assert_failure(failures, "active-class-mismatch")

    def test_only_manifest_self_metadata_may_omit_sha256(self) -> None:
        relative_path = "wiki/Project-Thesis.md"
        raw = b"thesis\n"
        self.write(relative_path, raw)
        missing_hash = self.active_entry(relative_path, raw, "HOT")
        del missing_hash["sha256"]

        failures = evaluate_manifest(
            self.repo,
            manifest([missing_hash]),
            tracked_paths=[relative_path],
        )

        self.assert_failure(failures, "manifest-entry-invalid")

    def test_manifest_self_metadata_may_omit_sha256(self) -> None:
        relative_path = "docs/integrity/ai-context-manifest.json"
        raw = b"{}\n"
        self.write(relative_path, raw)
        entry = {
            "path": relative_path,
            "class": "HOT",
            "load_policy": "targeted",
            "purpose": "self metadata",
        }

        failures = evaluate_manifest(
            self.repo,
            manifest([entry]),
            tracked_paths=[relative_path],
        )

        self.assertEqual([], failures)

    def test_strict_json_rejects_duplicates_nonfinite_utf8_and_trailing_data(self) -> None:
        path = self.repo / "manifest.json"
        invalid_documents = {
            "duplicate": b'{"schema": 1, "schema": 2}',
            "nonfinite": b'{"value": NaN}',
            "utf8": b'\xff',
            "trailing": b'{} trailing',
        }
        for label, raw in invalid_documents.items():
            with self.subTest(label=label):
                path.write_bytes(raw)
                with self.assertRaises(ContextSurfaceError) as raised:
                    load_json_strict(path)
                self.assertIn("manifest-json-invalid:", str(raised.exception))

    def test_relative_and_anchored_audit_links_are_normalized(self) -> None:
        relative_path = "wiki/survey/current/status.md"
        raw = (
            b"[review](../../audit/campaign/round-1/review.md#verdict)\n"
        )
        self.write(relative_path, raw)

        failures = evaluate_manifest(
            self.repo,
            manifest([self.active_entry(relative_path, raw, "CURRENT")]),
            tracked_paths=[relative_path],
        )

        self.assert_failure(failures, "direct-audit-round-link")

    def test_exact_active_review_transaction_is_the_only_round_exception(self) -> None:
        relative_path = "wiki/survey/current/status.md"
        active_review = (
            "wiki/audit/system-first-stage1a/round-12/"
            "stage1a-readiness-correction.md"
        )
        raw = (
            b"[correction](../../audit/system-first-stage1a/round-12/"
            b"stage1a-readiness-correction.md#result)\n"
        )
        self.write(relative_path, raw)
        self.write(active_review, b"correction\n")

        failures = evaluate_manifest(
            self.repo,
            manifest(
                [self.active_entry(relative_path, raw, "CURRENT")],
                active_review=active_review,
            ),
            tracked_paths=[relative_path, active_review],
        )

        self.assertEqual([], failures)

    def test_active_review_pointer_does_not_create_a_new_unnumbered_exception(self) -> None:
        path = "wiki/audit/campaign/round-12/correction.md"
        self.write(path, b"correction\n")

        failures = evaluate_manifest(
            self.repo,
            manifest([], active_review=path),
            tracked_paths=[path],
        )

        self.assert_failure(failures, "audit-epoch-state-invalid")

    def test_percent_encoded_relative_audit_link_cannot_bypass_routing(self) -> None:
        relative_path = "wiki/survey/current/status.md"
        raw = b"[review](..%2F..%2Faudit%2Fcampaign%2Fround-1%2Freview.md)\n"
        self.write(relative_path, raw)

        failures = evaluate_manifest(
            self.repo,
            manifest([self.active_entry(relative_path, raw, "CURRENT")]),
            tracked_paths=[relative_path],
        )

        self.assert_failure(failures, "direct-audit-round-link")

    def test_reference_style_audit_round_link_is_rejected_case_insensitively(self) -> None:
        relative_path = "wiki/Research-Objective.md"
        raw = (
            b"See [review][R].\n\n"
            b"[r]: wiki/audit/campaign/round-1/review.md\n"
        )
        self.write(relative_path, raw)

        failures = evaluate_manifest(
            self.repo,
            manifest([self.active_entry(relative_path, raw, "HOT")]),
            tracked_paths=[relative_path],
        )

        self.assert_failure(failures, "direct-audit-round-link")

    def test_unused_reference_definition_is_scanned_fail_closed(self) -> None:
        relative_path = "wiki/Research-Objective.md"
        raw = b"[future review]: <wiki/audit/campaign/round-1/review.md>\n"
        self.write(relative_path, raw)

        failures = evaluate_manifest(
            self.repo,
            manifest([self.active_entry(relative_path, raw, "HOT")]),
            tracked_paths=[relative_path],
        )

        self.assert_failure(failures, "direct-audit-round-link")

    def test_collapsed_reference_to_campaign_index_passes(self) -> None:
        relative_path = "wiki/Research-Objective.md"
        raw = (
            b"See [audit index][].\n\n"
            b"[audit index]: <wiki/audit/campaign/INDEX.md#round-12>\n"
        )
        self.write(relative_path, raw)

        failures = evaluate_manifest(
            self.repo,
            manifest([self.active_entry(relative_path, raw, "HOT")]),
            tracked_paths=[relative_path],
        )

        self.assertEqual([], failures)

    def test_reference_to_exact_active_review_transaction_passes(self) -> None:
        relative_path = "wiki/survey/current/status.md"
        active_review = (
            "wiki/audit/system-first-stage1a/round-12/"
            "stage1a-readiness-correction.md"
        )
        raw = (
            b"See [correction][ROUND].\n\n"
            b"[round]: <../../audit/system-first-stage1a/round-12/"
            b"stage1a-readiness-correction.md#result>\n"
        )
        self.write(relative_path, raw)
        self.write(active_review, b"correction\n")

        failures = evaluate_manifest(
            self.repo,
            manifest(
                [self.active_entry(relative_path, raw, "CURRENT")],
                active_review=active_review,
            ),
            tracked_paths=[relative_path, active_review],
        )

        self.assertEqual([], failures)

    def test_percent_encoded_reference_destination_cannot_bypass_routing(self) -> None:
        relative_path = "wiki/survey/current/status.md"
        raw = (
            b"See [review][r].\n\n"
            b"[r]: ..%2F..%2Faudit%2Fcampaign%2Fround-1%2Freview.md\n"
        )
        self.write(relative_path, raw)

        failures = evaluate_manifest(
            self.repo,
            manifest([self.active_entry(relative_path, raw, "CURRENT")]),
            tracked_paths=[relative_path],
        )

        self.assert_failure(failures, "direct-audit-round-link")

    def test_footnote_and_fenced_reference_examples_are_not_links(self) -> None:
        relative_path = "wiki/Research-Objective.md"
        raw = (
            b"A note.[^1]\n\n"
            b"[^1]: wiki/audit/campaign/round-1/review.md\n\n"
            b"```markdown\n"
            b"[example]: wiki/audit/campaign/round-1/review.md\n"
            b"```\n"
        )
        self.write(relative_path, raw)

        failures = evaluate_manifest(
            self.repo,
            manifest([self.active_entry(relative_path, raw, "HOT")]),
            tracked_paths=[relative_path],
        )

        self.assertEqual([], failures)

    def test_inline_links_inside_all_markdown_code_forms_are_ignored(self) -> None:
        relative_path = "wiki/Research-Objective.md"
        raw = (
            b"```markdown\n"
            b"[fenced](wiki/audit/campaign/round-1/review.md)\n"
            b"```\n\n"
            b"   ~~~~\n"
            b"[tilde](wiki/audit/campaign/round-1/review.md)\n"
            b"   ~~~~\n\n"
            b"    [indented](wiki/audit/campaign/round-1/review.md)\n"
            b"\t[tabbed](wiki/audit/campaign/round-1/review.md)\n\n"
            b"`[inline](wiki/audit/campaign/round-1/review.md)`\n"
            b"``literal ` [multi](wiki/audit/campaign/round-1/review.md) ` content``\n"
        )
        self.write(relative_path, raw)

        failures = evaluate_manifest(
            self.repo,
            manifest([self.active_entry(relative_path, raw, "HOT")]),
            tracked_paths=[relative_path],
        )

        self.assertEqual([], failures)

    def test_reference_definitions_inside_code_are_ignored(self) -> None:
        relative_path = "wiki/Research-Objective.md"
        raw = (
            b"~~~markdown\n"
            b"[fenced]: wiki/audit/campaign/round-1/review.md\n"
            b"~~~\n"
            b"    [indented]: wiki/audit/campaign/round-1/review.md\n"
            b"``[inline]: wiki/audit/campaign/round-1/review.md``\n"
        )
        self.write(relative_path, raw)

        failures = evaluate_manifest(
            self.repo,
            manifest([self.active_entry(relative_path, raw, "HOT")]),
            tracked_paths=[relative_path],
        )

        self.assertEqual([], failures)

    def test_multiline_reference_destination_to_audit_round_is_rejected(self) -> None:
        relative_path = "wiki/Research-Objective.md"
        raw = (
            b"See [review][r].\n\n"
            b"[r]:\n"
            b"  <wiki/audit/campaign/round-1/review.md>\n"
        )
        self.write(relative_path, raw)

        failures = evaluate_manifest(
            self.repo,
            manifest([self.active_entry(relative_path, raw, "HOT")]),
            tracked_paths=[relative_path],
        )

        self.assert_failure(failures, "direct-audit-round-link")

    def test_multiline_reference_destination_to_campaign_index_passes(self) -> None:
        relative_path = "wiki/Research-Objective.md"
        raw = (
            b"See [index][r].\n\n"
            b"[r]:\n"
            b"  wiki/audit/campaign/INDEX.md#round-12\n"
        )
        self.write(relative_path, raw)

        failures = evaluate_manifest(
            self.repo,
            manifest([self.active_entry(relative_path, raw, "HOT")]),
            tracked_paths=[relative_path],
        )

        self.assertEqual([], failures)

    def test_multiline_reference_destination_to_active_review_passes(self) -> None:
        relative_path = "wiki/survey/current/status.md"
        active_review = (
            "wiki/audit/system-first-stage1a/round-12/"
            "stage1a-readiness-correction.md"
        )
        raw = (
            b"See [correction][r].\n\n"
            b"[r]:\n"
            b"  <../../audit/system-first-stage1a/round-12/"
            b"stage1a-readiness-correction.md#result>\n"
        )
        self.write(relative_path, raw)
        self.write(active_review, b"correction\n")

        failures = evaluate_manifest(
            self.repo,
            manifest(
                [self.active_entry(relative_path, raw, "CURRENT")],
                active_review=active_review,
            ),
            tracked_paths=[relative_path, active_review],
        )

        self.assertEqual([], failures)

    def test_image_html_and_raw_url_audit_destinations_are_rejected(self) -> None:
        relative_path = "wiki/Research-Objective.md"
        raw = (
            b"![image](wiki/audit/campaign/round-1/image.png)\n"
            b"<a href=\"/wiki/audit/campaign/round-1/review.md\">review</a>\n"
            b"<img src='https://example.test/wiki/audit/campaign/round-1/image.png'>\n"
            b"https://example.test/wiki/audit/campaign/round-1/review.md\n"
        )
        self.write(relative_path, raw)

        failures = evaluate_manifest(
            self.repo,
            manifest([self.active_entry(relative_path, raw, "HOT")]),
            tracked_paths=[relative_path],
        )

        self.assertEqual(4, failure_codes(failures).count("direct-audit-round-link"))

    def test_double_encoded_audit_destination_is_rejected(self) -> None:
        relative_path = "wiki/Research-Objective.md"
        raw = b"[review](wiki%252Faudit%252Fcampaign%252Fround-1%252Freview.md)\n"
        self.write(relative_path, raw)

        failures = evaluate_manifest(
            self.repo,
            manifest([self.active_entry(relative_path, raw, "HOT")]),
            tracked_paths=[relative_path],
        )

        self.assert_failure(failures, "direct-audit-round-link")

    def test_residual_or_invalid_percent_encoding_fails_closed(self) -> None:
        relative_path = "wiki/Research-Objective.md"
        target = "wiki/audit/campaign/round-1/review.md"
        for _ in range(6):
            target = quote(target, safe="")
        raw = f"[review]({target})\n[bad](wiki/%FF.md)\n".encode("ascii")
        self.write(relative_path, raw)

        failures = evaluate_manifest(
            self.repo,
            manifest([self.active_entry(relative_path, raw, "HOT")]),
            tracked_paths=[relative_path],
        )

        self.assertEqual(2, failure_codes(failures).count("invalid-link-path"))

    def test_external_absolute_urls_outside_wiki_are_ignored(self) -> None:
        relative_path = "wiki/Research-Objective.md"
        raw = (
            b"[paper](https://arxiv.org/abs/2501.00001)\n"
            b"https://example.test/project/wiki/Research-Objective\n"
        )
        self.write(relative_path, raw)

        failures = evaluate_manifest(
            self.repo,
            manifest([self.active_entry(relative_path, raw, "HOT")]),
            tracked_paths=[relative_path],
        )

        self.assertEqual([], failures)

    def test_html_comments_pre_and_backticks_are_masked_but_inline_code_is_parsed(self) -> None:
        relative_path = "wiki/Research-Objective.md"
        raw = (
            b"<!-- [comment](wiki/audit/campaign/round-1/review.md) -->\n"
            b"<pre><a href='/wiki/audit/campaign/round-1/review.md'>x</a></pre>\n"
            b"`[backtick](wiki/audit/campaign/round-1/review.md)`\n"
            b"<code>[parsed](wiki/audit/campaign/round-1/review.md)</code>\n"
        )
        self.write(relative_path, raw)

        failures = evaluate_manifest(
            self.repo,
            manifest([self.active_entry(relative_path, raw, "HOT")]),
            tracked_paths=[relative_path],
        )

        self.assertEqual(1, failure_codes(failures).count("direct-audit-round-link"))

    def test_nested_absolute_audit_urls_fail_in_markdown_raw_and_html(self) -> None:
        relative_path = "wiki/Research-Objective.md"
        base = "https://github.example/repo/blob/master/wiki/audit/campaign/round-1/review.md"
        raw = (
            f"[markdown]({base})\n"
            f"{base}\n"
            f"<a href='{base}'>html</a>\n"
            "https://example.test/docs/wiki-audit-overview\n"
            f"`{base}`\n"
            f"<pre>{base}</pre>\n"
        ).encode("utf-8")
        self.write(relative_path, raw)

        failures = evaluate_manifest(
            self.repo,
            manifest([self.active_entry(relative_path, raw, "HOT")]),
            tracked_paths=[relative_path],
        )

        self.assertEqual(3, failure_codes(failures).count("direct-audit-round-link"))

    def test_four_space_list_continuation_is_not_masked_as_code(self) -> None:
        relative_path = "wiki/Research-Objective.md"
        raw = (
            b"- current pointer\n"
            b"    [review](wiki/audit/campaign/round-1/review.md)\n"
        )
        self.write(relative_path, raw)

        failures = evaluate_manifest(
            self.repo,
            manifest([self.active_entry(relative_path, raw, "HOT")]),
            tracked_paths=[relative_path],
        )

        self.assert_failure(failures, "direct-audit-round-link")

    def test_review_name_cannot_escape_with_case_or_percent_encoding(self) -> None:
        paths = [
            "wiki/New-Doctoral-REVIEW.md",
            "wiki/new-response.md",
            "wiki/new-proposal.md",
        ]
        for path in paths:
            self.write(path, b"audit\n")

        failures = evaluate_manifest(self.repo, manifest([]), tracked_paths=paths)

        self.assertEqual(
            3,
            failure_codes(failures).count("new-audit-artifact-outside-audit-root"),
            failures,
        )

    def test_expanded_audit_transaction_names_require_audit_root(self) -> None:
        names = [
            "reviewer-submission",
            "reviewer-report",
            "correction",
            "sign-off",
            "adjudication",
            "release-decision",
        ]
        paths = [f"wiki/2026-07-19-{name}.md" for name in names]
        for path in paths:
            self.write(path, b"audit\n")

        failures = evaluate_manifest(self.repo, manifest([]), tracked_paths=paths)

        self.assertEqual(
            len(paths),
            failure_codes(failures).count("new-audit-artifact-outside-audit-root"),
        )

    def test_amendment_number_controls_only_the_consolidation_failure(self) -> None:
        first = "wiki/campaign-protocol-amendment-1.md"
        fourth = "wiki/campaign-protocol-amendment-4.md"
        self.write(first, b"first\n")
        self.write(fourth, b"fourth\n")

        failures = evaluate_manifest(
            self.repo, manifest([]), tracked_paths=[first, fourth]
        )
        codes = failure_codes(failures)

        self.assertEqual(2, codes.count("new-audit-artifact-outside-audit-root"))
        self.assertEqual(1, codes.count("unconsolidated-amendment-forbidden"))

    def test_fourth_numbered_amendment_is_forbidden_inside_audit_root(self) -> None:
        path = "wiki/audit/campaign/round-4/protocol-amendment-4.md"
        self.write(path, b"amendment\n")

        failures = evaluate_manifest(self.repo, manifest([]), tracked_paths=[path])

        self.assert_failure(failures, "unconsolidated-amendment-forbidden")

    def test_fourth_numbered_correction_is_forbidden_inside_audit_root(self) -> None:
        path = "wiki/audit/campaign/epoch-2/round-4/protocol-correction-4.md"
        self.write(path, b"correction\n")

        failures = evaluate_manifest(self.repo, manifest([]), tracked_paths=[path])

        self.assert_failure(failures, "unconsolidated-amendment-forbidden")

    def epoch_fixture(
        self,
        *,
        path_epoch: int = 2,
        receipt_epoch: int = 2,
        receipt_version: int = 2,
        forged_hash: bool = False,
    ) -> tuple[str, list[str]]:
        spec_path = "wiki/survey/current/protocol.md"
        spec_raw = (
            "---\nprotocol_id: TEST\nprotocol_version: 2\n---\n\n# Effective spec\n"
        ).encode("utf-8")
        artifact = (
            f"wiki/audit/campaign/epoch-{path_epoch}/round-1/"
            "protocol-amendment-1.md"
        )
        receipt = (
            f"wiki/audit/campaign/epoch-{path_epoch}/consolidation-receipt.json"
        )
        receipt_document = {
            "schema": "ai-context-consolidation-receipt-v1",
            "campaign": "campaign",
            "epoch": receipt_epoch,
            "effective_spec": spec_path,
            "effective_spec_version": receipt_version,
            "effective_spec_sha256": "0" * 64 if forged_hash else raw_sha256(spec_raw),
        }
        self.write(spec_path, spec_raw)
        self.write(artifact, b"amendment 1 after consolidation\n")
        self.write(
            receipt,
            (json.dumps(receipt_document, sort_keys=True) + "\n").encode("utf-8"),
        )
        return artifact, [artifact, receipt, spec_path]

    def test_first_numbered_amendment_in_receipted_next_epoch_passes(self) -> None:
        _artifact, tracked = self.epoch_fixture()

        failures = evaluate_manifest(self.repo, manifest([]), tracked_paths=tracked)

        self.assertEqual([], failures)

    def test_forged_epoch_receipt_or_effective_spec_binding_fails(self) -> None:
        mutations = {
            "epoch": {"receipt_epoch": 3},
            "version": {"receipt_version": 3},
            "sha256": {"forged_hash": True},
        }
        for label, mutation in mutations.items():
            with self.subTest(label=label):
                _artifact, tracked = self.epoch_fixture(**mutation)
                failures = evaluate_manifest(
                    self.repo, manifest([]), tracked_paths=tracked
                )
                self.assert_failure(failures, "consolidation-epoch-invalid")

    @staticmethod
    def iteration_raw(
        *,
        campaign: str,
        epoch: int,
        ordinal: int,
        kind: str,
        spec_path: str,
        spec_version: int,
        spec_sha256: str,
    ) -> bytes:
        return (
            "---\n"
            "schema: ai-context-audit-iteration-v1\n"
            f"campaign: {campaign}\n"
            f"epoch: {epoch}\n"
            f"ordinal: {ordinal}\n"
            f"kind: {kind}\n"
            f"effective_spec: {spec_path}\n"
            f"effective_spec_version: {spec_version}\n"
            f"effective_spec_sha256: {spec_sha256}\n"
            "---\n\n"
            "# Registered audit iteration\n"
        ).encode("utf-8")

    def registered_epoch_state(
        self,
        layout=((1, (1, 2)), (2, (1,))),
        *,
        campaign: str = "campaign",
    ):
        spec_path = "wiki/survey/current/protocol.md"
        spec_raw = (
            "---\nprotocol_id: TEST\nprotocol_version: 2\n---\n\n"
            "# Effective protocol\n"
        ).encode("utf-8")
        spec_sha = raw_sha256(spec_raw)
        docs = {spec_path: spec_raw}
        for epoch, ordinals in layout:
            receipt_path = (
                f"wiki/audit/{campaign}/epoch-{epoch}/consolidation-receipt.json"
            )
            receipt = {
                "schema": "ai-context-consolidation-receipt-v1",
                "campaign": campaign,
                "epoch": epoch,
                "effective_spec": spec_path,
                "effective_spec_version": 2,
                "effective_spec_sha256": spec_sha,
            }
            docs[receipt_path] = (
                json.dumps(receipt, sort_keys=True) + "\n"
            ).encode("utf-8")
            for ordinal in ordinals:
                path = (
                    f"wiki/audit/{campaign}/epoch-{epoch}/round-{ordinal}/"
                    f"protocol-amendment-{ordinal}.md"
                )
                docs[path] = self.iteration_raw(
                    campaign=campaign,
                    epoch=epoch,
                    ordinal=ordinal,
                    kind="amendment",
                    spec_path=spec_path,
                    spec_version=2,
                    spec_sha256=spec_sha,
                )
        registered = {
            path: git_blob_id(raw)
            for path, raw in docs.items()
            if path.startswith("wiki/audit/")
        }
        document = manifest(
            [self.active_entry(spec_path, spec_raw, "CURRENT")]
        )
        return document, sorted(docs), registered, docs

    def validate_epoch_state(self, document, tracked, registered, docs):
        return surface.validate_audit_epoch_state(
            document,
            tracked,
            registered,
            lambda path: docs.get(path),
        )

    def test_registered_epoch_state_machine_accepts_contiguous_chain(self) -> None:
        document, tracked, registered, docs = self.registered_epoch_state()

        failures = self.validate_epoch_state(document, tracked, registered, docs)

        self.assertEqual([], failures)

    def test_epoch_state_machine_allows_early_consolidation_before_ordinal_three(self) -> None:
        document, tracked, registered, docs = self.registered_epoch_state(
            layout=((1, (1,)), (2, (1,)))
        )

        failures = self.validate_epoch_state(document, tracked, registered, docs)

        self.assertEqual([], failures)

    def test_epoch_state_machine_rejects_unnumbered_duplicate_gap_and_fourth(self) -> None:
        cases = {
            "gap": ((1, (1, 3)),),
            "fourth": ((1, (1, 2, 3, 4)),),
        }
        for label, layout in cases.items():
            with self.subTest(label=label):
                document, tracked, registered, docs = self.registered_epoch_state(
                    layout=layout
                )
                failures = self.validate_epoch_state(
                    document, tracked, registered, docs
                )
                self.assert_failure(failures, "audit-epoch-state-invalid")

        document, tracked, registered, docs = self.registered_epoch_state(
            layout=((1, (1,)),)
        )
        original = next(path for path in docs if path.endswith("amendment-1.md"))
        for round_id in ("duplicate-a", "duplicate-b", "duplicate-c"):
            duplicate = original.replace("round-1", f"round-{round_id}")
            docs[duplicate] = docs[original]
            tracked.append(duplicate)
            registered[duplicate] = git_blob_id(docs[duplicate])
        failures = self.validate_epoch_state(document, tracked, registered, docs)
        self.assert_failure(failures, "audit-epoch-state-invalid")

        original_raw = docs.pop(original)
        original_pin = registered.pop(original)
        tracked.remove(original)
        for round_id in range(1, 5):
            unnumbered = (
                f"wiki/audit/campaign/epoch-1/round-unnumbered-{round_id}/"
                "protocol-correction.md"
            )
            docs[unnumbered] = original_raw
            tracked.append(unnumbered)
            registered[unnumbered] = original_pin
        failures = self.validate_epoch_state(document, tracked, registered, docs)
        self.assert_failure(failures, "audit-epoch-state-invalid")

    def test_epoch_state_machine_rejects_skipped_epoch_and_missing_registration(self) -> None:
        document, tracked, registered, docs = self.registered_epoch_state(
            layout=((1, (1,)), (3, (1,)))
        )
        failures = self.validate_epoch_state(document, tracked, registered, docs)
        self.assert_failure(failures, "audit-epoch-state-invalid")

        for label, suffix in (
            ("artifact", "amendment-1.md"),
            ("receipt", "consolidation-receipt.json"),
        ):
            with self.subTest(label=label):
                document, tracked, registered, docs = self.registered_epoch_state(
                    layout=((1, (1,)),)
                )
                target = next(path for path in registered if path.endswith(suffix))
                registered.pop(target)
                failures = self.validate_epoch_state(
                    document, tracked, registered, docs
                )
                self.assert_failure(failures, "audit-artifact-unregistered")

    def test_epoch_state_machine_rejects_repin_and_forged_spec_binding(self) -> None:
        document, tracked, registered, docs = self.registered_epoch_state(
            layout=((1, (1,)),)
        )
        artifact = next(path for path in registered if path.endswith("amendment-1.md"))
        registered[artifact] = "0" * 40
        failures = self.validate_epoch_state(document, tracked, registered, docs)
        self.assert_failure(failures, "audit-registry-blob-mismatch")

        document, tracked, registered, docs = self.registered_epoch_state(
            layout=((1, (1,)),)
        )
        receipt = next(
            path for path in registered if path.endswith("consolidation-receipt.json")
        )
        receipt_document = json.loads(docs[receipt])
        receipt_document["effective_spec_sha256"] = "0" * 64
        docs[receipt] = (
            json.dumps(receipt_document, sort_keys=True) + "\n"
        ).encode("utf-8")
        registered[receipt] = git_blob_id(docs[receipt])
        failures = self.validate_epoch_state(document, tracked, registered, docs)
        self.assert_failure(failures, "consolidation-epoch-invalid")

    def test_epoch_state_machine_requires_metadata_path_and_receipt_identity(self) -> None:
        document, tracked, registered, docs = self.registered_epoch_state(
            layout=((1, (1,)),)
        )
        artifact = next(path for path in registered if path.endswith("amendment-1.md"))
        docs[artifact] = docs[artifact].replace(b"ordinal: 1\n", b"ordinal: 2\n")
        registered[artifact] = git_blob_id(docs[artifact])

        failures = self.validate_epoch_state(document, tracked, registered, docs)

        self.assert_failure(failures, "audit-iteration-metadata-invalid")

    def test_highest_epoch_receipt_requires_exact_current_manifest_binding(self) -> None:
        document, tracked, registered, docs = self.registered_epoch_state(
            layout=((1, (1,)),)
        )
        document["active_entries"][0]["sha256"] = "0" * 64

        failures = self.validate_epoch_state(document, tracked, registered, docs)

        self.assert_failure(failures, "consolidation-epoch-invalid")

    def test_unnumbered_fixed_correction_remains_legal_without_epoch_stub(self) -> None:
        path = (
            "wiki/audit/system-first-stage1a/round-12/"
            "stage1a-readiness-correction.md"
        )
        self.write(path, b"bounded fixed correction\n")

        failures = evaluate_manifest(self.repo, manifest([]), tracked_paths=[path])

        self.assertEqual([], failures)

    def test_exact_named_markdown_legacy_exceptions_pass_but_new_peer_fails(self) -> None:
        legacy = list(builder.EXACT_NAMED_LEGACY_EXCEPTIONS)
        tracked = []
        for entry in legacy:
            self.write(entry["path"], b"historical\n")
            tracked.append(entry["path"])
        new_peer = "wiki/2026-07-19-another-proposal.md"
        self.write(new_peer, b"new\n")
        tracked.append(new_peer)

        failures = evaluate_manifest(
            self.repo,
            manifest([], legacy=legacy),
            tracked_paths=tracked,
        )

        self.assertEqual(8, len(legacy))
        self.assertEqual(
            {
                "unclassified-persistent-document",
                "new-audit-artifact-outside-audit-root",
            },
            set(failure_codes(failures)),
            failures,
        )

    def test_review_named_machine_log_is_not_a_document_placement_violation(self) -> None:
        path = "wiki/survey/2026-07-19-new-review-log.jsonl"
        self.write(path, b'{"event":"read"}\n')

        failures = evaluate_manifest(self.repo, manifest([]), tracked_paths=[path])

        self.assertEqual([], failures)

    def test_agent_guides_normalize_only_the_three_client_lines(self) -> None:
        agents = "\n".join(
            [
                "# AGENTS.md",
                "",
                "This file provides guidance to Codex (Codex.ai/code) "
                "when working with code in this repository.",
                "",
                "same shared rule",
                "",
                "## Research skills",
                "",
                "Installed via the Windows Codex plugin marketplace (see `docs/setup.md`):",
                "skills",
                "",
            ]
        )
        claude = agents.replace("# AGENTS.md", "# CLAUDE.md").replace(
            "Codex (Codex.ai/code)", "Claude Code (claude.ai/code)"
        ).replace("Windows Codex plugin", "Windows Claude Code plugin")

        self.assertEqual(normalize_agent_guide(agents), normalize_agent_guide(claude))

    def test_agent_guide_client_exceptions_must_be_unique_and_in_place(self) -> None:
        valid = "\n".join(
            [
                "# AGENTS.md",
                "",
                "This file provides guidance to Codex (Codex.ai/code) "
                "when working with code in this repository.",
                "",
                "shared",
                "",
                "## Research skills",
                "",
                "Installed via the Windows Codex plugin marketplace (see `docs/setup.md`):",
                "skills",
                "",
            ]
        )
        description = (
            "This file provides guidance to Codex (Codex.ai/code) "
            "when working with code in this repository."
        )
        marketplace = (
            "Installed via the Windows Codex plugin marketplace (see `docs/setup.md`):"
        )
        mutations = {
            "missing": valid.replace(marketplace + "\n", ""),
            "duplicate": valid.replace(description, description + "\n" + description),
            "h1-not-line-one": "\n" + valid,
            "marketplace-outside-section": valid.replace(
                "## Research skills\n\n" + marketplace,
                marketplace + "\n\n## Research skills",
            ),
        }

        for label, mutated in mutations.items():
            with self.subTest(label=label), self.assertRaises(ContextSurfaceError):
                normalize_agent_guide(mutated)

    def test_agent_guide_rejects_every_foreign_client_identity_line(self) -> None:
        agents = "\n".join(
            [
                "# AGENTS.md",
                "",
                "This file provides guidance to Codex (Codex.ai/code) "
                "when working with code in this repository.",
                "",
                "shared",
                "",
                "## Research skills",
                "",
                "Installed via the Windows Codex plugin marketplace (see `docs/setup.md`):",
                "skills",
                "",
            ]
        )
        claude = agents.replace("# AGENTS.md", "# CLAUDE.md").replace(
            "Codex (Codex.ai/code)", "Claude Code (claude.ai/code)"
        ).replace("Windows Codex plugin", "Windows Claude Code plugin")
        guides = {"AGENTS": agents, "CLAUDE": claude}

        for client, valid in guides.items():
            foreign_client = "CLAUDE" if client == "AGENTS" else "AGENTS"
            for field in ("h1", "description", "marketplace"):
                foreign = surface.AGENT_GUIDE_CLIENTS[foreign_client][field]
                with (
                    self.subTest(client=client, field=field),
                    self.assertRaises(ContextSurfaceError),
                ):
                    normalize_agent_guide(valid + foreign + "\n")

    def test_fourth_agent_guide_difference_is_not_normalized(self) -> None:
        real_repo = Path(__file__).resolve().parents[2]
        agents = (real_repo / "AGENTS.md").read_text(encoding="utf-8")
        claude = (real_repo / "CLAUDE.md").read_text(encoding="utf-8")
        claude = claude.replace(
            "Umbrella repo for four studies",
            "Umbrella repo for changed studies",
            1,
        )
        self.write("AGENTS.md", agents.encode("utf-8"))
        self.write("CLAUDE.md", claude.encode("utf-8"))
        active = [
            self.active_entry("AGENTS.md", agents.encode("utf-8"), "HOT"),
            self.active_entry("CLAUDE.md", claude.encode("utf-8"), "HOT"),
        ]

        failures = evaluate_manifest(
            self.repo,
            manifest(active),
            tracked_paths=["AGENTS.md", "CLAUDE.md"],
        )

        self.assert_failure(failures, "agent-guides-not-mirrored")


class AiContextRepositoryPolicyTests(unittest.TestCase):
    """Acceptance contract for the real Task-7 documentation surface."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.repo = Path(__file__).resolve().parents[2]

    @classmethod
    def read_text(cls, relative_path: str) -> str:
        return cls.repo.joinpath(*PurePosixPath(relative_path).parts).read_text(
            encoding="utf-8"
        )

    @classmethod
    def read_bytes(cls, relative_path: str) -> bytes:
        return cls.repo.joinpath(*PurePosixPath(relative_path).parts).read_bytes()

    def test_collaboration_policy_declares_every_document_role_and_route(self) -> None:
        policy = self.read_text("wiki/AI-Collaboration.md")
        required_roles = (
            "HOT",
            "CURRENT",
            "REGISTRY",
            "AUDIT",
            "ARCHIVE",
            "WORKBENCH",
            "Engineering spec",
            "Engineering plan",
            "Check report",
            "Executable rule",
            "Ephemeral scratch",
        )
        required_routes = (
            "wiki/Research-Objective.md",
            "wiki/survey/current/",
            "wiki/survey/registry/",
            "wiki/audit/<campaign>/<round-id>/",
            "wiki/archive/<knowledge-layer>/<campaign>/",
            "wiki/survey/workbench/<campaign>/",
            "docs/superpowers/specs/",
            "docs/superpowers/plans/",
            "docs/checks/<campaign>/<release-id>/",
            "scripts/",
            "Not committed",
        )

        for token in (*required_roles, *required_routes):
            with self.subTest(token=token):
                self.assertIn(token, policy)
        for column in ("谁读取", "默认加载", "权威性", "进入条件", "搬运/退出条件"):
            with self.subTest(column=column):
                self.assertIn(column, policy)

    def test_collaboration_policy_defines_six_step_lifecycle_and_move_gate(self) -> None:
        policy = self.read_text("wiki/AI-Collaboration.md")
        lifecycle = (
            "Capture",
            "Classify",
            "Work",
            "Consolidate",
            "Release / Audit",
            "Archive / Expire",
        )
        positions = [policy.index(f"**{step}**") for step in lifecycle]
        self.assertEqual(sorted(positions), positions)

        required_meanings = (
            "第三次 amendment 或 correction",
            "超过 context budget",
            "reviewer Gate MAJOR",
            "handoff",
            "stage/release boundary",
            "competing active claims",
            "第三次修正必须立即折叠",
            "第四次修正",
            "禁止",
            "stage-0",
            "current manifest",
            "audit registry",
            "inbound reference",
            "Git blob",
            "git mv",
            "补丁链",
            "active truth",
        )
        for token in required_meanings:
            with self.subTest(token=token):
                self.assertIn(token, policy)

    def test_executable_collaboration_policy_validator_accepts_real_policy(self) -> None:
        policy = self.read_text("wiki/AI-Collaboration.md")

        self.assertEqual([], surface.validate_collaboration_policy(policy))

    def test_executable_collaboration_policy_validator_rejects_semantic_mutations(self) -> None:
        policy = self.read_text("wiki/AI-Collaboration.md")
        lines = policy.splitlines()
        hot_index = next(
            index for index, line in enumerate(lines) if line.startswith("| **HOT** |")
        )
        current_index = next(
            index for index, line in enumerate(lines) if line.startswith("| **CURRENT** |")
        )
        swapped = list(lines)
        swapped[hot_index], swapped[current_index] = (
            swapped[current_index],
            swapped[hot_index],
        )
        step_reordered = policy.replace("1. **Capture**", "1. **Classify**", 1).replace(
            "2. **Classify**", "2. **Capture**", 1
        )
        mutations = {
            "trigger-weakened": policy.replace(
                "以下任一事件先发生就立即 Consolidate：",
                "以下事件可以忽略：",
                1,
            ),
            "audit-overwrite": policy.replace(
                "round 件与 `consolidation-receipt.json` 首个 commit 起 immutable；index append-only",
                "round 件与 receipt 允许覆写；index 可改写",
                1,
            ),
            "role-row-swap": "\n".join(swapped) + "\n",
            "exit-reversed": policy.replace(
                "已注册件永不移动/改写",
                "已注册件可以移动并覆盖",
                1,
            ),
            "step-reordered": step_reordered,
            "receipt-order-removed": policy.replace(
                "先 commit receipt、append 注册",
                "稍后再处理 receipt",
                1,
            ),
            "epoch-continuity-removed": policy.replace(
                "epoch 从 1 连续递增",
                "epoch 可任意编号",
                1,
            ),
        }

        for label, mutated in mutations.items():
            with self.subTest(label=label):
                failures = surface.validate_collaboration_policy(mutated)
                self.assertIn("collaboration-policy-invalid", failure_codes(failures))

    def test_agent_guides_and_contributing_route_without_copying_full_policy(self) -> None:
        agents_raw = self.read_bytes("AGENTS.md")
        claude_raw = self.read_bytes("CLAUDE.md")
        agents = agents_raw.decode("utf-8")
        claude = claude_raw.decode("utf-8")

        self.assertLessEqual(len(agents_raw), 12288)
        self.assertLessEqual(len(claude_raw), 12288)
        self.assertEqual(normalize_agent_guide(agents), normalize_agent_guide(claude))
        for guide in (agents, claude):
            self.assertIn("wiki/Research-Objective.md", guide)
            self.assertIn("wiki/Project-Thesis.md", guide)
            self.assertIn("wiki/AI-Collaboration.md", guide)
            self.assertIn("Research-Objective.md` ≤5KB", guide)
            self.assertIn("Per-Work-Status.md ≤8KB", guide)
            self.assertIn("survey/README.md ≤4KB", guide)
            self.assertNotIn("搬运/退出条件", guide)

        contributing = self.read_text("CONTRIBUTING.md")
        for route in (
            "wiki/survey/current/",
            "wiki/survey/registry/",
            "wiki/audit/<campaign>/<round-id>/",
            "wiki/archive/<knowledge-layer>/<campaign>/",
            "wiki/survey/workbench/<campaign>/",
            "docs/superpowers/specs/",
            "docs/superpowers/plans/",
            "docs/checks/<campaign>/<release-id>/",
            "scripts/",
        ):
            with self.subTest(route=route):
                self.assertIn(route, contributing)
        self.assertIn("wiki/AI-Collaboration.md", contributing)

    def test_research_objective_is_bounded_current_truth(self) -> None:
        path = "wiki/Research-Objective.md"
        raw = self.read_bytes(path)
        text = raw.decode("utf-8")

        self.assertLessEqual(len(raw), 5120)
        refresh = re.search(r'^last_refresh: "(\d{4}-\d{2}-\d{2})', text, re.MULTILINE)
        self.assertIsNotNone(refresh)
        refresh_date = date.fromisoformat(refresh.group(1))
        self.assertEqual(date(2026, 7, 24), refresh_date)
        self.assertLessEqual(refresh_date, date.today())
        required_truth = (
            "Stage-1C v2 signed calibration input awaiting two independent coders",
            "Stage-1B v5 release",
            "external, reward-guided control plane",
            "20,727",
            "319",
            "226",
            "320-work calibration input",
            "15 pending problem labels",
            "13 canonical synthesis claims",
            "56-work calibration packet",
            "separate release signatures",
            "H5",
            "owner",
            "Model/API execution",
            "wiki/survey/current/README.md",
            "system-first-stage1c-v2-precalibration/README.md",
            "38fb9435d0c35e226ad62b16015a6dbee054e6c2",
            "Next action",
            "Supersession rule",
        )
        for token in required_truth:
            with self.subTest(token=token):
                self.assertIn(token, text)
        self.assertNotIn("ready for sign-off", text)

    def test_hot_state_preserves_stage1c_authority_boundary(self) -> None:
        for path in (
            "wiki/Research-Objective.md",
            "wiki/Per-Work-Status.md",
            "wiki/survey/current/status.md",
        ):
            text = self.read_text(path)
            with self.subTest(path=path):
                for token in (
                    "Stage-1B",
                    "Stage-1C",
                    "H5",
                ):
                    self.assertIn(token, text)
                self.assertRegex(
                    text,
                    r"(?i)H5[\s\S]{0,220}(?:pending|withheld|待|尚缺|不得进入)",
                )
                for stale in ("2225c48", ".wiki-tmp", "4506900"):
                    self.assertNotIn(stale, text)

    def test_secondary_status_and_survey_router_are_compact(self) -> None:
        per_work_raw = self.read_bytes("wiki/Per-Work-Status.md")
        per_work = per_work_raw.decode("utf-8")
        self.assertLessEqual(len(per_work_raw), 8192)
        refreshed = re.search(r"Last refreshed (\d{4}-\d{2}-\d{2})", per_work)
        self.assertIsNotNone(refreshed)
        per_work_date = date.fromisoformat(refreshed.group(1))
        objective = self.read_text("wiki/Research-Objective.md")
        objective_date = date.fromisoformat(
            re.search(r'^last_refresh: "(\d{4}-\d{2}-\d{2})', objective, re.MULTILINE).group(1)
        )
        self.assertEqual(date(2026, 7, 24), per_work_date)
        self.assertEqual(objective_date, per_work_date)
        self.assertLessEqual(per_work_date, date.today())
        for work in ("W1", "W2", "W3", "W4"):
            with self.subTest(work=work):
                self.assertEqual(
                    1,
                    len(re.findall(rf"^## {work}(?:\s|$)", per_work, flags=re.MULTILINE)),
                )
        self.assertIn("wiki/archive/", per_work)
        self.assertIn("wiki/survey/current/README.md", per_work)

        router_raw = self.read_bytes("wiki/survey/README.md")
        router = router_raw.decode("utf-8")
        self.assertLessEqual(len(router_raw), 4096)
        for route in (
            "current/",
            "registry/",
            "workbench/",
            "../audit/",
            "../archive/",
        ):
            with self.subTest(route=route):
                self.assertIn(route, router)
        self.assertNotIn("protocol_version", router)
        self.assertNotRegex(router, r"\b\d+/11\b")

    def test_real_manifest_is_generated_bounded_and_activates_only_task8_pair(self) -> None:
        relative_path = "docs/integrity/ai-context-manifest.json"
        document = load_json_strict(
            self.repo.joinpath(*PurePosixPath(relative_path).parts)
        )
        active = document["active_entries"]
        self.assertEqual(20, len(active))
        defaults = {
            entry["path"] for entry in active if entry["load_policy"] == "default"
        }
        self.assertEqual(
            {"AGENTS.md", "wiki/Research-Objective.md", "wiki/Project-Thesis.md"},
            defaults,
        )
        self.assertTrue(
            all(entry["class"] not in {"AUDIT", "ARCHIVE", "WORKBENCH"} for entry in active)
        )
        policy_entry = next(
            entry for entry in active if entry["path"] == "wiki/AI-Collaboration.md"
        )
        self.assertEqual("targeted", policy_entry["load_policy"])
        audit_index = next(
            entry
            for entry in active
            if entry["path"] == "wiki/audit/system-first-stage1a/INDEX.md"
        )
        self.assertEqual(
            ("HOT", "targeted"),
            (audit_index["class"], audit_index["load_policy"]),
        )
        correction = (
            "wiki/audit/system-first-stage1a/round-12/"
            "stage1a-readiness-correction.md"
        )
        self.assertNotIn(correction, {entry["path"] for entry in active})
        self.assertEqual(correction, document["active_review_transaction"])
        by_path = {entry["path"]: entry for entry in active}
        self.assertNotIn(SELF_REFERENTIAL_PACKAGE_REPORT, by_path)
        for path in INTEGRATION_EVIDENCE_PATHS:
            with self.subTest(path=path):
                self.assertIn(path, by_path)
                self.assertEqual(
                    ("HOT", "targeted"),
                    (by_path[path]["class"], by_path[path]["load_policy"]),
                )


class AiContextManifestBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.repo = Path(temporary.name)
        self.registry = self.repo / "wiki/survey/sf-audit-artifact-registry.json"
        self.registry.parent.mkdir(parents=True)
        artifacts = [
            {
                "path": f"wiki/legacy/review-{index:02d}.md",
                "git_blob": f"{index + 1:040x}",
            }
            for index in range(77)
        ]
        self.artifacts = artifacts
        self.registry.write_text(
            json.dumps({"artifacts": artifacts}), encoding="utf-8"
        )
        for artifact in artifacts:
            path = self.repo.joinpath(*PurePosixPath(artifact["path"]).parts)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"registered audit\n")
            artifact["git_blob"] = git_blob_id(path.read_bytes())
        self.registry.write_text(
            json.dumps({"artifacts": artifacts}), encoding="utf-8"
        )
        self.anchor_relative_path = "scripts/checks/ai_context_inventory.py"
        self.anchor = self.repo / self.anchor_relative_path
        self.anchor.parent.mkdir(parents=True)
        self.write_anchor_fixture()
        self.specs = (
            {
                "path": "AGENTS.md",
                "class": "HOT",
                "load_policy": "default",
                "purpose": "client guide",
            },
            {
                "path": "wiki/Research-Objective.md",
                "class": "HOT",
                "load_policy": "default",
                "purpose": "live state",
            },
            {
                "path": "wiki/Project-Thesis.md",
                "class": "HOT",
                "load_policy": "default",
                "purpose": "north star",
            },
            {
                "path": "docs/integrity/ai-context-manifest.json",
                "class": "HOT",
                "load_policy": "targeted",
                "purpose": "manifest metadata",
            },
        )
        for spec in self.specs[:-1]:
            path = self.repo.joinpath(*PurePosixPath(spec["path"]).parts)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes((spec["path"] + "\n").encode("utf-8"))
        agents_guide = (
            "# AGENTS.md\n\n"
            "This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.\n\n"
            "shared fixture\n\n## Research skills\n\n"
            "Installed via the Windows Codex plugin marketplace (see `docs/setup.md`):\n"
            "skills\n"
        )
        claude_guide = agents_guide.replace("# AGENTS.md", "# CLAUDE.md").replace(
            "Codex (Codex.ai/code)", "Claude Code (claude.ai/code)"
        ).replace("Windows Codex plugin", "Windows Claude Code plugin")
        (self.repo / "AGENTS.md").write_text(agents_guide, encoding="utf-8")
        (self.repo / "CLAUDE.md").write_text(claude_guide, encoding="utf-8")
        retained_path = self.repo / "wiki/survey/legacy-protocol.md"
        retained_path.parent.mkdir(parents=True, exist_ok=True)
        retained_path.write_bytes(b"legacy protocol\n")
        self.tracked = [
            self.anchor_relative_path,
            "wiki/survey/sf-audit-artifact-registry.json",
            "wiki/survey/legacy-protocol.md",
            "CLAUDE.md",
            *(artifact["path"] for artifact in artifacts),
            *(spec["path"] for spec in self.specs[:-1]),
        ]
        self.blobs = {
            path: git_blob_id(
                self.repo.joinpath(*PurePosixPath(path).parts).read_bytes()
            )
            for path in self.tracked
        }

    def registry_anchor(self) -> tuple[int, str]:
        canonical = [
            {"path": entry["path"], "git_blob": entry["git_blob"]}
            for entry in self.artifacts
        ]
        return len(canonical), hashlib.sha256(
            json.dumps(
                canonical, ensure_ascii=False, separators=(",", ":")
            ).encode("utf-8")
        ).hexdigest()

    def write_anchor_fixture(
        self,
        *,
        count: int | None = None,
        prefix_sha256: str | None = None,
    ) -> None:
        actual_count, actual_sha = self.registry_anchor()
        count = actual_count if count is None else count
        prefix_sha256 = actual_sha if prefix_sha256 is None else prefix_sha256
        self.anchor.write_text(
            "REGISTRY_BASELINE_COUNT = " + str(count) + "\n"
            "REGISTRY_BASELINE_PREFIX_SHA256 = (\n"
            f'    "{prefix_sha256}"\n'
            ")\n",
            encoding="utf-8",
            newline="\n",
        )

    def patched_builder(self):
        settings = {
            "ACTIVE_ENTRY_SPECS": self.specs,
            "ACTIVE_REVIEW_TRANSACTION": None,
            "BUDGETS_BYTES": {"AGENTS.md": 12288},
            "EXACT_NAMED_LEGACY_EXCEPTIONS": (),
            "EXACT_PREEXISTING_LEGACY_DOCS": (),
            "RETAINED_LEGACY_PATHS": (
                {
                    "path": "wiki/survey/legacy-protocol.md",
                    "class": "REGISTRY_LEGACY",
                },
            ),
        }
        if hasattr(builder, "ARCHIVE_TRANSITIONS"):
            settings["ARCHIVE_TRANSITIONS"] = ()
        if hasattr(builder, "REGISTRY_BASELINE_PREFIX_SHA256"):
            count, prefix_sha256 = self.registry_anchor()
            settings["REGISTRY_BASELINE_COUNT"] = count
            settings["REGISTRY_BASELINE_PREFIX_SHA256"] = prefix_sha256
        return mock.patch.multiple(builder, **settings)

    @staticmethod
    def archive_transitions():
        return tuple(
            {"source": source, "destination": destination, "git_blob": blob}
            for source, destination, blob in EXPECTED_ARCHIVE_TRANSITIONS
        )

    def archive_inventory(self, destination_indices=()):
        destination_indices = set(destination_indices)
        tracked = list(self.tracked)
        blobs = dict(self.blobs)
        real_repo = Path(__file__).resolve().parents[2]
        for index, transition in enumerate(self.archive_transitions()):
            path = (
                transition["destination"]
                if index in destination_indices
                else transition["source"]
            )
            target = self.repo.joinpath(*PurePosixPath(path).parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            real_source = real_repo.joinpath(
                *PurePosixPath(transition["source"]).parts
            )
            real_destination = real_repo.joinpath(
                *PurePosixPath(transition["destination"]).parts
            )
            source_bytes = (
                real_source.read_bytes()
                if real_source.exists()
                else real_destination.read_bytes()
            )
            self.assertEqual(transition["git_blob"], git_blob_id(source_bytes))
            target.write_bytes(source_bytes)
            tracked.append(path)
            blobs[path] = transition["git_blob"]
        return tracked, blobs

    def staged_graph(self, extra_paths=(), tracked=None, blobs=None):
        """Return a real stage-0-shaped graph and a cat-file-like reader."""

        base_paths = self.tracked if tracked is None else tracked
        paths = list(
            dict.fromkeys([*base_paths, *extra_paths])
        )
        raw_by_path = {
            path: self.repo.joinpath(*PurePosixPath(path).parts).read_bytes()
            for path in paths
        }
        actual_blobs = {path: git_blob_id(raw) for path, raw in raw_by_path.items()}
        selected_blobs = actual_blobs if blobs is None else {
            path: blobs[path] for path in paths
        }
        inventory = {
            path: {
                "mode": "100644",
                "blob": selected_blobs[path],
                "stage": 0,
            }
            for path in paths
        }
        raw_by_blob = {
            actual_blobs[path]: raw for path, raw in raw_by_path.items()
        }

        def read_blob(blob: str) -> bytes:
            return raw_by_blob[blob]

        return inventory, read_blob

    def add_registered_epoch(
        self,
        *,
        ordinal: int = 1,
        register_artifact: bool = True,
        register_receipt: bool = True,
        forged_spec_hash: bool = False,
    ) -> tuple[str, str, str]:
        spec_path = "wiki/survey/current/protocol.md"
        spec_raw = (
            "---\nprotocol_id: TEST\nprotocol_version: 2\n---\n\n"
            "# Effective protocol\n"
        ).encode("utf-8")
        spec_sha = raw_sha256(spec_raw)
        effective_sha = "0" * 64 if forged_spec_hash else spec_sha
        artifact = (
            "wiki/audit/campaign/epoch-1/round-1/"
            f"protocol-amendment-{ordinal}.md"
        )
        receipt = "wiki/audit/campaign/epoch-1/consolidation-receipt.json"
        docs = {
            spec_path: spec_raw,
            artifact: AiContextSurfaceTests.iteration_raw(
                campaign="campaign",
                epoch=1,
                ordinal=ordinal,
                kind="amendment",
                spec_path=spec_path,
                spec_version=2,
                spec_sha256=effective_sha,
            ),
            receipt: (
                json.dumps(
                    {
                        "schema": "ai-context-consolidation-receipt-v1",
                        "campaign": "campaign",
                        "epoch": 1,
                        "effective_spec": spec_path,
                        "effective_spec_version": 2,
                        "effective_spec_sha256": effective_sha,
                    },
                    sort_keys=True,
                )
                + "\n"
            ).encode("utf-8"),
        }
        for path, raw in docs.items():
            target = self.repo.joinpath(*PurePosixPath(path).parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
        for path, should_register in (
            (artifact, register_artifact),
            (receipt, register_receipt),
        ):
            if should_register:
                self.artifacts.append(
                    {"path": path, "git_blob": git_blob_id(docs[path])}
                )
        self.registry.write_text(
            json.dumps({"artifacts": self.artifacts}), encoding="utf-8"
        )
        self.write_anchor_fixture()
        self.specs = (
            *self.specs[:-1],
            {
                "path": spec_path,
                "class": "CURRENT",
                "load_policy": "targeted",
                "purpose": "effective protocol",
            },
            self.specs[-1],
        )
        self.tracked.extend((spec_path, artifact, receipt))
        self.blobs.update(
            {
                path: git_blob_id(
                    self.repo.joinpath(*PurePosixPath(path).parts).read_bytes()
                )
                for path in (
                    self.anchor_relative_path,
                    "wiki/survey/sf-audit-artifact-registry.json",
                    spec_path,
                    artifact,
                    receipt,
                )
            }
        )
        return spec_path, artifact, receipt

    def test_builder_requires_stage_bound_raw_for_every_influencing_input(self) -> None:
        inventory, read_blob = self.staged_graph()
        paths = {
            "active": "wiki/Research-Objective.md",
            "budget": "AGENTS.md",
            "other-agent-guide": "CLAUDE.md",
            "registry": "wiki/survey/sf-audit-artifact-registry.json",
            "inventory-anchor": self.anchor_relative_path,
            "legacy": "wiki/survey/legacy-protocol.md",
        }
        for label, relative_path in paths.items():
            with self.subTest(label=label):
                target = self.repo.joinpath(*PurePosixPath(relative_path).parts)
                original = target.read_bytes()
                target.write_bytes(original + b"dirty-after-stage\n")
                try:
                    with self.patched_builder(), self.assertRaises(
                        builder.ManifestBuildError
                    ) as raised:
                        builder.build_manifest(
                            self.repo,
                            index_inventory=inventory,
                            read_blob=read_blob,
                            allow_untracked_self=True,
                        )
                    self.assertIn("index-worktree-mismatch", str(raised.exception))
                finally:
                    target.write_bytes(original)

    def test_builder_rejects_crlf_worktree_against_staged_lf(self) -> None:
        target = self.repo / "AGENTS.md"
        target.write_bytes(b"line one\nline two\n")
        inventory, read_blob = self.staged_graph()
        target.write_bytes(b"line one\r\nline two\r\n")

        with self.patched_builder(), self.assertRaises(
            builder.ManifestBuildError
        ) as raised:
            builder.build_manifest(
                self.repo,
                index_inventory=inventory,
                read_blob=read_blob,
                allow_untracked_self=True,
            )

        self.assertIn("index-worktree-mismatch", str(raised.exception))

    def test_builder_rejects_staged_old_worktree_new_active_bytes(self) -> None:
        inventory, read_blob = self.staged_graph()
        target = self.repo / "wiki/Project-Thesis.md"
        target.write_bytes(b"newer worktree truth\n")

        with self.patched_builder(), self.assertRaises(
            builder.ManifestBuildError
        ) as raised:
            builder.build_manifest(
                self.repo,
                index_inventory=inventory,
                read_blob=read_blob,
                allow_untracked_self=True,
            )

        self.assertIn("index-worktree-mismatch", str(raised.exception))

    def test_builder_rejects_untracked_guide_and_nonregular_stage0_modes(self) -> None:
        inventory, read_blob = self.staged_graph()
        without_claude = dict(inventory)
        without_claude.pop("CLAUDE.md")
        with self.patched_builder(), self.assertRaises(
            builder.ManifestBuildError
        ) as untracked:
            builder.build_manifest(
                self.repo,
                index_inventory=without_claude,
                read_blob=read_blob,
                allow_untracked_self=True,
            )
        self.assertIn("agent-guide-untracked", str(untracked.exception))

        for mode in ("120000", "160000", "040000"):
            with self.subTest(mode=mode):
                malformed = json.loads(json.dumps(inventory))
                malformed["AGENTS.md"]["mode"] = mode
                with self.patched_builder(), self.assertRaises(
                    builder.ManifestBuildError
                ) as raised:
                    builder.build_manifest(
                        self.repo,
                        index_inventory=malformed,
                        read_blob=read_blob,
                        allow_untracked_self=True,
                    )
                self.assertIn("index-entry-not-regular", str(raised.exception))

    def test_builder_rejects_nonzero_stage_and_cat_file_blob_anomalies(self) -> None:
        inventory, read_blob = self.staged_graph()
        nonzero = json.loads(json.dumps(inventory))
        nonzero["AGENTS.md"]["stage"] = 2
        with self.patched_builder(), self.assertRaises(
            builder.ManifestBuildError
        ) as staged:
            builder.build_manifest(
                self.repo,
                index_inventory=nonzero,
                read_blob=read_blob,
                allow_untracked_self=True,
            )
        self.assertIn("index-entry-not-stage-0", str(staged.exception))

        anomalies = {
            "missing": lambda _blob: (_ for _ in ()).throw(KeyError("missing")),
            "wrong-raw": lambda _blob: b"not the indexed Git object\n",
            "wrong-type": lambda _blob: "not-bytes",
        }
        for label, broken_reader in anomalies.items():
            with self.subTest(label=label), self.patched_builder(), self.assertRaises(
                builder.ManifestBuildError
            ) as raised:
                builder.build_manifest(
                    self.repo,
                    index_inventory=inventory,
                    read_blob=broken_reader,
                    allow_untracked_self=True,
                )
            self.assertIn("index-blob", str(raised.exception))

    def test_builder_stage_binds_complete_audit_activation_pair(self) -> None:
        index_path = "wiki/audit/system-first-stage1a/INDEX.md"
        correction = (
            "wiki/audit/system-first-stage1a/round-12/"
            "stage1a-readiness-correction.md"
        )
        for path in (index_path, correction):
            target = self.repo.joinpath(*PurePosixPath(path).parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((path + "\n").encode("utf-8"))
        inventory, read_blob = self.staged_graph((index_path, correction))
        correction_path = self.repo.joinpath(*PurePosixPath(correction).parts)
        correction_path.write_bytes(b"changed after stage\n")

        with (
            self.patched_builder(),
            mock.patch.object(builder, "ACTIVE_REVIEW_TRANSACTION", correction),
            self.assertRaises(builder.ManifestBuildError) as raised,
        ):
            builder.build_manifest(
                self.repo,
                index_inventory=inventory,
                read_blob=read_blob,
                allow_untracked_self=True,
            )

        self.assertIn("index-worktree-mismatch", str(raised.exception))

    def test_builder_accepts_registered_epoch_state(self) -> None:
        self.add_registered_epoch()
        inventory, read_blob = self.staged_graph()

        with self.patched_builder():
            document = builder.build_manifest(
                self.repo, inventory, read_blob, allow_untracked_self=True
            )

        self.assertIn(
            "wiki/survey/current/protocol.md",
            {entry["path"] for entry in document["active_entries"]},
        )

    def test_builder_rejects_unregistered_epoch_artifact_or_receipt(self) -> None:
        for label, options in (
            ("artifact", {"register_artifact": False}),
            ("receipt", {"register_receipt": False}),
        ):
            with self.subTest(label=label):
                self.setUp()
                self.add_registered_epoch(**options)
                inventory, read_blob = self.staged_graph()
                with self.patched_builder(), self.assertRaises(
                    builder.ManifestBuildError
                ) as raised:
                    builder.build_manifest(
                        self.repo, inventory, read_blob, allow_untracked_self=True
                    )
                self.assertIn("audit-artifact-unregistered", str(raised.exception))

    def test_builder_rejects_dirty_registered_epoch_artifact_and_receipt(self) -> None:
        _spec, artifact, receipt = self.add_registered_epoch()
        inventory, read_blob = self.staged_graph()
        for label, path in (("artifact", artifact), ("receipt", receipt)):
            with self.subTest(label=label):
                target = self.repo.joinpath(*PurePosixPath(path).parts)
                original = target.read_bytes()
                target.write_bytes(original + b"dirty\n")
                try:
                    with self.patched_builder(), self.assertRaises(
                        builder.ManifestBuildError
                    ) as raised:
                        builder.build_manifest(
                            self.repo,
                            inventory,
                            read_blob,
                            allow_untracked_self=True,
                        )
                    self.assertIn("index-worktree-mismatch", str(raised.exception))
                finally:
                    target.write_bytes(original)

    def test_builder_rejects_forged_epoch_spec_binding(self) -> None:
        self.add_registered_epoch(forged_spec_hash=True)
        inventory, read_blob = self.staged_graph()

        with self.patched_builder(), self.assertRaises(
            builder.ManifestBuildError
        ) as raised:
            builder.build_manifest(
                self.repo, inventory, read_blob, allow_untracked_self=True
            )

        self.assertIn("consolidation-epoch-invalid", str(raised.exception))

    def test_builder_rejects_registered_prefix_repin(self) -> None:
        _spec, artifact, _receipt = self.add_registered_epoch()
        anchored_count = len(self.artifacts)
        anchored_sha = hashlib.sha256(
            json.dumps(
                [
                    {"path": entry["path"], "git_blob": entry["git_blob"]}
                    for entry in self.artifacts
                ],
                ensure_ascii=False,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        target = self.repo.joinpath(*PurePosixPath(artifact).parts)
        target.write_bytes(target.read_bytes() + b"repinned rewrite\n")
        self.artifacts[-2]["git_blob"] = git_blob_id(target.read_bytes())
        self.registry.write_text(
            json.dumps({"artifacts": self.artifacts}), encoding="utf-8"
        )
        self.blobs[artifact] = git_blob_id(target.read_bytes())
        self.blobs["wiki/survey/sf-audit-artifact-registry.json"] = git_blob_id(
            self.registry.read_bytes()
        )
        inventory, read_blob = self.staged_graph()

        with (
            self.patched_builder(),
            mock.patch.object(builder, "REGISTRY_BASELINE_COUNT", anchored_count),
            mock.patch.object(
                builder, "REGISTRY_BASELINE_PREFIX_SHA256", anchored_sha
            ),
            self.assertRaises(builder.ManifestBuildError) as raised,
        ):
            builder.build_manifest(
                self.repo, inventory, read_blob, allow_untracked_self=True
            )

        self.assertIn("audit-registry-prefix-mismatch", str(raised.exception))

    def test_archive_transition_constants_pin_exact_sources_destinations_and_blobs(self) -> None:
        actual = tuple(
            (entry["source"], entry["destination"], entry["git_blob"])
            for entry in getattr(builder, "ARCHIVE_TRANSITIONS", ())
        )

        self.assertEqual(EXPECTED_ARCHIVE_TRANSITIONS, actual)

    def test_archive_transition_accepts_all_sources_then_all_destinations(self) -> None:
        transitions = self.archive_transitions()
        tracked, blobs = self.archive_inventory()
        inventory, read_blob = self.staged_graph(tracked=tracked, blobs=blobs)
        with self.patched_builder(), mock.patch.object(
            builder, "ARCHIVE_TRANSITIONS", transitions, create=True
        ):
            prearchive = builder.build_manifest(
                self.repo, inventory, read_blob, allow_untracked_self=True
            )
        pending = {
            entry["path"]
            for entry in prearchive["legacy_cold_paths"]
            if entry["class"] == "PENDING_ARCHIVE"
        }
        self.assertEqual({entry["source"] for entry in transitions}, pending)

        tracked, blobs = self.archive_inventory(range(7))
        inventory, read_blob = self.staged_graph(tracked=tracked, blobs=blobs)
        with self.patched_builder(), mock.patch.object(
            builder, "ARCHIVE_TRANSITIONS", transitions, create=True
        ):
            archived = builder.build_manifest(
                self.repo, inventory, read_blob, allow_untracked_self=True
            )
        legacy_paths = {entry["path"] for entry in archived["legacy_cold_paths"]}
        self.assertTrue(all(entry["source"] not in legacy_paths for entry in transitions))
        self.assertTrue(
            all(classify_path(entry["destination"], []) == "ARCHIVE" for entry in transitions)
        )

    def test_archive_transition_rejects_partial_and_both_states(self) -> None:
        transitions = self.archive_transitions()
        cases = {
            "one_moved": ({0}, None),
            "both_source_and_destination": (set(), 0),
        }
        for label, (destination_indices, duplicate_index) in cases.items():
            with self.subTest(label=label):
                tracked, blobs = self.archive_inventory(destination_indices)
                if duplicate_index is not None:
                    transition = transitions[duplicate_index]
                    destination = transition["destination"]
                    target = self.repo.joinpath(*PurePosixPath(destination).parts)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(b"duplicate state\n")
                    tracked.append(destination)
                    blobs[destination] = transition["git_blob"]
                inventory, read_blob = self.staged_graph(
                    tracked=tracked, blobs=blobs
                )
                with (
                    self.patched_builder(),
                    mock.patch.object(
                        builder, "ARCHIVE_TRANSITIONS", transitions, create=True
                    ),
                    self.assertRaises(builder.ManifestBuildError) as raised,
                ):
                    builder.build_manifest(
                        self.repo, inventory, read_blob, allow_untracked_self=True
                    )
                self.assertIn("archive-transition-incomplete", str(raised.exception))

    def test_archive_transition_rejects_wrong_destination_blob(self) -> None:
        transitions = self.archive_transitions()
        tracked, blobs = self.archive_inventory(range(7))
        blobs[transitions[0]["destination"]] = "0" * 40
        inventory, read_blob = self.staged_graph(tracked=tracked, blobs=blobs)

        with (
            self.patched_builder(),
            mock.patch.object(
                builder, "ARCHIVE_TRANSITIONS", transitions, create=True
            ),
            self.assertRaises(builder.ManifestBuildError) as raised,
        ):
            builder.build_manifest(
                self.repo, inventory, read_blob, allow_untracked_self=True
            )

        self.assertIn("archive-transition-blob-mismatch", str(raised.exception))

    def test_real_retained_constants_are_exact_existing_paths(self) -> None:
        real_repo = Path(__file__).resolve().parents[2]
        paths = [
            entry["path"]
            for entry in (
                *builder.RETAINED_LEGACY_PATHS,
                *builder.EXACT_NAMED_LEGACY_EXCEPTIONS,
                *builder.EXACT_PREEXISTING_LEGACY_DOCS,
            )
        ]

        self.assertEqual(len(paths), len(set(paths)))
        self.assertFalse(any(any(token in path for token in "*?[") for path in paths))
        self.assertEqual(
            [],
            [
                path
                for path in paths
                if not real_repo.joinpath(*PurePosixPath(path).parts).is_file()
            ],
        )

    def test_builder_is_deterministic_and_self_hash_free(self) -> None:
        inventory, read_blob = self.staged_graph()
        with self.patched_builder():
            first = builder.render_manifest(
                self.repo,
                inventory,
                read_blob,
                allow_untracked_self=True,
            )
            second = builder.render_manifest(
                self.repo,
                inventory,
                read_blob,
                allow_untracked_self=True,
            )

        self.assertEqual(first, second)
        self.assertNotIn(str(self.repo).encode("utf-8"), first)
        self.assertNotIn(b"\\", first)
        document = json.loads(first)
        self.assertEqual(4, len(document["active_entries"]))
        self_entry = next(
            entry
            for entry in document["active_entries"]
            if entry["path"] == "docs/integrity/ai-context-manifest.json"
        )
        self.assertNotIn("sha256", self_entry)
        self.assertEqual(78, len(document["legacy_cold_paths"]))

    def test_builder_write_and_check_are_byte_exact(self) -> None:
        target = self.repo / "docs/integrity/ai-context-manifest.json"
        inventory, read_blob = self.staged_graph()
        with self.patched_builder():
            builder.write_manifest(self.repo, target, inventory, read_blob)
            try:
                failures = builder.check_manifest(
                    self.repo, target, inventory, read_blob
                )
            except builder.ManifestBuildError as exc:
                self.fail(f"pre-git-add bootstrap check raised: {exc}")
            self.assertEqual([], failures)
            document = load_json_strict(target)
            self.assertEqual(
                [], evaluate_manifest(self.repo, document, self.tracked)
            )
            target.write_bytes(target.read_bytes() + b" ")
            failures = builder.check_manifest(
                self.repo, target, inventory, read_blob
            )

        self.assertIn("manifest-byte-mismatch", failure_codes(failures))

    def test_manifest_check_rejects_tracked_old_self_with_generated_worktree(self) -> None:
        target = self.repo / "docs/integrity/ai-context-manifest.json"
        inventory, read_blob = self.staged_graph()
        with self.patched_builder():
            expected = builder.render_manifest(
                self.repo, inventory, read_blob, allow_untracked_self=True
            )
        target.parent.mkdir(parents=True)
        target.write_bytes(expected)
        old_raw = b'{"old":"staged manifest"}\n'
        old_blob = git_blob_id(old_raw)
        tracked_inventory = dict(inventory)
        tracked_inventory[builder.MANIFEST_RELATIVE_PATH] = {
            "mode": "100644",
            "blob": old_blob,
            "stage": 0,
        }

        def tracked_reader(blob: str) -> bytes:
            return old_raw if blob == old_blob else read_blob(blob)

        with self.patched_builder(), self.assertRaises(
            builder.ManifestBuildError
        ) as raised:
            builder.check_manifest(
                self.repo, target, tracked_inventory, tracked_reader
            )

        self.assertIn("index-worktree-mismatch", str(raised.exception))

    def test_manifest_check_rejects_post_stage_rewrite_and_crlf_self(self) -> None:
        target = self.repo / "docs/integrity/ai-context-manifest.json"
        inventory, read_blob = self.staged_graph()
        with self.patched_builder():
            builder.write_manifest(self.repo, target, inventory, read_blob)
        staged_inventory, staged_reader = self.staged_graph(
            extra_paths=(builder.MANIFEST_RELATIVE_PATH,)
        )
        staged_raw = target.read_bytes()
        mutations = {
            "post-stage-rewrite": staged_raw + b" ",
            "crlf": staged_raw.replace(b"\n", b"\r\n"),
        }
        for label, mutated in mutations.items():
            with self.subTest(label=label):
                target.write_bytes(mutated)
                with self.patched_builder(), self.assertRaises(
                    builder.ManifestBuildError
                ) as raised:
                    builder.check_manifest(
                        self.repo, target, staged_inventory, staged_reader
                    )
                self.assertIn("index-worktree-mismatch", str(raised.exception))
        target.write_bytes(staged_raw)

    def test_manifest_write_allows_dirty_tracked_self_then_requires_restage(self) -> None:
        target = self.repo / "docs/integrity/ai-context-manifest.json"
        target.parent.mkdir(parents=True)
        target.write_bytes(b'{"old":"staged"}\n')
        inventory, read_blob = self.staged_graph(
            extra_paths=(builder.MANIFEST_RELATIVE_PATH,)
        )
        target.write_bytes(b'{"dirty":"worktree"}\n')

        with self.patched_builder():
            builder.write_manifest(self.repo, target, inventory, read_blob)
            with self.assertRaises(builder.ManifestBuildError) as raised:
                builder.check_manifest(self.repo, target, inventory, read_blob)

        self.assertIn("index-worktree-mismatch", str(raised.exception))
        self.assertTrue(target.read_bytes().endswith(b"\n"))

    def test_manifest_bootstrap_rejects_wrong_target(self) -> None:
        wrong_target = self.repo / "docs/integrity/not-the-manifest.json"
        inventory, read_blob = self.staged_graph()
        with self.patched_builder(), self.assertRaises(
            builder.ManifestBuildError
        ) as raised:
            builder.write_manifest(
                self.repo, wrong_target, inventory, read_blob
            )

        self.assertIn("manifest-target-invalid", str(raised.exception))
        self.assertFalse(wrong_target.exists())

    @unittest.skipIf(os.name == "nt", "real self symlink check runs in WSL/POSIX")
    def test_manifest_bootstrap_rejects_self_symlink(self) -> None:
        target = self.repo / "docs/integrity/ai-context-manifest.json"
        target.parent.mkdir(parents=True)
        os.symlink(self.repo / "AGENTS.md", target)
        document = {
            "schema": "ai-context-manifest-v1",
            "active_entries": [dict(self.specs[-1])],
            "budgets_bytes": {},
            "legacy_cold_paths": [],
            "active_review_transaction": None,
        }

        failures = evaluate_manifest(self.repo, document, self.tracked)

        self.assertIn("untrusted-repo-path", failure_codes(failures))

    def test_manifest_bootstrap_does_not_excuse_another_untracked_active(self) -> None:
        target = self.repo / "docs/integrity/ai-context-manifest.json"
        extra_path = "wiki/survey/current/extra.md"
        extra_raw = b"extra\n"
        extra = {
            "path": extra_path,
            "class": "CURRENT",
            "load_policy": "targeted",
            "purpose": "must remain tracked",
            "sha256": raw_sha256(extra_raw),
        }
        inventory, read_blob = self.staged_graph()
        with self.patched_builder():
            builder.write_manifest(self.repo, target, inventory, read_blob)
        extra_file = self.repo.joinpath(*PurePosixPath(extra_path).parts)
        extra_file.parent.mkdir(parents=True, exist_ok=True)
        extra_file.write_bytes(extra_raw)
        document = load_json_strict(target)
        document["active_entries"].append(extra)

        failures = evaluate_manifest(self.repo, document, self.tracked)

        self.assertEqual(1, failure_codes(failures).count("active-path-untracked"))

    def test_audit_lifecycle_absent_is_a_valid_task7_manifest(self) -> None:
        target = self.repo / "docs/integrity/ai-context-manifest.json"
        correction = (
            "wiki/audit/system-first-stage1a/round-12/"
            "stage1a-readiness-correction.md"
        )
        inventory, read_blob = self.staged_graph()
        with self.patched_builder(), mock.patch.object(
            builder, "ACTIVE_REVIEW_TRANSACTION", correction
        ):
            try:
                builder.write_manifest(
                    self.repo, target, inventory, read_blob
                )
                document = load_json_strict(target)
            except builder.ManifestBuildError as exc:
                self.fail(f"absent audit lifecycle should be valid: {exc}")

        active_paths = {entry["path"] for entry in document["active_entries"]}
        self.assertNotIn("wiki/audit/system-first-stage1a/INDEX.md", active_paths)
        self.assertIsNone(document["active_review_transaction"])

    def test_audit_lifecycle_activates_only_when_both_paths_are_tracked(self) -> None:
        index_path = "wiki/audit/system-first-stage1a/INDEX.md"
        correction = (
            "wiki/audit/system-first-stage1a/round-12/"
            "stage1a-readiness-correction.md"
        )
        for path in (index_path, correction):
            target = self.repo.joinpath(*PurePosixPath(path).parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((path + "\n").encode("utf-8"))
        inventory, read_blob = self.staged_graph(
            extra_paths=(index_path, correction)
        )

        with self.patched_builder(), mock.patch.object(
            builder, "ACTIVE_REVIEW_TRANSACTION", correction
        ):
            document = builder.build_manifest(
                self.repo, inventory, read_blob, allow_untracked_self=True
            )

        index_entries = [
            entry for entry in document["active_entries"] if entry["path"] == index_path
        ]
        self.assertEqual(1, len(index_entries))
        self.assertEqual("targeted", index_entries[0]["load_policy"])
        self.assertEqual(correction, document["active_review_transaction"])

    def test_audit_lifecycle_half_present_fails_closed(self) -> None:
        index_path = "wiki/audit/system-first-stage1a/INDEX.md"
        correction = (
            "wiki/audit/system-first-stage1a/round-12/"
            "stage1a-readiness-correction.md"
        )
        for present in (index_path, correction):
            with self.subTest(present=present):
                target = self.repo.joinpath(*PurePosixPath(present).parts)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((present + "\n").encode("utf-8"))
                inventory, read_blob = self.staged_graph(extra_paths=(present,))
                with (
                    self.patched_builder(),
                    mock.patch.object(
                        builder, "ACTIVE_REVIEW_TRANSACTION", correction
                    ),
                    self.assertRaises(builder.ManifestBuildError) as raised,
                ):
                    builder.build_manifest(
                        self.repo, inventory, read_blob, allow_untracked_self=True
                    )
                self.assertIn("audit-activation-incomplete", str(raised.exception))

    def test_builder_check_rejects_crlf_and_performs_zero_writes(self) -> None:
        target = self.repo / "docs/integrity/ai-context-manifest.json"
        inventory, read_blob = self.staged_graph()
        with self.patched_builder():
            builder.write_manifest(self.repo, target, inventory, read_blob)
            target.write_bytes(target.read_bytes().replace(b"\n", b"\r\n"))
            with (
                mock.patch.object(Path, "mkdir") as mkdir,
                mock.patch.object(builder.tempfile, "mkstemp") as mkstemp,
                mock.patch.object(builder.os, "replace") as replace,
            ):
                failures = builder.check_manifest(
                    self.repo, target, inventory, read_blob
                )

        self.assertIn("manifest-byte-mismatch", failure_codes(failures))
        mkdir.assert_not_called()
        mkstemp.assert_not_called()
        replace.assert_not_called()

    def test_atomic_write_failures_are_controlled_and_leave_no_debris(self) -> None:
        target = self.repo / "docs/integrity/ai-context-manifest.json"
        target.parent.mkdir(parents=True)
        target.write_bytes(b"previous manifest\n")
        inventory, read_blob = self.staged_graph()
        scenarios = {
            "mkdir": mock.patch.object(
                Path, "mkdir", side_effect=OSError("mkdir denied")
            ),
            "mkstemp": mock.patch.object(
                builder.tempfile, "mkstemp", side_effect=OSError("mkstemp denied")
            ),
            "write": mock.patch.object(
                builder.os, "write", side_effect=OSError("write denied")
            ),
            "fsync": mock.patch.object(
                builder.os, "fsync", side_effect=OSError("fsync denied")
            ),
            "replace": mock.patch.object(
                builder.os, "replace", side_effect=OSError("replace denied")
            ),
        }
        for label, operation in scenarios.items():
            with self.subTest(label=label), self.patched_builder(), operation:
                with self.assertRaises(builder.ManifestBuildError) as raised:
                    builder.write_manifest(
                        self.repo, target, inventory, read_blob
                    )
                self.assertIn("manifest-write-failed", str(raised.exception))
                self.assertEqual(b"previous manifest\n", target.read_bytes())
                self.assertEqual([], list(target.parent.glob(f".{target.name}.*")))

    def test_write_fsync_replace_failures_leave_fresh_target_absent(self) -> None:
        inventory, read_blob = self.staged_graph()
        scenarios = {
            "write": mock.patch.object(
                builder.os, "write", side_effect=OSError("write denied")
            ),
            "fsync": mock.patch.object(
                builder.os, "fsync", side_effect=OSError("fsync denied")
            ),
            "replace": mock.patch.object(
                builder.os, "replace", side_effect=OSError("replace denied")
            ),
        }
        for label, operation in scenarios.items():
            target = self.repo / "docs/integrity/ai-context-manifest.json"
            if target.exists():
                target.unlink()
            with (
                self.subTest(label=label),
                self.patched_builder(),
                operation,
                self.assertRaises(builder.ManifestBuildError) as raised,
            ):
                builder.write_manifest(self.repo, target, inventory, read_blob)

            self.assertIn("manifest-write-failed", str(raised.exception))
            self.assertFalse(target.exists())
            self.assertEqual([], list(target.parent.glob(f".{target.name}.*")))

    def test_git_inventory_os_errors_are_controlled(self) -> None:
        with mock.patch.object(
            builder.subprocess, "run", side_effect=OSError("git unavailable")
        ), self.assertRaises(builder.ManifestBuildError) as builder_raised:
            builder._git_inventory(self.repo)
        self.assertIn("git-inventory-failed", str(builder_raised.exception))

        with mock.patch(
            "ai_context_surface_check.subprocess.run",
            side_effect=OSError("git unavailable"),
        ), self.assertRaises(ContextSurfaceError) as oracle_raised:
            _git_tracked_paths(self.repo)
        self.assertIn("git-ls-files-failed", str(oracle_raised.exception))

    def test_windows_worktree_gitdir_is_portable_to_wsl_for_all_git_readers(self) -> None:
        pointer_repo = self.repo / "linked-worktree"
        pointer_repo.mkdir()
        (pointer_repo / ".git").write_text(
            "gitdir: D:/repo/.git/worktrees/linked\n",
            encoding="utf-8",
            newline="\n",
        )
        prefix = surface.git_command_prefix(pointer_repo, platform="posix")
        self.assertEqual(
            [
                "git",
                "--git-dir=/mnt/d/repo/.git/worktrees/linked",
                f"--work-tree={pointer_repo}",
            ],
            prefix,
        )

        completed = mock.Mock(returncode=0, stdout=b"", stderr=b"")
        with (
            mock.patch.object(builder, "git_command_prefix", return_value=prefix),
            mock.patch.object(
                builder.subprocess, "run", return_value=completed
            ) as run,
        ):
            self.assertEqual({}, builder._git_inventory(pointer_repo))
        self.assertEqual(prefix + ["ls-files", "-s", "-z"], run.call_args.args[0])

        with (
            mock.patch.object(surface, "git_command_prefix", return_value=prefix),
            mock.patch.object(surface.subprocess, "run", return_value=completed) as run,
        ):
            self.assertEqual([], surface._git_tracked_paths(pointer_repo))
        self.assertEqual(prefix + ["ls-files", "-z"], run.call_args.args[0])

    def test_builder_validates_exact_registry_inventory(self) -> None:
        registry = json.loads(self.registry.read_text(encoding="utf-8"))
        registry["artifacts"].pop()
        self.registry.write_text(json.dumps(registry), encoding="utf-8")
        inventory, read_blob = self.staged_graph()

        with self.patched_builder(), self.assertRaises(builder.ManifestBuildError) as raised:
            builder.render_manifest(
                self.repo, inventory, read_blob, allow_untracked_self=True
            )

        self.assertIn("audit-registry-baseline-short", str(raised.exception))

    def test_registry_baseline_prefix_rejects_reorder_and_changed_blob(self) -> None:
        original = json.loads(self.registry.read_text(encoding="utf-8"))
        for label in ("reorder", "changed_blob"):
            with self.subTest(label=label):
                document = json.loads(json.dumps(original))
                if label == "reorder":
                    document["artifacts"][0], document["artifacts"][1] = (
                        document["artifacts"][1],
                        document["artifacts"][0],
                    )
                else:
                    document["artifacts"][0]["git_blob"] = "a" * 40
                self.registry.write_text(json.dumps(document), encoding="utf-8")
                inventory, read_blob = self.staged_graph()
                with self.patched_builder(), self.assertRaises(
                    builder.ManifestBuildError
                ) as raised:
                    builder.render_manifest(
                        self.repo,
                        inventory,
                        read_blob,
                        allow_untracked_self=True,
                    )
                self.assertIn("audit-registry-prefix-mismatch", str(raised.exception))

    def test_registry_allows_anchored_audit_root_append_without_legacy_inflation(self) -> None:
        index_path = "wiki/audit/system-first-stage1a/INDEX.md"
        correction = (
            "wiki/audit/system-first-stage1a/round-12/"
            "stage1a-readiness-correction.md"
        )
        for path in (index_path, correction):
            target = self.repo.joinpath(*PurePosixPath(path).parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((path + "\n").encode("utf-8"))
        document = json.loads(self.registry.read_text(encoding="utf-8"))
        correction_blob = git_blob_id(
            self.repo.joinpath(*PurePosixPath(correction).parts).read_bytes()
        )
        document["artifacts"].append({"path": correction, "git_blob": correction_blob})
        self.artifacts.append({"path": correction, "git_blob": correction_blob})
        self.registry.write_text(json.dumps(document), encoding="utf-8")
        self.write_anchor_fixture()
        inventory, read_blob = self.staged_graph(
            extra_paths=(index_path, correction)
        )

        with self.patched_builder(), mock.patch.object(
            builder, "ACTIVE_REVIEW_TRANSACTION", correction
        ):
            try:
                manifest_document = builder.build_manifest(
                    self.repo, inventory, read_blob, allow_untracked_self=True
                )
            except builder.ManifestBuildError as exc:
                self.fail(f"valid registry append was rejected: {exc}")

        active_paths = {entry["path"] for entry in manifest_document["active_entries"]}
        legacy_paths = {
            entry["path"] for entry in manifest_document["legacy_cold_paths"]
        }
        self.assertEqual(78, len(document["artifacts"]))
        self.assertIn(index_path, active_paths)
        self.assertEqual(correction, manifest_document["active_review_transaction"])
        self.assertNotIn(correction, legacy_paths)
        self.assertEqual(78, len(legacy_paths))

    def test_registry_rejects_an_unanchored_appended_tail(self) -> None:
        path = "wiki/audit/campaign/round-1/review.md"
        target = self.repo.joinpath(*PurePosixPath(path).parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"review\n")
        document = json.loads(self.registry.read_text(encoding="utf-8"))
        document["artifacts"].append(
            {"path": path, "git_blob": git_blob_id(target.read_bytes())}
        )
        self.registry.write_text(json.dumps(document), encoding="utf-8")
        inventory, read_blob = self.staged_graph(extra_paths=(path,))

        with self.patched_builder(), self.assertRaises(
            builder.ManifestBuildError
        ) as raised:
            builder.build_manifest(
                self.repo, inventory, read_blob, allow_untracked_self=True
            )

        self.assertIn("audit-registry-unanchored-append", str(raised.exception))

    def test_b8_registry_anchor_growth_is_atomic_and_stage_bound(self) -> None:
        index_path = "wiki/audit/system-first-stage1a/INDEX.md"
        correction = (
            "wiki/audit/system-first-stage1a/round-12/"
            "stage1a-readiness-correction.md"
        )
        for path in (index_path, correction):
            target = self.repo.joinpath(*PurePosixPath(path).parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((path + "\n").encode("utf-8"))
        base_registry_raw = self.registry.read_bytes()
        base_count, base_sha = self.registry_anchor()
        row = {
            "path": correction,
            "git_blob": git_blob_id(
                self.repo.joinpath(*PurePosixPath(correction).parts).read_bytes()
            ),
        }
        appended = json.loads(base_registry_raw)
        appended["artifacts"].append(row)
        appended_raw = json.dumps(appended).encode("utf-8")
        self.registry.write_bytes(appended_raw)
        inventory, read_blob = self.staged_graph(
            extra_paths=(index_path, correction)
        )

        with (
            self.patched_builder(),
            mock.patch.object(builder, "ACTIVE_REVIEW_TRANSACTION", correction),
            self.assertRaises(builder.ManifestBuildError) as unanchored,
        ):
            builder.build_manifest(
                self.repo, inventory, read_blob, allow_untracked_self=True
            )
        self.assertIn("audit-registry-unanchored-append", str(unanchored.exception))

        self.artifacts.append(row)
        correct_count, correct_sha = self.registry_anchor()
        self.assertEqual(78, correct_count)
        self.write_anchor_fixture()
        inventory, read_blob = self.staged_graph(
            extra_paths=(index_path, correction)
        )
        with self.patched_builder(), mock.patch.object(
            builder, "ACTIVE_REVIEW_TRANSACTION", correction
        ):
            document = builder.build_manifest(
                self.repo, inventory, read_blob, allow_untracked_self=True
            )
        self.assertEqual(correction, document["active_review_transaction"])

        bad_anchors = {
            "wrong-count": (correct_count + 1, correct_sha),
            "wrong-hash": (correct_count, "0" * 64),
        }
        for label, (count, prefix_sha256) in bad_anchors.items():
            with (
                self.subTest(label=label),
                self.patched_builder(),
                mock.patch.object(builder, "ACTIVE_REVIEW_TRANSACTION", correction),
                mock.patch.object(builder, "REGISTRY_BASELINE_COUNT", count),
                mock.patch.object(
                    builder, "REGISTRY_BASELINE_PREFIX_SHA256", prefix_sha256
                ),
                self.assertRaises(builder.ManifestBuildError),
            ):
                builder.build_manifest(
                    self.repo, inventory, read_blob, allow_untracked_self=True
                )

        self.registry.write_bytes(base_registry_raw)
        self.write_anchor_fixture()
        old_inventory, old_reader = self.staged_graph(
            extra_paths=(index_path, correction)
        )
        self.registry.write_bytes(appended_raw)
        with (
            self.patched_builder(),
            mock.patch.object(builder, "ACTIVE_REVIEW_TRANSACTION", correction),
            self.assertRaises(builder.ManifestBuildError) as unstaged_registry,
        ):
            builder.build_manifest(
                self.repo,
                old_inventory,
                old_reader,
                allow_untracked_self=True,
            )
        self.assertIn("index-worktree-mismatch", str(unstaged_registry.exception))

        self.write_anchor_fixture(count=base_count, prefix_sha256=base_sha)
        old_anchor_inventory, old_anchor_reader = self.staged_graph(
            extra_paths=(index_path, correction)
        )
        self.write_anchor_fixture()
        with (
            self.patched_builder(),
            mock.patch.object(builder, "ACTIVE_REVIEW_TRANSACTION", correction),
            self.assertRaises(builder.ManifestBuildError) as unstaged_anchor,
        ):
            builder.build_manifest(
                self.repo,
                old_anchor_inventory,
                old_anchor_reader,
                allow_untracked_self=True,
            )
        self.assertIn("index-worktree-mismatch", str(unstaged_anchor.exception))

    def test_registry_rejects_extra_outside_audit_root(self) -> None:
        extra_path = "wiki/2026-07-20-extra-review.md"
        target = self.repo.joinpath(*PurePosixPath(extra_path).parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"extra review\n")
        document = json.loads(self.registry.read_text(encoding="utf-8"))
        document["artifacts"].append(
            {"path": extra_path, "git_blob": git_blob_id(target.read_bytes())}
        )
        self.registry.write_text(json.dumps(document), encoding="utf-8")
        inventory, read_blob = self.staged_graph(extra_paths=(extra_path,))

        with self.patched_builder(), self.assertRaises(
            builder.ManifestBuildError
        ) as raised:
            builder.build_manifest(
                self.repo, inventory, read_blob, allow_untracked_self=True
            )

        self.assertIn("audit-registry-extra-path", str(raised.exception))

    def test_builder_fails_closed_when_an_active_artifact_is_missing(self) -> None:
        inventory, read_blob = self.staged_graph()
        missing = self.repo / "wiki/Project-Thesis.md"
        missing.unlink()

        with self.patched_builder(), self.assertRaises(builder.ManifestBuildError) as raised:
            builder.render_manifest(
                self.repo, inventory, read_blob, allow_untracked_self=True
            )

        self.assertIn("index-worktree-missing", str(raised.exception))

    def test_builder_rejects_duplicate_and_malformed_registry_blobs(self) -> None:
        original = json.loads(self.registry.read_text(encoding="utf-8"))
        mutations = {
            "duplicate": lambda document: document["artifacts"][1].update(
                path=document["artifacts"][0]["path"]
            ),
            "malformed_blob": lambda document: document["artifacts"][1].update(
                git_blob="not-a-blob"
            ),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                registry = json.loads(json.dumps(original))
                mutate(registry)
                self.registry.write_text(json.dumps(registry), encoding="utf-8")
                inventory, read_blob = self.staged_graph()
                with self.patched_builder(), self.assertRaises(
                    builder.ManifestBuildError
                ) as raised:
                    builder.render_manifest(
                        self.repo,
                        inventory,
                        read_blob,
                        allow_untracked_self=True,
                    )
                expected = "duplicate-path" if label == "duplicate" else "audit-registry-entry"
                self.assertIn(expected, str(raised.exception))

    def test_builder_rejects_forged_legacy_class_and_active_overlap(self) -> None:
        mutations = {
            "forged_class": (
                {
                    "path": "wiki/survey/legacy-protocol.md",
                    "class": "AUDIT_LEGACY",
                },
                "legacy-class-mismatch",
            ),
            "active_overlap": (
                {"path": "AGENTS.md", "class": "REGISTRY_LEGACY"},
                "active-legacy-overlap",
            ),
        }
        for label, (entry, expected) in mutations.items():
            inventory, read_blob = self.staged_graph()
            with (
                self.subTest(label=label),
                self.patched_builder(),
                mock.patch.object(builder, "RETAINED_LEGACY_PATHS", (entry,)),
                self.assertRaises(builder.ManifestBuildError) as raised,
            ):
                builder.render_manifest(
                    self.repo,
                    inventory,
                    read_blob,
                    allow_untracked_self=True,
                )
            self.assertIn(expected, str(raised.exception))

    def test_builder_rejects_wildcards_in_all_policy_constants(self) -> None:
        wildcard_specs = tuple(
            ({**spec, "path": "wiki/*.md"} if index == 0 else spec)
            for index, spec in enumerate(self.specs)
        )
        mutations = {
            "active": {"ACTIVE_ENTRY_SPECS": wildcard_specs},
            "budget": {"BUDGETS_BYTES": {"wiki/*.md": 1}},
            "review": {"ACTIVE_REVIEW_TRANSACTION": "wiki/audit/*/review.md"},
        }
        inventory, read_blob = self.staged_graph()
        for label, mutation in mutations.items():
            with (
                self.subTest(label=label),
                self.patched_builder(),
                mock.patch.multiple(builder, **mutation),
                self.assertRaises(builder.ManifestBuildError) as raised,
            ):
                builder.render_manifest(
                    self.repo,
                    inventory,
                    read_blob,
                    allow_untracked_self=True,
                )
            self.assertIn("wildcard", str(raised.exception))


if __name__ == "__main__":
    unittest.main()
