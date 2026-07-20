#!/usr/bin/env python3
"""Anchor-policy contract tests for survey PDF page locators."""
import os
import sys
import unittest
from copy import deepcopy


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sf_evidence_contract import (  # noqa: E402
    ABSENCE_ALLOWED_VALUES,
    ABSENCE_PROOF_OBLIGATIONS,
    ROW_REQUIRED_FIELDS,
    check_page_locator,
    normalized_tokens,
    validate_absence_cross_bindings,
    validate_bound_values,
    values_equal,
)
from sf_row_hash import row_hash  # noqa: E402


def binding(value):
    return {"kind": "canon", "value": value, "quote": "claim-bearing quote"}


def generic_row():
    row = {
        "method_path_id": "__fx12__#path",
        "core_weight_update": False,
        "external_component_weight_update": False,
        "controller_program_or_config_optimized_on_labels": False,
        "human_or_dev_label_model_selection": False,
        "deployment_label_access": False,
        "test_item_gold_access": False,
        "inference_external_new_information": False,
        "internal_visibility": "api_only",
        "core_topology": "single_core",
        "core_native_modality": "omni_native",
        "control_horizon": "sequential",
        "decision_rights": ["branch"],
        "candidate_pool_exists": True,
        "selection_policy": "scored_select",
        "selection_object": "candidate_output",
        "explicit_candidate_pool_selection": True,
    }
    row["claim_evidence"] = {
        field: binding(row[field]) for field in ROW_REQUIRED_FIELDS
    }
    signal = {
        "signal_id": "s1",
        "form": "scalar_score",
        "source": "llm_judge",
        "lifecycle": "online_step",
        "uses": ["prune"],
        "claim_evidence": {},
    }
    signal["claim_evidence"] = {
        field: binding(signal[field])
        for field in ("form", "source", "lifecycle", "uses")
    }
    edge = {
        "signal_id": "s1",
        "signal_use": "prune",
        "decision_right": "branch",
        "claim_evidence": {},
    }
    edge["claim_evidence"] = {
        field: binding(edge[field]) for field in ("signal_use", "decision_right")
    }
    row["signals"] = [signal]
    row["control_edges"] = [edge]
    return row


def absence_context():
    """Return one internally consistent negative-evidence fixture."""
    row = generic_row()
    pid = row["method_path_id"]
    field = "selection_object"
    sidecar_path = "wiki/survey/current/data/schema-v3/sidecars/__fx12__.sidecar.json"
    fulltext = {
        "id": "__fx12__",
        "kind": "pdf",
        "sha256": "a" * 64,
    }
    evidence = {
        "kind": "absence",
        "value": "none",
        "reason": (
            "The method defines no candidate-output comparison or selector after "
            "inspection of the method and inference procedure."
        ),
        "proof_obligation_id": ABSENCE_PROOF_OBLIGATIONS[field][
            "proof_obligation_id"
        ],
        "inspected_locators": [
            "section: Method / Inference procedure",
            "p7 anchor='single response is returned directly'",
        ],
        "owner_method_path_id": pid,
        "owner_sidecar": sidecar_path,
        "fulltext": deepcopy(fulltext),
        "coder_identity": "coder:fixture",
        "owner_row_sha256": "pending",
        "adjudication_row_id": "ABS-__fx12__-selection-object",
    }
    row["selection_object"] = "none"
    row["claim_evidence"][field] = evidence
    row["coder"] = "coder:fixture"
    evidence["owner_row_sha256"] = row_hash(row)
    sidecar = {
        "paper_work_id": "__fx12__",
        "coder": "coder:fixture",
        "fulltext": deepcopy(fulltext),
        "method_paths": [deepcopy(row)],
    }
    adjudication_row = {
        "adjudication_row_id": evidence["adjudication_row_id"],
        "method_path_id": pid,
        "owner_kind": "row",
        "field": field,
        "proof_obligation_id": evidence["proof_obligation_id"],
        "owner_sidecar": sidecar_path,
        "fulltext": deepcopy(fulltext),
        "coder_identity": "coder:fixture",
        "owner_row_sha256": evidence["owner_row_sha256"],
        "adjudicator_identity": "reviewer:fixture",
        "verdict": "AGREE",
        "independence": {
            "classification": "TEAM_ATTESTATION",
            "nonparticipation_scope": "Did not code or migrate this row.",
            "conflict_declaration": "No conflict declared.",
            "timestamp": "2026-07-20T12:00:00+08:00",
        },
    }
    adjudication = {
        "artifact_id": "ABSENCE-ADJUDICATION-FIXTURE",
        "rows": [adjudication_row],
    }
    return row, sidecar_path, sidecar, adjudication


