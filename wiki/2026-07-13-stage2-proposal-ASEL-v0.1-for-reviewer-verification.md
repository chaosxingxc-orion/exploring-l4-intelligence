---
title: "Fresh Stage-2 Proposal（A-SEL）v0.1 · DRAFT — 呈 reviewer 结构验证"
program_id: W1-ASEL-S2-001        # 全新 program ID；不复用 v4.2（RDU 前端）program 的任何 family/seed/确证标签
date: 2026-07-13
stage: 2-solution-validation (entry draft)
status: DRAFT-v0.1 / NOT-FROZEN / PENDING-REVIEWER-STRUCTURE-VERIFICATION
template_instance_of: "Research-Proposal-Template.md（逐节映射，见 §0.2）"
authorizes: "本稿不授权任何 data-sensitive 工作；M2 维持冻结直至 §11 解冻条件全闭合 + reviewer 签 Stage-2 gate"
predecessor: "v4.2（2026-07-12-research-proposal-v42-external-review.md）归档为 Stage-1 问题定义交付物（续32③）——本稿非其原地升级"
responds_to_review: "V42-REMEDIATION-SIGNOFF-ADR-2026-07-13 §9 Proposal A/B + §10 P0-B items 5–7"
owner_rulings: "Decision-Log 续32：A-SEL 唯一 headline；public-deterministic + 如实等级帽；修订续29"
evidence_grade_cap: "development / controlled-benchmark evidence（M-S1 路线①，预先接受；不作强 confirmatory 宣称）"
authored_by: "协调者本人（不委托），2026-07-13"
---

# Fresh Stage-2 Proposal（A-SEL）v0.1 — 待验证稿

## 0. 给 reviewer 的阅读与验证说明

### 0.1 本稿的性质与请求

这是签署审查 §10 P0-B item 6 要求的 **fresh Stage-2 proposal** 的第一稿。它**不是**重签申请，
**不**授权任何接触数据的选择性工作。我们请求 reviewer 做的是**结构验证**（本轮）：

1. §S1 的 Stage-1 科学身份收官是否满足审查 Proposal A 的全部字段（唯一 headline、最近邻表、
   load-bearing comparison、falsifier、资源上限、进入 Stage-2 的决定）；
2. 每一个待定数值是否都被显式挂在冻结门（§10 FG 表）而非用占位数字冒充已定——**本稿刻意
   不含任何"看起来已定其实没依据"的数**；
3. 门序是否正确：所有设计身份自由度在本稿 v1.0 冻结时落定（BEFORE_STAGE2_UNFREEZE），
   M2 只做预列 branch 内的标定，M3 只具体化预列 branch，不新增 primary claim；
4. 信息边界契约（§6.1）与隔离契约（§4.2）是否堵住审查 F-S4/F-S5 与本项目自身的
   "对象错误/信息越界假增益"史。

结构验证通过 → 我们完成 P0-B 工程项与 FG 冻结件 → 提交 v1.0 冻结稿请求 Stage-2 gate 签字。

### 0.2 模板映射（Research-Proposal-Template 实例合规）

| 模板节 | 本稿节 |
|---|---|
| §0 front-matter | frontmatter + §0 |
| §1 idea & falsifiable hypothesis | §S1 + §1 |
| §2 success/kill/pivot | §2 |
| §3 survey & positioning | §3 |
| §4 reproduced results (baseline+pilot) | §4（M2 标定协议）+ §5 |
| §5 theory & effectiveness gates | §7 |
| §6 risks/threats/ethics | §6 |
| §7 decision & outcome | §8 + §9（状态机） |
| §8 AI tools & verification | §12 |

---

## S1. Stage-1 科学身份收官记录（审查 Proposal A；owner 已选定）

- **唯一 primary identity：A-SEL**（owner 裁决，Decision-Log 续32②；与 2026-07-11 四项全签的
  唯一主问题"ρ 实现率"一致）。
