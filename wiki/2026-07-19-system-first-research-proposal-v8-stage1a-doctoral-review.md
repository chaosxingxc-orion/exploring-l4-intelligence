---
title: "System-first Research Proposal v8：Stage-1A 尾门敌意博士级复审"
date: "2026-07-19"
review_role: "严格外审人 / 博士生导师 / 研究诚信审计视角"
review_target: "wiki/2026-07-19-system-first-research-proposal-v8-consolidated.md"
target_commit: "a4ed640f3c0ec66875a5f395dfb32313573264d2"
target_git_blob: "87619149711f4541441210dc2689977ca0a0df8b"
target_sha256: "42e614f9852cf43ff0f13258faa44cdb6e86a7d10c7d7de3bcca64c003325a21"
review_verdict: "WITHHOLD_STAGE1B"
new_gate_major_count: 3
integrity_verdict: "未发现足以认定伪造、篡改或剽窃的证据；但仍存在会制造错误保证的验证不足，不得把当前绿色测试写成完整科学有效性证明"
scope_note: "本报告只新增日期审查件，不修改被评交付物、代码、sidecar、台账或正在进行的工作"
---

# 一、结论先行

## 1.1 当前究竟处于哪个阶段

当前仍是 **Stage-1A 的 survey-ready 尾门 / Stage-1B 启动签署前**，而不是已经进入
Stage-1B，更不是 Stage-2：

1. v8 自报 `current_activity_stage = Stage-1A survey-ready gate`；
2. systematic mapping 查询仍为 0；
3. 本轮没有新增研究模型调用和 smoke；
4. 现有活动是问题边界、证据模式、查询协议、台账 schema、编码器和校验器的收口；
5. 按当前阶段正典，**第一条正式系统查询才是 Stage-1B 的起点**，Stage-1B 仍然只做
   文献 mapping，不触碰研究模型；模型复现和方向性原型属于 Stage-2A。

因此，v8 对阶段的自我定位是正确的。sidecar、generator、reconciliation 和查询开局表
都是 Stage-1A 应有的研究基础设施，不属于越阶段实验。

## 1.2 总裁决

**暂不签署 Stage-1B，裁决为 `WITHHOLD_STAGE1B`。**

这不是因为 survey 必须在 Stage-1A 就读完所有未来论文，也不是要求团队现在跑模型、冒烟集、
统计功效或预算 cap。相反，v8 的检索车道已经具备开始系统 mapping 的广度。阻塞原因是：
**Stage-1B 要扩大的正是当前存在语义假绿的编码流水线**。若现在批量开查，错误会从 11 条
放大到数百条，形成带有可重复外观但不具备语义可靠性的知识库。

本轮有三个新的、有限且可验收的 Gate MAJOR：

| 门 | 结论 | 为什么是 Stage-1B 前置门 |
|---|---|---|
| Gate MAJOR-1 | `control_edges` 尚未绑定到具体 signal instance；行级 reward 与另一信号的控制边仍可被错误合取 | 会直接改变 RQ-SYS occupancy 与“空位”判断 |
| Gate MAJOR-2 | reconciliation 只验证“已有 evidence 条目的一致性”，没有验证承重字段 evidence 的完备性；错误 horizon 和伪 locator 可全绿 | Stage-1B 批量编码会把未举证判断当成已举证事实 |
| Gate MAJOR-3 | 仓库规定的 WSL2 正典环境只能复放到 10/11，而 v8 声称 11/11 | 正确指令下尚不能重放，不是恶意元数据问题 |

三个门全部清零后，可以签署 Stage-1B；不要求增加模型实验、不要求先给 survey 预算上限，
也不要求把 Stage-2 的 SESOI、正式效能验证或模型对标提前搬进来。

# 二、审查边界与多轮对抗式方法

本报告不是对成型论文做终稿审稿，而是检查 Stage-1A 尾门的四件事：

