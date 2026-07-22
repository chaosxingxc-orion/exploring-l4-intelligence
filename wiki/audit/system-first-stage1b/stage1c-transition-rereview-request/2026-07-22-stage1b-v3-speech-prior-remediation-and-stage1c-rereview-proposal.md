---
title: "Stage-1B v3 speech-prior remediation and Stage-1C transition re-review proposal"
date: "2026-07-22"
artifact_type: "INDEPENDENT_TRANSITION_REREVIEW_REQUEST"
review_target_commit: "626914a963637354642116b938eb9ab745a099c8"
superseded_release_commit: "51b527b88e1f9993f1c2bd9d826f86c73a6a938c"
requested_verdict: "SIGN_STAGE1C_TRANSITION | WITHHOLD_WITH_BOUNDED_DEFECTS"
novelty_verdict_requested: "NO"
execution_authority_requested: "NO"
---

# Stage-1B v3 speech-prior remediation and Stage-1C transition re-review proposal

## Executive request

Please independently review scientific release commit
`626914a963637354642116b938eb9ab745a099c8` and decide only whether Stage-1B now provides a
sufficiently complete, internally consistent and reviewable survey basis for formal Stage-1C problem
comparison.

The preceding review correctly withheld transition because the release had a material scientific
coverage defect: typical speech-related systems were present in local evidence but absent from the
strict mapping surface. AudioGenie-Reasoner was the clearest example. The same review also found that
the v2 manifest bound mutable HOT/status/router files whose contents still pointed to the superseded
v1 release. Those defects are accepted, not contested.

This proposal does **not** ask the reviewer to endorse novelty, rank candidate problems, select a
technical approach, approve a reproduction list, or authorize a model/API/dataset/prototype run.
Stage-1 remains survey and experimental-foundation work. Technical-approach innovation is intentionally
deferred to reproduction-first Stage-2A and validation in Stage-2B.

## Fixed object under review

The scientific object is the v3 release manifest at
`docs/checks/stage1b-closeout/2026-07-22-v3/release-manifest.json` in commit `626914a`. It binds 45
artifacts: 37 Git artifacts and eight external hash-pinned artifacts. The manifest excludes
`wiki/Research-Objective.md`, `wiki/survey/current/status.md` and
`wiki/survey/current/README.md`; those mutable routers are not part of the scientific object and
therefore cannot create the v2 self-pointer inconsistency.

The release is reproduced from
`wiki/survey/workbench/system-first-stage1b/2026-07-22-stage1b-release-v3-spec.json`. Its declared
correction policy is dated supersession only, and its binding mode is the containing Git commit. A
fresh materialization from the spec equals the committed manifest byte-for-byte.

## What was repaired

### 1. A bounded candidate universe now precedes the strict table

The repair does not patch only the reviewer-named paper. It constructs an explicit 81-work identity
universe from four already-existing sources:

| source inventory | source denominator | named decisions carried into the active ledger | hash authority |
|---|---:|---:|---|
| local full-text v4 | 451/451 PDFs extracted | 14 local speech-agent rescue decisions | paper-analysis SHA-256 `55b24547e58d19ec3190802da3d944ab682b4f1c7ed71f0caa432cd33666d172` |
| frozen-D0 root-aware rescue | 529/529 nonlocal high-recall candidates routed after processing all 20,727 frozen D0 identities | 53 named manual decisions | rescue-audit SHA-256 `63992b1e141fa0170675b2fab5243710d375bbda4c79923a33bc752a7a48fe02` |
| opening D2 direct-prior set | 13 named speech/omni priors and trained boundaries | 13 | Git artifact SHA-256 `f7bec0ba494526aaa2046b334b777038a3e4e1f26b9dd9b48e7b10ae97f02045` |
| bounded reviewer delta D2 | 12 D2 works | JarvisBench as the reviewer-relevant spoken-mediation boundary | external D2 SHA-256 `32054187b7697cbd90a468d4a9b0a18ba7826962cd0eb4f3cf547bf20a6a5ce9` |

After canonical-ID deduplication the union is 81 works. Every identity receives exactly one route:

- 23 `DIRECT_CONTROL_METHOD`;
- 19 `MEASUREMENT_INSTRUMENT`;
- 27 `BOUNDARY_COMPARATOR`;
- 11 `EXCLUDE_WITH_REASON` because training or model intervention is load-bearing; and
- one `H5_HELD` row, Daily-Omni, whose modality-specificity use remains withheld.

