import TfrlProofs.RuntimeReliability

#eval 1+1

open TfrlProofs.RuntimeReliability

example :
    let U : Bool → ℝ := fun z => if z then 1 else 0
    U false < U true := by
  intro U
  apply true_improvement_of_estimated_margin U U true false 0
  · intro z
    simp [U]
  · simp [U]

example :
    let U : Bool → ℝ := fun z => if z then 1 else 0
    U false ≤ U true := by
  intro U
  apply true_nonregression_of_estimated_margin U U true false 0
  · intro z
    simp [U]
  · simp [U]
