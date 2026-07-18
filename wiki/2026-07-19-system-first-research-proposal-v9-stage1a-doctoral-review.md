---
title: "System-first Research Proposal v9：Stage-1A 尾门敌意博士级复审"
date: "2026-07-19"
review_role: "严格外审人 / 博士生导师 / 研究诚信审计视角"
review_target: "wiki/2026-07-19-system-first-research-proposal-v9-consolidated.md"
target_commit: "bb3e2c38fba6814ba79bccb9e795d3af6f85c2f1"
target_git_blob: "80bd82072289387be9d2a4391fa2026fe36b3522"
target_sha256: "53da05d2d82032b6a2012adda47f67ef4cd226b8fc180f154dedd8d0b2bae849"
review_verdict: "WITHHOLD_STAGE1B_NARROW_REMEDIATION"
gate_status: "v8 MAJOR-1 CLOSED；v8 MAJOR-3 CLOSED；v8 MAJOR-2 PARTIALLY_OPEN"
new_gate_major_count: 1
integrity_verdict: "未发现 FFP；存在完成态措辞再次超过机器能力包络的 false-assurance/QRP 风险"
scope_note: "本报告只新增日期审查件，不修改 v9、回应信、脚本、sidecar、台账或团队正在进行的工作"
---

# 一、结论先行

## 1.1 当前阶段

当前仍处于 **Stage-1A survey-ready gate 的最后签署门**，尚未进入 Stage-1B：

1. v9 明确记录 `current_activity_stage = Stage-1A`；
2. systematic discovery/mapping query 仍为 0；
3. 本整改批没有研究模型调用或 smoke；
4. 当前工作仍是 survey schema、证据合同、开局队列和跨平台复放；
5. 按现行阶段正典，第一条正式系统查询才是 Stage-1B 起点；Stage-1B 仍禁止模型与 smoke。

因此，v9 的阶段自我定位正确。taxonomy v5、sidecar schema v2、路径解析和 opening table
都属于 Stage-1A 的合理基础设施，不属于提前跑 Stage-2 实验。

## 1.2 是否可以开展 Stage-1B

**本轮仍暂不签署 Stage-1B，但已从三门收缩为一项窄整改。**

裁决不是要求团队继续无限找论文，也不是要求跑模型、冒烟集、预算 cap 或 Stage-2 统计实验。
三项旧门的真实状态是：

| v8 门禁 | v9 实际状态 | 本轮裁决 |
|---|---|---|
| MAJOR-1：signal instance / same-signal causal binding | signals[]、edge signal_id、同信号同用途存在量词均已实现；CE-v3 也被纳入 | **CLOSED** |
| MAJOR-2：承重 evidence completeness / locator / release binding | strict 三态、部分 required evidence、row hash 已实现；但 signal/edge 结构与证据仍可假绿，release checker 不检查正文 | **PARTIALLY OPEN，唯一 Gate MAJOR** |
| MAJOR-3：WSL2 正典重放 | Windows 3.14 与 WSL2 Python 3.12 均 12/12，occupancy 相同 | **CLOSED** |

只要修复本报告给出的有限反例，再完成已知文献 carry-forward，即可签署 Stage-1B。无需再提交
一份大而全的新 proposal；新的 dated response、机器输出和窄幅复核即可。

# 二、审查方法与证据冻结

## 2.1 冻结对象

- HEAD：`bb3e2c38fba6814ba79bccb9e795d3af6f85c2f1`
- v9 git blob：`80bd82072289387be9d2a4391fa2026fe36b3522`
- v9 blob SHA-256：`53da05d2d82032b6a2012adda47f67ef4cd226b8fc180f154dedd8d0b2bae849`
- 审查开始时工作树干净。

## 2.2 四轮对抗式核查

### Round A：回应信与实现逐项对账

不是按 v9 的“已闭合”自述裁决，而是逐项阅读：