The machine-readable authority is
`wiki/survey/current/data/stage1b-speech-omni-prior-coverage-v1.json`. The bounded claim is that every
named decision in these four inventories is routed exactly once. It is not a claim that the literature
universe is closed or that the disclosed lexical root gate has no false negatives.

No new discovery query was issued. One known-ID correction was necessary: Interactive ASR
(`2604.09121`) had a direct-method route but no local full-text bytes. Its PDF and e-print were acquired
by direct arXiv ID dereference, stored outside Git and appended to the existing full-text hash ledger.
This closed an evidence-depth defect without reopening D0.

### 2. Every direct speech/omni method is now strictly comparable

The 32-row supplement at
`wiki/survey/current/data/stage1b-speech-direct-prior-supplement-v1.json` contains:

- all 23 direct control methods from the 81-work universe;
- eight load-bearing measurement instruments; and
- JarvisBench as one explicit spoken-mediation boundary.

Only `DIRECT_CONTROL_METHOD` rows enter the supplement method-occupancy denominator. Instruments and
boundaries remain load-bearing for evidence bundles but contribute zero method-occupancy rows. Every
row records core topology, core-native modality, speech/audio role, access visibility, weight-update
status, label-optimized controller/config status, signals, decision rights, control edges, selection
object, terminal operator, stopping/repair semantics, limitation, local PDF SHA-256 and a page anchor.

This resolves the earlier misleading contrast between an 11-path text/vision strict table and a
speech-primary portfolio. The release now reports both denominators without merging them:

- legacy schema-v7: 11 paths from eight works, nine load-bearing and two boundaries; and
- speech/omni supplement: 32 evidence rows, of which 23 direct methods enter occupancy.

The combined disclosed direct-method count is therefore 32 paths: nine legacy plus 23 speech/omni.
This is a bounded inspected-evidence count, not a prevalence estimate. All 23 speech/omni direct rows
include load-bearing speech/audio and API-only external control, but their decision cores differ:
audio-native, omni-native, a text coordinator over audio tools, or a cascade. The release does not
collapse these into a false “speech-native core” category.

### 3. The omitted typical systems are now visible in the scientific synthesis

The repaired mapping no longer depends on four opening priors alone. It explicitly routes, among
others:

- audio evidence acquisition and repair: AudioGenie-Reasoner, Thinking with Sound, Audio-Maestro,
  LongShOTAgent, Active Perception Agent, AudioRAG, Interactive ASR, AOP-Agent, Audio-Mind, Agentic
  ASR, VISA, EChO-Agent and Omni-Decision;
- speech/omni system orchestration: i-Code Studio, FAM-HRI, AURA, AudioToolAgent, Langbar,
  Agent-Omni, Unit-Based Agent, VoiceAgentRAG, Enterprise Realtime Voice Agent and the Pepper
  Realtime AI Assistant; and
- measurement: VoiceAgentBench, tau-Voice, Full-Duplex-Bench v3, Audio2Tool, Omni-DeepSearch,
  EVA-Bench, IHBench and the LALM audio-judge reliability study.

JarvisBench is retained as a boundary: its spoken mediation is relevant, but the downstream worker
tasks are text-dominant, so it does not establish speech-native method occupancy. Daily-Omni remains
visible as `H5_HELD`; it is not silently discarded or allowed to bypass the independent-coder gate.

### 4. The eligible-input bundles were corrected rather than cosmetically preserved

The new evidence materially changes the Stage-1B description:

- a broad “speech agents lack evidence state” statement is false within the bounded set;
- tool/agent routing is heavily occupied and cannot be treated as a gap by itself;
- budget/stop/repair has multiple direct speech/audio paths, so a later Stage-1C problem must identify
  a residual task/access/noise failure rather than claim the general mechanism is absent;
- evaluator reliability now has eight explicit speech/voice instruments, including a direct audit of
  audio-native judges; and
- interactive/full-duplex control is no longer described as method-sparse: direct systems and
  instruments both exist, although their objectives, access and evaluation contracts differ.

The two H5-dependent bundles—evidence-state transfer across modalities and specialist tool/agent
arbitration—remain `INELIGIBLE_FOR_STAGE_1C_SELECTION`. The three non-H5 bundles remain unranked
eligible inputs: budget/stop/repair, evaluator reliability and interactive/full-duplex system
objectives. Stage-1C, if signed, must compare them under one rubric before any owner selection.

## Verification performed

The correction is guarded by `scripts/survey/sf_stage1b_evidence_release_contract.py`:

