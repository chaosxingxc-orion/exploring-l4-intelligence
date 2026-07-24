#!/usr/bin/env python3
"""Contract tests for the authorized Stage-1C v2 pre-calibration package."""

from __future__ import annotations

import copy
import json
import unittest

from scripts.survey import sf_stage1c_v2_precalibration as precal


class Stage1CV2PrecalibrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = precal.run(write=False)
        cls.package = precal.load_package()

    def test_stage1b_release_signatures_are_effective_but_later_gates_remain_closed(self) -> None:
        authority = self.report["authority"]
        self.assertEqual("AUTHORIZE_STAGE1C_V2_CALIBRATION_PREPARATION", authority["owner_token"])
        self.assertTrue(authority["capability_delta_signed"])
        self.assertTrue(authority["targeted_anchor_signed"])
        self.assertFalse(authority["full_mapping_signed"])
        self.assertFalse(authority["research_execution_authorized"])

    def test_bootstrap_is_signed_for_calibration_but_not_full_mapping(self) -> None:
        bootstrap = self.package["bootstrap"]
        self.assertEqual(226, bootstrap["counts"]["frozen_base"])
        self.assertEqual(282, bootstrap["counts"]["inherited_union"])
        self.assertEqual(14, bootstrap["counts"]["capability_delta"])
        self.assertEqual(24, bootstrap["counts"]["targeted_overlay"])
        self.assertEqual(320, bootstrap["counts"]["candidate_union"])
        self.assertEqual(320, len(bootstrap["works"]))
        self.assertEqual(320, len({row["canonical_id"] for row in bootstrap["works"]}))
        self.assertEqual("SIGNED_CALIBRATION_INPUT_AWAITING_INDEPENDENT_CODERS", bootstrap["status"])
        self.assertTrue(bootstrap["stage1c_calibration_input"])
        self.assertFalse(bootstrap["stage1c_mapping_input"])
        self.assertTrue(all(row["signed"] for row in bootstrap["release_layers"]))

    def test_release_receipts_bind_each_signature_to_its_reviewed_rc1_bytes(self) -> None:
        receipts = self.package["release_receipts"]
        self.assertEqual(2, len(receipts["releases"]))
        by_layer = {row["layer"]: row for row in receipts["releases"]}
        self.assertEqual(
            "ee8f0564069475f58f9be313a7978db662665d1d379b213d3005507c59dea3a6",
            by_layer["CAPABILITY_DELTA_14"]["review_manifest_sha256"],
        )
        self.assertEqual(
            "d70de83e36b4d2c07ae0ab02506b60269620bd5d5768d6ca7b8366d11818e0e6",
            by_layer["TARGETED_OVERLAY_24"]["review_manifest_sha256"],
        )
        self.assertTrue(all(row["signature_effective"] for row in receipts["releases"]))
        self.assertTrue(all(row["full_mapping_authorized"] is False for row in receipts["releases"]))

    def test_validator_rejects_mapping_or_execution_authority_smuggled_into_release(self) -> None:
        mapping = copy.deepcopy(self.package)
        mapping["bootstrap"]["stage1c_mapping_input"] = True
        with self.assertRaises(precal.ContractError):
            precal.validate_package(mapping)

        execution = copy.deepcopy(self.package)
        execution["release_receipts"]["releases"][0]["research_execution_authorized"] = True
        with self.assertRaises(precal.ContractError):
            precal.validate_package(execution)

    def test_problem_and_intervention_axes_are_crosswalked_but_not_conflated(self) -> None:
        crosswalk = self.package["crosswalk"]
        self.assertEqual(6, len(crosswalk["problem_nodes"]))
        self.assertEqual(5, len(crosswalk["intervention_axes"]))
        self.assertFalse(crosswalk["problem_nodes_are_primary_organization_axis"])
        self.assertTrue(all(row["allowed_intervention_axes"] for row in crosswalk["problem_nodes"]))
        self.assertTrue(all(row["problem_status"] in {"INHERITED_CANDIDATE", "UNRANKED_CANDIDATE"} for row in crosswalk["problem_nodes"]))

    def test_all_fifteen_pending_problem_labels_are_explicitly_routed(self) -> None:
        routing = self.package["pending_problem_routing"]
        self.assertEqual(15, len(routing["routes"]))
        self.assertEqual(15, len({row["canonical_work_id"] for row in routing["routes"]}))
        self.assertTrue(all(row["route_disposition"] != "UNRESOLVED" for row in routing["routes"]))
        self.assertTrue(all(row["candidate_problem_promoted"] is False for row in routing["routes"]))

    def test_claim_registry_deduplicates_all_overlay_papers(self) -> None:
        claims = self.package["claims"]
        overlay_ids = set(self.package["overlay_ids"])
        linked = {link["canonical_work_id"] for link in claims["paper_to_claim_links"]}
        self.assertEqual(38, len(overlay_ids))
        self.assertEqual(overlay_ids, linked)
        self.assertLess(len(claims["claims"]), len(overlay_ids))
        self.assertTrue(all(claim["claim_origin"] in {"PAPER_REPORTED", "CROSS_PAPER_SYNTHESIS"} for claim in claims["claims"]))
        self.assertTrue(all(set(precal.CLAIM_SCOPE_FIELDS) <= set(claim["scope"]) for claim in claims["claims"]))

    def test_claim_validator_rejects_duplicate_claim_ids(self) -> None:
        broken = copy.deepcopy(self.package["claims"])
        broken["claims"].append(copy.deepcopy(broken["claims"][0]))
        with self.assertRaises(precal.ContractError):
            precal.validate_claim_registry(broken, set(self.package["overlay_ids"]))

    def test_eight_old_families_are_only_candidate_protocol_templates(self) -> None:
        templates = self.package["protocol_templates"]
        self.assertEqual(8, len(templates["templates"]))
        self.assertTrue(all(row["status"] == "CANDIDATE_PROTOCOL_TEMPLATE" for row in templates["templates"]))
        self.assertTrue(all(row["may_merge_split_or_remain_unrouted"] for row in templates["templates"]))
        self.assertTrue(all(row["branch_created"] is False for row in templates["templates"]))

    def test_remote_analogues_are_queued_with_rejection_conditions(self) -> None:
        translation = self.package["translation_queue"]
        self.assertGreater(len(translation["contracts"]), 0)
        self.assertTrue(all(row["load_bearing_status"] == "WITHHELD_PENDING_TRANSLATION" for row in translation["contracts"]))
        self.assertTrue(all(row["strongest_transfer_failure"] for row in translation["contracts"]))
        self.assertTrue(all(row["rejection_observation"] for row in translation["contracts"]))

    def test_schemas_cover_whole_package_entities(self) -> None:
        required = {
            "paper_audit", "run_cell", "observation", "paired_comparison", "dataset_node",
            "dataset_lineage_edge", "dataset_relation_edge", "claim_record", "family_record",
            "family_membership", "review_event", "translation_contract",
        }
        self.assertEqual(required, set(self.package["schemas"]["$defs"]))
        self.assertTrue(all(self.package["schemas"]["$defs"][name].get("required") for name in required))

    def test_calibration_manifest_is_exact_and_blind_packet_has_no_prior_labels(self) -> None:
        calibration = self.package["calibration"]
        packet = self.package["blind_packet"]
        ids = calibration["canonical_ids"]
        self.assertEqual("READY_FOR_INDEPENDENT_CODERS_NOT_EXECUTED", calibration["status"])
        self.assertTrue(calibration["two_stage1b_release_signatures_effective"])
        self.assertEqual(56, calibration["N"])
        self.assertEqual(38, calibration["overlay_record_count"])
        self.assertEqual(18, calibration["inherited_sentinel_count"])
        self.assertEqual(56, len(ids))
        self.assertEqual(56, len(set(ids)))
        self.assertEqual(["arxiv:2505.17862"], calibration["outside_candidate_union_calibration_only"])
        self.assertEqual(set(ids), {row["canonical_id"] for row in packet["items"]})
        forbidden = {"role", "primary_direction", "family", "problem_axis", "intervention_axis"}
        self.assertTrue(all(not forbidden & set(row) for row in packet["items"]))

    def test_agreement_and_later_blind_review_contracts_are_separate(self) -> None:
        agreement = self.package["agreement"]
        self.assertEqual(0.85, agreement["minimum_raw_agreement"])
        self.assertEqual(1, agreement["maximum_codebook_consolidations"])
        self.assertTrue(agreement["full_packet_recode_after_consolidation"])
        self.assertEqual(64, agreement["later_full_mapping_blind_review"]["minimum_unique_works"])
        self.assertTrue(agreement["later_full_mapping_blind_review"]["exclude_calibration_records"])

    def test_reproduction_candidates_remain_candidates_not_anchors(self) -> None:
        readiness = self.package["reproduction_readiness"]
        self.assertEqual(5, len(readiness["candidates"]))
        self.assertTrue(all(row["status"] == "CANDIDATE_NOT_ANCHOR" for row in readiness["candidates"]))
        self.assertEqual("WITHHELD_PENDING_READ_ONLY_CLOSURE", readiness["primary_selection"])
        self.assertEqual("WITHHELD_PENDING_READ_ONLY_CLOSURE", readiness["fallback_selection"])

    def test_report_is_deterministic(self) -> None:
        second = precal.run(write=False)
        self.assertEqual(
            json.dumps(self.report, ensure_ascii=False, sort_keys=True),
            json.dumps(second, ensure_ascii=False, sort_keys=True),
        )


if __name__ == "__main__":
    unittest.main()
