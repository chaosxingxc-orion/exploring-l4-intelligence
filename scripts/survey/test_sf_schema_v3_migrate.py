#!/usr/bin/env python3
"""Focused tests for the deterministic schema-v3 sidecar migration."""

from __future__ import annotations

import copy
import hashlib
import io
import json
import logging
import os
import sys
import tarfile
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock


logging.getLogger("pypdf").setLevel(logging.ERROR)


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sf_evidence_contract import (  # noqa: E402
    EDGE_REQUIRED_FIELDS,
    ROW_REQUIRED_FIELDS,
    SIGNAL_REQUIRED_FIELDS,
    check_page_locator,
    validate_bound_values,
)
import sf_schema_v3_migrate as migration  # noqa: E402
from sf_schema_v3_migrate import (  # noqa: E402
    ABSENCE_SELECTION_NOTE,
    ANCHOR_REPLACEMENTS,
    MigrationError,
    OUTPUT_DIR,
    SCHEMA_TEXT,
    SCHEMA_V3_BINDING_STATUS,
    SOURCE_DIR,
    SUCCESS_LINE,
    build_outputs,
    main,
    migrate_sidecar,
    replace_anchors,
    write_outputs,
)


ROW14_FIELDS = ROW_REQUIRED_FIELDS[:-2]

ADJUDICATION_REPAIR_BINDINGS = {
    (
        "2026.findings-acl.511#prm-guided-search",
        "row",
        "selection_object",
    ): {
        "value": "trajectory",
        "kind": "pdf_page",
        "page": 15,
        "anchor": "return path with highest reward",
    },
    (
        "2602.16485#calibrated-orchestration",
        "signal:s_profile",
        "source",
    ): {
        "value": "llm_judge",
        "kind": "pdf_page",
        "page": 7,
        "anchor": "each tool agent performs a self audit",
    },
    (
        "2602.16485#calibrated-orchestration",
        "edge:1",
        "signal_use",
    ): {
        "value": "route",
        "kind": "pdf_page",
        "page": 5,
        "anchor": "agents profiles to select only the most compatible tools",
    },
    ("2604.16529#rtv", "row", "selection_object"): {
        "value": "trajectory",
        "kind": "tex",
        "quote": (
            "where each round reduces a population of rollouts into a subset by "
            "dividing the population into groups of size $G$ and selecting a rollout "
            "from each group."
        ),
    },
    (
        "2604.16529#rtv-pdr-pipeline",
        "row",
        "explicit_candidate_pool_selection",
    ): {
        "value": True,
        "kind": "tex",
        "quote": (
            "apply \\textbf{RTV} to obtain a high-quality subset of $K$ summaries;"
        ),
    },
    ("2604.16529#rtv-pdr-pipeline", "row", "selection_object"): {
        "value": "trajectory",
        "kind": "tex",
        "quote": (
            "apply \\textbf{RTV} to the refined rollouts and return the final "
            "top-$1$ rollout."
        ),
    },
    ("2604.16529#rtv-pdr-pipeline", "edge:1", "decision_right"): {
        "value": "supply",
        "kind": "tex",
        "quote": (
            "\\textbf{RTV} is then applied to these summaries to select the top-$K$ "
            "summaries, which define the refinement context for the next iteration."
        ),
    },
    ("2605.08083#discovered-controller", "row", "selection_object"): {
        "value": "trajectory",
        "kind": "canon",
        "quote": (
            "每(model,problem)预采 128 轨迹;selector=controller 终态共识型 Agg"
        ),
    },
    ("2606.01667#agentic-orchestration", "row", "selection_object"): {
        "value": "candidate_output",
        "kind": "pdf_page",
        "page": 3,
        "anchor": "returned candidate ct answer reasoning approach confidence",
    },
    ("2606.01667#agentic-orchestration", "edge:2", "signal_use"): {
        "value": "synthesize_input",
        "kind": "pdf_page",
        "page": 2,
        "anchor": (
            "stop and synthesis decisions both rest on this single stateful in "
            "context view"
        ),
    },
    ("2606.03054#trained-gate", "signal:s_gate", "source"): {
        "value": "trained_classifier",
        "kind": "pdf_page",
        "page": 11,
        "anchor": "logistic regression classifier we train with l2",
    },
}


