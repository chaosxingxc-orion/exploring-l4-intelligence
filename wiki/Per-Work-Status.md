# Per-Work Status

> **This is the living status board — the page that changes most often.** Update it whenever a
> work's maturity or near-term plan shifts, and note big moves in [[Decision-Log]].
> Last reviewed: 2026-07-11.
> 现行 primary question（G0，2026-07-11）见 [[2026-07-11-stage1-audit-response-and-rulings]] §4。

| # | Repo | Status | One-line state |
|---|------|--------|----------------|
| **W4** | `speech-mllm-omni-embedding-rl` | 🟡 Skeleton → **active (flagship)** | Flagship: training-free RL to disentangle a frozen omni model's embeddings; omni-embed model wired. |
| **W1** | `speech-mllm-training-free-rl` | 🟢 Mature · pattern reference | Training-free reward/eval machinery W4 reuses; **holds the genuine reward-driven best-of-N result** (frozen Qwen3-Omni-30B via llama.cpp). |
| W2 | `speech-mllm-efficient-rl-alignment` | 🟡 Skeleton | Hydra scaffold + shared-lib wiring; RL loop to fill in. |
| W3 | `speech-mllm-multitask-rl` | 🟡 Skeleton | Hydra scaffold + shared-lib wiring; RL loop to fill in. |

**W4 — Omni-embedding speech disentanglement (flagship, active).** Training-free RL (no weight/
structure change) to steer the frozen `omni-embed-nemotron-3b` so task-conditioned embeddings of the
same audio give different, individually-better downstream performance across content/ASR+ST,
speaker-ID, emotion/SER, and language+intent. First-proof substrate: CREMA-D (speaker + emotion on the
same audio). **Done:** math-feasibility doc + per-factor operator decision (content→A, language→A,
speaker→hybrid, emotion→B); the CREMA-D two-factor proof loop runs end-to-end, reproducibly, logged to
MLflow (`bash scripts/train.sh seed=42`). **First result (3-factor CREMA-D):** the SAME frozen embedding gives
content ≈**1.00**, emotion ≈**0.36**, speaker ≈**0.04** (≈chance); instruction conditioning does not steer the embedding
(columns flat), confirming the suppression prediction (see [[W4-Training-Free-RL-Feasibility]] §0.1).
W4 首结果为 L0/L1 证据（factor readout availability/suppression：content≈1.0 是 12 句固定句 ID、emotion
部分可读、speaker 近 chance；matched>mismatched 判据 diagonal_dominant=False 未过）——"已解耦/thesis
demonstrated" 表述按 [[2026-07-11-stage1-audit-response-and-rulings]] 裁定废止；W4 待按 §7.1 重定义（#29）。
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
`scripts/pool_method_probe.py`.
**Honest correction (2026-07-01/02 adversarial reviews).** The headline emotion gain **+0.097 is a
NULL**: re-run across seeds on the 5090, the 95% t-CI **[−0.043, +0.116] spans 0** (the original was a
single-seed oracle-test-layer artifact); the reproducer now *emits* that t-CI so the committed JSON is
script-produced. A forensic pass also established the frozen bi-encoder's "selection" is **argmax
cosine, not reward-driven** — honest frozen-encoder *probing*, a distinct operator, **not** training-free
RL. Committed reproducible artifacts: emotion t-CI `cdbf1d2`, MInDS-14 paired-CI `ff6be7c`,
paralinguistic-negative probe `7ba8d0b`. **Next:** (1) strict same-audio SSL baseline
(emotion2vec/WavLM/ECAPA on the CREMA-D split); (2) multi-vector / ordered-trajectory emotion readout;
(3) emotion2vec-fusion; (4) W1→W4 RL-on-speaker bridge; then 1.4 content/language fan-out
(LibriSpeech/CoVoST2/FLEURS/MINDS14).

