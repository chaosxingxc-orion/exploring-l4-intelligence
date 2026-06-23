# Data & models (not included in git)

Model weights and datasets are **deliberately kept out of this repository** (≈281 GB total).
GitHub only ever holds code, docs, and the download scripts. You fetch your own copy locally with
the scripts in [`scripts/data/`](../scripts/data). The `.gitignore` blocks `speechrl-data/` plus
all weight/dataset/archive formats, so a stray `git add -A` can never push data.

## Where it lives

`speechrl-data/` under the repo root by default, resolved as
`${SPEECHRL_DATA_DIR:-<repo>/speechrl-data}`. On WSL2 the preferred location is ext4
(`~/speechrl-data/`) to avoid NTFS overhead — point `SPEECHRL_DATA_DIR` there if you like.
Layout: `models/`, `datasets/`, `repos/` (reference clones), `manifests/`.

## Quick start

```bash
source ~/.venvs/speechrl/bin/activate     # the py3.12 venv (see setup.md)
bash scripts/data/probe-access.sh         # read-only: confirm HF/ModelScope reachability
bash scripts/data/fetch-data.sh           # download everything (skips already-complete assets)
bash scripts/data/inventory.sh            # audit COMPLETE / PARTIAL / MISSING per asset
```

Per-asset control uses the underlying engine
`projects/speech-mllm-training-free-rl/scripts/wave0_fetch.sh` (run `… help` for all targets):

```bash
cd projects/speech-mllm-training-free-rl
bash scripts/wave0_fetch.sh m_omni_embed_nemotron   # just the W4 omni-embedding model
bash scripts/wave0_fetch.sh d_librispeech            # just one dataset
```

China-mainland mirrors (hf-mirror.com + ModelScope) are the default (`SPEECHRL_CN_MIRROR=1`).
Force a source with `SPEECHRL_MODEL_SOURCE=hf|modelscope` / `SPEECHRL_DATASET_SOURCE=…`.

## Models

The **flagship (W4) backbone is `omni-embed-nemotron-3b`** — a *frozen* omni encoder whose embeddings
W4 disentangles via training-free RL (it is never fine-tuned). The generation models below are W1's
reward-guided-RL bases / comparators.

| Local dir | ModelScope | Hugging Face | Notes |
|---|---|---|---|
| `qwen3-omni-30b-a3b-instruct` | `Intel/Qwen3-Omni-30B-A3B-Instruct-int4-AutoRound` | `Qwen/Qwen3-Omni-30B-A3B-Instruct` | INT4 build for 24 GB VRAM |
| `moss-audio-8b-instruct` | `openmoss/MOSS-Audio-8B-Instruct` | `OpenMOSS-Team/MOSS-Audio-8B-Instruct` | ~16 GB |
| `nemotron3-nano-omni-nvfp4` | `nv-community/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-NVFP4` | `nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-NVFP4` | NVFP4 |
| `minicpm-o-4_5(-gguf)` | `OpenBMB/MiniCPM-o-4_5` | `openbmb/MiniCPM-o-4_5-gguf` | GGUF on HF |
| `baichuan-omni-1d5` | `baichuan-inc/Baichuan-Omni-1d5` | `baichuan-inc/Baichuan-Omni-1d5` | optional, ~7B |
| `kimi-audio-7b-instruct` | — | `moonshotai/Kimi-Audio-7B-Instruct` | optional, HF only |
| `omni-embed-nemotron-3b` | `nv-community/omni-embed-nemotron-3b` | `nvidia/omni-embed-nemotron-3b` | **W4 flagship backbone** (frozen) — SentenceTransformer, ~4.7B, dim 2048, cosine; built on the Qwen2.5-Omni Thinker; NVIDIA OneWay Noncommercial + Qwen Research (research/eval only) |

`scripts/data/fetch-data.sh` pulls the four default generation models plus the W4 omni-embedding
model (set `SPEECHRL_SKIP_OMNI_EMBED=1` to skip it); `baichuan-omni-1d5` / `kimi-audio-7b-instruct`
are run individually.

## Datasets

Notes column tags each dataset to the **W4 factor family** it exercises (content / speaker / emotion / language+intent).

| Local dir | Primary source | Notes (W4 factor family) |
|---|---|---|
| `librispeech` | `openslr/librispeech_asr` | content/ASR; tens of GB |
| `covost2` | `facebook/covost2` | content/ST (speech translation) |
| `fleurs` | `google/fleurs` | content/ST + language-ID (multilingual) |
| `voxceleb` | `juliuscn/voxceleb` (MS) | speaker-ID; gated on HF — **not yet downloaded** (placeholder only) |
| `meld` | `declare-lab/MELD` (HF) | emotion/SER; hf-mirror in CN mode |
| `crema-d` | `MahiA/CREMA-D` (HF) | emotion/SER + speaker-ID — **first-proof substrate** (speaker+emotion on the same audio) |
| `minds14` | `PolyAI/minds14` (HF) / `google/xtreme_s` (MS) | language+intent (SLU) |
| `slurp` | GitHub + Zenodo (aria2) | language+intent (SLU); audio via manifest |
| `mmau-mini` | `AudioLLMs/MMAU-mini` (HF) | audio understanding; hf-mirror in CN mode |
| `mmar` | `BoJack/MMAR` (HF) | audio reasoning; hf-mirror in CN mode |
| `air-bench` | `evalscope/AIR-Bench` (MS) | audio benchmark |

> **CREMA-D labels (gotcha):** use the *filename* emotion code (`{spk}_{sent}_{EMO}_{int}.wav`; 6
> balanced classes, ~1000 each) and the filename speaker prefix (91 speakers) as ground truth. The
> `classname` column in `train.csv`/`test.csv` is heavily neutral-skewed (~54%) and disagrees with the
> filename code in ~54% of rows — use the CSVs only for train/test split membership.

Optional eval sets via ModelScope `evalscope`: `Seed-TTS-Eval`, `aime24/25/26`, `GSM8K-V`, `MMStar`.

## Reference repos (`repos/`, code only)

`slurp`, `mbr-for-asr`, `AudioGenie-Reasoner`, `TTRL`, `TPO`, `JitRL`, `slue-toolkit`.

## Useful env knobs

`SPEECHRL_DATA_DIR`, `SPEECHRL_WORKSPACE`, `SPEECHRL_VENV`, `SPEECHRL_CN_MIRROR`,
`SPEECHRL_MODEL_SOURCE`, `SPEECHRL_DATASET_SOURCE`, `SPEECHRL_SKIP_EXISTING`,
`SPEECHRL_SKIP_SLURP_AUDIO`, `SPEECHRL_SKIP_OMNI_EMBED`, `SPEECHRL_MS_WORKERS`, `SPEECHRL_HFD_THREADS`.

> Historical per-campaign download drivers are preserved under
> [`scripts/data/campaigns/`](../scripts/data/campaigns) for reference; `fetch-data.sh` is the supported entry point.
