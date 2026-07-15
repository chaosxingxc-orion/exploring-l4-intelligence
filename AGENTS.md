# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## What this is

Umbrella repo for a four-part research series on **training-free RL to activate the pretrained
knowledge of speech / omni multimodal LLMs** — reward-guided, inference-time optimization that changes
**no weights and no structure** (north star: `wiki/Project-Thesis.md`; live research state:
`wiki/Research-Objective.md`). It holds a shared library (`common/`), docs, and env scripts; the four
works are **separate GitHub repos** under `projects/` (each its own git repo, gitignored here).

| # | Work repo (under `projects/`) | Package | Role |
|---|---|---|---|
| W1 | `speech-mllm-training-free-rl` | `training_free_rl` | **Primary-program carrier** (mature; the pattern for W2–W4) |
| W4 | `speech-mllm-omni-embedding-rl` | `omni_embedding_rl` | Separate work, repositioned (fresh proposal pending #29) |
| W2 | `speech-mllm-efficient-rl-alignment` | `efficient_rl_alignment` | Supporting (skeleton) |
| W3 | `speech-mllm-multitask-rl` | `multitask_rl` | Supporting (skeleton) |

研究现状/成熟度不在本文件维护（单一真源 = `wiki/Research-Objective.md` /
`wiki/Per-Work-Status.md`）。Each work's entrypoint: `src/<pkg>/main.py` (Hydra loop, RL body stub).

## Environment (important)

- **Compute is WSL2 `Ubuntu-24.04`, not native Windows** — the machine's default `Ubuntu` distro is
  WSL1 (no GPU), so always target `wsl -d Ubuntu-24.04`. The RTX 5090 (Blackwell, sm_120) has no
  stable native-Windows torch wheels; verl/vLLM/flash-attn are Linux-only.
- **Python is pinned to 3.12** in a uv venv at `~/.venvs/speechrl` (ext4). System Python 3.14 is too
  new for ML wheels — do not use it. **Never touch `D:/ai-stack/mem0-venv`** (the isolated mem0 MCP
  env from `.mcp.json`).
- torch from the `cu128` index; if a "no kernel image" error appears, fall back to torch nightly
  `cu128`, then a source build with `TORCH_CUDA_ARCH_LIST=12.0`.
- Datasets/checkpoints/outputs live in `speechrl-data/` on the **E: drive**
  (`/mnt/e/chao_workspace/exploring-l4-intelligence/speechrl-data` from WSL; the repo/code itself
  stays on D:). `SPEECHRL_DATA_DIR` is persisted to this path in the WSL `~/.bashrc`; **never in
  git**. ext4 `~/speechrl-data/` holds only the local MLflow store (`mlruns`).

## Common commands

Run inside WSL2 with the venv active (`source ~/.venvs/speechrl/bin/activate`):

```bash
# One-time env setup (from repo root)
bash scripts/wsl-setup.sh        # CUDA toolkit for WSL + uv
bash scripts/env-setup.sh        # py3.12 venv + torch cu128 + verl + editable common

# Work on a single study
cd projects/speech-mllm-training-free-rl
uv pip install -e ../../common -e .
bash scripts/train.sh                          # train (Hydra)
bash scripts/train.sh rl.learning_rate=2e-6    # override any Hydra key
bash scripts/eval.sh

# Tests
pytest common/tests                            # shared-lib smoke tests
pytest                                         # within a work repo

# Experiment tracking (local MLflow file store; no server/account)
bash scripts/mlflow-ui.sh                      # http://127.0.0.1:5000
```

Data & model assets (~650 GB, **never in git**) are **frozen** to `docs/datasets.lock.json`
(28 datasets + 6 models + 7 ref repos, pinned revisions). One unified downloader reproduces it:

```bash
bash scripts/data/fetch-data.sh --list          # show the manifest, fetch nothing
bash scripts/data/fetch-data.sh                  # fetch everything missing (pinned revisions)
bash scripts/data/inventory.sh                   # audit COMPLETE / PARTIAL / MISSING
```

Full asset list + sources: `docs/data.md`. Regenerate the lock with `scripts/data/gen-lockfile.py`.

## Architecture notes (the big picture)

- **Shared library `speechrl_common`** (`common/src/speechrl_common/`): `audio` (load/resample,
  log-mel), `models` (Qwen2-Audio loader + per-task prompts), `rl` (verifiable reward fns: WER/ASR/
  exact-match — usable directly as GRPO/TRL reward callables), `data` (dataset registry), `tracking`
  (local-MLflow helper), `utils` (seed/logging/checkpoint).
- **Lazy-import discipline:** the package top level imports only light helpers; torch/transformers/
  librosa/mlflow/jiwer are imported *inside* the functions that use them. **Preserve this** when
  adding code — keep heavy imports inside functions, not at module top level.
- **Each work depends on `common` via `[tool.uv.sources]`** editable path `../../common`. Work
  `pyproject.toml` deliberately omits torch/verl (those come from the WSL env so the cu128 index is
  used).
- **Config:** Hydra per work — `configs/config.yaml` composes `model/ dataset/ rl/ experiment/`.
- **RL library:** verl (GRPO/PPO with vLLM rollouts). Base model: Qwen2-Audio (swap SALMONN /
  Qwen2.5-Omni via `models/` + config).

## Gotchas

- **Commit each change where it belongs (most important rule).** This umbrella owns `common/`,
  `docs/`, `scripts/`, `wiki/`, and root `*.md`. A work's code/configs/`README.md` belong to **that
  work's own repo** under `projects/<work>/`. `projects/*/` is gitignored here — if umbrella
  `git status` shows files under `projects/`, they're staged in the wrong repo. Routing table:
  `CONTRIBUTING.md`.
- **`CLAUDE.md` and `AGENTS.md` are sibling guides** (Claude Code / Codex) kept near-identical —
  when you change operating guidance in one, mirror it in the other.
- **`gh` on PATH:** the real GitHub CLI is `C:\Program Files\GitHub CLI\gh.exe` (PATH reordered
  ahead of the shadowing `C:\Python314\Scripts\gh`).
- **Line endings:** `.gitattributes` forces `eol=lf` (esp. `*.sh`) so scripts run in WSL — keep it.
- **Default branch is `master`** for the umbrella and all four work repos.
- **PYTHONPATH separator is `;` on Windows** Python (not `:`) when testing without an install.

## 记录规约（读什么、记什么——2026-07-15 整改生效）

- **默认加载面只有三处**：本文件 → `wiki/Research-Objective.md`（现状唯一热层入口，**开工先
  读**）→ `wiki/Project-Thesis.md`（北极星）。**`wiki/Decision-Log.md` 是冷审计层——绝不整篇
  读**，要出处 grep 单条续NN；子代理只指到 Research-Objective + 所需具体条目。`wiki/survey/`
  = 数据层，按需检索；**数字正典在台账，散文只引行号不复制**。
- **记录模板（强制，全文见 `wiki/AI-Collaboration.md` §记录规约）**：持久记忆五字段（结论/
  推理摘要/目的链/provenance/失效条件）；Decision-Log 新条目 ADR 骨架（Context/Decision/
  **Rationale**/Consequences/Supersedes）；热层每条锁带目的链。核心原则：**只记结论不记推理
  = 违规**——「为什么」必须在任何总结/压缩之前落盘。
- **分层取代**：审计层 append-only（更正走 dated supersession，绝不改写）；工作层
  supersede-in-place（原位改写 + 墓碑指针），**禁止限定语堆叠**。**战役收官即归档**：不被
  正典四件（Research-Objective / Project-Thesis / Per-Work-Status / CLAUDE.md）引用的日期件
  → `wiki/archive/`。
- **知识四层（owner 续47）**：事实层（=默认加载面）／工作知识（日志 append-only + 提炼条
  in-place；战役收官跑**提炼步**）／探索知识（论文库：**FETCH/精读即按 census/ledger schema
  登记，不登记不算读过**；库入口 `wiki/survey/README.md`）／程序知识（脚本/模板/checklist——
  **规约优先做成可执行检查**，保鲜=可测性）。**会话逃逸协议**：目的层讨论、承重结论、未完
  意图**会话结束前必落盘**。全文：AI-Collaboration §记录规约。
- **哈希正典**：一切 (commit, sha256) 证据对以 **git blob 字节**为正典（核验
  `git show <commit>:<path> | sha256sum`）；Windows 工作树 CRLF 哈希是变体，不作证据。
- **加载面预算（试运行值,续46 校准）**：CLAUDE.md ≤12KB、Research-Objective ≤5KB、记忆索引
  ≤30 行。
- **发布件提交前过敌意内审环**（复审至一轮零新发现）。决策后：append Decision-Log → 热层 →
  Per-Work-Status → 归档扫描 → `bash scripts/wiki-sync.sh`（wiki 真源=仓内 `wiki/*.md`，网页版
  只是镜像；mem0 MCP=个人便签，团队知识必须进 wiki）。

## 研究方法论（指针）

**研究流程三阶段** Stage-1（1A 问题界定 / 1B 方向性原型 / 1C 收官选题）→ Stage-2 方案验证 →
Stage-3 发表，**现在 = Stage-1A 收尾**；证据永持产生阶段的等级。**资源姿态三阶段（owner
2026-07-15）**：全力摸高 → 持续整合 → 成本压降——与研究流程三阶段**同名异构勿混**；前期预算
不限定，等预算类判据 = 第③阶段工具（`PHASE-3_TOOL`）。全文：`wiki/Research-Methodology.md`。

## 术语表（Glossary）与收词纪律

**收词纪律（owner 2026-07-13）：不再发挥创造新名词。** 新概念先在本表登记一行人话定义再使用；
外来代号首次出现处括注正名；同名绝不承载两个定义（同名异构必须拆名）。本表在 CLAUDE.md 与
AGENTS.md 间逐字镜像。**死代号与事故史**：`wiki/archive/terminology-tombstones.md`。

- **能力供给 c**：喂给冻结核心的上下文与外挂能力总和（prompt、检索证据、RDU 前端、工具输出、
  解码参数）；rollout 分布条件于它——合理供给下的 rollout 才有意义。
- **rollout / K 池**：冻结模型在供给 c 下对同一输入采样的 K 个候选输出。
- **oracle headroom H(c)**：事后用真值度量的「池内最优 − 默认输出」；**供给条件量**，换供给
  必须重测。
- **oracle**：「总选中池内最优」的假想选择器；只作上界，绝不作可部署数字。
- **selector**：不读 gold、只凭奖励/打分信号从 K 池挑输出的算子。
- **U（任务效用）**：单条输出效用记号（ASR=−WER、QA=EM…）。
- **ρ 实现率**：selector 兑现头空的比例，本质 ρ(c)；拆双锚 **rho_greedy**（锚=部署默认输出）
  / **rho_pool**（锚=池均值）；分母过小不报比率，标 `HEADROOM_TOO_SMALL` 只报绝对量。
- **delta_mbr / regret**：U_sel−U_mbr / U_oracle−U_sel；Stage-1 报告与双 ρ **四量并列**、
  **cellwise-only**（禁无权重跨任务总平均）；部署用 label-free proxy `S`、评估用 `U`，不混。
- **headroom 归因纪律**：selector 实验必须同报该池实测头空；**有头空的 null 才证伪选择器**；
  无头空的 null 只否定该供给配置（供给设计须问责登记，不得无限换供给重试）。
- **MBR**：无标签共识选择；**等 K 强制基线**。
- **RDU（Retrieve–Discover–Use）**：前端知识子系统——供给侧 c 的一种实现。
- **外部控制平面（external control plane / agent scaffold）**：围绕冻结黑盒核心的外部系统总称
  （观察/供给、记忆、工具、评估、选择、预算、停止）；口语「外设优化」的正名。
- **对外术语**：weight-frozen reward-guided inference-time optimization；内部简称 TFRL。
- **SESOI**：最小实质效应量；数值须外部锚定，Stage-2 才冻结。
- **directional-only / hypothesis-grade**：Stage-1 小样方向性证据等级；绝不升级为结论。
- **信息边界**：test-item gold（transcript/answer/qrel）不得进入 selector/reward/prompt/检索/
  候选构造的任何路径；杠杆分 **read-out**（允许）与 **new-info**（禁止）。
- **候选身份与研究态术语**（I1–I4 / UMBRELLA / strict-I2 / δ_corr / PRE_STAGE2_BLUEPRINT）：
  定义与现状统一维护在 `wiki/Research-Objective.md` §4；事故史见墓碑表。
- **诚信核查包 C1–C5**：重校准审查五项核查（尝试普查/数字 lineage/信息边界/负结果/更正）；
  与论文贡献编号 C1–C3 同形异义——引用必带「诚信核查」限定语。

## Research skills

Installed via the Windows Codex plugin marketplace (see `docs/setup.md`):
`academic-research-skills` (`/ars-*`), six `ai-research-skills` groups, official `lean@leanprover`
pack (`lean:*`). Deliberately scoped — K-Dense pack, community lean4-skills, lean-lsp-mcp
intentionally **not** installed.
