---
title: "Umbrella → Studies → Papers three-stage architecture implementation review assessment"
assessment_id: "PROGRAM-THREE-STAGE-ARCHITECTURE-IMPLEMENTATION-REVIEW-2026-08-04"
date: "2026-08-04"
addressed_to: "research engineering team and research owner"
reviewed_umbrella_commit: "d5ea710"
reviewed_governance_commit: "bb164e6"
reviewed_study_commit: "0d86ddccfddd7ba3e0e3156b03b3c7f92cd21dbf"
review_scope: "three-stage carrier binding, papers workspace foundation, SAEA boundary contract, registries, active truth, executable gates, and deferred promotion infrastructure"
assessment_status: "REVIEW_COMPLETE"
verdict: "CONDITIONAL_ACCEPT__PHASE_A_BOUNDARY_LANDED__ACTIVE_TRUTH_AND_FAIL_CLOSED_COVERAGE_INCOMPLETE"
execution_authority: "REVIEW_ONLY__NO_NEW_AUTHORITY"
model_execution_effect: "NO_NEW_AUTHORITY"
remote_repository_effect: "NO_NEW_AUTHORITY"
---

# Umbrella → Studies → Papers three-stage architecture implementation review assessment

> This review targets umbrella `d5ea710` (core governance implementation commit `bb164e6`) and the current
> independent study `speech-aware-evidence-acquisition@0d86ddc`. It examines whether the engineering team
> correctly implemented the 2026-08-04 owner ruling (Decision-Log-2026-08 continuation entry 91) and its
> minimal-first implementation plan. This document gives only review conclusions, defects and acceptance
> recommendations; it does not modify owner authority and authorizes no model/API calls, experiments, remote
> repository creation, pushes, Wiki publication or paper submission.

## 1. Overall verdict

The overall conclusion is:

```text
CONDITIONAL_ACCEPT
Phase-A architecture boundary: LANDED
Three-stage current truth: INCONSISTENT
Independent study adoption: NOT LANDED
Paper zero-state machine enforcement: NOT LANDED
First paper admission readiness: WITHHELD
```

The engineering team **correctly understood and landed the core concepts of the three-stage architecture**:

- Stage‑1 = umbrella;
- Stage‑2 = `studies/<slug>`, ending at a qualified paper candidate;
- Stage‑3 = `papers/<slug>`, owning large-scale confirmatory work, final evidence, papers and publication;
- the study gate keeps `OWNER_GO_AND_EXECUTION_CONTRACT`;
- the paper gate uses the new token `OWNER_GO_AND_PAPER_EXECUTION_CONTRACT`;
- a paper's success does not require a positive improvement — positive, zero and negative results are equally
  legitimate;
- paper repos use semantic naming and independent Git/GitHub, and never use R2, a venue or a year as engineering
  identity;
- with no real candidate, only `papers/README.md` and an empty registry are created, with no pre-built empty
  paper repository;
- the existing `wiki/experiments/` and `docs/checks/` paths were not restructured;
- SAEA's current E0/R0/R1/bounded-X is retained, and paper-scale work is moved out of default authority by a
  prose contract.

This shows the team did not mechanically transcribe the proposal, and did not mistake "adding a papers root" for
immediately creating paper engineering. It followed the owner's continuation entry 91 ruling of "set the boundary
first, defer the machinery, do not over-design".

But the current state can only be accepted as **Phase A conceptual boundary landed**, and cannot be called
"three-stage engineering remediation complete". The main reason is not the explicitly deferred promotion bundle,
but that:

1. several documents still in use continue to give the old two-stage execution instructions;
2. the independent SAEA study repo has received the new Stage‑3 boundary not at all;
3. the registry's sole `decision_record` was re-pointed at a non-self-contained supplementary contract;
4. `papers/registry.json` is called a machine authority, yet no program reads or validates it;
5. the current experiment-asset contract still writes every formal experiment as study-owned;
6. the deferred trigger for confirmatory reservation comes later than Stage‑2 X, creating a sequencing risk.

None of these blocks the current purely model-free E0, but they must be closed in the layered order below before
the first executable model-facing runner, bounded X, a second shared-carrier study, or the first paper admission.