- taxonomy v5 派生；
- schema-v2 sidecar；
- coding generator；
- reconciliation；
- release binding；
- canonical asset path resolver；
- amendment-14、回应信与 opening table v3。

### Round B：双环境复放

- Windows：Python 3.14.3；
- WSL2：`wsl -d Ubuntu-24.04`、`~/.venvs/speechrl`、Python 3.12.3；
- 两端运行 path resolver、generator check、taxonomy v5、release binding；
- 另在 WSL 对 74 条 immutability registry 做纯只读 evaluation。

### Round C：作者测试集之外的语义变异

重点模拟 Stage-1B 新增 method path，而不是只改已有 11 行、依赖作者为这 11 行写死的
per-ID expectation。反例均为普通编码错误，不是恶意篡改注册表或伪造 git 历史。

### Round D：官方来源文献补查

- 只使用 arXiv、ACL Anthology 等一手页面；
- 区分“已知但 carry-forward 失败”与“应由 Stage-1B 系统查询发现”；
- 检查遗漏是否暴露新的 query-lane 盲区。

# 三、应当明确认可的真实整改

## 3.1 v8 MAJOR-1 已真实关闭

taxonomy v5 不再把所有 signal 属性压成行级单值，而是：

- `signals[].signal_id` 一等化；
- control edge 引用 signal ID；
- edge lifecycle 若提供，必须与 signal lifecycle 相同；
- RQ-SYS 由同一 signal instance 上的 reward 性和 LIVE edge 派生；
- CE-v3 又把约束下推到 edge 自身 use，防止同一 signal 内“惰性 reward use + 非 reward edge”
  拼接；
- reward-guided selection 要求真实 pool、selection policy 和同一 reward signal 的
  select/prune use。

我复核了 A1–A8、K1–K7 和 v1–v3 independent counterexamples。v8 报告中给出的：

- terminal reward + 另一在线非 reward route edge；
- offline calibration + scored select；
- row/edge lifecycle mismatch；

现在均得到预期结果。当前 5/11 RQ-SYS 的派生至少不再由“异信号拼接”产生。

## 3.2 v8 MAJOR-3 已真实关闭

双环境复放结果：

| 环境 | generator | taxonomy v5 | occupancy |
|---|---|---|---|
| Windows nt / Python 3.14.3 | byte-identical | 12/12 PASS | reward 6/11；RQ 5/11；candidate 0/11；RGS 4/11；trajectory pool 2/11 |
| WSL2 Ubuntu-24.04 / Python 3.12.3 | byte-identical | 12/12 PASS | 与 Windows 完全相同 |

`sf_asset_path.py` 对 `E:/...` 与 `/mnt/e/...` 的映射修复了 v8 的直接失败。WSL 下对当前
registry 的纯 evaluation 也得到 74 registered / 0 failures。

因此，不应继续把 WSL2 写成阻塞项。建议补存两端独立机器快照，但这是可复现性记录完善，
不是本轮 Gate。

## 3.3 strict 三态与 adjudication row hash 是有效防线

- `unknown` 不再被静默当作 False 获得 strict 身份；
- 14 个当前 `REQ_FIELDS` 缺失会触发 required-evidence failure；
- 对已盖章行做 post-adjudication 修改会触发 row-hash mismatch；
- 原 v8 的 horizon 单翻转和 horizon+evidence 双翻转能够被拦截。

这些整改应当保留。后文指出的问题不是否定 row hash，而是 row hash 不能替代 schema
语义验证：错误若在一次新行被裁决前就进入，正确计算出的 hash 只会忠实冻结错误。

# 四、唯一 Gate MAJOR：证据完备合同尚未覆盖 Stage-1B 新行的承重信号与发布正文

## 4.1 “15 个承重字段”实际只有 14 个

代码中的 `REQ_FIELDS` 为：

```text
7 strict bits
+ internal_visibility
+ core_topology
+ core_native_modality
+ control_horizon
+ decision_rights
+ candidate_pool_exists
+ selection_policy
= 14
```

