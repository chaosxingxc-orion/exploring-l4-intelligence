---
artifact_id: "SF-STAGE1C-DIRECTION-REVIEW-TEMPLATE-V1"
role: "R2-R9 owner 协同重审的统一模板；按 2026-07-29 方向成立判据（Decision-Log 续76）"
status: "DRAFT_FOR_OWNER_COREVIEW; owner 未签"
authority: "owner direction criterion 2026-07-29; template wording executor-drafted"
execution_authority: "STAGE2A_WITHHELD"
---

# 研究方向重审模板 v1（07-29 判据）

> 用途：R2–R9 逐个按本模板产出一份 co-review 底稿，owner 逐节裁定后该方向才离开
> `OWNER_UNVERIFIED`。模板本身经 R2 首例校准后由 owner 定稿；在此之前对 R3–R9 只是草案。
> 文体要求（来自 R1/R2 整改教训）：文献归纳 + 方向处置，不是方法设计书；每个承重项给
> What/Why/How；量词必须带范围限定词。

## §1 方向元信息

ID、主维度、evidence_cut、前版 proposal 路径、本次重审输入（dossier/registry/ledger 条目枚举）。
所有承重引用必须能回溯到本地全文 hash 登记（`2026-07-17-sf-fulltext-ledger.jsonl` 或 registry
jsonl）；裸名引用 = 该节不合格。

## §2 两型归类（判据核心）

- **(a) 型**：列出本域（speech/omni）已有工作清单，每篇给「方法 / 局限 / 改进空间 / 可借鉴」
  四问答案（DFS 四问，找台阶不判生死）。已有工作将作为方法论基线参与对比。
- **(b) 型**：论证本域为空的检索范围与检索道（何时查过、查了什么、为何判空——判空必须给
  scope），再列跨域 donor 及各自借入的内容（协议/状态表示/算法/统计量；效果不跨模态外推）。
- 归类结论一句话 + 论证。混合型（本域有部分工作、改进杠杆借自跨域）按 (a) 报告并单列 donor。

## §3 具体任务定义与 readiness

- 任务载体：数据集官方名称、版本/revision、官方 split、样本数、获取渠道。
- readiness 逐项表：本地是否落盘 / hash / `docs/datasets.lock.json` 状态 / license /
  评测协议依赖（含 judge 模型这类外部 API 依赖）——缺项如实标注，不得以「已 pin」散文代替。
- 明确排除项：哪些论文资产不可用（未发布/不可复放），以及因此**不做**什么（不自建、不重标、
  不补快照）。

## §4 SOTA 基线锚定

- 存量业内最优是什么：系统/论文、数字、协议口径（judge、runs、subgroup），全部带 ledger/registry
  可回溯出处。
- 分层：必须复现的基线（等预算对照臂）/ 只引用不复现的参考数字，并说明理由。
- 参考论文之间不可公度时如实分列，不新造统一指标合并。

## §5 改进空间与研究问题

- 从 §2 四问的「局限/改进空间」推出候选杠杆（渐进推边界，不追概念新颖）。
- 每个杠杆过两道判别：read-out/new-info 判别（是否引入部署时不存在的信息）；
  与北极星一致性（API-only、reward-guided、TFRL 路线）。
- 明确研究问题一句话：在〈任务〉上，〈杠杆〉能否在等预算下相对〈SOTA 基线〉带来可靠提升。

## §6 对比实验骨架与数字击杀阈值

- 对照臂清单（direct、SOTA 复现臂、random/matched-cost 对照、目标杠杆臂）；等预算约束。
- 指标复用官方口径；报告项含 paired delta、下置信界、seed 方差、subgroup、cost。
- **数字击杀阈值（必填）**：SESOI、判死条件、降级/重路由去向。数值可标
  `TBD_AT_AUTHORIZATION` 但必须给出提案默认值；零数字阈值 = 该节不合格。

## §7 边界与暴露声明

API-only / gold fence / 数据与指标复用边界 / 本次重审的 exposure 四字段记账
（发生了什么检索/阅读，没发生什么执行）。

## §8 处置建议与 owner 裁定

- 执行者建议（GO_STANDALONE / MERGE / NO_GO）+ 最强反方论证（对抗分析：保留/挑战/备选）。
- owner 裁定栏：结论、日期、Decision-Log 条目号。**本节 owner 落笔前，全文一律
  `owner 未签`。**

## 验收清单（每份底稿自检）

1. 承重引用 100% 可回溯本地 hash；2. 两型归类有论证非断言；3. readiness 表无「散文代替事实」；
4. SOTA 数字有出处；5. 每杠杆过 read-out/new-info 判别；6. 击杀阈值带数字；7. 文体为归纳+处置；
8. 量词带 scope；9. 与保留方向的管辖冲突已显式讨论（判据均匀适用，不选择性执法）；
10. exposure 四字段完整。
