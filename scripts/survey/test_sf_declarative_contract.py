#!/usr/bin/env python3
"""Tests for the declarative contract engine (schema sf-declarative-contract-v1).

Positive coverage runs the three real contracts under docs/contracts/ against
the live repository.  Negative coverage builds isolated tempdir fixtures (no
repository file is ever written) covering: a missing must_contain string, a
forbidden must_not_contain string, a bad top-level schema value, a duplicate
JSON key, a jsonl_key_set_equality set mismatch, and a registry_ledger_binding
hash/status mismatch.
"""

from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import sf_declarative_contract as engine  # noqa: E402


def _silent(callable_, *args, **kwargs):
    """Run callable_ while discarding its stdout, and return its result."""
    with contextlib.redirect_stdout(io.StringIO()):
        return callable_(*args, **kwargs)


class RealContractsTests(unittest.TestCase):
    """The three production contracts must fully pass against live data."""

    def test_discover_finds_exactly_the_three_migrated_contracts(self) -> None:
        self.assertEqual(
            ["r1-problem-definition", "r2-problem-definition"],
            engine.discover_contract_ids(),
        )

    def test_each_real_contract_passes_individually(self) -> None:
        for contract_id in engine.discover_contract_ids():
            with self.subTest(contract_id=contract_id):
                self.assertTrue(_silent(engine.run_contract, contract_id))

    def test_check_all_cli_exits_zero(self) -> None:
        self.assertEqual(0, _silent(engine.main, ["--check-all"]))

    def test_check_single_cli_exits_zero(self) -> None:
        self.assertEqual(0, _silent(engine.main, ["--check", "r1-problem-definition"]))

    def test_check_unknown_contract_id_exits_one(self) -> None:
        self.assertEqual(1, _silent(engine.main, ["--check", "does-not-exist"]))

    def test_check_all_and_check_are_mutually_exclusive(self) -> None:
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                engine.main(["--check-all", "--check", "r1-problem-definition"])


class _FixtureRepoTestCase(unittest.TestCase):
    """Base class that points the engine at an isolated tempdir repo."""

    def setUp(self) -> None:
        self._temp = tempfile.TemporaryDirectory()
        self.addCleanup(self._temp.cleanup)
        self.repo = Path(self._temp.name)
        self.contracts_dir = self.repo / "docs" / "contracts"
        self.contracts_dir.mkdir(parents=True)
        patcher_repo = mock.patch.object(engine, "REPO", self.repo)
        patcher_dir = mock.patch.object(engine, "CONTRACTS_DIR", self.contracts_dir)
        patcher_repo.start()
        patcher_dir.start()
        self.addCleanup(patcher_repo.stop)
        self.addCleanup(patcher_dir.stop)

    def write_target(self, relative: str, content: str) -> None:
        path = self.repo.joinpath(*relative.split("/"))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def write_jsonl(self, relative: str, rows: list[dict]) -> None:
        path = self.repo.joinpath(*relative.split("/"))
        path.parent.mkdir(parents=True, exist_ok=True)
        text = "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n"
        path.write_text(text, encoding="utf-8")

    def write_contract(self, contract_id: str, document: dict) -> None:
        path = self.contracts_dir / f"{contract_id}.json"
        path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def write_contract_raw(self, contract_id: str, raw_text: str) -> None:
        path = self.contracts_dir / f"{contract_id}.json"
        path.write_text(raw_text, encoding="utf-8")


