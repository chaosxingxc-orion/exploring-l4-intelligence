---
artifact_id: "SF-P0R9-SEVEN-PAPERS-DFS-2026-07-18-01"
title: "P0-R9 七篇威胁论文 DFS 深读记录（全文精读,owner 裁决③：DFS 四问,非静态占位矩阵）"
date: 2026-07-18
method: "两个隔离深读代理（Opus）逐篇全文 PDF 精读（本地 fulltext 双份,台账 14/14）;schema = DFS 四问（方法/局限/改进空间/可借鉴）+ 身份轴事实（冻结/访问级别/信息来源/训练审计/控制机制/优化信号/任务范围/负结果）+ 与本项目关系（仅事实差异）"
verification: "承重引文抽查:主执行方对 3 篇 PDF 逐字 grep 复核 5/6 命中（2508.10016『training-free integration and control』/『no gradient-based training』;2606.08231『does not cover audio』×2 处;2602.23306『shared vocabularies … for logit fusion』;第 6 条为 hyphenation 改写差异非事实错误）"
discipline: "owner 裁决④（2026-07-18）:创新点尚未锁定——本件只载事实身份轴差异,禁止任何『创新点成立/不成立』定性;评审 P0-R9 §4 定位语 owner 未签,不进本件"
loadbearing_facts: "①2606.08231(ACL TTS survey)明文排除 audio/speech——speech/omni 方法空位的文献坐标;②2508.10016 自称仅『training-free integration and control』,是专家联邦+确定性路由,无候选采样/无 selector/无 reward;③2602.23306 = logits 级融合+外部 LRM(new-info),干净落在黑盒边界外;④2512.11109:外部 verifier>内部 confidence 一致成立、弱模型 Self-Refinement 退化、感知饱和任务无头空——selector 适用条件先验"
---

# P0-R9 七篇威胁论文 DFS 深读记录

## 批次 A（代理一:2508.10016 / 2602.23306 / 2512.11109 / 2606.08231〔导航级〕）

## 2508.10016 Training-Free Multimodal Large Language Model Orchestration

### DFS 四问
- **方法**：off-the-shelf LLM 控制器（Qwen2.5-14B，确定性解码 temp=0.0）根据用户意图发射闭词表控制 token（`[S.need_vision]`/`[S.need_audio]`/`[S.stop]` 等）；确定性 router 校验 token 并按静态 token→expert 映射调度**外部现成专家模型**（Qwen2.5-VL-32B/72B 视觉、Whisper-Small ASR、OCR/math）。三组件：C1 控制器路由、C2 text-centric evidence-keyed 跨模态记忆（cache-or-call，按 image hash / video chunk id / audio timestamp + SHA-1 checksum 精确键匹配复用）、C3 统一交互层（full-duplex 流式 + barge-in 取消）。专家输出被 textualize 成文本证据回灌，控制器只见文本 query + evidence key，永不见原始 payload。
- **局限**（自认+观察）：稀疏帧采样下细粒度时序计数退化（WorldSense Action Counting 23.03%、Object Counting 31.22%、Audio Counting 34.44%）；查询缺乏明确模态触发时路由歧义（Video-MME 0.8%、WorldSense 0.9% 无效路由，走 safe fallback）；连续频繁打断降低响应性；精确键匹配→局部扰动即 cache miss（有界重算）。实验仅 8×A100、seed=42、官方评测脚本。**范围观察**：无候选采样/无 selector/无 reward——纯确定性路由，因此没有池内择优的故事。
- **改进空间**：路由在歧义 case 是 non-oracle（作者列为 future work）；记忆复用判据是纯 lexical + 精确键，无语义容错（作者刻意选择以避免误复用）；omni 中 audio 类任务整体弱（WorldSense 音频三项 34-42%），说明 ASR 转文本丢失了副语言/声学线索；专家是黑盒文本回灌，无法追问专家（对照 ThinkOmni 的 caption-then-answer 单向缺陷同源）。
- **可借鉴**：evidence-keyed 记忆的 **cache-or-call 可验证复用**（键相等作复用判据，`d(k)=Read if k∈M else CallExpert`）；**闭词表控制 token + 确定性 router 校验 + 无效即 safe fallback**（可审计、可重放 trace：token→route→cache-or-call→output）；**commit-on-complete** 规则（只有完成的专家输出/最终段落入记忆，partial/canceled 保持 ephemeral）；barge-in 取消语义。这些是外部控制平面里 memory/routing/verification/stopping 四机制的成熟工程模板。

