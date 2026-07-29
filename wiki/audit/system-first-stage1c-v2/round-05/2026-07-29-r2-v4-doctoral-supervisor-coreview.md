---
title: "R2 开题报告 v4：博导视角隔离复审（round-04 三门关闭度裁定）"
date: "2026-07-29"
artifact_type: "DOCTORAL_SUPERVISOR_COREVIEW"
campaign: "system-first-stage1c-v2"
round: "round-05"
review_target: "wiki/survey/workbench/stage1c-portfolio/proposals/2026-07-29-r2-coreview-draft.md"
review_target_commit: "b06261f536812fda71be105a76a47b4673a71a44"
review_target_git_blob: "f3063b46748613a0f1e99e0fb20c4337bbbdc5bd"
review_target_worktree_sha256: "c2e127a3463aad3d28ca68484a98a23a522a8a8830ca74427f945d61d4f3e21e"
verdict: "MAJOR_REVISION_REQUIRED"
authority_effect: "WITHHOLD_ONLY_NO_OWNER_DECISION_NO_EXECUTION_GRANT"
human_signature_claimed: false
model_or_metric_execution_authorized: false
stage2a_authorized: false
novelty_verdict: "NOT_ISSUED"
---

# R2 v4 复审：三门实质通过，缺口下移到信号层与载体分辨力

## 一、评审结论

**裁决：`MAJOR_REVISION_REQUIRED`。**

