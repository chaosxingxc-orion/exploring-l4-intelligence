---
title: "Research Proposal v4.1：以业务效果为裁判、以 reward-guided selector 为身份锚的前端多模态知识体系——冻结 omni 的检索·发现·使用（RDU）+ 轨迹选择算子"
date: 2026-07-12
version: v4.1
supersedes: "v4（[2026-07-13-research-proposal-v4-external-review.md](2026-07-13-research-proposal-v4-external-review.md)，状态 REJECT/NO-GO）"
audience: "外部评审（self-contained review copy）"
scope: "training-free（零权重、零核心结构改动；外挂系统组件另加）、闭源 API 兼容的 omni agentic 知识子系统 + reward-guided 轨迹选择算子"
evidence_grade: "全部先验数字带 claim-ledger ID；status: valid|directional 者方可引（directional 一律标 Stage-1 假设级）；invalid 仅限失败史附录 D，绝不作正向动机；无 ledger 条目者标 unverified、不作设计依据"
relation_to_review: "v4 收到对抗式诚信审查（REJECT/NO-GO，四 FUNDAMENTAL + QRP），我方 5 路独立复核逐条核验 37/42 CONFIRMED、0 REFUTED，本 v4.1 按 owner 四项裁决（Decision-Log 续24）整体重构。"
---

# 以业务效果为裁判、以 reward-guided selector 为身份锚的前端多模态知识体系（v4.1）

> ## ⚠️ 勘误二（2026-07-12 当日发布，append-only；针对博导级对抗复审的已核验事实项）
>
> **v4.2 已按 Decision-Log 续26 裁决发布（`2026-07-12-research-proposal-v42-external-review.md`）；本 v4.1 自此为历史记录，外审一律使用 v4.2。**
>
> 本文发布当日收到第二轮对抗复审（`2026-07-12-response-v4-and-v41-doctoral-adversarial-review.md`）。我方 5 路独立复核其 42 项可核验主张：**39 CONFIRMED / 3 PARTIAL / 0 REFUTED**。以下五处为本文**已核验的事实性/算术性缺陷**，即日声明生效；结构修订属 owner 裁决事项，将以 v4.2 发布。**本文维持不可签字状态。**
>
> 1. **"可验证 reward" 为错名**（§3.2/§4.2）：自一致性、验证器一致度、置信引出三信号均不读 gold、无确定性验证器，按领域标准用法应称 **label-free proxy reward**；真效用 U 与代理 Û 的符号分离及 proxy 诊断（within-question rank AUROC、self-consistent-error 压力子集、Goodhart 曲线）待 v4.2。
> 2. **§4.3 算术性自相矛盾**："单次 RDU（K=1）与 selector 严格匹配同一 K 预算"不可能同真——K=1 改标**低成本系统基线**，等预算对照族仅含 K-candidate random / MBR / selector。
> 3. **§9.5 与 §9.8/§11 矛盾**：签字门要求证明"不可预测 custody"，而本方案采用的公开固定种子（续24④）只提供可复算性、不提供盲法——本方案的 custody 实为 **public deterministic evaluation（透明可复现、非盲法）**，证据等级按此如实标注；措辞修正待 v4.2。
> 4. **当前活跃 squtr 检索语料为 qrels-conditioned mini-corpus**：310 文档 = 110 个 test-qrels 全部正例 + 200 干扰项，正例密度较官方全语料（57,638 docs）抬升约 ×186——只可作 DEV smoke，**不构成"KB 与评估标注独立构建"**；全语料重建列入 v4.2 工程包。同时其 `n_golds=0 → CLEAN` 审计为空转通过（零 gold 被检查），审计语义拆分（query_independent_corpus / label_independent_build 等）与 `NOT_EVALUATED` 输出待修。
> 5. **S3 效果对比存在采样算力混杂**：触发臂 5–6 遍生成 vs 恒检索 2 遍，效果差异无法归因于触发策略本身；预算匹配设计（同采样预算下 never/always/triggered）待 v4.2。

> **本版与 v4 审查的关系（一句话）**：v4 被外部对抗式诚信审查判为 REJECT/NO-GO；我方对该审查 42 项可核验主张逐条独立复核（37 CONFIRMED / 5 PARTIAL / 0 REFUTED、无一被驳），据此按 owner 四项裁决（Decision-Log 续24）整体重构为本 v4.1，四处事实错误已改正、四个 FUNDAMENTAL 阻断项已按裁决处置。**在本 v4.1 完成外审与 §签字位 签字前，不得被引用为已通过评审或可进入 Stage-2 的方案。**

> **一句话主张**：不改任何一个权重、不改任何**核心**结构（外挂系统组件另加），把一个**冻结的 omni 核心**（本地 Qwen3-Omni-30B 作科学载具，闭源 API 作价值场景）搭成可验证、可闭环的 agentic system，通过精心组织的**检索–发现–使用（RDU）**前端知识子系统 + 一个**可部署 reward 引导的轨迹选择算子**，在**头空合格的知识依赖型语音任务**上对**裸核心基线**取得 **≥10% 的错误率相对下降**，并把 oracle 头空实现出可靠比例（selector realization rate ρ）。系统接口契约唯一——**音频/文本进、文本出、多次采样**——检索匹配特征由**独立冻结 embedder**（外挂系统组件）产生，故设计为**最小接口设计**，可迁移性由跨核心冒烟作证。

**评审重点导览**（load-bearing 章节）：

- **§3 双层主问题 + §4 轨迹选择算子**——本版智识内核与 TFRL 身份锚：(i) 系统效果 vs 裸核心；(ii) reward 引导 selector 的 ρ 实现率（恢复 owner 已签 G0 主问题）。
- **§5 接口契约**——为何检索特征是"独立冻结 embedder 的语音向量"而非核心裸信号；核心 2048d 隐态降为白盒诊断臂。
- **§6 匹配几何**——零训练生成桥接能否追平专训检索器（form-bridge 假设，非"同分布"既定事实）。
- **§9 统计分析计划 + 附录 A 原子假设清单**——原子化假设族（dataset × endpoint × contrast，一 p 值一校正路径）、去成本门、SESOI 诚实标注。
- **§11 复现与完整性**——tutorial 级可复现替代锁死仪式；claim-ledger 治理。

---

## 1. 背景与动机

### 1.1 部署现实：核心冻结、能力外挂

语音 / omni 多模态 LLM 已进入"核心冻结、能力外挂"的部署形态。最强的 omni 核心——本地冻结检查点（Qwen3-Omni-30B，arXiv:2509.17765）或闭源 API（GPT-4o-Audio、Gemini 一类）——使用方既不能改权重、也不能改结构；闭源 API 更只暴露**音频/文本进、文本出、多次采样**这单一接口契约，logprob / logit_bias / 语法约束都不保证可达。这不是缺陷假设，而是**部署现实**。

在此现实下，真实业务价值不在把某个核心的裸能力刷到极致（那是模型厂的事），而在把既有核心搭成**可验证、可闭环**的系统，针对性提升其**外挂能力**。三类外挂按粒度区分——知识（通用事实）、记忆（特定实例召回）、技能（任务模板注册）；本提案聚焦**知识子系统**，记忆 / 技能为同级外挂、暂缓。核心价值在于：无需触碰核心权重即可在知识依赖型语音任务上兑现效果，且**最小接口设计**便于向闭源 API 迁移。本地冻结核心是**科学载具**（严格可复现），闭源可迁移性是**价值主张**（跨核心冒烟作证）。

**术语纪律（C-5）**：本提案全程使用 **"零权重、零核心结构改动；外挂系统组件另加"**——RDU 明显新增了检索、触发、知识卡、两遍/多遍采样与 KB 等外挂系统结构，绝不表述为裸"零结构改动"。可迁移性一律表述为 **"最小接口设计 + 跨核心冒烟作证"**，绝不表述为"天然向任意闭源 API 迁移"。

