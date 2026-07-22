---
artifact_id: "SF-STAGE1C-ELIGIBLE-INPUTS-V1-2026-07-22"
owner_stage: "STAGE_1B"
ordering: "UNRANKED"
selection_authority: "NONE_IN_STAGE_1B"
h5_load_bearing_use: "WITHHOLD"
---

# Unranked Stage-1C eligible inputs

These are evidence bundles, not final candidate cards. Stage-1B does not rank them, choose a problem,
freeze a reproduction list, or propose a novel mechanism. Stage-1C may compare only the inputs marked
`ELIGIBLE_NON_H5`; an input marked `INELIGIBLE_FOR_STAGE_1C_SELECTION` remains visible but cannot be
selected until independent H5 coding and adjudication close.

All bundles inherit the limitations in `stage1b-mapping-release.md`: the 226-work registry and the
11-path strict occupancy set have different denominators; 2,633 T1 title-only identities, 232
citation-only arXiv IDs, DOI/title-only backward edges and all forward-citation edges remain outside
load-bearing no-match claims.

## Evidence-state control

| required element | bounded input |
|---|---|
| problem / gap hypothesis | Frozen omni/speech systems may lack a task-portable, externally inspectable evidence state that jointly represents support, conflict, dependencies, repair history, actionable needs and stopping readiness. |
| system-level direct evidence | Omni-Decision explicitly implements evidence state, critic commits, readiness, repair and exhaustion. EChO-Agent implements structured audio evidence, verifier feedback, repair/regeneration and dual-path selection. These are evidence that the space is already partly occupied. |
| component / transfer evidence | AOP-Agent uses hierarchical omni memory and observe-reflect-replan; VTM-Nav adds persistent structured memory and an execution guard; MSCE governs evidence-linked memory and skills. |
| strongest contradiction | Omni-Decision already covers much of the stated interface. AOP-Agent and EChO-Agent show direct no/low-training control loops, so a broad “evidence state is missing” claim is false. ActiveVision also shows that adding tools can shift, rather than solve, the verification bottleneck. |
| single-observation kill | Under the same frozen access and target task, one registered direct prior exposes the same auditable state/action contract and removes the prespecified residual failure without any additional controller state or action. |
| unresolved alternatives | Gains may come from better prompts, more capable base models, retrieval quality, tool coverage, memory capacity, or task decomposition rather than evidence-state control. |
| method limitations | State definitions can encode designer labels; an LLM critic may be uncalibrated; persistent memory can propagate stale evidence; state bookkeeping adds latency and may not transfer across modalities. |
| applicability | Candidate tasks: spoken/omni QA or agent tasks with observable evidence/tool traces. Access: API-only frozen core. Modality-transfer claims require H5. |
| feasible replacement data / nearest prior / evaluator | Use a locally locked speech/omni task only after Stage-1C selection; nearest priors are Omni-Decision, EChO-Agent and AOP-Agent; evaluator must separate task success, evidence correctness, unresolved-conflict recall, harmful repair and cost. No reproduction is authorized here. |
| expected value / reason not to do | Value: auditable and safety-relevant system state. Do not select if the residual collapses to a naming difference from Omni-Decision or requires hidden-state access. |
| H5 status | `INELIGIBLE_FOR_STAGE_1C_SELECTION`: the cross-modality/modal-specificity part depends on H5 coder-B and adjudication. |

## Tool/agent arbitration

