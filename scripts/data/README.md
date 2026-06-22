# scripts/data — model & dataset downloads

Models and datasets are **never committed to git** (≈281 GB). These scripts fetch your own local
copy into `${SPEECHRL_DATA_DIR:-<repo>/speechrl-data}`. Full reference: [`docs/data.md`](../../docs/data.md).

| Script | What it does |
|---|---|
| `fetch-data.sh` | Primary entry point. Downloads default models + W4 omni-embedding model + datasets + refs (skips already-complete assets, aria2-accelerated SLURP audio). |
| `probe-access.sh` | Read-only reachability/auth check for HF/ModelScope before a big fetch. |
| `inventory.sh` | Audits `speechrl-data/` and reports COMPLETE / PARTIAL / MISSING per asset. |
| `campaigns/` | Historical per-campaign drivers, preserved verbatim for reference. |

The actual per-asset engine (one function per model/dataset, mirror + retry logic) lives in
`projects/speech-mllm-training-free-rl/scripts/wave0_fetch.sh` — run `bash …/wave0_fetch.sh help`
for every target.

```bash
source ~/.venvs/speechrl/bin/activate
bash scripts/data/probe-access.sh
bash scripts/data/fetch-data.sh
```
