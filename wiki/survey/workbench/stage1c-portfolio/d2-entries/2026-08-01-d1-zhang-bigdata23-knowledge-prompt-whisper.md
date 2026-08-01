---
artifact_id: "SF-STAGE1C-D1-KPWHISPER-DOI10.1109-BIGDATA59044.2023.10386366"
arxiv_id: "none (DOI 10.1109/BigData59044.2023.10386366；无 arXiv 版、无 OA 全文)"
title: "Knowledge Prompt for Whisper: An ASR Entity Correction Approach with Knowledge Base"
authors: "Min Zhang, Xiaosong Qiao, Yanqing Zhao, Chang Su, Yinglu Li, Yuang Li, Ming Zhu, Mengyao Piao, Song Peng, Shimin Tao, Hao Yang, Yanfei Jiang（Huawei Translation Services Center）"
venue: "2023 IEEE International Conference on Big Data (BigData 2023), pp. 2975–2979（5 页短文；书目经 RAC 2409.06062 `main.bbl` 第 98–103 行独立复核一致）"
date: "2026-08-01"
read_level: "D1_ABSTRACT_PLUS_SECONDARY"
reader: "opus-agent"
status: "DRAFT_FOR_R2_INTEGRATION"
source_of_record: "**非 D2**。证据基座仅两件：(a) Semantic Scholar API 返回的官方摘要（由上游会话核验后作为已验证输入交付本件，本件零网络、未复取）；(b) 引用方 RAC (arXiv 2409.06062) 的 related-work 转述（本地 eprint 全文，本件一手复核）。**IEEE Xplore 全文付费墙，无 OA 副本**，故本件所有机制刻画的证据权重低于同批 D2 条目一档，正文逐句标注证据来源。"
local_evidence:
  - "无本篇本地全文——ledger 第 1324 行 access_class=DOI_METADATA_ONLY/NO_FULLTEXT，stored_at=null、sha256=null、bytes=0"
  - "二手源（本地一手可核）：E:/chao_workspace/exploring-l4-intelligence/speechrl-data/survey-fulltext/2409.06062/2409.06062.eprint（gzip tar，905478 bytes，ledger 第 1309 行）解包得 `main.tex` 第 96 行 related-work 转述 + `main.bbl` 第 98–103 行书目条目；本件对该二手源的两处直引已逐字复核通过"
  - "二手源辅助：同目录 2409.06062.pdf（516414 bytes，ledger 第 1308 行）——本件未据其取数"
ledger_ref: "wiki/survey/2026-07-17-sf-fulltext-ledger.jsonl 第 1324 行（全文件末行，本次 `wc -l`=1324 复核一致）；该行为 NO_FULLTEXT 行，非 fetch 成功行"
prior_status: "本篇经 round-14 博士导师级协同评审 MAJOR-2 进入读集（`wiki/audit/system-first-stage1c-v2/round-14/2026-08-01-r2-v15-doctoral-supervisor-coreview.md` 第 275–298 行：『新颖性合取的一个分量上，有两篇具名近邻未读，且本件自标开题前必读』）。上游来源=R2 draft §8 第 736–737 行 † 注与 §9 第 808–809 行调研义务，二者均由 D2-RAC 条目 §6.1 一手指认。**本件为该两篇中的第一篇；因无 OA 全文，只能交付 D1 级而非 MAJOR-2 处置条款要求的『D2 级源核』——处置只能部分关闭，见 §7。**"
exposure: "零网络请求（本次会话未发起任何 fetch/search/API 调用）；只读本地文件：RAC eprint（解包至会话 scratchpad，未写入仓库）、ledger、round-14 评审件、R2 draft、D2 模板件——全部只读，未改动任何既有文件；摘要直引为上游会话已核验输入，本件未复取亦未据网络扩展；零模型调用、零指标运行、零数据集下载；本件为唯一新建文件"
supersedes: "无（新建）"
---

# D1 摘要级条目：Knowledge Prompt for Whisper (Zhang et al., IEEE BigData 2023)

> **证据等级警示（贯穿全文）**：本件不是 D2。凡机制刻画均带证据标记——
> 【摘】= S2 官方摘要原文（上游已核验输入）；【转】= RAC 2409.06062 `main.tex` 第 96 行转述
> （本件一手复核）；【书】= RAC `main.bbl` 第 98–103 行书目元数据（本件一手复核）；
> 【推】= 本件推断，**不是证据**，任何承重引用不得使用【推】项。
> 无标记的断言在本件中不存在；若下游引用时标记丢失，即为证据降级事故。

