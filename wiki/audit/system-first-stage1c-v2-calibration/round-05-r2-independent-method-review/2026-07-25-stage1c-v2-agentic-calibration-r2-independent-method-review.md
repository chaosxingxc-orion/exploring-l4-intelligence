---
title: "Stage-1C v2 Agentic calibration R2 independent method review"
date: "2026-07-25"
artifact_type: "INDEPENDENT_AI_DOCTORAL_METHOD_ADVISORY_REVIEW"
campaign: "system-first-stage1c-v2-calibration"
round: "round-05-r2-independent-method-review"
reviewed_commit: "70786231f8f4a20a117ed6fc9369e00001750fc1"
reviewed_manifest: "wiki/survey/workbench/system-first-stage1c-v2-precalibration-r2/review-package-manifest-r2.json"
verdict: "WITHHOLD_WITH_BOUNDED_DEFECTS"
human_signature_claimed: false
owner_authority_claimed: false
coder_or_adjudicator_role_claimed: false
research_execution_performed: false
push_authorized: false
---

# Independent AI method review

This is a fresh no-fork AI advisory review of the exact R2 method package at Git commit
`70786231f8f4a20a117ed6fc9369e00001750fc1`. It is not a human signature, owner decision, coder
output or adjudication. All submission artifacts were inspected from Git object bytes using
`git show`/`git cat-file`, not mutable working-tree narration. No web search, research model, benchmark,
paper reproduction, prototype or push was run.

## Commit and manifest verification

- The reviewed manifest is
  `wiki/survey/workbench/system-first-stage1c-v2-precalibration-r2/review-package-manifest-r2.json`.
  Its Git blob id is `3a718f11231dd38f13f73f75124a60cf8d19b6e3`, exact size is 8,641 bytes and
  exact SHA-256 is `d1d25c647e7d95b5bdc3f9f4ff3efde2c0bc9f741bb362695a4e39d4b9685a0b`.
- The manifest declares 34 artifacts; the array contains 34 entries and 34 unique paths. All 34/34
  paths exist at the reviewed commit, and every declared byte count and SHA-256 matches the exact
  Git blob bytes.
- The independently recomputed frozen-package SHA-256 is
  `eaf2e3ca095a2d4fbe303e68c6fa273b73b26cd7a68476eaae9848ef16e1fa47`, matching the manifest,
  frozen contract and agreement-engine compiled constant.
- The sample remains exactly N=56 with 38 overlays and 18 sentinels. Canonical IDs are unique and
  ordered identically across the calibration manifest, source manifest and blind packet. Source,
  assignment and blind-packet bindings agree. The R2 source manifest, assignment manifest, claim
  registry and coder-view registry are blob-identical to their RC2R3 inherited counterparts, and
  the non-blank blind-packet supply projection is unchanged.
- The eight coder-visible artifacts recompute to bundle SHA-256
  `c0212cffe2994b5821d7016d2dee5f8f7af09e839fa263c1ce7857258de18b9b`; the prompt recomputes to
  `d89f7da3dc247afbff90a0879b89b1864dce1cc6f4990b772064f280fcef6905`. Both match the distribution
  and intake contracts.

## Evidence and checks inspected

The review inspected all manifest-listed contracts, schemas, ledgers, audit transactions, builder,
guard and agreement code, the full R2 test source, the contract report and verification summary.
The exact commit was exported to a validated temporary WSL2 directory and replayed under the pinned
`~/.venvs/speechrl` Python 3.12 environment with bytecode and pytest cache writes disabled:

- `30 passed, 42 subtests passed` for
  `scripts/survey/test_sf_stage1c_v2_precalibration_r2.py`;
- the dry package validator returned N=56, 38+18, eight coder-visible artifacts, zero anchors,
  threshold 0.85 and the compiled frozen hash above; and
- the committed verification evidence records Windows and WSL2 PASS, two deterministic write/replay
  comparisons over 22 files, 84% line and branch coverage overall, and 100% line and branch coverage
  for the P0/P1 guard module. Windows and coverage measurements were inspected as commit-bound
  evidence rather than independently rerun in this review.

The exact-union agreement implementation correctly increments every critical-field denominator for
every compiled key in the union. An unmatched object therefore fails segmentation and all applicable
critical fields, while `NOT_CALIBRATED` is reserved by `object_gate_status()` for a true both-zero
class. Raw schemas reject caller-authored `object_match_key`; source anchors use frozen rendition
hashes and typed coordinates. The reviewer-only positive-support ledger is outside the eight-artifact
coder bundle, the package leakage scan passes, local readiness remains reviewer-only, and all 15
readiness entries remain `CANDIDATE_NOT_ANCHOR`. Specialized/trained exclusions, BORROW_PROTOCOL
transfer guards, the fixed 0.85 threshold and zero-anchor state are present. These passing checks do
not close the defects below.

