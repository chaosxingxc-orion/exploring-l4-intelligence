import Mathlib

set_option linter.style.header false

/-!
# T1 — Gibbs / exponential-tilting optimality (finite support)

Let `Z` be a finite type, `q0 : Z → ℝ` a strictly positive reference distribution
summing to `1`, `R : Z → ℝ` a reward, and `β > 0` a temperature.

Define the partition function and the **Gibbs / exponentially-tilted** distribution
```
Zpart   = ∑ w, q0 w * exp (R w / β)
qstar z = q0 z * exp (R z / β) / Zpart
```
and the (KL-regularized) reward objective
```
F q = (∑ z, q z * R z) - β * ∑ z, q z * log (q z / q0 z).
```

**Main theorem (`tilting_optimal`).** For every probability distribution `q`
(`0 ≤ q z`, `∑ q = 1`) we have `F q ≤ F qstar`.

The proof rests on the exact identity (`tilting_objective_eq`, specialised in
`F_sub_eq_beta_mul_kl`)
```
F qstar - F q = β * ∑ z, q z * log (q z / qstar z)
```
whose right-hand side is `β` times a Kullback–Leibler divergence, nonnegative by
Gibbs' inequality (`kl_nonneg`, proved from `Real.log_le_sub_one_of_pos`).
-/

namespace TfrlProofs.Tilting

open scoped BigOperators
open Real Finset

variable {Z : Type*} [Fintype Z]

/-! ## A reusable Gibbs / KL inequality -/

/-- **Gibbs' inequality (KL ≥ 0).** For probability distributions `p` and `r` on a
finite type with `r` strictly positive, the relative entropy is nonnegative:
`0 ≤ ∑ z, p z * log (p z / r z)`.

Proof: the pointwise bound `p z - r z ≤ p z * log (p z / r z)` holds for every `z`
(trivially when `p z = 0`, and from `log x ≤ x - 1` applied to `x = r z / p z`
otherwise). Summing and using `∑ p = ∑ r = 1` gives `0 ≤ ∑ …`. -/
theorem kl_nonneg
    {p r : Z → ℝ} (hp : ∀ z, 0 ≤ p z) (hr : ∀ z, 0 < r z)
    (hpsum : ∑ z, p z = 1) (hrsum : ∑ z, r z = 1) :
    0 ≤ ∑ z, p z * Real.log (p z / r z) := by
  have pointwise : ∀ z, p z - r z ≤ p z * Real.log (p z / r z) := by
    intro z
    rcases eq_or_lt_of_le (hp z) with hz | hz
    · -- `p z = 0`
      rw [← hz, zero_mul]
      have : (0 : ℝ) - r z ≤ 0 := by linarith [hr z]
      simpa using this
    · -- `0 < p z`
      have hrz := hr z
      have hx : 0 < r z / p z := div_pos hrz hz
      have hlog := Real.log_le_sub_one_of_pos hx
      have hflip : Real.log (p z / r z) = - Real.log (r z / p z) := by
        rw [← Real.log_inv]; congr 1; field_simp
      have hcancel : p z * (r z / p z) = r z := by field_simp
      rw [hflip]
      have h2 : p z * (-(r z / p z - 1)) ≤ p z * (- Real.log (r z / p z)) := by
        apply mul_le_mul_of_nonneg_left _ (le_of_lt hz); linarith [hlog]
      have h3 : p z * (-(r z / p z - 1)) = p z - r z := by
        rw [mul_neg, mul_sub, mul_one, hcancel]; ring
      linarith [h2, h3.le, h3.ge]
  calc
    (0 : ℝ) = (∑ z, p z) - (∑ z, r z) := by rw [hpsum, hrsum]; ring
    _ = ∑ z, (p z - r z) := by rw [Finset.sum_sub_distrib]
    _ ≤ ∑ z, p z * Real.log (p z / r z) := Finset.sum_le_sum (fun z _ => pointwise z)

/-! ## The tilting setup -/

variable (q0 : Z → ℝ) (R : Z → ℝ) (β : ℝ)

/-- Partition function `Zpart = ∑ w, q0 w * exp (R w / β)`. -/
noncomputable def Zpart : ℝ := ∑ w, q0 w * Real.exp (R w / β)

