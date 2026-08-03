---
artifact_id: "SF-STAGE1C-R2-DATA-CLOSURE-2026-08-02"
title: "R2 论文载体的本地可复现性审计、Stage-2 数据闭包与分波次获取计划"
date: "2026-08-02"
status: "ACQUISITION_CLOSED__D0_COMPLETE__D1_D4_PENDING__MODEL_EXECUTION_WITHHELD"
scope: "R2 开题报告中会改变 Stage-2 实验设计的承重论文、主载体、复制载体、诊断载体和强制对照；不把所有引用论文的数据集都升级为下载义务"
authority_boundary: "owner 于 2026-08-02 授权本文覆盖的数据获取、派生、完整性核验与唯一 lock 整编；仍未授权模型/API、实验、指标结果、独立 study 建仓或发布"
---

# R2 论文载体的本地可复现性审计、Stage-2 数据闭包与分波次获取计划

> 执行状态不在本工作件维护。数据身份、下载状态、阻塞原因与验证收据的唯一当前权威是
> `docs/datasets.lock.json`；旧 candidate/gap manifests 已退役为无事实 pointer。

## 2026-08-02 获取闭包快照（非当前状态权威）

本计划的授权获取波次已结束，正式状态仍只读 canonical lock：

- Stage-2A 核心包 Earnings21、Earnings22、ConEC 均为 `COMPLETE`，D0 已关闭；
- PRISM、Rare5k 重建、BuzzWord、TED-EL 标注、ATCO2-1h、Eka-Medical、LibriSQA 亦已完成；
- SQA-5 与 ContextASR-Bench 分别保留为可续传 `PARTIAL`，不阻塞 Stage-2A；
- Earnings22 上游遗漏了 125 个 MP3 的 LFS attribute；本地获取器显式补规则、逐 OID
  materialize，并在复制后以 1,203 条 SHA-256 清单复核，残留 pointer 为 0；
- Rare5k 的公开可审计重建得到 83,949 个 rare words，和论文约 209.2k 不一致，因此只标为
  reconstruction，不冒充论文原工件；
- 下一步是 D1-D4 的无模型 loader、对齐、泄漏和评测协议闭包，不再扩大数据下载面。

审计收据：`docs/checks/audio-aware-evidence-acquisition/2026-08-02-acquisition/README.md`
（原写作 `docs/checks/r2-stage2a-data/`；按 2026-08-02 目录重整决议，工程路径面改用语义
slug，候选编号只留 provenance）。

## 一、结论先行

### 1. 是否还应继续用开放式论文扫描阻塞 Stage 2

**不应。** R2 已经具备进入工程闭包的条件；本节以下缺口判断是下载前审计基线，已由上方
闭包快照 supersede，当前事实只读 canonical lock：

- 本地已有大量通用语音/音频资产，且 `docs/datasets.lock.json` 中的 28 个冻结基线均标为
  `COMPLETE`；
- 但 R2 冻结的主载体不是这些通用资产，而是
  **Earnings21 音频与评测层 + Earnings22 dev 层 + ConEC 上下文及修订参考层**；
- 这三件当前均不在本地数据根目录；
- 其中数据本身公开且工程上可取得，因而这是**可计划消除的数据缺口**，不是继续扩大文献面的理由；
- ConEC、RECOVER、PRISM、RECAST、BR-ASR 等论文即使数据可取得，公开代码、prompt、检查点和
  协议参数也不足以支持“逐数字复现”。Stage 2 应预注册为**同数据、同信息边界的强重实现**，不能把
  “等待作者放出完整工件”设为开工条件。

**建议的开工裁定**：owner 一旦授权获取 Wave 1，并且
`Earnings21 + Earnings22 + ConEC` 通过本文 §七的数据闭包门，立即进入 Stage-2A 第零步；
不要等待 SLUE-SQA-5、ContextASR-Bench、TED-LIUM3 或 PlanRAG-Audio 全载体到齐。

### 2. 当前数据结论

