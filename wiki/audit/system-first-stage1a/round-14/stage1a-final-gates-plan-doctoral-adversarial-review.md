---
review_id: "STAGE1A-FINAL-GATES-PLAN-DOCTORAL-ADVERSARIAL-REVIEW-2026-07-20"
date: 2026-07-20
review_object: ".worktrees/stage1b-readiness-remediation/docs/superpowers/plans/2026-07-20-stage1a-final-gates-and-reviewer-proposal.md"
review_object_commit: "17e230f673ee27efb5e74f6fbfab15c7061d22da"
review_object_git_blob: "8081134013e5e47f2bb5b9cdf1e770a1276fd972"
review_object_sha256_git_blob_bytes: "3113be10560fecf8402edff0e28c111621a66d1d4cfbc551f7965988c560d926"
review_scope: "Stage-1A 收口实施计划、既有论文资产利用、引用闭包、证据合同、阶段边界与 Stage-1B 放行"
reviewer_posture: "严格审稿人 + 博导；作者外只读复核"
plan_verdict: "MAJOR_REVISION_BEFORE_EXECUTION"
stage1b_verdict: "WITHHOLD"
integrity_verdict: "NO_CURRENT_EVIDENCE_OF_FFP; MATERIAL_FALSE-ASSURANCE_RISK"
source_mutation: "NONE"
---

# 2026-07-20 Stage-1A 最终 gates 实施计划：博导式敌意复审

## 一、结论先行

### 1.1 当前到底处于哪个阶段

**当前仍是 Stage-1A survey-ready gate 的最终整改与送审准备期，Stage-1A 尚未正式关闭，Stage-1B 尚未开始，也未获授权。**

判断依据不是“是否碰过代码”，而是研究动作的语义：现行阶段正典规定，Stage-1A 负责问题与 survey 设计、纳排与编码合同、静态/变异测试和放行包；Stage-1B 才执行 systematic mapping；Stage-1B 全程禁止研究模型与 smoke；Stage-2A 才从最接近公开 prior 的复现开始。被审计划的全部任务仍是证据合同、旧库桥接、bibliography、proposal、审计索引和 release 治理，没有运行 systematic query，也没有模型、数据集指标、smoke 或方向性原型。因此，它没有实验性越阶段。

但要特别区分三件事：

1. “Stage-1A 整改计划已经写出”；
2. “Stage-1A 整改已经实施并通过作者外复核”；
3. “独立审稿人签署 search design，owner 对同一冻结包授权 Stage-1B”。

当前只达到第 1 项。计划中所有 task 仍是未执行 checkbox；计划自己也把 round 15 留给未来的独立审查。因此，任何“Stage-1A 三个 gate 已关闭”或“Stage-1B ready”表述都早于证据。

### 1.2 对该计划的总裁决

**`MAJOR_REVISION_BEFORE_EXECUTION`。**

这份计划比上一版设计显著进步：阶段/权限分离、冻结 query、禁止模型与 smoke、保留 evidence-v6、为 round 15 留出独立审查对象等都写对了。然而，计划新引入的若干机器闭环自身仍可能产生“假绿”，其中至少四项是 gate major：

| ID | Gate major | 当前后果 |
|---|---|---|
| GM-1 | legacy-corpus bridge 的单位与 schema 有损 | 可在丢失/压扁旧论文证据的同时报告 `unexplained_orphans=0` |
| GM-2 | `absence` 只检查非空外形，未作 field-specific 与跨引用绑定 | 不相干的 provenance、弱“未见”证据仍可能支持承重 absence |
| GM-3 | evidence-v7 的 canonical aggregate 与双平台生成顺序错误，且 WSL linked-worktree 当前不可用 | “Windows/WSL 一致”可能根本未由 canonical report 证明；计划会在 Task 10 前先失败 |
| GM-4 | bibliography 的正确性 oracle 自我循环，且系统主线旧论文未进入 reviewer-visible closure | 可做到“零占位符”，却仍然引用错误或 system-first 论证失衡 |

此外还有 Git 基线混用、`git diff --check` 检查范围无效、reviewer-known input 未冻结等重要 P1 问题。

### 1.3 是否可以开展 Stage-1B

**不可以，裁决为 `WITHHOLD`。**

这不是否定研究方向，也不是要求 Stage-1A 提前完成 Stage-1B 的全文 mapping。理由很具体：当前计划尚未整改和执行；round-14 proposal 尚未生成；round-15 独立审查尚不存在；owner 尚未对同一冻结 package 明确授权；而计划中的若干 checker 还不能证明其声称的性质。