v9、回应信和 amendment-14 均反复声称“15 个承重字段”。这首先是一个可验证的计数错误。
更重要的是，决定 reward/RQ/RGS 的以下字段并不在结构化 `claim_evidence` 合同内：

- signal form；
- signal lifecycle；
- signal uses；
- signal source；
- edge signal use；
- edge decision right 与 allowed relation；
- selection object / explicit selection 状态。

taxonomy JSON 用一句话声称每个 signal 的一个 `evidence` locator 同时支撑
form/lifecycle/uses，但程序只检查 locator 中某段文本是否存在，并不做字段—值绑定。

## 4.2 validator 没有执行 proposal 声称的 edge 结构合同

v9 声称：

> edge 引用 signal，且 edge.signal_use ∈ signal.uses，decision right 合法。

实际 `validate()` 只检查：

- signal ID 是否存在；
- 可选的 edge lifecycle 是否匹配 signal。

它没有把以下情况登记为 validator failure：

- `edge.signal_use` 不在所引 signal 的 uses；
- `edge.decision_right` 不在行级 rights；
- use/right 不在 allowed-relations 白名单。

`valid_live_edges()` 只会静默跳过这些坏边。静默跳过会改变 RQ occupancy，却不会告诉编码者
sidecar 自相矛盾。

### 精确反例 E1

对 Selective TTS 行，把 edge 的 use 从 signal 声明的 `prune` 改成 `select`，保持它仍引用
同一 signal，并按正常新行流程重新计算 adjudication row hash。

结果：

```text
validate(...)  -> []
reconcile(...) -> []
n_valid_live_edges: 1 -> 0
RQ-SYS: True -> False
```

这不是要求系统防止恶意重算 hash。它模拟的是 Stage-1B 新行第一次被创建、随后被裁决的正常
流程。新行没有现有 11 行的 per-ID author expectation；因此通用 validator/reconciliation
必须自己拒绝这种结构错误。

## 4.3 signal evidence 可用 `p9999` 绕过页码解析

行级 locator 和 edge locator 会调用 `check_page_tokens()`，但 signal 的 evidence 只调用
`check_quotes()`，没有调用页码范围检查。

### 精确反例 E2

把 ATLAS 的 signal evidence 改为 `p9999`，按正常新行流程生成 row hash：

```text
validate(...)  -> []
reconcile(...) -> []
```

因为 `check_quotes()` 看到它长得像 page token，就不报“unverifiable”；而 signal 路径从未
执行 page range。v9 的“p9999 死于 range 检查”只对部分 locator 成立。

## 4.4 即使行级 locator，也没有强制页内 anchor

`PAGE_TOKEN` 的 anchor 是可选的。对 PDF method path 把 locator 改为 `p1`，只要 PDF 有第一页，
就通过；`p1 the` 这样的通用英文 token 也通过。

### 精确反例 E3

```text
source_locator = "p1"
validate(...)  -> []
reconcile(...) -> []
```

所以当前只实现了“页码不超过 PDF 页数”，没有实现 proposal 所称“页码 + 页内 claim anchor”。
它能杀死荒谬的 p9999，却不能杀死最常见的、范围内但定位错误的页码。

此外，taxonomy 声明支持 `pdf_page` evidence kind，但 `check_evidence_entry()` 只实现
canon/tex/absence；实际使用 `pdf_page` 会得到 `evidence-kind-invalid`。这是合同与实现不一致。

## 4.5 signal form 可改变 RQ 结论而 evidence reconciliation 仍干净

### 精确反例 E4

把 Selective TTS 的在线 stage signal form 从 `scalar_score` 改成 `text_critique`，保留原来的
signal evidence locator，按正常新行流程生成 row hash：

```text
validate(...)  -> []
reconcile(...) -> []
该 signal 不再是 reward form
该行 RQ-SYS: True -> False
```

这证明 signal evidence 的存在性并不等于其 form/lifecycle/use 已被 evidence-value binding。
row hash 只能证明“裁决后没变”，不能证明“裁决时字段有对应证据”。

