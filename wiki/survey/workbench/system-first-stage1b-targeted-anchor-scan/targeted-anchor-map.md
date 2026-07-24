# Stage-1B 定向锚点事实地图（中文）

本文只回答“新扫描到了什么、论文怎么做实验、对 Stage‑1B 有什么证据用途、最强限制是什么”。
它不是研究方向排序、Stage‑1C family 统合或 research proposal。

## 一、speech/omni 直接实验与系统锚点候选

| 论文 | 论文实验设置 | Stage‑1B 用途 | 最强限制 |
|---|---|---|---|
| [Audio MultiChallenge](https://arxiv.org/abs/2512.14865) | 452 段自然多轮对话、47 位说话人、1,712 个 instance rubrics；固定相同历史，只评价最后一轮；拆成 inference memory、instruction retention、self coherence、voice editing，并比较 text/audio output 与 semantic/audio-cue memory。 | `BORROWED_PROTOCOL_ANALOGUE`；直接补足多轮语音记忆、指令保持和音频线索的测量合同；是 task-matched instrument candidate。 | 固定历史避免了早轮误差传播，因此不测模型从自身错误中恢复；LLM judge 仍是代理评价器。 |
| [MultiVox](https://arxiv.org/abs/2507.10859) | 1,000 个真人录制的 speech+image/video 样本；paired sample 固定文字和视觉、翻转语音属性，测试 speech cue 是否改变答案。 | `BORROWED_PROTOCOL_ANALOGUE`；提供去混杂的 MM3 因果多模态设计，可区分“有音频输入”和“必须利用音频”。 | 单轮、受控 benchmark，不覆盖长期状态、行动和恢复。 |
| [VCB Bench](https://arxiv.org/abs/2510.11098) | 音频对话的 instruction/knowledge/robustness 多维评价，含 clean/perturbed 条件，并对比客观与主观评价。 | `BORROWED_PROTOCOL_ANALOGUE`；补充音频对话 robustness 与 evaluator-disagreement instrument。 | 自动/主观评价并不一致；数据与 judge 尚未做本地 closure。 |
| [RealTalk-CN](https://arxiv.org/abs/2508.10015) | 中文 speech-text task-oriented dialogue，控制 disfluency、speaker、domain 和 modality switching。 | `BORROWED_PROTOCOL_ANALOGUE`；提供自然不流畅语音与跨模态切换的系统压力测试结构。 | 中文域和任务本体限制可迁移性；不是通用 omni control 实验。 |
| [Full-Duplex-Bench-v2](https://arxiv.org/abs/2510.07838) | 自动 examiner 与 WebRTC streaming；Daily、Correction、Entity Tracking、Safety 等任务；区分 turn-taking 与任务目标。 | `BORROWED_PROTOCOL_ANALOGUE`；是现有 FDB-v3 路由的 lineage 邻近节点，也是 full-duplex nearest-prior candidate。 | v2/v3 的数据、代码、协议修订与 evaluator 必须逐项闭合，现阶段不能称复现锚点。 |
| [Speech-Hands](https://arxiv.org/abs/2601.09413) | 用 internal/external/rewrite action token 做 ASR 与 audio-QA 自反思；action label 来自 ground truth，主体方案经过 SFT，另含 GRPO 比较。 | `REFERENCE_CONTEXT`；提供语音 agent 的显式 action space 与 rewrite 对照。 | 参数训练且使用 ground-truth-derived action label，不是 training-free 外部控制。 |
| [Temporal Contrastive Decoding](https://arxiv.org/abs/2604.15383) | 原音频与 temporal-blur 音频两路 next-token logits 做 contrastive decoding；在 MMAU/AIR 等条件比较。 | `REFERENCE_CONTEXT`；补入直接 audio training-free comparator，并清楚标记 gray-box access。 | 需要统一 LALM 内部 logits；属于模型输出解码，不是外部 action/reward control，语音分层结果也不应过度外推。 |
| [CESAR / process reward](https://arxiv.org/abs/2510.20867) | MMAU/MMSU/MMAR 上训练 audio process reward，含 process-reward ablation 与 test-time scaling。 | `REFERENCE_CONTEXT`；提供过程奖励怎样监督 audio reasoning 的训练边界。 | 奖励模型与策略均依赖训练，不能当作冻结核心的 training-free 证据。 |
| [Native Active Perception / OmniAgent](https://arxiv.org/abs/2606.19341) | 将 omni agent 表述为 POMDP；browse/listen/watch action、持久文本 memory、Agentic-SFT+TAURA RL，并测 positive test-time scaling。 | `REFERENCE_CONTEXT`；补齐 omni 主动感知、持久状态、工具动作与预算的系统上界设计。 | 所有主要收益经过 SFT/RL；持久 memory 是文本载体，不能归因于原生多模态记忆。 |
| [OmniRAG-Agent](https://arxiv.org/abs/2602.03707) | 图像/音频检索工具、最多 20 轮、GRPO，format+answer reward；音频工具返回 ASR transcript。 | `REFERENCE_CONTEXT`；提供长音视频 retrieval/action/stopping 的训练型系统边界。 | 并非 training-free；音频证据被转写成文本，不能证明音频原生控制。 |

## 二、多模态知识与主动证据获取

| 论文 | 论文实验设置 | Stage‑1B 用途 | 最强限制 |
|---|---|---|---|
| [When Seeing Is not Enough / GuessBench](https://arxiv.org/abs/2510.15421) | passive/full-information 对 active/incomplete-evidence；评价提问获取信息、何时停止和最终回答，覆盖约 20 个 MLLM。 | `BORROWED_PROTOCOL_ANALOGUE`；提供“被动给证据—主动问证据—停止”的 matched protocol 与 falsifier。 | 视觉猜测任务，不含 speech/omni；问问题能力和真实工具交互仍有差距。 |
| [M3-VQA](https://arxiv.org/abs/2604.25122) | 约 13k 样本；no knowledge、gold evidence、retrieval，及 heuristic/ reasoning-aware agentic retrieval；答案绑定可追溯证据。 | `BORROWED_PROTOCOL_ANALOGUE`；拆开知识缺失、检索失败、推理失败，并提供 gold-evidence oracle。 | 视觉多实体知识任务；gold evidence 和图像检索资产不可直接迁到音频。 |
| [GranuRAG](https://arxiv.org/abs/2605.15019) | 1,422 张图、71 个 landmarks，标注 element visibility；比较 scene/element evidence、baseline/CoT/GranuRAG，并测 attribution precision/recall/UCR。 | `BORROWED_PROTOCOL_ANALOGUE`；借鉴多粒度证据、部分可见控制与 unsupported-claim 指标。 | 地标数据域窄；即使最佳设置仍有 unsupported claims，且没有音频模态。 |
| [Utility-Oriented Visual Evidence Selection](https://arxiv.org/abs/2605.13277) | MRAG/Visual-RAG；比较 no-RAG、相关性、answer uncertainty、latent helpfulness、GT oracle、不同 surrogate。 | `BORROWED_PROTOCOL_ANALOGUE`；提供 relevance-versus-utility、top-k、surrogate/main-model 和 oracle arms。 | 虽称 training-free selection，但需要 surrogate final-layer logits 和学习模型；不满足严格 black-box。 |

知识方向得到的关键实验变量不是“是否加 RAG”一个开关，而是：候选证据供给、证据粒度、主动获取、
utility/relevance 区分、证据预算、停止、gold-evidence oracle 与最终 claim attribution。是否迁入语音/omni，
留待后续 Stage‑1C 分析，不在这里下结论。

## 三、多模态技能

| 论文 | 论文实验设置 | Stage‑1B 用途 | 最强限制 |
|---|---|---|---|
| [VISUALSKILL](https://arxiv.org/abs/2606.18448) | 177 个 computer-use tasks；层级化多模态 skill 与按需 `load_topic`；比较 no skill、同源 matched text-only skill、visual skill，并分析 construction/access 阶段。 | `BORROWED_PROTOCOL_ANALOGUE`；目前最干净的“同一技能内容、不同载体模态”对照之一，支持 MM3 协议设计。 | GUI 域且依赖 MCP/视觉资产；只有 matched text-only 对照能支撑模态因果，不能把总体增益全归为视觉技能。 |
| [SkillOps](https://arxiv.org/abs/2605.13716) | typed skill contract、HSEG、merge/repair/retire/validator/adapter；ALFWorld 中测试 200–2,000 skill libraries，并注入重复、冲突和退化。 | `BORROWED_PROTOCOL_ANALOGUE`；提供技能库规模、污染、合并、维护和适配器的系统化压力测试。 | 文本环境；大部分规模实验依赖合成退化，收益依赖特定 skill schema/validator。 |

技能记录被定义为“可复用程序/策略内容”。把 skill 文档存到库里，只能说明 memory 是载体；要证明
多模态技能本身有效，需要 matched text-only、相同来源、相同 access/budget 的对照。

## 四、多模态与 agent memory

| 论文 | 论文实验设置 | Stage‑1B 用途 | 最强限制 |
|---|---|---|---|
| [Mem-Gallery](https://arxiv.org/abs/2601.03515) | multimodal multi-session conversation；覆盖 extraction/adaptation、reasoning、management，比较 Full(Text)/Full(MM)、memory baselines 和 top-k。 | `BORROWED_PROTOCOL_ANALOGUE`；提供多模态长期记忆的内容模态、管理阶段和检索预算分层。 | 视觉语言域；多模态收益可能来自信息量，不等于证明模态形式本身必要。 |
| [Mem2ActBench](https://arxiv.org/abs/2601.19935) | 400 tasks、2,029 sessions；no/passive/oracle retrieval；把 retrieval 与 retrieved-but-unused 分开，并测 tool 与 argument。 | `BORROWED_PROTOCOL_ANALOGUE`；将“记住”拆成检索、使用和行动正确性，提供 oracle retrieval arm。 | 文本 agent；被动提供 memory 不等于真实 memory manager。 |
| [ImplicitMemBench](https://arxiv.org/abs/2604.08064) | 300 items；procedural memory、priming、conditioning；Learn/Prime–Interfere–Test，并采用 first-attempt scoring。 | `BORROWED_PROTOCOL_ANALOGUE`；用于区分显式回忆、技能自动执行和干扰后的行为适应。 | text-only 且主要是同一上下文内暴露，可能是 in-context learning，不是持久 memory。 |
| [AgeMem](https://arxiv.org/abs/2601.01885) | 统一 LTM/STM tool policy：add/update/delete/retrieve/summarize/discard；五个长程文本 benchmark，三阶段 step-wise GRPO。 | `REFERENCE_CONTEXT`；提供完整 memory action space 与 LTM/STM 协同边界。 | 文本且参数训练；不能把统一策略的收益归因于 training-free memory control。 |

memory 的实验必须分别观测写入/检索、取回内容的正确性、是否被决策真正使用、干扰/遗忘、跨会话
持久性和最终行动；只测最终任务分数会混淆知识、技能、memory 和系统 carrier。

## 五、training-free control、test-time scaling 与反证

| 论文 | 论文实验设置 | Stage‑1B 用途 | 最强限制 |
|---|---|---|---|
| [Energy-Based Decoding](https://arxiv.org/abs/2605.28020) | 冻结 text base model、外部轻量 reward、blockwise Metropolis-Hastings suffix refinement。 | `BORROWED_PROTOCOL_ANALOGUE`；提供明确 reward、proposal、accept/reject、预算与质量-成本结构。 | 控制对象仍是文本输出 suffix，不是外部工具/环境 action；reward model 本身是额外模型。 |
| [ThinkBooster](https://arxiv.org/abs/2606.06915) | 统一 test-time strategy library 与 proxy/scorer；显式分类 black-box/white-box 方法，并报告质量-成本。 | `BORROWED_PROTOCOL_ANALOGUE`；借鉴 strategy registry、access classification、scorer 与 budget accounting。 | 仅一部分策略满足 hosted black-box；统一框架结果不能抹平各策略的 access 差异。 |
| [Limits and Gains of TTS in VLM](https://arxiv.org/abs/2512.11109) | zero-shot、CoT、BoN、self-consistency、self-refinement、beam；MathVista/MMMU/MMBench，典型 N=5。 | `BORROWED_PROTOCOL_ANALOGUE` + falsifier；要求同时设置 internal confidence、external verifier、perception/reasoning strata。 | self-refinement 可伤害开放模型，perception task 可能没有可扩展 headroom；“多采样必增益”不成立。 |
| [Visual Test-time Scaling / RegionFocus](https://arxiv.org/abs/2505.00684) | GUI grounding；错误触发额外 crop/zoom perception，维护 image-as-map history；ScreenSpot/WebVoyager。 | `BORROWED_PROTOCOL_ANALOGUE`；提供 error-triggered observe/action、visual/text history 与额外感知预算的消融。 | 静态页面上的 VLM judge trigger、开销大；不等于动态环境中的可校准控制。 |

这些论文共同要求 Stage‑1B 继续保留 access contract：严格 black-box、可读 logprob/logit 的 gray-box、
可改模型内部状态的 white-box 和经过参数训练的 policy 不能合并成同一个“training-free RL”类别。

## 六、未纳入但保留扫描轨迹

| 论文 | 扫描结论 | 未纳入理由 |
|---|---|---|
| [Agent Skills Should Go Beyond Text](https://arxiv.org/abs/2606.01414) | 提出 static/dynamic/interleaved visual skill taxonomy，并有 work-in-progress 实验。 | 属 position/work-in-progress；同批 VISUALSKILL 已以更完整 matched control 覆盖该路径。 |
| [MCMA](https://arxiv.org/abs/2601.07470) | DPO 训练文本 memory copilot。 | 训练型文本 memory 边界与既有 Memory-R1 及同批 AgeMem 重叠，没有形成不可替代的新节点。 |

两篇的 PDF/e-print/文本及哈希仍在 scan record 和 external-binding report 中，因而“扫描过但未纳入”
是可审计状态，不会在以后被误当成遗漏或无理由退出。

## 七、现阶段能说与不能说

能说：新增证据覆盖了 speech/omni 的多轮/全双工/主动感知，以及视觉/文本 agent 中的主动知识获取、
多模态技能、长期/隐式 memory、test-time selection 和系统维护协议；其中多个实验结构值得后续分析。

不能说：哪一个方向最优、项目 novelty 在哪里、某论文可直接复现、某视觉/文本结果可迁移到语音，或
320 篇已经成为 Stage‑1C 的签名输入。这些结论需要独立 release verdict 和后续单独授权的分析阶段。
