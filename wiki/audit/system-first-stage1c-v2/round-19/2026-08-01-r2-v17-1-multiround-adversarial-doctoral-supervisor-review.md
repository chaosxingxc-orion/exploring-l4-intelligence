---
title: "R2 v17.1 多轮隔离开题审查（边界纠偏版）：聚焦研究问题与学界现状，不作新颖性判决"
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
review_scope: "STAGE1C_PROBLEM_FORMULATION_AND_STATE_OF_RESEARCH_ONLY"
novelty_review_in_scope: false
novelty_verdict: "OUT_OF_SCOPE_FOR_CURRENT_OPENING_REVIEW"
verdict: "MAJOR_REVISION_REQUIRED_FOR_PROBLEM_AND_FIELD_CLARITY"
major_count: 5
minor_count: 5
signature_ready: false
formal_opening_authorized: false
permission_note_issued: false
fresh_search_performed: true
isolated_adversarial_panels: 3
authority_effect: "REVIEW_ONLY_NO_OWNER_DECISION_NO_EXECUTION_GRANT"
human_signature_claimed: false
model_or_metric_execution_authorized: false
stage2a_authorized: false
---

# R2 v17.1 多轮隔离开题审查（边界纠偏版）

## 一、纠偏声明与裁决

**本轮只审两件事：研究问题是否讲清楚；学术界对这个问题已经研究到什么程度是否讲准确。**

当前处于开题报告阶段，不要求证明任务或技术方案的新颖性，不做“是否首创”“交集是否被占据”
或论文优先权判决。文献的作用是建立概念谱系、解释现有方法解决了什么、尚有哪些科学问题
没有被讲清，而不是用来否决一个研究题目。

据此撤回上一版审查中把“最近邻占位”“独立性承重”和“精确新颖性交集”当作开题门槛的
尺度。PlanRAG-Audio、GRGA、ATIR、RECOVER 等工作的意义，应从“是否挤压新颖性”改为“它们
分别代表了知识组织、供给、使用或控制的哪些既有研究路线，R2 应如何把这些路线讲进学界现状”。

**纠偏后的裁决仍为：当前版本需大修后再签字，但理由与新颖性无关。** 当前提案材料充分、
技术方向合理，也具备博士研究的展开空间；阻断点是：

1. 总研究问题、子问题和系统模块之间还没有形成唯一层级；
2. 知识组织、知识供给、知识使用三个形式在定义层分开，进入运行与实验后又混在一起；
3. 学界现状按论文逐项罗列较多，但没有按上述三个问题域形成稳定地图，且遗漏了 2026 年直接
   代表音频知识组织与规划检索的工作；
4. “为什么黑盒模型需要引入知识”与“如何评价知识是否被正确、经济地使用”尚未形成完整
   问题链；
5. 三个阶段包含的技术点很多，但尚未清楚说明每个模块究竟回答哪个学术问题，以及一个模块
   失败后对总课题意味着什么。

因此本轮不出具允许开题 notes。只要下面五项 MAJOR 在**报告层面**关闭，无需先证明新颖性、
无需先完成代码或实验、也无需先复现全部基线，即可重新申请正式开题。

## 二、审查方法与边界

本轮保留了三路隔离审查：概念—因果、文献—学界现状、方法—评价与可执行性。三个面板均未
读取历史 review；主审随后重新搜索 2021–2026 的 contextual ASR、audio memory、audio RAG、
agentic correction、long-form audio planning 和 Earnings21/22 等方向，并直读决定性一手来源。

隔离面板的意见只作为“问题发现器”。主审按照当前 Stage-1C 边界重新过滤：

- 关于概念混层、研究问题不唯一和评价链断裂的意见保留；
- 关于学界现状遗漏或表述不准确的意见保留；
- 关于新颖性被占据、必须证明超越最近邻、必须立即复现强基线的意见不作为开题裁决；
- 精确 SESOI、power、后端保真、数据 hash 和实现协议属于后续 Stage-2A 预注册或工程义务，
  不是本次开题报告的必要完成项。

