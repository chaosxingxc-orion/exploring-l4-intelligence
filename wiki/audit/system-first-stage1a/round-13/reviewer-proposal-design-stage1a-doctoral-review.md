---
title: "Reviewer Proposal and Master Release Design：Stage-1A 尾门敌意博士级审查"
date: "2026-07-20"
review_role: "严格外审人 / 博士生导师 / 研究诚信与系统综述方法审计"
review_target: ".worktrees/stage1b-readiness-remediation/docs/superpowers/specs/2026-07-20-reviewer-proposal-and-master-release-design.md"
target_commit: "55e283c6f53459657b88e1586a999bd7d580cf81"
target_git_blob: "607a2d931e3e34a397813734b6cb4f0b9f275cae"
target_sha256: "509b1336717476dc81011544e3b01cd92a7fef6ced7dd9c55b293ce87dd0962d"
design_verdict: "REVISE_BEFORE_RELEASE"
stage1b_verdict: "WITHHOLD_STAGE1B"
gate_major_count: 3
integrity_verdict: "未发现 FFP；存在新 evidence-kind 假绿与完成态/授权措辞超过证据的风险"
scope_note: "只新增本日期审查件；未修改目标 worktree、团队 proposal、脚本、台账、manifest、git config 或远端状态"
---

# 一、结论先行

## 1.1 当前到底处于哪个阶段

当前仍是 **Stage-1A survey-ready gate**，不是 Stage-1B，也不是 Stage-1A 已结束：

1. `wiki/Research-Objective.md` 与 `wiki/survey/current/status.md` 都把当前门标为 Stage-1A；
2. 该整改范围内正式 discovery query、研究模型调用和 smoke 都为 0；
3. 当前活动是 schema/data repair、离线检查、审稿包设计和独立复审准备，均属于 Stage-1A；
4. Stage-1B 的第一条系统检索仍未执行；
5. protocol-v2 §0 要求同一 committed package 上同时具备独立 search-design sign-off、owner
   execution approval 与 P0-R8/package gate PASS，目前前两项明确不存在。

因此，被审设计把自身称为“完成最小 Stage-1A submission transaction”，并明确不授权
Stage-1B，这一阶段定位基本正确。

## 1.2 能否开始 Stage-1B

**不能。当前裁决为 `WITHHOLD_STAGE1B`。**

这不是要求继续无限 survey、增加 query universe、运行模型、设置预算 cap 或提前做 Stage-2
实验。阻塞已经收缩为三个边界清楚的 Gate Major：

| Gate | 发现 | 当前裁决 |
|---|---|---|
| G1：schema-v3 evidence-kind/value compatibility | `absence` 可以为任意正向类别值作“证据”；作者外合法重签后 0 failure，却可改变 RQ headline | **FAIL / GATE** |
| G2：正式审查对象与独立性原子性 | 当前只有 release design，没有最终 proposal、正式引用闭包或独立 reviewer report；`Approved design` 也没有授权 provenance | **NOT YET DELIVERED / GATE** |
| G3：既有论文集进入本轮 claim flow | 95-work census、62-row claim ledger、92-seed manifest 与 65-entry bibliography 没有逐 work crosswalk；current source flow 不能证明纳入或有理由排除 | **FAIL / GATE** |

Windows 与规范 WSL2 的 integrated package gate 都真实 PASS，v9 的 signal/edge
field-binding 主整改大体成立；本报告不重开已经闭合的双平台、same-signal 或 PDF strong-anchor
问题。

## 1.3 对设计件本身的裁决

设计方向可保留，但必须 **REVISE BEFORE RELEASE**。尤其不能把该设计文件本身当成：

- scientific-merit verdict；
- search-design sign-off；
- reviewer signature；
- owner execution approval；
- citation-complete research proposal；
- Stage-1B readiness verdict。

# 二、审查方法与证据冻结

## 2.1 冻结对象

- worktree HEAD：`55e283c6f53459657b88e1586a999bd7d580cf81`
- target git blob：`607a2d931e3e34a397813734b6cb4f0b9f275cae`
- git-blob SHA-256：`509b1336717476dc81011544e3b01cd92a7fef6ced7dd9c55b293ce87dd0962d`
- 审查期间目标 worktree 保持 clean。

本报告使用 git blob 字节冻结目标；工作树 CRLF 变体不作证据正典。

## 2.2 四轮敌意审查

### Round A：阶段与授权审查

对账：

- `Research-Objective.md`；
- `Project-Thesis.md`；
- current protocol/status/manifest；
- 被审 design 的 dual-verdict、merge/push 与 owner 授权描述。

### Round B：技术包作者外重放

- Windows：`python scripts/survey/sf_current_package_check.py --check` → PASS；
- WSL2 Ubuntu-24.04：激活 `~/.venvs/speechrl` 后同一命令 → PASS；
- 两次均为脚本声明的 zero-write check，之后 worktree 仍 clean。

一次未激活 venv 的 WSL 系统 Python 运行因缺少 `pypdf` 失败；这是错误执行环境，已明确排除，
不作为团队缺陷或失败证据。

