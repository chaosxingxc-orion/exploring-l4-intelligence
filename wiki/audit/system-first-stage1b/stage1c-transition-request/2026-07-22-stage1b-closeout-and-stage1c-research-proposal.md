---
transaction: "RESEARCH_PROPOSAL_FOR_INDEPENDENT_STAGE_TRANSITION_REVIEW"
proposal_date: "2026-07-22"
proposal_status: "SUBMITTED_FOR_INDEPENDENT_REVIEW"
evidence_release_id: "system-first-stage1b-2026-07-22-v2"
evidence_release_commit: "51b527b88e1f9993f1c2bd9d826f86c73a6a938c"
requested_authority: "STAGE_1C_PROBLEM_SELECTION_ONLY"
novelty_verdict_requested: false
model_or_reproduction_authority_requested: false
h5_load_bearing_use: "WITHHOLD"
---

# Research proposal: frozen-omni external control and the Stage-1C problem-selection transition

## Decision requested from the reviewer

This proposal asks for one bounded decision: whether the evidence frozen at commit
`51b527b88e1f9993f1c2bd9d826f86c73a6a938c` is sufficient to close Stage-1B and begin Stage-1C
problem selection.

It does **not** ask the reviewer to certify novelty, endorse a technical mechanism, choose the research
problem, authorize a model run, or accept paper-reported results as reproduced. A positive decision
would authorize comparison of three unranked, non-H5 problem families. Model loading, smoke tests,
dataset metrics, reproduction and prototypes would remain withheld.

The scientific reason to move now is concrete. The project has a 20,727-work frozen discovery pool,
319 full-text-depth records, a 226-work retained portfolio, a strict 8-work/11-path mechanism map,
explicit negative evidence, and five falsifiable problem bundles. More undirected searching is now
less valuable than deciding which residual problem warrants reproduction-first study.

## 1. Program question and research object

The program asks:

> How far can reward-guided, gradient-free inference-time control activate capabilities already
> present in a frozen black-box omni model on speech and audio tasks?

The research object is not a new foundation model. It is an **external reward-guided control plane**
around a frozen core. The control plane may construct observations, maintain external state and
memory, call tools, generate candidates, evaluate evidence, select or synthesize outputs, allocate
budget, stop, retry, repair or abstain. Its core contract is strict:

- no change to the core model's weights or architecture;
- no required access to gradients, hidden states or attention;
- no assumption that dependable token log-probabilities are available;
- reward or evaluator evidence changes the next external action, not the frozen core;
- all claims are bound to the task, dataset, access contract and failure surface actually measured.

W1, `speech-mllm-training-free-rl`, is the primary program carrier. W2 and W3 remain supporting
training-based alignment studies; W4 remains a separate embedding-utility study. This proposal does
not activate W2-W4.

## 2. Why Stage-1B did not seek a novelty verdict

Stage-1B was designed to map method paths, decision rights, proximity, contradictions, instruments
and reproducibility conditions. It was not designed to prove that a preferred mechanism is new.
Demanding a technical novelty distinction before selecting the problem would reverse the research
order: it would force a solution narrative before the residual failure has been chosen.

The intended sequence is therefore:

1. **Stage-1B:** map the occupied method space and construct falsifiable, unranked gap inputs;
2. **Stage-1C:** compare the eligible problem inputs and select one problem;
3. **Stage-2A:** reproduce the nearest prior under the selected task and access contract, then
   converge the technical approach;
4. **Stage-2B:** test the selected intervention and its failure conditions.

The current proposal concerns only the transition from step 1 to step 2.

## 3. Stage-1B evidence base

### 3.1 Frozen discovery and full-text handling

The frozen D0 contains 20,727 unique arXiv work identities, each with an abstract-level disposition.
Of those, 319 reached D2 full-text depth; 226 were retained and 93 dropped. The retained portfolio has
four non-overlapping work roles: 12 core, 43 instrument, 45 transfer and 126 negative/boundary works.

