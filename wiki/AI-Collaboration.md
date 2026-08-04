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
| **HOT** | `AGENTS.md` / `CLAUDE.md`; `wiki/Research-Objective.md`; `wiki/Project-Thesis.md`; `wiki/Per-Work-Status.md`; `wiki/Experiment-Assets.md` | 每个新会话读前三项；Per-Work/实验资产按需 | 仅前三项 | 当前事实，supersede-in-place | owner 裁决、当前阶段、阻塞项、跨工作状态或实验资产权威边界必须立即可见 | 原位替换旧状态并留一个冷索引指针；不得日期版本化或堆限定语 |
| **REGISTRY** | `wiki/survey/registry/`（历史兼容路径 `wiki/survey/sidecars/` 由 manifest 管理） | 做论文核验、编码或写作的人/AI | 否 | 长期 census/claim/证据登记；本体 append-only，判决显式 supersede | 论文 FETCH/精读、canonical ID 或承重 claim 被采用 | 跨 campaign 保留；不得复制进协议散文，失效判决带 token，不删记录 |
| **AUDIT** | 普通 transaction：`wiki/audit/<campaign>/<round-id>/`；带 ordinal 的迭代修正：`wiki/audit/<campaign>/epoch-<N>/<round-id>/`; index=`wiki/audit/<campaign>/INDEX.md` | reviewer、审计者；AI 仅精确取证 | 否 | round 件与 `consolidation-receipt.json` 首个 commit 起 immutable；index append-only | reviewer submission/report/response/sign-off 直接写永久路径并登记；amendment/correction 走 epoch 状态机，唯一无编号例外是 path-pinned B8 correction | 已注册件永不移动/改写；退出活跃路由后仅由 campaign index 访问 |
| **ARCHIVE** | `wiki/archive/<knowledge-layer>/<campaign>/` | 仅历史/复现问题 | 否 | 搬入后 immutable | 未注册工作件已**闭合**（完成、被取代或废弃）且不再有活跃依赖 | 永久冷存；只有新的审计更正能解释其历史含义，不回迁成 current |
| **WORKBENCH** | `wiki/survey/workbench/<campaign>/` | 当前探索者 | 否 | 可变工作知识，不得承载完成声明 | 问题尚在探索、规则未被接受 | 有用结论整编进 HOT/REGISTRY；保留 dossier 归档；无价值 scratch 不提交 |
| **Engineering spec** | `docs/superpowers/specs/` | 实现者与 reviewer | 否 | 有界工程设计，经 Git review 版本化 | 多步骤工程改动需要先锁范围/约束 | 完成后由 Git 历史保留；research current page 不依赖 plan/spec 才能解释 |
| **Engineering plan** | `docs/superpowers/plans/` | 实现者 | 否 | 执行中 checkbox 可变 | 已批准设计需要分解执行 | 完成后停止作为 current research pointer；历史由 Git 保存 |
| **Study repository registry** | `studies/README.md`; `studies/registry.json` | owner、实现者、CI | 否，按工程任务定向 | 伞仓跟踪；只登记已获准的语义命名独立 Git 仓 | 独立研究对象获得 `OWNER_GO_AND_EXECUTION_CONTRACT`，语义名称和执行合同冻结 | 生命周期变化原位更新；候选编号不得成为 repo 名，未获准/已在建仓前日落的候选不得建空仓 |
| **Paper repository registry** | `papers/README.md`; `papers/registry.json` | owner、实现者、CI | 否，按工程任务定向 | 伞仓跟踪；语义命名独立 Git 仓（Stage‑3，续91） | 由合格 study candidate 经 `OWNER_GO_AND_PAPER_EXECUTION_CONTRACT` 晋级 | 生命周期原位更新；候选编号不得成为 repo 名；空 registry 合法、不得建空 paper 仓 |
| **Study experiment index** | `wiki/experiments/<study-slug>/README.md`，总路由=`wiki/Experiment-Assets.md` | owner、实现者、reviewer | 否，按 study 定向 | Wiki 管理实验状态与资产图；记录必须 pin repo commit、协议/配置/数据/模型与产物 | study 已登记，实验合同进入执行 | 结论整编进稳定当前页；release/audit bytes 不回写，study 日落后保留可恢复索引 |
| **Paper experiment index** | `wiki/experiments/papers/<paper-slug>/README.md`（首个 admission 时创建），总路由=`wiki/Experiment-Assets.md` | owner、实现者、reviewer | 否，按 paper 定向 | Wiki 管理 Stage‑3 实验状态与资产图；记录必须 pin paper commit、协议/数据与产物 | paper 已登记，promotion 完成 | 结论整编进稳定当前页；release/audit bytes 不回写 |
| **Check report** | `docs/checks/<campaign>/<release-id>/` | 门禁工具与核验者 | 否 | 被 release 引用后 immutable | 可重复检查产生平台/版本特定结果 | 新 release 新目录；禁止跨平台共用 last-writer-wins 文件名 |
| **Executable rule** | `scripts/` | CI、操作者、reviewer | 否（执行而非通读） | 正常代码生命周期，测试先行 | 散文规则可机械验证时 | 修改规则必须同步测试；散文只指向检查器，不维护第二套实现 |
| **Ephemeral scratch** | **Not committed** | 当前会话 | 否 | 无权威性 | 临时推理、草稿、一次性输出 | 交接前提炼有价值结论并附 provenance；其余删除/过期 |

