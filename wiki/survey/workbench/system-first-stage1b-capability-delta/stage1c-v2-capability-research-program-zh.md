---
title: "Stage-1C v2：面向知识、技能、记忆与训练免权重控制的实验族研究方案"
artifact_id: "SF-STAGE1C-V2-CAPABILITY-RESEARCH-PROPOSAL-ZH-RC1"
date: "2026-07-23"
status: "OWNER_REVIEW_PROPOSAL_AFTER_STAGE1B_DELTA_RC"
authority_effect: "NONE"
depends_on: "SIGN_STAGE1B_CAPABILITY_DELTA_RELEASE"
proposed_next_owner_token: "AUTHORIZE_STAGE1C_V2_CAPABILITY_EXPERIMENT_MAPPING"
experiment_execution_requested: false
stage2a_requested: false
novelty_verdict_requested: false
---

# Stage-1C v2：面向知识、技能、记忆与训练免权重控制的实验族研究方案

## 0. 提交结论与待决事项

本方案吸收了 supervisor review、owner 对“以实验统合”的要求，以及本轮 Stage-1B capability delta 的
14 篇新增证据。核心结论不是把论文重新分进五个文件夹，而是把 Stage-1C 的一级分析单位改成：

`因果干预方向 × 原子运行配置 × 配对比较 × dataset lineage/relation × experiment family`

研究本体采用五层而非五个并列“能力”：

1. **内容资产**：知识 K、技能 S、episodic experience；
2. **跨时机制**：记忆 M 的写入、索引、检索、更新、冲突、遗忘；
3. **系统载体**：multimodal agent system 的拓扑、角色、工具、共享状态和交互 loop；
4. **控制原则**：training-free reward/value/advantage 如何改变下一外部动作；
5. **多模态证据等级**：非文本信息只是出现，还是对正确决策具有同运行的因果必要性。

这套分法保留 owner 强调的“知识、技能、记忆都是重点”，同时修正它们不完全同构的问题：知识和技能
主要是可存储内容，记忆主要是跨时间的能力与机制。一个 skill bank 可以同时“存储技能”并“提供记忆
机制”，但除非实验分别改变 skill content 与 persistence policy，否则不得把同一个系统增益重复归因。

当前可供独立复审的 Stage-1B release candidate 是 296 个 canonical works：冻结 226、CURRENT 去重外层
56、本轮 capability delta 14。这个数字不是文献宇宙闭合；303 个一跳 arXiv 引用只提升 6 个，另外 297
个保持 seen-not-promoted。

本方案本身不授权 Stage-1C scale-out。建议的决策顺序是：

1. 独立 reviewer 先审查并决定是否给出 `SIGN_STAGE1B_CAPABILITY_DELTA_RELEASE`；
2. owner 阅读本方案；若认可输入、schema、calibration 与未执行协议范围，再给出
   `AUTHORIZE_STAGE1C_V2_CAPABILITY_EXPERIMENT_MAPPING`；
3. 完成校准包后另取 `SIGN_STAGE1C_V2_EXPERIMENT_MAPPING`，才批量编码 296-paper surface；
4. family/branch portfolio 再经独立签署；Stage-2A 执行仍需单独授权。

## 1. 为什么要按实验族统合，而不是按数据集或论文主题统合

Owner 对“基于实验去统合”的判断是合理的。数据集或数据族通常对应不同失败：长时对话考察跨 session
保持，GUI/terminal agent 考察环境执行，spoken tool use 考察语音到结构化动作，audio reasoning 考察非文本
证据与多步推理。高度相关的数据集会共享任务语义、标注与 evaluator，因此比标题相似的论文更有直接
参考价值。

但数据集不能成为唯一一级轴：

- 同一数据集可以被用于检索、记忆、技能、系统或 evaluator 研究；
- 同名数据集的 revision、split 或预处理不同，结果不能直接合并；
- dataset-derived 工作必须通过 `DERIVED_FROM` 等有来源的 lineage 边连接，不能写成同版本；
- 不同数据集也可能在同一失败机制上构成独立验证或 distribution shift；
- 文本/VLM 实验常与 speech/omni 共享决策结构，但只能是 `PROTOCOL_ANALOGUE`，不能继承数值。

所以 family 的核心签名应是：

`target failure × primary intervention × asset content × persistence × system topology × control regime ×
MM level × evaluation object × outcome semantics × environment/access × paired causal contract`

数据集 lineage 和 relation 用于 family 内分层，而不是覆盖协议兼容性。

## 2. 对“知识、技能、记忆、系统、training-free RL”划分的严格反思