- **Problem statement**：在核心模型权重与结构完全冻结、外部组件全部冻结使用、推理时仅做
  多采样+选择（weight-frozen reward-guided inference-time optimization）的约束下，**label-free
  的 reward-guided trajectory selector 能否把 K-样本池中已存在的 oracle headroom 兑现为
  可部署的、超过最小实质效应量的任务效用增益**——equal-K、对 generation 随机性边际化、
  且跨任务族正向复现。
- **不做的主张（明示降级）**：RDU-vs-strongest 归因（v4.2 原 headline）降为 secondary/ablation；
  单焦点集结果只作 case study 命名；no-harm 只作 safety guard，永不称 replication。
- **Load-bearing comparison**：selector vs **pool-mean（同池随机期望）** 为主对照，
  **MBR 与 pessimistic/hedged selector** 为强 comparator（equal-K、同池同预算）；oracle 仅作
  headroom 上界（永标 headroom，不作 deployable 数字报告）。
- **Falsifier（最小杀死条件）**：焦点族 equal-K、generation-marginal 增益的 CI 下界未越过
  SESOI_sel，或增益不能在第二任务族正向复现，或 selector 不显著优于 pool-mean——任一成立
  即放弃"一般 TFRL 价值"主张（详见 §2）。
- **资源上限**：单卡 RTX 5090（24GB laptop）+ llama.cpp 冻结栈；无云训练、无权重更新；
  M2 标定预算上限见 §4.4；生成调用预算 N\* 预注册（§5.3）。
- **进入 Stage-2 的决定**：owner 于 2026-07-13 作出（续32），条件是本稿结构验证 + §11 解冻
  条件闭合。

**最近邻表（novelty checkpoint，审查 A2）**：

| 最近邻 | 它已做 | 本研究的可测 delta |
|---|---|---|
| WavRAG (ACL 2025) | 原生 audio retrieval + text/audio 混合 KB | 不比检索组织；delta 在**选择算子**：equal-K 下 label-free selector 对 pool-mean/MBR 的增益 |
| VoxRAG (MAGMaR 2025) | transcription-free speech-to-speech retrieval | 同上；本研究核心是 reward-guided selection，不是检索通路 |
| AudioRAG (2026, arXiv 2602.10656) | audio reasoning + external retrieval 基准与 agentic baseline | 冻结核心、不 fine-tune；主张对象是 selector 兑现率 ρ，非 agentic pipeline |
| SQuTR (2026, arXiv 2602.12783) | 噪声鲁棒 spoken-query 检索基准 | 用作任务床之一（数据供体），非方法最近邻 |
| BoN/reward-hacking 谱系（Gao 2023；Huang 2025；Khalaf 2025） | proxy reward 下 BoN 的过优化理论/实证 | **最强方法最近邻**。delta：(i) 语音多任务族上 label-free proxy（非 RM 训练）+ equal-K 对照族的系统测量；(ii) N\*/Goodhart 拐点作为预注册负控（§5.3）；(iii) 若理论轨落地：受约束 selector 的同对象 Lean 收敛证明（§7T，可弃） |
| MBR decoding 谱系 | label-free 共识选择 | MBR 是本研究的**强 comparator**而非被略过的近邻——H3 直接对它 |

Novelty 判定按审查 A2 的 fail 条款自检：主张不是"组件合取"；最强 baseline（MBR/pessimistic）
被实例化为可跑对照，非 prose-only；delta 有 primary atom（§1）；失败会杀死或降级主张（§2）。

---

## 1. 研究想法与可证伪假设（模板 §1）

**动机**：Stage-1 方向性证据（全部 hypothesis-grade，§3.2）显示冻结 omni 核心的 K-样本池存在
真实 oracle headroom，但已实现率 ρ 低且随条件波动（~24% snr5 / ~42% clean，C-ASR-V2 电池）。
若 label-free selector 能把 ρ 稳定兑现为超过 SESOI 的净增益，则"不改权重、只优化推理轨迹选择"
是语音 MLLM 的一条可复用能力激活路径；若不能，该路线的一般价值主张应被杀死——两个方向都
是有价值的 Stage-2 结论。

**Primary 假设族（m=2，Holm 校正；α=0.05，双侧）**：