### Round C：schema-v3 作者外正常录入反例

不是伪造文件或破坏 hash，而是模拟 Stage-1B 新行的正常重编码：更新字段、更新对应 evidence
value、合法重算 row hash，再运行 structure → binding → source 三层合同。

### Round D：引用与邻近工作复核

- 检查 target 自身是否含论文引用；
- 检查其 source flow 能否解析 P1/P2；
- 检查 generated bibliography 的 author/year/link 完整性；
- 通过 arXiv、ACL Anthology 等论文官方页核验直接近邻与边界工作。

本轮网页检索是 **reviewer-side claim verification / reviewer-known-item discovery**，不是团队
Stage-1B systematic query。团队若采纳新增论文，必须标 `REVIEWER_KNOWN_ITEM`，不得冒充 frozen
query recall，也不得用这些论文反向修改冻结 query terms。

# 三、设计中做对了什么

## 3.1 阶段与权限分离基本正确

设计明确区分：

1. scientific proposal judgement；
2. search-design sign-off；
3. owner execution approval。

并明确两个有利 reviewer verdict 仍保持 `execution_authorized: false`。这比过去把内部 PASS、
reviewer sign-off 与 owner approval 混写的做法严谨。

## 3.2 dual-track 架构有合理性

Track A 处理研究问题、贡献假设和 falsifier；Track B 处理 v9 整改、机器反例和 readiness。
物理上放在一个文件中可以降低 reviewer navigation 成本，只要两条 verdict 的证据和语义保持
严格分离。

## 3.3 证据流优先引用正典而非复制数字

设计要求数字、hash 与 PASS 取自机器报告，并明确 proposal 不维护第二份 numeric canon。这一
原则正确。尤其 reader-visible headline 应继续由 persisted report 生成，而不是手抄。

## 3.4 append-only 审计与 current-state 更新顺序合理

proposal、后续 reviewer report 分别作为 immutable artifact；当前层只记录 pending/结论，不改写
历史 proposal。这符合审计层 append-only、当前层 supersede-in-place 的分层纪律。

## 3.5 release 事故披露没有被隐藏

设计要求把 wiki dry-run 误入 publish path 的事故带入 reviewer package，并说明远端未变化。
这是正确的诚信处理，不应因事故已修复而从审稿包消失。

## 3.6 `core.worktree` 修复理由真实

只读核查发现共享 `.git/config` 的 `core.worktree` 当前确实指向 WSL 路径
`/mnt/d/.../.worktrees/stage1b-readiness-remediation`，导致 Windows 主工作树的 Git 根解析失败；
linked worktree 则能解析。删除错误的 shared `core.worktree` 属于真实环境修复，不是无关扩张。

但执行时仍应记录变更前值、变更命令与两工作树 postcondition；不要把 design 中一句“remove”
当成已经完成。

# 四、Gate Major 1：`absence` evidence 可以合法制造 headline 假绿

## 4.1 精确作者外反例

从当前 schema-v3 输入复制 `2026.findings-acl.1724#pipeline`，执行以下普通重编码：

1. `s_stage_judge.form: scalar_score -> text_critique`；
2. 将该字段 evidence 更新为：

```json
{
  "kind": "absence",
  "value": "text_critique",
  "note": "not contradicted",
  "scope": "paper full text"
}
```

3. 使用项目自身 `_restamp` 合法重算 row hash；
4. 使用项目自身 generator 重新生成 coding；
5. 运行 `validate_load_bearing_contract`。

结果：

```text
structure failures = 0
binding failures   = 0
source failures    = 0
```

但 headline 派生发生变化：

```text
is_rq_sys_control_compatible: 5/11 -> 4/11
```

这证明当前 v6 仍可能对影响 occupancy 的错误证据给出全绿。

## 4.2 根因

`sf_evidence_contract.py` 将 `absence` 与 `canon/tex/pdf_page` 并列为任何 required field 都可用的
evidence kind；`_check_evidence_entry_v6` 对 absence 只检查：

- `note` 非空；
- `scope` 非空。

它不检查：

- absence 是否只用于允许的负向/none/unknown 值；
- 正向 `signal.form=text_critique` 为什么能由“没有反证”推出；
- protocol-v2 §7 声明的 source version；
- evidence coder；
- reason 与 inspected scope 的结构化字段；
- absence 搜索是否覆盖声明的完整对象。

因此“value 与 evidence.value 一致”被错误地等同于“evidence 支持该 value”。

## 4.3 为什么这是 Stage-1B gate，而不是恶意脚本鲁棒性

该反例没有篡改已经注册的 row、没有绕过 hash，也没有使用非法命令。它模拟的是新论文第一次
编码时很自然的错误：对一个正向类别使用“未发现相反描述”作为证据，然后完成正常 adjudication
流程。

Stage-1B 会批量新增没有 per-ID expectation 的 method paths；如果这种输入能绿，system-control
occupancy、reward/RQ 分类与后续选题都可能被污染。因此它属于科学数据合同，不是攻击防御。