## 1. 来源与证据等级声明

### 1.1 为何无全文

本篇发表于 IEEE BigData 2023 会议论文集（pp. 2975–2979）【书】，正式版仅在 IEEE Xplore 付费墙后
提供。上游会话的取全文尝试记录在 ledger 末行：

> `{"arxiv_id": "doi:10.1109/BigData59044.2023.10386366", "kind": "pdf", "url": "https://doi.org/10.1109/BigData59044.2023.10386366", "time_utc": "2026-08-01T00:02:23Z", "http_status": null, "attempts": 1, "bytes": 0, "sha256": null, "error": "NO_OA_FULLTEXT: IEEE paywall; NOT_ON_ARXIV (title/all-field/author-listing/S2-externalIds four-way negative); abstract-level evidence only (S2 API abstract + citing-paper 2409.06062 related-work characterization)", "stored_at": null, "access_class": "DOI_METADATA_ONLY/NO_FULLTEXT"}`

该行 `stored_at=null`、`sha256=null`、`bytes=0`、`http_status=null`——**本篇在本地不存在任何全文
字节，因此本件无 sha256 可复算，这是它与同批十件 D2 条目最根本的证据差别**。

### 1.2 四路 NOT_ON_ARXIV 证据（上游会话执行，本件不复取）

R2 的调研宪章是「arXiv 唯一引用宇宙」，非 arXiv 件须逐件出具排除证据（先例：PRISM
2023.emnlp-main.916 与 RECAST 2025.findings-emnlp.203 走「作者列表+题名双检」）。本篇的排除证据
为四路，全部记入 ledger `error` 字段：

| # | 路径 | 结果 |
|---|---|---|
| 1 | arXiv 题名检索 | 0 命中 |
| 2 | arXiv 全字段检索 | 0 命中 |
| 3 | 共同作者 arXiv 著录列表逐一排查 | 无对应条目 |
| 4 | Semantic Scholar `externalIds` | 无 `ArXiv` 键（仅 DOI/CorpusId 类） |

**四路一致为负 → 判定 NOT_ON_ARXIV，按 ACL/IEEE 类件例外入册，ledger `access_class` 记
`DOI_METADATA_ONLY/NO_FULLTEXT`（区别于 PRISM/RECAST 的 `ACL_ANTHOLOGY_ID_DEREFERENCE/
FULLTEXT_FETCH`——后者拿到了全文字节，本篇没有）。**

**本件对该四路证据的立场**：这是上游会话的执行结果，本件零网络，**无法独立复核**。本件只能声明
「已按四路排除、记录在册」，不得声明「本件已验证 arXiv 上无此文」。若下游需要签署级 arXiv 排除
结论，须由具备网络 exposure 的会话重跑并单独出具。

### 1.3 可信边界（本件一切结论适用）

1. **摘要不是论文**。摘要是作者的自我概括，系统性地省略：超参、消融、基线细节、失败模式、
   阈值、数据规模、训练/微调是否存在。**摘要里没有提到的东西，不构成「论文里没有」的证据。**
   本件所有「缺席」判定因此最多只能是「摘要级未见」，其强度严格低于 D2 条目的「全文核对缺席」。
2. **转述不是原文**。RAC 的 related-work 是竞争者视角的对比性概括，且 RAC 有把对手刻画得更笨重
   （"more computationally costly"）的结构性动机。转述可作**机制存在性**的独立佐证（RAC 是一手
   读过原文的第三方），但**不可作机制细节或数值的来源**。
3. **本件不得用于任何数值论证**。摘要给出的两个百分点（§4）是作者自报头条，无表、无基线族、
   无置信区间、无消融——按 R2 §8「头条与公开集是两类证据」的既有纪律，本篇连「公开集数」这一
   档都还没有。
4. **本件对 R2 的唯一承重用途是「占据判定」**（§5）——即某个动作/机制**是否已被他人做过**。
   占据判定对证据的要求是「存在性」而非「效果量」，因此摘要+转述在这一用途上**足够**；
   在任何效果、对比、优劣用途上**不足够**。
5. **本件所有 delta 缺席判定（§6）都带残余风险**，逐条已标注等级，禁止在下游整编中把
   `PROBABLE` / `UNRESOLVED` 提升为 `CONFIRMED`。

## 2. 书目一手复核（本件唯一能做到 D2 级严格度的部分）

RAC 的 `main.bbl` 第 98–103 行（本件从本地 eprint 解包后逐字复核）：

