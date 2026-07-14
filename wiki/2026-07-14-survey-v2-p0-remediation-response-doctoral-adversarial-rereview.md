---
title: Survey v2 Response 与 P0 整改博导级对抗复审
date: 2026-07-14
stage: Stage-1A
review_type: doctoral-adversarial-remediation-rereview
reviewed_response: wiki/2026-07-14-survey-v2-response-and-p0-remediation.md
reviewed_commit: 9a5bfa6820dbf3bd42c9a70951e991d6545c8605
verdict: RETURN_FOR_MAJOR_REVISION_P0_SIGNOFF_REJECTED
stage1b_authorized: false
owner_decision_requested: false
---

# Survey v2 Response 与 P0 整改博导级对抗复审

## 0. 最终裁决

**裁决：`RETURN_FOR_MAJOR_REVISION`；拒绝签收“P0 八项全部执行”。**

这轮回复比被审 Survey v2 明显更诚实，也完成了若干重要修复：团队承认 round-1 检索永久不可回放，撤回
`Survey complete/调研收官`，没有补造 raw response，没有申请 Stage-1B，纠正了 READ、MBR、TAP-GER、
ProGRes，并提交了能在 clean clone 中确定性重建的 bundle。这些都是真进步。

但“P0 全八项完成”与实际工件不符。本次复核的逐项裁定是：

- **完整关闭 2/8**：P0-1 状态纠偏、P0-2 提交诚实标记缺失的 replay bundle；
- **部分关闭 6/8**：P0-3 计数、P0-4 规范身份去重、P0-5 claim 证据、P0-6 同类事实审计、P0-7 identity、
  P0-8 repo 级禁词/状态门；
- **P1 全部未完成**：团队自己也已承认。

因此当前允许状态仍是 `ROUND1_SCOUT_COMPLETE`，但最大允许的否定性结论还要从回复所写的
`NO_DIRECT_MATCH_WITHIN_LOGGED_SCOPE` 再降一级为：

> **`NO_DIRECT_MATCH_AMONG_RETAINED_RECORDS`**：在目前保留下来的 94 个规则簇中尚未确认直接匹配；
> 由于原始结果宇宙与 screening 轨迹永久缺失，不能声称覆盖了当时的 logged search scope。

本轮没有发现伪造论文、编造实验数据或篡改原始记录的证据，故**不成立 FFP/蓄意学术欺诈指控**。但是，
以下行为构成高风险 QRP/研究治理失实：

1. 把“规则内确定性重建”写成“P0 全部完成”；
2. 把没有 canonical scholarly ID/version 的 94 个记录簇写成“精确 94 篇”；
3. 把不含 claim 文本和证据定位的降级表命名为 `claim_evidence`；
4. 用只能检查自身输出一致性的 12/12 PASS 暗示外部学术正确性；
5. 在 owner 只裁定“允许执行 P0、接受 Stage-1C 门控”的情况下，将 owner 填入 `integrity_reviewer` 签署位；
6. 用四篇/少数论文抽查推出“一手数字全部可溯源”的全称结论。

若团队在看到本复审后仍继续公开使用“P0 全部完成”“精确 94 篇”“owner integrity signoff”“全部数字已
溯源”，风险就会从可纠正的流程缺陷升级为明知证据不足仍作陈述的研究失实。

**不得进入 Stage-1C；不得申请 Stage-1B；当前正确工作是完成 P0-R 真值修复，再做 P1 的可回放 round-2。**

---

## 1. 审查范围与方法

固定审查快照：umbrella commit `9a5bfa6820dbf3bd42c9a70951e991d6545c8605`。

本轮不按成稿论文要求审查，而按 Stage-1A 整改验收审查以下对象：

1. 团队回复是否逐项满足上一轮 P0 的原始语义；
2. 回复的陈述能否由 replay bundle 独立支持；
3. “可重建”“可回放”“可验证”“科学正确”是否被混写；
4. identity 抗辩是已有问题定义，还是看到邻居后形成的合取；
5. 新增最近邻和事实更正是否忠于论文原文；
6. 是否存在选择性呈现、签署冒用、全称外推或其他诚信风险。

