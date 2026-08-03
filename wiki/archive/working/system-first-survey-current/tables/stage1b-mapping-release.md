---
artifact_id: "SF-STAGE1B-MAPPING-RELEASE-V4-2026-07-23"
stage: "STAGE_1B_LATE_EXECUTION_AND_CLOSEOUT"
status: "V5_RELEASE_CANDIDATE; NARROW_INDEPENDENT_TRANSITION_REREVIEW_REQUIRED"
h5_load_bearing_use: "WITHHOLD"
novelty_verdict: "NOT_PERMITTED_IN_STAGE_1B"
---

# Stage-1B systematic mapping release tables

This is the canonical Stage-1B synthesis. It maps method paths, proximity, limitations and
measurement coverage; it does not rank research problems, select a project, freeze a reproduction
list, or claim technical novelty. Counts use three deliberately separate denominators:

| population | denominator | permitted use | missing / conflict accounting |
|---|---:|---|---|
| frozen arXiv D0 | 20,727 work identities | discovery-flow accounting | 0 without an abstract disposition inside D0; not a literature-universe denominator |
| retained registry | 226 unique works | portfolio roles, task and broad speech/non-speech strata | 0 duplicate IDs; 215 works have no strict schema-v7 method-path row |
| legacy strict schema-v7 occupancy | 8 works / 11 method paths | text/vision mechanism, access and decision-right occupancy | 9 load-bearing paths; 2 boundary paths; speech/audio-bearing path count = 0 in this legacy set only |
| bounded speech/omni identity audit | 81 named works | explicit `DIRECT / INSTRUMENT / BOUNDARY / EXCLUDE / H5_HELD` routing | 81/81 routed exactly once: 23 direct methods, 19 instruments, 27 boundaries, 11 trained/model exclusions and 1 H5-held row |
| bounded known-prior reconciliation | 9 canonical works | reconcile seed manifest, CURRENT bibliography and registry without duplicate seeds | 2 direct methods and 5 instruments enter supplement v2; MM-ReAct and AuTAgent remain routed-only boundaries |
| closed eligible-bundle reconciliation | 18 canonical works | close six reviewer-gate identities plus 12 reliability/decision routes without new discovery | 18/18 have official metadata, local PDF/e-print evidence and one canonical claim-work action; six gate works and MUGEN enter supplement v3, 11 remain routed-only |
| speech/omni strict supplement | 46 works / 46 evidence rows | comparable speech-bearing method, measurement and boundary evidence | 26 direct methods enter the supplement method denominator; 18 instruments and 2 boundaries are load-bearing only for synthesis |
| bounded delta supplement | 193 work identities / 12 D2 full texts | new support, contradiction and boundary evidence | 181 excluded from this release's load-bearing map; 12 stay outside the frozen 226 denominator |

One work may expose several facets, but it contributes once to the 226-work portfolio. Occupancy uses
`method_path_id`, not paper facets. Multi-path works therefore contribute once per genuinely distinct
path, never once per role label.

## 1. Coverage and kill matrix

`Occupied` means a mechanism or measurement exists in the inspected evidence. It does not mean the
research problem is solved. A kill observation is a single result that would reject the corresponding
residual-gap hypothesis in Stage-1C.