class SyntheticAllFourPrimitivesPassTests(_FixtureRepoTestCase):
    """A self-contained fixture exercising all four primitives at once."""

    def test_fully_synthetic_contract_passes(self) -> None:
        self.write_target("docs/target.md", "alpha beta gamma\nno forbidden token here\n")
        self.write_jsonl(
            "data/registry.jsonl",
            [
                {
                    "arxiv_id": "1111.11111",
                    "canonical_id": "arxiv:1111.11111",
                    "schema": "fixture-registry-v1",
                    "provenance": {"pdf_sha256": "aaa", "eprint_sha256": "bbb"},
                },
                {
                    "arxiv_id": "2222.22222",
                    "canonical_id": "arxiv:2222.22222",
                    "schema": "fixture-registry-v1",
                    "provenance": {"pdf_sha256": "ccc", "eprint_sha256": "ddd"},
                },
            ],
        )
        self.write_jsonl(
            "data/ledger.jsonl",
            [
                {
                    "arxiv_id": "1111.11111",
                    "kind": "pdf",
                    "http_status": 200,
                    "error": None,
                    "stored_at": "/tmp/1111.pdf",
                    "sha256": "aaa",
                },
                {
                    "arxiv_id": "1111.11111",
                    "kind": "eprint",
                    "http_status": 200,
                    "error": None,
                    "stored_at": "/tmp/1111.eprint",
                    "sha256": "bbb",
                },
                {
                    "arxiv_id": "2222.22222",
                    "kind": "pdf",
                    "http_status": 200,
                    "error": None,
                    "stored_at": "/tmp/2222.pdf",
                    "sha256": "ccc",
                },
                {
                    "arxiv_id": "2222.22222",
                    "kind": "eprint",
                    "http_status": 200,
                    "error": None,
                    "stored_at": "/tmp/2222.eprint",
                    "sha256": "ddd",
                },
            ],
        )
        self.write_contract(
            "fixture-all-four",
            {
                "schema": "sf-declarative-contract-v1",
                "contract_id": "fixture-all-four",
                "cases": [
                    {
                        "id": "has_alpha_and_gamma",
                        "type": "must_contain",
                        "target": "docs/target.md",
                        "strings": ["alpha", "gamma"],
                    },
                    {
                        "id": "no_forbidden_delta",
                        "type": "must_not_contain",
                        "target": "docs/target.md",
                        "strings": ["delta"],
                    },
                    {
                        "id": "registry_ids_match",
                        "type": "jsonl_key_set_equality",
                        "target": "data/registry.jsonl",
                        "field": "arxiv_id",
                        "values": ["1111.11111", "2222.22222"],
                        "unique_field": "canonical_id",
                    },
                    {
                        "id": "registry_bound_to_ledger",
                        "type": "registry_ledger_binding",
                        "registry": "data/registry.jsonl",
                        "ledger": "data/ledger.jsonl",
                        "id_field": "arxiv_id",
                        "kinds": ["pdf", "eprint"],
                        "schema": "fixture-registry-v1",
                    },
                ],
            },
        )
        self.assertTrue(_silent(engine.run_contract, "fixture-all-four"))

    def test_targets_list_applies_the_same_strings_to_every_file(self) -> None:
        self.write_target("a.md", "shared-token only-in-a")
        self.write_target("b.md", "shared-token only-in-b")
        self.write_contract(
            "fixture-targets-list",
            {
                "schema": "sf-declarative-contract-v1",
                "contract_id": "fixture-targets-list",
                "cases": [
                    {
                        "id": "shared_token_in_both",
                        "type": "must_contain",
                        "targets": ["a.md", "b.md"],
                        "strings": ["shared-token"],
                    }
                ],
            },
        )
        self.assertTrue(_silent(engine.run_contract, "fixture-targets-list"))

    def test_targets_list_fails_if_any_one_file_is_missing_the_string(self) -> None:
        self.write_target("a.md", "shared-token")
        self.write_target("b.md", "no match here")
        self.write_contract(
            "fixture-targets-list-fail",
            {
                "schema": "sf-declarative-contract-v1",
                "contract_id": "fixture-targets-list-fail",
                "cases": [
                    {
                        "id": "shared_token_in_both",
                        "type": "must_contain",
                        "targets": ["a.md", "b.md"],
                        "strings": ["shared-token"],
                    }
                ],
            },
        )
        self.assertFalse(_silent(engine.run_contract, "fixture-targets-list-fail"))


