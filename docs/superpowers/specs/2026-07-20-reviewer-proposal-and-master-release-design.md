# Reviewer Proposal and Master Release Design

**Date:** 2026-07-20

**Status:** Owner-approved bounded revision after independent design review

**Approved by:** repository owner

**Approval time:** 2026-07-20, Asia/Taipei

**Authority reference:** this Codex task conversation. The owner instructed “merge to remote main，
并且写一份research proposal给reviewers”, approved the three design sections, selected the
dual-decision scope, and replied “Go” to the bounded remediation route after the doctoral review.

**Approved scope:** repair the three verified Stage-1A gates below; produce and register one
reviewer-facing proposal; merge the verified remediation to the repository default branch
`origin/master`. The approval excludes GitHub Wiki publication, Stage-1B query execution,
research-model or smoke calls, dataset experiments, and prototypes.

**Frozen reviewed design:** branch `codex/stage1b-readiness-remediation`, commit
`55e283c6f53459657b88e1586a999bd7d580cf81`, Git blob
`607a2d931e3e34a397813734b6cb4f0b9f275cae`.

**Observed release baseline:** `origin/master=bb3a1200d1813547979ef62bb02c7125292b8f2e`,
merge base `4af90521e935bae5285edc322ca94cedde810174`. Implementation must fetch again and
record the actual source head, fetched remote head, merge base, merge result, gate report, registry
anchor, and remote read-back. Relevant divergence or a failed gate stops release.

## 1. Objective and success criteria

Produce one self-contained reviewer-facing proposal that supports two independent decisions:

1. whether the scientific rationale is adequate to continue systematic mapping; and
2. whether the Stage-1A search design is ready for Stage-1B execution.

The implementation transaction succeeds at `SUBMITTED_FOR_INDEPENDENT_REVIEW`, not at Stage-1B.
It must close the locally verifiable gates, register the proposal as immutable audit evidence,
publish the repository state to `origin/master`, and leave the stage explicitly unstarted and
unauthorized.

Stage-1B begins only in a later same-package transaction after all of the following exist:

1. a separate independent reviewer report with `SEARCH_DESIGN_SIGNOFF=SIGN`;
2. a separate owner record authorizing Stage-1B execution against that exact reviewed package;
3. a final committed package with `execution_authorized: true`; and
4. a fresh P0-R8/current-package PASS on that package.

Speed is binding. Do not add optional searches, a new query lane, a research-model or smoke run,
prototype work, bulk full-text rereading, or another amendment chain.

## 2. Verified design-review gates

The 2026-07-20 doctoral design review is preserved byte-for-byte at first commit under the round-13
audit namespace. It targets the frozen design above and identified three gates.

### G1 — evidence-kind/value compatibility

The current source validator admits `absence` for any required field when `note` and `scope`
are nonempty. A legitimate new-row restamp can therefore bind positive
`signal.form=text_critique` to “not contradicted” absence evidence, pass all three contract layers,
and change RQ-SYS from 5/11 to 4/11.

The repair adds an explicit `evidence kind × field × encoded value` compatibility contract:

- positive categorical values require `canon|tex|pdf_page`;
- `absence` is allowed only for semantically negative, empty, `none`, or permitted `unknown`
  values;
- an allowed absence carries encoded value, inspected scope, reason, source version, coder, and
  adjudicator provenance;
- positive signal form/source plus absence fails before derivation;
- a legitimate negative absence remains a passing positive control.

Existing signal/edge identity, strong PDF anchors, and generated headline binding stay closed and
must not be redesigned.

### G2 — review object, authority, and independence

The engineering design is not the scientific proposal and cannot be used as a verdict. The final
proposal is a new immutable audit artifact. It contains requested-response schema only:

- `REQUESTED_SCIENTIFIC_RATIONALE_FOR_CONTINUING_MAPPING`
  with response values `ADEQUATE|REVISE|INADEQUATE`;
- `REQUESTED_SEARCH_DESIGN_SIGNOFF`
  with response values `SIGN|WITHHOLD`.

`ADEQUATE` means only that the problem and hypotheses justify continued systematic mapping. It does
not establish novelty, effectiveness, SOTA, a surviving Stage-1C candidate, or a doctoral
contribution.

The actual values exist only in the later independent reviewer report. That report must state:

