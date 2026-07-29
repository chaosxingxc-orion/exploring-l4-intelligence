---
title: "R2 音频驱动外部知识获取开题报告：博导视角协同评审"
date: "2026-07-29"
artifact_type: "DOCTORAL_SUPERVISOR_COREVIEW"
campaign: "system-first-stage1c-v2"
round: "round-03"
review_target: "wiki/survey/workbench/stage1c-portfolio/proposals/2026-07-29-r2-coreview-draft.md"
review_target_commit: "300a6181d52b318d27436b5e048fd853554e64e4"
review_target_git_blob: "062c253db3a60df16bea7fcf00cf88cbb2292c54"
review_target_worktree_sha256: "2c298e5c2b745c256240d592c16093400815b441b6eed618233b0c08808d155e"
verdict: "MAJOR_REVISION_REQUIRED_BEFORE_OWNER_DIRECTION_DECISION"
authority_effect: "WITHHOLD_ONLY_NO_OWNER_DECISION_NO_EXECUTION_GRANT"
human_signature_claimed: false
model_or_metric_execution_authorized: false
stage2a_authorized: false
novelty_verdict: "NOT_ISSUED"
---

# R2 开题报告博导视角评审：先重构知识问题，再决定是否独立立项

## 一、评审结论

**裁决：`MAJOR_REVISION_REQUIRED_BEFORE_OWNER_DIRECTION_DECISION`。**

当前稿件是一份有价值的文献调研与候选机制备忘录，但还不是一份可以签署
`GO_STANDALONE_AS_RETRIEVAL_SCHEDULING` 的博士开题报告。其最强部分是对 AudioRAG、
Omni-DeepSearch 和 VoiceAgentRAG 的数据、基线与失效面的批判性分析；其主要缺陷不是材料不足，
而是研究对象尚未稳定：知识组织、知识供给、知识使用、外部记忆、证据状态、实例内控制与可靠性门禁
被写成了一条连续的“RAG 代际跃迁”，没有落实到互斥的系统模块、独立变量和可归因实验。

本评审不否定 R2 的研究潜力，也不恢复旧版 `NO_GO/MERGE` 建议。R2 是否能够独立，取决于整改后能否
证明它拥有一个**音频特有、外部知识特有、可由独立实验识别的研究问题**。在此之前，owner 不应在
选项 A（独立）与选项 B（合并）之间落笔。

本文是 AI 生成的博导视角协同评审，不冒充自然人签字，不授予模型/API 调用、数据获取、指标运行、
原型、Stage-2A、创新性结论、push 或 wiki 发布权限。

## 二、审查对象与范围

审查对象为：

- `wiki/survey/workbench/stage1c-portfolio/proposals/2026-07-29-r2-coreview-draft.md`；
- Git commit：`300a6181d52b318d27436b5e048fd853554e64e4`；
- Git blob：`062c253db3a60df16bea7fcf00cf88cbb2292c54`；
- 工作树 SHA-256：`2c298e5c2b745c256240d592c16093400815b441b6eed618233b0c08808d155e`。

本轮审查重点是问题定义、概念结构、方法—模块映射、实验可归因性和评价闭环。它不重新执行 31 篇
全文抓取，不重新裁定论文数字，也不把跨域 donor 的效果外推到 speech/omni 域。

## 三、应当保留的内容

以下内容已经构成下一版的可靠骨架，不应推倒重写：

1. **数据集批判是当前最成熟部分。** 对 AudioRAG-500 的 metadata 构造与检索污染风险、
   Omni-DeepSearch-640 的单 split、live-web 漂移、无 no-tool 行和小样本分桶、VoiceAgentRAG-200
   缺少答案质量轴的判断，均直接影响载体资格。
2. **over-search 是真实、可检验的失效面。** 固定预算继续增加后总体饱和、局部类别下降以及已获得
   正确证据后继续搜索而答错，足以支持“固定统一预算不总是合理”的问题动机。