| unranked family | direct/system evidence | transfer/component evidence | strongest contradiction or boundary | current coverage | single-observation kill |
|---|---|---|---|---|---|
| Evidence-state control | Omni-Decision (`DP-2607.11433`), EChO-Agent (`DP-2606.15141`), AudioGenie-Reasoner (`DP-2509.16971`) and Audio-Mind (`DP-2605.28480`) expose explicit evidence, sufficiency, repair or acquisition state | AOP-Agent (`DP-2605.28192`) and Active Perception Agent (`DP-2512.23646`) supply observe-reflect-replan paths; VTM-Nav and MSCE remain non-speech transfer | The direct omni/audio loop is already occupied; the residual must be narrower than “speech agents lack evidence state” | `DIRECT_OCCUPIED_IN_BOUNDED_SPEECH_SET` | On the same frozen speech task, a coded direct prior exposes the same auditable state/action interface and removes the residual failure without any added controller mechanism |
| Tool/agent arbitration | AudioToolAgent (`DP-2510.02995`), Audio-Maestro (`DP-2510.11454`), VISA (`DP-2606.07264`), Agent-Omni (`DP-2511.02834`), i-Code Studio (`DP-2305.13738`), Speech-Copilot (`DP-2407.09886`) and AudioGPT (`DP-2304.12995`) explicitly route tools or agents | FAM-HRI (`DP-2503.16492`) and Langbar (`DP-2510.06223`) supply speech-bearing fusion and typed-tool boundaries; MM-ReAct is the non-speech origin boundary and AuTAgent is the trained-policy boundary | Routing itself is heavily occupied; learned gates remain a training-dependent boundary and reward/credit semantics are not uniformly present | `DIRECT_OCCUPIED_IN_BOUNDED_SPEECH_SET`, credit semantics partial | A static or already-coded router matches the proposed arbitration policy on success, calibration and harm under the same frozen access contract |
| Budget/stop/repair | AudioGenie-Reasoner (`DP-2509.16971`), Thinking with Sound (`DP-2509.21749`), LongShOTAgent (`DP-2512.16978`), Interactive ASR (`DP-2604.09121`), Agentic ASR (`DP-2605.29430`), MUGEN (`DP-2603.09714`), EChO-Agent (`DP-2606.15141`) and Omni-Decision (`DP-2607.11433`) expose continue/repair/select/stop edges | confidence stopping, budget forcing, Best-of-N/MCTS and execution guards remain component comparators | Repair can damage correct outputs; consensus or judge score can look strong while selection utility and decision margin remain weak | `OCCUPIED_WITH_RELIABILITY_GAP` | A preregistered existing stop/repair rule dominates the proposed policy on true task validity and cost across the target noise range |
| Evaluator/reward reliability | AudioJudge (`DP-2507.12705`), Audio-Aware LLM Judges (`DP-2506.05984`), SpeakerSleuth (`DP-2601.04029`), ParaPairAudioBench (`DP-2606.24648`), UniSRM (`DP-2605.23261`), LALM audio-judge reliability (`DP-2607.07985`), Omni-DeepSearch (`DP-2605.08762`), EVA-Bench (`DP-2605.13841`), WavReward (`DP-2505.09558`), SDiaReward (`DP-2603.14889`) and GSRM (`DP-2602.13891`) provide speech/audio routes | SpeechJudge, SpeechLLM-as-Judges, MOS-RMBench, NoRefER, SpeechQE, MACE, BRACE, CAF-Score, RAS and semantic-aware confidence calibration cover trained-judge, metric, preference, robustness and calibration boundaries; Oracle Gap, HALLMARK and the Best-of-N decision-utility diagnostic remain component comparators | Prompted frozen judges, trained reward models, benchmarks and direct controllers are distinct roles. Pairwise/pointwise disagreement, position or verbosity bias, lexical dominance, tie handling, shift and proxy-to-decision failure prevent a generic “audio-native judge is reliable” inference | `MEASUREMENT_RICH`, decision utility and cross-task calibration incomplete | One locally feasible evaluator retains prespecified calibration, ranking agreement, tie/abstention behavior, shift robustness and low harm—and preserves those properties when used for selection—across every target slice |
| Interactive/full-duplex objective | VoiceAgentRAG (`DP-2603.02206`), Enterprise Realtime Voice Agent (`DP-2603.05413`), Pepper (`DP-2603.21013`), Unit-Based Agent (`DP-2601.20230`) and AURA (`DP-2506.23049`) provide direct system paths; tau-Voice (`DP-2603.13686`), VoiceAgentBench (`DP-2510.07978`), Full-Duplex-Bench v3 (`DP-2604.04847`), EchoChain (`DP-2604.16456`), From Text to Voice (`DP-2605.15104`), Audio2Tool (`DP-2604.22821`), EVA-Bench (`DP-2605.13841`) and IHBench (`DP-2606.19595`) provide instruments | VideoFDB (`DP-2605.30256`) is an explicit audio-visual full-duplex benchmark boundary; JarvisBench (`DP-2607.16610`) is a spoken-mediation boundary, not a speech-native method | Direct systems now exist, but their objectives differ; static audio-QA gains still need not transfer to interruption, latency, visual grounding and long-horizon task success | `DIRECT_AND_INSTRUMENT_OCCUPIED_IN_BOUNDED_SPEECH_SET` | An existing frozen voice-agent controller on the identical interaction contract closes both task-success and interaction-quality deficits without the hypothesized policy |