允许团队继续的唯一工作是 **Stage-1A 窄整改**：修订本计划、实现并验证这些 gate、提交 round-14 请求、接受 round-15 独立审查。第一条 systematic discovery query 必须继续保持未执行。

### 1.4 研究诚信结论

**目前没有足够证据指控 fabrication、falsification 或 plagiarism（FFP），也不应把实现缺陷直接定性为学术欺诈。** 计划主动披露 inherited exposure、wiki dry-run 事故、未签署状态，并禁止 `first-ever`、`SOTA` 和把贡献假设写成结果；这些都是正向诚信信号。

但存在显著的 **questionable research practice / false-assurance 风险**：如果在已知 schema 会压扁冲突、canonical report 未聚合双平台、bibliography metadata 由同一硬编码同时充当事实和 oracle 的情况下，仍发布“完整闭包、双平台一致、三 gate 已关闭”，则报告会超过证据能力。当前应称为“可修复的结构性风险”；若反例被明确告知后仍故意隐藏或继续用强完成措辞，诚信等级才应升级。

## 二、审查对象、冻结与方法

### 2.1 冻结对象

- 目标文件：`.worktrees/stage1b-readiness-remediation/docs/superpowers/plans/2026-07-20-stage1a-final-gates-and-reviewer-proposal.md`
- commit：`17e230f673ee27efb5e74f6fbfab15c7061d22da`
- Git blob：`8081134013e5e47f2bb5b9cdf1e770a1276fd972`
- 以 Git blob 字节计算的 SHA-256：`3113be10560fecf8402edff0e28c111621a66d1d4cfbc551f7965988c560d926`
- 文件规模：43,125 bytes，832 行。

本报告只读审查该冻结件及其依赖，没有修改被审 worktree、计划、脚本、正典或团队交付物。本文件是主工作区中新建的独立日期审查报告。

### 2.2 实际完成的四轮敌意复核

1. **阶段与授权轮**：对齐 `Research-Methodology`、`Research-Objective`、current status/protocol 和计划中的 task/stop condition，检查 Stage-1A、1B、1C、2A 是否被混用。
2. **合同与执行顺序轮**：逐项检查 absence、evidence-v7、proposal manifest、audit registry、Windows/WSL、merge/push 的输入、输出、oracle 和失败条件。
3. **作者外反例与旧库轮**：对 census、seed、bibliography、claim ledger、full-text ledger 做交叉核查；检查一篇 work 多 claim、多 evidence grade、多 conflict status 时计划的 schema 是否仍无损。
4. **引用与诚信轮**：先使用全部既有论文资产，再以官方论文页做定向外部核验；区分“库中已有但未路由”“当前 bibliography 缺失”“真正新增 reviewer-known item”；最后检查是否存在 FFP 证据或仅是 false-assurance 风险。

外部查到的论文只能登记为 `REVIEWER_KNOWN_ITEM` / provenance fetch，`query_recall_credit=false`；不得反向宣称 frozen query 已发现它们，也不得用本次审稿人的检索替代 Stage-1B systematic mapping。

## 三、这份计划已经做对的部分

以下进步应保留，不能在整改时倒退：

1. **阶段边界正确**：计划明确不改 65 条 frozen query，不碰 attempt registry，不运行研究模型、smoke、prototype 或 Stage-1B execution surface（计划第 69–76 行）。
2. **权限分离基本正确**：round 14 是 submission，round 15 才是独立 reviewer report；计划不得预填 `SIGN`，也不得由实现者创建 round-15 文件。
3. **历史证据保护正确**：evidence-v6 与 context-v1 保持字节不变，新结论另发 v7/context-v2；这符合审计层不改写原则。
4. **采用 fail-closed 和 mutation test 的方向正确**：不是只增加散文解释，而是要求反例、input binding、occupancy 和 package checker。
5. **旧论文集终于被提升为正式 gate**：Task 4 意图把 census、seed、bibliography、claim/full-text ledger 连接到 current knowledge flow，这是必要方向，且比仅“可重放”更接近真正的知识组织。
6. **没有把 P2 当作 Stage-1B 阻塞项**：计划区分 P1 closure 与非阻塞 P2 queue，避免 Stage-1A 无限扩张。
7. **release 操作本身不属于研究越阶段**：修 Git、合并、push 是工程发布行为，只要不借此写入 Stage-1B 已授权状态，就仍在 Stage-1A 范围内。

因此，本次裁决不是推翻架构，而是要求把“看上去可审计”修成“确实不会误报”。

## 四、GM-1：旧论文集 bridge 会有损压缩，`0 orphan` 不能证明充分利用

