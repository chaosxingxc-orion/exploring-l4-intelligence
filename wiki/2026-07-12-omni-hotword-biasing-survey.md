---
title: "Omni 模型下的热词/上下文偏置：四透镜综合调研（传统技术存活裁定 + 检索式注入证据 + 本地测试床与偏置协议）"
date: 2026-07-12
stage: 1-problem-definition
status: "survey — 每条 load-bearing 主张标 VERIFIED(source)/PARTIALLY/UNVERIFIED；owner 定向：前端知识体系为研究对象，热词偏置=该问题在实体粒度的具象（Proposal-A H5 的附录 A）"
supersedes: null
feeds: ["2026-07-12-research-proposal-RDU-frontend-knowledge-v1.md 附录 A（『omni 热词/上下文偏置调研裁定』的落地）", "2026-07-12-retrieve-discover-use-analysis.md §2（『热词偏置=三段在实体粒度的实例』的证据）"]
lenses: "Lens1 传统偏置技术 × chat-API 存活性 / Lens2 prompt 偏置效应量与列表规模 / Lens3 检索式注入证据 / Lens4 基准·协议·本地测试床"
deployment: "冻结 Qwen3-Omni-30B via llama.cpp chat API（无 beam/lattice/frame-logit 访问；仅 prompt 注入 + logit_bias + GBNF grammar）+ 语音键 KB（音频/文本嵌入键·检索·prompt 递送）"
---

# Omni 模型下的热词/上下文偏置：传统技术是否失效，检索式注入是否是替代形态

> **📌 引用新鲜度合规注记（2026-07-12 追加，本调研文本不改、作有日期记录保留）**：依 Decision-Log 续17（方向影响型主张须 ≥1 篇 ≥2025-01 一手锚定；较早著作须带 [谱系]/[标准]/[已弃用] 角色标签），本调研的 direction-claims 已在 **FULL 提案**（`2026-07-12-research-proposal-omni-agentic-frontend-FULL.md` §2.1/§2.4/§4.3/§2.6）完成合规再锚，本survey**不重复改写**。已在 FULL 内落实者：
> - **替代形态（retrieve-then-inject）**：由 2025 一手 BR-ASR(2505.19179,HB-16)/RECAST(EMNLP2025,HB-23)/Hotword-RL(2512.21828,HB-15)/Locate-and-Focus(2507.18263,HB-25) 活体锚定；pre-2025 佐证 **Phoneme-RAG(2409.15353,HB-24)→[谱系]**、**M2R-Whisper(2409.11889,HB-26)→[谱系]**。
> - **解码器访问分水岭**：活体锚点 = 2025 trie(2508.17796,HB-3) + 当代 llama.cpp 工具(HB-8/10)；pre-2025 传统技术行 **shallow-fusion Zhao-IS2019(HB-1)/CLAS(1808.02480,HB-2)→[谱系]**、**TCPGen(2109.00627,HB-4)/contextual-adapters(2205.13660,HB-5)/CTC-WS(2406.07096,HB-6)→[已弃用]**。
> - **组件选型先验**：**GLAP** 已由一手 **arXiv:2506.11350（2025-06）** 锚定（多语种语音键，CLAP 词汇键 R@1≈0.1「已死」由 2025 BR-ASR co-anchor）。
> - **⚠ 待复核（survey-scoped，未在 FULL 落定）**：SLLM 列表规模研究 **arXiv:2604.12398（HB-12）** ID 形态异常需确认；**base-model reports（HB-33）** 中 Qwen2-Audio 部分 pre-2025 且 PDF 转换失败未穷尽确认——二者留作 survey 侧后续日期核验。
>
> **本文定位（owner 定向，2026-07-12）**：这是 RDU-frontend proposal（Proposal-A）挂账的**附录 A**，
> 也是 retrieve-discover-use 分析里「热词偏置=同一三段在实体粒度的实例」这句断言的证据底账。
> 任务不是论证「要不要做热词偏置」，而是裁定三件事：(a) 传统 ASR 上下文偏置技术在 **chat-API omni**
> 部署下**逐族存活性**（哪些结构性失效、哪些残存挂钩可用）；(b) **检索式 chunk 注入**是否确为替代
> 形态（owner 假设的裁定）；(c) 给出**本地测试床 + 偏置列表构造协议 + Information-Boundary 预注册要点**，
> 把 Proposal-A 的 **H5（实体粒度实例，≥15% 相对 B-WER）** 钉死。
>
> 四份透镜：Lens1（传统偏置技术 × chat-API 存活）、Lens2（prompt 偏置效应量与列表规模敏感性）、
> Lens3（检索式注入证据）、Lens4（基准·协议·本地数据拟合）。每条 load-bearing 事实标
> **VERIFIED(来源)** / **PARTIALLY** / **UNVERIFIED**。

---

## §1 owner 的问题：omni 下传统 ASR 热词技术是否失效？检索注入是否是替代形态？

**问题拆成两问：**

1. **失效问**：传统 ASR 的上下文偏置（contextual biasing / hotword）机器——shallow fusion、CLAS/深度上下文、
   trie/前缀树约束解码、TCPGen、contextual adapters、transducer/CTC beam boosting——在一个**权重与结构全冻结、
   经 llama.cpp chat-completions API 服务**的 omni 模型上，还成立吗？判据：这些技术各自需要什么**解码器内部访问**
   （训练 / beam 假设 / 逐步分数 / CTC 帧 log-prob），而 chat API **只暴露**三个控制面——(i) prompt 内容注入、
   (ii) `logit_bias`（对输入 logits 的逐 token 加性偏置）、(iii) GBNF 语法硬约束（另有可选返回的
   `logprobs`/`n_probs`，属输出侧 best-of-N/rerank，非偏置）。