**Cross-work paper — `papers/agent-level-tfrl/` (umbrella).** The W5 agent-level proposal was
adversarially collapsed and reframed (2026-07-02) into an honest single-model training-free-RL paper:
**C1** = W1's genuine best-of-N (primary), **C2** = W4's frozen-encoder probing (secondary, not RL),
**C3** = the reward-spread lens (sign + ceiling only), two sorry-free Lean lemmas. Four fresh hostile
review rounds → **CONVERGED, 0 surviving fundamental/major**; every number reproduced from committed
artifacts. Merged via PR #2. **That open question is now CLOSED (2026-07-04): the step-1 rationality campaign — pre-registered criteria (freeze b19bff2), two pilots with freeze-before-run commits, a 6-charge hostile panel, and a unanimous sound-with-corrections /ars-reviewer verdict — ended in an owner-ratified NO-GO** (M3 killed by measurement F=0.38108 vs 0.01; M5 inconclusive-by-inert-instrument → frozen default; re-open only on r1/r2/r3). Single-model work continues via P-D. See [[2026-07-03-omni-agentic-tfrl-go-no-go-decision]] and Decision-Log 2026-07-04.

**W1 — Training-free RL (mature pattern reference).** Gradient-free, reward-guided inference-time RL
(best-of-N, reward-guided decoding, reranking). The most complete work; its verifiable-reward/eval
machinery is what the flagship W4 reuses. **Genuine best-of-N result (2026-07-02, committed
`b7b4b0d`/`cd6aa92`/`f9d111a`):** frozen Qwen3-Omni-30B (Q8_0 GGUF, llama.cpp resident server,
`-ngl 28` on the 24 GB laptop 5090) samples N transcripts per LibriSpeech test-other+snr5 utterance,
a verifiable WER reward selects. Multi-seed (3 generation seeds pooled, n=144): **oracle-WER headroom
+0.042 [0.029, 0.056] at N=8, significant from N=4** (N=1 < greedy — the honest order-statistics
climb); the deployable label-free **MBR selector is non-significant at every N**.

> **2026-07-11 更正**：以上为 macro-utterance 指标，须始终标注为 macro。独立复算的 **CORPUS WER**
> （2026-07-11）：greedy 0.0925、oracle-8 0.0629（提升 +0.0296，bootstrap CI [0.0212, 0.0390]）、
> MBR-8 0.0938（−0.0012，CI 跨零）。response-review 指出在 corpus 指标下 **MBR 在 N=1/N=2 显著更差**
> （待 #26 统计重跑再核实）。此前的 macro-utterance 数字（+0.0418 oracle / +0.0037 MBR）本身没有错，
> 但必须始终标注为 macro，不得与 corpus WER 混用或省略标注。

Engine decision:
[[Inference-Engine-Choice]]. (Asset downloading is unified in the umbrella's
`scripts/data/fetch-data.sh`, driven by `docs/datasets.lock.json`; the old W1 `wave0_fetch.sh` engine
was retired.) Roadmap: **close the realized-vs-headroom gap** (a stronger label-free selector), broaden
reward-guided strategies, harden eval. **Stage-1 problem-definition (2026-07-04, methodology now in CLAUDE.md):** the
semantic-layer TFRL/ICL sufficiency question was surveyed (a strict-reviewed 16k-word paper, 171 refs,
[[2026-07-04-stage1-semantic-tfrl-survey]]) and reduced to ranked candidate problems
([[2026-07-04-stage1-problem-definition]]); at K2 the owner selected **CP-1 (quantify H_prompt−H_fix),
CP-3 (measure ρ(ASR)), CP-8 (calibration+PMI on SLU/MCQ), CP-4 (voice-agent pass@k)** for Stage-2.
Next: a semantic-task validation table + per-problem Research-Proposal-Template instances.
**Step-1 wave-1 baseline grid COMPLETE (2026-07-10):** the frozen 224-cell grid (56 dataset keys ×
{Qwen3-Omni-30B, MERaLiON-2-3B} GGUF × dev/test) fully executed, zero run failures; per-wave Opus
audit caught 60 mechanically-invalid MCQ cells (K8 gold-resolution bug) → surgical freeze-repair +
GPU-free rescore from stored replies, regression-guarded. Full table: W1 `_repro/wave1_results.md`.
**Wave-2 completed 32/32** (K4–K7 × qwen3 单底座 × dev/test，W1 `f8ca276` freeze-repair 后全有效)；
wave-3 8/8 批量化收官、Step-1 网格关账 76/76（W1 `07bbc66`）；重抽验证格通过后全量重跑因 2026-07-11
stop-the-line 暂停。
Details: [[Decision-Log]] 2026-07-10（续6）.