This is exhaustion of the frozen D0, not proof of literature-universe closure. Papers outside the
frozen pool can be added only through a dated, scoped delta or a targeted Stage-1C need.

### 3.2 Date-bounded delta without duplicate claim seeds

All 65 registered delta-query rows for 2026-07-16 through 2026-07-21 were dispositioned with zero
active failures. They produced 193 unique work identities. A single REC-0 decision selected 12 works
for local PDF, e-print and D2 processing; the other 181 were excluded only from this release's
load-bearing map. Duplicate seeds were zero.

Claim work is keyed by canonical work identity and method path. A paper can contribute multiple
facets, but it is not reintroduced as a second seed or counted twice in the 226-work portfolio.

### 3.3 Venue-route and citation surfaces

All 50 registered T1 routes have dispositions: 28 executed, 3 not held, and 19 explicitly
`WAIVED_UNAVAILABLE`. Executed routes exposed 71,254 titles; the broad wordlist matched 3,310. Of
these, 677 reconcile to known works and 2,633 remain title-only identities. The unresolved titles do
not support zero-hit or `NO_DIRECT_MATCH` claims.

All 12 frozen core works were parsed from local e-prints for backward arXiv-ID citations. This yielded
266 unique arXiv IDs, of which 232 are outside D0, delta and registry. DOI/title-only backward edges
remain unresolved. The public forward index returned HTTP 429 for all 12 targets, so those routes are
waived and no forward-closure claim is made.

### 3.4 Local source reuse

Selected arXiv PDFs and source e-prints are cached under the external `SPEECHRL_DATA_DIR`. Parsing and
repeat verification use those local bytes instead of repeatedly downloading the same public files.
The release stores hashes and ledgers in Git but does not commit PDFs or e-prints. Local caching reduces
bandwidth and improves repeatability; it does not expand the scientific coverage claim.

## 4. What the mapping says

The release deliberately separates populations that earlier drafts risked conflating:

| population | denominator | valid inference |
|---|---:|---|
| Frozen discovery pool | 20,727 works | disposition and flow inside frozen D0 |
| Retained portfolio | 226 works | role, task and broad speech/non-speech structure |
| Strict occupancy | 8 works / 11 paths | mechanisms, access and external decision rights |
| Delta supplement | 193 identities / 12 D2 works | dated support, contradiction and boundary evidence |

Nine strict paths are load-bearing and two are boundary paths. All 11 are API-only; seven are
text-native and four vision-native. The strict speech/audio-native count is zero because that cell was
not strictly coded, not because the literature is known to be empty.

The map shows that broad claims such as “external evidence state,” “tool routing,” or “repair” are
already occupied. The remaining research value lies in narrower reliability and control failures:
evaluator error, harmful repair, stopping under uncertainty, task-grounded interaction, and whether
external decision policies remain useful under a frozen speech/omni access contract.

## 5. Unranked Stage-1C inputs

Stage-1B produced five evidence bundles. Each contains direct support, transfer evidence, the strongest
contradiction, a single-observation kill criterion, alternative explanations, limitations, feasible
data/evaluator conditions, expected value and a reason not to proceed.

| problem family | current status | residual question |
|---|---|---|
| Budget, stopping and repair | `ELIGIBLE_NON_H5` | Can an external policy decide continue/stop/retry/repair/rollback under evaluator noise without causing more harm than it prevents? |
| Evaluator/reward reliability | `ELIGIBLE_NON_H5` | When does a paper-reported or LLM-based signal preserve task-valid ordering, calibration and low false-accept harm across the selected slices? |
| Interactive/full-duplex objective | `ELIGIBLE_NON_H5` | Does inference-time control improve grounded voice-agent task success and interaction quality rather than only static QA? |
| Evidence-state control | `INELIGIBLE_FOR_STAGE_1C_SELECTION` | Is there a speech-specific residual beyond already occupied evidence-state and repair loops? H5 is required for the modality-transfer claim. |
| Tool/agent arbitration | `INELIGIBLE_FOR_STAGE_1C_SELECTION` | Is there a cross-modal routing residual beyond existing tool routers and candidate selectors? H5 is required for specialization claims. |