**"知识依赖型语音任务"范围界定**：任务的正确输出依赖于**音频本身未携带、须由外部证据补足**的信息——语音知识问答（heysquad / SQuAD-zh / squtr，答案在语料而非音频）、口语意图/槽位理解（SLURP，域知识约束槽值）、实体/专名密集转写（is21_deep_bias / AISHELL-NER，稀词与命名实体须由偏置库补足）。纯声学任务（说话人、情感）不在范围。**头条主张的总体进一步限定为"头空合格的知识依赖型语音任务"**（§9.4 资格规则；S-2 处置）。

### 1.2 为什么是前端知识校正，而非后端融合

training-free 的主战场在**前端**——组织与校正输入侧多模态知识体系。**后端**（重排序 / 验证器）不立为独立研究方向，只作**数据集无关的标准 reward 信号供给**（§10、附录 C），且这些输出侧信号正是 §4 selector 算子的 reward 来源。三条理由：(1) 后融合自由改写在强、低-WER 冻结核心上普遍中性到有害（LIR-ASR arXiv:2509.15095，2025-09，Whisper-large-v3 上去规则约束令 LLM 自由改写使 CER/WER 由 2.89/5.23 恶化到 6.62/9.27；arXiv:2501.15310，2025-01 强核心经纠错 WER 不降反升）；(2) 前端注入受核心生成能力封顶但不破坏它，闭源 API 原生可达；(3) 后端唯一可移植的 training-free 原语（受约束选择 + 误差去相关信号）保留为 selector 的 reward、发现段触发与使用段信任标定，换数据集不换信号定义。

**基线哲学反转**：不要求先把核心调到极致再测知识系统。基线 = **裸核心标准用法**；long-context 全塞入、own-ASR 朴素级联从"基线"改编入**系统复杂度阶梯**。

### 1.3 组织框架：检索–发现–使用（RDU）

- **检索 Retrieve**：给定语音输入，如何在异构键空间找候选证据——核心难点是**匹配几何**（§6）；
- **发现 Discover**：何时需要知识、需哪类、检回候选里哪些真相关——一个**描述性**测量子系统（§7）；
- **使用 Use**：知识以何形态进入模型、模型采纳多少——版本化标准知识卡 + 信任标定（§8）。

RDU 的三段被 §4 的 reward-guided 算子外包一层：对同一输入采样 K 条完整 RDU 轨迹，以可部署 reward 选择——这是本工作的 TFRL 身份所在。

### 1.4 Stage-1 先验证据（严格 ledger-conformant；directional 一律 Stage-1 假设级）

- **递送/内容供给方向性最大杠杆（C-MINDS-V2，directional）**：clean MInDS-14 factorial 上 cards-only +0.246、instruction+cards +0.262；**纯 zero-shot 元指令回归 −0.245 [−.286, −.201]**——发现段必须供给**内容**，只给元指令反破坏行为。**caveat（务必随引）**：这是 composite candidate-card treatment，含 ~3% card-text/eval-transcript 表面重叠（+3/107 命中），**不能归因于卡 schema 本身**；仅作 §8 递送对比的**方向性 motivation**，非"标准卡 schema 已证"。
- **采纳固执（unverified observation，pending mint）**：冲突时模型约 24% 采纳外部知识的观察在 claim ledger 中**无对应条目**（原 C-KEEP 不存在，工件溯源与 mint 未完成）。该数字**不作设计依据**，仅记为"未核实观察、待 mint"；使用段信任标定的动机改由 C-MINDS-V2 的"内容供给主导"承载。
- **reward 标定线（C-ASR-V2，directional，已退出系统设计）**：存量池离线选择器电池中 logprob@8 在 clean/snr5 两条件 corpus-WER 方向一致（clean +0.0094 [.0034,.0165]、snr5 +0.0081 [.0005,.0161]），**但在真实发现网格（每条件 16 比较）全家族 Holm 校正后两条件均不存活**——directional，非独立复现。该信号依赖逐 token logprob，**已退出系统设计**（闭源不保证可达），仅留 ledger 作工程诊断。
- **基线库（C-BASELINES，directional inventory）**：dev 基线来自冻结 locked-group 工件，但 provenance 记 `git_dirty=true` 且 engine build / dataset revision / manifest hash 为空，dev/test 跨波有重叠——**全部维持 directional inventory 等级**，不具确证级 provenance（§9.1 基线表 provenance caveat）。

> 历史失败教训（C-T7 的"召回优先"效应方向）**仅**保留于**失败史附录 D**，`invalid`（信息泄漏语境），**绝不作正向动机**；"召回优先"在本版是一条**待检验假设**，其操作化约束由发现段（§7）在清白管线上重新独立建立。

---

## 2. 相关工作、新颖性矩阵与可守边界

**引用新鲜度规则（续17）**：每条方向影响型主张由 ≥1 篇 ≥2025-01 一手来源锚定；较早著作仅在带显式角色标签时引用——**[谱系]** / **[标准]** / **[已弃用]**。

**上下文偏置分水岭**：六族传统偏置技术（shallow fusion [谱系]、CLAS [谱系]、trie 约束解码 arXiv:2508.17796、TCPGen [已弃用]、contextual adapters [已弃用]、CTC-WS [已弃用]）在 chat-API omni 下无一原样存活，分水岭 = **解码器内部访问**。**检索式注入是文献收敛的替代形态**（BR-ASR arXiv:2505.19179；RECAST EMNLP2025 findings.203；Hotword-RL arXiv:2512.21828；Locate-and-Focus arXiv:2507.18263 ACL2025），两读数：top-2 甜点、N≥100 灾难幻觉；**赢家检索器都是专训对比检索器，off-the-shelf CLAP 词汇键已死（R@1≈0.1）**。

### 2.1 新颖性矩阵（6 新邻 + 3 已引邻）

| 工作 | 有什么 | 相对我方缺什么 |
|---|---|---|
| **WavRAG**（ACL 2025，2025.acl-long.613） | 原生 audio 检索 + text/audio 混合 KB | 无严格黑盒契约、无 modality×form×delivery 因子分解、无 reward-guided ρ selector |
| **VoxRAG**（MAGMaR 2025，2025.magmar-1.3） | 模块化、免转写 spoken-QA RAG（CLAP+FAISS） | 组件非全冻结论证、无因子归因、无 selector 算子；用 off-the-shelf CLAP（我方证其词汇键已死） |
| **PlanRAG-Audio**（Findings ACL 2026，arXiv:2605.20414） | 规划 modality/time-span 后从结构化 text/audio DB 检索，系统叙事最接近 D-R-U | 无 training-free/黑盒承诺、无独立构建 KB 泄漏边界、无 ρ 与因子化贡献测量 |
| **Adaptive Retrieval Without Self-Knowledge**（ACL 2025，2025.acl-long.319） | 35 个 adaptive-retrieval 方法统一效率/性能评估；轻不确定度常胜复杂 pipeline | 非语音/omni、非黑盒外挂、无生成桥接匹配几何、无 selector ρ；作我方发现段的**强效率对照参照** |
| **RAG-E**（arXiv:2601.21803） | retriever–generator 交互/失配的实证分解 | 佐证 §7 归因为**描述性 taxonomy 非加法恒等式**；非语音、无黑盒契约 |
| **Decomposing Retrieval Failures**（arXiv:2602.17981） | 检索失败因素非简单加法 | 同上，用以否定加法恒等式；无 modality-bridge / selector |
| **BR-ASR**（arXiv:2505.19179，已引） | 专训语音偏置检索近邻，"训练能买到什么"对照 | 需训练检索器；我方走零训练生成桥接反制 |
| **RECAST**（Findings EMNLP 2025，已引） | 对 decoder states 做对比训练检索 | 依赖训练 + 内部状态；违反我方黑盒契约 |
| **HyDE**（arXiv:2212.10496 [谱系]，已引） | a2a 假想答案桥 | **其自陈 caveat**：假想文档可含虚假细节，有效性依赖 dense bottleneck 过滤——我方 a2a 臂必带此幻觉风险标注，非只取"a2a matching"正面 |

