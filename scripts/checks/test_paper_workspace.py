"""Contract tests for the zero-state Stage-3 paper workspace gate."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("paper_workspace_check.py")
SPEC = importlib.util.spec_from_file_location("paper_workspace_check", SCRIPT)
assert SPEC and SPEC.loader
paper_workspace = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(paper_workspace)


class PaperZeroStateTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / "papers").mkdir()
        (self.root / "wiki").mkdir()
        (self.root / ".gitignore").write_text(
            "studies/*/\npapers/*/\n", encoding="utf-8"
        )
        (self.root / "papers" / "README.md").write_text(
            "# Paper project workspace\n", encoding="utf-8"
        )
        self.registry = {
            "schema": "paper-repository-registry-v1",
            "local_root": "papers",
            "repo_creation_gate": "OWNER_GO_AND_PAPER_EXECUTION_CONTRACT",
            "candidate_id_policy": "AUDIT_ONLY_NEVER_ENGINEERING_IDENTITY",
            "promotion_control_plane": "wiki/Experiment-Assets.md",
            "papers": [],
        }
        self.write_registry()
        self.write_control_plane(0)

    def write_registry(self, raw: str | None = None) -> None:
        text = raw if raw is not None else json.dumps(self.registry)
        (self.root / "papers" / "registry.json").write_text(text, encoding="utf-8")

    def write_control_plane(self, count: int) -> None:
        (self.root / "wiki" / "Experiment-Assets.md").write_text(
            f"Admitted paper repositories: **{count}**.\n", encoding="utf-8"
        )

    def test_zero_state_passes(self) -> None:
        document = paper_workspace.validate_zero_state(self.root)
        self.assertEqual([], document["papers"])

    def test_duplicate_json_key_fails_closed(self) -> None:
        self.write_registry(
            '{"schema": "paper-repository-registry-v1", "schema": "x", "local_root": "papers", '
            '"repo_creation_gate": "OWNER_GO_AND_PAPER_EXECUTION_CONTRACT", '
            '"candidate_id_policy": "AUDIT_ONLY_NEVER_ENGINEERING_IDENTITY", '
            '"promotion_control_plane": "wiki/Experiment-Assets.md", "papers": []}'
        )
        with self.assertRaisesRegex(paper_workspace.PaperWorkspaceError, "duplicate JSON key"):
            paper_workspace.validate_zero_state(self.root)

    def test_wrong_fixed_field_fails(self) -> None:
        self.registry["repo_creation_gate"] = "OWNER_GO_AND_EXECUTION_CONTRACT"
        self.write_registry()
        with self.assertRaisesRegex(paper_workspace.PaperWorkspaceError, "repo_creation_gate"):
            paper_workspace.validate_zero_state(self.root)

    def test_unexpected_top_level_key_fails(self) -> None:
        self.registry["reservation_ledger"] = "docs/integrity/somewhere.json"
        self.write_registry()
        with self.assertRaisesRegex(paper_workspace.PaperWorkspaceError, "exact keys"):
            paper_workspace.validate_zero_state(self.root)

    def test_registered_paper_entry_fails_closed_until_machinery_exists(self) -> None:
        self.registry["papers"] = [{"slug": "some-paper"}]
        self.write_registry()
        self.write_control_plane(1)
        with self.assertRaisesRegex(paper_workspace.PaperWorkspaceError, "promotion machinery"):
            paper_workspace.validate_zero_state(self.root)

    def test_unregistered_child_directory_fails(self) -> None:
        (self.root / "papers" / "rogue-paper").mkdir()
        with self.assertRaisesRegex(paper_workspace.PaperWorkspaceError, "no paper is admitted"):
            paper_workspace.validate_zero_state(self.root)

    def test_stray_file_on_surface_fails(self) -> None:
        (self.root / "papers" / "notes.txt").write_text("x\n", encoding="utf-8")
        with self.assertRaisesRegex(paper_workspace.PaperWorkspaceError, "zero-state surface"):
            paper_workspace.validate_zero_state(self.root)

    def test_missing_gitignore_rule_fails(self) -> None:
        (self.root / ".gitignore").write_text("studies/*/\n", encoding="utf-8")
        with self.assertRaisesRegex(paper_workspace.PaperWorkspaceError, "papers/\\*/"):
            paper_workspace.validate_zero_state(self.root)

    def test_control_plane_count_drift_fails(self) -> None:
        self.write_control_plane(1)
        with self.assertRaisesRegex(paper_workspace.PaperWorkspaceError, "count drift"):
            paper_workspace.validate_zero_state(self.root)

    def test_missing_control_plane_count_line_fails(self) -> None:
        (self.root / "wiki" / "Experiment-Assets.md").write_text(
            "no count here\n", encoding="utf-8"
        )
        with self.assertRaisesRegex(paper_workspace.PaperWorkspaceError, "admitted paper count"):
            paper_workspace.validate_zero_state(self.root)

    def test_missing_readme_fails(self) -> None:
        (self.root / "papers" / "README.md").unlink()
        with self.assertRaisesRegex(paper_workspace.PaperWorkspaceError, "README"):
            paper_workspace.validate_zero_state(self.root)


if __name__ == "__main__":
    unittest.main()