class FakePage:
    def __init__(self, text):
        self.text = text

    def extract_text(self):
        return self.text


class FakeReader:
    def __init__(self, page_texts):
        self.pages = [FakePage(text) for text in page_texts]


class RaisingPage:
    def extract_text(self):
        raise RuntimeError("unreadable PDF page")


class CountingPage(FakePage):
    def __init__(self, text):
        super().__init__(text)
        self.calls = 0

    def extract_text(self):
        self.calls += 1
        return super().extract_text()


class AnchorPolicyTest(unittest.TestCase):
    def setUp(self):
        self.reader = FakeReader(
            [
                "the method introduction",
                "the orchestrator decides every explore and stop action in context",
                "the appendix repeats common words but not the claim-bearing phrase",
            ]
        )

    def failures(self, locator):
        out = []
        check_page_locator(locator, self.reader, "fx#row", "row-locator", out)
        return out

    def test_page_token_without_anchor_fails(self):
        failures = self.failures("p1")
        self.assertTrue(any("page-token-without-anchor" in failure for failure in failures))

    def test_weak_anchor_fails(self):
        failures = self.failures("p1 anchor='the'")
        self.assertTrue(any("page-anchor-too-weak" in failure for failure in failures))

    def test_non_discriminative_anchor_fails(self):
        reader = FakeReader(["common method description"] * 4)
        out = []
        check_page_locator(
            "p2 anchor='common method description'",
            reader,
            "fx#row",
            "row-locator",
            out,
        )
        self.assertTrue(
            any("page-anchor-not-discriminative" in failure for failure in out)
        )

    def test_claim_bearing_anchor_passes(self):
        self.assertEqual(
            self.failures("p2 anchor='decides every explore and stop action'"), []
        )

    def test_missing_anchor_fails(self):
        failures = self.failures("p2 anchor='candidate majority controls termination'")
        self.assertTrue(any("page-anchor-missing" in failure for failure in failures))

    def test_row_required_fields_are_ordered_contract_list(self):
        self.assertEqual(
            ROW_REQUIRED_FIELDS,
            [
                "core_weight_update",
                "external_component_weight_update",
                "controller_program_or_config_optimized_on_labels",
                "human_or_dev_label_model_selection",
                "deployment_label_access",
                "test_item_gold_access",
                "inference_external_new_information",
                "internal_visibility",
                "core_topology",
                "core_native_modality",
                "control_horizon",
                "decision_rights",
                "candidate_pool_exists",
                "selection_policy",
                "selection_object",
                "explicit_candidate_pool_selection",
            ],
        )

    def test_normalized_tokens_accepts_none(self):
        self.assertEqual(normalized_tokens(None), [])

    def test_none_locator_is_empty(self):
        self.assertEqual(self.failures(None), [])

    def test_leading_zero_page_errors_use_canonical_page_number(self):
        self.assertEqual(
            self.failures("p01"),
            ["fx#row:row-locator:page-token-without-anchor:p1"],
        )
        self.assertEqual(
            self.failures("p01 anchor='the'"),
            ["fx#row:row-locator:page-anchor-too-weak:p1:the"],
        )

    def test_anchor_cannot_match_across_page_boundary(self):
        reader = FakeReader(["distinctive orchestrator", "controls"])
        out = []
        check_page_locator(
            "p1 anchor='distinctive orchestrator controls'",
            reader,
            "fx#row",
            "row-locator",
            out,
        )
        self.assertEqual(
            out,
            [
                "fx#row:row-locator:page-anchor-missing:"
                "p1:distinctive orchestrator controls"
            ],
        )

    def test_anchor_requires_exact_token_sequence_at_suffix_and_prefix(self):
        for page_text in (
            "candidate majority controls terminations",
            "uncandidate majority controls termination",
        ):
            reader = FakeReader([page_text])
            out = []
            check_page_locator(
                "p1 anchor='candidate majority controls termination'",
                reader,
                "fx#row",
                "row-locator",
                out,
            )
            self.assertEqual(
                out,
                [
                    "fx#row:row-locator:page-anchor-missing:"
                    "p1:candidate majority controls termination"
                ],
            )

    def test_page_tokens_inside_strong_anchor_are_not_extra_locators(self):
        reader = FakeReader(["method compares p2 outcome"])
        out = []
        check_page_locator(
            "p1 anchor='method compares p2 outcome'",
            reader,
            "fx#row",
            "row-locator",
            out,
        )
        self.assertEqual(out, [])

    def test_extraction_error_fails_closed(self):
        reader = FakeReader([])
        reader.pages = [FakePage("decides every explore and stop action"), RaisingPage()]
        out = []
        check_page_locator(
            "p1 anchor='decides every explore and stop action'",
            reader,
            "fx#row",
            "row-locator",
            out,
        )
        self.assertEqual(out, ["fx#row:row-locator:pdf-unreadable-for-page-check"])

    def test_document_is_extracted_once_for_multiple_strong_locators(self):
        pages = [
            CountingPage("decides every explore and stop action"),
            CountingPage("candidate majority controls termination"),
        ]
        reader = FakeReader([])
        reader.pages = pages
        out = []
        check_page_locator(
            "p1 anchor='decides every explore and stop action'; "
            "p2 anchor='candidate majority controls termination'",
            reader,
            "fx#row",
            "row-locator",
            out,
        )
        self.assertEqual(out, [])
        self.assertEqual([page.calls for page in pages], [1, 1])


