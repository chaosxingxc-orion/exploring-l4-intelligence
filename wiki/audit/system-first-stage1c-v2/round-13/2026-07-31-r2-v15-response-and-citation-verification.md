---
title: "R2 v15 回应信：round-13 复审的逐条独立核验（17/17 一手源核）与处置"
date: "2026-07-31"
artifact_type: "RESPONSE"
campaign: "system-first-stage1c-v2"
round: "round-13"
responds_to: "round-13/2026-07-31-r2-v14-doctoral-supervisor-literature-and-technical-coreview.md"
responds_to_git_blob: "8bd2b781b9dc70087455207250a3b50d7dffeae8"
review_target_was: "v14 blob ea2cdd0 @ dc5b048"
delivers: "v15（同路径就地演进；本回应落笔时未提交，blob 于提交后由 INDEX 补录）"
rulings_invoked: "Decision-Log 续82（2026-07-31 owner 三裁决 + capability-first 口径确认）"
verification_method: "三路隔离子代理 WebFetch 一手源（arXiv/ACL Anthology/ISCA Archive 摘要页+全文 PDF 抽取），与评审方法与结论互相独立"
authority_effect: "RESPONSE_ONLY_NO_EXECUTION_GRANT"
human_signature_claimed: false
model_or_metric_execution_authorized: false
stage2a_authorized: false
---

# R2 v15 回应：评审承重证据核验属实，裁决接受；三处代拟经 owner 落笔（续82）；八项验收 7 接受 1 拒绝

## 一、总回应

round-13 裁决 `MAJOR_REVISION_REQUIRED_BEFORE_FORMAL_OPENING` **接受**。裁决翻转的程序
合法性经独立核验成立：round-12 失效条件 7 的「知识自构造的发音候选」分支被 PRISM（确认
training-free）合法触发。v15 已按八项验收清单中被接受的七项重构；第 7 项（效率进主判据）
按 owner 续82② 拒绝，理由如实记录于本件 §四。

## 二、逐条独立核验结果（先核验、后回应）

对评审引用的 17 篇一手文献逐篇核验（存在性/书目/表述准确性），方法与评审独立：

**结论：17/17 真实存在，零虚构、零张冠李戴；摘要层表述基本准确。**

核心十篇的裁定性事实与评审刻画的偏差（不翻转评审结论、但 v15 矩阵不照抄评审表述）：

| 篇 | 核验裁定 | 关键事实/与评审表述的偏差 |
|---|---|---|
| PRISM (EMNLP 2023, Mittal et al.) | 属实且刻画准确 | training-free 确认（"without any retraining"）；TTS 逐实体、声学/语言状态 key、推理期 kNN、覆盖 Transducer+Whisper。**评审未展开：需白盒读取 encoder/decoder 隐状态，API-only 黑盒下不可运行**；含手工阈值超参 |
| Lei et al. (arXiv 2409.15353) | 属实；「有训练」偏轻 | 实为 ICASSP 2025；LoRA 微调整个 LLM-ASR 链（46M 可训参数）+独立检测模型+合成个人库训练数据；三段管线刻画逐字准确（检索用 G2P/音素编辑距离 NPD） |
| RAC (arXiv 2409.06062, Pusateri et al.) | 属实且刻画准确 | LoRA 适配 OpenLLaMA-7B；2.6M 实体向量库；**纯文本后处理、不回音频**——提案原「GER 回不到信号」半句在该篇上仍真 |
| DARAG (ACL Findings 2025) | 属实；一处用词错误 | 实为**生成式纠错器，非"comparator"**；检索为 SentenceBERT **语义**检索非语音学；主贡献是合成数据增强（RAC 组件次要）；LoRA 训练 LLaMA-2-7B |
| Siskos et al. (EMNLP Findings 2025) | 属实且三元素逐字确认 | "frozen vocabulary"/"black-box"/"plug-and-play" 均为原文用词；TED-LIUM3/Earnings21/SPGISpeech 恰这三集。**带星号：识别器须暴露 CB/context-list 接口（非任意 API ASR）；评测仅 1.5h/5h/5h 子集且 SPGISpeech 协议有改动；其 CB-RAG 卖点为延迟非精度** |
| RECAST (EMNLP Findings 2025) | 属实；一处倒挂 | 对比训练 retriever+白盒 decoder state 确认；**词表上限 4,000——评审「大词表效率」与 BR-ASR 200k 倒挂**；Hindi 臂实际用 LoRA 适配 Whisper |
| BR-ASR (Interspeech 2025) | 属实 | 200k 词表/20ms 确认；retriever 对比训练+同音负例课程；**「多种下游 ASR」实证仅 Qwen-Audio/SLAM-ASR 两族且均在 bias list 上训练过**；仅 LibriSpeech 英文 |
| WCTC-Biasing (Interspeech 2025) | 属实且两元素逐字确认 | 免重训练+白盒中间层读写确认；**限 CTC/自条件架构；日语 CSJ 系评测；headline 29% 为 OOV 关键词 F1 相对值，CER 并不同步改善** |
| RAG-Boost (MLC-SLM 2025) | 属实；一处重大遗漏 | 2 页 challenge 系统描述稿；四处训练组件；**其自报 raw（未训练）RAG 使 WER 13.83→32.98 恶化——评审未提；该负结果恰是"TF plug-in 非平凡、须门控/准入"的一手证据** |
| Speech-Hands (arXiv 2601.09413) | 属实；场次低报 | **实为 ACL 2026 oral**（评审当预印本引，威胁更强非更弱）；trained（"learnable reflection primitive"）确认——**故 round-12 失效条件 7 第一分支（training-free 双源）未被其触发，触发者为 PRISM 分支** |

