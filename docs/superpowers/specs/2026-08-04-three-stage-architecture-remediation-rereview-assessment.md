---
title: "Umbrella → Studies → Papers 三阶段架构整改第二轮 Review Assessment"
assessment_id: "PROGRAM-THREE-STAGE-ARCHITECTURE-REMEDIATION-REREVIEW-2026-08-04"
date: "2026-08-04"
addressed_to: "research engineering team and research owner"
reviewed_umbrella_commit: "16f3815"
reviewed_remediation_commit: "dc8c2f0"
reviewed_study_commit: "6c4b37e9ff90becde3df934fa2b87e136f1354eb"
review_scope: "second-round verification of prior findings, three-stage current truth, SAEA cross-repository adoption, exposure discipline, paper zero-state gate, registries, plans, and executable checks"
assessment_status: "REVIEW_COMPLETE"
verdict: "CONDITIONAL_ACCEPT__CORE_ARCHITECTURE_LANDED__CLOSURE_CLAIMS_OVERSTATED"
execution_authority: "REVIEW_ONLY__NO_NEW_AUTHORITY"
model_execution_effect: "NO_NEW_AUTHORITY"
remote_repository_effect: "NO_NEW_AUTHORITY"
---

# Umbrella → Studies → Papers 三阶段架构整改第二轮 Review Assessment

> 本 review 审查工程团队针对上一轮
> `2026-08-04-three-stage-architecture-implementation-review-assessment.md` 所做的整改。审查基线为
> umbrella `16f3815`（主体整改 `dc8c2f0`）和独立 study
> `speech-aware-evidence-acquisition@6c4b37e9ff90becde3df934fa2b87e136f1354eb`。本文只给出
> review 结论、缺陷分级与验收要求；不授权模型/API 调用、数据实验、远程建仓、push、Wiki 发布、
> paper admission 或投稿。

## 1. 总体裁决

本轮整改不是失败，也不需要推翻目录架构。团队已经把三阶段的**物理载体和主要治理边界**正确落地：

```text
Stage-1  umbrella                       方向框定、系统调研、选题与 owner decision
Stage-2  studies/<semantic-study>/      prior 复现、方案探索、candidate qualification
Stage-3  papers/<semantic-paper>/       大规模预注册 confirmatory、最终证据、论文与发表
```

相较上一版，以下关键问题已经实质解决：

- Stage‑2B/Stage‑3 的正典方法学已重新划界；
- SAEA 已采用独立 study 仓内的 Stage‑3 stop line；
- registry 已改为 pin 一份自包含的 consolidated execution contract；
- `papers/registry.json` 已有严格的零状态机器门；
- experiment asset control plane 已扩展为 study/paper carrier-aware；
- paper registry hash 已进入确定性 asset inventory；
- confirmatory reservation 的触发时点已提前；
- proposal/review 的裁决状态已得到回填；
- umbrella 和 study 当前 worktree 在 review 开始时均为 clean。

因此本次总判定为：

```text
Three-stage directory foundation:             ACCEPT
Study/paper repository ownership model:        ACCEPT
Self-contained SAEA authority:                 ACCEPT
Paper zero-state fail-closed gate:             ACCEPT
Current-truth replacement:                     PARTIAL
SAEA exposure-record contract:                 REJECT_PENDING_REPAIR
SAEA execution-scope semantic enforcement:     PARTIAL
Claim that all prior findings are closed:      REJECT
Current model-free E0 work:                     MAY_CONTINUE
First model-facing R0/R1/X execution:           HOLD_UNTIL_P1_FINDINGS_CLOSE
First paper admission:                         WITHHELD_BY_DESIGN_UNTIL_PHASE_B
```

核心判断是：**目录架构已经能够承载“一个 study 产生多篇独立 paper”的诉求，但整改不能被标记为
fully closed。** 当前剩余问题集中在执行合同的最后一公里，而不是目录拓扑本身。

## 2. Review 基线与核验范围

### 2.1 实际提交状态

Umbrella 当前相关提交：

```text
16f3815 governance(three-stage-review): stage studies registry re-pin to consolidated contract
dc8c2f0 governance(three-stage-review): close all prior findings per review (续92)
d5ea710 docs(three-stage): proposal input, adversarial review record, minimal-first plan
bb164e6 governance(three-stage): bind Stage-1/2/3 to umbrella/studies/papers carriers (续91)
```

