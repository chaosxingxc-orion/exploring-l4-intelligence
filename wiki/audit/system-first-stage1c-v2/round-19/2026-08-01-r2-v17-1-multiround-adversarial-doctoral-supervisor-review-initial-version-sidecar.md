---
title: "R2 v17.1 多轮隔离对抗式博导审查：方向值得保留，但须收敛为可识别的双源选择性控制问题"
date: "2026-08-01"
artifact_type: "REVIEW"
campaign: "system-first-stage1c-v2"
round: "round-19"
review_target: "wiki/survey/workbench/stage1c-portfolio/proposals/2026-07-29-r2-coreview-draft.md"
review_target_commit: "2d2cf52049d8d6d962abf8dc7fcaf3499f6e0ced"
review_target_git_blob: "bbc41c9eb8eec26c480f2c4f0fde96ea32ce488a"
review_target_blob_sha256: "2bf9b7ae5044dc226609a8391aece9ac6b72d5268b461abd403d69b52650fbb4"
review_target_size: "121,701 bytes; 1071 lines; Git blob bytes"
evidence_cutoff: "2026-08-01"
verdict: "MAJOR_REVISION_REQUIRED_BEFORE_FORMAL_OPENING"
major_count: 7
minor_count: 8
signature_ready: false
formal_opening_authorized: false
permission_note_issued: false
fresh_search_performed: true
isolated_adversarial_panels: 3
authority_effect: "REVIEW_ONLY_NO_OWNER_DECISION_NO_EXECUTION_GRANT"
human_signature_claimed: false
model_or_metric_execution_authorized: false
stage2a_authorized: false
novelty_verdict: "NOT_ISSUED_EXACT_INTERSECTION_REMAINS_PLAUSIBLE_BUT_UNPROVEN"
---

# R2 v17.1 多轮隔离对抗式博导审查

## 一、裁决摘要

**裁决：`MAJOR_REVISION_REQUIRED_BEFORE_FORMAL_OPENING`。当前不建议签字正式开题，不出具允许开题 notes。**

这不是对研究方向的否定。相反，经过三路隔离审查、主审重新检索和决定性原文复核后，我认为
本题仍有一个值得做、也可能形成博士级贡献的技术核：

> 在确有可验证外部信息缺口、同时存在声学歧义的任务上，为冻结黑盒 omni 核构造一个外置
> 控制器，使其按样本在“重新取得/重解析音频观测”和“查询外部知识”之间选择；在同核、同
> 证据池、同动作机会和同成本约束下，证明选择策略优于最强单源策略、固定串行组合与随机
> 路由，并通过证据准入机制控制 correct→wrong。

但当前报告还不是这一个命题。它同时承载了能力上界、发音库、个性化、多面知识组织、动态
切片、知识供给、准入与融合、contextual bandit、TFRL 身份、自建载体和跨系统 ASR 比较。
报告的材料量已经足够支持多篇论文，然而第一项确认性实验尚未对应一个唯一、无歧义的因果
估计量。更严重的是，本轮新检索发现了 **PlanRAG-Audio** 和 **GRGA** 等 2026 年直接近邻，
它们已经占据提案 §3.3 所称“语音域读集内全部缺席”的相当部分。因此，当前问题不是“参考
文献数量不够”，而是**最近邻覆盖、概念分层和主张—实验蕴含关系尚未闭合**。

正式开题前必须关闭本件七项 MAJOR。关闭后，本人倾向于再审一个收窄后的
`CONDITIONAL_GO`，但不预承诺通过。

## 二、审查对象、隔离方式与证据边界

### 2.1 对象绑定

- 提案路径：`wiki/survey/workbench/stage1c-portfolio/proposals/2026-07-29-r2-coreview-draft.md`
- 审查提交：`2d2cf52049d8d6d962abf8dc7fcaf3499f6e0ced`
- Git blob：`bbc41c9eb8eec26c480f2c4f0fde96ea32ce488a`
- blob SHA-256：`2bf9b7ae5044dc226609a8391aece9ac6b72d5268b461abd403d69b52650fbb4`
- 大小：121,701 bytes；1071 行；以 Git blob bytes 为准。

### 2.2 多轮对抗协议

本轮不是在既有结论上顺推，而是使用三个互不共享历史评审上下文的隔离面板重新审查：

