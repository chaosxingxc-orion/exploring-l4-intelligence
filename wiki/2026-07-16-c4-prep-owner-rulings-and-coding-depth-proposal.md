---
title: "Correction #4 预备：owner 三裁决 + 编码深度优化提案（讨论纪要）"
date: 2026-07-16
status: "WORKING_NOTE——裁决①②③ = owner 本会话口头裁决（待正式 append Decision-Log 续61）；提案④ = owner 未签，待确认后并入 correction #4"
context: "博导复审《2026-07-16-gate-s1-rereview-application-stage1a-doctoral-review.md》裁决 WITHHOLD — CORRECTION #4 REQUIRED；本会话对复审逐条独立核验（仓内事实断言全部证实）后，owner 对四个争点给出裁决"
---

# Correction #4 预备：owner 裁决与编码深度提案

## 独立核验结论（本会话，纪律 = reviewer-response-protocol）

复审的仓内事实断言**逐条核验全部属实**（route 表 10 行范围写法、validator 仅存会话记录、
REC-1 派生查询不可重建、REC-2 仅 INCLUDED、evidence_grade 重复、information_source_classes
示例歧义、51 查询无 cs.SE/cs.HC、词表双侧归一化歧义）。但复审的「claim–evidence mismatch」
定性混装三类：G3 = 真实完成态夸张（该认）；G4/G6 = 原要求已闭 + 本轮新增要求（裁决措辞
应更正）；G2 = 对已如实披露偏离的正常裁决驳回（不是 mismatch）。回应信按此分层。

## 裁决①（owner 2026-07-16）：venue_tier 采评审拆分

- **内容**：接受复审 C4-2——`venue_tier` 只保留发现优先级/DFS 排序键角色（梯队平局键不变），
  不再作实验可信度默认先验；承重全归逐篇 `study_quality`（七维结构化）；`T2_UNREVIEWED`
  标签退役，同行评审状态由 `publication_status` 独立承担。
- **性质**：本条是对续59 owner 裁决②（「先验+覆盖折中」）先验语义部分的 **dated
  supersession**（审计层 append-only，走 Decision-Log 新条目，不改写续59）。
- **Rationale**：裁决②的辩护词混淆了阅读优先级（tier 已在 DFS 排序键，保留）与证据承重
  （全文强制 A2-9 + 逐篇强制 study_quality 使「初期承重无据」场景在协议上不存在）。

## 裁决②（owner 2026-07-16）：ID 核验前置，注册新访问类

- **内容**：评审 §9.2 列出的 13 篇 sentinel + VideoAgent-2026（2606.23327）等 UNVERIFIED
  条目，**入种子 manifest / sentinel 清单之前**逐 ID 联网核验（owner：「错误或者幻觉会累积」）。
- **机制**：correction #4 中预注册访问类 `ID_DEREFERENCE`——按已知 arXiv ID/DOI 取对应页面、
  核验存在性+题名一致性；无查询串、无结果排序、无发现行为 → 不计入 `queries_executed`
  （零查询 attestation 语义保持为真），但**逐次留痕**（id / 时刻 / HTTP 状态 / 裁决
  HIT|MISMATCH|UNRESOLVED）入机器可读核验文件；attestation 文字同步披露该访问类。
- **MISMATCH 处置**：不入种子、留痕、回应信中向评审指明其 sentinel 不可解析/不符。

## 裁决③（owner 2026-07-16）：阶段语义确认——survey 执行 = Stage-1A

- 正典（Research-Methodology）：**Stage-1A = 问题界定（广泛 survey、候选研究问题、纸面
  原型设计）；Stage-1B = 方向性原型探索（触碰模型的廉价小样，单次触碰即算实验+exposure，
  须 owner 显式放行）**。开始执行 survey ≠ 进入 1B；1B 的标志是**跑模型**（如 P-α 头空探针）。
- 门序列：Gate S1 签署（reviewer）→ owner 执行批准 → P0-R8 复跑 → **survey 执行（仍是 1A）**
  → 1A close 签字（可回放 survey 完成 + 3–5 候选问题）→ **1B 放行签字** → 模型探针。
- 后续称谓统一用「**Stage-1A survey 执行期**」；owner 此前「Stage-1B 正在开始」表述据此更正
  （复审 §0.2 的阶段纠正成立）。

## 提案④（owner 未签，待确认）：编码三深度 + code-on-use（承重时点编码）

动机：REC-2 已约 60+ 字段，C4-2（七维质量）/C4-4（工作级 ledger）还要加；无人估算过
分钟/篇 × 预期篇数，协议完美但执行饿死是真实风险。

- **Depth-0（ledger 行，即 C4-4）**：每个 canonical 命中一行（ID/题名/source hits/去重/
  阶段/decision/reason code/reviewer），书目字段**脚本预填**（API 元数据自动进），人只填
  裁决字段。~1–2 min/篇。
- **Depth-1（筛选级 REC-2 核心）**：INCLUDED 工作填精简必填核：身份元数据（预填）+
  topic_relevance + proximity 六轴 + publication_status + venue_tier + threat 标志 +
  verification_depth。~5–10 min/篇。
- **Depth-2（承重级全合同）**：完整 REC-2（source_axes/omni_axes/rl_identity/tf_audit/
  evidence_axes + 七维结构化 study_quality）**仅在该工作实际承重时强制**——即 mapping
  报告引用其数字支撑/摧毁/占据某 claim，或被标 direct threat。触发 = code-on-use。
- **防走样机制**（不许变成暗降标准）：① validator 规则——报告中任何承重 claim 必须回指
  Depth-2 完整的 REC-2 行，缺则 FAIL；② 条件 NA 折叠——不适用的整块（如无 RL 宣称的工作
  的 rl_identity 九字段）允许单字段 `NA:<理由>` 折叠，不留九个空格子；③ 本政策在
  correction #4 中**预注册并向评审明示**为实现口径，非事后偏离。
- **吞吐估算（粗）**：~300 ledger 行 ×1.5min ≈ 8h；~80 INCLUDED ×8min ≈ 11h；~30 承重
  ×25min ≈ 12h → 合计 ~30h，可行；对照全员 Depth-2 ≈ 53h+ 且质量并不更高（PRISMA 惯例
  本就只对进入综合的研究做质量评估——code-on-use 与之同构）。
- **风险披露**：评审可能坚持全部 INCLUDED 七维编码；届时以 PRISMA 同构论证 + 吞吐数字
  申辩，owner 终裁。

## 待办（provenance：本会话；失效条件：correction #4 落盘并送签后本件归档）

1. owner 确认提案④ → append Decision-Log 续61（裁决①②③④一并，ADR 骨架，①标注对续59
   裁决②的 dated supersession）→ 热层同步。
2. 执行 correction #4（严格按复审 §14 十一项清单，一项不多）：C4-1 分层回应信（G3 认错
   更正 / G4/G6 按「原闭+新增」记录 / G2 按偏离裁决接受）→ C4-2（含裁决①）→ C4-3
   50 行机器可读 route + 仓内 validator → C4-4（Depth-0 ledger）→ C4-5 派生查询字段 +
   离线 replay test → C4-6 sentinel 核验（裁决② ID_DEREFERENCE 前置）+ cs.SE/cs.HC
   敏感性检查。估计 2–3 专注日，大头 C4-6。
