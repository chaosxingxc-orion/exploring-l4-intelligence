---
proposal_id: "R2"
title: "音频驱动外部知识检索的文献归纳、实验载体与方向处置"
role: "Stage-1C 研究内容分析报告；供 owner 作方向判断"
stage: "STAGE_1C_DIRECTION_CONFIRMATION"
status: "EXECUTOR_DRAFT_UNVERIFIED_BY_OWNER"
recommendation: "WITHDRAWN_TO_DRAFT__PENDING_OWNER_COWORK_UNDER_2026-07-29_CRITERION"
evidence_cut: "2026-07-28"
execution_authority: "WITHHELD"
---

# R2 — 音频驱动外部知识检索的文献归纳、实验载体与方向处置

## 0. 结论先行

> **状态（owner 2026-07-29，Decision-Log 续76）。** 本报告属 R2–R9 未与 owner 协同工作的执行者
> 草稿批次，owner 未校验。下述建议（原文保留）已撤回为草稿意见，不构成裁决。按 07-29 方向成立
> 判据，R2 属 (a) 型——AudioRAG、Omni-DeepSearch、VoiceAgentRAG 为本域已有工作，可作为方法论
> 基线在具体任务上与 SOTA 对比——方向资格待与 owner 协同重审；证据事实独立于处置结论保留。

**执行者原建议（已撤回为草稿意见）：R2 不作为独立研究方向进入 Stage-2；撤销原 Stage-2D，相关
数据、基线和方法按需并入 R5/R6/R8，跨轮缓存证据按需并入 R3/R7 或 R9。**

这个结论不否定外部知识的重要性。与 R1 不同，R2 面向的是 waveform 之外的真实 new information，研究
对象本身有明确价值；问题在于当前 proposal 没有一项由 R2 独占的研究决策权：

- `audio/external two-ledger evidence state` 是 R5 的证据状态与 provenance 合同；
- `whether/query/hop/stop` 是 R6 的实例内 action/trajectory control；
- 检索是否值得、预算是否继续、何时回退 incumbent 是 R8 的条件可靠控制；
- 跨轮 prefetch/cache 是 R3/R7 的外部状态复用或 R9 的交互延迟扩展。

参考论文已经提供 AudioRAG 和 Omni-DeepSearch 两类 audio-driven retrieval benchmark、固定搜索 pipeline、
模型基线和 accuracy 评价，也提供 VoiceAgentRAG 的跨轮预取/缓存系统与 latency/hit-rate 评价。若 R2 只复现
这些内容，它是其他方向使用外部知识 action 时本来就要完成的 baseline；若继续保留 proposal 中的
need detector、reward/VoI query-hop-stop policy、two-ledger attribution 和 pinned-snapshot utility 分解，则是在
Stage-1C 自行设计新方法、数据标签和指标，不符合本阶段“只分析归纳、数据与指标复用参考论文”的边界。

因此，R2 的正确产出是一次方向淘汰与证据重路由，而不是一份 Stage-2D 实验计划。

## 1. 本阶段的三条硬边界

### 1.1 只做研究方向确认

当前等价于开题报告：梳理参考论文已经研究了什么、使用了什么数据、基线和指标，并判断能否形成独立问题。
不为保住方向而发明 reward、VoI、need gate、检索快照、标签体系或新的控制器。

### 1.2 数据只复用参考论文正式发布的资产

- 可以原样复用 AudioRAG、Omni-DeepSearch 和 VoiceAgentRAG 作者正式发布的数据与既有划分。
- 不自行混入 waveform-sufficient 负例，不为 need detection 新标 `required/not-required/ambiguous`。
- 不把实时 web 搜索结果抓取并整理成新的 benchmark corpus，再称为参考论文数据集。
- 论文未发布冻结检索快照时，只能如实保留 live-search 漂移边界，不能自行造 snapshot 填洞。

### 1.3 指标只复用参考论文或官方 benchmark 口径

- AudioRAG 使用 GPT-4o judge 的 accuracy、三次运行平均和 A/B/C/D 错误分类。
- Omni-DeepSearch 使用三位 LLM judge 多数投票的 accuracy，并按 retrieval modality 与 audio content 分组。
- VoiceAgentRAG 使用 cache hit rate、retrieval latency、speedup 和累计节省时间。
- 不新造统一 utility、need-detection score、retrieval admission precision、evidence contribution、LCB 或
  cost-quality 总分来把三篇不可公度的论文强行合并。

