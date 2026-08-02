---
artifact_id: "SF-STAGE1C-D2-ERNBEST-INTERSPEECH2021.WANG21B"
arxiv_id: "none (ISCA Archive interspeech_2021.wang21b；DOI 10.21437/Interspeech.2021-1370)"
title: "Leveraging ASR N-best in Deep Entity Retrieval"
authors: "Haoyu Wang¹, John Chen²†, Majid Laali³, Kevin Durda³, Jeff King³, William Campbell¹, Yang Liu¹（¹ Amazon Alexa, USA；² University of Toronto, Canada；³ Amazon Alexa, Canada；† = \"Work done during internship at Amazon Alexa, Canada\"，p1/261 脚注）。**PDF `/Author` 元数据与正文排版署名逐字一致**（七名、同序、同拼写）。联系邮箱 `{wanhaoyu, laalim, durdak, jfkin, cmpw, yangliud}@amazon.com`（六个别名对应六位 Amazon 作者）、`johnc@cs.toronto.edu`。**全篇无通讯作者标记、无 ORCID、无致谢节**"
venue: "INTERSPEECH 2021（页首压印逐字：\"INTERSPEECH 2021 / 30 August – 3 September, 2021, Brno, Czechia\"，p1 y≈22–47；页脚逐字：\"Copyright © 2021 ISCA\" · 页码 \"261\" · \"http://dx.doi.org/10.21437/Interspeech.2021-1370\"，p1 y≈811）；会议分场 = \"Spoken Dialogue Systems I\"（PDF `/Subject` 元数据，正文未印）；刊页 **261–265**；**无 arXiv 版**（ledger `access_class` 为 ISCA_ARCHIVE_ID_DEREFERENCE，非 arXiv 通道；本次零网络会话不可独立复核，见 §1 证据等级声明）。**页面无任何 CC 许可行**——ISCA 版权声明是全部许可信息"
date: "2026-08-02"
read_level: "D2_DEEP_READ"
reader: "opus-agent"
status: "DRAFT_FOR_R2_INTEGRATION"
source_of_record: "**官方 ISCA Archive PDF 唯一源**（`/Creator Causal Productions Pty Ltd`＝ISCA 御用排版商、`/Producer Acrobat Distiller 10.1.9 (Windows)`、`/PTEX.Fullbanner pdfTeX 3.14159265-2.6-1.40.21 (TeX Live 2020)`、`/CreationDate D:20210901112254+09'30'`、`/ModDate D:20210901161156+09'30'`〔+09'30' = 澳洲阿德莱德时区，与 Causal Productions 所在地自洽〕、`/Keywords [Electronic Manuscript]`、`/Title Leveraging ASR N-Best in Deep Entity Retrieval`〔元数据写 \"N-Best\"、正文写 \"N-best\"，大小写不一致〕、A4 595.22×842pt、5 页）。**证据等级须降一档并写明**：本篇无 arXiv 版故**无 eprint LaTeX 源可取**，全部数字取自 PDF 内部对象（`pypdf` 文本层 + `pymupdf` 向量路径 + 高倍渲染目视），并与页码标记行交叉核对——这与读集内基于 `.eprint` 源文本的条目**不是同一证据等级**。三处渲染特有风险已在 §1 逐条声明：①图内文字使用 Identity-H 编码的 Calibri/CambriaMath 子集且**既无 `/ToUnicode` 也无 `cmap` 表**，文本层完全不可读，Figure 1/2 的全部标签系"高倍渲染目视 + 字符计数独立校验"两路得出；②Figure 2 的曲线数值**论文未印任何数字**，本件由 PDF 向量路径坐标 + 坐标轴刻度标定反算，方法与残差见 §6.3；③`pypdf` 在部分字体上插入伪空格（\"V arious\"、\"ash M = h1\"、\"asM =\"），引用时按 §1 声明 4 规则归一"
local_evidence:
  - "E:/chao_workspace/exploring-l4-intelligence/speechrl-data/survey-fulltext/interspeech_2021.wang21b/interspeech_2021.wang21b.pdf sha256 e892af9e18214d2c9ad807d84871654597eabffc8781abf2134cb8df22d6a10c，271267 bytes，**5 页**（`pypdf` 计数；对应刊页 261–265，其中正文 4 页 261–264、参考文献 1 页 265，**无附录**）（与 ledger 第 1455 行逐字节一致，本次复算通过）"
ledger_ref: "wiki/survey/2026-07-17-sf-fulltext-ledger.jsonl **第 1455 行**；本 id 仅此一行，kind=pdf，**无 eprint 行**（ISCA 通道，符合任务下达口径）"
prior_status: "本篇被登记为"语音实体检索/链接"谱系锚点候选，并被标注为"评测了域外拒识"（admission-adjacent）；此前 R2 读集零出现；首次 D2 全文深读"
exposure: "零网络请求（本会话未发起任何 fetch/search/WebFetch/WebSearch）；只读本地件——本篇 PDF、ledger 第 1455 行、D2 体例模板件（`2026-08-01-d2-2024-lrec-main-1365.md` 全文）；sha256 本次以 Python `hashlib` 流式复算；PDF 文本抽取产物、图像渲染件、向量坐标转储只写入会话 scratchpad，未写入仓库；零模型调用、零指标运行、零数据集下载、零 GPU；**本次未获取任何被引文献（含 [3]/[15] Li et al. 2020、[4] Raghuvanshi et al. 2019、[5] Wang et al. 2020、[18] Agarwal & Bikel 2020），凡涉及被引文献内容的陈述一律标为未本地复核**"
supersedes: "无（新建）"
---

# D2 深读：Leveraging ASR N-best in Deep Entity Retrieval (interspeech_2021.wang21b)

## 1. 来源核对

**ledger 逐行引用**（`wiki/survey/2026-07-17-sf-fulltext-ledger.jsonl` 第 1455 行，逐字）：

> `{"arxiv_id": "interspeech_2021.wang21b", "kind": "pdf", "url": "https://www.isca-archive.org/interspeech_2021/wang21b_interspeech.pdf", "time_utc": "2026-08-02T15:41:37Z", "http_status": 200, "attempts": 1, "bytes": 271267, "sha256": "e892af9e18214d2c9ad807d84871654597eabffc8781abf2134cb8df22d6a10c", "error": null, "stored_at": "E:/chao_workspace/exploring-l4-intelligence/speechrl-data/survey-fulltext/interspeech_2021.wang21b/interspeech_2021.wang21b.pdf", "access_class": "ISCA_ARCHIVE_ID_DEREFERENCE/FULLTEXT_FETCH"}`

本次以 Python `hashlib.sha256` 流式复算落盘件得 `e892af9e18214d2c9ad807d84871654597eabffc8781abf2134cb8df22d6a10c`，
**与 ledger 逐字节一致**；落盘字节数 `271267` 亦一致。
`access_class` 为 `ISCA_ARCHIVE_ID_DEREFERENCE`（非 arXiv 通道），与"无 arXiv 版"自洽但不构成独立证明。

**页数与页序核定**（`pypdf` 页计数 + 页脚页码位置）：**5 页**，刊页 261–265。逐页归属：

| PDF 页 | 刊页 | 内容 |
|---|---|---|
| 1 | 261 | 页首 ISCA 压印、标题/七位署名/三机构、Abstract、Index Terms、§1 Introduction、§2 Related Work（起）、脚注 †、页脚 ISCA 版权+页码+DOI |
| 2 | 262 | **Figure 1（双编码器架构图，跨双栏置顶）**、§2 末句、§3 Proposed Method（任务形式化）、§3.1 Text Encoding、§3.2 Mention Representation Aggregation（五个 bullet）、**Eq. 1** |
| 3 | 263 | **Eq. 2**、§3.3 Score and Threshold、**Eq. 3（拒识判据）**、§4 Dataset、§4.1 Dataset Construction、§4.2 Dataset Processing、§5 Experiments、§5.1 Experiment Setup、§5.2 Baseline、§5.3（起）、**Eq. 4** |
| 4 | 264 | §5.3 续、**Table 1（唯一结果表）**、§5.4 Experiment Results About Thresholds、**Eq. 5**、**Figure 2（阈值扫描曲线）**、§5.5 Discussions、§6 Conclusion |
| 5 | 265 | §7 References [1]–[26] |

→ **无附录、无 Limitations 节、无 Ethical/Broader-Impact 节、无致谢节、无代码/数据链接**。
全部承重事实只能取自 4 页正文；**任何"附录里有"的预期都不成立**。

**表图序核定**（按题注逐字）：
Table 1 = "Experiment results for the in-domain data. The Relative Error Reduction for a model m is calculated by comparing the relative difference between (100% − Accuracy_m) and (100% − Accuracy_baseline)."（p4/264，**全篇唯一表**）；
Figure 1 = "Dual encoder architecture for ASR N-best ER model. All ASR N-best mentions will be aggregated into a single representation. Each candidate entity will be encoded individually and the score will be calculated by a dot product with ASR N-best representation."（p2/262）；
Figure 2 = "Relative Error Reduction when varying threshold θ."（p4/264）。
公式共 **5 条**（Eq. 1–5）。参考文献 **26 条**。

**证据等级声明（承重，四条）**：

1. **无 eprint 源**。本篇与读集内 `2024.lrec-main.1365` / `2024.lrec-main.328` 同属"只有官方渲染 PDF"的一档，
   数字**不可逐字符验证**，只能验渲染。所有引自 Table 1 / Figure 2 的数字在升为 R2 承重引用前，须有网络时对官方 PDF 二次目视核对。
2. **图内文字在文本层完全不可读，本件另辟两路取证**。Figure 1/2 使用 `BPNO*/BPNP*+Calibri`、`Calibri-Bold`、`CambriaMath` 的 TrueType 子集，
   PDF 字典为 `<</Subtype/Type0/Encoding/Identity-H>>` 且**无 `/ToUnicode`**，嵌入字体表为 `['cvt ','fpgm','glyf','head','hhea','hmtx','loca','maxp','name','prep']`——**无 `cmap` 表**。
   故 glyph ID 无法映射回 Unicode，`pypdf`/`pdftotext` 在图区只吐空白与乱码。
   本件取证两路并行：**(甲)** 以 `pymupdf` 5–6 倍渲染后目视读出标签；**(乙)** 以 `rawdict` 取每个 span 的 `nchars` 与 bbox，
   用字符计数独立校验目视结果。校验全部命中：右轴七标签 nchars = `4,1,3,3,3,3,3` ⇔ `-0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5`；
   左轴八标签 nchars = `1,4,4,4,4,3,4,4` ⇔ `0, 0.02, 0.04, 0.06, 0.08, 0.1, 0.12, 0.14`；
   横轴九标签 nchars 全 = `3` ⇔ `0.1 … 0.9`；纵轴标题 nchars = `23`/`27` ⇔ `In-domain Accuracy RErr` / `Out-of-domain Accuracy RErr`；
   图例 nchars = `29`/`32` ⇔ `Self-Attention In-domain RErr` / `Sel-Attention Out-of-domain RErr`。
   → **图例第二行的 `Sel-Attention` 是原文拼写错误**（13 字符，非 14），由 nchars 独立证实，非渲染误读。
