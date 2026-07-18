---
artifact_id: "STAGE1A-V7-DOCTORAL-ADVERSARIAL-REVIEW-2026-07-18-01"
title: "Research Proposal v7：Stage-1A 尾门严格复审与 Stage-1B 启动裁定"
date: 2026-07-18
review_role: "严格审稿人 / 博士生导师 / 科研诚信复核"
review_target: "wiki/2026-07-18-system-first-research-proposal-v7-consolidated.md"
review_target_commit: "87877f1ff3cd5f6ee3da95dcf751ad255eddb5f5"
review_target_git_blob: "e2d0d7b949431a095290e88ec02300a505a25cb2"
review_target_sha256: "2c8c4fc10485097f880404bc8bc60f55075ef6e17d0fc999967819efad5dd01d"
verdict: "WITHHOLD_STAGE1B"
gate_majors: 3
scope_note: "仅新增本日期审查报告；未修改被审件、脚本、台账、编码表或团队其他工作。"
---

# Research Proposal v7：Stage-1A 尾门严格复审与 Stage-1B 启动裁定

## 0. 一页结论

### 0.1 当前到底处于哪个阶段

**当前仍是 Stage-1A 的 survey-ready gate（Stage-1B 正式启动前），尚未进入 Stage-1B。**

判定依据不是文档标题，而是活动事实：v7 自报 systematic mapping query = 0；第一条 systematic
query 才是 Stage-1B 起点；本轮没有新增研究模型调用或 smoke。按照当前阶段正典，Stage-1B 是
**系统性检索、筛选、精读、编码和饱和度追踪**，仍然以“看”和知识组织为主；模型复现属于
Stage-2A，方案原型与比较实验更在其后。因此：

- v7 的 survey schema、静态 validator、既有论文全文核对和开局队列整理属于 Stage-1A；
- Stage-1B 可以开展系统性 mapping，但不得运行研究模型、smoke 或效果实验；
- Stage-2A 的“最近邻复现先行”在 v7 中只是无执行力预告，当前没有发生越阶段执行。

### 0.2 总体裁定

**裁定：暂不签署 Stage-1B，WITHHOLD。**

这不是因为 proposal 还不够像论文，也不是因为必须继续无限扩充文献，而是因为批量 mapping 即将
依赖的两条承重机器链仍会产生 false green，另有一项审计层不可改写规则被实际违反：

1. **Gate MAJOR-1——RQ-SYS 的“因果控制”没有被机器实现。** 当前派生式只要求“存在某种
   reward use”且“存在某种 decision right”，并不要求该信号真的控制该权利。无关的两者可以被
   拼接成 `is_project_method_candidate=true`。
2. **Gate MAJOR-2——所谓 lineage reconciliation 只能查“字符串/文件存在”，不能发现语义
   错码。** 在隔离副本中把 `paper_work_id`、模态和 locator 改错，v3 测试仍然 9/9 PASS；团队
   请求复核的 P0-3“可发现错码”因此尚未达成。sidecar 单写链被推迟到 Stage-1B 首周，顺序错误。
3. **Gate MAJOR-3——已经接受评审的 v6 日期件被原位改写。** v6 在修复提交中发生 39 行新增、
   26 行删除；但 v7 又把 `v6@04cf987` 称为被审历史状态。历史 commit 尚在，故证据未灭失；然而
   这仍违反仓库自己的“审计层 append-only，更正走 dated supersession”规则。

上述三项都是**有限、可机器验收的门禁**。清零后，无须再重开研究命题，也无须先做模型实验，
即可签署 Stage-1B。

### 0.3 对科研诚信的结论

**目前没有足够证据指控 fabrication、falsification 或 plagiarism，也没有证据证明主观造假意图。**
团队对 PDR 的源文错码做了撤回、重算并保留了新旧数字，这反而是积极诚信信号。

但我也不能签署“诚信无保留通过”：v7 把一个可被简单语义突变绕过的检查称为
`fail-closed reconciliation`，并声称 P0-3 已解决；同时改写已评审日期件。这是**方法学层面的
错误保证与可疑研究实践风险（QRP risk）**。在未修正前，任何基于这套流水线生成的 occupancy、
空位或创新性数字，都只能视为人工草编码的方向性快照，不能视为经过 lineage 保证的机器事实。

