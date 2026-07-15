import Mathlib
import TfrlProofs.Realization

set_option linter.style.header false

/-!
# TH2a — Two context-differentiated systems: realization up to a knowledge-blind-spot floor

The omni verifier is NOT self-reward: it is **two context-differentiated systems** — a generator-agent
`S_G = M(·|c_G)` and a verifier-agent `S_V = M(·|c_V)`, the *same* frozen weights under *distinct*
system-prompt/context. Because context differentiation elicits functionally different behaviour from the
same weights (the basis of in-context learning), the two systems' errors are **not** automatically
correlated; the load-bearing quantity is the achievable error-**decorrelation**.

This file formalizes the resulting convergence judgment as a **coverage bound**. Partition the items into
- `K` (the complement of `U`): items the verifier-agent realizes the oracle on (per-item regret `0`) —
  this is where context differentiation decorrelates `S_V` from `S_G`; and
- `U`: the residual **shared knowledge blind-spot** — items where the frozen `M` genuinely lacks the
  information, so *no* context differentiation helps and both systems necessarily fail (regret `≤ B`, the
  reward range).

Then total regret `≤ B · |U|` (`total_regret_le`), i.e. realized reward `≥ oracle − B·(|U|/n)`; and as the
blind-spot **fraction** `→ 0`, the averaged regret `→ 0` — realized converges to the oracle
(`avg_regret_tendsto_zero`). The constraint term is the blind-spot fraction (`= 1 −` decorrelation
coverage). Per-item, `reg i ≤ 2·τ i` is the C4 bound `TfrlProofs.Realization.realized_gap_le_two_tau`;
on `K` the verifier's estimation error is small (decorrelated ⇒ `τ i ≈ 0`), on `U` it is not.

**Dual track (owner 2026-07-05).** `U` = the public knowledge blind-spot, PARKED: it is filled by an
*independent-of-M* signal — the omni-embedding system (W4) — which needs new omni agentic tasks (out of
scope here). Engineering (E10) must MEASURE the decorrelation coverage `|K|/n` (the ablation
coupled-vs-isolated context), not assume it is `1` (the earlier over-strong "shared-weights hard floor"
claim) nor `0`.
-/

namespace TfrlProofs.BlindSpot

open Finset

variable {ι : Type*} [Fintype ι]

/-- **Coverage / blind-spot realization bound.** If the per-item regret is `0` off the blind-spot `U`
(the verifier-agent realizes the oracle there) and `≤ B` on `U` (the reward range), then the total regret
is at most `B · |U|`. Equivalently realized reward `≥ oracle − B·|U|`: the composition realizes the oracle
except on the residual knowledge blind-spot. -/
theorem total_regret_le (reg : ι → ℝ) (U : Finset ι) (B : ℝ)
    (hK : ∀ i, i ∉ U → reg i = 0)
    (hU : ∀ i, i ∈ U → reg i ≤ B) :
    ∑ i, reg i ≤ B * U.card := by
  have hsplit : ∑ i, reg i = ∑ i ∈ U, reg i := by
    symm
    exact Finset.sum_subset (Finset.subset_univ U) (fun x _ hx => hK x hx)
  rw [hsplit]
  calc ∑ i ∈ U, reg i
      ≤ ∑ _i ∈ U, B := Finset.sum_le_sum (fun i hi => hU i hi)
    _ = U.card • B := Finset.sum_const B
    _ = B * (U.card : ℝ) := by rw [nsmul_eq_mul]; ring

/-- **Convergence to the oracle as the blind-spot fraction vanishes.** For a sequence of runs whose
averaged regret `avgreg n` is nonnegative and bounded by `B ·` the blind-spot fraction `frac n`, if
`frac n → 0` (context differentiation drives the decorrelation coverage to full) then the averaged regret
`→ 0`: the two-system composition realizes the oracle in the limit. The constraint term is `frac`
(`= 1 −` decorrelation coverage); a nonzero residual `frac` is exactly the parked knowledge blind-spot. -/
theorem avg_regret_tendsto_zero (avgreg frac : ℕ → ℝ) (B : ℝ)
    (h0 : ∀ n, 0 ≤ avgreg n) (hle : ∀ n, avgreg n ≤ B * frac n)
    (hfrac : Filter.Tendsto frac Filter.atTop (nhds 0)) :
    Filter.Tendsto avgreg Filter.atTop (nhds 0) := by
  refine squeeze_zero h0 hle ?_
  simpa using hfrac.const_mul B

end TfrlProofs.BlindSpot
