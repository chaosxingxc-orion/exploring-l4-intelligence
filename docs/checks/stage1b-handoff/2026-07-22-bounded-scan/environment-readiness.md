# Stage-1B bounded-scan environment readiness

**Scope:** no-model environment/asset presence check for the post-scan reproduction handoff.
No model was loaded, no dataset example was evaluated, and no metric, smoke result, or prototype was
produced.

## Runtime identity

| Item | Observed |
|---|---|
| WSL distribution | `Ubuntu-24.04` |
| Python environment | `~/.venvs/speechrl` |
| Python | 3.12.3 |
| torch | 2.9.1+cu128 |
| torch CUDA build | 12.8 |
| CUDA available / devices | true / 1 |
| Device 0 | NVIDIA GeForce RTX 5090 Laptop GPU |
| transformers / accelerate | 5.12.1 / 1.14.0 |
| hydra-core / mlflow | 1.3.3 / 3.14.0 |
| datasets / jiwer / librosa | 5.0.0 / 4.0.0 / 0.11.0 |
| POSIX pypdf | 6.14.2 |

## Locked assets

Direct directory-presence checks against `docs/datasets.lock.json` found all 28/28 declared dataset
directories and all 3/3 declared model directories under `SPEECHRL_DATA_DIR`:

- `models/qwen3-omni-30b-a3b-instruct-gguf`
- `models/nemotron3-nano-omni-nvfp4`
- `models/omni-embed-nemotron-3b`

This is a presence check, not a file-hash inventory and not evidence that a retained paper's exact
task split is locally reproducible. The earlier all-asset inventory attempt exceeded two minutes;
the handoff therefore requires file-level inventory only for the first selected reproduction slice,
avoiding a repeated full hash of the approximately 381 GB locked asset set.

## Gate result

**Environment construction READY; model execution WITHHELD.** The base WSL/Python/CUDA environment,
locked dataset directories, and locked model directories are present. Before the first reproduction,
the selected card must still bind an exact dataset split, upstream repository commit/license,
dependency environment, model artifact, metric, compute bound, and abort condition. A separate owner
authority decision is required before any model load/smoke or dataset metric run.
