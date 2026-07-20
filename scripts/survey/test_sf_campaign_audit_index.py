from __future__ import annotations

import copy
import json
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
DISPOSITION_SEMANTICS = "immutable-at-issue; derived-current-by-event-order-and-type"
B8_CORRECTION = (
    "wiki/audit/system-first-stage1a/round-12/"
    "stage1a-readiness-correction.md"
)
ROUND13_REVIEW = {
    (
        "wiki/audit/system-first-stage1a/round-13/"
        "reviewer-proposal-design-stage1a-doctoral-review.md"
    ): "6018bc73748383daf4b593b987c2a4bb0ff826d6",
}


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
    correction = B8_CORRECTION
    registry = {
        "artifacts": [
            {"path": "wiki/unrelated-review.md", "git_blob": blob(9)},
            {"path": proposal, "git_blob": blob(1)},
            {"path": correction, "git_blob": blob(2)},
        ]
    }
    contract = {
        "schema": "sf-campaign-audit-index-v3",
        "campaign": "system-first-stage1a",
        "disposition_semantics": DISPOSITION_SEMANTICS,
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


def repath_active_event(registry: dict, contract: dict, path: str, active_type: str) -> None:
    old_path = contract["rounds"][-1]["artifacts"][0]["path"]
    registry_row = next(row for row in registry["artifacts"] if row["path"] == old_path)
    registry_row["path"] = path
    artifact = contract["rounds"][-1]["artifacts"][0]
    artifact["path"] = path
    artifact["type"] = active_type
    contract["rounds"][0]["supersession"]["target"] = path


def append_receipt_event(
    registry: dict,
    contract: dict,
    *,
    round_number: int,
    path: str = "wiki/audit/system-first-stage1a/epoch-3/consolidation-receipt.json",
) -> str:
    registry["artifacts"].append({"path": path, "git_blob": blob(round_number)})
    contract["rounds"].append(
        {
            "round": round_number,
            "verdict": "PENDING_INDEPENDENT_REREVIEW",
            "disposition": "NON_ACTIVE_PREREQUISITE",
            "supersession": same_carrier_supersession("current-carrier", STATE),
            "current_carrier": STATE,
            "current_carrier_section": STATE_SECTION,
            "artifacts": [
                {
                    "path": path,
                    "git_blob": blob(round_number),
                    "type": "consolidation-receipt",
                }
            ],
        }
    )
    return path


def append_correction_event(registry: dict, contract: dict, *, round_number: int) -> str:
    path = "wiki/audit/system-first-stage1a/epoch-3/round-3/correction-3.md"
    registry["artifacts"].append({"path": path, "git_blob": blob(round_number)})
    contract["rounds"].append(
        {
            "round": round_number,
            "verdict": "PENDING_INDEPENDENT_REREVIEW",
            "disposition": "ACTIVE_REVIEW_TRANSACTION",
            "supersession": same_carrier_supersession("current-carrier", STATE),
            "current_carrier": STATE,
            "current_carrier_section": STATE_SECTION,
            "artifacts": [
                {
                    "path": path,
                    "git_blob": blob(round_number),
                    "type": "correction",
                }
            ],
        }
    )
    return path


def append_amendment_event(registry: dict, contract: dict, *, round_number: int) -> str:
    path = "wiki/audit/system-first-stage1a/epoch-3/round-3/amendment-3.md"
    registry["artifacts"].append({"path": path, "git_blob": blob(round_number)})
    contract["rounds"].append(
        {
            "round": round_number,
            "verdict": "PENDING_INDEPENDENT_REREVIEW",
            "disposition": "ACTIVE_REVIEW_TRANSACTION",
            "supersession": same_carrier_supersession("current-carrier", STATE),
            "current_carrier": STATE,
            "current_carrier_section": STATE_SECTION,
            "artifacts": [
                {
                    "path": path,
                    "git_blob": blob(round_number),
                    "type": "amendment",
                }
            ],
        }
    )
    return path


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
    def test_round13_preserves_design_review(self) -> None:
        contract = json.loads(
            (REPO / "wiki/audit/system-first-stage1a/campaign-index.json")
            .read_text(encoding="utf-8")
        )
        registry = json.loads(
            (REPO / "wiki/survey/sf-audit-artifact-registry.json")
            .read_text(encoding="utf-8")
        )
        round13 = next(row for row in contract["rounds"] if row["round"] == 13)
        actual = {
            artifact["path"]: artifact["git_blob"]
            for artifact in round13["artifacts"]
        }
        self.assertEqual(ROUND13_REVIEW, actual)
        registry_pins = {
            artifact["path"]: artifact["git_blob"]
            for artifact in registry["artifacts"]
            if artifact["path"] in ROUND13_REVIEW
        }
        self.assertEqual(ROUND13_REVIEW, registry_pins)
        self.assertEqual("WITHHOLD_STAGE1B", round13["verdict"])
        self.assertEqual("HISTORICAL_COLD", round13["disposition"])

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
        self.assertIn("At-issue disposition", rendered)
        self.assertIn("Derived current", rendered)
        self.assertEqual(1, rendered.count("`CURRENT_ACTIVE`"))
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

    def test_empty_missing_or_duplicate_real_carrier_section_fails(self) -> None:
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
        duplicate = dict(carriers)
        duplicate[STATE] += b"\n## Current State\n"
        with self.assertRaisesRegex(campaign.CampaignIndexError, "exactly once"):
            validate(registry, contract, duplicate)

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

    def test_receipt_then_correction_are_two_anchor_commit_boundaries(self) -> None:
        registry, initial, carriers = fixture_documents()
        head_count, head_prefix = baseline_for(initial)

        receipt_registry = copy.deepcopy(registry)
        receipt_contract = copy.deepcopy(initial)
        append_receipt_event(receipt_registry, receipt_contract, round_number=3)
        receipt_count, receipt_prefix = baseline_for(receipt_contract)
        campaign.validate_contract(
            receipt_registry,
            receipt_contract,
            carriers,
            baseline_count=receipt_count,
            baseline_prefix_sha256=receipt_prefix,
        )
        current_manifest._validate_campaign_anchor_lineage(
            receipt_contract["rounds"],
            head_count,
            head_prefix,
            receipt_count,
            receipt_prefix,
        )
        self.assertEqual(2, campaign.derived_current_round(receipt_contract["rounds"]))

        correction_registry = copy.deepcopy(receipt_registry)
        correction_contract = copy.deepcopy(receipt_contract)
        append_correction_event(correction_registry, correction_contract, round_number=4)
        correction_count, correction_prefix = baseline_for(correction_contract)
        campaign.validate_contract(
            correction_registry,
            correction_contract,
            carriers,
            baseline_count=correction_count,
            baseline_prefix_sha256=correction_prefix,
        )
        current_manifest._validate_campaign_anchor_lineage(
            correction_contract["rounds"],
            receipt_count,
            receipt_prefix,
            correction_count,
            correction_prefix,
        )
        self.assertEqual(4, campaign.derived_current_round(correction_contract["rounds"]))
        rendered = campaign.render_index(correction_contract).decode("utf-8")
        self.assertEqual(1, rendered.count("`CURRENT_ACTIVE`"))
        self.assertIn("`FORMER_CURRENT`", rendered)

    def test_receipt_then_amendment_are_two_anchor_commit_boundaries(self) -> None:
        registry, initial, carriers = fixture_documents()
        head_count, head_prefix = baseline_for(initial)

        receipt_registry = copy.deepcopy(registry)
        receipt_contract = copy.deepcopy(initial)
        append_receipt_event(receipt_registry, receipt_contract, round_number=3)
        receipt_count, receipt_prefix = baseline_for(receipt_contract)
        campaign.validate_contract(
            receipt_registry,
            receipt_contract,
            carriers,
            baseline_count=receipt_count,
            baseline_prefix_sha256=receipt_prefix,
        )
        current_manifest._validate_campaign_anchor_lineage(
            receipt_contract["rounds"],
            head_count,
            head_prefix,
            receipt_count,
            receipt_prefix,
        )

        amendment_registry = copy.deepcopy(receipt_registry)
        amendment_contract = copy.deepcopy(receipt_contract)
        append_amendment_event(amendment_registry, amendment_contract, round_number=4)
        amendment_count, amendment_prefix = baseline_for(amendment_contract)
        campaign.validate_contract(
            amendment_registry,
            amendment_contract,
            carriers,
            baseline_count=amendment_count,
            baseline_prefix_sha256=amendment_prefix,
        )
        current_manifest._validate_campaign_anchor_lineage(
            amendment_contract["rounds"],
            receipt_count,
            receipt_prefix,
            amendment_count,
            amendment_prefix,
        )
        self.assertEqual(4, campaign.derived_current_round(amendment_contract["rounds"]))

    def test_receipt_and_active_event_cannot_share_one_anchor_transaction(self) -> None:
        for append_active in (append_amendment_event, append_correction_event):
            registry, initial, _carriers = fixture_documents()
            head_count, head_prefix = baseline_for(initial)
            append_receipt_event(registry, initial, round_number=3)
            append_active(registry, initial, round_number=4)
            staged_count, staged_prefix = baseline_for(initial)
            with self.subTest(active=append_active.__name__):
                with self.assertRaisesRegex(
                    current_manifest.CurrentManifestError,
                    "exactly one semantic event",
                ):
                    current_manifest._validate_campaign_anchor_lineage(
                        initial["rounds"],
                        head_count,
                        head_prefix,
                        staged_count,
                        staged_prefix,
                    )

    def test_anchor_growth_must_append_a_new_round_not_extend_prior_active(self) -> None:
        _registry, initial, _carriers = fixture_documents()
        head_count, head_prefix = baseline_for(initial)
        changed = copy.deepcopy(initial)
        changed["rounds"][-1]["artifacts"].append(
            {
                "path": (
                    "wiki/audit/system-first-stage1a/epoch-3/"
                    "consolidation-receipt.json"
                ),
                "git_blob": blob(3),
                "type": "consolidation-receipt",
            }
        )
        staged_count, staged_prefix = baseline_for(changed)
        with self.assertRaisesRegex(
            current_manifest.CurrentManifestError, "new round"
        ):
            current_manifest._validate_campaign_anchor_lineage(
                changed["rounds"],
                head_count,
                head_prefix,
                staged_count,
                staged_prefix,
            )

    def test_anchor_count_cannot_roll_back_from_head(self) -> None:
        _registry, initial, _carriers = fixture_documents()
        head_count, head_prefix = baseline_for(initial)
        staged_count = head_count - 1
        staged_prefix = campaign.semantic_prefix_sha256(
            initial["rounds"], staged_count
        )
        with self.assertRaisesRegex(
            current_manifest.CurrentManifestError, "count rollback"
        ):
            current_manifest._validate_campaign_anchor_lineage(
                initial["rounds"],
                head_count,
                head_prefix,
                staged_count,
                staged_prefix,
            )

    def test_committed_receipt_tail_cannot_be_restamped_or_left_unanchored(self) -> None:
        registry, initial, carriers = fixture_documents()
        receipt_registry = copy.deepcopy(registry)
        receipt_contract = copy.deepcopy(initial)
        append_receipt_event(receipt_registry, receipt_contract, round_number=3)
        head_count, head_prefix = baseline_for(receipt_contract)

        restamped = copy.deepcopy(receipt_contract)
        restamped["rounds"][-1]["verdict"] = "WITHHOLD_STAGE1B"
        staged_count, staged_prefix = baseline_for(restamped)
        with self.assertRaisesRegex(
            current_manifest.CurrentManifestError, "same-count anchor restamp"
        ):
            current_manifest._validate_campaign_anchor_lineage(
                restamped["rounds"],
                head_count,
                head_prefix,
                staged_count,
                staged_prefix,
            )

        unanchored_registry = copy.deepcopy(receipt_registry)
        unanchored_contract = copy.deepcopy(receipt_contract)
        append_correction_event(unanchored_registry, unanchored_contract, round_number=4)
        with self.assertRaisesRegex(
            current_manifest.CurrentManifestError, "unanchored semantic tail"
        ):
            current_manifest._validate_campaign_anchor_lineage(
                unanchored_contract["rounds"],
                head_count,
                head_prefix,
                head_count,
                head_prefix,
            )

    def test_epoch_path_shapes_enforce_each_type(self) -> None:
        cases = (
            (append_receipt_event, "amendment"),
            (append_amendment_event, "correction"),
            (append_correction_event, "amendment"),
        )
        for append_event, swapped_type in cases:
            registry, contract, carriers = fixture_documents()
            append_event(registry, contract, round_number=3)
            contract["rounds"][-1]["artifacts"][0]["type"] = swapped_type
            with self.subTest(event=append_event.__name__, type=swapped_type):
                with self.assertRaisesRegex(campaign.CampaignIndexError, "path/type"):
                    validate(registry, contract, carriers)

    def test_active_types_reject_ordinary_round_and_opaque_paths(self) -> None:
        cases = (
            (
                "amendment",
                "wiki/audit/system-first-stage1a/round-13/review-note.md",
            ),
            (
                "correction",
                "wiki/audit/system-first-stage1a/round-13/correction.md",
            ),
        )
        for active_type, path in cases:
            registry, contract, carriers = fixture_documents()
            repath_active_event(registry, contract, path, active_type)
            with self.subTest(type=active_type, path=path):
                with self.assertRaisesRegex(campaign.CampaignIndexError, "path/type"):
                    validate(registry, contract, carriers)

    def test_post_baseline_non_active_types_reject_opaque_paths(self) -> None:
        for active_type, basename in (
            ("amendment", "artifact-a.md"),
            ("correction", "artifact-b.md"),
        ):
            registry, contract, carriers = fixture_documents()
            baseline_count, baseline_prefix = baseline_for(contract)
            path = f"wiki/audit/system-first-stage1a/round-3/{basename}"
            registry["artifacts"].append({"path": path, "git_blob": blob(3)})
            contract["rounds"].append(
                {
                    "round": 3,
                    "verdict": "PENDING_INDEPENDENT_REREVIEW",
                    "disposition": "HISTORICAL_COLD",
                    "supersession": same_carrier_supersession(
                        "current-carrier", STATE
                    ),
                    "current_carrier": STATE,
                    "current_carrier_section": STATE_SECTION,
                    "artifacts": [
                        {
                            "path": path,
                            "git_blob": blob(3),
                            "type": active_type,
                        }
                    ],
                }
            )
            with self.subTest(type=active_type, path=path):
                with self.assertRaisesRegex(campaign.CampaignIndexError, "path/type"):
                    campaign.validate_contract(
                        registry,
                        contract,
                        carriers,
                        baseline_count=baseline_count,
                        baseline_prefix_sha256=baseline_prefix,
                    )

    def test_receipt_type_requires_the_exact_epoch_receipt_shape(self) -> None:
        registry, contract, carriers = fixture_documents()
        baseline_count, baseline_prefix = baseline_for(contract)
        append_receipt_event(registry, contract, round_number=3)
        campaign.validate_contract(
            registry,
            contract,
            carriers,
            baseline_count=baseline_count,
            baseline_prefix_sha256=baseline_prefix,
        )

        invalid_paths = (
            "wiki/audit/system-first-stage1a/round-3/receipt.json",
            (
                "wiki/audit/system-first-stage1a/epoch-3/"
                "consolidation-receipt-v2.json"
            ),
        )
        for path in invalid_paths:
            registry, contract, carriers = fixture_documents()
            baseline_count, baseline_prefix = baseline_for(contract)
            append_receipt_event(
                registry,
                contract,
                round_number=3,
                path=path,
            )
            with self.subTest(path=path):
                with self.assertRaisesRegex(campaign.CampaignIndexError, "path/type"):
                    campaign.validate_contract(
                        registry,
                        contract,
                        carriers,
                        baseline_count=baseline_count,
                        baseline_prefix_sha256=baseline_prefix,
                    )

    def test_exact_b8_correction_is_the_only_non_epoch_active_exception(self) -> None:
        registry, contract, carriers = fixture_documents()
        self.assertEqual(B8_CORRECTION, contract["rounds"][-1]["artifacts"][0]["path"])
        validate(registry, contract, carriers)

        near_b8 = B8_CORRECTION.removesuffix(".md") + "-v2.md"
        repath_active_event(registry, contract, near_b8, "correction")
        with self.assertRaisesRegex(campaign.CampaignIndexError, "path/type"):
            validate(registry, contract, carriers)

    def test_epoch_active_events_require_an_earlier_same_epoch_receipt(self) -> None:
        for append_active in (append_amendment_event, append_correction_event):
            registry, contract, carriers = fixture_documents()
            append_active(registry, contract, round_number=3)
            with self.subTest(active=append_active.__name__, receipt="missing"):
                with self.assertRaisesRegex(
                    campaign.CampaignIndexError, "receipt prerequisite"
                ):
                    validate(registry, contract, carriers)

            registry, contract, carriers = fixture_documents()
            append_receipt_event(registry, contract, round_number=3)
            active_path = append_active(registry, contract, round_number=4)
            wrong_epoch_path = active_path.replace("epoch-3/", "epoch-4/")
            registry["artifacts"][-1]["path"] = wrong_epoch_path
            contract["rounds"][-1]["artifacts"][0]["path"] = wrong_epoch_path
            with self.subTest(active=append_active.__name__, receipt="wrong-epoch"):
                with self.assertRaisesRegex(
                    campaign.CampaignIndexError, "receipt prerequisite"
                ):
                    validate(registry, contract, carriers)

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