> `\bibitem{zhang2023knowledge}` / `M.~Zhang, X.~Qiao, Y.~Zhao, C.~Su, Y.~Li, Y.~Li, M.~Zhu,`
> `M.~Piao, S.~Peng, S.~Tao \emph{et~al.}, ``Knowledge prompt for {Whisper}: An {ASR} entity`
> `correction approach with knowledge base,'' in \emph{2023 IEEE International Conference on Big`
> `Data}.\hskip 1em plus 0.5em minus 0.4em\relax IEEE, 2023, pp. 2975--2979.`

**复核结论**：题名、作者序（前十人 + et al.，其中 `Y.~Li, Y.~Li` 对应 Yinglu Li 与 Yuang Li）、
会议名、年份、页码 2975–2979 **与上游交付的元数据逐项一致**【书】。这是本件独立于 S2 的第二条
书目来源，两源一致，**书目层无歧义**。

**引用编号解析**（承重，因 R2 下游会引 RAC 原文的 "[15]/[16]" 表述）：按 `main.bbl` 的
`\bibitem` 出现序复核——1 prabhavalkar2023end、2 van2023modeling、3 ma2023can、4 izacard2023atlas、
5 kandpal2023…、6 robertson1995okapi、7 ni2021sentence、8 jeon2020acoustic、9 guo2019spelling、
10 gu2024denoising、11 raghuvanshi2019entity、12 Wang2020ASREC、13 kang2024transformer、
14 cai2023kg、**15 zhang2023knowledge（本篇）**、16 ragdst。
**故 RAC 渲染稿中的 "[15]" 确指本篇、"[16]" 确指 Wang et al. ICASSP 2024（retrieval augmented
end-to-end spoken dialog models）——编号映射 CONFIRMED。**

## 3. 机制刻画（摘要级）

### 3.1 三步管线（全部证据为【摘】直引）

摘要原文：

> "For a given audio, our approach consists of three steps: (1) obtaining its ASR result by Whisper;
> (2) fuzzy matching the ASR result with a knowledge base to obtain candidate entities; (3) using the
> candidate entities as a prompt to obtain the final ASR result by Whisper again."

拆解：

| 步 | 动作 | 输入 | 输出 | 证据 |
|---|---|---|---|---|
| 1 | Whisper 首遍解码 | 音频 | 一遍假设（文本） | 【摘】 |
| 2 | 与知识库**模糊匹配** | 一遍假设（文本） | 候选实体集 | 【摘】 |
| 3 | 候选实体**作 prompt**，**再跑一次 Whisper** | 音频 + 候选 prompt | 最终假设 | 【摘】 |

**三点结构性观察**：

1. **第 3 步消费的是音频本身，不是文本假设**。摘要写 "to obtain the final ASR result by Whisper
   again"——Whisper 是语音识别器，其二次运行的输入必然含音频【摘】。这一点被 RAC 独立确认：
   RAC 第 96 行说 "both [15] and [16] requre the input audio, which means they cannot be applied in
   scenarios where only the textual ASR hypothesis is available"【转】（`requre` 为原文笔误，
   照录）。**两源独立一致 → 「二次解码回到音频」是本件证据最强的一条机制事实。**
2. **注入通道是 prompt，不是权重、不是解码环改写**。摘要用词是 "using the candidate entities as
   a prompt"【摘】；题名亦为 "Knowledge Prompt for Whisper"【书】。Whisper 的 prompt 通道
   （`initial_prompt` / prefix 条件化）是**公开 API 即可访问的接口**，无须读隐状态、无须改
   beam-search——**这使本篇在信息访问口径上比 PRISM（读 encoder/decoder 隐状态 + 改写解码环）与
   WCTC-Biasing（层间读写）都更接近 R2 的 API-only 黑盒边界**。
   **限定【推】**：「Whisper prompt 通道 = 近 API-only」是本件基于 Whisper 接口常识的推断，
   **摘要未说明其调用的是官方 API 还是本地 checkpoint，也未说明 prompt 是否经过任何适配**。
   若本篇实际使用了本地 checkpoint 的特权 prefix 注入或做过 prompt 侧微调，该刻画将被推翻。
   **此项须在全文可得后第一优先复核（§7）。**
3. **training-free 的证据是间接的，不是直接的**。摘要三步中无任何训练/微调动词【摘】；RAC 的
   对比句 "rather than an employing a adapted LLM for error correction, ASR is rerun with the
   generated context"【转】把本篇与「适配过的 LLM」对立，**隐含本篇不含适配模型**。
   **但两条都是「未提及」而非「明确否认」**——摘要省略训练细节是常态，RAC 的对比也只针对
   「纠错侧是否有 adapted LLM」，不排除模糊匹配器或 prompt 构造侧存在训练组件。
   **判定：training-free = PROBABLE（两源间接一致），不是 CONFIRMED。**

