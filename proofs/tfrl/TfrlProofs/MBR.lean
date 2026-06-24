import Mathlib

set_option linter.style.header false

/-!
# T5 — MBR consistency (Strong Law of Large Numbers)

Minimum-Bayes-Risk (MBR) decoding scores a candidate `c` by the *expected* loss
against the (unknown) reference/output distribution,
```
ρ(c) = 𝔼_{Y}[ ℓ(c, Y) ].
```
In practice we cannot compute `ρ(c)`; we use the **empirical MBR objective** over
`n` i.i.d. Monte-Carlo samples `Y₀, …, Y_{n-1}`,
```
ρ̂ₙ(c) = (1/n) ∑_{i<n} ℓ(c, Yᵢ).
```

**Consistency (`mbr_consistency`).** For a fixed candidate, if the per-sample losses
`L i ω = ℓ(c, Yᵢ(ω))` are i.i.d. (pairwise independent and identically distributed)
and integrable, then `ρ̂ₙ(c) → ρ(c)` almost surely as `n → ∞`. This is a direct
instance of Mathlib's strong law of large numbers (`ProbabilityTheory.strong_law_ae`,
Etemadi's pairwise-independent version).

The empirical objective here is written `(n : ℝ)⁻¹ • ∑ i ∈ range n, L i ω` to match
the Mathlib statement exactly; this equals `(1/n) ∑ … ℓ(c, Yᵢ)`.
-/

namespace TfrlProofs.MBR

open MeasureTheory ProbabilityTheory Filter Topology
open scoped BigOperators Function

variable {Ω : Type*} [MeasurableSpace Ω] {μ : Measure Ω}

/-- **T5 (MBR consistency, SLLN).** For a fixed candidate whose per-sample MBR losses
`L : ℕ → Ω → ℝ` are integrable, pairwise independent, and identically distributed,
the empirical MBR objective converges almost surely to the population MBR objective
`μ[L 0] = 𝔼[ℓ(c, Y)]`. -/
theorem mbr_consistency
    (L : ℕ → Ω → ℝ)
    (hint : Integrable (L 0) μ)
    (hindep : Pairwise ((· ⟂ᵢ[μ] ·) on L))
    (hident : ∀ i, IdentDistrib (L i) (L 0) μ μ) :
    ∀ᵐ ω ∂μ, Tendsto (fun n : ℕ ↦ (n : ℝ)⁻¹ • (∑ i ∈ Finset.range n, L i ω))
      atTop (𝓝 (μ[L 0])) :=
  strong_law_ae L hint hindep hident

end TfrlProofs.MBR
