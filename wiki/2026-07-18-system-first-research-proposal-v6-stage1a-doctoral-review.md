---
artifact_id: "STAGE1A-DOCTORAL-REVIEW-2026-07-18-V6"
title: "Research Proposal v6 的 Stage-1A 博导级构念、引文与准入复审"
date: 2026-07-18
review_object: "wiki/2026-07-18-system-first-research-proposal-v6-consolidated.md"
reviewed_commit: "04cf98726ac254eb1d27ba79b49283a30e50ad73"
reviewed_blob: "2af5131830e2a50a579658c8163f96b87524bb81"
reviewed_worktree_sha256: "0427c6a0e273dde8e7760b2e9c412418927eec5718eedcdcc9a1b06ac0b673cb"
review_role: "Gate S1 外部评审 / 博导式敌意复核"
stage_verdict: "仍处 Stage-1A survey-ready gate，尚未进入 Stage-1B"
gate_verdict: "WITHHOLD_STAGE1B_PENDING_NARROW_SEMANTIC_REMEDIATION"
severity: "2 GATE MAJOR + 4 MINOR；未发现可据此认定的学术欺诈"
mutation_policy: "本件只新增日期化审查报告；未修改研究团队任何源文件、提案、台账、schema 或脚本"
---

# Research Proposal v6 的 Stage-1A 博导级复审

## 0. 一句话裁定

**现在仍是 Stage-1A 的 survey-ready 尾门，不能据 v6 直接启动 Stage-1B。** v6 对上一轮的
carry-forward、角色分母、证据模式和阶段边界作了实质修复；但它准备拿去全量编码的 taxonomy
仍没有把项目的承重身份——“reward/advantage 驱动下一步动作的序贯外部控制”——编码进
`is_project_identity_candidate`，并且把 Agentic Coding 的 vanilla PDR 错写成了 LLM-judge
比较选择。后一个错误已经使正文最醒目的 **3/11** 占据数字失真。

因此，本轮不是要求团队继续无限扩写 proposal，也不是要求在 Stage-1A 跑模型；只允许完成一次
**窄幅 schema 语义整改 + 已读论文重编码 + 数字联动更正**。整改通过后，Stage-1B 可以开始；
整改前启动 65 条查询与批量全文编码，会把错误构念复制到整个 mapping 数据集，返工成本远大于
现在暂停一轮。

## 1. 我如何判断当前阶段

### 1.1 现行阶段正典

`Research-Methodology.md` 的现行定义是：

- Stage-1A：问题界定、survey 设计、检索式、种子/哨兵、编码 schema 与静态/变异测试；
- Stage-1B：systematic survey/mapping 的实际执行，包括检索、筛选、全文编码、引文闭包与饱和；
- Stage-1C：综合 3–5 张候选问题卡并由 owner 选题；
- Stage-2A：先复现最近且最强 prior，再做方向性原型；任何 smoke 或单 item 模型调用都算实验。

现行门状态还要求 **Gate S1 签署 + owner 批准 + 第一条 systematic query** 才进入 Stage-1B。
v6 自己也声明 systematic mapping query 为 0，且请求的正是 Stage-1B 签署。因此，不能用“开局表
已经做好”或“已深读 known items”反向宣称已经进入 1B。

### 1.2 四字段阶段判定

| 字段 | 本评审判定 | 理由 |
|---|---|---|
| `current_activity_stage` | Stage-1A survey-ready gate | schema、known-item、开局表和门禁仍在接受准入审查 |
| `new_model_touches_since_gate_freeze` | 采信团队呈报为 0 | 本轮未发现相反证据；该项仍是 TEAM_ATTESTATION，不升级为机器证明 |
| `cumulative_model_touches` | 非零 | union v2 已披露历史 exposure；这不改变当前活动阶段 |
| `legacy_experiments` | INHERITED_PRIOR_EXPOSURE | 不能当成 Stage-1B 或 Stage-2 新证据 |

### 1.3 是否越阶段

