---
title: "R2 v19 多轮隔离对抗式博导审查"
artifact_id: "SF-STAGE1C-R2-REVIEW-R21"
date: "2026-08-02"
campaign: "system-first-stage1c-v2"
round: 21
reviewed_artifact: "wiki/survey/workbench/stage1c-portfolio/proposals/2026-07-29-r2-coreview-draft.md"
reviewed_artifact_id: "SF-STAGE1C-R2-COREVIEW-V19"
reviewed_commit: "ab221c4018415fe99ca474dc6675d512c4e7cb27"
reviewed_git_blob: "c4a9e8f41565f2399015570882d20dbdf3141ab2"
reviewed_sha256: "f250401740fd106daae0293b4573064463765b285b7aeaab20ae8b9126a6d965"
reviewed_bytes: 225218
review_scope: "开题阶段：研究问题、概念体系、学界研究现状、技术可验证性、评价逻辑与报告可签署性"
novelty_scope: "OUT_OF_SCOPE"
review_method: "three isolated adversarial reviews plus fresh primary-source search and main-review rebuttal"
literature_cut: "2026-08-02"
verdict: "MAJOR_REVISION_REQUIRED_BEFORE_FORMAL_OPENING"
formal_opening_permission: "NOT_ISSUED"
stage2a_authorization: "WITHHELD"
---

# R2 v19 多轮隔离对抗式博导审查

## 1. 审查结论

**结论：`MAJOR_REVISION_REQUIRED_BEFORE_FORMAL_OPENING`。V19 当前不建议签署正式开题许可，本轮不出具允许开题的 notes。**

这不是对研究方向或待验证技术价值的否定。相反，V19 已经证明下列问题值得研究：冻结黑盒语音/omni 核在何时应重新观察音频、何时应取得外部证据、如何组织和供给这些证据、如何拒绝有害证据，以及能否以外置序贯控制在效果、可靠性和成本之间作出可复放的选择。

本轮不签字的原因是：**研究问题的文字承诺仍大于现有操纵能够识别的对象；ORG/SUPPLY/USE/OBS/CONTROL 的词典虽已建立，部分实验对象仍跨层漂移；三态统计总则与多个具体判据直接矛盾；档 B 与 pilot/confirmatory 合同仍未闭合；直接语音/音频学界现状仍有会改变问题地图的遗漏和发表态错分。**这些都是开题报告文本与实验合同层面可修复的问题，不要求现在运行模型、下载数据、调用 API、复现论文或证明新颖性。

本审查严格遵守 Stage-1C 边界：**不评价任务或方法新颖性，不判断首创性、优先权或论文占位，不要求 prior-difference 结论。**正式开题许可与 Stage-2A 执行许可是两件事；即使下一版通过开题审查，也不自动授权模型、数据、API 或实验执行。

## 2. 对抗式审查方法与隔离性

本轮把同一 Git blob 固定后，进行了四轮相互独立的检查：

1. **问题与概念隔离轮**：只读 AGENTS、当前 Research Objective、Project Thesis 与目标 V19；禁止读取 audit、历史 proposal/review/response、sidecar 和 Decision Log；检查总问题、RQ、五层概念、因果映射及“为何引知”。
2. **学界现状隔离轮**：采用同样的上下文隔离，重新检索 2021–2026 年 ACL Anthology、ISCA Archive、AAAI、IEEE/ICASSP 与 arXiv 一手来源；检查五条研究线、发表态、证据权重和直接邻域覆盖。
3. **方法与评价隔离轮**：采用同样的上下文隔离，检查有限时域控制、TF-Strict/API-only 边界、K0/K-SUP/K1/K-NB 等判据、pilot/confirmatory 分工、成本与最小执行路径。
4. **主审反证轮**：在前三轮结论回传后，主审重新逐行核对 V19，并主动尝试用总则覆盖、范围限定、失败出口和新增参考文献表推翻各项 MAJOR；同时对承重遗漏和发表态用官方页面复核。

三个隔离审查在互不读取历史审稿的条件下均独立给出 `MAJOR_REVISION / NOT READY FOR FORMAL OPENING`。它们共同确认“技术值得做”和“为何引知基本讲清”，也共同发现三态判定、RQ0 可识别性和方法合同未闭合。主审反证轮没有推翻这些核心结论。

## 3. V19 已经做对的事情

