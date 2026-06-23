# Architecture

An **umbrella + shared library + four independent repos** model. Full version in the repo's
[`docs/architecture.md`](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/blob/master/docs/architecture.md);
this page is the quick view. The project's purpose is [[Project-Thesis]] — training-free RL to
activate pretrained knowledge; **W4** (omni-embedding speech disentanglement) is the flagship.

## Repo model

```
exploring-l4-intelligence (umbrella, this repo)
├─ common/        speechrl-common — shared library, editable-installed by each work
├─ projects/      the four work repos (each its OWN git repo; gitignored here)
├─ docs/          setup + architecture + data
├─ scripts/       WSL2 / env / mlflow / wiki-sync / data helpers
└─ wiki/          source for this Wiki (shared knowledge & memory)
```

The four works are **separate GitHub repos** (independent history/issues) but develop against one
shared `speechrl-common` via the `[tool.uv.sources]` editable path `../../common`.

| # | Repo | Role | Focus |
|---|------|------|-------|
| **W4** | `speech-mllm-omni-embedding-rl` | **Flagship** | training-free RL to disentangle a frozen omni model's embeddings (content/ASR+ST, speaker-ID, emotion/SER, language+intent) |
| **W1** | `speech-mllm-training-free-rl` | **Pattern reference** | mature training-free reward/eval machinery W4 reuses |
| W2 | `speech-mllm-efficient-rl-alignment` | Supporting | efficient GRPO/DPO (LoRA) for speech↔language alignment |
| W3 | `speech-mllm-multitask-rl` | Supporting | one policy, RL across ASR/ST/SID/SER via verifiable rewards |

## Shared library (`speechrl_common`)

| Module | Purpose |
|---|---|
| `audio` | load/resample (16 kHz mono, `io`), log-mel features (`features`) |
| `models` | Qwen2-Audio loader (`qwen2_audio`), per-task prompt templates (`prompts`) |
| `rl` | verifiable reward fns (WER / ASR / exact-match) usable as GRPO/TRL callables (`reward`) |
| `data` | dataset registry + data-root resolution (`registry`) |
| `tracking` | local-MLflow run helper (`mlflow_logger`) |
| `utils` | `seed`, `logging`, `checkpoint` path helpers |
| `configs` | `base.yaml` Hydra config the works compose on top of |

**Lazy-import discipline:** the top level imports only light helpers; torch/transformers/librosa/
mlflow/jiwer are imported *inside* the functions that use them, so `import speechrl_common` and its
smoke tests pass before the heavy ML stack is installed. Preserve this when adding code.

**Conventions:** Hydra config per work (`config.yaml` composes `model/ dataset/ rl/ experiment/`);
local MLflow file store (`~/speechrl-data/mlruns`, no server); verl (Linux-only, in WSL2) for
GRPO/PPO with vLLM rollouts; artifacts live in WSL ext4 `~/speechrl-data/`, never in git; base model
Qwen2-Audio, swappable to SALMONN / Qwen2.5-Omni via `models/` + config.

---

## 中文

一个**伞仓 + 共享库 + 四个独立仓库**的模型；完整版见仓库
[`docs/architecture.md`](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/blob/master/docs/architecture.md)。

四个工作是**独立的 GitHub 仓库**（独立历史与 issue），但都通过 `[tool.uv.sources]` 的可编辑路径
`../../common` 依赖同一个 `speechrl-common`（其模块见上方表格）。

**惰性导入纪律：** 包顶层只导入轻量 helper；torch / transformers / librosa / mlflow / jiwer 都在用到
它们的函数**内部**才导入，所以重 ML 栈装好之前 `import speechrl_common` 和它的 smoke test 就能通过。
加代码时请保持这一点。

**约定：** 配置用 Hydra（每个工作 `config.yaml` 组合 `model/ dataset/ rl/ experiment/`）；追踪用本地
MLflow 文件存储（`~/speechrl-data/mlruns`，无服务器）；RL 库 verl（仅 Linux，在 WSL2 跑）做 GRPO/PPO
+ vLLM rollout；产物在 WSL ext4 `~/speechrl-data/`，绝不进 git；基座模型默认 Qwen2-Audio，可通过
`models/` + config 换成 SALMONN / Qwen2.5-Omni。
