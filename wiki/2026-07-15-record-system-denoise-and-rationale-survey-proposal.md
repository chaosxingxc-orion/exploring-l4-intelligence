---
title: "研发记录系统（文档/记忆/规约）降噪与推理保全——业内调研 + 选型分析 + 最小落地提案"
date: 2026-07-15
status: "PROPOSAL — 三步走第②③步交付物，待 owner 裁决后执行"
origin: "owner 2026-07-15 根因诊断（记忆只记事实不记推理 + 记录冗杂噪音大）与三步走指令；第①步调研 = deep-research 工作流 wf_4fff9a4f-4f7（105 个 Opus 代理 / 23 源 / 108 claims 提取 / 25 claims 每条 3 票对抗核验全过、0 refuted）"
evidence_discipline: "调研结论 = 文献模式级证据（非对本系统的实验）；§1.4 覆盖缺口如实登记；ADR/Zettelkasten 线标 AS_KNOWN_PRACTICE（成熟工程实践，本轮未进 top-25 核验集）"
---

# 研发记录系统降噪与推理保全：调研 + 选型 + 落地提案

> **给读者的一句话**：owner 确诊了本项目两类记录系统失效——①只记事实不记推理（意图丢失→目标
> 置换）；②记录冗杂成噪音（加载即淹没）。本件按三步走交付：业内已验证的解法（§1）→ 结合我们
> 四类承载体的选型（§2）→ 最简单方法先用 + 新仓提案（§3）。

## 0. 一页速览

- **失效①的业内共识解法**：把「推理/反思」作为一等记忆类型单独存储（不是只存结论），配
  provenance 元数据；根因在于默认的压缩/总结机制天然保事实弃推理——「为什么」必须在任何
  总结发生之前写成持久工件。
- **失效②的业内共识解法**：context rot 有实证（内容驱动、非长度驱动，模型会直接放弃）；
  解法 = 永不整库加载 + 按内容修剪（实测最优 = 保最新 + 滚动摘要）+ 打破纯 append-only
  （原位取代 + 写入过滤）；但**全自动遗忘/巩固是未解问题**——修剪必须人工治理、可逆。
- **总架构模式**：append-only 审计层 ⟂ 可改写工作层，物理分离，墓碑指针相连——恰好映射到
  我们的 Decision-Log（审计）与 Research-Objective（工作面），说明方向本来就对，坏在纪律
  没有约束「工作面只装现行真理」和「锁必须带推理」。
- **物理删除 vs 隔离归档的裁定建议**：**移出加载面、不销毁**——git 历史 + archive/ 即
  append-only 层，从工作树移走文件不破坏审计；证据显示全删会反噬（把还需要的内容删了导致
  任务做不完）。
- **最简单先用（§3.1）**：三个纯规约动作（模板升级/记忆库整编/CLAUDE.md 拆分），零代码、
  零基础设施，本周可落。
- **新仓（§3.2）**：umbrella 下新建 meta-research 仓，把「研发记录降噪 + 记忆 + 规约」当
  系统性研究对象；调研遗留的 4 个开放问题 + 我们的并发写问题 = 种子研究议程。

## 1. 第一步：业内调研（25 claims 三票对抗核验，0 refuted）

### 1.1 失效①「只记事实不记推理」——已验证解法