- 问题与阶段边界是否稳定到可以开始系统 mapping；
- 检索和文献角色是否足以避免系统性盲区；
- 编码—证据—派生链能否在规模化之前阻止语义假绿；
- 团队是否真实闭环了上轮问题，以及是否存在研究诚信风险。

我进行了四轮相互独立的核查：

### Round A：冻结与上轮问题闭环核查

- 冻结 commit、git blob 与 blob 字节 SHA-256；
- 对比 v6 原始评审版本与当前 HEAD；
- 复核 immutability registry；
- 复核 v7 三项 Gate MAJOR 的整改证据而不是只读回应信。

### Round B：干净环境复放

- Windows 当前环境运行 generator check 与 taxonomy v4 测试；
- 将 HEAD 导出到隔离目录；
- 按仓库强制口径使用 `wsl -d Ubuntu-24.04` 与
  `~/.venvs/speechrl` Python 3.12 运行同一套检查；
- 区分“恶意输入鲁棒性”与“正确指令下能否完成任务”。

### Round C：承重语义变异

不是只运行作者预先写好的七个 mutation，而是修改能改变科学结论的字段，随后重新生成
coding，并运行完整 11 项测试。核心问题是：**错误发生后，系统是否真的会红，而不是代码
是否能检测任意攻击。**

### Round D：论文 survey 与查询覆盖复核

- 复核 v8 的 49 条参考项及其角色分层；
- 检查上轮要求加入的直接近邻、边界和负结果是否真实进入；
- 以官方 arXiv / ACL Anthology 页面搜索新的直接近邻；
- 判断遗漏是“必须在 1A 开局表显式保证”的结构性遗漏，还是应由 1B 系统查询发现的正常遗漏。

# 三、必须明确认可的真实进步

严格审稿不等于忽略整改。v8 有四项实质进步。

## 3.1 上轮“已评审文档被原位改写”问题已经闭环

这是本轮最重要的诚信正向证据：

- 原 v6 在 commit `04cf987` 的 git blob 为
  `2af5131830e2a50a579658c8163f96b87524bb81`；
- HEAD 中 v6 仍为同一 blob；
- `git diff --exit-code 04cf987 -- <v6-path>` 为 0；
- 错误改写的历史 commit 没有被抹掉；
- 后续改为新的 dated response / v7 / v8；
- immutability registry 当前登记 71 条、71 个唯一对象，对当前 HEAD 复核为 0 failure。

所以，**上一轮 Gate MAJOR-3 已关闭**。本轮不得继续把该事故写成“仍在篡改”。当前的新问题
是校验覆盖不足，不是相同的不变性事故复发。

## 3.2 sidecar 单写链是正确的工程方向

`sidecar → deterministic generator → coding v5 → reconciliation` 明显优于在多份 JSON 中
手工同步。同一 method path 的 ID、kind、sha 同行绑定，canonical heading 解析、work ID
三方一致、coder/adjudicator 分离，都属于 Stage-1A 很有价值的程序知识。

特别值得保留：

- coding 是生成件而非第二个手写真源；
- 分母按当前记录动态计算，不再硬编码 N=11；
- method path ID 重复会失败；
- 11 条承重路径已有裁决状态；
- 作者提供的反例和非实现者反例都进入了测试链。

本报告要求补强这条架构，不建议推倒重写成每篇论文一段定制代码。

## 3.3 文献角色分层总体合理

v8 把 49 条分成：15 条正文深读、3 条校准、20 条 Stage-1B 开局队列、8 条测量工具、
3 条边界/负结果。这个分层避免把 benchmark、负结果和方法占据混进一个分母，符合
Stage-1A 的使命。

上轮要求的四类补充也已真实进入：

- Step-level verifier-guided hybrid TTS；
- RFG reward-free / internal-access 边界；
- DEGS internal-state 边界；
- legal verifier 负结果先验。

