---
artifact_id: "SF-STAGE1C-D2-XIAORAG-DOI10.1109-ICASSP49660.2025.10890057"
arxiv_id: "none (DOI 10.1109/ICASSP49660.2025.10890057；出版方 OA PDF)"
title: "Contextual ASR with Retrieval Augmented Large Language Model"
authors: "Cihan Xiao†* (Center for Language and Speech Processing, Johns Hopkins University, USA), Zejiang Hou‡, Daniel Garcia-Romero‡, Kyu J Han‡ (AWS AI Labs, USA)；首页脚注逐字：\"Work done during internship at AWS AI Labs.\"（* 号所指=第一作者）。**署名口径注**：PDF 排版写 \"Kyu J Han\"（无缩写点），任务下达写 \"Kyu J. Han\"——以排版为准照录"
venue: "ICASSP 2025（DOI 10.1109/ICASSP49660.2025.10890057）。**证据等级声明**：本地 PDF 为**出版方 OA 副本**（amazon.science CDN），`pdfTeX-1.40.26` / `/CreationDate D:20250206`（camera-ready 时点，与 ICASSP 2025 档期自洽），**页面上无 IEEE 页眉、无 venue 行、无 DOI 行**——venue/DOI 归属为**外部元数据（ledger 行 + 任务下达），本件未在 PDF 内部取得任何 venue 自证**；有网络时须以 IEEE Xplore 记录二次核对"
date: "2026-08-01"
read_level: "D2_DEEP_READ"
reader: "opus-agent"
status: "DRAFT_FOR_R2_INTEGRATION"
source_of_record: "**官方 OA PDF 唯一源，5 页**（`pdfinfo` 计数；正文 5 节 + 24 条参考文献；Fig.1 一幅；TABLE I/II/III 三表）。**证据等级须降一档**：本篇无 arXiv 版故**无 eprint LaTeX 源**，数字取自 `pdftotext -layout` 抽取 + **`pdftoppm` 200dpi 逐页图像目视核对**双通道。TABLE I 在 `pdftotext` 输出中列间空白严重坍缩（14 行数据错位为不可读序），**本件全部 Table I 数字以第 3 页渲染图像目视逐格读取为准，不采信文本抽取**；Table II/III 同法以第 4 页图像核对"
local_evidence:
  - "E:/chao_workspace/exploring-l4-intelligence/speechrl-data/survey-fulltext/icassp2025-xiao-rag/icassp2025-xiao-rag.pdf sha256 8516cfe66d007152a12fdb52cd0ed504fd36ca6576bb7b8853f0e6d727b1e2fa，674470 bytes，5 页（与 ledger 第 1357 行逐字节一致，本次 `sha256sum` 复算通过）"
ledger_ref: "wiki/survey/2026-07-17-sf-fulltext-ledger.jsonl **第 1357 行**（kind=pdf，无 eprint 行；access_class=`PUBLISHER_OA_DEREFERENCE/FULLTEXT_FETCH (NOT_ON_ARXIV four-way negative)`）"
prior_status: "**重扫描轨道发现**：本篇是 ConEC 载体的**第二评测者**（循 ConEC 官方 E-22 训练 / E-21 测试协议、直接消费 ConEC 逐场 context files），此前**从未进入 R2 读集**——既不在 §8 近邻十五件矩阵内，亦未被外审 round-16 具名列出。本件为首次 D2 全文深读"
exposure: "零网络请求（本会话未发起任何 fetch/search/WebFetch/WebSearch/API 调用）；只读本地件——本篇 PDF、ledger、R2 提案 draft 与签字表（只读未改）、既有 D2/D1 条目（ConEC 2024.lrec-main.328、Zhang BigData 2023、MementoGUI 2605.18652）；sha256 本次复算；PDF 文本抽取与页面渲染产物只写入会话 scratchpad，未写入仓库；零模型调用、零指标运行、零数据集下载、零 GPU；本件为唯一新建文件"
supersedes: "无（新建）"
---

# D2 深读：Contextual ASR with Retrieval Augmented LLM (Xiao et al., ICASSP 2025)

## 1. 来源核对

**ledger 逐行引用**（`wiki/survey/2026-07-17-sf-fulltext-ledger.jsonl` 第 1357 行）：

> `{"arxiv_id": "doi:10.1109/ICASSP49660.2025.10890057", "kind": "pdf", "url": "https://cdn.amazon.science/46/c8/8198e3674a4588fbb76fe1be7c15/contextual-asr-with-retrieval-augmented-large-language-model.pdf", "time_utc": "2026-08-01T15:30:48Z", "http_status": 200, "attempts": 1, "bytes": 674470, "sha256": "8516cfe66d007152a12fdb52cd0ed504fd36ca6576bb7b8853f0e6d727b1e2fa", "error": null, "stored_at": "E:/chao_workspace/exploring-l4-intelligence/speechrl-data/survey-fulltext/icassp2025-xiao-rag/icassp2025-xiao-rag.pdf", "access_class": "PUBLISHER_OA_DEREFERENCE/FULLTEXT_FETCH (NOT_ON_ARXIV four-way negative)"}`

本次复算 `sha256sum` 得 `8516cfe66d007152a12fdb52cd0ed504fd36ca6576bb7b8853f0e6d727b1e2fa`，**与 ledger 逐字节一致**；
落盘字节数 674470 亦一致。`access_class` 为 `PUBLISHER_OA_DEREFERENCE`（非 arXiv 通道），与 "NOT_ON_ARXIV" 自洽；
四路否定为**上游核验结论，本次零网络不可独立复核**——本件只能声明「已按四路排除、记录在册」。

**表序核定**（按 PDF 出现顺序，以题注为准）：TABLE I = 主实验结果（第 3 页顶，14 行系统 × Earnings21/VoxPopuli 各 WER/RWER/F1）；
TABLE II = Earnings21 上下文 hit-rate 消融（第 4 页左栏）；TABLE III = context-augmented 训练消融（第 4 页右栏）。
Fig. 1 = Hybrid RAG-ASR System 架构图（第 2 页顶）。全篇**无公式编号**。

**抽取通道声明（承重）**：`pdftotext -layout` 对 TABLE I 的输出把 14 行数据打散重排（如 row 11/12 的 ASR-HYP 与 Context 列错位、
行号 12–14 与数值分离），**若据文本抽取取数会系统性串行**。本件因此对第 3、4 页做 200/170 dpi 渲染并**逐格目视读取**，
§5 全部数字以图像为准。任何下游承重引用如与本件数字不一致，**以第 3 页图像为仲裁**。

---

## 2. 方法本质：一篇论文里的三个系统，不是一个系统的三次消融

论文提出**三个结构不同的系统**共享同一检索层，逐一核如下（§III 全文核对）。

### 2.1 共享检索层（三系统同一）

原文 §IV-A "Pre-processing" 逐字：

> "we default to chunking the context file into segments of **320 characters with a 20-character overlap** using LangChain. The chunked text is then embedded using the **ALL-MPNET-BASE-V2** model, retrieved based on the **top-4** results according to **FAISS**'s cosine similarity metric."

检索查询 = **Whisper 首遍 ASR 假设的句嵌入**（Fig. 1 中 `Whisper → Sentence BERT → Query → Text Retriever`）。
**该检索层三系统共用、逐句无条件执行、参数为全局常数（chunk 320/overlap 20/top-4）——无阈值、无 no-retrieval 分支、无按样本决策。**

### 2.2 变体 A —— 纯文本纠错（Text-based）