| required element | bounded input |
|---|---|
| problem / gap hypothesis | A frozen speech/omni system may lack a calibrated external policy for routing among models/tools, resolving conflicting outputs and assigning evaluator credit under one task contract. |
| system-level direct evidence | AudioToolAgent already routes among audio-language tools and reacts to conflicts; EChO-Agent selects between evidence-grounded candidates. |
| component / transfer evidence | MoBE performs optimization-free expert routing with online statistics; the UAV prior combines candidate generation, self-correction and multi-criteria selection; the registry includes bandit selection, tool gating and mixture/search mechanisms. |
| strongest contradiction | Existing prompt routers, learned gates and candidate selectors may already occupy every useful decision right. “Multi-agent” alone is not a gap, and a trained router cannot be silently counted as frozen inference control. |
| single-observation kill | A registered static or existing router matches the proposed policy on task success, calibration, abstention/harm and cost under the identical frozen API contract. |
| unresolved alternatives | Performance may be determined by tool quality, tool descriptions, input routing errors, context-window limits, base-model knowledge, or candidate diversity rather than arbitration. |
| method limitations | Credit signals can be non-identifiable; expert scores may be incomparable; online statistics can drift; multiple calls increase cost and correlated errors can eliminate oracle headroom. |
| applicability | Multi-tool speech/omni tasks with auditable calls and outcomes; API-only frozen cores. Cross-modal expert specialization is H5-dependent. |
| feasible replacement data / nearest prior / evaluator | Candidate instruments include voice tool-use/task-completion benches already routed in the corpus. Nearest priors are AudioToolAgent, EChO-Agent and MoBE. Evaluators require task success, route accuracy, conflict resolution, oracle gap, signal fidelity, harm and cost. |
| expected value / reason not to do | Value: a reusable external decision layer across heterogeneous tools. Do not select if candidate diversity/oracle gap is negligible or existing prompt routing already saturates the target contract. |
| H5 status | `INELIGIBLE_FOR_STAGE_1C_SELECTION`: modality-specialist routing and cross-modal transfer require H5 closure. |

## Budget, stopping and repair policy

| required element | bounded input |
|---|---|
| problem / gap hypothesis | With no gradients, hidden states or dependable log-probabilities, an external controller may still lack a robust policy for continue/stop/retry/repair/rollback under evaluator noise and finite budget. |
| system-level direct evidence | Omni-Decision implements readiness and exhaustion; EChO-Agent caps tool retries and repairs inconsistent answers; VRR-Stop explicitly models verifier false accept/reject and repair damage. |
| component / transfer evidence | Confidence stopping, budget forcing, Best-of-N/MCTS, persistent-memory guards and token vetoes provide component comparators. |
| strongest contradiction | Stopping and repair are already heavily occupied. VRR-Stop directly addresses noisy verify-repair loops; the remaining problem must be scoped to an uncovered task/access/noise cell, not claimed as a new general idea. |
| single-observation kill | A preregistered existing stop/repair rule dominates the proposed policy on true task validity and total cost throughout the target verifier-noise range. |
| unresolved alternatives | Apparent gains can arise from more sampling, better candidate generators, verifier capacity, prompt revisions, or easier tasks; estimated noise parameters may not be identifiable online. |
| method limitations | Repair can damage correct outputs; proxy acceptance can rise while validity falls; conservative guards may stop too early; sequential calls add latency. |
| applicability | API-only frozen systems with observable task outcome or verifiable intermediate evidence. The hypothesis is control-policy-specific and makes no modality-generalization claim. |
| feasible replacement data / nearest prior / evaluator | Select a locally feasible task only in Stage-1C. Nearest priors are VRR-Stop, Omni-Decision and EChO-Agent. Required evaluators: true task validity, verifier discrimination, repair damage, decision margin, rounds and latency/cost. |
| expected value / reason not to do | Value: directly controls reliability/cost and is falsifiable with negative outcomes. Do not select if no trustworthy outcome measure exists or oracle headroom is negligible. |
| H5 status | `ELIGIBLE_NON_H5`: restricted to API-only decision policy; no modality-specificity conclusion is allowed. |

## Evaluator and reward reliability