### 2.1 合理之处

第一，它把研究方向从“模型做了什么任务”转到“系统新增了什么能力资产”，更适合回答系统搭建、知识
引入、技能注入、记忆保持分别带来什么任务收益。

第二，它天然支持因果消融：同 core、数据、工具和预算下，分别加入 K、S、M，再研究控制器如何选择它们。

第三，它与本项目 north star 一致：核心模型保持 frozen，创新空间主要在外部资产、系统状态、候选与
reward-guided action control。

第四，它能把高价值 VLM/text agent 实验转译成 speech/omni 协议，而不假装任务或效果可以直接复现。

### 2.2 不合理或危险之处

**一是 K/S/M 不正交。** 一段对话经历可以先作为 episodic memory 保存，再被抽象为知识，最后编译成
skill。若只按论文自称分类，同一个贡献会被算三次。

**二是 memory 更像运算机制。** “memory 中存了 workflow”不等于同时证明 skill 和 memory 两个方向；
必须看实验改变的是 stored content，还是写入/检索/更新策略。

**三是系统与控制不是能力资产。** agent topology 是载体，training-free RL 是决策原则。把它们与 K/S/M
放在同一平面会造成“用了 planner 就算 RL”“有 vector DB 就算 memory capability”的错误。

**四是 multimodal 容易被任务标签冒充。** 多模态输入上的文本 prompt/skill 只能说明 MM1；资产保存图像
或音频是 MM2；只有移除/替换非文本证据会改变正确决策，且排除 transcript shortcut，才是 MM3。

**五是 frozen core 不等于没有学习。** XSkill、AutoSkill、Anything2Skill 等都可能在外部资产上使用标注、
成功/失败轨迹、LLM 编译或在线更新。必须分别记录 core update、asset construction、online update 和
label/test exposure。

**六是“技能最新”会制造时效偏差。** 2026 年技能论文密集、实验华丽，但 SkillsBench 和 SkillFlow 同时
表明效果依赖 harness、fit、修复能力与版本；自生成 skills 甚至可能低于 no-skill。不能因为论文新就优先
选题，也不能忽视多模态知识和记忆。

**七是整个系统的提升不等于组件提升。** GEMS 的顺序集成同时改变 agent、memory、skill；这类结果只能
证明 bundle，而不能把增益拆给三个方向。

### 2.3 扩充后的编码坐标

每个 paper、run cell 和 family 至少编码：

- `primary_direction`：D0/D1/D2/D3/D4；
- `asset_content_type`：declarative knowledge / procedural skill / episodic experience；
- `persistence_scope`：none / within episode / cross episode / long term；
- `system_carrier`：single call / fixed workflow / planner-actor / specialist federation 等；
- `control_status`：static、heuristic、judge-gated、reward-guided、trained-policy boundary；
- `multimodality_level`：MM0–MM3；
- `external_asset_construction`、`external_asset_online_update`、`label_or_test_exposure`；
- `causal_attribution`：isolated、partial、unresolved、instrumental 或 mixed。

这不是为了增加标签，而是为了防止错误归因和重复计数。

## 3. Stage-1C v2 的输入与输出

### 3.1 建议输入

只有 `SIGN_STAGE1B_CAPABILITY_DELTA_RELEASE` 后，输入才冻结为：

1. Stage-1B v5 的 226 个 canonical paper records；
2. CURRENT 59-route appendix 中与 226 去重后的 52 个 works；
3. TRACE、S2S-Arena、MTalk-Bench、SimulU 四个 priority works；
4. 本轮八个 seeds 与六个 citation promotions；
5. 对应 metadata、full text、代码/数据/版本与 hash locator；
6. 既有 dataset locks、local asset matrix、code loaders/entrypoints 和 access/terms 状态；
7. append-only reviewer/adjudication provenance。

合计 296 个 canonical works。297 个 seen-not-promoted citations 不进入 paper audit；以后若因明确路径原因提升，
必须再走新的 Stage-1B delta transaction。

### 3.2 建议输出

Stage-1C v2 只产生证据和未执行设计：

- 296/296 paper disposition 与 audit；
- 承重论文的 run cells、observations 与 paired comparisons；
- dataset lineage/relation graph；
- experiment-family cards；
- K/S/M × system × control 的横向能力图谱；
- 本地 `LOCAL_READY / LOCAL_ADAPTABLE / BLOCKED_ASSET_OR_TERMS / TRANSFER_ONLY` 协议；
- 通过五项门的未排序 research branch portfolio；
- Stage-2A reproduction funnel 的 arms 与 kill gates。