3. **incumbent 和 strongest fixed baseline 必须保留。** no-tool direct、固定预算三档、原论文 wrapper、
   random matched-cost 和 oracle/headroom 的基线意识是正确的。
4. **信息边界纪律正确。** API-only、test gold 不进 controller、跨域只借机制形状、他核数字只引用不
   冒充本项目结果，均应保留。
5. **处置仍应保持可逆。** 当前把 A/B 两种 portfolio 归属同时保留，比先验决定 R2 必须独立或必须
   合并更符合 Stage-1C 的权限边界。

## 四、P0-1：三种“知识形式”没有形成互斥概念

### 失败合同

`conceptual separability / system-object identity`。

当前稿件虽然显式使用“组织—供给—使用”三轴，但三轴实际仍按论文叙事分段，没有按系统中被改变的
对象定义。下一版必须使用以下最小词典，并在全文保持一致：

| 概念 | 必答问题 | 所属模块 | 不应混入 |
|---|---|---|---|
| 知识组织形式 | 知识以什么单元、schema、关系、索引、版本和 provenance 存在 | source registry、corpus、chunk/schema、index、graph、snapshot | 跨实例经验效用、检索触发、答案仲裁 |
| 知识供给形式 | 何时取、从哪里取、以什么 query 取、取多少、何时停止、如何压缩排序后送入上下文 | query builder、retriever、search planner、budget/stop policy、context composer | 证据已经进入后的融合、最终答案选择 |
| 知识使用形式 | 已获得证据如何被接纳、融合、冲突处理、归因、引用、修订或拒用 | result admission、grounding/fusion、answerer、arbiter、abstention | 索引结构、搜索预算、跨实例写入 |

必须同时拆开两个现在被称为同一机制的门：

- **pre-call acquisition gate**：尚未看到工具输出，决定是否购买一次调用；
- **post-retrieval/pre-context admission gate**：外部控制器已经看到结果，但结果尚未进入 frozen core
  的上下文，决定接纳、拒绝、压缩或标记冲突。

两者所需信号、成本和可识别实验不同，不得再用 `pre-call admission gate` 合并命名。

### 当前混淆造成的实质后果

1. A-MEM、MemRL、experience utility 的演化属于 D2 外部记忆生命周期，不能用来证明 R2 外部任务知识
   的组织创新空位。
2. “stop / admission / 预算是使用形式的收敛点”不成立：search stop 和 budget 属供给；admission 是
   供给—使用边界；grounding、conflict、citation、answer revision 才是使用。
3. “向量库/无组织”是自相矛盾表述。向量库是组织形式；真正缺少的可能是多粒度单元、音频锚点、
   跨模态关系、时间版本或 provenance，必须逐项陈述。
4. SpeechDPR、SpeechRAG、WavRAG 是组织/检索表征轴的核心本域证据，但当前只到登记未深读层；在其
   深读完成前，不足以发布“语音域整体仍处于文本 2020–2022 段位”的领域级判断。

### 最小修复

为 §2–§4 中每篇承重论文增加同一张方法卡，字段固定为：

```text
knowledge source/unit/schema/index/version/provenance
acquisition trigger/query representation/search plan/hop/stop
result admission/context placement/fusion/conflict/citation/abstain
changed module / held-constant modules
runtime-visible signals / gold-only signals
dataset / incumbent / strongest fixed baseline / primary metric / cost surface
```

演进综述只能在这些字段上比较，不得再以“论文出现时间较晚”替代机制级演进判断。

## 五、P0-2：黑盒合同被误写成了知识必要性的因果理由

### 失败合同

`problem necessity / information-source identity`。

黑盒只约束**不能如何修改模型**，不自动推出**为什么必须给模型外部知识**。参数知识难更新也只能说明
外部知识的一种可能价值，不能证明具体实例需要检索。下一版必须区分四类不同信息作用：