### 身份轴事实
- **冻结核心**：**不改权重、不改结构**。但**非单一冻结核心**——是「控制器 LLM + 专家联邦」多模型编排。原文 p2:"we perform no gradient-based training or fine-tuning for orchestration components... we only use static prompt specifications"；且明确 "We do not claim training-free multimodal capability; rather, we claim training-free integration and control"。omni 能力来自路由到分立视觉/ASR/TTS 专家，**不是激活单一 core 的预训练知识**。
- **访问级别**：**文本输出级（对专家黑盒）**。专家 "returns textualized evidence (as text tokens)"，控制器只观察 text query + evidence key，"never directly accesses the payload"（p5）。不碰 logits/hidden-state/梯度。**未越出黑盒**，但代价是多模型联邦。
- **信息来源**：专家做感知/格式转换，**不注入外部知识**——p3:"use experts strictly for modality perception/format conversion without external knowledge access"。即对输入自身内容的 read-out。但从「单一 core」视角，视觉/ASR 专家本身是**核心之外的额外模型**。
- **训练审计**：编排组件**零训练**（controller/router/memory/interaction 全静态 prompt）；专家全 off-the-shelf 预训练。注：Appendix F.3 有一个 LoRA 微调 controller 的**对照基线**（7,500 轨迹，非其方法；训练版 99.20% vs 免训 99.10%，仅 0.1% 差）——他们的方法本身不训练。
- **控制机制**：**routing + memory(cache-or-call) + verification(token schema/router 校验) + stopping(barge-in/[S.stop])** 在场；**无 sampling/selection/search/refinement**（确定性解码，无候选池）。
- **优化信号**：**rule-based**——router 确定性校验 + evidence-key 精确相等（"Key equality is the default reuse criterion"）。无 reward/confidence/consensus/learned evaluator。
- **任务范围**：**omni 多任务，含 speech/audio**。模态=image/video（视觉专家）+ audio/speech（ASR 专家 Whisper）+ text。基准：MME/MMBench/MMStar/MMMU/LVBench/Video-MME/WorldSense(holistic omni 含音频)/MathVision/CC-OCR。
- **负结果与适用条件**：(1) 路由歧义无明确模态触发→保守 no-op/延迟（0.8-0.9%）；(2) 稀疏采样下快速时序/计数任务退化；(3) 频繁连续打断降响应；(4) 精确键→轻微输入变动触发局部重算；(5) 音频类任务系统性偏弱（ASR 文本化丢声学线索）。

### 与本项目关系
- **重合组件**：外部控制平面的 memory（evidence-keyed cache-or-call）、routing（闭词表 token）、verification（schema 校验+fallback）、stopping（barge-in）；训练-free 整合；omni 含 speech；黑盒文本级访问；read-out-only（感知/格式转换，无外部知识）——**信息边界轴与本项目一致**。
- **关键身份差异**：(1) **多模型专家联邦 vs 单一冻结 speech/omni 核心**——本项目激活「一个 core 自身预训练知识」，此文用分立专家拼装 omni，是不同的能力来源；(2) **无候选采样/无 selector/无 reward**——确定性路由，没有 K 池、rho、oracle headroom 的度量对象；(3) 优化信号是 rule-based 键相等，非本项目的 reward/评分引导。
- **角色建议**：**component-prior**——它是外部控制平面 memory/routing/verification/stopping 四机制的现成工程模板（尤其 cache-or-call 可验证复用与 commit-on-complete），但在「核心身份轴」上是专家联邦而非单核激活，且缺 selector/reward 层，故不构成 exact-overlap。

## 2602.23306 ThinkOmni: Lifting Textual Reasoning to Omni-modal Scenarios via Guidance Decoding

### DFS 四问
- **方法**：**logits 级 guidance decoding**，融合冻结 OLLM（Qwen2.5-Omni-3B/7B、Omni-R1）与冻结 off-the-shelf LRM（DeepSeek-R1-Distill-Qwen-7B / Qwen3-8B，thinking mode）。①LRM-as-a-Guide：对比对 `ẑ = z_base + α·(z+ − z−)`，其中 `z_base=OLLM(x<t,O)`（全 omni 输入）、`z−=OLLM(x<t)`（**丢弃 omni 内容**只喂文本前缀）、`z+=LRM(x<t)`（LRM 只读文本前缀）。②Stepwise Contrastive Scaling：每步用三分布间 Jensen-Shannon 散度 `DR=JS(PR‖P)`、`DP=JS(PO‖P)` 自适应定权 `αr_t=clip(DR−DP,0,1)`（前 5 步 warmup），无需手调超参。单遍解码，逐 token 混合 logits 后采样。
- **局限**（自认+观察）：**要求 OLLM 与 LRM 共享词表**（同族）；额外前向开销（generate 阶段 2.88×）；LRM 无 omni 访问只能靠已解码文本前缀补偿。观察：本质是双模型 ensemble，非激活单核；LRM 知识偏科学/数学，音频/general omni 增益小（MMAU/OmniBench +0.4~+1.5 vs MathVision +7.9）。
- **改进空间**：LRM 完全看不到模态内容，靠文本轨迹「盲推」——感知错则推理必错（failure case b：音频鼓点起始时刻误判）；αr 仅由 logits 散度驱动，无真值/无外部校验，属启发式；共享词表限制排除了跨族强 LRM；作者自问 "what truly works during the reasoning process" 尚未解释机制。
- **可借鉴**：**per-step 自适应权重（JS 散度衡量感知 vs 推理主导度）** 的思路可迁移为「无标签的步级信号」；**对比式「移除模态输入」作 negative**（aggressive visual contrastive，直接删非文本输入而非加噪）；把「快思考感知 / 慢思考推理」显式解耦的分析框架。但注意：这些机制**依赖 logits**，本项目黑盒下不可直接用。

