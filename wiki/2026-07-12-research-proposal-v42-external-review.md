---
title: "Research Proposal v4.2：以效果为裁判、以 reward-guided selector 为身份锚的前端多模态知识体系——冻结 omni 的检索·发现·使用（RDU）+ 轨迹选择算子（收敛与锁定版）"
date: 2026-07-12
version: v4.2
supersedes: "v4.1（[2026-07-12-research-proposal-v41-external-review.md](2026-07-12-research-proposal-v41-external-review.md)，状态：待外审、五 F′ 待结构性处置）"
audience: "外部评审（self-contained review copy）"
scope: "training-free（零权重、零核心结构改动；外挂系统组件另加）、闭源 API 兼容的 omni agentic 知识子系统 + reward-guided 轨迹选择算子"
evidence_grade: "全部先验数字带 claim-ledger ID；status: valid|directional 者方可引（directional 一律标 Stage-1 假设级）；invalid 仅限失败史附录 D，绝不作正向动机；无 ledger 条目者标 unverified、不作设计依据"
relation_to_review: "v4.1 发布当日收到博导级对抗复审，判 MAJOR RECONSTRUCTION（五个 FUNDAMENTAL：F′-1 custody/F′-2 program 级 Type-I/F′-3 qrels-conditioned 语料/F′-4 proxy 误名/F′-5 预算混杂）。owner 已对五项逐条裁决（Decision-Log 续26，续24 为其上位标准）。本 v4.2 按裁决整体重构，逐项结构性处置五 F′。三处对审查者的尊重性商榷置于回信，不入本方案。"
status_note: "本 v4.2 仍待外部评审与 §14 签字；按单一最终确证版本制（G3），本版及此前所有版本按定义均为 development/exploration，不构成已通过评审或可进入确证的方案。"
---

# 以效果为裁判、以 reward-guided selector 为身份锚的前端多模态知识体系（v4.2，收敛与锁定版）

> **本版与前序审查的关系（一句话）**：v4 被判 REJECT/NO-GO；v4.1 收到博导级对抗复审，仍有五个可单独阻断确证的 FUNDAMENTAL。owner 已对五项全部裁决（续26）。本 v4.2 按裁决逐条**结构性**处置：F′-3 语料改**官方全语料**、qrels 只入评分；F′-1 custody 如实改称 **public deterministic evaluation**（**注：此为 rename + 延后盲法的裁决式处置；公开种子下的 selection-blindness 残余仍是 contested 敞口，§11 L4-6/§9.8，非完全结构性消解，L5-F1**）；F′-2 采**单一最终确证版本制**；F′-4 reward 改名 **label-free proxy reward** 并分离 U/Û；F′-5 K=1 改**低成本系统基线**、S3 改**轻量 1×3 预算匹配**。本版仍待外审与签字。

> **一句话主张**：不改任何一个权重、不改任何**核心**结构（外挂系统组件另加），把一个**冻结的 omni 核心**（本地 Qwen3-Omni-30B 作科学载具，闭源 API 作价值场景）搭成可闭环、可评测（reward-guided）的 agentic system（"verifiable/可验证" 一词按 §4 保留词纪律，只用于 §7.1 的确定性 per-K-type 验证器，不加诸整系统）。通过精心组织的**检索–发现–使用（RDU）**前端知识子系统 + 一个**可部署 proxy-reward 引导的轨迹选择算子**，在**头空合格的知识依赖型语音任务**上，对**裸核心基线**取得错误率相对下降（Q-A），并检验该选择算子能否在**等预算对照**下实现正的绝对效用增量、把 oracle 头空实现出可靠比例（Q-B）。系统接口契约唯一——**音频/文本进、文本出、多次采样**——检索匹配特征由**独立冻结 embedder**（外挂系统组件）产生，故设计为**最小接口设计**，可迁移性由跨核心冒烟作证。

**评审重点导览**（load-bearing 章节）：

- **§3 两个可分别裁定的确证问题 Q-A / Q-B + §4 轨迹选择算子（U/Û 记号）**——本版智识内核与 TFRL 身份锚（Q-A/Q-B 共用焦点集与 Holm 家族，非"真正独立"）。
- **§6.4 语料与 KB 独立性**——确证检索走**官方全语料**（57,638 docs），qrels 只入评分，五维审计语义，`NOT_EVALUATED` 规则，310 库永久降 DEV smoke。
- **§7 发现段 + S3 轻量 1×3 预算匹配**——同采样预算下 never/always/triggered，效果判定、成本描述。
- **§9 统计分析计划 + §9.5 单一最终确证版本制 + 附录 A 原子清单**——primary 仅 Q-A/Q-B 原子（每原子附 p 值**算法骨架**；α、per-dataset SESOI、no-harm margin、分母下限等**边界常数于 M3 确证注册落定**，本版不填），secondary 明确降为方向性排序、无 Holm 声明。
- **§9.8 / §11 复现与完整性**——public deterministic evaluation（诚实非盲法标签）+ tutorial 级 REPRODUCE.md 契约 + 单一标准测试入口（M1 门）。
- **§10.2 理论轨**——首定理 = 有限样本 selector regret，τ 由标定集上的 proxy 误差测量（非 argmax 一致度）。
- **§13.4 诚实缺口表**——尚未交付项 × 所属门。

> **编码命名空间图例（避免混淆）**：`C-1…C-6`、`I-*`、`S-*`、`F′-*`、`G*`、`R*` 均为**审查修订码（doctoral-review revision codes）**，**不是 claim-ledger 条目**；claim-ledger ID 一律形如 `C-<主题>`（如 `C-MINDS-V2`、`C-ASR-V2`、`C-BASELINES`、`C-T7`、`C-M3`、`C-PHASEA`），只有后者可按 evidence_grade 规则解析可引性。

---

## 1. 背景与动机

### 1.1 部署现实：核心冻结、能力外挂

语音 / omni 多模态 LLM 已进入"核心冻结、能力外挂"的部署形态。最强的 omni 核心——本地冻结检查点（Qwen3-Omni-30B，arXiv:2509.17765）或闭源 API（GPT-4o-Audio、Gemini 一类）——使用方既不能改权重、也不能改结构；闭源 API 更只暴露**音频/文本进、文本出、多次采样**这单一接口契约，logprob / logit_bias / 语法约束都不保证可达。这不是缺陷假设，而是**部署现实**。

在此现实下，价值不在把某个核心的裸能力刷到极致（那是模型厂的事），而在把既有核心搭成**可闭环、可评测（reward-guided）**的系统，针对性提升其**外挂能力**。三类外挂按粒度区分——知识（通用事实）、记忆（特定实例召回）、技能（任务模板注册）；本提案聚焦**知识子系统**，记忆 / 技能为同级外挂、暂缓。核心价值：无需触碰核心权重即可在知识依赖型语音任务上兑现效果，且**最小接口设计**便于向闭源 API 迁移。本地冻结核心是**科学载具**（严格可复现），闭源可迁移性是**价值主张**（跨核心冒烟作证）。

**术语纪律（C-5）**：全程使用 **"零权重、零核心结构改动；外挂系统组件另加"**——RDU 明显新增了检索、触发、知识卡、两遍/多遍采样与 KB 等外挂系统结构，绝不表述为裸"零结构改动"。可迁移性一律表述为 **"最小接口设计 + 跨核心冒烟作证"**，绝不表述为"天然向任意闭源 API 迁移"。**对外身份术语统一为 weight-frozen reward-guided inference-time optimization（G0）**。

**"知识依赖型语音任务"范围界定**：任务的正确输出依赖于**音频本身未携带、须由外部证据补足**的信息——语音知识问答（heysquad / SQuAD-zh / squtr，答案在语料而非音频）、口语意图/槽位理解（SLURP，域知识约束槽值）、实体/专名密集转写（is21_deep_bias / AISHELL-NER，稀词与命名实体须由偏置库补足）。纯声学任务（说话人、情感）不在范围。**头条主张进一步限定为"头空合格的知识依赖型语音任务"**（§9.4 资格规则；responder-cohort 选择在头条范围中如实声明，§9.4/§9.5）。

### 1.2 为什么是前端知识校正，而非后端融合

training-free 的主战场在**前端**——组织与校正输入侧多模态知识体系。**后端**（重排序 / 验证器）不立为独立研究方向，只作**数据集无关的标准信号供给**（§10、附录 C），且这些输出侧信号正是 §4 selector 算子的 proxy-reward 来源。三条理由：(1) 后融合自由改写在强、低-WER 冻结核心上普遍中性到有害（LIR-ASR arXiv:2509.15095，2025-09，Whisper-large-v3 上去规则约束令 LLM 自由改写使 CER/WER 由 2.89/5.23 恶化到 6.62/9.27；arXiv:2501.15310，2025-01 强核心经纠错 WER 不降反升）；(2) 前端注入受核心生成能力封顶但不破坏它，闭源 API 原生可达；(3) 后端唯一可移植的 training-free 原语（受约束选择 + 误差去相关信号）保留为 selector 的 proxy-reward、发现段触发与使用段信任标定，换数据集不换信号定义。

**基线哲学反转**：不要求先把核心调到极致再测知识系统。基线 = **裸核心标准用法**；long-context 全塞入、own-ASR 朴素级联从"基线"改编入**系统复杂度阶梯**。

### 1.3 组织框架：检索–发现–使用（RDU）

- **检索 Retrieve**：给定语音输入，如何在异构键空间找候选证据——核心难点是**匹配几何**（§6）；
- **发现 Discover**：何时需要知识、需哪类、检回候选里哪些真相关——一个**描述性**测量子系统（§7）；
- **使用 Use**：知识以何形态进入模型、模型采纳多少——版本化标准知识卡 + 信任标定（§8）。

RDU 的三段被 §4 的 reward-guided 算子外包一层：对同一输入采样 K 条完整 RDU 轨迹，以可部署 proxy-reward 选择——这是本工作的 TFRL 身份所在。

### 1.4 Stage-1 先验证据（严格 ledger-conformant；directional 一律 Stage-1 假设级）

- **递送/内容供给方向性最大杠杆（C-MINDS-V2，directional）**：clean MInDS-14 factorial 上 cards-only +0.246、instruction+cards +0.262；**纯 zero-shot 元指令回归 −0.245 [−.286, −.201]**——发现段必须供给**内容**，只给元指令反破坏行为。**caveat（务必随引）**：这是 composite candidate-card treatment，含 ~3% card-text/eval-transcript 表面重叠（+3/107 命中），**不能归因于卡 schema 本身**；仅作 §8 递送对比的**方向性 motivation**，非"标准卡 schema 已证"。
- **采纳固执（unverified observation，未 mint）**：冲突时模型约 24% 采纳外部知识的观察在 claim ledger 中**无对应条目**（原 C-KEEP 不存在、工件溯源未完成）。该数字**不作设计依据**，仅记为"未核实观察、待 mint"；使用段信任标定动机改由 C-MINDS-V2 的"内容供给主导"承载。
- **proxy 标定线（C-ASR-V2，directional，已退出系统设计）**：存量池离线选择器电池中 logprob@8 在 clean/snr5 两条件 corpus-WER 方向一致（clean +0.0094 [.0034,.0165]、snr5 +0.0081 [.0005,.0161]），**但在真实发现网格（每条件 16 比较）全家族 Holm 校正后两条件均不存活**——directional，非独立复现。该信号依赖逐 token logprob，**已退出系统设计**（闭源不保证可达），仅留 ledger 作工程诊断。
- **基线库（C-BASELINES，directional inventory）**：dev 基线来自冻结 locked-group 工件，但 provenance 记 `git_dirty=true` 且 engine build / dataset revision / manifest hash 为空，dev/test 跨波有重叠——**全部维持 directional inventory 等级**，不具确证级 provenance（§9.1 基线表 provenance caveat）。

> 历史失败教训（C-T7 的"召回优先"效应方向）**仅**保留于**失败史附录 D**，`invalid`（信息泄漏语境），**绝不作正向动机**；"召回优先"在本版是一条**待检验假设**，其操作化约束由发现段（§7）在清白管线上重新独立建立。

---

## 2. 相关工作、新颖性矩阵与可守边界

**引用新鲜度规则（续17）**：每条方向影响型主张由 ≥1 篇 ≥2025-01 一手来源锚定；较早著作仅在带显式角色标签时引用——**[谱系]** / **[标准]** / **[已弃用]**。

**上下文偏置分水岭**：六族传统偏置技术（shallow fusion [谱系]、CLAS [谱系]、trie 约束解码 arXiv:2508.17796、TCPGen [已弃用]、contextual adapters [已弃用]、CTC-WS [已弃用]）在 chat-API omni 下无一原样存活，分水岭 = **解码器内部访问**。**检索式注入是文献收敛的替代形态**（BR-ASR arXiv:2505.19179；RECAST EMNLP2025 findings.203；Hotword-RL arXiv:2512.21828；Locate-and-Focus arXiv:2507.18263 ACL2025），两读数：top-2 甜点、N≥100 灾难幻觉；**赢家检索器都是专训对比检索器，off-the-shelf CLAP 词汇键已死（GLAP 论文报告 CLAP 词汇键 R@1≈0.1——文献比较，非我方 in-house 复现，L4-3）**。

### 2.1 新颖性矩阵（6 新邻 + 3 已引邻）

> **矩阵读法（L5-03，非"对方缺什么"清单）**：第三列不是单纯罗列近邻的缺失，而是标注**我方相对该工作确立的、可度量的 delta**（配下方 companion 段落给出精确定位）。deficit-only 表是最弱的 novelty 辩护；此处每行的落点是一个**可测端点**而非"对方没有 X"。

| 工作 | 有什么 | 我方确立的可度量 delta（精确定位，非仅列缺失） |
|---|---|---|
| **WavRAG**（ACL 2025，2025.acl-long.613） | 原生 audio 检索 + text/audio 混合 KB，报相对 ASR-text pipeline 的速度优势 | 无严格黑盒契约、无 modality×form×delivery 因子分解、无 proxy-reward selector 净增益与 ρ |
| **VoxRAG**（MAGMaR 2025，2025.magmar-1.3） | 模块化、免转写 spoken-QA RAG（CLAP+FAISS） | 组件非全冻结论证、无因子归因、无 selector 算子；用 off-the-shelf CLAP（GLAP 报告其词汇键 R@1≈0.1、已死——文献来源，非我方 in-house 证明；无 ledger 条目故不作独立设计依据，L4-3） |
| **PlanRAG-Audio**（Findings ACL 2026，2026.findings-acl.1304） | 规划 modality/time-span 后从结构化 text/audio DB 检索，效率为核心结果，系统叙事最接近 D-R-U | 无 training-free/黑盒承诺、无独立构建 KB 泄漏边界、无 ρ 与因子化贡献测量 |
| **Adaptive Retrieval Without Self-Knowledge**（ACL 2025，2025.acl-long.319） | 35 个 adaptive-retrieval 方法统一效率/性能评估；轻不确定度常胜复杂 pipeline | 非语音/omni、非黑盒外挂、无生成桥接匹配几何、无 selector；作我方发现段的**强效率对照参照** |
| **RAG-E**（arXiv:2601.21803） | retriever–generator 交互/失配的实证分解 | 佐证 §7 归因为**描述性 taxonomy 非加法恒等式**；非语音、无黑盒契约 |
| **Decomposing Retrieval Failures**（arXiv:2602.17981） | 检索失败因素非简单加法 | 同上，用以否定加法恒等式；无 modality-bridge / selector |
| **BR-ASR**（arXiv:2505.19179，已引） | 专训语音偏置检索近邻 | 需训练检索器；我方走零训练生成桥接反制 |
| **RECAST**（Findings EMNLP 2025，已引） | 对 decoder states 做对比训练检索 | 依赖训练 + 内部状态；违反我方黑盒契约 |
| **HyDE**（arXiv:2212.10496 [谱系]，已引） | a2a 假想答案桥 | **其自陈 caveat**：假想文档可含虚假细节，有效性依赖 dense bottleneck 过滤——我方 a2a 臂必带此幻觉风险标注 |

