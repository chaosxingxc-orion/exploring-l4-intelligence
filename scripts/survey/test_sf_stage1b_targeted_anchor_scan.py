#!/usr/bin/env python3
"""Contract tests for the Stage-1B targeted-anchor literature-scan overlay."""

from __future__ import annotations

import json
import unittest
from unittest import mock

from scripts.survey import sf_stage1b_targeted_anchor_scan as scan


class Stage1BTargetedAnchorScanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = scan.run(write=False)
        cls.package, cls.scan_items, cls.records, cls.bindings = scan.validate_records()

    def test_scan_and_promotion_sets_are_exact(self) -> None:
        self.assertEqual(scan.EXPECTED_SCAN_IDS, {row["arxiv_id"] for row in self.scan_items})
        self.assertEqual(scan.EXPECTED_PROMOTED, {row["primary_identity"] for row in self.records})
        self.assertEqual(
            scan.EXPECTED_NOT_PROMOTED,
            {row["arxiv_id"] for row in self.scan_items if row["disposition"] == "SCANNED_NOT_PROMOTED"},
        )

    def test_fulltext_and_ledger_bindings_are_complete(self) -> None:
        self.assertEqual(78, len(self.bindings))
        self.assertEqual(52, self.report["external_bindings"]["ledger"]["target_renditions_verified"])
        self.assertEqual(0, self.report["external_bindings"]["ledger"]["conflicting_hashes"])

    def test_reference_borrow_reproduce_are_not_conflated(self) -> None:
        relations = {row["project_use_contract"]["primary_relation"] for row in self.records}
        self.assertEqual({"REFERENCE_CONTEXT", "BORROWED_PROTOCOL_ANALOGUE"}, relations)
        self.assertEqual(0, self.report["surface"]["reproduction_anchors"])

    def test_census_keeps_both_unsigned_overlays_separate(self) -> None:
        census = scan.build_census(self.records)
        self.assertEqual(282, census["inherited_current_union"])
        self.assertEqual(306, census["independent_targeted_overlay_surface"])
        self.assertEqual(320, census["combined_unsigned_candidate_union"])
        self.assertFalse(census["signed_release"])
        self.assertFalse(census["stage1c_input"])

    def test_frozen_and_reviewed_bytes_are_declared_unchanged(self) -> None:
        self.assertEqual(scan.FROZEN_RELEASE, self.package["frozen_stage1b_v5_release"])
        self.assertFalse(self.package["frozen_stage1b_v5_mutated"])
        self.assertFalse(self.package["capability_delta_rc1_mutated"])
        self.assertFalse(self.report["self_signed"])
        preserved = self.report["preserved_capability_delta_rc1"]
        self.assertGreater(preserved["artifact_count"], 0)
        self.assertTrue(preserved["all_manifest_artifacts_byte_verified"])

    def test_windows_resolves_wsl_data_root(self) -> None:
        configured = "/mnt/e/chao_workspace/exploring-l4-intelligence/speechrl-data"
        with mock.patch.dict(scan.os.environ, {"SPEECHRL_DATA_DIR": configured}), mock.patch.object(
            scan.os, "name", "nt"
        ):
            self.assertEqual(
                "E:/chao_workspace/exploring-l4-intelligence/speechrl-data",
                scan.external_root().as_posix(),
            )

    def test_report_is_deterministic(self) -> None:
        second = scan.run(write=False)
        self.assertEqual(
            json.dumps(self.report, ensure_ascii=False, sort_keys=True),
            json.dumps(second, ensure_ascii=False, sort_keys=True),
        )


if __name__ == "__main__":
    unittest.main()