Whisper 首遍假设 → 上述 FAISS 检回 → 检回上下文与假设拼接进 instruction template → prompt **Mistral-7B-Instruct-v0.3**。
两档：**zero-shot（预训练 LLM 不改）** 与 **LoRA 微调**。原文 §III-A：

> "Our experiments involve two settings: (1) a **zero-shot** scenario using the pre-trained LLM without modifications, and (2) a **fine-tuned** approach where the LLM is adapted using LoRA (Low-Rank Adaptation) **to reduce hallucination** and improve task-specific understanding."

**不回音频**——这一支是纯文本二次纠错器（GER 家族），信息访问上与 RAC/DARAG 同族。

### 2.3 变体 B —— 音频接地（Audio-grounded，**本篇的承重变体**）

骨干 = **QWen-audio-chat**（Whisper 音频编码器 + QWen-7B 作 decoder）。原文 §III-B 逐字：

> "The input sequence to the LLM decoder consists of a few key components: 1) the **audio representations** encoded by the ASR encoder, 2) the **retrieved textual context** and 3) the **first-pass ASR hypothesis**, along with the task instruction."

即 **音频 + 检回上下文 + 首遍假设** 三者同入 LLM decoder ——这正是「**带先前假设的音频重解码**」的完整形态。
两条训练期正则：

> "**Context dropout**, which randomly excludes the retrieved textual context from the prompt with a certain probability (**default 0.2**), forcing the model to rely more on the audio signal and the first-pass ASR hypothesis."
> "**First-pass hypothesis masking**, which applies BERT-style masks to tokens in the first-pass ASR hypothesis, with a **default probability of 0.4** … preventing it from acting lazily and **directly copy-pasting the first-pass hypothesis**."

**关键结构事实（本件对 R2 最有价值的一处）**：ASR-HYP 是**可缺省输入**。Table I row 9/10 的 `ASR-HYP` 列为 `-`，
即同一模型可**不带首遍文本、只用音频+检回上下文做 one-pass**；row 11/12 才带首遍假设。
论文自述 row 10 "showcases that the system is able to effectively perform **one-pass contextual ASR** as well"。
→ **同一模型、同一载体上同时存在「条件化单次解码」与「带先前假设的重解码」两个臂**（见 §7 的三分谱系与 §5.4 的受控差分）。

### 2.4 变体 C —— 混合（Hybrid）

在音频接地之上，把**频率法 custom vocabulary（CV）**经一条**新增的可训练通路**注入**音频表示**。原文 §III-C：

> "we use a design consisting of an **embedding layer followed by 2 transformer encoder layers**. A **joiner block with 2 transformer decoder layers** then takes in the **audio encoder's outputs as queries to cross-attend to these encoded text representations**, with a **residual connection** preserving the original audio information…"

Fig. 1 佐证：`Speech Encoder --Query--> X-attn Joiner <--K,V-- Text-to-audio Encoder <-- Unstructured Knowledge(Entity list)`，
joiner 输出与 speech encoder 输出经 `⊕`（题注："The ⊕ symbol represents addition"）合成 **AUGMENTED AUDIO FEATURES**，
再与 `<Instructions> [context] <masked-1st-pass-asr-hyp>` 一同进 LLM（LLM 上挂 Adapter=LoRA）。
文本编码器的 embedding 层用 **Whisper decoder 的 embedding 权重**初始化、用 Whisper tokenizer 分词。
CV 侧同样施加 context dropout（替换为特殊 mask token）。

**判定：变体 C 是架构改装**——新增两个模块、在音频编码器与 LLM 之间插入交叉注意力融合点。**在任何口径下都不是 API-only。**

---

## 3. 训练态与信息访问边界（合取判定的两条主证据链）

### 3.1 训练态：三变体全部 trained；唯一 training-free 臂是弱基线且自报幻觉

原文 §IV-A "Training" 逐字：

> "we adopt the **Low-Rank Adaptation (LoRA)** technique with **rank = 64** and **α = 128** for our experiments, resulting in approximately **163 million trainable parameters out of 8.5 billion** parameters for **QWen-audio-chat** LLM fine-tuning and **170 million out of 7.4 billion** parameters for **Mistral** fine-tuning."

混合系统另有两阶段训练：

> "In **phase 1**, we **freeze the LLM and the audio encoder**, training only the **text encoder and the joiner**. The combined text encoder and joiner have approximately **160 million parameters**… In **phase 2**, we apply **LoRA fine-tuning** on the augmented Earnings22 split."

**唯一的 training-free 臂 = 变体 A 的 zero-shot 档（Table I row 5/6）**，而论文对它的定性是：

> "For the text-based system, **direct inference using both the context and the first-pass hypothesis suffers from hallucinations**. To address this, we employ a **length-filtering mechanism that rejects the LLM hypothesis if its length deviates significantly from the first-pass ASR hypothesis**."

三条必须记下的后果：

1. **该 zero-shot 臂在数字上是净负的**（§5.2）：row 6（zero-shot + RAG）在 Earnings21 上 WER 11.39 / RWER 11.37，
   **双双劣于 Whisper 基线 10.92 / 10.95**；在 VoxPopuli 上 11.24 / 23.04，劣于基线 9.59 / 20.94 更甚。
   → **本篇不构成任何 training-free 先例；恰恰相反，它是「同载体上 training-free 文本 GER 净负」的一手证据。**
2. **length-filtering 是一条模型外的确定性否决规则**——这是本篇唯一的「外显阈值+回退首遍假设」结构，**须诚实登记为门先例的一个弱形态**
   （详见 §6.3）；但它是**幻觉抑制启发式**（只看长度偏离），不读任何信息价值信号，阈值未报值，且**只用于 zero-shot 臂**。
3. **「trained 二次纠错器」与「trained 音频重解码占据者」两个身份同时成立**：变体 A-FT 占据前者，变体 B/C 占据后者。

### 3.2 信息访问：三变体逐条判

| 变体 | 注入通道 | 是否读/改核内部 | API-only? |
|---|---|---|---|
| A 纯文本（zero-shot） | prompt（Mistral instruction template） | 否 | **接口层是**（但见 §3.1，该臂净负、且外挂 length-filter） |
| A 纯文本（LoRA-FT） | prompt + **LoRA 改权重** | 改权重 | **否** |
| B 音频接地 | LLM decoder 输入序列**手工装配**（音频表示 + 上下文 + 首遍假设 + 指令）+ **LoRA 改权重** | 需要能把 encoder 输出与文本 token 拼成 decoder 输入序列 | **否**（两重：序列装配 + 权重训练） |
| C 混合 | 在 **audio encoder 与 LLM 之间新增 text encoder + X-attn joiner + 残差加法** | **架构改装** | **否**（最强否定） |

**判定：`架构改装 = 非 API-only` 逐字成立**——Fig. 1 与 §III-C 的模块描述本身即证据，无需推断。

---

## 4. 协议：循 ConEC，但换掉了参考层（**R2 reference 双报决策的直接佐证**）

### 4.1 划分与上下文库：完全循 ConEC

> "Authors of **[19]** augmented the Earnings21/22 dataset by incorporating real-world contexts. **Following the settings in the paper, we use Earnings22 as the training data and Earnings21 as the test data.** We concatenate utterances from the same recordings by their chronological order for efficient training."

（`[19]` = Huang et al., "ConEC: Earnings call dataset with real-world contexts…", LREC-COLING 2024——参考文献表逐字核对一致。）

> "For each utterance in the Earnings21/22 corpus, we use the **context files associated with the corresponding recording** as the **RAG database** for retrieval."