**精确定位 companion（L5-03，逐近邻的可测 delta，非缺失罗列）**：面对 WavRAG/VoxRAG/PlanRAG-Audio 已压窄的 audio-RAG+组织新颖空间，我方的可守 delta 是**两个可度量端点**，任一近邻都未同时给出：**(1) 严格黑盒契约下 modality×form×delivery 的因子分解端点**——不是"也做 audio RAG"，而是在**同一独立冻结 embedder / 等内容递送**下把三轴各自的净贡献分离测量（S1a/S1b/S2 的受控设计，§6.2/§8.2）；**(2) selector 的 ρ 实现率端点**——ρ 刻画**等 K selector 相对 oracle 头空实现出的比例**，其分子/分母**同以（单样本、预算不匹配的）greedy 为低端锚** `ρ=(R_selector−R_greedy)/(R_oracle−R_greedy)`（§9.7）；**故 ρ 本身不表述为"在严格同 K 预算下报告"——只有 R_selector 与 R_oracle 共享 K，greedy 锚不匹配预算（L4-4）**。等预算超越性（selector vs random/MBR）与绝对增量在同 K 预算下另报。把"reward-guided 选择兑现了多少 oracle 头空"量化为一个数，而近邻工作以效率为核心结果、无此可部署 proxy-reward 选择量。**效果是唯一最终裁判**；我方不以机制新颖立论，而以"在此狭窄合取下这两个端点上取得可复算的效果"立论。

### 2.2 可守住的新颖性边界（狭窄合取）

WavRAG / VoxRAG / PlanRAG-Audio 已把 audio-RAG + 系统组织的新颖空间压窄；**单说"audio RAG + planning/RDU + frozen components"不足以构成博士级贡献**。可守、可检验的空白是一个**狭窄合取**——以下五者同时成立者，上述任一近邻均不具备：

> **严格黑盒契约（音频/文本进、文本出、多采样）× 全部组件冻结 × 知识库与评估标注独立构建（§6.4 全语料 + qrels 只入评分）× 贡献的因子化测量（modality bridge × form bridge × delivery）× proxy-reward 轨迹选择算子（等预算下绝对增量 + ρ 实现率）。**

**效果是唯一最终裁判**；我方不主张任一段机制新颖，而主张在此狭窄合取下取得效果并把 oracle 头空实现出可靠比例。可守贡献的载荷点：(1) 严格黑盒下 modality×form×delivery 因果分解；(2) q2q/HyDE 对**全语料**音频查询检索的稳定净增益；(3) proxy selector 在**等预算**下稳定实现 oracle 头空；(4) proxy 失效 / self-consistent error / reward hacking / N\* 的严谨边界；(5) 跨核心/数据集复制。若 selector 最终不优于 MBR/random，这仍是有价值的**负结果**（以"为何 label-free proxy 无法实现头空"为中心），不靠"TFRL"命名冒充贡献。

---

## 3. 两个可分别裁定的确证问题（Two separately adjudicated confirmatory questions）

本版把研究收成**两个可分别裁定的（separately adjudicated）**确证问题。**"可分别裁定"不等于"统计独立/机制解耦"**：Q-A（H_SYS_FOCUS）与 Q-B（H_SEL_ABS_DELTA）**共用同一焦点集 `<FOCUS>`、同处一个 Holm 家族（m=6）**，且 Q-B 的 selector 是 Q-A 所评 RDU 系统内的一个组件（弱/失败的 RDU 会同时压低两者）——故不作"两个真正独立"表述，只主张二者**各自裁定、互不混淆**。Q-A 不以裸核心为唯一 load-bearing 对照（复杂度阶梯并列裁定）；Q-B 不混入 K=1 成本臂（K=1 是低成本基线，在等预算族之外）。

### 3.1 Q-A：系统效果（SYSTEM effect，全语料、头空合格头条）

> 在**官方全语料 / query-independent corpus**（§6.4）、严格 core-black-box、所有外部组件冻结使用的条件下，以冻结 Qwen3-Omni-30B 为核心加装前端 RDU 知识子系统，能否在**头空合格的知识依赖型语音任务**上，对**裸核心标准用法基线**取得 **≥10% 错误率相对下降**、全家族校正后统计可靠、边界清白的效果提升？

- **Estimand**：最优 RDU 配置相对裸基线的**错误率相对下降**（单尺度，error = 1 − acc 换算）；**确证操作化（PF2）**：以在**冻结裸基线**上换算得的**固定绝对当量 margin `SESOI_abs`** 检验（等价于"在冻结基线上 ≥10% 相对下降"），非在确证半区逐-bootstrap 取比率。**如实标注分歧**：当确证半区裸误差 ≠ 冻结 dev 裸误差时，固定绝对 margin 与"10% 相对"不再重合——确证裸误差**高于**冻结值时该检验对"10% 相对"主张偏松（anti-conservative），**低于**时偏保守；故另报以**确证半区裸误差为分母（带预注册下限）**的比率 estimand 作敏感性，二者背离在 §9.8 provenance 一并披露。
- **总体范围（S-2）**：头条限定为**头空合格数据集**（§9.4 资格规则）；对不合格集不主张头条效果；焦点/复制集在 M2 由 eligibility-split 选出，**responder-cohort 选择在头条范围内如实声明**。
- **主聚合（S-5）**：**一个焦点数据集为 primary + 若干 replication 集带 no-harm 门**，**不以跨异构任务族的固定效应池化作 primary**；如展示任何聚合，报告异质性并要求 ≥2 预定任务族方向一致。
- **复杂度阶梯并列裁定**：①long-context 全塞入；②own-ASR 朴素级联（modality-bridge 对照，WER 作协变量）；③RDU 完整配置。头条比对裸基线；阶梯净增益（"组织智慧"）**单独裁定**，若仅 Q-A 达标而阶梯净增益 null → 系统有效但归因于"知识供给本身"，如实降级叙事、不 kill Q-A。

### 3.2 Q-B：selector 效果（TFRL 身份锚；等预算超越性原子 + 预算不匹配部署价值 co-primary；ρ 机制量）

> 给定**完全相同的 K 条**可部署 rewrite–retrieve–deliver–answer 轨迹，用**预注册、可部署、输出侧 proxy-reward（Û）**选择其一；这个 Û-selector 相对**等预算对照（K-candidate random / MBR）**，能否实现**正的绝对任务效用增量**，并把 oracle 候选头空实现出可靠比例？

- **等预算对照族（硬约束，G5）**：`K-candidate random`（K 条随机取一）/ `K-candidate MBR`（medoid）与 selector **严格匹配同一 K 生成预算与采样配置**。三者构成等预算 selector 族。
- **K=1 单次 RDU = 低成本系统基线（G5，等预算族之外）**：K=1 与 K>1 在生成预算上不可能严格相同，故 **K=1 永久标为"低成本系统基线"、绝不标"等预算"**；它作描述性成本对照报告，不进等预算 selector 族的确证判定。
- **Co-primary（绝对增量，G4）**：**Û-selector 的绝对任务效用增量**（R_selector − R_greedy，任务效用尺度）为 co-primary，与等预算超越性并列。**如实披露（F1）**：此原子是**有意的预算不匹配（budget-UNMATCHED）部署价值指标**——把"带 K 预算的系统"对照**RDU 全管线的单次 temp-0 缺省部署**（greedy = 与 selector 同一 RDU 配置、仅单样本零额外采样的部署缺省锚点；**区别于 §9.2 的裸核心基线——裸核心不含 RDU，R_greedy 含完整 RDU 只跑一遍**，F2），与等预算超越性原子（selector vs random/MBR，§4.4）目的不同、不同尺度并列。之所以 selector-vs-greedy 可进确证而 selector-vs-K=1 只作描述性：**greedy 是唯一的规范部署缺省（零额外采样）**，而 **K=1 只是一个任意的单次随机采样**、无规范地位（G5）；故 K=1 恒在等预算族之外只作低成本基线，而 greedy 作为部署缺省锚点进入 co-primary。primary 家族因此**同时含 matched（vs random/MBR）与 mismatched（vs greedy）两类对照，此处明确标注、不隐瞒**。**Q-B 最小效应量（L2-01/PF1）**：selector 绝对增量与等预算超越两类原子**各预注册一个数值 SESOI（pre-M2 冻结常数——owner 于 §14 签字位设定数值、先于任何 exploration/dev 运行，一经设定在任何 selector dev 观测作出后绝不新选或回改；与 Q-A 相对 SESOI 同属 pre-M2 冻结类，杜绝 identity-gating SESOI 被 selector dev 效应量 retro-fit，PF4）——`Q_B_SESOI_abs`（绝对增量，task-utility 尺度）与 `Q_B_SESOI_sup`（等预算超越，normalized-error 尺度）**，两原子的判据都要求 CI 界越过其各自 SESOI（非仅越过 point-zero null；等预算超越原子的 point-zero 口子已在附录 A 同步堵上，PF1）；**承诺显著但平凡（低于对应 Q-B-SESOI）的 selector 增量/超越绝不报为"selector/TFRL 身份已确证"**，杜绝 point-zero null 下任意小显著冒充身份成立。
- **Secondary-mechanistic（ρ，G4 + 博导 §4.4）**：**ρ = (R_selector − R_greedy)/(R_oracle − R_greedy)**，selector realization rate，**仅作机制量**，报告口径见 §9.7（aggregate-ratio、联合 cluster bootstrap、预注册分母下限、Fieller/percentile 敏感性），**不进 primary Holm 家族分母**。
- **身份声明**：Q-B 使本工作成为 thesis 定义的 **weight-frozen reward-guided inference-time optimization**（TFRL），而非"因为没训练就自动算 RL"。算子定义见 §4；同对象 Lean 定理（票 #27）见 §10.2。**机制/身份归因仅由等预算原子承载（L4-2）**：selector/TFRL **机制身份**只由等预算 vs random/MBR 两原子确证——它们才把"argmax-Û 选择技巧"从"raw best-of-K 覆盖增益"中隔离；H_SEL_ABS_DELTA（vs greedy，预算不匹配）是**部署价值**端点（G4 定为 co-primary），**单独不足以支撑机制主张**，正向 selector-vs-greedy 只报为"花 K 预算相对 greedy 的部署收益"、绝不读作"选择技巧已证"。
- **单集范围如实声明（S-5）**：Q-B 的三原子（H_SEL_ABS_DELTA / vs random / vs MBR）**全部只在单一焦点集 `<FOCUS>` 上确证**（primary m=6 固定，G3，不新增原子）；Q-A 有焦点 + 2 复制 no-harm 门，Q-B **无跨集复制**。故**被确证的 TFRL/selector 身份主张显式限定于该单一焦点集，跨数据集泛化明确推迟**（作 M5 后续 development 迭代或独立复制），**绝不把 selector 身份读成已跨集成立**。

### 3.3 五个次级科学点（S1a / S1b / S2 / S3 / S4，**降为方向性探索、无 Holm 声明**）

按博导复审裁决，**次级族整体降为 directional-only 探索层排序**（各自方向性报告、正负皆入 ledger）；**不做任何 Holm 家族存活声明、不并入 primary 分母**（§9.5、附录 A）：

- **S1a（同形式冻结匹配，form-bridge 假设）**：q2q vs q2a（同一冻结 embedder）检索质量（R@k/nDCG）+ 端到端贡献。**待检验的 form-bridge 假设，绝不预设"同分布"**（I-4）。
- **S1b（生成桥接 vs 专训检索器）**：最优生成桥接（建库 q2q + 查询 a2a/HyDE）能否零训练追平/超越专训冻结检索器（GLAP/nemotron）？**预注册承诺**：若须训练薄投影才达标，如实报 training-free 负结果，绝不静默替换。
- **S2（递送主效应，等内容 A/B）**：见 §8.2，**完全等内容 A/B**（同事实/示例/token 预算/位置，只变 schema/turn 结构）。
- **S3（发现段·效果优先触发研究，成本仅描述）**：见 §7，**轻量 1×3 预算匹配**（同采样预算下 never/always/triggered），**效果**判定；成本仅描述性计账，**不设任何成本成功门**（R1）。
- **S4（上下文实体偏置，构念独立臂）**：见 §9.6，**三构念拆分**，作构念相异的独立研究臂，非"共同机制"证据（C-6）。

---

## 4. Reward-guided 轨迹选择算子（Path B，TFRL 身份核心；U/Û 记号）

本节定义 §3.2 Q-B 的算子，与 Python 实现、Lean 定理（#27）**同指一物**。**记号纪律（F′-4/G4）**：真任务效用写 **U**（gold 仅在评估时可见），可部署 proxy 写 **Û**（consistency / cross-source-agreement / confidence）；**selector = argmax Û**、**oracle = argmax U**、**regret = U(argmax U) − U(argmax Û)**。**"verifiable" 一词只保留给规则/单测/exact-match 等确定性验证器，且保留词纪律扩及名词"验证器/verifier"——不执行确定性 correctness checker 的任何信号一律不得命名为"验证器"（L4-1）**，本算子的三种信号是 **label-free proxy reward**，不读 gold、不执行确定性 correctness checker。

### 4.1 动作空间与策略（frozen sampling）

- **动作空间 A**：给定输入 x，一条轨迹 τ = ⟨查询构造(改写) → 检索 → 递送(知识卡) → 作答⟩。每环节仅调用黑盒接口（音频/文本进、文本出、多采样），不触碰权重、不访问解码器内部。
- **策略 π（冻结采样）**：冻结核心以温度 T 采样生成 K 条轨迹 {τ₁…τ_K}。策略 = 冻结模型的采样分布本身；**不训练、不更新任何参数**。这是"training-free"的严格含义——搜索的是模型自身行为，不是模型权重。

### 4.2 proxy reward Û（可部署、输出侧、label-free，**永不读 gold**）

Û(τ) 只用系统契约内的输出侧信号：

- **自一致性一致率**：K 条轨迹答案间的一致度（逐 K-type 等价定义，§7.1）；
- **跨源一致度 δ_corr（cross-source-agreement；非"验证器"——它不执行任何 correctness checker，L4-1）**：第二个 context-differentiated 冻结 omni（同权重、异 system-prompt）对答案打分的跨源一致；**"cross-source" 在此仅指 context-differentiated（同权重、异 prompt），非 weight-independent——是同一模型问两次、非两个独立系统（L4-F3-minor）；任何 source-diversity 收益是 §4.5/§10 要求的 MEASURED δ_corr（实测误差去相关），非由命名假定独立性**；
- **答案级置信引出**：追问模型自评可答性/置信。

三者均可单用或线性组合，权重于 M2 探索层 dev 标定后冻结、不在确证层调；**该标定的检索必须跑在全语料/query-independent 语料上（L3-F3，§6.4）——绝不在 qrels-conditioned 310 上标定 selector 权重再前向转入确证**。**文献风险如实标注**：self-consistent errors 可跨采样稳定（Too Consistent to Detect，EMNLP2025 main.238）；confidence-weighted consistency 可能有用但同题内 calibration 特殊（CISC，Findings-ACL2025 1030，最 calibrated 者未必最宜 within-question 选择）；imperfect reward 下扩大 K 会 reward hacking（Best-of-N inference-time alignment，arXiv:2503.21878）。故 Û 是**不确定度 proxy**，其可用性由 §4.3 三诊断实测，不由命名假定。