独立 SAEA study 当前相关提交：

```text
6c4b37e governance(stage-boundary): adopt Stage-2 boundary + fail-closed execution-scope guard
0d86ddc security(model-gate): receipts are verified, not trusted
```

物理状态符合预期：

- `studies/speech-aware-evidence-acquisition/` 是独立 Git 仓；
- origin 为 `https://github.com/chaosxingxc-orion/speech-aware-evidence-acquisition.git`；
- branch 为 `master`；
- umbrella registry 的 remote、branch、package、local path 与实际仓一致；
- `papers/` 只有 umbrella-owned `README.md` 与空 `registry.json`；
- 没有 paper child checkout，也没有伪造 paper admission。

### 2.2 Authority 与 blob 核验

`studies/registry.json` 当前唯一 `decision_record` 指向：

```text
wiki/experiments/speech-aware-evidence-acquisition/
2026-08-04-owner-consolidated-execution-contract.md
```

其 Git blob 为 `8ddd0cf2a96908befc8b49e69602185729ba17ba`，与 registry 精确一致。合并合同
§9 中三份来源记录的 blob 也全部复算一致：

```text
e059b6257fad4be45f3014297a26c4a40257b9af  2026-08-03 owner GO
57bf8e23f7282162d06936b5ea484ea6fb5bdea8  2026-08-04 speech-only scope/identity
5f91226f25d6bfd5c5cd427c57fecc635eb43066  2026-08-04 Stage-3 boundary/paper gate
```

这关闭了上一轮“registry pin 到非自包含 supplement”的问题。当前执行者无需追 amendment chain
才能理解 SAEA 的身份、范围、预算、数据、baseline、exposure、执行序列和 Stage‑3 stop line。

## 3. 上一轮 Findings 关闭矩阵

| 上轮 finding | 本轮状态 | 评审结论 |
|---|---|---|
| P0-1 活动方法学仍把正式验证放在 Stage‑2B | **PARTIAL** | `Research-Methodology` 已正确改为 candidate qualification，但 AGENTS/CLAUDE 仍保留“validated in Stage‑2B”的旧句，默认上下文仍可能产生错误 authority 推断 |
| P0-2 独立 SAEA repo 未采用 Stage‑3 边界 | **PARTIAL / SUBSTANTIALLY LANDED** | 独立仓指南、README、engineering 和模型 gate 已采用新边界；但当前 guard 只验证 profile 名称，不验证实际 split、规模与预算，不能证明 paper-scale 工作不可伪装 |
| P1-1 decision record 非自包含 | **CLOSED** | consolidated contract 自包含，registry/index/HOT 全部 re-pin，source blobs 可复算 |
| P1-2 paper registry 无机器消费者 | **CLOSED FOR ZERO STATE** | 新 checker 严格验证空 registry、零 child、ignore、count；inventory 纳入 registry hash；完整 admission mode 合理延期 |
| P1-3 Experiment-Assets 仍是 study-only | **CLOSED AT CONTROL-PLANE LEVEL** | authority、record schema、index 路径和 admission transaction 已 carrier-aware；贡献指南仍有少量路径摘要遗漏，见 P2 |
| P1-4 confirmatory reservation 时序过晚 | **PARTIAL** | 四事件最早触发器已正确提前；umbrella experiment index 已增加字段，但 study exposure ledger 没有同步，临时保护链未闭合 |
| P2-1 placement/CONTRIBUTING 未覆盖 paper | **PARTIAL** | repository ownership 已覆盖 paper；paper experiment index 的路由摘要仍不完整 |
| P2-2 proposal/review 元数据停留在裁决前 | **CLOSED** | proposal 与 critique 已加入 owner adjudication 状态和续91/续92路由 |

因此，`docs/superpowers/plans/2026-08-04-three-stage-workspace-remediation.md` 中“close all prior
findings”及 R0/R2/R4 全部完成的表述过强。正确状态应是：**核心架构闭合，三项接口修复仍开放。**

## 4. 正确实施项

### C-1 — Stage‑2 与 Stage‑3 的正典方法学边界已修正

`wiki/Research-Methodology.md:20-28` 当前明确：

