---
title: 对《AI 协同 Survey 知识栈开源实现选型审查》的正式回应（六镜头敌意复核 + owner 裁决）
date: 2026-07-14
stage: Stage-1A
review_type: response-to-architecture-review
status: owner-adjudicated — SHELVE-ALL（全部搁置，Stage-1C 收官后再议）
target_doc: wiki/2026-07-14-ai-assisted-survey-knowledge-stack-open-source-evaluation.md
target_doc_commit: b41f9f85db359fa5b13cadbcb4024c130d43542e
generated_by: "Claude Fable 5 主会话（编排+综合）+ 六镜头敌意工作流 wf_ac8220be-dd5（6 agents / 556,735 tokens / 145 tool calls / ~11 min）"
verified_by: "Claude Fable 5 主会话亲自复核（清单见 §1.2）——非同一无监督代理：镜头产出为候选，本回应的每条 P0 级采信均经主会话独立源码/网络复核"
adjudicated_by: "owner（2026-07-14，AskUserQuestion 亲答两问：处置=全部搁置；落档=正式审查回应）"
evidence_archive: docs/checks/2026-07-14-knowledge-stack-eval-sixlens-adversarial-review.json
---

# 对《知识栈开源实现选型审查》的正式回应

> 按 2026-07-11 reviewer-response 先例成文：独立逐条核验 → 证据 → 接受/驳回 → 行动与门控承诺。
> 本回应 append-only；目标评审文档原文不改写，以 (commit `b41f9f8`, git-blob) 为正典锚。

## 0. Owner 裁决（先说结论）

**处置 = 全部搁置（SHELVE-ALL）。** 不批准 llm-wiki-compiler 隔离试点；**也不启动**协调者建议的
schema-first 最小实现；评审文档以**选型参考**身份留档（不是"批准执行"）。整体在 **Stage-1C 收官后再议**，
复活条件见 §4。当前关键路径不变：owner Stage-1C 选题 + 诚信核查 C1/C4。

> 记录分歧（协调者义务）：协调者本轮的建议是"拆分采纳"（原则+schema-first 现在做、编译器试点
> post-1C 条件化）；owner 裁决更保守（连 schema-first 一并搁置）。裁决即终局，此处仅如实登记两个立场。

## 1. 核验方法与 provenance

### 1.1 六镜头敌意工作流（wf_ac8220be-dd5）

| 镜头 | 任务 | 结论要点 |
|---|---|---|
| verify:upstream | 上游主推荐对象实时核验 | 事实刻画准确甚至偏保守；1 P1（审计/锁定 commit 错位） |
| verify:alternatives | 其余 16 项引用逐项核验 | 零死链/零张冠李戴；1 P1（OpenAlex 计费遗漏） |
| critique:consistency | 内部矛盾+收词纪律 | 1 P0（试点协议自相矛盾）+ 8 P1 |
| critique:stage-fit | 阶段适配+机会成本 | 1 P0（大工件三问全不过）+ 3 P1 |
| critique:cost-realism | 成本现实性+最小替代 | 1 P0（owner 门无法运行时强制）+ 4 P1 |
| critique:completeness | 遗漏项（存量/团队拓扑/自反性） | 5 P1 + 5 P2 |

完整镜头产出（含全部证据行号/URL/估算明细）原样存档于 `evidence_archive`（97.5 KB，六 lens 全文）。

### 1.2 主会话亲自复核（签署级抽查，全部坐实）

