#!/usr/bin/env python3
"""Contracts for versioned negative-evidence review preparation."""
from __future__ import annotations

import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest import mock


HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import sf_absence_provenance_migrate as migrate  # noqa: E402
from sf_evidence_contract import (  # noqa: E402
    ABSENCE_ALLOWED_VALUES,
    validate_absence_cross_bindings,
    validate_bound_values,
)
from sf_row_hash import row_hash  # noqa: E402


EXPECTED_SOURCE_TUPLES = [
    ("2026.findings-acl.1243#closed-prompt-only", "row", "explicit_candidate_pool_selection", "absence", "false"),
    ("2026.findings-acl.1243#closed-prompt-only", "row", "selection_object", "absence", '"none"'),
    ("2026.findings-acl.1243#open-sft-variant", "row", "explicit_candidate_pool_selection", "absence", "false"),
    ("2026.findings-acl.1243#open-sft-variant", "row", "human_or_dev_label_model_selection", "absence", "false"),
    ("2026.findings-acl.1243#open-sft-variant", "row", "selection_object", "absence", '"none"'),
    ("2026.findings-acl.1724#pipeline", "row", "inference_external_new_information", "absence", "false"),
    ("2604.16529#pdr-random-k", "row", "explicit_candidate_pool_selection", "absence", "false"),
    ("2604.16529#pdr-random-k", "row", "human_or_dev_label_model_selection", "absence", "false"),
    ("2604.16529#pdr-random-k", "row", "selection_object", "absence", '"none"'),
    ("2604.16529#rtv", "row", "decision_rights", "absence", "[]"),
    ("2604.16529#rtv", "row", "human_or_dev_label_model_selection", "absence", "false"),
    ("2604.16529#rtv-pdr-pipeline", "row", "human_or_dev_label_model_selection", "absence", "false"),
    ("2605.08083#discovered-controller", "row", "human_or_dev_label_model_selection", "absence", "false"),
    ("2605.08083#discovered-controller", "row", "inference_external_new_information", "absence", "false"),
    ("2606.03054#trained-gate", "row", "explicit_candidate_pool_selection", "absence", "false"),
    ("2606.03054#trained-gate", "row", "human_or_dev_label_model_selection", "absence", "false"),
    ("2606.03054#trained-gate", "row", "inference_external_new_information", "absence", "false"),
    ("2606.03054#trained-gate", "row", "selection_object", "absence", '"none"'),
]


class AbsenceMigrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sidecars = migrate.load_sidecars(migrate.SIDECAR_DIR)

    def test_source_inventory_is_exactly_18_stable_tuples_after_review_recode(self):
        records = migrate.collect_absence_records(self.sidecars)
        self.assertEqual(18, len(records))
        self.assertEqual(EXPECTED_SOURCE_TUPLES, migrate.source_tuples(records))

    def test_source_inventory_is_a_subset_of_allowed_negative_pairs(self):
        records = migrate.collect_absence_records(self.sidecars)
        observed = {
            (record["field"], migrate.canonical_value(record["value"]))
            for record in records
        }
        expected = {
            (field, migrate.canonical_value(value))
            for field, values in ABSENCE_ALLOWED_VALUES.items()
            for value in values
        }
        self.assertLessEqual(observed, expected)
        self.assertNotIn(
            ("external_component_weight_update", "false"), observed
        )
        self.assertNotIn(
            ("controller_program_or_config_optimized_on_labels", "false"),
            observed,
        )

    def test_source_inventory_has_no_positive_unknown_or_missing_absence(self):
        records = migrate.collect_absence_records(self.sidecars)
        for record in records:
            with self.subTest(record=record["source_tuple"]):
                allowed = ABSENCE_ALLOWED_VALUES[record["field"]]
                self.assertTrue(
                    any(record["value"] == value and type(record["value"]) is type(value)
                        for value in allowed)
                )
                self.assertNotIn(record["value"], (None, "", "unknown"))

    def test_preparation_covers_every_source_once_and_is_deterministic(self):
        first = migrate.prepare_migration(deepcopy(self.sidecars))
        second = migrate.prepare_migration(deepcopy(self.sidecars))
        self.assertEqual(first, second)
        migrated, proof_rows = first
        self.assertEqual(18, len(proof_rows))
        self.assertEqual(18, len({row["adjudication_row_id"] for row in proof_rows}))
        self.assertEqual(
            EXPECTED_SOURCE_TUPLES,
            sorted(tuple(row["source_tuple"]) for row in proof_rows),
        )
        self.assertEqual(len(self.sidecars), len(migrated))

    def test_preparation_never_assigns_semantic_verdict_or_reviewer(self):
        _, proof_rows = migrate.prepare_migration(deepcopy(self.sidecars))
        forbidden = {"verdict", "adjudicator_identity", "independence"}
        for proof in proof_rows:
            with self.subTest(row=proof["adjudication_row_id"]):
                self.assertFalse(forbidden & set(proof))
        artifact = migrate.review_artifact(proof_rows, reviewer_rows=[])
        self.assertEqual("PENDING_INDEPENDENT_REVIEW", artifact["status"])
        self.assertEqual([], artifact["rows"])
        self.assertIn("review_reason", artifact["review_row_required_fields"])
        self.assertEqual(22, artifact["original_proof_inventory_count"])
        self.assertEqual(4, artifact["retired_by_semantic_correction_count"])
        self.assertEqual(18, artifact["active_proof_inventory_count"])
        self.assertEqual("22 = 4 + 18", artifact["inventory_identity"])

    def test_pending_artifact_blocks_all_18_absence_bindings(self):
        migrated, proof_rows = migrate.prepare_migration(deepcopy(self.sidecars))
        artifact = migrate.review_artifact(proof_rows, reviewer_rows=[])
        failures = []
        absence_count = 0
        for filename, sidecar in migrated:
            sidecar_path = f"{migrate.SIDECAR_REPO_PREFIX}/{filename}"
            for row in sidecar["method_paths"]:
                count = sum(
                    entry.get("kind") == "absence"
                    for entry in row["claim_evidence"].values()
                )
                if not count:
                    continue
                absence_count += count
                failures.extend(
                    validate_absence_cross_bindings(
                        row, sidecar_path, sidecar, artifact
                    )
                )
        self.assertEqual(18, absence_count)
        self.assertEqual(
            18,
            sum("absence-adjudication-row-missing" in failure for failure in failures),
        )

    def test_bound_external_reviews_accept_two_explicit_cautions_as_affirmative(self):
        migrated, _ = migrate.prepare_migration(deepcopy(self.sidecars))
        artifact = json.loads(migrate.ADJUDICATION_PATH.read_text(encoding="utf-8"))
        self.assertEqual(18, len(artifact["rows"]))
        self.assertEqual(
            2,
            sum(row["verdict"] == "AGREE_WITH_CAUTION" for row in artifact["rows"]),
        )
        failures = []
        for filename, sidecar in migrated:
            sidecar_path = f"{migrate.SIDECAR_REPO_PREFIX}/{filename}"
            for row in sidecar["method_paths"]:
                failures.extend(
                    validate_absence_cross_bindings(
                        row, sidecar_path, sidecar, artifact
                    )
                )
        self.assertFalse(
            any("absence-verdict-not-agree" in failure for failure in failures),
            failures,
        )

    def test_migrated_rows_pass_local_contract_and_bind_non_circular_hash(self):
        migrated, _ = migrate.prepare_migration(deepcopy(self.sidecars))
        count = 0
        for _, sidecar in migrated:
            for row in sidecar["method_paths"]:
                self.assertEqual([], validate_bound_values(row))
                absences = [
                    entry
                    for entry in row["claim_evidence"].values()
                    if entry.get("kind") == "absence"
                ]
                if not absences:
                    continue
                count += len(absences)
                expected_hash = row_hash(row)
                self.assertEqual(
                    {expected_hash},
                    {entry["owner_row_sha256"] for entry in absences},
                )
                self.assertEqual(expected_hash, row["adjudication_row_sha256"])
                self.assertEqual(
                    "PENDING_INDEPENDENT_REVIEW", row["absence_review_status"]
                )
        self.assertEqual(18, count)

    def test_each_proof_has_exact_locators_reason_and_fulltext_binding(self):
        _, proof_rows = migrate.prepare_migration(deepcopy(self.sidecars))
        for proof in proof_rows:
            with self.subTest(row=proof["adjudication_row_id"]):
                self.assertTrue(proof["inspected_locators"])
                self.assertTrue(all(locator.strip() for locator in proof["inspected_locators"]))
                self.assertGreater(len(proof["reason"].split()), 8)
                self.assertRegex(proof["fulltext"]["sha256"], r"^[0-9a-f]{64}$")
                self.assertIn(
                    proof["implementer_assessment"]["status"],
                    {"READY_FOR_REVIEW", "IMPLEMENTER_CONCERN"},
                )
                self.assertTrue(proof["counterevidence_search_scope"])
                self.assertIsInstance(proof["counterevidence_locators"], list)
                self.assertIsInstance(proof["temporal_order_resolved"], bool)
                self.assertTrue(proof["why_counterevidence_does_not_change_verdict"])

    def test_four_review_challenged_negatives_are_removed_not_force_agreed(self):
        rows = {
            row["method_path_id"]: row
            for _, sidecar in self.sidecars
            for row in sidecar["method_paths"]
        }
        dream = rows["2026.findings-acl.511#prm-guided-search"]
        deepverifier = rows["2026.findings-acl.1243#open-sft-variant"]
        deepverifier_closed = rows["2026.findings-acl.1243#closed-prompt-only"]

        self.assertIs(
            True, dream["controller_program_or_config_optimized_on_labels"]
        )
        self.assertEqual(
            "pdf_page",
            dream["claim_evidence"][
                "controller_program_or_config_optimized_on_labels"
            ]["kind"],
        )
        self.assertEqual("unknown", dream["human_or_dev_label_model_selection"])
        self.assertEqual(
            "pdf_page",
            dream["claim_evidence"]["human_or_dev_label_model_selection"]["kind"],
        )
        self.assertEqual("unknown", deepverifier["external_component_weight_update"])
        self.assertEqual(
            "pdf_page",
            deepverifier["claim_evidence"]["external_component_weight_update"]["kind"],
        )
        self.assertEqual(
            "unknown", deepverifier_closed["human_or_dev_label_model_selection"]
        )
        self.assertEqual(
            "pdf_page",
            deepverifier_closed["claim_evidence"][
                "human_or_dev_label_model_selection"
            ]["kind"],
        )
        self.assertIn(
            "ABS2-216d90876d8397734c37",
            deepverifier_closed["semantic_correction"]["retired_absence_ids"],
        )
        for row in (dream, deepverifier, deepverifier_closed):
            self.assertEqual("adjudicated_agree", row["adjudication_status"])
            self.assertEqual(
                "EXTERNAL_DOCTORAL_REVIEWER_BOUND_TO_ROUND16_PRECHECK",
                row["semantic_adjudicator"],
            )
        for row in (dream, deepverifier):
            self.assertFalse(row["load_bearing"])

    def test_review_artifact_preserves_external_reviewer_rows_but_never_creates_them(self):
        _, proof_rows = migrate.prepare_migration(deepcopy(self.sidecars))
        reviewer_rows = [{"adjudication_row_id": "external", "verdict": "AGREE"}]
        artifact = migrate.review_artifact(proof_rows, reviewer_rows=reviewer_rows)
        self.assertEqual(reviewer_rows, artifact["rows"])
        reviewer_rows[0]["verdict"] = "DISAGREE"
        self.assertEqual("AGREE", artifact["rows"][0]["verdict"])

    def test_cli_write_then_check_is_byte_stable_and_avoids_frozen_query_inputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            sidecar_dir = os.path.join(temporary, "sidecars")
            shutil.copytree(migrate.SIDECAR_DIR, sidecar_dir)
            artifact = os.path.join(temporary, "adjudication.json")
            args = [
                "--sidecar-dir", sidecar_dir,
                "--adjudication", artifact,
            ]
            accessed = []
            original_read = migrate.read_strict_json

            def tracked_read(path):
                accessed.append(os.fspath(path))
                return original_read(path)

            with mock.patch.object(migrate, "read_strict_json", side_effect=tracked_read):
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(0, migrate.main([*args, "--write"]))
                    first = {
                        path: Path(os.path.join(sidecar_dir, path)).read_bytes()
                        for path in os.listdir(sidecar_dir)
                    }
                    first["artifact"] = Path(artifact).read_bytes()
                    self.assertEqual(0, migrate.main([*args, "--check"]))
                    self.assertEqual(0, migrate.main([*args, "--write"]))
                    second = {
                        path: Path(os.path.join(sidecar_dir, path)).read_bytes()
                        for path in os.listdir(sidecar_dir)
                    }
                    second["artifact"] = Path(artifact).read_bytes()
            self.assertEqual(first, second)
            forbidden = ("query-v", "attempt-registry", "compiled-query")
            self.assertFalse(
                any(token in path.lower() for path in accessed for token in forbidden),
                accessed,
            )

    def test_cli_check_fails_before_migration(self):
        with tempfile.TemporaryDirectory() as temporary:
            sidecar_dir = os.path.join(temporary, "sidecars")
            shutil.copytree(migrate.SIDECAR_DIR, sidecar_dir)
            artifact = os.path.join(temporary, "adjudication.json")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(
                    1,
                    migrate.main(
                        [
                            "--sidecar-dir", sidecar_dir,
                            "--adjudication", artifact,
                            "--check",
                        ]
                    ),
                )


if __name__ == "__main__":
    unittest.main()
