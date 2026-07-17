---
artifact_id: "SF-PRESS-QUERY-REVIEW-C4C-2026-07-18-01"
title: "SF-L14/L15 方法占位 lane 的 PRESS 式独立检索策略复审（正典存档）"
date: 2026-07-18
reviewer: "隔离子代理（Opus,零设计历史上下文）——owner 裁决 2026-07-18-②a:独立查询复核人 = 隔离代理 + owner 抽查"
review_subject: "C4C 新增 4 条查询片段(SF-L14-Q1/Q2,SF-L15-Q1/Q2) + 对照 61 条冻结查询/7 篇触发论文/T1 词表 v1"
verdict: "HARDCODING: NO / BOOLEAN: PASS / MAJOR x1 + MINOR x5 + OBSERVATION x7"
adoption: "MAJOR(steering/controlled-decoding 词族并入 L14-Q2)已采纳;MINOR 采纳 3 项(abs:frozen 入 L14-Q1,\"inference compute\" 入 L15-Q1,\"majority vote\"/\"self-refine\" 入 L15-Q2);采纳后三个思想实验摘要 TE-1/2/3 全部机器命中(采纳前 TE-2 漏检);O-3/O-4 宏化重构 + 可选补类(eess.IV/eess.SP/cs.IR)登记执行期债务表;O-2 已由我方 matcher 复现独立解决(2512.19433 实命中 SF-L5-Q5,与 P0-R9 评审 0-hit 表之部分异议独立收敛)"
provenance: "评审全文 = 代理最终消息逐字存档(仅前置本 frontmatter);评审人未参与 L14/L15 设计,未接触设计会话上下文"
---

# 检索策略同行评审报告 — SF-L14/L15 补救 lane（PRESS 独立复审）

**评审人角色**：独立检索策略同行评审（未参与查询设计）。只读复审，未修改任何文件。
**评审对象**：4 条新片段（SF-L14-Q1/Q2、SF-L15-Q1/Q2）；参照 61 条冻结查询、7 篇触发漏检论文、T1 会议路由词表 v1。

## 0. 总裁决

- **HARDCODING: NO** — 四条新 lane 是概念性方法占位轴，不是 7 篇的单篇捕获器。判据证据：(a) 逐组词项均为通用方法族词汇（orchestration/controller/routing、decoding+guidance/contrastive、test-time scaling 家族、self-verification/best-of-n 家族），无任何只可能来自某单篇题名的特异短语；(b) 关键——ThinkOmni 的方法名 "Stepwise Contrastive Scaling"、"LRM-as-a-Guide"，2508.10016 的 "cross-modal memory"，2512.19433 的 "trajectory exploration scaling" **均未被逐字写入**，设计方把题名短语**拆解成通用二元/三元词**（decoding AND guidance，而非 bigram "guidance decoding"）；(c) 3 个用完全不同措辞构造的假想论文中 2 个被接住（详见 §2），证明命中不依赖 7 篇原文词句。
- **BOOLEAN: PASS** — 4 条片段括号全部配对（L14-Q1 3组/L14-Q2 3组/L15-Q1 2组/L15-Q2 3组，各 open=close），每个 OR 组均显式括号封闭、组间纯 AND 连接，无裸 AND/OR 混用，无运算符优先级歧义；`abs:` 前缀、带连字符的引号短语、裸缩写（VLM/MLLM）风格与既有 61 条一致。
- **分级 findings**：MAJOR ×1，MINOR ×5，OBSERVATION（新 lane）×2，OBSERVATION（既有 61 条顺带）×5。
- **主验收结论**：6 篇可被 arXiv 查询接住的漏检论文（第 7 篇 ACL-F26-383 为会议路由件、cats=[]，本就不走 arXiv SF 查询，由词表 A 组 "test-time" 接住）**全部被新 lane 命中**（命中链见 §2 末）。补救达成其首要目的。以下 findings 均为改进项，非否决项。

## 1. 布尔与语法