- reviewer stable identity and role;
- no participation in schema, generator, fixture, proposal, or remediation implementation;
- conflict-of-interest declaration;
- exact reviewed commit, proposal blob, reports, manifests, and query bytes;
- additional reviewer-side web accesses and `REVIEWER_KNOWN_ITEM` disposition;
- replay commands and observed results;
- the two bounded verdicts and rationale.

The planned report path is
`wiki/audit/system-first-stage1a/round-15/research-proposal-independent-doctoral-review.md`.
The implementation agent must not manufacture that report or its signature.

### G3 — existing-corpus disposition and current routing

The final package adds one generated CURRENT bridge instead of loading all legacy assets into AI
context. The bridge crosswalks:

- 95 canonical census works;
- 92 current seed rows;
- 65 existing bibliography rows;
- 62 legacy claim-ledger rows and their version-pin overlay;
- the current full-text ledger; and
- reviewer-known items from the two latest reviews.

Each census work appears exactly once. Each seed and bibliography row has a source identity and
destination. Exact IDs, cross-ID aliases, and unresolved identities are separate. No silent merge is
allowed. Each disposition records stable ID, version, source campaign, inherited evidence grade,
protocol-defined role, relevant RQ/proposal section, inclusion or REC-0 exclusion reason, next-stage
action, available locator, conflict status, and invalidating condition.

Allowed roles reuse protocol language: `DEEPLY_READ`, `KNOWN_QUEUE`,
`MEASUREMENT_INSTRUMENT`, and `BOUNDARY/NEGATIVE_PRIOR`. An irrelevant work receives a REC-0
exclusion reason rather than a new taxonomy label. Legacy MATERIAL, CRITICAL, UNVERIFIED, and
double-review-pending claims never become load-bearing merely by appearing in the crosswalk.

The checker proves census 95/95 dispositions, seed 92/92 destinations, bibliography 65/65 provenance
roles, and zero unexplained orphans. The generated artifact binds input paths, Git blobs, generator
version, and output hash. The proposal uses only a load-bearing minimum subset; the full disposition
remains machine data.

This is a metadata/evidence-routing preflight. It executes zero new discovery queries, performs zero
research-model or smoke calls, and does not require bulk full-text rereading.

## 3. Literature carry-forward boundary

P1 is a submission condition: carry forward the four v9 required boundary/measurement works, bind the
Reinforced Agent ACL/arXiv identity, and remove all eight “author on official page” placeholders from
the reviewer-facing bibliography.

The design review's four additional P1-high works enter as `REVIEWER_KNOWN_ITEM` with official
metadata, route, role, and boundary hypothesis:

- arXiv:2605.04531 — reward-guided training-free VLM boundary comparator;
- ACL 2025 `2025.acl-long.775` — trained agentic reward/best-of-N boundary;
- ACL 2026 `2026.acl-industry.87` — trajectory/proxy-state measurement instrument;
- arXiv:2605.23261 — trained speech reward-model measurement boundary.

P2 is explicitly nonblocking. Existing TangramSR, OrchRM, ToolRM, Agent-RRM, DuplexPO, and
Multi-Faceted Interactivity Alignment rows plus arXiv:2602.01381 and ACL 2026
`2026.acl-srw.1` enter the Stage-1B priority queue. They need correct metadata and provenance but no
Stage-1A full-text coding.

Reviewer-known items cannot alter the frozen 65-query terms or be counted as frozen-query recall.

## 4. Proposal architecture

Create the submission as the next event after the design review:

`wiki/audit/system-first-stage1a/round-14/research-proposal-and-stage1b-signoff-request.md`

The proposal has two separated tracks.

### Track A — scientific rationale for continuing mapping

Track A states the north-star question, theoretical motivation, scoped research gap, research
questions, contribution hypotheses, staged methodology, falsifiers, risks, limitations, and doctoral
research value. Contributions remain hypotheses until Stage-1B mapping and later empirical stages.
No first-ever claim is permitted.

### Track B — Stage-1B search-design readiness request

Track B maps v9 E1-E5 and P0-A/B/C to repaired contracts, demonstrated negative tests, exact machine
artifacts, Windows/WSL replay, context consolidation, frozen execution boundary, and the disclosed wiki
dry-run incident. P1 is closed before submission; P2 is shown only as a nonblocking queue.

The proposal contains a claim-diff against v9 with exact fields:

- v9 claim ID and section;
- `UNCHANGED|CORRECTED|WITHDRAWN|NEW`;
- rationale;
- canonical evidence path plus hash/locator;
- `hypothesis_only|readiness_only` stage force.

