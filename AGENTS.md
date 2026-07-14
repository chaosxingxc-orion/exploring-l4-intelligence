# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## What this is

Umbrella repo for a four-part research series on **training-free RL to activate the pretrained
knowledge of speech / omni multimodal LLMs** — reward-guided, inference-time optimization that changes
**no weights and no structure** (full statement: `wiki/Project-Thesis.md`). It holds a shared library
(`common/`), docs, and env scripts; the four works are **separate GitHub repos** under `projects/`
(each its own git repo, gitignored by this umbrella).

| # | Work repo (under `projects/`) | Package | Role | Focus | Status |
|---|---|---|---|---|---|
| W1 | `speech-mllm-training-free-rl` | `training_free_rl` | **Primary study** | frozen-core RDU front-end knowledge system + reward-guided trajectory selector (ρ, G0); proposal v4.1 pending signature | 🟢 mature · primary |
| W4 | `speech-mllm-omni-embedding-rl` | `omni_embedding_rl` | Separate work (repositioned 2026-07-12) | frozen omni embedding utility (L0/L1); fresh proposal pending (#29) | 🟡 skeleton → repositioning |
| W2 | `speech-mllm-efficient-rl-alignment` | `efficient_rl_alignment` | Supporting | efficient GRPO/DPO (LoRA) for speech↔language alignment | 🟡 skeleton |
| W3 | `speech-mllm-multitask-rl` | `multitask_rl` | Supporting | one policy, RL across ASR/ST/SID/SER via verifiable rewards | 🟡 skeleton |

**W1 carries the current primary study; W4 is a separate, repositioned work** (2026-07-12 — see
`wiki/Decision-Log.md` 续24 and the Thesis supersession note). W1's mature structure and scripts
remain the pattern to mirror when growing W2–W4. Each work's
entrypoint is `src/<pkg>/main.py`, a Hydra `@hydra.main` loop whose RL body is currently a stub
(`log.info("TODO: implement the RL loop ...")`).

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
  (`/mnt/e/chao_workspace/exploring-l4-intelligence/speechrl-data` from WSL — moved off D: on
  2026-07-09; the repo/code itself stays on D:). `SPEECHRL_DATA_DIR` is persisted to this path in the
  WSL `~/.bashrc`, so runs find the data automatically; **never in git**. ext4 `~/speechrl-data/` holds
  only the local MLflow store (`mlruns`).

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

Data & model assets (~650 GB, **never in git**) live in `speechrl-data/` on the E: drive (gitignored;
`/mnt/e/…` from WSL, via `SPEECHRL_DATA_DIR`). The
set is **frozen** to `docs/datasets.lock.json` — the single manifest (28 datasets + 6 models + 7 ref
repos, pinned revisions). One unified, self-contained downloader reproduces it identically across teams:

```bash
bash scripts/data/fetch-data.sh --list          # show the manifest, fetch nothing
bash scripts/data/fetch-data.sh                  # fetch everything missing (skips complete; pinned revisions)
bash scripts/data/fetch-data.sh --install-deps   # install download deps (hf/modelscope/aria2) if missing
bash scripts/data/inventory.sh                   # audit COMPLETE / PARTIAL / MISSING
```

Full asset list + sources: `docs/data.md`. Regenerate the lock with `scripts/data/gen-lockfile.py`.
The `wave0_fetch.sh` engine and one-off `fetch-semantic-*`/`campaigns/` scripts were retired (unified).

## Architecture notes (the big picture)

- **Shared library `speechrl_common`** (`common/src/speechrl_common/`): `audio` (load/resample,
  log-mel), `models` (Qwen2-Audio loader + per-task prompts), `rl` (verifiable reward fns: WER/ASR/
  exact-match — usable directly as GRPO/TRL reward callables), `data` (dataset registry), `tracking`
  (local-MLflow helper), `utils` (seed/logging/checkpoint).
- **Lazy-import discipline:** the package top level imports only light helpers; torch/transformers/
  librosa/mlflow/jiwer are imported *inside* the functions that use them. So `import speechrl_common`
  and its smoke tests pass even before the heavy stack is installed. **Preserve this** when adding code
  — keep heavy imports inside functions, not at module top level.
- **Each work depends on `common` via `[tool.uv.sources]`** editable path `../../common`. Work
  `pyproject.toml` deliberately omits torch/verl (those come from the WSL env so the cu128 index is
  used) — see comments there.
- **Config:** Hydra per work — `configs/config.yaml` composes `model/ dataset/ rl/ experiment/`.
- **RL library:** verl (GRPO/PPO with vLLM rollouts). Base model: Qwen2-Audio (swap SALMONN /
  Qwen2.5-Omni via `models/` + config).

## Gotchas

- **Commit each change where it belongs (most important rule).** This umbrella owns `common/`,
  `docs/`, `scripts/`, `wiki/`, and root `*.md`. A work's code/configs/`README.md` belong to **that
  work's own repo** under `projects/<work>/`. `projects/*/` is gitignored here, so if umbrella
  `git status` ever shows files under `projects/`, they're staged in the wrong repo. Full routing
  table: `CONTRIBUTING.md`.
- **`CLAUDE.md` and `AGENTS.md` are sibling guides** (Claude Code / Codex) kept near-identical —
  when you change operating guidance in one, mirror it in the other.
- **`gh` on PATH:** the real GitHub CLI is `C:\Program Files\GitHub CLI\gh.exe` (System PATH was
  reordered so `gh` resolves to it, ahead of a shadowing Python script at `C:\Python314\Scripts\gh`).
- **Line endings:** `.gitattributes` forces `eol=lf` (esp. `*.sh`) so scripts run in WSL — keep it.
- **Default branch is `master`** for the umbrella and all four work repos.
- **PYTHONPATH separator is `;` on Windows** Python (not `:`) when testing without an install.

## Research skills

A curated skill set is installed via the Windows Codex plugin marketplace (see
`docs/setup.md`): `academic-research-skills` (paper pipeline, `/ars-*`) + six `ai-research-skills`
groups (post-training, multimodal, fine-tuning, inference-serving, optimization, mlops), plus the
official **`lean@leanprover`** pack (`leanprover/skills`, Apache-2.0) for Lean 4 formal proof —
host-agnostic skills invoked as `lean:*`: `lean:lean-proof` (step-by-step proving), `lean:lean-setup`
(elan/toolchain), `lean:mathlib-build`, `lean:mathlib-pr`, `lean:mathlib-review`, plus
`lean:lean-bisect`/`lean:lean-mwe`/`lean:lean-pr`/`lean:nightly-testing`.

Deliberately scoped — K-Dense `scientific-agent-skills`, the community `cameronfreer/lean4-skills`
pack, and the `lean-lsp-mcp` server are intentionally **not** installed: for formal proof we align
on the official Lean skills only, to keep the footprint light.

## Research methodology — three stages (current stage: 1)

Every research thread moves through three stages; each deliverable states its stage.

1. **Stage 1 — Problem definition (问题定义).** Goal: pin WHICH specific research problem to
   solve. The core work is ARGUMENTATION — ample survey of what problems exist and what
   approaches others use — never reliance on experiments. Method exploration must sweep the
   broader AI literature (text LLM and visual LLM methodology carries as much guidance as
   speech-LLM work). In-house runs are small-sample quick validations only: cheap, single-touch,
   tagged `directional-only`; small-n lacks significance and can settle nothing. Stage 1 ends
   with an owner discussion that selects the problem — never an automatic rollover into Stage 2.
2. **Stage 2 — Solution validation (方案验证).** Large-scale samples solidify the design and
   hypotheses: a fresh Research-Proposal-Template instance, pre-registered frozen criteria,
   paired-bootstrap CIs, full controls, adversarial review — the existing template machinery.
3. **Stage 3 — Publication (论文发表).** Full experimental substantiation, independent
   reproduction, hostile review to convergence.

**Theory track — Lean-locked, convergence-proved, dual-tracked with engineering.** Every theoretical
proposal MUST be formalized in Lean 4 (`proofs/tfrl/`, machine-checked, `sorry`-free bar documented
exceptions) with BOTH a correctness proof AND a **convergence proof** — a static identity is not a
result (the 2026-07-02 review killed the prior theory for being tautology-where-proven). The
engineering implementation must be about the SAME object the theorem is about (dual-track: the code's
selector/update rule ⟷ the theorem's operator). Convergence usually requires **explicit constraint
terms** that bound the problem's edges — KL trust-region (ε / the β regularizer), an over-optimization
budget cap (N*), a slow-drift / Lipschitz precondition, a reward-estimation-error bound — and the
load-bearing content is those constraints: prove the UNCONSTRAINED process fails to converge, then that
the CONSTRAINED one does. See `wiki/Theory-Convergence-and-Constraints.md`.

Evidence keeps the grade of the stage that produced it: a Stage-1 number stays
hypothesis-grade until re-established at Stage 2. Records are append-only — re-grade via a
dated reflection doc, never rewrite. When reading pre-2026-07 records, apply this lens.

## 术语表（Glossary）与收词纪律

**收词纪律（owner 2026-07-13）：不再发挥创造新名词。** 新概念必须先在本表登记一行人话定义再使用；
评审/代理新造的代号在 owner 面向文档首次出现处必须括注本表正名；同一个名字绝不承载两个定义
（同名异构必须拆名，如 ρ）。本表在 CLAUDE.md 与 AGENTS.md 间逐字镜像。

- **能力供给 c（capability supply）**：喂给冻结核心的上下文与外挂能力的总和——prompt、检索证据、
  RDU 前端、工具输出、解码参数。rollout 的分布条件于它（owner 2026-07-13：合理供给下的 rollout
  才有意义和价值）。
- **rollout / K 池（K-sample pool）**：冻结模型在给定供给 c 下对同一输入采样出的 K 个候选输出。
- **oracle headroom（头空）H(c)**：事后用真实标签度量的「池内最优 − 默认输出」。**供给条件量，
  非绝对量**——只在给定供给 c 下有定义，换供给必须重测；文献对应 best-of-N 理论的 coverage 条件。
- **oracle**：假想的「总能选中池内最优」的选择器；只作上界参考，永标 headroom，绝不作可部署数字。
- **selector（选择器）**：不读黄金答案、只凭奖励/打分信号从 K 池挑输出的算子。
- **U（任务效用）**：单条输出的任务效用记号（ASR 用 −WER、QA 用 EM 等）。Project-Thesis 的同一
  公式用 **R** 记号（R_selector/R_greedy/R_oracle），两套记法同构；本表统一用 U。
- **ρ 实现率（realization rate）**：选择器兑现头空的比例，本质是 ρ(c)（供给条件量）。两个变体拆名：
  **rho_greedy** = (U_sel−U_greedy)/(U_oracle−U_greedy)（与 Project-Thesis 的
  ρ=(R_selector−R_greedy)/(R_oracle−R_greedy) 同构，锚=部署默认输出）；
  **rho_pool** = (U_sel−E[U_pool])/(U_oracle−E[U_pool])（锚=池均值）。分母过小不报比率，
  标 `HEADROOM_TOO_SMALL` 只报绝对量。
- **delta_mbr / regret**：delta_mbr = U_sel − U_mbr（对 MBR 的绝对增量）；regret = U_oracle − U_sel
  （距 oracle 的遗憾）。Stage-1 报告与 rho_greedy/rho_pool **四量并列**描述（重校准审查 S1-M2）。
- **headroom 归因纪律**：selector 实验必须同报该池实测头空。**有头空的 null 才证伪选择器**；
  无头空的 null 只否定该供给配置——不否定选择原理，但也不自动豁免（供给设计须另行问责，
  不得无限换供给重试而不登记）。
- **MBR（minimum Bayes risk）**：无标签共识选择；经典强基线 / 新颖性击杀器。
- **RDU（Retrieve–Discover–Use）**：前端知识子系统——供给侧 c 的一种实现。
- **对外术语**：weight-frozen reward-guided inference-time optimization（不改权重/结构）；内部简称 TFRL。
- **A-SEL**：外审 2026-07-13 签署审查临时造的短代号（其 Proposal A 的 selector 选项），
  正名 =「选择器兑现率方向」。仅作历史引用，新文档一律用正名。
- **SESOI**：最小实质效应量；数值须外部锚定，Stage-2 才冻结。
- **directional-only / hypothesis-grade**：Stage-1 小样方向性证据等级；只作背景/方向材料，绝不升级为结论。
- **Stage-1A / 1B / 1C**（owner 2026-07-13 细分）：**1A**=问题界定（广泛 survey、候选研究问题、
  原型空间纸面设计、新颖性/可行性/诚信风险审查；既有数字只作背景方向材料）；**1B**=方向性原型探索
  （廉价小样、单次触碰、须 owner 显式放行、全部尝试与失败登记、不做显著性结论）；**1C**=收官选题
  （owner 基于 survey+原型决策包选唯一具体问题，kill/pivot/proceed，绝不自动滚入 Stage-2）。
- **信息边界（information boundary）**：测试 item 的 golden transcript/answer/qrel 不得进入 selector、
  reward、prompt、检索或候选构造的任何路径；杠杆分 **read-out**（读出既有能力，允许）与
  **new-info**（注入题目新信息，禁止）两类。
- **I1 / I2 / I3 / I4（身份候选）**：Stage-1C 待选的科学子问题候选——I1=一般 label-free N-best
  selector；I2=音频接地的冻结 omni selector；I3=受约束/可弃权、显式检测 Goodhart 拐点的跨任务
  selector（I1–I3 系重校准审查所拟）；I4=(供给 c, 选择器) 二元组——供给分层的兑现率研究（行使该
  审查 S1-F2 的"第四个"选项）。均为候选，Stage-1C 收官前不选。
- **δ_corr 拆名警示（同名异构，修正案 №1）**：`δ_corr` 只保留 TH2a 理论原义=**残余误差相关**
  （越小越近 oracle 收敛），经验估计对象=`error_corr`（有头空 item 上错误指示的 φ 相关）。
  「选择重合」永久移出该符号——拆名四量：`selection_overlap`（仅描述）/`error_corr`/
  `conditional_error_mi`/`complementary_gain`（router 上界增益）。曾被误操作化为「重合>90%⇒kill」，
  第三轮复审裁定构念替换（2026-07-14-identity-contracts-amendment-1.md）。
- **strict-I2 / 同核曲面选择器（= I2∩I4 合取）**：同一冻结 omni 既作生成器、又以**自身**音频接地
  信号作打分器，且以 ρ(c) 兑现面刻画——即 I2 与 I4 的合取身份。构件出处均早于 Survey v2 猎杀：
  同核双系统+δ_corr（TH2a，2026-07-05）、ρ 面（owner 2026-07-11 签署/续34）、own-signal 生存条件
  （I2 拟名当刻，重校准审查 2026-07-13）；「strict-I2」**命名**首现 2026-07-14 Survey v2 工件（补登
  于 SURVEY-RESP-2026-07-14-01，续38）。再复审裁定（续39 接受）：**POST_HOC_NARROWED_CANDIDATE，
  post_hoc_created_at=2026-07-14**——不得以「经攻击幸存」框架引用。bare-I2 的**机制**已被
  scaling-auditory 2503.23395 的同核 audio-conditioned beam log-lik 占据
  （DIRECT_OCCUPIED_AT_MECHANISM_LEVEL；任务格覆盖 MIXED/UNDERSEARCHED，单独报告）。
- **UMBRELLA（伞式交集身份，第五候选）**：training-free RL ∩ 冻结 omni ∩ advantage→下一步动作的
  立项交集对象（2026-06-26 立项即有，非 Survey v2 新造；「advantage→next action」锐化措辞首现
  续36/Survey v2）。与 I1–I4 并列待 Stage-1C；IAD 2504.01931 为预登记坍缩风险。
- **PRE_STAGE2_BLUEPRINT（蓝图素材）**：Stage-1A 期间撰写、无现时效力的未来方案结构草图（如
  `84c6cf6` 的选择器方向 proposal 草稿）；非 Stage-2 入口、非确证协议。
- **哈希正典（canonical hash）**：一切 (commit, sha256) 证据对以 **git blob 字节**为正典（LF，按
  `.gitattributes` 规范化；核验命令 `git show <commit>:<path> | sha256sum`）。Windows 工作树 CRLF
  副本的哈希是**变体**，单独出现不构成证据（2026-07-13 自检工作流坐实的 EOL 缺陷类；变体值须
  standing 注明与正典的换算关系）。
- **诚信核查包 C1–C5（integrity check pack）**：重校准审查 §8 的五项低成本核查——C1 尝试普查
  （registry vs raw run 集合差）、C2 叙述数字 lineage 回链、C3 信息边界审计、C4 负结果普查、
  C5 append-only 工件更正。**拆名警示（同名异构）**：与论文 `papers/agent-level-tfrl` 的贡献
  编号 C1–C3（真实 best-of-N / 冻结探针 / 奖励离散度透镜）同形异义——引用时必须带"诚信核查"
  限定语。

## Shared knowledge & memory (README + Wiki)

- **Canonical onboarding is the root `README.md` / `README_CN.md`** — read it first.
- **Project north star is `wiki/Project-Thesis.md`** — training-free RL to activate pretrained
  knowledge; the current primary study (W1) builds a frozen-core RDU knowledge system with a
  reward-guided trajectory selector (see the 2026-07-12 supersession note there). Read it right after
  the README.
- **Shared, durable team memory is the GitHub Wiki**, sourced from `wiki/` in this repo and published
  with `bash scripts/wiki-sync.sh`. Edit `wiki/*.md` (never only the web Wiki — it's a mirror that the
  sync script overwrites).
- **mem0 MCP is local/personal memory only** — not shared with the team. Promote anything the team
  needs into the Wiki.
- **Before starting:** read `wiki/Research-Objective.md` FIRST — it is the single hot current-state
  entry point (current stage, research object, active constraints, open items, supersession index).
  Then `wiki/Project-Thesis.md` (north star). **`wiki/Decision-Log.md` is the cold append-only
  archive — do NOT read it whole; grep a single 续NN entry only when you need a decision's
  provenance.** Point subagents at `Research-Objective.md` + the specific entries they need, never at
  the whole Decision-Log (context hygiene, 续34). **After a notable decision or learning:** append a
  dated entry to `wiki/Decision-Log.md`, then reflect the current-state delta into
  `wiki/Research-Objective.md` (archive first, then the hot view), update `wiki/Per-Work-Status.md`
  if a work's maturity/plan changed, and run `bash scripts/wiki-sync.sh`. Full protocol:
  `wiki/AI-Collaboration.md`.
