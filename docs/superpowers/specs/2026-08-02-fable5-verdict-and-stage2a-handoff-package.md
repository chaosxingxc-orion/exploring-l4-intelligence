# Fable5 裁决书：研究工程目录重整提案回应与 Stage-2A 交接包

> **状态（2026-08-04）：`IMPLEMENTED_AND_SUPERSEDED_2026-08-03`。** 本裁决/交接包已由 2026-08-03
> 目录重整实施完毕，仅作历史设计与交接理由保留，不再是现行入口。下文中的
> `study_repository: NOT_CREATED`、`uv pip install -e ../../common -e .` 等均描述实施前状态
> （study 现已建仓并于 2026-08-04 收窄为 `speech-aware-evidence-acquisition`，且不依赖
> `speechrl_common`）。现行权威入口：owner 合同
> （`wiki/experiments/speech-aware-evidence-acquisition/2026-08-04-owner-speech-domain-scope-and-identity-contract.md`）、
> Stage-2A 入场合同（`docs/superpowers/specs/2026-08-02-speech-aware-evidence-acquisition-stage2a-entry.md`）、
> study 仓 `README.md`，以及独立复核反馈
> （`docs/checks/program-architecture/2026-08-03-post-reorg-remediation-independent-review/feedback.md`）。

## 文档状态

```yaml
artifact_id: FABLE5-STUDY-DIRECTORY-REORGANIZATION-VERDICT-V1
implementation_status: IMPLEMENTED_AND_SUPERSEDED_2026-08-03  # added 2026-08-04; see banner
date: 2026-08-02
responds_to: docs/superpowers/specs/2026-08-02-fable5-study-directory-reorganization-proposal.md
verdict: ACCEPT_WITH_AMENDMENTS
umbrella_reorganization: COMMITTED
study_repository: NOT_CREATED__GATED_ON_OWNER_GO_AND_EXECUTION_CONTRACT
remote_repository_creation: WITHHELD
model_or_api_execution: WITHHELD
inventory_source_commits:
  umbrella: b9d7a30
  w1_training_free_rl: 7ed41f6
```

## 一、裁决

对目录重整提案返回 **`ACCEPT_WITH_AMENDMENTS`**。

接受的核心：伞仓管研究治理与实验资产图、每个获准语义研究对象独立 GitHub 仓、本地统一
checkout 到 `studies/`、candidate 编号只作 provenance、按 authority 而非"看起来相关"迁移。
这套拓扑与既有门禁（registry admitted-only、fail-closed workspace check、审计不可变）完全自洽。

本次事务已执行的部分：伞仓侧重整批次全部入 HEAD 并通过三道门禁
（`study_workspace_check` PASS、`sf_current_package_check --check` PASS、
`ai_context_surface_check` PASS、检查套件 131 项测试绿）。

本次事务明确未执行的部分：`studies/audio-aware-evidence-acquisition/` **未创建**。这不是遗漏，
是提案与门禁的一致要求——registry 只收 admitted 仓，workspace check 硬性要求每个 checkout
已注册、带真实 GitHub remote URL、有独立 `.git`。在 owner 签发
`OWNER_GO_AND_EXECUTION_CONTRACT` 之前，任何形态的 study 目录（占位、种子、未注册本地仓）
都会把 fail-closed 门禁打红，或迫使 registry 写入虚假条目。工程目录的创建被本文第五节
runbook 机械化为一次单事务操作，等待的只是 owner 一个裁决。

## 二、提案六问逐答

### Q1 — 仓名与包名

接受 `audio-aware-evidence-acquisition`（仓/slug）与 `audio_aware_evidence_acquisition`
（Python package）。slug 通过 workspace check 的语义 kebab-case 校验且不含 candidate token。

### Q2 — 需被新 study 消费的现有实现（文件级）

采纳方式分两类：**DEPEND**（study 以 editable 依赖消费，不复制）与
**COPY_AND_VERIFY**（按提案第六节协议在 R0 逐件复制核验，落 `migration-manifest.md`）。
全部条目当前为 CANDIDATE 态，本清单不构成搬迁授权。

