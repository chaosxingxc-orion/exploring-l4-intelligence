from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.survey import sf_stage1c_v2_positive_support_preflight as preflight


REPO = Path(__file__).resolve().parents[2]
RC2R3 = REPO / "wiki/survey/workbench/system-first-stage1c-v2-precalibration-rc2r3"
R1 = REPO / "wiki/survey/workbench/system-first-stage1c-v2-agentic-calibration-r1/frozen-r1"
PREFLIGHT_LEDGER = REPO / (
    "wiki/survey/workbench/system-first-stage1c-v2-agentic-calibration-r1/"
    "positive-support-ledger-r1.json"
)
PREFLIGHT_REPORT = REPO / (
    "wiki/survey/workbench/system-first-stage1c-v2-agentic-calibration-r1/"
    "positive-support-preflight-r1.json"
)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class Stage1cV2PositiveSupportPreflightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load(RC2R3 / "calibration-response-schema-v4-inherited.json")
        cls.packet = load(RC2R3 / "calibration-blind-packet-v4-inherited.json")
        cls.sources = load(RC2R3 / "calibration-source-byte-manifest-v4-inherited.json")
        cls.coder_a = load(R1 / "coder-a-responses.json")
        cls.coder_b = load(R1 / "coder-b-responses.json")

    def evidence_ledger(self) -> dict:
        return {
            "schema": "sf-stage1c-v2-positive-support-ledger-v1",
            "visibility": "REVIEWER_ONLY_NOT_DISTRIBUTED",
            "mandatory_object_classes": ["dataset_edges", "reproduction_evidence"],
            "evidence": {
                "dataset_edges": [
                    {
                        "paper_id": "acl:2026.findings-eacl.151",
                        "rendition_id": "SRC-2026.findings-eacl.151-PDF",
                        "locator": {"page": 3, "section": "3.1 Existing Benchmark Pitfalls"},
                        "support_type": "SUBSET_OF",
                        "evidence_summary": "The evaluated data use the English subset of S2S-Arena.",
                    },
                    {
                        "paper_id": "acl:2026.findings-eacl.151",
                        "rendition_id": "SRC-2026.findings-eacl.151-PDF",
                        "locator": {"page": 3, "section": "3.1 Existing Benchmark Pitfalls"},
                        "support_type": "REANNOTATED_FROM",
                        "evidence_summary": "The work re-annotates SpeakBench and S2S-Arena.",
                    },
                ],
                "reproduction_evidence": [],
            },
        }

    def test_real_r1_fails_for_blind_local_state_and_zero_reproduction_support(self) -> None:
        result = preflight.evaluate_preflight(
            response_schema=self.schema,
            blind_packet=self.packet,
            source_manifest=self.sources,
            evidence_ledger=self.evidence_ledger(),
            coder_responses={"A": self.coder_a, "B": self.coder_b},
        )
        self.assertEqual("FAIL", result["status"])
        self.assertIn(
            "BLIND_FIELD_DEPENDS_ON_WITHHELD_REPOSITORY_STATE:reproduction_evidence.local_asset_state",
            result["defects"],
        )
        self.assertIn(
            "MANDATORY_CLASS_ZERO_POSITIVE:reproduction_evidence", result["defects"]
        )
        self.assertIn(
            "POSITIVE_SUPPORT_MISSED_BY_BOTH_CODERS:dataset_edges", result["defects"]
        )
        self.assertEqual(2, result["object_classes"]["dataset_edges"]["support_count"])
        self.assertEqual(
            {"A": 0, "B": 0},
            result["object_classes"]["dataset_edges"]["coder_object_counts"],
        )

    def test_repaired_blind_contract_passes_when_every_mandatory_class_has_support(self) -> None:
        schema = copy.deepcopy(self.schema)
        reproduction = schema["$defs"]["reproduction_evidence"]
        reproduction["required"].remove("local_asset_state")
        reproduction["properties"].pop("local_asset_state")
        ledger = self.evidence_ledger()
        ledger["evidence"]["reproduction_evidence"] = [
            {
                "paper_id": "arxiv:2510.02995",
                "rendition_id": "SRC-2510.02995-PDF",
                "locator": {"page": 1, "section": "Abstract"},
                "support_type": "PAPER_REPRODUCTION_SUPPORT",
                "evidence_summary": "Fixture asserts paper-visible reproduction support.",
            }
        ]
        result = preflight.evaluate_preflight(
            response_schema=schema,
            blind_packet=self.packet,
            source_manifest=self.sources,
            evidence_ledger=ledger,
        )
        self.assertEqual("PASS", result["status"])
        self.assertEqual([], result["defects"])

    def test_reviewer_ledger_visibility_and_leakage_fail_closed(self) -> None:
        ledger = self.evidence_ledger()
        ledger["visibility"] = "CODER_VISIBLE"
        with self.assertRaisesRegex(preflight.PreflightError, "reviewer-only"):
            preflight.evaluate_preflight(
                response_schema=self.schema,
                blind_packet=self.packet,
                source_manifest=self.sources,
                evidence_ledger=ledger,
            )
        ledger = self.evidence_ledger()
        ledger["evidence"]["dataset_edges"][0]["selection_rationale"] = "known positive"
        with self.assertRaisesRegex(preflight.PreflightError, "forbidden leakage key"):
            preflight.evaluate_preflight(
                response_schema=self.schema,
                blind_packet=self.packet,
                source_manifest=self.sources,
                evidence_ledger=ledger,
            )

    def test_unknown_paper_rendition_and_bad_locator_fail_closed(self) -> None:
        ledger = self.evidence_ledger()
        ledger["evidence"]["dataset_edges"][0]["paper_id"] = "arxiv:unknown"
        with self.assertRaisesRegex(preflight.PreflightError, "unknown paper"):
            preflight.evaluate_preflight(
                response_schema=self.schema,
                blind_packet=self.packet,
                source_manifest=self.sources,
                evidence_ledger=ledger,
            )
        ledger = self.evidence_ledger()
        ledger["evidence"]["dataset_edges"][0]["rendition_id"] = "SRC-WRONG-PDF"
        with self.assertRaisesRegex(preflight.PreflightError, "unknown rendition"):
            preflight.evaluate_preflight(
                response_schema=self.schema,
                blind_packet=self.packet,
                source_manifest=self.sources,
                evidence_ledger=ledger,
            )
        ledger = self.evidence_ledger()
        ledger["evidence"]["dataset_edges"][0]["locator"]["page"] = 0
        with self.assertRaisesRegex(preflight.PreflightError, "positive page"):
            preflight.evaluate_preflight(
                response_schema=self.schema,
                blind_packet=self.packet,
                source_manifest=self.sources,
                evidence_ledger=ledger,
            )

    def test_mandatory_class_and_coder_identity_must_be_exact(self) -> None:
        ledger = self.evidence_ledger()
        ledger["mandatory_object_classes"] = ["dataset_edges", "dataset_edges"]
        with self.assertRaisesRegex(preflight.PreflightError, "unique mandatory"):
            preflight.evaluate_preflight(
                response_schema=self.schema,
                blind_packet=self.packet,
                source_manifest=self.sources,
                evidence_ledger=ledger,
            )
        with self.assertRaisesRegex(preflight.PreflightError, "exact A/B"):
            preflight.evaluate_preflight(
                response_schema=self.schema,
                blind_packet=self.packet,
                source_manifest=self.sources,
                evidence_ledger=self.evidence_ledger(),
                coder_responses={"A": self.coder_a},
            )

    def test_checked_r1_artifact_is_exactly_reproducible(self) -> None:
        ledger = load(PREFLIGHT_LEDGER)
        expected = load(PREFLIGHT_REPORT)
        actual = preflight.evaluate_preflight(
            response_schema=self.schema,
            blind_packet=self.packet,
            source_manifest=self.sources,
            evidence_ledger=ledger,
            coder_responses={"A": self.coder_a, "B": self.coder_b},
        )
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
