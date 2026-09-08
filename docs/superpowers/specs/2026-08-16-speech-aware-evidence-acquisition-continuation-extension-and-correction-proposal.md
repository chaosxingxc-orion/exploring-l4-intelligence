---
title: "Research proposal: speech-aware evidence acquisition continuation, engineering extension, and correction"
date: "2026-08-16"
status: "DRAFT_FOR_OWNER_REVIEW__NO_NEW_EXECUTION_AUTHORITY"
research_object: "speech-aware evidence acquisition"
study_repo: "studies/speech-aware-evidence-acquisition"
execution_contract: "wiki/experiments/speech-aware-evidence-acquisition/2026-08-04-owner-consolidated-execution-contract.md"
owner_amendment: "wiki/experiments/speech-aware-evidence-acquisition/2026-08-15-owner-go-dual-track-agentic.md"
shared_standard: "docs/superpowers/specs/2026-08-16-black-box-agent-harness-and-experiment-standard.md"
engineering_plan: "docs/superpowers/plans/2026-08-16-saea-supervisor-assessment-and-stage2a-continuation.md"
literature_cutoff: "2026-08-16"
adversarial_review: "second pass; ten attacks; scope and replaceability rules revised"
---

# Speech-Aware Evidence Acquisition: Continuation, Engineering Extension, and Correction

## 0. Decision

This proposal continues the admitted **speech-aware evidence acquisition** study. It does not replace the
study, rename it, demote it to one lane among several proposed knowledge studies, or create a parallel harness.
The existing research identity, execution contract, frozen black-box core, speech-only boundary, empirical
lineage, and engineering repository remain the foundation.

The corrected continuation thesis is:

> Can the existing speech-aware evidence-acquisition harness improve the task-relevant reliability of a frozen,
> API-only speech-omni model by constructing deployment-legal evidence, locating the speech uncertainty that
> needs it, supplying the smallest useful evidence packet at the right time, and verifying or rejecting the
> resulting revision—without model training, gold leakage, or cross-episode memory?

The study already owns the four necessary control dimensions:

1. `OBS` — obtain a stable speech observation and re-resolve selected spans;
2. `ORG` — construct and version legal, source-addressable evidence;
3. `SUPPLY` — select the evidence form, amount, order, modality, target, and timing;
4. `USE` — verify, accept, reject, splice, roll back, abstain, and stop.

The next work extends `ORG`, `SUPPLY`, and `USE` through the existing `OBS–ORG–SUPPLY–USE` system only when the
extension passes the speech-mediated admission test in Section 1.5. It does not split those dimensions into new
K2–K5 studies, but it also does not declare every future knowledge or agent task a child of SAEA. A future
agentic speech task system remains a separate umbrella Stage-1 candidate when planning, tool execution,
dialogue state, or environment interaction becomes the primary research object. The bounded Audio2Tool probe
admitted on 2026-08-15 remains leverage evidence, not permission to turn this study into a speech-to-action
paper.

This document provides research direction and an implementation plan. It creates no new repository, model
contact, dataset acquisition, confirmatory read, paid service use, or paper-scale authority.

## 1. What must remain unchanged

### 1.1 Research identity

The semantic research object remains **speech-aware evidence acquisition**. The study is not an ASR post-editor
and is not a generic RAG system. Its central object is the external control plane that acquires and uses evidence
when the evidence need is caused or mediated by speech uncertainty.

Entity-sensitive ASR is the current mechanistic instrument because it exposes exact before/after transitions,
wrong-reference copying, collateral edits, and evidence coverage. It is not the only task the execution contract
permits, and it need not be the final task-level demonstration.

### 1.2 Frozen-core and information boundary

The following constraints remain binding:

- the speech-omni core is a black-box, frozen, API-only component;
- no parameter update, acoustic-adapter training, answering-model substitution, or trained load-bearing critic;
- gold, gold-derived selection, reference transcripts, future turns, and test annotations never enter runtime;
- task-level frozen tools are allowed only when pinned, logged, and legal under the execution contract;
- the final output is produced by the frozen core plus deterministic harness operations;
- every evidence source, derivation, supply event, and accepted edit remains traceable;
- paper-scale confirmation still requires a separate paper repository and owner paper-execution contract.

### 1.3 Knowledge–memory boundary

This continuation studies knowledge, not memory.

Allowed knowledge includes metadata rosters, participant lists, issuer documents, public task schemas, legal
ontologies, tool registries, call-keyed documents, and inference-time products derived from legal inputs. It may
be organized before a campaign or derived within the current item and must retain provenance.

Disallowed memory includes writing outcomes from item `t` for use on item `t+1`, learning a persistent policy
from evaluation rewards, accumulating successful trajectories as demonstrations, or studying consolidation,
forgetting, retirement, retention, and longitudinal transfer. Those questions belong to a later memory study.

### 1.4 Existing engineering substrate

Engineering must extend, not fork, the current repository seams:

| Existing seam | Current role | Extension rule |
|---|---|---|
| `core.evidence` / `EVIDENCE_SOURCES` | Resolve none, ConEC, derived, oracle-refusal, and bias-list evidence | Add legal source adapters here; never create a second evidence service. |
| `core.evidence_derivation` / `TRANSFORMS` | Bind derived material to source hashes and pinned transforms | Add construction variants as versioned transforms with replayable manifests. |
| `core.evidence_budget` | Apply explicit evidence limits | Extend to structured packets while preserving deterministic truncation and accounting. |
| `core.flag_sources` | Locate roster-related uncertainty | Add flag families behind one typed interface and common trace schema. |
| `core.retrieval` | Score and retrieve candidate terms | Generalize only where the flag/retrieval contract remains causal and inspectable. |
| `core.policies` / `POLICIES` | Register fixed, observation-loop, and replay-loop policies | Add policy variants by registration; do not build a parallel agent runtime. |
| `reproduction.obs_loop` | Provide the stable long-form observation substrate | Freeze unless an explicit OBS ablation requires a change. |
| `reproduction.replay_loop` | Re-listen, deliver, verify, and splice | Correct the active reflection vehicle here and preserve all D7 guards. |
| tracing, attempts, bundles, finalizer | Bind exposure, events, outputs, cost, and commit identity | Treat these as scientific instrumentation, not optional infrastructure. |
| frozen scoring adapters | Score macro WER, entity outcomes, and task metrics | Add task adapters without altering an already-read ledger. |

### 1.5 Speech-mediated admission test

A new method, task, carrier, or engineering component belongs inside SAEA only if all six gates pass.

