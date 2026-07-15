---
review_id: DOCTORAL-ADVERSARIAL-REVIEW-2026-07-15-SYSTEM-FIRST-V1
date: 2026-07-15
review_target: wiki/2026-07-15-system-first-research-proposal-v1.md
target_proposal_id: STAGE1A-PROPOSAL-2026-07-15-02
target_commit: 9672856e6ee21c9a8064dee039423172e0df44b1
target_git_blob: ac59f3728933e7ee4e78f54fb4839e47739fd5d0
review_stage: Stage-1A（问题定义与技术原型纸面设计）
review_role: 严格外审人 / 博导 / 科研诚信审查
overall_verdict: RETURN_FOR_MAJOR_REVISION
stage1b_execution_gate: NO-GO
survey_execution_gate: NO-GO_UNTIL_SEARCH_PROTOCOL_SIGNED
integrity_verdict: FFP_NOT_ESTABLISHED; MATERIAL_QRP_RISK_REMAINS; SELECTIVE_OMISSION_RED_FLAG
mutation_scope: 本报告为独立新增评审件；未修改被审提案、代码、配置、状态页或既有研究记录
---

# System-first Stage-1A 研究提案 v1：博导级对抗审查

## 0. 一句话裁决

**主方向纠偏是正确的，但本提案尚不能签署为 Stage-1A 合格问题定义，也不能放行 Stage-1B。**

团队已经把研究对象从 selector 单组件重新抬回“冻结黑盒 omni 核心之外的 reward-guided agentic
control plane”，并诚实承认现有 Hydra 入口仍是 stub、现阶段没有新增实验、最近邻表尚未经可回放
survey 核验。这些是实质进步，不是文字粉饰。

但是，提案仍有六个承重缺陷：

1. “reward 影响下一步动作”不足以把 inference-time search/control 定义成 RL；
2. “摸高阶段预算不设 cap”使轨迹 headroom、失败停止条件和因果对照都失去可识别性；
3. 团队已经掌握的 `JitRL`、`Audio-Mind`、`Agent-Omni`、`EChO-Agent`、`AuTAgent` 等强最近邻被漏出
   §4，形成选择性遗漏红旗；
4. Reflexion/LATS/Voyager 等工作的 delta 被写得过于乐观，不能靠“对方没有使用我方新术语”制造机制差；
5. 目标工程 schema 方向合理，但现实工程仍是训练型 GRPO 配置 + stub + 大量定制脚本，尚不存在可配置
   agent 基座；
6. 内部“R2 CONVERGED”没有可回放评审原始工件，且 canonical 状态、NO-GO→重开链、C1/C4 状态之间
   仍有冲突。

因此本轮裁决是 **RETURN_FOR_MAJOR_REVISION**，不是否定研究纲领。正确下一步仍是 Stage-1A 的
survey、合同澄清、schema/mock 与治理修复，**不是开始跑模型或数据实验**。

## 1. 审查边界与证据快照

本审查按 Stage-1A 标准进行，不要求论文级统计显著性、最终 benchmark 覆盖或成品系统；但要求：

- 研究对象可证伪且不靠术语自证；
- 最近邻检索足以支撑“问题仍值得研究”，不是支撑论文级 novelty claim；
- Stage-1B 探针可在未来被配置化、回放和因果解释；
- 任何不利历史、失败、暴露和相邻工作不得被省略或降格；
- 本阶段不得用真实运行代替问题论证。

静态核验快照如下：

- 被审对象固定为 commit `9672856`、git blob `ac59f372...`；
- umbrella worktree 在审查开始时为 clean；
- W1 `src/training_free_rl/main.py` 仍只打印 `TODO: implement the RL loop`；
- W1 现有 Hydra 配置仅有 model/dataset/rl/experiment 四类，其中 `rl/grpo.yaml` 明含
  `learning_rate`、`kl_coef`、`group_size` 等训练型语义；
- W1 的测试仅验证包可 import；仓库未发现所提 `AgentRunner`、`Controller`、`TrajectoryRecorder`、
  `BudgetManager` 或 `StageGuard` 实现；
- `projects/.../scripts/` 下有 124 个 `.py/.sh` 文件，虽包含 loader、审计和知识脚本，仍足以印证“历史工作
  依赖定制脚本，尚非统一 runner”的自述。

以上只用于评价工程资格，不构成实验执行。

## 2. 四轮独立对抗审查结论

### 2.1 第一轮：科学身份与形式对象

#### 做对的部分

1. **系统优先身份已与 owner 最新裁决一致。** §1 明确 primary object、north-star method、TF-Strict、
   strict-black-box headline，并把 selector/evaluator 降为 supporting components。相较 selector-first
   提案，这是必要且正确的目标恢复。
2. **五个 headline 词都有 kill 条件。** black-box / training-free / RL / agentic / omni 不再互相担保，
   某一谓词失败就删名，这个纪律正确。
