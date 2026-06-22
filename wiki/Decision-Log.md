# Decision Log

> Append-only, lightweight ADRs — the team's durable **memory**. Newest on top. One entry per
> decision: date · what we decided · why · consequences. Humans and AIs both append here (see
> [[AI-Collaboration]]), then publish with `scripts/wiki-sync.sh`.

---

### 2026-06-22 · Establish the README + Wiki knowledge base
**Decision.** Make the root README the single canonical onboarding doc (English `README.md` + 中文
`README_CN.md`), and stand up this Wiki (sourced from `wiki/`, synced by `scripts/wiki-sync.sh`) as
shared team memory. Sync `CLAUDE.md`/`AGENTS.md` to point here.
**Why.** Knowledge was scattered across per-tool files and people's heads; humans and their AIs need
one consistent understanding.
**Consequences.** Edit wiki content in `wiki/`, not the web Wiki; record notable decisions here.

### (template) · <short title>
**Decision.** …  **Why.** …  **Consequences.** …

---

## Seed decisions (context already baked into the repo)

- **WSL2-only compute.** RTX 5090 (Blackwell sm_120) lacks stable native-Windows torch wheels;
  verl/vLLM/flash-attn are Linux-only. All training runs in WSL2.
- **Python pinned to 3.12.** System Python 3.14 is too new for ML wheels.
- **Four separate work repos under one umbrella.** Independent history/issues per work, shared code
  via editable `common/`. Keeps each paper's repo publishable on its own.
- **Data never in git.** ~281 GB lives in `speechrl-data/` (WSL ext4); `.gitignore` guards it.
- **verl for RL; Qwen2-Audio as default base** (swappable via `models/` + config).
- **W1 first.** Training-free RL is the most mature work and the reference pattern for W2–W4.

---

## 中文

> 追加式的轻量 ADR——团队的持久**记忆**。最新在最上。每条：日期 · 决定了什么 · 为什么 · 影响。人和 AI
> 都往这里追加（见 [[AI-Collaboration]]），再用 `scripts/wiki-sync.sh` 发布。

**条目格式：** 日期 · 标题；**决定**……**为什么**……**影响**……（英文区已有 2026-06-22 的首条与模板）。

**已固化在仓库里的初始决策：** 仅用 WSL2 算力（RTX 5090 无稳定原生 Windows torch；verl/vLLM 仅 Linux）；
Python 锁 3.12（系统 3.14 太新）；一个伞仓下四个独立工作仓库（各自历史/issue，靠可编辑 `common/` 共享
代码）；数据绝不进 git（≈281 GB 在 `speechrl-data/`，`.gitignore` 兜底）；RL 用 verl、基座默认
Qwen2-Audio（可换）；**先做 W1**（免训练 RL 最成熟，是 W2–W4 的参考范式）。