1. **external new information**：web/corpus 提供 waveform 和当前模型可见上下文中不存在的事实；
2. **observation re-representation**：ASR、重听、分段、不同音频 query 只是重表达已有信号，不是新增知识；
3. **latent-knowledge elicitation**：prompt、分解或采样让冻结模型表述其参数内已有知识；
4. **verification/provenance information**：外部证据主要用于确认、反驳或给出可审计来源。

R2若以 external knowledge 为研究对象，其问题必要性应来自以下任务结构：音频先确定实体、事件或属性，
答案还依赖时效、长尾、私域或需引用的外部事实。应明确写出：

```text
audio observation -> entity/event hypothesis -> external fact -> grounded answer
```

当前稿件没有说明失败究竟发生在“听错实体”“query 错”“未检到事实”“检到错误证据”“证据污染回答”
还是“模型不会利用正确证据”。这些不是一个问题，也不能由一个总 accuracy 解释。

### 与项目北极星的关系必须重写

AudioRAG 同时加入额外 text controller、问题分解、web retrieval 和新的最终推理权。其 wrapper 增益不能
直接表述为 frozen omni 的“潜在知识激活”。下一版必须选择并声明主张对象：

- 若主张 **system-level task capability**，允许外部 controller 承担推理，但不得把收益归因给 core；
- 若主张 **frozen core capability activation**，最终证据使用和作答权必须回到同一 frozen core，或通过
  controller/search/audio-tool/answerer 正交消融完成归因。

## 六、P0-3：当前只有动作菜单，没有可审查的方法合同

### 失败合同

`method identifiability / training-free-RL identity`。

“逐实例继续搜、换 query、停止”和“admission”只是动作集合，不足以构成 reward-guided 方法。下一版必须
实例化以下五项：

```text
state: controller 在第 t 步实际看见什么
action: SEARCH / REQUERY_AUDIO / ADMIT / REJECT / ANSWER / ABSTAIN / STOP 的精确定义
runtime reward or value estimate: 由哪些 deployment-visible 信号构成
transition: 哪个输出进入 evidence state，哪个输出进入 core context
policy/update: reward/advantage 如何改变下一动作，而不是只在终局 rerank
```

“答案一致性、检索—音频实体 corroboration、预算消耗”目前只是候选特征。必须说明它们如何组合成
决策量、如何在不使用 test gold 的条件下校准、阈值由谁拥有、估计器错误如何进入可靠性声明。若最终
方法只是 prompt 让 LLM 自行决定 stop，它与被批评的自由生成 controller 没有可识别差异。

### 模块级改进要求

下一版不要求同时创新所有模块，但必须对每个模块声明 `FIXED / BASELINE VARIABLE / PROPOSED
INNOVATION / OFFLINE EVALUATOR`：

| 模块 | 可研究问题 | 最低对照 |
|---|---|---|
| 知识源与索引 | corpus/snapshot、单元粒度、audio anchor、provenance | 同一证据库下 lexical/dense/hybrid 或明确固定一种，不静默变化 |
| audio→query | 单一转写实体还是多个竞争假设 | gold-entity ceiling、single-hypothesis、multi-hypothesis |
| retrieval planner | query、hop、budget、stop | best fixed budget、random matched-cost、always/never corners |
| evidence processor | 去重、冲突、来源质量、压缩 | raw top-k、relevance-only、result admission |
| context/use | 拼接、结构化 grounding、raw-audio re-anchor、citation | 同一 evidence set 下 unconditional 与 structured use |
| controller/evaluator | reward、VoI、阈值、incumbent fallback | hand-authored rule、terminal-only、offline oracle |

若下一版只把检索 planner 设为变量，其余模块必须冻结；若同时改变 planner 与 admission，必须做析因实验，
不能只比较整条新 wrapper 与整条旧 wrapper。

## 七、P0-4：数据载体无法回答当前宣称的“为什么/何时引入知识”

### 失败合同

`benchmark-question alignment / causal attribution`。

AudioRAG 与 Omni-DeepSearch 在构造阶段尽量过滤掉“不需要外部检索”的题。它们适合研究：

