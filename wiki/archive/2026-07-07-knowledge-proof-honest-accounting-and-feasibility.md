---
title: Knowledge-Injection Proofs — Honest Accounting + Convergence-Feasibility Verdict (WS-E)
date: 2026-07-07
stage: 1-argumentation (theory-track discipline)
lane: knowledge-backbone / theory
scope: append-only correction; does NOT rewrite prior records (per methodology)
audit_basis: read-only inspection of proofs/tfrl/TfrlProofs/*.lean + Theory-Convergence-and-Constraints.md + Decision-Log
---

> **LOG** — Stage-1 过程记录（hypothesis-grade），非现行真源；现行结论以 [[Decision-Log]] 与 [[Per-Work-Status]] 为准。

# Knowledge-Injection Proofs — Honest Accounting & Feasibility

Per owner (2026-07-07): **first honestly account, then judge feasibility.** This is an append-only
correction of overstated theory claims plus a Stage-1 verdict on whether a *genuine* convergence proof
for knowledge injection is achievable. It does not rewrite prior records; it re-grades them (methodology).

## Part 1 — Honest accounting (what the Lean actually proves)

### 1.1 The "knowledge crosses the gap" theorem is a tautology
`InfoBoundary.newinfo_can_cross_gap` and `AgenticElements.external_element_can_escape` prove only
`∃ (s s' : Fin 1 → Bool), (∀ i, s i ≠ true) ∧ (∃ j, s' j = true)` — a trivial existence witness
(`fun _ => false`, `fun _ => true`). This shows another distribution *can logically* contain a correct
answer; it **models no retrieval/injection mechanism** and carries **no result** that RAG/knowledge
injection crosses a knowledge gap. **Re-grade: FRAMING-ONLY (tautology), not a contribution** — the same
verdict the team already reached for the read-out counting bounds (`isolation-audit`, D3 review 2026-07-06:
"InfoBoundary(A) is a framing bound, not a contribution").

### 1.2 The convergence theorems are a general squeeze on ASSUMED bounds
`Realization.realized_tendsto_oracle` (C4, τ), `BlindSpot.avg_regret_tendsto_zero` (frac), and
`BestOfNConvergence.bestofn_regret_tendsto_zero` (τ) are **one real-analysis lemma** ("if `0 ≤ aₙ ≤ B·fₙ`
and `fₙ→0` then `aₙ→0`", `squeeze_zero`). The sequences (`τ`, `frac`) are free `ℕ→ℝ`; the load-bearing
antecedent (`τₙ→0`) is an **assumption**, not derived from any knowledge-injection update rule. C4 is
slightly stronger (the `≤ 2τ` bound is genuinely proved by `realized_gap_le_two_tau`), but `τ→0` remains
externally posited. **The process dynamics are unmodeled**, so this is "convergence-by-assumed-bound," not
convergence of a real system. And empirically **τ is large** (T9: the frozen omni adopts conflicting
external knowledge only ~24% of the time) → the antecedent does not hold → **the theorem is vacuous for the
deployed system** (it converges only in a limit the system never reaches).

### 1.3 Documentation overstatement — a REPEAT offense
CLAUDE.md's required **iterate-process convergence C1/C2** (`Iterate.lean`: `monotone_bounded_converges`,
`improve_budget N* ≤ (M−x₀)/δ`, `unconstrained_diverges`) is **NOT in the built/committed library** — it
lives in `speechrl-data/_repro/Iterate.lean` (gitignored, un-imported, un-committed). Yet the 2026-07-07
Decision-Log and `E6-final-conclusions-clean.md` repeatedly claim it "delivered sorry-free in `proofs/tfrl`
… Lean C1/C2/C4 all green." **This is documentation overstatement, and it is the SAME class of error the
team already recorded once** (Decision-Log:868 "Theory-Convergence previously claimed Realization.lean
existed — doc overstatement"; commit `8298846` "was falsely claimed verified"). **Re-grade: the "C1/C2
all-green" claim is RETRACTED** pending Iterate.lean being moved into `proofs/tfrl/TfrlProofs/`, imported,
and `lake build`-verified.

### 1.4 dual-track binding is docstring-only
Theorems name code objects (`decode.best_of_n`, accept-gate, `kl_best_of_n_bound`) only in docstrings; the
Lean operators (`ReadoutSelector.pick`, `Rhat`) have **no formal binding** to any Python selector, and
`Theory-Convergence §4` itself lists the CI sync-check as an open TODO. **The theorems are about abstract
shells, not the same object the engineering optimizes** — the dual-track requirement is unmet for knowledge.

### 1.5 sorry/axiom audit — clean
Only one `sorry` in the whole module (`BestOfN.lean:90`, the documented Beirami order-statistics step). No
`admit`, no `axiom`, no `native_decide` in the knowledge-relevant files. (This part of the record is sound.)

## Part 2 — Feasibility verdict: CAN a genuine convergence proof be built?

**Stage-1 deliverable = the verdict, not the proof.**

### 2.1 What a genuine proof requires
Model the knowledge-injection **update rule as an actual operator** on the frozen model's output
distribution, and prove convergence *from* that operator under explicit training-free constraints — not by
assuming `τ→0`. Per CLAUDE.md: prove the **unconstrained** process fails, then that the **constrained** one
succeeds; the load-bearing content is the constraints.

### 2.2 The obstruction (why the current "realized→oracle" claim is false)
In the training-free setting nothing drives `τ→0`. The reward proxy (retriever relevance / omni-embed
support, never gold) has a **fixed nonzero error floor** τ\* — the achievable error-decorrelation `δ_corr`
plus the knowledge blind-spot (cf. `omni-verifier-decorrelation` memory). So `τ → τ* > 0`, not 0.
Empirically τ is large (24% adoption; parametric stubbornness). **Therefore the unconstrained claim
"realized → oracle" is FALSE for the deployed system** — which is exactly why 1.2's theorem is vacuous.

### 2.3 The feasible reframe (the honest theorem shape)
A genuine, non-tautological theorem is **neighborhood-convergence**, not limit-to-oracle:
> **Constrained**: under a KL trust-region (β / ε) and an over-optimization budget cap N\*, the
> reward-guided knowledge selector converges to an **oracle − 2τ\* neighborhood**, where τ\* is the
> irreducible reward-proxy error floor. **Unconstrained**: without the budget cap, reward-hacking the
> proxy drives the realized output AWAY from oracle past N\* (over-optimization divergence).

This is the shape CLAUDE.md demands (unconstrained fails → constrained succeeds) and it is **provable**,
because both pieces follow from a bounded-but-nonzero proxy error + a Lipschitz/slow-drift precondition —
neither of which requires the false `τ→0`. `BestOfNConvergence.unconstrained_bestofn_no_converge` already
proves the negative half in miniature (regret ≥ c·ε under a fixed error floor); the positive half must be
re-stated as convergence **to the τ\*-neighborhood**, and — the missing piece — the operator must be the
actual injection/accept-gate update, dual-track-bound to the code.

### 2.4 Verdict
**FEASIBLE, but only as neighborhood-convergence under an explicit reward-proxy-error floor τ\*>0 + a
budget cap N\*** — NOT the "realized→oracle" limit currently claimed. The current theorems must be either
(a) explicitly relabeled as the τ→0 idealization (stating it does not hold empirically), or (b) rebuilt
around τ\*>0. The τ\*-neighborhood theorem, with a real injection operator and a dual-track CI binding, is
the **Stage-2 theory target**; the reward-proxy error floor τ\* (= `δ_corr` + blind-spot) is the
load-bearing constraint.

## Part 3 — Cleanup actions (follow-up; each needs `lake build` verification)

1. **Retract** the "C1/C2 all-green / delivered in proofs/tfrl" claim in Decision-Log + E6 via a dated
   correction (append-only). *(This doc is that correction; mirror a one-line pointer into Decision-Log.)*
2. **Relocate** `speechrl-data/_repro/Iterate.lean` → `proofs/tfrl/TfrlProofs/Iterate.lean`, add to
   `TfrlProofs.lean` import, and `lake build` to make C1/C2 actually library-verified — OR label it
   explicitly "library-external, unverified" everywhere it is cited.
3. **Mark** `newinfo_can_cross_gap` / `external_element_can_escape` docstrings as FRAMING-ONLY (tautology),
   consistent with the D3 read-out-bound re-grade.
4. **Add** the dual-track CI check (Lean operator ⟷ Python selector) to the theory backlog (Theory-Convergence §4).
5. **Stage-2**: build the τ\*-neighborhood convergence theorem around the real injection/accept-gate operator.

> Status of this doc's own claims: Parts 1–2 are from read-only Lean/wiki inspection (verified). The Part-3
> edits are NOT yet applied — they require a `lake build` pass and are the immediate follow-up, tracked so
> the "already verified" trap of 1.3 is not repeated.