## 4.4 必须的窄修复

建立显式 `evidence_kind × field × encoded_value` 合法性矩阵：

1. 正向类别值原则上只允许 `canon|tex|pdf_page`；
2. `absence` 只允许语义上可由完整检索支持的负向、空值或 `unknown/none`；
3. 对允许的 absence，强制 `encoded_value / inspected_scope / reason / source_version / coder`；
4. validator 必须拒绝“正向类别 + absence”，即使 row hash 合法；
5. 添加通用第 12 行反例，不依赖当前 11 个 ID；
6. 同时保留一个合法负向 absence 正控，避免修成“完全禁用 absence”。

验收必须包含：

```text
positive signal.form + absence -> FAIL
positive signal.source + absence -> FAIL
negative/none field + complete structured absence -> PASS
missing source_version/coder -> FAIL
上述 5/11 -> 4/11 反例在 derive 前被拦截
Windows current-package PASS
WSL2 venv current-package PASS
```

# 五、Gate Major 2：当前交付物不是可签署的 proposal，独立性合同也未落地

## 5.1 设计文件不是科学 proposal

目标共 142 行，是 document/release architecture，论文正式引用为 **0 条**。它没有实际给出：

- north-star 的完整论证；
- research gap 的论文证据；
- RQ 与贡献假设全文；
- falsifier 全文；
- 参考文献附录；
- reviewer verdict；
- reviewer identity/conflict declaration。

所以本轮最多能裁决“设计是否足以生产审稿包”，不能据此裁决 scientific merit 或 citation
correctness，更不能签 Stage-1B。

## 5.2 `Approved design` 缺少授权 provenance

文件头只写 `Status: Approved design`，没有：

- `approved_by`；
- `approval_time`；
- `authority_ref`；
- 获批 scope；
- source branch/head；
- expected remote/master pin。

但同一文件又把 merge/push 写进 scope，并使用“This authorization does not include ...”的授权
语气。AI 自己生成一份标记 `Approved` 的设计，不足以证明 owner 授权了对远端 `master` 的写操作。

这不是怀疑 owner 没有口头同意，而是审计载体无法让下一位 AI 区分“owner 批准”与“设计作者
自称已批准”。在补齐 provenance 前，不得仅凭此文件执行 push。

## 5.3 reviewer independence 只有名称，没有可执行合同

protocol-v2 要求 reviewer 独立于实现历史。当前 design 只反复写“independent reviewer”，没有定义：

- reviewer 与 implementation agent 的隔离标准；
- 是否参与过 schema/generator/fixtures 修改；
- review 输入的冻结 commit/blob 集；
- conflict-of-interest 声明；
- reviewer 使用了哪些额外网页查询；
- reviewer-known items 如何登记而不污染 query recall；
- reviewer report 的 immutable path/schema；
- 结论由谁签署、由谁确认 owner approval。

`/root/a6_adjudicator` 的 70/70 evidence adjudication 已明确不是 Gate-S1 reviewer sign-off，不能复用
其身份填补此空缺。

## 5.4 immutable proposal 中的“verdict fields”存在对象混乱

设计同时规定：

- proposal bytes 从 first commit 起 immutable；
- proposal 末尾放两个 reviewer verdict fields；
- reviewer report 以后作为另一 artifact append，永不改 proposal。

如果 proposal 不可改，里面的字段究竟是空模板、requested verdict schema，还是实际 verdict？若
reviewer 在后续报告写结论，proposal 内空字段会长期存在，容易成为第二状态源。

proposal 中应改名为：

```text
REQUESTED_SCIENTIFIC_CONTINUATION_JUDGEMENT
REQUESTED_SEARCH_DESIGN_SIGNOFF
```

实际值只存在于 reviewer report；current status 只从该 report 与 owner record 派生。

## 5.5 “scientific merit = ACCEPT”在 Stage-1A 语义过强

Stage-1B systematic mapping 尚未执行，Stage-1C 才进行证据综合与创新选择。此时 reviewer 可以
判断“问题是否重要、假设是否清楚、是否值得继续系统 mapping”，但不能用一个没有限定语的
`SCIENTIFIC_MERIT=ACCEPT` 暗示 novelty、有效性或博士贡献已经成立。

建议改为：

```text
SCIENTIFIC_RATIONALE_FOR_CONTINUING_MAPPING = ADEQUATE | REVISE | INADEQUATE
SEARCH_DESIGN_SIGNOFF = SIGN | WITHHOLD
```

并声明 `ADEQUATE` 不证明 first-ever、novelty、effectiveness、SOTA 或 Stage-1C 候选已存活。

# 六、引用与 literature survey 审查

## 6.1 target 的引用无法判为“合理”

因为 target 是 release design，论文引用为 0。它对 Project-Thesis、protocol、机器报告的内部
source routing 基本合理，但这不等于学术参考文献合格。

在最终 proposal 真正落盘前，任何“引用已闭合”都只是计划，不是证据。

## 6.2 source flow 漏掉实际承载 P1/P2 的文件

设计 §3 列出的 claim sources 没有包含：

