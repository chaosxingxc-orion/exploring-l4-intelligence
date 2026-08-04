# Three-Stage Workspace Remediation Plan (minimal-first, owner-trimmed)

**Goal:** 把 Stage‑3（大规模实证与发表）的使命从 study 仓的默认授权中移出，并以最小占位面立起
`umbrella → studies → papers` 三阶段载体架构；一切机器件推迟到真实内容出现。

**Ruling:** Owner 2026-08-04（Decision-Log-2026-08 续91）：三层载体即既有 Stage‑1/2/3 的载体绑定；
"缓着来，先把架构搭起来，没有到填内容之前不要过度设计"。评审依据：
`docs/superpowers/specs/2026-08-04-three-stage-architecture-critique-and-decision-request.md`
（该文对 GPT-5.6 原提案的接受/否决/重排序裁决全部生效）。

## Phase A — 已执行（2026-08-04）

- [x] Decision-Log-2026-08 追加续91 ADR：载体绑定、`OWNER_GO_AND_PAPER_EXECUTION_CONTRACT`
  token 冻结、paper 成功判据（正/零/负同等合法）、最小实施与延后清单、评审否决项维持。
- [x] 概念层 HOT 更新：`Project-Thesis`（repo 模型表 + study 终点句）、`Architecture`
  （目录树 + 三阶段 pipeline + 中英节奏句）、`Research-Objective`（载体绑定句，4994/5120B）、
  `CLAUDE.md`/`AGENTS.md`（伞仓所有面 + 节奏句，镜像一致，8558/8545B ≤12KB）、
  `Experiment-Assets`（Paper project registry 小节，admitted **0**）。
- [x] papers 占位面：`papers/README.md`（promotion rule + 空 registry 合法/空仓非法 + 延后声明）、
  `papers/registry.json`（`paper-repository-registry-v1`，`papers: []`）、`.gitignore` 加
  `papers/*/`。**无 checker**——机器校验随首个 admission 落地。
- [x] SAEA Stage‑3 边界合同：
  `wiki/experiments/speech-aware-evidence-acquisition/2026-08-04-owner-stage3-boundary-and-paper-gate-contract.md`
  （保留 E0/R0/R1/bounded X；study 终点=qualified paper candidate；paper-scale 默认禁止；
  历史 exposure/预算不回写）；实验索引路由与 front matter 更新；`studies/registry.json`
  decision_record re-pin（blob `5f91226f25d6bfd5c5cd427c57fecc635eb43066`）；
  `experiment-asset-inventory.json` 重渲染；AI context manifest 重建。
- [x] 验证：五道伞仓门禁 PASS；`pytest scripts/checks` 143 passed/2 skipped；
  WSL `pytest common/tests` 21 passed/1 skipped。

## Phase A′ — 实施 review 整改（2026-08-04，续92；review：specs/2026-08-04-three-stage-architecture-implementation-review-assessment.md）

- [x] **R0 当前真相全面替换**（P0-1/P1-3/P2-1/P2-2）：Research-Methodology Stage‑2B/3 重定义；
  README/README_CN/CONTRIBUTING(+CN)/docs/architecture/wiki-Architecture/客户端指南旧
  "全部工作留 study"句全部替换；Per-Work-Status 停止线；Experiment-Assets carrier 化
  （carrier type/split role/split identity hash/consumed）；AI-Collaboration 增 Paper registry 行
  + surface-check 常量与测试同 commit；proposal/评审件裁决 banner。
- [x] **R1 自包含权威**（P1-1，评审选项 A）：`2026-08-04-owner-consolidated-execution-contract.md`
  合并 GO+身份+范围+预算+execution scope+Stage‑3 停止线+来源 blob 表；registry/index/HOT 全部
  re-pin（blob `8ddd0cf2a96908befc8b49e69602185729ba17ba`）。