- every named source identity must have exactly one route;
- duplicate canonical IDs fail;
- all required typical identities and roles are fixed;
- every direct method must be present in the strict supplement;
- excluded/H5-held rows require a reason and cannot enter the supplement;
- every supplement identity used by the mapping resolves;
- every supplement row has exactly one self-contained reference row with author/year, stable arXiv
  link and the same page anchor; and
- the release spec must include coverage, supplement, references, mapping and eligible inputs while
  excluding mutable router roles.

The contract suite passes 24 tests with 97% branch coverage. The release-manifest suite and evidence
contract pass together. Fresh v3 manifest materialization equals the committed manifest. The current
manifest, bounded AI-context manifest and context-surface check pass after pointing the mutable current
layer to `626914a`; those pointer bytes are intentionally outside the scientific release.

## Remaining limitations, preserved explicitly

The reviewer should not infer more than the release claims:

1. Frozen-D0 exhaustion is not literature-universe closure.
2. The 2,633 title-only T1 identities, 232 backward arXiv IDs outside frozen sets, DOI/title-only
   edges and waived forward-citation routes remain disclosed omission surfaces.
3. Routed-only instruments and boundaries outside the 32-row supplement are not deeply compared.
4. H5 has coder-A anchors but no independent coder-B agreement/adjudication; H5 remains
   non-load-bearing.
5. Paper-reported metrics have not been reproduced by this project.
6. Workbench reproduction-readiness notes are resource audits, not an execution queue.
7. No model, API, dataset metric, smoke, reproduction or prototype execution occurred in this repair.

## Requested independent tests and verdict

Please answer the following three gate questions against commit `626914a`:

1. **Scientific-release integrity:** Do all 45 bound artifacts replay with the recorded hashes, and is
   the scientific object free of the v2 mutable-router/self-pointer inconsistency?
2. **Bounded speech-prior completeness:** Given the disclosed four-source universe and its limitations,
   are all named typical speech/omni candidates explicitly routed, and are all direct methods present
   in the strict comparable supplement?
3. **Stage-1C input sufficiency:** Without making a novelty verdict, are the corrected non-H5 bundles,
   contradictions, kill observations, applicability limits and nearest-prior routes sufficient to
   begin formal Stage-1C comparison?

Please return one of two outcomes:

- `SIGN_STAGE1C_TRANSITION` if all three tests pass; or
- `WITHHOLD_WITH_BOUNDED_DEFECTS`, listing only defects that are necessary before Stage-1C and
  identifying the affected manifest-bound artifact and claim.

A signature would authorize Stage-1C problem comparison only. It would not authorize model loading,
reproduction or technical implementation.

## Self-contained reference route

The following references are the 32 load-bearing supplement identities. Each local PDF hash and exact
method-path coding is in the manifest-bound supplement; the locator shown here is the page anchor used
by that row.

