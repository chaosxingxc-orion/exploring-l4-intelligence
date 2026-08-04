# L4 级智能探索

> [English](README.md) | **中文**
>
> 仓库标识：**`exploring-l4-intelligence`** — 探索迈向 L4 级（「创新者」）智能的路径。

这是研究计划的**伞式治理仓（umbrella governance repo）**：研究对冻结语音 / omni 多模态大模型的
**免训练、奖励引导的推理时控制**——在 **API-only 冻结核**外围构建外置 reward-guided 控制面，
零权重、零核心结构改动。完整主旨见 Wiki 的 [[Project-Thesis]]；当前研究状态见
[[Research-Objective]]。

> 📖 **从这里开始。** 本 README 是人和 AI 协作者的权威入口。更深入的文档在 [`docs/`](docs)；
> 项目真理源文件在 [`wiki/`](wiki)。

## 运行模式 · Program model

**Stage‑1 在伞仓，Stage‑2 开独立 study 仓，Stage‑3 开独立 paper 仓。** 每个新研究课题的详细讨论、
调研与论证都在伞仓完成（Wiki 调研层、审计轮次、owner 裁决）。方向通过 Stage‑1 且 owner 签发
`OWNER_GO_AND_EXECUTION_CONTRACT` 后，以**具体语义名称建立独立 GitHub 仓**，checkout 到
`studies/<semantic-name>/`。study 的终点是一个或多个**合格 paper candidate**；大规模 confirmatory
实验、论文写作与发表在 `papers/<semantic-name>/` 下另行获准的独立仓完成（须
`OWNER_GO_AND_PAPER_EXECUTION_CONTRACT`，当前没有任何 paper 获准）。候选编号（R1、R2……）只是
调研/审计 provenance，永不作为仓名。

伞仓长期保留**公共资产职能**：数据与模型下载（`docs/datasets.lock.json` 是唯一在线资产权威，
工具在 `scripts/data/`）、基线身份档案、文献调研基建、运行时 pin、治理门禁。数据集是不变的
gold truth；各 study 怎么用（切分、采样、prompt、协议）是其私有方案——随论文发表的切分会结晶为
**新数据集**（派生脚本+样本身份+provenance）晋升回伞仓。

## 已获准的 study

| Study（仓库） | 来源 | 开题 | 状态 |
|---|---|---|---|
| [speech-aware-evidence-acquisition](https://github.com/chaosxingxc-orion/speech-aware-evidence-acquisition) | R2（system-first-stage1c-v2 战役） | GO 2026-08-03；speech-only 身份 2026-08-04 | Stage‑2A E0（无模型数据门）进行中 |

登记表：[`studies/registry.json`](studies/registry.json)；逐 study 实验台账：
`wiki/experiments/<slug>/`。历史 W1–W4 工作仓已于 2026-08-03 退役——本地删除、远端保留为程序外
冷备份（墓碑：`wiki/archive/program/w1-w4-retirement/`）。

## 仓库结构 · Repo layout

```
common/         共享库（speechrl_common）：audio、models、rewards、data、tracking、utils
studies/        获准语义 study 仓的登记表与本地容器（每个子目录都是独立 git 仓）
papers/         获准 Stage-3 paper 仓的登记表与本地容器（每个子目录都是独立 git 仓；当前为空）
docs/           setup.md、datasets.lock.json（资产权威）、superpowers/specs、checks、integrity
scripts/        wsl-setup.sh、env-setup.sh、wiki-sync.sh、data/（下载）、checks/+survey/（门禁）
wiki/           GitHub Wiki 源文件——项目真理、调研层、审计、实验台账
speechrl-data/  数据根目录（数百 GB，E 盘，被 gitignore；WSL 侧 /mnt/e/…）
CLAUDE.md / AGENTS.md   给 AI 协作者的逐工具操作手册（Claude Code / Codex）
CONTRIBUTING.md         多仓归属与协作方式
```

## 环境 · Environment

**算力在 WSL2 `Ubuntu-24.04`，不在原生 Windows**（默认 `Ubuntu` 是 WSL1、无 GPU）。Python 固定
**3.12**（uv venv 在 `~/.venvs/speechrl`，ext4）；torch 走 `cu128` 源（RTX 5090，sm_120）。冻结
30B omni 核的推理走常驻 llama.cpp `llama-server`（GGUF）。完整说明见
[docs/setup.md](docs/setup.md)。

## 快速开始 · Quick start

```bash
# 伞仓治理门禁（离线，Windows 或 WSL 均可）
python scripts/checks/code_graph_check.py
python scripts/checks/study_workspace_check.py
python scripts/checks/legacy_asset_resolution_check.py
python scripts/checks/paper_workspace_check.py
python scripts/checks/ai_context_surface_check.py
python scripts/checks/build_ai_context_manifest.py --check

# 开发已获准的 study（WSL2 内、激活 venv）
cd studies/speech-aware-evidence-acquisition
uv pip install -e ".[dev]"
pytest
```

获准 study 的运行命令、配置和锁由其自己的仓维护；见该仓 `README.md` 与
`wiki/experiments/<slug>/` 下的执行合同。

## 数据与模型 · Data & models

权重和数据集**永不进 git**。`docs/datasets.lock.json` 是资产身份、生命周期、获取状态与核验的
唯一在线来源：

```bash
bash scripts/data/fetch-assets.sh    # 按锁取数（命名 profile；写采集回执）
bash scripts/data/inventory.sh       # 审计 COMPLETE / PARTIAL / MISSING
```

见 [docs/data.md](docs/data.md) 与 `scripts/data/README.md`。

## 给 AI 协作者 · For AI assistants

按此分层按序读仓库：

1. **[CLAUDE.md](CLAUDE.md) / [AGENTS.md](AGENTS.md)** —— 客户端操作手册；
2. **[[Research-Objective]]** —— 当前阶段、权限与下一步；
3. **[[Project-Thesis]]** —— 项目北极星。

文献公共层（`wiki/survey/README.md`）、`wiki/Experiment-Assets.md` 与逐 study 台账只在具名任务
时加载。持久决策
写回 [[Decision-Log]]；web wiki 只是镜像，仅在获授权时用 `scripts/wiki-sync.sh` 发布。完整协议见
[[AI-Collaboration]]。

## 文档导航 · Docs index

| | |
|---|---|
| [docs/setup.md](docs/setup.md) | WSL2 + CUDA + py3.12 venv + torch cu128 |
| [docs/architecture.md](docs/architecture.md) | 伞式治理仓 + 独立语义 study 仓模型 |
| [docs/data.md](docs/data.md) | 模型、数据集、镜像、下载脚本 |
| [common/README.md](common/README.md) | `speechrl_common` 模块地图与安装 |
| [CONTRIBUTING_CN.md](CONTRIBUTING_CN.md) | 多仓协作流程与约定 |
| [Wiki](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/wiki)（[`wiki/`](wiki)） | 项目真理：研究状态、调研层、审计、实验台账 |
