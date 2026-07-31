---
title: "R2 开题报告 v14：博导视角的文献与技术可行性复审"
date: "2026-07-31"
artifact_type: "REVIEW"
campaign: "system-first-stage1c-v2"
round: "round-13"
review_target: "wiki/survey/workbench/stage1c-portfolio/proposals/2026-07-29-r2-coreview-draft.md"
review_target_commit: "dc5b04857bd8d07a0251829a0fd3165ad7b2355e"
review_target_git_blob: "ea2cdd0197741f04af894f30146ddfcae35fe5e7"
review_target_blob_sha256: "663c84d4f85320e83475702954b25add57bf2360ca99979447ddedde04f0f9e1"
review_target_size: "62513 bytes; 726 lines; Git blob bytes"
responds_to: "round-12 zero-MAJOR internal-consistency review and v14 editorial closure"
verdict: "MAJOR_REVISION_REQUIRED_BEFORE_FORMAL_OPENING"
research_direction_assessment: "WORTH_CONTINUING_IF_NARROWED_AND_REBASELINED"
formal_opening_authorized: false
permission_note_issued: false
authority_effect: "REVIEW_ONLY_NO_OWNER_DECISION_NO_EXECUTION_GRANT"
human_signature_claimed: false
model_or_metric_execution_authorized: false
stage2a_authorized: false
novelty_verdict: "NOT_ISSUED_CLOSEST_NEIGHBOR_SUFFICIENCY_FAILED"
---

# R2 v14 博导复审：方向值得继续，但本版暂不允许正式开题

## 一、裁决

**裁决：`MAJOR_REVISION_REQUIRED_BEFORE_FORMAL_OPENING`。本轮不出具“允许开题 notes”。**

这不是对 R2 方向的否定。v14 已经从早期的概念混用稿，进步为一份有明确系统边界、有因果臂、
有失败出口、也开始认真区分有效性/合理性/可靠性/效率的研究蓝图。特别是 §1.3 对**知识组织、
知识供给、知识使用**的定义，§6.2 的因果阶梯，以及 §6.5 的四层评价，均达到“可以继续打磨”
的质量。

但正式开题的门槛不是“内部没有矛盾”，而是：**主问题已经锁定，最近邻已经读透，增量能够被
准确归因，主载体与最强基线已经冻结，核心技术风险值得用博士阶段的资源去验证。** v14 尚未
满足这几项。最关键的新事实是：提案在 §8/§9 明列为“未读”的 contextual biasing、GER、
retrieval-ASR 与 Speech-Hands，恰好覆盖它的核心结构；一手文献补扫还发现了提案未列出的
PRISM（EMNLP 2023），其“为实体合成语音—构造声学/文本 key-value memory—推理期近邻匹配”
与 §2.3 的发音库机制高度重合。

因此，round-12 的“零 MAJOR”只能理解为**件内一致性收敛**，不能外推为文献充分性或技术
独立性通过。事实上，round-12 自己的失效条件 7 已预先规定：若 Speech-Hands 或 biasing/GER
线显示已占据 training-free 双源动作选择或发音候选构造，则 §8 的组合格与相关判定必须重开。
本轮一手资料补扫已经触发该条件。

一句话评价：**R2 有值得做的科学内核，但 v14 把一条可能成立的内核扩写成了三个研究方向，并
在最近邻未读、主战场未定时提前提出“新基线/替代 ASR+GER”的强主张；现在签字，会把后续大部分
时间消耗在重新定义问题，而不是验证问题。**

---

## 二、值得肯定的部分

### 2.1 为什么黑盒模型仍需要知识，已经有了可用的问题意识

提案抓住了两个不同、且都真实存在的缺口：

1. **参数边界缺口**：冻结模型不能可靠吸收训练截止后的事实、私域实体、长尾术语、可审计出处
   与任务现场的新信息，外置知识因此不是“再提示一次”，而是参数外信息通道。
2. **音频观测缺口**：语音中的实体可能先被听错；错误实体又会生成一组彼此一致但整体错误的
   检索证据。此时只增加检索深度会放大错误，必须让系统在“重新解析音频”与“搜索外部事实”
   之间做因果上不同的动作选择。

