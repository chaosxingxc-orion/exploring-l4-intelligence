# Per-Work Status

> **This is the living status board — the page that changes most often.** Update it whenever a
> work's maturity or near-term plan shifts, and note big moves in [[Decision-Log]].
> Last reviewed: 2026-06-22.

| # | Repo | Status | One-line state |
|---|------|--------|----------------|
| **W4** | `speech-mllm-omni-embedding-rl` | 🟡 Skeleton → **active (flagship)** | Flagship: training-free RL to disentangle a frozen omni model's embeddings; omni-embed model wired. |
| **W1** | `speech-mllm-training-free-rl` | 🟢 Mature · pattern reference | The reusable training-free reward/eval machinery W4 builds on; owns the asset engine. |
| W2 | `speech-mllm-efficient-rl-alignment` | 🟡 Skeleton | Hydra scaffold + shared-lib wiring; RL loop to fill in. |
| W3 | `speech-mllm-multitask-rl` | 🟡 Skeleton | Hydra scaffold + shared-lib wiring; RL loop to fill in. |

**W4 — Omni-embedding speech disentanglement (flagship, active).** Training-free RL (no weight/
structure change) to steer the frozen `omni-embed-nemotron-3b` so task-conditioned embeddings of the
same audio give different, individually-better downstream performance across content/ASR+ST,
speaker-ID, emotion/SER, and language+intent. First-proof substrate: CREMA-D (speaker + emotion on the
same audio). **Done:** math-feasibility doc + per-factor operator decision (content→A, language→A,
speaker→hybrid, emotion→B); the CREMA-D two-factor proof loop runs end-to-end, reproducibly, logged to
MLflow (`bash scripts/train.sh seed=42`). **First result (3-factor CREMA-D):** the SAME frozen embedding gives
content ≈**1.00**, emotion ≈**0.36**, speaker ≈**0.04** (≈chance) — the thesis ("different downstream
tasks → different performance") demonstrated; instruction conditioning does not steer the embedding
(columns flat), confirming the suppression prediction (see [[W4-Training-Free-RL-Feasibility]] §0.1).
**F.1 (richer Operator-A axes):** layer sweep (37 layers) + audio-token pooling show speaker ~chance
and emotion ~0.40 *under single-instruction conditioning* — but this is a weak intervention;
**conclusion is provisional**, the model's strongest lever (ICL / activation heads) is **untested**.
Archived report: [[2026-06-22-omni-embed-speech-disentanglement-1.1.1]]. **Next (exp 1.2):** activation
heads / ICL — native text-query zero-shot retrieval + few-shot demonstrations with target-token pooling
— for speaker/emotion, before any Operator-B claim; then Operator B for what stays flat; then
content/language fan-out (LibriSpeech/CoVoST2/FLEURS/MINDS14).

**W1 — Training-free RL (mature pattern reference).** Gradient-free, reward-guided inference-time RL
(best-of-N, reward-guided decoding, reranking). The most complete work; owns the asset download
engine (`scripts/wave0_fetch.sh`); its verifiable-reward/eval machinery is what the flagship W4
reuses. Roadmap: broaden reward-guided strategies, expand datasets/benchmarks, harden eval.

**W2 — Efficient RL alignment (skeleton).** Efficient GRPO/DPO with LoRA / partial updates for
speech↔language alignment. Roadmap: implement the LoRA GRPO/DPO loop on top of the shared rewards;
adopt W1's config/eval patterns.

**W3 — Multi-task RL (skeleton).** One policy, RL across ASR/ST/SID/SER via per-task verifiable
rewards. Roadmap: wire per-task rewards from `speechrl_common.rl`; multi-task sampling/eval.

---

## 中文

> **这是活动状态板——更新最频繁的页面。** 任一工作的成熟度或近期计划变化时就更新它，重大变动同时记到
> [[Decision-Log]]。最近复核：2026-06-22。

各工作状态见上表。**W4（omni 嵌入语音解耦，旗舰，进行中）：** 免训练 RL（不改权重/结构）引导冻结的
`omni-embed-nemotron-3b`，使同一段音频在不同任务条件下的嵌入，在内容/ASR+ST、说话人、情感/SER、
语言+意图上产生不同且各自更优的下游表现。首个验证底座为 CREMA-D（同一音频上的说话人+情感）。路线：
数学可行性文档 + 逐因子算子决策 → CREMA-D 双因子验证闭环 → 各任务族扩展。详见
[[W4-Training-Free-RL-Feasibility]]。

**W1（免训练 RL，成熟范式参考）：** 免梯度、奖励引导的推理时 RL（best-of-N、奖励引导解码、重排序），
是最完整的工作，维护资产下载引擎（`scripts/wave0_fetch.sh`），其可验证奖励/评测机制正是旗舰 W4 复用的
地基。路线：拓展奖励引导策略、扩充数据集/基准、强化评测。

**W2（高效 RL 对齐，骨架）：** 用 LoRA / 部分更新的高效 GRPO/DPO 做语音↔语言对齐；路线：在共享奖励上
实现 LoRA 的 GRPO/DPO 主循环，沿用 W1 的配置/评测范式。**W3（多任务 RL，骨架）：** 单策略，跨
ASR/ST/SID/SER 的可验证奖励；路线：接入 `speechrl_common.rl` 的逐任务奖励、多任务采样/评测。