不产生模型调用、benchmark metric、项目 reproduction 结果、prototype、问题排名、owner selection 或 novelty
verdict。

## 4. 本轮新增证据如何改变研究判断

### 4.1 系统 D0：仍是必要基线，但证据不足以单独归因

GEMS 证明 agent-native generation、trajectory memory 和 on-demand skills 可以形成完整研究系统，但其顺序
集成不是 factorial。Stage-1C 必须把 single call、fixed workflow、agent loop 与 K/S/M 资产分开，否则“系统
收益”会吞掉所有能力归因。当前结论是 `INSUFFICIENT_EVIDENCE`，不是系统路线无效。

### 4.2 知识 D1：检索增益存在，多模态必要性尚未建立

RMR 的 no-retrieval、retrieval、k 与 modality 设置值得借鉴，但 text-only 条件也很强，且近邻 exemplar 可能
携带答案。Anything2Skill 进一步表明 skill compilation 可以和 raw RAG 形成四臂比较，但它是 MM0 文本
命令行任务。当前最重要的 residual 不是“RAG 是否有用”，而是：

- 非文本 evidence 是否在 information-matched transcript/caption 之外改变正确决策；
- active evidence acquisition 是否优于一次性 top-k；
- source→skill compilation 是否超过对同一 source 的 raw access。

因此 D1 当前为 `MIXED / MM3_INSUFFICIENT`。

### 4.3 技能 D2：证据最密集，但正负结果同时更强

MMSkills 与 RESOURCE2SKILL 提供高价值设计：text/state/image skill、branch loading、matched briefs、同 backend、
representation/source/selection ablation 和 human calibration。XSkill 说明 experience 与 skill 可以分开消融，
但外部资产构造使用训练 split 的 ground truth。Anything2Skill 提供 raw RAG 与 compiled skill 的直接对照。

反面证据同样承重：

- MMSkills 的 text-only arm 在某些模型上低于 no-skill；
- SkillsBench 有广泛平均增益，但 87 个任务中 13 个为负；self-generated skills 在三个 harness 上均低于
  no-skill；
- SkillFlow 中部分模型/harness 退化，坏 skill 会跨任务传播，skill inflation 和修复失败比缺少 skill 更重要；
- SRA 表明 recall/load 并不等于 incorporation/use。

因此 D2 的结论必须是 `MIXED`。研究对象应从“有没有 skill”升级为“skill 是否适用、是否被正确加载、
是否正确执行、是否可验证与修复”。

### 4.4 记忆 D3：已有强协议，仍需拆 content 与 persistence

原始 LoCoMo 给出 long-range、multi-hop、temporal、adversarial、summarization 与 multimodal dialogue outcomes，
但 QA/summary 用 image caption 替代图像。M2A 在 derived LoCoMo 上加入 raw/semantic 双层、tri-path 与迭代，
但多个组件共同变化且依赖自动 judge。Memory-R1 的 ADD/UPDATE/DELETE/NOOP 与 downstream answer reward 很
有启发，但 PPO/GRPO 会更新参数，只能是 trained boundary。

因此 D3 当前为 `MIXED`。关键 residual 是 evidence-preserving multimodal memory 是否相对 raw history 或
text summary 保留真正承重的 acoustic/visual state，以及 update/conflict/forget policy 是否降低污染而非只提高
retrieval。

### 4.5 控制 D4：统一假设仍成立，但新增 direct anchor 为空

本轮没有发现可直接充当 speech/omni、external black-box、training-free reward-guided reproduction anchor 的
论文。SRA 是 selection instrument；Memory-R1 是 trained boundary；普通 top-k、self-consistency 或 reflection
也不自动构成 RL。

D4 的最小定义仍是：核心权重不更新，live reward/value/advantage 对 retrieve、load、compose、update、reject、
stop 或 repair 的下一外部动作具有因果作用。当前证据状态为 `INSUFFICIENT_EVIDENCE`，必须在 Stage-1C 中
继续从已签署 speech priors 找 task-matched nearest anchor，而不能把 VLM/text analogue 写成复现。

## 5. 研究问题与可证伪假设

### RQ0：系统载体

在 K/S/M pool、工具、输入和预算相同的条件下，agent loop 是否相对 frozen-core 单次调用提高任务完成与
过程恢复？

`H0-SYS`：任何增益都由更多工具、context 或 K/S/M 资产解释；控制后 system effect 消失。

### RQ1：多模态知识

非文本证据是否提供 information-matched text 无法替代的决策信息？主动补证是否能提高 realized oracle
headroom？