## 2. Review baseline and actual changes

### 2.1 Umbrella changes examined

18 paths changed across `d4f07fa..d5ea710`, with the core implementation in `bb164e6`:

- added `papers/README.md` and `papers/registry.json`;
- added `papers/*/` to `.gitignore`;
- `Project-Thesis`, `Research-Objective`, `wiki/Architecture` and the client guides gained the three-stage binding;
- added the SAEA Stage‑3 boundary/paper-gate contract;
- `studies/registry.json` and the experiment index re-pinned `decision_record` to the new contract;
- updated the experiment asset inventory and the AI context manifest;
- wrote the owner ruling into continuation entry 91;
- the original proposal, the adversarial review and the minimal-first plan subsequently entered Git.

### 2.2 Current physical state

- umbrella worktree: clean;
- study worktree: clean;
- `papers/` contains only the umbrella-owned README and an empty registry;
- no paper child checkout exists;
- `papers=[]` in `papers/registry.json`;
- no new paper remote has been created or pushed;
- the current formal experiment ledger is still empty.

All of the above conforms to the owner ruling of "an empty registry is legal, an empty paper repo is not" and
"do not create repositories in advance".

### 2.3 Independent verification performed here

Two gates that do not depend on WSL data paths were run first on the Windows side:

```text
code graph: PASS (22 trusted nodes)
study workspace and experiment assets: PASS
```

`legacy_asset_resolution_check.py --verify-bundles` must be run in WSL2 per repository convention; running it
directly on Windows misresolves `/mnt/e/...` as a path on the current Windows drive, which is not a defect of this
implementation. After rerunning in `Ubuntu-24.04` with `~/.venvs/speechrl`:

```text
574 bindings verified
0 unresolved
4 bundle hashes verified
AI context surface: PASS (0 failures)
AI context manifest: PASS
pytest scripts/checks: 145 passed, 202 subtests passed
pytest common/tests: 21 passed, 1 skipped
```

Every existing gate is green, but no existing gate reads `papers/registry.json` and none checks three-stage
semantic consistency. So "everything PASSes" can only prove that this change did not break the old
study/asset/context foundation; it cannot prove that the paper stage is fail closed.

## 3. Correctly implemented items

### C-1 — The three-stage responsibilities are understood correctly

`wiki/Decision-Log-2026-08.md:17-25`, `wiki/Project-Thesis.md:66-76` and `papers/README.md:9-16` describe the
three carriers, the two gates and the paper success criterion consistently. In particular they make clear that:

- a study's result is a candidate, not a finished paper by default;
- a paper owns large-scale confirmatory work and publication;
- positive, zero and negative conclusions all count as completion;
- GO for one candidate does not automatically authorize other candidates in the same study.

These are the most important semantic results of this remediation and should be retained.

### C-2 — Minimal-first did not manufacture a fake admission

The team did not create an empty paper repo, empty remote, empty CI or a fake promotion receipt just to make the
architecture "look complete". `papers/README.md:13-22` states clearly that an empty registry is legal, an empty
child repo is not, and lists the deferral triggers. This matches this program's earlier experience of "never
pre-create a repository for an unadmitted research object".

### C-3 — Existing paths and historical assets were not damaged

The team accepted adversarial review C1: the current `wiki/experiments/<study-slug>/` and `docs/checks/<campaign>/`
paths were not moved. The 574 legacy bindings, four offline bundles, study origin/branch and the AI context
manifest still verify. No historical experiment/audit bytes were rewritten for the sake of the three-stage
structure.

### C-4 — SAEA's prose stop line now exists

The new contract `2026-08-04-owner-stage3-boundary-and-paper-gate-contract.md:25-35` writes the study endpoint as
a qualified paper candidate, and places production-scale implementation, large confirmatory work, final
superiority claims and publication behind the paper gate. This is the correct direction for authority.

## 4. Findings

### P0-1 — BLOCKER: the active-stage methodology still authorizes formal Stage‑2B experiments, directly conflicting with continuation entry 91

#### Evidence

Owner continuation entry 91 states:

