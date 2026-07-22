---
title: "Stage-1B second three-round bounded sampling contract"
date: 2026-07-22
stage: "STAGE_1B_SYSTEMATIC_MAPPING"
authority: "owner direction in active task: research 3,000 additional papers"
role: "WORKBENCH execution contract; no novelty verdict"
---

# Stage-1B second three-round bounded sampling contract

## Conclusion and purpose chain

The owner's new direction reopens broad sampling for exactly one additional batch of three
non-overlapping 1,000-paper rounds. This supersedes only the previous operational stop instruction;
it does not change the Stage-1B mapping boundary, H5 hold, 1,000-paper retained
cap, or the prohibition on research-model calls and dataset/model experiments.

The purpose is to test whether the first batch's rapid yield decline persists in the remaining D0
union and to add genuinely new method-path, experimental, and falsifier evidence before returning to
the knowledge-base/environment phase.

## Frozen replay boundary

- Source: the same frozen 20,727-ID D0 JSONL and source SHA-256 used by the first batch.
- Abstract policy: `sf-stage1b-abstract-policy-v6`. It retains v5 decisions and adds explicit acoustic
  phrases exposed by batch-2 audit (`speech source separation`, `speech understanding`, SpeechLLM,
  audio-language model) plus biometric/speaker similarity signals. The superseded batch-2 v5 run is
  an external audit cache. No further policy retuning is allowed after v6 sampling freezes.
- Sampling lanes: speech task/data, reproducible transfer, and interleaved tail calibration.
- Exclusion set: every ID in the first batch's three v5 round ledgers plus arXiv IDs already present
  in active CURRENT/REGISTRY and targeted Stage-1B workbench records.
- Replay receipt: the sampler must write the seed, handled-ID count/hash, canonical handled-ID file,
  source hash, dataset-lock hash, per-round hashes, and verify 3,000 new unique IDs.
- New IDs must be disjoint from the first 3,000 and from each other. Cross-batch full-text and final
  registry consolidation deduplicate again by canonical arXiv ID.

## Per-paper workflow

1. Read title and abstract; code speech-primary evidence, task, named local dataset, control path,
   reproducibility evidence, and one explicit abstract disposition.
2. Download a PDF only for deterministic `SELECT_FULLTEXT` records or an explicit
   `AUDIT_SELECT_FULLTEXT` promotion. A promotion is allowed only after abstract-level human audit:
   speech/audio work must expose a direct control/evaluation path worth resolving in the paper, and
   non-speech work must additionally have a paper-linked repository that passes the structural
   open-source precheck. Record the source disposition, promotion rationale, and repository evidence
   before downloading; append URL/status/bytes/hash/external path to the existing full-text ledger.
3. Extract/read the local PDF and record page-level method, training/frozen boundary, datasets,
   limitations, code/model/data availability, and evidence locators.
4. For speech/audio work, distinguish exact `TASK_MATCH` from dataset-name-only or split-review
   matches. For non-speech work, require a paper-linked reachable licensed repository with source and
   environment evidence before `KEEP_TRANSFER`.
5. Emit `KEEP_CORE`, `KEEP_INSTRUMENT`, `KEEP_TRANSFER`, `KEEP_NEGATIVE`, or `DROP`; no unresolved
   row silently enters the combined roster.
6. Download e-print only after a paper survives final consolidation. All PDF/e-print/data/model/code
   checkouts remain under `SPEECHRL_DATA_DIR`; Git stores scripts, links, hashes, metadata, and notes.

## Invalidation conditions

Stop and supersede this contract if the D0 or dataset-lock bytes change, the v6 policy is edited
during execution, fewer than 3,000 eligible unhandled IDs remain, cross-round overlap appears, a PDF
cannot receive an explicit bounded outcome, or the owner changes the batch size/scope again.

## Execution closeout

Completed without an invalidation event: 3,000 new unique abstracts, 25 audited PDFs, 25 successful
PDF/e-print receipt pairs, and zero unresolved full-text rows. Cross-batch consolidation retained
184 papers under the 1,000 cap. The sampling summary SHA-256 is
`cb5d5d5faaa9beb443e10aea44932b6330b495f250ef5ad5eaf4105135652786`; detailed decisions and
asset receipts are in `2026-07-22-batch2-three-round-research-closeout.md`.