def pinned_data_root():
    candidates = []
    configured = os.environ.get("SPEECHRL_DATA_DIR")
    if configured:
        candidates.append(Path(configured))
    candidates.extend(
        [
            Path("E:/chao_workspace/exploring-l4-intelligence/speechrl-data"),
            Path("/mnt/e/chao_workspace/exploring-l4-intelligence/speechrl-data"),
        ]
    )
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    raise AssertionError("pinned speechrl-data root is unavailable")


def rows_by_method_path(outputs):
    return {
        row["method_path_id"]: row
        for _, sidecar in outputs
        for row in sidecar["method_paths"]
    }


def bound_field(row, owner, field):
    if owner == "row":
        return row["claim_evidence"][field]
    owner_kind, owner_id = owner.split(":", 1)
    if owner_kind == "signal":
        signal = next(
            signal for signal in row["signals"] if signal["signal_id"] == owner_id
        )
        return signal["claim_evidence"][field]
    if owner_kind == "edge":
        return row["control_edges"][int(owner_id)]["claim_evidence"][field]
    raise AssertionError(f"unsupported binding owner {owner!r}")


def binding(value, kind="canon", quote="claim-bearing quote"):
    return {"value": copy.deepcopy(value), "kind": kind, "quote": quote}


def fixture_sidecar(
    method_path_id="2026.findings-acl.1724#pipeline",
    selection_policy="scored_select",
    selection_object="candidate_output",
    explicit_selection=True,
    edge_locator="canon: 'edge claim quote'",
):
    row = {
        "core_weight_update": False,
        "external_component_weight_update": False,
        "controller_program_or_config_optimized_on_labels": False,
        "human_or_dev_label_model_selection": False,
        "deployment_label_access": False,
        "test_item_gold_access": False,
        "inference_external_new_information": False,
        "internal_visibility": "api_only",
        "core_topology": "single_core",
        "core_native_modality": "text_only",
        "control_horizon": "sequential",
        "decision_rights": ["branch"],
        "candidate_pool_exists": True,
        "selection_policy": selection_policy,
        "selection_object": selection_object,
        "explicit_candidate_pool_selection": explicit_selection,
        "method_path_id": method_path_id,
        "signals": [
            {
                "signal_id": "s1",
                "form": "scalar_score",
                "source": "llm_judge",
                "lifecycle": "online_step",
                "uses": ["prune"],
                "claim_evidence": {
                    "form": binding("scalar_score"),
                    "lifecycle": binding("online_step"),
                    "uses": binding(["prune"]),
                },
            }
        ],
        "control_edges": [
            {
                "signal_id": "s1",
                "signal_use": "prune",
                "decision_right": "branch",
                "source_locator": edge_locator,
            }
        ],
    }
    row["claim_evidence"] = {field: binding(row[field]) for field in ROW14_FIELDS}
    return {
        "schema": "v2",
        "schema_v3_adjudicator": "must-not-survive",
        "method_paths": [row],
    }