```text
Validation inside Stage‑2 stays bounded and contains no production-scale confirmatory work;
only Stage‑3 owns large-scale pre-registered confirmatory work, final evidence and publication.
```

But the current `wiki/Research-Methodology.md` still specifies:

- line 21: Stage‑2B = "formal experiments and statistical inference after freezing hypotheses, controls and
  criteria";
- line 22: Stage‑3 is merely "extension, independent reproduction, paper-level audit";
- line 27: technical innovation is "validated in Stage‑2B";
- line 42: Stage‑1/2A numbers are upgraded in evidence rank after being rebuilt in Stage‑2B.

This is not a wording difference but the opposite allocation of experiment authority: the old methodology allows
formal statistical validation to be completed in the study repo, whereas the new ruling requires the paper gate
and an independent paper repo.

The same stale framing still appears in:

- `README.md:19-23`: after the Stage‑2 study repo is created, "all later engineering, experiments and papers live
  there";
- `README_CN.md:17-20`: all later engineering, experiments and papers live in the study;
- `CONTRIBUTING_CN.md:33-34`: after entering Stage‑2 all work is in the study;
- `docs/architecture.md:5-11`: only two repository classes, all Stage‑2+ work lives in the study;
- `AGENTS.md:15-23` and `CLAUDE.md`: first say all later work lives in the study, then say Stage‑3 is in papers;
- `wiki/Architecture.md:26-28` and `:63-71`: both statements are retained on the same page.

#### Impact

A new collaborator could follow the current `README`, the canonical architecture or the research methodology
exactly, bypass the paper gate, run formal Stage‑2B experiments in the study repo, and produce a paper. That would
make continuation entry 91 effective only in a few HOT paragraphs rather than a program-level execution rule.

#### Required repair

Within one truth-alignment transaction:

1. Change `wiki/Research-Methodology.md`'s Stage‑2B to candidate qualification/freezing rather than final
   confirmatory work; Stage‑3 takes over formal statistical inference at adequate scale, final evidence and papers;
2. Fix the old "all later work" sentences in README/README_CN, CONTRIBUTING/CONTRIBUTING_CN,
   `docs/architecture.md`, `wiki/Architecture.md` and AGENTS/CLAUDE;
3. Update `wiki/Per-Work-Status.md` to state SAEA's current paper-scale stop line;
4. Keep historical Decision-Log entries append-only, explained only by continuation entry 91's `Supersedes` and
   current routing, never written back into old entries;
5. Rebuild the AI context manifest and run the surface/budget checks.

#### Closing gate

P0-1 closes before any executable R0/R1/X model-facing runner is delivered. Purely model-free E0 may continue.

### P0-2 — BLOCKER: the independent SAEA repo has not adopted the new Stage‑3 boundary

#### Evidence

The umbrella's three-stage ruling was committed at `bb164e6` (11:48), but the study HEAD is still the earlier
`0d86ddc` (10:43). In the study repo:

- `AGENTS.md:19-24` calls the old speech scope/identity contract the "current contract" with no Stage‑3 paper gate;
- `README.md:15-16` likewise calls the old contract the current execution authority;
- `docs/engineering.md:33-42` describes only R0 and declares no paper-scale stop line;
- `FrozenCoreGate` in `contracts.py:236-444` validates only E0 and the runtime receipt;
- `test_governance_alignment.py` only checks that the file the registry points at exists, not the semantics of the
  new boundary contract;
- the study's local agent guidance, CI and entry gate cannot distinguish `baseline/bounded-probe` from
  `paper-scale/confirmatory`.

This means that from the umbrella's viewpoint SAEA has been narrowed, but an executor who clones the study alone or
enters the study repo directly still sees only the old authority. After E0 closes, the existing model gate would
allow any runner that calls it, with no knowledge of whether the call is bounded X or a forbidden paper-scale
campaign.

#### Impact

E0 is not yet closed and the runner is not yet implemented, so no out-of-bounds execution has occurred; but once
the R0/X entry becomes runnable code, a prose contract cannot fail closed inside the independent repo. The
three-stage boundary exists only in the umbrella and has not reached the repository that actually executes.

