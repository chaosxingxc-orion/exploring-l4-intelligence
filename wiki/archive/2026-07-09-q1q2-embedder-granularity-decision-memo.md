# 2026-07-09 · Q1/Q2 决策备忘录：嵌入器选型结构 × 任务粒度的知识组织（Stage-1 讨论材料）

> **性质**：Stage-1 论证/讨论文档，为 owner 2026-07-09 提出的两个设计问题给出**带推荐的决策单**，
> 覆盖 `2026-07-08-speech2vec-survey-2025plus.md` §7 留下的八项议程。**本文不做最终选型**——
> 每项推荐都留 owner 裁决位；数据裁决类问题（H-a vs H-b、主键对决）交给数据轨预注册测评。
> **依据**：07-08 调研（40 条对抗验证：34 CONFIRMED/6 PARTIAL/0 REFUTED）+ 本日三路审计
> （`2026-07-09-three-anchors-delta-regrade.md`）+ owner 本日裁定（A2 再定级；三条方法论要求）。

## 0. 两个问题（owner 原文大意）

- **Q1**：不同任务的语音向量是否应该用统一模型提取？emotion2vec、speech codec 等特征表示
  是否需要纳入考虑范围？
- **Q2**：不同语音片段/任务需要的向量表征不同——ASR 的知识引入更多是记录困难样本供后续使用；
  SLU 意图识别需要整段向量；SLU 槽位提取需要段落中的片段信息。这些如何有效组织与处理？

## 1. Q1 — 统一 vs 任务特化嵌入器

### 1.1 先分解命题：统一 *schema* ≠ 统一 *嵌入空间*

这两层经常被混着讨论，必须拆开：

- **存储/工程层（schema、索引、审计、快照）应当统一**——一套 kb_schema/kb_index/kb_audit
  管全部任务族，key 空间作为 source 的属性字段（`embedder` 已在 manifest 中）。这是纯工程
  决定，无需实验裁决。
- **嵌入空间层**：key 空间定义"相似"的语义，而各任务的等价类**彼此正交**——内容同/说话人异
  （ASR、QA）↔ 情感同/内容异（SER）↔ 意图同/措辞异（SLU）。一个空间难以处处最优，这不是
  猜测而是 2025-26 文献的结构性结论（下节）。

### 1.2 文献硬约束（全部经对抗验证）

| 事实 | 数字 | 含义 |
|---|---|---|
| F1：CLAP 词汇内容键失效 | LibriSpeech R@1 ≈ 0.1% vs GLAP 93.8%（en）/ AISHELL-2 98.5%（zh） | 我们现有唯一接通的真嵌入器对主任务族（内容型）不可用；只留声音事件域 + **负对照** |
| F3：无单一模型全任务族最优 | MAEB/TS-SUPERB 明示；speaker 特化小模型以 ~25× 少参胜通用 | "单键打天下"被文献否定；"每任务一键"（7 键）又无必要 |
| F2：frozen omni 隐态可检索 | LCO-Omni 无音频对比训练登 MAEB 榜一（52.2%）；WavRAG 用 frozen Qwen2-Audio last-token | "以 frozen omni 自身嵌入作键"有外部支持但零样本强度未定（nemotron AudioCaps R@1 20.5） |
| F4：codec/离散 token 作键 = 空白+劣势 | DASB：连续表征全面胜离散（WER 差 ~2pt、EER 差 ~8pt）；无文献用 token 作检索键 | **speech codec 不进第一梯队**，最多作低优先对照（且注意 DASB 无检索类别，"检索无用"是方向性外推） |
| F7：nemotron 主键地位动摇 | 音频零样本同类最弱 + NVIDIA OneWay **Noncommercial** | 与开源立场冲突 → 降为对照候选（loader 仍按官方非对称 API 修好） |

### 1.3 推荐结构：H-a vs H-b 竞争假设，数据轨预注册裁决

- **H-a（多外部特化键）**：内容主键 ×1 + speaker 特化键（ERes2NetV2 zh）+ emotion 特化键
  （Emotion2Vec-S）——**2–3 键架构**，调研矩阵的直接指向。
