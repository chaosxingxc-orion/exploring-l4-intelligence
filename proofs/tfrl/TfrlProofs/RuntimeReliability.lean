import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith.Frontend

set_option linter.style.header false

/-!
# Runtime reliability under a bounded reward-estimation error

The frozen core is treated as an API.  An external controller keeps an incumbent answer and may
replace it with a selected answer only when the estimated-reward margin is large enough.  If the
deployment-available estimate `Rhat` is uniformly within `ε` of the task utility `U`, a margin of
`2 * ε` is sufficient for true non-regression; a strict margin is sufficient for strict improvement.

These are conditional decision lemmas, not an empirical guarantee.  Lean verifies the implication
from the error-bound hypothesis.  The project must estimate and stress-test that hypothesis on
held-out task/acoustic strata; a compiled theorem cannot establish it for a real evaluator.
-/

namespace TfrlProofs.RuntimeReliability

variable {Z : Type*}

/-- If the estimated selected-over-incumbent margin is at least twice the uniform estimation error,
the selected answer is no worse than the incumbent under true utility. -/
theorem true_nonregression_of_estimated_margin
    (U Rhat : Z → ℝ) (selected incumbent : Z) (ε : ℝ)
    (herror : ∀ z, |Rhat z - U z| ≤ ε)
    (hmargin : Rhat incumbent + 2 * ε ≤ Rhat selected) :
    U incumbent ≤ U selected := by
  have hincumbent := (abs_le.mp (herror incumbent)).1
  have hselected := (abs_le.mp (herror selected)).2
  linarith

/-- A strict estimated margin above twice the uniform estimation error implies strict true-utility
improvement over the incumbent. -/
theorem true_improvement_of_estimated_margin
    (U Rhat : Z → ℝ) (selected incumbent : Z) (ε : ℝ)
    (herror : ∀ z, |Rhat z - U z| ≤ ε)
    (hmargin : Rhat incumbent + 2 * ε < Rhat selected) :
    U incumbent < U selected := by
  have hincumbent := (abs_le.mp (herror incumbent)).1
  have hselected := (abs_le.mp (herror selected)).2
  linarith

end TfrlProofs.RuntimeReliability