| Gate | Admission question | Fail meaning |
|---|---|---|
| G1 — speech-originated need | Is the evidence need caused or materially shaped by uncertain speech observation, recognition, speaker attribution, timing, or spoken semantics? | The object is generic knowledge access rather than SAEA. |
| G2 — speech-conditioned decision | Does the controller use audio, a speech-derived hypothesis, or a speech-specific uncertainty signal to decide whether, where, or what to acquire? | The intervention is ordinary static prompting or text RAG. |
| G3 — shared causal chain | Can the extension be decomposed as legal coverage → routing → delivery → verification/admission → task outcome? | It does not test the SAEA mechanism. |
| G4 — governed knowledge | Are source, transform, casing, selection, and target provenance legal and independently logged? | The arm is ceiling-tier or prohibited. |
| G5 — episode-local state | Does all outcome-derived working state reset at the governed item/session boundary? | The object has crossed into memory or continual learning. |
| G6 — deterministic attribution | Can a fixed or counterfactual baseline isolate the SAEA intervention under the same model, information, observation, and resource envelope? | The result cannot support a SAEA claim. |

Two practical tests make the boundary concrete:

1. **Gold-transcript replacement test.** Replace the audio observation with a correct transcript. If the
   intervention and claimed contribution remain unchanged, the work is probably generic knowledge control. It
   may be a useful external control, but it is not a core SAEA extension.
2. **Dominant-difficulty test.** Identify what makes the task hard after observation is controlled. If the
   dominant difficulty is dialogue planning, tool dependency management, persistent personalization, or duplex
   timing, the task belongs to the corresponding Stage-1 object even if speech is the input modality.

An extension that passes G1–G6 is a core SAEA work package. An extension that passes the information and
measurement gates but only partly passes G1–G3 may enter as a labelled diagnostic or bounded leverage probe.
Anything whose dominant research object lies elsewhere is routed out before engineering begins.

### 1.6 Preserve the scientific system, not every current implementation

“Build on the existing engineering solution” has four different meanings. Conflating them would either destroy
the study lineage or freeze avoidable defects.

| Layer | Status | Examples | Engineering rule |
|---|---|---|---|
| Scientific contract | Preserve | SAEA identity; speech-only scope; frozen black-box core; information boundary; split/exposure discipline; `OBS–ORG–SUPPLY–USE` factorization | Change only through an explicit owner amendment. |
| Measurement substrate | Preserve and extend compatibly | attempt/bundle/finalizer; event ledger; provenance tiers; scorer identity; cost accounting; counterfactual replay | New capabilities must retain old run readability and fail-closed semantics. |
| Algorithmic interfaces | Keep stable, extend through registration | evidence sources; transforms; flag sources; retrieval results; policies; task scorers | Add typed implementations behind existing contracts; justify any schema change with migration tests. |
| Algorithms and policy choices | Replaceable by evidence | roster-band matching; retrieval score; construction representation; supply packet; verifier; splice/edit strategy; stop rule | Compete through preregistered ablations; the current implementation has no protected status. |
| Closed or invalid routes | Retire, retain as evidence | cross-call error-pattern KB for the current candidate; pass-1 exemplar leakage; silently empty candidate pools; inconsistent double filtering; unsupported splices | Do not revive without new evidence that directly overturns the recorded failure. |

This rule permits substantial engineering innovation without creating a second experimental universe.

## 2. Empirical position at the continuation point

The next plan must start from measured facts, not from a new abstract architecture.

| Evidence | What it establishes | What it does not establish |
|---|---|---|
| Whole-call decoding collapsed on long recordings; the observation loop produced complete transcripts. | An agentic `OBS` substrate is necessary for this frozen runtime. | Superiority over published long-form ASR systems. |
| `SAEA-E-001` produced a 10-call bare-core reference floor with mean WER `0.2674`. | The study has a governed, traceable long-form baseline. | A final method result. |
| The frozen-ten zero arm scored `12.38` macro WER. | A same-substrate comparison anchor exists. | General ASR quality outside this carrier and split. |
| A matched 10-item full bag scored `12.39`, added only 241 correct entity tokens, and used roughly four times the prompt tokens. | More evidence is not automatically more useful; form and efficiency matter. | That every large context is harmful under every framing. |
| Oracle names scored `10.88`, improved 9/10 calls, and reduced entity WER from `32.01` to `19.95`. | Correct, compact, cased entity knowledge has substantial reachable headroom. | A deployment method; the arm is ceiling-tier. |
| A deployment-legal metadata roster scored `12.09`, improved 7/10 calls, and added 117 correct entity tokens. | Legal knowledge has directional value and recovers part of the oracle effect. | Statistical confirmation at `n=10`; the paired macro result was `p=.19`. |
| Metadata recovered roughly 20% of the oracle macro effect and 12% of the entity effect. | Label coverage is a primary bottleneck. | That retrieval and verification are already solved. |
| Targeted re-listen alone was effectively nil on the measured P1 vehicle. | Extra audio calls do not explain the knowledge effect on that arm. | That re-listening is useless on every span or downstream task. |
| Static oracle supply flipped 10/14 targeted entities but paid collateral and format costs. | The model can consume target knowledge, while static global carry is unsafe. | That reflection is superior; the replay vehicle was invalidated before that comparison. |
| The D7 series ended with a delivery gate pass: 14 accepted edits, all payloads verified, and conservative true-error delivery above the registered threshold. | The production replay path can acquire, deliver, and guard evidence end to end. | That the reflection operator improves aggregate outcomes. |
| Wrong forms such as `Pheonix` were sometimes resisted, while bad splices still caused pollution before guards. | Audio verification capacity is plausible and splice mechanics are a distinct risk. | A validated verification claim; P2 must decide it. |
| The examined cross-call error-pattern KB had no useful rare-name reachability. | That route is closed for the current candidate. | A verdict on all future memory or cross-call systems. |

The evidence supports continuation. It also limits the claim: the legal method is promising but incomplete, the
reflection taxonomy is unresolved, and task-level transfer is not yet demonstrated.

**Operational state at authoring.** The study ledger records that the first P2 block was aborted at manifest
binding after a mid-flight working-tree change. The completed `r0bias` inference is assigned to one-time offline
salvage and must not be re-flown; the four comparator arms were resumed under the same preregistration. The
study working tree is clean, but the ledger contains no terminal comparator verdict. Engineering must verify
the live process and terminal manifests before any study-repository edit. This proposal is not a live-status
authority and does not infer an outcome from the absence of new commits.

## 3. Second adversarial self-debate and surviving revisions

### Round 1 — sunk-cost prosecution

**Attack.** The study may be preserved only because its harness is extensive and many GPU hours have already
been spent. Engineering effort is not evidence that the research question remains valuable.

**Finding.** The attack rejects preservation by cost, but not preservation by evidence. SAEA has produced
addressable findings: whole-call observation failure, a governed long-form substrate, a strong oracle roster
ceiling, partial legal-roster recovery, a form-versus-dose result, a measured coverage gap, a closed cross-call
KB route, and a replay-vehicle failure taxonomy.

**Revision.** Continue because the study has accumulated reusable causal evidence and measurement capability.
Retain explicit stop conditions so that legal coverage, routing, or task-conversion failure can still complete
the study as a negative result.