### 3.2 与 R2 既有近邻的机制位对照（占据判定用，非效果对照）

| 维 | 本篇（摘要级） | RAC（D2 已核） | R2 提案 |
|---|---|---|---|
| 是否回音频 | **是**（Whisper 二次运行）【摘】【转】 | 否（纯文本后处理）| 是 |
| 注入接口 | prompt（近 API-only）【摘】+【推】 | prompt 串给 LoRA-7B | prompt（API-only） |
| 检索 key | 文本（一遍假设）模糊匹配【摘】 | 正字法声学近邻嵌入（ANE） | 拟含声学通道 |
| 训练态 | 疑似零训练【摘】【转】，PROBABLE | LoRA-4 纠错器 + LoRA-16 tagger | 零训练 |
| 动作条件化 | 摘要级未见任何条件【摘】 | 无（确定性阈值准入门存在） | 可标定标量+外显阈值 |
| 载体 | AISHELL-NER（中文）【摘】 | STOP（唯一公开）+ 内部合成集 | 待冻结 |

**这张表最重要的一格是「回音频 + prompt + 疑似零训练」三者同时为真**——在 R2 现有的十篇近邻中
**没有任何一篇同时满足**（RAC 不回音频；PRISM/WCTC 回音频但是白盒；Lei 回音频但训练 46M 参数；
Speech-Hands 回音频但 SFT 改核参数）。这是本篇对 R2 独立性主张的实际杀伤面，详见 §5。

## 4. 关键数字（全部为摘要级自报，禁止承重）

摘要原文：

> "Experimental results show that our approach not only significantly improves the entity recall rate
> in ASR results (from 70.97% to 84.82%), but also reduces the overall Character Error Rate (CER)."

| 项 | 值 | 证据 | 使用限制 |
|---|---|---|---|
| 实体召回率 | 70.97% → 84.82%（+13.85 pp） | 【摘】 | 仅可作**方向性存在证据**；无基线族、无置信区间、无消融 |
| CER | 「下降」，**摘要未给任何数字** | 【摘】 | **禁止赋任何数值**；只能引作定性「作者自报下降」 |
| 测试集 | AISHELLNER（中文） | 【摘】 | 单集、单语；下同 |

**四条必须随行的限定**：

1. **CER 无数**。摘要只说 "reduces"，没有幅度。R2 若引本篇的 CER 结论，只能写「作者自报 CER 下降，
   论文摘要未量化」——这与 D2-RAC 条目对 RAC 的 ICL 负结果所用的口径同型（"论文零数字，只能引作
   定性陈述"）。
2. **`AISHELLNER` 的标准写法应为 AISHELL-NER**（基于 AISHELL-1 的中文命名实体标注集）【推】——
   该身份映射是本件推断，**摘要只给了字符串 `AISHELLNER`，未给引用**。全文可得前不得据此讨论
   数据规模、切分或与其他工作的可比性。
3. **单集单语**。中文单一测试集，无跨语言、无跨域、无跨识别器证据【摘】。按 R2 §5.3 的载体纪律，
   本篇的战力口径不可与英文近邻（RAC/DARAG/BR-ASR/Siskos）并表比较。
4. **基线强度未知，增益可能含 headroom【推】**：70.97% 的起点是 Whisper 在中文实体上的表现；
   Whisper 的中文能力弱于英文是公开常识，故 +13.85 pp 中有多少来自「方法」、多少来自「弱基线的
   头顶空间」**无法从摘要判断**。**此项为推断，不得写入任何对外刻画**；记入本件只为提醒下游
   **不要**把 +13.85 pp 当作方法强度的证据。

## 5. 「重解析」分量判定（本件的承重结论）

### 5.1 判定

**本篇干净占据 R2 的「带知识候选重跑 ASR」动作分量，且占据形态比 RAC 的转述所暗示的更强。**

判定链（每环列证据）：

1. **动作存在**：步 (3) "using the candidate entities as a prompt to obtain the final ASR result by
   Whisper again"【摘】——检索到的知识候选被用来**再解码一次**。这在结构上就是 R2 的
   re-resolve / 重解析动作（对**已持有音频**的重新呈现与重新裁决，R2 §1.3 第②类信息作用）。
