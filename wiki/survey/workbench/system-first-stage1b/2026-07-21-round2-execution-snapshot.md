---
title: "Stage-1B round-2 execution snapshot"
date: 2026-07-21
stage: "STAGE_1B_SYSTEMATIC_MAPPING"
role: "WORKBENCH execution receipt; not REC-0 completion, occupancy, or novelty verdict"
---

# Stage-1B round-2 execution snapshot

## Priority queue and abstract gate

The deterministic queue builder read the 20,727-ID frozen D0 snapshot, removed the 31 previously
handled IDs that were actually present in D0 (34 exclusion IDs were supplied), ranked 20,696 eligible
records, and wrote a 120-row manual-review queue. Six protocol sentinels were forced to the front with
`query_recall_credit_for_forced_entry=false`. The queue is an ordering aid only: every row remains
`ABSTRACT_REVIEW_PENDING` until a human-readable abstract decision is recorded.

| Item | Result |
|---|---:|
| D0 input IDs | 20,727 |
| Eligible after matched prior-work exclusions | 20,696 |
| Priority queue rows | 120 |
| Forced sentinels | 6 |
| Priority-pass abstracts reviewed | 40 |
| `SELECT_FULLTEXT` / `DEFER` / `ABSTRACT_EXCLUDE` | 26 / 10 / 4 |
| Citation-triggered abstracts additionally selected | 4 |

The external queue is 310,427 bytes with SHA-256
`5cdba4e4e06109374e5f1c9099140b721d53a902faf6ee9a2a8804d2041bacb3`. Git retains the builder,
tests, abstract rationales, and external path/hash, not the 20,727-row D0 or 120-row queue bytes.

## Citation-triggered pass

An offline arXiv-ID scan of the first 16 opened round-2 texts found 410 distinct cited arXiv IDs.
Common backbone/system reports, datasets, and generic background were not expanded merely because
they were frequently cited. Four method/comparison records passed abstract screening and then D2:
`2503.12271`, `2501.09732`, `2408.03314`, and `2407.21787`.

Only `2503.12271` was discovered solely through citation traversal. The other three also occur in the
frozen D0 union, so their citation edges corroborate proximity but receive no additional query-recall
credit. This is a bounded citation pass, not citation closure.

## Download-after-abstract and local D2

The 26 priority-pass selections and four citation selections were downloaded only after the abstract
gate. All 30 PDFs were opened locally and mapped at D2. Twenty-nine e-prints are also present; the
`2503.12271` e-print failed twice with bounded SSL EOF retries, while its PDF downloaded and verified.

| Full-text item | Result |
|---|---:|
| Selected/read papers with PDF | 30 / 30 |
| Papers with PDF + e-print | 29 / 30 |
| Local renditions independently re-hashed | 59 / 59 available |
| Hash/byte mismatches | 0 |
| Verified local rendition bytes | 282,538,452 |

The append-only Git ledger is 112,430 bytes with SHA-256
`e08c069ea34b1821a585abff994349f8b15a7b10aab779b4a0e1b4e36526c1c9`; it retains URLs,
timestamps, attempts, sizes, SHA-256 receipts, and external paths. PDFs/e-prints and extracted text
remain under `speechrl-data/survey-fulltext/` and are not Git artifacts.

## Execution-date delta and T1 status

The 65-row append-only delta manifest covers the closed interval
`submittedDate:[202607160000 TO 202607212359]` without rewriting the frozen parent queries. It is
79,074 bytes with SHA-256
`86200b3a13f7fcf804dc960c0f5a3db852561dfb6db3523c884be783748edf4e`.

Four root rows were attempted and their failures retained in the external REC-1 delta ledger: one SSL
EOF, one HTTP 429, and two HTTP 503 outcomes. A later single one-result health probe timed out with
zero bytes after 25 seconds. Execution stopped rather than multiplying retries; 61 rows therefore remain
unattempted. This is **endpoint unavailable / delta incomplete**, not a zero-hit result. The external
4-row ledger is 4,504 bytes with SHA-256
`f1e6e9ba69b3ffb39b9c3c94a1c85624609622df935b6a19d53001317d44760b`.

The 50 T1 proceedings routes were not executed in round 2. Their historical route/status validation is
not a substitute for an execution-date REC-7 title scan. Both delta completion and T1 remain explicit
recall tasks for the next execution batch.

## Method-path result, without verdict

The second-round paths sharpen five separations that the next REC-2 coding pass must preserve:

1. candidate supply versus evaluator precision versus controller allocation;
2. same-core intrinsic signals versus external learned judges/reward models;
3. no base-model update versus no method-specific training anywhere;
4. task-native transforms versus retrieval or other answer-bearing external information; and
5. fixed-budget scaling versus a real stop/abstain/cancellation right.

Native-audio proximity now includes encoder-neuron intervention (IAAN) and uncertainty-gated temporal
contrastive decoding (TCD). Reward-guided audio generation and SMC search are adjacent but depend on
external evaluators. Multiple adverse studies show that self-refinement can degrade, visual attention can
decay with longer reasoning, and candidate coverage can rise while selection precision plateaus.

These observations map paths and invalidating conditions only. They do not establish an empty
intersection, technical novelty, Stage-1C problem ranking, or authority for model/dataset/prototype work.