**独立交叉确认**：论文 §IV-C 写 "the limited availability of context in the Earnings22 split (**43 out of 125 recordings**)"，
与 ConEC 侧的 Earnings-22 规模（125 录音）逐字吻合——**两篇对同一载体的描述互证，本篇确为同一 ConEC 上下文层的消费者**。

VoxPopuli 侧：> "we use a **single corpus-level database**, which consists of the **English portion of the Europarl** corpus, a non-parallel corpus of parliamentary proceedings."
（即 VoxPopuli 是**语料级单库**，与 Earnings 的**逐场库**是两种作用域——本篇的双载体对照在作用域上不受控，见 §5.5。）

### 4.2 参考层：未获 ConEC 修订转写，用原始参考（**承重**）

原文 §IV-A "Evaluation" 逐字：

> "The authors of [19] **augmented the Earnings21 data by replacing the `inaudible` and `unk` tokens with transcribed words**. **As we do not have access to this data, we reproduce the Whisper baseline using the original dataset**, applying **word-level Whisper normalization without deletion** to align word tags for compatibility, **as done for all of our results**."

**四条后果，逐条承重：**

1. **本篇的 Earnings21 数字与 ConEC 报告的数字不可直比**。三处口径同时不同：
   ①**参考层**（本篇=原始 Earnings-21 参考；ConEC=S&P 半自动修订后参考）；
   ②**评分栈**（本篇=word-level Whisper normalization without deletion；ConEC=fstalign + whisper_normalizer）；
   ③**稀有词定义**（本篇=训练集词频 + 评测集出现次数 + 一个**未报值的 occurrence threshold**；ConEC=SPGISpeech 词频 top-3k 之外）。
2. **有一个可量化的裂口读数**：本篇 Whisper 基线在 Earnings21 上 **WER 10.92**；ConEC 的 Whisper-large 行为 **7.98**。
   同一测试集、同一识别器族，**差 2.94 pp**。该差被三个混淆项共同解释——参考层、评分栈、**以及本篇自始至终未报 Whisper 型号**（§6.4 缺口 1）。
   **这是「跨篇拼接 Earnings21 数字必然出错」的一手实证，不是推断。**
3. **对 R2 reference 双报决策的直接佐证**：签字表现行口径为「reference 采 ConEC 修订版、**对照处双报**」。
   本篇证明该决策是**必需而非保守**——读集内已存在一篇同载体、同协议、**采用原始参考**的已发表工作；
   若 R2 只报修订版一列，则与本篇的一切对照都无法建立；若只报原始版，则与 ConEC 官方基线断链。**双报是唯一能同时接住两条谱系的口径。**
4. **本篇自身构成 R2 双报表的第二列样例**：R2 的「原始参考」列可直接把本篇 Table I 全表作为同口径外部读数
   （前提是评分栈亦对齐到 word-level Whisper normalization without deletion，**否则仍不可比**）。

### 4.3 CV 列表的构造（一条训练侧信息边界注记）

> "For the hybrid system, the **training CV list is crafted based on each utterance's ground-truth transcript with dynamically sampled distractors**, whereas the **evaluation CV list is derived solely from the recording-level context document**."

**评测侧干净**（CV 来自上下文文档，非 gold）；**训练侧是 gold 派生**（逐句从参考转写抽 + 动态干扰项）。
同类构造还有 §IV-C 的 context augmentation：> "synthesizes additional context documents by prompting the **Claude-3.5-Sonnet** LLM to generate background documents **based on the ground-truth transcript**"——同样只用于**训练**。
→ **登记为 `TRAIN_TIME_GOLD_DERIVED`**：不构成测试泄漏，但意味着该模型被训练成「习惯于高精度实体清单」，
其在真实（低覆盖、含干扰）上下文上的鲁棒性存在**训练分布偏置**。R2 若把本篇当对手臂，须声明这一非对称。

---

## 5. 关键数字（全部取自第 3/4 页渲染图像逐格核对）

### 5.1 TABLE I 全表（第 3 页；WER/RWER 越低越好，F1 越高越好；粗体=原表粗体）

| # | 系统 | Speech Encoder | Decoder | ASR-HYP | Context | E21 WER | E21 RWER | E21 F1 | VP WER | VP RWER | VP F1 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Baselines | Whisper | Whisper | - | - | 10.92 | 10.95 | 0.78 | 9.59 | 20.94 | 0.88 |
| 2 | Baselines | Whisper | Whisper | - | CV | **28.97** | **27.17** | 0.64 | - | - | - |
| 3 | Baselines | QWen-audio-chat | QWen-7B | - | - | 19.11 | 22.63 | 0.61 | 7.43 | 26.70 | 0.85 |
| 4 | Baselines | QWen-audio-chat | QWen-7B | - | RAG | **42.48** | **28.73** | 0.73 | 9.28 | 22.51 | 0.88 |
| 5 | Text-based | - | Mistral | Whisper | - | 12.51 | 12.04 | 0.84 | 9.48 | 23.56 | 0.87 |
| 6 | Text-based | - | Mistral | Whisper | RAG | 11.39 | 11.37 | 0.80 | 11.24 | 23.04 | 0.87 |
| 7 | Text-based | - | Mistral-FT | Whisper | - | 11.36 | 12.14 | 0.74 | 8.68 | 21.47 | 0.88 |
| 8 | Text-based | - | Mistral-FT | Whisper | RAG | 11.18 | 11.41 | 0.87 | 9.31 | 16.75 | 0.91 |
| 9 | Audio-grounded | QWen-audio-chat | QWen-7B-FT | - | - | 14.21 | 13.38 | 0.57 | 7.31 | 27.75 | 0.84 |
| 10 | Audio-grounded | QWen-audio-chat | QWen-7B-FT | - | RAG | 13.37 | 12.08 | 0.84 | 5.91 | 23.04 | 0.87 |
| 11 | Audio-grounded | QWen-audio-chat | QWen-7B-FT | Whisper | - | 8.99 | 9.46 | 0.80 | 5.65 | 17.80 | 0.90 |
| 12 | Audio-grounded | QWen-audio-chat | QWen-7B-FT | Whisper | RAG | 8.65 | 8.83 | 0.88 | **5.17** | **12.57** | **0.93** |
| 13 | Hybrid | QWen-audio-chat | QWen-7B-FT | Whisper | CV | **8.13** | 8.59 | 0.81 | - | - | - |
| 14 | Hybrid | QWen-audio-chat | QWen-7B-FT | Whisper | RAG + CV | 8.61 | **8.37** | **0.91** | - | - | - |

论文自述的四处头条（本件逐一复算通过）：
row 12 对 row 1 在 VoxPopuli 上 **WER −4.42 / RWER −8.37 / F1 +0.05**；row 12 对 row 1 在 Earnings21 上 **WER −2.27 / RWER −2.12**；
row 13 对 row 11 **RWER −0.87 / F1 +0.01**；row 14 对 row 13 **RWER −0.22 / WER +0.48**。

**两处原文叙述与表体不符（照录，下游以表体为准）**：
①"The substantial F1 increase (**0.27** for Earnings21 and **0.03** for VoxPopuli)" 一句挂在 "compared to the QWen baseline (**row 3**)" 之后，
但 0.27 / 0.03 实为 **row 9→row 10**（0.57→0.84 / 0.84→0.87）；row 3→row 10 为 +0.23 / +0.02。
②row 13→row 14 的 "a **0.03** increase in F1 score" 与表体 0.81→0.91（+0.10）不符；+0.03 对应的是 row 12（0.88）→row 14（0.91）。
→ **同一句内 RWER 差分与 F1 差分用了不同的参照行。R2 引用时一律以表体重算。**

