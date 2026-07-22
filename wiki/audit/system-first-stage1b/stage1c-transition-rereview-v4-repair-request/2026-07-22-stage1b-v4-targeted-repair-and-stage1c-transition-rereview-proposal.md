---
title: "Stage-1B v4 targeted repair and Stage-1C transition rereview proposal"
date: "2026-07-22"
artifact_type: "INDEPENDENT_TRANSITION_REREVIEW_REQUEST"
review_request_id: "SYSTEM_FIRST_STAGE1B_V4_TARGETED_REPAIR"
review_target_commit: "f11a2b1fd0b6d81b08caefc5d576fe13ed579883"
supersedes_review_target: "STAGE1B_V3"
request_status: "REREVIEW_REQUESTED"
requested_authority: "STAGE1C_COMMON_RUBRIC_PROBLEM_COMPARISON_ONLY"
novelty_verdict_requested: "NO"
model_api_metric_reproduction_prototype_authority_requested: "NO"
---

# Stage-1B v4 targeted repair and Stage-1C transition rereview proposal

## Executive request

Please independently review scientific release commit
`f11a2b1fd0b6d81b08caefc5d576fe13ed579883` and decide whether the four P0 defects in the Stage-1B
v3 rereview have been repaired sufficiently to begin formal Stage-1C common-rubric problem comparison.

We accept the prior verdict `WITHHOLD_WITH_BOUNDED_DEFECTS`. In particular, the declared v3 commit
identity was invalid; seven rows overstated their evidence depth; the bounded speech/omni ledger had
not been reconciled with already-known priors; and the data lock was being read as a current whole-disk
inventory when it was only a frozen baseline. These were scientific-state defects, not cosmetic review
comments. v4 repairs the underlying records and release process rather than appending exceptions to the
old proposal.

The requested authority is narrow. A positive signature should authorize comparison of the three
non-H5 candidate problem bundles under one Stage-1C rubric. It should not authorize a model/API call,
dataset metric, smoke test, reproduction, prototype, problem selection, technical design, or novelty
verdict. Stage-1 remains literature review and experimental-foundation work; technical-approach
innovation remains deferred to reproduction-first Stage-2A and validation in Stage-2B.

## Research proposal after the repair

The research question is unchanged: can a frozen speech/omni foundation model be governed by an
external, training-free, reward-guided control plane that chooses candidates, tools, evaluators,
routes, budgets, stopping and repair without changing core weights?

What changed is the evidence basis used to formulate a later problem choice. v4 shows that many nearby
systems provide external orchestration, state/event gates, or evaluator/verifier gates, but the inspected
direct-method set contains no row that can presently be coded as `REWARD_GUIDED_SELECTION`. This is not
a Stage-1 novelty claim. It is a taxonomy correction that prevents the broad label
`DIRECT_CONTROL_METHOD` from being mistaken for evidence that the north-star control mechanism is
already occupied.

Stage-1C, if signed, will compare these unranked non-H5 problem bundles under the same fields:

1. budget, stopping and repair under noisy or conflicting evidence;
2. evaluator/reward reliability under modality, task and distribution shift; and
3. interactive/full-duplex objectives, interruption recovery and real-time control.

Evidence-state transfer and tool/agent arbitration remain ineligible because their load-bearing H5
coding is still withheld. The proposal neither ranks the three eligible bundles nor recommends a
winner.

## Fixed review object and reproducibility

The v4 manifest is
`docs/checks/stage1b-closeout/2026-07-22-v4/release-manifest.json`. It binds 60 artifacts: 52 exact Git
blobs and eight external hash-bound artifacts. The commit-bound replay receipt at
`docs/checks/stage1b-closeout/2026-07-22-v4/release-replay.json` resolves both declared and actual review
identity to `f11a2b1fd0b6d81b08caefc5d576fe13ed579883` and verifies 60/60 entries with no missing, byte, or
SHA-256 mismatch.

Git blob bytes, rather than CRLF-sensitive working-tree bytes, are the historical evidence authority.
The v4 manifest generator reads the staged/index blob when binding Git artifacts, and the independent
replay reads the declared commit. Mutable HOT/CURRENT routers are not part of the scientific release;
they now point to the fixed commit without creating a self-referential release.

Focused verification completed with 53 passing tests and zero failures. Combined statement/branch
coverage across the changed evidence, materialization, acquisition and replay modules is 80%. This is
contract verification only; it is not a claim of experimental model performance.

## Response to the mandatory repairs

### P0-R1 — one real, signable release identity

