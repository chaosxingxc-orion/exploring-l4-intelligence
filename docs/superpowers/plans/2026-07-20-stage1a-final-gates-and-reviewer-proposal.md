# Stage-1A Final Gates and Reviewer Proposal Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remediate the four independently reproduced implementation findings, submit one immutable dual-track proposal for independent review, and publish the verified Stage-1A package to `origin/master` without claiming formal sign-off or starting Stage-1B.

**Architecture:** Repair the execution substrate first. Current evidence remains row-bound but gains a field-specific negative-evidence contract and cross-artifact validation. Legacy survey assets are connected through a lossless canonical-work union graph whose source rows and per-claim evidence remain explicit. Platform runners produce two leaf reports; a separate final aggregator alone may claim cross-platform consistency. Bibliography is generated from frozen official metadata receipts and exposes system-first, reward/verification, and training-free-boundary chains. Registered evidence-v6/context-v1 artifacts remain byte-identical.

**Tech Stack:** Python standard library, JSON/JSONL/Markdown, `unittest`, Git blob immutability, native Windows Git/Python, WSL2 Ubuntu-24.04 Python 3.12, official arXiv/ACL metadata endpoints.

**Design spec:** `docs/superpowers/specs/2026-07-20-reviewer-proposal-and-master-release-design.md`

---

## Frozen identities and authority

- `EVIDENCE_V6_RELEASE_ANCHOR=2f16b23`: used only to prove evidence-v6 and frozen-query/attempt bytes remain unchanged.
- `PLAN_REVIEW_ANCHOR=17e230f673ee27efb5e74f6fbfab15c7061d22da`: exact plan reviewed in round 14.
- `IMPLEMENTATION_FREEZE`: the commit containing this revised plan and revised design; Task 0 records its exact value and every generated receipt binds it.
- `PRE_MERGE_MASTER`: fetched `origin/master` immediately before merge.
- `MERGE_HEAD`: local merge commit verified before push.
- Round 13: `wiki/audit/system-first-stage1a/round-13/reviewer-proposal-design-stage1a-doctoral-review.md`.
- Round 14: `wiki/audit/system-first-stage1a/round-14/stage1a-final-gates-plan-doctoral-adversarial-review.md`.
- Round 15: future proposal submission.
- Round 16: future independent proposal review; the implementation actor must not create it.

The package may say only:

```text
FOUR_IMPLEMENTATION_FINDINGS_REMEDIATED
FORMAL_INDEPENDENT_REVIEW_PENDING
STAGE_1B_UNSTARTED_AND_UNAUTHORIZED
```

---

## File map

**Create**

- `scripts/checks/sf_cross_platform_git_preflight.py`
- `scripts/checks/test_sf_cross_platform_git_preflight.py`
- `docs/checks/system-first-stage1a/context-v2/git-anchor-receipt.json`
- `scripts/survey/sf_absence_provenance_migrate.py`
- `scripts/survey/test_sf_absence_provenance_migrate.py`
- `wiki/survey/current/data/absence-evidence-adjudication-v2.json`
- `scripts/survey/sf_identity_taxonomy_v7_test.py`
- `scripts/survey/test_sf_identity_taxonomy_v7_harness.py`
- `scripts/survey/sf_evidence_v7_aggregate.py`
- `scripts/survey/test_sf_evidence_v7_aggregate.py`
- `docs/checks/system-first-stage1a/evidence-v7/identity-taxonomy-v7-test.nt.json`
- `docs/checks/system-first-stage1a/evidence-v7/identity-taxonomy-v7-test.posix.json`
- `docs/checks/system-first-stage1a/evidence-v7/identity-taxonomy-v7-test.json`
- `scripts/survey/sf_existing_corpus_disposition.py`
- `scripts/survey/test_sf_existing_corpus_disposition.py`
- `wiki/survey/current/data/existing-corpus-disposition-v1.json`
- `docs/checks/system-first-stage1a/context-v2/existing-corpus-disposition-check.json`
- `wiki/survey/current/data/reviewer-known-items-v2.json`
- `wiki/survey/current/data/official-metadata-receipts-v1.jsonl`
- `wiki/survey/current/data/official-metadata/*`
- `scripts/survey/test_sf_bibliography_generator.py`
- `wiki/survey/current/bibliography.md`
- `scripts/survey/sf_reviewer_proposal_check.py`
- `scripts/survey/test_sf_reviewer_proposal_check.py`
- `wiki/survey/current/data/reviewer-proposal-source-manifest-v1.json`
- `docs/checks/system-first-stage1a/context-v2/reviewer-proposal-check.json`
- `wiki/audit/system-first-stage1a/round-15/research-proposal-and-stage1b-signoff-request.md`
- `docs/checks/system-first-stage1a/context-v2/current-package-check.json`
- `docs/checks/system-first-stage1a/context-v2/hostile-review-ledger.json`

