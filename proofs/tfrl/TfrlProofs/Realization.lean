import Mathlib

set_option linter.style.header false

/-!
# Realization bound (C4) — a label-free selector's realized gain is capped by its estimation error

Training-free RL over a **finite candidate pool** `Z` selects a candidate by maximizing an ESTIMATED
reward `Rhat` (a *label-free* selector — token-confidence / self-certainty, MBR-utility, or an
LLM-judge score), while the TRUE reward is `R`. The **oracle** selects `argmax R`. This file proves
the argmax-mismatch bound

  `R(oracle) − R(selector) ≤ 2 · τ`,   `τ` a uniform bound on `|Rhat − R|`,

so the realized-versus-oracle gap — equivalently `(1 − ρ)` times the oracle headroom, where `ρ` is the
fraction of headroom a selector realizes — is controlled by the selector's reward-estimation error `τ`
(constraint term **C4** of `wiki/Theory-Convergence-and-Constraints.md`).

**Dual track with the experiments.** `R` = task correctness; `Rhat` = the selector's label-free score;
`jhat` = the code's `argmax Rhat` (majority / self-certainty / judge); `jstar` = the pool oracle. The
theorem explains the measured `(c)` gap: on MMAU the oracle headroom is real (`+0.133`), yet a
label-free selector realizes ≈ 0 of it because the model is *confidently wrong* — its estimate `Rhat`
(confidence) is a poor proxy for `R` (correctness), i.e. `τ` is large. As `τ → 0`, `ρ → 1`.
-/

namespace TfrlProofs.Realization

open Finset

variable {Z : Type*}

/-- **C4 realization bound (argmax mismatch).** If `jhat` maximizes the estimate `Rhat` and
`|Rhat z − R z| ≤ τ` for every candidate `z`, then for *any* reference candidate `jstar` (in
particular the oracle `argmax R`) the reward gap `R jstar − R jhat ≤ 2 · τ`. The bound needs only that
`jhat` is the estimate's argmax; jstar's own optimality is not required (and when `jstar` is the
oracle this is exactly the oracle-versus-selector gap). -/
theorem realized_gap_le_two_tau (R Rhat : Z → ℝ) (jhat jstar : Z)
    (hjhat : ∀ z, Rhat z ≤ Rhat jhat)
    (τ : ℝ) (hτ : ∀ z, |Rhat z - R z| ≤ τ) :
    R jstar - R jhat ≤ 2 * τ := by
  -- R jstar − R jhat = (R jstar − Rhat jstar) + (Rhat jstar − Rhat jhat) + (Rhat jhat − R jhat)
  have h1 : R jstar - Rhat jstar ≤ τ := by
    have := (abs_le.mp (hτ jstar)).1; linarith
  have h2 : Rhat jhat - R jhat ≤ τ := (abs_le.mp (hτ jhat)).2
  have h3 : Rhat jstar ≤ Rhat jhat := hjhat jstar
  linarith

/-- **Perfect estimator realizes the oracle.** If the selector's estimate is exact (`τ = 0`), then the
selected candidate attains the oracle reward: `R jhat = R jstar`. (`ρ = 1`.) -/
theorem exact_estimator_is_oracle (R Rhat : Z → ℝ) (jhat jstar : Z)
    (hjhat : ∀ z, Rhat z ≤ Rhat jhat) (hjstar : ∀ z, R z ≤ R jstar)
    (hexact : ∀ z, Rhat z = R z) :
    R jhat = R jstar := by
  have hle : R jstar - R jhat ≤ 2 * 0 :=
    realized_gap_le_two_tau R Rhat jhat jstar hjhat 0
      (fun z => by rw [hexact z]; simp)
  have := hjstar jhat
  linarith

/-! ## Convergence of the constrained realization (C4 as a limit)

The static bound above becomes a **convergence** statement once the estimation error `τ` is the
constraint term driven to zero. Consider a sequence of label-free selectors indexed by `n` (e.g. a
larger judge, a better-calibrated confidence, more verification budget) whose estimators `Rhat n`
have uniform errors `τ n` with `τ n → 0`. Then the realized-versus-oracle reward gap `→ 0`: the
selected candidate's true reward converges to the oracle reward. `τ` is exactly the constraint that
bounds and closes the convergence — this is the theory-side statement of the empirical `(c)` lever
(drive `τ` down and `ρ → 1`; on frozen omni today `τ` is large — confidently wrong — so `ρ ≈ 0`). -/

open Filter Topology in
/-- **Constrained realization converges to the oracle.** For a fixed true reward `R` and a sequence
of estimators `Rhat n` with argmax `jhat n` and uniform estimation errors `τ n → 0`, the realized
reward gap `R jstar − R (jhat n) → 0`. Proof: squeeze between `0` (oracle optimality) and `2 · τ n`
(the static C4 bound). -/
theorem realized_tendsto_oracle (R : Z → ℝ) (Rhat : ℕ → Z → ℝ) (jhat : ℕ → Z) (jstar : Z)
    (hjhat : ∀ n z, Rhat n z ≤ Rhat n (jhat n)) (hjstar : ∀ z, R z ≤ R jstar)
    (τ : ℕ → ℝ) (hτ : ∀ n z, |Rhat n z - R z| ≤ τ n)
    (hτ0 : Tendsto τ atTop (𝓝 0)) :
    Tendsto (fun n => R jstar - R (jhat n)) atTop (𝓝 0) := by
  have hlo : ∀ n, 0 ≤ R jstar - R (jhat n) := fun n => by linarith [hjstar (jhat n)]
  have hup : ∀ n, R jstar - R (jhat n) ≤ 2 * τ n := fun n =>
    realized_gap_le_two_tau R (Rhat n) (jhat n) jstar (hjhat n) (τ n) (hτ n)
  have hg : Tendsto (fun n => 2 * τ n) atTop (𝓝 0) := by simpa using hτ0.const_mul 2
  exact squeeze_zero hlo hup hg

end TfrlProofs.Realization
