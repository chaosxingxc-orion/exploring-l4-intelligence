# 2026-07-09 · Step-2a 调研：多模态知识组织/加载的学术实践（2025-01+）

> **性质**：Stage-1 调研/讨论材料（step-2 冻结会输入，**不做选型**）。owner 五问（已知组织与
> 加载方式几何？agentic 操作原语？组织方式？加载/检索方式与策略？25 年后多模态先进实践？）
> 的系统性回答。**方法**：4 维 Opus web finder + 20 条承重 claims 对抗验证
> （**16 CONFIRMED / 4 PARTIAL / 0 REFUTED**，PARTIAL 修正见 §5）。
> **产出**：81 claims + **105 个网格槽位候选**（key-org 5 / value-org 21 / retrieval-strategy 21 /
> query-construction 16 / delivery 17 / primitive 11 / out-of-mock 14）。
> 原始档（已入库）：`survey/2026-07-09-step2a-d{1..4}-*.json` + `-verifications.json`。

## 1. 四维要点（★ = 对我们最承重）

**D1 语音/多模态 RAG 系统（22 claims，33 候选）**
- ★ **Stream RAG**（2510.02044）：流式语音中途发工具查询掩蔽时延；closed→open book 11.1→26.3%
  ——但靠**后训练**教 when-to-trigger。**AudioCRAG** 基准随之而来（2706 查询语音化）——现成
  口语 RAG 测试床（en）。
- ★ **GLM-Voice E2E S2S RAG**（2505.00028）：frozen SONAR 共享空间直检（语音→文本），
  HotpotQA +20%/RGB-zh +43%——frozen 编码器共享空间 = 我们 key-org 的直接同侪。
- ★ **SpeechT-RAG**（2502.10950）：**副语言（时序/韵律）检索键**做抑郁检测，training-free
  比肩微调——非词汇键可行性的实证 + training-free 论题支持。
- LongAudio-RAG：**时间戳声学事件结构化记录**作 value（胜 vanilla RAG 与 text-to-SQL）；
  PlanRAG-Audio：检索规划（模态+时间跨度）；VoiceAgentRAG：faiss 预测性语义缓存（延迟杠杆）；
  AER：情感 exemplar 的 paraphrase 增强检索；Hearing-More-with-Less：**retrieve-then-select**
  两段式（对话史音频+转写检索）；RASST：流式术语表多尺度检索。
- Audiopedia（2412 边界）：实体链接键→KG 三元组 value 的 frozen 消费基准。

**D2 知识组织结构（23 claims，18 候选）**
- 文本域结构性胜利谱系齐整：RAPTOR 递归摘要树 / SiReRAG 双索引 / **HippoRAG-2**（开放 KG+PPR）/
  LeanRAG / NodeRAG / MS GraphRAG（社区摘要，成本 H）/ PathRAG / Zep-Graphiti 双时序 KG /
  A-MEM Zettelkasten / ReasoningBank 案例库 / UniversalRAG 模态+粒度路由 / MoG 粒度路由 /
  多模态 KG（M3KG-RAG/MegaRAG）/ 跨粒度超图。
- ★ **空白判定：没有任何结构性胜利建立在语音向量键上**——全部在文本实体/段落（或图像视频）。
  我们的 grain-tagged + 父子多粒度 schema 已覆盖低成本区；树/图结构作低成本对照臂的判断
  与 07-07 结论一致（单跳 RAG 优先、多跳 Stage-2）。

**D3 加载与检索策略（17 claims，41 候选——最大维度）**
- 查询构造 10 种（HyDE/HyPE/Adaptive-HyDE、多查询扇出、self-query 元数据滤、跨模态非对称、
  分解、latent 推理 AdaQR/LaSER…）；混合稀疏+稠密 RRF；rerank 6 种（frozen 交叉编码器、
  RankGPT 零样本 listwise 可由**基座自己**当 reranker=L 成本、setwise/groupwise、蒸馏开源、
  RL 版=对照类）；固定深度多跳 IRCoT 式；**位置效应**（lost-in-the-middle 缓解的相关性边缘
  重排 L 成本、attention-basin 对齐）；**压缩注入**（LLMLingua-2 抽取式 / RECOMP 摘要式 /
  AttentionRAG / xRAG 软压缩）；长上下文 stuffing 对照臂。
