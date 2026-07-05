---
title: "Can adjusting the conditioning A realize the frozen omni's oracle-δ? — Stage-1 directional (Phase 2 of Q1)"
date: 2026-07-05
stage: 1-directional
status: VERDICT (directional) — returned to owner; Stage-2 confirmation required; pending strict review
question: "Given confirmed per-instance oracle-δ, can adjusting A (few-shot ICL / prompt-opt / two-system verifier) convert it into a deployable ≥+10% greedy gain? → branch 2.1 vs 2.2"
prereg: "[[2026-07-05-stage1-A-realization-prereg]] (frozen before runs)"
verdict: "ICL/prompt A-adjustment INSUFFICIENT (E7/E8 fail); the training-free TWO-SYSTEM (agentic) verifier realizes ~50% of the headroom the single model couldn't (E10) → design an omni agentic system (branch 2.2, with a positive seed). Directional, n=24-30."
---

# Can adjusting A realize the oracle-δ? (Phase-2 of the Q1 study)

> Continues [[2026-07-04-Q1-conclusion-ICL-sufficiency-omni]]. Phase-1: (a) real oracle-δ exists,
> (b-text) naive prompting inert, (c) cheap self-referential selection ≈ 0. Owner reframe (2026-07-05):
> instead of *selecting* the good answer (the (c) wall), can we **adjust A so the good answer becomes
> modal** (greedy)? This phase tests that, training-free, on the non-saturated zh+en surfaces, against
> the frozen P1 bar (relative +10%). **All numbers Stage-1 directional (n=24–30, single model/quant).**

## 1. Baselines — the δ ceilings each lever aims for (P2, n=150)
| Surface | lang·family | greedy | oracle-δ | status |
|---|---|---|---|---|
| big-bench-audio | en · spoken-reasoning | 0.567 | **+0.280** | non-sat |
| mmau-mini | en · SQA-reasoning | 0.653 | **+0.147** | non-sat |
| SQuAD-zh | zh · extractive QA | 0.753 | **+0.140** | non-sat |
| vocalbench-zh | zh · knowledge QA | 0.467 | **+0.107** | non-sat |
| spoken-squad | en · extractive QA | 0.873 | +0.087 | near-ceiling (not lever-tested) |
| OpenbookQA-zh / minds14-zh | zh · MCQ / SLU | 0.97 / 0.94 | ≈0 | SATURATED (demoted) |

## 2. Theory anchors (Lean, machine-checked, sorry-free)
- **TH2a `BlindSpot.lean`** — omni-as-reward = two context-differentiated systems (not self-reward);
  realized → oracle as the shared-knowledge blind-spot fraction → 0; the constraint is the achievable
  error-**decorrelation**. Residual floor = knowledge blind-spot (PARKED → W4).
- **TH2 `Reachability.lean`** — the **(b) mode-shift** theorem + the **(b)-cap**
  (`too_improbable_unreachable`): bounded conditioning cannot promote a too-improbable good answer to
  greedy → the theory pairing for E7/E8 failing.

## 3. Results (each traces to `_repro/*.json`)
### E7 — multimodal few-shot ICL (the owner's key lever): NEGATIVE
| Surface | 0-shot | 2-shot | Δgreedy | b2−b1 floor |
|---|---|---|---|---|
| mmau-mini | 0.833 | 0.800 | −0.033 | +0.033 |
| SQuAD-zh | 0.733 | 0.733 | +0.000 | +0.067 |
| big-bench-audio | 0.700 | 0.667 | −0.033 | +0.000 |
| vocalbench-zh | 0.533 | 0.267 | −0.266 | −0.033 |
→ **Audio few-shot ICL never lifts greedy** (3 hurt, 1 neutral); 0% deployable gain, far below +10%.
Real exemplars beat the shuffled floor by a little (weak task signal) but it never converts —
consistent with TH2's (b)-cap and the added difficulty of multimodal ICL.

### E8 — in-fence global prompt optimization (dev-scored system-prompt search): NEGATIVE
Test gain **+0.000 on every surface** (the search never beat the base prompt). Transfer 0.82–1.14.
→ Global prompt optimization does not move greedy either. (Consistent with Phase-1 prompt-space ≈ 0.)

