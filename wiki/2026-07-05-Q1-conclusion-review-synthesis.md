---
title: "Editorial synthesis — strict review of the Stage-1 Q1 conclusion (4-persona panel)"
date: 2026-07-05
stage: 1-review
decision: MAJOR REVISION (Devil's Advocate found CRITICAL → cannot Accept)
reviews_target: "[[2026-07-04-Q1-conclusion-ICL-sufficiency-omni]]"
---

> **LOG** — Stage-1 过程记录（hypothesis-grade），非现行真源；现行结论以 [[Decision-Log]] 与 [[Per-Work-Status]] 为准。

# Editorial synthesis — strict review of the Q1 conclusion

Four independent reviewers (Methodology/stats, Domain=speech-omni-ML, Devil's-Advocate, EIC+Formal-Methods),
blind to each other, each grounded in the committed artifacts + Lean sources. Panel IRON RULE: DA CRITICAL
blocks Accept. **Decision: MAJOR REVISION.** Applied revision → [[2026-07-04-Q1-conclusion-ICL-sufficiency-omni]]
(v2), re-verification below.

## What the panel affirmed (all 4)
- **Number-tracing is exemplary** — every in-house figure reconciles exactly to the committed JSON
  (Methodology recomputed from raw `per_utt`).
- **The Lean leg is real and honestly disclosed** — cited theorems correctly stated and sorry-free; the
  single Beirami `sorry` is called out and demonstrably unused; the volunteered "(b) has no theorem"
  asymmetry is genuine candor (EIC verified toolchain/mathlib pin + single library-wide sorry).
- **The oracle(label-aware)-vs-deployable(label-free) distinction is computed correctly** and the negative
  legs are conservatively argued (best selector still n.s. → biases against the paper's own claim).
- **The FBank/MFCC feature-level leakage audit instinct is exemplary** (correctly excludes
  preemphasis/denoise/telephone).

## Consensus defects → the revision must-fix list

| # | Severity | Finding (reviewers) | Fix applied in v2 |
|---|---|---|---|
| 1 | **CRITICAL** | **E6′ +0.060 is a speed-driven artifact.** Recomputed (Meth C1, re-verified independently): oracle{original,trim}=0.640=greedy → **H=+0.000**; the entire +0.060 rides on the two speed transforms. The time-*averaged* log-mel gate (Meth C2) is length-robust by construction, so ±10% speed scores 0.993 and passes while changing duration/tempo/counts — exactly the leakage MMAU temporal/counting items are vulnerable to. The paper's "{original,trim}-only still shows headroom" is factually wrong. | Affirmative multimodal claim **withdrawn**; report H_mm collapses to 0 under genuinely-safe transforms; M1-only, speed-driven, leakage-suspect. |
| 2 | **CRITICAL** | **Category error: "space insufficient" ≠ "current weak instruments don't harvest."** (DA C2, Domain C1/C2). Text leg used **un-optimized hand-authored** K≈8 prompts, not the OPRO/GEPA reward-scored search that is the actual training-free-RL-over-prompt method (survey's "central empty cell", UNRUN). (c) panel used only **cheap self-referential** selectors, omitting the in-fence **trained-verifier / frozen-LM-MBR** class — the only selectors the survey says ever produced an in-fence positive. C4's τ is selector-specific. | Verdict **narrowed** to "un-optimized instruction diversity + cheap self-referential selection do not harvest on one MMAU surface"; the skipped stronger instruments named as the reason it is directional, not settled. |
| 3 | **CRITICAL** | **`VERDICT-LOCKED` + program pivot violates the Stage-1 rule** (DA C3, Domain M4, EIC ED-1): CLAUDE.md — small-n "can settle nothing… never automatic rollover." | Frontmatter → **DIRECTIONAL (Stage-1)**; verdict framed as returned-to-owner, not a program decision. |
| 4 | MAJOR | **`gain_product` does not license building an agentic system** (DA M5, Domain M5, EIC FM-3): it is an *inertness* result for **context-isolated, separable-reward** composition; it does NOT cover a **non-isolated τ-reducing verifier/reranker/critic** — which is exactly the (c)-lever §5 recommends. "Add a reward" ≠ "build an agentic system." | §5 **reframed**: gain_product warns against naive agent-stacking; recommendation is motivated-not-forced; branch 2.1 (better in-fence selector / optimized prompt search) is at least as supported as 2.2. |
| 5 | MAJOR | **Single informative surface** (DA M1, Domain M4): MMAU MCQ (perception) — same slice_seed — carries (a)/(b-mm)/(c); MInDS near-saturated; below the doc's own ≥2-family bar; E5/multilingual/OOD untested. | Stated as the primary limitation; verdict scoped to "one MMAU surface." |
| 6 | MAJOR | **H_fix(+0.133) and E4 headroom(+0.140) are the same measurement** (Meth M4): same oracle 116/150, same slice; greedy is temp-0 **nondeterministic** under llama.cpp MoE (E3 96 vs E4 95). Budget-mismatch on H_mm (Meth M3, Domain M1). | Reported as a single ~0.133–0.140 estimate; greedy nondeterminism + budget-mismatch disclosed. |
| 7 | MAJOR | **Best selector is an under-powered POSITIVE** (DA M2, Domain C2): self-judge ρ=0.143 (~14% of headroom), CI barely crosses 0 — reported as "confirmed 0." Same model judging itself = weakest verifier. | Reported as a Stage-2-testable directional positive; "confirmed zero" removed. |
| 8 | MAJOR (formal) | **FM-1** §5 "ρ→1 **iff** τ→0" — theorem proves only forward. **FM-2** `gain_le_of_hoeffding` is hypothesis-gated (S assumed, like Beirami) — disclose symmetrically. | "iff"→"when"; Hoeffding cap disclosed as hypothesis-gated. |
| 9 | MINOR | rms_norm excluded by arbitrary 0.98 despite owner blessing loudness-norm (DA M3); τ inferred-from-ρ circular (Domain m2); ProGRes/RECOVER/PromptingWhisper not engaged (Domain m3); audio-EXPERIMENTAL/Q8_0 confound (Meth m7); CI terminology (Meth m5); unit mixing (Domain m4); glossary (EIC ED-2). | Addressed in v2 threats/limits + wording. |

## Re-review verification (fresh adversary, v2)
A fresh verification reviewer checked v2 line-by-line against the must-fix list and **independently
re-derived the decisive recomputation** (oracle{original,trim}=0.640=greedy → +0.000; oracle{original,+both
speeds}=0.700; every cited mel-cosine matches the artifact). **Verdict: ACCEPT** — all three CRITICALs (1,2,3)
and MAJORs 4/6/7 fully addressed; no new over-claim or over-correction (v2 declines to call either (b) or the
selector class "barren", keeps both branches live). Sole note: item 6's budget-mismatch was moot after the
H_mm withdrawal but not explicitly stated in v2 — now closed with a one-line disclosure in §2(b).

## The corrected verdict (one line)
Not "ICL insufficient." On **one** MMAU MCQ surface of **one** quantized omni at **one** operating point,
**un-optimized instruction diversity and cheap self-referential selection fail to harvest a real oracle
headroom** — the open problem is **(c) realization**, and the decisive stronger in-fence instruments
(optimized reward-scored prompt search; a trained-verifier / MBR selector) were **not run**. This is a
**directional Stage-1 signal for owner discussion**, not a locked verdict and not a program pivot. The
agentic question stays open and is **not** forced by `gain_product`.
