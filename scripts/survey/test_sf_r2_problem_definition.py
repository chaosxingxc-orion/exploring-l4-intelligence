from __future__ import annotations

import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
R2 = REPO / "wiki/survey/workbench/stage1c-portfolio/proposals/R2-audio-native-knowledge-acquisition.md"
CURRENT = REPO / "wiki/survey/current/research-directions.md"
STATUS = REPO / "wiki/survey/current/status.md"


class R2ProblemDefinitionContractTests(unittest.TestCase):
    def test_opening_report_is_marked_unverified_executor_draft(self) -> None:
        text = R2.read_text(encoding="utf-8")
        for required in (
            "音频驱动外部知识检索的文献归纳、实验载体与方向处置",
            "STAGE_1C_DIRECTION_CONFIRMATION",
            "EXECUTOR_DRAFT_UNVERIFIED_BY_OWNER",
            "WITHDRAWN_TO_DRAFT__PENDING_OWNER_COWORK_UNDER_2026-07-29_CRITERION",
            "已撤回为草稿意见",
            "owner 未校验",
            "Decision-Log 续76",
            "R5/R6/R8",
            "R3/R7 或 R9",
        ):
            self.assertIn(required, text)

    def test_report_uses_reference_datasets_baselines_and_metrics(self) -> None:
        text = R2.read_text(encoding="utf-8")
        for required in (
            "AudioRAG",
            "500",
            "Omni-DeepSearch",
            "640",
            "VoiceAgentRAG",
            "200",
            "NovaCRM",
            "Qwen3-Omni raw 为 37.0%",
            "46.2%",
            "GPT-4o judge accuracy",
            "三位 LLM judge",
            "cache hit rate",
            "retrieval latency",
        ):
            self.assertIn(required, text)

    def test_need_detection_mismatch_and_no_new_data_boundary_are_explicit(self) -> None:
        text = R2.read_text(encoding="utf-8")
        for required in (
            "没有负类就不能测 need detection",
            "不自行混入 waveform-sufficient 负例",
            "不为 need detection 新标",
            "不把实时 web 搜索结果抓取并整理成新的 benchmark corpus",
            "不新造统一 utility",
            "官方数据没有 negative class",
        ):
            self.assertIn(required, text)

    def test_current_layer_exposes_r1_sunset_and_r2r9_unverified_state(self) -> None:
        current = CURRENT.read_text(encoding="utf-8")
        status = STATUS.read_text(encoding="utf-8")
        for text in (current, status):
            self.assertIn(
                "NO_GO_AS_STANDALONE_DIRECTION__SUNSET_BEFORE_STAGE2", text
            )
            self.assertIn("OWNER_UNVERIFIED", text)
            self.assertIn("2026-07-29", text)
        self.assertIn("执行者草稿，owner 未校验", current)


if __name__ == "__main__":
    unittest.main(verbosity=2)
