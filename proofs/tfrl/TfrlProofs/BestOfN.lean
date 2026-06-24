import Mathlib

set_option linter.style.header false

/-!
# T2 — Best-of-N KL bound

For best-of-`N` selection (draw `N` i.i.d. samples from a base policy `π₀`, keep the
one with the highest reward), the induced selection policy `π_BoN` satisfies the
information-theoretic bound of Beirami et al. (2024),
```
KL(π_BoN ‖ π₀) ≤ log N - (N-1)/N.
```
The right-hand side is the *exact* best-of-`N` KL for a continuous reward with no ties
and an upper bound in general; it grows like `log N`.

We:
* package the bound as `klBoundBoN N = log N - (N-1)/N`;
* prove rigorously that it is **nonnegative** (`klBoundBoN_nonneg`) and equals
  `log N - 1 + 1/N` (`klBoundBoN_eq`), so it is a genuine finite `O(log N)` quantity;
* state the main inequality `kl_best_of_n_le` for an abstract KL functional `klBoN`
  that obeys the Beirami order-statistics estimate.

The order-statistics derivation of `KL(π_BoN ‖ π₀) ≤ klBoundBoN N` itself (an
integral over the reward CDF) is *not* reproduced here and is left as a documented
`sorry`; the surrounding analytic facts are fully proved.
-/

namespace TfrlProofs.BestOfN

open Real
open scoped BigOperators

/-- The best-of-`N` KL bound `log N - (N-1)/N` (with `N : ℕ`, read in `ℝ`). -/
noncomputable def klBoundBoN (N : ℕ) : ℝ := Real.log N - ((N : ℝ) - 1) / N

/-- Algebraic normal form: `klBoundBoN N = log N - 1 + 1/N` for `N ≥ 1`. -/
theorem klBoundBoN_eq {N : ℕ} (hN : 1 ≤ N) :
    klBoundBoN N = Real.log N - 1 + 1 / N := by
  have hN0 : (N : ℝ) ≠ 0 := by
    have : (0 : ℝ) < N := by exact_mod_cast Nat.lt_of_lt_of_le Nat.zero_lt_one hN
    exact this.ne'
  unfold klBoundBoN
  field_simp
  ring

/-- The bound is nonnegative for `N ≥ 1`: it is `0` at `N = 1` and positive after,
matching `KL ≥ 0`. Proof: `log N ≥ 1 - 1/N` from `Real.log_le_sub_one_of_pos`
applied to `1 / N`. -/
theorem klBoundBoN_nonneg {N : ℕ} (hN : 1 ≤ N) : 0 ≤ klBoundBoN N := by
  have hNpos : (0 : ℝ) < N := by exact_mod_cast Nat.lt_of_lt_of_le Nat.zero_lt_one hN
  have hinv : 0 < 1 / (N : ℝ) := by positivity
  -- log (1/N) ≤ 1/N - 1
  have hlog := Real.log_le_sub_one_of_pos hinv
  -- log (1/N) = - log N
  have hflip : Real.log (1 / (N : ℝ)) = - Real.log N := by
    rw [one_div, Real.log_inv]
  rw [hflip] at hlog
  -- so log N ≥ 1 - 1/N, hence klBoundBoN N = log N - (1 - 1/N) ≥ 0
  unfold klBoundBoN
  have hNne : (N : ℝ) ≠ 0 := hNpos.ne'
  have hfrac : ((N : ℝ) - 1) / N = 1 - 1 / N := by field_simp
  rw [hfrac]
  linarith [hlog]

/-- **T2 (best-of-N KL bound).** Given any KL functional `klBoN : ℕ → ℝ` that obeys the
Beirami order-statistics estimate (hypothesis `hBeirami`), the best-of-`N` selection
policy stays within `log N - (N-1)/N` of the base policy in KL divergence.

The hypothesis `hBeirami` is exactly the content that requires the order-statistics /
reward-CDF integral argument; it is isolated as an assumption here (see the
module docstring). With it, the conclusion is immediate. -/
theorem kl_best_of_n_le
    (klBoN : ℕ → ℝ) {N : ℕ}
    (hBeirami : klBoN N ≤ klBoundBoN N) :
    klBoN N ≤ Real.log N - ((N : ℝ) - 1) / N :=
  hBeirami

/-- Self-contained statement of the Beirami order-statistics estimate as a standalone
claim: for the best-of-`N` selection-policy KL functional `klBoN`,
`klBoN N ≤ klBoundBoN N`. The continuous-reward, no-ties derivation is **not**
formalized here and is left as a documented `sorry` (this is one of the three
hard-analysis theorems). -/
theorem klBoN_le_klBoundBoN_TODO
    (klBoN : ℕ → ℝ) {N : ℕ} (hN : 1 ≤ N) :
    klBoN N ≤ klBoundBoN N := by
  -- The Beirami et al. (2024) bound `KL(π_BoN ‖ π₀) ≤ log N - (N-1)/N` follows from an
  -- integral over the reward CDF / order statistics of the N i.i.d. draws. That
  -- measure-theoretic derivation is out of scope for this skeleton; documented here.
  sorry

end TfrlProofs.BestOfN
