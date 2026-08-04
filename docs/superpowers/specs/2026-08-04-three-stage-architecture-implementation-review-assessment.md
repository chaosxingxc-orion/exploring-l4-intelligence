---
title: "Umbrella → Studies → Papers 三阶段架构实施 Review Assessment"
assessment_id: "PROGRAM-THREE-STAGE-ARCHITECTURE-IMPLEMENTATION-REVIEW-2026-08-04"
date: "2026-08-04"
addressed_to: "research engineering team and research owner"
reviewed_umbrella_commit: "d5ea710"
reviewed_governance_commit: "bb164e6"
reviewed_study_commit: "0d86ddccfddd7ba3e0e3156b03b3c7f92cd21dbf"
review_scope: "three-stage carrier binding, papers workspace foundation, SAEA boundary contract, registries, active truth, executable gates, and deferred promotion infrastructure"
assessment_status: "REVIEW_COMPLETE"
verdict: "CONDITIONAL_ACCEPT__PHASE_A_BOUNDARY_LANDED__ACTIVE_TRUTH_AND_FAIL_CLOSED_COVERAGE_INCOMPLETE"
execution_authority: "REVIEW_ONLY__NO_NEW_AUTHORITY"
model_execution_effect: "NO_NEW_AUTHORITY"
remote_repository_effect: "NO_NEW_AUTHORITY"
---

# Umbrella → Studies → Papers 三阶段架构实施 Review Assessment

> 本 review 针对 umbrella `d5ea710`（核心治理实施 commit `bb164e6`）和当前独立 study
> `speech-aware-evidence-acquisition@0d86ddc`。它审查工程团队是否正确落实 2026-08-04 owner
> 裁决（Decision-Log-2026-08 续91）及其 minimal-first 实施计划。本文只给出 review 结论、缺陷与
> 验收建议，不修改 owner authority，不授权模型/API 调用、实验、远程建仓、push、Wiki 发布或论文
> 投稿。

## 1. 总体裁决

总体结论为：

```text
CONDITIONAL_ACCEPT
Phase-A architecture boundary: LANDED
Three-stage current truth: INCONSISTENT
Independent study adoption: NOT LANDED
Paper zero-state machine enforcement: NOT LANDED
First paper admission readiness: WITHHELD
```

工程团队**正确理解并落地了三阶段架构的核心概念**：

- Stage‑1 = umbrella；
- Stage‑2 = `studies/<slug>`，终点为 qualified paper candidate；
- Stage‑3 = `papers/<slug>`，负责大规模 confirmatory、最终证据、论文与发表；
- study gate 保留 `OWNER_GO_AND_EXECUTION_CONTRACT`；
- paper gate 使用新 token `OWNER_GO_AND_PAPER_EXECUTION_CONTRACT`；
- paper 的成功不是必须正提升，正、零、负结果同等合法；
- paper repo 使用语义命名、独立 Git/GitHub，不使用 R2、venue 或年份作为工程身份；
- 没有真实 candidate 时只建立 `papers/README.md` 和空 registry，没有预建空 paper 仓；
- 没有重组既有 `wiki/experiments/` 和 `docs/checks/` 路径；
- 当前 SAEA 的 E0/R0/R1/bounded-X 保留，paper-scale 工作被散文合同移出默认授权。

这说明团队没有把 proposal 机械照搬，也没有误把“新增 papers 根”理解为立刻创建论文工程。它遵循
了 owner 在续91中签发的“先立边界、机器件后置、不过度设计”裁决。

但当前状态只能接受为**Phase A 概念边界落地**，不能被称为“三阶段工程整改完成”。主要原因不是
被明确延期的 promotion bundle，而是：

1. 多个仍在使用的当前文档继续给出旧的两阶段执行指令；
2. 独立 SAEA study repo 完全没有收到新的 Stage‑3 边界；
3. registry 的唯一 `decision_record` 被改指向一份非自包含补充合同；
4. `papers/registry.json` 被称为 machine authority，却没有任何程序读取或验证；
5. 当前实验资产合同仍把所有正式实验写成 study-owned；
6. confirmatory reservation 的延后触发器晚于 Stage‑2 X，存在时序风险。

