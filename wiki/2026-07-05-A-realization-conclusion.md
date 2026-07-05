---
title: "Can adjusting the conditioning A realize the frozen omni's oracle-δ? — Stage-1 directional (Phase 2 of Q1)"
date: 2026-07-05
revised: 2026-07-05 (v2 — after 3-persona strict review; see [[2026-07-05-A-realization-review-synthesis]])
stage: 1-directional
status: DIRECTIONAL NULL — returned to owner; does NOT close Q1 or establish the agentic branch; Stage-2 preconditions pinned
question: "Given confirmed per-instance oracle-δ, can adjusting A (few-shot ICL / prompt-opt / two-system verifier) convert it into a deployable ≥+10% greedy gain? → branch 2.1 vs 2.2"
prereg: "[[2026-07-05-stage1-A-realization-prereg]] (frozen before runs)"
verdict: "Under the frozen +10% bar, NO in-fence lever realizes the oracle-δ. But under-powered (n=24, no CIs) AND under-scoped (real OPRO/GEPA, M3 cross-modal, on-surface self-selection control all unrun) → does NOT close Q1, does NOT establish agentic. Directional null returned to owner."
---

# Can adjusting A realize the oracle-δ? (Phase-2 of Q1)

> **v2 after strict 3-persona review** ([[2026-07-05-A-realization-review-synthesis]], MAJOR REVISION).
> The v1 verdict ("design an omni agentic system — Yes, positive seed") over-reached — the same failure
> the Phase-1 review caught. Corrected below: a directional NULL, not a build recommendation.
> Continues [[2026-07-04-Q1-conclusion-ICL-sufficiency-omni]]. **All numbers Stage-1 directional
> (n=24–30 on the levers, single model/quant, no bootstrap CIs computed) — settles nothing statistically.**

## 1. Baselines — the δ ceilings each lever aimed for (P2, n=150)
| Surface | lang·family | greedy | oracle-δ | status |
|---|---|---|---|---|
| big-bench-audio | en · spoken-reasoning | 0.567 | +0.280 | non-sat |
| mmau-mini | en · SQA-reasoning | 0.653 | +0.147 | non-sat |
| SQuAD-zh | zh · extractive QA | 0.753 | +0.140 | non-sat |
| vocalbench-zh | zh · knowledge QA | 0.467 | +0.107 | non-sat |
| spoken-squad / OpenbookQA-zh / minds14-zh | — | 0.87 / 0.97 / 0.94 | ≈0 | near-ceiling / SATURATED (not lever-tested) |

Real oracle-δ exists on the 4 non-saturated surfaces (n=150, N=8). *(Note: the E10 slice at n=24, N=3
collapses these δ to ≈0.04–0.08 — a much smaller, noisier denominator; see §3.)*

## 2. Theory anchors (Lean, machine-checked, sorry-free — full library builds, 8570 jobs)
- **TH2a `BlindSpot.lean`** (verified) — the two-system realization bound: realized → oracle as the
  shared-knowledge blind-spot fraction → 0 (`avg_regret_tendsto_zero`). It **frames** the decorrelation
  constraint (the constraint quantity is the achievable error-decorrelation); it is **asymptotic** and
  does **not** predict any fixed-n E10 number, nor does it assert that context isolation *produces*
  decorrelation (its own docstring says E10 must MEASURE that).
- **TH2 `Reachability.lean`** (verified — fixed a Mathlib-rename that had made it non-compiling; the
  earlier "machine-checked" claim was wrong and is corrected) — the **(b) mode-shift** theorem + the
  **(b)-cap** (`too_improbable_unreachable`). *Scope:* it is a theorem about an **abstract multiplicative
  reweighting model** `q_A ∝ q0·w` with a stipulated bound `R`; E7/E8 never measure `w`, `R`, or `q0`.
  So it **frames** why a bounded prompt lever might fail to lift greedy — it is **not** a proven
  explanation of the data, and it models "no lift," not the "hurts/regresses" that E7 shows.

## 3. Results (each traces to `_repro/*.json`; no bootstrap CIs computed — a deviation from prereg §5)
### E7 — multimodal few-shot ICL (owner's key lever): did NOT lift greedy (in this configuration)
| Surface | 0-shot | 2-shot | Δgreedy | b2−b1 floor |
|---|---|---|---|---|
| mmau-mini | 0.833 | 0.800 | −0.033 | +0.033 |
| SQuAD-zh | 0.733 | 0.733 | +0.000 | +0.067 |
| big-bench-audio | 0.700 | 0.667 | −0.033 | +0.000 |
| vocalbench-zh | 0.533 | 0.267 | −0.266 | −0.033 |
→ No surface shows a lift. **Caveat (review):** the ±0.033 deltas are *within* the disclosed temp-0 MoE
decode noise (mmau greedy reads 0.653/0.833/0.800/0.75 across runs), only k=[0,2] was run (not the
prereg shot-curve), MAXTOK=64 truncates reasoning, and demos are concatenated audios in one message
(non-standard ICL) — the vocalbench −0.266 is plausibly a multimodal-attention pathology. So the honest
reading is "**few-shot did not lift greedy in this configuration**," not "few-shot fundamentally hurts."

