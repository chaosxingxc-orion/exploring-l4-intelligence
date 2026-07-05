---
title: "Editorial synthesis — strict review of the A-realization verdict (3-persona panel)"
date: 2026-07-05
decision: MAJOR REVISION (2 CRITICAL: non-compiling Lean falsely labeled verified; confounded causal claim + post-hoc threshold)
reviews_target: "[[2026-07-05-A-realization-conclusion]]"
---

# Editorial synthesis — strict review of the A-realization verdict

Three independent reviewers (methodology/stats, devil's-advocate, EIC+formal), grounded in the artifacts,
Lean sources, and scripts. **Decision: MAJOR REVISION.** The review again caught an over-reach toward the
agentic branch — the same failure mode as the Phase-1 review. All findings accepted; corrections applied.

## What the panel affirmed
- **Number tracing is exact** (all P2/E7/E8/E10 figures reconcile to the JSON).
- **The mechanical negative direction is correct**: under the frozen +10% bar, no in-fence lever clears.
- **TH2a (`BlindSpot.lean`) is genuinely machine-checked** (verified green, sorry-free).
- Honest Stage-1 "settles-nothing" hedging is prominent and consistent.

## The defects → corrections applied

| # | Sev | Finding (reviewer) | Fix |
|---|---|---|---|
| 1 | **CRITICAL** | **TH2 `Reachability.lean` did NOT compile** — `div_lt_div_iff` removed in Mathlib v4.31.0, no olean; "machine-checked" was FALSE (my earlier "exit 0" was the pipe's exit, not lake's) (EIC-formal). | **FIXED** — `lt_div_iff₀`/`div_lt_iff₀`; now builds green, olean present, sorry-free; full library 8570 jobs. |
| 2 | **CRITICAL** | **The causal claim "two-system > self-selection" is confounded** — E4 self-selection ≈0 on MMAU; E10 positives on SQuAD-zh/big-bench-audio; **zero surface overlap, no on-surface self-selection control**; on MMAU (the only shared surface) the verifier scored **0.708 < greedy 0.75 (worse)** (DA C1, Meth C2). | Causal claim **withdrawn**; reframed as "not comparable to E4; needs an on-surface self-selection control." |
| 3 | **CRITICAL** | **Post-hoc ρ≥0.3 manufactured "E10 clears"** — not in the frozen prereg; the frozen bar is +10% greedy gain. Under it E10 = SQuAD +5.6%, big-bench +8.3% → **clears nothing** (Meth M2, DA M2). | **FIXED** in `dec_synthesis.py`; clear_counts={}; verdict template → directional null. |
| 4 | MAJOR | E10 is a **branch-2.1 verifier/MBR selector** (the framing books it in-fence/2.1), relabeled "agentic" to reach 2.2; its weak positive argues *for* 2.1, not 2.2 (DA M3). | Verdict no longer calls E10 "agentic"; the agentic question is left OPEN. |
| 5 | MAJOR | **No bootstrap CIs computed** (prereg §5 mandated); the positive prong depends on CIs it never computed (Meth M1). | Disclosed; positive prong dropped, not just hedged. |
| 6 | MAJOR | **ICL not closed** — real OPRO/GEPA, M3 cross-modal injection, the full shot-curve, and on-surface selection controls were never run (DA M4, Meth M4). | Verdict scoped to "the tested limited levers fail," not "ICL insufficient." |
| 7 | MAJOR | **E7 "hurts" is within decode noise** — mmau greedy reads 0.653/0.833/0.800/0.75 across runs (temp-0 MoE nondeterminism); the ±0.033 deltas are noise-level; only k=[0,2] (not the prereg shot-curve) (Meth M4). | Downgraded to "did not lift in this configuration." |
| 8 | MAJOR/MINOR (formal) | TH2 (b)-cap **frames, not proves** the empirical null (abstract `w`/`R`/`q0` never measured); models "no lift" not "hurts". TH2a **frames** the decorrelation constraint; it does not predict the E10 numbers (asymptotic vs fixed-n). ρ is a realization fraction, not the error-correlation the theorem is about (EIC, Meth M5). | Theory reworded "machine-checked as" → "framed by"; scoped to what each theorem actually states. |
| 9 | MINOR | "design an omni agentic system" reads stronger than a Stage-1 handoff warrants (EIC). | → "pursue/scope branch 2.2, Stage-2-gated" / left open. |

## The corrected verdict (one line)
Under the frozen +10% bar, **no in-fence lever (few-shot ICL, prompt-opt, two-system verifier) realizes
the oracle-δ**. But this is **under-powered (n=24, no CIs) AND under-scoped** (the decisive in-fence
instruments — real OPRO/GEPA, M3 cross-modal injection, an on-surface self-selection control — were not
run), so it **does not close Q1 and does not establish the agentic branch**. It is a **directional null
returned to the owner**, pinning the mandatory Stage-2 preconditions — not a branch decision, not a build
recommendation. E10's sub-threshold signal is a branch-2.1 selector result, confounded by surface.
