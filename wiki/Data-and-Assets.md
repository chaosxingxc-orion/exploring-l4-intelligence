# Data & Assets

Model weights and datasets (~650 GB) are **deliberately out of git** — GitHub holds only code, docs,
and download scripts. The dataset set is **FROZEN** to the local snapshot recorded in
[`docs/datasets.lock.json`](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/blob/master/docs/datasets.lock.json)
(28 datasets + 5 models, with pinned revisions) — we no longer download new datasets. The
human-readable asset list is the repo's
[`docs/data.md`](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/blob/master/docs/data.md).

**Where it lives.** `speechrl-data/` on the **E: drive** —
`/mnt/e/chao_workspace/exploring-l4-intelligence/speechrl-data` from WSL (moved off D: on 2026-07-09;
the repo/code stays on D:). Reached via `${SPEECHRL_DATA_DIR:-<repo>/speechrl-data}`, with
`SPEECHRL_DATA_DIR` persisted in the WSL `~/.bashrc` to the E: path (the repo-relative fallback no
longer holds data); ext4 `~/speechrl-data/` holds only the MLflow store. Layout:
`models/`, `datasets/`, `repos/`, `manifests/`, `checkpoints/`, `mlruns/`, `hf-cache/`.

**Fetch / audit.** One unified, lockfile-driven downloader reproduces the exact set — every team runs
the same command and gets identical data (HF assets pinned to the recorded commit):

```bash
bash scripts/data/fetch-data.sh --list   # show the manifest (datasets.lock.json), fetch nothing
bash scripts/data/fetch-data.sh          # fetch everything missing (skips complete; pinned revisions)
bash scripts/data/inventory.sh           # COMPLETE / PARTIAL / MISSING per locked asset
```

**Dependencies.** Needs the speechrl venv (`hf` + `modelscope` CLIs) and `aria2c`. If missing, the
downloader says so and points to `bash scripts/env-setup.sh` (full stack) or
`bash scripts/data/fetch-data.sh --install-deps` (lightweight download deps only). Mirrors default to
hf-mirror.com + ModelScope. The old `wave0_fetch.sh` engine and one-off fetch scripts were retired —
everything is unified in `fetch-data.sh`. Full tables + env knobs: `docs/data.md`.

---

## 中文

模型权重与数据集（≈650 GB）**有意不进 git**——GitHub 只放代码、文档和下载脚本。权威的资产清单（每个
模型与数据集、来源、镜像、环境变量）是仓库的
[`docs/data.md`](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/blob/master/docs/data.md)。

**放在哪：** `speechrl-data/` 现在在 **E 盘**——WSL 侧 `/mnt/e/chao_workspace/exploring-l4-intelligence/speechrl-data`（2026-07-09 从 D 盘迁出；仓库代码仍在 D 盘）。
按 `${SPEECHRL_DATA_DIR:-<repo>/speechrl-data}` 解析，且已在 WSL `~/.bashrc` 中把 `SPEECHRL_DATA_DIR` 固化为该 E 盘路径（仓库根的回退默认已不再存放数据）；ext4 `~/speechrl-data/` 只放 MLflow 存储。目录：`models/`、`datasets/`、`repos/`、`manifests/`、
`checkpoints/`、`mlruns/`、`hf-cache/`。

**拉取/审计：** 统一的、由 lockfile 驱动的下载器复现完全一致的数据集——各团队跑同一条命令得到相同数据
（HF 资产锁定到记录的 commit）：`bash scripts/data/fetch-data.sh --list`（看清单）、
`bash scripts/data/fetch-data.sh`（下载缺失项，跳过已完成）、`bash scripts/data/inventory.sh`（审计）。

**依赖：** 需要 speechrl venv（`hf` + `modelscope` CLI）与 `aria2c`。缺失时下载器会提示，并指向
`bash scripts/env-setup.sh`（完整栈）或 `bash scripts/data/fetch-data.sh --install-deps`（仅轻量下载依赖）。
默认镜像 hf-mirror.com + ModelScope。原 `wave0_fetch.sh` 引擎与一次性脚本已退役，全部统一到 `fetch-data.sh`。
完整模型/数据表与环境变量见 `docs/data.md`。
