# Stage-1C capability-first consolidation plan for the five research dimensions

**Status: complete (2026-07-27).** This plan consolidates the five-dimension dossiers, the T1/T2/T3
aggregation tables and the 32 sub-directions from 2026-07-26/27; it does not redo their paper-fact layer.
The goal is to write the owner's five unifying constraints into one CURRENT research contract and to
eliminate the competing explanations between the old C1/headroom framework and the five-dimension
combination.

## 1. The final contract that must be satisfied

1. The core model is always an `API-only` black box: a method must never depend on weights, gradients,
   hidden states, attention, logprobs or rewriting inside the decoder; a local open-weight model must also be
   used through an inference interface equivalent to a proprietary API.
2. The research goal is **reliably realized capability improvement**. Reliability constrains the variance of
   end-to-end task utility, tail degradation, cross-condition stability and the incumbent regression rate;
   evaluator reliability is only one component of it.
3. Knowledge, memory, skills and orchestration jointly construct system-level in-context state. Static
   fixed-pool headroom describes only the supply already executed, and must never become a precondition gate
   on whether system control is studied at all.
4. Lean is used to audit paper assumptions, the algorithm-proposition correspondence and conditional
   guarantees; it does not prove error bounds for a real evaluator and does not replace capability
   experiments. Every load-bearing theorem must list its assumptions, the applicable operator, what cannot be
   derived from it, and its code-conformance status.
5. The main proposal must take task capability as the dependent variable. Safety, injection defense, reward
   hacking, abstention and similar topics are retained as cross-cutting stress tests, vetoes or fallbacks, and
   never occupy a main-paper slot on their own.

## 2. Disposition of existing results

| Existing content | Disposition | Reason |
|---|---|---|
| The full-text D0-D6 dossiers, the T1/T2/T3 tables | Keep | Paper facts, assets and experiment fields are reusable |
| The five dimension definitions: knowledge / memory / skills / system / evolution | Keep and tighten | The dimensions are correct; they need a unified interpretation as the state/actions/dynamics of one control plane |
| The 32 sub-directions | Keep as a design menu | Not all are promoted to standalone topics; they are mapped into the 9 capability main lines |
| P1/P2/P3/P5/P6/P8 | Rename and merge into the final directions | They have direct capability mechanisms and executable experiments |
| P9 headroom/E1 gate | Demote to a cross-cutting measurement contract | No longer the primary question of "first judge whether there is any room" |
| P10 reward hacking | Demote to a stress test for every reward-guided experiment | The failure mode matters, but it is not the capability-improvement main line |
| P11 stop/abstain/budget | Merge into runtime control and the reliability objective | stop/rollback serves stable capability improvement and is not written up as a standalone abstention paper |
| D4.5 injection/provenance defense | Keep as an evidence-state invariant | Not treated as a safety direction or a new slot |
| D4.7 full-duplex | Demote to a late-stage validation carrier | Enabled only when task-capability attribution can be isolated; no specialized model branch |
| C1 primary selection | Revoke its primary-question status, keep the component evidence | Evaluator decision utility is cross-cutting instrumentation, not the research object of the whole project |

## 3. From 32 sub-directions to 9 finalized main lines

| final id | Source | Merging principle |
|---|---|---|
| R1 Adaptive observation and evidence supply | D1.1/1.2/1.3/1.5 | Topology, branching, pricing and effect probe merge into one closed loop |
| R2 Audio-native external knowledge acquisition | D1.4/1.6 | Retrieval and anticipatory supply share the acquisition/cost contract |
| R3 Acoustically keyed persistent memory | D2.1-D2.7 | Key, schema, write/read gate, lifecycle and attribution cannot be separated |
| R4 Runtime skill lifecycle | D3.1-D3.6 | Credit, composition, repair, induction and retirement of skills/tools form one chain |
| R5 Evidence-state agentic architecture | D4.1-D4.6 | Decision authority, answering authority, evidence state and incumbent retention are designed together |
| R6 Within-instance reward-guided context control | D5.3/5.4 + D1/D3 actions | Reward must decide the next action, not merely perform a final rerank |
| R7 Cross-instance experience-driven evolution | D5.5 + D2/D3 | No weight changes; improvement over time through external memory, advantage and policy statistics |
| R8 Condition-adaptive reliable capability control | D5.1/5.2/5.6 | headroom/gate/hacking become diagnostics and constraints on robust utility |
| R9 Five-dimension integrated capability activation system | D4 + D5 + R1-R8 | End-to-end validation of whether the combination beats a strong control group at the same supply and budget |