| 裁定 | 数据/工件 | 当前结论 |
|---|---|---|
| **本地可直接用** | LibriSpeech | 冻结 lock=`COMPLETE`，约 115.2 GB；可承载 LibriSpeech/Rare5k 协议，但 Rare5k 词表须按协议重新派生并固定 |
| **本地存在但不是 R2 主载体** | Spoken-SQuAD | 冻结 lock=`COMPLETE`，约 3.2 GB；可作低成本 Spoken-QA 先导，不等价于 SLUE-SQA-5 |
| **本地存在但布局非原版** | AISHELL-1 | 约 20.16 GB、41 个 parquet；完整 train/dev/test，但不是原始 OpenSLR wav 树；可用于 BuzzWord/中文 NEC 的相邻验证，不能冒充原布局逐字节复现 |
| **主载体本地缺失、公开可得** | Earnings21、Earnings22、ConEC | Stage-2A 唯一开工阻塞；应优先获取和 pin |
| **公开可得、非开工阻塞** | PRISM、SLUE-SQA-5、ContextASR-Bench、BuzzWord、TED-EL 标注、LibriSQA、AMI、ATCO2-1h、Eka-Medical | 按实验价值分波次获取；不能一次性全拉 |
| **当前来源不稳定/需额外许可** | TED-LIUM3、Common Voice 22、MSP-Podcast、IndicVoices | 先解决来源或使用条款，不进入 Wave 1 |
| **不能精确取得或复现** | 私有 750h 生产流量、PRISM 企业医疗集、RECOVER 未发布实体表/prompt、GRGA LongAudioQA、AudioSet 原始音频的稳定快照 | 只作引用、方法重实现或排除项，不设下载任务 |

### 3. 磁盘结论

2026-08-02 只读检查：E 盘总计约 3815.43 GB，已用约 772.57 GB，空闲约
**3042.86 GB**。磁盘容量足够执行本文全部推荐波次；当前主要风险是**数据身份、许可、版本、上下文
与参考转写的对齐**，不是空间。

---

## 二、收敛规则：把“文献扫描”改成“复现闭包”

### 2.1 四层论文/数据义务

从本件起，将 R2 论文分为四层：

1. **E0 引用层**：只说明研究现状或方法坐标，不下载数据；
2. **E1 结构重实现层**：公开方法足以实现相同信息边界，但无完整代码/prompt/检查点；只下载 R2
   所需载体，不追求原论文逐数字复现；
3. **E2 强制对照层**：会进入实验表的对手，须固定数据、协议和实现版本；
4. **E3 主/复制载体层**：决定 R2 核心结论，必须完成字节、许可、切分、标注和评价脚本闭包。

R2 当前 E3 只有：

- 主：Earnings21 + ConEC；
- dev/标定：Earnings22 + ConEC；
- 复制：TED-LIUM3（但可在主载体第零步之后到位）；
- O 臂主锚候选：SLUE-SQA-5（不作为 NB 主线开工前置）。

### 2.2 新论文只有四种情况可以重新打开 Stage-1 扫描

Stage 2 启动后，新论文默认只进入周度 delta ledger，不改变工程计划。只有满足下列任一条件才
`STOP-THE-LINE`：

1. 与 R2 **同任务、同信息边界、同公开载体**，且给出更强可运行基线；
2. 证明主载体、许可、指标或 test-gold 信息边界无效；
3. 发布当前某个强制对照缺失的代码、prompt、检查点或精确数据快照；
4. 改变最小实验的因果解释，例如证明“知识增益”实际来自参考转写泄漏或新增代答模型。

其他新增论文只补引用，不回滚开题、不扩展下载清单。建议 Stage 2 后采用**每周一次、限时 30 分钟**
的 delta scan，不再做无界深扫。

---

## 三、审计口径与证据边界

### 3.1 “本地存在”不等于“论文可复现”

本件分开判断五层：

| 层 | 问题 |
|---|---|
| 字节层 | 音频、文本、标注是否实际在盘，而非只有目录、README、LFS pointer 或代码仓库？ |
| 身份层 | 是否能固定到官方 revision/commit，并生成文件清单与 SHA-256？ |
| 协议层 | split、切片、词典、实体表、上下文、normalizer 和指标定义是否明确？ |
| 实现层 | 代码、prompt、超参、检查点和宿主模型接口是否公开？ |
| 数字层 | 能否合理预期复算论文表格，而不是只能实现同类方法？ |

本文使用三种可复现性标签：

