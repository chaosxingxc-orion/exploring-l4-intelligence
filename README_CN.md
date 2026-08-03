# L4 级智能探索

> [English](README.md) | **中文**
>
> 仓库标识：**`exploring-l4-intelligence`** — 探索迈向 L4 级（"创新者"）智能的路径。

这是一个**伞式治理仓（umbrella governance repo）**：研究如何用**免训练 RL（training-free RL）**——奖励引导、推理时、
零权重、零核心结构改动（外挂系统组件另加）的优化——把语音 / omni 多模态大模型在预训练中习得的知识
「激活」出来。候选方向编号只用于调研与审计；方向获得 owner GO 和执行合同后，才以具体研究名称在
`studies/` 下建立独立 GitHub 仓。W1–W4 仍是独立工作仓，不再承载整个主研究。完整主旨见 Wiki 的
[[Project-Thesis]] 页。

> 📖 **从这里开始。** 本 README 是人和 AI 协作者的**唯一权威入口**。更深入的文档在 [`docs/`](docs)；
> 团队共享知识与"记忆"在 **[GitHub Wiki](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/wiki)**
>（源文件在 [`wiki/`](wiki)）。

## 项目仓库 · Program repositories

每个工作都是**独立的 GitHub 仓库**（独立的历史与 issue），但都通过可编辑安装（editable install）
依赖同一个 [`common/`](common)（`speechrl-common`）。

| # | 工作（仓库） | 角色 | 方向 | 状态 |
|---|---|---|---|---|
| W1 | [speech-mllm-training-free-rl](https://github.com/chaosxingxc-orion/speech-mllm-training-free-rl) | 历史/组件工作 | 成熟 selector/evaluator 与 training-free-RL 证据；不是主程序载体 | 🟢 成熟证据 |
| W4 | [speech-mllm-omni-embedding-rl](https://github.com/chaosxingxc-orion/speech-mllm-omni-embedding-rl) | 独立工作（2026-07-12 重定位） | 冻结 omni 嵌入效用（L0/L1）；fresh proposal 待启（#29）；原"解耦旗舰"表述已被取代 | 🟡 骨架 → 重定位中 |
| W2 | [speech-mllm-efficient-rl-alignment](https://github.com/chaosxingxc-orion/speech-mllm-efficient-rl-alignment) | 支撑 | 高效 GRPO/DPO（LoRA）做语音↔语言对齐 | 🟡 骨架 |
| W3 | [speech-mllm-multitask-rl](https://github.com/chaosxingxc-orion/speech-mllm-multitask-rl) | 支撑 | 单一策略，跨 ASR/ST/SID/SER 的可验证奖励 RL | 🟡 骨架 |

目前还没有正式获准的 study 仓。首个计划中的语义研究对象“音频感知的证据获取”已经通过
Stage-1C 和正式开题，但 owner 的 Stage-2A 执行合同仍待签发。候选 R1 已在建仓前日落，因此不建立
空工程仓。仓库和实验资产状态统一从 [[Experiment-Assets]] 路由。

## 仓库结构 · Repo layout

```
common/         共享库（speechrl_common）：audio、models、rl rewards、data、tracking、utils
projects/       四个工作仓库（各自独立的 git 仓库；被本伞仓 gitignore）
studies/        正式语义研究仓的登记表与本地容器（每个子目录都是独立 git 仓）
docs/           setup.md、architecture.md、data.md、完整性与检查资产
scripts/        wsl-setup.sh、env-setup.sh、mlflow-ui.sh、wiki-sync.sh、data/（模型+数据集下载）
wiki/           GitHub Wiki 源文件 —— 项目真理与实验资产管理平面
speechrl-data/  数据根目录（≈650 GB 模型/数据集）—— 在 E 盘，被 gitignore；WSL 侧 /mnt/e/…
CLAUDE.md / AGENTS.md   给 AI 协作者的逐工具操作手册（Claude Code / Codex）
CONTRIBUTING.md         多仓归属与协作方式
```

## 环境 · Environment

**算力在 WSL2 `Ubuntu-24.04`，不在原生 Windows**（默认 `Ubuntu` 是 WSL1、无 GPU）。RTX 5090（Blackwell, sm_120）没有稳定的原生 Windows
torch 轮子，verl/vLLM/flash-attn 仅 Linux 可用，所有训练都在 WSL2 里跑。Python 固定 **3.12**
（uv venv 在 `~/.venvs/speechrl`，ext4），torch 走 `cu128` 源。**绝不动 `D:/ai-stack/mem0-venv`**
（`.mcp.json` 里隔离的 mem0 MCP 环境）。完整说明见 [docs/setup.md](docs/setup.md)。

## 快速开始 · Quick start

在 **WSL2 Ubuntu** 里（完整指南见 [docs/setup.md](docs/setup.md)）：

```bash
bash scripts/wsl-setup.sh     # 一次性：WSL 的 CUDA toolkit + uv
bash scripts/env-setup.sh     # py3.12 venv + torch cu128 + verl + 可编辑安装 common
source ~/.venvs/speechrl/bin/activate

# 开发现有 W1–W4 工作仓
cd projects/speech-mllm-training-free-rl
uv pip install -e ../../common -e .
bash scripts/train.sh                          # 训练（Hydra）
bash scripts/train.sh rl.learning_rate=2e-6    # 覆盖任意 Hydra 键
bash scripts/eval.sh
```

正式 study 的安装和运行命令由其独立仓维护。条件候选不能提前搭空工程；必须先关闭 owner GO 与执行
合同门禁，再登记到 `studies/registry.json`。

实验追踪：本地 MLflow（`bash scripts/mlflow-ui.sh` → http://127.0.0.1:5000；纯文件存储、无需服务器/
账号）。配置：每个工作用 Hydra。RL 库：verl。

## 数据与模型 · Data & models

权重和数据集（≈440 GB）**永不进 git** —— 自己在本地拉取（`.gitignore` 兜底，`speechrl-data/`
永远不会被误推）：

```bash
bash scripts/data/probe-access.sh   # 只读：检查 HF/ModelScope 可达性
bash scripts/data/fetch-data.sh     # 下载模型+数据集（跳过已完整的）
bash scripts/data/inventory.sh      # 审计 COMPLETE / PARTIAL / MISSING
```

完整清单、镜像（hf-mirror + ModelScope）、逐项目标见 [docs/data.md](docs/data.md)。

## 协作方式 · Working mode

这是多仓工作区，**改谁就提交到谁**：治理、Wiki、共享设施和 study 登记表提交到伞仓；W1–W4 代码
提交到对应 `projects/` 仓；正式研究代码提交到对应 `studies/` 独立仓。大型实验资产不进 Git，由
[[Experiment-Assets]] 统一索引。完整约定见 [CONTRIBUTING_CN.md](CONTRIBUTING_CN.md)。

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
| [docs/architecture.md](docs/architecture.md) | 伞式治理仓 + 工作仓 + 独立语义 study 仓模型 |
| [docs/data.md](docs/data.md) | 模型、数据集、镜像、下载脚本 |
| [common/README.md](common/README.md) | `speechrl_common` 模块地图与安装 |
| [CONTRIBUTING_CN.md](CONTRIBUTING_CN.md) | 多仓协作流程与约定 |
| [Wiki](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/wiki) ([`wiki/`](wiki)) | 共享知识与记忆（Architecture、Working-Mode、Per-Work-Status、AI-Collaboration、Decision-Log、Onboarding） |
