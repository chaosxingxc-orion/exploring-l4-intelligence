---
title: "Research proposal: agentic full-duplex speech interaction over a frozen omni core"
date: "2026-08-16"
status: "DRAFT_FOR_OWNER_REVIEW__NO_NEW_EXECUTION_AUTHORITY"
research_horizon: "causal real-time interaction"
program_fit: "TF-Strict external synchronization and dialogue control around frozen endpoints"
literature_cutoff: "2026-08-16"
shared_standard: "docs/superpowers/specs/2026-08-16-black-box-agent-harness-and-experiment-standard.md"
---

# Agentic Full-Duplex Speech Interaction over a Frozen Omni Core

## 0. Decision in one page

This is the highest-risk and potentially highest-impact topic. The original chain—fragment listening,
semantic understanding, dialogue management, and semantic/speech reply—is a useful component list, but it is
still a half-duplex pipeline if the system stops listening while it reasons or speaks. Full duplex requires
concurrent input and output, a shared clock, online arbitration, interruption, cancellation, echo/speaker
control, and recovery after overlap.

The surviving research question is:

> Can a training-free external synchronization and dialogue-control plane turn frozen speech/omni endpoints
> into a causally correct full-duplex task agent that listens while speaking, handles barge-in and
> self-correction, preserves verifiable task success, and exposes an auditable latency–behavior–accuracy
> frontier?

The system must be described as **engineered full-duplex synchronization over a frozen core**, not a native
full-duplex model. Public ChatGPT/OpenAI voice capabilities are an interaction target, not evidence of an
internal architecture. The proposal must compare native speech-to-speech and cascaded designs at the interface
level without guessing how proprietary systems work internally.

Recommended portfolio status: **retain as a Stage-1 high-risk direction; build a virtual-time benchmark and
causal event baseline before a live audio prototype.** Do not let a polished demo substitute for a research
claim, and do not open a study repository or contact live model services under this proposal alone.

This proposal inherits the shared black-box harness, baseline-availability, model-selection, phased-evidence,
and replay requirements in `2026-08-16-black-box-agent-harness-and-experiment-standard.md`. Where this proposal
is less strict, the shared standard controls. The first reproducible object is a virtual-time causal system;
live voice services are later endpoint cells, not the foundation of the evidence.

## 1. Why the original formulation fails

### 1.1 Sequential fragments are not full duplex

`listen -> understand -> manage -> reply` describes repeated turn-taking. True full duplex requires the input
path to continue during response generation and playback, and the output path to be interruptible based on
new input. Without concurrency and cancellation semantics, "full duplex" is a naming error.

### 1.2 A wrapper cannot manufacture native model capabilities

A turn-based omni core does not become a native synchronous model because an agent sends it smaller chunks.
An external system can run concurrent perception and response loops, possibly with multiple frozen endpoints
or instances, but it must claim engineered synchronization and measure the costs and semantic seams this creates.

### 1.3 The engineering surface can swallow the science

Streaming transport, VAD, ASR, echo cancellation, endpointing, LLM inference, tools, TTS, playback, and UI can
consume an entire project. A working voice assistant is not by itself a paper. The intervention must be a
replayable arbitration and transaction policy with strong baselines.

### 1.4 Latency can improve while task correctness collapses

Recent benchmarks show a large voice-versus-text task gap, failures on corrections and entity tracking, and
trade-offs between fast response, correct turn-taking, and multi-step tool success. Naturalness or first-audio
latency alone is not a valid primary outcome.

### 1.5 Proprietary voice products are not reproducible methods

OpenAI's public voice-agent documentation distinguishes native speech-to-speech sessions from chained
speech-to-text/reasoning/text-to-speech systems and documents interruption-capable real-time transports. It
does not disclose ChatGPT's internal model topology, training data, dialogue manager, or production scheduling
policy. This proposal may target observable capabilities only.

## 2. Scope and portfolio boundary