**没有发现本轮新增的越阶段行为。** v6 及其附件做的是静态 schema、已知论文全文读取、证据
分层、carry-forward 和程序门禁；没有运行研究模型，没有 smoke，没有用任务指标替候选方向
“拉票”。§6 的 Stage-2A 内容保持为无执行力预告，也没有把方向性数字升级成结论。

这一点应保留。即使本轮 WITHHOLD，也不得以“补一组模型结果更有说服力”为由跑实验；那会制造
真正的阶段越界。

## 2. 复核范围与可回放结果

本轮没有只读 v6 的散文，还交叉检查了：

- `2026-07-18-sf-identity-taxonomy-v2.json`；
- `2026-07-18-sf-known-item-coding-v3.json`；
- `2026-07-18-sf-independent-counterexamples-v1.json`；
- `2026-07-18-sf-stage1b-opening-tables.md`；
- `sf_identity_taxonomy_v2_test.py` 与持久化输出；
- Agentic Coding 与 Team-of-Thoughts 的官方原文；
- v6 附录和 Stage-1B 保证队列中尚未显式登记的直接近邻。

### 2.1 干净快照重放

在 commit `04cf9872` 的纯 `git archive` 中，使用 WSL2 `Ubuntu-24.04`、项目指定 Python 3.12
虚拟环境、零联网，复跑了九项 bundle-only 门禁、taxonomy v1/v2 和 quantifier scan，共
**12/12 exit 0**：

1. package summary；
2. package mutation harness；
3. record validator fixtures；
4. route adjudication；
5. sentinel recall；
6. query compiler；
7. child-query replay；
8. real-row dry-run；
9. route validation；
10. taxonomy v1 test；
11. taxonomy v2 test；
12. quantifier lint。

这证明了 **MACHINE_REPLAYED_STRUCTURE** 能力包络内的可回放性。它不证明论文事实被正确编码，
更不证明派生构念具有内容效度。本轮恰好发现：测试稳定地复现了错误的 PDR 语义，因此“全绿”
不能用于反驳下述 Gate Major。

## 3. 对上一轮整改的公允结论

### 3.1 已经实质修好的部分

以下整改不是表面改名，应当确认并保留：

- 将方法路径、speech/omni 测量工具和 evaluator/reward 负结果拆成三张表，避免分母混用；
- 将 Agentic Coding 的 RTV、PDR、组合 pipeline 分行，分析单位比 v5 更接近论文结构；
- 将 `core_native_modality` 与“数据集中出现音频”分开，阻止 ASR 级联或 benchmark 被误算成
  原生 omni 核心；
- 将 topology、control horizon、decision rights、selection object、terminal operator 拉入
  机器字段，方向正确；
- 对 W4 exposure 计数降为考古估计，不再冒充规范事件级机器计数；
- 将 quantifier scanner 明确降为词法 lint，不再冒充语义证明；
- EchoChain 等零命中件获得开局保证入口，carry-forward 不再完全依赖冻结查询召回；
- Stage-1B 明确禁止研究模型与 smoke，Stage-2A 明确 reproduction-first。

### 3.2 本评审必须自我更正的一点

上一轮评审称 `2506.12928` 不命中冻结 65 查询，这一事实判断是错的。团队给出的
SF-L2-Q1、SF-L5-Q5、SF-L8-Q5 三条命中可以由现行 matcher 复现。v6 将这次异议和评审撤回
纳入双向诚信轨，是正确做法。本报告正式维持更正，不再把该项列为缺陷。

这也是一个正面的科研诚信信号：团队没有因评审者身份而接受错误事实，而是提交了可复核反证。

## 4. Gate Major 1：项目身份判定仍然没有编码项目身份

### 4.1 机器派生式与 S0/RQ-SYS 不相等

当前程序实际计算：

```text
is_project_identity_candidate =
    data_access_strict_bits
    AND core_topology in {single_core, single_core_multi_call}
    AND core_native_modality in {audio_native, omni_native}
```

