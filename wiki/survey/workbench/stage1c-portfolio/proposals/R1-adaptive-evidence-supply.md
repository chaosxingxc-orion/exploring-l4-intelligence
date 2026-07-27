---
proposal_id: "R1"
title: "冻结 Speech/Omni 模型的多源上下文能力上界与自适应构造"
dimension: "D1 multimodal knowledge"
status: "problem shape owner-approved; references/methods/baselines under owner-directed step-2 correction (2026-07-27 rulings A/B: Qwen3-Omni-30B core, general-ASR mainline); experiment execution withheld"
evidence_cut: "2026-07-27"
execution_authority: "WITHHELD"
---

# R1 — 冻结 Speech/Omni 模型的多源上下文能力上界与自适应构造

## 开题摘要

本研究不再把 R1 定义成一个预设的 observation-branch 控制器，也不再询问已经被 2024-2026 年工作占据的
宽泛问题——“音频模型是否具有 few-shot in-context learning（ICL）能力”。研究对象是冻结、API-only
Speech/Omni 模型的**多源上下文条件化能力**：示例上下文与当前查询的不同可观测表征，能在多大程度上
改变任务能力；这些来源之间是互补、替代还是干扰；当能力空间和样本异质性确实存在时，训练自由的黑盒
智能体能否针对单个样本构造上下文，逼近给定可执行菜单内的经验上界。

研究按因果依赖分成两个阶段。阶段 A 先固定有限、可复现的上下文菜单，测量能力空间、来源主效应、交互
效应和样本级异质性。阶段 B 只在阶段 A 证明存在可恢复的选择机会后，研究不访问 test gold、不修改核心
模型参数的自适应构造。时延、调用次数、token 和货币成本完整记录，但不进入 R1 的研究目标或击杀条件；
成本压缩属于后续工作。

## 1. 学术问题、对象与边界

### 1.1 正式问题

> 在模型参数完全冻结、只能调用推理接口的条件下，示例上下文与当前查询的不同表征方式，能在多大程度上
> 改变 Speech/Omni 模型的任务能力？这些上下文来源之间存在怎样的互补、替代或干扰关系？在确认给定
> 可执行菜单内的能力空间后，黑盒智能体能否针对单个样本自适应构造上下文，并逼近该经验上界？

R1 的“多源上下文”只包含两类对象：

1. **demonstration context**：与测试样本身份隔离的带标签 speech/audio 示例；
2. **query context**：同一当前查询的 raw audio、分段/窗口、ASR 文本视图、raw+ASR 组合以及确定性的
   问题导向重表达。

第一版固定任务指令和答案格式，避免把任意 prompt wording 搜索混入上下文来源效应；排列与模态拓扑
`σ` 是研究变量，模板语义 `φ` 是受控变量。

### 1.2 与 R2-R6 的边界

- 公开网络、知识库或外部事实检索属于 R2；R1 的示例池不提供测试题缺失的实时世界事实。
- 跨部署实例持续写入、衰减和迁移的经验库属于 R3；R1 使用预先冻结、与测试集隔离的示例池。
- 音频工具如何实现、组合和获得信用属于 R4；R1 只把已定义的确定性重表达视为可选 query view。
- 谁拥有最终作答权和 evidence-state 生命周期属于 R5。
- reward 如何驱动多步策略、轨迹和下一动作属于 R6；R1 只定义上下文动作空间、离线上界和训练自由
  selector 的可行性，不主张 reward-learning 创新。

## 2. 2026 年相邻工作占位与新颖性边界

