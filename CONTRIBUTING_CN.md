# 贡献指南 · Contributing

> [English](CONTRIBUTING.md) | **中文**

这是**一个伞仓 + 四个独立工作仓库**。最重要的一条规则是：**把每个改动提交到它所属的仓库。**

## 五个仓库

- **`exploring-l4-intelligence`**（伞仓，本仓库）—— 负责 `common/`、`docs/`、`scripts/`、`wiki/`
  以及根目录 `*.md`。
- **`projects/<work>/`**（W1–W4）—— 各自是**独立的 git 仓库**（被伞仓 gitignore），有独立的历史、
  issue 和 remote。

## 改动该提交到哪

| 你改了…… | 提交到…… |
|---|---|
| `common/`、`docs/`、`scripts/`、`wiki/`、根 README/CONTRIBUTING | 伞仓 |
| 某工作的代码 / 配置 / `README.md`（在 `projects/<work>/` 下） | 那个工作自己的仓库 |

如果在伞仓里 `git status` 看到 `projects/` 下的文件，那就放错地方了——它们属于工作仓库。（`projects/*/`
在这里被 gitignore，正是为了防止这种情况。）

## 共享库 · `common/`

`speechrl-common` 被四个工作可编辑安装，改它会波及 W1–W4。

- 提交前跑 `pytest common/tests`——smoke 测试必须通过。
- **保持惰性导入纪律：** 把 torch/transformers/librosa/mlflow/jiwer 的导入留在**函数内部**，让
  `import speechrl_common` 始终廉价、重栈装好前 smoke 测试也能过。
- 跑单个测试，如 `pytest common/tests/test_smoke.py::test_reward_normalization_exact_match -q`。

## 环境 · Environment

所有训练都在 **WSL2** 里跑（见 [docs/setup.md](docs/setup.md)）。用共享的 py3.12 venv
（`~/.venvs/speechrl`）。别用系统 Python 3.14 跑该栈；**绝不动 `D:/ai-stack/mem0-venv`**。

## Git 约定

- 五个仓库默认分支都是 **`master`**；非琐碎改动开分支、提 PR。
- 每个提交 / PR 只限于单个仓库。
- `.gitattributes` 强制 `eol=lf`（尤其 `*.sh`），让脚本能在 WSL 跑——别动它。
- **绝不提交数据：** `speechrl-data/` 及各类权重/数据集/压缩格式都被 gitignore（≈410 GB 留在本地）。
  用 `scripts/data/` 拉取（见 [docs/data.md](docs/data.md)）。
- `gh` 解析到 `C:\Program Files\GitHub CLI\gh.exe`；Windows Python 下 `PYTHONPATH` 分隔符是 `;`。

## 知识与记忆 · Knowledge & memory

把持久的决策/经验记到 Wiki 的 `wiki/Decision-Log.md`，工作状态变化时更新 `wiki/Per-Work-Status.md`，
再用 `bash scripts/wiki-sync.sh` 发布。另见 Wiki 的
[Working-Mode](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/wiki/Working-Mode) 与
[AI-Collaboration](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/wiki/AI-Collaboration)。
