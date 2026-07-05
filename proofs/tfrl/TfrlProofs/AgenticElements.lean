import Mathlib
import TfrlProofs.InfoBoundary

set_option linter.style.header false
set_option linter.style.longLine false

/-!
# Agentic-level: a single-model USAGE PATTERN can't reach the under-all-contexts gap; only a new-info ELEMENT can

This lifts the read-out/new-info theorem (`TfrlProofs.InfoBoundary`) to the **agent-system** level, giving
the 2026-07-06 elements-vs-usage framework its machine-checked spine (D0
`[[2026-07-06-omni-agent-elements-vs-usage-framework]]`).

**Modelling.** A **usage pattern over one frozen model** — a role assignment, a "critic/verifier" prompt, a
multi-agent debate of the *same* weights, an orchestration/routing loop — ultimately emits an answer that
the frozen model `M` can itself produce **under some context** `ctx` (the role/system-prompt/turn-history).
Roles and prompts only *vary the context*; they add no information the model could not already emit under
*some* context. Formally: the system's answer satisfies `∃ ctx, M_can_output input ctx answer`.

The load-bearing quantity is then the **under-all-contexts knowledge gap**: an item where `M` cannot emit a
correct answer under **any** context. On such an item every single-model usage pattern necessarily fails —
because its answer is an `M`-output under *some* context, and none of those is correct
(`single_model_gap_unreachable`). This is the exact reason the E10/E10b two-system verifier (same weights,
critic prompt) never beats plain sampling: it is a usage pattern, and the ∀-context quantifier is what
prompt/role engineering cannot escape.

A **new-info element** (a tool that computes/fetches new facts, external knowledge, a memory holding
external content, or a genuinely complementary model) can emit an answer **not** of the form `M(input,·)`,
so it can be correct where the under-all-contexts gap holds (`external_element_can_escape`). Hence the
framework thesis: *for a frozen model, agentic leverage can only come from a new-info element, not a usage
pattern over the same model.*

**Dual track.** `M_can_output` ⟷ the frozen omni's context-conditioned generation; the ∀-context gap ⟷ the
capability/knowledge gap of T5 (`1 − oracle@N`, ~43% on knowledge-QA), taken over *all* prompt/role
contexts; `external_element_can_escape` ⟷ the audio-keyed memory / verifier-as-tool that supplies new info.
The finite-pool corollary `single_model_system_fails_on_gap` bridges to `InfoBoundary.readout_fails_on_gap`.
-/

namespace TfrlProofs.AgenticElements

open TfrlProofs.InfoBoundary

variable {Input Ctx α : Type*}

/-- **The agentic wall.** A single-model usage pattern emits an answer the frozen model `M` can produce
under *some* context (`hsys`). If the item is an **under-all-contexts knowledge gap** — `M` cannot emit a
correct answer under *any* context (`hgap`) — then the system's answer is wrong. Roles, critic prompts,
multi-agent debate of one model, orchestration: all only vary `ctx`, so none escapes the ∀-context gap. -/
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
new-info element. -/
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
