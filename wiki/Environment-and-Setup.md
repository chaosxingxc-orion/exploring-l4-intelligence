# Environment & Setup

The authoritative, step-by-step guide is the repo's
[`docs/setup.md`](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/blob/master/docs/setup.md).
This page is the orientation; follow `docs/setup.md` for exact commands.

**Why WSL2.** Compute is **WSL2 `Ubuntu-24.04`, not native Windows** (the default `Ubuntu` distro is WSL1 — no GPU;
always `wsl -d Ubuntu-24.04`): the RTX 5090 (Blackwell, sm_120) has
no stable native-Windows torch wheels, and verl/vLLM/flash-attn are Linux-only.

**The four phases**

1. **WSL2 + CUDA** — ensure a WSL2 (not WSL1) Ubuntu, then `bash scripts/wsl-setup.sh` (CUDA toolkit
   12.8+ for WSL + uv). Verify with `nvidia-smi` (lists the RTX 5090) and `nvcc --version` (12.8+).
2. **Python env + stack** — `bash scripts/env-setup.sh` builds the py3.12 uv venv at
   `~/.venvs/speechrl` (ext4), installs torch from the `cu128` index, then verl/vLLM and editable
   `common`. Activate with `source ~/.venvs/speechrl/bin/activate`.
3. **Work on a study** — `cd studies/<semantic-slug> && uv pip install -e ".[dev]" && pytest`;
   run commands are owned by the study repo (`../../common` is only a dev override for a study
   that has pinned that dependency; the current study declares none).
4. **Tracking** — local MLflow file store (`mlruns` on ext4); the Wiki experiment ledger pins run IDs.

**Pitfalls.** System Python 3.14 is too new for ML wheels — never use it for the stack. If a "no
kernel image" CUDA error appears: torch nightly `cu128`, then a source build with
`TORCH_CUDA_ARCH_LIST=12.0`. verl/vLLM/flash-attn are version-sensitive — pin versions and prefer a
prebuilt `flash-attn` wheel for your torch/CUDA/Python combo. **Never touch `D:/ai-stack/mem0-venv`.**

**Research skills (Windows Claude Code session).** Curated marketplace set: `academic-research-skills`
+ six `ai-research-skills` groups (post-training, multimodal, fine-tuning, inference-serving,
optimization, mlops); K-Dense `scientific-agent-skills` intentionally skipped. Exact install commands
are in `docs/setup.md` §5.