- **DATA-READY**：数据字节和标注可固定；
- **PROTOCOL-READY**：可按公开信息建立等价实验协议；
- **PAPER-EXACT**：有足够工件复算论文数字。

多数 R2 近邻至多达到前两档；这不妨碍 Stage 2，但必须限制复现措辞。

### 3.2 本地盘点方法与局限

- 读取了 `docs/datasets.lock.json`、`docs/datasets.candidates.json`、
  `docs/datasets.gap-candidates.json`、`docs/data.md` 和现有 fetch/inventory 脚本；
- 对实际数据根
  `E:/chao_workspace/exploring-l4-intelligence/speechrl-data/datasets` 做了顶层目录枚举和
  R2 目标名定向检查；
- 全量 `scripts/data/inventory.sh` 两次因遍历数百 GB 资产耗时过长，未获得完整收尾报告；因此本文
  对“本地不存在”的断言限于**已知标准目录名、lock/candidate 记录、repo/_repro 定向搜索均无命中**；
- 这足以判断 R2 主载体缺口，但下载后仍须用正式 inventory 生成收据；
- 所有网络核验只读，未触发任何数据下载。

---

## 四、本地现状：哪些承重数据已存在

### 4.1 可直接承载实验的数据

| 数据 | 本地路径 | 状态 | 能做什么 | 不能声称什么 |
|---|---|---|---|---|
| LibriSpeech | `speechrl-data/datasets/librispeech` | lock `COMPLETE`，约 115.2 GB | BR-ASR/RECAST/PRISM 的 LibriSpeech 协议；Rare5k 派生；通用 ASR 回归 | 不能因此声称 BR-ASR/RECAST 已可精确复现；二者代码/训练件不完整 |
| Spoken-SQuAD | `speechrl-data/datasets/spoken-squad` | lock `COMPLETE`，约 3.2 GB | Spoken-QA loader、指标和先导样本 | 不等价于 SLUE-SQA-5 的五源问答与 Spoken Wikipedia 文档层 |
| AISHELL-1 | `speechrl-data/datasets/aishell-1` | 41 个 parquet、约 20.16 GB | 中文 ASR/NEC 相邻验证 | 本地为 repackaged parquet，不是原始 OpenSLR 目录；须记录转换身份 |
| SLUE toolkit | `speechrl-data/repos/slue-toolkit` | 已 pin `ed23039507c8f01b704a5c43ed89b6e808a49405` | 预处理与评测代码参考 | 只有代码，没有 SLUE Phase-2/SQA-5 数据 |

### 4.2 明确不在本地的 R2 目标

定向检查未发现以下数据目录或已 pin 的等价数据资产：

`earnings21`、`earnings22`、`conec`、`ted-lium3`、`ted-el`、`prism`、`rare5k`、
`contextasr-bench`、`slue-sqa-5`、`buzzword`、`ami`、`msp-podcast`、`voxpopuli`、
`audioset`、`atco2`、`eka-medical`、`common-voice`、`indicvoices`。

其中 Rare5k 是 LibriSpeech train-960h 的派生词频协议，不应机械地视为独立大数据下载；其余按下文
分类。

---

## 五、承重论文—数据—复现性矩阵

### 5.1 Stage-2A 开工阻塞：主载体与 dev

| 数据/论文 | 官方可得性 | 本地 | 数据复现 | 论文数字复现 | 裁定 |
|---|---|---|---|---|---|
| **Earnings21** | Rev 官方仓库公开：44 files、约 39h，含完整音频、转写、speaker/punctuation/entity tags；HF `Revai/earnings21` 是 16 kHz 转码便利版，约 4.23 GB，但官方卡明确提示高级用法应回原仓库 | 缺失 | **高**：可 pin 官方 Git commit；E21 不需 LFS | 中：各论文切片、normalizer、参考版本不一致 | **Wave 1 必取原仓库版**；HF 版只能作缓存/快速读取备份，不能替代原始实体层 |
| **Earnings22** | 同一官方仓库公开：125 files、约 119h，完整音频、转写和地区/公司元数据；音频受 Git LFS 管理 | 缺失 | **高**：公开可得 | 中低：无 E21 同型逐 token 实体标注，R2 必须另定 dev reward/实体标注合同 | **Wave 1 必取**，用作所有阈值、prompt、候选宽度和停止规则的 dev/标定集 |
| **ConEC E21/E22 层** | 官方仓库公开，含 PDF、抽取词表、participant names、修订 `.nlp`、timestamps、WER tags 和纠错日志；数据仓当前 head 可 pin | 缺失 | **中高**：发布后的修订层可固定使用；但修订过程借助不公开 S&P transcript，无法独立重建/审计 | **低**：论文只指 icefall 根，无现成 ConEC recipe，未报关键 λ/检查点；不能期待逐数字复现 | **Wave 1 必取**；R2 只声称使用公开修订工件并重实现同信息边界，不声称重建其 gold 生成过程 |

