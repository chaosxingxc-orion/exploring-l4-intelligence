---
check_id: "SAEA-WHISPER-LARGE-V3-ACQUISITION-2026-09-06"
status: "PASS"
authority: "model acquisition, byte-closure verification and a CPU load smoke only; no audio, no transcription, no GPU"
---

# Tool-model acquisition receipt — Whisper large-v3 pinned and byte-closed

Date: 2026-09-06, on the owner's acquisition GO of the same day. This receipt closes acquisition
only. Umbrella `docs/datasets.lock.json` (entry `whisper-large-v3`) is the single live source of
asset identity; this file is the audit snapshot of how that entry was closed. **No corpus audio was
touched, no transcription was run, the GPU was never used, and the frozen Qwen3-Omni core was never
started.**

## 1. Why this model is in the catalog

The study's Earnings-22 tables currently sit beside numbers quoted out of other papers and out of
the Open ASR leaderboard. `SAEA-E22-DEV-WHISPER-ANCHOR-V1` replaces that quote with a number
measured on the study's own rows: whisper-large-v3 run as a TOOL model over the Earnings-22 dev
split under the leaderboard protocol (transformers inference; Whisper English text normalizer on
both reference and hypothesis), scored by the study's existing `asr-wer-whisper` scorer
(`asr-wer-whisper-v20240930`, vendored normalizer `whisper-english-v20240930`,
`src/speech_aware_evidence_acquisition/reproduction/asr_wer_whisper.py`). That yields an in-house
anchor on the study's exact rows instead of a cross-protocol comparison against a published figure.

Boundary: this is a frozen tool-level model. It is never a frozen-core component, never an
answering model, and never part of an OBS/ORG/SUPPLY/USE control path. Final answer authority
stays with the frozen Qwen3-Omni core. The anchor run itself is not authorized by this receipt —
it needs its own exposure-ledger row in the study repository before any result is read, and it is
measured on dev, never on a confirmatory split.

## 2. Lock registration (before any download)

Entry `whisper-large-v3` (kind `model`, lifecycle `AUXILIARY`, profile `speech-aware-tools`) was
written into `docs/datasets.lock.json` FIRST and only then fetched through the standard path. The
registration status was `MISSING`: the lock schema admits exactly `COMPLETE` / `PARTIAL` /
`MISSING` / `BLOCKED` (`scripts/data/asset_lock.py`, `ALLOWED_STATUS`, mirrored by the lock's own
`status_model`), and `MISSING` — "No governed local copy is present" — is the register-before-fetch
state this schema provides. Gates after registration and before any bytes moved:
`asset_lock.py validate` -> `OK 125 assets`; `test_asset_lock.py -v` -> 8/8 OK.

Identity verified live against the official `huggingface.co` model API BEFORE any download
(observed 2026-09-06):

| Field | Value |
|---|---|
| HF repo | `openai/whisper-large-v3` (`private: False`, `gated: False`) |
| Revision (API `sha`) | `06f233fe06e710322aca913c1bc4249a0d71fce1` (last modified 2024-08-12) |
| License | `apache-2.0` (`cardData.license`, and the `license:apache-2.0` tag) |
| Pipeline tag | `automatic-speech-recognition` |
| Files published at this revision | 21 |
| Files governed here | 11 (3,091,519,764 B) |

### What was selected, and what was deliberately left behind

Governed payload — the transformers-format fp16 weights plus everything
`WhisperForConditionalGeneration` and `WhisperProcessor` need:

| File | Bytes | Upstream identity checked |
|---|---:|---|
| `model.safetensors` | 3,087,130,976 | HF LFS oid (sha256) |
| `tokenizer.json` | 2,480,617 | Git blob SHA-1 |
| `vocab.json` | 1,036,558 | Git blob SHA-1 |
| `merges.txt` | 493,869 | Git blob SHA-1 |
| `tokenizer_config.json` | 282,843 | Git blob SHA-1 |
| `normalizer.json` | 52,666 | Git blob SHA-1 |
| `added_tokens.json` | 34,648 | Git blob SHA-1 |
| `generation_config.json` | 3,903 | Git blob SHA-1 |
| `special_tokens_map.json` | 2,072 | Git blob SHA-1 |
| `config.json` | 1,272 | Git blob SHA-1 |
| `preprocessor_config.json` | 340 | Git blob SHA-1 |