---

## 1. 审查对象、冻结点与可复核范围

| 项目 | 冻结值 |
|---|---|
| 被审文件 | `wiki/2026-07-18-system-first-research-proposal-v7-consolidated.md` |
| 仓库 HEAD | `87877f1ff3cd5f6ee3da95dcf751ad255eddb5f5` |
| 被审件 git blob | `e2d0d7b949431a095290e88ec02300a505a25cb2` |
| 被审件工作树 SHA-256 | `2c8c4fc10485097f880404bc8bc60f55075ef6e17d0fc999967819efad5dd01d` |
| 被审件长度 | 256 行 |
| 审查开始时工作树 | clean |
| 审查动作 | 只读检查、隔离副本重放、官方来源检索；未改团队源文件 |

本报告所称“v7”只指上述冻结对象。团队后续不得原位改写本报告或 v7 来“消除”意见；应提交新的
dated response / superseding artifact，并把修复 commit、blob、测试输出逐项钉定。

---

## 2. 多轮对抗式复审记录

### Round 1：阶段与文本内部一致性

检查问题：v7 是否把 Stage-1A 写成结果阶段？是否偷跑实验？Stage-2A 预告是否获得执行力？

结果：

- systematic query = 0 的声明与“第一条查询才进入 Stage-1B”一致；
- v7 没有把 11 条 known-item 快照冒充 systematic mapping 结果；
- 没有新增模型或 smoke；
- 创新点仍标为未锁定；
- Stage-2A 仅预告，不构成越阶段执行。

**Round 1：通过。**

### Round 2：纯净环境机器重放

我从冻结 commit 导出纯净副本，在 `wsl -d Ubuntu-24.04`、项目 Python 3.12 环境中重放：

- 九个 bundle-only 门禁；
- identity taxonomy v1、v2、v3；
- quantifier scan。

结果为 **13/13 进程退出码 0**，v3 报告为 9/9 PASS。它证明提交包在正确命令下可运行，且团队
给出的结构性通过结果可以复现。

但是，这只回答“测试会不会跑、既有 fixture 会不会过”，不回答“派生构念是否正确”“编码是否
忠于论文”。因此继续做语义突变。

### Round 3：构念对抗与语义突变

构造一条满足 strict、原生 omni、sequential 的记录：

- `signal_use=["select"]`；
- `decision_rights=["memory_write"]`；
- 没有任何证据说明选择分数控制 memory write。

现有 `derive()` 仍返回：

```text
is_reward_guided=True
is_s0_core_compatible=True
is_rq_sys_control_compatible=True
is_project_method_candidate=True
```

这直接推翻“RQ-SYS 派生式已机器表达因果控制”的完成态声明。

随后在隔离副本中对 ATLAS 编码做三处语义破坏：

- `paper_work_id: 2606.01667 -> bogus-work`；
- `core_io_modality: multimodal_in_text_out -> text_in_text_out`；
- `source_locator -> nonsense`。

`sf_identity_taxonomy_v3_test.py` 仍给出 **9/9 PASS**，occupancy 数字也不变。故 P0-3
“能发现错码”没有闭环。

**Round 3：失败，产生 Gate MAJOR-1 与 Gate MAJOR-2。**

### Round 4：论文谱系与遗漏检索

按以下交叉轴做定向检索和官方页核验：

- training-free / frozen / inference-time；
- sequential control / step-level verifier / refinement / stop / route；
- agentic TTS / verifier failure / trained boundary；
- multimodal / speech / omni；
- internal-state、logit 与 API-only 边界。

结论：v7 的主干文献广度已明显改善，上一轮指出的 PDR 原始论文、SWE-Replay、TRT 均已补入；
没有发现足以要求“重做整个 Stage-1A survey 设计”的新空洞。但发现一篇直接近邻未进入开局队列，
另有两篇高价值边界文献应显式编码，见 §7。

**Round 4：文献门不阻塞，但有 P1 补项。**

### Round 5：审计链与不可改写性