`H0-K`：text-only 或等 token irrelevant/matched context 解释全部收益；shuffled non-text evidence 同样有效。

### RQ2：多模态技能

带适用条件、状态证据、动作步骤、验证与 fallback 的 multimodal skill，是否优于 no-skill、text procedure
和 raw source access，并在 held-out tasks 上可复用？

`H0-S`：技能只是额外 context；oracle skill 也无 headroom，或自动 skill 的 harm/negative transfer 抵消收益。

### RQ3：多模态记忆

保留原始声学/视觉 evidence pointer 的 memory，是否在长时、更新与冲突任务上优于 raw history 和 text
summary，同时降低错误检索与污染？

`H0-M`：目标长度下 raw history 稳定支配；非文本 evidence 不改变答案；更新策略增加 staleness/harm。

### RQ4：training-free reward-guided orchestration

给定相同 K/S/M candidate pools，live reward-guided policy 是否比 static/top-k、LLM planner 或 judge gate 更好
地选择资产、停止与修复？

`H0-R`：oracle headroom 不足，reward 不改变下一动作，或 cost/harm-adjusted utility 不优于静态规则。

## 6. 建议形成的八个 experiment families

以下均为 `PROPOSED_BY_PROTOCOL_ANALOGY`，不是已有论文复现，也不是 novelty claim。每个 family 在实际编码
后还可 merge/split；这里不预注册 branch 数量，不排序。

### F0 — Frozen-core system harness isolation

- `primary_direction`：D0；
- 参考：GEMS、MM-ReAct、Agent-Omni 等系统拓扑；
- 关系：reference/borrow，不是 reproduction；
- 固定：core、输入、工具权限、K/S/M pool、evaluator 和阶段预算；
- arms：single call；fixed workflow；planner/actor；specialist orchestration；
- outcomes：task success、milestone progress、tool calls、latency/cost、harm、repairability；
- strongest alternative：更多 context、tool access 或并行 sampling；
- kill：matched-budget 且工具/K/S/M 相同后，system arm 的预注册最小效应不成立；
- readiness：`LOCAL_ADAPTABLE`，依赖 W1 baseline 与统一 harness。

### FK1 — Speech/omni evidence necessity

- `primary_direction`：D1；
- 借鉴：RMR 的 no/retrieval、modality、k；LoCoMo 的 answer-turn provenance；
- 本地候选：MMAR `3bd051...`、MMAU-mini `42bd87...`、MMSU `548e22...`、Audio2Tool
  `f1388da...` 的受控 slice；
- arms：internal-only；text/transcript evidence；structured acoustic cues；raw audio evidence；oracle evidence；
  modality-shuffled/irrelevant matched-token negative control；
- observations：answer/task success、evidence recall/precision、source grounding、missing-evidence detection、calls；
- MM3 gate：raw/structured audio 相对 information-matched text 改变正确 outcome，shuffled audio 无效；
- kill：text 或 irrelevant context 解释全部增益，或 retrieval 直接泄漏答案；
- readiness：`LOCAL_ADAPTABLE`；数据在本地，但需冻结 loader、task slice 与 evaluator。

### FK2 — Declarative knowledge to reusable skill compilation

- `primary_direction`：D1→D2；
- 借鉴：Anything2Skill 的 Base/RAG/Skill/RAG+Skill；RESOURCE2SKILL 的 source/representation ablation；
- source 固定为同一公开教程、工具文档或非评测任务轨迹；
- arms：no source；raw source RAG；distilled text skill；multimodal skill；RAG+skill；oracle procedure；
- held-out contract：source 构造与 evaluation task/example 不重叠；
- outcomes：task transfer、retrieval/load/use、steps、error、token/calls、source faithfulness；
- kill：skill 只压缩答案，无法跨 task 复用；raw RAG 达到相同 utility；
- readiness：`LOCAL_ADAPTABLE`，需先建立 leakage audit 和 skill compiler provenance。

### FS1 — Multimodal skill package factorial

- `primary_direction`：D2；
- 借鉴：MMSkills 的 no/text/state/image/loading、RESOURCE2SKILL 的 matched briefs、SkillsBench 的 paired trials；
- 本地候选：Audio2Tool revision-bound content、工具 descriptions、非测试公开教程；
- skill contract：when/when-not、precondition、audio/visual state cue、action/tool steps、verification、failure、
  fallback、source/version；
- arms：no skill；information-matched source；text procedure；state-card skill；raw-audio/visual-reference skill；
  runtime-gated full skill；oracle skill；
