---
title: AI 协同 Survey 知识栈开源实现选型审查
date: 2026-07-14
stage: Stage-1A
review_type: doctoral-adversarial-architecture-review
status: recommendation-for-isolated-pilot
repository_snapshot: 233dc7eb9224b5d7bc8df7bfd81a616ab15c6917
scope: knowledge-organization-and-ai-collaboration
---

# AI 协同 Survey 知识栈开源实现选型审查

## 0. 审查结论

**是的，必须调研开源实现；但问题不应被表述为“要不要装一个 LLM Wiki”。** 真正的选型问题是：

> 哪些组件分别承担文献身份、原始证据、结构化学术判断、AI 编译导航、图查询和人类审批，并且任何 AI 生成层都不能反过来污染事实层？

当前最合适的 Stage-1A 组合不是一个全包式产品，而是以下分层栈：

1. **Git + Markdown/JSONL/YAML + Schema 校验**：继续作为唯一的团队正典与审计账本；
2. **Zotero + 稳定 citation key/Better BibTeX 自动导出**：负责人工文献库、附件、批注和引用身份；
3. **OpenAlex + arXiv + Crossref**：负责 DOI/arXiv/version/引用关系的元数据核对与查漏；
4. **`atomicstrata/llm-wiki-compiler` 的锁版本隔离试点**：仅作为有类型、可重建、带审批门的“知识编译层”和 AI/MCP 读取层；必须为本项目另建 `l4-survey` profile，不能直接信任默认 AutoSci profile；
5. **STORM/Co-STORM（可选）**：只做问题分解、搜索车道扩展和反例候选生成，不得写入已确认学术事实；
6. **Graphiti（后置、可选）**：只有当“时间化观点/冲突/决策查询”确实产生稳定需求后，才作为由 Git 正典重建的派生图；
7. **现阶段不采用 TrustGraph、Wikibase、Microsoft GraphRAG 或 RAGFlow 作为主系统**：它们各有价值，但不能替代学术生命周期治理，且会显著增加双真相源、数据库运维和模式迁移风险。

对“LLM Wiki”的具体判断是：

- **理念成立**：原始资料不可变，AI 把它编译为持续更新、可查询的结构化 Wiki；
- **默认治理不够**：通用 LLM Wiki 往往围绕页面、摘要和链接，而本项目需要的是 claim、证据定位、冲突、身份候选、kill condition、决策和 supersession 的生命周期；
- **最值得试点的实现是 `llm-wiki-compiler`，不是直接迁移**；它目前仍存在足以阻止无条件采纳的成熟度问题；
- **LLM Wiki 必须是可删除、可重建的派生层**。删除它后若丢失任何唯一学术判断或审批证据，架构即不合格。

因此，本报告给出的不是“安装批准”，而是一个**带 kill 条件的隔离试点建议**。在试点通过前，不迁移当前 Wiki，不允许代理直接写入事实正典，不改变团队现行文件。

---

## 1. 先纠正需求：这不是“笔记软件选型”

Survey 在 L4 技术探索中至少同时承担六项工作：

1. **发现**：系统地扩展论文、方法、任务和反例；
2. **辨认**：解决同一论文多个版本、同一方法多个名称、同名异构等问题；
3. **论证**：把“某论文存在”转成“它支持或反驳哪个可审计命题”；
4. **比较**：在统一 operator、信息边界、供给条件、任务和指标下比较，而不是按论文段落抄摘要；
5. **决策**：记录为何保留、淘汰或重写研究身份候选；
6. **协同**：让人和 AI 都能读取上下文、提出增量，但不能绕过证据和审批规则。

“能全文搜索”“能聊天”“能自动总结”“能生成 Wiki 页面”都只是辅助能力。若一个系统不能回答以下问题，它就不能作为本项目的 Survey 正典：

- 这条主张对应论文的哪个版本、哪一页/表/公式/代码位置？
- 这是作者原话、评审者解释、AI 抽取候选，还是团队已审批判断？
- 这条证据支持、限制、反驳还是仅仅相关？
- 何时、由谁、基于什么新证据改变了状态？
- 某个“研究空白”是否只是检索遗漏、名称不一致或 scope 被悄悄移动？
- 能否从原始资料和事件账本冷启动重建全部派生页面？
- 能否证明 AI 的回答没有把另一段 AI 摘要循环当作一手证据？

