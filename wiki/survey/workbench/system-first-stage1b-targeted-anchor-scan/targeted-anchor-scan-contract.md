# Stage-1B 定向锚点扫描合同

## 1. 交易边界

输入是冻结 Stage‑1B v5、CURRENT 参考层、未签名 capability-delta RC1，以及围绕知识、技能、记忆、
multimodal agent system 和 training-free control 的新增检索结果。输出只是一组可审计的 Stage‑1B
论文证据记录。

本交易允许：检索、下载与哈希绑定全文；读取论文实验；记录方法路径、协议、数据/评价器、边界和
反证；将通过门槛的 canonical work 写入独立 registry shard。

本交易不允许：改写 v5；改写 capability-delta RC1；宣布 literature closure；形成 Stage‑1C family
或 branch；运行模型、API、benchmark metric、复现或 prototype；选择研究方向；作项目 novelty verdict。

## 2. 纳入门

候选论文至少满足一项，才进入 24 篇定向增量：

1. 与 speech/omni 的任务、系统或评价协议直接匹配，可能成为后续锚点候选；
2. 会实质改变知识、技能、记忆、系统载体或训练免费控制的 Stage‑1B 方法路径；
3. 提供可以迁移的对照 arm、评价器、预算/停止、主动获取、证据归因或因果拆分协议；
4. 提供足以约束强假设的负结果、边界或替代解释。

“近期”“多模态”“agent”或“分数高”本身不构成纳入理由。论文必须有全文、稳定 canonical ID、
精确 locator 和明确的最强限制。

## 3. 参考、借鉴与复现

| 关系 | Stage‑1B 含义 | 允许继承 | 禁止推断 |
|---|---|---|---|
| `REFERENCE_CONTEXT` | 用论文理解相邻方法、训练边界或失败条件 | 概念、动作空间、限制、反证 | 不把论文方法当作本项目实验 arm，不继承可复现性 |
| `BORROWED_PROTOCOL_ANALOGUE` | 借用实验设计中的决策结构，并明确改变模态、数据、模型或 access | 对照结构、变量、评价维度、kill/falsifier 设计 | 不称复现，不跨域继承分数、结论或资产可用性 |
| `REPRODUCTION_ANCHOR` | 对 task-matched nearest prior 做原样或声明偏差的复现 | 已闭合的数据、代码、模型、评价器与 access 合同 | 未闭合资产、版本或执行前不得登记 |

本批 24 条记录只有前两类，`REPRODUCTION_ANCHOR=0`。字段
`reproduction_candidate_status` 只表示“若以后补齐哪些条件，可能如何使用”，不是复现承诺。

## 4. 能力与系统编码

- `KNOWLEDGE`：进入当前决策的外部事实、证据或感知内容；
- `SKILL`：可复用、可组合的程序或操作策略；
- `MEMORY`：跨步骤/轮次/会话的保存、检索、更新、遗忘与利用；
- `SYSTEM`：承载感知、状态、工具、评价、动作、恢复和交互的系统结构；
- `CONTROL`：基于信号选择候选、动作、预算、停止或修复的策略。

这五项不是互斥研究主题。每篇论文登记一个 `primary_direction` 作为本次纳入的主要干预点，同时用
`intervention_axis` 保留 D0-D4 多标签。知识/技能是内容，记忆是时间与更新机制，系统是载体，控制是
决策原则；这样避免把“存储了技能”同时重复记成技能增益和记忆增益。

MM0-MM3 另行编码：任务含多模态不等于使用了多模态资产；使用多模态资产也不等于证明该模态是
必要因果因素。只有匹配的去模态/换模态对照才能支持 `MM3_CAUSALLY_MULTIMODAL`。

## 5. 论文实验事实合同

- 一条记录必须包含 setting、comparisons、supported facts、source locators 和 strongest boundary；
- 数值只允许留在论文自身的 dataset/model/access/budget stratum 内，不做跨论文聚合；
- 论文采用训练、内部 logits、外部 judge 或 surrogate 时必须显式记录，不能统一包装成 training-free
  black-box control；
- 数据集 lineage 只有在论文提供来源证据时登记；语义相似只允许登记 relation；
- 搜索结果、摘要、代码仓标题或本地文件存在均不能单独支撑实验结论、许可或可复现性。

## 6. 扫描决策

精读 26 篇后，24 篇纳入。两篇未纳入但不删除扫描证据：

- `2606.01414`：position/work-in-progress；其 visual-skill 路径已被同批更完整、对照更清楚的
  VISUALSKILL 覆盖；
- `2601.07470`：DPO 训练的文本 memory copilot；其边界对当前路径没有超出既有 Memory-R1 和同批
  AgeMem 所提供的增量信息。

“未纳入”不表示论文质量低，只表示它没有为本次 Stage‑1B 定向增量提供不可替代的新证据节点。

## 7. 计数与签名门

- 冻结 registry：226；
- CURRENT appendix/priority 去重后的继承并集：282；
- capability-delta RC1：14，未签名，保持独立；
- 本批定向纳入：24，与以上两层均无 canonical 重复；
- 本批独立候选面：`282 + 24 = 306`；
- 两个未签名增量的候选并集：`282 + 14 + 24 = 320`。

只有独立 reviewer 签发 `SIGN_STAGE1B_TARGETED_ANCHOR_SCAN_RELEASE` 后，本批记录才可能成为后续输入；
该签名不自动签署 capability delta，不自动激活 Stage‑1C，也不授予执行权限。