3. **Figure 2 的曲线值论文未印，本件为向量反算**。见 §6.3 的完整方法、标定残差与不确定度；该节全部数值**标为本件派生、非论文报数**。
4. **引用归一规则**。本件所有 `>` 引用按以下规则归一并声明：①连字 `ﬁ/ﬂ` 还原为 `fi/fl`；②`pypdf` 伪空格（如 `V arious`→`Various`、`ash M = h1`→`as h_M = h_1`、`asM =`→`as M =`）还原；③跨行连字符断词（`learn-able`→`learnable`）合并；④**原文错别与重复词照录不改**（如 §5.3 的 `comparing to the the learnable weights approach`、图例的 `Sel-Attention`）。
   数学下标在纯文本引用中写作 `h_M`、`h_ci`、`α_i` 等，与排版体 `hM`、`h^{c_i}` 对应。

---

## 2. 任务定义与形式化

### 2.1 任务形式化（§3，p2/262，逐字）

> "To formalize the task of ER, we define a query as m = {t_1, t_2, ..., t_N} where t_i is the i-th token after applying tokenization on the entity mention in the user utterance. The task of ER is to retrieve a proper entity from a catalog defined as C = {c_1, c_2, ..., c_K}, **or reject the query as out of domain input**. A given catalog entity c_i can be presented as c_i = {t_1, t_2, ..., t_M}. To solve the problem of ER, we design a model to learn the score (similarity) between a given pair as s(m, c_i) ∈ [0,1], and then **pick the top-1 ranked c_i as the result or reject the query if the top score is below a threshold θ**."

N-best 化之后的目标（§3，p2/262，逐字）：

> "As we aim to leverage ASR N-best information to improve the robustness of ER against ASR errors, we will expect a list of mentions available as M = {m_1, m_2, ..., m_L} from ASR N-best. These can be easily obtained by **aligning ASR hypotheses and mapping the entity mention in the top hypothesis to others, or performing NER on each hypothesis**. The goal of our model is thus to learn the score (similarity) between **a list of mentions and an entity candidate** c_i, s({m_1, m_2, ..., m_L}, c_i) ∈ [0,1]."

**形式定义层面的四项要点**：

- **查询单元是 mention，不是 utterance**。`m` 定义为"对 user utterance 中的 **entity mention** 分词后的 token 串"。
  整句话在 ER 阶段不可见——上游 NLU 的 NER 已经把 slot 切出来了。
  → 本篇的"上下文"只有 mention 本身；**无句级上下文、无对话历史、无 utterance 级特征**。
  这与读集内 TED-EL 的消歧输入 `ctx_l [M] men [\M] ctx_r`（左右上下文进编码器）**不同型**。
- **拒识写进了任务定义本身**（"or reject the query as out of domain input"），不是事后补丁。
- **打分空间是 s(·) ∈ [0,1]**，且拒识判据挂在这个分数上。
- **N-best 化后签名从 s(m, c) 变成 s({m_1..m_L}, c)**——即**多假设 → 单实体**的多对一打分，
  **不是**"多假设 → 多结果 → 选一个"的选择型结构。这一点在 §3 的签名里就已经定死，是本篇最承重的结构事实（详见 §4.3、§9 字段 5）。

### 2.2 任务身份：ER（检索）而非 EL（链接）

本篇自称 **Entity Retrieval (ER)**，目标是"retrieves entities in a **catalog** for the entity mentions in user utterances"（Abstract, p1/261）。
与 Entity Linking 的关系由论文自己给出（§3, p2/262，逐字）：

> "Although different neural network architectures have been proposed for **entity retrieval and linking** [16, 17, 18], in this work we follow the commonly used **dual encoder neural network architecture in [18]**."

其中 [18] = "Entity linking via dual and cross-attention encoders"（Agarwal & Bikel, 2020, arXiv:2004.03555，p5/265）。
→ **架构谱系承自文本 EL，任务身份是面向私有目录的 ER**。二者在本篇被明确区分但共用骨架。
（[16]/[17]/[18] 三件本次零网络未取，其内容一律未本地复核。）

### 2.3 应用场景（§1, p1/261，逐字）

> "Consider a speech-based virtual assistant that helps users control smart home appliances. For an utterance **turn on the den room light**, NER labels **den room light** as Appliance, and then ER takes this as a query and links to an entity in the catalog inventory, returning the most relevant smart light. Since "den" is a rare word, ASR may mistranscribe "den" as "dining", and the ER system in turn may end up **retrieving nothing or an irrelevant entity** from the catalog, adversely affecting the customer experience."

→ 场景 = 智能家居设备控制；实体 = 用户自命名的设备；失败模式 = ASR 把稀有词/自定义名转错。

---

## 3. 机制：ASR N-best 如何进入实体检索【**R2 问题 1 答复**】

**一句话答复**：N-best 以"**每条假设各出一个 mention 串 → 各自编码成向量 → 在查询侧被聚合成单一查询向量**"的方式进入检索；
聚合有五种做法，最好的是 self-attention；聚合之后与目录实体做点积打分。
**融合发生在查询编码阶段（query encoding phase），既不是重排、也不是选择、也不是纠错。**

### 3.1 从 N-best 到 mention 列表（§4.2 Dataset Processing，p3/263，逐字）

> "For each utterance, we obtain and process the ASR N-best hypotheses by **aligning additional ASR N-best hypotheses to ASR 1-best hypothesis token-by-token using Levenshtein approach** [24]. Based on the alignment, we can then **infer the alternative mentions in other ASR hypotheses based on the mention in the 1-best hypothesis**. Note that this string alignment is a much more computationally efficient method compared to running NER on every hypothesis. After this processing, for each utterance we have a **maximum of 5 mentions (this is because of the beam search limit in the ASR decoder)**. It is worth noting that the mentions may be the same in different ASR hypotheses. **We keep these duplicates as is** since we believe this is a valuable information for the model to learn how to weigh each ASR hypothesis."

**四项承重读数**：

1. **mention 边界由 1-best 单方面决定**。NER 只在 1-best 上跑一次，其余假设的 mention 是**通过 Levenshtein 对齐投影**过去的。
   → 若 1-best 的 mention **边界**错了（而不只是词错了），投影会把错误边界传播到全部 L 条假设。
   论文给了备选方案（"or performing NER on each hypothesis"，§3, p2/262）但**明确未采用**，理由是算力。**该权衡未被实验量化。**
2. **L ≤ 5，且上限来自 ASR 解码器的 beam 宽**——即 N-best 的规模不是本篇的可调超参，而是上游 ASR 的既定约束。
   **N 的消融（L=1,2,3,4,5 的效用曲线）全篇不存在。**
3. **重复 mention 被保留**。作者的理由是"让模型学会给每条假设加权"——
   即重复度本身被当作隐式置信度信号。**该假说全篇无消融验证。**
4. **对齐方法是纯字符串级 Levenshtein**，无音素、无声学、无 ASR 后验分。

### 3.2 文本编码（§3.1，p2/262，逐字）

> "While there have been multiple different approaches proposed for text encoding, we choose to follow the simple yet powerful approach of **embedding pooling** [21, p. 106]. While our approach can also be applied on other advanced text encoders, we do not focus on that in our study. For a given token t_i, we first conduct an **embedding look up** as h_{t_i} ∈ R^d. Hence for a given sequence of tokens t = {t_1, t_2, ..., t_N}, we can obtain emb({t_1, t_2, ..., t_N}) = {h_{t_1}, h_{t_2}, ..., h_{t_N}} ∈ R^{N×d}. We further conduct an **average over the N embeddings** to get the text-level representation as h_t = 1/N × Σ_1^N h_{t_i}."

> "This encoding approach can be applied to **both the query and the candidate entity**, using either shared embedding or separately learned embedding, resulting in h_{m_i} and h_{c_j} respectively."

→ **编码器 = 查表 + 平均池化**。**全篇零预训练模型、零 Transformer 编码器、零语言模型**。
唯一的 Transformer 组件是聚合层的 self-attention（Eq. 1–2），且它作用在**假设之间**而非 token 之间。
`d = 128`（§5.1, p3/263）；查询侧与候选侧**不共享 embedding**（§5.1 逐字："We do not share the embeddings between the mention encoder and candidate encoder."）。

### 3.3 五种聚合方式（§3.2，p2/262，逐字全录）

聚合的对象是 L 个 mention 表示 `h_{m_i}`，产物是单一查询表示 `h_M`。

| # | 方法 | 逐字定义 | 权重是否依赖输入 | 新增可学习参数 |
|---|---|---|---|---|
| 1 | **Pooling** | > "One straight forward way of computing h_M is to conduct an **average pooling** of h_{m_i} as h_M = 1/L × Σ_1^L h_{m_i}." | 否（等权） | **0** |
| 2 | **Learned Weighted Combination** | > "Since hypotheses have different likelihoods (or confidence score), we introduce **L learnable parameters** defined as α_i ∈ [0,1] (i ∈ {1,2,...,L}) to weigh each representation or hypothesis. Then we compute the query representation as h_M = Σ_1^L α_i × h_{m_i}." | **否**（只依赖 rank 位次） | L |
| 3 | **Global Attention** | > "Rather than using a set of global weights that are only dependent on the **rank** of a particular hypothesis on the n-best list, we propose to learn weights dependent on the **representation** of each ASR N-best hypothesis. In light of work [22], we introduce a learnable **context vector c ∈ R^d** that is used to attend to each mention's representation to calculate the weighted score as **α_i = c · h_{m_i}**. After obtaining these weights, we follow the same weighted averaging approach to compute h_M." | **是** | d |
| 4 | **Concatenated Projection** | > "first **concatenate** all the representations h_{m_i} as h_concat = [h_{m_1}, h_{m_2}, ..., h_{m_L}], then apply a **dense layer** to project it back to the model dimension as h_M = W h_concat, where **W ∈ R^{Ld×d}**." | 是（隐式） | L·d² |
| 5 | **Self-Attention** | > "In this work, we propose to apply **self-attention mechanism** [23] to aggregate all the mention representations. Using the L representations H = [h_{m_1}; h_{m_2}; ...; h_{m_L}], we first compute the self-attention scores A ∈ [0,1]^{L×L} by: **A = softmax((QH)(KH)^T / √d)** (1) … We then compute a new sequence of representations Ĥ = [ĥ_{m_1}; ĥ_{m_2}; ...; ĥ_{m_L}] by: **Ĥ = AVH** (2) … After this we can again follow the pooling approach to average all the representations ĥ_{m_i} as h_M = 1/L × Σ_1^L ĥ_{m_i}." | **是** | 3d² |

作者对 self-attention 的预期（§3.2 末，p2/262，逐字）：

> "Since the newly introduced parameters can help learn a proper relation between given mentions h_i and h_j based on the representation themselves to guide the aggregation, we expect this to be more powerful than the aforementioned approaches."

**本件登记的三处形式化缺口**（论文未讨论）：