第二点是 R2 最有研究价值、也最贴合总课题 black-box control plane 的位置。它比泛化的“给
omni 加 RAG”更具体：**知识不是总要引入，而是在模型观测不足、事实不足或证据冲突时，作为
可撤销、可审计的外部干预进入系统。**

### 2.2 概念词典已经明显改善

§1.3 给出的三分法在定义层基本正确：

| 形式 | 被改变的对象 | 典型决策 |
|---|---|---|
| 知识组织 | 存储与地址空间 | 单元、schema、关系、索引、版本、出处、key/value |
| 知识供给 | 从未见到已取回 | 何时取、从哪取、用什么 query、取多少、何时停 |
| 知识使用 | 从已取回到影响答案 | 准入、融合、冲突、归因、拒用、abstain |

这回应了早期版本最严重的概念混淆。§6.5 也已经把“引入知识是否有效”“引入是否合理”“用了
多少资源”分开计量，而不是只看最终准确率。

### 2.3 实验框架开始具备可证伪性

以下设计是正确方向：

- A1/A1′ 把“找不到正确知识”和“拿到知识但不会用”分开；
- A3 对 A2 隔离准入门价值；
- A4b−A4a 尝试隔离音频特有调度信号；
- wrong→correct 与 correct→wrong 同报，防止只展示收益；
- always/never、matched-cost、random-config、gold-entity/evidence 等对照较完整；
- K1–K5 与 K-Gate 允许机制失败后降级，而不是事后改口径。

这些内容可以保留，并应成为收窄后提案的骨架。

---

## 三、必须关闭的 MAJOR 问题

### MAJOR-1：最近邻文献不是“补充项”，而是已经改变核心主张的承重证据

v14 在 §1.2、§2.3、§8 中对近邻的概括是：“biasing 需每句预给候选表且训练进解码器；GER
回不到信号；组合格读集内为空”。这组概括在补扫后不能成立。

