---
title: "Research Proposal（完整版 v3，供 reviewers 审阅）：Omni Agentic System 的前端多模态知识体系——以业务效果为裁判的检索·发现·使用（RDU）"
date: 2026-07-12
stage: "1-problem-definition → 申请进入 Stage-2 预注册"
status: "DRAFT-FULL v3.1（续18 单一接口契约清扫完成）— 未签署、签署前零实验；本版为供 reviewers 审阅的完整展开，supersedes v2.1 作为 review copy，v2.1 仍作为决策骨架（decision skeleton）保留"
supersedes: 2026-07-12-research-proposal-omni-agentic-frontend-v2.md
decision_skeleton: 2026-07-12-research-proposal-omni-agentic-frontend-v2.md
verdict_vocabulary: "六级状态制（ACKNOWLEDGED→DECIDED→TICKETED→IMPLEMENTED→VERIFIED→PUBLISHED）；证据引用一律带 claim-ledger ID（docs/claim_ledger.yaml + survey HB-*）；status: valid|directional 者方可引，directional 一律标 Stage-1 假设级；无 ledger ID 的数字 = unverified"
panel_response: "v1 敌对评审团 5 FUNDAMENTAL + 12 MAJOR 全部处置（§12 映射表）"
appendices:
  - "附录 A → 2026-07-12-omni-hotword-biasing-survey.md（S4 热词/上下文偏置协议、测试床、传统技术存活裁定；logit_bias/GBNF 白空间臂已依续18裁定移除，调研记录原样保留于原文）"
  - "附录 B → 2026-07-12-omni-lm-rescoring-survey.md（reward 信号层：后融合/重排序认账 + 存量池离线标定实验）"
---

> **2026-07-12 第三轮 owner 裁定（以终为始）**：**取消白盒扩展层**——系统接口契约唯一：
> 音频/文本进、文本出、多次采样（黑盒）。logprob/logit_bias/GBNF 不是系统组件：logprob 留在
> ledger 作标定线记录（C-ASR-V2），发现段触发与信任标定全部改用输出侧信号（小样本自一致性、
> 验证器一致度、答案级置信引出，多采样成本如实入核算）；logit_bias/GBNF 白空间臂删除；本地
> 冻结核心只通过黑盒接口使用（接口对等性=设计属性），llama.cpp 白盒能力仅限工程诊断（#35），
> 与系统组件严格分离。本文所有『白盒扩展层』表述依此裁定作废，待 v3.1 编辑清除。


# Omni Agentic System 的前端多模态知识体系：以业务效果为裁判的检索·发现·使用（RDU）

## 0. 绑定裁定与本版定位（binding rulings & scope — v2.1 §0 为法）

**本版是完整展开的 review copy，供 reviewers 审阅；决策骨架仍为 v2.1**（`2026-07-12-research-proposal-omni-agentic-frontend-v2.md`）——两者若有出入，以 v2.1 §0 的 owner 裁定为准，本版仅作展开，不新增任何未经 owner 签署的决定。全部先验数字带 claim-ledger ID；`status: valid|directional` 者方可引，directional 一律标 **Stage-1 假设级**。

v1 的错误：把研究对象收窄到模型本体（frozen-key 纯度），并把主问题设计成"两头可发表"。owner 裁定（2026-07-12，两轮修正并入）：

1. **研究对象 = omni agentic system**——冻结 omni 为核心组件，**知识子系统与核心系统解耦、允许异构**（组件以"冻结使用 + 效果最优"选型，不背模型纯度包袱）。
2. **效果是唯一最终裁判**——主问题必须设计成去赢；系统效果不达标的后果是**回炉迭代**（预算界定），"负结果也是贡献"**禁止用于主问题**，仅保留给次级科学点 S1–S4。
3. **frozen-key sufficiency 降级为次级科学点 S1**（组件选型依据 + 激活叙事证据）。
4. **基线哲学反转**——不得要求先把核心模型调到极致再测知识系统；真实价值场景 = **把闭源 API 搭成可验证、可闭环的系统，针对性提升外挂能力（知识/记忆/技能）**。基线 = **裸核心标准用法**；long-context 塞入 / own-ASR 级联从"基线"改编入**系统复杂度阶梯**（外挂系统的最低阶形态）。
5. **闭源 API 兼容层为硬约束**——系统接口契约唯一：音频/文本进、文本出、多次采样，无 tier 划分（2026-07-12 第三轮裁定取消白盒扩展层，详见文首 banner 与 Decision-Log 续18）。logprob / logit_bias / GBNF 不是系统组件：其 Stage-1 标定记录保留于 ledger，仅供工程诊断，与系统组件严格分离。
6. **本地冻结核心 = 科学载具（可复现）**，闭源可迁移性 = 价值主张（接口最小化设计 + 跨核心迁移冒烟作证）。

v1 敌对评审团 5 FUNDAMENTAL + 12 MAJOR + 5 噪音 共 17 项处置见 §12，处置状态按**六级状态制**（ACKNOWLEDGED→DECIDED→TICKETED→IMPLEMENTED→VERIFIED→PUBLISHED）跟踪。

---

## 1. 背景与动机（Background & Motivation）

### 1.1 问题设定：冻结 omni 核心 + 可验证闭环系统的业务价值

语音 / omni 多模态 LLM 已进入"核心冻结、能力外挂"的部署形态。当下最强的 omni 核心——本地冻结检查点（Qwen3-Omni-30B，arXiv:2509.17765）或闭源 API（GPT-4o-Audio、Gemini 一类）——我方既不能改权重、也不能改结构；闭源 API 更进一步只暴露**音频/文本进、文本出、多次采样**这一单一系统接口契约，连 logprob / logit_bias / GBNF 都不保证可达（也不作为系统组件）。这不是缺陷假设，而是**部署现实**。

在这一现实下，真实业务价值**不在**把某个核心模型的裸能力刷到极致（那是模型厂的事），而在把一个既有核心（尤其闭源 API）搭成**可验证（verifiable）、可闭环（closed-loop）**的系统，针对性提升其**外挂能力**——知识（knowledge）、记忆（memory）、技能（skill）。三类补充按**粒度**区分：知识 = 通用事实、记忆 = 特定实例召回、技能 = 任务模板注册；本提案聚焦**知识子系统**，记忆 / 技能为同级外挂，暂缓。系统价值在于：无需触碰核心权重即可在知识依赖型语音任务上兑现效果，且**接口最小化设计**天然向闭源 API 迁移——本地冻结核心是**科学载具**（可复现），闭源可迁移性是**价值主张**。

### 1.2 为什么是前端知识校正，而非后端融合（owner 范围裁定）

owner 裁定（2026-07-12）：training-free 的主战场在**前端**——调整与校正输入侧的多模态知识体系；**后端**（重排序 / 验证器）不立为独立研究方向，只作为**数据集无关的标准 reward 信号供给**，令方案跨任务通用。三条理由：(1) 后融合（GER / rescoring）在强、低-WER 的冻结核心上普遍**中性到有害**——自由改写幻觉率 3–12%（Apple，arXiv:2405.15216 **[已弃用]**；**2025+ 再锚**：LIR-ASR arXiv:2509.15095，2025-09——在强核心 Whisper-large-v3（CER/WER 2.89/5.23）上去掉规则约束、令 LLM 自由改写使 CER/WER 恶化到 6.62/9.27，约 2.3× 劣化；arXiv:2501.15310，2025-01——强核心 Gemini-1.5-Pro 经 LLM 纠错后 WER 不降反升；见 §2.2），天花板低且反伤；(2) 前端注入受核心生成能力封顶但**不破坏**它，且闭源 API 原生可达（prompt 注入）；(3) 后端只保留其唯一可移植的 training-free 原语（受约束选择 + 误差去相关信号），作为**发现段触发器**与**使用段信任标定器**——换数据集不换信号定义（详见 §7 与附录 B）。

同时**反转基线哲学**（owner 第二轮修正）：不要求先把核心调到极致再测知识系统。基线 = **裸核心标准用法（bare-core standard usage）**；long-context 全塞入、own-ASR 朴素级联从"基线"改编入**系统复杂度阶梯**（外挂系统的最低阶形态）——主主张比对裸基线，阶梯主张比对**平凡知识供给**，检验"组织智慧"的净增益。

### 1.3 组织框架：检索-发现-使用（Retrieve–Discover–Use, RDU）三段

全部已验证据与未决问题以 RDU 三段透镜组织：

- **检索 Retrieve**：给定语音输入，如何在**异构键空间**中找到候选知识（键模态 × 向量模型 × 检索策略）；
- **发现 Discover**：**何时**需要知识、需**哪类**、检回候选里**哪些真相关**（触发 / 门控 + 候选内筛选；reward 信号在此作触发器）；
- **使用 Use**：知识以**何形态**进入模型、模型**采纳多少**（递送形式 + 采纳率 α + 信任校准）。

### 1.4 Stage-1 已确立的三段定律（账本 ID 溯源，全部 directional 级）

**发现段第一定律——召回律（recall over precision）**：精度门控证伪，gate−inject = **−0.134**，CI [−.23, −.05]（**C-T7** RAG-gate 探针）——冻结 omni 对干扰 passage 鲁棒，约束是**召回而非精度**，"宁可多送、不可漏送"。*诚实标注*：该探针的注入头条增益（+51.7pp）已因答案查找 / 信息边界违规判为账本 **invalid（C-T7）**，故可引用的**仅**是 gate−inject 这一去精度化对照，held as Stage-1 directional。

**发现段第二定律——纯指令有害**：真 zero-shot 指令（不给内容、只给元指令）在 MInDS-14 上 **−0.245**，CI [−.286, −.201]（**C-MINDS-V2**）——发现段必须供给**内容**，只给元指令反而破坏行为。

**使用段定律——递送主导 + 采纳固执**：结构化 card 递送 **+24.6pp**（相对 +34.6%，5/5 过 Holm；**C-MINDS-V2**）——**全项目最大已验效应**；2-turn 两轮 prompt 递送使冲突采纳翻倍（0.175→0.35，**C-MINDS-V2** 递送族的子结果，directional）。与之对偶的是**参数固执（adoption stubbornness）**：冲突时仅 **24%** 采纳外部知识（SQuAD keep-参数 0.70；该 keep-率探针**尚未编入 claim_ledger** → 按本版 verdict_vocabulary 记 unverified，签署前须补 ledger ID 或降为定性陈述）——使用段核心约束、信任校准的靶点。

**reward-infra 校准裁定（后端收编口径）**：**C-ASR-V2**——存量池离线选择器电池里，logprob@8 是**唯一**在 clean 与 snr5 两条件下 corpus-WER CI 均排除 0 的可部署选择器（clean +0.0094 [.0034,.0165]、snr5 +0.0081 [.0005,.0161]），兑现约 **24% / 42%** oracle 头空。*诚实的 Holm-16 口径*：在真实发现网格（4 选择器 × 4 个 N = 16 比较）全家族校正下**两条件均不存活**（noise1 adj p=.592、noise2 adj p=.075）；预选 logprob@8 端点仅在两次独立噪声抽样中**方向一致**——directional，非独立复现、非"可部署赢家"。"Holm family-wise survives"绝不得脱离"哪个家族"引用。（依 2026-07-12 续18 裁定，logprob 类信号已退出系统设计，本条记录保留于 ledger 作 Stage-1 标定线，仅供工程诊断，见 §7。）