1. **概念—因果面板**：只审“知识为何需要、三种形式是否互斥、模块与实验能否一一归因”。
2. **文献—占位面板**：从 2021–2026 重新搜索 acoustic exemplar、contextual ASR、audio
   RAG、agent planning、black-box correction、phonetic-semantic rescoring、Earnings21/22
   等邻域，只接受论文官方页、ACL/ISCA/AAAI、arXiv 和作者官方仓库。
3. **方法—统计面板**：只审主载体、对照臂、统计决策、效率、运行时保真和单人可执行性。

主审随后独立深读决定性一手文献，对三个面板进行反向质询。最后采用最强反方测试：**假定
报告中所有主要实验都得到正结果，这些结果是否必然推出作者想写进论文标题的结论？** 当前
答案是否定的。

三个隔离面板的票决分别为：概念—因果面板 `MAJOR_REVISION / NO_SIGN`，文献—占位面板
`MAJOR_REVISION / NO_STAGE1C_GO`，方法—统计面板
`NO_GO_AS_WRITTEN_FOR_FORMAL_PROPOSAL`。三者独立地把可保留的技术核收敛到双源按样本
选择；分歧主要在整改范围，而不在当前能否签字。主审又发现隔离文献面板未命中的
PlanRAG-Audio/GRGA，使否决证据只增不减。

本轮只做文献与文档审查；未运行模型、数据、指标或原型，未授予 Stage-2A 权限。本件是 AI
生成的学术评议，不冒充自然人博导签字，最终学术与执行裁量仍归 owner。

## 三、首先把三个“形式”说清楚

提案在 §1.3 和 §6.2 已给出接近正确的词典，但它只在定义层清楚，进入运行时动作集、模块和
实验后又重新混层。建议采用下面这一套唯一语义，不允许同一名词在不同章节换层：

| 层 | 唯一问题 | 输入→输出 | 可以改变的变量 | 不属于本层的内容 |
|---|---|---|---|---|
| **ORG：知识组织形式** | 已有知识被做成什么可寻址对象？ | 原始材料→带 schema、版本、出处和索引的知识单元 | 切片、粒度、key/value、索引、物化、版本、provenance | 是否发起查询、取多少、是否相信 |
| **SUPPLY：知识供给形式** | 对当前样本何时从哪里拿哪些候选证据？ | 当前任务状态+预算→候选证据集 | 触发、query、source、top-k、深度、停止、缓存 | 候选如何被答案采用 |
| **USE：知识使用形式** | 候选证据如何影响上下文和答案？ | 假设+候选证据→准入证据/答案/拒答 | admit/reject、融合、冲突、引用、abstain | 索引如何构造、是否再次查询 |
| **OPT/CONTROL：横切控制** | 如何选上述配置或动作？ | dev 反馈/在线状态→冻结配置或控制动作 | 规则、搜索、bandit/MDP 策略 | 不能再伪装成 ORG 的组成部分 |

还需补一个关键边界：`RE_RESOLVE` / `RE_SLICE` 是**重新取得或重表达已有观测**，不是外部
知识供给。若全篇坚持“三种知识形式”，它们必须放在知识系统之外的 `OBSERVATION CONTROL`
轨道；控制器可以在观测动作与知识动作之间选择，但不能把“重听”改名为“第二种知识”。

按此词典，现稿至少有五处错位：

- §6.3 把 `ADMIT/REJECT` 放进“查询族”，使 SUPPLY 和 USE 在动作空间中失去互斥性。
- §3.4 名义上讨论知识组织，档 B 实际优化运行期 action/query，属于 CONTROL/SUPPLY。
- `SRC-sel` 是纯 source selection，却同时绑定 K5 组织判据。
- 发音库主消融同时包含 acoustic key（ORG）、候选检索（SUPPLY）、世界知识 rescore（USE）和
  感知路由（CONTROL）；正结果不能归因到某一个层。
- `O-config` 在 SLUE-SQA-5 证明的组织增益没有进入 NB 主载体的整体臂，因而不能解释系统臂
  在 Earnings21 上的变化。

正式开题版必须只保留一张全篇唯一的映射表：

`模块 → 唯一层 → 唯一操纵变量 → 同层对照 → 主判据 → 失败出口`。

