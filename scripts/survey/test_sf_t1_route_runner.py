#!/usr/bin/env python3
"""Tests for the bounded Stage-1B T1 proceedings collector."""

from __future__ import annotations

import hashlib
import io
import json
import sys
import tempfile
import unittest
import urllib.error
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))

import sf_t1_route_runner as runner


WORDLIST = {
    "groups": {
        "A": ["training-free", "agent"],
        "B": ["speech", "multimodal"],
        "C": ["routing", "memory"],
    }
}


def route(**changes):
    row = {
        "route_id": "SF-T1R-ACL-2025",
        "venue_code": "ACL",
        "year": 2025,
        "status": "READY",
        "entry_status": "EXACT_URL",
        "entry_url": "https://example.test/acl-2025/",
        "entry_pattern": None,
        "entry_resolve_rule": None,
    }
    row.update(changes)
    return row


class MatchingTests(unittest.TestCase):
    def test_normalization_and_match_rule_are_dual_side_and_boundary_aware(self):
        compiled = runner.compile_wordlist(WORDLIST)
        self.assertEqual(runner.normalize("Training_Free  Agent"), "training free agent")
        self.assertTrue(runner.match_title("A Training-Free Agent", compiled)["matched"])
        self.assertTrue(
            runner.match_title("Multimodal Memory for Reasoning", compiled)["matched"]
        )
        self.assertFalse(runner.match_title("Speech Recognition", compiled)["matched"])
        self.assertFalse(runner.match_title("Reagent Design", compiled)["matched"])

    def test_family_extractors_only_return_paper_links(self):
        acl = b"""
        <a href='/2025.acl-long.1/'>Training-Free Agents for Speech</a>
        <a href='/events/acl-2025/'>ACL 2025</a>
        """
        cvf = b"""
        <a href='papers/X_paper.html'>Multimodal Memory Routing</a>
        <a href='menu.html'>Program</a>
        """
        self.assertEqual(
            runner.extract_titles(acl, "ACL", 2025),
            ["Training-Free Agents for Speech"],
        )
        self.assertEqual(
            runner.extract_titles(cvf, "CVPR", 2025),
            ["Multimodal Memory Routing"],
        )

        families = {
            "NEURIPS": b"<a href='/paper_files/paper/2025/hash/x-Abstract-Conference.html'>Agent Search</a>",
            "ICML": b"<div class='paper'><p class='title'>Verifier Routing</p><a href='paper.html'>abs</a></div>",
            "IS": b"<a href='paper25_interspeech.html'><p>Speech Memory<br><span>Author Name</span></p></a>",
        }
        for venue, payload in families.items():
            with self.subTest(venue=venue):
                expected = {
                    "NEURIPS": "Agent Search",
                    "ICML": "Verifier Routing",
                    "IS": "Speech Memory",
                }[venue]
                self.assertEqual(runner.extract_titles(payload, venue, 2025), [expected])

    def test_effective_url_requests_the_all_papers_cvf_page(self):
        self.assertEqual(
            runner.effective_entry_url("https://openaccess.thecvf.com/CVPR2025", "CVPR"),
            "https://openaccess.thecvf.com/CVPR2025?day=all",
        )
        self.assertEqual(
            runner.effective_entry_url("https://aclanthology.org/events/acl-2025/", "ACL"),
            "https://aclanthology.org/events/acl-2025/",
        )