- `wiki/survey/2026-07-19-sf-bibliography-v1.md`；
- `wiki/survey/2026-07-19-sf-stage1b-opening-tables-v4.md`。

但 v9 reviewer 要求的四项 P1 与六项 P2 正是由这两个数据件承载。当前
`wiki/survey/current/tables/opening-guarantees.md` 只有 11-path occupancy headline，没有论文角色表；
current manifest 也没有把上述 bibliography/opening-table v4 作为 current data source。

因此设计所说“Track B maps P1 and P2”目前缺少可解析 source path。必须在 proposal generator 或
manifest 中显式绑定，不得依赖下一位 AI 广泛搜索旧日期件。

## 6.3 P2 被误写成“requirements”会重新扩大 Stage-1A

v9 review 明确把 TangramSR、OrchRM、ToolRM、Agent-RRM、DuplexPO、Multi-Faceted
Interactivity Alignment 列为“Stage-1B 首批关注、但不阻塞开门”。

被审设计却把“P1 and P2 requirements”并列。若不加限定，P2 会被错误升级为 Stage-1A gate，
违反“完成窄整改后立即申请签署，不再无限扩张”的上一轮裁决。

正确写法：

- P1：提交前 metadata/role/route carry-forward 必须清零；
- P2：只登记为 Stage-1B priority queue，未全文编码不阻塞 sign-off。

## 6.4 所谓 self-contained bibliography 仍有 8 个作者占位符

现有 bibliography 有 65 个带链接的论文行，但以下 8 行作者仍写“登记待读（作者见官方页）”：

1. SDiaReward；
2. Mapping Smarter, Not Harder；
3. TangramSR；
4. OrchRM；
5. ToolRM；
6. Agent-RRM；
7. DuplexPO；
8. Multi-Faceted Interactivity Alignment。

protocol-v2 §9 要求 reviewer-facing artifact 自包含 author、year、stable link。把作者外包给“官方页”
不满足自包含。最终 proposal 提交前必须补齐正式元数据；这不要求做全文 Stage-1B coding。

例如官方页已经给出：

- Mapping Smarter：Wen-Kwang Tsao、Yao-Ching Yu、Chien-Ming Huang；
- TangramSR：Yikun Zong、Cheston Tan；
- OrchRM：King Yeung Tsang 等 8 位作者；
- ToolRM/Agent-RRM 可直接从 ACL Anthology BibTeX 生成。

## 6.5 进一步遗漏的直接近邻

以下工作未在当前 bibliography 中找到。它们不要求新开 query lane，也不要求 Stage-1A 全文编码；
但既然已被 reviewer 明确发现，必须进入 `REVIEWER_KNOWN_ITEM` carry-forward：

### P1-high：最终 proposal 至少登记角色、ID、route 与边界假设

1. **Reward-Guided Semantic Evolution for Test-time Adaptive Object Detection**
   （arXiv:2605.04531）

   training-free、无 backprop，以 reward-guided evolutionary search 改写 VLM text embedding。
   它不是 omni agent system，但直接占据“冻结多模态核心 + reward-guided inference-time control”
   的方法轴，是必须解释的 boundary comparator。

   官方页：https://arxiv.org/abs/2605.04531

2. **Agentic Reward Modeling: Integrating Human Preferences with Verifiable Correctness Signals
   for Reliable Reward Systems**（ACL 2025，`2025.acl-long.775`）

   RewardAgent 组合 preference、factuality 与 instruction-following signals，并用于
   inference-time best-of-N。它是“外部 reward 组合器/agentic evaluator”直接近邻；其训练路径
   使其主要是 boundary/measurement work，而不是 TF-Strict 占据。

   官方页：https://aclanthology.org/2025.acl-long.775/

3. **Toward Scalable Verifiable Reward: Proxy State-Based Evaluation for Multi-turn Tool-Calling
   LLM Agents**（ACL 2026 Industry，`2026.acl-industry.87`）

   它用 trace-derived proxy state 与 LLM judges 评价多轮 tool agent，直接关系到本项目 external
   control plane 的 trajectory reward、信息边界和可验证性。应放 measurement instrument / gold
   boundary，不进入 frozen-system method denominator。

   官方页：https://aclanthology.org/2026.acl-industry.87/

4. **UniSRM: A Unified Speech Reward Model for Reasoning-Based Fine-grained Assessment**
   （arXiv:2605.23261）

   这是覆盖 utterance quality 到 context coherence 的 unified speech reward model，正好补充
   omni/speech evaluator 侧。它是 trained RM，属于 measurement/boundary，不是 TF-Strict 方法。

   官方页：https://arxiv.org/abs/2605.23261

### P2：Stage-1B 理论与资源分析优先队列，不阻塞开门

5. **On the Power of (Approximate) Reward Models for Inference-Time Scaling**
   （arXiv:2602.01381）

   它把 approximate reward 的 Bellman error 与 SMC inference scaling 的复杂度联系起来，可作为
   reward error / control stability 的理论邻近项。

   官方页：https://arxiv.org/abs/2602.01381

