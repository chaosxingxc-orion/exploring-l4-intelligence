---
title: "Research proposal: interleaved perception, reasoning, and revision for long-context speech"
date: "2026-08-16"
status: "DRAFT_FOR_OWNER_REVIEW__NO_NEW_EXECUTION_AUTHORITY"
research_horizon: "within one long speech item"
program_fit: "TF-Strict external control over a frozen speech-capable omni core"
literature_cutoff: "2026-08-16"
shared_standard: "docs/superpowers/specs/2026-08-16-black-box-agent-harness-and-experiment-standard.md"
---

# Interleaved Perception, Reasoning, and Revision for Long-Context Speech

## 0. Decision in one page

This is the most execution-ready of the three topics, but the phrase **"listening, spelling, and revising"** is
too ASR-centric and underspecifies the research contribution. Chunked transcription, streaming ASR,
multi-pass correction, and long-context aggregation are established areas. Merely asking an omni model to read
successive chunks and rewrite a transcript would be an engineering recipe, not a defensible research object.

The surviving topic is:

> Can a training-free external controller improve a frozen speech-omni model on long-form spoken tasks by
> interleaving selective audio observation, provisional semantic state, source-grounded revision, and bounded
> compaction—under equal inference budgets and with state reset for every item?

"Spelling" remains one action for entity-sensitive transcription, but it is not the title or the primary
outcome. The controller must improve final task utility on long-context spoken QA, instruction following, or
meeting understanding, with ASR and entity fidelity used as mechanism diagnostics.

Recommended portfolio status: **advance first, subject to owner routing and a frozen multi-task carrier.** It
has the clearest local failure evidence and reuses the program's frozen-core runtime, but it must not alter the
live study repository or begin model contact under this proposal alone.

This proposal inherits the shared black-box harness, baseline-availability, model-selection, phased-evidence,
and replay requirements in `2026-08-16-black-box-agent-harness-and-experiment-standard.md`. Where this proposal
is less strict, the shared standard controls. The controller may search for the task ceiling during development,
but only the later consolidated, matched-budget experiment can support a causal policy claim.

## 1. Why the original formulation fails

### 1.1 Chunking is not a contribution

Streaming ASR, RNN-T-style temporal emission, sliding windows, simultaneous translation, multi-pass error
correction, recurrent compression, and long-audio caption aggregation already cover much of the apparent method.
The proposal must isolate an external **decision policy** that selects when and where to observe, revise,
compress, or stop.

### 1.2 Long context is not automatically useful

Long-context audio models degrade with input length and incur attention/KV-cache costs. Recent hour-scale
evidence finds no universally dominant inference paradigm: native end-to-end processing, cascaded aggregation,
and external reasoning each win in different regimes. "Use the omni model's long context" is therefore an
assumption to test, not a solution.

### 1.3 Revision can destroy correct content

Repeated rewriting may hallucinate entities, erase rare words, break timestamps, and amplify an early wrong
hypothesis. A revision is scientifically meaningful only when it is localized, source-aligned, and evaluated
for both wrong-to-correct and correct-to-wrong transitions.

### 1.4 More calls and more audio are confounds

An agent that rereads audio and receives a larger prompt will often improve. The method must beat fixed-window,
whole-context, and two-pass baselines at equal calls, tokens, processed-audio seconds, and declared lookahead.

### 1.5 ASR-only success is too small

The program has already learned that legal small entity rosters can improve ASR. The new topic earns research
value only if interleaving improves a harder semantic task or establishes a general control principle across at
least two long-form task types.

### 1.6 Current program evidence

The admitted study's existing readiness analysis reports a concrete failure signature: the current long-form
path removed 10,693 excess words, 86% of the removed words were deletions, and 1,648 seconds of source speech
were skipped. It also measured a prompt-length cost: approximately 4,700 prompt tokens reduced decoding to
3.07–4.40 tokens/s versus 13.07 tokens/s at 816 prompt tokens. These observations are documented in the study's
[interleaved listening and spelling readiness note](../../../studies/speech-aware-evidence-acquisition/docs/readiness/2026-08-10-interleaved-listening-and-spelling.md).

