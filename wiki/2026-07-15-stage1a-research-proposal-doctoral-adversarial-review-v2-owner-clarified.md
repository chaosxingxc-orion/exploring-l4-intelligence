---
title: "Stage-1A 研究提案博导级对抗审查 v2——按 owner 澄清重置为黑盒 Omni Agentic System × Training-Free RL"
date: 2026-07-15
review_object: "wiki/2026-07-15-stage1a-research-proposal-for-reviewer.md"
supersedes: "wiki/2026-07-15-stage1a-research-proposal-doctoral-adversarial-review.md 的科学对象排序；其文献遗漏、工程基座、历史暴露、阶段边界与 QRP 事实裁决继续有效"
owner_clarification: "第一创新假设=构建 omni agentic system；training-free RL=牵引该系统构建的北极星；基础 omni 模型按黑盒处理，只通过外部系统优化"
review_role: "严格外审 / 博导预答辩；owner 澄清后的独立重评"
stage_standard: "Stage-1A 只允许问题定义、survey、架构与协议设计、synthetic/mock 验证；任何真实数据或真实模型执行均属 Stage-1B"
decision: "RETURN_FOR_MAJOR_REVISION — 当前 proposal 的主问题错位；不签 round-2 现行设计，不放行 Stage-1B"
source_edit_policy: "仅新增本日期 v2 审查件；未修改研究团队 proposal、协议、代码、台账、状态文件或并发工作"
fraud_assessment: "FFP NOT ESTABLISHED；v1 已确认的重大记录范围失实与 QRP 风险继续有效"
---

# Stage-1A 研究提案博导级对抗审查 v2

## 0. 修订后的总裁决

owner 的最新澄清改变了评审的科学中心：项目不是以“设计一个更好的固定池 selector”为第一创新，而是以**构建一个面向冻结黑盒 omni foundation model 的 agentic system**为第一创新假设；training-free RL 不是池内重排的别名，而是驱动这个外部系统如何观察、评估、调用工具、组织记忆、分配预算并选择下一步动作的北极星控制原则。

因此，本评审撤回 v1 中“UMBRELLA 应只是与 selector 主线分开的可选平行项目”这一排序判断，改判为：

> **UMBRELLA/系统级对象应升为主研究纲领；I1–I4、evaluator、selector、headroom 与 Goodhart 退居为该系统的组件、基线、诊断量和安全问题。**

但这不会使当前 proposal 获得签署。相反，它暴露了更基础的错位：现行 proposal、`Project-Thesis.md` 与 `Research-Objective.md` 仍把 `label-free selector × ρ(c)` 写成 primary research object，把 UMBRELLA 列为第五候选。也就是说，当前 proposal 详细回答了一个**次级组件问题**，却尚未正式定义 owner 真正要研究的主系统。

本轮结论仍为 `RETURN_FOR_MAJOR_REVISION`：

- 不签署当前以 selector saturation 为中心的 round-2 search design；
- 不放行 Stage-1B；
- 要求先在 Stage-1A 新建一份 system-first proposal，并对 black-box、training-free、RL、omni、agentic 五个词分别给出可执行合同和 kill test；
- 系统创新只是 owner 选择的**创新假设**，不是已经成立的贡献。若现有多模态 agent/scaffolding 工作已占据，必须降级或锐化，不能以“我们把组件组合起来了”自动声明创新。

## 1. v1 评审意见如何调整

