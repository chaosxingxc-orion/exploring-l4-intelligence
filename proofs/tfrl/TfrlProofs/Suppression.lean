import Mathlib
import TfrlProofs.Tilting

set_option linter.style.header false

/-!
# T3 — Flat-reward no-go (suppression)

A *label-independent* reward cannot steer the Gibbs / exponentially-tilted
distribution: if the reward `R` is constant (`∀ z, R z = c`), then the tilted
distribution `qstar` coincides with the reference `q0` pointwise.

Consequently **Operator-A tilting is the identity** whenever the reward carries no
label information — there is no possible steering. This is the formal counterpart of
the empirical observation that a flat (constant) reward suppresses any reweighting.
-/

namespace TfrlProofs.Suppression

open scoped BigOperators
open Real Finset
open TfrlProofs.Tilting

variable {Z : Type*} [Fintype Z]

/-- With a constant reward, the partition function collapses to `exp (c / β)`
(using `∑ q0 = 1`). -/
theorem Zpart_const {q0 : Z → ℝ} {β c : ℝ}
    (hq0sum : ∑ z, q0 z = 1) (R : Z → ℝ) (hR : ∀ z, R z = c) :
    Zpart q0 R β = Real.exp (c / β) := by
  unfold Zpart
  have : ∀ z, q0 z * Real.exp (R z / β) = q0 z * Real.exp (c / β) := by
    intro z; rw [hR z]
  rw [Finset.sum_congr rfl (fun z _ => this z), ← Finset.sum_mul, hq0sum, one_mul]

/-- **T3 (flat-reward no-go).** If the reward `R` is constant (`∀ z, R z = c`), then
the exponentially-tilted distribution equals the reference distribution pointwise:
`qstar z = q0 z` for every `z`. Hence tilting performs no steering. -/
theorem qstar_eq_q0_of_const [Nonempty Z]
    {q0 : Z → ℝ} {β c : ℝ} (hq0sum : ∑ z, q0 z = 1)
    {R : Z → ℝ} (hR : ∀ z, R z = c) :
    ∀ z, qstar q0 R β z = q0 z := by
  intro z
  unfold qstar
  rw [Zpart_const hq0sum R hR, hR z]
  -- `q0 z * exp(c/β) / exp(c/β) = q0 z` since `exp(c/β) > 0`.
  rw [mul_div_assoc, div_self (Real.exp_pos _).ne', mul_one]

/-- The flat-reward objective restricted to `qstar` equals its value at `q0`
(an immediate corollary: tilting changes nothing, in particular not the objective). -/
theorem F_qstar_eq_F_q0_of_const [Nonempty Z]
    {q0 : Z → ℝ} {β c : ℝ} (hq0sum : ∑ z, q0 z = 1)
    {R : Z → ℝ} (hR : ∀ z, R z = c) :
    F q0 R β (qstar q0 R β) = F q0 R β q0 := by
  have h : qstar q0 R β = q0 := funext (qstar_eq_q0_of_const hq0sum hR)
  rw [h]

end TfrlProofs.Suppression
