from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import sf_stage1c_v2_precalibration_rc2r1 as rc2r1
    import sf_stage1c_v2_calibration_agreement_v3 as agreement_v3
else:
    from scripts.survey import sf_stage1c_v2_precalibration_rc2r1 as rc2r1
    from scripts.survey import sf_stage1c_v2_calibration_agreement_v3 as agreement_v3


class Stage1cV2PrecalibrationRc2r1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.package = rc2r1.build_package()

    def submitted_rows(self, coder_id: str, transaction_id: str) -> list[dict]:
        rows = []
        source_by_id = {
            row["source_item_id"]: row for row in self.package["source_manifest"]["items"]
        }
        for index, item in enumerate(self.package["blind_packet"]["items"], start=1):
            response = copy.deepcopy(item["blank_response"])
            source = source_by_id[item["source_item_id"]]
            response.update({
                "response_status": "CODER_SUBMITTED",
                "response_id": f"RESP-{coder_id}-{index:02d}",
                "coder_transaction_id": transaction_id,
                "coder_id": coder_id,
                "paper_labels": {
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
                        "scope_reason": "Boundary-only calibration fixture.",
                    },
                },
                "source_locators": [{
                    "locator_id": f"LOC-FIXTURE-{index:02d}",
                    "rendition_id": source["primary_rendition"]["rendition_id"],
                    "anchor_type": "PAGE",
                    "anchor_value": "1",
                    "precise_locator": "Page 1, fixture evidence.",
                }],
                "review_events": [{
                    "event_id": f"REV-{coder_id}-{index:02d}",
                    "event_type": "CODER_SUBMISSION",
                    "timestamp": "2026-07-24T12:00:00+08:00",
                    "prior_event_id": None,
                }],
            })
            response["object_absence_reasons"] = {
                name: "NOT_APPLICABLE_NON_EMPIRICAL"
                for name in rc2r1.BASE_CALIBRATED_OBJECT_ARRAYS
            }
            rows.append(response)
        return rows

    def bound_intake(self) -> dict:
        contract = copy.deepcopy(self.package["agreement_intake_contract"])
        contract["status"] = "BOUND_FOR_PRE_ADJUDICATION_AGREEMENT"
        for slot, coder_id, transaction_id, process_id, model in (
            (contract["coder_slots"][0], "CODER-A", "TX-A", "PROC-A", "gpt-5.6-sol"),
            (contract["coder_slots"][1], "CODER-B", "TX-B", "PROC-B", "gpt-5.6-terra"),
        ):
            slot.update({
                "coder_id": coder_id,
                "coder_transaction_id": transaction_id,
                "process_id": process_id,
                "model": model,
                "assignment_status": "FROZEN_SUBMITTED",
                "distribution_receipt_id": f"DIST-{coder_id}",
                "submission_receipt_id": f"SUBMIT-{coder_id}",
            })
        return contract

    def test_package_is_new_rc2r1_release_without_rewriting_rc2(self) -> None:
        self.assertEqual("sf-stage1c-v2-calibration-response-schema-v3", self.package["response_schema"]["$id"])
        self.assertEqual(56, self.package["calibration_manifest"]["N"])
        self.assertTrue(all(
            "system-first-stage1c-v2-precalibration-rc2r1" in path.as_posix()
            for path in rc2r1.ARTIFACT_PATHS.values()
        ))

    def test_agreement_rejects_identical_55_of_56_subset(self) -> None:
        left = self.submitted_rows("CODER-A", "TX-A")[:-1]
        right = self.submitted_rows("CODER-B", "TX-B")[:-1]
        with self.assertRaisesRegex(agreement_v3.AgreementError, "exact N=56"):
            agreement_v3.compute_agreement(
                left, right, intake_contract=self.bound_intake(),
                response_schema=self.package["response_schema"],
            )

    def test_agreement_rejects_wrong_exact_id_set(self) -> None:
        left = self.submitted_rows("CODER-A", "TX-A")
        right = self.submitted_rows("CODER-B", "TX-B")
        left[-1]["paper_id"] = "arxiv:wrong-id"
        with self.assertRaisesRegex(agreement_v3.AgreementError, "canonical paper set"):
            agreement_v3.compute_agreement(
                left, right, intake_contract=self.bound_intake(),
                response_schema=self.package["response_schema"],
            )

    def test_agreement_rejects_not_coded_and_invalid_completed_response(self) -> None:
        left = self.submitted_rows("CODER-A", "TX-A")
        right = self.submitted_rows("CODER-B", "TX-B")
        left[0]["paper_labels"]["paper_role"] = "NOT_CODED"
        with self.assertRaisesRegex(agreement_v3.AgreementError, "completed response"):
            agreement_v3.compute_agreement(
                left, right, intake_contract=self.bound_intake(),
                response_schema=self.package["response_schema"],
            )

    def test_agreement_rejects_same_coder_transaction_or_process(self) -> None:
        left = self.submitted_rows("CODER-A", "TX-A")
        right = self.submitted_rows("CODER-B", "TX-B")
        for field in ("coder_id", "coder_transaction_id", "process_id"):
            with self.subTest(field=field):
                intake = self.bound_intake()
                intake["coder_slots"][1][field] = intake["coder_slots"][0][field]
                with self.assertRaisesRegex(agreement_v3.AgreementError, "distinct"):
                    agreement_v3.compute_agreement(
                        left, right, intake_contract=intake,
                        response_schema=self.package["response_schema"],
                    )

    def test_object_critical_fields_are_gated_individually(self) -> None:
        left = self.submitted_rows("CODER-A", "TX-A")
        right = self.submitted_rows("CODER-B", "TX-B")
        for index, (a, b) in enumerate(zip(left, right), start=1):
            locator = a["source_locators"][0]["locator_id"]
            cell = {
                "object_match_key": f"cell-{index:02d}",
                "run_cell_id": f"RC-FIX-{index:02d}",
                "dataset_node_ids": [f"DS-FIX-{index:02d}"],
                "model": "same-model", "access_regime": "TF_STRICT_BLACK_BOX",
                "input_condition": "same-input", "intervention": "same-intervention",
                "control_signal": "same-signal", "decision_or_action": "same-action",
                "budget_horizon": "same-budget", "baseline_role": "INTERVENTION",
                "primary_intervention_axis": "D2_MULTIMODAL_SKILL",
                "source_locator_ids": [locator],
            }
            a["run_cells"] = [copy.deepcopy(cell)]
            b["run_cells"] = [copy.deepcopy(cell)]
            b["run_cells"][0]["primary_intervention_axis"] = "D3_MULTIMODAL_MEMORY"
            a["object_absence_reasons"]["run_cells"] = "OBJECTS_PRESENT"
            b["object_absence_reasons"]["run_cells"] = "OBJECTS_PRESENT"
        result = agreement_v3.compute_agreement(
            left, right, intake_contract=self.bound_intake(),
            response_schema=self.package["response_schema"],
        )
        gate = result["object_level"]["run_cells"]["critical_field_gates"]["primary_intervention_axis"]
        self.assertEqual(56, gate["denominator"])
        self.assertEqual(0.0, gate["exact_agreement"])
        self.assertEqual("FAIL", gate["gate_status"])

    def test_zero_positive_object_category_is_not_calibrated_and_fails_overall(self) -> None:
        result = agreement_v3.compute_agreement(
            self.submitted_rows("CODER-A", "TX-A"),
            self.submitted_rows("CODER-B", "TX-B"),
            intake_contract=self.bound_intake(),
            response_schema=self.package["response_schema"],
        )
        self.assertEqual("NOT_CALIBRATED", result["object_level"]["run_cells"]["segmentation_gate_status"])
        self.assertEqual("FAIL", result["overall_gate_status"])

    def test_borrow_protocol_requires_complete_translation_and_rejection_evidence(self) -> None:
        response = self.submitted_rows("CODER-A", "TX-A")[0]
        response["paper_labels"]["reference_borrow_reproduce"] = "BORROW_PROTOCOL"
        with self.assertRaisesRegex(rc2r1.ContractError, "BORROW_PROTOCOL"):
            rc2r1.validate_completed_response(response, self.package["response_schema"])

        locator = response["source_locators"][0]["locator_id"]
        response["protocol_transfer_evidence"] = [{
            "object_match_key": "transfer-fixture",
            "transfer_evidence_id": "TR-EVID-FIXTURE",
            "source_domain": "VISION_MULTIMODAL_AGENT",
            "source_protocol": "observe-decide-act",
            "target_speech_omni_variables": ["audio observation", "tool action"],
            "preserved_decision_structure": "observe-decide-act",
            "source_locator_ids": [locator],
            "rejection_condition": "No measurable action effect.",
            "rejection_observable": "Task outcome is unchanged against control.",
            "evidence_status": "COMPLETE",
        }]
        rc2r1.validate_completed_response(response, self.package["response_schema"])

    def test_reproduction_candidate_requires_every_closed_field(self) -> None:
        response = self.submitted_rows("CODER-A", "TX-A")[0]
        response["paper_labels"]["reference_borrow_reproduce"] = "REPRODUCTION_CANDIDATE"
        locator = response["source_locators"][0]["locator_id"]
        complete = {
            "object_match_key": "reproduction-fixture",
            "reproduction_evidence_id": "REPRO-EVID-FIXTURE",
            "task": "fixture-task", "dataset": "fixture-dataset",
            "dataset_revision": "rev-1", "split": "test",
            "official_repo": "https://example.invalid/official",
            "pinned_revision": "abc123", "entrypoint": "eval.py",
            "model_access": "TF_STRICT_BLACK_BOX", "license_terms": "Apache-2.0",
            "evaluator_or_ground_truth": "exact-match",
            "local_asset_state": "LOCAL_READY", "source_locator_ids": [locator],
            "closure_status": "CLOSED", "blockers": [],
        }
        required = set(self.package["response_schema"]["$defs"]["reproduction_evidence"]["required"])
        for missing in sorted(required - {"object_match_key", "reproduction_evidence_id"}):
            with self.subTest(missing=missing):
                broken = copy.deepcopy(response)
                evidence = copy.deepcopy(complete)
                evidence.pop(missing)
                broken["reproduction_evidence"] = [evidence]
                with self.assertRaises(rc2r1.ContractError):
                    rc2r1.validate_completed_response(broken, self.package["response_schema"])
        response["reproduction_evidence"] = [complete]
        rc2r1.validate_completed_response(response, self.package["response_schema"])

    def test_reference_cannot_carry_implicit_transfer_or_reproduction(self) -> None:
        response = self.submitted_rows("CODER-A", "TX-A")[0]
        response["protocol_transfer_evidence"] = [{"object_match_key": "illegal"}]
        with self.assertRaises(rc2r1.ContractError):
            rc2r1.validate_completed_response(response, self.package["response_schema"])

    def test_two_acl_sources_have_independent_official_receipts(self) -> None:
        receipts = self.package["acl_acquisition_receipts"]
        self.assertEqual(2, receipts["N"])
        by_paper = {row["canonical_id"]: row for row in receipts["receipts"]}
        self.assertEqual({
            "acl:2026.acl-long.1615", "acl:2026.findings-eacl.151"
        }, set(by_paper))
        source_by_paper = {
            row["canonical_id"]: row for row in self.package["source_manifest"]["items"]
        }
        for paper_id, receipt in by_paper.items():
            self.assertTrue(receipt["official_record_url"].startswith("https://aclanthology.org/"))
            self.assertEqual("2026-07-24T18:45:00+08:00", receipt["verified_at"])
            self.assertEqual(source_by_paper[paper_id]["primary_rendition"]["sha256"], receipt["local_pdf_sha256"])
            self.assertEqual(source_by_paper[paper_id]["primary_rendition"]["bytes"], receipt["local_pdf_bytes"])
            self.assertEqual(receipt["receipt_id"], source_by_paper[paper_id]["ledger_binding"]["independent_receipt_id"])

    def test_value_leakage_scanner_covers_every_coder_visible_artifact(self) -> None:
        names = rc2r1.CODER_DISTRIBUTION_ALLOWED_ARTIFACTS
        self.assertEqual([], rc2r1.scan_coder_bundle_leaks(self.package, names))
        for name in names:
            with self.subTest(name=name):
                broken = copy.deepcopy(self.package)
                broken[name]["debug_note"] = "AudioGenie-Reasoner must receive the expected label"
                self.assertTrue(rc2r1.scan_coder_bundle_leaks(broken, names))

    def test_report_keeps_every_research_execution_flag_false(self) -> None:
        report = rc2r1.build_report(self.package)
        self.assertEqual("AGENTIC_RC2R1_CODER_READY_NOT_DISTRIBUTED", report["status"])
        for field in (
            "coder_distributed", "agreement_computed", "research_model_called",
            "benchmark_metric_run", "paper_reproduction_run", "prototype_created",
            "full_mapping_signed",
        ):
            self.assertFalse(report["authority"][field])

    def test_materialized_rc2r1_package_replays_deterministically(self) -> None:
        report = rc2r1.run(write=False)
        self.assertEqual("AGENTIC_RC2R1_CODER_READY_NOT_DISTRIBUTED", report["status"])

    def test_package_mutations_fail_closed(self) -> None:
        def candidate(package: dict, work_id: str) -> dict:
            return next(
                row for row in package["reproduction_readiness"]["candidates"]
                if row["canonical_work_id"] == work_id
            )

        mutations = (
            lambda package: package["calibration_manifest"].__setitem__("N", 55),
            lambda package: package["source_manifest"].__setitem__("N", 55),
            lambda package: package["acl_acquisition_receipts"].__setitem__("N", 1),
            lambda package: package["acl_acquisition_receipts"]["receipts"][0].__setitem__("local_pdf_sha256", "0" * 64),
            lambda package: package["distribution_manifest"].__setitem__("distribution_authorized", True),
            lambda package: package["distribution_manifest"].__setitem__("content_bundle_sha256", "0" * 64),
            lambda package: package["distribution_manifest"]["artifacts"][0].__setitem__("sha256", "0" * 64),
            lambda package: package["agreement_intake_contract"].__setitem__("status", "BOUND_FOR_PRE_ADJUDICATION_AGREEMENT"),
            lambda package: package["coder_transaction"].__setitem__("distribution_authorized", True),
            lambda package: candidate(package, "CW-ARXIV-2509.16971").__setitem__("method_anchor_eligible", True),
            lambda package: candidate(package, "CW-ARXIV-2510.07838").__setitem__("status", "CANDIDATE_NOT_ANCHOR"),
            lambda package: candidate(package, "CW-ARXIV-2604.22821").__setitem__("research_execution_performed", True),
        )
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                broken = copy.deepcopy(self.package)
                mutate(broken)
                with self.assertRaises(rc2r1.ContractError):
                    rc2r1.validate_package(broken)

    def test_intake_binding_mutations_fail_before_agreement(self) -> None:
        left = self.submitted_rows("CODER-A", "TX-A")
        right = self.submitted_rows("CODER-B", "TX-B")
        mutations = (
            lambda value: value.__setitem__("schema", "wrong"),
            lambda value: value.__setitem__("status", "PREPARED_NOT_DISTRIBUTED"),
            lambda value: value.__setitem__("N", 55),
            lambda value: value.__setitem__("canonical_paper_ids", value["canonical_paper_ids"][:-1]),
            lambda value: value.__setitem__("items", value["items"][:-1]),
            lambda value: value.__setitem__("content_bundle_sha256", "wrong"),
            lambda value: value.__setitem__("prompt_hash", "wrong"),
            lambda value: value.__setitem__("coder_slots", value["coder_slots"][:1]),
            lambda value: value["coder_slots"][0].__setitem__("assignment_status", "UNASSIGNED"),
            lambda value: value["coder_slots"][0].__setitem__("model", "wrong-model"),
            lambda value: value["coder_slots"][0].__setitem__("expected_content_bundle_sha256", "0" * 64),
            lambda value: value["coder_slots"][0].__setitem__("expected_prompt_hash", "0" * 64),
            lambda value: value["coder_slots"][0].__setitem__("distribution_receipt_id", ""),
        )
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                intake = self.bound_intake()
                mutate(intake)
                with self.assertRaises(agreement_v3.AgreementError):
                    agreement_v3.compute_agreement(
                        left, right, intake_contract=intake,
                        response_schema=self.package["response_schema"],
                    )

    def test_response_binding_mutations_fail_before_metric(self) -> None:
        left = self.submitted_rows("CODER-A", "TX-A")
        right = self.submitted_rows("CODER-B", "TX-B")
        mutations = (
            lambda rows: rows[1].__setitem__("response_id", rows[0]["response_id"]),
            lambda rows: rows[0].__setitem__("coder_id", "CODER-X"),
            lambda rows: rows[0].__setitem__("coder_transaction_id", "TX-X"),
            lambda rows: rows[0].__setitem__("source_manifest_id", "WRONG"),
            lambda rows: rows[0].__setitem__("packet_item_id", "WRONG"),
            lambda rows: rows[0].__setitem__("response_status", "BLANK_NOT_DISTRIBUTED"),
        )
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                broken = copy.deepcopy(left)
                mutate(broken)
                with self.assertRaises(agreement_v3.AgreementError):
                    agreement_v3.compute_agreement(
                        broken, right, intake_contract=self.bound_intake(),
                        response_schema=self.package["response_schema"],
                    )


if __name__ == "__main__":
    unittest.main()
