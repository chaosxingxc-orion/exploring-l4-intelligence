---
title: "Research Objective & Current State — 日常加载的唯一现状入口（热层）"
role: "认知层：现状/研究对象/约束/open items/取代索引的单一极简入口。派生自 Decision-Log（审计层），可重建，非唯一记录。被取代的条目掉出本文件（在 archive/ 与 Decision-Log 里）。"
maintained: "每有取代关系变化即更新本文件；新决策先 append 进 Decision-Log 再反映到此。"
last_refreshed_commit: "self-referential hash unavailable pre-commit; this file's post-commit (commit, blob) triple is recorded in docs/integrity/record-policy-and-attestations.md. Last refresh: 2026-07-14 (续38 survey-v2 MAJOR_REVISION response + P0)."
---

# Research Objective & Current State

> **给读者/agent 的一句话**：默认只读本文件 + `CLAUDE.md`。要某条决策的出处才去 grep
> `Decision-Log.md`（冷档案，勿整篇读）。术语见 CLAUDE.md 术语表。

## 现在在做什么（Stage-1A · 问题界定）

- **阶段**：Stage-1A（广泛 survey / 候选问题 / 原型空间纸面设计 / 风险审查）。**Stage-1B 未放行、M2 冻结**。
- **研究对象（续34 锁定）**：**一个 label-free、供给条件的选择算子,在冻结 omni〔模型 × 任务〕矩阵上的
  兑现面（ρ(c)/H(c)/regret）**。ASR 是其中一行,非全部。**广度定位（续35 校准,reassessment §11.2-E）**：
  `survey_scope=cross_task_cross_model`;`scientific_question_status=candidate_not_selected`;
  `novelty=unverified`;**`breadth=external-validity 维度,不是本身即贡献`——"护城河"是工作假设,非已证新颖性**。
- **伪统一守卫**：共享对象 = 算子 + H(c) 记账法统一;各任务各留效用 U 与 SESOI;度量同一算子在每格的 ρ(c)
  （**cellwise-only,禁止无权重的"总 ρ"平均**）;**部署用 label-free proxy `S`,评估用 `U`,二者不混**。
- **候选身份（Stage-1C 才选,现不选）**：I1 一般 selector（机制近死）/ I2 音频接地（ASR 格被 READ 占;
  MILS 非 ASR、generate-and-score 施压;SER/audio-understanding 作为**选择**问题 UNDERSEARCHED）/
  I3 约束·弃权·Goodhart（对象 OPEN、守卫不新;SER reject-option 等祖先存在）/ **I4 跨矩阵兑现面
  （broad 死、narrow 待验、survey 高优先）**。**非 ASR 格一律 `UNDERSEARCHED`,非"空"（祖先已由 §4.2 举证）。**

## 现在绑定的约束（硬）

- weight-frozen（不改权重/结构）;**信息边界**：test-item gold 不入 selector/reward/prompt/检索/候选构造。
- 证据全 directional-only / hypothesis-grade——**无任何确证宣称**;有头空的 null 才证伪 selector（headroom 归因纪律）。
- **append-only**（改写历史=reviewer 升级触发）;**哈希正典=git blob 字节**;发布前对未提交工作树跑敌意自检、零确认才提交。

## Open items（live）

1. **Survey v2 = ROUND1_SCOUT_COMPLETE（续38 状态纠偏,非"完成/收官"）**：15 敌意 lane /
   SEARCH 218 + FETCH 87（勿再合称"305 查询"）/ **精确 94 篇**（113→110→104→94,`~93` 不可机械重现）。
   博导复审 MAJOR_REVISION 已核验+逐条回应+P0 八项整改：回应
   `2026-07-14-survey-v2-response-and-p0-remediation.md`、replay bundle
   `wiki/survey/replay/SURVEY-RESP-2026-07-14-01/`（历史 raw response 永久缺失=RAW_EVENT_UNAVAILABLE,
   round-1 检索不可重放;12/12 校验 PASS）。**结果（证据级封顶 ABSTRACT_VERIFIED 待双审）**：I1 kill
   方向保持（MBR 更正后更强）;**I4 = NO_DIRECT_MATCH_WITHIN_LOGGED_SCOPE,收窄表述**（scaling-surface
   方法学族已被 text/VLA 占据,空白=供给轴×冻结 omni×label-free 预测律;勿再称"最强空位"）;
   strict-I2（=I2∩I4,已登记术语表）/I3-combined/UMBRELLA 同带限定开放。**决策包 =
   PRE_STAGE1C_DECISION_DRAFT**——owner 已接受门控:P0+P1 关闭、STAGE1C_DECISION_READY 后才提请选题。
   **P1 清单**：9 既有饱和目标 + 8 新篇（bundle `round2_new_targets.jsonl`,含 CoVer 2602.12281=
   Proposal E 最近邻威胁;未来轮次按可回放模板全程捕获 raw response）、identity contract 冻结、
   comparator 重建、C1/C4、独立盲重建。