主载体版本建议（获取执行时仍须重新读取远端 head，若变化则 owner 选择是否升级）：

- `revdotcom/speech-datasets@c05ab6fd8b4b627d123c922a22a39e993dd37635`；
- `huangruizhe/ConEC@88440713d8b80dc4f19b225f6480237e78c379de`。

**许可门**：Earnings21 HF 卡标 `CC-BY-SA-4.0`，但 Rev GitHub 根未被 GitHub API 识别出机器可读
license；ConEC 论文为 `CC BY-NC 4.0`，但数据仓没有清晰仓库级 LICENSE，且修订参考含 S&P 专有
转写派生内容。**下载用于本地研究可先做，但任何二次分发、镜像或公开 lock 前必须由 owner 明确许可
口径。**

### 5.2 强制对照与诊断：数据可得不等于系统可复现

| 数据/对应论文 | 官方可得性与规模 | 本地 | 数据/协议裁定 | 系统复现裁定 | 优先级 |
|---|---|---|---|---|---|
| **PRISM entity-rich** | GitHub 发布四类实体数据，音频由 Google Drive 提供；README 标 CC BY-NC 4.0 | 缺失 | DATA-READY，规模较小；全合成 VITS，只能作声学/词典诊断 | 仓库只见数据，无论文方法完整实现；PRISM 还需白盒隐状态和改 beam，R2 API-only 下不可同边界运行 | **Wave 2** |
| **Rare5k** | 不是独立语料；协议是在 LibriSpeech train-960h 中 top-5k 为 common、其余约 209.2k 为 rare | LibriSpeech 已在 | 可本地派生；须固定 tokenizer、大小写、标点、词频并导出 hash | BR-ASR 未给足以精确复算的公开工程；只能重建数据协议/比较公开数字 | **Wave 2，无大下载** |
| **RECAST** | GitHub 存在，但 README 截至核验日仍写 “Code will be added soon” | repo/data 均未 pin | 其公开载体 LibriSpeech 已有；PRISM/IndicVoices 未有 | **PAPER-EXACT 不成立**；方法还需训练 retriever、读 decoder state、接管解码环 | E1 结构参考，不阻塞 |
| **BR-ASR** | 使用 LibriSpeech+Rare5k，200k 词表来自本地可派生协议 | 数据主体已在 | PROTOCOL-READY | 论文训练 10 epochs×960h、复用 bias-trained 后端且未形成可运行公开闭包；不应为开工重训 | E2 读数对照/协议对照；实现另立预算 |
| **Generative Annotation / BuzzWord** | GitHub 公开数据，Apache-2.0；HF `Luo9766/BuzzWord` 1500 rows，仓库约 1.37 GB | 缺失；AISHELL-1 已在 | BuzzWord DATA-READY | 仓库主要是 data，未给论文模型代码/检查点和足够超参；不能逐数字复算 | Wave 2 或中文扩展时取 |

### 5.3 O 臂与第二公开载体