### 2.2 可守住的新颖性边界（狭窄合取）

当前 survey **不支持**"RDU 系统组织是空白"或"天然兼容任意闭源 API"。可守、可检验的空白是一个**狭窄合取**——以下五者同时成立者，上述任一近邻均不具备：

> **严格黑盒契约（音频/文本进、文本出、多采样）× 全部组件冻结 × 知识库与评估标注独立构建 × 贡献的因子化测量（modality bridge × form bridge × delivery）× reward-guided 轨迹选择算子（ρ 实现率）。**

**效果是唯一最终裁判**；我方不主张任一段机制新颖，而主张在此狭窄合取下取得业务效果并把 oracle 头空实现出可靠比例。

---

## 3. 双层主问题（Primary Questions, two layers）

### 3.1 第(i)层：系统效果（SYSTEM effect）

> 以冻结 Qwen3-Omni-30B 为核心的 omni agentic system，加装前端 RDU 知识子系统（组件异构、全部冻结使用），能否在**头空合格的知识依赖型语音任务**上，对**裸核心标准用法基线**取得 **≥10% 错误率相对下降**、全家族校正后统计可靠、边界清白的效果提升？

- **Estimand**：最优 RDU 配置相对裸基线的**错误率相对下降**（单尺度，error = 1 − acc 换算）。
- **总体范围（S-2）**：头条限定为**头空合格数据集**（§9.4 资格规则）；对不合格集不主张头条效果。
- **主聚合（S-5）**：**一个焦点数据集为 primary + 若干 replication 集带 no-harm 门**，**不以跨异构任务族的固定效应池化作 primary**；如展示任何聚合，报告异质性并要求 ≥2 预定任务族方向一致。

### 3.2 第(ii)层：selector 实现率（TFRL 身份锚，恢复 owner 已签 G0）

> 对同一输入生成 K 条**可部署** rewrite–retrieve–deliver–answer 轨迹，用**预注册、可部署、输出侧可验证 reward** 选择其一；这个 reward 引导的轨迹选择算子相对**等预算对照**（随机选择 / MBR / 单次 RDU），能把 oracle 候选头空实现出多大比例？

- **Primary metric（恢复 G0）**：**ρ = (R_selector − R_greedy) / (R_oracle − R_greedy)**，selector realization rate；cluster bootstrap CI（cluster = speaker/session/question-family），同报绝对 delta 与全量成本诚实计账；oracle 分母 ≤0 的 item/集单独处理，禁止无限/负 ρ。
- **身份声明**：第(ii)层使本工作成为项目 thesis 定义的 **weight-frozen reward-guided inference-time optimization**（TFRL），而非"因为没训练就自动算 RL"。算子定义见 §4；与之同对象的 Lean 定理（票 #27）见 §10.2。

### 3.3 五个次级科学点（S1a / S1b / S2 / S3 / S4，各自如实报告、正负皆入 ledger）

- **S1a（同形式冻结匹配，form bridge 假设）**：给定冻结 embedder，把检索键从"文档内容形态"（q2a）改造为"问题形态"（q2q）能否提升匹配质量？此为**待检验的 form-bridge 假设，绝不预设"同分布"**（I-4）。Estimand = q2q vs q2a 检索质量（R@k/nDCG）+ 端到端贡献，同一冻结 embedder。
- **S1b（生成桥接 vs 专训检索器）**：最优生成桥接（建库 q2q + 查询 a2a/HyDE）能否零训练追平/超越专训冻结检索器（GLAP/nemotron）？**预注册承诺**：若须训练薄投影才达标，如实报为 training-free 负结果，绝不静默替换。
- **S2（递送主效应，equal-content A/B）**：见 §8.2，**完全等内容 A/B**（同事实/示例/token 预算/位置，只变 schema/turn 结构）。
- **S3（发现段·效果优先触发研究，成本仅描述）**：见 §7，触发式两遍 vs 恒检索的**效果**判定；成本仅作**描述性计账**，**不设任何成本成功门**（R1）。
- **S4（上下文实体偏置，构念独立臂）**：见 §9.6，作**构念相关但相异的独立研究臂**，非"共同机制"证据（C-6）。

---

## 4. Reward-guided 轨迹选择算子（Path B，TFRL 身份核心）

本节定义 §3.2 第(ii)层的算子，与 Python 实现、Lean 定理（#27）**同指一物**。

### 4.1 动作空间与策略（frozen sampling）

- **动作空间 A**：给定输入 x，一条轨迹 τ = ⟨查询构造(改写) → 检索 → 递送(知识卡) → 作答⟩。每个环节仅调用黑盒接口（音频/文本进、文本出、多采样），不触碰权重、不访问解码器内部。
- **策略 π（冻结采样）**：冻结核心以温度 T 采样生成 K 条轨迹 {τ₁…τ_K}。策略 = 冻结模型的采样分布本身；**不训练、不更新任何参数**。这是"training-free"的严格含义——搜索的是模型自身行为，不是模型权重。

### 4.2 reward（可部署、输出侧、可验证）

reward R(τ) 只用系统契约内的输出侧信号，**永不见 golden 转写/答案**：

- **自一致性一致率**：K 条轨迹答案间的一致度（逐 K-type 等价定义，§7.1）；
- **验证器一致度 δ_corr**：第二个 context-differentiated 冻结 omni（同权重、异 system-prompt）对答案打分的跨源一致；
- **答案级置信引出**：追问模型自评可答性/置信。

三者均可单用或线性组合，权重于 M2 探索层 dev 标定后冻结、不在确证层调。

### 4.3 选择规则、停止规则与预算 N*

- **选择规则（selector）**：τ\* = argmax_τ R(τ)（或 reward 加权）。这是 ρ 中的 R_selector。
- **停止规则 / 预算 cap N\***：K ≤ N\*（预算上限）；若一致率 ≥ 预注册阈值可提前停。N\* 由 §9 的 1 真格成本标定确定并冻结。
- **等预算对照（硬约束）**：random selection（K 条随机取一）/ MBR medoid / 单次 RDU（K=1），三者与 selector **严格匹配同一 K 预算与采样配置**，杜绝"selector 多采样 vs 对照单采样"的预算混杂。
- **ρ 的三个锚**：R_greedy = 单次 greedy；R_oracle = 按 golden 选最优（**仅上界、永久不可部署**）；R_selector = 上述可部署 selector。

### 4.4 与理论轨（#27）的同对象绑定

Lean 票 #27 形式化的正是本算子（非 RAG 系统外附的无关静态不等式）：**无约束失败 + 有约束收敛**——无 reward-估计误差界与预算 cap 时 selector 可被 reward hacking / 过优化支配而不收敛；在 reward-估计误差 ≤ τ 且预算 ≤ N\* 时给正确性 + 收敛/regret 界。假设账（§10.2）为 τ、N\* 与 C-4 必要条件各留测量槽。**Python↔Lean 逐例一致性测试**令实现的 selector 与定理算子逐例吻合；闭合前不作"Lean 已证我方 selector 收敛"的任何论文句。

---

## 5. 系统接口契约与组件（Interface Contract）

### 5.1 唯一硬契约（无 tier 划分）