V19 相比上一版有实质进步，不应在下一轮整改中丢失：

- **黑盒不等于缺知识。** §1.0 把动态性、私域性、情境性、可审计性和参数知识读取不稳定作为外部知识的理由，并把纯声学恢复留给 OBS；这是正确的问题起点（L138–147）。
- **五层词典已经形成。** ORG/SUPPLY/USE/OBS/CONTROL 的定义、数据流和主要所有权在定义层基本互斥（L261–292）；CONTROL 负责是否触发/停止，SUPPLY 负责候选与条件参数，这一方向正确。
- **RQ 卡片和模块映射明显改善。** RQ0–RQ4b 已给出操纵、对照、载体、estimand 与失败后范围；模块表也明确禁止跨层系统结果反推单层机制（L168–209）。
- **学界现状已有可用骨架。** L4 被拆成同录音结构化访问、外部音频库、外部世界知识三类；L5 不再把 modality gap 直接当成外部知识有效性的证据（L326–483）。
- **控制模型不再误称 contextual bandit。** 档 B 改成 dev 学、test 冻结的有限时域序贯策略，并给出了状态、动作、转移和延迟回报骨架（L667–687、L965–1010）。
- **评价从单一准确率扩展为五阶段证据链。** Need、Access、Use、Outcome、Efficiency 被分开；K-NB 也增加总 WER、worst-group、correct-to-wrong 和 coverage/abstention 护栏（L149–158、L1024–1046、L1167–1176）。
- **pilot 与 confirmatory 的角色已经被意识到，治理史也已移出正文。** 这两项是正式报告化的重要进展（L1048–1062）。
- **标准参考文献表已经出现。** §10 按发表态列出 136 项，解决了“完全没有独立可读文献表”的旧问题。

因此，本轮不是推倒重来，而是要求把已经建立的定义真正贯彻到每个 RQ、实验臂、判据和结论出口。

## 4. 必须关闭的重大问题

### MAJOR-1：RQ0 和总问题的承诺超过现有实验能够识别的范围

RQ0 承诺区分“观察不足、参数知识不足、可由外证纠正、何时不应引知”（L28–30、L138–147），但正式判定只使用 `A1′ gold-evidence masked − A0` 的外证 headroom（L174、L922–925、L1024–1027）。这个差分可以回答“在指定载体上，给定真外证是否存在可恢复余量”，却不能单独区分：

- 核从未拥有该知识；
- 核拥有但从语音通道读不出来；
- prompt/上下文只是激活了潜在参数知识；
- 音频观察不足与外部知识不足发生交互。

V19 自己已经承认 NB 主载体的正读数不能分离外部新信息与潜在知识激发（L1077–1080），因此 RQ0 的卡片必须服从这一可识别边界。

总问题决策表也没有完整消费六个 RQ：它主要组合 K0、任选一个层判据、K1b 与 K-NB（L181–193），没有显式消费 K1a/K2/K-RL/K-OPT，也没有把 RQ4b 的可靠性与效率 estimand 写入总答案。一个单一“机制成立”标签会掩盖相互独立的正负结果。

**关闭标准：**二选一。

1. 建议收窄 RQ0 为：“在预注册载体与任务型上，是否存在可由真外部证据恢复的任务余量，以及哪些负类不应触发外证？”不得据此声称识别了“参数知识不足”。
2. 若保留原承诺，则加入 `OBS × external evidence` 析因设计与预注册错误分型，使观察不足、外证不足及交互分别有 estimand。

总问题的答案应改成 RQ0–RQ4b 的**结论向量**，或明确一个主问题并将其余降为从问题；不能让 K1b 或 K-NB 代替整个研究问题树。

### MAJOR-2：概念词典已清楚，但实验归属仍有跨层漂移与自相矛盾

用户关心的“知识组织形式、供给形式、使用形式”在定义层已经明显改善；当前问题发生在操纵与归因层：

