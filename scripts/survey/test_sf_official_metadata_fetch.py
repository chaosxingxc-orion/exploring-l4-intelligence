#!/usr/bin/env python3
"""Offline-first contracts for official metadata caching."""
from __future__ import annotations

import contextlib
import io
import inspect
import json
import subprocess
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import sf_bibliography_generator as bibliography  # noqa: E402
import sf_official_metadata_fetch as fetcher  # noqa: E402


class OfficialMetadataFetchTest(unittest.TestCase):
    def test_arxiv_https_abs_fallback_parses_official_citation_metadata(self):
        raw = b"""<!doctype html><html><head>
        <meta name="citation_title" content="Fallback Title">
        <meta name="citation_author" content="First Author">
        <meta name="citation_author" content="Second Author">
        <meta name="citation_date" content="2025/10/01">
        <meta name="citation_arxiv_id" content="2510.00743">
        </head></html>"""
        policy = {
            "identity": {"kind": "arxiv", "id": "2510.00743"},
            "reference_role": "MEASUREMENT_INSTRUMENT",
            "chain": "TRAINING_FREE_AND_TRAINED_BOUNDARIES",
            "direct_neighbor": False,
            "next_action": "retain",
            "load_bearing": True,
            "access_class": "REVIEW_CLAIM_VERIFICATION",
            "source_locator": "review:200",
        }
        with tempfile.TemporaryDirectory(dir=bibliography.ROOT) as temporary, mock.patch.object(
            fetcher,
            "fetch",
            return_value=(raw, "2026-07-23T00:00:00Z"),
        ):
            row = fetcher.fetch_arxiv_html(policy, Path(temporary))
        self.assertEqual("Fallback Title", row["normalized"]["title"])
        self.assertEqual(["First Author", "Second Author"], row["normalized"]["authors"])
        self.assertEqual("https://arxiv.org/abs/2510.00743", row["normalized"]["stable_url"])
        self.assertEqual("https://arxiv.org/abs/2510.00743", row["official_url"])

    def test_fetch_success_and_bounded_failure(self):
        class Response:
            status = 200

            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            @staticmethod
            def read():
                return b"official bytes"

        with mock.patch.object(fetcher.urllib.request, "urlopen", return_value=Response()), mock.patch.object(
            fetcher.time, "sleep"
        ):
            body, accessed = fetcher.fetch("https://official.invalid/id", pause_seconds=0)
        self.assertEqual(b"official bytes", body)
        self.assertRegex(accessed, r"^20\d{2}-")

        with mock.patch.object(
            fetcher.urllib.request,
            "urlopen",
            side_effect=urllib.error.URLError("offline"),
        ), mock.patch.object(fetcher.time, "sleep"):
            with self.assertRaisesRegex(RuntimeError, "after 3 attempts"):
                fetcher.fetch("https://official.invalid/fail", pause_seconds=0)

    def test_endpoint_fetch_helpers_parse_and_freeze_raw_bytes(self):
        policies = bibliography.all_policies()
        samples = [
            (
                fetcher.fetch_arxiv_oai,
                policies["2310.04406"],
                bibliography.RAW_DIR / "arxiv-oai-2310.04406.xml",
            ),
            (
                fetcher.fetch_acl,
                policies["2025.emnlp-main.931"],
                bibliography.RAW_DIR / "acl-2025.emnlp-main.931.bib",
            ),
            (
                fetcher.fetch_github,
                policies["sierra-research/tau2-bench"],
                bibliography.RAW_DIR / "github-sierra-research--tau2-bench.json",
            ),
        ]
        with tempfile.TemporaryDirectory(dir=bibliography.ROOT) as temporary:
            raw_dir = Path(temporary)
            for helper, policy, source in samples:
                with self.subTest(identity=policy["identity"]):
                    with mock.patch.object(
                        fetcher,
                        "fetch",
                        return_value=(source.read_bytes(), "2026-07-20T00:00:00Z"),
                    ), contextlib.redirect_stdout(io.StringIO()):
                        row = helper(policy, raw_dir)
                    self.assertEqual(policy["identity"], row["identity"])
                    self.assertTrue((bibliography.ROOT / row["raw"]["path"]).is_file())

    def test_offline_rebuild_resolves_all_135_without_network(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "receipts.jsonl"
            with mock.patch.object(
                fetcher,
                "fetch",
                side_effect=AssertionError("offline mode attempted network access"),
            ):
                with contextlib.redirect_stdout(io.StringIO()):
                    result = fetcher.main(["--offline", "--output", str(output)])
            self.assertEqual(0, result)
            rows = [
                json.loads(line)
                for line in output.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertEqual(135, len(rows))
            self.assertEqual([], bibliography.validate_receipts(rows))

    def test_cached_raw_inventory_is_17_reused_plus_118_current(self):
        rows = bibliography.load_receipts()
        legacy = {
            row["raw"]["path"]
            for row in rows
            if row["raw"]["path"].startswith("docs/survey-provenance/atom/")
        }
        current = {
            row["raw"]["path"]
            for row in rows
            if row["raw"]["path"].startswith(
                "wiki/survey/current/data/official-metadata/"
            )
        }
        self.assertEqual(17, len(legacy))
        self.assertEqual(118, len(current))

    def test_current_raw_payloads_are_exempt_from_git_text_normalization(self):
        representative = next(
            row["raw"]["path"]
            for row in bibliography.load_receipts()
            if row["raw"]["path"].startswith(
                "wiki/survey/current/data/official-metadata/"
            )
        )
        result = subprocess.run(
            ["git", "check-attr", "text", "--", representative],
            cwd=bibliography.ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(f"{representative}: text: unset", result.stdout.strip())

    def test_fetcher_contains_no_discovery_or_fulltext_download_endpoint(self):
        source = inspect.getsource(fetcher)
        self.assertNotIn("search_query", source)
        self.assertNotIn("/pdf/", source)
        self.assertNotIn("/e-print/", source)
        self.assertIn("oai:ArXiv.org".casefold(), source.casefold())

    def test_offline_with_empty_raw_cache_fails_without_network(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "receipts.jsonl"
            raw_dir = root / "raw"
            with mock.patch.object(
                fetcher,
                "fetch",
                side_effect=AssertionError("offline mode attempted network access"),
            ):
                with contextlib.redirect_stdout(io.StringIO()):
                    result = fetcher.main(
                        [
                            "--offline",
                            "--output",
                            str(output),
                            "--raw-dir",
                            str(raw_dir),
                        ]
                    )
            self.assertEqual(1, result)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