## 2. 当前 R2 假设与实验载体不匹配

| 当前假设/设计 | 参考论文能否直接承载 | 审计结论 |
|---|---|---|
| H1：区分 waveform-sufficient 与 external-fact-required | AudioRAG 和 Omni-DeepSearch 的构造目标就是过滤掉不需要检索的题；官方数据没有 waveform-sufficient 对照桶 | **不能。** 必须另混数据或重标标签，违反数据复用边界 |
| H2：reward/VoI-guided query-hop-stop 优于 fixed policy | Omni-DeepSearch 只有固定搜索预算消融；AudioRAG 是自由生成的 Think-Call-Answer；没有发表的 reward/VoI policy | **不能直接复现。** 这会成为 R6 的新控制方法，而非 R2 的参考方法复现 |
| H3：audio/external 双账本减少外部证据覆盖原音 | 三篇论文均没有这个实验臂或官方指标 | **不属于 R2 独立贡献。** 这是 R5 evidence-state invariant |
| H4：把收益分成 grounding/query/retrieval/admission/reasoning/stop | Omni-DeepSearch 只提供 audio-entity 与 fixed-budget 消融；AudioRAG 没有 tool ablation | **协议不闭合。** 完整分解需要新标注、新指标和新增实验臂 |

最直接的矛盾在 H1：R2 把“是否需要检索”写成首要研究问题，却选择了两个经过 construction-time filtering、
几乎全体要求检索的 benchmark。官方数据没有 negative class；没有负类就不能测 need detection；自行补
负类会把项目带回自制数据集。

## 3. 直接参考论文的真实技术贡献

### 3.1 AudioRAG（2602.10656）

**论文贡献。** 论文发布 500 个 audio reasoning + information retrieval 问题：80% 由 GPT-4o 根据 MMAU、
CinePile、MNSC、FMA、Jazznet、MusicNet、iNaturalist 与 CHEER 的音频 metadata 生成，20% 由在线音视频
人工整理。它还提供一个 WebThinker 风格的 text-controller pipeline：Qwen3-8B 决定何时调用 Google Search
和何时以自然语言 query 调用 frozen omni audio tool。

**论文数据、基线和指标。** 数据集为作者发布的 500 题 AudioRAG；论文没有另给 train/dev/test 划分。
基线包括 Qwen2.5-Omni、Audio Flamingo 3、Audio-Reasoner、Baichuan-Omni、Qwen3-Omni、Gemini-2.5-Flash，
以及 `Qwen2.5/3-Omni + Qwen3-8B` agentic pipeline。主指标是 GPT-4o judge accuracy，三次运行平均；错误按
Reasoning / Audio Processing / Knowledge / Invalid 四类归因。Qwen3-Omni raw 为 37.0%，加入 Qwen3-8B
controller 后为 46.2%。

**对 R2 的边界。** 论文证明 audio-driven external retrieval 可以作为系统能力载体，但没有 need gate、
search-call cost、hop count、retrieval quality、tool ablation 或显式 stop policy。pipeline 同时增加了额外 text
reasoner、问题分解和 web retrieval，因此 37.0→46.2 不能单独归因给“更好的检索调度”。作者自己的错误
分析还显示 agentic pipeline 增加 Invalid Answer，归因于复杂推理进入无限循环；这是 R6/R8 的 stopping 与
rollback 证据，不是 R2 已发布的调度方法。

### 3.2 Omni-DeepSearch（2605.08762）

**论文贡献。** 论文把“仅从 audio 起步，主动检索 text/image/video，再做多跳推理”正式定义成 benchmark。
正式发布 640 题、15 个细分类别，覆盖 single/multi-audio、text/image/video retrieval 与 speech/music/
animal/environment audio。construction-time filtering 检查 audio dependence、retrieval necessity、visual
necessity、answer uniqueness 与 verifiability。