本轮未运行模型、数据、指标或原型，不授予 Stage-2A 权限。本件是 AI 生成的学术评议，不冒充
自然人博导签字，最终学术与执行裁量归 owner。

## 三、建议首先冻结的总研究问题

### 3.1 当前报告真正想研究的对象

现稿标题是“语音任务中的知识系统”，正文又同时讨论：实体发音、外部事实检索、长音频库、
多面索引、门控 agent、知识准入、contextual bandit 和能力上界。它们之间有关联，但“知识
系统”仍过宽，容易把数据结构、检索方法、推理控制和语音纠错全部装进同一个概念。

建议把研究对象明确为：

> **冻结黑盒 speech/omni 模型外围的推理时知识控制系统。** 它不修改核心模型参数，而是在
> 语音观测不确定、任务知识可能不完整且预算有限的条件下，负责把外部材料组织成可寻址知识，
> 决定何时向模型供给哪些知识，并控制候选证据如何进入答案。

这里“黑盒”描述接口约束，“冻结”描述参数约束，“知识系统”描述外置控制面。三者不能互相
代替：黑盒并不等于模型缺知识，冻结也不等于不能有外部控制器，重听音频也不等于获得了外部
知识。

### 3.2 建议的一句话总问题

> **在核心 speech/omni 模型冻结且内部状态不可依赖的条件下，如何围绕语音任务构造可组织、
> 可选择供给、可审慎使用的外部知识控制系统，并分别评价知识引入的必要性、有效性、合理性、
> 可靠性与效率？**

这个问题足够支撑博士课题，也能自然容纳三个研究阶段。双源动作选择、发音库、面联邦和 TFRL
都是候选技术路径，不应反过来取代总研究问题。

### 3.3 五个递进子问题

建议全文统一使用以下 RQ 层级：

- **RQ0：知识必要性与边界。** 哪些错误来自声学观测不足，哪些来自模型参数知识不足，哪些
  可以通过外部 task-time 知识纠正？什么时候不应引入知识？
- **RQ1：知识组织形式（ORG）。** 什么是知识单元、key、value、schema、索引、版本和出处？
  文本、音频、说话人、事件和时间信息应如何组织，才能被后续供给机制稳定寻址？
- **RQ2：知识供给形式（SUPPLY）。** 面对当前样本，何时查、查什么源、如何构造 query、取多少、
  何时停止？声学不确定性如何影响外部知识供给决策？
- **RQ3：知识使用形式（USE）。** 候选证据如何被核验、准入、融合、冲突消解、引用或拒绝，
  才不会把正确答案改错或被错误知识牵引？
- **RQ4：系统控制与评价。** 如何在冻结核心模型的前提下优化上述策略，并评价整体收益、归因、
  可靠性和资源效率？

这一层级比“阶段一/二/三分别做若干模块”更适合开题，因为它先给出科学问题，再允许技术方案
在后续研究中更换。

## 四、三个知识形式应如何贯穿全篇

### 4.1 唯一定义

| 形式 | 回答的问题 | 输入→输出 | 典型变量 | 不能混入的内容 |
|---|---|---|---|---|
| **ORG：知识组织** | 已有材料被表示成什么可寻址对象？ | 原始材料→知识单元与索引 | 切片、粒度、key/value、schema、索引、版本、provenance、物化 | 何时查询、是否相信 |
| **SUPPLY：知识供给** | 当前样本应取得哪些候选知识？ | 状态+预算→候选证据集 | 触发、query、source、top-k、深度、停止、缓存 | 证据如何影响答案 |
| **USE：知识使用** | 候选知识应怎样影响推理结果？ | 假设+候选证据→准入证据/答案/拒答 | admit/reject、融合、冲突、引用、abstain | 索引如何构造、是否再次查询 |

另设两个不属于“知识三形式”的横切面：

- **OBSERVATION / PERCEPTION**：重新切片、重新听取、重新解码、生成多假设。它处理的是已有
  音频观测，而不是外部知识。