这些问题不会阻断当前纯 model-free E0，但在首次可执行 model-facing runner、bounded X、第二个
共享 carrier 的 study 或首个 paper admission 之前，必须按下文分层关闭。

## 2. Review 基线与实际变更

### 2.1 审查到的 umbrella 变更

从 `d4f07fa..d5ea710` 共变更 18 个路径，核心实施位于 `bb164e6`：

- 新增 `papers/README.md`、`papers/registry.json`；
- `.gitignore` 新增 `papers/*/`；
- `Project-Thesis`、`Research-Objective`、`wiki/Architecture`、客户端指南加入三阶段绑定；
- 新增 SAEA Stage‑3 boundary/paper-gate contract；
- `studies/registry.json` 与 experiment index 将 `decision_record` re-pin 到新合同；
- 更新 experiment asset inventory 与 AI context manifest；
- 续91写入 owner 裁决；
- 原 proposal、对抗评审与 minimal-first plan 随后进入 Git。

### 2.2 当前物理状态

- umbrella worktree：clean；
- study worktree：clean；
- `papers/` 只有 umbrella-owned README 与空 registry；
- 不存在 paper child checkout；
- `papers/registry.json` 中 `papers=[]`；
- 没有创建或推送新的 paper remote；
- 当前正式实验 ledger 仍为空。

以上均符合“空 registry 合法、空 paper repo 非法”和“不提前建仓”的 owner 裁决。

### 2.3 本次独立验证

在 Windows 侧先运行两个不依赖 WSL 数据路径的门：

```text
code graph: PASS (22 trusted nodes)
study workspace and experiment assets: PASS
```

`legacy_asset_resolution_check.py --verify-bundles` 必须按仓库约定在 WSL2 运行；Windows 直接运行会把
`/mnt/e/...` 误解析为 Windows 当前盘路径，这不是本次实现缺陷。在 `Ubuntu-24.04`、
`~/.venvs/speechrl` 中重跑后：

```text
574 bindings verified
0 unresolved
4 bundle hashes verified
AI context surface: PASS (0 failures)
AI context manifest: PASS
pytest scripts/checks: 145 passed, 202 subtests passed
pytest common/tests: 21 passed, 1 skipped
```

所有现有门禁均为绿色，但现有门禁没有读取 `papers/registry.json`，也没有检查三阶段语义一致性。因此
“全部 PASS”只能证明旧 study/asset/context 基础没有被这次改动破坏，不能证明 paper-stage 已经
fail closed。

## 3. 正确实施项

### C-1 — 三阶段职责理解正确

`wiki/Decision-Log-2026-08.md:17-25`、`wiki/Project-Thesis.md:66-76` 与
`papers/README.md:9-16` 对三个 carrier、两个 gate 和 paper 成功标准的描述一致。尤其是明确了：

- study 的结果是 candidate，不是默认完成论文；
- paper owns large-scale confirmatory 与 publication；
- 正/零/负结论均可完成；
- 一个 candidate 的 GO 不自动授权同 study 的其他 candidate。

这些是本次整改最重要的语义成果，应保留。

### C-2 — Minimal-first 没有制造假 admission

团队没有为了“架构看起来完整”创建空 paper repo、空 remote、空 CI 或虚假的 promotion receipt。
`papers/README.md:13-22` 清楚写出 empty registry 合法、empty child repo 非法以及延后触发器。这符合
本程序此前“不为未获准研究对象预建仓”的经验。

### C-3 — 没有破坏现有路径和历史资产

团队接受对抗评审 C1：不搬迁当前 `wiki/experiments/<study-slug>/` 和 `docs/checks/<campaign>/`
路径。574 项 legacy bindings、四个 offline bundles、study origin/branch 和 AI context manifest
仍通过验证。没有为了三阶段结构重写历史 experiment/audit bytes。

### C-4 — SAEA 的散文 stop line 已经出现

新合同 `2026-08-04-owner-stage3-boundary-and-paper-gate-contract.md:25-35` 将 study 终点写成
qualified paper candidate，并把 production-scale implementation、large confirmatory、最终优越性
claim 和 publication 放到 paper gate 之后。这是正确的 authority 方向。

## 4. Findings

