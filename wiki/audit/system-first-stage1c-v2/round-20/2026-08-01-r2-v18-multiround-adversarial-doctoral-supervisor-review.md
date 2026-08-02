---
artifact_id: "SF-STAGE1C-R2-COREVIEW-ROUND20"
role: "R2 v18 开题报告的多轮隔离对抗式博导审查"
date: "2026-08-01"
campaign: "system-first-stage1c-v2"
round: "round-20"
target_path: "wiki/survey/workbench/stage1c-portfolio/proposals/2026-07-29-r2-coreview-draft.md"
target_commit: "eea6695f50b29ca6a5f43fbd3714a8d293e594f4"
target_git_blob: "e837886a3faf9cfb1c9712683510e1b0e0bbc461"
target_sha256: "780b737baa0ced5b14dbdfe48776df93c234cdb72c4d9328921de3d0bc17d9bf"
target_bytes: 196116
target_declared_version: "SF-STAGE1C-R2-COREVIEW-V18"
review_scope: "开题阶段：研究问题、概念体系、学界研究现状、技术可验证性、评价逻辑与报告可签署性"
novelty_review_in_scope: false
priority_or_firstness_review_in_scope: false
model_or_dataset_execution_performed: false
execution_authority_granted: false
permission_note_issued: false
verdict: "MAJOR_REVISION_REQUIRED_BEFORE_FORMAL_OPENING"
---

# R2 v18 多轮隔离对抗式博导审查

## 1. 审查结论

**结论：`MAJOR_REVISION_REQUIRED_BEFORE_FORMAL_OPENING`。当前不建议签署正式开题许可，故本轮不出具允许开题的 notes。**

这不是方向否决。相反，本报告所选择的研究主题——在冻结黑盒 speech/omni 核外围研究外部知识的组织、供给、使用及其选择性控制——具有明确的学术问题、成熟的相邻研究基础和可验证的技术价值。v18 也已经实质性修复了上一轮最突出的问题：总问题、RQ0–RQ4、ORG/SUPPLY/USE/OBS/CONTROL 词典、Need→Access→Use→Outcome→Cost 评价链和模块映射都已出现于正文。

暂不允许正式开题的原因，是这些定义还没有完全转化为一棵**主张范围与实验识别能力一致**的问题树；同时，学界现状仍漏掉数条直接语音/音频研究线，统计判定和档 B 控制过程还存在会改变结论含义的技术错误。它们都是报告层可关闭的问题，不要求现在运行模型、下载数据、复现论文或给出最终数值阈值。

本审查严格服从当前阶段边界：**不评价任务或方法新颖性，不判断是否首创，不要求 prior-difference 证明，不以“是否有人做过相似系统”作为开题否决理由。**

## 2. 对抗式审查方法与隔离性

本轮采用四个互相独立的镜头；前三个镜头均从零上下文读取当前有效边界与目标 proposal，不读取 round-03..19 的结论、自评或回应链：

1. **问题—概念镜头**：只审总问题、RQ 层级、ORG/SUPPLY/USE/OBS/CONTROL 边界、模块归因和“为什么引知”。
2. **学界现状镜头**：重新搜索 2021–2026 一手来源，按 contextual ASR、speech/acoustic memory、ASR correction、audio retrieval/RAG、speech/omni factual knowledge 五类重建问题地图。
3. **方法—评价镜头**：只审待验证技术点、实验可识别性、统计判定、可靠性、效率和可执行性。
4. **主审反证轮**：对前三路发现逐项回查 proposal 原文，并用 ACL Anthology、ISCA Archive、AAAI、IEEE/作者预印本等一手页面核验关键遗漏；对 `Audiopedia`、`TED-EL`、`iKnow-audio`、Xiang et al. 2025、CopyNE、N-best T5、HypR 等逐项做存在性与问题构念复核。

三路隔离审查均独立收敛到 `MAJOR_REVISION`；主审反证轮没有推翻其核心结论。仓内机械复查进一步确认：`Audiopedia`、`TED-EL`、`iKnow-audio`、CopyNE、N-best T5、HypR、Adaptive Contextual Biasing 和 CTC-Assisted LLM-Based Contextual ASR 均未进入目标正文；ContextASR-Bench 仅处于矩阵/未来义务位置，未进入 §1.7 的领域主线。

## 3. 对 round-19 五个报告级问题的关闭判断

