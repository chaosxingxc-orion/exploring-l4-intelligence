---
title: "Shared standard: black-box agent harness, baseline reproducibility, and model selection"
date: "2026-08-16"
status: "DRAFT_FOR_OWNER_REVIEW__NO_NEW_EXECUTION_AUTHORITY"
applies_to:
  - "speech-aware evidence acquisition continuation and extension"
  - "interleaved perception, reasoning, and revision"
  - "agentic full-duplex speech interaction"
program_fit: "TF-Strict reward-guided external control around frozen speech-capable omni cores"
literature_cutoff: "2026-08-16"
---

# Black-Box Agent Harness and Experimental Standard

## 0. Supervisory verdict

The three proposed topics should share one experimental substrate. The substrate is not incidental software:
it is the instrument that makes the research claim falsifiable. The core model is treated as an opaque,
replaceable service. The object allowed to improve is the external policy that observes public inputs and
outputs, manages typed state, chooses the next action, invokes tools, verifies outcomes, and accepts or rolls
back external changes.

The defensible program-level claim is therefore:

> Under a frozen black-box model contract, can a versioned and replayable harness systematically improve
> verified spoken-task outcomes through reward-guided external control, and can the improvement be separated
> from model choice, extra exposure, extra computation, evaluator leakage, and unreproducible services?

This framing survives only if four conditions hold:

1. every load-bearing baseline is locally reproducible or is replaced by a behaviorally equivalent native
   baseline with a documented difference;
2. the experiment freezes all factors other than the policy intervention during causal comparison;
3. model selection is capability-driven and preregistered rather than chosen after viewing task scores; and
4. every gain can be replayed from an event ledger and attributed to a bounded policy action.

The harness must not become a vague collection of agents. Its scientific kernel is a small action space,
explicit reward and constraints, immutable run manifests, deterministic replay, and counterfactual removal.
This document is a Stage-1 design standard only. It does not authorize a new study repository, model contact,
dataset download, service call, or live experiment.

## 1. Adversarial self-check: rounds four through eight

### Round 4 — baseline-availability prosecution

**Attack.** The proposals cite recent systems whose papers, code, data, model weights, and evaluator services
have different availability. A paper with a GitHub link is not necessarily reproducible. Some repositories
require commercial APIs, unpublished voices, manual downloads, separate incompatible environments, or an LLM
judge. If those systems are called baselines without reproducing their behavior, the comparison is rhetorical.

**Finding.** This attack succeeds. The proposals must distinguish artifact availability from scientific
comparability. Published systems may serve as architecture references, adapter sources, or external ceilings,
but only a locally smoke-tested implementation can be a load-bearing baseline.

**Revision.** Introduce the reproducibility classes in Section 5. Every baseline receives an availability
receipt before it receives a result row. R0 and R1 baselines may support primary claims. R2 systems are
sensitivity or external-reference comparisons until their dependencies are frozen. R3 systems remain related
work only.

### Round 5 — experimental-standardization prosecution

**Attack.** An agentic harness creates many degrees of freedom: prompts, stopping rules, number of calls,
retrieved tokens, audio overlap, retry policy, evaluator choice, task order, state lifetime, and failure
recovery. A positive result can be manufactured by tuning the whole stack on the test set or by giving the
agent more observations than the baseline.

**Finding.** This attack also succeeds. Logging is necessary but insufficient; the experiment needs a frozen
factorization and a campaign state machine. The Project Thesis also requires a specific resource order:
ceiling-seeking discovery first, consolidation second, and equal-budget comparison only after the mechanism is
known. Treating equal budget as the first gate would prematurely reject mechanisms whose value appears only
before cost reduction.

**Revision.** Use the phased protocol in Section 8. Discovery may spend unequal compute, but it cannot support
the final causal claim. Consolidation freezes the smallest surviving policy. Equal-budget and equal-exposure
comparisons then determine whether the policy itself adds value. Test-set access never drives policy changes.

### Round 6 — model-selection prosecution