据此，选型重点是**学术知识生命周期与信任边界**，不是编辑器体验。

---

## 2. 强制信任分层

建议采用以下五层模型：

| 层级 | 内容 | 可否作为 Stage gate / novelty / kill 的直接证据 | 写权限 |
|---|---|---:|---|
| T0 原始证据层 | PDF、HTML/代码快照、数据集卡、原始检索响应、内容哈希 | 是，但仍需解释 | 只追加/换版，不覆盖 |
| T1 人审正典层 | 文献身份、claim、证据定位、screening、冲突、决策、supersession | 是 | 人类审批或受控 PR 合并 |
| T2 AI 候选层 | 自动抽取的 claim、关系、摘要、去重建议、反例 | 否 | AI 可写，必须待审 |
| T3 编译导航层 | Wiki 页面、topic synthesis、图、context pack、索引 | 否；只能回链 T0/T1 | 编译器重建 |
| T4 会话临时层 | Chat、agent scratchpad、即时 RAG 回答 | 否 | 临时、可丢弃 |

核心不变量：

> T2–T4 可以提出调查方向；只有回到 T0，并经 T1 的显式判断，才可影响研究结论。

这条规则比选哪一个产品更重要。没有该分层，任何高级 GraphRAG 或 LLM Wiki 都只会更高效地产生难以审计的“知识幻觉”。

---

## 3. 开源实现核查

### 3.1 “LLM Wiki”不是一个唯一项目

[Karpathy 的 LLM Wiki 设计说明](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)描述的是一种架构模式：原始 sources 是 source of truth，LLM 按 schema 持续“编译”出 Wiki，并提供 ingest、query、lint、版本控制和矛盾/陈旧检查。这个方向非常适合 Survey 知识编译。

但该模式中“LLM owns the wiki”的说法，不能不加修改地用于学术研究。对本项目应改写为：

> LLM 可以拥有派生页面的生成过程；人类和受控规则拥有事实状态、证据解释及研究决策。

目前同名或近名实现至少有以下几类，不能混为一谈。

#### A. `atomicstrata/llm-wiki-compiler`