### 4.3 三件 proxy 诊断（预注册为探索性测量，G4）

- **within-question rank AUROC**：Û 在同一问题内对候选排序 U 的能力（pairwise accuracy / AUROC），**分离于跨问题 calibration/Brier/ECE**；
- **self-consistent-error 压力子集**：在"错误跨采样稳定"的子集上测 selector 的失效率；
- **Goodhart 曲线**：K 增大时**真效用 U 与 proxy 效用 Û 的分歧曲线**（是否出现 U 先升后降的 over-optimization）。

### 4.4 选择规则、停止规则与预算 N\*

- **选择规则（selector）**：τ̂ = argmax_τ Û(τ)（或 Û 加权）。这是 ρ 中的 R_selector。**记号绑定全程一致：τ̂ = selector = argmax Û、τ\* = oracle = argmax U**（同 §10.2、§4.5、§14），二者不可互换。
- **停止规则 / 预算 cap N\***：K ≤ N\*（预算上限）；若一致率 ≥ 预注册阈值可提前停。N\* 由 §9 的 1 真格成本标定确定并冻结。**N\* 是预算上限，不是收敛条件**（§10.2）。
- **等预算 selector 族**：random / MBR / selector 严格匹配同一 K 预算与采样配置，杜绝"selector 多采样 vs 对照单采样"混杂；**K=1 低成本基线在此族之外**（G5）。
- **ρ 的三个锚**：R_greedy = 单次 greedy（**规范的零额外算力部署缺省锚点**；故 co-primary 的 selector−greedy 是**有意预算不匹配的部署价值对照**，F1）；R_oracle = 按 gold 选最优（**仅上界、永久不可部署**）；R_selector = 上述可部署 selector。**ρ 只用任务效用 U 计算，绝不用 proxy 分数**（G4）。**注意区分**：selector vs greedy（co-primary，预算不匹配，对照部署缺省）与 selector vs random/MBR（等预算超越性，预算匹配）目的不同，见 §3.2 F1 披露。

### 4.5 与理论轨（#27）的同对象绑定

Lean 票 #27 形式化的正是本算子：**无约束失败 + 有约束收敛**——无 calibrated proxy 误差界（ε）与预算 cap（N\*）时，selector 在 imperfect proxy 下随 K 增大可被 reward hacking / Goodhart 支配（§4.3 曲线），regret 不趋零、可劣于随机；在 proxy 误差 ≤ ε 且预算 ≤ N\* 时给正确性 + 有限样本 regret 界（§10.2 首定理 U(τ\*)−U(τ̂) ≤ 2ε）。**Python↔Lean 逐例一致性测试**令实现的 selector 与定理算子逐例吻合；闭合前不作"Lean 已证我方 selector 收敛"的任何论文句。

---

## 5. 系统接口契约与组件（Interface Contract）

### 5.1 唯一硬契约（无 tier 划分）

只用任何闭源 API 都保证暴露的接口：**音频/文本输入、文本输出、多次采样**。发现段触发与 selector proxy-reward 一律用**输出侧信号**（§4.2、§7）。logprob 触发、`logit_bias`、语法硬约束**不是系统组件**（依赖解码器内部访问，闭源不保证可达）。本地冻结核心亦仅经黑盒接口使用，llama.cpp 白盒能力仅限工程诊断。

### 5.2 检索匹配特征 = 独立冻结 embedder 的语音向量（R2）

**为什么是语音向量而非核心裸信号（一段诚实回答）**：检索匹配在数学上需要一个**嵌入空间**——把语音查询与被存证据映到可算相似度的向量。该嵌入由**独立冻结 embedder**（GLAP / omni-embed-nemotron）产生，它是一个**外挂系统组件，如同 KB 本身**：契约约束的是我方对**核心 API** 的要求，**不是**系统里能包含哪些外部冻结组件。故音频查询的检索输入特征是语音向量、由外挂 embedder 得出，**不违反黑盒契约**。真正"死掉"的只是——把**核心自身的 2048d 隐态**当作**可部署检索键**：那需要核心暴露内部隐藏态，闭源 API 不保证可得。

### 5.3 组件表（全冻结使用；选型由 dev 效果决定并如实报告）

| 组件 | 角色 | 冻结使用标注 | 一手锚 |
|---|---|---|---|
| **GLAP** | 检索键嵌入（可部署主力，独立冻结 embedder） | trained-frozen；冻结使用、非 by-construction（LLMLingua-2 先例 [标准] 披露） | GLAP arXiv:2506.11350（2025-06，多语种语音内容检索，CLAP 无法胜任） |
| **omni-embed-nemotron** | 检索键嵌入（trained-frozen 天花板对照） | 冻结使用对照；非对称 `encode_document`；NC license 仅研究用（商业价值受限，如实标注） | Omni-Embed-Nemotron arXiv:2510.03458（2025-10，NVIDIA） |
| **own-ASR→文本级联** | **modality-bridge 对照臂**（阶梯②） | 边界清白（own-ASR 转写部署可得，非 gold）；cascade WER 作协变量 | 附录 B |
| **qwen3-omni-own 2048d 隐态** | **白盒诊断臂（demoted）** | **排除于一切 portable/deployable 头条主张**；只作白盒诊断 | LCO-Embedding arXiv:2510.11693（2025-10）+ MAEB arXiv:2602.16008（均分 ~50–52%，未饱和） |
| **专化侧翼** | 实体粒度检索器 + carrier-sentence 合成键 | 冻结使用；中文用学习跨模态检索器 | 附录 B |

> **对 W4 的显式声明**：核心 2048d 隐态降为白盒诊断臂，**不触碰 W4 叙事逻辑**——W4 是研究 omni **自身嵌入空间**的独立工作（§12），本降级只关乎 W1 的**可部署检索键**选择。

### 5.4 科学载具 vs 可迁移性（C-5 软化）

**科学载具** = Qwen3-Omni-30B Q8_0 GGUF via llama.cpp（`-ngl 28`，resident `llama-server`），数据/代码/种子全 pin；**确证脚本一旦（M4 之后）运行，其结果将在此载具上逐字节复现（L4-5：本版尚无确证结果，措辞为将来时）**。本系统只经黑盒接口消费核心，故本地核心上成立的系统级结论其输入面与闭源 API 完全一致。**可迁移性表述**：**最小接口设计 + 跨核心迁移冒烟**（第二核心 MERaLiON-2 或一闭源 API 上 1–2 集轻验，作证据、**非门控项**）；**绝不表述为"天然向任意闭源 API 迁移"**。

---

## 6. 检索段：匹配几何与语料/KB 独立性

### 6.1 匹配对象与递送对象分离

检索段深层难点是**匹配几何**：语音查询 q（问题分布）与被存证据 d（内容分布）**处于不同形态**。裁定：**匹配对象（key）与递送对象（value）分离**——value = 证据内容恒定；key = 最大化匹配信号的任意形态，含问题形态。

### 6.2 三态匹配几何（q2a / q2q / a2a，形式桥接均为待检验假设）

| regime | 键形态 | **假设**（待检验，I-4） | 实现（黑盒契约合法） |
|---|---|---|---|
| **q2a** | 键=文档内容 | 跨形态弱关联（基线假设） | 冻结 embedder 直接编码文档内容 |
| **q2q** | 键=为文档合成的伪问题 | 更强同形式匹配（**form-bridge 假设**） | 建库离线：冻结核心为每篇证据合成伪问题（doc2query 式 [谱系]）；语音查询即问题 |
| **a2a** | 键=查询的假想答案 | 更强同形式匹配（含 HyDE 幻觉风险） | 查询时：冻结核心为查询生成假想答案（HyDE arXiv:2212.10496 [谱系]，含其自陈"假想文档可含虚假细节"caveat） |

**明确措辞（I-4）**：q2q/a2a **只桥接问句/答句的话语形式，不等于桥接模态或分布相同**；是否真提升匹配是 S1a/S1b 要检验的。受控设计把三轴分开：**modality bridge**（独立-embedder 语音向量 vs own-ASR 文本）× **form bridge**（raw-doc/q2a vs q2q vs HyDE/a2a）× **delivery**（flat vs 等内容卡）。

### 6.3 零训练路线与 S1 分解

生成桥接两条路线都**只调黑盒 `generate`**：建库侧 q2q（离线一次性、成本摊薄）+ 查询侧 a2a（每查询一次生成）。S1a = 同形式冻结匹配（q2q vs q2a，同一 embedder）；S1b = 生成桥接（较优者）vs 专训冻结检索器（GLAP/nemotron）。**实体粒度**（S4）用**合成 carrier-sentence 键**（键落在与 utterance 同形态），同音精度由 §9.6 单独诊断。

### 6.4 语料与 KB 独立性（F′-3 / G1 结构性处置）

**确证检索语料 = 官方全语料，qrels 只入评分。** 这是本轮最重的实现级修复。

- **全语料要求**：squtr 确证检索使用**官方全语料**（FiQA，**57,638 docs**，G1 裁定的确证语料）；**若改用与 qrels 完全无关的 query-independent 固定 subset，则该 subset 必须作为一个具名 corpus 自身被 pin（其own `content_hash` + `doc_count`），且非 qrels-conditioned 310——它不是"全语料的替身"而是另一个被注册的语料对象**。**qrels 只在评分过程读取，绝不用于构建候选语料/索引/prompt/候选范围**。
- **硬前置门（L3-01，运行期强制；参数化 per registered corpus，L4-F1）**：确证（及 eligibility-split，见 §9.4/L3-05）打分前**断言所载语料 `content_hash == 该数据集预注册 corpus-lock hash` 且 `doc_count == 该数据集预注册 corpus-lock doc_count`**（**参数化断言**——对 squtr/FiQA 该 count 即 **57,638**；对 heysquad/SQuAD-zh 等各用其自身注册语料的 hash+count），不符即 **fail-closed（P0，绝不静默降级到 310 或 per-item context）**。**gate 不再把 57,638 硬编码为唯一常数**（否则与上一 bullet 允许的 query-independent subset 及 L3-02 每集各自开放语料自相矛盾，L4-F1）——它比对的是"**whichever corpus was registered**"的 hash+count 对。**该 corpus-lock 常量当前不在 `docs/datasets.lock.json`——squtr/FiQA 全语料及 is21_deep_bias / AISHELL-NER / SQuAD-zh 均不在冻结 28 集清单内（L3-BLK-1 已核实为真）**；故 **M1 前置交付项 = 把这些焦点/资格候选语料 pin 进 `docs/datasets.lock.json`（或具名 corpus-lock 工件），每条 pin 须锚定一个**上游第三方可验证来源**：HF dataset revision（或等价上游快照）+ **上游发布的 corpus checksum/doc_count**，而非仅一个团队自算常数（L3-F4——自算 hash 只证 replayability=self-pinned，不证 officialness/query-independence；上游 revision + 公开 checksum 才提供独立锚）**；在该 pin 落定前 L3-01 为**未满足门**、squtr 全语料 build 不得进入 eligibility/confirmatory（§13.4）。该 hash+count+上游 revision 写入 §9.8 确证 provenance 块。**`query_independent_corpus` 轴的 PASS 以此 hash 相等 + 上游锚存在为条件**，而非以 build-mode 标志断言——无 hash 匹配即该轴 `NOT_EVALUATED`。这堵住 F′-3 原样复发（"CLEAN 却跑在 qrels-conditioned 子集上"）的口子。
- **每个进 primary 家族的知识-QA 集都须自带具名开放语料（L3-02）**：**不止 squtr**——凡进 primary/eligibility 的知识-QA 集（heysquad、SQuAD-zh 等）都必须**具名其共享开放语料及其 hash**，并由 `object_correct` + `query_independent_corpus` 核验 KB 值是**该共享语料里检索到的文档**、**非该 item 自带的 gold 段落**（SQuAD 族天然 per-item context = answer-in-own-KB，正是 C-T7 无效模式，heysquad 曾据此产生无效 +51.7pp）。**在其开放语料被定义并审计通过前，heysquad/SQuAD-zh 不得进入 eligibility/primary**；`answer_presence_expected` 只在语料确为开放共享语料时才成立，绝不用于给 answer-in-own-context 放行。
- **310 库永久降级 + 禁入任何前向选择（L3-F3）**：当前 310-doc 工件（110 个 test-qrels 全部正例 + 200 干扰，正例密度较全语料抬升约 ×186）**永久标 `qrels-conditioned controlled mini-corpus`，只作 DEV smoke，绝不进头条**。**并明确：任何"选定后冻结进确证"的配置/超参/proxy-reward 权重选择（RDU config、检索 k/阈值、卡 schema、§4.2 selector 权重）绝不得在 310 上做**——凡其 selected config 会前向转入 confirmatory 的 exploration-dev 检索运行，**必须跑在全语料/query-independent 固定语料（同 §6.4，记同一 `corpus_content_hash`）**上；310 仅限**不选择任何东西的纯管线冒烟（plumbing smoke）**。否则在 qrels-conditioned 抬升密度下选出的 config 会把 leakage-shaped selection object 前向转入确证（确证语料虽清白，selection object 已被污染）。
- **q2q 建库边界**：允许 q2q 离线生成，但**只从全语料文档生成**；q2q generator **不见 test queries/qrels**；corpus build hash 与 q2q generation hash 分开记录。
- **概念澄清**：在正规 open-corpus QA/IR 中，"相关文档包含答案"是任务定义，**不应把答案从合法证据里 scrub 掉**；真正的泄漏是**用 test qrels/answers 决定语料构成/索引/prompt/候选范围**。**轴治理声明（open-corpus 类，如 squtr/FiQA——qrels-positive gold 文档 by construction 即语料文档）**：此类 open-corpus QA 由 `label_independent_build`（作 **BUILD-PROCESS 属性**判定：语料/索引/候选池/派生键在不读 eval qrels/answers/queries 下构建）治理，答案 span 在语料中自然出现由 `answer_presence_expected` 判为**预期、非失败**——两轴不再对同一事实给相反判决。**只有数据集自身 fabricate/inject 的 per-item gold-context 构念（如 SQuAD 族 per-item context = answer-in-own-KB）才触发 `label_independent_build` 的 per-item 排除**；开放语料里自然出现的文档与答案 span 绝不触发 fail-closed。
- **五维审计语义（拆分 `CLEAN`）+ 每轴可证伪测试（L3-03，绝非语义标签自证）**：泄漏审计拆为五个独立轴，**每轴给出机器可执行的证伪判据；任一轴的检查输入缺失即该轴输出 `NOT_EVALUATED`（不得默认 CLEAN）**——
  - `object_correct`：**断言 KB 值串 ≠ query 串 且 == 共享语料某文档**（字符串/文档 id 双核对）；
  - `query_independent_corpus`：**语料 `content_hash` == 该数据集预注册 corpus-lock hash 且 `doc_count` == 其预注册 count（L3-01 参数化门，L4-F1；该 corpus-lock 常量为 M1 pin 进 datasets.lock/corpus-lock 并锚定上游第三方 revision + 公开 checksum 的预注册值，L3-BLK-1/L3-F4）**，非 build-mode 标志自证、非团队自算 hash 单独自证；
  - `label_independent_build`：**BUILD-PROCESS 属性——语料/索引构成、候选池、及任何派生键（q2q 伪问题等）均在不读取 eval qrels/answers/queries 的前提下确定**（机器可核：corpus_mode=='full' 或一条 query-independent 构建规则；且建库输入 manifest 按记录的输入文件 hash 断言不含任何 qrels/answers/test-query 路径下的文件）——对输入 hash 集断言，而非口头声称"建库不读标签"；**并（L3-MAJ-3 + L3-F1，内容级、PER-ITEM 而非 set-level）断言（BUILD-PROCESS 违规检查）**：对每一个 eval item，断言其 **dataset-authored 注入 gold-context 文档**（仅限 datasets that fabricate a per-item gold context，如 SQuAD 族 per-item context = answer-in-own-KB，C-T7 无效模式）NOT ∈ 检索候选语料——**此 per-item 排除只针对数据集人造/注入的 per-item gold-context 文档，不针对开放语料里自然出现的文档，更不针对答案 span 的自然出现**（后者是任务定义、由 `answer_presence_expected` 覆盖，非失败）（逐 item 排除，而非"语料集合 ≠ gold 并集/超集"的 set-level 判据——**set-level ≠/⊈ 是可规避的弱检查：语料含 90% gold context + 干扰即 neither equal nor superset、误 PASS，却已 answer-in-own-KB 泄漏 90%，正是 C-T7 partial-coverage 复发**）；**故改为 per-item 命中断言（仅限注入 gold-context 文档）**：任一 item 的**dataset-authored 注入 gold-context 文档**出现在候选语料即该轴 fail-closed（真正的 build-process 违规——语料被 per-item 注入 gold context 污染）；开放语料里自然出现的文档或答案 span 绝不据此 fail-closed。**并独立断言 provenance**：每个具名"共享开放语料"须机器可核其**上游来源 manifest 与 eval 集 context 字段 disjoint**（溯源独立的真正外部语料如 Wikipedia dump / 官方全语料 revision，而非由各 item context 汇成），officialness 不得由 set-check 反推；在此之前 heysquad/SQuAD-zh 不得进 eligibility/primary；**并断言 q2q 生成输入 manifest 不含任何 test-query/transcript 路径（L3-MIN-5，令"q2q generator 不见 test queries"成为机器可核验而非散文承诺）**；
  - `answer_presence_expected`：**内容级预期——答案 SPAN 出现在一个 query-independently built 语料中属预期、永不判为失败**（正规 open-corpus QA 的任务定义，见本节概念澄清）；仅当 `query_independent_corpus` 已 PASS（语料确为开放共享语料）时此预期才适用，"合法证据含答案属预期、非泄漏"；否则不得据此放行 answer-in-own-context；
  - `provenance_complete`：**§9.8 所列 provenance 字段全部非空**，缺一即该轴失败。