### E8 — in-fence prompt optimization: null, but UNINFORMATIVE
Test gain +0.000 on every surface. But this was a **4-candidate system-prompt pick on dev n=20** — **not**
OPRO/GEPA (iterative, feedback-driven search). Near-zero search power → its null disconfirms nothing.

### E10 — generator/verifier two context-differentiated systems: SUB-THRESHOLD, confounded
| Surface | greedy | verifier(iso) | rel gain | ρ_iso | isolation−coupled |
|---|---|---|---|---|---|
| SQuAD-zh | 0.750 | 0.792 | **+5.6%** | 0.50 | +0.042 (1 item) |
| big-bench-audio | 0.500 | 0.542 | **+8.3%** | 0.50 | +0.000 |
| vocalbench-zh | 0.667 | 0.667 | +0.0% | 0.00 | +0.000 |
| mmau-mini | 0.750 | 0.708 | **−5.6%** (worse) | (δ=0 slice) | — |
→ **Under the frozen +10% bar, E10 clears NOTHING** (best +8.3%). The realization is **net +1 correct
item / 24** on 2 surfaces, with **no CI** (flip 1 item and it vanishes), **ρ=0 on the low-δ surface**,
and **worse than greedy on mmau**. Isolation beat the coupled verifier on **one surface, one item**
(SQuAD +0.042); on big-bench isolation=coupled → the decorrelation mechanism has essentially no support.
**Crucially, no on-surface self-selection control was run** — E4's self-selection ≈0 was on MMAU (zero
overlap), so this does NOT establish "two-system > self-selection"; the gap could be entirely surface.
ρ here is a *realization fraction*, not the error-correlation TH2a is about.

## 4. Verdict (Stage-1 directional — returned to owner; NOT a branch decision)

**By the frozen P1 rule, no in-fence lever (few-shot ICL, prompt-opt, two-system verifier) realizes the
oracle-δ to the deployable +10% bar.** But two things stop this from answering Q1:

1. **Under-powered.** n=24–30, no bootstrap CIs (a prereg deviation); the lever deltas sit inside the
   model's own temp-0 decode noise. Settles nothing statistically.
2. **Under-scoped.** The **decisive in-fence instruments were never run** — a real OPRO/GEPA optimized
   prompt search, M3 cross-modal (transcript/lattice) injection (the survey's strongest lever), the full
   few-shot shot-curve, and — critically — an **on-surface self-selection control** for E10. Until these
   run, "ICL is insufficient" is **not established**, and the E10 "two-system advantage" is **confounded**.

**So the honest answer to the owner's Q1, for this phase:**
- **Is ICL sufficient? — Undetermined, leaning "the limited levers we ran do not realize the headroom."**
  Not a proof of insufficiency: the strong pro-realization in-fence instruments are untested.
- **Should an omni agentic system be designed? — Not answered here.** E10 is a **branch-2.1** verifier/MBR
  selector (the framing books it in-fence), not an agentic system; it **failed** the frozen bar, and its
  weak sub-threshold signal — if anything — says **branch 2.1 (better in-fence selection) is under-tested**,
  not that 2.2 is warranted. The agentic question remains **open**.

**Mandatory Stage-2 preconditions before any branch decision (the value this phase delivers):** run, with
powered n and paired-bootstrap CIs — (a) a real OPRO/GEPA prompt search; (b) M3 cross-modal injection;
(c) the full few-shot shot-curve with a proper multi-turn ICL format + raised token cap; (d) E10 **with an
on-surface self-selection control** and the isolated-vs-coupled ablation with CIs. Only then is the
2.1-vs-2.2 branch decision earned. Returned to owner; no auto-rollover.

## 中文摘要（v2,经三人严格评审修订)
**判据(冻结):** 任一 in-fence 杠杆须过相对 +10% greedy 增益。**结果(Stage-1,n=24–30,无 CI):** E7 多模态
few-shot 未抬 greedy(且落在 temp-0 解码噪声内,只跑了 k=[0,2]);E8 只是 4 候选 system-prompt 挑选、非
OPRO/GEPA,零信息量;E10 两系统 verifier **全部低于 +10%**(SQuAD +5.6%、big-bench +8.3%)——是每面 24 题里
净 +1 题、无 CI、低-δ 面 ρ=0、mmau 上反而更差,隔离胜耦合仅 1 面 1 题,**且没跑同面自选取对照**(E4 的自选取
≈0 在 MMAU、零重叠),故**不能**断言"两系统胜过自选取"(可能全是任务差异)。**判定:按冻结判据无杠杆达标,
但既欠功效(n 小、无 CI)又欠范围(真 OPRO/GEPA、M3 跨模态注入、完整 shot-curve、同面自选取对照全没跑)——
故既未关闭 Q1、也未确立 agentic 分支。E10 是分支-2.1 的 verifier/选择器(非 agentic)且未达标,其弱信号若有
所指是"2.1 欠测",非 2.2。** 交主人;**Stage-2 前置(powered n + 配对 bootstrap CI):真 OPRO/GEPA、M3 注入、
完整 shot-curve、E10 带同面自选取对照 + 隔离/耦合消融——跑完才谈分支。无自动滚入。
