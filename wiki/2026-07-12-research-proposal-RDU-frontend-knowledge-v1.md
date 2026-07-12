---
title: "Research Proposal（v1，供 reviewers 审阅）：冻结 Omni 模型的前端多模态知识体系——检索·发现·使用"
date: 2026-07-12
stage: "1-problem-definition → 申请进入 Stage-2 预注册"
status: "DRAFT v1.1（附录 A/B 已并入）for hostile review — owner 未签署；签署前不跑任何实验"
lineage: "G0（续12）→ 范围收束（续16/续17 口径）→ 检索-发现-使用分析（2026-07-12）；回应四轮敌对审查的全部 P0"
verdict_vocabulary: "六级状态制；证据引用一律带 claim-ledger ID；无 ledger ID 的数字 = unverified"
---

# 冻结 Omni 模型的前端多模态知识体系：检索·发现·使用
## Weight-Frozen Reward-Guided Front-End Knowledge Correction for Omni Speech Models

> **致审稿人**：这份提案是四轮敌对审查（2026-07-10 方法学审计、07-10 法证诚信审查、07-11 答复
> 复审、07-11 完成声明法证复审）之后的重新立题。你们确认的每一个 P0 都在 §9 有对应的结构性
> 预防条款。本提案未签署、未预注册；**在你们审阅与 owner 签署之前，我们不运行任何实验**。

---

## 1. 研究问题（唯一 primary question）

> 对一个权重与结构全冻结的 omni 语音模型（Qwen3-Omni-30B），在**前端**构建的多模态知识体系
> 中，**检索**（键模态：audio-direct vs own-ASR 级联）×**发现**（触发策略：恒检索 / 不确定度
> 触发 / 不检索）×**使用**（递送形式：flat / 结构化 card / 2-turn 工具递送）三维的哪个组合，
> 能对知识依赖型语音任务产生 **≥10% 相对**、经完整家族校正后统计可靠、且边界清白的改善？

**明确的非目标**：后端输出融合/重排序不是研究对象（仅作 §6 的通用 reward 信号供给层）；
GER/生成式纠错、beam 级融合、任何需要训练的接入方式，全部出界。

**术语**：对外主术语 = weight-frozen reward-guided inference-time optimization；TFRL 仅为
内部缩写（首处定义，与 test-time-RL/TTRL——真更新权重——明确区分）。

## 2. 为什么是这个问题（先验证据，全部可溯 claim ledger）

**三段各有一条我们自己数据里长出的"定律"**（Stage-1 已验，directional）：

| 段 | 已验事实 | 证据 |
|---|---|---|
| 检索 | 键空间可行：30B 自身隐态音频嵌入活体可用（2048 维）；CLAP 词汇键失效；库值必须是证据内容而非查询（对象纪律，法证 P0-1 修复）| 61 CLEAN 源 + squtr qrels 语料侧重建（W1 e30af76）|
| 发现 | **召回定律**：精度门控证伪（gate−inject=−0.134 [−.23,−.05]）——冻结 omni 对干扰鲁棒，约束是召回；**纯指令无内容有害**（真 zero-shot 指令 −0.245 [−.286,−.201]，C-MINDS-V2）| T7-R1 证伪记录；MInDS v2 因子分解 |
| 使用 | **递送形式是最大已验杠杆**：结构化 card +24.6pp（相对 +34.6%，5/5 独特对比过 Holm，C-MINDS-V2）；2-turn 工具递送使冲突采纳翻倍（0.175→0.35）；参数固执 α：冲突时仅 24% 采纳 | MInDS v2；t10/E5 清白记录 |

**反面校准**（为何不做纯选择线）：ASR best-of-N 清白重做（C-ASR-V2）显示纯选择在近饱和任务
上是结构性小增益区——oracle 上界相对 31-38%，最好的可部署 selector（logprob 置信）相对
8-16%，且完整 4×4 家族 Holm 校正后仅 clean 条件显著（噪声侧 p=.59/.075）。覆盖率理论桥
（i.i.d. 模型，预测-观测偏差 ≤2.5pp）解释了封顶机制：选择不能超出候选池内容。**结论：选择
线降级为机制标定（续16）；≥10% 量级的杠杆在知识侧。**

