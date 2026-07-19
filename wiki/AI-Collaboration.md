# AI Collaboration

本页是 AI 与人类协作者的**文档放置、加载、整编与搬运唯一完整规范**。目标是让新会话只读很小的
当前层即可行动，同时让历史证据保持可审计。其他文件只保留短路由，不复制本页整套规则。

## 1. 默认加载与基本原则

默认加载面严格只有三项：客户端指南（`AGENTS.md` 或 `CLAUDE.md`）→
`wiki/Research-Objective.md` → `wiki/Project-Thesis.md`。`wiki/Per-Work-Status.md`、
`wiki/survey/current/` 与机器报告仅在任务需要时定向加载。

- 不整篇读取 `wiki/Decision-Log.md`，也不广泛加载 `wiki/20*.md`、历史 proposal/review/response/
  amendment、`wiki/audit/` 或 `wiki/archive/`；找出处时先走 campaign index，再 `rg` 精确条目。
- 当前真理只能存在于 HOT/CURRENT 的稳定文件。AUDIT 保存发生过什么，ARCHIVE 保存已退出的工作件；
  **不得用补丁链、回应信或 amendment chain 充当 active truth**。
- 数字、哈希与状态以 current manifest、台账或 release-scoped check report 为正典；散文引用正典，
  不手抄一份平行数字。
- 团队知识必须进入仓内文件。个人记忆或临时 AI 推理不是团队正典。

## 2. 文档类型与唯一位置

每个持久文档必须且只能声明一个角色；同一文件不能同时承担“当前有效规范”和“规范如何演变的审计史”。

| 类型 | 必须位置 | 谁读取 | 默认加载 | 权威性/可变性 | 进入条件 | 搬运/退出条件 |
|---|---|---|---|---|---|---|
| **HOT** | `AGENTS.md` / `CLAUDE.md`; `wiki/Research-Objective.md`; `wiki/Project-Thesis.md`; `wiki/Per-Work-Status.md` | 每个新会话读前三项；Per-Work 按需 | 仅前三项 | 当前事实，supersede-in-place | owner 裁决、当前阶段、阻塞项或跨工作状态必须立即可见 | 原位替换旧状态并留一个冷索引指针；不得日期版本化或堆限定语 |
| **CURRENT** | `wiki/survey/current/`（router、effective protocol、status、manifest、`tables/`、`data/`） | 正在执行该 campaign 的人/AI | 否，按任务定向 | 当前有效工作规范；稳定文件名，版本写入内容 | 工作规则被接受为当前可执行合同 | 新版原位取代；旧版若未注册且不再被 manifest 引用则进 ARCHIVE |
| **REGISTRY** | `wiki/survey/registry/`（历史兼容路径 `wiki/survey/sidecars/` 由 manifest 管理） | 做论文核验、编码或写作的人/AI | 否 | 长期 census/claim/证据登记；本体 append-only，判决显式 supersede | 论文 FETCH/精读、canonical ID 或承重 claim 被采用 | 跨 campaign 保留；不得复制进协议散文，失效判决带 token 而非删记录 |
| **AUDIT** | `wiki/audit/<campaign>/<round-id>/`; index=`wiki/audit/<campaign>/INDEX.md` | reviewer、审计者；AI 仅精确取证 | 否 | round 件首个 commit 起 immutable；index append-only | reviewer submission/report/response/correction/sign-off 在产生时直接写永久路径并登记 | 已注册件永不移动/改写；退出活跃路由后仅由 campaign index 访问 |
| **ARCHIVE** | `wiki/archive/<knowledge-layer>/<campaign>/` | 仅历史/复现问题 | 否 | 搬入后 immutable | 未注册工作件已被 CURRENT 取代且不再有活跃依赖 | 永久冷存；只有新的审计更正能解释其历史含义，不回迁成 current |
| **WORKBENCH** | `wiki/survey/workbench/<campaign>/` | 当前探索者 | 否 | 可变工作知识，不得承载完成声明 | 问题尚在探索、规则未被接受 | 有用结论整编进 CURRENT/REGISTRY；保留 dossier 归档；无价值 scratch 不提交 |
| **Engineering spec** | `docs/superpowers/specs/` | 实现者与 reviewer | 否 | 有界工程设计，经 Git review 版本化 | 多步骤工程改动需要先锁范围/约束 | 完成后由 Git 历史保留；research current page 不依赖 plan/spec 才能解释 |
| **Engineering plan** | `docs/superpowers/plans/` | 实现者 | 否 | 执行中 checkbox 可变 | 已批准设计需要分解执行 | 完成后停止作为 current research pointer；历史由 Git 保存 |
| **Check report** | `docs/checks/<campaign>/<release-id>/` | 门禁工具与核验者 | 否 | 被 release 引用后 immutable | 可重复检查产生平台/版本特定结果 | 新 release 新目录；禁止跨平台共用 last-writer-wins 文件名 |
| **Executable rule** | `scripts/` | CI、操作者、reviewer | 否（执行而非通读） | 正常代码生命周期，测试先行 | 散文规则可机械验证时 | 修改规则必须同步测试；散文只指向检查器，不维护第二套实现 |
| **Ephemeral scratch** | **Not committed** | 当前会话 | 否 | 无权威性 | 临时推理、草稿、一次性输出 | 交接前提炼有价值结论并附 provenance；其余删除/过期 |

