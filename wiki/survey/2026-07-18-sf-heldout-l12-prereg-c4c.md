---
artifact_id: "SF-HELDOUT-L12-PREREG-C4C-2026-07-18-01"
title: "fresh L12 held-out 预注册（P0-R9 MAJOR-G1 整改项 4）"
date: 2026-07-18
discipline: "隔离代理（Opus,零设计上下文,未接触任何协议查询词项/修订 diff）按研究方向描述独立选取 5 候选;本件在 matcher 运行前提交入 git（预注册时点 = 本件提交哈希）;matcher 运行后全部 5 候选的完整命中结果如实追加,不得静默丢弃未命中者;验收 = ≥1 候选实际命中 L12 lane 查询（SF-L12-Q1/Q2/Q3,吸取 C4B 教训:2602.21497 只被旧 L3 lane 救走却被写成「L12 侧」——本次 L12 命中为硬验收）"
era_constraint: "v1 ≥ 2025-01-01（owner 时代裁决,机器强制）"
agent_attestation: "未接触任何协议查询词项；仅用 export.arxiv.org；v1日期均已逐ID核验"
access_class: "HELD_OUT_SENTINEL_SOURCING（15 次检索/解引用 URL 由代理如实回报,登记入 c4c 访问台账）"
---

# fresh L12 held-out 预注册（C4C）

隔离代理交付的 5 候选（逐字登记,选取理由 = 代理原文）：

| # | arXiv ID | 题名 | v1 | 类别 | 代理选取理由（一句） |
|---|---|---|---|---|---|
| 1 | 2510.21794 | Token-Level Inference-Time Alignment for Vision-Language Models | 2025-10-20 | cs.CV, cs.AI | Training-free, fine-tuning-free inference-time decoding steering that aligns a frozen VLM's token distribution to reduce hallucination — the guided-decoding branch of external control. |
| 2 | 2506.08691 | VReST: Enhancing Reasoning in Large Vision-Language Models through Tree Search and Self-Reward Mechanism | 2025-06-10 | cs.CV | Explicitly training-free tree-search over candidate reasoning paths with a self-reward signal selecting among them on a frozen LVLM — reward-guided candidate sampling-and-selection. |
| 3 | 2603.16253 | Grounding the Score: Explicit Visual Premise Verification for Reliable Vision-Language Process Reward Models | 2026-03-17 | cs.CV, cs.AI | Verifier/process-reward-model that reranks generator candidates under test-time scaling, grounding step scores in visual-premise verification — the verification-as-selector branch. |
| 4 | 2606.03054 | ToolGate: Token-Efficient Pre-Call Control for Tool-Augmented Vision-Language Agents | 2026-06-02 | cs.AI | External pre-call gating/orchestration layer deciding whether a ReAct-style frozen VLM agent should execute each proposed tool call — the tool-calling/budget control-plane branch. |
| 5 | 2603.24257 | Memory-Augmented Vision-Language Agents for Persistent and Semantically Consistent Object Captioning | 2026-03-25 | cs.CV | External persistent memory around a VLM agent enforcing cross-viewpoint semantic consistency without retraining — the memory/state branch of the external scaffold. |

**预注册预测**：不作方向性预测（该由 matcher 裁决）;验收判据如 frontmatter。
**matcher 运行前状态**：本件提交时,5 候选的官方 Atom 元数据尚未送入任何 matcher。
