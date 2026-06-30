import Mathlib
import TfrlProofs.Tilting

set_option linter.style.header false

/-!
# OSA — Optimization-space adequacy for training-free RL (extends T1/T3)

Training-free RL tilts `q*(z) ∝ q0(z)·exp(R(z)/β)` (see `TfrlProofs.Tilting`). Define the
**optimization gain** of the tilted optimum over the baseline:
`gain = F(qstar) − F(q0)`.

**OSA-1 (this file).** The gain equals `β·log Zpart − E_{q0}[R]` (`gain_eq`); it is nonnegative
(`gain_nonneg`); under a **flat reward** (`R ≡ c`) it is **zero** (`flat_no_gain`, recovering T3 —
a degenerate / single-model output-context action space affords no improvement); and given the
isolated log-sum-exp / Hoeffding bound it is `≤ S` (`gain_le_of_hoeffding`, the chaining lemma in
the style of T6's `regret_O_sqrt_log`, where `S = spread²/(8β)`).

OSA-2 (product/agent space ⇒ additive growing gain) and OSA-3 (rollout instability + credit-assigned
convergence) follow in subsequent lemmas; see `OptSpace-notes.md`.
-/

namespace TfrlProofs.OptSpace

open scoped BigOperators
open Real Finset
open TfrlProofs.Tilting

variable {Z : Type*} [Fintype Z]

/-- The optimization gain of the tilted optimum over the baseline reference. -/
noncomputable def gain (q0 R : Z → ℝ) (β : ℝ) : ℝ :=
  F q0 R β (qstar q0 R β) - F q0 R β q0

variable {q0 R : Z → ℝ} {β : ℝ}

/-- **OSA-1 (gain identity).** `gain = β·log Zpart − E_{q0}[R]`. -/
theorem gain_eq [Nonempty Z] (hq0 : ∀ z, 0 < q0 z) (hβ : 0 < β)
    (hq0sum : ∑ z, q0 z = 1) :
    gain q0 R β = β * Real.log (Zpart q0 R β) - ∑ z, q0 z * R z := by
  unfold gain
  rw [F_sub_eq_beta_mul_kl hq0 hβ (fun z => (hq0 z).le) hq0sum]
  have hterm : ∀ z, q0 z * Real.log (q0 z / qstar q0 R β z)
      = q0 z * Real.log (Zpart q0 R β) - q0 z * R z / β := by
    intro z
    have h := log_qstar_div_q0 (R := R) (β := β) hq0 z
    have hflip : Real.log (q0 z / qstar q0 R β z)
        = - Real.log (qstar q0 R β z / q0 z) := by
      rw [← Real.log_inv]; congr 1; field_simp
    rw [hflip, h]; ring
  rw [Finset.sum_congr rfl (fun z _ => hterm z),
    Finset.sum_sub_distrib, ← Finset.sum_mul, ← Finset.sum_div, hq0sum]
  field_simp

/-- **OSA-1 (gain nonneg).** `0 ≤ gain` (Gibbs' inequality, `β > 0`). -/
theorem gain_nonneg [Nonempty Z] (hq0 : ∀ z, 0 < q0 z) (hβ : 0 < β)
    (hq0sum : ∑ z, q0 z = 1) :
    0 ≤ gain q0 R β := by
  unfold gain
  have hkl : 0 ≤ ∑ z, q0 z * Real.log (q0 z / qstar q0 R β z) :=
    kl_nonneg (fun z => (hq0 z).le) (fun z => qstar_pos hq0 z) hq0sum (qstar_sum_one hq0)
  have hid := F_sub_eq_beta_mul_kl (R := R) (β := β) hq0 hβ (fun z => (hq0 z).le) hq0sum
  nlinarith [mul_nonneg hβ.le hkl, hid]

/-- **OSA-1 (flat-reward no-go, recovers T3).** A constant reward — the degenerate / single-model
output-context action space with zero reward spread — yields **no** optimization gain. -/
theorem flat_no_gain [Nonempty Z] (hq0 : ∀ z, 0 < q0 z) (hβ : 0 < β)
    (hq0sum : ∑ z, q0 z = 1) {c : ℝ} (hR : ∀ z, R z = c) :
    gain q0 R β = 0 := by
  rw [gain_eq hq0 hβ hq0sum]
  have hRsum : ∑ z, q0 z * R z = c := by
    have hpt : ∀ z, q0 z * R z = q0 z * c := fun z => by rw [hR z]
    rw [Finset.sum_congr rfl (fun z _ => hpt z), ← Finset.sum_mul, hq0sum, one_mul]
  have hZ : Zpart q0 R β = Real.exp (c / β) := by
    unfold Zpart
    have hpt : ∀ z, q0 z * Real.exp (R z / β) = q0 z * Real.exp (c / β) :=
      fun z => by rw [hR z]
    rw [Finset.sum_congr rfl (fun z _ => hpt z), ← Finset.sum_mul, hq0sum, one_mul]
  rw [hRsum, hZ, Real.log_exp]
  field_simp
  ring

/-- **OSA-1 (quantitative no-go, chaining).** Given the log-sum-exp / Hoeffding bound
`β·log Zpart − E_{q0}[R] ≤ S` (isolated as a hypothesis, T6-style; with `S = spread²/(8β)` from
Hoeffding's lemma on the bounded variable `R/β`), the gain is at most `S`. As the reward spread
`→ 0`, `S → 0` and `gain → 0`. -/
theorem gain_le_of_hoeffding [Nonempty Z] (hq0 : ∀ z, 0 < q0 z) (hβ : 0 < β)
    (hq0sum : ∑ z, q0 z = 1) {S : ℝ}
    (hHoeff : β * Real.log (Zpart q0 R β) - ∑ z, q0 z * R z ≤ S) :
    gain q0 R β ≤ S := by
  rw [gain_eq hq0 hβ hq0sum]; exact hHoeff

end TfrlProofs.OptSpace
