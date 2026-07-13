---
title: "致 Reviewer：Stage-1A 中途预检请求 —— survey 覆盖设计预检（正式请求）+ 记录修复闭环通报（仅通报）"
date: 2026-07-13
request_type: "DESIGN_PRECHECK + RECORD_CLOSURE_NOTICE（非签字申请、非收官审阅）"
current_position: "Stage-1A（问题界定；owner 2026-07-13 的 Stage-1A/B/C 细分，定义见 CLAUDE.md 术语表）"
snapshot: "umbrella HEAD 0afad68 / W1 HEAD a532da0（哈希正典=git blob 字节，核验命令见 §1.4）"
requested: "§2 的 Q1–Q6（预计 reviewer 用时 ~15–20 分钟）"
explicitly_not_requested: "scoped sign-off 重签（其硬条件尚有未闭项）；Stage-1 收官裁决；任何科学有效性判断——当前不存在任何确证宣称"
main_review_planned: "Stage-1C 决策包就绪时（survey wiki 级 + 原型矩阵 + 诚信核查包 C1/C4 普查 + I1–I4 kill 判定 + owner 候选倾向）一次覆盖 Gate S1-A~E 与 Stage-2 gate"
author: "协调者（owner 授权发出）"
---

# Stage-1A 中途预检请求

## 0. 一段话说明

按您重校准审查的阶段纪律，我们不在收官包就绪前请求任何裁决。本文件只做两件事：
**（A）§1 通报**您各轮审查中记录类发现的修复闭环与自检收敛轨迹——仅供知情与可选抽查，
**不请求签字**；**（B）§2 正式请求**一次 15–20 分钟的 **survey 覆盖设计预检**（Q1–Q6）——
这是我们即将投入最大的一笔 Stage-1A 工作（5–8 篇最近邻全文核验 + 第二轮饱和检索）的**事前**
设计检查：若家族清单有漏项，现在指出的成本远低于事后返工。

## 1. 触点 A：记录修复闭环通报（仅通报，不请求裁决）

### 1.1 您的记录类发现 → 处置对照

| 发现 | 处置（全部 append-only，原文可见） |
|---|---|
| R6-M1（v6 responds-to 哈希混淆） | 更正件 §2 给出正确三元组；并建立**哈希正典约定**（=git blob 字节；此前各方流通的 `cd987ff0…` 系 CRLF 工作树变体，正典值 = `6c6adba2…` @`c7528fe`，换算关系已逐字节验证并落档） |
| R6-M2（证据快照/工件快照混写） | 拆为 `evidence_snapshot` / `artifact_snapshot` 双栏 |
| R6-M3 / S1-M4（13 项 YAML 塌缩） | 以列表 schema 重发 13/13、入库前 PyYAML 实测验证；**首版重发自身曾丢 2 处 `PLAUSIBLE_STAGE_` 限定，自检环抓出并恢复（如实披露）** |
| S1-M1（stage 标签超前） | `84c6cf6` 草稿更正为 PRE_STAGE2_BLUEPRINT（术语表已登记）；当前位置 Stage-1A |
| S1-M2（ρ 构念漂移） | 术语表四量并列：rho_greedy / rho_pool / delta_mbr / regret + U 记号注册（与 Project-Thesis R 记法同构说明） |
| S1-M3/M5/M6、诚信核查 C1/C4 | 落位为 Stage-1B 放行前置与 Stage-1C 决策包交付物（未完成，如实 OPEN） |

### 1.2 自检环收敛轨迹（owner 指令："工作流系统性自检后才准宣布完成"）

三轮多镜头敌意自检 + 逐发现独立对抗核证：**21 确认 → 7 → 1 → 0**（5 项误报被核证驳回）。
两项**自查自纠**的重项如实报告：①（FUNDAMENTAL 级）曾在三份正典文档引用 claim-ledger 判
INVALID、明令禁引的 +0.517（T7 答案泄漏数字）作供给条件性佐证——已三处撤引并勘误（干净 T8
复跑为 −0.066 null，且其口径是单输出注入收益、非头空测量；**目前没有合法的自家 H(c) 供给分层
测量**，该测量属未来 Stage-1B P0 原型）；②（MAJOR）撤引文本首版又把 benefit 误标 headroom——
已改并在术语表钉死两量之别。这两项正属于您 §5.2 监控的选择性引用风险类；自检环在对外发布前
拦截了它们。