这些论文的角色安排基本正确，没有把边界证据包装成项目直接占据。

## 3.4 没有越阶段跑实验

v8 没有新增模型调用、smoke、效果比较、超参数搜索或系统实现。Stage-2A 的复现只作为
后续 no-force preview，没有被写成当前已完成贡献。当前工程工作服务于 survey 的配置化、
可追踪与可扩容，属于 Stage-1A 合理范围。

# 四、Gate MAJOR-1：因果边仍未绑定到“同一信号实例”

## 4.1 当前实现到底验证了什么

`valid_edges()` 只要求：

- edge 的 `signal_use` 出现在该 method path 的行级 `signal_use` 列表；
- edge 的 `decision_right` 出现在行级 `decision_rights`；
- use/right 组合在白名单；
- locator 和 semantics 非空。

`derive()` 又分别计算：

1. 行级是否存在 reward form + online/terminal lifecycle + reward use；
2. 行级是否存在任意一条 live control edge；
3. 两者与 sequential horizon 合取为 RQ-SYS。

问题在于，1 与 2 **没有要求来自同一 signal**。edge 中的 `signal_lifecycle` 也没有与行级
`signal_lifecycle` 绑定，更没有 signal ID。只要一行里同时出现“某个 reward”与“某条控制边”，
系统就可以把它们组合为 reward-guided sequential control，即使控制边由另一个非奖励信号触发。

## 4.2 精确反例一：lifecycle 自相矛盾仍 11/11 PASS

在隔离副本中，仅把
`2026.findings-acl.1243#open-sft-variant` 的行级 `signal_lifecycle` 从
`online_step` 改为 `terminal`，保留两条 edge 为 `online_step`；随后重新生成 coding 并运行完整
测试。

结果：**11/11 PASS，RQ-SYS 仍为 5/11。**

这说明所谓 control edge 已经“因果绑定”并不成立：相互矛盾的生命周期没有被拦截。

## 4.3 精确反例二：不同信号被错误拼接成项目候选

构造一条严格 omni method path：

- 终局 scalar reward 只用于选择；
- 另一个在线、非 reward 的 route 信号控制 `tool_call`；
- 行级 horizon 为 sequential；
- 其余 strict/S0 位均满足。

当前 `derive()` 会同时给出：

- `is_reward_guided = True`；
- `is_rq_sys_control_compatible = True`；
- `is_project_method_candidate = True`。

但该结论在语义上是假的：reward 并没有控制在线工具决策。现有 schema 把两个信号的性质
拼成了一个不存在的因果链。

## 4.4 `reward_guided_selection` 也尚未成为可靠轴

当前该轴只检查 `selection_policy ∈ {scored_select, tournament_select}` 与 reward-form，
没有强制：

- candidate pool 真实存在；
- reward signal 的 lifecycle 可在该选择点使用；
- signal use 包含 select/prune；
- 选择 operator 与该 reward signal 绑定。

因此，`offline_calibration + scalar_score + scored_select` 可产生：

- `reward_guided_selection = True`；
- `is_reward_guided = False`。

这不是一个可解释的 occupancy 轴，除非团队明确把它改名为“表面 selection policy 形态”；
若继续称 reward-guided selection，则必须补齐同信号因果约束。

## 4.5 最小、可配置的整改

不要为每篇论文写定制判断。应把 sidecar 的信号层正规化：

```yaml
signals:
  - signal_id: verifier_score_step
    form: scalar_score
    source: llm_judge
    lifecycle: online_step
    uses: [revise, stop_budget]
    evidence: ...

control_edges:
  - signal_id: verifier_score_step
    decision_right: retry
    lifecycle: online_step
    evidence: ...
```

派生规则必须写成存在量词：存在同一个 `signal_id = s`，其 form/lifecycle/use 满足 reward
定义，且至少一条有效 control edge 引用 s 并通向允许的 decision right。不能把行级 reward
与任意 edge 分开求真后再合取。

