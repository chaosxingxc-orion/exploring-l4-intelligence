# Inference-Engine Choice — local Qwen3-Omni-30B on the 24 GB laptop GPU

> Decision record (2026-06-25 measured; 2026-07-03 written up). One-line verdict: **run the 30B
> omni model locally with llama.cpp (GGUF, partial offload); vLLM's Qwen3-Omni support is
> version-pairing work, deferred indefinitely now that the program is zero-parameter-training on a
> frozen core.** This engine choice produced the genuine best-of-N result of the retired W1 work
> (Decision-Log 2026-07-02) and remains the serving path for the admitted study.

## Measured environment (2026-06-25, this machine)

| Item | Measured |
|---|---|
| GPU | RTX 5090 Laptop, **24 GB** VRAM (Blackwell, sm_120) |
| WSL | `Ubuntu-24.04` (WSL2) — the default `Ubuntu` distro is WSL1, no GPU |
| CUDA | 12.8 + 13.0 installed; **pin nvcc 12.8** to match torch `cu128` |
| Stack | torch 2.9.1+cu128 · transformers 5.12.1 · vllm 0.14.0 · verl 0.8.0 · peft 0.19.1 · bitsandbytes 0.49.2 |
| RAM / disk | 54 GB RAM · ext4 ~870 GB free |
| Model on disk | int4 AutoRound HF dir 24.5 GB (`models/qwen3-omni-30b-a3b-instruct`) + **GGUF Q8_0 30.3 GB + bf16 mmproj 2.1 GB** (`models/qwen3-omni-30b-a3b-instruct-gguf`) |

## Why not the HF / vLLM int4 path (measured failures, not guesses)

- **HF `from_pretrained` on the int4 AutoRound dir does not fit.** Vanilla transformers loads the
  MoE experts as MISSING and re-initializes them in **fp32 → ~58 GB → OOM**, even thinker-only.
- **vLLM 0.14.0 + transformers 5.12.1 cannot initialize Qwen3-Omni at all.** Crash is in engine
  init *before any weight reaches the GPU* (peak 350 MiB):
  `AttributeError: 'Qwen2VLImageProcessor' object has no attribute 'max_pixels'` — the image
  processor is built even with `limit_mm_per_prompt image=0`. Root cause is multimodal-processor
  **version pairing**, not VRAM. Log: `/home/chao/vllm_int4_fit_test.log`.
- Sibling generative models hit the same wall offline: `moss-audio-8b` (custom processor `.py`
  missing), `minicpm-o-4_5` (driver hardcodes the Qwen3-Omni arch).
- The exploratory vLLM runner (`repro_asr_best_of_n_vllm.py`) was retired 2026-07-03 for this reason.

## The working path: llama.cpp GGUF (audio via mtmd)

Q8_0 (30.3 GB) > 24 GB VRAM, so **partial offload `-ngl 28`** (remaining layers + experts on CPU;
the MoE's 3B-active keeps it fast). Measured: **~4 min load (resident server), ~2.8 s/generation**.
llama.cpp audio input is flagged *experimental* upstream ("may have reduced quality") — acceptable;
the W1 multi-seed best-of-N artifact was produced exactly this way.

```bash
# Resident server (use for best-of-N loops — load once, sample many)
~/llama.cpp/build/bin/llama-server \
  -m  $SPEECHRL_DATA_DIR/models/qwen3-omni-30b-a3b-instruct-gguf/Qwen3-Omni-30B-A3B-Instruct-Q8_0.gguf \
  --mmproj $SPEECHRL_DATA_DIR/models/qwen3-omni-30b-a3b-instruct-gguf/mmproj-Qwen3-Omni-30B-A3B-Instruct-bf16.gguf \
  -ngl 28 -c 8192 --host 127.0.0.1 --port 8091
# POST /v1/chat/completions with an `input_audio` content part (base64 wav).
# Greedy = temperature 0; sample N with temperature>0 + varying seed.

# One-off CLI probe
~/llama.cpp/build/bin/llama-mtmd-cli -m <Q8_0.gguf> --mmproj <mmproj.gguf> \
  -ngl 28 -c 4096 --audio utt.wav -p "Transcribe the English speech. Output only the transcript."
```

Provisioning is codified: `scripts/env-setup.sh` **Phase 5** builds llama.cpp (CUDA 12.8, sm_120);
`scripts/data/fetch-qwen3-omni-gguf.sh` fetches exactly the two GGUF files (whole-repo pull >110 GB
deliberately avoided — lockfile source kind `hf-manual`). Reference best-of-N runners (rescued from
the retired W1 work):
`studies/speech-aware-evidence-acquisition/reference/w1-snapshot/baselines/repro_asr_best_of_n_v2.py`
(includes the proven prompt-cache livelock fix bundle) and `repro_asr_best_of_n_llamacpp.py`.

## Per-task engine matrix

| Task | Engine | Status |
|---|---|---|
| Local 30B omni ASR + best-of-N / frozen-core serving | **llama.cpp** (resident `llama-server`) | ✅ proven (historical W1 `f9d111a`); current study serving path |
| Embedding backbones (e.g. `omni-embed-nemotron-3b`) | HF / sentence-transformers | ✅ unaffected by this decision |
| vLLM serving of Qwen3-Omni | vLLM | ⏸ deferred indefinitely — version-pairing work; no training workload exists under the zero-parameter-training program line |

Historical note: the former verl/vLLM fine-tune and LoRA-deployment plans belonged to the retired
W2-era framing; the admitted program line trains no model parameters, so they are recorded only in
Git history.
