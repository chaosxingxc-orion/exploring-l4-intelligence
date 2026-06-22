# W4 — Training-Free RL for Omni-Embedding Speech Disentanglement: Feasibility

The mathematical-feasibility argument and algorithm survey behind the flagship claim in
[[Project-Thesis]]. This page locks the **formalism** (Wave D.1); the **algorithm survey table**
and **per-factor operator decision** are completed by the survey workflow (Wave D.2/D.3) with
verified sources. Status legend for claims: ✅ self-verified · ◐ sub-agent only · ⚠ assumption ·
✗ refuted.

## 0. Bottom line (D.3 decision — from the verified survey)

**Split each factor by whether it is NATIVE to a retrieval-trained SentenceTransformer or SUPPRESSED
by its contrastive/mean-pooling objective.**

| Factor | Operator | Why |
|---|---|---|
| **content** (ASR/ST) | **A** | the factor the model was built to expose; verifiable reward (WER/hit@k) ⇒ A is monotone best-of-K, no Condorcet pathology; instruction DoF is large (best-vs-worst prompt deltas up to ~55pp) |
| **language** (LID/intent) | **A** | near-semantic, frozen-LLM probes reach ~94–97% language-ID; verifiable labels ⇒ same monotone A selection |
| **speaker** (SID) | **hybrid** | retrieval+mean-pool tends to suppress speaker, but it lives in mid/late layers → A's layer/pooling/projector search (LEACE/RLACE) can recover it; B (generative readout) when the recovered probe margin is too low; closed-set retrieval gives a verifiable reward, so avoid consensus pseudo-reward |
| **emotion** (SER) | **B** | most collapsed by retrieval training — raw frozen probe ~31%, reaches ~78% only after (forbidden) adapter training; the generative Qwen2.5-Omni Thinker readout recovers what the pooled vector lost |

Every B/consensus path must gate the **per-class plurality separatrix** (`p_correct > every wrong-class
mass`, not 2-way `p>1/2`) on a held-out CREMA-D calibration set, because a near-chance paralinguistic
factor on the same audio makes hard majority vote amplify the dominant content/speaker confound. The
decisive pilot in all four cases is the falsifiable cross-probe inequality `A_t(e_t) > A_t(e_{t'})` on
same-audio CREMA-D, with the non-target factors held fixed. _(Source: D.2 survey workflow, 11 agents,
arXiv-cited; full result archived in the run transcript.)_

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

Each row: applies to **A** (embeddings)? to **B** (generation)? the **correction** needed for speech,
and a **convergence** sketch + concrete counterexample. All rows ✅ self-verified against the cited
sources in the D.2 workflow.