- **CONTROL / OPT**：使用规则、配置搜索、bandit 或其他策略，在 OBS、SUPPLY 和 USE 动作之间
  做选择。它是控制方式，不是第四种知识形式。

### 4.2 当前报告的主要混层点

- §6.3 把 `ADMIT/REJECT` 放入“查询族”；它们属于 USE，不属于 SUPPLY。
- `RE_RESOLVE/RE_SLICE` 属于观测重处理，不应称作知识查询或第二类知识。
- §3.4 档 B 优化运行期 action/query，属于 CONTROL/SUPPLY，不是知识组织本身。
- `SRC-sel` 是供给源选择，却同时绑定 K5 组织判据。
- 发音库同时封装 acoustic key、候选检索、世界知识 rescore 和感知触发；作为系统组件可以，
  但不能用一个消融同时证明 ORG、SUPPLY、USE 三个问题都被回答。
- O-config 在 Spoken QA 载体上的组织结论，没有自然进入 Earnings21 主系统的解释链。

### 4.3 报告中应新增的唯一映射表

每个承重模块都应按以下格式登记：

`模块 → 对应 RQ → 所属形式 → 输入/输出 → 改变的唯一变量 → 评价指标 → 失败后的学术解释`。

建议至少形成下面的模块地图：

| 系统模块 | 对应问题 | 角色 |
|---|---|---|
| 音频假设/重解析模块 | RQ0/RQ2 的感知侧输入 | OBS，不属于知识三形式 |
| 实体发音库与多面知识库 | RQ1 | ORG |
| source/query/action router | RQ2 | SUPPLY + CONTROL |
| evidence verifier/admission/fusion | RQ3 | USE |
| 配置搜索或策略优化器 | RQ4 | OPT，横切层 |
| trace、归因与成本账本 | RQ4 | EVALUATION |

系统级联合实验可以同时运行全部模块，但只能回答“整体系统是否有效”；各 RQ 的学术结论必须
来自对应模块的独立对照。这一点在开题报告中讲清即可，不要求当前就完成实验。

## 五、学术界研究现状应改成“问题地图”

当前提案已经收集了大量论文，也能给出不少定量读数；问题在于论文仍主要按阶段、领域和单件
前后排列，读者难以看出学界围绕 ORG、SUPPLY、USE 分别发展到哪里。建议改为下列五条研究线。

### 5.1 contextual ASR：知识主要作为识别偏置被供给

ConEC、Contextual Earnings-22、FineCoS、CB-Whisper 和 multi-pronunciation biasing 说明，学界
已经长期研究实体清单、真实会议材料、上下文短语选择、声学检测和发音变体如何改善 rare/entity
recognition。该线的典型特点是：知识多为词表或短语先验，供给位置靠近 ASR decoder，评价以
WER/B-WER/entity recall 为主。

R2 在现状章节需要讲清：这是**知识供给到识别器**的成熟路线；它对知识 provenance、跨源
组织、证据准入和下游答案合理性的讨论通常较弱。这里是问题维度差异，不是新颖性判断。

### 5.2 speech/acoustic memory：知识可以带有发音或音频 key

Pundak 的 audio exemplars、Mittal 等人的 speech-enriched memory，以及 TTS multi-pronunciation
工作表明，实体知识并不只能以文本字符串组织；音频 exemplar、合成发音、内部声学状态和 trie
都可以成为知识地址。

因此，提案的“实体发音库”应被表述为这条既有路线在冻结黑盒 omni 接口条件下的一种研究
实例。开题阶段要说明它解决 RQ1 的什么问题、受什么接口限制，而不是讨论是否首创。

### 5.3 ASR correction 与 agentic revision：重点逐渐转向知识如何使用

DANCER、G-SPIN、RECOVER、Interactive ASR 和 AgenticASR 代表另一条路线：先得到识别结果或
多假设，再使用实体描述、语境、LLM 约束、工具调用或迭代修订纠正结果。它们把问题从“偏置
解码”推进到“如何利用候选知识和历史输出进行裁决”。