| 数据 | 可得性 | 本地 | 规模/许可 | 复现裁定 | 下载裁定 |
|---|---|---|---|---|---|
| **SLUE-SQA-5** | 官方 HF `asapp/slue-phase-2` + 本地已有官方 toolkit | 缺失 | `sqa5` config 50,915 rows；原文件/Parquet 约 **109.965 GB**，全仓约 261.649 GB/页面报 281 GB；SQuAD/NQ/WebQuestions/CuratedTREC 部分与 Spoken Wikipedia 为 CC BY-SA 4.0，TriviaQA 部分 Apache-2.0 | DATA-READY、PROTOCOL-READY；无需等待其他 Phase-2 configs | **Wave 3，仅取 `sqa5` config**；不是 NB 主线开工门 |
| **Spoken-SQuAD** | 已冻结 | 已有 | 约 3.2 GB | 可先导，但任务分布窄于 SQA-5 | 先用本地做 loader/评测，不新增下载 |
| **ContextASR-Bench** | 官方 HF + GitHub evaluation code，MIT；41,329 rows、双语、Speech/Dialogue 两 config | 缺失 | HF repo 实际约 **90.024 GB**；官方卡/代码均公开 | DATA-READY、PROTOCOL-READY；比 RECOVER 的其他四个载体信息边界更干净 | **Wave 4 优先于 TED-LIUM3**，作第二公开实体上下文载体 |

### 5.4 复制与实体链接载体

| 数据 | 当前可得性 | 本地 | 复现问题 | 裁定 |
|---|---|---|---|---|
| **TED-LIUM3** | 论文/历史 loader 指向 OpenSLR 51；截至核验日 `https://www.openslr.org/51/` 显示 Resource not found，历史 archive URL返回 404；HF `LIUM/tedlium` loader 仍依赖该失效 URL | 缺失 | 不是“公开链接写过”就等于今天可稳定取得；历史 SHA-256 可用于镜像验真，但镜像许可与完整性须核 | **暂记 SOURCE-UNSTABLE**；不阻塞主载体第零步。只接受与历史 hash 匹配的可信镜像，不把随机网盘当权威源 |
| **TED-EL** | `BITHLP/TED-EL` 标注仓公开，当前可 pin；音频依赖 TED-LIUM3 | 缺失 | 论文未声明数据许可；无完整模型代码/关键超参，split 也存在未解项 | 标注 DATA-READY，但完整载体被 TED-LIUM3 阻塞；PAPER-EXACT 不成立 |

建议版本：`BITHLP/TED-EL@1338e98bccb29badc34dabf17d08c11642d54189`。在 TED-LIUM3
上游恢复或找到 hash 一致的可信镜像前，不创建“下载成功”的假计划。

### 5.5 只作方法参考、不得阻塞 Stage 2 的论文载体

| 论文/载体 | 数据状态 | 为什么不下载或不能声称精确复现 |
|---|---|---|
| **RECOVER**：Earnings21 / ATCO2 / Eka-Medical / Common Voice 22 / ContextASR | E21 缺且列入 Wave1；ATCO2 1h 研究子集公开；Eka HF 约 0.262 GB；CV22 通过 Mozilla Data Collective；ContextASR 公开 | 作者未发布代码、prompt、五集实体表及精确匹配规则；E21/Fox 表和 Common Voice 实体表还可能由 test gold 派生。R2 只在自己的 E21+ConEC 合法信息边界上重实现 1-Best/选择策略，不需先拉齐其他四集 |
| **PlanRAG-Audio**：LibriSpeech+LibriSQA / AMI / MSP-Podcast / VoxPopuli+AudioSet | LibriSpeech 已有；LibriSQA 元数据公开且很小；AMI CC BY 4.0 公开；MSP-Podcast 需提交访问/共享联系信息；VoxPopuli 公开；AudioSet 官方只稳定提供 CSV/特征，原始音频来自会失效的 YouTube IDs | 论文称公开复现，但截至核验未找到已发布代码/构造脚本；长音频多为 concat/crop 和作者生成摘要。全量获取成本高且不服务 R2 第零步，列 E0/E1，不建下载波次 |
| **GRGA / LongAudioQA** | GitHub 只有 partial code，README 明说完整数据将在接收后发布 | 数据未发布，不能下载；不把 partial repo 误写成可复现 |
| **2021 N-best entity retrieval** | 私有 750h 生产语音 | 不可获得；只复用思想，不创建获取任务 |
| **PRISM 企业医疗集** | 私有 | 不可获得；公开 synthetic/entity-rich 部分与企业部分必须分开 |
| **AudioSet raw audio** | 官方发布标签 CSV 和 2.4 GB 特征；原始 wav 不由官方稳定分发 | 视频删除造成快照漂移；除非论文给出固定派生快照，否则不能作为逐字节复现载体 |