### 4.1 计划把不同层级错误地压成“一篇 work 一个单值 record”

Task 4 要求每个 census work 出现一次，并给出单值字段：`source_campaign`、`inherited_evidence_grade`、`role`、`conflict_status` 等（计划第 387–407 行）。但真实旧库不是一篇 work 对应一个同质判断：

- 62 个 claim rows 对应 44 个 unique sources；至少 12 个 work 有多个 claim row；
- 至少 7 个 work 同时具有多种 evidence grade，例如 `P-0031`、`P-0005` 同时出现 `ABSTRACT`、`FULLTEXT`、`FULLTEXT_UNREACHABLE`，`P-0080` 同时有 `ABSTRACT` 与 `FULLTEXT`；
- 至少 8 个 work 同时具有多种 discrepancy status，例如 `P-0071` 同时有 `MATERIAL`、`MINOR`、`NONE`，`P-0031` 同时有 `MINOR`、`NONE`、`UNVERIFIED`；
- 同一 work 还可能来自 census、seed、bibliography、claim campaign 多个入口。

因此，单个 `inherited_evidence_grade` 或 `conflict_status` 必须选择“最好”“最坏”或“任意一条”，无论选哪种都会丢信息。所谓“never upgraded”测试仍可能在降级、冲突消失或来源覆盖丢失时通过。

### 4.2 role taxonomy 与现行 protocol 不一致

计划第 407 行允许 `BOUNDARY/NEGATIVE_PRIOR`；current protocol 的正典角色是 `BOUNDARY_COMPARATOR`，与 `DEEPLY_READ`、`KNOWN_QUEUE`、`MEASUREMENT_INSTRUMENT` 并列。不能让 bridge 再发明一个似是而非的角色值，否则下游会出现两套 taxonomy。

更严重的是，计划说无关论文要写 REC-0 exclusion reason，却没有 `screening_decision=EXCLUDE` 这一维。把所有 95 篇强制塞进四种“参考角色”，会出现两种坏结果：

- 被排除论文被伪装成 positive reference role；或
- role 为空/自创新值，却仍以 `unexplained_orphans=0` 通过。

### 4.3 三个分母不是同一批 work

计划已经诚实披露 census→seed 只有 13/95、census→bibliography 只有 3/95、seed→bibliography 只有 9/92。这正说明不能以“95 个 census work 每个出现一次”代表全库闭包：其余 79 个 seed 条目、绝大多数 bibliography 条目，以及 claim/full-text-only 身份仍可能是独立 canonical node、显式 alias 或 unresolved identity。

`census=95/95 seeds=92/92 bibliography=65/65 unexplained_orphans=0` 只有在 **每一个 source row 都恰好映射一次到 union canonical-work graph** 时才有意义。当前计划没有定义 union node denominator，也没有限制把大量条目统一路由到一个泛化 `UNRESOLVED` 桶。

此外，第 413 行的“83 arXiv/version-pinned”把两个统计合并成一个短语。应分别报告 `arXiv identity count=83` 与 `version-pinned count=83/95`，不能暗示恰好是同一 83 条，除非 checker 实际验证了集合相等。

### 4.4 必须如何修

bridge 至少需要以下两层，而不是一个扁平 record：

```json
{
  "canonical_work_id": "...",
  "identities": [
    {"source_id": "...", "relation": "EXACT_ID|EXPLICIT_ALIAS|UNRESOLVED", "provenance": "..."}
  ],
  "source_memberships": [
    {"campaign": "census|seed|bibliography|claim|fulltext", "source_row_id": "..."}
  ],
  "screening_decision": "INCLUDE|EXCLUDE|UNRESOLVED",
  "reference_role": "DEEPLY_READ|KNOWN_QUEUE|MEASUREMENT_INSTRUMENT|BOUNDARY_COMPARATOR|null",
  "claim_evidence": [
    {"claim_id": "...", "evidence_grade": "...", "discrepancy_status": "...", "locator": "...", "version": "..."}
  ],
  "current_disposition": {"reason": "...", "next_action": "...", "invalidating_condition": "..."}
}
```

强制验收条件：

- 每一个 census/seed/bibliography/claim/full-text source row 恰好出现一次，不能只检查三类总数；
- `EXCLUDE` 必须有 REC-0 reason，且 `reference_role=null`；`INCLUDE` 才必须有正典 role；
- heterogeneous grade/status 必须逐 claim 保留，测试至少覆盖上述 7/8 个真实反例；
- unresolved 必须报告数量、来源、原因、owner、deadline gate 和下一动作；任何 load-bearing unresolved 阻断 proposal；
- `reviewer-known-item input` 必须有精确路径、schema、快照 hash 和生成规则，不能作为漂移的隐式输入；
- `0 unexplained orphan` 只能表示“每条都解释了”，不能表示“每条都已验证”或“全部深入阅读”。