只用任何闭源 API 都保证暴露的接口：**音频/文本输入、文本输出、多次采样**。发现段触发与 selector reward 一律用**输出侧信号**（§4.2、§7）。logprob 触发、`logit_bias`、语法硬约束**不是系统组件**（依赖解码器内部访问，闭源不保证可达）。本地冻结核心亦仅经黑盒接口使用，llama.cpp 白盒能力仅限工程诊断。

### 5.2 检索匹配特征 = 独立冻结 embedder 的语音向量（R2）

**为什么是语音向量而非核心裸信号（一段诚实回答）**：检索匹配在数学上需要一个**嵌入空间**——把语音查询与被存证据映到可算相似度的向量。这个嵌入由**独立冻结 embedder**（GLAP / omni-embed-nemotron）产生，它是一个**外挂系统组件，如同 KB 本身**：契约约束的是我方对**核心 API** 的要求，**不是**系统里能包含哪些外部冻结组件。因此音频查询的检索输入特征是语音向量、由外挂 embedder 得出，**不违反黑盒契约**。真正"死掉"的只是——把**核心自身的 2048d 隐态**当作**可部署检索键**：那需要核心暴露内部隐藏态，闭源 API 不保证可得。

### 5.3 组件表（全冻结使用；选型由 dev 效果决定并如实报告）

| 组件 | 角色 | 冻结使用标注 | 一手锚 |
|---|---|---|---|
| **GLAP** | 检索键嵌入（可部署主力，独立冻结 embedder） | trained-frozen；冻结使用、非 by-construction（LLMLingua-2 先例 [标准] 披露） | GLAP arXiv:2506.11350（2025-06，多语种语音内容检索，CLAP 无法胜任） |
| **omni-embed-nemotron** | 检索键嵌入（trained-frozen 天花板对照） | 冻结使用对照；非对称 `encode_document`；NC license 仅研究用 | Omni-Embed-Nemotron arXiv:2510.03458（2025-10，NVIDIA） |
| **own-ASR→文本级联** | **modality-bridge 对照臂**（阶梯②） | 边界清白（own-ASR 转写部署可得，非 golden）；cascade WER 作协变量 | 附录 B |
| **qwen3-omni-own 2048d 隐态** | **白盒诊断臂（demoted）** | **排除于一切 portable/deployable 头条主张**；只作白盒诊断 | LCO-Embedding arXiv:2510.11693（2025-10）+ MAEB arXiv:2602.16008（均分 ~50–52%，未饱和） |
| **专化侧翼** | 实体粒度检索器 + carrier-sentence 合成键 | 冻结使用；中文用学习跨模态检索器 | 附录 B |

> **对 W4 的显式声明**：核心 2048d 隐态降为白盒诊断臂，**不触碰 W4 叙事逻辑**——W4 是研究 omni **自身嵌入空间**的独立工作（§12），本降级只关乎 W1 的**可部署检索键**选择。

### 5.4 科学载具 vs 可迁移性（C-5 软化）

**科学载具** = Qwen3-Omni-30B Q8_0 GGUF via llama.cpp（`-ngl 28`，resident `llama-server`），数据/代码/种子全 pin，确证层结果在此复现。本系统只经黑盒接口消费核心，故本地核心上成立的系统级结论其输入面与闭源 API 完全一致。**可迁移性表述**：**最小接口设计 + 跨核心迁移冒烟**（第二核心 MERaLiON-2 或一闭源 API 上 1–2 集轻验，作证据、**非门控项**）；**绝不表述为"天然向任意闭源 API 迁移"**，不以单核心成立冒称通用。

---

## 6. 检索段：匹配几何（form-bridge 假设，非"同分布"既定）

### 6.1 匹配对象与递送对象分离

检索段深层难点是**匹配几何**：语音查询 q（问题分布）与被存证据 d（内容分布）**处于不同形态**。裁定：**匹配对象（key）与递送对象（value）分离**——value = 证据内容恒定；key = 最大化匹配信号的任意形态，含问题形态。

### 6.2 三态匹配几何（q2a / q2q / a2a，形式桥接均为待检验假设）

| regime | 键形态 | **假设**（待检验，I-4） | 实现（黑盒契约合法） |
|---|---|---|---|
| **q2a** | 键=文档内容 | 跨形态弱关联（基线假设） | 冻结 embedder 直接编码文档内容 |
| **q2q** | 键=为文档合成的伪问题 | 更强同形式匹配（**form-bridge 假设**） | 建库离线：冻结核心为每篇证据合成伪问题（doc2query 式 [谱系]）；语音查询即问题 |
| **a2a** | 键=查询的假想答案 | 更强同形式匹配（**form-bridge 假设**，含 HyDE 幻觉风险） | 查询时：冻结核心为查询生成假想答案（HyDE arXiv:2212.10496 [谱系]，含其自陈"假想文档可含虚假细节"caveat） |

**明确措辞（I-4）**：q2q/a2a **只桥接问句/答句的话语形式，不等于桥接模态或分布相同**；是否真提升匹配是 S1a/S1b 要检验的。受控设计把三个轴分开：**modality bridge**（独立-embedder 语音向量 vs own-ASR 文本）× **form bridge**（raw-doc/q2a vs q2q vs HyDE/a2a）× **delivery**（flat vs 等内容卡）。

### 6.3 零训练路线与 S1 分解

生成桥接两条路线都**只调黑盒 `generate`**：建库侧 q2q（离线一次性、成本摊薄）+ 查询侧 a2a（每查询一次生成）。S1a = 同形式冻结匹配（q2q vs q2a，同一 embedder）；S1b = 生成桥接（较优者）vs 专训冻结检索器（GLAP/nemotron）。**实体粒度**（S4）用**合成 carrier-sentence 键**（键落在与 utterance 同形态），同音精度由 §9.6 单独诊断。

---

## 7. 发现段：描述性测量子系统（Discover）

发现段是**描述性诊断**（非门控、无 pass/fail 阈、无成本成功门）。算法空间显式枚举：恒检索（always）/ 触发式两遍（triggered）/ 从不检索（none），触发信号取自一致性 / 验证器一致度 / 置信引出。触发式两遍：第一遍 **m=5** 采样、T=0.7 取一致率（颗粒度 {0,.2,.4,.6,.8,1}），低一致率→触发→第二遍 greedy。**逐 K-type 等价定义**（预注册）：MCQ/闭式 = exact-match；抽取式 QA = normalized token-F1 ≥0.8；ASR = normalized WER ≤0.1（中文 **CER**，非 word-WER）。

### 7.1 效果优先，成本仅描述（R1）

报告**效果-成本曲线**而非单一赢家，但 **S3 确证判定只看效果**（触发式 vs 恒检索的效果 TOST/优越性，见 §9 家族），**成本不进任何成功门、不作 Pareto 支配主张**。成本为**全量诚实的描述性计账**（一次定对口径）：

- **completions**：触发 item = m+1 = **6** 遍（m=5）；未触发 = **5** 遍；恒检索 = **2** 遍/item；从不 = **1** 遍。
- 另报 **input+output tokens、wall-clock latency、GPU-seconds**。
- **效率优化明确推迟至后期阶段**；前期不给方案添加成本约束。

### 7.2 三层描述性指标栈

| 层 | 指标 | 定义（C-1/C-2 修订） |
|---|---|---|
| **L1 oracle-treatment responsiveness**（重命名，C-1） | 该 item 对 oracle 注入是否**响应** | **不再称"ground-truth 需求/iff"**；以重复采样估计 **P(Y₁−Y₀>0)**，报告四种潜在结局状态（0→1 benefiter / 1→0 harmed / 1→1 不变 / 0→0 non-responder），**描述性/诊断，永不作可部署标签** |
| **L2 触发响应对照** | 触发器决策 vs L1 responsiveness | TP/FP/FN/TN 对照表（描述性，非硬币） |
| **L3 失效 taxonomy**（C-2，非恒等式） | 漏检 / 失配 / 未采纳三类 | **描述性失败分类，不写"≈ 总缺口"的加法恒等式**（三类可重叠/交互，直接相加会双计数；generator 遇错证据行为非固定 distractor cost）。**未来识别设计**：顺序 counterfactual 干预（oracle 检索→oracle 排序→oracle 递送→oracle 采纳）或预注册 mediation/Shapley 分解 |

