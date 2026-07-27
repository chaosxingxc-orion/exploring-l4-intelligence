---
proposal_id: "R2"
title: "音频原生外部知识获取与检索调度"
dimension: "D1 multimodal knowledge"
status: "workbench proposal; owner review pending"
execution_authority: "WITHHELD"
---

# R2 — 音频原生外部知识获取与检索调度

## Proposal 摘要

本研究只处理“答案所需事实不在 waveform 内”的任务：控制器先从音频建立可审计 query state，再决定
是否检索、查什么、购买多少 hop、接纳哪条外部证据以及何时停止。它把 endogenous audio evidence 与
exogenous corpus/web evidence 分开记账，并用冻结检索快照消除 live-search 漂移，使能力增益能够归因到
检索决策，而不是搜索结果随时间变化。

R2 是条件启用方向：若任务不需要外部事实，检索不是默认动作。其价值必须超过 direct、structured
prompt 和固定检索链；否则不应以“agent 更复杂”为理由保留。

## 1. 研究问题与假设

- `H1 need detection`：部署可见信号可以区分“音频内部可答”与“需要外部事实”的实例，并以可用 precision
  避免无效检索。
- `H2 scheduling`：reward/VoI-guided query-hop-stop policy 在同 retrieval budget 下超过 fixed-k/fixed-hop。
- `H3 grounding`：显式区分 audio-derived claim 与 external claim 能减少检索内容覆盖原音证据造成的错误。
- `H4 attribution`：在 pinned snapshot 下，可把增益分解为 audio grounding、query、retrieval admission、
  reasoning 和 stop；若无法分解，则只允许报告系统级结果。

## 2. 最近工作与 donor 边界

| 证据 | 已有能力 | 开放台阶 |
|---|---|---|
| `SPEECH_NEAREST_PRIOR` AudioRAG (2602.10656) | 500 个 audio+retrieval 多跳问题；text controller 调 omni audio tool 和 web explorer | free-form 调度，无显式成本/VoI/stop；gold audio attribute 参与数据过滤，不可进入部署评分 |
| `SPEECH_NEAREST_PRIOR` Omni-DeepSearch (2605.08762) | audio-initiated 深搜索与完整轨迹 | 额外搜索可丢失已找到的正确证据；budget 非单调 |
| `SPEECH_NEAREST_PRIOR` VoiceAgentRAG (2603.02206) | 异步预取与延迟隐藏 | 主要是文本 RAG、缺答案质量轴；只能借 latency harness |
| `CROSS_DOMAIN_METHOD_DONOR` WebThinker | planner/explorer、取证摘要与多跳搜索合同 | 其文本效果不证明音频 query grounding |
| `CROSS_DOMAIN_METHOD_DONOR` ToolGate、Calibrate-Then-Act、VOI-search | 调用前门控、cost-aware exploration、硬双预算 | 离散文本 action 需重写为 audio-grounded query/action |

## 3. 方法设计

### 3.1 Two-ledger evidence state

每条 evidence 标记：`source={audio, external}`、audio time span、query、retrieval snapshot ID、document
hash、claim、support/contradict relation、cost 和 admission score。最终答案必须能回指“哪些 claim 来自原音、
哪些来自外部事实”。文本检索结果不能改写 raw-audio observation。

### 3.2 Action menu

```text
keep_direct
form_audio_grounded_query
retrieve_one_hop
refine_query
verify_against_audio
admit_or_reject_document
regenerate_answer
stop
```

第一版使用离线冻结 corpus/snapshot。每轮最多新增一个 hop；只有 estimated improvement 减去 retrieval
cost 为正且 margin 超过门槛时继续。Anticipatory prefetch 作为后期动作，只在真实交互延迟能被隐藏、并且
prefetch hit 对 task answer 有净贡献时启用。

### 3.3 Reward decomposition

Reward 不直接等于“搜索到了很多文档”。至少分成：query groundedness、evidence relevance、claim
support、answer consistency、contradiction、terminal utility proxy 和 cost。检索量、文档长度或 judge
verbosity 不能作为能力 reward。

## 4. 实验设计

### 4.1 Carrier 与切分

首选 AudioRAG-500，因为它显式需要 audio reasoning + information retrieval；第二载体是
Omni-DeepSearch 的可冻结子集。将题目按 `waveform-sufficient / external-fact-required / ambiguous` 分层，
分层标签仅用于离线评测，不能进入 controller。Live web 只做最后外部有效性，不用于主可复现结论。

### 4.2 Arms

`direct`、`structured prompt`、`always retrieve fixed-k`、`fixed-hop WebThinker/AudioRAG-style`、
`random matched-hop`、`need-gate only`、`adaptive query-hop-stop`、`oracle need/hop`。所有检索臂共享完全
相同的 snapshot、index、retriever 和 document cap。

### 4.3 指标

Primary：task accuracy/utility 的 paired delta 与 LCB。机制指标：need-detection precision/recall、
query success、retrieval recall、evidence admission precision、正确证据到达轮次、正确后继续搜索导致的
regression、type-D/loop failure、hop/call/bytes/latency/cost。分别报告 waveform-sufficient 桶的伤害和
external-required 桶的收益。

### 4.4 Ablations

- 去掉 audio span grounding；
- live vs pinned snapshot 只做漂移诊断；
- fixed stop vs marginal-VoI stop；
- retrieval admission 开/关；
- raw audio final re-grounding 开/关；
- prefetch 的 latency-only、quality-only 和 joint 结果。

## 5. Lean 与数学建议

形式化两个不同信息集合 `I_audio ⊆ I_t` 与 `I_external,t`，以及有限检索预算。证明：每个 document 带
snapshot/provenance；每步消耗预算；stop 后不再改变 state；gold 不属于任一 runtime information set。

定义 hop 的净值：

```text
Δ_t = E[U(y_{t+1}) - U(y_t) | visible trace] - λ_search C_t - λ_drift D_t
```

继续规则必须由可估量下界而非真实 `U` 决定。可进一步采用 anytime-valid confidence sequence 约束
重复检查造成的选择偏差；但在语音域成立前只称 donor-adapted statistical design。

## 6. 击杀与重路由

- waveform-sufficient 桶若无收益或受损，need gate 必须学会 no-retrieval；否则击杀默认检索。
- pinned retrieval 在 matched budget 下不超过 direct/structured/fixed-hop，移除该 carrier 或击杀自适应调度。
- live 数字无法由 snapshot 重现，只可报告 drift case study，不作 capability headline。
- 若 query 主要由 transcript 生成且丢失关键非言语线索，必须增加 audio re-grounding；仍失败则限定到 lexical
  speech tasks。
- 若外部事实可靠性无法审计，R2 不进入 R9 集成。

## 7. 执行路线与预期贡献

先冻结 snapshot，做 `direct vs fixed-hop vs need-gated one-hop`；只有 one-hop 有净能力收益后才增加
multi-hop、query rewrite 和 anticipatory prefetch。预期产出是一个 audio-grounded retrieval decision
contract、一套把检索收益与信息漂移分开的评测，以及在证据成立时的 cost-aware stop policy。

## 8. Provenance

语音机制与失败分类来自 D1/D4 dossiers 和 T1/T2；检索/预算 donor 来自 D6。所有跨域方法只支撑设计
可行性，R2 的 speech 效果是待检验的 `OUR_HYPOTHESIS`。
