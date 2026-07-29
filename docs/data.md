# Data & models (not included in git)

Model weights and datasets are **deliberately kept out of this repository**. GitHub holds only code,
source URLs, immutable revisions/content fingerprints, documentation and download/check scripts.
[`datasets.lock.json`](datasets.lock.json) is the reproducible `FROZEN_BASELINE`; later local assets
are tracked separately as `LOCAL_CANDIDATE_UNFROZEN`, and survey/reproduction material is
`SURVEY_AND_REPRO_AUXILIARY`. The layered inventory is
[`speechrl-data-layered-inventory.json`](checks/stage1b-closeout/2026-07-22-v4/speechrl-data-layered-inventory.json).

## Where it lives

`speechrl-data/` on the **E: drive** — `/mnt/e/chao_workspace/exploring-l4-intelligence/speechrl-data`
from WSL (moved off D: on 2026-07-09). Reached via `${SPEECHRL_DATA_DIR:-<repo>/speechrl-data}`;
`SPEECHRL_DATA_DIR` is persisted in the WSL `~/.bashrc` to point at the E: path (the repo-relative
`<repo>/speechrl-data` fallback no longer holds the data). ext4 `~/speechrl-data/` holds only the MLflow store
(`mlruns`). Layout: `models/`, `datasets/`, `repos/`
(reference clones; SLURP audio lives here too), `manifests/`.

## Frozen baseline, candidate acquisition and inventory

[`datasets.lock.json`](datasets.lock.json) is the baseline manifest, not a complete statement about
the current disk. Per baseline asset it
records the local subdir, source id, **pinned revision** (the HF or git commit sha where the local
snapshot recorded one; ModelScope tracks `master`; metadata-less entries are content-fingerprinted by
`size_bytes` + `files`), size, and status. The set is **FROZEN**: `scripts/data/fetch-data.sh` is a
self-contained, lockfile-driven downloader that fetches *exactly* this baseline and nothing else, so every
collaborating team reproduces identical data. HF datasets pull the recorded commit (cross-team
reproducible); the W1 `wave0_fetch.sh` engine was retired in favour of this one script.

`fetch-data.sh`, `fetch-candidates.sh`, `fetch-qwen3-omni-gguf.sh`,
`fetch-stage1c-priority-papers.sh` and `inventory.sh` are 2-3 line delegating shims (2026-07-29) to
[`scripts/data/fetch-assets.sh`](../scripts/data/fetch-assets.sh) — a single subcommand-dispatch
engine (`fetch-assets.sh <data|candidates|qwen3-gguf|papers|inventory> [args…]`) that carries each
former script's fetch logic verbatim (same manifest, same target paths, same flags) plus a small
shared library of env/venv lines that were byte-identical across two or more of them. The shims'
CLI, this doc's commands below, and the `datasets.lock.json` schema are all unchanged by that
merge; see [`scripts/data/README.md`](../scripts/data/README.md) for the engine/shim layout and the
pre-existing per-script behavioral inconsistencies it preserves as-is.

```bash
# 0) one-time: install the download deps if missing (see Dependencies below)
bash scripts/data/fetch-data.sh --list         # show the manifest, fetch nothing
bash scripts/data/fetch-data.sh                 # fetch everything missing (skips complete assets)
bash scripts/data/fetch-data.sh meld slurp      # fetch only named assets
bash scripts/data/fetch-data.sh --dry-run       # print the commands without downloading
bash scripts/data/inventory.sh                  # audit the on-disk snapshot vs the lock
bash scripts/data/fetch-candidates.sh --list   # list non-baseline public candidates
bash scripts/data/fetch-candidates.sh NAME     # revision/size-verified candidate download
```

China-mainland mirrors (hf-mirror.com + ModelScope) are the default. Candidate acquisition does not
silently mutate the frozen baseline. Promote a candidate only through an explicit future baseline
release; until then its exact status is recorded in the Stage-1C acquisition matrix.

### Dependencies

The downloader needs `python3`, `git`, `curl`, **`aria2c`**, and **`modelscope`** (`jq` optional, speeds
up `hfd`). HF datasets are fetched via hf-mirror's `hfd`+`aria2c` (auto-downloaded), because the Python
`hf` CLI rejects hf-mirror's HEAD metadata — so `aria2c` is required for HF in CN; the `hf` CLI is only a
fallback (direct huggingface.co). The downloader preflight-checks and, if anything's missing, points to:

```bash
bash scripts/env-setup.sh                       # full stack (torch/verl + download deps); creates the venv
bash scripts/data/fetch-data.sh --install-deps  # lightweight: download deps only (modelscope, aria2, jq, hf), no torch
```

## Models: current routing

The frozen baseline contains exactly three model directories:
`qwen3-omni-30b-a3b-instruct-gguf`, `nemotron3-nano-omni-nvfp4`, and
`omni-embed-nemotron-3b`. The other observed model directories are
`LOCAL_CANDIDATE_UNFROZEN`; their presence does not expand the baseline or authorize execution. Use
the layered inventory for current counts, bytes and provenance status.

### Superseded historical roster (do not use as current inventory)

The **flagship (W4) backbone is `omni-embed-nemotron-3b`** — a *frozen* omni encoder whose embeddings
W4 disentangles via training-free RL (never fine-tuned). The generation models are W1's
reward-guided-RL bases / comparators.

| Local dir | Size | Source (ModelScope / HF) | Role |
|---|---|---|---|
| `qwen3-omni-30b-a3b-instruct` | 24.5G | `Intel/Qwen3-Omni-30B-A3B-Instruct-int4-AutoRound` / `Qwen/Qwen3-Omni-30B-A3B-Instruct` | INT4 generation base (W1) |
| `qwen3-omni-30b-a3b-instruct-gguf` | 32.3G | `ggml-org/Qwen3-Omni-30B-A3B-Instruct-GGUF` (Q8_0 + bf16 mmproj only — `scripts/data/fetch-qwen3-omni-gguf.sh`) | **llama.cpp engine for W1's genuine best-of-N** (30B on 24 GB via `-ngl 28`; the vLLM/HF int4 path does not load — see wiki/Inference-Engine-Choice.md) |
| `nemotron3-nano-omni-nvfp4` | 20.9G | `nv-community/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-NVFP4` / `nvidia/…-NVFP4` | NVFP4 generation base (W1) |
| `minicpm-o-4_5` | 18.7G | `OpenBMB/MiniCPM-o-4_5` / `openbmb/MiniCPM-o-4_5-gguf` | generation comparator (W1) |
| `moss-audio-8b-instruct` | 16.9G | `openmoss/MOSS-Audio-8B-Instruct` / `OpenMOSS-Team/MOSS-Audio-8B-Instruct` | generation comparator (W1) |
| `omni-embed-nemotron-3b` | 8.8G | `nv-community/omni-embed-nemotron-3b` / `nvidia/omni-embed-nemotron-3b` | **W4 flagship backbone** (frozen) — SentenceTransformer, ~4.7B, dim 2048, cosine; NVIDIA OneWay Noncommercial + Qwen Research (research/eval only) |

> Not in the frozen set: optional `baichuan-omni-1d5` / `kimi-audio-7b-instruct` were never downloaded.
> A stale `minicpm-o-4_5-gguf` symlink (pointed outside `speechrl-data/`) was removed — use `minicpm-o-4_5`.

## Datasets (28-entry frozen baseline)

Grouped by the **W4 factor family** / eval role each exercises. Exact sizes, sources, and pinned
revisions are in [`datasets.lock.json`](datasets.lock.json).

### Content — ASR / ST
| Local dir | Size | Source | Notes |
|---|---|---|---|
| `librispeech` | 115G | ModelScope (`master`) | content/ASR; 100h+360h+960h |
| `fleurs-r` | 17G | HF `google/fleurs-r` | FLEURS-R (restored speech); ST + language-ID. *Was `fleurs` in old docs.* |
| `covost2` | 283M | HF `facebook/covost2` | content/ST translations (audio comes from Common Voice) |

### Speaker + Emotion — SER / SID
| Local dir | Size | Source | Notes |
|---|---|---|---|
| `crema-d` | 578M | HF `MahiA/CREMA-D` | emotion/SER **+ speaker-ID** — first-proof substrate (both on the same audio) |
| `meld` | 32G | HF `declare-lab/MELD` | emotion/SER (raw + features) |