任何跨层系统臂只能回答“组合系统是否有效”，不得反向声称三个层各自成立。

## 四、把“黑盒为何需要知识”从口号变成可识别命题

**模型是黑盒，不等于模型缺知识；模型听错，也不等于需要外部知识。** 黑盒只限制可用接口，
不能自动构成引知的必要性。引入知识至少要同时满足四个条件：

1. **信息缺口**：所需事实是参数外、私域、后 cutoff、动态或被受控删除的；
2. **感知歧义**：音频观测存在多个声学上可行的候选，单纯文本后处理不能可靠区分；
3. **可达证据**：外部源中确实存在 task-time 可用、可追溯且不含答案泄漏的证据；
4. **边际可用性**：同一个冻结核在得到真证据后提升，在交换/过期/伪证据下不应盲从。

因此，“需要知识”的最小实验不是裸核 vs 大系统，而是同核上的四臂干预：

- 无证据；
- task-time 可得真证据；
- 同格式交换证据；
- 过期或冲突证据。

只有真证据相对无证据产生超过 SESOI 的增益、交换/过期证据不被无条件接受，才能分别支持
知识的**必要性**与使用的**合理性**。

现稿已经诚实地把 ConEC 主载体登记为 `IN_DISTRIBUTION_CARRIER`，并承认它不能支撑“外部
知识补足模型所缺信息”的时态结论。这一诚实声明同时意味着：当前 NB 主载体只能直接证明
“上下文偏置/实体纠错/重解码是否有效”，不能承担广义“为什么黑盒需要外部知识”的主证明。
闭卷召回探针也只能发现明显记忆，不能证明没有预训练污染。

正式开题版必须指定一个真正承重的第二载体：后 cutoff、私域或受控 held-out 事实，具有明确
`available_at`、冻结知识快照和真假/交换/过期证据干预。Earnings21+ConEC 可以继续承担实体
密集 contextual ASR 与动作选择的真实性载体，但不能独自承载知识时态结论。

## 五、重新检索后的最近邻裁决

### 5.1 决定性新发现

现稿 §3.3 声称，图/层次索引、多面 key、多粒度和面级消融在语音域读集内“全部缺席”。该
结论在 2026-08-01 的证据截止面上已不可维持：

- **PlanRAG-Audio**：从结构化音频/文本数据库中，按 query 规划所需模态和时间片，只检回相关
  信息；数据库含 speech、speaker、emotion、sound event 等多流，并显著压缩输入长度。
- **GRGA**：把语义、时间、说话人和声学属性组织成多维图，使用 query decomposition、planning、
  execution、synthesis、reflection 进行迭代检索；原文明确表述策略无需参数更新，并把过程形式化
  为 POMDP。

这两件不是“同名但无关”的论文。它们分别直接占据了 R2 的 ORG（结构化多流/多维图）、
SUPPLY（按 query 选择面与时间范围、计划检索）和部分 CONTROL（迭代计划、反思、停止）。R2
仍可主张它们没有做**外部世界知识与音频重解析之间的按样本价值校准选择**，但不得再把多面
音频组织、query-conditioned face/span selection 或 training-free audio planning 当成空白。

### 5.2 必须进入 D2/最近邻矩阵的最小集合

