# Reviewer Proposal and Master Release Design

**Date:** 2026-07-20

**Status:** Owner-approved bounded revision after two independent pre-proposal reviews

**Authority:** The owner authorized a reviewer-facing research proposal, merge/push to the repository default branch, selected the dual-decision scope, and replied “好，继续吧” after receiving the final-gates plan review. This authority covers only Stage-1A remediation, proposal submission, repository merge, and `origin/master` push. It excludes systematic-query execution, research-model or smoke calls, metrics, prototypes, Stage-1B authorization, and GitHub Wiki publication.

**Frozen review objects:**

- design reviewed at `55e283c6f53459657b88e1586a999bd7d580cf81`, blob `607a2d931e3e34a397813734b6cb4f0b9f275cae`;
- first implementation plan reviewed at `17e230f673ee27efb5e74f6fbfab15c7061d22da`, blob `8081134013e5e47f2bb5b9cdf1e770a1276fd972`;
- design review registered in round 13;
- plan review registered in round 14.

The commit containing this revised design and revised plan becomes `IMPLEMENTATION_FREEZE`. It is distinct from the evidence-v6 release anchor, the reviewed-plan anchor, the fetched pre-merge master, and the final merge commit.

## 1. Objective and authority boundary

Produce one self-contained proposal that lets an independent reviewer answer two separate questions:

1. Is the scientific rationale adequate to continue systematic mapping?
2. Is the Stage-1A search design ready for Stage-1B execution?

The implementation transaction ends at:

```text
FOUR_IMPLEMENTATION_FINDINGS_REMEDIATED
FORMAL_INDEPENDENT_REVIEW_PENDING
SUBMITTED_FOR_INDEPENDENT_REVIEW
```

It does not end at formal gate closure or Stage-1B readiness. Stage-1B begins only after a later independent report gives search-design `SIGN`, the owner separately authorizes the exact reviewed package, the committed package records `execution_authorized=true`, and the final package gate passes. Stage-1B remains systematic mapping only and still forbids research-model/smoke execution.

Speed is binding. Do not add a query lane, run a frozen query, bulk-reread the corpus, or upgrade non-load-bearing P2 items merely to make the package look comprehensive.

## 2. Four verified implementation gates

### GM-1 — lossless existing-corpus disposition

The legacy bridge is a canonical-work union graph, not one flat record per census work. It covers every source row exactly once across:

- 95 census rows;
- 92 seed rows;
- 65 bibliography rows;
- 62 claim rows;
- 30 version-pin rows;
- 129 fulltext-ledger events; and
- the exact frozen reviewer-known-item artifact.

Each canonical node has an identity list, source-row memberships, screening decision, reference role, per-claim evidence list, and current disposition. Claim grades/statuses remain per claim; no “best”, “worst”, or arbitrary work-level scalar replaces them.

Canonical reference roles are exactly `DEEPLY_READ`, `KNOWN_QUEUE`, `MEASUREMENT_INSTRUMENT`, and `BOUNDARY_COMPARATOR`. `EXCLUDE` requires a REC-0 reason and null role. `INCLUDE` requires a canonical role. `UNRESOLVED` carries source, reason, owner, deadline gate, and next action; any load-bearing unresolved blocks submission.

Exact ID, explicit alias, and unresolved identity remain distinct. `unexplained_orphans=0` means only that every source row has an explicit destination; it does not mean every paper is verified, included, or deeply read.

### GM-2 — field-specific negative-evidence contract

There is no global absence value whitelist. Only the seven observed `(field, encoded value)` pairs may use absence evidence:

- `human_or_dev_label_model_selection=false`;
- `selection_object=none`;
- `explicit_candidate_pool_selection=false`;
- `inference_external_new_information=false`;
- `external_component_weight_update=false`;
- `controller_program_or_config_optimized_on_labels=false`;
- `decision_rights=[]`.

