# Speech-Aware Evidence Acquisition: Supervisor Assessment and Stage-2A Continuation Plan

> **Document role:** Engineering plan. This is an owner-requested planning and assessment artifact;
> it is not a new execution contract and does not authorize model contact, a new carrier, a
> confirmatory-split read, Stage-3 work, publication, or any spend outside the authorities already in
> force. Every model/tool contact still requires its own pre-registered exposure row and valid
> `ExecutionPlan`.
>
> **Immediate operational rule (2026-08-16):** the P2 R-ladder resume was live when this plan was
> authored. Do not modify or commit anything in
> `studies/speech-aware-evidence-acquisition/` until the active block has stopped and every attempted
> arm has reached a terminal manifest state. Re-check the process and the exposure ledger; this note
> is not a live-status authority.

## 1. Supervisor verdict

### 1.1 Bottom line

Continue the study and extend its evaluation ladder without changing its identity, repository, or engineering
substrate.

The program direction is clear, the admitted study is legitimate, and the recent experiments have
identified a useful mechanism substrate rather than merely producing a collection of prompt tricks.
However, **deployment-legal small-roster entity correction is not by itself a strong enough doctoral
endpoint**. It is a component experiment: unusually good for causal diagnosis, but too narrow for the
main research claim. The remaining scientific object should be stated as:

> **Can the existing speech-aware evidence-acquisition system improve the task-relevant reliability of a
> frozen, API-only speech-omni model by deciding what speech evidence to revisit, what deployment-legal
> knowledge to construct and retrieve, how to supply it, and whether to adopt or reject the resulting
> revision?**

This question is specific, falsifiable, operationally bounded, and connected to the program thesis.
The entity-ASR work remains the first, mechanistically transparent rung of SAEA and the source of its current
causal evidence. Additional task rungs test the value of the same mechanism; they do not replace the study or
authorize a generic agentic-task claim. The current engineering decomposition remains:

- `OBS` supplies localized audio and a stable long-form substrate;
- `ORG` constructs legal, provenance-bound entity references;
- `SUPPLY` selects a small number of references and controls their timing and framing;
- `USE` verifies against audio, edits locally, abstains, and stops.

The paper-candidate question remains concentrated in `ORG × SUPPLY × USE`, with `OBS` held fixed
except for explicit ablations, but the reward and primary endpoint move upward by task: entity state
transitions for mechanism diagnosis, QA answer/evidence correctness, SLU semantic-frame or command
success, and tool-call/action success for the bounded agentic bridge.

### 1.2 Assessment by doctoral-training criterion

| Criterion | Assessment | Supervisor decision |
|---|---|---|
| Program direction | **Clear** | The north star, frozen-core boundary, speech-only scope, and reliability objective are coherent. |
| Research topic | **Clear after preserving SAEA and extending its task ladder** | Study speech-aware acquisition, legal evidence construction, targeted supply, verification, and stopping through the current system. |
| Scientific value | **High if the task ladder succeeds; modest if it remains ASR-only** | Spoken QA, SLU, and tool/action outcomes test whether knowledge control activates useful task capability rather than only changing transcript spelling. |
| Novelty position | **Promising but not yet publication-safe** | The recent survey finds no claimed audio + own draft + retrieved reference + abstaining verification combination, but much of the frontier census is abstract-level and must be localized into a prior-difference matrix. |
| Evidence maturity | **Good discovery evidence; not a qualified candidate yet** | Several mechanism and engineering claims are credible, but the legal method, cross-carrier transfer, and independent confirmation are still incomplete. |
| Engineering maturity | **Strong for Stage-2A** | The runtime, tracing, leakage controls, provenance tiers, replay vehicle, and failure guards are unusually well instrumented. |
| Paper readiness | **No** | P2 is unresolved, the legal-tier end-to-end chain is unproven, and no Stage-3 authority exists. |

### 1.3 What should and should not be claimed today

**Defensible now:**

1. Knowledge form and prompt framing are first-order variables for this frozen model.
2. A small coherent entity roster can outperform a large bag of contextual terms while using far
   fewer prompt tokens.