新文档先按上表归类再创建，不能先扔进 `wiki/` 根目录后等未来清理。现有 path-pinned legacy
文件是兼容例外：保留原路径不等于 active；它们必须在 AI context manifest 的 cold inventory 中。

## 3. 六步生命周期

所有 campaign 使用同一条流水线：

1. **Capture** — 捕获结论、推理摘要、目的链、provenance、失效条件；未稳定内容只在
   Ephemeral scratch，必要时进入新 campaign 的 WORKBENCH。
2. **Classify** — 提交前指定唯一角色、权威来源、读者与退出条件。Reviewer transaction 在此即被
   分类为 AUDIT，不能先建在活跃目录再搬。
3. **Work** — Draft 在 WORKBENCH 演化；已接受的 Effective 规则只在 CURRENT 稳定文件中
   supersede-in-place。当前文件必须自包含，不能依赖 workbench/archive 才能解释。
4. **Consolidate** — 把日志/修正提炼为一个有效规范与短状态，更新 current manifest，并删除 active
   层的重复说法。设计中的 Correction = 新增 AUDIT 更正 + CURRENT 原位修复，绝不改旧 audit bytes。
5. **Release / Audit** — Review freeze、submission、report、response、correction、sign-off 直接进入
   AUDIT 永久路径并登记；检查输出进入独立 Check report 目录。Release 只引用已钉 hash 的输出。
6. **Archive / Expire** — Campaign close 时先提炼、再清 manifest/引用、最后搬运合格工作件；无价值
   scratch 过期不提交。Next campaign 使用新 WORKBENCH/AUDIT namespace，不复用旧文件名。

对应旧称谓：Draft→Work，Effective→Consolidate 后的 CURRENT，Review freeze→Release / Audit，
Correction→AUDIT 新记录加 CURRENT 原位修复，Campaign close→Archive / Expire，Next campaign→
新一轮 Capture。这个映射不改变 audit immutability。

## 4. 强制整编与搬运时点

以下任一事件先发生就立即 Consolidate：

- 将出现**第三次 amendment 或 correction**；
- protocol、router 或 HOT 文件**超过 context budget**；
- reviewer Gate MAJOR 关闭，或 **reviewer Gate MAJOR 改变 executable contract**；
- **handoff ambiguity**：只读 current protocol + status 仍无法确定下一动作；
- 到达 **stage/release boundary**、campaign verdict、sign-off request 或 publication release；
- 存在 **competing active claims**：两个 active 文件对同一当前字段给出竞争说法。

第三份 audit correction 可以保存历史，但**第三次修正必须立即折叠**进 effective spec；在 Consolidate
完成前，**第四次修正禁止新增**。整编不是再加一层解释，而是把 CURRENT 原位重写为单一、完整、
无补丁依赖的规范。

ARCHIVE 搬运在工作件“已被取代且不在 current manifest”时触发；安全时与替代件同一 commit 完成。
不安全时记录明确 closeout blocker，签署前解决，绝不强搬。已注册 AUDIT 是例外：永不搬运，只从
active routing 移除。

### 搬运前安全门（强制）

1. 从 **stage-0** Git index 读取 regular-file path、mode 与 Git blob；worktree bytes 必须等于该 blob，
   禁止对脏文件或未绑定快照做搬运判断。
2. 源路径不得在 **audit registry** 或 **current manifest**；注册 AUDIT 永不移动。
3. 对 stage-0 图检查所有 HOT/CURRENT 与已注册 AUDIT 的 **inbound reference**，并确认 active script
   无旧路径依赖；引用、plain text、相对/根路径、编码变体都纳入检查。
4. 先更新所有 live pointer 与 manifest/hash，保存 source/destination/mode/Git blob 的确定性计划；
   只接受“全在源端”或“全在目标端”，partial/both-path 状态 fail closed。
5. 使用 `git mv`，不得为加 archive banner 改内容。搬后证明 source absent、destination present、
   mode/blob 相同，且无 active old-path reference。

## 5. 记录、哈希与发布

- 持久知识五字段：**结论 / 推理摘要 / 目的链 / Provenance / 失效条件**。写不出目的链是停止信号；
  只记结论不记为什么不合格。
- Decision Log 新条目使用 ADR：Context / Decision / Rationale / Consequences / Supersedes。旧条目
  append-only；变更写新 ADR。
- 热层的每个承重状态都说明“为了哪个上级目标所以锁什么”。会话结束前，目的层结论、承重中间
  结论与未完成意图必须落盘到正确层。
- 证据哈希以 `(commit, sha256)` 的 **git blob bytes** 为正典；工作树 CRLF 只是一种变体。
- 发布前完成敌意内审、目的链检查、context/manifest/check gates 与 archive scan。Wiki 真源是仓内
  `wiki/*.md`；`scripts/wiki-sync.sh` 只在明确授权后发布，网页版只是镜像。