- **H1（焦点族，headline）**：`θ_gain^focus ≥ SESOI_sel`，其中
  `θ_gain = E_g E_s [ U(τ_sel(P_{g,s})) − (1/K)·Σ_{τ∈P_{g,s}} U(τ) ]`
  ——g 为 group（speaker/session/source-family 键，§4.2），s 为独立 generation seed
  （每 group ≥⟨FG-3⟩ 个独立 K 池），τ_sel 为 label-free selector 的选择，U 为该任务族的
  预注册效用（§4.1）。**估计量是 generation-marginal**（对 s 边际化）；conditional-on-pool
  仅作 secondary 报告。
- **H2（复现族，co-primary）**：在与焦点族**不同的任务族**上 `θ_gain^rep ≥ SESOI_sel`
  ——正向、equal-K、同方向；这是审查 B3 的"正向复制"，不是 no-harm。

**Secondary（不进 headline 合取）**：

- H3：`E[U(τ_sel)] ≥ E[U(τ_MBR)]`（对 MBR 的非劣/优效，边界⟨FG-2⟩定）；
- H4：`ρ = E_g E_s [(U(τ_sel) − U_pool-mean) / (U_oracle − U_pool-mean)] ≥ ρ_min`
  （分母 floor ⟨FG-2⟩ 预注册：headroom < floor 的 group 从 ρ 计算排除并报告排除数；
  报告均值与下分位）；
- H5（RDU secondary，降级自 v4.2）：`θ_rel = (E[err_bare] − E[err_system]) / E[err_bare]`，
  分子分母在每个 paired-group bootstrap replicate 内联合重算。

**预承诺阈值**：α=0.05 现在冻结；SESOI_sel 与 ρ_min 的**数值**按 M-S2 由外部锚档案给出
（⟨FG-1⟩，v1.0 冻结件——本稿拒绝在无档案时填数）。

## 2. Success / Kill / Pivot（模板 §2；确证一次性）

- **Go**：H1 与 H2 均通过（Holm 后 CI 下界 > SESOI_sel）→ 主张"weight-frozen reward-guided
  inference-time optimization 在受测任务族上兑现可部署增益"（等级帽：development/
  controlled-benchmark evidence，§3.3）。
- **Kill**（负结果承诺，如实发表）：H1 未过 → 一般价值主张死亡，记录为负结果；
  selector ≤ pool-mean（CI 含 0 的下方）→ 方法死亡。
- **Pivot（预列，不新增 primary）**：H1 过、H2 未过 → 降级为单族 case study（标题/摘要如实
  命名）；Goodhart 拐点早于 N\*（Û↑ 而 U↓，§5.3）→ 研究对象改为 constrained/hedged selector
  （理论轨 §7T 的对象），原 H1 结果保留并如实报告拐点。
- **Mode**：confirmatory（M4 一次开火；M4_FAIL_FINAL 为吸收态，§9）。

## 3. Survey、定位与证据等级（模板 §3）

### 3.1 定位

见 §S1 最近邻表。**Novelty delta 一句话**：最近邻（BoN/reward-hacking 谱系）研究"N 增大时
proxy 选择何时失效"；本研究预注册 N\* 与四臂去相关契约，在冻结语音 omni 核心上**测量并兑现**
equal-K、generation-marginal 的 label-free 选择增益，并使失败可判死——这一测量与判死结构
在语音 MLLM 上没有先例。引用登记：本稿全部引用沿用签署审查 §8 的已核验文献（Nosek 2018、
Dwork 2015、Cawley & Talbot 2010、ICH E9(R1)、Lakens 2018、MacKinnon & Webb 2018、
Bouthillier 2021、Gao 2023、Huang 2025、Khalaf 2025、Tan 2025、Kim 2025、Yao 2024、Deng 2024、
WavRAG、VoxRAG、AudioRAG、SQuTR）——新增引用须过逐条可解析源登记后方可入 v1.0。

### 3.2 既有证据的等级声明（append-only 纪律）