### 1.3 相关提交链

`7de1c5f`（T+0 包）→ `757465c`（一轮修复）→ `f102aca`（正典哈希 manifest wrapper）→
`262ace0`（二轮修复）→ `0afad68`（三轮收敛修复）；术语表 `f57cd81`。

### 1.4 可选抽查配方（自足，任何 clean clone 可复现）

release manifest 七工件哈希：伞仓五项 `git show 757465c:<path> | sha256sum`；W1 两项在
`projects/speech-mllm-training-free-rl/` 内 `git show a532da0:scripts/knowledge/corpus_lock.py |
sha256sum`（另一项 `scripts/baselines/deterministic_draw.py`）。对照
`docs/integrity/release_manifest.json` 与落档 `docs/checks/manifest-blob-verification-2026-07-13.txt`。

## 2. 触点 B：survey 覆盖设计预检（正式请求，Q1–Q6）

### 2.1 设计概要（被预检对象）

**研究方向（Stage-1A 工作伞，未收官）**：选择器兑现率方向——冻结 speech/omni 核心的 K 样本池
中，label-free 选择器能兑现多少 oracle headroom（ρ(c)，供给条件量）。survey 按您 §7 的覆盖门
执行，另加两条自家倾向：**效果地图优先**（逐篇抽"报告的头空/其方法吃掉几成"）与**供给条件性
组织轴**（逐篇记录候选池在什么供给下生成：裸采样 / beam-lattice / +LM / +检索）。

**八个方法家族**（T1 kill 供体 → T4 类比，逐篇 20 字段表）：①经典 MBR/expected-WER/ROVER/
confusion network；②reference-free ASR QE（NoRefER 谱系）；③acoustic-grounded 假设评估
（READ 谱系）；④confidence estimation + LTR rescoring；⑤LLM N-best rescoring/revision
（HypR/ProGRes/HyPoradise 谱系）；⑥multi-verifier/uncertainty/abstention/pessimistic selection；
⑦BoN scaling/reward overoptimization/test-time compute（含语音应用）；⑧文本/视觉 verifier-guided
selection（仅机制类比，不作语音新颖性证据）。

**数据/评测锚**：冻结 28 集（ASR: librispeech；口语 QA: heysquad/spoken-squad；SLU/intent 15 集；
audio understanding 5 集；ST/SER 等）+ 候选（aishell-1/thchs-30/cn-celeb1,2/squtr-FiQA 57,638
docs 语料锁定）；评测机械 = 冻结 Qwen3-Omni-30B（llama.cpp）K 池采样、WER/EM 可验证奖励、
已实现 oracle/MBR/random 对照、说话人组感知抽样、paired-bootstrap CI。每篇文献强制映射
"能在我们哪个数据集上作 equal-K kill test"。

**四个候选身份（Stage-1C 才选，现为候选空间）**：I1 一般 label-free N-best selector；I2 音频
接地的冻结 omni selector；I3 受约束/可弃权、显式检测 Goodhart 拐点的跨任务 selector；
I4 (供给 c, 选择器) 二元组——供给分层的 H(c) 兑现率研究（行使您 S1-F2 的"第四个"选项）。

### 2.2 第一轮 scout 结果摘要（供预检参考；全部 scout 级，进 wiki 前经协调者逐篇全文核验）

