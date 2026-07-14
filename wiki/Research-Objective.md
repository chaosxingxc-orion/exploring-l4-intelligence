---
title: "Research Objective & Current State — 日常加载的唯一现状入口（热层）"
role: "认知层：现状/研究对象/约束/open items/取代索引的单一极简入口。派生自 Decision-Log（审计层），可重建，非唯一记录。被取代的条目掉出本文件（在 archive/ 与 Decision-Log 里）。"
maintained: "每有取代关系变化即更新本文件；新决策先 append 进 Decision-Log 再反映到此。"
last_refreshed_commit: "self-referential hash unavailable pre-commit; this file's post-commit (commit, blob) triple is recorded in docs/integrity/record-policy-and-attestations.md. Last refresh: 2026-07-14 (续39 P0-rereview accepted: 2 CLOSED + 6 PARTIAL, identity-indexed tokens)."
---

# Research Objective & Current State

> **给读者/agent 的一句话**：默认只读本文件 + `CLAUDE.md`。要某条决策的出处才去 grep
> `Decision-Log.md`（冷档案，勿整篇读）。术语见 CLAUDE.md 术语表。
>
> **阶段 vs 工单速查（owner 2026-07-14 要求）**：项目阶段只有 Stage-1A/1B/1C → Stage-2 → Stage-3
> （**现在 = Stage-1A 收尾**）。P0 / P0-R / P1 是评审开出的 **Stage-1A 内部整改工单批次**（初审 P0
> 八项 → 再复审 P0-R 返工八项 → 选题前置 P1），C1–C5 是诚信核查包（C1/C4 为 Stage-1B 前置）——
> 它们都**不是**阶段。**排序（owner 续40 裁决）= 1A→1B→1C**：工单关闭 + Stage-1B 四探针（C1/C4
> 关闭+协议 owner 签批后开机）→ 申请 STAGE1C_DECISION_READY → owner 以调研+探针**双证据**做
> Stage-1C 选题收官。

## 现在在做什么（Stage-1A · 问题界定）

- **阶段**：Stage-1A（广泛 survey / 候选问题 / 原型空间纸面设计 / 风险审查）。**Stage-1B 未放行、M2 冻结**。
- **研究对象（续34 锁定）**：**一个 label-free、供给条件的选择算子,在冻结 omni〔模型 × 任务〕矩阵上的
  兑现面（ρ(c)/H(c)/regret）**。ASR 是其中一行,非全部。**广度定位（续35 校准,reassessment §11.2-E）**：
  `survey_scope=cross_task_cross_model`;`scientific_question_status=candidate_not_selected`;
  `novelty=unverified`;**`breadth=external-validity 维度,不是本身即贡献`——"护城河"是工作假设,非已证新颖性**。
- **伪统一守卫**：共享对象 = 算子 + H(c) 记账法统一;各任务各留效用 U 与 SESOI;度量同一算子在每格的 ρ(c)
  （**cellwise-only,禁止无权重的"总 ρ"平均**）;**部署用 label-free proxy `S`,评估用 `U`,二者不混**。
- **候选身份（Stage-1C 才选,现不选;现状=续39 按身份索引表,详 RESP-02 §3.3）**：I1=DIRECT_OCCUPIED
  （kill 方向保持,MBR 更正后更强）/ bare-I2=机制级占据（scaling-auditory 同核 beam log-lik）、任务格
  覆盖 MIXED/UNDERSEARCHED / strict-I2=POST_HOC_NARROWED_CANDIDATE（=I2∩I4,07-14 post-hoc 合成）/
  I3=abstain 分量已占,I3-combined 在保留记录中无匹配 / **I4=METHOD_FAMILY_OCCUPIED,音频/omni 供给
  分层实例化 UNDERSEARCHED,增量预测贡献未示** / UMBRELLA（第五候选）=保留记录中无匹配（IAD=预登记
  坍缩风险）。**否定性结论必须按身份索引并带强制伴随 token（RESP-02 §3.3）,全局 token 停用。**

## 现在绑定的约束（硬）

- weight-frozen（不改权重/结构）;**信息边界**：test-item gold 不入 selector/reward/prompt/检索/候选构造。
- 证据全 directional-only / hypothesis-grade——**无任何确证宣称**;有头空的 null 才证伪 selector（headroom 归因纪律）。
- **append-only**（改写历史=reviewer 升级触发）;**哈希正典=git blob 字节**;发布前对未提交工作树跑敌意自检、零确认才提交。