最低验收用例：

1. edge lifecycle 与被引用 signal lifecycle 不一致 → fail；
2. terminal reward + online nonreward route edge → RQ-SYS false；
3. online reward revise → retry → RQ-SYS true；
4. terminal reward select → synthesize/stop 可按既定政策判断，但不得获得 forward-step right；
5. 多信号 method path 不得依赖单一行级 `signal_form/lifecycle/use` 丢失身份；
6. `reward_guided_selection` 必须要求同一 reward signal、pool、select/prune use 与 operator；
7. offline calibration 不得自动成为 reward-guided inference selection。

若团队暂时不愿正规化 signals 数组，至少要强制 edge lifecycle == 行级 lifecycle；但这只能
修复单信号记录，不能正确表达 ATLAS/ToT/多阶段系统，因此不应作为长期 Stage-1B schema。

# 五、Gate MAJOR-2：reconciliation 有“完整”之名，无承重证据完备性之实

## 5.1 当前验证是条件式 presence check，不是 completeness check

`reconcile()` 对 `field_evidence` 的逻辑是：**如果某个 evidence 条目存在**，就检查其 value
是否与 method path 相同，以及 quote 能否在 canon/TeX 中出现。它没有规定哪些字段必须有
evidence，也没有验证每个派生结论的所有承重前提都已覆盖。

当前 8 个 sidecar 的实际覆盖是：

- 绝大多数只覆盖 `core_native_modality` 与 `signal_form`；
- DREAM 额外覆盖 `signal_source`；
- ToT 覆盖 `core_topology` 与 `signal_form`。

普遍未被 field evidence 覆盖的字段包括：

- `control_horizon`；
- `signal_lifecycle`；
- `signal_use`；
- `decision_rights`；
- `selection_policy`、candidate pool 与 selection object；
- strict 的多项 label/new-information/internal-visibility 位；
- edge 所引用的具体信号身份。

所以当前系统证明的是“已填写的少数 evidence 没有明显自相矛盾”，不是“occupancy 的全部
承重判断已由原文证据支撑”。

## 5.2 精确假绿一：改动 horizon 改变 headline，完整测试仍全绿

在隔离副本中，将
`2026.findings-acl.1243#open-sft-variant.control_horizon`
从 `sequential` 改成 `terminal`，重新生成 coding，运行完整 11 项测试。

结果：

- **11/11 PASS**；
- RQ-SYS headline 从 **5/11 变为 4/11**。

这是本轮最严重的反例：一个能够改变 proposal 核心占据数字的承重字段，既无字段证据约束，
也不触发任何完整性失败。由此，v8 的“七类突变 fail-closed”和“真 reconciliation”属于
超额保证。

## 5.3 精确假绿二：不存在的页码也被当作 locator 已解析

把一条 ATLAS 的 `source_locator` 改成 `p9999`，重新生成并运行完整测试。

结果：**11/11 PASS，派生数字不变。**

原因是无 quote 时，locator 只需匹配 `p\d+` 等字符串形状；系统没有检查 PDF 是否有该页、
该页是否含对应文本、locator 是否落到具体 claim。于是“locator 非空”和“locator 已解析”
被错误等同。

这也不属于恶意元数据攻击。研究编码人员在正确工作中写错页码，是最普通、最应被 Stage-1A
工具拦住的错误。

## 5.4 独立 AI 裁决不能替代 evidence completeness

coder 与 adjudicator 分离、两次 DISAGREE 被采纳，是好的治理证据。但 `adjudicated_agree`
只能说明另一代理同意了整行，不能证明：

- 它看到了每个承重字段；
- 它检查了每条 edge 的同信号因果链；
- locator 可被第三方定位；
- 缺失证据字段被 fail-closed。

独立裁决是程序的一层，不是字段证据的替代品。

## 5.5 最小整改：按“派生 claim”定义必需证据集合

