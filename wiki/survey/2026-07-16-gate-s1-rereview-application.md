---
artifact_id: SF-S1-REREVIEW-APP-2026-07-16-01
title: "Gate S1 search-design 窄幅复核申请书（G1–G6 整改后再送签）"
date: 2026-07-16
addressee: "Gate S1 评审人（search-design 签署权持有者）"
trigger: "《System-first Research Proposal v3：Stage-1A 收官就绪度对抗审查》裁决 = WITHHOLD SIGNATURE — TARGETED MAJOR REVISION（G1–G6）；owner 四裁决（Decision-Log 续59）→ amendment-3 整改批落盘；owner 2026-07-16 过目通过整改批并批准送签"
requested_scope: "窄幅复核（评审 §7.2/§9/§11 自定范围）：只查 G1–G6 闭合与 bundle correction #3 一致性，不再开 proposal 轮次"
attestation: "截至本申请书落笔，联网检索查询执行数 = 0；本申请书编制过程零联网访问"
---

# Gate S1 search-design 窄幅复核申请书

## §1 申请事项与签署对象

申请对 Gate S1 search-design 作**窄幅复核**并签署。签署对象 = bundle manifest
（`wiki/survey/2026-07-15-sf-bundle-manifest.md`）**dated correction #3 所钉 @37da7f3 的
不可变工件集合**（17 件，每件 git blob 已逐件机器重验一致；后续任何变更走 dated correction
新条目，不改写本集合）。整改落在两个提交：`37da7f3`（amendment-3 整改批，19 文件）+
`420ae2b`（correction #3 钉定）。

签署包六件套组成（协议 §12，A3 后映射；blob 均 @37da7f3）：

| 件 | 内容 | path | blob（short） |
|---|---|---|---|
| ① | 协议本体 + amendments 1–3 | `2026-07-15-system-first-survey-protocol-v1.md` / `…-amendment-1.md`（含 amendment-2 追加节） / `2026-07-16-sf-protocol-amendment-3.md` | `3133ffb76e03` / `cfbf1ac326a8` / `061c1437b489` |
| ② | seed manifest（74 条）+ 伴随报告 | `2026-07-15-sf-seed-manifest.jsonl` / `…-report.md` | `7eaefcc923e4` / `35148a9ae6f2` |
| ③ | 数据源与检索字符串 | 协议 §2/§4 + 编译冻结查询 51 行 `2026-07-15-sf-queries.jsonl` + 编译器 + T1 routes manifest `2026-07-16-sf-t1-proceedings-routes.md` | `c56ca22629a2` / `9508ef9eccdc` / `9bb2f3d3a8ac` |
| ④ | 纳排/抽取 schema | 协议 §6/§7（同件①协议 blob） | — |
| ⑤ | 空白记录模板 REC-1..REC-7 | `2026-07-15-sf-blank-templates.md` | `7129ed06d394` |
| ⑥ | 签署区 | 协议 §12（同件①协议 blob） | — |

签署语义不变（协议 §12）：**检索设计合格可执行；不构成对研究方案科学成立或 novelty 的背书。**

## §2 G1–G6 逐项闭合对照