- outcomes：task/tool success、skill retrieval/load/invocation/use、argument correctness、steps、harm、cost；
- falsifiers：wrong-but-plausible、stale、version-mismatched、overlong skill；
- kill：oracle skill 无 headroom；text-only 已解释收益；自动 skill 的负迁移或 harm 超过预注册界限；
- readiness：`LOCAL_ADAPTABLE_WITH_TERMS_GATE`；Audio2Tool 本地完整但 CC-BY-NC-4.0，需用途复核与 adapter。

### FS2 — Skill lifecycle, repair and negative transfer

- `primary_direction`：D2，persistence 为 cross-episode；
- 借鉴：SkillFlow 的 sequential family、empty library、raw-history control、cost/library health；AutoSkill 的
  versioned lifecycle；XSkill 的 experience/skill 双流；
- arms：no persistence；append-only trajectories；create-only skills；create+retrieve；create+retrieve+repair；
  oracle-maintained library；
- family reset：不同 task family 之间重置，防止 retrieval confound；
- outcomes：create precision、reuse、repair success、library size/duplication、negative transfer、cost、final outcome；
- stress：第一任务写入错误或过时 skill，观察后续是否识别、修复或继续传播；
- kill：repair policy不能降低错误传播，library growth 与 utility 无关或为负；
- readiness：`LOCAL_ADAPTABLE`；需定义可验证的 sequential task families 和 append-only trajectory audit。

### FM1 — Evidence-preserving multimodal memory carrier

- `primary_direction`：D3；
- 借鉴：LoCoMo 的长时/temporal/adversarial outcomes；M2A 的 raw+semantic、tri-path；
- 本地候选：IHBench revision `cbd828...`、多轮 spoken histories、Full-Duplex-Bench v3 受控 slice；
- arms：current turn；raw history；text summary memory；semantic memory；raw-audio-pointer evidence memory；
  oracle memory；
- 固定：stored information content 尽量 information-matched，单独改变 carrier/retrieval；
- outcomes：evidence recall、temporal/multi-hop correctness、resume point、speaker/prosody fidelity、harm、latency；
- kill：raw history 在目标 horizon 稳定支配；multimodal pointer 不改变正确 outcome；压缩不可恢复承重证据；
- readiness：IHBench `LOCAL_ADAPTABLE`；Full-Duplex-Bench v3 在 license/evaluator closure 前
  `BLOCKED_ASSET_OR_TERMS`。

### FM2 — Memory update, conflict, decay and refusal

- `primary_direction`：D3；
- 参考：M2A 的 iterative refinement；Memory-R1 的 ADD/UPDATE/DELETE/NOOP 只借 action space，不复现训练；
- arms：append-only；heuristic update；conflict-aware update；reward-guided training-free update；oracle update；
- controlled perturbations：correct、stale、conflicting、speaker-shift、modality-disagreeing memories；
- outcomes：write precision、update/delete correctness、conflict resolution、abstention、pollution、downstream task；
- strongest alternative：更强 retrieval 而非 update policy；
- kill：update policy不能降低污染，或错误写入比无 memory 更有害；
- readiness：`LOCAL_ADAPTABLE`，需构造 ground-truth state-transition 与 deterministic verifier。

### FR1 — Training-free reward-guided K/S/M orchestration

- `primary_direction`：D4；
- 边界：Memory-R1 是 trained RL；SRA 是 selection instrument；两者都不是本项目复现；
- 输入：FK/FS/FM 产生的同一 K/S/M candidate pools；
- actions：retrieve、inspect、load、compose、reject、update、stop、repair；
- arms：static/top-k；LLM planner；verifier/judge gate；reward/value/advantage sequential control；oracle selector；
- reward contract：live signal 必须改变下一外部动作，只给最终输出离线打分不算；
- outcomes：realized oracle headroom、selection regret、task utility、unnecessary calls、harm、latency、stop/repair；
- evaluator stress：加入 noise、bias、miscalibration 和 disagreement；
- kill：oracle headroom不足；reward arm 不优于 static/heuristic；收益只出现在 proxy 而不出现在 task outcome；
- readiness：`LOCAL_ADAPTABLE_AFTER_TASK_AND_EVALUATOR_FREEZE`。

## 7. Run cell、observation 与 paired comparison 数据合同

Stage-1C v2 不把“一次运行”和“一次方法比较”混成同一 cell。

一个原子 `run_cell` 身份至少包含：

`paper × dataset/revision/lineage/split/slice × preprocessing/input × core/revision/access × prompt ×
system topology × K/S/M assets/version/provenance × persistence policy × tools × intervention ×
decision rights × reward-next-action effect × budget/horizon × seed/aggregation`

