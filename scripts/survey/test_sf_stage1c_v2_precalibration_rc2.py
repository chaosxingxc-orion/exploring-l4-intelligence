#!/usr/bin/env python3
"""Acceptance tests for the bounded Stage-1C v2 pre-calibration RC2 repair."""

from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path
from unittest import mock

from jsonschema import Draft202012Validator, ValidationError

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import sf_stage1c_v2_calibration_agreement as agreement
    import sf_stage1c_v2_precalibration_rc2 as rc2
else:
    from scripts.survey import sf_stage1c_v2_calibration_agreement as agreement
    from scripts.survey import sf_stage1c_v2_precalibration_rc2 as rc2


class Stage1CV2PrecalibrationRC2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.package = rc2.build_package()
        cls.report = rc2.build_report(cls.package)

    def test_response_schema_is_the_single_typed_contract(self) -> None:
        schema = self.package["response_schema"]
        Draft202012Validator.check_schema(schema)
        self.assertEqual("sf-stage1c-v2-calibration-response-schema-v2", schema["$id"])
        self.assertGreater(rc2.count_enum_values(schema), 40)
        self.assertEqual(
            schema["$id"], self.package["blind_packet"]["calibration_response_schema_id"]
        )
        self.assertEqual(
            schema["$id"], self.package["agreement"]["calibration_response_schema_id"]
        )
        for field in self.package["agreement"]["critical_response_paths"]:
            self.assertTrue(rc2.schema_path_exists(schema, field), field)

    def test_response_schema_rejects_free_strings_and_accepts_blank_template(self) -> None:
        schema = self.package["response_schema"]
        validator = Draft202012Validator(schema)
        template = copy.deepcopy(self.package["blind_packet"]["items"][0]["blank_response"])
        validator.validate(template)
        broken = copy.deepcopy(template)
        broken["paper_labels"]["paper_role"] = "INVENTED_ROLE"
        with self.assertRaises(ValidationError):
            validator.validate(broken)

    def test_agentic_scope_schema_and_blank_response_are_typed(self) -> None:
        schema = self.package["response_schema"]
        paper_labels = schema["$defs"]["paper_labels"]
        self.assertIn("agentic_scope", paper_labels["required"])
        agentic = paper_labels["properties"]["agentic_scope"]
        self.assertEqual(
            {
                "scope_status", "loop_components", "core_dependency",
                "capability_assets", "control_role", "scope_reason",
            },
            set(agentic["required"]),
        )
        self.assertIn(
            "OUT_OF_SCOPE_SPECIALIZED_SYSTEM",
            agentic["properties"]["scope_status"]["enum"],
        )
        problem_enum = paper_labels["properties"]["problem_nodes"]["items"]["enum"]
        self.assertNotIn("INTERACTIVE_FULL_DUPLEX_OBJECTIVES", problem_enum)

        template = copy.deepcopy(self.package["blind_packet"]["items"][0]["blank_response"])
        Draft202012Validator(schema).validate(template)
        self.assertEqual("NOT_CODED", template["paper_labels"]["agentic_scope"]["scope_status"])
        broken = copy.deepcopy(template)
        broken["paper_labels"]["agentic_scope"]["scope_status"] = "AGENTIC_IF_WE_SAY_SO"
        with self.assertRaises(ValidationError):
            Draft202012Validator(schema).validate(broken)

        critical = set(self.package["agreement"]["critical_response_paths"])
        self.assertTrue({
            "paper_labels.agentic_scope.scope_status",
            "paper_labels.agentic_scope.loop_components",
            "paper_labels.agentic_scope.core_dependency",
            "paper_labels.agentic_scope.capability_assets",
            "paper_labels.agentic_scope.control_role",
            "run_cells[].primary_intervention_axis",
        } <= critical)

    def test_mapping_schema_bundle_types_categorical_and_scope_fields(self) -> None:
        bundle = self.package["schema_bundle"]
        Draft202012Validator.check_schema(bundle)
        self.assertGreater(rc2.count_enum_values(bundle), 35)
        self.assertEqual(
            set(rc2.rc1.CLAIM_SCOPE_FIELDS),
            set(bundle["$defs"]["claim_record"]["properties"]["scope"]["required"]),
        )
        self.assertIn("null", bundle["$defs"]["review_event"]["properties"]["prior_event_id"]["type"])
        for name, definition in bundle["$defs"].items():
            self.assertFalse(definition.get("additionalProperties", True), name)

        claim_validator = Draft202012Validator({
            "$schema": bundle["$schema"], "$ref": "#/$defs/claim_record",
            "$defs": bundle["$defs"],
        })
        claim = {
            "claim_id": "CLM-TEST", "object_type": "SCOPED_CLAIM_INSTANCE",
            "claim_text": "A bounded test proposition.", "claim_origin": "FAMILY_SYNTHESIS",
            "scope": {field: "TEST-STRATUM" for field in rc2.rc1.CLAIM_SCOPE_FIELDS},
            "evidence_relation": "SUPPORT", "evidence_state": "PARTIALLY_SUPPORTED",
            "project_status": "RESIDUAL_HYPOTHESIS_NOT_NOVELTY_VERDICT",
            "source_locator_ids": ["LOC-TEST-1"],
        }
        claim_validator.validate(claim)
        del claim["scope"]["evaluator"]
        with self.assertRaises(ValidationError):
            claim_validator.validate(claim)

    def test_full_mapping_schema_fails_closed_for_specialized_systems(self) -> None:
        paper_audit = self.package["schema_bundle"]["$defs"]["paper_audit"]
        self.assertTrue(
            {"agentic_scope_status", "branch_eligibility"} <= set(paper_audit["required"])
        )
        self.assertIn(
            "INELIGIBLE_SPECIALIZED_SYSTEM",
            paper_audit["properties"]["branch_eligibility"]["enum"],
        )
        self.assertEqual(
            "SPECIALIZED_SYSTEM_EXCLUSION_CANNOT_ENTER_CORE_MEMBER_OR_BRANCH_PRIMARY",
            self.package["schema_bundle"]["specialized_system_branch_gate"],
        )

    def test_run_cell_has_one_typed_primary_intervention(self) -> None:
        run_cell = self.package["response_schema"]["$defs"]["run_cell"]
        self.assertIn("primary_intervention_axis", run_cell["required"])
        axis = run_cell["properties"]["primary_intervention_axis"]
        self.assertEqual("string", axis["type"])
        self.assertNotIn("NOT_CODED", axis["enum"])
        broken = copy.deepcopy(self.package["blind_packet"]["items"][0]["blank_response"])
        broken["run_cells"] = [{
            "object_match_key": "table-1-row-a",
            "run_cell_id": "RC-TEST-1",
            "dataset_node_ids": ["DS-TEST-1"],
            "model": "fixture-model",
            "access_regime": "TF_STRICT_BLACK_BOX",
            "input_condition": "audio question",
            "intervention": "tool routing",
            "primary_intervention_axis": ["D0_SYSTEM_HARNESS", "D2_SKILL"],
            "control_signal": "tool result",
            "decision_or_action": "route",
            "budget_horizon": "one turn",
            "baseline_role": "INTERVENTION",
            "source_locator_ids": [],
        }]
        with self.assertRaises(ValidationError):
            Draft202012Validator(self.package["response_schema"]).validate(broken)

    def test_packet_calibrates_paper_and_object_level_mapping(self) -> None:
        packet = self.package["blind_packet"]
        self.assertEqual(56, len(packet["items"]))
        required_arrays = {
            "run_cells", "observations", "paired_comparisons", "dataset_nodes",
            "dataset_edges", "claim_decisions",
            "translation_or_compatibility_decisions", "source_locators", "review_events",
        }
        for item in packet["items"]:
            response = item["blank_response"]
            self.assertTrue(required_arrays <= set(response))
            self.assertTrue(all(isinstance(response[name], list) for name in required_arrays))
            self.assertEqual(
                set(rc2.CALIBRATED_OBJECT_ARRAYS), set(response["object_absence_reasons"])
            )

    def test_source_byte_manifest_binds_exact_input_for_all_56_items(self) -> None:
        source_manifest = self.package["source_manifest"]
        self.assertEqual(56, source_manifest["N"])
        self.assertEqual(56, len(source_manifest["items"]))
        self.assertEqual(56, len({row["canonical_id"] for row in source_manifest["items"]}))
        self.assertTrue(rc2.verify_source_manifest(source_manifest))
        for row in source_manifest["items"]:
            self.assertTrue(row["source_revision"])
            self.assertEqual("PDF", row["primary_rendition"]["kind"])
            self.assertRegex(row["primary_rendition"]["sha256"], r"^[0-9a-f]{64}$")
            self.assertTrue(row["ledger_binding"])
        by_id = {row["canonical_id"]: row for row in source_manifest["items"]}
        self.assertEqual("arXiv:2510.07838v2", by_id["arxiv:2510.07838"]["source_revision"])
        self.assertEqual("arXiv:2512.14865v1", by_id["arxiv:2512.14865"]["source_revision"])

    def test_agentic_sample_replaces_fdb_v3_without_changing_denominators(self) -> None:
        calibration = self.package["calibration_manifest"]
        ids = set(calibration["canonical_ids"])
        sentinel_ids = {row["canonical_id"] for row in calibration["inherited_sentinels"]}
        self.assertEqual(56, calibration["N"])
        self.assertEqual(38, len(calibration["overlay_ids"]))
        self.assertEqual(18, len(calibration["inherited_sentinels"]))
        self.assertIn("arxiv:2510.07838", ids)
        self.assertIn("arxiv:2512.23646", ids)
        self.assertIn("arxiv:2512.23646", sentinel_ids)
        self.assertNotIn("arxiv:2604.04847", ids)
        self.assertNotIn("arxiv:2604.04847", sentinel_ids)
        source_ids = {row["canonical_id"] for row in self.package["source_manifest"]["items"]}
        self.assertEqual(ids, source_ids)

    def test_synthesis_centres_are_templates_not_load_bearing_claims(self) -> None:
        registry = self.package["claim_templates"]
        self.assertEqual(13, len(registry["claim_templates"]))
        self.assertEqual([], registry["scoped_claim_instances"])
        self.assertTrue(all(row["object_type"] == "CLAIM_TEMPLATE" for row in registry["claim_templates"]))
        self.assertTrue(all(row["load_bearing"] is False for row in registry["claim_templates"]))
        self.assertEqual(
            "MERGE_ONLY_SCOPE_COMPATIBLE_AND_PROPOSITION_EQUIVALENT_INSTANCES",
            registry["scoped_instance_merge_rule"],
        )

    def test_agreement_contract_declares_denominators_gates_and_stop_rule(self) -> None:
        contract = self.package["agreement"]
        self.assertEqual("EXACT_SET_MATCH", contract["multilabel_gate_metric"])
        self.assertEqual("INCLUDE_AS_VALID_LABEL", contract["unknown_denominator_rule"])
        self.assertEqual(
            "EXCLUDE_ONLY_WHEN_BOTH_CODERS_SELECT_NOT_APPLICABLE",
            contract["not_applicable_denominator_rule"],
        )
        self.assertEqual("NOT_CALIBRATED", contract["zero_positive_category_status"])
        self.assertEqual("EXACT_OBJECT_MATCH_KEY_WITHIN_PAPER_AND_TYPE", contract["object_matching_rule"])
        self.assertEqual("STOP_AND_RETURN_TO_INDEPENDENT_REVIEW", contract["second_round_failure_action"])

    def test_agreement_engine_fails_object_undersegmentation_and_marks_empty_types(self) -> None:
        left = agreement.synthetic_response(run_cell_keys=["table-1-row-a", "table-1-row-b"])
        right = agreement.synthetic_response(run_cell_keys=["table-1-row-a"])
        result = agreement.compute_agreement([left], [right], minimum=0.85)
        self.assertAlmostEqual(2 / 3, result["object_level"]["run_cells"]["segmentation_f1"])
        self.assertEqual("FAIL", result["object_level"]["run_cells"]["gate_status"])
        self.assertEqual("NOT_CALIBRATED", result["object_level"]["observations"]["gate_status"])

    def test_agreement_denominator_excludes_only_bilateral_not_applicable(self) -> None:
        left = agreement.synthetic_response()
        right = agreement.synthetic_response()
        left["paper_labels"]["intervention_axes"] = ["NOT_APPLICABLE"]
        right["paper_labels"]["intervention_axes"] = ["NOT_APPLICABLE"]
        result = agreement.compute_agreement([left], [right])
        self.assertEqual(0, result["paper_level"]["intervention_axes"]["denominator"])
        self.assertEqual("NOT_CALIBRATED", result["paper_level"]["intervention_axes"]["gate_status"])

        right["paper_labels"]["intervention_axes"] = ["D0_SYSTEM_HARNESS"]
        result = agreement.compute_agreement([left], [right])
        self.assertEqual(1, result["paper_level"]["intervention_axes"]["denominator"])
        self.assertEqual("FAIL", result["paper_level"]["intervention_axes"]["gate_status"])

    def test_agreement_engine_rejects_mismatched_papers_and_duplicate_object_keys(self) -> None:
        left = agreement.synthetic_response(run_cell_keys=["table-1-row-a", "table-1-row-a"])
        right = agreement.synthetic_response(run_cell_keys=["table-1-row-a"])
        with self.assertRaises(agreement.AgreementError):
            agreement.compute_agreement([left], [right])
        other = agreement.synthetic_response()
        other["paper_id"] = "arxiv:other"
        with self.assertRaises(agreement.AgreementError):
            agreement.compute_agreement([agreement.synthetic_response()], [other])

    def test_agentic_scope_is_in_paper_level_exact_agreement(self) -> None:
        left = agreement.synthetic_response()
        right = agreement.synthetic_response()
        right["paper_labels"]["agentic_scope"]["scope_status"] = "TRANSFER_ANALOGUE"
        result = agreement.compute_agreement([left], [right])
        self.assertEqual(
            "FAIL", result["paper_level"]["agentic_scope.scope_status"]["gate_status"]
        )
        self.assertIn("agentic_scope.loop_components", result["paper_level"])

    def test_completed_response_validator_rejects_not_coded_or_unexplained_empty_arrays(self) -> None:
        schema = self.package["response_schema"]
        blank = copy.deepcopy(self.package["blind_packet"]["items"][0]["blank_response"])
        with self.assertRaises(rc2.ContractError):
            rc2.validate_completed_response(blank, schema)

        blank["response_status"] = "CODER_SUBMITTED"
        blank["coder_id"] = "CODER-A"
        blank["response_id"] = "RESP-A-1"
        blank["paper_labels"] = {
            "paper_disposition": "NON_EMPIRICAL_EVIDENCE_ONLY",
            "paper_role": "BOUNDARY",
            "problem_nodes": ["UNROUTED"],
            "intervention_axes": ["NOT_APPLICABLE"],
            "mm_level": "MM0_TEXT_ONLY",
            "reference_borrow_reproduce": "REFERENCE",
            "access_regime": "INSTRUMENT_ONLY",
            "empirical_experiment_present": False,
            "agentic_scope": {
                "scope_status": "REFERENCE_ONLY_BOUNDARY",
                "loop_components": ["NONE"],
                "core_dependency": "MIXED_OR_UNCLEAR",
                "capability_assets": ["NONE"],
                "control_role": "NONE",
                "scope_reason": "Non-empirical boundary evidence.",
            },
        }
        with self.assertRaises(rc2.ContractError):
            rc2.validate_completed_response(blank, schema)

    def test_completed_response_enforces_agentic_semantics(self) -> None:
        schema = self.package["response_schema"]
        response = copy.deepcopy(self.package["blind_packet"]["items"][0]["blank_response"])
        response.update({
            "response_status": "CODER_SUBMITTED",
            "response_id": "RESP-A-1",
            "coder_transaction_id": "TX-A",
            "coder_id": "CODER-A",
            "source_locators": [{
                "locator_id": "LOC-TEST-1", "rendition_id": "SRC-TEST-PDF",
                "anchor_type": "PAGE", "anchor_value": "1",
                "precise_locator": "Page 1, scope statement.",
            }],
            "review_events": [{
                "event_id": "REV-TEST-1", "event_type": "CODER_SUBMISSION",
                "timestamp": "2026-07-24T00:00:00Z", "prior_event_id": None,
            }],
        })
        response["object_absence_reasons"] = {
            name: "NOT_APPLICABLE_NON_EMPIRICAL" for name in rc2.CALIBRATED_OBJECT_ARRAYS
        }
        response["paper_labels"] = {
            "paper_disposition": "OUT_OF_SCOPE_WITH_REASON",
            "paper_role": "BOUNDARY",
            "problem_nodes": ["UNROUTED"],
            "intervention_axes": ["NOT_APPLICABLE"],
            "mm_level": "MM2_MULTIMODAL_ASSET",
            "reference_borrow_reproduce": "REFERENCE",
            "access_regime": "INSTRUMENT_ONLY",
            "empirical_experiment_present": False,
            "agentic_scope": {
                "scope_status": "OUT_OF_SCOPE_SPECIALIZED_SYSTEM",
                "loop_components": ["OBSERVE", "DECIDE", "ACT_OR_TOOL"],
                "core_dependency": "SPECIALIZED_MODEL_REQUIRED",
                "capability_assets": ["NONE"],
                "control_role": "NONE",
                "scope_reason": "Requires a specialized duplex core.",
            },
        }
        rc2.validate_completed_response(response, schema)

        direct_without_loop = copy.deepcopy(response)
        direct_without_loop["paper_labels"]["paper_disposition"] = "EMPIRICAL_EXTRACTABLE"
        direct_without_loop["paper_labels"]["paper_role"] = "DIRECT_METHOD"
        direct_without_loop["paper_labels"]["agentic_scope"].update({
            "scope_status": "DIRECT_AGENTIC",
            "loop_components": ["OBSERVE", "EVALUATE"],
            "core_dependency": "GENERIC_FROZEN_CORE",
            "control_role": "TRAINING_FREE_NON_REWARD_AGENTIC",
            "scope_reason": "Purported agentic loop.",
        })
        with self.assertRaises(rc2.ContractError):
            rc2.validate_completed_response(direct_without_loop, schema)

        specialized_direct = copy.deepcopy(direct_without_loop)
        specialized_direct["paper_labels"]["agentic_scope"].update({
            "loop_components": ["OBSERVE", "DECIDE", "ACT_OR_TOOL"],
            "core_dependency": "SPECIALIZED_MODEL_REQUIRED",
        })
        with self.assertRaises(rc2.ContractError):
            rc2.validate_completed_response(specialized_direct, schema)

    def test_coder_intake_blocks_distribution_until_real_independence_is_bound(self) -> None:
        coder = self.package["coder_transaction"]
        self.assertEqual("PREPARED_NOT_DISTRIBUTED", coder["status"])
        self.assertFalse(coder["distribution_authorized"])
        self.assertEqual("UNASSIGNED", coder["coder_slots"][0]["assignment_status"])
        self.assertEqual("gpt-5.6-sol", coder["coder_slots"][0]["planned_model"])
        self.assertEqual("gpt-5.6-terra", coder["coder_slots"][1]["planned_model"])
        self.assertEqual("HUMAN_DOMAIN_EXPERT_REQUIRED", coder["adjudicator"]["requirement"])
        self.assertTrue(coder["same_model_runs_are_not_automatically_independent"])

    def test_coder_visible_distribution_excludes_reviewer_only_leakage(self) -> None:
        distribution = self.package["distribution_manifest"]
        names = tuple(row["artifact_name"] for row in distribution["artifacts"])
        self.assertEqual(rc2.CODER_DISTRIBUTION_ALLOWED_ARTIFACTS, names)
        self.assertTrue({
            "calibration_manifest", "claim_templates", "reproduction_readiness",
            "schema_bundle", "coder_transaction",
        }.isdisjoint(names))
        self.assertEqual([], rc2.scan_coder_bundle_leaks(self.package, names))

    def test_distribution_and_adjudication_mutations_fail_closed(self) -> None:
        mutations = (
            lambda package: package["distribution_manifest"].__setitem__(
                "distribution_authorized", True
            ),
            lambda package: package["distribution_manifest"].__setitem__(
                "identity_binding_separate", False
            ),
            lambda package: package["coder_transaction"]["adjudicator"].__setitem__(
                "assignment_status", "ASSIGNED"
            ),
            lambda package: package["distribution_manifest"].__setitem__(
                "content_bundle_sha256", "0" * 64
            ),
            lambda package: package["distribution_manifest"]["artifacts"][0].__setitem__(
                "sha256", "0" * 64
            ),
            lambda package: package["coder_transaction"].__setitem__(
                "shared_content_bundle_sha256", "0" * 64
            ),
            lambda package: package["coder_transaction"].__setitem__(
                "distribution_authorized", True
            ),
            lambda package: package["coder_transaction"]["coder_slots"][0].__setitem__(
                "assignment_status", "ASSIGNED"
            ),
        )
        with mock.patch.object(rc2, "verify_source_manifest", return_value=True):
            for mutate in mutations:
                with self.subTest(mutate=mutate):
                    broken = copy.deepcopy(self.package)
                    mutate(broken)
                    with self.assertRaises(rc2.ContractError):
                        rc2.validate_package(broken)

    def test_anchor_and_specialized_route_mutations_fail_closed(self) -> None:
        def candidate(package: dict, work_id: str) -> dict:
            return next(
                row for row in package["reproduction_readiness"]["candidates"]
                if row["canonical_work_id"] == work_id
            )

        mutations = (
            lambda package: package["reproduction_readiness"].__setitem__(
                "primary_selection", "PROMOTED_WITHOUT_CALIBRATION"
            ),
            lambda package: package["reproduction_readiness"].__setitem__(
                "fallback_selection", "FORCED_FALLBACK"
            ),
            lambda package: candidate(package, "CW-ARXIV-2509.16971").__setitem__(
                "method_anchor_eligible", True
            ),
            lambda package: candidate(package, "CW-ARXIV-2510.07838").__setitem__(
                "status", "CANDIDATE_NOT_ANCHOR"
            ),
            lambda package: candidate(package, "CW-ARXIV-2512.14865").__setitem__(
                "status", "REPRODUCTION_CANDIDATE"
            ),
            lambda package: candidate(package, "CW-ARXIV-2604.22821").__setitem__(
                "status", "METHOD_ANCHOR"
            ),
            lambda package: candidate(package, "CW-ARXIV-2509.16971").__setitem__(
                "research_execution_performed", True
            ),
        )
        with mock.patch.object(rc2, "verify_source_manifest", return_value=True):
            for mutate in mutations:
                with self.subTest(mutate=mutate):
                    broken = copy.deepcopy(self.package)
                    mutate(broken)
                    with self.assertRaises(rc2.ContractError):
                        rc2.validate_package(broken)

    def test_coder_views_are_neutral_and_complete(self) -> None:
        assignment = self.package["assignment_manifest"]
        self.assertEqual(56, assignment["N"])
        self.assertTrue(assignment["sample_role_hidden"])
        self.assertEqual(56, len(assignment["items"]))

        coder_view = self.package["claim_template_coder_view"]
        full_ids = {
            row["claim_template_id"]
            for row in self.package["claim_templates"]["claim_templates"]
        }
        coder_ids = {row["claim_template_id"] for row in coder_view["claim_templates"]}
        self.assertEqual(full_ids, coder_ids)
        serialized_neutral_guidance = rc2.json_bytes({
            "coder_codebook": self.package["coder_codebook"],
            "claim_template_coder_view": coder_view,
        }).decode("utf-8")
        for forbidden in rc2.CODER_VIEW_FORBIDDEN_NAMED_EXPECTATIONS:
            self.assertNotIn(forbidden.casefold(), serialized_neutral_guidance.casefold())
        serialized_views = rc2.json_bytes({
            "assignment_manifest": assignment,
            "claim_template_coder_view": coder_view,
        }).decode("utf-8")
        self.assertNotIn("origin_work_ids", serialized_views)
        self.assertNotIn("paper_to_template_links", serialized_views)
        self.assertNotIn("selection_rationale", serialized_views)

    def test_leak_scanner_rejects_illegal_mutations(self) -> None:
        names = rc2.CODER_DISTRIBUTION_ALLOWED_ARTIFACTS

        rationale_leak = copy.deepcopy(self.package)
        rationale_leak["assignment_manifest"]["items"][0]["selection_rationale"] = "prior role"
        self.assertTrue(rc2.scan_coder_bundle_leaks(rationale_leak, names))

        label_leak = copy.deepcopy(self.package)
        label_leak["coder_codebook"]["rules"].append("FDB-v2 must be specialized exclusion")
        self.assertTrue(rc2.scan_coder_bundle_leaks(label_leak, names))

        link_leak = copy.deepcopy(self.package)
        link_leak["claim_template_coder_view"]["paper_to_template_links"] = []
        self.assertTrue(rc2.scan_coder_bundle_leaks(link_leak, names))

    def test_shared_bundle_hash_is_identity_independent(self) -> None:
        distribution = self.package["distribution_manifest"]
        names = tuple(row["artifact_name"] for row in distribution["artifacts"])
        self.assertEqual("CODER_VISIBLE_SHARED_CONTENT", distribution["scope"])
        self.assertTrue(distribution["identity_binding_separate"])
        self.assertEqual(
            rc2.coder_bundle_sha256(self.package, names),
            distribution["content_bundle_sha256"],
        )
        coder = self.package["coder_transaction"]
        self.assertEqual(
            distribution["content_bundle_sha256"], coder["shared_content_bundle_sha256"]
        )
        self.assertTrue(all(
            slot["expected_content_bundle_sha256"] == distribution["content_bundle_sha256"]
            for slot in coder["coder_slots"]
        ))
        self.assertTrue(all(slot["assignment_status"] == "UNASSIGNED" for slot in coder["coder_slots"]))
        self.assertFalse(distribution["distribution_authorized"])

    def test_materialized_rc2_package_replays_deterministically(self) -> None:
        replay = rc2.run(write=False)
        self.assertEqual("AGENTIC_RC2_CODER_READY_NOT_DISTRIBUTED", replay["status"])
        self.assertFalse(replay["authority"]["local_commit_created"])
        self.assertFalse(replay["authority"]["independent_review_submitted"])

    def test_read_only_agentic_closure_withholds_anchor_promotion(self) -> None:
        readiness = self.package["reproduction_readiness"]
        self.assertEqual(
            "WITHHELD_PENDING_POST_CALIBRATION_ANCHOR_PROMOTION",
            readiness["primary_selection"],
        )
        self.assertEqual("WITHHELD_NO_FORCED_FALLBACK", readiness["fallback_selection"])
        self.assertEqual(
            ["CW-ARXIV-2509.16971", "CW-ARXIV-2510.02995", "CW-ARXIV-2604.22821"],
            readiness["candidate_priority"][:3],
        )
        by_id = {row["canonical_work_id"]: row for row in readiness["candidates"]}
        self.assertEqual("CANDIDATE_NOT_ANCHOR", by_id["CW-ARXIV-2509.16971"]["status"])
        self.assertEqual(
            "REFERENCE_ONLY_OUT_OF_SCOPE_SPECIALIZED_SYSTEM",
            by_id["CW-ARXIV-2510.07838"]["project_relation"],
        )
        self.assertEqual("REFERENCE_ONLY", by_id["CW-ARXIV-2510.07838"]["status"])
        self.assertFalse(by_id["CW-ARXIV-2510.07838"]["method_anchor_eligible"])
        self.assertEqual(
            "INSTRUMENT_SUPPORT_REFERENCE_ONLY",
            by_id["CW-ARXIV-2512.14865"]["status"],
        )
        self.assertFalse(by_id["CW-ARXIV-2512.14865"]["method_anchor_eligible"])
        self.assertEqual("INSTRUMENT_SUPPORT", by_id["CW-ARXIV-2604.22821"]["status"])
        self.assertFalse(by_id["CW-ARXIV-2604.22821"]["method_anchor_eligible"])
        self.assertTrue(all(row["research_execution_performed"] is False for row in readiness["candidates"]))

    def test_agentic_rc2_is_coder_ready_but_keeps_all_execution_withheld(self) -> None:
        self.assertEqual("AGENTIC_RC2_CODER_READY_NOT_DISTRIBUTED", self.report["status"])
        self.assertEqual(
            rc2.OWNER_AGENTIC_RULING,
            self.report["authority"]["owner_agentic_scope_ruling"],
        )
        self.assertEqual(
            "EXCLUDED_FROM_RESEARCH_REPRODUCTION_AND_BRANCH_ROUTE",
            self.report["authority"]["specialized_duplex_route"],
        )
        self.assertTrue(all(self.report["reviewer_p0_closure"].values()))
        self.assertTrue(all(self.report["reviewer_p1_closure"].values()))
        self.assertFalse(self.report["authority"]["calibration_execution_started"])
        self.assertFalse(self.report["authority"]["coder_distributed"])
        self.assertFalse(self.report["authority"]["agreement_computed"])
        self.assertFalse(self.report["authority"]["full_mapping_signed"])
        self.assertFalse(self.report["authority"]["research_execution_authorized"])

    def test_exact_review_submission_authorization_is_bound_without_distribution(self) -> None:
        token = "AUTHORIZE_STAGE1C_V2_AGENTIC_RC2_REVIEW_SUBMISSION"
        authorization = rc2.OWNER_DIRECTION
        self.assertTrue(authorization.is_file())
        self.assertIn(token, authorization.read_text(encoding="utf-8"))
        self.assertTrue(self.report["authority"]["review_submission_authorized"])
        self.assertFalse(self.report["authority"]["coder_distributed"])
        self.assertEqual(22, rc2.build_review_manifest(self.report)["artifact_count"])


if __name__ == "__main__":
    unittest.main()
