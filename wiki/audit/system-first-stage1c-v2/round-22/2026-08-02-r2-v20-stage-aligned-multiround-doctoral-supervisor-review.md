---
title: "R2 v20 阶段对齐的多轮隔离博导审查：Stage-1C 通过，正式开题许可可签发"
artifact_id: "SF-STAGE1C-R2-REVIEW-R22"
date: "2026-08-02"
campaign: "system-first-stage1c-v2"
round: 22
reviewed_artifact: "wiki/survey/workbench/stage1c-portfolio/proposals/2026-07-29-r2-coreview-draft.md"
reviewed_artifact_id: "SF-STAGE1C-R2-COREVIEW-V20"
reviewed_commit: "97ad413e71ced562fd4cb858caf7896305eb0ca4"
reviewed_git_blob: "cfbc0616ca25359f07a85c7c56099862bba1bd8f"
reviewed_sha256: "1d74fc255abc593fa9f8c9f9a39508d15663d0dcd9d673cf2c1a5a20636d44d1"
reviewed_bytes: 248775
review_scope: "Stage-1C problem selection, literature sufficiency, technical testability, round-21 report-level closure, and Stage-2A handoff readiness"
novelty_scope: "OUT_OF_SCOPE; technical innovation converges in reproduction-first Stage-2A and is validated in Stage-2B"
method_convergence_scope: "OUT_OF_SCOPE; v20 freezes an exploration space, not a final innovative method"
review_method: "two stage-aligned isolated reviews plus fresh primary-source and local-asset counter-verification"
literature_cut: "2026-08-02"
verdict: "PASS_STAGE1C_FORMAL_OPENING"
formal_opening_permission: "ISSUED_IN_COMPANION_NOTE"
stage2a_authorization: "WITHHELD_PENDING_OWNER_GO_AND_EXECUTION_CONTRACT"
human_signature_claimed: false
---

# R2 v20 阶段对齐的多轮隔离博导审查

## 一、裁决

**裁决：`PASS_STAGE1C_FORMAL_OPENING`。v20 已达到正式开题条件；允许开题 note 在本轮 companion
文件中签发。**

本裁决确认的是：研究问题值得选，学界现状足以定位问题，待验证技术点具有合理的可实现性与失败
价值，Stage-2A 的最近邻复现清单和探索约束可以从报告中冻结。它**不确认**具体技术创新已经成立，
不冻结最终创新方案，也不声称任何方法优于 prior。技术创新应在 reproduction-first Stage-2A 中通过
复现与方向性原型收敛，并在 Stage-2B 的冻结验证中确认。

正式开题许可也不等于执行许可。独立 study 建仓、模型/API 调用、指标运行、论文复现、原型与实验
仍需 owner 单独签发 `OWNER_GO_AND_EXECUTION_CONTRACT`。

## 二、阶段边界：本轮实际审什么

现行正典 `wiki/Research-Methodology.md` 与 Decision-Log 续74/续83 已经明确：

| 阶段 | 本项目中的任务 | 与本轮的关系 |
|---|---|---|
| Stage-1A | 问题与 survey 设计 | 已关闭；不裁技术创新 |
| Stage-1B | systematic mapping 执行 | 已关闭；只映射方法路径与邻近关系 |
| **Stage-1C** | **综合证据、owner 选题，冻结 Stage-2A prior 复现清单与探索约束** | **本轮签字对象** |
| Stage-2A | 最近且最强 prior 复现、方向性原型与技术创新收敛 | 尚未获执行授权 |
| Stage-2B | 冻结方案后的正式验证与统计推断 | 尚未开始 |

因此，下列问题不能被用来拒绝当前开题：三支柱最终是否合并/拆分、哪一种 controller 才构成最终
创新、最终 estimand/SESOI/power 数值为何、方案是否在实验上真正优于 prior。owner 已明确裁定“三
支柱维持，拒绝在零实验的开题期预判收窄；收敛发生在 Stage-2 的大量基线实验中”。

一组早期内部对抗镜头曾以“开题前确定创新性、只保留单一 estimand”为标准给出拒签意见。主审在
建立审计交易前发现其违反阶段正典与 owner 裁决，故该镜头被废弃，不进入本轮证据或裁决。随后重新
发起的两个 stage-aligned 隔离包分别审查正式开题就绪度与 round-21 十项整改；本件只采用后两轮。

## 三、为什么 v20 可以正式开题

### 1. 问题成立，而且与北极星直接一致

报告研究冻结、API-only speech/omni 核外围如何组织、供给和使用证据，并把音频重处理 OBS 与外部
证据 SUPPLY 分开；它直接服务“冻结核心之外的 reward-guided control plane”这一项目北极星。RQ0
通过 OBS×外证 2×2 析因避免把“听不清”和“缺外部信息”混成一个概念；RQ0–RQ4b 最终输出为可并存
的结论向量，不再以一个总标签掩盖局部失败。

