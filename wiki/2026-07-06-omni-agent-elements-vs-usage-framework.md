---
title: "The elements-vs-usage framework: what a frozen omni agentic system can and cannot gain"
date: 2026-07-06
stage: 1-argumentation
status: "ACTIVE — the main thesis of the 2026-07-06 omni-agentic survey campaign (D0). Converged over four rounds of owner Socratic refinement; to be substantiated by the D1/D2 survey and tested as a falsifiable claim."
purpose: "Give the omni agentic system a problem-first anatomy: separate the ELEMENTS a system is built from, the USAGE PATTERNS that wield them, and the CONSTRAINTS that bound them — and prove where training-free leverage over a frozen model can even come from."
---

# The elements-vs-usage framework

> **One-line thesis.** For a **frozen** model, agentic leverage can only come from adding a genuine
> **new-information ELEMENT** (a tool that computes/fetches new facts, external knowledge, a memory holding
> external content, or a genuinely complementary model) — **not** from a cleverer **usage pattern** over the
> same model (roles, prompts, multi-agent, routing), because those are *read-out* and are capped by the
> model's own oracle ceiling (`TfrlProofs.InfoBoundary`; measured in E10/E10b).

## 1. Where this came from
The owner framed a general judgment: once a model is capable enough to *do work*, three deficits remain,
each compensated by an agentic component — **① capability** (skills: standardize + extend the capability
boundary via a harness / standardized declarations / API calls), **② knowledge** (reconcile inconsistency
& conflict across models → a unified knowledge spine), **③ memory** (softly supplement task ability the
model lacks; = the Q1b direction, [[2026-07-05-Q1-conclusion-corrected]]). The question: *what blind spots
remain, and is an omni agentic system worth building?*

My first answer proposed four more "missing pieces" (perception, planning/control, verification,
real-time/duplex). The owner correctly cut it down: **those aren't new *elements* — they are new *usage
patterns* of the existing elements** (a role = a model, or the same model under a different system/user
prompt, plus skills/memory/knowledge connectors). That cut, pushed through four rounds, produced the
taxonomy below — and it lands exactly on our own read-out/new-info theorem.

## 2. The three axes
| Axis | What it is | Members | Can it add information to a frozen model? |
|---|---|---|---|
| **① Elements** (≈ a closed set; the only new-info carriers) | the atomic building blocks | model(s) · system/user prompt · **connectors**: {skills/tools, knowledge, memory} | **Yes** — a connector that brings in a tool result / external fact / stored content, or a *different* model, carries information the frozen model's distribution lacks. Owner's ①②③ = the three connector-type elements. |
| **② Usage patterns** | how elements are wielded | roles / orchestration / multi-agent / routing (planning, verification-as-role) | **No** (over one frozen model) — recombining the *same* model under new prompts/roles is **read-out**: its output is still one of the model's own samples. |
| **③ Constraints / qualities** | properties that bound the system | perception fidelity (a *model* quality) · real-time / full-duplex (a *substrate*/base-architecture property) · alignment/safety (cross-cutting) | **No** — not elements; they bound or gate the system rather than supply new information. |

**Candidate "new element" to falsify:** a *live environment/state connector* (present-world state, e.g. the
tau2 DB-state) looks distinct from static knowledge and past memory — but it is delivered **through a tool
call**, so it likely folds back into the skills/tools element. "**The element set is closed**" is itself a
strong, falsifiable claim the survey should try to break.

## 3. Why usage patterns can't cross the boundary (theorem + measurement)
`TfrlProofs.InfoBoundary` (sorry-free): any selector that returns one of the model's own N samples is
correct only if some sample is correct (`readout_acc_le_oracle`), so its ceiling is oracle@N, and the
**capability/knowledge gap** (no correct sample) is an **irreducible floor** for the whole class
(`readout_error_ge_gap`). A usage pattern over a single frozen model — a planner role, a critic/verifier
role, an N-agent debate of one model — is exactly such a selector. **E10/E10b measured it**: the two-system
verifier (same weights + a critic system-prompt) never beats plain majority (CIs cross 0). Only a lever
that *changes the sampling distribution* via a new element can be correct where every base sample misses
(`newinfo_can_cross_gap`). ⇒ **Axis ② is read-out-bounded; the leverage is in Axis ①.** T5
([[2026-07-05-t5-headroom-composition]]) sizes the floor: up to ~43% on knowledge-QA.

**Verification forks** — a telling special case. **Verification-as-role** (same model + a "critic" prompt)
is Axis ② (weak; E10 refuted it). **Verification-as-tool** (an external checker / code executor / a
genuinely verifiable reward) is an Axis ① element (new-info: it computes correctness the model can't).

### 3b. Second-pass refinement (D1 survey verification, 2026-07-06)
The survey's three verification passes (adversarial + positive-search + citation; `2026-07-06-synthesis` §8)
sharpened two claims — the thesis holds, stated more precisely:
- **The oracle-reading, stated precisely (NOT "usage patterns are useless").** A usage pattern **can** raise
  the *deployed (greedy)* score up toward the model's own **oracle@N** — self-consistency / CoT do this on
  MMAU (2503.23395: +9–150% training-free on frozen ALMs) — but it **cannot exceed** that oracle. The thesis
  is about the **ceiling** (crossing the capability/knowledge boundary), not whether prompting ever helps.
  This is exactly `readout_acc_le_oracle` (bound), with greedy ≤ oracle the achievable room. Consequently
  "empty cell" claims must be scoped: training-free best-of-N is **occupied** on audio-understanding QA
  (MMAU), and **empty only on interactive voice-agent verifiable tasks** (τ²-voice / EVA-Bench) — the actual
  GAP-1.
- **A FOURTH lever family the taxonomy must name: inference-computation edits.** Decoding-algorithm /
  forward-pass restructuring — **EGLR** (Entropy-Gated Latent Recursion, 2606.16620: +8.2pp oracle expansion,
  info-free) and contrastive decoding — is training-free, single-model, info-clean, yet changes the model's
  own **output distribution** (not just its prompt). It is **neither** an element (no new info) **nor** a
  usage-pattern (not a role/prompt). It changes inference **structure/computation**, so it is **excluded by
  our "no weight AND no structure change" frozen contract** (Project-Thesis) — but it is the most plausible
  site of an *info-free* ceiling-expansion, so "the element set is closed" is narrowed to **"closed among
  prompt/orchestration usage patterns over a fixed inference computation."** (The `InfoBoundary` /
  `AgenticElements` theorems bound Axis-② selection over a *fixed* distribution; Axis-④ decoding-edits change
  the distribution and are out of their scope by construction — correctly, and out of our contract too.)