> 在 external-required 条件已成立时，如何构造 query、检索、停止和使用证据？

但不适合单独研究：

> 当前实例究竟应不应该引入外部知识？

因此必须二选一：

1. **收窄主张**：只研究 external-required 分布内的 search depth、stop 与 admission，不再声称解决通用
   knowledge-need detection；或
2. **补独立负控制分布**：使用已有正式 audio-sufficient benchmark/任务作为不检索控制，不自行造标签，
   但在同一 frozen core 上测量错误检索和无条件检索的伤害。

`no-tool direct` 是必要基线，不是博士研究贡献本身；“补一条论文缺失的协议行”只能算实验卫生或 benchmark
完善，不能单独支撑 R2 独立立项。

### 最低因果实验阶梯

下一版至少给出以下实验臂及每一臂回答的问题：

| 实验臂 | 识别对象 |
|---|---|
| A0：audio-only direct | incumbent；无外部证据时模型表现 |
| A1：gold evidence + fixed use | 外部知识对该 frozen core 的可恢复上界 |
| A2：retrieved evidence + unconditional concat | 检索管线总体收益与 evidence-induced harm |
| A3：与 A2 相同 evidence set + admission/fusion | 知识使用机制的独立贡献 |
| A4：同 store、同 answerer、等成本 adaptive query/hop/stop | 知识供给策略的独立贡献 |
| A5：shuffled/irrelevant/conflicting evidence | 盲从、污染、拒绝与 correct→wrong 风险 |
| A6：offline oracle over actually executed pool | 已执行 action menu 的 recoverable headroom |

`gold-entity` 只隔离音频实体识别，不能替代 `gold-evidence`；上下文中出现证据也不等于模型使用了证据。
后者必须通过 evidence removal/swap/conflict、引用归因或答案翻转等反事实检查识别。

## 八、P0-5：有效性、合理性、可靠性和效率没有形成四层评价

### 失败合同

`measurement validity / resource-normalized comparison`。

下一版必须分开报告四类问题，禁止合成一个新总分：

### 8.1 有效性：知识是否带来任务增益

定义外部证据的反事实边际效用：

```text
delta_E = U(M(x, q, E), y) - U(M(x, q), y)
```

至少报告 official task accuracy/utility、paired delta、bootstrap 95% CI、McNemar、SESOI、
wrong→correct、correct→wrong，以及按任务类别、音频类别和 hop depth 的分桶结果。

### 8.2 合理性：系统是否在正确的时机取了并使用了正确证据

至少离线评估：

- retrieve/skip、continue/stop、admit/reject 的混淆矩阵；
- reward/value estimator 对真实离线 `delta_E` 的 calibration 与 error bound；
- answer-bearing evidence coverage、来源 provenance、冲突与 unsupported claim；
- irrelevant/conflicting evidence 下的拒绝率和答案稳定性；
- evidence removal/swap 后答案是否按预期改变。

这些可以是诊断量，不需要改写成新的主 leaderboard metric；但若完全禁止这些诊断，R2 就无法回答知识引入
是否合理，只能报告 wrapper accuracy。

### 8.3 可靠性：平均提升是否掩盖伤害

至少报告 seed/run variance、correct→wrong、worst group/lower tail、coverage-quality、跨 audio 类型和
检索模态的符号一致性。abstain 不得通过把 coverage 压到接近零制造表面安全。

### 8.4 效率：知识提升是否值得其资源代价

成本必须保留为向量，不得合成模糊 `cost`：

```text
(retrieval hops, result bytes, frozen-core calls, audio seconds,
 controller tokens, judge calls, wall-clock latency, API currency,
 index-build/storage/amortized snapshot cost)
```

至少报告平均与 P95、超预算失败率、固定成本下的最佳质量、固定质量下的最低成本、accuracy–cost
Pareto frontier，以及每增加一次 hop 的边际任务效用。`等总预算` 必须说明是逐实例 hard cap、平均预算，
还是多维成本中的哪一维相等。

