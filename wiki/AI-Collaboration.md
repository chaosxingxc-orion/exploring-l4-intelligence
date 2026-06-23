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

- **Before starting:** read [[Project-Thesis]], [[Home]] and [[Per-Work-Status]]; skim [[Working-Mode]]
  and the relevant work's README.
- **While working:** follow [[Working-Mode]] — commit changes to the *correct* repo (umbrella vs a
  `projects/<work>` repo), preserve lazy-import discipline, keep data out of git.
- **After a decision or learning:** append a dated entry to [[Decision-Log]] (and update
  [[Per-Work-Status]] if maturity/plan changed), then run `bash scripts/wiki-sync.sh` to publish.
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