## 五、GM-2：`absence` 合同仍允许弱证据和不相干 provenance 支撑承重结论

### 5.1 value-only 白名单不是证据语义

计划第 135–143 行把 `False`、`None`、空字符串、`none`、`unknown`、空列表统一视为合法 absence。这个设计过宽：

- `unknown` 是认识论不确定，不是“不存在”；
- `None`/空字符串可能只是缺失值，而非编码后的否定；
- 不同字段允许的 absence 编码不同，必须是 `(field, encoded_value)` 兼容表，不能是全局 value set；
- 需要排除“not coded / not fetched / not applicable / unreachable”等状态被解释成科学 absence。

当前 22 个待迁移 absence 中并无必须依赖通用 `unknown` 的理由；在没有 field-specific justification 前，应从承重白名单移除。

### 5.2 非空字符串检查无法证明引用正确

计划第 154–176 行只验证 `source_version`、`coder`、`adjudicator_provenance` 是非空 mapping。它没有证明：

- `source_id/version_binding` 与该 row 的 `fulltext_ref` 是同一对象；
- `coder.source_sidecar` 指向的就是拥有该 evidence row 的 sidecar；
- `adjudicator_provenance.artifact` 包含该 row hash；
- adjudicator verdict 恰为 `AGREE`；
- fresh delta reviewer 与原 coder/implementer 真实独立。

因此，把任何存在的 sidecar、任何非空 artifact、任何 verdict 字符串填进去都可能通过外形验证。机器只能证明绑定和声明一致，不能证明组织身份独立；后者必须明确标为 `TEAM_ATTESTATION`，不能写成 machine-proved independence。

### 5.3 locator 不能替代内容版本

计划拟采用 “sidecar fulltext SHA-256 **或** canonical record locator” 作为 source version。URL/ACL ID/arXiv locator 是身份定位，不是本次检查过的内容版本。对承重 absence，必须绑定实际检视全文的不可变版本/hash；全文不可达时只能降级或 unresolved，不能用 locator 兜底后仍保留 load-bearing status。

### 5.4 “未见”“不矛盾”不是充分的负证据

例如现有 sidecar 对 `external_component_weight_update=false` 的理由接近“主干用了 SFT，未见验证侧组件另行训练”。如果未记录实际检查的 Method/Appendix 页面、术语集合与版本，这最多是弱证据，不是排除所有外部组件权重更新的充分证明。

必须建立 field-specific absence proof obligation：每个字段规定允许的编码值、必须检视的章节/页面/术语/表格、可接受的明确原文类型、全文版本，以及何种情况必须 `UNRESOLVED`。迁移脚本不能机械复制旧 note 后就升级成 structured absence。

### 5.5 通过标准

新增 mutation tests 至少要使以下反例失败：wrong fulltext hash、wrong sidecar、wrong row hash、artifact 不含该 row、verdict 非 `AGREE`、`unknown` 承重、空缺值冒充 absence、URL 代替全文 version、弱“not contradicted”理由、coder 与 fresh adjudicator 同一 actor。22 条真实 row 必须由非实现者逐条做语义复核，而不仅是 hash delta 复核。

## 六、GM-3：所谓双平台 canonical evidence-v7 尚不能成立，WSL 执行顺序也确定有错

### 6.1 canonical aggregate 在 POSIX 结果之前产生

Task 3 的命令顺序是：

1. Windows 生成 `.nt.json`；
2. Windows 同一个 runner 生成无后缀 `identity-taxonomy-v7-test.json`；
3. WSL 才生成 `.posix.json`。

所以第 2 个文件不可能是消费 Windows 与 POSIX 两份结果的“canonical aggregate”。它只是另一次 Windows 输出。`occupancy_equal_to_v6=true` 也只证明相对 v6 的 occupancy，没有证明 NT=POSIX，更没有绑定两份 leaf report 的输入 hash、runner hash 和平台 stamp。

正确拓扑应为：

```text
same frozen inputs
  ├─ Windows runner → nt leaf report
  └─ WSL2 runner    → posix leaf report
                        ↓
separate aggregator consumes both exact leaf bytes
  → checks input hashes + contract version + occupancy + named failures
  → canonical aggregate
```

aggregate 必须最后生成；current manifest 必须同时绑定 aggregate 与两份 leaf report。平台 runner 不得自己宣称跨平台一致。