1. 上游仓库真实性：`atomicstrata/llm-wiki-compiler` 存在，MIT、~1.7k stars，v1.0.0 发布 2026-07-11（评审前 3 天）；README 六项能力属实（WebFetch 亲验）。
2. 沙箱审计真实性：`%TEMP%\llm-wiki-compiler-audit-20260714` HEAD = `bed4dda13f5d4ea61d7cf635a9422d3c2740668e`，与评审 §9 声称逐字节吻合；`node_modules`/`dist` 在场。
3. 门差异指控：`src/profile/templates/builtin/autosci/entities.ts:70-87` —— `experiment.complete` 仅要求 `resultSummary` + 一条 `tests` 关系，`result` artifactRef 无必填/健康检查；官方指南却宣称 gate 存在。**属实。**
4. owner 门不可强制：`src/workflows/actor-identity.ts:7-14` 原文自认身份是 "ADVISORY … NOT proof of identity … The real boundary is OS-LEVEL ISOLATION"。**属实。**
5. 存量正典被忽略：`docs/claim_ledger.yaml` 头部明文 "SINGLE SOURCE OF TRUTH"，评审全文零提及。**属实。**
6. OpenAlex 计费：官方博客 2026-02-24 宣布强制 API key + 按量计费（search $0.001/次、每日 $1 免费额度）。**属实，评审遗漏。**

## 2. 确认清单（评审立住的部分 —— ACCEPT 为设计参照）

- **事实底座全部过硬**：16 个引用项目/资料真实、定性公允；核心指控（"文档说门存在、运行时未锁门"）被三路独立证据坐实（本会话源码亲验 + 两镜头，且 v1.0.0 与审计 commit 的 entities.ts blob 一致，发现可迁移）。**未发现任何编造或夸大。**
- **值得留档采信的判断**：① 问题改写（不是"装不装 Wiki"而是"分层承担+信任边界"）；② 五层信任分级思想（其编号 T0–T4 系该评审自造、未登记、与项目 2026-07-07 T0–T7 探针编号同名异构——引用必须带限定语，见 §5）；③ "组合必要、正典唯一"；④ 现阶段拒绝 TrustGraph/Wikibase/GraphRAG 作主系统；⑤ kill-条件机制本身。
- **诚实自限**：矩阵自称启发式、Windows 失败如实报"未通过"、请求 owner 裁决而非自我放行。

## 3. 缺陷登记（本回应采信的发现；完整证据见 evidence_archive）

### 3.1 P0（三条，阻断"现在执行"形式的批准）

| # | 镜头 | 缺陷 | 关键证据 |
|---|---|---|---|
| P0-1 | stage-fit | 全文零处讨论执行时机/关键路径；按 owner"大工件三问"全不过：消费者是 post-1C/Stage-2；16 对象中约 5 个（IdentityCandidate/KillCondition/MethodOperator/Proposal/ExperimentHook）依赖尚未做出的 I1–I4 选题与未冻结的 same-selector contract——现在建 = 把 I4 叙事固化进 schema、在 owner 决策前形成选题倾斜；与被叫停的 GLAP 全量预建同错误类 | grep 全文无 Stage-1C/C1/C4/时机；Research-Objective open items 1–4 |
| P0-2 | cost-realism | "owner-only decision 门"在该工具中**无法运行时强制**（actor 身份 advisory，真实边界=OS 级用户隔离，评审从未预算）；kill 条件 #1 在 Day-1 即被设计性触发。另"两天"系 3–5 倍低估（现实 6–11 人日：93 篇 PDF backfill、~46 门控回归测试、538 上游测试环境定诊等） | actor-identity.ts:7-14（主会话亲验） |
| P0-3 | consistency | 试点协议自相矛盾：锁 v1.0.0 后，§9 已实锤的 AutoSci 门偏差必然在场 → Day-1 第 6 项（"文档门与运行时门完全一致"）必然失败、kill 条件 2 必然触发；检查范围必须显式限定到自定义 profile 并登记具名豁免，否则试点死于出发点 | 评审自身 §8 L380/L384/L418 vs §9 L438/L441 |

### 3.2 P1（十五条，任何复活前必须补答；此处按主题归并）

