---
title: "Post-Stage-1B local full-text secondary filter v4"
date: 2026-07-22
role: "WORKBENCH analysis; current external snapshot is v4"
scope: "all files under SPEECHRL_DATA_DIR/survey-fulltext"
verdict_scope: "execution-shortlist refinement only; no novelty or Stage-1C problem selection"
---

# Post-Stage-1B local full-text secondary filter v4

## Conclusion

The local source contains **898 artifacts / 3,580,878,343 bytes**, including **451 unique PDFs** and
323 e-prints. All 451 PDFs were extracted and analyzed; extraction failures and low-text PDFs are both
zero. The 226-row Stage-1B registry is an exact subset, leaving 225 locally downloaded PDFs outside the
registry. Therefore, the secondary-processing denominator is 451, not 319 or 226.

The deterministic v4 pass routes the 451 papers as follows:

| Route | Papers |
|---|---:|
| explicit component training/model operation | 105 |
| explicit internal-state access | 17 |
| explicit vertical restricted-data barrier | 1 |
| Stage-1B negative/boundary only | 100 |
| measurement instrument only | 38 |
| transfer only | 89 |
| direct candidate before human correction | 4 |
| access contract needs manual review | 67 |
| no control path / low priority | 30 |

The two model-access exclusions total **122/451**. They are execution-shortlist exclusions, not removal
from the evidence portfolio.

## Human audit of load-bearing queues

The four automatic direct candidates reduce to **three** after page-level audit:

| arXiv | Audited route | Why |
|---|---|---|
| `2509.16971` AudioGenie-Reasoner | direct candidate | Training-free multi-agent refinement; evaluates on local MMAU-mini and MMAR. Paper says code “will be available”; live repository state was not checked. |
| `2510.02995` AudioToolAgent | direct candidate | Coordinates pretrained audio models as swappable tools, explicitly without new data/fine-tuning; local MMAR and a compatible MMAU test subset exist. Paper reports a GitHub repository; live state was not checked. |
| `2606.07264` VISA | direct candidate | Frozen/pretrained audio/vision experts with routing and disagreement resolution; MMAR is local. No code-availability claim is made load-bearing here. |
| `2505.22053` AudioGenie | **downgrade to transfer** | The mechanism is training-free and external, but its actual experiment object is MA-Bench. The automatic `mmau-mini` hit was non-load-bearing; MA-Bench is not in the local lock. |

The single restricted-data exclusion is `2605.24755`, a mental-health audio-diary study using ADAPT
participant transcripts. Page 1 identifies the clinical participant corpus; page 5 states that transcripts
were hosted on private institutional servers. It remains useful as a negative/vertical boundary, but is
not a local reproduction candidate.

All 12 Stage-1B core papers now have a second-pass route:

- model/internal boundary (5): `2411.05679`, `2505.20862`, `2605.31432` (DOA), `2606.05161`,
  `2606.17006`;
- instrument (1): `2512.16978`;
- transfer-only (6): `2508.02228`, `2509.12591`, `2605.24524`, `2606.03183`, `2607.06088`,
  `2607.11798`.

DOA is now resolved rather than merely “priority to inspect”: its policy derives a proxy alignment
signal from decoder self-attention, so it is a gray-box/internal-access comparator under the project
black-box contract.

## Vertical-domain finding

There are 132 PDFs with at least one title/abstract vertical-domain signal. Counts overlap by paper:
world/embodied 49, medical 32, education 31, finance 15, legal 14, 3D/spatial 11, and
science/engineering 8. Their data evidence is 15 local matches, 8 explicitly public/released but not
local, 108 with no matching local-data evidence, and 1 explicitly restricted case.

The important correction is semantic: **108 “no local match” papers are not 108 unavailable-data
papers**. They remain data-audit or transfer queues. This prevents domain names, patient-record
examples, proprietary model pretraining data, and privacy discussions in surveys from being promoted
into unsupported reproducibility claims.

## Reasoning and next queue

The next useful pass is no longer broad PDF filtering. It is bounded human coding of:

1. the three audited direct candidates;
2. 20 registry-backed transfer records (6 prior core + 14 prior transfer);
3. 69 unregistered transfer rows that need stable title/role/repository metadata;
4. 67 access-ambiguous rows, prioritizing speech/audio and reusable control mechanisms.

This pass should produce 3-5 Stage-1C problem/gap-hypothesis cards only after contradicting evidence,
kill criteria, data replacement feasibility, and reproduction scope are filled. It does not authorize
model loading, dataset metrics, reproduction runs, or prototypes.

## Provenance

- Source artifact ledger SHA-256: `800fb4c72ea3d0c50ed3ef73ac017657be29589f6b2c7ec4b15a263527124cb2`.
- v4 paper-analysis ledger SHA-256: `55b24547e58d19ec3190802da3d944ab682b4f1c7ed71f0caa432cd33666d172`.
- External snapshot: `SPEECHRL_DATA_DIR/survey-fulltext-secondary-analysis/2026-07-22-v4/`.
- Reproducer: `scripts/survey/sf_post_stage1b_corpus_refinement.py`.
- Verification: 21 tests pass; branch coverage is 90% for the reproducer; representative PDF pages for
  AudioToolAgent, DOA, and the clinical restricted-data paper were rendered and visually inspected.

## Invalidation conditions

Invalidate or rerun v4 if any source file/path/hash changes, a registry shard supersedes a paper role,
the dataset lock/local presence changes, a PDF version changes the load-bearing method/data contract,
or human audit overturns an automatic disposition. `v1`-`v3` are already superseded by v4 and must not
be cited as current counts.
