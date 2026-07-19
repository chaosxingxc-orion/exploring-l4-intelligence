#!/usr/bin/env python3
"""Focused tests for the deterministic schema-v3 sidecar migration."""

from __future__ import annotations

import copy
import hashlib
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sf_evidence_contract import (  # noqa: E402
    EDGE_REQUIRED_FIELDS,
    ROW_REQUIRED_FIELDS,
    SIGNAL_REQUIRED_FIELDS,
    validate_bound_values,
)
from sf_schema_v3_migrate import (  # noqa: E402
    ABSENCE_SELECTION_NOTE,
    ANCHOR_REPLACEMENTS,
    OUTPUT_DIR,
    SCHEMA_TEXT,
    SCHEMA_V3_BINDING_STATUS,
    SOURCE_DIR,
    SUCCESS_LINE,
    build_outputs,
    main,
    migrate_sidecar,
    replace_anchors,
    write_outputs,
)


ROW14_FIELDS = ROW_REQUIRED_FIELDS[:-2]


def binding(value, kind="canon", quote="claim-bearing quote"):
    return {"value": copy.deepcopy(value), "kind": kind, "quote": quote}


def fixture_sidecar(
    method_path_id="2026.findings-acl.1724#pipeline",
    selection_policy="scored_select",
    selection_object="candidate_output",
    explicit_selection=True,
    edge_locator="canon: 'edge claim quote'",
):
    row = {
        "core_weight_update": False,
        "external_component_weight_update": False,
        "controller_program_or_config_optimized_on_labels": False,
        "human_or_dev_label_model_selection": False,
        "deployment_label_access": False,
        "test_item_gold_access": False,
        "inference_external_new_information": False,
        "internal_visibility": "api_only",
        "core_topology": "single_core",
        "core_native_modality": "text_only",
        "control_horizon": "sequential",
        "decision_rights": ["branch"],
        "candidate_pool_exists": True,
        "selection_policy": selection_policy,
        "selection_object": selection_object,
        "explicit_candidate_pool_selection": explicit_selection,
        "method_path_id": method_path_id,
        "signals": [
            {
                "signal_id": "s1",
                "form": "scalar_score",
                "source": "llm_judge",
                "lifecycle": "online_step",
                "uses": ["prune"],
                "claim_evidence": {
                    "form": binding("scalar_score"),
                    "lifecycle": binding("online_step"),
                    "uses": binding(["prune"]),
                },
            }
        ],
        "control_edges": [
            {
                "signal_id": "s1",
                "signal_use": "prune",
                "decision_right": "branch",
                "source_locator": edge_locator,
            }
        ],
    }
    row["claim_evidence"] = {field: binding(row[field]) for field in ROW14_FIELDS}
    return {
        "schema": "v2",
        "schema_v3_adjudicator": "must-not-survive",
        "method_paths": [row],
    }