| round-19 问题 | v18 状态 | 本轮判断 |
|---|---|---|
| 总问题与 RQ 层级缺失 | 已增加一句话总问题、RQ0–RQ4 和 WP1–WP3（L17–32、L155–176） | **基本关闭**，但各 RQ 的主张范围仍大于实验识别范围，见 MAJOR-1 |
| ORG/SUPPLY/USE 与 OBS/CONTROL 混用 | 已给唯一词典与动作标签（L228–256） | **定义层关闭、操作归因层部分关闭**；SUPPLY 与 CONTROL、USE 与终结动作仍有交叉 |
| 学界现状不是问题地图 | 已重写为 L1–L5 五线（L290–369） | **部分关闭**；框架正确，但直接研究线仍有重大遗漏且 L2/L4/L5 内部混类 |
| 黑盒条件下为什么引知不清 | 已给动态性、私域性、情境性、可审计性、模态读取不稳定及反向边界（L133–142） | **论证层关闭**；主载体能支持的经验范围仍需收窄或补第二载体 |
| 有效性、合理性与效率评价不清 | 已给五段链与五类指标（L144–153、L868–894） | **框架层关闭**；效率尚只是记账，统计“判死”语义错误，可靠性没有进入总主张成立条件 |

## 4. 必须关闭的重大问题

### MAJOR-1：RQ 的承诺范围与实验能够识别的构念不一致

总问题和 RQ0–RQ4 的文字层级已经清楚（L17–32），但目前仍是“多个局部可判模块的集合”，还不是一棵由总问题统领、每个分支都能被对应设计回答的问题树。

具体表现为：

- **RQ1 过宽**。RQ1 承诺研究 key、value、schema、索引、版本和出处（L28–32），但正文把 value 合同明确设为“非实验轴”（L547–551）；K5 实际比较的是 key/切片/面/物化等配置 bundle（L1015–1027）。现设计能回答“key/index 配置是否有价值”，不能独立回答 value 形态、版本、出处与冲突 schema 如何建模及是否有效。
- **RQ2 的主判据更像 CONTROL，而不是 SUPPLY**。RQ2 承诺回答何时查、查什么源、query 如何构造与声学不确定性如何影响供给；但 H-SUPPLY 的主差分是 A4b−A4a，即“是否让感知信号进入 router”（L782–803）。多假设 query 只作伴读，SRC-sel 也没有独立成立判据。这会把“供给对象/来源的价值”与“控制器如何选动作”混为一个贡献。
- **RQ3 过宽**。RQ3 同时承诺核验、准入、融合、冲突、引用与拒答；主实验 A3−A2 只在同候选集下识别“准入是否有价值”（L801、L1007–1014）。这是值得做的清晰问题，但不能替代整组 USE 问题。
- **RQ4 成为兜底层**。RQ4 同时承载配置优化、运行期控制、记录/评价和整合系统主张（L174–176、L783–786），包含 K1a、K2、K-RL、K-OPT、K-NB 等不同构念，无法由一个单一结论关闭。
- **三形式仍有操作交叉**。词典把触发/停止写入 SUPPLY 变量（L233），后文又把触发裁定归 CONTROL；router 被标为 `SUPPLY×CONTROL`（L172）。USE 的输出含答案/拒答（L234），但动作表又把 ANSWER/ABSTAIN 作为独立终结动作。定义层互斥不等于操纵变量和因果归因已经互斥。

**关闭标准：**

1. 给每个 RQ 固定一个主构念、一个主操纵、一个同层对照、一个判定载体、一个主结论和一个失败出口。
2. RQ1 二选一：收窄为 key/index/切片/面组织；或增加同候选集下的 value/schema/version/provenance 对照与对应指标。
3. RQ2 至少把 query、source 或 depth 中一个供给变量升为主实验；感知信号是否进入 router 的差分归 CONTROL，不再代替 SUPPLY 结论。
4. RQ3 二选一：明确只研究“证据准入”；或补足融合、冲突、引用、拒答的析因设计。不能用一个准入差分覆盖全部使用形式。
5. 将 RQ4 至少拆成“控制/优化”和“系统评价”两个子问题，或明确其中一个只是横切方法而非独立学术问题。
6. 增加总问题级决策表：RQ0–RQ4 哪些组合导出“机制成立、仅系统有效、范围收窄、工程成功但机制未识别、结论不确定或否定”。

### MAJOR-2：学界现状数量很多，但直接问题域覆盖仍不充分，且组织权重失衡

