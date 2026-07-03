# Inference-Engine Choice — local Qwen3-Omni-30B on the 24 GB laptop GPU

> Decision record (2026-06-25 measured; 2026-07-03 written up). One-line verdict: **run the 30B
> omni model locally with llama.cpp (GGUF, partial offload); vLLM stays the RL-rollout / verl
> training engine of record for W2 — its Qwen3-Omni support is version-pairing work deferred until
> then.** This engine choice produced the W1 genuine best-of-N result (Decision-Log 2026-07-02).

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
deliberately avoided — lockfile source kind `hf-manual`). Working best-of-N runner:
`projects/speech-mllm-training-free-rl/scripts/repro_asr_best_of_n_llamacpp.py`.

## Per-task engine matrix

| Task | Engine | Status |
|---|---|---|
| Local 30B omni ASR + best-of-N (W1) | **llama.cpp** (resident `llama-server`) | ✅ proven — produced W1 `f9d111a` |
| W4 embedding backbone (`omni-embed-nemotron-3b`) | HF / sentence-transformers | ✅ unaffected by this decision |
| RL rollout + verl training (W2) | **vLLM** (engine of record) | ⏸ deferred — fix the transformers/vllm pairing when W2 starts |
| Post-fine-tune deployment | verl+vLLM train → `convert_hf_to_gguf.py` / `convert_lora_to_gguf.py` → llama.cpp | planned (merge path preferred) |

## LoRA deployment topology

Fine-tune with verl+vLLM (bitsandbytes 4-bit for QLoRA under 24 GB); then either **merge → GGUF**
(`convert_hf_to_gguf.py`, safest) or **adapter GGUF** (`convert_lora_to_gguf.py`) served by
llama.cpp. Both converters ship with the Phase-5 build.

---

## 中文

**一句话结论：本地跑 Qwen3-Omni-30B 用 llama.cpp（GGUF + `-ngl 28` 部分卸载）；vLLM 仍是 W2 RL
rollout / verl 训练的 engine of record，其 Qwen3-Omni 支持属版本配对工程、留到 W2 再解。** W1 的
真实 best-of-N 结果（Decision-Log 2026-07-02）正是这条路产出的。

**为什么不走 HF/vLLM int4（实测证据）：** HF `from_pretrained` 会把 int4 的 MoE 专家当缺失重新以
fp32 初始化（~58 GB，OOM，thinker-only 也不行）；vLLM 0.14.0 + transformers 5.12.1 在 engine 初始化
即崩（峰值显存仅 350 MiB，`Qwen2VLImageProcessor` 无 `max_pixels`）——是多模态处理器版本配对问题，
不是显存问题。探索性的 vLLM 脚本已于 2026-07-03 退役。

**可行路径：** Q8_0 30.3 GB > 24 GB 显存 → `-ngl 28` 部分卸载（MoE 3B 激活保持速度）；常驻
`llama-server` 约 4 分钟加载、每条生成约 2.8 秒；音频走 `/v1/chat/completions` 的 `input_audio`
（base64 wav）；greedy 即 temperature 0，采样用 temp>0 + 不同 seed。环境固化在 `env-setup.sh`
Phase 5；模型按文件取自 `fetch-qwen3-omni-gguf.sh`（lockfile 来源类型 `hf-manual`）。

**任务取舍：** 本地 30B 推理/best-of-N → llama.cpp（已验证）；W4 嵌入主干不受影响；W2 训练/rollout
→ vLLM（届时修版本配对）；微调后部署 → `convert_hf_to_gguf.py`（合并路，保险）或
`convert_lora_to_gguf.py`（adapter 路）→ llama.cpp。