2. **替代问**：如果传统机器整体失效，**检索式知识注入**（大热词库 → 按语音键检索小候选子集 → prompt/`logit_bias`/GBNF
   注入）是否就是它在 omni 下的替代形态？这正是 owner 的假设，也正是我们**语音键 KB × 检索 × 递送**三段机器在
   **实体粒度**的实例。

**一句话裁定（详见 §2/§4）**：**六大传统技术族无一原样迁移**——每一族都需要训练或解码器内部访问，chat-API 全不暴露；
**残存的只有三个退化替身**：prompt 注入（CLAS/attention-over-list 的退化后裔）、`logit_bias`（无结构的静态 shallow
fusion）、GBNF（硬约束的 trie 解码）。**检索式注入被 2024–2026 文献强证据支持为替代形态**——大列表直接塞入 prompt
在 Qwen-Audio 类模型上**灾难性崩溃**，检索到小子集再注入是「能用 vs 不能用」的分水岭。owner 假设成立。

---

## §2 传统技术在 chat-API omni 下的存活性判定表

**判定口径**：一族技术「存活」当且仅当其机制所需的解码器访问在 llama.cpp chat API 内可达。约束 = 无训练、无 beam
假设、无逐步 beam 分数、无音频编码器/CTC 帧 logit 张量。

| 传统杠杆 | 所需解码器访问 | chat-API omni 判定 | 依据 |
|---|---|---|---|
| **Shallow fusion（上下文 LM / WFST 在线重打分）** | 逐步 beam 分数 + WFST 组合进解码器；无训练 | **INAPPLICABLE**（作为集成方法）；`logit_bias` 仅是其**无结构静态回声** | HB-1 |
| **CLAS / 深度上下文** | **训练模型** + 网内 bias-encoder attention | **INAPPLICABLE**（违反「无权重/无结构」）；后裔 = prompt 注入 | HB-2 |
| **Trie / 前缀树约束解码** | beam search + 对 trie 的 next-token masking | **PARTIALLY** — GBNF 实现该 trie，但仅作**硬**约束（除非闭集选择否则杀死开放转写） | HB-3, HB-10 |
| **TCPGen（树约束指针生成器）** | **训练**；神经捷径写入输出分布 | **INAPPLICABLE** | HB-4 |
| **Contextual adapters / attention-over-list** | **训练** adapter；注入内部表示 | **INAPPLICABLE** | HB-5 |
| **Transducer/CTC beam boosting（含"免再训练"CTC-WS）** | CTC/transducer **帧 log-prob** + beam/贪心假设编辑 | **INAPPLICABLE** — chat API 不暴露帧 logits | HB-6 |
| *（替身）* prompt / 实体列表注入 | 无（文本 prompt） | **APPLICABLE** — 但随列表增大退化（lost-in-the-middle） | HB-7 |
| *（替身）* `logit_bias` 软加权 | 对输入 logits 的逐 token 偏置 | **PARTIALLY** — 静态、非序列/上下文感知、表面形式脆弱 | HB-8 |
| *（替身）* GBNF 硬约束（= 约束/trie 解码） | 逐步对 vocab masking | **PARTIALLY** — 仅闭集/格式锁用，硬约束伤开放转写 | HB-10 |

### 关键：即使「免再训练」的传统技术也失效

CTC-WS（NVIDIA NeMo, arXiv:2406.07096）是文献里最接近 training-free 的传统偏置——**无需再训练**、~13% 相对 WER 下降、
可扩到 1000 词近乎不衰减。**但它需要 CTC 帧 log-prob 张量**：被 spot 到的候选**在其帧区间替换贪心-CTC 结果**。
llama.cpp chat API 对音频编码器**不暴露任何 CTC/帧 logit**。→ **「免再训练」不等于「chat-API 可用」**：真正的分水岭
是**解码器内部访问**，不是训练与否。这是本调研最反直觉、最 load-bearing 的一条（HB-6）。

### 两个残存挂钩的可行性（llama.cpp 一手语义）

