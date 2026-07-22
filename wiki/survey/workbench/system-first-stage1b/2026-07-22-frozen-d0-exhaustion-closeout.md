---
title: "Stage-1B frozen-D0 identity exhaustion closeout"
date: 2026-07-22
stage: "STAGE_1B_SYSTEMATIC_MAPPING"
scope: "D0 exhaustion -> abstract audit -> repository gate -> local PDF/e-print -> page audit -> capped consolidation"
authority: "owner direction in active task: process every remaining paper with the same workflow"
verdict_scope: "method-path and proximity mapping only; no novelty verdict"
---

# Stage-1B frozen-D0 identity exhaustion closeout

## Outcome

The frozen 20,727-ID D0 corpus is exhausted. The final run processed the exact 9,602-ID set
`D0 - prior_handled`, in nine 1,000-paper rounds plus one 602-paper tail. Together with the earlier
11,000 systematic samples and 125 in-D0 targeted/registry records, every D0 identity now has an
abstract-level record. The handled ledger also contains 99 targeted papers outside D0; those 99 are
reported separately and are never subtracted from the D0 denominator.

The final batch advanced 21 papers to local PDF review and retained all 21 after page-level audit:
14 instruments, 5 transferable mechanisms and 2 negative/boundary records. Cross-batch full-text
depth is 319 papers; the retained roster is 226/1,000 = 12 core + 43 instrument + 45 transfer +
126 negative, with 93 drops and zero unresolved rows. This is a corpus-exhaustion statement for the
frozen D0 only, not a claim that the literature universe is closed or that no later work can matter.

## Replay and coverage evidence

- D0 SHA-256: `afc3d85eab383f81c96d293b13d053767500baec485c89ce03aeff32f3425883`.
- Dataset-lock SHA-256: `1790b43c0c2c9ba8b1a3d1ce3d1588d3aa84e63f7d680cef78e20da7adf70c1f`.
- Prior handled union: 11,224 IDs, of which 11,125 are in D0 and 99 are outside; canonical SHA-256
  `18da767f90e3232cbf956f44fe7b51c833b126bbe71a8d2c879dd0c518422047`.
- Final sampler summary: 9,602 unique, round sizes
  `[1000,1000,1000,1000,1000,1000,1000,1000,1000,602]`, overlap 0,
  `remaining_unhandled_after_sampling=0`, summary SHA-256
  `545d2b802dc60c773cdadb4893bf58b4a6114a95b01def529f2e99cba545f52b`.
- Round SHA-256 values, in order: `1a190742…a6a4`, `0db96cd9…f63959`,
  `5208bfd9…5343`, `dc5798a1…0449`, `9f9215c0…45c5`, `0d276e5e…1576`,
  `ad208dab…da03`, `336ab4d4…6d0`, `63fd559e…136c`, `76fb8802…38b2`.
- Abstract policy stayed frozen at `sf-stage1b-abstract-policy-v6`. It produced 125
  `DEFER_REPRO_CHECK`, 9,477 `EXCLUDE_ABSTRACT`, and no direct full-text authorization. Human audit
  promoted 21 papers without changing the policy mid-run.

The earlier 9,503 remainder estimate was wrong because it treated all 224 targeted/registry IDs as
members of D0. The set replay proved that only 125 were in D0. The corrected denominator and the
new partial-tail test prevent this category error from recurring.

## Repository and binary-asset boundary

The ten repository receipts cover 843 paper-link URLs, normalized to 828 repositories; 211 passed
the strict structural gate (reachable, declared license, source, README and environment file).
Non-speech full-text promotions were limited to those verified repositories. This inspection did not
clone or execute repository code and is not a reproduction claim.

All 21 PDFs were downloaded by known arXiv ID and extracted page by page; all 21 retained e-print
sources were fetched only after consolidation. PDF/e-print/extracted text and repository receipts
remain under `SPEECHRL_DATA_DIR`. Git contains the fetch/analyze scripts, arXiv and repository links,
hashes, audit decisions and metadata-only registry records—not binary papers, datasets, models or
repository checkouts.

## Speech/omni findings and local-data fit

Ten retained papers are speech/omni-primary, but none is promoted to core.

