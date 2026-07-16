---
title: "Gate S1 P0-R8：Stage-1A mapping 执行前窄幅博士生导师式对抗复审"
date: 2026-07-16
review_role: "严格外部审稿人 / 博士生导师 / research-integrity adversarial auditor"
review_stage: "Stage-1A survey-ready gate；首条系统 mapping 查询之前；Stage-1B 未放行"
review_target: "wiki/survey/2026-07-16-gate-s1-p0r8-rereview-application.md"
target_commit: "b6207d3a1eefa65ec3a09580913aee6698c841f0"
target_git_blob: "fe005fa38015d00bb5a67c9dc9d8df96f0cf0529"
target_worktree_sha256: "44C22C832657C568B920A9B6544337FC1BE99C3B4A1D425C3335BF5D1882F3C2"
verdict: "WITHHOLD SIGNATURE — 3 MAJOR + 2 MINOR；P0-R8 零新发现合同未满足"
integrity_verdict: "FFP NOT ESTABLISHED；MATERIAL CONTROL/REPORTING MISMATCH ESTABLISHED"
---

# Gate S1 P0-R8：Stage-1A mapping 执行前窄幅博士生导师式对抗复审

## 0. 一页裁决

**总裁决：不签署 Gate S1；首条系统 discovery query 继续保持为 0。**

Correction #4A 不是虚假交付。相反，本轮存在一组必须明确承认的真实进展：固定提交上的七条复跑命令
全部成功，七个确定性产物与 `af96a89` 中的 git blob 完全一致；manifest 表内逐项路径—短 blob 对未
发现错配，但其宣称的“31 件”计数本身是错的（实际 33 个非 fixture 文件 + 15 fixtures = 48 changed
files）；历史审计件确实没有被回写；ACL 2026、ICML 2025 等前轮 route 错误也已用 dated supersession
纠正。团队没有伪造这些文件，也没有靠手改输出冒充一次并不存在的脚本运行。

但是，P0-R8 的合同不是“脚本都能再次输出 PASS”，而是“一轮窄幅复审 0 新 MAJOR、0 新 MINOR，且
原 P0 的语义合同可被工件强制”。本轮对抗性反例证明：当前若干机器绿灯**可以在核心数据已经错误时
继续给 PASS**。因此申请中下列强断言不成立：

1. `sf_package_summary.py` 不能保证 92/55/50 正典计数，也不能证明 route 外部状态审计有效；
2. `sf_record_validator.py` 没有完整强制双向 lineage、D2 内层 schema 和 seed threat 触发；
3. `VQQA` 只验证了 `cs.MA` 一侧，不能独立验证 `cs.MM`；另有直接相关论文被现行 55 query 漏掉；
4. 7 份所谓“verbatim abstract”中有 3 份经过 URL/转义规范化，不是字节或字符意义的逐字原文；
5. `REGISTERED_BOUNDARY` 当前只检查某个路径存在，未检查该文件真的登记了该 boundary。

**诚信裁决：当前没有证据达到 fabrication、falsification 或 plagiarism（FFP）的认定阈值，也没有
发现本批次偷偷运行模型实验的仓内证据。** 但“全字段机器强制”“人无法手写绿灯”“类目补救独立
验证”“verbatim”均是超过实际工件能力的完成态陈述，属于 material claim–evidence mismatch。
前轮报告已经明确警告再次过度声称会升级完整性风险；因此这一次不能再仅当作文案瑕疵放行。

## 1. 阶段校准：不是 Stage-1A 尚未开始

仓内正典写得很清楚：当前已经处于 **Stage-1A 的 survey-ready gate**。问题界定、检索协议、种子与
查询冻结、route 设计、screening/coding schema 和离线回放，本身就是 Stage-1A 工作。尚未开始的是
Stage-1A 的系统 mapping 执行；尚未放行的是 Stage-1B 的模型/数据集方向性原型。

因此本轮只回答五件事：

- 这套 survey 合同是否已达到可执行、可失败、可追责；
- 引用和外部事实是否真实、是否被过度解释；
- 已知检索盲区是否仍会漏掉直接近邻；
- 当前工作是否越过 Stage-1A；
- 是否存在足以启动正式学术不端调查的证据。

