---
title: "Gate S1 再送签申请的 Stage-1A 博导级对抗复审"
date: "2026-07-16"
reviewed_artifact: "wiki/survey/2026-07-16-gate-s1-rereview-application.md"
review_role: "严格审稿人 / 博士生导师 / 研究诚信核查"
stage_basis: "Stage-1A 收官准备末段（survey-ready gate）；Stage-1B 尚未正式放行"
decision: "WITHHOLD SIGNATURE — TARGETED CORRECTION #4 REQUIRED"
mutation_policy: "独立日期化报告；不改写被审材料及团队在研文件"
---

# Gate S1 再送签申请的 Stage-1A 博导级对抗复审

## 0. 复审对象、边界与裁决标准

本报告复审以下申请：

- [Gate S1 search-design 窄幅复核申请书](survey/2026-07-16-gate-s1-rereview-application.md)；
- 申请书所指向的 correction #3 固定 bundle；
- 与 G1–G6 直接相关的协议、冻结查询、种子 manifest、T1 proceedings routes、空白记录模板和静态验证材料；
- 当前热层对 Stage-1A / Stage-1B 状态的正式表述。

本报告不修改任何团队文件，不替团队补写协议，不把 Stage-1A 当作一篇已经完成实验和统计分析的论文来审，也不以 Stage-2/Stage-3 的统计显著性、SESOI、完整消融或成本最优要求倒逼当前阶段。

但 Gate S1 是“是否允许开始系统检索”的方法学门，而不是鼓励性评语。其最低标准是：搜索设计必须能够被另一名执行者按固定对象重放；关键字段不能依赖口头解释；“已完成”“已实例化”“机器验证通过”等完成性陈述必须与仓内证据一一对应。

### 0.1 快照

- 复审时 HEAD：`99aa5a408cbb776c2ff0bb09d764d1596a89fc3b`。
- 被审申请书 git blob：`a81a01c03dac7e306a05e6629629b85a139e5822`。
- 被审申请书工作树 SHA-256：`A3B2042EA8ADC2FEBB08426CDACF5B398A804B9C2BFF535D209BD75303674B4A`。
- correction #3 所钉 17 件对象：独立逐项重算为 `17/17 PASS`；当前 HEAD 中这些对象没有发生漂移。
- 冻结种子：74 行、74 个唯一记录；其中本轮补充批 14 条。
- 冻结查询：51 行、51 个唯一 `query_id`；原 48 行前缀保持不变，新增 3 行。
- reviewer、owner execution approval、P0-R8 三处执行签名仍为空。
- `wiki/survey/replay/SF-SURVEY-2026` 尚不存在；在仓内可见范围内，“签署前零查询”与现状一致。

### 0.2 阶段事实必须先纠正

用户描述为“Stage1B 阶段正在开始”，但项目正式热层仍明确记载：

1. 当前是 **Stage-1A 收官准备末段（survey-ready gate）**；
2. Gate S1 尚未签署；
3. reviewer 签署、owner 执行批准、P0-R8 复跑三者缺一不可，之后才允许首条 survey 查询；
4. Stage-1A close 与 Stage-1B release 是两个不同签字；
5. Stage-1B 尚未放行。

因此，本报告采用可审计正典而不是口头简称：**Stage-1B 可以处于启动准备，但不能被表述为已经开始执行。** 允许准备 probe card、配置 schema 和停止条件；不允许在独立的 Stage-1B 放行前运行模型、数据集、headroom、MBR、selector 或外部控制平面方向性实验。

这不是过度保守，而是防止 Stage-1A 的 survey 证据与 Stage-1B 的原型结果相互污染，也防止团队在尚未完成问题地图时因早期偶然结果改变检索、纳排和承重规则。

## 1. 总裁决

**裁决：WITHHOLD SIGNATURE — TARGETED CORRECTION #4 REQUIRED。**

不要求 proposal v4，不要求重做整个方案，不要求预算 cap，也不要求现在跑任何模型实验。只要求对仍未闭合的搜索设计和记录合同做一次窄幅、可机器检查的 correction #4，然后立即复核签署。

团队这一轮不是“没有做事”。相反，G1 的降名与开放获取救援、G4 的五类合同传播、G5 的 bundle 重钉、G6 的年→月→日递归方向，都是真实而有价值的修复。申请书还主动披露了两处与前评审建议的偏离，这一点符合研究诚信要求。

但是，申请书把“部分闭合或纸面展开”写成“G1–G6 全闭合”，尤其把 10 行范围表达称为“50 条 route 实例化”，把未持久化的会话内检查称为“机器验证”，已经构成**材料性的 claim–evidence mismatch**。在 Gate S1 上，这足以暂缓签字。

### 1.1 G1–G6 分项裁决