以下 Stage-1 数字**全部 hypothesis-grade / directional-only**，只用于动机，不进任何确证推断：
oracle best-of-N headroom +0.042 [0.029, 0.056]（N=8，LibriSpeech test-other+snr5，n=144，
3 生成种子合并）；MBR 各 N 不显著；C-ASR-V2 ρ ~24%（snr5）/ ~42%（clean）。它们在 Stage-2
按本稿协议重建后才升级。

### 3.3 证据等级路线（M-S1，owner 续32④已定）

**public deterministic evaluation 路线**：公开 IDs/种子/基准 + 提交先于选择的确定性抽取。
本稿**预先接受**其解释帽——所得为 **development / controlled-benchmark evidence**，提供
replayability、不提供 selection blindness；论文 title/abstract 将如实定位；不作强 confirmatory
宣称；人员隔离的独立保管 holdout 不在本 program 主张范围内（若未来加做，另立 program ID）。

## 4. 数据、隔离与 M2 标定协议（模板 §4 前半；审查 B1）

### 4.1 任务族与效用（候选池 + 资格规则；winner 由 M2 在冻结规则下出）

- **候选任务族**（全部来自已冻结在盘资产，`docs/datasets.lock.json` + 候选清单）：
  ① ASR（LibriSpeech test-other 及噪声变体；U = −WER，群键=speaker）；
  ② 口语知识 QA（heysquad；U = EM/F1，群键=speaker×source-doc）；
  ③ 口语查询检索-QA（SQuTR/FiQA，须 §4.3 三层来源轴闭合；U = 检索-QA 正确率，
  群键=query-topic×speaker）。
- **资格规则（现在冻结）**：eligibility split 上 oracle headroom ≥ ⟨FG-4⟩ 且群键可用、许可
  允许、q2q 污染审计（§6.2）通过 → 合格；焦点族 = 合格族中按**预注册优先序 ①>②>③**取首个
  （不看效应大小挑最顺眼的——优先序现在定死）；复现族 = 剩余合格族中优先序次位。
- **U 的每族定义**在 v1.0 冻结（含 WER 截断/坏例语义、EM 归一化——⟨FG-5⟩）。

### 4.2 三池隔离契约（F-S5 修复为前置硬件）

- eligibility / development / confirmatory 三池 **group-disjoint**（item-disjoint 不够）：
  confirmatory 抽取先取全部 prior manifests 的 **group-key 并集**，把当前 pool 中属于这些
  groups 的 items **整组排除**，再按 group 抽样；prior manifest 持久化其 group manifest
  （或 hash+路径）使排除可重放。
- 负例测试为合并门槛：A/B 同 speaker、不同 item-ID、跨 manifest → 期望硬失败或 B 整组被排
  （F-S5 契约，实现挂 §11-2，**任何真实 split draw 之前**）。
- 沿用已落地硬门：全 draw-type 100% group-manifest 覆盖硬错、confirmatory 禁
  `force_supersede`、曝光登记册全并集机验、manifest 记 `group_manifest_hash/
  exclusion_definition_hash/pool_hash/code_sha`。
- confirmatory 细粒度结果不回流开发（solo 形态的可执行实现）：M4 输出先**封存**
  （加密/哈希登记）再由冻结脚本一次评分，向开发上下文只释放预注册的聚合判定，per-item
  明细在 verdict 记录后才解封。

### 4.3 语料/数据来源三层轴（F-S4 / 审查 Proposal D）

每个语料/数据集报三层，全 PASS 才得 `query_independent_corpus`：
`byte_identity`（自锁四检，已有）；`upstream_identity`（第二人 clean fetch + revision/LFS-OID
复核——P0-B 项）；`evaluation_independence`（构建不读 queries/qrels/labels）。
`model_pretraining_contamination` 单列描述性风险（§6.2），不由路径清白推不存在。
自锁单独存在时轴值 = `SELF_PIN_MATCH / UPSTREAM_NOT_VERIFIED`，绝不 PASS。

### 4.4 M2 标定协议（只允许预列 pilot；各用独立 calibration split）

