---
title: "三阶段架构提案对抗评审与裁决请求"
date: "2026-08-04"
review_target: "docs/superpowers/specs/2026-08-04-umbrella-studies-papers-three-stage-architecture-remediation-proposal.md"
review_method: "multi-round adversarial analysis grounded in repository facts"
verdict: "ACCEPT_CORE_SEMANTICS__REJECT_PATH_RESTRUCTURING__RESEQUENCE_IMPLEMENTATION"
adjudication_status: "ADJUDICATED__OWNER_ACCEPTED_WITH_MINIMAL_FIRST_TRIM__DECISION_LOG_XU91_XU92"
execution_authority: "DOCUMENTATION_ONLY__NO_NEW_AUTHORITY"
companion_plan: "docs/superpowers/plans/2026-08-04-three-stage-workspace-remediation.md"
---

# 三阶段架构提案对抗评审与裁决请求

评审对象是 2026-08-04 的《Umbrella → Studies → Papers 三阶段研究工程架构整改提案》
（下称"提案"）。评审方法：先以最强火力攻击其必要性（第 1 轮），再做最强辩护（第 2 轮），
然后用仓库的机器事实逐条检验双方论点（第 3 轮），最后给出裁决与修订（第 4 轮）。
所有事实断言均带出处，可用 `rg` 复核。

## 0. 裁决摘要

**接受**：三阶段载体语义、两道独立 gate、"晋级 = 证据交易"、§4 科学完整性原则全部、
平铺拓扑、独立 registry。

**否决**：一切既有路径重组（`wiki/experiments/`、`docs/checks/` 保持原状）；
`wiki/directions/` 目录层；study gate token 改名；把仓内布局（提案 §8.2/§8.3）当规范。

**重排序**：confirmatory reservation / exposure 台账从"paper 晋级件"提前为 **Stage-2 前置**；
promotion checker 与 dry-run 推迟到 SAEA 出现真实 candidate（触发器化）。

**机器事实一票否决项**（提案按字面实施会直接 FAIL 现有门禁，见 C9/C10）：
"dated amendment" 命名放 `wiki/experiments/` 会触发 `new-audit-artifact-outside-audit-root`；
改 AI-Collaboration 放置表而不同步 `ai_context_surface_check.py` 常量会 FAIL。

## 1. 第 1 轮 — 控方：必要性攻击

- **A1（规模失配 / YAGNI）**。程序现状：1 个 owner、1 个 admitted study、**0 条正式实验**
  （`wiki/experiments/speech-aware-evidence-acquisition/README.md` ledger 为空，E0 尚未关闭）。
  提案要求：第二套 registry、第二道 gate、20 字段晋级包、≥3 个新 checker、2 套新测试。
  程序的真实瓶颈是 E0 D1–D4，而不是缺 papers 目录。治理/研究工时比已经极高，
  每一小时花在 schema 上都是从 E0 挪走的。
- **A2（问题是假想的）**。提案 §2.1 的核心恐惧——"第二篇论文出现时 exposure/release 互相
  污染"——发生条件是存在第一篇论文。今天不存在。当下**真实**存在的缺口只有一个：
  SAEA 的 Stage-2A 合同（E0→R0→R1→X）没有 paper-scale 停止线。修一个缺口用一页合同就够，
  不需要一套架构。
- **A3（现有机制已可泛化）**。"语义命名独立仓 + owner GO + 执行合同 + registry 登记"这套
  admission 机制是通用的。真到了要建论文仓的那天，按同一机制再走一遍即可；为什么要预先
  建平行的根目录和 registry？
- **A4（捆绑谬误）**。提案把两样东西捆在一起卖：科学完整性机制（exposure 继承、confirmatory
  reservation、负结果合法）和载体架构（papers/ 根、双 registry）。前者与目录结构**正交**且
  更紧迫——SAEA 的 X 阶段就要读 discovery 数据了；后者可以等。捆绑销售掩盖了优先级差异。