### 2.1 Defining property

The agent is **causal**: at wall-clock time `t`, no component may consume future user audio. It continues to
capture and classify input while output speech is playing. New evidence can cancel, repair, or redirect the
response and can prevent an unsafe or stale tool transaction from committing.

### 2.2 In scope

- Frozen speech/omni, ASR, language, and TTS endpoints arranged behind stable interfaces.
- Native speech-to-speech and cascaded paths as controlled baselines.
- Concurrent audio ingestion, incremental semantic state, dialogue policy, response planning, speech playback,
  interruption monitoring, and transaction control.
- Barge-in, overlap, backchannels, hesitation, self-correction, entity tracking, multi-step tool use, and safety.
- Virtual-time simulation, loopback testing, and later governed human interaction.
- Training-free policies with versioned rules, prompts, thresholds, and external reward-guided decisions.

### 2.3 Out of scope

- Fine-tuning a native full-duplex spoken language model.
- Claiming architectural equivalence to ChatGPT voice, GPT Realtime, Gemini Live, Moshi, or another proprietary
  or trained native system.
- Cross-session knowledge evolution; memory is frozen within an evaluation campaign.
- Future right context or offline revision of already elapsed interaction time.
- General environmental-audio understanding beyond speech interaction and necessary echo/noise robustness.
- Irreversible real-world actions in early stages.

### 2.4 Non-overlap contract

- The continual-knowledge proposal may change persistent memory between episodes; this proposal freezes its
  knowledge snapshot for the entire benchmark.
- The interleaved proposal may revisit earlier audio with right lookahead; this proposal is strictly causal and
  optimizes real-time behavior.
- Shared ASR/model/TTS adapters, event logging, and task verifiers are infrastructure only.

## 3. Research questions and hypotheses

### RQ1 — Can external synchronization close the voice task gap?

**H1.** At matched frozen core and tool capabilities, a concurrent agentic controller improves verifiable
end-to-end task success over turn-based and naive cascaded streaming baselines under interruption, accent,
noise, and disfluency, while satisfying pre-registered latency constraints.

**Null H1.** The controller improves perceived responsiveness but not final environment state or policy
compliance.

### RQ2 — Does semantic dialogue state help under overlap and correction?

**H2.** An incrementally updated, provenance-bearing semantic state improves correction recovery, entity
tracking, and multi-step tool success relative to transcript-buffer and VAD-only control.

**Null H2.** A strong streaming transcript plus the frozen core's conversational context performs equally well.

### RQ3 — Can speculative response remain safe and reversible?

**H3.** Separating speculative speech from committed tool transactions, with cancel/resume and confirmation
barriers, reduces stale-response duration and wrong-action commits without excessive latency.

**Null H3.** Speculation creates more semantic contradictions and false starts than the latency it saves.

### RQ4 — Is the contribution a policy rather than a tuned demo?

**H4.** The same arbitration policy improves the latency–task-success–interaction frontier across at least two
frozen endpoint configurations and two task families.

**Null H4.** Gains depend on one vendor/model/threshold combination and do not transfer.

## 4. System architecture

### 4.1 Concurrent loops

```text
                         +-----------------------+
microphone -> ingest --->| acoustic event stream |--------------------+
                         +-----------------------+                    |
                                  |                                   v
                                  v                         +-------------------+
                         incremental semantics ------------>| dialogue state    |
                                  |                         | and policy        |
                                  |                         +-------------------+
                                  |                                   |
                                  |                      plan/tool/speech events
                                  |                                   v
                                  |                         +-------------------+
                                  +---- interruption ------>| output arbiter    |--> speaker
                                                            +-------------------+
                                                                      |
                                                               cancel/commit/resume
                                                                      v
                                                            tool transaction layer
```

This is a logical architecture, not a claim that every box must be a separate model. Components may share a
frozen omni endpoint when the endpoint supports the required streaming interface. The trace must still expose
separate input, semantic, policy, output, and transaction events.