| 工作 | 已占据的部分 | R2 仍可能保留的差异 |
|---|---|---|
| PlanRAG-Audio (2026) | 结构化 text/audio 多流库；模态/时间片规划与检索；长音频效率 | 未见外部世界事实与重听动作的同尺度价值选择 |
| GRGA (2026) | 多维音频图；training-free agent planning；POMDP、检索与反思 | 核/接口边界不同；未见 R2 的真假证据准入与双源动作析因 |
| ATIR (2026) | 音频—文本交错查询；emotion/speaker/environment contextual retrieval | 需训练 retriever；不是 TF-strict 黑盒控制器 |
| Pundak et al. (2022) | 纠正词的 audio exemplar 记忆及声学匹配 | 白盒/生产 ASR 内部表征；不做外部事实搜索路由 |
| CB-Whisper (2024) | TTS 实体声学表征、声学检测、动态提示/解码 | 检测器有训练；不是 API-only 双源 selector |
| Multi-Pronunciation Trie (2025) | TTS 多发音、Whisper token 变体、零样本 shallow fusion | 白盒 beam；没有世界知识准入与按样本动作选择 |
| FineCoS (2022) | 细粒度 contextual knowledge selection | 训练型、白盒；说明“逐样本选上下文”本身非空位 |
| MARS (2026) | acoustic/text historical context 的多模态检索与选择 | 选的是历史上下文，不是重听 vs 外部事实动作 |
| DANCER (2024) / G-SPIN (2026) | phonetic candidate + entity description/contextual semantic rerank | 不能再把“世界知识消歧发音候选”单独作为新机制 |
| Contextual Earnings-22 (2026) | E22 realistic custom vocabulary benchmark 与六类强基线 | 应进入载体/基线合同，不能只留作未来补扫义务 |
| Interactive ASR / AgenticASR (2026) | 迭代语义纠错、intent routing、流式 active-context revision | 不含外部知识是可保留差异；但“Agentic ASR”命名空间已占 |
| RECOVER (2026，现稿已纳入) | API-only、training-free、多假设+实体纠错/外显 rescore | 无音频回访、无按样本策略选择；仍是最强同边界 incumbent |

本轮没有发现一件同时明确满足“冻结黑盒 omni + TF-strict + 按样本选择重听或外部事实搜索 +
证据准入”的直接先例；这只说明**精确交集仍可能存活**，不构成优先权或正式新颖性判决。

## 六、七项 MAJOR

### MAJOR-1：最近邻覆盖失效，§3 的空位结论和 O-config incumbent 已被直接证伪

PlanRAG-Audio 和 GRGA 的存在使 §3.3“全部缺席”、§3.4“读集内无人做”的排他性表述失效；
ATIR、MARS、Pundak、CB-Whisper、FineCoS、DANCER/G-SPIN、Contextual Earnings-22 又分别压缩
了多面检索、声学记忆、上下文选择、音义联合裁决和载体基线的空间。当前 17 件矩阵不能再称
“最近邻覆盖完成”。

**关闭标准：**

1. 对 §5.2 表中至少十二组工作做 D2 级一手审计，逐项记录 frozen/white-box、目标任务训练、
   音频回访、知识来源、被选择的对象、运行时动作、数据载体和可执行性；
2. 重写 §3.3，不再声称图/多面/规划检索为空；
3. 将 PlanRAG-Audio、GRGA 设为 T2/组织—供给轴最强结构 incumbent，ATIR/MARS 为必要邻居；
4. 将 Contextual Earnings-22 从未来义务升级为载体与基线契约的一部分；
5. 重新写独立性承重句，只允许精确落在“双源动作选择及其真假证据准入”。

### MAJOR-2：ORG/SUPPLY/USE 在定义层清楚，在模块和动作层仍不可互斥归因

当前 A4b、PS-abl、SRC-sel、O-config、B-adapt 的归属不一致；`ADMIT/REJECT` 又被列入查询族。
这导致系统正结果无法推出某一层成立，系统负结果也无法定位故障层。

**关闭标准：**用第三节的唯一映射表重写所有承重模块；`RE_RESOLVE` 独立为观测控制；OPT
只作横切层；每个承重模块只能有一个主层和一个确认性对照。跨层臂只保留为最终系统读数。

### MAJOR-3：“为何引知”没有被主载体识别，activation 与 augmentation 仍混在一起

ConEC 的 task context 可以证明 contextual conditioning 的工程价值，却不能证明外部知识补足
了参数核所缺信息。提案一方面继承“激活模型潜在知识”的北极星，另一方面又主张构造外部
知识，两者分别对应 activation 和 augmentation，不能用一个实验口径混写。

**关闭标准：**

- 把主张拆为 `H-ACTIVATE`（重表达/重听使已有能力可读出）和 `H-AUGMENT`（参数外真证据产生
  边际收益）；
- 对后者指定后 cutoff/私域/受控删除载体；
- 运行无/真/交换/过期证据干预；
- 不再用闭卷召回探针证明“未污染”；
- Earnings21 上的结论收窄为实体密集语音中的选择性上下文增强。

### MAJOR-4：A4b−A4a 不能唯一识别“双源动作选择”