R2 应在这一线中说明 USE 层的研究问题：候选证据怎样准入，如何防止自由生成、错误替换和
correct→wrong，如何区分固定串行纠错与按样本控制。

### 5.4 audio retrieval 与 long-form audio planning：音频知识已有结构化组织与规划检索

WavRAG、ATIR、MARS、PlanRAG-Audio 和 GRGA 表明，学界已经开始研究：

- 原生音频/文本混合检索；
- speaker、emotion、event、time 等多模态信息；
- acoustic/text historical context selection；
- 结构化音频/文本数据库；
- 多维图、模态与时间片规划、迭代检索和反思。

这意味着现稿 §3.3“图/层次索引、多面 key、多粒度在语音域全部缺席”已不准确，必须修正。
但它们不是开题否决证据；相反，它们让 RQ1/RQ2 的学界现状更完整，也为 R2 提供可比较的组织
和供给范式。

### 5.5 speech/omni 模型内部知识与模态差距：解释为什么不能把文本能力直接等同于语音能力

关于 speech LLM factual recall 和 modality reasoning gap 的 2026 年工作说明，同一模型的文本
与语音输入可能呈现不同的知识读取和推理行为。这类研究支持“需要区分参数知识、语音感知和
外部证据”的问题意识，但不能单独证明外部知识必然有用。

### 5.6 现状综述应得出的结论

学术界已经分别研究了：

- 知识如何作为 contextual bias 进入识别；
- 发音和音频信息如何成为 memory/key；
- 外部描述和 LLM 如何纠正识别结果；
- 音频/文本知识如何结构化、检索和规划；
- 迭代 agent 如何选择工具、修订输出。

因此 R2 的学术问题不应写成“语音领域尚无知识系统”，而应写成：

> 现有研究分别优化了组织、供给或使用的某些环节，但在冻结黑盒 omni 接口条件下，如何把
> 三者作为可区分、可归因、可审计的推理时控制问题统一研究，仍缺少清晰的问题框架和评价
> 协议。R2 将围绕这三个形式提出分阶段研究问题，而不是预设某个具体模块必然新颖。

这是一条合格的“研究现状→研究问题”逻辑。它不声称首创，也不需要在当前阶段证明最近邻没有
覆盖精确交集。

## 六、为什么引入知识：需要建立完整的问题链

### 6.1 黑盒不是引知理由

模型是黑盒，只意味着不能依赖内部 logits、hidden states 或重新训练；它不说明模型缺知识。
引入外部知识的合理理由应来自任务信息结构：

- **动态性**：事实会在模型训练后变化；
- **私域性**：会议材料、联系人、企业术语等不在公共训练语料；
- **情境性**：同一声音候选在不同公司、说话人或事件中对应不同实体；
- **可审计性**：答案需要来源、时间和版本；
- **参数知识不可稳定读取**：语音模态可能无法可靠激活文本侧已有知识。

另一方面，纯声学不清楚、切片不当或口音失配首先需要的是重听/重解析，不一定需要外部知识。
这正是 RQ0 和 RQ2 应研究的边界。

### 6.2 建议的五段评价链

1. **Need / 必要性**：没有外部知识时是否存在可恢复 headroom？真证据是否优于无证据？
2. **Access / 供给有效性**：需要的证据是否被正确检回、在正确时机供给？
3. **Use / 使用合理性**：同一候选集下，系统是否接纳真证据、拒绝交换/过期/冲突证据？
4. **Outcome / 任务有效性**：最终任务指标是否改善，是否产生 correct→wrong 或其他副作用？
5. **Cost / 效率**：取得同等质量需要多少检索、调用、音频重处理、延迟和货币成本？

这五段可以自然对应现稿的 oracle、ORG/SUPPLY/USE 消融、合理性诊断和成本向量。开题报告应
先讲清评价对象与因果关系；具体 SESOI、置信区间、power 和成本阈值可在 Stage-2A 预注册。