/-- The Gibbs / exponentially-tilted distribution
`qstar z = q0 z * exp (R z / β) / Zpart`. -/
noncomputable def qstar (z : Z) : ℝ := q0 z * Real.exp (R z / β) / Zpart q0 R β

/-- The KL-regularized reward objective
`F q = (∑ z, q z * R z) - β * ∑ z, q z * log (q z / q0 z)`. -/
noncomputable def F (q : Z → ℝ) : ℝ :=
  (∑ z, q z * R z) - β * ∑ z, q z * Real.log (q z / q0 z)

variable {q0 R β}

/-- The partition function is strictly positive (a positive-weight sum of positive
exponentials over a nonempty index set). -/
theorem Zpart_pos [Nonempty Z] (hq0 : ∀ z, 0 < q0 z) : 0 < Zpart q0 R β := by
  unfold Zpart
  apply Finset.sum_pos
  · intro z _; exact mul_pos (hq0 z) (Real.exp_pos _)
  · exact Finset.univ_nonempty

/-- Each tilted weight is strictly positive. -/
theorem qstar_pos [Nonempty Z] (hq0 : ∀ z, 0 < q0 z) (z : Z) :
    0 < qstar q0 R β z := by
  unfold qstar
  exact div_pos (mul_pos (hq0 z) (Real.exp_pos _)) (Zpart_pos hq0)

/-- The tilted weights sum to one. -/
theorem qstar_sum_one [Nonempty Z] (hq0 : ∀ z, 0 < q0 z) :
    ∑ z, qstar q0 R β z = 1 := by
  unfold qstar
  rw [← Finset.sum_div]
  rw [div_eq_one_iff_eq]
  · rfl
  · exact (Zpart_pos hq0).ne'

/-- Pointwise log-decomposition of the tilted weight: for `0 < q0 z`,
`log (qstar z / q0 z) = R z / β - log Zpart`. -/
theorem log_qstar_div_q0 [Nonempty Z] (hq0 : ∀ z, 0 < q0 z) (z : Z) :
    Real.log (qstar q0 R β z / q0 z) = R z / β - Real.log (Zpart q0 R β) := by
  have hZ := Zpart_pos (R := R) (β := β) hq0
  unfold qstar
  -- Simplify `q0 z * exp(R z/β) / Zpart / q0 z` to `exp(R z/β) / Zpart`.
  have hq0z := (hq0 z).ne'
  have hsimp : q0 z * Real.exp (R z / β) / Zpart q0 R β / q0 z
      = Real.exp (R z / β) / Zpart q0 R β := by
    field_simp
  rw [hsimp, Real.log_div (Real.exp_pos _).ne' hZ.ne', Real.log_exp]

/-! ## The key identity and optimality -/

/-- **Master identity.** For any probability distribution `s` (with `0 ≤ s z` and
`∑ s = 1`),
`F s = β * log Zpart - β * ∑ z, s z * log (s z / qstar z)`.