2. **动作回到音频**：RAC 独立确认 "requre the input audio"【转】。故这不是文本层 rerank，
   而是**真的把音频再送一遍**。
3. **动作在 prompt 层，不改权重、不改解码环**：题名 "Knowledge Prompt"【书】+ 摘要 "as a
   prompt"【摘】。
4. **动作疑似 training-free**：§3.1 第 3 点，PROBABLE。

**合成结论**：环 1–3 为 CONFIRMED（摘要级，且环 2 有两源独立一致）；环 4 为 PROBABLE。
即使环 4 最终被全文推翻（论文其实有训练组件），**环 1–3 已足以占据「带知识候选、在 prompt 层
重跑 ASR」这一动作本身**。

### 5.2 对 R2 的直接约束（承重，须回写 §8）

R2 draft §8 第 736–737 行现有 † 注写的是：

> 「『回音频重解析』单项动作在 RAC 引文邻域已有先例（Whisper 知识提示重跑线与检索增强口语
> 对话线，各一篇、未入读集——补扫义务见 §9）；该 delta 不单独承重，承重的是合取。」

**本件对该注的处置意见：注的方向正确，但强度不足，必须升级。** 三点理由：

1. **「先例」的措辞太弱**。本篇不是「有个远亲也回过音频」，而是**同一动作、同一注入层
   （prompt）、同一目标（实体纠正）、同一识别器族（Whisper）**。R2 的重解析动作在**动作定义
   层面**与本篇不可区分。
2. **RAC 的成本论调不能被 R2 继承为差分**。RAC 以 "making it more computationally costly"【转】
   为由回避该动作——但 R2 **本来就要付这个成本**（R2 的重听动作同样是二次消费音频）。因此
   RAC 给出的那条「回避理由」对 R2 无效，**R2 与本篇在成本轴上同侧**。
3. **本篇很可能比 RAC 更接近 R2 的信息边界**（prompt 注入 + 疑似零训练）。R2 §8 把 RAC 列为
   「最容易被指为已占据的对手」——**该称号在重解析分量上应转移给本篇**。

**处置（三条，逐条可执行）**：

- **R2 不得在任何位置把「回音频重解析动作」作为独立新增变量单独主张**（此结论 D2-RAC 条目
  §6.1 已下，本件将其从「引文中的先例」升级为「已核到摘要+转述两源的具名占据」）。
- **§8 † 注应改写为具名形式**，例如：「『带知识候选在 prompt 层重跑 ASR』这一动作已由
  Zhang et al., IEEE BigData 2023（Knowledge Prompt for Whisper）占据，且其为 prompt 级、
  疑似零训练；本提案的重解析分量因此**零新颖性**，独立性只能挂在合取上。」
- **§8 组合格结论的量词自限须显式扩到本篇**：现有量词是「上表十篇+读集」，本篇现已入读集
  （D1 级），故量词覆盖已扩展；但**必须同时声明本篇为 D1 级证据**，否则合取结论会被误读为
  建立在同质证据面上。

### 5.3 一条必须记下的反向观察（对 R2 有利，但只能定性）

本篇的占据是**无条件管线**形态（§6.1）。这意味着：**「回音频重解析」被占据的是动作，不是
「何时做该动作」的决策问题**。R2 的机制核心（可标定标量 + 外显阈值 + 双源同尺度选择）**恰好
落在本篇没有触及的那一层**。这与 D2-MementoGUI 条目的教训同型（"跨域已有刷新门先例……R2 的
独立性主张应落在训练无关地做同一件事 + 用感知不确定性信号驱动它"）——只是本篇更近，它就在
语音域、就在 Whisper 上。

## 6. R2 残余 delta 核验（逐个，以摘要+转述为证据上限）

**方法学声明**：以下四项的「缺席」判定，其证据是「摘要与 RAC 转述中未见」。摘要的省略是常态，
因此**没有任何一项能达到 D2 条目那种「全文核对缺席」的强度**。等级定义：
`ABSENT_PROBABLE`（摘要给出了完整管线描述，若存在该机制应当出现而未出现）；
`UNRESOLVED_PENDING_FULLTEXT`（摘要的表述与该机制的存在/不存在**两者兼容**，无法判定）。
**本节零 CONFIRMED——这是证据等级的必然结果，不是核验不力。**

### 6.1 门控动作选择（gated action selection）—— `ABSENT_PROBABLE`