### 6.3 有效性、合理性与效率不能互相替代

- **有效性**回答“结果是否更好”；
- **合理性**回答“结果为什么变好、证据是否被正确使用”；
- **可靠性**回答“效果是否稳定、是否在某些群体或条件下反转”；
- **效率**回答“同等效果是否值得这些额外资源”。

一个系统提高实体准确率但恶化非实体内容，可能局部有效而整体不合理；一个系统准确率最高但
需要无条件搜索和多次重听，可能能力有效而效率很差。开题报告不必预先给出全部数字阈值，但
必须明确四类结论分别由哪些指标支持，不能用一个总分替代。

## 七、五项 MAJOR 及报告层关闭标准

### MAJOR-1：总问题、子问题和主张层级不唯一

当前“能力上界”“实体发音库”“组织优化”“双源动作选择”和“门控使用”都像主问题。读者
无法判断博士课题究竟要解释什么，哪些只是实现路径。

**关闭标准：**采用 §3 的一句话总问题和 RQ0–RQ4；每个技术模块明确标为某个 RQ 的候选方案；
能力上界降为待验证系统假设，不再统领全部章节。

### MAJOR-2：ORG/SUPPLY/USE 没有贯穿模块、动作和实验

概念词典已经接近合格，但实际动作集和判据再次混层，使正负结果都无法对应具体学术问题。

**关闭标准：**采用 §4 唯一词典；将 OBS 和 CONTROL 独立出去；新增全篇唯一模块映射表；
跨层系统臂只负责整体读数，不负责单层归因。

### MAJOR-3：学界现状不是稳定的问题地图，部分现状判断已经不准确

现稿有充足文献，却没有让读者快速看出 contextual ASR、speech memory、correction、audio RAG、
planning 分别研究了哪个层。PlanRAG-Audio 和 GRGA 等遗漏使 §3.3 的“全部缺席”表述失真。

**关闭标准：**按 §5 五条研究线重写现状；把代表工作放入 ORG/SUPPLY/USE/CONTROL 矩阵；每条
研究线只回答“已研究什么、常用技术和载体是什么、评价关注什么、与 R2 哪个 RQ 相连”。删除
“无人做”“全部缺席”“唯一空位”等当前阶段无必要且高风险的排他性措辞。

### MAJOR-4：为什么引知和如何评价引知尚未形成闭环

现稿已经有许多指标，但“黑盒→为何需要外部知识→知识是否检到→是否正确使用→是否值得成本”
的逻辑没有成为全文主轴。ConEC 主载体本身也只能直接支持 contextual ASR，不应被用来代表
所有知识必要性。

**关闭标准：**增加 §6 的五段评价链；明确参数知识、外部知识和音频观测三者边界；说明主载体
支持什么结论、第二类载体为何需要；为有效性、合理性、可靠性、效率分别指定指标族和解释，
具体数值留到执行前预注册。

### MAJOR-5：阶段、模块和预期学术产出没有一一对应

三个阶段包含的技术点过多，但报告没有清楚说明每一阶段结束时要回答哪个 RQ、形成什么知识、
失败时如何调整后续阶段。这样容易变成系统堆叠，而不是递进的博士研究。

**关闭标准：**把研究计划改为三个可独立成章的工作包：

| 工作包 | 主问题 | 主要对象 | 最低学术产出 | 失败后出口 |
|---|---|---|---|---|
| WP1：语音知识表示与组织 | RQ0/RQ1 | 发音/实体 key、知识单元、schema、provenance | 说明什么组织形式在何种语音错误上可寻址 | 声学 key 无价值则退回文本/G2P 组织，不影响 WP2/3 |
| WP2：不确定性条件下的知识供给 | RQ2 | query、source、重解析与搜索的控制 | 说明何时应供给何种信息及其边界 | 自适应控制无价值则保留强固定策略，记录适用边界 |
| WP3：证据准入、融合与系统评价 | RQ3/RQ4 | admit/reject、冲突、引用、成本 | 说明如何降低知识副作用并建立评价协议 | 准入无增益则缩小到可判定任务/载体 |