class SchemaV3MigrationTest(unittest.TestCase):
    def test_minimal_fixture_has_exact_row16_signal4_edge2_bindings(self):
        source = fixture_sidecar()

        migrated = migrate_sidecar(source)
        row = migrated["method_paths"][0]

        self.assertEqual(list(row["claim_evidence"]), ROW_REQUIRED_FIELDS)
        self.assertEqual(
            list(row["signals"][0]["claim_evidence"]), SIGNAL_REQUIRED_FIELDS
        )
        self.assertEqual(
            list(row["control_edges"][0]["claim_evidence"]),
            EDGE_REQUIRED_FIELDS,
        )
        self.assertEqual(validate_bound_values(row), [])
        self.assertEqual(migrated["schema"], SCHEMA_TEXT)
        self.assertEqual(
            migrated["schema_v3_binding_status"], SCHEMA_V3_BINDING_STATUS
        )
        self.assertNotIn("schema_v3_adjudicator", migrated)

    def test_migration_does_not_mutate_source(self):
        source = fixture_sidecar()
        before = copy.deepcopy(source)

        migrate_sidecar(source)

        self.assertEqual(source, before)

    def test_anchor_replacement_is_recursive_and_counted(self):
        source = {
            "locator": "canon: 'x' (p4 probe)",
            "nested": ["p4 probe", "p5 cost"],
        }
        counts = {key: 0 for key in ANCHOR_REPLACEMENTS}

        migrated = replace_anchors(source, counts)

        self.assertEqual(
            migrated["locator"],
            "canon: 'x' (p4 anchor='create extend probe and prune branches')",
        )
        self.assertEqual(
            migrated["nested"],
            [
                "p4 anchor='create extend probe and prune branches'",
                "p5 anchor='accuracy cost trade off'",
            ],
        )
        self.assertEqual(counts["p4 probe"], 2)
        self.assertEqual(counts["p5 cost"], 1)
        self.assertNotIn("p4 probe", repr(migrated))

    def test_positive_selection_fields_clone_named_existing_binding(self):
        source = fixture_sidecar()
        original = source["method_paths"][0]["claim_evidence"]["selection_policy"]

        row = migrate_sidecar(source)["method_paths"][0]
        selection_object = row["claim_evidence"]["selection_object"]
        explicit_selection = row["claim_evidence"][
            "explicit_candidate_pool_selection"
        ]

        self.assertEqual(selection_object["kind"], original["kind"])
        self.assertEqual(selection_object["quote"], original["quote"])
        self.assertEqual(selection_object["value"], "candidate_output")
        self.assertEqual(explicit_selection["value"], True)
        self.assertIsNot(selection_object, original)
        self.assertIsNot(explicit_selection, original)
        self.assertIsNot(selection_object, explicit_selection)

    def test_absence_selection_fields_bind_actual_values_and_exact_policy_text(self):
        source = fixture_sidecar(
            method_path_id="2604.16529#pdr-random-k",
            selection_policy="random_sample",
            selection_object="none",
            explicit_selection=False,
        )

        row = migrate_sidecar(source)["method_paths"][0]

        for field in ("selection_object", "explicit_candidate_pool_selection"):
            evidence = row["claim_evidence"][field]
            self.assertEqual(evidence["kind"], "absence")
            self.assertEqual(evidence["value"], row[field])
            self.assertEqual(evidence["scope"], "complete pinned method path")
            self.assertEqual(evidence["note"], ABSENCE_SELECTION_NOTE)

    def test_signal_source_clones_form_binding_and_binds_source_value(self):
        row = migrate_sidecar(fixture_sidecar())["method_paths"][0]
        signal = row["signals"][0]

        self.assertEqual(signal["claim_evidence"]["source"]["value"], "llm_judge")
        self.assertEqual(
            signal["claim_evidence"]["source"]["quote"],
            signal["claim_evidence"]["form"]["quote"],
        )
        self.assertIsNot(
            signal["claim_evidence"]["source"],
            signal["claim_evidence"]["form"],
        )

    def test_edge_bindings_extract_canon_or_tex_quoted_locator(self):
        for kind in ("canon", "tex"):
            with self.subTest(kind=kind):
                row = migrate_sidecar(
                    fixture_sidecar(edge_locator=f"{kind}: 'edge claim quote'")
                )["method_paths"][0]
                evidence = row["control_edges"][0]["claim_evidence"]
                for field in EDGE_REQUIRED_FIELDS:
                    self.assertEqual(evidence[field]["kind"], kind)
                    self.assertEqual(evidence[field]["quote"], "edge claim quote")
                    self.assertEqual(
                        evidence[field]["value"], row["control_edges"][0][field]
                    )

    def test_edge_locator_without_canon_or_tex_quote_fails_closed(self):
        source = fixture_sidecar(edge_locator="p4 anchor='edge claim quote'")

        with self.assertRaisesRegex(ValueError, "extract.*canon.*tex.*quote"):
            migrate_sidecar(source)