同一运行的 accuracy、task success、WER、MOS、latency、cost、harm 等是多个 observations，不重复 cell。
运行条件发生实质变化才新建 cell。

`paired_comparison` 明确 baseline 与 intervention 两个 cell，并分为：

- `EXACT_PAIRED`：除预声明 intervention 外全部关键字段匹配；
- `PARTIALLY_MATCHED`：存在已知混杂，只允许并列与不确定性陈述；
- `UNPAIRED_PARALLEL`：只作定性证据。

跨论文数值比较要求 dataset revision、split、core、access、input、prompt/system、metric/evaluator、budget 全部
匹配。本轮 delta 的论文报告数值全部保留在 paper 内，不作 pooled effect。

## 8. Dataset graph 与 experiment family 规则

Lineage 只在有来源时使用：`SAME_REVISION / DERIVED_FROM / SUBSET_OF / TRANSLATED_FROM /
AUDIO_RENDERING_OF / REANNOTATED_FROM / SPLIT_OF`。

实验关系使用：`INDEPENDENT_SAME_TASK / CROSS_DATASET_VALIDATION / DISTRIBUTION_SHIFT_TEST /
PROTOCOL_ANALOGUE`。

M2A 的 enhanced LoCoMo 应登记 `DERIVED_FROM` original LoCoMo，不能写 `SAME_REVISION`。文本/VLM protocol
迁移到 speech/omni 只登记 `PROTOCOL_ANALOGUE`。

Family membership：

- `CORE_MEMBER`：问题、outcome、environment/access 与 paired contract 兼容；
- `VALIDATION_MEMBER`：同问题的独立 dataset 或 shift；
- `TRANSFER_ANALOGUE`：决策结构同构但领域不同；
- `FALSIFIER`：挑战能力、metric 或策略；
- `INSTRUMENT_SUPPORT`：提供 evaluator/measurement/calibration。

每个 family 必须输出支持、null/negative、strongest contradiction、替代解释与不确定性，状态只能是
`CONSISTENT_SUPPORT / MIXED / NULL_OR_NEGATIVE / INSUFFICIENT_EVIDENCE`。

## 9. 本地资产与 readiness

| 协议 | 本地证据 | 当前 readiness | 闭合条件 |
|---|---|---|---|
| F0 system harness | W1 frozen baseline、common adapters、已有 tool/evaluator skeleton | `LOCAL_ADAPTABLE` | 冻结统一 harness、tool/access、budget |
| FK1 knowledge | MMAR、MMAU-mini、MMSU、VoiceBench 等 revision/content-locked 数据 | `LOCAL_ADAPTABLE` | 选 slice、loader、transcript/raw evidence、evaluator |
| FK2 compilation | 工具文档、非测试教程、Audio2Tool tool schema | `LOCAL_ADAPTABLE` | source/test leakage audit、compiler provenance |
| FS1 skill | Audio2Tool 71,441 revision-bound files，revision `f1388da...` | `LOCAL_ADAPTABLE_WITH_TERMS_GATE` | CC-BY-NC 用途复核、skill adapter、verifier |
| FS2 lifecycle | 可从本地 tool tasks 构建 sequential families | `LOCAL_ADAPTABLE` | family split、trajectory schema、repair verifier |
| FM1 memory carrier | IHBench repo commit `46cfbd...`、dataset `cbd828...`; Full-Duplex-Bench v3 bytes local | mixed | IHBench adapter；Full-Duplex license/evaluator closure |
| FM2 update/conflict | IHBench structured workflows、可控 state transitions | `LOCAL_ADAPTABLE` | ground-truth state/update contract |
| FR1 reward control | deterministic task rewards、speech judges/instruments 候选 | conditional | task、reward identity、noise model、next-action API 全冻结 |

VoiceAgentBench 虽 repo/data 本地锁定，但 community license 需 downstream-use review；Full-Duplex-Bench v3
release route未明确 dataset license；Audio2Tool 是 CC-BY-NC-4.0。资产“在本地”不等于 `LOCAL_READY`。

## 10. 参考、借鉴与复现的具体落位

### 10.1 参考

GEMS、AutoSkill、SKILLFOUNDRY、Memory-R1 主要作为系统边界、lifecycle、本体或 trained-policy 对照。我们
可以引用其概念、失败与 action space，但不声称使用其完整方法或复现其效果。

### 10.2 借鉴

