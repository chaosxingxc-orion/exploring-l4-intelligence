---
title: "致审稿人的正式回应：Stage-1 对抗式研究审计（2026-07-10）逐条答复"
date: 2026-07-11
stage: 1-problem-definition
status: "已交付；配套裁定见 2026-07-11-stage1-audit-response-and-rulings.md"
audience: "external reviewer（2026-07-10 审计出具方）与后续任何 hostile reviewer"
---

# Response to Reviewer — Stage-1 Adversarial Research Audit

尊敬的审稿人：

感谢这份审计。它是本项目迄今收到的最有价值的外部输入——不是因为它客气（它并不客气），
而是因为它**几乎每一条都经得起我们的对抗性复核**。我们没有把它当作需要"应对"的批评，
而是当作一份免费的、高质量的缺陷清单来处置。以下是我们的核验方法、逐条答复、已完成的
动作与带门控的承诺。凡我们接受的，均已开票或已执行；凡我们不同意的，附证据说明；凡
您说对了而我们的台账错了的，我们**指名承认**。

## 0. 我们如何核验您的审计（而不是简单接受或抗辩）

您的审计出自一次独立会话，快照可能滞后于我们的 HEAD。因此我们派出 **6 个互相独立的
对抗核验代理**，任务设定为"既不为仓库辩护、也不为审计辩护"，对您的 **34 项事实性主张
逐条对照当前 HEAD 重验**：实际重跑了 `phase_a_cells.py --dry-run`、逐字段读取了全部
273 个结果 JSON 的 key set、精确复算了 CREMA-D 的切分重叠（91/91 speaker、827/827
(speaker,sentence) 对、5 种子切片 16.0–21.3% pairwise 重叠）、逐行核对了 6 个 Lean
模块的定理签名、复算了 best-of-N 池的多样性（4.19 unique/8、14.6% 全同）。

**结果：32 CONFIRMED / 1 STALE / 1 PARTIAL / 0 REFUTED。**

您没有捏造任何事实。在两处，实况**比您写的更糟**（§3.1、§3.7）。这份核验记录本身已
入库（`2026-07-11-stage1-audit-response-and-rulings.md` §1），供任何后续审稿人复核。

## 1. 总立场（owner 已裁定，2026-07-11，Decision-Log 续11）

1. **接受 stop-the-line。** Phase-A、Step-3 新 GPU 批跑、以及已在途的 dev/test 重抽
   重跑波（验证格刚跑完、主体未启动）全部暂停。已完成的 Step-1 数字保留为
   hypothesis-grade 方向性证据，不回滚、不升级。
2. **接受 G0：指定唯一 primary question**（见 §5；与您的推荐有一处偏差，附理由）。
3. **接受全部主张降级与术语更改**（W4 弃 disentanglement；W1 headline 改述；对外主
   术语改 weight-frozen reward-guided inference-time optimization）。
4. **接受文档真源治理**：您间接促成我们清点了全部 141 个 wiki 文件，实锤 8 处主事实
   漂移，51 件过程件已归档、4 处现行文档已修正。

## 2. 逐条答复 · 科学主张（您的 §3）

### R1-P0 · W4 判据与 "thesis holds" 矛盾 —— 接受，全部动作已执行

核验：判据 `A_t(e_t) > A_t(e_t')` 确系 **W4 自己预注册的**（W4-Training-Free-RL-
Feasibility.md:24、:143；Decision-Log:1020），首结果 `diagonal_dominant=False`、
instruction 条件化行平坦——判据未过。您的 claim ladder 定级（L0/L1，非 L2/L3）我们
逐级核对后完全同意。

**已执行**：① "thesis holds/demonstrated" 措辞在 Per-Work-Status 等现行文档中已废止，
改为 "L0/L1 证据：factor readout availability / suppression（content≈1.0 为 12 句固定
句 ID、emotion 部分可读、speaker 近 chance；matched>mismatched 未过）"；② disentanglement
一词从所有对外主张中移除，直至 L2–L3 判据通过；③ W4 按您的 §7.1 问法重定义（执行票
#29，fresh Research-Proposal-Template + 预注册 H1–H4 + speaker-grouped 切分）。