`f11a2b1fd0b6d81b08caefc5d576fe13ed579883` is a real full Git commit containing the v4 scientific
object. Its manifest, spec and replay agree on the same full identity. The earlier invalid long v3 SHA
is retained only inside immutable historical review transactions; all active state and this superseding
request use the v4 identity.

Expected reviewer test:

```text
git cat-file -e f11a2b1fd0b6d81b08caefc5d576fe13ed579883^{commit}
release entries = 60
Git entries = 52
external entries = 8
verified = 60
failures = 0
```

### P0-R2 — honest full-text depth for all 81 routed works

The seven rows challenged in the review—2505.17862, 2507.22898, 2510.11098, 2601.06235,
2602.00675, 2603.23625 and 2606.13049—were resolved by exact arXiv-ID acquisition. Their PDFs and
e-prints are stored outside Git, and successful records were appended to the full-text ledger.

The v4 evidence contract checks all 70 `FULLTEXT_ROUTED` rows against four independent facts: a
successful ledger entry, the exact ledger `stored_at` path, local bytes, and matching SHA-256. The
remaining 11 rows are honestly `ABSTRACT_ROUTED`. Therefore the repair does not relabel an abstract
review as full-text inspection and does not use page-level claims without local source bytes.

### P0-R3 — known-prior reconciliation without duplicate seeds

The reconciliation input was bounded to project-known sources: the existing seed manifest, CURRENT
bibliography, the 226-work registry and the v3 81-work ledger. It did not reopen broad D0 discovery.

Nine required priors are now explicitly reconciled:

| Prior | Canonical disposition | Role in v4 |
|---|---|---|
| Speech-Copilot | `REUSE_CANONICAL_WORK_ID` | direct system prior |
| AudioGPT | `REUSE_CANONICAL_WORK_ID` | direct system prior |
| MM-ReAct | `REUSE_CANONICAL_WORK_ID` | origin-domain boundary |
| EchoChain | `REUSE_CANONICAL_WORK_ID` | interactive measurement instrument |
| From Text to Voice | `REUSE_CANONICAL_WORK_ID` | voice-tool measurement instrument |
| AuTAgent | `REUSE_CANONICAL_WORK_ID` | trained boundary, routed only |
| WavReward | `REUSE_CANONICAL_WORK_ID` | reward/evaluator instrument |
| SDiaReward | `REUSE_CANONICAL_WORK_ID` | episode-level reward instrument |
| GSRM | `REUSE_CANONICAL_WORK_ID` | reasoning-centric reward instrument |

No row creates a new claim work or duplicate seed. The v2 strict supplement contains 39 comparable
rows: 25 direct methods, 13 measurement instruments and one boundary. Instruments and boundaries do
not inflate direct-method occupancy.

### P0-R4 — layered asset facts and targeted public acquisition

The old `docs/datasets.lock.json` is now explicitly a `FROZEN_BASELINE`, not a complete current disk
snapshot. The new inventory separates three layers:

- `FROZEN_BASELINE`: 31/31 locked entries observed, zero missing;
- `CANDIDATE_UNFROZEN`: current local research candidates, with path/file/byte/source/revision status;
- `AUXILIARY`: local support assets excluded from baseline and candidate claims.

No whole-disk content hash or false global-lock claim was manufactured. Existing legacy candidates
whose exact provenance cannot be reconstructed are marked `UNRESOLVED_LOCAL_PROVENANCE`.

Public assets directly relevant to Stage-1C feasibility were downloaded outside Git, using parallel
file acquisition and immutable revisions where the provider supports them:

| Asset | Local data identity | Local code identity | Current status |
|---|---|---|---|
| VoiceAgentBench | HF revision `5ec6b7fcdaf25a1ffd5f538214d91dcf653c9ea4`; 7,663 files; 5,833,663,134 bytes | commit `d1efb7d4b71bed85534ce171460f8f2fb133a456` | complete and pinned |
| Full-Duplex-Bench v3 | archive SHA-256 `37545bd896f81718136598cf5be25d42ea9aa22efcd91f58370938d05d7d672f`; 203 extracted files; 947,535,966 bytes | commit `3e799c45a045256f47d5f1c9cda90157e2d2ec9e` | complete and content-pinned |
| Audio2Tool | HF revision `f1388da9a3189541ab82adac88824a0661670c43`; 71,441 files; 10,410,773,494 bytes | public repository verified; no exact commit asserted | complete and pinned |
| Omni-DeepSearch | HF revision `f6fafcd1ee9e5d370379b684bee3957c27dc25ac`; 911 files; 632,178,405 bytes | commit `0fbbcb443ad2162e3a1ee676a1af79c23af2958d` | complete and pinned |
| IHBench | HF revision `cbd8280ab59bc4a50c48cbe0511a307fba9945cf`; 4 files; 216,559,546 bytes | commit `46cfbd243e0deb018a66915883f8b6d88f01707c` | complete and pinned |
| EVA-Bench | baseline revision `566525430d942873f149273f0fa90fcaeba1f975`; 5 files | public repository verified; evaluator commit not yet pinned | local baseline |