1. **Eq. 1 / Eq. 2 的维度不自洽**。若按 `H = [h_{m_1}; …; h_{m_L}]` 的列堆叠读法 `H ∈ R^{d×L}`，
   则 `(QH)(KH)^T ∈ R^{d×d}`，与论文声明的 `A ∈ [0,1]^{L×L}` 矛盾；
   若按行堆叠读 `H ∈ R^{L×d}`，则 `QH`（`Q ∈ R^{d×d}`）本身无定义。
   同理 Eq. 2 的 `AVH` 在 `A ∈ R^{L×L}`、`V ∈ R^{d×d}` 下无法左乘成立。
   → **意图清楚（标准缩放点积自注意力，应为 `A = softmax((HQ)(HK)^T/√d)`、`Ĥ = A(HV)`），但排版式子不可直接照抄实现。** 标为 `NOTATION_ILL_FORMED`。
2. **`α_i ∈ [0,1]` 的约束机制未给**（方法 2）。既未说明用 sigmoid、也未说明用 softmax 归一；
   方法 3 的 `α_i = c · h_{m_i}` 是**无界点积**，论文声明的 `[0,1]` 值域同样无机制保障，且**未提归一化**。
3. **变长 L 的处理未给**（方法 4 承重）。`W ∈ R^{Ld×d}` 要求 L 固定，而正文只保证 `L ≤ 5`；
   当某条 utterance 的 N-best 少于 5 条时的 padding/masking 规则**全篇无一字**。
   同理 self-attention 的 padding mask 亦未提。

### 3.4 打分（§3.3，p3/263 + Figure 1，p2/262）

§3 逐字（p2/262）：

> "For the dual encoder model, we first encode the query by an encoder **h_M = f({m_1, m_2, ..., m_L}) ∈ R^d** and then encode the catalog entity by another encoder **h_{c_i} = g(c_i) ∈ R^d**. We then define the score similarity function between h_M and h_{c_i} as their **dot product**. While we could have used other mechanisms that jointly model the two representations [16, 17], we mainly focus on **dual encoder models because they will allow us to scale to search over millions of entities using an efficient k-nearest neighbour search** [19, 20]."

§3.3 逐字（p3/263）：

> "Once we obtain the query representation h_M and a given candidate entity's representation h_{c_i}, we then compute the **dot product** between the two as a raw similarity score. A **softmax function** will then be applied to normalize that into probabilities. For the ER task we would like to optimize the model to assign **1 to the correct entity and 0 to the rest of the entities in the catalog**."

**Figure 1 的图内内容**（p2/262，§1 声明 2 的两路取证结果）：
左半：`ASR 1-best = "mark's light"` / `ASR 2-best = "marque's light"` / … / `ASR N-best = "mike light"`，
各自经 token embedding（橙色）→ mention 表示（蓝色）→ 灰框 **"N-best Representation Aggregation"** → **单一绿色表示**；
右半：`Catalog Entity_1 = "Marque's room light"` / … / `Catalog Entity_K = "garage door"`，
各自经 **"Candidate Embedding"** → 候选表示；
顶部：两侧做 **"Dot Product"**（⊙）→ **"Softmax"** → 输出 `0.95 … 0.01`。

→ 图示与正文完全一致，并额外坐实两件事：**(a) 目录实体只有名字串**（"Marque's room light"、"garage door"），无描述、无类型、无属性；
**(b) 聚合是"多进一出"**——图注逐字 > "All ASR N-best mentions will be **aggregated into a single representation**."

### 3.5 机制定性（本件，承重）

| 维度 | 本篇取值 | 反例对照（**非评价**） |
|---|---|---|
| 融合层次 | **表示级（向量）** | 非串级改写、非 lattice/WCN、非 n-gram 特征 |
| 融合位置 | **查询编码阶段**（§1 逐字："during the **query encoding phase** for deep ER systems"） | 非解码期、非重排期、非结果后处理 |
| 融合算子 | 加权平均 / 拼接投影 / 自注意力 | — |
| 输出基数 | **1 个查询向量** | 非 L 个并行查询、非 L 组结果的合并 |
| 假设的去向 | **全部被吸收进单一向量，个体身份消失** | 无"选中第 k 条假设"这一动作 |
| 是否改动 ASR | **否**（只消费其 N-best 输出） | 对照：读集内 TED-EL 的 RBSEL-J2 需改写 ASR 词表并重训 |
| 是否使用 ASR 分数 | **否**（见 §8 字段 3） | 后验/置信度只被当作方法 2 的**动机**，从未作为输入 |

论文对自身机制的定位（§5.5 Discussions，p4/264，逐字）：

> "While it is intuitive to think that the ASR N-best may contain important information to make the representation more robust to ASR errors, it is also a key to **appropriately encode that information** for the model to obtain the maximum benefit. To make the most use of ASR N-best, the model should learn that it can **rely on the ASR 1-best hypothesis for a substantial amount of cases** but also should **learn from alternative hypotheses in the ASR N-best list via proper weighting**."

→ 作者自述的理想行为是"多数情况倚重 1-best、必要时从其他假设吸收"——
但这是**由训练得到的软权重**实现的，**不是逐样本的显式档位切换**。**该行为全篇无验证**（无注意力权重可视化、无"何时偏离 1-best"的案例分析）。

---

## 4. 拒识（rejection）机制的精确定位【**R2 问题 2 答复** — 本节承重】

### 4.1 全部相关原文（逐字，穷举，共五处）

| 出处 | 逐字 |
|---|---|
| Abstract, p1/261 | > "our best model achieves 11.07% relative error reduction **while maintaining the same performance on rejecting out-of-domain ER requests**." |
| §1, p1/261 | > "our proposed method yields 11.07% error reduction for the in-domain ER request, **without degrading performance for out-of-domain ER requests**." |
| §3, p2/262 | > "The task of ER is to retrieve a proper entity from a catalog … **or reject the query as out of domain input**." / > "pick the top-1 ranked c_i as the result or **reject the query if the top score is below a threshold θ**." |
| §3.3, p3/263 | > "Since in a spoken dialog system, one may ask something out of the catalog, **we should ideally reject the query instead of returning something wrong**. To address that, **a tuned threshold θ** can be used to **reject any top-ranked entity which has a score below the threshold**, that is, the final system decision is: [Eq. 3]" |
| §5.4, p4/264 | > "the ER system may receive and should **reject an out-of-domain query** when a user asks something irrelevant to the dialog system. As described in Section 3.3, we apply a threshold θ to **reject a given query if the top-ranked entity's confidence is below that threshold**." |

**Eq. 3（p3/263，逐字，已目视复核渲染）**：

> ŷ = { **argmax_i(h^M · h^{c_i})**  if **softmax(h^M · h^{c_i}) ≥ θ** ;  **−1**  else }   (3)

### 4.2 机制归类（逐条判定，全部可逐字定位）

**判定 1 —— 不是训练出来的分类器。**
拒识没有任何专属参数、专属损失或专属训练数据。训练目标只有一条（§3.3, p3/263）：
> "we would like to optimize the model to assign 1 to the correct entity and 0 to the rest of the entities in the catalog"
训练负例的来源是（§5.1, p3/263）：
> "during training we randomly pick at maximum **10 negative entities from registered devices** to form the negative cases for a given utterance for model training."
→ 负例是**同一用户目录内的错误设备**，**不是域外请求**。
§4.1（p3/263）虽构造了 out-of-domain 数据集，但其用途只出现在 §5.4 的评测里，
**全篇无一句说 OOD 样本进入训练**。→ 登记 `REJECTION_NOT_TRAINED`。

**判定 2 —— 不是请求前置过滤（pre-retrieval request filter）。**
Eq. 3 的判据取自 `softmax(h^M · h^{c_i})`，即**必须先完成检索与打分**才能求值；
且推理期打分覆盖全目录（§5.1, p3/263 逐字："During inference time, we calculate the scores on the **entire set of entities in the catalog** to find the best matched entity."）。
→ 检索**总是执行**，拒识发生在其后。`REJECTION_POSITION = POST_RETRIEVAL`。

**判定 3 —— 是检索分数门（retrieval-score gate），门的对象是 top-1 结果。**
§3.3 的措辞最精确：> "reject any **top-ranked entity** which has a score below the threshold"。
Eq. 3 的两支是"返回 argmax"或"返回 −1"。
→ 被门控的是**唯一一个被检索出来的候选**，产物是"不返回任何实体"。`GATE_OBJECT = TOP1_RETRIEVED_ENTITY`。

**判定 4 —— 门是单一全局常量，非逐样本策略。**
θ 的措辞是 > "a **tuned** threshold θ"（§3.3），且 Figure 2 用同一个 θ 扫描整个数据集（§5.4）。
**全篇无逐样本、逐用户、逐查询自适应的阈值**。`THRESHOLD_POLICY = SINGLE_GLOBAL_CONSTANT`。

**判定 5 —— 门信号来自检索器自身的分数，不是独立判据。**
判据变量是同一个双编码器点积经 softmax 的结果——**无第二模型、无验证器、无外部证据、无一致性检查、无声学线索**。
`ADMISSION_SIGNAL = SELF_SCORE_ONLY`。

### 4.3 对 R2 RQ3 量词面的直接答复（**载荷句**）

R2 的区分是：**证据 ADMISSION**（对检索回来的证据逐件判采纳/不采纳）vs **REQUEST-level 拒识**（在检索之前否掉查询）。
本篇**两者都不完全是**，其精确位置如下：

| R2 构念要素 | 本篇是否具备 | 逐字/结构依据 |
|---|---|---|
| 发生在检索**之后** | **是** | Eq. 3 读 `softmax(h·h)`；§5.1 推理期先扫全目录 |
| 在**请求**层面否掉查询（检索前） | **否**（但论文用请求层措辞） | §3/§5.4 说 "reject the query"、Abstract 说 "rejecting out-of-domain ER **requests**"，而机制上无任何前置过滤器 |
| 对**多件**检索证据逐件裁决 | **否** | 只对 argmax 一件裁决；无候选集层面的采纳/剔除 |
| 裁决依据是证据**内容**（相关性/可信度/冲突） | **否** | 依据是检索器自身的归一化相似度标量 |
| **逐样本**自适应策略 | **否** | θ 为离线调定的全局常量 |
| 多源仲裁 | **否** | 单一目录、单一分数（详见 §7、§9 字段 5） |
| 有"不作答"这一出口 | **是** | Eq. 3 的 `−1` 支 |

→ **本件给 R2 的定性（描述性，不含优劣判断）**：
本篇提供的是**输出侧的弃权闸门（abstention gate on the single top-1 retrieved entity），由检索器自身分数驱动、以单一离线全局阈值实现**；
它在**流水线位置上**位于检索之后（形似证据采纳），但在**裁决粒度、裁决依据、策略自适应性**三项上都不落在 R2 的证据采纳构念内；
它在**语义标签上**被论文写作请求级 OOD 拒识，但**机制上不存在请求级前置判定**。
**R2 引用时必须写作"检索后的 top-1 分数阈值弃权（论文以 OOD 请求拒识之名描述）"，不得写作"证据采纳门"，亦不得写作"请求前置拒识"。**

### 4.4 拒识评测口径（§5.4, p4/264）

**Eq. 5（p4/264，逐字，已目视复核渲染）**：

> Accuracy = Σ_{i=1}^{N_ood} 𝟙(ŷ_i == y_i) / N_ood   (5)
> > "where N_ood is the number of examples in the out-of-domain dataset."