| pilot | 标定什么 | branch rule（现在冻结的选择规则骨架） | 预算上限 |
|---|---|---|---|
| P-gen | generation 方差 → 每 group 独立 K 池数 | 取满足 power ≥ ⟨FG-3⟩ 规格的最小池数 ∈ {3,4,5}；不足则 n 加倍一次，再不足 → 报告 underpowered 并停 | ⟨FG-6⟩ GPU-h |
| P-corr | 四臂 δ_corr（§6.3） | δ_corr < 阈值 → 该信号剔除或换独立族 verifier（预列二选一） | ⟨FG-6⟩ |
| P-sim | 小簇推断法（§7E） | 冻结 DGP 网格上 Type-I ≤ 上限且 coverage 最优者，字典序 tie-break | CPU-only |
| P-q2q | 污染审计阈值适用 | 阈值预冻，仅执行，无自由度 | CPU-only |
| P-power | holdout 供给/功效表 | n 由 SESOI_sel+方差表查出，不回看效应 | 纸面 |

M2 **不得**：比较 selector 变体的任务效果、调 prompt 挑效应、接触 confirmatory 池。
selector 的 weights/K/threshold/prompt/embedder 搜索空间全枚举 + 预算入
`experiment_attempt_registry`（M-6：每次尝试带放弃理由，防 winner-only）——搜索本身发生在
development split，其全景（非 argmax 单点）随 M3 注册一并提交。

## 5. 生成随机性、comparator 与过优化负控（M-S4 / 审查 Proposal C）

### 5.1 随机性结构

外层重采样 group、内层重采样 generation replicate 的嵌套 bootstrap；每 group ≥⟨FG-3⟩ 独立
K 池（独立种子，种子表预注册）；primary 估计量对 generation **边际化**（§1 H1），
conditional-on-pool 作 secondary。

### 5.2 comparator 家族（equal-K、同池、同预算）

pool-mean（primary 对照）；MBR；pessimistic/hedged selector（不确定性惩罚，λ 网格预列）；
K=1 greedy（部署基线）；oracle（headroom 上界，只标 headroom）。random comparator 用
**池内条件期望**（pool mean-U），不再用一次幸运抽签，消除其 Monte-Carlo 噪声。

### 5.3 N\* 与 Goodhart 负控（预注册，在任何方向性结果之前）

生成预算 N\* = ⟨FG-7⟩（由 P-gen 方差与成本锚共同定，v1.0 冻结）。每 K ∈ 预列网格报告：
proxy `Û` 与真效用 U、corr(Û,U)、rank-AUROC、top-tail calibration、selected-vs-oracle regret、
generation-marginal 均值与下分位、self-consistent-error 率、abstention 收益。若在 K ≤ N\* 内
出现 `Û↑ 而 U↓` 拐点 → §2 Pivot：对象改 constrained/hedged selector，不以继续加 K 回应。

## 6. 风险、信息边界与审计（模板 §6）

### 6.1 信息边界契约（本项目失败史的第一防线）

- selector 与 proxy reward 的输入 = 候选轨迹本身 + 冻结外部资源；**任何测试 item 的
  golden transcript/answer/qrel 不得出现在 selector、reward、prompt、检索、候选构造的任何
  环节**（新信息类杠杆一律禁止；只允许 read-out 类杠杆）。
- 每个 lever 在 M3 注册时按 read-out / new-info 分类并给数据流证明（Information-Boundary
  Guard 执行单）；违反 = STOP-THE-LINE。
- 评分侧：U 由 ground-truth 脚本计算，永不由被测系统自评。

### 6.2 风险表