| # | 评审要求（原文要旨） | 闭合方式 | 证据定位 |
|---|---|---|---|
| G1 | arXiv-only 不得冒充综合宇宙；建议方案 A：arXiv 主 corpus + venue-native ID/DOI + 本地全文 hash 纳入 | **采方案 A**（A3-1）：arXiv-primary + 免费官方开放获取源救援（ACL Anthology/NeurIPS/PMLR/OpenReview/CVF/ISCA 等，venue-native ID/DOI + 本地备份 + sha256）；产出降名为「arXiv-primary systematic mapping（免费开放获取救援+显式移除记账）」，不自称 comprehensive universe。付费不可得者的处理与评审原文有一处机制偏离，**见 §4-1** | amendment-3 A3-1；协议 §2；routes manifest §4 |
| G2 | venue tier 不得替代 study-quality；三轴分立；T1 不自动承重、T3 不按 venue 自动排除；threat 判定与实验可信度分离 | 三轴分立落地（`verification_depth` / `publication_status` / `study_quality`〔HIGH/MEDIUM/LOW+一句理由〕）；T1 可 `T1_DEMOTED:<理由>` 降权；T2 高质经裁决 `T2_PROMOTED:<理由>` 可承重；T3 改按相关性/质量裁决，EXCLUDED 必须给理由；novelty/priority threat 判定 tier-blind。venue_tier 的剩余角色与评审原文有一处偏离，**见 §4-2** | amendment-3 A3-2；协议 §2；REC-2 `evidence_axes` 块 |
| G3 | 50 条 route 实例化（入口/track/词表/归一化/模糊匹配/raw hash/解析日志）；消除 T1/T2 同名异构 | 独立冻结件落盘：50 route ID（ICCV 偶数年 3 条 NOT_HELD 占位如实标注）、每会入口+正会 track 界定、词表 v1 = 73 项（A=39/B=18/C=16，规则 A∨(B∧C)，逐项零通配符）、题名归一化+exact/fuzzy（Jaccard≥0.90 / 编辑距离比≥0.92,fuzzy 逐条人工裁决留痕）、raw 题录存数据盘 sha256 入日志、四步解析流程、五计数字段禁口算；执行日志模板 REC-7。模板 T1–T6 → **REC-1..REC-7**，`T` 前缀自此 venue 梯队独占 | `2026-07-16-sf-t1-proceedings-routes.md`（§6 纸面自检 7/7 PASS，机器验证）；amendment-3 A3-3/A3-4；blank-templates REC-7 |
| G4 | 承重合同传播到数据结构（评审列出的全部字段） | 评审 G4 代码块所列字段**逐一**进入 REC-2 schema：`source_axes`（信息来源六类/answer_bearing_external_info/gold_path_audit/activation_attribution）、`omni_axes` 五轴、`rl_identity` 九字段（含 authors_call_it_rl）、`tf_audit` 扩展四字段、`learned_object` 扩枚举、`core_access` 扩枚举（+hidden-state/attention/API-multimodal）、`evidence_axes`（G2 三轴+quality_override）；三个 JSON 块均机器 parse 验证 | amendment-3 A3-5；`2026-07-15-sf-blank-templates.md` REC-2 |
| G5 | bundle/验证报告/热状态重对齐同一 blob 集（五个动作） | ① dated correction #3 钉定现行全件 ✓；② 编译器离线复跑——48 行原批**逐字节前缀不变**（前缀 sha256 一致），新 3 行 append，终态链条（协议 sha256 → 编译器 → jsonl sha256）落盘 ✓；③ routes manifest 静态验证（§6 自检 7/7，如实标注为机器自检、非独立外部验证）✓；④ `Research-Objective.md` 已清退役副源口径并同步至现行热层态（送签时 = 续60）✓；⑤ 「独立 static signoff review」= **本次申请的窄幅复核本身**（外部行为，无法自证，如实声明） | bundle correction #3；`docs/checks/2026-07-16-sf-queries-static-validation-rerun.md`（13/13 检查）；routes §6；Research-Objective |
| G6 | 分页拆分递归规则补全（单年 >2000 时可终止） | 年 → 月 → 日逐级确定性细分至每片 ≤2000；派生 `query_id = <父ID>-W<窗口序号>`，REC-1 行内记 `parent_query_sha256`，拆分事件全留痕 | amendment-3 A3-6；协议 §4 |

## §3 P0-1..P0-6 checkbox 对照

- **P0-1**（固定送签快照）：correction #3 ✓；热状态更新 ✓；编译器复跑+链条哈希 ✓；`queries_executed = 0` 维持 ✓。
- **P0-2**（来源与 venue 规则）：降名+救援 ✓；tier 不再终裁 ✓；`study_quality` 独立轴 ✓；T3 按相关性/质量裁决并登记理由 ✓；第五勾（全文不可得者的存在性保留）**机制偏离披露于 §4-1**。
- **P0-3**（routes 实例化）：五勾全 ✓（见 G3 行）。
- **P0-4**（schema 传播）：六勾全 ✓（见 G4 行）。
- **P0-5**（种子/查询敏感性）：14 篇种子全部入 manifest（批次2，`initial_tag[]` 只管阅读优先级不预判纳排）✓；离线敏感性审计（零联网）确认评审点名 7 短语为真盲区 → 增补 SF-L1-Q7/Q8、SF-L3-Q7 三条查询，48 条旧记录零覆盖 ✓；ToT/Socratic-Models 经审计裁量**不加查询**（种子+引文图兜底，理由留痕）——属评审「必要时新增」授权内的裁量，非偏离。VideoAgent-2026 的 arXiv ID 存在性标 UNVERIFIED，执行首步核验。
- **P0-6**（引用勘误）：Snell 降格为 trained-verifier/mechanism analogy ✓；HedgeTune 标 output-level overoptimization analogue ✓；「大幅头空」条件化 ✓；occupancy version-pin + full-text locator 登记为 **Stage-1A close 前义务**（评审原文即如此定位），未伪称已完成。

## §4 两处对评审原文的有意偏离（如实披露，请在窄幅复核中裁决）

