# Per-Work Status

> **This is the living status board — the page that changes most often.** Update it whenever a
> work's maturity or near-term plan shifts, and note big moves in [[Decision-Log]].
> Last reviewed: 2026-06-23.

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
**Model-understanding phase (1.2.1) DONE — ICL tested, verdict now evidence-backed.** Diagnostic probes
(I/O contract, query-token isolation, native text-query retrieval, few-shot ICL + label control) on the
frozen model: native text-query recovers content (0.99) but not emotion (0.27); in-context demos
strongly move the query rep (move 0.336) but are label-insensitive (0.047) and **few-shot demos hurt
emotion** (0.217→0.150). So **no weight-free Operator-A lever — instruction, layer, pooling, native
retrieval, or ICL — recovers speaker/emotion** *under single-vector mean pooling*; few-shot is
structurally/mechanically supported but not a useful label-activation lever.
**Paralinguistic-suppression survey + pooling-method probe (D2+D3) DONE — emotion verdict upgraded.** A
77-agent 3-vote-verified literature survey + a weight-free pooling-METHOD probe (mean/std/stats/attentive
× layer, CREMA-D seeds 42/7) show the suppression is **per-factor and a *readout* problem, not destruction**:
the single masked-mean vector is near-degenerate, so emotion needs a **richer readout** (attentive
mid-layer lifts emotion 0.40→~0.45–0.51 weight-free; ordered-trajectory/multi-vector is the big lever,
C-Gate +61pp), whereas **fine-grained speaker-ID is never written to the pooled output** (floored ≤0.067
across all methods/layers/seeds; recovered only by an external speaker encoder or disentangled codec).
Verdict (updated): **content→A (~1.0); emotion→A with a richer readout (multi-vector/trajectory/layer/
generative) BEFORE B; speaker→B / external-channel; language→provisional A**. Refs:
[[Paralinguistic-Suppression-Survey]], [[Omni-Embed-Model-Dossier]],
[[2026-06-23-omni-embed-speech-disentanglement-1.2.1]]. New code: `layer_probe.extract_pooled` +
`scripts/pool_method_probe.py`. **Next:** (1) strict same-audio SSL baseline (emotion2vec/WavLM/ECAPA on
the CREMA-D split); (2) multi-vector / ordered-trajectory emotion readout; (3) emotion2vec-fusion; (4)
W1→W4 RL-on-speaker bridge; then 1.4 content/language fan-out (LibriSpeech/CoVoST2/FLEURS/MINDS14).

**W1 — Training-free RL (mature pattern reference).** Gradient-free, reward-guided inference-time RL
(best-of-N, reward-guided decoding, reranking). The most complete work; its verifiable-reward/eval
machinery is what the flagship W4 reuses. (Asset downloading is now unified in the umbrella's
`scripts/data/fetch-data.sh`, driven by `docs/datasets.lock.json`; the old W1 `wave0_fetch.sh` engine
was retired.) Roadmap: broaden reward-guided strategies, harden eval.

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
是最完整的工作，其可验证奖励/评测机制正是旗舰 W4 复用的地基。（资产下载已统一到 umbrella 的
`scripts/data/fetch-data.sh`，由 `docs/datasets.lock.json` 驱动；原 W1 `wave0_fetch.sh` 引擎已退役。）
路线：拓展奖励引导策略、强化评测。

**W2（高效 RL 对齐，骨架）：** 用 LoRA / 部分更新的高效 GRPO/DPO 做语音↔语言对齐；路线：在共享奖励上
实现 LoRA 的 GRPO/DPO 主循环，沿用 W1 的配置/评测范式。**W3（多任务 RL，骨架）：** 单策略，跨
ASR/ST/SID/SER 的可验证奖励；路线：接入 `speechrl_common.rl` 的逐任务奖励、多任务采样/评测。
