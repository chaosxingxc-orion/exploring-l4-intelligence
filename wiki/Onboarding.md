# Onboarding

Zero-to-first-run for a new collaborator (or their AI). Assumes Windows + WSL2 with an RTX 5090.

1. **Read** the root [README](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/blob/master/README.md),
   then [[Architecture]] and [[Working-Mode]] here.
2. **Clone** the umbrella, then clone the four work repos into `projects/` (each is a separate repo;
   they're gitignored by the umbrella):
   ```bash
   git clone https://github.com/chaosxingxc-orion/exploring-l4-intelligence.git
   cd exploring-l4-intelligence/projects
   for w in training-free-rl efficient-rl-alignment multitask-rl omni-embedding-rl; do
     git clone https://github.com/chaosxingxc-orion/speech-mllm-$w.git
   done
   ```
3. **Set up the environment** (in WSL2): `bash scripts/wsl-setup.sh` → `bash scripts/env-setup.sh` →
   `source ~/.venvs/speechrl/bin/activate`. Details + pitfalls: [[Environment-and-Setup]].
4. **Sanity check:** `pytest common/tests` (passes before the heavy stack is installed) and
   `python -c "import torch; print(torch.cuda.get_device_name(0))"`.
5. **Get data** (only what you need): `bash scripts/data/probe-access.sh` →
   `bash scripts/data/fetch-data.sh`. See [[Data-and-Assets]].
6. **First run — start with W1** (the mature reference): `cd projects/speech-mllm-training-free-rl &&
   uv pip install -e ../../common -e . && bash scripts/train.sh`. Watch it in MLflow
   (`bash scripts/mlflow-ui.sh`).
7. **If you're an AI assistant:** also read [[AI-Collaboration]] and check [[Per-Work-Status]] before
   touching a work.

---

## 中文

新协作者（或其 AI）从零到第一次跑通。前提：Windows + WSL2 + RTX 5090。

（1）**读**根 [README](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/blob/master/README.md)，
再读本 Wiki 的 [[Architecture]] 和 [[Working-Mode]]。（2）**克隆**伞仓，再把四个工作仓库克隆进
`projects/`（各自独立仓库，被伞仓 gitignore）——命令见上。（3）**搭环境**（WSL2 里）：
`wsl-setup.sh` → `env-setup.sh` → `source` 激活；细节与坑见 [[Environment-and-Setup]]。（4）**自检：**
`pytest common/tests`（重栈装好前也能过）与 `python -c "import torch; ..."`。（5）**取数据**（按需）：
`probe-access.sh` → `fetch-data.sh`，见 [[Data-and-Assets]]。（6）**第一次跑——从 W1 开始**（成熟参考）：
`cd projects/speech-mllm-training-free-rl && uv pip install -e ../../common -e . && bash scripts/train.sh`，
用 MLflow 看（`mlflow-ui.sh`）。（7）**若你是 AI 协作者：** 动任何工作前再读 [[AI-Collaboration]] 并查
[[Per-Work-Status]]。
