import Mathlib
import TfrlProofs.InfoBoundary

set_option linter.style.header false
set_option linter.style.longLine false

/-!
# Agentic-level conditional bound under an explicit all-contexts gap

`single_model_gap_unreachable` says that a system output is wrong if it is produced by the frozen model
under some context and the answer is wrong under every possible context. This is valid but conditional:
the theorem does not establish that the all-contexts premise holds for a real benchmark item.

The earlier commentary equating a finite-sample oracle miss with an all-contexts gap is withdrawn. A
finite pool covers only the contexts and samples actually executed. System-level in-context control may
reach an answer available under another context, so this module cannot support the claim that agentic
leverage must come only from external new information.

`external_element_can_escape` remains a framing-only logical witness. The finite-pool corollary
`single_model_system_fails_on_gap` bridges only to `InfoBoundary.readout_fails_on_gap`.
-/

namespace TfrlProofs.AgenticElements

open TfrlProofs.InfoBoundary

variable {Input Ctx α : Type*}

/-- **The agentic wall.** A single-model usage pattern emits an answer the frozen model `M` can produce
under *some* context (`hsys`). If the item is an **under-all-contexts knowledge gap** — `M` cannot emit a
correct answer under *any* context (`hgap`) — then the system's answer is wrong. The theorem does not
establish `hgap` and therefore does not rule out gains from prompts, memory state or orchestration. -/
theorem single_model_gap_unreachable
    (M_can_output : Input → Ctx → α → Prop) (correct : α → Prop)
    (input : Input) (sys_out : α)
    (hsys : ∃ ctx, M_can_output input ctx sys_out)
    (hgap : ∀ ctx a, M_can_output input ctx a → ¬ correct a) :
    ¬ correct sys_out := by
  obtain ⟨ctx, h⟩ := hsys
  exact hgap ctx sys_out h

/-- **The new-info escape.** A new-info element can emit an answer that is *not* an `M`-output under any
context, so there exist configurations where the under-all-contexts gap holds yet the element is correct.
The oracle ceiling of the single-model class is therefore not absolute — crossing it *requires* a genuine
new-info element.

⚠ **FRAMING-ONLY (2026-07-07 WS-E re-grade).** The witness is trivial (`M` const-`false`, `correct := (·
= true)`, external output `true`); it models NO actual element mechanism. It proves only that an escape is
*logically possible*, not that any real tool/memory/element achieves it. No contribution under the
theory-track discipline. See `[[2026-07-07-knowledge-proof-honest-accounting-and-feasibility]]`. -/
theorem external_element_can_escape :
    ∃ (M_can_output : Unit → Unit → Bool → Prop) (correct : Bool → Prop) (input : Unit) (ext_out : Bool),
      (∀ ctx a, M_can_output input ctx a → ¬ correct a) ∧ correct ext_out :=
  ⟨fun _ _ a => a = false, fun a => a = true, (), true, by
    rintro _ a rfl; simp, rfl⟩

/-- **Finite-pool bridge to `InfoBoundary`.** A single-model system that returns one of its `K`
model-generated candidates is a read-out selector; when none of the `K` candidates is correct (the gap) it
fails. This is exactly `InfoBoundary.readout_fails_on_gap` re-read at the agent-system level. -/
theorem single_model_system_fails_on_gap
    {K : ℕ} (correct : α → Prop) (σ : ReadoutSelector K α) (gen : Fin K → α)
    (hgap : ∀ i, ¬ correct (gen i)) : ¬ correct (gen (σ.pick gen)) :=
  readout_fails_on_gap correct σ gen hgap

end TfrlProofs.AgenticElements