## 4.6 release binding 只绑定隐藏机器块，不绑定正文数字

`sf_release_binding_check.py` 解析：

```html
<!-- release_binding: {...} -->
```

然后把机器块与 JSON 输出对账。它不搜索、生成或比较正文中的数字。脚本注释声称
“stale prose numbers fail”，v9 又声称“散文数字不可能过期而不红”，两者均不成立。

### 精确反例 E5

保持机器块的 `reward_guided = 6/11` 不变，仅把 v9 正文：

```text
is_reward_guided = **6/11**
```

改成：

```text
is_reward_guided = **99/11**
```

结果：

```text
release check -> []  （PASS）
```

这不是攻击元数据，而是测试发布件中最普通的复制粘贴陈旧。v8 复审明确要求绑定 dated proposal
的固定数字；隐藏块正确、正文错误仍绿，说明该子门没有关闭。

## 4.7 为什么仍是 Gate，而不是脚本洁癖

Stage-1B 将新增大量此前没有 per-ID expectation 的 method paths。当前 11 条已有作者反例，
所以修改它们有时会被硬编码 expectation 偶然拦住；新行没有这种保护。

上述 E1–E5 均会影响：

- reward / RQ-SYS / reward-guided selection occupancy；
- 哪些论文被认为填补项目空位；
- dated report 对外呈现的 headline。

因此这是规模化前的科学数据合同问题，而不是为了防篡改而做的无限鲁棒性工程。

# 五、引用与文献 survey 评价

## 5.1 v9 新补六篇是否引用合理

总体合理：

- Reinforced Agent 的题名、作者和 arXiv ID 正确，确属执行前 reviewer feedback；
- TF-TTCL 的 ACL/arXiv 双 ID 及 training-free contextual rule steering 定位合理；
- Training-Free GRPO 被放在 upstream-label-learning / 名称碰撞边界，而不是误当 TF-Strict；
- TRACE、LWE、Min-Seek 被列为 Stage-1B 首批筛选，而非提前写成 occupancy；
- 15+3+22+8+4+3 = 55，分类计数自洽。

Reinforced Agent 已有 ACL GEM 2026 正式版本，建议把
`2026.gem-main.13` 与 arXiv:2604.27233 做同 work 去重绑定，优先使用 ACL 正式链接。

## 5.2 “自包含附录”名不副实

附录标题称“自包含”，但 A.1、A.2、A.4 都让读者回查 v8，很多条目只保留缩写/ID，没有
当前文档内的作者和稳定链接。git blob 钉定使其可追踪，却不等于自包含。

两种修复任选：

1. 真正重复完整 55 条元数据；或
2. 把标题改成“闭包可解析书目”，并提供机器生成的 work-ID → pinned predecessor row 映射。

这是 citation presentation 的 required correction，不单独构成 Gate MAJOR。

## 5.3 已知但没有 carry-forward 的高相关工作

以下不是要求团队预知未来，而是仓内已经登记或精读过，却没有进入 v9 opening role tables：

### P1：签 Stage-1B 前补进 opening guarantee

1. **Mapping Smarter, Not Harder: A Test-Time Reinforcement Learning Agent That Improve Without
   Labels or Model Updates**（EMNLP Industry 2025）

   它在仓内 sentinel 与 2026-07-16 access log 已登记。方法在推理时以 confidence reward
   迭代控制映射，并发起 web search 获取外部证据。它是“零权重更新但 new-info”最直接的
   RQ-SYS / 信息边界反例，应进入表 D，而不仅是召回哨兵。

   官方链接：https://aclanthology.org/2025.emnlp-industry.75/

2. **Boosting ASR Robustness via Test-Time Reinforcement Learning with Audio-Text Semantic
   Rewards（ASR-TRA）**

   仓内 2026-07-13 scout ledger 已完整定性：它使用 audio-text reward，但更新 model 与
   learnable prompt，因此不是 TF-Strict。由于它同时命中 speech、test-time RL、reward，
   是最重要的名称/身份边界之一，应进入表 D。

   官方链接：https://arxiv.org/abs/2603.05231