## 3. 预注册假设（H1–H4 + 实体粒度实例 H5）

- **H1（检索段·键模态）**：在证据语料 KB 上，audio-direct 检索的端到端增益 ≥ own-ASR 级联
  （若否——级联更强，则旗舰"omni 嵌入激活"叙事在检索段降级，如实报告）。
- **H2（发现段·触发）**：不确定度触发检索（按句 logprob/熵门限，dev 标定）在等增益下降低
  ≥30% 检索调用；恒检索不显著优于触发（召回定律的效率化）。
- **H3（使用段·递送）**：结构化 card / 2-turn 递送相对 flat 注入的增益 ≥ 检索段任何单维改进
  （递送主导假设，MInDS 先验）。
- **H4（组合）**：最优三维组合 vs（no-retrieval 基线）达到 ≥10% 相对改善且 CI 排除 0
  （完整家族校正后）；同时 random-retrieval 对照显著劣于最优组合（TOST margin=SESOI/2）。
- **H5（实体粒度实例，附录 A 调研裁定后冻结）**：在实体富集 ASR 测试床上，"发现实体倾向→
  检索热词→注入"的三段管线对实体 WER（B-WER）产生 ≥15% 相对改善——三段框架在传统热词
  技术失效（chat-API 无 beam 挂钩）处的替代形态验证。

## 4. 实验设计

### 4.1 数据（覆盖纪律：多集轻采样，每格 dev n=40）

- **主场**（知识依赖）：squtr（qrels 证据语料，检索指标可原生分解——**主 primary**）、
  heysquad（答案擦除段落）、SQuAD-zh（擦除后 source_text）；
- **闭卷锚点**：vocalbench-knowledge（参数化知识探针，无 KB——RAG 增益减闭卷增益 = 外部知识
  净贡献；续15/续16 再定性）；
- **实体粒度测试床**（H5）：附录 A 调研的 2-3 集推荐 + 偏置列表构造协议（真词+干扰词 =
  部署可得上下文惯例；列表构成/长度扫描/真词占比**预注册**，防止退化为给答案）；
- 切分：group-aware locked-DEV（seed 611741209 世代，仅 dev 侧；诚实回退标注沿用）。

### 4.2 臂族（探索层，dev only）

三维主臂 = 2（键模态）× 3（触发）× 3（递送）= 18 组合格/集；加 6 个机制对照臂（已实现、
fake-E2E 绿）：no-retrieval / random-retrieval / oracle-retrieval（上界）/ gold-transcript
（上界，边界违例标注）/ long-context stuffing / own-ASR cascade。原 Phase-A 35 臂中的纯检索
策略微调臂（top-k 扫描等）降为二级探索，仅在主臂出信号的维度上追加。**总预算 ≤（18+6）×
4 集 ≈ 96-100 dev 格 + H5 测试床 ≈ 30 格**——比原 140 格更小、更聚焦。

### 4.3 估计量与统计（回应 P0-3 与 RR-005/012）

- **Co-primary**：绝对任务 delta（组合臂 vs no-retrieval）+ 相对改善百分比；每集 cluster
  bootstrap（cluster=group_key，无组数据集如实标注 item 级回退）；
- **Secondary**：ρ（相对 oracle-retrieval 上界的实现率；Fieller/联合 bootstrap，分母策略
  预注册：CI 跨 0 的集标 unstable，不排除不外推）；检索质量 R@k/nDCG（squtr 原生 qrels）
  与端到端增益分离归因；H2 的调用率-增益曲线；
- **多重校正家族（此次全量预声明）**：每集一个家族 = 全部 24 臂 vs no-retrieval 的比较 +
  三维主效应对比（Holm + bootstrap max-T）；跨集 DerSimonian-Laird 汇总；**任何"显著"表述
  必须注明家族大小**；
- SESOI：主场任务 0.05 绝对（约 10-15% 相对，按各集基线换算并预注册具体值）；等价判定用
  TOST，margin=SESOI/2；
- 功效素描：n=40/格 × cluster 数 20-45——explora 层只做方向分级；确证层样本量在 Phase-B
  协议中按 dev 观测效应重新计算。

### 4.4 探索/确证防火墙（回应 P0-2/P0-5）

