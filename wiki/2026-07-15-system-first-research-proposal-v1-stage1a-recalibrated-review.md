---
review_id: STAGE1A-RECALIBRATED-REVIEW-2026-07-15-SYSTEM-FIRST-V1
date: 2026-07-15
review_target: wiki/2026-07-15-system-first-research-proposal-v1.md
recalibrates: wiki/2026-07-15-system-first-research-proposal-v1-doctoral-adversarial-review.md
target_commit: 9672856e6ee21c9a8064dee039423172e0df44b1
target_git_blob: ac59f3728933e7ee4e78f54fb4839e47739fd5d0
stage_lens: Stage-1A（问题界定、广泛 survey、原型空间与工程基座纸面选型）
verdict: ACCEPTABLE_TO_PROCEED_WITH_STAGE1A_SURVEY_PROTOCOLIZATION
stage1a_close: NOT_YET_REQUESTED
stage1b_execution: NOT_YET_REQUESTED_OR_AUTHORIZED
integrity_verdict: NO_FFP_EVIDENCE; NO_QRP_ESTABLISHED_AT_THIS_PRELIMINARY_PROPOSAL_STAGE
mutation_scope: 仅新增校准审查；不修改团队提案、代码、配置或既有记录
---

# System-first 提案 v1：Stage-1A 使命校准后的评审意见

## 0. 校准结论

上一版审查的主要偏差，是把后续实验成立所需的条件，提前当成 Stage-1A 提案必须关闭的 P0。经按项目
三阶段方法重新校准，现裁决为：

> **本提案已经足以作为 system-first Stage-1A survey 与技术原型空间梳理的起点。允许继续把八个
> survey lanes 实例化为可回放检索协议；不需要在当前冻结预算 cap、等预算比较、最终 headroom 定义、
> controller 算法或完整工程实现。**

这不是说上述问题不重要，而是它们目前应作为**调研问题、抽取字段和未来决策点**存在，不能成为阻止广度
探索的先验答案。

当前也没有在申请 Stage-1A close 或 Stage-1B execution。因此正确状态不是上一版所写的“S1 NO-GO / Stage-1B
NO-GO”，而是：

- `PROCEED_WITH_STAGE1A_SURVEY_PROTOCOLIZATION`；
- Stage-1A 尚在进行，不评价 close；
- Stage-1B 尚未申请，故不作 GO/NO-GO 裁决；
- 继续维持零真实实验、零数据触碰、零模型/API smoke。

## 1. Stage-1A 的使命与价值到底是什么

Stage-1A 的价值不是提前写出一份缩小版 Stage-2 protocol，而是完成以下五件事：

1. **恢复并表达研究愿景。** 明确研究对象是黑盒 omni agentic system，training-free reward-guided
   external control 是牵引方案，selector/evaluator 是组件。
2. **发现问题空间。** 广泛了解业内已经如何构建 agent、如何利用反馈、如何组织工具/记忆、哪些路径需要
   训练、哪些可以保持权重冻结。
3. **寻找可能的提升点。** 允许多种互相竞争的解释与机制并存，不在 survey 前过早收敛。
4. **识别未来需要证伪的风险。** 例如普通搜索解释、更多 compute 解释、文本工具编排坍缩、reward hacking；
   当前只需登记，不需完成实验判决。
5. **为 Stage-1B 准备候选原型空间。** 输出配置抽象、组件边界与廉价探针候选；由 owner 另行决定是否、何时
   进入 1B。

按这个标准，提案的主要价值呈现是成立的：它恢复了 system-first 对象，提出五份暂定合同，列出系统结构、
基线族、kill/pivot 思路、工程目标 schema、零执行纪律和八条 survey lanes。对 Stage-1A 起点而言，这些已经
足够丰富。

Stage-1A 不应被要求现在回答：

- 最终 controller 到底是不是严格意义上的 RL；
- 最终每个任务的 metric/SESOI；
- 最终使用多少调用、token 或 walltime；
- 最终如何定义动态轨迹 oracle；
- 最终哪组模型/数据集进入 confirmatory evaluation；
- 最终工程 runner 的生产级安全与并发细节。

这些问题的正确位置，是先进入 survey 的问题清单，再由调研证据和 Stage-1B 原型共同帮助收敛。

## 2. 对上一版评价的明确撤回与降级

### 2.1 撤回“Stage-1A 现在必须设置预算 cap”

这是上一版最明显的阶段错位。

当前“全力摸高、预算不先设科学 cap”的资源姿态，与 Stage-1A 的广度探索并不矛盾。Stage-1A 本身不跑
实验，因此不存在当前预算失控；更不应在尚未知道哪些方法、任务和工具有效之前，先冻结一个可能错误的资源
边界。