3. Oracle-selected names establish a static-bias upper-bound result on the frozen ten; they do not
   establish a deployment method.
4. A metadata-only roster is deployment-legal and directionally improves both macro and entity
   ledgers on the frozen ten, but the macro result is not statistically conclusive at `n=10`.
5. Raw token-logprob flagging is a poor localization signal for rare-entity errors in the observed
   traces; an entity/roster gate is operationally superior on the tested vehicle.
6. The replay vehicle can deliver references to localized windows and exercise accept/reject/abstain
   behavior after the D7 guard sequence.
7. The measured cross-call error-pattern KB does not cover the rare proper-name failures in the
   examined Earnings-21 reachability partition; this closes that implementation route for the
   current candidate, not every conceivable cross-call memory system.
8. The ASR rung provides a causal and safety instrument: it exposes whether evidence was supplied,
   copied, verified, adopted, or harmful before those mechanisms are evaluated in less observable
   downstream tasks.

**Not defensible yet:**

1. “External knowledge reliably improves speech recognition” as a general claim.
2. “Reflection is a different and better inference operator than static bias.” P2 is the deciding
   experiment and is not closed.
3. “The deployment-legal method achieves the oracle gain.” The legal roster recovers only part of
   the observed oracle effect.
4. “Acoustic exemplars work deployment-legally.” The strongest early exemplar flip had a
   gold-derived text label; the legal-label acoustic path remains open.
5. Cross-carrier, cross-task, cross-language, cross-model, or paper-level superiority claims.

## 2. Reliability audit of the current conclusions

Use the following grades only for the present model, serving stack, prompts, carriers, and registered
discovery splits.

| Conclusion | Grade | Why | What would strengthen or invalidate it |
|---|---|---|---|
| Large, unstructured contextual bags are inefficient and can be harmful | **Moderate–strong** | Repeated across doses/framings; the locked `n=10` run removed the earlier macro penalty but retained a roughly fourfold prompt-token burden. The correct statement is inefficiency and framing sensitivity, not universal toxicity. | Replicate under a second carrier and fixed format policy; invalidate the broad harm wording if a locked bag is consistently non-negative. |
| Small coherent form dominates large dose | **Strong discovery evidence** | Oracle names produced the best registered static-bias result on the frozen ten with a paired significant macro read and a large entity-ledger gain. | Still oracle-tier. A legal source with comparable coverage must reproduce the effect before it becomes a method claim. |
| Deployment-legal metadata roster helps | **Moderate** | Positive direction on both ledgers and concrete rare-name flips; macro `p=.19` at `n=10` is underpowered and not confirmatory. | Repeat on an independent carrier or larger legal discovery set; require call-level confidence intervals and correct-to-wrong analysis. |
| Prompt framing changes whether evidence is copied or verified | **Moderate mechanism evidence** | D4 screens showed large echo differences and typo copying only under the bias framing; wrong-reference controls at scale remain pending. | P2 must reproduce the framing interaction with pre-localize copy counts and wrong references. |
| Entity-aware roster-band localization is mechanically viable | **Strong engineering evidence, moderate scientific evidence** | D7E passed its pre-registered delivery gate after the defects were surfaced and guarded. Thresholds were tuned adaptively on reused discovery cases. | Freeze the implementation, report flag precision/recall and coverage on a non-tuning set, and ablate the gate components. |
| The replay controller improves task quality | **Unresolved** | Airworthiness, localized splicing, and bounded cost are demonstrated; aggregate/entity benefit has not been established. | P2 and then the legal-tier chain decide this. |
| Acoustic exemplars encode rare sound-to-spelling mappings | **Weak but interesting mechanism evidence** | One anchor entity flipped cleanly and common morphology did not; the label provenance was later downgraded to ceiling-tier. | Re-demonstrate with a legal document/metadata label, multiple entities, wrong-label controls, and call-level outcomes. |
| Cross-call error-pattern KB is not the right rare-entity source | **Moderate–strong for this route** | The registered reachability partition found no rare proper-name coverage in the cross-call stratum. | Do not universalize beyond the measured construction, corpus, and query definition. Reopen only if a materially different legal indexing source changes the coverage premise. |
| The method is novel | **Plausible, unqualified** | The survey found a credible gap and an apparently unclaimed three-way verification interface. However, several recent sources are abstract-only and executable prior parity is incomplete. | Close a claim-by-claim full-text prior-difference matrix and reproduce or bound the strongest same-boundary prior. |