**Attack.** A single convenient model can make a harness look effective. Q4 and Q8 variants of the same model
are not independent model replications. A runtime can expose only part of a model's official capability. A
closed API can silently change. Selecting a second model after seeing favorable scores is model-level
p-hacking.

**Finding.** This attack succeeds. The current Qwen Q4_K_M and Q8_0 artifacts are valuable for quantization
sensitivity, but they are one model family. The official Qwen stack also exposes different features across
Transformers, vLLM, hosted realtime APIs, and the current local llama.cpp path. A model name is therefore not a
sufficient experimental identity.

**Revision.** Freeze `model snapshot x precision x processor x runtime x endpoint capability surface` as one
factor. Select replication families before confirmatory results, using the capability and governance matrix in
Section 6. Never call an embedding model or an unevaluated reasoning checkpoint a replication core merely
because it is already downloaded.

### Round 7 — harness-versus-compute prosecution

**Attack.** The proposed method may win because it makes more calls, sees more audio, retains more text, uses a
stronger evaluator, retries failures, or calls a second model. “Agentic” can become a label for unbounded
test-time compute.

**Finding.** This is the central causal threat. The black-box restriction does not by itself control
computation. A harness improvement is scientifically meaningful only when its action policy beats strong
non-agentic schedules on a quality–cost frontier and survives a later matched-budget comparison.

**Revision.** The budget governor accounts for model calls, input/output tokens where exposed, processed and
unique audio seconds, wall time, concurrent model seconds, tool calls, retries, storage growth, and service
cost. A retry is a call, a discarded output is an output, and speculative synthesis is compute. Discovery and
matched-budget conclusions are reported separately.

### Round 8 — surviving formulation

After the attacks, the surviving research contribution is not “use an agent to improve an omni model.” It is:

> Design and validate external control policies whose decisions are observable, reward-grounded, replayable,
> portable across conforming black-box endpoints, and better than task-native deterministic and compute-matched
> controls on verified speech or spoken-language outcomes.

The three topics differ only in the policy state and time horizon:

| Topic | Persistent state | Action horizon | Core controlled decision |
|---|---|---|---|
| Knowledge construction/supply/use | Per item over a frozen campaign artifact | Knowledge interface | observe, organize, query, retrieve, pack, verify, stop |
| Interleaved revision | Within one item | Long-context inference | observe, patch, compact, stop, answer |
| Full duplex | Causal event time | Real-time interaction | listen, arbitrate, speak, cancel, repair, commit |

Cross-episode experiential memory is not one of the three current proposal objects. It is a deferred successor
study group. The shared structure is a strength only if state leakage between the current knowledge artifact,
within-item revision state, and real-time dialogue state is prohibited by tests.

## 2. Black-box scientific contract

### 2.1 Allowed observations

The harness may rely on only the interface information that a realistic frozen API can expose:

- submitted text, audio, and declared tool schemas;
- returned text, audio, tool calls, public finish reasons, errors, and timestamps;
- request parameters and model/endpoint version identifiers when the provider exposes them;
- external verifier outputs, environment state, and harness-owned state within the declared lifetime;
- token or cost accounting only when it is exposed consistently, otherwise an explicitly declared estimate.

### 2.2 Forbidden load-bearing access

No primary method or claim may require weights, gradients, activations, hidden states, attention, internal
confidence, undocumented logits, or guaranteed token log-probabilities. Local runtime diagnostics may explain
a failure but cannot select actions in the reported black-box method. Gray-box results receive a separate label
and cannot rescue a failed black-box hypothesis.

### 2.3 Experimental identity

Every run identity is the immutable tuple:

`task carrier x split x exposure ledger x model artifact x precision x processor x runtime x endpoint`

`capabilities x policy version x prompt envelope x verifier version x budget regime x seed x item order`

Changing any field creates a new cell. Results from different cells are never silently pooled.

### 2.4 Policy portability

