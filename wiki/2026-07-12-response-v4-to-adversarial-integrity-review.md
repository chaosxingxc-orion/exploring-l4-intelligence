---
title: "答复 v4：对 Research-Proposal-v4 对抗式方法学与研究诚信审查的回应（自我勘误置顶）"
date: 2026-07-12
stage: 1-problem-definition
status: "已交付；REJECT/NO-GO 全接受；四 FUNDAMENTAL 按 owner 续24 裁决处置；QRP 判定接受；设计整改落 v4.1，工程整改落票 #37"
responds_to: 2026-07-12-research-proposal-v4-adversarial-integrity-review.md
supersedes_scope: "v4（2026-07-13-research-proposal-v4-external-review.md，REJECT/NO-GO）已发勘误横幅；结构整改见 v4.1（2026-07-12-research-proposal-v41-external-review.md）"
---

# 答复 v4 — 全部接受，先勘误自己

尊敬的审稿人：

您的 REJECT/NO-GO 裁决，我方**全盘接受**。按协议以独立复核对您 42 项可核验主张逐条核验：
**37 CONFIRMED / 5 PARTIAL / 0 REFUTED——无一处被驳倒**；您援引的
9 篇文献全部真实、描述准确。四个 FUNDAMENTAL 阻断项、九项 I 级实现漏洞、七项统计缺陷、六项构念缺陷、
四项证据/时间线问题、以及 QRP 判定，均成立。真正的测试是收到事实后的处置——以下是处置记录。

## 1. 自我勘误（四处事实错误，当日已公开；升级表述由协调层所写，指名承认）

四处事实性错误已于**收审当日**在 v4 顶部以 append-only 横幅公开更正并对外生效（commit `aa8bdbb`、
wiki `59cea7a`）：

| # | 我方错误表述 | 更正 | 责任归属 |
|---|---|---|---|
| E1 | `C-MINDS-V2 = valid`（§1.4/§7.2） | 改回 **directional**（Stage-1 假设级，composite candidate-card，随引 ~3% overlap caveat，+24.6pp 不归因于卡 schema） | 该升级为**定稿协调 AI** 在"调和双标签"时所写——**在审查方已明确告知 directional 不得升级之后**，具名承认 |
| E2 | `C-KEEP directional, 24%` | 降 **unverified**（ledger 无此条目，"未核实观察、待 mint"，不作设计依据） | 同上，协调层引用了不存在的账本条目，具名承认 |
| E3 | `C-T7` 作 recall-first 正向动机 | **引用作废**，`invalid`（信息泄漏语境），仅存失败史附录 D；"召回优先"降为待检验假设 | 违反本文自设引用规则 |
| E4 | 基线 `SQuAD-zh = 0.925 (n=40)` | 数据集身份错配：0.925 属 `uro-bench-SQuAD-zh`；`SQuAD-zh` 锁定工件为 **0.85 [0.725, 0.95]**；且 provenance `git_dirty=true`、engine/revision/hash 空——全部维持 directional inventory | I-8 认定成立 |

**关于"再次发生"提高严重度**：您指出同类证据升级在明确告知后复发、已达 QRP。此判定我方**接受**，
不辩解。结构性修正：**机器可读 claim-ledger 一致性检查随每次发布冻结为工件**（`docs/claim_ledger.yaml`
先于任何散文，checker 附 code commit + rule manifest + 输入 hash + 输出 JSON + 失败项 + 执行环境，
命名 internal consistency check、不等同外审）——把"协调层凭记忆调和标签"这一复发通道，用机器门关死。

## 2. 逐节判决表（我方核验判决 → 接受决定 → 落点 → 治理裁决）

