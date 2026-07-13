---
title: "Response to Stage-1A Precheck Doctoral Adversarial Review — ACCEPT_WITH_ONE_REASONED_MODIFICATION"
date: 2026-07-14
responds_to:
  path: wiki/2026-07-13-reviewer-precheck-survey-design-and-record-closure-doctoral-review.md
  sha256_git_blob: cd56af0095d06b2e6197572e6e899e53ea460fde6625fe7f2b8a9f9eb0cbb3bf
  committed_at: 25cffa9
evidence_snapshot:              # repo state this response reports on
  umbrella_commit: d3ccae6587e1d46059a9681e2f33f984ae3325bc
  w1_commit: a532da06296681b3bbb30446a6fa285ca5bed508
artifact_snapshot:              # this file; blob hash reproducible via `git show <this-commit>:<path> | sha256sum` after commit
  path: wiki/2026-07-14-response-to-precheck-doctoral-review.md
stance: "ACCEPT_WITH_ONE_REASONED_MODIFICATION（唯一 modification = 反对把 scope 塌缩到 ASR）"
not_requested: "record-closure sign-off（接受未闭合）；Stage-1B 放行；Stage-1C 收官；新颖性确认"
verification: "协调者本人核验；本文机读块入库前 PyYAML schema 验证；发布前敌意自检"
---

# Response to Stage-1A Precheck Doctoral Review

## 0. 总立场

**ACCEPT_WITH_ONE_REASONED_MODIFICATION。** 退回裁定接受;不申请 record-closure 签署、不请求
Stage-1B 放行。审查的记录类、方法类、措辞收窄发现**全部接受并多数已落地**;唯一保留意见是审查
把 scope 收窄到 ASR(§2)——这一条我们以核验证据反制,而非抗辩。FFP 未成立、QRP 中——接受,并
逐条对照升级触发条件说明均未触发(§6)。

## 1. 记录类 P0 —— 已兑现(证据在库)

