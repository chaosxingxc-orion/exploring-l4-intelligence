---
title: "Stage-1A working brief 快速收敛独立复审"
date: 2026-07-21
review_role: "independent doctoral reviewer"
review_mode: "scientific-readiness-first; minimal tooling gate"
reviewed_artifact: ".worktrees/stage1b-readiness-remediation/wiki/survey/workbench/system-first-stage1a/2026-07-21-stage1a-working-brief.md"
reviewed_commit: "c01fba751b56588ed2f62cb6d01f6c25f3e95539"
reviewed_git_blob: "c6bf1dcd8fbd009f6596d0bf8a057de83c5d962e"
reviewed_blob_sha256: "bff3e6031eeec73cfd5f8d262e6fc8c325a75ec4178e0f7a28b0c0f111a20d5f"
reviewed_blob_bytes: 47433
reviewed_worktree_modified: false
supersession_scope: "supersedes the Stage-1B WITHHOLD recommendation for the newer frozen artifact only; prior factual findings remain historical evidence"
---

# Stage-1A working brief 快速收敛独立复审

## 0. 最终裁决

当前形式阶段仍是 **Stage-1A final remediation**，因为第一条 systematic discovery query 尚未执行，owner 也尚未授权 Stage-1B。可是从科学设计成熟度判断，团队已经达到 **可以结束 Stage-1A、立即转入 Stage-1B systematic mapping** 的水平。

本轮正式建议如下：

```text
CURRENT_STAGE = STAGE_1A_FINAL_REMEDIATION
SCIENTIFIC_RATIONALE_FOR_MAPPING = ADEQUATE
SEARCH_DESIGN_SIGNOFF = SIGN
STAGE_1B_START_RECOMMENDATION = GO_AFTER_OWNER_SAME_PACKAGE_AUTHORIZATION
H5_LOAD_BEARING_USE = WITHHOLD_UNTIL_BLIND_CODER_B_AND_ADJUDICATION
RESEARCH_MODEL_OR_SMOKE_IN_STAGE_1B = PROHIBITED
ACADEMIC_FRAUD_EVIDENCE = NOT_ESTABLISHED
```

关键变化是：**H5 coder-B 不再作为第一条 query 的前置阻塞。**它只阻塞 H5 七字段进入承重统计、gap claim 和 Stage-1C 综合。检索、去重、题录筛选、引文闭包、非 H5 字段的全文编码可以立即开始。

这是严格的分层放行，不是降低科学标准：不让一个 non-load-bearing calibration 无限阻塞整个 systematic mapping，也不允许未校准字段偷偷承重。

## 1. 为什么本轮可以从 WITHHOLD 改为 SIGN

上一冻结对象是 commit `9e708c5`。本轮对象已经更新为 commit `c01fba7`，不能沿用上一报告对旧 artifact 的 gate 结论。

团队已经实质修复此前会污染科学结果的四项问题：

1. H5 codebook V2 已明确 method-path 分析单位、core/system 层级、七字段定义和 tie-breaker；
2. coder A 的 21 个 locator 已改为 typed exact anchors，并声明在冻结 PDF 上 21/21 回放；
3. agreement 已由 coder rows 派生，已固化上一轮提出的两类 false-green regression；
4. 已形成不含 coder-A 值的 blind packet；
5. Omni-Decision 与 AOP-Agent 已提升为 P1 direct/deep-read，Light-Omni 与 LatentOmni 已路由为非阻塞 trained boundary comparators；
6. corpus 更新为 508 source rows、253 canonical works、93 official-receipt bibliography works 和 19 reviewer-known items。

本轮只做了最小包检查：draft `PASS`，release 仍因 H5、fresh v7 leaves 和未 promotion 而 `FAIL`。这表示工具如实报告现状，但**release-tool chain 是否全部完成不应再等同于 systematic mapping 是否可以开始**。

上一轮把 H5 completion 和完整 v7 发布链都视作第一条 query 的绝对前置，按当前“尽快开展 survey”的阶段使命看过于保守。H5 是编码子合同，不是 search recall、identity dedup 或 title/abstract screening 的因果前置。继续等待只会推迟真正能发现遗漏 prior 的工作。

## 2. 当前阶段的准确解释

### 2.1 形式状态

截至冻结 commit：

- Stage-1B 尚未开始；
- systematic discovery query = 0；
- research model/smoke = 0；
- dataset metric/prototype = 0；
- `INHERITED_PRIOR_EXPOSURE` 非零且未被覆盖；
- owner 尚未产生 Stage-1B authorization。

