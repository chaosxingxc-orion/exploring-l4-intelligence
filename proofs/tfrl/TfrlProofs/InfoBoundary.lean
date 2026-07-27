import Mathlib

set_option linter.style.header false
set_option linter.style.longLine false

/-!
# T8 — The fixed-pool information boundary

This file proves a narrow but useful fact: a selector that must return one of a fixed set of sampled
candidates cannot be correct unless that pool contains a correct candidate. Best-of-N, majority and MBR
belong to this class only while the candidate pool is held fixed.

The result is deliberately not a theorem about system-level in-context control. Any action that constructs
a new context and generates again leaves the fixed-pool class, whether the new context carries external
facts or reorganizes information already available to the frozen model. Consequently a finite-pool oracle
gap cannot establish an under-all-contexts capability gap and cannot be used to rule out ICL gains.

`newinfo_can_cross_gap` is a framing-only witness that a different sampler can hit when the original pool
misses. It identifies no real retrieval, memory or tool mechanism and does not prove external information
is the only way to alter reachability.
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
-dependent*: a lever that changes the sampling distribution can cross a gap that is impassable for that
fixed read-out pool. No claim about all possible contexts or about ICL follows.

⚠ **FRAMING-ONLY (2026-07-07 WS-E re-grade).** The witness below is a trivial `∃` over `Fin 1 → Bool`
(const-`false` vs const-`true`); it models NO retrieval/injection/memory mechanism. It proves only that
*some* distribution *can* differ — not that RAG/memory *does* cross the gap. Under the theory-track
discipline this carries **no result** (same class as the D3-review re-grade of the read-out counting
bounds as "a framing bound, not a contribution"). Do not cite it as evidence that knowledge injection
works. See `[[2026-07-07-knowledge-proof-honest-accounting-and-feasibility]]`. -/
theorem newinfo_can_cross_gap :
    ∃ (s s' : Fin 1 → Bool), (∀ i, s i ≠ true) ∧ (∃ j, s' j = true) :=
  ⟨fun _ => false, fun _ => true, by decide, ⟨0, rfl⟩⟩

end TfrlProofs.InfoBoundary