**本件登记的口径缺口两条**：

1. **OOD 的 `y_i` 从未定义**。§5.3（p3/263）把 `y_i` 定义为 > "the **index** of the ground-truth"；
   而 §4.1（p3/263）说 OOD 样本 > "the ground-truth should be **empty**"——空集没有 index。
   Eq. 3 的拒识支输出 `−1`，故只能**隐式推断** OOD 的 `y_i = −1`、从而 Eq. 5 实为**拒识率**。
   **该等式关系论文从未写出。** 标 `OOD_METRIC_IMPLICIT`。
2. **Eq. 3 的量词缺失**。判据写作 `softmax(h^M · h^{c_i}) ≥ θ`，其中 `i` 未被量化（应为 `max_i`）。
   与 argmax 支并读可推出意图，但**式子本身不自足**。

### 4.5 头条数字与拒识闸门在**互斥配置**下测得（**本件核出，论文未提示**）

§5.3（p4/264，逐字）：

> "It is worth noting that ŷ depends on the threshold θ of the model. **We set θ = 0 for this experiment** since the dataset is in-domain (i.e., there exists a ground-truth entity for each utterance), and leave the discussion of varying θ in the next section."

→ **Table 1 的 11.07%（含全部五行）是在 θ = 0、即拒识闸门完全关闭的条件下测得的。**
（θ=0 时 `softmax(·) ≥ 0` 恒真，Eq. 3 的 `−1` 支永不触发。）
而 §5.4 的拒识评测则在 θ ∈ [0.1, 0.9] 上进行。
**"供给腿"（N-best 融合增益）与"闸门腿"（拒识）在本篇从未在同一配置下同时报过一个数。**
两腿的交互只能从 Figure 2 读出——见 §6.3，读数结论是**增益随 θ 上升单调侵蚀**。

---

## 5. 训练态与冻结面【**R2 问题 3 答复**】

### 5.1 逐部件训练态

| 部件 | 规格 | 训练态 | 依据 |
|---|---|---|---|
| SentencePiece 分词器 | vocab **6000** | **在本数据集上训练** | §4.2, p3/263：> "a sentence-piece tokenizer [25] **trained on this dataset** with a vocabulary size of 6000 and use that for all experiments" |
| Query（mention）编码器 | token embedding 查表 + 平均池化，`d = 128` | **训练**（embedding 从头学） | §3.1, p2/262；§5.1, p3/263 |
| Candidate（目录实体）编码器 | 同上，**与查询侧不共享 embedding** | **训练** | §5.1, p3/263：> "We do **not share the embeddings** between the mention encoder and candidate encoder." |
| 聚合层 | 五选一（0 / L / d / Ld² / 3d² 参数） | **训练** | §3.2, p2/262 |
| 阈值 θ | 标量 | **不训练**，离线调定（"a tuned threshold"） | §3.3, p3/263 |
| 上游 ASR | 未指明型号/规模 | **本篇不动它**（只消费其 N-best） | §4.2, p3/263 |
| 上游 NLU（DC/IC/NER） | 未指明 | **本篇不动它**（只消费其 mention 切分） | §1, p1/261；§4.1, p3/263 |

**训练配置逐字**（§5.1, p3/263）：

> "In this work, we use the **same hyper-parameters for all the models**. We set the model dimension **d = 128**. We do not share the embeddings between the mention encoder and candidate encoder. The training is optimized using **Adam** optimizer with a learning rate of **0.001** and batch size of **128**. We set the maximum number of training epochs to be **1000** with an **early stopping strategy based on the development dataset's loss not decreasing for 10 epochs**. We **didn't exhaustively tune the hyper-parameters** of the network architecture as it is not the main focus of the study."

> "Since each user may have registered a different number of smart devices, during training we randomly pick at **maximum 10 negative entities** from registered devices to form the negative cases for a given utterance for model training. **During inference time, we calculate the scores on the entire set of entities in the catalog** to find the best matched entity."

### 5.2 判定（承重）

- **端到端还是级联？—— 级联，且是"上游黑箱 + 下游全训"的级联。**
  完整链路：音频 → ASR（beam search，N-best ≤ 5）→ NLU 的 NER（只在 1-best 上跑）→ Levenshtein 投影得 mention 列表 → 本篇的 ER 模型。
  本篇只训练最后一段；**上游 ASR/NLU 在本篇内不训练、不修改、不联合优化**。
- **训练自由度：ER 侧 100% 训练，零冻结。** 全篇**没有出现 "freeze/frozen" 一词**。
- **零预训练模型。** 全篇无 BERT/BART/wav2vec2/HuBERT 等任何预训练权重；
  embedding 从随机初始化在 750h 私有数据上学起；分词器亦在同一数据上训练。
  → 与读集内 TED-EL（BERT + Wav2vec2-Conformer + HuBERT-large + BART-large）**规模与形态都不同型**。
- **ASR 的接口深度：需要 N-best 列表，不只是 1-best 文本。**
  这是比"1-best 文本 API"更深一层的接口要求，但**浅于**"改写 ASR 词表并重训"（TED-EL RBSEL-J2）或"进 beam 读写分数"（ConEC 浅融合）。
  且 N 的上限（5）由上游 beam 宽决定，本篇**不可自主调节**。
  → 登记 `UPSTREAM_INTERFACE = NBEST_LIST_READ_ONLY (N ≤ 5, beam-capped)`。
- **训练自由度与 R2 的"training-free"构念完全不重叠**：本篇是 target-task 全训练，且训练数据是不可得的私有流量。
  → 登记 `FULL_TARGET_TASK_TRAINING` / `NO_FROZEN_CORE` / `NO_PRETRAINED_MODEL`。
- **划分不可审计**：§5.1 使用 "development dataset" 做早停，而 §4 的数据节**只描述 in-domain / out-of-domain 两个集合，从未定义 train/dev/test 划分**，
  亦未报任何子集规模。→ 登记 `SPLIT_UNREPORTED`（与读集内 TED-EL 的 `SPLIT_UNRESOLVED` 同型，但本篇更彻底：TED-EL 至少报了 train/test 文档数）。

---

## 6. 载体、指标与关键数字【**R2 问题 4 答复**】

### 6.1 载体（§4.1, p3/263）

> "We conduct our experiment on **750 hours of de-identified utterances** that users request to control a smart device. Each utterance contains an appliance name derived by the upstream ASR+NLU components, and ER needs to retrieve the right entity from **that user's registered smart devices**. The ground-truth of the utterance was generated through **user feedback signal and annotation process**."

**in-domain 标注的弱监督启发式（逐字，p3/263）**：

> "For instance, given a user asking "turn on my bedroom light", the "bedroom light" will be identified as an appliance name and sent for ER to get the actual entity from the user's registered devices. If ER returns the correct user-defined entity "My Bedroom Light" and the system receives a **positive feedback**, we consider "My Bedroom Light" as the ground-truth for the query "bedroom light". If a user asks "turn on bedroom light", and ASR accidentally mis-transcribes that into "bathroom light" … ER will fail to retrieve any entity … and the system may receive a **negative feedback signal**. In some cases the user may immediately **repeat or reformulate the query**, and get the right transcription … If both queries happen **consecutively in a short interval**, we will then associate "Bedroom Light" as the ground-truth for the mis-transcribed "bathroom light" in the first utterance. This approach provides us in-domain utterances."

**out-of-domain 的构造（逐字，p3/263）**：

> "We also annotate out-of-domain utterances when **there is no correct entity that can be matched with the given appliance name**, and hence the ground-truth should be **empty**. For example, consider an utterance, "turn off the music", **due to NLU errors**, "the music" has been tagged as an appliance name and passed to ER. Such utterances are collected to form an out-of-domain data set."

**本件登记的载体事实与缺口**：

- **OOD 的成因是上游 NLU 的误标注**，不是用户真的问了目录外的东西。
  即"域外"= **上游把不该送来的东西送来了**，这是一个**流水线内部错误吸收**问题，
  与"知识库里没有这个实体"（TED-EL 的 NULL，5.38%）**不同型**。
- **in-domain 的金标来自反馈信号 + 重述配对启发式**，其中"short interval"的具体时长**未报**；
  该启发式对"用户重述后仍失败"的样本如何处理**未报**；标注者人数、一致性、抽检比例**全部未报**。
- **规模只有一个数：750 小时。**
  `N_id`、`N_ood`、utterance 条数、用户数、每用户设备数、目录规模 K —— **全部未报**。
- **载体不可得**：私有去标识化 Alexa 流量，**无发布、无 URL、无许可声明**。

**目录规模的内部张力（本件核出）**：§3（p2/262）以 > "scale to search over **millions of entities** using an efficient k-nearest neighbour search" 论证选双塔；
而实际检索集是"that user's **registered smart devices**"（§4.1）、训练负例上限 10 件（§5.1）。
→ **"百万级"是设计动机而非本篇的实测设定；真实目录规模 K 全篇未报。** 标 `CATALOG_SIZE_UNREPORTED`。

### 6.2 指标与 Table 1

**指标定义（§5.3, p3/263，逐字）**：

> "Because of the nature of our spoken dialog system application domain, for a given user query there will be **only one relevant entity** in the catalog and all the other entities are not relevant. Hence the most critical metric is the correctness of the top entity that the ER system returns. We thus evaluate different approaches using the **accuracy** of the system, which is essentially the **Precision@1** of a retrieval problem [26], defined as: Accuracy = Σ_{i=1}^{N_id} 𝟙(ŷ_i == y_i) / N_id (4)"

**Table 1（p4/264，逐字照录，已目视复核渲染）**：

| Method | Relative Error reduction (%) |
|---|---|
| Baseline w/o ASR N-best | 0.00 |
| Mean Pooling | 6.02 |
| Learnable Weights | 8.61 |
| Global Attention | 8.57 |
| Concatenation | 8.87 |
| **Self-Attention** | **11.07** |

基线定义（§5.2, p3/263，逐字）：

> "one straight forward baseline is to use the **same text encoding to encode only the mention from ASR top-1 hypothesis** as h_M = h_1."

→ **基线 = 同架构、同编码器、同训练配置，只把 L 从 5 改成 1。** 这是干净的单变量对照（本件确认）。

**Table 1 的三条结构事实（承重）**：

1. **全篇零绝对准确率。** Table 1 只有一列相对误差下降；`Accuracy_baseline` 从未出现。
   由题注给出的定义 `RER = [(100−Acc_base) − (100−Acc_m)] / (100−Acc_base)`，可解出恒等式
   **`Acc_m = Acc_base + RER × (100 − Acc_base)`**——但 `Acc_base` 未知，故 **`Acc_m` 不可复原**。
   本件仅给敏感度演算以示量级（**以下全部为假设值，非论文数**）：

   | 假设 Acc_base | Self-Attention 的 Acc | 误差率 100−Acc |
   |---|---|---|
   | 70% | 73.321% | 30.00 → 26.679 |
   | 80% | 82.214% | 20.00 → 17.786 |
   | 90% | 91.107% | 10.00 → 8.893 |
   | 95% | 95.553% | 5.00 → 4.447 |

   → **R2 不得把 11.07% 转述为任何绝对准确率或绝对提升；本载体无绝对锚。** 标 `NO_ABSOLUTE_NUMBERS`。