| required element | bounded input |
|---|---|
| problem / gap hypothesis | External reward/evaluator signals for frozen speech/omni tasks may be insufficiently calibrated, unstable under shift, or misaligned with true task success to safely drive selection and repair. |
| system-level direct evidence | The retained portfolio contains 43 instruments, including speech/omni task-success and judge routes. |
| component / transfer evidence | Oracle Gap separates recoverable mass, signal coverage/fidelity, selection quality and harm. HALLMARK shows how false-positive rate controls deployment usefulness. VRR-Stop links verifier discrimination and decision margin to stopping reliability. |
| strongest contradiction | Some deterministic task environments already expose terminal success; a well-specified local evaluator may make a generic reward-reliability project unnecessary. Evaluator research is not itself a control-method novelty claim. |
| single-observation kill | One feasible existing evaluator meets prespecified calibration, ranking-agreement, shift and low-harm thresholds on every target slice and preserves them when used for selection. |
| unresolved alternatives | Failures may come from candidate quality, label noise, task ambiguity, data shift, judge prompt sensitivity, or base-rate changes rather than evaluator design. |
| method limitations | Calibration can be split-specific; scalar rewards hide heterogeneous errors; LLM judges share model biases; deterministic checks cover only part of task success. |
| applicability | Speech-native or omni tasks with auditable outcomes; no cross-modal generalization is asserted. Access remains external/API-only. |
| feasible replacement data / nearest prior / evaluator | Candidate instruments include tau-Voice-style terminal state, voice tool-use exactness and existing audio benchmark judges. Nearest diagnostic priors are Oracle Gap, HALLMARK and VRR-Stop. Measure calibration, MCC/ranking agreement, false positive/negative rates, harm and selection utility. |
| expected value / reason not to do | Value: prevents an unreliable reward from corrupting every downstream control decision. Do not select if a deterministic task oracle already covers the intended decision surface or the target lacks candidate headroom. |
| H5 status | `ELIGIBLE_NON_H5`: bounded to speech-native evaluator behavior; cross-modal transfer remains prohibited. |

## Interactive/full-duplex system objective

| required element | bounded input |
|---|---|
| problem / gap hypothesis | Inference-time control results from static QA may not transfer to full-duplex, interruptible, policy-grounded and environment-interacting voice agents, where task success and interaction quality can diverge. |
| system-level direct evidence | tau-Voice, VoiceAgentBench and EVA-Bench define interactive or agentic voice measurement. JarvisBench measures mediation of long-horizon execution and user guidance. |
| component / transfer evidence | AnovaX exposes a voice planner, typed executors and adaptive recovery; cascade and text-agent control priors provide architecture comparators. |
| strongest contradiction | The primary evidence is measurement/prototype evidence, not proof that reward-guided control succeeds. Stronger base models, cascades or better ASR may explain much of the deficit without a new controller. |
| single-observation kill | An existing frozen voice-agent controller on the identical interaction contract closes both task-success and interaction-quality deficits without the hypothesized external control plane. |
| unresolved alternatives | ASR errors, latency, VAD, turn-taking, tool schema, user simulator realism, policy constraints and base-model reasoning can each dominate the result. |
| method limitations | Live interaction is expensive and stochastic; simulated users can bias outcomes; task success may reward poor interaction; latency budgets constrain repeated inference. |
| applicability | Speech-native full-duplex or mediated long-horizon tasks, API-only frozen systems, observable tool/environment state. No transfer from static vision/text is assumed. |
| feasible replacement data / nearest prior / evaluator | Candidate datasets/environments must be chosen from locally feasible locked assets in Stage-1C. Nearest instruments are tau-Voice, VoiceAgentBench, EVA-Bench and JarvisBench; evaluate terminal task success, tool correctness, interruption recovery, latency, interaction quality and harmful claims. |
| expected value / reason not to do | Value: aligns the project with real agent behavior rather than static QA. Do not select if the environment cannot be made reproducible locally or if failures are almost entirely front-end ASR/VAD defects. |
| H5 status | `ELIGIBLE_NON_H5`: speech-native scope only; it makes no modality-specificity comparison. |

## Stage-1C handoff state

The eligible set is deliberately not reduced to three to five cards. Stage-1C must first compare the
three `ELIGIBLE_NON_H5` bundles using one common rubric: directness, contradictory coverage,
falsifiability, local feasibility, nearest-prior reproducibility and system-first value. The two H5
dependent bundles stay visible but cannot enter selection. Formal Stage-1C work still requires an
independent transition signature against the fixed Stage-1B release commit; model or reproduction
execution remains withheld after that signature until the later execution gate.