### Round 2 — scope-elasticity prosecution

**Attack.** Calling every knowledge, QA, SLU, or tool task an SAEA extension would transform a bounded speech
research object into a generic knowledge-agent program.

**Finding.** The attack succeeds. Speech as the input modality is not sufficient. The evidence need and control
decision must be materially speech-conditioned.

**Revision.** Apply Section 1.5 before work-package admission. A task that becomes scientifically identical
after replacing audio with a correct transcript is an external control or a separate object, not the SAEA core.

### Round 3 — narrow-ASR-endpoint prosecution

**Attack.** Deployment-legal small-roster spelling improvement is too narrow for a strong doctoral endpoint and
may be dismissed as prompt-level contextual biasing.

**Finding.** The attack succeeds against an ASR-only endpoint but not against entity-ASR as a mechanistic
instrument. Entity transitions expose delivery, copying, verification, harmful edits, and coverage more
directly than broad task scores.

**Revision.** Keep entity-ASR as the mechanism rung. Use SLURP, direct contextual-transfer carriers, and
conditional spoken QA to test whether the same acquisition policy changes meaningful task outcomes. Do not
rename the study “task-level knowledge control.”

### Round 4 — engineering-lock-in prosecution

**Attack.** Requiring all work to use the current implementation could protect roster-band scoring, replay
splicing, and present schemas even when better methods exist.

**Finding.** The attack succeeds if “reuse” means algorithmic immutability.

**Revision.** Preserve the scientific contract and measurement substrate. Keep interfaces stable where
possible. Treat construction, flagging, retrieval, verification, editing, and stopping algorithms as
replaceable hypotheses. Require registered adapters and migration tests rather than a parallel runtime.

### Round 5 — moving-target prosecution

**Attack.** Simultaneously changing knowledge construction, routing, verification, task adapters, and models
would create a moving target. Any positive task result would be causally uninterpretable.

**Finding.** The attack succeeds. A feature roadmap cannot substitute for an experiment sequence.

**Revision.** Close the operator question, then construction coverage, then routing, then safe use, then task
conversion. Model-free adapter, source, and literature preparation may proceed in parallel, but result-bearing
arms must follow the gated order.

### Round 6 — legality-and-coverage prosecution

**Attack.** Oracle-selected names prove only that the model follows privileged hints. Gold-derived selection,
casing, or span routing could manufacture a deployment result.

**Finding.** The attack succeeds. The legal roster currently recovers only a fraction of oracle headroom.

**Revision.** Treat legal coverage as the first causal stage. Freeze a source ladder from metadata to participant
rosters and pinned issuer documents. Record `span_source` and `reference_source` separately. If either field is
gold-derived, the entire arm is ceiling-tier regardless of the other fields.

### Round 7 — reflection-dependence prosecution

**Attack.** SAEA may have become rhetorically dependent on proving that verify-with-abstention is a distinct
operator, even though earlier replay arms mixed multiple vehicle defects.

**Finding.** The attack succeeds against operator-first positioning. D7E establishes delivery airworthiness,
not reflection superiority. P2 remains unresolved in the current ledger.

**Revision.** Apply the registered P2 AFFIRM/COLLAPSE/UNRESOLVED decision. If reflection collapses, continue only
with the simpler targeted-supply candidate. A failed reflection hypothesis is not a failed SAEA study.

### Round 8 — metric-standardization prosecution

**Attack.** P2 named harmful edit rate and recoverable-information ratio without formulas; the first arm was
read before the definitions were pinned. The branch rule therefore carries avoidable analytic freedom.

**Finding.** The attack succeeds as a reliability discount. The dated amendment constrains later reads but
cannot restore perfect preregistration chronology.

**Revision.** Carry the disclosure into every verdict. Print raw counts with HER/RIR, apply denominator guards,
mark unresolved clauses as unresolved, and require a clean preregistration before any paper-level operator
claim.

### Round 9 — benchmark-tour prosecution

**Attack.** Adding contextual ASR, SLU, spoken QA, and tool use can produce a benchmark tour in which every task
uses a different prompt trick and no shared mechanism transfers.

**Finding.** The attack succeeds unless one frozen policy graph and evidence-packet contract cross tasks.

**Revision.** Port only the smallest surviving construction–routing–verification policy. Require a legal
knowledge source, a detectable speech-mediated need, fixed baselines, deterministic task outcome, and bounded
correct-to-wrong regression on every task. Keep Audio2Tool secondary and probe-scoped.

### Round 10 — novelty-and-maturity prosecution

**Attack.** Contextual ASR, RECOVER, Voice Memory, RAG-based context discovery, DeRAGEC, and trained audio
retrieval already occupy much of the method space. The current `n=3`/`n=10` evidence may not support a distinct
contribution.

**Finding.** The attack succeeds against broad novelty or superiority claims. The remaining provisional gap is
narrower: training-free, black-box speech-conditioned acquisition with legal provenance, targeted supply,
audio-grounded verification/abstention, harmful-edit controls, and task conversion in one auditable harness.

**Revision.** Make simple fixed pipelines the strongest causal opponents. Treat the present findings as
Stage-2A discovery evidence. A policy contribution survives only if it beats fixed supply/retrieve–prompt
controls under matched information and resources and no stronger runnable prior establishes the same boundary.

### Surviving position

The strongest defensible direction is not “build a general knowledge agent,” and it is not “preserve the
current implementation.” It is:

> Preserve SAEA's research identity, evidence lineage, and scientific harness; replace any algorithm that fails;
> extend only through speech-mediated, legally sourced, causally attributable work; and test whether the
> smallest surviving acquisition policy converts local evidence recovery into meaningful spoken-task outcomes
> without increasing harmful edits or relying on privileged information.

## 4. Research questions and falsifiable hypotheses

### RQ1 — legal knowledge construction and coverage

Can SAEA construct a compact legal knowledge artifact that recovers substantially more oracle-reachable entity
coverage than metadata alone without importing gold-derived labels?

**H1.** A provenance-bound, call-keyed document construction pipeline will increase legal coverage and candidate
recall over metadata rosters while using fewer supplied tokens than raw-document injection.

**Falsification.** The construction ladder does not improve reachable coverage, improves only because of
gold-derived routing/casing, or requires raw documents at a cost that erases its benefit.

### RQ2 — speech-aware evidence acquisition

Can the current speech and draft state identify where legal evidence is needed better than global static supply
or a transcript-only generic retriever?

**H2.** Roster-band or another pinned speech-aware flag source, combined with legal candidate construction,
will deliver correct references to a useful fraction of true errors while keeping false-delivery and compute
within a frozen envelope.

**Falsification.** Oracle routing is strong but legal routing retains no useful fraction, or delivered false
references dominate the correct-reference opportunity set.

### RQ3 — verified evidence use

Does verify-with-abstention constitute a safer and more effective operator than span-scoped bias under matched
evidence and observation?