| 风险 | 可能×影响 | 消解门/实验 |
|---|---|---|
| Goodhart/reward hacking（Û↑U↓） | 中×高 | §5.3 N\* 负控 + 拐点 Pivot |
| 同权重 verifier 假独立 | 高×高 | §6.3 四臂 δ_corr，阈值预冻，未达即剔除 |
| 跨 split group 泄漏 | 中×高 | §4.2 整组排除 + 负例测试（P0-B 硬门） |
| 语料来源污染（自锁≠官方） | 中×高 | §4.3 三层轴；upstream 未验即不 PASS |
| 预训练回生 test query | 中×中 | q2q exact/fuzzy/semantic/**跨语言**审计（Yao 2024），阈值⟨FG-8⟩预冻；超限 item 剔除并报告 |
| 多重比较/择优报告 | 中×高 | m=2 Holm；全 sweep 报告；attempt registry 防 winner-only |
| 小簇尾部推断失效 | 中×中 | §7E 模拟契约（MacKinnon & Webb 警示接受） |
| public benchmark 适应性 | 高×中 | §3.3 等级帽如实；换代基准仅作 robustness 附注 |
| proxy ≠ 部署工件 | 低×中 | 复评实际部署选择器输出，非代理实现 |

伦理/许可：全部数据集许可与允许用途逐一登记（datasets.lock 已含）；语音为生物特征——
仅用公开研究语料、不做说话人身份推断类主张；dual-use 注：选择算子提升转写/问答质量，
无新增滥用面。

### 6.3 四臂去相关契约（M-S5）

对照族（阈值与删除规则在看任何结果前冻结，⟨FG-9⟩）：same-model/same-prompt/diff-sample；
same-model/diff-prompt；**diff-family frozen verifier**；non-model deterministic verifier。
δ_corr（误差去相关度/条件互信息）未达阈值的信号不得入 selector（Tan 2025 / Kim 2025 依据）。

## 7. 理论与有效性双门（模板 §5）

- **(T) 理论门（可弃项，不进 headline）**：仅当交付"UNCONSTRAINED 选择过程在 imperfect
  proxy 下不收敛 + CONSTRAINED（pessimistic/预算 N\*/去相关约束）过程收敛或 regret 有界"的
  **同对象**定理（Python selector ⟷ Lean 算子逐例 golden，含 ties/early-stop/K-cap/abstention）
  时，理论才作为贡献主张；否则删除理论主张，工程结果独立成立（F-10 处置）。generic
  argmax-mismatch 2ε lemma 不算数。
- **(E) 有效性门**：§1–§2 的预注册判据本身；有效性**只测不证**。
- **假设台账**：每个被假设量（headroom 存在性、proxy-U 相关下界、群内相关结构、δ_corr
  可达性）配一个测量槽（P-gen/P-corr/P-sim 交付），空槽 = 不得进 M3。

**(E) 推断机械（M-S6 契约）**：小簇/极端尾部方法（BCa / studentized-t / wild cluster /
randomization）由 P-sim 在**冻结 DGP 网格**（真实群距分布、ICC 网格⟨FG-10⟩、离散 endpoint、
缺失机制、模拟次数、独立模拟种子、Type-I 上限）上按预冻规则选出——方法选择自身零自由度。

## 8. 决策与产出（模板 §7）

结果对照 §2 判据记录 go/pivot/kill；负结果为一等公民产出（negative-result commitment）。
on-accept：Decision-Log 追加、Per-Work-Status 更新、wiki-sync；全部 claim 入 claim ledger
带 per-item 可复现工件与 `reproduce:` 一行命令；独立第三方 clean-checkout 复跑（模板 §4 要求）
+ claim 检查单代码评审。

## 9. 状态机（F-9，机读，v1.0 附 YAML）

`S2_DRAFT → S2_FROZEN → M2_CALIBRATION → M3_REGISTERED → M4_FIRED → {M4_PASS, M4_FAIL_FINAL}`；
`M4_FAIL_FINAL` 无出边（吸收态）；任何 bug 重跑 = 新 program ID，原 run 保留并解释；
M3 之后 pool/exclusion/评分脚本 hash 全部入 provenance，改动即 fail-closed。

## 10. 冻结门清单（v1.0 之前必须交付的数值/档案；本稿拒绝占位假数）