所以不能把当前历史状态写成“已经在 Stage-1B”。

### 2.2 科学就绪状态

Stage-1A 应回答的是：问题是否值得 survey、检索和纳排规则是否可执行、编码框架是否足以开始积累证据、已知 prior 是否被合理路由、阶段边界是否清楚。

当前交付物已经给出：

- RQ-SYS / RQ-MECH / RQ-SUPPLY-MAP / RQ-VERIFY-MAP / RQ-BOUND；
- frozen query/compiler、T1 proceedings routes、snowballing、REC-0 至 REC-7；
- D0/D1/D2 evidence grade；
- canonical-work dedup 与 claim hyperedge；
- coder/adjudicator 分离；
- exit/reopen 与 exposure 记账；
- Stage-1B、1C、2A、2B 的责任分界。

这已经超过“继续设计 proposal”的边际收益点。下一步最有信息增益的行动是执行 mapping，而不是继续强化门禁脚本。

## 3. 引用是否合理

### 3.1 总体结论：合理，可支持开始 survey

引用系统目前已经能支持 Stage-1B 启动：

- 书目身份来自 official raw receipt，并可离线重建；
- known-ID access 全部 `query_recall_credit=false`；
- metadata、abstract、fulltext 的证据等级没有混用；
- bibliography 明确只是 reviewer orientation subset，不冒充 mapping denominator；
- direct prior、trained comparator、reward/measurement、known queue 已分层；
- working brief 不再声称 first-ever，也不在 Stage-1A 给出技术 novelty verdict。

尤其是以下整改是科学上必要且已经完成的：