正确要求只有两条：

- survey 时把 `{model calls, tool calls, tokens, latency/cost, horizon, stopping}` 作为**文献抽取轴**，观察
  各类方法怎样随 test-time compute 扩展、在哪里出现收益饱和或退化；
- 将来真正执行时如实记录资源使用。记录不等于当前设定科学 cap。

物理/API 安全上当然总会有机器容量、账户费用和超时保护，但那是执行安全外框，不应被包装成 Stage-1A
冻结的科学预算，也不应限制 survey 查找高预算、多轮、搜索树或长期记忆方案。

等到找到有希望的方案后，再讨论：

1. 如何绘制效果—预算曲线；
2. 何时需要 matched-resource 因果比较；
3. 何时进入成本压降。

这些属于 Stage-1B 后段、Stage-1C 决策包或 Stage-2，而不是当前 proposal gate。

### 2.2 将“RL 与 search 必须现在二选一”降为 survey 核心问题

上一版指出“reward 改变下一步动作不必然等于 RL”，这个概念提醒仍然成立；错误在于要求团队现在就冻结
唯一判据。

Stage-1A 更有价值的做法是建立一条 taxonomy lane，调查文献如何区分：

- reward-guided search/planning；
- verifier-guided iterative refinement；
- in-context/verbal reinforcement；
- non-parametric policy/value update；
- test-time parameter update；
- classical RL 或 KL-regularized policy improvement。

在 survey 之前，提案使用宽口径的 `training-free reward-guided external control` 作为 north star 是合理的。
最终对外是否保留 RL 一词，应当是 Stage-1A 调研产物，而不是调研前的先验 gate。

### 2.3 将“轨迹 headroom 必须立即形式化”降为开放测量问题

固定 K 池的 headroom 不能直接无修改地搬到动态轨迹，这一提醒仍有价值；但 Stage-1A 目前只需要登记：

- 文献怎样定义 agent ceiling、oracle、best trajectory 或 attainable utility；
- 动态候选集、搜索深度和工具反馈怎样改变上界；
- 是否存在比 headroom 更适合系统级研究的量，例如 success-vs-compute curve、regret、task progress、
  recovery rate 或 failure coverage。

不应现在强迫团队在 `pool_headroom / trace_pool_headroom / controller_gain` 中选定一套，更不应因动态上界
尚未定义就阻止 survey。测量语言可以在 proposal 中保持“候选/待 survey 决定”。

### 2.4 撤回“遗漏强近邻即选择性遗漏/QRP 红旗”

被审 §4 已明确写 `PRELIMINARY`、`待可回放 survey 核验`，也没有据此宣称 first/novelty established。
在一份为下一步 survey 提供种子的提案里，最近邻表不完整本身不是学术不端，也不能被推定为 cherry-picking。

JitRL、Audio-Mind、Agent-Omni、EChO-Agent、AuTAgent 等仍然应该加入下一步 mandatory seeds；但正确表述是：

> 团队已有知识库为 system-first survey 提供了高价值起始种子，应在新协议中主动继承，避免重复发现和
> 跨会话知识丢失。

这是一项知识组织和 survey completeness 改进，不是当前 preliminary proposal 的诚信定罪。故上一版
`SELECTIVE_OMISSION_RED_FLAG` 与由此延伸的 `MATERIAL_QRP_RISK` 在本阶段撤回。

### 2.5 将完整 agent 工程要求降为未来 qualification checklist

capability manifest、事件溯源、gold firewall、tool sandbox、重放等都是合理的成熟系统要求，但要求
Stage-1A 现在全部实现，会把问题调研变成平台工程。

当前工程价值应限于：

- 确认未来实验不能继续“一实验一脚本”；
- 形成单一 runner 的组件边界和配置草案；
- 明确 task/model/tool/reward/memory/controller 应可替换；
- 可选地做纯 mock/schema 验证，但不把它当作科学问题成立的 P0；
- 真实 backend adapter 和真实数据调用继续留给另行授权的 Stage-1B。

提案 §8 对“现有基座仍是 stub”的诚实披露已经满足 Stage-1A 最基本要求。旧 GRPO config 与新 TF-Strict
身份的隔离，可以作为后续工程 ADR，而不是当前 survey 的阻断项。

## 3. 校准后对提案各部分的评价

### §1 program identity：通过

system-first、TF-Strict、strict black-box、selector 降组件都与 owner 方向一致。资源姿态“先摸高→持续
整合→成本压降”适合作为研究路线，不应由 reviewer 在 Stage-1A 擅自改写为提前限算力。

建议只补一句：预算与停止机制的具体形式由 system-first survey 和后续原型决定，当前不冻结。

