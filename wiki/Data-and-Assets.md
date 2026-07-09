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

---

## Relocating the data root (cross-drive move runbook)

`speechrl-data/` is env-var-addressed (`SPEECHRL_DATA_DIR`), so moving it across drives is mostly a
copy — but the load-bearing risk is everything that *derived* an absolute path from the old root, not
the bytes. The 2026-07-09 D:→E: move (649.5 GB / 555,618 files) is the reference; see
[Decision-Log](Decision-Log) (2026-07-09). Order of operations:

1. **Copy** with robocopy (NTFS→NTFS, multithreaded, restartable; ~1.6 GB/s here):
   `robocopy SRC DST /E /COPY:DAT /DCOPY:DAT /MT:16 /R:2 /W:5 /NP /NFL /NDL /LOG:move.log`.
   Read the summary **FAILED** column, **not** the exit code — robocopy exit **1 = success** (0–7 ok,
   8+ fail). The no-dir-list flag is `/NDL`; `/NDD` is invalid.
2. **Verify byte-identity BEFORE deleting the source** — cross-check ≥2 independent tools: robocopy
   accounting (0 FAILED) + PowerShell `Get-ChildItem -Recurse -File -Force | Measure Length -Sum` on
   both sides, plus a SHA-256 of the largest file. Guard against the empty-variable false positive
   (empty `==` empty prints "OK"): assert the counts are non-zero **and** equal.
3. **Confirm nothing holds the model files** before deleting — a resident `llama-server` mmaps the
   GGUF. `pgrep -af '[l]lama'` (bracket trick avoids self-match) + a `/proc/*/maps` scan. Delete the
   source with `cmd /c rd /s /q "PATH"` (much faster than PowerShell `Remove-Item -Recurse`).
4. **Point the env var at the new root for _all_ shells:**
   - WSL `~/.bashrc` (put the `export` at the **top**, above the `case $- in *i*` interactivity guard)
     → interactive + login shells.
   - **`WSLENV`** — set Windows *user* env vars `SPEECHRL_DATA_DIR=/mnt/<drive>/…/speechrl-data` **and**
     `WSLENV=SPEECHRL_DATA_DIR` → propagates into **non-interactive** `wsl bash <script>` detached runs
     too (which never source `~/.bashrc`). No sudo; effective for newly-launched processes.
5. **Reflection pass — grep DOWNSTREAM stores for the old absolute prefix**, not just repo code (repo
   code is env-var-addressed and stayed clean). The knowledge base
   (`$SPEECHRL_KB_DIR/knowledge_base/*/values.jsonl`, field `key_audio_ref`) had 100 baked-in
   `/mnt/d/...` paths; rewrite old→new with a `.bak` backup + verify a sample resolves and JSON parses.
6. **Update docs + the one hardcoded fetch script** (`CLAUDE.md`/`AGENTS.md`/`README(_CN)`/`docs/data.md`/
   `docs/setup.md`/this page + `scripts/data/fetch-qwen3-omni-gguf.sh`). The repo/code itself **stays
   put** — only the data root moves, so code paths like `common/src` absolute refs are unaffected.

> Don't declare "done" at the delete step — steps 5–6 are where cross-drive moves silently rot.

**中文速记：** 换盘搬 `speechrl-data` 主要是 robocopy 复制，但真正的风险是"派生了旧绝对路径"的东西：
(1) robocopy 退出码 **1=成功**，看 FAILED 列，`/NDL` 不是 `/NDD`；(2) 删源前多工具字节校验（robocopy +
PowerShell 计数 + 最大文件 SHA-256），防"空变量 == 空变量 → 假 OK"；(3) 删模型前确认没有 llama-server
mmap 占用，用 `rd /s /q` 删；(4) 环境变量三层覆盖：`~/.bashrc`（放交互守卫**之前**）+ **`WSLENV`**（覆盖
非交互 `wsl bash <脚本>` 分离式运行，免 sudo，对新进程生效）；(5) 反思阶段 grep **下游存储**（KB
`values.jsonl` 的 `key_audio_ref` 曾有 100 条 `/mnt/d` 死路径），不只是代码；(6) 更新文档 + 唯一硬编码的
`fetch-qwen3-omni-gguf.sh`。**删完不等于做完。**
