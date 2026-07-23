---
title: "Stage-1B v5 literature-promotion repair and Stage-1C transition rereview proposal"
date: "2026-07-23"
artifact_type: "INDEPENDENT_TRANSITION_REREVIEW_REQUEST"
review_request_id: "SYSTEM_FIRST_STAGE1B_V5_LITERATURE_PROMOTION_REPAIR"
review_target_commit: "38fb9435d0c35e226ad62b16015a6dbee054e6c2"
supersedes_review_target: "SYSTEM_FIRST_STAGE1B_V4_TARGETED_REPAIR"
request_status: "REREVIEW_REQUESTED"
requested_authority: "STAGE1C_COMMON_RUBRIC_PROBLEM_COMPARISON_ONLY"
novelty_verdict_requested: "NO"
model_api_metric_reproduction_prototype_authority_requested: "NO"
---

# Stage-1B v5 literature-promotion repair and Stage-1C transition rereview proposal

## Executive request

Please independently review scientific release commit
`38fb9435d0c35e226ad62b16015a6dbee054e6c2` and decide whether the bounded defects in the Stage-1B
v4 rereview are now repaired sufficiently to begin Stage-1C common-rubric problem comparison.

We accept the v4 verdict `WITHHOLD_WITH_BOUNDED_DEFECTS`. The review correctly identified two P0
problems: canonical papers had not been promoted into the current evaluator/reward evidence layer, and
the portable asset inventory reconstructed nonstandard locked paths incorrectly. It also identified two
P1 issues: Audio2Tool's remote content was mixed with auxiliary and extraneous files, and the reference
appendix did not fully reconcile prompted judges, trained reward models, benchmarks and direct
controllers.

v5 repairs the records and executable checks directly. It is not an amendment chain and does not reopen
broad discovery. The requested authority remains narrow: a positive signature may authorize comparison
of the three non-H5 problem bundles under one Stage-1C rubric. It does not authorize model/API calls,
dataset metrics, smoke tests, reproduction, prototypes, ranking, owner problem selection, technical
design or a novelty verdict.

## Research proposal after the evidence repair

The north-star question is unchanged: can an external, training-free, reward-guided control plane govern
frozen speech/omni foundation models by managing candidates, tools, evaluators, routes, budgets,
stopping and repair without changing core model weights?

The evidence basis has changed in a material but bounded way. MUGEN is now coded as a direct inference
method because K=10 audio-permutational self-consistency changes the final answer. The other newly
promoted works mainly strengthen measurement, calibration, robustness and decision-utility evidence.
Consequently, the strict speech/omni supplement changes from 39 to 46 rows:

| Role | v4 | v5 | Interpretation |
|---|---:|---:|---|
| direct control method | 25 | 26 | MUGEN adds one consensus-to-selection path |
| measurement instrument | 13 | 18 | five gate papers add judge/reward/benchmark coverage |
| boundary comparator | 1 | 2 | VideoFDB adds an audio-visual full-duplex boundary |
| total | 39 | 46 | different from the 226-work registry and 81-work identity audit |

The orthogonal direct-control basis changes from `9/9/7/0` to `9/9/8/0`: nine external orchestration,
nine state/event-gated, eight evaluator/verifier-gated, and zero currently coded as
`REWARD_GUIDED_SELECTION`. This is an occupancy description, not a novelty claim. Prompted frozen
judges, trained reward models, benchmark instruments and controllers whose signal changes a next action
remain distinct.

If Stage-1C is signed, it will compare these unranked non-H5 evidence bundles:

1. budget, stopping and repair under noisy or conflicting evidence;
2. evaluator/reward reliability, including whether proxy quality survives use in selection; and
3. interactive/full-duplex objectives, with an explicit audio-visual comparator but no claim to cover
   every GUI, robotics or multimodal setting.

Evidence-state transfer and tool/agent arbitration remain H5-dependent and ineligible. The proposal
does not select among the three eligible bundles.

## Fixed review object and replay

The v5 release manifest is
`docs/checks/stage1b-closeout/2026-07-23-v5/release-manifest.json`. It binds 108 artifacts: 64 exact Git
blobs and 44 external files. The 44 external entries include the prior eight release artifacts plus PDF
and e-print bytes for all 18 works in the closed promotion set.

