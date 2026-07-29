# scripts/data — unified data & model downloader

Models and datasets are **never committed to git** (~440 GB on disk). The set is **FROZEN** to the
snapshot in [`docs/datasets.lock.json`](../../docs/datasets.lock.json) — the single manifest. These
scripts fetch a local copy into `${SPEECHRL_DATA_DIR:-<repo>/speechrl-data}`. Full reference:
[`docs/data.md`](../../docs/data.md).

## Engine + shims (2026-07-29 shell-logic merge)

[`fetch-assets.sh`](fetch-assets.sh) is the single engine: a subcommand dispatcher plus the small
set of env/venv-activation lines that were byte-identical across two or more of the former
standalone scripts (see its header comment for exactly which lines and why). Each subcommand's
actual fetch/audit logic is migrated **verbatim** from its former script — same manifest, same
target paths, same flags, same retry/log behavior. This is a shell-logic merge only: pre-existing
behavioral differences *between* the former scripts (different `set` strictness, different retry
counts, different log-line prefixes, `candidates` not honoring `SPEECHRL_WORKSPACE` the way `data`
does, etc.) were **not** unified — they're preserved exactly and listed under "Known
inconsistencies" below.

The five former standalone entry points still work, unchanged, as 2-3 line delegating shims to
`fetch-assets.sh` — nothing about their documented CLI (flags, positional args, env overrides)
changed:

| Entry point (shim) | Subcommand | What it does |
|---|---|---|
| `fetch-data.sh` | `data` | **The unified, self-contained downloader.** Reads `datasets.lock.json` and fetches *exactly* the locked set (28 datasets + 5 models + 7 ref repos) from each asset's source at its pinned revision, skipping complete ones. `--list` / `--dry-run` / `--install-deps` / `<name…>`. |
| `fetch-candidates.sh` | `candidates` | Downloads the WS-D survey-sourced candidate datasets (`docs/datasets.candidates.json`), Xet-safe via `hf_complete.py` + single-connection aria2c. `--list` / `<name…>`. |
| `fetch-qwen3-omni-gguf.sh` | `qwen3-gguf` | Fetches the Qwen3-Omni-30B-A3B-Instruct GGUF (weight + mmproj) for llama.cpp, with pinned sha256 verification. |
| `fetch-stage1c-priority-papers.sh` | `papers` | Exact-ID Stage-1C priority-paper fetch with per-file sha256 verification. Its literal content is larger than the other shims because `docs/contracts/stage1c-common-rubric.json` asserts `must_contain` on this exact file's bytes (paper IDs + `SPEECHRL_DATA_DIR`/`aria2c`/`sha256sum`) — the migrated manifest identities stay inline in this file for that reason. |
| `inventory.sh` | `inventory` | Audits `speechrl-data/` and reports COMPLETE / PARTIAL / MISSING per locked asset. |

You can also call the engine directly: `bash scripts/data/fetch-assets.sh <subcommand> [args...]`
(run with no subcommand, or `-h`/`--help`, for the subcommand list).

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

### Known inconsistencies (pre-existing, preserved as-is by the merge)

- `candidates`' `REPO_ROOT` does not honor a `SPEECHRL_WORKSPACE` override the way `data`'s
  `WORKSPACE` does (`data` derives its data root as `${SPEECHRL_WORKSPACE:-<script-dir>/../..}`;
  `candidates` always derives it from the script location).
- `set` strictness differs per subcommand: `data`/`qwen3-gguf` use `set -uo pipefail`,
  `candidates` uses `set -u` only, `papers` uses `set -euo pipefail`, `inventory` sets nothing.
- `log`/`warn` prefixes and `retry()` semantics differ: `data` retries 3x (5s/10s/15s) tagged
  `[fetch]`; `candidates` retries 5x (10s/20s/…/50s) tagged `[fetch-candidates]`; `qwen3-gguf` has
  only a bare `log()` (no `warn`/`retry`) tagged `[fetch-gguf]`; `papers`/`inventory` have neither.
- `qwen3-gguf`'s venv-activation line does not export `PATH` the way `data`/`candidates`' does.
- `qwen3-gguf` hardcodes its workspace path to the D: drive rather than deriving it from the
  script's own location (used only for a log line, not for path resolution).

> The per-asset engine `wave0_fetch.sh` (formerly in the W1 repo) and the one-off campaign /
> `fetch-semantic-*` scripts were retired — everything is unified here, driven by `datasets.lock.json`.