- **`NOT_EVALUATED` 规则**：**`n_golds=0` 一律输出 `NOT_EVALUATED`，绝不输出 `CLEAN`**（零 gold 被检查不是"干净"，是"未评估"）。
- **阻断语义（L3-MAJ-2，对称于 L3-01 fail-closed）**：confirmatory 或 eligibility 对象上，**五轴中任一轴返回 `NOT_EVALUATED` 或非 PASS（不限于 query_independent_corpus 与 provenance_complete），即 fail-closed、阻断该对象进入评分**——`object_correct` / `label_independent_build` / `answer_presence_expected` 的 `NOT_EVALUATED` 同样阻断；**非 open-corpus 构念（如 SLURP-intent 的 ontology/intent-slot schema，无 corpus_content_hash/golds-in-corpus）不套用本 open-corpus 五维形审计的整体 fail-closed，而须先定义并通过其构念专属 fail-closed 泄漏门方可进入 primary Holm 家族——见附录 A L3-F5-minor**；绝不允许"未评估"被静默当作非阻断放行（这正是先前"n_golds=0 上审计通过"失败类的根因：先前修正的是 LABEL 不再打印 CLEAN，此处补足"non-PASS 即阻断评分"的语义）。
- **检索报告口径**：Recall@k / nDCG / MRR，端到端另报。

---

## 7. 发现段：描述性测量子系统（Discover）

发现段是**描述性诊断**（非门控、无 pass/fail 阈、无成本成功门）。算法空间显式枚举：恒检索（always）/ 触发式（triggered）/ 从不检索（none），触发信号取自一致性 / 跨源一致度（cross-source-agreement）/ 置信引出。**逐 K-type 等价定义**（预注册）：MCQ/闭式 = exact-match；抽取式 QA = normalized token-F1 ≥0.8；ASR = normalized WER ≤0.1（中文 **CER**，非 word-WER）。

### 7.1 S3 = 轻量 1×3 预算匹配（F′-5 / G5 结构性处置）

**S3 在同一固定采样预算下比较三种检索策略**，杜绝"triggered 多采样 vs always 少采样"的算力混杂：

| 每 item 固定**总生成预算 G**（三臂严格相同） | never | always retrieval | triggered retrieval |
|---|---|---|---|
| **G 遍生成/item（同一 G）** | ✓ G 遍、全程不检索 | ✓ G 遍、全程检索-conditioned | ✓ G 遍：前若干遍作一致率探针 → 低一致率则**在同一 G 预算内**改跑检索-conditioned 生成 |

- **触发信号来源同一 G 预算内**：triggered 的触发决策取自**与 always/never 同一 G 生成预算**里的前若干遍探针得到的一致率（颗粒度 {0,.2,.4,.6,.8,1}），低一致率则把**剩余预算**改为检索-conditioned 生成——**第二遍不是额外一遍，而是从同一 G 预算内支出**。故**三臂消耗的生成采样预算严格相同（都是 G 遍，无任何一臂多得生成）**，效果差异可归因于检索策略本身，**不再有 m+1 的额外生成混杂**（L5-01：原 m+1 表述已撤除）。
- **效果判定（R1）**：**S3 确证性判定只看效果**（never/always/triggered 的效果 TOST/优越性，§9 家族外的探索层），**成本不进任何成功门、不作 Pareto 支配主张**。
- **描述性成本 = 检索调用数（非生成数）**：生成预算三臂相等（都 G 遍）；**唯一的描述性成本差异是检索调用**——triggered 仅在被触发 item 上检索、always 每 item 检索、never 不检索。另报 input+output tokens、wall-clock、GPU-seconds。**效率优化明确推迟至后期，前期不加成本约束**。

### 7.2 三层描述性指标栈

| 层 | 指标 | 定义（C-1/C-2 修订） |
|---|---|---|
| **L1 oracle-treatment responsiveness**（重命名，C-1） | 该 item 对 oracle 注入是否**响应** | **不再称"ground-truth 需求/iff"**；以重复采样估计 **P(Y₁−Y₀>0)**（**重复采样次数与该 estimand 定义于 M2 冻结，PF-L5F4-minor，§13.4**），报告四种潜在结局状态（0→1 benefiter / 1→0 harmed / 1→1 不变 / 0→0 non-responder），**描述性/诊断，永不作可部署标签** |
| **L2 触发响应对照** | 触发器决策 vs L1 responsiveness | TP/FP/FN/TN 对照表（描述性，非硬币） |
| **L3 失效 taxonomy**（C-2，非恒等式） | 漏检 / 失配 / 未采纳三类 | **描述性失败分类，不写"≈ 总缺口"的加法恒等式**（三类可重叠/交互，直接相加会双计数）。**未来识别设计**：顺序 counterfactual 干预（oracle 检索→oracle 排序→oracle 递送→oracle 采纳）或预注册 mediation/Shapley 分解 |

L1–L3 驱动迭代归因（§13.2 back-edge），但**不承载确证判定**。

---

## 8. 使用段：标准知识卡（Use）

### 8.1 版本化知识卡 schema

字段 = content（递送对象）/ source-tag / relevance-signal / usage-directive；schema 版本化（写入 content_hash），跨集不变、只换 content。

### 8.2 S2 = 等内容 A/B（C-3）

**S2 收敛为完全等内容 A/B**：完全相同的事实、示例、token 预算与位置，**只改变 schema / turn 结构**——这样才把"标准卡组织"从"内容多少"中隔离出来（须过 tokenization/position 等值审计）。C-MINDS-V2 **仅作方向性 motivation 并随引 overlap caveat**（§1.4），**不作"标准卡 schema 已证"**。

### 8.3 信任标定（靶点，非一律推高的旋钮）

采纳倾向（"采纳固执"）是使用段靶点，但其 24% 观察为 unverified（§1.4），**不作设计常数**。信任标定目标 = 按证据质量条件化采纳：用输出侧信号（自一致性/跨源一致度/置信引出）估证据可信度，映射到 relevance-signal 字段与 usage-directive 措辞，间接调节采纳（系统不改权重，只改递送形态与指令强度）。

---

## 9. 实验设计与统计分析计划（SAP）

### 9.1 基线表（I-8 更正 + provenance caveat）

dev 基线来自冻结 locked-group 工件（seed 20260705，Q8_0 GGUF；**C-BASELINES：directional inventory**，`git_dirty=true`、engine build / dataset revision / manifest hash 空——非确证级 provenance）：

| 数据集（角色） | dev 基线 mean (n) | 度量 | 头空判读 |
|---|---|---|---|
| heysquad（replication 候选；头空大但 C-T7 泄漏史） | 0.225 (40) | span/QA acc | 抽取 QA，deployable 臂须以检索产出为条件（§9.6）；**在真正外部开放语料被定义并通过内容级（非路径级）泄漏审计前不得作 FOCUS，L3-MIN-6/L3-MAJ-3** |
| **SQuAD-zh**（更正） | **0.85 [0.725, 0.95] (40)** | QA acc | 近资格门边界（①闭卷<0.85 恰临界），大概率退场为诊断；以 eligibility-split 正式判定 |
| **uro-bench-SQuAD-zh**（若用，独立行） | **0.925 (40)** | QA acc | **与 SQuAD-zh 是不同工件**，不得混用；如用则单列，明显退场 |
| squtr（检索原生主场候选） | 待定（全语料重建后回填） | 检索-QA | 唯一检索原生；SESOI 待首个合法真格（全语料，§6.4） |
| vocalbench-knowledge（闭卷锚点） | 0.8875 (80) | QA acc | within-item 配对差，不做独立判定 |
| SLURP-intent（S4 邻） | 0.6452 (62) | intent acc | 中等头空 |
| is21_deep_bias（S4） | 待定；参照 test-clean B-WER 14.1→5.7@100 | 相对 B-WER↓ | oracle-list 正典 |
| AISHELL-NER（S4） | 待定（891 实体协议） | 相对 B-CER↓ | 中文实体场 |

### 9.2 基线与系统复杂度阶梯

**基线 = 裸核心标准用法**（dev 轻调后冻结、写入 hash）：固定任务模板（绝不含 gold 转写/答案/intent）；greedy（temp 0.0）**——此处 greedy 指裸核心的 temp-0 解码设置（无 RDU），与 §4.4 的 R_greedy（含完整 RDU 的单次 temp-0 全管线采样）是不同对象，勿混用（F2）**；dev 自由度仅限模板措辞与解析正则；只用系统接口契约。**阶梯**（§3.1）：①long-context 全塞入；②own-ASR 朴素级联（modality-bridge，WER 协变量）；③RDU 完整。头号主张比对裸基线；阶梯净增益单独裁定。

### 9.3 单尺度与 SESOI（S-3/S-4 诚实标注；**惯例阈值口径，无业务效果分支**）

主判定尺度 = **错误率相对下降**（消高基线天花板悖论）；**≥10% 相对下降（SESOI）这一相对下降尺度仅用于 Q-A 确证主判定（F4：非指"唯一确证判定是 Q-A"——Q-B 三原子有其各自 null/尺度与 Q-B-SESOI，见 §3.2 与附录 A，同为确证裁定的一部分）**。**S4 的 15% B-WER 不是确证主判定**——S4 整族已降为 directional-only 探索（§3.3、§9.5、附录 A），其 15% 仅作**描述性报告参照**，不做 Holm 存活声明、不并入 primary 分母。**相对/绝对尺度分歧如实标注（PF2）**：确证以在冻结裸基线换算的固定 `SESOI_abs`（绝对当量）操作化"≥10% 相对"；当确证半区裸误差 ≠ 冻结值时二者背离（裸误差偏高→对 10% 相对偏松），故另报确证半区裸误差为分母（带下限）的比率 estimand 敏感性（见 §3.1、附录 A H_SYS_FOCUS）。**时序纪律（PF4）——相对 SESOI 于 pre-M2 冻结，不随 dev/eligibility 结果移动**：程序级**相对 10% SESOI、资格门 2×SESOI 阈值、及 Q-B 两支最小效应量 `Q_B_SESOI_abs`/`Q_B_SESOI_sup` 均属 pre-M2 冻结常数，在触碰任何 eligibility-split 或 selector dev 数据之前记录归档**（区别于 M3 才落定的每集绝对换算 `SESOI_abs` 与 α，§9.5/§13.4）；**绝不在 eligibility/头空结果可见后新选或回改相对 SESOI 或资格阈值**（杜绝 focus 资格被 retro-fit 的 look-ahead）：
- **10% / 15% 明确标注为"惯例科学阈值（conventional scientific threshold）"，不称"业务效果（business effect）"**——本版**不补 stakeholder utility / 错误成本 / 延迟-token-预算 论证**，故按惯例阈值口径贯穿全文（标题、§2.2 及各处**一律不再作"业务效果"主张、不以"业务效果"作为 SESOI 依据**；文中若出现"业务效果"字样，仅为否定性免责说明）。
- **移除 H5 的 15%→10% 自动回退作为 SESOI 变更**（S-3）：dev <12% 观察**只能**是**工程 futility / 路由决定**，**绝不改变"有意义效果"的定义**。per-dataset SESOI 数值表预注册（把相对下降换算各集绝对当量）。

### 9.4 预注册参考系资格规则（S-2；规则保留、头条限定、responder 选择声明）

- **判定切分（四划分 group-disjoint，L3-04）**：独立划分 = exploration-dev / **eligibility-split** / **ε-calibration-set** / confirmatory，**四方 group-disjoint**（**当前 exploration-dev / eligibility / ε-calibration 三划分各 n=40；confirmatory 划分样本量不锁定为 40，而由 §13.4 M2 holdout 供给表按预注册功效目标从保留 test 半区抽取"加大-n 锁定 test"设定**，其 group 基数/互斥/disjoint/power 记入该表——**n=40 不适用于 confirmatory 划分**，F1/L2-02）。**与 §9.1 基线表 n 的关系（PF4-minor）**：§9.1 各集 dev 基线的 n（如 vocalbench-knowledge 80、SLURP-intent 62）是**冻结 locked-group 工件的历史 artifact 规模**，**与本处规划的 n=40 四方划分是不同对象**——前者为既有基线读数的样本量，后者为将于 M2 落定的资格/确证划分设计；二者不冲突、不得互推。**ε-calibration-set 是理论轨 proxy 误差界 ε 的标定集（§10.2，读 U）**，之所以允许它读 gold U，正因它**与 confirmatory groups 严格不相交**——disjointness 写入 §9.8 group/overlap 证明；若相交则 ε（票 #27 regret 定理载荷量）被 confirmatory 数据污染、§4.2"proxy 永不读 gold"保证被破坏。
- **判定条件（CI 下界）**：进入头条参考系须同时满足 ①闭卷基线 < 0.85；②知识头空（oracle-retrieval − bare-core）CI 下界 ≥ 2×SESOI（同 error-reduction 尺度）。**时序纪律（PF4）**：此处 2×SESOI 用的是**相对 10% SESOI（=20% 相对头空阈值）——pre-M2 冻结常数**（§9.3，在触碰 eligibility-split 数据前已归档），**非 M3 才落定的每集绝对 `SESOI_abs`**；故 M2 资格门引用的是一个**已冻结**的常数，绝不在 eligibility/头空结果可见后回改，杜绝 focus 资格 retro-fit。
- **eligibility 检索须同官方全语料（L3-05）**：**②的 oracle-retrieval 头空必须跑在与确证相同的官方全语料（§6.4，同 `corpus_content_hash` 硬门 L3-01）上**，eligibility 运行记录同一 corpus hash。否则若头空在泄漏/小语料（310 或 per-item context）下测得而确证走全语料，则 focus/复制集是**在虚高头空上被选**、确证不复现——一条喂入 responder-cohort 选择的 selection-object provenance 泄漏。
- **零合格集停止规则（L3-06）**：若**无任何数据集**满足资格门（①∧②），则 **Q-A 判为"不可检验（untestable）"——既非失败亦非通过**，`<FOCUS>` 无法实例化，**确证注册暂缓（withheld），回退 M2 development 迭代**（不得以空焦点隐式登记/空过一个 vacuous Q-A）。
- **头条范围声明（S-2）**：头条主张明确限定为 **"headroom-qualified knowledge-dependent speech tasks only"**；焦点/复制集在 M2 由 eligibility-split 选出，若焦点按 observed headroom 最大者选取，则**如实承认 responder-cohort selection**，头条只覆盖该 cohort，不泛化为全部知识依赖任务。
- **单向性 + 固定分母**：只出不进；家族分母按预注册 MAX 计，退场行记 N/A 不收缩分母。
- **诚实预告**：SQuAD-zh（0.85，临界）/ uro-bench-SQuAD-zh（0.925）大概率退场；最终以 eligibility-split 判定为准。