All `DP-*` identities resolve through the self-contained 59-route reference appendix and the
hash-pinned 46-row supplement. The wider 81-work candidate universe, including explicit exclusions
and routed-only papers, remains bound by its original coverage ledger. The nine-work known-prior and
18-work eligible-bundle reconciliations are separate denominators; both reuse canonical work IDs and
create no duplicate seed or claim work. Paper-reported metrics have not been reproduced by this project.

## 2. Strict system-control occupancy

The release preserves two comparable layers rather than silently rewriting the legacy denominator.
The first source is `wiki/survey/current/data/known-item-coding-v7.json`: 11 paths from 8 works, not
the 226-work roster. Every value below is path-level.

| facet | occupancy | denominator | missing / conflict |
|---|---|---:|---|
| load-bearing status | 9 load-bearing; 2 boundary | 11 paths | 0 missing |
| core topology | 7 single-core multi-call; 2 multi-model federation; 2 single-core | 11 | 0 missing |
| internal visibility | 11 API-only | 11 | no hidden-state/gradient-access path in this strict set |
| native modality | 7 text; 4 vision; 0 speech/audio | 11 | speech-native strict occupancy is unmeasured, not empty literature |
| core weight update | 10 false; 1 true | 11 | 0 missing |
| external component update | 8 false; 2 true; 1 unknown | 11 | one unresolved boundary value |
| controller/config optimized on labels | 6 true; 5 false | 11 | 0 missing |
| selection object | 4 none; 4 trajectory; 2 candidate output; 1 tool/agent | 11 | 0 missing |
| terminal operator | 4 select-one; 2 accept/reject; 2 synthesize; 2 none; 1 vote | 11 | 0 missing |

Decision rights are multi-label and therefore do not sum to 11: stop 5, tool-call 4, branch 3,
supply 2, synthesize 2, retry 2, route 1 and execute/skip 1. One path has no explicit decision right.
Signal sources likewise are multi-label: LLM judge 7, consensus 2, learned RM/PRM 1, trained
classifier 1 and state observation 1.

The second source is the speech/omni supplement. Its 46 rows have a different analytical role and
must not be folded into the legacy 11-path counts without disclosure:

| supplement role | rows | enters direct-method occupancy | use |
|---|---:|---:|---|
| `DIRECT_CONTROL_METHOD` | 26 | 26 | speech/audio-bearing external control paths |
| `MEASUREMENT_INSTRUMENT` | 18 | 0 | evaluator and interactive-task support, including trained reward boundaries |
| `BOUNDARY_COMPARATOR` | 2 | 0 | spoken mediation and audio-visual full-duplex boundaries |

All 26 direct rows use API-only external control and preserve the coded core weights. They all include
load-bearing speech/audio, but the decision core may be audio-native, omni-native, a text coordinator
over audio tools, or a cascade. Therefore “speech/audio-bearing path” must not be rewritten as
"speech-native core." Across the two strict layers, the disclosed direct-method count is 35
load-bearing paths (9 legacy plus 26 supplement); this is a bounded inspected-evidence count, not a
literature prevalence estimate.

The orthogonal control-basis table prevents direct-system occupancy from being mistaken for
reward-guided control: 9 rows are `EXTERNAL_ORCHESTRATION_ONLY`, 9 are
`STATE_OR_EVENT_GATED`, and 8 are `EVALUATOR_OR_VERIFIER_GATED`. No row in this bounded direct set is
currently classified `REWARD_GUIDED_SELECTION`; that empty cell is a descriptive result, not a
novelty claim.

## 3. Sensitivity by task, modality and access contract

