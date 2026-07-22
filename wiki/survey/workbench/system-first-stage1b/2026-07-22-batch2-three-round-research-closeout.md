---
title: "Stage-1B second 3x1,000 bounded sampling research closeout"
date: 2026-07-22
stage: "STAGE_1B_SYSTEMATIC_MAPPING"
scope: "abstract audit -> repository gate -> local PDF/e-print -> page-level audit -> capped consolidation"
verdict_boundary: "method-path and proximity mapping only; no novelty verdict"
---

# Stage-1B second 3x1,000 bounded sampling research closeout

## Conclusion

The owner-authorized second batch is complete. Three non-overlapping rounds contributed exactly
3,000 new abstracts from the frozen 20,727-ID D0 union. Twenty-five papers passed the bounded
abstract/repository audit, all 25 PDFs were downloaded outside Git, all 25 received page-level
full-text decisions, and unresolved full-text rows are zero. The second batch retains 2 core speech
control paths, 4 speech experiment/representation instruments, 17 repository-verified non-speech
transfer paths, and 2 negative/comparator records.

Cross-batch consolidation now contains 184 unique retained papers, below the 1,000-paper maximum:
12 `KEEP_CORE`, 26 `KEEP_INSTRUMENT`, 25 `KEEP_TRANSFER`, and 121 `KEEP_NEGATIVE`. The scan stops
here as directed. D0 is not exhausted, and no exhaustion claim is made.

## Auditable funnel

| Stage | Round 1 | Round 2 | Round 3 | Batch total |
|---|---:|---:|---:|---:|
| New abstract rows | 1,000 | 1,000 | 1,000 | 3,000 |
| Deterministic `SELECT_FULLTEXT` | 4 | 0 | 0 | 4 |
| `DEFER_ABSTRACT` | 13 | 0 | 0 | 13 |
| `DEFER_REPRO_CHECK` | 748 | 633 | 80 | 1,461 |
| `EXCLUDE_ABSTRACT` | 235 | 367 | 920 | 1,522 |
| Audited PDF promotions | 14 | 6 | 1 | 21 |
| PDFs/full texts read | 18 | 6 | 1 | 25 |

The deterministic layer was deliberately high precision. Human audit promoted a paper only when a
speech-primary method exposed a direct control/evaluation question, or a non-speech paper had both a
directly transferable method and a paper-linked repository that passed the structural open-source
gate. This recovered important false negatives such as DOA, DPRM, EasyEdit2, ASC-MQRA, SAGE,
EvilGenie, Gome, Self-Correcting RAG, and Bayesian Red Teaming without broadening the batch into a
generic agent/vision survey.

Across all six owner-directed rounds, 6,000 systematically sampled abstracts have now been read
(28.95% of D0). Including 224 previously handled targeted/registry IDs, the explicit handled boundary
is 6,224 IDs (30.03% of D0). Full-text depth is 276 papers and the consolidated retained set is 184.
The retained yield declined from 159/3,000 in batch 1 to 25/3,000 in batch 2, supporting the bounded
stop and transition to environment/knowledge-base construction.

## Repository reproducibility gate

Repository inspection is structural evidence, not an execution/reproduction claim. It checks
reachability, visible license, source, environment/configuration, evaluation entry points, and
weights/download structure. No repository code, model, or dataset was executed.

| Round | URL receipts | `OPEN_SOURCE_VERIFIED` | Incomplete/unlicensed/manual | Unreachable/invalid | Receipt SHA-256 |
|---|---:|---:|---:|---:|---|
| 1 | 180 | 25 | 49 | 106 | `2e7a4e2acc1f4381fa50b2b1076aa54f04e4899837f875db3b082ed246b1f53b` |
| 2 | 94 | 22 | 35 | 37 | `70828287e488deb8b22a5005a32c327c0de3b2fa304454672f14270ff62cb01b` |
| 3 | 114 | 32 | 39 | 43 | `6e11ecd474ddf3c21f225fa2b0bdd1c051bb6b0f3b8662a5fb047ab9f4f8c751` |

The 388 receipts contain 79 structurally verified open-source repositories. Seventeen non-speech
papers were retained after method-family deduplication; the remainder stay as external audit cache
and do not enter the active registry.

## Speech tasks and local-data fit