### P0-1 — BLOCKER：活动阶段方法学仍授权 Stage‑2B 正式实验，直接冲突续91

#### 证据

owner 续91规定：

```text
Stage‑2 内验证保持有界，不含 production-scale confirmatory；
Stage‑3 才拥有大规模预注册 confirmatory、最终证据与发表。
```

但当前 `wiki/Research-Methodology.md` 仍规定：

- 第 21 行：Stage‑2B = “冻结假设、对照、判据后正式实验与统计推断”；
- 第 22 行：Stage‑3 仅是“扩展、独立复现、论文级审计”；
- 第 27 行：技术创新“在 Stage‑2B 验证”；
- 第 42 行：Stage‑1/2A 数字在 Stage‑2B 重建后升级证据等级。

这不是措辞差异，而是实验 authority 的相反分配：旧方法学允许在 study repo 完成正式统计验证，
新裁决则要求 paper gate 和独立 paper repo。

同类旧口径仍出现在：

- `README.md:19-23`：Stage‑2 study 建仓后“all later engineering, experiments and papers live there”；
- `README_CN.md:17-20`：后续全部工程、实验和论文在 study；
- `CONTRIBUTING_CN.md:33-34`：进入 Stage‑2 后全部工作在 study；
- `docs/architecture.md:5-11`：只有两类仓，all Stage‑2+ work lives in study；
- `AGENTS.md:15-23` 与 `CLAUDE.md`：先写 all later work lives in study，随后又写 Stage‑3 在 papers；
- `wiki/Architecture.md:26-28`、`:63-71`：同一页内部同时保留两种说法。

#### 影响

一个新协作者可以完全遵循当前 `README`、canonical architecture 或 research methodology，却绕过
paper gate，在 study repo 中执行 Stage‑2B 正式实验并形成论文。这会使续91只在少数 HOT 段落中
有效，而不是程序级执行规则。

#### 必须修复

在一个 truth-alignment transaction 中：

1. 将 `wiki/Research-Methodology.md` 的 Stage‑2B 改为 candidate qualification/冻结，而非最终
   confirmatory；Stage‑3 接管足够规模的正式统计推断、最终 evidence 与论文；
2. 修复 README/README_CN、CONTRIBUTING/CONTRIBUTING_CN、`docs/architecture.md`、
   `wiki/Architecture.md`、AGENTS/CLAUDE 的旧“all later work”句；
3. 更新 `wiki/Per-Work-Status.md`，明确当前 SAEA 的 paper-scale stop line；
4. 历史 Decision-Log 条目保持 append-only，只由续91的 `Supersedes`/当前路由解释，不回写旧条目；
5. 重建 AI context manifest 并运行 surface/budget checks。

#### 关闭门

P0-1 在任何可执行 R0/R1/X model-facing runner 交付前关闭。纯 model-free E0 可以继续。

### P0-2 — BLOCKER：独立 SAEA repo 没有采用新 Stage‑3 边界

#### 证据

umbrella 的三阶段裁决提交于 `bb164e6`（11:48），但 study HEAD 仍是此前的 `0d86ddc`（10:43）。
Study repo 中：

- `AGENTS.md:19-24` 将旧 speech scope/identity contract 称为“当前合同”，没有 Stage‑3 paper gate；
- `README.md:15-16` 同样把旧合同称为 Current execution authority；
- `docs/engineering.md:33-42` 只描述 R0，未声明 paper-scale stop line；
- `contracts.py:236-444` 的 `FrozenCoreGate` 只验证 E0 与 runtime receipt；
- `test_governance_alignment.py` 只检查 registry 指向的文件存在，不检查新 boundary contract 的语义；
- study 的 local agent guidance、CI 和 entry gate 都无法区分 `baseline/bounded-probe` 与
  `paper-scale/confirmatory`。

这意味着从 umbrella 看，SAEA 已被收窄；但单独 clone 或直接进入 study repo 的执行者仍只看到旧
authority。现有 model gate 在 E0 关闭后会允许任何调用它的 runner，不知道调用属于 bounded X 还是
禁止的 paper-scale campaign。

#### 影响

当前 E0 尚未关闭且 runner 仍未实现，所以没有发生越界执行；但一旦 R0/X 入口变成可运行代码，散文
合同无法在独立仓内 fail closed。三阶段边界只存在于 umbrella，而没有到达实际执行仓。

