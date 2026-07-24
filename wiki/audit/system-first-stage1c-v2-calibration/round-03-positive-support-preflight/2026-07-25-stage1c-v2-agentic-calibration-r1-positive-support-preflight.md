---
title: "Stage-1C v2 Agentic calibration R1 positive-support preflight"
date: "2026-07-25"
artifact_type: "CALIBRATION_POSITIVE_SUPPORT_PREFLIGHT"
campaign: "system-first-stage1c-v2-calibration"
round: "round-03-positive-support-preflight"
status: "FAIL_WITH_BOUNDED_CONTRACT_DEFECTS"
sample_modified: false
coder_packet_modified: false
research_execution: false
---

# R1 positive-support preflight transaction

This reviewer-only, read-only transaction checks whether the frozen N=56 source packet can contain a
positive for every mandatory object class. It does not change R1 outputs, agreement, sample identity,
source exposure or coder labels.

The result is `FAIL` with three bounded defects:

1. TRACE (`acl:2026.findings-eacl.151`), page 3, supplies two dataset-edge positives: use of the
   English subset of S2S-Arena and re-annotation of existing SpeakBench/S2S-Arena data. Both R1 coders
   emitted zero `dataset_edges`, proving a codebook/object-trigger miss rather than a zero-positive
   sample.
2. Blind `reproduction_evidence` requires `local_asset_state`, while the packet explicitly withholds
   repository access. That field is not observable by either coder.
3. The same object requires `closure_status=CLOSED` and an empty blocker list. It cannot represent a
   paper-visible reproduction candidate that still needs reviewer/local closure, so the mandatory
   class has zero expressible positives.

The bounded repair is to split paper-visible reproduction support from reviewer-only local
readiness. A candidate may remain `OPEN_WITH_BLOCKERS`; only complete local closure plus 100% review
can promote an anchor. Dataset-edge triggers and compiler-owned object identity must also be made
explicit. The exact R2 package must rerun this preflight before distribution. A sentinel/source
replacement is not authorized or currently justified.

This transaction grants no codebook repair, new source acquisition, coder distribution, mapping,
research model/API, benchmark metric, reproduction, prototype, novelty verdict, Stage-2A or push.