## 2. 相关工作与定位（Related Work & Positioning）

### 2.1 上下文偏置（contextual biasing）：解码器访问分水岭 + 检索式注入线

**六族传统技术在 chat-API omni 下无一原样存活**，分水岭是**解码器内部访问（decoder access）——不是训练与否**（此 watershed 裁定的活体锚点 = 2025 的 trie 研究 arXiv:2508.17796 + 当代 llama.cpp 工具事实 HB-8/10，下列 pre-2025 技术行仅作谱系/已弃用支撑）：shallow fusion（在线 WFST/NNLM 重打分，需逐步 beam 分数；Zhao IS2019 **[谱系]**，HB-1）、CLAS / 深度上下文（需训练 bias-encoder attention；arXiv:1808.02480 **[谱系]**，HB-2）、trie / 前缀树约束解码（需 beam + next-token masking；arXiv:2508.17796，HB-3）、TCPGen（需端到端训练；arXiv:2109.00627 **[已弃用]**，HB-4）、contextual adapters（需训练 adapter；arXiv:2205.13660 **[已弃用]**，HB-5）、transducer/CTC beam boosting（需帧 log-prob；HB-6）。最反直觉的一条：连"免再训练"的 **CTC-WS**（arXiv:2406.07096 **[已弃用]**，NeMo）也失效——它需 CTC 帧 log-prob 在候选帧区间替换贪心结果，而 chat API 对音频编码器不暴露任何帧 logit。**残存的只有三个退化替身**：prompt 注入（退化 CLAS 后裔，经系统接口契约可达）、logit_bias（无结构静态 shallow fusion，字符串级子词袋、表面形式脆弱；llama.cpp issue #13605，HB-8）、GBNF（硬约束 trie 解码，伤开放转写；HB-10）——后两者依赖解码器内部访问特权，闭源 API 不保证，按 2026-07-12 续18 裁定已从本系统臂族移除（不再单独申报；原调研记录保留于附录 A 原文，仅供工程诊断参考，见附录 A 说明）。

**检索式注入（retrieve-then-inject）是文献收敛出的替代形态**：大偏置库 → 语音键检索小候选子集 → prompt 注入。证据在与 Qwen3-Omni **同族**基座上很强（replacement-form 论点由 2025 的 BR-ASR/RECAST/Hotword-RL/Locate-and-Focus 活体锚定，Phoneme-RAG 为 pre-2025 佐证行）：BR-ASR（Qwen-Audio，arXiv:2505.19179，HB-16）、RECAST（Phi-4 / GPT-4o-mini，EMNLP2025 findings.203，HB-23）、Phoneme-RAG（Apple，arXiv:2409.15353 **[谱系]**，HB-24）、Hotword-RL（Qwen2.5-7B，arXiv:2512.21828，HB-15）、Locate-and-Focus（Qwen2-Audio，arXiv:2507.18263，ACL2025，HB-25）。两条一致读数：(1) **top-2 甜点**——候选越多单调越差，整表塞 prompt 在 N≥100 灾难幻觉、"list-vomiting"（模型背诵列表而非转写；LOGIC，arXiv:2601.15397，HB-17）；(2) **关键约束**——所有赢家检索器都是**专门训练**的对比检索器（BR-ASR CLAP 命中 93/91%、GLCLAP 89/74%；HB-26），off-the-shelf CLAP 词汇键**已死**（R@1≈0.1，此裁定由 2025 BR-ASR/HB-26 co-anchor），唯一全 training-free 类比 M2R-Whisper（arXiv:2409.11889 **[谱系]**）的 token-kNN 段需 logit 访问（chat API 无）。**定位**：我方的差异**不在偏置机制新颖**，而在把这条被专训检索器统治的能力，做成**零训练（zero-training）、闭源 API 兼容**的系统——对外效果故事 = "零训练前端追平 / 超越需专训检索器的 pipeline"（S1 的 trained-frozen 对照臂作证）。

### 2.2 LLM 重排序 / GER：约束选择安全、自由改写陷阱 → 收编为 reward 基础设施

后融合正典由 **NTU-新加坡 ⟷ NVIDIA ⟷ IBM 的 GER 集群**主导（Yuchen Hu、Chen Chen、Eng Siong Chng、Chao-Han Huck Yang、Pin-Yu Chen；HyPoradise NeurIPS2023 arXiv:2309.15701 **[已弃用]**、RobustGER ICLR2024 arXiv:2401.10446 **[已弃用]**、ClozeGER ACL2024 arXiv:2405.10025 **[谱系]**、GenSEC SLT2024 arXiv:2409.09785 **[已弃用]**），**剑桥 CUED**（Ma / Gales / Knill）持 training-free 冻结分析线。对我方最 load-bearing 的裁定是**约束选择安全、自由改写陷阱**：N-best 受约束 closest-mapping（冻结 ChatGPT，1-shot 6.24 vs baseline 6.90、oracle 4.59；剑桥 arXiv:2307.04172 **[谱系]**；**2025+ 再锚**：SEAL arXiv:2501.08421，2025-01——"a simpler constrained decoding strategy reduces LLM hallucinations"，把受约束解码立为安全可部署原语；LIR-ASR arXiv:2509.15095，2025-09——去掉约束令误差近乎翻倍，即约束=安全的反证）受 oracle 硬封顶、永不幻觉、training-free 可用；而自由改写 GER 在强低-WER 基线上**灾难劣化**（Apple，arXiv:2405.15216 **[已弃用]**：LibriSpeech 2.2/5.3 → Llama-70B 0-shot 8.8/13.0，幻觉率 3–12%；**2025+ 再锚**同上 LIR-ASR / arXiv:2501.15310），GER 的 −40~−77% 大数**全是 fine-tuned**（HyPoradise 系）。因此 owner 将后端**收编为 reward 基础设施**——只保留受约束选择 / 误差去相关信号，不立后融合研究线；**δ_corr 引 ROVER（Fiscus 1997 **[谱系]**）"互补错误"谱系作借用基础设施**（28 年前的正典祖先），从本提案定理约束清单中移除，**不作理论贡献主张**（panel R4-MAJOR-5 修复；见 §7、§8）。**认账**：omni 自池 training-free 二遍解码本身确是空白（正典 N-best 源皆经典 ASR、纠错器皆独立文本 LLM），但我方**不以此空白立方向**——只把 logprob@8 端点当作 reward 信号的跨域标定（**C-ASR-V2**，directional）。

> **⚠ 新鲜度审计发现（TOPIC 2，ANCHORED-WITH-REVISION，待 owner 复核）**：「约束选择安全 / 自由改写陷阱」的**大原理**已被 2025 一手证据双向再锚（SEAL 2501.08421 立约束=安全、LIR-ASR 2509.15095 反证去约束翻倍误差），但**没有任何 2025 一手研究直接跑「受约束 N-best 选择/closest-mapping 完胜自由改写」的正面 head-to-head**——那条最贴合的直接证据仍停在 2023–2024（剑桥 2307.04172 / 2409.09554、Amazon TAP 2309.15649）。且剑桥 2409.09554（2024）发现：当 LLM 足够强（GPT-4）时，**无约束**解码在部分集上可**超过 N-best oracle**。故「一律约束」并非普适，而是**依模型能力 / 依 regime**——约束选择的安全优势在 ASR 核心已强、头空小、幻觉风险高（即 W4 的 regime）时最大。建议在本节与 §7 把该原语的适用性显式写为 **regime-conditional，而非普适**，勿把它当作跨能力恒真的结论。

### 2.3 主动检索（active retrieval）：FLARE / Self-RAG 谱系与 S3 的迁移问题

发现段的**两遍触发管线**（S3：第一遍生成取不确定度 → 决定检索 → 第二遍生成）**不是新方法**，其谱系是文本 LLM 的**主动 / 自适应 RAG**——**FLARE**（Jiang et al. 2023，arXiv:2305.06983 **[谱系]**，按生成置信度触发检索）与 **Self-RAG**（Asai et al. 2023，arXiv:2310.11511 **[谱系]**，自反思式按需检索）。两份偏置 / 重排调研均未覆盖此线，v1 提案亦漏引（panel R4-MAJOR-4 修复）。我方定位 S3 = **"主动检索能否迁移到冻结 omni"**（does active-retrieval transfer to frozen omni），非机制新颖；判定用**双门**（增益差 TOST + 调用降幅 ≥30% superiority，两门皆须过），且**在 mock 口径之外**作独立两遍管线运行——不违反 harness 的 `assert_no_adaptive_logic` 不变量（panel R3-FUND 修复）。

### 2.4 语音 / 多模态 RAG 语境（step2a 已验主张）

补足检索键模态谱与再听前沿：**音频键 / 跨模态检索是最佳拟合**（BR-ASR AcousticBias、VQ-RAG、GLCLAP、M2R-Whisper、Locate-and-Focus），避开"转写-bootstrap 失效"；但 BR-ASR 自身的赢家实为**文本键（TextualBias，更 OOV-鲁棒、更少同音命中）**——这一**分化答案恰恰不利于"omni 嵌入激活"的旗舰叙事**，故 H1（audio-direct vs own-ASR 级联）在文献里**已被差异化回答**，我方按**"training-free 约束下的确认性复现"而非发现**来定位（panel R4-MAJOR-3 修复）。**再听（re-listening）**是当前前沿（ClozeGER arXiv:2405.10025 **[谱系]** / AVGER arXiv:2501.04038——"Listening and Seeing Again"，2025-01，audio-visual GER 用 Q-former 多模态同步编码器把源信号喂回纠错器、LRS3 相对 WER −24%——把源音频喂回纠错器），Qwen3-Omni 天然可再听——但令 reward 音频接地，**Information-Boundary Guard 适用**（验证器不得见 golden 转写）。

> **⚠ 新鲜度审计发现（TOPIC 4，ANCHORED-带模态注记，待 owner 复核）**：AVGER（arXiv:2501.04038）已给「再听 > 纯文本纠错」一个可引的 2025 一手 ID（+24% 相对 WER），但它是 **audio-VISUAL**；同期唯一另一份 2025 再听一手 SEAL（2501.08421）走的是 **speaker-error** 轴（24–43% SER↓）。**纯音频（无视觉）再听、直接针对 WER 的 head-to-head 仍主要靠 2024 的 ClozeGER 锚定**。若本提案在 §7 主张「再听是 WER reward 层的最强杠杆」，须显式标注：该「音频-only-for-WER」切片的 2025 一手证据偏薄，最贴合的新鲜证据是邻模态（视听 / 说话人轴）。**同音 / 近音干扰污染**是音频相似检索的 #1 已证失效（BR-ASR DCL、RECAST 硬负挖掘；HB-21）——任何 retrieve-then-bias selector 须含**显式 precision / 去相关项**，正是理论轨要求的"界定问题边缘的显式约束"。

