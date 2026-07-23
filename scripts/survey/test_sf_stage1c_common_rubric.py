from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "wiki/survey/current/data/stage1c-common-rubric-comparison-v1.json"
TABLE = REPO / "wiki/survey/current/tables/stage1c-common-rubric-comparison.md"
STATUS = REPO / "wiki/survey/current/status.md"
MANIFEST_SCRIPT = REPO / "scripts/survey/sf_current_manifest.py"
BIBLIOGRAPHY = REPO / "wiki/survey/current/bibliography.md"
FETCH_SCRIPT = REPO / "scripts/data/fetch-stage1c-priority-papers.sh"

OUTSIDE_UNION_IDS = {
    "CW-ARXIV-2510.00743",
    "CW-ARXIV-2510.14664",
    "CW-ARXIV-2511.07931",
    "CW-ARXIV-2605.23261",
    "CW-ARXIV-2605.30256",
}
PRIORITY_IDS = {
    "CW-ACL-2026.findings-eacl.151",
    "CW-ACL-2026.acl-long.1615",
    "CW-ARXIV-2508.18240",
    "CW-ARXIV-2603.16924",
}
RUBRIC = {
    "problem_distinctness",
    "decision_causality",
    "measurement_validity",
    "modality_necessity",
    "failure_severity",
    "feasibility",
    "reproduction_anchor",
    "scope_compatibility",
    "evidence_maturity",
}
BUNDLES = {
    "BUDGET_STOP_REPAIR",
    "EVALUATOR_REWARD_RELIABILITY",
    "INTERACTIVE_FULL_DUPLEX_OBJECTIVES",
}


class Stage1CCommonRubricContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = json.loads(DATA.read_text(encoding="utf-8"))

    def test_authority_is_comparison_only_and_unranked(self) -> None:
        authority = self.document["authority"]
        self.assertEqual("STAGE_1C_COMMON_RUBRIC_COMPARISON", self.document["stage"])
        self.assertEqual("COMMON_RUBRIC_PROBLEM_COMPARISON_ONLY", authority["granted"])
        self.assertEqual(
            {
                "model_or_api_execution",
                "dataset_or_benchmark_metrics",
                "paper_reproduction",
                "prototype_implementation",
                "problem_ranking_or_selection",
                "novelty_verdict",
            },
            set(authority["withheld"]),
        )

    def test_five_outside_union_actions_are_corrected_without_duplicate_seed(self) -> None:
        rows = [
            row
            for row in self.document["routing_corrections"]
            if row["correction_type"] == "OUTSIDE_UNION_ACTION"
        ]
        self.assertEqual(OUTSIDE_UNION_IDS, {row["canonical_work_id"] for row in rows})
        for row in rows:
            self.assertEqual(
                "REGISTER_REVIEWER_DIRECTED_CANONICAL_ID_NO_DUPLICATE_SEED",
                row["corrected_value"],
            )
            self.assertTrue(row["reuses_single_canonical_work"])

    def test_role_and_signal_corrections_preserve_v5_provenance(self) -> None:
        corrections = {
            row["canonical_work_id"]: row
            for row in self.document["routing_corrections"]
        }
        joint_av = corrections["CW-ARXIV-2606.03183"]
        self.assertEqual("BOUNDARY", joint_av["current_disposition"])
        self.assertEqual("TRANSFER_BOUNDARY_DIRECT_CONTROL", joint_av["corrected_value"])
        mugen = corrections["CW-ARXIV-2603.09714"]
        self.assertEqual("SELF_CONSISTENCY_CONSENSUS", mugen["corrected_value"])
        self.assertEqual("PRESERVED_AS_HISTORICAL_RELEASE", self.document["stage1b_v5_taxonomy"])

    def test_priority_intake_has_one_route_per_canonical_work(self) -> None:
        rows = self.document["priority_intake"]
        ids = [row["canonical_work_id"] for row in rows]
        self.assertEqual(PRIORITY_IDS, set(ids))
        self.assertEqual(len(ids), len(set(ids)))
        for row in rows:
            self.assertIn(row["current_disposition"], {"INCLUDE", "BOUNDARY", "EXCLUDE_WITH_REASON", "QUEUED"})
            self.assertTrue(row["official_url"].startswith("https://"))

    def test_three_bundles_share_complete_rubric_without_ranking(self) -> None:
        rows = self.document["bundles"]
        self.assertEqual(BUNDLES, {row["bundle_id"] for row in rows})
        for row in rows:
            self.assertEqual("UNRANKED_NOT_SELECTED", row["selection_status"])
            self.assertEqual(RUBRIC, set(row["rubric"]))
            for assessment in row["rubric"].values():
                self.assertEqual({"assessment", "uncertainty"}, set(assessment))
                self.assertTrue(assessment["assessment"])
                self.assertTrue(assessment["uncertainty"])

    def test_human_table_and_hot_status_expose_the_same_boundary(self) -> None:
        table = TABLE.read_text(encoding="utf-8")
        status = STATUS.read_text(encoding="utf-8")
        for token in (*BUNDLES, *RUBRIC):
            self.assertIn(token, table)
        self.assertIn("Stage-1C common-rubric comparison started", status)
        self.assertIn("problem ranking and selection remain withheld", status)

    def test_current_manifest_routes_the_new_machine_and_human_surfaces(self) -> None:
        source = MANIFEST_SCRIPT.read_text(encoding="utf-8")
        self.assertIn(
            "wiki/survey/current/data/stage1c-common-rubric-comparison-v1.json",
            source,
        )
        self.assertIn(
            "wiki/survey/current/tables/stage1c-common-rubric-comparison.md",
            source,
        )

    def test_joint_av_coarse_role_is_boundary_in_active_bibliography(self) -> None:
        line = next(
            line
            for line in BIBLIOGRAPHY.read_text(encoding="utf-8").splitlines()
            if "Inference-Time Scaling for Joint Audio-Video Generation" in line
        )
        self.assertIn("| BOUNDARY_COMPARATOR |", line)

    def test_priority_fulltexts_have_one_reproducible_external_fetch_recipe(self) -> None:
        source = FETCH_SCRIPT.read_text(encoding="utf-8")
        for identity in (
            "2026.findings-eacl.151",
            "2026.acl-long.1615",
            "2508.18240",
            "2603.16924",
        ):
            self.assertIn(identity, source)
        self.assertIn("SPEECHRL_DATA_DIR", source)
        self.assertIn("aria2c", source)
        self.assertIn("sha256sum", source)


if __name__ == "__main__":
    unittest.main()