**Modify**

- `scripts/survey/sf_evidence_contract.py` and its tests.
- current schema-v3 sidecars and generated coding projection.
- `scripts/survey/sf_bibliography_generator.py`.
- campaign/current/AI manifest builders and tests.
- audit registry/index/anchors and generated receipts.
- `wiki/survey/current/{manifest.json,README.md,status.md,tables/opening-guarantees.md}`.
- `wiki/Research-Objective.md`.

**Never modify**

- registered audit artifact bytes, evidence-v6, or context-v1;
- `wiki/survey/2026-07-15-sf-queries.jsonl` or its compiler semantics;
- `docs/integrity/experiment_attempt_registry.jsonl`;
- any research-model, smoke, metric, headroom, prototype, or Stage-1B execution surface;
- GitHub Wiki;
- the round-16 independent review path.

---

### Task 0: Repair and freeze the cross-platform Git substrate

**User journey:** As a reviewer, I can resolve the same repository, commit, blob, and clean status from Windows and WSL before trusting any platform receipt.

- [ ] Add `test_sf_cross_platform_git_preflight.py` first. It must fail when a linked-worktree gitfile contains a Windows absolute `gitdir`, when shared `core.worktree` redirects the primary repository, when either platform resolves a different HEAD/blob, or when required anchor names are missing.
- [ ] Run the red test:

```powershell
python -m unittest scripts.checks.test_sf_cross_platform_git_preflight -v
```

- [ ] Record the current `.git` gitfile and shared `core.worktree` only in a local before/after diagnostic; do not publish raw local Git metadata as research evidence.
- [ ] Unset the erroneous shared `core.worktree`. Use `apply_patch` to replace the linked-worktree gitfile with the relative path `../../.git/worktrees/stage1b-readiness-remediation`, then verify native Windows and WSL direct Git commands; do not rely on a hidden one-off shell wrapper.
- [ ] Implement the read-only preflight. Its committed receipt records platform, resolved root, HEAD, selected blob, clean status, and the five named anchor values; it does not record machine-specific `.git` bytes.
- [ ] Verify both platforms:

```powershell
python scripts/checks/sf_cross_platform_git_preflight.py --check
wsl -d Ubuntu-24.04 bash -lc "source ~/.venvs/speechrl/bin/activate && cd /mnt/d/chao_workspace/exploring-l4-intelligence/.worktrees/stage1b-readiness-remediation && python scripts/checks/sf_cross_platform_git_preflight.py --check"
```

Expected: both direct Git contexts resolve the feature worktree and the same `IMPLEMENTATION_FREEZE`. No later WSL task runs until this passes.

---

### Task 1: Implement field-specific absence compatibility and cross-binding

**User journey:** As a coder, I cannot use missing, unknown, weak, or unrelated evidence to support a load-bearing negative field.

- [ ] Add red unit tests to `test_sf_evidence_contract.py` for positive categorical absence, `unknown`, `None`, empty string, wrong fulltext hash, wrong sidecar, wrong row hash, adjudication artifact missing the row, verdict other than `AGREE`, URL/locator used instead of content hash, weak `not contradicted`, and coder/adjudicator actor collision.
- [ ] Define only these currently observed allowed pairs; no global fallback set exists:

```python
ABSENCE_ALLOWED_VALUES = {
    "human_or_dev_label_model_selection": (False,),
    "selection_object": ("none",),
    "explicit_candidate_pool_selection": (False,),
    "inference_external_new_information": (False,),
    "external_component_weight_update": (False,),
    "controller_program_or_config_optimized_on_labels": (False,),
    "decision_rights": ([],),
}
```

- [ ] Define a proof obligation for each field. Each obligation names required inspected sections/pages, search terms or tables, acceptable explicit-negative evidence, immutable fulltext SHA-256, and the condition that forces `UNRESOLVED`. `unknown`, not-fetched, unreachable, not-coded, and not-applicable never support load-bearing absence.
- [ ] Require every absence entry to bind `proof_obligation_id`, exact inspected locators, immutable fulltext identity/hash, owner sidecar path, coder identity, row hash, and adjudication row ID.
- [ ] Make the validator load the owner sidecar and adjudication artifact and prove all bindings. It may prove binding consistency; actor independence is labelled `TEAM_ATTESTATION`, not machine proof.
- [ ] Run red, implement minimally, then green:

```powershell
python -m unittest scripts.survey.test_sf_evidence_contract scripts.survey.test_sf_identity_taxonomy_v6_contract -v
```

- [ ] Commit the contract and tests before migrating data.

---

### Task 2: Prepare 22 proofs and obtain fresh semantic adjudication

**User journey:** As an independent semantic reviewer, I inspect the actual negative-evidence obligation and source for every changed row, not merely a hash delta.

- [ ] Add migration tests proving exactly 22 source entries, seven allowed field/value pairs, zero positive/unknown/missing absence, stable `(method_path_id, owner, field, kind, value)` tuples, deterministic output, and no frozen-query access.
- [ ] Implement `sf_absence_provenance_migrate.py --check|--write`. It may prepare proof records and restamp rows but must not assign a new semantic verdict.
- [ ] For each entry, bind the sidecar `fulltext.sha256`; a canonical locator alone is insufficient. If the immutable fulltext is unavailable or the field obligation cannot be completed, mark the row non-load-bearing/`UNRESOLVED` and make the proposal package fail if it would support a load-bearing claim.
- [ ] A fresh non-implementer reviews all 22 records against the field-specific obligation and source. Their artifact contains stable identity, reviewed commits/blobs, nonparticipation scope, conflict declaration, timestamp, per-row reason, `AGREE|DISAGREE`, and `TEAM_ATTESTATION` independence classification.
- [ ] Validation must reject incomplete coverage, actor collision, wrong hash/path, weak proof, or any `DISAGREE`.
- [ ] Run:

```powershell
python -m unittest scripts.survey.test_sf_absence_provenance_migrate -v
python scripts/survey/sf_absence_provenance_migrate.py --check
python scripts/survey/sf_coding_generator.py --check
```

Do not continue to proposal construction until all load-bearing rows are independently `AGREE` or conservatively downgraded.

---

### Task 3: Build evidence-v7 as a real two-leaf DAG

**User journey:** As a reviewer, the canonical evidence report proves equality of two exact platform leaf reports rather than relabelling a Windows rerun.

- [ ] Add v7 harness tests for the reviewer’s positive-absence mutation and a legitimate field-specific negative control.
- [ ] Add aggregator tests before implementation. Deleting or replacing either leaf, altering input hash, runner/contract version, platform stamp, named failures, occupancy, or output semantics must fail.
- [ ] Each platform runner writes only its leaf. Both leaves bind the same frozen inputs, runner blob, contract version, adjudication artifact, and `IMPLEMENTATION_FREEZE`.
- [ ] Generate leaves in this order:

```powershell
python scripts/survey/sf_identity_taxonomy_v7_test.py --leaf --output docs/checks/system-first-stage1a/evidence-v7/identity-taxonomy-v7-test.nt.json
wsl -d Ubuntu-24.04 bash -lc "source ~/.venvs/speechrl/bin/activate && cd /mnt/d/chao_workspace/exploring-l4-intelligence/.worktrees/stage1b-readiness-remediation && python scripts/survey/sf_identity_taxonomy_v7_test.py --leaf --output docs/checks/system-first-stage1a/evidence-v7/identity-taxonomy-v7-test.posix.json"
python scripts/survey/sf_evidence_v7_aggregate.py --write
python scripts/survey/sf_evidence_v7_aggregate.py --check
```

