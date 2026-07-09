# 2026-07-09 · Stage-1 双轨闭环战役设计书（理论⟷数据 debate-verify-improve loop）

> **性质**：Stage-1 战役设计文档（讨论材料，待 owner 讨论门冻结后执行——**不冻结不开跑**）。
> 落实 owner 2026-07-09 三条方法论要求：①理论辅以小规模数据验证并跑 debate-verify-improve loop；
> ②理论有充足 survey 支撑、以 Lean 保证收敛与一致性、显式提取假设与约束项；③数据验证覆盖全部
> 本地数据集（无 silent cap）。
> **分工硬约束**：Fable 5 只做协调/判据冻结/对抗验收/综合/裁定；技术验证+调研 → Opus；代码 → Sonnet。
> **配套**：`2026-07-09-three-anchors-delta-regrade.md`（锚点增量再定级）、
> `2026-07-09-q1q2-embedder-granularity-decision-memo.md`（Q1/Q2 决策单）。

## 0. 战役结构

```
P1 收口三文档 → P2 Owner 讨论门(冻结测量协议) → P3 前置工程(Sonnet)
   → P4 理论轨(Opus survey → 假设/约束台账 → Lean) ⟷ P5 数据轨(全覆盖小规模测量)
   → P6 debate-verify-improve loop(Opus 辩论组) → P7 记录/同步
```

**原型迭代（loop 第 0 轮，已 organically 发生）**：T7 正结果被泄露审计证伪 → τ 理论解释失败
（TF-IDF 相关性代理 τ 过大）→ T8 清白重跑 null → 理论目标改进为 τ*>0 邻域收敛。本战役把
这个循环制度化。

## 1. 假设/约束台账（理论轨 ⟷ 数据轨的双向绑定表）

**纪律**：每条定理显式列出假设与约束项；**每个被假设的量必须有数据轨测量落点**——不再允许
"convergence-by-assumed-bound" 而假设量从未实测（2026-07-09 理论审计确认这是现状病根：三个
收敛定理全部是 squeeze_zero 套在外部假设的 τ→0 / blind-spot→0 上）。

| 约束项 | 理论角色 | 现有定理（状态，均已 2026-07-09 Opus 复核） | 可测代理量 | 测量落点（数据集） |
|---|---|---|---|---|
| **τ** 选择器估计误差 | C4：realized ≥ oracle − 2τ | `Realization.lean` `realized_gap_le_two_tau`（已证恒等界）；`realized_tendsto_oracle`（**条件性**，τ→0 为假设） | selector-vs-oracle 差 | ASR：librispeech dev/test(+snr5) 切片；QA：heysquad-scrubbed / spoken-squad / SQuAD-zh；MCQ：mmau-mini / mmsu / big-bench-audio |
| **τ\*** 门控注入邻域半径 | **Stage-2 定理目标**（P4 ①）：负半=τ>τ* 无门控不收敛；正半=门控+召回下界 ⇒ 收敛到 oracle−f(τ*) 邻域 | 不存在（待证） | 门控曲线：注入收益 vs 检索相似度/一致性阈值 | ASR 困难样本记忆：librispeech train→dev/test；aishell-1（待 lock 增补）zh 侧 |
| **N\*** 预算上限 | C2：过优化上限 | `Iterate.lean`（已证，抽象形式；**待落到 best-of-N 具体算子**，P4 ②） | 真实 N-曲线的内部极值 | W1 既有 best-of-N 机制：librispeech test-other+snr5（n=144 底座已存在） |
| **δ_corr** 双系统去相关 | TH2a：regret ≤ B·blind-spot | `BlindSpot.lean` `total_regret_le`（已证界）；`avg_regret_tendsto_zero`（条件性） | generator/verifier 错误相关系数 | QA/MCQ 各集（双系统 = 同权重不同 context） |
| **R** few-shot 可达界 | 上限定理：有界重加权抬不动过低概率答案 | `Reachability.lean` `too_improbable_unreachable`（**已证上限**——注意方向是限制注入而非支持注入） | few-shot 对输出分布的影响幅度 | minds14（intent ICL）、slurp（slot ICL）、SQuAD-zh |
| **α** 采纳率/参数固执 | τ 大的机制解释（目前仅 docstring，非定理） | 无定理；经验 T9=0.237、T10 递送翻倍 0.175→0.35（**均无 CI，重测须补**） | 反事实采纳率 × 递送形式（flat vs 2-turn tool） | QA/MCQ 全部纳入集（T9 协议扩展） |
| **召回下界** 检索质量 | τ* 定理的前件之一 | 无定理（作为显式假设进 τ* 定理） | 各嵌入器 × 各任务族 R@k / kNN 指标 | **全覆盖矩阵（§2）——同时裁决 H-a vs H-b** |
| Beirami KL 界 | best-of-N 的 KL 信赖域率 | `BestOfN.lean:90` **唯一 sorry**；`kl_best_of_n_le`/`regret_O_sqrt_log`/`gain_le_of_hoeffding` 把硬内容作假设前件（已复核 CONFIRMED） | N-曲线间接校验 | 同 N* 行 |

