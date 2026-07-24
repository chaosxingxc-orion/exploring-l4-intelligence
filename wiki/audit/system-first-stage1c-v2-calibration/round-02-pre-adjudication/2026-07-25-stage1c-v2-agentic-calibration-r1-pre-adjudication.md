---
title: "Stage-1C v2 Agentic calibration R1 pre-adjudication transaction"
date: "2026-07-25"
artifact_type: "CALIBRATION_PRE_ADJUDICATION_TRANSACTION"
campaign: "system-first-stage1c-v2-calibration"
round: "round-02-pre-adjudication"
coder_distributed: true
both_raw_outputs_frozen: true
agreement_computed: true
agreement_status: "FAIL"
owner_adjudication_completed: false
push_authorized: false
---

# Calibration R1 pre-adjudication transaction

Two fresh no-fork model coders completed exact N=56 literature coding under the accepted Agentic
RC2R3 method contract. Both files passed schema, semantic, identity and source-manifest checks before
either entered agreement. The transaction then froze both raw byte streams and only afterwards
computed pre-adjudication agreement at the immutable 0.85 threshold.

Frozen coder evidence:

- A (`gpt-5.6-sol`, `STAGE1C-RC2R3-CODER-A-R1`): 354559 bytes,
  `154c091a4727f2461a70dda4b1b3179bb004a14cee6ab1a04c3859dc495389b5`;
- B (`gpt-5.6-terra`, `STAGE1C-RC2R3-CODER-B-R1`): 716610 bytes,
  `ff922386cdf89617604209d30e63834151efb94941404b85a32a0da420f1e0c2`;
- agreement: `9e3f0a6afc969236c68590c0bf5372d7ecaea5f62adae8bc8acfdaf7cdf45d92`;
- complete disagreement evidence:
  `6de80624d94bfe93d0e58988c3bdb9a9ed97183c8e25fd6ef5640b1d58a45bc2`.

The raw agreement result is `FAIL`. Five of thirteen paper-level critical paths pass and eight fail.
All nine object types have zero shared exact match keys; their internal critical fields therefore
remain `NOT_CALIBRATED`. Both coders produced zero `dataset_edges` and zero
`reproduction_evidence`, so those zero-positive categories are independently uncalibrated. No owner
or automated adjudication has been applied to raw responses or metrics.

The detailed owner package recommends one bounded codebook consolidation: deterministic compiler-
owned object identities, explicit object-trigger/minimum-extraction rules and paper-level decision
tables. Any recode requires two new isolated contexts and the full same N=56. Replacing sentinels is
outside this transaction and would require separate authority and method review.

Current endpoint is `AGENTIC_CALIBRATION_R1_AGREEMENT_FAILED_OWNER_DECISION_REQUIRED`. Full mapping
remains closed pending a valid calibration release and `SIGN_STAGE1C_V2_EXPERIMENT_MAPPING`.
Research-model calls, benchmark metrics, paper reproduction, prototype, novelty verdict, Stage-2A
and push remain absent.