### 9.5 单一最终确证版本制 + 原子假设族（F′-2 / G3 结构性处置）

- **单一最终确证版本制（G3）**：**整个研究计划只有一个最终确证版本；此前所有版本（含本 v4.2）按定义均为 development / exploration**。program 级 Type-I 由此控制：确证的"一次开火"是**一次性、不可逆事件**，只发生一次。**所有 development 迭代（M2↔M5 dev loop）都发生在这一枪开火之前**；owner 唯有"有把握"时才签署 M3、进入 M4 开那唯一一枪。**撤销 per-version α 阶梯**（不再"每版声明 α"）；确证族 α 只在那唯一的确证注册时声明一次。
- **确证失败即终局（S-1，program 级 Type-I 的实体保证）**：一旦那唯一确证一枪开火，**其结果对该头条的显著性检验就是终局**——**通过 → Stage-3；失败 → 显著性检验就此结束，负结果归档入 cumulative evidence，绝不再开第二枪确证 α**。**不存在"迭代后再开那唯一一枪"**（若允许再开，`1−(1−α)^k → 1`，正是 F′-2 要杀死的 repeat-until-success）。开火后即便再迭代改系统，也只能以 **cumulative evidence（非确证显著性）** 报告；要重获确证级显著性只能诉诸 program 外的**独立新数据强制复制**，且须另行 owner 决策，本版不预设。M5→M2 back-edge 因此**仅在确证一枪尚未开火时可用**（即 M4 尚未进入的 development 阶段），**不构成对 M4 的第二次进入**。
- **原子化（S-1）**：primary 确证族按**原子假设**枚举——每个 **dataset × endpoint × contrast** 一个最终 p 值 + 一条校正路径；**无复合行冒充单一假设**。完整机器可读清单见**附录 A**；本版 primary confirmatory 族 = **6 个原子**（Q-A：1 焦点系统效果 + 2 replication no-harm；Q-B：selector 绝对增量 co-primary + 等预算 vs random + 等预算 vs MBR），**Holm within 族（m=6）**。**确证广度如实标注（L3-MAJ-4）**：这 6 原子 = **1 个焦点效应原子（H_SYS_FOCUS，唯一承载跨裸基线真效应的确证）+ 3 个 selector 原子（均只在单一焦点集 `<FOCUS>`）+ 2 个单侧非劣守卫（H_SYS_REP1/REP2，单侧非劣下任何非劣/受益平凡通过、可零真效应 PASS）**；**故 m=6 不得读作"多数据集确证"**——头条泛化实证仅立于单一焦点集的真效应加两个近乎必过的 no-harm 守卫，跨集泛化明确推迟（§3.2、§9.4 responder-cohort 声明）。
- **ρ 出族**：ρ 为 secondary-mechanistic，**不进 primary Holm 分母**（§9.7）。
- **次级族降级（无 Holm）**：S1–S4 归**独立探索族**，**directional-only、各自方向性报告、不做 Holm 存活声明、不并入 primary 分母**（附录 A secondary 段）。
- **主聚合（S-5）**：primary = 焦点集；replication 集走 no-harm 门；**不以异构任务族固定效应池化作 primary**。
- **focus 选择时序（诚实声明）**：候选 datasets → dataset-selection rule → eligibility IDs 与分析 → focus/rep identities → dev configuration selection → confirmatory registration，顺序冻结；**focus/replication 在 M2 由 eligibility-split 选出**，非先验固定；responder 选择在头条范围声明（§9.4）。

### 9.6 S4 三构念拆分（C-6）+ 偏置协议

**S4 拆为三个构念，各有独立 KB 定义 / 泄漏边界 / 成功指标 / 迁移主张，作构念相异的相关研究臂，非共同机制证据**：

| 构念 | KB 定义 | 泄漏边界 | 成功指标 | 迁移主张 |
|---|---|---|---|---|
| **事实型外部知识** | 语料证据文档（heysquad/squtr/SQuAD-zh，全语料 §6.4） | value=eval 前冻结外部语料，无 test-item；语料构成 query-independent | 错误率相对下降 | 跨知识 QA 集 |
| **任务本体/schema** | 域 ontology / intent-slot schema（SLURP） | schema 非答案 | intent/slot acc | 跨 SLU 域 |
| **上下文实体偏置** | 冻结热词/实体库（is21/AISHELL-NER） | 真词不保证入列 | 相对 B-WER/B-CER↓（**描述性参照 ≥15%，无 pass/fail、无 Holm；directional-only，§3.3/§9.3，L2-07**） | 跨实体转写 |

**偏置协议**：热词库 eval 前冻结（写 content_hash）；可部署列表 = 音频键检索产出（含 carrier-sentence 键），非注入 gold；**B-WER reference-anchored 计分**（分母=全部参考偏置词；检索漏检计为错误、绝不从计分对象剔除）；oracle 上界臂**永久不可部署**；H5 相对 B-WER 靶 15%（惯例阈值口径，§9.3；无 SESOI 回退）。命中与否额外作 H5a（召回 + 同音精度）单独报告。

### 9.7 统计口径：cluster bootstrap、ρ 机制量、功效诚实

- **paired cluster bootstrap**，group_key = 来源篇章 id / 说话人或场景。无组键集或补真组键、或不入确证。**resampling unit = group**（cluster），非 item。
- **ρ（secondary-mechanistic，博导 §4.4 口径，F5）**：**只算 aggregate ratio**（分子/分母各自的聚合均值之比），**不平均 item-level ratios**（后者小/零分母爆炸）；**对整个 numerator/denominator 联合 cluster bootstrap 重采样**；**预注册分母下限（数值于 M3 落定，L2-06）+ undefined 处理：某次重采样分母 < 下限时该次 ρ 记 `UNDEFINED`、剔出 ρ CI，并同时报告低于下限的重采样比例，绝不静默 floor 或隐藏丢弃**；**分母条件性预警（PF5-minor）：ρ 的分母是 oracle SELECTION 头空 `R_oracle−R_greedy`（best-of-K by gold − greedy），而 §9.4 资格门保证的是 RETRIEVAL 头空（oracle-retrieval − bare-core）——二者不同头空，FOCUS 资格并不 bound selection 头空，故焦点集上 ρ 分母仍可近简并（大量 below-floor 重采样→UNDEFINED），"realization rate" 可失解释力；因此预注册一条最小 oracle-selection-头空前置（或：仅当 below-floor 重采样比例 < 预注册上限时才报 ρ 为实现率，否则只报 selector 绝对增量与 below-floor 比例，不冒充 realization rate）**；做 **Fieller / percentile bootstrap 敏感性**；**不因分母小而删除不利数据集**；primary 报 absolute selector delta（co-primary），ρ 只作机制量。
- **功效诚实**：dev n≈40、有效 cluster 20–45，Holm 校正后功效低——**探索层不触发任何 kill**（输出=配置排序 + 确证协议草案）；kill 仅在确证层以**加大 n 的锁定 test**判定（该加大-n confirmatory 半区规模/功效目标由 §9.4 与 §13.4 holdout 供给表设定，不与 n=40 的 dev/eligibility/ε 三划分混同，F1/L2-02）。**小样本区间稳健（PF3）**：即便加大 n，确证有效 cluster 仍可能仅 ~20–45，故确证族区间/尾部 p 采 **BCa/studentized-t** 或经标定模拟验证覆盖的 percentile（附录 A S-8、§13.4 M2 预注册），不默认 non-studentized percentile。

### 9.8 采样 custody = public deterministic evaluation（F′-1 / G2 结构性处置）

- **如实命名（G2）**：本方案的 confirmatory 抽取由**提交先于选择的确定性脚本 + 固定公开种子**执行、第三方逐字节可复现——它提供 **replayability，不提供 selection blindness**。故该层**如实称 `public deterministic evaluation`（透明、可复算、非盲法）**；**删除"不可预测 custody"作为签字门的一切措辞**（续26②）。
- **零新机械（G2）**：不引入独立 custodian / benchmark server / secret seed / commit–reveal / burn；防过拟合由"程序性防火墙 + group-aware 抽样 + 单一最终确证版本制（§9.5）"承载。
- **两条正交轴，如实分离（L3-F2/L5-F1）**：**单一最终确证版本制（G3）控制的是 program 级 Type-I**（只开一枪、无 α 阶梯）；它与 **selection blindness（F′-1）正交、不等价**。由于**种子公开、池公开**，confirmatory item IDs **在 M3 dev-config/proxy 权重/卡 schema 冻结之前即可计算**，故 **"提交先于选择"不能关闭 intra-version 的 selection-conditioning（对已知 held-out items 调 dev 配置）通道**——因此本版**不再把"提交先于选择"列为 selection-blindness 防线**，只作 replayability 保证。此 selection-conditioning 残余为**公开、owner 自负的 contested 敞口**（§11 L4-6），非已消解项。
- **未来盲法选项（届时再定）**：若将来某篇论文需要 blinded confirmatory 等级，最轻量方案 = **代码+分析完全冻结后由第三方一次性评分**（benchmark server / 外部人员）——**届时再决，本版不预设**。
- **确证工件非空 provenance**：`git_sha`(`git_dirty=false`)、`engine_build_id`、`dataset_revision`、`manifest_hash`、`sample_manifest` hash、`seed`、`env_versions`、**语料 `corpus_content_hash` + `corpus_doc_count` + `upstream_source_revision`（须 == 该数据集预注册 corpus-lock hash/count 且锚定上游第三方 revision + 公开 checksum——M1 pin 进 datasets.lock/corpus-lock 的参数化常量，L3-BLK-1/L3-F4；对 squtr/FiQA 该 count = 57,638，对其余知识-QA 集用各自注册值，L4-F1；L3-01 硬门；eligibility-split 与确证共记同一 hash，L3-05）**、KB `content_hash` + `embedder_token`、group manifest + overlap proof + **pool/exclusion 定义 hash（confirmatory 模式下 pool/exclusion 一经提交即冻结，L5-02）** + **calibration-set group manifest（与其余三划分 disjoint，L3-04）**；度量定义（corpus vs macro、B-WER vs WER）显式标注。确证 re-run 从干净 checkout 执行。

---

## 10. reward 信号层与理论轨

### 10.1 reward 信号层（数据集无关借用基础设施，非理论贡献）

一组数据集无关的输出侧信号供给，服务三处：§4 selector proxy-reward、§7 发现段触发、§8.3 使用段信任标定。**不用于输出重排序作为独立研究主张**。误差去相关 δ_corr 引 ROVER（Fiscus 1997 [谱系]）作借用基础设施认账，**移出定理约束清单、不作理论贡献**。logprob 类白盒信号退出系统设计，仅留 ledger 作工程诊断。

### 10.2 理论轨（对象 = §4 selector 算子；首定理 = 有限样本 regret）

**形式化对象 = §4 的 Û-argmax 轨迹选择算子**（与 Python 同对象），非"模型本体纯度"。结构（CLAUDE.md 理论标准；博导 §5 校正）：

1. **无约束反例**：无 calibrated proxy 误差界（ε）与预算 cap 时，selector 在 imperfect Û 下随 K 增大可 reward-hack / Goodhart（§4.3 曲线），regret 不趋零、可劣于随机。
2. **有约束首定理（有限样本 selector regret）**：给定**独立标定集上可核验的 proxy 误差界**（高概率 |Û−U| ≤ ε），有 **U(τ\*) − U(τ̂) ≤ 2ε**（τ̂ = argmax Û，τ\* = argmax U）——**对齐已有 `Realization.lean` 的 generic argmax-mismatch bound**（票 #27 复用基础）。**如实定性（L4-F2-minor）**：此界是一个 **generic argmax-mismatch 恒等式**（给定 |Û−U|≤ε 两行即得），**非 operator-specific、非收敛结果**；它是理论轨的**基线引理**而**非 load-bearing 交付物**——真正的载荷（收敛）在下条第二定理，尚未证（§13.4 operator-linked = 0）。**"首定理"之名系 owner 裁决（续26/票 #27）指定沿用**，此处不改名而如实标注其 generic/非收敛性质，避免被读作理论轨已交付的核心结果。
3. **收敛为第二阶段（诚实分离）**：N\* 只是预算 cap、**不是收敛条件**；真正的收敛（随 verifier samples / calibration data 增长 ε_n → 0、regret → 0）作**显式第二定理**，需定义序列 Û_n 的更新与误差趋零机制，**不把有限性当收敛**。
4. **检索-递送必要条件（C-4，显式 MEASURED 假设，博导 §5.3 校正）**：`r₀·Δ_deliver ≥ (1−precision)·c_distractor` **目前至多是 heuristic design inequality**，须从**事件级 utility model**（含 knowledge-needed prevalence / trigger rate / conditional recall / FP rate / top-k 相关与不相关证据数 / 采纳概率 / item 异质与交互）推导，**不作为已识别的一般必要条件、不直接进 Lean 作 load-bearing 假设**；若下列测量槽无法建立，**理论贡献如实删除**。
5. **可执行一致性**：Python↔Lean 逐例一致性测试；sorry-free（记录例外）。闭合前不作"Lean 已证 selector 收敛"的论文句。

**假设账（每假设量给测量槽）**：

| 假设量 | 符号 | 测量槽 | 状态 |
|---|---|---|---|
| **proxy 误差界（标定集，非 argmax 一致度）** | ε (τ) | **ε-calibration-set（§9.4 第四划分，与 confirmatory groups 严格 group-disjoint，L3-04）上保存每候选 Û 与 U，建 high-prob \|Û−U\| 界 + regret**，验证跨 dataset/core shift；标定读 U 仅因该集永不与确证相交 | 待测 |
| 预算 cap | N\* | 1 真格成本标定 + K 扫描（只作 cap，非收敛） | 待测 |
| 检索召回 | r₀ | S1 检索 R@k | 待测 |
| 逐 item 递送增益 | Δ_deliver | oracle-retrieval vs bare 逐 item（注意混合"证据可得"与"递送形式"，需拆） | 待测 |
| 干扰代价 | c_distractor | random-retrieval 注入伤害 | 待测 |
| 检索精度 | precision | QA retrieval precision（**非** S4 同音 precision——二者不同，勿混用） | 待测 |
| **必要条件** | 事件级 utility model 导出式 | 由上导出 | 待验（heuristic，未识别为一般必要条件） |