### 5.2 冻结核 + 无条件注入 = 灾难（**本篇对 R2 最承重的一格**）

两个**冻结核 prompt 注入**对照，全部剧烈净负（Earnings21）：

| 对照 | 核状态 | 注入 | WER | RWER | F1 |
|---|---|---|---|---|---|
| row 1 → row 2 | 冻结 Whisper | **CV 列表** | 10.92 → **28.97**（+18.05 pp，×2.65） | 10.95 → 27.17（+16.22） | 0.78 → 0.64（−0.14） |
| row 3 → row 4 | 冻结 QWen-audio-chat | **RAG 上下文** | 19.11 → **42.48**（+23.37 pp，×2.22） | 22.63 → 28.73（+6.10） | 0.61 → 0.73（**+0.12**） |

**同一注入在 LoRA 适配后的核上完全逆转**（输入完全对齐的受控对：均为 no-hyp）：

| 输入 | 冻结核 | LoRA 核 | 差 |
|---|---|---|---|
| 音频，无上下文（row 3 → row 9） | 19.11 | 14.21 | **−4.90 pp** |
| 音频 + RAG（row 4 → row 10） | 42.48 | 13.37 | **−29.11 pp** |
| **归因差** | | | **24.21 pp 的适配收益专门用于「学会不被注入的上下文摧毁」** |

VoxPopuli 同型但幅度小一个量级：row 3→4 为 7.43→9.28（+1.85 pp）；row 4→10 为 9.28→5.91（−3.37）；row 3→9 为 7.43→7.31（−0.12）；归因差 **3.25 pp**。

**三条判定**：
1. **这是读集内「无条件注入净负」证据链上最强的一格**——它发生在**冻结核 + prompt 注入**（即 R2 的部署形态）、
   在 **R2 主载体（Earnings21 + ConEC 上下文）**上、且带 **no-injection 参照臂**（row 1 / row 3）。
   与 RECAST 全表灾难、RAG-Boost raw-RAG 净负、Huang24f vanilla NB 净负、ConEC row 3 三类退化同向，**但载体与接口形态最贴 R2**。
2. **同时是「噪声耐受属于核的训练分布而非注入策略」这一登记假设在单篇内的最干净证据**：
   同一上下文、同一骨干、同一输入格式，仅差 LoRA 适配 → 42.48 vs 13.37。
3. **指标符号相反的警告**：row 3→4 在 **WER 上 ×2.22 恶化、F1 上 +0.12 改善**。
   若 R2 只报实体 F1，无条件注入会被读成「有效」；只有总/稀有词 WER 才暴露灾难。
   **该格是 R2「主指标不得只报实体 F1」条款的一手外部实例。**

### 5.3 「加检索上下文」的十二个对照：总 WER 半数净负、稀有词 WER 几乎全数净正

对全表所有「同系统 ± 检索上下文」对照逐一取差（E21 七对、VoxPopuli 五对）：

| 对照 | E21 ΔWER | E21 ΔRWER | VP ΔWER | VP ΔRWER |
|---|---|---|---|---|
| row1→2（冻结 Whisper +CV） | **+18.05** | **+16.22** | — | — |
| row3→4（冻结 QWen +RAG） | **+23.37** | **+6.10** | **+1.85** | −4.19 |
| row5→6（zero-shot Mistral +RAG） | −1.12 | −0.67 | **+1.76** | −0.52 |
| row7→8（Mistral-FT +RAG） | −0.18 | −0.73 | **+0.63** | −4.72 |
| row9→10（QWen-FT +RAG, no hyp） | −0.84 | −1.30 | −1.40 | −4.71 |
| row11→12（QWen-FT +RAG, +hyp） | −0.34 | −0.63 | −0.48 | −5.23 |
| row13→14（Hybrid CV→RAG+CV） | **+0.48** | −0.22 | — | — |

**统计**：12 个对照中**总 WER 净负 6 个**（含两个冻结核对照、幅度最大）；**稀有词 WER 净负仅 2 个**（均为冻结核 Earnings21 臂）。
**四个音频接地微调对照（row9→10、row11→12，各两载体）在总 WER 与稀有词 WER 上全部净正**——
即 **「回音频 + 已适配」是本表中唯一不为无条件检索付总 WER 税的组合**。

**R2 可直接使用的两条陈述**：
- **(A) 无条件检索普遍带总 WER 税，且税率随核的适配程度递减**（冻结 +18~+23 pp → zero-shot ±1~2 pp → 微调文本 ±0.6 pp → 音频接地微调 −0.3~−1.4 pp）。
  **门控准入要保护的正是这笔税**，而 ConEC 已把总 WER 降为 `READOUT_ONLY`——两者合看：**门的价值应在稀有词/实体面报增益、在总 WER 面报"不退化"。**
- **(B) 即使是在该上下文分布上训练过的系统，叠加 RAG 仍付总 WER 税**（row 13→14 的 +0.48 pp，论文自归因
  "likely caused by the **additional noise introduced by the retrieved context**"）。→ **训练不能消除税，只能压低税率**；这是门控相对"再训练"的存活位。

### 5.4 首遍假设 vs 检回上下文的贡献分解（**同模型受控，读集内唯一**）

| 差分 | 含义 | E21 ΔWER | E21 ΔRWER | E21 ΔF1 | VP ΔWER | VP ΔRWER |
|---|---|---|---|---|---|---|
| row 10 → row 12 | **加首遍假设**（上下文已有） | **−4.72** | **−3.25** | +0.04 | −0.74 | −10.47 |
| row 9 → row 11 | **加首遍假设**（无上下文） | **−5.22** | **−3.92** | +0.23 | −1.66 | −9.95 |
| row 11 → row 12 | **加检回上下文**（首遍假设已有） | −0.34 | −0.63 | +0.08 | −0.48 | −5.23 |
| row 9 → row 10 | **加检回上下文**（无首遍假设） | −0.84 | −1.30 | +0.27 | −1.40 | −4.71 |

**读数**：在 Earnings21 上，**首遍假设的贡献是检回上下文的约 14 倍**（4.72 vs 0.34 pp WER）；
VoxPopuli 上约 1.5 倍（WER）/ 2 倍（RWER）。

**必须同时声明的混淆项（否则是误引）**：row 9/10 与训练设置**不匹配**——模型训练时首遍假设始终在场（仅按 p=0.4 做 token 级 mask），
从未见过完全缺席的输入；论文自述 row 12 才是 "with input aligning with the training setting"，并对 row 9 明说 "**Despite the mismatch in training and inference setting**"。
→ **4.72 / 5.22 pp 是首遍假设价值的上界，与训练/推理失配混杂，不可分离。** R2 若要干净读数，须自建对称训练的两臂。

### 5.5 TABLE II —— hit-rate 消融（第 4 页；Earnings21，默认 top-k=4）

| Context | Chunk Size | Overlap | Query | Hit-rate ↑ |
|---|---|---|---|---|
| **Oracle**（整份上下文文档，覆盖上界） | - | - | - | **69.02** |
| RAG | 50 | 0 | Whisper-ASR | 28.53 |
| RAG | **320** | **20** | **Whisper-ASR** | **42.08**（=主结果所用配置） |
| RAG | 500 | 20 | QWen-Audio-Chat | 42.98 |
| RAG | 500 | 20 | Whisper-ASR | 44.22 |
| RAG | 500 | 20 | Oracle | 45.50 |
| RAG | 1000 | 20 | QWen-Audio-Chat | 47.71 |
| RAG | 1000 | 20 | Whisper-ASR | 48.15 |
| RAG | 1000 | 20 | Oracle | 48.44 |
| **CV + RAG** | 320 | 20 | Whisper-ASR | **54.12** |

