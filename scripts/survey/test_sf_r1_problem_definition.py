from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
R1 = REPO / "wiki/survey/workbench/stage1c-portfolio/proposals/R1-adaptive-evidence-supply.md"
CURRENT = REPO / "wiki/survey/current/research-directions.md"
SUPPLEMENT = REPO / "wiki/survey/workbench/stage1c-portfolio/2026-07-27-r1-context-icl-evidence-supplement.md"
REGISTRY = REPO / "wiki/survey/registry/stage1c-r1-context-icl-2026-07-27-papers.jsonl"
LEDGER = REPO / "wiki/survey/2026-07-17-sf-fulltext-ledger.jsonl"

R1_NEIGHBORS = {
    "2402.01831",
    "2512.23808",
    "2601.18904",
    "2509.13395",
    "2512.18263",
    "2404.14716",
}


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


class R1ProblemDefinitionContractTests(unittest.TestCase):
    def test_opening_report_carries_the_locked_academic_problem(self) -> None:
        text = R1.read_text(encoding="utf-8")
        for required in (
            "语音/音频上下文学习方法复现与比较研究",
            "STAGE_1C_DIRECTION_CONFIRMATION",
            "NO_GO_AS_STANDALONE_DIRECTION__SUNSET_BEFORE_STAGE2",
            "OWNER_CONFIRMED_SUNSET_2026-07-29",
            "Decision-Log 续76",
            "不做创新点搜索",
            "数据只复用参考论文",
            "指标只复用参考论文",
            "Common Voice 15.0",
            "GLOBE-V2",
            "L2-ARCTIC",
            "MyST",
            "RSR",
            "MMAU",
            "MMAR",
            "MELD-Hard1k",
            "Qwen3-Omni-30B",
            "uniform random",
            "ECAPA-TDNN",
            "Vanilla SICL",
            "WER",
            "CER",
            "accuracy",
        ):
            self.assertIn(required, text)
        for retired in (
            "H_{\\mathrm{ctx}}",
            "O_{\\mathrm{sel}}",
            "I_{D\\times G}",
            "R_\\pi",
            "Qwen/Qwen2.5-Omni-7B",
        ):
            self.assertNotIn(retired, text)

    def test_current_contract_exposes_the_same_r1_boundary(self) -> None:
        text = CURRENT.read_text(encoding="utf-8")
        self.assertIn("### R1 — 冻结 Speech/Omni 模型的语音/音频上下文学习方法复现与比较", text)
        self.assertIn("Common Voice 15.0", text)
        self.assertIn("不自建数据", text)
        self.assertIn("不新造 utility", text)
        self.assertIn("NO_GO_AS_STANDALONE_DIRECTION__SUNSET_BEFORE_STAGE2", text)
        self.assertIn("不进入 Stage-2B", text)
        self.assertIn("MetaSICL", text)
        self.assertIn("TICL+", text)

    def test_registry_is_unique_and_hash_bound_to_fulltext_ledger(self) -> None:
        records = load_jsonl(REGISTRY)
        self.assertEqual(R1_NEIGHBORS, {row["arxiv_id"] for row in records})
        self.assertEqual(len(records), len({row["canonical_id"] for row in records}))
        ledger = {
            (row["arxiv_id"], row["kind"]): row
            for row in load_jsonl(LEDGER)
            if row.get("arxiv_id") in R1_NEIGHBORS
        }
        self.assertEqual(2 * len(R1_NEIGHBORS), len(ledger))
        for record in records:
            self.assertEqual("sf-paper-registry-record-v1", record["schema"])
            aid = record["arxiv_id"]
            for kind in ("pdf", "eprint"):
                row = ledger[(aid, kind)]
                self.assertEqual(200, row["http_status"])
                self.assertIsNone(row["error"])
                self.assertTrue(row["stored_at"])
                self.assertEqual(
                    row["sha256"], record["provenance"][f"{kind}_sha256"]
                )

    def test_supplement_preserves_split_and_claim_boundaries(self) -> None:
        text = SUPPLEMENT.read_text(encoding="utf-8")
        for required in (
            "SUPERSEDED_AS_DESIGN",
            "不再承载 R1 的当前研究设计",
            "12 条新增哈希记录",
            "test leave-one-out",
            "Base 与 Instruct",
            "LoRA",
            "context intervention protocol",
            "不构成技术 novelty verdict",
        ):
            self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