Each field has an explicit proof obligation naming inspected sections/pages, terms/tables, acceptable explicit-negative evidence, immutable fulltext SHA-256, and conditions forcing `UNRESOLVED`. `unknown`, missing, empty, not-fetched, unreachable, not-coded, and not-applicable cannot support a load-bearing scientific absence.

Every absence entry binds the owner row, owner sidecar, immutable fulltext identity/hash, coder, proof obligation, exact inspected locators, row hash, adjudication row, and `AGREE` verdict. The validator cross-checks these objects rather than checking nonempty strings. Actor independence is a named team attestation with identity, nonparticipation scope, timestamp, and conflict declaration; it is not labelled machine-proved.

The 22 current absence rows require fresh per-row semantic review under the new obligation. A hash-delta-only review is insufficient. Weak “not contradicted” or “not seen” prose cannot automatically support a load-bearing negative.

### GM-3 — cross-platform Git preflight and evidence DAG

Before any WSL gate, native Windows and WSL2 must directly resolve the primary repository and linked worktree to the correct root, HEAD, selected blobs, and status. The shared `core.worktree` redirect is removed, and the linked-worktree gitfile uses a cross-platform relative gitdir. Local Git metadata is not uploaded as scientific evidence; the committed preflight receipt records only resolved results and named anchors.

Evidence-v7 has this topology:

```text
same frozen inputs
  ├─ Windows runner -> NT leaf
  └─ WSL2 runner    -> POSIX leaf
                         ↓
separate final aggregator consumes both exact leaf bytes
  -> compares input hashes, runner/contract version, platform stamp,
     named failures, occupancy, and output semantics
  -> canonical aggregate
```

Platform runners never claim cross-platform equality. The aggregate is generated last. Current manifest binds aggregate and both leaves. Deleting/replacing a leaf or changing an input hash, platform stamp, named failure, or occupancy fails closed.

### GM-4 — independent metadata receipts and system-first citation closure

Bibliography metadata comes from saved official arXiv/ACL payloads and normalized receipts, not duplicate constants in generator and test. Each receipt records official URL, access time, access class, source version, raw response SHA-256, stable identity, title, and authors. Tests recompute output from the receipt.

Known-ID accesses are registered as `ID_DEREFERENCE`, `PROVENANCE_FETCH`, or `REVIEW_CLAIM_VERIFICATION`. They are not systematic discovery and receive no frozen-query recall credit, but they are not silently described as zero network access.

Reviewer-visible closure presents three evidence chains:

1. system-first speech/omni agent neighbors;
2. reward and verification mechanisms;
3. training-free and trained boundary comparators.

Existing direct neighbors that must be routed include AudioToolAgent, Audio-Mind, Agent-Omni, EChO-Agent, AuTAgent, Speech-Copilot, VoxMind, WavReward, and GSRM. The earlier P1/P2 set remains. `2508.16665` enters the verification/taxonomy chain; `2510.18982` and `2509.25845` are nonblocking P2 reviewer-known items. Only a source used for a load-bearing round-15 gap/boundary claim must reach D2 before submission.

## 3. Proposal architecture

Create:

`wiki/audit/system-first-stage1a/round-15/research-proposal-and-stage1b-signoff-request.md`

Track A states the north-star question, theoretical motivation, scoped gap, research questions, contribution hypotheses, staged methodology, falsifiers, risks, limitations, and doctoral value. Contributions remain hypotheses until Stage-1B mapping and later empirical stages. No first-ever, SOTA, established novelty, or established effectiveness claim is permitted.

Track B maps v9 E1–E5 and P0-A/B/C plus the round-13/14 findings to exact contracts, negative tests, machine artifacts, Windows/WSL replay, context consolidation, frozen execution boundary, and wiki dry-run incident.

The proposal exposes response schemas only:

