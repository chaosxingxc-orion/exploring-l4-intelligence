---
artifact_id: "SF-STAGE1B-CAPABILITY-DELTA-WORKBENCH-RC1"
date: "2026-07-23"
status: "RELEASE_CANDIDATE_AWAITING_INDEPENDENT_REVIEW"
authority: "AUTHORIZE_STAGE1B_CAPABILITY_DELTA_MAPPING"
requested_review_verdict: "SIGN_STAGE1B_CAPABILITY_DELTA_RELEASE"
stage1b_v5_release: "38fb9435d0c35e226ad62b16015a6dbee054e6c2"
stage1b_v5_mutated: false
stage1c_activated: false
---

# Stage-1B capability-delta release candidate

This workbench contains the bounded capability-oriented Stage-1B delta authorized by the owner on
2026-07-23. It preserves the frozen Stage-1B v5 release and adds a separate, reviewable surface for
knowledge, skill, memory, multimodal-agent-system and training-free reward-guided-control paths.

The release candidate contains eight owner-approved exact-ID seeds and six promoted one-hop
citation works. The machine census is:

- frozen Stage-1B v5 registry: 226 unique works;
- CURRENT 59-route appendix: 52 outside the frozen base and 7 overlapping it;
- CURRENT priority intake: 4 additional works;
- inherited canonical union: 282;
- capability delta: 14 works, disjoint from the inherited union;
- release-candidate surface: 296 unique works.

The 303 regex-resolvable arXiv identities seen in the bounded backward-citation pass are not a new
paper denominator. Six are promoted; 297 remain seen-not-promoted and have not received a paper
audit. Forward citation closure was waived after the public unauthenticated index returned rate-limit
responses. No literature-universe closure claim is permitted.

## Read order

1. `capability-delta-contract.md` — authority, ontology and acceptance contract;
2. `capability-path-map.md` — evidence-backed D0-D4 map and strict reference/borrow/reproduce
   dispositions;
3. `stage1c-v2-capability-research-program-zh.md` — detailed Chinese research proposal for owner
   review after an independent delta signature;
4. `data/capability-delta-records-v1.json` — 14 exact-ID, hash-bound paper records;
5. `data/one-hop-promotions-v1.json` and `data/backward-citation-*` — bounded citation provenance;
6. `data/canonical-census-v1.json` — deterministic canonical surface census;
7. `docs/checks/stage1b-capability-delta/2026-07-23-rc1/` — generated contract reports.

## Gate

This package requests an independent `SIGN_STAGE1B_CAPABILITY_DELTA_RELEASE`. It is not self-signed.
Until that verdict is registered, the 14 records are not Stage-1C inputs and no experiment-family
scale-out, branch formation, reproduction, benchmark run, prototype or research-model invocation is
authorized.