3. **Dual-Axis Generative Reward Model Toward Semantic and Turn-taking Robustness in Interactive
   Spoken Dialogue Models**

   仓内 2026-07-06 reward survey 已读过，当前又被遗忘。它训练 generative reward model，
   分别评价语义质量与 turn-taking timing，是 omni/speech reward instrument 的直接边界。
   应进入 measurement/reward-element 表，注明“trained RM，不满足全系统零训练”。

   官方链接：https://aclanthology.org/2026.acl-long.6/

4. **SDiaReward / ESDR-Bench**（arXiv:2603.14889；ACL 2026）

   仓内早期 survey 已把它裁为 trained spoken-dialogue reward element。它对自然口语、声学
   表达和对话偏好建模，正好补足现有表 B 只有 benchmark、没有 speech reward instrument
   的缺口。应 carry-forward，而不是依赖 1B 再次发现。

   稳定链接：https://arxiv.org/abs/2603.14889

这四项要求只是登记角色、ID、预期 route 和边界假设，不要求 Stage-1A 完成全文重编码。

## 5.4 Stage-1B 首批应关注、但不阻塞开门的新增近邻

### 系统控制 / verifier-refiner

- **TangramSR**：training-free VLM verifier-refiner，以 geometric consistency reward 递归
  修正，是多模态 reward loop 直接近邻。
  https://arxiv.org/abs/2602.05570
- **Reward Modeling for Multi-Agent Orchestration（OrchRM）**：直接在 orchestration 层
  训练 reward model 并用于 MAS TTS；因 reward model 被训练，主要是 TF-Strict 边界。
  https://arxiv.org/abs/2606.13598
- **ToolRM**：训练 tool-use reward model，并用于 BoN/self-correction/inference-time scaling；
  是 tool decision reward 的边界件。
  https://aclanthology.org/2026.findings-acl.419/
- **Exploring Reasoning Reward Model for Agents（Agent-RRM）**：结构化 critique + score
  驱动 agent refinement，但 reward model / integration 存在训练路径。
  https://aclanthology.org/2026.findings-acl.95/

### speech/omni 训练边界与 reward 设计

- **Decoupling Conversational Dynamics in Full-Duplex Spoken Models through RL（DuplexPO）**：
  factorized conversational-dynamics reward 控制 turn initiation/backchannel/yielding；属于
  权重更新的强边界，不是 TF-Strict 方法占据。
  https://arxiv.org/abs/2607.07148
- **Multi-Faceted Interactivity Alignment in Full-Duplex Speech Models**：四类交互 reward +
  LLM semantic reward 的 post-training；适合作为 RQ-OMNI/RQ-MEASURE 边界。
  https://arxiv.org/abs/2606.11167

## 5.5 是否暴露新的检索 lane 结构性遗漏

没有。现有 query families 已覆盖：

- agent feedback / inference-time control；
- reward-guided / verifier-guided；
- generative reward model；
- speech/audio/omni；
- VLM/MLLM test-time scaling；
- ACL venue routes。

TangramSR、OrchRM、ToolRM、Dual-Axis 等原则上可被现有 L2/L5/L12/L15 或 ACL routes 捕获。
所以不应继续修改 query universe，也不应因新增若干 P2 文献无限延长 Stage-1A。

# 六、研究范围是否越阶段

## 6.1 当前没有越阶段

- 没有 systematic mapping query；
- 没有模型或 smoke；
- 没有效果摸高、数据集对标、selector/evaluator 实验；
- Stage-2A 只保留 reproduction-first 预告；
- innovation 仍写成假设，没有“first-ever”声明。

因此，当前工程与 survey 工作都在 Stage-1A 合法范围内。

## 6.2 Stage-1B 仍应保持的边界