新文档先按上表归类再创建，不能先扔进 `wiki/` 根目录后等未来清理。现有 path-pinned legacy
文件是兼容例外：保留原路径不等于 active；它们必须在 AI context manifest 的 cold inventory 中。

工程仓与资产字节采用三层权威：`studies/<semantic-slug>/`（Stage‑2）与 `papers/<semantic-slug>/`
（Stage‑3，晋级后）是独立 Git/GitHub 执行仓，umbrella Wiki 是实验生命周期与资产关系的管理权威，
`SPEECHRL_DATA_DIR`/MLflow 保存大数据、权重、原始输出和运行对象。Wiki 必须索引这些字节的 URI/ID/hash，但不得复制大资产。W1–W4 的 `projects/` 仓不自动拥有任何
新 study；稳定且确实跨仓复用的能力才提升到 `common/`。

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

第三份 audit correction 可以保存历史，但**第三次修正必须立即折叠**进 effective spec。修正 ordinal
只在一个 **consolidation epoch** 内计数，合法值只有 1–3；同一 epoch 的**第四次修正禁止新增**，ordinal
4 永不合法。需要继续修正时必须先 Consolidate，然后创建下一个 `epoch-<N>`，ordinal 从 1 重启。

普通 review transaction 仍使用 `wiki/audit/<campaign>/<round-id>/`；唯一允许的无编号 fixed correction
是 path-pinned B8 文件
`wiki/audit/system-first-stage1a/round-12/stage1a-readiness-correction.md`。除此以外，新 amendment/correction
一律使用 `wiki/audit/<campaign>/epoch-<N>/<round-id>/<name>-<ordinal>.md`，并携带 LF-only front matter，
exact schema 为
`schema/campaign/epoch/ordinal/kind/effective_spec/effective_spec_version/effective_spec_sha256`，其中
schema=`ai-context-audit-iteration-v1`，metadata 必须与 path 及本 epoch receipt 完全一致。

每个 epoch 的 `epoch-<N>/consolidation-receipt.json` 是非默认加载、首个 commit 起 immutable 的 AUDIT 件，
exact schema 为 `schema/campaign/epoch/effective_spec/effective_spec_version/effective_spec_sha256`；其中
schema=`ai-context-consolidation-receipt-v1`。Artifact 与 receipt 都必须进入 audit registry、pin Git blob，且
stage-0 blob raw bytes 必须等于可信 worktree bytes。每个 campaign 的 epoch 从 1 连续递增；每个 epoch 的
ordinal 唯一且连续为 1..max，max≤3。最高 epoch receipt 必须绑定 current manifest 中的
`wiki/survey/current/protocol.md`，version 等于其 front matter，sha256 等于其 staged raw bytes。开启新 epoch
前，必须先 commit receipt、append 注册、同步提升 immutable registry prefix count/hash anchor，并通过
不可变性检查；因此新 epoch 存在即证明之前所有 epoch 的 registered receipt 链完整。上一 epoch 可因
其他强制触发器在 ordinal<3 时提前整编。伪造、缺号、重复、
未注册、repin 或 dirty bytes 均 fail closed。整编不是再加一层解释，而是把 CURRENT 原位重写为单一、
完整、无补丁依赖的规范。

任何 audit registry append 都必须与 `scripts/checks/ai_context_inventory.py` 的完整 prefix count/hash
anchor 及新 immutability report 处于同一 transaction；registry/anchor 先 stage，report 生成后再 stage，
然后运行 builder `--check` 与 zero-write 断言。只追加 registry 尾部、留旧 anchor 给下一任务修复是非法状态。

ARCHIVE 搬运在工作件“已被取代且不在 current manifest”时触发；安全时与替代件同一 commit 完成。
不安全时记录明确 closeout blocker，签署前解决，绝不强搬。已注册 AUDIT 是例外：永不搬运，只从
active routing 移除。

自 2026-07-28 起另设 **sunset 通道**（owner 裁决，Decision-Log 续75）：已被取代且无活跃引用的
工作件可从工作树删除以代替搬运，历史字节由 Git 保存。前提与安全门与 ARCHIVE 相同；每个删除
路径必须在当次 campaign 的 sunset ledger 登记 blob 哈希与找回命令，叙事类记录先蒸馏进 sunset
digest；注册 AUDIT 件字节不变，其工作树条目仅当 immutability 检查以 git 历史可达性验证时方可
删除。docs/checks 前公约散件与零引用报告、docs/superpowers/plans 零引用已完成计划适用本通道。

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
