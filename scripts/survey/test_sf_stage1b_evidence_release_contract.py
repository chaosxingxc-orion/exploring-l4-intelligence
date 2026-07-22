#!/usr/bin/env python3
"""Contracts for the bounded speech-evidence supplement and Stage-1B v3 release."""

from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

import sf_stage1b_evidence_release_contract as contract  # noqa: E402


def _row(
    paper_id: str,
    role: str,
    families: list[str],
) -> dict:
    direct = role == "DIRECT_CONTROL_METHOD"
    return {
        "evidence_id": f"DP-{paper_id}",
        "paper_work_id": paper_id,
        "method_path_id": f"{paper_id}#bounded-path",
        "title": f"Example {paper_id}",
        "analysis_role": role,
        "eligible_input_families": families,
        "bundle_load_bearing": True,
        "core_topology": "single_core_multi_call",
        "core_native_modality": "text_only",
        "includes_speech_audio": True,
        "speech_audio_role": "external_audio_tool" if direct else "evaluation_interface",
        "internal_visibility": "api_only",
        "core_weight_update": False,
        "external_component_weight_update": False,
        "controller_program_or_config_optimized_on_labels": False,
        "signals": [{"signal_id": "s1", "form": "verdict", "source": "task_state"}],
        "decision_rights": ["stop"] if direct else [],
        "control_edges": (
            [{"signal_id": "s1", "signal_use": "stop_budget", "decision_right": "stop"}]
            if direct
            else []
        ),
        "selection_object": "trajectory" if direct else "none",
        "terminal_operator": "accept_reject" if direct else "none",
        "stop_repair_semantics": "Stop when the bounded condition holds.",
        "load_bearing": direct,
        "fulltext_ref": {
            "ledger": "wiki/survey/2026-07-17-sf-fulltext-ledger.jsonl",
            "id": paper_id,
            "kind": "pdf",
            "sha256": "a" * 64,
        },
        "source_locator": "p3 anchor='bounded evidence locator'",
        "limitation": "Fixture limitation.",
    }


def _document() -> dict:
    return {
        "schema": contract.SUPPLEMENT_SCHEMA,
        "artifact_id": "SF-STAGE1B-SPEECH-DIRECT-PRIOR-SUPPLEMENT-V1",
        "scope": "BOUNDED_NON_H5_STAGE1C_INPUT_SUPPORT",
        "occupancy_rule": "ONLY_DIRECT_CONTROL_METHOD_ROWS_ENTER_METHOD_OCCUPANCY",
        "rows": [
            _row("2509.16971", "DIRECT_CONTROL_METHOD", ["budget_stop_repair"]),
            _row("2606.15141", "DIRECT_CONTROL_METHOD", ["budget_stop_repair"]),
            _row("2607.07985", "MEASUREMENT_INSTRUMENT", ["evaluator_reliability"]),
            _row("2603.13686", "MEASUREMENT_INSTRUMENT", ["interactive_full_duplex"]),
            _row("2510.07978", "MEASUREMENT_INSTRUMENT", ["interactive_full_duplex"]),
            _row("2605.13841", "MEASUREMENT_INSTRUMENT", ["evaluator_reliability", "interactive_full_duplex"]),
            _row("2607.16610", "BOUNDARY_COMPARATOR", ["interactive_full_duplex"]),
            _row("2603.02206", "DIRECT_CONTROL_METHOD", ["interactive_full_duplex"]),
            _row("2603.05413", "DIRECT_CONTROL_METHOD", ["interactive_full_duplex"]),
        ],
    }