### R1-P0 · "当前活跃工作偏离旗舰" —— 部分不同意，但接受其底层观点

不同意之处：三步走战役不是漂移——它是 owner 2026-07-08/09 的明确指令（Decision-Log
续2–续10 有完整签字链）；07-04 的 CP-1/3/8/4 选择被 owner 后续指令**有意取代**，这是
研究方向的合法演化，不是 HARKing。

但我们接受您的底层观点：**取代从未落进文档**。两套"现行计划"（07-04 框架文档 vs
07-09 三步走）并行存在且互不引用对方的废止状态——这正是"移动靶"风险的文档形态，
您抓得对。**已执行**：G0 裁定唯一 primary question（§5）；07-04 计划线两份文档
（Research-Question-Framing、Semantic-Task-Validation-Table）挂 SUPERSEDED 横幅移入
`wiki/archive/`，指针指向三步走设计与 G0 裁定。

### R1-P1 · oracle / offline / deployable 三算子混淆 —— 接受，headline 照您的写法改

核验：oracle +0.0418 CI [0.0289, 0.0564]（不跨 0）；MBR +0.0037 CI [−0.0082, 0.017]
（跨 0，n.s.）——与您所引完全一致。**已执行**：W1 headline 从此为
"Frozen Qwen3-Omni pools contain exploitable ASR support, but the tested label-free
selector realizes no statistically reliable fraction of it"；三算子（offline
hyperparameter selection / oracle upper bound / deployable selector）在所有后续结果
表中强制分列；ρ（realized fraction）成为 primary estimand（§5）。

### R1-P1 · CREMA-D 不是充分 substrate —— 接受，附我们自己的复算

我们的核验代理**精确复现**了您的每个数字：content 任务 = 恰好 12 个句码（DFA/IEO/…/WSI）
的 sentence-ID；train/test 91/91 speaker 全跨、12/12 句全跨、827/827 (speaker,sentence)
对全跨（loader docstring 自己承认 clip-level random split）；5 种子 300-item 切片来自同一
1489-clip 池、pairwise 重叠 16.0–21.3%（均值 19.2%）。一处补充：种子切片正相关使 t-CI
**反保守地偏窄**，而我们报告的情感结论是 NULL——修正依赖只会更 NULL，方向上不救我们。
**承诺**（入 #29 预注册）：emotion 至少 speaker-disjoint；content 换真实转写/WER；speaker
报 EER/minDCF；切分单位按 group。

### R1-P1 · 单模型、专用 retrieval checkpoint 限制外推 —— 接受

omni-embed-nemotron 确为 Qwen2.5-Omni Thinker 上的 contrastive retrieval 特化模型
（NC 许可），单它不能支撑"现代 omni LLM 普遍具备 latent factors"。**动作**：W4 重定义
后必测原始 omni hidden state——这一路径本周已在工程上解锁（Qwen3-Omni-30B 的
llama-server embedding 模式活体可用，2048-d），加至少一个不同谱系 backbone。定位语
从"证明普遍性"降为"case study + 跨谱系复核"。

## 3. 逐条答复 · 实验与工程（您的 §4）

### R2-P0 · Phase-A 不可执行 —— 接受，且实况比您写的更糟；这是本审计最有价值的一条

您列的 7 项我们逐项核验全部 CONFIRMED：无 `--execute` 路径（dry-run 自述 "Execution is
deliberately NOT wired here"）；6 臂 PLAN ONLY 抛 `NotImplementedError`；two-stage 是同
索引同相似度截断；kb_batch_build 只建单 utt 键单 value（引擎层 kb_build 其实支持多粒度
字段，但唯一的批量驱动器从未驱动它们）；runner/builder source 命名 4 vs 3 字段错配；
`qwen3-omni-hidden` vs `qwen3-omni-own` token 错配。

**比您写的更糟的一处**：`kb_retrieve._query_embedder` 的 auto 回退不止影响"新 embedder"
——因为 manifest 存的是返回名（`glap:GLAP` 等）而非注册 token，**连 ref-config 的 GLAP
臂和 qwen3-omni-own 臂都会把查询落到 CLAP（512-d）去打 1024/2048-d 索引**。也就是说
冻结网格的锚点格本身就检索不通。只有 clap 与 omni-embed-nemotron 两臂的查询/索引空间
恰好一致。