原文：> "This upper bound indicates that approximately **30% of the rare words are not covered by the context**."（69.02 → 约 30% 缺口）

**四条对 R2 直接承重的推算（本件计算）**：
1. **检索损失 ≫ 查询质量损失**。默认配置 42.08 距覆盖上界 69.02 有 **26.94 pp**；
   而把查询从 Whisper 假设（WER 10.92）换成 **oracle 转写（WER 0）**只涨 **1.28 pp**（44.22→45.50 @500）或 **0.29 pp**（48.15→48.44 @1000）。
   → **在本载体上，改善检索表示/深度的杠杆约为改善查询质量的 20 倍。**
2. **首遍质量对检索的影响极小**：把查询换成 WER 19.11 的 QWen-audio-chat 输出，hit-rate 仅降 **1.24 pp**（44.22→42.98 @500）
   或 **0.44 pp**（48.15→47.71 @1000）。→ **一个 WER 差近一倍的首遍假设，作为检索 query 几乎一样好。**
   **这是对 R2「用重听改善检索 key」这一分量的反向先验，必须写进 §0 具名反向先验**（限定：hit-rate 是检索侧代理指标，非 WER；
   且本载体上下文为逐场小库、语义检索，未必外推到大库/声学 key 设定）。
3. **chunk 尺寸只被在 hit-rate 上扫过，从未在 WER 上扫过**：主结果固定 320/20（hit-rate 42.08），
   而 1000/20 可达 48.15——**+6.07 pp hit-rate 的配置从未被报过 WER**。这是本篇的一个空格（§8 改进空间 (b)）。
4. **CV 与 RAG 在覆盖上互补**：同为 320/20、同为 Whisper 查询，CV+RAG 54.12 vs RAG-only 42.08 = **+12.04 pp**。
   → **多源互补性在本载体上首次有了覆盖率级读数**（ConEC 侧只有 PERSON 30%→82% / ORG 56%→66%）；
   **但仍无逐源 WER 消融**——「多源**选择**」在本载体上依然是空格。

### 5.6 TABLE III —— context augmentation（第 4 页；音频接地系统，Earnings21）

| Train Context | WER ↓ | RWER ↓ | P ↑ | R ↑ | F1 ↑ |
|---|---|---|---|---|---|
| Original | **8.65** | **8.83** | 0.96 | 0.82 | 0.88 |
| Augmented（Claude-3.5-Sonnet 依 gold 转写合成的背景文档） | 8.74 | 8.81 | **0.97** | **0.86** | **0.91** |

（Original 行与 Table I row 12 的 Earnings21 三格逐位一致 8.65/8.83/0.88——**内部自洽核对通过**。）
论文自述：> "this improvement comes with a minor growth in general WER by **0.09**, likely due to the model's **increased reliance on the context**, including any noise that may be present."
→ **第三次出现同一形状：召回/实体面涨、总 WER 跌**；且论文把机制归因为「对上下文的依赖增强」——**这正是准入门要调的那个旋钮**。

---

## 6. 合取判定（逐字引证）

R2 的独立性合取 = **API-only + training-free + 双源同尺度动作选择 + 外显世界知识 rescore**。逐项判：

### 6.1 training-free —— ✗（否定，且是强否定）

- 逐字：`rank = 64`、`α = 128`、`163 million trainable parameters out of 8.5 billion`（QWen-audio-chat）、
  `170 million out of 7.4 billion`（Mistral）、混合系统 phase-1 训练 `text encoder and the joiner`（`approximately 160 million parameters`）+ phase-2 LoRA。
- **唯一 zero-shot 臂（row 5/6）净负**（§5.3）且论文自述 `suffers from hallucinations`、需 `length-filtering mechanism` 兜底。
- **结论**：本篇**不占据** R2 的 training-free 分量；反而为「同载体上 training-free 文本 GER 净负」提供一手读数。

### 6.2 API-only —— ✗（否定，架构改装为最强证据）

- 变体 C 逐字：`an embedding layer followed by 2 transformer encoder layers` + `a joiner block with 2 transformer decoder layers`
  + `residual connection`，插在 `audio encoder's outputs` 与 LLM 之间（Fig. 1 的 `⊕`）。**这是新增模块的架构改装。**
- 变体 B 亦否：`The input sequence to the LLM decoder consists of … 1) the audio representations encoded by the ASR encoder, 2) … 3) …`
  ——需要**手工装配 decoder 输入序列**（把 encoder 输出与文本 token 拼接），黑盒 API 不提供该入口；叠加 LoRA。
- **结论**：本篇**不占据** API-only 分量。

### 6.3 门控动作选择 —— ✗（缺席），**但须诚实登记两处近似物**