## 4. Key changes

### 4.1 Objective function

Replace "first measure headroom, then decide whether to control" with:

```text
maximize robust task utility of the external controller
subject to API-only legality, bounded cost, and a preregistered regression/tail-risk constraint
```

headroom, oracle and evaluator calibration all become quantities that explain results; they may kill a
particular **already-executed action menu**, but they cannot kill a new context, memory, skill or evidence
state that has not yet been constructed.

### 4.2 Baselines and attribution

Every direction contains at least: direct readout, structured-prompt, best fixed action, random matched-cost,
consensus/MBR, full fixed chain; the gold oracle is reported offline only. All comparisons hold the same core,
task, input, maximum supply and billing convention fixed, and report generation gain, control gain, additional
information gain and cost separately.

### 4.3 Reliability

The minimum reliability reporting set is: paired task delta, confidence intervals, repeat-run variance,
worst-group/CVaR-style tail, correct→wrong and wrong→correct counts, sign consistency across acoustic
conditions/languages/tasks, and calls/latency/API cost. No absolute "guaranteed correct" is promised; what can
be promised is high-probability non-regression or bounded risk under a defined distribution and stated error
assumptions.

### 4.4 Lean audit

The existing `InfoBoundary` covers only fixed-pool read-out; it must no longer be written up as "ICL is
insufficient". The all-contexts gap in `AgenticElements` is a strong premise, and a finite-sample oracle miss
does not prove that premise. A new runtime reliability proposition is added: if the deployable reward's
consistent error with respect to true utility does not exceed `ε`, then an estimated margin `≥ 2ε` guarantees
non-regression relative to the incumbent, and `> 2ε` guarantees strict improvement. Whether the real world
satisfies the error bound remains the responsibility of experiments.

Before a reference method enters a proposal, fill in one row:

```text
paper claim | mathematical assumptions | black-box operator | Lean status |
implementation conformance | empirical assumptions | allowed conclusion
```

## 5. Recommended minimal Stage-2A vertical validation

The first batch validates only `R5 + R6 + R8`: build an incumbent-preserving evidence-state controller around
one frozen API core, using black-box-available signals to decide
`keep / branch-context / acquire-evidence / repair / stop`. MMAU-mini + MMAR are recommended as closed-set task
carriers so that the system-control effect is isolated first; open-ended tasks, RAG, cross-instance memory and
full-duplex are connected only after that vertical chain passes.

Before running, the following must be separately bound and authorized: model/service revision, data
revision/split/hash, prompt, sampling parameters, action menu, reward, budget, SESOI, reliability threshold,
gold fence and abort rule. Finalizing the directions does not authorize model/API calls, downloads,
reproduction, prototypes, pushes or wiki publication.

## 6. Files and checks

- [x] Added `wiki/survey/current/research-directions.md` as the single direction contract in force.
- [x] Updated `wiki/Research-Objective.md`, `wiki/Project-Thesis.md` and `wiki/Per-Work-Status.md` in place.
- [x] Updated the CURRENT router/status/manifest; the old C1 table now reads "component evidence, primary-question
  status revoked".
- [x] Updated the workbench README, marking master as consolidated evidence source material that no longer
  carries a completion claim.
- [x] Corrected the Lean over-extrapolation comments and added the runtime-reliability conditional theorem and a
  smoke test.
- [x] Ran the context surface, CURRENT layer, Stage-1C evidence, manifest replay, Lean targeted typecheck/Smoke,
  and the quantitative-wording scan. A whole-root `lake build` was not used as PASS evidence this time because
  the first-time cache for the existing mathlib/Tilting `.olean` was incomplete; the new modules and both Smoke
  examples passed directly under Lean 4.31.0.
- [x] Did not modify Stage-1B v5, audit bytes, existing full-text ledger rows or any project code; only rebound
  the previously appended ledger working bytes into the CURRENT manifest.

## 7. Invalidation conditions

This finalization is superseded only when the owner changes the five unifying constraints, the core ceases to be
API-only, the five-dimension scope is re-cut, H5 receives a new signature, or Stage-2A experiments provide
evidence sufficient to change the direction ordering. A new paper only updates the nearest-prior/implementation
choice and never automatically kills a direction; only if it dominates the corresponding mechanism under the same
black-box, supply, budget and reliability contract does it trigger a merge or a re-route.