2. **零方差、零重复、零显著性检验、零样本量。**
   `N_id` 未报，无种子数、无重复实验、无置信区间、无统计检验。
   而 §5.3（p4/264）逐字用了 > "we notice **significant** relative error reduction, which **proves** the importance of using ASR N-best in ER tasks"——
   **"significant"与"proves"均为修辞用法，无统计学支撑。** 标 `NO_SIGNIFICANCE_TESTING`。
3. **五个变体共用一套超参且未逐变体调优**（§5.1 两句逐字）。这对公平性有利，但意味着变体间排序未做鲁棒性验证。

**本件复算（基线无关的派生量，全部只依赖 Table 1 自身）**：

设各法残余误差比为 `1 − RER`，则可在**不知道 Acc_base** 的前提下算出任意两法之间的进一步相对误差下降：

| 对照 | 残余误差比 | Self-Attention 相对其的进一步相对误差下降 |
|---|---|---|
| vs Mean Pooling | 0.9398 | **5.3735%** |
| vs Learnable Weights | 0.9139 | **2.6918%** |
| vs Global Attention | 0.9143 | **2.7343%** |
| vs Concatenation | 0.9113 | **2.4141%** |

→ **头条 11.07% 中，仅约 2.4% 是"self-attention 相对次优聚合法（Concatenation）"的贡献；
其余部分是"用 N-best"这一动作本身相对 1-best 基线的贡献（Mean Pooling 即已取得 6.02%）。**
换言之：**增益的主体来自"多假设进入查询编码"这一供给动作，而非某种特定的聚合算子。**（本件派生，论文未拆分。）

**Learnable Weights (8.61) 与 Global Attention (8.57) 的差是 0.04 pp，折算成两法之间的相对误差差异仅 0.0437%**（本件复算）。
论文对此的措辞（§5.3, p4/264，逐字，**含原文重复词 "the the"**）：

> "For global attention approach, although more learnable parameters are introduced comparing to **the the** learnable weights approach, it doesn't show much improvement."

→ 严格地说 Global Attention **低于** Learnable Weights（8.57 < 8.61），论文表述为"没有多少提升"而非"下降"。
在无方差报告的条件下，**该 0.04 pp 差异不可判方向**。标 `WITHIN_NOISE_UNRESOLVED`。

**论文对各法的解释（§5.3, p4/264，逐字）**：

> "the **mean pooling** approach performs the worst, since it has no learnable parameters but merely averages representations from different ASR hypotheses."
> "Introducing additional learnable weights … is better than mean pooling, but due to the **limitation of weak linear transformation**, it under-performs the best approach."
> "For the **concatenation** approach, although it has the **highest number of additional parameters** and can theoretically learn such a weighting strategy, it still under-performs the self-attention based approach, potentially due to the **lack of explicit modeling of the importance of each mention**."
> "The best performing approach is the **self-attention** model architecture (a relative error reduction of **11.07%** over the baseline), which enables the model to **dynamically decide the importance of each representation by attending to other representations**."

**本件核对**：Concatenation 参数量 `L·d² = 5 × 128² = 81,920`，Self-Attention 参数量 `3d² = 3 × 128² = 49,152`
（本件按 §3.2 定义与 §5.1 的 `d=128`、§4.2 的 `L ≤ 5` 推算；**论文未报任何参数量**）。
→ 与论文"concatenation 参数最多却更差"的定性一致（81,920 > 49,152）。标为本件派生、可复核。

### 6.3 Figure 2 的数值反算（**本件派生；论文未印任何曲线数值**）

**Figure 2 是全篇唯一的拒识证据，且它不含任何印出的数字。** 本件的取数方法与残差如下。

**方法**：以 `pymupdf.get_drawings()` 取图内向量路径。红/蓝两条曲线各为一个 `fill` 路径（27 个 item），
其"去—回"两遍顶点包夹线心，取中点为数据点。坐标轴用两组基准标定：
左轴以 8 条水平网格线（PDF y = 380.26, 365.85, 351.85, 337.60, 323.35, 309.10, 294.85, 280.78）对应 `0.00 … 0.14`；
右轴以 7 个刻度标签中心（经 −0.16 pt 的标签-网格系统偏移校正）对应 `−0.1 … 0.5`，得 **177.517 pt / 单位**。

**标定残差（校验用）**：左轴 `y = 309.10` 反算得 **0.10014**（真值 0.10，残差 +1.4e−4）；
右轴 `y = 309.11` 反算得 **0.29997**（真值 0.30，残差 −3e−5）。
**横轴校验**：红线九个顶点 x = 364.89, 380.05, 395.25, 410.78, 426.09, 441.34, 456.57, 471.80, 487.24，
与九个刻度标签中心 x = 364.75, 380.04, 395.33, 410.62, 425.91, 441.20, 456.49, 471.77, 487.06 逐点相差 ≤ 0.2 pt
→ **确认曲线恰有 9 个数据点，位于 θ = 0.1 … 0.9。**

**反算结果**：

| θ | In-domain Accuracy RErr（左轴，红） | Out-of-domain Accuracy RErr（右轴，蓝） |
|---|---|---|
| 0.1 | 0.1020 | −0.0134 |
| 0.2 | 0.0919 | −0.0184 |
| 0.3 | 0.0905 | +0.0008 |
| 0.4 | 0.0866 | +0.0274 |
| 0.5 | 0.0767 | −0.0033 |
| 0.6 | 0.0651 | +0.0486 |
| 0.7 | 0.0556 | +0.0599 |
| 0.8 | 0.0500 | +0.0123 |
| 0.9 | 0.0331 | +0.0883 |

**独立交叉验证（承重）**：Table 1 报 θ=0 时 in-domain RErr = **0.1107**；
本件反算 θ=0.1 时 = **0.1020**，落在 θ=0 值之下且趋势连续。
→ **两个独立证据面（表格文本层 / 图形向量层）互相印证，标定可信。**

**三条读数结论（本件派生，论文均未点破）**：

1. **供给增益随拒识闸门收紧而单调侵蚀。** in-domain RErr 从 θ=0 的 0.1107 一路降到 θ=0.9 的 0.0331，
   **θ=0.9 时只剩 θ=0 增益的 29.92%**（本件复算 0.0331 / 0.1107）；θ=0.1→0.9 的落差为 **6.88 pp of RErr**。
   → **N-best 供给的收益与弃权闸门的强度是相互抵消的两腿**，而论文的头条数字取自闸门全关处。
2. **OOD 侧的相对差异确实很小且无趋势。** 蓝线全程落在 **[−0.0184, +0.0883]** 的窄带内，且非单调（θ=0.5、0.8 两处回落）。
   这**支持**论文"maintaining the same performance"的表述；
   但须注意**该带宽是相对量**：θ=0.9 处的 +0.0883 意味着 self-attention 把 OOD 侧的错误相对减少约 8.8%，
   **不是字面意义上的"相同"**。且因 `N_ood` 未报，**该带宽是否在采样噪声内不可判**。
3. **两处涉及"绝对准确率"的正文陈述在 Figure 2 中无对应曲线。** §5.4（p4/264）逐字：
   > "Although we notice **better performance for rejecting out-of-domain cases using a larger threshold** (e.g., θ = 0.9), practically we probably will not choose such a threshold because of the **significant drop of the accuracy for the in-domain dataset**. A proper threshold can be chosen depending on the distribution and the trade-off for the two cases."
   Figure 2 的两条轴都是 **RErr（相对基线的误差下降）**，**不是绝对准确率**。
   故上述"OOD 表现更好""in-domain 准确率显著下降"两句所依据的绝对准确率曲线**并未展示**。
   → 标 `TRADEOFF_CLAIM_UNPLOTTED`：本篇声明的 in-domain/OOD 权衡**在其证据面内不可核**。

**另注（口径不一致）**：§5.4 正文说 > "we observe nearly the same **accuracy curves** for any threshold θ"，
而图轴标签是 `Out-of-domain **Accuracy RErr**`。二者指称对象不同（绝对 vs 相对），论文未区分。

---

## 7. 知识来源与音频可达性【**R2 问题 5 答复**】

### 7.1 知识来源

| 项 | 取值 | 依据 |
|---|---|---|
| 知识源身份 | **用户自己注册的智能设备目录** `C = {c_1, …, c_K}` | §3, p2/262；§4.1, p3/263："retrieve the right entity from **that user's registered smart devices**" |
| 是否通用知识库 | **否**。无 Wikidata/Wikipedia/百科，无任何公共 KB | 全篇无 KB 类词 |
| 实体的表示内容 | **只有名字串**（经 SentencePiece 分词后查表平均） | §4.2, p3/263："we further process the mentions and **each catalog entity's name** with a sentence-piece tokenizer"；Figure 1 图内实体为 `Marque's room light` / `garage door` |
| 是否有实体描述/类型/属性 | **无**。零描述文本、零类型标签、零结构化属性 | 全篇无 description/type 字段 |
| 目录规模 K | **未报** | §6.1 的 `CATALOG_SIZE_UNREPORTED` |
| 目录是否跨样本共享 | **否**，逐用户 | §5.1："each user may have registered a **different number** of smart devices" |
| 知识进入模型的通路 | **被训练的候选编码器内部**（embedding 查表 + 平均），**非 prompt、非上下文拼接** | §3.1, p2/262 |
| 快照/版本 | 不适用（私有动态目录），**未报采集期** | — |
| 源的数目 | **1** | 见 §9 字段 5 |

→ 与读集内 TED-EL 的对照（**仅事实并置**）：TED-EL 检索的是 Wikidata 主命名空间全体实体，
且 > "des is the entity description provided by the knowledge base" 进入编码器；
**本篇的"知识"只有一串用户自定义设备名，无任何描述性文本可供消歧。**

### 7.2 音频可达性（**承重**）

**判定：检索侧完全触不到音频，且连 ASR 的分数也触不到。** 三条依据：

1. **架构上无音频通路**。Figure 1（p2/262）的左侧入口就是文本 token（`mark's light` / `marque's light` / `mike light`），
   波形、频谱、声学表示、音素在图中与正文中**均不出现**。
   全篇的输入形式化 `m = {t_1, …, t_N}`（§3）从一开始就是 token 串。
2. **N-best 的处理是纯字符串级**。§4.2（p3/263）逐字："aligning additional ASR N-best hypotheses to ASR 1-best hypothesis **token-by-token using Levenshtein approach**"——
   Levenshtein 是编辑距离，**无音素、无发音词典、无声学相似度**。
   论文在 §2（p1/261）明确把"引入音素特征"归给他人工作：
   > "[4] tried to recover ASR errors for ER by introducing **phonetic features** during the search phase."
   → **本篇未采用该路线**（[4] 本次未取，其内容未本地复核）。
3. **ASR 的后验/置信度分数从未作为输入**。这一点极易被误读，须逐字定位：
   §3.2（p2/262）在介绍 Learnable Weights 时写：
   > "Since hypotheses have **different likelihoods (or confidence score)**, we introduce L learnable parameters defined as α_i ∈ [0,1] … to weigh each representation or hypothesis."
   → likelihood 只是**引入按位次的可学习权重的动机**；
   **模型实际收到的是 L 个 mention 字符串，权重由训练学出（方法 2 依位次、方法 3/5 依表示），ASR 自己的分数从未进入任何式子。**
   Eq. 1–3 中不含任何 ASR 分数项。