**论文数据、基线和指标。** 官方 Hugging Face 资产共有 640 条，当前发布为一个 `train` split；每条包含
`task_category/sample_id/audio_file/question/answer/golden_path`，不包含冻结网页、文档 ID 或检索轨迹。
论文比较多种 Gemini、Qwen、MiMo 模型在统一 tool-augmented pipeline 下的 accuracy；三位 LLM judge
（GPT-5.4、Gemini-3-Pro、Claude-Sonnet-4.6）独立判断语义等价并多数投票。论文还报告 retrieval modality、
audio content subgroup、搜索预算 `(5,1)/(10,3)/(15,5)` 与 audio-entity inference/provided-entity 消融。

**对 R2 的边界。** 搜索预算从 `(5,1)` 增至 `(10,3)` 时 Gemini-3-Pro 平均 accuracy 由 29.06% 升到
43.44%，继续增至 `(15,5)` 只有 44.06%；但 subgroup 中同时有上升和下降，作者给出过度搜索导致正确证据
被干扰、最终耗尽预算的案例。它证明“预算不是越多越好”，却没有实现逐实例调度器。官方数据也没有
negative no-retrieval 类、正式 dev/test 划分或可复放的 retrieval snapshot；在不新增数据/协议的前提下，
只能把它作为 R6/R8 的外部知识 carrier，而不能据此闭合独立 R2。

### 3.3 VoiceAgentRAG（2603.02206）

**论文贡献。** 论文提出 Slow Thinker/Fast Talker 双 agent memory router：后台预测 3–5 个后续主题并把文档
预取进 FAISS cache，前台优先从 cache 读取，miss 时回退 Qdrant。最有价值的工程贡献是用 document
embedding 而不是 prediction-query embedding 建索引，以及跨 turn 的异步 prefetch/cache architecture。

**论文数据、基线和指标。** 作者自建 NovaCRM synthetic KB（12 documents、76 chunks）和 10 个场景×20
turn 的 200 条 scripted text queries。基线是 Traditional RAG，比较 dual-agent 版本的 cache hit rate 与
retrieval latency：overall hit rate 75%，cache hit 时 110.4ms→0.35ms，报告 316× retrieval speedup。

**对 R2 的边界。** 实验没有真实 speech/audio 输入，也没有答案正确性、groundedness 或 faithfulness 指标；
作者明确把 retrieval latency 作为 primary metric，因为 total latency 被 500–8000ms 的 LLM generation 方差
主导。它适合作为 R9 交互系统的 latency harness，或为 R3/R7 提供跨轮 cache 结构参考，但不能作为
“音频原生外部知识能力提升”的研究基线。

## 4. 数据与协议可承载性

| 资产 | 参考论文原始用途 | 当前可直接复用内容 | 不能自行补造的部分 | R2 处置 |
|---|---|---|---|---|
| AudioRAG-500 | audio + web retrieval benchmark | 500 题、原音、答案、paper prompt、accuracy 与四类错误 | frozen web corpus、need/no-need 标签、tool ablation、正式 split | 按需作为 R5/R6/R8 外部知识 carrier；不形成独立 R2 |
| Omni-DeepSearch-640 | audio-initiated text/image/video deep search | 官方 640 题、audio、answer、golden path、15 类分组、accuracy | retrieval snapshot、网页证据、dev/test、no-retrieval negative class | 按需作为 R6/R8 carrier；live-search 结果只按论文边界解释 |
| VoiceAgentRAG-200 | text RAG latency/cache | synthetic KB、scripted queries、Traditional RAG、hit-rate/latency | speech quality、answer quality、audio grounding | 仅作系统 latency/cache 参考，不承担 R2 能力结论 |

Omni-DeepSearch 官方资产已经本地存在，但目前只是 `LOCAL_CANDIDATE_UNFROZEN`；AudioRAG 与
VoiceAgentRAG 尚未进入 `docs/datasets.lock.json`。Stage-1C 不进行新下载或执行，这些 readiness 事实不改变
方向判断。

## 5. 基线与评价体系不能被合并成一项 R2 实验

三篇直接论文回答的是三个不同问题：

1. AudioRAG：加入 text controller + audio tool + live web 的整条 pipeline 是否优于 raw LALM；
2. Omni-DeepSearch：不同 omni model 在同一开放搜索任务上能做到什么，以及固定搜索预算怎样影响 accuracy；
3. VoiceAgentRAG：跨轮预取能否降低远程 vector DB 的 retrieval latency。

