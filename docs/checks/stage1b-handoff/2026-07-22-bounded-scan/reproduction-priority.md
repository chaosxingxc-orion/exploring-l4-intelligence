# Provisional comparator worksheet — not Stage-frozen

**Status:** `PROVISIONAL_INPUT / NOT_STAGE_FROZEN`. This artifact records feasibility evidence for
possible later Stage-1C selection; it is not a selected problem, ranked reproduction list, frozen
reproduction card, or execution authorization.

**Scope:** evidence and environment construction only. No dependency installation, checkpoint
download, model load, inference, dataset example evaluation, WER computation, or prototype was run.

## Provisional feasibility sequence

The retained portfolio has no paper that simultaneously satisfies all three preferred properties:
`KEEP_CORE`, an exact local `TASK_MATCH` dataset, and a verified runnable repository. The first slice
would therefore use a comparator-first sequence if Stage-1C later selects an ASR problem. Stage-1C
may reject or replace this sequence.

1. Reproduction anchor: arXiv `2509.16622`, *Audio-Conditioned Diffusion LLMs for ASR and
   Deliberation Processing* (`KEEP_INSTRUMENT`). It has a paper-linked Apache-2.0 repository and an
   exact local LibriSpeech task match, but trains Q-Former/LoRA components and is not a training-free
   core method.
2. Core method to connect next: arXiv `2508.02228`, *Large Language Model Guided Decoding for
   Self-Supervised Speech Recognition* (`KEEP_CORE`). Its zero-shot decoding path is directly
   relevant, but the paper evaluates WSJ0, TED-LIUM 3, and ALLSSTAR using off-the-shelf wav2vec 2.0,
   HuBERT, GPT-2, Falcon, and LLaMA 2 artifacts that are not in the current local lock.
3. Minimal method baseline: arXiv `2212.13378`, confidence-relaxed ASR decoding on LibriSpeech.
4. Early falsifier: arXiv `2603.05231`, test-time RL for ASR robustness on LibriSpeech. It tests
   whether added online optimization is necessary, but remains negative/boundary evidence rather
   than a frozen-control prior.

## Provisional anchor worksheet: `2509.16622`

| Field | Frozen value |
|---|---|
| Upstream | `https://github.com/liuzhan22/Diffusion-ASR` |
| Commit | `18c8263d4c01c519931240d8e613a5413551c5cb` (detached external checkout) |
| License | Apache-2.0 |
| External source location | `$SPEECHRL_DATA_DIR/repos/stage1b/Diffusion-ASR` |
| Environment | `environment.yaml`; upstream Python 3.10, torch 2.7.1, transformers 4.53.2 |
| Entry points | `inference.py`, `calc_wer_json.py`, `configs/decode_config.yaml` |
| Required model artifacts | Whisper large-v3, LLaDA-8B-Instruct, paper checkpoint |
| Dataset | local locked LibriSpeech, `test.clean` and `test.other` |
| Metric | case-normalized WER; preserve insertion/deletion/substitution counts |
| Target claim | reproduce the paper's cascade deliberation result before adapting the control path |
| Expected artifacts | immutable input manifest, resolved config, predictions JSON, WER receipt, runtime receipt |
| Compute bound | define after checkpoint sizes and one-sample memory estimate; no estimate is asserted yet |
| Pass criterion | exact paper checkpoint and normalization contract reproduce within a pre-registered tolerance |
| Abort condition | stop before inference if checkpoint provenance, data conversion, dependency resolution, or output isolation is ambiguous |

The repository structurally contains 57 files (654,099 bytes in the pinned external checkout), an
environment manifest, inference code, config, metric script, and license. Its example annotations
expect individual audio paths and transcripts. The local ModelScope snapshot is Parquet, so a
read-only Parquet-to-example adapter or materialized external audio view is required; directly
pointing the upstream code at the dataset directory would be invalid.

## Targeted local data receipt

The full LibriSpeech snapshot contains 265 observed files and 123,675,394,690 bytes; no `.part`,
`.tmp`, or `.incomplete` files were observed. Only the first slice's two test Parquet files were
content-hashed:

| Split artifact | Bytes | SHA-256 |
|---|---:|---|
| `all/test.clean/0000.parquet` | 350,452,636 | `7113aa4c3cf963fb54697145719a7725f984c8836d1c494a554cbb9f1a017df0` |
| `all/test.other/0000.parquet` | 332,873,172 | `38e0c86a8104585c577badd707ca4331e20fa2c645f46180af0b7bcdecff9249` |

This receipt establishes byte identity only. Dataset schema, row counts, audio decoding, reference
normalization, and compatibility with the paper's example JSON remain behind the no-model data gate.
Parquet metadata inspection (without decoding an audio example) found 2,620 rows / 27 row groups for
`test.clean` and 2,939 rows / 30 row groups for `test.other`. Both expose the same seven fields:
`file`, `audio{bytes,path}`, `text`, `speaker_id`, `chapter_id`, and `id`. This is sufficient to
specify the adapter contract but not to claim sample-level validity.

## Next no-model gate

1. Parse only the two test Parquet schemas and row metadata; do not decode audio or score examples.
2. Specify a deterministic adapter from Parquet rows to the repository's `path`/`text` annotation
   contract, keeping converted audio and manifests outside Git.
3. Separate the paper environment from `~/.venvs/speechrl`; do not install its mixed CPU/CUDA and
   Python-3.10 lock into the shared Python-3.12 environment.
4. Resolve the file allowlist/bytes and paper-checkpoint hash gaps recorded in
   `candidate-model-lock.md`; do not promote that proposal to the canonical lock yet. Acquisition
   and model load need a separate authority decision.
5. Define a two-step experiment: one-sample memory/config smoke, then bounded `test.clean` WER. The
   smoke and metric remain unexecuted.

Another provisional feasibility set is omni/audio reasoning (`2605.25179`, `2510.05478`,
`2602.13685`) because MMAU-mini/MMAR/MMSU and Qwen3-Omni are local. No relative rank is assigned:
Stage-1C problem selection must precede any reproduction ordering, and paper-specific repositories
have not passed the current open-source gate.