### 4.2 Required loops

1. **Ingest loop** — timestamps frames, runs echo/speaker/VAD controls, and never stops during playback.
2. **Semantic loop** — emits partial intent, entities, corrections, end-of-thought hypotheses, and uncertainty
   with audio-span provenance.
3. **Dialogue-policy loop** — chooses `WAIT`, `BACKCHANNEL`, `CLARIFY`, `PLAN`, `SPEAK`, `CANCEL`, `RESUME`,
   `CONFIRM`, or `COMMIT_TOOL`.
4. **Output loop** — streams speech, reports played versus buffered audio, and accepts low-latency cancellation.
5. **Monitor loop** — detects barge-in, echo leakage, semantic conflict, unsafe action, and stale response.

### 4.3 Semantic state

```text
DialogueState
  session_clock
  active_user_hypothesis[]
  confirmed_intent
  entities{value, status, source_span, revision}
  unresolved_slots[]
  dialogue_obligations[]
  pending_plan
  pending_tool_transactions[]
  response_status{speculative, confirmed, played_until}
  interruption_state
  safety_and_policy_state
  budget_and_latency_state
```

User self-correction creates a new entity/version and explicitly supersedes the old one. Transcript text alone
does not own dialogue truth.

### 4.4 Speculation and transaction semantics

- Speech may be speculative and cancellable.
- Read-only tool calls may be speculative if the benchmark permits them.
- State-changing tool calls require an explicit confirmation/commit barrier.
- Cancellation records what audio was generated, buffered, played, and semantically retracted.
- After barge-in, the next utterance must either repair the interrupted proposition or make clear it was abandoned.
- The agent must never treat its own playback echo as a user confirmation.

### 4.5 Event time and determinism

All events carry capture time, processing start/end, decision time, enqueue time, playback start/end, cancellation
time, and causal parents. Virtual-time replay must produce the same policy decisions from the same frozen event
sequence. Live wall-clock variance is reported separately.

## 5. Latest academic and product-interface landscape

