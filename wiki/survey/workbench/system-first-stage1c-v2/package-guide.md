---
title: "Package guide — Stage-1C v2 experiment-family mapping"
date: "2026-07-23"
artifact_type: "WORKBENCH_REVIEW_BRIEF"
requested_verdict: "SIGN_STAGE1C_V2_EXPERIMENT_MAPPING | WITHHOLD_WITH_BOUNDED_DEFECTS"
review_target_status: "PRE_SIGN_WORKBENCH"
novelty_verdict_requested: "NO"
model_or_metric_execution_requested: "NO"
---

# Reviewer brief: Stage-1C v2 experiment-family mapping

## Request

Please review the pre-sign Stage-1C v2 protocol, machine contract, 226-paper metadata bootstrap and
contract tests. Return exactly one of:

- `SIGN_STAGE1C_V2_EXPERIMENT_MAPPING`; or
- `WITHHOLD_WITH_BOUNDED_DEFECTS`, identifying the failed contract and the minimum repair.

This request asks only whether existing Stage-1B evidence may be recoded into experiment cells,
dataset relations, experiment families and evidence-gated branch proposals. It does not ask for a
novelty verdict or authorize model/API calls, metrics, reproduction or prototypes.

## Objects under review

1. `wiki/survey/workbench/system-first-stage1c-v2/protocol-v2.md`;
2. `wiki/survey/workbench/system-first-stage1c-v2/experiment-mapping-contract-v2.json`;
3. `wiki/survey/workbench/system-first-stage1c-v2/paper-audit-bootstrap-v2.json`;
4. `scripts/survey/sf_stage1c_v2_experiment_mapping.py` and its tests;
5. the pre-sign contract report under `docs/checks/stage1c-v2/`; and
6. `wiki/survey/workbench/system-first-stage1c-v2/review-package-manifest.json`, which binds the
   exact pre-sign objects by bytes and SHA-256 without binding itself.

The scientific source remains fixed Stage-1B v5 commit
`38fb9435d0c35e226ad62b16015a6dbee054e6c2`. The proposal must not modify or reinterpret that release.

## Review questions

1. Does the experiment cell represent one run configuration while keeping multiple metrics as child
   observations?
2. Do lineage and non-lineage dataset relations remain unambiguously separated and source-backed?
3. Does strict core membership prevent related but incomparable experiments from being merged?
4. Do typed validation, transfer, falsifier and instrument edges preserve useful related work without
   granting numeric comparability?
5. Are family conclusions stratified by dataset lineage and access before synthesis?
6. Do local readiness, five branch gates and four experiment arms yield a reviewable Stage-2A handoff
   without pre-running it?
7. Does every artifact preserve H5 and no-execution boundaries and avoid a project novelty verdict?
8. Does the metadata bootstrap cover 226/226 papers without claiming experiment cells or completed
   adjudication before this signature?

## Requested authority if signed

A signature authorizes only experiment-level evidence recoding, family synthesis, unexecuted local
protocol design and branch dossier preparation. CURRENT activation must record the exact signed
artifact and commit. A later independent `SIGN_STAGE1C_V2_FAMILY_BRANCH_PORTFOLIO` is still required
before freezing the Stage-2A handoff, and Stage-2A execution remains separately withheld.

## Current pre-sign state

This brief remains in WORKBENCH as a readable view of the exact package. The formal submission is the
separate immutable AUDIT transaction under `wiki/audit/system-first-stage1c-v2/round-01/`. No
reviewer identity, verdict or authority is inferred from generated checks or from the owner's
implementation direction.