6. **Multi-Agent Reasoning Improves Compute Efficiency: Pareto-Optimal Test-Time Scaling**
   （ACL 2026 SRW，`2026.acl-srw.1`）

   它比较 self-consistency、self-refinement、multi-agent debate 与 mixture-of-agents 的性能—计算
   Pareto 前沿。当前全力摸高阶段不应据此设置预算 cap，但它适合 Stage-1B resource comparator 和
   后期成本压降参考。

   官方页：https://aclanthology.org/2026.acl-srw.1/

## 6.6 是否需要再增加 query lane

目前没有足够证据要求修改冻结的 65 条 query：

- RGSE 可由 reward-guided/test-time/multimodal 方法轴捕获；
- RewardAgent 与 proxy-state reward 可由 reward/verifier/agent T1 route 捕获；
- UniSRM 可由 speech reward/measurement 的 venue route 与 citation chaining 捕获；
- 其余可作为 reviewer-known items 保证 DFS 入口。

正确动作是登记 known-item provenance，而不是看到新论文就反向调 query，避免 query 设计污染。

## 6.7 Gate Major 3：既有完整论文集没有进入可审计的 claim flow

用户进一步要求“以前收集到的整个论文集要充分利用”。这项要求是正确的，但必须把“充分利用”
定义为**逐 work 有处置、有理由、有 provenance**，而不是把所有旧论文机械塞进 proposal 参考文献。

公平地说，团队并非完全没有反扫旧库。`2026-07-15-gate-s1-own-library-sweep.md` 曾以零外部查询
扫描 12 个仓内来源，报告约 76 个 distinct IDs，并分成 STRONG 15、MEDIUM 23、WEAK 约 38；
其中一部分确实进入了 92-row seed manifest。这是有价值的 partial reuse，必须保留。问题在于该件
仍是约数分桶与代表项叙述，不是 canonical 95-work census 的逐项处置，也没有把旧 claim 的证据
等级、冲突和 final proposal 用途连接起来。因此它不能单独证明“整个论文集已利用”。

我对既有探索知识层做了只读机器对账，得到：

| 既有资产 | 当前机器事实 | 不能据此声称什么 |
|---|---:|---|
| canonical census v2 | 95 work rows；94 RESOLVED、1 UNRESOLVED；83/95 有版本钉 | 不能说 95 篇都已进入本轮 system-first 论证 |
| claim-ledger v2 | 62 rows、44 unique source keys、31 distinct census clusters；62/62 均 `double_review_pending=true` | 不能把旧 kill/occupancy/whitespace 判决当作已完成双审的定论 |
| claim-ledger 证据等级 | 35 FULLTEXT、20 ABSTRACT_ONLY、2 FULLTEXT_UNREACHABLE、5 SYNTHESIS_PENDING | 不能把 62 行合并叫“62 个全文验证结论” |
| claim-ledger discrepancy | 15 MATERIAL、2 CRITICAL、6 UNVERIFIED | 不能无条件复制旧散文结论或旧数字 |
| current seed manifest | 92 unique IDs（88 arXiv + 4 DOI） | 不能把 seed 数等同于既有论文集总量 |
| generated bibliography | 65 paper rows | 不能把 65 条称作全库闭包 |
| current fulltext ledger | 129 access events、38 unique arXiv IDs 有成功 PDF | 不能据此推断旧 census 未读；只能说旧库与当前全文台账未建立可解析关联 |

按 exact stable-ID 做 crosswalk，当前可见连接度为：

- census → seed：**13/95** work rows；
- census → bibliography：**3/95** work rows；
- seed → bibliography：**9/92** seed rows；
- seed 的 88 个 arXiv ID → current fulltext ledger：**19/88**；
- bibliography 的 47 个 arXiv ID → current fulltext ledger：**16/47**；
- census 的 83 个 arXiv ID → current fulltext ledger：**0/83**。

最后一项不代表旧论文没有被读过；旧 campaign 可能通过归档件、网页或此前 workflow 读过。它代表的
是更严重但更准确的问题：**现有 current data plane 无法把旧阅读证据连接到本轮 proposal claim。**

此外，seed manifest 中有 22 行标作 `census在库(题录+)`，但只有 **8/22** 能按 arXiv ID 精确命中
canonical census v2。seed 生成报告已经披露，另外 14 行是把“仓内已知”语义类推成该等级，而非
literal census membership。因此这个标签不能再被当作“旧 95-work census 已覆盖”的机器证据；
这不是欺诈，但若在 final proposal 中省略该限定，就会形成误导性覆盖叙述。

更直接地说，target §3 的 source flow 只写了泛化的 historical campaign index。current manifest
虽然纳入 seed manifest 与 current fulltext ledger，却没有纳入：

- `2026-07-14-canonical-census-v2/paper_works.jsonl`；
- `2026-07-14-claim-ledger-v2/claim_ledger_v2.jsonl` 及 version-pin overlay；
- `2026-07-19-sf-bibliography-v1.md`；
- `2026-07-19-sf-stage1b-opening-tables-v4.md`。

