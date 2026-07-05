---
title: "Can adjusting the conditioning A realize the frozen omni's oracle-δ? — Stage-1 directional (Phase 2 of Q1)"
date: 2026-07-05
revised: 2026-07-05 (v2 — after 3-persona strict review; see [[2026-07-05-A-realization-review-synthesis]])
stage: 1-directional
status: CLEAR directional verdict (de-confounded with CIs via E10b); Stage-2 for the 2 remaining in-fence/agentic instruments
question: "Given confirmed per-instance oracle-δ, can adjusting A (few-shot ICL / prompt-opt / two-system verifier) convert it into a deployable ≥+10% greedy gain? → branch 2.1 vs 2.2"
prereg: "[[2026-07-05-stage1-A-realization-prereg]] (frozen before runs)"
verdict: "ICL/cheap-in-fence realization is INSUFFICIENT: every cheap lever fails the +10% bar — few-shot ICL (E7), prompt-opt (E8), self-selection & the two-system verifier (E10/E10b, the latter REFUTED with CIs as a surface confound). An omni agentic system is warranted ONLY if it injects a genuinely NEW INDEPENDENT-of-M signal (cross-modal grounding / new verifiable reward / W4 embedding) — the internal-verification/composition route is refuted. Last open in-fence test: real OPRO/GEPA. Directional (n≤40); Stage-2 confirms."
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

## 4. Verdict (Stage-1 directional; de-confounded with CIs — a clear branch answer)

The E10b on-surface control removes the one thing that had kept the verdict "undetermined." The answer is
now clear on the tested space:

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
cross-modal grounding (M3 transcript/lattice injection), a new verifiable reward, or the omni-embedding
system (W4, the parked independent-signal source, #37) — **not** as internal agent-stacking or
self-verification (which `gain_product` forbids and E10b empirically refutes).

**So the clear directional answer:** ICL / cheap-in-fence realization is **insufficient**; the path to
harvesting the frozen omni's real headroom is a **new-independent-signal** injection (agentic or
cross-modal), not more internal ICL/selection. **Two Stage-2 tests remain to lock it** (powered n, CIs):
(a) a real OPRO/GEPA prompt search — the last cheap in-fence lever; (b) an M3 cross-modal-injection /
W4-embedding test — the first genuinely-new-signal lever. If (a) fails and (b) succeeds, the branch-2.2
agentic/new-signal direction is fully earned. Returned to owner; no auto-rollover.

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
信号**(agentic 或跨模态),非更多内部 ICL/选择。**两个 Stage-2 收尾测试(powered n + CI):**(a) 真 OPRO/GEPA
——最后一个廉价 in-fence 杠杆;(b) M3 跨模态注入 / W4-embedding——第一个真·新信号杠杆。若 (a) 败 (b) 成,
分支-2.2(agentic/新信号)完全坐实。交主人;无自动滚入。
