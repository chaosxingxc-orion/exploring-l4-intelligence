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

| Local dir | ModelScope | Hugging Face | Notes |
|---|---|---|---|
| `qwen3-omni-30b-a3b-instruct` | `Intel/Qwen3-Omni-30B-A3B-Instruct-int4-AutoRound` | `Qwen/Qwen3-Omni-30B-A3B-Instruct` | INT4 build for 24 GB VRAM |
| `moss-audio-8b-instruct` | `openmoss/MOSS-Audio-8B-Instruct` | `OpenMOSS-Team/MOSS-Audio-8B-Instruct` | ~16 GB |
| `nemotron3-nano-omni-nvfp4` | `nv-community/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-NVFP4` | `nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-NVFP4` | NVFP4 |
| `minicpm-o-4_5(-gguf)` | `OpenBMB/MiniCPM-o-4_5` | `openbmb/MiniCPM-o-4_5-gguf` | GGUF on HF |
| `baichuan-omni-1d5` | `baichuan-inc/Baichuan-Omni-1d5` | `baichuan-inc/Baichuan-Omni-1d5` | optional, ~7B |
| `kimi-audio-7b-instruct` | — | `moonshotai/Kimi-Audio-7B-Instruct` | optional, HF only |
| `omni-embed-nemotron-3b` | `nv-community/omni-embed-nemotron-3b` | `nvidia/omni-embed-nemotron-3b` | **W4** omni-embedding, ~4.7B, dim 2048; NVIDIA OneWay Noncommercial |

`scripts/data/fetch-data.sh` pulls the four default generation models plus the W4 omni-embedding
model (set `SPEECHRL_SKIP_OMNI_EMBED=1` to skip it); `baichuan-omni-1d5` / `kimi-audio-7b-instruct`
are run individually.

## Datasets

| Local dir | Primary source | Notes |
|---|---|---|
| `librispeech` | `openslr/librispeech_asr` | ASR; tens of GB |
| `mmau-mini` | `AudioLLMs/MMAU-mini` (HF) | hf-mirror in CN mode |
| `mmar` | `BoJack/MMAR` (HF) | hf-mirror in CN mode |
| `meld` | `declare-lab/MELD` (HF) | emotion |
| `crema-d` | `MahiA/CREMA-D` (HF) | emotion |
| `minds14` | `PolyAI/minds14` (HF) / `google/xtreme_s` (MS) | intent |
| `covost2` | `facebook/covost2` | ST |
| `fleurs` | `google/fleurs` | multilingual |
| `voxceleb` | `juliuscn/voxceleb` (MS) | gated on HF |
| `air-bench` | `evalscope/AIR-Bench` (MS) | audio benchmark |
| `slurp` | GitHub + Zenodo (aria2) | audio via manifest |

Optional eval sets via ModelScope `evalscope`: `Seed-TTS-Eval`, `aime24/25/26`, `GSM8K-V`, `MMStar`.

## Reference repos (`repos/`, code only)

`slurp`, `mbr-for-asr`, `AudioGenie-Reasoner`, `TTRL`, `TPO`, `JitRL`, `slue-toolkit`.

## Useful env knobs

`SPEECHRL_DATA_DIR`, `SPEECHRL_WORKSPACE`, `SPEECHRL_VENV`, `SPEECHRL_CN_MIRROR`,
`SPEECHRL_MODEL_SOURCE`, `SPEECHRL_DATASET_SOURCE`, `SPEECHRL_SKIP_EXISTING`,
`SPEECHRL_SKIP_SLURP_AUDIO`, `SPEECHRL_SKIP_OMNI_EMBED`, `SPEECHRL_MS_WORKERS`, `SPEECHRL_HFD_THREADS`.

> Historical per-campaign download drivers are preserved under
> [`scripts/data/campaigns/`](../scripts/data/campaigns) for reference; `fetch-data.sh` is the supported entry point.
