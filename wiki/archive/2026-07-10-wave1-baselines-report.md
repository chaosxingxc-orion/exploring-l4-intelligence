# 2026-07-10 · Step-1 波 1 基线锁定报告（224/224 完成，Opus 验收 ACCEPT-with-notes）

> **性质**：Stage-1 Step-1 波 1 收官记录。**数字权威来源 = W1 `_repro/wave1_results.md`**
> （聚合器自 224 个结果 JSON 生成，含逐格 mean±CI；本文只做验收结论与 caveat 摘要）。
> 全程 directional 分级；判据冻结于 `2026-07-09-step1-freeze-record.md`。

## 1. 完成与验收

- **网格 224/224**：56 数据条目（K1×4 + K2×4 + K8×47 + K9×1）× {Qwen3-Omni-30B GGUF,
  MERaLiON-2-3B GGUF} × {dev 40, test 60}；终态 failed=0（heysquad 两格补跑成功）。
- **Opus 对抗验收：ACCEPT-with-notes**——普查零缺格、全部冻结字段齐、双底座同 item-id 集
  零错配、边界纪律机械抽检零泄漏（指令中无任何 golden 文本）。
- **审计→修复→重评分闭环**（跨会话协作）：审计根因了 60 个机械零分格（全部 14 个 air-bench
  K8 + uro-OpenbookQA-zh 的 MCQ gold 未解析为选项索引），修复后**用存量回复重评分（未重新
  生成）**（W1 `3b2d4bd`），验收确认修复后无残留指标缺陷。

## 2. 基线要点（详表见 `_repro/wave1_results.md`）

- **Qwen3-Omni（主底座）**：ASR-en ~0.95（librispeech/seed-tts-en）、ASR-zh 0.84–0.95；
  zh 知识/MCQ 强（HSK5-zh 1.00 满分——验收核实为真实逐题命中、OpenbookQA-zh 0.95、
  GaokaoEval 0.95）；音频理解中档（mmau 0.72、mmsu 0.78、air-bench 各任务 0.15–0.90 分布）；
  弱项诚实（Gsm8k 口语数学 0.58、heysquad 0.2-0.28、containment 弱指标类 ≈0）。
- **MERaLiON-2 关键发现**：MCQ/音频感知可用（music-genre 0.43-0.55、mmsu-spoken 0.43），但
  **开放式转写/复述指令跟随退化——70% 提示词回声**（zh-ASR≈0 是真实能力缺陷；5600 条回复
  前缀剥离零残留，排除采集 bug）。**角色修正：step-2/3 中 MERaLiON 适用于 MCQ/封闭形态的
  跨模型验证，不适用于开放生成对照**。
- **K9 squtr 闭卷 floor**：按冻结设计 unscored（回复已存，供 step-2 RAG delta 对照）。

## 3. 入档 caveat（验收 notes）

1. **dev/test 重叠量化**：52/56 集有重叠（6 个 legacy 集 dev⊆test 全嵌套、小池 uro 子集重叠
   10–37、34 集低重叠、仅 4 集不相交）——dev/test 是同池两视图**不是独立 held-out**；
   Stage-1 方向性口径合规，**不得读作泛化性证据**；step-2 冻结会附裁决位：是否为 Phase-B
   改做不相交重抽。
2. **containment-EM 弱指标类**（MLC*/vocalbench-multi-round 等）：简短正确答案对冗长 gold
   计 0——指标诚实但弱，冻结时已标 directional-weak。
3. **低 n 诊断格**：clothoaqa 仅 4/7 有效项（数据缺口本日已补齐 1000/1000，波 2 前可重切）。
4. **sample_manifest 悬空指针**：49 个包 loader 数据集的快照文件未落盘（权威样本记录 =
   结果 JSON 内 per_item.item_id 列表，普查即基于此）——波 2 前工程修复项。
5. 3 个 qwen3 格有 1-2 条空生成（reply=null，正确置 None）。

## 4. 运行与基础设施记录

3 次中断（1 次锁语义 bug + 2 次会话边界击杀）全部由 checkpoint 零浪费恢复；根因修复入库：
gpu_session 锁记录调用方 pid（`ff913a8`）、驱动器失败不再中止后续底座（`8b9b364`）、
**WSL vmIdleTimeout=8h**（VM 秒级回收连坐 setsid 进程的根因）。跨会话并发协作按
concurrent-sessions 协议执行（本报告与姊妹会话的簿记/指标修复/波 2 驱动器互认）。

## 5. 下一步

Step-2 冻结会（材料齐：`2026-07-10-step2-grid-draft.md` 7+3 签字位 + 本报告 caveat 裁决位）；
波 2（K4–K7）驱动器已就绪（W1 `c9ee7d1`），与 step-2 Phase-A 排程协调开跑。