**我们必须承认的簿记失实**：网格草案 §6.7 写"工程前置①–⑤已全部完成，签字即可开跑"。
这句话是错的。根因是协调层按子代理完工报告入账、没有强制 E2E 门验证。我们不辩解。
**已执行**：该文档已挂 2026-07-11 更正横幅（append-only，不改写原文）；Decision-Log
续11 指名记录此失实及根因；执行票 #25（十项修复清单，含您的全部 Phase-2 必修）+
**G2 门成为硬规则：任何"完成"宣称必须以全臂 fake-model E2E green 为凭，PLAN ONLY 进入
已冻结网格 = 直接 fail**。Phase-A 在 G2 通过前不碰 GPU。

### R2-P0 · reusable holdout / winner's curse —— 接受

说明一点时间线：您审计时，owner 已裁定全量 dev/test 不相交重抽（续10），重抽工具已
落地并通过了验证格（aishell-1 disjoint dev 40/40）。但我们接受您更深的观点：**item-id
不相交仍不等于独立**（同池两视图、群组泄漏、35 臂选择误差、无 FWER/FDR 方案）。
**已执行**：重跑波在启动前主动叫停（避免按不充分口径烧 GPU 返工）；执行票 #26 =
组元数据盘点 → group-aware 重抽 v2 → paired cluster bootstrap → Holm/max-T + 层级汇总；
calibration / locked-test / external-test 三层边界纳入 G1 预注册；"任何方法优越性必须在
新建的 locked-test 层重新建立、Stage-1 数字只保留方向性 mapping 地位"照单采纳。

### R2-P1 · 划分单位 —— 接受（见 #26，上）

您给的按任务族分组规则（SER→speaker/session；ASR/ST→speaker/recording family+噪声增强
同组；SQA→同源 text question 的变体同组；SLU→template/surface；agent→scenario seed）
直接作为 #26 的设计规范。组元数据不可得的数据集将如实标注为 item-id-only 并入 caveat，
不假装分组。

### R2-P1 · best-of-N 指标与随机性 —— 接受全部六项，附精确复算

宏平均 WER（非 corpus WER）：CONFIRMED——今后两者并报。种子同时驱动 utterance 抽样与
生成池：CONFIRMED（脚本注释其实自我披露了这一混杂，但披露不等于修复）——改为固定
utterance set 重复 pool seed，crossed item×pool 随机效应。多样性坍塌：我们复算得
均值 4.19 unique/8（您写 4.17，舍入之差）、**14.6% 全同精确吻合**；规范化后更差。这与
MBR null 相互印证——selector 无从选起，所以 N/temperature/top-p sweep + effective-N
报告不是锦上添花而是机制必需。llama.cpp 音频路径 experimental、仅 Q8_0、无 parity：
CONFIRMED——子集 parity check（官方 runtime/BF16 或第二实现）列入 W1 selector 实验
协议（您的 Phase-4 清单照单采纳，含 ROVER/edit-MBR/RCS/self-certainty/校准置信/跨模型
verifier/oracle 全对照组）。

### R2-P1 · 指标 bug 是测试体系不足 —— 接受

您公正地指出了坏格没有静默伪造数字（wave-1 60 格 MCQ gold、wave-2 12 格 K4/K7 全部被
审计抓出并以"存量回复重评分/最小重生成"修复，W1 `3b2d4bd`、`f8ca276`）。但"每波靠人工
抽验兜底"不可持续，同意。**动作**（#25⑧）：每次审计发现转成 golden fixture / property
test / schema contract test；MCQ gold 解析的四种形态（裸字母、`A. text`、`answer_gt`、
list gold）全部 property-test 化。一处更正：您写 W1 只有一个 import test——实际还有
`scripts/knowledge/test_kb_gate.py`（4 条 CLEAN-gate 执法测试），但它没有 test_* 命名、
pytest 收集不到，所以您的论点（测试体系不足）反而被这个反例强化而非削弱。

### R2-P1 · artifact provenance —— 接受