def _coverage_document() -> dict:
    rows = []
    source_ids: dict[str, list[str]] = {
        "local-451-v4": [],
        "frozen-d0-root-gate-v1": [],
        "opening-d2-and-review-delta": [],
    }
    source_cycle = list(source_ids)
    for index, (paper_id, role) in enumerate(
        sorted(contract.REQUIRED_TYPICAL_PAPER_ROLES.items())
    ):
        source_id = source_cycle[index % len(source_cycle)]
        source_ids[source_id].append(paper_id)
        rows.append(
            {
                "paper_work_id": paper_id,
                "title": f"Typical speech/omni work {paper_id}",
                "analysis_role": role,
                "source_inventories": [source_id],
                "depth": "FULLTEXT_ROUTED",
                "supplement_status": (
                    "INCLUDED" if role in contract.SUPPLEMENT_MANDATORY_ROLES else "ROUTED_ONLY"
                ),
                "reason": (
                    "Explicit bounded exclusion or held-family reason."
                    if role in {"EXCLUDE_WITH_REASON", "H5_HELD"}
                    else "Explicit role assignment in the bounded speech/omni map."
                ),
            }
        )
    inventories = []
    for source_id, paper_ids in source_ids.items():
        inventories.append(
            {
                "inventory_id": source_id,
                "source_path": f"external/{source_id}.jsonl",
                "source_sha256": "b" * 64,
                "denominator": len(paper_ids),
                "coverage_claim": "Every named candidate is explicitly routed.",
                "named_candidate_ids": paper_ids,
            }
        )
    return {
        "schema": contract.COVERAGE_SCHEMA,
        "artifact_id": "SF-STAGE1B-SPEECH-OMNI-PRIOR-COVERAGE-V1",
        "scope": "BOUNDED_EXISTING_LOCAL_AND_FROZEN_D0_POOL",
        "source_inventories": inventories,
        "rows": rows,
    }


def _reference_appendix(document: dict) -> str:
    lines = [
        "# Stage-1B transition reference appendix",
        "",
        "| Evidence ID | Work | Authors / year | Stable link | Evidence route |",
        "|---|---|---|---|---|",
    ]
    for row in document["rows"]:
        paper_id = row["paper_work_id"]
        lines.append(
            f"| {row['evidence_id']} | {row['title']} | Example Author, 2026 | "
            f"[arXiv](https://arxiv.org/abs/{paper_id}) | `{row['source_locator']}` |"
        )
    return "\n".join(lines) + "\n"


def _release_spec() -> dict:
    artifacts = [
        ("strict_method_path_coding", "wiki/survey/current/data/known-item-coding-v7.json"),
        (
            "speech_prior_coverage",
            "wiki/survey/current/data/stage1b-speech-omni-prior-coverage-v1.json",
        ),
        (
            "speech_direct_prior_supplement",
            "wiki/survey/current/data/stage1b-speech-direct-prior-supplement-v1.json",
        ),
        (
            "transition_reference_appendix",
            "wiki/survey/current/stage1b-transition-reference-appendix.md",
        ),
        ("mapping_release", "wiki/survey/current/tables/stage1b-mapping-release.md"),
        ("eligible_inputs", "wiki/survey/current/tables/stage1c-eligible-inputs.md"),
    ]
    return {
        "release_id": "system-first-stage1b-2026-07-22-v3",
        "scientific_release_scope": "EXCLUDES_MUTABLE_HOT_AND_STATUS_ROUTERS",
        "artifacts": [
            {"role": role, "path": path, "location": "git", "producer": "fixture"}
            for role, path in artifacts
        ],
    }


class SpeechSupplementContractTests(unittest.TestCase):
    def test_valid_bounded_supplement_passes(self):
        self.assertEqual([], contract.validate_supplement(_document()))

    def test_missing_strict_comparable_field_fails(self):
        document = _document()
        del document["rows"][0]["internal_visibility"]
        self.assertIn(
            "SUPPLEMENT_REQUIRED_FIELD_MISSING:2509.16971:internal_visibility",
            contract.validate_supplement(document),
        )

    def test_instruments_and_boundaries_cannot_enter_method_occupancy(self):
        document = _document()
        document["rows"][2]["load_bearing"] = True
        self.assertIn(
            "SUPPLEMENT_NON_METHOD_LOAD_BEARING:2607.07985",
            contract.validate_supplement(document),
        )

    def test_each_non_h5_family_has_the_required_evidence_role(self):
        document = _document()
        document["rows"] = [
            row for row in document["rows"] if row["paper_work_id"] != "2607.07985"
        ]
        for row in document["rows"]:
            if row["analysis_role"] == "MEASUREMENT_INSTRUMENT":
                row["eligible_input_families"] = ["interactive_full_duplex"]
        self.assertIn(
            "SUPPLEMENT_FAMILY_ROLE_MISSING:evaluator_reliability:MEASUREMENT_INSTRUMENT",
            contract.validate_supplement(document),
        )

    def test_required_identity_cannot_silently_disappear(self):
        document = _document()
        document["rows"] = [
            row for row in document["rows"] if row["paper_work_id"] != "2509.16971"
        ]
        self.assertIn(
            "SUPPLEMENT_REQUIRED_ID_MISSING:2509.16971",
            contract.validate_supplement(document),
        )


