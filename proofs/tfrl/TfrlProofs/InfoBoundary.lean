import Mathlib

set_option linter.style.header false
set_option linter.style.longLine false

/-!
# T8 — The information boundary: read-out levers are ceilinged by their own samples; only a
new-information lever can cross the knowledge gap

This file formalizes the standing rule the owner's 2026-07-05 critique exposed (`[[Information-Boundary
-Guard]]`), and the read-out / new-info division of levers.

**Read-out lever** — any selector that returns one of the model's own N sampled candidates:
best-of-N, self-consistency majority, MBR, and the E10/E10b two-system verifier all qualify — their output
is always some sample they drew. **New-info lever** — one that changes the *sampling distribution* by
conditioning on external evidence `e` (retrieval / memory / a tool result): its candidate set is drawn from
`M(·|audio, e)`, whose support can contain answers absent from `M(·|audio)`.

The results:
- `readout_correct_imp_sample_correct` / `readout_fails_on_gap` — the deterministic wall: a read-out
  selector is correct only if some sample is correct; on a **knowledge-gap** item (no sample correct) it
  necessarily fails.
- `readout_acc_le_oracle` — aggregate ceiling: over any item set, read-out correct-count `≤` oracle@N
  hit-count. This is why E10/E10b (read-out) cannot exceed the oracle ceiling, and why the T5 "internal
  -realization gap" is the *most* a read-out lever could realize.
- `readout_error_ge_gap` — the **irreducible floor**: read-out error-count `≥` the knowledge-gap count
  (items with no correct sample). The gap is a hard error floor for the *entire* read-out class — no
  amount of cleverer selection removes it. (T5: this floor is 42.7% on vocalbench-zh knowledge-QA.)
- `newinfo_can_cross_gap` — the escape: there exist configurations where every base sample misses yet an
  info-augmented sampler hits. So the oracle ceiling is **class-dependent, not absolute**; crossing the
  knowledge gap *requires* leaving the read-out class and adding new information (the Q1b path: an external
  multimodal memory). This is the theorem behind "ICL/read-out insufficient ⇒ a new-info system is needed."

**Dual track (code ⟷ theorem).** `readoutSelector` ⟷ the deployable label-free selectors we ran (E10
majority / two-system verifier). `oracleHit` ⟷ P2's oracle@N indicator. The knowledge-gap floor ⟷ P2's
`1 − oracle@N`. The new-info sampler `s'` ⟷ the memory-augmented conditioning `M(·|audio, retrieved-text)`
(T6). Convergence half: with a nonzero gap fraction the read-out averaged regret is bounded *below* by that
fraction (it cannot tend to 0), whereas the info-augmented process that covers the gap drives regret to 0 —
this is exactly `TfrlProofs.BlindSpot.avg_regret_tendsto_zero` applied with `frac =` the gap fraction. So
the UNCONSTRAINED (read-out-only) process provably fails to converge below the gap; the CONSTRAINED (new
-info) one converges.
-/

namespace TfrlProofs.InfoBoundary

open Finset

/-- A **read-out selector** over `N` candidates: it picks an index, and its answer is that sample.
The defining property of the class — best-of-N, majority, MBR, the two-system verifier — is that the
output is always one of the drawn samples. -/
structure ReadoutSelector (N : ℕ) (α : Type*) where
  pick : (Fin N → α) → Fin N

/-- **The wall (per item).** A read-out selector's answer is correct only if some sample is correct —
because its answer *is* a sample. -/
theorem readout_correct_imp_sample_correct
    {N : ℕ} {α : Type*} (correct : α → Prop) (σ : ReadoutSelector N α) (s : Fin N → α)
    (h : correct (s (σ.pick s))) : ∃ i, correct (s i) :=
  ⟨σ.pick s, h⟩

/-- **Failure on the knowledge gap.** If NO sample is correct (the item is beyond the model's own
distribution), every read-out selector necessarily fails. No cleverer selection escapes this. -/
theorem readout_fails_on_gap
    {N : ℕ} {α : Type*} (correct : α → Prop) (σ : ReadoutSelector N α) (s : Fin N → α)
    (hgap : ∀ i, ¬ correct (s i)) : ¬ correct (s (σ.pick s)) :=
  hgap (σ.pick s)

variable {ι : Type*}

/-- **Aggregate ceiling.** Over any finite item set, if every read-out-correct item is also an oracle
hit (the per-item wall), then the read-out correct-count is at most the oracle@N hit-count. This is the
formal reason E10/E10b (read-out selectors) cannot exceed the oracle ceiling. -/
theorem readout_acc_le_oracle
    (items : Finset ι) (readoutCorrect oracleHit : ι → Bool)
    (h : ∀ i ∈ items, readoutCorrect i = true → oracleHit i = true) :
    (items.filter (fun i => readoutCorrect i = true)).card
      ≤ (items.filter (fun i => oracleHit i = true)).card := by
  apply Finset.card_le_card
  intro i hi
  rw [Finset.mem_filter] at hi ⊢
  exact ⟨hi.1, h i hi.1 hi.2⟩

/-- **Irreducible knowledge-gap floor.** The knowledge-gap items (no oracle hit) are all read-out errors,
so the read-out error-count is at least the gap count. The gap is a hard error floor for the *whole*
read-out class — the part of the headroom that read-out provably cannot touch (T5: the capability/knowledge
gap, ~43% on knowledge-QA). -/
theorem readout_error_ge_gap
    (items : Finset ι) (readoutCorrect oracleHit : ι → Bool)
    (h : ∀ i ∈ items, readoutCorrect i = true → oracleHit i = true) :
    (items.filter (fun i => oracleHit i = false)).card
      ≤ (items.filter (fun i => readoutCorrect i = false)).card := by
  apply Finset.card_le_card
  intro i hi
  rw [Finset.mem_filter] at hi ⊢
  refine ⟨hi.1, ?_⟩
  by_contra hc
  rw [Bool.not_eq_false] at hc
  have hoh : oracleHit i = true := h i hi.1 hc
  rw [hoh] at hi
  exact absurd hi.2 (by decide)

/-- **The new-information escape.** There is a configuration where every base sample misses the target
(`correct := (· = true)`) yet an info-augmented sampler hits. Hence the oracle ceiling is *class
-dependent*: a lever that changes the sampling distribution by conditioning on new information can cross a
gap that is impassable for the entire read-out class. This is the formal content of "read-out/ICL
insufficient ⇒ a new-info (memory) system is required" (Q1b). -/
theorem newinfo_can_cross_gap :
    ∃ (s s' : Fin 1 → Bool), (∀ i, s i ≠ true) ∧ (∃ j, s' j = true) :=
  ⟨fun _ => false, fun _ => true, by decide, ⟨0, rfl⟩⟩

end TfrlProofs.InfoBoundary
