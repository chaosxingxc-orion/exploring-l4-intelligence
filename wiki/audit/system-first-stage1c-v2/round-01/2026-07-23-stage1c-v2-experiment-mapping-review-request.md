---
title: "Stage-1C v2 experiment-family mapping independent review request"
date: "2026-07-23"
artifact_type: "INDEPENDENT_REVIEW_REQUEST"
campaign: "system-first-stage1c-v2"
round: "round-01"
at_issue_status: "SUBMITTED_FOR_INDEPENDENT_REVIEW"
requested_verdict: "SIGN_STAGE1C_V2_EXPERIMENT_MAPPING | WITHHOLD_WITH_BOUNDED_DEFECTS"
review_package_manifest_sha256: "64d19df36df5d7cebbae4a7a885561ef7d0996d10856a39d16eb690b63290f21"
frozen_stage1b_release: "38fb9435d0c35e226ad62b16015a6dbee054e6c2"
novelty_verdict_requested: "NO"
model_or_metric_execution_requested: "NO"
---

# Stage-1C v2 experiment-family mapping independent review request

## Decision requested

Please review the exact pre-sign package bound by SHA-256
`64d19df36df5d7cebbae4a7a885561ef7d0996d10856a39d16eb690b63290f21` at
`wiki/survey/workbench/system-first-stage1c-v2/review-package-manifest.json` and return exactly one
of:

- `SIGN_STAGE1C_V2_EXPERIMENT_MAPPING`; or
- `WITHHOLD_WITH_BOUNDED_DEFECTS`, identifying the failed contract and minimum repair.

The package proposes an experiment-led Stage-1C v2 derivation over the fixed 226-paper Stage-1B
registry. It defines run-config experiment cells, evidence-backed dataset lineage versus non-lineage
relations, strict experiment-family core membership, typed validation/transfer/falsifier/instrument
edges, local readiness, and evidence-gated research branches.

## Scope of a possible signature

A signature would authorize only:

1. 226/226 experiment-level evidence recoding from already retained full texts;
2. dataset-graph and experiment-family synthesis;
3. unexecuted local experiment protocols; and
4. evidence-gated branch dossier preparation.

It would not authorize a model/API call, dataset or benchmark metric, paper reproduction, prototype,
technical-innovation convergence, novelty verdict, or Stage-2A execution. A later independent
`SIGN_STAGE1C_V2_FAMILY_BRANCH_PORTFOLIO` would still be required to freeze the branch handoff, and
Stage-2A execution would remain separately withheld.

## Gate questions

1. Does one experiment cell represent one run configuration with multiple result observations?
2. Are factual dataset lineage and semantic/protocol relations unambiguously separated?
3. Does complete core-signature equality prevent incomparable experiments from being merged?
4. Do typed related-evidence edges preserve relevance without granting direct numeric comparability?
5. Are family results stratified by dataset lineage and access before synthesis?
6. Do local readiness, five branch gates and four experiment arms produce a falsifiable but
   unexecuted Stage-2A handoff?
7. Are H5, no-execution and no-novelty boundaries fail-closed?
8. Does the bootstrap cover 226/226 canonical records while claiming zero cells, families, branches
   or completed adjudications before signature?

## At-issue evidence state

The executable pre-sign report is `PASS_PRE_SIGN_CONTRACT_ONLY` with `authority_effect=NONE`, 226
unique paper rows, zero experiment cells, zero family memberships, zero branches and zero model or
metric executions. Generated PASS is evidence for contract integrity only; it cannot answer this
review request or self-grant authority.