This is strong motivation for observation scheduling and bounded state, but it is not evidence that the proposed
controller works. The same receipts could support a simpler fixed-window repair. The proposal therefore treats
deletion share, skipped time, and prompt slowdown as failure diagnostics and requires a semantic task plus
equal-exposure baselines before claiming a new method.

## 2. Scope and portfolio boundary

### 2.1 Unit of state

State begins when one long spoken item starts and is destroyed when that item ends. It may include a draft,
semantic ledger, source map, unresolved questions, and compressed history. Nothing learned from item `i` may
enter item `i+1`.

### 2.2 In scope

- Frozen API-only speech/omni core with repeated calls controlled externally.
- Long-form speech transcription, entity fidelity, spoken QA, instruction following, and meeting understanding.
- Adaptive audio windows, left context, declared right lookahead, re-observation, local revision, compaction,
  and stopping.
- Explicit source alignment and reversible edits.
- Offline or latency-relaxed evaluation; wall-clock cost remains measured.

### 2.3 Out of scope

- Cross-episode memory or continual knowledge evolution.
- Parameter training, hidden-state reuse, learned audio compression, or architecture modification.
- Claims of native streaming or native recurrent state inside the omni model.
- Live dialogue, simultaneous listening/speaking, barge-in, echo cancellation, or real-time turn-taking.
- General environmental audio and music; speech-only subsets are required.

### 2.4 Non-overlap contract

This proposal may use right lookahead and revise earlier text after later audio arrives. The full-duplex proposal
may do neither: it is causal and real-time. This proposal resets state per item; the continual-knowledge proposal
persists state across episodes. Shared telemetry and model adapters are infrastructure, not shared scientific
claims.

## 3. Research questions and hypotheses

### RQ1 — Does adaptive interleaving beat fixed inference schedules?

**H1.** Under matched model calls, prompt/output tokens, and processed-audio seconds, an adaptive controller over
`LISTEN`, `DRAFT`, `VERIFY`, `REVISE`, `COMPRESS`, and `STOP` improves final long-form task performance over
whole-audio, fixed-window, sliding-context, and two-pass baselines.

**Null H1.** Any improvement is explained by extra audio exposure, longer prompts, or more calls.

### RQ2 — Does revision improve semantic utility rather than only transcript form?

**H2.** Source-grounded local revision improves spoken QA/instruction/meeting outcomes while reducing deletion
and entity errors, with a bounded correct-to-wrong rate.

**Null H2.** Transcript changes do not improve downstream task scores or trade rare-word corrections for semantic
regressions.

### RQ3 — What state should survive long contexts?

**H3.** A structured compact state—verbatim tail, entity ledger, event/claim ledger, unresolved obligations, and
source pointers—beats an equal-token verbatim tail or free-form summary on long-range retrieval and sparse-event
reasoning.

**Null H3.** Long-context attention over the verbatim history is sufficient, or compaction loses the very evidence
needed later.

### RQ4 — Can the controller allocate observation where it matters?

**H4.** Reward-guided re-observation concentrates calls and audio seconds around uncertain, entity-bearing, or
task-relevant spans and improves unit gain per call relative to uniform overlap.

**Null H4.** The agent's uncertainty and span choices are uncalibrated; uniform or oracle-independent schedules
perform as well.

## 4. Control formulation

### 4.1 State

At step `t`, the external state is:

```text
S_t = {
  audio_frontier,
  observation_windows[],
  source_aligned_draft,
  entity_ledger,
  event_and_claim_ledger,
  unresolved_obligations,
  task_hypothesis,
  revision_history,
  budget_state
}
```

Every draft span links to one or more audio intervals and carries status `PROVISIONAL`, `SUPPORTED`,
`CONTESTED`, or `RETIRED`. A compacted fact must retain source pointers; compaction without provenance is not
eligible for later verification.

### 4.2 Actions