---

## 六、分波次获取计划

### 6.1 Wave 0：授权后的元数据与许可预检（小时级，不拉大文件）

**目标**：先把所有大下载变成 manifest 条目，杜绝 ad-hoc `git clone`/`hf download`。

执行项（2026-08-02 已获授权并启动）：

1. 把 `earnings21-original`、`earnings22-original`、`conec`、`prism-public`、`slue-sqa-5`、
   `contextasr-bench`、`buzzword`、`ted-el-annotations` 直接纳入唯一 `datasets.lock.json`；
2. 每项记录 source、revision、预计字节、许可、访问级别、role、目标目录和验证规则；
3. 对 GitHub/HF 只取元数据与 file list，生成预计下载量；
4. 将“repo 公开但 license 不清”明确写入 license/claim-limit，不把可下载误写成可再分发；
5. 不把 TED-LIUM3 放入可自动执行队列，先设 `SOURCE_UNSTABLE`。

Wave 0 已完成 schema/来源整编；下载与字节验证状态只读 canonical lock。

### 6.2 Wave 1：Stage-2A 最小开工包（必须）

**内容**：Earnings21 original + Earnings22 original + ConEC。

**空间预留**：先预留 **100 GB**，以覆盖 Git/LFS、工作树、校验缓存和后续 16 kHz 规范化副本；实际
字节数在 Wave 0 的 LFS manifest 后收紧。

**执行设计**：

- 在 WSL2 `Ubuntu-24.04` 下，目标根使用
  `/mnt/e/chao_workspace/exploring-l4-intelligence/speechrl-data`；
- Rev 仓使用 sparse checkout，只保留 `earnings21` 与 `earnings22`；Earnings22 再执行限定目录的
  `git lfs pull`，下载后检查没有残留 LFS pointer；
- ConEC 独立 clone 到 `repos/`，数据视图通过 loader 指向该 pin，不复制 PDF/转写到多个目录；
- 记录 Git commit、LFS OID/size、逐文件 SHA-256、总时长、采样率、call 数；
- E21 应核到 44 calls/约 39h，E22 应核到 125 calls/约 119h；偏离即失败；
- 做 E21/E22 ↔ ConEC call-id 覆盖表，分别报告音频、原参考、修订参考、PDF、participant names、
  extracted word list、timestamps、WER tags 的存在率；
- 许可说明和“ConEC 修订参考不能独立重建”的 provenance notice 与数据收据一起落盘。

**Wave 1 通过后即可进入 Stage-2A；后续波次不得继续阻塞。**

### 6.3 Wave 2：小体量诊断闭包

**内容**：

- PRISM entity-rich 数据和音频；
- 从本地 LibriSpeech 派生并 pin Rare5k 词表；
- BuzzWord（若中文 NEC/发音纠错进入近期 sprint）；
- 只 clone RECAST/Generative Annotation 等代码仓的固定 revision，用于核实“数据-only/代码未发布”状态，
  不承诺跑通论文系统。

**空间预留**：15 GB。Wave 1 loader 稳定后再执行。

### 6.4 Wave 3：O 臂数据

**内容**：仅 `asapp/slue-phase-2` 的 `sqa5` config；不拉 hvb/ted/vp_nel。

**空间预留**：至少 **250 GB**，覆盖约 110 GB 原/Parquet 数据、HF cache 和处理副本。若 loader 可以
直接以单一缓存消费，优先避免重复 materialization。

**执行条件**：Spoken-SQuAD 上的 O-arm loader、指标、evidence contract 已先跑通；否则先拉 110 GB
不会降低工程风险。

建议 pin HF revision：`e2989c55a53593a8e39b8f8ebdb47ccaccbe484a`；执行日如发生更新，
须重新选择版本而不是默默跟随 `main`。

### 6.5 Wave 4：第二公开载体与复制载体

优先顺序：

1. **ContextASR-Bench**：约 90.024 GB，MIT，数据和 evaluation code 都公开，且上下文层比 RECOVER
   其他载体更干净；建议 pin HF
   `7906fd98d1d093bf244df80e726e07fc8afed6a6` 与 GitHub
   `897de87bd4eb430de28dca807fc725958c7ebc85`；
