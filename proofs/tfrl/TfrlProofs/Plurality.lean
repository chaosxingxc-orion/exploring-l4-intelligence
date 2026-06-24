import Mathlib

set_option linter.style.header false

/-!
# T4 — Strict-plurality (Condorcet) gate

If some candidate `a` strictly beats every other candidate `b ≠ a` in vote count,
then `a` is the (unique) argmax: every candidate has count `≤ count a`, and any
candidate achieving that maximum must equal `a`.

This is the combinatorial gate that justifies a deterministic plurality vote /
self-consistency selection: a strict plurality winner is well-defined and unique.
-/

namespace TfrlProofs.Plurality

variable {K : Type*}

/-- A *strict plurality winner* `a`: it strictly out-counts every other candidate. -/
def IsStrictPluralityWinner (count : K → ℕ) (a : K) : Prop :=
  ∀ b, b ≠ a → count b < count a

/-- A strict plurality winner is a maximizer: no candidate has a higher count. -/
theorem le_of_strictPluralityWinner
    {count : K → ℕ} {a : K} (h : IsStrictPluralityWinner count a) :
    ∀ b, count b ≤ count a := by
  intro b
  by_cases hb : b = a
  · subst hb; exact le_rfl
  · exact (h b hb).le

/-- A strict plurality winner is the *unique* maximizer: any candidate whose count
    is at least `count a` must be `a` itself. -/
theorem eq_of_count_ge_strictPluralityWinner
    {count : K → ℕ} {a : K} (h : IsStrictPluralityWinner count a) :
    ∀ b, count a ≤ count b → b = a := by
  intro b hb
  by_contra hba
  -- `b ≠ a` gives `count b < count a`, contradicting `count a ≤ count b`.
  exact absurd hb (not_le.mpr (h b hba))

/-- **T4 (strict-plurality gate).** If `a` strictly beats every other candidate,
    then `a` is the unique argmax of `count`: it is a maximizer, and any maximizer
    equals `a`. -/
theorem strictPlurality_unique_argmax
    {count : K → ℕ} {a : K} (h : IsStrictPluralityWinner count a) :
    (∀ b, count b ≤ count a) ∧ (∀ b, count a ≤ count b → b = a) :=
  ⟨le_of_strictPluralityWinner h, eq_of_count_ge_strictPluralityWinner h⟩

/-- Packaged existence form: a strict-plurality hypothesis yields a unique argmax. -/
theorem exists_unique_argmax_of_strictPlurality
    {count : K → ℕ}
    (h : ∃ a, ∀ b, b ≠ a → count b < count a) :
    ∃ a, (∀ b, count b ≤ count a) ∧ (∀ b, count a ≤ count b → b = a) := by
  obtain ⟨a, ha⟩ := h
  exact ⟨a, strictPlurality_unique_argmax ha⟩

end TfrlProofs.Plurality
