# AI Collaboration

How AI assistants (Claude Code, Codex, …) and humans stay on **one consistent understanding** of this
project. The goal: an AI picking up the repo cold should reach the same mental model a teammate has.

**The knowledge layering.**

1. **Root README** (`README.md` / `README_CN.md`) — canonical onboarding; read first.
1.5. **[[Project-Thesis]]** — the canonical statement of the project's purpose, the three core terms,
   and the flagship claim. The "why" behind every work; read right after the README. For the flagship,
   [[W4-Training-Free-RL-Feasibility]] is the *math* and [[W4-Research-Plan]] is the *plan*.
2. **`CLAUDE.md` / `AGENTS.md`** — per-tool operating guides (commands, gotchas, discipline). Kept
   byte-for-byte equivalent so Claude Code and Codex behave the same.
3. **This Wiki** (source in `wiki/`) — **shared, durable, team-visible memory.** Decisions, status,
   conventions, learnings. Edited as normal files, published with `scripts/wiki-sync.sh`.
4. **mem0 MCP** — **local, personal** scratch memory for one user's tooling. Never a substitute for
   the Wiki; anything the team needs must be promoted to the Wiki.

**Protocol for AI assistants.**

- **Before starting:** read [[Research-Objective]] FIRST (the single hot current-state entry), then
  [[Project-Thesis]]; [[Decision-Log]] is the cold audit layer — **grep a single 续NN entry only**,
  never read it whole. Skim [[Working-Mode]] and the relevant work's README as needed.
- **While working:** follow [[Working-Mode]] — commit changes to the *correct* repo (umbrella vs a
  `projects/<work>` repo), preserve lazy-import discipline, keep data out of git.