### 6.2 当前 linked worktree 在 WSL 下实际不可识别

作者外只读重放得到：

- worktree `.git` 内容为 Windows 绝对路径：`gitdir: D:/chao_workspace/.../.git/worktrees/stage1b-readiness-remediation`；
- Windows `git -C <worktree> rev-parse --show-toplevel` 成功；
- WSL `git -C /mnt/d/.../.worktrees/stage1b-readiness-remediation rev-parse --show-toplevel` 返回 128，并把 Windows `D:/...` 错接到当前 POSIX path 后；
- 显式设置正确的 `GIT_DIR=/mnt/d/.../.git/worktrees/stage1b-readiness-remediation` 与 `GIT_WORK_TREE=/mnt/d/.../.worktrees/stage1b-readiness-remediation` 后成功。

计划把 Git metadata repair 放在 Task 10，但早在 Task 3 和 Task 9 就要从 WSL worktree 跑可能读取 Git/blob binding 的脚本。因此它会先失败，或者在不同 Git 上下文中产生无法比较的 receipt。

并且，Task 10 只 unset shared `core.worktree` 并不足以修复 linked worktree `.git` 内的 Windows 绝对 `gitdir:`。两者是两个独立问题。

### 6.3 必须如何修

在任何 WSL gate 前增加 **Task 0: cross-platform Git preflight**：

- 分别证明 primary repo 与 linked worktree 在 Windows、WSL 中都能得到正确 root、HEAD、blob 和 clean status；
- 要么把 linked-worktree metadata 规范成双方都可解释的相对路径，要么所有 WSL 命令显式、统一使用正确的 `GIT_DIR/GIT_WORK_TREE` wrapper；
- 先处理 shared `core.worktree`，再运行 evidence-v7，而不是到 merge 前才处理；
- 对 metadata 修复本身保留 before/after receipt，但不要把本机 `.git` 内容作为论文证据上传；
- 只有两份 leaf report 产生后才运行 aggregator。

这是正常指令下的真实执行错误，不是恶意篡改元数据测试，完全属于用户强调的脚本正确性与可回放性范围。

## 七、GM-4：引用闭包仍然不是 system-first，metadata 测试存在循环 oracle

### 7.1 对计划中引用设计的总体判断

计划不是正式 research proposal，所以不要求它自己在正文列完整学术参考文献；它通过 Task 5 生成 bibliography、Task 6 绑定 source manifest 的架构是合理的。问题在于 Task 5 当前只保证“六个新增 ID 存在、作者不是占位符”，无法保证元数据来自独立权威来源，也没有确保 system-first 直接邻近工作进入 reviewer-visible closure。

### 7.2 硬编码 expected metadata 不是独立 oracle

若 generator 与 test 都手工写入同一组 title/authors/URL，它们可以一起错而测试仍绿。正确做法是保存 machine-readable official metadata receipt：

- arXiv Atom/export、ACL Anthology BibTeX 或官方页面；
- 记录 URL、访问时间、access class、原始响应 hash、版本；
- generator 消费 receipt；test 从 receipt 重算并与输出比较；
- 新增访问登记为 `ID_DEREFERENCE`、`PROVENANCE_FETCH` 或 `REVIEW_CLAIM_VERIFICATION`，不得静默记作 zero discovery，也不得获得 frozen-query recall credit。

“零作者占位符”只证明格式完整，不证明引用正确。

### 7.3 现有整套论文资产没有被充分用于 system-first 论证

作者外检索确认，下列直接相关工作已经存在于本仓历史 census、seed、claim 或 archive 中，但在当前 65 条 `2026-07-19-sf-bibliography-v1.md` 中均为 0 次：

| 工作 | 现有资产状态 | 本轮必须做的事 |
|---|---|---|
| AudioToolAgent, arXiv:2510.02995 | census/seed/claim/多份 review 已有 | 作为 speech tool-agent 直接邻近，进入 opening/bibliography；若支持 gap claim，需 D2 |
| Audio-Mind, arXiv:2605.28480 | census/claim/既有 proposal 已有 | 作为 omni audio agent 直接邻近，显式能力与训练边界 |
| Agent-Omni, arXiv:2511.02834 | census/既有 review 已有 | 作为 omni agent system comparator 路由 |
| EChO-Agent, arXiv:2606.15141 | census/neighbor matrix 已有 | 作为 embodied/omni agent comparator 路由 |
| AuTAgent, arXiv:2602.13685 | census/claim 已有 | 显式训练/工具使用边界，不能因非 frozen black-box 而消失 |
| Speech-Copilot, arXiv:2407.09886 | seed/早期 survey 已有 | 作为 speech tool orchestration 先行系统比较 |
| VoxMind, arXiv:2604.15710 | archive 已有 | 作为 end-to-end agentic spoken dialogue 的训练型强边界；官方摘要明确包含 470h AgentChat 与动态工具管理，不能漏掉 |
| WavReward, arXiv:2505.09558 | 早期 survey/archive 已有 | 作为训练型 speech reward evaluator / measurement boundary |
| GSRM, arXiv:2602.13891 | archive 已有 | 作为 speech reward-model 边界登记和去重 |

