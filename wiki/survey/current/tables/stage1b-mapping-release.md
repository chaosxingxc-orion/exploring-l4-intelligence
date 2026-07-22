---
artifact_id: "SF-STAGE1B-MAPPING-RELEASE-V1-2026-07-22"
stage: "STAGE_1B_LATE_EXECUTION_AND_CLOSEOUT"
status: "READY_FOR_RELEASE_FREEZE; INDEPENDENT_TRANSITION_REVIEW_REQUIRED"
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
| strict occupancy | 8 works / 11 method paths | mechanism, access and decision-right occupancy | 9 load-bearing paths; 2 boundary paths; speech-native path count = 0 |
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
| Evidence-state control | Omni-Decision: explicit evidence state, critic, repair/readiness and exhaustion; EChO-Agent: structured audio evidence, verifier and repair/select | AOP-Agent observe-reflect-replan; VTM-Nav persistent visual-topological memory; MSCE evidence-grounded memory/skill governance | The direct omni loop is already occupied; ActiveVision shows that tool use can merely move failure into verification | `DIRECT_OCCUPIED`, speech-specific strict occupancy unknown | On a frozen voice-agent task, an existing registered direct prior exposes the same auditable state/action interface and removes the residual failure without any added controller mechanism |
| Tool/agent arbitration | AudioToolAgent prompt-guided audio-tool routing; EChO-Agent dual-path selection | MoBE optimization-free expert routing; test-time UAV candidate scoring; schema/tool-gating priors in the registry | Existing routers and candidate selectors may already cover the proposed decision right; learned gates are a training-dependent boundary | `DIRECT_OCCUPIED`, reward/credit semantics partial | A static or already-registered router matches the proposed arbitration policy on success, calibration and harm under the same frozen access contract |
| Budget/stop/repair | Omni-Decision readiness/exhaustion; EChO retry caps and repair; VRR-Stop noisy verify-repair stopping | confidence stopping, budget forcing, Best-of-N/MCTS and execution guards in retained transfer paths | Repair can damage correct outputs; verifier discrimination and decision margin can reverse the stop decision | `OCCUPIED_WITH_RELIABILITY_GAP` | A preregistered existing stop/repair rule dominates the proposed policy on true task validity and cost across the target noise range |
| Evaluator/reward reliability | speech/omni benchmark and judge instruments in the 43-instrument stratum | Oracle Gap decomposes recoverable mass, coverage, fidelity and harm; HALLMARK isolates false-positive deployment risk | 126 negative/boundary works; LLM selection can be negative and high reported acceptance can coexist with lower true validity | `MEASUREMENT_RICH`, cross-task calibration incomplete | One locally runnable evaluator retains prespecified calibration, ranking agreement and low harm across every target slice, leaving no evaluator-reliability deficit |
| Interactive/full-duplex objective | tau-Voice, VoiceAgentBench and EVA-Bench define voice task success; JarvisBench measures spoken mediation | AnovaX supplies a voice-planner/executor/recovery topology; cascade and voice-tool benchmarks supply comparators | These are mainly instruments or prototypes, not evidence that an external reward controller succeeds; static QA gains need not transfer to interruption and long-horizon interaction | `INSTRUMENT_OCCUPIED`, control method sparse | An existing frozen voice-agent controller, evaluated on the same interactive contract, closes the task-success and interaction-quality deficit without the hypothesized control plane |

Evidence locators for Omni-Decision, AOP-Agent, AudioToolAgent and EChO-Agent are in
`wiki/survey/workbench/system-first-stage1b/2026-07-21-opening-d2-method-path-notes.md`.
Delta PDF hashes and page locators remain in the external D2 ledger identified by the closeout
manifest; paper-reported metrics have not been reproduced by this project.

## 2. Strict system-control occupancy

Source: `wiki/survey/current/data/known-item-coding-v7.json`. Population is 11 paths from 8 works,
not the 226-work roster. Every value below is path-level.

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

## 3. Sensitivity by task, modality and access contract

| stratum | core | instrument | transfer | negative/boundary | total | interpretation |
|---|---:|---:|---:|---:|---:|---|
| speech/omni-primary works | 12 | 38 | 0 | 26 | 76 | strong instruments and negatives; transfer was intentionally routed outside the speech-primary role logic |
| non-speech works | 0 | 5 | 45 | 100 | mechanism transfer and falsifiers dominate |
| strict text-native paths | — | — | — | — | 7 | all API-only; path-level, not role-level |
| strict vision-native paths | — | — | — | — | 4 | all API-only; path-level, not role-level |
| strict speech/audio-native paths | — | — | — | — | 0 | missing strict coding, not proof of an empty method cell |

The 76 speech/omni works are distributed across ASR (26 tags), TTS (12), spoken agent (6), spoken
QA/reasoning (5), SER (5), audio generation (4), speaker tasks (4), ST (4), and smaller strata.
Tags are multi-label. Access sensitivity can be stated only for the 11 strict paths: all are API-only;
no headline result may extrapolate from them to hidden-state or gradient-access systems. Nine of the
12 delta full texts contain a training/no-update wording conflict requiring human interpretation;
six contain strong no-update evidence and ten contain a page-local control path. These delta facts are
supplementary and do not change the strict denominator.

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

| work | proximity fact | local evidence | readiness statement |
|---|---|---|---|
| Omni-Decision (2607.11433) | closest inspected evidence-state → critic → action/readiness/repair path | PDF + e-print + D2 page locators | direct comparator; repository/execution status does not authorize reproduction |
| AOP-Agent (2605.28192) | hierarchical omni memory and observe-reflect-replan | PDF + e-print + D2 page locators | direct comparator; non-streaming limitation retained |
| AudioToolAgent (2510.02995) | audio tools coordinated by a text-only central LLM; conflict-triggered follow-up | PDF + e-print + D2 page locators | direct system comparator; no separate explicit reward located |
| EChO-Agent (2606.15141) | structured audio evidence, diagnostic feedback, verifier repair and dual-path selection | PDF + e-print + D2 page locators | direct evidence-chain comparator; training-free wording remains unclear |
| Oracle Gap and Signal Fidelity (2607.17531) | fixed-pool recoverable mass, signal fidelity and harm diagnostic | PDF + e-print + delta D2 locator ledger | measurement/negative prior; project has not reproduced reported values |
| VRR-Stop (2607.17641) | noisy verifier/repairer model with a stopping rule and guard | PDF + e-print + delta D2 locator ledger | close stop/repair comparator; transfer to speech is untested |
| tau-Voice (2603.13686) | full-duplex grounded voice-agent task-success instrument | existing local corpus route | instrument, not a successful control mechanism |

## 7. H5 and release boundary

Coder-A has 21/21 replayable anchors, but independent coder-B, agreement and third-party disagreement
adjudication remain absent. Therefore `H5_LOAD_BEARING_USE=WITHHOLD`: H5 contributes zero rows to
occupancy, headline or gap selection. Eligible inputs that require modality-specificity inference are
marked ineligible in the companion Stage-1C input file. Non-H5 path mapping above remains usable.

The formal state after this table is `READY_FOR_RELEASE_FREEZE`, not `STAGE_1C_SIGNED`. A fixed commit
and manifest must precede an independent transition review. Corrections after the freeze enter only
through a dated superseding release.
