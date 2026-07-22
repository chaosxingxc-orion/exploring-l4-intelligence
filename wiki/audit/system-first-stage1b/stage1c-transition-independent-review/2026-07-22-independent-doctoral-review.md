---
transaction: "INDEPENDENT_DOCTORAL_STAGE_TRANSITION_REVIEW"
review_date: "2026-07-22"
review_target: "wiki/audit/system-first-stage1b/stage1c-transition-request/2026-07-22-stage1b-closeout-and-stage1c-research-proposal.md"
target_sha256: "ce20cf5db3d9c3890eb30232ee336f0b788ab24afebba5f1d2811b3d49ed5905"
claimed_release_commit: "51b527b88e1f9993f1c2bd9d826f86c73a6a938c"
review_status: "WITHHOLD_FOR_BOUNDED_EVIDENCE_REPAIR"
model_or_reproduction_authority: "WITHHOLD"
---

# Stage-1B closeout → Stage-1C transition 独立严格复审

> 审查角色：严格外部审稿人 / 博士生导师  
> 审查范围：阶段身份、固定 release、引用和论文路由、mapping 与 eligible inputs、阶段越界和 Stage-1C 准入  
> 审查方法：项目既有论文集与本地全文优先；外部检索仅用于核验论文身份、角色与遗漏，不用搜索结果替代本地 D2 证据  
> 写入纪律：本报告为新的独立审查件；未修改 transition proposal、release、CURRENT、registry、脚本或研究代码

## 0. 最终裁定

```text
CURRENT_STAGE                         = STAGE_1B_RELEASE_FROZEN_TRANSITION_REVIEW
STAGE_1B_DISCOVERY_CLOSE              = PASS
STAGE_1B_MAPPING_CLOSE                = WITHHOLD
STAGE_1B_RECORD_RELEASE               = WITHHOLD
STAGE_1C_ELIGIBLE_INPUTS              = WITHHOLD
STAGE_1C_FORMAL_START                 = WITHHOLD
STAGE_1C_TEMPLATE_AND_RUBRIC_PREP      = ALLOW
MODEL_OR_REPRODUCTION_EXECUTION       = WITHHOLD
NOVELTY_VERDICT                       = NOT_REQUESTED_AND_NOT_PERMITTED
ACADEMIC_FRAUD_EVIDENCE               = NOT_ESTABLISHED
REMEDIATION_SCOPE                     = TARGETED_EVIDENCE_AND_RELEASE_REPAIR_ONLY
NEW_BROAD_D0_CAMPAIGN                 = NOT_REQUIRED
```

本轮与上一轮不同：团队已经把 D0、delta、T1 disposition、citation surface、mapping tables 和 eligible inputs 固定到 Git release；本审查独立重算 release manifest 后确认 **37/37 个已列入 manifest 的对象 bytes 与 SHA-256 全部一致**。因此，不能再指控团队只是用未提交工作树拼装结论，Stage-1B discovery close 可以通过。

但是，本次仍不能签署 Stage-1C。阻断原因不是需要更多无边界搜索，而是三个非常具体的承重缺口：

1. mapping release 明确引用的页级 D2 证据文件没有进入 release manifest；“37/37 全绿”只验证了清单内对象，没有证明承重清单完整。
2. 11 条 strict occupancy 路径全部来自 text/vision，speech/audio-native strict path 为 0；与此同时，三个可选问题都面向 speech/voice。语音直接近邻只存在于非 manifest-bound workbench notes，未进入同一编码合同。
3. 团队已有全文证据中的 AudioGenie-Reasoner 是 budget/stop/repair 家族的关键直接反证，却从 mapping release、eligible-input bundle 和 proposal 三者中消失；interactive bundle 又使用了缺少自包含引用与统一 D2 路由的 EVA-Bench、JarvisBench 等工作。

这是“接近放行、但尚不可签字”，不是“推倒重来”。完成文末 R1–R4 后可直接重新申请 Stage-1C，不应重开 20,727 规模 discovery。

## 1. 当前究竟处于哪个阶段

当前不是 Stage-1A，也不是普通 Stage-1B 执行期，而是：

