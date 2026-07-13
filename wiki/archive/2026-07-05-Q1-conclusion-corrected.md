---
title: "Q1 conclusion (CORRECTED, boundary-clean): is ICL sufficient for training-free RL on a frozen omni model, and should we design an omni agentic system?"
date: 2026-07-05
stage: 1-directional
status: "ACTIVE — supersedes the 2026-07-04 conclusion (whose M3-based Q1b lock was RETRACTED as an information-boundary violation). Terminal Stage-1 gate = owner checkpoint (T9); NOT an auto-rollover to Stage 2."
supersedes: 2026-07-04-Q1-conclusion-ICL-sufficiency-omni.md (Q1a stands; the M3/Q1b lock is withdrawn)
---

# Q1 — corrected conclusion

> **Reading rule.** Every in-house number here is **Stage-1 directional** (small-n, single-model
> [Qwen3-Omni-30B via llama.cpp], single-touch) — it *illustrates* the argument, it does not *settle* it
> (CLAUDE.md: small-n "can settle nothing"). The load-bearing content is the **argument + theory**; the
> numbers are consistent with it. Every lever cited passes the [[Information-Boundary-Guard]] (no use of the
> test item's golden transcript/answer; deployable at inference). The prior conclusion's Q1b lock was built
> on **M3 (golden-transcript injection)**, which the owner correctly identified as a boundary violation and
> which is **retracted**; this document rebuilds Q1b on legitimate ground.

## Q1a — Is in-context learning / instruct-prompt optimization sufficient? **NO (directional, well-argued).**

ICL and prompt-space levers are all members of one class — they **read out** the frozen model's own
distribution without adding information. We tested **four** legitimate read-out levers (few-shot,
candidate-pick prompt-opt, iterative prompt-opt, two-system verification) and **none** reaches the
headroom:

| Legitimate read-out lever | Result (boundary-clean) | Source |
|---|---|---|
| Proper **task-definition few-shot** (audio + text how-to-handle + reasoned demos from *train*, test audio-only) | **never beats plain** greedy (mmau −0.075 n.s.; vocalbench −0.175 SIG−; SQuAD +0.000 n.s.). Demos carry genuine task-signal (C−b1 SQuAD +0.10 SIG+) but the multimodal few-shot format cost cancels it. | T2 `_repro/t2_taskdef_fewshot.json` |
| **Global prompt optimization** (OPRO/GEPA-style dev-set pick + transfer, text-only) | no deployable gain | E8 |
| **Two context-differentiated systems** (frozen omni as generator + verifier via context isolation) — the "omni-as-reward" idea, done legitimately | verifier **never beats majority**; CIs cross 0 | E10 + E10b control |

**The remaining read-out levers, for completeness.**
- **Iterative feedback-driven prompt optimization** (T3, APE/OPRO/TextGrad-style: offline dev-set
  refinement over R rounds, frozen test eval, text-only, no leakage) — the last *prompt-space* lever
  distinct from E8's candidate-pick and T2's few-shot. **No gain on any surface** (mmau +0.000 CI[0,0];
  vocalbench −0.050 CI[−0.125,0]; SQuAD-zh −0.050 CI[−0.2,0.1] — all n.s.). The refinement either
  breaks output format (mmau: dev 0.40→0.00) or overfits dev and transfers negatively (vocalbench/SQuAD),
  so the dev-best instruction never beats base on test. `_repro/t3_iterative_promptopt.json`.
- **Verifiable-reward best-of-N** (T4) — resolved by argument, not a new run, and the argument is itself a
  Stage-1 finding: a *deployable* verifiable reward (correct without the golden label) exists only for
  **rule-checkable** outputs (math re-computation, code execution, format/constraint satisfaction). The
  semantic-QA/MCQ surfaces here are **not** rule-checkable — correctness needs the label — so the only
  deployable signal available is **consistency/confidence**, and the consistency selector was already
  tested (E10b majority self-selection: never beats greedy). Hence verifiable-reward best-of-N is *inapplicable*
  to open semantic QA and *redundant* with E10b where it is applicable; it becomes a real instrument only if
  a rule-checkable audio sub-task (spoken math/code) is added — a Stage-2 scoping question, not a Q1a gap.

**Why read-out is capped — theory + data.** T8 (`TfrlProofs.InfoBoundary`, sorry-free) proves any read-out
selector is correct only if one of the model's own samples is correct (`readout_acc_le_oracle`), so its
ceiling is oracle@N; and the **capability/knowledge gap** — items with *no* correct sample in N tries — is
an **irreducible error floor** for the entire read-out class (`readout_error_ge_gap`). T5
[[2026-07-05-t5-headroom-composition]] measures that floor on the model's own samples: it is large exactly
where knowledge is needed — **42.7% on vocalbench-zh knowledge-QA**. So even a *perfect* deployable read-out
selector would leave ~43% of knowledge-QA unanswerable. **ICL/read-out is structurally insufficient**, and
the failure is not "we didn't optimize the prompt hard enough" — it is that the answer is not in the model's
distribution to be read out.

## Q1b — Should we design an omni agentic system? **YES — but specifically a multimodal external-knowledge MEMORY, not self-reward or transcript injection.**

The corrected argument has three legs:

1. **There is a real, large target that read-out provably cannot reach** — the capability/knowledge gap
   (T5: up to 42.7%). This is not a decoding problem; it is a knowledge-boundary problem.
2. **Only a new-information lever can cross it** — T8 `newinfo_can_cross_gap`: a lever that changes the
   *sampling distribution* by conditioning on external evidence can be correct where every base sample
   misses; the read-out ceiling is class-dependent, not absolute. So crossing the gap **requires** leaving
   the ICL/read-out class and adding new information.
3. **The legitimate form of that lever is an external multimodal memory** (design:
   [[2026-07-05-omni-multimodal-memory-design]]) — key = a unified **compressed** speech embedding; value =
   a dict `{(task, language) → external-knowledge text}`; three RL-optimizable strategies (compression /
   retrieval / usage). It is **not** self-reward (E10 refuted that), **not** golden-transcript injection (M3,
   retracted — a boundary violation), and **not** a cross-session accumulating agent (the 2026-07-03 closure
   fence). It supplies information the frozen model lacks, keyed by the deployable query representation.

**Scope of the "yes".** This is a **conditional, mechanism-specified yes**, correctly graded: the argument
(1)+(2) is theorem-backed and boundary-clean; the *empirical* claim that a **training-free** memory realizes
the gap is a directional probe, not yet established. First feasibility data point (T6 Step 1 — can one
unified **compressed** speech key support task-relevant retrieval? owner's "先探索统一编码的可行性"):

> **T6 Step 1 result (Stage-1 directional; `_repro/t6_compression_feasibility.json`).** Key = the model's
> own short content-summary of the audio (deployable, index-only — not injected, not the golden transcript),
> embedded (TF-IDF char-ngram; the neural multilingual embedder failed to load offline — a noted limitation).
> On minds14-zh intents: within-task retrieval **precision@5 = 0.62 vs chance 0.08 vs random-key floor 0.10
> (lift +0.54)** — the compression preserves task-relevant structure. **Unified index** (minds14 pooled with
> SQuAD-zh): task-purity **1.0** (queries retrieve only same-task neighbors) and unified-vs-per-task
> precision delta **0.0** (pooling a second task does not degrade retrieval). → **A single unified compressed
> key is feasible** — the owner's preferred path holds; no need to fall back to per-task encoding yet.
> Caveat: the TF-IDF proxy rewards lexical overlap, and two very dissimilar tasks separate easily; a neural
> embedder and nearer tasks are the Step-1.1 hardening. This tests the **key** only — retrieval/usage
> strategies and the knowledge-gap payoff are Steps 2–3.

**What Q1b is NOT.** It is not a licence to build the full agentic system now (that is Stage-2 work behind
the owner checkpoint), and it does not resurrect the read-out levers Q1a closed. W4's flagship
disentanglement is itself a **read-out** lever ([[2026-07-05-W4-value-reassessment]]): it improves the
memory's retrieval *key* but cannot supply the missing knowledge — memory and W4 compose, they don't
substitute.

## How others realize frozen-model headroom without leakage (archive-grounded; full survey is owner-gated)
Consistent with the corrected verdict, and positioning the memory direction against prior art (the full
lane-by-lane survey battle D4/D5 is deliberately **gated behind the owner checkpoint K1/T9** for its compute
cost — this is the light grounding):
- **Prompt/ICL levers plateau on accuracy** — ALICE-style demos fix *format* not accuracy; VoxParadox shows
  ICL reads the *text* channel, not the acoustics. Matches E8/T2 (prompt-space gains cancel).
- **Support-set / new-info expansion works — but so far only in adjacent settings.** ProGRes (prompt-based
  rescoring / new-hypothesis generation, 5–25% rel WER) and RECOVER (entity correction, 8–46%) *add*
  information and *do* move the ceiling — but they are **text-LLM-over-ASR**, not the omni model expanding
  its **own** support. "A frozen omni + external multimodal memory expanding its own rollout support" is an
  **unoccupied cell** — which is why Q1b points there.
- **Label-free selection is weak** — the one external positive (frozen-LM MBR ~9% rel) is small and needs a
  reward channel; on our surfaces no deployable verifiable reward exists (the T4 argument).
- **Paralinguistic recovery on a frozen model is all weight-changing** (VoxParadox DPO/LoRA) — no
  training-free demonstration exists; consistent with W4 being read-out, not a knowledge source (#37).

Net: the literature agrees read-out plateaus and that *new information* moves the ceiling; the specific,
un-taken step is a **training-free multimodal memory that expands a frozen omni's own rollout support** —
exactly the Q1b candidate, and exactly what needs Stage-2 validation.

## Verdict
- **Q1a: ICL/instruct-prompt optimization is insufficient** for training-free RL on the frozen omni
  semantic layer (directional; **four** legitimate read-out levers fail; the read-out ceiling is a proven
  wall; the knowledge gap that defeats it is measured at up to ~43%).
- **Q1b: yes, a beyond-ICL system is warranted, and it must be a new-information lever — a multimodal
  external-knowledge memory** — because that is the *only* class that can cross the knowledge gap (T8), and
  because that gap is real and large (T5). The training-free realizability of that memory is the next
  directional probe (T6), and the go/no-go on *building* it is the **owner's Stage-1 checkpoint (T9)** — this
  document does not auto-advance to Stage 2.

## Evidence ledger (all Stage-1 directional; all boundary-clean)
- T2 few-shot: `_repro/t2_taskdef_fewshot.json` · E8 prompt-opt · E10/E10b two-system: `_repro/`
- T5 decomposition: [[2026-07-05-t5-headroom-composition]] (from P2 `_repro/p2_baselines.json`)
- T8 theory: `proofs/tfrl/TfrlProofs/InfoBoundary.lean` (sorry-free) + `BlindSpot.lean` (convergence)
- Guard + rubric: [[Information-Boundary-Guard]] · [[2026-07-05-task-definition-rubric]]
- Memory design: [[2026-07-05-omni-multimodal-memory-design]] · W4 re-grade: [[2026-07-05-W4-value-reassessment]]
- Retraction of the prior lock: [[2026-07-05-A-realization-conclusion]] (banner) + Decision-Log RETRACTION note