### 2.5 定位总述：零训练 omni agentic 系统的效果主张

一句话：**我方不主张任一段的机制新颖，而主张在一个零训练、闭源 API 兼容的 omni agentic 系统上，把 RDU 三段精心组织后取得业务效果**——对裸核心标准用法基线 ≥10% 相对、全家族校正后可靠、边界清白，并在系统复杂度阶梯上相对平凡知识供给（long-context 塞入、own-ASR 朴素级联）有可靠净增益。与每条先行工作的关系：偏置线（§2.1）——我方**零训练** vs 其**专训检索器**；后融合线（§2.2）——**收编为 reward 基础设施**，非方向；主动检索（§2.3）——**迁移问题**，非新方法；语音 RAG（§2.4）——**键模态答案已分化**，H1 为确认性复现。**效果是唯一最终裁判**（owner 裁定）：clean positive 不再是 v1 那种"5 队已复现"的必然结论，因为主张的对象是**系统级零训练效果**（而非任一机制），且成败以业务效果、而非"负结果也是贡献"的自我安慰来判定（后者仅保留给次级科学点 S1–S4）。

### 2.6 引用新鲜度合规声明（Citation-Freshness Compliance）

> **编号说明**：本小节按 owner 指令名为「§2.5 引用新鲜度合规声明」，因 §2.5 号位已被「定位总述」占用，实际落位 **§2.6**（仅编号顺延，内容即指令所指的合规声明）。

**规则（Decision-Log 续17，2026-07-12 owner 裁定）**：每条**方向影响型主张**（方法有效性裁决、替代形态论证、效应量先验、测试床选型理由）必须由 **≥1 篇 ≥2025-01 的一手来源**锚定。较早著作**仅在带显式角色标签**时允许：**[谱系]** = 历史谱系、**[标准]** = 方法学/统计标准（不过期）、**[已弃用]** = 引用以宣告其死亡/被证伪。本提案的调研附录（附录 A/B）**作为有日期的历史记录原样保留**；本合规工作只改**本 FULL 提案**内的引用，并在两份 survey 顶部各加一条「哪些方向主张已在本 FULL 中再锚」的日期注记。

**审计口径与结果（63 条 audit 项）**：

| 判定 | 计数 | 处置 |
|---|---|---|
| COMPLIANT（已有 ≥2025 一手 / 当代工具事实，使用正确） | **18** | 无需改动 |
| NEEDS-ROLE-TAG（pre-2025，仅缺角色标签） | **36** | 于 FULL 内出现处加 [谱系]/[标准]/[已弃用] |
| NEEDS-REANCHOR（作活体效应量先验但无 ≥2025 co-anchor） | **3** | 加 ≥2025 一手再锚 + 旧源保留带标签 |
| NEEDS-DATE-CHECK（日期/ID 待确认） | **6** | 4 条已由 ≥2025 一手落定，2 条 survey-scoped 待复核 |

**NEEDS-REANCHOR 三条的落定（锚点猎取全部命中 ≥2025 一手）**：
- Apple frozen-GER 负结果 arXiv:2405.15216（§1.2/§2.2）→ 再锚 LIR-ASR **arXiv:2509.15095**（2025-09）+ **arXiv:2501.15310**（2025-01），旧源标 **[已弃用]**。
- 剑桥受约束 closest-mapping arXiv:2307.04172（§2.2）→ 再锚 SEAL **arXiv:2501.08421**（2025-01）+ LIR-ASR 2509.15095，旧源标 **[谱系]**（**带修正**，见下 ⚠）。
- Amazon TAP arXiv:2309.15649 → **仅存于附录 B（RESCORING §3/§4），不在本 FULL 正文**，此处不改；同题再锚（SEAL/LIR-ASR）已适用，留待 survey 顶注记。

**NEEDS-DATE-CHECK 六条**：4 条以 ≥2025 一手落定并写入 FULL——AVGER **arXiv:2501.04038**（2025-01，§2.4）、GLAP **arXiv:2506.11350**（2025-06，§4.3）、omni-embed-nemotron **arXiv:2510.03458**（2025-10，§4.3）、LCO-Omni **arXiv:2510.11693**（2025-10）+ MAEB **arXiv:2602.16008**（2026-02，§4.3）。**2 条 survey-scoped 未决**（只在附录 A、不在 FULL）：SLLM 列表规模研究 arXiv:2604.12398（ID 形态异常，需确认非转写错）、base-model reports HB-33（Qwen2-Audio 部分 pre-2025、报告 PDF 转换失败未穷尽确认），二者随 survey 顶注记留作后续核验。

**⚠ 触发的方向修正标记（3 处，均已就地加 ⚠ 注，待 owner 复核；本合规工作不擅自改方向）**：
1. **§2.2（TOPIC 2，ANCHORED-WITH-REVISION）**——「约束选择安全 vs 自由改写陷阱」大原理有 2025 双向锚，但无 2025 一手跑正面 head-to-head；剑桥 2409.09554（2024）显示强 LLM（GPT-4）无约束可超 N-best oracle → 该原语适用性应写为 **regime/能力条件性，非普适**。
2. **§4.3 + §3.3 S1（GLAP/nemotron/LCO/MAEB，ANCHORED-WITH-REVISION）**——「冻结 omni-own 键充分」应改述为「最强廉价键、无音频训练达 SOTA 但 MAEB 均分仅 ~50–52%、SOTA 证据含一层轻量非音频对比精化而非纯 raw 2048d readout」。
3. **§2.4（TOPIC 4，ANCHORED-带模态注记）**——「再听是 WER reward 层最强杠杆」的 2025 一手证据为**邻模态**（AVGER 视听 / SEAL 说话人轴）；纯音频-for-WER 切片仍主要靠 2024 ClozeGER，须显式标注证据偏薄。

**旁注（TOPIC 3，ANCHORED，无需 FULL 内改向）**：外部-LM 重排序在强首遍上天花板低（~9–16% 相对）之效应量先验，现由 2026 的 arXiv:2606.23306 与 2025 的 CHSER arXiv:2505.18463 重新锚定；该论点主要承载于附录 B（RESCORING §2）的 pre-2025 谱系（Salazar/Conformer/AED），其 [标准] 标签与新锚随 survey 顶注记登记，不改本 FULL 正文。

---

## 3. 问题陈述与假设（Problem Statement & Hypotheses）

### 3.1 主问题（唯一，效果口径）

本研究把研究对象定为 **omni agentic system**——冻结 omni 为核心组件，知识子系统与核心系统解耦、允许异构。主问题逐字取自骨架 v2.1 §1（owner 2026-07-12 裁定，两轮修正并入）：

> 以冻结 Qwen3-Omni-30B 为核心（科学载具；接口按闭源 API 兼容层约束）的 omni agentic system，加装前端多模态知识子系统（检索-发现-使用三段，组件异构、全部冻结使用），能否在知识依赖型语音任务上，对**裸核心标准用法基线（bare-core baseline）**取得 **≥10% 相对（relative）**、全家族校正后统计可靠、边界清白的业务效果提升？并在**系统复杂度阶梯（sophistication ladder）**上，精心组织的 RDU 配置相对平凡知识供给（long-context 塞入、own-ASR 朴素级联）是否有可靠净增益（net gain，组织智慧的次级主张）？

这是一个**双主张（dual-claim）结构**：(a) **头号主张** = 最优 RDU 配置 vs 裸核心基线，相对 ≥10%；(b) **阶梯主张** = 最优 RDU vs 平凡供给臂（long-context 全塞入 / own-ASR 朴素级联的较优者）的可靠净增益，用以裁定「增益是否归因于 RDU 的组织智慧，而非仅仅来自任何知识供给」。

- **成功语义（win-design）**：达标 → 系统主张成立，对外效果故事 = 「零训练前端追平/超越需专训检索器的 pipeline」（trained-frozen 对照臂支撑，见 S1）。
- **失败语义**：不达标 → 进入**系统设计迭代循环**（§9 预算界定的 pivot 规则，Stage-2 内 ≤2 轮、每轮 owner 批准），耗尽迭代预算仍不达标才由 owner 决定是否转向边界性结论。**「负结果也是贡献」的表述禁止用于主问题**——主问题按去赢设计，不设「两头可发表（publishable-either-way）」的自我安慰盾牌；该表述仅保留给次级科学点 S1–S4。（本条明确不采纳 v1 敌对评审团 R4 FUND-1/2 的「把 frozen-key 升为可两头发表的 primary」建议——owner 已 overrule；但评审团对各 estimand 的**修复**全部并入，见 §12 映射。）
- **合规口径（compliance）**：组件「冻结使用（frozen-use）」= 我方不训练任何参数（零 LoRA、零投影、零 adapter）；上游预训练组件（含 trained-frozen 检索器如 GLAP / nemotron）照 **LLMLingua-2 先例**（Pan et al. 2024, arXiv:2403.12968 **[标准]**——作披露惯例而非效果论据：方法在部署侧 training-free，但如实披露其压缩器为上游训练所得）标注为「用法 training-free、非 training-free-by-construction」，不作为 by-construction 证据。若任一环节须训练一个薄投影才能达标，则如实报告为 training-free 检索的**负结果**，绝不静默替换。

### 3.2 主效果假设 H-sys（primary）

- **Estimand**：最优 RDU 配置相对基线的**相对改善百分比**（单尺度），主聚合口径 = 跨集固定效应（cross-dataset fixed effect）；DerSimonian-Laird 随机效应仅作参考（k=3–4，τ² 不可靠，panel R1-m1 处置）。
- **决策规则（decision rule，panel F1/#4/M6 修复）**：一律相对尺度单门；**per-dataset SESOI 数值表**预注册于统计节（各集基线水平 → 10% 相对换算的绝对值，取代 v1「0.05 绝对 ≈ 10–15% 相对」的跨集伪不变量）；主判定 = 相对 ≥10% 且家族校正后 CI 下界越过该集 SESOI。H-sys 家族 = 最优配置 vs 裸基线（1）+ 阶梯对比（2）= **3 项**，连同 S1–S4 与闭卷锚点共 **15 项全枚举**进 Holm/max-T（表见 §5.6），「显著」必注家族。**交互模型预注册**（panel M3/#13）：键×递送交互 CI 宽度门控主效应解读，H-sys 赢家按**格级（cell-level）**估计选择而非边际估计。cluster bootstrap（group_key；无组集如实回退）。
- **双主张裁定**：**go = H-sys-a**（vs 裸基线，相对 ≥10%，家族校正 CI 下界越 SESOI）于确证层达标；**H-sys-b（阶梯净增益）单独裁定**——若最优 RDU 对两条平凡供给臂的净增益家族校正 CI 下界均 >0 → 「组织智慧」叙事挣得；若仅 H-sys-a 达标而阶梯净增益为 null → 系统有效但增益归因于「知识供给本身」而非 RDU 组织，如实降级叙事，**不 kill H-sys-a**。闭卷锚点改为 **within-item 配对对比**（同一音频，KB 供给 vs 保留，panel M9/#9 修复），作为家族第 15 项。
- **确证层裁决（confirmatory-layer adjudication）**：判定于确证层、**custodian 单通道单次消费、读取即 burn**；**探索层不触发任何 kill**（panel M2/#12），探索层输出仅为配置排序 + Phase-B 协议草案。