| # | 解法模式 | 证据（票数） | 出处 |
|---|---|---|---|
| R1 | **推理/反思 = 一等记忆类型**：Generative Agents 的 reflection 周期性把原始观察综合成高阶推断并写回记忆流；Reflexion 把「对反馈的语言化自我反思」存入情节缓冲；2026 agent-memory 综述把 reflective self-improvement 列为五大机制族之一（与原始事实存储明确分开） | 3-0 ×3 claims | [Generative Agents](https://arxiv.org/abs/2304.03442) · [Reflexion](https://arxiv.org/abs/2303.11366) · [survey 2603.07670](https://arxiv.org/abs/2603.07670) |
| R2 | **每条记忆带 provenance + 解释性上下文元数据**：MemOS 的 MemCube 封装内容+出处+版本；A-MEM 每条笔记带 LLM 生成的上下文描述/关键词/标签。注意（诚实限定）：二者存的是「来源+解释」，并非完整决策 rationale——元数据补充 R1、不能替代 R1 | 3-0 ×2 | [MemOS](https://arxiv.org/abs/2507.03724) · [A-MEM](https://arxiv.org/abs/2502.12110) |
| R3 | **根因确认：默认压缩机制天然弃推理**——Anthropic compaction 的保留清单 = 架构决定/未解 bug/实现细节，**不含 rationale**；综述警告「每轮压缩静默丢弃低频细节……agent 记住的是消毒后的通用版历史」（第一天的指令到第三轮可能消失）。⇒「为什么」必须在任何总结之前写成持久工件 | 3-0 ×2 | [Anthropic context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) · survey |

### 1.2 失效②「噪音淹没」——实证确认 + 已验证解法

| # | 模式 | 证据（票数） | 出处 |
|---|---|---|---|
| N0 | **context rot 实证为真**：窗口内 token 越多、召回越差；2606.29718（4 个旗舰开源模型 × 3 个 deep-search 基准）显示堆积的上下文使模型**直接放弃或过早给不确定答案**——且退化由**内容**驱动、非物理窗口长度 | 3-0 ×2 | [Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) · [arXiv 2606.29718](https://arxiv.org/pdf/2606.29718) |
| N1 | **永不整库加载**：Generative Agents 只按 recency+importance+relevance 检索子集；Anthropic 长程 harness 结论「compaction 不够」——用启动时读取的结构化工件（progress 文件+git log）承载持久状态；memory tool = agent 自主决定存什么的外置结构化笔记 | 3-0 ×5 | 同上 + [long-running harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) + [cookbook](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools) |
| N2 | **按内容修剪、不按长度截断**：修剪对象选错会反噬——**全删堆积上下文使「放弃率」归零但「做不完率」显著上升**；七种策略实测最优 = **保最新几轮 + 滚动摘要**（keep-latest w/ summary） | 3-0 ×3 | [arXiv 2606.29718](https://arxiv.org/pdf/2606.29718) |
| N3 | **打破纯 append-only**：A-MEM 新记忆触发旧记忆的上下文表示**原位演化取代**（非堆叠）；MemoryBank 按 Ebbinghaus 曲线做时间衰减+重要性强化；综述把「写入路径过滤」「矛盾处理」列为必要工程实践——「逐字存储一切几乎总是错的」 | 3-0 ×3 | [A-MEM](https://arxiv.org/abs/2502.12110) · [MemoryBank](https://arxiv.org/abs/2305.10250) · survey |
| N4 | **治理警示：自动巩固/学习遗忘 = 未解问题**（2026 综述开放挑战清单）⇒ 修剪必须**人工治理、计划性、可逆**（墓碑/归档，绝不硬删审计层），不能信任全自动遗忘器 | 3-0（单综述源，medium） | survey 2603.07670 |

### 1.3 总架构模式（问题 (d) 的答案）

**双层分离**：append-only 审计/事件层（git commit 历史、Generative Agents 记忆流、事件溯源
的 event store）⟂ 可改写的工作真理层，物理分离；**墓碑模式** = 「丢弃可重取的载荷、保留
『发生过』的记录」（Anthropic tool-result clearing 即此）。git 本身就是该模式的正典实例：
append-only 对象库 + 可变工作树。（3-0 ×3 + 1 条 2-1：「审计 vs 工作层」的措辞是分析性
引申，git 的客观结构支持该读法。）

### 1.4 覆盖缺口（如实登记）

- **人类知识管理线（ADR/Zettelkasten/decision journal）薄**：AWS/Microsoft ADR 流程、
  decision journal、Zettelkasten 源已抓取（见源清单）但其 claims 未进 top-25 核验集。ADR 的
  Context/Decision/Rationale/Consequences 结构与 Proposed→Accepted→**Superseded**（已接受
  的 ADR 永不改写、变更走新 ADR 取代）生命周期按 **AS_KNOWN_PRACTICE** 引用——成熟工程
  实践，非本轮核验 claim。
- **域迁移限定**：context-rot 实证来自**单轨迹内**长程搜索 agent，外推到**跨会话**持久记忆
  （wiki/CLAUDE.md）合理但非直接研究——正是新仓可补的实验空白。
- 全部结论为文献模式级证据；无一条是对本系统的实验。

### 1.5 调研遗留的开放问题（新仓种子议程）

1. 巩固节奏与自动化边界：人工治理的整编批次用什么触发器/节奏？多少可安全自动化？
2. 目标置换检测的操作化：「目的链审计」具体长什么样、每会话怎么便宜地算？
3. **多代理并发写**：25 条 claims 无一处理并发会话写共享正典（我们的真实痛点）；
   写入过滤+原位取代+墓碑如何在并发编辑下不丢更新、不产生冲突取代？
4. 加载面预算与逐出规则：默认加载面的目标 token 预算多大才不触发 rot？「已取代细节」
   （该修剪）与「低频承重细节」（必须保留）怎么区分？

## 2. 第二步：结合我们四类承载体的选型分析

### 2.0 现状噪音量化（2026-07-15 实测）

| 承载体 | 现状规模 | 主要失效形态 |
|---|---|---|
| (a) 持久记忆库 memory/ | 32 文件 / 148KB；索引 MEMORY.md 10.2KB **每会话必载** | ①记锁不记为什么；②索引行超密、点时记录永不退役 |
| (b) wiki 热层 | Research-Objective 13.3KB（取代索引 28 行死名词、10 处「勿再引/撤回」）；Thesis 11KB 带层层 supersession 注记 | ②取代注记淤积——「现状真理」里一半在讲什么不是现状 |
| (c) 规约层 | CLAUDE.md 19.8KB **每会话必载**（操作规约+术语表+方法论+历史警示混装）；AGENTS.md 镜像 | ②混装超载；①规约有裁决日期无裁决理由 |
| (d) 审计层 | Decision-Log 185KB / 续44；archive/ 58 件；评审件若干 | ①「续NN」多记裁决少记推理；②虽有 grep-on-demand 纪律但热层仍大量转述它 |

每会话开工前固定加载 (a) 索引 + (c) ≈ 30KB 高密度中文（≳1 万 token）——ZenML 生产案例
把「CLAUDE.md 类偏好文件随增长压垮上下文」列为具名失效，正是我们的形态。

### 2.1 承载体 (a)：持久记忆库

- **失效①方案（采 R1+R2）**：记忆模板升级为强制五字段——**结论**（锁了什么）/
  **推理摘要**（为什么：备选项、取舍逻辑，3–5 句）/ **目的链**（服务于哪个上级目标，链到
  北极星或其子节点）/ **provenance**（源自哪次讨论/续NN/commit）/ **失效条件**（什么情况
  该重审此条）。现有 Why/How-to-apply 保留但 Why 必须是推理不是事实复述。
- **失效②方案（采 N1+N2+N4）**：MEMORY.md 索引设硬预算（≤30 行）；每条记忆标
  stage/review-by；**人工治理的整编批次**（对齐 N4：不自动）——合并重叠（如 WSL 三条
  gotcha）、退役已完结战役的点时运维条目（移 archive 子目录，git 保历史）；目标 32→约 15
  个活跃文件。
- **本次危机的直接教训已按新模板补写**：owner-clarification / three-phase-doctrine /
  memory-root-cause / reviewer-drift-guard 四条均含推理层。

### 2.2 承载体 (b)：wiki 热层正典

- **失效①方案**：热层每条「锁」强制带一句目的链（「为了 X 所以锁 Y」）——目标置换检测靠
  它变成可 diff 的对象（§2.5）。
- **失效②方案（采 N1+N3+墓碑）**：**按 owner 裁决整体重写（重新搞一套）**，不修补：
  Research-Objective v2 只装现行真理；28 行取代索引整体迁出为 archive 的「墓碑索引」文件
  （热层留一行指针）；旧 Thesis/Objective 整文件移入 archive/（git 历史即审计）。热层设
  content-aware 预算（建议 ≤5KB/文件），修剪规则 = 已取代内容出面、低频承重内容（硬约束、
  信息边界这类）保留——对齐 N2「删错会反噬」。
- **时机联动**：热层重写与 system-first 身份签署（v2 评审 Gate S0）**同一动作**完成，避免
  写两遍。

### 2.3 承载体 (c)：规约层（CLAUDE.md / AGENTS.md）

- **失效①方案**：每条规约带一行 why（多数已有裁决日期，补裁决理由）；理由长的链到
  memory/wiki 条目。
- **失效②方案（按功能拆分，采 N1）**：CLAUDE.md 只保**每会话必需**的操作层——环境/命令/
  提交路由/硬约束/**活术语表**；方法论三阶段、术语典故、历史警示、死代号（A-SEL、δ_corr
  警示等）拆到按需检索的独立文档（`docs/` 或 wiki），死代号进 archive「代号对照表」。
  目标 19.8KB→约 8–10KB。AGENTS.md 镜像纪律不变。
- 风险登记：拆分后模型可能漏读按需文档——对策 = 活术语表每词留一行 + 指针，判断性内容
  才外移；此消彼长的实际效果 = 新仓的第一个可测问题（§1.5-4）。

### 2.4 承载体 (d)：审计层（Decision-Log / archive / 评审件）

- **失效①方案（ADR 化，AS_KNOWN_PRACTICE）**：新「续NN」条目采 ADR 骨架——
  **Context**（什么触发）/ **Decision**（裁决）/ **Rationale**（为什么，含否掉的备选）/
  **Consequences**（代价与约束）/ **Supersedes**（取代谁）。已接受条目不改写、变更走新条
  ——与我们 append-only 纪律天然同构。
- **失效②方案**：维持 grep-on-demand 铁律并加严——热层禁止成段转述 Decision-Log（只留
  续NN 指针）；未提交的评审件类工件当日入库（本次 v1/v2 评审件仍 untracked = 违例待纠）。

### 2.5 横切机制：目的链与目标置换审计

北极星→阶段目标→当前锁 三级目的链写进热层；**每次战役收官/评审接受前**跑一次目的一致性
检查（人工 checklist 起步）：逐条活跃锁问「它服务的上级目标还在吗、还对吗」。这次 selector
漂移若有此检查，续34 锁定时就会暴露「ρ 从指标变对象」的置换。自动化版本（diff 工具）留给
新仓研究（§1.5-2）。

### 2.6 「历史信息要不要物理清理」的裁定建议

**移出加载面、不销毁。** 依据：N2（删掉仍需要的内容→任务做不完率上升）+ N4（自动遗忘不可
信→人工可逆）+ 我们的 QRP 更正义务（dated correction 需要审计层存在）+ git 事实（从工作树
移走/改写文件不损失任何历史字节）。具体：被取代文档→archive/（或压缩 tar 出 repo 视野）+
墓碑一行；加载面文件按预算重写；**唯一禁止的是硬删 git 历史**。

### 2.7 承载体补遗：wiki 本体的三分治（owner 07-15 追问「wiki 里的大量数据信息怎么处理」后补）

盘点（07-15 实测）：顶层 99 文件 = 24 常青 + 75 日期件；`survey/` 数据件 2.7MB / 44 文件；
`archive/` 已有 58 件。处理方案按内容类别三分治：

- **常青层（约 20 件保留顶层）**：Thesis / Objective / Per-Work-Status / 协作与环境文档 +
  领域 dossier（W4 双件、Omni-Embed dossier 等休眠工作的参考件保留，按需检索、不入默认加载）。
  热层三件受预算约束（动作 D）。
- **情节层（75 个日期件）**：恢复并机械化「战役收官即归档」（G0 既有规则、实践失守至今积压
  75 件）——**活性判据 = 被正典四件（Research-Objective / Project-Thesis / Per-Work-Status /
  CLAUDE.md）引用**；不被引用且战役已收官的日期件 → `wiki/archive/`（git mv：历史与哈希锚
  零损失——旧 (commit, path) 证据对经 `git show <commit>:<path>` 永远可解析）。**本轮首扫已
  执行**：≤07-10 且不被正典引用的 17 件归档；07-11 之后的留待 Stage-1A 收官扫。
- **数据层（survey/ 台账与回放包）**：**原地不动**——已天然在默认加载面之外，且是证据锚密集
  区（移动虽不破坏旧锚，但无收益不折腾）。纪律 = **数字正典在台账、散文只引行号不复制**
  （既有 CL2 对账口径的推广）。
- **执行节奏**：归档扫描自本轮起并入「战役收官」固定动作（与 wiki-sync 同批）；活性判据
  机械可查（grep 正典四件）。是否脚本化为 P0-R8 式检查项，按 stage-gated 三问先人工跑通
  两轮再定。

## 3. 第三步：最简单的先用 + 新仓提案

### 3.1 立即动作（纯规约，零代码——按 stage-gated 三问自检：本 stage 用、无参数选型、无预建工件）

- **动作 A（模板）**：①记忆五字段模板 ②「续NN」ADR 骨架 ③热层目的链字段——写进规约层
  （CLAUDE.md 精简版 + AI-Collaboration.md），即日生效。
- **动作 B（整编批次一）**：记忆库人工整编 32→约 15 活跃条 + MEMORY.md 硬预算 30 行；
  被整编内容移 memory/archive/ 子目录。
- **动作 C（拆分）**：CLAUDE.md/AGENTS.md 按 §2.3 拆分瘦身。
- **动作 D（联动，待 S0）**：Thesis/Objective v2 全新重写随 system-first 身份签署一并落地。

### 3.2 新仓提案（umbrella 下，与 W1–W4 并列的 meta-research 线）

- **名称候选**（owner 定，遵守收词纪律不造新术语）：`research-record-ops`（主推：研发记录
  工程）/ `agent-memory-hygiene` / `docops-lab`。
- **定位**：把「AI 协作研发过程中的文档噪音、持久记忆、规约」当**系统性研究对象**——不是
  工具仓，是带可测问题的研究仓（可产出方法论论文/开源工件）。
- **章程草案**：研究问题 = §1.5 四个开放问题 + 多代理并发写；可测指标 = 加载面 token 预算、
  rot 行为指标（放弃率/重读率）、检索命中率、目标置换事故数、整编成本；方法 = 先在本项目
  自身上做 A/B（如加载面瘦身前后的会话效率对比——天然有 07-15 前的基线事故记录）；工件 =
  模板、lint/一致性检查脚本、整编流程。
- **边界（防再犯）**：动作 A–C 不等新仓；新仓只承载**研究与工具化**，任何大建设过
  stage-gated 三问。

## 4. 待 owner 裁决

1. §3.1 动作 A/B/C 是否放行（D 已绑定 S0）？
2. 新仓名称与章程（§3.2）？
3. §2.6 归档策略确认：移出加载面不销毁（唯一例外是否允许把超大历史 tar 出 repo）？
4. 热层预算数值（建议：CLAUDE.md ≤10KB、Research-Objective ≤5KB、MEMORY.md ≤30 行）——
  数值本身即新仓第一个待标定参数，先按建议值试运行？