> **Stage-1B release frozen / independent Stage-1C transition review pending。**

判定依据：

- Stage-1A search design 已签字，Stage-1B survey 已实际执行；
- frozen D0 20,727/20,727 有摘要处置；
- 65/65 delta rows 和 50/50 T1 route dispositions 已记录；
- mapping release 与 unranked eligible inputs 已形成；
- 固定 release commit 为 `51b527b88e1f9993f1c2bd9d826f86c73a6a938c`；
- proposal 请求的权限仅为 `STAGE_1C_PROBLEM_SELECTION_ONLY`，没有请求模型、指标、复现或 novelty authority。

因此，当前审查问题不是“能否开始 Stage-1B”，而是“Stage-1B 的证据对象是否足以支持 Stage-1C 进行问题选择”。

## 2. 审查快照与复核结果

### 2.1 当前审查对象

| 对象 | bytes | SHA-256 |
|---|---:|---|
| transition research proposal | 16,803 | `ce20cf5db3d9c3890eb30232ee336f0b788ab24afebba5f1d2811b3d49ed5905` |
| `wiki/Research-Objective.md` | 4,605 | `0da80a8e47cac685623eaad77dd3be3413f179617e112ea3daabbf231104478f` |
| `wiki/Project-Thesis.md` | 6,524 | `5aafddb9d32d085462f619e739cb3d1f8b47740d39d88b0cfc6b38f99e7f9623` |
| effective protocol | 63,244 | `16d04d0b83cf4bf667e6418b5e3edd1a42c51809358c66696a009ffa5f002bda` |
| Stage-1B mapping release | 13,134 | `a7ebcb7d910f46486ca540b25f6722b7d07418e05f43130b7413818e15d8fb94` |
| Stage-1C eligible inputs | 13,900 | `afe4a7a25c470e22bfd574cab3fcf4a62b394a5a1614b219714cc2014407d6f7` |
| release manifest | 13,861 | `51e3229352354c3f20ffa4496536cbf6f6bedd7c715c4e9aadc779439cb84492` |
| opening D2 method-path notes | 31,669 | `f7bec0ba494526aaa2046b334b777038a3e4e1f26b9dd9b48e7b10ae97f02045` |
| current bibliography | 32,333 | `f045d1d1284616b273d068794a7e3bb94cbf118753bae1c4a5e16f9cbe21113a` |

### 2.2 固定 release 的机械复核

对 `51b527b` 中 `release-manifest.json` 的 31 个 Git blobs，以 `git cat-file blob <commit>:<path>` 读取原始字节；对 6 个 external assets 读取本地冻结文件。结果为：

```text
release_id       = system-first-stage1b-2026-07-22-v2
manifest_entries = 37
git_entries      = 31
external_entries = 6
verified         = 37
byte_mismatch    = 0
sha256_mismatch  = 0
missing          = 0
```

这个结果应被正式认可。团队已经纠正上一轮 working-tree evidence 不可引用的问题。

但该复核只能证明“列入 manifest 的 37 项没有漂移”。它不能证明 mapping 文本引用的所有承重证据都已列入 manifest。这正是本轮发现的 P0 缺陷。

## 3. 已经正确关闭的事项

### 3.1 Discovery 与召回债务披露达到放行标准

以下处理合理：

- D0 exhaustion 被限定为 frozen pool，不冒充 literature-universe closure；
- delta 65/65 有 disposition，而不是把网络失败写成 zero hit；
- T1 50/50 有 disposition，明确区分 28 executed、3 not held、19 waived；
- 2,633 个 title-only T1 identities 没有被写成 irrelevant 或 zero hit；
- 232 个 out-of-set backward arXiv IDs、DOI/title-only edges 和 forward HTTP 429 被保留为 limitation；
- 不从 11-path strict sample 推断 prevalence；
- H5 coder B 未完成，团队没有让 H5 进入 occupancy、headline 或 selection；
- model/smoke、metric、reproduction、prototype exposure 均为 0。

因此，本审查给 `STAGE_1B_DISCOVERY_CLOSE = PASS`。未解析 title/citation surfaces 应在 Stage-1C 由具体问题触发定向核验，而不是阻止阶段迁移的永久尾债。