A4b 相比 A4a 同时新增感知信号、`RE_RESOLVE` 价值估计、感知驱动的发音库路由和可能更多
音频计算；`β≠0` 只是权重不为零，不是机制独立性的因果证据。因此 A4b 胜出仍可能完全由更多
信息或更多调用解释。

**关闭标准：**在同一 frozen omni、同一候选池和动作匹配预算下，至少冻结以下臂：

1. NONE；
2. SEARCH-only；
3. RE_RESOLVE-only；
4. 固定 `SEARCH→RE_RESOLVE`；
5. 固定 `RE_RESOLVE→SEARCH`；
6. random/count-matched router；
7. R2 gated router；
8. oracle router。

主机制估计量必须是 gated router 相对**最强单源、最强固定串行和随机匹配路由**的增量，并
报告 2×2 source-availability interaction。首先在 dev 证明存在两类“各自独占受益样本”；若
不存在 action heterogeneity，就没有必要学习或设计双源 selector。

### MAJOR-5：主载体、终点和统计决策仍会污染确认性解释

Stage-2A“第零步”拟读取 Earnings21 全集余量后再定 SESOI、power、子切片与判据；若随后仍在
同一 E21 上作确认性检验，就把 test 变成了 design set。E22 实体标注和上下文可得性又仍是未来
义务。与此同时，多处使用“95% 下置信界 ≤0 ⇒ 判死”，把证据不足误当成实质无效。

另一个关键问题是，主终点允许“修好实体、毁掉整句”：现稿把总 WER 降为 READOUT_ONLY，
而已登记的 RECOVER 结果正好展示 E-WER 改善与总体 WER 恶化可以同时发生。

**关闭标准：**

- E21 在 SESOI、power、臂和阈值冻结前保持 untouched；只用 source-call 隔离的 E22 dev/pilot；
- 冻结 E22 entity annotation、context availability、source-level calibration/validation split，
  并审计 E21/E22 公司、人物、产品、实体字符串和检索库重叠；
- 主判据改为“实体指标 superiority **且** 总 WER/非实体 WER non-inferiority **且**
  correct→wrong 不超界”；
- 采用三态决策：`GO: LCB > SESOI`；`NO_GO: UCB < SESOI`；其余为 `INCONCLUSIVE`；
- 以 call/company 为聚类单元做 cluster bootstrap、随机化检验或 GEE/混合模型；power 不得把
  2086 段当独立样本；
- 预先冻结一个 primary hypothesis 与 multiplicity family，禁止在多配置、子桶、回退载体和
  择优基线之间事后挑选。

### MAJOR-6：合理性和效率目前是“记录项”，不是可证伪研究命题

四层评价框架比多数提案成熟，但合理性只有指标仪表盘，没有总的失败出口；效率明确“记账
不设限”，`COST_DISPARATE` 也不影响主结论。这样只能回答“测了多少”，不能回答“引知是否
合理、是否值得”。

**关闭标准：**

- 合理性必须预注册证据级失败门：真/交换/过期/冲突证据的 admit/reject、unsupported claim、
  correct→wrong、abstain coverage 和 removal/swap 反事实；
- 把 `V̂` 在完成校准前改称 heuristic score；报告 calibration curve、Brier/ECE、动作排序
  regret 和 oracle gap，而不是只看最终准确率；
- 效率至少选择一个确认性口径：质量约束下成本上界，或成本约束下效用优势；若坚持效果优先，
  就把本节准确改名“资源审计”，不得在摘要中主张效率；
- 必报 core calls、retrieval hops、audio seconds、tokens、wall-clock、API cost、RTF、峰值 VRAM、
  冷/热缓存延迟、P95，以及每个有效实体修正的完整链路边际成本；
- 所有 selector 对照必须匹配动作机会、证据量和预算，否则效率差异会重新污染机制归因。

### MAJOR-7：研究范围与 RL 身份没有收敛，首轮不可由一个确认性实验完成

现稿同时要求重实现多个无代码基线、四类载体、发音库、TTS/克隆、五路工具信号、多面索引、
动态切片、准入门、bandit、自建题集与大量消融。它适合作为博士阶段的研究组合，不适合作为
一次开题要签署的首个技术合同。