### 3.3 四个次级科学点（S1–S4）

- **S1（frozen-key sufficiency，降级后的 v1 主问题）**。**动机**：冻结 omni 自身 2048d 隐态音频嵌入能否作为**零训练投影的检索键**（v1 旗舰内核，现降为次级）+ 组件选型依据 + 「激活」叙事证据。**Estimand**：omni-own 键 vs 专化冻结键 vs trained-frozen（nemotron）的检索质量（squtr 原生 R@k / nDCG）与端到端贡献。**家族**：3 键空间两两 = **3 项**。**反馈系统设计**：决定检索段键空间选型——若 omni-own 不足，系统换更强冻结组件继续，负结果仅记为 S1 边界，**不阻塞 H-sys**；预注册承诺——若须训练投影，报告为 training-free 的负结果（回应 panel FUND-2，且诚实对待 HB-26「off-the-shelf CLAP 词汇键已死 R@1≈0.1，赢家检索器多 purpose-trained」的激进赌注）。**⚠ 新鲜度审计（见 §4.3 ⚠ 注 + §2.6）**：一手 LCO-Embedding（2510.11693）/ MAEB（2602.16008）强制把「冻结 omni-own 键充分」改述为「最强廉价键、无音频训练达 SOTA 但 MAEB 均分仅 ~50–52%、且 SOTA 证据含一层轻量非音频对比精化而非纯 raw readout」——S1 的「纯零适配 2048d readout 即足」措辞据此收紧，待 owner 复核。
- **S2（递送主效应）**。**动机**：递送形式是全项目最大已验杠杆（结构化 card 递送相对 +34.6%，5/5 过 Holm，**C-MINDS-V2**，directional）。**Estimand（panel F2/#5 修复，取代 v1「≥ 任意维度」的病态定义）**：单一预注册对比 = 递送主效应（card + 两轮 prompt 递送合并最优 vs flat）− 键模态主效应，**联合 CI**。**家族**：**1 项**。**反馈系统设计**：裁定使用段「组织」与检索段「键选择」谁承载更多效应，锁定递送形式。（「两轮 prompt 递送」= 预制两轮消息在**单次**生成调用内递送，非模型发起的工具往返，panel R3-MINOR 更名处置。）
- **S3（发现段·两遍管线）**。**动机**：何时检索——全项目证据最薄段；定位 = active-retrieval（**FLARE**, Jiang et al. 2023, arXiv:2305.06983 **[谱系]** / **Self-RAG**, Asai et al. 2023, arXiv:2310.11511 **[谱系]**）向冻结 omni 的迁移。**Estimand + 出 mock 口径（panel F3-R3/#2 修复）**：触发式检索作为**独立 two-pass pipeline**（第一遍生成→取生成不确定度→决定检索→第二遍生成），在 mock 口径**之外**运行，不违反 `assert_no_adaptive_logic` 不变量。**双门判定（dual-gate，panel M4/#14 修复）**：增益差 **TOST**（margin 预注册，触发 vs 恒检索等增益）+ 调用降幅 **≥30% superiority** 检验，**两门皆须过**。**家族**：**2 项**。**反馈系统设计**：裁定触发式检索是否值一次额外生成遍（发现段配「触发」还是「恒检索」）；第一遍不确定度信号取**输出侧 m=3 采样自一致性一致率**（sampled self-consistency agreement rate），不再使用 logprob 阈值——logprob 类信号已退出系统设计，仅留 ledger 作工程诊断（见 §4.2、§7、续18）。
- **S4（实体粒度实例；热词/上下文偏置）**。**动机**：热词偏置 = RDU 三段在实体粒度的具象（H5），retrieve-then-inject 被 ≥5 篇同族基座论文强证据支持为替代形态（附录 A §4）。**Estimand + 反答案注入（panel F3/#3 修复，规避 C-M3/C-T7 的 answer-injection 失效类）**：可部署列表 = **eval 前冻结的热词库经音频键检索的产出（outcome）**；「真词保证入列」的列表**降为 oracle 上界臂，永久标注不可部署**；B-WER 主指标（相对 ≥15% 靶，比 H-sys 更严）**以检索产出为条件**计算，真词命中如实记录、绝不保证。**H5a 单独报告**：检索召回 + **同音精度（homophone precision）**——BR-ASR RecallH / DCL 类比（HB-21），界定同音误注入率，作为收敛论证要求的显式 precision/去相关项。**家族**：列表长度扫描 {2,5,10,50}（4）+ 主对比（1）= **5 项**。测试床 = is21_deep_bias / AISHELL-NER / SLURP（附录 A 协议）。**反馈系统设计**：偏置列表由检索产出，oracle 臂降级；若三段管线不显著优于 full-list-stuffing → 检索式注入假设在实体粒度证伪，如实报负。

## 4. 系统架构（System Architecture）

### 4.1 RDU 三段管线（检索-发现-使用）

```
语音输入 audio-in
  └─▶ [发现 Discover：何时/需何类知识 — 两遍管线（S3），出 mock 口径]
        └─▶ [检索 Retrieve：异构键空间（S1 对比后选型）× 检索策略]
              └─▶ [使用 Use：递送形式（card / 两轮 prompt / flat）+ 信任标定]
                    └─▶ 冻结 omni 核心生成 core generation ─▶ 业务效果 business effect
```

三段各自映射到既有账本机器：**检索段** = 键组织 × 向量模型 × 检索策略；**发现段** = 触发/门控（第一定律「宁可多送、不可漏送」——精度门控已证伪 C-T7 gate−inject=−0.134；纯指令无内容有害 MInDS −0.245，C-MINDS-V2）；**使用段** = 递送形式 + 采纳率 α（参数固执，冲突时仅约 24% 采纳外部知识——信任标定靶点）。

### 4.2 系统接口契约（硬约束）

**系统接口契约（唯一，无 tier 划分）**——只用任何闭源 API 都保证暴露的接口：**音频/文本输入、文本输出、多次采样（multi-sampling）**。发现段触发用**输出侧信号（output-side signals）**：采样自一致性（m=3）、验证器一致度、答案级置信引出（re-prompt 引出）。这是可迁移到任意闭源 API 的部署口径（2026-07-12 第三轮裁定取消白盒扩展层，见文首 banner）。

logprob 触发、`logit_bias` 加性偏置、GBNF 语法硬约束**不是系统组件**：三者均依赖本地核心的解码器内部访问，闭源 API 不保证可达，按续18 裁定已从系统臂族移除。我方唯一已验的相关信号 logprob@8（**C-ASR-V2**，directional：clean 5.79→4.86 corpus-WER，sig）依赖逐 token logprob，其 Stage-1 标定记录保留于 ledger，仅供工程诊断（llama.cpp 白盒能力，#35），与系统组件严格分离，不作发现段触发信号使用——发现段触发一律改用上述输出侧信号。`logit_bias`/GBNF 两臂已删除，不再作 H5 的 15% 载重（原探索记录见附录 A 说明；纯 logit_bias 类比 LOGIC 曾仅兑现约 9% 相对，恰在门槛下，此数字随臂删除一并归档为历史参考）。

### 4.3 知识子系统候选组件（全冻结使用）

选型由 **dev 效果决定并如实报告**——系统不押注任一组件。

| 组件 | 角色 | 键/来源 | 冻结使用标注 | 依据 |
|---|---|---|---|---|
| **qwen3-omni-own** | 键=查询嵌入（旗舰） | 2048d 隐态音频嵌入（H-b 解锁，**活体已验**） | 我方零训练/零投影；核心为上游预训练，按 LLMLingua-2 先例（arXiv:2403.12968 **[标准]**）标注（用法 training-free，非 by-construction） | RDU §1；**冻结-omni-own 键作可检索性主张的一手锚**：LCO-Embedding arXiv:2510.11693（2025-10，NeurIPS2025，冻结 Qwen2.5-Omni 级 MLLM 无音频训练即 MAEB #1）+ MAEB arXiv:2602.16008（2026-02） |
| **GLAP** | 音频-文本对比检索键 | R@1≈93.8/98.5 | **trained-frozen**：purpose-trained 上游对比检索器，冻结使用，非 training-free-by-construction | GLAP arXiv:2506.11350（2025-06，>93% EN / ~98% ZH 语音内容检索 R@1，多语种键 CLAP 无法胜任）；附录 A §4；speech2vec facts **[谱系]** |
| **omni-embed-nemotron** | **trained-frozen 对照臂** | asymmetric `encode_document`；NC license | 冻结使用对照，仅作 S1 天花板对照；NC 许可仅研究用 | Omni-Embed-Nemotron arXiv:2510.03458（2025-10，NVIDIA 基于 Qwen2.5-Omni Thinker 的 4.7B 双编码器，NVIDIA OneWay NC 许可）；speech2vec facts **[谱系]** |
| **专化侧翼** | 实体粒度检索器 | 实体/语音学键 | 冻结使用；中文语音学算法不迁移（RECAST Hindi 论证），中文用学习跨模态检索器 | 附录 A §4（HB-24 = Phoneme-RAG arXiv:2409.15353 **[谱系]**；replacement-form 由 2025 BR-ASR/RECAST/Locate co-anchor） |
| **own-ASR→文本级联** | 无音频键的键模态对照 | own-ASR 转写→文本检索 | 边界清白（转写部署可得，非泄漏）；**cascade ASR WER 作 covariate 报告**（panel R2-MINOR） | 附录 B §5 |

> **⚠ 新鲜度审计发现（GLAP/nemotron/LCO-Omni/MAEB，ANCHORED-WITH-REVISION，待 owner 复核）**：组件选型先验（GLAP=多语种语音键 / nemotron=NC-许可天花板 / 冻结 omni 自身状态可检索）现已全部由 2025+ 一手锚定（GLAP 2506.11350、Nemotron 2510.03458、LCO-Embedding 2510.11693、MAEB 2602.16008），内部 speech2vec 记忆笔记被**证实而非反驳**。但一手证据强制一处修正，须回传 S1（§3.3）框架：**旗舰赌注「冻结 omni 自身 2048d 嵌入是充分的 training-free 检索键」应改述为「是最强的廉价键，达到无音频训练的 SOTA，但 MAEB 均分仅约 50–52%（远未饱和），且该 SOTA 证据用了一层轻量非音频对比精化 + 投影，并非纯零适配的 raw 2048d readout」**。两个小数级事实（CLAP 基线近零 R@1；nemotron 精确 encode_query/encode_document API）因本次抓取受限仍属记忆笔记级，若需硬核验请另标。此 ~50–52% 头空正是「training-free RL 值得一搏」的现实效应量先验。

`content_hash` 扩展至**嵌入器 SHA + revision + 量化 + 归一化配置 + 索引参数/top-k**，并断言**键==查询嵌入器 fail-closed**（panel M8/#8 修复，堵 C-PHASEA P0-4 的静默换空间 bug；详见 §6.2）。

