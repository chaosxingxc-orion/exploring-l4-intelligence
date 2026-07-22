---
title: "Stage-1B arXiv execution and local-fulltext snapshot"
date: 2026-07-21
role: "WORKBENCH execution receipt summary; not REC-0 completion or a novelty verdict"
stage: "STAGE_1B_SYSTEMATIC_MAPPING"
---

# Stage-1B arXiv execution and local-fulltext snapshot

## Frozen-query execution

Execution used the 65 registered arXiv rows without rewriting the observed query prefix. The runner
validated every frozen-row hash, retained failed attempts, paginated/split deterministically, stored
raw Atom bytes outside Git, and resumed through the bounded retry policy.

| Item | Result |
|---|---:|
| Frozen root rows executed | 65 / 65 |
| REC-1 rows | 535 |
| Successful result pages | 489 |
| Split-count probes | 39 |
| Failed attempts retained | 7 |
| Active failures after bounded retry | 0 |
| Unique arXiv IDs in offline BFS snapshot | 20,727 |
| Query/page source events retained | 32,688 |
| Raw Atom bytes hash-verified | 84,342,316 |
| First / last receipt UTC | 2026-07-21T12:30:19.242379Z / 2026-07-21T14:46:42.127957Z |

The local REC-1 JSONL is 1,272,129 bytes with SHA-256
`6a239a65aa16db0461aae3fb1e2c3bdedbbfc2d881a62636b6b3c7cb658306cc`. The offline BFS candidate
snapshot is 55,080,637 bytes with SHA-256
`afc3d85eab383f81c96d293b13d053767500baec485c89ce03aeff32f3425883`. It is stored with research
data under `speechrl-data/survey-bfs/stage1b-2026-07-21/`, not in Git. The builder and its tests remain
in `scripts/survey/` so the snapshot is reproducible from REC-1 plus the external raw responses.

These 20,727 D0 records are a retrieval union, not an included-work count or prevalence estimate.
Canonical identity resolution, REC-0 decisions, a second screen, T1 proceedings routes, and the
2026-07-16-to-execution-date delta batch remain open.

## Abstract-before-download gate

The opening adversarial-proximity queue contains 27 D1 `SELECT_FULLTEXT` decisions: 15 P0 method/
counterevidence papers, 10 P1 comparators, and 2 P2 measurement instruments. All 27 were selected
from title/abstract analysis before acquisition. After selection, the downloader fetched both the PDF
and e-print for every paper to the external survey store.

| Full-text item | Result |
|---|---:|
| Selected papers with PDF + e-print | 27 / 27 |
| Unique renditions independently re-hashed | 54 / 54 |
| Hash/byte mismatches | 0 |
| Total local rendition bytes | 213,312,554 |
| New P0 papers read at D2 | 15 / 15 |
| New P1/P2 papers read at D2 | 12 / 12 |
| Total local papers represented across opening D2 notes | 34 |

One short-lived overlapping downloader produced two successful receipts for the same
`2512.05542` PDF one second apart. Both rows have identical byte count and SHA-256; the duplicate
process was stopped and the 54 unique local renditions all verify against the latest successful ledger
row. No downloaded PDF/e-print is intended for Git. Git retains only the fetcher, URLs, timestamps,
byte counts, SHA-256 ledger, screening rationale, and derived method notes.

## Evidence-safe interpretation

The first D2 batch already establishes close general, multimodal, audio, and omni method paths:
reward/value-guided tree search, stateful sufficiency/reobserve loops, verifier-driven repair,
pre-execution action review, evidence-aware consensus, and cross-trial verbal reinforcement. It also
contains adverse controls: feedback may add little beyond retry, verifier rounds can undo correct
answers, sophisticated search can lose to simple aggregation, and active view selection can be
statistically unresolved when evidence extraction/calibration is weak.

This snapshot therefore narrows the remaining Stage-1B question to exact topology, information
access, persistent-state boundary, signal-to-action right, supply/evaluator attribution, and speech/
omni causal specificity. It does not support a novelty verdict, an empty-intersection statement, a
Stage-1C problem choice, or any model/dataset/prototype experiment.