实际执行的核查包括：

- 对照上一轮 P0-1…P0-8 和 sign-off checklist；
- 审阅 response、Decision-Log、Research-Objective、evidence archive 和完整 replay bundle；
- 结构化统计 `papers.jsonl` 与 `claim_evidence.jsonl` 的字段完备率；
- 审阅 `build_and_validate.py` 的 alias、claim 和 validator 实现；
- 从 clean local clone 重新执行 `C:\Python314\python.exe build_and_validate.py`；
- 抽查更正论文及新增最近邻的 arXiv 固定版本/正文；
- 对支持方解释、敌意解释与诚信解释分别进行裁决。

clean-clone 重建结果：脚本退出 0，12/12 内部校验通过，生成后 git 工作树保持 clean。这个结果证明
**字节级确定性**，不证明论文去重、claim 真值、coverage 或 novelty 已经正确。

---

## 2. 团队这轮做对了什么

### 2.1 对不可恢复历史采取了正确态度

团队没有根据最终 94 条记录补造 305 次检索的 raw response、结果宇宙和 screening 轨迹，而是明确写成
`RAW_EVENT_UNAVAILABLE`。这是本轮最重要的诚信进步。

`search_events.jsonl` 将 218 次 SEARCH 与 87 次 FETCH 分开，时间戳缺失用 `null`，287 个非明确失败事件
写为 `OUTCOME_UNVERIFIED_RAW_UNAVAILABLE`，没有把“未记录失败”冒充成功。这部分处理严谨。

### 2.2 状态纠偏正确

把 `Survey v2 complete/调研收官` 降为 `ROUND1_SCOUT_COMPLETE`，把决策包降为
`PRE_STAGE1C_DECISION_DRAFT`，并明确不请求 owner 选题、不请求 Stage-1B，符合当前 Stage-1A 阶段。

### 2.3 四项主要事实更正大体正确

