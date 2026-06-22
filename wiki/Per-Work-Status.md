# Per-Work Status

> **This is the living status board — the page that changes most often.** Update it whenever a
> work's maturity or near-term plan shifts, and note big moves in [[Decision-Log]].
> Last reviewed: 2026-06-22.

| # | Repo | Status | One-line state |
|---|------|--------|----------------|
| W1 | `speech-mllm-training-free-rl` | 🟢 Mature · reference (still expanding) | Most developed; the template the others follow. |
| W2 | `speech-mllm-efficient-rl-alignment` | 🟡 Skeleton | Hydra scaffold + shared-lib wiring; RL loop to fill in. |
| W3 | `speech-mllm-multitask-rl` | 🟡 Skeleton | Hydra scaffold + shared-lib wiring; RL loop to fill in. |
| W4 | `speech-mllm-omni-embedding-rl` | 🟡 Skeleton | Hydra scaffold; omni-embed model download target wired. |

**W1 — Training-free RL (reference, still expanding).** Gradient-free, reward-guided inference-time
RL (best-of-N, reward-guided decoding, reranking). It is the most complete work and owns the asset
download engine (`scripts/wave0_fetch.sh`). Roadmap: broaden reward-guided strategies, expand
datasets/benchmarks, and harden eval — *and keep growing it as the reference others copy.*

**W2 — Efficient RL alignment (skeleton).** Efficient GRPO/DPO with LoRA / partial updates for
speech↔language alignment. Roadmap: implement the LoRA GRPO/DPO loop on top of the shared rewards;
adopt W1's config/eval patterns.

**W3 — Multi-task RL (skeleton).** One policy, RL across ASR/ST/SID/SER via per-task verifiable
rewards. Roadmap: wire per-task rewards from `speechrl_common.rl`; multi-task sampling/eval.

**W4 — Omni-embedding RL (skeleton).** RL over contrastive/retrieval objectives for omni embeddings
(`omni-embed-nemotron-3b` download target already wired). Roadmap: contrastive RL objective + retrieval eval.

---

## 中文

> **这是活动状态板——更新最频繁的页面。** 任一工作的成熟度或近期计划变化时就更新它，重大变动同时记到
> [[Decision-Log]]。最近复核：2026-06-22。

各工作状态见上表。**W1（免训练 RL，参考范式，仍在扩展）：** 免梯度、奖励引导的推理时 RL（best-of-N、
奖励引导解码、重排序），是最完整的工作，并维护资产下载引擎（`scripts/wave0_fetch.sh`）。路线：拓展
奖励引导策略、扩充数据集/基准、强化评测——并**作为他人参照的范式持续生长**。

**W2（高效 RL 对齐，骨架）：** 用 LoRA / 部分更新的高效 GRPO/DPO 做语音↔语言对齐；路线：在共享奖励上
实现 LoRA 的 GRPO/DPO 主循环，沿用 W1 的配置/评测范式。**W3（多任务 RL，骨架）：** 单策略，跨
ASR/ST/SID/SER 的可验证奖励；路线：接入 `speechrl_common.rl` 的逐任务奖励、多任务采样/评测。
**W4（omni 嵌入 RL，骨架）：** 面向 omni 嵌入的对比/检索目标 RL（`omni-embed-nemotron-3b` 下载目标已
接好）；路线：对比式 RL 目标 + 检索评测。
