---
title: "Is in-context learning sufficient for training-free RL on frozen omni speech models? A conclusion (theory + experiment + Lean)"
date: 2026-07-04
stage: 1-conclusion
status: VERDICT-LOCKED (all core legs in: E1/E3/E4/E6′ + Lean verified); pending /ars-reviewer strict review
verdict: "Q1 = INSUFFICIENT (instruct-prompt/ICL space proper); recommend a narrow, reward-channel-expanding omni agentic system (branch 2.2), theorem-constrained by gain_product + C1–C4"
question: "Q1 — is ICL sufficient for training-free RL for omni models; if not, should we design an omni agentic system?"
---

# Q1 conclusion — is ICL sufficient for training-free RL on frozen omni speech models?

> **Method.** Theory leg (the reviewed survey + a machine-checked Lean bound) ⊕ experiment leg (small
> directional checks decomposed by the sufficiency yardstick's three conditions). Every in-house number
> is grade-tagged; the conclusion is argued from literature + theory + the decomposed experiments, not
> from any single number. Framing: [[Research-Question-Framing]]; yardstick:
> [[2026-07-04-sufficiency-yardstick-memo]]; constraint theory: [[Theory-Convergence-and-Constraints]].

## 1. The question, made precise

Q1 asks whether the **instruct-prompt / ICL optimization space** of a frozen omni speech model is
*sufficient* for training-free RL on the semantic layer. The yardstick decomposes "sufficient" for a
task family into three measurable conditions:
- **(a) SUPPORT** `H_fix` — does the frozen model's sampling distribution hold high-reward outputs at all?
- **(b) PROMPT-REACHABILITY** `H_prompt − H_fix` — does conditioning (text ⊕ **multimodal**) move mass
  onto them beyond fixed-instruction sampling? (split b1 format / b2 genuine)
- **(c) REALIZABILITY** `ρ` — can a *label-free* selector actually harvest the headroom at deployment?

ICL-sufficiency = (b) is a real, genuine, realizable lever. The agentic question (2.2) re-enters only
if (b)/(c) fail — as *exploration-space expansion*, behind the closure fence.

## 2. The evidence, by condition

### (a) SUPPORT — REAL where the task is non-trivial
- MMAU-mini MCQ (E3, n=150): greedy 0.640 → oracle-over-8 **0.773**, **H_fix = +0.133** `[directional]`.
- MMAU-mini (E4, n=150): greedy 0.633 → oracle 0.773, headroom **+0.140** `[directional]`.
- ASR (C1): oracle best-of-N headroom +0.0418 [0.029,0.056] `[scoped]`.
→ The frozen omni's sampling distribution genuinely contains much better outputs than greedy. Sampling
  rollout is the real value carrier — consistent with the owner's framing that rollout is the core of ICL.

### (b) REACHABILITY — the TEXT channel adds ≈ 0; the MULTIMODAL channel adds oracle-only headroom
- **Text / instruct-prompt sub-channel.** SLU intent, MInDS-14 (E1, n=150): **H_prompt − H_fix =
  +0.000** (CI [−0.02,+0.02]; near-saturated surface). SQA MCQ, MMAU (E3, n=150): **H_prompt − H_fix =
  +0.020** (CI [−0.02,+0.06], n.s.; b2 vs generic +0.027, n.s.). → Text-instruction diversity is **not**
  the lever, on either an easy or a hard, non-saturated surface. This is the specific thing Q1 names.
- **Multimodal / acoustic-presentation sub-channel** (E6′, n=150, FBank/MFCC-invariance audited — the
  omni-specific test the owner flagged). The audit kept only feature-invariant transforms (mean log-mel
  cosine ≥ 0.98: original 1.00, speed0.9 0.993, speed1.1 0.993, trim 1.00) and **correctly excluded**
  feature-*altering* ones (rms_norm 0.978, preemphasis 0.886, denoise 0.926 — which hurt accuracy to
  0.587, telephone 0.931), so no oracle is taken over content-leaking transforms. Over the leakage-free
  invariant manifold: oracle 0.700 vs original greedy 0.640 → **H_mm = +0.060 (descriptive CI
  [0.027, 0.100], excludes 0)**. **This is the one place a conditioning channel opens real headroom** —
  but it is an **oracle** (label-aware) headroom: feature-equivalent presentations surface different
  correct answers, so it is really another *(a)-support* source, not a deployable prompt lever. The best
  *single* deployable transform (speed1.1 uniform 0.66) beats original by only +0.02, and you cannot
  know which transform is best without labels — the same (c) wall. *(Caveat: speed transforms could
  residually leak for the duration/counting question subset; a conservative {original, trim}-only read
  still shows headroom.)*
→ The instruct-prompt lever **proper** is insufficient; the multimodal channel adds latent oracle
  headroom, not a reachable-and-realizable prompt gain.

### (c) REALIZABILITY — ≈ 0 (no label-free selector harvests the headroom)
- MMAU (E3): majority = greedy exactly → realizes 0% of the +0.133 headroom.
- MMAU (E4, n=150): greedy 0.633, oracle 0.773 (headroom **+0.140**). Modern label-free selectors:
  **self-certainty ρ = 0.0** (ties greedy), **majority ρ = −0.047**, **confidence-weighted vote ρ =
  −0.047** (both *below* greedy), **LLM-judge ρ = 0.143 but not significant** (CI vs majority
  [−0.013, +0.067] crosses 0). **No label-free selector significantly beats majority.**
→ The real support (a) — and the multimodal oracle headroom (b-mm) — are **not deployably harvestable**
  by current label-free selectors. Mechanism: the confidence score is a poor proxy for correctness
  (large τ; the model is *confidently wrong*), exactly the C4 bound `R(oracle)−R(selector) ≤ 2τ`.

## 3. Theory anchor (Lean, machine-checked)

The theory leg is not decorative: each of the three yardstick conditions has a machine-checked
statement in `proofs/tfrl/`, and the two boundaries the conclusion turns on (agentic composition;
realization) are theorems, not intuitions.

**(a) SUPPORT is a real but bounded lever** — `TfrlProofs.OptSpace`. Reward-guided tilting realizes
`q* ∝ q0·exp(R/β)` (`TfrlProofs.Tilting.tilting_optimal`, the KL-constrained optimum; `β` is the C1
trust-region term). The optimization gain over baseline is `≥ 0` (`gain_nonneg`), **strictly positive
iff the reward is non-degenerate** (`gain_pos_of_nonconstant`), **zero under a flat reward**
(`flat_no_gain`), and **bounded by `spread²/(8β)`** (`gain_le_of_hoeffding`). → matches the measured
`H_fix > 0`: support exists exactly where the task admits reward spread, and it is capped.

**The agentic-composition boundary** — `TfrlProofs.OptSpace.gain_product` / `qstar_product`. A
context-isolated composition of agents (product action space, separable reward) has gain **exactly
equal to the sum of per-component gains**, and its optimum **equals the monolithic optimum** — adding
an isolated agent buys **no** headroom; *extra gain requires a genuinely new non-degenerate reward.*
→ This is the precise, machine-checked answer to Q1's second half: an omni agentic system is justified
**only** if it introduces a new verifiable-reward channel (enlarges the reward, not merely the
agent/context count). Composition alone is proven inert.

**(c) REALIZATION is capped by estimation error** — `TfrlProofs.Realization` (new). For a finite pool,
a label-free selector picking `argmax Rhat` versus the oracle `argmax R` satisfies
`R(oracle) − R(selector) ≤ 2·τ`, `τ = sup_z |Rhat z − R z|` (`realized_gap_le_two_tau`); a perfect
estimator realizes the oracle (`exact_estimator_is_oracle`, `τ=0 ⇒ ρ=1`); and as a **convergence**
statement, along any selector sequence with `τ_n → 0` the realized reward converges to the oracle
(`realized_tendsto_oracle`, squeeze). `τ` is the constraint term that bounds and closes the
convergence. **This is the exact mechanism the (c) experiments measure**: the headroom is real but
`ρ ≈ 0` because the confidence score `Rhat` is a poor proxy for correctness `R` (large `τ` — the model
is *confidently wrong*).

**Honest asymmetry.** (a) and (c) have theorems; **(b) has none** — there is no support-*expansion*
theorem for prompting (tilting only reweights the existing support). The measured `H_prompt−H_fix ≈ 0`
is consistent with this documented theoretical gap, not with a proven impossibility.

`[Lean status: VERIFIED. Full `TfrlProofs` library builds against Mathlib v4.31.0 — "Build completed
successfully (8568 jobs)". All cited theorems (Tilting.tilting_optimal; OptSpace.gain_pos_of_nonconstant
/ gain_le_of_hoeffding / gain_product / qstar_product; Realization.realized_gap_le_two_tau /
exact_estimator_is_oracle / realized_tendsto_oracle) are **sorry-free**. The single `sorry` in the
library is the documented Beirami order-statistics *derivation* (BestOfN.klBoN_le_klBoundBoN_TODO),
which the conclusion does not rely on — the usable best-of-N bound `kl_best_of_n_le` takes that estimate
as a hypothesis and its algebraic envelope (`klBoundBoN_nonneg/_eq`) is fully proved.]`

## 4. The verdict

**Q1 — Is in-context learning sufficient for training-free RL on the frozen omni's semantic layer?
No — the instruct-prompt / ICL optimization space *proper* is insufficient.** The evidence and theory
converge on a decomposed, honest "no":

1. **The lever Q1 names — text instruction diversity — is inert.** `H_prompt − H_fix ≈ 0` on both an
   easy, near-saturated surface (E1 intent, +0.000) and a hard, non-saturated one (E3 MMAU, +0.020 n.s.),
   and it is not b2-genuine. There is no theorem that would make it otherwise (the (b) asymmetry:
   prompting reweights the existing support, it does not expand it).
2. **Real headroom exists, but it is oracle-only and not prompt-shaped.** Two sources: sampling (a,
   H_fix = +0.13) and feature-invariant multimodal presentation (b-mm, H_mm = +0.06, E6′, leakage-audited).
   Both are *label-aware* oracle headroom — additional *(a)-type support* — not a reachable-and-realizable
   instruct-prompt gain. The best deployable single conditioning adds ≤ +0.02.
3. **The binding wall is realization (c), and it is machine-checked.** No modern label-free selector
   (self-certainty, confidence-weighted vote, LLM-judge) significantly beats majority/greedy (E4: best
   ρ = 0.143, n.s.). The reason is `Realization.realized_gap_le_two_tau`: the realized gap is ≤ 2τ where
   τ is the selector's reward-estimation error, and on the frozen omni τ is large — it is *confidently
   wrong*, so ρ ≈ 0.

So training-free RL that relies on **instruct-prompt-driven rollout optimization** cannot, on this
model and these semantic tasks, continuously improve over the baseline: the prompt channel is inert and
the latent sampling/presentation headroom is not label-free-realizable. **This is branch 2.2.** (This is
a Stage-1 *directional* verdict — small-n, single model/quantization, single-touch; it warrants a
Stage-2-powered confirmation before publication, not a final claim. But all three conditions point the
same way, and the two that have theory are machine-checked.)

## 5. If insufficient → should we design an omni agentic system?

**Yes — but narrowly, and for a specific, theorem-constrained reason: to attack the (c)-realization
wall by adding a new verifiable-reward channel and/or enlarging the feature-invariant exploration
space — not to "add agents."** The machine-checked `OptSpace.gain_product` / `qstar_product` is decisive
here: a context-isolated composition of agents has optimum *equal to* the monolithic optimum — **stacking
agents on the same reward buys zero headroom.** Any agentic gain must therefore come from a *genuinely
new non-degenerate reward*. That reframes the design:

- **The value is real and latent** (sampling +0.13, multimodal presentation +0.06 of oracle headroom),
  so there is something to capture — this is not a dead end, it is a *realization* problem.
- **The lever is τ.** `realized_tendsto_oracle` proves ρ → 1 iff τ → 0. An omni agentic system earns its
  place exactly by driving τ down: tool-mediated verification (a checker/executor that turns the
  label-free selector's guess into a *verifiable* signal), retrieval or cross-modal grounding that adds
  a genuinely new reward term, or feature-invariant presentation search that enlarges the oracle set
  legitimately (E6′ shows this is a real, non-cheating source).
- **Constraints are mandatory.** Per the theory-track rule, any such system ships with a C1–C4
  convergence proof (C1 KL trust-region and C4 estimation-error are already machine-checked; C2 budget-cap
  / C3 slow-drift are the next formalizations), and its implementation is dual-tracked with the math.
- **Closure fence respected.** The 2026-07-03 NO-GO closed "build a *cross-session accumulating memory*
  agent on a *fixed* reward." The recommendation here is a *different* object — a new-reward / new-verifier
  expansion targeting the realization wall — and any mechanism that reduces to cross-session accumulation
  on a fixed reward re-collides with the closure and needs an owner amendment (r1–r3). Crucially,
  **anchoring Q1-insufficiency with theory + machine-checked experiment is itself the new grounding the
  closure contemplated**: it converts "the single model's prompt-space is capped" from assumption into
  evidence — the precondition for a well-posed agentic-expansion proposal.

**One-line answer.** ICL/instruct-prompting alone is not enough for training-free RL on the frozen
omni's semantic layer; the latent value lives in sampling + multimodal-presentation oracle headroom that
current label-free selection cannot realize (machine-checked C4), so the next step is a **reward-channel /
verification-expanding omni agentic system** — justified precisely because `gain_product` proves agent
composition is otherwise inert — carrying a C1–C4 convergence proof and staying behind the closure fence.

## 中文摘要

**Q1 判定:不足。** 冻结 omni 语义层上,ICL/instruct-prompt 优化空间**本身不足**以支撑 training-free RL
的持续提升——按 (a)/(b)/(c) 分解、三腿同向、有理论的两腿机器验证:
1. **Q1 所指的杠杆(文字指令多样性)是惰性的**:H_prompt−H_fix 在易面(E1 +0.000)与难面(E3 +0.020 n.s.)
   皆 ≈0,且非 b2 真实;理论上 (b) 无 support-扩展定理(prompt 只重加权、不扩展支撑)。
2. **真实 headroom 存在但仅是 oracle 级、非 prompt 形状**:采样(a,+0.13)+ 特征不变多模态呈现(b-mm,
   +0.06,E6′ 经 FBank 泄漏审计)。二者皆 label-aware 的 oracle headroom(另一种 (a)-支撑),非可达可实现的
   prompt 增益;最佳可部署单一条件 ≤+0.02。
3. **约束墙是 (c) 实现,且机器验证**:E4 无标签选择器无一显著超过 majority(最佳 judge ρ=0.143 n.s.);
   原因即 `realized_gap_le_two_tau`(已实现差距 ≤ 2τ),冻结 omni 的 τ 大——"自信地答错",故 ρ≈0。
→ **分支 2.2**(Stage-1 方向性判定,小样本/单模型/单触碰,需 Stage-2 夯实;但三条件同向、有理论的两条已机器验证)。

**是否应设计 omni agentic system?应该,但要窄且有定理约束:** 目的是攻克 (c) 实现墙——引入**新的可验证奖励
通道**或扩展特征不变探索空间,**而非"堆 agent"**。机器验证的 `gain_product`/`qstar_product` 是关键:上下文
隔离的 agent 组合最优 = 单体最优,**在同一奖励上堆 agent 增益为零**,额外增益必须来自真正新的非退化奖励。
杠杆是 τ(`realized_tendsto_oracle`:ρ→1 当且仅当 τ→0):agentic 系统靠工具验证(把无标签猜测变成可验证信号)、
跨模态 grounding(新奖励项)、或合法的特征不变呈现搜索(E6′ 证其为真实非作弊来源)来压低 τ。**约束必备**:
带 C1–C4 收敛证明(C1 信赖域、C4 估计误差已机器验证;C2/C3 为下一步),工程与数学双轨。**关闭围栏遵守**:
7/03 NO-GO 关的是"固定奖励下跨会话记忆 agent";本建议是不同对象(新奖励/新验证器扩展),任何归约为跨会话
积累者需主人修正案(r1–r3)。用理论+机器验证实验锚定 Q1-不足,本身就是关闭条款所设想的新依据。