签署后只做：检索、去重、获取、全文证据、编码、裁决、occupancy、负结果地图和饱和记录。

以下继续留在 Stage-2A：

- 模型推理或冒烟集；
- prior reproduction 的实际运行；
- evaluator/controller 的效果比较；
- 新方法原型；
- 数据集/模型大规模对标。

v9 的 Stage-2A preview 没有执行力，所以本身不越线。

# 七、研究诚信裁决

## 7.1 未发现学术欺诈证据

本轮仍没有 fabrication、falsification 或 plagiarism 证据。诚信正向迹象包括：

- v8 原件不改字节，以 v9 dated supersession 回应；
- CE-v3 击穿初版派生被主动披露；
- Windows/WSL 失败被复现并真实修复；
- method candidate 仍如实报告 0/11；
- 模型调用为 0，没有把工具测试包装为研究效果；
- 已知论文“看过但遗忘”被登记，而非伪装首次发现。

因此不得指控团队造假。

## 7.2 仍存在 false-assurance / QRP 风险

v9 声称：

- “15 承重字段逐行强制”；
- “edge.signal_use ∈ signal.uses”；
- “PDF 页码范围 + 页内 anchor”；
- “散文数字不可能过期而不红”；
- MAJOR-2 已闭合。

本报告的 E1–E5 逐项证明这些完成态陈述超过了当前实现。更合理的表述应是：

> strict/identity/control/selection 的 14 个行级字段已有结构化 evidence；signal/edge 仍是
> locator-level evidence；row hash 防裁决后漂移；release machine block 已对账，但正文尚未
> 生成绑定。

若团队收到这些精确反例后继续对外使用“全部 fail-closed”，QRP 风险会升级；目前仍更像
工程验证不足和完成态夸张，不足以推断主观欺诈。

# 八、窄整改与验收协议

## P0-A：让通用 validator 真正执行 signal/edge schema

必须新增：

1. edge.signal_id 必须存在；
2. edge.signal_use 必须属于所引 signal.uses；
3. edge.decision_right 必须属于 row.decision_rights；
4. use/right 必须属于 allowed relation；
5. 无效 edge 不得只是被 derive 静默忽略，必须让 load-bearing row 失败；
6. 测试必须模拟 **新增的第 12 行**，不得依赖现有 11 行 per-ID expectation。

验收：E1 即使带合法 row hash，仍由 validator 明确失败。

## P0-B：把 signal evidence 从一个自由 locator 升级为字段绑定

建议结构：

```yaml
signals:
  - signal_id: s_stage_judge
    form: scalar_score
    lifecycle: online_step
    uses: [prune]
    claim_evidence:
      form: {kind: canon, value: scalar_score, quote: ...}
      lifecycle: {kind: canon, value: online_step, quote: ...}
      uses: {kind: canon, value: [prune], quote: ...}
```

不要求一字段一段不同引文；同一 quote 可以复用，但必须显式声明它支撑哪些值，并由程序做
value binding。

同时：

- signal evidence 也必须执行 page-range/anchor 检查；
- `pN` 必须附非空、具有最低辨识度的 anchor；
- `pdf_page` evidence kind 要么实现，要么从 taxonomy/docs 删除；
- proposal 中“15”改成真实数量，或把遗漏的选择字段纳入后再给出新数量。

验收：E2、E3、E4 全部红；不能只靠 row hash 红，必须有对应 evidence/schema failure。

## P0-C：让 release binding 真正覆盖读者看到的数字

推荐二选一：

1. headline 表完全由 test JSON 生成，禁止手写；或
2. 用 generated block markers 包住正文表，checker 重新 render 并比较整块字节。

仅检查隐藏 binding block 不够。验收：保持隐藏块不变、把正文 6/11 改为 99/11，检查必须失败。

## P1：已知文献 carry-forward

在 opening tables 新日期版本中补入：