campaign audit index 也没有为上述论文数据件提供逐 work routing。下一位 AI 即使严格按 current router
工作，也不会自然看到这批旧论文。这说明问题不在“AI 忘性”，而在知识组织合同没有把旧库接入
本轮承重路径。

这一项构成第三个 Gate Major，但关闭方式必须保持 Stage-1A 边界：**零新 query、零模型、零 smoke、
零全文批量重读**。提交前只需生成一个可机检的 existing-corpus disposition table，并满足：

1. canonical census 的 95 个 `W-*` 每个恰好出现一次；W-0014 继续如实标 UNRESOLVED；
2. 92 个 current seeds、65 个 bibliography rows 与旧 campaign paper IDs 通过稳定 ID/alias 做 crosswalk，
   未能自动对齐者进入人工 identity queue，不静默合并；
3. 每个 work 至少记录：canonical/stable ID、version、来源 campaign、现有 evidence grade、当前 role、
   对应 RQ/proposal section、纳入或排除理由、下一阶段动作、claim locator、冲突/失效条件；
4. role 使用协议已有分区：`DEEPLY_READ`、`KNOWN_QUEUE`、`MEASUREMENT_INSTRUMENT`、
   `BOUNDARY/NEGATIVE_PRIOR`；无关项用 REC-0 的排除理由登记，不另造一套术语；
5. 旧 claim-ledger 中 15 MATERIAL、2 CRITICAL、6 UNVERIFIED 行不得静默承重；若本轮 proposal
   使用其 claim，必须显式采用更正后版本，并在 Stage-1B 按 code-on-use 升到相应深度；
6. proposal 正文只引用真正承重的最小子集；全库处置放机器表/附录，防止 citation stuffing；
7. checker 证明 census 95/95 有处置、seed 92/92 有去向、bibliography 65/65 有来源角色、零 unexplained
   orphan，并输出 exact-ID 与 cross-ID/alias 两类去重统计；
8. 处置表、生成器版本、输入 blobs 与输出 hash 被 final proposal/source manifest 显式绑定。

这才叫充分利用：相关论文进入论证，不相关论文留下可审计排除理由，旧负结果进入 falsifier/negative
prior，旧测量工作进入 evaluator/measurement 设计，旧理论进入 hypothesis lineage；任何旧 evidence
都保留原产生阶段与证据等级，不因被新 proposal 引用而自动升级。

在上述 crosswalk 完成前，团队可以说“已建立 95-work census、92-seed current manifest 与 65-entry
review bibliography”，但不能说“历史论文集已充分纳入本轮 proposal”。

# 七、研究范围是否越过当前阶段

## 7.1 没有实验性越阶段

设计明确禁止：

- research-model call；
- model smoke；
- dataset experiment；
- prototype；
- 新 query universe；
- Stage-2 directional experiment。

merge、push、manifest、审稿包与离线 validator 都是 Stage-1A packaging/governance，不是
Stage-1B mapping 或 Stage-2 实验。因此没有“触碰模型”的越线。

## 7.2 存在表述性与流程性超前

以下不是实验越线，但会把 Stage-1A 证据说得过强：

1. 用 `SCIENTIFIC_MERIT=ACCEPT` 暗示博士贡献已确认；
2. 新建大而全 proposal，却不提供相对 v9 的 claim-diff，可能重新移动 scientific target；
3. 把 P2 priority queue 升级成 Stage-1A requirements；
4. 用无 provenance 的 `Approved design` 承载 merge/push 授权。

## 7.3 Track A 必须是受控 consolidation，不是重启 proposal

上一轮明确要求“不再提交宏大重写；只交窄整改、P1 与机器反例”。如果为了上下文自包含确实要
形成一个 consolidated reviewer artifact，可以接受，但必须附机器或人工 claim-diff：

| 字段 | 要求 |
|---|---|
| v9 claim ID/section | 原始主张定位 |
| disposition | UNCHANGED / CORRECTED / WITHDRAWN / NEW |
| rationale | 为什么变更 |
| evidence source | 正典 path + hash/locator |
| stage force | hypothesis only / readiness only |

没有 diff 的“新 proposal”会引入新的 citation、scope 与 wording 漂移，迫使 reviewer 从头审查，
反而违背 speed constraint。

# 八、release 与审稿事务的额外治理问题

## 8.1 将 review submission success 与 remote push success 分层

当前 success criteria 同时包含 proposal 注册、current state 更新、双端 gate、merge 和 push。
建议明确四个状态：

1. `PACKAGE_READY_FOR_REVIEW`；
2. `SUBMITTED_FOR_INDEPENDENT_REVIEW`；
3. `REVIEWED_SIGN_OR_WITHHOLD`；
4. `OWNER_AUTHORIZED_STAGE1B`。

远端 push 失败只说明 release 未完成，不自动否定 scientific rationale；reviewer WITHHOLD 也不应
被一个成功 push 掩盖。

## 8.2 分支分叉需要显式 pin 和 stop condition