### 4.4 科学载具 vs 可迁移性主张

**本地冻结核心 = 科学载具（science vehicle）**：Qwen3-Omni-30B Q8_0 GGUF via llama.cpp（`-ngl 28`，resident `llama-server`），数据/代码/种子全 pin，**确证层结果在此复现**（可复现性由此保证；owner 修正⑥）。

**闭源可迁移性 = 价值主张（portability claim）**：真实价值场景 = 把闭源 API 搭成可验证、可闭环的系统。兑现 = **接口最小化设计**（§4.2 系统接口契约只用音频/文本进、文本出、多采样）+ **跨核心迁移冒烟（cross-core smoke）**——同一系统接口契约配置在第二核心上 1–2 集轻验作可迁移性证据（候选：MERaLiON-2 或一个闭源 API，时间线 Week-3）。二者分工明确：科学结论落在冻结本地核心（严格可复现），可迁移性作为价值证据由跨核心冒烟支撑，**不以单核心成立冒称通用**。

---

## 5. 实验设计与统计分析计划（Experimental Design & Statistical Analysis Plan）

本节将 §1 的效果口径主问题与 §3 的一主四次假设结构落到可预注册、可审计的执行层。所有引用的先验数字均标注 claim ID（`docs/claim_ledger.yaml` / 两份 survey 的 HB-* 账本），仅 `status: valid|directional` 者可引，且 directional 一律标 Stage-1 假设级。

### 5.1 数据集、主场与 per-dataset 基线（覆盖纪律：多集轻采样 dev n≈40–80）

主场三集 = **squtr（corpus 侧重建后）/ heysquad / SQuAD-zh**；**闭卷锚点** vocalbench-knowledge（§5.6 within-item 配对，非独立 lift 靶，修复 panel #9）；**S4 实体测试床** = is21_deep_bias（英文正典）/ AISHELL-NER（中文正典）/ SLURP（检索原生 SLU）。全部音频已在盘（E: 盘 `SPEECHRL_DATA_DIR`）。下表的 dev 基线来自已冻结的 locked-group 工件（`_repro/baselines/*__qwen3-omni-30b-gguf__dev.locked.json`，seed 20260705，Q8_0 GGUF，`-ngl 28`；**C-BASELINES：directional**，Stage-1，勿当独立 held-out）：

| 数据集（角色） | dev 基线 mean (n) [ci95] | 度量 (K 型) | 头空判读 |
|---|---|---|---|
| **heysquad**（主场，主发力集） | **0.225** (40) [0.10, 0.35] | span/QA acc (K8) | 头空最大；C-T7 提醒此为 SQuAD 式抽取 QA，注入正确 passage 会退化为"抄答案"——deployable 臂必须以检索产出为条件（§6.1）。 |
| **SQuAD-zh**（uro-bench，主场） | **0.925** (40) [0.825, 1.00] | QA acc (K8) | 近饱和；见 §5.6 SESOI 说明——10% 相对当量超天花板，不可达；仅作近饱和负头空检查，受 §9 oracle-headroom 退场规则约束。 |
| **squtr（corpus 侧）**（主场，检索原生） | **待定**（K9，corpus 重建后 1 真格打样；C-PHASEA invalid 的对象修复前不可打分） | 检索-QA (K9) | 唯一检索原生主场；SESOI 待首个合法真格后回填。 |
| vocalbench-knowledge（闭卷锚点） | 0.8875 (80) [0.8125, 0.95] | QA acc (K8) | 近饱和；锚点=within-item（KB-供 − KB-留同题配对差），不做独立 10% 判定。 |
| SLURP-intent（S4 邻） | 0.6452 (62) [0.516, 0.758] | intent acc (K6) | 中等头空，可支撑相对判定。 |
| SLURP-slot（S4） | 待定（K7，未打分） | SLU-F1 / B-CER (K7) | slot 值即实体、每 utt 天然有一个（HB-30）；SESOI 待首格。 |
| is21_deep_bias（S4） | 待定（英文；列表冻结后）；参照 HB-28 test-clean B-WER 14.1→5.7@100 | 相对 B-WER↓ (HB-27) | oracle-list 正典；对文献 apples-to-apples。 |
| AISHELL-NER（S4） | 待定（中文；取 NER 标签后。AISHELL-1 ASR acc 0.8908 仅作运行背景，非 B-CER 靶） | 相对 B-CER↓ (HB-29) | 891 实体协议。 |

（spoken-squad dev 0.85 (40) [0.725, 0.95] 保留为可选第四主场备胎，非预注册主场。）

### 5.2 基线定义——"裸核心标准用法"的可操作化（去主观）

基线 = **裸核心（frozen Qwen3-Omni-30B，无任何外挂知识子系统）以标准用法运行**。为使"标准用法"客观可判，操作化定义如下，全部 dev 轻调后**冻结**、写入 prereg，之后不得改：(a) **prompt** = 各 K 型任务的固定模板（`templates.py`，音频进 + 固定任务定义文本：label 集/MCQ 选项/工具注册/JSON schema；绝不含 golden 转写/答案/intent）；(b) **采样** = greedy（temperature 0.0，top_p 0.95，top_k 40，repeat_penalty 1.0，max_tokens 200，即 locked 工件的 `sampling_params`）；(c) **dev 轻调自由度**仅限模板措辞与输出解析正则，在 dev n≈40 上单次择优后冻结，**冻结点写入 hash**；(d) 基线只用**系统接口契约**（音频/文本进、文本出、采样），与主配置同级——不给基线任何额外特权，也不给外挂。这样"基线是否被刻意压低"可由第三方对照冻结模板与采样参数客观核验。

### 5.3 系统复杂度阶梯（sophistication ladder，臂族内自低向高）

owner 第二轮裁定的基线哲学反转落地为阶梯，**不要求先把核心调到极致**：①**long-context 全塞入**（平凡知识供给：把候选知识整段塞进 prompt，无检索；预期在 Qwen-Audio 族大列表下崩溃，HB-16 N≥100 灾难幻觉、HB-25 全注入 TSR 28.20% ≪ 检索 65.53%）；②**own-ASR 朴素级联**（omni 自身 ASR→文本键检索→注入，外挂系统最低阶形态；ASR WER 作协变量，修复 panel R2-minor）；③**RDU 完整配置**（检索键模态 × 使用递送，发现段两遍见 S3）。**主主张（H-sys 比较 1）比对裸基线；阶梯主张（比较 2/3）比对 ①②**——即"精心组织的 RDU 相对平凡供给的组织智慧净增益"。

### 5.4 S4 实体偏置协议（全文；修复 panel #3 的答案注入；完整协议见附录 A）

**度量**：主指标 = 相对 B-WER/B-CER 下降 `(B-WER_nobias − B-WER_bias)/B-WER_nobias`（HB-27；B-WER/U-WER 度量约定 = Le et al. arXiv:2104.02194, IS2021 **[标准]**，度量惯例不过期；偏置词占比小，整体 WER 会稀释效应，故报 B-WER 不报 WER）；U-WER/插入错误并列报告以惩罚盲抄。

**热词库冻结**：每个测试床的热词/实体库在 **eval 之前**冻结（测试床皆为标准基准工件 **[标准]**：is21_deep_bias 的 ~209.2K 稀词池 HB-28 = Le et al. 2104.02194, IS2021；AISHELL-NER 891 实体 HB-29 = ICASSP2022；SLURP 逐域 slot 值库 HB-30 = arXiv:2011.13205, EMNLP2020；选型理由由 2025 注入文献 co-motivate），库快照写入 content_hash（§6.2）。库冻结后不得因看到 eval 结果而增删。

**可部署列表 = 音频键检索产出**（不是注入 golden）：对每条 utt，deployable 臂的偏置列表 = {音频键检索 over 冻结库的 **top-k 产出**} ∪ {干扰词}。真实体**不保证入列**——只有当它被检索命中才出现；命中与否作为**检索召回/同音精度（H5a）单独报告**，不进 B-WER 的条件。B-WER **以检索产出为条件计算**，非以注入为条件。这结构性阻断 C-T7（`answer_in_own_KB=1.0`、检索用 question 文本、clean rerun −0.066 null）与 C-M3（注入 test-item golden 转写 → 假 +22.4%）的泄漏类。

**保证入列 = oracle 上界臂（不可部署）**：真词保证命中的列表（Phoneme-RAG 训练侧惯例）降为**永久标注"不可部署、只作上界 headroom"**的 oracle 臂，与 gold-transcript 臂同级；绝不作主指标。

**干扰词构造**：干扰词从各测试床**固定池**按**预注册 seed + 列表规模 N** 采样（模型不能靠盲抄列表取胜）；真词占比（半 utt 含真实体、半不含，HB-15 惯例）预注册、中途不改。

**列表长度扫描 {2, 5, 10, 50}**（deployable 检索 top-k 轴，4 格）：先验甜点 top-2（HB-15 KER 11.99@top-2 vs 15.21@top-10），更多候选单调更差；此 4 格全进家族（§5.6 #10–13）。另设 oracle-list 距 distractor-N∈{100,500,1000,2000} 的**上界参考曲线**（HB-28 惯例，仅对文献 apples-to-apples，不进主家族）。注入形式 `logit_bias`/GBNF 两臂**已依 2026-07-12 续18 裁定移除**，不再作为 H5 载荷或探索项（HB-8 表面形式脆弱、纯 logit_bias 类比仅 ~9% 恰在门槛下，原调研记录保留于附录 A §7 原文，仅供工程诊断参考；修复 panel #16）。H5 的 15% 相对靶改由检索短列表 prompt 单独承载，可达性待 D6 首格实测复核（**⚠ 见风险节 §10 标注**）。

### 5.5 臂预算、按遍计价与 1 真格标定承诺

探索层（dev only）：系统配置 ≈ 键空间(4) × 递送(3) ≈ 12–16 格/集 + 基线族 3（裸/①/②）+ 对照臂 4（random-retrieval、oracle-retrieval 上界、gold-transcript 上界、no-retrieval）≈ **20–23 格 × 4 集 ≈ 90 格** + S3 两遍管线 8 格 + S4 测试床 ~24 格。**每臂按生成遍数计价**：own-ASR 级联 / HyDE 两遍臂仍按 ×2 生成遍计价；**S3 触发式检索臂改按 m+1 遍计价**（修复 panel #15 + 续18 自一致性成本口径）——第一遍不确定度信号取 **m=3 次采样的自一致性一致率**（非单遍 logprob 阈值），第一遍本身即需 m=3 次生成，触发后再加 1 次第二遍生成：**触发 item 每条 = m+1 = 4 遍，未触发 item 每条 = m = 3 遍**（原按 2 遍/item 的估计已过时、系统性低估自一致性成本，此处如实上调）。S3 两遍管线 8 格的总生成遍预算相应从 8×2=16 遍上调为区间 **8×3 ~ 8×4 = 24–32 遍**（依实测触发率而定）。**硬承诺**：开跑前**实测 1 真格 wall-clock（含 m=3 采样耗时）**（记入 `_repro/step2_mock/`）再据以定预算，不以未实测常数承诺时间线。