| 一手工作 | 已经实现的结构 | 对 v14 的直接影响 |
|---|---|---|
| [PRISM / Speech-enriched Memory, EMNLP 2023](https://aclanthology.org/2023.emnlp-main.916/) | 为稀有实体逐项合成语音，将声学/语言状态作为 key、文本 token 作为 value，推理期近邻检索；覆盖 Transducer 与 Whisper | 与“G2P/TTS 构造实体发音库—冻结表示作声学 key—检回实体 value”高度重合；发音库不能再被默认当作 R2 的机制创新核 |
| [Lei et al., 2024](https://arxiv.org/abs/2409.15353) | 先从语音检测实体，再以实体假设检索音近实体，最后做上下文化解码 | 已覆盖“可能听错的实体假设→音近候选→LLM 裁决”的三段链；虽有训练，不在严格 TF 边界内，但必须作为结构最近邻与强基线 |
| [Retrieval Augmented Correction, 2024](https://arxiv.org/abs/2409.06062) | 由错误 ASR 假设生成查询，从实体向量库检索，再交给适配 LLM 纠错 | 已覆盖实体库、错误假设查询、检索增强 GER；提案不能把 GER 概括为无检索或只在 N-best 上盲纠错 |
| [DARAG, ACL Findings 2025](https://aclanthology.org/2025.findings-acl.125/) | 命名实体 datastore + 检索增强生成式纠错 | 是实体纠错与知识检索结合的直接 trained comparator |
| [RAG context discovery for ASR, EMNLP Findings 2025](https://aclanthology.org/2025.findings-emnlp.768/) | 自动发现上下文、冻结词表、黑盒 plug-and-play、无需 ASR 微调；在 TED-LIUM3/Earnings21/SPGISpeech 上验证 | 反驳“contextual biasing 都需要逐句人工候选表”；同时给出 R2 可直接采用的长音频/财报载体与 no-context/oracle 对照 |
| [RECAST, EMNLP Findings 2025](https://aclanthology.org/2025.findings-emnlp.203/) | 从预训练 ASR decoder state 检索大型文本 keyword 库，再提示下游 speech LM | 覆盖声学状态→词项检索、位置定位、大词表效率；虽然 retriever 经过训练，仍是必须击败或解释信息边界差异的强基线 |
| [BR-ASR, Interspeech 2025](https://www.isca-archive.org/interspeech_2025/gong25_interspeech.html) | speech-to-bias 检索、同音干扰课程、大到 200k 词表，检索结果可接多种下游 ASR | 对发音库的可扩展性、同音负例与延迟提出了现成强基线 |
| [WCTC-Biasing, Interspeech 2025](https://www.isca-archive.org/interspeech_2025/nakagome25_interspeech.html) | 无需重训练的 wildcard CTC keyword spotting 与层间 biasing | 直接否定“biasing 必然训练”的全称表述；虽需模型中间层，不满足 API-only，但必须列入方法边界表 |
| [RAG-Boost, MLC-SLM 2025](https://www.isca-archive.org/mlcslm_2025/wang25_mlcslm.html) | 实时 ASR 部分假设查询音频-文本与领域词向量库，并与当前假设融合纠错 | 已覆盖 live hypothesis→audio/text store→LLM 融合链 |
| [Speech-Hands, 2026](https://arxiv.org/abs/2601.09413) | 学习“信任自身还是咨询外部音频感知”的显式反思决策，覆盖 ASR 与 audio reasoning | 与“何时重听/何时相信当前核”的 agentic 控制目标直接相邻；trained 与 black-box 边界是差异，不是可以不读的理由 |

这不等于“R2 已经没人可做”。仍可能成立的增量是一个**合取命题**：在 API-only、参数冻结、
无新增代答 LLM 的边界下，用可审计的确定性信号，在“重解析原始音频”和“检索外部世界知识”
之间做 reward-guided 分配，并证明它在 matched cost 下优于强 plug-and-play ASR/RAG 基线。

但这与当前“发音库本身是机制核”“知识系统替代 ASR+GER”的表述不是一回事。最近邻矩阵没有
重做之前，提案的创新增量、对照臂和主战场都会错位。

**关闭条件**：至少完成上述十篇的逐篇 D2 级条目；将 §8 改为“机制单元—训练态—信息访问—
动作空间—输出权—公开载体—可复现实验”的 prior-difference matrix；每一项 R2 主张必须指向
一个最近邻并说明新增变量，禁止再用“整条线都训练/都需人工表”的全称句。

### MAJOR-2：三形式在词典里分开了，在研究问题与模块归因里仍然混在一起

概念定义已经合格，但章节和实验变量还没有按定义落地：

- §2 名为“谁搜索谁”，实际同时改变 key 表示（组织）、query/召回（供给）和 world-knowledge
  rescore（使用）；
- §3 把 value 定义为“检回内容如何被使用”，等于把“使用”重新塞回“组织”；
- §4 的门控环同时拥有 SEARCH/RE_RESOLVE（供给）与 ADMIT/REJECT（使用）；
- TFRL 又联合搜索切片、面、融合权重、候选宽度、阈值和物化边界，若整体提升，无法回答究竟是
  组织、供给还是使用产生了增益。

必须把“知识是什么样”“知识怎么到达”“知识如何影响输出”变成三个正交接口，而不是三个叙事
章节：

| 层 | 输入→输出 | 允许优化的变量 | 独立主判据 | 对应系统模块 |
|---|---|---|---|---|
| ORG | 原始材料→带版本/出处的可寻址单元 | chunk、facet、key、index、materialization | recall/coverage、冲突与出处完整性 | knowledge builder/index |
| SUPPLY | 当前状态→候选证据集 | trigger、query、retriever、top-k、stop/budget | retrieve/skip、query recall、under/over-call | controller/retriever |
| USE | 候选证据集→上下文/答案影响 | admit、fusion、rescore、conflict、abstain | evidence utility、correct→wrong、grounding | admission/arbitration |
| OPT | dev reward→冻结配置/策略 | 搜索算法与预算 | 对 random/equal-budget optimizer 的增益 | TFRL/配置优化器 |

每个主实验一次只改一层；跨层联合优化只能作为系统级最终臂，不能承担单层机制归因。

**关闭条件**：重写 RQ/Hypothesis/Arm 映射表，至少给出 H-ORG、H-SUPPLY、H-USE 三条可独立
证伪的假设；PS-abl 不能再同时包含发音 key、候选检索与世界知识重排；A3 必须只改变准入，
A4b 必须只改变供给调度。

### MAJOR-3：最强主张的载体和 incumbent 仍是 PENDING，不能作为正式开题的中心命题

§0 声称“omni+知识系统替代专用 ASR+biasing/GER 成为新基线”，但 §5.1 又明确写
`PENDING_CARRIER_SELECTION`。这不是一个可在开题后补的实施细节，而是决定研究问题含义的
构成部分：在 LibriSpeech bias list、Earnings21、会议/播客实体 QA、语音助手 rare entity 上，
“知识”“实体”“任务效用”和最强 incumbent 都不同。

尤其在补扫后，incumbent 不能再写成一个抽象的“ASR+biasing-GER”合成臂。至少要区分：

- retraining-free 内部可见方法（PRISM、WCTC）；
- trained retrieval/biasing 上界（RECAST、BR-ASR、Lei et al.）；
- black-box/no-ASR-finetuning 的自动上下文发现（Siskos et al.）；
- retrieval-augmented GER（Pusateri/DARAG）；
- omni/agentic 决策（Speech-Hands）。

它们的信息边界不同，不能挑一个较弱实现后称为“赢了 incumbent”。

**关闭条件**：正式开题稿必须锁定一个主载体、一个复制载体、一个诊断集；给出版本、split、
核心样本定义、主指标、最强可运行基线、oracle 与 power analysis。自建 150–200 题先导集可以
做诊断或补充，不宜同时承担提出问题、选择样本和证明方法三个角色。

### MAJOR-4：当前规模是三到四篇论文，不是一个有优先级的博士开题主线

v14 同时要做：实体发音记忆、口音变体、会话内音色克隆、多面 key 联邦、长音频 T2 库、
组织结构的 reward-guided 搜索、双源调度、准入/冲突处理、跨核可移植性，以及一套新数据集。
这些组件各自都可能失败，而且彼此依赖，导致“每个失败都能降级，但没有一个结果必须产出”的
风险。博士开题需要最小承重脊柱，而不是功能组合清单。

建议收窄为：

> **主问题**：在冻结、API-only 的 omni 核上，外置控制器能否利用音频侧不确定性，在
> RE_RESOLVE 与 SEARCH_EXTERNAL_KNOWLEDGE 之间做 training-free、可审计、matched-cost 的
> 动作分配，并在实体/知识密集语音任务上同时提高任务效用、降低错误知识注入？

对应工作包：

1. **WP0 最近邻与载体冻结**：关掉 MAJOR-1/3；
2. **WP1 核心论文**：双源调度 + 准入，使用朴素且强的固定知识组织；
3. **WP2 条件扩展**：只有 WP1 证明知识确有可恢复 headroom，才研究多面/长音频组织优化；
4. **WP3 探索项**：个性化 TTS/voice-clone key；不再承载正式开题的核心成败。

发音库可以保留为知识源/基线组件，但在 PRISM 与 Lei et al. 之后，不宜未经 prior-difference
论证就继续挂“机制核”。

### MAJOR-5：若要称为 TFRL，必须说明它不只是 dev 集上的超参数搜索

§3.4/§6.3 当前的档 A 是在 dev 上调 α/β/γ/δ、阈值、top-k、切片、融合权重，然后冻结进 test。
这是合理的 derivative-free 配置优化，但仅凭“以 reward 为目标”并不能自动成为 RL。若没有
episode-level policy update、credit assignment、探索策略或明确的 contextual bandit/black-box
policy optimization 形式，审稿人会把它判为 hyperparameter optimization。

另外，手写线性 V̂ 的量纲、可识别性与校准方式仍未闭合：多个分量高度相关，α/β/γ/δ 可吸收
特征尺度，`argmax V̂` 又跨不同动作族比较不可直接同尺度。五路信号还停留在义务清单，说明策略
并未真正实例化。

**关闭条件**：二选一并写死。

- 若保留 TFRL：定义 MDP/bandit 对象、trajectory reward、优化器、探索预算、离线/在线边界、
  credit assignment，并与 random search、Bayesian/evolutionary search、固定规则等预算比较；
- 若只做 dev 配置搜索：改称 reward-guided black-box policy/configuration search，不用 RL
  身份承载方法创新。

### MAJOR-6：技术风险需要更锋利的反证，而不是只登记“不过就降级”

### 6.1 发音库的风险

冻结通用音频 encoder 未必在音素近似上形成可检索空间；TTS 伪影、语速、共发音、噪声与口音
可能主导距离。必须至少比较：字面/别名检索、G2P/phoneme edit distance、PRISM 式 synthetic-
speech memory、冻结声学 encoder、trained retrieval 上界。只有冻结声学 key 在同预算下超过
简单 phonetic baseline，才说明它值得做。

### 6.2 世界知识重排的风险

“世界上存在 Meyer 会议、不存在 Mayer 会议”是过于理想化的例子。真实世界常见两候选都存在、
私域名字不在 web、热门实体压过长尾正确实体、证据源本身冲突。必须加入：双候选均存在、正确
候选无公开证据、库中无正确候选、热门错误候选、别名/跨语言实体、恶意或陈旧证据等负类，并
把“拒绝改写”作为合法动作。

### 6.3 voice cloning 的风险

逐候选克隆再比对的成本可能随候选数线性爆炸；TTS 与自然语音分布差异也可能让个性化 key
变差。它还引入 consent、speaker leakage、第三方姓名/PII 与模型许可问题。现有会话内边界是
好起点，但应升为明确红线，并把该组件降为 WP3。优先验证更简单的 speaker normalization/
speaker-conditioned embedding；只有其失败且 clone key 有独立增益时再升级。

### 6.4 “知识层结构上吃不掉”的风险

模型无法覆盖训练截止后事实、私域知识和出处审计，这支持**某些知识需求长期存在**；但不能由
“文本 RAG 仍存在”推出“本提案的知识层组织结构不会被模型吃掉”。后者是经验性假设，不是
结构定理。应改成带范围的可证伪命题：在动态/私域/可审计信息分布上，外置知识对当前冻结核有
正 oracle headroom；若 headroom 消失，相应组件蜕壳。

---

## 四、如何更严密地回答“为什么引入知识、是否引得对、用得是否高效”

建议把评价写成一条从**必要性**到**净价值**的证据链：

| 问题 | 必须回答的反事实 | 主读数 | 失败含义 |
|---|---|---|---|
| 是否需要知识 | 给 gold entity/evidence 后是否存在可恢复增益？ | oracle headroom：A1/A1′−A0；need/no-need 分层 | 无 headroom：载体或核不适合，不能评价检索策略 |
| 是否取到了对的知识 | 正确证据是否被召回，错误实体是否被放大？ | recall/coverage、entity-hit、query correctness、source validity | 组织/供给失败 |
| 是否在对的时机引入 | retrieve/skip、re-resolve/search 是否与离线最优动作一致？ | 触发混淆矩阵、under-call、over-call、policy regret | 供给/调度失败 |
| 是否正确使用 | 同一证据集下，准入/融合是否改善答案且不污染？ | A3−A2、correct→wrong、unsupported claim、removal/swap | 使用失败 |
| 是否产生净效果 | 相对无知识和最强基线是否有稳定增益？ | paired ΔU、CI、worst-group、replication | 系统主张失败 |
| 是否高效 | 同等成本下是否更好，或同等质量下是否更省？ | matched-cost ΔU、P95 latency、cost/corrected case、Pareto frontier | 只证明“多花资源可变好” |

v14 已经拥有上述大部分原件，但把效率降为“只记账、不进主判据”与“替代 incumbent/成为新
基线”的强主张不相容。若只做 capability-first discovery，可以把绝对成本放宽；但仍需至少有
一个 matched-cost 或 quality-constrained 结论。否则无法区分控制策略的价值与额外调用资源的
价值。

建议预注册三个效率读数：

1. `ΔU | matched_cost`：总 core/tool/retrieval 成本匹配时的效用差；
2. `cost_per_net_correction = total_incremental_cost / (wrong→correct − correct→wrong)`；
3. gate 相对 always-call 的质量非劣条件下，P50/P95 latency、调用次数与音频秒数节省。

索引构建、TTS/克隆、快照与标注成本必须做摊销敏感性分析，不能只报在线成本。

---

## 五、建议重写后的最小假设集

正式开题稿不应再以“做一个完整知识系统”为假设，而应给出少量可被数据否定的命题：

- **H0 / 必要性前提**：在锁定主载体上，gold entity/evidence 相对裸核存在超过 SESOI 的 oracle
  headroom；否则 R2 不进入主实验。
- **H1 / 音频特有供给**：matched cost 下，读取音频不确定性信号的 A4b 优于不读取该信号的
  A4a，并降低由错误实体导致的错误检索链；这是 R2 最核心的独立性主张。
- **H2 / 知识使用**：固定候选证据集时，显式准入/冲突处理相对无条件拼接提高净效用，并降低
  correct→wrong；这隔离“会不会用知识”。
- **H3 / 系统价值**：在公开主载体与复制载体上，API-only frozen omni controller 相对最强
  plug-and-play contextual ASR/RAG/GER 基线取得预注册的效果增益或 matched-cost Pareto 改善。
- **H4 / 条件扩展**：只有 H0–H3 成立后，多面组织相对调优的单面/稀疏/phonetic baseline 有
  任务端增益；否则组织优化不进入论文主张。

PRISM 式发音记忆、phonetic retrieval、世界知识重排、clone key 都是 H1/H3 下可比较的实现，
不应各自再被写成并列的博士主问题。

---

## 六、允许开题前的验收清单

以下八项全部关闭后，才建议进入下一轮“是否允许正式开题”的签字审查：

1. **最近邻闭环**：完成 PRISM、Lei、Pusateri、DARAG、Siskos、RECAST、BR-ASR、WCTC、
   RAG-Boost、Speech-Hands 的逐篇源核与 prior-difference matrix。
2. **主句收窄**：把“知识系统替代 ASR+GER”改为一个带任务、信息边界、成本条件和失败出口的
   单句研究问题；删除未经验证的“新基线”“结构上吃不掉”全称表述。
3. **三形式落到模块**：ORG/SUPPLY/USE/OPT 各有独立输入输出、独立实验臂与独立主读数。
4. **载体冻结**：一个公开主载体、一个公开复制载体、一个只承担机制诊断的最小对集；不以自建
   集单独支撑核心结论。
5. **最强基线冻结**：按信息访问边界分组，至少包括简单 phonetic baseline、retraining-free
   baseline、trained upper bound、retrieval-GER、black-box context discovery。
6. **方法身份闭合**：TFRL 或 reward-guided configuration search 二选一；给出优化器、预算、
   特征尺度/校准、随机搜索对照与冻结协议。
7. **效率进入判据**：至少一个 matched-cost 主结论、cost/net-correction、P95 latency 和索引/
   TTS 摊销；不能只做九维日志。
8. **范围与伦理**：voice cloning 降为条件探索项；consent、会话内使用、不留存、不输出、不涉
   第三方 PII 升为红线；给出无法合规时的无克隆回退路线。

建议 Fable5 提交 v15 时同时附一份不超过两页的“开题签字包”：研究问题一句话、三条主假设、
主/复制载体、五个最强基线、核心臂图、主判据与 kill criteria。正文可以长，签字依据必须短且
不可歧义。

---

## 七、给 Fable5 的导师 notes

> 这版不是不能做，而是还不能以当前强度正式开题。你已经把系统内部逻辑补得很细，但外部
> 最近邻没有进入问题定义，导致“发音库机制核”“contextual biasing/GER 的边界”“新基线”
> 三个承重判断发生偏移。先不要继续给系统加组件。把 PRISM 2023 到 Speech-Hands 2026 这条
> 近邻线读透，锁死主载体，把研究主线收敛到“冻结黑盒条件下，音频不确定性如何调度重解析与
> 外部知识，并在 matched cost 下减少错误知识注入”。多面组织可以做第二阶段，音色克隆放到
> 条件探索。完成本评审八项后，我愿意按正式开题标准再审；在那之前，不建议 owner 签署允许
> 开题 notes。

---

## 八、本轮一手文献补扫清单

除 MAJOR-1 表中的十项核心近邻外，本轮还核对了以下一手来源，用于判断历史基线、合成语音
风险、SpeechLLM contextualization 与检索式 speech understanding 的边界：

- [Class LM and Word Mapping for Contextual Biasing, Interspeech 2020](https://www.isca-archive.org/interspeech_2020/huang20f_interspeech.html)：动态实体、发音映射与 context FST；说明“发音知识进入 biasing”并非新问题。
- [Effective Training of Contextual Biasing Adapters with Synthetic Audio, Interspeech 2023](https://www.isca-archive.org/interspeech_2023/naowarat23_interspeech.html)：合成音训练与真实/合成表示差异；支撑 TTS domain-gap 风险。
- [Record Deduplication for Entity Distribution Modeling, Interspeech 2023](https://www.isca-archive.org/interspeech_2023/huang23g_interspeech.html)：动态实体集合与误识别实体分布；说明热门/长尾先验和实体库更新本身就是研究变量。
- [CB-Whisper, LREC-COLING 2024](https://aclanthology.org/2024.lrec-main.262/)：open-vocabulary keyword spotting 与 bias list，是 Whisper 系 contextual biasing 的基线入口。
- [Contextual Biasing Speech Recognition in Speech-enhanced LLM, Interspeech 2024](https://www.isca-archive.org/interspeech_2024/gong24b_interspeech.html)：SpeechLLM 上的 contextual biasing，不能把该线只定位成传统 ASR decoder 内部方法。
- [RASU: Retrieval Augmented Speech Understanding, Interspeech 2024](https://www.isca-archive.org/interspeech_2024/yang24b_interspeech.html)：speech segment/transcript retrieval 与生成式理解，覆盖语音检索增强的另一信息边界。
- [How to Leverage Synthetic Speech for LLM-Based ASR Systems?, 2026](https://arxiv.org/abs/2606.29031)：直接分析 synthetic-real representation gap；虽为同期预印本，仍应作为 clone/TTS key 风险证据跟踪而非承重基线。

本轮合计核对 17 项直接相关的一手工作。数量本身不构成充分性；核心要求仍是把这些工作映射到
R2 的具体主张、信息边界、实验臂和公开载体。

---

## 九、复审边界、证据与失效条件

本轮做了两类检查：

- 对 Git blob `ea2cdd0`（726 行、62,513 bytes）逐节复核问题定义、三形式、方法、臂族、判据、
  载体和义务清单；
- 对提案自己标为未读的最近邻方向做一手来源补扫，优先使用 ACL Anthology、ISCA Archive 与
  arXiv 作者页；重点深读了 PRISM、Lei et al.、Siskos et al.、RECAST、BR-ASR、Speech-Hands，
  并核对 Pusateri、DARAG、WCTC、RAG-Boost 等结构与边界。

本轮**没有**运行模型/API、获取数据集、执行指标、复现方法或验证数值；不发布 novelty verdict，
只裁定“当前最近邻证据不足以支撑正式开题中的独立性/基线/技术价值表述”。公开文献检索仍不
保证穷尽；若后续发现更接近的 training-free API-only 双源控制工作，必须再次收窄主张。

本评审不翻改 round-12 原文，也不代行 owner 生效裁定；它基于 round-12 明列失效条件后出现的
新证据，重新判断正式开题门槛。本文不授予 Stage-2A、模型/API 调用、数据获取、指标运行、原型、
push 或 wiki 发布权限。审计层文件提交后不得原位改写；后续用 response/amendment 与新一轮复审
关闭。