| 工作 | 已占据的命题 | 对 R1 的有效证据 | 尚未回答的 R1 问题 |
|---|---|---|---|
| Audio Flamingo (2402.01831) | 经过专门训练的 audio LM 可进行 few-shot ICL 与 retrieval | 多类音频分类任务和 unseen-label 实验说明 audio demonstration 可以改变输出 | 不代表任意冻结 API core；未联合分解示例与 query representation |
| MiMo-Audio (2512.23808) | 大规模预训练可涌现 speech/audio few-shot 能力 | SpeechMMLU、MMAU 等建立强 few-shot carrier | 原论文主要证明模型能力，不研究多源上下文菜单和逐样本选择 |
| MetaSICL (2601.18904) | vanilla SICL 已跨儿童 ASR、AU/AR、多语 ASR 和 ST 验证 | frozen vanilla arm 在 MyST/RSR/MMAU/MMAR 上提供直接基线 | 主方法更新 LoRA，超出本项目；fixed retrieval、单次运行、未做多源交互与上界恢复 |
| TICL (2509.13395) | 语义检索的 speech demonstration selection | 口音、多语和儿童 ASR，最高报告 84.7% relative WER reduction | 只优化示例选择，query view 固定；未与非 ASR 音频推理联合研究 |
| TICL+ (2512.18263) | 语义检索后按声学相似度重排 | 四个儿童 ASR corpus，最高报告相对 zero-shot 53.3%、相对 TICL 37.6% WER reduction | 仍是 ASR demo retrieval；未测 query re-representation 及其交互 |
| ByCS (2404.14716) | speech/text/vision 的 Bayesian example selection | RASC863/CORAAL 上证明示例—查询交互可用于选择 | Whisper 架构、逐候选 inverse inference 成本高；没有统一上下文构造 |
| TwS (2509.21749) | 当前音频可在 test time 进行问题导向 DSP/重表达 | MELD/MELD-Hard1k 提供 query-view 机制载体 | 单条破坏性链、合成扰动与算子匹配；没有 demonstration 因子 |
| Chain of Modality (2604.14520) | 模态顺序/拓扑会改变 omni 结果 | 多个 cell 中 router 输给 best fixed，证明拓扑异质性不能假定可路由 | 音视任务为主，未联合 demo selection 与当前音频多视图 |

因此以下表述均被禁止作为 R1 创新：

- “首次研究 speech/audio few-shot ICL”；
- “首次为 speech ICL 选择示例”；
- “首次在 test time 变换音频”或“首次研究 audio test-time compute”。

R1 的候选创新假设被收紧为：

> 将 demonstration context 与当前查询的多种可观测表征统一为一个多源上下文构造问题，在 ASR 与通用
> 音频理解/推理两条主线上测量菜单内经验上界、交互效应和样本级异质性，并检验训练自由的黑盒智能体
> 能否恢复其中的选择机会。

这只是 occupancy 后仍待实验验证的组合假设，不使用 “first-ever” 或绝对 novelty verdict。

## 3. 形式化定义

给定冻结黑盒模型 `M`、音频查询 `x`、任务指令 `q`、与测试样本隔离的示例池 `D`，以及查询的可用
表征集合 `G(x)`。一个上下文配置为：

\[
c=(S_D,S_G,\sigma,\phi)\in\mathcal C_{\mathrm{exec}}(x),
\]

其中 `S_D ⊆ D` 是示例子集，`S_G ⊆ G(x)` 是查询表征子集，`σ` 是顺序/拓扑，`φ` 是冻结模板。输出为：

\[
\hat y_c=M(q,x;c).
\]

为统一高低方向，定义 item-level utility：ASR 使用
`u_i(c)=1-min(WER_i(c),1)`，closed-option AU/AR 使用 `u_i(c)=1[ŷ_i=y_i*]`；原始 WER/CER/accuracy
仍分别报告，归一化 utility 不取代任务指标。

### 3.1 菜单内经验上界与能力空间

直接推理配置记为 `c₀`。对**预注册并实际执行**的有限菜单：

\[
U_i^*=\max_{c\in\mathcal C_{\mathrm{exec}}(x_i)}u_i(c),
\qquad
H_{\mathrm{ctx}}=\mathbb E_{i\in test}[U_i^*-u_i(c_0)].
\]

`U_i*` 只使用 test gold 做离线描述，不能进入任何运行时状态。全文统一称其为“给定可执行菜单内的
经验上界”，不得写成模型的绝对能力上界或 all-contexts ceiling。

