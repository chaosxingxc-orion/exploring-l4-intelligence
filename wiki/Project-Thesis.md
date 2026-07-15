# Project Thesis

The single, canonical statement of what this series is for. Read right after
[[Research-Objective]] (the hot current-state entry).

## Thesis (north star)

A modern omni / multimodal LLM has already absorbed broad, **cross-modal, multi-granularity task
knowledge** during pretraining. This series asks one question:

> **How far can _training-free RL_ — reward-guided control that changes none of the core model's
> weights or internal architecture — go to _activate_ that latent knowledge and lift a frozen,
> black-box omni model's performance on speech / audio tasks?**

**Program statement (owner rulings 2026-07-14/15, Decision-Log 续45/46; formal Gate S0 signature
pending — [[2026-07-15-s0-program-identity-signoff]]).** The object we build and study is an
**external reward-guided control plane** (an agentic system) around the frozen black-box core:
observation/supply building, state & external memory, tool/retrieval use, candidate generation,
evaluation, selection, budget/risk/stopping, provenance & information-boundary guarding.
**Training-free RL is the north-star principle pulling this system's design** — reward/advantage
decides the *next action*; in-pool selection is its degenerate special case. The **first innovation
hypothesis is the system itself** (the founding UMBRELLA identity, 2026-06-26): occupancy against
ReAct / Reflexion / LATS / IAD / MM-ReAct / AudioToolAgent-class prior work is under survey — **no
"first-ever" claims** before that check closes.

- **Black-box contract**: core methods may not require weights, gradients, hidden states, attention,
  or guaranteed logprobs. The local llama.cpp deployment is a low-cost verification environment —
  gray-box diagnostics only, never load-bearing.
- **North-star metric family**: headroom / realization accounting — H(c) and the ρ family
  (pool-level, generalizing to trajectory-level). **The metric pulls the design; the metric is not
  the research object** (the 2026-07 inversion lesson — see tombstones).
- **Resource posture**: reach the ceiling first (no budget cap; budget logged), then consolidate,
  then cost-reduce. Equal-budget comparisons are `PHASE-3_TOOL`s, not phase-1 gates.

## Three terms (defined once, used everywhere)

- **Training-free RL** — reward-guided, gradient-free control at inference time over a frozen core
  (sequential control; best-of-N / reranking / MBR as special cases). External control-plane
  structure is explicitly designed and versioned; the core's weights and architecture stay untouched.
- **Activation of pretrained knowledge** — eliciting capabilities the base model already holds but
  does not surface out-of-the-box; measured as realized headroom under verifiable rewards.
- **External control plane（外部控制平面）** — the agent scaffold around the frozen core (supply,
  memory, tools, evaluation, selection, budget, stopping); the registered plain name for what was
  colloquially「外设优化」.

## How the four works relate

| # | Work (repo) | Role |
|---|---|---|
| **W1** | `speech-mllm-training-free-rl` | **Primary-program carrier** — external control plane over a frozen black-box omni core; the mature selector/evaluator line continues as its component dossier |
| W4 | `speech-mllm-omni-embedding-rl` | Separate work — L0/L1 embedding-utility studies (fresh proposal pending #29) |
| W2 | `speech-mllm-efficient-rl-alignment` | Supporting — efficient GRPO/DPO (LoRA) speech↔language alignment |
| W3 | `speech-mllm-multitask-rl` | Supporting — one policy, RL across ASR/ST/SID/SER via verifiable rewards |

## Supersession

This 2026-07-15 restatement **supersedes** the 2026-07-12 note (selector-first primary study,
"primary metric = ρ") and the earlier W4-flagship framing, per owner rulings in Decision-Log
续45/46; canonical force is formalized by the Gate S0 signature. Prior full text: git history
(`git show e482465:wiki/Project-Thesis.md`); dead terms & incident history:
`wiki/archive/terminology-tombstones.md`. The W4 "speech disentanglement" flagship claim remains
dead (L2–L3 criteria unmet).

---

## 中文

本系列唯一权威目的陈述。紧随 [[Research-Objective]]（热层现状入口）之后读。

### 主旨（北极星）

现代 omni / 多模态大模型在预训练中已吸收**跨模态、多粒度的任务知识**。本系列只问一个问题：

> **仅靠「免训练 RL」——不改核心模型权重与内部结构、由奖励引导的控制——能在多大程度上「激活」
> 这些潜藏知识，提升一个冻结黑盒 omni 模型在语音任务上的表现？**

**纲领表述（owner 裁决 2026-07-14/15，续45/46；Gate S0 签署待办）**：我们构建并研究的对象是围绕
冻结黑盒核心的**外部 reward-guided 控制平面**（agentic system）：观察/供给构造、状态与外部记忆、
工具/检索、候选生成、评估、选择、预算/风险/停止、溯源与信息边界守卫。**免训练 RL 是牵引该系统
设计的北极星原则**——reward/advantage 决定下一步动作，池内选择是退化特例。**第一创新假设 =
系统本身**（立项即有的 UMBRELLA 身份）：对 ReAct/Reflexion/LATS/IAD/MM-ReAct/AudioToolAgent 类
先行工作的占据核查未完成前，**不得宣称任何「首个」**。

- **黑盒合同**：核心方法不得要求 weights/gradients/hidden states/attention/保证 logprobs；
  本地 llama.cpp = 低成本校验环节（灰盒诊断，永不承重）。
- **北极星指标族**：头空/兑现率记账——H(c) 与 ρ 族（池级→轨迹级）。**指标牵引设计，指标不是
  研究对象**（2026-07 指标倒置教训）。
- **资源姿态**：全力摸高（预算不设 cap、照实记录）→ 持续整合 → 成本压降；等预算对照 =
  `PHASE-3_TOOL`。

### 取代说明

本 2026-07-15 版取代 2026-07-12 取代说明（selector-first primary、「primary 指标 = ρ」）与更早的
W4 旗舰框架（据续45/46；S0 签署使效力正式化）。旧全文在 git 历史
（`git show e482465:wiki/Project-Thesis.md`）；死名词与事故史在
`wiki/archive/terminology-tombstones.md`。W4「语音解耦」旗舰主张维持废止（L2–L3 判据未过）。
