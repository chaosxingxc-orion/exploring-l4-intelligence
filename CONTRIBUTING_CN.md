# 贡献指南 · Contributing

> [English](CONTRIBUTING.md) | **中文**

这是**一个伞式治理仓 + 若干独立的获准 study 仓**的工作区。最重要的一条规则是：
**把每个改动提交到它所属的仓库。**

## 仓库类别

- **`exploring-l4-intelligence`**（伞仓，本仓库）—— 负责 `common/`、`docs/`、`scripts/`、`wiki/`、
  `studies/README.md`、`studies/registry.json` 以及根目录 `*.md`。
- **`studies/<semantic-study>/`** —— 每个经 owner 放行的研究对象都是**独立 Git/GitHub 仓**；本地
  位于伞仓工作区下，但被伞仓 gitignore。建仓要求 `OWNER_GO_AND_EXECUTION_CONTRACT`，候选编号
  不得成为仓名。

历史 W1–W4 工作仓已于 2026-08-03 退役（本地删除、远端冷备份；墓碑：
`wiki/archive/program/w1-w4-retirement/`）。

## 改动该提交到哪

| 你改了…… | 提交到…… |
|---|---|
| `common/`、`docs/`、`scripts/`、`wiki/`、根 README/CONTRIBUTING | 伞仓 |
| `studies/README.md` 或 `studies/registry.json` | 伞仓 |
| 获准 study 的代码 / 配置 / `README.md`（在 `studies/<semantic-study>/` 下） | 那个 study 自己的仓库 |

如果伞仓 `git status` 显示 study checkout 下的代码，就放错地方了；该容器被伞仓 gitignore，
`studies/` 中只有 README 和 registry 属于伞仓。候选方向不能提前建空仓：它可能在工程前日落，
也可能与其他候选合并成一个按真实研究对象命名的仓。

## 运行节奏

每个新研究课题的 Stage‑1（详细讨论、调研、论证）在伞仓完成；进入 Stage‑2 时开独立 study 仓，
之后的全部工作在该仓完成。伞仓长期保留数据与模型下载职能（`docs/datasets.lock.json` +
`scripts/data/`，公共资产）。数据集是不变的 gold truth；切分/采样/prompt/协议是各 study 的
私有方案，随论文发表的切分结晶为新数据集晋升回伞仓。

## 共享库 · `common/`

`speechrl-common` 被各获准 study 可编辑安装，改它会波及所有 study。

- 提交前跑 `pytest common/tests`——smoke 测试必须通过。
- **保持惰性导入纪律：** 把 torch/transformers/librosa/mlflow/jiwer 的导入留在**函数内部**，让
  `import speechrl_common` 始终廉价。
- 通用实现须有至少两个真实消费者才提升进 `common/`。

## 环境 · Environment

计算在 **WSL2 Ubuntu-24.04**（见 [docs/setup.md](docs/setup.md)），共享 py3.12 venv
（`~/.venvs/speechrl`）。别用系统 Python 3.14 跑 ML 栈；**绝不动 `D:/ai-stack/mem0-venv`**。

## Git 约定

- 伞仓默认分支 **`master`**；获准 study 在自身仓记录分支策略。非琐碎改动开分支、提 PR。
- 每个提交 / PR 只限于单个仓库。
- `.gitattributes` 强制 `eol=lf`（尤其 `*.sh`）——别动它。
- **绝不提交数据：** `speechrl-data/` 及权重/数据集/压缩格式全部 gitignore。用 `scripts/data/`
  按锁拉取（见 [docs/data.md](docs/data.md)）。
- `gh` 解析到 `C:\Program Files\GitHub CLI\gh.exe`；Windows Python 下 `PYTHONPATH` 分隔符是 `;`。

## 文档路由与知识记录

新建文件前先定角色：完整放置表与生命周期以 `wiki/AI-Collaboration.md` 为正典，
[CONTRIBUTING.md](CONTRIBUTING.md) 的 Documentation routing 表是路由摘要。持久决策连同理由写
`wiki/Decision-Log.md`；提交前跑相关门禁
（`python scripts/survey/sf_current_package_check.py --check` 等）。web wiki 只是镜像，
`scripts/wiki-sync.sh` 仅在获授权时发布。

Wiki 管理实验生命周期与资产关系；代码/配置在 study 仓，大型数据、权重和原始输出在
`SPEECHRL_DATA_DIR`，MLflow 保存运行跟踪，Wiki 绑定它们的 ID、位置和哈希。统一入口是
`wiki/Experiment-Assets.md`。