class SpeechPriorCoverageContractTests(unittest.TestCase):
    def test_valid_bounded_candidate_universe_passes(self):
        self.assertEqual([], contract.validate_coverage(_coverage_document()))

    def test_typical_audio_system_cannot_silently_disappear(self):
        document = _coverage_document()
        document["rows"] = [
            row for row in document["rows"] if row["paper_work_id"] != "2510.02995"
        ]
        self.assertIn(
            "COVERAGE_REQUIRED_ID_MISSING:2510.02995",
            contract.validate_coverage(document),
        )

    def test_named_source_candidate_must_have_exactly_one_route(self):
        document = _coverage_document()
        source_id = document["source_inventories"][0]["named_candidate_ids"][0]
        document["rows"] = [
            row for row in document["rows"] if row["paper_work_id"] != source_id
        ]
        self.assertIn(
            f"COVERAGE_SOURCE_ID_UNROUTED:{source_id}",
            contract.validate_coverage(document),
        )

    def test_duplicate_identity_fails_even_when_roles_differ(self):
        document = _coverage_document()
        duplicate = copy.deepcopy(document["rows"][0])
        duplicate["analysis_role"] = "BOUNDARY_COMPARATOR"
        document["rows"].append(duplicate)
        self.assertIn(
            f"COVERAGE_DUPLICATE_PAPER_ID:{duplicate['paper_work_id']}",
            contract.validate_coverage(document),
        )

    def test_exclusion_and_h5_hold_require_a_reason(self):
        document = _coverage_document()
        row = next(
            row
            for row in document["rows"]
            if row["analysis_role"] in {"EXCLUDE_WITH_REASON", "H5_HELD"}
        )
        row["reason"] = ""
        self.assertIn(
            f"COVERAGE_REASON_MISSING:{row['paper_work_id']}",
            contract.validate_coverage(document),
        )

    def test_all_direct_rows_resolve_to_supplement(self):
        coverage = _coverage_document()
        supplement = {
            "rows": [
                {"paper_work_id": row["paper_work_id"]}
                for row in coverage["rows"]
                if row["analysis_role"] in contract.SUPPLEMENT_MANDATORY_ROLES
            ]
        }
        self.assertEqual(
            [], contract.validate_coverage_supplement_link(coverage, supplement)
        )
        missing_id = supplement["rows"].pop()["paper_work_id"]
        self.assertIn(
            f"COVERAGE_SUPPLEMENT_ROW_MISSING:{missing_id}",
            contract.validate_coverage_supplement_link(coverage, supplement),
        )

    def test_coverage_structural_failures_are_explicit(self):
        self.assertEqual(
            ["COVERAGE_DOCUMENT_NOT_OBJECT"], contract.validate_coverage([])
        )
        for mutation, expected in (
            (lambda d: d.__setitem__("schema", "wrong"), "COVERAGE_SCHEMA_INVALID"),
            (lambda d: d.__setitem__("scope", "wrong"), "COVERAGE_SCOPE_INVALID"),
            (lambda d: d.__setitem__("source_inventories", None), "COVERAGE_SOURCE_INVENTORIES_INVALID"),
            (lambda d: d.__setitem__("rows", None), "COVERAGE_ROWS_NOT_ARRAY"),
        ):
            document = _coverage_document()
            mutation(document)
            self.assertIn(expected, contract.validate_coverage(document))

    def test_coverage_source_and_row_metadata_fail_closed(self):
        source_mutations = (
            (lambda s: s.__setitem__("source_path", ""), "COVERAGE_SOURCE_PATH_MISSING"),
            (lambda s: s.__setitem__("source_sha256", "bad"), "COVERAGE_SOURCE_SHA_INVALID"),
            (lambda s: s.__setitem__("denominator", 0), "COVERAGE_SOURCE_DENOMINATOR_INVALID"),
            (lambda s: s.__setitem__("coverage_claim", "short"), "COVERAGE_SOURCE_CLAIM_MISSING"),
            (lambda s: s.__setitem__("named_candidate_ids", []), "COVERAGE_SOURCE_NAMED_IDS_INVALID"),
            (lambda s: s["named_candidate_ids"].append(s["named_candidate_ids"][0]), "COVERAGE_SOURCE_NAMED_IDS_DUPLICATE"),
        )
        for mutation, prefix in source_mutations:
            document = _coverage_document()
            source = document["source_inventories"][0]
            source_id = source["inventory_id"]
            mutation(source)
            self.assertTrue(
                any(failure.startswith(f"{prefix}:{source_id}") for failure in contract.validate_coverage(document)),
                prefix,
            )

        document = _coverage_document()
        document["source_inventories"].append(copy.deepcopy(document["source_inventories"][0]))
        self.assertTrue(any(f.startswith("COVERAGE_SOURCE_ID_DUPLICATE") for f in contract.validate_coverage(document)))
        document = _coverage_document()
        document["source_inventories"].append("bad")
        self.assertIn("COVERAGE_SOURCE_NOT_OBJECT:3", contract.validate_coverage(document))
        document = _coverage_document()
        document["rows"].append("bad")
        self.assertIn(f"COVERAGE_ROW_NOT_OBJECT:{len(document['rows']) - 1}", contract.validate_coverage(document))

        row_mutations = (
            (lambda r: r.pop("title"), "COVERAGE_REQUIRED_FIELD_MISSING"),
            (lambda r: r.__setitem__("analysis_role", "wrong"), "COVERAGE_ROLE_INVALID"),
            (lambda r: r.__setitem__("source_inventories", []), "COVERAGE_ROW_SOURCES_INVALID"),
            (lambda r: r.__setitem__("source_inventories", ["unknown"]), "COVERAGE_ROW_SOURCE_UNKNOWN"),
            (lambda r: r.__setitem__("supplement_status", "wrong"), "COVERAGE_SUPPLEMENT_STATUS_INVALID"),
        )
        for mutation, prefix in row_mutations:
            document = _coverage_document()
            row = document["rows"][0]
            mutation(row)
            self.assertTrue(any(f.startswith(prefix) for f in contract.validate_coverage(document)), prefix)

        document = _coverage_document()
        direct = next(row for row in document["rows"] if row["analysis_role"] == "DIRECT_CONTROL_METHOD")
        direct["supplement_status"] = "ROUTED_ONLY"
        self.assertTrue(any(f.startswith("COVERAGE_DIRECT_NOT_INCLUDED") for f in contract.validate_coverage(document)))
        document = _coverage_document()
        excluded = next(row for row in document["rows"] if row["analysis_role"] == "EXCLUDE_WITH_REASON")
        excluded["supplement_status"] = "INCLUDED"
        self.assertTrue(any(f.startswith("COVERAGE_EXCLUDED_ROW_INCLUDED") for f in contract.validate_coverage(document)))
        document = _coverage_document()
        extra = copy.deepcopy(document["rows"][0])
        extra["paper_work_id"] = "9999.99999"
        document["rows"].append(extra)
        self.assertIn("COVERAGE_ROW_NOT_IN_SOURCE_INVENTORY:9999.99999", contract.validate_coverage(document))

    def test_coverage_supplement_rejects_unknown_and_excluded_rows(self):
        coverage = _coverage_document()
        unknown = {"rows": [{"paper_work_id": "9999.99999"}]}
        self.assertIn(
            "SUPPLEMENT_COVERAGE_ROW_MISSING:9999.99999",
            contract.validate_coverage_supplement_link(coverage, unknown),
        )
        excluded = next(row for row in coverage["rows"] if row["analysis_role"] == "EXCLUDE_WITH_REASON")
        self.assertIn(
            f"SUPPLEMENT_COVERAGE_ROLE_FORBIDDEN:{excluded['paper_work_id']}",
            contract.validate_coverage_supplement_link(
                coverage, {"rows": [{"paper_work_id": excluded["paper_work_id"]}]}
            ),
        )


