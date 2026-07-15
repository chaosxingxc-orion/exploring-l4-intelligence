---
title: "T5 — headroom composition: internal-realization gap vs capability/knowledge gap (from own samples)"
date: 2026-07-05
stage: 1-directional
purpose: "Decompose the frozen omni's headroom WITHOUT leakage (own samples only), to see which legitimate lever can realize which part — and to size the multimodal memory's target market (the capability/knowledge gap)."
---

> **LOG** — Stage-1 过程记录（hypothesis-grade），非现行真源；现行结论以 [[Decision-Log]] 与 [[Per-Work-Status]] 为准。

# T5 — What is the headroom made of?

> Legitimate (Information-Boundary Guard): uses **only the model's own N=8 samples** (P2, n=150). No golden
> beyond scoring. Two components fall straight out of greedy vs oracle-over-N.

## The decomposition
For each item: **greedy** = deployed answer; **oracle** = correct iff ≥1 of N samples is correct.
- **Internal-realization gap = oracle − greedy** — the correct answer IS in the model's own sample
  distribution, but greedy misses it. In principle internally realizable (better decoding/selection) — but
  E10/E10b showed **no deployable label-free selector realizes it.**
- **Capability/knowledge gap = 1 − oracle** — **NO** sample is correct in N=8 → the answer is essentially
  absent from the model's distribution → **beyond internal realization; needs an EXTERNAL signal
  (knowledge/memory).** This is the multimodal memory system's target market.

| Surface | greedy | oracle@8 | **internal-realization gap** (oracle−greedy) | **capability/knowledge gap** (1−oracle) |
|---|---|---|---|---|
| big-bench-audio (en, reasoning) | 0.567 | 0.847 | +0.280 | 0.153 |
| mmau-mini (en, SQA-reasoning) | 0.653 | 0.800 | +0.147 | **0.200** |
| SQuAD-zh (zh, extractive) | 0.753 | 0.893 | +0.140 | 0.107 |
| vocalbench-zh (zh, **knowledge QA**) | 0.467 | 0.573 | +0.107 | **0.427** |
| spoken-squad (en, extractive) | 0.873 | 0.960 | +0.087 | 0.040 |

## Reading
1. **The internal-realization gap is real everywhere (+0.09…+0.28)** — and we have shown (E10/E10b) that
   internal levers (self-selection, two-system verification) cannot deployably realize it. Legitimate
   candidates left for this part: a **verifiable-reward** selector where a deployable reward exists (T4).
2. **The capability/knowledge gap is LARGEST on the knowledge-QA task** — **vocalbench-zh 42.7%**: on ~43%
   of items the frozen model produces **no** correct answer in 8 tries. That is not a decoding problem; it
   is a **knowledge-boundary** problem → exactly what an **external multimodal memory** (T6) targets.
   Perception-heavy or reasoning tasks (mmau 20%, big-bench 15%, extractive 4–11%) have a smaller such gap.
3. **Caveat:** "no-correct-in-8" is a proxy (more samples might find some) and mixes true knowledge gaps
   with hard perception gaps (mis-hearing every time). For knowledge-QA (fact recall) it is predominantly
   the former. To split knowledge vs perception further needs the T6/W4 probes — but the directional split
   is clear: **knowledge-QA is knowledge-bound; that is the memory's market.**

## Implication for the plan
- **Memory (T6)** targets the **capability/knowledge gap** (external knowledge, input-keyed) — largest and
  most clearly memory-shaped on knowledge-QA (vocalbench-zh, ~43%). First memory probe should be there.
- **Verifiable-reward selection (T4)** targets the **internal-realization gap** where a deployable reward
  exists.
- **W4 read-out** targets the perception slice of both (better key + better perception), not the knowledge
  gap (consistent with #37: W4 reorganizes own info, adds none).
