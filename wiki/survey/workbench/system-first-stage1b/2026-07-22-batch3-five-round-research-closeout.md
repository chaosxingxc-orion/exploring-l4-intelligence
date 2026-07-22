---
title: "Stage-1B third 5x1,000 bounded sampling research closeout"
date: 2026-07-22
stage: "STAGE_1B_SYSTEMATIC_MAPPING"
scope: "abstract audit -> repository gate -> local PDF/e-print -> page-level audit -> capped consolidation"
verdict_boundary: "method-path and proximity mapping only; no novelty verdict"
---

# Stage-1B third 5x1,000 bounded sampling research closeout

## Conclusion

The owner-authorized third batch is complete. Five mutually disjoint rounds contributed exactly
5,000 new abstracts from the frozen 20,727-ID D0 union after excluding the 6,224-ID prior boundary.
Twenty-two papers passed human abstract/repository audit, all 22 PDFs were downloaded outside Git,
all received page-level full-text decisions, and unresolved rows are zero. Twenty-one papers survive:
3 speech experiment/measurement instruments, 15 open non-speech transfer paths, and 3 negative or
boundary records. One open paper was dropped as method-family duplication.

Across all eleven rounds, systematic abstract depth is now 11,000 papers (53.07% of D0). Including
224 earlier targeted/registry IDs, the explicit handled boundary is 11,224 IDs (54.15% of D0).
Full-text depth is 298 papers and the capped cross-batch roster contains 205 unique papers:
12 `KEEP_CORE`, 29 `KEEP_INSTRUMENT`, 40 `KEEP_TRANSFER`, and 124 `KEEP_NEGATIVE`. The retained set
is far below the 1,000-paper maximum. This is a bounded stop, not a D0-exhaustion claim.

## Replay correction and funnel

The first attempted replay exposed a boundary bug before any downloads: JSONL handled files were
searched as unstructured text, so five arXiv citations inside abstracts were incorrectly added to the
handled set (6,229 instead of 6,224). That run is preserved outside Git as a superseded audit cache.
The sampler now reads only each JSONL record's own `arxiv_id`, with a regression test; the formal run
replayed against exactly 6,224 handled IDs.

| Stage | R1 | R2 | R3 | R4 | R5 | Total |
|---|---:|---:|---:|---:|---:|---:|
| New abstract rows | 1,000 | 1,000 | 1,000 | 1,000 | 1,000 | 5,000 |
| `DEFER_REPRO_CHECK` | 620 | 429 | 28 | 130 | 160 | 1,367 |
| `EXCLUDE_ABSTRACT` | 380 | 571 | 972 | 870 | 840 | 3,633 |
| Deterministic `SELECT_FULLTEXT` | 0 | 0 | 0 | 0 | 0 | 0 |
| Human PDF promotions | 5 | 6 | 1 | 8 | 2 | 22 |
| Final retained | 5 | 6 | 1 | 7 | 2 | 21 |

The zero deterministic selections and 0.42% final retained yield show that the high-relevance head of
the frozen union is substantially depleted. Human audit remained useful because abstract phrases did
not expose several valid method boundaries; it did not broaden the batch into a generic agent survey.

## Repository reproducibility gate

Repository inspection is structural evidence only: reachability, declared license, source,
documentation, dependency/environment files, and selected evaluation/configuration structure. No
repository code, model, dataset, or benchmark was executed.

| Round | Paper-link URLs | Canonical repositories | Invalid | `OPEN_SOURCE_VERIFIED` | Receipt SHA-256 |
|---|---:|---:|---:|---:|---|
| 1 | 145 | 144 | 1 | 27 | `25ef9c72f91b499170b1eb7be1a796ea4793f3d91fcec706ba5238bf2a28ebd9` |
| 2 | 216 | 214 | 1 | 50 | `d1178dd57f74a6440b037aa641d6b4cdf314d62f189565d0c2fb18e5ecdef596` |
| 3 | 128 | 127 | 1 | 23 | `7adeedee8364a26cbb65b0ffe72e8b4e12ead79c6a3f2b81fa128f39d9ca0bdc` |
| 4 | 361 | 359 | 1 | 86 | `86af2524f4de30b5d417e64f4ba4bb5b63c3536a25664e0f1d7dd78b244df5a9` |
| 5 | 133 | 132 | 1 | 20 | `02cce8dde4633c6865ee4bfb56ea5a1a69eee4122f00ddd417c4e88eb665f69b` |

