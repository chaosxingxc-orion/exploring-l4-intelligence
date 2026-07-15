import Mathlib
import TfrlProofs.BlindSpot

set_option linter.style.header false
set_option linter.style.longLine false

/-!
# Theory-track: convergence of the CONSTRAINED reward-guided best-of-N selection process

The D3 review (2026-07-06) correctly flagged that `InfoBoundary`/`AgenticElements` are **static identities**
(correctness-only): a selector cannot beat the best of its N samples. Per the project's theory-track bar
(CLAUDE.md: *a static identity is not a result*; a theorem needs correctness AND **convergence**, with the
load-bearing content in the **constraint terms** that bound the problem's edges), the missing dual-bar piece
is a convergence result for the *constrained* selection process. This file supplies it, following the
mandated shape: **prove the UNCONSTRAINED process fails to converge, then that the CONSTRAINED one does.**

The object is the reward-guided best-of-N selector of GAP-1/GAP-3 (an omni verifier picking among N frozen-
generator samples). Its per-run **regret** = oracle − realized is bounded, per the C4 estimation-error bound
(`TfrlProofs.Realization.realized_gap_le_two_tau`: `reg ≤ 2·τ`), by `B · τ_N`, where `τ_N` is the
**reward-estimation error** — small exactly when the verifier is **decorrelated** from the generator (the
achievable δ_corr of the omni-verifier-decorrelation constraint; `[[omni-verifier-decorrelation-w4-bridge]]`).

- `bestofn_regret_tendsto_zero` (**constrained ⇒ converges**): if `τ_N → 0` (the constraint: estimation error
  vanishes as decorrelation improves), realized reward converges to the oracle (`regret → 0`).
- `unconstrained_bestofn_no_converge` (**unconstrained ⇒ fails**): if the estimation error is bounded *below*
  by `ε > 0` (a non-decorrelated / self-preference-biased verifier — the E10/E10b regime) and regret tracks
  it, then regret stays `≥ c·ε > 0` forever — the process does **not** converge to the oracle.

Together: convergence of reward-guided best-of-N is **not** automatic; it **requires** the decorrelation
constraint `τ_N → 0`. This is the theory of GAP-3 (and the admissibility condition for GAP-1's selector).
-/

namespace TfrlProofs.BestOfNConvergence

open Filter Topology

variable (regret tau : ℕ → ℝ)

/-- **Constrained convergence.** Reward-guided best-of-N with per-run regret nonnegative and bounded by
`B · τ n` (the C4 estimation-error bound), where the estimation error `τ n → 0` (the decorrelation
constraint), realizes the oracle in the limit: `regret → 0`. The constraint term is `τ`; a nonzero residual
`τ` is exactly a non-decorrelated verifier. -/
theorem bestofn_regret_tendsto_zero (B : ℝ)
    (h0 : ∀ n, 0 ≤ regret n) (hle : ∀ n, regret n ≤ B * tau n)
    (htau : Tendsto tau atTop (nhds 0)) :
    Tendsto regret atTop (nhds 0) := by
  refine squeeze_zero h0 hle ?_
  simpa using htau.const_mul B

/-- **Unconstrained non-convergence.** If the reward-estimation error is bounded *below* by `ε > 0` (an
un-decorrelated / self-preference-biased verifier — E10/E10b's same-context regime) and per-run regret tracks
it from below (`c · τ n ≤ regret n`, `c > 0`), then `regret n ≥ c·ε > 0` for every `n`: the unconstrained
selection process is bounded away from the oracle and does **not** converge. Convergence therefore *requires*
the constraint `τ → 0`. -/
theorem unconstrained_bestofn_no_converge (c ε : ℝ)
    (hc : 0 < c) (hε : 0 < ε)
    (hτ : ∀ n, ε ≤ tau n) (hlo : ∀ n, c * tau n ≤ regret n) :
    ∀ n, c * ε ≤ regret n := by
  intro n
  have : c * ε ≤ c * tau n := by nlinarith [hτ n]
  exact le_trans this (hlo n)

/-- **Positive floor corollary.** Under the unconstrained hypotheses, the regret never enters `(-∞, c·ε)`;
in particular it cannot tend to `0` (its values stay `≥ c·ε > 0`). -/
theorem unconstrained_regret_pos (c ε : ℝ)
    (hc : 0 < c) (hε : 0 < ε)
    (hτ : ∀ n, ε ≤ tau n) (hlo : ∀ n, c * tau n ≤ regret n) :
    ∀ n, 0 < regret n := by
  intro n
  have h := unconstrained_bestofn_no_converge regret tau c ε hc hε hτ hlo n
  nlinarith [mul_pos hc hε]

end TfrlProofs.BestOfNConvergence