### 3.2 固定策略与自适应选择机会

最佳固定配置必须只在 calibration/dev 上选择：

\[
c_{\mathrm{fixed}}=\arg\max_{c\in\mathcal C_{\mathrm{exec}}}
\mathbb E_{i\in cal}[u_i(c)].
\]

它在 test 上不再重选。样本级自适应存在的最大描述性机会为：

\[
O_{\mathrm{sel}}=
\mathbb E_{i\in test}[U_i^*]-
\mathbb E_{i\in test}[u_i(c_{\mathrm{fixed}})].
\]

若 `O_sel` 接近零，最佳配置几乎不随样本变化，自适应构造没有学术必要性。

### 3.3 来源交互与上界恢复

在匹配的四格设计中，`D` 表示加入示例，`G` 表示加入替代 query view：

\[
I_{D\times G}=\mathbb E[u(D+G)-u(D)-u(G)+u(c_0)].
\]

`I>0` 支持互补，`I<0` 支持干扰，接近零支持可加或无交互；因子主效应与置信区间必须同时报告。

为避免逐样本零分母，智能体 `π` 的恢复率定义为 aggregate ratio，而不是先计算 item ratio：

\[
R_\pi=
\frac{\mathbb E[u_i(\pi(x_i))]-\mathbb E[u_i(c_0)]}
{\mathbb E[U_i^*]-\mathbb E[u_i(c_0)]},
\]

且只在分母大于预注册数值容差 `δ` 时报告。若分母不成立，只报告原始 paired delta。

## 4. 研究问题与可证伪假设

### RQ1 — 多源上下文能力空间是否存在？

在 ASR 与 AU/AR 两条主线上，`H_ctx` 是否稳定大于零？菜单经验上界是否同时超过 direct 和在开发集
确定的 best fixed？这回答“是否存在已执行菜单可触达的条件化能力”，不回答模型还有多少未知能力。

### RQ2 — demonstration 与 query representation 如何共同作用？

两类来源是互补、替代还是干扰？示例数量、检索相似度、模态组合与排列顺序分别解释多少方差？若收益
只来自采样次数或模板变化，R1 的多源机制主张失败。

### RQ3 — 最佳配置为何因样本而异？

最佳配置是否随任务类别、音频长度、噪声/混响、口音/年龄、基线正确性和跨调用稳定性系统变化？这些
异质性是否可由部署时可见变量预测？分析必须区分“存在异质性”和“异质性可路由”。

### RQ4 — 无答案智能体能否恢复选择机会？

仅使用输入、检索分数、确定性特征和黑盒模型反馈的训练自由 selector，能否超过 random、单来源
selector 和 best fixed，并恢复一部分 `O_sel`？test gold、gold-derived metadata、hidden state、logprob 和
任何核心模型参数更新均禁止。

### RQ5 — 结论适用于哪些任务与模型？

效应是否在 ASR 与 AU/AR 都成立，并能否在第二个独立模型家族上复现关键对照？若只在一个模型或一条
主线成立，结论必须收缩到该实例，不宣称通用 Speech/Omni 机制。

## 5. 数据集、示例池与模型载体

### 5.1 紧凑双主线设计

| 主线 | 数据集 | R1 承载内容 | 示例池规则 | 当前 readiness |
|---|---|---|---|---|
| ASR | MyST | 儿童会话语音；demo selection、query view、WER 与异质性 | 仅 official train/dev；test 身份隔离 | metadata verified；资产/许可/hash 待 Stage-2 合同 |
| ASR | RSR | 儿童朗读语音；与 MyST 构成 distribution contrast | 仅 official train/dev；test 身份隔离 | official training split 被 MetaSICL 使用；本地资产待冻结 |
| AU/AR | MMAU Test-mini | sound/music/speech 混合；通用音频条件化 | 独立 demo pool 未审计前，只运行 query-view arm | metadata_only；test-mini 1k；禁止 test leave-one-out |
| AU/AR | MMAR | 多层音频推理；检验机制是否超越 ASR | 独立 demo pool 未审计前，只运行 query-view arm | metadata_only；公开 1k benchmark；禁止 test leave-one-out |
| 受控机制 | MELD + MELD-Hard1k | clean/扰动配对；query view × demo 的机制压力测试 | MELD train/dev 作 demo，clean/hard paired test 只评测 | MELD 待获取；Hard1k 按 TwS recipe 重建且不声称 byte-identical |