2. **TED-LIUM3 + TED-EL**：只有在可信来源恢复并与历史 hash 一致后执行；预留 150–200 GB；
3. 需要时再获取 ATCO2-1h、Eka-Medical，验证 RECOVER 跨域趋势；不获取 ATCO2 5281h 训练集；
4. Common Voice 22、MSP-Podcast、IndicVoices 需 owner 明确接受访问/许可条款后另立 acquisition item。

### 6.6 明确延期/不下载

- SPGISpeech 5000h：ConEC 用其训练 ASR 和定义 rare word，但 R2 第零步不需要重训该识别器；
- PlanRAG-Audio 的 AMI/MSP/VoxPopuli/AudioSet 全组合：方法参考，不是 R2 最小实验；
- GRGA LongAudioQA：未发布；
- 私有 750h、PRISM 企业医疗：不可获得；
- 全量 Common Voice 22：RECOVER 的实体表未发布，拉全量不能恢复其论文协议；
- 全量 SLUE Phase-2 281 GB：只需 `sqa5`，禁止无差别 snapshot。

---

## 七、Stage-2 数据闭包门

Wave 1 必须同时满足以下条件，才能把 R2 状态从“开题分析”切到“第零步工程”：

### Gate D0：身份与字节

- [x] 两个 Git repo revision 已固定；
- [x] Earnings22 所有 LFS 文件均已 materialize，无 pointer 残留；
- [x] 文件清单、总字节和 SHA-256 收据已生成；
- [x] E21=44 calls、E22=125 calls，时长量级与官方说明一致。

### Gate D1：跨层对齐

- [ ] 每个 E21/E22 call 的 audio、原 reference、ConEC 修订 reference、context 文件映射明确；
- [ ] 缺 PDF/participant/timestamp/tag 的 call 被显式列出，而不是静默过滤；
- [ ] 原参考与修订参考双报路径可由同一 sample id 访问。

### Gate D2：信息边界与泄漏

- [ ] `available_at`/来源字段可以区分当时可得材料、事后材料、gold/oracle 构造；
- [ ] Fox/RECOVER 类 test-gold 派生词表永不进入 controller 主路径；
- [ ] E21 只作 evaluation，全部阈值/prompt/停止规则只在 E22/dev 冻结；
- [ ] 按 call/company 的 group split 与实体泄漏检查已定义。

### Gate D3：评价协议

- [ ] `fstalign + whisper_normalizer` 版本固定；
- [ ] 对 reference 与自身比较得到零错误的 model-free sanity check；
- [ ] WER、rare-word WER、实体类指标、实体准确率的分母与 normalizer 单测通过；
- [ ] 总 WER 明确为 READOUT_ONLY 时，实验代码不会误把它当主优化目标。

### Gate D4：最小工程读取

- [ ] 10 个固定 smoke samples 可完成 audio decode、原/修订 transcript、三类 context 读取；
- [ ] 10 个样本的 provenance JSON 能完整回溯文件和 hash；
- [ ] 不调用模型也能构造 no-context / real-context / oracle-context 三臂输入；
- [ ] 正式收据写入 `docs/checks/audio-aware-evidence-acquisition/<release-id>/`，通过相关 offline gate。

**D0–D4 通过即进入 Stage 2。** PRISM、SQA-5、ContextASR 或 TED-LIUM3 未下载不影响此裁定。

---

## 八、对“可复现”的最终措辞建议

开题和后续论文应使用以下受限表述：

1. **Earnings21/22 + ConEC**：公开数据工件可取得并可固定；ConEC 修订参考的生成过程包含不可公开
   的 S&P 转写来源，不能独立重建；论文基线无 turnkey recipe，R2 做同载体重实现而非逐数字复现。
2. **RECOVER**：公开评测载体多数可得，但代码、prompt、实体表和规则不全；只重实现其公开算法，并
   用 ConEC 真实上下文替代 test-gold 派生表。
3. **PRISM/RECAST/BR-ASR**：数据协议可复用；系统需要白盒接口、训练件或未发布代码，不能当
   API-only 可运行 baseline。PRISM 公开 synthetic 集只能作诊断。
4. **SLUE-SQA-5/ContextASR-Bench**：数据和评价协议公开，属于可下载的第二阶段载体；不是主载体
   数据缺失的替代品。