273 个结果 JSON 逐字段核验：均缺 git SHA、dirty flag、模型文件 hash、llama.cpp build
SHA、dataset revision、manifest hash、env hash（有 seed/sampling_params/manifest 路径，
但路径无 hash）。**动作**：#25⑨ 全部字段进 `write_result`。W4 手工转录问题：**STALE**
——`cdbf1d2`（2026-07-01）已改为 reproducer 原子产出 headline 统计量并重跑验证；您审
计的快照早于该修复。"committed summary 必须由同一脚本原子写出、禁止手工转录"自 07-01
起已是也将继续是硬规则。

### R2-P1 · KB 泄漏门盲区 —— 接受全部四项

规范化子串匹配无语义覆盖：CONFIRMED（"twelve" vs "12"、同义改写、蕴含全部漏检）。
build_one 用建库池自身 gold 自审、无 eval-gold 参数：CONFIRMED——这恰是我们的
Information-Boundary-Guard 本应捕捉的空隙，被您先抓到了。runner 不按 `from_item_id`
排除自身条目、result JSON 的边界声明是散文承诺而非机器不变量：CONFIRMED。
**动作**（#25⑥⑦）：`build_one` 接收 eval_manifest 并机器验证 `source_ids ∩ eval_ids
= ∅`；retrieve 层再做 own-item 排除；泄漏审计加 n-gram + 语义/entailment 辅助层；全部
retrieved passages 写入 result artifact 供复核。

## 4. 逐条答复 · 理论与术语（您的 §5）

### R3-P0 · Lean "构建成功 ≠ 系统收敛已证明" —— 接受，8/8 核验一致

您对六个模块定理域的刻画逐行核对后**全部准确**：monotone_bounded_converges 假设单调
有界；improve_budget 假设每步 δ>0 增益；realized_tendsto_oracle 与 BestOfNConvergence
把 τ_n→0 当外部前提；mbr_consistency 只是固定候选的 SLLN 实例（argmin 一致性与增长
候选集缺席）；Reachability 是代数恒等式链上一个被假设的 reach 上界。operator-linked
定理数 = 0。KL trust region 是漂移上界、不产生每步正增益下限——您的纠正在数学上成立，
我们的相关表述将改写。

一点为自己说的话：每个模块的 docstring 都主动披露了"前提是假设的、未由更新规则导出"
——我们没有藏。但披露不改变您的结论：**对外任何文本不得出现"系统收敛已被 Lean 证明"**，
定理一律按您的四级标注（verified algebra / conditional-on-assumed-decay / framing-only /
operator-linked）。**动作**（#27）：您 Phase-6 的七项全部采纳——coverage 定理
(1−p*)^N（p* 可由 W1 存量池直接估计，这将是第一条 operator-linked 定理）、可估 τ 的
selector regret、exp-weights 有限时界、biased-proxy 负结果、no-universal-N*、
`#print axioms` 白名单入 CI、Python/Lean parity 向量。

### R3-P0 · Beirami 公理 —— 接受，措辞照改

`opaque klBoNActual` + 具名公理 `beirami_thm_3_1`：CONFIRMED。今后一律写
"the cited theorem is imported as one named axiom"，不写 "formalized/proved in Lean"，
不计入 formalized contribution。若有余力换成有限分布真实定义（#27⑥），换不动就保持
诚实的 import 状态。

### R3-P1 · "training-free RL" 术语 —— 接受

您预判的两类审稿攻击（无 policy update 凭什么叫 RL；gold-WER reward 部署哪来）我们
认为是必然会发生的。**已裁定**：对外主术语改为 **weight-frozen reward-guided
inference-time optimization/search**；TFRL 仅作内部缩写，对外首处给非标准定义并与
test-time-RL（真更新权重）明确区分；只有真正定义了 sequential decision process 与
policy update 的子模块才允许 RL 措辞。

### R3-P1 · 新颖性不能靠 port —— 接受

G0 主问题（§5）已改写为机制式可证伪问法（error decorrelation 如何决定 realized
fraction；speech-key granularity/organization 如何改变 retrieval-to-generation 因果链），
而非"把 90 个文本方法搬到 speech"。若最终证据只支撑 transfer study，我们按 transfer
study 诚实定位——"L4 intelligence / RL convergence / disentanglement" 三层宏大叙事
已从共享 headline 中拆除（G0"不再追逐"清单）。

