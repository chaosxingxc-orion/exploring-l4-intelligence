---
title: "Stage-1B final frozen-corpus exhaustion contract"
date: 2026-07-22
stage: "STAGE_1B_SYSTEMATIC_MAPPING"
authority: "owner direction in active task: process every remaining paper with the same workflow"
role: "WORKBENCH execution contract; no novelty verdict"
---

# Stage-1B final frozen-corpus exhaustion contract

## Purpose and authority

The owner explicitly reopens the scan after batch 3 and directs that every paper remaining in the
frozen D0 corpus be processed with the established abstract-analysis, reproducibility, PDF,
full-text and retention workflow. This supersedes the previous operational stop, but it does not
authorize new discovery queries, model execution, dataset experiments, smoke tests, prototypes, or
a Stage-1B novelty verdict.

## Corrected frozen boundary

- D0 contains 20,727 unique arXiv IDs, SHA-256
  `afc3d85eab383f81c96d293b13d053767500baec485c89ce03aeff32f3425883`.
- The canonical handled union contains 11,224 IDs, SHA-256
  `18da767f90e3232cbf956f44fe7b51c833b126bbe71a8d2c879dd0c518422047`.
- Exactly 11,125 handled IDs are in D0; 99 earlier targeted/registry IDs are outside D0. Therefore
  the frozen-corpus remainder is 9,602, not the earlier arithmetic estimate of 9,503.
- The final run must emit nine 1,000-paper rounds and one 602-paper tail round, with no overlap and
  with `D0 - handled - final_sample = empty` proved from record identities.
- Dataset lock SHA-256 remains
  `1790b43c0c2c9ba8b1a3d1ce3d1588d3aa84e63f7d680cef78e20da7adf70c1f`;
  abstract policy remains `sf-stage1b-abstract-policy-v6`.

## Per-paper workflow

1. Code every title and abstract for speech-primary status, task, named dataset, local-lock/local-byte
   status, inference-time control path, training boundary, reproducibility evidence and disposition.
2. Audit speech/audio candidates for program relevance and distinguish local match, lock-only match,
   absent asset and unstated dataset. Non-speech candidates advance only when their transferable
   mechanism has a paper-linked repository that passes structural open-source verification.
3. Download only abstract-audited full-text selections. Store PDFs outside Git; read them page by
   page and record page locators, method/training boundary, datasets, limitations and availability.
4. Give every downloaded paper one terminal decision: `KEEP_CORE`, `KEEP_INSTRUMENT`,
   `KEEP_TRANSFER`, `KEEP_NEGATIVE`, or `DROP`. Download e-print source only for retained papers.
5. Keep all PDF/e-print/data/model/repository bytes under `SPEECHRL_DATA_DIR`; Git receives only
   scripts, links, hashes, evidence records and compact reports. The cross-batch retained roster must
   remain at or below 1,000 papers.

## Stop and invalidation conditions

The scan stops only after all 9,602 remaining D0 IDs have an abstract record and the set difference
is empty. It is invalid if source or lock bytes change, prior/final rounds overlap, the policy changes
mid-run, an unverified non-speech paper reaches PDF authorization, a downloaded paper lacks a
terminal full-text decision, or local binary assets enter Git.

## Execution closeout

Closed with 9,602/9,602 final abstracts, zero overlap and an empty D0 set difference. Twenty-one
audited PDFs and e-prints were retained as 14 instruments, 5 transferable mechanisms and 2 boundary
negatives. Cross-batch consolidation contains 226 papers under the 1,000 cap with zero unresolved
rows; details and receipts are in `2026-07-22-frozen-d0-exhaustion-closeout.md`.
