#!/usr/bin/env python3
"""Focused contract checks for the taxonomy-v6 declaration artifact."""
from __future__ import annotations

import json
import os
import unittest


REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
V5_PATH = os.path.join(
    REPO, "wiki", "survey", "2026-07-19-sf-identity-taxonomy-v5.json"
)
V6_PATH = os.path.join(
    REPO, "wiki", "survey", "current", "data", "identity-taxonomy-v6.json"
)

SEMANTIC_KEYS = [
    "enums",
    "signal_schema",
    "control_edge_schema",
    "signal_use",
    "decision_rights",
    "reward_forms",
    "allowed_relations",
    "allowed_relations_provenance",
    "derived_v5",
    "adjudication_binding",
    "cross_platform_contract",
    "killer_and_acceptance_contract",
    "single_write_pipeline",
]

ROW_CLAIMS = [
    "core_weight_update",
    "external_component_weight_update",
    "controller_program_or_config_optimized_on_labels",
    "human_or_dev_label_model_selection",
    "deployment_label_access",
    "test_item_gold_access",
    "inference_external_new_information",
    "internal_visibility",
    "core_topology",
    "core_native_modality",
    "control_horizon",
    "decision_rights",
    "candidate_pool_exists",
    "selection_policy",
    "selection_object",
    "explicit_candidate_pool_selection",
]

RELEASE_RULE = (
    "active release discovery resolves through "
    "wiki/survey/current/manifest.json; historical bound artifacts remain "
    "available through explicit legacy regression."
)


def _unique_object(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError(f"duplicate JSON key: {key}")
        obj[key] = value
    return obj


def _reject_nonfinite(value):
    raise ValueError(f"non-finite JSON number: {value}")


def load_strict(path):
    with open(path, "rb") as handle:
        text = handle.read().decode("utf-8")
    return json.loads(
        text,
        object_pairs_hook=_unique_object,
        parse_constant=_reject_nonfinite,
    )


class TaxonomyV6ContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.v5 = load_strict(V5_PATH)
        cls.v6 = load_strict(V6_PATH)

    def test_derivation_semantics_are_byte_independent_but_value_equal(self):
        for key in SEMANTIC_KEYS:
            with self.subTest(key=key):
                self.assertEqual(self.v5[key], self.v6[key])
        self.assertIn("derived_v5", self.v6)
        self.assertNotIn("derived_v6", self.v6)

    def test_metadata_declares_only_the_schema_v3_contract_delta(self):
        self.assertEqual(
            "SF-IDENTITY-TAXONOMY-V6-2026-07-19-01",
            self.v6["artifact_id"],
        )
        self.assertEqual(
            "schema-v3: row16 + signal4 + edge2 evidence bindings; "
            "discriminative PDF anchors",
            self.v6["schema"],
        )
        self.assertEqual(
            "UNCHANGED_FROM_TAXONOMY_V5",
            self.v6["derivation_semantics"],
        )

    def test_required_evidence_contract_is_exact(self):
        contract = self.v6["required_evidence_contract"]
        self.assertEqual(
            "Every load-bearing encoded value is field-bound and "
            "source-resolved before derivation.",
            contract["principle"],
        )
        self.assertEqual(
            {
                "row": ROW_CLAIMS,
                "signal": ["form", "source", "lifecycle", "uses"],
                "edge": ["signal_use", "decision_right"],
            },
            contract["claims"],
        )
        self.assertEqual(
            self.v5["required_evidence_contract"]["evidence_kinds"],
            contract["evidence_kinds"],
        )

    def test_release_discovery_uses_current_manifest_and_legacy_regression(self):
        self.assertEqual(RELEASE_RULE, self.v6["release_binding"]["rule"])
        self.assertEqual({"rule"}, set(self.v6["release_binding"]))


if __name__ == "__main__":
    unittest.main()
