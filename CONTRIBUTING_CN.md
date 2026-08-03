# 贡献指南 · Contributing

> [English](CONTRIBUTING.md) | **中文**

这是**一个伞式治理仓 + 独立工作仓 + 正式研究仓**的工作区。最重要的一条规则是：
**把每个改动提交到它所属的仓库。**

## 仓库类别

- **`exploring-l4-intelligence`**（伞仓，本仓库）—— 负责 `common/`、`docs/`、`scripts/`、`wiki/`、
  `studies/README.md`、`studies/registry.json` 以及根目录 `*.md`。
- **`projects/<work>/`**（W1–W4）—— 各自是**独立的 git 仓库**（被伞仓 gitignore），有独立的历史、
  issue 和 remote。
- **`studies/<semantic-study>/`** —— 每个经 owner 放行的研究对象都是**独立 Git/GitHub 仓**；本地
  位于伞仓工作区下，但被伞仓 gitignore。建仓要求 `OWNER_GO_AND_EXECUTION_CONTRACT`，候选编号不得成为仓名。

## 改动该提交到哪

| 你改了…… | 提交到…… |
|---|---|
| `common/`、`docs/`、`scripts/`、`wiki/`、根 README/CONTRIBUTING | 伞仓 |
| `studies/README.md` 或 `studies/registry.json` | 伞仓 |
| 某工作的代码 / 配置 / `README.md`（在 `projects/<work>/` 下） | 那个工作自己的仓库 |
| 正式 study 的代码 / 配置 / `README.md`（在 `studies/<semantic-study>/` 下） | 那个 study 自己的仓库 |

如果伞仓 `git status` 显示嵌套工程代码，就放错地方了。`projects/` 和 study 子仓都由各自 Git 管理；
`studies/` 中只有 README 和 registry 属于伞仓。候选方向不能提前建空仓：它可能在工程前日落，也可能与
其他候选合并成一个按真实研究对象命名的仓。

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

- 现有伞仓与 W1–W4 默认分支是 **`master`**；正式 study 在自身仓记录分支策略。非琐碎改动开分支、提 PR。
- 每个提交 / PR 只限于单个仓库。
- `.gitattributes` 强制 `eol=lf`（尤其 `*.sh`），让脚本能在 WSL 跑——别动它。
- **绝不提交数据：** `speechrl-data/` 及各类权重/数据集/压缩格式都被 gitignore（≈440 GB 留在本地）。
  用 `scripts/data/` 拉取（见 [docs/data.md](docs/data.md)）。
- `gh` 解析到 `C:\Program Files\GitHub CLI\gh.exe`；Windows Python 下 `PYTHONPATH` 分隔符是 `;`。

## 知识与记忆 · Knowledge & memory

把持久的决策/经验记到 Wiki 的 `wiki/Decision-Log.md`，工作状态变化时更新 `wiki/Per-Work-Status.md`，
再用 `bash scripts/wiki-sync.sh` 发布。另见 Wiki 的
[Working-Mode](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/wiki/Working-Mode) 与
[AI-Collaboration](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/wiki/AI-Collaboration)。

Wiki 管理实验生命周期与资产关系；代码/配置在 study 仓，大型数据、权重和原始输出在
`SPEECHRL_DATA_DIR`，MLflow 保存运行跟踪，Wiki 绑定它们的 ID、位置和哈希。统一入口是
`wiki/Experiment-Assets.md`。