### 2.1 Main validity threats

1. **Adaptive reuse of discovery cases.** The fast-three and frozen-ten calls have been inspected
   repeatedly while prompts, thresholds, sources, and guards evolved. They remain useful for
   engineering and mechanism discovery, but no longer behave like an independent validation set.
2. **Small call-level sample size.** Entity-token counts provide diagnostic resolution but do not
   create independent experimental units. Primary inference must remain paired at the call/query
   level; token-level significance must not replace it.
3. **Many screened variants.** The history contains multiple doses, forms, frames, windows, flag
   rules, and repairs. Final claims must be tied to pre-registered contrasts and effect sizes, not to
   the best observed cell.
4. **Ceiling/legal conflation.** A gold-derived span or reference makes an entire arm ceiling-tier.
   Wrong-reference controls test verification behavior, not selection legality.
5. **Format sensitivity.** Number rendering and casing can move WER without changing recognition.
   Frozen WER remains primary, but a pre-specified format-normalized secondary and entity state
   transitions are required.
6. **Single-system dependence.** Current evidence is tied to one quantized model and one serving
   stack. Stage-2 need not solve cross-model generality, but the candidate must state this scope
   explicitly.
7. **External-validity gap.** The strongest evidence is finance-domain long-form ASR. The study has
   not yet shown transfer to another real-speech task or that an entity repair changes an end task.
8. **Operations can contaminate science.** Mid-flight repository writes already caused a completed
   inference arm to fail manifest binding. Clean-tree and immutable-flight discipline are part of
   research validity, not merely operations hygiene.

## 3. Candidate decision and stop rules

### 3.1 Primary candidate

Keep one primary Stage-2 candidate:

**Task-aware knowledge control for a frozen speech-omni model, evaluated from speech fidelity to
task success.**

The candidate contains three nested claims:

- **C1 — control-mechanism claim:** targeted, provenance-bound supply plus verification/abstention
  controls knowledge adoption more safely than undifferentiated static context;
- **C2 — task-capability claim:** the same control abstraction improves at least two task levels
  beyond transcript WER, with task-native rewards and negative/oracle controls;
- **C3 — reliability claim:** task gain is not purchased through evidence copying, correct-to-wrong
  regressions, ontology/schema leakage, or uncontrolled cost.

The combined method claim is allowed only if all three survive. The ASR P2 result selects or rejects
one consumption operator for the higher-task ladder; it no longer decides the study's total value.
If the operator collapses, use the simplest non-harmful supply interface as the control and continue
to test whether task-aware organization/retrieval and reward produce downstream value. If every
higher-task rung is null, retain the ASR work as a bounded negative/component result rather than a
flagship candidate.

### 3.2 Secondary items

- Keep acoustic exemplars as an ablation or optional extension until they pass a legal-label test;
  do not make them part of the minimum method.
- Keep IC-001 interleaved listening/history compaction as a separate OBS candidate. It must not gate
  the knowledge candidate.
- Promote Spoken QA and SLU to required task-level rungs within the current speech-domain boundary.
- Keep Audio2Tool as the already-authorized bounded leverage probe only. It may show that knowledge
  control changes action structure; it does not expand this study's claim surface.
- Keep the agentic speech task system as a separate Stage-1 object in the umbrella. Do not merge it
  into this study without a new owner amendment.

### 3.3 Task ladder and scientific role of each rung