### 身份轴事实
- **冻结核心**：**不改权重、不改结构**，但**双模型 logits 融合**（OLLM+LRM），非单一核心。p5:"the entire ThinkOmni procedure is training-free, requiring no additional finetuning or corpus statistics"〔抽查注:该句为改写级引文,hyphenation/措辞与原文有出入;同页 Limitation 段『requires shared vocabularies between the OLLM and LRM for logit fusion』已逐字复核命中〕。
- **访问级别**：**LOGITS**（关键越界轴）。全程操作 next-token logits `zt∈R^V`、混合 logits（Eq 2/3/5/8）。p10 Limitation:"ThinkOmni requires shared vocabularies between the OLLM and LRM for logit fusion"。**远超出黑盒/文本输出级**，需完整 logit 向量 + 词表对齐。
- **信息来源**：**new-info 注入**——外部 LRM 提供其参数化推理知识；p4:"we discard the omni-modal content and feed MO only the textual prefix"，LRM 只读文本前缀不读 omni。guidance 是**外部模型知识注入**，非 OLLM 自身知识的 read-out。
- **训练审计**：**零训练**，全 off-the-shelf 公开模型（Qwen2.5-Omni / Omni-R1 / DeepSeek-R1 / Qwen3）。
- **控制机制**：**均不在场**（无 routing/sampling/selection/search/memory/stopping）。唯一机制=解码时 logit 级 steering（单遍，逐 token 混合）。
- **优化信号**：**内部 confidence/disagreement 型**——JS 散度在线度量三分布分歧定权。非 reward model / external critic / consensus / gold。
- **任务范围**：**omni 多任务推理，含 audio/speech**。视觉：MathVista/MathVision/MathVerse；音频：MMAU(speech/sounds/music)；音视频：Daily-Omni/OmniBench。共 6 基准 >10,000 样本。
- **负结果与适用条件**：固定 α 次优（极端 α 两基准都降）；Average Logits Fusion −11.8/−15.8/−6.0（朴素混合有害）；Caption-then-Answer 降（信息单向流，OLLM 无法响应 LRM 需求）；VCD 在 MathVista 降（增感知非增推理）；LRM 太小则退化（词表/能力不匹配）；Qwen3-14B 在 MMAU/OmniBench 无进一步增益；失败模式：感知对但推理错（600ml 标签 vs 400ml 刻度冲突）、感知错致推理错（鼓点起始）。

### 与本项目关系
- **重合组件**：训练-free、冻结模型、推理时、omni 含 audio、目标「激活/提升推理」、per-step 自适应无手调。
- **关键身份差异**：(1) **logits 访问**——直接违反本项目严格黑盒（只见文本输出）；(2) **外部 LRM = new-info 注入**——违反单一冻结核心 + read-out-only（引入另一模型的参数知识）；(3) 需共享词表/同族；(4) **无候选池/无 selector**——是 logit 融合不是对 K 池择优，无 rho/headroom 结构；(5) 双模型 ensemble 非单核激活。
- **角色建议**：**boundary-comparator**——它是「黑盒边界外一步」的典范（logits + 外部模型 + new-info），干净地落在访问级轴与信息边界轴的**违规侧**，正可用来锐化界定本项目「不做什么」。

## 2512.11109 Limits and Gains of Test-Time Scaling in Vision-Language Reasoning

### DFS 四问
- **方法**：系统性**实证研究**（非新系统），对 6 种推理时方法——CoT、Best-of-N、Self-Consistency、Self-Refinement、Beam Search——在开源（Qwen2.5-VL-7B、InternVL2.5-8B、Mulberry-8B）与闭源（Gemini-2 Flash、GPT-4o-mini、Claude-3-Haiku）VLM 上、于 MathVista/MMMU/MMBench 做横切评测。Best-of-N 用两类验证：内部 confidence（logits log-likelihood，仅开源）+ 外部 verifier（Gemini-2 作 judge，映射 excellent/good/.../bad → 1.0/0.75/.../0.0）。Beam Search 同分 confidence-based（开源）/verifier-based（闭源）。
- **局限**（自认+观察）：仅 3 基准、每模型部分方法（闭源拿不到内部 confidence）；MMBench 只报小分类 correct/total（n 极小，如 Spatial 3/4）；无速度/成本分析；外部 verifier 固定用 Gemini-2（引入强外部模型）。**范围**：纯 vision-language，**无 audio/speech**。
- **改进空间**：作者点名 future work=「自适应 TTS」+「多模态 reward model」——即当前 selector 信号（内部 confidence 不可靠、外部 verifier 靠他家模型）都不理想；未研究 memory/routing/full-duplex；n 小使分类结论仅方向性。
- **可借鉴**：**selector 设计的直接实证证据**——(a) 外部 verifier > 内部 confidence 一致成立（"Best-of-N (Verifier Based) consistently outperforms Best-of-N (Confidence Based)"）；(b) 内部 confidence 不是 correctness 可靠指标；(c) Self-Consistency（多数投票=无标签共识，≈本项目 MBR 等 K 基线）在开源 VLM 常优于 confidence-BoN；(d) Self-Refinement 在弱开源模型常退化，只在强闭源模型受益；(e) 任务依赖强——多步推理受益、感知饱和任务无益。这些是本项目 rho/headroom/selector 适用条件的现成先验。