- 本提案覆盖的全部运行 = **探索层（dev only）**，产出 = Phase-B 协议（预命名赢家 ≤3 组合 +
  全部对照）；
- **确证层**：owner 签署 Phase-B 协议后，由 custodian（owner 本人 + 密封机制：与执行会话零
  共享上下文的全新会话，库外抽取，仓库只存 salted commitment）重抽 confirmatory TEST；
  基线与全部确证臂**同一通道单次评分**（单次消费条款）；读取即 burn，失败不重抽；
- 现有 65 个 locked manifest 已**永久降级**为 exposed-dev-like（明文+11.2% 旧重叠，法证
  P0-2 判定），仅作 dev 使用。

## 5. 边界纪律（Information-Boundary-Guard 实例化）

① KB 值 = 证据内容，建库池与 eval 池机器不相交（eval_manifest ∩=∅ 强制）；own-item 双重
排除；泄漏门 = 规范化子串硬门 + n-gram/嵌入相似辅门；全部 retrieved passages 入结果工件。
② 偏置列表（H5）：构造协议预注册；gold-scrub 后过 CLEAN 门；上界臂永久标注不可部署。
③ KB custody：content_hash（values+keys+ids+code sha）+ refuse-overwrite/归档式取代（已实现，
26/26 测试）；每个结果工件记录 KB content_hash。
④ Provenance：git sha+dirty=false（clean checkout 运行）、模型/引擎 hash、manifest hash、
逐项行级输出、脚本原子写出——G2-L3（真机 ref-config 重建）先绿后跑。

## 6. 通用 reward 信号供给层（后端的唯一角色）

数据集无关信号表（附录 B 调研裁定后冻结）：自身按句 logprob/熵、外部冻结文本 LM 评分
（δ_corr 去相关约束，理论账本 C4 系）、自一致性、验证器一致度。用途仅两处：**发现段触发器**
（H2 的门限信号）与**使用段信任标定**（α 校准）。标定实验为纯离线 CPU（存量池按句信号 vs
知识增益相关性），不新增 GPU 实验。**信号不用于输出重排序的研究主张。**

## 7. 理论轨（Proposal-F，与工程同对象）

在 Lean 中定义实际 selector/触发算子（candidate 分布、argmax/tie、门限触发），证明：
①工程规则正确性；②无约束反例（召回定律的形式面：过严门控的不收敛/漏检下界）；③带约束
（召回下限 + τ 可估 + N* 预算）的收敛/界；④Python/Lean 可执行 conformance（有限向量逐例）。
现有 Coverage.lean 保留为 i.i.d. 模型前置（**不计入 operator-linked**，ledger count=0 权威）；
`#print axioms` 白名单 CI 已上线。

## 8. Kill criteria（预注册，触发即执行、照常发表）

1. oracle-retrieval 在主场无增益 → 瓶颈不在检索，前端知识体系问题在该任务族**降级为负结果
   论文**；
2. random-retrieval 与最优组合 TOST 等价 → 检索选择性无价值，只报递送效应；
3. H4 的最优组合在 ≥2 集上相对改善 <10% 或家族校正后 CI 含 0 → 结论"前端知识校正在此
   规模不达标"，转投 limits 论文，不换臂追显著；
4. H5 实体测试床上三段管线不显著优于全列表塞入 → 检索式注入假设在实体粒度证伪，如实报告；
5. 确证层任何主张 = 确证 TEST 单通道结果，探索层数字永不升级。

## 9. 审稿人关切 → 结构性预防映射

| 审查确认的缺陷 | 本提案的预防条款 |
|---|---|
| P0-1 对象错配（查询当知识）| §5① 值语义 + content_hash custody + custodian 抽验 50 值（RI-2 验收沿用）|
| P0-2 假性 holdout | §4.4 custodian 密封重抽 + commitment-only + 单通道单次消费；旧 manifest 永久降级 |
| P0-3 家族缩窄 | §4.3 全家族预声明 + "显著必注家族大小" |
| P0-4 dirty/口径夸大 | §5④ clean-checkout + 行级 provenance；cell/item 双口径强制分列 |
| P0-5 未签 prereg | 本文档即 RI-3 签署对象；签署前零实验 |
| 伪重复/伪独立 | §4.3 cluster bootstrap + fold-seed 类重跑只称 split-robustness；"independent" 一词仅限真独立主体 |
| 升级表述复发 | 六级状态制 + ledger 先于叙述（续15 自查条款）|

