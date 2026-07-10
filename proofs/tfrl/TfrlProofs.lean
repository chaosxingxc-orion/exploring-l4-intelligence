import TfrlProofs.Basic
import TfrlProofs.Tilting
import TfrlProofs.Suppression
import TfrlProofs.Plurality
import TfrlProofs.BestOfN
import TfrlProofs.MBR
import TfrlProofs.Regret
import TfrlProofs.OptSpace
import TfrlProofs.Realization
import TfrlProofs.BlindSpot
import TfrlProofs.Reachability
import TfrlProofs.InfoBoundary
import TfrlProofs.AgenticElements
import TfrlProofs.BestOfNConvergence
import TfrlProofs.Iterate

/-!
# TfrlProofs — root module

## Sorry/axiom ledger (keep current)

* **`sorry` count: 0.** The library builds with no `sorry` anywhere.
* **Named axioms: 1** — `TfrlProofs.BestOfN.beirami_thm_3_1`, the Beirami et al. (2024)
  order-statistics estimate `KL(π_BoN ‖ π₀) ≤ log N − (N−1)/N` (arXiv:2401.01879,
  Theorem 3.1: finite outcome space, distinct rewards / Assumption 2.1, an **upper
  bound**, not an equality). It is stated about the *opaque* functional
  `TfrlProofs.BestOfN.klBoNActual` (a fixed but unspecified `ℕ → ℝ`), which keeps the
  axiom satisfiable — hence consistent — unlike a universally-quantified version, which
  would be false. It replaced the former documented `sorry`
  (`klBoN_le_klBoundBoN_TODO`, removed 2026-07-10); `kl_best_of_n_le` now consumes it
  directly. Audit with `#print axioms TfrlProofs.BestOfN.kl_best_of_n_le`.
-/