class SchemaV3MigrationTest(unittest.TestCase):
    def test_minimal_fixture_has_exact_row16_signal4_edge2_bindings(self):
        source = fixture_sidecar()

        migrated = migrate_sidecar(source)
        row = migrated["method_paths"][0]

        self.assertEqual(list(row["claim_evidence"]), ROW_REQUIRED_FIELDS)
        self.assertEqual(
            list(row["signals"][0]["claim_evidence"]), SIGNAL_REQUIRED_FIELDS
        )
        self.assertEqual(
            list(row["control_edges"][0]["claim_evidence"]),
            EDGE_REQUIRED_FIELDS,
        )
        self.assertEqual(validate_bound_values(row), [])
        self.assertEqual(migrated["schema"], SCHEMA_TEXT)
        self.assertEqual(
            migrated["schema_v3_binding_status"], SCHEMA_V3_BINDING_STATUS
        )
        self.assertNotIn("schema_v3_adjudicator", migrated)

    def test_pending_migration_removes_both_adjudicator_field_names(self):
        source = fixture_sidecar()
        source["schema_v3_binding_adjudicator"] = "must-also-not-survive"

        migrated = migrate_sidecar(source)

        self.assertEqual(
            migrated["schema_v3_binding_status"], SCHEMA_V3_BINDING_STATUS
        )
        self.assertNotIn("schema_v3_binding_adjudicator", migrated)
        self.assertNotIn("schema_v3_adjudicator", migrated)

    def test_migration_does_not_mutate_source(self):
        source = fixture_sidecar()
        before = copy.deepcopy(source)

        migrate_sidecar(source)

        self.assertEqual(source, before)

    def test_anchor_replacement_is_recursive_and_counted(self):
        source = {
            "locator": "canon: 'x' (p4 probe)",
            "nested": ["p4 probe", "p5 cost"],
        }
        counts = {key: 0 for key in ANCHOR_REPLACEMENTS}

        migrated = replace_anchors(source, counts)

        self.assertEqual(
            migrated["locator"],
            "canon: 'x' (p4 anchor='create extend probe and prune branches')",
        )
        self.assertEqual(
            migrated["nested"],
            [
                "p4 anchor='create extend probe and prune branches'",
                "p5 anchor='accuracy cost trade off'",
            ],
        )
        self.assertEqual(counts["p4 probe"], 2)
        self.assertEqual(counts["p5 cost"], 1)
        self.assertNotIn("p4 probe", repr(migrated))

    def test_positive_selection_fields_clone_named_existing_binding(self):
        source = fixture_sidecar()
        original = source["method_paths"][0]["claim_evidence"]["selection_policy"]

        row = migrate_sidecar(source)["method_paths"][0]
        selection_object = row["claim_evidence"]["selection_object"]
        explicit_selection = row["claim_evidence"][
            "explicit_candidate_pool_selection"
        ]

        self.assertEqual(selection_object["kind"], original["kind"])
        self.assertEqual(selection_object["quote"], original["quote"])
        self.assertEqual(selection_object["value"], "candidate_output")
        self.assertEqual(explicit_selection["value"], True)
        self.assertIsNot(selection_object, original)
        self.assertIsNot(explicit_selection, original)
        self.assertIsNot(selection_object, explicit_selection)

    def test_absence_selection_fields_bind_actual_values_and_exact_policy_text(self):
        source = fixture_sidecar(
            method_path_id="2604.16529#pdr-random-k",
            selection_policy="random_sample",
            selection_object="none",
            explicit_selection=False,
        )

        row = migrate_sidecar(source)["method_paths"][0]

        for field in ("selection_object", "explicit_candidate_pool_selection"):
            evidence = row["claim_evidence"][field]
            self.assertEqual(evidence["kind"], "absence")
            self.assertEqual(evidence["value"], row[field])
            self.assertEqual(evidence["scope"], "complete pinned method path")
            self.assertEqual(evidence["note"], ABSENCE_SELECTION_NOTE)

    def test_signal_source_clones_form_binding_and_binds_source_value(self):
        row = migrate_sidecar(fixture_sidecar())["method_paths"][0]
        signal = row["signals"][0]

        self.assertEqual(signal["claim_evidence"]["source"]["value"], "llm_judge")
        self.assertEqual(
            signal["claim_evidence"]["source"]["quote"],
            signal["claim_evidence"]["form"]["quote"],
        )
        self.assertIsNot(
            signal["claim_evidence"]["source"],
            signal["claim_evidence"]["form"],
        )

    def test_edge_bindings_extract_canon_or_tex_quoted_locator(self):
        for kind in ("canon", "tex"):
            with self.subTest(kind=kind):
                row = migrate_sidecar(
                    fixture_sidecar(edge_locator=f"{kind}: 'edge claim quote'")
                )["method_paths"][0]
                evidence = row["control_edges"][0]["claim_evidence"]
                for field in EDGE_REQUIRED_FIELDS:
                    self.assertEqual(evidence[field]["kind"], kind)
                    self.assertEqual(evidence[field]["quote"], "edge claim quote")
                    self.assertEqual(
                        evidence[field]["value"], row["control_edges"][0][field]
                    )

    def test_edge_locator_without_canon_or_tex_quote_fails_closed(self):
        source = fixture_sidecar(edge_locator="p4 anchor='edge claim quote'")

        with self.assertRaisesRegex(ValueError, "extract.*canon.*tex.*quote"):
            migrate_sidecar(source)

    def test_source_binding_must_be_mapping_with_supported_kind(self):
        cases = {
            "not-mapping": "malformed binding",
            "unsupported-kind": {
                "value": "scored_select",
                "kind": "unsupported",
                "quote": "claim-bearing quote",
            },
            "non-string-kind": {
                "value": "scored_select",
                "kind": [],
                "quote": "claim-bearing quote",
            },
        }
        for label, malformed in cases.items():
            with self.subTest(label=label):
                source = fixture_sidecar()
                source["method_paths"][0]["claim_evidence"][
                    "selection_policy"
                ] = malformed
                with self.assertRaisesRegex(
                    MigrationError, "selection_policy.*(binding|kind)"
                ):
                    migrate_sidecar(source)

    def test_kind_specific_source_binding_shapes_fail_closed(self):
        cases = {
            "canon-blank-quote": {
                "value": False,
                "kind": "canon",
                "quote": "   ",
            },
            "absence-missing-note": {
                "value": False,
                "kind": "absence",
                "scope": "complete pinned method path",
            },
            "pdf-page-bad-page": {
                "value": False,
                "kind": "pdf_page",
                "page": 0,
                "anchor": "distinctive source phrase",
            },
            "pdf-page-blank-anchor": {
                "value": False,
                "kind": "pdf_page",
                "page": 4,
                "anchor": " ",
            },
        }
        for label, malformed in cases.items():
            with self.subTest(label=label):
                source = fixture_sidecar()
                source["method_paths"][0]["claim_evidence"][
                    "core_weight_update"
                ] = malformed
                with self.assertRaisesRegex(MigrationError, "core_weight_update"):
                    migrate_sidecar(source)

    def test_valid_pdf_page_binding_retains_page_and_anchor(self):
        source = fixture_sidecar()
        source["method_paths"][0]["claim_evidence"]["selection_policy"] = {
            "value": "scored_select",
            "kind": "pdf_page",
            "page": 4,
            "anchor": "distinctive source phrase",
        }

        migrated = migrate_sidecar(source)
        cloned = migrated["method_paths"][0]["claim_evidence"]["selection_object"]

        self.assertEqual(cloned["kind"], "pdf_page")
        self.assertEqual(cloned["page"], 4)
        self.assertEqual(cloned["anchor"], "distinctive source phrase")

    def test_signal_source_binding_is_validated_before_cloning(self):
        source = fixture_sidecar()
        source["method_paths"][0]["signals"][0]["claim_evidence"]["form"][
            "quote"
        ] = ""

        with self.assertRaisesRegex(MigrationError, "signal.*form.*quote"):
            migrate_sidecar(source)

    def test_edge_locator_rejects_malformed_truncated_or_ambiguous_quotes(self):
        malformed_locators = (
            "canon: 'agent's decision controls branch'",
            "canon: 'first claim'; tex: 'second claim'",
            "canon: 'unterminated claim",
            "canon: ''",
            "unknown: 'claim text'",
            "unknown-canon: 'claim text'",
            "unknown: canon: 'claim text'",
            "junk canon: 'claim text'",
            "canon: 'claim text' unknown-anchor='other text'",
            "canon: 'complete claim' trailing '",
        )
        for locator in malformed_locators:
            with self.subTest(locator=locator):
                with self.assertRaisesRegex(
                    MigrationError, "edge:0:.*canon.*tex.*quote"
                ):
                    migrate_sidecar(fixture_sidecar(edge_locator=locator))

    def test_no_explicit_selection_rows_reject_value_drift(self):
        drift = (
            {"selection_object": "candidate_output"},
            {"explicit_selection": True},
        )
        for override in drift:
            with self.subTest(override=override):
                kwargs = {
                    "method_path_id": "2604.16529#pdr-random-k",
                    "selection_policy": "random_sample",
                    "selection_object": "none",
                    "explicit_selection": False,
                    **override,
                }
                with self.assertRaisesRegex(
                    MigrationError, "NO_EXPLICIT_SELECTION.*selection"
                ):
                    migrate_sidecar(fixture_sidecar(**kwargs))

    def test_positive_selection_rows_reject_value_drift(self):
        drift = (
            {"selection_object": "none"},
            {"selection_object": None},
            {"selection_object": ""},
            {"selection_object": 0},
            {"selection_object": []},
            {"selection_object": {}},
            {"explicit_selection": False},
        )
        for override in drift:
            with self.subTest(override=override):
                kwargs = {
                    "selection_object": "candidate_output",
                    "explicit_selection": True,
                    **override,
                }
                with self.assertRaisesRegex(
                    MigrationError, "POSITIVE_SELECTION_EVIDENCE.*selection"
                ):
                    migrate_sidecar(fixture_sidecar(**kwargs))


