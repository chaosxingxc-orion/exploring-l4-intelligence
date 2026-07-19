#!/usr/bin/env python3
"""Focused regression tests for the parameterized coding generator."""
from __future__ import annotations

import contextlib
import inspect
import io
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import sf_coding_generator as generator  # noqa: E402


class CodingGeneratorTest(unittest.TestCase):
    def test_cli_defaults_select_the_active_v7_projection(self):
        args = generator.parse_args([])
        self.assertEqual("v7", args.profile)
        self.assertEqual(generator.ACTIVE_SIDECAR_DIR, args.sidecar_dir)
        self.assertEqual(generator.ACTIVE_OUT, args.out)
        self.assertEqual(generator.ACTIVE_TAXONOMY, args.taxonomy)
        self.assertFalse(args.check)

    def test_render_keeps_the_legacy_public_contract_and_bytes(self):
        signature = inspect.signature(generator.render)
        self.assertEqual(["sidecars", "taxonomy", "profile"], list(signature.parameters))
        self.assertEqual(generator.LEGACY_TAXONOMY,
                         signature.parameters["taxonomy"].default)
        self.assertEqual("v6", signature.parameters["profile"].default)

        sidecars = generator.load_sidecars(generator.LEGACY_SIDECAR_DIR)
        with io.open(generator.LEGACY_OUT, encoding="utf-8") as handle:
            expected = handle.read()
        self.assertEqual(expected, generator.render(sidecars))

    def test_v7_defaults_render_active_metadata_and_eleven_rows(self):
        sidecars = generator.load_sidecars(generator.ACTIVE_SIDECAR_DIR)
        rendered = generator.render(
            sidecars,
            taxonomy=generator.ACTIVE_TAXONOMY,
            profile="v7",
        )
        document = json.loads(rendered)
        self.assertEqual("SF-KNOWN-ITEM-CODING-V7-2026-07-19-01",
                         document["artifact_id"])
        self.assertEqual(
            "known-item coding v7 — GENERATED projection of schema-v3 sidecars",
            document["title"],
        )
        self.assertEqual(generator.ACTIVE_TAXONOMY, document["taxonomy"])
        self.assertEqual(11, len(document["rows"]))
        self.assertEqual(
            sorted(row["method_path_id"] for row in document["rows"]),
            [row["method_path_id"] for row in document["rows"]],
        )
        self.assertTrue(rendered.endswith("\n"))

    def test_cli_write_then_check_uses_explicit_paths(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = os.path.join(temporary, "coding.json")
            args = [
                "--profile", "v7",
                "--sidecar-dir", generator.ACTIVE_SIDECAR_DIR,
                "--out", output,
                "--taxonomy", "taxonomy-fixture.json",
            ]
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(0, generator.main(args))
                self.assertEqual(0, generator.main([*args, "--check"]))
            with io.open(output, encoding="utf-8") as handle:
                document = json.load(handle)
            self.assertEqual("taxonomy-fixture.json", document["taxonomy"])

    def test_cli_check_reports_a_missing_or_stale_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = os.path.join(temporary, "missing.json")
            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                result = generator.main([
                    "--profile", "v7",
                    "--sidecar-dir", generator.ACTIVE_SIDECAR_DIR,
                    "--out", output,
                    "--taxonomy", generator.ACTIVE_TAXONOMY,
                    "--check",
                ])
            self.assertEqual(1, result)
            self.assertIn("[FAIL]", stdout.getvalue())

    def test_invalid_profile_is_an_argparse_error(self):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as raised:
                generator.main(["--profile", "v8"])
        self.assertEqual(2, raised.exception.code)

    def test_missing_sidecar_directory_is_a_controlled_error(self):
        missing = os.path.join(HERE, "does-not-exist")
        with self.assertRaisesRegex(SystemExit, "no sidecars under"):
            generator.load_sidecars(missing)


if __name__ == "__main__":
    unittest.main()
