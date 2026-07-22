import json
import tempfile
import unittest
from pathlib import Path

import sf_delta_rec0_closeout as target


class DeltaRec0CloseoutTests(unittest.TestCase):
    def test_build_decisions_is_exhaustive_and_does_not_duplicate_known_work(self):
        candidates = [
            {"arxiv_id": "2607.00001", "title": "New", "abstract": "a"},
            {"arxiv_id": "2607.00002", "title": "Known", "abstract": "b"},
            {"arxiv_id": "2607.00003", "title": "Other", "abstract": "c"},
        ]
        selections = {
            "2607.00001": {
                "role": "KEEP_TRANSFER",
                "family": "routing",
                "reason": "changes the routing map",
            }
        }
        rows = target.build_decisions(candidates, selections, {"2607.00002"})
        self.assertEqual([row["arxiv_id"] for row in rows], [
            "2607.00001", "2607.00002", "2607.00003"
        ])
        self.assertEqual(rows[0]["abstract_disposition"], "SELECT_FULLTEXT")
        self.assertEqual(rows[1]["abstract_disposition"], "DUPLICATE_KNOWN_WORK")
        self.assertEqual(rows[2]["abstract_disposition"], "EXCLUDE_STAGE1B_LOAD_BEARING")
        self.assertEqual(sum(row["creates_seed"] for row in rows), 1)

    def test_unknown_selection_and_duplicate_candidates_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "selection ids absent"):
            target.build_decisions(
                [{"arxiv_id": "2607.00001"}],
                {"2607.99999": {"role": "KEEP_CORE", "family": "x", "reason": "y"}},
                set(),
            )
        with self.assertRaisesRegex(ValueError, "duplicate candidate"):
            target.build_decisions(
                [{"arxiv_id": "2607.00001"}, {"arxiv_id": "2607.00001"}], {}, set()
            )

    def test_run_writes_hash_bound_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            candidates = root / "candidates.jsonl"
            candidates.write_text(
                json.dumps({"arxiv_id": "2607.00001", "title": "A", "abstract": "z"}) + "\n",
                encoding="utf-8",
            )
            config = root / "config.json"
            config.write_text(
                json.dumps({
                    "selections": [{
                        "arxiv_id": "2607.00001", "role": "KEEP_CORE",
                        "family": "evidence_state", "reason": "map-changing"
                    }]
                }), encoding="utf-8"
            )
            known = root / "known.jsonl"
            known.write_text("", encoding="utf-8")
            output = root / "decisions.jsonl"
            summary = root / "summary.json"
            result = target.run(candidates, config, [known], output, summary)
            self.assertEqual(result["candidate_rows"], 1)
            self.assertEqual(result["selected_fulltext"], 1)
            self.assertEqual(result["unresolved"], 0)
            self.assertEqual(len(result["decision_ledger_sha256"]), 64)
            self.assertEqual(json.loads(summary.read_text("utf-8"))["selected_fulltext"], 1)


if __name__ == "__main__":
    unittest.main()