- **缺席证据**：检索层参数为全局常数（chunk 320/overlap 20/**top-4**），**逐句无条件执行**；
  全篇无阈值、无 no-retrieval 分支、无「是否重跑」判断步、无按样本的动作决策。
- **近似物 1 —— context dropout（p=0.2）与 first-pass masking（p=0.4）**：二者是**训练期随机正则**，
  作用是让模型在上下文缺席时仍可用，**不是推理期的决策规则**。它们让「无上下文」成为模型的一个合法工作点——
  这在结构上**为门控准备了条件，但不构成门控**。
- **近似物 2 —— length-filtering（唯一的推理期外显否决）**：`rejects the LLM hypothesis if its length deviates significantly from the first-pass ASR hypothesis`。
  这**是**一条模型外、确定性、带阈值、回退到首遍假设的准入规则。**必须登记为门先例的弱形态**（与 Lei 的布尔触发、RAC 的确定性准入过滤、
  PRISM 手工阈值同族），并据此**收窄 R2 措辞**：R2 的 delta 不是「首次给重解析加一道外显阈值」，而是
  **「门控信号读的是信息价值/感知不确定性，而非输出长度这类与信息无关的健全性代理」**，且**阈值可标定**（本篇阈值未报值、未标定、未消融）。

### 6.4 外显世界知识 rescore —— ✗（外显分量缺席）

- 检回上下文与 CV 全部**直接进 decoder 输入**，由 LLM 在解码中隐式取舍；**无独立的存在性/语境裁决阶段、无候选打分、无可读出的知识分数**。
- 与 Zhang 线的判定同型（核内隐式裁决）；R2 的 delta 须继续限定为**「外显、可标定、与解码分离的」** rescore。

### 6.5 双源同尺度选择 —— ✗（缺席）

- 本篇确有**两个外部源**（语义 RAG 上下文 + 频率法 CV），且 row 13/14 给出 CV-only 与 RAG+CV 两个臂——
  **但这是臂对照，不是运行时选择**；row 14 是**无条件并用**（`RAG + CV`），无预算分配、无二选一、无「都不用」出口。
- 且**缺逐源 WER 消融**：Table II 只给覆盖率级的 CV 增量（+12.04 pp hit-rate），**从无 RAG-only vs CV-only vs 并用的等条件 WER 三臂**
  （row 13/14 的 CV-only 与 RAG+CV 之间少了 RAG-only 这一臂，且两行 chunk/top-k 未声明是否同配置）。

### 6.6 合取结论

**本篇在四分量中占据零项**（training-free ✗、API-only ✗、双源选择 ✗、外显 rescore ✗）。
**合取存活。** 但本篇是读集内**在载体与协议上最贴近 R2 的一篇**（同 ConEC 上下文层、同 E-22/E-21 划分），
因此它的**反向读数（§5.2/§5.5 第 2 条）比任何远域近邻都更有杀伤力**——必须全数写入 R2 的反向先验，不得只取有利面。

---

## 7. 「重解析」谱系更新判定（三分动作空间）

R2 现行 †注把该分量的占据记为两条线（Zhang 线=TF prompt 重跑；Wang 线=条件化单次解码、非重解码）。
**本篇是该动作空间的第三点，且填的是此前空着的那格。**

| 线 | 训练态 | 是否回音频 | 是否带**先前假设** | 注入层 | 动作形态 |
|---|---|---|---|---|---|
| **Zhang**（BigData 2023） | training-free〔摘要级 PROBABLE〕 | 是（Whisper 二次运行） | 是（第一步的一遍假设催生候选，但**假设本身不入第二遍**——第二遍输入=音频+候选 prompt） | prompt（近 API-only） | **TF prompt 重跑** |
| **Wang**（ICASSP 2024, 2402.01828） | 训练 speech retriever + SLM | 是（音频驱动检索 + SLM 解码） | **否**（无先前假设可重；先前轮音频架构上不可回访） | 文本拼接 + 白盒训练 | **条件化单次解码** |
| **Xiao（本篇）** | **trained**（LoRA r=64 α=128；混合档另训 160M 模块） | 是 | **是**（首遍假设**显式作为 decoder 输入的第 3 项**） | decoder 输入序列装配 / 架构改装 | **trained 带先前假设的音频重解码** |

**三分判定**：三者按 {训练态} × {是否带先前假设} 把动作空间切成三格——
**「training-free × 带先前假设 × 音频重解码」这一格由 Zhang 线部分占据（prompt 通道、疑似零训练），
「trained × 带先前假设」由本篇占据，「trained × 不带先前假设」由 Wang 线占据。**

**R2 的 delta 因此必须精确表述为**（三条，逐条可直接替换 §8 †注的现有措辞）：

1. **重解析动作本身零新颖性**——三线已从三个方向占满该动作空间的主要形态。
2. **R2 的 delta = 门控**：*何时*重解析、*重听哪一段*、*以何种先前假设重解析*——由**模型外可标定标量 + 外显阈值**裁决。
   三线**全部无条件执行**（Zhang 三步管线全称量化于所有音频；Wang 单次解码固定序；本篇逐句 top-4 无条件、
   其唯一推理期否决规则读的是输出长度而非信息价值）。
3. **R2 的 delta 还叠加 training-free + API-only 两个约束**——本篇**在同一载体上证明了这两个约束的代价**：
   在冻结核 + prompt 注入下，同一上下文使 WER 从 19.11 涨到 42.48；LoRA 适配把它压到 13.37。
   → **R2 的门控必须承担 LoRA 在本篇里承担的那 24.21 pp 的「抗注入」职责**。这是 R2 机制必要性的最强正面论证，
   同时也是 R2 最大的风险：**若门控做不到，R2 在本载体上的 API-only 路线直接被本篇证伪。**

**衍生的臂族建议**：本篇给出一条**可运行的 trained comparator 拓扑**——
「音频 + 检回上下文 + 首遍假设 → 单次重解码」。R2 §5.3 已有 `serial-composition` 固定档；
建议再补一条 **`prior-hypothesis-conditioned re-decode`（无门控、首遍假设无条件入上下文）** 固定档，
其效果差分（§5.4 的 −4.72 pp）说明这条臂**很强**，是 R2 门控增量必须超过的具名基线。

---

## 8. DFS 四问

**方法**：用 RAG 把上下文 ASR 从「手工 custom vocabulary」改造为「以首遍 ASR 假设为查询、从逐场文档库检回文本块」的检索问题，
再用三条注入路线把检回内容送给 LLM：纯文本二次纠错（Mistral）、音频接地重解码（QWen-audio-chat：音频+上下文+首遍假设同入 decoder）、
以及把频率法 CV 经新增 text-encoder+joiner 注入音频表示的混合式。全部经 LoRA 适配；核心主张是
**微调后的系统学会了从检回内容中抽取相关上下文来纠错，且对噪声上下文鲁棒**。

**局限**：
1. **不是 training-free**——三变体全 trained；唯一 zero-shot 臂在两载体上净负且自报幻觉。
2. **不是 API-only**——变体 B 需装配 decoder 输入序列，变体 C 是架构改装。
3. **参考层与 ConEC 不同**（未获修订转写、用原始参考 + word-level Whisper normalization），
   且**从未报 Whisper 型号**——已发表数字与 ConEC 侧不可直比，与本篇自身也难以复现。
4. **稀有词与 F1 定义不完整**：稀有词依赖「训练集词频 + 评测集出现次数 + **未报值的 occurrence threshold**」；
   **F1 的定义（对什么求 P/R）全篇未给**。
5. **无置信区间、无显著性检验、无随机种子、无重复实验**；每格单次读数。
6. **检索侧超参从未在 WER 上消融**：chunk size / overlap / top-k 只在 hit-rate 上扫过；主结果用的 320/20 甚至不是 hit-rate 最优档。
7. **多源无逐源 WER 消融**：CV 与 RAG 的互补性只有覆盖率级证据（+12.04 pp），且 row 13/14 缺 RAG-only 臂。
8. **训练侧 gold 派生**：训练 CV 由 gold 转写抽取 + 干扰项；context augmentation 由 Claude-3.5-Sonnet 依 gold 转写合成。
   评测侧干净，但模型带「高精度实体清单」的训练分布偏置。
9. **无代码、无检查点、无 λ/阈值数值**（length-filter 的"significantly"未量化）→ **不可复算**。
10. **row 9/10 与训练设置失配**，论文自认；其差分因此与失配混杂。
11. **正文两处差分叙述与表体不符**（§5.1）。
12. **无门控臂、无 no-retrieval 逐句分支、无成本记账**（token/时延全篇未报）。

**改进空间**（按对 R2 的价值排序）：
- **(a) 门控是本篇最大的空格，且本篇自己造出了门控的必要性**：row 3→4 的 +23.37 pp 说明冻结核下必须有人把噪声上下文挡住；
  本篇用 LoRA 挡，R2 用门挡。**「LoRA vs 门」是一个干净的、同载体的对照命题。**
- **(b) chunk/top-k 的 WER 曲线**：hit-rate 已知在 320→1000 上单调涨（42.08→48.15）并趋饱和，
  但**注入量增大同时抬高稀释代价**——**hit-rate 与 WER 的交叉点（crossover）从未被测过**。
  这与 R2 已登记的 DICT-SCALE 规模扫描同题，且本篇提供了现成的覆盖率轴。
- **(c) 逐源等条件三臂（RAG-only / CV-only / RAG+CV）在 WER 上的对照**——本篇只做了后两臂。
- **(d) 首遍假设的价值在对称训练下重测**（消除 §5.4 的失配混淆）。
- **(e) 把 length-filter 换成信息价值门**：本篇已证明「需要一道输出侧否决」，但用的是长度启发式；
  换成可标定标量是直接的替换实验。

**可借鉴**：
1. **「同一模型、ASR-HYP 可缺省」的设计**是读集内唯一能在**同一权重**下同时跑 one-pass 与 re-decode 的结构——
   R2 若要做「重解析 vs 单次」的干净对照，这是现成的拓扑（但须对称训练）。
2. **hit-rate 作为检索侧中间指标 + oracle 覆盖上界（69.02）**：这是 ConEC oracle-headroom 程序在**检索侧**的对应物。
   **建议 R2 §7 判别力条款把「先算 oracle headroom」扩写为两级**：**上下文覆盖上界（本篇 69.02）→ 检索命中率（42.08）→ 效果**，
   两级都要先算，才能把「没赢」归因到「库里没有」还是「检索没找到」还是「核没用上」。**这是本篇最可移植的方法论贡献。**
3. **查询质量的价格标签（1.24~1.28 pp hit-rate）**：任何「改善检索 query」的机制在本载体上的天花板已被本篇钉死。
4. **context dropout / hypothesis masking 两条训练期正则**：若 R2 后续需要一条 trained 上界对照臂，这两条是让模型
   「在证据缺席时不崩」的成熟做法——**恰是门控在 training-free 侧要替代的东西**。

---

## 9. §8 矩阵行草案

R2 §8 矩阵列序（`proposals/2026-07-29-r2-coreview-draft.md` 第 734 行表头）：
`| 近邻 | 训练态 | 信息访问 | 机制单元 | 公开载体 | R2 新增变量（逐项具名） |`

**建议置于 ConEC 行之后**（同载体谱系相邻），并把量词自限从「十五件」改为「**十六件**」（十四件 D2 + Zhang 摘要级 + 本件 D2；
**准确件数须由 R2 主稿在同一 commit 内复算**）。

| 近邻 | 训练态 | 信息访问 | 机制单元 | 公开载体 | R2 新增变量（逐项具名） |
|---|---|---|---|---|---|
| Xiao et al. (ICASSP 2025, DOI 10.1109/ICASSP49660.2025.10890057；无 arXiv 版〔上游四路否定，本件零网络未复核〕；出版方 OA PDF，**页面无 IEEE 页眉/venue 行**) | **三变体全 trained**：LoRA **r=64 / α=128**——QWen-audio-chat **163M/8.5B**、Mistral **170M/7.4B**；混合式另有 phase-1 训练 text encoder+joiner（**约 160M**）再 phase-2 LoRA。**唯一 zero-shot 臂（Mistral 直推）在两载体总 WER/稀有词 WER 上双双劣于 Whisper 基线，且自述 `suffers from hallucinations`、须外挂 length-filtering 兜底**——**非 training-free 先例，反为「同载体 TF 文本 GER 净负」一手读数** | **非 API-only（两级否定）**：①音频接地变体须**手工装配 LLM decoder 输入序列**（音频表示 + 检回上下文 + 首遍假设 + 指令）；②混合变体为**架构改装**——在 audio encoder 与 LLM 之间新增 embedding+2 层 transformer encoder 与 2 层 decoder 的 X-attn **joiner**，输出与音频表示**残差相加**（Fig.1 `⊕`）。叠加 LoRA 改权重 | 三系统共享一条**无条件**检索层（首遍 Whisper 假设 → ALL-MPNET-BASE-V2 句嵌入 → FAISS 余弦 **top-4**，chunk **320 字符/overlap 20**，全局常数、无阈值、无 no-retrieval 分支）；**变体 A** 纯文本二次纠错（Mistral-7B-Instruct-v0.3）；**变体 B 音频接地重解码**（首遍假设**可缺省**→同一权重下亦可 one-pass）；**变体 C 混合**（频率法 CV 经受训 text encoder+joiner 注入音频表示）。训练期正则：context dropout **p=0.2**、first-pass hypothesis masking **p=0.4**。**推理期唯一外显否决=length-filtering（长度偏离即弃 LLM 假设、回退首遍；阈值未报值、读的是长度而非信息价值）** | **Earnings21（评测）/ Earnings22（训练）——逐字循 ConEC 协议**，RAG 库=**ConEC 逐场 context files**；VoxPopuli（Europarl 英文语料级单库）。**未获 ConEC 修订转写、用原始参考 + word-level Whisper normalization without deletion，且全篇未报 Whisper 型号→与 ConEC 数字不可直比（其 Whisper 基线 E21 WER 10.92 vs ConEC Whisper-large 7.98）**。主结果：row12 音频接地 8.65/8.83/0.88（E21）、**5.17/12.57/0.93**（VP）；row14 混合 8.61/**8.37**/**0.91**。**冻结核无条件注入两格灾难：Whisper+CV 10.92→28.97、QWen-audio-chat+RAG 19.11→42.48；同输入下 LoRA 适配把后者压到 13.37（归因差 24.21pp 专用于抗注入）**。hit-rate：上下文覆盖上界 69.02、默认配置 42.08、CV+RAG 54.12；**oracle 查询较 Whisper 查询仅 +1.28pp** | 零训练（其三变体全 trained、唯一 zero-shot 臂净负）；API-only（其架构改装+decoder 序列装配）；**门控动作选择**（其检索逐句无条件 top-4；context dropout/masking 为训练期正则非推理决策；length-filter 为长度启发式、读输出长度不读信息价值、阈值未报未标定）；**多源同尺度选择**（其 CV 与 RAG **无条件并用**，缺 RAG-only 等条件臂、无逐源 WER 消融）；**外显世界知识 rescore**（其候选裁决为核内隐式解码取舍，无独立裁决阶段）。**† 重解析谱系**：本篇=**trained 带先前假设的音频重解码**，与 Zhang（TF prompt 重跑）、Wang（条件化单次、无先前假设）三分该动作空间——R2 delta=**门控选择性 + training-free + API-only 的重解析**，动作本身零新颖性 |

