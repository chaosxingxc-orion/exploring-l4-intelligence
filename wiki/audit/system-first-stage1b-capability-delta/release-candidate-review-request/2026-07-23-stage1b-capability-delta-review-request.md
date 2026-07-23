---
title: "Stage-1B capability-delta release-candidate independent review request"
date: "2026-07-23"
artifact_type: "INDEPENDENT_REVIEW_REQUEST"
campaign: "system-first-stage1b-capability-delta"
round: "release-candidate-review-request"
review_target: "SF-STAGE1B-CAPABILITY-DELTA-REVIEW-PACKAGE-RC1"
review_package_manifest_sha256: "ee8f0564069475f58f9be313a7978db662665d1d379b213d3005507c59dea3a6"
requested_verdict: "SIGN_STAGE1B_CAPABILITY_DELTA_RELEASE"
request_grants_authority: false
self_signed: false
frozen_stage1b_v5_release: "38fb9435d0c35e226ad62b16015a6dbee054e6c2"
stage1c_activation_requested: false
experiment_execution_requested: false
novelty_verdict_requested: false
---

# Stage-1B capability-delta release-candidate review request

Please independently review the package bound by SHA-256
`ee8f0564069475f58f9be313a7978db662665d1d379b213d3005507c59dea3a6` at:

`wiki/survey/workbench/system-first-stage1b-capability-delta/review-package-manifest.json`

The requested verdict is `SIGN_STAGE1B_CAPABILITY_DELTA_RELEASE`. This request does not grant that
verdict and does not ask the reviewer to authorize Stage-1C experiment mapping or research execution.

## Claimed release-candidate facts to verify

1. The frozen Stage-1B v5 release remains commit
   `38fb9435d0c35e226ad62b16015a6dbee054e6c2`; no registry shard or v5 table is rewritten.
2. The delta contains exactly eight owner-approved seeds and six one-hop promotions, with no duplicate
   canonical identities.
3. All 14 works have official identity/version, PDF, eprint and extracted-text bindings; 42 external
   SHA-256 checks pass.
4. The append-only full-text ledger has two identical retry events, not conflicting renditions; no rows
   were removed to hide the retries.
5. One-hop extraction saw 303 regex-resolvable arXiv identities. Six are promoted and 297 remain
   seen-not-promoted outside the denominator. DOI/title-only and forward closure are explicitly open.
6. The canonical census recomputes 226 frozen works, 59 appendix routes with seven base overlaps, four
   disjoint priority works, a 282 inherited union and a disjoint 14-work delta, for 296 candidate works.
7. K/S/M are not treated as symmetric folders: content, persistence, primary intervention, system
   carrier, control status and MM0-MM3 level are coded separately.
8. Every work is explicitly `REFERENCE_CONTEXT` or `BORROWED_PROTOCOL_ANALOGUE`. The delta contains
   zero claimed speech/omni reproduction anchors, and all reproduction subtypes remain null.
9. Paper-reported numbers have exact locators, remain within-paper evidence and are not project results
   or cross-paper numerical aggregates.
10. The detailed Chinese proposal defines unexecuted, unranked D0/D1/D2/D3/D4 experiment families,
    local readiness, falsifiers and kill criteria without granting Stage-1C or Stage-2 authority.

## Adversarial questions

- Does any promoted work lack a real backward edge from at least one authorized seed?
- Does the 296 census accidentally count all 303 citations, duplicate appendix routes, or overwrite the
  frozen 226 denominator?
- Is a system bundle silently credited to knowledge, skill and memory without a matched ablation?
- Is a multimodal task mislabeled as causally multimodal despite a text shortcut or caption substitution?
- Is “frozen core” used to conceal supervised external asset construction or online updates?
- Is any borrowed VLM/text protocol described as a reproduction, or are paper values extrapolated to
  speech/omni?
- Are SkillsBench/SkillFlow negative results and Memory-R1's trained boundary retained strongly enough
  to prevent a one-sided skills or RL conclusion?
- Do local-asset claims distinguish bytes present from loader, license, evaluator and access readiness?
- Can the checker reproduce the review manifest and fail on external hash, citation parent, census,
  relation or frozen-release drift?

## Acceptable outcomes

- `SIGN_STAGE1B_CAPABILITY_DELTA_RELEASE` if identity, provenance, path mapping, limitations and machine
  contract are sufficient for the 14 works to become a signed Stage-1C input overlay; or
- `WITHHOLD_STAGE1B_CAPABILITY_DELTA_RELEASE` with bounded, actionable defects.

Even a positive verdict releases only the Stage-1B delta evidence surface. Stage-1C mapping still
requires owner scope authorization and the separate `SIGN_STAGE1C_V2_EXPERIMENT_MAPPING` gate; model
execution and Stage-2A remain independently withheld.