---

## 11. 边界纪律、复现与完整性（R4：tutorial 级可复现）

**Information-Boundary Guard（STANDING RULE）**：任何杠杆若靠部署没有的信息抬指标即 **invalid，无论统计多显著**；四问全 YES 方可跑（部署可得性、模态尊重、无 test-item 泄漏、真能力非喂答案）。逐臂裁定：检索键嵌入（GLAP/nemotron，含 q2q/a2a 生成桥，query=音频、伪问题/HyDE 由核心自生）→部署；own-ASR 级联（query=own-ASR 非 gold）→部署；标准知识卡（无 test-item 答案）→部署；S4 deployable 列表（真词不保证入列）→部署；oracle-retrieval / gold-transcript / 保证入列列表 / **核心 2048d 隐态**→**非部署或仅诊断/上界**。

**替代复现标准 = tutorial 级可复现（R4）**：拒绝"全部锁死"路线（独立 custodian、commit–reveal、burn 一并否决，含最小 commit–reveal 变体）。替代标准三条：**① tutorial 级可复现**——第三方能 step-by-step 跑出全部宣称结果；**② 零数据集泄漏**；**③ 零学术欺诈**。落地 = **将于 M1 撰写为 REPRODUCE.md 契约**（磁盘尚无此文件，见 §13.4 缺口表）：pinned 数据 manifest + 提交入库代码 SHA（`git_dirty=false`）+ 确定性脚本 + 固定种子 + 预期输出与容差带 + **单一标准测试入口**（`PYTHONPATH=src pytest -q`，M1 门，§13.3）。**明确不采用 custodian / commit–reveal / burn 仪式**——理由（owner 裁决）："我们是在做研究而不是做复杂的系统工程"。**"零学术欺诈"是治理承诺、非可操作抽样偏差机制**；防偏差由 §9.5/§9.8 的程序性防火墙承载。

**关于博导复审"独立监督：强制（INDEPENDENT OVERSIGHT REQUIRED）"的处置（L5-04，如实入正文而非仅在回信）**：owner 立场为**在本阶段以 tutorial 级可复现 + 全流程透明（public deterministic evaluation、逐字节可复算、程序性防火墙）替代强制独立监督（续24④）**，**婉拒**在研究阶段引入独立 custodian / research-integrity 独立方；§11 的 internal consistency check 已如实标注"非独立评审"。若将来某篇论文需要 blinded/independent 等级，最轻量选项 = 冻结后第三方一次性评分（§9.8，届时再定）。对该"强制"判词的完整尊重性商榷置于回信；此处保证正文对该硬判词**有明确可见的处置痕迹、非静默略过**。**（L4-6 如实定性）此项为 UNRESOLVED / 有争议项（contested），非已结构性消解**——博导"独立监督：强制"与 owner"本阶段婉拒"并存且未和解；**采纳独立评分的具体门槛 = 任何 Stage-3 确证性发表之前**（届时按 §9.8 冻结后第三方一次性评分选项决定）。外审应将其读作 owner 自负的公开分歧，而非已处置项。

**claim-ledger 治理**：机器账本（`docs/claim_ledger.yaml`）**先于**任何散文——消费者以账本 status 解析可引性，散文旧正面措辞一律被账本覆盖。一致性检查以**真实可执行工件**交付（票 #38，**本版已随包交付**：`scripts/checks/v42_conformance.py` + `docs/checks/v42-rules.yaml` + `docs/checks/v42-conformance-output.json` + `docs/checks/v42-environment.txt`，第三方可在 WSL 复跑得到逐规则一致裁决），命名为 **internal consistency check（明确非独立评审、非 research-integrity independence）**，范围标签为 `DOCUMENT PACKAGE READY FOR EXTERNAL REVIEW`（**不用 `RELEASE-READY`**，避免被读作"科学已闭合/可执行"）。诚实史（L4-01/L5-02）：v4.1 轮曾承诺这些工件而未交付（磁盘仅有自陈未随附的 `docs/checks/v41-conformance-report.md`）——该失信已在回信勘误具名承认；本版以实际交付关闭该项。命名相关的 relabel（internal consistency check、DOCUMENT PACKAGE READY）用以关闭博导复审 §7.2/§7.3 的误名。

**五类常驻失败模式（结构性预防）**：P1 信息边界泄漏（喂 gold→假增益；C-M3/C-T7 = invalid）→ 递送=检索产出、oracle/gold 永久非部署、每杠杆过 IB-Guard；P2 对象错配（KB 值=查询自身文本；C-PHASEA = invalid）→ 语料侧 KB 重建（全语料 §6.4）、content_hash 扩至 embedder+索引、伪问题 builder 只从审计过的 corpus-document source manifest 构建、**squtr 非 dry-run 一律 hard-require corpus source，缺失即 P0 报错、绝不回落 legacy**；**并（L5-05，博导 I-5）在 M1 交付一份全系统 silent auto-fallback / auto-substitution 清单**——不止 squtr corpus-source 这一处，还含 query-embedder 自动回落（C-PHASEA 曾据此悄然换嵌入空间）、source-name 自动替换、KB 自动回退等**每一条**，逐条**改为 fail-closed 或给出显式论证**（清单入 §13.4 缺口表、M1 门）；P3 transductive 混淆（C-MINDS-POLICY = invalid）→ 卡池与 eval 不相交、选择仅在 dev；P4 依赖运行冒充重复 / winner's-curse → 独立组 cluster bootstrap、赢家 dev 格级选定确证层单通道重立；P5 家族误计 / 事后收窄 → primary 原子族全枚举预注册（附录 A）、全进 Holm、次级族 directional 不做 Holm 声明。

**伦理/许可/dual-use**：逐集 license + permitted-use（nemotron NC 仅研究用，商业价值受限如实标注）；生物特征/声纹按 PII 处理；上下文偏置用途界定为无障碍/知识辅助。

---

## 12. 工作身份（Work Identity，事务一致刷新）

**本提案 = W1（`speech-mllm-training-free-rl`）的 primary study。** W1 = 项目的成熟 training-free 范式参考，本工作把其 reward/eval 机制升为一个完整的 reward-guided 前端知识系统。lineage（事务一致，Thesis / Per-Work-Status / 本 proposal 须同步刷新）：

- **G0（2026-07-11，四项全签）**：owner 签署 W1 收窄问题为 primary，primary estimand 含 **ρ = (R_selector − R_greedy)/(R_oracle − R_greedy)**（本版按 G4 将 ρ 降为 secondary-mechanistic、绝对增量升 co-primary）。
- **RDU refocus**：三段设计修订（匹配几何 / 被测量发现段 / 标准知识卡）、单一接口契约、里程碑 DAG、确定性抽样脚本。
- **本 v4.2（续26）**：五 F′ 结构性处置——全语料 + qrels 只入评分、custody 改 public deterministic evaluation、单一最终确证版本制、proxy 改名 + U/Û 分离、K=1 低成本基线 + S3 1×3 预算匹配。

**W4 是独立工作，不受触碰**：W4（`speech-mllm-omni-embedding-rl`）研究 omni **自身嵌入空间**的 task-conditioned 可读性/可选择性（L0/L1 定位，票 #29）。本版把核心 2048d 隐态降为 W1 的白盒诊断臂**不改变 W4 的研究对象或叙事**。

---

## 13. 风险、迭代/停止规则与里程碑门控 DAG

### 13.1 风险与缓解

| 风险 | 似然×影响 | 消解 gate |
|---|---|---|
| 跨模态路由缺口（audio-query→text-keyed-corpus） | 高×高（M1 门槛） | M1 先交 own-ASR 文本臂；audio-key 臂门控于路由 live 验证；cascade WER 协变量 |
| 匹配几何失效（生成桥接不足以追平专训检索器） | 中×高 | S1a/S1b 分层判定；须训练薄投影则如实报 training-free 负结果 |
| 同音/近音污染（BR-ASR DCL / RECAST 硬负） | 高×中 | 音频+文本键双持；必要条件含显式 precision 项；carrier-sentence 键；H5a 单独报 |
| proxy reward 无信息（self-consistent error / overconfidence） | 中×高 | 三件 proxy 诊断（§4.3）；ρ 报实现率、Û 于 dev 标定后冻结；等预算对照界定 selector 净值；ε 假设账测量槽 |
| 多采样成本（K 条轨迹 + G 预算内探针遍数，§7.1；原"m 遍"表述已按 L5-01 统一为总预算 G 内的探针遍数，PF5-minor） | 中×中 | 全量诚实计账（§7.1）；1 真格标定 N\*；效率优化推迟后期；**不设成本门** |
| 小簇退化（有效 N 20–45） | 中×中 | cluster bootstrap（unit=group）；焦点集为 primary、replication no-harm（不池化异构族） |

### 13.2 迭代 / 停止规则（效果优先；确证层专属 kill；单一最终确证版本制）

1. 唯一确证版本（**cross-atom 合成逻辑，PF-L5F5**）：headline 成立须 **H_SYS_FOCUS 通过 AND 两 replication no-harm 原子（H_SYS_REP1/REP2）均通过**（任一 no-harm 守卫失败即 kill headline）；**selector 实现**须 H_SEL_ABS_DELTA 的**绝对增量 CI 下界 > `Q_B_SESOI_abs`**（预注册最小效应，非 point-zero——对齐附录 A/§3.2 L2-01/PF1，非 ">0"）**且**等预算超越 random/MBR 两原子的 CI 界均越过 `Q_B_SESOI_sup`。六原子采**平-Holm（flat Holm，m=6，各原子独立判定）非层级 gatekeeping**；上述 headline/selector 两组合取仅为**报告口径的合成读法**，多重性仍完全由 m=6 Holm-adjusted p 承载（§9.5、附录 A S-7；答博导 §4.1）。全部满足 → 系统主张 + selector 实现成立，进入 Stage-3。
2. **开火前**（尚在 development、确证一枪未打）不达标 → **development 迭代循环**：用 §7.2 描述性 taxonomy 定位瓶颈段 → 修组件/协议 → 回 M2 探索（M5→M2 back-edge），**均属 development，不开确证 α**；owner 有把握才签 M3、进 M4 打那唯一一枪。归因仅限探索 dev（确证 test 绝不重读）。
2b. **开火后失败即终局（S-1）**：那唯一确证一枪一旦打出且失败 → **显著性检验就此结束、负结果归档 cumulative evidence，绝不第二次进入 M4 / 不再开确证 α**（§9.5）；此后迭代只能以 cumulative evidence 报告，重获确证级显著性须 program 外独立新数据复制 + 另行 owner 决策。
3. selector 绝对增量 CI 在**单一焦点集 `<FOCUS>`** 的确证判定**不越过 `Q_B_SESOI_abs`**（且等预算超越 random/MBR 不成立）→ 结论定为"support exists, realization fails"，照常发表（以"为何 label-free proxy 无法实现头空"为中心）。**（PF3/PF-L5F3：Q-B 无跨集复制，selector 身份限定单一焦点集，§3.2/§9.5——原"两独立 test surface"系旧 focus+replication 设计遗留，已撤除。）**
4. **负结果纪律**：primary 禁用于去赢（按去赢设计）；次级点 S1–S4 正负皆入 ledger（directional）。

### 13.3 里程碑门控 DAG（无日历周；按门 entry criteria 全绿推进）

```
                 ┌── M2↔M5 back-edge（开火前 development 迭代，不开确证 α）──┐
                 ▼                                                          │
M1 工程就绪 ─▶ M2 探索完成 ─▶ M3 确证协议签署(owner) ─▶ M4 单一最终确证【一次性开火】
                                                              │
   ┌── PASS ─▶ Stage-3 进入 ─▶【独立评分门（L4-6/§9.8）】─▶ Stage-3 确证性发表
   └── FAIL ─▶ 终局：显著性检验结束、归档 cumulative evidence
               （S-1：绝不第二次进入 M4；back-edge 仅在开火前有效）
```
> **DAG 语义（S-1）**：M4 是**一次性、不可逆**的确证开火。**M2↔M5 的 development back-edge 只在 M4 开火之前有效**；M4 一旦开火，PASS→Stage-3、FAIL→终局归档，**两种结局都不再返回 M4**（不存在"迭代后再打那一枪"）。
> **独立评分依赖（L3-F2/L5-F1，reconcile §11 L4-6）**：M4 的 PASS 令头条**进入 Stage-3**，但**任何 Stage-3 确证性发表之前须过独立评分门**（§9.8 冻结后第三方一次性评分选项，L4-6）——DAG 显式画出此依赖，与 §11 L4-6 一致。**owner-ruling 冲突如实标注（G2/G3）**：博导 F′-1/E-3 要求"公开固定种子层非盲法→M4 确证结果证据等级下调为 exploratory，或把第三方评分并入 M4 开火本身"；**owner 裁决（续26-G2）保留 confirmatory 等级、custody 仅改名 public deterministic evaluation、第三方评分推迟至发表前"届时再定"**，**故本版按裁决不下调 M4 等级、不把第三方评分并入 M4**——该分歧为 §11 L4-6 记录的 UNRESOLVED/contested 敞口，非已消解（此处不"修复"而如实标注 ruling 冲突）。

**M1 工程就绪（仅工程可执行项；holdout 表 / 资格判定 / 原子族定稿 / 签字属各自后续门）**：
- clean-checkout 重建绿；**单一标准测试入口 `PYTHONPATH=src pytest -q` 零 error**（不依赖非标准脚本入口）；
- **squtr 全语料 / query-independent build**（§6.4）；伪问题建库路径只从 corpus-document source manifest 输入；**squtr 非 dry-run hard-require corpus source，缺失即 P0 报错、绝不回落 legacy**；
- **五维审计拆分 + `n_golds=0 → NOT_EVALUATED`**（消除空转 CLEAN）；
- **group-aware 确定性抽样**（group manifest + 按 group 抽样 + 强制加载并排除全部 prior-exposure union，缺一即 fail-closed）；**confirmatory 模式下 deterministic_draw 对固定种子下的 pool/exclusion 定义变更 fail-closed（禁止 force_supersede 重抽），pool/exclusion 定义 hash 记入确证 provenance（L5-02，博导 §6.3/§6.4）**；
- **§4 K-轨迹 selector harness + 等预算 K-candidate random/MBR**；**K=1 基线不标 equal-budget**；
- 真跨模态 **live smoke**（GLAP/Nemotron 音频→文本检索报告；升 supported 前不得为 stub）；real q2q 2-doc smoke + 全语料 scaling 估计；
- 知识卡 schema；S4 资产（is21 + AISHELL-NER + B-WER 打分器）；中文 CER + minimal-pair 测试通过；
- 1 真格成本标定（含 G 预算内探针遍数 + K-轨迹 wall-clock，PF5-minor：统一 §7.1 的 G 总预算 + 探针遍数口径，非旧"m 遍"）；旧 KB 重建或永久标 incomplete-provenance。