| Rung | Task and legal knowledge | Primary endpoint | Scientific role |
|---|---|---|---|
| L0 | Entity-dense long-form ASR; metadata/issuer documents | Entity state transitions, HER, macro WER, cost | Mechanism microscope and safety calibration; not the headline contribution |
| L1 | Spoken QA; inference-time-legal question context, retrieved passages, call/document evidence | Answer EM/F1, evidence support/citation correctness, abstention, answer-destroying regressions | Tests knowledge accessibility, organization, retrieval, and grounded use beyond transcription |
| L2 | SLU on SLURP; ontology, intents, slot types, permitted values | Semantic-frame exact match, slot F1, intent accuracy, command-level success | Tests whether controlled knowledge converts speech into structured task state on real human speech |
| L3 | Authorized Audio2Tool probe; tool registry, signatures, constraints | Exact tool call, argument/slot correctness, schema violations; WER secondary | Bounded bridge from knowledge control to action-shaped success; synthetic-speech and probe-scoped |
| L4 | Separate agentic task-system research object | Executed state transition, pass@1/pass^k, containment, reliability | Full agentic thesis; requires its own Stage-1 closure and future execution contract |

The ladder is not “run the same entity list on four datasets.” Each rung changes the legal knowledge
object and the reward while preserving one controller abstraction:

- ASR: names and document labels; reward = faithful speech/entity recovery;
- Spoken QA: retrieved passages and provenance; reward = supported answer correctness;
- SLU: ontology and permitted slot values; reward = correct semantic frame/command;
- agentic bridge: tool schemas and state constraints; reward = valid tool/action structure.

The main scientific question is whether a task-aware controller learns or executes different
`ORG/SUPPLY/USE` decisions under these rewards, and whether those decisions improve reliability more
than a fixed context-injection baseline.

### 3.4 Continue, collapse, reroute, and stop conditions

| Gate | Continue | Collapse/reroute | Stop the primary candidate |
|---|---|---|---|
| P2 operator gate | Verify framing retains repairs and materially lowers wrong-reference copying or harmful edits relative to bias | R1, R0-bias, and R2 are practically indistinguishable: remove “different operator” language and retain only targeted small-N supply | Wrong-reference copying remains high under verify framing or the controller increases harm without a recoverable benefit |
| Legal-source gate | Legal reference construction has usable routing recall and improves entity outcomes without unacceptable macro/HER regression | Coverage, not consumption, is limiting: reroute effort to legal source materialization and flag recall | Even oracle routing plus legal content cannot beat zero or metadata after the vehicle is frozen |
| Task-value gate | Spoken QA or SLU improves on a task-native endpoint with legal knowledge and no unacceptable reliability regression | Only ASR/entity metrics move: downgrade the method to a component result and redesign the task-aware policy | No higher-task gain after the legal interface and reward are frozen |
| Transfer gate | At least two task levels, including one independent real-speech carrier, show the predicted direction; bounded Audio2Tool may separately show action leverage | Value is task-specific: narrow the claim to the supported task and report the failed transfer | Gains disappear on every independent task or depend on gold-derived selection |
| Qualification gate | Frozen controller abstraction, task-native claims/nulls, baselines, cost, risk controls, statistical plan, and unread-confirmatory declaration are complete | Produce a negative/null qualified candidate if the cross-task mechanism question is answered cleanly | Evidence remains confounded after the planned legal and task-ladder tests |

## 4. Engineering continuation plan

Dependencies are strict. Do not start a later phase merely because GPU capacity is idle.

### Phase 0 — Protect and close the live P2 block

**Purpose:** preserve one-shot semantics and make P2 analyzable.

- [ ] Confirm the study worktree remains clean for the entire active flight; make no study-repo
  edits or commits while any P2 arm or manifest binder is alive.
- [ ] Confirm each attempted arm reaches a terminal manifest state; record failed/aborted spend and
  never silently overwrite an attempt directory.
- [ ] Resume only the arms named in `docs/arms/p2-rladder-resume.arms`; do not re-fly the completed
  sealed R0-bias inference.
- [ ] Salvage the sealed R0-bias attempt offline exactly once, with an explicit receipt binding raw
  trace, output, analysis revision, and original aborted manifest.
