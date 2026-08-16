"""Contract tests for semantic study repositories and experiment assets."""

from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import subprocess
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).with_name("study_workspace_check.py")
SPEC = importlib.util.spec_from_file_location("study_workspace_check", SCRIPT)
assert SPEC and SPEC.loader
study_workspace = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(study_workspace)


class StudyWorkspaceContractTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / "studies").mkdir()
        (self.root / "papers").mkdir()
        (self.root / "wiki").mkdir()
        (self.root / "docs" / "integrity").mkdir(parents=True)
        (self.root / ".gitignore").write_text("studies/*/\npapers/*/\n", encoding="utf-8")
        (self.root / "AGENTS.md").write_text("# AGENTS.md\nguide\n", encoding="utf-8")
        (self.root / "CLAUDE.md").write_text("# CLAUDE.md\nguide\n", encoding="utf-8")
        (self.root / "papers" / "registry.json").write_text(
            json.dumps(
                {
                    "schema": "paper-repository-registry-v1",
                    "local_root": "papers",
                    "repo_creation_gate": "OWNER_GO_AND_PAPER_EXECUTION_CONTRACT",
                    "candidate_id_policy": "AUDIT_ONLY_NEVER_ENGINEERING_IDENTITY",
                    "promotion_control_plane": "wiki/Experiment-Assets.md",
                    "papers": [],
                }
            ),
            encoding="utf-8",
        )
        self.write_control_plane(0)
        (self.root / "wiki" / "Research-Objective.md").write_text(
            "endpoint: speech-aware-evidence-acquisition in Stage-2A E0\n",
            encoding="utf-8",
        )
        self.registry = {
            "schema": "study-repository-registry-v2",
            "local_root": "studies",
            "repo_creation_gate": "OWNER_GO_AND_EXECUTION_CONTRACT",
            "candidate_id_policy": "AUDIT_ONLY_NEVER_ENGINEERING_IDENTITY",
            "experiment_control_plane": "wiki/Experiment-Assets.md",
            "studies": [],
        }
        self.write_registry()

    def write_control_plane(self, admitted_count: int) -> None:
        (self.root / "wiki" / "Experiment-Assets.md").write_text(
            f"Admitted study repositories: **{admitted_count}**.\n"
            "experiment_id\nstudy commit\nconfig hash\nprotocol hash\n"
            "model revision\ndataset revision\nMLflow run\nartifact location\n"
            "artifact hashes\nresult summary\nshared code revision\n"
            "split role\nsplit identity hash\nconsumed\ndeviations\ndecision\n",
            encoding="utf-8",
        )

    def write_registry(self) -> None:
        (self.root / "studies" / "registry.json").write_text(
            json.dumps(self.registry), encoding="utf-8"
        )
        self.write_control_plane(len(self.registry.get("studies", [])))

    @staticmethod
    def git_blob(raw: bytes) -> str:
        return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()

    def admitted_study(self) -> dict:
        slug = "speech-aware-evidence-acquisition"
        decision = self.root / "wiki" / "decisions" / "speech-aware.md"
        experiment_index = self.root / "wiki" / "experiments" / slug / "README.md"
        decision.parent.mkdir(parents=True, exist_ok=True)
        experiment_index.parent.mkdir(parents=True, exist_ok=True)
        decision.write_text("GO\n", encoding="utf-8")
        experiment_index.write_text(
            "---\n"
            f'study_slug: "{slug}"\n'
            f'study_repo: "https://github.com/example/{slug}.git"\n'
            f'local_checkout: "studies/{slug}"\n'
            'experiment_id_namespace: "SAEA-E-<nnn>"\n'
            "---\n\ncurrent experiments\n"
            "| experiment_id | date | split role | split identity hash | consumed |\n"
            "|---|---|---|---|---|\n",
            encoding="utf-8",
        )
        return {
            "name": "Speech-aware evidence acquisition",
            "slug": slug,
            "local_path": f"studies/{slug}",
            "github_repo": f"https://github.com/example/{slug}.git",
            "default_branch": "master",
            "package_name": slug,
            "created_at": "2026-08-03",
            "experiment_namespace": "SAEA-E",
            "lifecycle": "engineering",
            "decision_record": "wiki/decisions/speech-aware.md",
            "decision_record_blob": self.git_blob(b"GO\n"),
            "experiment_index": f"wiki/experiments/{slug}/README.md",
        }

    def init_git_checkout(self, path: Path, origin: str | None = None) -> None:
        path.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["git", "init", "--quiet", "--initial-branch=master", str(path)],
            check=True,
            capture_output=True,
        )
        if origin is not None:
            subprocess.run(
                ["git", "-C", str(path), "remote", "add", "origin", origin],
                check=True,
                capture_output=True,
            )

    def test_empty_registry_is_valid_before_any_direction_is_admitted(self) -> None:
        loaded = study_workspace.load_and_validate_registry(self.root)
        self.assertEqual([], loaded["studies"])

    def test_semantic_admitted_study_with_independent_git_is_valid(self) -> None:
        entry = self.admitted_study()
        self.init_git_checkout(self.root / entry["local_path"], origin=entry["github_repo"])
        self.registry["studies"] = [entry]
        self.write_registry()

        loaded = study_workspace.load_and_validate_registry(self.root)

        self.assertEqual(entry["slug"], loaded["studies"][0]["slug"])

    def test_fake_git_metadata_is_rejected(self) -> None:
        entry = self.admitted_study()
        checkout = self.root / entry["local_path"]
        checkout.mkdir(parents=True)
        (checkout / ".git").mkdir()
        self.registry["studies"] = [entry]
        self.write_registry()
        with self.assertRaises(study_workspace.StudyWorkspaceError):
            study_workspace.load_and_validate_registry(self.root)

    def test_require_installed_demands_checkout_origin_and_branch(self) -> None:
        entry = self.admitted_study()
        self.registry["studies"] = [entry]
        self.write_registry()

        study_workspace.load_and_validate_registry(self.root)
        with self.assertRaisesRegex(study_workspace.StudyWorkspaceError, "not installed"):
            study_workspace.load_and_validate_registry(self.root, require_installed=True)

        checkout = self.root / entry["local_path"]
        self.init_git_checkout(checkout, origin="https://github.com/example/wrong.git")
        with self.assertRaisesRegex(study_workspace.StudyWorkspaceError, "origin"):
            study_workspace.load_and_validate_registry(self.root, require_installed=True)

        subprocess.run(
            [
                "git",
                "-C",
                str(checkout),
                "remote",
                "set-url",
                "origin",
                entry["github_repo"],
            ],
            check=True,
            capture_output=True,
        )
        study_workspace.load_and_validate_registry(self.root, require_installed=True)

    def test_cross_source_truth_detects_count_and_frontmatter_drift(self) -> None:
        entry = self.admitted_study()
        self.init_git_checkout(self.root / entry["local_path"], origin=entry["github_repo"])
        self.registry["studies"] = [entry]
        self.write_registry()
        study_workspace.validate_cross_source_truth(self.root)

        self.write_control_plane(0)
        with self.assertRaisesRegex(study_workspace.StudyWorkspaceError, "admitted-count drift"):
            study_workspace.validate_cross_source_truth(self.root)

        self.write_control_plane(1)
        index = self.root / entry["experiment_index"]
        index.write_text(
            index.read_text(encoding="utf-8").replace("SAEA-E-<nnn>", "OTHER-1"),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(study_workspace.StudyWorkspaceError, "frontmatter drift"):
            study_workspace.validate_cross_source_truth(self.root)

        (self.root / "wiki" / "Research-Objective.md").write_text(
            "endpoint mentions nothing\n", encoding="utf-8"
        )
        with self.assertRaisesRegex(study_workspace.StudyWorkspaceError, "HOT endpoint"):
            study_workspace.validate_cross_source_truth(self.root)

    def test_ledger_header_only_mutation_is_rejected_despite_prose_terms(self) -> None:
        entry = self.admitted_study()
        self.init_git_checkout(self.root / entry["local_path"], origin=entry["github_repo"])
        self.registry["studies"] = [entry]
        self.write_registry()
        index = self.root / entry["experiment_index"]
        frontmatter = index.read_text(encoding="utf-8").split("---\n")[1]
        # Prose keeps all three terms; the header table loses them. Substring search
        # over the whole document would pass; header parsing must fail.
        index.write_text(
            "---\n" + frontmatter + "---\n\n"
            "Every record must carry a split role, a split identity hash, and a consumed mark.\n"
            "| experiment_id | date |\n|---|---|\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(
            study_workspace.StudyWorkspaceError, "exposure columns"
        ):
            study_workspace.validate_cross_source_truth(self.root)

    def test_experiment_index_without_any_ledger_header_is_rejected(self) -> None:
        entry = self.admitted_study()
        self.init_git_checkout(self.root / entry["local_path"], origin=entry["github_repo"])
        self.registry["studies"] = [entry]
        self.write_registry()
        index = self.root / entry["experiment_index"]
        frontmatter = index.read_text(encoding="utf-8").split("---\n")[1]
        index.write_text(
            "---\n" + frontmatter + "---\n\nno table at all\n", encoding="utf-8"
        )
        with self.assertRaisesRegex(
            study_workspace.StudyWorkspaceError, "ledger table header"
        ):
            study_workspace.validate_cross_source_truth(self.root)

    def test_stage_truth_forbids_stage2b_validation_language_on_default_surface(self) -> None:
        study_workspace.validate_stage_truth(self.root)
        (self.root / "CLAUDE.md").write_text(
            "# CLAUDE.md\ninnovation is validated in Stage-2B\n", encoding="utf-8"
        )
        with self.assertRaisesRegex(study_workspace.StudyWorkspaceError, "stage-truth drift"):
            study_workspace.validate_stage_truth(self.root)
        # Normalization covers both letter case and the non-breaking hyphen.
        (self.root / "CLAUDE.md").write_text(
            "# CLAUDE.md\nInnovation is VALIDATED IN STAGE‑2B.\n", encoding="utf-8"
        )
        with self.assertRaisesRegex(study_workspace.StudyWorkspaceError, "stage-truth drift"):
            study_workspace.validate_stage_truth(self.root)
        (self.root / "CLAUDE.md").write_text("# CLAUDE.md\nguide\n", encoding="utf-8")
        (self.root / "AGENTS.md").unlink()
        with self.assertRaisesRegex(study_workspace.StudyWorkspaceError, "stage-truth surface"):
            study_workspace.validate_stage_truth(self.root)

    def test_inventory_pins_paper_registry_hash_and_fails_without_it(self) -> None:
        (self.root / "docs" / "integrity" / "experiment_attempt_registry.jsonl").write_text(
            "", encoding="utf-8"
        )
        inventory = study_workspace.build_experiment_asset_inventory(
            self.root, history_lookup=lambda path: None, resolution_lookup={}
        )
        self.assertEqual(
            "papers/registry.json", inventory["paper_registry"]["path"]
        )
        self.assertEqual(64, len(inventory["paper_registry"]["sha256"]))

        (self.root / "papers" / "registry.json").unlink()
        with self.assertRaisesRegex(
            study_workspace.StudyWorkspaceError, "paper registry"
        ):
            study_workspace.build_experiment_asset_inventory(
                self.root, history_lookup=lambda path: None, resolution_lookup={}
            )

    def test_decision_record_blob_drift_is_rejected(self) -> None:
        entry = self.admitted_study()
        self.init_git_checkout(self.root / entry["local_path"], origin=entry["github_repo"])
        entry["decision_record_blob"] = self.git_blob(b"different\n")
        self.registry["studies"] = [entry]
        self.write_registry()
        with self.assertRaisesRegex(study_workspace.StudyWorkspaceError, "blob drift"):
            study_workspace.load_and_validate_registry(self.root)

    def test_candidate_number_and_candidate_lifecycle_are_rejected(self) -> None:
        for slug, lifecycle in (
            ("r2-external-retrieval", "engineering"),
            ("speech-aware-evidence-acquisition", "conditional-go"),
        ):
            with self.subTest(slug=slug, lifecycle=lifecycle):
                entry = self.admitted_study()
                entry.update(
                    {
                        "slug": slug,
                        "local_path": f"studies/{slug}",
                        "github_repo": f"https://github.com/example/{slug}.git",
                        "lifecycle": lifecycle,
                        "experiment_index": f"wiki/experiments/{slug}/README.md",
                    }
                )
                self.registry["studies"] = [entry]
                self.write_registry()
                with self.assertRaises(study_workspace.StudyWorkspaceError):
                    study_workspace.load_and_validate_registry(self.root)

    def test_unregistered_or_non_git_study_directory_is_rejected(self) -> None:
        unregistered = self.root / "studies" / "unregistered-study"
        unregistered.mkdir()
        with self.assertRaisesRegex(
            study_workspace.StudyWorkspaceError, "unregistered study directory"
        ):
            study_workspace.load_and_validate_registry(self.root)

        unregistered.rmdir()
        entry = self.admitted_study()
        (self.root / entry["local_path"]).mkdir(parents=True)
        self.registry["studies"] = [entry]
        self.write_registry()
        with self.assertRaisesRegex(
            study_workspace.StudyWorkspaceError, "independent Git repository"
        ):
            study_workspace.load_and_validate_registry(self.root)

    def test_duplicate_paths_and_missing_wiki_bindings_are_rejected(self) -> None:
        entry = self.admitted_study()
        duplicate = dict(entry, name="Duplicate")
        self.registry["studies"] = [entry, duplicate]
        self.write_registry()
        with self.assertRaises(study_workspace.StudyWorkspaceError):
            study_workspace.load_and_validate_registry(self.root)

        self.registry["studies"] = [entry]
        (self.root / entry["decision_record"]).unlink()
        self.write_registry()
        with self.assertRaisesRegex(study_workspace.StudyWorkspaceError, "decision_record"):
            study_workspace.load_and_validate_registry(self.root)

    def test_experiment_control_plane_requires_complete_asset_keys(self) -> None:
        study_workspace.validate_experiment_control_plane(self.root)
        (self.root / "wiki" / "Experiment-Assets.md").write_text(
            "experiment_id\nstudy commit\n", encoding="utf-8"
        )
        with self.assertRaisesRegex(
            study_workspace.StudyWorkspaceError, "experiment control plane"
        ):
            study_workspace.validate_experiment_control_plane(self.root)

    def test_legacy_inventory_reports_four_state_resolution(self) -> None:
        legacy = self.root / "docs" / "integrity" / "experiment_attempt_registry.jsonl"
        live = self.root / "projects" / "work" / "_repro" / "live.json"
        live.parent.mkdir(parents=True)
        live.write_text("{}\n", encoding="utf-8")
        rows = [
            {"path": "projects/work/_repro/live.json"},
            {"path": "projects/work/_repro/history.json"},
            {"path": "projects/work/_repro/cold.json"},
            {"path": "projects/work/_repro/waived.json"},
            {"path": "other/missing.json"},
        ]
        legacy.write_text(
            "".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8"
        )
        resolution = {
            "projects/work/_repro/cold.json": {
                "path": "projects/work/_repro/cold.json",
                "state": "COLD_BACKUP_RESOLVED",
            },
            "projects/work/_repro/waived.json": {
                "path": "projects/work/_repro/waived.json",
                "state": "UNRESOLVED",
                "waiver": {
                    "waived_by": "owner",
                    "waived_on": "2026-08-03",
                    "reason": "test",
                },
            },
        }

        inventory = study_workspace.build_experiment_asset_inventory(
            self.root,
            history_lookup=lambda path: "abc123" if path.endswith("history.json") else None,
            resolution_lookup=resolution,
        )

        summary = inventory["legacy_experiment_attempts"]
        self.assertEqual(5, summary["recorded_entries"])
        self.assertEqual(1, summary["worktree_present"])
        self.assertEqual(1, summary["local_git_history"])
        self.assertEqual(1, summary["cold_backup_resolved"])
        self.assertEqual(1, summary["waived_unresolved"])
        self.assertEqual(1, summary["unresolved"])
        self.assertEqual(["other/missing.json"], summary["unresolved_assets"])

    def test_unwaived_unresolved_legacy_assets_fail_closed(self) -> None:
        legacy = self.root / "docs" / "integrity" / "experiment_attempt_registry.jsonl"
        legacy.write_text(
            json.dumps({"path": "projects/work/_repro/gone.json"}) + "\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(study_workspace.StudyWorkspaceError, "fail-closed"):
            study_workspace.enforce_legacy_fail_closed(self.root)

        resolution_path = self.root / study_workspace.RESOLUTION_PATH
        resolution_path.write_text(
            json.dumps(
                {
                    "schema": "legacy-asset-resolution-v1",
                    "resolutions": [
                        {
                            "path": "projects/work/_repro/gone.json",
                            "state": "COLD_BACKUP_RESOLVED",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        study_workspace.enforce_legacy_fail_closed(self.root)

    def test_registry_and_entry_schema_errors_fail_closed(self) -> None:
        invalid_documents = (
            {**self.registry, "extra": True},
            {**self.registry, "repo_creation_gate": "CONDITIONAL_GO"},
            {**self.registry, "studies": {}},
        )
        for document in invalid_documents:
            with self.subTest(document=document):
                self.registry = document
                self.write_registry()
                with self.assertRaises(study_workspace.StudyWorkspaceError):
                    study_workspace.load_and_validate_registry(self.root)

        entry = self.admitted_study()
        invalid_entries = []
        missing_key = dict(entry)
        missing_key.pop("name")
        invalid_entries.append(missing_key)
        invalid_entries.extend(
            (
                {**entry, "name": ""},
                {**entry, "local_path": "studies/wrong"},
                {**entry, "github_repo": "ssh://example.invalid/repo"},
                {**entry, "experiment_index": "wiki/experiments/wrong/README.md"},
                {**entry, "decision_record": "docs/decision.md"},
            )
        )
        for invalid in invalid_entries:
            with self.subTest(invalid=invalid):
                self.registry = {
                    **study_workspace.FIXED_REGISTRY_FIELDS,
                    "studies": [invalid],
                }
                self.write_registry()
                with self.assertRaises(study_workspace.StudyWorkspaceError):
                    study_workspace.load_and_validate_registry(self.root)

    def test_strict_json_paths_ignore_and_missing_control_plane_fail_closed(self) -> None:
        registry_path = self.root / "studies" / "registry.json"
        registry_path.write_text('{"schema": 1, "schema": 2}', encoding="utf-8")
        with self.assertRaisesRegex(study_workspace.StudyWorkspaceError, "duplicate JSON key"):
            study_workspace.load_and_validate_registry(self.root)

        registry_path.write_text("{", encoding="utf-8")
        with self.assertRaisesRegex(study_workspace.StudyWorkspaceError, "cannot load strict JSON"):
            study_workspace.load_and_validate_registry(self.root)

        self.registry = {**study_workspace.FIXED_REGISTRY_FIELDS, "studies": []}
        self.write_registry()
        (self.root / ".gitignore").write_text("projects/*/\n", encoding="utf-8")
        with self.assertRaisesRegex(study_workspace.StudyWorkspaceError, r"studies/\*/"):
            study_workspace.load_and_validate_registry(self.root)

        with self.assertRaises(study_workspace.StudyWorkspaceError):
            study_workspace._repo_path(self.root, "../escape")
        (self.root / "wiki" / "Experiment-Assets.md").unlink()
        with self.assertRaisesRegex(study_workspace.StudyWorkspaceError, "control plane"):
            study_workspace.validate_experiment_control_plane(self.root)

    def test_legacy_inventory_and_inventory_snapshot_fail_closed(self) -> None:
        legacy = self.root / "docs" / "integrity" / "experiment_attempt_registry.jsonl"
        with self.assertRaisesRegex(study_workspace.StudyWorkspaceError, "cannot read legacy"):
            study_workspace.build_experiment_asset_inventory(self.root)

        for raw in ('{"path":', '{}\n'):
            with self.subTest(raw=raw):
                legacy.write_text(raw, encoding="utf-8")
                with self.assertRaises(study_workspace.StudyWorkspaceError):
                    study_workspace.build_experiment_asset_inventory(self.root)

        legacy.write_text("\n", encoding="utf-8")
        inventory = study_workspace.build_experiment_asset_inventory(self.root)
        inventory_path = self.root / study_workspace.INVENTORY_PATH
        inventory_path.write_text("{}\n", encoding="utf-8")
        with self.assertRaisesRegex(study_workspace.StudyWorkspaceError, "is stale"):
            study_workspace.validate_inventory_file(self.root)
        inventory_path.write_text(study_workspace._render_json(inventory), encoding="utf-8")
        study_workspace.validate_inventory_file(self.root)

    def test_cli_checks_renders_and_reports_controlled_failure(self) -> None:
        legacy = self.root / "docs" / "integrity" / "experiment_attempt_registry.jsonl"
        legacy.write_text("", encoding="utf-8")
        inventory = study_workspace.build_experiment_asset_inventory(self.root)
        (self.root / study_workspace.INVENTORY_PATH).write_text(
            study_workspace._render_json(inventory), encoding="utf-8"
        )
        with mock.patch.object(study_workspace, "REPO", self.root):
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(0, study_workspace.main([]))
            self.assertIn("PASS", output.getvalue())

            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(0, study_workspace.main(["--render-inventory"]))
            self.assertIn(study_workspace.INVENTORY_SCHEMA, output.getvalue())

            (self.root / "studies" / "registry.json").unlink()
            error = io.StringIO()
            with redirect_stderr(error):
                self.assertEqual(1, study_workspace.main([]))
            self.assertIn("FAIL", error.getvalue())


if __name__ == "__main__":
    unittest.main()