不建议要求所有字段机械地逐项复制引文。应为每个派生 claim 声明 `load_bearing_fields`：

| 派生 claim | 最少承重证据 |
|---|---|
| strict | 权重更新、controller/label selection、deployment/test gold、external new info、internal visibility |
| reward-guided | signal form、lifecycle、use，以及同一 signal 的身份 |
| S0 | strict + topology + native modality |
| RQ-SYS | reward signal + horizon + decision right + 同 signal control edge |
| reward-guided selection | pool existence + selection policy/operator + select/prune use + 同 reward signal |

允许三类 evidence：

1. 正面原文锚点；
2. 明确的结构化 metadata / algorithm object；
3. 对“未使用/不可见”等负命题的专门 absence adjudication，含检查范围与不确定性。

缺证据时字段应为 `unknown/not_adjudicated`，不能默认为 False 后参与 strict 合取。

Locator 必须可解析：

- PDF：页码必须在页数范围内，并绑定页内 text anchor 或图表/算法对象；
- TeX：quote 必须出现在指定 section/object，而不是整包任意位置；
- canon：anchor 必须在指定 work section 内；
- 仅 `p9999` 这样的语法 token 不得视为解析成功。

新增 mutation 至少覆盖：

- wrong horizon；
- wrong lifecycle；
- wrong decision right；
- wrong selection policy/pool；
- fake page `p9999`；
- signal/edge identity mismatch；
- 两个字段同时翻转但仍维持表面自洽。

最后，v8 中固定的 6/11、5/11、4/11、0/11 等 release claim 应由生成件写入或由发布检查
对账。通用扩容 validator 不应硬编码 N=11，但**具体 dated proposal 的数字必须绑定到该次
生成输出**。否则数据变化后测试全绿而发布文本仍旧，不能称 release reconciliation。

# 六、Gate MAJOR-3：WSL2 正典环境并未实现 11/11 重放

## 6.1 复放结果

Windows 当前环境中：

- generator `--check`：通过；
- taxonomy v4：11/11 PASS。

但按仓库强制环境，在隔离 HEAD 副本中使用：

```text
wsl -d Ubuntu-24.04
source ~/.venvs/speechrl/bin/activate
Python 3.12.3
```

结果是：

- generator check：通过；
- taxonomy v4：**10/11 PASS，V7 FAIL**。

关键失败为：

```text
2604.16529:eprint-unreadable:E:/chao_workspace/.../2604.16529.eprint
2604.16529#pdr-random-k:row-locator:tex-quote-missing
2604.16529#pdr-random-k:field-evidence-tex-quote-missing
```

根因是 ledger 保存 Windows `E:/...`，而 WSL2 中相同资产路径应为 `/mnt/e/...`；当前
`tex_text(stored_at)` 直接使用台账路径，没有平台无关解析。

## 6.2 为什么这是 Gate，而不是低优先级“防篡改鲁棒性”

团队不需要在当前阶段防守恶意人员篡改元数据，这一点没有争议。但这里不是恶意输入：

- WSL2 Ubuntu-24.04 是仓库明文指定的正典环境；
- 使用的是正确命令、正确 distro、正确 Python；
- 正常台账路径在正典环境中不可读；
- 因而 v8 的 11/11 不能由规定环境重放。

这是“在正确指令下正确完成任务”的最低要求，必须在 Stage-1B 批量运行前修复。

## 6.3 最小整改

二选一即可：

1. ledger 保存 `asset_root_id + relative_path`，运行时由环境解析；或
2. 增加单一、可测试的 canonical path resolver，将 Windows volume path 在 WSL 映射到
   `/mnt/<drive>/...`，反向在 Windows 解析。

验收只要求：

- Windows 与 `wsl -d Ubuntu-24.04` 都能读取同一登记资产；
- 两边 generator 输出字节一致；
- 两边 taxonomy v4 得到同一 occupancy 与 11/11；
- 记录 Python 版本和执行命令。