- [READ 2606.04680](https://arxiv.org/abs/2606.04680) 的标题和方法已纠正；其摘要只声称最高约 20% relative
  error reduction，团队撤回原来的“~70–85% oracle”是正确的；
- [MBR-ASR 2510.19471v2](https://arxiv.org/abs/2510.19471) 确为 MBR 在 ASR/ST 上的研究，回复将 MBR 与
  ProGRes/Llama-3 comparator 拆开是正确的；
- [TAP-GER 2309.15649v2](https://arxiv.org/abs/2309.15649) 明确同时研究 rescoring 与 generative error
  correction；不能把越过原 N-best oracle 的生成式结果当固定池 selector；
- [ProGRes 2409.00217v2](https://arxiv.org/abs/2409.00217) 明确动态生成新 hypotheses 扩池，回复将其从
  in-pool selector 重分类是正确的。

### 2.4 新增三篇最近邻不是伪造

- [2606.02981](https://arxiv.org/abs/2606.02981)确实用一次 labeled validation sampling 的输出统计预测
  Best-of-N gain，报告 Spearman ρ=0.90；团队将其视为 I4 预测方向的直接压力是合理的；
- [LLM-as-a-Verifier 2607.05391v2](https://arxiv.org/pdf/2607.05391)正文 Table 3 确实并列 Pass@1、oracle
  Pass@N 与 verifier 结果，并称回收了较大部分 oracle headroom；
- [CoVer 2602.12281v2](https://arxiv.org/abs/2602.12281)确实联合扩展 rephrased instructions 与 action
  candidates，再选择高层 prompt 与 action chunks；它是 Proposal E 的强近邻。

因此，本轮问题不是“团队又编了三篇论文”，而是这些核验结果没有以固定版本、locator 和 reviewer 身份进入
正典 claim ledger。

---

## 3. P0 闭环逐项裁定

| P0 | 团队声称 | 本轮裁定 | 原因 |
|---|---|---|---|
| 1 状态纠偏 | 完成 | **CLOSED** | 状态已降级，未申请 1B/1C |
| 2 replay bundle | 完成 | **CLOSED_WITH_PERMANENT_REPLAY_FAILURE** | bundle 可确定性生成，历史缺失未补造；但 search replay 永久失败 |
| 3 分开重算 returned/screened/included/excluded | 完成 | **PARTIAL** | SEARCH/FETCH 和 113→94 有数；returned/screened/included/excluded 仍为 UNKNOWN |
| 4 canonical ID/version/aliases/merge reason | 完成 | **MAJOR_PARTIAL** | aliases/merge_basis 存在；94/94 缺 version、URL、content hash；多数 canonical_key 是短名 |
| 5 39 FT 与承重 claim 审计 | 完成 | **PARTIAL** | 完成统一降级；未形成 113 条 claim+evidence；人类双审和固定版本仍待 P1 |
| 6 四项事实与同类错误普查 | 完成 | **PARTIAL** | 四项主要错误已纠正；没有证明其余数值/operator 已全量审计 |
| 7 bare-I2 与 I2∩I4 拆分、身份冻结 | 完成 | **PARTIAL / DISPUTED** | 名称已拆；但 strict-I2 是 7 月 14 日后见邻居后的合取登记，身份合同仍待 P1 |
| 8 禁词与状态机 fail-fast | 完成 | **PARTIAL** | bundle 内部扫描有效；没有 repo 级状态升级门，也未验证决策包/热状态的语义一致性 |

由此，“P0 全八项完成”“P0 executed”必须被新日期记录 supersede 为：

> **P0-1/P0-2 closed；P0-3…P0-8 partial；P0 sign-off rejected。**

---

## 4. 多轮对抗式评审

### Round 1 — “12/12 PASS”到底证明了什么

支持方最强论点：脚本在 clean clone 中可运行，生成后的 Git diff 为空，所有 manifest hash、行数、外键、
状态 token 和 JSON/YAML 解析都一致，因此 bundle 可重建。

这点成立，但证明范围很窄：

- V2 证明 305 个 event ID 唯一，不证明 305 次检索结果被保存；
- V3 证明 `papers.jsonl` 有 94 个内部 `paper_id`，不证明它们是 94 个真实唯一 scholarly works；
- V4/V5 证明 claim row ID 与 paper FK 一致，不证明 row 中存在可验证 claim；
- V6 重新计算脚本自己生成的计数，不提供独立 gold；
- V7 只证明 grade 被统一压低；
- V8 只扫描脚本挑选的 status-like 字段；
- V9 检查 README 中一个硬编码 token，不能阻止其他文件写 `complete`；
- V10–V12 证明输出完整性和编码格式。

因此准确命名应是：

> `12/12 INTERNAL_BUILD_CONSISTENCY_PASS`，不是 `replay verified`、`survey verified` 或 `P0 verified`。

### Round 2 — “精确 94 篇”是假精确

对 `papers.jsonl` 的字段普查结果：

```text
paper_id        94/94
aliases         94/94
merge_basis     94/94
canonical_id     0/94
version          0/94
title            0/94
url              0/94
content_hash     0/94
```

脚本里的 `canonical_key` 规则是：先从人工 id 字符串中抓第一个 arXiv 样式数字，抓不到就使用第一条人工短名。
因此 `sridhar2019reject`、`chou2023calibration` 这类 key 不是 canonical scholarly ID。

更严重的是，Stage-3 alias 不是通过 DOI/arXiv/OpenAlex/标题作者自动核对得到，而是脚本中的
`ALIAS_CLUSTERS` 硬编码表。两个 initially uncertain pair 被升级为 confirmed 的主要根据又是原 ledger 自己的
`dedup_rule` 预期 lane 数以及 `our_data` 相似。这是**用被审数据自己的预期计数验证合并**，存在循环性。

`uncertain_pairs: []` 也是直接写入的结果；脚本没有对 110 个短名做全对全 bibliographic identity census，
不能证明没有遗漏别名。

正确表述应是：

> `94_RECORD_CLUSTERS_UNDER_EXPLICIT_RULESET`，其 alias 合并可重算；真实唯一 work 数仍未完成规范身份普查。

这不意味着 94 一定错误；意味着现有工件没有资格称它“精确唯一论文数”。

### Round 3 — `claim_evidence.jsonl` 没有承载 claim evidence

113 条基础行实际只有：

```text
claim_id, source_row_id, ledger_row_index, lane, paper_id,
original_grade, effective_grade, downgrade_reason
```

字段普查结果：

```text
claim_text       0/118
paper_version    0/118
source_url       0/118
content_hash     0/118
verified_by      0/118
locator          5/118
```

基础 113 行甚至没有复制原 ledger 的具体 finding/claim，只做了统一 grade cap。因此它是
`claim_grade_reclassification.jsonl`，不是 claim-evidence ledger。

5 条 correction 有 topic、corrected text 和表号，但 verification status 都明确是“单遍 AI 全文重算；人类双审
待 P1”。其中 ProGRes 只写 `arXiv 2409.00217`，甚至没有节/页/表 locator；第 5 条仍明确
`RAW_EVENT_UNAVAILABLE`。

团队完成的是“停止错误上标”，尚未完成“承重 claim 已经有证据”。这两件事不能合并报完成。

### Round 4 — 否定性结论与缺失结果宇宙矛盾

团队一方面正确承认：

- 305 次检索的 raw responses 永久缺失；
- 实际返回的 ranked result universe 永久缺失；
- screening/include/exclude 决策永久缺失；
- round-1 search 本身不可重放。

另一方面却把最大允许结论写成 `NO_DIRECT_MATCH_WITHIN_LOGGED_SCOPE`。

这里的“logged scope”若指全部 305 次查询可能返回的结果，团队没有数据证明每个结果都被筛过；若只指最终
94 个保留簇，则应明确写“among retained records”。现在的措辞把“查询被记下”偷换成“查询结果宇宙被完整
审阅”，不成立。

在 round-2 真正记录 `search_results.jsonl` 和 `screening_decisions.jsonl` 前，禁止以 round-1 支撑
survey-level absence。

### Round 5 — 事实纠正是否可外推为“全部数字真实”

回复 R10 写“一手数字全部可溯源到真实论文真实表格”。本轮证据不支持这个全称命题：

- 团队全文核验了四个主要争议对象；
- evidence lens 抽查的 FT 行只有少数；
- 39/39 FT 原记录没有固定版本和 locator；
- 113 条基础 claim 仍无 claim text；
- 新增三篇尚未进入固定版本 claim ledger。

能够成立的结论是：

> **已抽查的错误数字可追溯到真实论文或真实表格，当前更像提取/归类错误，未发现凭空捏造；未审数字仍是
> 未核验，不得外推。**

这一区别直接关系学术诚信。样本中未发现造假，不等于完成了总体无造假的证明。

### Round 6 — bare-I2 的“格局混合”抗辩不成立

如果 bare-I2 的定义是“存在一种音频接地的冻结 omni selector”，那么只要 audio-understanding/SER 中已有一个
直接实现，它作为宽泛存在性身份就已被占据。ST/SLU 格暂未见同类，只能说明任务覆盖不全，不能恢复宽泛身份的
新颖性。

团队把“身份是否已有实例”和“每个任务格是否都有实例”混成了两个量词：

- novelty identity 通常是存在性问题：是否已有直接方法实例；
- coverage matrix 是全称/分层问题：各任务格是否都被覆盖。

因此推荐裁定：

```text
bare-I2: DIRECT_OCCUPIED_AT_MECHANISM_LEVEL
cross-task coverage: MIXED / UNDERSEARCHED
strict-I2: POST_HOC_NARROWED_CANDIDATE, novelty OPEN
```

### Round 7 — “合取洗白已被日期链反驳”仍然过强

团队正确指出，TH2a 的 same-weights/context-differentiated generator-verifier 和 δ_corr 思路在 2026-07-05 已
存在；I3 的弃权+Goodhart 组合以及 UMBRELLA 的立项也有更早记录。这显著降低“所有组成件都是看到邻居后临时
发明”的嫌疑。

但这不能证明 `strict-I2 = I2∩I4` 这个**具体研究身份**在邻居出现前已经冻结。仓库术语表自己承认
`strict-I2` 命名首现于 2026-07-14，且 response 承认此前“未登记、未标 post-hoc、身份未冻结”。

已有两个组成件 A、B，不等于此前预注册了 A∩B 作为 novelty identity。正确裁定应是：

- “所有技术组成件事后发明”——**REFUTED**；
- “具体 strict-I2 identity 在近邻前已冻结”——**NOT ESTABLISHED**；
- strict-I2 可继续作为 7 月 14 日产生的 post-hoc hypothesis，但不能作为“原身份经攻击仍幸存”的证据。

I3/UMBRELLA 的日期抗辩比 strict-I2 更强，暂接受其定义并非本轮临时合取；仍须在 P1 identity contract 中逐字
固定并做差异审计。

### Round 8 — I4 抗辩在“完全相同对象”层面成立，在“科学贡献”层面未成立

回复说五篇邻居没有完全实现“供给类型轴 c × ρ(c)/H(c)/regret × frozen omni”。字面上可以成立；但科学
新颖性不能靠要求论文使用本项目自造符号或精确轴名。

方法家族已高度拥挤：

- [Snell et al. 2408.03314](https://arxiv.org/abs/2408.03314)按 prompt difficulty 自适应分配 test-time
  compute；
- [VG-Search 2505.11730v2](https://arxiv.org/abs/2505.11730)研究 verifier granularity、budget、
  generator-verifier 与 task attributes；
- [The Art of Scaling TTS 2512.02008](https://arxiv.org/abs/2512.02008)在统一条件下研究 model type、
  problem difficulty、strategy、budget 的最佳选择；
- [Test-Time Personalization 2605.10991](https://arxiv.org/abs/2605.10991)把 BoN curve 分解为四个可测量量，
  研究 reward hacking 和 collapse；
- [2606.02981](https://arxiv.org/abs/2606.02981)直接预测 BoN gain；
- [LLM-as-a-Verifier 2607.05391v2](https://arxiv.org/pdf/2607.05391)直接并列 Pass@1、oracle 与 selector
  realization；
- [CoVer 2602.12281v2](https://arxiv.org/abs/2602.12281)同时改变供给侧 instruction 与候选 action。

因此 I4 的正确状态不是 `DIRECT_OCCUPIED`，也不是 clean whitespace，而是：

> **`METHOD_FAMILY_OCCUPIED; AUDIO/OMNI SUPPLY-STRATIFIED INSTANTIATION UNDERSEARCHED; DISTINCT
> PREDICTIVE CONTRIBUTION NOT YET SHOWN`。**

要形成 proposal，必须提出邻域工作没有的可证伪预测，例如：在不读 label 的条件下，哪一种 pool-side statistic
能跨供给类型预测 rho/regret；在哪些条件下规律反转；该预测相对 difficulty/entropy/disagreement baseline 增加
什么可测信息。仅把已有 scaling surface 换成 c、H(c)、ρ(c) 记号不构成创新。

### Round 9 — 签署与独立性

response 的 `generated_by` 和 `verified_by` 都由同一个 Claude Fable 5 主会话承担；五个 lens 虽是不同 agent ID，
但同模型、同工作流、同协调者汇总。它们适合内部 adversarial QA，不等于未参与生成的独立 scientific reviewer。

团队已将 independent reviewer 标 `PENDING`，这部分诚实。

但 `integrity_reviewer` 填写 owner 并给出 signed_at，所列 owner 行为只是：

1. P0 核验完允许执行；
2. 接受 P0+P1 关闭后再进入 Stage-1C 的门控。

这不等同于 owner 已审阅 bundle、重算 94、确认四项更正或签署诚信结论。除非存在 owner 对**精确响应字节和
verdict**的明确签名，当前写法构成 signature-role inflation。

必须改为：

```yaml
integrity_reviewer:
  id: "PENDING"
owner_adjudications:
  - "authorized P0 execution after verification"
  - "accepted P0+P1 gate before Stage-1C request"
```

owner 的治理裁决应被尊重，但不能被扩写成未发生的审计签署。

---

## 5. 学术欺诈与不当研究实践裁定

### 5.1 FFP：当前不成立

| 风险 | 本轮证据 | 裁定 |
|---|---|---|
| Fabrication：虚构论文/数据 | 抽查论文均真实；错误数字可追到论文表格或算子误读 | **NOT ESTABLISHED** |
| Falsification：篡改原始记录 | 旧工件保留，缺失日志未补造，使用 supersession | **NOT ESTABLISHED** |
| Plagiarism | 本轮无相关证据 | **NOT ASSESSED / NO INDICATION** |

### 5.2 QRP/治理失实：高风险

| 风险 | 严重度 | 说明 |
|---|---:|---|
| 完成状态上标 | **FUNDAMENTAL** | 2/8 closed 却写 P0 全部完成 |
| 假精确论文数 | **MAJOR** | 94 是规则簇数，不是 canonical work census |
| claim-evidence 名实不符 | **MAJOR** | 113 基础行无 claim/evidence locator |
| 否定性结果过界 | **FUNDAMENTAL** | 无结果宇宙却写 within logged scope |
| 全称无造假式外推 | **MAJOR** | 少数抽查推出“全部数字可溯源” |
| owner 签署角色膨胀 | **FUNDAMENTAL** | governance adjudication 被写入 integrity reviewer 位 |
| 自验证当独立验证 | **MAJOR** | 同脚本/同模型验证内部一致性 |
| post-hoc identity 洗白风险 | **MAJOR** | 组成件预先存在不等于合取身份预冻结 |

本轮最危险的不是某个表格数字，而是**把真实但有限的修复包装成全面关闭**。这与上一轮“batch complete 写成
survey complete”是同一类行为，只是换成了“internal consistency pass 写成 P0 complete”。说明团队的完成状态
控制问题仍未根治。

---

## 6. 对正在处理的 P1 工作的评价

团队列出的 P1 方向总体正确：继续 9+8 最近邻、未来检索保存 raw response、冻结 identity、重建 comparator、
C1/C4、双审和独立盲重建。这说明团队理解下一步不能直接选题。

但执行顺序仍需重排。当前 P1 直接建立在错误的“P0 已完成”基线上；若先扩充 17 篇，会把短名、空 claim、
无版本、模糊 operator 继续放大。

### 正确顺序

1. **P0-R 真值修复**：先修 94、claim ledger、状态、签署与最大允许结论；
2. **Identity freeze**：冻结 bare-I2、strict-I2、I3、I4、UMBRELLA 的 exact contract 和量词；strict-I2 标
   `post_hoc_created_at=2026-07-14`；
3. **Round-2 protocol freeze**：数据库、query families、aliases、时间窗、纳排、stopping rule、版本策略；
4. **执行可回放 search**：每个 SearchEvent 保存 raw response hash；每个 result 保存 rank 和 screening decision；
5. **建立 claim-level evidence**：先完成所有 load-bearing claims，再做非承重 broad records；
6. **同协议 comparator cards**：只有 operator taxonomy 与 evidence 完成后再重建；
7. **C1/C4 与负结果**：registry 和所有失败/排除进入分母；
8. **独立盲重建**：由未参与生成的人/代理对固定 hash 进行，机械复现与科学复核分开签；
9. **申请 STAGE1C_DECISION_READY**：所有 blocker 关闭后再交 owner，仍不自动进入 Stage-1B。

### P1 还缺的设计

- 17 个 target 只是 seed list，不是 saturation protocol；
- 必须做 forward/backward citation chase，但也要有同义词、方法别名、跨领域 query expansion；
- 必须预先定义“何时停止”，不能在找到支持空白的论文后停止；
- 必须区分 work identity、version identity 与 claim identity；
- 对不存在性结论要报告数据库和日期边界；
- 对 newly found direct neighbor，要允许 kill，而不是继续添加限定词；
- AI reviewer 与 human reviewer 的最高证据等级必须分开。

---

## 7. 必须执行的 P0-R 修复单

### P0-R1：状态和签署纠偏

- 新建日期 response supersede “P0 全八项完成”；
- Decision-Log 和 Research-Objective 把 P0 改为 `2 CLOSED + 6 PARTIAL`；
- `integrity_reviewer` 置 PENDING；owner 裁决单列；
- `12/12 PASS` 前缀固定为 `INTERNAL_BUILD_CONSISTENCY`。

**验收**：repo 热状态中不存在将当前 bundle 描述为 independent replay pass/P0 complete 的无界定文字。

### P0-R2：把 94 从“篇数”降为“规则簇数”

- 当前先统一写 `94 record clusters under v1 ruleset`；
- 为每个 work 补 arXiv ID/DOI/OpenAlex ID 中至少一个 canonical ID；
- 记录 title、authors、version、version date、source URL、content hash；
- alias merge 不能以原 ledger 期望 count 作为主要证据；
- 对无 canonical ID 的条目标 `IDENTITY_UNRESOLVED`，不得计入 exact unique works。

**验收**：脚本分别输出 `record_clusters`、`identity_resolved_works`、`versions`、`identity_unresolved`；不得只给一个 94。

### P0-R3：重建真正的 claim ledger

每个 load-bearing claim 至少包括：

```text
claim_id
paper_work_id
paper_version_id
exact_claim_text
team_interpretation
operator_type
source_locator
source_content_hash
support_relation
generated_by
verified_by
verification_status
```

非承重 broad survey 记录可以停在 ABSTRACT_VERIFIED，但不得以其 support/kill scientific identity。

**验收**：所有 kill、occupancy、novelty、numeric headline、operator classification 100% 有固定版本和 locator；
人类未双审时明确封顶，不得写 final kill。

### P0-R4：拆分三种复核

1. build reproducibility：脚本/哈希/格式；
2. bibliographic audit：身份、版本、去重；
3. scientific claim audit：原文、数字、operator、推理。

三者分别出 verdict，禁止一个 12/12 总分覆盖三类问题。

### P0-R5：纠正最大允许结论

round-1 只允许：

```text
NO_DIRECT_MATCH_AMONG_RETAINED_RECORDS
SEARCH_RESULT_UNIVERSE_UNAVAILABLE
SCIENTIFIC_SATURATION_NOT_ASSESSABLE
```

round-2 通过可回放 protocol 后，才可使用 `WITHIN_PROTOCOL` 或 `WITHIN_LOGGED_SCOPE`。

### P0-R6：身份量词与 post-hoc 日志

- bare-I2 用存在性身份判断，记 mechanism occupied；
- task matrix 单独报告 mixed coverage；
- strict-I2 标明 2026-07-14 post-hoc synthesis；
- 任何新增限定都记录“新增时间、触发论文、是否改变 novelty verdict”；
- I4 不得以符号不同作为新颖性，必须给出新预测或新约束。

### P0-R7：同类错误普查

四篇纠正不是普查完成。应对所有 load-bearing records 运行：

- selector / generator / revision / tool loop / weight-update 分类；
- pool 是否改变；
- verifier 是否 trained/external/same-core；
- 数字的 dataset/split/model/K/budget/metric；
- oracle 定义和分母；
- 固定版本与表格 locator。

**验收**：抽取表由另一 reviewer 随机复核；发现一条同类错误即扩大复核范围。

### P0-R8：真实 repo 级状态门

validator 必须读取 response、hot status、decision package、claim ledger 与 signoff，而不是只检查自己生成的 README。

至少 fail closed：

- search universe 缺失却出现 `WITHIN_LOGGED_SCOPE`；
- identity unresolved 却出现 exact unique work count；
- load-bearing claim 无 locator 却出现 kill/occupied/verified；
- independent reviewer pending 却出现 independent replay passed；
- owner 未签 exact hash 却进入 integrity reviewer；
- P0/P1 blocker 非空却出现 `STAGE1C_DECISION_READY`。

---

## 8. 可保留的 proposal 探索方向

本复审不是要求团队停止探索。相反，以下方向值得保留，但必须作为问题候选而不是已证空白：

### A. Label-free gain prediction

对抗 [2606.02981](https://arxiv.org/abs/2606.02981) 的 labeled predictor：能否仅凭 pool 内 disagreement、
audio-text grounding、selector score geometry 与 supply metadata，预测 H(c)、rho 或 regret？

检查点：相对 difficulty、entropy、agreement、length 等通用 baseline 是否有跨模型/任务增量预测力。

### B. Supply–selector interaction

对抗 [CoVer](https://arxiv.org/abs/2602.12281)：供给选择与候选选择是否存在不可分离的 interaction？固定总预算
下，先选供给再选候选是否优于联合选择或 one-shot BoN？

检查点：必须分解 supply gain、selection gain、interaction，不能把扩池收益记到 selector。

### C. Verifier scaling 与 Goodhart

对抗 [LLM-as-a-Verifier](https://arxiv.org/pdf/2607.05391) 和
[Test-Time Personalization](https://arxiv.org/abs/2605.10991)：增大 verifier granularity/repetition/K 时，何时
rho 上升，何时 reward hacking 使真实 U 下降？能否 label-free 检测拐点并弃权？

检查点：same-core/shared-bias、不同模型 verifier、gold-free proxy 与真实 U 的分离。

### D. Audio/omni domain transfer law

不是“文本方法搬到音频就是创新”，而是检验文本/VLA scaling law 在 audio-conditioned frozen omni 上何时失效。

检查点：音频编码成本、长上下文、ASR corruption、模态 grounding、任务效用异质性是否产生可预测的 regime
change；若没有，就只能算实例化/工程贡献。

### E. Negative-result knowledge

把 underperformance、pool collapse、headroom absent、selector failure、identity kill 作为一等知识对象。

检查点：失败是否进入搜索/尝试分母；能否从失败推导下一轮 query 或 kill，而不是从最终成功叙事反推轨迹。

---

## 9. Reviewer sign-off

```yaml
reviewer_verdict: RETURN_FOR_MAJOR_REVISION_P0_SIGNOFF_REJECTED
stage: Stage-1A
accepted_progress:
  - honest RAW_EVENT_UNAVAILABLE handling
  - deterministic clean-clone bundle rebuild
  - state downgrade to ROUND1_SCOUT_COMPLETE
  - READ/MBR/TAP-GER/ProGRes corrections
  - no Stage-1B or Stage-1C request
p0_closure:
  closed: [P0-1, P0-2]
  partial: [P0-3, P0-4, P0-5, P0-6, P0-7, P0-8]
integrity_assessment:
  fabrication: NOT_ESTABLISHED
  falsification: NOT_ESTABLISHED
  plagiarism: NOT_ASSESSED_NO_INDICATION
  qrp_governance_risk: HIGH
required_next_state: P0_REMEDIATION_IN_PROGRESS
maximum_permitted_claim: NO_DIRECT_MATCH_AMONG_RETAINED_RECORDS
owner_decision_requested: false
stage1b_authorized: false
unresolved_blockers:
  - canonical scholarly identity and version census absent
  - round-1 search result universe and screening trail permanently unavailable
  - real claim-evidence ledger absent
  - load-bearing human double review absent
  - identity contract and post-hoc log not frozen
  - repo-level state gate not demonstrated
  - independent blind scientific review absent
  - integrity_reviewer attribution requires correction or explicit exact-hash owner signature
```

## 10. 最终博导意见

这支团队已经证明自己愿意承认错误，也有能力快速制造大量审计工件；问题是它仍然习惯把“工件生成成功”写成
“科学整改完成”。本轮的 12/12 PASS 与上一轮的 “Survey complete” 具有同一结构：局部目标达成后，状态被
提升到超出证据覆盖的层级。

真正的修复不是再增加一个更长的 validator，而是建立三条不可混淆的线：

1. **字节能否重建**；
2. **文献身份和检索宇宙能否审计**；
3. **科学 claim 是否被原文支持**。

团队在第一条取得了明显进展，在第二条只完成了规则内聚类，在第三条只完成了少数更正和全量降级。把这三条
如实分开，当前工作就是合格且有价值的 Stage-1A 整改；把它们重新合并成“P0 全部完成”，就会继续积累不当
研究实践风险。

本轮最稳妥、也最严厉的结论是：**没有证据证明团队在造假；但也没有证据允许团队宣称整改闭环。继续研究可以，
继续上标不可以。**