**理论轨 Lean 工作单（Opus 执行，驱动 lean:lean-proof / lean:mathlib-build；只对 Windows 提交树
`proofs/tfrl/`）**：① τ*>0 门控注入邻域收敛（负半+正半）；② N* 落到 best-of-N 算子；③ 清欠——
Beirami sorry 证明或降级为显式带引用假设、Pinsker/Hoeffding 前件消除或钉为显式假设；④ 一致性——
dual-track binding 从 docstring 升级为测试（代码算子 ⟷ 定理假设的 CI 检查）。
**理论轨 survey 单（Opus，post-2025 窗口，text/VLM 域同权重）**：检索增强推理的收敛/一致性理论、
gated kNN（kNN-Whisper 一系）、trust-region 推理时优化、over-confidence 形式化先例——
finder→adversarial-verify 工艺，产出带验证的引用台账。

## 2. 数据覆盖矩阵（底数 = E 盘机器盘存，2026-07-09）

**底数核定（机器盘存，不信 manifest）**：39 个数据集在盘 = lock 28（全部 COMPLETE）+ gap 候选 7 +
WS-D 候选 4；零无主目录。模型 18 个在盘 = lock 6 + 候选 12 全齐（**嵌入器对决候选池已就位**：
GLAP 3.2G、LCO-Omni 3B/7B GGUF、Emotion2Vec-S、emotion2vec-plus-large、ERes2NetV2-zh、CAM++-zh、
WavLM base+/large、MERaLiON-SE2、ReDimNet-b6、CLAP、omni-embed-nemotron-3b）。

### 2.1 纳入清单（26 个，按任务族）

| 任务族 | 数据集（loader 状态） | 测量项 |
|---|---|---|
| ASR en | librispeech dev/test 切片（部分：W1 bon 脚本有）；train 960h 只作记忆池 | τ、N*、门控曲线、检索质量 |
| ASR zh | aishell-1（无 loader；**待 lock 增补裁决**）、thchs-30（无；朗读多样性补充） | 同上 zh 侧 |
| ST/LID | covost2（无）、fleurs-r zh/en 子集（无） | 检索质量、τ（生成任务侧观察项） |
| SER+SID | crema-d（无）、meld 切片（无）；esd、csemotions（无；zh-SER，待 lock 增补）；cn-celeb1、voxceleb1-test（无；SID，待 lock 增补） | **特化键对决（H-a）+ W4 单空间读出（H-b）** |
| SLU intent | minds14（**有** zh）、slurp（无）、speech-massive（无；eval-only license 注意） | 检索质量、R（few-shot 影响）、α |
| SLU slot | slurp、speech-massive（均无——**slot 金标唯二来源，P3 必修**） | 两级检索方案验证、R |
| 音频理解/推理 MCQ | mmau-mini（**有**）、mmsu（无）、mmar（无）、big-bench-audio（**有**） | τ、α、δ_corr |
| 口语 QA | heysquad-scrubbed（T8 内联）、spoken-squad（**有**）、uro-bench/SQuAD-zh（**有**）、vocalbench-zh（**有**）、audiocaps-qa（无；声音事件 QA——CLAP 合法域） | τ、α、δ_corr、检索质量 |
| 备定 | squtr（21G）、audio2tool、auditorybench-plusplus（任务定位与测量项在 P3 核定 loader 时一并定，**不许静默跳过**） | 待定 |
| 可选 | cn-celeb2（73G，仅当 cn-celeb1 不够用） | SID 扩展 |

