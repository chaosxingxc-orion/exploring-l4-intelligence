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

/-- **Strict Gibbs inequality.** For strictly positive probability distributions `p`, `r` that
differ at some point, the relative entropy is *strictly* positive. (The non-strict version is
`kl_nonneg`; the strictness comes from `Real.log_lt_sub_one_of_pos` at the differing coordinate.) -/
theorem kl_pos_of_ne {p r : Z → ℝ} (hp : ∀ z, 0 < p z) (hr : ∀ z, 0 < r z)
    (hpsum : ∑ z, p z = 1) (hrsum : ∑ z, r z = 1) (hne : ∃ z, p z ≠ r z) :
    0 < ∑ z, p z * Real.log (p z / r z) := by
  obtain ⟨z0, hz0⟩ := hne
  have pointwise : ∀ z, p z - r z ≤ p z * Real.log (p z / r z) := by
    intro z
    have hz := hp z
    have hrz := hr z
    have hx : 0 < r z / p z := div_pos hrz hz
    have hlog := Real.log_le_sub_one_of_pos hx
    have hflip : Real.log (p z / r z) = - Real.log (r z / p z) := by
      rw [← Real.log_inv]; congr 1; field_simp
    have hcancel : p z * (r z / p z) = r z := by field_simp
    rw [hflip]
    have h2 : p z * (-(r z / p z - 1)) ≤ p z * (- Real.log (r z / p z)) := by
      apply mul_le_mul_of_nonneg_left _ hz.le; linarith [hlog]
    have h3 : p z * (-(r z / p z - 1)) = p z - r z := by
      rw [mul_neg, mul_sub, mul_one, hcancel]; ring
    linarith [h2, h3.le, h3.ge]
  have strict0 : p z0 - r z0 < p z0 * Real.log (p z0 / r z0) := by
    have hz := hp z0
    have hrz := hr z0
    have hx : 0 < r z0 / p z0 := div_pos hrz hz
    have hxne : r z0 / p z0 ≠ 1 := by
      intro h; apply hz0; field_simp [hz.ne'] at h; linarith
    have hlog := Real.log_lt_sub_one_of_pos hx hxne
    have hflip : Real.log (p z0 / r z0) = - Real.log (r z0 / p z0) := by
      rw [← Real.log_inv]; congr 1; field_simp
    have hcancel : p z0 * (r z0 / p z0) = r z0 := by field_simp
    rw [hflip]
    have h2 : p z0 * (-(r z0 / p z0 - 1)) < p z0 * (- Real.log (r z0 / p z0)) := by
      apply mul_lt_mul_of_pos_left _ hz; linarith [hlog]
    have h3 : p z0 * (-(r z0 / p z0 - 1)) = p z0 - r z0 := by
      rw [mul_neg, mul_sub, mul_one, hcancel]; ring
    linarith [h2, h3.le, h3.ge]
  have hsum_lt : ∑ z, (p z - r z) < ∑ z, p z * Real.log (p z / r z) :=
    Finset.sum_lt_sum (fun z _ => pointwise z) ⟨z0, Finset.mem_univ z0, strict0⟩
  have hzero : ∑ z, (p z - r z) = 0 := by
    rw [Finset.sum_sub_distrib, hpsum, hrsum]; ring
  linarith [hsum_lt, hzero]

/-- **OSA-1 (strict positivity for a non-degenerate reward).** If the reward is *non-constant* on
the support, the optimization gain is *strictly* positive: `0 < gain`. Combined with the additivity
`gain_product` (OSA-2), this defeats the "sum of `k` near-zero gains is vacuous" objection — each
context-isolated block with a non-degenerate reward contributes a strictly positive term, so the
total gain is strictly increasing in the number of non-degenerate blocks. Whether the frozen model
actually yields non-degenerate per-block rewards remains the empirical (Phase-2) question. -/
theorem gain_pos_of_nonconstant [Nonempty Z] (hq0 : ∀ z, 0 < q0 z) (hβ : 0 < β)
    (hq0sum : ∑ z, q0 z = 1) (hR : ∃ z w, R z ≠ R w) :
    0 < gain q0 R β := by
  have hqs_ne : ∃ z, q0 z ≠ qstar q0 R β z := by
    by_contra h
    push_neg at h
    obtain ⟨z, w, hzw⟩ := hR
    apply hzw
    have hZ := Zpart_pos (R := R) (β := β) hq0
    have key : ∀ u, Real.exp (R u / β) = Zpart q0 R β := by
      intro u
      have hu := h u
      unfold qstar at hu
      have : q0 u * Zpart q0 R β = q0 u * Real.exp (R u / β) := by
        field_simp at hu ⊢; linarith [hu]
      have := mul_left_cancel₀ (hq0 u).ne' this
      linarith [this]
    have hexp : Real.exp (R z / β) = Real.exp (R w / β) := by
      rw [key z, key w]
    have hdiv : R z / β = R w / β := Real.exp_injective hexp
    field_simp at hdiv
    exact hdiv
  have hkl : 0 < ∑ z, q0 z * Real.log (q0 z / qstar q0 R β z) :=
    kl_pos_of_ne hq0 (fun z => qstar_pos hq0 z) hq0sum (qstar_sum_one hq0) hqs_ne
  have hid := F_sub_eq_beta_mul_kl (R := R) (β := β) hq0 hβ (fun z => (hq0 z).le) hq0sum
  unfold gain
  nlinarith [mul_pos hβ hkl, hid]

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

/-- **OSA-3a (rollout deficit).** Any rollout policy `q` sits below the tilted optimum by exactly
`β·KL(q ‖ qstar)`, a nonnegative gap (`kl_nonneg`, `β > 0`) that is `0` iff `q = qstar`. So a naive
rollout that fails to reach `qstar` incurs a strictly positive deficit (no monotone path). That
append-only / myopic rollout *does* fail (plateau / context-collapse / contamination) is the
empirical content grounded by the θ2 survey; the `β·KL` trust region *motivates* slow drift toward
`qstar`, but finite-time convergence is left open (a conjecture, not proved here; OSA-3b; JitRL
2601.18510). -/
theorem rollout_deficit [Nonempty Z] (hq0 : ∀ z, 0 < q0 z) (hβ : 0 < β)
    {q : Z → ℝ} (hq : ∀ z, 0 ≤ q z) (hqsum : ∑ z, q z = 1) :
    F q0 R β q = F q0 R β (qstar q0 R β) - β * ∑ z, q z * Real.log (q z / qstar q0 R β z)
      ∧ 0 ≤ β * ∑ z, q z * Real.log (q z / qstar q0 R β z) := by
  refine ⟨by linarith [F_sub_eq_beta_mul_kl (R := R) (β := β) hq0 hβ hq hqsum], ?_⟩
  exact mul_nonneg hβ.le
    (kl_nonneg hq (fun z => qstar_pos hq0 z) hqsum (qstar_sum_one hq0))

/-! ## OSA-2 / OSA-3b — context-isolated product action space

Two agents with **context isolation** = a product action space `Z1 × Z2` with an independent
base `q0 = q01 ⊗ q02` and a separable reward `R = R1 ⊞ R2`. The partition function factorizes, so
the **gain decomposes additively** (`gain_product`, OSA-2 — the gain over the product *equals* the
sum of per-component gains; this is a decomposition of a **fixed** optimum, **not** an enlargement:
by `qstar_product` the isolated optimum *equals* the monolithic one, so context isolation buys no
extra headroom — additional gain can come only from genuinely new non-degenerate rewards), and the
**optimal policy factorizes** (`qstar_product`, OSA-3b — per-isolated-component credit-assigned
tilting equals the global `qstar`, which is T1-optimal). -/

section Product

variable {Z1 Z2 : Type*} [Fintype Z1] [Fintype Z2]
variable {q01 R1 : Z1 → ℝ} {q02 R2 : Z2 → ℝ} {β : ℝ}

/-- The partition function factorizes over a context-isolated product (pure algebra). -/
theorem Zpart_product :
    Zpart (fun p : Z1 × Z2 => q01 p.1 * q02 p.2) (fun p => R1 p.1 + R2 p.2) β
      = Zpart q01 R1 β * Zpart q02 R2 β := by
  unfold Zpart
  rw [Fintype.sum_prod_type]
  rw [Finset.sum_mul_sum]
  refine Finset.sum_congr rfl (fun z1 _ => Finset.sum_congr rfl (fun z2 _ => ?_))
  rw [add_div, Real.exp_add]; ring

/-- The product reference distribution sums to one. -/
theorem prod_sum_one (hq01sum : ∑ z, q01 z = 1) (hq02sum : ∑ z, q02 z = 1) :
    ∑ p : Z1 × Z2, q01 p.1 * q02 p.2 = 1 := by
  rw [Fintype.sum_prod_type, ← Finset.sum_mul_sum, hq01sum, hq02sum, mul_one]

/-- The expected separable reward is additive. -/
theorem meanR_product (hq01sum : ∑ z, q01 z = 1) (hq02sum : ∑ z, q02 z = 1) :
    ∑ p : Z1 × Z2, (q01 p.1 * q02 p.2) * (R1 p.1 + R2 p.2)
      = (∑ z, q01 z * R1 z) + (∑ z, q02 z * R2 z) := by
  rw [Fintype.sum_prod_type]
  have : ∀ z1, ∑ z2, q01 z1 * q02 z2 * (R1 z1 + R2 z2)
      = q01 z1 * R1 z1 + q01 z1 * (∑ z2, q02 z2 * R2 z2) := by
    intro z1
    have hpt : ∀ z2, q01 z1 * q02 z2 * (R1 z1 + R2 z2)
        = q01 z1 * R1 z1 * q02 z2 + q01 z1 * (q02 z2 * R2 z2) := fun z2 => by ring
    rw [Finset.sum_congr rfl (fun z2 _ => hpt z2), Finset.sum_add_distrib,
      ← Finset.mul_sum, hq02sum, mul_one, ← Finset.mul_sum]
  rw [Finset.sum_congr rfl (fun z1 _ => this z1), Finset.sum_add_distrib,
    ← Finset.sum_mul, hq01sum, one_mul]

/-- **OSA-2 (additive decomposition of the gain over isolated agents).** The gain over a
context-isolated product **equals the sum** of the per-component gains. This is a decomposition of a
*fixed* optimum, not an enlargement of it: by `qstar_product` the context-isolated optimum coincides
with the monolithic optimum, so an independent agent adds **no** optimization headroom beyond what a
single model already attains on the same reward — extra gain requires a genuinely new
non-degenerate reward. -/
theorem gain_product [Nonempty Z1] [Nonempty Z2]
    (hq01 : ∀ z, 0 < q01 z) (hq02 : ∀ z, 0 < q02 z) (hβ : 0 < β)
    (hq01sum : ∑ z, q01 z = 1) (hq02sum : ∑ z, q02 z = 1) :
    gain (fun p : Z1 × Z2 => q01 p.1 * q02 p.2) (fun p => R1 p.1 + R2 p.2) β
      = gain q01 R1 β + gain q02 R2 β := by
  have e0 := gain_eq (q0 := fun p : Z1 × Z2 => q01 p.1 * q02 p.2)
      (R := fun p => R1 p.1 + R2 p.2)
      (fun p => mul_pos (hq01 p.1) (hq02 p.2)) hβ (prod_sum_one hq01sum hq02sum)
  rw [e0, gain_eq hq01 hβ hq01sum, gain_eq hq02 hβ hq02sum,
    Zpart_product, Real.log_mul (Zpart_pos hq01).ne' (Zpart_pos hq02).ne',
    meanR_product hq01sum hq02sum]
  ring

/-- **OSA-3b (optimal policy factorizes = credit-assigned tilt reaches the global optimum).**
The Gibbs optimum over the isolated product is the product of the per-component optima, so
per-isolated-component (credit-assigned) tilting equals the global `qstar` — which is T1-optimal. -/
theorem qstar_product (p : Z1 × Z2) :
    qstar (fun p : Z1 × Z2 => q01 p.1 * q02 p.2) (fun p => R1 p.1 + R2 p.2) β p
      = qstar q01 R1 β p.1 * qstar q02 R2 β p.2 := by
  unfold qstar
  rw [Zpart_product, add_div, Real.exp_add]
  ring

end Product

end TfrlProofs.OptSpace