### 身份轴事实
- **冻结核心**：**不改权重/结构**，每实验单模型；但 Best-of-N/Beam 的 verifier 变体引入**外部辅助模型**（Gemini-2）。
- **访问级别**：**混合**。开源 confidence 变体需 logits——p4:"confidence can be estimated by computing the log-likelihood of each answer using the model's output logits"；闭源 p8:"these models do not expose token-level probabilities"，故只能 verifier-based（文本级）。**confidence 变体越黑盒边界，verifier/majority/CoT/SR 变体在文本输出级、黑盒兼容**。
- **信息来源**：CoT/Self-Consistency/Self-Refinement=纯 **read-out**（模型自生成）；Best-of-N(verifier)/Beam(verifier)=**外部模型评分注入**（Gemini-2 judge，读候选文本打分，非 gold）。混合。
- **训练审计**：**零训练**——未训 reward model（直接用现成 Gemini 当 verifier）；future work 才提议训多模态 reward model。
- **控制机制**：**几乎全在场**——sampling(BoN/Self-Consistency)、selection(reward/verifier/majority vote)、verification(外部 verifier)、search(Beam)、refinement(Self-Refinement 迭代)、stopping(SR 收敛判据/Tmax)。**无 memory/routing**。
- **优化信号**：**多样**——rule/consensus(majority vote)、confidence(内部 logits)、external critic/learned evaluator(Gemini verifier)、self-critique(SR)。
- **任务范围**：**vision-language 多任务**（数学推理 MathVista、多学科 MMMU、细粒度感知 MMBench）；模态=image+text。**不含 audio/speech**。
- **负结果与适用条件**（丰富）：(1) 开源 VLM 的 Self-Refinement 常**降分**（"iterative refinement often degrades performance due to unstable reasoning dynamics"）——弱模型自我批判不可靠；(2) 内部 confidence **不可靠**（"the model's internal confidence score is not a reliable indicator of correctness"）；(3) confidence-Beam 在开源三模型**全部表现差**；(4) 感知中心 MMBench 上 CoT/SC/BoN "produce minimal or no improvement"（浅层 MCQ + 强模型饱和）；(5) TTS 非万能，强任务依赖（多步推理受益、感知任务狭窄增益）。

### 与本项目关系
- **重合组件**：与本项目 selector/rollout 设计空间**高度重合**——Best-of-N（候选采样+择优）、外部 verifier（评分 selector）、Self-Consistency（无标签共识=MBR 等 K 基线）、confidence/verification/stopping。是本项目 selector 问题在 VLM 上的实证地图。
- **关键身份差异**：(1) **纯 vision-language，无 speech/audio**（本项目=speech/omni）；(2) confidence 变体用 logits（开源）——部分越黑盒；但 verifier/majority/CoT/SR 变体黑盒兼容；(3) 外部 verifier=另一个强模型（供给侧 c 的一种），属无标签 proxy S、**不碰 test-item gold**，故信息边界内合规，只是「外部模型」这一杠杆与本项目「激活核心自身信号」姿态不同；(4) 无 memory/routing/full-duplex；(5) 实证研究非系统。
- **角色建议**：**component-prior**——直接为本项目 selector/verification 层提供适用条件证据（外部 verifier>内部 confidence、confidence 不可靠、Self-Refinement 弱模型退化、感知任务无头空），是 rho/headroom 归因纪律的现成先验；但受限于 VL-only 与部分 logits 变体，需在 speech/omni 与严格黑盒下重测（跨供给必重测头空）。

## 2606.08231 Test-Time Scaling in Multimodal Foundation Models: A Comprehensive Survey（导航级深读）

### DFS 四问
- **方法**：首个 MFM 上 TTS 综述。**统一 taxonomy 三范式**（Fig 2）：①sampling-based（Best-of-N / Majority Voting）；②feedback-based（Reward Models[ORM/PRM] / Iterative Refinement）；③search-based（Beam Search / Tree Search / Heuristic-and-Adaptive Search）。**形式化**（Eq 3）`π*=argmax_π E_{y~π(·|x,θ)}[U(x,y)] s.t. C(π,x)≤B, θ fixed`——与本项目 TFRL 供给/效用/预算表述同构。显式区分三资源轴：TTS(compute) / test-time memory(KV cache/RAG/episodic) / TTT-adaptation(weights)。覆盖 MFM=MLLM+Diffusion。约 120 条参考文献；Appendix A 约 35 个基准表（生成+推理+VLA+医疗）。
- **局限**（自认，关键）：**明确排除音频**——p10:"this work exclusively focuses on vision-language modalities (i.e., images and videos) and does not cover audio or other sensory inputs"〔主执行方逐字复核命中〕；不与纯 LLM 的 TTS 做对比；承认覆盖不穷尽。
- **改进空间**：作者列 future——hybrid scaling（当前多为单策略，采样/搜索/反馈少融合）、error propagation/snowball（长链缺阻断机制）、hallucination 的 process-level 抑制（当前多是 output 级事后检查）。这些正是 selector/停止/验证的开放问题。
- **可借鉴**：三范式分类可作本项目外部控制平面「候选生成-选择-验证-搜索」的**导航骨架**；ORM vs PRM（结果奖励 vs 过程奖励）区分；benchmark 表可作选型参考。但注意许多被综述的 reward model（VisualPRM、Athena 等）是**训练出来的** PRM——落在本项目 TF-Strict（含外部组件零训练）之外，引用时须甄别。