1. **RQ1 范围前后冲突。** RQ 卡片把 RQ1 收窄为 key/索引/切片/面，并把 value/schema/version/provenance 定为后续分支或工程义务（L28–31、L175）；§3.3 却又把外部知识的版本、出处、冲突、abstain schema 称为“R2 的实验对象”，并说 O-config 正在检验它们（L645–648）。
2. **同一任务音频的 T2 库身份不唯一。** 当前录音被索引时写入 ORG，取回时又归 OBS；但总对象把 ORG 描述为外部材料的组织，而“世界写的=知识、模型自己听到的=观测”的规则又排斥当前录音成为外部知识。这样同一个对象既承担知识组织主张，又被声明为非知识。
3. **RQ3 已收窄到证据准入，模块名仍包含融合/冲突。** ABSTAIN 也同时被放在 USE 变量与终结动作中（L206、L261–292）。
4. **SUPPLY 与 CONTROL 的所有权偶有回漂。** 定义说触发/停止决策归 CONTROL，但 §6.2 的简写又把触发/停止列入 SUPPLY 变量。

**关闭标准：**

- 将当前任务音频索引单列为 `OBS-INDEX`，只检验观察组织和访问效率，不承担“外部知识 ORG”结论；或者把总对象明确扩大成“外部知识与内部观测状态的联合控制系统”，并分别报告两类结论。
- 统一 RQ1：若 schema/version/provenance 不在主实验中，就从“实验对象”措辞中删除；若要检验，就增加明确操纵、对照和判据。
- 把 RQ3 模块统一命名为“证据准入”，融合、冲突、引用和拒答留作后续支线。
- 固定 ABSTAIN 的动作层；USE 只评价该动作的正确性。全篇统一“SUPPLY 定义候选与条件参数，CONTROL 决定是否执行”。

### MAJOR-3：三态统计总则正确，但具体判据仍把“未证正效应”当成“证明无效”

§7 总则要求：`SUPPORTED` 必须由下置信界越过 SESOI；`REFUTED_OR_NEGLIGIBLE` 必须由上置信界、等效/ROPE 或反向非劣检验支持；其余均为 `INCONCLUSIVE`（L1068–1075）。这个总则是正确的。

但具体条款仍直接写出相反语义：

| 判据 | V19 触发语句 | 问题 |
|---|---|---|
| K0 | `LCB < SESOI → 无 headroom`（L1077–1082） | 未达到正向阈值不等于可忽略；应看 UCB 或等效检验 |
| K1a | `LCB ≤ 0 → 判死`（L1115–1120） | 把低功效/不确定误判为反证 |
| K1b | 任一合取条件未满足即判死（L1121–1132） | 合取中“未支持”只能使总命题不确定；被正式反证才可推翻 |
| K-NB | 多个组×指标均 `LCB ≤ 0` 才判死（L1143–1148） | 若主张是“胜过全部强对手”，任一承重对手被正式反证即可推翻全称命题 |
| K-PS/K4/K5 | 继续以 LCB 未越零或未显著作为负出口（L1177–1217） | 与三态总则冲突 |
| K-RL/K-OPT | `LCB ≤ 0/无增益 → 不立`（L1240–1248） | 未区分 negligible 与 inconclusive |
| K-XOVER | “不存在显著优势区 → 判空”（L1249–1252） | 未显著不等于全目标区间等效 |

L1073–1075 试图用“所有旧触发句都按总则解释”作全局覆盖，但正式开题报告不能同时保留互相相反的不等式，再要求读者自行改写其含义。这会造成分析脚本、预注册、学生执行和答辩委员四套不同判读。

**关闭标准：**每一个主判据都必须显式写成三行真值表：

- `SUPPORTED`: 预注册正向效应的 LCB 越过 SESOI；
- `REFUTED_OR_NEGLIGIBLE`: UCB 不超过可忽略界，或预注册等效/ROPE/反向非劣检验成立；
- `INCONCLUSIVE`: 其余全部情况。

合取命题应写明“全部分量支持才成立；任一承重分量被正式反证则推翻；仅有分量未获支持则不确定”。K-NB 必须二选一：保留“胜过所有入判组”的全称主张并采用相应反证逻辑，或把主张收窄为预指定对手子集。

### MAJOR-4：RQ4a 的因果对象、档 B 序贯合同和 TF-Strict 边界尚未闭合

RQ4a 一张卡同时承载双源按样本选择、通用调度、over/under-search、档 B 序贯策略和档 A 优化器身份（L178、L928–930）。其中 A4b−A4a 不只增加“感知信号”，还增加 `RE_RESOLVE/RE_SLICE` 的动作可用性和实际调用量；现有 count-matched 只作 READOUT，不能唯一识别“按样本双源选择”。K1b 的 β 非零与胜过 serial-composition 仍可能来自多了动作、信息或预算。

