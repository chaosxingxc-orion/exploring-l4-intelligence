---
title: "知识轨 · 最终结论(全部干净证据 + Lean C1/C2/C4)—— omni agentic system 下多模态知识的表示/使用/TFRL"
date: 2026-07-07
stage: 1-argumentation + boundary-clean directional 实验 + Lean 理论(sorry-free)
status: "取代被泄漏污染的旧结论。所有经验证据 boundary-clean(audio 输入 + 无 gold 泄漏)。覆盖:4 个 semantic 集 + proto-agentic;full-agentic 记为离线不可行。directional;须 powered 复现。"
---

> **LOG** — Stage-1 过程记录（hypothesis-grade），非现行真源；现行结论以 [[Decision-Log]] 与 [[Per-Work-Status]] 为准。

# E6 最终结论(在"无数据泄露 + 输入不越界"前提下,论据充足)

> 前提兑现:所有经验证据都满足两条硬约束——输入=音频、KB/注入不含本题 gold(用答案擦除 / 反事实 A′ 两种干净手段各自把关)。全部 directional(n≤60/集)。

## 一、干净证据全景

| 实验(边界干净) | 关键数 | 读数 |
|---|---|---|
| **T8 答案擦除**(heysquad,audio-ASR query) | base 0.283 · scrub 0.217 · **clean_H0=−0.066 CI[−.17,.03] null** · lookup +0.516 | 去掉答案后外部知识**零推理增强**;表面 RAG 100% 是查答案 |
| **CF 反事实利用率**(SQuAD-zh/vocalbench-zh/big-bench-audio) | **CF_follow 均值 0.237**;SQuAD 上 keep-参数 0.70;base_says_A′≈0 | 冲突时**只 24% 采纳外部**——**参数固执**,难覆盖自身错误 |
| **T0 一致注入**(对照) | follow ~0.75 | 一致/填空时肯用 |
| **t10 proto-agentic**(SQuAD-zh,2 轮工具 vs 单轮) | single 0.175 → **two-turn-tool 0.35(+0.175,翻倍)** | **递送形式是杠杆**:agentic 工具式递送~倍增采纳 |
| **Lean(sorry-free,全库绿)** | `Realization`(C4:τ→0⇒oracle,realized≥oracle−2τ)+ `Iterate`(C1 单调有界收敛、C2 预算 N*≤(M−x₀)/δ、无约束发散) | TFRL 选择/迭代**收敛已机器证明** |

**覆盖(诚实):** semantic 4 集(heysquad/SQuAD-zh/vocalbench-zh/big-bench-audio)+ proto-agentic(2 轮工具);**full-agentic 基准(eva 模拟器 / tau2 DB-env / audiomc o4-mini rubric)离线不可行**,记为需基础设施的缺口(E4)。

## 二、三问结论

### Q1 多模态知识如何表示 / 组成(RAG? LLMWiki? 更新形态?)
- **存储结构层面(RAG vs LLMWiki vs KG):清白证据下 under-determined**——无干净"事实-gap + 外部 KB(不含答案)"测试床(OpenbookQA 饱和+无 fact-book;reading-comp=查答案);更富结构无从干净检验。RAG(flat text-passage)是**待超越基线**,但其"知识增强"价值未被清白证实。
- **但真正有清白信号的是"递送/交互形式"而非存储结构:** t10 表明**把知识作为 agentic 工具结果递送 > flat 预置**(采纳 0.175→0.35)。→ **表示的一阶答案:知识组织为可检索的显式文本事实,以 agentic 工具-调用交互递送**;LLMWiki/KG 的结构收益留待多跳 Stage-2(且需先建干净测试床)。

### Q2 如何使用(检索式加载?)
检索式加载 + 注入是机制,但清白证据下**受三重刻画**:(a) **不推理增强**(擦除后 null);(b) **参数固执**——冲突外部只 24% 采纳,难修参数错误;(c) **递送形式显著影响**——agentic 工具式递送使采纳翻倍。⇒ **使用之道 = agentic 工具-增强递送 + 信任校准**,不是 flat-RAG 预置;检索加载必要但远不充分。

### Q3 是否有 training-free RL 优化空间?方案长啥样?
**有,且是边界干净、有真实 headroom 的——但在正确的轴上:**
- **不在**:精度门控(R1,已证伪掉点)、推理增强(擦除 null)。
- **在**:**(i) 递送-形式选择**(t10:形式一换采纳翻倍 → reward-guided 选 {agentic-tool / flat / 格式} 有实测 headroom);**(ii) 信任/覆盖校准**(CF:外部证据强时提采纳、弱时保参数)。
- **收敛(已 Lean 证明):** 方案 = `audio query → 检索外部事实 → reward-guided 选择{递送形式, 是否覆盖参数, 何时检索} → 注入 → 冻结 omni 作答`;reward = **去相关证据强度**(omni-embed / 多源一致,非 gold)。承重约束 **τ(C4:realized≥oracle−2τ,τ→0⇒oracle)+ N* 预算(C2)+ 信赖域单调收敛(C1)**;无约束发散(负结果)。`proofs/tfrl` 的 `Realization.lean` + `Iterate.lean` 已 sorry-free 交付这套收敛骨架,双轨绑定 `decode.best_of_n`/接受门/`kl_best_of_n_bound(N)`。

## 三、一句话总纲(论据充足)
**严格无泄漏下:冻结 2026 omni 消费外部知识仅限"非冲突显式事实填空(≈查答案)"——不推理增强、且参数固执难覆盖自身错误;但"知识的*递送形式*"是清白、可训练无关优化的杠杆(agentic 工具式递送使采纳翻倍)。TFRL 的优化空间因此落在"递送-形式选择 + 信任校准"两轴(非精度门控/增强),其收敛已由 Lean(C1/C2/C4,sorry-free)证明。** 对"用 RAG 修参数错误"的硬限制(参数固执)是本轮最重要的负向机制发现,也精确指出下一步:reward-guided 信任校准 + 递送形式优化,在一个**须构造的事实-gap 干净测试床**上做 powered 验证。

## 四、幸存/作废/后置
- **幸存(清白):** Lean C1/C2/C4;调研/taxonomy;概念对齐;T8/CF/t10 清白实验。
- **作废(泄漏):** T7 的 R1/H0 正向主张(已挂横幅)。
- **后置(owner/Stage-2):** ① 构造事实-gap + 干净 KB 测试床(powered 验证增强与信任校准);② 递送-形式 & 信任-校准的 reward-guided 选择器(E5 清白目标)+ 其 τ/N* 实测;③ LLMWiki/GraphRAG 留多跳;④ full-agentic 需模拟器/verifiable-env 基础设施。