**W2 — Efficient RL alignment (skeleton).** Efficient GRPO/DPO with LoRA / partial updates for
speech↔language alignment. Roadmap: implement the LoRA GRPO/DPO loop on top of the shared rewards;
adopt W1's config/eval patterns.

**W3 — Multi-task RL (skeleton).** One policy, RL across ASR/ST/SID/SER via per-task verifiable
rewards. Roadmap: wire per-task rewards from `speechrl_common.rl`; multi-task sampling/eval.

---

## 中文

> **这是活动状态板——更新最频繁的页面。** 任一工作的成熟度或近期计划变化时就更新它，重大变动同时记到
> [[Decision-Log]]。最近复核：2026-07-11。

各工作状态见上表。**W4（omni 嵌入语音解耦，旗舰，进行中）：** 免训练 RL（不改权重/结构）引导冻结的
`omni-embed-nemotron-3b`，使同一段音频在不同任务条件下的嵌入，在内容/ASR+ST、说话人、情感/SER、
语言+意图上产生不同且各自更优的下游表现。首个验证底座为 CREMA-D（同一音频上的说话人+情感）。路线：
数学可行性文档 + 逐因子算子决策 → CREMA-D 双因子验证闭环 → 各任务族扩展。详见
[[W4-Training-Free-RL-Feasibility]]。

**W1（免训练 RL，成熟范式参考）：** 免梯度、奖励引导的推理时 RL（best-of-N、奖励引导解码、重排序），
是最完整的工作，其可验证奖励/评测机制正是旗舰 W4 复用的地基。**真实 best-of-N 结果（2026-07-02，
`b7b4b0d`/`cd6aa92`/`f9d111a`）：** 冻结 Qwen3-Omni-30B（Q8_0 GGUF，llama.cpp，24GB 5090 上
`-ngl 28`）+ 可验证 WER 奖励选择；多种子（n=144）oracle headroom 在 N=8 达 +0.042 [0.029,0.056]、
N≥4 显著；无标签 MBR 各 N 均不显著（以上为 macro-utterance 指标，**见下方 2026-07-11 更正**）。
引擎决策见 [[Inference-Engine-Choice]]。（资产下载已统一到
umbrella 的 `scripts/data/fetch-data.sh`；原 `wave0_fetch.sh` 已退役。）路线：**收窄
realized-vs-headroom 差距**（更强的无标签选择器）、拓展奖励引导策略、强化评测。另：W4 的旗舰情感增益
+0.097 经跨种子重跑修正为 **NULL**（t-CI [−0.043,+0.116] 跨 0）；跨工作论文
`papers/agent-level-tfrl/`（C1=W1 真实 best-of-N，C2=W4 诚实探针，C3=奖励离散度透镜）已于
2026-07-02 四轮敌对审查收敛并经 PR #2 合入。论文遗留的开放问题（agentic 分解是否超越冻结单模型）已于 2026-07-04 经预注册战役裁定 **NO-GO 关闭**（M3 测量击杀、M5 惰性仪器按冻结默认、重开仅凭 r1/r2/r3），单模型工作经 P-D 继续——见 [[2026-07-03-omni-agentic-tfrl-go-no-go-decision]]。

**W2（高效 RL 对齐，骨架）：** 用 LoRA / 部分更新的高效 GRPO/DPO 做语音↔语言对齐；路线：在共享奖励上
实现 LoRA 的 GRPO/DPO 主循环，沿用 W1 的配置/评测范式。**W3（多任务 RL，骨架）：** 单策略，跨
ASR/ST/SID/SER 的可验证奖励；路线：接入 `speechrl_common.rl` 的逐任务奖励、多任务采样/评测。