1. **付费不可得记录的处置（G1/P0-2 第五勾）**。评审原文：「无法获得全文者保留为 coverage
   gap，不从“存在性”记录中消失」。owner 裁决①（2026-07-16）：「付费就废弃这条记录，因为我们
   获取不到原文」。落地折中（A3-1）= `REMOVED_PAYWALLED_UNOBTAINABLE` **计数移除**：记录
   退出语料、不承重，但移除事件+ID+题名+venue+计数**强制进入 flow report**，凡占据类/
   NO_DIRECT_MATCH 结论必须伴随移除计数披露。即：存在性记账由 flow report 承担（不消失），
   语料成员资格按 owner 裁决废弃。与全文强制 A2-9 同构（读不到原文的东西不承重）。
2. **venue_tier 的剩余角色（G2）**。评审原文倾向「venue tier 只作 publication metadata」。
   owner 裁决②落地为：tier 保留为**默认先验权重**（非纯元数据），由逐篇强制的
   `study_quality` **双向覆盖**（`T1_DEMOTED`/`T2_PROMOTED` 均须登记理由）。评审的四条实质
   要求（T1 不自动承重、T3 不自动排除、三轴分立、threat 判定 tier-blind）全部满足；偏离仅
   在于先验角色的保留——理由：在逐篇质量评估完成前，tier 是唯一可用的默认排序信号，全降
   元数据会使初期承重判断无据可依。

（模板改名一项按评审给出的 `REC-1..REC-6` 选项执行并顺延新增 REC-7 route 日志，不是偏离。）

## §5 过程证据

- **敌意内审环**：双镜头（计数一致性 / G1–G6 闭合完备性）R1 = 1 MAJOR + 4 MINOR + 2 NIT →
  全部修复 → R2 窄幅机器复检清零 → `A3_BATCH_LOOP_CONVERGED@37da7f3`（A3-10 纪律：带对象带锚）。
- **可复现链条**：现行协议 sha256 → 编译器（sfqc-1.0.0/1.1.0 版本分层+增补注册表+防混入守卫）→
  `2026-07-15-sf-queries.jsonl` sha256，且 48 行原批与旧文件逐字节前缀一致（前缀 sha256 相同）
  ——完整哈希见 `docs/checks/2026-07-16-sf-queries-static-validation-rerun.md` 终态补记。
- **钉定核验**：correction #3 全部 17 件 blob 由 git 逐件机器重验（编制中发现并当场更正一处
  预填错误哈希——sweep 件 `8cf7b46e79be`，更正过程留痕于会话记录）。
- **本申请书自身的校验环**：落盘后过一轮独立敌意校验镜头（禁网，逐项核 blob 哈希 17/17、
  提交、评审引文逐字、数字、A3 转述、偏离披露完备性），R1 = 1 MAJOR（协议章节号误引
  §13→§12，内容本身逐字正确）+ 1 MINOR + 4 NIT，全部修复后 R2 窄幅复检清零（grep §13
  零残留 + 引文重比对）。
- **attestation**：截至本申请书落笔，联网检索查询执行数 = 0；amendment-3 批全部子代理工作
  显式禁网。

## §6 已登记的执行期义务（非签署阻塞，如实列出）

1. flow report 移除记账（§4-1）与 route 五计数机器汇总——执行期义务，REC-7/流程报告承接。
2. VideoAgent-2026（batch-2 种子）arXiv ID 存在性——执行首步核验，不可解析标 UNRESOLVED。
3. occupancy 数字 version-pin + full-text locator——Stage-1A close 前完成（评审 P0-6 定位）。
4. routes 表内 `ENTRY_TO_RESOLVE`（PMLR 2025/2026 卷号）与 `NOT_YET_PUBLISHED` 各年——
   执行时确定性解析/§5bis 增量复查，事件入 REC-7 不改冻结表。

## §7 请求的复核范围与签署后路径

- **请求范围**（评审 §7.2/§9/§11 原定）：G1–G6 闭合核验 + correction #3 所钉 bundle 的
  一致性核验。**不请求也不需要 proposal 轮次**（评审明示「不要求 proposal v4，不要求再加
  一轮元叙事」）。
- **签署后路径**（协议 §12/§12.1，三方分立缺一不可）：reviewer search-design 签署 →
  owner 执行批准 → P0-R8 状态门复跑 → 方可执行首条查询；随即开始 survey 执行，产出对齐
  评审 §10 的 Stage-1A close 证据清单。
- **owner 送签批准记录**：2026-07-16，owner 过目 amendment-3 整改批全件后批准送签
  （「我觉得现在没啥问题」）。此为**送签批准**，与 §12 签署区的「owner 执行批准」是两个
  独立动作，后者在 reviewer 签署后另行签字。

—— 申请人：研究执行方（W1）。本件自身随提交入 git，blob 以提交为准；对本件的任何更正走
dated correction，不改写。