**证据**：摘要以 "For a given audio, our approach consists of three steps"【摘】开头——
**全称量化于所有输入音频**，随后三步以 (1)(2)(3) 顺序列出，**无任何条件从句、无阈值、无
「若……则跳过」分支、无「是否重跑」的判断步**。这是一条**无条件三步管线**。

**论证**：R2 的门控动作选择要求的是「按样本决定要不要付这个动作的代价」。本篇的第 3 步对每条
音频都执行；即使某条音频的一遍假设已经正确、或知识库无相关实体，摘要描述的管线仍会走完三步。
故本篇**不构成对 R2「门控」分量的占据**。

**残余风险（必须声明）**：
- 摘要**几乎必然**省略了模糊匹配的相似度阈值。模糊匹配按定义带阈值——但**该阈值是候选筛选
  （准入侧），不是动作选择（采集侧）**，二者在 R2 §1.6 双门框架里分属不同门。即便全文证实
  存在匹配阈值，**也只占据准入门先例位（与 RAC 的 `D_max`/`R_max`、Lei 的 NPD 阈值同族），
  不占据动作门**。R2 的准入门差分本来就已挂在「可标定标量 + 按样本自适应」而非「有没有门」上
  （D2-RAC §7 第 3 条），故此风险不改变 R2 结论。
- **无法排除**全文存在一条退化分支「若候选集为空则不重跑」。若存在，那是**数据可得性触发**，
  不是可标定的决策信号——按 D2-Lei 条目对布尔触发的既有处置，仍不占据 R2 的标量门位。
  但 R2 的措辞须避免「本篇完全无条件」这种绝对句，改用「摘要级未见任何按样本的动作决策」。

### 6.2 世界知识 rescore —— `ABSENT_PROBABLE`，但**附一条会削弱 R2 措辞的一手观察**

**证据**：知识库在摘要中只出现于第 2 步，功能是 "fuzzy matching the ASR result with a knowledge
base to obtain candidate entities"【摘】——**知识库是一个被字符串匹配查询的索引，仅产出候选**。
摘要中**没有任何**：实体存在性裁决、语境合理性判断、候选间的知识驱动打分/排序、或独立的
rescore 阶段。

**论证**：R2 的「世界知识 rescore」是指用世界知识**裁决声学上混淆的候选**（哪个实体在这个语境
里真的存在/合理）。本篇的知识库不承担裁决职能，只承担召回职能。故**外显的 rescore 分量缺席**。

**必须记下的削弱项（本件最重要的负面发现之一）**：**本篇的第 3 步在功能上执行了一次隐式的
候选裁决**——候选实体全部进入 prompt，Whisper 在二次解码中**同时**条件于音频与候选集，
其解码过程本身就在候选间做取舍。这不是显式 rescore 阶段，但它**确实完成了「多候选择一」**。

因此：
- **R2 不得声称「本篇不做任何候选裁决」**——那是可被反驳的强句。
- **R2 的 delta 必须精确表述为**：「**外显、可标定、与解码分离的世界知识 rescore 分量**」，
  而非「任何形式的候选裁决」。本篇占据的是**核内隐式裁决**（裁决混在二次解码里、不可读出、
  不可标定、无独立的知识信号）；R2 主张的是**核外可读出的标量裁决**。
- 这条与 D2-Speech-Hands 条目的既有 delta 表述（「模型外计算的 training-free 可标定标量 +
  外显阈值；其证伪的是模型内口头仲裁」）**结构完全同型**，可直接复用其措辞纪律。

### 6.3 声学 key 检索 —— **一半 `ABSENT_PROBABLE`、一半 `UNRESOLVED_PENDING_FULLTEXT`**

这是本件唯一判不下来的一项，也是**全文获取义务的第一优先动因**。必须拆成两问：

**问 A：检索的查询来自音频还是文本？——`ABSENT_PROBABLE`（查询=文本）。**
摘要第 2 步是 "fuzzy matching **the ASR result** with a knowledge base"【摘】——被匹配的对象是
**第 1 步产出的文本假设**，不是音频、不是声学嵌入、不是任何音频侧表征。故本篇的检索 key 通道
是**文本派生**的，未占据 R2 的「以音频侧表征为检索 key」这一形态。

**问 B：该文本模糊匹配是字面的还是拼音/音素级的？——`UNRESOLVED_PENDING_FULLTEXT`。**
摘要只给了 "fuzzy matching" 四个字，**没有说明相似度定义**。而这是中文 ASR 实体纠错场景：
**中文同音/近音混淆是该任务的主要错误来源，拼音级模糊匹配是该领域的常规做法**【推】。
因此「fuzzy matching = 拼音编辑距离」与「= 汉字字面编辑距离」**在摘要证据下等概率兼容**。