| 来源（commit 见 frontmatter） | 目标位置 | 方式 | 理由 |
|---|---|---|---|
| `common/src/speechrl_common/`（audio/io、rl/metrics、models/generative_omni、models/prompts、tracking/mlflow_logger、utils/seed） | study 依赖 `../../common` | DEPEND | 已是 program-level 共享层，与 W1–W4 同机制 |
| W1 `scripts/baselines/two_pass_runner.py` | `src/.../models/` 冻结核 adapter 参考 | COPY_AND_VERIFY | llama-server + input_audio 的真实可运行调用路径在此 |
| W1 `scripts/baselines/provenance.py` | `src/.../tracing/` | COPY_AND_VERIFY | 请求/响应/成本 provenance 记账基元 |
| W1 `scripts/baselines/metrics.py`、`stats.py`、`deterministic_draw.py` | `src/.../scoring/` 与实验统计 | COPY_AND_VERIFY | 评分与确定性抽样基元，探针战役中经过实测 |
| W1 `scripts/loaders/_common.py`、`registry.py` | `src/.../data/` loader 骨架 | COPY_AND_VERIFY（仅模式） | 载体 loader 的注册/公共层模式；载体本身全部新写 |
| W1 `scripts/knowledge/kb_retrieve.py`、`kb_schema.py`、`corpus_lock.py` | `src/.../evidence/` 候选 | DEFER_TO_METHOD | 证据供给侧候选；方法未收敛前不采纳（KB 全量构建处于 PARKED） |

**明确不迁移**：W1 的 27 个探针时代数据集 loader、baselines wave/cell 一次性实验脚本、
KB 全量构建管线、任何 `_repro` 历史。Earnings21、Earnings22、ConEC 无现成 loader，属 study 新代码。

### Q3 — program-level 与 study-only 的划分

- **Program-level（留伞仓）**：`scripts/data/` 采集与资产锁工具、`docs/datasets.lock.json`、
  `docs/checks/` 回执、三道治理门禁、`speechrl_common` 共享层。
- **Study-only（独立仓）**：三载体 loader 与 split 管理、冻结核 API adapter、evidence
  schema（provenance/OBS-SUPPLY 分离/准入/最终使用）、scorer adapter、trace、实验组合层。

### Q4 — 首个 closest-prior reproduction 建议

建议 **ConEC 上下文偏置 / contextual-ASR 线**作为首个 reproduction：公开 GitHub artifact、与已
锁载体 Earnings21/22 同谱系（readiness 在候选中最高）、信息边界与本研究同构。RECOVER 类纠正线
与 Siskos 实体消解线列为第二/第三队列；Corona 2017、Raghuvanshi 2019、Flemotomos 2024、
COALA 2026 按 entry contract 先作 threat/reproduction 候选评估，再冻结 mandatory 表。
mandatory 表的最终冻结属 owner execution contract 裁决。

### Q5 — execution contract 仍需 owner 冻结的字段

| 字段 | 建议值（可直接采纳） | 必须 owner 裁决 |
|---|---|---|
| 远程仓 | — | GitHub org/URL |
| Runtime | llama.cpp llama-server 常驻 + Qwen3-Omni-30B GGUF（`-ngl 28`，既有实测路径） | build commit 与 GGUF 文件 hash 定版 |
| 载体 | lock 内 Earnings21/22/ConEC 三键 | discovery/confirmatory split 种子与冻结程序 |
| Baseline | Q4 队列次序 | mandatory 名单 + exact revision |
| 预算 | — | 调用/GPU/音频秒/首切片上限与 stop-go 检查点 |
| Exposure | 继承 exposure 排除表沿用现行记账 | 每 run 触达台账格式确认 |

### Q6 — 总回复

`ACCEPT_WITH_AMENDMENTS`，修正案见下节。

## 三、修正案

- **A1（Phase-1 原子性升为显式约束）**：workspace check 要求 registry 条目携带真实 GitHub URL
  且本地 checkout 有独立 `.git`，因此"本地 checkout 先行、远程后补"在机制上不可行。Phase 1
  六步（签发合同→远程建仓→checkout→registry→experiment index→门禁）必须单事务完成。
- **A2（pre-GO 调研主场明确化）**：owner GO 之前，本方向一切调研（文献 delta lane、D1–D4
  无模型数据闭环、contract 字段准备）的主场是**伞仓根目录**——这些工作的 authority 本就在伞仓。
  不得以任何临时目录冒充 study 仓。启动面见第六节。
- **A3（迁移清单为候选态）**：Q2 清单在 R0 按 copy-and-verify 协议逐件裁决落
  `migration-manifest.md`；采纳与否以新仓测试通过为准，不因清单在册而自动搬迁。

## 四、Owner-GO 冻结前置

owner 只需完成一件事：审阅第 Q5 表，把"必须 owner 裁决"列的六个值写成具体值，并以带日期的
决策记录签发 `OWNER_GO_AND_EXECUTION_CONTRACT`。其余全部机械化。

## 五、GO 事务 runbook（签发后单事务执行）

