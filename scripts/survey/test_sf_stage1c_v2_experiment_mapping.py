from __future__ import annotations

import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch


REPO = Path(__file__).resolve().parents[2]
SURVEY_SCRIPTS = REPO / "scripts" / "survey"
if str(SURVEY_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SURVEY_SCRIPTS))

import sf_stage1c_v2_experiment_mapping as stage1c_v2  # noqa: E402


CONTRACT = (
    REPO
    / "wiki"
    / "survey"
    / "workbench"
    / "system-first-stage1c-v2"
    / "experiment-mapping-contract-v2.json"
)
BOOTSTRAP = (
    REPO
    / "wiki"
    / "survey"
    / "workbench"
    / "system-first-stage1c-v2"
    / "paper-audit-bootstrap-v2.json"
)
PROTOCOL = (
    REPO
    / "wiki"
    / "survey"
    / "workbench"
    / "system-first-stage1c-v2"
    / "protocol-v2.md"
)
REVIEW_REQUEST = (
    REPO
    / "wiki"
    / "survey"
    / "workbench"
    / "system-first-stage1c-v2"
    / "package-guide.md"
)
REVIEW_MANIFEST = (
    REPO
    / "wiki"
    / "survey"
    / "workbench"
    / "system-first-stage1c-v2"
    / "review-package-manifest.json"
)
CURRENT_STATUS = REPO / "wiki" / "survey" / "current" / "status.md"
HOT_STATE = REPO / "wiki" / "Research-Objective.md"


def _cell(**overrides: object) -> dict:
    cell = {
        "paper_work_id": "arxiv:2600.00001",
        "dataset": {
            "canonical_name": "example-bench",
            "revision": "abc123",
            "split": "test",
        },
        "core": {
            "model_id": "frozen-omni",
            "revision": "v1",
            "access_protocol": "API_ONLY",
        },
        "input_condition": "RAW_AUDIO",
        "intervention": "ADAPTIVE_STOP",
        "budget_horizon": "MAX_CALLS_8",
        "observations": [
            {
                "metric": "accuracy",
                "baseline_value": 0.5,
                "method_value": 0.6,
                "within_cell_delta": 0.1,
            },
            {
                "metric": "calls",
                "baseline_value": 8,
                "method_value": 5,
                "within_cell_delta": -3,
            },
        ],
    }
    cell.update(overrides)
    return cell