| stratum | core | instrument | transfer | negative/boundary | total | interpretation |
|---|---:|---:|---:|---:|---:|---|
| retained-registry speech/omni-primary works | 12 | 38 | 0 | 26 | 76 | registry role counts only; does not include every rescued local/frozen-D0 identity |
| bounded named speech/omni audit | 23 | 19 | 0 | 38 | 80 + 1 held | 27 boundaries + 11 trained/model exclusions form the 38; Daily-Omni is the additional H5-held row |
| non-speech works | 0 | 5 | 45 | 100 | mechanism transfer and falsifiers dominate |
| strict text-native paths | — | — | — | — | 7 | all API-only; path-level, not role-level |
| strict vision-native paths | — | — | — | — | 4 | all API-only; path-level, not role-level |
| legacy strict speech/audio-bearing paths | — | — | — | — | 0 | legacy schema-v7 set only |
| supplement speech/audio-bearing direct paths | — | — | — | — | 26 | all include load-bearing speech/audio; core-native modality varies |

The 76 retained-registry speech/omni works are distributed across ASR (26 tags), TTS (12), spoken agent (6), spoken
QA/reasoning (5), SER (5), audio generation (4), speaker tasks (4), ST (4), and smaller strata.
Tags are multi-label. Access sensitivity can be stated only for the 11 strict paths: all are API-only;
no headline result may extrapolate from them to hidden-state or gradient-access systems. Nine of the
12 delta full texts contain a training/no-update wording conflict requiring human interpretation;
six contain strong no-update evidence and ten contain a page-local control path. The separate 46-row
speech/omni supplement now changes the release's speech-specific evidence surface, but not the frozen
226-work registry denominator or the legacy schema-v7 counts.

## 4. Instruments, negative priors and boundary comparators

| portfolio | works | speech/omni | non-speech | evidence condition |
|---|---:|---:|---:|---|
| measurement instruments | 43 | 38 | 5 | all 43 have at least one registry evidence locator and invalidation condition |
| negative / boundary priors | 126 | 26 | 100 | all 126 have at least one registry evidence locator and invalidation condition |
| open transfer mechanisms | 45 | 0 | 45 | repository gate: 68/226 open-source verified across all roles; role is not a reproducibility claim |
| core mechanisms | 12 | 12 | 0 | direct/core citation targets are exactly these 12 canonical work IDs |

Repository state across the 226 works is 68 `OPEN_SOURCE_VERIFIED`, 18 paper-linked but unverified,
39 unreachable and 101 with no repository evidence. A reachable URL, a paper promise, an inspectable
repository and local reproducibility remain distinct claims.

## 5. Saturation and flow

| step | input | output | unresolved / inaccessible | stopping meaning |
|---|---:|---:|---:|---|
| frozen arXiv execution | 65 registered queries | 20,727 unique D0 IDs | 0 active query failures | frozen arXiv pool built; not literature closure |
| D0 abstract handling | 20,727 | 20,727 dispositions | 0 inside D0 | frozen-D0 identity exhaustion only |
| D0 full-text depth | 20,727 | 319 D2 full texts | non-selected abstracts remain D0-only | code-on-use depth, not random prevalence |
| D0 consolidation | 319 | 226 retained + 93 drop | 0 disposition unresolved | roster freeze |
| date-bounded delta | 193 unique IDs | 12 D2 supplements + 181 non-load-bearing exclusions | 0 REC-0 unresolved | 2026-07-16..2026-07-21 only |
| T1 venue routes | 50 routes / 71,254 titles on executed routes | 28 executed, 3 not held, 19 waived; 3,310 wordlist-matched titles | 2,633 title-only identities unresolved | no waived route is reported as zero hit |
| direct/core backward citation | 12 core works | 266 unique arXiv-ID edges; 34 already in D0/delta/registry | 232 outside frozen identity sets; DOI/title-only edges unresolved | bounded arXiv-ID subset only |
| direct/core forward citation | 12 core works | 12 explicit waivers | public index returned HTTP 429 | no zero-new-forward-edge claim |

The 2,633 T1 title-only identities and 232 citation-only arXiv IDs are disclosed omission surfaces.
They are excluded from `NO_DIRECT_MATCH` and literature-closure claims, but do not justify reopening
the broad D0 campaign. Future resolution must be targeted by a Stage-1C input or a dated delta.

## 6. Direct-prior proximity and reproduction readiness