**对 R2 的处置（三条）**：
1. **R2 不得声称「声学/语音学 key 通道在本篇缺席」为已核实**。该断言目前是 UNRESOLVED；
   若全文显示本篇用拼音级匹配，则本篇同时占据「语音学 key 检索」形态位（与 Lei 的 G2P/音素
   编辑距离、RAC 的 ANE 同族），R2 §2.3 的 key 选型章须相应增列一个中文域先例。
2. **但 R2 的精确 delta 表述在两种结局下都存活**：即便是拼音匹配，其 key 仍由**文本串重建的
   期望发音**而来，不是**该次发音的实际声学**——这与 D2-RAC 条目对 ANE 所下的限定
   （「不回音频 ≠ 无声学信息……R2 的 delta 须精确到『该次发音的实际声学 vs 文本串的先验期望
   发音』」）**逐字同型**。**结论：只要 R2 一律使用该精确表述，问 B 的结局不影响 delta 成立。**
   这是本件对 R2 最有价值的防御性发现——它把一个未决风险**提前中和**了。
3. **反向注记**：本篇的第 3 步确实让**实际声学**参与了最终裁决（Whisper 二次解码读音频）。
   所以在**整条管线**的层面上，本篇并非「不用实际声学」；它只是**不用实际声学做检索 key**。
   R2 在引用本篇时必须区分这两个位置，否则会被反驳「你说人家不用实际声学，可人家重跑了 Whisper」。

### 6.4 双源调度 —— `ABSENT_PROBABLE`，并附一条**结构性发现，建议改动 R2 臂族**

**证据**：摘要给出的是一条**固定串行序**：解码 → 检索 → 重解码【摘】。**只有一个外部源
（知识库）**，且检索与重听**不是两个可选动作**——检索的产物是重听的输入。摘要中无源选择、
无预算分配、无「这次该重听还是该查库」的判断。

**论证**：R2 的「双源同尺度门控选择」预设两个动作是**可替代的臂**（在同一尺度上比较其信息
增益，选其一或分配预算）。本篇不存在这个决策问题，故未占据该分量。

**结构性发现（本件第二条重要负面发现，建议直接改 R2 §5.3/§6.2 臂族）**：
本篇展示的是**串行复合**（retrieval → re-decode）而非**互斥选择**。这是一个**在语音域已被
实证走通的、比 R2 的「二选一调度」更自然的组合形态**。R2 现有臂族把两源当作互斥或加权分配，
**没有一条臂对应「先检索、再把检索结果喂给重听」的串行复合**——而这恰恰是本篇（以及 Lei 的
「检测→检索→上下文化解码」）的实际形状。

**建议**：R2 §5.3 对照臂清单**新增一条 `serial-composition` 固定档臂**（无门控、检索结果无条件
喂入重听），作为 incumbent 而非 ablation。理由有三：
- 它是**本篇的直接可运行复现**，把「已占据的动作」变成 R2 必须超过的**具名基线**，而不是
  一个只在 prior-difference 表里被承认的先例；
- 若 R2 的门控调度臂**打不过**这条无门控串行臂，则 R2 的门控增量在语音域直接被证伪——
  这是一条干净的 kill criterion，符合 §7 的 K 系列体例；
- 它与 §5.3 已有的 `re-resolve-count-matched 固定档`（D2-NAP 条目建议、已收录）**互补**：
  后者控重听次数，前者控**组合拓扑**。

### 6.5 汇总表

| R2 delta 分量 | 本篇判定 | 等级 | 残余风险 |
|---|---|---|---|
| 回音频重解析动作 | **已被占据** | 摘要级 CONFIRMED（环 2 双源一致） | 无（这是正向占据，证据充分） |
| 门控动作选择 | 缺席 | `ABSENT_PROBABLE` | 匹配阈值/空候选退化分支未知；但均落准入侧或数据触发，不改结论 |
| 世界知识 rescore | 外显分量缺席 | `ABSENT_PROBABLE` | **隐式核内裁决存在**；R2 措辞须收窄到「外显可标定」 |
| 声学 key 检索 | 查询=文本（缺席）；相似度定义未知 | 问 A `ABSENT_PROBABLE`／问 B `UNRESOLVED` | **中文拼音匹配可能性高**；但 R2 的精确 delta 表述在两种结局下均存活 |
| 双源调度 | 缺席（单源、串行、无选择） | `ABSENT_PROBABLE` | 无实质风险；但暴露 R2 臂族缺 `serial-composition` 档 |
| training-free | 疑似成立（本篇自身属性，非 R2 delta） | `PROBABLE` | 若全文有训练组件，则 §5 环 4 失效、环 1–3 不变 |