1. **审计/锁定错位**（upstream）：§9 证据采自 main HEAD `bed4dda`（2026-07-13），§8 却要锁 v1.0.0 tag `67306f2`（2026-07-11），中隔 4 commit 含 3 个大功能 PR；复核已证 entities.ts 两版本 blob 一致（`6edf920…`），但 Windows 失败等运行时发现未绑定锁定版；须对齐到同一 commit 并留档。
2. **OpenAlex 计费遗漏**（alternatives）：强制 API key + 按量计费（2026-01/02 生效）未提；矩阵"运维成本 低"失去事实基础；须补退化路径（Crossref/arXiv 优先、快照本地化、响应缓存入 T0〔该评审的原始证据层〕）。
3. **收词纪律成批违规**（consistency）：40+ 新造代号零登记；T0–T4 与既有 T0–T7 探针编号、"方案 A"与同日姊妹评审"Proposal A"（及术语表 A-SEL 条目的历史"Proposal A"）同名异构/三义碰撞；§6 还把登记义务从 MUST 软化为"可对齐"。处置见 §5。
4. **"非 AI 的 EvidenceSpan"谓词未定义**（consistency）：与方案 A 唯一入 T1 路径（AI 提取→人审）两种读法皆坏（门永不可满足，或人审即洗白）；须精确定义（如"人类逐字核对原文定位"）。
5. **"两天"与 16 对象互相矛盾**（consistency+cost）：Day-1"最小 profile"vs §6"至少 16 对象"；验收门"所有生命周期门有正负例回归测试"在两天内不可达；须显式规定试点子集。
6. **kill 条件 7/9 无机器可查成分**（consistency+cost）：违反其自身 §6 不变量；#7 基线双义（现行模板纸面成本 vs 实践成本差约 3 倍）且无对照臂；须冻结基线定义 + 同语料平行计时。
7. **§9 审计无 T0 工件**（consistency+completeness）：无日志/hash 入库，按其自身模型属 T2 却直接驱动决策，自反不合规；本回应已代为把六镜头证据入库 `docs/checks/`，但上游沙箱原始日志仍缺——复活时须重跑并留档。
8. **签署缺位**（consistency）：自称"最终签署意见"却无 generated_by/verified_by，违反其 §11.2 背书的同日模板规则 8。本回应以自身 frontmatter 示范补齐。
9. **全称否定命题零检索记录**（consistency）："没有单一开源项目同时满足…"无选型检索登记，按其自身标准属"检索遗漏"风险；须降级为有界命题或补 SearchEvent 级登记。
10. **存量机器零盘点**（completeness）：`docs/claim_ledger.yaml`（明文 SSOT）、305 条 `search-query-log.jsonl`、scout-ledger、neighbor-matrix FT/AB/SC 证据分级、22 规则 conformance checker——与 §6 ontology 高度同构却零映射；编译器自带 claim 存储将直接踩其 kill 条件 3（双事实源）；复活前置 = 字段级对账表 + 单正典声明。
11. **团队拓扑失真**（completeness）：权限表设了本团队不存在的独立"人类 reviewer"角色；并发 Claude 会话共享 checkout 的多写者竞态零设防（上游亦无锁机制）；须按单 owner + 多 AI 会话重写。
12. **Zotero 搭便车**（completeness）：项目今天并不使用 Zotero；采纳=从零建库回填 93+ 篇，且批注存 SQLite 非 Git 可重建——评审对 LLM Wiki 设"可删除/可重建"测试却未对 Zotero 层适用同一测试；须同标准审查或改评 JabRef/纯 Git 方案。
13. **编译 LLM 后端全缺**（completeness）：模型、费用、API key、网络可达性（本周实证 WebFetch 被封、2 条引用 NOT_RESOLVED）、离线策略零讨论；"确定性编译"无从验证。
14. **试点自身无进入条件**（stage-fit）：给 Graphiti 设了"≥10 个稳定时间图查询"的需求门，对自己推荐的编译器试点却不设等价门——双标；复活时进入条件见 §4。
15. **93 篇全文获取成本未计**（cost）：EvidenceSpan"页/表/行+摘录 hash"验收门在受限网络下不可达（仅身份层 backfill 即 2–3 人日）；须计预算 + 网络受限降级协议（如 ABSTRACT 级显式标记）。