- **A5（瀑布僵化）**。冻结 20 字段 bundle 才准建仓，假设 candidate 在晋级时刻已经轮廓清晰。
  ML 研究是迭代的；每次回流都要 dated decision，摩擦大到一定程度，执行者（owner+AI）就会
  开始绕台账走——治理过重反而制造违规。

## 2. 第 2 轮 — 辩方：最强辩护

- **D1（零实验时定边界最便宜）**。今天 ledger 为空，是定 stage 边界的历史最低成本点。等
  confirmatory 被读过再回头补边界，污染已不可逆。提案 §11.3 自己也点了这一条。
- **D2（停止线需要命名线外之物）**。A2 说"一页合同就够"，但停止线必须写明"线外是什么、
  归谁、凭什么恢复"。不定义 paper-stage 载体，停止线就只是散文，机器无法查。精确定义
  线外之物，恰恰就是这份提案。
- **D3（本仓的运行模式需要机器门）**。执行主体是 owner + LLM 协作者。本仓自己的历史证明
  散文规则会漂移、机器门不会：G1 教训（commit c9c9f6f "legacy validator now proves bindings,
  not formats"）就是散文声称已证明、机器一查并没有。防 scope-creep 的对象恰恰是 AI 执行者
  自身，所以 fail-closed checker 不是官僚主义，是本仓已验证的防御手段。
- **D4（多 candidate 是明示意图）**。SAEA 研究问题（OBS/ORG/SUPPLY/USE 四轴）天然产出多个
  可分立检验的改进点；owner 在三阶段表述中明确"一个 study 形成一个或多个 paper candidate"。
  单仓混装多论文的风险不是假想，是既定路线的必然后果。
- **D5（混装破坏机器检查）**。A3 说"papers 当作另一个 study 登记就行"——但 study 与 paper
  的 lifecycle 词表、退出门、exposure 语义都不同；塞进同一 registry 会把
  `study_workspace_check.py` 的精确校验（exact-key、lifecycle 白名单）变成两义。平行根目录
  + 平行 registry 反而是**更便宜**的机器可分离方案。
- **D6（20 字段各有对应事故）**。bundle 每个字段都映射一类真实失败（baseline 不可运行、
  exposure 失踪、power 未算、样本重用……）。填表几小时，任一失败类的返工以周计。

## 3. 第 3 轮 — 控方反击：仓库机器事实检验

辩方赢了"要不要"（D1–D3 成立），但提案的"怎么做"在仓库事实面前多处失守：

- **C1（路径重组是净负收益——否决）**。提案 §7 要把实验索引迁到
  `wiki/experiments/studies/<slug>/`、检查收据迁到 `docs/checks/studies|papers|promotions/`。
  事实：① `study_workspace_check.py:148` 硬编码
  `expected_index = f"wiki/experiments/{slug}/README.md"`；② registry v2 对 decision_record
  做 **blob pin**（`_validate_study_entry` 现场重算 sha1 比对）；③ 该路径被 Research-Objective、
  Experiment-Assets、studies/README、CLAUDE.md 至少四处 HOT 引用，搬运要过 AI-Collaboration §4
  五步安全门；④ 现行 `docs/checks/<campaign>/<release-id>/` 本来就是 campaign 泛化的——
  paper 收据用 `docs/checks/<paper-slug>/<release-id>/`、promotion 收据用
  `docs/checks/promotion-<paper-slug>/<release-id>/` 即可，零迁移。路径里表达 stage 毫无必要，
  registry 字段已经表达了。**裁决：全部 grandfather，不迁移任何既有路径。**
- **C2（reservation 台账时空双错位——重排序）**。提案把 confirmatory reservation 放进晋级包
  （Stage-3 入口），但 Stage-2A 合同的 X 阶段就要消费 discovery 数据、R0 就要求"未读
  confirmatory carrier"；而且**两个 study** 共享 Earnings21 时冲突同样发生，根本轮不到 paper。
  另外 §7 拓扑图里 reservation ledger 没有落位——风险表把它当 BLOCKER 缓解，正文却没给它
  一个文件路径。**裁决：程序级台账 `docs/integrity/confirmatory-reservation-ledger.json`
  立即建立，配 fail-closed checker，SAEA 边界合同写入查询义务。**