任何示例必须来自 official train/dev，或来自经过来源核验、音频/文本近重复去重和污染审计的独立池。
若 MMAU/MMAR 没有合法、任务匹配的独立示例池，其 demonstration arm 明确记为 `UNAVAILABLE_SPLIT_FENCE`，
不得用测试答案 leave-one-out 伪造 few-shot 结论；两者仍承担 raw/transcript/both/重表达的 query-view 实验。

### 5.2 模型载体

| 角色 | 模型 | 执行范围 | 解释限制 |
|---|---|---|---|
| 主模型 | `Qwen/Qwen2.5-Omni-7B` | 完整菜单、机制分解、异质性和 selector | 官方接口支持 interleaved audio，但 exact revision/service/decoding 待独立 Stage-2 合同 |
| 独立复核 | `XiaomiMiMo/MiMo-Audio-7B-Instruct` | direct、best fixed、菜单 oracle、最终 selector 四个关键条件 | MiMo 原论文的系统 few-shot 主证据主要来自 Base；Base/Instruct 数字不得混写，复核必须本地重跑 |

两者都通过服务化推理接口使用；不做 LoRA、微调、梯度更新或内部解码器改写。MetaSICL 的 LoRA 主方法
只作为 occupancy 边界，唯一可复用实验臂是原始 checkpoint 的 vanilla SICL。

## 6. 决定性实验

### 6.1 协议与泄漏审计

在任何 capability 表之前冻结 dataset revision/split/hash、query ID、demo ID/source split、去重规则、模型
revision、prompt template、decoding 和输出解析。calibration/dev 负责选 best fixed 与 selector 阈值；test
只运行一次预注册方案。所有运行记录至少包含：`model_id, dataset_id, sample_id, demo_ids,
demo_source_splits, query_views, topology, template_id, decoding_id, output, utility, provenance`。

### 6.2 阶段 A：能力上界与机制

第一版可执行菜单使用：

- shots `k ∈ {0,1,4,8}`；
- demonstration policy：random、TICL semantic KNN、ASR 上的 TICL+ acoustic rerank、受限候选池上的
  ByCS；label-aware best-demo 只作离线 oracle；
- query view：raw audio、ASR transcript、raw+transcript、一个预注册的 deterministic query-focused
  segment/transform；
- topology：demo-before-query 为主，另做一次预注册的 modality/order permutation；
- `φ` 使用同一任务模板，禁止针对测试样本人工改 prompt。

先在 calibration 的代表性有界子集枚举菜单，冻结保留配置，再在 test 执行。核心对照为 direct、
same-observation resampling、random demo、semantic/acoustic demo、query-view only、demo+query-view、best fixed
和 offline menu oracle。通过 `demo present/absent × alternate query view present/absent` 四格设计估计
`I_{D×G}`，再做 shots、retrieval 和 order 消融。

### 6.3 阶段 B：训练自由的自适应构造

只有 `H_ctx` 与 `O_sel` 均超过预注册数值容差、且最佳配置存在可解释样本异质性时才进入阶段 B。
selector 只能读取部署可见量：任务类型、音频长度与确定性声学 proxy、retrieval 分数、direct 输出格式、
跨采样/跨视图一致性以及 frozen cross-family judge 的可见输出。允许规则、检索、黑盒自评和有限 test-time
search；不训练 controller，不访问 test gold。