The policy reads and emits typed public events. Model-specific formatting lives in an adapter. The policy must
not branch on a model name except through declared capability negotiation. If a model lacks a required
capability, the run is unsupported rather than repaired with hidden model-specific logic.

### 2.5 Knowledge-versus-memory lifetime rule

For the current knowledge-study family, the campaign knowledge artifact is built from predeclared authorized
sources and frozen before confirmatory evaluation. Query-time evidence state resets after each item or governed
session. Evaluation outcomes cannot write or modify state that is visible to a later evaluated item. Persistent
experience writes, consolidation, retention, forgetting, retirement, and continual transfer belong to the next
memory-study group and require a separate proposal and experimental standard extension.

## 3. Harness architecture

### 3.1 Required modules

| Module | Responsibility | Research safeguard |
|---|---|---|
| `ModelAdapter` | Normalize request, response, stream, cancellation, and tool events. | Keeps the policy independent of model internals. |
| `CapabilityProbe` | Produce a signed capability receipt for the exact endpoint. | Prevents assumed streaming/audio/tool support. |
| `TaskAdapter` | Load one frozen carrier and expose legal observations and verifiers. | Prevents task-specific leakage into the core. |
| `Policy` | Choose one typed external action from the current state. | Defines the actual intervention. |
| `BaselineRegistry` | Resolve pinned baseline manifests and availability classes. | Prevents moving or fictional baselines. |
| `BudgetGovernor` | Account for and enforce exposure and compute regimes. | Separates policy gains from extra compute. |
| `EventLedger` | Append causally ordered observations, actions, outputs, costs, and hashes. | Makes runs auditable and replayable. |
| `Verifier` | Compute executable or label-grounded outcomes. | Keeps reward independent of self-evaluation. |
| `Evaluator` | Produce frozen task and diagnostic metrics. | Separates online control reward from held-out evaluation. |
| `ReplayEngine` | Reconstruct runs with virtual time and recorded responses. | Tests determinism without model contact. |
| `CounterfactualRunner` | Remove, replace, or reorder one policy action. | Attributes outcomes to the claimed mechanism. |
| `ArtifactStore` | Store manifests, traces, patches, audio maps, and reports by content hash. | Prevents post-hoc artifact mutation. |

The architecture may borrow modular task/model/scorer ideas from Inspect AI and audio-task coverage from
AU-Harness, but the program needs a smaller speech-specific substrate with stricter exposure, event-time, and
counterfactual contracts. Importing a large framework must not weaken those contracts.

### 3.2 Core event schema

Every event contains at least:

- `run_id`, `episode_id`, monotonic `event_id`, and parent event IDs;
- event time and wall-clock time, with the clock source declared;
- observation interval or source span available at decision time;
- policy action, policy version, and bounded rationale code;
- model request/response content hashes and endpoint receipt;
- resource deltas, retry ancestry, cancellation state, and failure class;
- verifier result, state transition, and commit/rollback status.

Free-form chain-of-thought is neither required nor stored. The harness records decision codes, evidence
references, and externally checkable state transitions.

### 3.3 No hidden repair rule

Task- or model-specific fixes must enter one of three auditable locations: an adapter, a frozen policy variant,
or a task verifier. A new conditional added after inspecting test failures creates a new policy version and
invalidates the old confirmatory run.

## 4. Systematic improvement loop

The common improvement loop is:

1. **Observe:** expose only currently legal task and audio evidence.
2. **Propose:** let the frozen policy choose a typed next action.
3. **Execute:** call the same black-box endpoint or external tool under the budget governor.
4. **Verify:** use executable state or frozen labels where possible; isolate any LLM judge.
5. **Attribute:** replay without the selected state/action or with a matched deterministic alternative.
6. **Update permitted external state:** admit only evidence-supported changes within the topic's declared
   lifetime; never update model parameters.
7. **Regression gate:** test hard cases, privacy/safety constraints, and prior successful episodes.
8. **Accept or roll back:** version every accepted policy or state change.