- [ ] The aggregator runs last and consumes the exact two leaf bytes. Current manifest binds all three reports. Expected scientific occupancy remains `RQ-SYS 5/11`, `reward_guided_selection 4/11`, `trajectory_pool 2/11`; equality is proved NT=POSIX and each leaf=v6 occupancy.
- [ ] Prove `git diff EVIDENCE_V6_RELEASE_ANCHOR..HEAD -- docs/checks/system-first-stage1a/evidence-v6` is empty.

---

### Task 4: Generate a lossless existing-corpus union graph

**User journey:** As a researcher, every inherited source row has exactly one explicit destination without collapsing heterogeneous claims, grades, or conflicts.

- [ ] Add red tests using real heterogeneous cases including `P-0031`, `P-0005`, `P-0071`, and `P-0080`. A flat best/worst grade, lost claim row, generic unresolved bucket, excluded item with a positive role, or duplicated source membership must fail.
- [ ] Freeze `reviewer-known-items-v2.json` with schema, exact path, generation rule, source provenance, SHA-256, access class, and `query_recall_credit=false` where applicable.
- [ ] Implement canonical nodes with this shape:

```json
{
  "canonical_work_id": "stable graph node",
  "identities": [{"source_id": "...", "relation": "EXACT_ID|EXPLICIT_ALIAS|UNRESOLVED", "provenance": "..."}],
  "source_memberships": [{"campaign": "census|seed|bibliography|claim|version_pin|fulltext|reviewer_known", "source_row_id": "..."}],
  "screening_decision": "INCLUDE|EXCLUDE|UNRESOLVED",
  "reference_role": "DEEPLY_READ|KNOWN_QUEUE|MEASUREMENT_INSTRUMENT|BOUNDARY_COMPARATOR|null",
  "claim_evidence": [{"claim_id": "...", "evidence_grade": "...", "discrepancy_status": "...", "locator": "...", "version": "..."}],
  "current_disposition": {"reason": "...", "next_action": "...", "invalidating_condition": "..."}
}
```

- [ ] Require every nonblank source row exactly once: census 95, seed 92, bibliography 65, claim 62, version pin 30, fulltext ledger 129, plus the exact frozen reviewer-known denominator. These are source-row denominators, not assumed identical work sets.
- [ ] `EXCLUDE` requires REC-0 reason and `reference_role=null`; `INCLUDE` requires a canonical role. Unresolved records carry count, source, reason, owner, deadline gate, and next action. Any load-bearing unresolved fails the package.
- [ ] Report `arXiv identity count` and `version-pinned count` separately and test set equality before ever combining them.
- [ ] Emit the graph plus a source receipt with Git blobs/SHA-256 and run:

```powershell
python -m unittest scripts.survey.test_sf_existing_corpus_disposition -v
python scripts/survey/sf_existing_corpus_disposition.py --write
python scripts/survey/sf_existing_corpus_disposition.py --check
```

`unexplained_orphans=0` means only that every source row has an explanation; it never means every paper is verified or deeply read.

---

### Task 5: Generate bibliography from official receipts and restore system-first balance

**User journey:** As a reviewer, citation metadata is independently reproducible and the proposal’s system thesis is situated against direct speech/omni agent systems as well as reward methods.