| 片段 | 组数 | 括号 | 逻辑 | 结论 |
|---|---|---|---|---|
| SF-L14-Q1 | 3（系统对象轴 / 模态 / 免训练家族） | 3=3 平衡 | (OR)AND(OR)AND(OR) | PASS |
| SF-L14-Q2 | 3（decoding / 引导家族 / 模态） | 3=3 平衡 | (单)AND(OR)AND(OR) | PASS |
| SF-L15-Q1 | 2（TTS 家族 / 模态） | 2=2 平衡 | (OR)AND(OR) | PASS |
| SF-L15-Q2 | 3（自验证家族 / 模态 / 时点-采样） | 3=3 平衡 | (OR)AND(OR)AND(OR) | PASS |

- 优先级：既有 61 条依赖「每个 OR 组全括号 + 组间纯 AND」这一安全实践；4 条新片段完全遵守，无歧义。composed 后为 `(cat…) AND submittedDate:[…] AND (<片段>)`，顶层全 AND，无优先级风险。
- 风格一致：L14-Q2 把单项写作 `(abs:decoding)`（单term加括号）是既有 61 条未见的轻微风格差异，无害（OBSERVATION）。
- 大小写：`abs:VLM`/`abs:MLLM`/`abs:"best-of-n"` 依赖 arXiv 大小写不敏感匹配，与既有 `abs:LLM`/`abs:MCTS` 用法一致。

## 2. 硬编码判定（关键验收）

**逐组通用性核验**：
- L14-Q1 group1 `orchestration/orchestrator/controller/routing` = 通用系统对象词族（远超 2508.10016）。
- L14-Q2 group2 `guidance/guide/guided/contrastive` = 通用引导/对比解码词族；`contrastive`+`decoding`+`visual` 恰好覆盖 VCD（Visual Contrastive Decoding）这一 MLLM 去幻觉子领域，是真方法占位，**非**为 ThinkOmni 定制。
- L15-Q1 group1 = test-time scaling 领域的正典词汇。
- L15-Q2 group1 `self-verification/self-consistency/majority voting/best-of-n/self-refinement/self-correction` = 通用推理时选择/自校验词族。

**特异短语扫描**：未发现任何只可能来自单篇题名的短语。对照——若为硬编码，会出现 `abs:"Stepwise Contrastive Scaling"`、`abs:"LRM-as-a-Guide"`、`abs:"trajectory exploration scaling"` 之类；这些**均不存在**。

**3 个思想实验摘要（措辞刻意不同于 7 篇原文）+ 命中判断**：

- **TE-1（测 L14-Q1 编排轴）**：「We propose a modular assistant that *routes* each user utterance to a bank of pre-trained, *frozen* *speech* and vision experts. A lightweight text-based *controller* selects and sequences the experts at inference time without parameter updates. Because the backbone remains *off-the-shelf*, the system integrates new modalities without retraining.」
  → **命中**。group1: `controller` ✓；group2: `speech` ✓；group3: `off-the-shelf` ✓。**注**：`frozen`/`without parameter updates` 不在 group3，本例仅靠 `off-the-shelf` 兜住 → 支持 §3 的 "frozen" 缺口。
- **TE-2（测 L14-Q2 引导解码轴）**：「To improve audio captioning from a *frozen audio-language model*, we *steer* its token generation using *logit adjustments* from an auxiliary scorer. This *decoding*-time *steering* requires no training and no fine-tuning.」
  → **漏检**。group1: `decoding` ✓；group3(模态): `audio` ✓；但 group2 引导家族 `guidance/guide/guided/contrastive` **全不命中**——摘要用 `steer/steering/logit adjustments`。且无其他 lane 覆盖 → **确定性漏检**，构成本报告唯一 MAJOR（steering/controlled-decoding 词族全局无覆盖）。
- **TE-3（测 L15 机制轴）**：「We study whether allocating more *inference compute* helps small *vision-language* models. Comparing repeated *sampling* with *majority vote* against a *best-of-n* reranker, we find gains on multi-step *visual* reasoning.」
  → **命中（经 Q2，非 Q1）**。L15-Q1 group1 需精确短语，`inference compute`（无连字符-time）≠ `inference-time compute` → Q1 漏；L15-Q2: group1 `best-of-n` ✓、group2 `vision-language`/`visual` ✓、group3 `sampling` ✓ → 命中。暴露 Q1 短语脆性与 `majority vote`(单数) 缺口。