比较被审 v6 commit `04cf987` 与当前 HEAD：

```text
wiki/2026-07-18-system-first-research-proposal-v6-consolidated.md
39 insertions, 26 deletions
```

改动不是只加 tombstone，而是把 taxonomy v2、3/11 等被审内容原位替换成 taxonomy v3、2/11
以及新的 lineage 声明。v7 同时把 `v6@04cf987` 定义为被审历史状态，并说本件是更正后的干净重钉。
若如此，正确动作应是保持 v6 字节不变、让 v7 承载更正，而不是同时改写 v6。

**Round 5：失败，产生 Gate MAJOR-3。**

---

## 3. 上一轮整改中可以正式接受的部分

严厉审查不等于拒绝承认有效修复。以下整改成立，后续不应再反复重开。

### 3.1 PDR 源文错码已正确撤回

v7 已把 vanilla PDR 从 reward-guided selection 改为 random-K supply/context mechanism，并把：

- strict ∧ reward ∧ pool：3/11 撤回为 2/11；
- unique work：明确为 1/8；
- `#rtv`、`#pdr-random-k`、`#rtv-pdr-pipeline` 分行编码。

这与 [PDR 原始论文](https://arxiv.org/abs/2510.01123) 以及 Agentic Coding 中对 random-K 的使用
关系相容。此项接受。

### 3.2 Team of Thoughts 的 reward 身份降级基本合理

团队把离线校准标量与推理时内容内评价区分开，不再仅因有“evaluation”措辞就把其计入部署期
reward-guided 方法；同时补全题名。以当前 Stage-1A 证据，放入 profile-conditioned
orchestration boundary 是合理的保守编码。后续精读可再拆离线 profile 构造与在线 orchestration，
但不再作为本轮门禁。

### 3.3 K 池从系统身份必要条件降为机制分层是正确方向

项目第一创新点是外部控制平面上的 omni agentic system，K 池只是候选构造/选择机制之一，不能把
整个系统问题退化成 selector 论文。因此 v7 的三分派生：S0 core compatibility、RQ-SYS control
compatibility、二者合取，概念方向优于 v6。

### 3.4 拓扑政策 A 与严格敏感列并报可以接受

同一冻结核心的多角色、多调用被计作单核系统，是 owner 对研究对象的有效定义；同时保留 strict
single-call/single-core 敏感列，能避免把定义选择伪装成自然事实。此项不需要在 Stage-1A 再争论。

### 3.5 文献补链有效

[PDR 原始论文](https://arxiv.org/abs/2510.01123)、
[SWE-Replay](https://arxiv.org/abs/2601.22129) 与
[Test-time Recursive Thinking](https://arxiv.org/abs/2602.03094) 已进入 A.3，并被赋予不同的
方法/反例角色。上一轮对应遗漏可关闭。

---

## 4. Gate MAJOR-1：RQ-SYS 派生式没有表达“信号实际控制权利”

### 4.1 文本定义与机器定义不等价

v7 的文本声称：reward/评价反馈会作用于 route、retry、tool、supply、stop 等下一步动作权。
但脚本实际逻辑是：

```python
reward = lifecycle_is_online_or_terminal and form_is_reward and any_reward_use
rq = reward and control_horizon_is_sequential and any_decision_right
```

这里缺少最关键的谓词：

```text
exists valid causal edge: signal_use -> decision_right
```

因此，“有评分用于 select”与“系统另外拥有 memory_write 权利”就足以合成 RQ-SYS；评分不需要影响
memory_write。更严重的是，纯 terminal selector 只要在同一记录里挂上一个无关的 sequential
decision right，也可能被升级成完整系统控制候选。

### 4.2 这不是实现细节，而是研究身份的承重错误

`is_project_method_candidate` 决定：

- 哪些方法占据项目身份；
- “0/11 空位”是否成立；
- Stage-1C 的相邻工作与创新性判断；
- 后续复现 shortlist。

如果信号和控制权之间没有因果边，项目会把“末端打分器 + 无关 agent scaffold”误报为
reward-guided sequential control。这会系统性夸大最近邻占据，或在不同字段组合下制造假空位。

### 4.3 必须如何修复

不要再增加一个模糊布尔位。应把因果关系做成第一类机器记录，例如：

```json
"control_edges": [
  {
    "signal_use": "revise",
    "decision_right": "retry",
    "signal_lifecycle": "online_step",
    "source_locator": "...",
    "edge_semantics": "verifier feedback triggers another attempt"
  }
]
```

并建立显式、可审查的允许关系或关系类型。至少要区分：

| 信号用途 | 可能控制的权利 | 不能自动推出的权利 |
|---|---|---|
| revise | retry / branch | memory_write / route |
| stop_budget | stop | supply / select |
| supply | supply / branch | tool_call（除非有证据） |
| route | route / tool_call | retry |
| select / prune | 当选择决定后续分支时为 branch；只选最终答案时仍是 terminal | 任意 sequential right |

映射不能靠字段名相等猜测，因为现有行已有 `revise -> retry`、`prune/select -> branch/stop` 等不同
词汇。需要每条 edge 的 source locator 和语义裁决。

### 4.4 MAJOR-1 验收条件

- [ ] schema 新增可枚举、可定位的 signal-to-right `control_edges`；
- [ ] `is_rq_sys_control_compatible` 要求至少一条有效 edge，而非两个非空集合；
- [ ] 增加 disjoint killer：`select` + `memory_write` 无 edge 必须为 false；
- [ ] 增加 terminal-only killer：最终答案选择 + 无关 sequential right 必须为 false；
- [ ] 增加正控：`revise -> retry`、`stop_budget -> stop` 至少各一条为 true；
- [ ] 逐行复核当前 11 method paths 的 edge 证据；unknown 不满足；
- [ ] 重算 5/11、4/8、0/11；数字若变化，按机器结果更新，不维护旧数字；
- [ ] 由非实现者提出至少一个新语义反例，不能只由实现者自写自测。

---

## 5. Gate MAJOR-2：lineage reconciliation 是 presence check，不是错码发现链

### 5.1 v7 声称了什么

v7 多处使用以下完成态语言：

- `lineage reconciliation fail-closed`；
- `P0-3 可发现错码`；
- coding 行将在 sidecar 单写链中生成，消灭同类错误通道。

但实际 sidecar generator 尚不存在，v7 又把它安排为“Stage-1B 首周工具”。这意味着首批 mapping
准备依靠的仍是手工 coding v4，而不是已验收的单写投影。

### 5.2 当前 V7 实际只检查什么

当前脚本只验证：

1. fulltext ledger 中存在同 id 且带任意 `sha256` 的行；
2. `canonical_record_id` 指向的文件存在；
3. `#anchor` 字符串在文件任意位置出现；
4. lineage 字符串非空。

它不验证：

- `fulltext_ref.kind` 是否与实际来源类型相符；
- 记录 SHA 是否就是该论文、该版本、该对象的 SHA；
- coding 的模态、signal、rights、selection 等字段是否来自 canonical record；
- locator 是否能解析到具体段落、表、算法或行；
- `paper_work_id` 是否对应 canonical work；
- coder 与 adjudicator 是否是可识别且独立的角色；
- coding 行是否真由 sidecar 生成。

因此，`paper_work_id=bogus-work`、错误模态和 `source_locator=nonsense` 同时存在仍能 9/9 PASS，
不是偶然漏测，而是当前数据流根本没有“源记录字段 -> 投影字段”的可比对象。

### 5.3 还有四个会在 Stage-1B 扩容时暴露的问题

1. `V6` 检查把条件直接写成 `True`，所谓双分母/双政策持久化没有断言；
2. `n_paths` 分母硬编码为 `/11`，新增第 12 条 mapping 后会立即产生错误报表；
3. unique work 从 `method_path_id.split('#')[0]` 推断，而不是使用声明的 `paper_work_id`；这正是
   `paper_work_id` 被改错后计数不变的原因；
4. V1 强制恰好 11 行，只是已知样本快照测试，不是可接收 Stage-1B 批次的通用 validator。

### 5.4 双人语义裁决尚未被证明

11 行 coding 的 `coder` 全部为 `W1`。多数承重行的 `semantic_adjudicator` 也为 `W1`；其余使用
“v6 复审 + W1”等描述性字符串。`W1` 是工作组标签，不是可追责的 actor identity，也不能证明
编码者与裁决者独立。工具门禁不能把“字段非空”解释成“双人独立复核已完成”。

### 5.5 为什么 sidecar 必须在 Stage-1B 前完成

Stage-1B 的任务是批量获取、筛选、精读、编码和汇总。一旦第一批论文用旧手抄链录入，再补
sidecar，就会形成两种来源体系：首批需要迁移，迁移本身又会产生新错码，且 occupancy 的历史
变化难以区分“新发现”与“工具迁移”。

完成 sidecar/generator 是 Stage-1A 的 survey infrastructure 收口，不是 Stage-2 实验，也不会
造成阶段超前。把它前置不是苛求论文级完善，而是防止 mapping 开始后批量放大已知错误通道。

### 5.6 MAJOR-2 最小修复合同

#### A. 数据单写

- [ ] 为现有 8 works / 11 method paths 建立 canonical per-paper sidecar；
- [ ] sidecar 包含 paper/version/hash、method-path、原文 locator、编码字段、控制 edge、coder、
      adjudicator、裁决状态；
- [ ] coding v5 必须由 generator 从 sidecar 生成；禁止同一语义在 sidecar 与 coding 手工双写；
- [ ] generator 输出排序和字节稳定，重复生成零 diff。

#### B. 真 reconciliation

- [ ] 精确校验 id、kind、version、sha256 与 ledger 同一行绑定；
- [ ] `canonical_record_id` 解析到具体记录，而非“文件中出现过该字符串”；
- [ ] locator 必须可解析；页码/section/table/algorithm/quote-anchor 至少有一种机器可证存在；
- [ ] `paper_work_id` 必须与 sidecar/canonical record 一致；
- [ ] 所有派生字段都从 source fields 重算，禁止信任 coding 中自报派生值；
- [ ] 负控突变必须覆盖 wrong work、wrong modality、wrong signal、nonsense locator、wrong SHA、
      wrong kind，六项均应 fail closed。

#### C. 扩容正确性

- [ ] 分母使用 `len(rows)` 和真实 `paper_work_id` 去重，不得写死 11；
- [ ] 把 V6 的 `True` 替换成可失败断言；
- [ ] 增加 N≠11 fixture，例如第 12 行加入后报告自动变为 `/12`；
- [ ] validator 接受批次增量，但拒绝 method-path 重复、work 错绑和未裁决承重行；
- [ ] 当前 11 行通过“从 sidecar 生成 -> reconciliation -> occupancy”的端到端重放。

#### D. 人员/AI 协作可追责

- [ ] coder / adjudicator 使用稳定 actor id，不使用泛化 `W1`；
- [ ] 承重身份、空位和负结果行必须 `coder != semantic_adjudicator`；
- [ ] AI 可做首编或对抗复核，但须记录模型/会话或任务标识、输入来源和人工签署角色；
- [ ] unresolved disagreement 不得进入完成态 occupancy，只能进入 conflict queue。

---

## 6. Gate MAJOR-3：v6 日期件被改写，审计层 append-only 失守

### 6.1 事实

原始 v6 提交为 `04cf987`。后续 `70c1b04` 不仅新增整改材料，还直接改写：

```text
wiki/2026-07-18-system-first-research-proposal-v6-consolidated.md
39 insertions, 26 deletions
```

改写内容包括 taxonomy v2 -> v3、3/11 -> 2/11、新增 lineage 完成态声明和文献。也就是说，当前
路径上的“v6”已不是评审在 `04cf987` 看到的 v6。

### 6.2 风险

git 历史仍能找回旧字节，所以这不是证据销毁；但它造成三种不必要歧义：

- 引用“v6 某节”时，默认分支当前文本与历史评审文本不同；
- 后续 AI 若只读当前路径，会把整改后内容误当作原始送审内容；
- 团队可以在无意中形成“旧版本看起来从未犯错”的漂白效果。

v7 末尾已经写了“更正走 dated correction”。这条规则必须对 v6 本身生效，而不是只约束未来。

### 6.3 MAJOR-3 验收条件

- [ ] 以新提交把 v6 当前路径恢复为 `04cf987` 的原始 blob
      `2af5131830e2a50a579658c8163f96b87524bb81`；
- [ ] 不用 rebase/reset 擦除 `70c1b04`，保留事故与恢复动作；
- [ ] v7 继续作为更正后的 superseding artifact，不把修复重新塞回 v6；
- [ ] 在 v7/response 中用 `(commit, git-blob)` 指向被审 v6 和修复后 v7；
- [ ] 为 dated audit artifacts 增加只检测“已发布后是否被改写”的检查；检测到时失败并要求新日期件；
- [ ] 后续引用不得写裸路径 `v6 §4.2`，必须写 `v6@04cf987 §4.2` 或 superseded v7 的定位。

这项检查只要求在正确工作流下保持审计语义，不要求防御恶意篡改元数据；符合当前阶段重点。

---

## 7. 引用合理性与论文遗漏审查

### 7.1 总评：广度基本合格，claim-level 可追踪性仍不够

v7 的 45 条附录按 DEEPLY_READ、CALIBRATION、KNOWN_QUEUE、MEASUREMENT_INSTRUMENT 分层，
角色区分清楚；system/control 与 speech/omni measurement 没有混分母。这比罗列大书目更有研究价值。

但“自包含”仍有边界：§4.3 的 verifier/majority/self-refinement 负结果先验是承重内容，却只写
“locator = 矩阵”，没有在 v7 中给出 claim -> paper -> locator 的键。Stage-1A 不要求论文式完整
related work，但至少应让 reviewer 和下游 AI 能从每条承重先验跳到唯一矩阵行。建议在 v7 response
中提供 claim key 和 canonical record id，而不是继续堆散文引用。

### 7.2 P0：上一轮三篇谱系补链已完成

- [PDR 原始论文](https://arxiv.org/abs/2510.01123)：已加入并按机制拆行；
- [SWE-Replay](https://arxiv.org/abs/2601.22129)：已加入相邻系统队列；
- [TRT](https://arxiv.org/abs/2602.03094)：已作为无外部反馈替代解释。

本轮不重复要求。

### 7.3 P1：直接近邻遗漏，必须进入 Stage-1B 开局队列

**[Step-level Verifier-guided Hybrid Test-Time Scaling for Large Language Models](https://aclanthology.org/2025.emnlp-main.931/)**
(Chang et al., EMNLP 2025) 明确研究 training-free TTS，并以 process verification 引导
conditional step-level self-refinement，再与 parallel scaling 组合。它与 RQ-SYS 的“反馈是否改变
后续 retry/branch/stop”高度贴合，比若干泛化 TTS 队列项更接近控制边。

要求：加入 opening queue，并至少拆两条 method path：conditional sequential refinement 与 hybrid
parallel/sequential composition；重点编码 verifier 是否训练、信号到权利的 control edge、是否需要
内部状态、是否使用 labels。它是 **P1 carry-forward**，不是基于摘要直接判定项目占据。

### 7.4 P1：内部可见性 / 非 API-only 边界队列

以下两篇不一定占据 TF-Strict，但对“黑盒假设究竟排除了什么”很重要：

- [RFG: Reward-Free Guidance](https://arxiv.org/abs/2509.25604)：用 enhanced/reference dLLM 的
  log-likelihood ratio 参数化轨迹 reward；inference-time 无显式 reward，但依赖内部概率与增强模型
  来源。应作为 implicit-reward / internal-access / upstream-training 边界；
- [Depth-Entropy Guided Sampling](https://arxiv.org/abs/2607.09693)：用 layer-wise entropy collapse
  作为 pseudo-reward 并做 MCMC sampling。它是 training-free，但明确需要内部层状态，故很可能在
  `internal_visibility=api_only` 上出界；恰好可检验 taxonomy 的边界一致性。

要求：登记为 KNOWN_QUEUE/BOUNDARY，不因“training-free”标题直接计入 project method。

### 7.5 P1：负结果先验的已知来源应显式回链

[Evaluating the Role of Verifiers in Test-Time Scaling for Legal Reasoning Tasks](https://aclanthology.org/2025.nllp-1.15/)
已经出现在仓库早期审计材料中，研究 outcome-level BoN 与 process-level tree-search verifier 在低 N、
不同模型/监督类型下的效用。它不是本轮新发现，却没有进入 v7 附录。若 §4.3 继续使用
“majority/self-consistency 可能不弱于 verifier”等负结果先验，应把该 paper/claim key 显式连回，
避免“团队记得结论但开局队列忘了来源”。

### 7.6 非阻塞但应改进的编码轴

PDR random-K 当前设 `selection_object=none`，能避免把随机采样误计为 reward selector，但也丢失了
“存在候选池、只是随机选”的事实。建议拆成：

- `candidate_pool_exists: true/false/unknown`；
- `selection_policy: none/random_sample/scored_select/consensus/...`；
- `reward_guided_selection: derived`。

这样既不会恢复错误的 3/11，也能让 random-K 成为公平机制基线。

### 7.7 文献门最终裁定

**未发现必须重做 Stage-1A 文献协议的系统性漏域。** 一篇直接近邻和三项边界/回链补项可以在修复
门禁后作为 Stage-1B opening batch 的固定首批，不应成为无限 survey 的借口。当前真正的问题已经
从“书目广度不足”转移到“编码与派生链是否可信”。

---

## 8. 是否有超越当前阶段的探索尝试

### 8.1 没有发生的越阶段行为

- 没有运行模型或 smoke；
- 没有把 known-item 11 paths 写成系统性 survey 结论；
- 没有锁定创新性或论文 claim；
- 没有执行 Stage-2A reproduction；
- 没有设资源预算 cap 来提前压缩探索空间。

因此 v7 在**活动层面没有越阶段**。

### 8.2 有两处需要收紧的“完成态语言”

以下不是实验越阶段，而是证据等级超前：

- 把 presence-only check 称为 `fail-closed reconciliation`；
- 把“sidecar 将在 Stage-1B 首周实现”与“P0-3 已关闭”同时写入完成态。

在修复前，应改称：`LINEAGE_FIELDS_PRESENT / SEMANTIC_RECONCILIATION_PENDING`。Stage-1A 可以设计
future Stage-2A blueprint，但不能把尚未存在的工具作为已关闭证据。

---

## 9. 科研诚信与“是否涉嫌学术欺诈”的严格判断

### 9.1 目前支持诚信的证据

- PDR 错码被公开撤回，3/11 改为 2/11，没有维持有利旧数字；
- ToT reward 身份被保守降级；
- systematic query = 0、历史 model exposure、evidence grade 均有降级表述；
- v7 没有把 0/11 宣称为已证创新点。

这些行为不符合“蓄意维持虚假有利结论”的典型模式。

### 9.2 目前不能接受的诚信风险

- 检查名和 prose 宣称超出了检查能力，产生 false assurance；
- coder/adjudicator 身份不独立却容易被读成已双审；
- 日期件被原位改写，会让默认分支上的历史错误消失；
- 机器 PASS 与语义正确被反复并置，容易让下游 AI 把结构测试误当事实核验。

### 9.3 定性

**没有证据足以指控学术欺诈；存在需要立即整改的 QRP / research-governance 风险。**

如果团队收到本轮语义反例后仍继续对外宣称“可发现错码、fail closed”，或继续原位改写已评审日期
件而不披露，则风险性质会从工具能力不足上升为明知证据不足仍作完成态陈述。当前不作该推定。

---

## 10. 给研究团队 AI 的明确整改协议

### 10.1 禁止动作

1. 不得运行研究模型、smoke 或效果实验；
2. 不得原位改写 v7、本报告或其他已评审日期件；
3. 不得用“9/9 PASS”单独回答语义错码问题；
4. 不得为了维持 5/11、0/11 而调整规则；先冻结语义，再接受重算结果；
5. 不得把新增文献从摘要直接编码成项目占据；
6. 不得以继续扩书目代替修复 generator/reconciliation。

### 10.2 必须按顺序完成

#### Step A：恢复审计层语义

- 恢复 v6 当前路径为 `04cf987` 原始字节；
- 新增 dated response，记录错误发生、发现、影响和修复 commit；
- 加 audit-artifact immutability check。

#### Step B：修正 RQ-SYS 因果派生

- 定义 `control_edges` schema；
- 逐条给现有 11 paths 补 locator；
- 加 disjoint/terminal-only killer；
- 重算 occupancy。

#### Step C：完成单写 lineage 流水线

- canonical sidecar -> generator -> coding v5 -> reconciliation -> occupancy；
- 去除 `/11` 和 method_path 前缀推 work 的写法；
- 六类 semantic mutation 全部 fail；
- 端到端重复生成零 diff。

#### Step D：补 opening queue，不重开 proposal

- 加入 Step-level Hybrid TTS；
- 加入 RFG、DEGS 边界；
- 把 legal verifier 负结果先验连到 claim key；
- 不因此改写研究北极星或扩大为实验计划。

#### Step E：提交复审包

复审包至少包含：

- 新 dated response；
- 修复 commit 与每个承重文件的 git blob；
- old/new taxonomy 字段 diff；
- 11 path 的 control-edge 对账表；
- sidecar/generator/reconciliation 的数据流说明；
- 六类突变结果和一个 N≠11 扩容结果；
- 重算 occupancy，不手抄数字；
- v6 恢复证明；
- `systematic query=0`、`new model touches=0` 的签署声明。

### 10.3 回应格式

每条 reviewer item 必须采用：

```text
Finding ID
Disposition: ACCEPT / PARTIAL / DISPUTE
Root cause
Changed artifact + commit + git blob
Machine check and exact result
Adversarial negative control
New derived numbers
Residual risk / unresolved item
```

`DISPUTE` 必须给出源文 locator 或可运行反例；“我们认为”“测试已绿”不构成证据。

---

## 11. Stage-1B 放行矩阵

| 门禁 | 当前状态 | 放行标准 |
|---|---|---|
| 阶段记账清楚 | PASS | 保持 query=0 至签署；Stage-1B 仍禁模型/smoke |
| 研究问题未越阶段锁定 | PASS | 保持 hypothesis-grade，不重开工作论文 claim |
| PDR/ToT 纠错 | PASS | 不再维护旧 3/11；保留源文定位 |
| 文献主干广度 | PASS_WITH_P1 | 四项补入 opening/boundary queue 即可 |
| RQ-SYS 因果构念 | **FAIL / GATE MAJOR-1** | disjoint 与 terminal killer 失败闭合；现有行有 control edge |
| semantic lineage | **FAIL / GATE MAJOR-2** | sidecar 单写链上线；六类错码突变均失败；N≠11 正确 |
| 审计日期件不可改写 | **FAIL / GATE MAJOR-3** | v6 恢复原 blob；新 dated supersession；immutability check |
| 科研诚信最终签署 | WITHHOLD | 三项 MAJOR 清零后再签；当前不作 fraud 指控 |

---

## 12. 最终决定

**v7 不是失败的 proposal。** 它已经把研究对象从“K 池 selector”纠正回“围绕冻结 omni 核心的外部
reward-guided sequential control plane”，也正确地把 Stage-1B 限定为 survey execution，而非模型
实验。PDR 数字撤回、ToT 降级、拓扑敏感列和文献补链均可接受。

但 v7 仍不是可安全批量执行的 survey system：身份派生缺因果边，lineage 检查不能发现语义错码，
审计日期件又被原位改写。若现在直接进入 Stage-1B，mapping 规模越大，错误放大越快，后续 1C
综合反而更难可信。

因此最终裁定为：

> **WITHHOLD Stage-1B。只阻塞于 Gate MAJOR-1、2、3。**
>
> 三项通过机器反例复核并由 owner 签署后，**可以开始 Stage-1B systematic mapping**；无需先跑模型，
> 无需先做 smoke，无需增加预算 cap，也无需重开已经裁定的研究北极星。第一条 systematic query
> 仍是 Stage-1B 的正式起点。