#### 必须修复

这是一个跨仓事务，不能只改 umbrella：

1. 先在 umbrella 解决 P1-1 的有效合同问题；
2. 在 SAEA repo 更新 AGENTS/CLAUDE、README 和 engineering current authority；
3. 由 study 自己设计并实现最小 execution-scope interface，至少可区分：
   `baseline-reproduction`、`bounded-discovery-probe`、`paper-scale-confirmatory`；
4. Study repo 对第三类必须在无 paper contract/paper repo 的情况下 fail closed；更简单的实现也可以是
   study repo 永不接受 paper-scale profile；
5. 增加 contract tests，证明伪造 stage 字符串、超出 bounded budget、confirmatory profile 和缺少
   paper authority 时都会拒绝；
6. umbrella registry/index 最后 pin 新 study commit 与有效合同。

伞仓不应规定 study 内部目录布局，但有权通过 owner contract 要求这一跨仓可验证接口。

#### 关闭门

P0-2 在首个 model-facing R0/X runner 可执行前关闭。当前 model-free E0 不受阻。

### P1-1 — MAJOR：registry 的唯一 decision record 被改成非自包含补充合同

#### 证据

`studies/registry.json:18-19` 和 experiment index frontmatter 当前 pin：

```text
2026-08-04-owner-stage3-boundary-and-paper-gate-contract.md
```

但该文件 frontmatter 明确写：

```text
relation: supplements ...; narrows default execution authority only
```

它没有自包含重述：

- `OWNER_GO_AND_EXECUTION_CONTRACT` authorization；
- semantic repo URL/local path/package/namespace；
- speech-only 完整范围与排除项；
- frozen core、数据、baseline、信息边界；
- 预算和 stop lines 的具体值；
- 原 scope contract 的完整路径/blob。

同时 `Research-Objective.md:18-23`、`Experiment-Assets.md:8-16` 和 `studies/README.md:19-23`
仍把原 speech-domain scope/identity contract 当作当前权威。于是 registry 的“唯一 decision_record”与
其他 current surfaces 指向不同合同；要理解有效 authority 必须追一条 supplement chain。

这违反本仓“active truth 必须自包含，amendment/response chain 不得充当 working context”的规则，也
削弱了 registry decision-record blob 的审计意义：机器证明的是补充件字节没漂移，不是完整执行合同
没漂移。

#### 修复选项

优先推荐 A：

- 新建一份**自包含**的 effective owner contract，继承原 GO 事实，同时完整重述 speech-only 身份、
  E0/R0/R1/bounded-X、预算/exposure 和 Stage‑3 stop line；
- registry/index 只 pin 这一份 effective contract/blob；
- 原两份合同留作历史/来源记录。

可接受的 B：

- registry `decision_record` 恢复指向自包含 scope/identity contract；
- 在未来 registry v3 增加独立、机器校验的 `stage_boundary_record` 字段；
- 在 v3 落地前，experiment index 明确列出两份 current authority，但不得称补充件为唯一 current
  effective contract。

### P1-2 — MAJOR：`papers/registry.json` 被称为 machine authority，但没有任何机器消费者

#### 证据

`wiki/Experiment-Assets.md:28` 将 `papers/registry.json` 称为 Machine authority；然而：

- `rg` 在 `scripts/`、tests 和 `docs/integrity/` 中找不到 `papers/registry.json`、
  `paper-repository-registry` 或 paper workspace checker；
- `study_workspace_check.py` 只读取 `studies/registry.json`；
- `.gitignore` 已经忽略 `papers/*/`；
- experiment asset inventory 不含 paper registry path/hash；
- code graph 与 AI context manifest 不登记 paper registry；
- 当前所有门禁在 paper schema 完全不受检查的情况下仍 PASS。

#### 影响

当前空状态没有伪 admission，因此不阻断 E0。但任何人都可以在 `papers/` 下创建未登记 child repo，
umbrella `git status` 看不到它，现有 gate 也不会失败；也可以破坏 registry schema/count 而不触发当前
workspace checks。“Machine authority”目前只是散文称谓。

#### 建议修复

