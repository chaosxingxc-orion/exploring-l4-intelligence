from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path
from unittest import mock

from jsonschema import Draft202012Validator, ValidationError

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import sf_stage1c_v2_calibration_agreement_v6 as agreement_v6
    import sf_stage1c_v2_precalibration_r2 as r2
    import sf_stage1c_v2_r2_guards as guards
else:
    from scripts.survey import sf_stage1c_v2_calibration_agreement_v6 as agreement_v6
    from scripts.survey import sf_stage1c_v2_precalibration_r2 as r2
    from scripts.survey import sf_stage1c_v2_r2_guards as guards


class Stage1cV2PrecalibrationR2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.package = r2.build_package()
        cls.source_by_paper = {
            row["canonical_id"]: row for row in cls.package["source_manifest"]["items"]
        }

    def completed_boundary(self, paper_index: int = 0, *, coder: str = "CODER-A") -> dict:
        item = self.package["blind_packet"]["items"][paper_index]
        response = copy.deepcopy(item["blank_response"])
        source = self.source_by_paper[response["paper_id"]]
        response.update({
            "response_status": "CODER_SUBMITTED",
            "response_id": f"RESP-{coder}-{paper_index:02d}",
            "coder_transaction_id": f"TX-{coder}",
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
            name: "NOT_APPLICABLE_NON_EMPIRICAL" for name in r2.OBJECT_ARRAYS
        }
        return response

    def dataset_node(self, response: dict, *, object_id: str, locator_id: str) -> dict:
        return {
            "dataset_node_id": object_id,
            "name": "MMAU",
            "revision": "paper-reported",
            "split": "test-mini",
            "source_locator_ids": [locator_id],
        }

    def actual_artifacts(self) -> dict[str, bytes]:
        return {
            name: r2.json_bytes(self.package[name])
            for name in r2.CODER_DISTRIBUTION_ALLOWED_ARTIFACTS
        }

    def receipt(self, slot: str) -> dict:
        model = "gpt-5.6-sol" if slot == "A" else "gpt-5.6-terra"
        return r2.build_delivery_receipt(
            self.package,
            received_artifacts=self.actual_artifacts(),
            received_prompt_bytes=r2.json_bytes(self.package["coder_prompt"]),
            slot=slot,
            coder_id=f"CODER-{slot}",
            transaction_id=f"TX-CODER-{slot}",
            process_id=f"PROC-{slot}",
            task_id=f"TASK-{slot}",
            model=model,
            delivered_at="2026-07-25T12:00:00+08:00",
            submitted_at="2026-07-25T18:00:00+08:00",
        )

    def runtime(self) -> tuple[dict, list[dict]]:
        bindings = (
            {
                "slot": "A", "coder_id": "CODER-A", "transaction_id": "TX-CODER-A",
                "process_id": "PROC-A", "task_id": "TASK-A", "model": "gpt-5.6-sol",
            },
            {
                "slot": "B", "coder_id": "CODER-B", "transaction_id": "TX-CODER-B",
                "process_id": "PROC-B", "task_id": "TASK-B", "model": "gpt-5.6-terra",
            },
        )
        receipts = [self.receipt("A"), self.receipt("B")]
        return r2.bind_runtime_intake(self.package, bindings, receipts), receipts

    def submitted_rows(self, slot: str) -> list[dict]:
        coder = f"CODER-{slot}"
        return [self.completed_boundary(index, coder=coder) for index in range(56)]

    def test_r2_preserves_exact_sample_and_is_not_distributed(self) -> None:
        report = r2.build_report(self.package)
        self.assertEqual(56, self.package["calibration_manifest"]["N"])
        self.assertEqual(38, self.package["calibration_manifest"]["overlay_count"])
        self.assertEqual(18, self.package["calibration_manifest"]["sentinel_count"])
        self.assertEqual("AGENTIC_CALIBRATION_R2_METHOD_READY_NOT_DISTRIBUTED", report["status"])
        self.assertFalse(report["authority"]["coder_distributed"])
        self.assertFalse(report["authority"]["agreement_computed"])
        self.assertEqual(
            agreement_v6.FROZEN_CONTRACT_SHA256,
            r2.sha256_bytes(r2.json_bytes(self.package["frozen_package_contract"])),
        )

    def test_raw_schema_forbids_coder_authored_object_match_keys(self) -> None:
        schema = self.package["response_schema"]
        for array_name, definition_name in r2.OBJECT_DEFINITION_BY_ARRAY.items():
            with self.subTest(array=array_name):
                definition = schema["$defs"][definition_name]
                self.assertNotIn("object_match_key", definition["properties"])
                self.assertNotIn("object_match_key", definition["required"])
        response = self.completed_boundary()
        response["dataset_nodes"] = [{
            "object_match_key": "caller-key",
            **self.dataset_node(
                response,
                object_id="DS-1",
                locator_id=response["source_locators"][0]["locator_id"],
            ),
        }]
        with self.assertRaises(ValidationError):
            Draft202012Validator(schema).validate(response)

    def test_compiler_derives_same_identity_from_semantics_not_coder_ids(self) -> None:
        left = self.completed_boundary(coder="CODER-A")
        right = self.completed_boundary(coder="CODER-B")
        left_locator = left["source_locators"][0]["locator_id"]
        right_locator = right["source_locators"][0]["locator_id"]
        left["dataset_nodes"] = [self.dataset_node(left, object_id="DS-LEFT", locator_id=left_locator)]
        right["dataset_nodes"] = [self.dataset_node(right, object_id="DS-RIGHT", locator_id=right_locator)]
        compiled_left = r2.compile_response_objects(left, self.package["source_manifest"])
        compiled_right = r2.compile_response_objects(right, self.package["source_manifest"])
        self.assertEqual(
            compiled_left["dataset_nodes"][0]["object_match_key"],
            compiled_right["dataset_nodes"][0]["object_match_key"],
        )
        self.assertNotEqual("DS-LEFT", compiled_left["dataset_nodes"][0]["object_match_key"])

    def test_source_anchor_is_compiler_owned_and_coordinate_sensitive(self) -> None:
        response = self.completed_boundary()
        locator_id = response["source_locators"][0]["locator_id"]
        response["dataset_nodes"] = [self.dataset_node(response, object_id="DS-1", locator_id=locator_id)]
        page_one = r2.compile_response_objects(response, self.package["source_manifest"])
        changed = copy.deepcopy(response)
        changed["source_locators"][0]["anchor_value"] = "2"
        changed["source_locators"][0]["precise_locator"] = "Page 2, benchmark definition."
        page_two = r2.compile_response_objects(changed, self.package["source_manifest"])
        self.assertNotEqual(
            page_one["dataset_nodes"][0]["object_match_key"],
            page_two["dataset_nodes"][0]["object_match_key"],
        )
        anchor = page_one["compiled_source_anchors"][0]
        self.assertRegex(anchor["source_anchor_id"], r"^SA-[0-9a-f]{24}$")
        self.assertEqual("PAGE", anchor["anchor_type"])

    def test_unmatched_object_enters_every_applicable_field_denominator(self) -> None:
        left = self.completed_boundary(coder="CODER-A")
        right = self.completed_boundary(coder="CODER-B")
        locator_id = left["source_locators"][0]["locator_id"]
        left["dataset_nodes"] = [self.dataset_node(left, object_id="DS-ONLY-A", locator_id=locator_id)]
        compiled_left = r2.compile_response_objects(left, self.package["source_manifest"])
        compiled_right = r2.compile_response_objects(right, self.package["source_manifest"])
        result = agreement_v6._compute_metrics(
            {left["paper_id"]: compiled_left},
            {right["paper_id"]: compiled_right},
            [left["paper_id"]],
            0.85,
        )
        gate = result["object_level"]["dataset_nodes"]
        self.assertEqual("FAIL", gate["segmentation_gate_status"])
        for field, field_gate in gate["critical_field_gates"].items():
            with self.subTest(field=field):
                self.assertEqual(1, field_gate["denominator"])
                self.assertEqual(0, field_gate["numerator"])
                self.assertEqual("FAIL", field_gate["gate_status"])

    def test_not_calibrated_is_reserved_for_true_both_zero_class(self) -> None:
        left = r2.compile_response_objects(self.completed_boundary(coder="CODER-A"), self.package["source_manifest"])
        right = r2.compile_response_objects(self.completed_boundary(coder="CODER-B"), self.package["source_manifest"])
        paper_id = left["paper_id"]
        result = agreement_v6._compute_metrics({paper_id: left}, {paper_id: right}, [paper_id], 0.85)
        gate = result["object_level"]["dataset_edges"]
        self.assertEqual(0, gate["coder_a_objects"])
        self.assertEqual(0, gate["coder_b_objects"])
        self.assertEqual("NOT_CALIBRATED", gate["gate_status"])

    def test_two_different_unmatched_objects_count_as_union_two_not_max_one(self) -> None:
        left = self.completed_boundary(coder="CODER-A")
        right = self.completed_boundary(coder="CODER-B")
        left["dataset_nodes"] = [self.dataset_node(
            left, object_id="DS-A", locator_id=left["source_locators"][0]["locator_id"]
        )]
        right_node = self.dataset_node(
            right, object_id="DS-B", locator_id=right["source_locators"][0]["locator_id"]
        )
        right_node["name"] = "MMAR"
        right["dataset_nodes"] = [right_node]
        compiled_left = r2.compile_response_objects(left, self.package["source_manifest"])
        compiled_right = r2.compile_response_objects(right, self.package["source_manifest"])
        paper_id = left["paper_id"]
        result = agreement_v6._compute_metrics(
            {paper_id: compiled_left}, {paper_id: compiled_right}, [paper_id], 0.85
        )
        gate = result["object_level"]["dataset_nodes"]
        self.assertEqual(2, gate["union_objects"])
        self.assertTrue(all(
            field_gate["denominator"] == 2
            for field_gate in gate["critical_field_gates"].values()
        ))

    def test_paper_reproduction_support_is_blind_observable_and_local_state_is_not(self) -> None:
        definition = self.package["response_schema"]["$defs"]["paper_reproduction_support"]
        self.assertNotIn("local_asset_state", definition["properties"])
        self.assertIn("OPEN_WITH_BLOCKERS", definition["properties"]["closure_status"]["enum"])
        local = self.package["local_reproduction_readiness"]
        self.assertEqual("REVIEWER_ONLY_NOT_DISTRIBUTED", local["visibility"])
        self.assertNotIn("local_reproduction_readiness", r2.CODER_DISTRIBUTION_ALLOWED_ARTIFACTS)

    def test_open_paper_support_is_recordable_but_not_candidate_closure(self) -> None:
        response = self.completed_boundary()
        locator_id = response["source_locators"][0]["locator_id"]
        support = {
            "reproduction_support_id": "PRS-AUDIO-1",
            "task": "audio question answering",
            "dataset": "MMAU",
            "dataset_revision": "paper-reported",
            "split": "test-mini",
            "official_repo": "https://github.com/GLJS/AudioToolAgent",
            "pinned_revision": "NOT_STATED_IN_SOURCE",
            "entrypoint": "NOT_STATED_IN_SOURCE",
            "model_access": "MIXED_OR_UNCLEAR",
            "license_terms": "NOT_STATED_IN_SOURCE",
            "evaluator_or_ground_truth": "accuracy",
            "source_locator_ids": [locator_id],
            "closure_status": "OPEN_WITH_BLOCKERS",
            "blockers": ["Pinned revision and entrypoint are not stated in the supplied paper."],
        }
        response["paper_reproduction_support"] = [support]
        response["object_absence_reasons"]["paper_reproduction_support"] = "OBJECTS_PRESENT"
        r2.validate_completed_response(response, self.package["response_schema"], self.package["source_manifest"])
        response["paper_labels"]["reference_borrow_reproduce"] = "REPRODUCTION_CANDIDATE"
        with self.assertRaisesRegex(r2.ContractError, "closed paper support"):
            r2.validate_completed_response(response, self.package["response_schema"], self.package["source_manifest"])

    def test_empirical_extractable_requires_material_objects_and_typed_pair_absence(self) -> None:
        response = self.completed_boundary()
        response["paper_labels"]["paper_disposition"] = "EMPIRICAL_EXTRACTABLE"
        response["paper_labels"]["paper_role"] = "DIRECT_METHOD"
        response["paper_labels"]["empirical_experiment_present"] = True
        response["paired_comparison_absence_reason"] = "NO_BASELINE_INTERVENTION_PAIR"
        for name in r2.OBJECT_ARRAYS:
            response["object_absence_reasons"][name] = "NONE_REPORTED"
        with self.assertRaisesRegex(r2.ContractError, "material run cells"):
            r2.validate_completed_response(response, self.package["response_schema"], self.package["source_manifest"])
        enum = self.package["response_schema"]["properties"]["paired_comparison_absence_reason"]["enum"]
        self.assertIn("NO_CLOSED_COMPARABILITY_KEY", enum)
        self.assertIn("NO_BASELINE_INTERVENTION_PAIR", enum)

    def test_object_locators_cannot_be_title_or_abstract_only(self) -> None:
        response = self.completed_boundary()
        locator_id = response["source_locators"][0]["locator_id"]
        response["source_locators"][0].update({
            "anchor_type": "SECTION", "anchor_value": "Abstract", "precise_locator": "Abstract",
        })
        response["dataset_nodes"] = [self.dataset_node(response, object_id="DS-1", locator_id=locator_id)]
        response["object_absence_reasons"]["dataset_nodes"] = "OBJECTS_PRESENT"
        with self.assertRaisesRegex(r2.ContractError, "title/abstract-only"):
            r2.validate_completed_response(response, self.package["response_schema"], self.package["source_manifest"])

    def test_decision_tables_cover_paper_and_object_triggers(self) -> None:
        tables = self.package["coder_codebook"]["decision_tables"]
        self.assertEqual(
            {
                "paper_disposition", "paper_role", "reference_borrow_reproduce",
                "access_and_dependency", "agentic_scope", "primary_intervention",
                "loop_and_capability_assets", "object_extraction_triggers",
            },
            set(tables),
        )
        for name, rows in tables.items():
            with self.subTest(table=name):
                self.assertTrue(rows)
                self.assertTrue(all("when" in row and "code" in row and "counterexample" in row for row in rows))

    def test_exact_positive_support_preflight_closes_both_mandatory_classes(self) -> None:
        ledger = r2.build_positive_support_ledger(self.package)
        report = r2.validate_positive_support(ledger, self.package)
        self.assertEqual("PASS", report["status"])
        self.assertEqual(
            {"dataset_edges", "paper_reproduction_support"},
            set(report["mandatory_object_classes"]),
        )
        for name, gate in report["class_gates"].items():
            with self.subTest(name=name):
                self.assertGreaterEqual(gate["source_supported_positive_count"], 1)
                self.assertTrue(gate["schema_expressible"])
                self.assertEqual("PASS", gate["status"])

    def test_package_fails_closed_on_sample_replacement_or_anchor_promotion(self) -> None:
        broken = copy.deepcopy(self.package)
        broken["calibration_manifest"]["canonical_ids"][0] = "arxiv:replacement"
        with self.assertRaisesRegex(r2.ContractError, "unchanged N=56"):
            r2.validate_package(broken)
        broken = copy.deepcopy(self.package)
        broken["local_reproduction_readiness"]["candidates"][0]["anchor_status"] = "REPRODUCTION_ANCHOR"
        with self.assertRaisesRegex(r2.ContractError, "promoted a reproduction anchor"):
            r2.validate_package(broken)

    def test_receiver_side_receipt_and_runtime_intake_bind_actual_bytes(self) -> None:
        intake, receipts = self.runtime()
        self.assertEqual("BOUND_FOR_PRE_ADJUDICATION_AGREEMENT", intake["status"])
        self.assertEqual({"TASK-A", "TASK-B"}, {row["task_id"] for row in intake["coder_slots"]})
        self.assertEqual(
            self.package["distribution_manifest"]["content_bundle_sha256"],
            receipts[0]["received_content_bundle_sha256"],
        )
        self.assertEqual(8, len(receipts[0]["received_artifacts"]))

    def test_receipt_and_runtime_fail_closed_on_byte_or_identity_changes(self) -> None:
        artifacts = self.actual_artifacts()
        name = r2.CODER_DISTRIBUTION_ALLOWED_ARTIFACTS[0]
        artifacts[name] = artifacts[name][:-1] + bytes([artifacts[name][-1] ^ 1])
        with self.assertRaisesRegex(r2.ContractError, "actual received artifact"):
            r2.build_delivery_receipt(
                self.package,
                received_artifacts=artifacts,
                received_prompt_bytes=r2.json_bytes(self.package["coder_prompt"]),
                slot="A", coder_id="CODER-A", transaction_id="TX-CODER-A",
                process_id="PROC-A", task_id="TASK-A", model="gpt-5.6-sol",
                delivered_at="2026-07-25T12:00:00+08:00",
                submitted_at="2026-07-25T18:00:00+08:00",
            )
        intake, receipts = self.runtime()
        del intake
        wrong = (
            {
                "slot": "A", "coder_id": "OTHER", "transaction_id": "TX-CODER-A",
                "process_id": "PROC-A", "task_id": "TASK-A", "model": "gpt-5.6-sol",
            },
            {
                "slot": "B", "coder_id": "CODER-B", "transaction_id": "TX-CODER-B",
                "process_id": "PROC-B", "task_id": "TASK-B", "model": "gpt-5.6-terra",
            },
        )
        with self.assertRaisesRegex(r2.ContractError, "coder_id"):
            r2.bind_runtime_intake(self.package, wrong, receipts)

    def test_receipt_rejects_missing_extra_nonbytes_prompt_and_invalid_model(self) -> None:
        base_kwargs = {
            "package": self.package,
            "received_artifacts": self.actual_artifacts(),
            "received_prompt_bytes": r2.json_bytes(self.package["coder_prompt"]),
            "slot": "A", "coder_id": "CODER-A", "transaction_id": "TX-CODER-A",
            "process_id": "PROC-A", "task_id": "TASK-A", "model": "gpt-5.6-sol",
            "delivered_at": "2026-07-25T12:00:00+08:00",
            "submitted_at": "2026-07-25T18:00:00+08:00",
        }
        missing = copy.deepcopy(base_kwargs)
        missing["received_artifacts"].pop(next(iter(missing["received_artifacts"])))
        with self.assertRaisesRegex(r2.ContractError, "exact actual received artifact set"):
            r2.build_delivery_receipt(**missing)
        nonbytes = copy.deepcopy(base_kwargs)
        nonbytes["received_artifacts"][r2.CODER_DISTRIBUTION_ALLOWED_ARTIFACTS[0]] = "bad"
        with self.assertRaisesRegex(r2.ContractError, "must be bytes"):
            r2.build_delivery_receipt(**nonbytes)
        bad_prompt_type = copy.deepcopy(base_kwargs)
        bad_prompt_type["received_prompt_bytes"] = "bad"
        with self.assertRaisesRegex(r2.ContractError, "prompt must be bytes"):
            r2.build_delivery_receipt(**bad_prompt_type)
        bad_prompt = copy.deepcopy(base_kwargs)
        bad_prompt["received_prompt_bytes"] = b"wrong prompt"
        with self.assertRaisesRegex(r2.ContractError, "actual received prompt differs"):
            r2.build_delivery_receipt(**bad_prompt)
        bad_model = copy.deepcopy(base_kwargs)
        bad_model["model"] = "wrong-model"
        with self.assertRaisesRegex(r2.ContractError, "invalid actual-byte delivery receipt"):
            r2.build_delivery_receipt(**bad_model)
        with self.assertRaisesRegex(r2.ContractError, "exact A/B"):
            r2.bind_runtime_intake(self.package, [], [])

    def test_full_n56_agreement_validates_frozen_root_and_compiles_raw_objects(self) -> None:
        intake, receipts = self.runtime()
        result = agreement_v6.compute_agreement(
            self.submitted_rows("A"),
            self.submitted_rows("B"),
            runtime_intake=intake,
            frozen_contract=self.package["frozen_package_contract"],
            response_schema=self.package["response_schema"],
            source_manifest=self.package["source_manifest"],
            distribution_manifest=self.package["distribution_manifest"],
            delivery_receipt_schema=self.package["delivery_receipt_schema"],
            delivery_receipts=receipts,
            positive_support_preflight=self.package["positive_support_preflight"],
        )
        self.assertEqual(56, result["paper_count"])
        self.assertEqual("FAIL", result["overall_gate_status"])
        self.assertTrue(result["compiler_owned_identity_validated"])
        self.assertTrue(result["unmatched_union_denominators_applied"])

    def test_agreement_rejects_threshold_static_root_runtime_and_receipt_mutations(self) -> None:
        with self.assertRaisesRegex(agreement_v6.AgreementError, "frozen agreement minimum"):
            agreement_v6._validate_minimum(0.84)
        intake, receipts = self.runtime()
        broken = copy.deepcopy(self.package["response_schema"])
        broken["title"] = "mutation"
        with self.assertRaisesRegex(agreement_v6.AgreementError, "response schema SHA"):
            agreement_v6._validate_static_artifacts(
                frozen=self.package["frozen_package_contract"],
                runtime_intake=intake,
                response_schema=broken,
                source_manifest=self.package["source_manifest"],
                distribution_manifest=self.package["distribution_manifest"],
                delivery_receipt_schema=self.package["delivery_receipt_schema"],
                positive_support_preflight=self.package["positive_support_preflight"],
            )
        broken_intake = copy.deepcopy(intake)
        broken_intake["coder_slots"][1]["process_id"] = broken_intake["coder_slots"][0]["process_id"]
        with self.assertRaisesRegex(agreement_v6.AgreementError, "distinct non-empty process_id"):
            agreement_v6._validate_runtime_intake(broken_intake)
        broken_receipts = copy.deepcopy(receipts)
        broken_receipts[0]["receipt_sha256"] = "0" * 64
        with self.assertRaisesRegex(agreement_v6.AgreementError, "self-digest"):
            agreement_v6._validate_delivery_receipts(
                receipts=broken_receipts,
                slots=sorted(intake["coder_slots"], key=lambda row: row["coder_slot"]),
                schema=self.package["delivery_receipt_schema"],
                distribution=self.package["distribution_manifest"],
                intake=intake,
            )

    def test_runtime_intake_guards_cover_identity_model_and_compiler_flags(self) -> None:
        intake, _ = self.runtime()
        cases = (
            ("unknown R2", lambda value: value.__setitem__("schema", "wrong")),
            ("not bound", lambda value: value.__setitem__("status", "PREPARED")),
            ("frozen agreement minimum", lambda value: value.__setitem__("agreement_minimum", 0.84)),
            ("compiler-owned", lambda value: value.__setitem__("compiler_owned_object_identity_required", False)),
            ("drops unmatched", lambda value: value.__setitem__("unmatched_objects_enter_critical_field_denominators", False)),
            ("exact N=56", lambda value: value.__setitem__("N", 55)),
            ("slots A/B", lambda value: value["coder_slots"].pop()),
            ("distinct non-empty coder_id", lambda value: value["coder_slots"][1].__setitem__("coder_id", "CODER-A")),
            ("both coder slots", lambda value: value["coder_slots"][0].__setitem__("assignment_status", "UNASSIGNED")),
            ("isolated-model", lambda value: value["coder_slots"][0].__setitem__("model", "gpt-5.6-terra")),
            ("expected content bundle", lambda value: value["coder_slots"][0].__setitem__("expected_content_bundle_sha256", "0" * 64)),
            ("expected prompt", lambda value: value["coder_slots"][0].__setitem__("expected_prompt_hash", "0" * 64)),
        )
        for message, mutate in cases:
            with self.subTest(message=message):
                broken = copy.deepcopy(intake)
                mutate(broken)
                with self.assertRaisesRegex(agreement_v6.AgreementError, message):
                    agreement_v6._validate_runtime_intake(broken)

    def test_compiler_resolves_dataset_run_observation_and_edge_references(self) -> None:
        response = self.completed_boundary()
        locator_id = response["source_locators"][0]["locator_id"]
        response["dataset_nodes"] = [
            self.dataset_node(response, object_id="DS-A", locator_id=locator_id),
            {**self.dataset_node(response, object_id="DS-B", locator_id=locator_id), "name": "MMAR"},
        ]
        response["run_cells"] = [{
            "run_cell_id": "RC-A", "dataset_node_ids": ["DS-A"], "model": "Frozen core",
            "access_regime": "TF_STRICT_BLACK_BOX", "input_condition": "audio + question",
            "intervention": "tool routing", "control_signal": "tool evidence",
            "primary_intervention_axis": "SKILL", "decision_or_action": "route tool",
            "budget_horizon": "20 calls", "baseline_role": "INTERVENTION",
            "source_locator_ids": [locator_id],
        }]
        response["observations"] = [{
            "observation_id": "OBS-A", "run_cell_id": "RC-A", "metric_or_evaluator": "accuracy",
            "outcome_semantics": "higher is better", "raw_result": "77.5%",
            "observation_role": "PRIMARY_OUTCOME", "source_locator_ids": [locator_id],
        }]
        response["dataset_edges"] = [{
            "dataset_edge_id": "DE-A", "edge_type": "RELATION", "source_dataset_id": "DS-A",
            "relation": "INDEPENDENT_SAME_TASK", "target_dataset_id": "DS-B",
            "reason": "Independent validation", "source_locator_ids": [locator_id],
        }]
        compiled = r2.compile_response_objects(response, self.package["source_manifest"])
        dataset_keys = {row["dataset_node_id"]: row["object_match_key"] for row in compiled["dataset_nodes"]}
        run_key = compiled["run_cells"][0]["object_match_key"]
        self.assertEqual([dataset_keys["DS-A"]], compiled["run_cells"][0]["dataset_node_ids"])
        self.assertEqual(run_key, compiled["observations"][0]["run_cell_id"])
        self.assertEqual(dataset_keys["DS-B"], compiled["dataset_edges"][0]["target_dataset_id"])

    def test_compiler_rejects_unknown_cross_references_and_duplicate_signatures(self) -> None:
        response = self.completed_boundary()
        locator_id = response["source_locators"][0]["locator_id"]
        response["dataset_nodes"] = [self.dataset_node(response, object_id="DS-A", locator_id=locator_id)]
        duplicate = copy.deepcopy(response["dataset_nodes"][0])
        duplicate["dataset_node_id"] = "DS-B"
        response["dataset_nodes"].append(duplicate)
        with self.assertRaisesRegex(r2.ContractError, "duplicate compiler-derived dataset_nodes"):
            r2.compile_response_objects(response, self.package["source_manifest"])

        run = self.completed_boundary()
        run["run_cells"] = [{
            "run_cell_id": "RC-A", "dataset_node_ids": ["DS-MISSING"], "model": "core",
            "access_regime": "TF_STRICT_BLACK_BOX", "input_condition": "audio",
            "intervention": "route", "control_signal": "signal",
            "primary_intervention_axis": "SKILL", "decision_or_action": "act",
            "budget_horizon": "1", "baseline_role": "INTERVENTION",
            "source_locator_ids": [run["source_locators"][0]["locator_id"]],
        }]
        with self.assertRaisesRegex(r2.ContractError, "undeclared dataset node"):
            r2.compile_response_objects(run, self.package["source_manifest"])

        undeclared_locator = self.completed_boundary()
        undeclared_locator["dataset_nodes"] = [
            self.dataset_node(undeclared_locator, object_id="DS-A", locator_id="LOC-MISSING")
        ]
        with self.assertRaisesRegex(r2.ContractError, "undeclared source locator"):
            r2.compile_response_objects(undeclared_locator, self.package["source_manifest"])

    def test_completed_response_semantic_guards_fail_closed(self) -> None:
        cases: list[tuple[str, object]] = []
        invalid_schema = self.completed_boundary()
        invalid_schema.pop("paper_id")
        cases.append(("schema validation", invalid_schema))
        blank = self.completed_boundary()
        blank["response_status"] = "BLANK_NOT_DISTRIBUTED"
        cases.append(("must be CODER_SUBMITTED", blank))
        not_coded = self.completed_boundary()
        not_coded["paper_labels"]["paper_role"] = "NOT_CODED"
        cases.append(("retains NOT_CODED", not_coded))
        pair_not_coded = self.completed_boundary()
        pair_not_coded["paired_comparison_absence_reason"] = "NOT_CODED"
        cases.append(("NOT_CODED paired", pair_not_coded))
        object_reason = self.completed_boundary()
        object_reason["dataset_nodes"] = [self.dataset_node(
            object_reason,
            object_id="DS-A",
            locator_id=object_reason["source_locators"][0]["locator_id"],
        )]
        cases.append(("objects require OBJECTS_PRESENT", object_reason))
        pair_reason = self.completed_boundary()
        pair_reason["paired_comparison_absence_reason"] = "OBJECTS_PRESENT"
        cases.append(("empty paired comparison", pair_reason))
        borrow = self.completed_boundary()
        borrow["paper_labels"]["reference_borrow_reproduce"] = "BORROW_PROTOCOL"
        cases.append(("BORROW_PROTOCOL requires", borrow))
        for message, response in cases:
            with self.subTest(message=message):
                with self.assertRaisesRegex(r2.ContractError, message):
                    r2.validate_completed_response(
                        response, self.package["response_schema"], self.package["source_manifest"]
                    )

    def test_specialized_transfer_and_reproduction_blocker_guards(self) -> None:
        specialized = self.completed_boundary()
        locator_id = specialized["source_locators"][0]["locator_id"]
        specialized["paper_labels"]["agentic_scope"]["scope_status"] = "OUT_OF_SCOPE_SPECIALIZED_SYSTEM"
        specialized["paper_labels"]["agentic_scope"]["core_dependency"] = "SPECIALIZED_MODEL_REQUIRED"
        specialized["dataset_nodes"] = [self.dataset_node(specialized, object_id="DS-A", locator_id=locator_id)]
        specialized["run_cells"] = [{
            "run_cell_id": "RC-A", "dataset_node_ids": ["DS-A"], "model": "specialized",
            "access_regime": "MIXED_OR_UNCLEAR", "input_condition": "audio",
            "intervention": "duplex", "control_signal": "signal",
            "primary_intervention_axis": "D0_SYSTEM_HARNESS", "decision_or_action": "act",
            "budget_horizon": "turn", "baseline_role": "INTERVENTION",
            "source_locator_ids": [locator_id],
        }]
        specialized["object_absence_reasons"]["dataset_nodes"] = "OBJECTS_PRESENT"
        specialized["object_absence_reasons"]["run_cells"] = "OBJECTS_PRESENT"
        with self.assertRaisesRegex(r2.ContractError, "specialized/trained exclusion"):
            r2.validate_completed_response(
                specialized, self.package["response_schema"], self.package["source_manifest"]
            )

        transfer = self.completed_boundary()
        transfer["protocol_transfer_evidence"] = [{
            "transfer_evidence_id": "TR-EVID-A", "source_domain": "TEXT_AGENT",
            "source_protocol": "observe-decide-act", "target_speech_omni_variables": ["audio evidence"],
            "preserved_decision_structure": "observe-decide-act", "source_locator_ids": [transfer["source_locators"][0]["locator_id"]],
            "rejection_condition": "no improvement", "rejection_observable": "accuracy",
            "evidence_status": "COMPLETE",
        }]
        transfer["object_absence_reasons"]["protocol_transfer_evidence"] = "OBJECTS_PRESENT"
        with self.assertRaisesRegex(r2.ContractError, "only BORROW_PROTOCOL"):
            r2.validate_completed_response(
                transfer, self.package["response_schema"], self.package["source_manifest"]
            )

        support = self.completed_boundary()
        support["paper_reproduction_support"] = [{
            "reproduction_support_id": "PRS-A", "task": "task", "dataset": "data",
            "dataset_revision": "v1", "split": "test", "official_repo": "https://example.com/repo",
            "pinned_revision": "x", "entrypoint": "main", "model_access": "MIXED_OR_UNCLEAR",
            "license_terms": "terms", "evaluator_or_ground_truth": "accuracy",
            "source_locator_ids": [support["source_locators"][0]["locator_id"]],
            "closure_status": "OPEN_WITH_BLOCKERS", "blockers": [],
        }]
        support["object_absence_reasons"]["paper_reproduction_support"] = "OBJECTS_PRESENT"
        with self.assertRaisesRegex(r2.ContractError, "requires at least one blocker"):
            r2.validate_completed_response(
                support, self.package["response_schema"], self.package["source_manifest"]
            )

    def test_positive_support_and_package_mutations_fail_closed(self) -> None:
        ledger = copy.deepcopy(self.package["positive_support_ledger"])
        ledger["evidence"]["paper_reproduction_support"] = []
        with self.assertRaisesRegex(r2.ContractError, "positive evidence"):
            r2.validate_positive_support(ledger, self.package)
        broken = copy.deepcopy(self.package)
        broken["distribution_manifest"]["distribution_authorized"] = True
        with self.assertRaisesRegex(r2.ContractError, "before independent method acceptance"):
            r2.validate_package(broken)
        broken = copy.deepcopy(self.package)
        broken["agreement"]["agreement_minimum"] = 0.84
        broken["distribution_manifest"] = r2.build_distribution_manifest(broken)
        with self.assertRaisesRegex(r2.ContractError, "threshold"):
            r2.validate_package(broken)

    def test_positive_support_rejects_wrong_class_source_rendition_and_locator(self) -> None:
        wrong = copy.deepcopy(self.package["positive_support_ledger"])
        wrong["mandatory_object_classes"].reverse()
        with self.assertRaisesRegex(r2.ContractError, "exact mandatory classes"):
            r2.validate_positive_support(wrong, self.package)
        outside = copy.deepcopy(self.package["positive_support_ledger"])
        outside["evidence"]["dataset_edges"][0]["paper_id"] = "arxiv:outside"
        with self.assertRaisesRegex(r2.ContractError, "outside unchanged N=56"):
            r2.validate_positive_support(outside, self.package)
        rendition = copy.deepcopy(self.package["positive_support_ledger"])
        rendition["evidence"]["dataset_edges"][0]["source_locators"][0]["rendition_id"] = "SRC-WRONG"
        with self.assertRaisesRegex(r2.ContractError, "outside frozen paper renditions"):
            r2.validate_positive_support(rendition, self.package)
        locator = copy.deepcopy(self.package["positive_support_ledger"])
        locator["evidence"]["dataset_edges"][0]["object"]["source_locator_ids"] = ["LOC-MISSING"]
        with self.assertRaisesRegex(r2.ContractError, "undeclared locator"):
            r2.validate_positive_support(locator, self.package)

    def test_review_manifest_fails_closed_until_exact_artifacts_exist(self) -> None:
        report = r2.build_report(self.package)
        with mock.patch.dict(r2.ARTIFACT_PATHS, {"agreement": r2.WORKBENCH / "missing.json"}, clear=True):
            with self.assertRaisesRegex(r2.ContractError, "review inputs missing"):
                r2.build_review_manifest(report)


class Stage1cV2R2GuardBranchTests(unittest.TestCase):
    def test_exact_mandatory_positive_classes_pass_and_every_deviation_fails(self) -> None:
        expected = ("dataset_edges", "paper_reproduction_support")
        self.assertEqual(
            expected,
            guards.require_exact_positive_classes(list(expected), {name: [{}] for name in expected}),
        )
        with self.assertRaisesRegex(guards.GuardError, "exact mandatory classes"):
            guards.require_exact_positive_classes(list(reversed(expected)), {name: [{}] for name in expected})
        with self.assertRaisesRegex(guards.GuardError, "positive evidence"):
            guards.require_exact_positive_classes(list(expected), {expected[0]: [{}], expected[1]: []})

    def test_paper_local_observability_split_passes_and_both_leaks_fail(self) -> None:
        schema = {"$defs": {"paper_reproduction_support": {"properties": {"task": {}}}}}
        guards.require_paper_local_observability_split(
            schema, ("response_schema", "coder_prompt"), "local_reproduction_readiness"
        )
        leaked_schema = copy.deepcopy(schema)
        leaked_schema["$defs"]["paper_reproduction_support"]["properties"]["local_asset_state"] = {}
        with self.assertRaisesRegex(guards.GuardError, "local state"):
            guards.require_paper_local_observability_split(
                leaked_schema, ("response_schema",), "local_reproduction_readiness"
            )
        with self.assertRaisesRegex(guards.GuardError, "reviewer-only artifact"):
            guards.require_paper_local_observability_split(
                schema, ("response_schema", "local_reproduction_readiness"),
                "local_reproduction_readiness",
            )

    def test_object_gate_status_has_only_both_zero_not_calibrated(self) -> None:
        self.assertEqual("NOT_CALIBRATED", guards.object_gate_status(0, 0, ["NOT_CALIBRATED"]))
        self.assertEqual("PASS", guards.object_gate_status(1, 1, ["PASS", "PASS"]))
        self.assertEqual("FAIL", guards.object_gate_status(1, 0, ["FAIL", "FAIL"]))


if __name__ == "__main__":
    unittest.main()