### §2 五份合同：作为 provisional survey taxonomy 通过

这些合同目前的价值是指导检索和文献编码，而不是构成最终 publication claim。应在标题或段首注明：

```text
PROVISIONAL_STAGE1A_TAXONOMY — to be revised by survey evidence
```

此前指出的 RL/search 边界、TF-Strict 中预训练冻结组件如何分类、native modality 如何定义，都应转成
survey extraction questions。它们不是当前拒签理由。

### §3 系统架构：通过

控制平面图足以表达要研究的系统对象。无需现在给出可执行算法、MDP 完整定义或收敛证明。预算对象四轴
作为未来记录维度是合理的；“不设 cap”不应解释为将来永不停止，而是当前不以效率约束缩小探索空间。

### §4 最近邻表：作为 seed table 条件通过

现有论文 ID 基本真实，表中 delta 明确写成假设。需要做的是把下列已知工作加入下一步 search protocol 的
mandatory seeds，而不是在 proposal 当前版本完成全文综述：

- JitRL；
- Audio-Mind；
- Agent-Omni；
- EChO-Agent；
- AuTAgent；
- AWM / ExpeL；
- Self-Refine / CRITIC / TPO；
- HuggingGPT / AudioGPT；
- DSPy / TextGrad；
- TTRL 作为更新权重的边界对照。

Reflexion、LATS、Voyager 的现有 delta 应标 `TO_VERIFY_FULLTEXT`，避免在 survey 前写成确定事实即可。

### §5–§6 基线和 kill：作为 future probe menu 通过

五臂与 kill 表在 Stage-1A 的价值，是告诉 survey 需要寻找哪些替代解释，而不是要求现在冻结完整实验设计。

- one-shot、BoN/MBR、feedback-randomized、reward-free search、reward-guided controller 是合理的候选基线族；
- 结构匹配、预算匹配和 compute scaling 应在 survey 中比较不同论文做法；
- 当前不需要裁决未来先跑哪一个，也不需要用等预算门阻止摸高；
- headroom、modality、reward、memory、stopping 都可保留为候选 kill probes。

建议把“kill 触发”统一改为 `candidate_kill_logic_for_stage1b_design`，防止读者误以为这些实验已经冻结。

### §7 支撑 dossiers：通过

selector/evaluator 历史资产作为组件知识继续有效。system-first survey 应继承而不是废弃它们，但无需让组件
measurement 再次主导研究身份。

### §8 工程 qualification：方向通过

“现状不是配置化基座”的披露正确；单一 runner schema 也符合 owner 希望。Stage-1A 可以做 schema/ADR/
mock，也可以在 survey 更清楚后再做，不能让平台建设抢占问题调研。

### §9 零执行与 inherited exposure：通过

这是本轮最清楚、最符合阶段纪律的部分。没有发现提案偷跑新实验。历史暴露如实继承，未来 Stage-1B 再做
manifest 排除即可。

### §10 Stage-1B 蓝图：作为无授权草图通过

它已经明确“无现时效力、开机须 owner 签批”。因此不应因为里面还没有最终预算、指标或完整因果设计而
否定 Stage-1A 提案。

为避免名称噪音，可把 `PRE_STAGE2_BLUEPRINT` 换成 `STAGE1B_EXPLORATION_MENU_DRAFT`，但这只是文档清晰度
建议，不是科学 gate。

### §11 Owner gates：应允许进入 search protocol 实例化

八条 lanes 目前是**协议输入**，而不是协议本身。上一版以“还没有 exact queries”为由拒签 search design，
混淆了“允许团队写协议”与“协议完成后允许执行查询”。

正确流程是：

1. 本提案通过，允许团队实例化 exact-query protocol；
2. 团队提交 query strings、数据库、纳排、日志与停止规则；
3. reviewer 再签“可以执行第一条查询”；
4. survey 执行与综合完成后，才讨论 Stage-1A close。

因此当前应给 Gate S1 的状态是 `PROTOCOLIZATION_AUTHORIZED / QUERY_EXECUTION_STILL_PENDING`。

## 4. 现阶段最有价值的 proposal 检查点

这些检查点不会提前收敛方法，也不会要求跑实验：

### Checkpoint A：问题空间是否足够广

- 是否同时覆盖 text-agent、VLM/omni、audio agent、compound AI system？
- 是否同时覆盖 search、reflection、memory、tool routing、verification、non-parametric adaptation？
- 是否查训练自由和训练型最强上界两侧，而不是只查完全同口径论文？

### Checkpoint B：每篇论文能否帮助回答“我们还能探索什么”

抽取字段建议保持开放：

```text
core access / modality path / external components / feedback type /
what changes at test time / persistence scope / compute scaling /
claimed mechanism / strongest result / failure mode / reusable implementation
```