不需要现在实现完整 promotion graph，但应立即增加一个低成本 zero-state gate：

- strict JSON/duplicate-key/schema/fixed-field validation；
- `papers=[]` 与 `Admitted paper repositories: **0**` 一致；
- `papers/` 下不存在任何 child directory；
- `.gitignore` 精确包含 `papers/*/`；
- paper registry hash 进入确定性 asset inventory；
- 负向测试覆盖 malformed registry、非空未登记目录、count drift。

到真实 candidate 时再扩展 entry schema、origin/branch、primary/supporting study、promotion receipt 和
`--require-installed`，即可同时遵守 owner 的 minimal-first 裁决与 fail-closed 原则。

### P1-3 — MAJOR：Experiment-Assets 对 paper 的声明与通用实验合同互相冲突

#### 证据

`wiki/Experiment-Assets.md:26-32` 新增 paper registry，并声明未来 paper experiment index 位于：

```text
wiki/experiments/papers/<paper-slug>/
```

但同一文件：

- authority table 第 44-49 行只定义 study identity 和 independent study repo；
- 第 57 行仍写“Every formal experiment”都进入 `wiki/experiments/<study-slug>/`；
- required binding 使用 `study commit`，没有 carrier type 或 paper commit；
- update transaction 第 98 行附近只定义 study admission，没有 paper promotion transaction；
- experiment asset inventory 只绑定 `study_registry`。

#### 影响

首个 paper 到来时，工程团队无法从 current control plane 判断：paper 实验应该登记 paper commit 还是
study commit、使用哪一条 update transaction、是否进入现有 asset inventory。新 section 宣布了路径，
但没有把它整合进权威表和通用实验 schema。

#### 建议修复

不迁移现有 study 路径，只把通用术语扩成 carrier-aware：

- `carrier_type = study | paper`；
- `carrier repository URL + exact commit`；
- Stage‑2 记录继续在 `wiki/experiments/<study-slug>/`；
- Stage‑3 记录可使用已裁决的 `wiki/experiments/papers/<paper-slug>/`；
- authority table 同时列出 study 与 paper code/config/tests；
- update transaction 分成 study admission 与 paper promotion；
- empty paper registry 也进入 asset graph hash。

### P1-4 — MAJOR / OWNER-ACCEPTED RISK：confirmatory reservation 的触发器晚于 candidate 形成过程

#### 证据

对抗评审 C2 已正确指出：reservation 是 Stage‑2 前置，因为 R0/X 已经建立 discovery/confirmatory
边界，多个 studies 也可能在 paper 之前共享 carrier。原评审修订答复要求立即建立 program ledger。

owner 续91随后有意收缩实施，把 reservation ledger 延后到：

```text
SAEA candidate 进入 paper-candidate-ready
或 owner 启动首个 paper admission
```

该延期是 owner 明确接受的风险，不能归咎为团队擅自遗漏。但触发器仍存在时序问题：bounded X 用于
形成 candidate；如果直到 candidate ready 才建立 reservation，selection exposure 已经发生。若期间
第二个 study 共享 Earnings21/22/ConEC，单仓 exposure ledger 也无法阻止跨仓重复消费。

当前已有 2026-08-03 程序纪律作为临时保护：

- 首条正式 experiment ledger row 必须带 split identity hash 和“已消耗”标记；
- 新 study 的 Stage‑1 carrier selection 必须扫描已有 experiment/exposure ledgers；
- 第二个 study 实际共享 carrier 时建立只读聚合视图。

但当前 SAEA experiment ledger 表头尚无显式 `split identity hash` / `consumed` 字段，且没有机器检查。

#### 建议裁决

无需立即实现 proposal 中完整 reservation 系统，但应把触发器改成以下事件的**最早一个**：

1. 首个 bounded X run 读取 discovery 结果之前；
2. 第二个 study 计划使用相同 carrier/split family 之前；
3. 首个 confirmatory split 被物化、查询或读取之前；
4. 任何 candidate 请求 `paper-candidate-ready` 之前。

在 ledger 系统落地前，至少立即给 SAEA experiment index 增加 split hash、role、consumed/exposure
字段，并用 test 验证首条正式记录不能省略。这是对 owner minimal-first 的最小安全补丁，而不是提前
实现完整 promotion architecture。