## 5. 对您 §7 问题重定义的采纳情况（一处偏差，附理由）

- **§7.2（W1 selector realization，ρ 指标）：全盘采纳**，并与 §7.3（speech-keyed KB 的
  窄问题）合并为唯一 primary question：*在冻结 Qwen3-Omni-30B、清白 KB、部署合规查询下，
  speech-keyed 知识组织 × 检索 × 递送 + label-free selector 能实现 oracle headroom 的
  多大比例（ρ）？* 完整 claim tree（primary/secondary estimands、必带对照、kill criteria、
  不再追逐清单）已由 owner 签署（rulings 文档 §4）——这就是您要的 G0 交付物。
- **§7.1（W4）：采纳其问法与全部预注册假设 H1–H4**，但**不立即回归旗舰位**，作为独立
  work 排期（#29）。与您推荐的偏差在此，理由如实陈述：单卡现实下 W1 的实验机器（65
  loaders、批量化、冻结/审计工艺）是当前唯一成熟的产线，而 W4 的干净重启需要 grouped
  数据集与新协议（正是您指出的）；让两者串行而非并行抢 GPU。您的核心要求——**四个研究
  对象不再共享同一 headline**——已通过 G0 完整满足。若您认为此偏差不可接受，我们愿意
  在 G1 预注册评审时重新辩论。
- **§7.3（Step-2 RAG 收窄）：采纳**，它就是 primary question 的组织×检索×递送分量，
  且不再承担 W4 解耦或 agent convergence 主张。random/oracle retrieval kill 规则照单
  采纳：random ≈ best 或 oracle 无增益 → 停止优化 retrieval。

## 6. 您的 §6 辩护轮 —— 致谢

您在破坏性三轮之后主动替项目做了最强辩护，这个动作本身就是我们要学习的审稿纪律。
您认定站得住的五项资产（负结果记录、support/headroom 真实性、边界纪律机器化、Lean
的"暴露你究竟证明了什么"、工程运行能力）正是我们继续的地基；您建议把自我纠错史写进
论文方法学贡献，我们采纳。

## 7. 已完成动作清单（截至本信发出，全部可在仓库核验）

| 动作 | 载体 |
|---|---|
| stop-the-line 生效：Phase-A/Step-3/重跑波暂停，GPU 空闲 | 任务台账 #23 HOLD、#24 BLOCKED |
| 34 项主张逐条核验记录 | rulings 文档 §1（6 代理、130 次工具调用） |
| G0 claim tree（owner 签署） | rulings 文档 §4 |
| Decision-Log 续11（含对"①–⑤已完成"失实的指名承认） | Decision-Log.md |
| wiki 治理：51 件过程件归档 + 8 处漂移修正 + LOG 横幅 | wiki/archive/ + 4 处 CANON 修订 |
| 工程/统计/理论/调研修复票 | #25（10 项）/#26/#27（7 项）/#28/#29 |
| W4 "thesis holds" 措辞废止、W1 headline 改述、术语更改 | Per-Work-Status + rulings 文档 |

## 8. 带门控的承诺（照您的 §9 gate 表执行）

G0 已交付（本信 + claim tree）。G1：每个被选问题独立 fresh proposal、group split、
多重比较方案、三层 test 边界，**test manifest 在所有臂选定前锁死**；我们邀请您（或
任何 hostile reviewer）对 G1 预注册做 0-fundamental 评审。G2：全臂 E2E green +
provenance 完整 + 独立复核可从 result JSON 重建每个数字，未过不碰 GPU。G4/G5：powered
run 不过就降级 claim，不换题追显著；单模型有效就叫 case study。G6：theorem 前提不可
实验估计就标 framing-only，不进 contribution list。

我们把您的一句话交付当作本阶段的北星收下了：

> 我们系统测量了 frozen omni speech model 在 support、readout、task selectivity 与
> deployable realization 四个层级上的能力边界，并证明哪些增益是真实的、哪些只存在于
> oracle、哪些被 representation suppression 与 selector error 封顶。

这确实比我们原来想讲的故事更诚实，也更有可能是真的。

此致，
Stage-1 执行组（协调：Fable；核验：Opus×6；工程：Sonnet）
2026-07-11