| ID | Reference | Role | Local evidence anchor |
|---|---|---|---|
| DP-2305.13738 | Yuwei Fang et al. (2023), [i-Code Studio](https://arxiv.org/abs/2305.13738) | direct | p1, “configurable and composable framework” |
| DP-2503.16492 | Yuzhi Lai et al. (2025), [FAM-HRI](https://arxiv.org/abs/2503.16492) | direct | p1, “introduce FAM-HRI” |
| DP-2506.23049 | Leander Melroy Maben et al. (2025), [AURA](https://arxiv.org/abs/2506.23049) | direct | p1, “Speech Agents, ReAct Reasoning” |
| DP-2509.16971 | Yan Rong et al. (2025), [AudioGenie-Reasoner](https://arxiv.org/abs/2509.16971) | direct | p1, “until sufficient information” |
| DP-2509.21749 | Zhen Xiong et al. (2025), [Thinking with Sound](https://arxiv.org/abs/2509.21749) | direct | p1, “Thinking-with-Sound” |
| DP-2510.02995 | Gijs Wijngaard et al. (2025), [AudioToolAgent](https://arxiv.org/abs/2510.02995) | direct | p1, “arbitrate conflicting tool outputs” |
| DP-2510.06223 | Hans G. W. van Dam et al. (2025), [Langbar](https://arxiv.org/abs/2510.06223) | direct | p3, “current view” |
| DP-2510.07978 | Dhruv Jain et al. (2025), [VoiceAgentBench](https://arxiv.org/abs/2510.07978) | instrument | p1, “comprehensive benchmark” |
| DP-2510.11454 | Kuan-Yi Lee et al. (2025), [Audio-Maestro](https://arxiv.org/abs/2510.11454) | direct | p1, “autonomously call external tools” |
| DP-2511.02834 | Huawei Lin et al. (2025), [Agent-Omni](https://arxiv.org/abs/2511.02834) | direct | p1, “delegates subtasks to modality-specific agents” |
| DP-2512.16978 | Mohammed Irfan Kurpath et al. (2025), [LongShOTAgent](https://arxiv.org/abs/2512.16978) | direct | p2, “training-free omni-modal evidence-seeking agent” |
| DP-2512.23646 | Keda Tao et al. (2025), [Active Perception Agent](https://arxiv.org/abs/2512.23646) | direct | p1, “dynamic planning” |
| DP-2601.20230 | Haoyuan Yu et al. (2026), [Unit-Based Agent](https://arxiv.org/abs/2601.20230) | direct | p2, “keep listen and listen-to-speak” |
| DP-2602.10656 | Jingru Lin et al. (2026), [AudioRAG](https://arxiv.org/abs/2602.10656) | direct | p1, “external information grounding” |
| DP-2603.02206 | Jielin Qiu et al. (2026), [VoiceAgentRAG](https://arxiv.org/abs/2603.02206) | direct | p4, “Slow Thinker operates asynchronously” |
| DP-2603.05413 | Jielin Qiu et al. (2026), [Enterprise Realtime Voice Agents](https://arxiv.org/abs/2603.05413) | direct | p1, “9-chapter progressive tutorial” |
| DP-2603.13686 | Soham Ray et al. (2026), [tau-Voice](https://arxiv.org/abs/2603.13686) | instrument | p1, “verifiable completion of complex grounded tasks” |
| DP-2603.21013 | Erich Studerus et al. (2026), [Pepper Realtime AI Assistant](https://arxiv.org/abs/2603.21013) | direct | p2, “instantly interrupt the robot speech” |
| DP-2604.04847 | Guan-Ting Lin et al. (2026), [Full-Duplex-Bench v3](https://arxiv.org/abs/2604.04847) | instrument | p2, “evaluating real-time voice agents” |
| DP-2604.09121 | Peng Wang et al. (2026), [Interactive ASR](https://arxiv.org/abs/2604.09121) | direct | p1, “agentic framework for interactive ASR” |
| DP-2604.22821 | Ramit Pahwa et al. (2026), [Audio2Tool](https://arxiv.org/abs/2604.22821) | instrument | p1, “invoking tools from raw speech” |
| DP-2605.08762 | Tao Yu et al. (2026), [Omni-DeepSearch](https://arxiv.org/abs/2605.08762) | instrument | p2, “audio as the only initial modality” |
| DP-2605.13841 | Tara Bogavelli et al. (2026), [EVA-Bench](https://arxiv.org/abs/2605.13841) | instrument | p3, “live, task-oriented multi-turn conversations” |
| DP-2605.28192 | Ke Xu et al. (2026), [AOP-Agent](https://arxiv.org/abs/2605.28192) | direct | p1, “observe-reflect-replan loop” |
| DP-2605.28480 | Yucheng Wang et al. (2026), [Audio-Mind](https://arxiv.org/abs/2605.28480) | direct | p2, “conditional evidence acquisition” |
| DP-2605.29430 | Zixuan Jiang et al. (2026), [Agentic ASR](https://arxiv.org/abs/2605.29430) | direct | p1, “Agentic Correction and Semantic Evaluation” |
| DP-2606.07264 | Wenming Tu et al. (2026), [VISA](https://arxiv.org/abs/2606.07264) | direct | p1, “routing to resolve disagreements” |
| DP-2606.15141 | Siyuan Zhang et al. (2026), [EChO-Agent](https://arxiv.org/abs/2606.15141) | direct | p1, “planning, tool execution, evidence integration” |
| DP-2606.19595 | Ahmad Salimi et al. (2026), [IHBench](https://arxiv.org/abs/2606.19595) | instrument | p1, “Post-Interruption Recovery” |
| DP-2607.07985 | A. Sayyad et al. (2026), [LALM audio-judge reliability](https://arxiv.org/abs/2607.07985) | instrument | p4, “10 baselines by 6 DSP defects” |
| DP-2607.11433 | Ming Ma et al. (2026), [Omni-Decision](https://arxiv.org/abs/2607.11433) | direct | p1, “structured evidence state” |
| DP-2607.16610 | Chen Chen et al. (2026), [JarvisBench](https://arxiv.org/abs/2607.16610) | boundary | p1, “dual value of mediation” |