loader 现状：**7 有 / ~19 无**——P3 的主工程量（多为 parquet/清单读取）。

### 2.2 显式排除清单（无 silent cap，每条带理由）

| 数据集 | 理由 |
|---|---|
| air-bench | 异构非检索结构（07-08 盘点判定） |
| voicebench（整体） | 评分复杂；其 QA 子集若纳入在 P3 单独裁决 |
| voiceassistant-eval | 超出简单 QA 范围 |
| audiomc | 需交互 rollout（registry 已标 deferred） |
| soulx-duplug | 非知识任务 + 全双工已出局（owner 2026-07-06 裁定） |
| eva-bench / tau2-bench | 需模拟器 / 外部 DB 环境（离线不可行，E6 记录） |
| seed-tts-eval | TTS 评测，非检索/知识任务 |
| aime24/25/26 | 纯文本数学，无语音键 |
| m3ed | 不在盘（百度盘手动，owner 已豁免） |
| slue-sqa-5 / esc-50 / fsd50k / mlc-slm / full-duplex-bench-v3 | 不在盘（前三=未取的开放候选；mlc-slm=gated 已弃；full-duplex=渠道不稳已弃） |

### 2.3 测量协议底座

X-ARES（22 任务 probe/kNN 骨架）+ VocSim（training-free 内容同一性协议）为协议底座；
**kb_snapshot（item-id 冻结）+ kb_audit（泄露审计）从第一天强制接入**——不再允许 parquet 行序
可复现性（07-08 审计刺 3）。CLAP 全程作负对照（协议有效性检验：好协议必须把 CLAP 在内容任务上
判死）。全部结果 JSON：sample_manifest + directional 标签 + boundary 字段如实 + 显式采样参数。
GPU 共驻：嵌入器默认走 CPU（既有先例），7B 级与 llama-server 分时（讨论门定）。
每数据集 n≈40–60（Stage-1 方向性标准），全程过 Information-Boundary-Guard 四问。

## 3. debate-verify-improve loop 协议（P6）

1. **对齐**：台账每行 = 一条理论声称（含约束项）× 一组数据判定（支持 / 证伪 / 域外）。
2. **辩论**（仅对分歧行）：Opus 理论辩方 vs Opus 数据驳方，各出一份 brief（引定理原文与数据
   JSON 原值）；Fable 裁定：理论错（改约束项/收窄声称）、数据错（重测/修协议）、或两者兼有。
3. **改进动作**三类：修约束项（如 τ→0 改 τ*>0）、新增 Lean 目标（进理论轨工作单）、换杠杆
   （如精度门控→召回优先，T7→T8 先例）。
4. **复测** → 回到 1。**干涸判据**：连续一轮无新分歧；或 owner 叫停。
5. 每轮产出 dated wiki 文档（append-only）；**提升空间清单是 loop 的正式交付物**。

## 4. 工程前置（P3，Sonnet，讨论门后执行）

优先级建议（owner 裁决位 +11）：**P0** = retrieve 侧强制 verdict 门（当前只写不查——任何新实验的
前置）+ kb_snapshot 接入一切新跑；**P1** = 纳入清单 loader 补齐（~19 个）+ 嵌入器 loader
（GLAP/E2V-S/ERes2NetV2/WavLM + nemotron 官方 API 修复 + llama.cpp embedding 导出探明）+
llama.cpp SHA 钉扎 / GGUF hash 钉扎 / 采样参数显式化；**P2** = KB schema 演进
（key_granularity/span/grain）+ lock 元数据修复（aime/seed-tts 误标、10 处 unpinned revision 注记）
+ reproduce 字段 E 盘更新 + registry "built" 虚标修正。

## 5. 冻结与升级纪律

本战役全程 Stage-1：结论一律 directional，不做显著性声称；进 Stage-2 的对象（τ* 定理、H-a/H-b
胜者的大规模验证）须新开 Research-Proposal-Template + 预注册判据冻结会。证据分级沿用
append-only 再定级纪律。