| Paper | Bounded role | Speech task/control path | Paper data versus local lock | Experiment implication |
|---|---|---|---|---|
| [DOA](https://arxiv.org/abs/2605.31432) | `KEEP_CORE` | Training-free SpeechLLM SimulST read/write policy from decoder self-attention; bounded audio-history pruning | MCIF and ACL 60/60 are not local; local CoVoST2/FLEURS-R are task-related but not the paper's long-form split | Highest-proximity method. Reproduction requires decoder-attention access; the local Qwen3-Omni GGUF path does not yet establish that interface. |
| [Flow Matching Speech Separation](https://arxiv.org/abs/2607.06088) | `KEEP_CORE` | Frozen speaker encoder scores stochastic separation candidates; biometric best-of-N plus chunk alignment | Libri2Mix is not local; LibriSpeech is source-related but not an exact replacement | Direct speech best-of-N analogue, but no paper-linked repository and no exact local dataset block immediate reproduction. |
| [SURE](https://arxiv.org/abs/2605.30899) | `KEEP_INSTRUMENT` | Unified evaluation, normalization, RPS scoring, and paper/code-to-runnable-recipe conversion | Exact local coverage includes LibriSpeech ASR, CoVoST2 ST, and MELD SER; local SLURP is relevant but the reported SLU evaluation uses MMSU-Reason | Best template for the experiment harness and knowledge-base-to-recipe bridge. Dataset/split use must remain explicit. |
| [Omnilingual SONAR](https://arxiv.org/abs/2603.16606) | `KEEP_INSTRUMENT` | Trained multilingual/cross-modal speech embedding and similarity-search comparator | Local FLEURS-R requires split review; local LibriSpeech is an exact ASR-family asset | Useful embedding/reward feature comparator, not a training-free control method. |
| [StepAudio 2.5](https://arxiv.org/abs/2605.23463) | `KEEP_INSTRUMENT` | RLHF-trained omni speech model with ASR multi-token verification, preference TTS, and generative-reward realtime dialogue | LibriSpeech is locally usable for ASR; FLEURS-R requires split review; other report benchmarks are absent | Architecture/reward/decoding comparator only; the load-bearing method is trained. |
| [High-Fidelity Neural PPGs](https://arxiv.org/abs/2402.17735) | `KEEP_INSTRUMENT` | Pitch/pronunciation disentanglement and acoustic pronunciation distance; MIT-licensed package | Paper uses Common Voice/TIMIT/Arctic; no exact standalone local Common Voice snapshot | Representation/control instrument; not a frozen SpeechMLLM method. |

## Transfer map for experiment design and citation use

The 17 non-speech transfers are more useful when grouped by the component they can instantiate than
as a single citation pool.

### Candidate generation, ordering, budget, and falsifier search

- [DivInit](https://arxiv.org/abs/2606.17209): diversify first-turn query seeds before parallel
  rollouts; directly tests whether breadth is wasted by correlated candidates.
- [DPRM](https://arxiv.org/abs/2604.24357): keep the host model/loss/data fixed and replace reveal
  order with online reward estimates plus Soft-BoN reweighting.
- [ASC-MQRA](https://arxiv.org/abs/2606.04323): stochastic self-consistency followed by vote-margin
  triggered re-arbitration; the test-set regression is evidence that uncertainty triggers need
  calibration and an abstention/stop rule.
- [Imagine-then-Plan](https://arxiv.org/abs/2601.08955): adaptive lookahead horizon from task progress
  and future-trajectory feedback; separate its prompted training-free and RL-trained variants.
- [Bayesian Red Teaming](https://arxiv.org/abs/2305.17444): query-efficient black-box failure search
  using past evaluations and diversity-aware Bayesian optimization.
- [Gome](https://arxiv.org/abs/2603.01692): preserve diagnostic feedback as update direction, success
  memory as momentum, and parallel traces as distributed optimization.
- [Self-Correcting RAG](https://arxiv.org/abs/2604.10734): jointly allocate context under a budget and
  explore answers with NLI-rewarded MCTS.
- [CyclicReflex](https://arxiv.org/abs/2506.11077): zero-extra-compute reflection-token logit
  scheduling; a minimal decoding-control baseline.

### Internal-state steering, routing, and token retention

- [VISTA](https://arxiv.org/abs/2502.03628): training-free activation and token-logit steering.
- [EasyEdit2](https://arxiv.org/abs/2504.15133): reusable parameter-preserving steering-vector
  generation/application interface.
- [SAGE / SPD-Faith](https://arxiv.org/abs/2602.07833): train-free evidence calibration derived from
  attention decay and residual-stream failure analysis.
- [VisionTrim](https://arxiv.org/abs/2601.22674): global/local token saliency plus text-guided token
  complement; a candidate analogue for acoustic-token budgets.
- [CLiViS](https://arxiv.org/abs/2506.17629): training-free planner/perceiver orchestration with a
  dynamic cognitive map and evidence memory.

### Knowledge and evidence substrates

- [A-MEM](https://arxiv.org/abs/2502.12110): dynamically generated, linked, and evolving memory notes.
- [MAGIC-Video](https://arxiv.org/abs/2605.08271): typed multimodal memory graph plus long-horizon
  narrative chain.
- [Visual Agentic Memory](https://arxiv.org/abs/2605.16481): online retention, hierarchical memory,
  retrieval, raw-evidence inspection, and bounded termination.
- [SkillSmith](https://arxiv.org/abs/2605.15215): compile large procedural skills into minimal runtime
  interfaces with provenance and a reproduction checklist.

## Negative and comparator evidence

- [LLaVA-CoT](https://arxiv.org/abs/2411.10440) remains a trained multimodal comparator whose SWIRES
  search demonstrates staged reward-guided expansion and retracing; it is not evidence for an
  end-to-end training-free method.
- [EvilGenie](https://arxiv.org/abs/2511.21654) supplies the main verifier falsifier: held-out tests,
  LLM judges, edit detection, and human review disagree in informative ways, and capable agents can
  optimize the visible environment instead of the intended task.

## Environment and knowledge-base consequences

The next environment should be built around four separable interfaces:

1. A SURE-like normalized evaluation layer with explicit task, split, post-processing, metric, and
   report contracts for local LibriSpeech, CoVoST2, FLEURS-R, MELD, SLURP, MMAR/MMAU/MMSU, and the
   existing lock.
2. Frozen inference adapters for candidate generation, score/verifier calls, selection/routing,
   budget/stopping, and trace capture. DOA needs an attention-exposure feasibility check before it can
   be selected as the first reproduction target.
3. A falsifier layer that treats reward hacking, candidate correlation, distribution-shifted
   uncertainty triggers, and judge disagreement as first-class tests rather than afterthoughts.
4. A registry-backed executable knowledge layer: metadata and page locators in Git, downloaded bytes
   external, and SkillSmith/A-MEM-style bounded interfaces that can materialize an experiment recipe
   without loading the full survey into context.

This report does not authorize model loading, smoke tests, metrics, dataset experiments, or
prototypes. It only closes the owner-authorized scan and prepares the evidence boundary for that
separately authorized phase.

## Replay and asset receipts

- Frozen D0 SHA-256: `afc3d85eab383f81c96d293b13d053767500baec485c89ce03aeff32f3425883`.
- Dataset lock SHA-256: `1790b43c0c2c9ba8b1a3d1ce3d1588d3aa84e63f7d680cef78e20da7adf70c1f`.
- Sampling summary SHA-256: `cb5d5d5faaa9beb443e10aea44932b6330b495f250ef5ad5eaf4105135652786`.
- Pre-sampling handled-ID receipt: 3,224 IDs,
  `4e9155c92099aefb15f313edab07eeef2d0ca2a58944d832bcee1fa30e693418`.
- Round JSONL SHA-256: round 1
  `4ebf11169e9d18bcb8305129e17aeea36e5ea9b73f2fc5c8d29c2dd93f2fa5ee`; round 2
  `05ebf7fdbec453bcdab6b16b299988a870b837fa38c01f3b5207d833e0baff92`; round 3
  `d6719be9504ab2a61786d22ab619e07990d3bb2c22de6ae8c01eabb6a227bd63`.
- Batch-2 full-text triage: 25 rows, SHA-256
  `9d64826e0b966a3db4f3c8be1baf348c48267ead413ebb7d2d1b61cd66d61c50`.
- Download ledger: all 25 batch-2 papers have successful PDF and e-print receipts; ledger SHA-256
  `dbeac340cc9af05c9872199e04ebb23b3319c8688ede315800413ca4efdd337f`.
- Batch-2 retained roster: 25 rows, SHA-256
  `2a22b194fc7041d82772f0ba6f114c686586557b6e22e510b88db58b4091380f`.
- Cross-batch retained roster: 184 rows, SHA-256
  `3ec9e6fdff6e07ad6408dc97d34b9ae5828b160f2545fb08ae8c6ee1ae51a69d`.
- Git registry shard: `stage1b-bounded-batch2-2026-07-22-papers.jsonl`, 25 metadata-only rows,
  SHA-256 `90256eae28f53bd6ab536936fa7ee940ccb58e5b3f3dc555bab21f51137bb75a`.
- Combined generated registry view: 184 rows, SHA-256
  `8788f7b8d6a56afc364f2f29059d1393c175513e4180672fa1d2bc238d12fd70`.

PDFs, extracted text, e-prints, repository receipts, and consolidated working rosters live under
`SPEECHRL_DATA_DIR`. Git contains only scripts, download links/status/hashes, bounded decisions,
page locators, reports, and registry views.