官方仓库：[atomicstrata/llm-wiki-compiler](https://github.com/atomicstrata/llm-wiki-compiler)

这是本轮最接近需求的实现。它提供：

- typed entities / relations；
- configurable lifecycle profile 和 fail-closed transition；
- 内容哈希锁定的审批；
- review queue、freshness、claim/source-line citation；
- lint、eval、JSON/JSON-LD/GraphML/OKF 导出；
- SDK、CLI、MCP 和 context pack；
- 内置 [AutoSci profile](https://github.com/atomicstrata/llm-wiki-compiler/blob/main/docs/guides/autosci-research-workflow.mdx)，包含 paper、idea、experiment、review 等科研对象；
- [sources contract](https://github.com/atomicstrata/llm-wiki-compiler/blob/main/SOURCES_CONTRACT.md)，明确 source hash、模型与 prompt version、行级 claim 和增量编译；
- [MCP agent integration](https://github.com/atomicstrata/llm-wiki-compiler/blob/main/docs/guides/mcp-agent-integration.mdx)，允许只读 context pack，并把外部导入停在待审批状态。

**优点**：它不是单纯“页面生成器”，而是尝试把 lifecycle、证据引用、审批和编译确定性纳入运行时。其范式与本项目已有的 Git 正典、哈希正典、Stage gate 以及 AI 审阅需求相容。

**严厉保留意见**：

1. 该项目非常新，v1.0.0 在本审查日前不久发布，不能把 API 稳定性或长期维护视为已验证；
2. 默认 AutoSci 是通用科研 profile，不含本项目最关键的 claim/evidence/identity/kill condition/supersession 完整对象；
3. 本地审计发现，文档宣称实验完成需要健康 result artifact，但当前运行时 profile 检查显示 artifact precondition 未启用；源码中的 `experiment.complete` 约束也未体现相同的 artifact transition requirement。这不是措辞小问题，而是“文档说门存在、运行时实际未锁门”的控制面差异；
4. Windows 临时沙箱中 `template init autosci` 因 `wiki/papers` 路径边界判断失败；全量测试还因 `spawn npx ENOENT` 的 Windows 兼容问题未能启动。项目目标运行环境是 WSL2，这不能直接证明 WSL 失败，但也不能声称跨平台验证通过；
5. 若直接把生成 Wiki 当正典，会重演 AI 页面覆盖人工判断的问题。

**结论**：进入锁版本、隔离、只写候选区的试点；禁止直接部署为团队正典。

#### B. `nashsu/llm_wiki`

官方仓库：[nashsu/llm_wiki](https://github.com/nashsu/llm_wiki)

它提供桌面/网页体验、不可变 raw sources、source traceability、知识图、语义搜索、异步审查队列、deep research、API/MCP 与 Codex 集成，产品完整度较高。

**适合**：个人/小组资料浏览、来源回链、图形导航、人与 AI 的异步审阅体验。

**不足**：公开设计更偏页面和知识库产品；没有充分展示本项目所需的 claim-level 状态机、研究身份候选、kill condition、阶段门与 Git 正典一致性。GPLv3 也意味着未来分发或深度嵌入时需要单独审查许可证影响。

**结论**：可作为 UI 体验参照或个人浏览器；不作为当前团队正典首选。

#### C. `lucasastorian/llmwiki`

官方仓库：[lucasastorian/llmwiki](https://github.com/lucasastorian/llmwiki)

它提供本地/远程使用、Web UI、MCP 读写、多种文档摄入、来源/crosslink/graph，许可证宽松。

**适合**：快速搭建可浏览、可被 agent 访问的 Wiki。

**不足**：公开材料没有证明其具备学术 claim 生命周期、细粒度证据审批和研究决策门；本审查时也缺乏稳定 release 信号。

**结论**：工程轻便，但治理能力不足；不优先于 `llm-wiki-compiler`。

### 3.2 文献身份与元数据层

#### Zotero + citation key/Better BibTeX

[Zotero](https://github.com/zotero/zotero)仍然适合承担人工文献库、附件、批注、collection 和引用导出。[Better BibTeX](https://github.com/retorquere/zotero-better-bibtex)可为文本/Git 工作流提供稳定 citation key 与自动导出；考虑到新版 Zotero 已强化 citation key，试点时应验证哪些能力仍需 BBT，而不是机械地叠加插件。

Zotero 不应承担 claim graph 或研究决策。它解决的是“这是什么文献、附件在哪里、人如何阅读与引用”，不是“这条证据如何改变研究身份”。

#### OpenAlex + arXiv + Crossref

[OpenAlex API](https://developers.openalex.org/api-reference/introduction)适合 DOI、work/author/source、引用和 related works 查漏；arXiv API/页面负责预印本编号与版本；Crossref 负责 DOI 元数据。三者必须按标识符优先级合并，不能只凭标题字符串去重。

建议正典身份至少保存：

- DOI（如有）；
- arXiv ID + version；
- OpenAlex work ID；
- venue/year/status；
- source URL 与检索时间；
- 内容哈希；
- “同一 work 的不同版本”与“不同 work 的相似标题”两个不同关系。

### 3.3 AI Survey / 问题扩展层

#### STORM / Co-STORM

[Stanford STORM](https://github.com/stanford-oval/storm)通过多视角提问、检索和大纲合成生成 Wiki 风格长文；Co-STORM 加入人机协作讨论和动态 mind map。官方也明确生成内容仍需人工编辑。

对本项目最有价值的不是让它写“最终 Survey”，而是：

- 生成互相冲突的搜索视角；
- 补充跨模态、文本 LLM、vision LLM、test-time search/selection 等检索车道；
- 生成反例问题和未覆盖的比较轴；
- 把每次搜索计划与结果落成 SearchEvent / SearchResult 候选。

**禁止用途**：不得把 STORM 生成段落本身当论文证据；不得让其自动给研究空白盖章；不得绕过原文定位。

### 3.4 时间化知识图层

#### Graphiti

[Graphiti](https://github.com/getzep/graphiti)支持 episode/provenance、时间有效区间、增量更新、可规定 Pydantic ontology、混合图检索和 MCP，适合回答：

- 某身份候选在什么时间、因何证据被降级？
- 某 claim 何时被新版本论文限制或反驳？
- 当前判断与 7 月 11 日判断为何不同？

但其事实和关系往往由 LLM 抽取/更新，不能直接成为学术真相。若采用，它只能从 Git 的 T0/T1 事件重建，图中任何自动 invalidation 都必须回写为待审建议，而不是静默改变正典。

**结论**：列为第二阶段增强项；先证明图查询需求，再承担 Neo4j/FalkorDB 等运维与双存储一致性成本。

### 3.5 重型语义/GraphRAG 平台

#### Wikibase

[Wikibase 数据模型](https://www.mediawiki.org/wiki/Wikibase/DataModel/Primer)在 epistemic 设计上非常优秀：statement、qualifier、reference、rank 能表达有争议、带条件、非唯一真值的学术主张。它值得作为 schema 设计参照。

但 Wikibase 是重型服务，不是 Git-native；本项目需额外开发 AI 生命周期、审批、差异评审和构建回放。Stage-1A 当前不值得为公共知识基础设施付出这笔成本。

#### TrustGraph

[TrustGraph](https://github.com/trustgraph-ai/trustgraph)提供 GraphRAG、RDF/ontology、agent/MCP 和较强 provenance；其文档展示 document→page→chunk→edge 的溯源链与查询推理记录。

它适合多项目、强图查询、语义集成或受监管场景，但会引入图数据库、向量存储、流水线和服务运维。它并不自动提供本项目的 Stage-1A screening/identity/kill 生命周期。

**结论**：当前明显过度建设；只有知识规模、跨团队联邦或合规要求超过 Git-native 方案后再重评。

#### Microsoft GraphRAG / RAGFlow

[Microsoft GraphRAG](https://github.com/microsoft/graphrag)适合从文档中抽取实体、关系、community summary 并改善 global/local query；官方同时提醒索引成本和版本迁移问题。[RAGFlow](https://github.com/infiniflow/ragflow)擅长文档解析、RAG 和 agent 服务。

两者都不是研究治理系统：它们不会自然管理 screening 决定、研究身份、证据强度、kill condition 或 supersession。若 PDF 解析或大规模语料问答成为瓶颈，可把它们当派生检索后端；不得反客为主。

---

## 4. 候选适配矩阵

评分为本轮评审启发式判断（高/中/低），不是性能 benchmark。

| 组件 | 学术身份 | claim/证据 | 人审门 | Git/可重建 | AI 协同 | 运维成本 | 当前角色判定 |
|---|---|---|---|---|---|---|---|
| Git + schema | 高 | 高（需自定义） | 高 | 高 | 中 | 低 | 唯一正典 |
| Zotero + BBT | 高 | 低 | 中 | 中 | 中 | 低 | 文献与附件入口 |
| OpenAlex/arXiv/Crossref | 高 | 低 | 不适用 | 高（缓存响应） | 高 | 低 | 身份核对与查漏 |
| llm-wiki-compiler | 中/高 | 高潜力 | 高潜力 | 高 | 高 | 中 | 首选隔离编译试点 |
| nashsu/llm_wiki | 中 | 中 | 中/高 | 中 | 高 | 中 | UI/个人知识库备选 |
| lucasastorian/llmwiki | 中 | 中 | 低/中 | 中 | 高 | 中 | 快速 Wiki，不作正典 |
| STORM/Co-STORM | 低 | 低 | 低 | 中 | 高 | 中 | 搜索视角/问题扩展 |
| Graphiti | 中 | 中/高 | 需外建 | 中 | 高 | 中/高 | 后置时间图投影 |
| Wikibase | 高 | 高 | 中 | 低/中 | 需定制 | 高 | schema 参照，暂不部署 |
| TrustGraph | 中/高 | 高 | 需定制 | 中 | 高 | 很高 | 规模化后重评 |
| GraphRAG/RAGFlow | 低/中 | 中 | 低 | 中 | 高 | 高 | 检索后端，不作治理层 |

关键结论：没有单一开源项目同时在“文献管理、claim 证据、研究决策、AI 协同、Git 审计、低运维”上成立。**组合是必要的，但组合必须只有一个正典。**

---

## 5. 三种可选组合架构

### 方案 A：Git-native 编译栈——当前推荐

```text
Zotero / OpenAlex / arXiv / Crossref
                 |
                 v
       T0 原始来源与检索快照
                 |
        AI 提取候选（T2）
                 |
          人审 PR / 哈希审批
                 v
   T1 Git 正典：claim / evidence / decision
                 |
        确定性编译 / lint / eval
                 v
 T3 LLM Wiki / MCP context pack / 图与页面
```

组成：现有 Git + schema；Zotero/BBT；OpenAlex/arXiv/Crossref；锁定版本的 `llm-wiki-compiler` custom profile；STORM 可选。

**优势**：与现有团队流程最接近；审计清楚；生成层可删除；无需长期数据库；最适合 Stage-1A 快速探索又不牺牲证据纪律。

**风险**：需要设计自己的科研 ontology、校验器和审批路径；`llm-wiki-compiler` 尚新，不能免测。

**综合判断**：当前首选。

### 方案 B：Git-native + Graphiti 时间图

在方案 A 后增加由 T1 事件构建的 Graphiti 投影，用于时间、冲突和 agent memory 查询。

**优势**：对“判断如何演化”“哪条旧结论已被何物 supersede”更强；复杂关联查询更自然。

**风险**：正典和图之间会出现一致性压力；LLM 抽取边可能误改事实有效期；需要图服务运维。

**进入条件**：至少出现 10 个稳定、反复使用且文本/SQL/静态索引难以满足的时间图查询；所有图数据可从 Git 冷重建；不得有图独占事实。

**综合判断**：保留为后置升级，不应首日安装。

### 方案 C：Wikibase/TrustGraph 中心化语义栈

把公开语义模型、图数据库和 GraphRAG 作为中心，人和 AI 都围绕它工作。

**优势**：适合更大规模、跨团队共享、复杂 ontology、公共服务和联邦查询。

**风险**：迁移和运维成本最高；Git 审查体验下降；必须另造阶段门；容易在 Stage-1A 把大量时间花在知识平台而不是研究问题上。

**综合判断**：当前拒绝。未来只有在规模与共享需求被数据证明后重启评估。

---

## 6. `l4-survey` profile 的最低 ontology

默认 AutoSci profile 不足以表达本项目的 Survey 决策。试点至少应包含以下对象；名称可与项目术语表对齐，但语义不得合并偷懒。

| 对象 | 最低必填字段 | 主要不变量 |
|---|---|---|
| PaperWork | canonical IDs、题名、作者、venue/status | work 与 version 分离 |
| PaperVersion | version ID、日期、URL、content hash | 所有 evidence 指向具体版本 |
| SearchEvent | query、数据库、时间、filters、执行者、原始响应 hash | 检索可回放，失败也保留 |
| SearchResult | result ID、rank、命中原因、dedup link | 不得只保留最终纳入项 |
| ScreeningDecision | include/exclude/defer、理由、reviewer、时间 | 排除理由可审计 |
| Claim | 精确命题、scope、status、作者/团队/AI 来源 | 一个 claim 不混多个命题 |
| EvidenceSpan | source version、页/段/表/公式/行、摘录 hash | 必须可定位回原文 |
| SupportRelation | supports/limits/contradicts/related、strength、理由 | “提到”不等于“支持” |
| MethodOperator | 输入、状态、动作、信息边界、是否改权重/结构 | 防止按营销名比较 |
| IdentityCandidate | I1–I4 等问题定义、必要条件、当前状态 | 不能由 AI 自动 proceed |
| Conflict | 冲突双方、冲突类型、待核查项、resolution | 冲突不被平滑摘要吞掉 |
| KillCondition | 触发谓词、证据要求、裁决人 | 必须可机器检查一部分 |
| Proposal | 问题、假设、替代解释、验证钩子 | 仍属 Stage-1A 候选 |
| Decision | owner decision、依据、被拒选项、日期 | 不得自动滚入 Stage-2 |
| ExperimentHook | future observable、控制、泄漏风险 | 不是当前实验结果 |
| Supersession | old record、new record、原因、日期 | 更正不覆盖历史 |

至少建立以下关系：

- `version_of`、`found_by`、`screened_as`；
- `asserted_by`、`supported_by`、`limited_by`、`contradicted_by`；
- `implements_operator`、`uses_information`、`compares_against`；
- `occupies_identity`、`leaves_open`、`challenges_novelty`；
- `triggers_kill`、`motivates_proposal`、`supersedes`；
- `derived_from`、`approved_from_candidate`。

学术门不能只检查字段存在，还必须检查跨对象条件，例如：

- `Claim.status=accepted` 前至少有一个非 AI 的 EvidenceSpan，且具体版本和定位可用；
- load-bearing claim 至少两名角色中有一名人类 reviewer；
- `IdentityCandidate.status=proceed` 只能由 owner decision 触发；
- `KillCondition.triggered=true` 必须绑定裁决证据；
- AI 不得把 T3 Wiki 页面作为 EvidenceSpan 的 primary source；
- `PaperVersion` 改变时，相关 EvidenceSpan 必须标记 freshness review；
- 任何同名方法若 operator 不同，必须拆成不同对象。

---

## 7. AI 协同权限模型

### 7.1 推荐权限

| 动作 | AI | 人类 reviewer | owner |
|---|---:|---:|---:|
| 搜索和生成候选 | 允许 | 允许 | 允许 |
| 创建 T2 claim/evidence 候选 | 允许 | 允许 | 允许 |
| 修改 T0 原始内容 | 禁止 | 禁止；只能新增版本 | 禁止覆盖 |
| T2→T1 审批 | 禁止自批 | 允许 | 允许 |
| 更改研究身份状态 | 建议，不裁决 | 评议，不最终裁决 | 裁决 |
| 触发 kill/proceed | 建议并给证据 | 复核 | 最终裁决 |
| 生成 T3 Wiki/context pack | 允许 | 允许 | 允许 |
| 直接用 T3 支持结论 | 禁止 | 禁止 | 禁止 |

### 7.2 防止循环污染

每条 AI 输出必须记录：

- 输入 context pack 的版本/hash；
- 模型 ID、prompt/template 版本；
- 输出 candidate hash；
- 引用的 T0/T1 record IDs；
- 是否发生外部检索及其 SearchEvent；
- 审批人和审批的精确内容 hash。

代理默认只获得 T1/T3 只读 MCP；写入只能进入 candidate/review branch。即使工具支持 MCP write，也不应把“接口能写”误当作“代理被授权写正典”。

---

## 8. 两天隔离试点 proposal

这不是迁移计划，而是选型实验。必须在独立目录或独立试验仓库进行，不接管现有 `wiki/`。

### Day 1：可运行性和 schema 门

1. 在 WSL2 用户空间安装隔离 Node 24 工具链；不触碰 `speechrl` Python venv；
2. 锁定 `llm-wiki-compiler` v1.0.0 及精确 commit，不追 `main`；
3. 在 WSL 执行 install、build、官方 tests 和 AutoSci init；记录完整日志与 hash；
4. 建立最小 `l4-survey` profile；
5. 为 claim 审批、artifact 健康状态、owner-only decision、supersession 编写门控回归测试；
6. 验证文档宣称的门和运行时门完全一致。

### Day 2：十篇论文的对抗式知识回放

选取覆盖以下问题的约 10 篇/项目资料：MBR、best-of-N/selection、speech/omni selector、test-time revision、reward hacking、STORM/知识组织、时间图或 provenance。不是为扩大 survey 结论，而是测试知识系统。

必须完成五项对抗任务：

1. **身份去重**：同一 arXiv 多版本和标题别名不得形成重复 work；
2. **逐条追证**：一个关键效果数字必须从 claim 回到正确版本、页/表/行与原文 hash；故意注入错误区间，系统必须把它挡在 T2；
3. **operator 辨析**：能区分 selection、revision、training、retrieval/new-info，不因论文都使用 reward 就合并；
4. **研究空白审计**：能表达“宽泛问题已被占据，但受额外条件约束的交集仍待查”，且保留 scope 变化记录，不能自动包装成 novelty；
5. **全链回放**：从 raw sources + event log 冷构建 T1/T3，审批、冲突和 supersession 不丢失。

### 验收门

以下全部通过才允许进入更大试点：

- 100% 论文有 canonical identity 和具体版本；
- 100% load-bearing claims 有 source locator、version、content hash；
- 0 条 AI candidate 未经审批进入 T1；
- 0 条 T3/T4 内容被登记为 primary evidence；
- clean clone 冷构建后所有正典 ID、关系和审批 hash 一致；
- 删除编译输出后能完全重建，无唯一事实损失；
- 所有生命周期门有正例和负例回归测试；
- WSL2 官方测试与本项目门控测试通过；若上游测试因环境问题失败，状态必须是未通过，而不是“基本通过”；
- 独立 reviewer/AI 能仅凭导出的 context pack 回答问题，并把每个关键判断回链 T0/T1；
- 对 intentionally wrong claim、stale version、AI self-citation、missing artifact 四类攻击全部 fail closed。

### 立即 kill / pivot 条件

满足任一项即停止迁移，不以“以后再补”豁免：

1. profile 无法在运行时真正强制 claim/decision/artifact 门；
2. 文档规则与运行时约束再次出现不可自动检测的偏差；
3. 必须手工维护两个事实源，且不能证明单向重建；
4. context pack 丢失证据 locator 或混淆 T1/T2/T3；
5. 冷重建改变审批、关系或对象 ID；
6. AI 能通过引用生成 Wiki 页面绕过原始证据；
7. 每条关键 claim 的结构化录入与审批成本显著高于现行模板，却没有带来可量化的查错、查重或回放收益；
8. WSL2 安装、测试或升级要求污染主研究环境；
9. 项目维护节奏、破坏性变更或许可证条件不适合团队持续使用。

若编译器被 kill，保留 ontology 和验收集，回退到 Git + schema 的最小实现；不得因为工具失败而放弃知识纪律。

---

## 9. 本轮对 `llm-wiki-compiler` 的临时沙箱核查记录

本轮未在项目中安装任何依赖，未修改现有团队文件。只在系统临时目录对上游仓库进行了非生产核查。

- 上游审计 commit：`bed4dda13f5d4ea61d7cf635a9422d3c2740668e`；
- `npm ci --ignore-scripts`：通过；
- `npm run build`：通过；
- `template inspect autosci`：可运行，报告 12 entity、12 relation、5 workflow、7 artifact；relation preconditions 为 true，artifact preconditions 为 false；
- Windows `template init autosci`：失败，报 entity directory `wiki/papers` 未被识别为位于 `wiki/` 下，疑似路径分隔符/边界校验兼容问题；
- Windows 全量测试启动：未通过，global setup 出现 `spawn npx ENOENT`；因此不能声称上游 tests passed；
- 静态核对：AutoSci 文档要求 experiment 完成时存在健康 result artifact，但当前 profile 源码的 `experiment.complete` 仅体现摘要/关系等条件，未看到相同 artifact transition requirement；与 inspect 输出一致。

以上结果不是对项目质量的最终判决。它们说明：

1. 该实现有实质能力，不是概念仓库；
2. 它仍未达到“拿来即用、默认控制可信”的程度；
3. WSL2 上必须重新跑完整测试；
4. 本项目必须用自己的门控回归测试验证真实运行时，不能只阅读文档。

---

## 10. 什么时候才需要更重的系统

不要把“未来可能有很多知识”当作今天部署图平台的理由。只有出现下列可观测信号时才升级：

- 论文/版本/claim 数量使 Git 静态索引无法在可接受时间回答常用查询；
- 多个独立研究 work 需要共享同一 ontology 和引用身份；
- 时间化冲突查询成为高频工作，而不是演示需求；
- 需要向外部团队公开 SPARQL/RDF 或公共知识门户；
- 对 agent 的跨会话动态 memory 有明确评测集；
- 已证明 Graphiti/Wikibase/TrustGraph 能在查错率、召回率、回放时间或人审成本上显著胜过方案 A。

升级时仍保持：Git/T0/T1 是可导出正典，重型服务是派生索引；除非另行完成数据治理评审，不允许悄悄倒置。

---

## 11. 对研究团队的明确要求

1. 不再把“我们有 Wiki/Graph/RAG”描述成知识组织已经完成；必须报告对象、状态机、证据门和信任边界；
2. Survey response 模板中的回放字段应保留，但升级为 SearchEvent、Claim、EvidenceSpan、Conflict、Decision 和 Supersession 的结构化记录；
3. AI 只能提交候选差异；load-bearing claim、novelty、kill/proceed 必须显式人审；
4. 所有生成页面必须标注其派生性、build commit、schema/profile version、source snapshot 和生成时间；
5. 对任何外部工具，先建立验收集与 kill 条件，再安装和迁移；
6. 不得因工具 UI 漂亮而绕过当前 Git 历史、日期报告与 owner 决策；
7. 不得把自动 graph edge、embedding 相似或 LLM synthesis 表述为论文之间已经成立的学术关系；
8. 工具选型的成功指标应是：漏检/误引/版本混淆/循环引用下降，争议定位和决策回放加快，而不是生成了多少页面或图节点。

---

## 12. 最终签署意见

**建议批准“方案 A 的隔离试点”，不批准“直接采用某个 LLM Wiki 并迁移现有知识库”。**

`atomicstrata/llm-wiki-compiler` 是当前最值得认真试的开源实现，因为它已触及 typed relation、lifecycle、hash-pinned review、source-line claim 和 MCP context pack，这些正是学术 AI 协同所需要的基础机制。但本轮实际核查已经发现文档/运行时 artifact gate 差异与 Windows 可运行性问题；其默认 AutoSci schema 也不足以表达 L4 Survey 的研究身份与决策纪律。因此它目前是**高潜力、低成熟度置信的候选**，不是可无条件信任的基础设施。

最稳妥的路线是：

> 先把知识对象、信任区和审批门定义正确，再让 LLM Wiki 编译它；不要先安装一个 Wiki，再让研究方法适应产品已有的数据模型。

这也回答了“重放是否足够”：不够。重放只证明过程能再跑；一个合格的 Survey 知识系统还必须能表达证据、冲突、条件、时间、决策和被淘汰的替代解释，并且让 AI 扩展认知覆盖而不获得篡改学术正典的权力。

---

## 13. 主要官方资料

- [Karpathy: LLM Wiki design pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [atomicstrata/llm-wiki-compiler](https://github.com/atomicstrata/llm-wiki-compiler)
- [llm-wiki-compiler Sources Contract](https://github.com/atomicstrata/llm-wiki-compiler/blob/main/SOURCES_CONTRACT.md)
- [llm-wiki-compiler AutoSci workflow](https://github.com/atomicstrata/llm-wiki-compiler/blob/main/docs/guides/autosci-research-workflow.mdx)
- [llm-wiki-compiler MCP integration](https://github.com/atomicstrata/llm-wiki-compiler/blob/main/docs/guides/mcp-agent-integration.mdx)
- [nashsu/llm_wiki](https://github.com/nashsu/llm_wiki)
- [lucasastorian/llmwiki](https://github.com/lucasastorian/llmwiki)
- [Zotero](https://github.com/zotero/zotero)
- [Better BibTeX for Zotero](https://github.com/retorquere/zotero-better-bibtex)
- [OpenAlex API](https://developers.openalex.org/api-reference/introduction)
- [Stanford STORM / Co-STORM](https://github.com/stanford-oval/storm)
- [Graphiti](https://github.com/getzep/graphiti)
- [Wikibase Data Model Primer](https://www.mediawiki.org/wiki/Wikibase/DataModel/Primer)
- [TrustGraph](https://github.com/trustgraph-ai/trustgraph)
- [Microsoft GraphRAG](https://github.com/microsoft/graphrag)
- [RAGFlow](https://github.com/infiniflow/ragflow)