The commit-bound replay receipt at
`docs/checks/stage1b-closeout/2026-07-23-v5/release-replay.json` resolves both declared and actual review
identity to `38fb9435d0c35e226ad62b16015a6dbee054e6c2` and verifies 108/108 artifacts with zero missing,
byte-count or SHA-256 failures. Git blob bytes remain the historical authority.

The executable v5 evidence contract reports `PASS` for all of the following:

- 18 unique canonical works: six gate works plus 12 reliability/decision routes;
- 18/18 local PDF hashes and 135/135 unique official-metadata receipts;
- a 59-route self-contained reference appendix, including MM-ReAct and AuTAgent boundaries;
- supplement roles `26 direct / 18 instrument / 2 boundary`;
- control basis `9 orchestration / 9 state-event / 8 evaluator-verifier / 0 reward-guided`;
- Python/PowerShell inventory semantic equality at `31 frozen / 33 candidate / 5 auxiliary / 0 missing`;
- Audio2Tool remote, auxiliary and extraneous content accounting;
- complete UniSRM-Bench manifest and exact commits for three public reference repositories.

Focused verification completed with 50 passing repair tests plus seven release-manifest tests and zero
failures. These are evidence-contract tests, not experimental model results.

## P0-A — canonical corpus to current-layer promotion

The promotion set is closed, not query-expanded:

- six reviewer-gate works: AudioJudge (`2507.12705`), Audio-Aware LLM Judges (`2506.05984`),
  SpeakerSleuth (`2601.04029`), ParaPairAudioBench (`2606.24648`), UniSRM (`2605.23261`) and VideoFDB
  (`2605.30256`);
- nine reviewer-named routes: SpeechJudge, SpeechLLM-as-Judges, MOS-RMBench, NoRefER, SpeechQE, MACE,
  BRACE, CAF-Score and MUGEN; and
- three same-lane canonical routes already exposed by the corpus: semantic-aware confidence calibration,
  Best-of-N decision-utility failure and RAS.

Each identity has one canonical claim-work action:
`REUSE_CANONICAL_WORK_ID_NO_DUPLICATE_CLAIM_WORK`. No new duplicate seed was created. Six gate works and
MUGEN enter the strict supplement; 11 works remain routed-only because they are trained metrics,
benchmarks, calibration methods or decision-utility diagnostics rather than comparable direct methods.

The updated current layer now makes the reliability axes explicit:

- pairwise versus pointwise judgement;
- position and verbosity bias;
- lexical dominance versus paralinguistic sensitivity;
- tie and abstention behavior;
- calibration and distribution shift;
- trained-reward boundaries; and
- correlation or judge score versus actual downstream selection utility.

This closes the promotion loss without claiming that the literature universe is closed or that any
reported paper metric has been reproduced.

## P0-B — portable inventory parity

The Python implementation no longer reconstructs a locked path as `{kind}s/{leaf-name}` when the lock
records a nonstandard location such as `repos/slurp/scripts/audio`. It preserves the explicit
`local_subdir`/`local_path`. The PowerShell implementation also now resolves an absolute output path
correctly.

Both implementations pass the same nonstandard-path fixture, including a same-leaf collision, and the
real NTFS inventory is semantically identical in both outputs:

```text
FROZEN_BASELINE          observed=31 locked=31 missing=0
LOCAL_CANDIDATE_UNFROZEN observed=33
SURVEY_AND_REPRO_AUXILIARY entries=5
```

The real recursive count is intentionally executed natively on the filesystem holding the data. WSL2
remains the ML execution environment, but traversing more than 70,000 files through `/mnt/e` adds no
scientific value and caused avoidable timeouts.

## P1-C — Audio2Tool content identity and hygiene

No user files were deleted. The v5 content receipt separates:

| Layer | Files | Bytes | Interpretation |
|---|---:|---:|---|
| revision-bound remote content | 71,441 | 10,410,773,494 | exact HF manifest; missing = 0 |
| `.hfd` auxiliary content | 11 | 62,611,468 | downloader metadata/logs, not dataset rows |
| extraneous retained content | 610 | 1,158,458 | duplicate-name/local extras, not remote dataset content |