| v1 意见 | v2 处置 | 新解释 |
|---|---|---|
| selector 不足以支撑 training-free RL headline | **保留** | selector 是局部决策动作，不是完整 agentic control |
| evaluator 与 selector 必须拆开 | **保留并升格** | 还要再增加 controller/policy、state、feedback、tool/action、stopping 层 |
| UMBRELLA 应与 fixed-pool selector 分开 | **修改排序** | 算子仍须分开，但 UMBRELLA 现在是主纲领，selector 是其子模块/基线 |
| I1–I4 是 Stage-1C 竞争身份 | **撤回为主问题候选** | 改作系统内四类 supporting questions，不再与主系统身份等权竞争 |
| I4 测量学可能是最值得保留的方向 | **降为系统诊断贡献** | 可测 external controller 何时有效，但不能取代系统与控制方法本体 |
| Proposal A/C 可作主线，agentic loop 另立项 | **撤回该优先级** | system-first 为主；测量、Goodhart 与 audio-grounded evaluator 为支撑工作包 |
| 工程必须配置化 | **保留并加严** | 配置对象从 dataset/model/selector 扩展为 agent graph/state/action/reward/tool/memory/budget |
| Stage-1A 零真实实验 | **完全保留** | 当前先重写研究合同和 survey，不得用实验结果反向定义 system |
| “GPU 至今零运行”与历史工件冲突 | **完全保留** | 应改为“本 proposal 新执行为零；历史暴露广泛存在” |
| FFP 未建立、重大 QRP 已建立 | **完全保留** | owner 的科学澄清不改变事实记录裁决 |

## 2. 建议冻结的新研究对象

### 2.1 一句话对象

> **在严格黑盒、基础模型权重与内部结构不变、总交互预算固定的条件下，能否通过一个外部 reward-guided sequential control plane，把冻结 omni foundation model 组织成真正能感知多模态环境、维护状态、调用工具、利用反馈并选择下一步动作的 agentic system，并在等预算下取得超越 one-shot prompting、BoN/MBR reranking 与普通无奖励 agent workflow 的增量？**

这句话包含五个必须分别证成的谓词：`black-box`、`training-free`、`reward-guided/RL`、`omni`、`agentic`。任何一个谓词失败，都必须降名，不能用其余四个替代。

其中，black-box 是为了跨模型/API 可迁移性、部署现实和核心不可修改而选定的**额外设计约束**，不是 training-free 的逻辑推论：不训练权重的方法仍可能读取 logits 或 hidden states。团队口语中的“外设优化”在论文中建议统一写成 `external control plane / external agent scaffold`，避免被理解为硬件外设。

### 2.2 系统分层

```text
真实环境 / 多模态观测
        ↓
外部 Agentic Control Plane
  ├─ observation/supply builder
  ├─ state + episodic/external memory
  ├─ tool/retrieval registry
  ├─ candidate action/trajectory generator
  ├─ evaluator/verifier/reward estimator
  ├─ selection rule / planner / controller
  ├─ budget + risk + stopping/abstention
  └─ provenance + information-boundary guard
        ↕ 仅经冻结接口
黑盒 Omni Foundation Model Mθ
        ↓
外部动作 / 工具执行 / 新观测 / reward or feedback
        ↺
```

其中：

- generator 产生候选动作或轨迹；
- evaluator/scorer/verifier 评价候选或执行结果；
- selector/reranker 在当前候选中做局部选择；
- controller/policy 决定下一步是观察、检索、调用工具、采样、评价、选择、修订、弃权还是停止；
- agentic system 是整个反馈闭环。

固定 K 池 selector 可以出现在环内，但它不能代表整个系统。

## 3. 五份必须新增的身份合同

### 3.1 Black-box contract

**推荐最小允许接口**：

```text
generate(multimodal_context, tool_schema, sampling_controls)
    -> text | structured_message | tool_call | multimodal_output
```

核心方法不得要求：

- gradients、weights、hidden states、attention；
- 修改 tokenizer、adapter、LoRA 或模型内部结构；
- 保证可得的 full logits / token-level logprobs；
- 仅本地 llama.cpp 白盒诊断才有的私有接口。

当前 P-γ 的 echo-logprob / same-core likelihood 可以保留为**灰盒诊断 comparator**，但若它是主控制器必要输入，就违反严格 black-box headline。若团队坚持 logprob 是允许接口，必须把目标降为 `API-accessible gray-box`，不得继续声称最小黑盒可迁移性。