只读检查时 remediation branch 相对本地 `master` 为 ahead 78 / behind 22，merge base 为
`4af90521...`。设计已经要求 fetch/reconcile 与 non-force push，这是正面措施；但执行记录仍应钉定：

- source head；
- fetched `origin/master`；
- merge base；
- merge result；
- registered artifact count/hash；
- merge 后 gate report；
- remote ref read-back。

若这些值与获批设计不一致，应停下重新确认，而不是把“normal merge”当作开放授权。

## 8.3 Stage-1B 最终启动还需要单独的同包事务

本设计只做到“提交审查并发布 master”。即使该事务成功，也仍需要：

1. 独立 reviewer report 写入不可变审计件；
2. search-design verdict = SIGN；
3. owner 对该 exact reviewed package 明确授权；
4. 在含 reviewer/owner 状态的最终 committed package 上重跑 P0-R8/package gate；
5. 确认 `execution_authorized: true` 与三项证据指向同一包；
6. 才能执行第一条 discovery query。

因此设计执行成功和 Stage-1B 开始之间仍有一个合法的 follow-on transaction，不能合并成一句
“proposal pushed, therefore Stage-1B ready”。

# 九、研究诚信判断

## 9.1 未发现学术欺诈或 FFP

本轮没有发现：

- fabricated paper；
- fabricated experiment/result；
- 隐藏模型运行；
- 篡改已注册审计 artifact；
- 把工具检查包装成研究效果；
- 远端 push 成功的虚假声明。

相反，团队主动撤回 v10 的过强 E1-E5 closure wording，披露 wiki dry-run incident，并保留
Stage-1B unauthorized 状态。这些是正面诚信行为。

## 9.2 但 false-assurance 风险仍然存在

如果在收到本报告的 absence 反例后仍声称：

- “所有 evidence kind 均语义 fail-closed”；
- “schema-v3 已能保证任意新行证据正确”；
- “14/14 PASS 等于 search-design signed”；
- “Approved design 等于 owner push authorization”；
- “design 文件已完成 citation review”；

则会构成明显的完成态夸张/QRP 风险。

当前更合理的结论是：技术团队完成了高质量的大部分整改，但 evidence kind 合法性矩阵与正式
review transaction 尚未闭合。这不足以推断主观欺诈。

# 十、有限整改与验收计划

## P0-A：关闭 absence 假绿

1. 实现 evidence-kind/value compatibility matrix；
2. structured absence 强制五字段；
3. 添加正向类别 + absence 失败反例；
4. 添加合法负向 absence 正控；
5. 证明 `5/11 -> 4/11` 反例在 derive 前失败；
6. 双平台 current-package PASS。

## P0-B：修订 reviewer proposal design

1. `Approved design` 增加 owner/authority provenance，或降级为 `Proposed design`；
2. dual verdict 改成 requested-response schema；
3. scientific verdict 限定为“是否值得继续 mapping”；
4. 明确 reviewer independence、输入 snapshot、冲突声明与报告路径；
5. 增加 v9 claim-diff，禁止无记录的 novelty/scope 新主张；
6. 明确 P1 为提交门、P2 为非阻塞 Stage-1B queue。

## P0-C：让正式 proposal 的引用闭包可检查

1. source flow 显式绑定 bibliography-v1 与 opening-tables-v4，或生成等价 current artifact；
2. 8 个作者占位符全部补齐；
3. 每项包含 title、author、year、stable link、role、provenance；
4. 新增四个 P1-high reviewer-known items；
5. 新增两个 P2 queue items但不阻塞；
6. 加 checker：reviewer-facing proposal 不允许“作者见官方页/登记待读”占位符；
7. 生成 existing-corpus disposition table，把 census 95、seed 92、bibliography 65 与旧 campaign IDs
   逐项 crosswalk；相关项承重、无关项有 REC-0 排除理由，零 unexplained orphan；
8. 把 census v2、claim-ledger v2、version-pin overlay、disposition table 与生成 hash 纳入 source flow；
9. 对旧 ledger 的 MATERIAL/CRITICAL/UNVERIFIED claim 禁止无条件继承；
10. numeric claim 仍必须有 page/table/figure locator。

## P0-D：完成真实审查事务

1. 生成并冻结 self-contained proposal；
2. 注册 proposal blob/hash；
3. 独立 reviewer 对 frozen package 出具 separate immutable report；
4. reviewer report 中分别给出 continuation judgement 与 search-design signoff；
5. 若 SIGN，再由 owner 单独授权；
6. 最终同包重跑 gate 后才能开始 Stage-1B。

## 明确禁止的无关扩张

- 不增加研究模型或 smoke；
- 不执行 dataset experiment/prototype；
- 不重新设计 65-query universe；
- 不因为 P2 队列未全文精读而阻塞；
- 不重开 same-signal、Windows/WSL、PDF strong-anchor 已通过项；
- 不做恶意元数据攻击防御；
- 不再新建宏大 amendment chain。

# 十一、放行矩阵