- Mapping Smarter → new-info boundary；
- ASR-TRA → test-time weight/prompt-update boundary；
- Dual-Axis GRM → trained speech reward instrument；
- SDiaReward → trained spoken-dialogue reward instrument；
- Reinforced Agent ACL GEM ID 与 arXiv ID 去重绑定。

只要求角色/ID/route/边界假设，不要求 Stage-1A 深读扩容。

## P2：双平台证据留档

当前事实已由本评审独立复放确认，不是 Gate。后续建议输出：

- Windows report；
- WSL2 report；
- aggregator 对两份 occupancy 做 equality assertion。

不要让同一路径文件由最后一次运行覆盖 platform 字段后，再靠散文声称“双端留痕”。

# 九、放行矩阵

| 放行项 | 当前状态 | 结论 |
|---|---|---|
| Stage-1A / 1B 边界 | PASS | 定义正确，无模型越线 |
| signal-instance 因果派生 | PASS/CLOSED | same-signal + same-use 已实现 |
| WSL2 canonical replay | PASS/CLOSED | 双端 12/12、occupancy 同值 |
| strict tri-state / row-hash | PASS | 可保留 |
| signal/edge 通用 schema validation | FAIL/GATE | E1 可假绿 |
| signal evidence value binding | FAIL/GATE | E2/E4 可假绿 |
| PDF locator claim anchor | FAIL/GATE | 合法范围内错误页 E3 可假绿 |
| release prose binding | FAIL/GATE | 正文 99/11 仍 PASS |
| 新补六篇引用 | PASS | 角色合理，需 ACL ID 去重 |
| 已知文献 carry-forward | REQUIRED P1 | 四项漏入 opening role tables |
| 查询 lane 广度 | PASS | 不新增 lane，不无限延长 1A |
| 是否存在 FFP | NO FINDING | 维持透明更正纪律 |
| 是否签 Stage-1B | **WITHHOLD** | 一项窄 Gate MAJOR + P1 清零后签署 |

# 十、给研究团队 AI 的明确执行要求

1. 不要再提交宏大重写；只交 P0-A/B/C、P1 和机器反例输出。
2. 不要把 row hash 当成语义 validator；它只证明盖章后未漂移。
3. 不要只给现有 11 行增加 expectation；必须测试没有手写 expectation 的新行。
4. 不要把静默丢弃 invalid edge 当作 fail-closed。
5. 不要以 p9999 已失败声称 locator 已解决；必须测试范围内错误页和无 anchor 页。
6. 不要再复制正文 headline；将读者可见表变成生成块。
7. 不要修改 v9；以新的 dated response/supersession 回应。
8. 不要增加模型、smoke、数据集实验或预算 cap；这些与本轮门无关。
9. 不要重开已经关闭的 MAJOR-1/MAJOR-3；修复应保持现有双端与因果正控。
10. 完成窄整改后应立即申请签署，不得以“还能继续找论文”为由再次延迟 Stage-1B。

# 十一、最终意见

v9 是本系列 proposal 中迄今最接近可放行的一版。信号实例化真正解决了 v8 的异信号因果拼接，
canonical path resolver 也真实修复了 WSL2 复放。团队对 CE-v3 的主动披露和对旧 v8 的 dated
supersession 符合诚信要求。

但 v9 把“部分行级 evidence + row hash + 机器块对账”重新命名成了“全部承重字段完备、真实
locator、正文永不陈旧”。作者外反例表明，Stage-1B 新行仍可以携带 signal/edge 自相矛盾、
不存在的 signal 页码或未绑定的 signal form，并在通用 validator/reconciliation 中得到空失败；
正文数字也没有被 release checker 读取。

因此本轮裁决为：

> **当前仍是 Stage-1A 尾门；暂不签 Stage-1B。v8 MAJOR-1 与 MAJOR-3 正式关闭，只保留
> MAJOR-2 的窄幅尾项。完成 P0-A/B/C 与已知文献 P1 后，应立即签署 Stage-1B 系统 mapping，
> 不再扩张 Stage-1A，也不提前运行任何模型实验。**

