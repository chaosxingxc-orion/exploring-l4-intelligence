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
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import sf_coding_generator as generator  # noqa: E402


class InjectedStagingFile:
    """Binary staging-file proxy that injects an I/O failure."""

    def __init__(self, raw, failure):
        self.raw = raw
        self.failure = failure
        self.write_calls = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.raw.close()
        return False

    def write(self, payload):
        if self.failure == "partial-write":
            if self.write_calls:
                raise OSError("injected write failure after a partial write")
            self.write_calls += 1
            return self.raw.write(payload[:max(1, len(payload) // 2)])
        return self.raw.write(payload)

    def flush(self):
        self.raw.flush()
        if self.failure == "flush":
            raise OSError("injected flush failure")

    def fileno(self):
        return self.raw.fileno()


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
        with io.open(generator.LEGACY_OUT, "rb") as handle:
            expected = handle.read()
        self.assertEqual(expected, generator.render(sidecars).encode("utf-8"))

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
            self.assertEqual(["coding.json"], os.listdir(temporary))

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

    def test_cli_check_rejects_a_physically_different_crlf_file(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = os.path.join(temporary, "coding.json")
            payload = generator.render(
                generator.load_sidecars(generator.ACTIVE_SIDECAR_DIR),
                taxonomy=generator.ACTIVE_TAXONOMY,
                profile="v7",
            ).encode("utf-8")
            with io.open(output, "wb") as handle:
                handle.write(payload.replace(b"\n", b"\r\n"))
            with contextlib.redirect_stdout(io.StringIO()):
                result = generator.main([
                    "--profile", "v7",
                    "--sidecar-dir", generator.ACTIVE_SIDECAR_DIR,
                    "--out", output,
                    "--taxonomy", generator.ACTIVE_TAXONOMY,
                    "--check",
                ])
            self.assertEqual(1, result)

    def test_write_failures_preserve_or_omit_target_and_clean_staging(self):
        original_fdopen = os.fdopen
        for failure in ("partial-write", "flush", "replace"):
            for target_exists in (True, False):
                with self.subTest(failure=failure, target_exists=target_exists):
                    with tempfile.TemporaryDirectory() as temporary:
                        output = os.path.join(temporary, "coding.json")
                        original = b"existing-target-bytes\r\n"
                        if target_exists:
                            with io.open(output, "wb") as handle:
                                handle.write(original)
                        args = [
                            "--profile", "v7",
                            "--sidecar-dir", generator.ACTIVE_SIDECAR_DIR,
                            "--out", output,
                            "--taxonomy", generator.ACTIVE_TAXONOMY,
                        ]

                        def injected_fdopen(fd, mode):
                            return InjectedStagingFile(
                                original_fdopen(fd, mode), failure
                            )

                        if failure == "replace":
                            patcher = mock.patch.object(
                                generator.os,
                                "replace",
                                side_effect=OSError("injected replace failure"),
                            )
                        else:
                            patcher = mock.patch.object(
                                generator.os,
                                "fdopen",
                                side_effect=injected_fdopen,
                            )
                        with patcher, contextlib.redirect_stdout(io.StringIO()):
                            with self.assertRaises(OSError):
                                generator.main(args)

                        self.assertEqual(target_exists, os.path.exists(output))
                        if target_exists:
                            with io.open(output, "rb") as handle:
                                self.assertEqual(original, handle.read())
                        expected_entries = ["coding.json"] if target_exists else []
                        self.assertEqual(expected_entries, os.listdir(temporary))

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