### 3.3 主要 P2（复活时随试点报告一并补）

SOURCES_CONTRACT"行级 claim"错置；维护风险基线未登记（bus factor≈1、开核信号"Private marketplace…outside the public repository"、v0.5.0 全员崩溃史、组织改名、3.2 个月 14 tag）；运维评级偏乐观（Node≥24 + 19 运行时依赖含双 LLM SDK = 第二条完整工具链）；Day-1 步骤 5/6 顺序倒置；方案 B"10 个查询"门槛无口径；§11 生效时点未标；ARS 插件三套引用验证并存风险；漏评 ASReview/JabRef/Semantic Scholar/PRISMA-S/W3C PROV；与 wiki-sync 发布面及归档约定的接缝未讨论。

## 4. 复活条件（未来重启时的门 —— 本节即"搁置"的精确语义）

1. **时机门**：owner 完成 Stage-1C 选题（proceed/pivot），且确认存在下一轮结构化检索需求（round-2 饱和排期或 Stage-2 proposal 证据链）——与评审给 Graphiti 设门同一标准。
2. **顺序门**：若重启，**schema-first 先行**（identity-invariant 核心对象 JSON Schema + 校验器 + 与 claim_ledger.yaml/replayability 模板的字段级对账、单正典声明，估 1.5–2 人日）；编译器试点只能作为其后置、按评审 §10 自身升级信号触发。
3. **规格门**：任何编译器试点执行前，§3.1 三条 P0 + §3.2 全部 P1 必须在修订版试点协议中逐条关闭（owner 门改 git PR 层强制或预算 OS 隔离；审计与锁定同 commit；诚实工期 6–11 人日；LLM 后端与网络降级；OpenAlex 计费退化路径；存量对账；单人团队权限模型；术语登记）。
4. **裁决门**：修订版协议重新提交 owner 裁决；本次"搁置"不构成任何未来批准的默示。

## 5. 术语处置（收词纪律）

因提案已搁置，**不**将评审新造代号（T0–T4 信任层、l4-survey、16 对象名、方案 A/B/C 等）登记入
CLAUDE.md 术语表——登记会固化未采纳的术语。过渡规则：任何文档引用这些代号时必须带限定语
（例："T0–T4（2026-07-14 知识栈评审自造的信任分层编号，未登记；勿与 2026-07-07 T0–T7 探针编号
混同）"；"方案 A（知识栈评审的 Git-native 组合，勿与同日 survey-v2 评审的 Proposal A 混同）"）。
若未来复活并获批，届时按纪律拆名重命名后登记（T 编号与 L0–L4 均已被占用，须换前缀）。

## 6. 工件与哈希锚

- 目标评审文档正典：commit `b41f9f85db359fa5b13cadbcb4024c130d43542e` : `wiki/2026-07-14-ai-assisted-survey-knowledge-stack-open-source-evaluation.md`（核验 `git show <commit>:<path> | sha256sum`）。
- 六镜头完整产出：`docs/checks/2026-07-14-knowledge-stack-eval-sixlens-adversarial-review.json`（含各 agent tokens/tool-calls/时长与全部证据明细）。
- 上游沙箱：`%TEMP%\llm-wiki-compiler-audit-20260714`，HEAD `bed4dda13f5d4ea61d7cf635a9422d3c2740668e`（临时目录，未入正典——此为 §3.2-7 登记的已知缺口）。
- 上游锚点：v1.0.0 tag = `67306f2090eb755c9934ce8ed3e5d1199cc94c65`（2026-07-11）；autosci entities.ts 两版本 blob 一致 `6edf92035ea…`。
- 同批收档：`wiki/2026-07-14-survey-response-replayability-template.md`、`wiki/2026-07-14-survey-v2-and-stage1c-decision-package-doctoral-adversarial-review.md`（同 commit `b41f9f8`，as received，其内容裁决不在本回应范围）。
