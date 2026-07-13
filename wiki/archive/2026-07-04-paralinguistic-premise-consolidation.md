> **LOG** — Stage-1 过程记录（hypothesis-grade），非现行真源；现行结论以 [[Decision-Log]] 与 [[Per-Work-Status]] 为准。

# Settled premise — frozen omni models and shallow speech signals (speaker / emotion)

> Consolidation of existing evidence (zero new experiments), per the owner's Stage-1 directive:
> solidify "omni models no longer represent shallow speech signals" as the premise that focuses
> our research on the SEMANTIC layer (ASR / SLU / Spoken-QA / Speech-Agentic). The premise is
> stated with its correct two-class scoping — overstating it was one of the recorded caveats of
> the 2026-06-23 semantic pivot ("'only semantic' overstates").

## 1. The premise, correctly scoped

**Vector/embedding class (contrastive bi-encoder, e.g. omni-embed-nemotron-3b): SETTLED.**

- **Speaker: never written to the pooled output.** ≤ 0.067 (chance 0.011 baseline reference ~×6,
  still floor-level for 91-way ID) across ALL 37 Thinker layers × pooling methods
  (mean/std/stats/attentive) × seeds; recovered in the literature only by an external speaker
  encoder (ECAPA-LLM, 1.03% EER) or a disentangled codec — both weight-changing.
  Mechanism: contrastive InfoNCE provably discards features not needed to separate positives
  (arXiv:2008.05659); mean-pooling discards the second-order statistics speaker-ID needs.
- **Emotion: present but unread at the single-vector readout.** Weight-free ceiling ~0.40 (mean
  pooling) to ~0.45–0.51 (attentive-stats @L16; seed-sensitive, CIs overlap on seed 7). The
  headline +0.097 gain was corrected to **NULL across seeds** (95% t-CI [−0.043, +0.116]).
  Final-layer probes in the literature still find 3–55× chance — suppression at readout, not
  destruction; the big levers identified (ordered-trajectory / multi-vector readout, C-Gate
  +61pp) are architecture/readout changes, not prompting.
- **ICL does not rescue either factor on this class.** Demos move the representation strongly
  (move 0.336) but are label-insensitive (0.047), and few-shot demos HURT emotion (0.217→0.150).

**Generative class (Thinker-Talker, e.g. Qwen3-Omni): literature-only, negative-leaning —
hypothesis-grade, stated as such.**

- Paralinguistic information demonstrably exists in the token stream (a frozen LLM can perceive
  it when the encoder exposes it, arXiv:2410.01162; WavBench emotion 75–93%; emotion-sensitive
  neurons localizable, arXiv:2509.16589 / 2601.03115) — **presence is not the bottleneck**.
- But **every demonstrated recovery is a weight change**: VoxParadox 17.40→65.20 required DPO +
  a prompt-conditioned layer mixer (arXiv:2605.27772); forced-choice LoRA lifted CREMA-D emotion
  +44.5pp while speaker stayed unmoved (arXiv:2602.23136); speaker fine-ID resists prompting/ICL
  even on speech-aware LLMs — near-chance, only coarse gender works (arXiv:2603.10827).
- **No training-free demonstration exists** (in our archives or the 2026-07-03 delta scans) of
  instruct-prompt/ICL activating paralinguistics on a frozen generative omni.

## 2. Consequence for research focus

Under the training-free thesis (no weight or structure change), the shallow-signal axes offer:
vector class — nothing to read (speaker) or a readout-architecture problem (emotion, out of
fence); generative class — no known prompt-reachable path, all known fixes out of fence.
**Therefore the semantic layer (ASR / SLU / Spoken-QA / Speech-Agentic) — where content fidelity
is ≈1.0 on the vector class, generation is pretraining-native, and the surviving in-house
positives live (MInDS +0.126 scoped; C1 oracle headroom +0.0418 scoped) — is the rational focus.**
This resolves the 2026-06-23 OPEN ("full pivot vs second track"): full focus on the semantic
layer for Stage-1; the paralinguistic axes remain closed under this premise unless X2-class
delta scans surface a training-free counter-example (standing watch item).

## 3. Falsifiability of the premise

The premise is overturned for the generative class if literature demonstrates a **training-free**
(prompt/ICL-only) recovery of speaker-ID or emotion on a frozen omni model that survives
label-sensitivity + acoustic-grounding controls. The X2 delta-scan lane of the Stage-1 campaign
re-checks this each campaign; as of 2026-07-04, none exists.

## 4. 中文摘要

前提（正确限定后）：**向量类已定论**——speaker 从未写入池化向量（≤0.067，全 37 层×方法×种子；
对比学习+均值池化的机制性丢弃），emotion 存在但单向量读不出（天花板 ~0.4-0.51，+0.097 已修正为
跨种子 NULL），ICL 两者皆救不动（label-sens 0.047、demos 伤害 emotion）。**生成类文献级偏负**——
信息在 token 流里存在（不是瓶颈），但所有已示范的恢复都改权重（VoxParadox 靠 DPO、LoRA +44.5pp、
ECAPA 外挂），speaker 连生成类都抗拒 prompt/ICL；**不存在任何 training-free 的副语言激活示范**。
推论：训练无关论题下，研究聚焦**语义层**（内容保真 ≈1.0、幸存正数字所在）是理性选择——一并收口
6/23 的"全转向 vs 双轨"OPEN（全转向语义层）。前提可证伪条件与常设监测（X2）见 §3。