No ordering is implied by the table. The two H5-dependent families remain visible so that the evidence
is not lost, but they cannot be selected until an independent coder B, agreement calculation and
third-party disagreement adjudication are complete.

## 6. Proposed Stage-1C procedure

If the reviewer signs the transition, Stage-1C will compare only the three `ELIGIBLE_NON_H5` bundles.
The comparison will use a common rubric rather than a preferred-paper narrative:

1. **Problem importance:** the failure affects task validity, safety, recoverable headroom or usable
   interaction—not merely a benchmark score.
2. **Direct evidence and contradiction:** both supporting and strongest disconfirming evidence are
   present under a comparable access contract.
3. **Falsifiability:** one prespecified observation can reject the residual-gap hypothesis.
4. **Black-box fit:** the problem can be studied without weight, gradient, hidden-state or guaranteed
   log-probability access.
5. **Measurement feasibility:** suitable local data and an evaluator with explicit error modes are
   available or can be lawfully acquired.
6. **Nearest-prior reproducibility:** at least one close comparator has adequate artifacts or a bounded
   reimplementation path; repository availability is not itself a reproducibility claim.
7. **System-first value:** solving the problem would clarify an external decision right such as
   evaluation, stopping, repair, routing or abstention.
8. **Scope and cost:** the first reproduction and falsification test fit the available compute and can
   be stopped without expanding into another literature campaign.

Stage-1C will produce one selected problem statement, rejected alternatives with reasons, a frozen
kill criterion, the target task/access contract, the nearest-prior reproduction shortlist, evaluator
requirements, and an explicit Stage-2A authorization request. Selection remains an owner decision
after reviewer sign-off; this proposal makes no substitute selection.

## 7. Reproduction-first path after selection

The eventual Stage-2A sequence is intentionally conservative:

1. lock the selected task, dataset split, frozen model and black-box access contract;
2. reproduce or faithfully reimplement the nearest prior before proposing a new mechanism;
3. establish the frozen model baseline, prior result, evaluator calibration and oracle/recoverable
   headroom where measurable;
4. test the smallest external-control intervention and its kill condition;
5. report success, cost, evaluator error, harmful actions and negative slices;
6. only then decide whether a technical innovation claim is warranted.

These steps describe the research trajectory. They are not authorized executions in the present
transaction.

## 8. Recent remediation since the adverse review

| reviewer concern | remediation now frozen or registered |
|---|---|
| Working-tree evidence could not support a release claim | Release v2 is bound to fixed commit `51b527b`; 37 manifest artifacts comprise 31 Git blobs and 6 external assets, with zero replayed byte/hash mismatches. |
| Recall obligations were incomplete or silently treated as zero | Delta is 65/65 dispositioned; T1 is 50/50 dispositioned; waivers, 2,633 title-only identities, 232 out-of-set citation IDs and unresolved edge classes are explicit. |
| Mapping outputs and denominators were missing | The canonical mapping now supplies coverage/kill, strict occupancy, sensitivity, instrument/negative, flow, proximity and readiness tables with separate denominators. |
| Candidate work risked duplicate seeds and facets | Canonical work identity and method-path identity are separate; delta duplicate seeds are zero and portfolio roles remain non-duplicated. |
| Stage-1B was prematurely asked to prove innovation | Novelty is explicitly out of scope for Stage-1B; Stage-1C selects the problem, and Stage-2A converges the approach after nearest-prior reproduction. |
| H5 was incomplete but risked leaking into conclusions | H5 contributes zero occupancy, headline or selection rows. Two dependent bundles are explicitly ineligible. |
| H5 packet pinned an obsolete codebook hash | Release v2 supersedes v1 solely to repair the codebook binding and include the calibration and companion packet hash; scientific counts and conclusions did not change. |
| Repeated public arXiv access was inefficient | Selected PDFs/e-prints are cached and parsed locally; ledgers and hashes preserve provenance without committing source assets. |
| Amendment chains inflated AI context | Active truth is consolidated in stable HOT/CURRENT files; reviewer transactions are cold AUDIT artifacts and the current request is immutably registered. |
| Old Stage-1A state was still encoded in current checks | Per-work state and current-surface contracts now follow the 2026-07-22 Stage-1B closeout boundary. |