档 B 的有限时域骨架比 V18 正确，但还不是可复现合同：状态定义没有显式包含工具调用后形成的候选证据区，`ADMIT/REJECT(e)` 因而缺少完整来源；策略类、行为/探索策略、coverage 条件和 credit assignment 仍被推迟到 authorization 前义务（L965–1010、L1540–1542）。档 A 与档 B 是否共享动作空间、horizon、信息和调参预算也未完全冻结。

此外，红线写“不为本任务新训练任何模型”（L120–123），档 B 又允许在 dev 上学习并更新控制器（L669–682、L1005–1010）。仅说“模型外计算”还不足以说明控制器是否属于 task-trained model。

**关闭标准：**

- 将 RQ4a 至少拆为：`RQ4a-1 双源按样本动作选择` 与 `RQ4a-2 序贯策略/优化器身份`。
- 对 RQ4a-1 建立明确析因：SUPPLY-only、OBS-only 或固定 OBS、无条件串行、双源自适应；固定信息预算和调用预算，用 interaction 或差分中的差分识别选择价值。
- 为档 B 补齐 `C_t` 候选区、初始态、动作合法域、观测随机性、终止态、horizon、episode return、策略类、离线 credit assignment、行为策略、随机种子和覆盖条件。
- 权威定义控制器：若保留 TF-Strict，应明确它是外置、非神经、无梯度、仅 dev 标定、test 完全冻结的哪一种策略；若当前 Stage 边界仍把它视为 task-trained model，则删除档 B 的 RL 身份主张，保留 reward-guided 配置/策略选择。

### MAJOR-5：pilot/confirmatory 角色、强基线冻结和最小执行路径仍不一致

§6.6 正确声明 150–200 题先导集只用于构念、流程、方差和触发门 gold，不能代替全部确认性证据（L1059–1062）；K0 随后却把“先导数据集”指定为正式判定载体，K4 也把结论限制在先导载体（L1077–1080、L1200–1210）。如果阈值、标注规则、prompt 或载体选择由同一先导数据调定，再用它作正式裁决，确认性语义不成立。

K-NB 的强对手集合包含多项待重实现工作。V19 对信息边界的分组是进步，但还缺少一个规则：若 mandatory baseline 重实现失败，结论应是“主张不可判”，而不是事后把该对手移出入判集。

“最小核心实验”仍同时跨 K0/K5/K-SUP/K4/K-NB、多载体和自建数据；§9 还有大量承重义务，资源只写“小/中/大”，没有最小确认路径的人月、GPU/API、标注和存储上界（L1048–1057、L1513–1572）。这不足以支持导师判断课题是否能在博士阶段按依赖顺序完成。

**关闭标准：**

- 将 pilot 只用于构念、方差、阈值和流程；K0/K4 正式结论来自独立冻结确认集。或者把“先导数据集”改名为 carrier family，并在其中预先划分互不重叠的 discovery/confirmatory split，按源音频、说话人、company 和 entity 去泄漏。
- 冻结不可事后缩减的 mandatory baseline set、版本、信息边界、调参预算与 readiness gate；任一 mandatory 对手不可运行时，K-NB 记 `INCONCLUSIVE_BASELINE_NOT_READY`。
- 增加一条真正的 minimum confirmatory path：一个主载体、必需基线、一个主指标族、确认样本量/power 输入、调用/GPU/存储/标注人月/经费上界、stop/go 顺序。复杂面联邦、个性化、档 B、多载体复制和全部基线迁移作为条件扩展，不得互为前置。

### MAJOR-6：学界现状的骨架已改善，但直接研究线仍有承重遗漏和证据权重错误

V19 的五线地图已经能用于讨论，但“136 条参考文献”不能代替直接问题域的完整覆盖。fresh search 与官方一手页面复核发现：

