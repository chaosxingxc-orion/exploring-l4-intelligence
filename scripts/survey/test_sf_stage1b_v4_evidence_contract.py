#!/usr/bin/env python3
"""Focused contracts for the Stage-1B v4 rereview repairs."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

import sf_stage1b_v4_evidence_contract as contract  # noqa: E402


class ReconciliationContractTests(unittest.TestCase):
    def setUp(self):
        self.document = json.loads((REPO / contract.RECONCILIATION_PATH).read_text(encoding="utf-8"))

    def test_required_known_priors_are_unique_and_reused(self):
        self.assertEqual([], contract.validate_reconciliation(self.document))

    def test_duplicate_seed_action_fails(self):
        mutated = copy.deepcopy(self.document)
        mutated["rows"][0]["seed_action"] = "CREATE_NEW_SEED"
        self.assertTrue(any(item.startswith("RECONCILIATION_SEED_ACTION_INVALID") for item in contract.validate_reconciliation(mutated)))


class ControlBasisContractTests(unittest.TestCase):
    def setUp(self):
        self.supplement = json.loads((REPO / contract.SUPPLEMENT_PATH).read_text(encoding="utf-8"))
        self.control = json.loads((REPO / contract.CONTROL_BASIS_PATH).read_text(encoding="utf-8"))

    def test_every_direct_row_has_one_control_basis(self):
        self.assertEqual([], contract.validate_control_basis(self.control, self.supplement))

    def test_missing_direct_row_fails(self):
        mutated = copy.deepcopy(self.control)
        mutated["rows"].pop()
        self.assertTrue(any(item.startswith("CONTROL_BASIS_DIRECT_ID_MISMATCH") for item in contract.validate_control_basis(mutated, self.supplement)))


class FulltextBindingContractTests(unittest.TestCase):
    def test_local_pdf_hash_is_required_when_local_check_enabled(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            pdf = root / "survey-fulltext" / "1234.56789" / "1234.56789.pdf"
            pdf.parent.mkdir(parents=True)
            pdf.write_bytes(b"pdf-bytes")
            sha = hashlib.sha256(pdf.read_bytes()).hexdigest()
            ledger = [{"arxiv_id": "1234.56789", "kind": "pdf", "http_status": 200, "error": None, "bytes": 9, "sha256": sha, "stored_at": str(pdf)}]
            rows = [{"paper_work_id": "1234.56789", "depth": "FULLTEXT_ROUTED", "fulltext_ref": {"sha256": sha}}]
            self.assertEqual([], contract.validate_fulltext_bindings(rows, ledger, data_root=root))
            pdf.write_bytes(b"corrupt")
            self.assertIn("FULLTEXT_LOCAL_SHA_MISMATCH:1234.56789", contract.validate_fulltext_bindings(rows, ledger, data_root=root))


class AssetMatrixContractTests(unittest.TestCase):
    def setUp(self):
        self.document = json.loads((REPO / contract.ASSET_MATRIX_PATH).read_text(encoding="utf-8"))

    def test_exact_identity_and_no_git_data_policy_are_explicit(self):
        self.assertEqual([], contract.validate_asset_matrix(self.document))

    def test_voicebench_identity_warning_is_required(self):
        mutated = copy.deepcopy(self.document)
        voice = next(row for row in mutated["assets"] if row["asset_id"] == "voiceagentbench")
        voice["dataset_status"].pop("identity_warning")
        self.assertIn("ASSET_VOICE_IDENTITY_WARNING_MISSING", contract.validate_asset_matrix(mutated))


class RepositoryIntegrationTests(unittest.TestCase):
    def test_repository_v4_contract(self):
        self.assertEqual([], contract.validate_repository(REPO, require_local=False))


if __name__ == "__main__":
    unittest.main()