本轮**不要求**模型效果、benchmark、显著性、SESOI、selector/evaluator 数字、预算 cap、Stage-2 因果
实验或论文级结论。下述修复均可离线完成，不构成 Stage-1B。

## 2. 审查对象、方法和五轮对抗

### 2.1 冻结对象与环境

- 目标申请：`wiki/survey/2026-07-16-gate-s1-p0r8-rereview-application.md`；
- 目标 HEAD：`b6207d3a1eefa65ec3a09580913aee6698c841f0`；
- Correction #4A 工件提交：`af96a89`；manifest 提交：`b7fd74b`；
- `af96a89` 与 `b6207d3` 当前均是 `origin/master` 的祖先，申请提交已由 merge `1ca8089` 合入；
- 重放环境：`wsl -d Ubuntu-24.04`，Python 3.12.3；冻结提交被解包到系统临时目录，未写团队工作树。

### 2.2 五轮对抗复核

| 轮次 | 对抗问题 | 结果 |
|---|---|---|
| A：chain-of-custody | commit、blob、历史不回写、确定性输出能否独立复现 | **部分通过**：逐项短 hash 未见错配，七个产物 byte-identical，旧件 diff 为空；但 manifest 31 件声明与实际 33 件不符 |
| B：semantic replay | PASS 是否证明申请声称的真实合同 | **不通过**：PASS 证明当前 fixtures 自洽，不证明合同完备 |
| C：mutation testing | 主动注入错误后，门禁是否会失败 | **不通过**：2 seeds、空 route evidence、交叉 lineage、非法枚举均可 PASS |
| D：external survey | 官方 route、arXiv 元数据、遗漏论文与 held-out 是否支持叙述 | **部分通过**：引用真实；发现 cs.MM 验收过度解释及 Seg-Agent 漏检 |
| E：反向辩护 | 将发现分别按“测试范围有限/正常文本规范化/当前未使用通道”作最强辩护 | **未推翻**：两项降为 MINOR，其余三项仍会改变 gate 结论 |

这不是把同一主观看法重复五遍：A 轮尝试确认团队结论，C 轮刻意寻找能骗过门禁的反例，D 轮不依赖
仓内叙述，E 轮又主动为团队寻找最强无罪解释。最终严重度按反向辩护后结果给出。

## 3. 已通过且不应反复要求重做的内容

### 3.1 固定提交与复放真实性：通过

在 `af96a89` 的隔离副本中，以下命令均为退出码 0：package summary、query compiler、child replay、
real-row dry-run、record validator tests、route structural validator、sentinel recall。重跑后的下列 blob 与
冻结提交完全一致：

- package summary `55a66d9df0e8…`；
- child replay `ce71ae27af41…`；
- real-row dry-run `91378a4f9691…`；
- record tests `2b1b7c53651e…`；
- route validation `3efef48872c1…`；
- sentinel report `63b3d300a3b3…`；
- compiled queries `4cfd3b9063f0…`。

因此不能把问题描述成“团队伪造了测试输出”。正确描述是：**测试真实运行并可复现，但测试 oracle 与
覆盖面不足，导致真实的绿灯承载了过强结论。** 另需单独更正 bundle 数字：`git diff --name-only
5cde3e3 af96a89` 为 48 files，其中 fixtures 15、非 fixtures 33；manifest 表第二列也枚举出 33 个真实
文件路径，不是申请所称 31 个。逐项 blob 正确不能抵消集合基数错误。

### 3.2 Child splitter 主路径：本轮通过，保留非阻断加固项

前轮的真实 frozen-row `KeyError` 和缺 YEAR 层已经修复。55/55 真实行能进入规范函数，跨年 overflow
首事件是 `SPLIT_YEAR`，10/10 与 17/17 均可确定性回放。这部分不应再次以旧问题阻断。

后续可加固但不阻断本次 gate 的点包括：强制每个 frozen query 只有一个日期窗、拒绝负数/非整数
oracle 结果、由真实 executor 强制调用 `assert_unique_ids`，以及明确 terminal STOP 记录绝不能继续发网。

### 3.3 Route 当前事实状态：未发现新的时点误判