RMR、Anything2Skill、MMSkills、RESOURCE2SKILL、SkillFlow、SkillsBench、LoCoMo、M2A、SRA、XSkill 的高
价值部分是实验设计：paired arms、modality/state ablation、source-versus-skill、sequential family、negative
transfer、retrieval-versus-use、long-range/conflict outcomes。迁移到 speech/omni 后必须写
`PROPOSED_BY_PROTOCOL_ANALOGY`，逐项声明保留与改变的元素。

### 10.3 复现

当前 14 条 delta 中 reproduction anchor 数为零。Stage-1C 必须在 296-paper signed surface 内寻找 task/access-
matched speech/omni nearest prior。进入 branch 的 reproduction arm需声明：

- `EXACT_REPRODUCTION`；或
- `CLOSE_REPRODUCTION_WITH_DECLARED_DEVIATIONS`；或
- `TASK_MATCHED_METHOD_TRANSFER`，且不得叫原实验复现。

完整 OSWorld、terminal 或 scientific-agent 环境不应为了“看起来更强”而直接复现；除非它本身成为目标任务，
否则只作 transfer analogue。

## 11. 296-paper 编码、校准与复核流程

### Phase A — pre-scale calibration

从 296 works 中按 role、D0-D4、task/data、empirical/non-empirical、MM0-MM3 分层抽取小批量。至少包含：

- 本轮 14 条全部；
- 一个 direct speech/omni method；
- 一个 measurement instrument；
- 一个 negative/falsifier；
- 一个 dataset lineage case；
- 一个 bundled attribution case；
- 一个 H5-dependent case。

双编码并裁决 primary direction、content/persistence、MM level、run-cell 边界、paired status、family membership
与 reference/borrow/reproduce。只有关键字段一致率和所有分歧裁决完成，才提交
`SIGN_STAGE1C_V2_EXPERIMENT_MAPPING`。

### Phase B — full audit

- 296/296 canonical works 全量主编码，恰好一次；
- empirical load-bearing works 抽取承重实验、negative/null、modality、causal ablation 与限制；
- non-empirical/boundary works 作为 claim、机制或 falsifier 节点，不伪造 cell；
- 至少 20% 按 role/data/task 分层盲审；
- 所有 CORE_MEMBER、dataset lineage、family conclusion、reproduction anchor 与 branch card 100% 复核裁决；
- audit rows append-only，修订通过 adjudication event，不原位重写已裁决历史。

### Phase C — family and local protocol synthesis

按 dataset lineage/access 分层合成，不跨不可比 strata 做数值平均。每个本地 family 形成 readiness、adapter、
evaluator、strongest falsifier 与 kill criterion。

### Phase D — emergent branch portfolio

一个 family 只有同时满足以下五项才可成为 primary branch：

1. `LOCAL_READY` 或有明确 closure checklist 的 `LOCAL_ADAPTABLE`；
2. 清晰、可证伪 residual；
3. task-matched nearest prior/reproduction anchor；
4. 可观察 outcome、ground truth 或 evaluator；
5. strongest falsifier 与预注册 kill criterion。

每个 branch 必须含 frozen-core single-call、nearest-prior reproduction、candidate strategy 和可定义时的 oracle。
不满足者留在 family map，不能为凑数量升级。

## 12. 审查接受标准

- 296 IDs 全覆盖、无重复、无无理由退出；
- 226 frozen records 和 v5 release hash 不变；
- 每个 empirical run cell 有稳定 ID、完整配置和 source locator；
- 多 metric 不复制 cell，运行条件变化必须新建 cell；
- 每条 lineage 有来源；语义相似只登记 relation；
- CORE_MEMBER 通过问题、outcome、environment/access 与 comparison compatibility；
- 不匹配 comparability key 的 observations 不进入跨论文数值聚合；
- 每个 family 有 contradiction、uncertainty、readiness 与 kill；
- MM3 只由同运行 modality-necessity evidence 支撑；H5 未闭合不得泛化；
- 参考、借鉴、复现字段完整，迁移设计不得冒充 reproduction；
- 所有 `READY_FOR_FUNNEL` branches 通过五项门并有统一 arms；
- schema、hash、manifest、Windows/WSL path、可重复生成和 audit immutability 通过机器检查；
- 全流程不产生研究模型调用、benchmark metric、reproduction 结果或 prototype。

## 13. 风险与控制

