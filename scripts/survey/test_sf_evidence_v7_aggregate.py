#!/usr/bin/env python3
"""Adversarial contracts for the two-leaf evidence-v7 aggregator."""
from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import sf_evidence_v7_aggregate as aggregate  # noqa: E402


def valid_leaf(role, runner_sha256):
    return {
        "artifact_id": aggregate.LEAF_ARTIFACT_ID,
        "contract_version": aggregate.CONTRACT_VERSION,
        "implementation_freeze": aggregate.IMPLEMENTATION_FREEZE,
        "runner": {
            "path": aggregate.RUNNER_RELATIVE_PATH,
            "sha256": runner_sha256,
        },
        "input_provenance": {
            "coding": {"path": "coding.json", "sha256": "1" * 64},
            "absence_adjudication": {
                "path": "absence.json",
                "sha256": "2" * 64,
            },
            "sidecars": [
                {"path": "sidecar-a.json", "sha256": "3" * 64},
                {"path": "sidecar-b.json", "sha256": "4" * 64},
            ],
        },
        "input_snapshot_sha256": "5" * 64,
        "platform": {
            "os": role,
            "sys_platform": "win32" if role == "nt" else "linux",
            "python": "3.14.3" if role == "nt" else "3.12.11",
        },
        "checks": [
            {"id": "V0", "check": "contract", "result": "PASS", "detail": ""}
        ],
        "occupancy": {"n_method_paths": 11, "reward_guided": "6/11"},
        "mutation_results": {
            "legitimate_field_specific_negative_control": [],
            "positive_categorical_absence": ["absence-field-value-not-allowed"],
        },
        "failure_codes": [],
        "summary": "1/1 PASS",
        "verdict": "PASS",
    }


class AggregateTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.runner = self.root / "runner.py"
        self.runner.write_bytes(b"frozen runner bytes\n")
        self.runner_sha256 = hashlib.sha256(self.runner.read_bytes()).hexdigest()
        self.nt_path = self.root / "leaf.nt.json"
        self.posix_path = self.root / "leaf.posix.json"
        self.nt = valid_leaf("nt", self.runner_sha256)
        self.posix = valid_leaf("posix", self.runner_sha256)
        self.write_leaves()

    def tearDown(self):
        self.temporary.cleanup()

    def write_json(self, path, value):
        path.write_text(
            json.dumps(value, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8",
            newline="\n",
        )

    def write_leaves(self):
        self.write_json(self.nt_path, self.nt)
        self.write_json(self.posix_path, self.posix)

    def build(self):
        return aggregate.aggregate_leaves(
            self.nt_path, self.posix_path, runner_path=self.runner
        )

    def test_valid_distinct_platform_leaves_build_exact_receipt(self):
        receipt = self.build()
        self.assertEqual("PASS", receipt["verdict"])
        self.assertEqual(
            self.nt["input_snapshot_sha256"], receipt["input_snapshot_sha256"]
        )
        self.assertEqual(
            {"nt", "posix"}, {leaf["platform_os"] for leaf in receipt["leaves"]}
        )
        self.assertEqual(
            hashlib.sha256(self.nt_path.read_bytes()).hexdigest(),
            next(leaf["sha256"] for leaf in receipt["leaves"] if leaf["platform_os"] == "nt"),
        )

    def test_deleting_either_leaf_fails(self):
        for target in (self.nt_path, self.posix_path):
            with self.subTest(target=target.name):
                self.write_leaves()
                target.unlink()
                with self.assertRaises(aggregate.AggregationError):
                    self.build()

    def test_replacing_posix_leaf_with_nt_leaf_fails(self):
        self.posix_path.write_bytes(self.nt_path.read_bytes())
        with self.assertRaisesRegex(aggregate.AggregationError, "platform"):
            self.build()

    def test_shared_contract_and_semantic_mutations_fail(self):
        cases = {
            "input hash": lambda leaf: leaf.update(input_snapshot_sha256="9" * 64),
            "runner blob": lambda leaf: leaf["runner"].update(sha256="9" * 64),
            "contract version": lambda leaf: leaf.update(contract_version="other"),
            "implementation freeze": lambda leaf: leaf.update(implementation_freeze="9" * 40),
            "named failures": lambda leaf: leaf["failure_codes"].append("ABSENCE_REVIEW"),
            "occupancy": lambda leaf: leaf["occupancy"].update(n_method_paths=10),
            "checks": lambda leaf: leaf["checks"][0].update(result="FAIL"),
            "summary": lambda leaf: leaf.update(summary="0/1 PASS"),
            "verdict": lambda leaf: leaf.update(verdict="FAIL"),
        }
        for label, mutate in cases.items():
            with self.subTest(label=label):
                self.posix = valid_leaf("posix", self.runner_sha256)
                mutate(self.posix)
                self.write_leaves()
                with self.assertRaises(aggregate.AggregationError):
                    self.build()

    def test_platform_stamp_mutations_fail(self):
        cases = [
            {"os": "nt", "sys_platform": "linux", "python": "3.12.11"},
            {"os": "posix", "sys_platform": "win32", "python": "3.12.11"},
            {"os": "windows", "sys_platform": "linux", "python": "3.12.11"},
        ]
        for stamp in cases:
            with self.subTest(stamp=stamp):
                self.posix = valid_leaf("posix", self.runner_sha256)
                self.posix["platform"] = stamp
                self.write_leaves()
                with self.assertRaises(aggregate.AggregationError):
                    self.build()

    def test_runner_file_drift_fails_even_when_leaves_agree(self):
        self.runner.write_bytes(b"changed runner bytes\n")
        with self.assertRaisesRegex(aggregate.AggregationError, "runner"):
            self.build()

    def test_write_then_check_is_deterministic_and_writes_only_aggregate(self):
        output = self.root / "aggregate.json"
        args = [
            "--nt-leaf", os.fspath(self.nt_path),
            "--posix-leaf", os.fspath(self.posix_path),
            "--runner", os.fspath(self.runner),
            "--output", os.fspath(output),
        ]
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, aggregate.main([*args, "--write"]))
            initial = output.read_bytes()
            self.assertEqual(0, aggregate.main([*args, "--check"]))
            self.assertEqual(0, aggregate.main([*args, "--write"]))
        self.assertEqual(initial, output.read_bytes())
        self.assertEqual(
            {"aggregate.json", "leaf.nt.json", "leaf.posix.json", "runner.py"},
            {path.name for path in self.root.iterdir()},
        )

    def test_check_rejects_missing_or_stale_aggregate(self):
        output = self.root / "aggregate.json"
        args = [
            "--nt-leaf", os.fspath(self.nt_path),
            "--posix-leaf", os.fspath(self.posix_path),
            "--runner", os.fspath(self.runner),
            "--output", os.fspath(output),
            "--check",
        ]
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(1, aggregate.main(args))
            output.write_bytes(b"{}\n")
            self.assertEqual(1, aggregate.main(args))


if __name__ == "__main__":
    unittest.main()