- Stage‑2A 做 closest-prior reproduction 与 bounded directional exploration；
- Stage‑2B 做 candidate qualification、冻结假设/对照/判据、power 与预注册准备；
- Stage‑3 才执行 production-scale confirmatory、正式统计推断、最终 evidence 与 publication；
- Stage‑1/2 的数字在 Stage‑3 confirmatory 重建前保持 hypothesis/candidate grade。

这是三阶段设计的关键科学边界，已经从局部 proposal 上升为 current methodology，应保留。

### C-2 — Paper 零状态门实现得克制且正确

`scripts/checks/paper_workspace_check.py` 没有提前设计未知的首篇 paper schema，而是只冻结当前事实：

- exact top-level schema；
- duplicate JSON key fail closed；
- `papers=[]`；
- `papers/` 无 child directory、无 stray file；
- `.gitignore` 含精确的 `papers/*/`；
- control-plane admitted count 与 registry 一致；
- 任一非空 paper entry 在完整 promotion machinery 落地前直接失败。

这是 minimal-first 与 fail-closed 的合理平衡。完整 entry schema、promotion receipt、origin/branch、
candidate bundle 和 `--require-installed` 继续留在首个真实 admission 前，不属于本轮遗漏。

### C-3 — 独立 study repo 已收到治理边界

SAEA 的 standalone README、AGENTS/CLAUDE 与 engineering guide 都能发现 consolidated contract 和
paper gate。`FrozenCoreGate.assert_model_touch_allowed(execution_profile)` 在读取 E0/runtime receipt 前
先检查 execution profile，并且：

- `model-free-check` 不允许触发模型；
- `baseline-reproduction`、`bounded-discovery-probe` 才能进入 receipt 校验；
- paper/confirmatory/production/unknown profile fail closed；
- 当前 `reproduce.sh`、`evaluate.sh` 仍固定 exit 2，尚无可执行模型入口。

这比上一版“独立仓完全不知道 Stage‑3”有实质进步。

### C-4 — Experiment asset graph 已扩展为 carrier-aware

`wiki/Experiment-Assets.md` 当前同时定义 study 与 paper authority，并为正式实验记录增加：

- carrier type；
- carrier repository exact commit；
- split role；
- split identity hash；
- consumed；
- shared code revision；
- study admission 与 paper promotion 两类 transaction。

同时 `experiment-asset-inventory-v3` 绑定 study registry 与 paper registry 的 SHA-256，解决了上一轮
paper registry 游离于资产图之外的问题。

## 5. Findings

### P1-1 — MAJOR / CURRENT-TRUTH BLOCKER：默认 AI 指南仍把技术创新写成“在 Stage‑2B 验证”

#### 证据

`AGENTS.md:132-135` 与镜像的 `CLAUDE.md:132-135` 仍写：

```text
technical-approach innovation converges only in reproduction-first Stage-2A
and is validated in Stage-2B.
```

但 canonical `wiki/Research-Methodology.md:27-28` 已明确：

```text
Stage-2B 收敛为合格 paper candidate，最终在 Stage-3 paper 仓的
pre-registered confirmatory 中验证。
```

`wiki/Research-Objective.md:23-24` 与 `wiki/Experiment-Assets.md:16` 还使用
“Innovation and final method remain Stage‑2A/2B outputs”，如果没有同时说明“final validation and
claim remain Stage‑3”，也容易被解释成旧的两阶段证据模型。

#### 为什么是 major

AGENTS/CLAUDE 是每个新 AI 会话的默认加载面。虽然它们前文已经声明 Stage‑3 载体，research boundary
段落却仍给出“validated in Stage‑2B”的直接指令。执行者可以据此把 Stage‑2B 的 bounded candidate
qualification 扩张为最终技术验证；这正是上一轮 P0-1 想消除的歧义。

当前 `ai_context_surface_check.py` 只验证 placement 表和上下文结构，没有覆盖这条阶段语义，所以所有
context gates 为绿仍无法发现该冲突。

#### 必须修复

统一成不含歧义的三句式，例如：

```text
innovation converges through reproduction-first Stage-2A;
Stage-2B qualifies and freezes a paper candidate with bounded evidence;
final validation and publication-grade claims belong to Stage-3.
```

