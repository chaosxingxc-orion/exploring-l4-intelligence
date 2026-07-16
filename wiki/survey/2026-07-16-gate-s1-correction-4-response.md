---
artifact_id: "SF-S1-C4-RESPONSE-2026-07-16-01"
title: "Correction #4 回应信（superseding response）——对博导复审 WITHHOLD 的分层回应与六项交付"
date: 2026-07-16
addressee: "Gate S1 评审人（search-design 签署权持有者）"
supersedes: "续60 申请书（2026-07-16-gate-s1-rereview-application.md）中的 G1–G6 完成性表述——本信为其 dated superseding response,原件不改写"
trigger: "《Gate S1 再送签申请的 Stage-1A 博导级对抗复审》裁决 WITHHOLD SIGNATURE — TARGETED CORRECTION #4 REQUIRED；owner 四裁决 = Decision-Log 续61"
attestation: "联网检索查询执行数 = 0 维持；ID_DEREFERENCE 访问类 21 次已按 amendment-4 §1 注册并逐次留痕（2026-07-16-sf-id-dereference-log.jsonl）"
---

# Correction #4 回应信

## §1 总立场

我方对复审的全部**仓内事实断言逐条独立重验,全部属实**（route 表 10 行范围写法/自检脚本仅存
会话记录/REC-1 派生查询不可重建/REC-2 仅 INCLUDED/`evidence_grade` 重复/
`information_source_classes` 示例歧义/51 查询无 cs.SE、cs.HC/词表双侧归一化歧义）。回应原则 =
**认错认准**：该认的完成态夸张全部收回并更正;性质不同的项分层陈述,不以笼统道歉覆盖精确
责任——不该认的认了同样是记录失真。

## §2 完成性表述的日期化更正（C4-1 主文）

以下表述**取代**续60 申请书 §2 对应行（原件按 append-only 保留）：

| 项 | 续60 表述 | 更正后表述（本信生效） | correction #4 后状态 |
|---|---|---|---|
| G1 | 已闭合 | **closed with limitation**——有界覆盖表述维持,穷尽性结论永不宣称;付费移除四条件（逐工作身份/双计数分离/不承重/集中度偏差报告）接受并入 flow report 义务 | 维持 closed with limitation |
| G2 | 已闭合（附偏离②） | **当时未闭合**——venue≠quality 混淆属实 | **已修复**：owner 裁决①改判采评审拆分（§4）;七维结构化+三合成验收案例（amendment-4 §3） |
| G3 | 「50 route ID 独立冻结件落盘…机器验证」 | **更正为：当时仅 10 个 venue 范围模板覆盖 50 个预期 venue-year 组合,逐条实例化未完成;「机器验证」的脚本与输出未持久化,不构成可复跑验证**——此为本轮唯一承认的**完成态夸张**,与在案 QRP 更正义务同型,郑重收回 | **已修复**：50 行 JSONL 逐条序列化 + 词表机器正典（73 raw/71 有效,双侧归一化正典化）+ 仓内 validator + 持久化输出 12/12 PASS |
| G4 | 已闭合 | **原要求（合同传播）当时已闭合——复审 §6.1 亦确认;工作级筛选 ledger 为本轮新增要求,接受** | **已交付**：REC-0 主账 + schema 三修 + 三合成 lineage 验收案例（amendment-4 §4） |
| G5 | 已闭合 | 维持（复审独立重验 17/17 一致）;对象边界限定接受——当前热层为 bundle 外状态证据,不混作签名对象 | 维持 closed |
| G6 | 已闭合 | **递归规则（原要求）当时已补;派生查询逐字段可重放为本轮加深要求,接受** | **已交付**：REC-1 派生行强制字段 + GMT/闭区间语义 + 节流/退避/续跑/单日硬停止 + 规范实现 + 离线 replay test 9/9 PASS |

**每个完成态动词的 artifact+hash+复跑命令 = amendment-4 §5 工件清单**（逐行给出）。

## §3 对「材料性 claim–evidence mismatch」定性的分层回应

我方接受该定性对 **G3** 完全成立,并接受复审 §12.2 的告诫：完成态语言覆盖缺口是本团队在案
QRP 的同型复发,本信 §2 即时更正。同时按评审回应纪律陈述两点分层意见,请复审知悉（不构成
对裁决的异议,WITHHOLD 我方接受）：