5. **TED-LIUM3/TED-EL**：历史公开不等于当前可下载；在 OpenSLR 51 失效期间标为来源不稳定。
6. **PlanRAG-Audio/GRGA**：论文结构值得参考，但作者构造脚本/数据尚不足，不纳入 R2 的逐数字复现
   承诺。

---

## 九、官方来源与本地深读证据

### 9.1 官方数据/代码来源

- [Rev speech-datasets（Earnings21/22）](https://github.com/revdotcom/speech-datasets)
- [Revai Earnings21 HF 卡](https://huggingface.co/datasets/Revai/earnings21)
- [ConEC 数据仓](https://github.com/huangruizhe/ConEC)
- [PRISM 数据仓](https://github.com/AshishMittal/PRISM)
- [RECAST 状态页](https://github.com/AshishMittal/Recast)
- [SLUE toolkit](https://github.com/asappresearch/slue-toolkit)
- [SLUE Phase-2 / SQA-5](https://huggingface.co/datasets/asapp/slue-phase-2)
- [ContextASR-Bench code](https://github.com/MrSupW/ContextASR-Bench)
- [ContextASR-Bench data](https://huggingface.co/datasets/MrSupW/ContextASR-Bench)
- [TED-EL](https://github.com/BITHLP/TED-EL)
- [OpenSLR 51 当前状态](https://www.openslr.org/51/)
- [Generative Annotation / NEC](https://github.com/L6-NLP/Generative-Annotation-NEC)
- [BuzzWord](https://huggingface.co/datasets/Luo9766/BuzzWord)
- [GRGA partial release](https://github.com/tangquanwei/GRGA)
- [ATCO2 官方数据页](https://www.atco2.org/data)
- [Eka-Medical](https://huggingface.co/datasets/ekacare/eka-medical-asr-evaluation-dataset)
- [Mozilla Common Voice](https://www.mozillafoundation.org/en/common-voice/)
- [LibriSQA](https://github.com/ZihanZhaoSJTU/LibriSQA)
- [AMI 下载页](https://groups.inf.ed.ac.uk/ami/download/)
- [AMI 许可](https://groups.inf.ed.ac.uk/ami/corpus/license.shtml)
- [MSP-Podcast](https://www.lab-msp.com/MSP/MSP-Podcast.html)
- [AudioSet 官方下载页](https://research.google.com/audioset/download.html)
- [PlanRAG-Audio](https://arxiv.org/abs/2605.20414)

### 9.2 本地 D2 深读件

- [ConEC D2](d2-entries/2026-08-01-d2-2024-lrec-main-328.md)
- [TED-EL D2](d2-entries/2026-08-01-d2-2024-lrec-main-1365.md)
- [PRISM D2](d2-entries/2026-08-01-d2-2023-emnlp-main-916.md)
- [RECAST D2](d2-entries/2026-08-01-d2-2025-findings-emnlp-203.md)
- [BR-ASR D2](d2-entries/2026-08-01-d2-2505-19179.md)
- [RECOVER D2](d2-entries/2026-08-01-d2-2603-16411.md)
- [PlanRAG-Audio D2](d2-entries/2026-08-01-d2-2026-findings-acl-1304.md)
- [GRGA D2](d2-entries/2026-08-01-d2-2026-findings-acl-1038.md)
- [Generative Annotation D2](d2-entries/2026-08-02-d2-2025-emnlp-main-1052.md)
- [私有 750h N-best retrieval D2](d2-entries/2026-08-02-d2-interspeech-2021-wang21b.md)

---

## 十、owner 决策结论

owner 已在 2026-08-02 给出执行指令，按以下边界落地：

1. **授权数据闭包**：允许刷新 canonical lock、获取并 pin 公开 R2 载体、生成数据收据；
2. **许可处置**：ConEC 修订参考和 NC/条款不明资产只作本地研究使用，未经单独核验不二次分发；
3. **开工边界不变**：下载不等于 Stage-2 模型执行授权；Stage-1C/正式开题现已通过，D1–D4 与
   Stage-2A 执行合同仍须关闭。

不稳定、受限与私有来源继续 fail-closed，不以随机镜像或规避条款代替。