TFRL、bandit 或配置搜索作为 WP2/WP3 的方法候选，不应在开题阶段成为必须证明的身份主张。

## 八、MINOR

1. “ASR-free”应改成“无独立专用 ASR 前端”或其他准确接口描述；omni 核仍在执行语音识别。
2. “能力上界”建议改成“预注册配置族内的最佳已测系统效果”。
3. “双源知识动作”应改成“双源信息获取/控制动作”；重听不产生外部知识。
4. `V̂` 在得到校准证据前宜称 heuristic score 或 action score，而不是已知 value estimator。
5. 版本元数据和签字表应在重投时同步到当前 v17.1/round-19 状态，但这只是文档治理问题。

## 九、建议的开题报告新目录

1. **研究背景与核心矛盾**：冻结黑盒语音模型、语音不确定性、task-time 知识需求。
2. **研究对象与概念框架**：参数知识/外部知识/观测；ORG/SUPPLY/USE；OBS/CONTROL 横切面。
3. **学术界研究现状**：contextual ASR、speech memory、correction、audio RAG/planning、模态知识。
4. **总研究问题与 RQ0–RQ4**：每个问题的输入、输出、可观察现象和适用边界。
5. **总体技术路线**：系统模块图及模块—RQ—形式映射。
6. **WP1：知识组织**：候选方案、载体、评价思路和失败出口。
7. **WP2：知识供给与控制**：候选方案、载体、评价思路和失败出口。
8. **WP3：知识使用与评价**：准入、融合、可靠性、效率和失败出口。
9. **数据与载体**：每个载体能支持什么结论，不能支持什么结论。
10. **预期研究产出、计划与风险**：按 RQ/WP 表述，不按组件数量表述。

## 十、重新申请正式开题的最低条件

- [ ] 一句话总问题和 RQ0–RQ4 固定；
- [ ] 参数知识、外部知识、音频观测和重解析动作的边界清楚；
- [ ] ORG/SUPPLY/USE 的唯一词典贯穿动作、模块、假设和评价；
- [ ] 学界现状按五条研究线重写，并纳入 PlanRAG-Audio、GRGA、ATIR、MARS 等代表工作；
- [ ] 删除当前阶段不需要的排他性新颖性措辞；
- [ ] 每个模块只对应一个主 RQ，并有独立评价和失败解释；
- [ ] Need→Access→Use→Outcome→Cost 五段评价链完整；
- [ ] 三个工作包、载体适用边界、预期学术产出和失败出口明确；
- [ ] 签字表与正文能在一页内准确复述上述结构。

这些条件全部是报告逻辑条件，不要求在正式开题前完成技术验证。精确基线实现、统计 power、
数据 hash、运行后端和数值阈值可以进入 Stage-2A 前的可执行合同。

## 十一、最终意见

**方向合理，课题规模足够，参考文献数量已经充足；当前不足是“问题结构”和“现状结构”，而
不是尚未证明新颖性。**

最值得保留的不是某个单独模块，而是如下研究框架：面对冻结黑盒语音/omni 模型，把知识问题
拆成组织、供给和使用三个可区分形式；先判断是否真的需要外部知识，再研究知识如何被取得、
如何被安全利用，最后分别评价效果、归因、可靠性和效率。

PlanRAG-Audio、GRGA、RECOVER、ConEC 等不是对 R2 的否决，而是必须正确放入学术史地图的
坐标。报告应借它们说明学界已经把哪些子问题推进到了什么程度，然后自然引出 R2 要系统研究
的 RQ0–RQ4。只要完成这种重构，即使尚未做新颖性判决、尚未跑实验，也可以达到正式开题所需
的逻辑成熟度。

当前 `formal_opening_authorized: false`，本轮不出具允许开题 notes；完成上述报告级大修后，
建议进行一次只审“研究问题—现状—方法—评价”一致性的窄面复审。