**kill-black-box**：关闭 logprob/内部信号后核心增量消失。

### 3.2 Training-free contract

这里有一个当前文档尚未解决的关键歧义：training-free 是只冻结基础模型，还是冻结整个系统的可学习参数？

| 口径 | 允许什么 | 学术名称建议 |
|---|---|---|
| TF-Strict | 基础模型、外部 evaluator/controller 均不训练；只改变上下文、外部状态、记忆、搜索树、工具轨迹和非参数统计 | **推荐作为 training-free RL headline** |
| TF-Core | 基础模型冻结，但外部 reward model/controller 允许训练 | frozen-core agent optimization / lightweight post-training；不宜裸称 training-free system |

owner 当前“只能通过外设优化”的描述更接近 TF-Strict。Stage-1A 必须签定口径；不能在实验后根据效果切换。

另一个术语冲突也必须修正：项目旧表述是“不改权重、不改结构”，但构建 agentic system 本身就在**新增外部系统结构**。正确说法应是：

> `no modification to the core model's weights or internal architecture; external control-plane structure is explicitly designed and versioned.`

否则“构建外部系统”与“不改结构”在字面上自相矛盾。

**kill-training-free**：任何承重增量依赖为当前任务训练的新参数、LoRA、policy、reward model 或 verifier。

### 3.3 RL / reward-guided control contract

为了防止把所有 test-time compute 都称为 RL，至少要定义：

```text
state s_t:
  observations, interaction history, memory, retrieved evidence,
  tool state, candidate actions, past rewards, remaining budget

action a_t:
  observe | prompt | retrieve | call_tool | sample | evaluate |
  select | revise | abstain | stop

feedback r_t:
  externally observable execution result, verifier signal,
  consistency/risk signal, environment feedback

transition:
  s_{t+1} = F(s_t, a_t, observation_{t+1}, r_t)

controller:
  a_t = π_ext(s_t, reward history, budget)
```

如果 reward 只在最后给 K 个答案排序，且不会改变下一步动作，则它只是 reward-model reranking。若存在 feedback→next action，但 controller 只是固定规则或 search/planning，领域 reviewer 仍可能称之为 inference-time search/alignment，而非 RL；团队必须用理论对象和对照实验说明为什么 RL 是必要而非宣传性术语。

**最强判别对照**：

1. one-shot prompting；
2. 等预算 BoN/MBR/rerank；
3. 等预算 agent workflow，但反馈随机/不进入下一步；
4. 等预算 heuristic search，无 reward/advantage；
5. reward-guided sequential controller。

只有第 5 项相对 2–4 的增量，才能归因于 training-free reward-guided control。

**kill-RL**：reward 不影响 next action；或等预算下与普通 search/feedback workflow 无差异。

### 3.4 Agentic contract

最低成立条件：

- 至少两个时间步，且第一步结果能够改变第二步动作；
- 有持久外部状态，而非每次独立 prompt；
- 有真实环境动作、工具调用、检索、记忆操作或显式 observation acquisition 中至少一类；
- 有 budget、stopping、failure recovery 或 abstention；
- 对轨迹而非只对终态候选定义 provenance；
- 在等预算下与 one-shot selector 可区分。

**kill-agentic**：系统可等价重写为“生成 K 个候选后取 argmax”，或所有工具序列在运行前固定、反馈不改变路径。

### 3.5 Omni contract

“底座模型名字里有 Omni”不等于系统是 omni agentic。至少要区分：

- `model modality capability`：模型宣称支持哪些模态；
- `agent observation`：controller/agent 实际看到了什么；
- `tool modality`：工具输入输出的模态；
- `action modality`：系统能否产生或作用于非文本环境；
- `causal grounding`：替换/遮蔽某模态是否改变计划与效用。