| 项 | 处置 | 证据 |
|---|---|---|
| P0-REC-1（snapshot 混写回归） | **CLOSED** | `2026-07-13-precheck-provenance-correction.md`：evidence/artifact 快照拆分 + canonical git-blob 哈希 `8a1ec913…`，全 40-char SHA。提交 `14943f1` |
| P0-REC-2（五处未声明规范化） | **CLOSED** | correction §3 标题撤销"无内容变更"；新增 §3a `status_field_normalizations` 表,五处 raw 逐字保全 + rule。提交 `14943f1` |
| P0-SURV-1（57/44 无 ledger） | **CLOSED** | `wiki/survey/2026-07-13-scout-ledger-round1.json`：从 workflow journal 重建,8族/57条/**46**独立;dedup 规则可复现,查询日志局限已如实登记。提交 `14943f1` |
| P0-SURV-3（I4 措辞降级） | **CLOSED** | 续34 + `Research-Objective.md`：broad_claim=KILLED / narrow_joint=PLAUSIBLE_NOT_VERIFIED。提交 `d3ccae6` |

**诚实自陈**:提交前敌意自检(`wf_a7603edd`)抓出我自己重建 ledger 里的 off-by-one(unique 47→**46**;
Whispering LLaMA 2310.06434 跨两族,旧 dedup 键只挖 url 里的 arxiv id,漏了 venue_year 里的)——**在提交前
被自己拦下、当场修**,不是又让外审抓。这正是审查希望我们建立的质量控制。同轮再检又抓到我修复文本里一处
新小错(F-S6 "仅大小写" vs 实为"大小写+分隔"),亦已改。

## 2. 唯一保留意见:反对把 scope 塌缩到 ASR(reasoned modification,非抗辩)

**接受的部分(轴 A,措辞)**:I4 的横扫式新颖性主张("没人拿供给当设计轴")已死——contextual ASR/
RAG/oracle-context 早把供给当轴。措辞已降级。

**反制的部分(轴 B,研究范围)**:审查列的击杀器与 P-A~P-G 原型、Survey v2 三新族**几乎全在 ASR**。
若顺此收窄,整个研究塌缩到 ASR 一个任务,丢掉本项目横跨 28 数据集 + 冻结 **omni**(非 ASR)核心的存在
理由。核验证据(承重,已按审查 §10 逐条核对):§10.1–10.5 的语音击杀器落在 **ASR(及 ASR+ST,如 Jinnai
2510.19471)**;§10.6–10.7(Huang/Snell test-time compute、selective-QA/conformal)是文本/QA。§10 里唯一的
非 ASR 音频源是 **MILS(2501.18096)**——审查自己标注其为"训练-free 多模态生成/评分…**不是同构 ASR
selector**",它做的是音频字幕的 generate-and-score,**不是固定 K 池上的选择/兑现问题**。因此,**§10 没有
一条把 SER / SLU-intent / spoken-QA 作为选择(兑现率)问题处理,也没有一条把 label-free 选择算子放到冻结
omni〔模型 × 任务〕兑现面上**。故审查"I2/I4 已被占据"**只在 ASR(及 ASR-邻接)单元格成立**,SER/SLU/
spoken-QA/跨矩阵兑现面这些格仍空。

**据此的研究对象(续34 锁定)**:一个 label-free、供给条件的选择算子在冻结 omni〔模型 × 任务〕矩阵上的
**兑现面(ρ(c)/H(c)/regret)**;ASR 是一行,广度是护城河。**这加强而非削弱审查的严格性**:审查的 P-F
"伪统一"攻击我们照单接受为守卫——**共享对象=算子+H(c) 记账法,各任务各留 U/SESOI,度量同一算子在每格的
ρ(c)**;"击杀器是否跨任务迁移"设为 Survey v2 一等轴(ASR 击杀器不迁移 → 广度对象未被占据的证据)。

**对 Survey v2 设计的影响**:审查要求的三新族(候选池构造 / 上下文供给 / selective-prediction)**每一族
都必须跨任务矩阵扫**,而非默认 ASR;每个 direct-killer 标注其覆盖的〔任务 × 模型〕单元格。

## 3. Q1–Q6 逐条处置(机读)

```yaml
question_dispositions:
  - q: Q1_family_completeness
    disposition: ACCEPT_WITH_MODIFICATION
    action: "加候选池构造/上下文供给/selective-prediction 三新族、拆 selection≠revision（全接受）；MODIFICATION=三新族每族跨任务矩阵扫，不默认 ASR"
  - q: Q2_kill_assignment
    disposition: ACCEPT
    action: "按审查最小击杀矩阵强化 I1–I4 direct killers；补 matched-information/matched-cost 条件"
  - q: Q3_i4_whitespace
    disposition: ACCEPT
    action: "broad_claim=KILLED / narrow_joint=PLAUSIBLE_NOT_VERIFIED / priority=HIGH_FOR_SURVEY_NOT_SELECTED（已落 续34+Research-Objective.md）；narrow 对象重述为跨矩阵兑现面（§2）"
  - q: Q4_survey_priority
    disposition: ACCEPT_WITH_MODIFICATION
    action: "采纳审查重排优先序；MODIFICATION=每优先项加'跨任务迁移'检验；Jinnai-MBR 等已核验条目在 ledger 逐条标证据等级，不整批降级"
  - q: Q5_corpus_gap
    disposition: ACCEPT
    action: "SCOPE_NOW_RUN_LATER：Stage-1A 交付 domain×failure-mode×dataset 纸面映射并即时限定 claim 边界；会话/电话/会议域缺口如实登记（暂无 WSJ/AMI/SWBD/CHiME/TED-LIUM 在盘）"
  - q: Q6_record_closure
    disposition: ACCEPT
    action: "接受 PARTIALLY_VERIFIED_NOT_CLOSED；不签 closure；§1 记录 P0 已把可签部分兑现，snapshot/五规范化/ledger 三项已修"
```

## 4. 强制整改与门槛 —— 状态

```yaml
mandatory_before_next_survey_conclusion:
  P0-REC-1: DONE            # 14943f1
  P0-REC-2: DONE            # 14943f1
  P0-SURV-1: DONE           # 14943f1（46 unique，非 47）
  P0-SURV-2: SCHEDULED_NEXT # taxonomy 重构 + ~46 篇按 ontology v2 重映射（Survey v2 设计紧接本 response）
  P0-SURV-3: DONE           # d3ccae6（含 §2 的跨矩阵重述）
P1_before_stage1c:
  status: PENDING
  items: [direct_killer_matrix_per_I, i4_supply_vs_selector_decomposition, budget_fairness_design,
          domain_scope_map, i2_audio_ablation_evaluator_independence_protocol,
          i3_risk_coverage_conformal_deferral, per_candidate_kill_pivot_proceed_dossier]
P2_stage1b:
  status: NOT_REQUESTED_NOT_AUTHORIZED   # owner 显式放行为前置；放行前置=survey 覆盖门 + 诚信核查 C1–C5
```

## 5. 候选身份状态(接受审查裁定 + 覆盖重述)

| 候选 | 审查裁定 | 我方（接受 + 覆盖重述） |
|---|---|---|
| I1 一般 selector | NEAR_KILLED_COMPLETE_AUDIT | 接受;机制近死,仅作跨矩阵 ρ(c) 结果存活 |
| I2 音频接地 | OCCUPIED_REQUIRES_NARROWING | 接受;**ASR 格**被 READ 占,MILS(非 ASR、generate-and-score 音频字幕)施压 broad-I2 但非选择击杀器;SER/audio-understanding 作为**选择**问题未验;窄=omni 自有信号+δ_corr |
| I3 约束/弃权/Goodhart | PLAUSIBLE_MECHANISM_NOT_NOVEL_BY_GUARDS | 接受;守卫不新,可能新意在语音+可验证奖励+跨任务的 Goodhart 检测对象 |
| I4 跨矩阵兑现面 | BROAD_KILLED_NARROW_PLAUSIBLE | 接受 broad 死;narrow=跨〔模型×任务〕矩阵兑现面(§2),survey 高优先、**不选** |

## 6. 诚信

接受 `FFP=NOT_ESTABLISHED / QRP_CONTROL_RISK=MODERATE / intent_to_deceive=NO_EVIDENCE`。逐条对照审查 §6.3
升级触发条件,声明**均未触发**:57/46 ledger 已可重建提交(非撤回);无删除失败尝试(scout journal 全留);
+0.517 泄漏数字已撤引且未复用;canonical hash 可重算(git blob 正典,manifest 已重建);无 gold 进入 selector
路径;全程 append-only correction,无覆盖旧文档。质量控制的改进证据:提交前敌意自检拦下我自己的 off-by-one。

## 7. 本 response 的 provenance(canonical)

见 frontmatter 三元组:`responds_to`(审查文件 blob `cd56af00…` @`25cffa9`)/ `evidence_snapshot`
(umbrella `d3ccae6…` / W1 `a532da0…`)/ `artifact_snapshot`(本文件,blob 哈希提交后经
`git show <commit>:<path> | sha256sum` 可复算)。单一 `snapshot` 字段已弃用(P0-REC-1 纪律)。

## 8. 请求

请 reviewer 就 **§2 的唯一 reasoned modification**(研究对象=跨矩阵兑现面、Survey v2 三新族跨任务扫、
击杀器跨任务迁移设一等轴)确认或校正。其余全部接受;Survey v2 设计紧随本 response,P1 dossier 与 Stage-1C
收官包为后续。**不申请任何签署。**