1. **Speech entity retrieval/linking 谱系没有独立成线。** 2021 年 ASR N-best entity retrieval、2023 年大目录 Retrieve-and-Copy 和 2024 年 TED-EL 共同说明“ASR 不确定性→实体检索/链接→拒绝/消歧”不是 acoustic memory 或普通 world-knowledge RAG 的附属项。它直接影响 RQ1 的 key/index 和 RQ2 的供给对象。
2. **ASR correction 缺少 acoustic-key→candidate→admission 的强近邻。** Whispering LLaMA、2025 Generative Annotation、DeRAGEC 和 RECOVER 应被放在同一轴上，明确训练态、音频是否仍可访问、候选拒绝能力和知识来源。
3. **长音频控制不能写成“音频域 2026 起步”。** Interspeech 2024 已有 deep-Q 的长音频跳读策略；Interspeech 2025 已有 training-free 的音频/文本双维 chunking 与 LLM refinement；2026 的 PlanRAG-Audio/GRGA 是进一步结构化和规划，而不是起点（L239–243 的时间线需要修正）。
4. **L5 缺少任务级 factuality 与更早的正式 cross-modal evidence。** NAACL 2025 的 speech/text 表示分析和 AAAI 2026 CCFQA 应与 Xiang、MCR-Bench、ACL 2026 TARS 并列，避免只由隐藏层分析推断“参数知识能否从语音可靠读出”。
5. **发表态与正式链接错分会改变证据权重。** WavRAG 已是 ACL 2025 正式论文，却仍列为 arXiv preprint；Speech-Hands 已有 ACL 2026 正式条目；Audiopedia 已有 ICASSP 2025 正式 DOI；LongAudio-RAG 的当前正式题名也已变化。DeRAGEC 虽在表中写 published，正文仍把它放在摘要级/待升 D2 的位置。

**关闭标准：**

- 将 L2 拆成 `acoustic/speech-key memory` 与 `speech entity retrieval/linking/disambiguation` 两支。
- 补入下表的直接正式工作，并用统一变量列描述：问题、知识/证据源、音频访问、训练态、接口、组织/供给/使用位置、载体/指标、失败模式。
- 正式同行评议、已录用、纯预印本、benchmark/dataset、跨域 donor 分层加权；承重结论优先由全文核验的正式一手论文支持。
- 所有正式工作改用 Anthology/ISCA/AAAI/IEEE DOI 主链接；作者、题名、venue/year 和发表态逐条核对。

## 5. fresh-search 后建议补入的直接一手研究