但 v6 §1 明确写的承重研究问题是：外部 **reward-guided sequential control** 是否让终态选择
之外的决策获得额外效用；`Project-Thesis.md` 进一步规定 reward/advantage 要决定下一步动作，
池内选择只是退化特例。

当前派生式没有要求：

- `is_reward_guided == true`；
- `control_horizon == sequential`；
- reward/feedback 是否因果地改变 route/retry/branch/tool/supply/memory/stop 等下一步动作；
- `decision_rights` 是否非空且属于本研究外部控制平面的权利；
- signal 是在线反馈、终态评分，还是开发集离线校准产物。

所以它只在测“严格信息/训练边界 + 单核 + 原生模态”，最多可称 **S0 核心兼容位**，不能称
“S0/RQ-SYS 投影”或“项目身份候选”。一个完全没有 reward 和序贯控制的冻结原生 audio 模型，
会被该式误报为项目候选；一个真正用 reward 控制 route/supply/stop、但没有显式 K 池的系统，
又会被正文的“空位坐标”排除。

### 4.2 v6 又把 K 池重新变成承重身份

v6 §4.2 的“待检验候选空位坐标”要求：

```text
strict ∧ reward-guided ∧ K-pool ∧ native audio/omni single core
```

这与已经签署的 system-first thesis 冲突。K-pool selector 是一种机制路径，甚至是序贯控制的
退化特例；它不是系统身份必要条件。若某系统按 reward 决定是否取证、调用工具、修改供给、重试
或停止，而没有先生成固定 K 池，它反而可能比 terminal selector 更符合 RQ-SYS。

这不是无害的旧术语残留。若以该坐标执行 Stage-1B，检索结果会被再次组织成 selector-first
occupancy，系统级 route/retry/tool/memory/stop 论文会被降级或漏算。

### 4.3 `is_reward_guided` 的派生式也比研究问题窄

当前机器式要求：

```text
signal_form in {scalar_score, pairwise_comparison, verifiable_outcome}
AND signal_use intersects {select, prune, revise}
```

它有三项结构性偏差：

1. 研究问题允许 reward 决定 route、retry、branch、tool call、memory write、supply、stop、
   execute/skip；这些都被派生式排除。
2. 它按“信号长什么样”决定是否是 reward，却没有优先判断“信号从哪里来、何时产生、是否在线
   影响下一动作”。二值可验证结果可以是有效 reward；反过来，离线开发集准确率虽是 scalar，
   也不等于部署时在线 reward。
3. ToolGate 应被排除，主要因为其门控器经过监督训练、且不是部署期 reward 搜索；不能上升为
   “所有 binary gate 都不是 reward”的一般规则。

### 4.4 CE-1b 不是当前 topology 语义的有效反例测试

独立反例 CE-1b 声称 ATLAS 的 orchestrator+solver 分解应使其不属于项目身份，但当前测试中
ATLAS 已经因 `vision_native` 而返回 false。也就是说，即便把 topology 任意改坏，测试仍可由
另一个轴通过。这是典型的 **vacuous pass / pass-by-other-axis**，并没有检验它声称检验的拓扑
蕴含。

更重要的是，taxonomy 已经把 topology 放进承重派生式，却把“同权重多调用是否仍算单一核心”
推迟到 Stage-1C。这个裁决不能等到批量编码之后：Stage-1B 中每一篇同权重多角色/多调用系统
都会受它影响。可接受的处理只有两种：

- 在 Stage-1B 前冻结明确政策；或
- 同时保留两种政策的敏感性列，mapping 全程双算，Stage-1C 再选择解释。

不能一边让该轴参与唯一正典数字，一边称其语义尚未裁决。

### 4.5 必须如何修

至少拆成以下三个派生量，名称与能力包络一致：

```text
is_s0_core_compatible =
    strict information/training boundary
    AND declared single-frozen-core policy
    AND native audio/omni core

is_rq_sys_control_compatible =
    online reward/evaluative feedback exists
    AND control_horizon == sequential
    AND reward/feedback causally affects at least one next-action right

is_project_method_candidate =
    is_s0_core_compatible AND is_rq_sys_control_compatible
```

