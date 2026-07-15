---
response_id: SURVEY-RESP-2026-07-14-03
title: P0-R 整改进展评审稿（提交 reviewer 重新裁决；round-2 与 1B 在裁决前挂起）
date: 2026-07-14
responds_to_review: "wiki/2026-07-14-survey-v2-p0-remediation-response-doctoral-adversarial-rereview.md @ commit 7079956（verdict RETURN_FOR_MAJOR_REVISION / required_next_state P0_REMEDIATION_IN_PROGRESS）"
survey_snapshot:
  repository: exploring-l4-intelligence (umbrella)
  commit: 78d048550080bb3131b3d1db9646ff4dfbf0c0f0
  dirty_worktree: "本稿与三份 round-1 存档件的 supersession banner（决策包/kill 矩阵/邻居矩阵，原文一字未改）同一 commit 提交；§1 哈希在 78d0485 计算，对应文件其后未改动"
stage: Stage-1A（收尾整改段）
stage_claim: ROUND1_SCOUT_COMPLETE + P0_REMEDIATION_IN_PROGRESS
generated_by: "Claude Fable 5 主会话；构建=census/ledger 两工作流（wf_d851964f 9 agents / wf_999d1d80 10 agents）+ 协调者亲验；各新工件提交前分别过敌意预检（发现/修复计数登记于各 commit message，可 git log 核验；对外评审的核验证据存档 docs/checks/2026-07-14-*.json）"
verified_by: "机械层=协调者亲验（校验器亲跑、抽查行、哈希重算）；科学双审与独立盲审=未完成（如实列于 §5 blockers）"
owner_adjudications_of_record:
  - "续40：阶段排序 1A→1B→1C；四探针全包（签批后开机——尚未签批，GPU 零运行）"
  - "续41：身份合同+same-selector contract 冻结签核（治理裁决，非审计签署）"
  - "2026-07-14：在继续 round-2/1B 之前先提交本评审稿——两线挂起待 reviewer 裁决"
owner_decision_requested: false
stage1b_authorized: false
---

# P0-R 整改进展评审稿

> 提交目的：再复审要求的 required_next_state = P0_REMEDIATION_IN_PROGRESS 已推进到本稿状态。
> 请 reviewer 重新裁决 P0 闭环计分、裁决四处抗辩、并**在执行前**预审两份预注册协议——
> 这是最便宜的审查点。round-2 检索与 1B 探针在裁决返回前不启动。

## 0. 一页状态（逐项，不聚合）

```text
P0-R1 状态/签署纠偏      申报 CLOSED   （撤回聚合上标;integrity_reviewer=PENDING;owner 裁决单列）
P0-R2 canonical census   申报 ADVANCED （census v1 单遍 AI：94 簇→92 RESOLVED/2 AMBIGUOUS/0 UNRESOLVED,
                                        36 versions pinned;ID 载体零碰撞〔82 arXiv/11 DOI 全 distinct;
                                        无 ID 条目仅单遍观察,非保证〕;人工双审待做——请 reviewer 裁定
                                        CLOSED 还需什么）
P0-R3 真 claim 台账      申报 ADVANCED （44 承重行:35 全文定位/7 摘要/2 不可达;43 条 discrepancy=
                                        对自己的候选更正;非承重宽度记录与人工双审待做）
P0-R4 三线分签           申报 CLOSED   （字节线=INTERNAL_BUILD_CONSISTENCY_12/12 亲跑;文献线/claim 线
                                        在 RESP-02 时点如实签 NOT_REACHED,现状已推进为 SINGLE_PASS_AI
                                        ——两时点状态见 §6,分签机制本身即申报对象）
P0-R5 最强结论 token     申报 CLOSED   （按身份索引表+记录集钉定+强制伴随 token;热层与新文档已停用
                                        全局 token;三份 round-1 存档件〔决策包/kill 矩阵/邻居矩阵〕
                                        已加带日期 supersession banner,原文一字未改）
P0-R6 身份量词/post-hoc  申报 CLOSED   （合同 FROZEN@dce5c79,owner 签核;strict-I2 标 post_hoc_created_at;
                                        post-hoc 日志含预置行;合取量词规则明文）
P0-R7 同类错误普查       申报 PARTIAL  （44 承重行的算子×verifier 普查完成;全记录普查排 round-2）
P0-R8 repo 级状态门      申报 NOT_DONE （排期在 round-2 序列内,未开工——不虚报）
```

## 1. 自再复审以来的新工件（正典锚 @ commit 78d0485）