不要求引入复杂攻击模型，也不要求检查任意伪造路径。

# 七、引用与文献 survey 评价

## 7.1 引用总体是否合理

**总体合理，但“参考文献齐全”与“承重 claim 已被逐字段引用支撑”必须分开评价。**

合理之处：

- 49 条数量及 15+3+20+8+3 的角色分解自洽；
- arXiv 与 ACL Anthology 使用稳定链接；
- measurement instrument 不进入方法 occupancy；
- boundary/negative prior 没有冒充直接方法支持；
- PDR、ToT 等身份更正继续保持，没有旧名字回滚；
- 上轮要求的 Step-level hybrid、RFG、DEGS、legal verifier 均已加入正确层级。

不足之处不是“没有更多引用”，而是正文的核心 occupancy 仍依赖 sidecar 中大量未被
field evidence 覆盖的字段。换言之，书目层面已经可用，claim-to-evidence 层面尚未过门。

## 7.2 新发现的高相关直接近邻

### P1：应在 Stage-1B opening guarantee 显式加入

1. **Reinforced Agent: Inference-Time Feedback for Tool-Calling Agents**
   （arXiv:2604.27233）

   官方摘要描述 reviewer 在执行前评价 provisional tool calls，并以 progressive feedback
   推动后续决策，并在 BFCL 与 Tau2-Bench 等任务上报告结果。它直接涉及外部 reviewer
   信号如何控制在线 agent action，是 RQ-SYS / TF-Strict 边界的高价值近邻。reviewer prompt
   或 reviewer model 的优化状态必须拆 method path 编码，不能只按论文题名归为 training-free。

   稳定链接：https://arxiv.org/abs/2604.27233

2. **Training-Free Test-Time Contrastive Learning for Large Language Models**
   （TF-TTCL，ACL Findings 2026 / arXiv:2604.13552）

   此项已存在于 seed/census，但没有进入 v8 自包含附录与 opening table。由于其题名和
   training-free、test-time、continual control 直接相交，应把 ACL 正式版本作为已知边界项
   显式列出，而不是依赖 1B 偶然再次发现。

   稳定链接：https://aclanthology.org/2026.findings-acl.1482/

3. **Training-Free GRPO**（arXiv:2510.08191）

   此项也已经在仓内 seed/旧台账，但 v8 的自包含书目和 opening table 未显式给出。它与项目
   内部简称有高度名称碰撞，必须在开局时完成“论文所称 training-free”与本项目 TF-Strict
   的边界编码，防止后续把同名当同定义。

   稳定链接：https://arxiv.org/abs/2510.08191

### P2：应由 Stage-1B 首批系统查询捕获，不构成新的开门阻塞

1. **Efficient Test-Time Scaling via Temporal Reasoning Aggregation（TRACE）**：
   训练免费终止/一致性控制的边界近邻，重点检查 confidence 是否属于 reward、是否只控制 stop。
   https://aclanthology.org/2026.findings-acl.651/
2. **Becoming Experienced Judges: Selective Test-Time Learning for Evaluators（LWE）**：
   以 evaluator/meta-prompt 顺序更新为核心，适合检查
   evaluator 持久化和外部控制器边界。
   https://aclanthology.org/2026.eacl-short.50/
3. **Thinking Long, but Short: Stable Sequential Test-Time Scaling for Large Reasoning Models
   （Min-Seek）**：training-free sequential scaling 的非显式 reward 替代路线，可作为
   RQ-CTRL 反例/邻域，不必在 Stage-1A 深读。
   https://aclanthology.org/2026.findings-eacl.153/

## 7.3 是否存在“查询设计的结构性漏项”

目前没有证据表明需要再新增一个大检索 lane：已有 query families 覆盖 feedback、verifier、
reward-guided、training-free、stopping/control 等组合，原则上能够发现 Reinforced Agent、
TRACE、LWE 和 Min-Seek。