## 4. Pruning the frontier (owner's two challenges)
Two owner challenges carved out what our research can *own*:

- **The controller need not be multimodal.** Planning/control operates over symbols (task, tool specs,
  intermediate results), so it can be a **text LLM API** (e.g. DeepSeek V4 Pro). ⇒ control/orchestration is
  **commodity** — not our omni research point; and when that controller is a *separate, stronger* model it
  is itself a **new-info element** (complementary reasoning), consistent with the theorem. **But the M3
  lesson bites:** if the omni only feeds a **transcript** to the text LLM, that is ASR→text-LLM — the audio
  is thrown away and the omni is pointless. So the omni's legitimate role is to expose **more than a
  transcript**.
- **The omni is not a full-duplex base, and we won't change the base.** Current omni models (incl.
  Qwen3-Omni) are **turn-based / half-duplex**; true full-duplex needs a purpose-built dual-stream base
  (Moshi-style). Making the frozen omni full-duplex = changing the base = violating the training-free / no-
  weights / no-structure thesis. ⇒ **full-duplex / real-time is out of research scope** (survey landscape
  only, tagged "requires base change"); the system operates turn-based; intra-turn latency is an inference-
  engine matter.

**Three new-info sources, cleanly divided.** A text-LLM controller adds **reasoning + world knowledge**
(but bounded by the transcript — it can't un-mishear); the **omni** adds **perception** (> transcript);
**memory/knowledge connectors** add **external stored knowledge**. Complementary and orthogonal.

## 5. Our research frontier (what's left after pruning)
Only two **omni-specific new-info elements**:
1. **The omni as a rich perception element** — training-free activation so it exposes the **">transcript
   delta"** (paralinguistic/semantic content ASR can't) to whatever controller consumes it. *This promotes
   the M3 lesson to the core research question: what is that delta, and is it load-bearing (does the system
   beat ASR→text-LLM)?*
2. **Audio-understanding-keyed memory / knowledge connectors** — the Q1b direction
   ([[2026-07-05-omni-multimodal-memory-design]]).

Everything else — control (commodity text LLM), full-duplex (frozen-base-forbidden), verification-as-role
(read-out) — we **consume or exclude**, we do not research. W4 stays a **read-out** lever that supplies the
memory's retrieval *key* ([[2026-07-05-W4-value-reassessment]]).

## 6. The open architectural fork (survey decides, T9 resolves)
- **A — omni-as-sensor + text-LLM-brain:** omni exposes the >transcript delta to a strong text-LLM
  controller; research = the delta + audio-keyed memory.
- **B — omni-as-brain (end-to-end):** no external controller; research = training-free activation of the
  frozen omni's own reasoning/knowledge/orchestration. Closest to the original project thesis.
- **C — layered hybrid, task-routed.**

Owner (2026-07-06): **do not pre-lock.** The D1 survey classifies every 2025+ system as omni-sensor vs
omni-brain vs hybrid, maps construction + failure modes of each class, and the architecture decision is a
first-class item for the **T9** owner checkpoint.

## 7. The falsifiable claim the survey must test
> **Is there any 2025+ multimodal/speech agent system that crossed a capability boundary purely via a
> *usage pattern* over one frozen model — or does every crossing, without exception, introduce a new-info
> element?** If the former exists, the thesis is wrong; if not, it is corroborated (and "the element set is
> closed" gains support).

## 8. Fence status (2026-07-03 closure — amended)
The owner amended the 2026-07-03 NO-GO closure (Decision-Log 2026-07-06) via its own §9 owner-amendment
path, re-opening the full agentic system incl. cross-session accumulation. The survey therefore covers
cross-session systems, but every candidate problem (D4) is still tagged **single-session vs cross-session**;
the amendment entry is the coverage of record.

## Anchors
- Theory: `proofs/tfrl/TfrlProofs/InfoBoundary.lean`, `BlindSpot.lean` · [[Theory-Convergence-and-Constraints]]
- Measurement: [[2026-07-05-Q1-conclusion-corrected]] (E10/E10b, T2/T3), [[2026-07-05-t5-headroom-composition]]
- Prior agentic surveys (extend, don't re-derive): `wiki/survey/2026-06-30-agent-level-synthesis.md` (S1),
  `wiki/survey/2026-06-30-agent-memory-skills-design.md` (S2), `wiki/survey/2026-07-04-stage1-L4-speech-agentic.md` (L4 P1–P5)
- Guard: [[Information-Boundary-Guard]] · Fence: `wiki/2026-07-03-omni-agentic-tfrl-go-no-go-decision.md` + Decision-Log 2026-07-06
