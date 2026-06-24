# Working Mode

How we work across the **five repos** (umbrella + W1–W4). See also [CONTRIBUTING.md](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/blob/master/CONTRIBUTING.md).

**Where each change goes.** This is the rule that trips people up most:

- `common/`, `docs/`, `scripts/`, `wiki/`, root `*.md` → commit to **this umbrella repo**.
- A work's own code/configs/README → commit to **that work's own repo** under `projects/<work>/`
  (they are gitignored by the umbrella, with independent history/issues/remotes).

**Shared-library ripple.** `common/` (`speechrl-common`) is editable-installed by all four works. A
change there affects W1–W4 — run `pytest common/tests` (the lazy-import smoke tests), and keep heavy
imports inside functions so `import speechrl_common` stays cheap.

**Git conventions.** Default branch is **`master`** for all five repos. Branch for non-trivial work,
open a PR, keep commits scoped to one repo. `.gitattributes` forces `eol=lf` (especially `*.sh`) so
scripts run in WSL — keep it. Never commit data: `speechrl-data/` and all weight/dataset/archive
formats are gitignored (~410 GB stays local).

**Config & tracking.** Hydra per work (`config.yaml` composes `model/ dataset/ rl/ experiment/`);
override any key on the CLI (`bash scripts/train.sh rl.learning_rate=2e-6`). Tracking is local MLflow
under `~/speechrl-data/mlruns` — no server, no account.

**Gotchas.** `gh` resolves to `C:\Program Files\GitHub CLI\gh.exe` (ahead of a shadowing Python
script). On Windows Python the `PYTHONPATH` separator is `;` (not `:`) when testing without an install.

**Knowledge & memory.** Record durable decisions/learnings in [[Decision-Log]] and publish via
`scripts/wiki-sync.sh`. AI assistants follow [[AI-Collaboration]].

---

## 中文

我们在**五个仓库**（伞仓 + W1–W4）上的协作方式；另见
[CONTRIBUTING_CN.md](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/blob/master/CONTRIBUTING_CN.md)。

**改谁提交到谁**（最容易踩的点）：`common/`、`docs/`、`scripts/`、`wiki/`、根目录 `*.md` → 提交到
**本伞仓**；某个工作自己的代码/配置/README → 提交到 **`projects/<work>/` 那个工作自己的仓库**（它们被
伞仓 gitignore，有独立历史/issue/remote）。

**共享库波及：** `common/`（`speechrl-common`）被四个工作可编辑安装，改它会影响 W1–W4 —— 跑
`pytest common/tests`，并保持重导入在函数内部，让 `import speechrl_common` 始终廉价。

**Git 约定：** 五仓默认分支都是 **`master`**；非琐碎改动开分支、提 PR，提交只限于单个仓库；
`.gitattributes` 强制 `eol=lf`（尤其 `*.sh`），别动它；绝不提交数据（`speechrl-data/` 及各类权重/
数据集/压缩格式都被忽略）。

**配置与追踪：** 每个工作用 Hydra（`config.yaml` 组合 `model/ dataset/ rl/ experiment/`），命令行可
覆盖任意键；追踪是本地 MLflow（`~/speechrl-data/mlruns`，无服务器/账号）。

**坑：** `gh` 解析到 `C:\Program Files\GitHub CLI\gh.exe`（在一个同名 Python 脚本之前）；Windows
Python 下 `PYTHONPATH` 分隔符是 `;` 不是 `:`。

**知识与记忆：** 把持久的决策/经验记到 [[Decision-Log]]，用 `scripts/wiki-sync.sh` 发布；AI 协作者遵循
[[AI-Collaboration]]。
