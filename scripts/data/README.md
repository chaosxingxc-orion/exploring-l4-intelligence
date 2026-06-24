# scripts/data — unified data & model downloader

Models and datasets are **never committed to git** (~410 GB on disk). The set is **FROZEN** to the
snapshot in [`docs/datasets.lock.json`](../../docs/datasets.lock.json) — the single manifest. These
scripts fetch a local copy into `${SPEECHRL_DATA_DIR:-<repo>/speechrl-data}`. Full reference:
[`docs/data.md`](../../docs/data.md).

| Script | What it does |
|---|---|
| `fetch-data.sh` | **The unified, self-contained downloader.** Reads `datasets.lock.json` and fetches *exactly* the locked set (28 datasets + 5 models + 7 ref repos) from each asset's source at its pinned revision, skipping complete ones. Any team reproduces identical data with one command. `--list` / `--dry-run` / `--install-deps` / `<name…>`. |
| `inventory.sh` | Audits `speechrl-data/` and reports COMPLETE / PARTIAL / MISSING per locked asset. |
| `probe-access.sh` | Read-only HF reachability/auth check (rarely needed once frozen). |

```bash
bash scripts/data/fetch-data.sh --list          # show the manifest, fetch nothing
bash scripts/data/fetch-data.sh                  # fetch everything missing (skips complete)
bash scripts/data/fetch-data.sh meld slurp       # fetch only named assets
bash scripts/data/inventory.sh                   # audit vs the lock
```

**Dependencies.** Needs `python3`, `git`, `curl`, `aria2c`, `modelscope` (`jq` optional). HF datasets
download via hf-mirror's `hfd`+`aria2c` (the `hf` CLI is only a fallback — it is incompatible with
hf-mirror). The downloader preflight-checks and, if anything is missing, points to:

```bash
bash scripts/env-setup.sh                        # full stack (torch/verl + download CLIs); creates the venv
bash scripts/data/fetch-data.sh --install-deps   # lightweight: just the download CLIs + aria2 (no torch)
```

> The per-asset engine `wave0_fetch.sh` (formerly in the W1 repo) and the one-off campaign /
> `fetch-semantic-*` scripts were retired — everything is unified here, driven by `datasets.lock.json`.
