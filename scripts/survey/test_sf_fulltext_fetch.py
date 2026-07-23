#!/usr/bin/env python3
"""Tests for full-text fetch ordering controls."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))

import sf_fulltext_fetch as fetcher


class FulltextFetchTests(unittest.TestCase):
    def test_data_root_normalization_preserves_wsl_mount_and_translates_only_on_windows(self):
        wsl_path = "/mnt/e/chao_workspace/exploring-l4-intelligence/speechrl-data"
        self.assertEqual(wsl_path, fetcher._normalize_data_root(wsl_path, platform="posix"))
        self.assertEqual(
            "E:/chao_workspace/exploring-l4-intelligence/speechrl-data",
            fetcher._normalize_data_root(wsl_path, platform="nt"),
        )

    def test_pdf_validation_rejects_html_error_pages(self):
        self.assertTrue(fetcher.valid_body("pdf", b"%PDF-1.7\n" + b"x" * 2048))
        self.assertFalse(fetcher.valid_body("pdf", b"<html>error</html>" + b"x" * 2048))

    def test_pdf_first_pass_selects_only_pdf_rendition(self):
        parsed = fetcher.parse_cli(["fetch.py", "--rendition", "pdf", "2601.00001"])
        self.assertEqual(parsed["ids"], ["2601.00001"])
        self.assertEqual(parsed["renditions"], (("pdf", "https://arxiv.org/pdf/{aid}"),))

    def test_default_retains_both_renditions(self):
        parsed = fetcher.parse_cli(["fetch.py", "2601.00001"])
        self.assertEqual(parsed["renditions"], fetcher.RENDITIONS)

    def test_invalid_rendition_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "rendition"):
            fetcher.parse_cli(["fetch.py", "--rendition", "html", "2601.00001"])

    def test_help_and_invalid_id_never_issue_a_network_request(self):
        with mock.patch.object(fetcher, "fetch") as network:
            self.assertEqual(fetcher.main(["fetch.py", "--help"]), 0)
            self.assertEqual(fetcher.main(["fetch.py", "--bogus"]), 2)
        network.assert_not_called()

    def test_cli_rejects_malformed_arxiv_identity(self):
        with self.assertRaisesRegex(ValueError, "invalid arXiv ID"):
            fetcher.parse_cli(["fetch.py", "not-an-id"])

    def test_fetch_retries_and_main_records_success_skip_and_failure(self):
        response = mock.MagicMock()
        response.__enter__.return_value.status = 200
        response.__enter__.return_value.read.return_value = b"pdf-bytes"
        with mock.patch.object(fetcher.urllib.request, "urlopen", return_value=response):
            status, body, attempts, error = fetcher.fetch("https://example.test/paper")
        self.assertEqual((status, body, attempts, error), (200, b"pdf-bytes", 1, None))
        with mock.patch.object(fetcher.urllib.request, "urlopen", side_effect=OSError("offline")), mock.patch.object(
            fetcher.shutil, "which", return_value=None
        ), mock.patch.object(fetcher.time, "sleep"):
            status, body, attempts, error = fetcher.fetch("https://example.test/paper")
        self.assertIsNone(status)
        self.assertEqual(attempts, fetcher.MAX_ATTEMPTS)
        self.assertIn("offline", error)

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            ledger = root / "ledger.jsonl"
            with mock.patch.object(fetcher, "DEFAULT_DATA_DIR", str(root)), mock.patch.object(
                fetcher, "LEDGER", str(ledger)
            ), mock.patch.object(fetcher, "fetch", return_value=(200, b"%PDF-1.7\n" + b"x" * 2048, 1, None)), mock.patch.object(
                fetcher.time, "sleep"
            ):
                self.assertEqual(fetcher.main(["fetch.py", "--rendition", "pdf", "2601.00001"]), 0)
                self.assertEqual(fetcher.main(["fetch.py", "--rendition", "pdf", "2601.00001"]), 0)
            self.assertTrue((root / "survey-fulltext" / "2601.00001" / "2601.00001.pdf").is_file())
            with mock.patch.object(fetcher, "DEFAULT_DATA_DIR", str(root)), mock.patch.object(
                fetcher, "LEDGER", str(ledger)
            ), mock.patch.object(fetcher, "fetch", return_value=(None, b"", 4, "offline")), mock.patch.object(
                fetcher.time, "sleep"
            ):
                self.assertEqual(fetcher.main(["fetch.py", "--rendition", "pdf", "2601.00002"]), 1)

    def test_fetch_uses_curl_fallback_after_python_tls_failure(self):
        completed = mock.MagicMock(returncode=0, stdout=b"x" * 2048, stderr=b"")
        with mock.patch.object(fetcher.urllib.request, "urlopen", side_effect=OSError("tls eof")), mock.patch.object(
            fetcher.shutil, "which", return_value="curl"
        ), mock.patch.object(fetcher.subprocess, "run", return_value=completed), mock.patch.object(fetcher.time, "sleep"):
            status, body, attempts, error = fetcher.fetch("https://example.test/paper")
        self.assertEqual(status, 200)
        self.assertEqual(len(body), 2048)
        self.assertEqual(attempts, 2)
        self.assertIsNone(error)


if __name__ == "__main__":
    unittest.main(verbosity=2)