Equivalently `F s + β·KL(s ‖ qstar) = β·log Zpart`, the constant value of the
objective along the tilting family. The per-coordinate algebra splits the log of
`s z / qstar z` into the `s z / q0 z` term (which builds `F`) plus the affine
`R z / β - log Zpart` correction; coordinates with `s z = 0` contribute `0` to both
sides. -/
theorem F_eq [Nonempty Z] (hq0 : ∀ z, 0 < q0 z) (hβ : 0 < β)
    {s : Z → ℝ} (hs : ∀ z, 0 ≤ s z) (hssum : ∑ z, s z = 1) :
    F q0 R β s
      = β * Real.log (Zpart q0 R β) - β * ∑ z, s z * Real.log (s z / qstar q0 R β z) := by
  -- Per-coordinate identity (note `β * (R z / β) = R z`, using `β ≠ 0`):
  -- β · (s z · log (s z / qstar z))
  --   = β · (s z · log (s z / q0 z)) - s z · R z + β · (s z · log Zpart)
  have hβ' : β ≠ 0 := hβ.ne'
  have hterm : ∀ z, β * (s z * Real.log (s z / qstar q0 R β z))
      = β * (s z * Real.log (s z / q0 z)) - s z * R z
        + β * (s z * Real.log (Zpart q0 R β)) := by
    intro z
    rcases eq_or_lt_of_le (hs z) with hz | hz
    · rw [← hz]; ring
    · have hqs := qstar_pos (R := R) (β := β) hq0 z
      -- log (s z / qstar z) = log (s z / q0 z) - log (qstar z / q0 z)
      have hsplit : Real.log (s z / qstar q0 R β z)
          = Real.log (s z / q0 z) - Real.log (qstar q0 R β z / q0 z) := by
        rw [Real.log_div hz.ne' hqs.ne', Real.log_div hz.ne' (hq0 z).ne',
          Real.log_div hqs.ne' (hq0 z).ne']
        ring
      rw [hsplit, log_qstar_div_q0 hq0 z]
      field_simp
      ring
  -- Sum the per-coordinate identity into a single equation.
  have hsum : β * ∑ z, s z * Real.log (s z / qstar q0 R β z)
      = β * (∑ z, s z * Real.log (s z / q0 z)) - (∑ z, s z * R z)
        + β * (∑ z, s z * Real.log (Zpart q0 R β)) := by
    rw [Finset.mul_sum, Finset.mul_sum, Finset.mul_sum,
      ← Finset.sum_sub_distrib, ← Finset.sum_add_distrib]
    exact Finset.sum_congr rfl (fun z _ => hterm z)
  -- `∑ s z * log Zpart = log Zpart`.
  have hconst : ∑ z, s z * Real.log (Zpart q0 R β) = Real.log (Zpart q0 R β) := by
    rw [← Finset.sum_mul, hssum, one_mul]
  rw [hconst] at hsum
  unfold F
  linarith [hsum]

/-- **Key identity (`F qstar - F q = β · KL(q ‖ qstar)`).** -/
theorem F_sub_eq_beta_mul_kl [Nonempty Z] (hq0 : ∀ z, 0 < q0 z) (hβ : 0 < β)
    {q : Z → ℝ} (hq : ∀ z, 0 ≤ q z) (hqsum : ∑ z, q z = 1) :
    F q0 R β (qstar q0 R β) - F q0 R β q
      = β * ∑ z, q z * Real.log (q z / qstar q0 R β z) := by
  -- `F qstar`: the KL term vanishes since `qstar z / qstar z = 1`, `log 1 = 0`.
  have hFstar : F q0 R β (qstar q0 R β) = β * Real.log (Zpart q0 R β) := by
    rw [F_eq hq0 hβ (fun z => (qstar_pos hq0 z).le) (qstar_sum_one hq0)]
    have : ∀ z, qstar q0 R β z * Real.log (qstar q0 R β z / qstar q0 R β z) = 0 := by
      intro z; rw [div_self (qstar_pos hq0 z).ne', Real.log_one, mul_zero]
    rw [Finset.sum_congr rfl (fun z _ => this z)]
    simp
  -- `F q`: master identity for `q`.
  have hFq := F_eq (R := R) (β := β) hq0 hβ hq hqsum
  rw [hFstar, hFq]; ring

/-- **T1 (exponential-tilting optimality).** Among all probability distributions
`q` on the finite support `Z`, the Gibbs / exponentially-tilted distribution
`qstar` maximizes the KL-regularized reward objective `F`. -/
theorem tilting_optimal [Nonempty Z] (hq0 : ∀ z, 0 < q0 z) (hβ : 0 < β)
    {q : Z → ℝ} (hq : ∀ z, 0 ≤ q z) (hqsum : ∑ z, q z = 1) :
    F q0 R β q ≤ F q0 R β (qstar q0 R β) := by
  have hkl : 0 ≤ ∑ z, q z * Real.log (q z / qstar q0 R β z) :=
    kl_nonneg hq (fun z => qstar_pos hq0 z) hqsum (qstar_sum_one hq0)
  have hid := F_sub_eq_beta_mul_kl (R := R) (β := β) hq0 hβ hq hqsum
  nlinarith [mul_nonneg hβ.le hkl, hid]

end TfrlProofs.Tilting