### 身份轴事实
- **冻结核心**：综述界定 TTS=θ fixed（与本项目一致），并与 TTT（改权重）、memory（改动态状态）区分。被综述方法多为单模型冻结，但含大量**外挂 reward model / verifier / world model / 多 agent**。
- **访问级别**：综述层面不统一——涵盖从黑盒（MLLM-as-judge、majority vote）到需 logits（diffusion CFG、KL 打分）到需训练（PRM）全谱。**含越黑盒方法**。
- **信息来源**：混合——BoN/majority 多为 read-out，但 RAG（Vidorag、Dong et al.、VideoICL）、world model（MindJourney、VLA-Reasoner）、外部 reward model 均属 **new-info 注入**。
- **训练审计**：综述明确把 TTT/adaptation（改权重）划出 TTS；但 feedback-based 内**很多 PRM/ORM 是训练的**（VisualPRM、Athena、EQA-RM），非全零训练——**与本项目 TF-Strict 有冲突子集**。
- **控制机制**：三范式覆盖 sampling/selection/verification/search/refinement；memory 被划为**平行轴**（非 TTS 本体）；routing/stopping 散见于 adaptive search（动态终止）。
- **优化信号**：rule/consensus(majority)、reward(ORM/PRM)、confidence、learned evaluator、MLLM-as-judge、world-model 全覆盖。
- **任务范围**：**vision-language 多任务/生成+推理**（图像/视频生成、视频/空间/数学推理、VLA、医疗、GUI）；**显式不含 audio/speech**。
- **负结果与适用条件**：综述性讨论——sampling 增益随候选数递减；feedback 引入串行延迟依赖 verifier；search 开销最高但精度优先时最有效；长链 error snowballing 缺阻断；hallucination 事后检查不治本。

### 与本项目关系
- **重合组件**：TTS 形式化（θ fixed + 预算约束 + 效用最大化）与本项目 TFRL 供给-选择-效用框架同构；三范式=外部控制平面候选/反馈/搜索三支柱的分类骨架。
- **关键身份差异**：(1) **显式排除 audio/speech**——本项目 speech/omni 核心恰落在此「comprehensive survey」覆盖空白，是可占据的方法空位坐标〔事实陈述,非定位定性——owner 未锁创新点〕；(2) 综述含改权重/训练 PRM/logits/RAG/world-model 等**越出本项目严格黑盒 + TF-Strict + read-out-only 的子集**，非整体可采信；(3) memory 被它划为平行轴，本项目将 memory 纳入统一控制平面。
- **角色建议**：**navigation-only**——提供 taxonomy 骨架 + benchmark 地图 + 关键佐证「主流多模态 TTS 综述明确不覆盖音频」；但其数字/方法须逐条按黑盒/零训练/信息边界三判据甄别后方可入证据层，本身不作证据权重。

**批次 A 跨篇小结（事实梯度,非结论）**：四篇沿身份轴形成清晰梯度——2508.10016（黑盒文本级 + read-out，但专家联邦非单核，无 selector）→ 2512.11109（selector/验证/采样全谱实证，黑盒兼容子集丰富，但 VL-only 无 speech + confidence 变体用 logits）→ 2602.23306（logits + 外部 LRM new-info，干净落在黑盒边界外，含 audio）→ 2606.08231（导航骨架 + 明确 audio 空白）。「严格黑盒 + 单核 speech/omni + selector」交集在这四篇中无 exact-overlap。所有身份轴判断为事实差异陈述，创新点成立与否属 owner 职权。

## 批次 B（代理二:2607.09438 / 2606.28864 / 2512.19433——负结果/异质性证据类,供给侧 vs 选择侧归因精读）

〔主执行方引文抽查:6/6 逐字命中——「trained multimodal PRM beats majority vote」「the conditions under which TTS runs」「lose focus when given more compute」「without changing its weights」「logit probability of "yes"」「outperform our self-verified feedback」〕

## 2607.09438 Test-Time Scaling for Small VLMs on Multilingual Visual MCQ