R1 日落的根本原因是缺少可比较的独立研究问题；R2 与之不同。它已有清晰任务、同域 prior、强反向
先验、可运行/需重实现/只作结构参照的基线分组，以及每层失败后如何收缩范围的出口。即使 Stage-2
最终证明若干支柱不承载，负结果也能明确改变研究范围，而不是让方向失去可解释性。

### 2. 学界现状已经足以支持选题，而不是声称“无人做过”

v20 用五条研究线、21 件直接近邻矩阵和 145 项独立参考文献，覆盖 contextual ASR、实体检索/
纠错、音频 RAG、长音频组织/规划、主动工具/证据控制、载体与评价。RECOVER、Audio-Mind、PRISM、
ConEC、RECAST、BR-ASR、Siskos、GRGA、PlanRAG-Audio、Speech-Hands 等均被放在明确的信息边界与
训练态中。报告不把候选 gap 写成已成立创新，也不作 first-ever 断言。

本轮新检索又发现四件应带入 Stage-2A threat/reproduction queue 的直接工作：Corona et al. 2017
的黑盒 ASR N-best 重排、Raghuvanshi et al. 2019 的黑盒 ASR 字符/音素实体消歧、Flemotomos et al.
2024 的音频接地大目录短选，以及 2026-07 的 COALA。这些工作会影响后续 prior reduction 与基线
选择，但没有推翻“在冻结 omni 核上重新复现最强 prior 并探索 ORG/SUPPLY/USE/CONTROL”的问题
可研究性，故不构成 Stage-1C 阻塞。

- https://aclanthology.org/I17-2021/
- https://aclanthology.org/D19-3011/
- https://arxiv.org/abs/2411.00664
- https://arxiv.org/abs/2607.08117

literature cut 冻结为 2026-08-02。此后新增论文默认进入 delta ledger；只有改变问题可研究性、主载体
合法性/信息边界，或提供同合同更强可运行 prior 时，才触发 `STOP_THE_LINE`。普通新增近邻不再回滚
正式开题或拖延 Stage-2A。

### 3. 待验证技术点在技术上值得做

本轮不判断它们是否创新，只判断是否有充分理由投入 Stage-2A：

1. **OBS 与外证是否具有不同的可恢复余量。** 听错实体会产生“高相关但错误”的检索链；2×2 析因
   能判断重听、真外证及其交互是否值得继续。
2. **知识组织形式是否改变可访问性。** key、切片、面与发音库在旧 ASR/白盒模型上的结论，未必能
   直接迁移到 Qwen3-Omni；reproduction-first 重审具有明确价值。
3. **来源选择是否比无条件合并更稳健。** ConEC 的 slides、财报稿与参会者名单具有不同覆盖与干扰
   结构，K-SUP 可以给出边界化结果。
4. **证据准入是否减少错误修正。** contextual biasing 和 RAG 已显示上下文既可能改善实体，也可能
   恶化总体转写；显式 admission 的 correct-to-wrong 代价值得独立测量。
5. **reward-guided 配置/序贯控制是否有承载力。** 档 A/档 B 的身份与价值无需在开题时预判；v20
   已给出与 random/Bayesian/evolutionary search、固定/串行策略相比较的探索框架与失败出口。
6. **omni-only 系统能否在实体轴逼近或超过专用 ASR 管线。** 这是高风险 capability-first 假设，
   不是方向成立前提；无论支持、反证或不确定，都能产生有用的系统边界。

这些问题既有强 prior 可复现，又有明显相反证据，不是“先假定一定有效”的工程项目；它们正适合在
Stage-2A 通过实验收敛。

### 4. 载体与工程起点真实存在

Earnings21、Earnings22 与 ConEC 已在本地按固定 revision 完成 D0 物化；PRISM、Rare5k 重建等诊断
资产也已登记。Qwen3-Omni Q8、mmproj 与固定 llama.cpp 构建已有本地可核验起点。ConEC 提供真实
财报电话会材料、修订 reference 与实体上下文；E21/E22 提供 44/125 calls 的真实音频主/dev 载体。

这不等于论文 exact reproduction 已经成立。ConEC shallow-fusion、RECOVER、RECAST 等公开实现不完整，
E22 缺 E21 同型实体标注，ConEC/第三方材料再分发许可仍需限界，llama.cpp Q8 也不能冒充 Qwen 官方
BF16/vLLM 结果。这些事实已经被正确路由为 D1–D4、baseline readiness 与 execution-contract 义务；
它们支持“需要 Stage-2A 复现”，而不是迫使继续停留在 Stage-1C。

## 四、round-21 十项签字门复核

