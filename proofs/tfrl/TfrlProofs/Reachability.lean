import Mathlib

set_option linter.style.header false

/-!
# TH2 — (b)-reachability: when can adjusting the conditioning A shift the greedy answer?

The strict review noted the library has **no theorem for condition (b)** (prompt/conditioning
reachability). This file supplies one. Adjusting the conditioning `A` reweights the frozen base
distribution: `q_A z ∝ q0 z · w z`, where `w : Z → ℝ` is the (nonnegative) multiplicative effect of `A`
(few-shot demos, an instruction, a system prompt). Deployment reads the **mode** (greedy), so the
question "can adjusting A make the good answer `z*` the greedy output?" is: is `z*` the argmax of `q_A`?
The normalizer cancels, so `z*` beats the base mode `m` under `A` iff `q0 z*·w z* > q0 m·w m`.

- `mode_shift_iff_ratio` — the exact characterization: `z*` becomes modal iff the reweighting ratio
  `w z*/w m` exceeds the initial odds `q0 m/q0 z*`.
- `reachability_needs_reach` — if `A`'s reweighting power is bounded (`w z*/w m ≤ R`), then making `z*`
  modal *requires* `q0 m/q0 z* < R`.
- `too_improbable_unreachable` — **the (b)-cap**: if `z*` is too improbable under the frozen base
  relative to `A`'s bounded power (`R ≤ q0 m/q0 z*`), then **no** conditioning within that power makes
  `z*` the greedy answer. This is the theory pairing for the measured "adjusting A (few-shot / prompt)
  does not lift greedy toward the oracle": the good answers exist in the pool (oracle-δ > 0) but sit too
  far below the mode for a bounded prompt-reweighting to promote them. The constraint term is `R` (the
  conditioning's reweighting reach / trust region).
-/

namespace TfrlProofs.Reachability

variable {Z : Type*}

/-- **(b) mode-shift characterization.** With a strictly positive base `q0` and reweighting `w`, the
good answer `z*` overtakes the base mode `m` under `A` (`q0 m·w m < q0 z*·w z*`, i.e. `z*` is preferred
after normalization) **iff** the reweighting ratio exceeds the initial odds: `q0 m/q0 z* < w z*/w m`. -/
theorem mode_shift_iff_ratio (q0 w : Z → ℝ) (zstar m : Z)
    (hqs : 0 < q0 zstar) (hwm : 0 < w m) :
    q0 m * w m < q0 zstar * w zstar ↔ q0 m / q0 zstar < w zstar / w m := by
  rw [div_lt_div_iff hqs hwm, mul_comm (w zstar) (q0 zstar)]

/-- If `A`'s reweighting power is bounded by `R` (`w z*/w m ≤ R`), then making `z*` the greedy answer
requires the initial odds `q0 m/q0 z*` to be below `R`. -/
theorem reachability_needs_reach (q0 w : Z → ℝ) (zstar m : Z) (R : ℝ)
    (hqs : 0 < q0 zstar) (hwm : 0 < w m)
    (hbound : w zstar / w m ≤ R)
    (hmodal : q0 m * w m < q0 zstar * w zstar) :
    q0 m / q0 zstar < R :=
  lt_of_lt_of_le ((mode_shift_iff_ratio q0 w zstar m hqs hwm).mp hmodal) hbound

/-- **The (b)-cap (impossibility under bounded conditioning).** If the good answer is too improbable
under the frozen base relative to `A`'s bounded reweighting power (`R ≤ q0 m/q0 z*` and `w z*/w m ≤ R`),
then **no** conditioning within that power makes `z*` the greedy output. -/
theorem too_improbable_unreachable (q0 w : Z → ℝ) (zstar m : Z) (R : ℝ)
    (hqs : 0 < q0 zstar) (hwm : 0 < w m)
    (hbound : w zstar / w m ≤ R) (hfar : R ≤ q0 m / q0 zstar) :
    ¬ q0 m * w m < q0 zstar * w zstar := by
  intro hmodal
  exact absurd (reachability_needs_reach q0 w zstar m R hqs hwm hbound hmodal) (not_lt.mpr hfar)

end TfrlProofs.Reachability
