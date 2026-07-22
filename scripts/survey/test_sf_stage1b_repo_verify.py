#!/usr/bin/env python3
"""Tests for repository evidence classification."""

from __future__ import annotations

import sys
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))

import sf_stage1b_repo_verify as verify


class RepositoryVerificationTests(unittest.TestCase):
    def test_canonicalizes_github_subpaths(self):
        self.assertEqual(
            verify.canonical_repository_url("https://github.com/acme/project/tree/main/demo"),
            "https://github.com/acme/project",
        )
        self.assertEqual(
            verify.canonical_repository_url("https://github.com/acme/project.git."),
            "https://github.com/acme/project",
        )

    def test_public_licensed_code_with_environment_is_verified(self):
        metadata = {"archived": False, "license": {"spdx_id": "Apache-2.0"}, "default_branch": "main"}
        paths = ["README.md", "LICENSE", "pyproject.toml", "configs/eval.yaml", "src/model.py"]
        result = verify.classify_github_repository("https://github.com/acme/project", metadata, paths)
        self.assertEqual(result["status"], "OPEN_SOURCE_VERIFIED")
        self.assertTrue(result["code_present"])
        self.assertTrue(result["environment_present"])

    def test_public_code_without_license_is_not_verified(self):
        metadata = {"archived": False, "license": None, "default_branch": "main"}
        paths = ["README.md", "requirements.txt", "main.py"]
        result = verify.classify_github_repository("https://github.com/acme/project", metadata, paths)
        self.assertEqual(result["status"], "REPOSITORY_REACHABLE_LICENSE_UNRESOLVED")

    def test_empty_or_document_only_repo_is_not_reproduction_ready(self):
        metadata = {"archived": False, "license": {"spdx_id": "MIT"}, "default_branch": "main"}
        result = verify.classify_github_repository(
            "https://github.com/acme/project", metadata, ["README.md", "LICENSE"]
        )
        self.assertEqual(result["status"], "INSPECTABLE_BUT_REPRO_INCOMPLETE")

    def test_verify_github_records_tree_or_failure(self):
        metadata = {"archived": False, "license": {"spdx_id": "MIT"}, "default_branch": "main"}
        tree = {"tree": [{"type": "blob", "path": "README.md"}, {"type": "blob", "path": "main.py"}], "truncated": False}
        with mock.patch.object(verify, "_gh_api", side_effect=[metadata, tree]):
            result = verify.verify_github("https://github.com/acme/project", Path("gh"))
        self.assertEqual(result["status"], "INSPECTABLE_BUT_REPRO_INCOMPLETE")
        with mock.patch.object(verify, "_gh_api", side_effect=RuntimeError("offline")):
            failed = verify.verify_github("https://github.com/acme/project", Path("gh"))
        self.assertEqual(failed["status"], "REPOSITORY_UNREACHABLE")

    def test_run_deduplicates_canonical_urls_and_retains_invalid_links(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            triage = root / "triage.jsonl"
            triage.write_text(
                json.dumps(
                    {
                        "repo_urls": [
                            "https://github.com/acme/project/tree/main",
                            "https://github.com/acme/project.",
                            "https://gitlab.com/acme/other",
                            "https://example.com/not-a-repo",
                        ]
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            output = root / "verified.json"
            with mock.patch.object(
                verify,
                "verify_github",
                return_value={"url": "https://github.com/acme/project", "status": "OPEN_SOURCE_VERIFIED"},
            ):
                summary = verify.run(triage, output, Path("gh"))
            self.assertEqual(summary["canonical_repositories"], 2)
            self.assertEqual(summary["invalid_urls"], 1)
            self.assertTrue(output.is_file())


if __name__ == "__main__":
    unittest.main(verbosity=2)
