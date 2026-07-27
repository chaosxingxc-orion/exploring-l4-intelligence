#!/usr/bin/env python3
"""Adversarial contracts for the lossless existing-corpus union graph."""
from __future__ import annotations

import copy
import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import sf_existing_corpus_disposition as disposition  # noqa: E402


EXPECTED_DENOMINATORS = {
    "census": 95,
    "seed": 92,
    "bibliography": 65,
    "claim": 62,
    "version_pin": 30,
    "fulltext": 1243,
    "reviewer_known": 19,
}


class ExistingCorpusDispositionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = disposition.load_source_rows()
        cls.artifact = disposition.build_union(cls.sources)

    def test_source_denominators_are_real_rows_not_assumed_work_counts(self):
        self.assertEqual(
            EXPECTED_DENOMINATORS,
            {campaign: len(rows) for campaign, rows in self.sources.items()},
        )
        self.assertEqual(EXPECTED_DENOMINATORS, self.artifact["source_denominators"])

    def test_every_source_row_has_exactly_one_explicit_destination(self):
        expected = {
            (campaign, row["source_row_id"])
            for campaign, rows in self.sources.items()
            for row in rows
        }
        destinations = [
            (row["campaign"], row["source_row_id"])
            for row in self.artifact["source_dispositions"]
        ]
        self.assertEqual(len(expected), len(destinations))
        self.assertEqual(expected, set(destinations))
        self.assertEqual(len(destinations), len(set(destinations)))
        self.assertEqual(0, self.artifact["summary"]["unexplained_orphans"])

    def test_metadata_rows_are_explicit_destinations_not_fake_works(self):
        metadata = [
            row for row in self.artifact["source_dispositions"]
            if row["destination_type"] == "SOURCE_METADATA"
        ]
        self.assertEqual(
            {("version_pin", "line:0001|_meta"), ("fulltext", "line:0025|NOTE")},
            {(row["campaign"], row["source_row_id"]) for row in metadata},
        )
        self.assertTrue(all(row["canonical_work_id"] is None for row in metadata))

    def test_named_heterogeneous_cases_preserve_every_claim_grade_and_status(self):
        expected = {
            "P-0005": {
                "count": 5,
                "grades": {
                    "CLAIM_LOCATED_FULLTEXT",
                    "FULLTEXT_UNREACHABLE_THIS_ROUND",
                    "ABSTRACT_ONLY",
                    "SYNTHESIS_PENDING_REVIEW",
                },
                "statuses": {"MINOR", "UNVERIFIED", "MATERIAL"},
            },
            "P-0031": {
                "count": 8,
                "grades": {
                    "CLAIM_LOCATED_FULLTEXT",
                    "FULLTEXT_UNREACHABLE_THIS_ROUND",
                    "ABSTRACT_ONLY",
                    "SYNTHESIS_PENDING_REVIEW",
                },
                "statuses": {"MINOR", "UNVERIFIED", "NONE", "MATERIAL"},
            },
            "P-0071": {
                "count": 6,
                "grades": {"CLAIM_LOCATED_FULLTEXT", "SYNTHESIS_PENDING_REVIEW"},
                "statuses": {"MATERIAL", "MINOR", "NONE"},
            },
            "P-0080": {
                "count": 2,
                "grades": {"CLAIM_LOCATED_FULLTEXT", "ABSTRACT_ONLY"},
                "statuses": {"MATERIAL", "NONE"},
            },
        }
        by_cluster = {
            identity["source_id"]: node
            for node in self.artifact["canonical_work_nodes"]
            for identity in node["identities"]
            if identity["source_id"].startswith("P-")
        }
        for cluster_id, contract in expected.items():
            with self.subTest(cluster_id=cluster_id):
                node = by_cluster[cluster_id]
                evidence = node["claim_evidence"]
                self.assertEqual(contract["count"], len(evidence))
                self.assertEqual(contract["grades"], {row["evidence_grade"] for row in evidence})
                self.assertEqual(
                    contract["statuses"],
                    {row["discrepancy_status"] for row in evidence},
                )
                self.assertNotIn("evidence_grade", node)
                self.assertNotIn("discrepancy_status", node)

    def test_graph_reports_the_reviewer_reproduced_heterogeneity_without_collapse(self):
        self.assertEqual(5, self.artifact["summary"]["multi_target_claim_edges"])
        self.assertEqual(16, self.artifact["summary"]["multi_claim_work_count"])
        self.assertEqual(15, self.artifact["summary"]["multi_evidence_grade_work_count"])
        self.assertEqual(12, self.artifact["summary"]["multi_discrepancy_status_work_count"])

    def test_claim_works_are_deduplicated_and_never_generate_seed_rows(self):
        accounting = self.artifact["deduplication_accounting"]
        self.assertEqual(95, accounting["unique_census_works"])
        self.assertEqual(92, accounting["seed_source_rows"])
        self.assertEqual(92, accounting["unique_seed_works"])
        self.assertEqual(0, accounting["duplicate_seed_source_rows"])
        self.assertEqual(13, accounting["seed_rows_reusing_census_work"])
        self.assertEqual(0, accounting["generated_seed_rows"])
        self.assertEqual(62, accounting["claim_source_rows"])
        self.assertEqual(75, accounting["claim_work_references"])
        self.assertEqual(31, accounting["unique_claim_works"])
        self.assertEqual(44, accounting["deduplicated_claim_work_references"])
        self.assertEqual(0, accounting["claim_targets_not_in_census"])

    def test_split_census_works_are_not_over_deduplicated_by_shared_cluster_alias(self):
        destinations = {
            row["source_row_id"]: row["canonical_work_id"]
            for row in self.artifact["source_dispositions"]
            if row["campaign"] == "census"
        }
        self.assertNotEqual(
            destinations["line:0016|W-0016"],
            destinations["line:0017|W-0017"],
        )

    def test_duplicate_seed_external_id_reuses_one_canonical_work(self):
        builder = disposition.UnionBuilder()
        first = {
            "source_row_id": "line:0001|2503.23395",
            "payload": {"id": "2503.23395", "name": "Alias A"},
        }
        second = {
            "source_row_id": "line:0002|arxiv:2503.23395",
            "payload": {"id": "arxiv:2503.23395", "name": "Alias B"},
        }
        builder.add_seed(first)
        builder.add_seed(second)
        self.assertEqual(1, len(builder.nodes))
        node = next(iter(builder.nodes.values()))
        self.assertEqual(2, len(node["source_memberships"]))

    def test_claim_cannot_create_a_work_or_seed(self):
        builder = disposition.UnionBuilder()
        row = {
            "source_row_id": "line:0001|CL-X",
            "payload": {
                "claim_id": "CL-X",
                "paper_work_id": "P-MISSING",
                "arxiv_id": "2999.99999",
            },
        }
        with self.assertRaisesRegex(ValueError, "exactly one inherited canonical work"):
            builder.add_claim(row)
        self.assertEqual({}, builder.nodes)

    def test_flattened_claim_scalar_or_lost_claim_fails_closed(self):
        mutated = copy.deepcopy(self.artifact)
        node = next(
            node for node in mutated["canonical_work_nodes"]
            if any(identity["source_id"] == "P-0031" for identity in node["identities"])
        )
        node["evidence_grade"] = "CLAIM_LOCATED_FULLTEXT"
        node["claim_evidence"].pop()
        failures = disposition.validate_union(mutated, self.sources)
        self.assertIn("WORK_LEVEL_CLAIM_SCALAR", failures)
        self.assertIn("CLAIM_MEMBERSHIP_MISMATCH", failures)

    def test_duplicate_source_membership_fails_closed(self):
        mutated = copy.deepcopy(self.artifact)
        member = copy.deepcopy(mutated["canonical_work_nodes"][0]["source_memberships"][0])
        mutated["canonical_work_nodes"][1]["source_memberships"].append(member)
        self.assertIn(
            "DUPLICATE_SOURCE_MEMBERSHIP",
            disposition.validate_union(mutated, self.sources),
        )

    def test_screening_role_contract_fails_closed(self):
        mutated = copy.deepcopy(self.artifact)
        node = next(
            node for node in mutated["canonical_work_nodes"]
            if node["screening_decision"] == "INCLUDE"
        )
        node["screening_decision"] = "EXCLUDE"
        node["reference_role"] = "KNOWN_QUEUE"
        node["current_disposition"]["reason_code"] = "NOT_REC_0"
        failures = disposition.validate_union(mutated, self.sources)
        self.assertIn("EXCLUDE_WITH_ROLE", failures)
        self.assertIn("EXCLUDE_WITHOUT_REC_0", failures)

    def test_generic_unresolved_bucket_fails_closed(self):
        mutated = copy.deepcopy(self.artifact)
        node = next(
            node for node in mutated["canonical_work_nodes"]
            if node["screening_decision"] == "UNRESOLVED"
        )
        node["current_disposition"].pop("owner")
        node["current_disposition"].pop("deadline_gate")
        self.assertIn(
            "UNRESOLVED_OBLIGATION_INCOMPLETE",
            disposition.validate_union(mutated, self.sources),
        )

    def test_exact_alias_and_unresolved_identity_relations_remain_distinct(self):
        relations = {
            identity["relation"]
            for node in self.artifact["canonical_work_nodes"]
            for identity in node["identities"]
        }
        self.assertEqual(disposition.RELATIONS, relations)

    def test_source_receipt_mutation_fails_closed(self):
        mutated = copy.deepcopy(self.artifact)
        mutated["source_receipts"][0]["sha256"] = "0" * 64
        self.assertIn(
            "SOURCE_RECEIPT_MISMATCH",
            disposition.validate_union(mutated, self.sources),
        )

    def test_duplicate_canonical_external_identity_fails_closed(self):
        mutated = copy.deepcopy(self.artifact)
        source = next(
            node for node in mutated["canonical_work_nodes"]
            if any(identity["source_id"] == "2503.23395" for identity in node["identities"])
        )
        target = next(node for node in mutated["canonical_work_nodes"] if node is not source)
        target["identities"].append(
            {
                "source_id": "2503.23395",
                "relation": "EXACT_ID",
                "provenance": "mutation",
            }
        )
        self.assertIn(
            "DUPLICATE_CANONICAL_IDENTITY",
            disposition.validate_union(mutated, self.sources),
        )

    def test_reference_roles_are_exactly_the_current_protocol_taxonomy(self):
        observed = {
            node["reference_role"]
            for node in self.artifact["canonical_work_nodes"]
            if node["reference_role"] is not None
        }
        self.assertEqual(disposition.CANONICAL_ROLES, observed)
        self.assertEqual([], disposition.validate_union(self.artifact, self.sources))

    def test_version_pins_and_arxiv_identity_sets_are_separate_and_equal(self):
        identity = self.artifact["identity_accounting"]
        self.assertNotEqual(
            identity["all_arxiv_identity_count"],
            identity["version_pinned_work_count"],
        )
        self.assertEqual(
            identity["version_pinned_work_ids"],
            identity["version_pinned_arxiv_work_ids"],
        )
        self.assertTrue(identity["version_pinned_arxiv_set_equal"])

    def test_reviewer_known_artifact_is_frozen_and_has_no_query_recall_credit(self):
        artifact = json.loads(disposition.REVIEWER_KNOWN_PATH.read_text(encoding="utf-8"))
        self.assertEqual(19, len(artifact["items"]))
        self.assertEqual("REVIEW_CLAIM_VERIFICATION", artifact["access_class"])
        self.assertFalse(artifact["query_recall_credit"])
        self.assertEqual(
            artifact["items_sha256"],
            hashlib.sha256(disposition.canonical_json_bytes(artifact["items"])).hexdigest(),
        )
        self.assertEqual(
            disposition.REVIEW_SOURCE_SHA256,
            artifact["source_provenance"]["sha256"],
        )
        self.assertEqual(
            disposition.REVIEW_2026_07_21_SOURCE_SHA256,
            artifact["additional_source_provenance"]["sha256"],
        )
        self.assertEqual(
            disposition.ROUND16_PRECHECK_SOURCE_SHA256,
            artifact["round16_precheck_source_provenance"]["sha256"],
        )
        self.assertEqual(
            disposition.ROUND17_WORKING_BRIEF_SOURCE_SHA256,
            artifact["round17_working_brief_source_provenance"]["sha256"],
        )
        by_id = {item["arxiv_id"]: item for item in artifact["items"]}
        self.assertEqual(
            {"2502.04128", "2602.22897", "2602.00846", "2512.16899"},
            {identity for identity in by_id if identity in {
                "2502.04128", "2602.22897", "2602.00846", "2512.16899"
            }},
        )
        self.assertTrue(
            all(by_id[identity]["query_recall_credit"] is False for identity in {
                "2502.04128", "2602.22897", "2602.00846", "2512.16899"
            })
        )
        self.assertEqual(
            {"2606.00579", "2606.03183", "2502.19328", "2605.10344", "2508.00890"},
            {identity for identity in by_id if identity in {
                "2606.00579", "2606.03183", "2502.19328", "2605.10344", "2508.00890"
            }},
        )
        self.assertTrue(
            all(by_id[identity]["query_recall_credit"] is False for identity in {
                "2606.00579", "2606.03183", "2502.19328", "2605.10344", "2508.00890"
            })
        )
        self.assertEqual(
            {"2607.11433", "2605.28192", "2607.05511", "2605.22012"},
            {identity for identity in by_id if identity in {
                "2607.11433", "2605.28192", "2607.05511", "2605.22012"
            }},
        )

    def test_round17_core_priors_are_unique_and_rerouted(self):
        by_identity = {
            identity["source_id"]: node
            for node in self.artifact["canonical_work_nodes"]
            for identity in node["identities"]
            if identity["source_id"] in {
                "2607.11433", "2605.28192", "2607.05511", "2605.22012"
            }
        }
        self.assertEqual(4, len(by_identity))
        self.assertEqual("DEEPLY_READ", by_identity["2607.11433"]["reference_role"])
        self.assertEqual("DEEPLY_READ", by_identity["2605.28192"]["reference_role"])
        self.assertEqual("BOUNDARY_COMPARATOR", by_identity["2607.05511"]["reference_role"])
        self.assertEqual("BOUNDARY_COMPARATOR", by_identity["2605.22012"]["reference_role"])

    def test_build_is_deterministic_and_never_loads_query_or_attempt_registries(self):
        self.assertEqual(self.artifact, disposition.build_union(self.sources))
        paths = {path.as_posix() for path in disposition.source_paths()}
        self.assertFalse(any("sf-queries" in path for path in paths))
        self.assertFalse(any("experiment_attempt_registry" in path for path in paths))

    def test_write_then_check_round_trip(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            artifact_path = root / "existing-corpus-disposition-v1.json"
            report_path = root / "existing-corpus-disposition-check.json"
            disposition.write_outputs(
                self.artifact,
                artifact_path=artifact_path,
                report_path=report_path,
            )
            self.assertEqual(
                [],
                disposition.check_outputs(
                    self.artifact,
                    artifact_path=artifact_path,
                    report_path=report_path,
                ),
            )
            artifact_path.write_text("{}\n", encoding="utf-8")
            self.assertIn(
                "ARTIFACT_DRIFT",
                disposition.check_outputs(
                    self.artifact,
                    artifact_path=artifact_path,
                    report_path=report_path,
                ),
            )


if __name__ == "__main__":
    unittest.main()