- **H-b（omni 单空间多读出）**：W4 旗舰论题——frozen omni 一个嵌入空间，任务条件化读出。
  小规模先例 Multi-Axis Factor-Partitioned（P@1 65.5% vs 0.3%）；但 W4 自身证据显示 pooled
  单向量对 speaker 近 chance、emotion 需 richer readout——H-b 若成立也大概率是
  "内容/意图强、副语言弱"的**部分成立**。
- **推荐**：不预锁。数据轨检索质量测评设计成**能直接裁决 H-a vs H-b**（同数据切片、同协议、
  同 n，两假设各自最优配置对决）。这同时是 W4 论题的第一次外部可比检验——裁决无论向哪边，
  都是 on-thesis 的结果（effect-over-novelty：赢的一边直接成为 KB 默认键结构）。

### 1.4 emotion2vec / codec / CLAP / nemotron 的角色（Q1 直接答复）

**是的，emotion2vec 类特化表征应纳入**——但角色分明：

| 表征 | 角色 | 注记 |
|---|---|---|
| Emotion2Vec-S（Apache） | H-a 的 emotion 键候选 + SER 上界对照 | **zh 实证缺口大**（M3ED 仅 +1.8，survey PARTIAL #26）——zh SER 必测不可省 |
| ERes2NetV2 zh（Apache） | H-a 的 speaker 键候选 | 特化以 ~25× 少参胜通用（✅） |
| WavLM Base+/Large（MIT） | speaker/通用稳健基线 | TS-SUPERB 佐证 |
| speech codec（EnCodec 类离散 token） | **低优先对照**，非候选 | F4；若讨论决定纳入用 DASB 协议 |
| CLAP | 声音事件域 + **负对照**（协议有效性检验：好协议必须把 CLAP 判死） | F1 |
| omni-embed-nemotron-3b | 对照候选（NC license 排除默认键） | loader 修复照做（官方 encode_document/encode_query） |

### 1.5 内容主键入围（议程 #1）

三者同入数据轨对决，不预选：**GLAP**（0.9B、双语硬确证、Apache、轻）、**LCO-Omni GGUF**
（MAEB 榜一、llama.cpp 栈内、聚类几何弱）、**Qwen3-Omni 自身隐态**（最 on-thesis、文献空白 =
我们的空间、零证据；技术前提 = llama.cpp embedding 导出，P3 工程核查项）。

## 2. Q2 — 任务粒度的知识组织

### 2.1 组织基线：按 knowledge / skill / memory 三粒度，不按任务硬编码

分类学（`2026-07-06-capability-taxonomy-knowledge-skill-memory.md`）：knowledge=一般事实、
skill=任务模板、memory=具体实例回忆。**owner Q2 中的三个场景恰好落在不同粒度**——这正是
"value 只覆盖 knowledge 粒度"（A1 洞 4）要补的洞。

### 2.2 ASR 困难样本 → **memory 粒度**（实例回忆，不是 knowledge）

- **组织**：key = utterance 级声学/内容嵌入（主键空间）；**词级定位键为后备**（CLAR 式 CIF
  词边界声学键，B-WER 12.9→2.78 的 2025 先例；BR-ASR 证明 200k 规模键库可行、~20ms/查询）。
  value = (音频引用, 校正转写, 错误模式标签, 上下文域标签)，grain 标 `memory`。
- **来源池边界（信息边界红线）**：只准来自 **train/dev 划分或历史流量**，绝不含评测项
  （librispeech 960h train → dev/test 评测是天然划分；zh 侧用 aishell-1 train/dev/test，
  须先过 lock 增补裁决）。
- **部署侧"困难"判定**：只准用**可部署信号**（多采样不一致、熵、置信度），不准用 WER-vs-gold
  （golden 依赖 = 边界违规，Information-Boundary-Guard 第 1/4 问）。
- **注入必须门控**：kNN-Whisper 证明 kNN 检索 OOD 会伤害且超参敏感；**门控阈值文献无人量化**
  —— 这是我们 δ_corr/τ 邻域收敛理论的直接实验落点（理论轨 P4 的 τ*>0 定理 ↔ 数据轨 P5 的
  门控曲线测量，双向绑定的示范案例）。

### 2.3 SLU intent → utterance 级 key，value 分粒度存

key = 整段 utterance 嵌入（内容主键空间）；value 里**标签定义/任务说明（knowledge）与
历史已判实例（memory）分开存**、分别检索——混存会让检索器在"取定义"和"取相似例"之间失焦。
数据：minds14（zh loader 已有）、slurp、speech-massive。