**M2 探索完成**：全臂族 dev 跑完（modality×form×delivery × selector × 阶梯 × S1–S4）——**凡 selected config 前向转入确证的 exploration-dev 检索一律跑在全语料/query-independent 语料上（L3-F3，§6.4/§4.2），310 仅作不选择任何东西的 plumbing smoke**；发现段三层描述性指标栈；§10.1 离线信号标定表 + 三件 proxy 诊断（§4.3）；**holdout 供给表**；资格判定（eligibility-split，CI 下界 ≥2×SESOI）；focus/rep 选定并声明 responder；**primary 原子族清单（附录 A）与确证族 α 定稿**；退出 = 确证协议草案成文。

**M3 确证协议签署（owner）**：审阅 M2 产出并签署（七项，§14）；探索层不触发任何 kill。

**M4 单一最终确证**：确定性脚本抽取（提交先于选择、group-aware）；单通道评分；primary 原子族 Holm（m=6）判定 vs 预注册 SESOI；ρ 机制量（aggregate-ratio + Fieller/percentile）；跨核心迁移冒烟（非门控）。

**M5**：达标→Stage-3；不达标→development 迭代或 owner 复盘。收尾：Decision-Log 追加 + Per-Work-Status 更新。

### 13.4 诚实缺口表（尚未交付项 × 所属门）

| 尚未交付项 | 现状 | 所属门 |
|---|---|---|
| §4 K-轨迹 selector harness + 等预算 K-candidate random/MBR | 未实现 | **M1** |
| 真跨模态 live smoke（GLAP/Nemotron 音频→文本检索报告） | 脚本存在、未跑 | **M1** |
| squtr 全语料（57,638 docs）build + 全语料 q2q 嵌入 | 未建（310 库仅 DEV smoke） | **M1** |
| 焦点/资格候选语料 pin 进 datasets.lock/corpus-lock（FiQA/squtr 全语料、is21_deep_bias、AISHELL-NER、SQuAD-zh：**上游第三方 revision + 公开 checksum + per-set `content_hash` 与 `doc_count`**，参数化 L3-01 门键此值，L4-F1/L3-F4） | 未 pin（不在冻结 28 集内，L3-01 所键 corpus-lock 常量尚不存在，L3-BLK-1） | **M1** |
| 五维审计拆分 + `NOT_EVALUATED` 输出 | 待改（现为空转 CLEAN） | **M1** |
| group-aware 抽样 + 强制 exposure-union 排除 | 现为 item-id 抽样、exclusion optional | **M1** |
| deterministic_draw confirmatory 模式：pool/exclusion 重定义 fail-closed + 禁 force_supersede 重抽 + pool/exclusion hash 入 provenance | 未实现（现 force_supersede 允许改 pool/exclusion 后重抽；append-only JSONL 可编辑非防篡改，L5-02） | **M1** |
| 标准 `pytest` 全仓零 error | 现有 4 errors（results fixture） | **M1** |
| 旧 KB 重建 / 永久 incomplete-provenance 标注 | sidecar 含 guess/assumed，非 build-time | **M1** |
| holdout 供给表（每集 group 基数/互斥/disjoint/power；**含 confirmatory 加大-n 锁定 test 半区规模与功效目标，F1/L2-02**；**含确证族区间/尾部方法选择 BCa/studentized-t 或标定验证的 percentile，PF3**） | 未交付 | **M2** |
| primary 原子族数值定稿（focus/rep、per-dataset `SESOI_abs`、no-harm margin、K、N\*、reward 权重、α；**相对 10% SESOI、2×SESOI 资格阈值、及 Q-B 两支 `Q_B_SESOI_abs`（selector 绝对增量）/`Q_B_SESOI_sup`（等预算超越，normalized-error 尺度，L2-01/PF1）除外——均属 pre-M2 冻结常数（owner 于 §14 签字位设定、先于任何 exploration/dev 运行、selector dev 观测后绝不回改），PF4**） | 模板占位 | **M2→M3（Q-B-SESOI 除外，pre-M2）** |
| 三件 proxy 诊断实测（rank AUROC / self-consistent-error / Goodhart） | 未测 | **M2** |
| §7.2 L1 oracle-treatment responsiveness 的**重复采样次数与 estimand 定义**（`P(Y₁−Y₀>0)`）冻结（PF-L5F4-minor；描述性/never-confirmatory，但比照其余测量槽入门） | 未冻结（§7.2 未定采样次数） | **M2** |
| #27 Lean 首定理（有限样本 regret）+ Python↔Lean conformance | 有可复用 argmax-mismatch bound，operator-linked = 0 | **M2/独立理论轨** |
| internal consistency check 工件（checker code + rule manifest + 输入 hash + 输出 JSON + 失败项 + 执行环境） | **已交付**（`scripts/checks/v42_conformance.py` + `docs/checks/v42-{rules.yaml,conformance-output.json,environment.txt}`，12/12 PASS 可复跑；v4.1 轮曾承诺未交付，失信已在回信具名承认） | **M1（#38）✅** |
| REPRODUCE.md 复现契约（pinned manifest + 代码 SHA + 确定性脚本 + 种子 + 预期输出/容差 + 单一测试入口） | 未撰写（磁盘无 REPRODUCE.md） | **M1** |
| 全系统 silent auto-fallback / auto-substitution 清点（embedder / source-name / KB 等，逐条改 fail-closed 或显式论证） | 未清点（现仅 squtr corpus-source 一处 hard-require） | **M1** |

---

## 14. Owner / Reviewer 签字位

> **可修订工作参数**：签字时可修订的三项 = **G 预算内探针遍数（触发/采样诊断设置；PF5-minor：即 §7.1 总预算 G 内的探针遍数，非旧"m"）**、**H5 futility 门槛（工程 futility/路由，非 SESOI）**、**确证族 α（单一确证注册时声明一次）**。**无成本类成功门**，**无 H5 SESOI 回退**，**无 per-version α 阶梯**（均已按 R1/S-3/G3 撤除）。

1. **两个可分别裁定的确证问题**（Q-A/Q-B 共用焦点集与 Holm 家族，非"真正独立"，L4-05）（Q-A 系统效果 vs 裸基线 ≥10%、全语料、头条限定 headroom-qualified；Q-B selector vs 等预算 random/MBR、绝对增量 co-primary + ρ 机制量、K=1 低成本基线在族外）+ 系统接口契约（单一，检索特征=独立冻结 embedder 语音向量；核心 2048d 隐态=白盒诊断臂）。签字：待定。
2. **10% 错误率相对下降（惯例科学阈值口径，不称业务效果）+ per-dataset SESOI 数值表（签字前固定）+ 资格规则（eligibility-split ①闭卷<0.85 ②headroom CI 下界≥2×SESOI；头条限定 headroom-qualified + responder 声明）**。签字：待定。
3. **§4 reward-guided 轨迹选择算子（U/Û 分离、动作/策略/proxy-reward/选择/停止 N\*）+ #27 Lean 同对象（无约束失败 + 有约束首定理 U(τ\*)−U(τ̂)≤2ε + 假设账 ε/N\*/C-4 heuristic）**。签字：待定。
4. **语料/KB 独立性（全语料 + qrels 只入评分 + 五维审计 + `NOT_EVALUATED` + 310 库永久 DEV smoke）**。签字：待定。
5. **原子假设族（附录 A，primary m=6，Holm within 族）+ 单一最终确证版本制（G3）+ 次级族 directional 无 Holm + custody = public deterministic evaluation**。签字：待定。
6. **复现与完整性标准 = tutorial 级可复现（REPRODUCE.md 契约 + 单一标准测试入口）+ 零泄漏 + 零欺诈；确定性脚本 + 固定种子；不采用 custodian/commit-reveal/burn**。签字：待定。
7. **里程碑门控 DAG（M1 仅工程就绪项、own-ASR 先行、路由 live 并行纳入 M1；M4 一次性开火、失败即终局归档，S-1）+ S3 轻量 1×3 预算匹配 + S4 三构念拆分**。签字：待定。<br/>（**F3 移除**：原"预算超首格 1.5× 中断回报"机制正文未定义、且与"无成本成功门"抵触，本版删除该签署项以免签一条未定义承诺；如需成本监控中断，另作**运维监控中断**而非成功/futility 门在 §13.1 单列。）

---

## 附录 A — 原子假设清单（machine-readable，S-1）

> primary confirmatory 族 = **6 原子**（Holm within 族，m=6；确证族 α 于单一确证注册时声明一次，G3）。焦点集 `<FOCUS>` 与 replication 集 `<REP1>/<REP2>` 于 M2 eligibility-split 后定名（诚实预告：squtr-全语料 为焦点候选，heysquad/SLURP-intent 为 replication 候选；**heysquad/SQuAD-zh 须先具名并审计其开放共享语料方可进入 eligibility，L3-02**；若按 headroom 选取则声明 responder-cohort）。**非开放语料构念的 fail-closed 泄漏门（L3-F5-minor）**：SLURP-intent 的知识对象是 **ontology/intent-slot schema（§9.6 构念 2，"schema 非答案"）**，无 corpus_content_hash、无 golds-in-corpus、`doc_count==57,638` 对其无意义——五维（open-corpus-QA 形）审计对其**不能整体判 N/A 静默绕过，亦不能在 L3-MAJ-2 下因某轴 NOT_EVALUATED 而含糊**。故 **SLURP-intent 进入 primary Holm 家族之前，须先定义一个构念专属 fail-closed 泄漏审计**：断言 intent/slot schema **不含任何 per-item gold 标签**、且以 content_hash 冻结、其内容与 eval 标签集 **disjoint**；**在该构念专属门定义并通过前，SLURP-intent 不得进入 primary 家族**（或明确将非 open-corpus 构念排除于 replication 原子之外）。**空焦点停止规则（L3-06）：若 eligibility 门下无任何数据集合格，`<FOCUS>` 无法实例化，则 Q-A 判"不可检验（untestable，非失败非通过）"、确证注册暂缓、回退 M2，绝不以空焦点 vacuous 登记/空过。** **次级族（S1–S4）directional-only、各自多重性、不做 Holm 声明、不并入 primary 分母**。

**每原子共享的 p 值算法骨架（paired cluster bootstrap；S-8）**：以下为**算法骨架**，其**边界常数——family α、per-dataset `SESOI_abs`（相对 10% 于签字前换算得的绝对当量）、no-harm margin（绝对尺度，L2-04）、分母下限、N\*、reward 权重——一律于 M3 单一确证注册时落定，本版不填**（§13.4 缺口表 M2→M3）。**注意区分（PF4）**：程序级的**相对 SESOI（10%）、资格门 2×SESOI 阈值、及 Q-B 两支最小效应量 `Q_B_SESOI_abs`（selector 绝对增量，task-utility 尺度）/`Q_B_SESOI_sup`（等预算超越，normalized-error 尺度，L2-01/PF1）均属 pre-M2 冻结常数**（见 §9.3/§9.4，owner 于 §14 签字位设定数值、在触碰任何 eligibility-split 或 selector dev 数据之前记录），M3 只做每集绝对换算与 α 落定，**绝不在 eligibility/头空/selector dev 结果可见后回改相对 SESOI、资格阈值或 Q-B SESOI**。故本规格提供的是"可执行算法的骨架 + 判据形式"，**非已可执行的完整数值规格**，不得据此宣称预注册已就绪。
- **null**：见各原子 `null`；**direction**：见各原子 `direction`（**全部单侧**：单侧下降 / 单侧非劣 / 单侧优越；**本族无 TOST 双侧原子**，S-2）。
- **resampling unit = group（cluster）**：按 group_key（篇章 id / 说话人-场景）重采样 group（非 item）；每 bootstrap 重取 B=10000 次。
- **随机采样方差如实披露（PF6-minor）**：selector/random/MBR 三者输出都依赖**实际抽到的哪 K 条样本**；仅重采样 item/group 是**条件于单次已实现的 K-生成**，未纳入温度 T 采样本身的方差——故 confirmatory 结果**显式声明为条件于该单次 K-生成**，此局限如实标注（"selector superiority conditional on one draw at temperature T"）；预注册**可选**加一个 generation-level 重采样 / 多次独立 K-draw 分量把采样方差纳入确证 CI（若 M2 成本标定允许，M2→M3 决定）。
- **统计量**：paired mean-diff（system 与对照在同 item/group 配对）；**区间/尾部方法（小样本稳健，PF3）**：因确证有效 cluster 可低至 ~20–45（§9.7）且 Holm-rank-1 原子要在 ≈α/6 单侧尾部（~0.008）估计，non-studentized percentile 仅一阶精确、在小簇数与极端尾分位处覆盖可失准；故确证族**改采 BCa 或 studentized bootstrap-t**，**或**在签字前以**标定模拟**证成 percentile 在该确证有效-cluster 数与 α/m 尾部覆盖达标后方沿用 percentile——**二选一于 M2 holdout 表随功效目标一并预注册**，不得默认 non-studentized percentile。
- **p 值（单侧，无 double 化——S-6；单一方法，L2-03）**：对每个原子**统一采用 shift/null bootstrap**——把配对差整体平移使其均值等于该原子的 null VALUE，在此平移后的 null 分布上重采样，**p = 重采样统计量朝备择方向至少与实际观测统计量一样极端的比例**。null VALUE 逐原子取值：**H_SYS_FOCUS 为 `SESOI_abs`（绝对当量，见 S-4）**、**selector 等预算超越（vs random/MBR）为 `−Q_B_SESOI_sup`（L2-01 预注册最小效应，normalized-error 尺度；非 point-zero null——PF1）**、**selector 绝对增量（vs greedy）为 `Q_B_SESOI_abs`（L2-01）**、**no-harm 复制原子为 −margin**。**不作 double 化**（doubling 属双侧运算，对单侧检验不适用）；**且不把"recenter 到 null 后再取落在 null 一侧的比例"当作 p**——该量 recenter 后恒 ≈0.5、退化（L2-03：避免把 CI-反演与 shift-null 两法胶合成矛盾复合体，本族统一以"相对观测统计量的极端性比例"定义单侧 p）。
- **no-harm 复制门 = 单侧非劣（single one-sided non-inferiority，替代 TOST——S-2）**：**H0: effect ≤ −margin（相对裸基线恶化超过绝对 no-harm margin）；拒绝 H0 → 判定 no-harm 成立**。**不用 TOST/两单侧取大者**——full TOST 是双侧等价检验，其上侧分量会把"真实收益超过 +margin"的强受益复制**错误判为不通过**；单侧非劣下**任何非劣/受益都平凡通过**，方向正确。**两 replication NI 原子的单侧 p 与其余四原子同入 m=6 Holm 家族校正（L2-05），并如实标注其平凡通过性（L3-MAJ-4）**。
- **decision rule（保守合取，多重性仅由 Holm-adjusted p 承载——S-7）**：判 PASS **须两条件同时成立**——(i) **Holm-adjusted 单侧 p < α**；(ii) **未校正、单侧 95% CI（区间方法 = BCa 或 studentized bootstrap-t，M2 二选一冻结；non-studentized percentile 不得为默认，PF3/本节 S-8 上文）界越过 SESOI/no-harm margin（L2-06：CI 为单侧，与单侧检验层级对齐——单侧 95% 界 ↔ 0.05 单侧水平；下降/非劣原子取单侧下界、selector 超越原子取 selector−对照 差的单侧上界）**。**不再用"CI 优先于点估计"的措辞**（该措辞在统计上不自洽：把多重性校正的 p 与非校正的 95% CI 并列还称 CI 优先并无依据）。明确口径：**多重性完全由 Holm-adjusted p 承载**；附加的未校正 CI 条件是**有意的保守合取**（更严、只会降低而非抬升 Type-I），非多重性控制的一部分。
- **"≥10%" 是 SESOI 值，不是点估计通过判据（F5 + S-4）**：§9.3 标题的"主判定 = ≥10%"里的 **10% 指 SESOI 数值**（相对当量），**不是"点估计 ≥10% 即通过"**。操作判据是上面的 (i)∧(ii)，其中 (ii) 要求 **CI 下界越过 SESOI**——比"点估计 ≥ SESOI"更严。**故不再把二者称为"同一 null 的两面"**。尺度换算（S-4）：**相对 10% SESOI 在签字前用冻结裸基线换算为每集固定绝对 margin `SESOI_abs`**，H_SYS_FOCUS 直接以绝对配对 mean-diff 对 `SESOI_abs` 判定（不作 per-bootstrap ratio）。
- **missingness = fail_closed**；**selection_rule = frozen（M2 eligibility 后冻结，顺序见 §9.5）**。