- `LISTEN(start, end, left_context, right_lookahead)` acquires a bounded audio view.
- `DRAFT(span, content, support)` adds provisional text or semantic structure.
- `VERIFY(target, evidence_window)` requests focused re-observation or consistency checking.
- `REVISE(target, replacement, cited_evidence)` applies a reversible patch rather than rewriting the full state.
- `COMPRESS(region, schema)` replaces state with a structured representation and source map.
- `STOP(reason)` commits the final answer when expected improvement no longer justifies cost.

The action schedule may be model-proposed but is constrained by deterministic audio, token, call, and lookahead
budgets. The controller never receives hidden states or attention maps.

### 4.3 Reward vector

Report a vector before any scalarization:

```text
[final_task_score,
 entity_or_transcript_score,
 wrong_to_correct,
 correct_to_wrong,
 grounded_edit_precision,
 processed_audio_seconds,
 model_calls,
 tokens,
 latency]
```

If a scalar control reward is required, freeze it before the confirmatory run and show sensitivity to reasonable
weights. No single learned or model-judged reward may silently define success.

## 5. Latest academic landscape and remaining gap

| Work | What it establishes | Consequence for this proposal |
|---|---|---|
| [Speech ReaLLM, 2024](https://arxiv.org/abs/2406.09569) | A trained decoder-only architecture can emit continuously without explicit endpointing by modeling time. | This proposal cannot claim native streaming; its novelty must be external control of a frozen model. |
| [Qwen2.5-Omni Technical Report, 2025](https://arxiv.org/abs/2503.20215) | Block-wise encoders, time-aligned multimodal positions, and a Thinker–Talker design enable streaming input/output. | Internal blockwise recurrence is trained architecture, not available to a black-box controller. |
| [Qwen3-Omni Technical Report, 2025](https://arxiv.org/abs/2509.17765) | A released omni model combines audio perception, multimodal reasoning, and streaming speech generation. | Provides the frozen core and long-context capability, but not evidence that repeated external revision helps. |
| [SimulS2S-LLM, ACL 2025](https://aclanthology.org/2025.acl-long.817/) | A test-time policy can unlock simultaneous inference for a trained speech LLM and improve quality–latency trade-offs. | Test-time scheduling is occupied; our difference is multi-action revision/compaction on long tasks with a frozen API core. |
| [AudioMarathon, 2025](https://arxiv.org/abs/2510.07293) | Long-audio performance drops from 90–300 seconds; token pruning and KV eviction introduce efficiency trade-offs. | Length and efficiency are primary experimental axes, not afterthoughts. |
| [VoiceGiraffe, 2026](https://arxiv.org/abs/2605.27976) | Hour-scale audio remains unsolved; no single E2E/cascaded paradigm dominates; sparse-event persistence is a bottleneck. | Compare whole-context, aggregation, and external-reasoning baselines; target sparse-event tracking. |
| [Multilingual Long-Form Speech Instruction Following, IWSLT 2026](https://aclanthology.org/2026.iwslt-1.16/) | Segmented candidates can be preferred by ASR likelihood yet degrade semantic tasks; MBR can correct that failure. | ASR quality is not a safe proxy for semantic task quality; final-task evaluation is mandatory. |
| [MISP-Meeting, ACL 2025](https://aclanthology.org/2025.acl-long.753/) | Real long-form meetings require transcription and summarization under far-field and multimodal conditions. | Offers a realistic task family, but only the speech-aligned and legally admissible subset fits the program boundary. |
| [LCIRC, NAACL 2025](https://aclanthology.org/2025.naacl-long.524/) | Recurrent, query-dependent compression can extend text context efficiently. | Compression is occupied at the learned text-model level; our claim must concern external, source-grounded audio-task state. |

**Gap inference.** The cited work covers trained temporal architectures, simultaneous decoding, long-audio
benchmarks, recurrent text compression, and long-form instruction following. It does not establish a
training-free, source-grounded controller that chooses when to listen, revise, and compact a frozen speech-omni
model and is evaluated under equal exposure on both transcription mechanisms and final long-form semantic
tasks. Stage 1 must still perform citation-neighbor and code-level checks before any novelty language is used.

## 6. Task and dataset ladder

### L0 — deterministic edit and compaction tests

- Synthetic audio timelines represented by fixed mock observations.
- Seed entity corrections, delayed disambiguation, contradictions, sparse events, and compaction loss.
- Prove source maps, patch reversibility, lookahead enforcement, and budget accounting without model contact.

### L1 — long-form transcription and entity fidelity

- Use frozen, already governed long-form speech carriers where legally and experimentally appropriate.
- Primary role: diagnose deletions, skipped time, rare entities, boundary artifacts, and revision behavior.
- This is a mechanism rung, not the paper's final value claim.

### L2 — long-context spoken QA

- Candidate: speech-only, legally available slices of VoiceGiraffe or a long-form spoken-QA carrier.
- Construct length and evidence-position strata; reserve sparse-event and multi-hop questions.
- Require direct audio availability and auditable answer labels. Do not create audio by concatenating test items
  unless the experiment is explicitly labeled synthetic.

### L3 — long-form instruction following or meeting understanding

- Candidates: IWSLT 2026 long-form instruction-following data and a legally frozen speech-aligned meeting task.
- Use at least two semantic outputs, such as QA plus structured event/entity extraction or instruction following.
- Avoid broad summarization scores as the sole primary metric; include factuality and source-support checks.

The first Stage-2 slice should use L1 plus one L2/L3 carrier. A positive ASR-only result is insufficient for
promotion.

## 7. Baselines and controlled variants

| ID | Method | Role |
|---|---|---|
| B0 | Whole-audio single call | Native long-context baseline where legal and feasible. |
| B1 | Non-overlapping fixed chunks + concatenation | Lowest-complexity chunk baseline. |
| B2 | Fixed overlap + text carry | Strong conventional long-form baseline. |
| B3 | Sliding verbatim tail at fixed token budget | Tests long local context without structured state. |
| B4 | Two-pass transcription then LLM correction/answer | Separates multi-pass benefit from adaptive control. |
| B5 | Chunk captions/transcripts + one final reasoning call | Cascaded aggregation baseline. |
| B6 | Oracle schedule or oracle relevant spans | Bounds observation allocation. |
| B7 | Proposed interleaved controller | Full method. |

Required ablations: fixed versus adaptive windows; no revision; full rewrite versus local patches; no source
map; free-form summary versus structured compaction; entity-only versus task-ledger compaction; no right
lookahead; fixed versus adaptive stopping; equalized tokens; equalized processed-audio seconds; equalized calls.

### 7.1 Availability and comparability verdict

The load-bearing first suite is native R0: whole-audio single call, fixed non-overlapping chunks, fixed overlap,
sliding verbatim tail, two-pass correction/answer, and transcript-or-caption aggregation. These controls can use
one model adapter, one audio-interval ledger, and one verifier, so failures are attributable rather than hidden
inside different research codebases.

AU-Harness is the preferred external task-adapter source because its official Apache-2.0 implementation spans
long-form ASR, intent classification, speech QA, instruction following, speech function calling, speech-to-SQL,
and other audio-to-text tasks. It remains R2 for this program until the exact speech-only subsets, endpoint
adapter, deterministic metrics, model-specific prompts, and any judge dependency pass a local receipt.
AudioMarathon is also R2: official code exists, but model-specific environments and its broad general-audio
coverage require repair and boundary filtering. LibriSpeech-Long is an R1 candidate for long-form diagnostic
audio, but it cannot carry the main claim because it is transcription-centric. VoiceGiraffe remains R3 at this
literature cutoff because its paper-linked repository was unavailable. SimulS2S-LLM and unreleased long-form
instruction datasets are architectural or carrier references, not load-bearing baselines.

## 8. Evaluation design

### 8.1 Primary outcome

Choose one task-grounded metric per frozen carrier before execution: exact/semantic QA accuracy, structured
event/slot F1, instruction compliance, or fact-grounded meeting score. Report transcript WER/CER and entity
metrics as mechanisms, not as the only success criterion.

### 8.2 Revision metrics

- Wrong-to-correct and correct-to-wrong edits.
- Grounded edit precision: fraction of edits supported by newly cited audio evidence.
- Grounded edit recall on seeded delayed-evidence cases.
- Edit locality, source-map coverage, and timestamp drift.
- Deletion/insertion/substitution shares, rare-entity recall, and skipped-audio seconds.
- Oscillation count and rollback success.

### 8.3 Long-context diagnostics

- Accuracy by audio length, evidence position, evidence sparsity, and hop count.
- State survival: retention of entities, events, obligations, and contradictions after each compaction.
- Lost-in-the-middle and delayed-disambiguation panels.
- Compaction ratio versus semantic retention.

### 8.4 Efficiency and statistics

- Calls, input/output/audio tokens where available, processed-audio seconds, overlap factor, prompt length,
  first and total latency, real-time factor, GPU/CPU, and wall time.
- Paired bootstrap intervals over items and hierarchical analysis over dataset, length, and condition.
- Report a Pareto frontier, not a single quality-minus-cost number.
- Freeze a primary equal-budget contrast: B7 versus the strongest of B0–B5.
- Re-run all methods under at least two prompt-budget regimes to expose context-cost dependence.

### 8.5 Evidence phases

Phase A seeks the best attainable development-set task performance, allowing adaptive observation, rereading,
and revision while logging calls, unique audio, processed audio, overlap, prompt growth, and latency. Phase B
freezes the smallest observation–patch–compaction policy that retains the gain. Phase C compares it with the
strongest B0–B5 schedule under matched model, calls, retry allowance, processed/unique audio, prompt envelope,
and output budget. Phase D runs Q4-versus-Q8 sensitivity and a preregistered different-family M1 endpoint. The
same interval ledger and task verifier must serve every cell.

## 9. Stage-1 exploration package

### E1 — prior-difference audit

- Map long-form ASR, multi-pass correction, simultaneous speech inference, long-audio QA, recurrent compression,
  and agentic audio-reasoning systems.
- Record which methods require training, hidden states, audio embeddings, token logits, or architecture changes.
- Search specifically for frozen black-box audio controllers with localized revision and source-aligned compaction.
- Exit: one exact prior-difference claim survives implementation-level comparison.

### E2 — carrier and task audit

- Verify release status, hashes, licenses, speech provenance, duration distribution, answer creation, and metrics.
- Confirm that any AudioMarathon/VoiceGiraffe use is limited to speech rather than music/environmental sound.
- Confirm that meeting QA has aligned audio rather than transcript-only labels.
- Exit: one long-form semantic carrier is executable and legal, with no synthetic/real provenance ambiguity.

### E3 — headroom and failure audit

- Use existing receipts to quantify whole-call deletion, skipped time, boundary error, prompt-length slowdown, and
  task-score decay with duration.
- Define clean-text and relevant-span oracles to separate observation failure from reasoning incapacity.
- Exit: a failure is large enough, controllable by inference policy, and relevant to a semantic outcome.

### E4 — edit-safety protocol

- Seed already-correct rare entities, delayed corrections, contradictory later evidence, and unsupported rewrite
  temptations.
- Freeze patch admission, source citation, rollback, and stop policies.
- Exit: deterministic tests reject unsupported or nonlocal revisions.

## 10. Engineering baseline

### 10.1 Components

1. **Audio interval service** — exact sample/time slicing, left context, right lookahead, and immutable window IDs.
2. **State ledger** — typed draft spans, entities, events, obligations, support status, and source pointers.
3. **Action scheduler** — constrained action schema, budgets, deterministic validation, and stopping.
4. **Patch engine** — localized, reversible revisions with before/after and evidence links.
5. **Compactor** — verbatim-tail, free-summary, and structured-state implementations behind one interface.
6. **Task adapters** — transcription, QA, structured extraction, and instruction-following contracts.
7. **Replay runner** — executes identical schedules and counterfactual actions across methods.
8. **Evaluator** — task, edit, context, reliability, and cost metrics.

### 10.2 Mandatory interfaces

```text
open_item(audio_id, task_contract) -> state_id
listen(state_id, interval, context_policy) -> Observation
propose_action(state_id, observation, budget) -> Action
apply_patch(state_id, patch, support) -> state_id | rejection
compact(state_id, region, representation, budget) -> state_id
finalize(state_id) -> TaskOutput
score(task_output, reference_contract) -> MetricVector
replay(item_id, action_schedule, method_config) -> RunTrace
```

### 10.3 Trace requirements

Every model call records prompt hash, model/runtime identity, audio interval hashes, state snapshot, action,
output, parser result, cost, latency, and parent call. Every final answer must be reconstructable from the trace.
The system must distinguish audio seconds newly processed from repeated/overlapped seconds.

### 10.4 Test gates

- No interval exceeds the audio frontier plus declared right lookahead.
- Applying and reversing a patch restores an identical state hash.
- Every supported span reaches an audio interval or explicitly marked textual instruction.
- Compaction never silently drops an unresolved obligation.
- All baselines obey identical call/token/audio budgets when the experiment says equal budget.
- Mock-model tests reproduce fixed action schedules exactly.

## 11. Work packages and decision gates

| WP | Deliverable | Gate |
|---|---|---|
| WP0 | Literature/prior-difference matrix and adversarial review | Research object survives chunking/multi-pass precedents. |
| WP1 | Long-form semantic carrier and legal/exposure contract | Direct audio, labels, license, and provenance pass. |
| WP2 | Offline state/patch/compaction/replay harness | Deterministic edit-safety tests pass. |
| WP3 | Whole, fixed-chunk, sliding-tail, and two-pass ceiling/frontier study | Strongest baseline, headroom, and discovery cost are frozen. |
| WP4 | Consolidated adaptive observation and stopping study | The smallest surviving policy passes the matched-exposure Phase-C comparison. |
| WP5 | Local revision and source-grounding study | H2 improves semantic outcomes with bounded regressions. |
| WP6 | Structured compaction and length scaling | H3 survives equal tokens and sparse-event panels. |
| WP7 | Cross-task replication and candidate decision | Effect holds on transcription mechanism plus one semantic task. |

## 12. Adversarial self-debate record

### Round 1 — strongest rejection

**Reject the topic.** It is chunked ASR plus self-correction. Streaming ASR and multi-pass correction already
exist; long prompts are slow; repeated rewriting will hallucinate; and any gain will come from more calls and
overlap. "Spelling" narrows the work back to entity ASR, whose research value the owner already questioned.

### Round 2 — decomposition attack

The topic overlaps continual memory through compaction and full-duplex interaction through incremental audio.
If the controller is unconstrained, it can always reread the full audio and win by compute. If it is constrained,
a fixed sliding window may be just as strong. Long-context reasoning can also be evaluated on transcripts,
making the omni audio path unnecessary.

### Round 3 — surviving revision

Reset state for every item; permit declared lookahead but no live interaction; match calls, tokens, and processed
audio; use local source-grounded patches instead of full rewrites; compare against whole-context, fixed chunk,
sliding tail, two-pass, and cascaded aggregation; require a final spoken semantic task in addition to ASR
diagnostics. The claim becomes adaptive observation–revision–compaction control, not chunking.

### Round 4 — reproducibility attack

The most attractive long-audio papers do not all provide runnable, model-neutral baselines. A public benchmark
may mix environmental sound with speech, require a separate environment per model, truncate audio differently,
or score with an LLM judge. A paper-linked repository may also be unavailable.

**Revision:** make the six simple native schedules R0 and load-bearing. Adopt AU-Harness task definitions only
through pinned speech-only adapters and deterministic metrics. Keep AudioMarathon R2 pending repair,
LibriSpeech-Long as a diagnostic carrier, and VoiceGiraffe or paper-only systems as R3 motivation until their
release receipts close.

### Round 5 — experimental-standardization attack

“Same audio” is ambiguous when one method rereads overlaps, skips silence, or revisits suspected entities. The
controller may also see later evidence before a baseline or preserve more text in state. Matching only call
count would not match information or compute.

**Revision:** ledger both unique and processed audio intervals, overlap factor, lookahead, prompt state, output
tokens, retries, and wall time. Run every schedule on identical items with explicit observation availability.
Keep the test split invisible to all edit and compaction decisions and count correct-to-wrong revisions as
first-class failures.

### Round 6 — model-selection attack

Long-audio behavior depends on the processor and runtime as much as the model card: truncation, context limits,
audio tokenization, and serving support may differ. Q4 and Q8 are not independent confirmations, and a model
chosen for unusually good long-context behavior after pilots would bias the result.

**Revision:** freeze the exact model, precision, processor, runtime, context limit, and interval encoding in the
run identity. Use Q4 as the operational discovery cell and Q8 only as sensitivity. Preselect M1 by required
audio/long-context capability and reproducibility before confirmatory results, then run the frozen policy
without retuning.

### Round 7 — harness-versus-compute attack

Adaptive schedules can always win if they inspect more audio or make more correction calls. Conversely, an
equal-budget gate imposed before the mechanism is known can kill the very behavior under study.

**Revision:** separate ceiling discovery from evidence of causality. First determine whether selective
observation and source-grounded repair can work at all, with cost logged. Then consolidate. Only afterward match
information and compute and compare frontiers across two budgets. Counterfactually replace adaptive choices
with fixed windows on the same recorded model responses wherever valid.

### Round 8 — surviving claim

The topic survives as within-item black-box control over what audio to observe, what local semantic state to
revise, what evidence to retain, and when to stop. It does not claim that chunking or self-correction is new.
Promotion requires semantic-task improvement, safe local edits, exact exposure accounting, and frozen-policy
transfer to a second model family; otherwise the result should narrow to whichever single mechanism survives.

### Residual risk after revision

The proposed controller may still collapse to a hand-designed window schedule, or the frozen model may be unable
to make reliable uncertainty and edit decisions. That negative result is valuable only if oracle schedules and
equal-budget baselines prove where the limitation lies.

## 13. Stop, revise, and promotion criteria

### Stop

- No legally executable long-form semantic speech carrier exists.
- Whole-audio or fixed sliding context matches the controller at equal budget.
- Gains require materially more processed audio, calls, or tokens.
- Revision improves WER but not task outcomes, or correct-to-wrong regressions erase the gain.
- Source-grounded compaction loses sparse evidence at the same rate as free summaries.
- Clean transcripts close nearly all headroom, showing that the remaining problem is core reasoning rather than
  inference-time speech control.

### Revise

- Observation allocation works but revision fails: study adaptive evidence acquisition only.
- Revision works but compaction fails: narrow to bounded-duration tasks and remove long-memory novelty.
- Only entity-sensitive tasks improve: state an entity-resolution claim and do not generalize to long reasoning.

### Eligible for Stage-2 owner decision

- A semantic long-form carrier, strong baselines, and a no-leak information boundary are frozen.
- At least one adaptive action beats its fixed counterpart at equal exposure.
- Final semantic task performance improves with bounded regression, not merely transcript form.
- Source maps and counterfactual schedules attribute the effect to interleaved control.
- A second task family reproduces the mechanism or clearly bounds its domain.

## 14. Handoff to engineering

Engineering should first implement the audio-interval, typed-state, local-patch, and replay contracts with a mock
model. The initial deliverable is a deterministic experiment harness that can prove identical exposure across
whole, chunked, two-pass, and agentic schedules. Only after carrier and execution approval should the team bind
the frozen omni runtime. Do not begin with a general agent framework: the paper lives or dies on exact audio
accounting, reversible edits, source support, and task-level attribution.

Implement these contracts through shared harness work packages H0–H8. AU-Harness or any other external toolkit
may supply task adapters and metric definitions only after an availability receipt; it must not replace the
common event ledger, capability receipt, budget governor, split boundary, or counterfactual replay engine.