**H3.** Verification will reduce wrong-reference copying and harmful accepted edits at matched entity recovery;
the own draft may add recoverable information only when it does not anchor the model to its previous error.

**Falsification.** P2 satisfies the preregistered taxonomy-collapse rule, wrong-reference copying survives the
verification framing, or denominator guards leave the operator distinction unresolved.

### RQ4 — task-value transfer

Does the smallest legal SAEA policy improve meaningful spoken-task outcomes beyond spelling and WER?

**H4.** The same acquire–supply–verify pattern will improve answer-critical entities, SLURP slot/command success,
or another deterministic task endpoint with bounded correct-to-wrong regression.

**Falsification.** The method improves transcript entities but not the downstream outcome, or every task requires
a different policy that cannot be expressed as the same SAEA control law.

### RQ5 — black-box harness value

Can the improvement be attributed to external control rather than model choice, extra calls, extra legal
information, or changed serving infrastructure?

**H5.** After ceiling discovery and consolidation, the smallest policy will retain a benefit against fixed
pipelines under matched model, information, observation, and resource envelopes.

**Falsification.** A fixed retrieve-and-prompt baseline matches the policy, gains disappear under matched
resources, or the result depends on private runtime behavior that cannot be reproduced through the black-box
contract.

### Claim stack and dependency order

The study should qualify claims one layer at a time. A higher claim cannot compensate for a failed lower layer.

| Claim | Required evidence | Current status | Promotion condition |
|---|---|---|---|
| C0 — governed observation and measurement | Complete long-form observation, immutable identity, leakage controls, attributable traces | Supported as a Stage-2 substrate | Preserve as common-mode infrastructure. |
| C1 — legal evidence accessibility | Legal construction materially expands reachable target coverage over metadata at bounded distractor and token cost | Partial; metadata works directionally, document construction open | Pass WP1 construction gate. |
| C2 — speech-aware acquisition | A speech-conditioned route delivers useful legal evidence more precisely or efficiently than global/fixed transcript-only supply | D7 vehicle airworthy; legal routing unproven | Pass WP2 against fixed and oracle-routing controls. |
| C3 — verified use | Admission/verification improves target recovery or reduces copying/harm relative to span bias at matched evidence | Unresolved; P2 decides the operator taxonomy | AFFIRM or retain a narrower supply-only claim. |
| C4 — task conversion | The same smallest policy changes a deterministic non-ASR spoken-task outcome | Unproven | Pass at least one natural-speech task-value rung. |
| C5 — portability | The frozen policy retains direction on an independent carrier and later a different model family | Unproven; not a current start gate | Stage-2 carrier transfer, then separately authorized confirmation. |

The proposal explicitly does not claim:

- a general-purpose knowledge agent;
- online continual evolution or cross-episode memory;
- a new trained retriever or speech encoder;
- general speech-to-action competence from the bounded Audio2Tool probe;
- full-duplex interaction, dialogue management, or long-lived personalization;
- cross-model or publication-level superiority from the current discovery evidence.

## 5. Corrected system design

### 5.1 State and action model

The harness maintains per-item state only:

```text
episode_state = {
  observation_manifest,
  pass1_hypothesis,
  candidate_spans,
  legal_knowledge_manifest,
  delivered_evidence,
  verifier_outputs,
  accepted_edits,
  rejected_edits,
  cost,
  stop_reason
}
```

The allowed action space stays small and inspectable:

```text
OBSERVE(span_or_window)
CONSTRUCT(source_ids, transform_id)
FLAG(flag_policy_id)
RETRIEVE(query, k, budget)
SUPPLY(span, evidence_packet, framing)
VERIFY(span, audio, candidate, optional_own_draft)
ACCEPT(edit)
REJECT(edit, reason)
ROLLBACK(edit_id)
ANSWER(task_output)
ABSTAIN(reason)
STOP(reason)
```

No action writes persistent experience for later evaluation items.

### 5.2 Evidence packet

Every delivered packet must carry:

```text
evidence_packet = {
  packet_id,
  sample_id,
  source_ids,
  source_tier,
  transform_id,
  transform_version,
  content_hash,
  candidate_forms,
  modality,
  target_span,
  retrieval_scores,
  budget_bytes,
  span_source,
  reference_source,
  legality_tier,
  oracle_ceiling_probe
}
```

The packet is immutable after supply. Any replacement creates a new packet and a new trace event.

### 5.3 Reward and constraints

Discovery may use a vector reward rather than a hidden scalar:

```text
reward = {
  task_gain,
  entity_gain,
  evidence_support,
  harmful_edit_penalty,
  wrong_reference_copy_penalty,
  unsupported_change_penalty,
  latency_penalty,
  model_call_penalty,
  supplied_token_penalty
}
```

The harness may select actions from these logged signals. It may not update model parameters or learn a
persistent cross-item policy from held-out outcomes.

### 5.4 Causal decomposition

The integrated result must be decomposable into:

```text
legal source coverage
  -> construction recall
  -> routing/flag recall
  -> evidence delivery precision
  -> verification and admission
  -> local edit quality
  -> task outcome
```

This chain replaces a single end-to-end score as the primary research instrument. A failed downstream result
must be assignable to one stage rather than described as “the agent did not work.”

## 6. Engineering correction backlog

These are corrections to the current vehicle, not a request to rebuild it.

| Priority | Correction | Required result |
|---|---|---|
| P0 | Protect any live P2 flight from working-tree mutation. | Every attempted arm reaches a terminal manifest; no mid-flight commit or guide edit invalidates binding. |
| P0 | Mirror the P2 HER/RIR definition amendment into the study during the next GPU gap. | The formulas travel with the preregistration; the late-pin disclosure remains explicit. |
| P0 | Preserve fail-closed derived-candidate materialization. | Unsupported or empty candidate pools cannot be silently interpreted as “no need.” |
| P0 | Preserve pass-1 evidence/exemplar suppression in reflection arms. | The shared pass-1 draft is not already biased by the evidence later attributed to replay. |
| P0 | Preserve matched-form, pre-localize response, and source-tier trace fields. | Wrong-reference copying and delivery can be audited from stored bytes. |
| P0 | Keep flag and retrieval semantics single-valued. | A flag that selects a roster candidate cannot be silently rejected by a second unrelated metric. |
| P0 | Retain reference-only rejection and splice-support guards. | Reference echo and mislocalized insertions cannot enter the final transcript as accepted edits. |
| P1 | Add structured evidence-packet tracing. | Every supply action binds source, transform, target, budget, legality, and content hashes. |
| P1 | Add per-stage opportunity accounting. | Coverage, route, delivery, verify, accept, and task-conversion denominators are machine-derived. |
| P1 | Add deterministic counterfactual replay. | Remove, shuffle, or replace evidence without changing unrelated run identity. |
| P1 | Add task-adapter scoring behind the frozen scorer registry. | ASR, entity, QA, slot/frame, and tool-argument metrics share one manifest discipline. |
| P2 | Add matched-resource accounting. | Model calls, audio seconds, prompt/completion tokens, wall time, and retries are comparable by arm. |