此外，当前 `state_t→action_t→更新 H/E→下一动作` 的动作会改变后继状态，更接近有限时域
MDP/POMDP，不是普通 contextual bandit；`delta_E` 又依赖 gold，只能离线评估，不能作为真实
推理期可观测 reward。若策略只在 dev 学完、test 冻结，也需要说明“training-free”究竟只限制
核心模型，还是禁止任何任务学习。

**关闭标准：**

1. 首轮只保留一个主载体、一个复制载体、一个核心机制和 5–8 个确认性臂；
2. 克隆 key、多面联邦、O-config、SLUE-SQA 组织优化、自建大基准和在线 RL 全部后置；
3. 二选一：`TF-Strict` 固定规则控制器；或允许外部控制器学习并改称 `frozen-core control`；
4. 若保留 contextual bandit，只允许在 episode 起点选择冻结宏策略；若逐步决策，则按 MDP/POMDP
   形式化，并给出 test-time 可观测 reward 或明确纯离线策略学习边界；
5. 冻结实际运行后端、量化/模型 hash、prompt、sampling、context 与音频预处理，并先做输出
   保真 gate，防止把后端退化误判成方法失败。

## 七、MINOR 与措辞修正

1. **“能力上界”过强。** 当前只是冻结配置族内的最佳已测系统，不是模型或任务上界；建议改
   “预注册配置族内最佳观测效果”。
2. **“ASR-free”不准确。** omni 核本身仍完成语音识别；应写 `dedicated-ASR-front-end-free` 或
   “无独立专用 ASR 前端”。
3. **“双源知识动作”术语漂移。** 重听不是新知识，应写“双源信息获取/控制动作”。
4. **value 建模不是实验轴。** 当前只有一页纸合同，标题不应把 key/value 均写成已验证贡献。
5. **K4 操作定义不自足。** `Knowledge-error`、`type-D`、阈值和人工 adjudication 需冻结。
6. **动态 web 不可完全重放。** URL/hash 不能恢复当时的排名和未选候选；确认性实验应用冻结
   本地快照，live web 只作外部有效性。
7. **Agentic ASR 命名冲突。** 2026 年已有 Interactive ASR/AgenticASR；R2 应避免把“agentic
   ASR”当独立命名贡献。
8. **版本元数据落后。** 正文 frontmatter 仍主要描述到 round-16/V17，而仓库当前已到 v17.1
   与 round-18 后状态；重投时必须同步正文、签字表和 review chain。

## 八、建议的最小可签开题版本

### 8.1 建议题目

**冻结黑盒语音—语言模型的双源选择性控制：重解析音频与外部知识查询的按样本路由**

### 8.2 单一核心问题

> 当冻结黑盒 omni 核面对同时包含声学歧义和参数外事实缺口的样本时，能否仅依据推理时可观测
> 信号，在重解析音频与查询外部知识之间进行按样本选择，并在同核、同证据与同成本条件下，
> 稳定优于最强单源和固定串行策略，同时不增加总体转写损害与知识盲从？

### 8.3 四个依次解锁的假设

- **H0 / Need**：真外部证据相对无证据有超过 SESOI 的同核增益；无 headroom 则停止。
- **H1 / Heterogeneity**：SEARCH-only 和 RE_RESOLVE-only 各自存在独占受益样本；否则停止 selector。
- **H2 / Selection**：gated router 优于最佳单源、最佳固定串行和随机匹配路由。
- **H3 / Safe use**：同证据集下，准入门提高真证据利用并控制交换/过期证据和 correct→wrong。

ORG 在首轮只作为固定工程实现，不立独立创新主张；O-config、个性化、面联邦和 RL 留作后续
工作。这样，三种知识形式仍被严格记录，但只有 SUPPLY/CONTROL 与 USE 进入首轮主机制检验。

### 8.4 最小执行顺序

1. **Runtime gate**：冻结模型/后端/hash/量化和输入协议，验证裸核与官方/API 的差距。
2. **Data gate**：E22 source-level dev/validation、实体标注与 task-time context；E21 untouched。
3. **Headroom gate**：只在 dev/pilot 做无/真/交换/过期证据与 oracle。
4. **Action-heterogeneity gate**：NONE、SEARCH-only、RE_RESOLVE-only、fixed-both、oracle route。
5. **Mechanism screen**：字面/别名、G2P/音素、audio exemplar/TTS key，同库同 top-k；声学 key
   不胜廉价基线即降级，克隆 key 不进入首轮。
