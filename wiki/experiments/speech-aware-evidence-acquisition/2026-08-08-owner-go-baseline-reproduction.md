---
title: "Owner GO: sampled baseline-reproduction execution (R0.1 plan P1/P2 entry)"
date: 2026-08-08
authority: "owner session directive (Claude Code /goal, 2026-08-08): «完成规划好的实验和工作，完成数据集采样和相关工作基线的复现，模型采用Qwen3-omni，如果有涉及到知识或者向量化的，可以考虑用本地的生成式embedding模型 | 多轮自检下，程序无误，工程可复现»"
scope: "study speech-aware-evidence-acquisition, Stage-2A"
---

# Owner GO — sampled baseline reproduction (2026-08-08)

依据 owner 会话指令（上引 YAML `authority` 原文），本记录落地以下决定：

1. **采纳** study 仓 `docs/readiness/2026-08-07-r1-replan-reproduction-plan.md`
   （P0–P4，含四构造抽象框架、sample-once manifest 政策、T 系列类比轨道）
   作为 R1 re-plan 的执行形态（HANDOVER 选项 2+3 复合）。采样已按
   sample-once 政策冻结（manifest 锚 `c5130274…`）。
2. **执行序列**：首次模型触达 = `SAEA-E-001-r0-smoke`（R0 runbook 既定
   smoke，bare-core，e22 dev subset10）；随后按 P2 顺序在可见载体上执行
   （R4 三臂优先，其样本即冻结 dev subset10）。每次触达仍须各自的
   `ExecutionPlan` + exposure 预登记行 + fail-closed 闸门——本记录不豁免
   任何机器强制。
3. **模型选型**：冻结核 = Qwen3-Omni（lock 键
   `qwen3-omni-30b-a3b-instruct-gguf`，llama.cpp receipt-pinned 运行时）。
   涉及知识构建/向量化的组件（T1/T2 检索等）允许使用**本地生成式
   embedding 模型**作为 pinned 工具级组件（入日志、带哈希、无答案权），
   与确定性检索器（BM25）同等地位；最终答案权始终在冻结核。
4. **已知边界**：D/F 族载体（audio2tool、voiceagentbench、big-bench-audio
   等）尚无 `speech-aware-*` lock profile，gate 不可见——P1/R2/R5 的真实
   触达在 lock 修正案（伞仓正式路径）落地前不执行；工程脚手架先行。
   该修正案需单独的 owner 数据身份决定，不由本记录隐式授予。
5. **自检纪律**：dry-run 验证一律使用 `-dryrun` 后缀的独立 run-id 命名空间
   （真实 run-id 的 attempts 计量绝不被验证消耗）；每次真跑前 dry-run must
   pass；工程可复现性以 manifest/收据/固定种子为准绳。

记录人：implementer（Claude），受 owner 直接指令；审计链接：study 仓
`docs/readiness/` 全套 + `docs/exposure-ledger.md` 对应行。