The proposal does not maintain a second numeric canon. Reader-visible numbers are generated from
persisted reports or cited through exact source bindings.

## 5. Evidence and claim flow

The proposal binds:

- purpose and program identity: `wiki/Project-Thesis.md`;
- current stage and authority: `wiki/Research-Objective.md`;
- executable mapping design: `wiki/survey/current/protocol.md`;
- v9 review and the immutable round-12 correction;
- schema-v3 evidence and Windows/WSL reports;
- integrated current-package report;
- wiki dry-run incident report;
- generated existing-corpus disposition and its source receipt;
- complete generated reviewer bibliography and opening roles;
- campaign audit index.

The repair exposure statement remains scoped: discovery queries, research-model calls, and smoke runs
are zero within this repair. Nonzero `INHERITED_PRIOR_EXPOSURE` remains unchanged.

## 6. Audit and current-state transaction

The user-provided design review is currently untracked in the primary worktree. Before first commit,
preserve its bytes and place it directly at:

`wiki/audit/system-first-stage1a/round-13/reviewer-proposal-design-stage1a-doctoral-review.md`

Do not create a committed root-level legacy path. Register its exact blob as the immutable round-13
design-review event in the append-only audit registry and campaign index.

The final proposal is the following round-14 submission, not an amendment. Its bytes become immutable
at first commit. Existing registered audit rows, including round 13, are never changed. The campaign
contract is extended narrowly so one proposal or application may be the active review transaction;
the AI manifest points to the exact round-14 proposal. A later independent report is a new round-15
event rather than an append into round 14. Generated index, current manifest, AI context manifest,
audit immutability report, and integrated package report are refreshed through their executable
contracts.

After registration:

- `wiki/Research-Objective.md` says the three local remediation gates are closed and formal review
  is submitted, while both requested reviewer judgements remain pending;
- `wiki/survey/current/status.md` carries the same short state;
- active-review routing points to the round-14 proposal;
- Stage-1B remains unstarted and unauthorized.

## 7. Release states and merge flow

State is represented by four non-equivalent labels:

1. `PACKAGE_READY_FOR_REVIEW`;
2. `SUBMITTED_FOR_INDEPENDENT_REVIEW`;
3. `REVIEWED_SIGN_OR_WITHHOLD`;
4. `OWNER_AUTHORIZED_STAGE1B`.

Remote push success changes repository availability, not scientific or reviewer verdicts.

Before merging, remove the erroneous shared `core.worktree` setting that points the primary
repository at the linked remediation worktree. Record its prior value and removal command, then prove
both worktrees resolve to their own roots and are clean.

Run on the proposal commit:

- integrated current-package gate on Windows and WSL2;
- evidence-contract, current-layer, AI-context, and current-package focused tests on both platforms;
- audit immutability and AI context surface checks;
- frozen-query and experiment-attempt-registry zero-difference checks;
- `git diff --check` and clean-status checks.

Then use WSL2 for remote operations:

1. fetch `origin` and record the actual default branch and remote head;
2. compare source head, remote head, merge base, and affected paths with the approved baseline;
3. stop on relevant divergence or reconcile benign divergence and rerun the package;
4. merge the remediation branch to local `master` with a normal merge commit;
5. rerun headline gates on the merged tree;
6. push `master` to `origin/master` without force;
7. read the remote ref and prove it equals the local merge commit.

This authorization does not include GitHub Wiki publication. A test, merge, or push failure preserves
the branch and evidence and stops the release.

## 8. Rejected expansions

- No new query lane or reverse engineering of query terms from reviewer-known papers.
- No Stage-1A full-text coding of the nonblocking P2 queue.
- No bulk rereading of the 95-work census.
- No self-authored “independent” reviewer report.
- No new macro proposal target without the v9 claim-diff.
- No amendment chain; the engineering spec is revised in place and the effective research state is
  consolidated in CURRENT.

## 9. Invalidating conditions

Stop and return to the relevant gate if the absence counterexample remains green, the crosswalk has an
unexplained orphan, a bibliography placeholder remains, a canonical report/hash changes unexpectedly,
Windows/WSL occupancy diverges, frozen query or attempt-registry bytes change, audit registration is
non-append-only, remote divergence affects the reviewed package, a reviewer identifies a new blocker,
or the owner changes the stage or authority ruling.
