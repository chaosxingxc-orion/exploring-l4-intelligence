#!/usr/bin/env python3
"""Tests for the Stage-1B arXiv query executor.

User journey: as the mapping coordinator, I can execute frozen compiler rows,
retain byte-identical Atom responses, append one REC-1 row per page, and resume
without issuing a duplicate network request.
"""

import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import sf_arxiv_query_runner as runner


ATOM = b"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"
      xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">
  <opensearch:totalResults>2</opensearch:totalResults>
  <opensearch:startIndex>0</opensearch:startIndex>
  <opensearch:itemsPerPage>2</opensearch:itemsPerPage>
  <entry><id>http://arxiv.org/abs/2607.00002v1</id><title>Second paper</title></entry>
  <entry><id>https://arxiv.org/abs/2607.00001v2</id><title>First paper</title></entry>
</feed>
"""


def atom(total, start=0, ids=()):
    entries = "".join(
        f"<entry><id>https://arxiv.org/abs/{paper_id}v1</id><title>x</title></entry>"
        for paper_id in ids
    )
    return (
        '<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom" '
        'xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">'
        f"<opensearch:totalResults>{total}</opensearch:totalResults>"
        f"<opensearch:startIndex>{start}</opensearch:startIndex>"
        f"<opensearch:itemsPerPage>{len(ids)}</opensearch:itemsPerPage>"
        f"{entries}</feed>"
    ).encode()


def frozen_row():
    row = {
        "query_id": "SF-L1-Q1",
        "lane": "SF-L1",
        "decoded_search_query": (
            "cat:cs.AI AND submittedDate:[202607010000 TO 202607152359] "
            "AND abs:agent"
        ),
        "url_encoded_search_query": (
            "cat%3Acs.AI%20AND%20submittedDate%3A%5B202607010000%20TO%20"
            "202607152359%5D%20AND%20abs%3Aagent"
        ),
        "categories": ["cs.AI"],
        "date_from": "202607010000",
        "date_to": "202607152359",
        "start": 0,
        "max_results": 2,
        "sortBy": "relevance",
        "sortOrder": "descending",
        "compiler_version": "test",
    }
    row["record_sha256"] = runner.compute_record_hash(row)
    return row


class FrozenRowTests(unittest.TestCase):
    def test_rejects_changed_frozen_row(self):
        row = frozen_row()
        row["sortOrder"] = "ascending"
        with self.assertRaisesRegex(ValueError, "record_sha256"):
            runner.validate_frozen_row(row)

    def test_atom_parser_returns_total_and_canonical_ids(self):
        parsed = runner.parse_atom_page(ATOM)
        self.assertEqual(parsed["total_results"], 2)
        self.assertEqual(parsed["start_index"], 0)
        self.assertEqual(parsed["items_per_page"], 2)
        self.assertEqual(parsed["ids"], ["2607.00002", "2607.00001"])

    def test_load_rows_accepts_valid_file_and_rejects_duplicate_id(self):
        row = frozen_row()
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "queries.jsonl"
            path.write_text(json.dumps(row) + "\n", "utf-8")
            self.assertEqual(runner.load_frozen_rows(path)[0]["query_id"], "SF-L1-Q1")
            path.write_text(json.dumps(row) + "\n" + json.dumps(row) + "\n", "utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate frozen query_id"):
                runner.load_frozen_rows(path)

    def test_build_url_preserves_all_request_controls(self):
        url = runner.build_url("cat:cs.AI AND abs:agent", 75, 25, "submittedDate", "ascending")
        self.assertIn("search_query=cat%3Acs.AI%20AND%20abs%3Aagent", url)
        self.assertIn("start=75&max_results=25", url)
        self.assertTrue(url.endswith("sortBy=submittedDate&sortOrder=ascending"))

    def test_network_transport_retries_and_returns_failure(self):
        with mock.patch.object(runner.urllib.request, "urlopen", side_effect=TimeoutError("x")), \
             mock.patch.object(runner.time, "sleep") as sleeper:
            status, body, attempts, error = runner.network_transport("https://example.invalid")
        self.assertIsNone(status)
        self.assertEqual(body, b"")
        self.assertEqual(attempts, runner.MAX_ATTEMPTS)
        self.assertIn("TimeoutError", error)
        self.assertEqual(sleeper.call_count, runner.MAX_ATTEMPTS - 1)


class ExecutionTests(unittest.TestCase):
    def test_executes_logs_hashes_and_resumes_without_network(self):
        row = frozen_row()
        calls = []

        def transport(url):
            calls.append(url)
            return 200, ATOM, 1, None

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            rec1 = root / "rec1.jsonl"
            raw = root / "raw"
            summary = runner.execute_rows(
                [row], rec1, raw, transport=transport, sleep=lambda _: None
            )
            self.assertEqual(summary["pages_written"], 1)
            self.assertEqual(summary["unique_hits"], 2)
            self.assertEqual(len(calls), 1)

            records = [json.loads(line) for line in rec1.read_text("utf-8").splitlines()]
            self.assertEqual(records[0]["query_id"], "SF-L1-Q1")
            self.assertEqual(records[0]["query_ref"], row["record_sha256"])
            self.assertEqual(records[0]["response_sha256"], hashlib.sha256(ATOM).hexdigest())
            self.assertEqual(records[0]["included"], ["2607.00002", "2607.00001"])
            self.assertEqual((raw / "SF-L1-Q1" / "start-000000.atom").read_bytes(), ATOM)

            resumed = runner.execute_rows(
                [row], rec1, raw, transport=transport, sleep=lambda _: None
            )
            self.assertEqual(resumed["pages_written"], 0)
            self.assertEqual(resumed["pages_skipped"], 1)
            self.assertEqual(len(calls), 1)

    def test_paginates_until_total_results_is_exhausted(self):
        row = frozen_row()
        row["max_results"] = 1
        row["record_sha256"] = runner.compute_record_hash(
            {k: v for k, v in row.items() if k != "record_sha256"}
        )
        pages = {
            0: ATOM.replace(b"<opensearch:itemsPerPage>2", b"<opensearch:itemsPerPage>1")
                   .replace(
                       b"  <entry><id>https://arxiv.org/abs/2607.00001v2</id><title>First paper</title></entry>\n",
                       b"",
                   ),
            1: ATOM.replace(b"<opensearch:startIndex>0", b"<opensearch:startIndex>1")
                   .replace(b"<opensearch:itemsPerPage>2", b"<opensearch:itemsPerPage>1")
                   .replace(
                       b"  <entry><id>http://arxiv.org/abs/2607.00002v1</id><title>Second paper</title></entry>\n",
                       b"",
                   ),
        }

        def transport(url):
            start = int(url.split("start=", 1)[1].split("&", 1)[0])
            return 200, pages[start], 1, None

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            summary = runner.execute_rows(
                [row], root / "rec1.jsonl", root / "raw",
                transport=transport, sleep=lambda _: None,
            )
            self.assertEqual(summary["pages_written"], 2)
            self.assertEqual(summary["unique_hits"], 2)

    def test_failed_request_is_logged_and_stops_the_query(self):
        row = frozen_row()

        def transport(_url):
            return None, b"", 4, "TimeoutError: timed out"

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            summary = runner.execute_rows(
                [row], root / "rec1.jsonl", root / "raw",
                transport=transport, sleep=lambda _: None,
            )
            record = json.loads((root / "rec1.jsonl").read_text("utf-8"))
            self.assertEqual(summary["failed_requests"], 1)
            self.assertEqual(record["failed_request"], "TimeoutError: timed out")
            self.assertEqual(record["included"], [])

    def test_overflow_splits_by_day_and_logs_every_probe(self):
        row = frozen_row()
        calls = []

        def transport(url):
            calls.append(url)
            if len(calls) == 1:
                return 200, atom(2001), 1, None
            return 200, atom(0), 1, None

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            summary = runner.execute_rows(
                [row], root / "rec1.jsonl", root / "raw",
                transport=transport, sleep=lambda _: None,
            )
            records = [
                json.loads(line)
                for line in (root / "rec1.jsonl").read_text("utf-8").splitlines()
            ]
        self.assertEqual(summary["split_probes_written"], 15)
        self.assertEqual(summary["failed_requests"], 0)
        self.assertEqual(len(records), 31)
        self.assertEqual(
            sum(record["request_role"] == "RESULT_PAGE" for record in records), 16
        )

    def test_duplicate_existing_rec1_key_fails_closed(self):
        duplicate = {
            "query_id": "SF-L1-Q1",
            "page_start": 0,
            "request_role": "RESULT_PAGE",
        }
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "rec1.jsonl"
            path.write_text(json.dumps(duplicate) + "\n" + json.dumps(duplicate) + "\n", "utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate REC-1 key"):
                runner.execute_rows([], path, Path(temporary) / "raw")

    def test_execution_metadata_binds_commit_protocol_queries_and_h5_hold(self):
        row = frozen_row()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            query_path = root / "queries.jsonl"
            output = root / "metadata.json"
            query_path.write_text(json.dumps(row) + "\n", "utf-8")
            with mock.patch.object(runner, "_git_head", return_value="a" * 40):
                runner.write_execution_metadata(output, query_path, [row], "test actor")
            metadata = json.loads(output.read_text("utf-8"))
        self.assertEqual(metadata["execution_commit"], "a" * 40)
        self.assertEqual(metadata["selected_query_ids"], ["SF-L1-Q1"])
        self.assertEqual(metadata["h5_load_bearing_use"], "WITHHOLD")
        self.assertEqual(metadata["research_model_or_smoke_executions"], 0)

    def test_retry_failed_page_appends_supersession_and_continues_pagination(self):
        row = frozen_row()
        failed = {
            "query_id": row["query_id"],
            "engine": "arxiv_api",
            "query_ref": row["record_sha256"],
            "request_role": "RESULT_PAGE",
            "page_start": 0,
            "max_results": 1,
            "totalResults": None,
            "sortBy": "relevance",
            "sortOrder": "descending",
            "timestamp": "2026-07-21T00:00:00Z",
            "request_url": runner.build_url(
                row["decoded_search_query"], 0, 1, "relevance", "descending"
            ),
            "raw_response_ref": None,
            "response_sha256": None,
            "http_status": None,
            "attempts": 4,
            "n_hits_page": 0,
            "included": [],
            "excluded": [],
            "failed_request": "TimeoutError",
            "access_class": "SYSTEMATIC_DISCOVERY_QUERY",
        }
        calls = []

        def transport(url):
            start = int(url.split("start=", 1)[1].split("&", 1)[0])
            calls.append(start)
            return 200, atom(2, start, [f"2607.0000{start + 1}"]), 1, None

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            rec1 = root / "rec1.jsonl"
            rec1.write_text(json.dumps(failed) + "\n", "utf-8")
            summary = runner.retry_failed_pages(
                rec1, root / "raw", transport=transport, sleep=lambda _: None
            )
            records = [json.loads(line) for line in rec1.read_text("utf-8").splitlines()]
            repeated = runner.retry_failed_pages(
                rec1, root / "raw", transport=transport, sleep=lambda _: None
            )

        self.assertEqual(summary["failures_selected"], 1)
        self.assertEqual(summary["pages_written"], 2)
        self.assertEqual(calls, [0, 1])
        self.assertEqual(records[1]["request_role"], "RESULT_PAGE_RETRY_1")
        self.assertEqual(records[1]["retry_of_timestamp"], failed["timestamp"])
        self.assertEqual(records[2]["page_start"], 1)
        self.assertEqual(repeated["failures_selected"], 0)


if __name__ == "__main__":
    unittest.main()