- **After a decision or learning:** append a dated **ADR-shaped** entry to [[Decision-Log]] (see
  §记录规约 below), reflect the delta into [[Research-Objective]] (and [[Per-Work-Status]] if a
  work's maturity/plan changed), run the archive sweep (战役收官即归档), then
  `bash scripts/wiki-sync.sh` to publish.
- **Source of truth:** edit `wiki/*.md` in the repo, never only the web Wiki — the web copy is a
  mirror that `wiki-sync.sh` overwrites.

**Why this works.** Per-tool files (CLAUDE.md/AGENTS.md) keep each AI runnable; the Wiki keeps all
humans and all their AIs reading from the same evolving memory instead of re-deriving context or
drifting apart.

---

## 中文

让 AI 协作者（Claude Code、Codex……）和人对本项目保持**一致理解**的方式。目标：一个冷启动接手仓库的 AI
应当得到和团队成员一样的心智模型。

**知识分层：**（1）根 README（`README.md` / `README_CN.md`）——权威上手，先读。（2）`CLAUDE.md` /
`AGENTS.md`——逐工具操作手册（命令、坑、纪律），两者保持逐字节一致，让 Claude Code 与 Codex 行为相同。
（3）本 Wiki（源在 `wiki/`）——**团队共享、持久、可见的记忆**：决策、状态、约定、经验；当普通文件编辑，
用 `scripts/wiki-sync.sh` 发布。（4）mem0 MCP——**本地、个人**的临时记忆，不能替代 Wiki；团队需要的东西
必须升级进 Wiki。

**AI 协作协议：** 开工前读 [[Project-Thesis]]、[[Home]] 和 [[Per-Work-Status]]，浏览 [[Working-Mode]] 与对应工作的 README；
工作中遵循 [[Working-Mode]]（把改动提交到**正确**的仓库——伞仓还是 `projects/<work>`，保持惰性导入纪律，
数据不进 git）；产生决策/经验后，在 [[Decision-Log]] 追加带日期的条目（成熟度/计划变了就更新
[[Per-Work-Status]]），再 `bash scripts/wiki-sync.sh` 发布；**真源**是仓库里的 `wiki/*.md`，不要只改网页版
（网页是镜像，会被 `wiki-sync.sh` 覆盖）。

**为什么有效：** 逐工具文件让每个 AI 都能跑；Wiki 让所有人和他们的 AI 都从同一份不断演进的记忆出发，
而不是各自重建上下文、逐渐走偏。

---

## 记录规约（2026-07-15 整改动作 A：三模板 + 分层规则）

**为什么有这一节**：2026-07-15 owner 确诊两类记录失效——①只记事实结论不记推理（跨会话意图
丢失 → 目标置换无从察觉，selector 漂移事故的根因）；②append-only 堆叠成噪音（加载即淹没）。
业内调研与选型分析：`wiki/2026-07-15-record-system-denoise-and-rationale-survey-proposal.md`
（25 条 claim 三票对抗核验；核心依据：推理必须作为一等记忆类型在任何压缩之前落盘；context
rot 实证为真；自动遗忘不可信——修剪必须人工治理、可逆）。

### 模板一：持久记忆五字段（Claude 侧 memory/*.md 及同类个人记忆）

1. **结论**（锁了什么/学到什么）；2. **推理摘要**（为什么：当时的备选项与取舍逻辑，3–5 句）；
3. **目的链**（服务于哪个上级目标——链到北极星或阶段目标；写不出目的链 = 写入时的红旗）；
4. **Provenance**（源自哪次讨论/续NN/commit）；5. **失效条件**（什么情况须重审本条）。

### 模板二：Decision-Log「续NN」ADR 骨架

**Context**（什么触发了这个决定）/ **Decision**（裁决内容）/ **Rationale**（为什么——含
被否掉的备选与否掉理由）/ **Consequences**（代价、新约束、影响面）/ **Supersedes**（取代
哪条旧决定，无则写 none）。已接受条目**不改写**，变更走新条目——与 append-only 纪律同构。

### 模板三：热层目的链

[[Research-Objective]] 每条「锁」带一句目的链（「为了 X 所以锁 Y」）；**每次战役收官/评审
接受前跑目的一致性检查**：逐条活跃锁问「它服务的上级目标还在吗、还对吗」——目标置换靠这个
机制变成可检出事件。

### 分层与归档规则

- **工作层**（热层三件 / CLAUDE.md / 记忆索引）：supersede-in-place（原位改写 + 一行墓碑
  指针），**禁止限定语堆叠**；加载面预算（试运行）：CLAUDE.md ≤10KB、Research-Objective
  ≤5KB、记忆索引 ≤30 行。
- **审计层**（Decision-Log / wiki/archive/ / 历史评审件）：append-only，绝不进默认加载面；
  日期件当日提交入库。
- **数据层**（wiki/survey/ 台账与回放包）：按需检索；数字正典在台账，散文只引行号不复制。
- **战役收官即归档**：不被正典四件（Research-Objective / Project-Thesis / Per-Work-Status /
  CLAUDE.md）引用的日期件 → `wiki/archive/`（git mv；旧 (commit, path) 证据锚经
  `git show <commit>:<path>` 永远可解析，归档零损失）。
- **整编批次**：人工治理、计划性、可逆——绝不自动垃圾回收正典记录。

## 知识四层与晋升管线（2026-07-15 owner 裁决，续47；上文三模板归入下表继续有效）

**四层定义与读写协议：**

| 层 | 内容 | 读 | 写/改 | 保鲜 |
|---|---|---|---|---|
| **事实层** | 锚定工作空间的基础事实（目的/架构/身份/规约）= 默认加载面（CLAUDE.md + Research-Objective + Project-Thesis + S0/合同） | **每会话第一步** | owner 裁决/签署后 supersede-in-place | 事件驱动（裁决/签署即改） |
| **工作知识** | 双态：**日志**（续NN/日期件——按时间、审计用）+ **提炼条**（memory 五字段/常青页——按主题、行动用） | 日志 grep 按需；提炼条按索引 | 日志 append-only；提炼条 in-place | 失效条件 + 整编批次 + 用即改 |
| **探索知识** | 论文库：census（canonical ID+版本钉）+ claim-ledger（claim×work×span+五级证据等级）+ SOTA cards | survey/写作时检索 | **本体只增**；判决层可修订（带伴随 token） | 论文不腐；会腐的是判决——判决带 token 重估 |
| **程序知识** | 脚本/校验器/模板/checklist/runbook（`scripts/**`、三模板、敌意内审环、wsl-ops 类 runbook、ars 工具） | **调用/执行**，非阅读 | 改代码即改；**规约优先做成可执行检查**（散文规约拦不住的，机器门拦得住——P0-R8 经验） | **可测性**——坏了显形；复跑即体检 |

**知识 vs 日志判别**：三个月后一个不在场的新会话要用它，是「grep 出处」（日志）还是「直接照着
做」（知识）？同一事件**双写**：日志行入审计层，知识条入提炼层。

**L2 提炼步**（挂「战役收官」钩子，先于归档扫描）：从本战役日志提出 0–N 条知识条目，每条过
三问——①不在场的人能直接照着做吗？②目的链写得出吗？③与既有条目重复吗（重复则并入不新增）。
敌意内审环带此三问。**提炼是压缩理解，不是压缩文本**（owner 2026-07-13）。

**L3 登记规约（从严，owner 2026-07-15）**：**凡 FETCH/精读过的论文必须按 census/ledger schema
登记（canonical ID、版本钉、承重 claim+span、证据等级）——不登记不算读过。** 与 survey 并行
执行（每篇随手 2–5 分钟，不阻塞主流程）；存量 census v2（95 works）+ ledger v2（62 行）= 库的
种子；人读标记/核验缓存用 ars 工具（`/ars-mark-read` 等）。库入口：`wiki/survey/README.md`。
嵌入检索/LLMWiki 编译 = 库到规模且检索痛点真实后再议（轻路径，尊重续37 四门）。

**晋升管线**：日志 →（提炼步）→ 工作知识 →（选拔判据：**反复被用 + 已稳定 + 足够小**）→
事实层锚点；探索知识的判决 → 事实层。降级同理：事实层条目失去承重 → 墓碑。

**会话逃逸协议**：会话（工作记忆）结束/清空前必落盘——①目的层/北极星层讨论结论（当天入
memory/日志）；②承重中间结论（入日志）；③未完成意图（入 Research-Objective open items 或票）。
**没落盘的讨论 = 不存在**（2026-07-15 /clear 遗忘事故的教训）。

**负清单（刻意不采纳的主流做法）**：自动遗忘/自动 consolidation（未解问题——人工可逆整编）；
嵌入检索先行（续37）；参数化记忆（记录系统与研究主线同为 training-free：改进只发生在外部结构）。