## 九、P0-6：可复现性边界存在内部矛盾

稿件一方面把“无冻结检索快照”列为 Omni-DeepSearch 不能成为标准基线的阻断项，另一方面在边界声明中
规定“不补检索快照”。若检索环境随时间变化，则不同策略看到的不是同一知识环境，paired delta、方法归因
和复放均不成立。

若当前 owner 边界禁止制作新的 benchmark corpus，仍必须至少做到：

- pin 搜索服务、日期、query 和参数；
- 完整落盘每次返回的 URL/document ID/rank/content hash；
- 所有可共享查询在各实验臂间复用同一返回；
- 对 adaptive 独有查询保留完整 trace 与内容 hash；
- 单列 source-page reachability/metadata contamination strata。

如果连上述 evidence logging 都不允许，则不得发布可复现的 controller dominance 主张，载体应降级为
方向性 feasibility evidence。

## 十、P1：领域演进结论和创新台阶表达过强

“文本域问题已收敛”“视觉域四臂协议已成标准”“语音域整个自适应→定价跃迁尚未发生”等表述超过当前
证据强度。现有材料足以说：

> 在本地登记并完成相应深读的 read set、截至 2026-07-29，尚未观察到某机制。

但不足以自动说：

> 整个领域缺席，因此移植该机制就是博士创新。

跨域机制空位只产生 candidate hypothesis。R2 还必须回答“为什么 speech/audio 的问题结构使该机制需要
重新设计”，而不是只证明文本域较早出现。最值得发展的音频特有结构是：

- 外部检索 query 依赖一个可能听错的 entity/event hypothesis；
- 系统必须区分 perceptual uncertainty 与 external-knowledge uncertainty；
- 错误音频实体会产生高度相关但完全错误的外部证据；
- 因此预算可能需要在 `re-resolve audio` 与 `search external facts` 两个不同信息源之间分配。

如果整改后没有形成这类 audio-specific 机制，而只是把通用 VoI/stop controller 迁移到一个音频 benchmark，
则 R2 不足以独立，应作为 R6/R8 的 external-retrieval carrier 和 action-family specialization。

## 十一、P1：数字击杀阈值尚不可执行

当前 K1–K4 可以保留为占位，但授权前必须修复：

1. `+2.0pt` 需要结合实际 test n、baseline rate、discordant-pair 数和 judge noise 做 power analysis；
2. “over-search 型错误”必须给可执行定义，例如“某一步已存在支持正确答案的证据/答案，后续额外检索导致
   最终错误”，并说明由谁、用什么信息离线判定；
3. “等 accuracy”必须有 non-inferiority margin，而不是点估计相等；
4. AudioRAG 上轻微、无统计分辨力的负值不应自动等同“符号翻转击杀”，应预注册 replication criterion；
5. Knowledge-error 和 Type-D 的 judge prompt、重复性、人类一致性或异质 judge 复核必须进入 metric contract；
6. 对多杠杆、多数据集和多分桶比较规定 multiplicity correction。

## 十二、建议替换的主研究问题

建议将当前一句话问题改为：

> 在“音频先确定实体/事件、答案依赖外部事实”的任务上，冻结黑盒 omni 系统能否仅凭部署可见信号，
> 估计一次外部证据动作的边际价值，并在固定知识环境和等资源条件下，相对最优固定检索策略，同时提高
> 任务效用、降低 evidence-induced correct→wrong，并减少无效检索？

该问题允许形成三个有顺序的子问题，但不要求同时把三者都宣称为创新：

1. **Necessity**：该任务/实例的缺口是音频感知、外部知识，还是推理；
2. **Supply**：在固定 store/use 下，audio-conditioned query/hop/stop 是否优于 best fixed；
3. **Use**：在固定 evidence set 下，admission/grounding 是否优于 unconditional concat。

知识组织层可以先作为冻结实验合同；只有在证明现有索引无法承载 audio anchor、provenance 或多假设 query
后，才升级为独立方法变量。这样既把三种形式讲清楚，也避免一次 proposal 同时声称改进所有模块。