比较 random context、best fixed、demo-only selector、query-view-only selector、联合 selector 和 offline
menu oracle。R1 不要求 cost-matched dominance：资源消耗完整记录，用于解释而非否决能力结果；若要声称
收益来自“选择”而非“更多执行”，另加相同已执行菜单的 matched-compute 归因对照，但不把成本加入目标。

### 6.4 统计与稳定性

- 对 item-level utility 做 paired bootstrap 95% CI 和 effect size；binary outcome 补 McNemar。
- ASR 与 AU/AR 原始指标分别报告，不用跨任务平均分隐藏方向相反的效应。
- 确定性解码可用时固定为确定性；否则重复调用并报告 within-configuration variance。
- 分桶报告任务、音频长度、clean/noise/reverb、口音/年龄、direct correct/wrong 与模型家族。
- 成本记录 calls、audio-seconds、context length、latency 和货币成本，但不设 R1 成本通过阈值。

## 7. 可证伪结论与停止规则

R1 的学术完成不要求正结果，预先接受以下闭合路径：

1. `H_ctx≈0`：给定菜单没有可利用的上下文能力空间；停止阶段 B，但不得外推为 all-contexts 不可能。
2. `H_ctx>0` 且 `O_sel≈0`：存在更好的固定上下文，但没有样本级自适应必要性；交付 best fixed 机制结论。
3. `O_sel>0` 但 deployment-visible 特征不可预测：报告“存在选择机会、无答案 selector 无法恢复”。
4. selector 不超过 best fixed：自适应主张失败；不能用 offline oracle 或 retrospective best config 代替。
5. 只在 synthetic Hard1k 有效：结论收缩为合成扰动/operator 匹配，不宣称通用能力激活。
6. 只在单模型/单主线成立：按模型或任务限定，不宣称 Speech/Omni 普适规律。
7. demo pool 无法通过 split/contamination audit：对应 few-shot arm 取消，不用测试集标签补洞。

## 8. Lean 与数学审计

现有 `TfrlProofs.InfoBoundary` 只证明固定候选 read-out selector 不能超出已抽样池；R1 改变 context 并重新
生成，因此不属于该定理的量化域。这个事实只阻止错误的 impossibility 外推，不证明任何上下文有效。

R1 的上界、主效应、交互和恢复率是经验统计量，不由 Lean 证明。Lean 可以审计的内容限于：有限菜单的
索引类型、gold 与 runtime state 的类型隔离、best-fixed 与 per-item oracle 的定义域、aggregate recovery
ratio 的非零分母前提，以及后续 R5/R6 接入时的 incumbent/termination 条件。任何真实 `H_ctx>0`、
异质性可预测或 selector 有效的结论都必须来自实验。

## 9. 预期贡献与允许措辞

若证据成立，R1 允许按强度递进地贡献：

1. 一个无测试泄漏、覆盖 ASR 与 AU/AR 的多源上下文干预协议；
2. demonstration 与 query representation 的主效应、交互和样本异质性图谱；
3. 给定菜单内经验上界与 best-fixed 之间的选择机会测量；
4. 一个训练自由黑盒 selector 对该选择机会的可复现实证恢复。

不允许把 benchmark accuracy 的单点提升写成“模型学会新知识”，不允许把 menu oracle 写成绝对天花板，
也不允许把 Audio Flamingo、MetaSICL、TICL/TICL+ 的已有效果重新包装成 R1 创新。

## 10. Provenance

新增相邻工作全文已于 2026-07-27 通过
`wiki/survey/2026-07-17-sf-fulltext-ledger.jsonl` 绑定 PDF/e-print SHA-256，并登记在
`wiki/survey/registry/stage1c-r1-context-icl-2026-07-27-papers.jsonl`。逐篇占位、实验数字和边界摘要见
`../2026-07-27-r1-context-icl-evidence-supplement.md`。TwS/CoM 与现有数据资产事实继续来自 D1 dossier 和
T1/T2/T3；本 proposal 的“统一多源上下文 + 能力上界 + 自适应构造”是 `OUR_HYPOTHESIS`。