## 9. Claims intentionally not made

The team does not claim:

- literature-universe closure or zero missed papers;
- resolution of the 2,633 title-only T1 identities or 232 citation-only arXiv IDs;
- forward-citation closure;
- prevalence from the 11-path strict sample;
- an empty speech-native method cell;
- H5 completion or modality-transfer evidence;
- repository availability as local reproducibility;
- project reproduction of any paper-reported metric;
- a selected problem, frozen reproduction list or technical novelty;
- whole-repository historical-test cleanliness as scientific evidence.

The load-bearing claim is narrower: the frozen Stage-1B release is sufficiently structured,
contradiction-aware and falsifiable to support a bounded Stage-1C comparison without another broad
discovery campaign.

## 10. Principal risks and stop conditions

| risk | control or stop condition |
|---|---|
| A direct prior already removes the proposed residual | Reject that bundle; do not rescue it by renaming the mechanism. |
| Evaluator errors dominate the apparent gain | Stop method development and treat evaluator reliability as the primary problem or invalidate the task setup. |
| Candidate diversity or oracle headroom is negligible | Stop external selection/search work for that task. |
| Repair damages more correct outputs than it fixes | Reject the repair policy at the preregistered harm threshold. |
| Static improvements fail on interaction quality | Reject transfer to the full-duplex objective. |
| The selected study needs hidden states, gradients or weight updates | It is outside TF-Strict and must be reframed or routed to another work. |
| New identity-level evidence changes a bundle's strongest contradiction | Supersede the Stage-1C input before selection; do not silently append an amendment. |

## 11. Evidence package for independent replay

The scientific evidence object is fixed release commit
`51b527b88e1f9993f1c2bd9d826f86c73a6a938c`. The most direct entry points are:

- `docs/checks/stage1b-closeout/2026-07-22/release-manifest.json`;
- `wiki/survey/current/tables/stage1b-mapping-release.md`;
- `wiki/survey/current/tables/stage1c-eligible-inputs.md`;
- `docs/checks/stage1b-closeout/2026-07-22/t1-rec7-closeout.json`;
- `docs/checks/stage1b-closeout/2026-07-22/t1-title-reconciliation.json`;
- `docs/checks/stage1b-closeout/2026-07-22/direct-core-citation-summary.json`;
- `wiki/audit/system-first-stage1b/stage1c-transition-request/2026-07-22-stage1c-transition-review-request.md`.

This proposal is an audit-layer submission narrative. It does not alter the release bytes. Its exact
Git blob is registered separately so that later corrections require a new dated artifact.

## 12. Requested verdict

Please return an evidence-backed value for each field against the fixed release:

```text
STAGE_1B_DISCOVERY_CLOSE        = PASS | WITHHOLD
STAGE_1B_MAPPING_CLOSE          = PASS | WITHHOLD
STAGE_1B_RECORD_RELEASE         = PASS | WITHHOLD
STAGE_1C_ELIGIBLE_INPUTS        = PASS | WITHHOLD
STAGE_1C_FORMAL_START           = SIGN | WITHHOLD
MODEL_OR_REPRODUCTION_EXECUTION = WITHHOLD
```

If a field is withheld, please identify the smallest evidence defect that blocks it. Another broad
D0 campaign should be required only if a specific omitted identity changes one of the five problem
families or invalidates a load-bearing denominator.