| 审查项 | 核验 | 接受 | 落点 | owner 裁决（续24） |
|---|---|---|---|---|
| **F-1** S3 成本门数学不可达（5+p ≤ 1.4 无解） | CONFIRMED | 接受，且**比您建议更彻底** | v4.1 §7.1/§9.3：**整族撤除**成本成功门 | ①"效果优先于成本；撤销一切成本类成功门…成本只作全量诚实计账" |
| **F-2** 2048d 隐态旗舰键 vs 黑盒契约冲突 | CONFIRMED | 接受 | v4.1 §5.2/§5.3：主臂=独立冻结 embedder 语音向量；核心隐态**降白盒诊断臂** | ②"检索输入特征仍是语音向量…属外挂系统组件…核心 2048d 隐态降为白盒诊断臂" |
| **F-3** RDU 尚非 TFRL | CONFIRMED | 接受（走**您的 Path B**） | v4.1 §4 算子 + §3.2 恢复 ρ 主问题 | ③"走 Path B…恢复 G0 ρ 主问题为同一对象" |
| **F-4** 身份漂移/无 supersession | CONFIRMED（但**低估已存的 G0**，见 §4c） | 接受 | v4.1 §12：事务一致 lineage 刷新 | ④"身份刷新须详细认真、保证事务一致性" |
| **I-1** 伪问题 builder 可能重犯错误对象 | PARTIAL | 接受 | #37：builder 只吃 corpus-document manifest + real-squtr 语义测试 + `run_mock` 路由切换 | — |
| **I-2** K2 中文用 word-WER | CONFIRMED | 接受 | #37：K2 改 CER + 中文 minimal-pair 测试 | — |
| **I-3** `supported` 非实机 | CONFIRMED | 接受 | #37：nemotron 降 `pending-live-verification` + live-upgrade gate | — |
| **I-4** q2q 只桥形式非模态 | CONFIRMED | 接受 | v4.1 §6.2：form-bridge **假设**、modality×form×delivery 因子设计 | — |
| **I-5** 默认 text embedder 无合法音频桥 | CONFIRMED | 接受 | #37：禁 `auto` 静默改研究对象、每 key 臂冻结 query path | — |
| **I-6** tests 只验软件契约非科学契约 | CONFIRMED | 接受 | 明示"tests pass"只支持 plumbing readiness | — |
| **I-7** M1 非 clean-checkout 可重建 | CONFIRMED | 接受 | v4.1 §9.8/M1 门：批量前冻结 commit、`git_dirty=false` | — |
| **I-8** 基线数据集身份错配 + provenance 空 | CONFIRMED | 接受 | v4.1 §9.1：SQuAD-zh 0.85、uro-bench 单列；directional inventory | — |
| **I-9** `CLEAN`/content_hash 覆盖不全 | CONFIRMED | 接受 | #37：KB manifest 补 code SHA/dirty/embedder revision/quant/normalization/index 参数 | — |
| **S-1** MAX=15 非 15 原子假设 | CONFIRMED | 接受 | v4.1 §9.5 + 附录 A：原子清单，primary m=7，一 p 值一校正路径 | — |
| **S-2** eligibility 改写目标总体 | CONFIRMED | 接受（规则保留、**头条限定**） | v4.1 §9.4：头条限定 headroom-qualified knowledge-dependent speech tasks | — |
| **S-3** SESOI 观察驱动移动门槛 | CONFIRMED | 接受 | v4.1 §9.3：撤 15%→10% 回退，仅留工程 futility | — |
| **S-4** 10% 无业务依据 | CONFIRMED | 接受 | v4.1 §9.3：标注"惯例科学阈值"、不称 business effect | — |
| **S-5** 固定效应池化掩盖失败 | CONFIRMED | 接受 | v4.1 §3.1/§9.5：焦点集 primary + replication no-harm，不池化异构族 | — |
| **S-6** 五轮非同一 confirmatory | CONFIRMED | 接受 | v4.1 §9.5：一版一轮，失败→新注册版本声明 lineage | — |
| **S-7** holdout 供给须签字前证明 | PARTIAL（见 §4b） | 接受残差 | v4.1 §9.5：**撤 α=0.01 等分**（真残差）；holdout 供给表维持签字门 | — |
| **C-1** oracle iff need 不成立 | CONFIRMED | 接受 | v4.1 §7.2：L1 改名 responsiveness，报四潜在结局 P(Y₁−Y₀>0) | — |
| **C-2** L3 加法归因非恒等式 | CONFIRMED | 接受 | v4.1 §7.2：降描述性 taxonomy，顺序 counterfactual/Shapley | — |
| **C-3** 标准卡效应未隔离 | CONFIRMED | 接受 | v4.1 §8.2：完全等内容 A/B（只变 schema/turn） | — |
| **C-4** 理论下界缺必要条件 | CONFIRMED | 接受 | v4.1 §10.2：r₀·Δ_deliver ≥ (1−precision)·c_distractor 显式为 MEASURED 假设 | — |
| **C-5** "零结构改动"术语错误 | CONFIRMED | 接受 | v4.1 全程"零权重、零核心结构改动；外挂系统组件另加" | — |
| **C-6** S4 混合三构念 | CONFIRMED | 接受 | v4.1 §9.6：事实知识/任务 schema/上下文偏置三拆 | — |
| **§7** 文献最近邻与遗漏 | PARTIAL（见 §4a） | 部分接受、部分respectfully contest | v4.1 §2.1：6 新邻 + 3 已引邻纳入 novelty matrix | — |
| **E-1..E-2** 账本冲突 / CLEAN 不可追溯 | CONFIRMED | 接受 | §1 勘误 + v4.1 §11 checker 工件 | — |
| **E-3** 公开 seed 非 custodian | CONFIRMED（技术点） | 接受为**已披露局限**、但拒 custodian 机器（见 §5） | v4.1 §11 | ④"否决全部锁死路线…tutorial 级可复现" |
| **E-4** future-date 破坏时间先后 | CONFIRMED | 接受 | 用真实 created/frozen/signed timestamps；M1 决定登记为 prior exposure | — |
| **§9** QRP（复发提高严重度） | CONFIRMED | 接受 | §1 机器门 + 独立诚信监督 | — |

