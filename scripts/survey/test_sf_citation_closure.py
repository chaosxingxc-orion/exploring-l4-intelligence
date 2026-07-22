import gzip
import io
import json
import tarfile
import tempfile
import unittest
from pathlib import Path

import sf_citation_closure as target


def _tar_blob(name: str, text: str) -> bytes:
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode="w:gz") as archive:
        payload = text.encode()
        info = tarfile.TarInfo(name)
        info.size = len(payload)
        archive.addfile(info, io.BytesIO(payload))
    return stream.getvalue()


class CitationClosureTests(unittest.TestCase):
    def test_extracts_unique_arxiv_ids_from_bibliography_members(self):
        blob = _tar_blob("refs.bib", "A 2401.00001v2 B 2401.00001 C 2502.12345")
        result = target.extract_backward_arxiv_ids(blob, "2607.00001")
        self.assertEqual(result["arxiv_ids"], ["2401.00001", "2502.12345"])
        self.assertEqual(result["scope"], "bbl/bib members")

    def test_falls_back_to_gzipped_tex(self):
        blob = gzip.compress(b"\\cite{X} arXiv:2301.01010")
        result = target.extract_backward_arxiv_ids(blob, "2607.00001")
        self.assertEqual(result["arxiv_ids"], ["2301.01010"])
        self.assertIn("all text members", result["scope"])

    def test_falls_back_to_raw_text(self):
        result = target.extract_backward_arxiv_ids(b"plain arXiv:2201.00001", "2607.00001")
        self.assertEqual(result["arxiv_ids"], ["2201.00001"])

    def test_run_preserves_forward_waiver_and_hashes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            store = root / "store" / "2607.00001"
            store.mkdir(parents=True)
            (store / "2607.00001.eprint").write_bytes(
                _tar_blob("x.bib", "@a{one, note={2401.00001}}")
            )
            targets = root / "targets.json"
            targets.write_text(json.dumps({"targets": [{
                "arxiv_id": "2607.00001", "title": "T", "role": "KEEP_CORE"
            }]}), encoding="utf-8")
            known = root / "known.jsonl"
            known.write_text(json.dumps({"arxiv_id": "2401.00001"}) + "\n", encoding="utf-8")
            output = root / "ledger.jsonl"
            summary = root / "summary.json"
            result = target.run(targets, store.parent, [known], output, summary)
            row = json.loads(output.read_text("utf-8"))
            self.assertEqual(row["backward_status"], "EXECUTED_ARXIV_ID_SUBSET")
            self.assertEqual(row["known_backward_ids"], ["2401.00001"])
            self.assertEqual(row["forward_status"], "WAIVED_PUBLIC_INDEX_RATE_LIMITED")
            self.assertEqual(result["targets"], 1)
            self.assertEqual(len(result["ledger_sha256"]), 64)

    def test_missing_eprint_and_duplicate_targets_are_explicit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            targets = root / "targets.json"
            targets.write_text(json.dumps({"targets": [{
                "arxiv_id": "2607.00001", "title": "Missing", "role": "KEEP_CORE"
            }]}), encoding="utf-8")
            output = root / "ledger.jsonl"
            summary = root / "summary.json"
            result = target.run(targets, root / "store", [root / "absent.jsonl"], output, summary)
            self.assertEqual(result["unresolved_targets"], 1)
            self.assertEqual(json.loads(output.read_text("utf-8"))["backward_status"], "EPRINT_MISSING")
            targets.write_text(json.dumps({"targets": [
                {"arxiv_id": "2607.00001"}, {"arxiv_id": "2607.00001"}
            ]}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate"):
                target.run(targets, root / "store", [], output, summary)


if __name__ == "__main__":
    unittest.main()