The unresolved states are equally important:

- tau2-bench code is commit-pinned, but it is not evidence that the exact tau-Voice dataset contract is
  locally locked; no substitution is made.
- The LALM audio-judge recordings are private or pending.
- No verified public EchoChain code or paired-audio dataset was found.
- From Text to Voice generator code is pinned at
  `7602b6c602c96bcdb2fd7fa1acd25ab2349dc4a6`, but its exact generated corpus is not packaged.
- SoulX-Duplug and similarly named VoiceBench assets remain adjacent resources, not exact benchmark
  substitutes.

The acquisition path is reproducible through `scripts/data/fetch-candidates.sh` and
`scripts/data/hf_complete.py`. The repository records URLs, immutable revisions, content hashes,
expected paths and inventory receipts. Dataset, checkpoint and output bytes remain under
`SPEECHRL_DATA_DIR` and are never added to Git.

## Response to the classification and common-rubric repairs

### P1-R5 — control basis separated from direct-method identity

The 25 direct rows now have an orthogonal `control_basis` record with evaluator identity, whether the
signal changes the next action, whether labels optimized any policy/configuration, and whether weights
change. Counts are:

```text
EXTERNAL_ORCHESTRATION_ONLY       = 9
STATE_OR_EVENT_GATED              = 9
EVALUATOR_OR_VERIFIER_GATED       = 7
REWARD_GUIDED_SELECTION           = 0
```

This result narrows what Stage-1C may infer. `DIRECT_CONTROL_METHOD` means a load-bearing external
signal-to-action path, not training-free RL and not necessarily reward-guided selection.

### P1-R6 — the same feasibility fields for every eligible bundle

The mapping and eligible-input table now expose, for each non-H5 bundle, nearest direct prior,
measurement instruments, paper/full-text status, repository status and commit, dataset source and
revision, local path/status, license/access constraints, Stage-2 blocker and known unavailability.
No bundle receives favorable treatment because its assets happened to be easier to download.

The result remains a comparison input, not a ranking:

| Bundle | Stage-1B conclusion | Stage-1C status |
|---|---|---|
| Budget / stop / repair | occupied by state/event and verifier-gated paths; residual failures must be specified | `ELIGIBLE_NON_H5`, unranked |
| Evaluator / reward reliability | instrument coverage is explicit; trained reward models are measurement/boundary evidence | `ELIGIBLE_NON_H5`, unranked |
| Interactive / full-duplex | direct systems and benchmarks exist; exact objectives, access and recovery contracts differ | `ELIGIBLE_NON_H5`, unranked |
| Evidence-state transfer | H5-dependent | ineligible |
| Tool/agent arbitration | H5-dependent | ineligible |

## What this release does not claim

1. Frozen-D0 exhaustion is not literature-universe closure.
2. The bounded known-prior reconciliation is not a new broad survey.
3. Local presence is not equivalent to license clearance or Stage-2 reproduction readiness.
4. Paper-reported results are not project-reproduced results.
5. No model, API, dataset metric, smoke test, reproduction or prototype was run.
6. No problem is ranked or selected, and no novelty verdict is requested.
7. Public availability is recorded honestly; missing exact assets are not replaced by nearby names.

## Requested independent verdict

Please answer these gate questions against the exact v4 commit:

1. Does P0-R1 pass: one real full release identity with 60/60 replay and zero mismatch?
2. Does P0-R2 pass: all 70 full-text routes have ledger, local-byte and SHA agreement?
3. Does P0-R3 pass: the nine known priors are canonically reused without duplicate claim work, and
   their direct/instrument/boundary roles are visible in the 39-row supplement?
4. Does P0-R4 pass: baseline, candidate and auxiliary asset facts are separated; critical public
   assets are pinned where available; unavailable exact assets remain explicit?
5. Are P1-R5/R6 sufficient to prevent orchestration/reward conflation and support a fair common-rubric
   comparison of the three non-H5 bundles?

Please return one of two bounded outcomes:

- `SIGN_STAGE1C_COMMON_RUBRIC_COMPARISON` if these tests pass; or
- `WITHHOLD_WITH_BOUNDED_DEFECTS`, naming only the remaining manifest-bound defect required before
  Stage-1C.

A positive signature authorizes Stage-1C problem comparison only. Model and reproduction execution,
technical implementation and novelty convergence remain separately withheld.