class ReferenceAndReleaseContractTests(unittest.TestCase):
    def test_reference_appendix_is_self_contained(self):
        document = _document()
        self.assertEqual(
            [], contract.validate_reference_appendix(_reference_appendix(document), document)
        )

    def test_reference_appendix_requires_author_year_and_stable_link(self):
        document = _document()
        text = _reference_appendix(document).replace(
            "Example Author, 2026", "unknown", 1
        )
        failures = contract.validate_reference_appendix(text, document)
        self.assertIn("REFERENCE_AUTHOR_YEAR_MISSING:DP-2509.16971", failures)

    def test_mapping_and_eligible_tokens_must_resolve(self):
        document = _document()
        texts = [
            "DP-2509.16971 DP-2606.15141 DP-2607.07985 DP-2603.13686 "
            "DP-2510.07978 DP-2605.13841 DP-2607.16610 DP-2603.02206 "
            "DP-2603.05413 DP-9999.99999"
        ]
        self.assertIn(
            "REFERENCE_TOKEN_UNRESOLVED:DP-9999.99999",
            contract.validate_reference_tokens(texts, document),
        )

    def test_every_supplement_row_is_used_in_active_synthesis(self):
        document = _document()
        texts = [
            " ".join(
                row["evidence_id"]
                for row in document["rows"]
                if row["paper_work_id"] != "2603.05413"
            )
        ]
        self.assertIn(
            "REFERENCE_TOKEN_UNUSED:DP-2603.05413",
            contract.validate_reference_tokens(texts, document),
        )

    def test_release_spec_binds_scientific_evidence_and_excludes_hot_routers(self):
        self.assertEqual([], contract.validate_release_spec(_release_spec()))

        mutated = _release_spec()
        mutated["artifacts"].append(
            {
                "role": "hot_state",
                "path": "wiki/Research-Objective.md",
                "location": "git",
                "producer": "fixture",
            }
        )
        self.assertIn(
            "RELEASE_MUTABLE_ROUTER_INCLUDED:hot_state",
            contract.validate_release_spec(mutated),
        )

    def test_release_spec_requires_supplement_and_reference_roles(self):
        spec = _release_spec()
        spec["artifacts"] = [
            row for row in spec["artifacts"]
            if row["role"] != "transition_reference_appendix"
        ]
        self.assertIn(
            "RELEASE_REQUIRED_ROLE_MISSING:transition_reference_appendix",
            contract.validate_release_spec(spec),
        )

    def test_supplement_structural_and_semantic_failures_are_explicit(self):
        self.assertEqual(["SUPPLEMENT_DOCUMENT_NOT_OBJECT"], contract.validate_supplement([]))
        top_mutations = (
            ("schema", "wrong", "SUPPLEMENT_SCHEMA_INVALID"),
            ("scope", "wrong", "SUPPLEMENT_SCOPE_INVALID"),
            ("occupancy_rule", "wrong", "SUPPLEMENT_OCCUPANCY_RULE_INVALID"),
            ("rows", None, "SUPPLEMENT_ROWS_NOT_ARRAY"),
        )
        for key, value, expected in top_mutations:
            document = _document()
            document[key] = value
            self.assertIn(expected, contract.validate_supplement(document))
        document = _document()
        document["rows"].append("bad")
        self.assertIn(f"SUPPLEMENT_ROW_NOT_OBJECT:{len(document['rows']) - 1}", contract.validate_supplement(document))
        document = _document()
        document["rows"].append(copy.deepcopy(document["rows"][0]))
        self.assertIn("SUPPLEMENT_DUPLICATE_PAPER_ID:2509.16971", contract.validate_supplement(document))

        cases = (
            (lambda r: r.__setitem__("evidence_id", "wrong"), "SUPPLEMENT_EVIDENCE_ID_INVALID"),
            (lambda r: r.__setitem__("analysis_role", "wrong"), "SUPPLEMENT_ROLE_INVALID"),
            (lambda r: r.__setitem__("eligible_input_families", []), "SUPPLEMENT_FAMILIES_INVALID"),
            (lambda r: r.__setitem__("eligible_input_families", ["wrong"]), "SUPPLEMENT_FAMILY_INVALID"),
            (lambda r: r.__setitem__("bundle_load_bearing", False), "SUPPLEMENT_BUNDLE_NOT_LOAD_BEARING"),
            (lambda r: r.__setitem__("includes_speech_audio", False), "SUPPLEMENT_NOT_SPEECH_AUDIO_RELEVANT"),
            (lambda r: r.__setitem__("load_bearing", False), "SUPPLEMENT_DIRECT_METHOD_NOT_LOAD_BEARING"),
            (lambda r: r.__setitem__("decision_rights", []), "SUPPLEMENT_DIRECT_METHOD_EDGE_MISSING"),
            (lambda r: r.__setitem__("fulltext_ref", None), "SUPPLEMENT_FULLTEXT_REF_INVALID"),
            (lambda r: r["fulltext_ref"].__setitem__("id", "wrong"), "SUPPLEMENT_FULLTEXT_ID_MISMATCH"),
            (lambda r: r["fulltext_ref"].__setitem__("sha256", "bad"), "SUPPLEMENT_FULLTEXT_SHA_INVALID"),
            (lambda r: r["fulltext_ref"].__setitem__("ledger", ""), "SUPPLEMENT_FULLTEXT_LEDGER_MISSING"),
            (lambda r: r.__setitem__("source_locator", "bad"), "SUPPLEMENT_SOURCE_LOCATOR_INVALID"),
        )
        for mutation, prefix in cases:
            document = _document()
            mutation(document["rows"][0])
            self.assertTrue(any(f.startswith(prefix) for f in contract.validate_supplement(document)), prefix)

    def test_reference_and_release_negative_paths(self):
        document = _document()
        text = _reference_appendix(document)
        first = document["rows"][0]
        without_row = "\n".join(line for line in text.splitlines() if first["evidence_id"] not in line)
        self.assertIn(f"REFERENCE_ROW_COUNT:{first['evidence_id']}:0", contract.validate_reference_appendix(without_row, document))
        without_link = text.replace(f"https://arxiv.org/abs/{first['paper_work_id']}", "https://example.invalid", 1)
        self.assertIn(f"REFERENCE_STABLE_LINK_MISSING:{first['evidence_id']}", contract.validate_reference_appendix(without_link, document))
        without_locator = text.replace(first["source_locator"], "p1 anchor='different bounded locator'", 1)
        self.assertIn(f"REFERENCE_LOCATOR_MISSING:{first['evidence_id']}", contract.validate_reference_appendix(without_locator, document))

        self.assertEqual(["RELEASE_SPEC_NOT_OBJECT"], contract.validate_release_spec([]))
        for key, value, expected in (
            ("release_id", "wrong", "RELEASE_ID_INVALID"),
            ("scientific_release_scope", "wrong", "RELEASE_SCIENTIFIC_SCOPE_INVALID"),
            ("artifacts", None, "RELEASE_ARTIFACTS_NOT_ARRAY"),
        ):
            spec = _release_spec()
            spec[key] = value
            self.assertIn(expected, contract.validate_release_spec(spec))
        spec = _release_spec()
        spec["artifacts"].append(copy.deepcopy(spec["artifacts"][0]))
        self.assertIn("RELEASE_DUPLICATE_ROLE", contract.validate_release_spec(spec))
        spec = _release_spec()
        spec["artifacts"].append("bad")
        self.assertTrue(any(f.startswith("RELEASE_ARTIFACT_ROLE_INVALID") for f in contract.validate_release_spec(spec)))

    def test_repository_missing_and_invalid_json_fail_closed(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            failures = contract.validate_repository(Path(temp_dir))
            self.assertTrue(any(f.startswith("REPOSITORY_ARTIFACT_MISSING") for f in failures))
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)
            for relative in (
                contract.COVERAGE_PATH,
                contract.SUPPLEMENT_PATH,
                contract.REFERENCE_PATH,
                contract.MAPPING_PATH,
                contract.ELIGIBLE_PATH,
                contract.RELEASE_SPEC_PATH,
            ):
                path = repo / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("not-json" if path.suffix == ".json" else "text", encoding="utf-8")
            self.assertTrue(contract.validate_repository(repo)[0].startswith("REPOSITORY_JSON_INVALID"))


class RepositoryIntegrationTests(unittest.TestCase):
    def test_repository_v3_evidence_contract(self):
        self.assertEqual([], contract.validate_repository(REPO))


if __name__ == "__main__":
    unittest.main()