- [Omni-Decision](https://arxiv.org/abs/2607.11433) 已从低优先级 queue 修正为 P1 direct neighbor；
- [AOP-Agent](https://arxiv.org/abs/2605.28192) 已登记为无额外训练的 active omni-perception direct neighbor；
- [Light-Omni](https://arxiv.org/abs/2607.05511) 经全文确认含 learnable soft prompts/trained adapters，被放入 trained boundary；
- [LatentOmni](https://arxiv.org/abs/2605.22012) 因 supervised fine-tuning/latent supervision 被放入 trained/white-box boundary。

这些分类不证明项目创新，但已经足够证明 protocol 能容纳最接近的已知反例。

### 3.2 仍需保留的引用纪律

Stage-1B 中必须继续坚持：

- 论文最终分数不能替代 method-path 编码；
- “training-free”自称不能替代核心/外围更新、white-box access、new-info、human/dev selection 的逐项判断；
- direct neighbor 必须编码 action rights、state lifecycle、verification、stopping 和信息边界；
- `DEEPLY_READ` 只表示达到 D2，不表示该论文已被正确因果归因；
- 任何 gap/novelty 结论都留到 Stage-1C，不在 screening 过程中形成。

## 4. 是否仍有论文遗漏

### 4.1 不能、也不应该在 Stage-1A 宣称“无遗漏”

当前 253-work union 和 93-work bibliography 已经是良好起点，但 systematic discovery 尚未执行，所以此时最多能说“已知直接邻居已获得合理覆盖”，不能说 recall 完整。

这不是新的 Stage-1A blocker，而正是启动 Stage-1B 的理由。

### 4.2 本轮快速抽查发现的非阻塞 queue

本轮只做一轮窄检索，发现两个尚未出现在本地 corpus 的相关方法：

1. [OmniSelect: Dynamic Modality-Aware Token Compression](https://arxiv.org/abs/2605.18041)：training-free、使用 AudioCLIP relevance 做动态 token pruning。它可能属于供给侧控制／trained peripheral boundary，需要 Stage-1B 判断其是否满足黑盒边界。
2. [OmniDrop: Layer-wise Token Pruning](https://arxiv.org/abs/2605.14458)：在 decoder layers 内做 query-guided pruning，明显需要内部 token/layer access，优先作为 white-box/structure boundary comparator。

处理要求很简单：将二者登记为 reviewer-known、`query_recall_credit=false`，放入 Stage-1B opening queue。**不要求在 Stage-1A 深读，不得因此延迟第一条 query。**

除此之外，本报告不再追加“先找到更多论文才能开始”的开放式要求。漏检风险应由 frozen routes、snowballing、citation closure 和 exit mechanism 在 Stage-1B 中正式处理。

## 5. 是否存在超越本阶段的探索

### 5.1 没有执行层越界

未发现本轮执行：

- 研究模型或 smoke；
- 数据集推理；
- WER/EM/headroom/selector 实验；
- prototype；
- 用小样结果选择技术路线。

known-ID 全文读取、H5 人工校准、query compiler 和 evidence schema 均属于 survey readiness，而不是 Stage-2 实验。

### 5.2 对未来实验的描述没有构成越界

working brief 中的 matched ablation、MBR、oracle、SESOI、复现优先等内容是阶段责任和 falsifier 的预告，没有被写成已执行结果。它们能防止 Stage-1B 把论文报告值和项目新实验混在一起，应保留。

### 5.3 当前反而存在“停留过久”的风险

现阶段最大的范围风险已不是过早实验，而是继续围绕 package、manifest、mutation 和跨平台形式证明反复整改，挤占 systematic mapping 本身。

从本报告开始，除非出现会直接造成数据丢失、论文身份错配、纳排不可执行或证据越界的错误，否则一般代码健壮性问题应进入普通 backlog，不再阻塞 Stage-1B。

## 6. H5 应如何与 Stage-1B 并行

H5 coder-B 尚未完成，但 H5 calibration 明确是 non-load-bearing。正确做法不是继续全局 WITHHOLD，而是拆分权限：

### 现在可以开始

- frozen discovery queries；
- proceedings/T1 routes；
- canonical identity 与 dedup；
- title/abstract screening；
- backward/forward snowballing；
- REC-0 exclusion ledger；
- non-H5 method-path fields；
- D2 fulltext acquisition与普通事实编码；
- Omni-Decision/AOP-Agent opening-prior coding。

### H5 闭合前禁止

- 把七字段编码用于 headline/gap claim；
- 报告 H5 occupancy、agreement 或 speech-specific conclusion；
- 用 coder A 单方值筛掉论文；
- 将 H5 结果送入 Stage-1C candidate cards；
- 因 codebook 尚未完全校准而事后改写 frozen search query。

### 并行完成

- 独立 coder B 的 3×7 blind pass；
- 第三方 disagreement adjudication；
- calibration 完成后再启用 H5 load-bearing coding。

如果 coder B 暴露 codebook 实质歧义，只重做已经发生的少量 H5 字段编码；不要回滚 identity、screening 和非 H5 mapping。

## 7. 最小开门流程

不需要再经过一轮大型整改。建议按以下最短路径执行：

1. 将 commit `c01fba7` 及本报告登记为 exact-package review input；
2. owner 对该 commit 作 dated Stage-1B authorization，并明确 `H5_LOAD_BEARING_USE=WITHHOLD`；
3. 立即执行第一条 frozen query，开始 attempt/receipt 记账；
4. 同期把 OmniSelect/OmniDrop 登记为 reviewer-known opening queue，不计 recall；
5. coder B 与 adjudicator 独立并行，不阻塞检索和筛选；
6. H5 完成后只开启七字段承重，不重开已冻结 query；
7. Stage-1B 全程继续禁止研究模型、smoke 和任务指标实验。

原先的 fresh v7 dual-platform leaves、aggregate 和 formal promotion 可以作为记录层收尾并行完成，但不再建议将其设为第一条 discovery query 的科学前置。若 owner 仍要求完整发布仪式，可以在不改变 Stage-1B 数据语义的前提下尽快补齐，不应继续展开新的 robustness campaign。

## 8. 学术诚信判断

当前没有 fabrication、falsification 或 plagiarism 证据。团队：

- 保留了 H5 pending 和 release blocked；
- 接受了负证据反例；
- 没有把 reviewer-known paper 计为 query recall；
- 没有把 D1 metadata 冒充 D2 mechanism；
- 没有把 known-prior routing 写成 novelty 证明；
- 没有隐藏 inherited exposure。

因此没有理由继续以“潜在造假”作为默认阻塞。后续诚信重点应转到正常 systematic review 风险：漏检、双人筛选独立性、选择性全文升级、negative evidence、重复 work 和无证据 gap claim。

## 9. 博导结论

这份交付物已经完成 Stage-1A 的主要使命。引用链与本地论文集足以作为 systematic mapping 的起点，直接邻居已得到合理纠偏，阶段边界清楚，且没有偷跑实验。

严格审稿并不意味着必须等待所有非承重子合同和工具发布链完美无缺。真正严格的做法是让限制跟随它所保护的结论：H5 未校准，就禁止 H5 承重；但不应禁止与 H5 无关的检索、去重和筛选。

因此，本轮给出 **search design SIGN**。在 owner 对冻结 commit 作同包授权后，团队应立即进入 Stage-1B，停止继续围绕一般代码鲁棒性扩展审查，把主要精力投入 systematic survey execution。

