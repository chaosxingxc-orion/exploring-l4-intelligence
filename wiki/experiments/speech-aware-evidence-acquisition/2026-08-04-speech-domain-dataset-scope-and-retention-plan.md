---
artifact_id: "SAEA-SPEECH-DATA-SCOPE-2026-08-04"
title: "Speech-domain dataset scope, Stage-2 roles and local retention plan"
date: "2026-08-04"
status: "CURRENT__DOWNLOAD_WAVE_CLOSED__SPEECH_BINDINGS_FROZEN__NO_DATA_DELETION"
authority: "owner directives 2026-08-04"
canonical_state_source: "docs/datasets.lock.json"
---

# Speech-domain dataset scope, Stage-2 roles and local retention plan

## 1. Conclusion

The current download wave has closed; Stage-2A no longer waits on new data. All five datasets targeted for
completion in this wave are marked `COMPLETE` in the canonical lock: `audioset-metadata-features`,
`ami-meeting-corpus`, `slue-sqa-5`, `fsd50k`, `contextasr-bench`.

Download completion and research adoption are two different judgments:

- AMI, SLUE-SQA-5 and ContextASR-Bench are speech-domain and may enter subsequent pre-registered experiments;
- FSD50K and AudioSet are general/environmental audio and do not enter this study;
- ESC-50 is likewise general audio and does not enter this study, even though it was already held locally;
- all downloaded data is retained — never deleted, never re-downloaded; its identity, size, revision,
  checksum and status continue to be maintained solely by `docs/datasets.lock.json`.

This removes the former implicit chain of "appears in a paper → download → becomes an R2 experiment set by
default". From now on there must first be a research question or a baseline role, and only then a data binding.

## 2. Domain-applicability judgment

### 2.1 Included

The primary evaluable target of the data must be human speech and its linguistic content, including ASR,
entity recognition/correction, contextual biasing, spoken QA and meeting speech understanding. Noise
conditions may serve as perturbations for speech robustness, but environmental sound classification is not
itself a task here.

### 2.2 Excluded but retained

Data whose primary labels are acoustic events, soundscapes, music or non-speech sound sources does not enter
the study, even though an omni model can accept such input. The reason for exclusion is the domain of the
research question — not that the local bytes are invalid, and not an unverified assertion about the model's
training history.

### 2.3 Forbidden inferences

- "The file extension is audio" does not establish general-audio; speech is also carried by audio files;
- "It has already been downloaded" does not establish that it must be experimented on;
- "A paper cited the dataset" does not establish that it must be reproduced;
- "The model is omni" does not automatically bring every modality task into the same research object.

## 3. Single source of truth and retention policy

`docs/datasets.lock.json` is the only live source, responsible for: upstream identity, revision, source,
local path, exact size, verification method, checksum/hash, status, lifecycle and profile. This document
only states this study's experiment roles; it does not copy hashes.

No data is deleted in this wave. Any future cleanup must satisfy every one of the following: explicit owner
authorization, exact paths resolved, no active/planned experiment referencing it, a dated amendment in the
lock, and a recoverability or re-acquisition statement for after the deletion. FSD50K, AudioSet and ESC-50
currently satisfy none of the deletion conditions, because the owner has explicitly required that the
download results be retained.

## 4. Stage-2 data tiers

| Tier | Data | Research question | Enabling condition | Conclusions it can support |
|---|---|---|---|---|
| Core-main | Earnings21 + ConEC | Entity mishearing, contextual evidence and error reinforcement | E0 identity/leakage/scorer/trace closed | Main mechanism and task utility |
| Core-dev | Earnings22 + ConEC | Calibrating thresholds, candidate width, stopping strategy and source policy | Isolated from confirmatory | Configuration selection, never final confirmation |
| Diagnostic | PRISM public, Rare5k reconstruction, BuzzWord | Local failure modes for rare words, proper nouns and biasing | Corresponding scorer and slice pre-registered | Diagnosis, no extrapolation to the population |
| Secondary-SQA | SLUE-SQA-5 | Interaction of speech observation and external textual evidence in spoken QA | The minimal core path holds | Cross-task speech replication |
| Secondary-context | ContextASR-Bench | Bilingual contextual ASR, forms of context supply | A same-boundary baseline is runnable | Cross-language/context replication |
| Secondary-meeting | AMI meeting corpus | Multi-speaker, long-context and meeting entity pressure | Fixed mixed-headset condition, explicit segmentation | Condition transfer / stress testing |
| Optional | TED-EL annotations, ATCO2-1h, Eka-Medical, LibriSQA | Specific entity/domain/low-cost adjacent questions | Each carries its own protocol hash | Pre-registered local questions only |
| Cross-domain retained | FSD50K, AudioSet metadata/features, ESC-50 | None | Never enabled in this study | Supports no conclusion in this study |