#### Required repair

This is a cross-repository transaction and cannot be done in the umbrella alone:

1. First resolve the effective-contract problem of P1-1 in the umbrella;
2. Update AGENTS/CLAUDE, README and the engineering current authority in the SAEA repo;
3. Have the study itself design and implement a minimal execution-scope interface that can at least distinguish
   `baseline-reproduction`, `bounded-discovery-probe` and `paper-scale-confirmatory`;
4. The study repo must fail closed on the third class when there is no paper contract/paper repo; an even simpler
   implementation is for the study repo to never accept a paper-scale profile;
5. Add contract tests proving refusal for a forged stage string, an over-budget bounded plan, a confirmatory
   profile, and missing paper authority;
6. Finally, have the umbrella registry/index pin the new study commit and the effective contract.

The umbrella should not prescribe the study's internal directory layout, but it is entitled to require this
cross-repository verifiable interface through the owner contract.

#### Closing gate

P0-2 closes before the first model-facing R0/X runner becomes executable. The current model-free E0 is unblocked.

### P1-1 — MAJOR: the registry's sole decision record was changed to a non-self-contained supplementary contract

#### Evidence

`studies/registry.json:18-19` and the experiment index frontmatter currently pin:

```text
2026-08-04-owner-stage3-boundary-and-paper-gate-contract.md
```

But that file's frontmatter explicitly says:

```text
relation: supplements ...; narrows default execution authority only
```

It does not self-containedly restate:

- the `OWNER_GO_AND_EXECUTION_CONTRACT` authorization;
- the semantic repo URL / local path / package / namespace;
- the complete speech-only scope and its exclusions;
- the frozen core, data, baselines and information boundary;
- the concrete values of budgets and stop lines;
- the full path/blob of the original scope contract.

Meanwhile `Research-Objective.md:18-23`, `Experiment-Assets.md:8-16` and `studies/README.md:19-23` still treat the
original speech-domain scope/identity contract as the current authority. So the registry's "sole decision_record"
points at a different contract from the other current surfaces, and understanding the effective authority requires
following a supplement chain.

This violates this repository's rule that "active truth must be self-contained and amendment/response chains must
not serve as working context", and it weakens the audit meaning of the registry decision-record blob: the machine
proves that the supplement's bytes have not drifted, not that the complete execution contract has not drifted.

#### Repair options

Option A is preferred:

- issue a **self-contained** effective owner contract that inherits the original GO facts while completely
  restating the speech-only identity, E0/R0/R1/bounded-X, budget/exposure and the Stage‑3 stop line;
- have the registry/index pin only this one effective contract/blob;
- keep the two original contracts as historical/source records.

Acceptable option B:

- restore `decision_record` in the registry to point at the self-contained scope/identity contract;
- add a separate, machine-validated `stage_boundary_record` field in a future registry v3;
- before v3 lands, have the experiment index explicitly list both current authorities, but never call the
  supplement the sole current effective contract.

### P1-2 — MAJOR: `papers/registry.json` is called a machine authority but has no machine consumer

#### Evidence

`wiki/Experiment-Assets.md:28` calls `papers/registry.json` a Machine authority; however:

- `rg` finds no `papers/registry.json`, `paper-repository-registry` or paper workspace checker in `scripts/`, the
  tests or `docs/integrity/`;
- `study_workspace_check.py` reads only `studies/registry.json`;
- `.gitignore` already ignores `papers/*/`;
- the experiment asset inventory contains no paper registry path/hash;
- the code graph and the AI context manifest do not register the paper registry;
- every current gate still PASSes while the paper schema is entirely unchecked.

#### Impact

The current empty state contains no fake admission, so E0 is not blocked. But anyone could create an unregistered
child repo under `papers/`, the umbrella `git status` would not see it, and no existing gate would fail; the
registry schema/count could likewise be broken without tripping the current workspace checks. "Machine authority"
is at present only a prose label.

#### Suggested repair

The full promotion graph need not be implemented now, but a low-cost zero-state gate should be added immediately:

- strict JSON/duplicate-key/schema/fixed-field validation;
- `papers=[]` agrees with `Admitted paper repositories: **0**`;
- no child directory exists under `papers/`;
- `.gitignore` contains exactly `papers/*/`;
- the paper registry hash enters the deterministic asset inventory;
- negative tests cover a malformed registry, a non-empty unregistered directory and count drift.

Extending the entry schema, origin/branch, primary/supporting study, promotion receipt and `--require-installed`
can wait for a real candidate, which satisfies both the owner's minimal-first ruling and the fail-closed principle.

### P1-3 — MAJOR: Experiment-Assets' paper declarations conflict with the general experiment contract

#### Evidence

`wiki/Experiment-Assets.md:26-32` adds the paper registry and declares that a future paper experiment index lives
at:

```text
wiki/experiments/papers/<paper-slug>/
```

But in the same file:

- the authority table at lines 44-49 defines only study identity and the independent study repo;
- line 57 still says "Every formal experiment" goes into `wiki/experiments/<study-slug>/`;
- the required binding uses `study commit`, with no carrier type and no paper commit;
- the update transaction near line 98 defines only study admission, with no paper promotion transaction;
- the experiment asset inventory binds only `study_registry`.

#### Impact

When the first paper arrives, the engineering team cannot determine from the current control plane whether a paper
experiment should register a paper commit or a study commit, which update transaction to use, or whether it enters
the existing asset inventory. The new section announces a path without integrating it into the authority table and
the general experiment schema.

#### Suggested repair

Do not migrate existing study paths; only make the general terminology carrier-aware:

- `carrier_type = study | paper`;
- carrier repository URL + exact commit;
- Stage‑2 records continue under `wiki/experiments/<study-slug>/`;
- Stage‑3 records may use the already-ruled `wiki/experiments/papers/<paper-slug>/`;
- the authority table lists both study and paper code/config/tests;
- the update transaction splits into study admission and paper promotion;
- an empty paper registry also enters the asset graph hash.

### P1-4 — MAJOR / OWNER-ACCEPTED RISK: the confirmatory reservation trigger comes later than the candidate-formation process

#### Evidence

Adversarial review C2 already correctly pointed out that reservation is a Stage‑2 prerequisite, because R0/X
already establish the discovery/confirmatory boundary and multiple studies may share a carrier before any paper.
The revised review answers required creating the program ledger immediately.

Owner continuation entry 91 subsequently contracted the implementation deliberately, deferring the reservation
ledger to:

```text
a SAEA candidate entering paper-candidate-ready
or the owner starting the first paper admission
```

That deferral is a risk the owner explicitly accepted and cannot be blamed on the team as an unauthorized omission.
But the trigger still has a sequencing problem: bounded X is used to form the candidate; if reservation is not
established until the candidate is ready, selection exposure has already occurred. And if a second study shares
Earnings21/22/ConEC in the meantime, a single-repository exposure ledger cannot prevent cross-repository duplicate
consumption.

The 2026-08-03 program discipline already provides temporary protection:

- the first formal experiment ledger row must carry the split identity hash and a "consumed" marker;
- carrier selection during a new study's Stage‑1 must scan the existing experiment/exposure ledgers;
- a read-only aggregate view is created when a second study actually shares a carrier.

But the current SAEA experiment ledger header has no explicit `split identity hash` / `consumed` fields, and there
is no machine check.

#### Suggested ruling

The full reservation system in the proposal need not be implemented immediately, but the trigger should be changed
to the **earliest** of the following events:

1. before the first bounded X run reads a discovery result;
2. before a second study plans to use the same carrier/split family;
3. before the first confirmatory split is materialized, queried or read;
4. before any candidate requests `paper-candidate-ready`.

Before the ledger system lands, at minimum add split hash, role, and consumed/exposure fields to the SAEA experiment
index immediately, with a test verifying that the first formal record cannot omit them. This is the smallest safety
patch to the owner's minimal-first stance, not an early implementation of the full promotion architecture.

### P2-1 — MINOR: the canonical placement table and the contribution guide do not register the paper layer

