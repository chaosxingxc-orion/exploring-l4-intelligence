---
title: "Stage-1B three-round bounded sampling contract"
date: 2026-07-22
stage: "STAGE_1B_SYSTEMATIC_MAPPING"
authority: "owner direction in active task"
role: "Current bounded-scan execution contract; no novelty verdict"
---

# Stage-1B three-round bounded sampling contract

## Execution status

**CLOSED on final policy v5.** The three rounds are complete; broad scanning stops. Final abstract
counts are 251 select / 1,561 defer / 1,188 exclude, all 251 selected PDFs reached full-text analysis,
the audited retained roster is 159 with zero unresolved rows, and all 159 retained e-prints are
present externally. Earlier v1-v4 ledgers remain
external audit caches and are superseded for active decisions. The detailed receipt is
`2026-07-22-bounded-three-round-execution-snapshot.md`.

## Owner decision and stopping rule

The open-ended D0-wide screening plan is replaced for the active research workflow by approximately
three non-overlapping rounds of 1,000 papers each. After the third round and consolidation, expansion
scanning stops. The retained paper set must be at most 1,000 unique canonical works. The next program
phase is construction of the experiment environment and research knowledge base, not a fourth broad
scan.

This bounded design changes the supported claim scope. It preserves a replayable sample-based method
map and evidence portfolio; it does not claim exhaustive REC-0 closure over all 20,727 D0 records or
the old E1/E2/E3 corpus-exhaustion conclusion.

## Three complementary rounds

| Round | Primary lane | Purpose |
|---|---|---|
| 1 | `SPEECH_TASK_AND_DATASET` | Prioritize speech/audio tasks, record task type, named datasets, and exact local-lock matches. |
| 2 | `TRANSFER_REPRODUCIBLE` | Prioritize non-speech method paths only when the abstract supplies reproducibility evidence; later verify the repository/artifacts. |
| 3 | `TAIL_CALIBRATION` | Interleave remaining relevance-score bands to detect missed method families and adverse evidence instead of taking another homogeneous top list. |

The three manifests are deterministic, non-overlapping, exclude previously handled papers, retain the
frozen D0 SHA-256, and live outside Git under `speechrl-data/survey-bfs/`. Git retains the sampler,
tests, contract, summaries, URLs/hashes, screening rationale, and derived notes.

## Per-round pipeline

1. Analyze all 1,000 titles/abstracts with transparent lexical and dataset features.
2. Emit one of `SELECT_FULLTEXT`, `DEFER_ABSTRACT`, `DEFER_REPRO_CHECK`, or
   `EXCLUDE_ABSTRACT`, with reason codes.
3. Audit selections and boundary/exclusion samples before acquisition.
4. Download PDF for abstract-authorized works; after final keep/drop, download e-print only for the
   retained set. Append URL, status, bytes, SHA-256, and external path to the full-text ledger.
5. Read local full text, record method path, datasets, code/model/data availability, limitations, and
   evidence locators.
6. Emit final `KEEP_CORE`, `KEEP_TRANSFER`, `KEEP_NEGATIVE`, `KEEP_INSTRUMENT`, `DEFER`, or
   `DROP` with a nonempty reason.

No research-model call, dataset experiment, model smoke, or prototype is authorized by this scan.

## Speech/audio decision fields

Every selected speech/audio record must state:

- task tags: ASR, ST, SER, speaker, TTS, SLU/intent, spoken QA/reasoning, spoken agent/dialogue, or
  audio generation;
- datasets named in abstract and then full text;
- normalized dataset identity and source locator;
- `LOCAL_MATCH`, `LOCK_MATCH_NOT_PRESENT`, `NO_LOCAL_MATCH`, or `NOT_STATED` against
  `docs/datasets.lock.json` plus the external directory presence check;
- whether the available local split is suitable for the claimed task, rather than merely sharing a
  dataset name.

The current lock contains 28 datasets and all 28 declared directories are present. A local match
raises execution priority but is not evidence that the paper's result reproduces locally.

## Non-speech transfer decision fields

Non-speech papers are retained only when the method supplies a transferable signal-to-action path and
the implementation can be inspected or reproduced. Final full-text coding separates:

- abstract-only open-source claim;
- project/repository URL resolved;
- repository reachable and license visible;
- code sufficient for the claimed method path;
- weights/data/configs available where required;
- environment or simulator dependency;
- transferable component and the speech adaptation needed.

`OPEN_SOURCE_VERIFIED` requires official repository/project evidence; an abstract promise or generic
project page alone is insufficient. A technically interesting but closed non-speech system may remain
as `KEEP_NEGATIVE` or boundary context, but not as a reproduction candidate.

## Consolidation and cap

Deduplicate by canonical work and split mixed papers by method path only in the knowledge base. Rank
retained works by core speech relevance, local dataset executability, method-path uniqueness,
reproducibility, threat value, and evidence quality. When equivalent papers occupy the same cell,
retain the strongest reproducible representative plus the strongest adverse control. The consolidated
paper roster must not exceed 1,000; extra duplicates become citation/navigation records without D2
maintenance obligations.

The scan stops after round 3 even if fewer than 1,000 works remain. The cap is a maximum, not a quota.