K-pool、terminal select、sequential revise、route、supply、tool、memory、stop 应作为机制分层，
而非塞入项目身份。另增 `signal_lifecycle`（至少 offline calibration / inference pre-context /
online step / terminal）或等价字段，避免把开发集分数和在线 reward 混成一个 scalar。

## 5. Gate Major 2：Agentic Coding 的 PDR 被事实性误编码，中央计数已经错误

### 5.1 原论文说了什么

官方论文 [Scaling Test-Time Compute for Agentic Coding](https://arxiv.org/abs/2604.16529)
区分两种操作：RTV 负责比较/选择，PDR 负责跨轮复用。官方 TeX source 的方法与消融进一步明确：

- vanilla PDR 使用 **random-K**：随机抽取 K 个上一轮摘要作为下一轮 refinement context；
- select-K 才使用 RTV 从 N 个摘要中选 K 个；
- 原始 PDR 最后一轮执行单 rollout，本文的 PDR 消融用 N 个末轮 rollout 的平均表现估计；
- full pipeline 才是“RTV 选 K → PDR 复用 → RTV 选最终 top-1”。

本地已冻结官方 e-print 的 SHA256 为
`137d5a936deea31ad2b62e9e830119ecc6f2c3405f4cd2e44b7e6190d7a543ad`；上述事实可在
`paper.tex` 的 sequential refinement、unified pipeline 和 random-K/select-K ablation 段直接复核。

### 5.2 当前 coding-v3 写了什么

`#pdr` 当前被编码为：

```text
signal_form = pairwise_comparison
signal_source = llm_judge
signal_use = [prune, supply]
terminal_operator = prune
is_reward_guided = true  # 由派生式得到
```

这把 full pipeline 的 RTV 选择能力错误继承给了 vanilla PDR，违反 taxonomy 自己声称的
“一行不得继承另一 variant 的优点”。PDR 的 `supply` 与 sequential horizon 是对的；pairwise
judge、prune 和 reward-guided 则不对。应给 random sampling 合法枚举，或用 `none/random_sample`
如实表达，而不是为了让字段有值而强塞 `pairwise_comparison`。

### 5.3 哪些数字必须联动撤回

在不改变其他 10 行的最低限度更正下：

- `strict ∧ reward-guided ∧ trajectory-pool` 从 **3/11** 降为 **2/11**：`#rtv` 与
  `#rtv-pdr-pipeline`；
- 这两条仍全部属于同一 work，因此还必须并列报告 **unique work = 1/8**，不能把组件路径与
  组合路径当成三份独立先验证据；
- `is_reward_guided` 至少从 **8/11** 降为 **7/11**；
- 正文 §4.2、claim-evidence matrix、持久化 occupancy 输出、opening table 和所有回应信中的
  派生数字必须一起更正。

这还是“最低限度”数字。Team-of-Thoughts 的 signal 也需要下述裁决，裁决后可能再降为 6/11。

### 5.4 为什么 12/12 PASS 没有挡住它

测试从 coding-v3 读取同一组手工值，再检查派生数字是否符合作者写入的期望；它没有把每行字段
同官方全文 locator 或 REC-2 正典记录做机器对账。因此，错误值和错误期望可以一起变绿。

这说明 `canon_projection` 目前仍主要是一项声明，而不是可执行 lineage。整改不需要重造整个
survey 工具链，但每条 method path 至少应补：

- `paper_work_id`、`paper_version_used`；
- `canonical_record_id` / REC-2 或 DFS 记录指针；
- 承重字段的 `source_locator`；
- 原文对象 SHA256；
- coder 与 semantic adjudicator；
- 从正典记录生成 projection，或能发现两者不一致的 reconciliation test。

否则，Stage-1B 批量编码只会稳定地产生更多“结构合规、语义失真”的绿色记录。

## 6. Minor 1：Team-of-Thoughts 不应未经裁决就编码成在线 LLM-judge reward

官方 [Team of Thoughts](https://arxiv.org/html/2602.16485) 描述的是：

- 预推理阶段用带 ground truth 的 calibration set 选择 orchestrator、形成 tool-agent 能力画像；
- 推理阶段 orchestrator 根据 query 与这些 profile 动态调用异质 tool agents，并评估、聚合响应；
- 其离散实现被表述为基于 query、候选响应和 calibration performance 的分类/稀疏权重分配。

当前 row 却写 `signal_form=scalar_score`、`signal_source=llm_judge`、
`signal_use=[route,select,synthesize_input]`，由此把它列入 `is_reward_guided`。这里至少混了三个阶段：
开发集 ground-truth accuracy、自然语言 capability profile、推理期 orchestrator 的路由/合成。

这项不能仅凭“orchestrator 会 evaluation”就算 reward。应拆清：

- offline calibration signal 的来源和用途；
- inference-time route 的直接依据；
- 是否存在每步在线标量/比较反馈；
- 该反馈是否因果改变下一动作。

若全文没有部署期独立 reward 信号，应把它作为 **profile-conditioned orchestration / evaluator
boundary**，而不是在线 reward-guided 占据者。由于它不影响当前 strict∧reward∧trajectory-pool
主数字，本项单列 MINOR；但它会影响 8/11 总数，须在 Stage-1B 前裁决。

## 7. Minor 2：method-path 分母与 work 分母仍需双报

v6 已经正确说“全部来自同一篇 Agentic Coding”，但仍用 3/11 展示占据密度。RTV、PDR 和组合
pipeline 不是三个独立工作；组合路径还包含前两者。方法路径分母适合描述机制拓扑，work 分母
适合描述文献占据强度，两者不可替代。

Stage-1B 所有 occupancy 至少双报：

```text
method-path occupancy = x / N_paths
unique-work occupancy = y / N_works
```

组合路径还应带 `component_path_ids`，防止在综合时把 component、ablation 和 deployed/full
pipeline 当成独立复制证据。

## 8. Minor 3：所谓“独立语义反例”需要可证伪，而不是代理身份背书

“由非实现者代理提出”可以降低同源偏差，但不是学术意义上的独立验证，也无法仅靠声明核验。
CE-1a 已被实现者修正事实前提，CE-1b 又由另一模态轴偶然通过。这说明当前制度更像来源分工，
还不是有效的 construct oracle。

要求不应是审查代理元数据鲁棒性，而应是反例内容满足：

- 每例只改变一个待检验构念，避免由其他轴代偿通过；
- 同时有正边界例、负边界例和 near-miss；
- 对每个派生量至少一个“旧规则会错、新规则会对”的 killer fixture；
- 反例预期来自书面定义，而不是从当前实现结果反推；
- 修改派生式后，旧缺陷 fixture 必须红、新合同 fixture 才能绿。

这符合用户已明确的重点：验证脚本在正确输入下正确完成任务；不要求现阶段花精力模拟恶意篡改
元数据。

## 9. 引用审查与论文遗漏

### 9.1 引用组织总体评价

v6 的参考文献比 v5 更可靠：按 DEEPLY_READ、CALIBRATION、KNOWN_QUEUE、
MEASUREMENT_INSTRUMENT 分节，speech benchmark 不再混入方法占据分母；arXiv/ACL 稳定链接
大体可解引用。作为 Stage-1A 送审件，这种组织方式已经足够，不应要求团队在 survey 开始前
预先穷尽所有论文——否则 Stage-1B 本身失去意义。

但“足以启动 mapping”不等于“开局队列可以漏掉自己中央方法的原始来源”。本轮沿 v6 已深读
论文的官方引用链检查，发现三项应保证进入 Stage-1B，而不是等待查询偶然召回。

### 9.2 P0 补入：PDR 原始论文

[Rethinking Thinking Tokens: LLMs as Improvement Operators](https://arxiv.org/abs/2510.01123)
（Madaan et al., 2025）正式提出 Parallel-Distill-Refine：并行生成、蒸馏到有界 workspace、
条件精炼并进入下一轮。它还包含“纯推理时 PDR 编排”与“为 PDR 训练 8B thinking model”两种
边界，正好能检验 TF-Strict 的路径拆分。

v6 已把 PDR 当作中央 method path，却没有在附录或 opening queue 中列其原始论文。这既是引文
谱系遗漏，也是造成 PDR/RTV 混码的直接风险。应作为 guaranteed DFS entry，分别编码 inference
orchestration 与 trained variant。

### 9.3 P0 补入：SWE-Replay

[SWE-Replay: Efficient Test-Time Scaling for Software Engineering Agents](https://arxiv.org/abs/2601.22129)
（Ding & Zhang, 2026）复用历史轨迹，在从头探索与从关键中间步骤分支复用之间动态选择，并明确
不依赖外部 LLM value estimate。它与“状态/轨迹复用、branch decision rights、无显式 reward
selector”的边界直接相关，是检验本项目是否错误要求 K-pool/scalar reward 的高价值近邻。

Agentic Coding 本身引用该工作，但当前 seed/opening table 没有登记。应进 system/control
method table，而不是仅作为 Agentic Coding 的隐含参考文献。

### 9.4 P1 补入：Test-time Recursive Thinking

[Test-time Recursive Thinking: Self-Improvement without External Feedback](https://arxiv.org/abs/2602.03094)
（Zhuang et al., 2026）使用 rollout-specific strategy、累积知识和自生成 verification signal 做
迭代自改进，作者明确把“没有 external feedback”作为边界。它不必被预判为项目占据者，但应作为
RQ-CTRL 的强反例/替代解释：增益究竟来自 reward-guided control，还是来自更好的自条件化与
供给设计？

### 9.5 已有文献不应重复判为遗漏

Self-Refine、Reflexion、Self-Certainty、ReAct 等已经在现有 seed manifest、谱系 lane 或旧 survey
中登记。它们未全部出现在 v6 附录，不等于团队从未覆盖。Stage-1B 要做的是把这些 inherited
entries 通过 carry-forward ledger 接到新 taxonomy，而不是重新做一轮散文综述。

### 9.6 引文格式小修

- Team-of-Thoughts 的官方全题名含 “through Orchestrated Tool Calling”，v6 A.1 目前截短；
- DeepVerifier 的官方题名含完整副标题，作为表中简称可接受，但参考文献正典最好保留全题名；
- GitHub 资源 `tau2-bench voice` 在真正用于证据时应钉 release/commit，而不只给浮动仓库首页；
- “DEEPLY_READ” 应绑定 version + locator + fulltext SHA，不要仅由附录分节名称承担。

这些不单独阻断 Stage-1B，但应随本轮窄改一起处理。

## 10. 多轮敌意评审记录

### Round A：阶段反证

我尝试用“known-item 已深读、门禁已全绿、开局表已完成”证明团队已进入 Stage-1B。反证失败：
现行阶段正典以第一条 systematic query 为起点，团队自己呈报为 0。因此结论仍是 Stage-1A 尾门。

### Round B：上一轮整改反证

我尝试证明 taxonomy v2 与三张开局表只是改名。该反证也失败：原生模态轴、分析单位、角色分母、
carry-forward 和证据模式均有实质改善；2506.12928 的三条命中也支持团队异议。

### Round C：构念 killer cases

构造三个最小思维实验后，现行身份派生式失败：

1. 严格、单核、原生 audio，但无 reward/无序贯控制——当前误报项目候选；
2. 严格、单核、原生 omni，reward 决定 tool/stop，但无固定 K 池——正文空位坐标漏报；
3. 在线二值可验证结果决定 retry/stop——当前因 signal form/use 枚举而可能漏报。

因此 Gate Major 1 成立。

### Round D：source-to-code 对抗抽查

我选择中央 3/11 中唯一含序贯控制的 `#pdr` 回查官方 TeX source。原文的 random-K 与 coding-v3
的 pairwise LLM judge 直接矛盾，且 full pipeline 才使用 RTV select-K。因此 Gate Major 2 成立。

### Round E：相邻论文扩展搜索

沿 Agentic Coding 的官方引用链和近邻主题核查，找到 PDR 原始论文、SWE-Replay 和 TRT 三项未在
当前 opening table 登记的高价值条目。前两项为 guaranteed-entry 缺口；TRT 为高优先边界。
这证明开局表仍可补强，但不支持“Stage-1A 必须先穷尽所有文献”的过度要求。

### Round F：诚信与越阶段反证

我检查了团队是否用内部测试绿灯冒充外部实验复验、是否掩盖历史 exposure、是否把校准件混入
方法分母、是否新增模型调用。v6 对证据模式的降格总体诚实，也主动保留异议和更正；没有发现
足以建立 fabrication/falsification/plagiarism 的证据。现存问题是严重语义编码错误与内部审查
未能发现源文矛盾，属于应纠正的研究质量问题，不等同于已证实的欺诈。

## 11. 科研诚信裁定

### 11.1 当前不能指控学术欺诈

本轮没有证据证明团队伪造论文、伪造模型结果、篡改实验数据、隐匿新模型运行或故意删除负结果。
相反，以下事实对诚信判断有利：

- v6 明示 systematic query 为 0，不冒充 survey 结果；
- 外部论文数字被限制为 SOURCE_REPORTED_TRACEABLE；
- W4 exposure 使用估计证据模式并披露 MInDS 事故链；
- 2506.12928 对评审错误提出了可复核异议；
- CE-1b 的构念争议没有被偷偷写成已裁决事实。

### 11.2 但有 material semantic QRP 风险

PDR 的编码与原文直接冲突，且该错码支撑 3/11 headline。现阶段更合理的解释是实现者把
PDR+RTV 组合路径的信号继承到了 vanilla PDR，属于粗心、schema lineage 不足或语义审查失败，
尚不能推断主观造假。

但是，从本报告送达起，该错误已获得明确 source locator。若团队在没有新原文反证的情况下仍
保留“PDR=pairwise LLM judge”和 3/11，则风险性质会从可纠正错误升级为明知冲突后的误导性呈报。

另请注意，commit message 中的“hostile review ZERO_MAJOR”只能证明内部流程曾这样记录，不能当成
独立同行评审结论。v6 正文仍请求 schema 语义复核，这一姿态是正确的。

## 12. 准入整改合同

以下是进入 Stage-1B 前的最小整改，不要求新实验，也不要求重做整个 proposal。

### P0-1：冻结真正的 system-first 身份派生

交付物：

- S0 core compatibility、RQ-SYS sequential control、full project candidate 三个派生量；
- signal lifecycle/source/use 的可执行定义；
- K-pool 从身份必要条件降为机制分层；
- topology 的单一政策或双政策敏感性输出；
- 对应 killer fixtures 与派生输出。

验收点：

- “原生 omni 但无 reward”不得报 full candidate；
- “reward 决定下一动作但无 K 池”可以进入 RQ-SYS candidate；
- terminal RTV 只能报组件/退化路径，不能冒充 sequential control；
- online binary verifiable signal 不因二值形式自动排除；
- trained offline gate 不因具有评价性自动纳入；
- CE-1b 必须由 topology 本身决定测试结果，或明确双算。

### P0-2：重编码 Agentic Coding 并重算所有派生数字

交付物：

- `#rtv`、vanilla `#pdr-random-k`、`#pdr-rtv-select-k/full-pipeline` 的源文一致编码；
- method-path 与 unique-work 双分母；
- headline、matrix、opening table、持久化 JSON 的联动更正；
- 能让旧 PDR 错码 fixture 失败的测试。

最低预期数字：

- strict∧reward∧trajectory-pool = 2/11 method paths；
- unique work = 1/8；
- reward-guided 总数最多先报 7/11，待 Team-of-Thoughts 裁决。

### P0-3：把 canonical projection 从声明变成 lineage

交付物：

- method row 到 REC-2/DFS canonical record 的机器可解析 ID；
- 承重字段 source locator、paper version、fulltext hash；
- projection producer 或 reconciliation validator；
- 任意 canonical field 与 coding row 不一致时 fail-closed。

这里不要求把所有论文全文结构化成复杂数据库；只要求中央 occupancy 数字不能再由无 locator 的
手填副本独立生长。P0-3 与 P0-2 可在同一窄改中完成，不另开长期工程。

### P1-1：裁决 Team-of-Thoughts

将 offline ground-truth calibration、profile、inference routing、response evaluation 分阶段编码；
明确是否存在部署期在线 reward。若没有，撤出 reward-guided 集合并重算总数。

### P1-2：补 guaranteed literature entries

将 2510.01123 PDR origin 与 2601.22129 SWE-Replay 加入 system/control opening table；将
2602.03094 TRT 加入边界/反证队列。只做登记、全文编码计划和 provenance，不要求在 Stage-1A
宣称它们的最终占据结论。

### P1-3：引文与资源钉定

修正截短题名；对实际使用的 GitHub measurement resource 钉 commit/release；DEEPLY_READ 条目
补 version、locator、fulltext hash。

## 13. Stage-1B 放行清单

| Gate 条件 | 当前状态 | 放行标准 |
|---|---|---|
| 阶段边界清楚、零新模型调用 | PASS | 继续保持；不得补跑 smoke |
| discovery/mapping 协议与可回放基础设施 | PASS | 新 commit 干净 archive 仍全绿 |
| carry-forward 与角色分母 | PASS_WITH_MINOR | 补入三项直接近邻；继续双分母 |
| project identity 内容效度 | **FAIL / GATE MAJOR** | P0-1 killer cases 全过 |
| central known-item source accuracy | **FAIL / GATE MAJOR** | P0-2 原文一致，数字联动闭合 |
| canonical-record lineage | PARTIAL | P0-3 可发现错码，而非只复现错码 |
| 科研诚信 | NO FFP ESTABLISHED | 错误公开更正并保留 supersession 链 |
| owner 批准 | PENDING | reviewer 复核零新 Gate Major 后另行签署 |

**最终决定：本件暂不签 Stage-1B。** 允许团队在 Stage-1A 内完成上述窄幅更正；不允许以本轮
意见为由扩大成新的实验战役、预算讨论或模型 smoke。更正件只要满足 P0-1～P0-3、P1-1 的
语义验收，并在干净提交态重放通过，评审应快速复核，不得借机重开已签署的 S0、v3 working
thesis 或要求“survey 前先完成 survey”。

## 14. 给研究团队 AI 的执行顺序

1. 冻结本报告所审 commit、blob、官方 e-print hash；不要原位改写审计件。
2. 先写三条人话定义：S0 core、RQ-SYS sequential control、full project candidate。
3. 用三个 killer cases 反推 schema，先让旧实现红，再改派生式。
4. 从 Agentic Coding 官方 TeX 重编码 RTV、random-K PDR、full pipeline；不要从 v6 散文复制值。
5. 分阶段重编码 Team-of-Thoughts；不确定处标 `ADJUDICATION_REQUIRED`，不要猜最近枚举。
6. 生成 method-path 与 unique-work 两套 occupancy，并联动所有 claim/matrix。
7. 接上 canonical record ID、locator、version、hash，再跑 reconciliation。
8. 登记 PDR origin、SWE-Replay、TRT 三项 guaranteed entries。
9. 在新 commit 的纯 archive 中复跑门禁；另做一次人工 source-to-code 抽查。
10. 输出一份日期化回应信，逐项给“问题—修改—证据—新数字—未决项”，再申请窄幅复核。

在以上工作完成前，不执行第一条 systematic query；完成并签署后，第一条查询即正式进入
Stage-1B。Stage-1B 仍然只“看、读、编码、综合”，不触碰研究模型。