- [x] **R2 独立 study 仓采用**（P0-2）：study commit `6c4b37e9ff90becde3df934fa2b87e136f1354eb`
  ——指南/README/engineering 路由新合同；`contracts.assert_execution_scope` fail-closed（仅
  model-free-check/baseline-reproduction/bounded-discovery-probe；paper-scale 永拒）；
  `FrozenCoreGate.assert_model_touch_allowed(execution_profile)` 必须声明 profile；76 项测试绿。
- [x] **R3 零状态 paper 门**（P1-2）：`paper_workspace_check.py`（严格空 registry/零 child/
  ignore 规则/计数一致；任何 paper 条目 fail closed）+ 11 项负向测试；inventory 升 v3 纳入
  paper registry sha256。
- [x] **R4 exposure 最小前置**（P1-4）：SAEA 台账增 split role/split identity hash/consumed 列，
  checker 强制（REQUIRED_LEDGER_COLUMNS + CONTROL_PLANE_TERMS）；reservation 台账触发器改为
  四事件最早者（首个 bounded X 读 discovery 前 / 第二个共享 carrier study 前 / 首个
  confirmatory split 物化或读取前 / 任一 candidate 申请 paper-candidate-ready 前）。

## Phase B — 延后（触发器已按续92修订：下列四事件最早者，或 owner 启动首个 paper admission——首个 bounded X 读取 discovery 结果前 / 第二个共享 carrier study 前 / 首个 confirmatory split 物化或读取前 / 任一 candidate 申请 paper-candidate-ready 前）

到触发时**按彼时仓库现状另写执行计划**（细节届时重新设计，本节只固定验收语义与已裁决的约束，
防止降覆盖）：

1. **Promotion schema**（candidate bundle + promotion receipt）：BLOCKER/RECOMMENDED 分级
  （评审 C8）；bundle 冻结为 study 仓 Git blob，umbrella receipt 双向绑定 paper initial commit。
2. **paper_workspace_check**：从 `study_workspace_check.py` 提取共享验证器后实现（评审确认可行）；
  空 registry 合法、未登记目录 fail、candidate token 禁入 slug/package/namespace、
  primary_study 必须解析、读 child 内容的校验门控在 `--require-installed`（评审 C4）。
3. **Program-wide confirmatory reservation ledger**：`docs/integrity/` 下机器台账 + fail-closed
  checker；生效点在任何 confirmatory 读取之前（评审 C2）。在此之前由边界合同 + study 仓
  `docs/exposure-ledger.md` + 2026-08-03 程序可见性纪律（split-hash/已消耗标记）承担。
4. **study registry v3**：超集 lifecycle 词表（新增 candidate-development/paper-candidate-ready）+
  provenance 字段；registry+checker+tests 单事务（评审 C3）。
5. **AI-Collaboration 放置表增 paper 行**：必须与 `ai_context_surface_check.py` 的
  `POLICY_ROLE_ORDER`/`POLICY_ROLE_SEMANTICS` 常量及测试同 commit（评审 C10）。
6. **首仓 admission runbook**：语义命名、远程创建显式授权、六步非原子晋级事务、初始 CI、
  `docs/checks/promotion-<paper-slug>/<release-id>/` 收据、合成 dry-run 的 fail-closed 用例。

## 永久约束（已裁决，不随 Phase B 重开）

- 不重组 `wiki/experiments/` 与 `docs/checks/` 既有路径（grandfather，评审 C1）；
- 不建 `wiki/directions/`；study gate 保留 `OWNER_GO_AND_EXECUTION_CONTRACT`（评审 C5/C6）；
- `wiki/` 下新文件 basename 禁用 `AUDIT_NAME_RE` token（amendment/proposal/review/…，评审 C9）；
- 伞仓不规定 study/paper 仓内部布局，只经合同约定接口（评审 C7）；
- paper 成功不以正提升为条件；HARKing 防线（预注册、confirmatory 未读、exposure 单调）不可弱化。