| 研究线 | 一手工作 | 对开题问题地图的意义 |
|---|---|---|
| Speech entity retrieval | [Leveraging ASR N-Best in Deep Entity Retrieval, Interspeech 2021](https://www.isca-archive.org/interspeech_2021/wang21b_interspeech.html) | N-best 直接进入实体检索，并评价域外拒绝；连接 OBS、ORG 与 USE |
| 大目录 contextual ASR | [Retrieve and Copy, EMNLP Industry 2023](https://aclanthology.org/2023.emnlp-industry.60/) | 把 20K 目录、近音干扰、检索和延迟共同纳入；是 RQ1/RQ2 的历史节点 |
| Speech entity linking | [TED-EL, LREC-COLING 2024](https://aclanthology.org/2024.lrec-main.1365/) | 正式定义音频、mention 与 entity 对齐的 speech entity linking 载体 |
| 生成式 ASR 纠错 | [Whispering LLaMA, EMNLP 2023](https://aclanthology.org/2023.emnlp-main.618/) | 跨模态生成式 correction 前驱；应与纯文本 GER 和音频可访问 correction 区分 |
| Acoustic-key entity correction | [Generative Annotation for ASR Named Entity Correction, EMNLP 2025](https://aclanthology.org/2025.emnlp-main.1052/) | 用语音特征检索候选并生成式定位/纠错，直接邻接 RQ1/RQ3 |
| Training-free candidate admission | [DeRAGEC, Findings ACL 2025](https://aclanthology.org/2025.findings-acl.786/) | training-free in-context 候选去噪，应提升为正式全文承重证据 |
| 自动上下文发现 | [Retrieval Augmented Generation based context discovery for ASR, Findings EMNLP 2025](https://aclanthology.org/2025.findings-emnlp.768/) | 直接回答自动供给何种 context，并给出 no-context/oracle 差距 |
| Contextual ASR benchmark | [ContextASR-Bench, 2025](https://arxiv.org/abs/2507.05727) | 大规模多域实体与三种 context 使用模式；当前仍为预印本，权重应与正式论文分开 |
| Agentic entity correction | [RECOVER, 2026](https://arxiv.org/abs/2603.16411) | 多假设、实体检索和受限纠错的直接黑盒近邻；目前仍是 under-review preprint |
| 长音频策略控制 | [Efficient SQA from Long Audio Contexts: A Policy-driven Approach, Interspeech 2024](https://www.isca-archive.org/interspeech_2024/johnson24_interspeech.html) | deep-Q 学习何时跳过、跳多远，修正“2026 才起步”的时间线 |
| 长音频分块检索 | [On Retrieval of Long Audios with Complex Text Queries, Interspeech 2025](https://www.isca-archive.org/interspeech_2025/yang25n_interspeech.html) | training-free 双维 chunking、聚合和 LLM refinement，直接关联 ORG 与效率 |
| Transcription-free audio retrieval | [VoxRAG, MAGMaR 2025](https://aclanthology.org/2025.magmar-1.3/) | spoken query 直接检索 audio segment；workshop 证据，宜低权重登记 |
| Native audio/text RAG | [WavRAG, ACL 2025](https://aclanthology.org/2025.acl-long.613/) | 正式 ACL 论文；纠正 V19 的 preprint 状态，并提供 native audio retrieval/效率对照 |
| 长音频规划检索 | [PlanRAG-Audio, Findings ACL 2026](https://aclanthology.org/2026.findings-acl.1304/) | 规划所需模态和时间片、只取 query-relevant 信息；是 2026 的扩展节点而非起点 |
| 长会议图检索 | [GRGA, Findings ACL 2026](https://aclanthology.org/2026.findings-acl.1038/) | 多维图组织、agent planning 与生成；帮助限定同录音结构化访问线 |
| Cross-modal representation | [How do Multimodal Foundation Models Encode Text and Speech?, NAACL 2025](https://aclanthology.org/2025.naacl-short.51/) | 提供正式的 speech/text 层间表示差距证据，但不能替代任务级外证实验 |
| Modality gap | [Understanding the Modality Gap, EMNLP 2025](https://aclanthology.org/2025.emnlp-main.262/) | 说明 speech/text 表示和行为差距；支持 RQ0 的问题动机但不证明引知有效 |
| Cross-modal factuality | [CCFQA, AAAI 2026](https://ojs.aaai.org/index.php/AAAI/article/view/40312) | 直接评测八语种 speech/text factuality，和“参数知识能否经语音可靠读出”同构 |
| Modality reasoning gap | [Closing the Modality Reasoning Gap, ACL 2026](https://aclanthology.org/2026.acl-long.857/) | TARS 的正式 ACL 状态；训练型对齐证据，用于界定冻结黑盒外控边界 |

这张表的目的不是证明 R2 新或不新，而是保证开题报告能准确说明：学界分别在检索什么、如何组织、如何供给、如何使用、是否保留音频访问、是否训练模型、如何评价失败。

## 6. 待验证技术点是否值得做

在不讨论新颖性的前提下，以下技术问题均通过“值得验证”门：

1. **外部知识必要性边界**：在私域、动态或上下文依赖任务中，真外证是否提供超出裸核的可恢复 headroom；负类何时不应引知。
2. **组织形式**：声学 key、G2P/文本 key、切片尺度、信息面和物化边界，哪一种能使错误可寻址并改善下游任务，而不只改善 retrieval proxy。
3. **供给形式**：slides、财报稿、参会者名单等来源在等信息预算下是否具有不同价值；source selection 是否优于无条件合并。
4. **使用形式**：同一候选证据集下，显式准入能否减少 knowledge-error、过纠正和 correct-to-wrong，而保持 coverage。
5. **双源控制**：重新观察音频与获取外证是否应按样本竞争，还是固定串行/单源策略已经足够。
6. **外置序贯策略**：dev 学、test 冻结的控制器能否在同动作、信息和预算下超过固定策略及等预算搜索。
7. **系统效果、可靠性和效率**：知识增强是否在实体准确率/稀有词指标改善的同时满足总 WER、worst-group、正确样本伤害和 abstention 护栏，并给出全链路成本画像。

真正需要整改的是这些问题的**可识别性和裁决语义**，而不是删掉技术方向。

## 7. 建议的正式开题问题树

建议下一版用以下结构取代单一“机制成立”总标签：

| RQ | 只回答什么 | 最小操纵 | 结论边界 |
|---|---|---|---|
| RQ0 Need | 指定载体是否有真外证可恢复余量；哪些负类不应触发 | A0 vs A1′；若保留观察分解则加 OBS×external 析因 | 不推断参数内是否“存过”该知识 |
| RQ1 ORG | key/index/slicing/faces 配置族是否改善任务效用 | incumbent vs frozen optimized configuration；必要时加分因素消融 | 不把系统整体增益归给单个组织因子 |
| RQ2 SUPPLY | 预指定来源在等信息预算下的相对价值 | per-source vs frozen merged-context construction | 不外推为逐样本 selector，除非另有自适应操纵 |
| RQ3 USE | 同一候选集下证据准入是否有效且少伤害 | admission on/off，候选固定 | 不声称已解决融合、冲突、引用或拒答 |
| RQ4a-1 CONTROL | OBS 与外证动作是否需要按样本选择 | SUPPLY-only / OBS-only / serial / adaptive factorial | 固定动作可用性、信息量和预算 |
| RQ4a-2 OPT | 外置序贯策略是否优于档 A/固定策略 | 档 A vs 档 B，动作空间/horizon/预算相同 | 单独回答方法身份，不替代双源因果结论 |
| RQ4b SYSTEM | 整合系统的效果、可靠性与效率画像 | 主张臂 vs 冻结 mandatory baseline set | 分别报告效用、伤害、覆盖和成本，不压成单分数 |

最终总答案是一组可并存的结论，例如“Need 支持、ORG 不确定、SUPPLY 某来源支持、USE 支持、adaptive CONTROL 反证、SYSTEM 有效但成本较高”，而不是强迫所有层共同落入一个标签。

## 8. 重新送审的签字门

下一版满足以下十项后，才建议进入“是否允许正式开题”的签字审查：

- [ ] RQ0 收窄到可识别 headroom，或加入 OBS×外证析因；总答案完整消费 RQ0–RQ4b。
- [ ] 当前任务音频固定为 OBS-INDEX，或总对象明确扩大为“知识+观测状态”；两类结论分开。
- [ ] RQ1 的 schema/version/provenance 实验身份前后一致；RQ3 全篇只称证据准入。
- [ ] K0、K-SUP、K1a、K1b、K-NB、K-PS、K4、K5、K-RL、K-OPT、K-XOVER 全部逐条改成显式三态真值表。
- [ ] K-NB 的全称主张、mandatory baseline set、反证逻辑和 baseline-not-ready 出口一致。
- [ ] RQ4a 拆分，双源选择采用可识别析因；档 B 补齐状态、候选区、策略类、credit assignment、探索/覆盖与同预算合同。
- [ ] TF-Strict 对外置控制器的“可学习对象”给出权威一致定义。
- [ ] pilot/discovery 与 confirmatory 数据、阈值、prompt、标签规则和载体选择完全隔离。
- [ ] 补齐直接正式研究线，修正时间线、正式题名、venue/DOI/链接和证据权重。
- [ ] 冻结一个资源有上界、依赖可执行、失败可停止的 minimum confirmatory path；效率比率定义净/毛修正、零/负分母、correct-to-wrong 抵扣、索引摊销与区间估计。

这些都是**报告级关闭标准**。本轮不要求给出最终数值阈值；可以把阈值留给 Stage-2A 第零步 power/余量输入，但统计方向、数据隔离、主指标、对手集合和失败语义必须在开题报告里先写对。

## 9. 最终处置

- 当前 verdict：`MAJOR_REVISION_REQUIRED_BEFORE_FORMAL_OPENING`。
- 技术价值：**通过；值得在报告合同修复后开展。**
- 学界现状：**骨架通过，直接线覆盖与证据权重未通过。**
- 研究问题与概念：**定义层大幅改善，操纵/归因层未通过。**
- 方法与评价：**有限时域方向通过，三态统计、因果识别、pilot/confirmatory 与 TF-Strict 合同未通过。**
- 正式开题许可：**本轮不签发，因此不存在允许开题 notes。**
- Stage-2A：**继续 withheld；本 review 不授权模型、数据、API、prototype、reproduction 或实验。**
- 下一动作：Fable5 按 §8 十项签字门形成 V20；复审只检查“问题树、五层归属、三态判据、RQ4a/档 B、direct-field map、minimum confirmatory path”。若该轮无 MAJOR，再另行出具正式开题许可 note。