> **CREMA-D labels (gotcha):** use the *filename* emotion code (`{spk}_{sent}_{EMO}_{int}.wav`; 6
> balanced classes) and the filename speaker prefix (91 speakers) as ground truth. The `classname`
> column in `train.csv`/`test.csv` is neutral-skewed (~54%) and disagrees with the filename code in
> ~54% of rows — use the CSVs only for train/test split membership.
>
> Speaker-ID note: VoxCeleb (gated, only ever a placeholder) was deleted; speaker identity is exercised
> via CREMA-D.

### Language + Intent — SLU
| Local dir | Size | Source | Notes |
|---|---|---|---|
| `speech-massive` | 30G | HF `FBK-MT/Speech-MASSIVE` | 12-lang SLU intent+slot (CC-BY-NC, eval-only) |
| `slurp` | 13G | git + Zenodo `4274930` | English SLU; **audio at `repos/slurp/scripts/audio/{slurp_real,slurp_synth}`**, transcripts in `repos/slurp/dataset` (`datasets/slurp` symlink created on setup) |
| `minds14` | 1.1G | HF `PolyAI/minds14` | language+intent (SLU), 14 langs |

### Audio understanding / reasoning / benchmark
| Local dir | Size | Source | Notes |
|---|---|---|---|
| `air-bench` | 41G | ModelScope (`master`) | AIR-Bench audio benchmark |
| `mmar` | 2.8G | HF `BoJack/MMAR` | audio reasoning |
| `mmau-mini` | 2.6G | HF `TwinkStart/MMAU` | audio understanding |
| `mmsu` | 1.6G | HF `ddwang2000/MMSU` | multi-skill spoken-reasoning MCQ |
| `big-bench-audio` | 305M | HF `ArtificialAnalysis/big_bench_audio` | spoken reasoning, 1000 items |

### Spoken QA / dialogue / assistant / agent (eval suite)
| Local dir | Size | Source | Notes |
|---|---|---|---|
| `heysquad` | 14G | HF `yijingwu/HeySQuAD_human` | extractive spoken-QA |
| `uro-bench` | 11G | HF `Honggao/URO-Bench` | EN+ZH spoken-dialogue agentic |
| `voicebench` | 10G | ModelScope (`master`) | spoken-QA + agentic suite |
| `voiceassistant-eval` | 8.8G | HF `MathLLMs/VoiceAssistant-Eval` | 13-cat assistant eval (roleplay/safety/S2S) |
| `audiomc` | 4.9G | HF `ScaleAI/audiomc` | multi-turn instruction retention |
| `vocalbench` | 4.6G | HF `VocalNet/VocalBench` | 9-axis conversational eval |
| `vocalbench-zh` | 3.7G | HF `VocalNet/VocalBench-zh` | Mandarin spoken-interaction |
| `spoken-squad` | 3.2G | HF `AudioLLMs/spoken_squad_test` | ASR-noise-robust spoken QA |
| `soulx-duplug` | 317M | HF `Soul-AILab/SoulX-Duplug-Eval` | full-duplex turn-taking EN+ZH (zips) |
| `tau2-bench` | 25M | ModelScope (`master`) | voice tool-use agent data |
| `eva-bench` | 257K | HF `ServiceNow-AI/eva` | voice-agent task+experience (airline); tiny by design |

### TTS / reasoning evals
| Local dir | Size | Source | Notes |
|---|---|---|---|
| `seed-tts-eval` | 357M | ModelScope (`master`) | Seed-TTS eval set |
| `aime24` / `aime25` / `aime26` | <40K each | ModelScope (`master`) | AIME math-reasoning eval sets |

## Reference repos (`repos/`, code only — pinned in lockfile)

`slurp`, `mbr-for-asr`, `AudioGenie-Reasoner`, `TTRL`, `TPO`, `JitRL`, `slue-toolkit` — each pinned to a
commit sha in [`datasets.lock.json`](datasets.lock.json).

## Useful env knobs

`SPEECHRL_DATA_DIR`, `SPEECHRL_WORKSPACE`, `SPEECHRL_VENV`, `SPEECHRL_LOCKFILE` (manifest path),
`SPEECHRL_HF_ENDPOINT` (default hf-mirror.com), `SPEECHRL_MS_WORKERS`, `SPEECHRL_PYTHON`.
`fetch-data.sh` fetches only the frozen baseline. `fetch-candidates.sh` is an explicit, separately
verified acquisition path and never edits the baseline lock automatically.
