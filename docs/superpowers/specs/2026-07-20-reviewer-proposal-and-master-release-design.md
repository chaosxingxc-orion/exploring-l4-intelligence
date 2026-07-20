# Reviewer Proposal and Master Release Design

**Date:** 2026-07-20

**Status:** Approved design

**Scope:** Complete the minimum Stage-1A submission transaction needed for independent review,
merge the verified remediation to the repository default branch, and push that branch. This design
does not authorize Stage-1B execution.

## 1. Objective and success criteria

Produce one self-contained reviewer-facing proposal that supports two independent decisions:

1. whether the research direction has sufficient scientific merit for doctoral work; and
2. whether the Stage-1A search design is ready for Stage-1B systematic-mapping execution.

The work succeeds when the proposal is registered as immutable audit evidence, HOT/CURRENT state says
that formal review has been submitted without claiming a verdict, all existing gates pass on Windows
and WSL2, the remediation is merged to the remote default branch `master`, and the remote ref is
verified. Entry into Stage-1B still requires both an independent reviewer search-design sign-off and
a separate explicit owner execution approval.

Speed is a binding constraint: do not expand Stage-1A with optional searches, new research-model or
smoke runs, prototype work, a new query universe, or another amendment chain. Submit the bounded
package as soon as the existing evidence and repository gates are green.

## 2. Chosen document architecture

Create one immutable audit artifact at:

`wiki/audit/system-first-stage1a/round-13/research-proposal-and-stage1b-signoff-request.md`

The proposal has two explicitly separated tracks.

### Track A — scientific research proposal

Track A states the north-star question, theoretical motivation, scoped research gap, research
questions, contribution hypotheses, staged methodology, falsifiers, risks, limitations, and doctoral
research value. Contributions remain hypotheses until Stage-1B mapping and later empirical stages
produce evidence. It must not make a first-ever claim or present the 11 known method paths as a
systematic-mapping population.

### Track B — Stage-1B readiness request

Track B maps the v9 review's E1-E5, P0-A/B/C, P1, and P2 requirements to the repaired contract,
demonstrated negative tests, exact machine artifacts, Windows/WSL replay, context consolidation,
frozen execution boundary, and the disclosed wiki dry-run incident. It asks for search-design
sign-off; it does not grant that sign-off.

The proposal ends with two independent reviewer verdict fields:

- `SCIENTIFIC_MERIT = ACCEPT | REVISE | REJECT`
- `SEARCH_DESIGN_SIGNOFF = SIGN | WITHHOLD`

Neither field stands in for owner authorization. Even two favorable reviewer verdicts leave
`execution_authorized: false` until the owner acts separately.

## 3. Evidence and claim flow

The proposal derives its claims from existing canonical sources rather than creating parallel truth:

- purpose and program identity: `wiki/Project-Thesis.md`;
- stage and authority: `wiki/Research-Objective.md`;
- executable mapping design: `wiki/survey/current/protocol.md`;
- requested remediation: the v9 doctoral review;
- remediation evidence: schema-v3 v6 and its Windows/WSL reports;
- integrated technical state: the current-package report;
- integrity disclosure: the wiki dry-run incident report;
- historical routing: the campaign audit index.

Numeric values, hashes, and PASS claims cite machine reports. The proposal does not maintain a second
numeric canon. The E1-E5 closure matrix uses the fixed structure “original counterexample -> repaired
contract -> demonstrated failing fixture -> current evidence.” Scientific statements state their
evidence mode and limitations.

The repair exposure statement is scoped and exact: discovery queries, research-model calls, and smoke
runs are zero within this repair. That statement does not erase nonzero
`INHERITED_PRIOR_EXPOSURE`.

## 4. Audit and current-state transaction

The proposal is an ordinary round-13 review submission, not an amendment. Its bytes become immutable
at first commit. Its Git blob is appended to the audit-artifact registry and the round-13 campaign
index without modifying existing registered rows. The generated campaign index and AI context routing
are refreshed through their existing executable contracts.

After registration, supersede current state in place:

- `wiki/Research-Objective.md` says internal adversarial review and completion verification are
  complete, formal dual-verdict review is submitted, and both reviewer verdicts remain pending;
- `wiki/survey/current/status.md` carries the same bounded state in short form;
- the active-review transaction points to the round-13 proposal;
- Stage-1B remains unstarted and unauthorized.

A later reviewer report is appended as a separate immutable round-13 artifact. It never rewrites the
proposal. A failed gate produces `SEARCH_DESIGN_SIGNOFF = WITHHOLD` but does not force the scientific
merit verdict to the same value.

## 5. Verification and release flow

Before merging, remove the erroneous shared-repository `core.worktree` setting that points the main
repository at the linked remediation worktree. Verify both the primary worktree and linked worktree
resolve to their own roots and are clean. This is an environment-state repair; it does not change
tracked research content.

Run on the proposal commit:

- the integrated current-package gate on Windows and WSL2;
- current-layer, AI-context, and current-package focused tests on both platforms;
- audit immutability and AI context surface checks;
- frozen-query and experiment-attempt-registry zero-difference checks;
- `git diff --check` and clean-status checks.

Then use WSL2 for remote Git operations:

1. fetch `origin` and confirm its default branch is still `master`;
2. confirm the primary worktree is clean and reconcile any newly arrived remote commits;
3. merge the remediation branch to local `master` with a normal merge commit;
4. rerun headline gates on the merged tree;
5. push `master` to `origin/master` without force;
6. read the remote ref and prove it equals the local merge commit.

This authorization does not include publishing the GitHub Wiki. A test, merge, or push failure stops
the release and preserves the branch and evidence for diagnosis.

## 6. Rejected alternatives

- **Two companion documents:** gives stronger physical separation but increases reviewer navigation
  and creates another coordination point at the final gate.
- **Short cover plus canonical links:** is smaller but is not self-contained and repeats the exact
  context-dependency failure this consolidation was designed to remove.

The selected single-document, dual-verdict structure is the shortest path to review without
conflating scientific merit, search-design sign-off, or owner execution authority.

## 7. Invalidating conditions

Stop and return to the relevant gate if any canonical report or hash changes, Windows/WSL occupancy
diverges, frozen query or attempt-registry bytes change, audit registration is non-append-only, the
remote default branch changes, a reviewer identifies a new blocker, or the owner changes the stage or
authority ruling.