3. **固定 K 选择被放回退化特例。** 这既保留历史资产，又避免再次把研究对象偷换为 selector。
4. **没有把系统创新写成既成事实。** §4 明示 delta 是待证伪假设，没有“首个”宣称。

#### P0-SCI-1：现有 RL 合同不能区分 RL、规划与启发式搜索

§2 的判据是“reward 改变 next action”。这最多证明系统是 **feedback-conditioned sequential
control**。MCTS、best-first search、beam search、verifier-guided refinement 同样会让评分影响下一次扩展，
但通常被称为 inference-time search/planning，而不是“学习了一个策略”。

[ReAct](https://arxiv.org/abs/2210.03629)、[LATS](https://arxiv.org/abs/2310.04406)、
[Tree of Thoughts](https://arxiv.org/abs/2305.10601)、[IAD](https://arxiv.org/abs/2504.01931) 都会根据
环境/价值/验证反馈改变后续动作。仅凭这一点，提案无法说明自己的“training-free RL”区别于上述工作。

必须在 Stage-1A 冻结二选一边界：

- **RL 路径**：外部系统存在明确的 policy/value/advantage update，奖励跨轨迹或跨 episode 改变
  `π_ext(a|s)`，并能写出更新算子、状态持久性、信用分配与稳定约束；或证明该算子等价于一个明确的
  KL-regularized policy-improvement objective。
- **搜索路径**：系统只在当前 item 内用固定算法扩展/筛选轨迹，不从奖励更新跨 item 的决策规则；此时
  对外正名应是 `reward-guided inference-time search/control`，TFRL 只保留为 program north star，不能作为
  已满足的方法类别。

这不是名称洁癖。两条路径的基线、收敛对象、污染风险和贡献归属完全不同。

#### P0-SCI-2：“无限预算摸高”使轨迹 headroom 没有定义

项目 glossary 的 `H(c)` 原本定义在给定供给 `c` 的有限 K 池上。提案 §6/§10 未给新定义，直接写成
“池/轨迹级头空”，同时 §1/§3/§5 又规定预算不设 cap。对动态 agent 而言，这会产生三个问题：

1. 轨迹集合随 controller、随机种子、工具反馈和预算共同变化，不再是固定 K 池；
2. 没有有限 horizon/budget，就没有可枚举或可比较的 oracle trajectory set；
3. “没找到更好轨迹”可能是探索不足，不能推导“该格无 headroom”。

必须拆成三个不同量，禁止继续共用一个 `H`：

```text
pool_headroom(c, K)       = 固定、先生成的同一候选池内 oracle − default
trace_pool_headroom(c,B) = 在预先固定 controller proposal distribution、预算 B、随机性协议下，
                           已生成轨迹池内 oracle − default
controller_gain(c,B)     = controller 在预算 B 下的期望效用 − matched default
```

第二个量仍只是“已采到的轨迹池上界”，不是环境中的真实可达最优。第三个量才是 controller 的效果，但不是
oracle headroom。若坚持研究真正的 policy headroom，必须再限定 environment、controller class、horizon、
可用信息与 outer resource envelope；否则它在经验上不可识别。

#### P0-SCI-3：效率可推迟，因果可比性不能推迟

owner 有权把“同预算下谁更省”放到 Phase 3；但提案把这一裁决扩张成“归因对照只需结构匹配，不需预算
归一”，这是方法学错误。

若 arm 5 因 reward 触发更多 model calls、工具调用、token 或更长 latency，而 arm 3/4 没有同等暴露，
差异可由计算量而不是 reward→action 机制解释。此处的 matched exposure 是**内部效度条件**，不是效率研究。

允许的 Stage-1B 设计应是：

- 主摸高曲线报告 `U(B)`，B 是 `{model_calls, tool_calls, tokens, walltime/cost}` 的预注册资源向量；
- 可采用宽松、很大的 outer envelope，但必须有限且先登记；
- 因果对照在相同 B 或相同实际 exposure strata 内比较 arm 3/4/5；
- Phase 3 才讨论 Pareto efficiency、成本压降和最优预算。

“无限 cap”还与 agentic 合同中的 budget/stopping、自身 §6 的预算失控 kill 直接冲突，应立即删除或改成
“不以小预算限制摸高，但使用预注册的有限安全外框并报告完整预算反应曲线”。

#### P1-SCI-4：TF-Strict 的“零可训练参数”表述逻辑错误

冻结的预训练 LLM/evaluator 本身包含可训练参数；研究要求应是**不更新/不拟合**，不是“参数不存在”。建议
改为三分表：

| 组件状态 | TF-Strict 是否允许 | 必须披露 |
|---|---:|---|
| `FROZEN_PRETRAINED_COMPONENT` | 是 | checkpoint/API version、训练来源可得性、无任务内更新 |
| `PREDECLARED_NONPARAMETRIC_STATE_UPDATE` | 有条件 | 写入/删除/检索规则、是否跨 item、污染与回滚 |
| `TASK_FITTED_OR_WEIGHT_UPDATED` | 否（仅 comparator） | 训练数据、目标、参数、与主结果隔离 |

“非参数统计”和 memory mutation 仍然是适应甚至学习，不能用“没有梯度”自动豁免。必须冻结哪些外部状态可以
更新、在何时更新、能否读取 evaluation item、是否跨 split 继承。

#### P1-SCI-5：omni 合同可能通过定义排除竞争者

“核心本身接触原始/表征级多模态观察”方向正确，但“表征级”过宽：ASR transcript、外部 audio encoder
embedding、核心内部 hidden state 都可被叫作 representation，却分别落在降名、外部工具和违反黑盒三种情况。

应改为：核心通过公开支持的 native modality API 接收原始音频/图像/视频，或接收一个预先声明且保留超越
文本转写信息的公开表征；外部 encoder 输出只算 capability supply/tool observation，不能冒充“核心原生
omni grounding”。同时把 headline 收窄为 **native-omni-core external-control agent**。否则用自行定义的
“omni core in-loop”排除 Agent-Omni/AudioToolAgent，容易变成定义性 novelty。

模态消融也不能只做“静音/遮蔽”造成 OOD；需要语义匹配但声学/视觉因素变化的反事实、模态置换和文本转写
等信息量对照。

#### P1-SCI-6：agentic 合同的逻辑“或”过松

§2 写“有 budget、stopping、abstention 或 failure recovery”。按字面只满足任一项即可。任何有限循环都应
强制拥有 **budget + horizon + stopping**；abstention/recovery 可按任务性质二选一或声明不适用。此外，
“≥2 步”只能防 one-shot，不能证明有效 agenticity；还需记录反馈干预对 action distribution/branch choice 的
影响，而不是只展示一个成功例。

#### P1-SCI-7：奖励代理与 gold utility 尚未被系统级隔离

合同写了 `r_t` 不含 gold，但缺少单独的 `RewardChannelSpec` 与 post-hoc `UtilityEvaluator`。至少冻结：

- controller 可见的 reward/feedback `S`；
- reviewer 可见但 controller 永不可见的 gold utility `U`；
- 每个 reward 的来源、校准数据、是否含 benchmark-specific rubric、是否读取参考答案；
- reward hacking/over-optimization 的压力轴与停止规则。

[Scaling Laws for Reward Model Overoptimization](https://arxiv.org/abs/2210.10760) 已表明继续优化不完美代理
会让真实目标先升后降。故预算越大越不能省略独立 utility 与 Goodhart 审计。

### 2.2 第二轮：引用真实性、机制解释和遗漏论文

#### 总体判断

**现有 arXiv ID 基本都是真实且与标题对应，未发现伪造文献；但“文献存在”不等于“机制 delta 正确”。**
§4 作为 preliminary seed table 可以存在，却不能承担创新定位或 Gate S1 签署。当前最严重的问题不是假
引用，而是：

- 对若干先行工作的 black-box/training-free 属性描述错误或缺证；
- 团队本地已知的更强竞争者被遗漏；
- 没有作者、版本、venue、页/节/table locator 和 claim-level span，无法从“题录核验”升级为机制核验。

#### 对现有引用逐项复核

| 工作 | 题录 | 提案叙述审查 | 必须改写的 delta |
|---|---|---|---|
| [ReAct](https://arxiv.org/abs/2210.03629) | 有效 | 基本正确 | 它已经实现 feedback-conditioned reasoning/action；差异只能落在 native omni、reward update 或系统化控制，不是“有没有 agent loop” |
| [Reflexion](https://arxiv.org/abs/2303.11366) | 有效 | **偏误** | 原文明确“不更新权重”、用语言反馈和 episodic memory；可由黑盒 API 实现。不能写“其 training-free 不含严格黑盒”作为机制差，除非给出接口级反证 |
| [LATS](https://arxiv.org/abs/2310.04406) | 有效 | **弱化了竞争** | 原文是 gradient-free MCTS、LM value/self-reflection、环境反馈。它与本项目的 reward-guided external controller 高度相邻；“没声明 TF-Strict”不是科学 delta |
| [IAD](https://arxiv.org/abs/2504.01931) | 有效 | 定位正确但严重威胁未充分吸收 | 它直接研究 black-box agentic task 上 sampling–evaluation–feedback、比较 BoN 并做 verifier-guided refinement 因果分析；应列为主 kill paper |
| [MM-ReAct](https://arxiv.org/abs/2303.11381) | 有效 | 基本正确 | 是多模态工具编排先行；项目只能声称 native-omni-core grounding 的待证差异 |
| [ViperGPT](https://arxiv.org/abs/2303.08128) | 有效 | 不完整 | 原文明示无需进一步训练、API 组合视觉模块；它占据 training-free compound-system orchestration，缺 reward loop 才是差异 |
| [Voyager](https://arxiv.org/abs/2305.16291) | 有效 | **弱化了竞争** | 原文明示 GPT-4 black-box query、无 fine-tuning、环境反馈、自验证、skill library；它直接占据 black-box + no-weight-update + persistent external skills |
| [AudioToolAgent](https://arxiv.org/abs/2510.02995) | 有效 | 基本正确 | 直接 audio agent system 竞争者；不能只用“中央文本体”一笔降级，应按本项目 omni 五轴逐项编码 |
| [LLM-as-a-Verifier](https://arxiv.org/abs/2607.05391) | 有效 | **“只占 evaluator”过早** | 原文面向 agentic task 提供 fine-grained feedback，并可作 task-progress proxy/dense RL feedback；其 scoring-token-logit 依赖应标能力差异，而非未精读即宣布“不占系统” |
| [CoVer](https://arxiv.org/abs/2602.12281) | 有效 | 方向正确 | 它是训练过的 VLA verifier，不能承重 TF-Strict，但直接占据 joint instruction/action test-time verification 与 scaling；应作 trained comparator/边界对照 |
| [Scaling Auditory Cognition](https://arxiv.org/abs/2503.23395) | 有效 | 机制占据警示正确 | 继续保留为 audio TTC/selection 直接先行 |

结论：团队内部“十条 ID 都通过”只能证明 bibliographic validity，不能推出 delta validity。尤其 Reflexion、
LATS、Voyager 三行必须重写。

#### P0-LIT-1：遗漏团队自己已经知道的强最近邻

这不是普通的“survey 还可多补几篇”。以下工作已经出现在团队现行
`2026-07-14-neighbor-matrix-v2.md`、`sota-cards-v2.md`、canonical census 或历史 agent-level survey 中，
却未进入本提案 §4：

1. [JitRL](https://arxiv.org/abs/2601.18510)：标题即 “Continual Learning in LLM Agents Without
   Gradient Updates”，以非参数经验记忆估计 advantage 并调制 action logits；这是 training-free RL 最直接
   的机制近邻。它因需要 logit access 不满足 strict black-box headline，恰应成为“方法最近、接口不合”的
   主边界论文，而不是被遗漏。
2. [Audio-Mind](https://arxiv.org/abs/2605.28480)：冻结 omni 前端、planner-guided 有界工具使用/重听，团队
   claim ledger 已有 full-text locator；它直接压力测试 frozen-omni agentic system 与长链退化。
3. [Agent-Omni](https://arxiv.org/abs/2511.02834)：不重训地协调 text/image/audio/video 专家，是
   system-level omni orchestration 的直接竞争者。
4. [EChO-Agent](https://arxiv.org/abs/2606.15141)：以冻结 Qwen3-Omni 组织 Tool→Evidence→Reason→Verify
   的音频推理工作流，是 native audio/omni agent 的直接近邻。
5. [AuTAgent](https://arxiv.org/abs/2602.13685)：训练 tool policy，故不能承重 TF-Strict；但它直接定义了
   “何时、调用哪个音频工具”并报告 tool-selection 上界，是必须超越的 trained comparator。
6. [Agent Workflow Memory](https://arxiv.org/abs/2409.07429)、
   [ExpeL](https://arxiv.org/abs/2308.10144)：分别占据可复用 workflow memory 与 API-only/no-parametric-update
   experiential learning，直接挑战 external memory/skill 的新颖性。

内部现行矩阵甚至已经总结：“每个组件分别被占据，intersection 暂未发现；IAD 是坍缩风险。”新提案却只列
较弱/较老近邻，会给外部 reviewer 造成团队绕开最强反例的观感。**这构成选择性遗漏红旗，但鉴于提案显式
标注 preliminary、Gate S1 尚未执行，本审查不据此认定故意欺诈。**修复期限必须是 owner/reviewer 对本提案
签字之前，而不是 survey 收尾时再补。

#### P1-LIT-2：还应纳入的机制族

Gate S1 不能只把下列工作当背景引用，而应纳入机制矩阵：

- 黑盒反馈修订：[Self-Refine](https://arxiv.org/abs/2303.17651)、
  [CRITIC](https://arxiv.org/abs/2305.11738)、
  [TPO](https://arxiv.org/abs/2501.12895)；
- 复合系统与工具编排：[HuggingGPT](https://arxiv.org/abs/2303.17580)、
  [AudioGPT](https://arxiv.org/abs/2304.12995)；
- compound-system optimization：[DSPy](https://arxiv.org/abs/2310.03714)、
  [TextGrad](https://arxiv.org/abs/2406.07496)；这些方法未必满足 TF-Strict，但能防止把“可配置外部控制面”
  误当成新机制；
- 边界对照：[TTRL](https://arxiv.org/abs/2504.16084) 明确在 test-time 用 RL 更新权重，应归
  `OUT_OF_SCOPE_WEIGHT_UPDATED`，不能与 training-free 混写。

#### P0-LIT-3：八个 lanes 只是主题列表，不是可签署检索协议

§11 缺少 exact queries、数据库、日期范围、venue coverage、纳排标准、dedup、版本钉、forward/backward
snowballing、停止规则、双人冲突裁决、claim locator 和负结果口径。因此当前 Gate S1 search design 的审查
结论为 **NO-GO_UNTIL_SEARCH_PROTOCOL_SIGNED**。

最低合格协议应包含：

1. discovery sources：arXiv、ACL Anthology、OpenReview、IEEE Xplore、ACM DL，Semantic
   Scholar/OpenAlex 仅作发现；承重证据回到论文原文/正式 proceedings；
2. 每 lane 的 exact Boolean query、同义词、时间窗、结果 cap 和排序；
3. 上述强近邻作为 mandatory seed，并对其做一轮 backward + forward citation chaining；
4. 纳排矩阵至少编码：core access、parameter update、external state update、reward type、policy update、
   modality path、tool use、budget/horizon、task、trained comparator；
5. 任何“NO_DIRECT_MATCH”必须达到预注册 saturation：连续两轮 snowballing 无新增直接邻居，且两名 reviewer
   独立同意；
6. 每个 load-bearing delta 必须有 version pin + section/page/table/equation locator + 不超过必要长度的 source
   span；
7. 搜索日志、原始响应或可重建结果 ID、失败请求、排除理由均写入 L3；
8. 最强 10–15 篇 threat papers 做双人独立 full-text extraction，不能用摘要核验代替。

### 2.3 第三轮：工程基座与可配置实验资格

#### 方向性判断

提案 §8 对现状的表述是诚实的，目标 schema 也比“每个实验写一个脚本”合理得多。**正确裁决不是要求团队
现在造一个完整平台，而是要求 Stage-1A 冻结最小 contract/schema，并用纯合成测试证明 fail-closed。**真实
backend、真实 dataset、API smoke 均应继续禁止到单独的 Stage-1B 放行。

#### P0-ENG-1：当前工程不是所提系统的基座

现有事实是：

- 主入口为 stub；
- 配置中心仍是 `rl/grpo.yaml`，语义上指向权重训练，与 TF-Strict 新身份相冲突；
- 仅有 import smoke test；
- 现有大量实验逻辑散落在脚本中；
- §8 列出的组件都还是纸面名词。

因此不能写“在现有 Hydra 基座上直接开始 agent 实验”。正确做法是建立新的、身份隔离的配置 namespace，
例如 `control/`, `environment/`, `reward/`, `budget/`, `memory/`, `tools/`；旧 `rl/grpo` 明确标
`LEGACY_WEIGHT_UPDATING/OUT_OF_SCOPE`，避免把历史 training config 误复用到 TF-Strict。

#### P1-ENG-2：目标 schema 仍缺十个复现与安全承重件

在 §8 已列组件之外，Stage-1A schema 必须至少补：

1. `TaskSpec / EpisodeSpec`：输入、允许信息、终止、gold 隔离、任务 utility；
2. `CapabilityManifest`：每个 backend/component 是否读 logits/hidden/gold、是否更新参数/外部状态、支持哪些
   modality；不满足 headline 时启动前 fail；
3. `RewardChannelSpec` 与 `UtilityEvaluator` 进程级隔离；
4. `TrajectoryEvent` 事件溯源：event id、parent id、state hash、action、observation、reward、cost、provenance、
   info-boundary label；
5. config lock：resolved config、git commit、model/API version、dataset manifest、prompt/tool schema hash；
6. nondeterminism contract：seed、temperature、并发顺序、retry 是否计预算、API nondeterminism；
7. tool contract：side effect、sandbox、timeout、idempotency、失败类型、rollback；
8. state snapshot/rollback 与跨 item memory 污染边界；
9. budget vector + horizon 的硬 enforcement，不只是记录；
10. recorded-response replay：真实 API 不保证可重算，但必须能用录制响应重放 controller/selector/evaluator
    逻辑。

#### Stage-1A 允许的工程交付

- JSON Schema/Pydantic dataclass 等静态 schema；
- mock model、mock environment、mock tool、mock reward；
- golden transcript 的**合成**泄漏负测；
- stage1a 连接真实路径/API/backend 必失败；
- 同一 recorded trajectory 在同版本规则下重放得到相同 controller decision；
- 固定池 selector 作为单步退化特例；
- capability manifest 不合规时 fail-closed。

本阶段不应编写真实 Qwen/Claude/OpenAI/llama.cpp adapter，不应读取任何 benchmark item，也不应以“接口冒烟”
为由做一次真实调用。提案对此总体克制，需保持。

### 2.4 第四轮：科研诚信与治理连续性

#### 诚信结论

- **Fabrication/Falsification/Plagiarism：未建立。** 未发现伪造论文 ID、伪造新实验结果或抄袭证据。
- **Material QRP risk：仍存在。** 选择性遗漏强近邻、机制 delta 过度有利、审查不可回放、状态正典冲突，若
  未更正就进入 owner/reviewer 签署或后续对外叙述，会构成重大可疑研究实践。
- **当前不能指控故意学术欺诈。** 意图无法从文档推定；且提案显式写明 preliminary/zero execution/no
  novelty claim，这些披露降低了欺诈判断。但这不降低修复义务。

#### P0-GOV-1：“R2 CONVERGED”不可审计

frontmatter 用很长一段话声称三路 Opus 内审、R1 修复、R2 零新发现，并自述草稿曾预写虚构审计块后自行
纠正。仓库中能找到这段叙述和 Decision-Log 摘要，却未找到独立保存的 reviewer prompt、原始输出、时间/
run id、版本输入、逐项 disposition 或文件哈希。故外部 reviewer 无法区分“真实独立审查”与“作者对自己
审查过程的摘要”。

应把状态改为 `INTERNAL_DRAFT_REVIEW_REPORTED_ZERO_NEW_FINDINGS`，不得写 `CONVERGED`。未来每轮必须有：

```text
review_run_id
reviewer/model/tool identity
input commit + target blob
exact prompt/instructions
raw response artifact + sha256
finding ledger
author disposition
rereview artifact + sha256
```

“预写虚构审计块”虽然在提交前纠正，不构成本次已提交 FFP，但必须保留为过程事故，并把“审计字段默认
PENDING、只有原始证据存在后才能转正”实现成机器检查，而非只写教训。

#### P0-GOV-2：最强不利证据的知识迁移失效

团队 L3 已经登记 JitRL/Audio-Mind/Agent-Omni/EChO/AuTAgent，当前 proposal 却遗漏它们；这说明“即读即
登记”尚未保证“新提案自动继承所有 threat papers”。建议新增 proposal build gate：

- 从 canonical census 查询所有 `kills ∈ {UMBRELLA, system-first}` 或
  `operator_type ∈ {tool-loop, agent-loop, external-policy-update}` 的 works；
- 生成 mandatory-threat appendix；
- 作者若不放入最近邻表，必须逐篇写排除理由；
- 未完成这一 join，proposal linter 失败。

这比依赖 AI 会话记忆可靠得多。

#### P1-GOV-3：NO-GO 历史不是未重开，但当前引用链不完整

事实链应完整写为：

1. 2026-07-04 owner ratified agent-level NO-GO；
2. 2026-07-06 owner 依原决定预留的 owner-level amendment 路径，明确重开完整 omni agentic system；
3. 2026-07-15 Gate S0 再次签署 system-first 身份。

所以本提案**不是偷偷违反一个仍有效的 NO-GO**。但 `Per-Work-Status.md` 和 `survey/README.md` 仍突出
“CLOSED absent r1–r3”，未伴随 07-06 amendment；这与 Decision-Log 自己规定的“以后引用关闭须同时引用
修正”不一致。提案也应增设一段 `prior_adverse_decision_and_reopening_basis`，同时引用关闭、修正和 S0，
避免只展示有利的新签字。

#### P1-GOV-4：C1/C4 状态发生回退

修正案 №1 与 Decision-Log 续43 已记录 owner 分栏签字并“C1/C4 正式关闭，Stage-1B 诚信前置满足”；新
Research-Objective 和提案 §10 又写“于 1B-0 由 owner 终验”。如只是再次确认，应写
`CLOSED; RECONFIRM_HASH_ONLY`，不能恢复成 pending gate。否则签字状态会循环，后续可被选择性解释。

#### P1-GOV-5：living status board 未随主身份更新

`Per-Work-Status.md` 顶部仍停留在 2026-07-14、selector-first/v4.2 状态，并在 agent-level 段落只写旧 NO-GO。
Project-Thesis/Research-Objective 已 system-first 不等于 canonical 全部一致。应在不改历史段落的前提下更新
living current-state 区，并加 supersession 链；这不是 append-only 历史重写。

## 3. 当前研究范畴是否越过 Stage-1A

### 合法且应继续的 Stage-1A 工作

- owner-signed identity 与五份合同的文字/反例冻结；
- system-first 可回放 survey 的设计、执行和 claim ledger；
- 强最近邻 threat matrix 与候选问题收缩；
- 单一 runner 的配置 schema、capability manifest、mock/fail-closed 测试；
- future Stage-1B probe 的纸面协议与 kill logic；
- 历史暴露、失败、NO-GO/reopen、C1/C4 状态的治理清算。

### 已出现的阶段越界或边界模糊

1. §10 标题把 “Stage-1B 蓝图”标成 `PRE_STAGE2_BLUEPRINT`。应改为
   `STAGE1B_PROTOCOL_DRAFT — NO EXECUTION AUTHORITY`。Stage-1A 可以起草 1B 协议，但不能用 Stage2
   蓝图标签模糊 1A/1B/2 三个门。
2. B0 的第一条真实调用、B1–B5 的任何模型/数据/API 运行都属于 Stage-1B，当前不得执行。
3. “把效用推到多高”“超越业界最优”是后续经验目标，不是 Stage-1A 可完成的科学结论。
4. 在 controller/update rule 尚未冻结前，不宜先写宏大的收敛定理；Stage-1A 只需定义 proof obligations 和
   形式对象。机制选定后，理论轨与实现必须证明同一个算子。
5. 选具体 task/dataset/model 可以在 survey 后形成候选矩阵，但不能用先跑的结果反向选择有利 cell。

因此，团队目前“零新执行”是正确的。越界主要存在于**文档标签与未来设计的可识别性**，尚未发现本提案
实际偷跑新实验。

## 4. 建议替换为一个更可证伪的 Stage-1A 科学问题

现有“构建 omni agentic system”仍过于像工程愿景。建议在 Stage-1A 收敛为：

> 在核心模型和所有外部参数均冻结、仅允许公开 API、gold 与 controller 完全隔离的条件下，外部 reward-
> guided controller 是否能在**必须依赖原生非文本模态且具有可验证环境反馈的序列任务**上，相对同资源暴露
> 的 reward-free search、feedback-randomized workflow 和 one-shot/BoN 基线产生可重复的因果增量？若有，
> 该增量来自 policy/state update、工具供给，还是单纯额外 test-time compute？

它保留 owner 的两层创新假设：第一层是 native-omni agentic system，第二层是 training-free reward-guided
control；同时把最危险的三种坍缩直接写进问题：文本工具编排、普通 search、更多预算。

Stage-1A 不需要现在决定唯一 metric，但必须先决定 admissible task class：

- native modality 有因果必要性；
- 环境/工具产生不依赖 gold 的可验证反馈；
- 至少两个反馈依赖决策点；
- 可以定义有限 horizon 与资源外框；
- 有 one-shot、BoN/MBR、reward-free search 和 randomized-feedback 对照。

## 5. 分级整改计划

### P0-A：科学合同修复（先于任何 survey 结论）

1. 增加 RL-vs-search decision table，并选择对外命名规则；
2. 定义 `pool_headroom`、`trace_pool_headroom`、`controller_gain`，停止共用 `H`；
3. 用有限 outer envelope 替换“预算不设 cap”，区分摸高曲线、因果 matched exposure 与 Phase-3 效率；
4. 重写 TF-Strict 为“无参数更新/任务拟合”，冻结 external-state mutation contract；
5. 收紧 native-omni input contract，定义 representation 的允许/禁止实例；
6. 修正 agentic 合同为 budget+horizon+stopping 必选；
7. 加 `RewardChannelSpec` / `UtilityEvaluator` / gold firewall。

**验收物**：一张 predicate matrix + 一份形式对象定义 + 每条合同至少两个正例、两个反例、一个边界例。

### P0-B：system-first survey 协议与最近邻修复

1. 把现有八 lanes 实例化为 exact-query protocol；
2. mandatory seeds 至少包含 IAD、JitRL、Audio-Mind、Agent-Omni、EChO-Agent、AudioToolAgent、AuTAgent、
   Reflexion、LATS、Voyager、AWM、ExpeL、Self-Refine、CRITIC、HuggingGPT、AudioGPT、DSPy、TextGrad、
   TPO、TTRL、Gao overoptimization；
3. 每篇按统一 schema 编码，不允许用“未写 TF-Strict”作为机制差；
4. 最强 threat papers 双人 full-text extraction；
5. backward/forward chaining + saturation stop；
6. 产出“已占据机制 / 接口差异 / 模态差异 / 尚未证实的 intersection”四栏矩阵。

**验收规则**：所有 `NO_DIRECT_MATCH` 都有 query log、排除记录和 saturation 证据；所有主 delta 有原文 locator。

### P0-C：Stage-1A 最小工程 qualification

1. 新建 TF-Strict agent config namespace，旧 GRPO config 明确隔离；
2. 冻结 typed schema 与 capability manifest；
3. 实现纯 mock 的 event-sourced runner 骨架；
4. 完成 gold firewall、StageGuard、budget enforcement、recorded-response replay 的合成负测；
5. 暂不接真实 backend/dataset/API。

**验收规则**：切换 model/task/tool/reward/controller 只改配置；每次 run 生成 resolved config 和 trace；违规
能力在启动前 fail；重放得到相同控制决策。

### P0-D：诚信与治理闭环

1. 将本提案内部 review 状态从 `CONVERGED` 降为可验证的内部状态；
2. 保存 R1/R2 原始评审工件或承认历史 raw unavailable；以后禁止只留摘要；
3. 给 §4 增加强邻 mandatory-threat appendix，解释每个排除；
4. 在 proposal 中补 07-04 NO-GO→07-06 owner amendment→07-15 S0 全链；
5. 同步 living status board 与 survey README 的 supersession note；
6. C1/C4 写为 closed + hash reconfirm，不得回退为 pending；
7. 保留“曾预写审计块后纠正”的事故记录，并添加机器门。

### P1：Stage-1B 协议草案重写

P0 全部通过后，才可提交独立 `STAGE1B_PROTOCOL_DRAFT`。建议顺序：

```text
B0 capability/API feasibility（授权后第一条真实调用，attempt #1）
→ B1 native-modality causal necessity
→ B2 finite-budget headroom / exploration adequacy
→ B3 reward→policy/action causal probe（matched exposure）
→ B4 reward hacking + stopping/abstention
→ B5 measurement/VoI probe
```

当前把 P-α 直接映射为“轨迹 headroom”不成立，必须先完成有限预算与轨迹池定义。B1/B2/B3 的顺序可由
成本决定，但任何 null 都必须区分：无模态必要性、无已采轨迹 headroom、controller 无兑现能力，三者不得
互相替代。

## 6. 给团队 AI 的强制检查清单

团队下一版回复必须逐条回答，不能以“已接受”代替证据：

- [ ] 是否给出 RL 与 search 的可执行判别器？
- [ ] 是否定义有限 B/horizon，并区分三种 headroom/gain？
- [ ] 是否在因果对照中匹配实际 resource exposure？
- [ ] 是否修正 TF-Strict 的“零可训练参数”措辞？
- [ ] 是否把 reward proxy 与 gold utility 进程/权限隔离？
- [ ] 是否把 JitRL、Audio-Mind、Agent-Omni、EChO、AuTAgent 放入 threat table？
- [ ] 是否重写 Reflexion/LATS/Voyager delta，并给 full-text locator？
- [ ] 是否完成 exact-query、纳排、snowball、saturation、双审协议？
- [ ] 是否明确现有 W1 不是可配置 agent base，并隔离 legacy GRPO 配置？
- [ ] 是否只做 schema/mock/fail-closed，零真实 backend/data/API？
- [ ] 是否把 Stage-1B 草案正名，维持独立 owner execution gate？
- [ ] 是否保存可回放的 review raw artifacts？
- [ ] 是否完整呈现 NO-GO→amendment→S0 链？
- [ ] 是否把 C1/C4 保持 closed，不循环造 gate？
- [ ] 是否同步 living status，但不重写历史记录？

任一 P0 项未完成，不得把状态写成 `CONVERGED`、`STAGE1A_COMPLETE`、`NOVELTY_ESTABLISHED`、
`STAGE1B_AUTHORIZED` 或“已可对标/超过 SOTA”。

## 7. 最终签署意见

| Gate | 本轮意见 | 理由 |
|---|---|---|
| S0 program identity | **维持有效，但合同需 major revision** | owner 身份选择有效；科学命名边界尚未冻结 |
| S1 survey search design | **拒签** | 只有 lanes，无可执行检索协议；已知强近邻遗漏 |
| S2 five contracts | **拒签** | RL/search、预算/headroom、TF-Strict、omni 表征仍有歧义 |
| S3 runner schema/mock | **条件接受方向，尚未交付** | 设计方向正确；现实仍为 stub/legacy configs |
| S4 exposure/integrity | **部分通过，需状态修复** | 零新执行与 inherited exposure 披露正确；治理状态不一致 |
| S5 Stage-1A close | **NO-GO** | P0-SCI/LIT/ENG/GOV 未关闭 |
| Stage-1B execution | **NO-GO** | 尚未有已签独立协议，且轨迹/预算对象未定义 |

**结论：RETURN_FOR_MAJOR_REVISION。**

我认可本轮最重要的方向恢复：研究对象应是 system-first，selector 是组件，training-free reward-guided
external control 是北极星。但目前的提案仍把“一个有反馈的 agent scaffold”过快等同于“training-free RL”，
把“更多计算摸高”与“reward 机制因果增益”混在一起，并遗漏团队已知的最强竞争工作。只有先完成上述 P0，
这个方向才从愿景变成一个严格、可证伪、不会被普通 inference-time search 或 audio tool orchestration 轻易
坍缩的博士研究问题。