class CollectionTests(unittest.TestCase):
    def test_success_persists_raw_hash_counts_and_matches(self):
        body = b"<a href='/2025.acl-long.1/'>Training-Free Agents for Speech</a>"

        def transport(_url):
            return 200, body, 1, None

        with tempfile.TemporaryDirectory() as temporary:
            result = runner.collect_route(
                route(),
                runner.compile_wordlist(WORDLIST),
                Path(temporary),
                transport=transport,
            )
            raw = Path(result["raw_toc_ref"])
            self.assertTrue(raw.is_file())
            self.assertEqual(result["raw_toc_sha256"], hashlib.sha256(body).hexdigest())
        self.assertEqual(result["disposition"], "EXECUTED")
        self.assertEqual(result["n_titles_total"], 1)
        self.assertEqual(result["n_matched"], 1)
        self.assertEqual(result["matched_titles"][0]["title"], "Training-Free Agents for Speech")

    def test_reuses_registered_raw_toc_without_another_network_request(self):
        body = b"<a href='/2025.acl-long.1/'>Training-Free Agents for Speech</a>"
        with tempfile.TemporaryDirectory() as temporary:
            raw_dir = Path(temporary)
            (raw_dir / "SF-T1R-ACL-2025.html").write_bytes(body)
            result = runner.collect_route(
                route(),
                runner.compile_wordlist(WORDLIST),
                raw_dir,
                transport=lambda _url: self.fail("network must not be called"),
                reuse_raw=True,
            )
        self.assertEqual(result["disposition"], "EXECUTED")
        self.assertEqual(result["attempts"], 0)
        self.assertTrue(result["raw_reused"])

    def test_not_held_and_unavailable_are_explicit_dispositions(self):
        calls = []

        def transport(url):
            calls.append(url)
            return None, b"", 2, "TimeoutError"

        not_held = runner.collect_route(
            route(status="NOT_HELD", entry_status="NOT_APPLICABLE", entry_url=None),
            runner.compile_wordlist(WORDLIST),
            Path("unused"),
            transport=transport,
        )
        self.assertEqual(not_held["disposition"], "NOT_HELD")
        self.assertEqual(calls, [])

        with tempfile.TemporaryDirectory() as temporary:
            unavailable = runner.collect_route(
                route(),
                runner.compile_wordlist(WORDLIST),
                Path(temporary),
                transport=transport,
            )
        self.assertEqual(unavailable["disposition"], "WAIVED_UNAVAILABLE")
        self.assertEqual(unavailable["failure_code"], "TimeoutError")
        self.assertIsNone(unavailable["n_matched"])

    def test_http_success_without_parseable_titles_is_not_zero_hit(self):
        with tempfile.TemporaryDirectory() as temporary:
            result = runner.collect_route(
                route(),
                runner.compile_wordlist(WORDLIST),
                Path(temporary),
                transport=lambda _url: (200, b"<html>javascript shell</html>", 1, None),
            )
        self.assertEqual(result["disposition"], "WAIVED_UNAVAILABLE")
        self.assertEqual(result["failure_code"], "NO_PARSEABLE_TITLES")
        self.assertIsNone(result["n_matched"])

    def test_entry_to_resolve_records_failed_resolution_instead_of_guessing(self):
        unresolved = route(
            route_id="SF-T1R-MM-2025",
            venue_code="MM",
            entry_status="ENTRY_TO_RESOLVE",
            entry_url=None,
            entry_pattern="conference hub -> proceedings DOI",
            entry_resolve_rule="resolve from official hub",
        )
        with tempfile.TemporaryDirectory() as temporary:
            result = runner.collect_route(
                unresolved,
                runner.compile_wordlist(WORDLIST),
                Path(temporary),
                transport=lambda _url: (200, b"<html>no 2025 proceedings link</html>", 1, None),
            )
        self.assertEqual(result["disposition"], "WAIVED_UNAVAILABLE")
        self.assertEqual(result["failure_code"], "ENTRY_RESOLUTION_FAILED")

    def test_entry_to_resolve_uses_one_official_candidate(self):
        unresolved = route(
            route_id="SF-T1R-MM-2025",
            venue_code="MM",
            entry_status="ENTRY_TO_RESOLVE",
            entry_url=None,
        )
        hub = b"<a href='/doi/proceedings/10.1145/123'>ACM MM 2025</a>"
        toc = b"<html>official TOC shell</html>"
        calls = []

        def transport(url):
            calls.append(url)
            return (200, hub, 1, None) if len(calls) == 1 else (200, toc, 1, None)

        with tempfile.TemporaryDirectory() as temporary:
            result = runner.collect_route(
                unresolved,
                runner.compile_wordlist(WORDLIST),
                Path(temporary),
                transport=transport,
            )
        self.assertEqual(result["failure_code"], "NO_PARSEABLE_TITLES")
        self.assertEqual(result["resolved_entry_url"], "https://dl.acm.org/doi/proceedings/10.1145/123")
        self.assertEqual(len(calls), 2)

    def test_network_transport_success_terminal_http_and_bounded_retry(self):
        response = mock.MagicMock()
        response.status = 200
        response.read.return_value = b"ok"
        response.__enter__.return_value = response
        response.__exit__.return_value = False
        with mock.patch.object(runner.urllib.request, "urlopen", return_value=response):
            self.assertEqual(runner.network_transport("https://example.test"), (200, b"ok", 1, None))

        not_found = urllib.error.HTTPError("https://example.test", 404, "not found", {}, None)
        with mock.patch.object(runner.urllib.request, "urlopen", side_effect=not_found):
            status, body, attempts, error = runner.network_transport("https://example.test")
        self.assertEqual((status, body, attempts, error), (404, b"", 1, "HTTP_404"))

        with mock.patch.object(runner.urllib.request, "urlopen", side_effect=TimeoutError("slow")), \
             mock.patch.object(runner.time, "sleep") as sleeper:
            status, body, attempts, error = runner.network_transport("https://example.test")
        self.assertIsNone(status)
        self.assertEqual(body, b"")
        self.assertEqual(attempts, runner.MAX_ATTEMPTS)
        self.assertIn("TimeoutError", error)
        self.assertEqual(sleeper.call_count, 1)

    def test_write_report_is_deterministic_and_summarizes_50_dispositions(self):
        rows = [
            {"route_id": f"R{i:02d}", "disposition": "EXECUTED", "n_titles_total": 2, "n_matched": 1}
            for i in range(47)
        ] + [
            {"route_id": "N1", "disposition": "NOT_HELD", "n_titles_total": 0, "n_matched": 0},
            {"route_id": "N2", "disposition": "WAIVED_UNAVAILABLE", "n_titles_total": None, "n_matched": None},
            {"route_id": "N3", "disposition": "WAIVED_UNAVAILABLE", "n_titles_total": None, "n_matched": None},
        ]
        with tempfile.TemporaryDirectory() as temporary:
            one = Path(temporary) / "one.json"
            two = Path(temporary) / "two.json"
            report = runner.write_report(one, rows, "routes-sha", "words-sha")
            runner.write_report(two, rows, "routes-sha", "words-sha")
            self.assertEqual(one.read_bytes(), two.read_bytes())
            persisted = json.loads(one.read_text("utf-8"))
        self.assertEqual(report["summary"]["routes_dispositioned"], 50)
        self.assertEqual(persisted["summary"]["executed"], 47)
        self.assertEqual(persisted["summary"]["waived_unavailable"], 2)

    def test_merge_rows_replaces_only_registered_route_ids(self):
        base = [{"route_id": f"R{i:02d}", "disposition": "WAIVED_UNAVAILABLE"} for i in range(50)]
        replacement = [{"route_id": "R07", "disposition": "EXECUTED"}]
        merged = runner.merge_rows(base, replacement)
        self.assertEqual(len(merged), 50)
        self.assertEqual(merged[7]["disposition"], "EXECUTED")
        with self.assertRaisesRegex(ValueError, "not present"):
            runner.merge_rows(base, [{"route_id": "UNKNOWN", "disposition": "EXECUTED"}])

    def test_cli_dispositions_exactly_50_registered_not_held_routes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            routes = root / "routes.jsonl"
            words = root / "words.json"
            output = root / "report.json"
            rows = [
                route(
                    route_id=f"R{i:02d}",
                    status="NOT_HELD",
                    entry_status="NOT_APPLICABLE",
                    entry_url=None,
                )
                for i in range(50)
            ]
            routes.write_text("".join(json.dumps(row) + "\n" for row in rows), "utf-8")
            words.write_text(json.dumps(WORDLIST), "utf-8")
            argv = [
                "sf_t1_route_runner.py",
                "--routes", str(routes),
                "--wordlist", str(words),
                "--raw-dir", str(root / "raw"),
                "--output", str(output),
            ]
            with mock.patch.object(sys, "argv", argv), \
                 mock.patch.object(runner.time, "sleep"), \
                 redirect_stdout(io.StringIO()):
                self.assertEqual(runner.main(), 0)
            report = json.loads(output.read_text("utf-8"))
        self.assertEqual(report["summary"]["routes_dispositioned"], 50)
        self.assertEqual(report["summary"]["not_held"], 50)


if __name__ == "__main__":
    unittest.main(verbosity=2)