### DFS 四问
- **方法**：在多语种"图中文本"选择题基准 EXAMS-V(11 语言、20 学科)上,用单 A40/A100-40GB 预算,对两个冻结策略模型(Qwen2.5-VL-7B、Qwen3.5-4B)系统比较三大方法族:(1) 采样-共识族(flat self-consistency,N=8/16,多数投票);(2) 结构化搜索族(describe-then-reason + PRM 引导的 beam-annealing 搜索 PRM-BAS);(3) 后置选择器族(多数投票 / 训练-free 生成式 critic / 单独训练的判别式 PRM Qwen-VL-PRM-7B,均带 skip-on-high-agreement 规则)。另加两轴 scaling(链数 vs 每链 token 预算)、温度扫描、guided-parse-repair(vLLM `guided_choice` 对 {A–E} 强制提交答案)。核心论点:"What matters is the conditions under which TTS runs, not the search or verification machinery"(p.1)。
- **局限**:作者自认(p.8)——只用同族两个 Qwen 模型;parseability 效应依赖具体 prompt 格式;昂贵消融跑在 dev-200(±7pp Wilson CI);PRM null 疑为结构性(reasoning 步 P(+)≈0.85 聚合后无信号);未做微调/few-shot。观察:任务纯粹是 MCQ(可验证答案字母),对开放式/生成式任务外推性未知。
- **改进空间**:选择器 null 被归因到"分母太小"(skip 规则后只有 26% 弱一致题被重打分),但没有正面测多语种良好校准 PRM 能否破 null;perception-vs-reasoning 归因用"学科"当视觉复杂度弱代理;decouple 感知与推理的假设未实现。
- **可借鉴**:(1) **归因方法论**——把 CoT→SC 的增益拆成"截断吸收(parse-fail 修复)"vs"多样性收益"(p.4),证明所谓 reasoning 增益其实来自输出可解析性——正是本项目"供给侧 vs 选择侧"拆分模板。(2) **等成本对齐**:PRM-BAS vs flat SC 同题集比,8.7× 成本换 −0.39pp。(3) **chain-agreement 分层审计**(App A):按投票一致度分层看每层准确率与选择器可改进空间——可直接搬为 K 池 headroom 分层诊断。(4) 负结果转 Stage-1B 维度:"rollout 高度相关(unanimous 但错)时多数投票放大共同错误"(Chinese −2.8pp,22.3% 8/8 一致)——须测 **rollout 误差独立性** 作为 headroom 前置条件。

### 身份轴事实
- **冻结核心**:不改权重(纯 TTS)。推理核心单个冻结 VLM,但选择阶段引入**第二个单独训练的模型**:"A discriminative PRM (Qwen-VL-PRM-7B ...), a separately trained model, scores each chain"(p.3)。
- **访问级别**:白盒本地推理(vLLM),**用 logits/log-prob**——多数投票"with log-probability tie-breaking";并用约束解码 guided_choice(p.3)。**越出严格黑盒**。
- **信息来源**:主要核心自身 read-out;判别式 PRM 是外部训练模型的打分注入。test-item gold 未进任何路径(真值仅事后度量)。
- **训练审计**:混合——生成式 critic training-free;判别式 PRM 是 "separately trained model"。一个 training-free 选择器+一个 trained 选择器并列比较。
- **控制机制**:sampling(SC)/search(PRM-BAS)/selection(majority/critic/PRM)/parse-repair(guided decoding)。
- **优化信号**:consensus(多数投票,**胜**)/confidence(log-prob tie-break)/learned evaluator(trained PRM,null 到负)/生成式 critic(self-recognition bias 污染,null)。"neither a training-free generative critic nor a trained multimodal PRM beats majority vote"(p.1,逐字复核命中)。
- **任务范围**:视觉-文本 MCQ,4B/7B,**不含 speech/audio**。
- **负结果与适用条件(供给侧 vs 选择侧,逐条)**:①最大增益来自**可解析性**(~9% dev 链推理对却不提交答案字母;换 prompt 后 parse-fail<2%、+~6pp——"what looks like reasoning failure can be an extraction failure");②**token 预算>>链数**(1k→2k +3.7pp vs 8→16 链 +0.15pp);③结构化搜索输给平搜索(PRM-BAS −0.39pp/8.7× 成本;P(+) 饱和使 71.9% 题全 beam 收敛同一字母,熵降 89%);④选择器双池 null(Q2.5 池 critic 精确 null、PRM +0.45pp n.s.;Q3.5 池两者**转负**——池准确率越高、错误尾越小,近平衡选择器净转负);⑤**策略模型主导**(换模型 +11.4pp,"upgrading the policy dominates any inference-time strategy");⑥SC 适用边界=各链独立犯错;高度相关时放大共同错误。

### 与本项目关系
- **重合组件**:采样-选择-验证外部控制平面;training-free 选择器;reward/评分引导;供给侧 vs 选择侧归因方法;单一冻结推理核心;skip-on-confidence 预算分配。
- **关键身份差异**:(1) 视觉-文本 MCQ 非 speech/omni;(2) log-prob+guided_choice 越出严格黑盒;(3) trained PRM 组件违 TF-Strict(但其结果恰为 null,可作反例);(4) 可验证答案字母的判别式结构与我们 ASR/QA verifiable reward 同构,无生成式对应。
- **角色建议**:**component-prior**——对"选择/验证组件"的最强先验:干净 selector-null + 供给侧主导 + 等成本搜索反例,直接支撑"有头空才能证伪选择器、无头空 null 只否定供给配置"的既有纪律。

