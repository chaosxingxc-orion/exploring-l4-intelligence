# Stage-1C literature-first closeout plan

**Owner direction:** 2026-07-25 — clear the remaining Stage-1C debt, plan the work in detail, and
finish Stage-1C while reducing nonessential code-robustness work in favor of paper research.

**Outcome:** close Stage-1C with a ranked three-card problem portfolio, one selected primary problem,
a bounded reproduction-first handoff for Stage-2A, explicit kill criteria, and no model, benchmark or
prototype execution.

## 1. Scope and priority rule

The work is ordered by scientific decision value:

1. evidence that can change the selected research problem;
2. evidence that can kill or sharply narrow a candidate problem;
3. evidence needed to freeze the nearest-prior/reproduction handoff;
4. only then, minimal checks that prevent a false research conclusion.

Schema hardening, mutation coverage, cross-platform duplication and new general-purpose checkers are
out of scope unless their absence could change the selected problem, a paper's role, or a load-bearing
claim. Existing audit artifacts and frozen releases remain immutable.

## 2. Legacy-debt disposition

- [x] Treat R2R1 as a frozen, technically checked but undistributed terminal artifact. Do not run a
  third N=56 dual-model recode: the two previous raw coders already demonstrated that the object-level
  contract is not an efficient route to the Stage-1C problem decision.
- [x] Close the calibration campaign as `RETIRED_WITHOUT_DISTRIBUTION_OR_INDEPENDENT_ACCEPTANCE`;
  preserve R1/R2/R2R1 bytes and
  the `FAIL` agreement as method evidence, not as a gate on the non-H5 problem portfolio.
- [x] Keep H5 as `WITHHOLD_NON_LOAD_BEARING`. It blocks cross-modality generalization claims only; it
  does not block speech-native or API-only problem selection.
- [x] Mark old unchecked engineering-plan boxes as historical execution prose, not current debt. The
  HOT/CURRENT layer is the only source for the remaining action.

**Acceptance:** no current page routes the next action to R2R1 review, N=56 recoding, or H5 completion;
none of those items is represented as scientifically completed.

## 3. Literature questions and evidence set

Review the frozen Stage-1B evidence plus a bounded 2026-07-25 update against four questions:

1. Do speech/audio evaluators provide deployment-level decision signal, or only aggregate agreement?
2. When do noisy evaluators make selection, repair, or stopping worse than the frozen baseline?
3. Is interactive/full-duplex evaluation a distinct primary problem or a validation setting for a more
   general external-control problem?
4. Which nearest priors and assets are sufficiently exact for a reproduction-first Stage-2A handoff?

The load-bearing update must include primary sources for speech judges (AudioJudge, TRACE,
SpeakerSleuth, ParaPairAudioBench, and the LALM voice-agent reliability study), decision-utility and
control comparators (JudgeBoN, Oracle Gap, VRR-Stop), direct audio agents (AudioGenie-Reasoner,
AudioToolAgent, MUGEN), and speech-agent validation (VoiceAgentBench, tau-Voice, FDB-v3, IHBench).

- [x] Record supporting evidence, strongest contradiction, transfer boundary, and uncertainty for
  every candidate.
- [x] Separate measurement instruments, direct controllers, trained rewards, and validation carriers.
- [x] Do not turn a recent-paper count, a benchmark gap, or an aggregate correlation into a novelty
  or causal-control claim.

**Acceptance:** every load-bearing factual statement has a stable primary-source link or a frozen local
evidence reference; fact and project inference are visibly separated.

## 4. Candidate-card construction and ranking

Create exactly three final problem cards from the existing non-H5 inputs:

- `C1_DECISION_CALIBRATED_REWARD`: evaluator/reward reliability measured by downstream decision
  utility for select/repair/stop/abstain;
- `C2_NOISY_STOP_REPAIR`: continue/stop/retry/repair/rollback under evaluator noise and finite cost;
- `C3_INTERACTIVE_OUTCOME_CONTROL`: speech-native interaction where terminal success and interaction
  quality diverge.

Rank lexicographically, not by an ungrounded sum:

1. compatibility with the frozen black-box external-control thesis;
2. residual distinctness after the closest 2025–2026 priors;
3. falsifiability with a task-visible oracle and explicit harm;
4. local reproduction feasibility;
5. whether success would explain more than one decision right without becoming a vague umbrella.

- [x] Give each card a problem statement, evidence for and against, nearest prior, exact falsifier,
  feasible data/evaluator path, limitations, and reason not to select it.
- [x] Rank all three and select one primary problem; retain one fallback and one validation-only route.

**Acceptance:** the winner is chosen because it best answers the thesis under the evidence, not because
it is easiest to code or has the most papers.

## 5. Selected-problem contract

Freeze the selected problem at the problem level only. The contract must define:

- observation, external state, candidate supply, evaluator signal, decision rights and terminal truth;
- oracle headroom, signal coverage/fidelity, conditional decision quality, harm and cost;
- pointwise/pairwise/listwise/tie-or-abstain protocols without treating them as interchangeable;
- model/task/slice shift and a conservative fallback when signal is not decision-identifiable;
- single-observation kill criteria and alternative explanations;
- explicit exclusions: trained reward optimization, hidden-state access, specialized duplex-model
  development, novelty claims and technical-mechanism freeze.

- [x] State 3–5 research questions and the minimum evidence that would answer each.
- [x] Freeze the primary/fallback/validation reproduction list and every current blocker.
- [x] Define the Stage-2A entry gate without executing Stage-2A.

**Acceptance:** another researcher can tell what is being tested, what would refute it, and why each
reproduction item is present without reading the retired calibration chain.

## 6. Consolidation and verification

- [x] Supersede the Stage-1C common-rubric table and data in place with ranked, selected closeout
  artifacts.
- [x] Update `wiki/Research-Objective.md`, `wiki/Per-Work-Status.md`, the current router/status and the
  decision log; keep the current layer self-contained.
- [x] Route the retired calibration workbench through its audit index and remove it from the active next
  action without modifying frozen artifacts.
- [x] Run only focused semantic/current-layer/manifest checks plus a repository diff review. Do not add
  a new checker merely to validate this closeout.

**Completion state:** `STAGE1C_COMPLETE_PROBLEM_SELECTED_STAGE2A_REPRODUCTION_AUTHORIZATION_PENDING`.
Stage-2A model calls, benchmark execution, reproduction, prototype work, push and wiki publication stay
closed until a separate owner authorization.
