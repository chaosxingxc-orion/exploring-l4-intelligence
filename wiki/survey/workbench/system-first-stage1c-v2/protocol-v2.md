---
title: "Stage-1C v2 experiment-family mapping protocol — pre-sign draft"
protocol_id: "SF-STAGE1C-V2-EXPERIMENT-FAMILY-MAPPING"
protocol_version: 2
effective_status: "WORKBENCH_AWAITING_INDEPENDENT_SIGNATURE"
requested_verdict: "SIGN_STAGE1C_V2_EXPERIMENT_MAPPING"
frozen_stage1b_release: "38fb9435d0c35e226ad62b16015a6dbee054e6c2"
execution_authorized: false
---

# Stage-1C v2 experiment-family mapping protocol

## 0. Authority and activation

This is a WORKBENCH proposal, not CURRENT authority. It **does not self-grant**
`SIGN_STAGE1C_V2_EXPERIMENT_MAPPING`, experiment-level recoding, family adjudication, branch
formation, model/API execution, dataset metrics, paper reproduction, prototype work or a novelty
verdict. The current signed authority remains the bounded Stage-1C v1 common-rubric comparison until
an independent reviewer signs this v2 mapping protocol.

Before the signature, permitted work is limited to metadata-only inventory, schema and checker
implementation, deterministic tests and preparation of the independent review package. The 226
bootstrap rows must remain `AWAITING_AUTHORIZED_EXPERIMENT_RECODE`, contain zero experiment cells and
claim no empirical status, family membership or branch readiness.

After a valid independent signature is registered, CURRENT may be superseded in place and the
experiment-level recoding campaign may start. That signature still authorizes no research model,
benchmark metric, reproduction or prototype execution. A later
`SIGN_STAGE1C_V2_FAMILY_BRANCH_PORTFOLIO` freezes the family/branch handoff but likewise gives no
Stage-2A execution authority.

## 1. Purpose and units

Stage-1C v2 turns the fixed Stage-1B evidence surface into an experiment-led decision package:

`226 paper records → run-config experiment cells → dataset graph → experiment families → common
capabilities → evidence-gated research branches`.

The analysis units are deliberately separate:

1. **Paper record** — provenance and portfolio role, never the experimental comparison unit.
2. **Experiment cell** — one run configuration, with one or more result observations.
3. **Dataset edge** — either factual lineage or an explicitly non-lineage experimental relation.
4. **Experiment family** — directly comparable core cells plus typed validation, transfer,
   falsifier and instrument evidence.
5. **Research branch** — one locally realizable primary family and the evidence needed to enter a
   reproduction-first Stage-2A funnel.

## 2. Paper audit

All 226 canonical Stage-1B registry records are audited exactly once. Each row records role, source
domain, full-text locators, empirical status, cell IDs, load-bearing disposition, reason, coder,
reviewer and adjudication state. A work with no extractable experiment becomes a non-cell evidence
node. Conceptual or pseudo experiment cells are prohibited.

The frozen registry and Stage-1B v5 release are read-only sources. Stage-1C records are new derived
artifacts and never rewrite registry shards, release-bound Stage-1B tables or historical evidence.

## 3. Experiment cells and observations

A cell identity is:

`paper × dataset/revision/split × core/revision/access × input condition × intervention ×
budget/horizon`.

Accuracy, WER, MOS, task success, latency, calls, cost and harm from the same run are observations on
that cell. A changed run condition creates a new cell. Each observation preserves the paper-reported
baseline, method value, within-cell delta, uncertainty if reported, and page/table/figure locator.

No omnibus effect is computed. Cross-paper numbers may be compared only under an exact key containing
dataset revision, split, model and revision, access, input condition, metric and budget. Otherwise
they remain parallel, uncertainty-bearing evidence.

## 4. Dataset lineage and relation

Lineage is a factual provenance claim and is restricted to `SAME_REVISION`, `DERIVED_FROM`,
`SUBSET_OF`, `TRANSLATED_FROM`, `AUDIO_RENDERING_OF`, `REANNOTATED_FROM` and `SPLIT_OF`. Every lineage
edge requires a traceable source locator.

`INDEPENDENT_SAME_TASK`, `CROSS_DATASET_VALIDATION`, `DISTRIBUTION_SHIFT_TEST` and
`PROTOCOL_ANALOGUE` are non-lineage relations. They require a bounded rationale and evidence mode and
must never be rendered as dataset ancestry.

## 5. Experiment families

Direct core compatibility requires the same problem, evaluation object, outcome semantics,
environment mode, access protocol and interpretable baseline-to-intervention comparison. Different
datasets may be core members only when those fields match; lineage and access remain visible strata.

Other evidence attaches with one of four typed relations: `VALIDATION_MEMBER`, `TRANSFER_ANALOGUE`,
`FALSIFIER` or `INSTRUMENT_SUPPORT`. These relations do not inherit direct numeric comparability.
Family conclusions are one of `CONSISTENT_SUPPORT`, `MIXED`, `NULL_OR_NEGATIVE` or
`INSUFFICIENT_EVIDENCE` after stratification by lineage and access.

Every card separates the author's claimed contribution, the evidence supported by the paper's own
experiments, the strongest contradiction and a bounded project residual hypothesis. The residual is
not a technical novelty verdict.

## 6. Local protocols and branches

Every `LOCAL_READY` family and every closable `LOCAL_ADAPTABLE` family receives an unexecuted local
protocol. Assets with missing bytes, terms, passwords or exact versions remain
`BLOCKED_ASSET_OR_TERMS`; cross-domain design-only families remain `TRANSFER_ONLY`.

A primary family becomes `READY_FOR_FUNNEL` only if all five gates pass: local readiness, falsifiable
residual, task-matched nearest prior, observable outcome/evaluator, and strongest falsifier plus kill
criterion. No branch quota is imposed. Others stay `REFERENCE_ONLY`.

Every ready branch carries frozen-core baseline, nearest-prior reproduction, candidate-strategy and
oracle/upper-bound arms. If an oracle is not definable, the reason is mandatory. Candidate strategy
coding stops at inputs, state, signals, decision rights, actions and expected causal path; algorithmic
innovation convergence remains Stage-2A work after reproduction.

## 7. Review, outputs and failure conditions

Primary coding covers 226/226 records. Blind review covers at least 20% stratified by role, data and
task. All core members, load-bearing relations, family conclusions and branch cards receive 100%
review and adjudication.

The campaign fails closed on a missing paper, duplicate ID, fabricated cell, unsupported lineage,
incompatible core member, inexact numeric aggregation, unreviewed load-bearing row, H5-dependent
conclusion, missing branch gate or unauthorized execution claim.

The post-sign outputs are the paper audit, experiment cells, dataset graph, family cards, task/capability
views, local protocols, branch portfolio and a separate release/check receipt. Human tables are
generated from machine evidence rather than hand-maintained in parallel.

## 8. H5 and empirical execution boundary

H5-dependent material may be recorded but cannot support modality-specificity or cross-modal claims
until blind coder-B and adjudication close. No Stage-1C v2 artifact may report a project model result,
benchmark metric, reproduction outcome or prototype. Stage-2A requires its own explicit execution
gate after the family/branch portfolio is independently signed.