Online feedback used by the policy and held-out metrics used by the researcher must be different channels.
Test labels, judge rationales, and aggregate test scores never enter the policy state. The current knowledge
proposal prohibits outcome-derived cross-episode writes entirely; future memory studies must define their own
development-stream and evaluation boundary.

## 5. Baseline reproducibility standard

### 5.1 Availability classes

| Class | Evidence required | Permitted scientific role |
|---|---|---|
| R0 — native deterministic | Program-owned implementation, pinned dependencies, local unit/replay tests, no undeclared network dependency. | Load-bearing baseline and causal control. |
| R1 — reproduced external | Official code and required data/weights are available under usable terms; exact revision is pinned; an independent local smoke run and metric check pass. | Load-bearing external baseline after receipt. |
| R2 — conditionally reproducible | Official implementation exists, but execution depends on commercial APIs, manual assets, unfrozen services, separate judges, or material adapter repair. | Sensitivity analysis, adapter source, or external reference; not primary until dependencies freeze. |
| R3 — descriptive only | Paper only, broken/missing repository, unavailable data/weights, or insufficient instructions. | Related work or conceptual ceiling only. |

Availability and comparability are separate columns. A runnable native full-duplex model may be R1 for
availability but scientifically incomparable to a training-free wrapper because it changes the trained core.

### 5.2 Required availability receipt

Before a baseline enters a table, record:

- paper and official repository URLs;
- repository commit, release, license, and access date;
- data, weights, prompts, preprocessing, and evaluator availability;
- required hardware, services, API versions, accounts, and expected cost;
- exact install and run entry point;
- smallest smoke item, expected output schema, and locally observed result;
- deviations from the paper and whether each deviation changes scientific comparability.

“Code available” without a successful smoke receipt remains R2 or R3.

### 5.3 Current evidence map

This is a Stage-1 availability judgment, not a claim that any external baseline has been reproduced locally.

| Artifact | Current availability judgment | Consequence for the proposals |
|---|---|---|
| EvoMemBench, A-MEM, EvoLib, and EvolveMem | Deferred: official artifacts vary from R1 candidates to R2 service-dependent implementations, but their cross-episode or self-evolving object belongs to the next memory-study group. | Boundary/prior evidence only; not baselines for the current SAEA continuation. |
| Adaptive retrieval / Counterfactual RAG | Paper and some implementation availability varies; methods establish retrieval-necessity, efficiency, and correlated-evidence controls. | SAEA prior-difference and native R0 ablation source; reproduce only after a receipt. |
| WavRAG / Google Speech-to-Retrieval | WavRAG establishes trained audio retrieval; Google's SVQ dataset is public while the production S2R method is a reference architecture. | Audio-retrieval prior and carrier source, not equal-method TF-Strict baselines. |
| AU-Harness | R2 now, potentially R1 after adaptation: Apache-2.0 code covers speech QA, intent, function calling, long ASR, and other tasks, but endpoint and LLM-judge configuration can be service-dependent. | Reuse task adapters and deterministic metrics where legal; retain the program ledger and policy layer. |
| AudioMarathon | R2: official code and multi-model scripts exist, but environments are model-specific and much of the suite is outside the speech-only boundary. | Audit only speech subsets; do not treat the whole benchmark as in scope. |
| VoiceGiraffe | R3 at the literature cutoff: the paper-linked repository was unavailable when checked. | Motivation only until a verifiable release appears. |
| LibriSpeech-Long | R1 candidate: official derived long-form speech code/data path is public and bounded. | Useful long-form diagnostic carrier; insufficient alone because it is transcription-centric. |
| Full-Duplex-Bench v1/v1.5 | R2 pending local smoke: code, static data, server-client inference, and metrics are public. | Best first external interaction compatibility target after the R0 virtual-time suite. |
| Full-Duplex-Bench v2/v3 | R2: code and data are public, but the live paths require Node/WebRTC or LiveKit, provider APIs, ASR, and sometimes an LLM judge. | External dynamic/tool benchmark after deterministic local validation; never the sole primary evidence. |
| FD-Bench | R2: dataset and pipeline are public, but model-specific stacks, generated speech, and a nonstandard license require audit. | Optional offline stress suite; not a default load-bearing baseline. |
| HumDial-FDBench | R2 pending adapter/license/data receipt: public test data, scenarios, and protocol exist. | Valuable natural interruption/rejection panel after leakage and execution audits. |
| tau2-bench / tau-Voice | Text core is an R1 candidate; voice path is R2 because it depends on realtime providers plus TTS/STT services and provider-specific assets. | Use task-state verification concepts; treat voice scores as service-dependent reference cells. |
| Moshi and other trained native duplex models | R1 candidates for availability, but reference ceilings for comparability. | They cannot prove the external policy effect because the trained core differs. |