| 项 | 团队申请 | 本次裁决 | 核心理由 |
|---|---|---|---|
| G1 | 已闭合 | **CLOSED WITH LIMITATION** | arXiv-primary 已降名，免费官方源救援和付费移除记账基本合理；仍须保持有界覆盖表述，不能升级为全领域穷尽性结论。 |
| G2 | 已闭合 | **NOT CLOSED** | `venue_tier` 仍被当作证据权重先验；T2 混合 preprint、同行评审期刊与非清单会议，却统一把实验数字默认标为 `T2_UNREVIEWED`，逻辑上错误。质量轴只有三档加一句理由，复核性不足。 |
| G3 | 已闭合 | **NOT CLOSED** | 文件只有 10 行范围写法，不是 50 条逐条序列化 route；入口不是完整 URL，存在 `ENTRY_TO_RESOLVE`；7/7 验证器及其输出没有持久化。 |
| G4 | 已闭合 | **原要求形式闭合，但执行记录系统仍不闭合** | 五类合同确实进入 REC-2；但 REC-2 只记录 INCLUDED，缺少工作级去重、筛选阶段、排除、检索失败与裁决 provenance。字段还存在重复和机器语义歧义。 |
| G5 | 已闭合 | **CLOSED** | correction #3 的 17 件固定对象独立核验 17/17 一致，是本轮最扎实的闭合项。当前热层是 bundle 外状态证据，不应混作签名对象。 |
| G6 | 已闭合 | **PARTIALLY CLOSED** | 递归层级已补；派生子查询的精确边界、字符串、hash、窗口语义和请求节流仍未进入可重放记录。 |

### 1.2 可否签署

现在不能签。阻断项不是“论文数量还不够多”，而是四个很窄的协议问题：

1. G2 的 venue 与 study quality 仍混淆；
2. G3 没有 50 条真实 route 记录，也没有仓内可复跑验证器；
3. G4 缺少完整的工作级筛选/去重/裁决记录；
4. G6 派生查询不可精确重建。

此外，查询类目存在 `cs.SE` / `cs.HC` 盲区，已由直接邻近论文反证，必须在首条查询前处理。

## 2. 对团队回复质量的总体评价

### 2.1 做对的部分

1. **把检索产出降名为 arXiv-primary systematic mapping。** 这使结论强度与来源边界更一致。
2. **采用免费官方开放获取救援。** ACL Anthology、PMLR、OpenReview、CVF、ISCA 等能够覆盖大量高价值正式工作，并允许版本钉定与本地 hash。
3. **保留付费不可得工作的身份和计数。** 虽不纳入承重，但至少不会在 coverage flow 中无声消失。
4. **将来源、omni 五轴、RL 身份、TF 审计和 evidence axes 传播到 REC-2。** 这解决了前一轮“散文有定义、数据结构没有”的主要问题。
5. **重新钉定 correction #3 bundle。** 17/17 一致性可以独立验证，不是单纯自述。
6. **维护零查询边界。** 目前没有发现团队先跑结果、再改搜索协议的仓内证据。
7. **区分 reviewer、owner 和 P0-R8。** 权责分离符合 Gate 的设计目标。
8. **主动披露两处偏离。** 这比用措辞掩盖分歧更可取。

### 2.2 仍不合格的部分

团队把“有设计”与“已实例化”、把“会话里跑过检查”与“检查证据已持久化”、把“原 G4 字段已加入”与“完整记录系统已可执行”混在了一起。

对普通工作笔记，这可能只是措辞不严；对签核申请，它会误导签署者认为另一名研究者已经可以无解释地重放 50 条 route、重建派生查询并复核每篇工作的纳排链。当前事实并非如此。

博士研究训练中，最危险的习惯不是出现缺口，而是用完成态语言覆盖缺口。团队现在必须把完成性陈述收回到证据实际达到的级别。

## 3. G1：检索宇宙与开放获取政策

### 3.1 为什么本项可以“有限闭合”

协议已明确：

- 51 条预注册检索全部经 arXiv API；
- Semantic Scholar / OpenAlex 只作发现层，命中回 arXiv 或免费官方全文；
- 无 arXiv 版本但存在官方开放获取全文时，可用 venue-native ID / DOI、本地备份和 SHA-256 纳入；
- 付费且无免费版本者标 `REMOVED_PAYWALLED_UNOBTAINABLE`，在 flow report 保留 ID、题名、venue 与计数；
- 最终成果不称 comprehensive universe。

