# Environment & Setup

The authoritative, step-by-step guide is the repo's
[`docs/setup.md`](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/blob/master/docs/setup.md).
This page is the orientation; follow `docs/setup.md` for exact commands.

**Why WSL2.** Compute is **WSL2 Ubuntu, not native Windows**: the RTX 5090 (Blackwell, sm_120) has
no stable native-Windows torch wheels, and verl/vLLM/flash-attn are Linux-only.

**The four phases**

1. **WSL2 + CUDA** — ensure a WSL2 (not WSL1) Ubuntu, then `bash scripts/wsl-setup.sh` (CUDA toolkit
   12.8+ for WSL + uv). Verify with `nvidia-smi` (lists the RTX 5090) and `nvcc --version` (12.8+).
2. **Python env + stack** — `bash scripts/env-setup.sh` builds the py3.12 uv venv at
   `~/.venvs/speechrl` (ext4), installs torch from the `cu128` index, then verl/vLLM and editable
   `common`. Activate with `source ~/.venvs/speechrl/bin/activate`.
3. **Work on a study** — `cd projects/<work> && uv pip install -e ../../common -e . && bash scripts/train.sh`.
4. **Tracking** — `bash scripts/mlflow-ui.sh` → http://127.0.0.1:5000 (local file store).

**Pitfalls.** System Python 3.14 is too new for ML wheels — never use it for the stack. If a "no
kernel image" CUDA error appears: torch nightly `cu128`, then a source build with
`TORCH_CUDA_ARCH_LIST=12.0`. verl/vLLM/flash-attn are version-sensitive — pin versions and prefer a
prebuilt `flash-attn` wheel for your torch/CUDA/Python combo. **Never touch `D:/ai-stack/mem0-venv`.**

**Research skills (Windows Claude Code session).** Curated marketplace set: `academic-research-skills`
+ six `ai-research-skills` groups (post-training, multimodal, fine-tuning, inference-serving,
optimization, mlops); K-Dense `scientific-agent-skills` intentionally skipped. Exact install commands
are in `docs/setup.md` §5.

---

## 中文

权威的逐步指南是仓库的
[`docs/setup.md`](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/blob/master/docs/setup.md)；
本页是导览，确切命令以 `docs/setup.md` 为准。

**为什么用 WSL2：** 算力在 **WSL2 Ubuntu，不在原生 Windows**——RTX 5090（Blackwell, sm_120）没有稳定
的原生 Windows torch 轮子，且 verl/vLLM/flash-attn 仅 Linux。

**四个阶段：**（1）WSL2 + CUDA：确保是 WSL2（非 WSL1）Ubuntu，跑 `bash scripts/wsl-setup.sh`，用
`nvidia-smi` / `nvcc --version` 验证。（2）Python 环境：`bash scripts/env-setup.sh` 建 py3.12 venv
（`~/.venvs/speechrl`，ext4），装 `cu128` 的 torch、verl/vLLM 和可编辑 `common`；`source` 激活。
（3）开发单个工作：`cd projects/<work> && uv pip install -e ../../common -e . && bash scripts/train.sh`。
（4）追踪：`bash scripts/mlflow-ui.sh`。

**坑：** 系统 Python 3.14 太新，别用于该栈；遇到 "no kernel image" 先 torch nightly `cu128`，再
`TORCH_CUDA_ARCH_LIST=12.0` 源码编译；verl/vLLM/flash-attn 版本敏感，建议锁版本并用预编译
`flash-attn` 轮子。**绝不动 `D:/ai-stack/mem0-venv`。**

**研究技能（在 Windows 的 Claude Code 会话里装）：** 精选 `academic-research-skills` + 六个
`ai-research-skills` 组；K-Dense `scientific-agent-skills` 有意不装。安装命令见 `docs/setup.md` 第 5 节。