## 6. Standardized model selection

### 6.1 Model roles

| Role | Selection rule | Claim scope |
|---|---|---|
| M0 — discovery anchor | Existing pinned and operational speech-omni artifact with sufficient task headroom. | Mechanism discovery on one frozen stack. |
| M0q — quantization/runtime audit | Same model family under another precision or serving runtime. | Sensitivity only; never cross-model replication. |
| M1 — open replication family | Different model family, pinnable weights/runtime, usable license, and required black-box capabilities; selected before confirmatory results. | Portability of the frozen policy. |
| M2 — closed frontier reference | Versioned commercial endpoint with declared capabilities and cost, if separately authorized. | Time-stamped external reference, never the sole load-bearing result. |
| MO — oracle/diagnostic | Transcript oracle, span oracle, or evaluator model isolated from the acting path. | Headroom or attribution only. |

### 6.2 Current anchor decision

For any future owner-authorized discovery campaign, the existing Qwen3-Omni-30B-A3B-Instruct GGUF Q4_K_M
artifact served by the pinned local llama.cpp path is the presumptive M0 because it is the program's current
operational black-box anchor. The Q8_0 artifact is M0q. The local asset lock records their provenance, hashes,
runtime, memory fit, speed difference, and a bounded eight-slice transcript comparison.

This is not a permanent endorsement and does not authorize model contact. It is a standardization decision:
do not change the anchor merely because another local artifact is newer or scores better on an exploratory
subset. Q4-versus-Q8 effects must be labeled quantization/runtime effects. `nemotron3-nano-omni-nvfp4` requires
its own speech capability and serving audit before it can be an M1 candidate. `omni-embed-nemotron-3b` is an
embedding component, not an acting omni core.

The official Qwen release confirms that the Instruct model supports audio/text input and text/audio output,
but the exposed surface varies by runtime; for example, the official vLLM serving path currently documents
thinker-only service behavior. The capability receipt, not the model card headline, defines the experimental
cell.

### 6.3 Capability matrix

Score each exact endpoint as `native`, `emulated`, `unsupported`, or `unverified` for:

- audio input, text input, text output, and audio output;
- long-audio limits and processor truncation behavior;
- streaming input, streaming text/audio output, and cancellation acknowledgment;
- tool schema submission, structured tool calls, and tool-result continuation;
- concurrent input during output and explicit session-state reset;
- deterministic or controllable decoding, retry semantics, and version pinning;
- context limits, request size, latency, throughput, cost, and license constraints.

Topic 1 requires audio input, text/structured output, reset, and stable multi-episode service. Topic 2 adds
long-audio and explicit interval accounting. Topic 3 requires causal streaming/cancellation; an emulated
capability is allowed only if the paper claims engineered synchronization rather than native duplex.

### 6.4 Selection rules

1. Freeze task requirements before naming M1 candidates.
2. Exclude a candidate that cannot satisfy the minimum interface without changing the research question.
3. Select by capability, pinning, license, reproducibility, and feasible cost—not by pilot task score.
4. Freeze the M0/M1 panel before matched-budget evaluation.
5. Keep acting, planning, embedding, and judging roles explicit. A stronger hidden planner is a new method cell.
6. Prefer deterministic verifiers. If an LLM judge is unavoidable, freeze it independently and report
   judge-free metrics plus sensitivity to at least one alternative rubric or judge.