class BoundValueTest(unittest.TestCase):
    def failures(self, row):
        return validate_bound_values(row)

    def test_complete_generic_row_passes(self):
        self.assertEqual(self.failures(generic_row()), [])

    def test_signal_source_must_match_its_evidence_value(self):
        row = deepcopy(generic_row())
        row["signals"][0]["source"] = "learned_rm_prm"
        failures = self.failures(row)
        self.assertTrue(
            any(
                "signal:s1:source:evidence-value-mismatch" in failure
                for failure in failures
            )
        )

    def test_edge_signal_use_must_match_its_evidence_value(self):
        row = deepcopy(generic_row())
        row["signals"][0]["uses"] = ["select"]
        row["signals"][0]["claim_evidence"]["uses"]["value"] = ["select"]
        row["control_edges"][0]["signal_use"] = "select"
        failures = self.failures(row)
        self.assertTrue(
            any(
                "edge:0:signal_use:evidence-value-mismatch" in failure
                for failure in failures
            )
        )

    def test_edge_decision_right_must_match_its_evidence_value(self):
        row = deepcopy(generic_row())
        row["control_edges"][0]["decision_right"] = "supply"
        failures = self.failures(row)
        self.assertTrue(
            any(
                "edge:0:decision_right:evidence-value-mismatch" in failure
                for failure in failures
            )
        )

    def test_selection_object_must_match_its_evidence_value(self):
        row = deepcopy(generic_row())
        row["selection_object"] = "trajectory"
        failures = self.failures(row)
        self.assertTrue(
            any(
                "row:selection_object:evidence-value-mismatch" in failure
                for failure in failures
            )
        )

    def test_explicit_pool_selection_must_match_its_evidence_value(self):
        row = deepcopy(generic_row())
        row["explicit_candidate_pool_selection"] = False
        failures = self.failures(row)
        self.assertTrue(
            any(
                "row:explicit_candidate_pool_selection:evidence-value-mismatch"
                in failure
                for failure in failures
            )
        )

    def test_edge_decision_right_requires_evidence(self):
        row = deepcopy(generic_row())
        del row["control_edges"][0]["claim_evidence"]["decision_right"]
        failures = self.failures(row)
        self.assertTrue(
            any(
                "edge:0:decision_right:required-evidence-missing" in failure
                for failure in failures
            )
        )

    def test_boolean_evidence_integer_value_is_a_mismatch(self):
        row = deepcopy(generic_row())
        row["claim_evidence"]["core_weight_update"]["value"] = 1
        self.assertIn(
            "__fx12__#path:row:core_weight_update:evidence-value-mismatch",
            self.failures(row),
        )

    def test_values_equal_requires_identical_concrete_types(self):
        self.assertFalse(values_equal(True, 1))
        self.assertFalse(values_equal(1, True))

    def test_values_equal_rejects_boolean_integer_list_elements(self):
        self.assertFalse(values_equal([True], [1]))
        self.assertFalse(values_equal([1], [True]))

    def test_signal_uses_boolean_integer_list_elements_mismatch(self):
        row = deepcopy(generic_row())
        row["signals"][0]["uses"] = [True]
        row["signals"][0]["claim_evidence"]["uses"]["value"] = [1]
        self.assertIn(
            "__fx12__#path:signal:s1:uses:evidence-value-mismatch",
            self.failures(row),
        )

    def test_absent_row_field_with_null_evidence_is_encoded_field_missing(self):
        row = deepcopy(generic_row())
        del row["selection_object"]
        row["claim_evidence"]["selection_object"]["value"] = None
        self.assertIn(
            "__fx12__#path:row:selection_object:encoded-field-missing",
            self.failures(row),
        )

    def test_list_claim_evidence_is_invalid_container(self):
        row = deepcopy(generic_row())
        row["claim_evidence"] = []
        self.assertIn(
            "__fx12__#path:row:core_weight_update:evidence-container-invalid",
            self.failures(row),
        )

    def test_string_evidence_entry_is_invalid(self):
        row = deepcopy(generic_row())
        row["claim_evidence"]["selection_object"] = "not a mapping"
        self.assertIn(
            "__fx12__#path:row:selection_object:evidence-entry-invalid",
            self.failures(row),
        )

    def test_none_signals_is_invalid_container(self):
        row = deepcopy(generic_row())
        row["signals"] = None
        self.assertIn(
            "__fx12__#path:signals:container-invalid", self.failures(row)
        )

    def test_invalid_evidence_kind_fails(self):
        row = deepcopy(generic_row())
        row["claim_evidence"]["selection_object"]["kind"] = "unsupported"
        self.assertIn(
            "__fx12__#path:row:selection_object:evidence-kind-invalid",
            self.failures(row),
        )

    def test_unhashable_list_items_mismatch_without_exception(self):
        row = deepcopy(generic_row())
        row["decision_rights"] = [{"branch": True}]
        row["claim_evidence"]["decision_rights"]["value"] = [{"branch": True}]
        self.assertIn(
            "__fx12__#path:row:decision_rights:evidence-value-mismatch",
            self.failures(row),
        )

    def test_non_mapping_row_is_invalid_container(self):
        self.assertEqual(self.failures([]), ["?:row:container-invalid"])

    def test_non_mapping_signal_and_edge_entries_are_invalid(self):
        row = deepcopy(generic_row())
        row["signals"] = [None]
        row["control_edges"] = [None]
        self.assertEqual(
            self.failures(row),
            [
                "__fx12__#path:signal:0:entry-invalid",
                "__fx12__#path:edge:0:entry-invalid",
            ],
        )


