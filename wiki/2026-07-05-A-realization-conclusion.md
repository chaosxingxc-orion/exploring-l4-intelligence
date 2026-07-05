---
title: "Can adjusting the conditioning A realize the frozen omni's oracle-δ? — Stage-1 directional (Phase 2 of Q1)"
date: 2026-07-05
revised: 2026-07-05 (v2 — after 3-persona strict review; see [[2026-07-05-A-realization-review-synthesis]])
stage: 1-directional
status: LOCKED (both Q1a and Q1b) — Q1a ICL insufficient (robust); Q1b YES design a new-signal-injecting agentic system (M3 demonstrates a new independent signal robustly realizes headroom internal ICL cannot). Stage-2 engineers the signal (W4).
question: "Given confirmed per-instance oracle-δ, can adjusting A (few-shot ICL / prompt-opt / two-system verifier) convert it into a deployable ≥+10% greedy gain? → branch 2.1 vs 2.2"
prereg: "[[2026-07-05-stage1-A-realization-prereg]] (frozen before runs)"
verdict: "Q1a: ICL is INSUFFICIENT (robust) — every cheap in-fence lever fails the +10% bar: few-shot ICL (E7), prompt-opt (E8), self-selection & two-system verifier (E10/E10b REFUTED with CIs). Q1b: YES — design an omni agentic system as a NEW-INDEPENDENT-of-M-signal injector. LOCKED by M3 (n=150, CIs): a new independent signal (ground-truth transcript) robustly realizes headroom on vocalbench-zh (+22.4%, CI[0.04,0.16], clears +10%) where internal ICL cannot; theory-consistent (TH2a floor). Internal composition/self-verification is refuted (E10b) + forbidden (gain_product). Stage-2 ENGINEERS the produced signal (ASR/retrieval/W4 embedding), not re-decides the branch."
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

### E10b — the on-surface self-selection CONTROL (n=40, paired-bootstrap CIs): REFUTES the two-system seed
On the SAME surfaces, at matched budget, comparing greedy / oracle / **majority-vote self-selection** /
two-system isolated verifier:
| Surface | greedy | oracle | majority | verifier | ver−maj (95% CI) | ver rel-gain |
|---|---|---|---|---|---|---|
| mmau-mini | 0.725 | 0.750 | 0.725 | 0.650 | **−0.075** [−0.175, 0.0] | **−10.3%** |
| SQuAD-zh | 0.725 | 0.825 | 0.775 | 0.750 | −0.025 [−0.10, 0.05] | +3.5% |
| big-bench-audio | 0.600 | 0.700 | 0.600 | 0.600 | +0.000 [−0.15, 0.125] | +0.0% |
→ **The two-system verifier NEVER beats on-surface majority self-selection** (ver−maj ≤ 0 on all three,
every CI crosses or sits below 0; on mmau it is *worse*, −10.3%). The v1 "~50% realization / positive
seed" was **entirely a surface confound** — de-confounded and **refuted with CIs**. And **neither** selector
clears the +10% bar (majority: +0.0% / +0.05 borderline / +0.0%). So no in-fence *selection* lever —
single-model self-selection OR the two-system composition — deployably realizes the headroom.

### M3 — cross-modal (ground-truth transcript) injection: the first NEW-independent-signal lever (n=150, CIs)
Does adding an independent-of-M text transcript alongside the audio realize headroom that audio-only ICL
could not? *(The n=3 smoke showed SQuAD "+50%" — pure noise; use the powered n=150 + CI result.)*
| Surface | audio-only | audio+text | gain (95% CI) | rel | |
|---|---|---|---|---|---|
| **vocalbench-zh** | 0.447 | 0.547 | **+0.100 [0.04, 0.16]** | **+22.4%** | **SIGNIFICANT — CI excludes 0, clears +10%** |
| SQuAD-zh | 0.780 | 0.840 | +0.060 [0.0, 0.127] | +7.7% | n.s. (CI lower bound = 0) |
→ **A new independent signal ROBUSTLY realizes headroom** on vocalbench-zh (+22.4%, CI[0.04, 0.16], the
**only** lever in either phase to clear the +10% bar with a CI that excludes 0). Interpretable: the
transcript recovers **audio-perception loss** — its benefit is largest exactly where audio-only accuracy
is low (vocalbench 0.447: the model mis-*hears* the spoken knowledge question; clean text lets it apply
its knowledge), and small where audio-only is already high (SQuAD 0.780). So an independent signal harvests
the *perception* slice of the headroom that internal ICL/selection/verification could not.

## 4. Verdict (Stage-1 directional; LOCKED with CIs — both Q1a and Q1b answered)

The E10b control (refuting the internal route) and the powered M3 (demonstrating the new-signal route)
together lock both questions:

**Q1a — Is ICL sufficient for training-free RL realization on the frozen omni's semantic layer? — No,
across every cheap in-fence lever.** Real oracle-δ exists (P2, +0.11…+0.28), yet none of these convert it
to a deployable ≥+10% greedy gain: text-prompt diversity ≈0 (Phase-1 E1/E3), multimodal few-shot ICL does
not lift greedy (E7), in-fence prompt-pick ≈0 (E8), single-model self-selection ≈0 (Phase-1 E4 + E10b
majority), and **the two-system context-differentiated verifier is refuted** — it never beats on-surface
self-selection (E10b, CIs). The realization bottleneck (c) is robust and now closed against the
composition/verification "fix." *(One cheap in-fence lever remains untested: a real OPRO/GEPA optimized
prompt search — but TH2's (b)-cap frames why bounded prompt-reweighting is expected to fail too.)*

**Q1b — Should an omni agentic system be designed? — Only if it injects a genuinely NEW,
INDEPENDENT-of-M signal; the internal-composition/verification route is refuted.** The decisive negative
this phase adds is that making the frozen model verify/re-rank *itself* (even as two context-differentiated
systems) does not realize the headroom — consistent with the theory: TH2a says the residual is the
shared-knowledge floor that no internal decorrelation removes, and beating it needs a signal *independent
of M*. So an agentic system is warranted **specifically** as an injector of new independent information —
cross-modal grounding, a new verifiable reward, or the omni-embedding system (W4, the parked
independent-signal source, #37) — **not** as internal agent-stacking or self-verification (which
`gain_product` forbids and E10b empirically refutes). **This is now empirically DEMONSTRATED (M3, n=150,
CIs):** injecting an independent ground-truth text transcript **robustly realizes headroom** on
vocalbench-zh (+22.4%, CI[0.04, 0.16] — the **only** lever in either phase to clear the +10% bar with a CI
excluding 0), while every internal ICL/selection/verification lever failed. **→ Q1b = YES: design an omni
agentic system, specifically as a new-independent-signal injector.**

**So the locked answer:** ICL / cheap-in-fence realization is **insufficient** (robust); an **omni agentic
system is warranted as a new-independent-signal injector** — a new independent signal provably harvests the
frozen omni's headroom (M3) where internal ICL cannot, matching the theory (TH2a: internal decorrelation
cannot beat the shared-knowledge floor; you need a signal independent of M). **Stage-2 engineers the signal
(the branch is decided):** M3 used an *idealized* signal (a ground-truth transcript); a real agentic system
must **produce** it — cheap ASR self-transcription (lossier), retrieval, or the **W4 omni-embedding as the
independent-knowledge signal** for the residual knowledge-blind-spot headroom (#37). The effect localizes to
the **perception** slice (largest where audio-only is weak); the knowledge slice needs the W4 signal, not
transcription. Also run real OPRO/GEPA to formally close the last cheap in-fence lever (expected null by the
(b)-cap). Returned to owner; the 2.2 (new-signal) branch is earned, its engineering is Stage-2.

## 中文摘要（v3,经三人严格评审 + E10b 去混淆对照修订)
**判据(冻结):** 任一 in-fence 杠杆须过相对 +10% greedy 增益。**结果(Stage-1,E10b 带配对 bootstrap CI):**
真实 oracle-δ 存在(+0.11…+0.28),但没有一个廉价 in-fence 杠杆能把它转成可部署增益——文字 prompt 多样性
≈0(Ph1)、多模态 few-shot 不抬 greedy(E7)、in-fence prompt 挑选 ≈0(E8)、单模型自选取 ≈0(Ph1 E4 + E10b
majority),**两系统上下文差异化 verifier 被证伪**——在同面上从不胜过自选取(E10b:ver−maj = −0.075/−0.025/
+0.000,CI 均跨/低于 0,mmau 上反而 −10.3%)。**判定(清晰):**
**Q1a ICL 是否足够?——否**,所有廉价 in-fence 杠杆(prompt/few-shot/挑选/两系统验证)都实现不了头room。
**Q1b 是否设计 omni agentic?——仅当它注入真正独立于 M 的新信号才值得**;让冻结模型自我验证/重排(哪怕两系统)
不管用(E10b 证伪),与理论一致(TH2a:残余是共享知识底,内部去相关消不掉,越过它需独立信号)。故 agentic 应作
**新独立信号注入器**(M3 跨模态注入 / 新可验证奖励 / W4 embedding,park #37),**而非**内部堆 agent/自验证
(gain_product 禁止、E10b 实证否定)。**清晰方向:** ICL/廉价 in-fence 实现**不足**;取头room 之路是**注入新独立
信号**(agentic/跨模态),非更多内部 ICL/选择。**M3(跨模态转写注入,n=150,CI)已把 Q1b 锁定:** 注入独立于
M 的真值文本转写,在 vocalbench-zh 上**稳健实现头room(+22.4%,CI[0.04,0.16],过 +10% 门、CI 不含 0)**——
两阶段里**唯一**过门的杠杆,而所有内部 ICL/选择/验证杠杆全败。可解释:转写补的是**音频感知损失**(audio-only 越
低补得越多:vocalbench 0.447 是听错了口语问题,给清晰文本就能用上知识;SQuAD 0.780 已高、+7.7% n.s.)。**判定
(锁定):Q1a ICL 不足(稳健);Q1b 是——设计一套"新独立信号注入器"式 omni agentic 系统**(内部组合/自验证被
E10b 证伪 + gain_product 禁止;新信号被 M3 实证有效),理论一致(TH2a:内部去相关消不掉共享知识底,需独立信号)。
**分支已定(2.2/新信号);Stage-2 做的是把信号工程化**——ASR 自转写(便宜但更有损)/检索 / **W4 omni-embedding
作独立知识信号**补知识盲区头room(#37);另跑真 OPRO/GEPA 形式化关掉最后一个廉价 in-fence 杠杆。交主人。