- [ ] Add tests that fail when generator constants are used as the metadata oracle, a raw official payload/response hash is absent, an official identity does not round-trip, a placeholder remains, or a reviewer-known item receives query recall credit.
- [ ] Fetch only known IDs from official arXiv export/Atom or ACL Anthology BibTeX/pages. Store raw payload snapshots and normalized receipts with URL, access timestamp, access class (`ID_DEREFERENCE|PROVENANCE_FETCH|REVIEW_CLAIM_VERIFICATION`), source version, raw SHA-256, title, authors, and identity. These accesses are not discovery queries and are not reported as zero network exposure.
- [ ] Route the existing direct neighbors AudioToolAgent, Audio-Mind, Agent-Omni, EChO-Agent, AuTAgent, Speech-Copilot, VoxMind, WavReward, and GSRM into the graph and reviewer bibliography.
- [ ] Retain prior P1/P2 items. Add Trust but Verify (`2508.16665`) to the verification/taxonomy chain; add `2510.18982` and `2509.25845` as nonblocking P2 reviewer-known items. None alters the 65 frozen queries.
- [ ] Opening roles visibly cover three chains: system-first direct neighbors, reward/verification mechanisms, and training-free/trained boundary comparators.
- [ ] Only works used by round-15 load-bearing gap/boundary claims must reach D2 before submission. Other P2 items remain `KNOWN_QUEUE` or `BOUNDARY_COMPARATOR` with an explicit next action.
- [ ] Generate and verify:

```powershell
python -m unittest scripts.survey.test_sf_bibliography_generator -v
python scripts/survey/sf_bibliography_generator.py --write --output wiki/survey/current/bibliography.md
python scripts/survey/sf_bibliography_generator.py --check --output wiki/survey/current/bibliography.md
```

---

### Task 6: Build the dual-track proposal and source manifest

**User journey:** As an independent reviewer, I can separately judge the scientific rationale for continuing mapping and the Stage-1B search design without encountering a prefilled verdict.

- [ ] Add proposal checker tests first. Reject missing Track A/B, actual reviewer verdicts, Stage-1B authorization/start claims, missing owner provenance, incomplete v9 claim diff, unbound number, unsupported novelty/SOTA language, low-grade load-bearing citation, reviewer-known recall credit, or omitted incident/exposure statement.
- [ ] Build a source manifest binding Project-Thesis, Research-Objective, current protocol/status, v9 proposal/review/response, round-12 correction, round-13/14 reviews, evidence-v7 aggregate and leaves, union graph/receipt, official metadata receipts, bibliography/opening roles, context-v1 incident, frozen query bytes, campaign index, and named Git anchors.
- [ ] Write `wiki/audit/system-first-stage1a/round-15/research-proposal-and-stage1b-signoff-request.md` with:

```text
REQUESTED_SCIENTIFIC_RATIONALE_FOR_CONTINUING_MAPPING = ADEQUATE|REVISE|INADEQUATE
REQUESTED_SEARCH_DESIGN_SIGNOFF = SIGN|WITHHOLD
```

These are response schemas only. Actual values exist only in round 16.
- [ ] Track A contains question, motivation, scoped gap, RQs, hypotheses, staged method, falsifiers, risks, limitations, and doctoral value. Track B maps v9 E1–E5 and P0-A/B/C plus round-13/14 findings to exact contracts and replay evidence.
- [ ] The v9 claim-diff columns are exact claim ID/section, `UNCHANGED|CORRECTED|WITHDRAWN|NEW`, rationale, evidence path+hash/locator, and `hypothesis_only|readiness_only`.
- [ ] The exposure statement says zero systematic discovery-query execution and zero research-model/smoke calls in this repair, while listing nonzero metadata/provenance accesses and unchanged `INHERITED_PRIOR_EXPOSURE`.
- [ ] Run proposal tests/checker. Keep the proposal uncommitted until the audit registration transaction.

---

### Task 7: Register round 15 and publish context-v2

**User journey:** As a maintainer, the proposal becomes immutable at first commit and current state points to exactly that submission while reviewer and owner decisions remain pending.

- [ ] Add campaign tests proving one proposal/application may become the later `ACTIVE_REVIEW_TRANSACTION`, a review cannot, and round 16 must be a new event.
- [ ] Compute the proposal Git blob before commit, append exactly one registry row, append round 15 to campaign index, and advance anchors from the committed 80/43 prefix to 81/44. Do not extend round 14.
- [ ] First commit proposal+registry+campaign+anchors atomically. Then regenerate and commit the immutability report after the registered artifact exists at HEAD, matching the checker’s one-row transaction contract.
- [ ] Point current/AI manifests to the round-15 proposal, evidence-v7 aggregate+both leaves, union graph/receipt, official metadata receipts, bibliography, and context-v2 package report. Legacy source assets remain outside default AI load; the union graph is their CURRENT bridge.
- [ ] Set current state to:

```text
FOUR_IMPLEMENTATION_FINDINGS_REMEDIATED; FORMAL_INDEPENDENT_REVIEW_PENDING.
The round-15 proposal is submitted. Stage-1B is unstarted and unauthorized.
The first systematic query remains forbidden until round-16 SIGN and separate owner authorization of the exact reviewed package.
```

- [ ] Generate current/AI manifests and `context-v2/current-package-check.json`. Keep Research-Objective ≤5120 bytes, current status ≤16 lines, and default AI load exactly three files.

---

### Task 8: Run adversarial release verification

**User journey:** As the owner, I receive evidence over the entire implementation range, not merely a clean working tree.

- [ ] Run focused Windows tests/checks and equivalent WSL headline gates after Task 0. No relevant skip is allowed.
- [ ] Generate `hostile-review-ledger.json` containing every new finding, disposition, failing test, repair commit, and recheck result. Repeat until a full review round yields zero new findings; do not retain only the final PASS.
- [ ] Use explicit ranges:

```powershell
git diff --check IMPLEMENTATION_FREEZE..HEAD
git diff --name-status IMPLEMENTATION_FREEZE..HEAD
git diff EVIDENCE_V6_RELEASE_ANCHOR..HEAD -- docs/checks/system-first-stage1a/evidence-v6 docs/checks/system-first-stage1a/context-v1 wiki/survey/2026-07-15-sf-queries.jsonl docs/integrity/experiment_attempt_registry.jsonl
```

Expected: first command clean; second reviewed; third empty.
- [ ] Run audit immutability, campaign index, union graph, bibliography receipt, proposal, current package, and AI context checks. Verify round-16 path is absent and no actual SIGN/authorization value is present.

---

### Task 9: Merge verified package and push `origin/master`

- [ ] Fetch remote in WSL after Task 0. Record `PRE_MERGE_MASTER`, source HEAD, merge base, default branch, and affected paths. Stop on relevant divergence.
- [ ] Prove primary and feature worktrees clean. Delete the two original untracked root review copies only after their SHA-256 values match committed round-13/14 audit blobs; report this recoverable cleanup.
- [ ] Merge with a normal merge commit, set `MERGE_HEAD`, and verify:

```bash
git diff --check PRE_MERGE_MASTER..MERGE_HEAD
python scripts/survey/sf_current_package_check.py --check
python scripts/survey/sf_audit_immutability_check.py --check
python scripts/checks/ai_context_surface_check.py --check
```

- [ ] Push `master` to `origin/master` without force and prove `ls-remote` equals `MERGE_HEAD`. Do not publish GitHub Wiki.
- [ ] Report `SUBMITTED_FOR_INDEPENDENT_REVIEW`, not Stage‑1B readiness. State that systematic queries, models, smoke, metrics, and prototypes were not executed.

---

## Mandatory stop conditions

Stop before proposal registration or merge if any condition holds:

- cross-platform Git preflight fails;
- an absence field/value lacks an explicit obligation or immutable fulltext binding;
- any load-bearing absence lacks fresh semantic `AGREE` or remains unresolved;
- either platform leaf is missing or the final aggregator does not bind both exact bytes;
- any source row is missing/duplicated, heterogeneous claim evidence is collapsed, or load-bearing identity is unresolved;
- metadata is not reproducible from official receipts or system-first closure has a silent omission;
- a load-bearing proposal citation is below its required evidence grade;
- a frozen query/compiler or attempt registry changes;
- an audit transaction rewrites history or appends more than one registry row per commit;
- current/package language claims formal sign-off from local PASS;
- remote divergence is relevant, a force push would be required, or any Stage-1B/model/smoke action would occur.
