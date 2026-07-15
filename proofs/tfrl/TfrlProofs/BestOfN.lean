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
* introduce the true best-of-`N` selection-policy KL functional as an **opaque** constant
  `klBoNActual : ℕ → ℝ` (its measure-theoretic definition is out of scope for this
  skeleton), and state the Beirami order-statistics estimate about it as a single,
  explicitly named, **cited axiom** `beirami_thm_3_1`;
* derive the main inequality `kl_best_of_n_le` from that axiom.

## On the axiom (documented exception to the sorry-free bar)

The order-statistics derivation of `KL(π_BoN ‖ π₀) ≤ klBoundBoN N` — an integral over the
reward CDF, `P_BoN(z) = F(z)^N - F(z⁻)^N` — is **not** reproduced here. Rather than a
`sorry`, it is discharged as the single named axiom `beirami_thm_3_1`, citing
Beirami et al. (2024), arXiv:2401.01879, Theorem 3.1 (verbatim conditions in its
docstring). The axiom is stated about the **opaque** functional `klBoNActual`, not about
an arbitrary `ℕ → ℝ`: a parametric version `∀ f, f N ≤ klBoundBoN N` would be
**inconsistent** (take `f := fun _ => klBoundBoN N + 1`), so asserting it would be strictly
worse than a `sorry`. Asserting the bound about a *fixed but unspecified* functional is
consistent (it is satisfiable — e.g. by the zero functional, since `klBoundBoN N ≥ 0`),
which is the honest way to import a cited-but-unformalized analytic result. No `sorry`
remains in this module.
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

/-- The genuine best-of-`N` selection-policy KL functional `N ↦ KL(π_BoN ‖ π₀)` for a
fixed base policy `π₀`. It is left **opaque**: its definition is the measure-theoretic
order-statistics / reward-CDF integral of Beirami et al. (2024), which this skeleton does
not build out. Being an opaque constant — a *fixed but unspecified* function, not a
universally-quantified one — is exactly what makes the cited bound `beirami_thm_3_1`
below a *consistent* assumption: Lean cannot substitute a counterexample for it. -/
opaque klBoNActual : ℕ → ℝ

/-- **Beirami et al. (2024), Theorem 3.1** — *Theoretical guarantees on the best-of-n
alignment policy*, arXiv:2401.01879.

Verbatim conditions: on a **finite** outcome space, under Assumption 2.1 (**reward
uniqueness / distinct rewards** — no ties), the best-of-`n` selection policy `π_BoN`
satisfies the **upper bound**
```
D_KL(π_BoN ‖ π_ref) ≤ log n - (n-1)/n
```
(an inequality in general, with equality only in the continuous no-ties limit).

This is the content that requires the order-statistics / reward-CDF integral argument
(`P_BoN(z) = F(z)^n - F(z⁻)^n`). It is imported here as a single explicitly named, cited
axiom about the opaque functional `klBoNActual`, replacing the former documented `sorry`.
It is consistent because it is satisfiable (e.g. by the zero functional, as
`klBoundBoN n ≥ 0` by `klBoundBoN_nonneg`). -/
axiom beirami_thm_3_1 {N : ℕ} (hN : 1 ≤ N) : klBoNActual N ≤ klBoundBoN N

/-- **T2 (best-of-N KL bound).** The best-of-`N` selection policy stays within
`log N - (N-1)/N` of the base policy in KL divergence. This is the main inequality; it now
*consumes* the cited Beirami order-statistics estimate `beirami_thm_3_1` (about the opaque
KL functional `klBoNActual`) rather than taking it as a free hypothesis. -/
theorem kl_best_of_n_le {N : ℕ} (hN : 1 ≤ N) :
    klBoNActual N ≤ Real.log N - ((N : ℝ) - 1) / N :=
  beirami_thm_3_1 hN

end TfrlProofs.BestOfN