| 风险 | 控制 |
|---|---|
| 最新技能论文吸引注意导致方向偏置 | D1/D2/D3 平行建 family，不按论文数量或年份投票 |
| K/S/M 重叠导致双重归因 | content、persistence、primary intervention 分字段；bundle 标 unresolved |
| 多模态任务被 text shortcut 解决 | MM0-MM3 门、matched text、shuffled modality、same-run ablation |
| 技能泄漏 evaluation 答案 | source/test isolation、task overlap audit、held-out transfer |
| 自生成技能累积错误 | SkillFlow-style sequential stress、repair/forget、negative transfer 指标 |
| memory 压缩损失声学/视觉证据 | raw pointer arm、evidence fidelity、conflict/update outcome |
| judge/reward 偏差被误当成 utility | deterministic verifier 优先；proxy/task 分离；noise/disagreement stress |
| “frozen”掩盖外部监督 | 单列 asset construction/update 与 label/test exposure |
| 协议借鉴被写成复现 | 强制 use relation 与 reproduction subtype；task mismatch fail closed |
| 本地存在被误写成 ready | loader、revision、license、evaluator、access 全闭合才 LOCAL_READY |
| citation 扩展无限膨胀 | 有界触发、Stage-1B delta transaction、seen-not-promoted 不进 denominator |

## 14. 预期研究贡献形式（非 novelty verdict）

如果后续实验支持，本项目可能形成四类可检验贡献，但当前不作新颖性或有效性判断：

1. 一个能隔离 system、knowledge、skill、memory 和 reward-guided control 的 speech/omni 因果实验框架；
2. 一套 evidence-preserving multimodal K/S/M 资产合同与 modality-necessity 评估；
3. 一个在冻结核心之上对 K/S/M 选择、停止、修复进行 live reward-guided control 的外部控制面；
4. 一组同时报告 headroom、selection utility、harm、cost、staleness 与 negative transfer 的实验协议。

这些只是 residual hypotheses 与设计目标。是否构成技术创新、是否优于 nearest prior，要到 Stage-2A
reproduction-first 和 Stage-2B matched evaluation 后才能判断。

## 15. 一手来源与项目证据

### 本轮 capability delta 一手论文

- [RMR](https://arxiv.org/abs/2405.20834)
- [M2A](https://arxiv.org/abs/2602.07624)
- [XSkill](https://arxiv.org/abs/2603.12056)
- [GEMS](https://arxiv.org/abs/2603.28088)
- [Skill Retrieval Augmentation](https://arxiv.org/abs/2604.24594)
- [MMSkills](https://arxiv.org/abs/2605.13527)
- [Anything2Skill](https://arxiv.org/abs/2606.09316)
- [RESOURCE2SKILL](https://arxiv.org/abs/2606.29538)
- [AutoSkill](https://arxiv.org/abs/2603.01145)
- [SKILLFOUNDRY](https://arxiv.org/abs/2604.03964)
- [SkillFlow](https://arxiv.org/abs/2604.17308)
- [SkillsBench](https://arxiv.org/abs/2602.12670)
- [LoCoMo](https://arxiv.org/abs/2402.17753)
- [Memory-R1](https://arxiv.org/abs/2508.19828)

### 项目内证据

- `data/capability-delta-records-v1.json`：14 个 exact-ID、full-text hash、路径与实验设置记录；
- `data/one-hop-promotions-v1.json`：6 个提升与 parent edge；
- `data/canonical-census-v1.json`：226→282→296 去重审计；
- `docs/checks/stage1b-capability-delta/2026-07-23-rc1/`：机器报告；
- `docs/datasets.lock.json`：本地数据 revision/status；
- `docs/checks/stage1b-closeout/2026-07-22-v4/stage1c-asset-acquisition-matrix.json`：本地资产、许可与
  Stage-2 blocker；
- `wiki/survey/current/stage1b-transition-reference-appendix.md` 与 CURRENT priority intake：继承证据面。

## 16. 建议 owner 授权边界

若独立 reviewer 已登记 `SIGN_STAGE1B_CAPABILITY_DELTA_RELEASE`，且 owner 认可本 proposal，可使用：

`AUTHORIZE_STAGE1C_V2_CAPABILITY_EXPERIMENT_MAPPING`

建议该 token 只授权：冻结 signed 296-paper input、完善 schema/codebook、构建 calibration packet、执行 paper
disposition/experiment extraction/dataset graph/family mapping、生成未执行 local protocols 与 branch candidates。

它不应授权研究模型/API 调用、benchmark metric、论文 reproduction、prototype、Stage-2A、branch 选择/排名或
novelty verdict；scale-out 前仍需 `SIGN_STAGE1C_V2_EXPERIMENT_MAPPING`，family/branch freeze 后仍需
`SIGN_STAGE1C_V2_FAMILY_BRANCH_PORTFOLIO`。