**对 §8 其余部分的连带处置建议（三条）**：

1. **双侧证据合同须新增本篇的两格**：`Whisper+CV 10.92→28.97`（+18.05 pp）与 `QWen-audio-chat+RAG 19.11→42.48`（+23.37 pp）——
   **冻结核 + prompt 注入 + R2 主载体**，带 no-injection 参照臂，是该合同「净负」侧**载体最贴、幅度最大**的实例。
   同时本篇提供该合同**登记假设的最强单篇证据**：同上下文、同骨干、仅差 LoRA → 42.48 vs 13.37。
   **成对声明的另一侧（Siskos「数量补质量」）仍须同时出现。**
2. **†注须从「两线」改写为「三线三分」**（§7 表），并把 R2 的 delta 措辞收窄为「门控选择性 + TF + API-only 的重解析」。
   同时须新增一句：**本篇的 length-filter 是推理期外显否决的弱先例**，故 R2 的 delta 不是「首次加外显阈值」而是「门控信号读信息价值且可标定」。
3. **incumbent 分组合同**：建议在 ⑤retrieval-GER 组内钉入本篇变体 A-FT（Mistral-FT + RAG），
   在 ④trained 上界组内钉入变体 B（音频接地重解码）——**后者是读集内唯一「同载体 + 同上下文层 + 回音频」的 trained 对手**，
   但须同时声明：**无代码/无检查点/阈值未报 → 不可运行，属结构参考档，不入可运行组**（与 Huang24f 同处置）。

---

## 10. 2026 重审条款（预置）

**承重前提（2025 年成立）**：
- **P1**：冻结的音频 LLM 无法在 prompt 里安全消费检回的真实文档上下文——注入即崩（19.11→42.48）。
- **P2**：让核能用上下文的唯一办法是**在该上下文分布上训练它**（LoRA / joiner）。
- **P3**：把首遍 ASR 假设喂回去做重解码，其价值远大于检回上下文（E21 上约 14 倍）。
- **P4**：真实（噪声）上下文与结构化（Europarl）上下文对系统的要求不同——前者会击穿纯文本纠错路线。

**逐条重审命题（Stage-2A 复现先行；每条给可证伪形式）**：

