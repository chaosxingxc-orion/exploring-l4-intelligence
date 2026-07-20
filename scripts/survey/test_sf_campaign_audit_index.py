from __future__ import annotations

import copy
import subprocess
import sys
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts" / "survey" / "sf_campaign_audit_index.py"
SURVEY_DIR = SCRIPT.parent
if str(SURVEY_DIR) not in sys.path:
    sys.path.insert(0, str(SURVEY_DIR))

import sf_campaign_audit_index as campaign
import sf_current_manifest as current_manifest


def blob(number: int) -> str:
    return f"{number:040x}"


def fixture_documents() -> tuple[dict, dict]:
    proposal = "wiki/2026-07-15-system-first-research-proposal-v1.md"
    correction = "wiki/audit/system-first-stage1a/round-2/correction.md"
    registry = {
        "artifacts": [
            {"path": "wiki/unrelated-review.md", "git_blob": blob(9)},
            {"path": proposal, "git_blob": blob(1)},
            {"path": correction, "git_blob": blob(2)},
        ]
    }
    contract = {
        "schema": "sf-campaign-audit-index-v1",
        "campaign": "system-first-stage1a",
        "current_carriers": {
            "rules": "wiki/survey/current/protocol.md",
            "state": "wiki/survey/current/status.md",
        },
        "rounds": [
            {
                "round": 1,
                "verdict": "WITHHOLD_STAGE1B",
                "disposition": "SUPERSEDED_BY_LATER_ROUND",
                "supersession": {
                    "mode": "later-round-artifact",
                    "target": correction,
                },
                "current_carrier": "wiki/survey/current/protocol.md",
                "artifacts": [
                    {"path": proposal, "git_blob": blob(1), "type": "proposal"}
                ],
            },
            {
                "round": 2,
                "verdict": "PENDING_INDEPENDENT_REREVIEW",
                "disposition": "ACTIVE_REVIEW_TRANSACTION",
                "supersession": {
                    "mode": "current-carrier",
                    "target": "wiki/survey/current/protocol.md",
                },
                "current_carrier": "wiki/survey/current/status.md",
                "artifacts": [
                    {
                        "path": correction,
                        "git_blob": blob(2),
                        "type": "correction",
                    }
                ],
            },
        ],
    }
    return registry, contract


class CampaignAuditIndexRepositoryTests(unittest.TestCase):
    def test_repository_contract_and_generated_index_agree(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), "--check"],
            cwd=REPO,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        self.assertEqual(0, completed.returncode, completed.stderr or completed.stdout)

    def test_current_manifest_gate_hashes_the_checker_contract_registry_and_index(self) -> None:
        specs = (*current_manifest.BASE_FILE_SPECS, *current_manifest._AUDIT_FILE_SPECS)
        roles = {spec.role for spec in specs}
        self.assertTrue(
            {
                "campaign_audit_index_checker",
                "campaign_audit_contract",
                "audit_artifact_registry",
                "campaign_audit_index",
            }.issubset(roles)
        )


class CampaignAuditIndexContractTests(unittest.TestCase):
    def test_exact_contract_renders_every_campaign_binding_and_semantic_field(self) -> None:
        registry, contract = fixture_documents()
        campaign.validate_contract(registry, contract)
        rendered = campaign.render_index(contract).decode("utf-8")
        for round_entry in contract["rounds"]:
            self.assertIn(f"| {round_entry['round']} |", rendered)
            self.assertIn(round_entry["verdict"], rendered)
            self.assertIn(round_entry["disposition"], rendered)
            self.assertIn(round_entry["supersession"]["target"], rendered)
            self.assertIn(round_entry["current_carrier"], rendered)
            for artifact in round_entry["artifacts"]:
                self.assertIn(artifact["path"], rendered)
                self.assertIn(artifact["git_blob"], rendered)
                self.assertIn(artifact["type"], rendered)

    def test_added_deleted_or_wrong_blob_campaign_item_fails(self) -> None:
        registry, contract = fixture_documents()
        cases = []

        added = copy.deepcopy(registry)
        added["artifacts"].append(
            {
                "path": "wiki/2026-07-19-system-first-research-proposal-v3.md",
                "git_blob": blob(3),
            }
        )
        cases.append(added)

        deleted = copy.deepcopy(registry)
        deleted["artifacts"].pop()
        cases.append(deleted)

        wrong_blob = copy.deepcopy(registry)
        wrong_blob["artifacts"][-1]["git_blob"] = blob(8)
        cases.append(wrong_blob)

        for changed in cases:
            with self.subTest(changed=changed):
                with self.assertRaises(campaign.CampaignIndexError):
                    campaign.validate_contract(changed, contract)

    def test_duplicate_path_duplicate_round_and_missing_round_fail(self) -> None:
        registry, contract = fixture_documents()

        duplicate_path = copy.deepcopy(contract)
        duplicate_path["rounds"][1]["artifacts"].append(
            copy.deepcopy(duplicate_path["rounds"][0]["artifacts"][0])
        )
        duplicate_round = copy.deepcopy(contract)
        duplicate_round["rounds"].append(copy.deepcopy(duplicate_round["rounds"][1]))
        missing_round = copy.deepcopy(contract)
        missing_round["rounds"][1]["round"] = 3

        for changed in (duplicate_path, duplicate_round, missing_round):
            with self.subTest(changed=changed):
                with self.assertRaises(campaign.CampaignIndexError):
                    campaign.validate_contract(registry, changed)

    def test_wrong_supersession_direction_fails(self) -> None:
        registry, contract = fixture_documents()
        contract["rounds"][0]["supersession"]["target"] = contract["rounds"][0][
            "artifacts"
        ][0]["path"]
        with self.assertRaisesRegex(campaign.CampaignIndexError, "later round"):
            campaign.validate_contract(registry, contract)

    def test_legal_append_and_generated_index_restamp_passes(self) -> None:
        registry, contract = fixture_documents()
        before = campaign.render_index(contract)
        new_path = "wiki/audit/system-first-stage1a/round-3/correction.md"
        registry["artifacts"].append({"path": new_path, "git_blob": blob(3)})
        contract["rounds"][1].update(
            {
                "disposition": "SUPERSEDED_BY_LATER_ROUND",
                "supersession": {
                    "mode": "later-round-artifact",
                    "target": new_path,
                },
            }
        )
        contract["rounds"].append(
            {
                "round": 3,
                "verdict": "PENDING_INDEPENDENT_REREVIEW",
                "disposition": "ACTIVE_REVIEW_TRANSACTION",
                "supersession": {
                    "mode": "current-carrier",
                    "target": "wiki/survey/current/protocol.md",
                },
                "current_carrier": "wiki/survey/current/status.md",
                "artifacts": [
                    {"path": new_path, "git_blob": blob(3), "type": "correction"}
                ],
            }
        )

        campaign.validate_contract(registry, contract)
        after = campaign.render_index(contract)
        self.assertNotEqual(before, after)
        self.assertIn(new_path.encode("utf-8"), after)


if __name__ == "__main__":
    unittest.main()