Closed or forbidden engineering routes:

- do not revive the measured cross-call error-pattern KB for the current candidate;
- do not implement a persistent memory store under the name “knowledge”;
- do not create a new agent framework beside the current harness;
- do not use gold-derived casing, selection, or span routing in a legal-tier arm;
- do not scale beyond the current gate merely because an oracle arm is positive;
- do not treat an empty candidate pool, missing trace field, or failed materialization as a negative scientific
  result.

## 7. Work packages for the engineering team

### WP0 — close the unresolved P2 R-ladder

**Purpose.** Decide whether reflection survives as a distinct operator after vehicle corrections.

**Existing arms.** `R0-bias`, `R1-verify`, `R2-own-draft`, and wrong-reference controls under both bias and
verify framing on the frozen ten.

**Required reads.** Co-primary paired macro and entity ledgers; pre-localize wrong-reference copy counts; HER
with raw counts; RIR with raw counts; format-normalized secondary; term-level flips; call, audio, token, and
wall cost.

**Decision.** Apply the registered AFFIRM/COLLAPSE rules mechanically. If a denominator guard binds, record the
clause as unresolved. Do not reinterpret a taxonomy collapse as a failed study: the surviving candidate may
still be targeted, legal small-N supply, but it must drop “distinct reflection operator” language.

**Exit artifact.** One verdict that separates: scientific outcome, vehicle reliability, late metric pinning,
and any required clean confirmation.

### WP1 — construct deployment-legal knowledge with higher coverage

**Purpose.** Convert the observed metadata-to-oracle gap into a measurable construction problem.

**Source ladder.** Freeze the source set before result reads:

1. metadata-only roster;
2. metadata plus participant roster;
3. metadata-resolved, pinned public issuer documents;
4. legal system-derived entity candidates from the same call or authorized documents;
5. oracle labels as a ceiling-tier diagnostic only.

**Construction ladder.** Compare raw text, normalized terms, cased terms, typed entity records, alias sets, and
minimal relation/schema fields. Every transformation receives a version, parameters hash, input hashes, output
hash, and source-tier receipt.

**Primary metrics.** Legal coverage of oracle-reachable errors, candidate recall, casing accuracy, distractor
rate, bytes/tokens per covered target, and construction latency.

**Gate.** Continue only if a legal construction variant materially expands reachable coverage over metadata
without an unacceptable distractor or budget increase. If it does not, narrow the SAEA candidate to metadata-
available domains rather than hiding the coverage ceiling.

### WP2 — route legal evidence to the right speech uncertainty

**Purpose.** Measure the acquisition policy separately from evidence quality.

**Routing ladder.** Evaluate, on the same candidate artifact:

1. global static supply;
2. fixed transcript-only lexical query;
3. roster-band flagging from the own pass-1 draft;
4. speech/audio representation retrieval where already pinned and legal;
5. hybrid candidate generation with deterministic arbitration;
6. oracle routing as a ceiling-tier diagnostic.

**Required controls.** Matched irrelevant references, shuffled legal references, no-knowledge re-listen, and
equal-candidate-set fixed top-k.

**Primary metrics.** Opportunity recall, delivered-reference precision/recall, false-delivery rate, routing
coverage by entity class, query cost, and retained fraction of the oracle-routing ceiling.

**Gate.** Do not scale the full chain unless legal routing retains a useful preregistered fraction of oracle
routing and the false-delivery burden is compatible with the verification stage.

### WP3 — consolidate safe evidence consumption

**Purpose.** Turn delivery into verified task improvement.

**Consumption variants.** Compare static span bias, verify-with-abstention, verify plus own draft, reference
replacement, and no-reference re-listen. Keep the audio span, legal candidate set, pass-1 draft, and serving
substrate fixed.

**Safety requirements.** Pre-localize echo capture, wrong-reference controls, unsupported-change rejection,
local splice support, rollback, and an explicit stop reason.

**Primary metrics.** Correct-to-correct preservation, wrong-to-correct conversion, correct-to-wrong regression,
HER, RIR, wrong-reference copy count, unsupported edit count, accepted/rejected edit counts, and net task gain.

**Gate.** Promote the smallest consumption policy that preserves most target recovery while reducing harmful
edits. If verification adds no value, use the simpler targeted supply policy and report the negative result.

### WP4 — extend the task ladder without changing the study identity

Every adapter must pass G1–G6 before a result-bearing arm is registered. The task changes the outcome metric,
not the scientific identity or policy graph.

#### WP4A — SLURP entity-to-command value

SLURP is explicitly admitted through the entity clause. Use the inference-time ontology as deployment-legal
knowledge. Measure slot value, semantic frame, and command-level success; keep intent-only and transcript-only
baselines. The claim is that evidence acquisition recovers task-critical entities, not that SAEA solves general
spoken-language understanding.

#### WP4B — off-domain evidence-acquisition transfer

Use SlideASR-Bench or another receipt-verified speech-only roster carrier to test whether the construction,
routing, and supply machinery transfers beyond earnings calls. This is a mechanism-transfer test, not a new
research object. Synthetic-speech rows may be diagnostics, but the main transfer read must retain a clearly
reported human/synthetic provenance and cannot silently stand in for natural-speech external validity.

#### WP4C — spoken QA and evidence use

Use only a held and license-verified speech QA carrier with deterministic answer/evidence scoring. Select items
whose answer is changed by speech-critical evidence; report answer gain conditional on observation and evidence
availability. Do not use a service-dependent LLM judge as the sole primary endpoint.

#### WP4D — bounded Audio2Tool leverage probe

Run only the owner-admitted prompt-side entity-roster comparison on the authorized subset and license terms.
Primary outcomes are exact tool and argument correctness; WER is secondary. Cluster by underlying query where
multiple audio renditions exist. The result may show that knowledge injection changes end-to-end success, but
it must not be used to claim a general speech-to-action system or to absorb the separate Stage-1 agentic task
candidate into SAEA. Do not run the noisy cells until a legal, registered noise path exists; a missing noise
source is not permission to invent one post hoc.

**Task-ladder gate.** At least one natural-speech non-ASR task must show a deterministic improvement attributable
to the same construction–routing–verification policy, with bounded correct-to-wrong regression. Otherwise keep
the paper candidate at the mechanism level and do not inflate its endpoint. Audio2Tool alone cannot pass this
gate because its audio is synthesized and its admission is probe-scoped.

### WP5 — baseline reproduction and prior-difference closure

Before candidate qualification, produce an availability receipt for every load-bearing baseline:

- artifact URL and immutable revision;
- code and data license;
- model/runtime dependencies;
- evaluator dependency and service requirement;
- local smoke status;
- required deviation from the published system;
- classification as reproducible baseline, runnable arm, external reference, or related work only.