| Algorithm | A? | B? | Correction for speech | Convergence / counterexample |
|---|---|---|---|---|
| **TTRL** (majority-vote pseudo-reward; updates weights) | no — no token dist / no "mode" over a vector; frozen weights forbid the GRPO step. Survives only as best-of-K over conditionings with a **verifiable** reward | partial — drop the GRPO update ⇒ collapses to MBR/self-consistency *selection*, not learning | verifiable > consensus; per-class Condorcet gate; **kill GRPO group-normalization** (it hands largest advantage to least-reliable pseudo-labels); dedup cosine-clustered candidates | amplifier of the model's existing sign per factor (Condorcet separatrix `p>` plurality); **can't create an absent factor** (cond. P). Counterexample: CREMA-D emotion, base ~28% < plurality, content-confound wins the vote → steers to the wrong emotion |
| **TPO** (test-time preference opt, frozen) | no — no decoding head to emit critiques into; dense embedders don't *obey* instructions (negative WISE −49…−11; SICR 0.1–6.9%) | yes (native) — optimize the decoded text, then export an embedding (a proxy: best text ≠ best vector) | replace the learned RM with **verifiable** rewards; on A drop the textual-gradient loop, keep only verifiable-reward selection; explicit KL cap (TPO has none) | monotone non-decreasing on the *proxy* reward (cache+argmax), converges to a rewrite-operator fixed point; true reward can fall once proxy overfits. Counterexample: instruction-invariant embedder → reward-hacks a small probe set, worse out-of-sample |
| **JitRL** (KL-closed-form logit modulation + non-param memory) | partial — `z'=z+βÂ` needs a softmax; a vector has none. Re-erect a categorical action space at the **selection** level (which instruction/pool/layer/projector) ⇒ memory-amortized best-of-N over conditionings | yes — logit tilt is native; memory amortizes advantages across episodes | verifiable reward (not the LLM-judge — biased on paralinguistics, breaks the unbiased-return assumption); cosine-kNN over audio features (not Jaccard-over-text); min-count gate before trusting the optimism bonus; entropy floor | contextual-bandit consistency to `q*(a)∝q0 exp(βÂ)` under cosine-kNN + Lipschitz; re-freezing the projector gives drift Δ=0 (cleaner than JitRL's agent setting). Counterexample: speaker⟂emotion confound in the neighborhood → selects a *speaker* embedding for emotion (Goodhart) |
| **MBR** (minimum Bayes risk, frozen) | no — no sampling distribution to draw N from; cosine-consensus = medoid (nearest mean direction), which does **not** estimate any downstream reward (agreement ≠ correctness) | yes (native home) — sample N transcripts, MBR-select, export the winner's embedding; ASR WER 0.042→0.033, ST BLEU 18.6→22.5 at N=4–8 | never reuse the utility as the eval metric (metric-bias = reward hacking); needs sample **diversity** (ε-sampling T≈1; bias–diversity decomposition); prob-weighted MBR as trust region; length-robust utility (chrF, not corpus BLEU) for short clips | SLLN: `R̂_N→E_{p_θ}[u]` at O(1/√N); converges to the *misspecified* optimum if `p_θ≠p_true`. Counterexample: homophone — 7/8 samples share the same acoustic error, MBR confidently picks the wrong consensus |
| **best-of-N / reward-guided decoding** | partial — best-of-K over the (small) conditioning/pooling/projector set; the √(log N) ceiling is brutal at tiny N | yes (native) — sample, score by verifiable reward, pick, export | verifiable > pseudo; **soft-BoN** at temperature β (tightens regret under noisy reward); cap `KL ≤ log N − (N−1)/N`; cap N at the over-optimization threshold N\*; common random numbers across candidates; mind the **re-embedding gap** (re-score the exported vector with the same probe) | soft-BoN → `q*(z)∝q0 exp(R/β)`; gain ≤ `R_max·√(KL/2)=O(√log N)`, converges to the *proxy* optimum. Counterexample (A): speaker-invariant embedder ⇒ flat reward ⇒ argmax is noise, soft-BoN collapses to uniform (no steering) |

**Cross-cutting corrections (settled):** use **verifiable rewards** (WER/exact-match/retrieval-hit/
probe-accuracy from `speechrl_common.rl`) instead of consensus/majority pseudo-rewards wherever a
ground-truth signal exists; per-class **Condorcet gate** for any consensus path; **variance reduction**
(common random numbers + a control-variate baseline) for the gradient-free 𝒵_A search; an explicit
**KL/entropy trust region** at the reward-vs-KL knee; **reward calibration** (held-out probe set; drop
medium-consensus candidates); and beware the **re-embedding gap** in Operator B (the reward must
re-score the exported vector, since best-decoded-text ≠ best-disentangled-vector).

### Key empirical findings (D.2, verified)

- **Operator A has real degrees of freedom** on a vector-output frozen model — instruction text
  (largest; best-vs-worst-prompt deltas up to ~55pp), closed-form inference-time projections
  (LEACE/RLACE/whitening), pooling, and layer selection, plus additive steering vectors. The binding
  risk is weak/uncontrolled **steerability (S)**, which is exactly what reward-guided selection fixes.
- **The objective is exact.** `J(q)=E_q[R]−β·KL(q‖q0)` has the unique maximizer `q*(z)=q0(z)exp(R/β)/Z`
  (Gibbs); both operators are estimators of this same tilted target. Best-of-N is a sampling
  approximation with `KL ≤ log N − (N−1)/N` (an upper bound) and win-rate ≤ `N/(N+1)`.
- **Model specifics confirm the design.** omni-embed-nemotron-3b merges the text prompt + audio into
  ONE Qwen2.5-Omni Thinker sequence, then masked-mean-pools to a normalized 2048-d vector — so the
  `text` conditioning provably reshapes the pooled embedding (validates `embed_batch`). Audio path =
  Whisper-style, 16 kHz mono, 128 mel.
- **Suppression risk is mechanistic, not hypothetical.** The Whisper-ASR backbone concentrates
  speaker/emotion in mid-layers and de-prioritizes them in the final/pooled layer; single-vector
  contrastive training is dominated by content/speaker variance. Speaker and phonetic content occupy
  **near-orthogonal subspaces** (avg |cos| ≈ 0.13), and speaker is **linearly removable** without
  hurting content (projecting out the speaker subspace *improved* ABX phone discrimination) — strong
  support for the LEACE/RLACE Operator-A projections.

Sources (arXiv): 2605.22544, 2410.23841 (instruction DoF / non-obedience); 2306.03819, ravfogel22a
(PMLR v162), 2104.01767 (LEACE/RLACE/whitening); 1610.01644 (linear probes); 1503.02406 (IB);
2504.16084 (TTRL), 2501.12895 (TPO), 2601.18510 (JitRL), 2510.19471 (MBR-for-ASR), 2401.01879,
2507.05913 (BoN theory); 2305.12464, 2505.19273, 2501.05310, 2410.01162, 2605.02804 (speech
disentanglement/probing); 2510.03458, Qwen2.5-Omni docs (model specifics).

## 5. Per-factor decision & pilot tests (D.3)

The decision is in §0. Selection rule from the evidence: `(P)+(L)+(S)` hold ⇒ **A**; `(P)` fails (factor
suppressed) ⇒ **B**; partial ⇒ **hybrid**. Per-factor pilot on same-audio CREMA-D (filename labels):

- **content (A)** — build `Z_A = {3–5 instructions} × {mean/last pooling} × {final, penultimate layer}
  × {raw, whitened, speaker-erasing LEACE}`; score WER + retrieval hit@1. PASS if argmax-over-`Z_A`
  beats the default-prompt baseline AND matches/beats a generative-B decode at lower compute.
- **language (A)** — FLEURS (LID) + MINDS14/SLURP (intent); PASS requires the cross-probe inequality
  `A_language(e_language) > A_language(e_content)` and vice-versa; LEACE language-erasure control.
  Escalate intent to hybrid if SLURP intent stays near chance under all A conditionings.
- **speaker (hybrid)** — sweep layer × pooling × speaker-isolating projector; verifiable closed-set
  retrieval hit@1 on the 91 filename speakers. Trigger B if best-A probe stays low or B materially
  exceeds it. Confound check: hold emotion fixed, vary speaker (ensure the axis isn't gender/channel).
- **emotion (B)** — A-side ceiling (best layer × pooling × diff-of-means steering, probe-margin on a
  held-out split) vs B-side generative emotion decode with a per-class Condorcet gate. If neither
  clears the 6-way plurality separatrix, emotion is **below the frozen model's separatrix (P fails)**
  and no operator disentangles it without an adapter — report that honestly as a negative result.

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

**算法综述与逐因子决策**见英文区表格（TTRL/TPO/JitRL/MBR/best-of-N 的 A?/B?/修正/收敛性，均经 D.2
工作流 11 个 agent 带 arXiv 来源自验证）。**D.3 逐因子结论：内容→A、语言→A、说话人→混合、情感→B**——按
「该因子是检索式 SentenceTransformer 的原生能力还是被对比/均值池化目标压制」来切分：内容/语言是模型原生
且有可验证奖励（WER/检索命中/标签），A 即单调 best-of-K、无 Condorcet 病态；情感最易被检索训练压制（冻结
裸探针约 31%，需被禁止的适配器训练才到约 78%），改用生成式 Qwen2.5-Omni Thinker 读出（B）；说话人居于
中后层、可被 LEACE/RLACE 投影恢复，故 A 的层/池化/投影搜索 + 必要时 B 读出（混合）。任何 B/共识路径都要在
留出校准集上过**逐类多数分离阈**（`p_correct >` 每个错误类质量，而非二分 `p>1/2`）。关键经验：模型把文本
指令与音频并入同一 Thinker 序列再均值池化（证实 `embed_batch` 设计）；Whisper-ASR 主干在末层弱化说话人/情感
（压制风险有据）；说话人与音素内容近正交（|cos|≈0.13）且可线性移除而不伤内容。试点＝CREMA-D 双因子同音频
交叉探针不等式 `A_t(e_t) > A_t(e_{t'})`，固定非目标因子以排除混淆。