## 7. Standard baseline ladder

Each topic instantiates the same ladder:

| Level | Baseline | Purpose |
|---|---|---|
| B0 | Direct single-call or stateless black-box core | Measures base capability. |
| B1 | Strong task-native deterministic policy | Tests whether agentic machinery is needed. |
| B2 | Exposure- and compute-expanded non-agentic policy | Separates scheduling/compute from adaptive control. |
| B3 | Generic external-control policy | Separates topic-specific mechanism from generic reflection, retrieval, or FSM control. |
| B4 | Proposed smallest surviving policy | Tests the bounded research intervention. |
| B5 | Component ablations and counterfactual removals | Attributes the gain. |
| B6 | Oracle diagnostic | Measures headroom and error source. |
| B7 | External or trained reference ceiling | Provides context without serving as causal proof. |

The strongest baseline is determined on development data before the primary comparison. A baseline that fails
for an implementation reason cannot be counted as evidence for the proposal.

## 8. Standard experimental protocol

### Phase A — ceiling-seeking discovery

- Follow the Project Thesis: do not cap compute prematurely; log every resource.
- Search for whether any legal external policy can approach the frozen core's task ceiling.
- Use development data only, explicitly mark adaptive exploration, and retain all failed variants.
- Compare quality–cost frontiers, but do not call unequal-compute wins causal policy evidence.
- Stop if a task has no headroom, no verifiable reward, or no black-box-compatible action.

### Phase B — mechanism consolidation

- Freeze the smallest policy that preserves the discovery gain.
- Remove redundant agents, prompts, calls, state fields, and task-specific rules.
- Predeclare primary outcome, hard-case panels, hypotheses, and stop conditions.
- Freeze model/endpoint receipts, prompts, task splits, verifier, policy, and harness commit.

### Phase C — matched-budget causal comparison

- Compare B4 with the strongest B0–B3 control under identical task items and randomized paired order.
- Match calls, model identity, prompt envelope, retrieved tokens, unique and processed audio, retry allowance,
  and any second-model access appropriate to the claim.
- Report both strict matched budget and a frontier across at least two budget regimes.
- Count failures, timeouts, cancellations, discarded generations, and retries in the denominator and cost.
- Use paired bootstrap intervals and hierarchical effects over task, condition, order, and endpoint where data
  support them; report medians, tails, and worst slices as well as means.

### Phase D — robustness and portability

- Run frozen-policy quantization/runtime sensitivity on M0q.
- Run the preregistered M1 family without retuning the policy, then permit a separately labeled adapter-only
  calibration if needed.
- Test task order, acoustic condition, length, domain, and adversarial state perturbations.
- A cross-model effect requires a different family, not merely another quantization.

### Phase E — held-out confirmation

- Use a never-inspected test carrier and an independent runner.
- No policy mutation, prompt tuning, baseline replacement, or model selection after results are viewed.
- Publication-grade large-scale confirmation remains Stage 3 and requires its own admitted paper repository.

## 9. Metrics and attribution rules

### 9.1 Primary outcome hierarchy

1. executable environment or exact structured task success;
2. frozen label-grounded semantic correctness;
3. validated deterministic proxy;
4. blinded human rating or frozen LLM judge only when the preceding levels are impossible.

WER, retrieval recall, edit rate, latency, and naturalness are mechanism or interaction metrics unless the
carrier's task is explicitly transcription, retrieval, editing, or conversational quality.

### 9.2 Required counterfactuals

- replace the adaptive action with the strongest fixed action under the same budget;
- remove the cited knowledge item, observed span, state field, or arbitration decision;
- replay the same model responses with a different policy where causally valid;
- shuffle irrelevant state to detect prompt-length or priming effects;
- replay with oracle information to measure remaining model versus controller headroom.