- **C3（v3 迁移未指定，按字面必炸）**。`study_workspace_check.py:47`
  `ADMITTED_LIFECYCLES = {"engineering", "validation", "paused", "complete", "sunset"}`，
  `:105` 强制 exact-key。提案 v3 词表（`topic-analysis | baseline-qualification | ...`）与现值
  `engineering` 不兼容，且没写映射。**裁决：v3 取超集词表（保留现有五值，新增
  `candidate-development`、`paper-candidate-ready`），SAEA 现值不动；registry+checker+tests
  一个事务落地。**
- **C4（多机降级冲突）**。`--require-installed` 是 primary dev machine 模式（owner 2026-08-03）；
  candidate bundle 若住在 study 仓内，promotion 校验就要读 child 仓内容，在无 checkout 的机器上
  必须降级而非 FAIL。提案 §9.3 未处理。**裁决：一切读 child 内容的校验都门控在
  `--require-installed` 之后，镜像现有 origin/branch 检查的处理。**
- **C5（HOT 预算无记账）**。`wiki/Research-Objective.md` 现为 4763 字节，预算 5120，余量
  **357 字节**；manifest 活动条目 ≤30（`ai_context_surface_check.py:1709` 硬编码）。提案 T6
  说"HOT 只做 compact router"，却没算新增文本要花掉的字节。**裁决：每处 HOT 编辑给出字节
  预算，超预算先裁旧文本。**
- **C6（gate token 改名是纯负债）**。`OWNER_GO_AND_EXECUTION_CONTRACT` 已被 registry fixed-field
  校验（`study_workspace_check.py:28`）、CONTRIBUTING、AI-Collaboration 表、已签合同引用。
  改名为 `OWNER_GO_AND_STUDY_CONTRACT` 要动所有这些且制造新旧双词表。**裁决：study gate
  保留现 token；只新增 `OWNER_GO_AND_PAPER_EXECUTION_CONTRACT`。**
- **C7（越权规定独立仓内部布局）**。提案 §8.2/§8.3 规定 study/paper 仓的 src/docs 目录树。
  CONTRIBUTING 首条纪律是"commit each change to the repo it belongs to"；SAEA 有自己的
  CLAUDE.md 与治理。伞仓可以经由合同要求**接口**（如 exposure ledger 路径、candidate bundle
  路径在 registry 声明），不能规定别仓内部结构。**裁决：§8 降级为非规范模板。**
- **C8（20 字段一刀切）**。字段各有价值（D6 成立）但强度不同。**裁决：分级——13 个 BLOCKER
  字段缺失即拒绝晋级；其余 RECOMMENDED 缺失需 owner 显式豁免。**
- **C9（"amendment"命名触发机器门——提案字面实施必 FAIL）**。
  `ai_context_surface_check.py:81` 的 `AUDIT_NAME_RE` 匹配
  `proposal|amendment|review|report|response|correction|sign-off|adjudication|submission` 等
  basename token；`:1831-1838` 对 `wiki/` 下任何命中该名且不在 `wiki/audit|archive/` 的 `.md`
  报 `new-audit-artifact-outside-audit-root`。提案 §11.3/T3 反复要求的 "dated amendment" 若照
  字面建为 `wiki/experiments/.../*-amendment.md`，surface check 直接 FAIL。现行合法形态就是
  SAEA 已用的 **owner contract 命名**（`...-contract.md`，如 2026-08-04 那份），或走
  `wiki/audit/<campaign>/epoch-N/` 状态机。**裁决：SAEA 收窄件命名为
  `...-owner-study-stage-boundary-and-paper-gate-contract.md`。**
- **C10（AI-Collaboration 放置表被机器钉死）**。`ai_context_surface_check.py:516-539`
  以 `POLICY_TABLE_HEADERS / POLICY_ROLE_ORDER / POLICY_ROLE_SEMANTICS` 硬编码校验放置表的
  行序与语义 token。加 "Paper repository registry" 行必须同一 commit 更新 checker 常量与测试。
  提案 T1 完全没提这层耦合。