The local baseline ladder remains primary: no knowledge; full legal context; compact metadata roster; fixed
lexical/dense retrieval; fixed retrieve–pack–answer; targeted supply without verification; targeted verify-with-
abstention; and oracle ceilings. External systems strengthen positioning only when their behavior is runnable
under the same boundary.

### WP6 — candidate package and handoff

Assemble one self-contained Stage-2A candidate package containing:

1. exact improvement claim and null hypothesis;
2. unchanged study identity and scope statement;
3. prior-difference matrix with availability classes;
4. legal source and derivation contract;
5. frozen policy graph and event schema;
6. baseline and ablation matrix;
7. exposure, metric, and deviation receipts;
8. discovery findings separated from unread confirmation plans;
9. limitation and negative-result register;
10. explicit owner decision request for stop, continue within Stage-2A, or promote a paper candidate.

### Engineering ticket map

These tickets describe the baseline to prepare after WP0 reaches a verified GPU gap. They do not authorize a
study edit or model run. Implement deterministic tests before registering any result-bearing arm.

| Ticket | Existing ownership seam | Change | Model-free acceptance test | Depends on |
|---|---|---|---|---|
| E0 — flight protection | launcher, attempts, bundle/finalizer | Add an operator-visible clean-tree/freeze preflight receipt and refuse mutation-sensitive launch states. | Dirty-tree, changed-HEAD, and concurrent-flight fixtures fail before inference; clean fixture binds the expected commit. | WP0 terminal-state check. |
| E1 — evidence packet v1 | `core.evidence`, `core.evidence_derivation`, tracing | Materialize the Section 5.2 packet fields without introducing a second evidence registry. | Hash, source tier, transform version, target, budget, and legality round-trip exactly; mutation produces a new packet id. | E0. |
| E2 — legal construction adapters | `EVIDENCE_SOURCES`, `TRANSFORMS`, evidence budget | Add metadata/roster/document construction variants and manifests. | Gold-derived source refuses legal tier; missing source and transform mismatch fail closed; deterministic rebuild is byte-identical. | E1. |
| E3 — opportunity ledger | scorer adapters, trace reader, offline reports | Derive coverage → route → delivery → verify → accept → task-conversion counts from immutable events. | Hand-authored fixtures reproduce exact numerators/denominators; empty and `<10` denominators trigger the registered guards. | E1. |
| E4 — routing contract | `core.flag_sources`, `core.retrieval` | Define one typed `FlagDecision`/`RetrievalDecision` path with explicit pass-through semantics where the flag already selects a candidate. | Flagged candidates cannot disappear without a logged reason; shuffled and irrelevant references remain distinguishable. | E2, E3. |
| E5 — admission/edit controller | `core.policies`, replay loop, splice/edit utility | Make verify, reject, abstain, accept, rollback, and stop explicit events; preserve D7E guards as the initial implementation. | Reference-only response, unsupported splice, wrong target, and empty support reject; valid local edit and rollback replay deterministically. | E3, E4, P2 verdict. |
| E6 — task adapters | carrier registry, scorers, configs | Add SLURP first, then approved transfer/QA adapters through the existing experiment identity. | Same fixture scores transcript, entity, slot/frame, and task outputs deterministically; one source item remains one independent unit. | E2–E5, task admission receipt. |
| E7 — counterfactual reporter | trace replay, report builder | Re-score remove/shuffle/replace-evidence counterfactuals and matched-resource summaries. | Counterfactual changes only the declared evidence event; unrelated observation/model identity stays equal. | E3–E6. |
| E8 — compatibility and regression | existing test suite and recorded-response replay | Prove old arms remain readable and current baseline configs retain semantics. | Legacy manifests load; old evidence sources resolve; no-policy recorded-response replay is unchanged; new fields have explicit defaults or migrations. | Every prior ticket. |

Definition of engineering-baseline completion:

- all model-free unit and replay tests pass;
- legacy run manifests remain readable;
- one mock end-to-end item produces complete `OBS/ORG/SUPPLY/USE/COST/STOP` events;
- provenance and state-reset negative tests fail closed;
- the strongest fixed baselines can use the same legal information and task adapter;
- no runtime result has been read to choose thresholds, prompts, or metric definitions;
- a new arm is not registered until its scientific question, changed factor, controls, unit, metrics, branch
  rule, and exposure row are complete.

## 8. Standard experiment matrix

The following matrix keeps the causal questions separate. Not every row requires immediate execution; each row
requires a valid authority and preregistration before model contact.

| Block | Frozen factors | Changed factor | Required controls | Promotion read |
|---|---|---|---|---|
| A — construction | model, OBS, task items, supply policy | legal source/representation | raw source, metadata, oracle ceiling | coverage and efficiency |
| B — routing | model, OBS, legal candidate artifact, verifier | flag/query/retrieval policy | global, transcript-only, irrelevant, oracle route | delivery recall/precision |
| C — use | model, OBS, spans, references, candidate set | framing/admission policy | no-relisten, relisten-only, wrong reference | task gain, HER, copy resistance |
| D — integration | model, carrier, legal information | smallest end-to-end policy | strongest fixed pipeline | net outcome and cost |
| E — task transfer | policy and black-box contract | task adapter/carrier | native task baselines | deterministic task success |
| F — portability | policy, task, resource envelope | model family/runtime | per-model no-policy baseline | direction and failure taxonomy |

### 8.1 Phased evidence discipline

1. **Ceiling-seeking discovery.** Oracle and unequal-cost arms may reveal headroom; they cannot support the
   deployment claim.
2. **Mechanism consolidation.** Remove components until the smallest policy retains the observed effect.
3. **Matched-resource causal comparison.** Freeze legal information, model, task items, observation, and budget;
   compare the policy against the strongest fixed baseline.
4. **Robustness and task transfer.** Change one axis at a time and preserve task-specific deterministic metrics.
5. **Held-out confirmation.** Requires the proper paper-stage authority; no policy decision follows a held-out
   read.

### 8.2 Required unit of analysis

- use the original call, utterance, query, or scenario as the independent unit;
- never count replay windows, audio renditions, or multiple slots from one item as independent samples;
- use paired item-level comparisons where the same item appears in both arms;
- publish per-item transitions and raw denominators with aggregate statistics;
- separate discovery, development, and confirmatory exposure in the ledger.

## 9. Metrics and reliability requirements

### 9.1 Mechanism metrics

- legal source coverage;
- construction recall and distractor rate;
- routing opportunity recall and delivery precision;
- delivered-on-true-error fraction;
- evidence bytes/tokens per covered opportunity;
- accepted and rejected replay counts;
- wrong-reference copy count on pre-localize text;
- RIR with numerator and denominator;
- HER per ledger with numerator and denominator;
- correct-to-wrong and wrong-to-correct transitions;
- unsupported-change and splice-mislocalization counts.

### 9.2 Task metrics