当前音频研究可以作为 omni system 的第一块 substrate，但若全部音频先被 STT 文本化、中央 agent 从不接触音频，最多是 audio-tool orchestration。AudioToolAgent 已展示中央 LLM 编排 audio tools 的邻域；你们必须说明“agent 实际接触原始/表征级多模态观测”带来的新增能力。

**kill-omni**：去掉非文本模态，系统行为与效用不变；或非文本仅是预处理输入，controller 实际是纯文本 agent。

## 4. 当前 proposal 的 P0 错位

### P0-SYS-1：primary object 仍是 selector surface

现行提案标题、§0、§1 和 `Research-Objective` 都把 “label-free、供给条件的选择算子在 model×task 矩阵上的兑现面”作为研究对象。UMBRELLA 仍是第五候选。这与 owner 澄清相反。

**要求**：不得只在原 proposal 加一段 agentic 文字；应新建 system-first proposal，以本报告 §3 五合同为骨架。旧 selector proposal 降为 supporting dossier，不得继续代表整个 Stage-1A 问题定义。

### P0-SYS-2：Project-Thesis 的 primary study 已过时

`Project-Thesis.md` 当前仍写 W1 primary study = RDU + reward-guided trajectory selector，primary metric = rho；`Research-Objective.md` 同样锁定 selector object。owner 的新澄清尚未进入正典，所以后续 AI 会继续把 selector 当主线。

**要求**：由研究团队在 owner 正式签字后以 dated supersession 更新 thesis/objective；本审查不代为修改。

### P0-SYS-3：round-2 survey universe 过度 selector-centric

当前 21 lanes 大量围绕 MBR、BoN、abstention、headroom、audio reranking。它们对控制平面有用，但不足以判定 omni agentic system 的新颖性。必须扩展或重做以下 survey lane：

1. reasoning+acting 与 environment feedback：ReAct、Reflexion、LATS、Self-Refine；
2. test-time agent feedback/control：IAD 等 sampling–evaluation–feedback 工作；
3. multimodal tool agents：MM-ReAct、ViperGPT、AudioToolAgent 及 audio/vision/robot agent 后继；
4. external memory/skill acquisition：Voyager 类 skill library 与 episodic memory；
5. training-free verification/control：LLM-as-Verifier、CoVer、test-time verification；
6. black-box prompt/search/agent optimization 与 API-only constraints；
7. reward hacking、verifier gaming、tool-result spoofing、loop over-optimization；
8. 等预算 agent evaluation、trajectory credit、cost/latency/risk accounting。

现有 selector round-2 可以作为 `SURVEY-B: evaluation/selection submodule`，但不能签为项目总 survey。

### P0-SYS-4：黑盒 headline 与现有技术计划冲突

echo-logprob、同核 likelihood、hidden-state/embedding 白盒诊断等，不应进入 strict black-box system 的承重路径。proposal 必须给每个组件标：

```text
BLACK_BOX_CORE | API_OPTIONAL | GRAY_BOX_DIAGNOSTIC | OUT_OF_SCOPE
```

任何 `GRAY_BOX_DIAGNOSTIC` 结果只能解释本地实现，不能支持跨闭源 API 的系统 claim。

### P0-SYS-5：没有 system-level falsification

当前 kill/pivot/proceed 表主要判断 selector、headroom、Goodhart 与 rho。主系统至少还缺：

- feedback causal ablation；
- tool/memory/action necessity；
- equal-budget loop vs one-shot；
- modality removal；
- reward removal/randomization；
- external-state removal；
- black-box-interface capability removal；
- failure recovery 与 stopping 合理性。

### P0-SYS-6：配置化基座只覆盖“实验单元”，未覆盖 agent graph

v1 工程批评继续有效且需要加严。未来统一 runner 不仅要配置 dataset/model/evaluator/selector，还必须配置完整 agentic transition graph。否则每种 tool loop、memory loop、reward loop 仍会变成一段定制代码。

### P0-SYS-7：Stage-1A 仍然禁止真实实验