§1.7 的五线框架是正确方向，已纳入 PlanRAG-Audio、GRGA、DeRAGEC、Voice Memory、MoshiRAG 等新近工作；对训练态、接口边界和知识来源的描述通常谨慎。问题不在“引用少”，而在**直接语音/音频邻居的关键问题链仍缺席，而文本/视觉 donor 占据了过多解释篇幅**。

fresh-search 确认至少以下直接工作必须进入开题现状主图：

- **Speech entity linking → 外部 KB**：TED-EL 已直接定义 speech entity linking，并提供音频、文本与 mention–entity 对齐语料。它不能被一般发音记忆或 ASR correction 替代。
- **Knowledge-intensive audio QA → 外部知识**：Audiopedia 已把 Audio Entity Linking 与外部知识增强用于 knowledge-intensive audio QA。当前把外部世界知识线主要写成 2026 AudioRAG/Omni-DeepSearch，会造成时间线与问题域失真。
- **Audio-centric KG grounding**：iKnow-audio 已用 audio-centric knowledge graph 做声学类别的结构化语义 grounding。故“外部世界知识统一寻址仍是开放面”必须收窄为更具体的版本、出处、冲突、准入、审计和冻结黑盒联合控制问题。
- **系统性 modality-gap 证据**：Xiang et al. 2025 已系统研究 speech–text alignment 与 modality gap；MCR-Bench 进一步给出音频/文本冲突时的 text bias。当前 L5 主要以两篇 2026 工作承重，证据权重倒置。
- **Contextual ASR 的选择、整体实体与大规模评测**：Adaptive Contextual Biasing、CopyNE、CTC-Assisted LLM-Based Contextual ASR 和 ContextASR-Bench 应进入 L1 主线，而不是把 benchmark 留作未来纳排义务。
- **一般 ASR correction 底座**：N-best T5、HypR 及 acoustic/confidence-aware correction 应作为 L3 的通用骨架；否则 L3 被过度等同为实体纠错。

L4 还应强制拆成三类不同信息边界：

1. 同一录音内的结构化索引、规划与重听；
2. 外部音频/语音库检索；
3. 外部世界知识、KB 或 web grounding。

这三类在知识来源、可用载体、评价指标和污染风险上不同，不能只用一条“audio retrieval/RAG”线承载。

**关闭标准：**重写 §1.7，使每条研究线固定回答“研究问题、知识/证据来源、接口与训练态、代表工作、常用载体/指标、已知失败模式”；主文补入上述直接工作；把文本/视觉 donor 压缩成跨域启发；统一 literature cut；增加标准参考文献表（作者、题名、venue/year、DOI/URL、peer-reviewed/preprint 状态）。目前只有编号、D2/TCR 状态和证据 ledger，不是正式开题报告可独立阅读的参考文献系统。

### MAJOR-3：档 B 被称为 contextual bandit，但 proposal 定义的是多步状态转移控制，且在线 reward 不可观测

档 B 声称“运行期按实例状态选动作/配置”，控制器轻量策略可在交互中更新（L553–563）；方法合同却包含动作历史、SEARCH/RE_RESOLVE/RE_SLICE/ADMIT 对后续状态的改变、终结动作和终局 credit assignment（L818–859）。在这里，动作会改变下一步的假设集、证据集与可选动作，故不是标准 contextual bandit 的单步独立决策结构，而是有限时域的序贯控制问题。

同时，proposal 把 reward 定义为离线标定的 `delta_E`，而 `delta_E` 的正式定义依赖真实标签 `y`（L877–879）。正常 test/部署 episode 中并不能即时观察该 reward，因而 ε-greedy/UCB 所需的反馈时点和更新信号不成立。报告还需要说明“运行期更新轻量策略”与“不为本任务新训练任何模型”的红线如何兼容。

**关闭标准：二选一。**

- **方案 A（建议用于开题收敛）**：所有策略学习/标定只发生在 dev；test 上完全冻结，只做确定性或给定种子可复放的序贯宏策略选择；删除“运行期 contextual bandit 更新”和 K-RL 身份主张。
- **方案 B**：正式改写为有限时域 MDP/POMDP 或其他序贯决策合同，明确状态、horizon、转移、可观测反馈、奖励延迟、离线/在线边界、credit assignment 及 TF-Strict 兼容性。此时不能继续把同一过程称为 contextual bandit。

这不是命名小问题：错误的决策过程身份会改变需要的反馈、基线、估计量和可归因结论。

### MAJOR-4：“未证明正效应”被多处写成“证明无效”，统计判定语义不成立