- ASR: call-level WER, entity-WER, entity correct count, format-normalized secondary;
- spoken QA: deterministic answer score, answer-critical entity correctness, evidence support, abstention;
- SLU: intent, slot value, full semantic frame, and command-level success;
- tool-shaped probe: exact tool, normalized arguments, schema validity, dependency correctness where applicable.

### 9.3 Efficiency metrics

- frozen-core calls and audio seconds;
- prompt and completion tokens;
- evidence bytes/tokens supplied;
- wall time and GPU hours;
- retrieval/tool invocations;
- retries, timeouts, aborted attempts, and failed-attempt cost;
- task gain per 1,000 supplied tokens and per additional model call.

### 9.4 Reliability rules

- define every metric before the first result that can influence it is read;
- disclose and retain the P2 late-definition sequence;
- print raw denominators for every rate;
- preregister degenerate-denominator behavior;
- keep the scorer immutable within a campaign;
- never replace a failed primary metric with a favorable post-hoc secondary;
- log negative and invalidated arms with their original registration;
- distinguish vehicle failure, null mechanism, and insufficient statistical resolution.

## 10. Model and baseline standardization

### 10.1 Current anchor

The current Qwen3-Omni Q4_K_M runtime remains the discovery anchor because the study's result lineage, latency
engineering, serving receipts, and causal contrasts are bound to it. Q4 versus Q8 is a numerics/quantization
check, not an independent model replication.

Do not switch the primary model while resolving P2, legal construction, routing, or task adapters. A model
change would confound the intervention with a new capability surface.

### 10.2 Portability model

A second model family becomes relevant only after the smallest policy is frozen and the model satisfies the
same black-box contract: direct speech input, deterministic-enough decoding, stable response schema, accessible
latency/cost accounting, and legal reproducibility. It is a portability test, not a model-selection sweep.

### 10.3 Baseline availability classes

| Class | Meaning | Claim role |
|---|---|---|
| R0 | Native deterministic baseline in the current harness | Primary causal comparison. |
| R1 | Official artifact reproduced locally with pinned code/data/model and bounded documented deviations | Primary or strong secondary comparison. |
| R2 | Partly reproducible; proprietary service, missing release, or material adapter substitution remains | Sensitivity or external reference only. |
| R3 | Paper description, unavailable artifact, or incompatible boundary | Related work only. |

## 11. Academic landscape and survey updates

The relevant frontier is not one literature family. The candidate must remain positioned at the intersection of
contextual speech recognition, speech/audio retrieval, evidence-use control, and spoken task evaluation.