```text
REQUESTED_SCIENTIFIC_RATIONALE_FOR_CONTINUING_MAPPING = ADEQUATE|REVISE|INADEQUATE
REQUESTED_SEARCH_DESIGN_SIGNOFF = SIGN|WITHHOLD
```

Actual values exist only in the future independent report:

`wiki/audit/system-first-stage1a/round-16/research-proposal-independent-doctoral-review.md`

The v9 claim diff records claim ID/section, `UNCHANGED|CORRECTED|WITHDRAWN|NEW`, rationale, canonical evidence path plus hash/locator, and `hypothesis_only|readiness_only`. Reader-visible numbers are generated from persisted reports or cited through exact bindings; the proposal does not create a second numeric canon.

Load-bearing citations must bind claim ID, evidence grade, immutable version, and locator. Non-load-bearing P2 items may remain queued.

## 4. Evidence and exposure flow

The proposal binds Project-Thesis, Research-Objective, current protocol/status, v9 proposal/review/response, round-12 correction, round-13/14 reviews, evidence-v7 aggregate and leaves, context-v2 package report, context-v1 incident, lossless union graph and receipt, official metadata receipts, complete bibliography/opening roles, frozen query bytes, campaign audit index, and named Git anchors.

The exposure statement is scoped and typed:

- systematic discovery queries executed in this repair: zero;
- research-model calls: zero;
- smoke runs: zero;
- known-ID metadata/provenance accesses: reported by access class and receipt;
- inherited prior exposure: unchanged and nonzero.

## 5. Audit transaction and current routing

Registered events are immutable and each registry-growth commit appends exactly one artifact:

- round 13: design review;
- round 14: implementation-plan review;
- round 15: proposal submission and active review transaction;
- round 16: future independent proposal review.

The campaign checker is extended narrowly so one later proposal/application may be the active review transaction. Round 15 is committed with its registry row, campaign event, and prefix anchors; the immutability report is regenerated only after the registered artifact exists at HEAD, as required by the current checker.

After proposal registration, Research-Objective and current status say only that four implementation findings were remediated and formal independent review is pending. Active review routing points to round 15. Stage-1B remains unstarted and unauthorized.

## 6. Release verification and merge

Five named anchors have separate meanings: evidence-v6 release, reviewed plan, implementation freeze, pre-merge master, and merge head. Every receipt binds the implementation freeze. Release-range checks use explicit commit ranges; a clean worktree alone is insufficient.

Before merge:

- Windows and WSL preflight pass;
- four gate checkers pass;
- hostile review records every finding/repair and completes one zero-new-finding round;
- evidence-v6/context-v1/query/attempt bytes are unchanged;
- audit and campaign indexes pass;
- round-16 review and owner authorization are absent;
- both worktrees are clean.

Fetch `origin`, record actual default branch and remote head, stop on relevant divergence, merge with a normal merge commit, rerun headline gates on the merged tree, run `git diff --check PRE_MERGE_MASTER..MERGE_HEAD`, push `master` without force, and prove remote readback equals the merge commit. GitHub Wiki remains untouched.

Remote push changes repository availability only. It does not create reviewer `SIGN`, owner authorization, or Stage-1B start.

## 7. Rejected expansions and invalidating conditions

Rejected:

- new query lanes or reverse-engineering query terms from reviewer-known papers;
- systematic query execution;
- model/smoke/metric/prototype work;
- bulk fulltext rereading;
- requiring all P2 items to reach D2;
- self-authored round-16 verdict;
- force push, audit rewrite, or GitHub Wiki publication;
- another amendment chain.

Stop if cross-platform Git fails, absence proof is weak or misbound, a load-bearing row is unresolved, platform leaves diverge, the union graph loses/duplicates a source row, metadata lacks official receipt, system-first closure silently omits a direct neighbor, a load-bearing citation lacks grade/version/locator, a frozen execution surface changes, an audit append violates its one-row transaction, local PASS is phrased as formal sign-off, or relevant remote divergence appears.
