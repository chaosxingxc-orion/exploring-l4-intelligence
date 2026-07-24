from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path
from unittest import mock

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import sf_stage1c_v2_calibration_agreement_v5 as agreement_v5
    import sf_stage1c_v2_precalibration_rc2r3 as rc2r3
else:
    from scripts.survey import sf_stage1c_v2_calibration_agreement_v5 as agreement_v5
    from scripts.survey import sf_stage1c_v2_precalibration_rc2r3 as rc2r3


class Stage1cV2PrecalibrationRc2r3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.package = rc2r3.build_package()

    def actual_artifacts(self, package: dict | None = None) -> dict[str, bytes]:
        package = package or self.package
        return {
            name: rc2r3.json_bytes(package[name])
            for name in rc2r3.CODER_DISTRIBUTION_ALLOWED_ARTIFACTS
        }

    def receipt(self, package: dict | None = None, *, slot: str = "A") -> dict:
        package = package or self.package
        model = "gpt-5.6-sol" if slot == "A" else "gpt-5.6-terra"
        return rc2r3.build_delivery_receipt(
            package,
            received_artifacts=self.actual_artifacts(package),
            received_prompt_bytes=rc2r3.json_bytes(package["coder_prompt"]),
            slot=slot,
            coder_id=f"CODER-{slot}",
            transaction_id=f"TX-{slot}",
            process_id=f"PROC-{slot}",
            task_id=f"TASK-{slot}",
            model=model,
            delivered_at="2026-07-24T19:00:00+08:00",
            submitted_at="2026-07-24T21:00:00+08:00",
        )

    def submitted_rows(self, coder_id: str, transaction_id: str) -> list[dict]:
        rows: list[dict] = []
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
                        "scope_reason": "Runtime-integrity fixture.",
                    },
                },
                "source_locators": [{
                    "locator_id": f"LOC-FIXTURE-{index:02d}",
                    "rendition_id": source["primary_rendition"]["rendition_id"],
                    "anchor_type": "PAGE", "anchor_value": "1",
                    "precise_locator": "Page 1, fixture evidence.",
                }],
                "review_events": [{
                    "event_id": f"REV-{coder_id}-{index:02d}",
                    "event_type": "CODER_SUBMISSION",
                    "timestamp": "2026-07-24T20:00:00+08:00", "prior_event_id": None,
                }],
            })
            response["object_absence_reasons"] = {
                name: "NOT_APPLICABLE_NON_EMPIRICAL"
                for name in rc2r3.BASE_CALIBRATED_OBJECT_ARRAYS
            }
            rows.append(response)
        return rows

    def runtime(self) -> tuple[dict, list[dict]]:
        bindings = (
            {"slot": "A", "coder_id": "CODER-A", "transaction_id": "TX-A", "process_id": "PROC-A", "task_id": "TASK-A", "model": "gpt-5.6-sol"},
            {"slot": "B", "coder_id": "CODER-B", "transaction_id": "TX-B", "process_id": "PROC-B", "task_id": "TASK-B", "model": "gpt-5.6-terra"},
        )
        receipts = [self.receipt(slot="A"), self.receipt(slot="B")]
        return rc2r3.bind_runtime_intake(self.package, bindings, receipts), receipts

    def test_rc2r3_is_immutable_successor_and_uses_v5_contracts(self) -> None:
        report = rc2r3.build_report(self.package)
        self.assertEqual("AGENTIC_RC2R3_CODER_READY_NOT_DISTRIBUTED", report["status"])
        self.assertEqual(0.85, agreement_v5.AGREEMENT_MINIMUM)
        self.assertEqual(0.85, self.package["agreement"]["agreement_minimum"])
        self.assertEqual(
            agreement_v5.FROZEN_CONTRACT_SHA256,
            rc2r3.sha256_bytes(rc2r3.json_bytes(self.package["frozen_package_contract"])),
        )
        self.assertTrue(all(
            "system-first-stage1c-v2-precalibration-rc2r3" in path.as_posix()
            for path in rc2r3.ARTIFACT_PATHS.values()
        ))

    def test_threshold_cannot_be_lowered_or_changed_by_caller(self) -> None:
        for value in (0.01, 0.84, 0.86, 1.0):
            with self.subTest(value=value):
                with self.assertRaisesRegex(agreement_v5.AgreementError, "frozen agreement minimum"):
                    agreement_v5._validate_minimum(value)
        self.assertEqual(0.85, agreement_v5._validate_minimum(0.85))

    def test_happy_exact_runtime_reaches_per_critical_path_metrics(self) -> None:
        intake, receipts = self.runtime()
        result = agreement_v5.compute_agreement(
            self.submitted_rows("CODER-A", "TX-A"),
            self.submitted_rows("CODER-B", "TX-B"),
            runtime_intake=intake,
            frozen_contract=self.package["frozen_package_contract"],
            response_schema=self.package["response_schema"],
            source_manifest=self.package["source_manifest"],
            distribution_manifest=self.package["distribution_manifest"],
            delivery_receipt_schema=self.package["delivery_receipt_schema"],
            delivery_receipts=receipts,
        )
        self.assertEqual(56, result["paper_count"])
        self.assertEqual(0.85, result["minimum"])
        self.assertEqual("FAIL", result["overall_gate_status"])
        self.assertTrue(result["frozen_provenance_validated"])

    def test_compute_rejects_threshold_override_before_metrics(self) -> None:
        for minimum in (0.01, 0.84, 0.86, 1.0):
            with self.subTest(minimum=minimum):
                with self.assertRaisesRegex(agreement_v5.AgreementError, "frozen agreement minimum"):
                    agreement_v5.compute_agreement(
                        [], [], runtime_intake={}, frozen_contract={}, response_schema={},
                        source_manifest={}, distribution_manifest={}, delivery_receipt_schema={},
                        delivery_receipts=[], minimum=minimum,
                    )

    def test_static_artifact_hash_guards_reject_mutations(self) -> None:
        intake, _ = self.runtime()
        cases = (
            ("response schema SHA", "response_schema", "$id"),
            ("source manifest SHA", "source_manifest", "status"),
            ("distribution manifest SHA", "distribution_manifest", "status"),
            ("delivery receipt schema SHA", "delivery_receipt_schema", "title"),
        )
        for message, name, field in cases:
            with self.subTest(name=name):
                artifact = copy.deepcopy(self.package[name])
                artifact[field] = "MUTATED"
                kwargs = {
                    "response_schema": self.package["response_schema"],
                    "source_manifest": self.package["source_manifest"],
                    "distribution_manifest": self.package["distribution_manifest"],
                    "delivery_receipt_schema": self.package["delivery_receipt_schema"],
                }
                kwargs[name] = artifact
                with self.assertRaisesRegex(agreement_v5.AgreementError, message):
                    agreement_v5._validate_static_artifacts(
                        frozen=self.package["frozen_package_contract"],
                        runtime_intake=intake, **kwargs,
                    )

    def test_compiled_root_and_runtime_intake_guards_fail_closed(self) -> None:
        intake, _ = self.runtime()
        frozen = copy.deepcopy(self.package["frozen_package_contract"])
        frozen["agreement_minimum"] = 0.84
        with self.assertRaisesRegex(agreement_v5.AgreementError, "compiled RC2R3 frozen contract"):
            agreement_v5._validate_static_artifacts(
                frozen=frozen, runtime_intake=intake,
                response_schema=self.package["response_schema"],
                source_manifest=self.package["source_manifest"],
                distribution_manifest=self.package["distribution_manifest"],
                delivery_receipt_schema=self.package["delivery_receipt_schema"],
            )
        cases = (
            ("unknown RC2R3", lambda value: value.__setitem__("schema", "wrong")),
            ("not bound", lambda value: value.__setitem__("status", "UNASSIGNED")),
            ("frozen agreement minimum", lambda value: value.__setitem__("agreement_minimum", 0.84)),
            ("exact N=56", lambda value: value.__setitem__("N", 55)),
            ("coder slots A/B", lambda value: value["coder_slots"].pop()),
            ("distinct non-empty coder_id", lambda value: value["coder_slots"][1].__setitem__("coder_id", "CODER-A")),
            ("distinct non-empty coder_transaction_id", lambda value: value["coder_slots"][1].__setitem__("coder_transaction_id", "TX-A")),
            ("distinct non-empty process_id", lambda value: value["coder_slots"][1].__setitem__("process_id", "PROC-A")),
            ("distinct non-empty task_id", lambda value: value["coder_slots"][1].__setitem__("task_id", "TASK-A")),
            ("both coder slots", lambda value: value["coder_slots"][0].__setitem__("assignment_status", "UNASSIGNED")),
            ("isolated-model plan", lambda value: value["coder_slots"][0].__setitem__("model", "gpt-5.6-terra")),
            ("expected content bundle", lambda value: value["coder_slots"][0].__setitem__("expected_content_bundle_sha256", "0" * 64)),
            ("expected prompt", lambda value: value["coder_slots"][0].__setitem__("expected_prompt_hash", "0" * 64)),
        )
        for message, mutate in cases:
            with self.subTest(message=message):
                broken = copy.deepcopy(intake)
                mutate(broken)
                with self.assertRaisesRegex(agreement_v5.AgreementError, message):
                    agreement_v5._validate_runtime_intake(broken)

    def test_receipt_is_derived_from_actual_bytes(self) -> None:
        receipt = self.receipt()
        expected = self.package["distribution_manifest"]
        self.assertEqual(expected["content_bundle_sha256"], receipt["received_content_bundle_sha256"])
        self.assertEqual(expected["coder_prompt_sha256"], receipt["received_prompt_sha256"])
        self.assertEqual("TASK-A", receipt["task_id"])
        self.assertEqual(len(rc2r3.CODER_DISTRIBUTION_ALLOWED_ARTIFACTS), len(receipt["received_artifacts"]))

    def test_one_byte_artifact_or_prompt_mutation_fails_closed(self) -> None:
        artifacts = self.actual_artifacts()
        first = rc2r3.CODER_DISTRIBUTION_ALLOWED_ARTIFACTS[0]
        artifacts[first] = artifacts[first][:-1] + bytes([artifacts[first][-1] ^ 1])
        with self.assertRaisesRegex(rc2r3.ContractError, "actual received artifact"):
            rc2r3.build_delivery_receipt(
                self.package, received_artifacts=artifacts,
                received_prompt_bytes=rc2r3.json_bytes(self.package["coder_prompt"]),
                slot="A", coder_id="CODER-A", transaction_id="TX-A",
                process_id="PROC-A", task_id="TASK-A", model="gpt-5.6-sol",
                delivered_at="2026-07-24T19:00:00+08:00",
                submitted_at="2026-07-24T21:00:00+08:00",
            )
        prompt = rc2r3.json_bytes(self.package["coder_prompt"])
        prompt = prompt[:-1] + bytes([prompt[-1] ^ 1])
        with self.assertRaisesRegex(rc2r3.ContractError, "actual received prompt"):
            rc2r3.build_delivery_receipt(
                self.package, received_artifacts=self.actual_artifacts(),
                received_prompt_bytes=prompt, slot="A", coder_id="CODER-A",
                transaction_id="TX-A", process_id="PROC-A", task_id="TASK-A",
                model="gpt-5.6-sol", delivered_at="2026-07-24T19:00:00+08:00",
                submitted_at="2026-07-24T21:00:00+08:00",
            )

    def test_receipt_requires_exact_actual_artifact_set_and_bytes_types(self) -> None:
        artifacts = self.actual_artifacts()
        artifacts.pop(next(iter(artifacts)))
        with self.assertRaisesRegex(rc2r3.ContractError, "exact actual received artifact set"):
            rc2r3.build_delivery_receipt(
                self.package, received_artifacts=artifacts,
                received_prompt_bytes=rc2r3.json_bytes(self.package["coder_prompt"]),
                slot="A", coder_id="CODER-A", transaction_id="TX-A",
                process_id="PROC-A", task_id="TASK-A", model="gpt-5.6-sol",
                delivered_at="2026-07-24T19:00:00+08:00",
                submitted_at="2026-07-24T21:00:00+08:00",
            )

    def test_receipt_schema_and_binding_guards_fail_closed(self) -> None:
        kwargs = {
            "received_artifacts": self.actual_artifacts(),
            "received_prompt_bytes": rc2r3.json_bytes(self.package["coder_prompt"]),
            "slot": "A", "coder_id": "CODER-A", "transaction_id": "TX-A",
            "process_id": "PROC-A", "task_id": "TASK-A", "model": "wrong-model",
            "delivered_at": "2026-07-24T19:00:00+08:00",
            "submitted_at": "2026-07-24T21:00:00+08:00",
        }
        with self.assertRaisesRegex(rc2r3.ContractError, "invalid actual-byte delivery receipt"):
            rc2r3.build_delivery_receipt(self.package, **kwargs)
        intake, receipts = self.runtime()
        bindings = (
            {"slot": "A", "coder_id": "OTHER", "transaction_id": "TX-A", "process_id": "PROC-A", "task_id": "TASK-A", "model": "gpt-5.6-sol"},
            {"slot": "B", "coder_id": "CODER-B", "transaction_id": "TX-B", "process_id": "PROC-B", "task_id": "TASK-B", "model": "gpt-5.6-terra"},
        )
        with self.assertRaisesRegex(rc2r3.ContractError, "coder_id"):
            rc2r3.bind_runtime_intake(self.package, bindings, receipts)
        with self.assertRaisesRegex(rc2r3.ContractError, "exact A/B"):
            rc2r3.bind_runtime_intake(self.package, bindings[:1], receipts[:1])

    def test_delivery_receipt_semantic_mutations_fail_closed(self) -> None:
        intake, receipts = self.runtime()

        def resign(receipt: dict) -> None:
            receipt["receipt_sha256"] = rc2r3.sha256_bytes(
                rc2r3.json_bytes(rc2r3._receipt_projection(receipt))
            )

        cases = (
            ("invalid delivery receipt", lambda rs, it: rs[0].pop("coder_id")),
            ("self-digest", lambda rs, it: rs[0].__setitem__("receipt_sha256", "0" * 64)),
            ("coder_id", lambda rs, it: (rs[0].__setitem__("coder_id", "OTHER"), resign(rs[0]))),
            ("invalid delivery receipt", lambda rs, it: (rs[0].__setitem__("distribution_manifest_id", "OTHER"), resign(rs[0]))),
            ("actual content bundle", lambda rs, it: (rs[0].__setitem__("received_content_bundle_sha256", "0" * 64), resign(rs[0]))),
            ("actual prompt", lambda rs, it: (rs[0].__setitem__("received_prompt_sha256", "0" * 64), resign(rs[0]))),
            ("actual artifact bytes", lambda rs, it: (rs[0]["received_artifacts"][0].__setitem__("sha256", "0" * 64), resign(rs[0]))),
            ("delivery_receipt_id", lambda rs, it: it["coder_slots"][0].__setitem__("delivery_receipt_id", "OTHER")),
            ("delivery receipt digest", lambda rs, it: it["coder_slots"][0].__setitem__("delivery_receipt_sha256", "0" * 64)),
            ("actual content bundle", lambda rs, it: it["coder_slots"][0].__setitem__("received_content_bundle_sha256", "0" * 64)),
            ("actual prompt", lambda rs, it: it["coder_slots"][0].__setitem__("received_prompt_sha256", "0" * 64)),
        )
        for message, mutate in cases:
            with self.subTest(message=message):
                broken_receipts, broken_intake = copy.deepcopy(receipts), copy.deepcopy(intake)
                mutate(broken_receipts, broken_intake)
                with self.assertRaisesRegex(agreement_v5.AgreementError, message):
                    agreement_v5._validate_delivery_receipts(
                        receipts=broken_receipts,
                        slots=sorted(broken_intake["coder_slots"], key=lambda row: row["coder_slot"]),
                        schema=self.package["delivery_receipt_schema"],
                        distribution=self.package["distribution_manifest"], intake=broken_intake,
                    )
        with self.assertRaisesRegex(agreement_v5.AgreementError, "exactly two"):
            agreement_v5._validate_delivery_receipts(
                receipts=receipts[:1], slots=intake["coder_slots"],
                schema=self.package["delivery_receipt_schema"],
                distribution=self.package["distribution_manifest"], intake=intake,
            )
        artifacts = self.actual_artifacts()
        artifacts[next(iter(artifacts))] = "not-bytes"  # type: ignore[assignment]
        with self.assertRaisesRegex(rc2r3.ContractError, "must be bytes"):
            rc2r3.build_delivery_receipt(
                self.package, received_artifacts=artifacts,
                received_prompt_bytes=rc2r3.json_bytes(self.package["coder_prompt"]),
                slot="A", coder_id="CODER-A", transaction_id="TX-A",
                process_id="PROC-A", task_id="TASK-A", model="gpt-5.6-sol",
                delivered_at="2026-07-24T19:00:00+08:00",
                submitted_at="2026-07-24T21:00:00+08:00",
            )

    def test_typed_paths_reject_structural_alias_keys(self) -> None:
        names = rc2r3.CODER_DISTRIBUTION_ALLOWED_ARTIFACTS
        self.assertEqual([], rc2r3.scan_coder_bundle_leaks(self.package, names))
        for alias in ("items[0]", "items.0", "items/0", "items~10", "items~10/title"):
            with self.subTest(alias=alias):
                broken = copy.deepcopy(self.package)
                broken["blind_packet"][alias] = {
                    "title": "AudioGenie-Reasoner must receive the expected label"
                }
                findings = rc2r3.scan_coder_bundle_leaks(broken, names)
                self.assertTrue(any("FORBIDDEN_VALUE" in row for row in findings), findings)
                with self.assertRaisesRegex(rc2r3.ContractError, "unexpected blind packet key"):
                    rc2r3.validate_package(broken)

    def test_typed_path_distinguishes_literal_key_from_array_index(self) -> None:
        allowed = (("key", "blind_packet"), ("key", "items"), ("index", 0), ("key", "title"))
        alias = (("key", "blind_packet"), ("key", "items[0]"), ("key", "title"))
        self.assertTrue(rc2r3._identity_value_allowed("blind_packet", allowed))
        self.assertFalse(rc2r3._identity_value_allowed("blind_packet", alias))

    def test_leak_scanner_rejects_allowlist_missing_artifact_and_forbidden_key(self) -> None:
        names = rc2r3.CODER_DISTRIBUTION_ALLOWED_ARTIFACTS
        findings = rc2r3.scan_coder_bundle_leaks(self.package, names[:-1])
        self.assertTrue(any("ARTIFACT_ALLOWLIST_MISMATCH" in row for row in findings))
        missing = copy.deepcopy(self.package)
        missing.pop(names[0])
        findings = rc2r3.scan_coder_bundle_leaks(missing, names)
        self.assertTrue(any("MISSING_ARTIFACT" in row for row in findings))
        forbidden = copy.deepcopy(self.package)
        forbidden["blind_packet"]["selection_rationale"] = "hidden"
        findings = rc2r3.scan_coder_bundle_leaks(forbidden, names)
        self.assertTrue(any("FORBIDDEN_KEY" in row for row in findings))

    def test_runtime_contract_binds_task_identity_and_actual_receipts(self) -> None:
        bindings = (
            {"slot": "A", "coder_id": "CODER-A", "transaction_id": "TX-A", "process_id": "PROC-A", "task_id": "TASK-A", "model": "gpt-5.6-sol"},
            {"slot": "B", "coder_id": "CODER-B", "transaction_id": "TX-B", "process_id": "PROC-B", "task_id": "TASK-B", "model": "gpt-5.6-terra"},
        )
        receipts = [self.receipt(slot="A"), self.receipt(slot="B")]
        intake = rc2r3.bind_runtime_intake(self.package, bindings, receipts)
        self.assertEqual({"TASK-A", "TASK-B"}, {row["task_id"] for row in intake["coder_slots"]})
        broken = copy.deepcopy(receipts)
        broken[0]["task_id"] = "TASK-FORGED"
        broken[0]["receipt_sha256"] = rc2r3.sha256_bytes(
            rc2r3.json_bytes(rc2r3._receipt_projection(broken[0]))
        )
        with self.assertRaisesRegex(agreement_v5.AgreementError, "task_id"):
            agreement_v5._validate_delivery_receipts(
                receipts=broken,
                slots=sorted(intake["coder_slots"], key=lambda row: row["coder_slot"]),
                schema=self.package["delivery_receipt_schema"],
                distribution=self.package["distribution_manifest"], intake=intake,
            )

    def test_no_execution_or_distribution_is_recorded(self) -> None:
        report = rc2r3.build_report(self.package)
        for field in (
            "coder_distributed", "agreement_computed", "research_model_called",
            "benchmark_metric_run", "paper_reproduction_run", "prototype_created",
            "novelty_verdict_made", "full_mapping_signed", "push_authorized",
        ):
            self.assertFalse(report["authority"][field])

    def test_static_projection_and_package_guards_fail_closed(self) -> None:
        with self.assertRaisesRegex(rc2r3.ContractError, "lacks frozen RC2R3"):
            rc2r3.static_intake_projection({})
        mutations = (
            ("duplicate canonical", lambda p: p["calibration_manifest"]["canonical_ids"].__setitem__(1, p["calibration_manifest"]["canonical_ids"][0])),
            ("distributed coders", lambda p: p["distribution_manifest"].__setitem__("distribution_authorized", True)),
            ("coder-visible leakage", lambda p: p["blind_packet"]["items"][0].__setitem__("selection_rationale", "hidden")),
            ("coder bundle hash", lambda p: p["distribution_manifest"].__setitem__("content_bundle_sha256", "0" * 64)),
            ("distribution artifact", lambda p: p["distribution_manifest"]["artifacts"][0].__setitem__("sha256", "0" * 64)),
            ("agreement minimum", lambda p: p["agreement_intake_contract"].__setitem__("agreement_minimum", 0.84)),
            ("prepared-not-distributed", lambda p: p["agreement_intake_contract"].__setitem__("status", "BOUND")),
            ("agreement contract threshold", lambda p: (
                p["agreement"].__setitem__("agreement_minimum", 0.84),
                p.__setitem__("distribution_manifest", rc2r3.build_distribution_manifest(p)),
            )),
            ("frozen package contract", lambda p: p["frozen_package_contract"].__setitem__("N", 55)),
            ("promoted a reproduction anchor", lambda p: p["reproduction_readiness"]["candidates"][0].__setitem__("method_anchor_eligible", True)),
            ("research execution", lambda p: p["reproduction_readiness"]["candidates"][0].__setitem__("research_execution_performed", True)),
        )
        for message, mutate in mutations:
            with self.subTest(message=message):
                broken = copy.deepcopy(self.package)
                mutate(broken)
                with self.assertRaisesRegex(rc2r3.ContractError, message):
                    rc2r3.validate_package(broken)

    def test_completed_response_and_review_manifest_fail_closed(self) -> None:
        response = self.submitted_rows("CODER-A", "TX-A")[0]
        response["response_status"] = "BLANK_NOT_DISTRIBUTED"
        with self.assertRaises(rc2r3.ContractError):
            rc2r3.validate_completed_response(
                response, self.package["response_schema"], self.package["source_manifest"]
            )
        report = rc2r3.build_report(self.package)
        with mock.patch.dict(rc2r3.ARTIFACT_PATHS, {"agreement": rc2r3.WORKBENCH / "missing.json"}, clear=True):
            with self.assertRaisesRegex(rc2r3.ContractError, "review inputs missing"):
                rc2r3.build_review_manifest(report)


if __name__ == "__main__":
    unittest.main()
