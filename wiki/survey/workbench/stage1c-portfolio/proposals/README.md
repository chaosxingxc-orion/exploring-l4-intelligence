---
artifact_id: "SF-STAGE1C-CAPABILITY-PROPOSALS-V1"
role: "workbench research-proposal portfolio; owner review pending"
authority: "derived from CURRENT research-directions contract; no execution authority"
stage: "STAGE_1C_PROPOSAL_DRAFT"
execution_authority: "STAGE2A_WITHHELD"
---

# 九项候选能力激活研究开题报告

## 1. Portfolio 结论

本目录把 CURRENT 的原九条候选方向逐项扩写为以问题定义、文献占位、数据集和实验承载为中心的开题报告。
共同研究对象不是模型参数，
而是围绕冻结 speech/omni 推理 API 的外部控制平面：系统通过构造、选择和更新 in-context
状态，决定观察什么、保留什么经验、调用什么技能、谁拥有作答权，以及 reward 如何改变下一步动作。

R1 已由 owner 裁决在 Stage-2 前日落（2026-07-29 确认，Decision-Log 续76）；R2 分析为执行者草稿
（owner 未校验），其日落/重路由建议已撤回为草稿意见，待按 2026-07-29 方向成立判据与 owner 协同
重审；R3-R9 同为 owner 未校验的旧版 proposal。九篇文档是九个候选的审计记录，不是九个必须启动的
独立项目。
当前保留路线及可选 evidence carrier 为：

```text
R5 evidence-state architecture
  └─ R6 within-instance reward control
       └─ R8 reliable capability control
            ├─ R4 runtime skill lifecycle
            ├─ R3 acoustic-keyed memory ── R7 cross-instance evolution
            └─ optional published external-knowledge carrier (only when facts are absent from audio)
                         └─ R9 integrated system
```

第一执行候选仍是 `R5 + R6 + R8` 的最小纵向切片；其余 proposal 提供扩展研究问题、可证伪实验和
重路由条件，不改变 CURRENT 的 Stage-2A 执行仍待授权状态。

## 2. Proposal 索引

| ID | Proposal | 主维度 | 直接语音证据 | 跨域 donor 的角色 | 建议批次 |
|---|---|---|---|---|---|
| R1 | [语音/音频上下文学习方法复现与比较](R1-adaptive-evidence-supply.md) | D1 知识 | 八篇直接/近邻论文；只复用论文数据、基线和指标 | 已发表方法按需路由至 R3–R8 | **Owner 确认（2026-07-29）：Stage-1C 日落，不进入 Stage-2** |
| R2 | [音频驱动外部知识检索的文献归纳与方向处置](R2-audio-native-knowledge-acquisition.md) | D1 知识 | AudioRAG、Omni-DeepSearch、VoiceAgentRAG | 不再借 donor 发明独立调度器；证据路由至 R3/R5/R6/R7/R8/R9 | **执行者草稿，owner 未校验；按 07-29 判据属 (a) 型，待协同重审** |
| R3 | [声学条件键控的持久多模态记忆](R3-acoustic-keyed-memory.md) | D2 记忆 | AOP-Agent、audio uncertainty；直接跨实例语音工作薄 | 借 M2Note、MemRL、PhysMem、MemCollab 的 schema/门控 | Stage-2C |
| R4 | [运行时多模态技能的信用、组合与生命周期](R4-runtime-skill-lifecycle.md) | D3 技能 | Speech-Copilot、Audio-Maestro、AuTAgent | 借 Trace2Skill、PANDO 的归纳/退役协议 | Stage-2B |
| R5 | [Incumbent-preserving 证据状态智能体架构](R5-evidence-state-agent-architecture.md) | D4 系统 | Audio-Mind、Agent-Omni、AudioToolAgent、ARC agents | 借 WebThinker 的取证合同 | Stage-2A |
| R6 | [实例内 reward-guided context 与轨迹控制](R6-within-instance-reward-control.md) | D5 进化 | speech 中主要是 select-only 或手工循环 | 借 JitRL、ETS、ATLAS、Training-Free GRPO 的控制机制 | Stage-2A |
| R7 | [跨实例经验驱动的无权重系统进化](R7-cross-instance-system-evolution.md) | D5 进化 | 当前读集内直接 speech 占据不足 | 借 MemRL、JitRL、bandit/prequential 协议 | Stage-2C |
| R8 | [条件自适应的可靠能力控制](R8-reliable-capability-control.md) | D5 横切 | AudioProcessBench、AudioJudge、SpeakerSleuth、Omni-RRM | 借 Best-of-Poisson/HedgeTune、CITE 等校准与压力协议 | Stage-2A |
| R9 | [五维集成的可靠能力激活系统](R9-integrated-capability-activation-system.md) | 集成 | Audio-Mind、Agent-Omni、Omni-DeepSearch、ARC agents | 只借组合归因与长期评测协议 | Stage-2E |