This table is unranked and is not a frozen reproduction list.

| role / cluster | explicitly routed works | proximity and readiness statement |
|---|---|---|
| direct audio evidence acquisition and repair | AudioGenie-Reasoner (`DP-2509.16971`), Thinking with Sound (`DP-2509.21749`), Audio-Maestro (`DP-2510.11454`), LongShOTAgent (`DP-2512.16978`), Active Perception Agent (`DP-2512.23646`), AudioRAG (`DP-2602.10656`), MUGEN (`DP-2603.09714`), Interactive ASR (`DP-2604.09121`), AOP-Agent (`DP-2605.28192`), Audio-Mind (`DP-2605.28480`), Agentic ASR (`DP-2605.29430`), VISA (`DP-2606.07264`), EChO-Agent (`DP-2606.15141`) and Omni-Decision (`DP-2607.11433`) | The bounded inspected set already contains acquisition, transformation, consensus selection, routing, verification, repair and stop paths. Reproduction readiness varies and no execution is authorized. |
| direct speech/omni system orchestration | i-Code Studio (`DP-2305.13738`), FAM-HRI (`DP-2503.16492`), AURA (`DP-2506.23049`), AudioToolAgent (`DP-2510.02995`), Langbar (`DP-2510.06223`), Agent-Omni (`DP-2511.02834`), Unit-Based Agent (`DP-2601.20230`), VoiceAgentRAG (`DP-2603.02206`), Enterprise Realtime Voice Agent (`DP-2603.05413`) and Pepper Realtime AI Assistant (`DP-2603.21013`) | These occupy typed-tool, multi-agent, streaming, retrieval, interruption and listen/speak control surfaces. They differ materially in core modality and task contract, so they are mapped rather than ranked. |
| speech/voice measurement instruments | VoiceAgentBench (`DP-2510.07978`), tau-Voice (`DP-2603.13686`), Full-Duplex-Bench v3 (`DP-2604.04847`), Audio2Tool (`DP-2604.22821`), Omni-DeepSearch (`DP-2605.08762`), EVA-Bench (`DP-2605.13841`), IHBench (`DP-2606.19595`), LALM audio-judge reliability (`DP-2607.07985`), AudioJudge (`DP-2507.12705`), Audio-Aware LLM Judges (`DP-2506.05984`), SpeakerSleuth (`DP-2601.04029`), ParaPairAudioBench (`DP-2606.24648`) and UniSRM (`DP-2605.23261`) | These support task, tool, interruption, search and evaluator-reliability bundles but enter zero method-occupancy rows. The 11 routed-only reliability works remain explicit in the 18-work reconciliation and appendix. |
| audio-visual full-duplex boundary | VideoFDB (`DP-2605.30256`) | Extends the interaction comparator to full-duplex vision-speech; it is a benchmark instrument, not evidence that a speech-native controller occupies the same task contract. |
| spoken-mediation boundary | JarvisBench (`DP-2607.16610`) | Useful long-horizon mediation instrument, but its worker tasks are text-dominant; it cannot establish a speech-native control method. |
| non-speech close comparators retained from v2 | Oracle Gap and Signal Fidelity (2607.17531); VRR-Stop (2607.17641) | Retain recoverable-mass, signal-fidelity, harm and noisy verify/repair-stop diagnostics; speech transfer remains untested. |

The broader candidate account also names 49 routed-only instruments/boundaries, 11 trained/model
exclusions and Daily-Omni as `H5_HELD`. Their absence from the strict 46-row table is an explicit role
decision, not an omission.

## 7. H5 and release boundary

Coder-A has 21/21 replayable anchors, but independent coder-B, agreement and third-party disagreement
adjudication remain absent. Therefore `H5_LOAD_BEARING_USE=WITHHOLD`: H5 contributes zero rows to
occupancy, headline or gap selection. Eligible inputs that require modality-specificity inference are
marked ineligible in the companion Stage-1C input file. Non-H5 path mapping above remains usable.

The formal state after this table is `V5_RELEASE_CANDIDATE`, not `STAGE_1C_SIGNED`. A fixed commit
and manifest must precede an independent transition review. Corrections after the freeze enter only
through a dated superseding release.