先说该说的：round-04 的五项 MAJOR 中四项（MAJOR-1/-2/-3/-4）**真实关闭**，六项 MINOR **全部关闭**，
且关闭方式不是措辞腾挪。A4 拆成 A4a/A4b 后，独立性主张、K1b 与 §6 MERGE 触发确实全部改挂同一
差分；A1 的资产前提经本评审对 `merged.json` 独立复算，与 v4 逐项声明**完全一致**（480/640、
trace/* 四类共 160 条缺字段、URL 0 条、图像态证据实例可复现）；K2 的新 `t*` 定义确实只用答案轨迹
与 gold 离线比对，不再需要检索正文；§2.1 三张承重方法卡为新写内容，本评审抽验其中 20 余项数字与
结构事实，**无一失真**。这一版在"把研究对象翻译成实验"这一步上是有真实进展的。

但本轮不能给零 MAJOR。三处缺口：

1. **A4b−A4a 这条差分的含义尚未被确定。** 拆分在**动作层**干净（re-resolve 固定即固定，无自适应
   泄漏），但在**信号层**未定：§4.1 的 `V̂(SEARCH)` 含 `α1·(1 − maxAgree(H_t))`，而 `H_t` 是音频
   实体/事件假设集——被标为"通用调度"的 A4a 因此已经吃到感知不确定性信号，与 §3.2"R2 状态含实体
   假设不确定性"和 §6 MERGE 分支的措辞直接冲突；同时 A4a 的"固定 re-resolve 档"强度未定，与 K1a
   自己用"最优固定档"的标准不对称；承载音频特有性的 `audCons(H_t)` 至今只有符号没有定义。
2. **主载体在本项目自己的核上接近地板（6.56），而全部击杀阈值都是"不显著即判死"。** 该设计无法
   区分"杠杆无效"与"载体没有分辨力"，且论文原表恰好提供了反面证据（弱模型 Mimo-V2.5 的
   entity/end-to-end/gold-entity = 12.50/11.72/22.03，作者原文明说弱模型几乎得不到 search-guided
   refinement 的好处）。这条本轮首次提出，非 v4 引入的退步，但它落在 owner 即将落笔的判据上。
3. **MAJOR-5 只关闭了一半。** §2 的方法卡已就地重编码，但 §5.2 把四层评价与九维成本向量整体寄存
   在**已被本件宣告取代的 v3 blob**（`1397f876…`）里——正是 round-04 判 MAJOR-5 的同型缺陷，只是
   换了一节；而 front matter 写着"本件自足，不以任何已取代 blob 承重"，该句因此不成立。

三项的修复量都很小（三条声明式、一条判据前置、一段回填），没有一项需要新研究、新数据或执行环境。
本评审**不建议**回退 MERGE，**不**给出 novelty verdict，也不改变 R2 现有状态标记。

本文是 AI 生成的博导视角隔离复审，不冒充自然人签字，不授予模型/API 调用、数据获取、指标运行、
原型、Stage-2A、创新性结论、push 或 wiki 发布权限。owner 的续77 生效裁定继续 withheld。

## 二、审查对象、范围与本轮实际核验动作

审查对象为 front matter 所绑定的 blob，已独立 `git rev-parse` 复核：commit
`b06261f536812fda71be105a76a47b4673a71a44`、blob `f3063b46748613a0f1e99e0fb20c4337bbbdc5bd`，
工作树 sha256 `c2e127a3…f3e21e` 与 blob 内容 sha256 **逐字节一致**（无 CRLF 偏差）。

本轮不咨询送审方的写作过程。除阅读 round-03/round-04 评审与 v4 回应信、Decision-Log 续76/77/78、
模板 v2、`wiki/Research-Objective.md`、`wiki/survey/current/research-directions.md` 外，执行了以下
**本地证据抽验**（零网络、零模型/API 调用、零指标运行、零数据集下载、零原型）：

| # | 动作 | 结果 |
|---|---|---|
| 1 | 复算 `E:/…/datasets/omni-deepsearch/merged.json` 字段与分层 | 640 条；`golden_path` 480 条、缺 160 条；缺字段者精确等于 `trace/{BIO,ENV,MUSIC,SPEECH}` 各 40；`golden_path` 含 URL **0 条**；跳数 3–10（中位 5）；首条答案 `MCMXVIII`（扉页图像态）——**与 v4 §5.1/§3.4 声明逐项一致** |
| 2 | 解包 `survey-fulltext/2605.08762/*.eprint` 核 `arxiv.tex` | `tab:entity_ablation`：Gemini-3-Pro 33.76/50.00/43.44 ✓；同表 Mimo-V2.5 12.50/22.03/11.72；`tab:retry_ablation`：29.06→43.44→44.06 ✓、IMAGE 38.75→50.00 与 SPEECH 55.00→70.83 升、VIDEO 36.88→31.25 与 ENV 36.67→20.83 降 ✓；主表 Qwen3-Omni-30B-A3B (Thinking) **6.56** ✓ |
| 3 | 读 `survey-fulltext/2602.10656/*.pdf` 核 AudioRAG 卡 | 500 题 ✓；开源集 80%／在线视频 20% ✓；六裸模型基线（32.2/28.8/20.2/24.4/37.0/45.0）与 Qwen3-Omni 37.0→46.2 ✓；GPT-4o judge 三次平均 ✓；A/B/C/D = Reasoning/Audio-Processing/Knowledge/Invalid ✓（论文原文定义）；判官 prompt 逐字含 `Audio Attribute` 与 `Ground Truth` → v4"错误判官见 gold audio attribute" ✓；"Invalid Answer increases … infinite logical loops" ✓ |
| 4 | 读 `survey-fulltext/2603.02206/*.pdf` 核 VoiceAgentRAG 卡 | 76 chunk ✓、TTL 300s ✓、τ=0.40 ✓、75%（150/200）与 warm 79% ✓、110.4ms→0.35ms ✓、316× ✓、200 query/10 场景 ✓、唯一基线 Traditional RAG ✓ |
| 5 | 解包 `survey-fulltext/2401.13463/*.eprint` 核 A1′ 锚语义 | SLUE-SQA-5 每题**配一段 40 秒 Spoken Wikipedia 口语 passage 且含答案**，"gold passage" 定义即该配对关系（L232/L244）；论文同时声明假设口语 passage 的转写不可得（L243） |
| 6 | `grep` 承重 id 于 `wiki/survey/2026-07-17-sf-fulltext-ledger.jsonl` | 三篇 agentic + 三篇检索线 + 十篇 donor 共 16 个 id **全部在册** |
| 7 | `git cat-file blob 1397f876…` 取 v3 §5.2 原文 | v3 §5.2 为一整段承重合同（四层各自报告量 + 九维成本向量 + "等预算指哪一维"），**v4 未回填**（见 MAJOR-C） |

## 三、round-04 三门与 11 条关闭度

### 3.1 三门裁定（round-04 §六）

| 门 | 问题 | 判定 |
|---|---|---|
| 门 1 | 是否存在实验差分把音频特有的 re-resolve/search 分配与通用调度分开，且 §6 MERGE 触发挂在该差分上 | **CLOSED**（差分存在且唯一承载主张；但差分的**含义**未确定 → MAJOR-A） |
| 门 2 | A1 名实是否相符、覆盖缺口是否如实声明 | **CLOSED**（数据复算一致；两表对齐；缺口逐项如实） |
| 门 3 | 决策量的函数形式与时序合法性是否在 proposal 层、标定是否在 authorization 清单；K2 是否只依赖已授权落盘量 | **CLOSED**（形式、时序声明、§7 落点、K2 离线可算均成立；残余定义缺口见 MAJOR-A(c)/MINOR-c） |

### 3.2 逐条关闭度

| round-04 条目 | 判定 | 依据 |
|---|---|---|
| MAJOR-1 无臂识别音频特有机制 | **CLOSED** | §5.1 A4a/A4b 两行定义互斥；§3.1"由 A4b−A4a 差分唯一承载"；§5.4 K1b 判据对象=`A4b−A4a` 下置信界；§6 支持独立第 2 行与 MERGE 第 1 行同挂该差分且互为反面（K1b 不显著∧K1a 显著→MERGE），逻辑自洽；K1a/K1b 分层无循环 |
| MAJOR-2 A1 资产不存在 | **CLOSED** | A1 改回 `gold-entity + gold-path ceiling` 并对齐论文 oracle；A1′ 只构造于官方 gold passage 真实存在的 Spoken-SQuAD/SLUE-SQA-5（抽验 5 证实 SLUE-SQA-5 官方配对 gold passage 存在）；覆盖缺口 480/640、trace/* 25%、图像态证据三项**与本评审复算完全一致**；§4.2 与 §5.1 的 gold-entity 已对齐（MINOR-2 随之消解） |
| MAJOR-3 决策量缺席 | **CLOSED** | §4.1 给出 `V̂` 三式（待标定系数线性族）+ 时序合法性声明 + "评价层不合成总分／决策层给标量组合式"的分层更正；§7 authorization 清单已含"V̂ 估计量族选型与权重/阈值标定协议"；§5.2 合理性层已含 calibration 与误差界。逐变量时序核查：`agree/maxAgree`（已采样候选，t 前可见 ✓）、`gapCorr`（已接纳证据 ✓）、`nov`（query 历史 ✓）、`b_t`（预算余额 ✓）、`srcQual/confl`（ADMIT 属 post-retrieval 门，e 已可见 ✓）、`disp`（H_t 的离散度，可见但无定义）、`audCons`（**无定义且不在 §4.1 的合法性枚举句内**）→ 残余入 MAJOR-A(c) |
| MAJOR-4 K2 不可离线判定 | **CLOSED** | 新 `t*` 定义已剥掉"E_t 含 answer-bearing 证据"，只用**当步候选答案与 gold 的离线比对**，输入均为系统自身输出与已授权 rank/hash 轨迹，不需检索正文；§5.3 的正文落盘确为"可选请求（不默认、owner 未裁前不生效）"，§5.4 与之口径一致（"若获批则升级全量版"），**未擅自扩张续77①**；统计声明的精度问题见 MINOR-c |
| MAJOR-5 方法卡未施加于承重载体／继承已取代 blob | **PARTIALLY_CLOSED** | §2.1 三张六字段卡就地重编码且抽验准确（动作 3/4）；§2.1/§2.2 编号恢复；§1.5 引用枚举与累计 exposure、§3.4 readiness 表均件内回填；但 §5.2 把四层评价与九维成本向量整体"继承 v3 §5.2"，同型缺陷未清除 → **MAJOR-C** |
| MINOR-1 归因聚合 | **CLOSED** | §2.3 (d) 按篇分述三种异质归因并保留 possibly 限定；"context placement"降为"本项目提出的候选解释"、明写"不作为读集共识引用"、由 A3 检验；§4.2 context/use 行改标"（§2.3 候选解释的检验位）"，旧"三篇证明共同瓶颈"表述已撤 |
| MINOR-2 两表不一致 | **CLOSED** | §4.2 `audio→query` 行"gold-entity ceiling（=A1）"与 §5.1 A1 同名同义 |
| MINOR-3 探针成本 | **CLOSED**（有残余，见 MINOR-e） | §5.2 明写 `r_consistency` 与 K2 逐步候选答案探针计入 A4a/A4b 等预算并报双读数 |
| MINOR-4 A5 生成器 | **CLOSED** | §5.1 A5 行声明确定性跨题重排/置换（无 LLM），并给出改用 LLM 时的 C1 记录与"不参与作答"声明 |
| MINOR-5 模板验收项 | **CLOSED** | §1.5 深读层/登记未深读层枚举 + ledger 回溯（抽验 6 全部在册）；§3.4 readiness 表为表非散文（列填写瑕疵见 MINOR-a） |
| MINOR-6 WavRAG 表号 | **CLOSED** | §2.3 改为"按内容引用，表号未在源中确认" |

**计数：CLOSED 9 / PARTIALLY_CLOSED 1（MAJOR-5）；三门实质通过。**

## 四、新发现问题（分级）

### MAJOR-A：`A4b − A4a` 差分的含义未被确定——拆分在动作层干净，在信号层未定

这是对门 1 的补充裁定，不是对 MAJOR-1 的翻案：**臂结构已经存在且承载主张**，问题在于没有任何
规则说明两臂各自**允许使用哪些信号**、A4a 的固定档**取哪一档**。三个具体面：

**(a) `α1` 泄漏：被称为"通用调度"的 A4a 已含感知不确定性信号。** §4.1：

```text
V̂(SEARCH(q) | s_t) = α1·(1 − maxAgree(H_t)) + α2·gapCorr(E_t, ĥ_t) + α3·nov(q | A_{1..t-1})
state_t = { H_t 实体/事件假设集（含各假设自一致性计数 agree(h)）, … }
```

`H_t` 按 §3.1 即音频推出的实体/事件假设集，`1 − maxAgree(H_t)` 就是该文自己定义的
perceptual uncertainty。若 A4a 使用完整 `V̂(SEARCH)`，则 A4a = **audio-conditioned** search
scheduling，而 §5.1 把 A4a 的识别对象写成"通用 query/hop/stop 的贡献（=MERGE 情形的全部内容）"，
§3.2 又把"状态含实体假设不确定性"列为 R2 专属。三处不能同时为真。后果落在 MERGE 分支：K1b 不显著
∧ K1a 显著时，§6 判"唯一新内容=通用 query/hop/stop"并路由 R6/R8——但按 §3.2 的状态定义，此时系统
里仍有一个音频派生的调度信号，该 MERGE 标签是错的。**round-04 的教训（判死条件与成立条件必须落在
可区分的读数上）在这一分支上尚未兑现。**

**(b) A4a 的比较强度未定，差分可被弱比较臂抬高。** §5.1/§3.1 只写"re-resolve 固定策略／
re-resolve 固定"，never/always/常数档均未指定，也未要求取 dev 上最优档。K1a 自己对固定基线用的是
"**最优**固定档"（§5.4），K1b 的比较臂却无同等要求。若 A4a 的 re-resolve 常数取得偏弱，
`A4b − A4a` 会因比较臂欠优而系统性偏正——而这正是支撑"独立"的那一侧。注意 (a) 与 (b) 的偏倚方向
相反（(a) 保守、(b) 冒进），两者都未被量化，因此差分读数的解释目前不成立。

**(c) 承载音频特有性的 `audCons(H_t)` 只有符号没有定义。** `V̂(RE_RESOLVE) = β1·disp(H_t) +
β2·(1 − audCons(H_t))`，而 §6"支持独立"第 3 行与 MERGE 第 2 行都把裁定挂在 **β 分量**上。
`audCons` 与 `disp` 在全文无可实现定义：若 `audCons` 指重复解码的一致性，则 t 前可见、成本已由
§5.2 探针条款覆盖；若指"假设与波形的声学相符度"，则可能需要新增打分组件，触及续78 红线；两种读法
的合规性与时序合法性结论相反。§4.1 的合法性枚举句（"已采样候选的一致性计数、已接纳证据的
corroboration、query 历史、预算余额"）恰好**不含** `audCons`，缺口因此不是笔误。

*最小修复（三条声明式，不新增实验臂、不需执行环境）*：(i) 明写信号归属——`α1` 项仅 A4b 可用，
A4a 的 `V̂(SEARCH)` 只含 `α2/α3`；或反之，明确把 `1 − maxAgree` 重新定性为通用答案不确定性并同步
更正 §3.2 与 §6 的措辞；(ii) 明写 A4a 的固定 re-resolve 档取 dev 上最优（sweep 后取最强），使 K1b
与 K1a 的比较强度对称；(iii) 给 `audCons` 与 `disp` 各一句可实现定义，并声明其由已有冻结组件或核
自身采样计算（红线合规），同时补入 §4.1 的时序合法性枚举。

### MAJOR-B：主载体在本项目自己的核上接近地板，而全部击杀阈值都是"不显著即判死"

v4 §2.1 自己记下了这条事实却从未使用它：主载体 Omni-DeepSearch 上，**本项目的冻结核
Qwen3-Omni-30B-A3B (Thinking) 只有 6.56**（本评审在源表复核 ✓）。同一论文的实体消融给出弱模型的
完整画像：Mimo-V2.5 = entity 12.50 / end-to-end 11.72 / **给定 gold entity 也只有 22.03**，作者据此
明写弱模型几乎得不到 search-guided refinement 的好处。本项目的核比 Mimo 更弱。

后果不是"难做"，而是**判据失效**：§5.4 的 K1a/K1b/K2/K3 全部是"下置信界 ≤0 / 未降低 → 判死"。
在一个可能不具分辨力的载体上，这些 null 无法与"杠杆真的无效"区分，**false-negative kill 会把 R2
直接推进 MERGE 或整体判死**；同时 §3.1 主研究问题三目标之一"降低 evidence-induced correct→wrong"
的可测性也成问题——核在 640 题上仅约 40 余题为正确，correct→wrong 的样本基数在此量级，CI 会宽到
无意义。次载体 AudioRAG-500 上核为 37.0（不受地板效应影响），但它 §3.4 自陈未落盘、无 frozen
corpus、构造期 gold 泄漏入过滤器与判官，不能独自承担这一角色。

这条本轮首次提出；round-03/04 未及此处，v4 也未使问题变坏。但它落在 owner 即将落笔的判据上，
且不需要新研究即可修复。

*最小修复（proposal 层）*：(i) 给全部击杀阈值加 **assay-sensitivity 前置条件**——A1/A6 显示非退化
headroom 且 A2 相对 A0 有可测增益时，K 判据才具备判死效力；否则该轮读数只能记为"载体无分辨力"，
不得推出"杠杆无效"或 MERGE；(ii) §3.4 增一段载体风险与回退路径（含类别受限分析、或把 AudioRAG-500
升为共同主载体并如实带上其污染面），使 owner 在裁定时看到"这套实验可能测不动"这一风险本身。

### MAJOR-C：MAJOR-5 未完全关闭——§5.2 把评价合同寄存在已取代的 v3 blob，且 front matter 的自足性声明因此不成立

v4 §5.2 正文为：

> 有效性/合理性/可靠性/效率四层与九维成本向量**继承 v3 §5.2**。补充（MINOR-3）：……

本评审取 v3 blob `1397f876…` 核验：被"继承"的对象是一整段承重合同——四层各自必报的量
（`delta_E` 定义、paired delta、bootstrap 95% CI、McNemar、SESOI、wrong→correct/correct→wrong、
三类分桶；三类混淆矩阵、calibration 与误差界、coverage/provenance/unsupported claim；seed 方差、
worst-group/尾部、符号一致性、abstain 不得压 coverage）、九维成本向量的**逐维枚举**，以及"等预算
指逐实例 hard cap 还是平均预算、在哪一维"这一执行合同指针。这些在 v4 件内**不存在**。

这与 round-04 判 MAJOR-5 的形态完全相同（"一边宣告取代，一边把实质主体寄存在被取代的同路径
blob"），只是对象从 v2 换成 v3；而 v4 front matter 明写"本件自足，不以任何已取代 blob 承重"，该句
可被 `git show` 直接证否。round-03 清单第 8 项（四层评价、不合成总分）是 **CLOSED** 项，若 owner
以 v4 为唯一生效载体，该已关闭项无法在件内核验。

*最小修复*：把 v3 §5.2 那一段原样回填进 v4 §5.2（约十行），或删去 front matter 的自足性声明并如实
改写为"评价层合同见 v3 §5.2"——**前者才符合 `CLAUDE.md` 的 active-truth-self-contained**。

### MINOR-a：§3.4 readiness 表第四行两列填写不合列义，而该行现已承重

`Spoken-SQuAD / SLUE-SQA-5` 行的"本地"列填的是"论文级公开资产（…交叉使用）"——没有回答**是否已
落盘**（其余三行分别是"有（LOCAL_CANDIDATE_UNFROZEN…）／未落盘／未落盘"）；"评测依赖"列填的是
"文本 gold passage 官方存在"，属资产事实而非评测依赖。A1′ 现为 SQ1 诊断的唯一合规载体，其本地
就绪度必须在件内可读。

### MINOR-b：A1′ 锚的资产精度与构造模式需各一句限定

抽验 5 显示：SLUE-SQA-5 的官方 gold passage 是**一段 40 秒口语 passage**（论文并明确假设其转写不
可得），"文本 gold passage 官方存在"这一表述对 Spoken-SQuAD 成立、对 SLUE-SQA-5 需经 Spoken
Wikipedia 文本对齐才成立——考虑到 MAJOR-2 的成因正是资产表述精度，此处宜先行收紧。另需声明 A1′
在**开放检索模式**下构造（问题音频 + 从语料库检索），否则若 gold passage 与输入音频本身重合，
A1′ 注入的就不是 §1.3 第 1 类 external new information 而是第 2 类 observation re-representation，
与该文自己的信息作用词典冲突。

### MINOR-c：K2 的统计对象欠定，"抽样估计"的标签比实际更弱

按 v4 的新定义，`t*` 与 over-search 事件对**全部实例**都可离线算出（答案轨迹 + gold + rank/hash
轨迹），抽样只发生在"对 `t*` 邻域的判官复核"这一子环节。因此"如实报告为抽样估计而非全量判定"
反而低估了自己的判定力，且三件关键信息缺失：抽样框（抽的是事件、步还是实例）、**判官看到什么**
（若需检索正文，则该复核回到 MAJOR-4 的授权面，与 §5.3 的"可选请求未生效"冲突）、CI 覆盖的是抽样
误差还是判官噪声。建议改写为"主判定全量、判官复核抽样校正"，并把判官输入限定为答案轨迹与 gold。

### MINOR-d：论文数字的模型归属未标注，且 A1 严格强于论文 oracle

`33.76/43.44/50.00` 与预算消融 `29.06/43.44/44.06` 在源中**均只对 Gemini-3-Pro 成立**（论文原文
"We study the effect of search budget using Gemini-3-Pro"），而同表本项目核为 6.56；§2.1/§5.1 引用
时未标模型，易被读成本项目核的上界。另外论文 oracle 只提供**实体**（50.00），A1 定义为
`gold-entity + gold-path`（含实体链），是**更强**的 oracle——"直接对齐论文 oracle 分解…可外部
校验"应限定为"协议对齐、数值仅作外部参照，A1 自身读数不应等同 50.00"。

### MINOR-e：admission 侧的判定开销未进等预算条款

§5.2 的探针条款只覆盖 `r_consistency` 与 K2 的逐步候选答案探针（A4 臂）。但 `confl(e, E_t)` 与
`srcQual(e)` 的计算若由冻结核或 frozen judge 承担，同样是 A3 独有而 `raw top-k / relevance-only`
基线不需要的调用，等预算合同应一并覆盖，否则 A3 的对照会与 A4 犯同一个 MINOR-3 型错误。

## 五、专项判断：本轮三项 MAJOR 是否越界索要 authorization 层义务

**结论：均未越界。** 逐条自审：

- **MAJOR-A** 要的是信号归属规则、比较臂强度规则与两个符号的定义——都是设计声明，不需要 test n、
  不需要 dev 数据、不产生任何数值。（本轮**不**索要 α/β/γ/λ 的标定值、SESOI 数值或 power 结果。）
- **MAJOR-B** 要的是判据的结构性前置条件与一段载体风险声明，不是 power analysis 结果。数值仍应
  留在 authorization；本评审只要求"null 在何种条件下才可读作判死"这一逻辑先于执行确定。
- **MAJOR-C** 是纯文书回填。

同时确认本轮**不**索要、也认可继续推迟的项：K1–K4 数值、judge 保真合同细节、数据集 lock 与分层
切分、检索服务 pin、三篇检索线检查点发布状态核查、探针预算维度与 cap 形式、A5 种子协议。v4 §7 的
authorization 清单对这些的分层处理**正确**，且已按 round-04 要求纳入 V̂ 标定协议。

另附一项**认可**：§1.5 把"补抓层 19 篇清单见 git 历史 v2 §1"标为"记账指针非承重继承"是可接受的
——这些条目在 v4 全文未被引用、不承重，与 MAJOR-C 中"承重合同寄存于已取代 blob"性质不同。

## 六、裁决与复审最短路径

**裁决：`MAJOR_REVISION_REQUIRED`。** 续77② 的生效条件（关闭 round-03 §十四 全部清单项）仍差一步：
清单本身已实质关闭 9/10，但第 8 项（四层评价）的载体不在件内（MAJOR-C），且独立性判据的读数含义
（MAJOR-A）与判据的可信性前提（MAJOR-B）未定。

v5 复审只需判定三件事：

1. A4a/A4b 的**允许信号集**与 A4a 的固定档强度是否已写定，`audCons`/`disp` 是否已可实现定义并进入
   时序合法性枚举；§3.2/§6 的措辞是否与所选口径一致（MAJOR-A）。
2. 击杀阈值是否已带 assay-sensitivity 前置，§3.4 是否已如实陈述主载体在本项目核上的地板风险与
   回退路径（MAJOR-B）。
3. §5.2 是否已件内回填四层评价与九维成本向量，front matter 的自足性声明是否与件内事实一致
   （MAJOR-C）。

五项 MINOR 随 v5 一并核验，不单独构成复审门。本评审再次确认：**不建议**回退 MERGE——v4 的证据底座
（三张承重方法卡经源抽验准确、载体资产复算一致）与识别骨架已达开题报告标准，剩余缺口全部是把已
写清楚的设计再收紧一格。

## 七、目的链、Provenance 与失效条件

**结论：** R2 v4 关闭了 round-04 的四项 MAJOR 与全部六项 MINOR，但 MAJOR-5 残留一处同型缺陷，
另有两处新缺口落在差分含义与载体分辨力上。续77 有条件 GO 的生效条件尚未成就，owner 的生效裁定
继续 withheld。本文不改变 R2 的既有状态标记，不授予任何执行权限。

**推理摘要：** v4 把 round-04 的四项 MAJOR 按处方逐项做实，且做实的方式经得起源核验——`merged.json`
的复算与 v4 的每一句覆盖声明一致，三张新方法卡的二十余项数字在论文源中逐条命中。但把处方执行到位
之后，识别问题下移了一层：臂拆开了，可两臂各自允许看什么信号没有规定，而 `V̂(SEARCH)` 的第一项正是
音频感知不确定性；差分成立了，可承载音频特有性的 `audCons` 还只是符号；判据可执行了，可判据运行的
载体在本项目自己的核上只有 6.56，且论文原表已示范弱模型对这类改进几乎无响应。因此不能从"处方已
执行"推出"独立性判据已可被实验读数支持"。

**目的链：** 为了让 owner 在"R2 独立 / 合并入 R6-R8"之间落笔时，其裁定能被后续实验证实或证否；
所以独立性主张不仅要挂在一个可被读数区分的差分上（round-04 已达成），还要求该差分的**两侧内容**与
**读数的可信前提**同样被写定；所以本轮把裁定条件精确定位到信号归属、比较强度与载体分辨力，而不再
重复审查文献充分性与臂结构存在性。

**Provenance：** 本文只审查 front matter 所绑定的 Git blob `f3063b46…`（commit `b06261f5…`，工作树
sha256 `c2e127a3…` 与 blob 一致，已独立复核）。判断依据为：round-03 评审
`…/round-03/2026-07-29-r2-doctoral-supervisor-coreview.md`；round-04 评审与 v4 回应信
`…/round-04/`（两件）；owner 裁决 `wiki/Decision-Log.md` 续76/续77/续78；模板
`…/proposals/2026-07-29-direction-coreview-template.md`；正典 `wiki/Research-Objective.md` 与
`wiki/survey/current/research-directions.md`；以及第二节表列的七项本地证据抽验（`merged.json` 640
条复算、`2605.08762` LaTeX 源、`2602.10656` 与 `2603.02206` PDF、`2401.13463` LaTeX 源、fulltext
ledger、v3 blob `1397f876…`）。本轮 exposure：零网络检索、零模型/API 调用、零指标运行、零数据集
下载、零原型；新增动作仅为本地已落盘资产的读取、解包与比对。

**失效条件：** 若 v5 或其回应关闭本文第四节的三项 MAJOR，并由新的 review transaction 判定差分的
信号归属已写定、判死线已具备灵敏度前提、评价合同已件内自足，则本 withholding 仅作为历史审计事实
保留。若 owner 直接裁定改变研究对象定义、载体或红线边界（对象定义权归 owner），本文中依赖旧口径的
条目按新裁决作废，但**已核验的证据事实**（`merged.json` 的字段与分层复算、`2605.08762` 的 oracle
与预算消融归属及核模型 6.56、三张方法卡的源核对结果、SLUE-SQA-5 gold passage 的口语形态、v3 §5.2
的内容与 v4 的缺失）独立于处置结论继续有效。本文为审计层记录，不得原位改写。