| # | 签字门 | 主审状态 | v20 关闭证据 |
|---|---|---|---|
| 1 | RQ0 可识别化；总答案消费全部 RQ | CLOSED | OBS×外证 2×2、错误分型、结论向量 |
| 2 | OBS-INDEX 与外部知识结论分离 | CLOSED | 当前录音索引只承担 OBS 组织/访问，不承担 ORG 外证结论 |
| 3 | RQ1 身份一致；RQ3 统一证据准入 | CLOSED | schema/version/provenance 降工程合同；RQ3 名称和操纵统一 |
| 4 | 十一判据显式三态 | CLOSED | 逐项给出 supported/refuted-or-negligible/inconclusive 语义 |
| 5 | K-NB 全称、mandatory、反证与 baseline-not-ready | CLOSED | readiness 在预注册冻结前裁定；冻结后不可缩减，失效即 inconclusive |
| 6 | RQ4a 拆分与档 B 合同 | CLOSED | 4a-1/4a-2 分开；状态、动作、horizon、策略类、探索和 credit 均在案 |
| 7 | TF-Strict 控制器定义 | CLOSED | 按 owner 续87 权威口径落地；是否形成最终方法留 Stage-2A |
| 8 | discovery/confirmatory 隔离 | CLOSED | 调定只在 discovery；confirmatory 预冻结并按源材料分组；E21/E22 另有 call/company 防泄漏 |
| 9 | 直接正式研究线与发表态 | CLOSED | 九件补齐、时间线修正、发表态分权；本地在册主链接不妨碍 venue/DOI 标注 |
| 10 | 有上界、可停止的 minimum path 与效率比率 | CLOSED | 三件依赖、stop/go、调用/GPU/标注/存储量级和完整比率定义均在案 |

隔离闭合轮曾将 #5/#8/#9/#10 标为 PARTIAL。主审不采纳，理由如下：

- #5 的原门要求冻结后不得事后移除对手；v20 的 readiness-before-freeze 与
  `INCONCLUSIVE_BASELINE_NOT_READY` 正是可执行时序，不是漏洞。
- #8 要求调定与确认读数隔离；proposal 已对自建载体按适用的源音频/说话人/主题分组，并对 E21/E22
  另列 call/company 防泄漏。把 company/entity 强加到所有载体超出原门。
- #9 要求正式题名、venue/DOI/链接与证据权重；v20 已给出正式身份，并明示主链接指本地在册形态。
  是否把每行主链接机械替换为出版商 URL 是书目整理，不影响报告可签性。
- #10 要求“资源有上界、依赖可执行、失败可停止”，不要求一个载体或在 Stage-1C 冻结经费采购数；
  owner 还明确拒绝开题期强制收窄三支柱。v20 已给量级上界与停机路径。

因此十项均在 Stage-1C 报告层关闭；不能把 execution-contract 的精确 pin、预算与 power 数值倒灌成
新的开题门。

## 五、非阻塞修正与 Stage-2A carry-forward

下列事项不影响允许开题，但必须进入执行合同或 Stage-2A prior 队列：

1. 将 v20 §9 中 E21/E22/ConEC 的“待获取/可得性”旧义务同步为 `D0_CLOSED`，只保留 D1–D4。
2. 把 RECAST 由“可运行”改为“当前作者仓未发布方法代码、结构/读数参照”；Contextual Earnings-22
   的 release 状态按实际可验证工件冻结。
3. 冻结 mandatory baselines 的 exact revision、信息边界、调优预算、readiness 标准和 fallback；结果
   未就绪时不得偷换成弱对手。
4. 冻结 E21/E22/ConEC 的许可/再分发声明；本地研究可用不等于可公开镜像。
5. D1–D4 关闭 ID/分段/上下文映射、泄漏、评分、十样本 provenance/trace；这些属于当前已授权的
   无模型资产闭包，不产生实验结果。
6. 在 Stage-2A 首轮开始前，把本轮四件新增直接 prior 纳入 reproduction/threat queue；不要求 v20
   为此再升 v21 或重开签字。

## 六、权限与下一动作

- 正式开题：**通过**；companion note 生效。
- 技术创新/具体方法结论：**未判，且本阶段禁止判**。
- Stage-2A：**尚未授权**。
- 当前可继续：既有数据授权内的 D1–D4 无模型闭包，以及 execution-contract 文档准备。
- 建仓条件：owner 明确签发 `OWNER_GO_AND_EXECUTION_CONTRACT` 后，才能创建语义独立仓
  `audio-aware-evidence-acquisition`，登记 `studies/registry.json` 和 Wiki 实验索引。
- Stage-2A 入口：先做最近邻/载体/评分链 reproduction，不以一开始执行 v20 全部 `10^5` 调用为目标；
  reproduction 结果再决定三支柱的合并、拆分、日落与技术创新形态。

**最终结论：v20 逻辑与证据已足以支撑问题选择；技术风险真实、可验证且值得进入 Stage-2。允许
正式开题，下一道门是独立的 owner execution contract，不是第 23 轮开放式论文扫描。**