同步处理 AGENTS/CLAUDE，并把 Research-Objective/Experiment-Assets 的“final method”改成
“candidate method/design”，避免“final method”和“final validation”混用。给 current-truth checker 增加
负向样例，至少禁止默认加载面出现无 Stage‑3 限定的 `validated in Stage-2B`。

### P1-2 — MAJOR / EXECUTION LEDGER BLOCKER：权威合同要求的 exposure 字段没有落到独立 study ledger

#### 证据

自包含合同 `2026-08-04-owner-consolidated-execution-contract.md:96` 规定，study 仓
`docs/exposure-ledger.md` 的正式行必须带：

```text
split role
split identity hash
consumed
```

同一合同 §7 还要求 confirmatory 读取前同时在 experiment ledger 与 exposure ledger 登记 split
identity hash，并保证 inherited exposure 单调不减。

然而独立 study 当前实际表头
`studies/speech-aware-evidence-acquisition/docs/exposure-ledger.md:10-11` 仍是：

```text
date | run/experiment id | model/tool | speech carrier + split |
calls | speech audio seconds | artifacts | notes
```

它没有 `scope`、`execution profile`、`split role`、`split identity hash`、`consumed` 或
`inherited exposure`。现有 study test
`tests/contract/test_exposure_and_gate.py:54-63` 也只断言 date、run id、model/tool、calls 和 audio
seconds 等旧列存在。

Umbrella `study_workspace_check.py:359-367` 检查的不是这个 exposure ledger，而是 umbrella experiment
index；并且它只搜索三个词是否在**全文任意位置**出现，没有解析 `## Ledger` 的真实 Markdown 表头。
当前 index 的说明段落本身已经含这三个词，因此即便从表头删除三列，checker 仍可能通过。现有负向
测试的 fixture 恰好只在表头放这些词，没有覆盖“正文仍有词、表头被删”的真实回归场景。

#### 影响

Phase A′ 的 R4 声称“SAEA 台账增列且 checker 强制”，但实际上只有 umbrella experiment ledger 增列；
每次模型/工具 touch 真正要求预先填写的 study exposure ledger 仍无法表达权威合同字段。第一次读取
结果后再补结构，会破坏“before results are read”和 exposure 单调不减的可审计性。

#### 必须修复

在独立 SAEA repo 中：

1. 给 `docs/exposure-ledger.md` 增加至少
   `execution profile / scope / split role / split identity hash / consumed / inherited exposure`；
2. 明确 `consumed=yes` 的不可逆语义及 model-free touch 的填写规则；
3. study contract test 必须解析目标表头，而不是做全文 substring 搜索；
4. umbrella checker 对 experiment index 也应解析 `## Ledger` 后的第一张表表头；
5. 新增真实回归测试：保留正文中的三个术语，只删除表头列，checker 必须失败；
6. 在两仓修复完成前，把 remediation plan 的 R4 从 complete 改为 partial/open。

该项必须在首个 model/tool touch 或 bounded-X 结果读取前关闭；当前纯 model-free E0 文档与静态检查
可以继续。

### P1-3 — MAJOR / PRE-MODEL BLOCKER：execution-scope guard 只验证自报标签，不验证实际运行语义

#### 证据

`contracts.assert_execution_scope(profile)` 对
`baseline-reproduction` / `bounded-discovery-probe` 只做字符串白名单判断。随后
`FrozenCoreGate.assert_model_touch_allowed(execution_profile)` 只验证该字符串、E0 receipt 与 runtime
receipt。接口没有接收或验证：

- split role；
- split identity hash；
- discovery/confirmatory 状态；
- planned sample/model-call 数；
- planned GPU-hours/audio-seconds；
- run/campaign identity；
- exposure ledger 的预登记记录。

因此一个 production-scale 或 confirmatory run 只要自报为 `bounded-discovery-probe`，当前 gate 就无法
区分。测试证明了“不接受 paper-scale 这个字符串”，却没有证明“paper-scale 行为永远被拒绝”。上一轮
验收标准中要求的“超出 bounded budget”和“confirmatory split 冒充 discovery”也没有测试覆盖。

当前风险尚未转化为越界执行，因为 `scripts/reproduce.sh` 和 `scripts/evaluate.sh` 仍固定 exit 2；但一旦
R0/R1/X entrypoint 开放，单一字符串 guard 就不再是足够的执行边界。