## 10. 时间线与交付（签署后）

Week 1：G2-L3 clean 重建 + 跨模态查询路由补齐 + H5 测试床偏置协议落地 → 探索层 ~130 格
（dev，轻采样，GPU ~1.5 天）；Week 2：三维主效应分析 + Phase-B 协议起草（预命名赢家）+
理论轨 ①②；Week 3：owner 签 Phase-B → custodian 重抽 → 单通道确证 + 理论轨 ③④ →
论文解禁评估（G7 敌对复审）。

## 11. Owner / Reviewer 签字位

1. primary question 措辞（§1）；2. H1-H5 与 SESOI 数值；3. 臂族与预算（§4.2）；4. 家族定义
（§4.3）；5. custodian 密封协议细则；6. H5 偏置列表协议（附录 A 落地后）；7. reward 信号表
（附录 B 落地后）；8. kill criteria；9. 时间线。

## 附录 A：热词/上下文偏置调研裁定（全文：[[2026-07-12-omni-hotword-biasing-survey]]，33 条 claim ledger）

1. **传统技术存活性**：六大偏置族在 chat-API omni 下**无一原样存活**（分水岭=解码器内部访问，
   非训练与否）；退化替身仅三：prompt 注入 / `logit_bias`（脆弱、非序列感知）/ GBNF（仅闭集安全）。
2. **检索式注入假设：STRONGLY SUPPORTED**（≥5 独立团队，Qwen/Phi 族实测）：整表塞入毁转写
   （N≥100 灾难幻觉，"list-vomiting"），**检索 top-2 小子集是甜点**。
3. **对 H5 的两条强约束**（预注册进设计）：①赢家检索器多为专训——"冻结 omni 嵌入作热词键是否
   足够"本身就是 H1 在实体粒度的形式，作为显式待测假设；②**同音/近音污染是音频相似检索的
   第一失效模式**——发现段定律按粒度分化：**段落级召回优先（已验），实体级需显式精度约束**
   （本提案的一个新预注册子假设 H5a）。
4. **H5 测试床冻结**：LibriSpeech + is21_deep_bias 列表（英文正典协议）；AISHELL-1 + AISHELL-NER
   （中文，音频在盘）；SLURP（实体+三杠杆全适用）。指标：B-WER 主、U-WER/整体 WER 副；
   偏置协议 = 检索步替换 oracle 列表（真词+干扰词、列表长度扫描 {2,5,10,50} 预注册）。
5. **白空间臂**：A-inj-logitbias / A-inj-gbnf（文献未用过的部署杠杆）——探索层收录；警示：
   LOGIC 类比显示纯 logit_bias 仅 ~9% 相对（门槛线下），达标形态预计是检索短列表 prompt +
   闭集 GBNF 组合。

## 附录 B：reward 信号收割（全文：[[2026-07-12-omni-lm-rescoring-survey]]，20 条 claim ledger）

1. **数据集无关信号表（供发现段触发/使用段标定）**：自身按句 logprob/熵（已存）、外部冻结文本
   LM 的 PLL/约束式评分（δ_corr 去相关，ROVER-Fiscus 1997 为可引祖先）、自一致性。**约束式选择
   是唯一安全 training-free 原语；自由生成式纠错（GER）在强基线上劣化且幻觉（3-12% 幻觉词），
   出界。**
2. **文献格局**：GER 谱系主导者 = NTU-SG↔NVIDIA↔IBM 集群（Huck Yang 枢纽）；冻结分析线 =
   剑桥 CUED；**"omni 自产 N-best 的 training-free 二遍处理"为已核验空白**——本提案 §6 的
   触发器标定实验恰落此格（但按 owner 定向仅作 reward 基础设施，不立方向主张）。
3. **工程分账（防效应污染）**：官方 test-other 2.48% vs 我们 oracle@8 3.57%——重排序结构性
   够不着官方数字；~3.3pp 差距=llama.cpp 实验音频路径+Q8 量化+子集，**工程票 #35 单独追踪，
   永不计入 TFRL 效应**；一切对外 WER 带栈标注。