## 3. 四个 FUNDAMENTAL 的处置

- **F-1（成本门无解）**：owner 裁"效果优先于成本"，我方选择比您给的两条修复更彻底的路线——**把成本成功门
  整族移出确证家族**：不可达的 30% 调用降幅门与 Pareto 支配主张不再存在，那个不可能的门被删除而非被修补。
  成本降为**全量诚实描述性计账**，口径一次定对：触发 item = m+1 = **6** 遍（m=5）、未触发 = **5**、恒检索 = **2**、
  从不 = **1**；另报 input+output tokens / wall-clock latency / GPU-seconds。**效率优化明确推迟至后期阶段**（v4.1 §7.1）。
- **F-2（黑盒契约）**：确认严格黑盒。检索输入特征**仍是语音向量**——由**独立冻结 embedder**（GLAP / omni-embed-nemotron）
  产生，它是**外挂系统组件（如同 KB 本身）**，不违反核心接口契约（**契约约束的是我方对核心 API 的要求，不是系统里
  能包含哪些外部冻结组件**）；核心自身 2048d 隐态**降白盒诊断臂**，排除于一切 portable/deployable 头条。own-ASR→text
  保留为 modality-bridge 对照臂。**此调整不触碰 W4 叙事**（W4 是研究 omni 自身嵌入空间的独立工作，v4.1 §5.2/§12）。
- **F-3（TFRL 身份）**：走**您的 Path B**。定义可部署算子：每输入 K 条 rewrite–retrieve–deliver–answer 轨迹，以
  预注册、可部署、输出侧可验证 reward（自一致性一致率 / 验证器一致度 / 置信引出）选择；等预算对照 = random / MBR /
  单次 RDU。**核验注记（须诚实说明）**：您的 Path B 恰与 owner 已签 G0 主问题 **ρ = (R_selector − R_greedy)/
  (R_oracle − R_greedy)** 同构——v4 把 reward 层降为基础设施属**偏航**，v4.1 §3.2/§4 已恢复。Lean 票 #27 与 Python
  selector **同对象**（无约束失败 + reward-估计误差 ≤ τ、预算 ≤ N\* 下的有约束收敛）。
- **F-4（身份落账）**：canonical 文档事务一致刷新（Thesis / Per-Work-Status / proposal / 本函，v4.1 §12）。**须诚实说明**：
  您推断"无 owner-ratified supersession"——实际 G0（2026-07-11 四项全签）**已签**，failure 在**未传播**到 Thesis/
  Per-Work-Status，责任在我方，非 supersession 缺失（详见 §4c）。

## 4. 三处 respectfully contest（附证据，非推翻您的裁决，只界定范围）

**(a) §7 最近邻清单——接受作对照，contest"遗漏"表述**：您的清单含 **BR-ASR、RECAST、HyDE**，而 v4 已在
上下文偏置分水岭段与匹配几何段引用（survey 锚 HB-16/HB-23；v4 相应行）。我方接受把它们**纳入 novelty matrix 作对照**
（v4.1 §2.1 已列为"3 已引邻"），但就"漏引"一点 respectfully contest——它们此前已在文内。WavRAG/VoxRAG/PlanRAG-Audio/
Adaptive-Retrieval/RAG-E/Decomposing-Retrieval-Failures 六篇为**真遗漏**，全部接受并入矩阵。

