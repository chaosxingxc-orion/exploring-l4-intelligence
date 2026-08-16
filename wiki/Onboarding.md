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
   `python scripts/checks/code_graph_check.py`, `python scripts/checks/study_workspace_check.py`
   (`--require-installed` on the primary dev machine),
   `python scripts/checks/legacy_asset_resolution_check.py`,
   `python scripts/checks/ai_context_surface_check.py`,
   `python scripts/checks/build_ai_context_manifest.py --check`.
5. Fetch only authorized assets with `scripts/data/`; models/datasets/outputs live in
   `SPEECHRL_DATA_DIR`, while local MLflow runs stay on ext4.
6. Do not create a study checkout from a candidate. After owner GO plus an execution contract, use the
   semantic URL in `studies/registry.json` and clone that independent repository into `studies/`.
7. Follow the owning repository's README for execution. One study is admitted
   (speech-aware-evidence-acquisition); its model/API execution is bounded by its execution contract
   (E0 data gates plus runtime receipt before any model touch). The retired W1–W4 work repos are cold
   backups, not entry points.

Remote creation, push and Wiki publication require explicit authorization.