```yaml
family: primary_confirmatory_final      # SINGLE final confirmatory version (G3); alpha declared once at that registration
correction: holm                        # within this family, m = 6
selection_rule: frozen_after_eligibility_split   # order frozen per §9.5; responder-cohort declared if headroom-selected
resampling_unit: group                  # cluster bootstrap, B=10000; interval/tail = BCa 或 studentized bootstrap-t（M2 标定后二选一冻结；non-studentized percentile 不得为默认，PF3/S-8）
missingness: fail_closed
atoms:
  # ---- Q-A: system effect (full/query-independent corpus, headroom-qualified) ----
  - hypothesis_id: H_SYS_FOCUS
    question: Q_A_system_effect
    dataset: <FOCUS>
    endpoint: absolute_error_reduction_vs_fixed_margin   # S-4: relative-10% SESOI pre-converted to a FIXED absolute per-dataset margin using the frozen bare baseline; test absolute paired mean-diff (no per-bootstrap ratio). PF2: the fixed-margin surrogate can diverge from 10%-relative when confirmatory-split bare error != frozen dev bare error (anti-conservative if confirmatory bare error is higher); report a ratio-estimand sensitivity with denominator = confirmatory-split bare error (preregistered floor) and disclose divergence in §9.8 provenance
    contrast: best_frozen_rdu_vs_bare_core          # corpus per §6.4 (full/query-independent), corpus_content_hash gate L3-01
    null: "absolute error reduction <= SESOI_abs (= 10% x frozen_bare_error, pre-registered per dataset)"
    direction: one_sided_reduction
    statistic: paired_cluster_bootstrap_mean_diff
    decision: "holm_p<alpha AND 95% BCa/studentized-bootstrap-t CI lower of ABSOLUTE paired mean-diff > SESOI_abs; interval/tail = BCa 或 studentized bootstrap-t（M2 标定后二选一冻结；non-studentized percentile 不得为默认，PF3/S-8）"
    role: primary
  - hypothesis_id: H_SYS_REP1
    question: Q_A_system_effect
    dataset: <REP1>
    endpoint: absolute_normalized_error_difference   # L2-04: absolute paired mean-diff of normalized error rates (NOT a per-bootstrap ratio); no_harm_margin is ABSOLUTE
    contrast: best_frozen_rdu_vs_bare_core
    null: "system worse than bare by more than ABSOLUTE no-harm margin"
    direction: one_sided_non_inferiority   # S-2: reject H0 effect<=-margin => no-harm; NOT TOST
    statistic: paired_cluster_bootstrap_mean_diff
    decision: "holm_p<alpha (one-sided NI p enters the m=6 Holm family, L2-05) AND uncorrected one-sided 95% BCa/studentized-bootstrap-t CI lower of absolute paired mean-diff > -no_harm_margin (NOT pooled, S-5); interval/tail = BCa 或 studentized bootstrap-t（M2 标定后二选一冻结；non-studentized percentile 不得为默认，PF3/S-8）"
    role: replication
  - hypothesis_id: H_SYS_REP2
    question: Q_A_system_effect
    dataset: <REP2>
    endpoint: absolute_normalized_error_difference   # L2-04: absolute paired mean-diff of normalized error rates (NOT a per-bootstrap ratio); no_harm_margin is ABSOLUTE
    contrast: best_frozen_rdu_vs_bare_core
    null: "system worse than bare by more than ABSOLUTE no-harm margin"
    direction: one_sided_non_inferiority   # S-2: reject H0 effect<=-margin => no-harm; NOT TOST
    statistic: paired_cluster_bootstrap_mean_diff
    decision: "holm_p<alpha (one-sided NI p enters the m=6 Holm family, L2-05) AND uncorrected one-sided 95% BCa/studentized-bootstrap-t CI lower of absolute paired mean-diff > -no_harm_margin; interval/tail = BCa 或 studentized bootstrap-t（M2 标定后二选一冻结；non-studentized percentile 不得为默认，PF3/S-8）"
    role: replication
  # ---- Q-B: selector effect (equal-K family; K=1 is OUTSIDE this family) ----
  - hypothesis_id: H_SEL_ABS_DELTA
    question: Q_B_selector_effect
    dataset: <FOCUS>
    endpoint: absolute_task_utility_delta            # R_selector - R_greedy on task utility U
    contrast: reward_guided_selector_vs_greedy       # F1: DELIBERATELY budget-UNMATCHED deployment-value metric (K-budget system vs greedy). F2: greedy = SINGLE temp-0 pass of the FULL RDU pipeline (same RDU config as selector, one sample), NOT the bare-core §9.2 baseline (bare core has no RDU) -- so this atom's low-end anchor differs from H_SYS_FOCUS's (bare core) and is NOT that contrast restated; no double-count in the Holm family. Distinct purpose from the equal-budget superiority atoms below; K=1 stays descriptive because greedy is the sole canonical default while K=1 is an arbitrary single stochastic sample
    null: "absolute task-utility delta <= Q_B_SESOI_abs (preregistered minimum effect, PRE-M2 FROZEN CONSTANT set at the §14 signature before any exploration/dev run, never reselected after any selector dev observation per PF4; NOT point-zero, L2-01)"
    direction: one_sided_positive
    statistic: paired_cluster_bootstrap_mean_diff
    decision: "holm_p<alpha AND uncorrected one-sided 95% BCa/studentized-bootstrap-t CI lower of absolute task-utility delta > Q_B_SESOI_abs (L2-01: preregistered minimum effect, NOT merely >0; L2-05/L2-06); interval/tail = BCa 或 studentized bootstrap-t（M2 标定后二选一冻结；non-studentized percentile 不得为默认，PF3/S-8）"
    role: primary_co_primary
    scope_note: "S-5: confirmed on <FOCUS> only; no Q-B cross-dataset replication; selector/TFRL identity claim explicitly scoped to this single dataset, generalization deferred. L4-2: this budget-UNMATCHED atom is a DEPLOYMENT-VALUE endpoint (co-primary per G4) and CANNOT alone support the selector/TFRL MECHANISM claim -- mechanism identity rests only on the equal-K vs random/MBR atoms"
  - hypothesis_id: H_SEL_VS_RANDOM
    question: Q_B_selector_effect
    dataset: <FOCUS>
    endpoint: normalized_error
    contrast: selector_vs_random_selection_equal_K   # equal-budget selector family
    null: "selector superiority over equal-K random <= Q_B_SESOI_sup (preregistered minimum effect on normalized-error scale, PRE-M2 FROZEN CONSTANT set at the §14 signature before any exploration/dev run, never reselected after any selector dev observation per PF4; NOT point-zero, L2-01/PF1)"
    direction: one_sided_superiority
    statistic: paired_cluster_bootstrap_mean_diff
    decision: "holm_p<alpha AND uncorrected one-sided 95% BCa/studentized-bootstrap-t CI upper of (selector - comparator) normalized-error paired mean-diff < -Q_B_SESOI_sup (L2-01/PF1: preregistered minimum superiority, NOT merely <0; L2-05 concrete inequality; selector lower normalized error = better); interval/tail = BCa 或 studentized bootstrap-t（M2 标定后二选一冻结；non-studentized percentile 不得为默认，PF3/S-8）"
    role: primary
  - hypothesis_id: H_SEL_VS_MBR
    question: Q_B_selector_effect
    dataset: <FOCUS>
    endpoint: normalized_error
    contrast: selector_vs_mbr_medoid_equal_K         # equal-budget selector family
    null: "selector superiority over equal-K MBR <= Q_B_SESOI_sup (preregistered minimum effect on normalized-error scale, PRE-M2 FROZEN CONSTANT set at the §14 signature before any exploration/dev run, never reselected after any selector dev observation per PF4; NOT point-zero, L2-01/PF1)"
    direction: one_sided_superiority
    statistic: paired_cluster_bootstrap_mean_diff
    decision: "holm_p<alpha AND uncorrected one-sided 95% BCa/studentized-bootstrap-t CI upper of (selector - comparator) normalized-error paired mean-diff < -Q_B_SESOI_sup (L2-01/PF1: preregistered minimum superiority, NOT merely <0; L2-05 concrete inequality; selector lower normalized error = better); interval/tail = BCa 或 studentized bootstrap-t（M2 标定后二选一冻结；non-studentized percentile 不得为默认，PF3/S-8）"
    role: primary

mechanistic_metric:                       # secondary-mechanistic, NOT in Holm denominator (G4, §9.7)
  - rho_selector_realization:
      formula: "(R_selector - R_greedy)/(R_oracle - R_greedy)"
      estimator: aggregate_ratio_only       # never mean of item-level ratios
      resampling: joint_cluster_bootstrap_of_numerator_and_denominator
      denominator_floor: preregistered_M3_slot   # L2-06: numeric value set at M3; if a resample denominator < floor, that resample's rho = UNDEFINED, excluded from the rho CI, and the below-floor resample fraction is reported (never silently floored or hidden-dropped)
      sensitivity: [fieller, percentile_bootstrap]
      note: "computed on task utility U only; oracle is upper bound, never deployable"

low_cost_baseline:                        # OUTSIDE equal-budget family (G5)
  - single_rdu_K1:
      label: low_cost_system_baseline       # NEVER labeled equal-budget
      role: descriptive_cost_reference

secondary_exploratory: directional_only_no_holm   # S1-S4; ranking only; NOT in primary denominator
secondary_atoms_summary:
  - S1a: q2q_vs_q2a_same_embedder            # retrieval R@k + end-to-end (form-bridge hypothesis)
  - S1b: generative_bridge_vs_trained_frozen # GLAP/nemotron ceiling; report training-free negative honestly
  - S2:  standard_card_vs_flat_EQUAL_CONTENT # identical facts/examples/tokens/position, vary schema only (C-3)
  - S3_effect: never_vs_always_vs_triggered_SAME_SAMPLING_BUDGET  # light 1x3; effect-only; cost DESCRIPTIVE (R1)
  - S4a: factual_external_knowledge          # construct 1 (C-6)
  - S4b: task_ontology_schema                # construct 2
  - S4c: contextual_entity_biasing_rel_BWER  # construct 3, reference-anchored; >=15% is a DESCRIPTIVE reference only, no pass/fail, no Holm (directional-only, L2-07)
```

---

## 附录 B — 热词 / 上下文偏置调研裁定（S4 协议锚）

四透镜调研（传统偏置技术 × chat-API 存活性 / prompt 偏置效应量与列表规模 / 检索式注入证据 / 基准·协议·本地测试床）。核心裁定：六族传统偏置技术在 chat-API omni 下无一原样存活（分水岭=解码器内部访问）；retrieve-then-inject 是文献收敛替代形态；top-2 甜点、N≥100 灾难幻觉、off-the-shelf CLAP 词汇键已死（R@1≈0.1）、赢家检索器多为专训对比检索器——正是 §6 匹配几何要以零训练生成桥接反制的现实。`logit_bias`/语法约束记录原样保留，仅供工程诊断，不作系统组件。own-ASR→text 级联作 modality-bridge 对照臂，cascade WER 作协变量。

---

## 附录 C — reward 信号层调研（后端认账 + 存量池离线标定）

四透镜（经典后融合 / LLM-GER training-free / omni 二遍解码现状 / 存量池离线标定设计）。核心裁定：约束选择安全、自由改写陷阱（regime-conditional，SEAL arXiv:2501.08421 立受约束解码为安全原语，剑桥 arXiv:2409.09554 示强 LLM 可超 N-best oracle）；GER 大数全为 fine-tuned；omni 自池 training-free 二遍解码本身是空白，**不以此空白立方向**——只把输出侧信号当作 §4 selector proxy-reward、发现段触发与使用段标定的供给。self-consistency/verbal confidence 是有用不确定度 proxy 但存在 self-consistent errors / overconfidence（Too Consistent to Detect；CISC），imperfect reward 下扩 N 会 reward hacking（Best-of-N inference-time alignment）——三件 proxy 诊断（§4.3）正为此设。δ_corr 引 ROVER（Fiscus 1997 [谱系]）作借用基础设施认账，不作理论贡献。

---

## 附录 D — 评审历史与已弃方案（失败史；invalid 证据仅存于此）

**失败对象谱系（仅作失败史，绝不作正向证据）**：C-M3 假 +22.4%（喂 test-item gold 转写，invalid）；**C-T7 假 +51.7pp**（heysquad SQuAD-type answer-lookup，answer_in_own_KB=1.0、检索用问题文本，invalid——**其"召回优先"效应方向仅记于此，绝不作 §7 动机**）；C-PHASEA（PLAN-ONLY 冒充可执行 + squtr KB 值=query 自身文本对象错配，invalid；后续工程侧 P0 已修但语料侧对象错误使无一有效 Phase-A cell 运行，故维持 invalid，全语料重建 §6.4 后重开）；C-MINDS-POLICY（transductive + 三因子混淆，invalid，已被 C-MINDS-V2 directional 取代）。

**owner 设计裁定谱系**：v1 敌对评审团（5 FUNDAMENTAL + 12 MAJOR）→ 研究对象重立为 omni agentic system、效果唯一裁判、frozen-key 降次级、基线哲学反转；续18 取消白盒扩展层（单一接口契约）；续24 撤成本门、接口按 R2 收敛、Path B 恢复 ρ、tutorial 级可复现替代锁死仪式；**续26（本版）五 F′ 结构性处置**——全语料 + qrels 只入评分、custody 改 public deterministic evaluation、单一最终确证版本制、proxy 改名 + U/Û 分离、K=1 低成本基线 + S3 1×3 预算匹配。

**已弃方案**：主问题"两头可发表"盾牌（仅留次级点）；自由改写 GER 作独立后融合线（收编为 reward 基础设施）；δ_corr 作理论贡献（降 ROVER 借用）；确证抽取的 NIST 信标 / 全新会话 / burn / commit–reveal 仪式（简化为提交先于选择的确定性脚本 + 固定种子，逐字节可复现，如实称 public deterministic evaluation）；**S3 成本类成功门（≥30% 调用降幅 + Pareto 支配，数学不可达，R1 撤除）**；**H5 15%→10% SESOI 自动回退（S-3 撤除）**；**每版 α 阶梯 / 5-look sequential trial（S-6/S-7 → G3 单一最终确证版本制取代）**；**qrels-conditioned 310 库作确证语料（F′-3 撤除，改全语料）**；**proxy 误称 verifiable reward（F′-4 撤除，改 label-free proxy + U/Û）**；**"不可预测 custody"签字门（F′-1 撤除，改 public deterministic evaluation）**；**K=1 标 equal-budget（F′-5 撤除，改低成本基线在族外）**。

**证据分级**：全部先验数字带 claim-ledger ID；status valid|directional 者方可引（directional 一律 Stage-1 假设级），invalid 仅限本附录、无 ledger 条目者标 unverified。Stage-1 证据保持其产生阶段等级，须在 Stage-2 大样本下重立方升级。