1. 创建远程仓 `https://github.com/<org>/audio-aware-evidence-acquisition.git`（需 owner 明示授权）；
2. `git init` 本地仓并首提交种子，checkout 至 `studies/audio-aware-evidence-acquisition/`；
3. `studies/registry.json` 写入条目（模板如下，`decision_record` 指向 owner 签发的决策记录）：

```json
{
  "name": "audio-aware evidence acquisition",
  "slug": "audio-aware-evidence-acquisition",
  "local_path": "studies/audio-aware-evidence-acquisition",
  "github_repo": "https://github.com/<org>/audio-aware-evidence-acquisition.git",
  "lifecycle": "engineering",
  "decision_record": "wiki/<owner-go-decision-record>.md",
  "experiment_index": "wiki/experiments/audio-aware-evidence-acquisition/README.md"
}
```

4. 创建 `wiki/experiments/audio-aware-evidence-acquisition/README.md`（实验台账索引）；
5. 跑 `study_workspace_check`、`sf_current_package_check --check`、`ai_context_surface_check`；
6. 伞仓单 commit 收束；study 仓按提案 Phase 2 骨架推进 R0 纵向链。

study 仓种子 `CLAUDE.md` 内容（GO 时原样落盘，之后由该仓自治演进）：

```markdown
# CLAUDE.md — audio-aware-evidence-acquisition

独立研究仓：冻结 speech/omni 核上的音频感知证据获取（provenance: 见伞仓 wiki 审计层）。

## 研究边界（不可变）
- 冻结 Qwen3-Omni 核经 API 形态服务边界访问；零参数修改；无任务训练模型；无第二答题 LLM。
- gold 答案/参考转写/测试标注/未来轮不得越过运行时边界。
- OBS 重解析与外部证据供给分开可追踪；一切外部响应/工具动作/模型请求版本化可哈希。
- discovery 与 confirmatory 不相交；confirmatory 判据读结果前冻结。

## 路由
- 当前研究状态与实验台账：伞仓 `wiki/Research-Objective.md`、
  `wiki/Experiment-Assets.md`、`wiki/experiments/audio-aware-evidence-acquisition/README.md`。
- 数据身份：伞仓 `docs/datasets.lock.json`（按键引用，不复制 hash）；字节在
  `SPEECHRL_DATA_DIR`，永不入 Git。
- 执行合同（模型触达、预算、baseline、停止条件的唯一授权面）：伞仓
  `docs/superpowers/specs/2026-08-02-audio-aware-evidence-acquisition-stage2a-entry.md`
  及 owner 签发的 GO 决策记录。

## 环境
- WSL2 `Ubuntu-24.04` + `~/.venvs/speechrl`（Python 3.12）；推理走 llama.cpp llama-server
  （GGUF，`-ngl 28` 常驻）。安装：`uv pip install -e ../../common -e .`。

## 禁止
- 未经执行合同的任何模型/API 触达（含单样本 smoke）；向本仓提交数据/权重/原始 trace；
  绕过 migration-manifest 搬运 W1–W4 代码；push 未经伞仓授权。
```

## 六、pre-GO 阶段：R2 方向调研 session 启动面

在 GO 之前为本方向单开 session 时，工作目录取**伞仓根**，按序载入：

1. `CLAUDE.md`（自动载入）→ `wiki/Research-Objective.md` → `wiki/Project-Thesis.md`；
2. 本裁决书；
3. `docs/superpowers/specs/2026-08-02-audio-aware-evidence-acquisition-stage2a-entry.md`
   （E0/R0/R1/X 序列与 freeze sheet）；
4. 正式开题许可说明（路径见治理节）——含文献截止 `2026-08-02`、STOP_THE_LINE 四触发器、
   delta ledger 规则。

该 session 允许的工作：文献 delta lane（每周有界）、D1–D4 无模型数据闭环、prior readiness
评估、contract 字段准备。禁止：模型触达、建仓、把调研产出写进 `studies/`。

## 七、治理与佐证

- 提案：`docs/superpowers/specs/2026-08-02-fable5-study-directory-reorganization-proposal.md`
- 架构规格：`docs/superpowers/specs/2026-08-02-study-repositories-and-experiment-assets.md`
- 开题许可：`wiki/audit/system-first-stage1c-v2/round-22/2026-08-02-audio-aware-evidence-acquisition-formal-opening-permission-note.md`
  （`FORMAL_OPENING_APPROVED` 与 `STAGE2A_EXECUTION_WITHHELD` 并行有效）
- 伞仓重整落地：commits `c4a26a6`（46 件治理批次）、`b9d7a30`（stage-0 报告重盖）；
  三门禁 PASS、检查套件 131 项测试绿。