次要七篇（huang20f/naowarat23/huang23g/CB-Whisper/gong24b/RASU/2606.29031）：全部属实；
五篇标题被评审截短（不改指称，但 RASU 掉了 "through Generative Modeling"、naowarat23 掉了
"Attention-based…Personalised ASR" 两处承重限定）；RASU 的「speech-to-speech 检索」实为
语音查询→段检索但下游消费**文本**转写+意图标签，范围仅 SLU 意图预测；2606.29031 仅
"Submitted to SLT 2026" 未录用（评审用作风险跟踪件，用法恰当）；两位 Huang 为不同作者。

**读集缺位核验**：全文 ledger（62 行）对十篇核心近邻零命中、"biasing" 零出现、d2-entries
33 篇无涉——评审「提案未读/未列出」前提属实。

**横切事实（对 v15 承重）**：十篇无一同时满足 API-only+training-free（PRISM/WCTC 白盒；
Lei/RAC/DARAG/RECAST/BR-ASR/RAG-Boost/Speech-Hands 含训练；Siskos 黑盒但依赖 CB 接口）——
评审 §一自给的「合取命题」出路经独立核验确实无人占据。

## 三、逐 MAJOR 回应

- **MAJOR-1（近邻承重）**：**接受**。全称句（「biasing 需每句预给候选表且训练进解码器」
  「GER 无检索」）被 Siskos/WCTC/RAC/DARAG 证伪，退役；v15 §8 建近邻十篇 prior-difference
  矩阵（逐篇训练态/信息访问/机制单元/新增变量）+incumbent 五组分组合同；十篇 D2+ledger
  登记列开题前义务第一位。**同时指出**：矩阵不照抄评审表述（上表偏差逐项修正），且按
  续82① 加「2026 重审条款」——2023 时代近邻的承重前提在冻结 omni 核上是否仍成立为
  Stage-2A 复现先行重审对象。发音库机制核定位经 owner 续82① 维持，novelty 锚点迁至合取
  （API-only 黑盒 key × 世界知识 rescore × 门控动作 × 口音/个性化族），§2.3 重写。
- **MAJOR-2（三形式归因）**：**接受并指出部分诉求 v14 已满足**。v15 §6.2 加 ORG/SUPPLY/
  USE/OPT 三层接口纪律+H0/H-SUPPLY/H-USE/H-ORG/H-SYS 假设映射；PS-abl 加三级子消融
  （声学 key vs 朴素语音学／候选检索／世界知识 rescore）；value 定义滑移修正（§1.5/§3.4）。
  **更正评审**：「A3 必须只改变准入」在 v14 已成立（A3=同证据集+准入），「A4b 必须只改变
  供给调度」的隔离（探针共用仪器+K1b β 权重条件）v14 已有——关闭条件中该两句是对既有
  设计的重述而非缺口。