#### 必须修复

在启用第一个 model-facing entrypoint 前，选择以下一种闭环方式：

- 推荐：定义结构化、可哈希的 execution plan/manifest，至少绑定 profile、carrier/split、split role、
  split identity hash、planned calls/GPU-hours/audio、protocol hash、run id 和 exposure row；由 gate 在
  receipt 前校验 manifest；
- 最小替代：保持当前 entrypoint fail closed，并明确把现有函数降级命名为“profile token validator”；
  在真实 runner PR 中将结构化 scope/budget/split gate 作为不可跳过的合并条件。

必须增加以下负向测试：

- `bounded-discovery-probe` + confirmatory split → fail；
- allowed profile + 超合同 call/GPU/audio cap → fail；
- 缺 split identity hash 或 exposure pre-registration → fail；
- profile 与 run manifest/campaign kind 不一致 → fail；
- 任一 paper-scale manifest 即使 profile 字符串伪装为 allowed 值也 fail。

这不是要求现在实现完整 Stage‑3 promotion machinery，而是确保 study 自己不能靠重命名运行来绕过
Stage‑3 边界。

### P2-1 — MINOR：paper/checker 的中英文 onboarding 与路径摘要仍不一致

#### 证据

- English `README.md:51-52` 的 layout 有 `papers/`，中文 `README_CN.md:43-49` 没有；
- English `README.md:72-77` 的 gate 清单含 `paper_workspace_check.py`，中文
  `README_CN.md:64-68` 没有；
- `CONTRIBUTING.md:85` 的 experiment lifecycle route 只列
  `wiki/experiments/<study-slug>/README.md`，没有 paper index；
- `AGENTS.md:44-46` 的 path summary 只列 per-study experiment index，容易把
  “long-lived paper records”误读为 Stage‑3 paper project record；
- `wiki/AI-Collaboration.md` 有 Paper repository registry 行，却没有 Paper experiment index 行。

Repository ownership 本身已经写对，所以这是路由完整性问题，不是架构 blocker。但如果保持现状，
中文入口和 canonical placement 摘要仍会漏跑 gate 或把首个 paper index 放错位置。

#### 建议修复

同步中英文 README 的 layout 与命令清单；把 lifecycle 路由写成：

```text
study: wiki/experiments/<study-slug>/README.md
paper: wiki/experiments/papers/<paper-slug>/README.md
```

如果 AI-Collaboration 增加 Paper experiment index 行，必须与
`ai_context_surface_check.py` 的 `POLICY_ROLE_ORDER`、`POLICY_ROLE_SEMANTICS` 及测试同一事务。

### P2-2 — MINOR：整改计划与 papers README 对“已实现/仍延后”描述互相矛盾

#### 证据

`papers/README.md:20-21` 仍写“workspace checks ... intentionally deferred”，但零状态
`paper_workspace_check.py` 已存在并进入 AGENTS/README 的默认门禁清单。

`docs/superpowers/plans/2026-08-04-three-stage-workspace-remediation.md` 同时存在：

- Phase A′ R3：`paper_workspace_check.py` 已完成；
- Phase B item 2：`paper_workspace_check` 将来“实现”；
- Phase A′ R0：AI-Collaboration 已增 Paper registry 行；
- Phase B item 5：再次写“AI-Collaboration 放置表增 paper 行”；
- Phase A′ R4：声称 exposure 台账与 checker 已完成，但实际只完成 umbrella experiment index。

另外 Phase A′ R3 写“11 项负向测试”，实际是 11 个 test methods，其中 1 个为正常通过用例、10 个为
负向用例。测试覆盖本身足够，但状态报告不应夸大。

#### 建议修复

- `papers/README` 改为“zero-state workspace check 已实现；full promotion/admission-mode check 延后”；
- Phase B item 2 改成“extend zero-state checker to admitted-entry mode”；
- Phase B item 5 若指未来 paper experiment index row，就精确命名；若只指 registry row则删除；
- R4 改为 partial，待 P1-2 关闭后再勾 complete；
- 保持历史 Phase A 叙述，但明确其已被 Phase A′ supersede，不要让“无 checker”看起来仍是 current。

### P2-3 — MINOR：study executable contract 的模块级 authority 注释仍指向已被合并的来源合同

