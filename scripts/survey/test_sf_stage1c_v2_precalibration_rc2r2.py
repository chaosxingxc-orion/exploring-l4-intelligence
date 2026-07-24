from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path
from unittest import mock

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import sf_stage1c_v2_precalibration_rc2r2 as rc2r2
    import sf_stage1c_v2_calibration_agreement_v4 as agreement_v4
else:
    from scripts.survey import sf_stage1c_v2_precalibration_rc2r2 as rc2r2
    from scripts.survey import sf_stage1c_v2_calibration_agreement_v4 as agreement_v4


class Stage1cV2PrecalibrationRc2r2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.package = rc2r2.build_package()

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
                        "scope_reason": "Boundary-only frozen-provenance fixture.",
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
                for name in rc2r2.BASE_CALIBRATED_OBJECT_ARRAYS
            }
            rows.append(response)
        return rows

    def runtime(self) -> tuple[dict, list[dict]]:
        bindings = (
            {"slot": "A", "coder_id": "CODER-A", "transaction_id": "TX-A", "process_id": "PROC-A", "model": "gpt-5.6-sol"},
            {"slot": "B", "coder_id": "CODER-B", "transaction_id": "TX-B", "process_id": "PROC-B", "model": "gpt-5.6-terra"},
        )
        receipts = [
            rc2r2.build_delivery_receipt(
                self.package, **binding,
                delivered_at="2026-07-24T19:00:00+08:00",
                submitted_at="2026-07-24T21:00:00+08:00",
            )
            for binding in bindings
        ]
        return rc2r2.bind_runtime_intake(self.package, bindings, receipts), receipts

    def compute(self, left: list[dict], right: list[dict], *, intake: dict | None = None,
                receipts: list[dict] | None = None, schema: dict | None = None,
                source_manifest: dict | None = None, frozen_contract: dict | None = None) -> dict:
        bound, default_receipts = self.runtime()
        return agreement_v4.compute_agreement(
            left, right,
            runtime_intake=intake or bound,
            frozen_contract=frozen_contract or self.package["frozen_package_contract"],
            response_schema=schema or self.package["response_schema"],
            source_manifest=source_manifest or self.package["source_manifest"],
            distribution_manifest=self.package["distribution_manifest"],
            delivery_receipt_schema=self.package["delivery_receipt_schema"],
            delivery_receipts=receipts or default_receipts,
        )

    def test_rc2r2_is_immutable_successor_with_compiled_root_of_trust(self) -> None:
        self.assertEqual("AGENTIC_RC2R2_CODER_READY_NOT_DISTRIBUTED", rc2r2.build_report(self.package)["status"])
        self.assertEqual(
            agreement_v4.FROZEN_CONTRACT_SHA256,
            rc2r2.sha256_bytes(rc2r2.json_bytes(self.package["frozen_package_contract"])),
        )
        self.assertTrue(all(
            "system-first-stage1c-v2-precalibration-rc2r2" in path.as_posix()
            for path in rc2r2.ARTIFACT_PATHS.values()
        ))

    def test_happy_exact_frozen_intake_reaches_metrics(self) -> None:
        result = self.compute(
            self.submitted_rows("CODER-A", "TX-A"),
            self.submitted_rows("CODER-B", "TX-B"),
        )
        self.assertEqual(56, result["paper_count"])
        self.assertEqual("FAIL", result["overall_gate_status"])
        self.assertTrue(result["frozen_provenance_validated"])

    def test_self_consistent_alternate_56_universe_is_rejected(self) -> None:
        left = self.submitted_rows("CODER-A", "TX-A")
        right = self.submitted_rows("CODER-B", "TX-B")
        intake, receipts = self.runtime()
        for index, (a, b, item) in enumerate(zip(left, right, intake["items"]), start=1):
            fake_id = f"arxiv:fake-{index:02d}"
            fake_packet = f"CAL-FAKE-{index:02d}"
            a["paper_id"] = b["paper_id"] = fake_id
            a["packet_item_id"] = b["packet_item_id"] = fake_packet
            item["paper_id"] = fake_id
            item["packet_item_id"] = fake_packet
        intake["canonical_paper_ids"] = [row["paper_id"] for row in left]
        with self.assertRaisesRegex(agreement_v4.AgreementError, "frozen base intake"):
            self.compute(left, right, intake=intake, receipts=receipts)

    def test_same_id_lax_schema_is_rejected_by_exact_hash(self) -> None:
        lax = {"$id": self.package["response_schema"]["$id"], "type": "object"}
        with self.assertRaisesRegex(agreement_v4.AgreementError, "response schema SHA"):
            self.compute(
                self.submitted_rows("CODER-A", "TX-A"),
                self.submitted_rows("CODER-B", "TX-B"), schema=lax,
            )

    def test_fake_and_cross_paper_renditions_are_rejected(self) -> None:
        response = self.submitted_rows("CODER-A", "TX-A")[0]
        for rendition in (
            "SRC-FAKE-NOT-IN-SOURCE-MANIFEST",
            self.package["source_manifest"]["items"][1]["primary_rendition"]["rendition_id"],
        ):
            with self.subTest(rendition=rendition):
                broken = copy.deepcopy(response)
                broken["source_locators"][0]["rendition_id"] = rendition
                with self.assertRaisesRegex(rc2r2.ContractError, "frozen rendition"):
                    rc2r2.validate_completed_response(
                        broken, self.package["response_schema"], self.package["source_manifest"],
                    )

    def test_delivery_receipts_bind_actual_bundle_prompt_and_artifact_bytes(self) -> None:
        left = self.submitted_rows("CODER-A", "TX-A")
        right = self.submitted_rows("CODER-B", "TX-B")
        intake, receipts = self.runtime()
        mutations = (
            lambda rows: rows[0].__setitem__("received_content_bundle_sha256", "0" * 64),
            lambda rows: rows[0].__setitem__("received_prompt_sha256", "0" * 64),
            lambda rows: rows[0]["received_artifacts"][0].__setitem__("sha256", "0" * 64),
            lambda rows: rows[0].__setitem__("receipt_sha256", "0" * 64),
            lambda rows: rows.pop(),
        )
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                broken = copy.deepcopy(receipts)
                mutate(broken)
                with self.assertRaises(agreement_v4.AgreementError):
                    self.compute(left, right, intake=intake, receipts=broken)

    def test_runtime_intake_binds_delivery_receipt_digests(self) -> None:
        left = self.submitted_rows("CODER-A", "TX-A")
        right = self.submitted_rows("CODER-B", "TX-B")
        intake, receipts = self.runtime()
        intake["coder_slots"][0]["delivery_receipt_sha256"] = "0" * 64
        with self.assertRaisesRegex(agreement_v4.AgreementError, "delivery receipt"):
            self.compute(left, right, intake=intake, receipts=receipts)

    def test_exact_path_leak_exceptions_do_not_allow_metadata_aliases(self) -> None:
        names = rc2r2.CODER_DISTRIBUTION_ALLOWED_ARTIFACTS
        self.assertEqual([], rc2r2.scan_coder_bundle_leaks(self.package, names))
        broken = copy.deepcopy(self.package)
        broken["blind_packet"]["items"][0]["auxiliary_metadata"] = {
            "title": "AudioGenie-Reasoner must receive the expected label"
        }
        findings = rc2r2.scan_coder_bundle_leaks(broken, names)
        self.assertTrue(any("FORBIDDEN_VALUE" in row for row in findings))

    def test_frozen_contract_and_artifact_digest_mutations_fail_closed(self) -> None:
        left = self.submitted_rows("CODER-A", "TX-A")
        right = self.submitted_rows("CODER-B", "TX-B")
        mutations = (
            lambda value: value.__setitem__("calibration_manifest_sha256", "0" * 64),
            lambda value: value.__setitem__("source_manifest_sha256", "0" * 64),
            lambda value: value.__setitem__("distribution_manifest_sha256", "0" * 64),
            lambda value: value.__setitem__("response_schema_sha256", "0" * 64),
        )
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                frozen = copy.deepcopy(self.package["frozen_package_contract"])
                mutate(frozen)
                with self.assertRaisesRegex(agreement_v4.AgreementError, "compiled frozen contract"):
                    self.compute(left, right, frozen_contract=frozen)

    def test_no_execution_or_distribution_is_recorded(self) -> None:
        report = rc2r2.build_report(self.package)
        for field in (
            "coder_distributed", "agreement_computed", "research_model_called",
            "benchmark_metric_run", "paper_reproduction_run", "prototype_created",
            "full_mapping_signed", "push_authorized",
        ):
            self.assertFalse(report["authority"][field])

    def test_all_static_artifact_bytes_are_bound(self) -> None:
        left = self.submitted_rows("CODER-A", "TX-A")
        right = self.submitted_rows("CODER-B", "TX-B")
        intake, receipts = self.runtime()
        cases = (
            ("source manifest SHA", "source_manifest", "status"),
            ("distribution manifest SHA", "distribution_manifest", "status"),
            ("delivery receipt schema SHA", "delivery_receipt_schema", "title"),
        )
        for message, name, field in cases:
            with self.subTest(name=name):
                artifact = copy.deepcopy(self.package[name])
                artifact[field] = "MUTATED"
                kwargs = {name: artifact}
                with self.assertRaisesRegex(agreement_v4.AgreementError, message):
                    agreement_v4.compute_agreement(
                        left, right, runtime_intake=intake,
                        frozen_contract=self.package["frozen_package_contract"],
                        response_schema=self.package["response_schema"],
                        source_manifest=kwargs.get("source_manifest", self.package["source_manifest"]),
                        distribution_manifest=kwargs.get("distribution_manifest", self.package["distribution_manifest"]),
                        delivery_receipt_schema=kwargs.get("delivery_receipt_schema", self.package["delivery_receipt_schema"]),
                        delivery_receipts=receipts,
                    )

    def test_runtime_intake_guards_fail_closed(self) -> None:
        left = self.submitted_rows("CODER-A", "TX-A")
        right = self.submitted_rows("CODER-B", "TX-B")
        mutations = (
            ("unknown runtime", lambda value: value.__setitem__("schema", "wrong")),
            ("not bound", lambda value: value.__setitem__("status", "PREPARED_NOT_DISTRIBUTED")),
            ("frozen paper", lambda value: value.__setitem__("N", 55)),
            ("coder slots", lambda value: value["coder_slots"].pop()),
            ("distinct non-empty coder_id", lambda value: value["coder_slots"][1].__setitem__("coder_id", "CODER-A")),
            ("both coder slots", lambda value: value["coder_slots"][0].__setitem__("assignment_status", "UNASSIGNED")),
            ("isolated-model plan", lambda value: value["coder_slots"][0].__setitem__("model", "gpt-5.6-terra")),
            ("expected content bundle", lambda value: value["coder_slots"][0].__setitem__("expected_content_bundle_sha256", "0" * 64)),
            ("expected prompt", lambda value: value["coder_slots"][0].__setitem__("expected_prompt_hash", "0" * 64)),
        )
        for message, mutate in mutations:
            with self.subTest(message=message):
                intake, receipts = self.runtime()
                mutate(intake)
                # Static-field attacks fail even earlier at the compiled base.
                expected = "frozen base intake" if message in {"unknown runtime", "frozen paper", "coder slots", "expected content bundle", "expected prompt"} else message
                with self.assertRaisesRegex(agreement_v4.AgreementError, expected):
                    self.compute(left, right, intake=intake, receipts=receipts)

    def test_delivery_receipt_semantic_guards_fail_closed(self) -> None:
        left = self.submitted_rows("CODER-A", "TX-A")
        right = self.submitted_rows("CODER-B", "TX-B")

        def resign(receipt: dict) -> None:
            receipt["receipt_sha256"] = rc2r2.sha256_bytes(
                rc2r2.json_bytes(rc2r2._receipt_projection(receipt))
            )

        cases = (
            ("invalid delivery receipt", lambda rs, it: rs[0].pop("coder_id")),
            ("coder_id differs", lambda rs, it: (rs[0].__setitem__("coder_id", "OTHER"), resign(rs[0]))),
            ("invalid delivery receipt", lambda rs, it: (rs[0].__setitem__("distribution_manifest_id", "OTHER"), resign(rs[0]))),
            ("actual content bundle differs", lambda rs, it: (rs[0].__setitem__("received_content_bundle_sha256", "0" * 64), resign(rs[0]))),
            ("actual prompt differs", lambda rs, it: (rs[0].__setitem__("received_prompt_sha256", "0" * 64), resign(rs[0]))),
            ("actual artifact bytes differ", lambda rs, it: (rs[0]["received_artifacts"][0].__setitem__("sha256", "0" * 64), resign(rs[0]))),
            ("receipt ID differs", lambda rs, it: (rs[0].__setitem__("receipt_id", "OTHER"), resign(rs[0]))),
            ("actual content bundle differs", lambda rs, it: it["coder_slots"][0].__setitem__("received_content_bundle_sha256", "0" * 64)),
            ("actual prompt differs", lambda rs, it: it["coder_slots"][0].__setitem__("received_prompt_sha256", "0" * 64)),
            ("lacks distribution_receipt_id", lambda rs, it: it["coder_slots"][0].__setitem__("distribution_receipt_id", "")),
        )
        for message, mutate in cases:
            with self.subTest(message=message):
                intake, receipts = self.runtime()
                mutate(receipts, intake)
                with self.assertRaisesRegex(agreement_v4.AgreementError, message):
                    self.compute(left, right, intake=intake, receipts=receipts)

    def test_response_binding_guards_fail_closed(self) -> None:
        mutations = (
            ("exact frozen N=56", lambda rows: rows.pop()),
            ("response coder_id", lambda rows: rows[0].__setitem__("coder_id", "OTHER")),
            ("coder transaction", lambda rows: rows[0].__setitem__("coder_transaction_id", "OTHER")),
            ("source manifest", lambda rows: rows[0].__setitem__("source_manifest_id", "OTHER")),
            ("packet item", lambda rows: rows[0].__setitem__("packet_item_id", "OTHER")),
            ("invalid completed response", lambda rows: rows[0].__setitem__("response_status", "BLANK_NOT_DISTRIBUTED")),
        )
        right = self.submitted_rows("CODER-B", "TX-B")
        for message, mutate in mutations:
            with self.subTest(message=message):
                left = self.submitted_rows("CODER-A", "TX-A")
                mutate(left)
                with self.assertRaisesRegex(agreement_v4.AgreementError, message):
                    self.compute(left, right)
        duplicate = self.submitted_rows("CODER-A", "TX-A")
        duplicate[1]["paper_id"] = duplicate[0]["paper_id"]
        with self.assertRaisesRegex(agreement_v4.AgreementError, "duplicate paper"):
            self.compute(duplicate, right)
        with self.assertRaisesRegex(agreement_v4.AgreementError, "minimum"):
            bound, receipts = self.runtime()
            agreement_v4.compute_agreement(
                self.submitted_rows("CODER-A", "TX-A"), right,
                runtime_intake=bound, frozen_contract=self.package["frozen_package_contract"],
                response_schema=self.package["response_schema"],
                source_manifest=self.package["source_manifest"],
                distribution_manifest=self.package["distribution_manifest"],
                delivery_receipt_schema=self.package["delivery_receipt_schema"],
                delivery_receipts=receipts, minimum=0,
            )

    def test_metric_nonempty_match_mismatch_and_malformed_objects(self) -> None:
        left_row = self.submitted_rows("CODER-A", "TX-A")[0]
        right_row = copy.deepcopy(left_row)
        for array_name in agreement_v4.OBJECT_ARRAYS:
            left_row[array_name] = []
            right_row[array_name] = []
        node = {
            "object_match_key": "dataset-node-key", "dataset_id": "DATA-1",
            "name": "Fixture", "revision": "v1", "split": "test",
            "source_locator_ids": [left_row["source_locators"][0]["locator_id"]],
        }
        left_row["dataset_nodes"] = [copy.deepcopy(node)]
        right_row["dataset_nodes"] = [copy.deepcopy(node)]
        result = agreement_v4._compute_metrics(
            {left_row["paper_id"]: left_row}, {right_row["paper_id"]: right_row},
            [left_row["paper_id"]], 0.85,
        )
        self.assertEqual("PASS", result["object_level"]["dataset_nodes"]["gate_status"])
        right_row["dataset_nodes"][0]["object_match_key"] = "different-key"
        result = agreement_v4._compute_metrics(
            {left_row["paper_id"]: left_row}, {right_row["paper_id"]: right_row},
            [left_row["paper_id"]], 0.85,
        )
        self.assertEqual("FAIL", result["object_level"]["dataset_nodes"]["gate_status"])
        left_row["dataset_nodes"].append(copy.deepcopy(left_row["dataset_nodes"][0]))
        with self.assertRaisesRegex(agreement_v4.AgreementError, "duplicate dataset_nodes"):
            agreement_v4._compute_metrics(
                {left_row["paper_id"]: left_row}, {right_row["paper_id"]: right_row},
                [left_row["paper_id"]], 0.85,
            )

    def test_builder_guards_and_deterministic_materialization(self) -> None:
        cases = (
            ("exact N=56", lambda p: p["calibration_manifest"].__setitem__("N", 55)),
            ("duplicate canonical", lambda p: p["calibration_manifest"]["canonical_ids"].__setitem__(1, p["calibration_manifest"]["canonical_ids"][0])),
            ("source bytes", lambda p: p["source_manifest"].__setitem__("N", 55)),
            ("leakage", lambda p: p["blind_packet"]["items"][0].__setitem__("auxiliary_metadata", {"title": "AudioToolAgent expected label"})),
            ("distributed coders", lambda p: p["distribution_manifest"].__setitem__("distribution_authorized", True)),
            ("bundle hash", lambda p: p["distribution_manifest"].__setitem__("content_bundle_sha256", "0" * 64)),
            ("distribution artifact", lambda p: p["distribution_manifest"]["artifacts"][0].__setitem__("sha256", "0" * 64)),
            ("prepared-not-distributed", lambda p: p["agreement_intake_contract"].__setitem__("status", "BOUND")),
            ("frozen package", lambda p: p["frozen_package_contract"].__setitem__("prompt_sha256", "0" * 64)),
            ("promoted a reproduction anchor", lambda p: p["reproduction_readiness"]["candidates"][0].__setitem__("method_anchor_eligible", True)),
            ("research execution", lambda p: p["reproduction_readiness"]["candidates"][0].__setitem__("research_execution_performed", True)),
        )
        with mock.patch.object(rc2r2, "verify_rc2r1_immutable"):
            for message, mutate in cases:
                with self.subTest(message=message):
                    package = rc2r2.build_package()
                    mutate(package)
                    with self.assertRaisesRegex(rc2r2.ContractError, message):
                        rc2r2.validate_package(package)
        self.assertEqual("AGENTIC_RC2R2_CODER_READY_NOT_DISTRIBUTED", rc2r2.run(write=False)["status"])

    def test_builder_helpers_reject_invalid_bindings_and_schema(self) -> None:
        names = rc2r2.CODER_DISTRIBUTION_ALLOWED_ARTIFACTS
        self.assertTrue(any("ALLOWLIST" in row for row in rc2r2.scan_coder_bundle_leaks(self.package, names[:-1])))
        missing = copy.deepcopy(self.package)
        missing.pop("coder_prompt")
        self.assertTrue(any("MISSING_ARTIFACT" in row for row in rc2r2.scan_coder_bundle_leaks(missing, names)))
        with self.assertRaisesRegex(rc2r2.ContractError, "exact A/B"):
            rc2r2.bind_runtime_intake(self.package, [], [])
        response = self.submitted_rows("CODER-A", "TX-A")[0]
        wrong_schema = copy.deepcopy(self.package["response_schema"])
        wrong_schema["$id"] = "wrong"
        with self.assertRaisesRegex(rc2r2.ContractError, "exact RC2R2"):
            rc2r2.validate_completed_response(response, wrong_schema, self.package["source_manifest"])
        absent = copy.deepcopy(response)
        absent["paper_id"] = "absent-paper"
        with self.assertRaisesRegex(rc2r2.ContractError, "absent from the frozen rendition"):
            rc2r2.validate_completed_response(absent, self.package["response_schema"], self.package["source_manifest"])


if __name__ == "__main__":
    unittest.main()
