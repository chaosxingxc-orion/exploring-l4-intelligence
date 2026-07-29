---
artifact_id: "SF-STAGE1C-DIRECTION-COREVIEW-TEMPLATE-V1"
role: "R2-R9 owner 协同重审的统一开题报告模板；按 2026-07-29 方向成立判据（Decision-Log 续76）及 owner 同日澄清"
status: "DRAFT_FOR_OWNER_COREVIEW; owner 未签"
authority: "owner direction criterion + clarification 2026-07-29; template wording executor-drafted"
execution_authority: "STAGE2A_WITHHELD"
---

# 研究方向开题报告模板 v1（07-29 判据）

> **owner 澄清（2026-07-29，逐义转录）**：我们定义的是研究内容和方向，类似开题报告。开题报告
> 必须清晰分析三件事：**待开展研究的内容、研究的实验基线、研究的方法调研**。实验基线规则：
> 本域有实验基线的，参考其对应的数据集和评测方法；没有实验基线的，参考视觉多模态领域或文本
> 智能体领域的相关工作，针对性开展自己的实验设计，对比基线可参考相同语音任务和数据集下的
> 表现。研究内容和方法可以参考业内其他工作。
>
> 用途：R2–R9 逐个按本模板产出 co-review 底稿，owner 逐节裁定后该方向才离开
> `OWNER_UNVERIFIED`。模板经 R2 首例校准后由 owner 定稿。文体要求（R1/R2 整改教训）：文献
> 归纳 + 开题分析，不是方法设计书；承重项给 What/Why/How；量词带范围限定词。

## §1 元信息与证据可回溯

ID、主维度、evidence_cut、前版 proposal 路径、本次输入（dossier/registry/ledger 条目枚举）。
所有承重引用必须回溯到本地全文 hash 登记（`2026-07-17-sf-fulltext-ledger.jsonl` 或 registry
jsonl）；裸名引用 = 该节不合格。

## §2 待开展研究的内容

- **研究问题一句话**：在〈具体语音/音频任务〉上，〈杠杆/机制〉能否在等预算下相对〈基线〉带来
  可靠提升。
- **研究内容分解**：列出要研究的子问题（机制、条件、失效模式），每条说明为什么属于本方向
  （与其他 R 的管辖界线显式划清，判据均匀适用、不选择性执法）。
- **明确不研究什么**：因证据边界或 readiness 排除的内容，如实列出。

## §3 研究的方法调研

- **本域已有方法**（speech/omni）：每篇过 DFS 四问——方法 / 局限 / 改进空间 / 可借鉴（找台阶
  不判生死）。
- **业内其他工作**（视觉多模态、文本智能体等）：可参考的研究内容与方法，逐条注明借入什么
  （协议/状态表示/算法/统计量）；效果不跨模态外推（H5 边界）。
- **改进空间 → 候选杠杆**：从四问的局限/改进空间推出；每个杠杆过两道判别：
  read-out/new-info 判别（不引入部署时不存在的信息）、北极星一致性（API-only、reward-guided、
  TFRL 路线）。

## §4 研究的实验基线

按 owner 两型规则归类并落实：

- **(a) 本域有实验基线**：采用该基线对应的**数据集与评测方法**（官方 split、judge/指标口径、
  报告法）；基线数字逐个锚定（系统/配置/数字/出处 hash 可回溯）。分层：须复现的基线（等预算
  对照臂，用项目核心跑通）/ 只引用的参考数字（他核结果不改写为本项目结果）。
- **(b) 本域无实验基线**：引用视觉多模态/文本智能体领域的相关工作作为设计参照，针对性设计
  自己的实验；**对比基线参考相同语音任务和数据集下已有系统的表现**（列出该任务/数据集下
  现有最强公开数字作为锚）。
- **readiness 表**（两型都必填）：数据集本地落盘 / hash / `docs/datasets.lock.json` / license /
  split / 评测依赖（judge 等外部 API）——缺项如实标注，不得以散文代替；不自建、不重标、不补
  快照。
- 多篇参考不可公度时分列报告，不新造统一指标合并。

## §5 实验设计与数字击杀阈值

- 对照臂清单（direct、基线复现臂、random/matched-cost 对照、目标杠杆臂）；等预算约束。
- 报告项：paired delta、下置信界、seed 方差、subgroup、calls/cost；指标复用 §4 确定的口径。
- **数字击杀阈值（必填）**：SESOI、判死条件、降级/重路由去向。数值可标
  `TBD_AT_AUTHORIZATION` 但必须给提案默认值；零数字阈值 = 该节不合格。

## §6 边界与暴露声明

API-only / gold fence / 数据与指标复用边界 / 本次重审 exposure 四字段记账。

## §7 处置建议与 owner 裁定

- 执行者建议（GO_STANDALONE / MERGE / NO_GO）+ 最强反方论证（对抗分析：保留/挑战/备选）。
- owner 裁定栏：结论、日期、Decision-Log 条目号。**本节 owner 落笔前，全文一律 `owner 未签`。**

## 验收清单

1. 承重引用 100% 可回溯本地 hash；2. 研究内容分解有管辖界线论证；3. 方法调研覆盖本域 + 业内
参考两层且各条注明借入内容；4. 基线两型归类落实到数据集+评测方法，数字有出处；5. readiness
表无散文代替；6. 每杠杆过 read-out/new-info 判别；7. 击杀阈值带数字；8. 文体为归纳+开题分析；
9. 量词带 scope；10. exposure 四字段完整。命名纪律：wiki 下非 audit 文件名不得含
review/report/proposal/response 等审计保留 token（surface check 会拦截）。