它们的实验单位、信息源、系统组成和主指标均不同。正确的复用方式是让消费它们的方向分别复用原论文
baseline 与 metric，而不是为 R2 新造统一评价体系：

- R5 若使用 AudioRAG，比较 raw core 与论文 agentic wrapper，并保留 A/B/C/D error taxonomy；
- R6 若使用 Omni-DeepSearch，比较论文 fixed search budgets 与自身已获授权的 trajectory baselines，并继续用
  official accuracy/subgroup reporting；
- R8 在同一 carrier 上报告论文已有的 subgroup 与 budget regression，不额外发明 R2 总分；
- R9 若研究 voice latency，复用 VoiceAgentRAG 的 Traditional RAG、hit rate 与 retrieval latency。

这也说明为什么“完整复现 R2”没有独立必要性：基线复现应由实际使用对应 action/carrier 的研究完成。

## 6. 参考论文中应重路由的技术贡献

| 技术贡献 | 不应再被称为 R2 独立贡献的原因 | 正确路由 |
|---|---|---|
| AudioRAG 的 omni-as-audio-tool、text controller 与四类错误 | 已是发表 pipeline；系统角色与 evidence flow 属于架构 | R5 |
| AudioRAG/Omni-DeepSearch 的 query、search、retry、stop 轨迹 | 下一动作与有限预算正是实例内 trajectory control | R6 |
| Omni-DeepSearch 的 fixed-budget saturation 与 over-search failure | 提供条件异质性、尾部回归和 rollback 动机 | R8 |
| Omni-DeepSearch 的 audio-only start 与 golden path | 是外部知识 carrier 和离线诊断资产，不是新方法 | R6/R8，必要时 R9 |
| VoiceAgentRAG 的 document-embedding cache 与 async prefetch | 主要贡献是跨轮状态复用和 latency engineering | R3/R7 或 R9 |
| frozen/live retrieval、provenance 与 raw-audio preservation | 是实验可复现与 evidence-state invariant | R5/shared protocol |

外部知识 action 仍然保留在项目 action menu 中；日落的是 R2 这个独立课题和 Stage-2D 名额，而不是删除
知识检索能力。

## 7. Stage-1C 处置建议

建议 owner 采用：

**`NO_GO_AS_STANDALONE_DIRECTION__MERGE_AS_OPTIONAL_EXTERNAL_KNOWLEDGE_CARRIER`**。

采用后：

1. R2 不进入 Stage-2D，portfolio 不再为 R2 单独安排复现、prototype 或 controller；
2. R2 本报告作为方向淘汰与文献归纳记录保留；
3. AudioRAG、Omni-DeepSearch、VoiceAgentRAG 的数据、baseline 和 metric 分别迁入实际消费它们的方向；
4. R5+R6+R8 仍先在既定闭集 carrier 上验证核心控制问题，不因 R2 报告自动接入 live web；
5. 只有当某个保留方向的研究问题确实需要 waveform 外部事实时，才在独立 Stage-2 合同中启用对应官方
   benchmark；不得为了恢复 R2 而新增数据或指标。

如果 owner 不接受日落，R2 也不能按当前 proposal 直接进入 Stage-2：至少要先证明一个参考论文原样发布的
数据集同时包含 need/no-need 对照、正式 split、可复放检索环境和原论文评价指标。当前证据不满足这些条件。

## 8. Provenance 与暴露声明

- 直接全文：AudioRAG 2602.10656（PMLR 312，PDF pp.1–8、11–13）；VoiceAgentRAG 2603.02206v2
  （PDF pp.1–11、13）；Omni-DeepSearch 2605.08762v1（PDF pp.1–12、15–28、42–43）。
- 本地证据：`2026-07-26-d1-knowledge-dossier-draft.md`、Stage-1B registry、官方本地
  Omni-DeepSearch 640-item asset 与其 README/schema。
- 本轮没有新增发现查询、模型/API 调用、数据下载、指标运行、复现或原型实现。
- 论文数字是参考论文结果，不是本项目实验结果；Omni-DeepSearch 的本地存在只证明资产可读，不证明
  复现、license closure 或检索环境可重放。