## 2606.28864 On Test-Time Scaling for Vision-Language Models

### DFS 四问
- **方法**:首个跨模型规模的 zero-shot TTS 系统研究——13 个指令微调 LVLM(Qwen2.5-VL/Qwen3-VL/InternVL-3.5/Molmo2,2B–72B)× 9 方法族 × 6 基准(MMStar/RealWorldQA/HallusionBench/WeMath/LogicVista/A-OKVQA)。9 方法:prompting 族(CoT/S-CoT/Plan-and-Solve)、采样-共识(SC)、聚合、迭代精化、模态分解(Describe-Answer/CCoT)、Prompt-Repetition。全部只加 prompt 不改权重。另有二轮答案抽取 fallback、token-budget 截断实验、注意力动力学分析、KV-cache 因果干预、LLM-as-judge 分析。
- **局限**:作者自认——"是否需要 TTS"的部署级判据未做(仅建议);注意力分析仅 CoT。观察:白盒注意力/KV 干预是**分析工具**而非可部署方法;任务全是 VQA/MCQ/Yes-No 无生成式;SC 超参未扫。
- **改进空间**:"是否需要 TTS 的路由器"只是建议;perception 退化机制未做因果消融到"哪一步开始漂移";VLM 专用法为何输给通用 CoT 未深挖。
- **可借鉴**:(1) **异质性矩阵**——同一 TTS 方法在 reasoning vs perception 基准一升一降,可迁移为按任务类型分层报增益的模板。(2) **能力先决条件**:指令遵循差的模型 TTS 全失效——冻结核心的**指令遵循能力是供给生效前提**。(3) **token-budget 截断归因**:reasoning 任务减 token 掉分、perception 任务减 token 反升。(4) 负结果转 Stage-1B:"LVLMs lose focus when given more compute than necessary"——**over-compute 失焦**立为可测维度。

### 身份轴事实
- **冻结核心**:不改权重——"without changing its weights or performing any additional training"(p.4,逐字复核命中);每实验独立单核心;TTS 回路内无第二模型(LLM-judge 仅评估)。
- **访问级别**:**可部署方法 = prompt/输出级(黑盒);诊断层用 attention/KV**("completely remove the image tokens (i.e., their Key/Value cache) from all layers",p.13)——方法层黑盒、诊断层越出黑盒。
- **信息来源**:核心自身 read-out;Describe-Answer/CCoT 的 caption/scene-graph 是同一模型自产上下文(仍 read-out)。外部模型仅评估用,不入部署回路。
- **训练审计**:**零训练任何组件**(纯 zero-shot)。
- **控制机制**:prompting/sampling+consensus/aggregation/refinement/decomposition/repetition 全族;选择=多数投票。
- **优化信号**:consensus(最稳最强)与 self-refinement(常退化)。**回路内无 learned evaluator**。
- **任务范围**:VQA/MCQ/Yes-No,2B–72B+闭源 GPT-5.2 对照,**不含 speech/audio**。
- **负结果与适用条件**:①**小而强模型受益最大**(SC 把 Qwen3-VL-2B WeMath 35%→64%;4B+CoT 超 32B baseline);②**能力先决**(指令遵循差→TTS 全失效——弱核心下 null 只否定该核心);③**perception 任务 over-compute 失焦**(TTS 常退化,300-token 截断反而更好,"extra test-time compute that enables verbosity often drives LVLMs to overthink and hallucinate");④**VLM 专用法输给通用法**;⑤**视觉信息前载**(image attention 早期峰值,>200 步丢 image-KV 几乎无影响——长链后段不再读图);⑥闭源不免疫(GPT-5.2 上 perception 退化仍在,只是较轻)。

### 与本项目关系
- **重合组件**:zero-shot training-free(严格对齐 TF-Strict);单一冻结核心;激活预训练知识;SC+多数投票;prompting 供给;解码预算杠杆;任务自适应路由思想。
- **关键身份差异**:(1) 视觉-语言非 speech/omni;(2) 可部署方法黑盒但诊断用 attention/KV;(3) 判别式无生成式;(4) 回路内无 reward/learned-selector——比本项目 reward-guided selector 更"轻",可作供给侧-only 对照。
- **角色建议**:**component-prior**——跨 13 模型的异质性先验(小核心杠杆最大/指令遵循是前提/over-compute 失焦/通用胜定制),直接支撑「合理供给下 rollout 才有意义」与供给设计问责纪律。

## 2512.19433 dMLLM-TTS: Self-Verified and Efficient Test-Time Scaling for Diffusion Multi-Modal LLMs