class Stage1CV2ExperimentMappingTests(unittest.TestCase):
    """User journeys for the pre-sign Stage-1C v2 contract.

    As a researcher, I can inventory every frozen Stage-1B paper without
    pretending that experiment-level recoding has already occurred.
    As a coder, I get stable experiment, family, dataset-edge and branch rules.
    As an independent reviewer, I can verify the proposed authority boundary.
    As a gatekeeper, I cannot activate CURRENT before the requested signature.
    """

    def test_frozen_registry_has_exactly_226_unique_records(self) -> None:
        records = stage1c_v2.load_registry_records()
        ids = [row["canonical_id"] for row in records]
        self.assertEqual(226, len(ids))
        self.assertEqual(226, len(set(ids)))

    def test_pre_sign_bootstrap_covers_registry_without_false_cells(self) -> None:
        records = stage1c_v2.load_registry_records()
        package = stage1c_v2.build_pre_sign_bootstrap(records)

        stage1c_v2.validate_pre_sign_bootstrap(package, records)
        rows = package["paper_audit_bootstrap"]
        self.assertEqual(226, package["paper_census"]["unique_records"])
        self.assertEqual(226, len(rows))
        self.assertEqual(
            {"AWAITING_AUTHORIZED_EXPERIMENT_RECODE"},
            {row["pre_sign_disposition"] for row in rows},
        )
        self.assertTrue(all(row["experiment_cell_ids"] == [] for row in rows))
        self.assertTrue(
            all(row["adjudication_status"] == "NOT_STARTED" for row in rows)
        )

    def test_committed_bootstrap_is_reproducible(self) -> None:
        expected = stage1c_v2.build_pre_sign_bootstrap(
            stage1c_v2.load_registry_records()
        )
        actual = json.loads(BOOTSTRAP.read_text(encoding="utf-8"))
        self.assertEqual(expected, actual)

    def test_contract_exposes_exact_controlled_vocabularies(self) -> None:
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        self.assertEqual(
            stage1c_v2.DATASET_LINEAGE_TYPES,
            set(contract["controlled_vocabularies"]["dataset_lineage"]),
        )
        self.assertEqual(
            stage1c_v2.DATASET_RELATION_TYPES,
            set(contract["controlled_vocabularies"]["dataset_relation"]),
        )
        self.assertEqual(
            stage1c_v2.FAMILY_MEMBERSHIP_TYPES,
            set(contract["controlled_vocabularies"]["family_membership"]),
        )
        self.assertEqual(
            stage1c_v2.FAMILY_EVIDENCE_STATES,
            set(contract["controlled_vocabularies"]["family_evidence_state"]),
        )
        self.assertEqual(
            stage1c_v2.LOCAL_READINESS_STATES,
            set(contract["controlled_vocabularies"]["local_readiness"]),
        )

    def test_cell_identity_uses_run_configuration_not_metrics(self) -> None:
        first = _cell()
        second = _cell(
            observations=[
                {
                    "metric": "harm",
                    "baseline_value": 0.2,
                    "method_value": 0.1,
                    "within_cell_delta": -0.1,
                }
            ]
        )
        changed_run = _cell(budget_horizon="MAX_CALLS_16")

        self.assertEqual(
            stage1c_v2.experiment_cell_id(first),
            stage1c_v2.experiment_cell_id(second),
        )
        self.assertNotEqual(
            stage1c_v2.experiment_cell_id(first),
            stage1c_v2.experiment_cell_id(changed_run),
        )

    def test_comparability_key_is_metric_and_run_exact(self) -> None:
        cell = _cell()
        key = stage1c_v2.comparability_key(cell, cell["observations"][0])
        changed_metric = dict(cell["observations"][0], metric="wer")
        changed_budget = _cell(budget_horizon="MAX_CALLS_16")

        self.assertNotEqual(
            key,
            stage1c_v2.comparability_key(cell, changed_metric),
        )
        self.assertNotEqual(
            key,
            stage1c_v2.comparability_key(
                changed_budget, changed_budget["observations"][0]
            ),
        )

    def test_core_family_compatibility_ignores_dataset_but_not_problem(self) -> None:
        signature = {
            "problem_id": "proxy-guided-selection",
            "evaluation_object": "selected_answer",
            "outcome_semantics": "terminal_task_validity",
            "environment_mode": "STATIC_BATCH",
            "access_protocol": "API_ONLY",
            "comparison_interpretability": "BASELINE_TO_INTERVENTION",
        }
        different_dataset_same_contract = dict(signature)
        incompatible_problem = dict(signature, problem_id="interrupt-recovery")

        self.assertTrue(
            stage1c_v2.core_membership_compatible(
                signature, different_dataset_same_contract
            )
        )
        self.assertFalse(
            stage1c_v2.core_membership_compatible(signature, incompatible_problem)
        )

    def test_lineage_requires_provenance_and_relation_does_not_claim_lineage(self) -> None:
        valid_lineage = {
            "edge_type": "DERIVED_FROM",
            "source_dataset": "spoken-squad",
            "target_dataset": "squad",
            "source_locator": "paper p3 and dataset card",
            "evidence_mode": "SOURCE_REPORTED_TRACEABLE",
        }
        invalid_lineage = dict(valid_lineage, source_locator="")
        valid_relation = {
            "edge_type": "INDEPENDENT_SAME_TASK",
            "source_dataset": "minds14",
            "target_dataset": "slurp",
            "rationale": "Independent corpora share an intent-classification task.",
            "evidence_mode": "REVIEWER_INFERENCE",
        }

        self.assertEqual("lineage", stage1c_v2.validate_dataset_edge(valid_lineage))
        with self.assertRaises(stage1c_v2.ContractError):
            stage1c_v2.validate_dataset_edge(invalid_lineage)
        self.assertEqual("relation", stage1c_v2.validate_dataset_edge(valid_relation))

    def test_ready_branch_requires_five_gates_and_four_arm_contract(self) -> None:
        branch = {
            "local_readiness": "LOCAL_READY",
            "residual_hypothesis": "The proxy may corrupt adaptive stopping.",
            "nearest_prior": "DP-2603.09714",
            "outcome_contract": "terminal validity plus cost and harm",
            "strongest_falsifier": "A fixed rule dominates over the noise range.",
            "kill_criterion": "Kill if the fixed rule dominates validity and cost.",
            "arms": {
                "frozen_baseline": "single_call",
                "nearest_prior_reproduction": "mugen_consensus",
                "candidate_strategy": ["calibrated_adaptive_stop"],
                "oracle_upper_bound": "gold_validity_selector",
            },
        }
        self.assertEqual((True, []), stage1c_v2.branch_readiness(branch))

        missing_prior = dict(branch, nearest_prior="")
        ready, missing = stage1c_v2.branch_readiness(missing_prior)
        self.assertFalse(ready)
        self.assertIn("nearest_prior", missing)

        no_oracle_reason = dict(branch)
        no_oracle_reason["arms"] = dict(
            branch["arms"],
            oracle_upper_bound="",
            oracle_not_definable_reason="No terminal oracle exists.",
        )
        self.assertEqual((True, []), stage1c_v2.branch_readiness(no_oracle_reason))

    def test_pre_sign_artifacts_request_but_do_not_self_grant_authority(self) -> None:
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        self.assertEqual(
            "AWAITING_INDEPENDENT_SIGNATURE", contract["authority"]["state"]
        )
        self.assertEqual(
            "SIGN_STAGE1C_V2_EXPERIMENT_MAPPING",
            contract["authority"]["requested_verdict"],
        )
        self.assertIn(
            "CURRENT_ACTIVATION", contract["authority"]["withheld_before_signature"]
        )
        self.assertIn("does not self-grant", PROTOCOL.read_text(encoding="utf-8"))
        self.assertIn(
            "SIGN_STAGE1C_V2_EXPERIMENT_MAPPING",
            REVIEW_REQUEST.read_text(encoding="utf-8"),
        )

        for current_path in (CURRENT_STATUS, HOT_STATE):
            self.assertNotIn(
                "SIGN_STAGE1C_V2_EXPERIMENT_MAPPING",
                current_path.read_text(encoding="utf-8"),
            )

    def test_contract_and_persisted_package_pass_executable_validation(self) -> None:
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        stage1c_v2.validate_contract_artifact(contract)
        package, report = stage1c_v2.verify_persisted()
        self.assertEqual(226, package["paper_census"]["unique_records"])
        self.assertEqual("PASS_PRE_SIGN_CONTRACT_ONLY", report["status"])

    def test_registry_loader_fails_closed_without_four_shards(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(stage1c_v2.ContractError):
                stage1c_v2.registry_shards(Path(directory))

    def test_identity_and_comparison_contracts_reject_missing_fields(self) -> None:
        with self.assertRaises(stage1c_v2.ContractError):
            stage1c_v2.experiment_cell_id({"paper_work_id": "arxiv:x"})
        with self.assertRaises(stage1c_v2.ContractError):
            stage1c_v2.comparability_key(_cell(), {"metric": ""})
        with self.assertRaises(stage1c_v2.ContractError):
            stage1c_v2.core_membership_compatible(
                {"problem_id": "x"}, {"problem_id": "x"}
            )

    def test_dataset_edge_contract_rejects_missing_and_unknown_relations(self) -> None:
        with self.assertRaises(stage1c_v2.ContractError):
            stage1c_v2.validate_dataset_edge({"edge_type": "DERIVED_FROM"})
        with self.assertRaises(stage1c_v2.ContractError):
            stage1c_v2.validate_dataset_edge(
                {
                    "edge_type": "INDEPENDENT_SAME_TASK",
                    "source_dataset": "a",
                    "target_dataset": "b",
                    "evidence_mode": "REVIEWER_INFERENCE",
                    "rationale": "",
                }
            )
        with self.assertRaises(stage1c_v2.ContractError):
            stage1c_v2.validate_dataset_edge(
                {
                    "edge_type": "SEMANTICALLY_RELATED",
                    "source_dataset": "a",
                    "target_dataset": "b",
                    "evidence_mode": "REVIEWER_INFERENCE",
                }
            )

    def test_branch_readiness_reports_all_missing_contract_parts(self) -> None:
        ready, missing = stage1c_v2.branch_readiness({})
        self.assertFalse(ready)
        self.assertIn("local_readiness", missing)
        self.assertIn("residual_hypothesis", missing)
        self.assertIn("arms", missing)

        ready, missing = stage1c_v2.branch_readiness(
            {
                "local_readiness": "LOCAL_READY",
                "residual_hypothesis": "x",
                "nearest_prior": "x",
                "outcome_contract": "x",
                "strongest_falsifier": "x",
                "kill_criterion": "x",
                "arms": {
                    "frozen_baseline": "",
                    "nearest_prior_reproduction": "",
                    "candidate_strategy": [],
                    "oracle_upper_bound": "",
                },
            }
        )
        self.assertFalse(ready)
        self.assertIn("arms.frozen_baseline", missing)
        self.assertIn("arms.nearest_prior_reproduction", missing)
        self.assertIn("arms.candidate_strategy", missing)
        self.assertIn("arms.oracle_upper_bound_or_reason", missing)

    def test_bootstrap_builder_rejects_duplicate_source_records(self) -> None:
        records = stage1c_v2.load_registry_records()
        with self.assertRaises(stage1c_v2.ContractError):
            stage1c_v2.build_pre_sign_bootstrap([records[0], records[0]])

    def test_bootstrap_validator_rejects_authority_and_claim_drift(self) -> None:
        records = stage1c_v2.load_registry_records()
        package = stage1c_v2.build_pre_sign_bootstrap(records)

        wrong_schema = dict(package, schema="wrong")
        with self.assertRaises(stage1c_v2.ContractError):
            stage1c_v2.validate_pre_sign_bootstrap(wrong_schema, records)

        wrong_authority = json.loads(json.dumps(package))
        wrong_authority["authority"]["state"] = "SIGNED"
        with self.assertRaises(stage1c_v2.ContractError):
            stage1c_v2.validate_pre_sign_bootstrap(wrong_authority, records)

        wrong_verdict = json.loads(json.dumps(package))
        wrong_verdict["authority"]["requested_verdict"] = "SIGN_SOMETHING_ELSE"
        with self.assertRaises(stage1c_v2.ContractError):
            stage1c_v2.validate_pre_sign_bootstrap(wrong_verdict, records)

        claimed_cell = json.loads(json.dumps(package))
        claimed_cell["paper_audit_bootstrap"][0]["experiment_cell_ids"] = ["EC-fake"]
        with self.assertRaises(stage1c_v2.ContractError):
            stage1c_v2.validate_pre_sign_bootstrap(claimed_cell, records)

        claimed_adjudication = json.loads(json.dumps(package))
        claimed_adjudication["paper_audit_bootstrap"][0][
            "adjudication_status"
        ] = "COMPLETE"
        with self.assertRaises(stage1c_v2.ContractError):
            stage1c_v2.validate_pre_sign_bootstrap(claimed_adjudication, records)

    def test_bootstrap_validator_rejects_duplicate_and_missing_papers(self) -> None:
        records = stage1c_v2.load_registry_records()
        package = stage1c_v2.build_pre_sign_bootstrap(records)

        duplicate = json.loads(json.dumps(package))
        duplicate["paper_audit_bootstrap"][1]["paper_work_id"] = duplicate[
            "paper_audit_bootstrap"
        ][0]["paper_work_id"]
        with self.assertRaises(stage1c_v2.ContractError):
            stage1c_v2.validate_pre_sign_bootstrap(duplicate, records)

        missing = json.loads(json.dumps(package))
        missing["paper_audit_bootstrap"].pop()
        with self.assertRaises(stage1c_v2.ContractError):
            stage1c_v2.validate_pre_sign_bootstrap(missing, records)

        wrong_disposition = json.loads(json.dumps(package))
        wrong_disposition["paper_audit_bootstrap"][0][
            "pre_sign_disposition"
        ] = "CODED"
        with self.assertRaises(stage1c_v2.ContractError):
            stage1c_v2.validate_pre_sign_bootstrap(wrong_disposition, records)

    def test_contract_validator_rejects_authority_and_vocabulary_drift(self) -> None:
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

        wrong_schema = dict(contract, schema="wrong")
        with self.assertRaises(stage1c_v2.ContractError):
            stage1c_v2.validate_contract_artifact(wrong_schema)

        wrong_authority = json.loads(json.dumps(contract))
        wrong_authority["authority"]["state"] = "SIGNED"
        with self.assertRaises(stage1c_v2.ContractError):
            stage1c_v2.validate_contract_artifact(wrong_authority)

        wrong_verdict = json.loads(json.dumps(contract))
        wrong_verdict["authority"]["requested_verdict"] = "OTHER"
        with self.assertRaises(stage1c_v2.ContractError):
            stage1c_v2.validate_contract_artifact(wrong_verdict)

        no_current_hold = json.loads(json.dumps(contract))
        no_current_hold["authority"]["withheld_before_signature"].remove(
            "CURRENT_ACTIVATION"
        )
        with self.assertRaises(stage1c_v2.ContractError):
            stage1c_v2.validate_contract_artifact(no_current_hold)

        vocabulary_drift = json.loads(json.dumps(contract))
        vocabulary_drift["controlled_vocabularies"]["dataset_lineage"].append(
            "SEMANTICALLY_RELATED"
        )
        with self.assertRaises(stage1c_v2.ContractError):
            stage1c_v2.validate_contract_artifact(vocabulary_drift)

    def test_cli_writes_report_without_authority_effect(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            report_path = Path(directory) / "report.json"
            stdout = StringIO()
            with redirect_stdout(stdout):
                result = stage1c_v2.main(["--report", str(report_path)])
            self.assertEqual(0, result)
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual("NONE", report["authority_effect"])
            self.assertEqual(0, report["checks"]["model_or_metric_execution"])
            self.assertIn("PASS_PRE_SIGN_CONTRACT_ONLY", stdout.getvalue())

    def test_cli_fails_closed_when_contract_is_missing(self) -> None:
        stderr = StringIO()
        with tempfile.TemporaryDirectory() as directory:
            missing_contract = Path(directory) / "missing.json"
            with patch.object(stage1c_v2, "CONTRACT_PATH", missing_contract):
                with redirect_stderr(stderr):
                    result = stage1c_v2.main([])
        self.assertEqual(1, result)
        self.assertIn("FAIL:", stderr.getvalue())

    def test_review_manifest_binds_exact_pre_sign_objects_only(self) -> None:
        expected = stage1c_v2.build_review_manifest()
        actual = json.loads(REVIEW_MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(expected, actual)
        self.assertEqual("NONE", actual["authority_effect"])
        paths = {row["path"] for row in actual["artifacts"]}
        self.assertIn(
            "wiki/survey/workbench/system-first-stage1c-v2/protocol-v2.md", paths
        )
        self.assertIn(
            "docs/checks/stage1c-v2/pre-sign-2026-07-23/contract-report.json",
            paths,
        )
        self.assertFalse(any("wiki/survey/current/" in path for path in paths))
        self.assertFalse(any("wiki/Research-Objective.md" in path for path in paths))


if __name__ == "__main__":
    unittest.main()