## 5. Explanation of the download-wave closure

### 5.1 How the five items in this wave are handled

| lock key | Local status | New ruling | Enters the Stage-2 list? |
|---|---|---|---|
| `slue-sqa-5` | COMPLETE | speech secondary carrier | Yes, enabled after core |
| `contextasr-bench` | COMPLETE | speech secondary carrier | Yes, enabled after core |
| `ami-meeting-corpus` | COMPLETE | speech meeting stress/transfer carrier | Yes, requires its own protocol |
| `fsd50k` | COMPLETE | cross-domain retained | No |
| `audioset-metadata-features` | COMPLETE | cross-domain retained | No |

A completion receipt in the download queue is not experiment completion. For the first three, Stage-2 still
needs loader, split, information boundary, metric and baseline readiness; for the last two, no further
engineering task is generated in this study.

### 5.2 No re-downloading

Before any fetch, query the lock entry through `asset_lock.py` and check the local `verification` against
the partial marker. A `COMPLETE` asset is verified only, never re-pulled by default. Only on checksum drift,
a missing file, or the owner choosing a new revision is a dated resume/upgrade plan created; a resume reuses
the existing `.aria2`/cache and complete files, and deleting before downloading is forbidden.

## 6. Baseline and data-consumption matrix

| baseline/comparison | Preferred carrier | Purpose | Minimum readiness |
|---|---|---|---|
| bare frozen core | Earnings21/22 | Measure the true baseline without external knowledge | runtime pin + fixed prompt |
| legal fixed context | Earnings + ConEC | Separate context availability from control gain | visible-field hash, no gold leakage |
| ConEC/contextual ASR | Earnings + ConEC | Primary closest-prior reproduction | runnable revision, scorer alignment |
| RECOVER-style 1-best correction | Earnings | Forced-correction comparison | same input boundary, no second answering LLM |
| entity resolution/context biasing | Earnings, ContextASR, diagnostics | Entity and rare-word comparison | vocabulary source and injection timing frozen |
| random/mismatched evidence | Every enabled carrier | Check whether the gain is only a context-length/prompt effect | same budget as real evidence |
| oracle evidence bound | discovery only | Estimate the supply upper bound | explicitly marked oracle, never in confirmatory runtime |

SLUE-SQA-5, ContextASR and AMI should not all be opened in the first week. Recommended order: Earnings core
→ one closest prior → replication on either SLUE-SQA-5 or ContextASR → AMI stress test. This localizes the
cause of a failure with the fewest variables.

## 7. Rules for refreshing the experiment list

For every newly discovered paper, answer four questions first:

1. Does it change the current speech-domain research question or the same-boundary closest prior?
2. Is its data consumed by a concrete baseline, replication or diagnostic hypothesis?
3. Is the data public, acceptably licensed, under 1 TB per item, and revision-pinnable?
4. Can data already held locally answer the same question?

Only when the first two are "yes", the last three pass, and the owner accepts the marginal cost is an
acquisition proposal added to the lock. Otherwise only the literature/threat list is updated. A new paper
can never expand the experiment table automatically.

## 8. Immediate Stage-2A tasks

1. Close E0 D1–D4 for Earnings21/22 + ConEC;
2. Fix the four-axis `OBS/ORG/SUPPLY/USE` trace schema;
3. Complete the bare core, fixed legal context and one closest-prior vertical slice;
4. Freeze the joint effectiveness/reasonableness/efficiency evaluation table;
5. After the core stop/go, choose SLUE-SQA-5 or ContextASR as the first secondary carrier;
6. Check that the dependency graph and test discovery paths contain no FSD50K, AudioSet or ESC-50.

No further downloads are added before the above tasks are complete. This both preserves the data assets
already obtained and converges engineering attention back onto the speech-domain research question.