→ 登记 `NO_AUDIO_ACCESS`（检索侧零声学）+ `NO_PHONETIC_FEATURES` + `NO_ASR_SCORE_ACCESS`（连解码器置信度都被丢弃）。
**本篇从上游 ASR 只保留了"N 条字符串"这一条最窄的信息带宽。**

---

## 8. 自述局限与场地事实【**R2 问题 6 答复**】

### 8.1 自述局限（**全篇无 Limitations 节**，本节为穷举）

本篇**没有 Limitations 节、没有 Ethical Considerations 节、没有 Broader Impact 节**（§1 页序核定，5 页无附录）。
全部可归为作者自认局限的表述只有三处，且都是"本研究不聚焦于此"式的范围声明：

| 出处 | 逐字 | 性质 |
|---|---|---|
| §3.1, p2/262 | > "While our approach can also be applied on **other advanced text encoders**, we do not focus on that in our study." | 范围声明（编码器未探索） |
| §5.1, p3/263 | > "We **didn't exhaustively tune the hyper-parameters** of the network architecture as it is not the main focus of the study." | 范围声明（调参不完全） |
| §5.4, p4/264 | > "practically we probably will not choose such a threshold because of the **significant drop of the accuracy for the in-domain dataset**. A proper threshold can be chosen depending on the distribution and the trade-off for the two cases." | 权衡自述（阈值需按分布定，未给选法） |

§6 Conclusion（p4/264）以外推陈述收尾，**无 future work、无 limitation**：

> "Our approach to aggregate the representations from ASR N-best can be applied to **other retrieval and ranking models for ER or general encoders for other NLU downstream tasks**."

→ **该外推主张（可迁移到其他检索/排序模型与其他 NLU 下游任务）在本篇零实验支撑**，只在单一 ER 任务、单一私有载体上验证过。

### 8.2 论文未自认、本件核出的局限（须区分标注为本件发现）

1. **绝对准确率全篇缺席** → 头条数字不可转成绝对量，无跨工作可比锚（§6.2）。
2. **头条数字在 θ=0 测得，与拒识闸门互斥**；两腿的联合效用在 Figure 2 中呈单调侵蚀（§4.5、§6.3）。
3. **拒识的"绝对水平"从未报**——只报了 self-attention 相对基线的 RErr，
   **"这个系统到底能拒掉多少 OOD"这一问题在本篇无答案**（§6.3 结论 3）。
4. **零方差/零重复/零显著性检验/零样本量**，却使用 "significant"、"proves"（§6.2）。
5. **N-best 规模无消融**：L 固定为 ≤5 且由上游 beam 宽决定，`L=2,3,4` 的效用曲线不存在（§3.1）。
6. **变长 L 的 padding/masking 规则未给**，而 Concatenation 的 `W ∈ R^{Ld×d}` 强制要求定长（§3.3 缺口 3）。
7. **Eq. 1/Eq. 2 维度不自洽、Eq. 3 量词缺失、Eq. 5 的 `y_i` 对 OOD 未定义**（§3.3、§4.4）。
8. **train/dev/test 划分从未定义**，而 dev 被用于早停（§5.2）。
9. **目录规模 K 未报**，且"百万级实体"是动机而非实测设定（§6.1）。
10. **效率主张全为定性**：Levenshtein 投影"更省算力"、双塔"可扩展到百万实体"——**零延迟/吞吐/内存测量**（§3.1、§3.4）。
11. **§5.5 声称的理想行为（多数倚重 1-best、必要时吸收其他假设）零验证**——无注意力权重分析、无案例研究（§3.5）。
12. **代码与数据均不可得**（§9 字段 8）。
13. **引文卫生**：**[3] 与 [15] 是同一篇文献**（M. Li, W. Ruan, X. Liu, L. Soldaini, W. Hamza, C. Su, "Improving spoken language understanding by exploiting asr n-best hypotheses", arXiv:2001.05284, 2020），
    在参考文献表中以两种格式重复登记（p5/265）；且两处正文引用语境不同——
    §2 把 [3] 归入 > "**Post-editing** models have also been explored to rewrite the error-prone ASR transcriptions [3, 7]"，
    而把 [15] 归入 > "In [15], a **Bi-LSTM** model was proposed to leverage ASR N-best on a **domain classification** task"。
    **本件只登记这一形式事实（重复条目 + 语境不一致），不判定其内容对错——该文献本次未本地取得。**
14. **Index Terms 含 "error correction"，而方法不做任何转写纠错**（只在表示层融合，从不改写字符串）。属框架用词，非机制。

### 8.3 场地事实（venue facts，自证据）

| 项 | 值 | 自证据 |
|---|---|---|
| 会议 | INTERSPEECH 2021 | p1 页首压印 "INTERSPEECH 2021 / 30 August – 3 September, 2021, Brno, Czechia"（x≈36, y≈22–47） |
| 分场 | "Spoken Dialogue Systems I" | PDF `/Subject` 元数据（**正文未印**，仅元数据自证） |
| 版权 | "Copyright © 2021 ISCA" | p1 页脚 x≈36, y≈811 |
| 刊页 | 261–265（5 页） | p1 页脚居中 "261"；末页 "265" |
| DOI | 10.21437/Interspeech.2021-1370 | p1 页脚右 "http://dx.doi.org/10.21437/Interspeech.2021-1370" |
| 许可 | **无 CC 或任何开放许可行** | 全文无 |
| 排版商 | Causal Productions Pty Ltd（ISCA 御用） | `/Creator`；`/CreationDate` 与 `/ModDate` 的 `+09'30'` 时区与其阿德莱德所在地自洽 |
| 制作链 | pdfTeX 3.14159265-2.6-1.40.21 (TeX Live 2020) → Acrobat Distiller 10.1.9 (Windows) | `/PTEX.Fullbanner`、`/Producer` |
| 篇幅体例 | 4 页正文 + 1 页参考文献 = Interspeech 标准上限 | 页序核定 |
| Index Terms | > "speech recognition, error correction, entity retrieval, N-best, self-attention" | p1/261 |
| 元数据一致性 | `/Author` 七名与排版署名逐字一致；`/Title` 写 "N-**B**est" 而正文写 "N-**b**est" | `pypdf` 元数据 vs p1 标题行 |

→ **ISCA 排版链自证完整**，与 ledger 的 `ISCA_ARCHIVE_ID_DEREFERENCE` 通道自洽。

---

## 9. R2 审计字段（逐项）

### 字段 1 —— 冻结 / 白盒态

| 部件 | 训练态 | 接口态 |
|---|---|---|
| SentencePiece 分词器（vocab 6000） | **在本数据集训练** | 白盒 |
| Query 编码器（embedding + 均值池化，d=128） | **训练**（随机初始化） | 白盒（需梯度） |
| Candidate 编码器（不共享 embedding） | **训练** | 白盒 |
| 聚合层（五选一） | **训练** | 白盒 |
| 阈值 θ | 离线调定的标量 | — |
| 上游 ASR | **本篇不训练、不修改** | **需读取 N-best 列表**（比 1-best 文本 API 深一层；N ≤ 5 由 beam 宽定死） |
| 上游 NLU / NER | **本篇不训练、不修改** | 需读取 mention 切分（仅 1-best 上） |

**分层结论**：**本篇零 API-only 部件、零冻结推理控制环、零预训练模型。**
全篇不含 "freeze/frozen" 一词。上游 ASR/NLU 虽未被修改，但那是**分工边界**而非**冻结核推理控制**构念；
本篇自身的全部可学习部件都在私有目标数据上从零训练。
→ 登记 `FULLY_WHITE_BOX` / `NO_FROZEN_CORE` / `NO_PRETRAINED_MODEL` / `UPSTREAM_INTERFACE = NBEST_LIST_READ_ONLY`。

### 字段 2 —— 目标任务训练

**全部训练，无例外**，且**连词表都在目标数据上训练**。
调参通道不可审计：§5.1 用 "development dataset" 早停，而 §4 从未定义 train/dev/test 划分或任何子集规模。
→ 登记 `FULL_TARGET_TASK_TRAINING` + `SPLIT_UNREPORTED`。

### 字段 3 —— 音频回看（query-time audio revisit）

**无。零回看，且零声学接触。** 详见 §7.2 三条依据。
本篇比读集内 TED-EL 更彻底地脱离声学面：TED-EL 至少有 GSEL-J 一条 HuBERT→BART 的连续声学流，
**本篇从第一个式子起输入就是 token**。此外连 ASR 的置信度/后验都未消费。
→ 登记 `NO_AUDIO_REVISIT` / `NO_AUDIO_ACCESS` / `NO_ASR_SCORE_ACCESS`。

### 字段 4 —— 知识来源

**逐用户注册设备目录（仅名字串），单一源，规模未报，无描述文本，无公共 KB。** 详见 §7.1。
→ 登记 `KNOWLEDGE_SOURCE = PRIVATE_PER_USER_DEVICE_CATALOG (names only)` / `CATALOG_SIZE_UNREPORTED` / `NO_ENTITY_DESCRIPTIONS`。

### 字段 5 —— 选择对象（**R2 承重**）

**被选择的是"目录候选实体"；ASR 假设侧发生的是融合，不是选择。** 逐条：

- **选择空间** = 目录全体实体（推理期扫全目录，§5.1）；
  **选择规则** = `argmax_i(h^M · h^{c_i})` 并受 θ 闸门（Eq. 3）。
- **假设侧无选择**。签名从 §3 起就是 `s({m_1, …, m_L}, c_i)`——**多假设 → 单分数**；
  Figure 1 图注逐字 > "All ASR N-best mentions will be **aggregated into a single representation**"。
  **全篇零假设重排、零假设选择、零 1-best/N-best 档位切换、零 lattice/WCN。**
- 论文自己把"重排"划在他人工作里（§2, p1/261 逐字）：
  > "One approach that is frequently applied is to rely on **meta-features to rerank the hypotheses** [9, 10, 11]." /
  > "In [13, 14], the N-best list was modeled jointly through a probabilistic approach **without re-ordering**."
  → 本篇属于后一类（不重排）的神经版。
- **源的数目 = 1**，故不存在源间选择或仲裁。
- 唯一的**逐样本二值决策**是 Eq. 3 的"返回 / 弃权"，且由单一全局 θ 驱动（§4.2 判定 4）。

→ 登记 `SELECTION_OBJECT = CATALOG_ENTITY`；`HYPOTHESIS_HANDLING = SOFT_FUSION (not selection)`；`SOURCE_COUNT = 1`。
**这一条是本篇与"双源逐样本动作选择"最需要划清的界线：N-best 是同一查询的多个转写，不是多个知识源；
且它们被融合而非被选择。**

### 字段 6 —— 运行时动作

推理期拓扑固定：编码 L 条 mention → 聚合 → 全目录点积 → softmax → argmax → 阈值判定。
**无分支、无回看、无检索预算、无重试、无查询改写、无多轮、无工具调用、无跨源仲裁。**
唯一的运行时决策是 Eq. 3 的弃权闸门——**逐样本触发、但策略参数（θ）全局固定**。
→ 登记 `RUNTIME_ACTIONS = SINGLE_GLOBAL_THRESHOLD_ABSTENTION (fixed forward pass otherwise)`。