L1–L3 驱动迭代归因（§13.2 back-edge：漏检大→修触发；失配大→修匹配几何；未采纳大→修知识卡/信任标定），但**不承载确证判定**。

---

## 8. 使用段：标准知识卡（Use）

### 8.1 版本化知识卡 schema

字段 = content（递送对象）/ source-tag / relevance-signal / usage-directive；schema 版本化（写入 content_hash），跨集不变、只换 content。

### 8.2 S2 = 等内容 A/B（C-3）

**S2 收敛为完全等内容 A/B**：完全相同的事实、示例、token 预算与位置，**只改变 schema / turn 结构**——这样才把"标准卡组织"从"内容多少"中隔离出来。C-MINDS-V2 **仅作方向性 motivation 并随引 overlap caveat**（§1.4），**不作"标准卡 schema 已证"**。

### 8.3 信任标定（靶点，非一律推高的旋钮）

采纳倾向（"采纳固执"）是使用段靶点，但其 24% 观察为 unverified（§1.4），**不作设计常数**。信任标定目标 = 按证据质量条件化采纳：用输出侧信号（自一致性/验证器一致度/置信引出）估证据可信度，映射到 relevance-signal 字段与 usage-directive 措辞，间接调节采纳（系统不改权重，只改递送形态与指令强度）。

---

## 9. 实验设计与统计分析计划（SAP）

### 9.1 基线表（I-8 更正 + provenance caveat）

dev 基线来自冻结 locked-group 工件（seed 20260705，Q8_0 GGUF；**C-BASELINES：directional inventory**，`git_dirty=true`、engine build / dataset revision / manifest hash 空——非确证级 provenance）：

| 数据集（角色） | dev 基线 mean (n) | 度量 | 头空判读 |
|---|---|---|---|
| heysquad（主场候选，头空最大） | 0.225 (40) | span/QA acc | 抽取 QA，deployable 臂须以检索产出为条件（§9.6） |
| **SQuAD-zh**（更正） | **0.85 [0.725, 0.95] (40)** | QA acc | 近资格门边界（①闭卷<0.85 恰临界），大概率退场为诊断；以 eligibility-split 正式判定 |
| **uro-bench-SQuAD-zh**（若用，独立行） | **0.925 (40)** | QA acc | **与 SQuAD-zh 是不同工件**，不得混用；如用则单列，明显退场 |
| squtr（检索原生主场候选） | 待定（corpus 重建后回填） | 检索-QA | 唯一检索原生；SESOI 待首个合法真格 |
| vocalbench-knowledge（闭卷锚点） | 0.8875 (80) | QA acc | within-item 配对差，不做独立判定 |
| SLURP-intent（S4 邻） | 0.6452 (62) | intent acc | 中等头空 |
| is21_deep_bias（S4） | 待定；参照 test-clean B-WER 14.1→5.7@100 | 相对 B-WER↓ | oracle-list 正典 |
| AISHELL-NER（S4） | 待定（891 实体协议） | 相对 B-CER↓ | 中文实体场 |

### 9.2 基线与系统复杂度阶梯

**基线 = 裸核心标准用法**（dev 轻调后冻结、写入 hash）：固定任务模板（绝不含 golden 转写/答案/intent）；greedy（temp 0.0）；dev 自由度仅限模板措辞与解析正则；只用系统接口契约。**阶梯**：①long-context 全塞入（平凡供给）；②own-ASR 朴素级联（modality-bridge 对照，WER 作协变量）；③RDU 完整配置。头号主张比对裸基线；阶梯净增益（"组织智慧"）**单独裁定**，若仅第(i)层达标而阶梯净增益为 null → 系统有效但归因于"知识供给本身"，如实降级叙事，不 kill 第(i)层。

### 9.3 单尺度与 SESOI（S-3/S-4 诚实标注）

主判定尺度 = **错误率相对下降**（消高基线天花板悖论）；主判定 = ≥10%（H-sys）/ ≥15%（S4 B-WER）。**SESOI 于签字前固定，不随 dev 效果移动**：
- **10% / 15% 明确标注为"惯例科学阈值（conventional scientific threshold）"，不称"业务效果（business effect）"**——除非补充 stakeholder utility / 错误成本 / 延迟-token-预算 论证；本版不作此论证，故按惯例阈值口径。
- **移除 H5 的 15%→10% 自动回退作为 SESOI 变更**（S-3）：dev <12% 观察**只能**是**工程 futility / 路由决定**（是否为该测试床启用短列表偏置），**绝不改变"有意义效果"的定义**。per-dataset SESOI 数值表预注册（把相对下降换算各集绝对当量）。

### 9.4 预注册参考系资格规则（S-2；规则保留、头条限定）

- **判定切分**：第三个独立 **eligibility-split**（与 exploration-dev、confirmatory 三方 group-disjoint，n=40/集）。
- **判定条件（CI 下界）**：进入头条参考系须同时满足 ①闭卷基线 < 0.85；②知识头空（oracle-retrieval − bare-core）CI 下界 ≥ 2×SESOI（同 error-reduction 尺度）。
- **头条范围声明（S-2）**：头条主张明确限定为 **"headroom-qualified knowledge-dependent speech tasks only"**；资格筛选不恢复外部效度，故不冒称覆盖全部知识依赖任务。
- **单向性 + 固定分母**：只出不进；家族分母按预注册 MAX 计，退场行记 N/A 不收缩分母。
- **诚实预告**：SQuAD-zh（0.85，临界）/ uro-bench-SQuAD-zh（0.925）大概率退场；最终以 eligibility-split 判定为准。

### 9.5 原子假设族、多重性与轮次（S-1 / S-5 / S-6 / S-7）

- **原子化（S-1）**：确证族按**原子假设**枚举——每个 **dataset × endpoint × contrast** 一个最终 p 值 + 一条校正路径；**无复合行冒充单一假设**。完整机器可读清单见**附录 A**；本版 primary confirmatory 族 = **7 个原子假设**（1 焦点系统效果 + 2 replication no-harm + selector 层 ρ 1 + 3 等预算对照），**Holm within 声明族（m=7）**。次级科学点 S1–S4 归**独立的 secondary 探索族**，各自多重性、directional 报告，不并入 primary 分母。
- **主聚合（S-5）**：primary = 焦点集；replication 集走 no-harm 门；**不以异构任务族固定效应池化作 primary**；如展示聚合，报异质性 + ≥2 任务族方向一致。
- **一版一轮（S-6）**：**一个版本 = 一轮 confirmatory**；失败 → **新注册版本并声明 lineage**（旧轮永久保留入 cumulative evidence）；**放弃"5-look sequential trial"框架**（更简单，符合"少加约束"）。
- **每版 α（S-7）**：**撤销"每轮 α=0.01 等分"**（该等分在 holdout 供给证明之前采纳，无据）；**per-version α 在该版本注册时声明**。**holdout 供给表仍为签字门**：签字前须证明每集 group 基数 / 互斥 / disjoint / power 与不可预测 custody，再定研究规模。

### 9.6 S4 三构念拆分（C-6）+ 偏置协议

**S4 拆为三个构念，各有独立 KB 定义 / 泄漏边界 / 成功指标 / 迁移主张，作构念相异的相关研究臂，非共同机制证据**：