### P2-1 — MINOR：canonical placement 与贡献指南没有登记 paper 层

`wiki/AI-Collaboration.md:33-42` 的 canonical placement table 只有 Study repository registry 和
Study experiment index；工程资产三层权威也只写 study repo。`CONTRIBUTING.md`/中文版本仍把仓类写成
umbrella + studies，没有说明：

- `papers/README.md`/registry 属于 umbrella；
- `papers/<slug>/` 的改动提交到独立 paper repo；
- paper remote creation/push/publication 仍需明确授权；
- paper index、promotion receipt 和 release 的归属。

对抗评审 C10 正确说明：修改 AI-Collaboration table 必须与
`ai_context_surface_check.py` 的 `POLICY_ROLE_ORDER`/`POLICY_ROLE_SEMANTICS` 和 tests 同 commit。
这项工作可以很小，不应等到首个 paper admission 才修 CONTRIBUTING 的错误所有权模型。

### P2-2 — MINOR：proposal/review 元数据仍停留在裁决前状态

原 proposal frontmatter 仍是：

```text
proposal_status: PROPOSED_FOR_REVIEW
supersession_effect: NONE_UNTIL_OWNER_ACCEPTANCE...
```

但 owner 已在续91作出部分接受、部分否决和延期裁决。对抗评审文件标题仍为“裁决请求”，frontmatter
仍写 `execution_authority: DOCUMENTATION_ONLY`，没有顶部 status note 指向续91。Companion plan 能解释
现状，但执行者必须读三份文件才能知道 proposal 哪些段落有效。

建议保留原正文，只更新 frontmatter/status banner：

```text
REVIEWED__PARTIALLY_ACCEPTED_AND_OWNER_TRIMMED__SEE_DECISION_LOG_续91
```

并明确“评审正文第 4/5 节 + owner 续91优先于原 proposal”。这不会改写历史理由，只修复当前路由。

## 5. 对“延期项”的公平判定

以下没有在 Phase A 实现，**不应单独算工程团队错误**，因为 owner 续91明确延期：

- full paper entry schema；
- primary/supporting study graph；
- 20 字段 candidate bundle 的 BLOCKER/RECOMMENDED 分级；
- promotion receipt 双向 commit 绑定；
- full `paper_workspace_check --require-installed`；
- synthetic cross-repo promotion dry run；
- study registry v3 lifecycle；
- 首个 paper admission runbook 和 CI；
- 真实 paper child repo/remote。

但是，延期必须满足两个条件：

1. 当前零状态不能被散文误称为已经机器闭环；
2. 触发器必须早于第一个不可逆动作，而不是与该动作同时或更晚。

因此 P1-2 的 zero-state gate、P1-4 的 Stage‑2 exposure 前置仍需要提前处理；其余完整 machinery 可以
按 owner 决定留到真实 candidate。

## 6. 建议整改顺序

### R0 — Current truth alignment（umbrella，立即）

关闭 P0-1、P1-3、P2-1、P2-2：

- 修 Research-Methodology、README、CONTRIBUTING、docs/wiki Architecture、AGENTS/CLAUDE、Per-Work；
- generalize Experiment-Assets 的 carrier authority；
- 更新 AI-Collaboration + checker constants/tests；
- 给 proposal/review 加 owner adjudication status note；
- 重建 manifest 并跑全部 umbrella gates。

这是文档与既有 checker 的小事务，不需要 model、数据、paper repo 或远程权限。

### R1 — Self-contained authority（umbrella，立即）

关闭 P1-1：签发一份自包含 effective SAEA contract 或采用双字段 schema，再 re-pin registry/index/
inventory。此步需要 owner 对载体合同形式确认，但不改变已裁决的研究边界。

### R2 — Independent study adoption（SAEA + umbrella，R0 runner 前）

关闭 P0-2：先提交 study repo 的 guidance/tests/execution-scope guard，取得 study commit；再由 umbrella
记录该 commit 与 contract。不能只在 umbrella 宣布 study 已收窄。

### R3 — Zero-state paper gate（umbrella，近期）

关闭 P1-2：只验证空 registry、零 child、count、ignore 和 hash；完整 paper schema 仍触发器化。