独立抽查支持当前关键状态：ACL Anthology 已列出 ACL 2026 六卷；CVF 已公开 CVPR 2026 papers；ICML
2026 已于 7 月 6–11 日举行，但 PMLR 索引截至复审时仍只列 ICML 2025 volume 267，故把 ICML 2026
proceedings 标为 `NOT_YET_PUBLISHED` 仍可成立；ACM MM 2026 官方会期为 11 月 10–14 日，当前
`NOT_YET_PUBLISHED` 合理。参见 [ACL Anthology](https://aclanthology.org/venues/acl/)、
[CVPR 2026 Open Access](https://openaccess.thecvf.com/CVPR2026)、
[ICML 2026 官方页](https://icml.cc/Conferences/2026)、
[PMLR 索引](https://proceedings.mlr.press/) 和
[ACM MM 2026 官方页](https://2026.acmmm.org/)。

这只说明**当前人工裁定大体正确**，不等于 package summary 已经机器证明了这些事实；后者是下述
MAJOR-1 的核心区别。

## 4. 新发现：3 个 MAJOR

### MAJOR-1：package summary 存在可复现的 false-green，不能承担“机械化完成态”

申请把 `sf_package_summary.py` 描述成 92/55/50 全量一致、外部 route 审计 PASS、陈旧口径零命中的
统一机器门。实际代码与对抗结果不支持这一强度。

#### 4.1.1 精确正典计数没有被强制

`counts_ok` 只要求 seeds/query 各自唯一，并只对 routes 强制 50；它没有强制 seeds=92、queries=55、
sentinels=21、held-out=2 或约定类目集合。隔离副本中把 seed 输入替换为**仅 2 个不同 ID**，脚本仍输出：

> `package summary: PASS`，`seed_rows=2`。

这直接反证申请中的“PASS 即 92/55/50 正典一致”。脚本会把重数写进 JSON，但“能显示错误数字”和
“会因错误数字失败”不是同一件事。

同一缺口已经在真实 bundle 数字中出现：申请和 manifest 都写“31 件 + fixtures 树（15 件）”，而
`af96a89` 相对 `5cde3e3` 实际是 33 个非 fixture 文件 + 15 fixtures = 48 files。manifest 表内逐项 hash
均能匹配，却没有机器重数发现标题数字少了 2 件。这不是 mutation 假设，而是当前签署包中的现实
claim–artifact mismatch。

#### 4.1.2 route 外部状态项只查 `n_routes == 50`

隔离副本把 route audit evidence 替换成：

```json
{"n_routes":50,"rows":[],"note":"no probes and no adjudication"}
```

package summary 仍将“routes 外部状态审计证据件”标为 PASS。它没有验证 50 个唯一 route ID、URL、
UTC、HTTP/失败码、body hash、amendment 裁定、status 对应关系或证据新鲜度。更根本地，原 collector
明确声明自己**不裁定 status**，package summary 却把“存在 50 行 collector 输出”升级成 PASS。

#### 4.1.3 stale-token scan 可被同一行 marker 绕过，且 active surface 不完整

扫描器遇到一行含任一历史 marker 就跳过整行。隔离副本加入：

> `ACTIVE CANON: REC-1..REC-7; ... HISTORICAL_SUPERSEDED`

扫描仍为 PASS。marker 应只豁免结构化历史块或某个被明确标注的 token occurrence，不能豁免整行。
同时 `ACTIVE_FILES` 没有覆盖本次申请、correction response、bundle manifest、Research-Objective 与
routes v2 等实际签署面。

#### 4.1.4 缓存证据被信任，而不是从 producer/input 重新验证

child、record、route、sentinel 项主要读取持久 JSON 中的 `verdict`/计数；summary 不核对 producer blob、
input hash、output hash，也不重新执行确定性 producer。因此“人无法手写 ✅”是错误陈述：人仍可改写
evidence JSON 后提交，summary 不具备区分能力。此次独立 replay 证明**当前 JSON 恰好是真实的**，但
门禁结构不能阻止下一次被手填或陈旧缓存欺骗。

**裁决：MAJOR。** 这是统一签署门本身的 soundness 问题，不是显示格式问题。

### MAJOR-2：REC validator 的“V1–V13 / D2 全合同”强于实际约束

#### 4.2.1 REC-0 ↔ REC-2 不是双向一致关系

V4 只检查 REC-0 指向的 REC-2 存在且 depth 一致；V7 只检查 REC-2 的 `rec0_backref` 指向某个 INCLUDED
REC-0。两者没有检查彼此属于同一 work，也没有检查一一对应。

在隔离 positive fixture 中，仅交换两个 REC-2 的 `rec0_backref`：

- REC-0 AMC 仍指 `REC2-AMC`；但 `REC2-AMC` 回指 EvoLib canonical ID；
- REC-0 EvoLib 仍指 `REC2-EVOLIB`；但 `REC2-EVOLIB` 回指 AMC canonical ID。

这是明确的交叉串线，validator 仍返回 `n_violations: 0, verdict: PASS`。因此承重 claim 虽然指到一个
D2 行，却可能归属另一篇 work；这会破坏所有后续 claim lineage。

#### 4.2.2 D2 只验证“有 dict”，不验证完整内层字段

`is_block_object(v)` 的实质是“`v` 为 dict 且 status != NA”。空 `{}` 就是合法 block。matrix、tf_audit、
source_axes、extraction 的必填键、非空值与枚举均未检查。隔离 fixture 中把：

- `matrix.core_access`、`reward_type` 置空；
- `matrix.parameter_update` 改成 `NOT_AN_ENUM_VALUE`；
- `tf_audit.base_model_updated` 置空，`test_time_parameter_update` 改成非法枚举；
- `source_axes.answer_bearing_external_info` 置空、attribution 改非法枚举；
- extraction strongest result 置空；proximity 关键值置空；

validator 仍为 PASS。申请所说的“D2 全字段 + 信息边界 + TF audit 机器强制”因此不成立。

#### 4.2.3 seed threat tag 没有进入 validator 输入

D2/dual-coding 触发只读 REC-2 内部 `initial_tag`，不与 seed manifest 的 `initial_tag` 交叉核对。隔离 fixture
删除 `DIRECT_THREAT` 与整个 `threat_dual_coding` 后仍 PASS。当前 AMC 还因 core/claim 保持 D2，但对一篇
不被 claim 引用、topic 被误写为 element 的 threat，标签可在转录时无痕丢失并绕过双编码。

此外还有：孤儿 REC-2/多对一映射未拒绝；`OTHER:`/`DUPLICATE_OF:` 可空后缀；duplicate target 不要求
存在；`int(disagreements)` 遇非法类型会崩溃而不是输出结构化 violation。16/16 只能说明 14 个已写负例
会失败，不能说明 V1–V13 的每个子句已覆盖。

**裁决：MAJOR。** 这是研究 claim 与论文身份绑定的承重链路，不能留给人工默契。

### MAJOR-3：SF-L11 的独立验收只覆盖一半，且存在已复现的相关论文漏检

申请称：VQQA 的五个 query hits（含 SF-L11 两条）构成“类目补救独立验证”。VQQA 的 arXiv categories
是 `cs.CV/cs.AI/cs.LG/cs.MA`，**没有 `cs.MM`**；它只能独立验证 SF-L11 的 `cs.MA` 一侧。MAR3 是
primary `cs.MM`，但它已被用作确定反例并进入 seed/query 设计，不是独立 held-out。

独立 external survey 找到了更合适的 `cs.MM` holdout：

- **TimeLogic Challenge @ CVPR 2026**（[arXiv:2606.01631](https://arxiv.org/abs/2606.01631)），
  primary/only `cs.MM`，training-free evidence-seeking MLLM agent。将官方题名、摘要、类目放入隔离
  sentinel runner 后，现行查询得到 `QUERY_HIT=1`，说明 SF-L11 的 cs.MM 设计其实有能力通过更严格的
  独立验收。团队应使用这类证据，而不是让 VQQA 承担它没有覆盖的类目。

同时发现一个现行 query 的实际漏检：

- **Seg-Agent: Test-Time Multimodal Reasoning for Training-Free Language-Guided Segmentation**
  （[arXiv:2605.12953](https://arxiv.org/abs/2605.12953)），categories=`cs.CV/cs.AI`。它使用冻结 MLLM、
  generation–selection–refinement 视觉反馈环且无参数更新，是 system-first omni control plane 的直接
  component 邻居。相同离线 matcher 得到 `UNRESOLVED_MISS=1`，并报告 2 个“term matched but category
  blocked”：SF-L11 词项能匹配，却因只开放 cs.MM/cs.MA 而被挡住。

这不是要求检索“永不漏一篇”，也不是在 Stage-1A 前强行穷尽论文；它是一个**已经知道、可重复、与
研究对象直接相关的结构性反例**。在 survey-ready gate 已知它之后仍签署，才是 premature closure。

**裁决：MAJOR。** P0-R5 的目的正是让 coverage test 可证伪；现在它被新的外部 sentinel 证伪了。

## 5. 新发现：2 个 MINOR

### MINOR-1：“verbatim abstract”用词不准确

通过 arXiv Atom API 将 7 份当前摘要做 whitespace-normalized 比较：MAR3、VQQA、EvoLib、Useful
Memories 四份一致；AMC、TF-TTCL、MappingSmarter 三份不完全一致。差异集中于：

- GitHub URL 被抓取工具改成 `this https URL`；
- LaTeX `\%` 被规范化为 `%`。

这更像 fetch/sanitization 层的正常变换，不像研究人员编造摘要，而且不影响本轮 query match 结论。
但“verbatim”在证据链上有明确含义，不能用于经过规范化的文本。应改为 `source-normalized abstract`，
登记 normalization 规则；若要称 verbatim，应保留 raw Atom response/version/hash。

### MINOR-2：`REGISTERED_BOUNDARY` 只验证文件存在

sentinel runner 对 `accepted_boundary.registered_in` 只做 `os.path.exists`；任意存在的文件都能把 miss
变成 REGISTERED_BOUNDARY，即使文件不含该论文、boundary、日期或接受理由。当前 21 sentinels 中该通道
计数为 0，所以没有改变本轮 PASS；但合同声称该通道必须回指 dated amendment，代码没有强制。

## 6. 引用与外部事实审计

### 6.1 引用真实性：总体通过

Correction #4A access log 的 7 个 arXiv ID、题名、类目和核心摘要均能在官方页面找到。AMC 的 trained
value function、TF-TTCL 的 frozen LLM + textual rules、EvoLib 的跨实例 library、MappingSmarter 的
test-time web evidence、MAR3 的 audio-visual 多 agent、Useful Memories 的连续更新退化、VQQA 的
black-box multimodal critique，均没有发现 citation hallucination。

因此本轮不成立“引用伪造”。问题是两个较窄的 citation-use mismatch：VQQA 被解释成完整验证 cs.MM/
cs.MA，及 normalized text 被称为 verbatim。

### 6.2 Survey 方法引用应如何使用

当前 query、route、REC-0/REC-2、flow、version pin 和 access log 的方向，符合可回放 mapping 的需要。
[PRISMA-S](https://pmc.ncbi.nlm.nih.gov/articles/PMC7839230/)适合约束完整报告每个信息源、完整查询、
日期、去重与更新过程，但它自己明确是 reporting guideline，不是搜索质量或 review conduct 的替代品。
查询策略本身更适合增加一次类似
[PRESS 2015](https://pubmed.ncbi.nlm.nih.gov/27005575/)的独立 peer review：检查 Boolean/field tags、
拼写与词形、类目/数据库限制、日期限制、已知 sentinel recall 和每个限制项的副作用。项目采用 systematic
mapping 而非立即做效果综合，也与
[Petersen 等 systematic mapping 指南](https://doi.org/10.1016/j.infsof.2015.03.007)的目标区分一致。

不要把这些规范转化成 Stage-2 的论文质量结论；在当前阶段，它们只用于保证 search/screen/code 的透明、
一致和可追溯。

## 7. 本轮遗漏/新增论文：如何处理而不把 gate 变成无限 survey

下面不是“签署前必须精读完所有论文”的 cap，也不是最终 related-work 列表，而是独立 survey 暴露出的
已知近邻及其 Stage-1A 作用。

| 工作 | 与项目关系 | 当前 55-query 离线结果 | Stage-1A 动作 |
|---|---|---|---|
| [WorldEvolver, 2606.30639](https://arxiv.org/abs/2606.30639) | 冻结 agent/参数，deployment-time context、episodic/semantic memory、selective foresight 自演化 | QUERY_HIT×2 | 加入 execution-early / persistence 与 world-model 边界编码 |
| [MemoPilot, 2606.08656](https://arxiv.org/abs/2606.08656) | 冻结 player，但用 multi-turn GRPO 训练外部 memory updater；是“核心冻结≠系统 training-free”的强反例 | QUERY_HIT×1 | 加入 direct boundary/threat queue，分开编码 core 与 external training |
| [PolarMem, 2602.00415](https://arxiv.org/abs/2602.00415) | frozen VLM 上的 training-free polarized graph memory；负记忆/逻辑约束 | QUERY_HIT×1 | 加入 multimodal memory、安全与 rollback 方向 |
| [Seg-Agent, 2605.12953](https://arxiv.org/abs/2605.12953) | training-free visual feedback + generation/selection/refinement loop | **UNRESOLVED_MISS** | 作为 query regression counterexample，修跨类目受控道 |
| [TimeLogic, 2606.01631](https://arxiv.org/abs/2606.01631) | primary cs.MM、training-free evidence-seeking VideoQA agent | QUERY_HIT×1 | 用作真正独立的 cs.MM sentinel |
| [AudioGenie, 2505.22053](https://arxiv.org/abs/2505.22053) | training-free multimodality-to-multiaudio multi-agent，含 supervisor feedback/self-correction | QUERY_HIT×2 | execution-early omni/audio system component |
| [Dopamine Audiobook, 2504.11002](https://arxiv.org/abs/2504.11002) | training-free MLLM agent、TTS 动态选择与自评 | QUERY_HIT×1 | evaluator/control-plane/audio component 对照 |

这张表给出两个重要结论：

1. “未列为 92 seed”不等于检索失败；六篇可被 query 找到，系统 mapping 正是发现它们的阶段。
2. 但 Seg-Agent 已证明存在一个类别约束造成的真漏检；该项必须在签署前修，因为我们已经知道它。

## 8. 是否超越 Stage-1A

### 8.1 当前 P0-R8 批次：没有实质越界

`af96a89` 本批新增的是 query/seed/route/schema/fixtures/replay/access log，没有模型 rollout、数据集推理、
benchmark 或效果结论。known-ID dereference、venue status search 和离线 matcher 属于 Stage-1A 的 survey
准备与事实核查，不是 Stage-1B 模型实验。

仓内确实保留 W1 的历史 best-of-N 与 W4 的历史 probing 结果，但正典明确把它们标为既有证据并冻结；
它们不是本 correction 批次新跑的结果，不能用来指控本轮越阶段。反过来，也不能把这些历史结果的证据
等级偷偷升级成当前 proposal 的新证明。

“discovery queries executed = 0”在**协议 mapping query**的窄义下成立；同时项目确实发生了 known-ID
访问、route probes 和 8 次 venue-status web search。团队已做双计数披露，现阶段不构成语义隐瞒。

### 8.2 继续允许与继续禁止

允许：修 validator、补 negative fixtures、增加/镜像 query categories、准备 executor/REC writer、做
synthetic dry-run、登记新增论文、修正 provenance。

禁止：签署前执行系统 mapping query/T1 scan；Stage-1B release 前触碰模型或数据集推理；把任何候选
controller/memory/agent loop 写成已收敛路线；用第三阶段资源压降逻辑提前设置预算 cap。

## 9. 科研诚信裁决：高风险控制缺口，不等于已证明造假

### 9.1 支持无罪解释的证据

- 所有公布的确定性脚本输出均可独立重现并与 committed blob 一致；
- manifest 逐项短 hash、fixtures tree、历史不回写检查没有发现伪造（但集合基数 31 应为 33）；
- 7 个论文 ID 和核心内容真实；
- route 纠错保留了 v1 历史件，没有静默抹去前错；
- 没有本批次模型实验、捏造效果或隐藏负结果可供认定。

### 9.2 已成立的 QRP / integrity concern

- 把“fixtures 覆盖了 14 个负例”表述为“V1–V13 全合同机器强制”；
- 把“collector 有 50 行”表述为“外部状态审计 PASS”；
- 把“重数且唯一”表述为“正典精确计数已强制”；
- 把单侧 cs.MA held-out 表述为整个 cs.MM/cs.MA 补洞的独立验证；
- 把 source-normalized 文本表述为 verbatim。

这些可以由过度自信、验收 oracle 设计不足和用词不严解释；目前没有证据证明主观造假意图。因此裁决仍
是 `FFP NOT ESTABLISHED`。但这份报告之后若仍原样声称“零新发现/全字段强制/可签署”，则会变成明知
反例后继续作失实完成态陈述，应升级为 formal research-integrity review，并由 owner 之外的独立人员
保管输入与重放。

## 10. 签署前详细整改计划（给研究团队 AI 的执行合同）

### P0-1：让 package summary 真正 fail closed

1. 从一个正典 constants/manifest 读取并强制：92 seeds、55 queries、50 routes、21 sentinels、2 held-out、
   compiler/protocol 版本、prefix hash 和期望类目集合；任何偏差非零退出。
2. 不从手写 evidence JSON 单独继承 PASS。对确定性项在隔离目录重跑 producer，核对 producer hash、
   input hash、output hash；或至少校验 persisted report 中完整的 producer/input/output lineage。
3. route collector 只能报 `EVIDENCE_PRESENT`，不能由 `n_routes=50` 变 PASS。新增独立 adjudication validator：
   逐 route_id 对齐 v2、collector row、tier-B/C locator、adjudicated status 和日期；缺行、重复、空 evidence、
   状态无依据都失败。
4. active signature surface 从 bundle manifest 机器生成，不能手写七个文件。stale-token 豁免改成结构化
   historical block 或 occurrence-level 标注；同一行出现 marker 不得吞掉其他 active token。
5. 加入本报告已证明的 negative fixtures：2 seeds、空 route rows、陈旧 token+marker 同行、篡改 cached
   verdict、缺 active file；它们必须全部非零退出。

**验收：**原始包 PASS；上述五类 mutation 全 FAIL；输出列出精确期望值与实测值，不能只列唯一性。

### P0-2：补全 REC-0/REC-2/claim 双向 lineage 与内层 schema

1. 对每个 INCLUDED REC-0 强制唯一 REC-2，并同时满足：
   `REC0.extraction.rec2_backref == REC2.id` 且
   `REC2.rec0_backref == REC0.canonical_id`；拒绝 orphan、many-to-one、cross-wire。
2. validator 必须读取 frozen seed manifest 或其 hash-pinned projection，以 canonical ID 联结 `initial_tag`；
   seed 中的 DIRECT_THREAT 不得在 REC-2 转录时消失。
3. 给 matrix、tf_audit、source_axes、omni_axes、rl_identity、proximity、extraction、resource_axes、
   method_occupation、evidence_axes 定义内层必填键、enum、非空规则；`{}` 不得算完整 block。
4. `publication_status` 只保留一个正典位置；D1/D2 共享字段不能一处 top-level、一处 evidence_axes 而靠
   人工记忆解释。
5. `OTHER:<text>` 与 `DUPLICATE_OF:<id>` 后缀必须非空，duplicate target 必须存在；非法 type 形成可读
   violation，不允许 validator crash。
6. 新增至少以下负例：cross-wire、orphan、many-to-one、空 D2 block、非法 inner enum、seed threat tag
   被删、DIRECT_THREAT 无 dual coding、空 duplicate target、bad disagreements type。

**验收：**本文三组对抗 fixture 均非零退出；每个 violation 给 rule、work ID、字段路径和原因。

### P0-3：修 coverage 验收，不靠不断加 seed 掩盖 query 盲区

1. 将 TimeLogic 2606.01631 作为 reviewer-supplied、primary-cs.MM、未参与原 query 词项设计的 sentinel；
   先冻结其来源/version/hash，再运行，预期现有 SF-L11 QUERY_HIT。
2. 将申请中“VQQA 验证 SF-L11 类目补救”更正为“VQQA 验证 cs.MA 一侧”；MAR3 标为 seeded regression，
   不再称 held-out。
3. 将 Seg-Agent 2605.12953 登记为 query-regression counterexample。优先把 SF-L11 Q1 的**既有词项**镜像
   到受控 `cs.CV/cs.AI` categories，或提供等价、可审计的 rescue；不要从 Seg-Agent 摘要发明新词项。
4. category 修订后由另一名 reviewer/agent 提供一个未参与修订的 cs.CV/cs.AI held-out；任何 rescue 都
   不成立时必须 UNRESOLVED_MISS，不允许 explanation 转 PASS。
5. WorldEvolver、MemoPilot、PolarMem、AudioGenie、Dopamine 进入 execution-early queue；它们无需在
   gate 前完成 D2 精读，但既已由本轮发现就不得再次丢失。

**验收：**TimeLogic=QUERY_HIT；Seg-Agent 从 UNRESOLVED 变成可解释的 QUERY_HIT/预注册 seed rescue；
fresh held-out 不因 seed 污染而通过；query 前缀历史保持，新增行采用 appended/versioned amendment。

### P0-4：修 abstract 与 boundary provenance

1. 对 7 份 sentinel abstract 二选一：保存 exact raw Atom/abs text + URL/version/time/hash；或把字段改名为
   `source_normalized_abstract` 并登记 URL 替换、LaTeX escape、whitespace 规则。
2. `REGISTERED_BOUNDARY` 必须验证 dated amendment 中存在 paper ID、boundary code、理由、裁决者和日期，
   不能只查文件存在。
3. 为两项各加一正一负 fixture：正确登记通过；路径存在但无该 ID 必须失败。

### P0-5：再次窄幅复审与签署条件

新提交只需要覆盖 P0-1…P0-4，不要求模型实验、不要求继续无限扩张 proposal。新 bundle 必须以 git blob
固定；外部 reviewer 重跑原七项加本文 mutations。只有 **0 新 MAJOR、0 新 MINOR**，方可签署 mapping
execution gate；之后仍需 owner 单独批准首条 query。Stage-1A close 与 Stage-1B release 继续是两个决策。

## 11. Survey 后续应组织出的 proposal 检查点（非本 gate 的实验要求）

1. **核心冻结与外部组件训练分离。** AMC/MemoPilot 类工作必须分别编码 base model、value/updater、
   method-specific training、test-time update，禁止用一个 `training-free` 标签混洗。
2. **read-out、环境反馈与 new-info 分离。** 自采样、verifier、真实环境转移、web/RAG 外部答案信息对
   “激活预训练知识”的归因完全不同。
3. **状态寿命与污染传播。** within-item trajectory、across-item rule/skill/memory、world model context、
   negative memory 分层；Useful Memories 与 PolarMem 应组织 rollback、停止和冲突抑制问题。
4. **system-level omni 与 component multimodality 分离。** AudioGenie、Dopamine、MAR3、Seg-Agent、
   TimeLogic 是重要组件邻居，但只有同时编码核心看到什么、工具 I/O、行动模态、反馈闭环和因果 grounding，
   才能判断是否构成 omni agentic system。
5. **controller 的可部署性与训练身份。** reward/critic/value/evaluator 从哪里来、是否读 gold、是否训练、
   是否可黑盒部署，必须与论文自称 RL 分开裁定。
6. **Stage-1B 配置合同先纸面化。** dataset/model/inference/evaluator/control-plane/stopping 采用配置化抽象，
   但现在只定义 schema 和 dry-run；真正模型调用等 Stage-1B release。

## 12. 给研究团队 AI 的无歧义执行摘要

不要把本报告理解成“重做整个 proposal”“立刻跑模型”或“签署前读完所有论文”。下一步只有四类离线
修复：

1. 让 package summary 对精确计数、真实 evidence 和 stale-token mutation fail closed；
2. 修 REC 双向 lineage、seed threat 联结和 D2 内层 schema；
3. 用 TimeLogic 验证真正 cs.MM held-out，修 Seg-Agent 跨类目漏检；
4. 更正 verbatim/boundary provenance，然后提交新 blob bundle 复审。

在此之前：**reviewer signature = WITHHELD；协议 discovery query = 0；模型触碰 = 0；Stage-1B = NOT
RELEASED。**

修复之后若窄幅复审零新发现，应及时签署 Stage-1A mapping execution gate；不要再借本报告设置预算 cap、
要求 Stage-2 数字，或把 survey-ready gate 无限延长。