Not fetched (duplicate serializations of the same weights, about 21.6 GB avoided):
`pytorch_model.bin` (3,087,394,553 B), `flax_model.msgpack` (6,174,007,324 B),
`model.fp32-00001-of-00002.safetensors` + `model.fp32-00002-of-00002.safetensors`
(6,174,112,072 B), `pytorch_model.fp32-00001-of-00002.bin` +
`pytorch_model.fp32-00002-of-00002.bin` (6,174,402,576 B), and the two fp32 index files that only
address those shards. `.gitattributes` and `README.md` are repo furniture and were not governed.
The repo publishes **no** ONNX and **no** TFLite directory at this revision, so there was nothing
of that kind to exclude.

The acquired `normalizer.json` is the model-side English spelling map that ships with the
checkpoint. It is **not** the study's scoring normalizer: that stays the separately vendored,
read-only `reproduction/whisper_normalizer/` copy pinned at upstream tag `v20240930`.

## 3. Download and byte closure

- Channel: the umbrella's own path, `bash scripts/data/fetch-assets.sh data whisper-large-v3` ->
  `asset_lock.py fetch` -> `hf_complete.py` pinned-revision manifest + `aria2c`, official
  `https://huggingface.co` endpoint, one connection per file. No parallel or hand-rolled path.
- `hf_complete.py` independently resolved the revision to
  `06f233fe06e710322aca913c1bc4249a0d71fce1` and reported `total_files=11
  total_bytes=3091519764`, matching the registered entry exactly.
- One round; `missing=0` afterwards. Wall clock **1,425 s** (2026-09-06T17:15:54Z ->
  2026-09-06T17:39:39Z) for 3.09 GB, averaging about 2.1 MiB/s — the link, not the disk, was the
  limit.
- Landing: `$SPEECHRL_DATA_DIR/models/whisper-large-v3/` — the ONE working copy (3,091,521,536 B on
  disk including the `.hfd` manifest directory and the local receipt). No whisper checkpoint
  existed anywhere under the data root before this fetch, and the `hf_complete.py`/`aria2c` path
  never populates the Hugging Face hub cache, so no second copy was created.
- Byte closure, re-hashed locally after download (all 11 files):

| Check | Result |
|---|---|
| Files present | 11 / 11 |
| Size mismatches | 0 |
| `model.safetensors` sha256 vs HF LFS oid | match (`a8e94b85976e5864ba3e9525c7e6c83b2a1eca42d4b797a0c7c24d778e40fd95`) |
| Ten non-LFS files vs upstream Git blob SHA-1 | 10 / 10 match, byte for byte |
| Partial markers (`.aria2` / `.part` / `.incomplete`) | 0 |

`model.safetensors` is LFS-tracked, so its Git blob at the pinned revision is the ~130-byte pointer
file rather than the payload; the LFS oid is its upstream identity and that is what the lock pins.
Every other governed file is a plain Git blob, and reconstructing `sha1("blob <size>\0" + bytes)`
locally reproduces the exact blob id the repo tree reports at
`06f233fe06e710322aca913c1bc4249a0d71fce1`. All eleven sha256 values are recorded in the lock's
`source.files`.

- Machine check: `asset_lock.py inventory whisper-large-v3 --full --fail-on-drift` -> `COMPLETE`,
  `drift=0`, exit 0. Local receipt: `models/whisper-large-v3/.speechrl-asset.json` (revision field
  equals the pinned revision).

## 4. CPU load smoke — no audio