**本件派生的一处未讨论问题（承重）**：Eq. 3 的判据是 **softmax 归一化后的概率**，
而 softmax 的归一化域是"该用户目录内的全部实体"，其基数 K **逐用户不同**（§5.1 明言"each user may have registered a different number of smart devices"）。
→ **同一个全局 θ 在不同用户上具有不同的操作语义**（目录越大，top-1 的归一化概率天然越低，越容易被误拒）。
**论文全篇未讨论该校准问题，Figure 2 亦未按目录规模分层。** 标 `THRESHOLD_UNCALIBRATED_ACROSS_CATALOG_SIZE`。

### 字段 7 —— 载体

**750 小时去标识化 Alexa 智能家居控制流量**（私有），分 in-domain 与 out-of-domain 两个集合；
金标由用户反馈信号 + 重述配对启发式 + 人工标注混合得到。
**无公开发布、无许可、无规模明细（`N_id`/`N_ood`/用户数/目录规模全未报）。**
**载体时态**：2021 年（或更早）的商用语音助手流量；用户自定义设备名 → 与任何公开预训练分布的关系不可判（数据不可得）。
→ 登记 `PROPRIETARY_CARRIER` / `NOT_REPRODUCIBLE` / `NO_PUBLIC_BENCHMARK`。

### 字段 8 —— 代码 / 数据可得性

| | 状态 | 依据 |
|---|---|---|
| **数据** | **不可得**。私有去标识化生产流量，无 URL、无许可、无申请通道 | §4.1；全文无链接 |
| **模型代码** | **不可得**。**全篇零 URL、零脚注链接、零附录**（唯一脚注是实习声明） | 页序核定 + 全文扫描 |
| **绝对数字** | **未报**。Table 1 只有相对量；Figure 2 无印数 | §6.2、§6.3 |
| **已报超参** | d=128、Adam、lr 0.001、batch 128、max 1000 epochs、早停 patience 10、负例上限 10、SP vocab 6000、L ≤ 5 | §4.2、§5.1 |
| **未报超参/设定** | `N_id`、`N_ood`、目录规模 K、train/dev/test 划分、参数量、ASR 型号与 WER、NLU/NER 型号、硬件、训练时长、随机种子、padding 规则、α_i 的约束实现 | 全文 |

→ **判定**：**数据不可得 + 代码不可得 + 绝对数字不可得 + 载体不可复制**。
本篇是读集内**可复算性最低**的一档：读集内 TED-EL 至少数据可得（`BITHLP/TED-EL`）、ConEC 至少指向 icefall 仓库根，
**本篇三者皆无**。R2 若需对手臂，**只能在完全不同的载体上重建方法，与本篇数字之间不存在任何校准锚**。
→ 登记 `NO_CODE / NO_DATA / NO_ABSOLUTE_NUMBERS / NO_CALIBRATION_ANCHOR`。

---

## 10. DFS 四问

**方法**：在"ASR → NLU(NER) → 实体检索"的商用语音助手流水线里，把上游 ASR 的 N-best（≤5 条，beam 宽所限）
经 Levenshtein 对齐投影成 L 个 mention 串，各自用"embedding 查表 + 平均池化"编成向量，
再在**查询编码阶段**用五种聚合方式之一压成单一查询向量，与目录实体名向量做点积 + softmax，取 argmax 并受单一全局阈值 θ 闸门。
五种聚合中 self-attention 最好。核心实证主张两句：
**（i）用 N-best 相对只用 1-best，在私有 750h 智能家居载体上带来 11.07% 相对误差下降（θ=0）；
（ii）该增益不以牺牲域外拒识为代价（Figure 2 的 OOD RErr 全程近零）。**
自陈的新颖性边界（§2, p1/261，逐字）：
> "While neural network based ER has become the state-of-the-art approach, to the best of our knowledge there hasn't been any study conducted to **leverage ASR N-best in neural network models for ER**."
→ 声明限定在"**神经 ER + N-best**"这一交点，而非"N-best 用于 SLU"（§2 自引 [12] 2006 WCN-NER、[13]/[14] 2008、[15] 2020 Bi-LSTM 域分类）
或"ER 抗 ASR 错误"（自引 [4] 2019 音素特征、[5] 2020 Transformer 改写）。**本件只登记该声明及其边界，不作新颖性裁决。**

**自述局限**（§8.1 逐字，此处只列指向）：①未探索更先进的文本编码器；②未充分调参；③阈值需按分布与权衡选定、未给选法。
**全篇无 Limitations 节**；§6 的可迁移性外推零实验支撑。

**改进空间**（按对 R2 的信息量排序，逐条注明是否被论文点名）：

- **(a) 让检索侧触达声学/音素**——本篇从第一个式子起就只有 token，
  连 ASR 自己的置信度都丢弃；而失败模式（"den"→"dining"、"bedroom"→"bathroom"）本质是**发音近而字形远**，
  正是 Levenshtein 字符串对齐最看不见的一类。论文把音素路线明确归给 [4] 并未采用。**论文未点名此改法。**
- **(b) 消费 N-best 的分数而非只消费其字符串**——方法 2 的动机段承认假设有不同 likelihood，
  但实现只学位次权重。把真实后验/置信度作为特征喂入是最小改动。**论文未点名。**
- **(c) 供给与闸门的联合优化**——§4.5/§6.3 显示头条增益在 θ=0 取得、随 θ 上升侵蚀到 29.9%；
  一个逐样本（而非全局）的弃权策略、或按目录规模校准的阈值，是本篇结构上最直接的缺口。**论文只说"proper threshold can be chosen"，未给方法。**
- **(d) 假设选择 / 重排 与 融合 的对照**——本篇自觉地站在"不重排"一侧，
  但**没有做"重排臂 vs 融合臂"的同载体对照**，故"融合优于选择"在本篇内无证据。**论文未讨论。**
- **(e) L 的消融与 beam 宽解耦**——N≤5 是上游约束而非设计选择；增益对 L 的边际曲线未知。**论文未讨论。**
- **(f) mention 边界的独立判定**——所有假设的 mention 边界都由 1-best 投影而来，边界错时无救。
  论文给出了"每条假设各跑 NER"的备选并以算力为由排除，**未量化该权衡**。**论文点名了备选、未点名其代价。**

**可借鉴**：

1. **"多假设 → 单查询向量"的最小干预形态本身**：不改 ASR、不改 NLU、不改目录、不做纠错，
   只在查询编码处多吸收几条字符串，就取得 6.02%（等权平均，**零新增参数**）的相对误差下降。
   **"零参数的平均池化即已吃到增益的大半"这一读数是本篇最可迁移的一条**（本件复算：self-attention 相对 mean pooling 的进一步相对下降仅 5.37%）。
2. **干净的单变量基线设计**：基线 = 同架构同编码器同超参，只把 `h_M = f({m_1..m_L})` 换成 `h_M = h_1`。
   R2 若要论证"多假设供给"的净效用，这是可直接复刻的对照骨架。
3. **把拒识写进任务定义并与主指标同表评估的做法**（§3 的任务定义 + §5.4 的阈值扫描）：
   即便本篇的实现只是全局阈值，**"主指标增益必须在拒识闸门开启的条件下重测"这一评测习惯是可继承的**——
   且本篇恰好提供了一个反面读数（头条数在闸门关闭处取得，见 §4.5）。
4. **Figure 2 的双轴扫描图式**（一条轴给 in-domain 相对增益、一条轴给 OOD 相对增益、横轴给阈值）
   是"供给腿 × 闸门腿"交互的紧凑呈现方式；R2 若需展示同类交互可参照，
   但**必须补上本篇缺的部分**（同图给绝对准确率、给样本量与置信带、按目录规模分层）。

---

## 11. 与 R2 的差异面（**描述性，不含判定**）

本节只做"本篇有什么 / 没有什么"的映射，不含任何优劣或新颖性判断。

### 11.1 冻结黑盒 omni 核

**本篇不涉及。** 本篇的全部可学习部件（分词器、两侧 embedding、聚合层）都在私有目标数据上从零训练（§9 字段 1、2）；
**全篇不含 "freeze/frozen" 一词，亦无任何预训练/基础模型**——最大的单体组件是 `3d² = 49,152` 参数的自注意力层（本件推算）。
上游 ASR/NLU 虽未被本篇修改，但本篇对它们的要求是**读取 N-best 列表与 mention 切分**，
这是分工边界而非"冻结核 + 推理期控制"的接口条件。
模型族方面：**零 omni 模型、零指令模型、零 prompt 通道、零 LLM**。

### 11.2 逐样本双源动作

**本篇不涉及。** 逐条对照：

- **源的数目**：知识源只有**逐用户设备目录一个**（§9 字段 4）。无第二知识源，故不存在源间选择或仲裁。
- **N-best 不是第二个源**：它是同一条音频的多个转写假设，且被**融合成单一向量**，个体身份在打分前即消失（§9 字段 5）。
- **动作的逐样本性**：推理期拓扑固定；唯一的逐样本决策是 Eq. 3 的返回/弃权二值判定，
  且其策略参数 θ 是**离线调定的全局常量**，对所有样本、所有用户相同（§9 字段 6）。
- **选择的对象**：唯一的"选择"是在单一目录的全体实体上取最高分（§9 字段 5），即**同源内部的候选排序**。
- **假设侧**：无 N-best 重排、无 1-best/N-best 档位切换、无回退（§9 字段 5）。

### 11.3 证据采纳（evidence admission）

**本篇提供了一个位置相近、粒度与依据都不同的构件，且其边界可逐字定位。** 详细判定见 §4.3 的七行对照表，此处摘要：

- **有**：检索之后的"不返回"出口（Eq. 3 的 `−1` 支），以及对该出口的专门评测集与专门指标（§4.1 OOD 集、Eq. 5）。
- **无**：对**多件**检索证据的逐件采纳/剔除；基于证据**内容**（相关性、可信度、冲突）的判据；
  **逐样本自适应**的采纳策略；跨源仲裁；对被采纳证据的下游用法分化。
- **依据的性质**：判据是检索器**自身**的归一化相似度，无独立验证器、无第二意见、无一致性检查。
- **语义标签与机制的错位**：论文以请求级措辞描述（"reject the query"、"rejecting out-of-domain ER requests"），
  但机制上不存在检索前的请求判定。
- **未讨论的校准问题**：softmax 的归一化域是逐用户变基数的目录，故全局 θ 跨用户不等价（§9 字段 6 派生）。

### 11.4 时间线定位（语音实体检索 / 链接 → 外部知识）

**逐字可定位的时点与其上下游（仅事实陈述，不评价）**：