- **C11（manifest sha256 pin）**。AI context manifest 的活动条目含 `sha256`（`ENTRY_KEYS`），
  任何 HOT 文件编辑都要求重建 manifest 并过 `build_ai_context_manifest.py --check`。
  实施步骤必须把"编辑 → 重建 → 校验"作为一个事务，提案未写。

同时记录**提案经核验为真**的断言（对抗评审的诚实义务）：§2.2 papers 基础设施为零（属实）；
§9.3 共享验证器可提取（`study_workspace_check.py` 函数划分支持，属实）；§11.3 "尚无正式实验、
迁移成本最低"（ledger 为空，属实）；`.gitignore` 的 `studies/*/` 模式可平移（属实）。

## 4. 第 4 轮 — 裁决综合

| 提案内容 | 裁决 | 依据 |
|---|---|---|
| 三阶段载体语义、两道 gate | **接受** | D1/D2/D4/D5 |
| §4 科学完整性原则（负结果合法、不追正提升、exposure 单调） | **原文照准** | 无有效反驳 |
| 晋级 = 冻结 bundle + 双向 receipt + 六步非原子事务 | **接受** | 与本仓 blob-pin 风格同构 |
| 平铺拓扑、独立 registry、伞仓只跟踪 README+registry | **接受** | D5 |
| `wiki/experiments/`、`docs/checks/` 路径重组 | **否决** | C1 |
| `wiki/directions/` 目录层 | **否决**（registry 留 `direction` 字符串字段） | C5、无 gate 定义 |
| study gate token 改名 | **否决** | C6 |
| §8.2/§8.3 仓内布局 | **降级为非规范模板** | C7 |
| reservation/exposure 台账 | **提前为 Stage-2 前置，落 docs/integrity/** | C2 |
| 20 字段 bundle | **接受但分 BLOCKER/RECOMMENDED** | C8 |
| registry v3 | **接受，超集词表 + 单事务迁移** | C3 |
| "dated amendment" 载体 | **改为 owner contract 命名** | C9 |
| T1–T4 打包立即实施 | **拆分**：裁决+边界合同+台账+最小 papers 面立即；promotion checker/dry-run 挂触发器 | A1/A4 vs D1 的平衡 |

## 5. 对提案 §16 八问的修订答复（请 owner 逐项裁决）

1. 接受 `umbrella → studies → papers` 三阶段载体；但拓扑只新增 `papers/` 根，不重组任何既有路径。
2. 接受 "study 终点 = paper candidate qualified"。
3. 接受 "paper 成功 = 对预注册 claim 作出可靠判断，而非必须正提升"（原文照准）。
4. 接受两道独立 gate；study gate 保留 `OWNER_GO_AND_EXECUTION_CONTRACT`，
   新增 `OWNER_GO_AND_PAPER_EXECUTION_CONTRACT`。
5. 接受 SAEA 保留为 study；收窄件为 dated **owner contract**（命名规避审计 token），
   保留 E0/R0/R1/bounded-X 既有授权与全部历史 exposure 事实。
6. 接受一个 paper 一个 `primary_study`、零到多个 `supporting_studies`。
7. 接受 program-wide confirmatory reservation 与 inherited exposure 硬门，
   且**生效点提前到 Stage-2**（X 阶段之前），台账住 `docs/integrity/`。
8. **改批**：立即实施 = 裁决 ADR + SAEA 边界合同 + reservation 台账 + papers 最小工作面 +
   共享验证器提取 + registry v3 + promotion schema 校验器（无消费者）；
   触发器实施（SAEA 任一 candidate 进入 `paper-candidate-ready`）= promotion graph checker +
   合成 dry-run + 首仓 admission。

实施分解见 companion plan：`docs/superpowers/plans/2026-08-04-three-stage-workspace-remediation.md`。
本文与该 plan 均不授予模型调用、实验、远程建仓、push 或发布权限。