### 5.6 统计分析计划

**单尺度（修复 panel #4/F1/F4）**：一律以**相对改善百分比**为主尺度，主判定 = 相对尺度单门 ≥10%（H-sys）/≥15% 相对 B-WER（S4）；**不设"绝对且相对"双门**（避免高基线集自相矛盾达标）。

**per-dataset SESOI 数值表（预注册附表）**：为可解释性与功效计算，把 10% 相对门槛换算为各集绝对当量（决策仍在相对尺度）：

| 数据集 | dev 基线 | 10% 相对 → 绝对当量 (目标水平) | 可达性 |
|---|---|---|---|
| heysquad | 0.225 | **+0.0225** (→0.2475) | 可达，头空充足 |
| SQuAD-zh | 0.925 | +0.0925 (→**1.0175，超天花板**) | **不可达**；受 §9 退场规则，不能同时"达标又失败" |
| vocalbench-knowledge（锚点） | 0.8875 | within-item 配对差，不设 10% lift 靶 | N/A |
| SLURP-intent | 0.6452 | **+0.0645** (→0.7097) | 可达 |
| squtr / SLURP-slot / is21 / AISHELL-NER | 待定 | 首个合法真格后回填（squtr 待 corpus 侧重建；S4 待列表冻结） | 待定（预留 sign-off 槽） |

（SQuAD-zh 的不可达是诚实结果，非缺陷：0.925 近饱和 → 该集大概率触发 §9「oracle-retrieval 无增益 → 退出主场」，保留仅作近饱和负头空检查。）

**15 项家族全枚举（修复 panel #11/M1；每假设一预声明家族，全表进 Holm/max-T）**：

| # | 假设族 | 对比 | 检验 |
|---|---|---|---|
| 1 | H-sys | 最优 RDU 配置 vs 裸核心基线 | paired cluster-boot, 相对单门 ≥10% |
| 2 | H-sys 阶梯 | 最优 RDU vs long-context 全塞入① | superiority (相对) |
| 3 | H-sys 阶梯 | 最优 RDU vs own-ASR 朴素级联② | superiority (相对) |
| 4 | S1 | omni-own 键 vs 专化冻结键（R@k + 端到端） | paired |
| 5 | S1 | omni-own 键 vs trained-frozen（nemotron） | paired |
| 6 | S1 | 专化冻结 vs nemotron | paired |
| 7 | S2 | 递送主效应（card+2轮 合并最优 vs flat）− 键模态主效应，联合 CI | 联合 CI（非"≥任意维度"，修复 panel #5/F2） |
| 8 | S3 | 触发式 two-pass vs 恒检索：增益差 TOST（margin 预注册） | 等价 (TOST) |
| 9 | S3 | 触发式 two-pass 调用降幅 ≥30% | superiority（双门，修复 panel #14/M4） |
| 10–13 | S4 | 列表长度 {2, 5, 10, 50} 相对 B-WER（4 格） | 各格 paired |
| 14 | S4 | 检索式注入主对比 vs 全列表塞入 | superiority (≥15% 相对) |
| 15 | 闭卷锚点 | within-item KB-供 vs KB-留 配对差（同音频同题） | paired |

**Holm + max-T**：15 项按 Holm step-down（α=0.05）与 max-T（置换/自举最大统计量）双跑，"显著"必注所属家族与家族规模（吸取 C-ASR-V2 更正教训：曾把家族事后收窄为 4 selector×N=8 报"Holm 存活"，全网格实为 16–48 比较，更正后 neither 存活——**家族一经预注册不得事后收窄**）。

**交互模型预注册（修复 panel #13/M3）**：预声明格级模型 `y ~ key + delivery + key×delivery + (1|group)`；H-sys 赢家**按格级估计**选择（非边际）；S2 主效应解读**以 key×delivery 交互 CI 宽度门控**——交互 CI 宽/主导时只报格级、不塌缩为边际（防"边际平均把键模态主效应稀释成 null 而错杀 S1"）。先验预期存在交互（不确定度触发只在好递送下有益；audio-direct 可能只在 card 下有益）。

**cluster bootstrap（诚实回退）**：paired cluster bootstrap，group_key = 来源篇章 id（heysquad/SQuAD：Wikipedia passage）/ 说话人或场景（SLURP）；跨集以**固定效应为主**，DerSimonian-Laird τ²（k=3–4）**仅作参考不决策**（panel R1-m1 处置）。**无组键的集**：或补真组键、或不入确证层（修复 panel #7/M7）；不得以 item-level bootstrap 冒充组无泄漏。

**功效诚实（panel #12/M2）**：dev n≈40、heysquad ci95 宽达 [0.10,0.35]（有效 cluster 数 20–45 而非 40），在 +0.0225 绝对当量上、Holm 校正 15 项后，排除 0 的功效低。**故探索层不触发任何 kill**（输出 = 配置排序 + Phase-B 协议草案）；**kill 仅在确证层**、以加大 n 的锁定 test 抽取后判定。

### 5.7 探索/确证防火墙 + 信标种子 custodian 协议（全文；修复 panel #6/#7/#12）

**探索层**：dev-only，输出仅配置排序 + Phase-B 协议草案（预命名赢家 ≤3 + 基线族 + 对照），**无 accept/reject、无 kill**。

**确证层**（owner 签 Phase-B 后）：**先公布 hash{抽取脚本、排除后合格组 ID 全集、种子规则}入库（抽取之前）**；**种子取自公共未来信标**（预命名的比特币区块高度哈希或 NIST randomness beacon 指定时刻脉冲，抽取前无法预知，杜绝协调者反复抽取择优的 commitment-after-observation）；**独立人类联署**（custodian ≠ owner/设计者/运行者，修复 panel #6 的 custodian=owner 违规）；**全新会话仅接收已承诺脚本 + pool**，执行抽取；抽出的 ID 须由第三方从 revealed salt+seed **可重算**。确证池**组不相交于 union(dev + 旧 test + 65 曝光清单)**（修复 panel #7）；无组键数据集不入确证层或先补组键。**单通道单次消费、读取即 burn**——确证工件一经打开即焚，不得二次探索。

## 6. 边界与 custody（Boundary Discipline & Custody）

v1 §5 边界纪律全部保留，本节按 v2 系统对象逐臂加固。总原则（Information-Boundary Guard，`wiki/Information-Boundary-Guard.md` STANDING RULE）：**任何杠杆若靠部署没有的信息抬指标即 invalid，无论统计多显著**；四问全 YES 方可跑（部署可得性、模态尊重、无 test-item 泄漏、真能力非喂答案）。

### 6.1 IB-Guard 逐臂实例化（含 S4）

| 臂类型 | 部署可得性 (Q1) | 模态尊重 (Q2) | 无 test-item 泄漏 (Q3) | 裁定 |
|---|---|---|---|---|
| 检索键嵌入（omni-own / GLAP / nemotron） | query = 音频（部署有）✅ | 音频键直接；查询用 omni 自身理解 ✅ | value = 外部语料证据、库 eval 前冻结、绝不含 test-item ✅ | 部署 |
| own-ASR 级联 | query text = omni **自身 ASR 输出**（非 golden）✅ | omni 对 query 的自身转写属合法处理（IB-Guard "omni's own transcription of the query"）✅ | 不注入 golden 转写 ✅；ASR WER 作协变量报告 | 部署（阶梯②） |
| 递送（flat/card/2-turn） | 文本任务定义 + 检索到的 KB 值 ✅ | 文本指令，不替换音频输入 ✅ | 无 test-item 答案 ✅ | 部署 |
| 闭卷锚点（within-item） | 同一音频，KB-供 vs KB-留；KB-留即部署默认 ✅ | ✅ | 配对同题，无泄漏 ✅ | 部署 |
| S4 deployable 偏置列表 | = 音频键检索产出（§5.4）✅ | 音频键 ✅ | 真实体不保证入列、只在检索命中时出现；干扰词按 seed 采样 ✅ | 部署 |
| oracle-retrieval / gold-transcript / 保证入列列表 | ❌ 部署无此输入 | — | 用了 reference/golden | **永久非部署，只作上界 headroom** |

具象泄漏教训（直接反例）：C-M3（注入 test-item golden 转写 → 假 +22.4%；部署无此输入，且若有则 omni 无必要）、C-T7（`answer_in_own_KB=1.0`、检索用 question 文本 → 假 +51.7pp，clean rerun −0.066 null）、C-MINDS-POLICY（support 取自 held-out eval 行 → transductive，非 zero-shot）。**这三条是 S4 与检索臂必须结构性规避的类。**

### 6.2 KB custody——content_hash 扩展与 fail-closed 断言（修复 panel #8/M8）

现行 `content_hash_of`（`kb_schema.py`）= sha256(values.jsonl bytes + keys.npy bytes + sorted from_item_ids + code_git_sha)——只钉存储向量，**不钉检索函数**。扩展为额外覆盖：**嵌入器 SHA + revision + 量化 + 归一化配置**（键侧与查询侧各一）与**索引构建参数**（`index_backend`、metric、归一化、top-k），并在每条检索结果上戳 per-result 索引 hash。**fail-closed 键==查询断言**：查询时 `kb_retrieve._query_embedder` 必须以 manifest 的 `embedder_token` 重嵌入到与持久化键**同一空间**，键侧 token ≠ 查询侧 token 时**抛错（RAISE），绝不回退到 CLAP/'auto'**——这正是 C-PHASEA P0-4（query-embedder auto-fallback 静默换嵌入空间/维度、content_hash 仍"匹配"却复现 bug）的修复。SLURP/is21/AISHELL-NER 的冻结热词库快照亦纳入 content_hash。

### 6.3 逐工件 provenance 要求

确证工件必须非空以下字段（现 dev 工件的 `git_dirty=true`、`engine_build_id=null`、`dataset_revision=null`、`manifest_hash=null` 属 Stage-1 探索可容忍，**确证层不可**）：`git_sha`（且 `git_dirty=false`）、`engine_build_id`（llama.cpp build）、`dataset_revision`（来自 `docs/datasets.lock.json` pin）、`manifest_hash`、`sample_manifest` hash、`seed`、`env_versions`、KB `content_hash` + `embedder_token`。度量定义（corpus vs macro、B-WER vs WER）显式标注（吸取 C-ASR-ORACLE 的 corpus/macro 混淆教训）。

### 6.4 clean-checkout 规则与 ACCESS 纪律教训

**clean-checkout 规则**：确证 re-run 从干净 checkout（`git_dirty=false`）执行，**绝不用作者的 warm session**（模板 §4）；独立第三方或独立 agent 复跑，记 re-runner 身份 + 日期 + 数字 + run ID，落在预注册容差带内方过。