The canonical placement table at `wiki/AI-Collaboration.md:33-42` contains only Study repository registry and Study
experiment index; the three-layer engineering asset authority likewise mentions only the study repo.
`CONTRIBUTING.md` and its Chinese version still describe the repository classes as umbrella + studies, without
stating:

- that `papers/README.md`/registry belong to the umbrella;
- that changes under `papers/<slug>/` are committed to the independent paper repo;
- that paper remote creation/push/publication still require explicit authorization;
- where the paper index, promotion receipts and releases belong.

Adversarial review C10 correctly notes that modifying the AI-Collaboration table must happen in the same commit as
the `POLICY_ROLE_ORDER`/`POLICY_ROLE_SEMANTICS` constants of `ai_context_surface_check.py` and their tests. This
work can be very small, and CONTRIBUTING's incorrect ownership model should not wait until the first paper admission
to be fixed.

### P2-2 — MINOR: the proposal/review metadata is still in its pre-ruling state

The original proposal's frontmatter is still:

```text
proposal_status: PROPOSED_FOR_REVIEW
supersession_effect: NONE_UNTIL_OWNER_ACCEPTANCE...
```

But the owner has already made a partial-accept, partial-reject and deferral ruling in continuation entry 91. The
adversarial review file is still titled "decision request", its frontmatter still says
`execution_authority: DOCUMENTATION_ONLY`, and it carries no status note at the top pointing to continuation
entry 91. The companion plan can explain the current state, but an executor must read three files to learn which
paragraphs of the proposal are in force.

The recommendation is to keep the original body and update only the frontmatter/status banner:

```text
REVIEWED__PARTIALLY_ACCEPTED_AND_OWNER_TRIMMED__SEE_DECISION_LOG_XU91
```

and to state explicitly that "sections 4/5 of the review body + owner continuation entry 91 take precedence over
the original proposal". This rewrites no historical rationale and repairs only current routing.

## 5. A fair judgment on the "deferred items"

The following were not implemented in Phase A and **should not be counted as engineering team errors**, because
owner continuation entry 91 explicitly deferred them:

- the full paper entry schema;
- the primary/supporting study graph;
- BLOCKER/RECOMMENDED grading of the 20-field candidate bundle;
- bidirectional commit binding of the promotion receipt;
- the full `paper_workspace_check --require-installed`;
- a synthetic cross-repo promotion dry run;
- study registry v3 lifecycle;
- the first paper admission runbook and CI;
- a real paper child repo/remote.

However, a deferral must satisfy two conditions:

1. the current zero state must not be described in prose as already machine-closed;
2. the trigger must come before the first irreversible action, not at the same time or later.

The P1-2 zero-state gate and the P1-4 Stage‑2 exposure prerequisite therefore still need to be handled early; the
remaining full machinery may, as the owner decided, wait for a real candidate.

## 6. Suggested remediation order

### R0 — Current truth alignment (umbrella, immediate)

Closes P0-1, P1-3, P2-1, P2-2:

- fix Research-Methodology, README, CONTRIBUTING, docs/wiki Architecture, AGENTS/CLAUDE, Per-Work;
- generalize the carrier authority in Experiment-Assets;
- update AI-Collaboration + the checker constants/tests;
- add an owner adjudication status note to the proposal/review;
- rebuild the manifest and run all umbrella gates.

This is a small transaction over documents and existing checkers; it needs no model, data, paper repo or remote
permissions.

### R1 — Self-contained authority (umbrella, immediate)

Closes P1-1: issue a self-contained effective SAEA contract or adopt the two-field schema, then re-pin the
registry/index/inventory. This step needs the owner to confirm the form of the carrier contract, but it does not
change the already-ruled research boundary.

### R2 — Independent study adoption (SAEA + umbrella, before the R0 runner)

Closes P0-2: first commit the study repo's guidance/tests/execution-scope guard and obtain the study commit; then
have the umbrella record that commit and the contract. It is not enough to announce in the umbrella that the study
has been narrowed.

### R3 — Zero-state paper gate (umbrella, near term)

Closes P1-2: validate only the empty registry, zero children, count, ignore rule and hash; the full paper schema
stays trigger-driven.