系统定位改变不构成提前开机理由。当前 Stage-1A 应做 survey、五合同、架构 schema、mock environment 和 synthetic transition tests；不得调用真实 llama-server/API、不得读取真实 item 做 smoke、不得根据结果修改 action/reward 定义。

## 5. 文献邻域的重新组织

### 5.1 Agentic reasoning、行动与反馈

- [ReAct](https://arxiv.org/abs/2210.03629)：reasoning 与 acting 交织，是“反馈影响下一步动作”的基础 comparator；
- [Reflexion](https://arxiv.org/abs/2303.11366)：通过语言反馈与 episodic memory 改善后续尝试，直接压力测试“外部状态更新是否已知”；
- [Language Agent Tree Search](https://arxiv.org/abs/2310.04406)：将 search、value/feedback 与 agent trajectory 结合，压力测试 training-free control 的方法新颖性；
- [On the Role of Feedback in Test-Time Scaling of Agentic AI Workflows / IAD](https://arxiv.org/abs/2504.01931)：明确把 agentic test-time alignment 分成 sampling、evaluation、feedback，几乎就是你们系统控制面必须面对的最直接框架。

审查含义：`feedback→next action` 本身不是空白；创新必须落在 omni/black-box 约束、控制算法或系统规律上。

### 5.2 Multimodal / omni tool agents

- [MM-ReAct](https://arxiv.org/abs/2303.11381)：中央语言模型编排视觉专家完成 multimodal reasoning/action；
- [ViperGPT](https://arxiv.org/abs/2303.08128)：通过代码生成与模块执行完成视觉推理；
- [Voyager](https://arxiv.org/abs/2305.16291)：environment feedback、技能库与迭代 prompting 形成持续 agent；
- [AudioToolAgent](https://arxiv.org/abs/2510.02995)：中央 LLM 编排 audio-language tools，已直接占据一部分 audio agentic system 组合空间。

审查含义：构建一个“中央 agent + 多模态工具”的系统本身很可能只是已有范式迁移。你们需要证明：黑盒 omni core 本身在环中接触多模态、reward-guided controller 有等预算增量，并且不是固定工具路由。

### 5.3 Training-free verification、动作选择与风险

- [LLM-as-a-Verifier](https://arxiv.org/abs/2607.05391)：无需额外训练的通用验证与 agentic feedback；
- [CoVer](https://arxiv.org/abs/2602.12281)：test-time verification 同时作用于 instruction/action，直接压力测试供给+动作控制；
- [Inference-Time Reward Hacking](https://arxiv.org/abs/2506.19248)：外部 reward 被过度优化时会出现 Goodhart，且循环控制比一次性选择风险更大；
- MBR/BoN、pessimism、abstention 文献继续作为 evaluator/selector 与 safety 子模块 prior，而不再作为整个系统身份的唯一 survey。

### 5.4 当前仍不能声称的空白

在 system-first round-2 未完成前，不得声称：

- “首个 omni agentic system”；
- “首个 black-box agent optimization”；
- “首个 training-free RL agent”；
- “首个 reward-guided multimodal tool agent”；
- “外部控制平面本身具有新颖性”。

目前最多可写：

> `Owner-selected innovation hypothesis; direct occupancy and differentiating mechanism remain under Stage-1A survey.`

## 6. 重构后的研究问题树

### 主问题 RQ-SYS

严格黑盒、核心模型权重/内部架构不变时，外部 reward-guided sequential control 能否把 omni model 组织成具有真实多模态感知、工具行动、状态维护和反馈适应能力的 agentic system？

### RQ-CTRL：Training-free controller

在等调用、令牌、延迟和工具预算下，reward/advantage-guided controller 是否优于 one-shot、BoN/MBR、普通反馈 workflow 与 heuristic search？

### RQ-OMNI：多模态因果接地

非文本模态是否实际改变 evaluator、计划、工具选择与最终效用，而非只在前处理阶段被转写为文本？

### RQ-SAFE：Goodhart、风险与停止

外部 reward 被循环优化时，何时产生 reward hacking、工具投机、错误累积或 overthinking；能否通过悲观评价、弃权、预算和 stopping 控制？

### RQ-MEASURE：系统规律

哪些 label-free observables 能预测 headroom、trajectory improvement、failure regime 与是否值得继续计算？原 I4/rho(c) 在这里成为测量层，而不是 primary identity。

### 原 I1–I4 的新位置

| 原身份 | system-first 中的位置 |
|---|---|
| I1 一般 selector | one-shot/terminal selection baseline |
| bare-I2 / strict-I2 | audio-grounded evaluator/scorer 组件与模态因果探针 |
| I3 | safety、Goodhart、abstention、stopping 子系统 |
| I4 | compute/supply/trajectory 的测量与调度规律 |
| UMBRELLA | **主研究对象，不再是第五个等权候选** |

## 7. 配置化工程基座的修订要求

### 7.1 单一 agent runner schema

建议 Stage-1A 冻结如下结构，并仅用 fake backend/mock environment 做验证：

```yaml
study:
  id: s1b_agentic_probe_001
  stage: stage1b_directional
  hypothesis: RQ-CTRL

core_model:
  backend: black_box_chat_api
  asset: qwen3_omni_30b_gguf
  frozen: true
  interface_contract: black_box_v1
  forbidden_capabilities: [weights, gradients, hidden_states, attention]
  optional_capabilities: [logprobs]

environment:
  task: audio_tool_task
  dataset_adapter: ...
  observation_modalities: [audio, text]
  action_adapter: ...
  item_manifest: ...
  prior_exposure_union: ...

agent:
  state_schema: state_v1
  observation_builder: ...
  memory:
    type: external_episodic
    update_rule: fixed_nonparametric
  tools: [retrieval, calculator, audio_analyzer]
  action_space: [observe, retrieve, call_tool, sample, evaluate, select, revise, abstain, stop]

evaluation:
  evaluators: [...]
  reward_aggregation: ...
  information_boundary: fail_closed

controller:
  type: reward_guided_search
  trainable_parameters: 0
  state_update: ...
  action_rule: ...
  counterfactual_controls: [reward_randomized, feedback_blocked]

budget:
  max_model_calls: ...
  max_tool_calls: ...
  max_tokens: ...
  max_latency_s: ...

stopping:
  rule: ...
  abstention: ...

artifacts:
  resolved_config: required
  trajectory_log: required
  raw_io: required
  reward_trace: required
  environment_attestation: required
  attempt_registry: required
```

### 7.2 禁止“一种 agent loop 一段脚本”

实现必须抽象为：

- `CoreModelBackend`；
- `EnvironmentAdapter`；
- `ObservationBuilder`；
- `MemoryStore`；
- `Tool` registry；
- `Evaluator` registry；
- `SelectionRule` registry；
- `Controller` / `Planner`；
- `BudgetManager`；
- `StoppingPolicy`；
- `TrajectoryRecorder`；
- `StageGuard`。

换 task、model、tool、reward、memory、controller、budget 或 stopping 时只换配置/注册组件，不复制主循环。

### 7.3 Stage-1A synthetic tests

- `stage=stage1a` 连接真实 backend、数据路径或 API 时 fail；
- fake environment 中 reward 是否真的改变 next action；
- feedback blocked/randomized control 是否与 reward-guided 路径可区分；
- budget 在 model/tool/token/latency 四轴都能硬停止；
- evaluator 看见 gold 时 fail；
- 黑盒 contract 禁止 hidden/logit 依赖；
- trajectory log 能逐步重建 state/action/observation/reward；
- 同一 resolved config 得到相同 trajectory hash；
- component capability 不满足时配置解析即失败；
- fixed-pool selector 能作为 controller 的退化特例被单元测试复现。

这些测试不允许加载真实模型或真实数据，因此不违反 Stage-1A 零实验边界。

## 8. Stage-1A 修订路线

### Gate S0：owner 身份确认

形成一页签字件，明确：

```text
primary_object = black-box omni agentic system
north_star_method = training-free reward-guided external control
selector/evaluator = supporting components
training_free_scope = TF-Strict or TF-Core
core_structure_policy = internal architecture frozen; external system structure allowed
```

没有这份签字，后续 AI 会继续在旧 selector 正典上工作。

### Gate S1：system-first survey protocol

- 保留原 selector survey 作为子包；
- 新增 §4 的八类 agentic/system lanes；
- 对 ReAct、Reflexion、LATS、IAD、MM-ReAct、ViperGPT、Voyager、AudioToolAgent、LLM-as-Verifier、CoVer 做 backward/forward chase；
- 每个工作按五合同标注：black-box / training-free / RL-control / omni / agentic；
- 不用合取缺席自动证明新颖性；必须比较机制 delta。

### Gate S2：五合同与 falsification table

逐合同冻结 positive/negative examples、kill/pivot/proceed 和允许接口；任何词无法操作化则从 headline 删除。

### Gate S3：配置架构与 mock verification

完成 §7 schema、component registry 设计和 synthetic tests；不运行真实 backend。

### Gate S4：历史暴露与记录更正

- 把“GPU 至今为零”更正为“本 system-first proposal 新执行为零”；
- 历史 574 工件和数据暴露继续作为 inherited background；
- 真实 Stage-1B item manifest 必须排除 exposure union；
- 不把已暴露的 test-other 称为 untouched publication holdout。

### Gate S5：Stage-1A close review

只有在 S0–S4 全部关闭、system-first round-2 执行并形成候选机制 delta 后，才能请求 owner 结束 Stage-1A。结束 Stage-1A 与放行 Stage-1B 必须是两个签字动作。

## 9. Stage-1B 未来最小探针顺序（仅蓝图，当前禁止执行）

1. **B0 interface smoke**：进入 Stage-1B 后，第一条真实调用即登记 attempt #1；证明严格黑盒路径可运行。
2. **B1 agenticity causal probe**：feedback-enabled vs feedback-blocked/randomized，等预算；先证明反馈确实改变 next action。
3. **B2 omni grounding probe**：correct/permuted/masked modality，检验计划、工具选择与效用是否因模态变化。
4. **B3 reward-control probe**：reward-guided controller vs heuristic search vs BoN/MBR，等预算。
5. **B4 safety probe**：reward pressure/budget 增加时的 Goodhart、错误累积、abstention/stopping。
6. **B5 measurement probe**：用原 I4 指标预测何时继续计算值得、何时应停止。

如果 B1 失败，立即停止把系统称为 agentic RL；如果 B2 失败，降为文本 agent + audio tools；如果 B3 失败，降为通用 agent scaffold；不得跳过前置失败继续用 B5 的 surface 寻找正面叙事。

## 10. 研究贡献的正确表述顺序

Stage-1A 当前只能写“候选贡献”，不能写已证创新：

### Candidate C1：System

一个不修改核心模型内部的、接口可审计的 omni agentic control-plane architecture。

**非贡献情形**：只是 LangChain/AutoGen 类 orchestration 的音频适配，或中央 agent 只看文本。

### Candidate C2：Method

一个零可训练参数、reward/advantage-guided 的 sequential controller，在等预算下优于 search/workflow/rerank。

**非贡献情形**：reward 只用于最终排序，或收益来自更多调用。

### Candidate C3：Safety/Measurement

描述 black-box omni agent 在供给、预算、任务与 reward pressure 下的有效区间、失败规律和 stopping/abstention 机制。

**非贡献情形**：只画单模型三任务曲线，无通用 baseline 增量或可迁移规律。

## 11. 给研究团队 AI 的强制改稿指令

下一版 proposal 必须按以下顺序写，禁止从旧文复制 selector headline 后仅换名：

1. owner-signed program identity；
2. 五合同定义与术语降级规则；
3. system architecture、state/action/reward/transition/budget；
4. system-level closest prior 与 delta table；
5. equal-budget baselines；
6. system kill/pivot/proceed；
7. evaluator/selector/measurement supporting dossiers；
8. 配置化工程 qualification；
9. Stage-1A 零实验声明与 inherited exposure；
10. Stage-1B 未来蓝图；
11. owner Stage-1A close gate。

禁止出现以下句式：

- “因为没有训练，所以天然是黑盒”；
- “因为使用 reward，所以属于 RL”；
- “因为模型叫 omni，所以系统是 omni agent”；
- “因为调用了工具，所以是 agentic”；
- “没有单篇工作同时包含全部组件，所以我们有创新”；
- “selector 兑现率提高，所以 omni agentic system 成立”；
- “本轮未运行，所以项目历史上 GPU 零运行”。

## 12. 签署清单

```text
IDENTITY-01 primary object is system-first, not selector-first
IDENTITY-02 UMBRELLA promoted from fifth candidate to program object
IDENTITY-03 I1-I4 mapped to supporting layers

CONTRACT-01 black-box allowed/forbidden capabilities frozen
CONTRACT-02 TF-Strict vs TF-Core owner decision frozen
CONTRACT-03 RL state/action/reward/transition/controller defined
CONTRACT-04 agentic causal criterion defined
CONTRACT-05 omni causal grounding criterion defined

SURVEY-01 agentic/system lanes executed replayably
SURVEY-02 direct occupants and mechanism deltas recorded
SURVEY-03 selector survey labeled as submodule survey
SURVEY-04 no global novelty claim

ENGINE-01 single configurable agent runner designed
ENGINE-02 environment/tool/memory/evaluator/controller registries specified
ENGINE-03 StageGuard synthetic tests pass
ENGINE-04 no real backend/data touched in Stage-1A

INTEGRITY-01 inherited 574-artifact exposure disclosed
INTEGRITY-02 new-execution count scoped to current proposal
INTEGRITY-03 item-level exposure union required for Stage-1B
```

任一项 FAIL：不得签 Stage-1A close，不得开机。

## 13. 学术诚信裁决是否变化

不变化。

- owner 的新科学定位不能消除“GPU 至今零运行/全部文献级”与历史登记冲突；
- 也不能自动补齐已知 prior 遗失、test/dev 暴露和配置化缺口；
- 目前仍未建立 fabrication、falsification、plagiarism 的证据与故意链条，因此不认定 FFP；
- 重大范围失实与 QRP 风险已经建立，必须用 dated correction 修复；
- 若团队在知悉后仍把历史实验隐藏为零、把暴露 split 称为 untouched、或用 selector 结果替代 system claim，诚信风险将升级。

结论继续是：`FFP NOT ESTABLISHED; MATERIAL QRP ESTABLISHED; CORRECTION REQUIRED BEFORE SIGNOFF.`

## 14. 最终导师意见

owner 的澄清使项目的科学志向更完整：你们不是要在一个 K 池中挑得稍好，而是要探索**外部 reward-guided control 是否能把冻结黑盒 omni model 组织成真正的 agentic system**。这是一个值得严肃调查的研究纲领。

但越是系统级纲领，越不能靠宽泛名词掩盖对象：

- 黑盒要经 capability removal 仍成立；
- training-free 要经参数审计成立；
- RL 要经 reward→next-action 因果与 equal-budget comparator 成立；
- omni 要经模态移除实验成立；
- agentic 要经 feedback/state/tool/stopping 闭环成立。

当前 selector proposal 可保留为高质量 supporting survey，却不能再代表主 proposal。研究团队下一步不是运行 P-α/β/γ/δ，也不是继续为 strict-I2 寻找合取空白；而是先在 Stage-1A 完成 program identity、五合同、system prior survey 与可配置 agent architecture。完成后再送审，当前版本仍不签字。