## Load-bearing bounded defects

### 1. Duplicate coder-local IDs make compiled cross-references ambiguous

`compile_response_objects()` uses one mutable `id_maps` dictionary. Inside `compile_array()`, each
local ID is assigned with `id_maps[source_id] = key`, but neither the response schema nor the compiler
requires those local IDs to be unique. Distinct objects can therefore reuse one local ID, produce two
different compiler-owned segmentation keys and silently overwrite the reference target.

An exact-commit adversarial response containing two schema-valid dataset nodes named `MMAU` and
`MMAR`, both with local ID `DS-DUP`, passed `validate_completed_response()`. Both nodes received
different `OBJ-*` keys, while a run referencing `DS-DUP` silently resolved to the second node. Thus
the compiler does not establish an unambiguous source-object graph even though ordinary unknown-
reference and duplicate-signature tests pass.

Bounded repair: reject duplicate local IDs before any map insertion, preferably with separate typed
maps for every object class; verify uniqueness and exact resolution for every reference-bearing ID
field with adversarial tests.

### 2. `REPRODUCTION_CANDIDATE` can be granted without closed paper support

The codebook says candidate status requires paper-visible closure of task, data, repository,
entrypoint, access, terms and evaluator. The runtime guard, however, only checks for
`closure_status == CLOSED_PAPER_SUPPORT` and an empty blocker list. Required fields are otherwise
non-empty strings, and `model_access` may remain `MIXED_OR_UNCLEAR`.

An exact-commit adversarial response labeled `REPRODUCTION_CANDIDATE` passed completed-response
validation while `dataset_revision`, `split`, `pinned_revision`, `entrypoint` and `license_terms`
were all `NOT_STATED_IN_SOURCE`, `model_access` was `MIXED_OR_UNCLEAR`, closure was
`CLOSED_PAPER_SUPPORT`, and blockers were empty. This collapses the intended distinction between
open paper support and a reproduction candidate. Reviewer-only local readiness and the no-anchor
guard do not repair the false candidate classification.

Bounded repair: define typed observable/missing states and require every closure-bearing field to be
affirmatively closed before accepting `CLOSED_PAPER_SUPPORT` or `REPRODUCTION_CANDIDATE`; reject
unknown/not-stated placeholders and add direct adversarial tests.

### 3. Agreement runtime does not bind the actual frozen coder response bytes

Receiver-side delivery receipts correctly bind the eight input artifacts and prompt, but they contain
no coder-response byte length or SHA-256. `bind_runtime_intake()` marks both slots
`FROZEN_SUBMITTED` and synthesizes `submission_receipt_id` from the delivery receipt without receiving
or hashing either response. `compute_agreement()` validates whichever response objects the caller
supplies, but it cannot prove they are the outputs frozen before agreement.

In an exact-commit adversarial replay, the A response set was changed after the runtime intake and
delivery receipts were created. The changed response remained schema-valid and
`compute_agreement()` accepted all 56 papers while reporting `frozen_provenance_validated: true`.
The static `raw_outputs_frozen_before_agreement: true` flag therefore records policy but does not
provide freeze integrity.

Bounded repair: create independent submission receipts over the exact canonical raw response bytes
(count, length and SHA-256 for each coder), freeze both before agreement, bind those digests and
receipt identities into the runtime intake/frozen root, and require `compute_agreement()` to recompute
and compare them before validation or metrics. Add mutation-before/after-freeze adversarial tests.

## Verdict and authority boundary

The exact union-denominator, both-zero-only `NOT_CALIBRATED`, blindness, threshold and platform
evidence are materially improved, but the three reproduced defects affect compiler graph identity,
reproduction-candidate semantics and freeze-before-agreement provenance. They are load-bearing for
coder intake. The R2 method contract is therefore withheld pending a bounded repair and a new exact
independent review.

This verdict authorizes no coder distribution, recode, agreement, owner adjudication,
`SIGN_STAGE1C_V2_EXPERIMENT_MAPPING`, 320-paper mapping, research/model/API execution, benchmark,
paper reproduction, prototype, novelty verdict, Stage-2A, branch/portfolio signature, publication or
push. The reviewer remains an AI advisory reviewer only.

Non-blocking caution: the committed Windows/coverage and two-run determinism results are summary
evidence rather than measurements freshly regenerated here; retain exact commands, interpreter,
working directory, coverage denominator and post-run diff evidence in the successor transaction.

`WITHHOLD_WITH_BOUNDED_DEFECTS`
