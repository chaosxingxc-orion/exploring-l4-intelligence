#!/usr/bin/env python3
"""Focused contract checks for the taxonomy-v6 declaration artifact."""
from __future__ import annotations

import os
import sys
import tempfile
import unittest


REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sf_json_contract import JsonContractError, read as read_strict_json  # noqa: E402
from sf_taxonomy_v6_contract import (  # noqa: E402
    EXPECTED_ADDED_KEYS,
    EXPECTED_CHANGED_KEYS,
    RELEASE_RULE,
    ROW_CLAIMS,
    SEMANTIC_KEYS,
    validate_taxonomy_v6,
)
V5_PATH = os.path.join(
    REPO, "wiki", "survey", "2026-07-19-sf-identity-taxonomy-v5.json"
)
V6_PATH = os.path.join(
    REPO, "wiki", "survey", "current", "data", "identity-taxonomy-v6.json"
)

EXPECTED_CHANGED_EXISTING_KEYS = set(EXPECTED_CHANGED_KEYS)
EXPECTED_UNION_DELTA = EXPECTED_ADDED_KEYS | EXPECTED_CHANGED_EXISTING_KEYS


def load_strict(path):
    return read_strict_json(path)[0]


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

    def test_reusable_taxonomy_contract_is_clean(self):
        self.assertEqual(validate_taxonomy_v6(self.v5, self.v6), [])

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
        self.assertEqual(
            "identity taxonomy v6 — frozen derivation semantics with "
            "schema-v3 evidence contract",
            self.v6["title"],
        )
        self.assertEqual(
            "v6 supersedes v5 for active release discovery; derivation "
            "semantics unchanged, evidence contract upgraded to schema-v3 "
            "row16 + signal4 + edge2 bindings and discriminative PDF anchors.",
            self.v6["supersession"],
        )

    def test_top_level_delta_is_exhaustively_classified(self):
        v5_keys = set(self.v5)
        v6_keys = set(self.v6)
        added_keys = v6_keys - v5_keys
        removed_keys = v5_keys - v6_keys
        changed_existing = {
            key for key in v5_keys & v6_keys if self.v5[key] != self.v6[key]
        }
        self.assertEqual(EXPECTED_ADDED_KEYS, added_keys)
        self.assertEqual(set(), removed_keys)
        self.assertEqual(EXPECTED_CHANGED_EXISTING_KEYS, changed_existing)
        self.assertEqual(
            EXPECTED_UNION_DELTA,
            added_keys | removed_keys | changed_existing,
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
                "row": list(ROW_CLAIMS),
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

    def test_strict_loader_rejects_malformed_json_classes(self):
        cases = [
            ("duplicate-key", b'{"x": 1, "x": 2}'),
            ("non-finite", b'{"x": NaN}'),
            ("invalid-utf8", b'{"x": "\xff"}'),
            ("trailing-junk", b'{} trailing'),
        ]
        with tempfile.TemporaryDirectory() as temporary:
            for name, payload in cases:
                with self.subTest(name=name):
                    path = os.path.join(temporary, f"{name}.json")
                    with open(path, "wb") as handle:
                        handle.write(payload)
                    with self.assertRaises(JsonContractError):
                        load_strict(path)


if __name__ == "__main__":
    unittest.main()