### R4 — Exposure/reservation minimum (umbrella + study, before bounded X)

Closes P1-4: extend the experiment ledger fields and tests; upgrade to a program-wide reservation/derived view when
one of the four earliest trigger events occurs.

### R5 — Full promotion machinery (at a real candidate)

Implement per the owner's Phase B: candidate schema, paper entry schema, promotion receipt, the full paper checker,
the dry run, and the first repository admission. Closing R0–R4 does not automatically authorize R5.

## 7. Acceptance criteria after repair

### 7.1 Semantic consistency

- No current onboarding/architecture/methodology page may still say that after Stage‑2 all paper work stays in the
  study;
- Stage‑2B explicitly stops at candidate qualification and does not own production-scale confirmatory work;
- Stage‑3 explicitly owns formal-scale statistical inference, final evidence and publication;
- `Per-Work-Status` and the SAEA index state the current paper-scale stop line;
- historical logs are not written back, and continuation entry 91 has clear supersession routing.

### 7.2 The independent SAEA repository

- a standalone clone's AGENTS/README reveals the current paper gate;
- the study runner cannot accept a paper-scale/confirmatory execution profile;
- contract tests fail for a forged profile, an over-budget plan and missing authority;
- the legal E0/R0/R1/bounded-X paths remain executable;
- after the study and the umbrella each commit, the registry/ledger pins exactly.

### 7.3 Paper zero state

- a malformed/duplicate-key paper registry fails;
- an unregistered child appearing under `papers/` fails;
- a mismatch between the paper count and Experiment-Assets fails;
- registry hash drift fails the asset inventory;
- an empty registry stays legal;
- creating a paper remote or child repo is not required.

### 7.4 Exposure

- the first formal study experiment must carry split hash, role and consumed/exposure;
- inherited exposure is monotonically non-decreasing;
- it can be proven before bounded X that confirmatory data is unread;
- a cross-repository read-only conflict check is produced when a second shared-carrier study arrives;
- paper promotion never re-marks already-read data as unread by changing repository.

### 7.5 Command gate

In WSL2 `Ubuntu-24.04` with `~/.venvs/speechrl`, at minimum the following must pass:

```text
python scripts/checks/code_graph_check.py
python scripts/checks/study_workspace_check.py --require-installed
python scripts/checks/legacy_asset_resolution_check.py --verify-bundles
python scripts/checks/ai_context_surface_check.py
python scripts/checks/build_ai_context_manifest.py --check
pytest scripts/checks -q
pytest common/tests -q
```

plus new equivalents of:

```text
paper zero-state registry/workspace negative tests
three-stage current-truth semantic assertions
SAEA execution-scope negative tests
split-hash / consumed / inherited-exposure record tests
```

## 8. Final determination for the engineering team

This round is not a failed implementation. The team correctly completed the minimal directory foundation the owner
explicitly approved, and did not damage the existing study, legacy assets or context gates. The results worth
keeping are: the three-stage carriers have an owner ruling, the papers root exists without any fake project, SAEA
has a paper-scale stop line at the umbrella layer, and the positive/zero/negative results policy is fixed.

But the team contracted its reading of "minimal implementation" too far: it deferred not only the future promotion
machinery but also **the complete replacement of current active truth** and **synchronizing the independent study's
execution surface**. Those two are not over-design; they are the work required to make an already-issued boundary
actually effective.

The delivery determination of this review is therefore:

```text
Phase A directory foundation: ACCEPT
Owner ruling capture: ACCEPT
No-empty-paper discipline: ACCEPT
Current-truth alignment: REJECT_PENDING_REPAIR
SAEA cross-repo boundary enforcement: REJECT_PENDING_REPAIR
Paper machine authority claim: WITHHOLD
First paper admission readiness: WITHHOLD
Current model-free E0: MAY_CONTINUE
Model-facing R0/X implementation: HOLD_BEFORE_P0-1/P0-2_CLOSE
```

The recommendation is that the team first complete one small but complete remediation round following R0→R4, and
then request an independent re-review. Do not implement real paper promotion early, and do not mark the three-stage
architecture as fully implemented merely because every old gate is currently green.