Run in the shared `~/.venvs/speechrl` with `CUDA_VISIBLE_DEVICES` empty, `HF_HUB_OFFLINE=1` and
`TRANSFORMERS_OFFLINE=1`, against the local directory only. **Nothing was installed or upgraded.**
The GPU was serving a study cell throughout (about 23.4 GB in use, 69 % utilisation at the start of
this work) and was never touched — `torch.cuda.is_available()` reported `False` inside the smoke.

| Observation | Value |
|---|---|
| Stack | transformers 5.12.1, torch 2.9.1+cu128 |
| `WhisperProcessor.from_pretrained` | OK, 0.4 s |
| Feature extractor | `WhisperFeatureExtractor`, 16 kHz, 128 mel bins, 30 s windows |
| Tokenizer | `WhisperTokenizer`, `vocab_size` 50,257, length 51,866 |
| `WhisperForConditionalGeneration.from_pretrained` | OK, 6.0 s (`dtype=float32`, `low_cpu_mem_usage=True`) |
| Placement | device `cpu`, dtype `torch.float32` |
| **Parameters** | **1,543,490,560** |
| Config | `d_model` 1280, 32 encoder layers, 32 decoder layers, 128 mel bins, `vocab_size` 51,866 |
| Generation config | alignment heads present, 100 language ids |

transformers 5.x takes `dtype=`; the smoke keeps a `torch_dtype=` fallback for older stacks and did
not need it. No audio array was constructed, no `generate` call was made, and no transcription was
produced.

## 5. Gates

Run from the umbrella after the entry was promoted to `COMPLETE` (all offline, all rc=0):

| Gate | Result |
|---|---|
| `bash scripts/data/inventory.sh` | `BLOCKED=11 COMPLETE=113 MISSING=0 PARTIAL=1 drift=0`; `whisper-large-v3 lock=COMPLETE observed=COMPLETE` |
| `python scripts/data/asset_lock.py validate` | `OK 125 assets` |
| `python scripts/data/test_asset_lock.py` | 8 tests, OK |
| `python scripts/checks/study_workspace_check.py` | `study workspace and experiment assets: PASS` |
| `python scripts/checks/legacy_asset_resolution_check.py --verify-bundles` | `PASS` (574 bindings, 0 unresolved, 4 bundle hashes verified) |
| `python scripts/checks/code_graph_check.py` | `PASS (24 trusted nodes)` |
| `python scripts/checks/paper_workspace_check.py` | `PASS (1 admitted)` |
| `python scripts/checks/ai_context_surface_check.py` | `PASS (0 failures)` |
| `python scripts/checks/build_ai_context_manifest.py --check` | `PASS` |

The single `PARTIAL` inventory row is `meetingbank`, which is pre-existing, consistent
(`lock=PARTIAL observed=PARTIAL`) and unrelated to this acquisition. Total catalog drift is 0.

## 6. Open item

The `speech-aware-tools` profile description in `docs/datasets.lock.json` still names only the
embedding models and was deliberately **not** edited here: another session holds an uncommitted
change on that exact line, and rewriting it would have entangled or silently overwritten that work.
The `whisper-large-v3` record therefore carries its own scope in its `research_role` and
`claim_limit` fields — a frozen tool-level ASR reference model, not the encode-only retriever the
profile blurb currently describes. The blurb should be widened the next time that line is touched
by whoever owns the pending change.

## 7. Boundary statement

Zero frozen-core contact: the Qwen3-Omni llama-server was never started. Zero corpus contact: no
Earnings-21/22, ConEC, SLURP, Audio2Tool, AMI or any other study audio or text was read, and no
audio of any kind reached this model — the smoke stops at construction and parameter counting. Zero
GPU use: the running study cell kept the device to itself. The shared `~/.venvs/speechrl` was not
modified; no `pip install` ran. Paid spend: 0. No other `docs/datasets.lock.json` entry was touched.
Any subsequent use of this model on study data — the `SAEA-E22-DEV-WHISPER-ANCHOR-V1` anchor run
itself — requires its own registered exposure-ledger row in the study repository before its result
is read.