6. **Fixed router study**：最强单源、两种串行、随机匹配、gated、oracle；同核同预算。
7. **一次性确认**：基于 dev 的簇级 power 与 SESOI 预注册后解封 E21。
8. **独立复制**：在后 cutoff/私域/受控知识缺口载体复现；否则不得外推“知识系统”。
9. **RL 后置**：只有固定门控显著、仍有策略余量且 reward 边界闭合后再决定 bandit/MDP。

## 九、值得做与暂不值得做

### 值得优先做

- 重听 vs 查知识的双源 action heterogeneity；
- 同核、同证据、同预算的静态/串行/门控/oracle 因果阶梯；
- API-only 发音候选生成与世界上下文裁决的廉价筛选；
- 真/交换/过期/冲突证据的准入与 correct→wrong 控制；
- 感知损失、检索损失、使用损失的 oracle 分账；
- 可重放 trace、簇级可靠性和每次有效修正成本。

### 首轮暂不值得做

- 音色克隆个性化；
- 情感/说话人/事件/时间锚的全量面联邦；
- Spoken-SQuAD/SLUE-SQA 上独立 O-config 方法主张；
- 在 reward 可观测性未解决前做在线 B-adapt；
- 用跨核、跨载体 trained comparator 判定知识系统因果贡献；
- 自建大基准与新方法同时确认；
- 重实现所有六组 incumbent 后才允许得到第一条机制读数。

## 十、签字门槛

下列事项应全部关闭，才值得重新申请正式开题：

- [ ] 最近邻矩阵补入 PlanRAG-Audio、GRGA、ATIR、Pundak、CB-Whisper、Multi-Pronunciation、
  FineCoS、MARS、DANCER/G-SPIN、Contextual Earnings-22 和两件 Agentic ASR；
- [ ] §3 空位结论和签字表独立性承重句完成重写；
- [ ] 模块—层—变量—对照—判据—出口唯一映射；
- [ ] activation 与 augmentation 分立，第二知识时态载体具名；
- [ ] E21 在预注册前 untouched，E22 开发协议与实体标注闭合；
- [ ] 双源八臂因果阶梯、动作机会和预算匹配；
- [ ] 单一 primary endpoint + 总体/非实体 WER non-inferiority guardrail；
- [ ] GO/NO_GO/INCONCLUSIVE 三态、簇级 power 与 multiplicity family 冻结；
- [ ] 合理性反事实门和效率判据（或明确降级为资源审计）；
- [ ] TF-Strict vs frozen-core learning 边界，以及 bandit vs MDP 身份二选一；
- [ ] 运行时后端和输出保真 gate；
- [ ] 首轮砍到一个主问题、一个主载体、一个复制载体和 5–8 个确认性臂。

## 十一、最终意见

**研究价值：高。当前开题成熟度：不足。**

现稿最可贵的地方是：已经主动承认 RECOVER 占据 API-only、training-free 和文本侧外显 rescore，
也开始使用 oracle headroom、判死条件、污染审计、成本向量与强对照。这说明研究者具备做严谨
系统研究的意识。问题不在野心不够，而在野心没有被压缩成一个确认性命题。

最强反方仍然成立：即使现有所有主臂均为正，结果也可能完全由“更多音频重试 + 更强上下文
偏置/文本纠错 + 更高调用预算”解释，而不必承认新的知识组织机制；ConEC 又不能证明参数外
知识缺口，O-config 不在同一主载体，A4b−A4a 也没有唯一隔离双源选择。因此，正结果目前不
蕴含“冻结黑盒语音知识系统成立”。

修订方向应非常明确：**保留双源选择性控制；把广义知识系统、能力上界、全量组织优化、克隆
个性化和在线 RL 从第一次开题验收中拆开。** 当最小命题、最近邻、载体、因果对照、统计判定
和资源边界同时闭合后，本课题值得再次送审。

本轮不出具允许开题 notes，`formal_opening_authorized: false`，且不产生任何 Stage-2A 执行
权限。

## 十二、聚焦一手参考文献