因此，本轮文献结论是：

- 开局保证应补三项：Reinforced Agent、TF-TTCL、Training-Free GRPO；
- 其余新项进入 Stage-1B 首批队列；
- **不要在 Stage-1A 继续追求“读尽所有论文”**；
- 文献遗漏本身不阻塞开门，阻塞的是编码和证据链会把新论文错误固化。

# 八、研究范畴是否超越本阶段

## 8.1 未越阶段的内容

- 问题定义、严格黑盒和 external control plane 边界；
- 查询 compiler、child-query split、sentinel/calibration；
- sidecar schema、generator、record validator、lineage；
- 开局已知队列、负结果和 measurement instrument 分类；
- 为 Stage-2A 留下“复现先行”的 no-force blueprint。

这些都是 Stage-1A 可以且应该做的工作。

## 8.2 必须压回 Stage-2 的内容

v8 当前没有实际越线，但后续不得把以下事项塞入 Stage-1B：

- 任何研究模型推理或 smoke；
- 新方法效果摸高；
- 任何模型/数据集 benchmark 对标；
- selector/evaluator 的经验比较；
- SESOI 冻结、统计效能或多 seed 正式实验；
- 在未完成 prior reproduction 前开始项目方向性 prototype。

Stage-1B 的产出应只有：检索、去重、获取、证据分级、编码、独立裁决、占据图与负结果地图。
Stage-1C 才综合/选题；Stage-2A 先复现已有工作，再做方向性原型。

# 九、研究诚信与“是否涉嫌学术欺诈”裁决

## 9.1 本轮没有 FFP 证据

没有发现足以支持 fabrication、falsification 或 plagiarism 指控的证据。反而存在多项反欺诈
正向迹象：

- v6 原字节已经恢复，事故历史保留；
- 团队公开承认上轮错误保证；
- 独立裁决的 DISAGREE 被采纳，而非被抹平；
- method candidate 仍报告 0/11，没有为了叙事制造“已有占据”；
- 模型调用为 0，未把 proposal 工具测试包装成模型效果。

因此，**不得把本轮问题直接定性为学术欺诈。**

## 9.2 但存在 QRP / false-assurance 风险

v8 使用“真 reconciliation”“七类突变 fail-closed”“评审三重语义破坏已全被拦截”等强措辞，
但本轮已经给出：

- 改变 headline 的 horizon mutation 仍 11/11；
- row/edge lifecycle 矛盾仍 11/11；
- `p9999` 仍 11/11；
- 正典 WSL2 只能 10/11。

所以这些措辞在当前证据下不成立。若团队在收到精确反例后仍继续对外宣称“完整 fail-closed”
并据此发布 occupancy 结论，才会升级为严重 questionable research practice；目前更合理的
解释是验证设计不足与过度命名，而非主观造假。

整改期间应把表述降级为：

> 当前实现已验证单写真源、部分字段锚点和既定 mutation 集；尚未证明所有承重语义或跨环境
> fail-closed。

# 十、有限整改计划：不把 Stage-1A 变成无限工程项目

## P0-A：信号实例正规化

交付：

1. sidecar schema 增加 `signals[].signal_id`；
2. 每条 control edge 必须引用 signal ID；
3. reward/RQ/selection 从同一 signal instance 派生；
4. 现有 11 条 method path 迁移并重新裁决多信号路径；
5. 加入 §4.5 的七个 killer/positive controls。

验收：所有反例得到预期布尔值；原有正控不被误杀；生成仍是配置驱动。

## P0-B：承重字段 evidence contract

交付：

1. 为五类派生 claim 定义 required evidence set；
2. 缺失字段变成 unknown/not-adjudicated，不得默认为 strict False/True；
3. locator 真正解析到页/节/对象；
4. 加入 wrong horizon、fake page、lifecycle、signal-edge mismatch 等 mutation；
5. dated proposal 的固定数字与生成输出做 release binding。

