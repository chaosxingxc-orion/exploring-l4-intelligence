# scripts/data — unified data & model downloader

Models and datasets are **never committed to git**. The only current catalog is
[`docs/datasets.lock.json`](../../docs/datasets.lock.json). It contains a frozen-baseline profile,
observed local candidates, bounded study acquisition profiles and blocked/deferred records. These
scripts fetch a local copy into `${SPEECHRL_DATA_DIR:-<repo>/speechrl-data}`. Full reference:
[`docs/data.md`](../../docs/data.md).

## Engine + shims

[`asset_lock.py`](asset_lock.py) is the lock-driven validator/fetcher/inventory engine.
[`fetch-assets.sh`](fetch-assets.sh) is the compatibility dispatcher. Its data, candidate and
inventory entry points cross an immediate lock-driven boundary into `asset_lock.py`; the specialized
GGUF and paper-integrity paths remain shell subcommands.

The five former standalone entry points remain delegating shims to `fetch-assets.sh`:

| Entry point (shim) | Subcommand | What it does |
|---|---|---|
| `fetch-data.sh` | `data` | Reads only `datasets.lock.json`; defaults to `frozen-baseline`, or fetches named assets. `--list` / `--dry-run` / `--install-deps` / `<name…>`. |
| `fetch-candidates.sh` | `candidates` | Compatibility alias for the lock's `local-candidates` profile. The old candidate JSON is a fact-free retired pointer. |
| `fetch-qwen3-omni-gguf.sh` | `qwen3-gguf` | Fetches the Qwen3-Omni-30B-A3B-Instruct GGUF (weight + mmproj) for llama.cpp, with pinned sha256 verification. |
| `fetch-stage1c-priority-papers.sh` | `papers` | Exact-ID Stage-1C priority-paper fetch with per-file sha256 verification. Its literal content is larger than the other shims because `docs/contracts/stage1c-common-rubric.json` asserts `must_contain` on this exact file's bytes (paper IDs + `SPEECHRL_DATA_DIR`/`aria2c`/`sha256sum`) — the migrated manifest identities stay inline in this file for that reason. |
| `inventory.sh` | `inventory` | Audits every governed asset by reading only the canonical lock. |

You can also call the engine directly: `bash scripts/data/fetch-assets.sh <subcommand> [args...]`
(run with no subcommand, or `-h`/`--help`, for the subcommand list).

```bash
bash scripts/data/fetch-data.sh --list          # show the manifest, fetch nothing
bash scripts/data/fetch-data.sh                  # frozen-baseline profile (skips complete)
bash scripts/data/fetch-data.sh meld slurp       # fetch only named assets
bash scripts/data/inventory.sh                   # audit vs the lock
python scripts/data/asset_lock.py fetch --profile speech-aware-core
```

**Dependencies.** Needs `python3`, `git`, `git-lfs`, `curl`, `hf`, `modelscope` for legacy baseline
records, and `gdown` for registered Drive attachments. `aria2c` is retained for specialized
large-file paths. The downloader preflight-checks and, if anything is missing, points to:

```bash
bash scripts/env-setup.sh                        # full stack (torch/verl + download CLIs); creates the venv
bash scripts/data/fetch-data.sh --install-deps   # lightweight: just the download CLIs + aria2 (no torch)
```

### Specialized legacy paths

- `qwen3-gguf`'s venv-activation line does not export `PATH` the way `data`/`candidates`' does.
- `qwen3-gguf` hardcodes its workspace path to the D: drive rather than deriving it from the
  script's own location (used only for a log line, not for path resolution).

> The per-asset engine `wave0_fetch.sh` (formerly in the W1 repo) and the one-off campaign /
> `fetch-semantic-*` scripts were retired — everything is unified here, driven by `datasets.lock.json`.