### R4 — Exposure/reservation minimum（umbrella + study，bounded X 前）

关闭 P1-4：扩 experiment ledger 字段与测试；在四个最早触发事件之一发生时升级为 program-wide
reservation/derived view。

### R5 — Full promotion machinery（真实 candidate 时）

按 owner Phase B 实施：candidate schema、paper entry schema、promotion receipt、完整 paper checker、
dry run、首仓 admission。R0–R4 关闭不代表 R5 自动授权。

## 7. 修复后验收标准

### 7.1 语义一致性

- 任一 current onboarding/architecture/methodology 页面都不得再写 Stage‑2 后所有论文工作留在 study；
- Stage‑2B 明确止于 candidate qualification，不拥有 production-scale confirmatory；
- Stage‑3 明确拥有正式规模统计推断、最终 evidence 与 publication；
- `Per-Work-Status` 和 SAEA index 明确当前 paper-scale stop line；
- 历史日志不回写，续91拥有清晰 supersession routing。

### 7.2 SAEA 独立仓

- standalone clone 的 AGENTS/README 能发现当前 paper gate；
- study runner 不能接受 paper-scale/confirmatory execution profile；
- contract test 对伪造 profile、超预算、缺 authority 失败；
- E0/R0/R1/bounded-X 合法路径保持可执行；
- study 与 umbrella 各自 commit 后，registry/ledger 精确 pin。

### 7.3 Paper 零状态

- malformed/duplicate-key paper registry 失败；
- `papers/` 出现未登记 child 时失败；
- paper count 与 Experiment-Assets 不一致时失败；
- registry hash 漂移使 asset inventory 失败；
- empty registry 继续合法；
- 不要求创建 paper remote 或 child repo。

### 7.4 Exposure

- 首条正式 study experiment 必须带 split hash、role、consumed/exposure；
- inherited exposure 单调不减；
- bounded X 前可证明 confirmatory 未读；
- 第二个共享 carrier study 到来时产生跨仓只读冲突检查；
- paper promotion 不会因换 repo 把已读数据重新标为未读。

### 7.5 命令门

在 WSL2 `Ubuntu-24.04`、`~/.venvs/speechrl` 中至少通过：

```text
python scripts/checks/code_graph_check.py
python scripts/checks/study_workspace_check.py --require-installed
python scripts/checks/legacy_asset_resolution_check.py --verify-bundles
python scripts/checks/ai_context_surface_check.py
python scripts/checks/build_ai_context_manifest.py --check
pytest scripts/checks -q
pytest common/tests -q
```

并新增等价的：

```text
paper zero-state registry/workspace negative tests
three-stage current-truth semantic assertions
SAEA execution-scope negative tests
split-hash / consumed / inherited-exposure record tests
```

## 8. 给工程团队的最终判定

本轮不是失败实施。团队正确完成了 owner 明确批准的最小目录基础，并且没有破坏现有 study、legacy
资产或 context gates。值得保留的成果是：三阶段载体已获 owner 裁决，paper 根存在但没有假项目，
SAEA 在 umbrella 层已有 paper-scale stop line，正/零/负结果政策也已固定。

但团队对“最小实施”的理解收缩得过头：它不仅延期了未来 promotion machinery，也遗漏了**当前活动
真相的完整替换**和**独立 study 执行面的同步**。这两项不是过度设计，而是让已经签发的边界真正生效
所必需的工作。

因此本 review 的交付判定是：

```text
Phase A directory foundation: ACCEPT
Owner ruling capture: ACCEPT
No-empty-paper discipline: ACCEPT
Current-truth alignment: REJECT_PENDING_REPAIR
SAEA cross-repo boundary enforcement: REJECT_PENDING_REPAIR
Paper machine authority claim: WITHHOLD
First paper admission readiness: WITHHOLD
Current model-free E0: MAY_CONTINUE
Model-facing R0/X implementation: HOLD_BEFORE_P0-1/P0-2_CLOSE
```

建议团队先按 R0→R4 完成一轮小而完整的 remediation，再申请独立复核。不要提前实现真实 paper
promotion，也不要因为当前所有旧门禁为绿就把三阶段架构标记为 fully implemented。

