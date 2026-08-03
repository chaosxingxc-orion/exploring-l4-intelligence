# Onboarding

Zero-to-ready for a new collaborator or AI. Assumes Windows + WSL2 `Ubuntu-24.04` with an RTX 5090.

1. Read the client guide (`AGENTS.md` or `CLAUDE.md`), then [[Research-Objective]] and
   [[Project-Thesis]]. For a repository/experiment task, also read [[Experiment-Assets]].
2. Clone the umbrella. For an admitted-study task, clone that study's repo (URL in
   `studies/registry.json`) into `studies/<slug>/`; it is an independent repo ignored by the umbrella.
3. Run `bash scripts/wsl-setup.sh`, `bash scripts/env-setup.sh`, then
   `source ~/.venvs/speechrl/bin/activate` inside WSL2. Never use native/system Python 3.14 for the ML
   stack and never touch `D:/ai-stack/mem0-venv`.
4. Run `pytest common/tests` and the umbrella gates:
   `python scripts/checks/code_graph_check.py`, `python scripts/checks/study_workspace_check.py`,
   `python scripts/checks/ai_context_surface_check.py`,
   `python scripts/checks/build_ai_context_manifest.py --check`.
5. Fetch only authorized assets with `scripts/data/`; models/datasets/outputs live in
   `SPEECHRL_DATA_DIR`, while local MLflow runs stay on ext4.
6. Do not create a study checkout from a candidate. After owner GO plus an execution contract, use the
   semantic URL in `studies/registry.json` and clone that independent repository into `studies/`.
7. Follow the owning repository's README for execution. One study is admitted
   (audio-aware-evidence-acquisition); its model/API execution is bounded by its execution contract
   (E0 data gates plus runtime receipt before any model touch). The retired W1–W4 work repos are cold
   backups, not entry points.

Remote creation, push and Wiki publication require explicit authorization.

---

## 中文

新协作者先读客户端指南、[[Research-Objective]] 和 [[Project-Thesis]]；仓库/实验任务再读
[[Experiment-Assets]]。伞仓负责治理与 Stage‑1 调研；获准 study 按 `studies/registry.json` 的 URL
克隆到 `studies/<slug>/`。环境只用 WSL2 `Ubuntu-24.04` 和 `~/.venvs/speechrl`，大型资产只放
`SPEECHRL_DATA_DIR`。

候选方向不能提前克隆/创建 study，只有 owner GO 与执行合同关闭后才建仓。当前获准 study 为
audio-aware-evidence-acquisition，其模型/API 执行受其执行合同约束（先关 E0 数据门+runtime 收据）。
已退役的 W1–W4 是冷备份，不是入口。未经明确授权不得创建远程仓、push 或发布 Wiki。
