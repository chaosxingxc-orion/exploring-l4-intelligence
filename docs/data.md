# Data & models (not included in git)

Model weights and datasets are **deliberately kept out of this repository** (~410 GB total on disk).
GitHub only ever holds code, docs, and the download scripts. The dataset set is now **FROZEN** to the
local snapshot recorded in [`datasets.lock.json`](datasets.lock.json) (see *Frozen set* below) — we no
longer download new datasets. The `.gitignore` blocks `speechrl-data/` plus all weight/dataset/archive
formats, so a stray `git add -A` can never push data.

## Where it lives

`speechrl-data/` under the repo root by default, resolved as
`${SPEECHRL_DATA_DIR:-<repo>/speechrl-data}`. On WSL2 ext4 (`~/speechrl-data/`) is preferred to avoid
NTFS overhead — point `SPEECHRL_DATA_DIR` there if you like. Layout: `models/`, `datasets/`, `repos/`
(reference clones; SLURP audio lives here too), `manifests/`.

## Frozen set & unified downloader

[`datasets.lock.json`](datasets.lock.json) is the **single manifest** and source of truth. Per asset it
records the local subdir, source id, **pinned revision** (the HF or git commit sha where the local
snapshot recorded one; ModelScope tracks `master`; metadata-less entries are content-fingerprinted by
`size_bytes` + `files`), size, and status. The set is **FROZEN**: `scripts/data/fetch-data.sh` is a
self-contained, lockfile-driven downloader that fetches *exactly* this set and nothing else, so every
collaborating team reproduces identical data. HF datasets pull the recorded commit (cross-team
reproducible); the W1 `wave0_fetch.sh` engine was retired in favour of this one script.

```bash
# 0) one-time: install the download deps if missing (see Dependencies below)
bash scripts/data/fetch-data.sh --list         # show the manifest, fetch nothing
bash scripts/data/fetch-data.sh                 # fetch everything missing (skips complete assets)
bash scripts/data/fetch-data.sh meld slurp      # fetch only named assets
bash scripts/data/fetch-data.sh --dry-run       # print the commands without downloading
bash scripts/data/inventory.sh                  # audit the on-disk snapshot vs the lock
```

China-mainland mirrors (hf-mirror.com + ModelScope) are the default. To **change** the set, regenerate
the lockfile + update the registry, then re-fetch — it is never an accident.

### Dependencies

The downloader needs `python3`, `git`, `curl`, **`aria2c`**, and **`modelscope`** (`jq` optional, speeds
up `hfd`). HF datasets are fetched via hf-mirror's `hfd`+`aria2c` (auto-downloaded), because the Python
`hf` CLI rejects hf-mirror's HEAD metadata — so `aria2c` is required for HF in CN; the `hf` CLI is only a
fallback (direct huggingface.co). The downloader preflight-checks and, if anything's missing, points to:

```bash
bash scripts/env-setup.sh                       # full stack (torch/verl + download deps); creates the venv
bash scripts/data/fetch-data.sh --install-deps  # lightweight: download deps only (modelscope, aria2, jq, hf), no torch
```

## Models (5 local, ~90 GB)

The **flagship (W4) backbone is `omni-embed-nemotron-3b`** — a *frozen* omni encoder whose embeddings
W4 disentangles via training-free RL (never fine-tuned). The generation models are W1's
reward-guided-RL bases / comparators.

| Local dir | Size | Source (ModelScope / HF) | Role |
|---|---|---|---|
| `qwen3-omni-30b-a3b-instruct` | 24.5G | `Intel/Qwen3-Omni-30B-A3B-Instruct-int4-AutoRound` / `Qwen/Qwen3-Omni-30B-A3B-Instruct` | INT4 generation base (W1) |
| `nemotron3-nano-omni-nvfp4` | 20.9G | `nv-community/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-NVFP4` / `nvidia/…-NVFP4` | NVFP4 generation base (W1) |
| `minicpm-o-4_5` | 18.7G | `OpenBMB/MiniCPM-o-4_5` / `openbmb/MiniCPM-o-4_5-gguf` | generation comparator (W1) |
| `moss-audio-8b-instruct` | 16.9G | `openmoss/MOSS-Audio-8B-Instruct` / `OpenMOSS-Team/MOSS-Audio-8B-Instruct` | generation comparator (W1) |
| `omni-embed-nemotron-3b` | 8.8G | `nv-community/omni-embed-nemotron-3b` / `nvidia/omni-embed-nemotron-3b` | **W4 flagship backbone** (frozen) — SentenceTransformer, ~4.7B, dim 2048, cosine; NVIDIA OneWay Noncommercial + Qwen Research (research/eval only) |

> Not in the frozen set: optional `baichuan-omni-1d5` / `kimi-audio-7b-instruct` were never downloaded.
> A stale `minicpm-o-4_5-gguf` symlink (pointed outside `speechrl-data/`) was removed — use `minicpm-o-4_5`.

## Datasets (28 locked, ~320 GB)

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
The downloader fetches only what the lockfile records, so there is no separate freeze toggle.