验收：本报告三个精确 semantic mutation 全部触发失败；任意改变 5/11 headline 的未举证变异
不能在 release check 中全绿。

## P0-C：正典环境重放

交付：平台无关 asset path resolver 或 relative-path ledger；Windows/WSL2 两份机器输出。

验收：同一 commit、同一 sidecar bytes 在 Windows 与 Ubuntu-24.04/Python3.12 均为 11/11，
occupancy 一致。

## P1：开局文献补齐

交付：把 Reinforced Agent、TF-TTCL、Training-Free GRPO 加入 opening guarantee，并给出
角色、去重 ID、预期 route 和边界假设。TRACE/LWE/Min-Seek 进入首批 Stage-1B 发现/筛选队列。

验收：不是要求 Stage-1A 深读完成，只要求不会因“已知但未列”而漏过。

# 十一、Stage-1B 放行矩阵

| 放行项 | 当前状态 | 放行所需证据 |
|---|---|---|
| 阶段定义与无模型边界 | PASS | 保持现有定义 |
| 查询与文献角色广度 | PASS_WITH_P1 | 三项 opening guarantee 登记；其余交给 1B |
| 上轮文档不变性事故 | PASS/CLOSED | v6 blob 与 registry 证据已足够 |
| 单写真源架构 | PASS | 保持 sidecar→generator，不回到双写 |
| signal-to-control 同实例因果 | FAIL/MAJOR-1 | identity-bound signals + killer tests |
| 承重证据完备性与 release 对账 | FAIL/MAJOR-2 | required evidence + true locator + headline binding |
| WSL2 正典复放 | FAIL/MAJOR-3 | Ubuntu-24.04 Python3.12 11/11 |
| 学术欺诈证据 | NO FINDING | 保持更正与负结果透明度 |
| 是否允许 Stage-1B | **WITHHOLD** | 三个 MAJOR 全部清零后签署 |

# 十二、给研究团队 AI 的执行约束

1. 不要再通过增加更多宏大术语回应本报告；直接提交 schema、派生公式、反例和双环境输出。
2. 不要把作者预设 mutation 全红等同于语义完备；必须先通过本报告给出的作者外反例。
3. 不要为了过门手工特判当前 11 条论文；所有规则必须适用于 N≠11 的新批次。
4. 不要把 unknown 自动编码成 False，再因全 False 获得 strict 身份。
5. 不要跑研究模型或 smoke 来“证明工具有效”；那既不能修复本报告问题，也会越阶段。
6. 不要增加 Stage-1A survey 预算 cap；先修复扩容前的语义合同，Stage-1B 保持广搜姿态。
7. 不要原位改写 v8；以新的 dated response 回应，并保持 v8 blob 不变。
8. 回应必须逐项提供：变更 commit、受影响 schema、正/负控输入、预期与实际输出、Windows/WSL
   环境、仍未覆盖的限制。

# 十三、最终意见

v8 已经从“多人手工维护的漂亮 proposal”前进到“具有单写真源与部分可执行契约的 survey
基础设施”，并真实闭环了上轮最敏感的不变性事故。这一点应予明确认可。

但它还没有达到可以规模化填充的门槛：当前系统能让一项改变 RQ-SYS headline 的错误在完整
测试下 11/11 通过，也能把不同信号实例拼成不存在的 reward-control 因果链；同时规定的
WSL2 正典环境无法得到声称的 11/11。继续扩容会把这些问题从局部原型放大为系统性知识污染。

因此本轮裁决是：

> **当前仍为 Stage-1A 尾门；Stage-1B 暂缓签署。三个 Gate MAJOR 是有限、配置化、无需模型
> 实验即可完成的整改。全部清零后，应立即允许开展 Stage-1B 系统 mapping，不再以“还可以
> 多找论文”为理由无限延长 Stage-1A。**