统一的 API-only、gold fence、基线、统计、成本、可靠性和 Lean 分工见
[共享实验与形式化协议](shared-experiment-and-formal-protocol.md)。单篇 proposal 只在此基础上增加自己的
变量、基线和击杀条件。

## 3. 如何理解“参考视觉/文本工作”

当语音侧没有直接工作时，本 portfolio 采用三级证据标签：

1. `SPEECH_NEAREST_PRIOR`：可支持语音域的机制、失败模式或基线设计；仍不自动支持本 proposal 的效果。
2. `CROSS_DOMAIN_METHOD_DONOR`：只借状态表示、算法、协议、统计量或形式化假设；效果不得跨模态外推。
3. `OUR_HYPOTHESIS`：从项目约束与 donor 结构推出的待检验设计，必须通过语音实验决定去留。

因此，“视觉/文本方法在其领域有效”在这里最多说明方案可实现、变量可测或对照可构造，不说明它会在
speech/omni 模型上提高能力。H5 仍为 `WITHHOLD_NON_LOAD_BEARING`。

## 4. Review 与执行边界

R1 日落裁决已经 owner 确认（2026-07-29，Decision-Log 续76）；R2 no-go/merge 建议已撤回为执行者
草稿意见；R2–R9 均为 owner 未校验（`OWNER_UNVERIFIED`）的 workbench proposal，须按 2026-07-29
方向成立判据与 owner 协同重审后才能定处置。它们可以用于
方向评审、Stage-2 合同收敛和实验准备清单，
但不授权模型/API 调用、数据下载、metrics、reproduction、prototype、技术 novelty verdict、push 或 wiki
publication。任何执行都要先把 proposal 中仍标为 `TBD_AT_AUTHORIZATION` 的模型、数据、prompt、预算、
SESOI、阈值和 hash 冻结成独立 Stage-2 合同。

## 5. 重审通道（2026-07-29 起）

- 重审模板：[`2026-07-29-direction-review-template.md`](2026-07-29-direction-review-template.md)
  （owner 未签草案，经 R2 首例校准后定稿）
- R2 协同重审底稿：[`2026-07-29-r2-coreview-draft.md`](2026-07-29-r2-coreview-draft.md)
  （owner 未签；裁定点=独立方向 vs 并入 R6/R8）

## 6. 证据路由

- 有效方向合同：`wiki/survey/current/research-directions.md`
- 五维语音证据：`2026-07-26-d1-knowledge-dossier-draft.md` 至
  `2026-07-26-d5-tfrl-dossier-draft.md`
- 视觉/文本 donor：`2026-07-26-d6-donor-lane-dossier-draft.md`
- 统一设计菜单：`2026-07-27-five-dimension-taxonomy-and-experiment-plan-draft.md`
- 数据/模型/评估器 readiness：`2026-07-26-t2-datasets.jsonl`、
  `2026-07-26-t3-models-evaluators.jsonl`
- 形式化模块：`proofs/tfrl/TfrlProofs/`