1. **RC-1（对 P1，本篇最直接的重审位，也是 R2 路线的存活检验）**：
   在 2026 冻结 omni 核上重跑「裸核 vs 裸核+无条件注入同一 ConEC 上下文」两臂。
   **证伪形式**：若 2026 核在无条件注入下**不再**出现总 WER 剧烈退化（如退化 < 2 pp），
   则 P1 在 2026 已失效——**R2 门控准入的必要性论证随之从「必要项」降回「优化项」**，K-Gate 的效应量预期须下调。
   反之若仍崩，则本篇的 +23.37 pp 是 R2 机制必要性的现成外部锚。
2. **RC-2（对 P2，R2 与本篇的正面对决）**：R2 的门控准入能否在**不训练核**的前提下，
   把无条件注入的退化压到与本篇 LoRA 适配同量级？**证伪形式**：若门控臂在 Earnings21 总 WER 上仍显著劣于「不注入」参照臂，
   则「门控可替代适配」不成立，R2 在本载体上的 API-only 路线被证伪（对应 K-Gate / K-NB 出口）。
3. **RC-3（对 P3）**：在**对称训练/对称提示**条件下重测「带首遍假设 vs 不带」的差分。
   本篇的 4.72 pp 与训练/推理失配混杂（论文自认 mismatch）。
   **证伪形式**：若对称条件下差分收缩到与检回上下文同量级（< 1 pp），则「先前假设是重解析的主要价值来源」这一前提不成立，
   R2 的重解析设计应改为条件化单次（Wang 形态）。
4. **RC-4（对 P4，与 ConEC RC-1 耦合）**：本篇已用 320 字符**文本块**（而非 ConEC 基线的 bag-of-unigrams）注入，
   即 ConEC RC-1 的「非词袋上下文」实验位**已被部分占据**——占据形态为 **trained + 块检索 + top-4**，
   **仍未被占据的是**：training-free、API-only、以及**整段原始文档注入**（本篇最大也只到 1000 字符块且未报 WER）。
   **证伪形式**：若在 2026 长上下文核上「整段 slides/财报稿注入」不优于「320 字符 top-4 块检索」，
   则「结构化上下文」分量应下调，R2 的注入形态回退到块检索。
   **本条须回写 ConEC 条目 §9 RC-1**——该重审位不再是完全空格。
5. **RC-5（覆盖—命中—效果三级归因，建议升格为通用程序）**：
   本篇给出 `上下文覆盖上界 69.02 → 实际命中 42.08 → WER` 三级链条。
   **建议写进 R2 §7 判别力条款**：任何「没赢」的读数，必须先在这三级上定位，否则归因不可判。
6. **RC-6（遗留核对义务，非模型命题）**：有网络时须完成三项：
   ①以 IEEE Xplore 记录核 venue/DOI/页码（本地 OA PDF 无 venue 自证）；
   ②核实是否存在代码/检查点发布（本篇正文未给任何仓库指针）；
   ③核 Whisper 型号——若作者在后续版本/海报中披露，本篇与 ConEC 的 2.94 pp 裂口可少一个混淆项。

---

## 11. 深读后新增的、R2 应该知道的事实

1. **R2 主载体上已存在第二评测者，且其参考口径与 ConEC 不同**。本篇循 ConEC 划分与上下文库，
   但**明说未获修订转写、用原始参考**，且换了归一化方式、换了稀有词定义、未报 Whisper 型号。
   **裂口读数 10.92 vs 7.98（2.94 pp）是「跨篇拼接 Earnings21 数字必然出错」的一手实证。**
   → **R2 的 reference 双报决策由此从「保守」升为「必需」**：两条谱系（ConEC 修订版 / 本篇原始版）各有已发表锚点，
   只报一列即断掉另一条对照链。**双报表须同时冻结评分栈列**，否则双报仍不可比。
2. **冻结核 + 无条件注入在 R2 主载体上是灾难级净负，且带 no-injection 参照臂**：
   Whisper+CV 10.92→28.97、QWen-audio-chat+RAG 19.11→42.48。**这是读集内载体最贴、幅度最大的一格。**
3. **「噪声耐受属于核的训练分布」这一登记假设，本篇给出了单篇内最干净的证据**：
   同上下文、同骨干、同输入格式，仅差 LoRA → 42.48（冻结）vs 13.37（适配）；
   而无上下文时同一适配只值 4.90 pp。**24.21 pp 的适配收益专门用于抗注入——这正是 R2 门控要接手的职责量。**
4. **总 WER 与实体/稀有词指标在无条件注入下符号可以相反**（row 3→4：WER ×2.22 恶化、F1 +0.12 改善）。
   → **R2 若只报实体 F1，会把灾难读成胜利。** 与 ConEC 把总 WER 降为 `READOUT_ONLY` 的决定**并不矛盾**——
   正确口径是：**主判据用稀有词/实体 WER，同时把总 WER 作为强制的"不退化"守卫指标报出**（非主判据，但不得省略）。
5. **无条件检索普遍带总 WER 税，且训练只能压低税率不能消除**：12 个对照中 6 个总 WER 净负；
   即便是在该上下文分布上训练过的混合系统，叠加 RAG 仍付 +0.48 pp（论文自归因为检回上下文的噪声）。
   **这是门控相对「再训练」的存活位。**
6. **检索损失比查询质量损失大约 20 倍**（26.94 pp vs 1.28 pp）。**这是对 R2「用重听改善检索 key」分量的反向先验**，
   须写入 §0 具名反向先验并带限定：hit-rate 为检索侧代理指标；本载体为逐场小库 + 语义检索，
   未必外推到大库或声学 key 设定。**同时它给 R2 指了更值钱的方向：检索表示/深度 > 查询精修。**
7. **首遍假设的贡献远大于检回上下文（E21 约 14 倍）**，但该读数与训练/推理失配混杂，**是上界不是估计**。
   若在对称条件下仍成立，则 R2 的「重解析」价值主要来自**先前假设的再呈现**而非**新证据**——
   这会把 R2 的机制重心从"取什么"移到"怎么再看"，并直接影响 K1a/K1b 的臂设计。
8. **ConEC RC-1（非词袋上下文）不再是完全空格**：本篇已用 320 字符文本块 + top-4 检索注入，
   **占据形态=trained + 块检索**；未被占据的是 training-free、API-only、整段文档注入。
   **须回写 ConEC 条目 §9 RC-1 的空格声明。**
9. **多源互补性在本载体上首次有了覆盖率级读数**（CV+RAG 54.12 vs RAG-only 42.08，+12.04 pp），
   **但逐源 WER 消融仍是空格**——R2 的「多源**选择**」delta 在本载体上依然未被占据（本篇 row 14 是无条件并用）。
10. **本篇提供了 R2 可直接升格的三级归因程序**：覆盖上界 → 检索命中率 → 任务效果。
    ConEC 给的是「效果侧 oracle headroom」，本篇给的是「证据侧覆盖/命中 headroom」，**两者合起来才能把"没赢"归因到具体环节**。
11. **推理期外显否决的弱先例已存在**（length-filtering：长度偏离即弃 LLM 假设、回退首遍）。
    **R2 措辞须收窄**：delta 不是「首次给重解析加外显阈值」，而是「阈值读的是可标定的信息价值/感知不确定性，而非与信息无关的健全性代理」。
12. **本篇不可运行**：无代码、无检查点、length-filter 阈值未量化、Whisper 型号未报、F1 定义未给、稀有词阈值未报值。
    → **只能作结构参考档与反向读数来源，不得入可运行对手组。**