- [TISDiSS](https://arxiv.org/abs/2509.15666) varies shared Reconstructor repetitions to expose an
  inference-depth curve on one trained speech-separation model. It is a direct acoustic controller,
  but WSJ0-2mix, Libri2Mix and WHAMR! are not in the local lock.
- [Phoenix-VAD](https://arxiv.org/abs/2509.20410) maps streaming speech to Continue/Stop actions.
  Its encoder is frozen, while the adapter and LLM are trained with LoRA on internal data; retain the
  stop policy, not a training-free end-to-end claim.
- [Counterfactual Activation Editing](https://arxiv.org/abs/2506.00832) edits TTS encoder states at
  inference for prosody/pronunciation correction, but relies on trained auxiliary components and
  non-local LJSpeech.
- [XAI-grounded speech-deepfake explanations](https://arxiv.org/abs/2606.16137) feed XAI evidence to
  a non-fine-tuned multimodal LLM. The detector/auxiliary MLP are trained and PartialSpoof is not local.
- [Cross-lingual dysarthria severity](https://arxiv.org/abs/2604.10123) yields an interpretable,
  training-free measure over frozen HuBERT. Local LibriSpeech can reproduce one healthy-control
  reference, but the clinical corpora and cross-corpus calibration are non-local.
- [VoxPrivacy](https://arxiv.org/abs/2601.19956) shows broad failures in speaker-conditioned and
  proactive privacy decisions; its core VoxPrivacy/AISHELL-2/WenetSpeech assets are not local.
- [SpeechRole](https://arxiv.org/abs/2508.02013) adds speech-to-speech interaction, expressiveness and
  role-fidelity evaluation; its new corpus is not local and repository licensing remains unresolved.
- [OpenOmni](https://arxiv.org/abs/2408.03047), [MiniMind-O](https://arxiv.org/abs/2605.03937) and
  [LiViBench](https://arxiv.org/abs/2601.15016) are retained as integration/model/omnimodal evaluation
  instruments. Their exact assets are not locally locked; OpenOmni's repository license is unresolved
  and LiViBench partly depends on proprietary construction models.

The only exact local occurrence in this batch is LibriSpeech as a healthy-control source for the
dysarthria measure; it does not make the pathological-speech task locally executable. Nine other
speech/omni papers require named assets absent from the lock or do not state an evaluation corpus.

## Open non-speech transfer findings

- [Patched MOA](https://arxiv.org/abs/2407.18521) provides open Best-of-N, mixture aggregation and
  MCTS around fixed target models; [OPTS](https://arxiv.org/abs/2503.01163) explicitly selects
  prompt-design strategies with bandits.
- [EET](https://arxiv.org/abs/2601.05777) turns retrieved experience, patch/test evidence and
  calibrated confidence into stop/continue/discard decisions. [Tool Attention](https://arxiv.org/abs/2604.21816)
  gates tool schemas from intent overlap and execution state.
- [ACING](https://arxiv.org/abs/2411.12736) trains an external actor-critic prompt controller while
  keeping the black-box target frozen; this is transferable outer-loop optimization, not a pure
  inference-only path.
- [Explain-Query-Test](https://arxiv.org/abs/2501.11721) contributes a self-evaluation signal.
  [Curie](https://arxiv.org/abs/2502.16069), [EnvBench](https://arxiv.org/abs/2503.14443),
  [EnvScaler](https://arxiv.org/abs/2601.05808) and [AutoResearchBench](https://arxiv.org/abs/2604.25256)
  supply open contracts for experiment execution, environment construction and literature-agent
  evaluation.
- [s1](https://arxiv.org/abs/2501.19393) is retained as negative boundary evidence: budget forcing is
  a runtime action, but the reported system first receives supervised fine-tuning on s1K.

## Durable artifacts and next boundary

- Batch-4 registry shard: `wiki/survey/registry/stage1b-bounded-batch4-exhaustive-2026-07-22-papers.jsonl`
  — 21 records, SHA-256 `16f1289f56c7f4414902ea66d0030fc19fe2d38021b0c5502e226029c8c4a0c7`.
- Exhaustive metadata view: `wiki/survey/registry/views/stage1b-bounded-exhaustive-2026-07-22.json`
  — 226 records, SHA-256 `8e3fcc5348afc4ff3425afac0da5fc6abb11aa33306fa74943c4d82ed4ed9e59`.
- Cross-batch external roster SHA-256:
  `28b4631c70596a0d72a3be3ad7a5ab9f7f13e1272f30e00d0f678e2745e3766b`.

Broad scanning now stops because the owner-requested frozen corpus is exhausted. This artifact does
not close Stage-1B by itself: T1/delta/citation limitations, mapping tables, eligible inputs and a
commit-bound release are handled by the later Stage-1B closeout package. Model loads, dataset metrics,
smoke tests, reproductions and prototypes remain outside this stage. H5 remains non-load-bearing
until independent coder B and third-party adjudication close.