`studies/speech-aware-evidence-acquisition/src/speech_aware_evidence_acquisition/contracts.py:3-5`
仍称工程合同由：

```text
SAEA-OWNER-SPEECH-SCOPE-AND-IDENTITY-2026-08-04
```

冻结。该件现在是 source/history record；当前唯一执行 authority 是
`SAEA-OWNER-CONSOLIDATED-EXECUTION-CONTRACT-2026-08-04`。函数级 execution-scope docstring 已写
consolidated contract，因此行为没有错，但模块入口仍给出旧 authority identity。

建议将模块级注释改为 consolidated record id，并把旧 id 明确标成 inherited source，而不是 current
execution contract。

## 6. 对合理延期项的判定

以下仍未实现，但属于 owner 已明确接受的 Phase B 延期，**不构成本轮缺陷**：

- 非空 paper registry 的完整 entry schema；
- candidate bundle/promotion receipt 双向 Git blob/commit 绑定；
- primary/supporting study graph；
- paper checkout origin/branch/package/namespace 校验；
- `paper_workspace_check --require-installed`；
- program-wide confirmatory reservation ledger；
- study registry v3 lifecycle；
- 首仓 admission runbook、CI 与 synthetic dry run；
- 真实 `papers/<slug>/` child repo 和 GitHub remote。

但延期只在下列条件成立时安全：

1. 当前零状态继续 fail closed；
2. 首个 bounded-X 读结果、第二个共享 carrier study、首个 confirmatory split 物化/读取、任一
   paper-candidate-ready 请求或 owner 启动 paper admission——以最早事件为 Phase B 触发器；
3. 在 program-wide reservation 落地前，study exposure ledger 已能可靠记录 split identity 与 consumed；
4. 任何 paper entry 被加入 registry 前，零状态 checker 必须先扩展，不能临时跳过。

第 3 条目前不成立，因此 P1-2 必须先修。

## 7. 建议整改顺序

### R0 — 修正默认 current truth（umbrella，小事务，立即）

关闭 P1-1：同步 AGENTS/CLAUDE，澄清 Research-Objective/Experiment-Assets 的 candidate method 与 final
validation 区别，增加 current-truth semantic regression test，重建 AI context manifest。

### R1 — 闭合 exposure ledger 接口（study + umbrella，任何结果读取前）

关闭 P1-2：先改独立 study 的 exposure ledger/schema/test，再把 umbrella checker 改为解析真实 ledger
表头；umbrella 最后记录新的 study adoption commit。不能只改 umbrella index。

### R2 — 将 profile token 升级为语义 scope gate（study，第一个 model-facing runner 前）

关闭 P1-3：结构化绑定 split、规模、预算、run identity 与 exposure pre-registration；加入 mislabeled
confirmatory 和 over-budget 负向测试。当前两个 shell entrypoint 在此之前保持 exit 2。

### R3 — 清理 onboarding/plan 漂移（umbrella，可与 R0 合并）

关闭 P2-1/P2-2/P2-3：同步中英文入口、paper index 路由、zero-state/full-check 用词、计划 checkbox 与
contracts 模块 authority 注释。

### R4 — 保持 Phase B 触发器，不提前创建 paper repo

完成 R0–R3 不代表 paper admission 获准。首个真实 candidate 出现时，按当时仓库现状另写 promotion
执行计划，先扩 checker/schema/receipt，再创建独立 paper repo。

## 8. 修复后验收标准

### 8.1 Current truth

- AGENTS/CLAUDE、Research-Objective、Research-Methodology 和 Experiment-Assets 对 Stage‑2B/3 使用
  一致的 candidate-grade/final-validation 语言；
- 默认加载面不再出现无 Stage‑3 限定的“validated in Stage‑2B”；
- 中英文 README 的 repo layout 和 gate 清单一致；
- CONTRIBUTING/AI-Collaboration 能路由 study 与 paper 两类 experiment index。

### 8.2 Exposure

- 独立 study 的正式 exposure row 能记录 scope/profile、split role/hash、consumed、inherited exposure；
- first result read 之前有行，`consumed=yes` 不可逆；
- checker 解析真实表头；正文出现术语不能替代表头字段；
- experiment ledger 与 exposure ledger 可通过 run/experiment id 对齐；
- umbrella registry/index pin 修复后的 study commit。