- [ ] Run the pre-registered P2 analysis only after all arms are terminal. Do not inspect or report
  interim WER/entity outcomes.
- [ ] Report both co-primary call-level reads, HER, recoverable-information ratio, pre-localize echo
  and wrong-reference copy counts, per-term state transitions, format-normalized secondary, cost,
  and all deviations.
- [ ] Apply the pre-registered `AFFIRMED` versus `TAXONOMY COLLAPSE` branch mechanically.

**Exit artifact:** a single English P2 verdict in the study readiness layer, with immutable run
identities and a decision that explicitly supersedes incompatible 2026-08-14/15 wording.

### Phase 1 — Consolidate the active truth

**Purpose:** remove the present handoff ambiguity before new scientific arms.

- [ ] Update `wiki/Research-Objective.md` with the P2 decision, the legal-tier blocker, and one next
  action; keep it within the HOT-page budget.
- [ ] Update the study experiment index with formal records or explicit routing to the registered
  bounded probes; do not leave “one formal experiment” as the only visible lifecycle fact if P2 has
  become load-bearing.
- [ ] Supersede the candidate freeze in place or issue one consolidated successor. Do not add a
  fourth layer of amendments.
- [ ] Reconcile the following phrases everywhere they remain active: “all static supply fails,”
  “deployment-legal acoustic exemplar,” “reflection is unbounded,” and “knowledge dimensions are
  closed.” Each must match the P2 verdict and the legality doctrine.
- [ ] Record the exact discovery exposure already incurred and state that the fast-three/frozen-ten
  are tuning sets, not independent validation.
- [ ] Run the study suite and umbrella context/manifest gates before committing the consolidation.

**Exit criterion:** a new engineer can read the HOT state, consolidated candidate, legality doctrine,
and exposure ledger and identify exactly one next experiment without reading the amendment chain.

### Phase 2 — Close the ASR mechanism rung without turning it into the thesis

**Purpose:** select a safe, interpretable control interface that higher task rungs can reuse. This
phase is bounded mechanism calibration; it is not allowed to expand into an indefinite search for
the perfect entity roster.

#### 2A. Legal knowledge construction

- [ ] Materialize the tier-3 document-label source from call metadata to pinned issuer documents.
  Freeze source URLs/identifiers, retrieval date, content hashes, parser revision, casing rule, and
  coverage before any result is read.
- [ ] Prohibit reference transcripts, test annotations, gold-guided term selection, and gold-derived
  casing by executable checks.
- [ ] Produce a coverage report by call and entity class: metadata-only, pinned-document reachable,
  self-derived, and unreachable.
- [ ] Treat source coverage as a scientific variable. Do not hide missing legal labels by evaluating
  only the cases that have them.

#### 2B. Routing-recall gate

- [ ] First run an offline/oracle-routing decomposition: oracle span routing with legal references
  versus the frozen S1 roster-band router with the same legal references.
- [ ] Measure span recall, candidate recall, false-fire rate, and delivered-reference-on-true-error at
  a fixed per-call flag budget.
- [ ] If oracle routing converts but S1 loses most of the effect, stop consumption tuning and invest
  only in localization.
- [ ] Ablate the smallest defensible locator family: roster/phonetic band, intra-call
  self-consistency, and the current rarity term. Add blank-audio grounding only if the API-shaped
  implementation can be pinned without hidden-state access and earns its extra calls.

#### 2C. Legal consumption experiment

- [ ] Freeze the P2-selected interface and compare legal-tier zero, metadata roster, document roster,
  and targeted verify/replay under identical serving and scoring.
- [ ] Keep an oracle names/reference arm as a ceiling only; label both `span_source` and
  `reference_source` in every table.
- [ ] Use wrong-reference and no-use controls to separate supplied, attended, copied, verified, and
  adopted evidence.
- [ ] Pre-register the minimal clinically/scientifically meaningful effect and the maximum acceptable
  HER/correct-to-wrong regression before launch.
- [ ] Report call-level effect sizes and uncertainty even if the significance threshold is missed.

