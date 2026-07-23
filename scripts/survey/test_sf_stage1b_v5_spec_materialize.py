#!/usr/bin/env python3
"""Contract for the self-contained Stage-1B v5 release specification."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

import sf_stage1b_v5_spec_materialize as materialize  # noqa: E402


class Stage1BV5SpecMaterializeTests(unittest.TestCase):
    def test_v5_spec_has_closed_denominators_and_no_duplicate_artifact(self):
        base = json.loads((REPO / materialize.BASE_SPEC).read_text(encoding="utf-8"))
        document = materialize.materialize(base)
        self.assertEqual("system-first-stage1b-2026-07-23-v5", document["release_id"])
        self.assertEqual(18, document["denominators"]["eligible_bundle_reconciliation"])
        self.assertEqual(46, document["denominators"]["strict_speech_omni_supplement"])
        self.assertEqual(26, document["denominators"]["direct_control_paths_in_supplement"])
        roles = [row["role"] for row in document["artifacts"]]
        paths = [row["path"] for row in document["artifacts"]]
        self.assertEqual(len(roles), len(set(roles)))
        self.assertEqual(len(paths), len(set(paths)))
        self.assertIn("eligible_bundle_reconciliation", roles)
        self.assertIn("unified_asset_downloader", roles)
        self.assertEqual(36, sum(role.startswith("external_v5_fulltext_") for role in roles))


if __name__ == "__main__":
    unittest.main()