| FG | 内容 | 交付物 | 依据 |
|---|---|---|---|
| FG-1 | SESOI_sel 与 ρ_min 数值 | 外部锚档案：成本-效用推导（增益 vs K× 推理成本）、文献效应分布、专家 elicitation 记录、量纲换算；benchmark-anchored 单独不作数 | M-S2 / Lakens 2018 |
| FG-2 | H3 非劣边界、H4 分母 floor | 同 FG-1 档案 + P-power | M-S3 |
| FG-3 | 每 group K 池数与 power 规格 | P-gen 标定（branch rule §4.4） | M-S4 / Bouthillier 2021 |
| FG-4 | eligibility headroom 资格线 | 由 FG-1 换算（资格线 = SESOI 的可兑现前提），非拍脑袋 | F-S1 |
| FG-5 | 每族 U 定义细则 | 评分脚本 + golden tests | — |
| FG-6 | M2 各 pilot GPU-h 上限 | owner 资源裁定 | §S1 资源上限 |
| FG-7 | N\* 生成预算 | P-gen 方差 + 成本锚 | M-S4 / Khalaf 2025 |
| FG-8 | q2q 污染阈值（含跨语言） | 阈值备忘 + 审计脚本 | M-7 / Yao 2024 |
| FG-9 | δ_corr 阈值与删除规则 | P-corr 前冻结的规则文档 | M-S5 |
| FG-10 | DGP 网格/ICC/Type-I 上限 | P-sim 契约文档 | M-S6 |

## 11. 解冻条件（本稿 → v1.0 → Stage-2 gate 的顺序）

1. reviewer 本轮**结构验证**（§0.1 四项）；
2. F-S5 整组排除 + 负例测试落码并绿（任何真实 split draw 之前）；
3. F-S4 上游第二人 clean fetch + `query_independent_corpus` 轴语义收紧落码；
4. P0 配置轨迹重建（不可回溯处冻结列 UNKNOWN 并划定其污染面）；
5. FG-1/2/4/5/6/7/8/9/10 冻结件齐（FG-3 允许由 P-gen 在 M2 按预冻 branch rule 填）；
6. v1.0 冻结稿 + reviewer 签 Stage-2 gate（对本稿，非对 v4.2）→ M2 解冻。

## 12. AI 工具与验证（模板 §8）

沿用模板全表：引用逐条可解析源登记；AI 产数/代码须独立复现（pinned data + `reproduce:`）后
才被信任；对抗面板（统计/复现/理论/领域/anti-gaming）在 v1.0 冻结前过一轮零新发现；
共享结论入 wiki，个人便签不替代共享记录。**本稿由协调者本人撰写与核对（owner 不委托指令）；
后续机械性工程项可委托但一律过敌意复核环。**

---

## 13. 机读摘要（供 reviewer 与后续自动核验）

```yaml
proposal:
  program_id: W1-ASEL-S2-001
  version: v0.1-draft
  frozen: false
  authorizes_data_sensitive_work: false
  headline_identity: A-SEL
  primary_hypotheses: [H1_focus_equalK_marginal_gain_ge_SESOI, H2_second_family_positive_replication]
  family_m: 2
  correction: holm
  alpha: 0.05
  evidence_grade_cap: development_controlled_benchmark
  comparators: [pool_mean_primary, MBR, pessimistic_hedged, greedy_K1, oracle_headroom_only]
  estimand_primary: generation_marginal
  kill_conditions:
    - H1_CI_lower_not_exceed_SESOI
    - selector_not_above_pool_mean
    - single_set_only -> case_study_naming
    - goodhart_before_Nstar -> pivot_constrained_selector
  isolation:
    cross_split: group_disjoint_via_prior_group_union_exclusion
    negative_test_required: same_group_different_item_cross_manifest
  corpus_axes: [byte_identity, upstream_identity, evaluation_independence, contamination_descriptive]
  information_boundary: no_test_item_gold_anywhere_in_selector_or_reward_path
  freeze_gates_open: [FG-1..FG-10]
  unfreeze_order: [structure_verification, F-S5_code, F-S4_anchor, P0_config_history, FG_freeze, v1.0_gate_signature]
  theory_track: droppable_unless_same_object_constrained_convergence_lean
requested_from_reviewer_now: structure_verification_only
```