**Exit decision:** either a frozen legal control interface, a coverage-limited diagnostic, or a clean
negative result. No additional prompt search is permitted merely because the legal arm is null. Once
the supply/verification behavior and harm envelope are understood, move to task-native rewards.

### Phase 3 — Run the task-value ladder

**Purpose:** test whether knowledge control creates value beyond transcript spelling. ASR metrics are
secondary diagnostics in this phase; every rung has a task-native primary endpoint.

#### 3A. Spoken QA — knowledge accessibility and grounded use

- [ ] Re-check SLUE-SQA-5's deleted-pair/restoration feasibility before first task touch. If the
  official scorer silently removes answer-destroyed examples, define a failure-preserving evaluation
  or stop and document why the carrier cannot answer the question.
- [ ] Register an untouched discovery/dev identity and freeze the legal knowledge available to each
  question: supplied passage, retrievable passage corpus, metadata, or no external evidence. Gold
  answers and answer-derived retrieval never enter runtime.
- [ ] Compare at minimum: direct audio answer; transcript-then-answer; legal retrieval + answer;
  task-aware verify/iterate; mismatched evidence; oracle evidence ceiling; no-use control.
- [ ] Make answer EM/F1 and supported-answer correctness primary. Report ASR/entity state only as a
  mediator: identify wrong transcript/correct answer, correct transcript/wrong answer, and
  evidence-induced answer regression.
- [ ] Trace the complete causal chain: speech observation -> query construction -> retrieved evidence
  -> evidence admission -> answer -> abstention/stop. A QA gain without evidence-use verification is
  insufficient.
- [ ] Keep `spoken-squad` as a fallback diagnostic only after its unresolved license is cleared; do
  not make a publication-bearing claim depend on a dataset with unspecified terms.

#### 3B. SLU — real-speech structured task success

- [ ] Use SLURP under the existing owner amendment. Freeze an official split and scorer before any
  run; use the shipped real human speech and the inference-time-available ontology.
- [ ] Treat intent labels, slot types, allowed values, device/user catalogues, and command schema as
  distinct legal knowledge classes. Do not derive a per-example candidate list from the gold frame.
- [ ] Compare direct speech-to-frame, static ontology, task-aware retrieval, and
  verify-with-abstention under matched prompts and serving.
- [ ] Make semantic-frame exact match or command-level success primary; report intent accuracy, slot
  F1, invalid-value rate, over-correction, and ASR/entity changes as decompositions.
- [ ] Include ontology-mismatch and wrong-value controls. The controller must reject a plausible but
  illegal slot value rather than merely copy the nearest catalogue entry.
- [ ] Freeze the control abstraction learned on Earnings-21/QA. Only carrier adapters, legal
  knowledge schemas, and task reward may change; per-dataset policy redesign is not transfer.

#### 3C. Tool-shaped agentic leverage — bounded, secondary

- [ ] Run only the already-authorized Audio2Tool roster probe after verifying the local split,
  non-commercial-license firewall, query-level clustering, and the existence of an independently
  registered noise source. Omit the noisy axis if that source does not exist.
- [ ] Make exact tool-call/argument success primary and ASR quality secondary.
- [ ] Treat multiple renditions of one query as clustered observations; do not count them as
  independent queries.
- [ ] Label the result synthetic-speech and probe-scoped. It can demonstrate action leverage but
  cannot establish real-speech generalization.
- [ ] Do not build a full-duplex backend, executed environment, or new agentic carrier in this study.
  Those belong to the separately opened Stage-1 agentic task-system object.

**Exit criterion:** at least one of Spoken QA or SLU improves on a task-native endpoint with legal
knowledge, and the other provides either supporting transfer or a well-instrumented null. The
Audio2Tool result, if run, answers only whether controlled knowledge can change a tool-shaped output.

### Phase 4 — Baseline and novelty closure

**Purpose:** make the candidate defensible to a skeptical reviewer.

- [ ] Build a claim-by-claim prior-difference matrix for RECOVER, Voice Memory, Lei et al.'s entity
  gate, DeRAGEC, contextual-biasing systems, and the closest audio-grounding/reflection work.