| Work | Established fact relevant to SAEA | Required distinction or action |
|---|---|---|
| [ConEC, LREC-COLING 2024](https://aclanthology.org/2024.lrec-main.328/) and contextual ASR lines | Context and entity evidence can improve speech recognition under purpose-built methods. | Reproduce or behaviorally match the strongest runnable context baselines; SAEA's claim must concern frozen-core acquisition and verified use. |
| [Retrieval-Augmented Context Discovery for ASR, Findings EMNLP 2025](https://aclanthology.org/2025.findings-emnlp.768/) | The published context ladder reports a clean dose/quality response on ASR, including Earnings-21, but no official runnable code was found in the local audit. | Use the context-quality ladder and reported result as a prior; implement a clearly labelled behavioral arm rather than claiming literal reproduction. |
| [RECOVER, 2026](https://arxiv.org/abs/2603.16411) | The closest black-box entity-repair prior orchestrates hypothesis variants and retrieved entities and reports entity-sensitive improvements across multiple datasets; the local audit found no released code. | It is the primary method-difference opponent. SAEA must isolate what localized audio verification and legal source control add beyond text/hypothesis orchestration. |
| [Voice Memory, 2026](https://arxiv.org/abs/2607.26410) | It measures whether post-ASR edits are harmful and how much recoverable information is used, while operating with N-best hypotheses and memory rather than localized audio verification. | Adopt HER/RIR only with pinned local definitions; keep cross-episode memory outside the present method boundary. |
| [DeRAGEC, Findings ACL 2025](https://arxiv.org/abs/2506.07510) | Candidate denoising and synthetic rationale target named-entity correction after ASR. | Candidate quality and denoising are occupied; compare against a runnable/native denoising control before claiming construction novelty. |
| [ProfASR-Bench, 2025](https://arxiv.org/abs/2512.23686) | Its context/profile/oracle/adversarial ladder directly probes whether supplied professional context helps, but the current public carrier is synthetic and lacks a held-out test split. | Use it as a secondary counter-claim and adversarial-context reference, never as the headline natural-speech validation. |
| [WavRAG, ACL 2025](https://aclanthology.org/2025.acl-long.613/) | Hybrid audio/text retrieval can avoid some transcript-cascade loss with a trained retriever. | Audio-native retrieval is prior art; SAEA contributes only if the black-box, training-free control plane adds evidence. |
| [Adaptive Retrieval Without Self-Knowledge?, ACL 2025](https://aclanthology.org/2025.acl-long.319/) | Retrieval is not always needed and adaptive policies must account for efficiency. | Zero retrieval, fixed top-k, and cost-normalized controls are mandatory. |
| [Retrieval Is Not Enough, NeurIPS 2025](https://proceedings.neurips.cc/paper_files/paper/2025/file/1f09e1ee5035a4c3fe38a5681cae5815-Paper-Conference.pdf) | Retrieved evidence can still be misused; trained critics are one response. | SAEA must measure evidence admission and harm without adding a trained answering critic. |
| [Counterfactual RAG, ICLR 2026](https://openreview.net/forum?id=9U51rOnGko) | Correlated evidence may overwhelm decisive evidence; arbitration and counterfactual evidence matter. | Wrong-reference and matched-irrelevant controls are essential, especially under speech uncertainty. |
| [MMSU, ICLR 2026](https://proceedings.iclr.cc/paper_files/paper/2026/hash/34e278fbbd7d6d7d788c98065988e1a9-Abstract-Conference.html) | Spoken understanding and reasoning exceed transcription alone. | Use semantic tasks to test task value, but audit human/synthetic speech, scoring, and license boundaries. |
| [AudioBench, NAACL 2025](https://arxiv.org/abs/2406.16020) | Public spoken QA and audio-language evaluation expose broad capability differences. | Reuse deterministic adapters where possible; do not rely on a service LLM judge for the primary claim. |
| [Audio2Tool, 2026](https://arxiv.org/abs/2604.22821) | Spoken tool use exposes acoustic and compositional failures with structured targets. | Use only the owner-admitted bounded leverage probe; do not expand SAEA into a general tool agent. |
| [AU-Harness](https://github.com/ServiceNow/AU-Harness) | Public adapters cover QA, intent, function calling, and long ASR tasks. | Audit and reuse adapters, not its experiment identity or any service-dependent evaluator. |

Required survey work before candidate qualification:

1. refresh the contextual-ASR prior matrix with exact code, data, model, and metric availability;
2. compare SAEA's roster-band and reflection path against the closest trained and training-free entity methods;
3. audit whether a published system already combines localized audio, own draft, retrieved reference, explicit
   verification/abstention, and harmful-edit accounting;
4. audit task carriers for natural versus synthetic speech, license, deterministic scoring, deleted items, and
   judge dependence;
5. state which external systems are reproducible baselines and which are architecture references only;
6. keep memory literature in a deferred successor survey unless a method actually changes this study's prior
   boundary.

The provisional gap is not a first-ever claim. It is that no currently verified runnable prior in the local
survey establishes the complete SAEA combination under a frozen black-box omni core: legal evidence
construction, speech-aware targeting, small and timed supply, audio-grounded verification/abstention, harmful-
edit control, and task-level transfer without parameter training.

## 12. Milestones and decision gates

| Milestone | Engineering deliverable | Research gate | Failure response |
|---|---|---|---|
| M0 — P2 closure | Terminal manifests, immutable scoring package, verdict | AFFIRM, COLLAPSE, or UNRESOLVED by registered rules | Narrow operator claim; schedule clean confirmation only under authority. |
| M1 — legal construction | Source manifests, versioned transforms, coverage report | Better legal coverage than metadata at bounded distractor/cost | Narrow to metadata-rich domains or stop construction expansion. |
| M2 — routing | Common flag/retrieval trace and oracle/legal routing ladder | Legal route retains useful oracle fraction | Retune once by preregistered family or stop full-chain scaling. |
| M3 — safe use | Consolidated verifier/admission policy | Net target gain with bounded HER/copying | Use simpler supply-only policy or stop reflection claim. |
| M4 — task value | One deterministic non-ASR task result | Same policy changes meaningful task outcome | Keep mechanism-only candidate; do not inflate scope. |
| M5 — prior closure | Baseline receipts and prior-difference matrix | No unaddressed stronger runnable prior | Reproduce, narrow, or stop candidate. |
| M6 — candidate package | Self-contained Stage-2A package | Owner judges candidate qualified for paper planning | Remain in bounded Stage-2A or sunset. |

## 13. Stop, narrow, and promotion rules

### Stop the current route if

- legal source construction cannot cover the errors that drive the oracle headroom;
- legal routing retains no useful fraction of oracle routing;
- wrong-reference copying or harmful edits remain unacceptable after the smallest guard set;
- a fixed pipeline matches the policy under the same information and resource envelope;
- a stronger runnable prior already establishes the same method and boundary;
- the only positive task result depends on gold-derived information, cross-item memory, or an unreproducible
  service.

### Narrow the claim if

- P2 collapses reflection into targeted bias;
- the legal effect exists only in metadata-rich or roster-rich domains;
- task value appears only for entity-sensitive outcomes;
- Audio2Tool succeeds but no natural-speech task transfers;
- the second model family does not preserve direction;
- a key rate remains denominator-guarded or statistically unresolved.

### Eligible for owner consideration as a qualified candidate only if

- one legal end-to-end SAEA policy survives construction, routing, supply, and use gates;
- the gain is attributable against strong fixed and irrelevant-evidence controls;
- harmful edit and wrong-reference behavior are bounded and fully reported;
- at least one meaningful task endpoint or a compelling mechanism endpoint survives;
- baseline receipts and prior-difference claims are complete;
- all discovery limitations, late definitions, exposure deviations, and negative results remain visible;
- the proposed confirmation is unread and belongs to a separately authorized paper repository.

## 14. Immediate handoff to engineering

The immediate sequence is:

1. do not touch the study working tree while the P2 block is active;
2. close P2 and publish the registered operator verdict with the metric-definition disclosure;
3. mirror the P2 metric amendment during the next GPU gap;
4. consolidate the current D7E guards and evidence-packet trace contract;
5. implement the legal construction ladder through existing evidence sources and transforms;
6. run oracle-routing before legal-routing scale-up, then close the routing gate;
7. consolidate the smallest legal consumption policy;
8. run SLURP first among task-value extensions, then the receipt-ready transfer carriers;
9. keep Audio2Tool bounded and firewall it from the main claim;
10. assemble the qualified-candidate package instead of opening parallel knowledge-study repositories.

The engineering objective is not to invent another agent stack. It is to make the current SAEA stack a better
scientific instrument: more legal coverage, better targeting, safer use, stronger task relevance, and cleaner
causal evidence.

## 15. Team organization and reporting contract

| Workstream | Primary responsibility | May proceed while a GPU arm is live? | Handoff condition |
|---|---|---|---|
| Research lead | Claim stack, preregistration, branch rules, boundary decisions, verdicts | Read-only planning outside the study tree | Every arm has one question, one changed factor, and mechanical decisions. |
| Harness engineering | E0/E1/E3/E5/E7/E8, trace and replay integrity | No study-tree edit; model-free design may proceed elsewhere | Recorded-response and negative-control suite pass. |
| Knowledge engineering | Legal source receipts, E2 transforms, coverage/distractor analysis | Source audit and model-free manifests only | Legal construction gate report with hashes and per-layer recovered fractions. |
| Routing engineering | E4 flag/retrieval implementations and oracle/legal routing ladder | Offline fixture work only | Opportunity-ledger recall/precision report and false-delivery taxonomy. |
| Task adapters | SLURP, approved transfer, conditional QA scoring | Adapter audit/model-free fixtures only | G1–G6 admission receipt and deterministic scorer test. |
| Independent evaluation | Frozen scoring, counterfactuals, statistical checks, claim audit | Yes, but no live result read outside the registered sequence | Reproducible report from immutable manifests, including negative results. |
| Operator | Clean-tree preflight, launch, process monitoring, terminal manifests, exposure accounting | Owns the live-flight freeze | Every attempt terminal; cost and deviations reconciled before handoff. |

Parallel work is allowed only when it cannot change a live arm's bytes, thresholds, prompts, metrics, or
interpretation. Literature review, source/license audits, deterministic fixture design, and task-adapter schema
work may overlap execution. Study-tree edits, registration changes, threshold tuning, and result-driven prompt
changes may not.

Every engineering handoff must report:

1. current milestone and gate status;
2. exact study commit, config/protocol hashes, and dependency receipts;
3. changed axis and factors proven unchanged;
4. dataset/carrier, split role, split identity hash, and inherited exposure;
5. model/tool contacts, calls, audio seconds, tokens, wall time, and failed-attempt cost;
6. preregistered primary and safety metrics with raw denominators;
7. correct-to-wrong, wrong-to-correct, wrong-reference, and unsupported-change transitions;
8. deviations, vehicle failures, and whether any result was read before a definition changed;
9. decision reached by the registered rule;
10. next safe action and any owner decision required.

No workstream may report “agent improvement” without identifying the legal source, speech-conditioned decision,
delivered packet, admission outcome, counterfactual baseline, and task transition that produced it.
