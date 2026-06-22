# W4 — Training-Free RL for Omni-Embedding Speech Disentanglement: Feasibility

The mathematical-feasibility argument and algorithm survey behind the flagship claim in
[[Project-Thesis]]. This page locks the **formalism** (Wave D.1); the **algorithm survey table**
and **per-factor operator decision** are completed by the survey workflow (Wave D.2/D.3) with
verified sources. Status legend for claims: ✅ self-verified · ◐ sub-agent only · ⚠ assumption ·
✗ refuted.

## 0. Bottom line (filled by D.3)

> _Pending the survey + CREMA-D pilot._ Working hypothesis: a **hybrid** operator — embedding-layer
> test-time search (Operator A) for factors the frozen retrieval encoder keeps (content, language),
> and generative-end search (Operator B) for factors it may suppress (speaker, emotion).

## 1. Problem & the central difficulty

The flagship backbone `omni-embed-nemotron-3b` emits a **single dense vector** per (audio, text)
input — it does **not** generate tokens. The hottest reproducible training-free-RL methods (TTRL,
TPO, MBR, best-of-N, reward-guided decoding) are built on **sampling + reranking discrete token
sequences**. A vector-output model has no token distribution to sample, so that machinery has no
native action space here. Feasibility therefore hinges on **defining a legitimate inference-time
search space for a vector-output frozen model** (Operator A) versus **borrowing a generative model's
search and exporting an embedding from the winner** (Operator B).

## 2. Training-free RL, formally

Frozen parameters θ (never updated). Input x. A search/action space 𝒵 of inference-time degrees of
freedom and a search distribution q over 𝒵 that we optimize **at inference time** (q lives outside
θ). A deterministic read-out g_θ(x, z) produces the deployed answer/embedding; R is a **verifiable**
reward (computed from ground-truth labels, never model-judged).

**Objective (constrained inference-time expected-reward maximization):**

```
q* = argmax_q  E_{z~q}[ R(g_θ(x, z)) ]  −  β · KL(q ‖ q0)
```

with closed form (exponential tilting / Gibbs):

```
q*(z) ∝ q0(z) · exp( R(g_θ(x, z)) / β )
```

- `q0` = base search distribution (default conditioning / greedy / uniform). The **KL-to-base term
  is the trust region** that keeps activated behavior near the pretrained prior — it prevents
  degenerate collapse and reward hacking. (This is the same identity behind best-of-N ↔ RLHF
  equivalence and KL-constrained logit modulation.) ✅
- **No-weight-update invariant:** ∂/∂θ is never taken. All optimization is over the small
  inference-time object q (a temperature, a selection logit vector, a low-rank projection, a prompt
  index). This is what makes it *training-free*.

### Operator A — embedding-layer inference-time search (𝒵_A)

The model outputs `e = f_θ(x, c) ∈ ℝ^2048` (no tokens). Inference-time degrees of freedom:
conditioning/instruction selection `c ∈ C` (reuse `prompts.instruction_for`); pooling strategy (if
pre-pool states are exposed); a learned-at-inference linear/subspace projection `P` (a probe/
transform, **not** a θ update); candidate selection over K conditionings. Reward `R_A` = verifiable
downstream signal on `e` (retrieval hit@k via `rl.embedding_metrics`, or probe accuracy via
`rl.probe`). **Novel** — not present in published TTRL/TPO/MBR. The same tilting closed form holds
over 𝒵_A. (S, "steerability", is **partly confirmed**: the model is instruction-aware — it accepts a
`text` field with the audio. ✅)

### Operator B — generative-omni-end search (𝒵_B)

Use a generative omni model (Qwen3-Omni / Nemotron-3-Nano-Omni, already download targets) as the
policy; run best-of-N / MBR / reward-guided decoding over token sequences `y ~ π_θ(·|x,c)` (reuses
existing TTRL/MBR/BoN math), pick `y*`, then export an embedding from `y*` / its hidden states.
**Math is off-the-shelf**; the only novelty is the export step.

## 3. Disentanglement, formally

Latent factors of an utterance: `y = (y_content, y_speaker, y_emotion, y_language)`. A frozen
embedder is **task-disentangleable** if for each factor t there is a decodable subspace/map `D_t`
recovering `y_t` while ~invariant to the others. The **falsifiable claim** (testable on CREMA-D and
the four families):

```
∃ task-conditioned e_t = f_θ(x, c_t) and probes A_t  such that
A_t(e_t) > A_t(e_{t'})  for t' ≠ t   (gap ≥ δ, p < 0.05)
```

