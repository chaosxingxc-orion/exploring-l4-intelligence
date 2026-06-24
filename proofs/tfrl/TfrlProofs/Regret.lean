import Mathlib
import TfrlProofs.BestOfN

set_option linter.style.header false

/-!
# T6 — Best-of-N regret is `O(√log N)`

Combine two ingredients:

* **Pinsker / bounded-reward gain.** If the reward is bounded by `R_max` in absolute
  value, the expected-reward gain of any policy `π` over the base `π₀` is controlled
  by total variation, and via Pinsker's inequality by the square-root of the KL:
  ```
  gain(π) = 𝔼_π[r] - 𝔼_{π₀}[r] ≤ R_max · √(KL(π ‖ π₀) / 2).
  ```
  (`TV ≤ √(KL/2)` is Pinsker; `gain ≤ 2 R_max · TV`-type bounds give the displayed
  form. We take this estimate as the hypothesis `hPinsker`.)

* **T2 best-of-N KL bound.** `KL(π_BoN ‖ π₀) ≤ klBoundBoN N = log N - (N-1)/N ≤ log N`.

Chaining them (`regret_O_sqrt_log`) yields the explicit regret bound
```
gain(π_BoN) ≤ R_max · √(log N / 2),
```
which is `O(√log N)`. The monotonicity composition is proved rigorously; the Pinsker
estimate is an isolated hypothesis.
-/

namespace TfrlProofs.Regret

open Real
open TfrlProofs.BestOfN

/-- `klBoundBoN N ≤ log N` for `N ≥ 1` (the subtracted `(N-1)/N` is nonnegative). -/
theorem klBoundBoN_le_log {N : ℕ} (hN : 1 ≤ N) : klBoundBoN N ≤ Real.log N := by
  have hNpos : (0 : ℝ) < N := by exact_mod_cast Nat.lt_of_lt_of_le Nat.zero_lt_one hN
  unfold klBoundBoN
  have hsub : 0 ≤ ((N : ℝ) - 1) / N := by
    apply div_nonneg _ hNpos.le
    have : (1 : ℝ) ≤ N := by exact_mod_cast hN
    linarith
  linarith

/-- **T6 (best-of-N regret `O(√log N)`).** Suppose the expected-reward gain of the
best-of-`N` policy over the base policy is Pinsker-bounded by `R_max · √(kl / 2)` for a
KL value `kl`, the reward bound `R_max` is nonnegative, and `kl` obeys the best-of-`N`
KL bound `kl ≤ klBoundBoN N` (T2). Then the regret is `O(√log N)`:
```
gain ≤ R_max · √(log N / 2).
```

Both the Pinsker estimate and the KL bound enter as hypotheses; the conclusion follows
by monotonicity of `√` and `klBoundBoN N ≤ log N`. -/
theorem regret_O_sqrt_log
    {gain R_max kl : ℝ} {N : ℕ} (hN : 1 ≤ N)
    (hRmax : 0 ≤ R_max)
    (hPinsker : gain ≤ R_max * Real.sqrt (kl / 2))
    (hKL : kl ≤ klBoundBoN N) :
    gain ≤ R_max * Real.sqrt (Real.log N / 2) := by
  -- kl ≤ klBoundBoN N ≤ log N, so √(kl/2) ≤ √(log N /2), then multiply by R_max ≥ 0.
  have hkl_log : kl ≤ Real.log N := le_trans hKL (klBoundBoN_le_log hN)
  have hsqrt : Real.sqrt (kl / 2) ≤ Real.sqrt (Real.log N / 2) := by
    apply Real.sqrt_le_sqrt
    linarith
  have hmul : R_max * Real.sqrt (kl / 2) ≤ R_max * Real.sqrt (Real.log N / 2) :=
    mul_le_mul_of_nonneg_left hsqrt hRmax
  linarith

/-- The displayed regret rate is itself nonnegative-and-finite: `R_max · √(log N /2) ≥ 0`
for `N ≥ 1` and `R_max ≥ 0`, confirming the `O(√log N)` bound is a genuine bound. -/
theorem regret_rate_nonneg {R_max : ℝ} {N : ℕ} (hN : 1 ≤ N) (hRmax : 0 ≤ R_max) :
    0 ≤ R_max * Real.sqrt (Real.log N / 2) := by
  have hlog : 0 ≤ Real.log N := by
    apply Real.log_nonneg
    exact_mod_cast hN
  positivity

end TfrlProofs.Regret