| 工件 | blob sha256 前 16 位 | 内容 |
|---|---|---|
| RESP-02 逐条回应 | `c89649ef33dcec8f` | 六项 QRP 指控承认+四处有据抗辩（§4，待裁决） |
| 身份合同 v1（FROZEN） | `1338f6b16f540902` | 六身份完整三结局判据+合取量词规则+same-selector contract+post-hoc 日志；owner 签核（治理裁决） |
| 1B 四探针协议 v1 | `cd1f8bfe6e050533` | 预注册；池共享硬规定；kill/pivot 与合同逐字对齐；预声明切点；**未签批未开机** |
| round-2 检索协议 v1 | `f0274e579170da94` | 预注册；五枚举事件+raw capture 硬约束；**未执行任何查询** |
| canonical census v1 | `4be50fa0be4d918b` / `f7d3856e46ef8bed` | 92/2/0 分列；P-0016 误并簇、P-0084 双候选如实登记 |
| claim 台账 v1 | `4ca1d16da804567d` / `18e2a48711260a4f` | 44 行+算子普查+43 discrepancy 全列 |
| C1/C4 诚信普查 | `a3999861674b500e` / `4ae58ae3f320f340` / `4352c0c4836caf15` | C1 补登 E 盘运行树+MLflow；C4 台账 29 行；config-selection 轨迹=永久缺口如实登记 |

## 2. 对再复审 §9 unresolved_blockers 的逐项现状

| blocker（再复审原文） | 现状 |
|---|---|
| canonical scholarly identity and version census absent | census v1 done（单遍 AI+协调者抽查）；36/94 versions pinned；双审待做 |
| round-1 search result universe … permanently unavailable | 维持 RAW_EVENT_UNAVAILABLE（不可救，已如实签 REPLAY_FAILED(search-replay)） |
| real claim-evidence ledger absent | v1 done：44 承重行带 verbatim quote+locator+operator 分类 |
| load-bearing human double review absent | **仍缺**——owner 双审包排 E2；本稿不虚报 |
| identity contract and post-hoc log not frozen | FROZEN@dce5c79，owner 签核，日志含预置行 |
| repo-level state gate not demonstrated | **仍缺**——P0-R8 排期未开工 |
| independent blind scientific review absent | **仍缺**——排 E2 |
| integrity_reviewer attribution requires correction or explicit exact-hash owner signature | 已按前一分支纠正（PENDING+owner 裁决单列；合同签核亦按治理裁决记录，未采 exact-hash 签名分支） |

## 3. 台账对我们自己的更正（43 条 discrepancy 的承重样本——证明环路在工作）

KIT 2606.04730：我方 ST oracle 误写 +2.0（实为 **+6.11**）；且其 label-free 兑现在 SQA(−11.06/−3.33)
与 SSUM(−8.60/−2.19) 为**负**、仅 ASR 正兑现（77.6%/60.0%）——我方原「fraction realized across 4
speech tasks」框架高估了一个以负值为主的结果。JudgeBoN Recovery 锚=池均值（只 formalize rho_pool，
非 rho_greedy）。ernez「80%」=置信水平非覆盖率、集合预测非单输出选择器。MBR ~31%=LibriSpeech
特定（ReazonSpeech ~9%）。audio-mind Goodhart cliff 系 n=6。（全表：ledger_report.md）

## 4. 请 reviewer 裁决的四件事

1. **P0 闭环重计分**：按 §0 申报逐项裁定（尤其 R2/R3 从 PARTIAL 升格还差什么——我们不自行升格）。
2. **RESP-02 §4 四处抗辩**：跨轮移动球门（WITHIN_LOGGED_SCOPE 系初审处方，亲验）；P0-3 永久性
   与 P0-2 逻辑一致性；Round 6/7/8 修辞与裁定脱节；全局 token 逻辑洞（已建设性修复为身份索引表）。
3. **两份协议的执行前预审**：探针协议（含 kill/pivot 判读、预声明切点、C-T7 防线、池共享）与
   round-2 协议（五枚举、raw capture、停止规则）——发现缺陷此刻改，成本最低。
4. **P-0084/P-0016 处置确认**：KIT 双候选已由台账数字对齐解至 2606.04730（可接受？）；P-0016
   误并簇拆分方案（拆两 work）确认。

## 5. 如实声明（本稿不含的东西）

round-2 检索未跑一条查询；1B 探针零 GPU 运行（协议未签批）；人工双审、独立盲审、repo 状态门
均未完成；census/ledger 均为单遍 AI + 协调者抽查级；全部数字 directional-only/hypothesis-grade；
Stage-1B/1C 均不请求。

## 6. 三线分签（现状）

```yaml
build_reproducibility: { verdict: "INTERNAL_BUILD_CONSISTENCY_12/12（bundle）;census/ledger 行数与分布协调者亲验", by: "coordinator", date: "2026-07-14" }
bibliographic_audit: { verdict: "CENSUS_V1_SINGLE_PASS_AI（92/2/0 分列;双审待做）", by: null, date: null }
scientific_claim_audit: { verdict: "CLAIM_LEDGER_V1_SINGLE_PASS_AI（44 行;kills 方向性维持;双审待做）", by: null, date: null }
independent_reviewer: PENDING
integrity_reviewer: PENDING
maximum_permitted_claims: "RESP-02 §3.3 按身份索引表（全局 token 停用）"
```