K0 用 `95% 下置信界 < SESOI` 推出“无外部证据 headroom”（L900–905）；K1a 用 `LCB≤0` 判调度杠杆死（L928–933）；K5、K-RL 及若干系统判据沿用同型规则（L1015–1052）。下置信界没有越过正效应阈值，只能说明未建立预期正效应；当区间很宽时，它不能证明效应为零、为负或小到可忽略。power analysis 不能替代等效性/非劣/无效性检验。

**关闭标准：所有主判据统一为三态。**

- `SUPPORTED`：效应下界超过预注册的实质性阈值；
- `REFUTED_OR_NEGLIGIBLE`：效应上界不超过预注册阈值，或通过预注册等效性/ROPE/非劣反向检验；
- `INCONCLUSIVE`：其余情况，包括样本不足、区间过宽和载体无分辨力。

K0、K1a、K1b、K-NB、K-PS、K5、K-RL、K-OPT 及其失败出口都应采用同一语义。报告现在不需要填写最终阈值，但必须先把“阴性证据”和“证据不足”分开。

### MAJOR-5：已建立“成本账本”，尚未建立“效率评价”；可靠性也未进入总主张成立条件

总问题明确承诺评价必要性、有效性、合理性、可靠性与效率（L17–19），五段链又把 Cost 表述为“同等质量需要多少成本”（L144–153）。但 §6.5 实际只列九维成本向量并声明“记账不设限”，等成本、等质量和 Pareto 被后置为诊断且不进主判据（L889–894）。这能回答“用了多少资源”，不能回答“是否更高效”。

可靠性指标包括 run 方差、correct→wrong、worst-group、coverage-quality 和口音分层（L887–888），但 K-NB 的成立主要由平均效果读数承担，可靠性没有形成系统主张的非回归条件。因此“可靠提升”仍可能由平均收益掩盖尾部退化。

**关闭标准：**

1. 若本阶段只做资源透明性，将结论名改成“成本画像/资源占用”，不要称效率评价。
2. 若保留效率主张，至少指定一个比较性 estimand：固定质量下成本、固定成本下效果、增量成本/每个实体修正，或带区间的 Pareto 支配；数值阈值可在 Stage-2A 前预注册。
3. 为系统主张增加最小可靠性条件，例如总 WER 与关键 worst-group 非劣、correct→wrong 上界、coverage 不得通过大量 abstain 人为压低风险。平均准确率不能替代这些条件。

### MAJOR-6：研究计划和正式报告载体仍然过载，最小可执行主线不清楚

当前文件 196,116 bytes、1,652 行。L1370–1633 大量保存 v3–v18、R1–R23 的审计史、修补记录和自评收敛统计。这些内容属于 AUDIT，不应与当前研究问题、学界现状和方法合同共同承担“正式开题正文”角色。它们使读者必须穿越审计日志才能判断科学问题，也与仓内“一份文档只能有一个角色、active truth 不由回应链承重”的协作规范冲突。

执行层同样过载：150–200 题的先导集同时承担必要性、负类、口音、非词面、多 claim、准入、组织和多个判据（L734–750）；整个计划又包含大量系统臂、分层消融、不可直接运行基线重实现和跨载体比较（L788–814、L1290–1339），却没有清楚给出“先做哪个最小实验、失败后哪些支线立即停止”。

**关闭标准：**

1. 主报告只保留当前科学叙事：问题—现状—RQ—假设—方法—评价—计划—风险—参考文献。审计史、逐轮修补、哈希 ledger 和近邻精确数字表移至 AUDIT/附录并由短链接引用。
2. 增加依赖有向的执行表：能力门 → 载体门 → 最小核心实验 → 条件分支 → 独立复制。每阶段列输入、产出、停止条件、资源量级与失败后的收缩范围。
3. 明确 150–200 题只用于构念、流程和方差先导；确认性判据使用由 power 决定、冻结且独立的扩展集。若坚持把先导集直接用于多个确认性结论，必须先给样本分配和多重比较可行性论证。
4. 冻结一个“最小开题主线”。建议只保留：RQ0 必要性门 → 一个 ORG 同层比较 → 一个 SUPPLY/CONTROL 比较 → 一个 USE 准入比较 → 系统级效果/可靠性/成本画像。其余个性化、复杂面联邦、档 B、全部基线重实现均作为条件扩展，不得互为前置。

## 5. 待验证技术点是否值得做