class NegativeCaseTests(_FixtureRepoTestCase):
    def _basic_contract(self, contract_id: str, case: dict) -> None:
        self.write_contract(
            contract_id,
            {
                "schema": "sf-declarative-contract-v1",
                "contract_id": contract_id,
                "cases": [case],
            },
        )

    def test_missing_must_contain_string_fails(self) -> None:
        self.write_target("doc.md", "only this sentence is present\n")
        self._basic_contract(
            "missing-string",
            {
                "id": "needle_absent",
                "type": "must_contain",
                "target": "doc.md",
                "strings": ["NEEDLE_NOT_PRESENT"],
            },
        )
        self.assertFalse(_silent(engine.run_contract, "missing-string"))

    def test_forbidden_must_not_contain_string_fails(self) -> None:
        self.write_target("doc.md", "this text carries FORBIDDEN_TOKEN inline\n")
        self._basic_contract(
            "forbidden-present",
            {
                "id": "forbidden_should_be_absent",
                "type": "must_not_contain",
                "target": "doc.md",
                "strings": ["FORBIDDEN_TOKEN"],
            },
        )
        self.assertFalse(_silent(engine.run_contract, "forbidden-present"))

    def test_bad_schema_value_fails(self) -> None:
        self.write_target("doc.md", "content\n")
        self.write_contract(
            "bad-schema",
            {
                "schema": "not-the-declarative-contract-schema",
                "contract_id": "bad-schema",
                "cases": [
                    {
                        "id": "irrelevant",
                        "type": "must_contain",
                        "target": "doc.md",
                        "strings": ["content"],
                    }
                ],
            },
        )
        self.assertFalse(_silent(engine.run_contract, "bad-schema"))

    def test_missing_schema_field_fails(self) -> None:
        self.write_target("doc.md", "content\n")
        self.write_contract(
            "no-schema",
            {
                "contract_id": "no-schema",
                "cases": [
                    {
                        "id": "irrelevant",
                        "type": "must_contain",
                        "target": "doc.md",
                        "strings": ["content"],
                    }
                ],
            },
        )
        self.assertFalse(_silent(engine.run_contract, "no-schema"))

    def test_duplicate_top_level_json_key_fails(self) -> None:
        self.write_target("doc.md", "content\n")
        raw = (
            "{\n"
            '  "schema": "sf-declarative-contract-v1",\n'
            '  "schema": "sf-declarative-contract-v1",\n'
            '  "contract_id": "dup-key",\n'
            '  "cases": [\n'
            "    {\n"
            '      "id": "irrelevant",\n'
            '      "type": "must_contain",\n'
            '      "target": "doc.md",\n'
            '      "strings": ["content"]\n'
            "    }\n"
            "  ]\n"
            "}\n"
        )
        self.write_contract_raw("dup-key", raw)
        self.assertFalse(_silent(engine.run_contract, "dup-key"))

    def test_duplicate_case_field_key_fails(self) -> None:
        self.write_target("doc.md", "content\n")
        raw = (
            "{\n"
            '  "schema": "sf-declarative-contract-v1",\n'
            '  "contract_id": "dup-case-key",\n'
            '  "cases": [\n'
            "    {\n"
            '      "id": "irrelevant",\n'
            '      "id": "irrelevant-again",\n'
            '      "type": "must_contain",\n'
            '      "target": "doc.md",\n'
            '      "strings": ["content"]\n'
            "    }\n"
            "  ]\n"
            "}\n"
        )
        self.write_contract_raw("dup-case-key", raw)
        self.assertFalse(_silent(engine.run_contract, "dup-case-key"))

    def test_unknown_case_type_fails(self) -> None:
        self.write_target("doc.md", "content\n")
        self._basic_contract(
            "unknown-type",
            {
                "id": "irrelevant",
                "type": "some_primitive_that_does_not_exist",
                "target": "doc.md",
                "strings": ["content"],
            },
        )
        self.assertFalse(_silent(engine.run_contract, "unknown-type"))

    def test_jsonl_key_set_equality_mismatch_fails(self) -> None:
        self.write_jsonl(
            "registry.jsonl",
            [
                {"arxiv_id": "1111.11111", "canonical_id": "arxiv:1111.11111"},
                {"arxiv_id": "9999.99999", "canonical_id": "arxiv:9999.99999"},
            ],
        )
        self._basic_contract(
            "set-mismatch",
            {
                "id": "ids_do_not_match",
                "type": "jsonl_key_set_equality",
                "target": "registry.jsonl",
                "field": "arxiv_id",
                "values": ["1111.11111", "2222.22222"],
                "unique_field": "canonical_id",
            },
        )
        self.assertFalse(_silent(engine.run_contract, "set-mismatch"))

    def test_jsonl_key_set_equality_duplicate_unique_field_fails(self) -> None:
        self.write_jsonl(
            "registry.jsonl",
            [
                {"arxiv_id": "1111.11111", "canonical_id": "arxiv:same"},
                {"arxiv_id": "2222.22222", "canonical_id": "arxiv:same"},
            ],
        )
        self._basic_contract(
            "dup-unique-field",
            {
                "id": "canonical_id_must_be_unique",
                "type": "jsonl_key_set_equality",
                "target": "registry.jsonl",
                "field": "arxiv_id",
                "values": ["1111.11111", "2222.22222"],
                "unique_field": "canonical_id",
            },
        )
        self.assertFalse(_silent(engine.run_contract, "dup-unique-field"))

    def test_registry_ledger_binding_sha256_mismatch_fails(self) -> None:
        self.write_jsonl(
            "registry.jsonl",
            [
                {
                    "arxiv_id": "1111.11111",
                    "schema": "fixture-registry-v1",
                    "provenance": {"pdf_sha256": "expected-hash", "eprint_sha256": "bbb"},
                }
            ],
        )
        self.write_jsonl(
            "ledger.jsonl",
            [
                {
                    "arxiv_id": "1111.11111",
                    "kind": "pdf",
                    "http_status": 200,
                    "error": None,
                    "stored_at": "/tmp/1111.pdf",
                    "sha256": "WRONG-HASH",
                },
                {
                    "arxiv_id": "1111.11111",
                    "kind": "eprint",
                    "http_status": 200,
                    "error": None,
                    "stored_at": "/tmp/1111.eprint",
                    "sha256": "bbb",
                },
            ],
        )
        self._basic_contract(
            "hash-mismatch",
            {
                "id": "pdf_hash_must_match",
                "type": "registry_ledger_binding",
                "registry": "registry.jsonl",
                "ledger": "ledger.jsonl",
                "id_field": "arxiv_id",
                "kinds": ["pdf", "eprint"],
                "schema": "fixture-registry-v1",
            },
        )
        self.assertFalse(_silent(engine.run_contract, "hash-mismatch"))

    def test_registry_ledger_binding_missing_ledger_row_fails(self) -> None:
        self.write_jsonl(
            "registry.jsonl",
            [
                {
                    "arxiv_id": "1111.11111",
                    "schema": "fixture-registry-v1",
                    "provenance": {"pdf_sha256": "aaa", "eprint_sha256": "bbb"},
                }
            ],
        )
        self.write_jsonl(
            "ledger.jsonl",
            [
                {
                    "arxiv_id": "1111.11111",
                    "kind": "pdf",
                    "http_status": 200,
                    "error": None,
                    "stored_at": "/tmp/1111.pdf",
                    "sha256": "aaa",
                }
                # eprint row intentionally missing
            ],
        )
        self._basic_contract(
            "missing-ledger-row",
            {
                "id": "both_kinds_required",
                "type": "registry_ledger_binding",
                "registry": "registry.jsonl",
                "ledger": "ledger.jsonl",
                "id_field": "arxiv_id",
                "kinds": ["pdf", "eprint"],
                "schema": "fixture-registry-v1",
            },
        )
        self.assertFalse(_silent(engine.run_contract, "missing-ledger-row"))

    def test_registry_ledger_binding_http_error_fails(self) -> None:
        self.write_jsonl(
            "registry.jsonl",
            [
                {
                    "arxiv_id": "1111.11111",
                    "schema": "fixture-registry-v1",
                    "provenance": {"pdf_sha256": "aaa", "eprint_sha256": "bbb"},
                }
            ],
        )
        self.write_jsonl(
            "ledger.jsonl",
            [
                {
                    "arxiv_id": "1111.11111",
                    "kind": "pdf",
                    "http_status": 404,
                    "error": "not found",
                    "stored_at": "",
                    "sha256": "aaa",
                },
                {
                    "arxiv_id": "1111.11111",
                    "kind": "eprint",
                    "http_status": 200,
                    "error": None,
                    "stored_at": "/tmp/1111.eprint",
                    "sha256": "bbb",
                },
            ],
        )
        self._basic_contract(
            "http-error",
            {
                "id": "must_have_fetched_cleanly",
                "type": "registry_ledger_binding",
                "registry": "registry.jsonl",
                "ledger": "ledger.jsonl",
                "id_field": "arxiv_id",
                "kinds": ["pdf", "eprint"],
                "schema": "fixture-registry-v1",
            },
        )
        self.assertFalse(_silent(engine.run_contract, "http-error"))

    def test_path_traversal_target_is_rejected(self) -> None:
        self._basic_contract(
            "path-traversal",
            {
                "id": "escape_attempt",
                "type": "must_contain",
                "target": "../outside.md",
                "strings": ["x"],
            },
        )
        self.assertFalse(_silent(engine.run_contract, "path-traversal"))

    def test_target_and_targets_together_is_rejected(self) -> None:
        self.write_target("doc.md", "content\n")
        self._basic_contract(
            "target-and-targets",
            {
                "id": "ambiguous",
                "type": "must_contain",
                "target": "doc.md",
                "targets": ["doc.md"],
                "strings": ["content"],
            },
        )
        self.assertFalse(_silent(engine.run_contract, "target-and-targets"))

    def test_empty_contracts_dir_check_all_fails(self) -> None:
        self.assertEqual(1, _silent(engine.main, ["--check-all"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
