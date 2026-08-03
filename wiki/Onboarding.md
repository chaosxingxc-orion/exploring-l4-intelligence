# Onboarding

Zero-to-ready for a new collaborator or AI. Assumes Windows + WSL2 `Ubuntu-24.04` with an RTX 5090.

1. Read the client guide (`AGENTS.md` or `CLAUDE.md`), then [[Research-Objective]] and
   [[Project-Thesis]]. For a repository/experiment task, also read [[Experiment-Assets]].
2. Clone the umbrella. Clone only the W1–W4 work repo needed for the task into `projects/`; each is an
   independent repo and is ignored by the umbrella.
3. Run `bash scripts/wsl-setup.sh`, `bash scripts/env-setup.sh`, then
   `source ~/.venvs/speechrl/bin/activate` inside WSL2. Never use native/system Python 3.14 for the ML
   stack and never touch `D:/ai-stack/mem0-venv`.
4. Run `pytest common/tests` and the umbrella gate
   `python scripts/survey/sf_current_package_check.py --check`.
5. Fetch only authorized assets with `scripts/data/`; models/datasets/outputs live in
   `SPEECHRL_DATA_DIR`, while local MLflow runs stay on ext4.
6. Do not create a study checkout from a candidate. After owner GO plus an execution contract, use the
   semantic URL in `studies/registry.json` and clone that independent repository into `studies/`.
7. Follow the owning repository's README for execution. Today there is no admitted study repository and
   no model/API experiment authority; W1 is legacy/component work, not the default first run.

Remote creation, push and Wiki publication require explicit authorization.

---

## 中文

新协作者先读客户端指南、[[Research-Objective]] 和 [[Project-Thesis]]；仓库/实验任务再读
[[Experiment-Assets]]。伞仓负责治理，按任务需要把 W1–W4 克隆到 `projects/`。环境只用 WSL2
`Ubuntu-24.04` 和 `~/.venvs/speechrl`，大型资产只放 `SPEECHRL_DATA_DIR`。

候选方向不能提前克隆/创建 study。只有 owner GO 与执行合同关闭后，才按 `studies/registry.json` 的
语义名称和 URL 克隆独立仓。目前正式 study 登记为 0，也没有模型/API 实验权限；W1 是历史/组件工作，
不是默认首跑入口。未经明确授权不得创建远程仓、push 或发布 Wiki。