| 构念 | KB 定义 | 泄漏边界 | 成功指标 | 迁移主张 |
|---|---|---|---|---|
| **事实型外部知识** | 语料证据文档（heysquad/squtr/SQuAD-zh） | value=eval 前冻结外部语料，无 test-item | 错误率相对下降 | 跨知识 QA 集 |
| **任务本体/schema** | 域 ontology / intent-slot schema（SLURP） | schema 非答案 | intent/slot acc | 跨 SLU 域 |
| **上下文实体偏置** | 冻结热词/实体库（is21/AISHELL-NER） | 真词不保证入列 | 相对 B-WER/B-CER↓（≥15%） | 跨实体转写 |

**偏置协议**：热词库 eval 前冻结（写 content_hash）；可部署列表 = 音频键检索产出（含 carrier-sentence 键），非注入 golden；**B-WER reference-anchored 计分**（分母=全部参考偏置词；检索漏检计为错误、绝不从计分对象剔除，杜绝"只对检索到的词打分"泄漏）；oracle 上界臂**永久不可部署**；H5 相对 B-WER 靶 15%（惯例阈值口径，§9.3；无 SESOI 回退）。命中与否额外作 H5a（召回 + 同音精度）单独报告。

### 9.7 cluster bootstrap 与功效诚实

paired cluster bootstrap，group_key = 来源篇章 id / 说话人或场景。无组键集或补真组键、或不入确证。**功效诚实**：dev n≈40、有效 cluster 20–45，Holm 校正后功效低——**探索层不触发任何 kill**（输出=配置排序 + Phase-B 协议草案）；kill 仅在确证层以加大 n 的锁定 test 判定。

### 9.8 采样 custody 与 provenance（见 §11）

确证抽取由**提交先于选择的确定性脚本 + 固定种子**执行，第三方逐字节可复现（续21-B①，维持）。确证工件非空 provenance：`git_sha`(`git_dirty=false`)、`engine_build_id`、`dataset_revision`、`manifest_hash`、`sample_manifest` hash、`seed`、`env_versions`、KB `content_hash` + `embedder_token`；度量定义（corpus vs macro、B-WER vs WER）显式标注。确证 re-run 从干净 checkout 执行。

---

## 10. reward 信号层与理论轨

### 10.1 reward 信号层（数据集无关借用基础设施，非理论贡献）

一组数据集无关的输出侧信号供给，服务三处：§4 selector reward、§7 发现段触发、§8.3 使用段信任标定。**不用于输出重排序作为独立研究主张**。误差去相关 δ_corr 引 ROVER（Fiscus 1997 [谱系]）作借用基础设施认账，**移出定理约束清单、不作理论贡献**。logprob 类白盒信号退出系统设计，仅留 ledger 作工程诊断。

### 10.2 理论轨（对象 = §4 selector 算子；无约束失败 + 有约束收敛）

**形式化对象 = §4 的 reward-argmax 轨迹选择算子**（与 Python 同对象），非"模型本体纯度"。结构（CLAUDE.md 理论标准）：

1. **无约束反例**：无 reward-估计误差界与预算 cap 时，selector 在 reward 无信息/被 hack 时可过优化、不收敛或劣于随机。
2. **有约束收敛**：reward-估计误差 ≤ **τ** 且预算 ≤ **N\*** 时，给正确性 + 收敛/regret 界。
3. **检索-递送复合必要条件（C-4，显式声明为 MEASURED 假设）**：检索-递送复合算子要有正头空，**必要条件** = **r₀·Δ_deliver ≥ (1−precision)·c_distractor**（r₀=检索召回、Δ_deliver=逐 item 递送增益、precision=检索精度、c_distractor=干扰代价）——**显式陈述为待测假设，非隐藏进结论**；若下列测量槽无法建立，**理论贡献如实删除**。
4. **可执行一致性**：Python↔Lean 逐例一致性测试；sorry-free（记录例外）。闭合前不作"Lean 已证 selector 收敛"的论文句。

**假设账（每假设量给测量槽）**：

| 假设量 | 符号 | 测量槽 | 状态 |
|---|---|---|---|
| reward-估计误差界 | τ | 存量池离线：selector vs oracle 一致度 | 待测 |
| 预算 cap | N\* | 1 真格成本标定 + K 扫描 | 待测 |
| 检索召回 | r₀ | S1 检索 R@k | 待测 |
| 逐 item 递送增益 | Δ_deliver | oracle-retrieval vs bare 逐 item | 待测 |
| 干扰代价 | c_distractor | random-retrieval 注入伤害 | 待测 |
| 检索精度 | precision | S4 H5a 同音精度 | 待测 |
| **必要条件** | r₀·Δ_deliver ≥ (1−precision)·c_distractor | 由上导出 | 待验 |

---

## 11. 边界纪律、复现与完整性（R4：tutorial 级可复现）

**Information-Boundary Guard（STANDING RULE）**：任何杠杆若靠部署没有的信息抬指标即 **invalid，无论统计多显著**；四问全 YES 方可跑（部署可得性、模态尊重、无 test-item 泄漏、真能力非喂答案）。逐臂裁定：检索键嵌入（GLAP/nemotron，含 q2q/a2a 生成桥，query=音频、伪问题/HyDE 由核心自生）→部署；own-ASR 级联（query=own-ASR 非 golden）→部署；标准知识卡（无 test-item 答案）→部署；S4 deployable 列表（真词不保证入列）→部署；oracle-retrieval / gold-transcript / 保证入列列表 / **核心 2048d 隐态**→**非部署或仅诊断/上界**。

**替代复现标准 = tutorial 级可复现（R4）**：拒绝审查者的"全部锁死"路线（独立 custodian、commit–reveal、burn 记录一并否决，含最小 commit–reveal 变体）。替代标准三条：**① tutorial 级可复现**——第三方能 step-by-step 跑出全部宣称结果；**② 零数据集泄漏**；**③ 零学术欺诈**。落地 = **REPRODUCE.md 契约**：pinned 数据 manifest + 提交入库代码 SHA（`git_dirty=false`）+ 确定性脚本 + 固定种子（续21-B①）+ 预期输出与容差带。**明确不采用 custodian / commit–reveal / burn 仪式**——理由（owner 裁决）："我们是在做研究而不是做复杂的系统工程"；防过拟合由"提交先于选择 + 程序性防火墙 + 一版一轮 confirmatory（§9.5）"承载。

**claim-ledger 治理**：机器账本（`docs/claim_ledger.yaml`）**先于**任何散文——消费者以账本 status 解析可引性，散文中的旧正面措辞一律被账本覆盖。**一致性检查随发布冻结为工件**（由独立 checker 代理执行、非本文；附 checker code commit + rule manifest + 输入 hash + 输出 JSON + 失败项 + 执行环境），命名为 internal consistency check，**不等同外部评审**。

**五类常驻失败模式（结构性预防）**：P1 信息边界泄漏（喂 golden→假增益；C-M3/C-T7 = invalid）→ 递送=检索产出、oracle/gold 永久非部署、每杠杆过 IB-Guard；P2 对象错配（KB 值=查询自身文本；C-PHASEA = invalid）→ 语料侧 KB 重建、content_hash 扩至 embedder+索引、伪问题 builder 只从审计过的 corpus-document source manifest 构建；P3 transductive 混淆（C-MINDS-POLICY = invalid）→ 卡池与 eval 不相交、选择仅在 dev；P4 依赖运行冒充重复 / winner's-curse → 独立组 cluster bootstrap、赢家 dev 格级选定确证层单通道重立；P5 家族误计 / 事后收窄 → 原子族全枚举预注册（附录 A）、全进 Holm、"显著"必注家族。

**伦理/许可/dual-use**：逐集 license + permitted-use；生物特征/声纹按 PII 处理；上下文偏置用途界定为无障碍/知识辅助。

---

## 12. 工作身份（Work Identity，R4 事务一致刷新）