不要在 Stage-1A 强迫每篇论文落入最终合同；允许出现新类别并修改 taxonomy。

### Checkpoint C：是否避免过早做 intersection novelty

当前最有价值的产出不是“没有论文同时满足五个词”，而是：

- 哪些机制已经成熟；
- 哪些组合只是工程组合；
- 哪些 failure mode 仍未解决；
- 哪些方向在 omni/audio 中尚未充分探索；
- 哪些开源实现可以组合成未来原型。

### Checkpoint D：是否形成多个候选，而非单一路线

survey 结束时至少保留 3–5 个 system-level candidate problems，例如：

- native multimodal evidence acquisition；
- reward-guided tool/observation scheduling；
- external memory/skill consolidation；
- verifier-guided iterative control；
- failure-aware stopping/recovery；
- 跨任务的统一外部 controller。

Stage-1A 不应在 survey 前预先指定哪一个必胜。

### Checkpoint E：工程基座是否服务探索，而不是主导探索

配置草案只需证明未来可以换模型、数据、工具、reward、controller，不需要现在实现生产框架。任何工程工作
都应回答：它是否让下一阶段更容易比较多个候选方向？如果只是提前为一个尚未选定的方法写大量代码，应暂停。

## 5. 校准后的下一步计划

### 现在立即做：Stage-1A survey protocolization

1. 用 §11 八 lanes 生成 exact-query protocol；
2. 把团队现有 census 中的强邻居自动加入 mandatory seeds；
3. 给每 lane 设计开放抽取字段，预算/调用量只是其中一轴；
4. 设计可回放 search log、论文版本和 claim locator；
5. reviewer 审核协议后再执行检索；
6. survey 中允许 taxonomy、候选系统结构和研究问题发生改变。

### 可以并行但不承重：工程纸面选型

1. 写一页 runner/config ADR；
2. 比较可复用开源实现和自研最小骨架；
3. 设计 model/dataset/tool/reward/controller 的配置接口；
4. 不接真实 backend，不读取数据，不以代码量作为 Stage-1A 进度。

### 现在不要做

- 不设置科学预算 cap；
- 不冻结 equal-budget 实验；
- 不选最终 controller；
- 不跑真实模型、数据或 API；
- 不根据已有小样数字淘汰 survey lane；
- 不宣称 novelty、SOTA 或系统机制成立；
- 不把 provisional contracts 写成 publication definitions。

## 6. 诚信判断的校准

在当前阶段，提案已经明确：最近邻表 preliminary、survey 未执行、创新是假设、零新实验、既有数字仅为
hypothesis-grade。基于这些披露：

- 没有证据支持 fabrication/falsification/plagiarism；
- 也不足以认定选择性引用或 material QRP；
- internal `CONVERGED` 最多是文档内部复检用词过强，建议改成“内部一致性复检完成”，但不是本轮阻断项；
- canonical 状态和 C1/C4 措辞不一致是治理清理任务，不应劫持 system-first survey。

真正需要警惕的诚信风险发生在未来：如果 system-first survey 已完成后仍故意排除已知强邻，或把 preliminary
delta 转写成已证 novelty，才应升级审查。目前不应预判团队有欺诈动机。

## 7. 最终校准签署

| 项目 | 校准后意见 |
|---|---|
| system-first 研究身份 | 通过，符合 owner 方向 |
| Stage-1A proposal 起点 | 通过，可继续工作 |
| 八 lanes | 通过，允许实例化检索协议 |
| 第一条真实 survey 查询 | 待 exact-query protocol 单独签署 |
| preliminary 最近邻表 | 条件通过；强邻作为下一步 mandatory seeds |
| 五份系统合同 | 作为 provisional taxonomy 通过 |
| 工程 schema | 作为纸面/可选 mock 方向通过，不承重 |
| 新实验执行 | 继续禁止；团队当前零执行正确 |
| Stage-1A close | 尚未申请，不评价 |
| Stage-1B | 尚未申请或授权，不作 GO/NO-GO |
| 科研诚信 | 无 FFP 证据；当前 preliminary 阶段不建立 QRP |

**最终结论：ACCEPTABLE_TO_PROCEED_WITH_STAGE1A_SURVEY_PROTOCOLIZATION。**

本轮真正应该严格的地方，是保证 survey 足够广、记录可回放、强反例会被主动纳入、候选方向不会被过早
收窄；而不是提前替未来实验设预算 cap、冻结最终测量学或要求完整 agent 平台。Stage-1A 的使命是扩大并
组织认知空间，直到团队能够有依据地选择值得进入 Stage-1B 的问题，而不是在认知空间尚未打开前就把答案
写死。
