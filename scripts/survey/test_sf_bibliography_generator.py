#!/usr/bin/env python3
"""Contracts for receipt-derived, system-first reviewer bibliography."""
from __future__ import annotations

import copy
import contextlib
import hashlib
import io
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import sf_bibliography_generator as bibliography  # noqa: E402


DIRECT_NEIGHBORS = {
    "2510.02995",
    "2605.28480",
    "2511.02834",
    "2606.15141",
    "2602.13685",
    "2407.09886",
    "2604.15710",
    "2505.09558",
    "2602.13891",
}
REVIEWER_ADDITIONS = {
    "2508.16665",
    "2510.18982",
    "2509.25845",
    "2502.20379",
    "2509.19676",
    "2510.23451",
    "2606.19341",
    "2502.04128",
    "2602.22897",
    "2602.00846",
    "2512.16899",
    "2606.00579",
    "2606.03183",
    "2502.19328",
    "2605.10344",
    "2508.00890",
}


class BibliographyGeneratorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipts = bibliography.load_receipts()

    def test_exact_90_unique_work_receipts_retain_65_and_add_25(self):
        self.assertEqual(90, len(self.receipts))
        identities = [row["identity"]["id"] for row in self.receipts]
        self.assertEqual(90, len(set(identities)))
        legacy = bibliography.legacy_bibliography_policies()
        self.assertEqual(65, len(legacy))
        self.assertTrue(set(legacy) <= set(identities))
        self.assertTrue(DIRECT_NEIGHBORS <= set(identities))
        self.assertTrue(REVIEWER_ADDITIONS <= set(identities))

    def test_arxiv_year_uses_initial_preprint_not_oai_datestamp(self):
        by_id = {row["identity"]["id"]: row for row in self.receipts}
        expected = {
            "2510.02995": 2025,
            "2510.07978": 2025,
            "2310.04406": 2023,
            "2508.21787": 2025,
            "2509.25845": 2025,
        }
        for identity, year in expected.items():
            with self.subTest(identity=identity):
                self.assertEqual(year, by_id[identity]["normalized"]["year"])
                self.assertEqual("initial_preprint", by_id[identity]["year_basis"])

    def test_selection_receipt_accounts_for_all_union_nodes_and_visible_works(self):
        selection = bibliography.load_selection_receipt()
        self.assertEqual(250, selection["union_population"])
        self.assertEqual(250, len(selection["union_dispositions"]))
        self.assertEqual(90, selection["reviewer_visible_total"])
        self.assertEqual(
            90,
            selection["selected_from_union"]
            + selection["reviewer_directed_outside_union"],
        )
        self.assertEqual(
            250,
            sum(selection["union_reason_code_counts"].values()),
        )
        self.assertNotIn(
            "NOT_SELECTED_REVIEWER_VISIBLE_SCOPE",
            selection["union_reason_code_counts"],
        )
        selected = [row for row in selection["union_dispositions"] if row["selected"]]
        self.assertTrue(all(row["selection_basis"] for row in selected))
        self.assertEqual(
            bibliography.VISIBLE_SELECTION_BASES,
            {
                basis
                for row in selected
                for basis in row["selection_basis"]
            },
        )

    def test_raw_official_payload_hash_and_identity_round_trip(self):
        for receipt in self.receipts:
            with self.subTest(identity=receipt["identity"]):
                raw_path = bibliography.ROOT / receipt["raw"]["path"]
                raw = raw_path.read_bytes()
                self.assertTrue(raw)
                self.assertEqual(len(raw), receipt["raw"]["bytes"])
                self.assertEqual(hashlib.sha256(raw).hexdigest(), receipt["raw"]["sha256"])
                reparsed = bibliography.parse_official_payload(
                    receipt["identity"], raw, receipt["raw"]["media_type"]
                )
                self.assertEqual(receipt["identity"], reparsed["identity"])
                self.assertEqual(receipt["normalized"]["title"], reparsed["title"])
                self.assertEqual(receipt["normalized"]["authors"], reparsed["authors"])
                self.assertEqual(receipt["normalized"]["year"], reparsed["year"])
                self.assertEqual(receipt["year_basis"], reparsed["year_basis"])

    def test_receipts_are_typed_nonquery_accesses_with_no_recall_credit(self):
        allowed = {
            "ID_DEREFERENCE",
            "PROVENANCE_FETCH",
            "REVIEW_CLAIM_VERIFICATION",
        }
        for receipt in self.receipts:
            self.assertIn(receipt["access_class"], allowed)
            self.assertFalse(receipt["query_recall_credit"])
            self.assertRegex(receipt["access_time_utc"], r"^20\d{2}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
            self.assertTrue(receipt["source_version"])
            self.assertTrue(receipt["official_url"].startswith("https://"))

    def test_no_placeholder_metadata_survives(self):
        forbidden = ("登记待读", "作者见官方页", "TBD", "UNKNOWN_AUTHOR", "placeholder")
        for receipt in self.receipts:
            combined = receipt["normalized"]["title"] + " " + " ".join(
                receipt["normalized"]["authors"]
            )
            self.assertFalse(any(token.casefold() in combined.casefold() for token in forbidden))
            self.assertTrue(receipt["normalized"]["authors"])

    def test_roles_and_three_reviewer_visible_chains_are_exact(self):
        self.assertEqual(
            bibliography.CANONICAL_ROLES,
            {receipt["bibliography"]["reference_role"] for receipt in self.receipts},
        )
        self.assertEqual(
            bibliography.CHAINS,
            {receipt["bibliography"]["chain"] for receipt in self.receipts},
        )
        by_id = {receipt["identity"]["id"]: receipt for receipt in self.receipts}
        for identity in DIRECT_NEIGHBORS:
            self.assertTrue(by_id[identity]["bibliography"]["direct_neighbor"])

    def test_generator_metadata_comes_from_receipts_not_constants(self):
        mutated = copy.deepcopy(self.receipts[:1])
        mutated[0]["normalized"]["title"] = "RECEIPT CONTROLLED TITLE"
        rendered = bibliography.render_bibliography(mutated)
        self.assertIn("RECEIPT CONTROLLED TITLE", rendered)
        self.assertFalse(hasattr(bibliography, "ROUND11"))
        self.assertFalse(hasattr(bibliography, "V8_BLOB"))

    def test_duplicate_identity_or_missing_raw_binding_fails_closed(self):
        duplicate = self.receipts + [copy.deepcopy(self.receipts[0])]
        self.assertIn("DUPLICATE_IDENTITY", bibliography.validate_receipts(duplicate))
        missing = copy.deepcopy(self.receipts)
        missing[0]["raw"].pop("sha256")
        self.assertIn("RAW_BINDING_INCOMPLETE", bibliography.validate_receipts(missing))

    def test_reviewer_known_cannot_receive_query_recall_credit(self):
        mutated = copy.deepcopy(self.receipts)
        row = next(receipt for receipt in mutated if receipt["identity"]["id"] == "2510.18982")
        row["query_recall_credit"] = True
        failures = bibliography.validate_receipts(mutated)
        self.assertIn("QUERY_RECALL_CREDIT_FORBIDDEN", failures)

    def test_render_has_each_identity_once_and_no_placeholder(self):
        rendered = bibliography.render_bibliography(self.receipts)
        for identity in DIRECT_NEIGHBORS | REVIEWER_ADDITIONS:
            self.assertEqual(1, rendered.count(identity), identity)
        self.assertIn("System-first speech/omni agent neighbors", rendered)
        self.assertIn("Reward and verification mechanisms", rendered)
        self.assertIn("Training-free and trained boundary comparators", rendered)
        self.assertNotIn("登记待读", rendered)

    def test_write_then_check_round_trip(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "bibliography.md"
            bibliography.write_output(self.receipts, output)
            self.assertEqual([], bibliography.check_output(self.receipts, output))
            output.write_text("drift\n", encoding="utf-8")
            self.assertEqual(["BIBLIOGRAPHY_DRIFT"], bibliography.check_output(self.receipts, output))

    def test_validation_passes_for_committed_receipts(self):
        self.assertEqual([], bibliography.validate_receipts(self.receipts))

    def test_cli_write_check_and_drift_paths(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "bibliography.md"
            selection = Path(temporary) / "selection.json"
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(
                    0,
                    bibliography.main(
                        [
                            "--write",
                            "--output",
                            str(output),
                            "--selection-output",
                            str(selection),
                        ]
                    ),
                )
                self.assertEqual(
                    0,
                    bibliography.main(
                        [
                            "--check",
                            "--output",
                            str(output),
                            "--selection-output",
                            str(selection),
                        ]
                    ),
                )
                output.write_text("drift\n", encoding="utf-8")
                self.assertEqual(
                    1,
                    bibliography.main(
                        [
                            "--check",
                            "--output",
                            str(output),
                            "--selection-output",
                            str(selection),
                        ]
                    ),
                )


if __name__ == "__main__":
    unittest.main()
