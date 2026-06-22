# L4 级智能探索

> [English](README.md) | **中文**
>
> 仓库标识：**`exploring-l4-intelligence`** — 探索迈向 L4 级（"创新者"）智能的路径。

这是一个**伞仓（umbrella repo）**：研究如何用**免训练 RL（training-free RL）**——奖励引导、推理时、
不改权重也不改结构的优化——把语音 / omni 多模态大模型在预训练中习得的知识「激活」出来，提升其在特定
语音任务上的开箱表现；外加四个工作共用的共享库。旗舰工作（W4）以此**解耦冻结 omni 模型的语音嵌入**。
完整主旨见 Wiki 的 [[Project-Thesis]] 页。

> 📖 **从这里开始。** 本 README 是人和 AI 协作者的**唯一权威入口**。更深入的文档在 [`docs/`](docs)；
> 团队共享知识与"记忆"在 **[GitHub Wiki](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/wiki)**
>（源文件在 [`wiki/`](wiki)）。

## 四部曲 · The series

每个工作都是**独立的 GitHub 仓库**（独立的历史与 issue），但都通过可编辑安装（editable install）
依赖同一个 [`common/`](common)（`speechrl-common`）。

| # | 工作（仓库） | 角色 | 方向 | 状态 |
|---|---|---|---|---|
| **W4** | [speech-mllm-omni-embedding-rl](https://github.com/chaosxingxc-orion/speech-mllm-omni-embedding-rl) | **旗舰** | 免训练 RL 解耦冻结 omni 模型的嵌入（内容/ASR+ST、说话人、情感/SER、语言+意图） | 🟡 骨架 → 进行中 |
| **W1** | [speech-mllm-training-free-rl](https://github.com/chaosxingxc-orion/speech-mllm-training-free-rl) | **范式参考** | W4 复用的成熟免训练奖励/评测机制（best-of-N、奖励引导解码、重排序） | 🟢 成熟 · 参考 |
| W2 | [speech-mllm-efficient-rl-alignment](https://github.com/chaosxingxc-orion/speech-mllm-efficient-rl-alignment) | 支撑 | 高效 GRPO/DPO（LoRA）做语音↔语言对齐 | 🟡 骨架 |
| W3 | [speech-mllm-multitask-rl](https://github.com/chaosxingxc-orion/speech-mllm-multitask-rl) | 支撑 | 单一策略，跨 ASR/ST/SID/SER 的可验证奖励 RL | 🟡 骨架 |

**W4 是旗舰首发工作；W1 是成熟的免训练「范式」参考**，其奖励/评测机制被 W4 复用——推进 W2–W4 时以
W1 的结构与脚本为模板。每个工作的最新进度看 Wiki 的 [[Per-Work-Status]]；项目主旨见 [[Project-Thesis]]。

## 仓库结构 · Repo layout

```
common/         共享库（speechrl_common）：audio、models、rl rewards、data、tracking、utils
projects/       四个工作仓库（各自独立的 git 仓库；被本伞仓 gitignore）
docs/           setup.md（WSL2 + 环境）、architecture.md、data.md（下载）
scripts/        wsl-setup.sh、env-setup.sh、mlflow-ui.sh、wiki-sync.sh、data/（模型+数据集下载）
wiki/           GitHub Wiki 的源文件 —— 共享知识与记忆（用 scripts/wiki-sync.sh 推送）
speechrl-data/  数据根目录（≈281 GB 模型/数据集/检查点）—— 被 gitignore，放在 WSL ext4
CLAUDE.md / AGENTS.md   给 AI 协作者的逐工具操作手册（Claude Code / Codex）
CONTRIBUTING.md         五个仓库的协作方式
```

## 环境 · Environment

**算力在 WSL2 Ubuntu，不在原生 Windows。** RTX 5090（Blackwell, sm_120）没有稳定的原生 Windows
torch 轮子，verl/vLLM/flash-attn 仅 Linux 可用，所有训练都在 WSL2 里跑。Python 固定 **3.12**
（uv venv 在 `~/.venvs/speechrl`，ext4），torch 走 `cu128` 源。**绝不动 `D:/ai-stack/mem0-venv`**
（`.mcp.json` 里隔离的 mem0 MCP 环境）。完整说明见 [docs/setup.md](docs/setup.md)。

## 快速开始 · Quick start

在 **WSL2 Ubuntu** 里（完整指南见 [docs/setup.md](docs/setup.md)）：

```bash
bash scripts/wsl-setup.sh     # 一次性：WSL 的 CUDA toolkit + uv
bash scripts/env-setup.sh     # py3.12 venv + torch cu128 + verl + 可编辑安装 common
source ~/.venvs/speechrl/bin/activate

# 开发单个工作
cd projects/speech-mllm-training-free-rl
uv pip install -e ../../common -e .
bash scripts/train.sh                          # 训练（Hydra）
bash scripts/train.sh rl.learning_rate=2e-6    # 覆盖任意 Hydra 键
bash scripts/eval.sh
```

实验追踪：本地 MLflow（`bash scripts/mlflow-ui.sh` → http://127.0.0.1:5000；纯文件存储、无需服务器/
账号）。配置：每个工作用 Hydra。RL 库：verl。

## 数据与模型 · Data & models

权重和数据集（≈281 GB）**永不进 git** —— 自己在本地拉取（`.gitignore` 兜底，`speechrl-data/`
永远不会被误推）：

```bash
bash scripts/data/probe-access.sh   # 只读：检查 HF/ModelScope 可达性
bash scripts/data/fetch-data.sh     # 下载模型+数据集（跳过已完整的）
bash scripts/data/inventory.sh      # 审计 COMPLETE / PARTIAL / MISSING
```

完整清单、镜像（hf-mirror + ModelScope）、逐项目标见 [docs/data.md](docs/data.md)。

## 协作方式 · Working mode

五个仓库（伞仓 + 四个工作），**改谁就提交到谁**：动 `common/`、`docs/`、`scripts/`、`wiki/` 提交到
本伞仓；动某个工作（含其 README）提交到**那个工作自己的仓库**（它们被本伞仓 gitignore）。默认分支
`master`。改 `common/` 会波及 W1–W4，记得跑 `pytest common/tests`。完整约定见
[CONTRIBUTING_CN.md](CONTRIBUTING_CN.md) 与 Wiki 的 [[Working-Mode]]。

## 给 AI 协作者 · For AI assistants

如果你是 AI 协作者（Claude Code / Codex 等），按这个分层理解仓库：

1. **本 README** —— 权威入口。
2. **[[Project-Thesis]]**（Wiki）—— 项目主旨、三个核心术语与旗舰主张；读完本页紧接着读。
3. **[CLAUDE.md](CLAUDE.md) / [AGENTS.md](AGENTS.md)** —— 你的逐工具操作手册（命令、坑、纪律）。
4. **[GitHub Wiki](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/wiki)**（源在 [`wiki/`](wiki)）—— 团队共享、可演进的知识与记忆。
5. **mem0 MCP** —— **本地、个人**记忆，不与团队共享。

规矩：**开工前先读** Wiki 的 [[Project-Thesis]]、[[Home]] 和 [[Per-Work-Status]]；产生重要决策/经验时，**写回** Wiki 的
[[Decision-Log]]，再 `bash scripts/wiki-sync.sh` 发布。这样人和各自的 AI 才能拿到一致的理解。完整协议
见 [[AI-Collaboration]]。

## 文档导航 · Docs index

| | |
|---|---|
| [docs/setup.md](docs/setup.md) | WSL2 + CUDA + py3.12 venv + torch cu128 + verl |
| [docs/architecture.md](docs/architecture.md) | 伞仓 + 共享库 + 四仓模型 |
| [docs/data.md](docs/data.md) | 模型、数据集、镜像、下载脚本 |
| [common/README.md](common/README.md) | `speechrl_common` 模块地图与安装 |
| [CONTRIBUTING_CN.md](CONTRIBUTING_CN.md) | 多仓协作流程与约定 |
| [Wiki](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/wiki) ([`wiki/`](wiki)) | 共享知识与记忆（Architecture、Working-Mode、Per-Work-Status、AI-Collaboration、Decision-Log、Onboarding） |