### 2.4 SLU slot → **两级检索默认**，frame/多向量后备

- **默认（F5，当前证据下最稳）**：utterance 键检回**带槽位标注的相似整句**作 few-shot →
  span 定位交给 frozen 模型 ICL。理由：语音域不存在成熟 late-interaction/多向量检索器
  （现存子句方案用 Smith-Waterman/DTW 而非 ColBERT-MaxSim；frame 级 CLAP 只在声音事件验证过）。
- **后备实验**：frame/多向量键、H-QuEST 式 token 子句重排——列入数据轨可选清单，不进默认。
- **前置工程**：slurp/speech-massive 是仅有的 slot 金标源，**均无 loader**（P3 Sonnet 票）。
  speech-massive 注意 eval-only license 条款。

### 2.5 KB schema 演进需求（P3 工程票，本备忘录只定需求）

`key_granularity` 字段（utterance/word/segment）+ **父子多键**（segment 键带 span offset 指回
父 utterance 音频）+ value 的 `grain` 标签（knowledge/skill/memory）+ **retrieve 侧强制
verdict 门**（当前 leakage_audit.verdict 只写不查——A1 新洞 1，必须在任何新实验前修）。

## 3. 理论接口：Reachability 上限定理的设计含义

本日理论审计确认：Lean 库中关于 few-shot 的唯一实质定理（`Reachability.lean`
`too_improbable_unreachable`）证明的是**有界 prompt/few-shot 重加权无法把过低概率答案抬成
greedy 输出**——即"prompt 内重加权"这条路有机器检查的上限。设计含义：外接知识要起效，杠杆在
**(i) 改变输入携带的条件比特（真 new-info：检索到的事实/实例本身）+ (ii) 交付形式**（T10：
2-turn 工具递送使反事实采纳 0.175→0.35）+ **(iii) 门控**（何时注入）。这三个杠杆恰好都是
数据轨的测量对象（α、递送形式对比、门控曲线）。与 A2 再定级表述一致：外接优势不是已证定理，
是待测的工程-理论联合问题。

## 4. 八项议程逐条推荐 + 三项新增裁决位

| # | 议程 | 推荐 | owner 裁决位 |
|---|---|---|---|
| 1 | 内容主键选型 | GLAP + LCO-Omni + Qwen3-Omni 隐态三者同入对决 | 是否砍任一 |
| 2 | H-a vs H-b | 设计成可直接裁决的预注册对决 | 确认 |
| 3 | 特化键去留 | speaker/emotion 各设候选键入对决；zh-SER 补 esd/csemotions | 确认 |
| 4 | lock 增补 | 4 小模型（GLAP/E2V-S/ERes2NetV2/WavLM）批准走 candidates→lock | 批准与否 |
| 5 | nemotron 角色 | 降对照（NC），loader 照修 | 确认 |
| 6 | slot 方案 | 两级检索默认、frame/多向量后备 | 确认 |
| 7 | T11 骨架 | X-ARES + VocSim 协议 + kb_snapshot/kb_audit，并入数据轨覆盖矩阵 | prereg 冻结会排期 |
| 8 | GPU 共驻 | 嵌入器走 CPU（已有先例）或与 llama-server 分时 | 取舍 |
| +9 | **lock 增补范围扩至 gap 数据集** | aishell-1/cn-celeb1/esd/csemotions/voxceleb1-test（已下载已核验）入 lock；cn-celeb2/thchs-30 按需 | 批准与否 |
| +10 | **"同基座"消解方向** | 推荐：把 scale-up 路径改写为 llama.cpp/Qwen3-Omni 栈（证据所在的栈），Hydra+Qwen2-Audio 路径降级为 W2/W3 专用 | 定向 |
| +11 | **复现加固优先级** | P0=retrieve verdict 门+kb_snapshot 接入；P1=llama.cpp SHA/GGUF hash/采样参数显式化；P2=lock 元数据修复+reproduce 字段更新 | 排序确认 |

## 5. 关联文档

三锚点增量再定级：`2026-07-09-three-anchors-delta-regrade.md`；战役设计书（假设/约束台账 +
全盘存覆盖矩阵 + loop 协议）：`2026-07-09-stage1-dual-track-campaign.md`；调研主文档：
`2026-07-08-speech2vec-survey-2025plus.md`。