class AbsenceEvidenceContractTest(unittest.TestCase):
    def failures(self, row):
        return validate_bound_values(row)

    def test_allowed_pairs_are_exact_and_field_specific(self):
        self.assertEqual(
            ABSENCE_ALLOWED_VALUES,
            {
                "human_or_dev_label_model_selection": (False,),
                "selection_object": ("none",),
                "explicit_candidate_pool_selection": (False,),
                "inference_external_new_information": (False,),
                "external_component_weight_update": (False,),
                "controller_program_or_config_optimized_on_labels": (False,),
                "decision_rights": ([],),
            },
        )

    def test_each_allowed_field_has_a_complete_proof_obligation(self):
        self.assertEqual(set(ABSENCE_ALLOWED_VALUES), set(ABSENCE_PROOF_OBLIGATIONS))
        required = {
            "proof_obligation_id",
            "required_inspection_targets",
            "search_terms_or_tables",
            "acceptable_explicit_negative_evidence",
            "force_unresolved_if",
        }
        for field, obligation in ABSENCE_PROOF_OBLIGATIONS.items():
            with self.subTest(field=field):
                self.assertEqual(required, set(obligation))
                self.assertTrue(all(obligation[key] for key in required))

    def test_complete_allowed_absence_passes_local_contract(self):
        row, _, _, _ = absence_context()
        self.assertEqual(self.failures(row), [])

    def test_positive_categorical_absence_fails(self):
        row, _, _, _ = absence_context()
        entry = deepcopy(row["claim_evidence"]["selection_object"])
        entry["value"] = "api_only"
        entry["proof_obligation_id"] = "NEG-INTERNAL-VISIBILITY"
        row["internal_visibility"] = "api_only"
        row["claim_evidence"]["internal_visibility"] = entry
        self.assertIn(
            "__fx12__#path:row:internal_visibility:absence-field-value-not-allowed",
            self.failures(row),
        )

    def test_unknown_none_and_empty_absence_values_fail(self):
        for value in ("unknown", None, ""):
            with self.subTest(value=value):
                row, _, _, _ = absence_context()
                row["selection_object"] = value
                row["claim_evidence"]["selection_object"]["value"] = value
                self.assertIn(
                    "__fx12__#path:row:selection_object:"
                    "absence-field-value-not-allowed",
                    self.failures(row),
                )

    def test_url_or_locator_cannot_substitute_for_fulltext_hash(self):
        for invalid in (
            "https://arxiv.org/pdf/1234.56789",
            "p7 anchor='candidate selection'",
        ):
            with self.subTest(invalid=invalid):
                row, _, _, _ = absence_context()
                row["claim_evidence"]["selection_object"]["fulltext"][
                    "sha256"
                ] = invalid
                self.assertIn(
                    "__fx12__#path:row:selection_object:"
                    "absence-fulltext-sha256-invalid",
                    self.failures(row),
                )

    def test_weak_not_contradicted_reason_fails(self):
        row, _, _, _ = absence_context()
        row["claim_evidence"]["selection_object"]["reason"] = "not contradicted"
        self.assertIn(
            "__fx12__#path:row:selection_object:absence-reason-weak",
            self.failures(row),
        )

    def test_empty_inspected_locators_fail(self):
        row, _, _, _ = absence_context()
        row["claim_evidence"]["selection_object"]["inspected_locators"] = []
        self.assertIn(
            "__fx12__#path:row:selection_object:absence-locators-invalid",
            self.failures(row),
        )

    def test_wrong_proof_obligation_for_field_fails(self):
        row, _, _, _ = absence_context()
        row["claim_evidence"]["selection_object"]["proof_obligation_id"] = (
            "NEG-HUMAN-MODEL-SELECTION"
        )
        self.assertIn(
            "__fx12__#path:row:selection_object:"
            "absence-proof-obligation-mismatch",
            self.failures(row),
        )