class SchemaV3IntegrationTest(unittest.TestCase):
    def copy_pinned_sources(self, destination):
        destination.mkdir(parents=True)
        for source_path in sorted(SOURCE_DIR.glob("*.sidecar.json")):
            (destination / source_path.name).write_bytes(source_path.read_bytes())

    def test_pinned_corpus_has_exact_counts_and_complete_bindings(self):
        outputs = build_outputs(SOURCE_DIR)
        sidecars = [sidecar for _, sidecar in outputs]
        rows = [row for sidecar in sidecars for row in sidecar["method_paths"]]
        signals = [signal for row in rows for signal in row["signals"]]
        edges = [edge for row in rows for edge in row["control_edges"]]

        self.assertEqual(len(sidecars), 8)
        self.assertEqual(len(rows), 11)
        self.assertEqual(len(signals), 12)
        self.assertEqual(len(edges), 18)
        for sidecar in sidecars:
            self.assertEqual(sidecar["schema"], SCHEMA_TEXT)
            self.assertEqual(
                sidecar["schema_v3_binding_status"], SCHEMA_V3_BINDING_STATUS
            )
        for row in rows:
            self.assertEqual(validate_bound_values(row), [])

    def test_build_outputs_rejects_control_edge_count_drift(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source_dir = Path(temp_dir) / "sidecars"
            self.copy_pinned_sources(source_dir)
            target = source_dir / "2026.findings-acl.1243.sidecar.json"
            sidecar = json.loads(target.read_text(encoding="utf-8"))
            sidecar["method_paths"][0]["control_edges"].pop()
            target.write_text(
                json.dumps(sidecar, ensure_ascii=False, indent=1) + "\n",
                encoding="utf-8",
                newline="\n",
            )

            with self.assertRaisesRegex(
                MigrationError, "expected 18 control edges, found 17"
            ):
                build_outputs(source_dir)

    def test_adjudication_override_table_covers_exact_disagreement_tuples(self):
        overrides = getattr(migration, "BINDING_OVERRIDES", {})

        self.assertEqual(set(overrides), set(ADJUDICATION_REPAIR_BINDINGS))

    def test_pinned_corpus_has_exact_adjudication_repair_bindings(self):
        rows = rows_by_method_path(build_outputs(SOURCE_DIR))

        for key, expected in ADJUDICATION_REPAIR_BINDINGS.items():
            pid, owner, field = key
            with self.subTest(method_path_id=pid, owner=owner, field=field):
                self.assertEqual(bound_field(rows[pid], owner, field), expected)

        calibrated = rows["2602.16485#calibrated-orchestration"]
        profile = calibrated["signals"][0]
        repaired_edge = calibrated["control_edges"][1]
        route_binding = {
            "value": "route",
            "kind": "pdf_page",
            "page": 5,
            "anchor": "agents profiles to select only the most compatible tools",
        }
        self.assertEqual(profile["uses"], ["route"])
        self.assertEqual(
            profile["claim_evidence"]["uses"],
            {
                **route_binding,
                "value": ["route"],
            },
        )
        self.assertEqual(repaired_edge["signal_use"], "route")
        self.assertEqual(repaired_edge["decision_right"], "tool_call")
        self.assertEqual(
            repaired_edge["claim_evidence"]["decision_right"],
            {**route_binding, "value": "tool_call"},
        )

        pipeline = rows["2604.16529#rtv-pdr-pipeline"]
        exact_select_k = ADJUDICATION_REPAIR_BINDINGS[
            (
                "2604.16529#rtv-pdr-pipeline",
                "row",
                "explicit_candidate_pool_selection",
            )
        ]
        self.assertEqual(
            pipeline["claim_evidence"]["selection_policy"],
            {**exact_select_k, "value": "tournament_select"},
        )

    def test_adjudication_repair_evidence_resolves_in_pinned_sources(self):
        from pypdf import PdfReader

        data_root = pinned_data_root()
        pdf_paths = {
            "2026.findings-acl.511#prm-guided-search": (
                data_root
                / "survey-backups"
                / "2026.findings-acl.511"
                / "2026.findings-acl.511.pdf"
            ),
            "2602.16485#calibrated-orchestration": (
                data_root / "survey-fulltext" / "2602.16485" / "2602.16485.pdf"
            ),
            "2606.01667#agentic-orchestration": (
                data_root / "survey-fulltext" / "2606.01667" / "2606.01667.pdf"
            ),
            "2606.03054#trained-gate": (
                data_root / "survey-fulltext" / "2606.03054" / "2606.03054.pdf"
            ),
        }
        eprint_path = (
            data_root
            / "survey-fulltext"
            / "2604.16529"
            / "2604.16529.eprint"
        )
        with tarfile.open(eprint_path, "r:*") as archive:
            paper_member = archive.extractfile("paper.tex")
            self.assertIsNotNone(paper_member)
            paper_tex = paper_member.read().decode("utf-8")
        canon_text = (
            Path(__file__).resolve().parents[2]
            / "wiki"
            / "survey"
            / "2026-07-18-sf-known-item-dfs-systemcontrol.md"
        ).read_text(encoding="utf-8")
        readers = {}

        for key, binding_entry in ADJUDICATION_REPAIR_BINDINGS.items():
            pid, owner, field = key
            with self.subTest(method_path_id=pid, owner=owner, field=field):
                if binding_entry["kind"] == "pdf_page":
                    reader = readers.setdefault(pid, PdfReader(pdf_paths[pid]))
                    failures = []
                    locator = (
                        f"p{binding_entry['page']} "
                        f"anchor='{binding_entry['anchor']}'"
                    )
                    check_page_locator(
                        locator,
                        reader,
                        pid,
                        f"{owner}:{field}",
                        failures,
                    )
                    self.assertEqual(failures, [])
                elif binding_entry["kind"] == "tex":
                    self.assertIn(binding_entry["quote"], paper_tex)
                else:
                    self.assertEqual(binding_entry["kind"], "canon")
                    self.assertIn(binding_entry["quote"], canon_text)

    def test_replacement_explore_anchor_passes_real_pdf_locator_contract(self):
        from pypdf import PdfReader

        replacement = (
            "p4 anchor='repeatedly decides whether to call explore or to stop and "
            "synthesize'"
        )
        pdf_path = (
            pinned_data_root()
            / "survey-fulltext"
            / "2606.01667"
            / "2606.01667.pdf"
        )
        failures = []
        check_page_locator(
            replacement,
            PdfReader(pdf_path),
            "2606.01667#agentic-orchestration",
            "source_locator",
            failures,
        )

        self.assertEqual(failures, [])
        self.assertEqual(ANCHOR_REPLACEMENTS["p4 explore"], replacement)

    def test_all_pinned_anchor_occurrences_are_replaced_and_conserved(self):
        outputs = build_outputs(SOURCE_DIR)
        source_text = "".join(
            path.read_text(encoding="utf-8")
            for path in sorted(SOURCE_DIR.glob("*.sidecar.json"))
        )
        generated_text = "".join(
            json.dumps(sidecar, ensure_ascii=False) for _, sidecar in outputs
        )
        expected_counts = {
            "p4 probe": 2,
            "p5 cost": 1,
            "p3 Algorithm": 1,
            "p8 Fig": 2,
            "p14 delegated": 1,
            "p4 explore": 1,
        }

        self.assertEqual(set(expected_counts), set(ANCHOR_REPLACEMENTS))
        for source, expected_count in expected_counts.items():
            replacement = ANCHOR_REPLACEMENTS[source]
            self.assertEqual(source_text.count(source), expected_count)
            self.assertEqual(generated_text.count(source), 0)
            self.assertEqual(generated_text.count(replacement), expected_count)

    def test_write_outputs_is_stable_lf_utf8_and_matches_committed_outputs(self):
        outputs = build_outputs(SOURCE_DIR)
        committed_outputs = outputs
        adjudication_path = (
            Path(__file__).resolve().parents[2]
            / "wiki"
            / "survey"
            / "current"
            / "data"
            / "schema-v3-adjudication.json"
        )
        if adjudication_path.is_file():
            import sf_schema_v3_finalize as finalizer

            committed_outputs = finalizer.finalize_outputs(
                outputs,
                adjudication_path.read_bytes(),
            )
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "sidecars"
            write_outputs(committed_outputs, output_dir)
            first = {
                path.name: path.read_bytes()
                for path in sorted(output_dir.glob("*.sidecar.json"))
            }

            self.assertEqual(len(first), 8)
            self.assertEqual(
                set(first), {source_path.name for source_path, _ in committed_outputs}
            )
            for name, data in first.items():
                self.assertNotIn(b"\r", data, name)
                self.assertTrue(data.endswith(b"\n"), name)
                data.decode("utf-8")
                self.assertEqual(
                    data, (OUTPUT_DIR / name).read_bytes(), f"committed drift: {name}"
                )

            write_outputs(committed_outputs, output_dir)
            second = {
                path.name: path.read_bytes()
                for path in sorted(output_dir.glob("*.sidecar.json"))
            }
            self.assertEqual(second, first)

    def test_loader_rejects_duplicate_keys_and_nonfinite_constants(self):
        malformed_cases = {
            "duplicate key": '{"method_paths": [], "method_paths": []}\n',
            "non-finite JSON constant NaN": '{"method_paths": [], "x": NaN}\n',
        }
        for expected_error, malformed_json in malformed_cases.items():
            with self.subTest(expected_error=expected_error):
                with tempfile.TemporaryDirectory() as temp_dir:
                    source_dir = Path(temp_dir) / "sidecars"
                    self.copy_pinned_sources(source_dir)
                    target = sorted(source_dir.glob("*.sidecar.json"))[0]
                    target.write_text(malformed_json, encoding="utf-8", newline="\n")

                    with self.assertRaisesRegex(
                        MigrationError, rf"{target.name}.*{expected_error}"
                    ):
                        build_outputs(source_dir)

    def test_check_and_write_reject_nonportable_input_without_destination_drift(self):
        malformed_values = ("overflow-number", "unpaired-surrogate")
        for case in malformed_values:
            with self.subTest(case=case):
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_root = Path(temp_dir)
                    source_dir = temp_root / "source"
                    output_dir = temp_root / "destination"
                    self.copy_pinned_sources(source_dir)
                    write_outputs(build_outputs(SOURCE_DIR), output_dir)
                    before = {
                        path.name: path.read_bytes()
                        for path in sorted(output_dir.glob("*.sidecar.json"))
                    }
                    target = sorted(source_dir.glob("*.sidecar.json"))[0]
                    source_text = target.read_text(encoding="utf-8")
                    if case == "overflow-number":
                        malformed_source = source_text.replace(
                            "{\n", '{\n "strict_input_probe": 1e9999,\n', 1
                        )
                    else:
                        malformed_source = source_text.replace(
                            '"method_path_id": '
                            '"2026.findings-acl.1243#closed-prompt-only"',
                            '"method_path_id": "\\ud800"',
                            1,
                        )
                    target.write_text(
                        malformed_source,
                        encoding="utf-8",
                        newline="\n",
                    )

                    for mode in ("--check", "--write"):
                        with self.subTest(case=case, mode=mode):
                            stdout = io.StringIO()
                            stderr = io.StringIO()
                            with redirect_stdout(stdout), redirect_stderr(stderr):
                                exit_code = main(
                                    [mode],
                                    source_dir=source_dir,
                                    output_dir=output_dir,
                                )
                            self.assertNotEqual(exit_code, 0)
                            self.assertNotIn("schema-v3 migration: PASS", stdout.getvalue())
                            self.assertIn("schema-v3 migration: ERROR:", stderr.getvalue())
                            self.assertFalse(
                                any(
                                    0xD800 <= ord(char) <= 0xDFFF
                                    for char in stderr.getvalue()
                                )
                            )
                            after = {
                                path.name: path.read_bytes()
                                for path in sorted(output_dir.glob("*.sidecar.json"))
                            }
                            self.assertEqual(after, before)

    def test_renderer_rejects_nan_before_touching_destination(self):
        outputs = build_outputs(SOURCE_DIR)
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "sidecars"
            write_outputs(outputs, output_dir)
            before = {
                path.name: path.read_bytes()
                for path in sorted(output_dir.glob("*.sidecar.json"))
            }
            outputs[0][1]["not_json"] = float("nan")

            with self.assertRaisesRegex(MigrationError, "render.*non-finite"):
                write_outputs(outputs, output_dir)

            after = {
                path.name: path.read_bytes()
                for path in sorted(output_dir.glob("*.sidecar.json"))
            }
            self.assertEqual(after, before)

    def test_destination_rejects_stale_sidecar_without_deleting_or_writing(self):
        outputs = build_outputs(SOURCE_DIR)
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "sidecars"
            output_dir.mkdir()
            stale = output_dir / "stale.sidecar.json"
            stale.write_bytes(b"stale bytes\n")

            with self.assertRaisesRegex(MigrationError, "unexpected.*stale"):
                write_outputs(outputs, output_dir)

            self.assertEqual(stale.read_bytes(), b"stale bytes\n")
            self.assertEqual(list(output_dir.iterdir()), [stale])

    def test_source_rename_rejects_old_destination_name_without_deleting_it(self):
        outputs = build_outputs(SOURCE_DIR)
        old_source, first_sidecar = outputs[0]
        renamed_source = old_source.with_name("renamed.sidecar.json")
        renamed_outputs = [(renamed_source, first_sidecar), *outputs[1:]]
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "sidecars"
            output_dir.mkdir()
            old_destination = output_dir / old_source.name
            old_destination.write_bytes(b"old destination bytes\n")

            with self.assertRaisesRegex(MigrationError, "unexpected.*old destination"):
                write_outputs(renamed_outputs, output_dir)

            self.assertEqual(old_destination.read_bytes(), b"old destination bytes\n")
            self.assertEqual(list(output_dir.iterdir()), [old_destination])

    def test_replace_failure_cleans_every_temporary_sibling(self):
        outputs = build_outputs(SOURCE_DIR)
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "sidecars"
            with mock.patch(
                "sf_schema_v3_migrate.os.replace",
                side_effect=OSError("forced replacement failure"),
            ):
                with self.assertRaisesRegex(OSError, "forced replacement failure"):
                    write_outputs(outputs, output_dir)

            self.assertEqual(list(output_dir.glob("*.tmp")), [])

    def test_build_and_temp_write_leave_pinned_source_bytes_unchanged(self):
        source_paths = sorted(SOURCE_DIR.glob("*.sidecar.json"))
        before_bytes = {path.name: path.read_bytes() for path in source_paths}
        before_hashes = {
            name: hashlib.sha256(data).hexdigest()
            for name, data in before_bytes.items()
        }

        outputs = build_outputs(SOURCE_DIR)
        with tempfile.TemporaryDirectory() as temp_dir:
            write_outputs(outputs, Path(temp_dir) / "sidecars")

        after_bytes = {path.name: path.read_bytes() for path in source_paths}
        after_hashes = {
            name: hashlib.sha256(data).hexdigest()
            for name, data in after_bytes.items()
        }
        self.assertEqual(after_bytes, before_bytes)
        self.assertEqual(after_hashes, before_hashes)

    def test_cli_check_is_injectable_exact_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "must-not-exist"
            stdout = io.StringIO()
            stderr = io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                exit_code = main(
                    ["--check"], source_dir=SOURCE_DIR, output_dir=output_dir
                )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stdout.getvalue(), SUCCESS_LINE + "\n")
            self.assertEqual(stderr.getvalue(), "")
            self.assertFalse(output_dir.exists())

    def test_cli_rejects_both_modes_nonzero(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            with self.assertRaises(SystemExit) as raised:
                main(
                    ["--check", "--write"],
                    source_dir=SOURCE_DIR,
                    output_dir=OUTPUT_DIR,
                )
        self.assertNotEqual(raised.exception.code, 0)
        self.assertIn("not allowed with argument --check", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