| 审查项 | 证据状态 | 裁决 |
|---|---|---|
| 当前阶段 | current hot layer + protocol-v2 | Stage-1A |
| discovery/model/smoke 边界 | 本整改 scoped 0；inherited exposure 保留 | PASS |
| Windows integrated gate | zero-write rerun | PASS |
| WSL2 Ubuntu-24.04 venv integrated gate | zero-write rerun | PASS |
| v6 row16/signal4/edge2 value binding | 现有 tests 与 package | MOSTLY PASS |
| evidence-kind/value compatibility | 正向 form + absence 全绿，RQ 5/11→4/11 | **FAIL / GATE** |
| PDF strong-anchor | 现有 v6 反例与双端重放 | PASS，不重开 |
| release prose binding | generated block + current release checker | PASS，不重开 |
| design stage boundary | 明确不授权 Stage-1B | PASS |
| design authorization provenance | `Approved design` 无 approved_by/authority_ref | **FAIL / GATE** |
| final reviewer-facing proposal | 尚未生成 | **MISSING / GATE** |
| reviewer independence contract | 只有名称，无操作合同 | **FAIL / GATE** |
| target citations | 0；仅为 release design | 不可作 citation sign-off |
| bibliography metadata | 65 链接行，8 author placeholders | REQUIRED CORRECTION |
| 旧 census → current seed | exact stable-ID 仅 13/95；无逐 work 处置表 | **FAIL / GATE** |
| 旧 census → bibliography | exact stable-ID 仅 3/95；其余无纳入/排除理由 | **FAIL / GATE** |
| 旧 claim-ledger 成熟度 | 62/62 double-review pending；15 MATERIAL + 2 CRITICAL | 只可导航/有条件复用 |
| existing-corpus source routing | current manifest 未绑定 census/claim ledger/bibliography/opening v4 | **FAIL / GATE** |
| v9 P1 carry-forward | 数据件存在但 design source flow 未绑定 | REQUIRED CORRECTION |
| P2 角色 | 应为非阻塞 priority queue | design wording 需改 |
| 新 query lane | 未发现必要性 | NO CHANGE |
| 是否越实验阶段 | 无模型/smoke/prototype | NO |
| 是否发现 FFP | 无 | NO FINDING |
| 是否可开展 Stage-1B | 三项 Gate Major + 正式审查/owner 记录缺失 | **WITHHOLD** |

# 十二、给研究团队 AI 的强制执行摘要

1. 不要把本设计文件包装成 final proposal 或 reviewer verdict。
2. 不要因 Windows/WSL 已 PASS 就声称 search design 已签署。
3. 修复 `absence` 适用域；必须复现并击杀本报告的 5/11→4/11 反例。
4. 不要把“evidence.value 相等”写成“evidence 语义支持 value”。
5. 不要把 P2 priority queue 升级为 Stage-1A gate。
6. consolidated proposal 必须提供相对 v9 的 claim-diff，不能再次移动审稿对象。
7. bibliography 的 8 个作者占位符在 reviewer-facing release 前必须清零。
8. reviewer independence 必须能由记录验证，不得只写一个形容词。
9. `Approved design` 必须有 owner authority provenance；否则改成 proposed。
10. proposal 只声明 requested verdict；真实 verdict 只写在独立 reviewer report。
11. owner approval 在 reviewer sign-off 之后单独发生，并在最终同包上重跑 gate。
12. 不得只引用最新 65 条而遗忘旧 census/ledger；先做 95/92/65 的零查询 crosswalk 与逐 work 处置。
13. “充分利用”不等于全引：正文只放承重子集，排除项必须有理由，旧 evidence 不自动升级。
14. 完成这些窄项后立即复审，不得以“还可能有论文”为由无限延长 Stage-1A。

# 十三、最终导师意见

这份 release design 的优点是明显的：它理解了内部技术 PASS、独立 search-design sign-off 与
owner execution authority 不是一回事；它保留 incident、append-only 审计与双平台重放；它也
没有越线运行模型实验。

但它现在仍只是“如何提交审查”的设计，而不是可以被签署的研究 proposal。更重要的是，v6 的
field-value binding 仍没有解决 evidence kind 的语义适用域：一个正向 signal form 可以只靠
“未发现反证”的 absence entry 绿灯，并真实改变 RQ-SYS headline。这个反例发生在正常新行录入
流程，不是恶意攻击，因此必须在 Stage-1B 规模化之前关闭。与此同时，旧 95-work census、62-row
claim ledger、92-seed manifest 与 65-entry bibliography 尚未形成逐 work 可审计 crosswalk；因此
当前也不能证明历史论文集已被本轮 proposal 有意识地吸收或排除。

最终裁决：

> **当前仍为 Stage-1A survey-ready gate。Windows/WSL integrated package 与既有 v9 主整改大体
> 通过，但 absence evidence 假绿、历史论文集逐 work 对账、正式独立审查事务三项尚未闭合，因此
> Stage-1B 暂不放行。完成 P0-A/B/C/D 后应立即进行一次窄幅独立复审；若 search-design SIGN、
> owner 随后明确授权且最终同包 gate PASS，即可开始第一条 Stage-1B systematic query。**