### 9.3 Multiple comparisons and tuning

One primary contrast and one primary outcome are frozen per carrier. All other variants are secondary or
exploratory. Report the complete attempted policy family from the discovery ledger. Do not present the best of
many prompts as if it were a single preregistered method.

## 10. Reproducibility and release gates

No result is promotion-eligible until all applicable gates pass:

1. **Black-box conformance:** forbidden internal signals are absent from policy inputs.
2. **Model receipt:** artifact/runtime/endpoint and capability hashes are frozen.
3. **Carrier receipt:** license, provenance, split, exposure, and verifier contracts pass.
4. **Baseline receipt:** every load-bearing baseline is R0 or R1 and independently smoke-tested.
5. **Deterministic mock:** seeded success, failure, retry, cancellation, and rollback cases replay exactly.
6. **Budget audit:** resource accounting closes without untracked calls, audio, retries, or judges.
7. **Information boundary:** test outcomes and future audio cannot reach the policy.
8. **Counterfactual attribution:** removing the claimed mechanism changes the outcome where the claim says it
   should and does not merely change prompt length.
9. **Regression and safety:** hard-case and prior-success panels remain within frozen bounds.
10. **Independent replay:** a second runner reconstructs metrics and final state from released manifests.

## 11. Engineering work plan

| WP | Deliverable | Acceptance gate |
|---|---|---|
| H0 | Factor inventory and interface decision record | Every mutable degree of freedom has an owner and manifest field. |
| H1 | Event schema, artifact hashes, and virtual clock | Golden traces replay byte-for-byte except declared nondeterministic fields. |
| H2 | Black-box `ModelAdapter` contract and mock endpoint | Forbidden-access tests fail closed; timeout/retry/cancel semantics pass. |
| H3 | `TaskAdapter`, verifier, split, and exposure contracts | Test labels and future evidence are unreachable from policy code. |
| H4 | Baseline registry and availability-receipt generator | R0/R1/R2/R3 classification is machine-readable and every result resolves to a receipt. |
| H5 | Budget governor and resource ledger | Calls, audio exposure, tokens/estimates, retries, concurrency, and cost reconcile. |
| H6 | Policy API and topic-specific typed action spaces | No task/model conditionals exist in the harness core. |
| H7 | Replay and counterfactual engine | State/action removal and fixed-policy substitution reproduce expected deltas. |
| H8 | Metric/statistics pipeline | Paired records, confidence intervals, tail slices, failures, and frontier plots regenerate from traces. |
| H9 | External compatibility adapters | AU-Harness and one duplex benchmark ingest/export path pass without weakening local contracts. |
| H10 | Independent-runner package | Clean-environment dry run rebuilds manifests and deterministic reports. |

Implementation order is H0 through H8. H9 begins only after native R0 baselines pass. No live service or model
is needed for H0–H8 because the mock endpoint and recorded-response replay are the first engineering target.

## 12. Topic-specific consequences

### 12.1 Speech-aware evidence acquisition continuation

Do not create a replacement knowledge study or a parallel agent framework. Extend the admitted SAEA study
through its existing `OBS–ORG–SUPPLY–USE` interfaces, result lineage, execution contract, and repository. Its R0
controls are no knowledge, full/raw legal context, static legal roster, lexical or frozen dense retrieval, fixed
multi-hypothesis query, and fixed retrieve–pack–answer. The legal knowledge artifact is source-derived and
versioned; episode evidence state resets. The harness must prevent evaluation outcomes from modifying future
inputs and must counterfactually remove, shuffle, or replace every decisive evidence item. Cross-episode memory
methods remain deferred boundary evidence. A bounded agentic-task probe may demonstrate leverage only when a
dated owner amendment admits it; it does not change SAEA's claim surface.

### 12.2 Interleaved perception and revision