| Work or primary source | What it establishes | Consequence for this proposal |
|---|---|---|
| [Beyond Turn-Based Interfaces, EMNLP 2024](https://aclanthology.org/2024.emnlp-main.1192/) | Synchronous LLMs explicitly model real-world time and train on large synthetic plus real spoken-dialogue corpora. | Time-aware full duplex is occupied as a trained-model approach; our difference is external frozen-core control. |
| [OmniFlatten, ACL 2025](https://aclanthology.org/2025.acl-long.709/) | Multi-stage post-training can create an end-to-end GPT full-duplex model for interruption, overlap, and low latency. | A wrapper must not claim native full-duplex modeling. |
| [Incorporating Dialogue State Tracking, Findings IJCNLP 2025](https://aclanthology.org/2025.findings-ijcnlp.49/) | Explicit dialogue state is relevant to task-oriented full-duplex systems. | State tracking is a required baseline, not automatically novel. |
| [Full-Duplex-Bench v2, ACL 2026](https://aclanthology.org/2026.acl-short.4/) | Multi-turn systems struggle with simultaneous speech, corrections, and entity tracking across daily, correction, entity, and safety tasks. | Supplies diagnostic task families and an automated streaming protocol. |
| [Full-Duplex-Bench v3, 2026](https://arxiv.org/abs/2604.04847) | Real human disfluency plus chained tools exposes accuracy/latency/turn-taking trade-offs; self-correction remains difficult. | Use real disfluent speech and tool execution, not only synthetic clean dialogue. |
| [tau-Voice, 2026](https://arxiv.org/abs/2603.13686) | Voice agents retain only a fraction of text-agent task capability on 278 grounded tasks; most failures are attributed to agent behavior in its setup. | Primary metric must be verified task completion plus interaction quality. |
| [Hierarchical Acoustic-Semantic Modeling, ACL 2026](https://aclanthology.org/2026.acl-long.419/) | Native full-duplex models face acoustic–semantic interference; hierarchical separation improves QA and interaction metrics. | Separating acoustic events from semantic state is motivated, but our training-free external implementation is distinct. |
| [BayLing-Duplex, 2026](https://arxiv.org/abs/2606.14528) | A fine-tuned single autoregressive LLM can learn when to listen, speak, and stop without an auxiliary turn module. | Learned arbitration is a strong ceiling; it is outside TF-Strict. |
| [OpenAI Voice Agents guide](https://developers.openai.com/api/docs/guides/voice-agents) | Public interfaces distinguish native speech-to-speech from chained voice agents and support low-latency interruption-capable sessions and tools. | Use as an observable capability target; do not infer ChatGPT internals. |
| [OpenAI GPT-Realtime-2.1 model page](https://developers.openai.com/api/docs/models/gpt-realtime-2.1) | The official interface describes native audio input/output, tools, and improved interruption behavior. | A proprietary reference point, not a reproducible architecture or required dependency. |

**Gap inference.** The field has strong trained native full-duplex models and rapidly improving benchmarks.
What remains plausible—but unproven—is whether an external, training-free concurrency, semantic-state,
cancellation, and transaction policy can recover a meaningful part of the task gap with frozen endpoints and
remain transferable across endpoint configurations. This is narrower than building a voice assistant and must
survive a fresh Stage-1 proximity audit before novelty language is used.

## 6. Evaluation ladder

### L0 — virtual-time event simulator

- Scripted audio/semantic events with exact overlap, pauses, backchannels, self-corrections, and barge-in times.
- Mock frozen endpoints with controllable latency and error profiles.
- Deterministic tools and database state.
- Purpose: prove causality, cancellation, transaction barriers, and trace semantics without live audio or models.

### L1 — offline streaming replay

- Replay existing real or legally generated multi-turn audio on a virtual clock.
- Candidate diagnostic protocol: Full-Duplex-Bench v2/v3 after data, license, and code audit.
- No microphone, speaker, or network jitter; component latency is injected from recorded distributions.

### L2 — local loopback real time

- Real audio capture and playback with controlled echo path, network delay, and CPU/GPU contention.
- Read-only or sandboxed tools only.
- Purpose: validate that virtual-time gains survive physical scheduling and acoustic feedback.

### L3 — grounded task benchmark

- Candidate: tau-Voice or another released environment with final-state verification, after reproducibility and
  service-dependency audit.
- Compare clean, accent, noise, disfluency, overlap, and correction conditions.
- Keep the knowledge snapshot fixed across methods and episodes.

### L4 — governed human interaction

- Enter only after task, safety, privacy, and recording approvals.
- Use a pre-registered protocol and sandboxed tasks; no irreversible external actions.
- Human ratings supplement but do not replace task-state and temporal metrics.

## 7. Baselines and ablations

| ID | Baseline | Purpose |
|---|---|---|
| B0 | Text oracle agent | Measures non-speech task ceiling. |
| B1 | Turn-based speech-to-speech / explicit endpoint | Measures conventional half duplex. |
| B2 | Streaming STT -> frozen LLM -> streaming TTS | Strong cascaded voice baseline. |
| B3 | VAD-only cancellation | Tests simple reactive barge-in. |
| B4 | Rule/FSM dialogue manager with explicit slots | Strong non-agentic task baseline. |
| B5 | Concurrent loops with transcript buffer only | Isolates semantic state. |
| B6 | Proposed semantic-state arbitration and transaction policy | Full system. |
| B7 | Available native full-duplex model/API | Reference ceiling, not an equal-access causal baseline unless frozen and reproducible. |

Required ablations: stop input during output; remove semantic state; remove source spans; remove speculation;
allow unsafe immediate commits; disable cancellation; disable repair after cancellation; VAD versus semantic
interruption; fixed versus adaptive backchannel; one versus two frozen endpoint instances; frozen policy on a
second endpoint stack.

### 7.1 Availability and comparability verdict

The load-bearing first suite is native R0: turn-based, cascaded with deterministic mocks, VAD-only cancellation,
explicit FSM dialogue management, and transcript-buffer concurrency on the same virtual event stream. These
baselines establish causality and transaction safety without a commercial realtime service.

Full-Duplex-Bench now provides public v1/v1.5 static pipelines and data plus v2/v3 dynamic and tool-use stacks.
The v1/v1.5 path is the preferred first external compatibility target, but it remains R2 until a local adapter
and metric smoke pass. The v2 path requires a Node/WebRTC orchestrator, model adapters, ASR, and Gemini/OpenAI
keys; the v3 path requires LiveKit Cloud, realtime provider services, ASR, and optionally a GPT judge. They are
therefore R2 dynamic reference panels, not the primary reproducibility substrate. tau-Voice likewise has an
open task/state framework but its voice path depends on provider realtime APIs plus TTS/STT services. FD-Bench
and HumDial-FDBench add useful offline and natural interruption panels after license, data, and adapter audits.

Moshi and other trained native duplex systems may be runnable R1 artifacts but remain B7 reference ceilings:
their trained synchrony is not scientifically comparable to external control over a frozen core. Availability
does not turn them into evidence that this proposal's arbitration policy caused an effect.

## 8. Evaluation and statistics

### 8.1 Primary task metrics

- Final environment-state success / pass@1.
- Tool selection, argument correctness, transaction validity, and policy compliance.
- Multi-turn instruction and safety success.
- Voice-to-text capability retention relative to B0.

### 8.2 Interaction metrics

- Time to first **useful** audio, not merely first waveform.
- End-of-user-evidence to relevant response latency.
- Barge-in detection and speech-stop latency.
- False interruption, missed interruption, and interruption-avoidance rates.
- Turn-take rate, gap/overlap distributions, backchannel precision, and overtalk duration.
- Self-correction recovery, entity-version accuracy, context continuity, and repair success.
- Stale-response played duration and semantic retraction completeness.

### 8.3 Causality and safety metrics

- Future-audio access violations: must be zero.
- Echo-as-user false confirmations: must be zero in the gated test panel.
- Wrong state-changing commits after correction or interruption.
- Speculation cancellation rate, saved latency, wasted synthesis, and semantic contradiction rate.
- Trace completeness and deterministic virtual-time replay.

### 8.4 Cost and analysis

- Concurrent model seconds, calls, tokens, audio seconds, network time, CPU/GPU utilization, real-time factor,
  TTS waste, and tool latency.
- Report task-success versus latency and task-success versus interruption-quality Pareto frontiers.
- Use paired scenario seeds and the same prerecorded/simulated user event stream across methods.
- Bootstrap scenarios and model task/condition/endpoint as hierarchical factors.
- Do not average task failure away with naturalness ratings.

### 8.5 Evidence phases

Phase A seeks the best development-set task/latency/safety frontier in virtual time with all concurrency and
speculation costs logged. Phase B removes redundant agents, event types, rules, and speculative actions and
freezes the smallest policy that retains the gain. Phase C compares it with the strongest turn-based, cascaded,
VAD, and FSM controls on identical event streams under matched model access, concurrent seconds, retries,
audio exposure, and tool privileges. Phase D repeats the frozen policy on a preregistered second endpoint
configuration. Live physical-clock measurements validate scheduling realism; they do not replace causal replay.

## 9. Stage-1 exploration package

### E1 — proximity and taxonomy audit

- Separate engineered synchronization, learned synchronization, cascaded streaming, and native speech-to-speech.
- Inspect Synchronous LLMs, Moshi-family systems, OmniFlatten, Freeze-Omni-family systems, BayLing-Duplex,
  Lychee-FD, and current benchmark implementations.
- Record training requirements, streaming APIs, concurrency, interruption semantics, tools, data, code, license,
  and reproducibility.
- Exit: a precise prior-difference statement survives both model and systems literature.

### E2 — benchmark and dependency audit

- Verify Full-Duplex-Bench and tau-Voice releases, audio provenance, licenses, scenario availability, service
  dependencies, task verifiers, real/virtual clock assumptions, and costs.
- Confirm which benchmarks accept cascaded or architecture-agnostic entrants.
- Exit: one diagnostic and one grounded task carrier are runnable without hidden labels or unavailable services.

### E3 — endpoint capability audit

- For each candidate frozen endpoint, document incremental input, incremental output, cancellation, session
  state, tool calls, audio formats, timestamp semantics, determinism, and local/offline availability.
- Distinguish official public behavior from inferred internals.
- Exit: at least one reproducible stack supports continuous capture plus interruptible playback.

### E4 — latency and causal budget

- Define frame size, semantic update cadence, maximum decision latency, TTS cancellation granularity, and tool
  commit deadline.
- Build a latency budget from measured or vendor-documented components, with distributions rather than one mean.
- Exit: the target frontier is physically plausible and each latency number has provenance.

### E5 — safety and transaction protocol

- Specify echo attacks, accidental confirmations, contradictory corrections, interruption during sensitive
  actions, prompt injection through speech, and replayed audio.
- Freeze which actions are speculative, read-only, confirmation-gated, or prohibited.
- Exit: deterministic tests prevent state-changing commits in every seeded unsafe scenario.

## 10. Engineering baseline

### 10.1 Components

1. **Clocked event bus** — monotonic timestamps, causal parents, bounded queues, backpressure, and virtual/live
   time modes.
2. **Audio ingress** — framing, VAD, speaker attribution, echo suppression interface, and capture continuity.
3. **Incremental semantic adapter** — partial text plus intent/entity/correction events with provenance.
4. **Dialogue-state store** — versioned entities, obligations, plans, response status, and safety state.
5. **Arbitration policy** — validated `WAIT/BACKCHANNEL/CLARIFY/SPEAK/CANCEL/CONFIRM/COMMIT` actions.
6. **Output controller** — streaming TTS/audio, played/buffered accounting, cancellation, and repair markers.
7. **Tool transaction manager** — speculative read, staged write, confirmation, commit, rollback, and final-state
   verifier.
8. **Scenario runner** — virtual-time users, prerecorded audio, injected latency/noise/overlap, and endpoint
   adapters.
9. **Evaluator** — task, temporal, interaction, safety, cost, and Pareto reports.

### 10.2 Mandatory interfaces

```text
ingest(audio_frame, capture_time) -> AcousticEvent[]
interpret(acoustic_events, dialogue_snapshot) -> SemanticEvent[]
arbitrate(dialogue_snapshot, new_events, budget) -> DialogueAction
stream_response(response_plan) -> OutputEvent[]
cancel(response_id, cause_event) -> CancellationReceipt
stage_tool(action) -> PendingTransaction
commit_tool(transaction_id, confirmation_event) -> ToolReceipt
replay(scenario_id, endpoint_profile, policy_version) -> SessionTrace
score(session_trace, task_contract) -> MetricVector
```

### 10.3 Concurrency invariants

- Audio capture and event timestamping continue while output is generated and played.
- No action depends on an event with a future capture timestamp.
- Every output frame is marked buffered, played, cancelled, or dropped.
- A state-changing tool call cannot commit from a speculative entity value.
- Cancellation is idempotent and produces one receipt.
- Queue overflow and component failure enter a safe degraded mode rather than silently dropping user speech.

### 10.4 Test gates

- Deterministic virtual-time replay.
- Barge-in at every output offset, including before first audio and during a tool confirmation.
- User self-correction before and after speculative speech.
- Echo and overlapping third-speaker rejection.
- Component crash, timeout, queue overflow, and late event arrival.
- Exact measurement of stop latency and stale played audio.
- Cross-endpoint contract tests with mock, cascaded, and native-streaming adapters.

## 11. Work packages and decision gates

| WP | Deliverable | Gate |
|---|---|---|
| WP0 | Full-duplex taxonomy, prior-difference matrix, and adversarial review | External policy claim survives trained/native precedents. |
| WP1 | Benchmark, endpoint, license, dependency, and safety contracts | One reproducible stack and task carrier pass. |
| WP2 | Deterministic virtual-time event bus, transactions, and mock endpoints | Causality and safety invariants pass all seeded tests. |
| WP3 | Turn-based, cascaded, VAD-only, and FSM ceiling/frontier study | Task/latency frontier, headroom, discovery cost, and failure taxonomy are frozen. |
| WP4 | Consolidated concurrent semantic-state and arbitration policy | The smallest surviving policy passes identical-stream, matched-resource Phase C. |
| WP5 | Speculation, cancellation, repair, and commit barriers | H3 improves latency without wrong-action growth. |
| WP6 | Local loopback and second endpoint configuration | Virtual-time effect survives physical scheduling and endpoint change. |
| WP7 | Grounded task benchmark and Stage-2 candidate decision | H4 and release gates pass; claim stays engineered, not native. |

## 12. Adversarial self-debate record

### Round 1 — strongest rejection

**Reject the topic.** Full-duplex research is rapidly occupied by trained native models; an agent wrapper around
a turn-based core is only a cascaded product; latency engineering will dominate; and proprietary ChatGPT voice
behavior cannot provide a reproducible method. A polished demo could still fail every grounded task benchmark.

### Round 2 — decomposition attack

The proposed fragment loop is half duplex. If input and output run concurrently, multiple model instances,
streaming ASR/TTS, VAD, echo cancellation, and tool transactions introduce too many confounds for scientific
attribution. Dialogue state is established prior work, while memory and incremental listening overlap the other
two proposals. Training-free rules may not match learned turn-taking.

### Round 3 — surviving revision

Claim only engineered synchronization over frozen endpoints. Freeze knowledge, prohibit future audio, require
continuous capture during playback, and expose concurrent loops through one causal event protocol. Make the
intervention an arbitration plus transaction policy; compare turn-based, cascaded, VAD-only, FSM, and transcript-
buffer baselines; evaluate final state, correction/entity behavior, interruption, latency, and safety on identical
event streams. Start in virtual time and require transfer to a second endpoint stack.

### Round 4 — reproducibility attack

The field's benchmark availability has improved, but the dynamic paths are not self-contained experiments.
Current Full-Duplex-Bench v2/v3 and tau-Voice paths bind the evaluator to provider APIs, WebRTC/LiveKit, TTS,
ASR, voices, or LLM judges. A successful run may be impossible to replay when a service changes. Native duplex
models also change the trained core and therefore answer a different question.

**Revision:** make deterministic virtual-time controls R0 and load-bearing. Target Full-Duplex-Bench v1/v1.5
first for external compatibility. Keep v2/v3, tau-Voice, FD-Bench, and HumDial-FDBench as R2 until exact service,
data, judge, and adapter receipts close. Keep trained native systems as reference ceilings only.

### Round 5 — experimental-standardization attack

Realtime scores are highly sensitive to clock source, network jitter, audio device buffering, ASR alignment,
TTS chunking, echo cancellation, and provider retry behavior. Comparing systems on different event streams or
with different cancellation semantics cannot establish a dialogue-policy effect.

**Revision:** use one causal event schema and recorded user stream; separate event time from wall time; define
when input becomes available and cancellation becomes acknowledged; replay all policies in virtual time; then
validate the same frozen policy in local loopback. Count failures, discarded audio, speculative synthesis,
concurrent model seconds, and wrong tool commits.

### Round 6 — model-selection and capability attack

An omni model headline does not guarantee the endpoint surface needed for this study. Official Qwen artifacts
support broad audio/text input and text/audio output, but runtimes expose different subsets; the official vLLM
service documentation, for example, currently limits serving behavior to the thinker path. The current local
llama.cpp cell must not be assumed to support causal input streaming, speech output, or cancellation until the
capability probe proves each operation.

**Revision:** select endpoint cells by an exact capability matrix rather than model reputation. Q4 and Q8 are
one-family runtime sensitivity, not portability. Predeclare a second endpoint configuration before results.
If the local anchor lacks a native primitive, label the capability `emulated` and preserve the claim as
engineered synchronization; never imply that the core became natively duplex.

### Round 7 — harness-versus-systems-integration attack

A larger stack can appear more intelligent because it uses separate ASR, planner, dialogue manager, TTS,
judge, and retry services. The contribution then becomes an uncontrolled product integration, and latency gains
may come from speculation or parallel hardware rather than better decisions.

**Revision:** freeze roles and count every endpoint. Compare against a cascaded system with the same component
access. Consolidate the policy before matched-resource evaluation. Attribute gains through removal of semantic
state, arbitration, speculation, cancellation, repair, and commit barriers on the same recorded responses.
Report quality–latency–safety frontiers instead of one composite score.

### Round 8 — surviving claim

The topic survives only as a causal, replayable external arbitration and transaction policy over frozen
endpoints. It does not claim to reproduce ChatGPT's private architecture or to transform a half-duplex core into
a native duplex model. Promotion requires verified task-state improvement under interruption and correction,
continuous input capture, zero gated causal/safety violations, matched-resource controls, and transfer to a
second endpoint configuration.

### Residual risk after revision

The result may remain a systems integration paper with no durable algorithmic insight, or may show that learned
native synchrony is essential. Continue only if the external policy shifts a reproducible Pareto frontier and
the effect transfers across endpoint configurations.

## 13. Stop, revise, and promotion criteria

### Stop

- No reproducible benchmark or endpoint supports the required streaming and cancellation contracts.
- The proposed system cannot continuously capture input during playback.
- Improvements are limited to first-audio latency with no task-success or correction gain.
- VAD-only or FSM baselines match the agentic controller.
- Wrong state-changing commits, echo confirmations, or future-audio violations cannot be driven to zero on the
  gated panel.
- Gains disappear on a second endpoint configuration.
- Service cost or proprietary dependencies prevent independent replay.

### Revise

- Semantic state helps but speculation fails: remove speculative speech and study causal state arbitration.
- Interruption works but tools fail: narrow to conversational full duplex and do not claim agentic tasks.
- Cascaded systems win while native endpoints fail, or vice versa: state an architecture-conditional result.

### Eligible for Stage-2 owner decision

- The work has a precise engineered-synchronization prior difference.
- Virtual-time traces prove causality, cancellation, and transaction safety.
- Strong turn-based, cascaded, VAD-only, and FSM baselines are reproducible.
- Task success improves under difficult speech/interaction conditions while latency and interruption constraints
  remain satisfied.
- The policy transfers across at least two endpoint configurations or has a justified bounded claim.
- Independent replay reconstructs final tool state and all temporal metrics.

## 14. Handoff to engineering

Engineering should build the virtual-time event and transaction substrate before any live voice UI. The first
demo should be intentionally plain: a scripted user interrupts, corrects an entity, and attempts a state-changing
tool action; the trace must prove what audio was available, what speech was played, what was cancelled, and why
the tool did or did not commit. Only after this passes should the team attach live audio endpoints. This ordering
keeps the research claim centered on causal arbitration and task reliability rather than interface polish.

Implement the substrate through shared harness work packages H0–H8. External benchmark or provider adapters
enter through H9 only after native R0 policies, capability probes, causal replay, and budget reconciliation pass.
No live endpoint may bypass the event ledger, cancellation acknowledgment, transaction barrier, or final-state
verifier.