1. **G4/G6 属「原要求已闭合 + 本轮新增/加深要求」**,复审 §6.1（「不能不公正地说团队没有修
   G4」）与 §8.1（「已经修对的部分」）自身已作此区分——建议最终记录中 G4/G6 不与 G3 的
   完成态夸张同列为 mismatch 病例。新增要求我方全部接受并已交付。
2. **G2 属「已如实披露的偏离经裁决驳回」**：续60 申请书 §4-2 独立成节请评审裁决,非隐瞒性
   陈述。评审驳回后 owner 已改判（§4）。建议 mismatch 清单中不计入已披露偏离项。

## §4 owner 改判披露（Decision-Log 续61,2026-07-16）

- **裁决①（venue_tier）**：接受评审立场——tier 降为发现层元数据（T1 手扫范围标记 + DFS
  排序键平局 + coverage 分层描述）,**零证据权重**;`T2_UNREVIEWED`/`T1_DEMOTED`/`T2_PROMOTED`
  退役;承重全归逐篇 `study_quality` 七维。此为对续59 裁决②先验语义的 **dated supersession**
  ——改判理由：原辩护词混淆了阅读优先级（保留于排序键）与证据承重（全文强制+逐篇强制下
  「初期承重无据」场景协议上不存在）。
- **裁决②（sentinel ID 前置核验）**：评审 §9.2 清单 13 篇在入种子前逐 ID 联网核验（防幻觉
  累积）;`ID_DEREFERENCE` 访问类注册于 amendment-4 §1。**核验结果：14/14 HIT（含 batch-2
  遗留的 VideoAgent-2026）——复审引文清单零幻觉,特此确认并致谢**;AgentEval 主类目 cs.SE
  零 cross-list、v1=2026-07-08 在窗内,类目盲区论证被独立坐实。
- **裁决③（阶段语义）**：survey 执行 = Stage-1A 核心工作;复审 §0.2 的阶段纠正成立,
  「Stage-1B 正在开始」表述收回,后续统一称「Stage-1A survey 执行期」。
- **裁决④（编码深度）**：D0/D1/D2 + code-on-use 预注册于 amendment-4 §2,**明示待评审在
  窄幅复核中一并裁决**;若评审坚持全 INCLUDED 七维编码,按评审裁决执行。

## §5 复审 §14 签署清单自评

| 项 | 状态 | 证据 |
|---|---|---|
| correction #4 对完成性表述作日期化更正 | ✅ | 本信 §2 |
| G2 venue / publication status / study quality 三者真正分离 | ✅ | amendment-4 C4-2 + 协议 §2/§6 折入 + REC-2 七维 + §3 三合成案例 |
| 50 条 route 逐行机器可读 | ✅ | `2026-07-16-sf-t1-routes.jsonl`（50 行） |
| route validator 与固定输出在 bundle 内 | ✅ | `scripts/survey/sf_t1_routes_validate.py` + `docs/checks/2026-07-16-sf-t1-routes-validation.json`（12/12） |
| 工作级 screening/dedup/adjudication 记录可用 | ✅ | REC-0 模板 + amendment-4 §4 三合成 lineage |
| child query 可精确重放 | ✅ | `sf_child_query_split.py` + replay test 9/9（同父+同计数→逐字相同） |
| cs.SE / cs.HC 类目盲区有检查或可审计补救 | ✅ | SF-L10 受控道（53 条,51 前缀字节不变）+ 坐实的 cs.SE 哨兵 |
| 至少一组 sentinel recall 结果已落盘 | ✅ | `docs/checks/2026-07-16-sf-sentinel-recall.json`（9 HIT + 5 EXPLAINED_MISS,零 unexplained） |
| correction #4 manifest 的 blob/hash 一致 | ⏳ | 本批提交后 bundle manifest dated correction #4 钉定（两段提交,与 correction #3 同构） |
| reviewer、owner、P0-R8 仍保持分立 | ✅ | 签署区未动,三方缺一不可维持 |
| 首条真实查询前仍为零查询 | ✅ | attestation=0;ID_DEREFERENCE 已注册披露（非检索查询） |

## §6 双向合同

复审 §14 承诺：「若以上全通过,应签署 Gate S1 并允许立即开始 Stage-1A survey,**不应再以
『还可以更完善』为由无限延期**」。我方将此承诺与本信一并钉入记录作为**双向合同**：我方不再
借整改重开 proposal 或扩展知识工程;评审按清单核验,全过即签。签署后路径不变（reviewer
签署 → owner 执行批准 → P0-R8 复跑 → 首条查询）。

—— 申请人：研究执行方（W1）。本件随提交入 git,blob 以提交为准;更正走 dated correction。