## 十三、R2 与 R6/R8 的独立性判据

### 可支持 R2 独立的条件

- 研究对象明确限定为外部知识 action family，而非任意 trajectory；
- 方法利用音频特有的 query/entity uncertainty、audio anchor 或跨模态 provenance；
- 在同一通用 controller 形状下，能够识别外部检索特有的状态、动作、风险与成本；
- 至少一个实验可单独归因给 R2 模块，而不是整条 R5+R6+R8 wrapper；
- 与本域 incumbent 和具体 SOTA baseline 在相同任务/数据上形成闭合比较。

### 应合并到 R6/R8 的条件

- 唯一新内容是通用 `query/hop/stop` reward policy；
- 所有信号、状态和可靠性阈值与其他 action family 完全同形；
- 音频只充当输入载体，不改变方法或失效机制；
- R2 的实验只能通过完整 R5/R6/R8 系统运行，无法形成独立消融与主张。

## 十四、Fable5 逐项回应与复审清单

请下一版 proposal 或 response 按以下顺序逐项回应，避免只补引用或增加篇幅：

- [ ] 给出组织/供给/使用三者的互斥定义，并用统一方法卡重新编码承重论文；
- [ ] 把 external new information、observation re-representation、latent elicitation 和 verification 分开；
- [ ] 明确 R2 的主张对象是 system capability 还是 frozen-core activation；
- [ ] 给出实例化的 state/action/reward/transition/policy，不再只列动作菜单；
- [ ] 对所有模块标注 FIXED/BASELINE/INNOVATION/EVALUATOR；
- [ ] 在“收窄 external-required 主张”与“引入正式 audio-sufficient 负控制”之间作出选择；
- [ ] 给出 A0–A6 最低因果实验阶梯，并区分 gold-entity 与 gold-evidence；
- [ ] 分开定义有效性、合理性、可靠性和效率，不合成新总分；
- [ ] 解决 live retrieval 的复放与污染审计矛盾；
- [ ] 收窄领域级 absence/standard/convergence 量词，补深读组织轴核心本域论文；
- [ ] 完成 K1–K4 的 operational definition、power 和 judge-fidelity 合同；
- [ ] 用明确判据说明 R2 为何独立于 R6/R8，或接受 MERGE 路由。

完成上述项目后，复审只需判断三个问题：研究对象是否唯一、实验是否可归因、audio-specific 增量是否足以
独立。不要求为了形式完整继续无界扩张文献，也不要求在 Stage-1C 执行任何模型、数据或指标实验。

## 十五、目的链、Provenance 与失效条件

**结论：** 当前 R2 需要重大结构性修改，owner 的独立/合并裁定继续 withheld。

**推理摘要：** 现稿已经证明本域存在检索饱和、over-search、证据污染和成本缺失，但尚未区分知识组织、
供给与使用，也没有把 black-box 外部知识必要性、reward-guided 方法和因果评价闭合，因此不能从“存在空位”
推出“当前 L1/L2 构成独立研究方向”。

**目的链：** 为 Stage-2A 选择一个可复现、可证伪、符合 API-only frozen-core 边界且能与 incumbent SOTA
比较的具体问题；所以 Stage-1C 必须先保证研究对象唯一、模块边界清楚、主张可由正交实验识别。

**Provenance：** 本文只审查 front matter 所绑定的 R2 v2 Git blob，并依据当前
`wiki/Research-Objective.md`、`wiki/Project-Thesis.md`、`wiki/survey/current/research-directions.md`、
`wiki/survey/workbench/stage1c-portfolio/proposals/shared-experiment-and-formal-protocol.md` 及 proposal 已登记的
本域/donor dossier 边界作判断。

**失效条件：** 若后续 exact proposal/response 已关闭第十四节全部项目，并由新 review transaction 判断
研究对象、归因和独立性成立，则本 withholding verdict 仅作为历史审计事实保留；不得原位改写本文。