The 976 canonical checks plus five invalid URLs yielded 206 structurally open repositories. Only
method-distinct candidates entered the PDF stage; the rest remain external audit cache.

## Speech tasks and local-data fit

| Paper | Role | Full-text result | Local-data consequence |
|---|---|---|---|
| [UITron-Speech](https://arxiv.org/abs/2506.11127) | `KEEP_INSTRUMENT` | Qwen2.5-Omni is trained on synthetic speech/mixed-modality GUI data; the crop-and-refine grounding correction itself is training-free at inference. | Aguvis, OS-Atlas, ScreenSpot, and GUI-Odyssey assets are not in the local lock. It is an SLU/spoken-GUI instrument, not an immediately runnable local task. |
| [CAFA](https://arxiv.org/abs/2509.06382) | `KEEP_INSTRUMENT` | Ambient YAMNet features, audiogram and user feedback drive information-gain questioning, structured hearing-aid commands, an ethical regulator, and an independent LLM judge without domain-specific LLM fine-tuning. | The paper uses 200 synthetic fitting sessions and a 10-adult user study rather than a locked public speech dataset. No exact local data path exists. |
| [Phonological Subspace](https://arxiv.org/abs/2604.21706) | `KEEP_INSTRUMENT` | Training-free d-prime measurement over six frozen speech SSL backbones, with open analysis code and explicit cross-corpus calibration limits. | Local LibriSpeech is an exact corpus occurrence but contributes only 150 healthy controls. Dysarthria severity still needs non-local clinical corpora such as TORGO/UA-Speech/SAP; therefore the task is `REQUIRES_SPLIT_REVIEW`, not direct reproduction. |

No new `KEEP_CORE` paper emerged. The batch strengthens experiment and measurement coverage without
changing the existing direct-neighbor map.

## Transfer map

### Reward, routing, budget and stopping

- [DAS](https://arxiv.org/abs/2501.05803): training-free tempered SMC for reward-aligned sampling
  that explicitly limits reward over-optimization and diversity collapse.
- [DebUnc](https://arxiv.org/abs/2407.06426): uncertainty communicated through prompts or token
  weights between debate rounds.
- [Chain of Mindset](https://arxiv.org/abs/2602.10063): training-free step-level cognitive-mode router
  with a bidirectional context gate.
- [RVLM](https://arxiv.org/abs/2603.24224): no-fine-tuning generate/execute loop with adaptive depth
  and early termination; proprietary Gemini remains an implementation boundary.
- [FOREAGENT](https://arxiv.org/abs/2601.05930): trained pairwise predictor followed by verification;
  transferable as execution-budget allocation, not as a training-free result.

### Memory and knowledge representation

- [MemQ](https://arxiv.org/abs/2605.08374): runtime TD credit propagation over a memory-provenance DAG.
- [PlugMem](https://arxiv.org/abs/2603.03296): compact propositional and prescriptive knowledge units
  instead of raw trajectories.
- [CoPS](https://arxiv.org/abs/2410.16670): pessimism-based, distribution-matched prior-experience selection.
- [Procedural Memory Retrieval](https://arxiv.org/abs/2511.21730): a generalization cliff showing that
  embedding retrieval discards temporal procedure structure.
- [MemLens](https://arxiv.org/abs/2605.14906): long-context degradation versus memory-agent visual
  fidelity loss under storage-time compression.

### Search, evaluation and reproducibility environment

- [A-MapReduce](https://arxiv.org/abs/2602.01331): parallel wide-search decomposition, aggregation,
  experiential allocation, and cost measurement.
- [Pi-Serini](https://arxiv.org/abs/2605.10848): tuned lexical retrieval depth as a surfaced-evidence
  recall baseline for a literature knowledge layer.
- [Repo2Run](https://arxiv.org/abs/2502.13681): build/test feedback to replayable Dockerfiles; 361/420
  benchmark repositories reached executable environments.
- [One-Eval](https://arxiv.org/abs/2603.09821): traceable benchmark resolution, dataset/schema
  normalization, metric routing, human checkpoints, and rollback.
- [PaperBench](https://arxiv.org/abs/2504.01848): author-approved hierarchical reproduction rubrics,
  executable submissions, and a separately evaluated grading judge.

## Negative and deduplication evidence

- [AgentProp-Bench](https://arxiv.org/abs/2604.16706) separates judge reliability, parameter
  rejection, downstream recovery, and a model-dependent runtime interceptor.
- [MemSyco-Bench](https://arxiv.org/abs/2607.01071) tests rejecting, scoping, updating, and reconciling
  retrieved memories instead of assuming memory is always beneficial.
- [ThetaEvolve](https://arxiv.org/abs/2511.23473) persists GRPO-trained checkpoints at test time and
  is therefore a reproducible boundary, not training-free inference control.
- [HiRED](https://arxiv.org/abs/2408.10945) passed the repository and full-text checks but was dropped
  because its fixed-budget attention token dropping duplicates the retained VisionTrim method family.

## Replay and asset receipts

- Formal sampling summary SHA-256: `810aab2976f4a3f65cad132df2cfad8203ad249bce1985deecf4bd63684871e2`.
- Pre-sampling handled set: 6,224 IDs, SHA-256
  `928df92dea1f9bf1ba22b32b1733a5fc871fbf9d22b2b600872561ef0f3ba05d`.
- Round JSONL SHA-256: `07d9532a5d255d4c7819932a8a392bd7ddfab5e6124a869d8f821bbb3d239690`,
  `b1716e55086ab27b75846a171c228c072238cda6b2fff124c56450e2cbaf250c`,
  `49d64a3f19fc211b472c5d1eb6aa5f604e38f3e9af892e3e2dd9f081c8e0f72e`,
  `d532f7c0e9ca069d425284e7446741cc3024e1970797049349a8319e1ba46f49`, and
  `3026963e0fd58488734692fa56b5b253c10b6cbe0d8fa459a13d60f27d1faf26`.
- Promotion and human-override receipt SHA-256:
  `ee9fd5c47dbff1bbea49919cf5fbfb890d821ceb02df858c3102fe21e4426d77` and
  `08a4e700f82825fc09bb5ee2323448ce5164598fad56cbb2caa0a354037b2bc9`.
- Full-text triage: 22 rows, SHA-256
  `04ddc8de45d88cb0e8a1c6ebe4cc16cf4c016e4ec84245395df315a98b94cfac`.
- All 22 PDFs succeeded; all 21 retained papers also have successful e-print receipts. The append-only
  download ledger SHA-256 is `5476446a6df206d3aa625b563f990a03801b2c0725a3d718b312d384eb54e4b2`.
- Batch-3 retained roster: 21 rows, SHA-256
  `d4a60ce78bde619fd50faca2dd227aacf4853e5ada93b2d6dc691d941fe43bea`.
- Cross-batch retained roster: 205 rows, SHA-256
  `7e4093abcf1f49ffc38d23a94964f0a24ccf236f425fb325013a4a9e31bdc899`.
- Batch-3 Git registry shard: 21 metadata-only rows, SHA-256
  `9e3d530170920f887fdab0aa7292662ba8acb9b9e34ba74adfcbb32fcf11015d`.
- Three-shard generated view: 205 rows, SHA-256
  `4eab03cc61da1c1252159433ccf0b298879b5d729e4d92c1a8b6c850ff8229ee`.

PDFs, extracted text, rendered audit pages, e-prints, and repository receipts remain under
`SPEECHRL_DATA_DIR`. Git contains only scripts, links, hashes, decisions, page locators, reports, and
metadata-only registry records. No model, dataset, repository code, smoke test, metric run, or prototype
was executed.