- ★ **空白判定：语音原生 rerank 不存在**——所有 reranker 打分的都是文本/转写；
  （speech-query, speech-key）对的打分器无人做。

**D4 agentic 检索原语与编排（19 claims，13 候选）**
- 原语消融证据（文本域）：**iterate 支配，route/rewrite 中性偏正，reflect/verify 在 7B 上
  贡献有限**（修正版见 §5.2——大模型上未必）；tool-registry 检索（MCP 压测到 11k 服务器）；
  novelty-gated write-back；流式并行触发。
- ★ **空白判定：全部干净消融都在文本 7B + 文本键上**——frozen 语音/omni + 语音向量键上的
  原语消融 = 无人做过 = step-2 网格的学术贡献位。

## 2. 网格槽位候选总账（105 项，mock 可用性已标注）

按 grid_slot 分布：**key-org 5**（音频原生联合键 / 副语言键 / 声纹键 / 实体链接键 / HyPE
文档侧假设提示键）· **value-org 21** · **retrieval-strategy 21** · **query-construction 16** ·
**delivery 17** · **primitive 11** · **out-of-mock 14**（RL 版查询重写/rerank/自适应停止/
门控/规划——**step-3 杠杆清单的直接输入**）。
成本分布以 L/M 为主——mock 网格的可行子集充足。全表见 survey/ 原始档（每项带 what/cost/evidence）。

## 3. 四条空白（= 我们的占位，与既有空白判定合并后全景）

1. **语音向量键上的组织结构**（D2）：结构性胜利全在文本键——我们的 speech-keyed
   grain-tagged KB 是空位。
2. **语音原生 rerank**（D3）：（语音查询,语音键）打分器不存在。
3. **frozen reader 上的 training-free RL**（D1/D4）：Stream RAG/RASST 后训 reader、
   WavRAG/SEAL/BR-ASR 训检索器、SpeechT-RAG training-free 但无 RL——**准确率杠杆的
   training-free 占位无人做**（与理论调研"无门控收敛证明"空白互相印证）。
4. **frozen 语音底座上的原语消融**（D4）：iterate/route/rewrite/reflect 的干净消融只在
   文本 7B 上——我们 step-2 网格本身即填此空白。

## 4. 对 step-2 冻结会的输入（建议，不预决）

- mock 网格的**低成本必选臂**（L 成本 × 有测量证据）：direct dense（基线）/ ASR-cascade
  检索（基线）/ retrieve-then-select 固定版 / RankGPT 式基座自 rerank（零训练）/ 相关性
  边缘重排（位置）/ flat vs 结构化 vs 工具递送 / grain-typed 递送标记 / 长上下文 stuffing
  对照 / 同意图 exemplar（AER 简化版）。
- **中成本裁决臂**：HyDE 系查询构造 / RRF 混合 / LLMLingua 压缩注入 / 固定深度 IRCoT /
  RAPTOR-lite 或 HippoRAG-lite 之一作结构对照（二选一，成本入档）。
- **out-of-mock 14 项**直接转 step-3 TFRL 杠杆候选表（与 3a 调研合并）。
- 与 2b 底账合并时的增量：key-org 增 HyPE（文档侧）与实体链接键（H 成本备选）；
  delivery 增位置重排与压缩注入两族（此前底账未列）；primitive 增 isotonic 校准置信原语
  （step-3 τ 测量的现成工具）。

## 5. PARTIAL 修正（4/20，引用须用修正版）

1. context-rot claim 拆分：18 前沿模型上下文利用不均匀成立（引 Chroma context-rot）；
   附带的外推句删除。
2. 原语消融"reflect/verify 贡献有限"**仅限 7B 模型**证据——不得外推到大模型（正中我们
   要测的空白）。
3. AttnRank 任务面：多跳 QA + few-shot，非全任务族。
4. MCP 压测规模：1→11,100 服务器（原述少一个数量级）。

## 6. 状态

Step-2a 完成。与 2b 底账合并 → step-2 冻结会材料就绪（待 Step 0 收官 + Step 1 波 1 后开会）。
**本文不做选型。**
