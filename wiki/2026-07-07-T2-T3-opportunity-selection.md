---
title: "T2 综合 + T3 首个可测机会选定(知识轨)"
date: 2026-07-07
stage: 1-argumentation
status: "T2 = effect-map 成品(见 2026-07-07-tfrl-baseline-effect-map.md)。T3 = 自主选定(证据明确、非硬分叉;owner 可否决)。Owner review pending; wiki-sync deferred。"
---

# T2 综合 + T3 选定

## T2(WS-4 效果映射)—— 结论
成品在 [[2026-07-07-tfrl-baseline-effect-map.md]](8 个决策点 D1–D8 × 具名基线 × 训练无关 RL 杠杆 × 提升机制 × 代码归宿)。要点:
- **T0 已把目标重定向**到"利用效率"的两侧 headroom:(a) 采纳/门控(C<A)+ (b) 注入/利用(B≪1.0)。
- **相似原理已存在于文本域**(RTTC/AdaRewriter/TARG)→ **不追新机制**;贡献 = 在冻结 Qwen3-Omni 上抬升具名基线(effect-over-novelty)。
- **检索器是"要训练"的瓶颈,消费是训练无关容易的部分** → TFRL 预算投 D1/D2 利用侧,检索器用现成工具。
- 边界干净是**条件性**的:奖励须为 proxy/去相关/可验证,绝不读 gold;防 (a) gold 泄漏 + (b) 同模型自评去相关塌缩。

## T3 —— 首个可测机会(自主选定)

**选定:R1 = 奖励引导的采纳门控(D1)为首;R2 = 注入-格式/模态(D2)为紧随可叠加第二杠杆;R3(when-gate+query 改写)暂缓。**

**理由(为何 R1 先行):**
1. **前提被 T0 最稳信号确认.** C<A(错配注入拖累)在两集一致;比 B−A(big-bench +0.075,噪声)稳。R1 攻的正是"该拒的注入要拒"这块**已测**的 headroom。
2. **最便宜、可复用.** `W4 policies/accept_gate.py`(bootstrap-delta 门控)+ `rl/embedding_metrics.retrieval_reward`/`recall_at_k` + `rl/decode.plurality_gate`(margin 门)已存在。
3. **边界干净 + 去相关.** 奖励 = omni-embed 相关性/支持度——**omni-embed 是异于生成器 Qwen3-Omni 的模型**(verifier-as-tool、天然去相关),且非 gold。
4. **基线明确(要打败的):** (i) inject-top-k-always 地板(即 C<A 那个 regime);(ii) CRAG(2401.15884)——在**不训练 T5-large**的前提下追回其 evaluator 式路由增益。

**为何 R2 紧随:** 攻 B≪1.0("该用的没用上"),T0 finding-(b) 确认;与 R1 共用同一 retrieve→gate→inject→generate 回路(T6 一次搭好)。注意:其 modality 子杠杆(audio vs 自转写)的**幅度依赖模型代际**(perception-delta 在更强基座上可能缩小)。

**为何 R3 暂缓:** 其前提=omni 在**音频条件**下暴露**可校准、能区分"知识不确定 vs 感知不确定"的 logit-margin**——TARG 的证据是**前代、纯文本**,我们**未验**。若 margin 不可用,when-gate 塌成 always-retrieve;query-改写(D5)那半不依赖此前提,作为 R3 的稳健残余保留。

**owner 可否决点:** 若你更想先打"跨模态检索净新"或"语音特有的 D5 query 改写",告诉我即可换首发;默认按 R1→R2 推进。

## 下游(据此解锁)
- **T4 契约:** H0(外部知识 headroom,oracle-retrieval 上限)· **H-util-gate(R1:门控 vs inject-all 地板)** · H-util-fmt(R2)· 对照 provenance-firewall/answer-overlap/mismatch-placebo。
- **T6 build:** retrieve→**gate(R1)**→**inject-format(R2)**→冻结 Qwen3-Omni 生成 的最小回路(复用 rag_answer/accept_gate/embedding_metrics/decode)。
- **T5 Lean:** 把"采纳门控 + best-of-N 注入选择"形式化为选择过程,C1(KL 信赖域)/C2(N* 预算)收敛。