### 8.3 Execution scope

- model-free profile 不能触发模型；
- baseline/bounded profile 必须绑定结构化 run plan；
- confirmatory split、超预算、缺 split hash、缺 exposure reservation、profile/manifest 不一致均 fail；
- paper-scale 行为不能通过把 profile 写成 `bounded-discovery-probe` 绕过；
- `reproduce.sh`/`evaluate.sh` 只有在该 gate 接入后才可从预 R0 的 exit 2 状态开放。

### 8.4 Paper zero state

- empty registry 继续合法；
- malformed/duplicate-key registry、count drift、stray file、child checkout 继续失败；
- full admission schema 未实现前任何非空 entry 继续失败；
- 不创建 paper placeholder repo，不创建 remote，不 push。

### 8.5 命令门

至少重新通过：

```text
python scripts/checks/code_graph_check.py
python scripts/checks/study_workspace_check.py --require-installed
python scripts/checks/paper_workspace_check.py
python scripts/checks/ai_context_surface_check.py
python scripts/checks/build_ai_context_manifest.py --check
python -m pytest scripts/checks -q

# WSL2 Ubuntu-24.04 + ~/.venvs/speechrl
python scripts/checks/legacy_asset_resolution_check.py --verify-bundles
pytest common/tests -q
cd studies/speech-aware-evidence-acquisition && pytest -q
```

并新增至少四类负向测试：stage truth drift、ledger-header-only mutation、mislabeled confirmatory、
over-budget allowed-profile。

## 9. 本轮独立验证结果

本 review 实际运行结果：

```text
code graph: PASS (24 trusted nodes)
study workspace --require-installed: PASS
paper workspace (zero state): PASS
AI context surface: PASS (0 failures)
AI context manifest: PASS
pytest scripts/checks: 156 passed, 2 skipped, 202 subtests passed
SAEA pytest in WSL2: 76 passed
common/tests in WSL2: 21 passed, 1 skipped
legacy resolution in WSL2: 574 bindings, 0 unresolved, 4 bundle hashes verified
git diff --check: PASS in umbrella and study
```

Windows 直接执行 legacy `--verify-bundles` 会把 `/mnt/e/...` 当作 Windows 路径而失败；按仓库规定在
`wsl -d Ubuntu-24.04` 中运行后通过。这是调用环境约束，不是本轮三阶段整改回归。

现有测试全绿与上述 findings 并不矛盾：

- current truth checker 没有断言 Stage‑2B/3 的关键语义句；
- exposure checker 查的是 umbrella index 全文 token，不是 child exposure ledger 的真实表头；
- execution-scope tests 只验证 profile 字符串，没有结构化 run semantics。

## 10. 给工程团队的最终判定

工程团队已经正确理解了用户所说的三类载体不是普通目录分类，而是研究生命周期的三个阶段：

- umbrella 生产选题与研究方向判断；
- study 生产可复现、可证伪、可晋级的 paper candidates；
- paper 对一个具体 candidate 承担发表级实证与论文交付。

这一点已经进入目录、registry、合同、methodology、paper zero-state gate 和独立 study repo，值得接受。
本轮不应再争论是否需要区分 studies 与 papers，也不应把 paper 合并回 study。

但团队把“新增了 profile guard”和“umbrella index 加了三列”过早等同于“所有 findings 已关闭”。真实
执行链仍有两个断点：study exposure ledger 没有合同字段，profile guard 也没有绑定实际运行规模与
split。再加上默认 AI 指南残留旧 Stage‑2B 验证语义，当前版本还不能签署为完全整改完成。

最终交付判定：

```text
ACCEPT the three-stage repository architecture.
ACCEPT the consolidated SAEA authority and paper zero-state gate.
REOPEN current-truth alignment, exposure ledger enforcement, and semantic scope enforcement.
ALLOW model-free E0 work only.
HOLD the first model-facing run until P1-1/P1-2/P1-3 close.
KEEP full paper promotion machinery deferred; do not create a paper repo yet.
```

建议工程团队完成 R0–R3 后申请一次聚焦式复核。下一轮不需要重新审查全部 574 项 legacy 资产或重做
三阶段设计，只需证明这三条开放接口已经真正 fail closed，并清除 P2 文档漂移。