### DFS 四问
- **方法**:面向**文生图**扩散多模态 LLM(Lumina-DiMOO/MMaDA/Muddit,1B–8B)的首个 TTS 框架。两轴 scaling:trajectory exploration(N 初始轨迹)+ iterative refinement(每轨迹 T 步)。两创新:**Self-Verified Feedback(SVF)**——复用同一 dMLLM 的图像理解,把对齐评分框成 QA("Is this image shows {prompt}? Yes/No"),取 yes 的 logit 概率作对齐分(免外部 verifier);**Hierarchical Trajectory Search(HTS)**——coarse-to-fine 探索→剪枝→精化,O(NT)→O(N+T)。基准 GenEval,成本度量 NFE。
- **局限**:作者自认——SVF 弱于强外部 verifier("current dMLLMs still have considerable room to improve in visual comprehension");refinement 步数经验定 64;单基准。观察:SVF 分数校准/自评偏差无细粒度审计;超参经验设定。
- **改进空间**:self-recognition bias 未量化;中间高噪阶段 SVF "less meaningful" 只做定性;外部 verifier 差距未反哺 SVF 改进。
- **可借鉴**:(1) **自验证=内生 reward 模板**——Yes/No QA + yes-logit 作 label-free 打分,是 label-free proxy S 的具体实现范式(但依赖 logit)。(2) **compute 自适应再分配**:HTS 中间 SVF 分早剪枝,5–6× 提速且更高分——"效率增益(算力分配)"与"质量增益(探索+精化)"分离归因。(3) 负结果转 Stage-1B:**自验证天花板 = 核心自身理解力**(SVF<GPT-4o)——「selector 强度 ≤ 核心理解强度」须登记为供给约束。

### 身份轴事实
- **冻结核心**:不改权重、无额外训练;**真·单核心**——同一 dMLLM 兼任生成与验证(与本项目单一冻结核心高度一致)。
- **访问级别**:**用 logits**——"leverages the logit probability of 'yes' as the text-image alignment score"(p.5,逐字复核命中);另操作扩散 mask/KV(架构内在)。**越出严格黑盒**。
- **信息来源**:核心自身理解 read-out(self-verification);外部 verifier(GPT-4o/VILA-Judge/CLIP)仅对照分支。gold 未入回路。
- **训练审计**:**零训练**(SVF 复用内生理解,HTS 是搜索算法)。
- **控制机制**:sampling(exploration)/search(分层剪枝)/verification(SVF)/refinement 四类整合对比。
- **优化信号**:confidence/self-evaluation(yes-logit,主)vs learned evaluator(外部,对照)。**SVF 弱于 GPT-4o**(0.92 vs 0.95 / 0.66 vs 0.71 / 0.67 vs 0.74)。
- **任务范围**:**文生图生成**,扩散 MLLM 1B–8B,**不含 speech/audio**。
- **负结果与适用条件**:①self-verification 有效但**封顶**("external verifiers, particularly ... GPT-4o, outperform our self-verified feedback",逐字复核命中——天花板=核心自身理解力);②效率增益来自搜索算法的 compute 再分配(供给侧),非单纯选择器;③质量增益与基线**负相关**(弱模型提升最大 +20.2%/+16.8% vs 强模型 +8.8%——与 2606.28864 呼应);④中间高噪阶段自评失效(信号须延后到结构显现)。

### 与本项目关系
- **重合组件**:自验证反馈(self-verification 作 selector/reward)、候选探索-剪枝-选择-精化控制平面、training-free、**单一冻结核心兼任生成与验证**、compute 自适应分配、label-free 对齐打分。
- **关键身份差异**:(1) 文生图生成任务,reward=文-图对齐,与我们 U(ASR=−WER/QA=EM) 判别结构不同;(2) yes-logit 越出严格黑盒;(3) 扩散架构非自回归 speech/omni;(4) 无 speech/audio。
- **角色建议**:**component-prior**(兼 boundary-comparator 性质:self vs external verifier 强度边界)——对"自验证/选择器"与"预算-搜索"组件的直接先验。

---

## 全七篇跨批小结（事实,非结论;创新点定性属 owner 职权,尚未锁定）

1. **供给侧主导的一致证据**（三篇负结果类独立收敛）：可解析性/单链 token 预算/策略模型本身
   (2607.09438)、指令遵循能力+任务类型 (2606.28864)、compute 分配算法 (2512.19433)——TTS
   增益大头在供给侧 c,不在复杂 selector。与我们 headroom 归因纪律（供给条件量、无头空 null
   只否定供给配置）直接互证。
2. **选择/验证侧的边界证据**：trained PRM 与 training-free critic 均不敌多数投票 (2607.09438);
   self-refinement 弱模型退化 (2606.28864/2512.11109);self-verification 封顶于核心理解力
   (2512.19433);外部 verifier > 内部 confidence (2512.11109)。MBR/majority 等 K 强制基线的
   既有纪律被七篇反复支持。
3. **身份轴普查**：七篇中**零篇**同时满足「严格黑盒 + 单一冻结核心 + speech/omni + 候选选择」
   ——各差至少一轴（联邦非单核/logits/无 selector/无 audio/生成域/外部模型 new-info）;
   2606.08231 综述明文排除 audio。此为事实普查结果,占位与空位的定位裁决留待 owner。
4. **Stage-1B 探索维度登记**（负结果转化）：rollout 误差独立性作 headroom 前置条件;
   over-compute 失焦;指令遵循能力作供给生效前提;selector 强度≤核心理解强度;可解析性
   修复先于一切 selector 比较。