**ACCESS 纪律教训（写入执行手册）**：(1) **信息边界过界是本项目的既有失败模式**——反复把部署没有的信息（尤其 test-item golden 转写/答案）喂给模型造假增益，统计学没抓住、任务定义+模态透镜抓住了；对每个杠杆跑 IB-Guard、区分 read-out 杠杆 vs new-info 杠杆、绝不信 n=3 smoke。(2) **并发会话协调**：GPU launch 前查 `pgrep` + `gpu_session` lock，commit 前后复查 git log，勿把树 diff 默认为自己所为。(3) **WSL detached-run**：`python -u`（否则空日志）、`HF_HUB_OFFLINE=1`（缓存 embedder 会卡 HF 网调）、embedder 置 CPU 让 GPU 给 llama-server、按路径 kill 不自杀。(4) **KB 对象纪律**：库值必须是**证据内容**而非 query/question 本身（C-PHASEA 续15：squtr 曾把 FiQA query 自文当 KB 值、vocalbench 把 question 自文当值——对象错配，非知识利用）；corpus 侧重建（`build_squtr_corpus_source`）+ G2 layer-3 真机 ref-config 重建通过前，squtr 主场不产合法真格。

---

## 7. reward 信号层（数据集无关的借用基础设施，非理论贡献；详账见附录 B）

**定位（RDU §0 定向 + panel M17/R4-MAJOR-5 修复）**：reward 信号层**不是本提案的研究方向**，而是一组**数据集无关的标准信号供给**——换数据集不换信号定义。它**只**服务两处前端决策：(a) **发现段触发**（S3 两遍管线第一遍的 when/what-to-retrieve 门），(b) **使用段信任标定**（采纳率 α 与冲突消解的权重）。**明确不用于输出重排序作为研究主张**（那是 Proposal-B 的 parked 范围）。**δ_corr 从我方定理约束清单中移除**，引 ROVER（Fiscus 1997 **[谱系]**，附录 B C17）作为跨源误差互补的 28 年前正典，作**借用基础设施**认账，不作理论贡献。

**信号表（系统接口契约约束：全部输出侧信号，无 tier 划分）**

| 信号 | 所需接口 | 触发用途（发现段） | 标定用途（使用段） | 证据/状态 |
|---|---|---|---|---|
| 小样本自一致性（m=3 采样一致率 / ROVER 词对齐投票 / MBR 互评 WER） | 多次采样（m=3）、文本出 | 一致率低→触发检索 | 一致度→信任权重 | MBR@8 中性（ns），C-ASR-V2 directional |
| 验证器一致度（δ_corr：第二个 context-differentiated 冻结 omni 打分候选，同权重异 system-prompt） | 二遍推理、文本出 | 验证器质疑→触发 | 跨源一致→采纳 | 借用基础设施（ROVER/Fiscus，附录 B C17/C19 OPEN） |
| 答案级置信引出（追问模型自评可答性/置信） | 追加一轮、文本出 | 低置信→触发 | 自评置信→α 校准 | 未验，探索层标定 |

logprob 类白盒信号退出系统设计，其 Stage-1 标定记录保留于 ledger（C-ASR-V2），仅供工程诊断（#35）。**成本纪律**：自一致性触发需多采样（m 次生成），成本入 §5 的按遍计价（第一遍 m=3 次 + 触发后第二遍 1 次 = 触发 item 共 m+1 遍，见 §5.5）。

**离线标定实验（存量池、CPU、near-free；探索层不触发 kill，见 §9）**：在冻结 `_repro/asr_bon_v2_{clean,snr5}.json`（test.other 96 utt × pool8 × 3 seed，候选与 per-utt logprob 已存，logprob 字段仅供工程诊断复核、不进入触发/标定口径）上，逐 item 计算各信号与该 item **oracle 知识增益**（oracle@8 − greedy）的 Spearman 秩相关 ρ_s 与标定曲线 → 产出触发阈 τ\* 与使用段信任权重。**报告纪律**：clean/snr5 分列（附录 B §3 区间律，平均会掩盖），corpus+macro 双分母，cluster bootstrap CI，预冻 SESOI，报 S/D/I 与 pool-collapse rate、proxy-vs-oracle 秩相关。**边界（Information-Boundary Guard）**：选择/验证器**永不见 golden 转写**，δ_corr 验证器再听音频时 prompt 里绝不放参考。CPU 臂（logprob/MBR/自一致/熵/PLL，均为存量池离线标定 battery、非系统组件）near-zero 边际；**δ_corr 臂需 GPU**（resident llama-server，对存量池一遍打分，不重生成）。

## 8. 理论轨（形式化对象 = 系统算子；与工程实现同指一物）

**对象转移**（v2.1 §7）：从"模型本体纯度"转为**系统算子**——两遍管线触发规则与检索-递送复合算子。**门类匹配**（template §5）：触发是**有限一次性选择器** → 出**良定性说明 + 相关界**，**不强证"收敛"**（收敛在此未定义）；多轮迭代化推广才需 C1/C3。写证充分，Lean 只留给**有限性引理**（recall 下界 = margin 算术、过严门控反例 = 有限构造）。

1. **两遍触发算子** g: signal s ↦ {retrieve, ¬retrieve}（阈值 τ）。**正确性** = 有界信号上的确定阈值良定（finite-argmax 良定）。**无约束反例（过严门控）**：precision 最大化的门在信号无信息（ρ_s≈0）时把 recall→0，漏掉需知识的 item，端到端增益 G(g)=recall·Δ_deliver−(1−precision)·c_distractor 可 → 0 或负——**由 gate−inject=−0.134 的方向性证据激励（C-T7；"约束是召回而非精度""宁可多送不可漏送"）**，**不引 C-T7 的 +51.7pp 泄漏正数**（C-T7 = invalid）。**recall 下限约束下的保证**：加显式约束 recall(g)≥r₀，则 G(g)≥r₀·Δ_deliver−(1−precision)·c_distractor；在 S1 的精度鲁棒性（冻结 omni 对干扰 passage 鲁棒，c_distractor 有界）下，当 Δ_deliver>0 时 RHS≥0——**两段结构**：无约束过严门失败（负）+ recall 下限恢复下界（正），与 C4 同构（recall-floor 是发现段算子的新约束项，类比 C4 的 τ）。
2. **检索-递送复合算子** D∘R：检索返回 ∅ 时 = 冻结基策略的恒等（no-retrieval 无头空）——绑定 OptSpace 的 `gain_product`/`qstar_product`：孤立的非信息检索**买不到头空，增益必来自递送真新证据**，即系统只靠**扩大 reward**（送入真新知识）而非"多挂检索机器"帮忙的机器验证陈述。
3. **Coverage.lean 作 i.i.d. 前置（非 operator-linked）**：复用现有 i.i.d.-Bernoulli 覆盖引理（`missProb_eq_prod`/`missProb_antitone`/`missProb_strictAnti`/`missProb_le_of_N_ge`）描述 top-k 检索覆盖所需实体的概率 1−(1−p)^k。**但明确 NOT operator-linked**：ledger **C-THEORY 的 operator-linked 定理计数 = 0 为权威**，Coverage.lean 形式化的是抽样/取样步、非选择/触发规则，**此前置不改变 count=0**。
4. **可执行一致性（G6）**：双轨绑定——Python↔Lean 逐例一致性测试（沿用 Coverage 的 parity 向量惯例 p=1/4,N=3⇒miss 27/64），令实现的触发/复合算子与定理假设逐例吻合。**G6 对新系统算子闭合前，不作"Lean 证明我方触发收敛"的任何论文句**；C-THEORY 纪律：sorry 计数 0 ≠ 收敛已证，Beirami 界是 imported axiom 非 Lean-proved。
5. **约束项 + 假设账（每假设量给测量槽，dual-track debate-loop）**：已有 C4 `realized_gap_le_two_tau`（τ→oracle，DONE）、C1（β 信赖域）、C2（N\* 预算）；**新增 recall-floor 为发现段专属约束**。待经验验证的假设：per-item 检索召回 p、干扰代价界 c_distractor（S1 精度鲁棒性）、信号-增益相关 ρ_s（§7 标定表）——各有测量槽。

## 9. 迭代 / 停止规则（效果优先；确证层专属 kill）

1. **确证层 H-sys 达标** → 系统主张成立，进入 Stage-3 评估。
2. **确证层不达标** → **系统迭代循环**：分解归因瓶颈段（检索/发现/使用）→ 修订组件/协议 → 重新探索；**预算 cap = Stage-2 内最多 2 轮迭代（每轮需 owner 批准，§13 slot 7）**，耗尽后 owner 复盘决定是否转向边界性结论。
3. **oracle-retrieval 无增益的集** → 该集退出主场（瓶颈不在知识供给，非系统失败）。
4. **确证层专属 kill（panel M12/F-firewall）**：探索层**不触发任何 kill**，输出 = 配置排序 + Phase-B 协议草案；一切 TOST/CI 判定只在 owner 签 Phase-B 后的 custodian 单通道确证层发生（cluster 有效 N=20–45，探索层 CI 不作 accept/reject）。
5. **负结果纪律**："负结果也是贡献"**禁用于主问题**（v2.1 §0③）——H-sys 不达标只能进迭代循环，不自我安慰；**次级科学点 S1–S4 各自如实报告，正负皆入 claim_ledger，不影响 H-sys 判定路径**（S1 若 omni-own 键不足，系统换更强冻结组件继续，负结果仅记 S1 边界）。

## 10. 风险与缓解（含五类跨评审周期的常驻失败模式）

| 风险 | 似然×影响 | 消解 gate / 实验 |
|---|---|---|
| 跨模态路由缺口（audio-query→text-keyed-corpus 未实现，C-PHASEA / R3-MAJOR-1） | 高×高（Week-1 时间线） | Week-1 先交 own-ASR 文本-文本臂；路由并行建+验证；audio-key 臂门控于路由验证；cascade ASR WER 作协变量 |
| 同音/近音污染（音频相似检索 #1 失效，HB-21；RECAST 硬负挖掘） | 高×中 | 音频键+文本键双持（BR-ASR TextualBias OOV-鲁棒，HB-26）；recall-floor 算子含显式 precision 项；同音精度 H5a 单独报；c_distractor 由 S1 界定 |
| 闭源 API 信号成本（自一致性/置信引出/验证器一致度需额外采样；δ_corr 需 GPU） | 中×中 | 系统接口契约按生成遍计价（含 m=3 自一致性的 m+1 遍，M15）；离线标定用存量池 CPU near-free；δ_corr = 对存量池一遍打分非重生成；logprob 仅留 ledger 作工程诊断（#35），不进系统触发 |
| 小簇退化（有效 N=cluster 20–45，R1-M2；k=3–4 时 DL τ² 不可靠） | 中×中 | group_key cluster bootstrap；固定效应为主、DL 仅参考；无组集不入确证层或补组键（M7）；kill 确证层专属 |
| GPU 预算（多遍臂被少算，R3-MAJOR-2；per-pass GEN_TIME 未实测） | 中×中 | 按遍计价（M15）；开跑前实测 1 真格；两批切分（text-key 先）；GPU 会话 lock 协调 |
| logit_bias/GBNF 亚门槛（历史发现：~9% LOGIC 恰在 10% 线下，中文多 token 实体表面形式脆弱，HB-8/17；两臂已依续18裁定移除） | 低×低（风险随臂移除而消解，但见下方 ⚠） | 两臂不再是系统风险，原调研记录保留于附录 A；**⚠ substance flag**：H5 的 15% 相对靶原设计为「检索短列表 prompt + 闭集 GBNF 组合」达成，GBNF 移除后改为单靠检索短列表 prompt 承载，可达性未经重新验证，需 D6 首格实测复核，若不足须回§9 迭代 |