| 技术点 | 博导判断 | 成立条件 |
|---|---|---|
| 区分 OBS 不足、潜在知识未激活与外部知识增补的必要性边界 | **值得，且应作为 RQ0** | 不能只用 gold evidence headroom 代替错误分型；需明确可区分的观测与载体 |
| 声学 key、G2P/语音学 key 与文本 key 的同层比较 | **值得** | 同预算、同候选集、同检索目标；结论限于组织/寻址，不反推整系统 |
| 基于不确定性的“重听还是检索”选择 | **值得，是语音特有的强问题** | 按序贯控制正确建模；把 SUPPLY 内容变量与 CONTROL 动作选择分开 |
| 同候选证据集下的 evidence admission | **值得，且现有 A2/A3 设计较干净** | RQ3 收窄为准入，或另补融合/冲突/引用实验 |
| 多面 key/value/schema 与版本/出处/冲突管理 | **有条件值得** | 必须实际操纵 schema/value 并给独立判据；否则只作为工程合同 |
| 配置族最佳效果超过专用 ASR+GER | **可作为系统级待验假设** | 不应统领 RQ；必须有强基线、可靠性护栏和三态统计判定 |
| 运行期 contextual bandit | **当前定义不值得直接执行** | 先修正为离线冻结策略或正式序贯决策问题，再判断是否保留 |

因此，本轮对技术价值的判断不是“题目不值得做”，而是：**最有价值的技术点已经出现，但需要从巨型系统设计中抽出来，由清楚的 RQ、同层对照和可判定结论统领。**

## 6. 建议的开题问题树

建议把总问题收敛为：

> 在冻结黑盒 speech/omni 核条件下，外部知识在什么任务与错误条件下是必要的，何种组织、供给和使用机制能产生可归因且可靠的任务收益；这些收益如何与音频观测重处理区分，并以效果、合理性、可靠性和成本—效果关系评价？

由此形成如下问题树：

- **RQ0 必要性边界**：何时需要外部知识，何时只需要 OBS；内部潜在知识激活与参数外证据增补怎样区分。
- **RQ1 ORG**：只研究报告实际操纵的组织变量；若保留 schema/value，则给独立对照。
- **RQ2 SUPPLY**：同一控制状态下，query/source/depth 如何影响 Access；触发和动作选择属于 CONTROL 横切层。
- **RQ3 USE**：优先收窄为准入/冲突/拒答中的一个主问题；其余作为后续分支。
- **RQ4a CONTROL/OPT**：固定或离线冻结的序贯策略如何选 OBS/SUPPLY/USE 动作。
- **RQ4b SYSTEM EVALUATION**：整合系统是否有效、可靠，并在什么成本—质量边界内成立。

每个 RQ 用一张同构卡片表达：`构念 → 主操纵 → 同层对照 → 判定载体 → estimand → 三态结论 → 失败后范围`。这样报告可以显著缩短，且不会损失当前已经积累的技术细节。

## 7. 重新送审的签字门

下一版满足下列八项后，才建议进入“是否允许正式开题”的签字审查：

1. RQ1/RQ2/RQ3/RQ4 的承诺范围与主操纵、主判据一一对应。
2. ORG/SUPPLY/USE 的操作归因互斥；CONTROL 只负责选择，不占用被选动作的层贡献。
3. §1.7 补齐 Audiopedia、TED-EL、iKnow-audio、Xiang 2025、MCR-Bench、CopyNE、N-best T5/HypR、ContextASR-Bench 等直接研究，并重构 L4 三类信息边界。
4. 增加标准参考文献表并统一 literature cut；预印本与正式发表状态分列。
5. 档 B 改为离线冻结策略，或改写为正式序贯决策合同；不可继续使用当前 contextual-bandit 说法。
6. 所有主判据采用 `SUPPORTED / REFUTED_OR_NEGLIGIBLE / INCONCLUSIVE` 三态语义。
7. “效率”要么收窄为成本画像，要么给比较性成本—效果 estimand；可靠性进入系统主张护栏。
8. 主报告移除审计史，给出最小核心实验、依赖顺序、先导/确认性数据分工和条件扩展路线。

以上八项均为**报告级关闭项**；重新送审不以 Stage-2A 实验结果、模型调用、数据集运行或新颖性证明为前提。

## 8. fresh-search 关键一手文献

以下文献用于本轮判断“学界现状是否讲清楚”，不是 prior-art 排他性清单：

