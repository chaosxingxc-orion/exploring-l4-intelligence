#!/usr/bin/env python3
"""Focused tests for the deterministic schema-v3 sidecar migration."""

from __future__ import annotations

import copy
import os
import sys
import unittest


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
    SCHEMA_TEXT,
    SCHEMA_V3_BINDING_STATUS,
    migrate_sidecar,
    replace_anchors,
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


if __name__ == "__main__":
    unittest.main()