- **本篇 = 2021-08/09（Interspeech 2021, Brno；PDF 制作日 2021-09-01）**。
- **本篇自陈的上游谱系**（§2, p1/261，逐字，被引件本次均未取、内容未本地复核）：
  - ER 抗 ASR 错误：> "[4] tried to recover ASR errors for ER by introducing phonetic features during the search phase."（Raghuvanshi et al., **2019**, EMNLP-IJCNLP Demo）；
    > "In [5], a transformer based model was proposed to explicitly rewrite the noisy search term based on synthetic data generated by error simulation."（H. Wang et al., **2020**, INTERSPEECH——与本篇第一作者同姓名）。
  - N-best 用于 SLU：> "[12] constructed a **word confusion network** on the N-best hypotheses and used it to conduct NER, but it is constrained with rules on limited use cases."（Hakkani-Tür et al., **2006**）；
    > "In [13, 14], the N-best list was modeled jointly through a probabilistic approach without re-ordering."（**2008**）；
    > "In [15], a Bi-LSTM model was proposed to leverage ASR N-best on a **domain classification** task."（Li et al., **2020**）。
  - 架构谱系：双塔来自文本 EL 的 [18]（Agarwal & Bikel, **2020**）；自注意力来自 [23]（Vaswani et al., **2017**）；全局注意力的 context vector 来自 [22]（Luong et al., **2015**）。
- **该时点上的技术形态**（逐条为事实陈述）：知识源 = 私有小目录、仅实体名；
  知识消费方式 = 名字串进入从零训练的 embedding 池化编码器；
  检索 = 单轮双塔点积 + softmax（无重排级、无多轮、无查询改写、无迭代）；
  音频消费 = **零**（连 ASR 分数都不消费）；
  动作空间 = 固定前向 + 单一全局阈值弃权。
  **这一形态早于 2024 的语音实体链接语料线（TED-EL / ConEC）与 2026 深检索线**（多轮/自适应检索、工具调用、逐样本动作、冻结核 prompt 通道等）；
  本节只登记其在时间线上的先后位置，不对其与后续工作的关系作任何评价性判断。

**与读集内两件语音-实体载体论文的并置（仅作事实对照，不含优劣）**：

| | wang21b（本篇，2021） | ConEC（2024.lrec-main.328） | TED-EL（2024.lrec-main.1365） |
|---|---|---|---|
| 任务 | 实体检索（私有目录） | 上下文偏置 ASR | 语音实体链接（Wikidata） |
| 外部信息的身份 | 逐用户设备名目录 | 当期公开文档（IR slides / 财报稿 / 名单） | 通用百科 KB（Wikidata QID） |
| 外部信息的内容 | **仅名字串** | 偏置词表 | 实体名 + **描述文本** |
| 外部信息的进入通路 | 从零训练的候选编码器 embedding | beam 内浅融合（λ 加分） | 被训练的双塔/交叉编码器输入 |
| 转写侧假设 | **N-best（L≤5）软融合成单向量** | 1-best | 1-best |
| 训练态 | **全部从零训练**（含分词器） | 偏置层零训练；识别器 SPGISpeech 训练 | 全部部件训练（+BLINK 预训练） |
| 预训练模型 | **无** | 有（识别器） | 有（BERT/wav2vec2/HuBERT/BART） |
| 弃权 / 不作答 | **有**（Eq. 3 全局阈值，且有 OOD 评测集与指标） | 无 | **无**（gold 有 5.38% NULL，方法侧与指标侧双缺席） |
| 主指标 | Precision@1（**只报相对误差下降**） | WER（总/常见/稀有/逐实体类型） | 实体链接 P/R/F1（mention 串匹配口径） |
| 绝对数字 | **全篇无** | 有 | 有 |
| 载体 | **私有 750h 生产流量** | Earnings-21/22 之上的上下文层 | TED-LIUM 3 之上的标注层 |
| 代码 | **无任何 URL** | icefall 仓库根（无 recipe） | 无自有 URL |
| 数据 | **不可得** | `huangruizhe/ConEC` | `BITHLP/TED-EL` |

---

## 12. 深读后新增的、R2 应该知道的事实

1. **N-best 在本篇是"融合"不是"选择"。**
   签名从 §3 起就是 `s({m_1, …, m_L}, c_i)`，Figure 1 图注逐字 "aggregated into a **single** representation"。
   **全篇零假设重排、零假设选择、零档位切换。**
   → **R2 若把本篇引作"N-best 选择腿"的先例，是误引**；准确表述为"**N-best 在查询编码阶段被软加权融合为单一查询表示**"。

2. **拒识 = 检索后的 top-1 分数阈值弃权，不是训练出来的分类器，也不是请求前置过滤。**
   无 OOD 训练数据（负例只取自同用户目录内的错误设备）、无专属参数、无专属损失；
   θ 是离线调定的**全局常量**；判据是检索器自身的 softmax 分数。
   → 本篇既不落在 R2 的"证据采纳"构念内（无逐件裁决、无内容依据、无逐样本策略），
   也不是真正的"请求级前置拒识"（检索总是先跑完）。**R2 的 RQ3 量词面必须按 §4.3 的七行表逐格记账。**

3. **头条 11.07% 是在 θ=0（拒识闸门关闭）下测得的。**（§5.3 逐字："We set θ = 0 for this experiment"）
   **供给腿与闸门腿在本篇从未在同一配置下同时报过一个数。**

4. **闸门开启后供给增益单调侵蚀。**（本件由 Figure 2 向量反算，标定残差 ≤1.4e−4，并与 Table 1 的 θ=0 值交叉验证）
   in-domain RErr：θ=0 → 0.1107；θ=0.1 → 0.1020；θ=0.9 → **0.0331**，
   即 **θ=0.9 时只剩 θ=0 增益的 29.92%**。
   → **R2 报"知识供给增益"时，必须声明弃权闸门处于何种配置；两腿不可分别取各自最优值拼接。**

5. **OOD 侧的"维持不变"是相对量的窄带，不是绝对水平的报告。**
   Figure 2 蓝线全程落在 **[−0.0184, +0.0883]**（本件反算）。
   **本篇从未报出"能拒掉多少 OOD"的绝对数**——它只报了 self-attention 与 1-best 基线在 OOD 上的**差异**。
   且 `N_ood` 未报，**该窄带是否在噪声内不可判**。

6. **绝对准确率全篇缺席，因此本篇不提供任何跨工作的校准锚。**
   由题注定义只能解出恒等式 `Acc_m = Acc_base + RER × (100 − Acc_base)`，而 `Acc_base` 未知。
   → **R2 不得把 11.07% 转述为绝对准确率或绝对提升。**

7. **增益的主体来自"用多假设"这一动作，而非某种聚合算子。**（本件基线无关的复算）
   零参数的 Mean Pooling 已取得 6.02%；self-attention 相对次优的 Concatenation 只再进一步相对下降 **2.41%**；
   Learnable Weights (8.61) 与 Global Attention (8.57) 之差折算仅 **0.0437%**，在无方差报告下不可判方向。

8. **检索侧完全触不到音频，连 ASR 的置信度都不消费。**
   对齐用 Levenshtein（纯字符串），无音素、无声学；
   §3.2 的 likelihood 只是"引入位次权重"的动机，从未作为输入进入任何式子。
   → 本篇是"**从上游 ASR 只保留 N 条字符串**"的最窄信息带宽形态；
   而其典型失败模式（den→dining、bedroom→bathroom）恰是发音近而字形远的一类。

9. **知识源是逐用户的设备名目录，只有名字串。**
   无描述、无类型、无属性、无公共 KB；规模 K 未报；
   §3 用于论证双塔选型的"百万级实体"是**设计动机而非实测设定**。

10. **softmax 归一化域随用户目录规模变化，故全局 θ 跨用户不等价。**（本件派生，论文未讨论）
    目录越大、top-1 归一化概率天然越低、越易被误拒。Figure 2 未按目录规模分层。
    → 这是"用检索器自身分数做弃权判据"这一族方案的一个结构性校准缺口，R2 若采同类判据须自行处理。

11. **复算性为读集内最低档**：代码无、数据无、绝对数字无、载体私有；
    另有 `N_id`/`N_ood`/K/划分/参数量/ASR 型号与 WER/硬件/种子全部未报。
    → R2 若需对手臂，只能在完全不同的载体上重建方法，**与本篇数字之间不存在任何校准锚**。

12. **形式化层面三处不自足**：Eq. 1/Eq. 2 的维度不自洽（`A ∈ [0,1]^{L×L}` 与 `(QH)(KH)^T` 不兼容）、
    Eq. 3 的 `i` 未量化（应为 `max_i`）、Eq. 5 的 `y_i` 对 OOD（ground truth 为空）未定义。
    意图均可推断，但**式子不可直接照抄实现**。另：变长 L 的 padding/masking 规则全篇无一字，而 Concatenation 强制定长。

13. **统计学纪律缺席**：零重复、零方差、零置信区间、零显著性检验、零样本量，
    却使用 > "we notice **significant** relative error reduction, which **proves** the importance of using ASR N-best"（§5.3）。
    → **R2 引用本篇任何数字时须同时声明"单次运行、无方差、无检验"。**

14. **场地与文献事实**：ISCA 排版链自证完整（Causal Productions / pdfTeX TeX Live 2020 / Distiller 10.1.9；
    `/Subject` 记分场为 "Spoken Dialogue Systems I"）；4 页正文 + 1 页参考文献；**无 Limitations / Ethics / 附录 / 任何 URL**；
    参考文献 26 条中 **[3] 与 [15] 为同一篇（arXiv:2001.05284）重复登记**，且两处正文引用语境不同
    （[3] 被归入 post-editing 改写、[15] 被归入 N-best 域分类）——本件只登记形式事实，不判定内容对错。

---

## 13. 遗留核对义务（有网络时的第一批动作）

1. **对官方 ISCA Archive PDF 目视复核 Table 1 全部六行数字与 Figure 2 两条曲线**（§1 证据等级声明 1、3）。
   Figure 2 的九对数值系本件向量反算，虽有两路交叉验证（标定残差 ≤1.4e−4；θ=0.1 值与 Table 1 的 θ=0 值趋势连续），
   **仍应在有网络时以独立工具（如 Adobe 内容抽取或作者原图）复核**，特别是右轴的偏移校正量（−0.16 pt）。
2. **取 [5] H. Wang et al., "ASR error correction with augmented transformer for entity retrieval", INTERSPEECH 2020**——
   与本篇第一作者同姓名、同任务、同机构线，**是本篇最近的自身前驱**，很可能含本篇缺失的载体统计与绝对基线数字。**第一优先补充源。**
3. **取 [4] Raghuvanshi et al., "Entity resolution for noisy ASR transcripts", EMNLP-IJCNLP 2019 Demo**——
   本篇明确归属的"音素特征"路线，是 §10 改进空间 (a) 的直接对照件。
4. **取 [15]/[3] Li et al., arXiv:2001.05284**——确认其是否确为同一文献重复登记（§8.2 第 13 条），
   并核 §2 把它归入 "post-editing" 是否为引用错配。
5. **取 [18] Agarwal & Bikel, arXiv:2004.03555**——本篇双塔架构的直接来源，用以核定本篇相对其的改动面。
6. **检索本篇的后续引用**（2022–2026），确认"N-best 融合进检索查询编码"这一形态是否有更晚的公开载体版本
   （本篇载体私有，任何复现都必须换载体）。
7. **核 ISCA Archive 页面**是否提供补充材料、海报或视频（正文无附录，但 ISCA 站点偶有附件）。