Start with R0 whole-audio, fixed chunks, sliding tail, two-pass, and transcript-then-answer schedules. AU-Harness
is the preferred external task-adapter source because it already spans speech QA, intent, function calling,
long ASR, instruction following, and other audio-to-text tasks; only speech-boundary-legal subsets and
deterministic metrics should be adopted. The primary scientific contrast occurs after adaptive observation and
revision have been consolidated, not during ceiling seeking.

### 12.3 Agentic full duplex

Start with an R0 virtual-time event suite, not a voice demo. Full-Duplex-Bench v1/v1.5 is the first external
compatibility target; v2/v3, HumDial-FDBench, FD-Bench, and tau-Voice are later service/data-dependent panels.
Trained native models remain reference ceilings. The external policy claim requires continuous capture,
causal availability, cancellation acknowledgment, transaction barriers, and deterministic final-state replay.

## 13. Stop and promotion criteria

### Stop or split the shared harness claim if

- topic implementations require incompatible hidden model assumptions rather than typed adapters;
- no R0/R1 baseline can be made scientifically comparable;
- gains vanish after matched exposure and compute;
- a simple deterministic policy matches the agentic policy;
- counterfactual replay cannot attribute improvements to the claimed action;
- model/runtime drift dominates the policy effect; or
- the harness becomes so broad that policy changes cannot be enumerated and preregistered.

### Eligible for owner consideration of execution only if

- the shared black-box, event, budget, baseline, and replay contracts are frozen;
- the topic has a legal carrier, verified headroom, and at least one R0 strong baseline;
- the discovery-versus-causal evidence phases are explicitly separated;
- the M0 role and preregistered M1 selection rule are accepted;
- deterministic mock and independent replay gates pass without model contact; and
- the remaining research object is a bounded policy, not a general-purpose agent platform.

## 14. Primary sources and availability evidence

- Program contract: `wiki/Project-Thesis.md`; current authority: `wiki/Research-Objective.md`; local artifacts:
  `docs/datasets.lock.json`.
- [Qwen3-Omni official repository](https://github.com/QwenLM/Qwen3-Omni) and
  [official model card](https://huggingface.co/Qwen/Qwen3-Omni-30B-A3B-Instruct).
- [Inspect AI official repository](https://github.com/UKGovernmentBEIS/inspect_ai).
- [AU-Harness official repository](https://github.com/ServiceNow/AU-Harness).
- [Adaptive Retrieval Without Self-Knowledge?](https://aclanthology.org/2025.acl-long.319/),
  [Counterfactual RAG](https://openreview.net/forum?id=9U51rOnGko), and
  [the RAG-Reasoning survey](https://aclanthology.org/2025.findings-emnlp.648/).
- [WavRAG](https://aclanthology.org/2025.acl-long.613/),
  [Google Speech-to-Retrieval](https://research.google/blog/speech-to-retrieval-s2r-a-new-approach-to-voice-search/),
  and [the SVQ dataset card](https://huggingface.co/datasets/google/svq/blob/main/README.md).
- Deferred memory-study evidence: [EvoMemBench](https://github.com/DSAIL-Memory/EvoMemBench),
  [A-MEM](https://github.com/agiresearch/A-mem), [EvoLib](https://github.com/microsoft/EvoLib), and
  [EvolveMem](https://github.com/aiming-lab/SimpleMem/tree/main/EvolveMem).
- [AudioMarathon official repository](https://github.com/DabDans/AudioMarathon) and
  [LibriSpeech-Long official repository](https://github.com/google-deepmind/librispeech-long).
- [Full-Duplex-Bench official repository](https://github.com/DanielLin94144/Full-Duplex-Bench),
  [FD-Bench official repository](https://github.com/pengyizhou/FD-Bench), and
  [HumDial-FDBench official repository](https://github.com/ASLP-lab/HumDial-FDBench).
- [tau2-bench official repository](https://github.com/sierra-research/tau2-bench) and
  [tau-Voice paper page](https://openreview.net/forum?id=2Oj6fg0m1j).
- [Moshi official repository](https://github.com/kyutai-labs/moshi).