## 十二、学界现状建议引用的一手文献

### contextual ASR 与语境供给

1. Huang et al. (2024), [ConEC: Earnings Call Dataset with Real-world Contexts for Benchmarking Contextual Speech Recognition](https://aclanthology.org/2024.lrec-main.328/).
2. Durmus et al. (2026), [Contextual Earnings-22: A Speech Recognition Benchmark with Custom Vocabulary in the Wild](https://arxiv.org/abs/2604.07354).
3. Han et al. (2022), [Improving End-to-End Contextual Speech Recognition with Fine-Grained Contextual Knowledge Selection](https://arxiv.org/abs/2201.12806).
4. Li et al. (2024), [CB-Whisper: Contextual Biasing Whisper Using Open-Vocabulary Keyword-Spotting](https://aclanthology.org/2024.lrec-main.262/).
5. Liu et al. (2025), [Zero-shot Context Biasing with Trie-based Decoding using Synthetic Multi-Pronunciation](https://arxiv.org/abs/2508.17796).

### speech/acoustic memory 与实体知识组织

6. Pundak et al. (2022), [On-the-fly ASR Corrections with Audio Exemplars](https://www.isca-archive.org/interspeech_2022/pundak22_interspeech.html).
7. Mittal et al. (2023), [Speech-enriched Memory for Inference-time Adaptation of ASR Models to Word Dictionaries](https://aclanthology.org/2023.emnlp-main.916/).
8. Chan et al. (2023), [Using External Off-Policy Speech-To-Text Mappings in Contextual End-To-End Automated Speech Recognition](https://arxiv.org/abs/2301.02736).

### correction、知识裁决与 agentic revision

9. Wang et al. (2024), [DANCER: Entity Description Augmented Named Entity Corrector for Automatic Speech Recognition](https://aclanthology.org/2024.lrec-main.387/).
10. Singh et al. (2026), [Graph-Based Phonetic Error Correction of Noisy ASR](https://aclanthology.org/2026.acl-industry.151/).
11. Kumar and Sachdeva (2026), [RECOVER: Robust Entity Correction via agentic Orchestration of hypothesis Variants for Evidence-based Recovery](https://arxiv.org/abs/2603.16411).
12. Jiang et al. (2026), [Towards Human-Like Interactive Speech Recognition With Agentic Correction and Semantic Evaluation](https://arxiv.org/abs/2605.29430).
13. Jiang et al. (2026), [AgenticASR: Refining Speech Recognition in Real-World Scenarios via an Agentic Approach](https://arxiv.org/abs/2607.28175).

### audio retrieval、组织与规划

14. Chen et al. (2025), [WavRAG: Audio-Integrated Retrieval Augmented Generation for Spoken Dialogue Models](https://aclanthology.org/2025.acl-long.613/).
15. Zhao et al. (2026), [ATIR: Towards Audio-Text Interleaved Contextual Retrieval](https://aclanthology.org/2026.acl-long.1006/).
16. Mu et al. (2026), [Hearing More with Less: Multi-Modal Retrieval-and-Selection Augmented Conversational LLM-Based ASR](https://ojs.aaai.org/index.php/AAAI/article/view/40528).
17. Someki et al. (2026), [PlanRAG-Audio: Planning and Retrieval Augmented Generation for Long-form Audio Understanding](https://aclanthology.org/2026.findings-acl.1304/).
18. Tang et al. (2026), [Don't Just Listen, Try Planning: Graph-based Retrieval-Generation Agent for Long-form Audio Meeting Understanding](https://aclanthology.org/2026.findings-acl.1038/).

### speech/omni 知识与模态差距

19. Modica et al. (2026), [Do Factual Recall Mechanisms Carry over from Text to Speech in Multimodal Language Models?](https://aclanthology.org/2026.starsem-conference.28/).
20. Wang et al. (2026), [Closing the Modality Reasoning Gap for Speech Large Language Models](https://aclanthology.org/2026.acl-long.857/).