**结论**：3 例中 2 例被不同措辞接住，且未依赖原文短语 → 概念轴，非单篇捕获器 → **HARDCODING: NO**。

**7 篇命中链**：2508.10016→L14-Q1（controller+omni+off-the-shelf）；2602.23306→L14-Q2（decoding+Guide/contrastive+omni-modal）；2512.11109/2606.28864/2607.09438→L15-Q1（test-time scaling+VLM/vision-language）；2512.19433→L15-Q2（self-verified+multi-modal+test-time/sampling）；ACL-F26-383→非 arXiv、走词表路由。

## 3. 词汇缺口

**系统对象轴（L14）**
- **[MAJOR] steering 解码词族全局缺失**：`steer / steering / "controlled decoding" / control`——受控/操控解码（controlled decoding、steering vectors、activation steering）是与 guided/contrastive 并列的方法子族，65 条（旧+新）均未覆盖。加入 L14-Q2 group2。噪声：`steering` 亦指激活转向（相关性尚可），中等，可接受。
- **[MINOR] 免训练家族缺 `frozen`**（+ `plug-and-play`/`"plug and play"`、`gradient-free`）：`frozen` 是权重冻结系统最常见自称（且是本项目北极星用语），L14-Q1 group3 六个同义词竟无此项。噪声低（frozen）/中（plug-and-play 亦指成像 PnP 先验）。
- **[MINOR] 编排轴可补** `router`（Q1 有 routing 无 router，arXiv 词干化不保证桥接）、`coordinator`、`cascade`、`expert`（SF-L3-Q2 已用 expert）。`router/coordinator/cascade` 低-中噪声；`expert` 中噪声，视量决定。

**机制轴（L15）**
- **[MINOR] 选择家族缺**：`"majority vote"`（单数，2607.09438 实际用词）、`self-refine`（Madaan 方法正名，词表已收、Q2 未收）、`reranking/rerank`、`"weighted voting"`。arXiv 词干化不保证 vote↔voting、refine↔refinement 互通，建议单复数/动名词并列枚举（成本近零、噪声低）。
- **[MINOR] Q1 短语脆性**：仅收连字符 `*-time` 短语，漏 `"inference compute"`（无 -time）、`"test-time reasoning"`。建议补 `"inference compute"`。注：`"test-time adaptation"`(TTA) 通常改权重、属越界，**不建议**加。

## 4. 类别与窗口

- **13 类全并集合理**——与 L10–L13 的 union 一致，且方法占位轴的真正过滤器是词组而非类别，全并集正是「不按论文该在哪预筛」的正确姿态。7 篇触发论文的类别（cs.CL/cs.CV/cs.LG/cs.AI）全覆盖。
- **[OBSERVATION] 可选补类**：`eess.IV`（图像/视频处理，部分 VLM/video 交叉挂此）、`eess.SP`（信号处理，部分纯音频/语音只挂此）、`cs.IR`（检索/路由/RAG）。因词组已承担过滤、加类近零成本；非必需。
- **窗口 202210–202607 合理**：覆盖全部 7 篇（202508–202607）；符合「窗口不砍」纪律（2025 前保留但作发现道非质量证据）。

## 5. 噪声风险（逐条）

| 片段 | 最宽词组 | 主要噪声源 | mapping 阶段可接受？ |
|---|---|---|---|
| L14-Q1 | group3（test-time/inference-time 常见） | 被 group1 编排词 + 模态双重收窄 | 是，中噪声 |
| **L14-Q2** | **decoding+guided/guidance+visual/video** | **扩散 classifier-free guidance 生成文献**（guided+visual/video+decoding 高频）——四条中最宽 | 是，但预算更重人工筛；量爆则加 scope 词 |
| L15-Q1 | 模态组（visual/video 常见） | 被精确 TTS 短语强收窄——四条中最干净 | 是，低-中噪声 |
| L15-Q2 | group3（sampling/search/scaling 常见） | search+visual+self-* 或引入规划/机器人噪声 | 是，中噪声 |