## 7. 全文获取义务（登记）

**本件状态 = 未完成的 D2。** round-14 MAJOR-2 的处置条款要求「v16 交付前完成两篇的 **D2 级**
源核与 ledger 登记」。本件因 IEEE 付费墙**无法达成 D2 级**，故：

- **MAJOR-2 只能部分关闭**：本篇的「占据判定」已足以支撑 §8 † 注的回写（该用途对证据的要求是
  存在性，摘要+转述已足够，见 §1.3 第 4 条）；但「D2 级源核」这一字面要求未成就。
  **本件不主张 MAJOR-2 已关闭**——是否接受 D1 级作为该分量的关闭条件，是**评审/owner 的裁决**，
  不是本件可自裁的事项。
- **ledger 已如实记录**（第 1324 行 `DOI_METADATA_ONLY/NO_FULLTEXT`），无伪装成 fetch 成功行，
  证据链无污染。

**升格触发条件与动作**：若后续通过**合法**途径获得全文（机构 IEEE Xplore 订阅、作者主页/
ResearchGate 的合规副本、或作者索取），**立即**执行：

1. 落盘至 `speechrl-data/survey-fulltext/doi-10.1109-BigData59044.2023.10386366/`，
   补 ledger 行（`kind: pdf`、`sha256`、`bytes`、`access_class` 改为实际取得类），
   **本条目原地升为 `read_level: D2_DEEP_READ` 并全文改写**（本条目为 current 层工作件，
   非审计层，可原地更新；升格时须在 `supersedes` 记录 D1 版的 git blob）。
2. **复核优先级（按对 R2 的承重度排序，逐项已在正文标注）**：
   - **P0 — §6.3 问 B**：模糊匹配的相似度定义是字面还是拼音/音素级？（决定是否新增中文域
     语音学 key 先例）
   - **P0 — §3.1 第 2 点**：prompt 注入是否真为 Whisper 公开 prompt 通道？是否用官方 API？
     是否有 prompt 侧适配/微调？（决定「近 API-only」刻画是否成立）
   - **P1 — §3.1 第 3 点**：全流程是否真零训练？（决定 §5 环 4；不影响环 1–3）
   - **P1 — §6.1**：是否存在按样本的动作条件（阈值、空候选跳过分支）？其形态是准入侧还是
     采集侧？
   - **P1 — §6.2**：是否存在独立于二次解码的 rescore/排序阶段？
   - **P2 — §4**：CER 的实际数字、基线族、消融、AISHELL-NER 的切分与规模、知识库规模与
     公开状态、Whisper 型号与是否中文微调版。
   - **P2 — §6.4**：是否报告过「不重跑、只做文本纠正」的对照臂？若有，即是本篇内部的
     `serial-composition` vs `text-only` 差分，直接可用。
3. **升格后须回写的下游件**：R2 draft §8 † 注与矩阵、§9 调研义务清单（划掉本篇）、
   D2-RAC 条目 §6.1 的「两篇未进读集」表述、round-14 MAJOR-2 的关闭记录。

**姊妹件**：MAJOR-2 点名的第二篇 = Wang et al., "Retrieval augmented end-to-end spoken dialog
models", ICASSP 2024, pp. 12056–12060（RAC `main.bbl` 第 105–109 行 `ragdst`【书】），
**尚未处理**——MAJOR-2 在其完成前无论如何不可宣布关闭。

## 8. 本件对 R2 的净输入（三句话）

1. **R2 的「回音频重解析」分量新颖性 = 零**，已被本篇在语音域、Whisper 上、prompt 层、
   疑似零训练地占据；§8 † 注必须从「有先例」升级为「具名占据」，独立性全部押在合取上。
2. **R2 的其余四个分量在本篇内均未见占据**，但两处措辞必须收窄：世界知识 rescore 要限定为
   「外显可标定」（本篇有隐式核内裁决）；声学 key 要限定为「该次发音的实际声学 vs 文本串的
   期望发音」（本篇的匹配是否拼音级未决，但该限定使结论对两种结局都免疫）。
3. **R2 臂族应新增 `serial-composition` incumbent 档**（检索 → 无条件喂入重听），
   本篇即其可运行原型；R2 的门控调度若打不过这条臂，门控增量在语音域即被证伪。