- [ ] For every load-bearing citation, prefer full text and register the local receipt. Abstract-only
  evidence may motivate an experiment but must not carry the final novelty claim.
- [ ] Separate: artifact exists; reported number reproduces; method runs under this API-only,
  zero-training boundary.
- [ ] Reproduce the strongest runnable same-boundary baseline when possible. Otherwise freeze an
  `INCONCLUSIVE_BASELINE_NOT_READY` receipt with the exact blocker and compare through official
  scorers plus published numbers without implying a direct reproduction.
- [ ] State the proposed delta narrowly: not “first knowledge-enhanced speech agent,” but the exact
  cross-task control abstraction—legal knowledge construction, task-aware retrieval/supply,
  audio/evidence verification, abstention/stopping, provenance, and reliability accounting—that
  survives the experiments.
- [ ] Run one bounded literature delta immediately before candidate qualification; do not reopen the
  retired full Stage-1 survey unless new evidence triggers a contract invalidation condition.

### Phase 5 — Assemble the qualified candidate package

**Purpose:** reach the Stage-2 endpoint without crossing into Stage-3.

- [ ] Freeze the improvement claim, scope, null hypothesis, mechanism diagram, minimum method, and
  ablation graph.
- [ ] Freeze baselines and all executable revisions, prompt/config hashes, source-materialization
  hashes, split identities, and analysis code.
- [ ] Include effectiveness, reasonableness, and efficiency: macro/task metrics, entity metrics,
  wrong-to-correct and correct-to-wrong, HER, tails, calls/tokens/latency/GPU/CPU, evidence supplied
  and adopted, and unit gain.
- [ ] Provide a complete exposure statement: which discovery/dev identities were read, how adaptive
  tuning occurred, and which confirmatory identities remain unread.
- [ ] Provide the Stage-3 confirmatory design without executing it: primary endpoint, sample unit,
  power/sensitivity analysis, multiplicity plan, stop rules, and replication carriers.
- [ ] Submit the package for owner qualification. A positive, null, or negative candidate is allowed;
  ambiguity is not.
- [ ] Do not create a paper repository or run confirmatory work without
  `OWNER_GO_AND_PAPER_EXECUTION_CONTRACT`.

## 5. Research questions still requiring investigation

### Must answer before candidate qualification

1. Does verify-with-abstention actually resist wrong references better than bias framing at call
   scale, or were the D4 differences small-screen artifacts?
2. How much of the oracle names effect is reachable from legal metadata and pinned documents without
   gold-guided selection?
3. Is the bottleneck legal label coverage, flag localization, model verification, or splice/adoption?
   Report a recovered-fraction decomposition for each layer.
4. At a fixed flag budget, what are the precision, recall, coverage, and HER trade-offs of the frozen
   entity locator?
5. Does knowledge control improve answer correctness or structured task success when WER does not
   improve, and which intermediate state explains that gain?
6. Which knowledge representation is appropriate at each task level: entity roster, document
   passage, ontology/slot catalogue, or tool schema—and can one controller operate over all of them?
7. Does the frozen method transfer to a real-speech carrier with different task structure?
8. What is the strongest same-boundary prior, and which part of the proposed method remains a genuine
   delta after full-text comparison?

### Important, but may be deferred to Stage-3 or a separate study

1. Cross-model and quantization robustness.
2. Multilingual entity correction beyond the current carriers.
3. Privacy, licensing, and staleness policies for real deployment knowledge stores.
4. Learned versus training-free detectors; learned detectors are outside this study's method boundary
   but are useful ceiling references.
5. Full level-E, real-human-speech agent benchmarks. The umbrella's agentic task-system Stage-1 object
   owns this question.
6. Long-horizon reward-guided policy optimization after the fixed candidate method is qualified.

## 6. Team organization and handoff contract

No worker may both tune an arm and independently certify its final statistical interpretation.