**五类跨评审周期常驻失败模式（各带结构性预防）**——从 claim_ledger 的 invalid 谱系提炼，作标准风险常挂：
- **P1 信息边界泄漏**（喂 golden 转写/答案→假增益；C-M3、C-T7 = invalid）→ 结构预防：递送列表 = 检索产出（S4，非注入）；oracle/gold 臂永久标不可部署上界；G3 泄漏红队 gate；每杠杆过 Information-Boundary Guard。
- **P2 对象错配**（KB 值 = 查询自身文本而非检索语料文档；C-PHASEA = invalid）→ 语料侧 KB 重建（squtr 310 docs text-keyed）；content_hash 扩展至嵌入器+索引（M8）；值必为证据内容。
- **P3 transductive/非零样本混淆**（support 建自 eval 行；C-MINDS-POLICY = invalid）→ card 池与 eval 不相交；确证池组不相交于 union(dev+旧test+65曝光)（M7）；选择仅在 dev。
- **P4 依赖运行冒充重复 / winner's-curse**（5 依赖运行称"5×"；seed 未隔离；C-W4-EMO、C-ASR-SEEDS = invalid；H3 估计 winner's-curse）→ 独立组 cluster bootstrap；H-sys 赢家按 dev 格级估计选定、确证层单通道重立；S2 单一预注册对比（F5/M13）。
- **P5 家族误计 / 事后收窄**（7-vs-5 对比；Holm4 vs 全发现网格；C-MINDS-V2、C-ASR-V2 更正）→ 15 项家族全枚举预注册、全进 Holm/max-T（M11）；"显著"必注家族；交互模型预注册（M13）。

**伦理/许可/数据治理**：逐集 license+permitted-use（squtr/heysquad/SQuAD-zh/vocalbench-knowledge/is21_deep_bias/AISHELL-NER/SLURP/LibriSpeech）；生物特征/声纹（AISHELL 说话人、SLURP）与情感数据按 PII/敏感属性处理；**dual-use 注记**：上下文偏置可被误用于监听式关键词 spotting——预期用途界定为**无障碍/知识辅助**。

## 11. 时间线与交付（3 周，v2.1 §10 展开 + 跨核心迁移冒烟）

**Week 1（今日可跑技术栈优先，路由并行）**：D1 own-ASR 级联文本-文本臂可跑；D2 文本键系统配置（flat/card/2-turn 递送）；D3 跨模态 audio-query→text-key 路由建成并在留出样本验证；D4 S4 偏置协议（is21_deep_bias 经 WSL git clone + AISHELL-NER 标签 + B-WER 打分器 + 检索→列表对齐）；D5 两遍管线 harness（mock 口径之外，过 assert_no_adaptive_logic）；D6 1 真格 wall-clock/per-pass 标定；D7 探索分两批（batch-1 text-key 周末开跑，batch-2 audio-key 待路由验证）。
**Week 2（分解归因 + Phase-B 草案）**：D8 三段归因分析（检索/发现/使用）；D9 §7 离线信号标定表（CPU 存量池）；D10 Phase-B 协议草案（预命名赢家 ≤3 + 基线族 3 + 对照臂 4 + custodian 脚本 + 信标 seed 规则 + 候选 ID 全集 hash）；D11 S1 报告（omni-own 键 vs 专化冻结 vs trained-frozen nemotron，squtr 原生 R@k/nDCG）；D12 S2/S3/S4 探索排序 + 交互-CI 宽度检查。
**Week 3（确证 + 迁移证据）**：D13 owner 签 Phase-B（§13 slot 6）；D14 custodian 信标抽取（公共信标 seed、承诺脚本、全新会话）；D15 单通道确证跑、读取即 burn；D16 H-sys 判定 vs 预注册 SESOI 家族；D17 **跨核心迁移冒烟**——系统接口契约配置在第二核心（MERaLiON-2 或一闭源 API）上 1–2 集轻验，作**可迁移性证据（价值主张）**；D18 Decision-Log 追加 + Per-Work-Status 更新 + wiki-sync。

## 12. Panel 17 项处置映射（逐条一行，按全提案编号；六级状态制跟踪）

- **F1**（重构主问题）→ §0/§1/§3：主问题重构为效果口径、裸基线+阶梯双主张，owner 裁定。
- **F2**（H2 触发被禁 + 未引先行）→ §2.3/§3-S3：触发出 mock 口径作独立两遍管线，引 FLARE/Self-RAG，定位为 active-retrieval 向冻结 omni 迁移。
- **F3**（H5 B-WER 答案注入）→ §3-S4/§5.4：可部署列表 = 音频键检索产出（非注入），保证入列列表降为 oracle 上界臂、标不可部署。
- **F4**（co-primary 阈值自相矛盾）→ §3.2/§5.6：单尺度（相对改善%）+ per-dataset SESOI 数值表，去掉绝对/相对双门冲突。
- **F5**（H3 估计病态）→ §3-S2/§5.6：单一预注册对比 = 递送主效应 − 键模态主效应 + 联合 CI，去"≥任意维度"。
- **M6**（custodian 非独立/承诺不绑定）→ §5.7：独立人 co-sign + 先公布 hash{脚本,候选全集,seed 规则} + 信标 seed + 全新会话只收承诺脚本。
- **M7**（防火墙漏 42 无组集群泄漏）→ §5.7/§5.6：确证池组不相交于 union(dev+旧test+65曝光)，无组集不入确证或补组键。
- **M8**（content_hash 漏检索函数）→ §4.3/§6.2：扩展至嵌入器 SHA+revision+量化+归一化 + 索引参数（键==查询 fail-closed）。
- **M9**（闭卷锚点跨集相减）→ §3.2/§5.1：改 within-item 配对对比（同音频，KB 供给 vs 保留）。
- **M10**（Week-1 不可跑）→ §11：Week-1 交 own-ASR 文本臂 + 建/验路由 + 重键语料，cascade WER 作协变量。
- **M11**（家族不完整）→ §5.6：15 项全家族枚举、全进 Holm/max-T，"显著"必注家族。
- **M12**（kill 打在欠功探索层）→ §5.7/§9：探索层无 kill，kill 确证层专属，探索层出排序非 accept/reject。
- **M13**（无交互模型）→ §5.6：预注册键×递送交互，H-sys 赢家按格级估计选，主效应解读受交互-CI 宽度门控。
- **M14**（H2 "等增益"接受零假设）→ §3-S3/§5.6：双门 = 增益差 TOST（margin 预注册）+ 调用降幅 ≥30% superiority，两门须过。
- **M15**（GPU 预算漏多遍臂）→ §4.2/§5.5：按生成遍计价（two-pass ×2），开跑前实测 1 真格。
- **M16**（logit_bias/GBNF 未建 + ~9%）→ 附录 A + §4.2/§7：两臂已依 2026-07-12 续18 裁定移除（原探索记录保留于附录 A），不再作 H5 承重；H5 的 15% 靶改由检索短列表 prompt 单独承载（可达性待复核，见 §10 ⚠）。
- **M17**（δ_corr 既 disclaim 又承重）→ §7/§8：定位"借用基础设施"，引 ROVER/Fiscus（1997 **[谱系]**），移出定理约束清单。
- **噪音 5 项**（主席驳回）：R1-m1（k=3–4 DL τ²）报固定效应/per-dataset、非决策性；R1-m2 家族重计并入 M11；R3 "2-turn 工具"更名"两轮 prompt 递送"（cosmetic）；R3 "新 scheduler" 作工程任务非设计缺陷；R4-MINOR8 两遍缺口占用被 F1 pivot 吸收。

## 13. Owner / Reviewer 签字位（9 槽，标推荐默认）

1. **§1 主问题措辞（裸基线 + 阶梯双主张）+ 系统接口契约（单一，无 tier 划分，续18）** — 推荐默认：**照签**（双主张结构消解 R4-F1/F2）。签字：待定。
2. **10% 相对门槛 + per-dataset SESOI 数值表** — 推荐默认：**单相对尺度为主判定，签前填满 SESOI 数值表**（各集基线→10% 绝对换算）。签字：待定。
3. **§3 次级科学点取舍（S1–S4）** — 推荐默认：**四点全留，S1 非阻塞**（omni-own 不足则换冻结组件续跑）。签字：待定。
4. **§5.5 臂预算（~90 格 + S3 8 格 + S4 ~24 格）** — 推荐默认：**按遍计价、门控于 1 真格标定**（D6 后复核 wall-clock）。签字：待定。
5. **§5.6 家族表（15 项全枚举）** — 推荐默认：**照签 15 项 Holm/max-T**。签字：待定。
6. **custodian 信标协议** — 推荐默认：**独立人 co-sign（非 owner 单签，R2-M6）+ 公共信标 seed + 承诺脚本**。签字：待定。
7. **§9 迭代预算（Stage-2 内 2 轮 cap，每轮 owner 批准）** — 推荐默认：**2 轮 cap**。签字：待定。
8. **S4 偏置协议（检索产出列表 + oracle 上界臂不可部署）** — 推荐默认：**检索产出列表；测试床 = is21_deep_bias / AISHELL-NER / SLURP**。签字：待定。
9. **时间线（3 周 + 跨核心迁移冒烟）** — 推荐默认：**照签，带 Week-1 现实化注记**（own-ASR 先行、路由并行；H1/audio-key 门控于路由验证）。签字：待定。

---

## 附录（Appendices）

- **附录 A — S4 热词/上下文偏置协议、测试床、传统技术存活裁定**：`2026-07-12-omni-hotword-biasing-survey.md`（四透镜：Lens1 传统偏置技术 × chat-API 存活性 / Lens2 prompt 偏置效应量与列表规模 / Lens3 检索式注入证据 / Lens4 基准·协议·本地测试床；HB-1…HB-30 账本）。§2.1、§3-S4、§5.4 全部 HB-* 引用与 is21_deep_bias / AISHELL-NER / SLURP 协议以此为准。**移除说明（续18）**：`logit_bias`/GBNF 白空间臂已依 2026-07-12 第三轮 owner 裁定（续18）自系统臂族移除，不再是本 FULL 提案的系统组件；本 survey 原文对二者的调研记录（HB-8/HB-10 等）原样保留，仅供工程诊断参考。
- **附录 B — reward 信号层：后融合/重排序认账 + 存量池离线标定实验**：`2026-07-12-omni-lm-rescoring-survey.md`（Lens1 经典后融合 / Lens2 LLM-GER training-free / Lens3 omni 二遍解码研究现状 / Lens4 存量池离线重排序设计；C17=ROVER/Fiscus 1997、C19=δ_corr OPEN）。§2.2、§7 的 reward-infra 认账、δ_corr 借用定位、logprob@8（C-ASR-V2）标定以此为准。