1. Li et al. [TED-EL: A Corpus for Speech Entity Linking](https://aclanthology.org/2024.lrec-main.1365/). LREC-COLING 2024.
2. Penamakuri et al. [Audiopedia: Audio QA with Knowledge](https://arxiv.org/abs/2412.20619). ICASSP 2025；作者预印本。
3. Olvera et al. [iKnow-audio: Integrating Knowledge Graphs with Audio-Language Models](https://aclanthology.org/2025.emnlp-main.1759/). EMNLP 2025.
4. Xiang et al. [Understanding the Modality Gap: An Empirical Study on the Speech-Text Alignment Mechanism of Large Speech Language Models](https://aclanthology.org/2025.emnlp-main.262/). EMNLP 2025.
5. Wang et al. [When Audio and Text Disagree: Revealing Text Bias in Large Audio-Language Models](https://aclanthology.org/2025.emnlp-main.246/). EMNLP 2025.
6. Modica et al. [Do Factual Recall Mechanisms Carry over from Text to Speech in Multimodal Language Models?](https://aclanthology.org/2026.starsem-conference.28/). *SEM 2026.
7. Wang et al. [Closing the Modality Reasoning Gap for Speech Large Language Models](https://aclanthology.org/2026.acl-long.857/). ACL 2026.
8. Zhou et al. [CopyNE: Better Contextual ASR by Copying Named Entities](https://aclanthology.org/2024.acl-long.147/). ACL 2024.
9. Xu et al. [Adaptive Contextual Biasing for Transducer Based Streaming Speech Recognition](https://www.isca-archive.org/interspeech_2023/xu23d_interspeech.html). Interspeech 2023.
10. [CTC-Assisted LLM-Based Contextual ASR](https://arxiv.org/abs/2411.06437). 2024；预印本。
11. Wang et al. [ContextASR-Bench: A Massive Contextual Speech Recognition Benchmark](https://arxiv.org/abs/2507.05727). 2025；预印本/公开基准。
12. Ma et al. [N-best T5: Robust ASR Error Correction using Multiple Input Hypotheses and Constrained Decoding Space](https://www.isca-archive.org/interspeech_2023/ma23e_interspeech.html). Interspeech 2023.
13. Wang et al. [HypR: A Comprehensive Study for ASR Hypothesis Revising with a Reference Corpus](https://www.isca-archive.org/interspeech_2024/wang24j_interspeech.html). Interspeech 2024.
14. Im et al. [DeRAGEC: Denoising Named Entity Candidates with Synthetic Rationale for ASR Error Correction](https://aclanthology.org/2025.findings-acl.786/). Findings of ACL 2025.
15. Ghosh et al. [Failing Forward: Improving Generative Error Correction for ASR with Synthetic Data and Retrieval Augmentation](https://aclanthology.org/2025.findings-acl.125/). Findings of ACL 2025.
16. Yang et al. [Voice Memory for Agentic Speech Recognition](https://arxiv.org/abs/2607.26410). 2026；预印本。
17. Siskos et al. [Retrieval Augmented Generation based Context Discovery for ASR](https://aclanthology.org/2025.findings-emnlp.768/). Findings of EMNLP 2025.
18. Someki et al. [PlanRAG-Audio: Planning and Retrieval Augmented Generation for Long-form Audio Understanding](https://aclanthology.org/2026.findings-acl.1304/). Findings of ACL 2026.
19. Tang et al. [Don’t Just Listen, Try Planning: Graph-based Retrieval-Generation Agent for Long-form Audio Meeting Understanding](https://aclanthology.org/2026.findings-acl.1038/). Findings of ACL 2026.
20. Chien et al. [MoshiRAG: Asynchronous Knowledge Retrieval for Full-Duplex Speech Language Models](https://arxiv.org/abs/2604.12928). 2026；预印本。
21. [WavRAG: Audio-Integrated Retrieval Augmented Generation for Spoken Dialogue Models](https://aclanthology.org/2025.acl-long.613/). ACL 2025.
22. [Graph-Based Phonetic Error Correction of Noisy ASR (G-SPIN)](https://aclanthology.org/2026.acl-industry.151/). ACL Industry 2026.

## 9. 最终处置

- 当前 verdict：`MAJOR_REVISION_REQUIRED_BEFORE_FORMAL_OPENING`。
- 方向处置：保留 R2，继续报告级重构；**不是 NO-GO**。
- 正式开题许可：**本轮不签发**。
- Stage-2A：继续 `WITHHELD`；本 review 不授权模型/API/数据/指标/复现/原型执行。
- 下一动作：按 §7 八项签字门完成 v19，再做一次只面向“问题树 + 直接语音/音频现状 + 统计/控制合同”的隔离复审。若该轮无 MAJOR，再出具允许正式开题的 note。