2. **诚信核查 C1/C4**（Stage-1B 放行前置）：C1 尝试普查（registry vs raw run）、C4 负结果普查。
3. **same-selector contract**（Stage-1C 前）：冻结 operator/score inputs/预算/弃权/gold 边界/池几何,
   跨任务不可固定处显式标 task-specific。
4. **Stage-1C 决策包**：I1–I4 kill/pivot/proceed dossier + 供给收益/selector 收益分解 + 预算公平性 +
   可证伪三结论（proceed/pivot/kill）;**agentic-loop vs 一次性 rerank** 作为开放的 Stage-1C 问题。
5. **知识栈选型 = PARKED（续37）**：外来评审（llm-wiki-compiler 试点提案）经六镜头敌意复核后
   owner 裁决**全部搁置**（含 schema-first）,Stage-1C 收官后按四门复活（时机/顺序/规格/裁决）;
   回应 `2026-07-14-response-to-knowledge-stack-evaluation.md`。其新造代号（T0–T4 信任层、方案 A 等）
   **未登记**,引用须带限定语（勿与 T0–T7 探针编号、survey-v2 评审 Proposal A 混同）。

（已闭/移除：reviewer response 已提交 `0be1285` + 接受 reassessment 的 response-v2;冷热归档已执行
`34024fc`,50 文档入 archive/。）

## 取代索引（什么已死 / 被谁取代 —— 见旧条目勿当现状）

| 旧结论/命名 | 现状 | 出处 |
|---|---|---|
| RDU 为 headline | 降为 secondary/ablation | 续32 |
| `A-SEL` 命名 | 正名「选择器兑现率方向」 | 术语表 / 续33 |
| v4.2 = Stage-2 入口 | Stage-1 问题定义交付物 | 续32 |
| `84c6cf6` proposal 草稿 | PRE_STAGE2_BLUEPRINT（无现时效力） | 续33 |
| 程序代号 `W1-ASEL-S2-001` | 冻结弃用 | 续33 |
| 自家 +0.517（检索供给佐证） | 撤引（C-T7 泄漏 INVALID;干净值 −0.066 null） | 续33·勘误 |
| I4 "最干净 whitespace" | broad 死 / narrow 待验（跨矩阵兑现面） | 续34 |
| scope 收窄到 ASR | 反制:ASR 是一行,研究对象是跨矩阵兑现面（reviewer 已接受 breadth-first） | 续34 / 续35 |
| 全 append-only 大文件当主工作面 | 冷热分离,默认只读本热层 | 续34 |
| "非 ASR 格仍空" | **UNDERSEARCHED**（SER/SLU/ST/AAC 祖先已举证） | 续35 |
| "广度是护城河"（已证贡献） | 工作假设,非已证新颖性;`breadth=external-validity 维度` | 续35 |
| P0-SURV-1 = CLOSED | **PARTIAL**（计数可重建/搜索不可重放/科学覆盖 OPEN） | 续35 |
| response `0be1285` 的"格空/护城河"措辞 | 由 response-v2 dated successor 取代 | 续35 |
| "Survey v2 complete / 调研收官"（续36/233dc7e） | **ROUND1_SCOUT_COMPLETE** | 续38 |
| 决策包"待 owner 选题" | **PRE_STAGE1C_DECISION_DRAFT**（P0+P1 门控后才提请） | 续38 |
| READ "~70-85% oracle" | 更正:Table 1 兑现 7.7–68.5%（LS 仅 12–17%） | 续38·勘误 |
| "~93 papers" | **精确 94**（113→110→104→94;93 不可机械重现） | 续38 |
| I4 "最强空位/strongest differentiator" | 收窄:方法学族邻域已占,空白=供给轴×冻结omni×label-free预测律 | 续38 |
| TAP-GER/ProGRes = kill-I1 DIRECT | 重分类:扩池/改写算子,非池内选择占据 | 续38·勘误 |

## 正典工件指针

- 现状真理：**本文件**。审计真理：`Decision-Log.md`（冷,勿整篇读）、`Per-Work-Status.md`。
- 发布快照：`docs/integrity/release_manifest.json`（git-blob 哈希）+ `docs/checks/manifest-blob-verification-2026-07-13.txt`。
- survey：`wiki/survey/2026-07-13-scout-ledger-round1.json`（8族/57条/46独立,SCOUT 级;**计数可重建,
  raw-query 重放 OPEN,科学覆盖 OPEN**）;Survey v2 产物 `wiki/survey/2026-07-14-*`（生成中）。
- 记录政策/attestation：`docs/integrity/record-policy-and-attestations.md`（冷热分层 + provenance 三元组不变量）。
- 规则/术语：`CLAUDE.md` / `AGENTS.md`（镜像）。