The hygiene rule is explicit: `DO_NOT_DELETE; STAGE2_LOADER_MUST_USE_REVISION_BOUND_ALLOWLIST`.
Therefore local extras neither inflate the remote dataset claim nor become an excuse for destructive
cleanup.

## P1-D — complete appendix and role separation

The transition appendix now has 59 unique routes: 46 supplement rows plus 13 routed-only rows. It
contains official title, author, year, stable link, role and evidence route for every entry. The 18-work
promotion rows also bind local PDF SHA-256 values. MM-ReAct and AuTAgent are retained as explicit
routed-only boundaries.

The neutral field `control_signal_or_decision_component_identity` replaces the conflated
`reward_or_evaluator_identity`. A work is counted as a direct controller only when its signal changes a
next action; a judge, metric, reward model or benchmark that only measures an output does not inflate
direct-method occupancy.

## Public asset acquisition and honest unavailability

Public data remain outside Git under `SPEECHRL_DATA_DIR`. Git contains only exact source URLs,
revisions, acquisition scripts and receipts.

| Asset | Pinned identity | Local result | Constraint |
|---|---|---|---|
| UniSRM-Bench | HF revision `b96b356e2aa2db1fb3b14883c90acafb653958ca` | 1,463/1,463 manifest files; 325,920,409 bytes; missing 0 | public, non-gated |
| SpeakerSleuth project | commit `5e1bbffe07235de51bfdd571a2c396da77a744a1` | local repository | current repo is a project page; announced code/data absent |
| ParaPairAudioBench | commit `f2058333edac404ff7524beb6d543d0a67f05554` | public metadata/routes local | SVC age/gender source audio requires manual access review |
| UniSRM code | commit `8b72922ae38ad7c3e46d618f6c29d00689b7c45c` | local repository | no execution authority inferred |
| StyleSet | exact paper identity | not downloaded | announced, no verified endpoint |
| VideoFDB evaluation data | official project page | not downloaded | terms acceptance and password required; no consent inferred |

The unified downloader is resumable and no longer mistakes a partially populated HF directory for a
complete asset. A pinned completion marker is written only after every `.hfd/manifest` path exists.
Nearby datasets are not substituted for inaccessible exact assets.

## What v5 does not claim

1. Frozen-D0 exhaustion or the 18-work repair is not literature-universe closure.
2. Canonical reuse is not a new seed or duplicated claim work.
3. A prompted judge, trained reward model, benchmark and direct controller are not interchangeable.
4. Local presence is not license clearance or Stage-2 reproduction readiness.
5. Paper-reported results are not project-reproduced results.
6. No model/API call, dataset metric, smoke test, reproduction or prototype was run.
7. No Stage-1C problem is ranked or selected, and no novelty verdict is requested.

## Requested independent verdict

Please answer these questions against the exact v5 commit:

1. Does P0-A pass: are the six gate and 12 route works canonically reconciled, locally hash-bound and
   visible in the mapping, eligible-input and reference layers without duplicate claim work?
2. Does P0-B pass: do both inventory implementations preserve nonstandard paths and replay the same
   `31/33/5/0` real inventory?
3. Does P1-C pass: is Audio2Tool's revision-bound remote content separated from retained auxiliary and
   extraneous files with a Stage-2 allowlist rule?
4. Does P1-D pass: does the 59-route appendix provide official identity and local evidence while keeping
   judge, trained reward, benchmark and controller roles distinct?
5. Is the resulting evidence sufficient to begin an unranked Stage-1C common-rubric comparison of
   budget/stop/repair, evaluator reliability and interactive/full-duplex objectives?

Please return one of two bounded outcomes:

- `SIGN_STAGE1C_COMMON_RUBRIC_COMPARISON`; or
- `WITHHOLD_WITH_BOUNDED_DEFECTS`, naming only the remaining release-bound defect required before
  Stage-1C.

A positive signature authorizes Stage-1C problem comparison only. Model/reproduction execution,
technical implementation and novelty convergence remain separately withheld.