这里的要求不是把所有论文都升级成 `DEEPLY_READ`，也不是在 Stage-1A 再做一次 mapping。正确动作是：所有既有论文都进入 GM-1 的 union disposition graph；上述 system/reward 直接邻近至少进入 reviewer bibliography 与 opening role；只有被 proposal 用作承重 gap/novelty/boundary claim 的论文才必须在 round 14 前达到 D2。其余可明确 `KNOWN_QUEUE`、`BOUNDARY_COMPARATOR` 或 REC-0 exclusion。

以 system-first 为第一创新假设，却让 reviewer bibliography 主要围绕 generic test-time reward/verifier，而不显式呈现 speech/omni agent system frontier，会使研究问题看起来被 reward 技术反客为主。这是论证结构偏差，不是单纯少几篇引用。

### 7.4 定向外部核验发现的补充项

以下不应修改 frozen query，也不应算 query recall；它们应登记为 reviewer-known items：

- [Trust but Verify! A Survey on Verification Design for Test-time Scaling](https://arxiv.org/abs/2508.16665)：库中 archive 已出现但未进入 current closure；它直接提供 verifier 类型、训练方式与使用位置的综述框架，适合作为 Track A taxonomy/calibration 来源。
- [Test-time Verification via Optimal Transport: Coverage, ROC, & Sub-optimality](https://arxiv.org/abs/2510.18982)：本仓当前未命中。它把 generator coverage、verifier ROC 与 sampling sub-optimality 联合建模，正好约束本项目不能把“增大 K”“更好 verifier”“更好 selector”混成一个提升来源。建议 P2，Stage-1B fetch/code；若 round-14 用其理论论断则提前 D2。
- [VoxMind: An End-to-End Agentic Spoken Dialogue System](https://arxiv.org/abs/2604.15710)：既有 archive 资产，必须进入 trained system boundary，而不是重新计作外部发现。
- [WavReward: Spoken Dialogue Models With Generalist Reward Evaluators](https://arxiv.org/abs/2505.09558) 与 [GSRM: Generative Speech Reward Model for Speech RLHF](https://arxiv.org/abs/2602.13891)：训练型 speech reward/evaluator 邻近，至少需要明确 disposition。
- [Training-Free Reward-Guided Image Editing via Trajectory Optimal Control](https://arxiv.org/abs/2509.25845)：模态和任务边界较远，可作为 element-level method comparator 的 P2 reviewer-known item；不应为它新增 query lane，也不阻塞 Stage-1B 开门。

### 7.5 引用闭包的合格标准

不是“引用越多越好”，而是同时满足：

1. 论文身份和元数据有独立官方 receipt；
2. 既有全库每条有无损 disposition；
3. system-first、reward/verification、training-free boundary 三条链都可见；
4. load-bearing claim 只引用达到所需 evidence grade 的来源；
5. reviewer-known 与 frozen-query recall 严格分开；
6. 未引用项有明确 exclusion/queue reason，而不是沉默丢失。

## 八、其他 P1 结构问题

### 8.1 Git baseline 被一把尺子承担了三种语义

计划多处硬编码 `2f16b23`。该 commit 可以作为 evidence-v6 不变性的历史锚，但不能同时自然代表：

- 本实施计划开始时的 freeze（应为目标 HEAD `17e230f...`）；
- merge 前 master 的 remote 基线（应 fetch 后记录 `origin/master`/merge-base）；
- merge 后本次 release 的完整 changed range。

应建立命名锚：`EVIDENCE_V6_RELEASE_ANCHOR`、`IMPLEMENTATION_FREEZE`、`PRE_MERGE_MASTER`、`MERGE_HEAD`，并在 receipt 中绑定各自 commit 与用途。

### 8.2 `git diff --check` 的调用范围不足

在 clean committed tree 上直接运行 `git diff --check` 通常只看未提交差异，不能证明本轮已提交内容没有 whitespace error。Task 9 应检查 `git diff --check IMPLEMENTATION_FREEZE..HEAD`；merge 后应检查 `git diff --check PRE_MERGE_MASTER..MERGE_HEAD`，并审阅该范围的 changed paths。clean status 不是 release-range 内容审计。

### 8.3 “close three gates”措辞仍需对象限定

计划目标写 “Close the three reviewer-named Stage-1A gate majors”，但正式独立 review gate 直到 round 15 才可能关闭。round 14 之前最多写：

> `THREE_IMPLEMENTATION_FINDINGS_REMEDIATED; FORMAL_INDEPENDENT_REVIEW_PENDING`

不能把本地 checker PASS 等同于 reviewer sign-off。

### 8.4 “fresh non-implementer”应绑定角色冲突声明

需要记录 actor identity、未参与哪些脚本/数据修改、审查对象 hash、时间、verdict 和利益冲突声明。仍应明确这是团队流程 attest，不是机器能够证明的事实。

## 九、是否超越 Stage-1A 范围

### 9.1 没有越界的部分

- 静态 contract、schema、mutation test；
- 旧论文资产 crosswalk 与 current knowledge routing；
- official metadata/provenance verification；
- proposal/source manifest/audit package；
- Windows/WSL 可回放性；
- Git release 修复与审计。

这些都是 Stage-1A 的 survey readiness infrastructure。即使代码量较大，只要不执行 systematic query 和研究模型，就不能因为“写了脚本”而误判成 Stage-1B/2。

### 9.2 会越界的动作

- 执行任意一条 frozen discovery query 或 proceedings route；
- 开始 REC-0/REC-2 的 systematic production population；
- 运行任何研究模型、smoke、headroom、WER/accuracy 或方案比较；
- 用定向补文献结果宣称 systematic recall 已完成；
- 在 round-15/owner 授权前把 `execution_authorized` 写为 true。

计划目前文本禁止了这些动作，应继续保留。修正文献闭包只允许对已知 ID 做 metadata/full-text provenance fetch，必须按访问类别登记。

## 十、严格整改 proposal：按依赖关系执行

### P0-0：先修执行地基，不要等到 Task 10

1. 新增 cross-platform Git preflight；
2. 修复/包裹 linked worktree 的 Windows/WSL gitdir 解析；
3. 分离四个 Git anchors；
4. 让所有后续 receipt 都绑定同一 `IMPLEMENTATION_FREEZE`。

**通过条件**：Windows 与 `wsl -d Ubuntu-24.04` 都能在 primary 和 linked worktree 得到正确 root/HEAD/blob/status；失败时后续 task 不运行。

### P0-1：重构 corpus disposition 为无损 union graph

1. 明确定义 canonical work node 与 source-row membership；
2. 分离 screening decision 和 reference role；
3. role 统一为 protocol 正典值；
4. 每个 claim 的 grade/status/version/locator 保留为数组元素；
5. reviewer-known input 冻结为具体 artifact；
6. 对所有旧论文资产生成 disposition，而非只对 census 节点生成。

**通过条件**：真实 heterogeneous 反例不丢失；所有 source rows exactly-once；unresolved 与 exclusion 可解释；load-bearing unresolved 使 package FAIL。

### P0-2：把 absence 从“有字段”升级为“字段级负证据合同”

1. 建 `(field, allowed_absence_value, proof_obligation)` 表；
2. 移除通用 `unknown`/空缺值的承重资格；
3. 跨绑定 row、sidecar、fulltext hash、adjudication artifact 和 verdict；
4. 无 immutable fulltext version 就降级；
5. 对 22 条逐条 fresh semantic adjudication；
6. 增加上述反例 mutation tests。

**通过条件**：弱“未见”不能自动支撑承重 absence；错误引用和非 AGREE 判决必失败。

### P0-3：重建 evidence-v7 双平台 DAG

1. Windows/WSL 分别只写 leaf；
2. aggregator 最后消费两个 exact leaf；
3. 比较 source hashes、runner/contract version、named failures、occupancy、output semantics；
4. aggregate 与 leaves 同时进入 current manifest；
5. 用 mismatch leaf 反例证明 aggregate fail closed。

**通过条件**：删除/替换任一 leaf、改变输入 hash、改变 occupancy 或平台 stamp，canonical aggregate 必须 FAIL。

### P0-4：完成 system-first bibliography closure

1. 从 official metadata receipt 生成 bibliography，不让手写 expected 充当 oracle；
2. 把既有 AudioToolAgent、Audio-Mind、Agent-Omni、EChO-Agent、AuTAgent、Speech-Copilot、VoxMind、WavReward、GSRM 逐项路由；
3. 登记本轮 reviewer-known additions，全部 `query_recall_credit=false`；
4. proposal 的每个 gap/boundary claim 绑定 claim ID、evidence grade、locator/version；
5. 不要求非承重 P2 在 Stage-1A 全部精读。

**通过条件**：system-first opening 有直接系统邻近与训练型边界；零 silent omission；metadata 可从独立 receipt 重算。

### P1：修 release 与措辞

1. 所有 `git diff --check` 使用明确 commit range；
2. proposal/package 状态写为 implementation-remediated / independent-review-pending；
3. non-implementer independence 作为具名 attest；
4. hostile self-review 至少一整轮零新发现，并把新发现及修复保留在审计记录中，不只写最终 PASS。

## 十一、Stage-1B 放行矩阵

| 条件 | 当前状态 | 是否阻塞 |
|---|---|---|
| 阶段正典明确，Stage-1B 禁模型/smoke | 已满足 | 否 |
| frozen query/compiler 未变 | 计划保证，尚待实施后证明 | 是 |
| GM-1 无损旧库 disposition | 未满足 | **是** |
| GM-2 field-specific absence + cross-binding | 未满足 | **是** |
| GM-3 真正双平台 aggregate + WSL preflight | 未满足 | **是** |
| GM-4 system-first bibliography + independent metadata receipts | 未满足 | **是** |
| round-14 immutable proposal 已生成并绑定同一 package | 未发生 | **是** |
| round-15 独立 reviewer 给出 `SIGN` | 未发生 | **是** |
| owner 对同一 exact package 明确授权 | 未发生 | **是** |
| current manifest/package check 为同包 PASS，`execution_authorized=true` | 未发生 | **是** |

只有上表所有阻塞项关闭后，执行第一条 frozen systematic query 才标志 Stage-1B 正式开始。放行 Stage-1B 也不等于允许模型或 smoke；模型暴露仍要等到 Stage-2A，且先复现最近、最强、公开 prior。

## 十二、给研究团队 AI 的无歧义执行指令

```text
CURRENT_STAGE = STAGE_1A_FINAL_REMEDIATION
PLAN_REVIEW_VERDICT = MAJOR_REVISION_BEFORE_EXECUTION
STAGE_1B_SEARCH_DESIGN_SIGNOFF = WITHHOLD
RESEARCH_MODEL_EXECUTION = FORBIDDEN
SMOKE_EXECUTION = FORBIDDEN
SYSTEMATIC_QUERY_EXECUTION = FORBIDDEN_UNTIL_ROUND15_SIGN_AND_OWNER_SAME_PACKAGE_AUTHORIZATION

DO_NOT:
  - modify frozen query terms/compiler;
  - create or prefill round-15 reviewer verdict;
  - count reviewer-known or inherited papers as frozen-query recall;
  - collapse heterogeneous per-claim evidence into one work-level grade/status;
  - treat UNKNOWN/missing value as load-bearing absence;
  - call a Windows rerun a dual-platform aggregate;
  - claim formal gates closed from local checker PASS;
  - run model, smoke, dataset metric, headroom, or prototype.

MUST_BEFORE_ROUND14_SUBMISSION:
  1. fix cross-platform Git preflight and evidence-v7 DAG;
  2. implement lossless union corpus disposition;
  3. implement field-specific and cross-bound absence validation;
  4. generate bibliography from bound official metadata receipts;
  5. route all inherited system-first/reward neighbors with query_recall_credit=false where applicable;
  6. run fresh Windows + WSL checks and one zero-new-finding hostile round;
  7. label package SUBMITTED_FOR_INDEPENDENT_REVIEW, not STAGE1B_READY.
```

## 十三、最终导师意见

研究团队已经从“写一份好看的 proposal”前进到“尝试建立可审计的研究知识系统”，方向是对的。真正的短板也因此暴露得更清楚：当前最危险的不是少一个模型实验，而是 **知识图谱的单位不清、负证据的语义不够强、平台证据的聚合关系不真实、系统主线论文没有进入当前论证闭包**。这些问题若不修，后续 Stage-1B 的大量 mapping 只会把不可靠的组织结构放大。

所以本轮不批准 Stage-1B，但也不要求扩大 Stage-1A 去做实验、预算 cap 或无限追加论文。请做一次窄而深的结构整改：无损利用已有全库，确保每个 PASS 真能证明其命名的性质，然后把同一冻结包交给独立 reviewer 与 owner。届时 Stage-1B 可以开始，而且开始的第一步应是 systematic mapping，不是触碰研究模型。