### E10 — generator/verifier TWO context-differentiated systems + decorrelation ablation: WEAK PARTIAL
| Surface | greedy | oracle | δ | ρ_isolated | ρ_coupled | isolation gain |
|---|---|---|---|---|---|---|
| SQuAD-zh | 0.750 | 0.833 | 0.083 | **0.50** | 0.00 | **+0.042** |
| big-bench-audio | 0.500 | 0.583 | 0.083 | **0.50** | 0.50 | +0.000 |
| vocalbench-zh | 0.667 | 0.708 | 0.042 | 0.00 | 0.00 | +0.000 |
| mmau-mini | 0.750 | 0.750 | 0.000 | (n/a: δ=0 in slice) | — | — |
→ On the two surfaces with real headroom in this small slice, the **isolated (context-differentiated)
verifier realizes ~50% of the oracle-δ** — a meaningful contrast with Phase-1's self-referential
selectors (E4: ρ ≈ 0). On SQuAD-zh, isolation beats the coupled verifier (+0.042: context
differentiation decorrelates, as TH2a predicts). **But it is weak, inconsistent (ρ=0 on the low-δ
surface), and very noisy at n=24** — directional only.

## 4. Verdict (Stage-1 directional — returned to owner; Stage-2 confirmation required)

**Q1 (the owner's question), answered for this phase:**

1. **Is ICL sufficient for training-free RL on the frozen omni's semantic layer? — No.** Adjusting the
   conditioning A by **prompting** does not realize the model's real latent headroom: multimodal
   few-shot ICL (the key lever) *hurts* greedy (E7), and in-fence global prompt-optimization yields 0%
   (E8). The good answers exist in the pool (oracle-δ +0.11…+0.28) but bounded prompt-reweighting cannot
   promote them to greedy — measured, and machine-checked as TH2's (b)-cap.

2. **Should an omni agentic system be designed? — Yes, and with a positive (not merely default) seed.**
   The one lever that realizes any headroom is the **training-free two-system composition** (a
   context-differentiated generator + verifier — already an agentic move): it realizes **~50% of the
   oracle-δ** on the surfaces with real headroom, where the single model's self-selection realized ≈ 0
   (E4). Context isolation decorrelates the verifier from the generator (TH2a), giving a real, if weak,
   realization the single model cannot. So the agentic direction is warranted not as "prompting failed,
   fall back to agents," but because **the two-system composition demonstrably harvests headroom that
   ICL/self-selection cannot.**

**This is branch 2.2** — design an omni agentic system — with the shape the theory prescribes:
context-differentiated composition to drive decorrelation (τ down, ρ up), and the **residual shared
knowledge blind-spot filled by an independent-of-M signal — the omni-embedding system (W4)** — which
requires defining new omni agentic tasks (PARKED, [[Theory-Convergence-and-Constraints]] · task #37).
`gain_product` is respected: the gain comes from the generator-verifier composition (not covered by the
inertness theorem) and, ultimately, a genuinely new independent reward, not from stacking isolated
agents.

**Confidence & limits.** Stage-1 directional: n=24–30 on the levers, single model / single quantization,
E10 inconsistent across surfaces and noisy (one ρ is a div-by-0 artifact on a δ=0 slice). This **settles
nothing** statistically (CLAUDE.md); it is a directional signal for the owner. Stage-2 must confirm the
E10 two-system realization at powered n with the isolated-vs-coupled ablation before any build commitment.

## 中文摘要
**问题:** 调 A 能否把已确认的 oracle-δ 变成可部署 greedy 增益。**结果(Stage-1 方向性,n=24–30):**
① **prompt 类 A-调整不足**——多模态 few-shot(主人关键杠杆)不升反降(E7),in-fence 全局 prompt 优化
+0.0%(E8);好答案在池中但有界 prompt 重加权推不上去(实测 + TH2 (b)-cap 机器验证)。② **两系统组合
(上下文差异化 generator/verifier,已是 agentic)是唯一实现头room 的杠杆**:在有真实 δ 的两个面上实现
**~50% 的 oracle-δ**(ρ_iso=0.5),而单模型自选(E4)≈0;SQuAD-zh 上隔离胜过耦合(+0.042,去相关如 TH2a
所料)——真实但弱且噪声大。**判定:** Q1=**ICL 不足**;**应设计 omni agentic system**(分支 2.2,带正向种子:
两系统组合能取到 ICL/自选取不到的头room),按理论走上下文差异化去相关,残余知识盲区用 W4 omni-embedding
独立信号补(park #37)。**Stage-1 方向性,settle 不了统计,须 Stage-2 夯实。**
