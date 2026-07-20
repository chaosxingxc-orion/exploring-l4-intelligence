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


RULES = "wiki/survey/current/protocol.md"
STATE = "wiki/survey/current/status.md"
RULES_SECTION = "Rules Section"
STATE_SECTION = "Current State"


def blob(number: int) -> str:
    return f"{number:040x}"


def same_carrier_supersession(mode: str, target: str) -> dict:
    return {
        "mode": mode,
        "target": target,
        "target_current_carrier": STATE,
        "target_current_carrier_section": STATE_SECTION,
        "transfer_rule": "same-carrier-section",
    }


def fixture_documents() -> tuple[dict, dict, dict[str, bytes]]:
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
        "schema": "sf-campaign-audit-index-v2",
        "campaign": "system-first-stage1a",
        "current_carriers": {"rules": RULES, "state": STATE},
        "rounds": [
            {
                "round": 1,
                "verdict": "WITHHOLD_STAGE1B",
                "disposition": "SUPERSEDED_BY_LATER_ROUND",
                "supersession": same_carrier_supersession(
                    "later-round-artifact", correction
                ),
                "current_carrier": STATE,
                "current_carrier_section": STATE_SECTION,
                "artifacts": [
                    {"path": proposal, "git_blob": blob(1), "type": "proposal"}
                ],
            },
            {
                "round": 2,
                "verdict": "PENDING_INDEPENDENT_REREVIEW",
                "disposition": "ACTIVE_REVIEW_TRANSACTION",
                "supersession": same_carrier_supersession(
                    "current-carrier", STATE
                ),
                "current_carrier": STATE,
                "current_carrier_section": STATE_SECTION,
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
    carriers = {
        RULES: b"# Protocol\n\n## Rules Section\n\n## Other Rules\n",
        STATE: b"# Current State\n\n## Other State\n",
    }
    return registry, contract, carriers


def baseline_for(contract: dict) -> tuple[int, str]:
    count = sum(len(row["artifacts"]) for row in contract["rounds"])
    return count, campaign.semantic_prefix_sha256(contract["rounds"], count)


def validate(
    registry: dict,
    contract: dict,
    carriers: dict[str, bytes],
    *,
    baseline_contract: dict | None = None,
) -> None:
    anchored = contract if baseline_contract is None else baseline_contract
    count, prefix = baseline_for(anchored)
    campaign.validate_contract(
        registry,
        contract,
        carriers,
        baseline_count=count,
        baseline_prefix_sha256=prefix,
    )


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

    def test_current_manifest_gate_hashes_the_semantic_anchor_and_contract_chain(self) -> None:
        specs = (*current_manifest.BASE_FILE_SPECS, *current_manifest._AUDIT_FILE_SPECS)
        roles = {spec.role for spec in specs}
        self.assertTrue(
            {
                "campaign_audit_semantic_anchor",
                "campaign_audit_index_checker",
                "campaign_audit_contract",
                "audit_artifact_registry",
                "campaign_audit_index",
            }.issubset(roles)
        )


class CampaignAuditIndexContractTests(unittest.TestCase):
    def test_exact_contract_renders_carrier_section_and_all_semantic_fields(self) -> None:
        registry, contract, carriers = fixture_documents()
        validate(registry, contract, carriers)
        rendered = campaign.render_index(contract).decode("utf-8")
        for round_entry in contract["rounds"]:
            self.assertIn(f"| {round_entry['round']} |", rendered)
            self.assertIn(round_entry["verdict"], rendered)
            self.assertIn(round_entry["disposition"], rendered)
            self.assertIn(round_entry["supersession"]["target"], rendered)
            self.assertIn(round_entry["current_carrier"], rendered)
            self.assertIn(round_entry["current_carrier_section"], rendered)
            for artifact in round_entry["artifacts"]:
                self.assertIn(artifact["path"], rendered)
                self.assertIn(artifact["git_blob"], rendered)
                self.assertIn(artifact["type"], rendered)

    def test_empty_or_missing_real_carrier_section_fails(self) -> None:
        registry, contract, carriers = fixture_documents()
        for section in ("", "Missing Section"):
            changed = copy.deepcopy(contract)
            changed["rounds"][1]["current_carrier_section"] = section
            changed["rounds"][1]["supersession"][
                "target_current_carrier_section"
            ] = section
            with self.subTest(section=section):
                with self.assertRaises(campaign.CampaignIndexError):
                    validate(
                        registry,
                        changed,
                        carriers,
                        baseline_contract=contract,
                    )

    def test_added_deleted_wrong_blob_or_duplicate_mapping_fails(self) -> None:
        registry, contract, carriers = fixture_documents()
        added = copy.deepcopy(registry)
        added["artifacts"].append(
            {
                "path": "wiki/2026-07-19-system-first-research-proposal-v3.md",
                "git_blob": blob(3),
            }
        )
        deleted = copy.deepcopy(registry)
        deleted["artifacts"].pop()
        wrong_blob = copy.deepcopy(registry)
        wrong_blob["artifacts"][-1]["git_blob"] = blob(8)
        duplicate_path = copy.deepcopy(contract)
        duplicate_path["rounds"][1]["artifacts"].append(
            copy.deepcopy(duplicate_path["rounds"][0]["artifacts"][0])
        )

        for changed_registry, changed_contract in (
            (added, contract),
            (deleted, contract),
            (wrong_blob, contract),
            (registry, duplicate_path),
        ):
            with self.subTest(changed=(changed_registry, changed_contract)):
                with self.assertRaises(campaign.CampaignIndexError):
                    validate(
                        changed_registry,
                        changed_contract,
                        carriers,
                        baseline_contract=contract,
                    )

    def test_duplicate_or_missing_round_fails(self) -> None:
        registry, contract, carriers = fixture_documents()
        duplicate_round = copy.deepcopy(contract)
        duplicate_round["rounds"].append(copy.deepcopy(duplicate_round["rounds"][1]))
        missing_round = copy.deepcopy(contract)
        missing_round["rounds"][1]["round"] = 3
        for changed in (duplicate_round, missing_round):
            with self.subTest(changed=changed):
                with self.assertRaises(campaign.CampaignIndexError):
                    validate(
                        registry, changed, carriers, baseline_contract=contract
                    )

    def test_fixed_prefix_rejects_allowed_semantic_reassignments_after_restamp(self) -> None:
        registry, contract, carriers = fixture_documents()
        mutations = {}

        carrier_swap = copy.deepcopy(contract)
        for row in carrier_swap["rounds"]:
            row["current_carrier"] = RULES
            row["current_carrier_section"] = RULES_SECTION
            row["supersession"]["target_current_carrier"] = RULES
            row["supersession"]["target_current_carrier_section"] = RULES_SECTION
            if row["supersession"]["mode"] == "current-carrier":
                row["supersession"]["target"] = RULES
        mutations["allowed-carrier-swap"] = carrier_swap

        round_swap = copy.deepcopy(contract)
        first_artifact = round_swap["rounds"][0]["artifacts"][0]
        second_artifact = round_swap["rounds"][1]["artifacts"][0]
        round_swap["rounds"][0]["artifacts"] = [second_artifact]
        round_swap["rounds"][1]["artifacts"] = [first_artifact]
        round_swap["rounds"][0]["supersession"]["target"] = first_artifact["path"]
        mutations["round-reassignment"] = round_swap

        type_swap = copy.deepcopy(contract)
        type_swap["rounds"][0]["artifacts"][0]["type"] = "review"
        mutations["type-reassignment"] = type_swap

        verdict_swap = copy.deepcopy(contract)
        verdict_swap["rounds"][0]["verdict"] = "STAGE1A_PROTOCOLIZATION_ONLY"
        mutations["verdict-reassignment"] = verdict_swap

        disposition_swap = copy.deepcopy(contract)
        disposition_swap["rounds"][0]["disposition"] = "HISTORICAL_COLD"
        disposition_swap["rounds"][0]["supersession"] = same_carrier_supersession(
            "current-carrier", STATE
        )
        mutations["disposition-reassignment"] = disposition_swap

        section_swap = copy.deepcopy(contract)
        for row in section_swap["rounds"]:
            row["current_carrier_section"] = "Other State"
            row["supersession"]["target_current_carrier_section"] = "Other State"
        mutations["section-swap"] = section_swap

        for label, changed in mutations.items():
            with self.subTest(label=label):
                campaign.render_index(changed)
                with self.assertRaisesRegex(
                    campaign.CampaignIndexError, "baseline prefix"
                ):
                    validate(
                        registry,
                        changed,
                        carriers,
                        baseline_contract=contract,
                    )

    def test_target_carrier_section_inconsistency_fails_even_with_recomputed_anchor(self) -> None:
        registry, contract, carriers = fixture_documents()
        contract["rounds"][1]["supersession"]["target_current_carrier"] = RULES
        contract["rounds"][1]["supersession"][
            "target_current_carrier_section"
        ] = RULES_SECTION
        with self.assertRaisesRegex(campaign.CampaignIndexError, "row carrier"):
            validate(registry, contract, carriers)

    def test_wrong_later_round_target_direction_fails(self) -> None:
        registry, contract, carriers = fixture_documents()
        contract["rounds"][0]["supersession"]["target"] = contract["rounds"][0][
            "artifacts"
        ][0]["path"]
        with self.assertRaisesRegex(campaign.CampaignIndexError, "later round"):
            validate(registry, contract, carriers)

    def test_legal_append_is_pure_new_round_and_preserves_frozen_prefix(self) -> None:
        registry, contract, carriers = fixture_documents()
        original_rounds = copy.deepcopy(contract["rounds"])
        count, prefix_sha256 = baseline_for(contract)
        correction = (
            "wiki/audit/system-first-stage1a/epoch-3/round-3/correction-3.md"
        )
        receipt = (
            "wiki/audit/system-first-stage1a/epoch-3/consolidation-receipt.json"
        )
        registry["artifacts"].extend(
            [
                {"path": correction, "git_blob": blob(3)},
                {"path": receipt, "git_blob": blob(4)},
            ]
        )
        contract["rounds"].append(
            {
                "round": 3,
                "verdict": "PENDING_INDEPENDENT_REREVIEW",
                "disposition": "ACTIVE_REVIEW_TRANSACTION",
                "supersession": same_carrier_supersession(
                    "current-carrier", STATE
                ),
                "current_carrier": STATE,
                "current_carrier_section": STATE_SECTION,
                "artifacts": [
                    {"path": correction, "git_blob": blob(3), "type": "correction"},
                    {"path": receipt, "git_blob": blob(4), "type": "receipt"},
                ],
            }
        )

        self.assertEqual(original_rounds, contract["rounds"][:2])
        campaign.validate_contract(
            registry,
            contract,
            carriers,
            baseline_count=count,
            baseline_prefix_sha256=prefix_sha256,
        )
        self.assertEqual(
            prefix_sha256,
            campaign.semantic_prefix_sha256(contract["rounds"], count),
        )

    def test_epoch_correction_and_receipt_are_campaign_artifacts_but_generators_are_not(self) -> None:
        correction = (
            "wiki/audit/system-first-stage1a/epoch-13/round-13/correction-13.md"
        )
        receipt = (
            "wiki/audit/system-first-stage1a/epoch-13/consolidation-receipt.json"
        )
        self.assertTrue(campaign.is_campaign_artifact(correction))
        self.assertTrue(campaign.is_campaign_artifact(receipt))
        self.assertFalse(
            campaign.is_campaign_artifact(
                "wiki/audit/system-first-stage1a/INDEX.md"
            )
        )
        self.assertFalse(
            campaign.is_campaign_artifact(
                "wiki/audit/system-first-stage1a/campaign-index.json"
            )
        )

    def test_registered_future_epoch_correction_or_receipt_missing_contract_fails(self) -> None:
        registry, contract, carriers = fixture_documents()
        future_paths = (
            "wiki/audit/system-first-stage1a/epoch-13/round-13/correction-13.md",
            "wiki/audit/system-first-stage1a/epoch-13/consolidation-receipt.json",
        )
        for number, path in enumerate(future_paths, 3):
            changed = copy.deepcopy(registry)
            changed["artifacts"].append({"path": path, "git_blob": blob(number)})
            with self.subTest(path=path):
                with self.assertRaisesRegex(
                    campaign.CampaignIndexError,
                    "registry/contract campaign paths differ",
                ):
                    validate(
                        changed,
                        contract,
                        carriers,
                        baseline_contract=contract,
                    )


if __name__ == "__main__":
    unittest.main()