### 3.2 阶段职责表述基本正确

proposal 正确区分：

- Stage-1B：method paths、proximity、contradictions、instruments、reproducibility conditions；
- Stage-1C：比较 eligible problem inputs，选择问题；
- Stage-2A：先复现最近 prior，再收敛技术机制；
- Stage-2B：验证干预与失败条件。

它没有要求 Stage-1B 证明技术创新，也没有把 Stage-1C 签字偷换成模型执行授权。此前被过早冻结的 ASR/omni reproduction material 已降级为 `PROVISIONAL_INPUT / NOT_STAGE_FROZEN`，这一点正确。

## 4. P0：release manifest 未绑定 mapping 自己引用的页级证据

mapping release 在 coverage/kill matrix 后明确写道：Omni-Decision、AOP-Agent、AudioToolAgent 和 EChO-Agent 的 evidence locators 位于：

`wiki/survey/workbench/system-first-stage1b/2026-07-21-opening-d2-method-path-notes.md`

该文件确实存在于 release commit，并包含 PDF/e-print hash、逐篇页码、状态/信号/动作/训练边界和 proximity 说明。然而，它**不在 37 项 release manifest 中**。同样未绑定的还有 `wiki/survey/current/bibliography.md`。

由此产生四个后果：

1. mapping headline 可以被 hash 复核，但其直接证据 locator 不能沿 manifest 路径复核；
2. proposal 所称“37 manifest artifacts 足以支持独立 replay”并不完整；
3. 日后即便 notes 发生修改，当前 release verifier 也不会报错；
4. eligible inputs 中 system-level direct evidence 的页级依据没有进入冻结证据对象。

这是 record completeness failure，而不是 hash mismatch。自动检查全绿不能覆盖一个没有进入检查集合的承重文件。

### 最小修复

- 发布 dated superseding release v3；
- 将 opening D2 notes、self-contained bibliography/reference appendix、任何被 eligible inputs 直接引用的 D2 ledger/sidecar 加入 manifest；
- mapping table 中每一项 direct/system evidence 指向 manifest-bound record 和页码；
- verifier 增加“reader-visible reference → manifest entry”完整性检查，但不需要增加恶意元数据测试。

在此之前：`STAGE_1B_RECORD_RELEASE = WITHHOLD`。

## 5. P0：strict occupancy 与研究对象存在结构性错位

proposal 报告 strict occupancy 为 8 works / 11 paths，其中：

```text
text-native         = 7
vision-native       = 4
speech/audio-native = 0
```

团队诚实写明“0 是未严格编码，不是文献为空”，这避免了虚假结论；但它仍暴露一个准入问题：三个 `ELIGIBLE_NON_H5` 输入分别是 budget/stop/repair、evaluator reliability、interactive/full-duplex，它们全部要在 speech/voice contract 下比较。当前统一 strict schema 却没有一条 speech/audio-native path。

这意味着：

- text/vision priors 可以进入统一 occupancy 分母；
- 语音 direct priors 只以 prose notes 或浅层 registry facet 出现；
- Stage-1C 将无法区分“方法路径确实未占据”和“团队没有用同一 schema 编码”；
- 所谓 common rubric 的 directness、black-box fit、decision rights 和 nearest-prior distance 不能在同一字段空间比较。

Stage-1B 不必严格编码全部 226 篇，也不必估计 prevalence；但至少必须对所有 `ELIGIBLE_NON_H5` bundles 的承重 direct priors 做同合同编码。

### 最小修复

建立一个**有界 speech/omni direct-prior strict supplement**，不重开 survey。至少覆盖：

- budget/stop/repair 的直接语音或 omni paths；
- evaluator reliability 的直接 speech instruments/diagnostics；
- interactive/full-duplex 的关键 benchmark/reference-system paths。

每条必须复用现有字段：core topology、native modality、access、weight/update boundary、signal、decision right、control edge、selection object、stop/repair semantics、load-bearing status 与页级 locator。随后更新 occupancy/sensitivity，或明确建立与 text/vision strict table 平行且可比较的 speech supplement。