**`logit_bias`（HB-8, VERIFIED(Lens1: `tools/server/README.md` + issue #13605)）：**
- **可达**：在 **chat-completions 端点**可用；**接受字符串**——llama.cpp 把字符串 token 化，对**每个构成子 token**施加偏置
  （官方原文「just like the presence_penalty」）。`false`/`-inf` = 永不产生。
- **致命局限**：偏置是**固定、上下文无关的逐 token 加性项，在每个解码步施加**——是**子词袋（bag-of-subword）**加权，
  **非** trie/序列感知。后果：(1) **无跨 token 门控**——boost「Nvidia」的子 token 会在别处也 boost，且不让后子 token
  条件于前子 token，无法「偏好序列而不破坏开放转写」；(2) **表面形式脆弱**（issue #13605：对少数 token id 设 `-inf`，
  模型仍产出该词——同词有前导空格/大小写/复数/子词切分等多种 token 实现）；(3) **值标度**用原始加性浮点，与 OpenAI 的
  −100…+100 约定**不 1:1**，移植权重不通用。
- **裁定**：真·chat-API 可达的软加权杠杆，但是**退化、无结构的 shallow fusion**——适合 nudge/禁少数**token 化受控**的
  token；**无法忠实实现多 token 热词 boost**，激进使用会腐蚀通用转写。

**GBNF grammar（HB-10, VERIFIED(Lens1: `grammars/README.md`)）：**
- **机制**：每步推进语法 parser 状态，把**所有与语法不一致的 vocab token 的 logit 置 −∞** 再采样；输出**保证语法合法**。
  可编码**允许实体串的 trie/前缀树**——因此**能在 token 级重现经典 trie/约束解码**。
- **致命局限**：**硬约束、非软加权**。整条转写约束到实体列表 = **摧毁开放转写**（只能吐列出的串），无法「偏好但不强制」。
  混合语法（自由文本 ∪ 实体交替）可表达但脆弱：语法无法从声学表达「实体该出现在哪」，要么过度许可（无偏置效果）
  要么过度约束（强插伪实体）；GBNF **没有** WFST shallow fusion 那种置信加权偏好。
- **裁定**：适合**闭集/受迫选择**（如「答案须为这些实体之一」、格式锁），**不是**通用开放转写偏置工具；朴素语法伤开放 ASR。

**返回的 `logprobs`/`n_probs`** 额外支持对完整假设的 best-of-N / rerank（W1 机器）——那是**输出侧**杠杆，与解码器偏置正交，
属 [[2026-07-12-omni-lm-rescoring-survey]] 的地盘，本文不展开。

---

## §3 prompt 偏置的效应量与列表规模敏感性

**核心裁决（load-bearing）：prompt 内实体列表注入是唯一 chat-API 原生存活的「偏置」，但它随列表规模从"温和退化"滑向
"灾难崩溃"——崩溃点落在我们的 Qwen-Audio 模型族上。**

### 列表规模退化曲线（跨论文一致方向）

| 来源(arXiv) | 模型族 | 指标 | 小列表 | 大列表 | 退化行为 | 依据 |
|---|---|---|---|---|---|---|
| 2411.06437 | Vicuna-7B+WavLM | B-WER(clean) | 3.67 @100 | 4.41 @2000 | 温和单调（CTC 预筛，列表被 keep 短） | HB-11 |
| 2604.12398 | Speech-LLM | B-WER | 3.2–4.2 @10 | 4.4–5.8 @200 | ~20–30% 相对上升；干扰词混淆 | HB-12 |
| 2502.11572 | Whisper(FT) | R-WER | best @~70 | worse @150 | 224-token≈70 词上限后退化 | HB-13 |
| 2310.09424 | SALM | precision | 高 @少 | 降 @多 | recall 平、precision 落（过偏置） | HB-14 |
| 2512.21828 | Qwen2.5-7B | KER | 11.99 @top-2 | 15.21 @top-10 | 非单调；最优 ~top-2 | HB-15 |
| **2505.19179** | **Prompt-QwenAudio** | — | 小列表可用 | **N≥100 灾难幻觉** | **无检索则崩溃** | **HB-16** |
| 2601.15397 | Phi-4-mini-mm | EWER | 可用 | **"list-vomiting"/无视音频** | prompting 失败；logit-space 鲁棒 | HB-17 |

**读数：**
- **朴素「整表塞入」在 Qwen-Audio 类 instruction-following 音频-LLM 上灾难崩溃**：BR-ASR 明记
  *"catastrophic hallucination in Prompt-QwenAudio above N≥100 without retrieval filtering"*、*"SLAM-ASR baseline
  without retrieval fails catastrophically at N≥500"*（HB-16, VERIFIED(Lens2/3: 2505.19179)）。LOGIC 命名此失效为
  **"list-vomiting"**（模型背诵列表而非转写，如输出 *"Aaron, Aarthy, Alex…"*），并指出*"列表长时模型可能完全无视声学输入"*
  （HB-17, PARTIALLY(Lens2: 2601.15397 全文抓取失败，abstract/图级验证)）。**这直接落在我们的部署模型族。**
- **有 CTC/检索预筛把列表 keep 短时，退化是温和的**：2411.06437 从 B-WER 3.67@N100 到 4.41@N2000（~20% 相对上升，
  no-bias 基线 10.02），单调但缓——**因为 CTC 预筛保持有效列表短**（HB-11）。这正是「检索是解药」的反面印证。
- **效应集中在实体/稀词 token，不在整体 WER**：几乎所有结果里 B-WER/NE-WER 大幅相对改善而整体 WER/U-WER 几乎不动
  （实体词是小 token 比例）。**报 B-WER，不是 WER**，否则效应被稀释掩盖。
- **prompt 偏置在"被训练去跟随它"的模型上最好用**：SALM 无 "Speech ICT" 训练**无法跟随**关键词 prompt（HB-14）；
  Qwen3-ASR 的 SFT **显式含 "context biasing data"**（HB-18）。冻结、未被偏置训练的模型可能有**"上下文利用差"**——
  ProfASR-Bench 显示即使 oracle prompt 也只把 Whisper-Small WER 挪 −0.06pp（HB-19）。**反向权衡**：作为
  instruction-following omni，Qwen2.5/3-Omni **确实**借世界知识利用上下文（ContextASR-Bench：Qwen2.5-Omni 相对
  Whisper-large-v3 −39.9% WER / −42% NE-FNR，HB-20，secondary）——它坐落在 Whisper（弱）与专训 SLLM（强）之间。

**失效模式清单（供 over-optimization / KL-trust-region 约束框架）：**
list-vomiting/无视音频（HB-16/17）· 实体幻觉/过偏置（precision 随 recall 落，HB-14）· GER 过纠正（HB-C，见 rescoring 调研）·
同音/近音混淆（HB-21, BR-ASR DCL；ProfASR *hydralazine→hydroxyzine*）· 上下文利用差（HB-19）· 真词不在列表则增益归零
（HB-22, 2309.00723：1.1–2.7% 相对）。

---

## §4 检索式注入的证据与 owner 假设的裁定

**裁定：owner 假设（检索式 chunk 注入 = 传统热词在 omni 下的替代形态）被多论文一手证据 STRONGLY SUPPORTED。**

2024–2026 全领域已收敛到 owner 的论点：大偏置库须**先检索小相关子集再注入**——因为整表塞 prompt 会灾难性劣化 speech-LLM
（幻觉 + 上下文溢出 + 干扰噪声），而检索保持平坦。这在与我们**同族**的基座（Qwen-Audio / Qwen2-Audio / Phi-4 speech-LLM）
上被**五篇独立论文**证明。

### 「检索 vs 塞入」在大列表下的对决（最 load-bearing）

| 论文 | 基座 | 大规模整表塞入 | 检索（小 top-k） | 塞入崩溃点 | 依据 |
|---|---|---|---|---|---|
| **BR-ASR**(IS2025) | Qwen-Audio | N=500 B-WER 32.1/39.1；**N≥1000 完全失败** | N=2000 **B-WER 2.8/7.1** | N≥100 幻觉 | HB-16 |
| **RECAST**(EMNLP2025) | GPT-4o-mini/Phi-4 | GPT-4o-mini 全词 **WER 82.5**；Phi-4 K=50 幻觉 WER 38.9 | Whisper K=50 **WER 11.5 / E-WER 17.2** | Phi-4 K=10→50 退化 | HB-23 |
| **Phoneme-RAG**(Apple24) | Mistral-7B+Conformer | "设计上避免塞全库" | k≤10 **WER −30.2%, NER −73.6% 相对** | k=20 已劣于 k=10 | HB-24 |
| **Hotword-RL**(2512, 25) | Qwen2.5-7B | top-10 KER 15.21 | top-2 KER **11.99**（+RL→8.29） | 更多候选单调更差 | HB-15 |
| **Locate-and-Focus**(ACL25) | **Qwen2-Audio** | 全高频词注入 TSR 28.20% | 检索 **TSR 65.53%** | 全注入淹没信号 | HB-25 |

**在与 Qwen3-Omni 同精神的 Qwen 族 speech-LLM 上，把 500–2000 词热词表塞进 prompt 不是"帮助减弱"，而是"摧毁"转写
（WER 20–80%）。检索 ~top-2 到 top-50 子集是能用与不能用之别。** 这是 owner 断言的最强形式。

### 检索键模态谱（按对我们语音键 KB 的拟合排序）

1. **音频键 / 跨模态（最佳拟合，最佳结果）**：BR-ASR AcousticBias（热词→TTS→用 SpeechLLM 自身语音编码器）、VQ-RAG、
   GLCLAP、M2R-Whisper、Locate-and-Focus、RECAST 解码器态。避开「转写-bootstrap 失效」。**我们的语音键 KB 正是此类。**
2. **偏置词的文本/LLM 嵌入键（BR-ASR TextualBias，实为 BR-ASR 的赢家）**：更 OOV-鲁棒、更少同音命中（−0.3% abs B-WER，
   RecallH −10%）。→ 建议 KB **同时持音频键与文本键**，末段匹配偏好文本侧重编码。
3. **语音学键（Phoneme-RAG）**：英文人名强，但 Soundex/Metaphone **不迁移到中文**（RECAST 的 Hindi 论证）。中文用**学习的
   跨模态检索器**，非语音学算法。

### 两条对我们最要命的约束

- **检索器几乎都是"专门训练"的**：BR-ASR redesigned CLAP 命中 93/91%、GLCLAP 89/74%，但**都是 purpose-trained** 对比检索器。
  与我们已记录事实一致——**off-the-shelf CLAP 词汇键已死（R@1≈0.1）**。**唯一完全 training-free 的类比是 M2R-Whisper**
  （冻结 Whisper，AISHELL-1 CER 5.76→4.11，−30.7%），但其 token 级 kNN 段**需要 logit 访问**（chat API 无），
  **只有句级 ICL 半段是 prompt 兼容**。→ **「冻结 omni 嵌入作为足够检索键」是激进赌注，须作为显式假设去测量**，或预算一个薄检索
  投影训练步（HB-26）。
- **同音/近音干扰污染 = 音频相似检索的 #1 已证失效**：BR-ASR 整个 DCL 机制、RECAST 硬负挖掘、整条语音学检索线都为它而生
  （HB-21）。任何 retrieve-then-bias selector 的收敛论证须含**显式 precision/去相关项**界定同音误注入率（BR-ASR RecallH 的
  类比）——这正是理论轨要求的「界定问题边缘的显式约束」。

**注入形式——我们覆盖良好且有白空间**：所有论文最主流、最佳的注入形式是**把检索到的 top-k 列进转写指令 prompt**——与
llama.cpp chat API 1:1。`logit_bias`（boost 检索子 token）与 GBNF（硬约束到检索实体集）是**更强杠杆，但被调研的
ASR-偏置论文全都没用于此**——是 W1 的真·白空间/新颖机会，但带已知危险（RECAST/BR-ASR 已记的幻觉插入/同音混淆）。
**安全框架 = 语法约束到"检索并验证过"的小子集（非全 200k）。**

---

## §5 本地测试床推荐（2-3 集 + 偏置列表构造协议 + Information-Boundary 预注册要点）

### 指标约定（先钉死）

B-WER / U-WER（Le et al. IS2021, arXiv:2104.02194；中文对应 B-CER / U-CER）：U-WER=偏置列表**外**词的 WER，
B-WER=列表**内**词的 WER；插入错误若插入词在列表则归 B-WER，否则归 U-WER。**主效应量 = 相对 B-WER 下降**
`(B-WER_nobias − B-WER_bias)/B-WER_nobias`——整体 WER 因偏置词占比小而几乎不动，效应集中在 B-WER。（HB-27）

### 推荐 top-3 本地测试床（全部盘上已有音频）

1. **LibriSpeech + fbai `is21_deep_bias`（英文，oracle-list 正典）**。#1 因为整套 Le et al. 协议——稀词定义
   （音频训练集 top-5k 之外，~209.2K 稀词型为干扰池）、逐 utt 列表、N∈{100,500,1000,2000} 干扰集、B-WER/U-WER 打分——
   是**可下载、按 utt-id 对齐**我们已有音频的**成品工件**。给出与文献 apples-to-apples 的退化曲线，演练
   **prompt 注入 + `logit_bias`** 在开放 ASR 上。*须核 test-other 是否在盘（taxonomy 仅列 test.clean）。*（HB-28）
2. **AISHELL-1 + AISHELL-NER 标签（中文，oracle-list 正典，近零获取成本）**。音频已在盘；仅需开源 AISHELL-NER 标注。
   解锁既定 **891-实体 / B-CER** 中文协议与中文退化曲线——鉴于部署的 zh 重心 + Qwen3-Omni 中文强，**必备**。（HB-29）
3. **SLURP（英文 SLU，检索原生 + 可语法约束）**。最贴**我们的**机器：(a) slot 值即实体，每 utt 天然有一个（实体密度最高）；
   (b) 逐域 slot 库是**天然的非-oracle KB**——检索步（音频键→候选 slot 值）是**被测对象**而非手递 oracle 列表；
   (c) **三个 llama.cpp 杠杆全适用**——prompt 注入检索候选、`logit_bias` 于 slot 值 token、**GBNF** 约束 slot 值 span 到
   检索闭集；(d) SLU-F1 给干净的已发布实体指标。（HB-30）

*（可选第 4，方言轴）*：`voicebench-sd-qa`（SD-QA）作口音分层实体识别——复用盘上数据、自构实体列表，测偏置增益是否耐口音漂移。

### 偏置列表构造协议（Le et al. 惯例 → 我们的检索化改造）

- **oracle-list 惯例（可复现 baseline）**：逐 utt 列表 = {该 utt reference 中的稀词/实体} ∪ {N 个从固定池采样的**干扰词**}；
  N ∈ {100,500,1000,2000} 扫描；B-WER 仅在偏置词上打分；**半 utt 含真词、半不含**（Hotword-RL 惯例）以测假激活。
- **诚实的、项目对齐的协议 = 用检索步替换 oracle 列表**：大实体 KB → **音频键检索 → top-k 候选 → prompt/`logit_bias`/GBNF**。
  于是「列表规模 N」轴变为**检索干扰负载 / precision@k** 轴，§3 的退化曲线变为**检索质量曲线**。这令冻结模型 + KB 检索
  是被测对象，并**结构性阻止把 golden target 喂给模型**。

### Information-Boundary 预注册要点（[[Information-Boundary-Guard]] 实例化）

- **真词+干扰词惯例是合法的**（真词=部署可得的「上下文」，如联系人表），**当且仅当**：(a) 干扰词从固定池按**预注册 seed +
  列表规模**采样（模型不能靠盲抄列表取胜）；(b) **U-WER/插入与 B-WER 并列报告**（盲抄被当插入错误惩罚）。
- **列表长度扫描预注册**：N（或 top-k）网格、真词占比、干扰词来源，全部 prereg；不得中途改。
- **禁止退化为给答案**：**永不**把完整 reference 转写放进列表——只放抽取的稀词/实体 + 干扰词。eval 时**不得**把该 utt 的
  golden 实体作为「保证命中」注入（Phoneme-RAG 训练时故意保证命中，那是训练侧；**eval 侧只能作为众多干扰词之一**）。
  oracle-retrieval / gold-transcript 臂**永久标注不可部署、只作上界**。（回应 memory「信息边界过界=假增益」的失败模式。）

**须获取（按优先级）**：① `facebookresearch/fbai-speech/is21_deep_bias` 偏置列表（微小文本；解锁英文正典复现，**HIGH**；
GitHub 当前被本环境 fetch 拦，走 WSL `git clone`/mirror）；② AISHELL-NER 标注（`Alibaba-NLP/AISHELL-NER`，音频已在盘，
**HIGH**）；③ LibriSpeech test-other 切分（若不在盘，**MEDIUM**）；④ ConEC（LREC2024，Earnings-21 ~39h 的**真实**非-oracle
上下文；**MEDIUM-LOW**）。

---

## §6 与现有 Phase-A 机器的映射（新臂族草案 + 与 Proposal-A 的关系）

**核心映射**：语音键 KB × 检索 × 递送 → **热词/实体库 × 检索选择 × 注入形式**——这是 Proposal-A 三段
（检索键模态 × 发现触发 × 使用递送）在**实体粒度**的直接实例，即 **H5**。

| Proposal-A 三段 | 通用（知识依赖任务） | **本臂族（实体粒度实例，H5）** | 部署杠杆 |
|---|---|---|---|
| **检索 Retrieve**（键模态） | audio-direct vs own-ASR 级联；证据语料 KB | 音频键检索热词/实体库；value = 实体串（+ 音频键 & 文本键双持） | FAISS 检索（同 Phase-A） |
| **发现 Discover**（触发/候选内筛选） | 恒检索 / 不确定度触发 / 不检索 | **检测句中稀词/实体倾向 → 触发实体检索**；top-k 门（top-2 甜点，HB-15） | logprob/熵触发器（CPU） |
| **使用 Use**（递送形式） | flat / 结构化 card / 2-turn | **prompt 列出 top-k** / **`logit_bias` 于实体子 token** / **GBNF 约束到检索闭集** | 三杠杆全适用（SLURP 上） |

**新臂族草案（并入 Phase-A / 服务 H5）——注入形式维新增两个部署可达杠杆**：

- **A-inj-prompt**：检索 top-k 实体列进转写指令（文献主流，chat-API 原生）——已被 Phase-A「递送」维覆盖。
- **A-inj-logitbias（新）**：对检索实体的子 token 施 `logit_bias`——**无调研的 ASR-偏置论文用过**，白空间；带 §2 局限
  （静态、表面形式脆弱），需 token 化受控 + 小子集。
- **A-inj-gbnf（新）**：GBNF 约束 slot/实体 span 到**检索并验证过的**闭集——仅 SLURP 类**闭集/受迫选择**任务安全，开放 ASR 禁用。
- **A-trigger（发现段）**：实体倾向触发 vs 恒检索 vs 不检索三臂——填 Proposal-A「发现段证据最薄」的洞（RDU §1）。
- **对照臂**：no-bias / random-list（阴性，须反伤）/ full-list-stuffing（复现 §3 崩溃）/ oracle-list（上界，标不可部署）/
  own-ASR→文本级联（检索键模态对照）。

**与 Proposal-A 的关系（精确）**：本调研 = **Proposal-A 的附录 A**（proposal §3 H5、§4.1 实体测试床、§附录 A 槽位）。
它**不新开研究方向**——是同一「检索-发现-使用」三段在实体粒度的可证伪实例：
- **H5 预注册阈值 = ≥15% 相对 B-WER**（proposal §3）；kill criterion #4：若三段管线不显著优于全列表塞入 → 检索式注入假设
  在实体粒度**证伪，如实报告**（proposal §8）。
- 臂族并入 Phase-A **须待「测试床与效应量确认」**（RDU §3 条件）——本调研即提供该确认：测试床 = §5 top-3，效应量先验 = §7。
- **注入形式两个新杠杆（logit_bias/GBNF）是本调研为 Phase-A 贡献的净增**——原 Phase-A「递送」维只有 flat/card/2-turn/
  system-prompt/rerank/压缩，无 logit/grammar 级；owner 定向「前端校正」正落在此。

---

## §7 效应量预期 vs owner 的 10% 相对门槛

**owner 门槛**：H4 primary = **≥10% 相对**（知识依赖任务，组合臂 vs no-retrieval）；**H5 实体实例 = ≥15% 相对 B-WER**
（更严的靶）。

**field 中 B-WER 相对增益范围（分「达标机制」）**：

| 机制类别 | field 相对 B-WER 增益范围 | chat-API omni 可部署？ | 相对 10%/15% 门槛 |
|---|---|---|---|
| **oracle-list + 训练/beam**（trie-DB+SF、TCPGen、CLAS、zero-shot trie 解码、DVPA） | **~40–72% 相对**（HB-1/3/4；DVPA 54–72%；LibriSpeech 48–60%；TCPGen 40–42%；trie-decode 42–44%） | **否**（须训练/beam/帧 logit） | 舒适超过——但**非可部署形态** |
| **检索-喂-短列表 prompt 注入**（BR-ASR、RECAST、Phoneme-RAG、Locate-and-Focus） | **宽带、大多 30–60% 相对**（BR-ASR Qwen-Audio no-bias→bias B-WER 8.4→2.8=67%，但含其**专训**检索器；RECAST E-WER −54%；Phoneme-RAG NER −73.6%） | **部分**（prompt 注入原生可达；但赢家检索器多为专训） | **可望超过 15%**——若检索器足够（§4 约束） |
| **logit-space 偏置**（= 最贴 `logit_bias` 的机制，LOGIC） | **~9% 相对 EWER**（11 locale 均值；zh-CN 28.51→25.88；aggressive 17%） | **是**（logit-space 是 chat-API 可达形态的最近类比） | **恰在/略低于 10% 门槛——警报** |
| **纯 prompt 整表塞入**（无检索） | **负**（灾难崩溃，WER 20–80%） | 是（但崩溃） | 远低于门槛 |

**裁定（对 owner 门槛的诚实预期）：**
- **oracle-list 的 30–60% 相对是不可部署形态**——不能据以承诺我们的可部署系统达标。
- **≥10%（H4）在可部署形态上可达但不保证**；**≥15%（H5，实体粒度）是更硬的靶**。诚实预期：**检索-喂-短列表 prompt 注入
  在良好收窄的实体测试床上有望清过 15% 相对 B-WER**（BR-ASR/RECAST 量级支持），**但两条风险**：(1) **检索器质量**——
  off-the-shelf 键失效（CLAP R@1≈0.1），若不训薄投影则增益打折（HB-26）；(2) **纯 `logit_bias` 类比只兑现 ~9%
  （LOGIC）——最贴 llama.cpp 原生杠杆的机制恰在门槛线下**，警示单靠 logit_bias 可能不达 15%，须靠 prompt 短列表 +
  （闭集处）GBNF 组合。
- **达标路径**：检索把有效列表 keep 短（§3 温和退化区）+ 递送用 prompt 短列表为主、logit_bias 为辅、闭集处 GBNF——
  避开 §3 的崩溃区与 §4 的同音污染。**若最优组合在 ≥2 集上 <10%（H4）或 <15%（H5）→ 触发 kill criterion，如实报负结果。**

---

## §8 Claim ledger（逐条状态）

| # | Claim | 状态 / 来源 |
|---|---|---|
| HB-1 | shallow fusion（上下文 LM/WFST 在线重打分）需逐步 beam 分数 + WFST 组合；chat-API 无，`logit_bias` 仅无结构静态回声 | **VERIFIED**(Lens1: Zhao IS2019 + 2104.02194 框架) |
| HB-2 | CLAS/深度上下文需训练（bias-encoder attention 在网内），up to ~68% 相对 WER 改善，随干扰短语增多退化（Fig4） | **VERIFIED**(Lens1: arXiv:1808.02480, SLT2018)；per-set 数(Songs18.7→6.9 等)为 ar5iv 渲染 **PARTIALLY** |
| HB-3 | trie/前缀树约束解码需 beam+next-token masking；zero-shot trie 解码 42/43% B-WER 下降、U-WER 不变，但需 beam=10 | **VERIFIED**(Lens1: arXiv:2508.17796) |
| HB-4 | TCPGen 需端到端训练（神经指针捷径入输出分布）；R-WER 42.2%(AED)/39.6%(RNN-T) 相对下降，列表 1000+5000 干扰 | **VERIFIED**(Lens1: arXiv:2109.00627, ASRU2021) |
| HB-5 | contextual adapters 需训练 adapter（cross-attention 注入内部表示）；NE +31.29% WERR，通用集 −3~−4% | **VERIFIED**(Lens1: arXiv:2205.13660, ICASSP2022) |
| HB-6 | CTC-WS 免再训练**但需 CTC 帧 log-prob**（帧区间替换）；~13% 相对 WER 下降、扩到 1000 词近平；chat-API 无帧 logit → INAPPLICABLE | **VERIFIED**(Lens1: arXiv:2406.07096, IS2024) |
| HB-7 | prompt/in-context 实体列表注入 = CLAS 的 chat-API 后裔，APPLICABLE 但随列表增大退化（上下文窗/延迟/lost-in-the-middle） | **VERIFIED**(Lens1/2: arXiv:2601.15397) |
| HB-8 | llama.cpp `logit_bias`：chat 端点可用、接受字符串（偏置每子 token）；但静态逐 token、无序列结构、表面形式脆弱（#13605）；值标度非 OpenAI 1:1 | **VERIFIED**(Lens1: `tools/server/README.md` + issue #13605/#3149) |
| HB-10 | GBNF 把不合语法 token logit 置 −∞；可编码实体 trie=约束解码，但硬约束、伤开放转写，无置信加权偏好；宜闭集/格式锁 | **VERIFIED**(Lens1: `grammars/README.md`) |
| HB-11 | CTC-Assisted LLM-ASR：B-WER 3.67@N100→4.41@N2000（温和单调，CTC 预筛），no-bias 10.02 | **VERIFIED**(Lens2: arXiv:2411.06437) |
| HB-12 | SLLM：B-WER 3.2–4.2@10词→4.4–5.8@200词，非上下文基线 20.5；干扰词随数增混淆 | **VERIFIED**(Lens2: arXiv:2604.12398) |
| HB-13 | Whisper 原生 prompt 224-token≈70 词上限；R-WER 随 N 过 ~70 退化；强 R-WER 数来自 fine-tune 非 zero-shot | **VERIFIED**(Lens2: arXiv:2502.11572) |
| HB-14 | SALM 需 Speech-ICT 训练才跟随关键词 prompt；过偏置 precision 0.94→0.66–0.74 落而 recall 升 | **VERIFIED**(Lens2: arXiv:2310.09424, ICASSP2024) |
| HB-15 | Hotword-RL：GLCLAP 检索 top-2 最优（Media KER 11.99），top-5/10 退化；+GRPO **训练 LoRA**（非 training-free）→8.29 | **VERIFIED**(Lens2/3: arXiv:2512.21828) |
| HB-16 | BR-ASR：Prompt-QwenAudio N≥100 灾难幻觉、N≥500/1000 完全失败；检索后 2k→200k(100×) 仅 +2.9pts abs B-WER；B-WER 2.8/7.1@2000 | **VERIFIED**(Lens2/3: arXiv:2505.19179, IS2025, 全文读) |
| HB-17 | LOGIC：prompting 三失效（上下文窗/lost-in-middle/"list-vomiting"）；logit-space 前缀树 ~9% 相对 EWER 均值(11 locale)、zh-CN 28.51→25.88、+2.8% RTF、列表规模常数时间 | **PARTIALLY**(Lens2: arXiv:2601.15397，全文抓取失败，abstract/搜索级) |
| HB-18 | Qwen3-ASR（从 Qwen3-Omni 后训）SFT 含 "context biasing data"、学用 system-prompt 上下文 token；无 with/without 效应数 | **VERIFIED**(Lens2: arXiv:2601.21337) |
| HB-19 | ProfASR-Bench「上下文利用差」：oracle prompt 仅挪 Whisper-Small WER −0.06pp（Qwen2.5-Omni-3B + Whisper 测） | **VERIFIED**(Lens2: arXiv:2512.23686)；post-cutoff |
| HB-20 | ContextASR-Bench：omni LALM 借世界知识利用上下文；Qwen2.5-Omni −39.9% WER / −42% NE-FNR vs Whisper-large-v3 | **PARTIALLY**(Lens2: arXiv:2507.05727，secondary summary，within-model delta UNVERIFIED) |
| HB-21 | 同音/近音干扰污染 = 音频相似检索 #1 失效（BR-ASR DCL 全机制；RECAST 硬负挖掘；ProfASR hydralazine→hydroxyzine） | **VERIFIED**(Lens3: 2505.19179 + 2512.23686) |
| HB-22 | 真词不在列表则增益归零（LLM-GER 实体偏置 1.1–2.7% 相对） | **VERIFIED**(Lens2: arXiv:2309.00723, ICASSP2024) |
| HB-23 | RECAST：冻结 ASR 解码器态检索；LOCATION E-WER 37.7→17.2(−54.3%)；GPT-4o-mini 全词 WER 82.5、Phi-4 K=50 幻觉；Hindi 有效（语音学算法失效处）；注入=prompt | **VERIFIED**(Lens3: EMNLP2025 findings.203, 全文读) |
| HB-24 | Phoneme-RAG：语音学检索 k≤10；WER 6.36→4.44(−30.2%)、NE-error 37.52→9.90(−73.6%)；k=20 劣于 k=10 | **VERIFIED**(Lens3: arXiv:2409.15353, Apple) |
| HB-25 | Locate-and-Focus（Qwen2-Audio）：检索 TSR 24.12→65.53% vs 全注入 28.20%；BLEU 35.82→49.30 | **VERIFIED**(Lens3: arXiv:2507.18263, ACL2025) |
| HB-26 | 赢家检索器几乎都 purpose-trained（BR-ASR CLAP 93/91、GLCLAP 89/74）；off-the-shelf CLAP 词汇键死(R@1≈0.1)；唯一全 training-free 类比 M2R-Whisper 的 token-kNN 需 logit 访问（chat-API 无），仅句级 ICL 可用 | **VERIFIED**(Lens3: 2505.19179+2409.11889 + memory speech2vec) |
| HB-27 | B-WER/U-WER 指标约定（Le et al.）；中文 B-CER/U-CER；主效应量=相对 B-WER 下降 | **VERIFIED**(Lens4: arXiv:2104.02194, IS2021) |
| HB-28 | LibriSpeech Le 协议：稀词=top-5k 外(~209.2K)、逐 utt 列表 ∪ N∈{100,500,1000,2000} 干扰；test-clean B-WER 14.1→5.7@100(−59.6%)→7.3@2000(−48.2%)；fbai is21_deep_bias 供成品列表 | **VERIFIED**(Lens4: arXiv:2104.02194) |
| HB-29 | AISHELL-NER：AISHELL-1 test 3393 NE→891-实体偏置列表、B-CER；音频已在盘，仅需 NER 标签 | **VERIFIED**(Lens4: AISHELL-NER ICASSP2022) |
| HB-30 | SLURP：slot 值=实体、SLU-F1、每 utt 天然有实体；三 llama.cpp 杠杆全适用（prompt/logit_bias/GBNF） | **VERIFIED**(Lens4: arXiv:2011.13205, EMNLP2020) |
| HB-31 | DVPA：LibriSpeech B-WER 9.59@N100(−72%)→15.74@N500(−54%)；WenetSpeech 298-NE B-CER −75.69% 相对 | **VERIFIED**(Lens4: arXiv:2505.23077)；N=1000 cell **UNVERIFIED** |
| HB-32 | ConEC(LREC2024)：Earnings-21 44 calls 真实上下文（slides/新闻/名单）；真上下文比 oracle 列表更嘈杂——artificial 协议高估可达增益 | **VERIFIED**(Lens4: 2024.lrec-main.328)；列表规模/WER cell **UNVERIFIED**(PDF 不可解析) |
| HB-33 | 基座 Qwen2-Audio/2.5-Omni/3-Omni 技术报告无专门 hotword/biasing feature 文档 | **PARTIALLY**(Lens2: 报告 PDF 转换失败，无 feature 浮现但未穷尽确认) |

**未验证 / 缺口（诚实标注）**：LOGIC 全文（9% EWER/11 locale abstract 级，HB-17）；ContextASR-Bench within-model delta（HB-20）；
DVPA N=1000 cell、ConEC 列表规模与 baseline WER cell、Earnings-21 per-NER-category 数（HB-31/32）；基座报告 biasing-feature
缺席（HB-33）；「vanilla Whisper `initial_prompt` 列表规模曲线」——领域已弃（原生 prompt 弱，无强数存在）；
「冻结 omni 嵌入作足够检索键」为**显式假设待测**（HB-26），非已证。

---

### 一句话结论

传统 ASR 热词技术在 chat-API omni 下**六族无一原样存活**——判分水岭是**解码器内部访问**（训练/beam/帧 logit），
连"免再训练"的 CTC-WS 也因需帧 logit 而失效；**残存的只有 prompt 注入（退化 CLAS）、`logit_bias`（无结构静态 shallow
fusion）、GBNF（硬约束 trie 解码）**。**owner 的检索式注入假设被强证据支持为替代形态**——整表塞 prompt 在 Qwen-Audio 族
N≥100 灾难崩溃，检索到小子集（top-2 甜点）再注入是能用之别；**注入形式的 `logit_bias`/GBNF 两杠杆是无 ASR-偏置论文用过的
白空间**，但纯 logit_bias 类比（LOGIC）只兑现 ~9% 相对、恰在 owner 10% 门槛线下，H5 的 15% 靶须靠**检索短列表 prompt +
闭集 GBNF** 组合达成。本地测试床 = **LibriSpeech+is21_deep_bias / AISHELL-1+AISHELL-NER / SLURP**，用**检索步替换 oracle 列表**
即结构性满足 Information-Boundary，把 Proposal-A 的 H5 钉死。