**本提案 = W1（`speech-mllm-training-free-rl`）的 primary study。** W1 = 项目的成熟 training-free 范式参考，本工作把其 reward/eval 机制升为一个完整的 reward-guided 前端知识系统。lineage（事务一致，Thesis / Per-Work-Status / 本 proposal / 响应函须同步刷新）：

- **G0（2026-07-11，四项全签）**：owner 签署 W1 收窄问题为 primary，primary estimand = **ρ = (R_selector − R_greedy)/(R_oracle − R_greedy)**（`2026-07-11-stage1-audit-response-and-rulings.md` §4）。
- **RDU refocus（续17–续21）**：三段设计修订（匹配几何 / 被测量发现段 / 标准知识卡）、单一接口契约、里程碑 DAG、确定性抽样脚本。
- **本 v4.1（续24）**：Path B 恢复 ρ 主问题为 §4 算子的同对象锚，撤成本门，接口契约按 R2 收敛，身份事务一致刷新。

**W4 是独立工作，不受触碰**：W4（`speech-mllm-omni-embedding-rl`）研究 omni **自身嵌入空间**的 task-conditioned 可读性/可选择性（disentanglement 措辞已按 G0 降级 L0/L1、按 §7.1 重立项 #29）。本 v4.1 把核心 2048d 隐态降为 W1 的白盒诊断臂**不改变 W4 的研究对象或叙事**。

---

## 13. 风险、迭代/停止规则与里程碑门控 DAG

### 13.1 风险与缓解

| 风险 | 似然×影响 | 消解 gate |
|---|---|---|
| 跨模态路由缺口（audio-query→text-keyed-corpus） | 高×高（M1 门槛） | M1 先交 own-ASR 文本臂；audio-key 臂门控于路由验证；cascade WER 协变量 |
| 匹配几何失效（生成桥接不足以追平专训检索器） | 中×高 | S1a/S1b 分层判定；须训练薄投影则如实报 training-free 负结果 |
| 同音/近音污染（BR-ASR DCL / RECAST 硬负） | 高×中 | 音频+文本键双持；必要条件含显式 precision 项；carrier-sentence 键；H5a 单独报 |
| selector reward 无信息（自一致性/置信引出弱） | 中×高 | ρ 报实现率、reward 于 dev 标定后冻结；等预算对照界定 selector 净值；τ 假设账测量槽 |
| 多采样成本（K 条轨迹 + m=5） | 中×中 | 全量诚实计账（§7.1）；1 真格标定 N\*；效率优化推迟后期；**不设成本门** |
| 小簇退化（有效 N 20–45；k=3–4 DL τ² 不可靠） | 中×中 | cluster bootstrap；焦点集为 primary、replication no-harm（不池化异构族） |

### 13.2 迭代 / 停止规则（效果优先；确证层专属 kill；一版一轮）

1. 确证层第(i)层达标且第(ii)层 ρ CI 下界 >0 → 系统主张 + selector 实现成立，进入 Stage-3。
2. 不达标 → **系统迭代循环**：用 §7.2 描述性 taxonomy 定位瓶颈段（漏检/失配/未采纳）→ 修组件/协议 → **新注册版本（一版一轮，S-6）声明 lineage** → 重新探索（M5→M2 back-edge）。归因仅限探索 dev（确证 test 绝不重读）。
3. selector ρ CI 在两独立 test surface 均不高于 0 → 结论定为"support exists, realization fails"，照常发表。
4. **负结果纪律**：禁用于主问题（按去赢设计）；次级点 S1–S4 正负皆入 ledger。

### 13.3 里程碑门控 DAG（无日历周；按门 entry criteria 全绿推进）

```
M1 工程就绪 ─▶ M2 探索完成 ─▶ M3 Phase-B 签署(owner) ─▶ M4 确证完成 ─▶ M5 迭代或 Stage-3 裁决
             ▲                                                              │
             └──────── M5→M2 back-edge（不达标→新注册版本，一版一轮）◀────────┘
```

- **M1 工程就绪**：clean-checkout 重建绿；跨模态路由实现验证；两遍/K-轨迹 harness；伪问题建库路径（corpus-document source manifest 输入，非 query）；确定性抽样脚本 + 固定种子（提交入库）；知识卡 schema；S4 资产（is21 + AISHELL-NER + B-WER 打分器）；中文 CER + minimal-pair 测试通过；真跨模态模型 live smoke（升 supported 前不得为 stub）；1 真格成本标定（含 m=5 + K-轨迹 wall-clock）。
- **M2 探索完成**：全臂族 dev 跑完（modality×form×delivery × selector × 阶梯 × S1–S4）；发现段三层描述性指标栈；§10.1 离线信号标定表；**holdout 供给表（签字门）**；资格判定（eligibility-split，CI 下界 ≥2×SESOI）；**原子族清单（附录 A）与 per-version α 定稿**；退出 = Phase-B 协议草案成文。
- **M3 Phase-B 签署（owner）**：审阅 M2 产出并签署；探索层不触发任何 kill。
- **M4 确证完成**：确定性脚本抽取（提交先于选择）；单通道评分；原子族 Holm（m=7 primary）判定 vs 预注册 SESOI；ρ 判定 vs 等预算对照；跨核心迁移冒烟（非门控）。
- **M5**：达标→Stage-3；不达标→新注册版本迭代或 owner 复盘。收尾：Decision-Log 追加 + Per-Work-Status 更新 + wiki-sync。

**汇报口径**：按门 entry criteria 绿/未绿汇报，不按日历。预算超首格实测 1.5× 中断回报 owner。

---

## 14. Owner / Reviewer 签字位

> **可修订工作参数**：以下签字时均可修订的三项 = **m=5 触发/采样诊断设置**、**H5 futility 门槛（工程 futility/路由，非 SESOI）**、**per-version α（该版注册时声明）**。**无成本类成功门**，**无 H5 SESOI 回退**（均已按 R1/S-3 撤除）。

1. **双层主问题**（(i) 系统效果 vs 裸基线 ≥10%，头条限定 headroom-qualified；(ii) selector ρ vs 等预算对照，恢复 G0）+ 系统接口契约（单一，检索特征=独立冻结 embedder 语音向量；核心 2048d 隐态=白盒诊断臂）。签字：待定。
2. **10% 错误率相对下降（惯例科学阈值口径）+ per-dataset SESOI 数值表（签字前固定、不随 dev 移动）+ 资格规则（eligibility-split ①闭卷<0.85 ②headroom CI 下界≥2×SESOI；头条限定 headroom-qualified）**。签字：待定。
3. **§4 reward-guided 轨迹选择算子**（动作空间/策略/reward/选择/停止 N\*/ρ）+ #27 Lean 同对象（无约束失败 + 有约束收敛 + 假设账 τ/N\*/C-4 必要条件）。签字：待定。
4. **原子假设族（附录 A，primary m=7，Holm within 族）+ 一版一轮 confirmatory + per-version α（S-6/S-7）+ holdout 供给表签字门**。签字：待定。
5. **次级科学点取舍（S1a/S1b/S2 等内容 A/B/S3 效果优先成本描述/S4 三构念拆分）**。签字：待定。
6. **复现与完整性标准 = tutorial 级可复现（REPRODUCE.md 契约）+ 零泄漏 + 零欺诈；确定性脚本 + 固定种子；不采用 custodian/commit-reveal/burn**。签字：待定。
7. **里程碑门控 DAG（M1→M5，own-ASR 先行、路由并行纳入 M1、预算超首格 1.5× 中断回报）**。签字：待定。

---

## 附录 A — 原子假设清单（machine-readable，S-1）