class AbsenceCrossBindingTest(unittest.TestCase):
    def failures(self, row, sidecar_path, sidecar, adjudication):
        return validate_absence_cross_bindings(
            row, sidecar_path, sidecar, adjudication
        )

    def test_complete_cross_binding_passes(self):
        args = absence_context()
        self.assertEqual(self.failures(*args), [])

    def test_wrong_fulltext_hash_fails(self):
        row, sidecar_path, sidecar, adjudication = absence_context()
        row["claim_evidence"]["selection_object"]["fulltext"]["sha256"] = "b" * 64
        self.assertIn(
            "__fx12__#path:row:selection_object:absence-fulltext-binding-mismatch",
            self.failures(row, sidecar_path, sidecar, adjudication),
        )

    def test_wrong_sidecar_fails(self):
        row, sidecar_path, sidecar, adjudication = absence_context()
        row["claim_evidence"]["selection_object"]["owner_sidecar"] = (
            "wiki/survey/current/data/schema-v3/sidecars/wrong.sidecar.json"
        )
        self.assertIn(
            "__fx12__#path:row:selection_object:absence-owner-sidecar-mismatch",
            self.failures(row, sidecar_path, sidecar, adjudication),
        )

    def test_wrong_row_hash_fails(self):
        row, sidecar_path, sidecar, adjudication = absence_context()
        row["claim_evidence"]["selection_object"]["owner_row_sha256"] = "0" * 64
        self.assertIn(
            "__fx12__#path:row:selection_object:absence-owner-row-hash-mismatch",
            self.failures(row, sidecar_path, sidecar, adjudication),
        )

    def test_adjudication_artifact_missing_row_fails(self):
        row, sidecar_path, sidecar, adjudication = absence_context()
        adjudication["rows"] = []
        self.assertIn(
            "__fx12__#path:row:selection_object:absence-adjudication-row-missing",
            self.failures(row, sidecar_path, sidecar, adjudication),
        )

    def test_verdict_other_than_agree_fails(self):
        row, sidecar_path, sidecar, adjudication = absence_context()
        adjudication["rows"][0]["verdict"] = "DISAGREE"
        self.assertIn(
            "__fx12__#path:row:selection_object:absence-verdict-not-agree",
            self.failures(row, sidecar_path, sidecar, adjudication),
        )

    def test_coder_and_adjudicator_collision_fails(self):
        row, sidecar_path, sidecar, adjudication = absence_context()
        adjudication["rows"][0]["adjudicator_identity"] = "coder:fixture"
        self.assertIn(
            "__fx12__#path:row:selection_object:absence-actor-collision",
            self.failures(row, sidecar_path, sidecar, adjudication),
        )

    def test_independence_is_team_attestation_not_machine_proof(self):
        row, sidecar_path, sidecar, adjudication = absence_context()
        adjudication["rows"][0]["independence"]["classification"] = (
            "MACHINE_PROVED"
        )
        self.assertIn(
            "__fx12__#path:row:selection_object:"
            "absence-independence-attestation-invalid",
            self.failures(row, sidecar_path, sidecar, adjudication),
        )


if __name__ == "__main__":
    unittest.main()
