---
title: "Can adjusting the conditioning A realize the frozen omni's oracle-δ? — Stage-1 directional (Phase 2 of Q1)"
date: 2026-07-05
stage: 1-directional
status: DRAFT-IN-PROGRESS (E7 landing negative; E8/E10 running; verdict pending)
question: "Given confirmed per-instance oracle-δ, can adjusting A (few-shot ICL / prompt-opt / two-system verifier) convert it into a deployable ≥+10% greedy gain? → branch 2.1 vs 2.2"
prereg: "[[2026-07-05-stage1-A-realization-prereg]] (frozen before runs)"
---

# Can adjusting A realize the oracle-δ? (Phase-2 of the Q1 study)

> Continues [[2026-07-04-Q1-conclusion-ICL-sufficiency-omni]]. Phase-1 established: (a) real oracle-δ
> exists, (b-text) naive prompting inert, (c) cheap label-free selection ≈ 0. The owner reframed the
> next question (2026-07-05): rather than *select* the good answer post-hoc (the (c) wall), can we
> **adjust A so the good answer becomes modal** (greedy), avoiding selection? This phase tests that,
> training-free, on the non-saturated zh+en surfaces, against the frozen P1 bar (relative +10%).

## 1. Baselines — the δ ceilings each lever aims for (P2, n=150, committed)
| Surface | lang·family | greedy | oracle-δ | in coverage? |
|---|---|---|---|---|
| mmau-mini | en · SQA-reasoning | 0.653 | **+0.147** | ✓ |
| big-bench-audio | en · spoken-reasoning | 0.567 | **+0.280** | ✓ |
| SQuAD-zh | zh · extractive QA | 0.753 | **+0.140** | ✓ |
| vocalbench-zh | zh · knowledge QA | 0.467 | **+0.107** | ✓ |
| spoken-squad | en · extractive QA | 0.873 | +0.087 | (near-ceiling) |
| OpenbookQA-zh | zh · MCQ | 0.973 | +0.000 | SATURATED (demoted) |
| minds14-zh | zh · SLU intent | 0.940 | +0.007 | SATURATED (demoted) |

Real, sizeable oracle-δ exists on the 4 non-saturated surfaces (+0.107 … +0.280). The frozen model
holds much better answers than greedy; the question is whether adjusting A promotes them to greedy.

## 2. Theory anchors (Lean, machine-checked, sorry-free)
- **TH2a `BlindSpot.lean`** — omni-as-reward = TWO context-differentiated systems (generator/verifier),
  not self-reward; realized reward → oracle as the shared-knowledge blind-spot fraction → 0
  (`avg_regret_tendsto_zero`); the constraint is the achievable error-decorrelation. Residual floor =
  the knowledge blind-spot (PARKED → W4).
- **TH2 `Reachability.lean`** — the **(b) mode-shift** theorem: adjusting A (reweighting `w`) makes the
  good answer `z*` greedy iff `w(z*)/w(m) > q0(m)/q0(z*)`; and the **(b)-cap**
  (`too_improbable_unreachable`): if `z*` is too improbable under the frozen base relative to A's bounded
  reweighting power, **no** conditioning makes it greedy. → the theory pairing for a null/negative A-lever.

## 3. Results (Stage-1 directional; each traces to `_repro/*.json`)
### E7 — multimodal few-shot ICL (the owner's key lever) — NEGATIVE so far
Few-shot audio demos do **not** lift greedy toward oracle; they **degrade** it:
| Surface | 0-shot greedy | 2-shot greedy | b2−b1 floor |
|---|---|---|---|
| mmau-mini | 0.833 | 0.800 | +0.033 |
| vocalbench-zh | 0.533 | 0.267 | −0.033 |
| SQuAD-zh | <pending> | <pending> | <pending> |
| big-bench-audio | <pending> | <pending> | <pending> |
→ Directional read: audio few-shot ICL is counterproductive on the frozen omni — far below the +10%
bar, negative. Consistent with TH2's (b)-cap (bounded conditioning can't promote the good answers) and
with the added difficulty of multimodal ICL (extra audio contexts degrade attention). *(pending 2 surfaces)*

### E8 — in-fence global prompt optimization (dev-scored system-prompt search) + transfer
<RESULT PENDING — running>

### E10 — generator/verifier two-system + isolated-vs-coupled decorrelation ablation
<RESULT PENDING — running>. Key readouts: ρ_isolated (realized oracle-δ fraction), isolation gain over
coupled (does context differentiation decorrelate → lower τ?), catch-rate on the generator's errors.

## 4. Verdict <PENDING E8/E10 + dec_synthesis + strict review>
<The mechanical P1 rule (relative +10%, b2-genuine, transfer, majority of non-saturated surfaces) is
applied by dec_synthesis. Emerging shape: E7 (few-shot) fails/hurts → the owner's key A-lever does not
realize the δ. If E8 (prompt-opt) and E10 (two-system verifier) also fail the bar → adjusting A does NOT
convert the oracle-δ to a deployable gain → branch 2.2 (agentic reward/verification expansion, with the
residual knowledge floor parked → W4). If E10's isolated verifier realizes ≥ρ_min via decorrelation →
the two-system route is the realization lever (a training-free agentic composition) → a 2.1/2.2 hybrid.
Locked only after the 4-persona strict re-review.>

## 中文摘要 <待锁定>
<问题:调 A 能否把已确认的 oracle-δ 变可部署 greedy 增益。P2 基线:4 个非饱和面有真实 δ(+0.107…+0.280)。
理论:TH2a 两系统去相关收敛 + TH2 (b) 可达性与 (b)-cap。E7(多模态 few-shot,主人关键杠杆)方向性为负——
不升反降。E8/E10 运行中。判定待 E8/E10 + dec + 严格评审。>
