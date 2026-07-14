# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Umbrella repo for a four-part research series on **training-free RL to activate the pretrained
knowledge of speech / omni multimodal LLMs** — reward-guided, inference-time optimization that changes
**no weights and no structure** (north star: `wiki/Project-Thesis.md`; live research state:
`wiki/Research-Objective.md`). It holds a shared library (`common/`), docs, and env scripts; the four
works are **separate GitHub repos** under `projects/` (each its own git repo, gitignored here).

| # | Work repo (under `projects/`) | Package | Role |
|---|---|---|---|
| W1 | `speech-mllm-training-free-rl` | `training_free_rl` | **Primary-study carrier** (mature; the pattern to mirror for W2–W4) |
| W4 | `speech-mllm-omni-embedding-rl` | `omni_embedding_rl` | Separate work, repositioned (fresh proposal pending #29) |
| W2 | `speech-mllm-efficient-rl-alignment` | `efficient_rl_alignment` | Supporting (skeleton) |
| W3 | `speech-mllm-multitask-rl` | `multitask_rl` | Supporting (skeleton) |

研究现状/成熟度**不在本文件维护**（单一真源）：看 `wiki/Research-Objective.md` 与
`wiki/Per-Work-Status.md`。Each work's entrypoint is `src/<pkg>/main.py`, a Hydra `@hydra.main`
loop whose RL body is currently a stub.

## Environment (important)

- **Compute is WSL2 `Ubuntu-24.04`, not native Windows** — the machine's default `Ubuntu` distro is
  WSL1 (no GPU), so always target `wsl -d Ubuntu-24.04`. The RTX 5090 (Blackwell, sm_120) has no stable
  native-Windows torch wheels; verl/vLLM/flash-attn are Linux-only. All training runs in WSL2.
- **Python is pinned to 3.12** in a uv venv at `~/.venvs/speechrl` (ext4). The system Python 3.14 is
  too new for ML wheels — do not use it for the stack. **Never touch `D:/ai-stack/mem0-venv`** (the
  isolated mem0 MCP env from `.mcp.json`).
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

Run a single test: `pytest common/tests/test_smoke.py::test_reward_normalization_exact_match -q`.

Data & model assets (~650 GB, **never in git**) are **frozen** to `docs/datasets.lock.json`
(28 datasets + 6 models + 7 ref repos, pinned revisions). One unified downloader reproduces it:

```bash
bash scripts/data/fetch-data.sh --list          # show the manifest, fetch nothing
bash scripts/data/fetch-data.sh                  # fetch everything missing (pinned revisions)
bash scripts/data/fetch-data.sh --install-deps   # install download deps if missing
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
- **`gh` on PATH:** the real GitHub CLI is `C:\Program Files\GitHub CLI\gh.exe` (System PATH
  reordered so it resolves ahead of the shadowing Python script at `C:\Python314\Scripts\gh`).
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
- **哈希正典**：一切 (commit, sha256) 证据对以 **git blob 字节**为正典（核验
  `git show <commit>:<path> | sha256sum`）；Windows 工作树 CRLF 哈希是变体，不作证据。
- **加载面预算（试运行值）**：CLAUDE.md ≤10KB、Research-Objective ≤5KB、记忆索引 ≤30 行。
- **每个发布件提交前过敌意内审环**（多镜头，修复后复审至一轮零新发现）；决策后：先 append
  Decision-Log → 反映热层 → Per-Work-Status →（归档扫描）→ `bash scripts/wiki-sync.sh`。
  wiki 真源是 `wiki/*.md`，网页版只是镜像。mem0 MCP 是个人便签，团队知识必须进 wiki。

## 研究方法论（一行 + 指针）

**研究流程三阶段** Stage-1（1A 问题界定 / 1B 方向性原型 / 1C 收官选题）→ Stage-2 方案验证 →
Stage-3 发表，**现在 = Stage-1A 收尾**；证据永持产生阶段的等级。**资源姿态三阶段（owner
2026-07-15）**：全力摸高 → 持续整合 → 成本压降——与研究流程三阶段**同名异构勿混**；前期预算
不限定，等预算类判据 = 第③阶段工具（`PHASE-3_TOOL`）。全文（含 1A/1B/1C 允许边界与理论轨
Lean 收敛要求）：`wiki/Research-Methodology.md`。

## 术语表（Glossary）与收词纪律

**收词纪律（owner 2026-07-13）：不再发挥创造新名词。** 新概念先在本表登记一行人话定义再使用；
外来代号首次出现处括注正名；同名绝不承载两个定义（同名异构必须拆名）。本表在 CLAUDE.md 与
AGENTS.md 间逐字镜像。**死代号与事故史**：`wiki/archive/terminology-tombstones.md`。

- **能力供给 c**：喂给冻结核心的上下文与外挂能力总和（prompt、检索证据、RDU 前端、工具输出、
  解码参数）；rollout 分布条件于它——合理供给下的 rollout 才有意义。
- **rollout / K 池**：冻结模型在供给 c 下对同一输入采样的 K 个候选输出。
- **oracle headroom H(c)**：事后用真值度量的「池内最优 − 默认输出」；**供给条件量**，换供给
  必须重测（对应 best-of-N 理论的 coverage 条件）。
- **oracle**：假想「总能选中池内最优」的选择器；只作上界参考，绝不作可部署数字。
- **selector**：不读 gold、只凭奖励/打分信号从 K 池挑输出的算子。
- **U（任务效用）**：单条输出效用记号（ASR=−WER、QA=EM…）；Project-Thesis 的 R 记法同构。
- **ρ 实现率**：selector 兑现头空的比例，本质 ρ(c)；拆双锚 **rho_greedy**（锚=部署默认输出）
  / **rho_pool**（锚=池均值）；分母过小不报比率，标 `HEADROOM_TOO_SMALL` 只报绝对量。
- **delta_mbr / regret**：U_sel−U_mbr / U_oracle−U_sel；Stage-1 报告与双 ρ **四量并列**、
  **cellwise-only**（禁无权重跨任务总平均）；部署用 label-free proxy `S`、评估用 `U`，不混。
- **headroom 归因纪律**：selector 实验必须同报该池实测头空；**有头空的 null 才证伪选择器**；
  无头空的 null 只否定该供给配置——不否定选择原理，但供给设计须问责登记，不得无限换供给重试。
- **MBR**：无标签共识选择；经典强基线/新颖性击杀器；**等 K 强制基线**。
- **RDU（Retrieve–Discover–Use）**：前端知识子系统——供给侧 c 的一种实现（现为
  secondary/ablation）。
- **对外术语**：weight-frozen reward-guided inference-time optimization；内部简称 TFRL。
- **SESOI**：最小实质效应量；数值须外部锚定，Stage-2 才冻结。
- **directional-only / hypothesis-grade**：Stage-1 小样方向性证据等级；绝不升级为结论。
- **信息边界**：test-item 的 golden transcript/answer/qrel 不得进入 selector、reward、prompt、
  检索或候选构造的任何路径；杠杆分 **read-out**（允许）与 **new-info**（禁止）。
- **I1 / I2 / I3 / I4 / UMBRELLA（候选身份，Stage-1C 才选）**：I1=一般 label-free N-best
  selector；I2=音频接地的冻结 omni selector；I3=受约束/可弃权/显式 Goodhart 拐点；I4=(供给 c,
  选择器) 二元组的供给分层兑现率；UMBRELLA=training-free RL ∩ 冻结 omni ∩ advantage→下一步
  动作的立项交集（2026-06-26 立项即有）。现状与限定：`wiki/Research-Objective.md`。
- **strict-I2（= I2∩I4 合取）**：同一冻结 omni 既作生成器又以自身音频接地信号打分，以 ρ(c)
  面刻画；限定 POST_HOC_NARROWED_CANDIDATE（07-14 后验合成，不得以「幸存」框架引用）；
  命名史见墓碑表。
- **δ_corr**：仅保留 TH2a 理论义 = 残余误差相关；经验四量 `selection_overlap`/`error_corr`/
  `conditional_error_mi`/`complementary_gain`（修正案 №1 拆名）；事故史见墓碑表。
- **PRE_STAGE2_BLUEPRINT**：Stage-1A 期间撰写、无现时效力的未来方案结构草图。
- **诚信核查包 C1–C5**：重校准审查五项低成本核查（C1 尝试普查/C2 数字 lineage/C3 信息边界
  审计/C4 负结果普查/C5 append-only 更正）；与论文贡献编号 C1–C3 同形异义——引用必须带
  「诚信核查」限定语。

## Research skills

Installed via the Windows Claude Code plugin marketplace (see `docs/setup.md`):
`academic-research-skills` (`/ars-*`), six `ai-research-skills` groups, and the official
**`lean@leanprover`** pack (`lean:*` skills) for Lean 4 formal proof. Deliberately scoped —
K-Dense scientific-agent-skills, community lean4-skills, and lean-lsp-mcp are intentionally
**not** installed (official Lean skills only, light footprint).