8/8 家族、57 条目（~44 篇去重）、引用可解析性核查零虚构（2 处场地标注待正）。初步 kill 信号：
**I1 机制层近死**（MBR 1997–2025 占有；Jinnai 2510.19471 在 Whisper 系上 equal-N 胜 beam——
协调者已摘要级核验方向属实，其 oracle 兑现率具体数字待全文钉死）；**I2 概念层被双重占位**
（READ 2606.04680：training-free+reference-free、TTS 条件似然打分、up to 20% rel WERR 噪声下
更强——已摘要级核验；MILS 2501.18096：冻结打分器 select-refine 跑通音频、代码公开——已核验）；
**I3 对象 OPEN 但守卫机制不新**；**I4 最干净空位——~44 篇中零篇把供给类型作设计轴分层测
H(c)，+检索臂零覆盖**。另发现一条语料缺口：会话/电话/会议/真实噪声 ASR 语料（WSJ/AMI/SWBD/
CHiME/TED-LIUM 类）不在盘上。

**第二轮饱和检索优先序（拟）**：① audio-native RAG / retrieval-augmented speech（+检索供给臂，
正对 I4）；② speech/omni 模型自评估/自奖励/原生似然置信（I2 的剩余格）；③ ASR/语音的 selective
prediction/abstention/校准（I3）；④ verifier–generator 去相关/同族评估混淆（I2 测量效度）；
⑤ 跨任务统一语音奖励与 test-time selection；⑥ 冻结模型能力/知识激发与上下文扩展头空分解（I4
构念效度）。

### 2.3 待评审点（Q1–Q6，恳请逐条简答）

```yaml
precheck_questions:
  - id: Q1
    topic: family_completeness
    question: 对"冻结 speech/omni K 池上的 label-free 选择"这一问题域，上述八家族是否漏了
      必查的直系祖先家族？（例：跨系统 system combination/ROVER-类、流式/lattice 在线重打分、
      对话上下文重打分，是否应独立成族而非并入现有族？）
  - id: Q2
    topic: kill_test_assignment
    question: kill test 指派是否正确——I1 的主击杀器=equal-K MBR；I2=READ 类外挂 TTS 打分
      （同族评估混淆需另行 delta_corr 防护）；I3=文本域 hedging/pessimism 基线移植？有无更强的
      击杀器被漏配？
  - id: Q3
    topic: I4_whitespace_validity
    question: 您是否知道任何先例把能力供给类型（裸核心 vs +上下文 vs +检索）作为设计轴分层、
      并测量供给条件头空 H(c) 或其兑现率？若有请给出处——我们希望 I4 的空位判定现在就接受
      最强反例检验。
  - id: Q4
    topic: round2_priority
    question: 第二轮饱和检索的六项优先序（§2.2）是否需要调整——有无应提级/降级/新增的关键词族？
  - id: Q5
    topic: corpus_gap_impact
    question: 盘上缺会话/电话/会议类 ASR 语料这一事实，是否在现在这个时点就实质性限定某个候选
      身份的主张范围（从而应改变候选清单或其 kill 条件），还是可以合法推迟到 Stage-1C 如实
      标注主张边界？
  - id: Q6
    topic: record_closure_spot_check
    question: （可选）§1 的记录修复处置对照中，是否有任何一项您认为未对准您的原发现？
      （不请求签字，仅请求异议——无异议可不答。）
not_requested:
  - scoped_signoff_reapplication   # 其硬条件（group-disjoint 代码、上游二次拉取、配置轨迹）仍 OPEN，条件闭合后另行申请
  - stage1_closure_verdict         # 收官包（survey wiki 级 + 原型 + C1/C4 普查 + 决策 memo）就绪后作为主审阅提交
  - any_scientific_validity_judgement
```

## 3. 时间线

- **现在**：本预检（Q1–Q6）；您的回答将直接约束最近邻全文核验与第二轮检索的范围。
- **Stage-1B**（须 owner 显式放行，前置=survey 覆盖门+诚信核查 C1–C5 齐备）：供给分层原型矩阵
  （P0 headroom 地图起步）。
- **Stage-1C**：完整决策包提交您作**主审阅**（Gate S1-A~E + 若 owner 选 proceed 则对 fresh
  Stage-2 proposal 签 Stage-2 gate——一次审阅覆盖两个门）。
- **平行线程**：scoped sign-off 重签按其硬条件清单独立推进，不与阶段绑定。