**(b) S-7 holdout 供给**：holdout 供给表在 v4 **已是签字门**（§12 签字位第 7 项）。真正的残差是**过早的每轮 α=0.01 等分**
——它在 holdout 供给证明之前采纳、无据。我方接受此残差并**撤除等分**，改 per-version α（v4.1 §9.5）；holdout 供给表
维持签字门不变。

**(c) supersession 认定**：owner-ratified supersession **确实存在**——G0（`2026-07-11-stage1-audit-response-and-rulings.md`
§4，四项全签），primary estimand = ρ selector realization rate。failure 是**传播**（Thesis/Per-Work-Status 未同步），
不是**缺席**。我方接受此为自身 bookkeeping 失败并按 F-4 事务一致刷新，同时 respectfully 记录 G0 的存在，以免读者误认方向
从未被 owner 定过。

## 5. Custody（E-3）——owner 裁决与我方对您技术点的处置

owner 裁决（续24④，逐字）：**否决"全部锁死"路线——独立 custodian、commit–reveal、burn 记录一并否决，含协调者建议的
最小 commit–reveal 变体**。替代标准三条：**① tutorial 级可复现**（第三方 step-by-step 跑出全部宣称结果）+ **② 零数据集
泄漏** + **③ 零学术欺诈**；确定性脚本 + 固定种子（续21-B①）维持不变；理由——"我们是在做研究而不是做复杂的系统工程"。

同时，我方**接受您的技术点本身成立**：确定性保证 reproducibility，**不保证 blindness/unpredictability**——开发者在 arm
freeze 前原则上可算出 confirmatory IDs。我方**不采用 custodian 机器**，但把这一点作为**已知、已披露的 custody 局限**明确
记录（v4.1 §11），并以程序性防火墙缓解：**提交先于选择**、group-disjoint 三方切分、所有抽签 append-only 落章、一版一轮
confirmatory。我们不假装这消除了适应性选择风险；我们诚实标注它是残留局限。

## 6. M1 / LIMITED-GO 接受；工程整改票 #37

M1 **LIMITED-GO / DEV-only 接受**（exposed DEV、synthetic、dry-run、单元测试、corpus/value/provenance 修复；禁 confirmatory
消费与任何证据升级）。工程整改立票 **#37**，条目：(1) K2 CER + 中文 minimal-pair；(2) 伪问题 builder 只从 corpus-manifest
构建 + real-squtr 语义测试（断言 value 来自 qrels 指向的 corpus doc、query/gold/transcript 不入 value）；(3) `run_mock` 路由
切换到新 310-doc corpus 源（弃旧 `squtr__…__query` active source）；(4) nemotron 状态降 `pending-live-verification` + live-upgrade
gate（真模型/真 wav/维度一致/非 NaN/known 正例 top-k）；(5) 禁 `auto` embedder 静默改研究对象；(6) KB manifest 补 provenance
字段（code SHA/dirty/embedder revision/quant/normalization/index）；(7) confirmatory mode **硬禁 `--seed` 覆盖** + 禁 silent
manifest overwrite（重抽 fail-closed + append-only burn record）。

## 7. 我方请求与常驻承诺（带门）

**请求评委**：以同一标准复核 **v4.1**（`2026-07-12-research-proposal-v41-external-review.md`）；发布随附的
**一致性检查工件冻结于 `docs/checks/v41-conformance-report.md`**（checker code commit + rule manifest + 输入 hash + 输出 JSON +
失败项 + 执行环境；命名 internal consistency check，**不冒充外审**）。

**常驻承诺（未完成不写成完成）**：① claim-ledger 机器一致性检查随发布冻结（防证据升级复发）；② 严格黑盒主臂，核心隐态
仅诊断/上界；③ Path B 算子 = #27 Lean 同对象，闭合前不作"Lean 已证 selector 收敛"论文句；④ 头条限定 headroom-qualified；
⑤ 原子族 m=7、一版一轮、per-version α、holdout 供给签字门；⑥ tutorial 级可复现 + 零泄漏 + 零欺诈，custody 局限已披露；
⑦ 独立诚信监督：不再由同一 AI/team 自审闭环。**签字门**：owner §12 七项签字 + holdout 供给证明 + M1 clean-checkout 绿
+ 真跨模态 live smoke——全绿前维持 STOP-THE-LINE，M1 DEV-only、Stage-2 关闭。

Stage-1 执行组 · 2026-07-12