1. Someki et al. (2026), [PlanRAG-Audio: Planning and Retrieval Augmented Generation for Long-form Audio Understanding](https://aclanthology.org/2026.findings-acl.1304/).
2. Tang et al. (2026), [Don't Just Listen, Try Planning: Graph-based Retrieval-Generation Agent for Long-form Audio Meeting Understanding](https://aclanthology.org/2026.findings-acl.1038/).
3. Zhao et al. (2026), [ATIR: Towards Audio-Text Interleaved Contextual Retrieval](https://aclanthology.org/2026.acl-long.1006/).
4. Mu et al. (2026), [Hearing More with Less: Multi-Modal Retrieval-and-Selection Augmented Conversational LLM-Based ASR](https://ojs.aaai.org/index.php/AAAI/article/view/40528).
5. Pundak et al. (2022), [On-the-fly ASR Corrections with Audio Exemplars](https://www.isca-archive.org/interspeech_2022/pundak22_interspeech.html).
6. Li et al. (2024), [CB-Whisper: Contextual Biasing Whisper Using Open-Vocabulary Keyword-Spotting](https://aclanthology.org/2024.lrec-main.262/).
7. Liu et al. (2025), [Zero-shot Context Biasing with Trie-based Decoding using Synthetic Multi-Pronunciation](https://arxiv.org/abs/2508.17796).
8. Han et al. (2022), [Improving End-to-End Contextual Speech Recognition with Fine-Grained Contextual Knowledge Selection](https://arxiv.org/abs/2201.12806).
9. Wang et al. (2024), [DANCER: Entity Description Augmented Named Entity Corrector for Automatic Speech Recognition](https://aclanthology.org/2024.lrec-main.387/).
10. Singh et al. (2026), [Graph-Based Phonetic Error Correction of Noisy ASR](https://aclanthology.org/2026.acl-industry.151/).
11. Durmus et al. (2026), [Contextual Earnings-22: A Speech Recognition Benchmark with Custom Vocabulary in the Wild](https://arxiv.org/abs/2604.07354).
12. Jiang et al. (2026), [Towards Human-Like Interactive Speech Recognition With Agentic Correction and Semantic Evaluation](https://arxiv.org/abs/2605.29430).
13. Jiang et al. (2026), [AgenticASR: Refining Speech Recognition in Real-World Scenarios via an Agentic Approach](https://arxiv.org/abs/2607.28175).
14. Modica et al. (2026), [Do Factual Recall Mechanisms Carry over from Text to Speech in Multimodal Language Models?](https://aclanthology.org/2026.starsem-conference.28/).
15. Wang et al. (2026), [Closing the Modality Reasoning Gap for Speech Large Language Models](https://aclanthology.org/2026.acl-long.857/).
16. Huang et al. (2024), [ConEC: Earnings Call Dataset with Real-world Contexts for Benchmarking Contextual Speech Recognition](https://aclanthology.org/2024.lrec-main.328/).
17. Chan et al. (2023), [Using External Off-Policy Speech-To-Text Mappings in Contextual End-To-End Automated Speech Recognition](https://arxiv.org/abs/2301.02736).
18. Mittal et al. (2023), [Speech-enriched Memory for Inference-time Adaptation of ASR Models to Word Dictionaries](https://aclanthology.org/2023.emnlp-main.916/) (提案中的 PRISM 线).
19. Kumar and Sachdeva (2026), [RECOVER: Robust Entity Correction via agentic Orchestration of hypothesis Variants for Evidence-based Recovery](https://arxiv.org/abs/2603.16411).
20. Del Rio et al. (2021), [Earnings-21: A Practical Benchmark for ASR in the Wild](https://www.isca-archive.org/interspeech_2021/delrio21_interspeech.html).

---

**SIDECAR 尾注（非原件内容，重建时添加）**：本件为 round-19 初版评审（7 MAJOR、新颖性
驱动尺度）的**会话上下文逐字重建件**。原件于 2026-08-01 由 owner 与评审方协同纠偏时被
原位改写为「边界纠偏版」（同目录主件），改写发生在任何 Git 提交之前，故原件无 blob 可考。
重建保真度=会话转录级（重建自评审落盘当日同会话的完整 Read 记录），非字节保存级。本件
仅作审计留痕，其尺度已被纠偏版正式撤回，不具有任何裁决效力。