#!/usr/bin/env python3
"""Contract tests for the AI context-surface and document-routing oracle."""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath
from unittest import mock


sys.path.insert(0, str(Path(__file__).resolve().parent))

from ai_context_surface_check import (
    ContextSurfaceError,
    classify_path,
    evaluate_manifest,
    load_json_strict,
    normalize_agent_guide,
)
import build_ai_context_manifest as builder


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

    def test_classification_precedence_is_exact(self) -> None:
        legacy = [
            {"path": "wiki/survey/current/legacy.md", "class": "AUDIT_LEGACY"},
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
        active_review = "wiki/audit/campaign/round-12/correction.md"
        raw = b"[correction](../../audit/campaign/round-12/correction.md#result)\n"
        self.write(relative_path, raw)

        failures = evaluate_manifest(
            self.repo,
            manifest(
                [self.active_entry(relative_path, raw, "CURRENT")],
                active_review=active_review,
            ),
            tracked_paths=[relative_path],
        )

        self.assertEqual([], failures)

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
        active_review = "wiki/audit/campaign/round-12/correction.md"
        raw = (
            b"See [correction][ROUND].\n\n"
            b"[round]: <../../audit/campaign/round-12/correction.md#result>\n"
        )
        self.write(relative_path, raw)

        failures = evaluate_manifest(
            self.repo,
            manifest(
                [self.active_entry(relative_path, raw, "CURRENT")],
                active_review=active_review,
            ),
            tracked_paths=[relative_path],
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
        active_review = "wiki/audit/campaign/round-12/correction.md"
        raw = (
            b"See [correction][r].\n\n"
            b"[r]:\n"
            b"  <../../audit/campaign/round-12/correction.md#result>\n"
        )
        self.write(relative_path, raw)

        failures = evaluate_manifest(
            self.repo,
            manifest(
                [self.active_entry(relative_path, raw, "CURRENT")],
                active_review=active_review,
            ),
            tracked_paths=[relative_path],
        )

        self.assertEqual([], failures)

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

    def test_new_amendment_inside_audit_root_still_requires_consolidation(self) -> None:
        path = "wiki/audit/campaign/round-12/protocol-amendment-4.md"
        self.write(path, b"amendment\n")

        failures = evaluate_manifest(self.repo, manifest([]), tracked_paths=[path])

        self.assert_failure(failures, "unconsolidated-amendment-forbidden")

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
            ["new-audit-artifact-outside-audit-root"], failure_codes(failures), failures
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
                "Installed via the Windows Codex plugin marketplace (see `docs/setup.md`):",
                "skills",
                "",
            ]
        )
        claude = agents.replace("# AGENTS.md", "# CLAUDE.md").replace(
            "Codex (Codex.ai/code)", "Claude Code (claude.ai/code)"
        ).replace("Windows Codex plugin", "Windows Claude Code plugin")

        self.assertEqual(normalize_agent_guide(agents), normalize_agent_guide(claude))

    def test_fourth_agent_guide_difference_is_not_normalized(self) -> None:
        real_repo = Path(__file__).resolve().parents[2]
        agents = (real_repo / "AGENTS.md").read_text(encoding="utf-8")
        claude = (real_repo / "CLAUDE.md").read_text(encoding="utf-8")
        claude = claude.replace(
            "Umbrella repo for a four-part research series",
            "Umbrella repo for a changed research series",
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
        self.registry.write_text(
            json.dumps({"artifacts": artifacts}), encoding="utf-8"
        )
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

    def patched_builder(self):
        return mock.patch.multiple(
            builder,
            ACTIVE_ENTRY_SPECS=self.specs,
            EXACT_NAMED_LEGACY_EXCEPTIONS=(),
            RETAINED_LEGACY_PATHS=(
                {
                    "path": "wiki/survey/legacy-protocol.md",
                    "class": "REGISTRY_LEGACY",
                },
            ),
        )

    def test_real_retained_constants_are_exact_existing_paths(self) -> None:
        real_repo = Path(__file__).resolve().parents[2]
        paths = [
            entry["path"]
            for entry in (
                *builder.RETAINED_LEGACY_PATHS,
                *builder.EXACT_NAMED_LEGACY_EXCEPTIONS,
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
        with self.patched_builder():
            first = builder.render_manifest(self.repo, self.registry)
            second = builder.render_manifest(self.repo, self.registry)

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
        with self.patched_builder():
            builder.write_manifest(self.repo, target, self.registry)
            self.assertEqual([], builder.check_manifest(self.repo, target, self.registry))
            document = load_json_strict(target)
            tracked = [entry["path"] for entry in document["active_entries"]]
            self.assertEqual([], evaluate_manifest(self.repo, document, tracked))
            target.write_bytes(target.read_bytes() + b" ")
            failures = builder.check_manifest(self.repo, target, self.registry)

        self.assertIn("manifest-byte-mismatch", failure_codes(failures))

    def test_builder_validates_exact_registry_inventory(self) -> None:
        registry = json.loads(self.registry.read_text(encoding="utf-8"))
        registry["artifacts"].pop()
        self.registry.write_text(json.dumps(registry), encoding="utf-8")

        with self.patched_builder(), self.assertRaises(builder.ManifestBuildError) as raised:
            builder.render_manifest(self.repo, self.registry)

        self.assertIn("audit-registry-count", str(raised.exception))

    def test_builder_fails_closed_when_an_active_artifact_is_missing(self) -> None:
        missing = self.repo / "wiki/Project-Thesis.md"
        missing.unlink()

        with self.patched_builder(), self.assertRaises(builder.ManifestBuildError) as raised:
            builder.render_manifest(self.repo, self.registry)

        self.assertIn("active-path-missing", str(raised.exception))

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
                with self.patched_builder(), self.assertRaises(
                    builder.ManifestBuildError
                ) as raised:
                    builder.render_manifest(self.repo, self.registry)
                expected = "duplicate-path" if label == "duplicate" else "audit-registry-entry"
                self.assertIn(expected, str(raised.exception))


if __name__ == "__main__":
    unittest.main()