整体符合已声明姿态（mapping 阶段允许宽召回 + 人工筛）。唯 L14-Q2 需预留更重的人工筛工时。

## 6. 既有 61 条顺带观察（非本次验收对象，仅登记 ≤5）

- **O-1（最高价值）**：L11/L12/L13 把 `(agent OR agentic OR multi-agent)` 设为**强制 AND 组**（与 training-free+模态并列），SF-L2-Q1 把 test-time scaling 与 `(agent/agentic/workflow)` 强制配对——**这正是外审所指术语召回陷阱**，2508.10016/2602.23306/全部 TTS-VLM 论文即死于此闸。新 L14/L15 去闸（全 13 类、无 agent 前提）是对的补救；请复核 L14/L15 是否**完全吸收** L11–L13 的意图，否则那三条 lane 继续漏。
- **O-2（可测的系统性隐患）**：全部 lane 假设 `abs:"test-time"` 能匹配 "Test-Time Scaling" 中的 token。但 **SF-L5-Q5**（verifier AND test-time AND scaling，cats 含 cs.CV，窗口覆盖）按逻辑**本应**接住 2512.19433（三词俱全），若其仍被列为确定性漏检，最可能祸首即 arXiv 连字符/短语匹配行为。建议**实测确认**该假设——它是 65 条查询共同的地基。
- **O-3**：权重冻结 OR 集跨 lane 不一致（frozen/off-the-shelf/training-free/tuning-free/without-fine-tuning/gradient-free 散落不齐）→ 应定义单一可复用宏。
- **O-4**：模态 OR 集跨 lane 不一致（VLM/MLLM 在 L15 有、L14 无；LVLM/LMM/OLLM 全缺；`vision` 与 `visual` 未并列）→ 单一模态宏含缩写+单复数变体。
- **O-5**：单复数/动名词覆盖普遍不足（router↔routing、vote↔voting、refine↔refinement）→ 两形并列，成本近零、噪声低。

---

**签署**：本片段集 **BOOLEAN PASS / HARDCODING NO**，达成补救首要目的（6 篇 arXiv 漏检全部经概念轴命中）。放行前建议至少落地唯一的 MAJOR（steering/controlled-decoding 词族并入 L14-Q2），并对 O-2 做一次 arXiv 连字符匹配实测以护住整套查询地基；其余 MINOR/OBSERVATION 为低成本增益，可批量并入 O-3/O-4 的「宏化」重构一次性处理。

---

## 附：设计方采纳记录（2026-07-18,评审后动作）

1. **MAJOR 采纳**：`abs:steering OR abs:steer OR abs:"controlled decoding"` 并入 SF-L14-Q2 引导家族组。
2. **MINOR 采纳 3 项**：`abs:frozen` → L14-Q1 免训练组；`abs:"inference compute"` → L15-Q1；`abs:"majority vote"` + `abs:"self-refine"` → L15-Q2。
3. **采纳后机器复验**：TE-1→SF-L14-Q1、TE-2→SF-L14-Q2（采纳前漏检）、TE-3→SF-L15-Q1+Q2——三个异措辞思想实验全命中；7 篇触发论文命中链不变；编译器 65/65 PASS、前缀 61 逐字节不变。
4. **O-2 处置**：与我方 P0-R9 复现独立收敛——正典 matcher 下 2512.19433 实命中 SF-L5-Q5、2607.09438 实命中 SF-L5-Q1（P0-R9 评审 0-hit 表 2/7 行不成立,见 C4C 回应信有据异议节）；arXiv 线上连字符行为实测归入执行首步（REC-7 同批）。
5. **未采纳项登记债务表**（amendment-8 §债务）：O-3/O-4 宏化重构、可选补类 eess.IV/eess.SP/cs.IR、reranking/"weighted voting"/plug-and-play/router/coordinator/cascade 等扩词——执行期首轮召回数据到手后一次性评估（避免签署前无限加词）。
6. **O-1 复核结论**：L15-Q2 的 self-* 家族已无 agent 闸覆盖 L11-Q2 词族意图；L11–L13 保持不动（append-only,其 agent 词族对真用 agent 语言的文献仍是有效通道）。