class SchemaV3IntegrationTest(unittest.TestCase):
    def test_pinned_corpus_has_exact_counts_and_complete_bindings(self):
        outputs = build_outputs(SOURCE_DIR)
        sidecars = [sidecar for _, sidecar in outputs]
        rows = [row for sidecar in sidecars for row in sidecar["method_paths"]]
        signals = [signal for row in rows for signal in row["signals"]]
        edges = [edge for row in rows for edge in row["control_edges"]]

        self.assertEqual(len(sidecars), 8)
        self.assertEqual(len(rows), 11)
        self.assertEqual(len(signals), 12)
        self.assertEqual(len(edges), 18)
        for sidecar in sidecars:
            self.assertEqual(sidecar["schema"], SCHEMA_TEXT)
            self.assertEqual(
                sidecar["schema_v3_binding_status"], SCHEMA_V3_BINDING_STATUS
            )
        for row in rows:
            self.assertEqual(validate_bound_values(row), [])

    def test_all_pinned_anchor_occurrences_are_replaced_and_conserved(self):
        outputs = build_outputs(SOURCE_DIR)
        source_text = "".join(
            path.read_text(encoding="utf-8")
            for path in sorted(SOURCE_DIR.glob("*.sidecar.json"))
        )
        generated_text = "".join(
            json.dumps(sidecar, ensure_ascii=False) for _, sidecar in outputs
        )
        expected_counts = {
            "p4 probe": 2,
            "p5 cost": 1,
            "p3 Algorithm": 1,
            "p8 Fig": 2,
            "p14 delegated": 1,
            "p4 explore": 1,
        }

        self.assertEqual(set(expected_counts), set(ANCHOR_REPLACEMENTS))
        for source, expected_count in expected_counts.items():
            replacement = ANCHOR_REPLACEMENTS[source]
            self.assertEqual(source_text.count(source), expected_count)
            self.assertEqual(generated_text.count(source), 0)
            self.assertEqual(generated_text.count(replacement), expected_count)

    def test_write_outputs_is_stable_lf_utf8_and_matches_committed_outputs(self):
        outputs = build_outputs(SOURCE_DIR)
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "sidecars"
            write_outputs(outputs, output_dir)
            first = {
                path.name: path.read_bytes()
                for path in sorted(output_dir.glob("*.sidecar.json"))
            }

            self.assertEqual(len(first), 8)
            for name, data in first.items():
                self.assertNotIn(b"\r", data, name)
                self.assertTrue(data.endswith(b"\n"), name)
                data.decode("utf-8")
                self.assertEqual(
                    data, (OUTPUT_DIR / name).read_bytes(), f"committed drift: {name}"
                )

            write_outputs(outputs, output_dir)
            second = {
                path.name: path.read_bytes()
                for path in sorted(output_dir.glob("*.sidecar.json"))
            }
            self.assertEqual(second, first)

    def test_build_and_temp_write_leave_pinned_source_bytes_unchanged(self):
        source_paths = sorted(SOURCE_DIR.glob("*.sidecar.json"))
        before_bytes = {path.name: path.read_bytes() for path in source_paths}
        before_hashes = {
            name: hashlib.sha256(data).hexdigest()
            for name, data in before_bytes.items()
        }

        outputs = build_outputs(SOURCE_DIR)
        with tempfile.TemporaryDirectory() as temp_dir:
            write_outputs(outputs, Path(temp_dir) / "sidecars")

        after_bytes = {path.name: path.read_bytes() for path in source_paths}
        after_hashes = {
            name: hashlib.sha256(data).hexdigest()
            for name, data in after_bytes.items()
        }
        self.assertEqual(after_bytes, before_bytes)
        self.assertEqual(after_hashes, before_hashes)

    def test_cli_check_is_injectable_exact_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "must-not-exist"
            stdout = io.StringIO()
            stderr = io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                exit_code = main(
                    ["--check"], source_dir=SOURCE_DIR, output_dir=output_dir
                )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stdout.getvalue(), SUCCESS_LINE + "\n")
            self.assertEqual(stderr.getvalue(), "")
            self.assertFalse(output_dir.exists())

    def test_cli_rejects_both_modes_nonzero(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            with self.assertRaises(SystemExit) as raised:
                main(
                    ["--check", "--write"],
                    source_dir=SOURCE_DIR,
                    output_dir=OUTPUT_DIR,
                )
        self.assertNotEqual(raised.exception.code, 0)
        self.assertIn("not allowed with argument --check", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