这与“受限来源的系统映射”是相容的。PRISMA-S 要求完整记录信息源、检索策略、补充检索路径以及去重方式，而不是强迫任何综述购买全部付费材料；但来源限制必须与结论强度同步披露。[PRISMA-S](https://pmc.ncbi.nlm.nih.gov/articles/PMC8270366/)

### 3.2 不能再越过的结论边界

arXiv 的学科覆盖度并不均匀，历史上不同计算机科学子领域向 arXiv 迁移的速度也不同。因此以下说法仍然不允许：

- “该领域不存在其他相关工作”；
- “我们穷尽了 omni agentic system 的全部研究”；
- “没有 direct match”但不同时报告付费移除、不可得和类目边界；
- 用 arXiv 命中率推断整个同行评审文献宇宙的占据率。

有关 arXiv 在计算机科学不同子领域覆盖差异的实证分析可见 [arXiv:1710.05225](https://arxiv.org/abs/1710.05225)。最终表述应固定为：“在预注册的 arXiv-primary 检索宇宙、免费官方源救援和显式移除规则下，未发现/发现……”。

### 3.3 对付费移除方案的严格条件

申请书称以“ID+题名+venue+计数”保留存在性，原则上可以接受，但执行时必须满足：

1. flow report 不只保存总数，还要保存逐工作身份；
2. `REMOVED_PAYWALLED_UNOBTAINABLE` 与 `REMOVED_UNOBTAINABLE` 分开计数；
3. 不可得论文可以影响 coverage limitation 和 novelty 风险提示，但不能作为方法效果的承重证据；
4. 若不可得记录高度集中于某一 venue/年份/子领域，必须报告选择偏差，而不是只报告一个总数。

满足这些条件后，不再要求本轮重开 G1。

## 4. G2：venue tier 与 study quality 仍然混淆

这是本轮最重要的方法学阻断项。

### 4.1 T1 清单是项目自定清单，不是学界证据质量等级

当前 T1 仅包含 ACL、EMNLP、NeurIPS、ICML、ICLR、CVPR、ICCV、ACM MM、ICASSP、INTERSPEECH。它遗漏了与本课题直接相关的 AAAI、IJCAI、AAMAS、NAACL、EACL、COLING、TMLR、JMLR、RSS、CoRL、ICRA、IROS、CHI、UIST 等 venue。

这不意味着 Stage-1A 必须立即扩展到所有 venue；但它意味着“T1”只能表示“本项目预注册重点扫描清单”，不能表示默认更可信的证据类别。

### 4.2 当前 T2 定义产生逻辑错误

协议把“其他未发表 preprint、期刊、非 T1 会议”全部归入 T2，又规定 T2 实验数字默认带 `T2_UNREVIEWED`。

于是会出现：

- 已经同行评审的 TMLR / JMLR 论文，因为不在项目 T1 清单，被标为 `T2_UNREVIEWED`；
- 非 T1 但严格同行评审的 AAMAS / RSS / CoRL / CHI 论文，被等同于未审 preprint；
- T1 论文仅因 venue 身份默认承重，除非研究者主动降级。

这在语义上自相矛盾，也会系统性偏向团队熟悉的 venue。

### 4.3 正确拆分

`publication_status` 已经能够表达 preprint / peer-reviewed / withdrawn / retracted。它应负责“是否经过同行评审”。

`venue_tier` 应只负责：

- 是否属于本项目重点 proceedings 手扫范围；
- 发现优先级或路线来源；
- 最终 coverage 分层描述。

它不应直接赋予实验结论更高或更低的可信度。是否承重，应由逐篇 study-quality 维度和 claim locator 决定。

### 4.4 `HIGH/MEDIUM/LOW + 一句理由` 不足以重放

当前 REC-2 把数据边界、对照公平、统计不确定性、消融、复现性、代码可得、claim–evidence match 压进一个自由文本理由。两名编码者可以因为完全不同的缺陷都填 `MEDIUM`，但下游无法判断差异。

本轮不需要引入复杂评分模型，只需把既有七个质量维度拆为结构化字段：

- data boundary；
- control / comparison fairness；
- uncertainty reporting；
- ablation / attribution；
- reproducibility；
- code / artifact availability；
- claim–evidence match。

每一维至少记录 `PASS / PARTIAL / FAIL / UNCLEAR / NA`、一句理由、全文 locator 和编码者。总的 `HIGH/MEDIUM/LOW` 可以保留为摘要，但不得替代分维证据。

### 4.5 G2 的签署条件

1. 删除“venue tier = 默认实验可信度先验”的语义；或明确其只影响发现优先级，不影响证据承重。
2. 禁止把所有 T2 统一标成 `T2_UNREVIEWED`；使用 `publication_status`。
3. 把七个 study-quality 维度结构化。
4. novelty / priority threat 继续保持 tier-blind，这是团队现有设计中正确的一点。

## 5. G3：50 条 proceedings route 并未真正实例化

### 5.1 事实核查

申请书宣称“50 route ID 已冻结并机器验证”。实际 route 状态表只有 10 个数据行：

- 9 行使用 `SF-T1R-<VENUE>-2022..2026` 这样的范围表达；
- ICCV 行使用 `SF-T1R-ICCV-2023,2025`，同时在状态文本里说明 3 个偶数年占位；
- 表中没有 50 个逐条可枚举、可解析的 `route_id` 记录；
- 入口多为不带 scheme 的模式串，而不是 50 个逐条固定 URL；
- ICML 还存在 `ENTRY_TO_RESOLVE`；
- 仓内没有找到可复跑的 route validator 及其结构化输出。

所以，“10 个 venue 范围模板蕴含 50 个 venue-year 组合”可以成立；“50 条 route 已实例化”不成立。

### 5.2 为什么这不是措辞小问题

逐条实例化的目的，是让另一个执行者不需要猜测：

- `2022..2026` 是五个独立记录还是一个循环；
- ICCV 的 NOT_HELD 占位是否也有唯一 route ID；
- URL 中 `{year}` 如何替换；
- 2025/2026 ICML 的卷号何时、如何解析；
- READY 状态是在何时、由谁、根据哪个页面判断；
- route 发生重定向或页面结构变化时如何记录。

这些信息若只存在于自然语言和执行者脑中，就不能称为冻结 route。

### 5.3 词表归一化也有潜在实现歧义

route 文档明确对“题名”执行 lowercase、NFKC、`[-_/]` 替换和空格折叠，但没有同样明确要求先对词表项执行同一函数。词表同时包含 `multi-agent` / `multiagent`、`tool use` / `tool-use`、`reward-guided` / `reward guided` 等重复形态。

若实现只归一化标题、不归一化词表，匹配结果依赖实现细节；若两边都归一化，73 项会发生等价项合并，纸面“73 项”与有效词项数不同。两种实现都不能靠猜。

### 5.4 G3 的最低修复

生成机器可读的 50 行 JSONL 或 YAML，每行至少含：

- 唯一 `route_id`；
- venue、year、track set；
- exact entry URL，或明确 `NOT_HELD / NOT_YET_PUBLISHED / ENTRY_TO_RESOLVE`；
- access 状态；
- route 状态判断时间与依据；
- 词表版本/hash；
- 归一化规则版本/hash；
- 执行后 raw TOC hash 和解析日志回指。

同时持久化一个只读 validator，并让它检查：50 个唯一 ID、venue-year 唯一性、状态枚举、URL/待解析状态互斥、ICCV 年份约束、词表两侧同函数归一化以及有效词项计数。

在完成前，申请书应把“50 route 实例化”改为“10 个 venue 模板覆盖 50 个预期 venue-year route，逐条实例化待完成”。

## 6. G4：合同传播完成，但筛选与抽取记录仍不完整

### 6.1 原 G4 要求确实已完成

REC-2 已包含：

- `source_axes`；
- omni 五轴；
- `rl_identity` 九字段；
- 扩展后的 `tf_audit`；
- 扩展 `learned_object` / `core_access`；
- `evidence_axes` 和 quality override。

因此，不能不公正地说团队“没有修 G4”。前一轮要求的合同传播已经形式完成。

### 6.2 但 REC-2 只记录 INCLUDED，导致完整纳排链断裂

REC-1 是每页日志，保存本页 included/excluded ID 和理由；REC-2 只为 INCLUDED 工作建记录。缺少一个跨查询、跨 route、跨引文图的工作级主记录来回答：

- 同一 work 被多少条查询/route 命中；
- 哪些 hit 被合并为同一 canonical work；
- title/abstract 阶段为何排除；
- full-text 阶段为何排除；
- 是因不相关、重复、全文不可得，还是信息边界不合格；
- 谁做了初筛、谁做了复核，分歧如何裁决；
- 最终 REC-2 抽取来源于哪个命中和哪个固定版本。

PRISMA 2020 的解释文件要求报告各筛选阶段的 reviewer 数量、独立性与排除原因；本项目不必机械照搬医学综述格式，但这些 provenance 对任何可回放 systematic mapping 都是基本要求。[PRISMA 2020 explanation](https://pmc.ncbi.nlm.nih.gov/articles/PMC8005925/)

### 6.3 schema 内部存在三处机器语义问题

1. 协议使用 `system_level_proximity` 等名称，REC-2 使用 `system_level` 等缩写；如果已有编译/校验器按逐字字段名工作，会发生漂移。
2. `evidence_grade` 与 `evidence_axes.verification_depth` 重复，并靠“冲突时以后者为准”补救。最好只保留一个正典字段，兼容字段只在导出层生成。
3. `information_source_classes` 的示例是一个数组，但数组中只有一个包含六个 pipe 分隔选项的字符串。执行者可能把它填成一个字符串、多个枚举或任意组合，机器无法确定。

### 6.4 G4 的最低修复

不需要推翻 REC-1/REC-2。只需补充一个工作级筛选记录，或扩展现有模板，使每个 canonical work 无论最终 INCLUDED / EXCLUDED / DUPLICATE / UNOBTAINABLE 都有一行，并记录：

- canonical ID 与所有 source hit；
- dedup merge provenance；
- screening stage；
- decision 与标准化 reason code；
- reviewer、时间和 adjudicator；
- full-text/version ref；
- extraction reviewer/date；
- REC-2 回指。

同时统一三处 schema 命名和枚举语义。此修复属于 survey 执行基础设施，不是 Stage-1B 实验。

## 7. G5：bundle correction #3 可以通过

本轮对 correction #3 manifest 中的 17 件对象逐条核验：预期 git blob 与实际对象全部一致，当前 HEAD 也未改变这些文件。G5 可以认定闭合。

需要保留一个限定：当前 `Research-Objective.md` 的热层状态是 HEAD 上的继续更新，它不属于 37da7f3 固定的签名对象。可以说“当前热层与 bundle 叙述一致”，但不能说“签名 bundle 自身证明了未来热层永不漂移”。这不是阻断项，只是对象边界要说清楚。

静态验证报告顶部仍保留旧链条、末尾用 supplement 覆盖。虽然终态 hash 正确，但未来最好让摘要只指向唯一终态，避免读者误把历史表当现行表。

## 8. G6：递归分页方向正确，派生查询仍不可回放

### 8.1 已经修对的部分

从“按年拆分”改为“年→月→日递归拆分”，解决了单年超过 2000 后规则无法继续的问题。把派生 ID 关联到父查询 hash 也是正确方向。

### 8.2 仍缺的记录

REC-1 当前没有要求派生子查询逐条保存：

- `date_from` / `date_to`；
- 边界是闭区间、半开区间还是 API 特定语义；
- 时区；
- 完整 decoded query；
- 完整 URL-encoded query；
- 子查询自身 SHA-256；
- 父 hash；
- split level、顺序和触发时的 `totalResults`。

派生查询也不在冻结 `queries.jsonl` 中。只保存 `<parent>-W<n>` 和 `parent_query_sha256`，无法重建真正发给 API 的字符串。

### 8.3 arXiv API 的执行纪律

arXiv API 用户手册说明单次 slice 最大 2000、最多可访问 30000 个结果，并建议大查询细分；对重复调用还建议约 3 秒延迟。日期检索使用 GMT。[arXiv API User’s Manual](https://info.arxiv.org/help/api/user-manual.html)

因此协议还应补：

- GMT；
- 精确窗口边界；
- 每个派生查询的 hash 与字符串；
- 3 秒节流、失败重试、指数退避或等价策略；
- 中断后的 resume 规则；
- 单日仍超过 2000 时明确停止并登记接口限制，不得静默截断。

### 8.4 G6 的签署条件

在 REC-1 或独立 child-query 记录中加入上述字段，并用一个无需联网的合成例子证明：给定父查询和 `totalResults`，可确定性生成相同子查询列表和相同 hash。

## 9. 引用与论文谱系审计

### 9.1 本轮新增 14 条的总体判断

本轮补入的 AFlow、ADAS、GPTSwarm、RAP、Tree of Thoughts、PromptAgent、Magentic-One、Agent-S、Chameleon、Socratic Models 等，覆盖了自动化 agent design、搜索/规划、系统级 agent scaffold 和多模态组合的重要谱系。将训练过的自动设计器放在 trained/system comparator，而不是误标 TF-Strict，是正确做法。

Snell 与 HedgeTune 的勘误方向也合理：前者不能被简化成普适的 training-free agent 证据，后者更适合作 output-level overoptimization 类比。VideoAgent 的 arXiv ID `2606.23327` 当前可解析；其完整训练/持久化边界仍应在全文阶段审计，不能仅凭摘要定性。

因此，现有引用不是“乱引”或“完全失效”。问题是仍遗漏了若干直接威胁 system-first / training-free / black-box / test-time control 身份的工作。

### 9.2 建议在首轮 survey 中设为高优先级的遗漏工作

以下不是要求立即把所有论文升级为承重证据。Stage-1A 应先作为 seed 或强制查询命中检查，随后按全文、版本与 REC-2 合同审计。

| 工作 | 为什么是直接遗漏 | Stage-1A 处理 |
|---|---|---|
| [Tree Search for Language Model Agents, arXiv:2407.01476](https://arxiv.org/abs/2407.01476) | 在真实 agent 环境中做 inference-time best-first search，使用多模态 value function，直接关系 RQ-CTRL / RQ-SYS / RQ-OMNI；不能只用 ToT 代替。 | **强制 seed / 全文审计** |
| [Thinking vs. Doing: Agents that Reason by Scaling Test-Time Interaction, arXiv:2506.07976](https://arxiv.org/abs/2506.07976) | 区分基于 prompting 的 training-free interaction scaling 与训练式 test-time interaction RL，是“推理时多交互是否足够”的直接边界工作。 | **强制 seed / 拆分训练与非训练部分** |
| [Collaborative Multi-Agent Test-Time Reinforcement Learning, arXiv:2601.09667](https://arxiv.org/abs/2601.09667) | 明确使用 test-time RL 命名，声称无需 tuning，并以文本经验和多 agent deliberation 更新控制；直接威胁项目身份与术语边界。 | **强制 seed / TF-Strict 与持久化审计** |
| [A Survey on Optimization of LLM-based Agents, arXiv:2503.12434](https://arxiv.org/abs/2503.12434) | 含 parameter-free、experience、feedback、tool/retrieval、多 agent 等分类，可作为引用图导航。 | **仅 DISCOVERY_NAVIGATION，不作一手承重** |
| [AgentOccam, arXiv:2410.13825](https://arxiv.org/abs/2410.13825) | 通过对齐 observation/action space 改善冻结 agent，而非搜索更多候选；是“外部控制平面激活预训练能力”的强替代解释。 | **强制 seed / 机制对照** |
| [Language Models as Black-Box Optimizers for VLMs, arXiv:2309.05950](https://arxiv.org/abs/2309.05950) | 黑盒 VLM、不可访问权重/embedding/logit，以文本反馈和 hill-climbing 做优化；是 multimodal black-box component 的直接先例。 | **强制 seed / RQ-OMNI、RQ-CTRL** |
| [AgentOptimizer, arXiv:2402.11359](https://arxiv.org/abs/2402.11359) | 核心模型可冻结，但 agent functions 被视为可学习对象；正好界定 TF-Strict 与结构/函数更新的边界。 | **trained comparator / 身份审计** |
| [AutoGuide, arXiv:2403.08978](https://arxiv.org/abs/2403.08978) | 从历史交互生成可复用指南，涉及跨 item persistence 与外部知识的形成。 | **持久化边界 seed** |
| [MetaReflection, arXiv:2405.13009](https://arxiv.org/abs/2405.13009) | 将反馈抽象为可迁移反思知识，直接触及 memory/readout/new-info 与跨任务持久化。 | **持久化边界 seed** |
| [AgentEval, arXiv:2607.06873](https://arxiv.org/abs/2607.06873) | 面向黑盒、有状态 workflow 的边界测试，直接关系 RQ-SAFE；其 primary category 为 cs.SE，也暴露当前查询类目盲区。 | **强制 seed / 类目敏感性哨兵** |
| [The Devil's Advocate, arXiv:2405.16334](https://arxiv.org/abs/2405.16334) | 零样本 anticipatory reflection、post-action reflection 与 backtracking，是外部控制策略的重要基线。 | **控制基线 seed** |
| [Black-Box Prompt Optimization, arXiv:2311.04155](https://arxiv.org/abs/2311.04155) | 无需更新目标模型参数的黑盒 prompt 优化，涉及外部优化器与目标模型的边界。 | **组件级 comparator** |
| [A Survey on Agent Workflow, arXiv:2508.01186](https://arxiv.org/abs/2508.01186) | 可补 workflow/orchestration 的组织谱系，并提示 HCI/软件工程类目。 | **仅导航，不作一手承重** |

### 9.3 为什么这些遗漏会影响 Gate，而不是“survey 跑完自然会发现”

Gate S1 不需要提前列尽所有论文，正常遗漏本应由系统查询发现。但以上列表中至少有两篇暴露了**查询设计本身**的问题：

- AgentEval 的主要 arXiv 类目为 `cs.SE`；
- agent workflow / interaction 研究可能进入 `cs.HC` 或软件工程 venue；
- 当前 SF-L1 只覆盖 `cs.CL/cs.AI/cs.LG/cs.CV/cs.RO`，SF-L3 额外加 `cs.SD/eess.AS`，SF-L6–8 反而只保留前三类；
- T1 proceedings 手扫也没有 SE/HCI/agent systems 对应 venue。

这不是要求无边界扩类，而是要求做可证伪的敏感性检查：把上述直接邻近工作作为 sentinel，用其已知标题/摘要离线测试现有 query family 是否能命中；若不能，要么加入 `cs.SE` / `cs.HC` 的受控 lanes，要么给出可审计理由并设置补充发现道。

## 10. 查询和种子本身的进一步核查

### 10.1 正向结果

- 51 条查询均有唯一 ID；
- decoded 与 URL-encoded 字符串、categories、date window、compiler version 和 record hash 均已记录；
- 原 48 条前缀没有被无声改写；
- 14 条新增 seed 的身份可枚举；
- 当前没有发现 query 已执行而日志缺失的证据。

### 10.2 仍缺的 Gate 证据

申请书提到离线敏感性审计和机器验证，但没有在签名 bundle 中提供一份机器可读的 sentinel-recall 结果。语法可编译不等于能召回关键邻域。

应固定一小组覆盖不同威胁族的已知论文，至少包括：

- test-time agent search；
- multi-agent test-time RL；
- black-box VLM optimization；
- agent workflow safety / stateful testing；
- cross-item memory / reflection；
- omni/multimodal tool agent。

记录每篇由哪条 query family、哪个类目或哪个 proceedings route 召回。未命中不是失败，未命中却没有解释才是 Gate 缺陷。

这项检查只验证搜索设计，不允许使用 survey 结果回填、改写已冻结的科学结论。

## 11. Stage-1A / Stage-1B 范围审计

### 11.1 当前允许的工作

以下都属于 Stage-1A 收官准备或 Stage-1B 的纸面启动准备，可以继续：

- correction #4；
- 50 条 route 的逐条序列化与 validator；
- REC 模板、去重和筛选 ledger；
- query executor、日志、失败恢复和 hash 工具；
- reviewer 签署后执行 systematic mapping；
- 形成 3–5 个候选问题；
- 仅在纸面上定义 Stage-1B probe card、配置接口、停止条件、信息边界和预期证伪模式；
- 检查工程基座是否能以配置选择数据集、模型、推理策略、reward/evaluator 和记录器。

### 11.2 当前不允许的工作

在 Stage-1A close 与独立 Stage-1B release 前，下列行为会越界：

- 实际加载模型并运行数据集样本；
- 产生任何 headroom、MBR、selector、reward-guided search 或 controller 的方向性数字；
- 根据早期模型结果改变 query、seed、纳排或 study-quality 规则；
- 把工具链 smoke test 包装成“实验”；
- 以未放行的结果选择最终模型、数据集或研究问题；
- 声称“Stage-1B 已经开始并得到初步效果”。

如果团队确实已经运行过上述工作，应立即单独登记运行时间、配置、输入、输出和知情人员，并标为 `PRE_RELEASE / NON_EVIDENTIARY`，不得删除、不得纳入 Stage-1A survey 结论。当前仓内没有发现这类运行的直接证据，所以本报告不作无依据指控。

### 11.3 本复审没有要求的超前工作

本报告明确不要求：

- 预算 cap；
- 现在冻结最终模型/数据集；
- Stage-2 的 SESOI、功效分析或正式显著性检验；
- 等成本全基线；
- 大规模实验、完整消融或 SOTA 复现；
- 提前收敛到单一技术方案。

当前目标是让 survey 能够开始且可回放，而不是提前结束探索。

## 12. 研究诚信与“是否涉嫌学术欺诈”

### 12.1 本次没有发现的事项

在可见材料范围内，没有发现以下直接证据：

- 伪造或篡改实验结果；
- 虚构已执行查询或伪造返回记录；
- 删除不利的 survey 结果；
- 把 test gold 输入 selector/reward/prompt；
- 伪造论文、作者、版本或引用 locator；
- 在签名为空时谎称已获 reviewer 正式签署。

零查询状态、空签名和 17/17 bundle 一致性反而是有利的诚信证据。因此，目前不能把团队定性为 fabrication、falsification 或 plagiarism。

### 12.2 已经存在的高风险研究行为

但以下问题不能轻描淡写：

1. 把 10 行范围表达写成“50 route 已实例化”；
2. 把没有持久化 validator/output 的检查写成“机器验证”；
3. 把 G2、G3、G6 的部分修复写成“全闭合”；
4. 用 venue 清单对实验可信度赋默认权重，同时声称 study quality 已独立；
5. 在 REC-2 只有 INCLUDED 的情况下，给读者造成完整纳排 provenance 已具备的印象。

这些属于**材料性陈述与证据不匹配、不可复核自证和潜在选择性报告风险**。它们当前更接近 questionable research practice / 研究治理缺陷，而不是已经证实的学术欺诈。

如果团队在收到本报告后仍保留“50 条已实例化”“G1–G6 全闭合”等完成态表述，并据此获得 Gate 签署或对外发表，那么问题会从可修复的记录缺陷升级为误导性陈述。严重性取决于团队是否及时更正，而不是取决于措辞是否听起来像“技术细节”。

### 12.3 本轮诚信等级判断

- FFP（伪造/篡改/剽窃）直接证据：**未发现**。
- 未经授权先跑 Stage-1B 实验的证据：**未发现**。
- claim–evidence mismatch：**确认存在，且足以阻断签署**。
- 重放与 provenance 风险：**高**。
- 可通过一次窄幅 correction 修复：**是**。

## 13. Correction #4：最小且充分的整改计划

本轮不得借机重开 proposal，不得把整改扩成无限期知识工程。建议只做以下六项。

### C4-1：纠正 Gate 申请的完成性表述

将以下意思写入一个 superseding response，而不是改写历史审查件：

- G1 = closed with limitation；
- G2 = open；
- G3 = open；
- G4 = contract propagation closed, execution ledger open；
- G5 = closed；
- G6 = partially closed；
- “50 route 实例化”改为“50 route 组合已规划，逐条序列化待完成”；
- “机器验证”只指向仓内可运行脚本和固定输出。

验收：新回复中的每个完成态动词都有具体 artifact、hash 和复跑命令。

### C4-2：修复 G2

- `venue_tier` 降为扫描/发现元数据，不直接决定实验承重；
- `publication_status` 独立表示同行评审状态；
- 去除统一的 `T2_UNREVIEWED` 语义；
- 七个 study-quality 维度结构化，附 locator 和 reviewer；
- 总 rating 只能由分维记录导出或人工裁决，不能替代分维记录。

验收：给出三个合成案例——高质量非 T1 同行评审论文、低质量 T1 论文、未审但有 priority threat 的 preprint——三者能得到不矛盾的编码。

### C4-3：修复 G3

- 落盘 50 行机器可读 route；
- 逐条唯一 ID；
- exact URL 或明确非 READY 状态；
- 双侧同函数归一化；
- 持久化 validator 和输出；
- validator 检查 50 唯一组合、状态、URL、ICCV、词表有效项与 hash。

验收：新的研究者仅用 bundle 即可列出 50 条 route，不需解析 `..` 或询问作者。

### C4-4：补工作级筛选/去重记录

- 所有命中工作都留 canonical 行，不限 INCLUDED；
- 记录 source hits、去重、阶段、reason code、reviewer、adjudication、version 和 REC-2 回指；
- 统一 `proximity` 字段命名；
- 消除/导出重复的 evidence 字段；
- `information_source_classes` 使用真实枚举数组。

验收：用三个合成命中展示“同一论文被 query+venue 命中后合并”“摘要排除”“全文不可得”的完整 lineage。

### C4-5：修复 G6

- 派生查询保存精确 date window、GMT、decoded/encoded query、child hash、parent hash、split level、trigger count；
- 明确边界语义、节流、重试、resume 和单日超限；
- 落盘一个离线合成 replay test。

验收：相同父查询和输入计数生成逐字相同的子查询与 hash。

### C4-6：查询类目与 sentinel recall

- 把本报告列出的直接遗漏工作加入 seed 候选或 sentinel 清单；
- 对 `cs.SE`、`cs.HC` 做受控敏感性检查；
- 若不扩类，必须证明补充 route / citation graph 能稳定召回这些工作；
- 结果机器可读地落盘，并说明每个 sentinel 的召回路径。

验收：每个 sentinel 都是 HIT 或 EXPLAINED MISS；不得以“之后 survey 可能发现”替代解释。

## 14. 下一次 Gate S1 签署清单

reviewer 只需检查以下项目，不应再要求 proposal v4：

- [ ] correction #4 对完成性表述作日期化更正；
- [ ] G2 venue / publication status / study quality 三者真正分离；
- [ ] 50 条 route 逐行机器可读；
- [ ] route validator 与固定输出在 bundle 内；
- [ ] 工作级 screening/dedup/adjudication 记录可用；
- [ ] child query 可精确重放；
- [ ] `cs.SE` / `cs.HC` 类目盲区有检查或可审计补救；
- [ ] 至少一组 sentinel recall 结果已落盘；
- [ ] correction #4 manifest 的 blob/hash 一致；
- [ ] reviewer、owner、P0-R8 仍保持分立；
- [ ] 首条真实查询前仍为零查询。

若以上全通过，应签署 Gate S1 并允许立即开始 Stage-1A survey，不应再以“还可以更完善”为由无限延期。

## 15. 给研究团队的最终博士生导师意见

这轮整改有实质进步，尤其是 bundle 固定、来源降名、合同传播与零查询纪律。研究方向本身也仍有足够探索空间：围绕冻结黑盒核心构建 omni agentic system，以 training-free RL 作为外部控制平面的牵引原则，在 Stage-1A 尚未被现有材料否定。

但“方向值得做”不能为搜索设计的完成性夸张背书。现阶段最需要纠正的不是技术路线，而是研究者对“我已经完成了什么”的证据纪律。

严格结论如下：

1. **研究问题与 system-first 身份可以继续。**
2. **团队回复不是敷衍，也没有发现 FFP 直接证据。**
3. **Gate S1 目前不能签。**
4. **无需重写 proposal；做一次 correction #4 即可。**
5. **Stage-1B 只能准备，尚不能执行。**
6. **整改通过后应立刻运行 Stage-1A survey，避免继续用元审查代替研究。**

最终裁决：**WITHHOLD SIGNATURE — TARGETED CORRECTION #4 REQUIRED。**
