#!/usr/bin/env python3
"""Tests for deterministic schema-v3 adjudication finalization."""

from __future__ import annotations

import copy
import hashlib
import inspect
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sf_schema_v3_finalize as finalizer  # noqa: E402
import sf_schema_v3_migrate as migration  # noqa: E402
from sf_identity_taxonomy_v5_test import row_hash as canonical_row_hash  # noqa: E402


def all_rows(outputs):
    return [
        row
        for _, sidecar in outputs
        for row in sidecar["method_paths"]
    ]


def row_by_id(outputs, method_path_id):
    return next(
        row for row in all_rows(outputs) if row["method_path_id"] == method_path_id
    )


class SchemaV3FinalizerTest(unittest.TestCase):
    def load_artifact(self):
        return json.loads(finalizer.ADJUDICATION_PATH.read_text(encoding="utf-8"))

    def write_artifact(self, directory, artifact):
        path = Path(directory) / "adjudication.json"
        path.write_text(
            json.dumps(artifact, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        return path

    def assert_rejected(self, artifact, pattern):
        with self.assertRaisesRegex(finalizer.FinalizationError, pattern):
            finalizer._validate_adjudication(
                artifact,
                migration.build_outputs(migration.SOURCE_DIR),
            )

    def assert_release_artifact_rejected(self, artifact):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = self.write_artifact(temp_dir, artifact)
            with self.assertRaisesRegex(
                finalizer.FinalizationError, "artifact.*SHA-256.*mismatch"
            ):
                finalizer.build_finalized_outputs(
                    migration.SOURCE_DIR,
                    path,
                )

    def assert_pending_snapshot_rejected(self, pending):
        with self.assertRaisesRegex(
            finalizer.FinalizationError, "pending.*snapshot.*(mismatch|names)"
        ):
            finalizer.finalize_outputs(
                pending,
                finalizer.ADJUDICATION_PATH.read_bytes(),
            )

    def test_all_agree_artifact_stamps_every_sidecar_and_canonical_row_hash(self):
        pending = migration.build_outputs(migration.SOURCE_DIR)
        finalized = finalizer.finalize_outputs(
            pending,
            finalizer.ADJUDICATION_PATH.read_bytes(),
        )

        self.assertEqual(len(finalized), 8)
        self.assertEqual(len(all_rows(finalized)), 11)
        for (_, pending_sidecar), (_, finalized_sidecar) in zip(
            pending, finalized, strict=True
        ):
            self.assertEqual(
                finalized_sidecar["schema_v3_binding_status"],
                "ADJUDICATED_AGREE",
            )
            self.assertEqual(
                finalized_sidecar["schema_v3_binding_adjudicator"],
                "/root/a6_adjudicator",
            )
            expected = copy.deepcopy(pending_sidecar)
            expected["schema_v3_binding_status"] = "ADJUDICATED_AGREE"
            expected["schema_v3_binding_adjudicator"] = "/root/a6_adjudicator"
            for row in expected["method_paths"]:
                row["adjudication_row_sha256"] = canonical_row_hash(row)
            self.assertEqual(finalized_sidecar, expected)
            for row in finalized_sidecar["method_paths"]:
                self.assertEqual(
                    row["adjudication_row_sha256"], canonical_row_hash(row)
                )

    def test_public_finalization_api_accepts_only_pending_and_raw_artifact_bytes(self):
        signature = inspect.signature(finalizer.finalize_outputs)
        self.assertEqual(
            list(signature.parameters), ["pending", "artifact_raw_bytes"]
        )

        pending = migration.build_outputs(migration.SOURCE_DIR)
        raw_bytes = finalizer.ADJUDICATION_PATH.read_bytes()
        mutated_artifact = self.load_artifact()
        mutated_artifact["binding_verdicts"][0]["reason"] += " split-root drift"
        with self.assertRaises(TypeError):
            finalizer.finalize_outputs(pending, mutated_artifact, raw_bytes)

        finalized = finalizer.finalize_outputs(pending, raw_bytes)
        self.assertEqual(len(finalized), 8)

    def test_public_finalization_api_rejects_artifact_hash_override(self):
        signature = inspect.signature(finalizer.finalize_outputs)
        self.assertNotIn("expected_artifact_sha256", signature.parameters)
        with self.assertRaises(TypeError):
            finalizer.finalize_outputs(
                migration.build_outputs(migration.SOURCE_DIR),
                finalizer.ADJUDICATION_PATH.read_bytes(),
                expected_artifact_sha256="0" * 64,
            )

    def test_public_finalization_api_rejects_pending_hash_override(self):
        signature = inspect.signature(finalizer.finalize_outputs)
        self.assertNotIn("expected_pending_sha256", signature.parameters)
        with self.assertRaises(TypeError):
            finalizer.finalize_outputs(
                migration.build_outputs(migration.SOURCE_DIR),
                finalizer.ADJUDICATION_PATH.read_bytes(),
                expected_pending_sha256={},
            )

    def test_release_artifact_sha_rejects_any_reviewer_record_mutation(self):
        cases = []

        binding_tuple = self.load_artifact()
        binding_tuple["resolution_log"][0]["tuple"]["method_path_id"] += "-drift"
        cases.append(("binding-resolution-tuple", binding_tuple))

        anchor_locator = self.load_artifact()
        anchor_locator["resolution_log"][11]["locator"][
            "repaired_locator"
        ] += " drift"
        cases.append(("anchor-repaired-locator", anchor_locator))

        anchor_occurrence = self.load_artifact()
        anchor_occurrence["resolution_log"][11]["locator"]["occurrences"] = 2
        cases.append(("anchor-occurrence", anchor_occurrence))

        coupled_uses = self.load_artifact()
        coupled_uses["resolution_log"][12]["review_scope"][0][
            "encoded_value"
        ] = ["route", "synthesize_input"]
        cases.append(("coupled-uses", coupled_uses))

        original_issue = self.load_artifact()
        original_issue["resolution_log"][0]["original_issue"] += " prose drift"
        cases.append(("original-issue-prose", original_issue))

        reason = self.load_artifact()
        reason["binding_verdicts"][0]["reason"] += " prose drift"
        cases.append(("reason-prose", reason))

        reversed_resolutions = self.load_artifact()
        reversed_resolutions["resolution_log"].reverse()
        cases.append(("resolution-order", reversed_resolutions))

        for label, artifact in cases:
            with self.subTest(label=label):
                self.assert_release_artifact_rejected(artifact)

    def test_reviewed_pending_snapshot_rejects_unreviewed_content_drift(self):
        mutation_cases = []

        edge_semantics = copy.deepcopy(migration.build_outputs(migration.SOURCE_DIR))
        all_rows(edge_semantics)[0]["control_edges"][0]["edge_semantics"] += " drift"
        mutation_cases.append(("edge-semantics", edge_semantics))

        pdf_anchor = copy.deepcopy(migration.build_outputs(migration.SOURCE_DIR))
        row_by_id(pdf_anchor, "2026.findings-acl.511#prm-guided-search")[
            "claim_evidence"
        ]["selection_object"]["anchor"] += " drift"
        mutation_cases.append(("pdf-anchor", pdf_anchor))

        canon_quote = copy.deepcopy(migration.build_outputs(migration.SOURCE_DIR))
        row_by_id(canon_quote, "2026.findings-acl.1243#closed-prompt-only")[
            "claim_evidence"
        ]["selection_policy"]["quote"] += " drift"
        mutation_cases.append(("canon-quote", canon_quote))

        tex_quote = copy.deepcopy(migration.build_outputs(migration.SOURCE_DIR))
        row_by_id(tex_quote, "2604.16529#rtv")["claim_evidence"][
            "selection_object"
        ]["quote"] += " drift"
        mutation_cases.append(("tex-quote", tex_quote))

        absence_scope = copy.deepcopy(migration.build_outputs(migration.SOURCE_DIR))
        row_by_id(absence_scope, "2026.findings-acl.1243#closed-prompt-only")[
            "claim_evidence"
        ]["selection_object"]["scope"] += " drift"
        mutation_cases.append(("absence-scope", absence_scope))

        absence_note = copy.deepcopy(migration.build_outputs(migration.SOURCE_DIR))
        row_by_id(absence_note, "2026.findings-acl.1243#closed-prompt-only")[
            "claim_evidence"
        ]["selection_object"]["note"] += " drift"
        mutation_cases.append(("absence-note", absence_note))

        metadata = copy.deepcopy(migration.build_outputs(migration.SOURCE_DIR))
        metadata[0][1]["work_title"] += " drift"
        mutation_cases.append(("top-level-metadata", metadata))

        for label, outputs in mutation_cases:
            with self.subTest(label=label):
                self.assert_pending_snapshot_rejected(outputs)

    def test_reviewed_pending_snapshot_rejects_missing_extra_and_renamed_sidecars(self):
        pending = migration.build_outputs(migration.SOURCE_DIR)
        cases = (
            ("missing", pending[:-1]),
            (
                "extra",
                [
                    *pending,
                    (Path("extra.sidecar.json"), copy.deepcopy(pending[0][1])),
                ],
            ),
            (
                "renamed",
                [
                    (pending[0][0].with_name("renamed.sidecar.json"), pending[0][1]),
                    *pending[1:],
                ],
            ),
        )
        for label, mutated in cases:
            with self.subTest(label=label):
                self.assert_pending_snapshot_rejected(mutated)

    def test_reviewed_snapshot_constants_match_remediation_commit_and_migration(self):
        expected = getattr(finalizer, "EXPECTED_PENDING_SIDECAR_SHA256", None)
        self.assertIsInstance(expected, dict)
        self.assertEqual(len(expected), 8)
        self.assertEqual(
            finalizer.EXPECTED_ADJUDICATION_SHA256,
            "3e08d7a3c1c6db53a31ad0e023f9957e8f1b604a0e3c4e91b1b525c7400acd5f",
        )

        commit_bytes = {}
        for name in sorted(expected):
            relative_path = (
                Path("wiki")
                / "survey"
                / "current"
                / "data"
                / "schema-v3"
                / "sidecars"
                / name
            ).as_posix()
            result = subprocess.run(
                [
                    "git",
                    "show",
                    f"{finalizer.SOURCE_HEAD}:{relative_path}",
                ],
                cwd=finalizer.REPO_ROOT,
                capture_output=True,
                check=True,
            )
            commit_bytes[name] = result.stdout

        commit_hashes = {
            name: hashlib.sha256(data).hexdigest()
            for name, data in commit_bytes.items()
        }
        fresh_rendered = dict(
            migration._render_outputs(migration.build_outputs(migration.SOURCE_DIR))
        )
        fresh_hashes = {
            name: hashlib.sha256(data).hexdigest()
            for name, data in fresh_rendered.items()
        }
        self.assertEqual(expected, commit_hashes)
        self.assertEqual(expected, fresh_hashes)
        self.assertEqual(fresh_rendered, commit_bytes)
        finalized = finalizer.finalize_outputs(
            migration.build_outputs(migration.SOURCE_DIR),
            finalizer.ADJUDICATION_PATH.read_bytes(),
        )
        self.assertEqual(len(finalized), 8)

    def test_finalizer_uses_the_canonical_row_hash_implementation_for_all_rows(self):
        rows = all_rows(migration.build_outputs(migration.SOURCE_DIR))
        self.assertEqual(len(rows), 11)
        self.assertIs(finalizer.row_hash, canonical_row_hash)
        self.assertEqual(
            [finalizer.row_hash(row) for row in rows],
            [canonical_row_hash(row) for row in rows],
        )

    def test_importing_finalizer_does_not_leak_resource_warnings(self):
        result = subprocess.run(
            [
                sys.executable,
                "-W",
                "always::ResourceWarning",
                "-c",
                "import sf_schema_v3_finalize",
            ],
            cwd=Path(__file__).parent,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")

    def test_wrong_reviewer_source_status_and_summary_counts_are_rejected(self):
        cases = (
            (("artifact_id",), "wrong-artifact", "artifact_id"),
            (("schema",), "wrong-schema", "schema"),
            (("reviewer_id",), "other", "reviewer_id"),
            (("reviewer_id",), "", "reviewer_id"),
            (("source_head",), "0" * 40, "source_head"),
            (("summary", "status"), "DISAGREEMENTS_FOUND", "summary.*status"),
            (("summary", "agree"), 69, "summary.*agree"),
            (("summary", "disagree"), 1, "summary.*disagree"),
            (("summary", "anchor_agree"), 5, "summary.*anchor_agree"),
            (("summary", "anchor_disagree"), 1, "summary.*anchor_disagree"),
            (("summary", "disagree"), False, "summary.*disagree"),
        )
        for path, value, pattern in cases:
            with self.subTest(path=path, value=value):
                artifact = self.load_artifact()
                target = artifact
                for key in path[:-1]:
                    target = target[key]
                target[path[-1]] = value
                self.assert_rejected(artifact, pattern)

    def test_disagree_duplicate_missing_extra_and_malformed_binding_rows_rejected(self):
        mutations = []

        disagree = self.load_artifact()
        disagree["binding_verdicts"][0]["verdict"] = "DISAGREE"
        mutations.append((disagree, "verdict"))

        duplicate = self.load_artifact()
        duplicate["binding_verdicts"][-1] = copy.deepcopy(
            duplicate["binding_verdicts"][0]
        )
        mutations.append((duplicate, "duplicate"))

        missing = self.load_artifact()
        missing["binding_verdicts"].pop()
        mutations.append((missing, "70|missing"))

        extra = self.load_artifact()
        extra["binding_verdicts"].append(
            {
                **copy.deepcopy(extra["binding_verdicts"][0]),
                "field": "unknown_field",
            }
        )
        mutations.append((extra, "70|unknown|extra"))

        malformed = self.load_artifact()
        malformed["binding_verdicts"][0]["unexpected"] = True
        mutations.append((malformed, "keys|extra"))

        for artifact, pattern in mutations:
            with self.subTest(pattern=pattern):
                self.assert_rejected(artifact, pattern)

    def test_binding_value_and_kind_mismatch_are_rejected(self):
        value_mismatch = self.load_artifact()
        value_mismatch["binding_verdicts"][0]["encoded_value"] = True
        self.assert_rejected(value_mismatch, "encoded_value")

        kind_mismatch = self.load_artifact()
        kind_mismatch["binding_verdicts"][0]["evidence_kind"] = "canon"
        self.assert_rejected(kind_mismatch, "evidence_kind")

    def test_anchor_mismatch_count_duplicate_and_extra_are_rejected(self):
        mismatch = self.load_artifact()
        mismatch["anchor_verdicts"][0]["new_locator"] += " drift"
        self.assert_rejected(mismatch, "anchor.*unknown|anchor.*mismatch")

        count = self.load_artifact()
        count["anchor_verdicts"][0]["occurrences"] = 1
        self.assert_rejected(count, "occurrences")

        duplicate = self.load_artifact()
        duplicate["anchor_verdicts"][-1] = copy.deepcopy(
            duplicate["anchor_verdicts"][0]
        )
        self.assert_rejected(duplicate, "duplicate")

        extra = self.load_artifact()
        extra["anchor_verdicts"].append(copy.deepcopy(extra["anchor_verdicts"][0]))
        self.assert_rejected(extra, "6|duplicate|extra")

    def test_missing_initial_review_and_resolution_log_rows_are_rejected(self):
        missing_initial = self.load_artifact()
        del missing_initial["initial_review"]
        self.assert_rejected(missing_initial, "initial_review|keys")

        missing_resolution = self.load_artifact()
        missing_resolution["resolution_log"].pop()
        self.assert_rejected(missing_resolution, "13")

        empty_resolution = self.load_artifact()
        empty_resolution["resolution_log"][0]["actual_repair"] = ""
        self.assert_rejected(empty_resolution, "resolution_log.*non-empty")

        empty_resolution_detail = self.load_artifact()
        empty_resolution_detail["resolution_log"][0]["tuple"]["field"] = ""
        self.assert_rejected(
            empty_resolution_detail, "resolution_log.*tuple.*non-empty"
        )

    def test_write_is_repeatable_utf8_lf_and_check_is_no_write(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "sidecars"
            finalizer.write_finalized_outputs(output_dir=output_dir)
            first = {
                path.name: path.read_bytes()
                for path in sorted(output_dir.glob("*.sidecar.json"))
            }
            self.assertEqual(len(first), 8)
            for data in first.values():
                self.assertNotIn(b"\r", data)
                self.assertTrue(data.endswith(b"\n"))
                data.decode("utf-8")

            finalizer.write_finalized_outputs(output_dir=output_dir)
            second = {
                path.name: path.read_bytes()
                for path in sorted(output_dir.glob("*.sidecar.json"))
            }
            self.assertEqual(second, first)

            before = copy.deepcopy(second)
            finalizer.check_finalized_outputs(output_dir=output_dir)
            after = {
                path.name: path.read_bytes()
                for path in sorted(output_dir.glob("*.sidecar.json"))
            }
            self.assertEqual(after, before)

    def test_check_rejects_byte_drift_and_stale_destinations_without_writing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "sidecars"
            finalizer.write_finalized_outputs(output_dir=output_dir)
            target = sorted(output_dir.glob("*.sidecar.json"))[0]
            target.write_bytes(target.read_bytes() + b" ")
            drifted = target.read_bytes()

            with self.assertRaisesRegex(finalizer.FinalizationError, "drift"):
                finalizer.check_finalized_outputs(output_dir=output_dir)
            self.assertEqual(target.read_bytes(), drifted)

            stale = output_dir / "stale.sidecar.json"
            stale.write_bytes(b"stale\n")
            with self.assertRaisesRegex(finalizer.FinalizationError, "unexpected"):
                finalizer.check_finalized_outputs(output_dir=output_dir)
            self.assertEqual(stale.read_bytes(), b"stale\n")

    def test_cli_modes_and_exact_success_line(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "sidecars"
            stdout = io.StringIO()
            stderr = io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                self.assertEqual(
                    finalizer.main(["--write"], output_dir=output_dir), 0
                )
            self.assertEqual(stdout.getvalue(), finalizer.SUCCESS_LINE + "\n")
            self.assertEqual(stderr.getvalue(), "")

            stdout = io.StringIO()
            stderr = io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                self.assertEqual(
                    finalizer.main(["--check"], output_dir=output_dir), 0
                )
            self.assertEqual(stdout.getvalue(), finalizer.SUCCESS_LINE + "\n")
            self.assertEqual(stderr.getvalue(), "")

    def test_real_artifact_finalizes_to_committed_bytes(self):
        rendered = dict(
            migration._render_outputs(finalizer.build_finalized_outputs())
        )
        self.assertEqual(set(rendered), finalizer.EXPECTED_DESTINATION_NAMES)
        for name, data in rendered.items():
            self.assertEqual(
                data,
                (finalizer.OUTPUT_DIR / name).read_bytes(),
                f"committed finalized drift: {name}",
            )


if __name__ == "__main__":
    unittest.main()
