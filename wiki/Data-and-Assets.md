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

## Relocating the data root (cross-drive move runbook)

`speechrl-data/` is env-var-addressed (`SPEECHRL_DATA_DIR`), so moving it across drives is mostly a
copy — but the load-bearing risk is everything that *derived* an absolute path from the old root, not
the bytes. The 2026-07-09 D:→E: move (649.5 GB / 555,618 files) is the reference; see
[Decision-Log](Decision-Log.md) (2026-07-09). Order of operations:

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
6. **Update docs + the one hardcoded fetch script** (`CLAUDE.md`/`AGENTS.md`/`README.md`/`docs/data.md`/
   `docs/setup.md`/this page + `scripts/data/fetch-qwen3-omni-gguf.sh`). The repo/code itself **stays
   put** — only the data root moves, so code paths like `common/src` absolute refs are unaffected.

> Don't declare "done" at the delete step — steps 5–6 are where cross-drive moves silently rot.