## Open items（live）

1. **Survey v2 = ROUND1_SCOUT_COMPLETE；P0 整改 = 2 CLOSED + 6 PARTIAL（再复审拒签已接受,续39）**：
   15 敌意 lane / SEARCH 218 + FETCH 87（勿合称"305 查询"）/ **94 记录簇（v1 规则集,113→110→104→94;
   非 canonical work census——census=P0-R2 待做,`~93` 不可机械重现）**。两轮博导审查均已核验+逐条
   回应：RESP-01 `2026-07-14-survey-v2-response-and-p0-remediation.md`（其完成度声明/94 标签/全局
   token/签署块已被 RESP-02 supersede）+ **RESP-02 `2026-07-14-p0r-response-to-remediation-rereview.md`
   （现行有效,含按身份索引的最强结论表 §3.3 与三线分签）**。bundle
   `wiki/survey/replay/SURVEY-RESP-2026-07-14-01/`：INTERNAL_BUILD_CONSISTENCY_12/12（仅证字节可
   重建;文献 census 与 claim 台账两条线 NOT_REACHED）;round-1 检索宇宙永久缺失。**按身份最强结论
   （证据级封顶 ABSTRACT_VERIFIED 待双审）**：I1=DIRECT_OCCUPIED（kill 方向保持,MBR 更正后更强）;
   bare-I2=机制级占据/覆盖混合;strict-I2=POST_HOC_NARROWED_CANDIDATE;**I4=METHOD_FAMILY_OCCUPIED,
   音频/omni 供给分层实例化 UNDERSEARCHED,增量预测贡献 NOT YET SHOWN**;否定性结论一律
   AMONG_RETAINED_RECORDS@94簇 + 强制伴随 token（宇宙缺失/饱和不可评估）。**决策包 =
   PRE_STAGE1C_DECISION_DRAFT**——owner 门控:P0-R+P1 关闭、STAGE1C_DECISION_READY 后才提请选题。
   **重排 P1 序列（按再复审 §6 相对顺序并入 §7 的 P0-R 编号,两处偏差列明于 RESP-02 §3.5）**：
   P0-R2 canonical census → P0-R3 真 claim 台账 → identity freeze（含 post-hoc 日志）→ round-2
   protocol freeze → 可回放检索（9+8 篇,含 CoVer=Proposal E 威胁）→ comparator cards → C1/C4 →
   P0-R8 repo 级状态门 → 独立盲重建。**并行 GPU 线（续40,1B 先行）**：探针协议预注册→owner 签批→
   四探针 P-α 头空/P-β MBR 基线/P-γ 同核信号/P-δ 供给对比（directional-only,单次触碰,尝试全登记）;
   决策包 v2 = 调研+探针双证据。
2. **诚信核查 C1/C4**（Stage-1B 放行前置）：C1 尝试普查（registry vs raw run）、C4 负结果普查。
3. **same-selector contract**（Stage-1C 前）：冻结 operator/score inputs/预算/弃权/gold 边界/池几何,
   跨任务不可固定处显式标 task-specific。
4. **Stage-1C 决策包**：I1–I4 kill/pivot/proceed dossier + 供给收益/selector 收益分解 + 预算公平性 +
   可证伪三结论（proceed/pivot/kill）;**agentic-loop vs 一次性 rerank** 作为开放的 Stage-1C 问题。
5. **知识栈选型 = PARKED（续37）**：外来评审（llm-wiki-compiler 试点提案）经六镜头敌意复核后
   owner 裁决**全部搁置**（含 schema-first）,Stage-1C 收官后按四门复活（时机/顺序/规格/裁决）;
   回应 `2026-07-14-response-to-knowledge-stack-evaluation.md`。其新造代号（T0–T4 信任层、方案 A 等）
   **未登记**,引用须带限定语（勿与 T0–T7 探针编号、survey-v2 评审 Proposal A 混同）。

（已闭/移除：reviewer response 已提交 `0be1285` + 接受 reassessment 的 response-v2;冷热归档已执行
`34024fc`,50 文档入 archive/。）