> 每个 `dataset × endpoint × contrast` 一个最终 p 值 + 一条校正路径；primary confirmatory 族 = 7 原子（Holm within 族，m=7）。焦点集 `<FOCUS>` 与 replication 集 `<REP1>/<REP2>` 于 M2 eligibility-split 后定名（诚实预告：squtr-corpus 为焦点候选，heysquad/SLURP-intent 为 replication 候选）。secondary 族（S1–S4）另表、directional、不并入 primary 分母。

```yaml
family: primary_confirmatory_v1        # per-version α declared at registration (S-7); one version = one round (S-6)
correction: holm                       # within this family, m = 7
selection_rule: frozen_before_eligibility
missingness: fail_closed
atoms:
  - hypothesis_id: H_SYS_FOCUS
    layer: system_effect               # question (i)
    dataset: <FOCUS>
    endpoint: normalized_error_reduction
    contrast: best_frozen_rdu_vs_bare_core
    statistic: paired_cluster_bootstrap_mean_diff
    decision: relative_reduction_ge_10pct_and_CI_lower_over_SESOI
    role: primary
  - hypothesis_id: H_SYS_REP1
    layer: system_effect
    dataset: <REP1>
    endpoint: normalized_error_reduction
    contrast: best_frozen_rdu_vs_bare_core
    statistic: paired_cluster_bootstrap_mean_diff
    decision: no_harm_gate              # replication, not pooled (S-5)
    role: replication
  - hypothesis_id: H_SYS_REP2
    layer: system_effect
    dataset: <REP2>
    endpoint: normalized_error_reduction
    contrast: best_frozen_rdu_vs_bare_core
    statistic: paired_cluster_bootstrap_mean_diff
    decision: no_harm_gate
    role: replication
  - hypothesis_id: H_SEL_RHO_FOCUS
    layer: selector_realization         # question (ii), restores G0
    dataset: <FOCUS>
    endpoint: rho_selector_realization  # (R_selector - R_greedy)/(R_oracle - R_greedy)
    contrast: reward_guided_selector_vs_greedy
    statistic: paired_cluster_bootstrap_CI
    decision: rho_CI_lower_gt_0
    role: primary
  - hypothesis_id: H_SEL_VS_RANDOM
    layer: selector_realization
    dataset: <FOCUS>
    endpoint: normalized_error
    contrast: selector_vs_random_selection_equal_budget
    statistic: paired_cluster_bootstrap_mean_diff
    decision: superiority
    role: primary
  - hypothesis_id: H_SEL_VS_MBR
    layer: selector_realization
    dataset: <FOCUS>
    endpoint: normalized_error
    contrast: selector_vs_mbr_medoid_equal_budget
    statistic: paired_cluster_bootstrap_mean_diff
    decision: superiority
    role: primary
  - hypothesis_id: H_SEL_VS_SINGLE
    layer: selector_realization
    dataset: <FOCUS>
    endpoint: normalized_error
    contrast: selector_vs_single_pass_rdu_equal_budget
    statistic: paired_cluster_bootstrap_mean_diff
    decision: superiority
    role: primary

secondary_family: secondary_science_v1   # S1-S4; directional; own multiplicity; NOT in primary denominator
secondary_atoms_summary:
  - S1a: q2q_vs_q2a_same_embedder            # retrieval R@k + end-to-end (form-bridge hypothesis)
  - S1b: generative_bridge_vs_trained_frozen # GLAP/nemotron ceiling
  - S2:  standard_card_vs_flat_EQUAL_CONTENT # identical facts/examples/tokens/position, vary schema only (C-3)
  - S3_effect: triggered_two_pass_vs_always_retrieval_EFFECT_ONLY  # TOST; cost DESCRIPTIVE only, NO cost gate (R1)
  - S4a: factual_external_knowledge          # construct 1 (C-6)
  - S4b: task_ontology_schema                # construct 2
  - S4c: contextual_entity_biasing_rel_BWER  # construct 3, reference-anchored, >=15% (conventional threshold)
```

---

## 附录 B — 热词 / 上下文偏置调研裁定（S4 协议锚）

四透镜调研（传统偏置技术 × chat-API 存活性 / prompt 偏置效应量与列表规模 / 检索式注入证据 / 基准·协议·本地测试床）。核心裁定：六族传统偏置技术在 chat-API omni 下无一原样存活（分水岭=解码器内部访问）；retrieve-then-inject 是文献收敛替代形态；top-2 甜点、N≥100 灾难幻觉、off-the-shelf CLAP 词汇键已死（R@1≈0.1）、赢家检索器多为专训对比检索器——正是 §6 匹配几何要以零训练生成桥接反制的现实。`logit_bias`/语法约束记录原样保留，仅供工程诊断，不作系统组件。own-ASR→text 级联作 modality-bridge 对照臂，cascade WER 作协变量。

---

## 附录 C — reward 信号层调研（后端认账 + 存量池离线标定）

四透镜（经典后融合 / LLM-GER training-free / omni 二遍解码现状 / 存量池离线标定设计）。核心裁定：约束选择安全、自由改写陷阱（regime-conditional，SEAL arXiv:2501.08421 立受约束解码为安全原语，剑桥 arXiv:2409.09554 示强 LLM 可超 N-best oracle）；GER 大数全为 fine-tuned；omni 自池 training-free 二遍解码本身是空白，**不以此空白立方向**——只把输出侧信号当作 §4 selector reward、发现段触发与使用段标定的供给。δ_corr 引 ROVER（Fiscus 1997 [谱系]）作借用基础设施认账，不作理论贡献。

---

## 附录 D — 评审历史与已弃方案（失败史；invalid 证据仅存于此）

**失败对象谱系（E0–E6，仅作失败史，绝不作正向证据）**：C-M3 假 +22.4%（喂 test-item golden 转写，invalid）；**C-T7 假 +51.7pp**（heysquad SQuAD-type answer-lookup，answer_in_own_KB=1.0、检索用问题文本，invalid——**其"召回优先"效应方向仅记于此，绝不作 §7 动机**）；C-PHASEA（PLAN-ONLY 冒充可执行 + squtr KB 值=query 自身文本对象错配，invalid）；C-MINDS-POLICY（transductive + 三因子混淆，invalid，已被 C-MINDS-V2 directional 取代）。E6 clean re-run 给 clean_H0 = −0.066（null）。

**owner 设计裁定谱系**：v1 敌对评审团（5 FUNDAMENTAL + 12 MAJOR）→ 研究对象重立为 omni agentic system、效果唯一裁判、frozen-key 降次级、基线哲学反转；续18 取消白盒扩展层（单一接口契约，logprob/logit_bias/语法约束退出系统组件）；续24（本版重构令）撤成本门、接口按 R2 收敛、Path B 恢复 ρ、身份事务一致刷新、tutorial 级可复现替代锁死仪式。

**已弃方案**：主问题"两头可发表"盾牌（仅留次级点）；自由改写 GER 作独立后融合线（收编为 reward 基础设施）；δ_corr 作理论贡献（降 ROVER 借用）；确证抽取的 NIST 信标 / 全新会话 / burn / commit–reveal 仪式（简化为提交先于选择的确定性脚本 + 固定种子，逐字节可复现）；**S3 成本类成功门（≥30% 调用降幅 + Pareto 支配，数学不可达，R1 撤除，成本降为描述性计账）**；**H5 15%→10% SESOI 自动回退（S-3 撤除，仅保留为工程 futility 决定）**；**每轮 α=0.01 等分（S-7 撤除，改 per-version α）**；**5-look sequential trial 框架（S-6 撤除，一版一轮）**。

**证据分级**：全部先验数字带 claim-ledger ID；status valid|directional 者方可引（directional 一律 Stage-1 假设级），invalid 仅限本附录、无 ledger 条目者标 unverified。Stage-1 证据保持其产生阶段等级，须在 Stage-2 大样本下重立方升级。