i.e. steering toward task t yields an embedding measurably better for t's probe than one steered
toward another task. **Sufficient conditions** (to verify empirically — the pilot's job):

- **(P) Presence** — pretraining absorbed factor t: `I(e; y_t) > 0`.
- **(L) Accessibility** — a low-complexity (linear/shallow) `D_t` reaches accuracy ≥ τ (ground in the
  linear-probing / information-bottleneck literature).
- **(S) Steerability** — conditioning `c_t` actually moves e along the factor's subspace.

**Suppression counterexample (the key risk).** Retrieval encoders are often trained to be
speaker/channel/emotion **invariant**. If so, `I(e; y_speaker) ≈ 0` ⇒ (P) fails ⇒ **no frozen-vector
operator can recover speaker**, and Operator B (re-extract from a generative model that keeps those
cues) is mandatory for that factor. ⚠ (decided by the CREMA-D pilot in Track E.4).

## 4. Algorithm survey (completed by the D.2 workflow)

For each candidate the survey records: applies to **A**? to **B**? the **correction** needed for the
speech modality; and a **convergence** sketch or counterexample — each row with sources + a status
tag. (Skeleton; rows verified/expanded by Wave D.2.)

| Algorithm | A? | B? | Correction for speech | Convergence / counterexample | Status |
|---|---|---|---|---|---|
| TTRL (majority-vote pseudo-reward; trains weights as published) | — | partial | replace majority vote with a **verifiable** reward; for frozen use, drop the grad step → best-of-N | Condorcet: vote converges to truth only if base acc > threshold; fails on weak SER/SID | ◐ |
| TPO (test-time preference opt, frozen) | — | ✓ | rule-based verifiable critique; monotone accept (revert non-improving) | fixed-point if the textual-gradient is a contraction; else oscillation | ◐ |
| JitRL (KL-closed-form logit modulation) | partial | ✓ | modulate conditioning/projection params, not token logits; gate on memory quality | inherits the KL-optimal closed form; empty/OOD memory ⇒ no-op (safe) | ◐ |
| MBR (minimum Bayes risk, frozen) | indirect | ✓ | use a non-self utility (embedding cosine / BLEU), 4–8 samples | converges to Bayes-risk min; correlated errors ⇒ confident-wrong centroid | ◐ |
| best-of-N / reward-guided decoding | A-form (over conditionings) | ✓ | control variates / common random numbers; cap N at the KL knee | monotone in N; over-optimization grows with N | ◐ |

**Cross-cutting corrections to settle:** verifiable reward instead of majority vote; variance
reduction for the gradient-free 𝒵_A optimizer; KL/entropy trust region tuned at the reward-vs-KL
knee; reward calibration (pseudo vs verifiable) on a held-out set.

## 5. Per-factor operator decision criteria (filled by D.3)

Select per factor from the CREMA-D + small-pilot evidence: default-embedding linear-probe accuracy
(**P**), linear-vs-MLP probe gap (**L**), instruction-conditioning shift (**S**), whether the
inequality `A_t(e_t) > A_t(e_{t'})` holds via conditioning alone, plus compute/latency and license.
Rule: (P)+(L)+(S) hold ⇒ **A** (cheap, novel); (P) fails ⇒ **B** for that factor.

## 6. Verifiable-claim registry (schema)

Each survey claim is one record: `id · statement · type{empirical,theoretical,definitional} ·
operator{A,B,both,n/a} · factor{content,speaker,emotion,language,n/a} · sources[urls] · support
(exact eq/number) · status{✅,◐,⚠,✗} · counterexample_checked · pilot_dependency`.

## 7. Pilot (Track E.4) & risks

The pilot is the **CREMA-D two-factor proof** (speaker + emotion on the same audio) — see
[[Per-Work-Status]] and the W4 repo. Top risks: **R1** steerability (mitigated — model is
instruction-aware); **R2** factor suppression (speaker/emotion may be invariant → Operator B);
**R3** linear-vs-nonlinear accessibility; **R4** reward-proxy validity (hold-out to avoid
over-optimization). License: NVIDIA OneWay Noncommercial + Qwen Research — research/eval only.

---

## 中文

支撑 [[Project-Thesis]] 中旗舰主张的「数学可行性论证 + 算法综述」。本页先锁定**形式化**（Wave D.1）；
**算法综述表**与**逐因子算子决策**由调研工作流（Wave D.2/D.3）带可核验来源补全。主张状态标记：
✅ 自验证 · ◐ 仅子代理 · ⚠ 假设 · ✗ 已证伪。

**核心难点。** 旗舰底座 `omni-embed-nemotron-3b` 每个输入只输出一个稠密向量，**不生成 token**；而最火的
免训练 RL（TTRL/TPO/MBR/best-of-N/奖励引导解码）都建立在「对离散 token 序列采样+重排」之上。向量输出模型
没有可采样的 token 分布，故需要重新定义算子：**A 类**＝在嵌入层做推理时搜索（条件化/池化/子空间投影/候选
选择，奖励=下游可验证信号）；**B 类**＝用生成式 omni 模型做 best-of-N/MBR 搜索再导出嵌入。

**免训练 RL 形式化。** 冻结 θ，在推理时对搜索分布 q 优化：`q* = argmax_q E_{z~q}[R(g_θ(x,z))] −
β·KL(q‖q0)`，闭式解 `q*(z) ∝ q0(z)·exp(R/β)`（指数倾斜）；KL-到-基线项是信任域，防坍缩与奖励作弊；
全程不对 θ 求梯度——这正是「免训练」。（英文区给出 A/B 两类算子的动作空间，不重复。）

**解耦形式化。** 把可证伪主张写成不等式 `A_t(e_t) > A_t(e_{t'})`（t≠t'，间隔≥δ，p<0.05）：朝任务 t 条件化
得到的嵌入，在 t 的探针上要显著优于朝别的任务条件化的嵌入。充分条件：(P) 因子存在、(L) 可线性/浅层解码、
(S) 可被条件化引导（S 已部分确认——模型接受随音频附带的文本指令）。**抑制反例（关键风险）：** 检索编码器常被
训练成对说话人/信道/情感不变，若 `I(e;y_说话人)≈0` 则 (P) 不成立，任何冻结向量算子都无法恢复说话人，该因子
必须改用 B 类。这由 CREMA-D 试点（Track E.4）裁定。

**算法综述与逐因子决策**见英文区表格（TTRL/TPO/JitRL/MBR/best-of-N 的 A?/B?/修正/收敛性，及验证标记），
由 D.2 工作流补全、D.3 给出逐因子 A/B/混合结论。试点为 CREMA-D 双因子（同音频说话人+情感）验证闭环。