## 取代索引（什么已死 / 被谁取代 —— 见旧条目勿当现状）

| 旧结论/命名 | 现状 | 出处 |
|---|---|---|
| RDU 为 headline | 降为 secondary/ablation | 续32 |
| `A-SEL` 命名 | 正名「选择器兑现率方向」 | 术语表 / 续33 |
| v4.2 = Stage-2 入口 | Stage-1 问题定义交付物 | 续32 |
| `84c6cf6` proposal 草稿 | PRE_STAGE2_BLUEPRINT（无现时效力） | 续33 |
| 程序代号 `W1-ASEL-S2-001` | 冻结弃用 | 续33 |
| 自家 +0.517（检索供给佐证） | 撤引（C-T7 泄漏 INVALID;干净值 −0.066 null） | 续33·勘误 |
| I4 "最干净 whitespace" | broad 死 / narrow 待验（跨矩阵兑现面） | 续34 |
| scope 收窄到 ASR | 反制:ASR 是一行,研究对象是跨矩阵兑现面（reviewer 已接受 breadth-first） | 续34 / 续35 |
| 全 append-only 大文件当主工作面 | 冷热分离,默认只读本热层 | 续34 |
| "非 ASR 格仍空" | **UNDERSEARCHED**（SER/SLU/ST/AAC 祖先已举证） | 续35 |
| "广度是护城河"（已证贡献） | 工作假设,非已证新颖性;`breadth=external-validity 维度` | 续35 |
| P0-SURV-1 = CLOSED | **PARTIAL**（计数可重建/搜索不可重放/科学覆盖 OPEN） | 续35 |
| response `0be1285` 的"格空/护城河"措辞 | 由 response-v2 dated successor 取代 | 续35 |
| "Survey v2 complete / 调研收官"（续36/233dc7e） | **ROUND1_SCOUT_COMPLETE** | 续38 |
| 决策包"待 owner 选题" | **PRE_STAGE1C_DECISION_DRAFT**（P0-R+P1 门控后才提请） | 续38/39 |
| READ "~70-85% oracle" | 更正:Table 1 兑现 7.7–68.5%（LS 仅 12–17%） | 续38·勘误 |
| "~93 papers" → 续38"精确 94" | **「v1 规则集 94 记录簇」**（canonical census=P0-R2 待做） | 续39 |
| I4 "最强空位/strongest differentiator" | METHOD_FAMILY_OCCUPIED;实例化 UNDERSEARCHED;增量贡献未示 | 续38/39 |
| TAP-GER/ProGRes = kill-I1 DIRECT | 重分类:扩池/改写算子,非池内选择占据 | 续38·勘误 |
| 续38"P0 八项全部执行"（RESP-01） | **P0: 2 CLOSED + 6 PARTIAL（3 残留簇）**;RESP-02 supersede | 续39 |
| RESP-01 把 owner 写入 integrity_reviewer 签署位 | **失实更正**:owner 仅两项治理裁决;integrity=PENDING | 续39 |
| 全局 NO_DIRECT_MATCH_WITHIN_LOGGED_SCOPE | 按身份索引 token 表（RESP-02 §3.3）;全局 token 停用 | 续39 |
| "一手数字全部可溯源"（RESP-01 R10 行） | 限定:已抽查者可溯源;未审数字=未核验,不外推 | 续39 |
| "12/12 校验 PASS"（无界定） | **INTERNAL_BUILD_CONSISTENCY_12/12**（仅字节线;三线分签） | 续39 |

## 正典工件指针

- 现状真理：**本文件**。审计真理：`Decision-Log.md`（冷,勿整篇读）、`Per-Work-Status.md`。
- 发布快照：`docs/integrity/release_manifest.json`（git-blob 哈希）+ `docs/checks/manifest-blob-verification-2026-07-13.txt`。
- survey：`wiki/survey/2026-07-13-scout-ledger-round1.json`（8族/57条/46独立,SCOUT 级;**计数可重建,
  raw-query 重放 OPEN,科学覆盖 OPEN**）;Survey v2 产物 `wiki/survey/2026-07-14-*`（生成中）。
- 记录政策/attestation：`docs/integrity/record-policy-and-attestations.md`（冷热分层 + provenance 三元组不变量）。
- 规则/术语：`CLAUDE.md` / `AGENTS.md`（镜像）。