在此之前：`STAGE_1B_MAPPING_CLOSE = WITHHOLD`。

## 6. P0：已有论文集中的关键直接近邻被 synthesis 遗漏

### 6.1 AudioGenie-Reasoner 是实质性遗漏

团队已经全文读取 [AudioGenie-Reasoner](https://arxiv.org/abs/2509.16971)，D2 notes 记录：

- 它是 training-free multi-agent audio reasoning system；
- planning agent 输出 `Sufficient` / `Insufficient`；
- `Insufficient` 触发新的音频信息采集计划；
- sufficient 或最大迭代数触发停止；
- 性能在两到三轮达到峰值、第四轮下降，直接暴露 over-iteration harm；
- notes 自己将其定义为 “direct training-free audio state → sufficiency → observe/stop neighbor”。

这篇论文与 budget/stopping/repair family 的 residual question 高度重合，而且比纯 text/vision transfer 更直接。然而：

- `stage1b-mapping-release.md` 没有 AudioGenie-Reasoner；
- `stage1c-eligible-inputs.md` 的 budget bundle 没有它；
- transition proposal 也没有它；
- 承载它的 D2 notes 又未被 manifest 绑定。

这不是“还可以补一篇 related work”的普通编辑问题，而是可能改变 strongest contradiction、kill criterion 和 nearest-prior shortlist 的承重遗漏。Stage-1C 在看见它之前排序 budget/stop/repair，会形成典型的选择性 bibliography bias。

### 6.2 其他已捕获但未进入 active synthesis 的高价值边界

以下不是全新的 universe omission；它们已经出现在 frozen D0 或 delta，但当前 active synthesis 没有充分利用：

- [VoiceAgentRAG](https://arxiv.org/abs/2603.02206)：D0 中为 `DEFER_ABSTRACT`。其 background Slow Thinker + foreground Fast Talker + proactive retrieval cache 是 realtime voice agent 的外部 memory/routing 系统，应进入 interactive family 的 alternative explanation 或 boundary comparator。
- [Daily-Omni](https://arxiv.org/abs/2505.17862)：D0 中为 speech/audio relevance ambiguous。它提供 training-free modular audio-visual agent baseline；主要影响 H5-dependent evidence-state/tool-arbitration families，至少应保留定向 D2/边界路由。
- [Building Enterprise Realtime Voice Agents from Scratch](https://arxiv.org/abs/2603.05413)：D0 将其排除为 “speech without target control path” 是合理的，但如果 Stage-1C 比较 interactive/full-duplex objective，它必须作为 latency、cascade 与 pipeline confounding 的 boundary evidence，而不是完全从 problem bundle 消失。

本次外部核验没有发现一个可证明完全位于 D0/delta/T1 之外、且立即推翻三个 eligible families 的新 P0 identity。发现的问题是**论文身份已经搜到，但深度与 synthesis 路由不完整**。因此不要求新 broad campaign，只要求定向升级。

## 7. 引用是否合理

### 7.1 论文角色判断大体正确

对核心近邻的角色判断基本符合论文原始内容：

- AudioToolAgent 是音频工具协调与冲突后追问的直接系统近邻，但不应被写成显式 reward controller；
- EChO-Agent 提供 structured evidence、verifier、repair/regeneration 和 dual-path selection；
- Omni-Decision 提供 evidence state、validation、repair、readiness/exhaustion；
- AOP-Agent 提供 training-free active omni perception 和 observe-reflect-replan；
- $\tau$-Voice、VoiceAgentBench、EVA-Bench 主要是 measurement instruments，不是 control mechanism success；
- JarvisBench 同时具有 instrument、spoken mediation prototype 和 human-guidance boundary，不能只算普通 full-duplex benchmark。

这些角色分离优于把所有包含 “agent” 的论文混成一个 prior class。

### 7.2 reviewer-facing 文档违反自身引用合同

有效协议规定：每个 reviewer-facing artifact 都要有 self-contained reference appendix，包含 author、year、stable link；数字性论文主张需要 page/table/figure locator。

但本次 transition proposal：

- 没有 References/Bibliography appendix；
- 没有论文 stable links；
- 读者无法仅从 proposal 解析 five bundles 所依赖的论文身份。

`stage1c-eligible-inputs.md` 同样只写简称，没有 author/year/stable link；EVA-Bench 和 JarvisBench 甚至不在 current bibliography 中。mapping release 虽给出少量 arXiv IDs，却把页级证据外包给未 manifest-bound workbench notes。

因此引用判断是：

```text
PAPER_IDENTITY_ROUTING               = MOSTLY_CORRECT
ROLE_SEPARATION                      = GOOD
SELF_CONTAINED_REVIEWER_CITATION     = FAIL
PAGE_LEVEL_LOAD_BEARING_PROVENANCE   = INCOMPLETE
ACTIVE_SYNTHESIS_USE_OF_LOCAL_CORPUS = INCOMPLETE
```

### 7.3 “strongest contradiction” 必须限定集合

因为仍有 2,633 title-only T1 identities、232 out-of-set backward arXiv IDs、DOI/title-only edges 和 forward waivers，eligible inputs 不应无修饰地写 `strongest contradiction`。应改为：

> strongest contradiction among the manifest-bound D2/retained evidence inspected by the release

这不会阻止 Stage-1C，但可防止读者把 scoped evidence 误解为全领域最强反证。

## 8. 五个 problem families 的逐项评价

| family | 当前评价 | 主要缺陷 | Stage-1C 状态 |
|---|---|---|---|
| Evidence-state control | 反证意识好，Omni-Decision/AOP/EChO 已证明宽泛 novelty 不成立 | H5 未完成；direct D2 notes 未 manifest-bound | 继续 `INELIGIBLE` |
| Tool/agent arbitration | 已承认 AudioToolAgent/MoBE 等占位，边界合理 | H5 未完成；Daily-Omni、VoiceAgentRAG 等路由未闭合 | 继续 `INELIGIBLE` |
| Budget/stop/repair | gap 可证伪且符合 TF-Strict；VRR/repair harm 方向好 | 漏掉 AudioGenie-Reasoner 这一直接 speech prior；strict speech coding 为 0 | `WITHHOLD` 直至修复 |
| Evaluator/reward reliability | 作为控制系统前置问题很重要；明确 evaluator 不是方法 novelty | 43 instruments 主要是 portfolio 级，不足以证明统一 calibration gap；speech direct evidence 未统一深读/编码 | `WITHHOLD` 直至最小 D2 supplement |
| Interactive/full-duplex | 最符合 system-first 的真实 agent 落脚点，且没有偷称方法成功 | EVA/Jarvis 引用不自包含；VoiceAgentRAG/cascade confounder 未进入反证；部分 instrument 仅 D0 | `WITHHOLD` 直至 targeted route |

这张表不替 Stage-1C 排序问题。它只判断 Stage-1B 输入是否具备被排序的资格。

## 9. 当前研究范畴是否超越本阶段

### 9.1 没有发生实验越界

未发现 research model load、smoke、dataset metric、headroom、reproduction 或 prototype。proposal 的 Stage-2A 路径只是未来流程描述，没有冒充已授权执行。

### 9.2 Stage-1C procedure 本身处于正确边界

Stage-1C 拟进行：

- problem importance 比较；
- 正反证据与 kill criterion 比较；
- TF-Strict/black-box fit；
- measurement feasibility；
- nearest-prior reproducibility assessment；
- owner problem selection；
- 形成后续 Stage-2A authorization request。

这些属于 Stage-1C，不是 Stage-2A。只要不执行模型、不复现、不开发新 controller，就没有越界。

### 9.3 当前真正的问题是“提前可选”，不是“提前实验”

团队把三个 bundles 标记为 `ELIGIBLE_NON_H5`，但它们的承重引用和 speech direct coding 尚未闭合。换言之，当前不是实验超前，而是 **selection eligibility 先于 evidence eligibility**。必须先修正资格，再让 Stage-1C 排序。

## 10. 学术诚信判断

本轮没有发现伪造论文、虚构实验、捏造 37/37 hash replay、伪造 coder B、抄袭或将 paper-reported metrics 冒充 project reproduction。37/37 manifest entries 的 byte/hash 复核确实通过，proposal 也主动披露 title-only、citation-only、H5 和 forward-index limitations。

因此：

```text
FABRICATION      = NOT_EVIDENCED
FALSIFICATION    = NOT_EVIDENCED
PLAGIARISM       = NOT_EVIDENCED
SELECTIVE_SYNTHESIS_RISK = MATERIAL
```

AudioGenie-Reasoner 已经被团队深读但未进入最终 bundle，这构成选择性 synthesis 风险；目前更像交付物整合失败，而不是蓄意学术欺诈。若团队在收到本意见后仍在不披露该 prior 的情况下排序 budget/stop/repair，则风险性质会显著升级。

## 11. 最小整改要求

### R1 — 发布自包含的 superseding release

必须：

- 用 v3 或新的 dated release supersede v2；
- manifest 绑定 opening D2 notes、reference appendix/bibliography 和所有 eligible-input 的直接 D2 证据；
- 修复 release v2 内部仍携带 v1 pointer/35-artifact 叙述的问题，或把 mutable HOT/CURRENT router 明确排除出 scientific release object；
- 提供 reference-to-manifest completeness report。

不需要：增加元数据攻击、恶意路径或篡改脚本测试。

### R2 — 增加 speech/omni strict supplement

只编码本轮承重的直接近邻，不编码全部 226 篇。至少让三个可选 bundles 的 direct speech evidence 可以与 11-path text/vision table 使用同一合同比较。

### R3 — 修复三个 eligible bundles

必须：

- budget/stop/repair 纳入 AudioGenie-Reasoner，并重写 strongest contradiction、kill criterion 和 nearest-prior set；
- evaluator reliability 列明少量真正 load-bearing instruments/diagnostics 的 identity、locator、evaluator error contract；
- interactive/full-duplex 补齐 $\tau$-Voice、VoiceAgentBench、EVA-Bench、JarvisBench 的稳定身份与证据深度，并纳入 VoiceAgentRAG 与 cascade/latency boundary；
- 所有 `strongest` 限定 inspected set。

### R4 — 独立快速复核

复核只检查：

1. 新 release 的 manifest completeness；
2. speech supplement 是否与现有 strict schema 可比；
3. AudioGenie-Reasoner 和 interactive boundary 是否进入正确 bundle；
4. reviewer-facing reference appendix 是否自包含；
5. H5 仍为 WITHHOLD、模型执行仍为 0。

无需重新运行 frozen D0、T1 broad scan 或模型实验。

## 12. 给研究团队 AI 的明确指令

```text
DO NOT reopen the 20,727-work broad D0 campaign.
DO NOT run a model, smoke, metric, reproduction, or prototype.
DO NOT rank or select the three problem families yet.
DO NOT treat 37/37 listed hashes as proof that the manifest is complete.
DO NOT omit AudioGenie-Reasoner from budget/stop/repair proximity.
DO NOT call a speech-native occupancy cell empty; it is currently unmeasured.
DO NOT use EVA-Bench or JarvisBench as reviewer-facing evidence without stable identity and locator.

DO bind every load-bearing D2/reference artifact in a superseding release.
DO create a bounded speech/omni direct-prior strict supplement.
DO revise the three non-H5 bundles using the already collected corpus.
DO add a self-contained author/year/stable-link reference appendix.
DO request a narrow transition re-review against one fixed commit.
```

## 13. 可重审后的预期裁定

若 R1–R4 全部完成，且没有新证据推翻三个 bundles，下一轮应预期：

```text
STAGE_1B_DISCOVERY_CLOSE        = PASS
STAGE_1B_MAPPING_CLOSE          = PASS
STAGE_1B_RECORD_RELEASE         = PASS
STAGE_1C_ELIGIBLE_INPUTS        = PASS
STAGE_1C_FORMAL_START           = SIGN
MODEL_OR_REPRODUCTION_EXECUTION = WITHHOLD
```

本轮不给 `SIGN`，不是因为团队 survey 数量不足，而是因为已有高价值论文和页级证据尚未进入冻结、统一、可比较的承重结构。先修复这个小而关键的断点，再进入 Stage-1C，能够避免下一阶段用不对称证据选题。
