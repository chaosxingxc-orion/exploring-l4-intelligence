#!/usr/bin/env python3
"""Contract tests for the Stage-1B capability-delta release candidate."""

from __future__ import annotations

import json
import unittest
from unittest import mock

from scripts.survey import sf_stage1b_capability_delta as delta


class Stage1BCapabilityDeltaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = delta.run(write=False)
        cls.package, cls.records, cls.bindings = delta.validate_records()

    def test_authorized_surface_is_exactly_eight_seeds_and_six_promotions(self) -> None:
        identities = {row["primary_identity"] for row in self.records}
        self.assertEqual(delta.EXPECTED_SEEDS | delta.EXPECTED_PROMOTIONS, identities)
        self.assertEqual(14, len(identities))

    def test_frozen_release_is_preserved_and_candidate_is_unsigned(self) -> None:
        self.assertEqual(delta.FROZEN_RELEASE, self.package["frozen_stage1b_v5_release"])
        self.assertFalse(self.package["frozen_stage1b_v5_mutated"])
        self.assertFalse(self.report["self_signed"])
        self.assertEqual(
            "RELEASE_CANDIDATE_AWAITING_INDEPENDENT_REVIEW",
            self.report["status"],
        )

    def test_reference_borrow_reproduce_contract_has_no_false_anchor(self) -> None:
        relations = {
            row["project_use_contract"]["primary_relation"] for row in self.records
        }
        self.assertEqual({"REFERENCE_CONTEXT", "BORROWED_PROTOCOL_ANALOGUE"}, relations)
        self.assertEqual(0, self.report["surface"]["reproduction_anchors_in_delta"])
        self.assertTrue(
            all(
                row["project_use_contract"]["reproduction_subtype"] is None
                for row in self.records
            )
        )

    def test_all_external_bindings_are_hash_verified(self) -> None:
        self.assertEqual(42, len(self.bindings))
        self.assertTrue(all(len(row["sha256"]) == 64 for row in self.bindings))
        self.assertEqual(
            28,
            self.report["external_bindings"]["ledger"]["target_renditions_verified"],
        )

    def test_identical_ledger_retries_are_retained_without_hash_conflict(self) -> None:
        ledger = self.report["external_bindings"]["ledger"]
        self.assertEqual(0, ledger["conflicting_hashes"])
        self.assertEqual(2, ledger["identical_duplicate_events_retained"]["2405.20834:eprint"])
        self.assertEqual(2, ledger["identical_duplicate_events_retained"]["2602.07624:eprint"])

    def test_canonical_census_is_226_plus_overlay_plus_delta(self) -> None:
        census = delta.build_census(self.records)
        self.assertEqual(226, census["frozen_base"]["count"])
        self.assertEqual(59, census["current_reference_appendix"]["count"])
        self.assertEqual(7, census["current_reference_appendix"]["overlap_with_frozen_base"])
        self.assertEqual(282, census["inherited_canonical_union"])
        self.assertEqual(14, census["capability_delta"]["count"])
        self.assertEqual(296, census["release_candidate_surface"])

    def test_seen_not_promoted_citations_do_not_enter_denominator(self) -> None:
        citation = self.report["citation_expansion"]
        self.assertEqual(303, citation["seen_unique_arxiv_ids"])
        self.assertEqual(6, citation["promoted"])
        self.assertEqual(297, citation["seen_not_promoted"])
        self.assertEqual(296, self.report["surface"]["release_candidate_canonical_surface"])

    def test_windows_resolves_wsl_data_root_semantics(self) -> None:
        configured = "/mnt/e/chao_workspace/exploring-l4-intelligence/speechrl-data"
        with mock.patch.dict(delta.os.environ, {"SPEECHRL_DATA_DIR": configured}), mock.patch.object(
            delta.os, "name", "nt"
        ):
            self.assertEqual(
                "E:/chao_workspace/exploring-l4-intelligence/speechrl-data",
                delta.external_root().as_posix(),
            )

    def test_report_is_deterministic(self) -> None:
        second = delta.run(write=False)
        self.assertEqual(
            json.dumps(self.report, ensure_ascii=False, sort_keys=True),
            json.dumps(second, ensure_ascii=False, sort_keys=True),
        )


if __name__ == "__main__":
    unittest.main()