| Workstream | Owner role | Deliverable | Handoff gate |
|---|---|---|---|
| Flight operations | Experiment operator | Terminal manifests, immutable attempt inventory, spend/deviation receipt | Evaluator confirms all registered arms are terminal before reads |
| Evaluation/statistics | Independent evaluator | Locked analysis output, call-level inference, HER/state transitions, branch decision | Research lead signs that the pre-registered branch was applied without reinterpretation |
| Legal source construction | Data/provenance engineer | Hashed materialization, coverage ledger, leakage checks | Boundary reviewer confirms no gold-derived selection or casing |
| Localization | Retrieval/algorithm engineer | Frozen flagger, ablations, fixed-budget precision/recall report | Evaluator approves thresholds before legal consumption run |
| Runtime/controller | Core engineer | Frozen P2-selected interface, guards, trace completeness, tests | Operator confirms byte-identical config and clean-tree preflight |
| Spoken QA | QA/evidence engineer | Legal retrieval contract, answer/evidence scorer, causal trace, negative/oracle controls | Boundary + statistics review before first QA contact |
| SLU | Semantic-task engineer | SLURP split/scorer parity, ontology contract, frame/slot/task metrics | Boundary + statistics review before first SLU contact |
| Agentic bridge | Tool-task engineer | Audio2Tool probe contract, clustered query analysis, schema/action metrics | Owner-amendment and license review before first probe contact |
| Literature/positioning | Research survey lead | Full-text receipts and prior-difference matrix | Research lead approves claim wording before qualification |
| Governance | Umbrella maintainer | HOT/current consolidation, experiment index, context gates | Owner reviews the qualified-candidate request |

### Required progress report for every phase

Each handoff is one short English report containing:

1. decision requested;
2. authority and registered experiment IDs;
3. exact code/config/data/model/artifact identities;
4. results separated into effectiveness, reasonableness, and efficiency;
5. deviations and exposure;
6. which claim is supported, weakened, invalidated, or still unresolved;
7. next gate and explicit actions that remain prohibited.

## 7. Definition of Stage-2A completion

This plan is complete when all of the following are true:

- [ ] P2 has a terminal, pre-registration-faithful verdict.
- [ ] The active research question and candidate wording are consolidated and self-contained.
- [ ] A deployment-legal method has either passed its frozen gate or produced a clean negative result.
- [ ] The locator, source, delivery, verification, and adoption contributions are decomposed.
- [ ] Spoken QA and SLU have task-native, pre-registered reads; at least one shows legal-knowledge
  value beyond transcript WER, and any null rung is explained without post-hoc retuning.
- [ ] The Audio2Tool leverage probe is either completed within its bounded authorization or formally
  skipped with the blocker recorded; it is not a qualification gate by itself.
- [ ] The strongest same-boundary prior is reproduced or precisely bounded.
- [ ] The candidate package includes task success, evidence grounding, reliability, harm, and
  cost—not only mean WER.
- [ ] Confirmatory identities remain unread and Stage-3 execution has not begun.
- [ ] The owner can decide `QUALIFY`, `QUALIFY_NEGATIVE`, `REROUTE`, or `STOP` without requesting
  another exploratory prompt sweep.

## 8. Provenance and invalidation

This assessment is based on the active program state and the following targeted evidence:

- `wiki/Research-Objective.md` and `wiki/Project-Thesis.md`;
- the consolidated execution contract and study experiment index under
  `wiki/experiments/speech-aware-evidence-acquisition/`;
- study readiness verdicts dated 2026-08-14/15 for KC/KX, P1, MM, N10, legality, candidate freeze,
  and rectification;
- the registered P2 arms and append-only exposure ledger;
- the 2026-08-14 entity-flag survey and 2026-08-15 agentic task-system survey;
- the 2026-08-15 owner amendment admitting the bounded Audio2Tool probe and SLURP carrier while
  opening the agentic task system as a separate Stage-1 object.

Reassess this plan if P2 changes the operator taxonomy, a stronger runnable same-boundary prior is
found, the legal materialization cannot satisfy the information boundary, the study scope changes,
or the owner issues a new execution/paper contract.
