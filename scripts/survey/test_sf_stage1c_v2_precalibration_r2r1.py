from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path
from unittest import mock

from jsonschema import Draft202012Validator, ValidationError

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import sf_stage1c_v2_calibration_agreement_v7 as agreement_v7
    import sf_stage1c_v2_precalibration_r2r1 as r2r1
else:
    from scripts.survey import sf_stage1c_v2_calibration_agreement_v7 as agreement_v7
    from scripts.survey import sf_stage1c_v2_precalibration_r2r1 as r2r1


class Stage1cV2PrecalibrationR2R1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.package = r2r1.build_package()
        cls.source_by_paper = {
            row["canonical_id"]: row for row in cls.package["source_manifest"]["items"]
        }

    def completed_boundary(self, paper_index: int = 0, *, slot: str = "A") -> dict:
        coder = f"CODER-{slot}"
        item = self.package["blind_packet"]["items"][paper_index]
        response = copy.deepcopy(item["blank_response"])
        source = self.source_by_paper[response["paper_id"]]
        response.update({
            "response_status": "CODER_SUBMITTED",
            "response_id": f"RESP-{coder}-{paper_index:02d}",
            "coder_transaction_id": f"TX-CODER-{slot}",
            "coder_id": coder,
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
                    "scope_reason": "Typed boundary fixture.",
                },
            },
            "source_locators": [{
                "locator_id": f"LOC-{coder}-{paper_index:02d}",
                "rendition_id": source["primary_rendition"]["rendition_id"],
                "anchor_type": "PAGE",
                "anchor_value": "1",
                "precise_locator": "Page 1, first contribution paragraph.",
            }],
            "paired_comparison_absence_reason": "NOT_APPLICABLE_NON_EMPIRICAL",
            "review_events": [{
                "event_id": f"REV-{coder}-{paper_index:02d}",
                "event_type": "CODER_SUBMISSION",
                "timestamp": "2026-07-25T12:00:00+08:00",
                "prior_event_id": None,
            }],
        })
        response["object_absence_reasons"] = {
            name: "NOT_APPLICABLE_NON_EMPIRICAL" for name in r2r1.OBJECT_ARRAYS
        }
        return response

    def dataset_node(self, response: dict, object_id: str, name: str = "MMAU") -> dict:
        return {
            "dataset_node_id": object_id,
            "name": name,
            "revision": "paper-reported",
            "split": "test-mini",
            "source_locator_ids": [response["source_locators"][0]["locator_id"]],
        }

    def run_cell(self, response: dict, object_id: str, dataset_id: str) -> dict:
        return {
            "run_cell_id": object_id,
            "dataset_node_ids": [dataset_id],
            "model": "frozen core",
            "access_regime": "TF_STRICT_BLACK_BOX",
            "input_condition": "audio",
            "intervention": "tool routing",
            "control_signal": "task evidence",
            "primary_intervention_axis": "D0_SYSTEM_HARNESS",
            "decision_or_action": "route",
            "budget_horizon": "one turn",
            "baseline_role": "INTERVENTION",
            "source_locator_ids": [response["source_locators"][0]["locator_id"]],
        }

    def reproduction_support(self, response: dict, *, closed: bool = True) -> dict:
        observed = {field: "OBSERVED_IN_SOURCE" for field in r2r1.REPRODUCTION_FACT_FIELDS}
        return {
            "reproduction_support_id": "PRS-AUDIO-1",
            "task": "audio question answering",
            "dataset": "MMAU",
            "dataset_revision": "v1",
            "split": "test-mini",
            "official_repo": "https://github.com/example/audio-agent",
            "pinned_revision": "abc123",
            "entrypoint": "python eval.py",
            "model_access": "TF_STRICT_BLACK_BOX",
            "license_terms": "Apache-2.0",
            "evaluator_or_ground_truth": "accuracy",
            "field_evidence_states": observed,
            "source_locator_ids": [response["source_locators"][0]["locator_id"]],
            "closure_status": "CLOSED_PAPER_SUPPORT" if closed else "OPEN_WITH_BLOCKERS",
            "blockers": [] if closed else ["One or more required facts are not paper-observable."],
        }

    def submitted_rows(self, slot: str) -> list[dict]:
        return [self.completed_boundary(index, slot=slot) for index in range(56)]

    def actual_artifacts(self) -> dict[str, bytes]:
        return {
            name: r2r1.json_bytes(self.package[name])
            for name in r2r1.CODER_DISTRIBUTION_ALLOWED_ARTIFACTS
        }

    def delivery_receipt(self, slot: str) -> dict:
        receipt = r2r1.build_delivery_receipt(
            self.package,
            received_artifacts=self.actual_artifacts(),
            received_prompt_bytes=r2r1.json_bytes(self.package["coder_prompt"]),
            slot=slot,
            coder_id=f"CODER-{slot}",
            transaction_id=f"TX-CODER-{slot}",
            process_id=f"PROC-{slot}",
            task_id=f"TASK-{slot}",
            model="gpt-5.6-sol" if slot == "A" else "gpt-5.6-terra",
            delivered_at="2026-07-25T12:00:00+08:00",
            submitted_at="2026-07-25T18:00:00+08:00",
        )
        self.assertTrue(receipt["receipt_id"].startswith(f"R2R1-DELIVERY-{slot}-"))
        return receipt

    def bindings(self) -> list[dict[str, str]]:
        return [
            {
                "slot": "A", "coder_id": "CODER-A", "transaction_id": "TX-CODER-A",
                "process_id": "PROC-A", "task_id": "TASK-A", "model": "gpt-5.6-sol",
            },
            {
                "slot": "B", "coder_id": "CODER-B", "transaction_id": "TX-CODER-B",
                "process_id": "PROC-B", "task_id": "TASK-B", "model": "gpt-5.6-terra",
            },
        ]

    def frozen_runtime(self) -> tuple[dict, list[dict], list[dict], dict[str, bytes]]:
        delivery = [self.delivery_receipt("A"), self.delivery_receipt("B")]
        raw = {
            "A": r2r1.canonical_response_bytes(self.submitted_rows("A")),
            "B": r2r1.canonical_response_bytes(self.submitted_rows("B")),
        }
        submissions = [
            r2r1.build_submission_receipt(
                self.package,
                delivery_receipt=delivery[index],
                raw_response_bytes=raw[slot],
            )
            for index, slot in enumerate(("A", "B"))
        ]
        runtime = r2r1.bind_runtime_intake(
            self.package, self.bindings(), delivery, submissions
        )
        return runtime, delivery, submissions, raw

    def agreement_kwargs(
        self, runtime: dict, delivery: list[dict], submissions: list[dict]
    ) -> dict:
        return {
            "runtime_intake": runtime,
            "frozen_contract": self.package["frozen_package_contract"],
            "response_schema": self.package["response_schema"],
            "source_manifest": self.package["source_manifest"],
            "distribution_manifest": self.package["distribution_manifest"],
            "delivery_receipt_schema": self.package["delivery_receipt_schema"],
            "delivery_receipts": delivery,
            "submission_receipt_schema": self.package["submission_receipt_schema"],
            "submission_receipts": submissions,
            "positive_support_preflight": self.package["positive_support_preflight"],
        }

    def rehash_submission(self, receipt: dict) -> None:
        receipt["receipt_sha256"] = r2r1.sha256_bytes(
            r2r1.json_bytes(r2r1._submission_receipt_projection(receipt))
        )

    def test_r2r1_preserves_sample_and_remains_not_distributed(self) -> None:
        report = r2r1.build_report(self.package)
        self.assertEqual(56, self.package["calibration_manifest"]["N"])
        self.assertEqual(38, self.package["calibration_manifest"]["overlay_count"])
        self.assertEqual(18, self.package["calibration_manifest"]["sentinel_count"])
        self.assertEqual("AGENTIC_CALIBRATION_R2R1_METHOD_READY_NOT_DISTRIBUTED", report["status"])
        self.assertFalse(report["authority"]["coder_distributed"])
        self.assertFalse(report["authority"]["agreement_computed"])

    def test_package_is_deterministic_blind_and_source_identical_to_r2(self) -> None:
        rebuilt = r2r1.build_package()
        self.assertEqual(self.package, rebuilt)
        self.assertEqual(
            r2r1.r2.build_package()["source_manifest"], self.package["source_manifest"]
        )
        self.assertEqual(8, len(r2r1.CODER_DISTRIBUTION_ALLOWED_ARTIFACTS))
        self.assertNotIn(
            "submission_receipt_schema", r2r1.CODER_DISTRIBUTION_ALLOWED_ARTIFACTS
        )
        self.assertEqual(
            [],
            r2r1.scan_coder_bundle_leaks(
                self.package, r2r1.CODER_DISTRIBUTION_ALLOWED_ARTIFACTS
            ),
        )

    def test_duplicate_local_ids_are_rejected_before_reference_resolution(self) -> None:
        response = self.completed_boundary()
        response["dataset_nodes"] = [
            self.dataset_node(response, "DS-DUP", "MMAU"),
            self.dataset_node(response, "DS-DUP", "MMAR"),
        ]
        response["run_cells"] = [self.run_cell(response, "RUN-1", "DS-DUP")]
        with self.assertRaisesRegex(r2r1.ContractError, "duplicate coder-local dataset_nodes ID"):
            r2r1.compile_response_objects(response, self.package["source_manifest"])

    def test_typed_maps_allow_cross_type_strings_without_cross_type_overwrite(self) -> None:
        response = self.completed_boundary()
        response["dataset_nodes"] = [self.dataset_node(response, "LOCAL-SAME")]
        response["run_cells"] = [self.run_cell(response, "LOCAL-SAME", "LOCAL-SAME")]
        response["translation_or_compatibility_decisions"] = [{
            "decision_id": "DEC-1",
            "decision_type": "CORE_MEMBER_COMPATIBILITY",
            "target_object_type": "dataset_nodes",
            "target_object_id": "LOCAL-SAME",
            "compatibility_decision": "COMPATIBLE",
            "reason": "Dataset protocol is compatible.",
            "source_locator_ids": [response["source_locators"][0]["locator_id"]],
        }]
        compiled = r2r1.compile_response_objects(response, self.package["source_manifest"])
        target = compiled["translation_or_compatibility_decisions"][0]["target_object_id"]
        self.assertEqual(compiled["dataset_nodes"][0]["object_match_key"], target)
        self.assertNotEqual(compiled["run_cells"][0]["object_match_key"], target)

    def test_unknown_or_untyped_compatibility_target_fails_closed(self) -> None:
        response = self.completed_boundary()
        definition = self.package["response_schema"]["$defs"]["compatibility_decision"]
        self.assertIn("target_object_type", definition["required"])
        response["translation_or_compatibility_decisions"] = [{
            "decision_id": "DEC-1", "decision_type": "CLAIM_EQUIVALENCE",
            "target_object_type": "dataset_nodes", "target_object_id": "MISSING",
            "compatibility_decision": "WITHHELD", "reason": "Target is absent.",
            "source_locator_ids": [response["source_locators"][0]["locator_id"]],
        }]
        with self.assertRaisesRegex(r2r1.ContractError, "undeclared typed target"):
            r2r1.compile_response_objects(response, self.package["source_manifest"])

    def test_reproduction_candidate_requires_every_fact_affirmatively_observed(self) -> None:
        response = self.completed_boundary()
        response["paper_labels"]["reference_borrow_reproduce"] = "REPRODUCTION_CANDIDATE"
        support = self.reproduction_support(response)
        support["dataset_revision"] = "NOT_STATED_IN_SOURCE"
        support["field_evidence_states"]["dataset_revision"] = "NOT_STATED_IN_SOURCE"
        response["paper_reproduction_support"] = [support]
        response["object_absence_reasons"]["paper_reproduction_support"] = "OBJECTS_PRESENT"
        with self.assertRaisesRegex(r2r1.ContractError, "affirmatively observed"):
            r2r1.validate_completed_response(
                response, self.package["response_schema"], self.package["source_manifest"]
            )

    def test_closed_support_rejects_placeholder_values_and_ambiguous_access(self) -> None:
        mutations = {
            "placeholder": ("entrypoint", "NOT_STATED_IN_SOURCE"),
            "ambiguous-access": ("model_access", "MIXED_OR_UNCLEAR"),
            "dynamic-revision": ("pinned_revision", "main"),
        }
        for label, (field, value) in mutations.items():
            with self.subTest(label=label):
                response = self.completed_boundary()
                support = self.reproduction_support(response)
                support[field] = value
                response["paper_reproduction_support"] = [support]
                response["object_absence_reasons"]["paper_reproduction_support"] = "OBJECTS_PRESENT"
                with self.assertRaisesRegex(r2r1.ContractError, "closed paper support"):
                    r2r1.validate_completed_response(
                        response, self.package["response_schema"], self.package["source_manifest"]
                    )

    def test_open_support_requires_non_observed_fact_and_blocker(self) -> None:
        response = self.completed_boundary()
        support = self.reproduction_support(response, closed=False)
        response["paper_reproduction_support"] = [support]
        response["object_absence_reasons"]["paper_reproduction_support"] = "OBJECTS_PRESENT"
        with self.assertRaisesRegex(r2r1.ContractError, "non-observed fact"):
            r2r1.validate_completed_response(
                response, self.package["response_schema"], self.package["source_manifest"]
            )
        support["field_evidence_states"]["pinned_revision"] = "NOT_STATED_IN_SOURCE"
        support["pinned_revision"] = "NOT_STATED_IN_SOURCE"
        r2r1.validate_completed_response(
            response, self.package["response_schema"], self.package["source_manifest"]
        )
        support["blockers"] = []
        with self.assertRaisesRegex(r2r1.ContractError, "at least one blocker"):
            r2r1.validate_completed_response(
                response, self.package["response_schema"], self.package["source_manifest"]
            )

    def test_submission_receipt_binds_exact_canonical_raw_bytes_and_order(self) -> None:
        delivery = self.delivery_receipt("A")
        raw = r2r1.canonical_response_bytes(self.submitted_rows("A"))
        receipt = r2r1.build_submission_receipt(
            self.package, delivery_receipt=delivery, raw_response_bytes=raw
        )
        self.assertEqual(len(raw), receipt["response_bytes"])
        self.assertEqual(r2r1.sha256_bytes(raw), receipt["response_sha256"])
        self.assertEqual(56, receipt["response_count"])
        Draft202012Validator(self.package["submission_receipt_schema"]).validate(receipt)
        with self.assertRaisesRegex(r2r1.ContractError, "canonical raw response bytes"):
            r2r1.build_submission_receipt(
                self.package, delivery_receipt=delivery, raw_response_bytes=raw + b"\n"
            )
        wrong_order = list(reversed(self.submitted_rows("A")))
        with self.assertRaisesRegex(r2r1.ContractError, "canonical paper order"):
            r2r1.build_submission_receipt(
                self.package,
                delivery_receipt=delivery,
                raw_response_bytes=r2r1.json_bytes(wrong_order),
            )
        changed_rows = self.submitted_rows("A")
        changed_rows[0]["paper_labels"]["agentic_scope"]["scope_reason"] = "Changed before freeze."
        changed_raw = r2r1.json_bytes(changed_rows)
        changed_receipt = r2r1.build_submission_receipt(
            self.package, delivery_receipt=delivery, raw_response_bytes=changed_raw
        )
        self.assertNotEqual(receipt["response_sha256"], changed_receipt["response_sha256"])

    def test_runtime_intake_binds_two_submission_receipts_and_frozen_root(self) -> None:
        runtime, _, submissions, _ = self.frozen_runtime()
        self.assertEqual("FROZEN_RESPONSES_BOUND", runtime["frozen_response_root"]["status"])
        self.assertRegex(runtime["frozen_response_root"]["root_sha256"], r"^[0-9a-f]{64}$")
        slots = {row["coder_slot"]: row for row in runtime["coder_slots"]}
        for receipt in submissions:
            slot = slots[receipt["coder_slot"]]
            self.assertEqual(receipt["receipt_id"], slot["submission_receipt_id"])
            self.assertEqual(receipt["response_sha256"], slot["response_sha256"])
            self.assertEqual(receipt["receipt_sha256"], slot["submission_receipt_sha256"])

    def test_agreement_rejects_response_mutation_after_freeze(self) -> None:
        runtime, delivery, submissions, raw = self.frozen_runtime()
        changed = json.loads(raw["A"].decode("utf-8"))
        changed[0]["paper_labels"]["paper_role"] = "FALSIFIER"
        mutated = {**raw, "A": r2r1.json_bytes(changed)}
        with self.assertRaisesRegex(agreement_v7.AgreementError, "frozen response bytes"):
            agreement_v7.compute_agreement(
                mutated, **self.agreement_kwargs(runtime, delivery, submissions)
            )

    def test_agreement_rejects_tampered_receipt_or_frozen_root_before_metrics(self) -> None:
        runtime, delivery, submissions, raw = self.frozen_runtime()
        tampered_receipts = copy.deepcopy(submissions)
        tampered_receipts[0]["response_sha256"] = "0" * 64
        with self.assertRaisesRegex(agreement_v7.AgreementError, "submission receipt"):
            agreement_v7.compute_agreement(
                raw, **self.agreement_kwargs(runtime, delivery, tampered_receipts)
            )
        tampered_runtime = copy.deepcopy(runtime)
        tampered_runtime["frozen_response_root"]["root_sha256"] = "0" * 64
        with self.assertRaisesRegex(agreement_v7.AgreementError, "frozen response root"):
            agreement_v7.compute_agreement(
                raw, **self.agreement_kwargs(tampered_runtime, delivery, submissions)
            )

    def test_agreement_accepts_only_bound_bytes_and_marks_provenance_validated(self) -> None:
        runtime, delivery, submissions, raw = self.frozen_runtime()
        result = agreement_v7.compute_agreement(
            raw, **self.agreement_kwargs(runtime, delivery, submissions)
        )
        self.assertEqual(56, result["paper_count"])
        self.assertTrue(result["frozen_provenance_validated"])
        self.assertTrue(result["submission_receipts_validated"])
        self.assertTrue(result["frozen_response_root_validated"])

    def test_schema_rejects_missing_typed_evidence_states(self) -> None:
        response = self.completed_boundary()
        support = self.reproduction_support(response)
        support.pop("field_evidence_states")
        response["paper_reproduction_support"] = [support]
        with self.assertRaises(ValidationError):
            Draft202012Validator(self.package["response_schema"]).validate(response)

    def test_raw_response_decoder_and_receipt_identity_fail_closed(self) -> None:
        bad_raw = ("not-bytes", b"\xff", r2r1.json_bytes({"not": "a-list"}))
        for value in bad_raw:
            with self.subTest(value=repr(value)):
                with self.assertRaisesRegex(r2r1.ContractError, "canonical raw response bytes"):
                    r2r1._decode_canonical_responses(value)  # type: ignore[arg-type]

        delivery = self.delivery_receipt("A")
        rows = self.submitted_rows("A")
        rows[0]["coder_id"] = "OTHER"
        with self.assertRaisesRegex(r2r1.ContractError, "coder differs"):
            r2r1.build_submission_receipt(
                self.package,
                delivery_receipt=delivery,
                raw_response_bytes=r2r1.json_bytes(rows),
            )
        rows = self.submitted_rows("A")
        rows[0]["coder_transaction_id"] = "OTHER-TX"
        with self.assertRaisesRegex(r2r1.ContractError, "transaction differs"):
            r2r1.build_submission_receipt(
                self.package,
                delivery_receipt=delivery,
                raw_response_bytes=r2r1.json_bytes(rows),
            )
        rows = self.submitted_rows("A")
        rows[1]["paper_id"] = rows[0]["paper_id"]
        with self.assertRaisesRegex(r2r1.ContractError, "duplicate paper IDs"):
            r2r1.build_submission_receipt(
                self.package,
                delivery_receipt=delivery,
                raw_response_bytes=r2r1.json_bytes(rows),
            )

    def test_runtime_binding_rejects_missing_or_inconsistent_receipts(self) -> None:
        runtime, delivery, submissions, _ = self.frozen_runtime()
        self.assertEqual("BOUND_FOR_PRE_ADJUDICATION_AGREEMENT", runtime["status"])
        with self.assertRaisesRegex(r2r1.ContractError, "exact A/B"):
            r2r1.bind_runtime_intake(
                self.package, self.bindings()[:1], delivery, submissions
            )
        bad_hash = copy.deepcopy(submissions)
        bad_hash[0]["receipt_sha256"] = "0" * 64
        with self.assertRaisesRegex(r2r1.ContractError, "receipt hash differs"):
            r2r1.bind_runtime_intake(
                self.package, self.bindings(), delivery, bad_hash
            )
        bad_identity = copy.deepcopy(submissions)
        bad_identity[0]["process_id"] = "OTHER-PROCESS"
        self.rehash_submission(bad_identity[0])
        with self.assertRaisesRegex(r2r1.ContractError, "submission process_id"):
            r2r1.bind_runtime_intake(
                self.package, self.bindings(), delivery, bad_identity
            )
        bad_link = copy.deepcopy(submissions)
        bad_link[0]["delivery_receipt_id"] = "OTHER-DELIVERY"
        self.rehash_submission(bad_link[0])
        with self.assertRaisesRegex(r2r1.ContractError, "not bound to delivery"):
            r2r1.bind_runtime_intake(
                self.package, self.bindings(), delivery, bad_link
            )

    def test_compiler_rejects_every_unknown_reference_class_and_duplicate_signature(self) -> None:
        response = self.completed_boundary()
        response["run_cells"] = [self.run_cell(response, "RUN-1", "MISSING")]
        with self.assertRaisesRegex(r2r1.ContractError, "undeclared dataset node"):
            r2r1.compile_response_objects(response, self.package["source_manifest"])

        response = self.completed_boundary()
        response["observations"] = [{
            "observation_id": "OBS-1", "run_cell_id": "MISSING",
            "metric_or_evaluator": "accuracy", "observation_role": "PRIMARY",
            "raw_result": "0.5", "within_group_delta": "none",
            "source_locator_ids": [response["source_locators"][0]["locator_id"]],
        }]
        with self.assertRaisesRegex(r2r1.ContractError, "undeclared run cell"):
            r2r1.compile_response_objects(response, self.package["source_manifest"])

        response = self.completed_boundary()
        response["paired_comparisons"] = [{
            "comparison_id": "PAIR-1", "baseline_cell_id": "MISSING-A",
            "intervention_cell_id": "MISSING-B", "comparison_interpretation": "none",
            "source_locator_ids": [response["source_locators"][0]["locator_id"]],
        }]
        with self.assertRaisesRegex(r2r1.ContractError, "undeclared run cell"):
            r2r1.compile_response_objects(response, self.package["source_manifest"])

        response = self.completed_boundary()
        response["dataset_edges"] = [{
            "dataset_edge_id": "EDGE-1", "edge_type": "SUBSET_OF",
            "source_dataset_id": "MISSING-A", "target_dataset_id": "MISSING-B",
            "evidence_basis": "paper statement",
            "source_locator_ids": [response["source_locators"][0]["locator_id"]],
        }]
        with self.assertRaisesRegex(r2r1.ContractError, "undeclared dataset node"):
            r2r1.compile_response_objects(response, self.package["source_manifest"])

        response = self.completed_boundary()
        response["dataset_nodes"] = [
            self.dataset_node(response, "DS-1"), self.dataset_node(response, "DS-2")
        ]
        with self.assertRaisesRegex(r2r1.ContractError, "duplicate compiler-derived"):
            r2r1.compile_response_objects(response, self.package["source_manifest"])

    def test_agreement_static_and_runtime_guards_fail_independently(self) -> None:
        runtime, delivery, submissions, raw = self.frozen_runtime()
        kwargs = self.agreement_kwargs(runtime, delivery, submissions)
        with self.assertRaisesRegex(agreement_v7.AgreementError, "minimum"):
            agreement_v7.compute_agreement(raw, minimum=0.84, **kwargs)

        mutations = {
            "schema": ("schema", "wrong", "unknown R2R1"),
            "status": ("status", "UNBOUND", "not bound"),
            "threshold": ("agreement_minimum", 0.84, "minimum"),
            "flag": ("typed_local_object_maps_required", False, "required flag"),
            "N": ("N", 55, "exact N=56"),
        }
        for label, (field, value, message) in mutations.items():
            with self.subTest(label=label):
                changed = copy.deepcopy(runtime)
                changed[field] = value
                with self.assertRaisesRegex(agreement_v7.AgreementError, message):
                    agreement_v7._validate_runtime_intake(changed)

        changed = copy.deepcopy(runtime)
        changed["coder_slots"][1]["coder_id"] = changed["coder_slots"][0]["coder_id"]
        with self.assertRaisesRegex(agreement_v7.AgreementError, "distinct non-empty coder_id"):
            agreement_v7._validate_runtime_intake(changed)
        changed = copy.deepcopy(runtime)
        changed["coder_slots"][0]["assignment_status"] = "UNASSIGNED"
        with self.assertRaisesRegex(agreement_v7.AgreementError, "must be frozen"):
            agreement_v7._validate_runtime_intake(changed)
        changed = copy.deepcopy(runtime)
        changed["coder_slots"][0]["model"] = "wrong-model"
        with self.assertRaisesRegex(agreement_v7.AgreementError, "model differs"):
            agreement_v7._validate_runtime_intake(changed)
        changed = copy.deepcopy(runtime)
        changed["coder_slots"][0]["response_sha256"] = None
        with self.assertRaisesRegex(agreement_v7.AgreementError, "lacks frozen response binding"):
            agreement_v7._validate_runtime_intake(changed)

        broken_frozen = copy.deepcopy(self.package["frozen_package_contract"])
        broken_frozen["agreement_minimum"] = 0.84
        with self.assertRaisesRegex(agreement_v7.AgreementError, "compiled R2R1 frozen contract"):
            agreement_v7.compute_agreement(raw, **{**kwargs, "frozen_contract": broken_frozen})

    def test_submission_receipt_validator_covers_slot_schema_and_runtime_mismatch(self) -> None:
        runtime, delivery, submissions, raw = self.frozen_runtime()
        slots = sorted(runtime["coder_slots"], key=lambda row: row["coder_slot"])
        args = {
            "slots": slots,
            "schema": self.package["submission_receipt_schema"],
            "intake": runtime,
            "frozen": self.package["frozen_package_contract"],
            "paper_ids": runtime["canonical_paper_ids"],
        }
        with self.assertRaisesRegex(agreement_v7.AgreementError, "slots A/B"):
            agreement_v7._validate_submission_receipts_and_bytes(
                receipts=submissions, raw_by_slot={"A": raw["A"]}, **args
            )
        with self.assertRaisesRegex(agreement_v7.AgreementError, "submission receipts require"):
            agreement_v7._validate_submission_receipts_and_bytes(
                receipts=submissions[:1], raw_by_slot=raw, **args
            )
        invalid_schema = copy.deepcopy(submissions)
        invalid_schema[0].pop("response_count")
        with self.assertRaisesRegex(agreement_v7.AgreementError, "invalid submission receipt"):
            agreement_v7._validate_submission_receipts_and_bytes(
                receipts=invalid_schema, raw_by_slot=raw, **args
            )
        wrong_identity = copy.deepcopy(submissions)
        wrong_identity[0]["coder_id"] = "OTHER"
        self.rehash_submission(wrong_identity[0])
        with self.assertRaisesRegex(agreement_v7.AgreementError, "runtime slot"):
            agreement_v7._validate_submission_receipts_and_bytes(
                receipts=wrong_identity, raw_by_slot=raw, **args
            )
        wrong_intake = copy.deepcopy(runtime)
        wrong_intake["coder_slots"][0]["response_bytes"] += 1
        with self.assertRaisesRegex(agreement_v7.AgreementError, "frozen runtime intake"):
            agreement_v7._validate_submission_receipts_and_bytes(
                receipts=submissions, raw_by_slot=raw,
                **{
                    **args,
                    "intake": wrong_intake,
                    "slots": sorted(
                        wrong_intake["coder_slots"], key=lambda row: row["coder_slot"]
                    ),
                },
            )

    def test_matching_objects_exercise_exact_object_field_metrics(self) -> None:
        rows_a, rows_b = self.submitted_rows("A"), self.submitted_rows("B")
        for rows in (rows_a, rows_b):
            rows[0]["dataset_nodes"] = [self.dataset_node(rows[0], "DS-LOCAL")]
            rows[0]["object_absence_reasons"]["dataset_nodes"] = "OBJECTS_PRESENT"
        delivery = [self.delivery_receipt("A"), self.delivery_receipt("B")]
        raw = {
            "A": r2r1.json_bytes(rows_a),
            "B": r2r1.json_bytes(rows_b),
        }
        submissions = [
            r2r1.build_submission_receipt(
                self.package, delivery_receipt=delivery[index], raw_response_bytes=raw[slot]
            )
            for index, slot in enumerate(("A", "B"))
        ]
        runtime = r2r1.bind_runtime_intake(
            self.package, self.bindings(), delivery, submissions
        )
        result = agreement_v7.compute_agreement(
            raw, **self.agreement_kwargs(runtime, delivery, submissions)
        )
        gate = result["object_level"]["dataset_nodes"]
        self.assertEqual(1, gate["matched_objects"])
        self.assertEqual(1.0, gate["segmentation_f1"])
        self.assertTrue(all(
            field["denominator"] == 1 and field["numerator"] == 1
            for field in gate["critical_field_gates"].values()
        ))

    def test_package_mutations_fail_closed(self) -> None:
        cases = []
        changed = copy.deepcopy(self.package)
        changed["calibration_manifest"]["canonical_ids"][0] = "replacement"
        cases.append((changed, "exact N=56"))
        changed = copy.deepcopy(self.package)
        changed["calibration_manifest"]["overlay_count"] = 37
        cases.append((changed, "38 overlays"))
        changed = copy.deepcopy(self.package)
        changed["response_schema"]["$id"] = "wrong"
        cases.append((changed, "schema identity"))
        changed = copy.deepcopy(self.package)
        changed["distribution_manifest"]["distribution_authorized"] = True
        cases.append((changed, "before independent ACCEPT"))
        changed = copy.deepcopy(self.package)
        changed["agreement"]["agreement_minimum"] = 0.84
        changed["distribution_manifest"] = r2r1.build_distribution_manifest(changed)
        cases.append((changed, "threshold"))
        changed = copy.deepcopy(self.package)
        changed["local_reproduction_readiness"]["candidates"][0]["anchor_status"] = "REPRODUCTION_ANCHOR"
        cases.append((changed, "promoted a reproduction anchor"))
        for package, message in cases:
            with self.subTest(message=message):
                with self.assertRaisesRegex(r2r1.ContractError, message):
                    r2r1.validate_package(package)

    def test_static_projection_and_review_manifest_missing_inputs_fail_closed(self) -> None:
        intake = copy.deepcopy(self.package["agreement_intake_contract"])
        intake.pop("submission_receipt_schema_id")
        with self.assertRaisesRegex(r2r1.ContractError, "lacks frozen R2R1"):
            r2r1.static_intake_projection(intake)
        report = r2r1.build_report(self.package)
        with mock.patch.dict(
            r2r1.ARTIFACT_PATHS,
            {"agreement": r2r1.WORKBENCH / "missing.json"},
            clear=True,
        ):
            with self.assertRaisesRegex(r2r1.ContractError, "review inputs missing"):
                r2r1.build_review_manifest(report)


if __name__ == "__main__":
    unittest.main()