- **MAJOR-3（载体/incumbent PENDING）**：**接受时序裁定**（载体冻结先于开题签字）。
  **更正评审**：v14 §0 已如实披露悬置，不存在遮掩。v15 §5.1 载体候选按一手核验具名入围
  （LibriSpeech+Rare5k／Earnings21/SPGISpeech／PRISM 词典协议）；incumbent 五组合同入 §8。
- **MAJOR-4（规模收窄）**：**部分接受**。三层假设脊柱+条件扩展结构接受（H-ORG 判据化、
  克隆列为①′梯级之后的升级项）；**机制核降级不接受**——owner 续82① 裁定维持（评审此项
  属对象定义权代拟，评审件自身已如实标注 REVIEW_ONLY）。
- **MAJOR-5（TFRL 身份）**：**接受选项一**（owner 续82③：保留 TFRL 并做实）。v15 §3.4
  改身份两档制：档 B contextual bandit 升为身份承载形态（对象/探索/credit assignment/
  离线-在线边界列 §9 义务）；档 A 如实定位 derivative-free 配置优化+等预算优化器对照
  （random/Bayesian/evolutionary）；§6.3 加跨动作族 V̂ 同尺度合同。
- **MAJOR-6（风险反证）**：**6.1/6.2/6.4 接受**（§2.3 检索层对照阶梯含 G2P/编辑距离与
  PRISM 白盒参照上界；§5.4 负类分类学预注册含拒绝改写=合法动作；§0 护城河句改带范围
  可证伪命题）。**6.3 部分接受**：v14 P13N 三臂已是逐级设计+K-PS 逐个降级+伦理边界在案，
  v15 增①′归一化前置梯级；克隆是否升红线第四条仍待 owner（round-12 OBS-1 悬置不变）。

## 四、八项验收处置

| # | 验收项 | 处置 |
|---|---|---|
| 1 | 十篇 D2+prior-difference matrix | 接受；矩阵已入 §8（证据状态 UNREGISTERED_FIRSTHAND），D2+ledger 登记=开题前义务第一位 |
| 2 | 主句收窄、删全称 | 接受；capability-first 口径（续82 确认）五处同步；全称句退役 |
| 3 | 三形式落模块 | 接受；§6.2 三层接口+假设映射 |
| 4 | 载体冻结 | 接受；候选具名入围，冻结列开题前义务 |
| 5 | 五组最强基线 | 接受；§8 incumbent 分组合同（含对评审表述的四处修正） |
| 6 | 方法身份闭合 | 接受选项一：保留 TFRL+档 B bandit 做实（续82③） |
| 7 | 效率进主判据 | **拒绝**（续82②：效果优先纲领维持，效率九维记账不设限、不进主判据；能力上界口径已卸掉「替代」词汇的成本可比承诺，主张与判据自洽） |
| 8 | 范围与伦理 | 大体接受（①′梯级+既有 P13N 阶梯+§2.4 边界）；红线第四条待 owner 落笔 |

## 五、边界、证据与失效条件

本轮核验 exposure：17 篇近邻一手核验（WebFetch 摘要页+全文 PDF 抽取，三路隔离子代理；
全文暂存会话 scratchpad，未入 ledger——登记为开题前义务）。零研究模型/API 执行、零指标
运行、零数据集下载、零复现、零原型。本件不授予 Stage-2A、模型/API 调用、数据获取、指标
运行、原型、push 或 wiki 发布权限；不发 novelty verdict；不代行 owner 生效裁定（所引
三裁决=Decision-Log 续82，owner 会话裁定的正式落笔）。审计层文件提交后不得原位改写。

失效条件：①十篇 D2 逐篇源核若推翻本件任何承重刻画（训练态/信息访问/机制单元），对应
矩阵行与 §2.3 合取论证须重开；②若后续发现同时满足 API-only+training-free+双源+世界知识
rescore 的更近邻，合取命题须再收窄；③owner 若改判克隆红线，§2.4/§9 对应条款重开。
