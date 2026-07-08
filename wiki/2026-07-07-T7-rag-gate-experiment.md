---
title: "T7 — R1 门控 + H0 headroom 实验(heysquad RAG,冻结 Qwen3-Omni)"
date: 2026-07-07
stage: 1-directional
status: "Stage-1 directional (n=60, single-touch, paired-bootstrap CI). Boundary-clean. Owner review pending; wiki-sync deferred。"
---

# T7 实验结果 —— R1 门控 + H0 headroom

> 🚨 **作废/重大 caveat(2026-07-07,泄漏审计后):** 本实验**不边界干净**,结论**不可作正向证据**。审计(`scripts/t7_leakage_audit.py`)显示:**KB 逐条含各自 ground truth(answer_in_own_KB=1.0),注入 top-k 含答案率 0.90**——heysquad 是 SQuAD 阅读理解,答案本就是 context 里的片段。故 H0=+0.517 / inject_k=0.767 **几乎全是"注入文本含答案→模型抄"(查答案),非外部知识辅助推理**。另:检索 query 用了**问题文本**(部署时不可得,应用音频)。两处都违反边界。**被 [[2026-07-07-T8-clean-rag-rerun]](音频 query + 答案擦除)取代。** 保留原文仅作过程记录。

**Testbed(边界干净).** heysquad(SQuAD 型口语 QA):KB = 403 个 `context` passage(检索知识);query = 问题文本(隔离利用杠杆,避开 ASR 噪声);gold `answers` held-out 仅打分、绝不注入。检索器 = word-TFIDF(MiniLM 离线不可用降级;检索器非研究对象)。生成 = 冻结 Qwen3-Omni(Q8_0 GGUF)。脚本 `scripts/t7_rag_gate_probe.py` → `_repro/t7_rag_gate_probe.json`,seed 20260707。

## 结果(n=60)
| 臂 | 含义 | acc |
|---|---|---|
| base | 纯参数(不注入) | **0.283** |
| inject_k | 注入 top-5 检索 passage(全) | **0.767** |
| gate (R1) | 只采纳 sim≥0.9×max(均 1.4/5) | **0.633** |
| oracle | 注入本项 gold passage(H0 上限) | **0.800** |

检索 hit@5 = 0.90;gate 保住 gold 仅 0.733。

- **H0(oracle−base)= +0.517,CI[0.383, 0.65]**;base 答错的 43 项救回 **74.4%**。
- **H-util-gate(gate−inject_k)= −0.134,CI[−0.233, −0.05]**(CI 全 < 0)。

## 判读(诚实:一强正 + 一验证性负)
1. **H0 大幅确认(强正):** 冻结 Qwen3-Omni 有**巨大知识 gap**(base 0.283)且**极善消费检索来的外部知识**(inject_k 0.767 ≈ oracle 0.80)。RAG 把地板抬了 +0.517。这在 scale 上确认并强化了 T0 的"消费通道开着"。
2. **R1 精度门控被证伪(验证性负):** 激进采纳门控**掉点**(0.767→0.633),因为 **(i) 模型对干扰 passage 鲁棒**(inject-all 已≈oracle,不需要滤)、**(ii) 门控牺牲召回**(丢掉 gold 27%)。→ **"滤干扰"不是这个强模型上的有效杠杆;约束是召回而非精度。**
3. **与 T0 的 C<A 不矛盾:** 单独喂错事实 hurts(T0-C);但对的 passage 在场时,附带干扰无害(强模型能挑出信号)。

## 对 thesis 的影响(喂 T8 螺旋)
- **知识轨的核心正向主张成立:** 冻结 omni + 外挂 passage-RAG 能大幅提升知识含量,且模型消费稳健。
- **利用杠杆需再次重定向:** R1(精度门控)出局;剩余的 training-free 利用空间在 **(a) 效率**(何时/多少检索——base 已对 0.283 项无需检索)、**(b) 更受压的 regime**(ASR-噪声 query、多跳)、**(c) 召回保持型选择**,而非"滤干扰"。在**干净检索 + 强模型**下,plain RAG 已近饱和 headroom(inject_k 0.767 vs oracle 0.80),留给"利用优化"的**准确率**空间小——TFRL 价值更可能在**效率/受压 regime**。

## 边界与分级
- n=60、单触点、directional;paired-bootstrap CI 已给但 Stage-1 grade。
- 边界干净:query=问题文本(非答案)、答案 held-out 不注入、库=passage 池、门控奖励=检索相关性(proxy、非 gold、异于生成器的模型=去相关)。
- caveat:检索器是 TF-IDF(弱);MiniLM 可用时相关性分更准,门控可能不同——但"模型对干扰鲁棒 + 召回是瓶颈"这一结论不依赖检索器强弱。
