---
title: "Stage-1B third five-round bounded sampling contract"
date: 2026-07-22
stage: "STAGE_1B_SYSTEMATIC_MAPPING"
authority: "owner direction in active task: cover 5,000 additional papers"
role: "WORKBENCH execution contract; no novelty verdict"
---

# Stage-1B third five-round bounded sampling contract

## Purpose and authority

The owner reopens the systematic scan for exactly five additional, mutually disjoint rounds of
1,000 abstracts. This replaces the prior operational stop after 6,000 sampled abstracts, while
preserving the frozen Stage-1B evidence boundary, the retained-set cap of 1,000 papers, and the ban
on research-model execution, dataset experiments, smoke tests, and prototype claims.

The objective is coverage, not a novelty verdict: resolve additional speech method/data neighbors,
open and reproducible non-speech transfer mechanisms, and useful negative evidence before returning
to the experiment-environment and knowledge-base phase.

## Frozen replay boundary

- Source is the same 20,727-ID D0 JSONL, SHA-256
  `afc3d85eab383f81c96d293b13d053767500baec485c89ce03aeff32f3425883`.
- Dataset lock is unchanged, SHA-256
  `1790b43c0c2c9ba8b1a3d1ce3d1588d3aa84e63f7d680cef78e20da7adf70c1f`.
- Abstract coding remains `sf-stage1b-abstract-policy-v6`; no policy tuning is permitted after this
  batch freezes.
- The handled set is the canonical union of the 3,224-ID pre-batch-2 boundary and all 3,000 batch-2
  round IDs. Therefore all earlier six sampled rounds and earlier targeted/registry IDs are hard
  exclusions before batch 3 starts.
- The five-round lane cycle is speech task/data, reproducible transfer, interleaved tail calibration,
  residual speech task/data, and residual reproducible transfer. A seed, source and lock hashes,
  handled-ID count/hash, per-round hashes, and exact unique/disjoint checks are mandatory.

## Per-paper decision workflow

1. Analyze title and abstract for speech-primary status, task, named dataset and local-lock match,
   inference-time control path, training/frozen boundary, reproducibility evidence, and an explicit
   abstract disposition.
2. Speech/audio candidates may advance when their method or evaluation path can inform the local
   program; exact local task/data matches, related-but-not-exact assets, absent assets, and split
   review are recorded separately.
3. Non-speech candidates may advance only when the mechanism is transferable and a paper-linked
   repository passes reachability, license, source, environment/configuration, and evaluation-entry
   structural checks. This is not an execution or reproduction claim.
4. Download a PDF only for deterministic `SELECT_FULLTEXT` rows or recorded human
   `AUDIT_SELECT_FULLTEXT` promotions. Read local PDFs page by page and record evidence locators,
   datasets, method/training boundary, limitations, and availability.
5. Assign every downloaded paper one terminal decision: `KEEP_CORE`, `KEEP_INSTRUMENT`,
   `KEEP_TRANSFER`, `KEEP_NEGATIVE`, or `DROP`. Download e-print source only after the paper survives
   bounded full-text consolidation.
6. Keep PDF/e-print/data/model/repository bytes under `SPEECHRL_DATA_DIR`. Git stores scripts,
   source links, receipts/hashes, decisions, page locators, and compact reports only.

## Stop and invalidation conditions

The batch stops after exactly 5,000 new unique abstracts. It is invalid if source or lock bytes
change, fewer than 5,000 eligible unhandled IDs remain, any cross-round or prior-round overlap is
observed, the frozen policy changes mid-run, downloaded papers retain unresolved decisions, or the
owner changes scope again. The final cross-batch roster must remain at or below 1,000 papers.

## Execution closeout

Completed after one fail-closed replay correction: JSONL handled inputs now read record identities
rather than citations embedded in abstracts. The formal run covered 5,000 unique abstracts, audited
22 PDFs, retained 21 papers, and left zero unresolved full-text rows. Cross-batch consolidation contains
205 papers under the 1,000 cap. Evidence, findings, and receipts are recorded in
`2026-07-22-batch3-five-round-research-closeout.md`.
