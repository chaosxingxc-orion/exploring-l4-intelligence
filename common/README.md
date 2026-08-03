# speechrl-common

Program-infrastructure library of the `exploring-l4-intelligence` umbrella. It was originally built
for the historical W1–W4 work repositories (retired 2026-08-03; remotes kept as cold backups).
Admitted studies do not depend on it by default: a study consumes it only after registering an
explicit dependency pin (exact umbrella commit) in its migration manifest, with `../../common`
editable installs reserved for local development override. Per-module consumer/ownership/deprecation
status lives in [`OWNERSHIP.md`](OWNERSHIP.md).

## Layout

| Module | Purpose |
|---|---|
| `speechrl_common.audio` | audio load/resample (`io`), log-mel features (`features`) |
| `speechrl_common.models` | speech-LLM loaders (`qwen2_audio`), omni-embed loader (`omni_embed`), prompt templates (`prompts`) |
| `speechrl_common.rl` | verifiable rewards/metrics: `reward` (WER/ASR/exact-match), `embedding_metrics` (recall@k/MRR/retrieval), `probe` (linear/kNN accuracy), `disentanglement` (separation/silhouette/leakage), `metrics` (accuracy/F1/BLEU/chrF/EER) |
| `speechrl_common.eval` | probing/retrieval harness over a frozen embedder (`probing`) |
| `speechrl_common.data` | dataset registry + data-root resolution (`registry`) |
| `speechrl_common.tracking` | local-MLflow run helper (`mlflow_logger`) |
| `speechrl_common.utils` | `seed`, `logging`, `checkpoint` path helpers |
| `speechrl_common.configs` | `base.yaml` Hydra config the retired works composed on top of (legacy) |

Optional extras: `audio`, `models`, `embed` (sentence-transformers, the legacy omni-embed backbone),
`probe` (scikit-learn), `metrics` (sacrebleu), `tracking`, `dev`. Heavy deps stay lazy-imported.

## Design note

Importing `speechrl_common` is cheap: heavy deps (torch, transformers, librosa, mlflow, jiwer)
are **lazy-imported** inside functions, so the package imports and its smoke tests pass before the
full ML stack (verl/torch) is installed.

## Install (from a study repo's venv, in WSL2 — local development override only)

```bash
uv pip install -e ../../common            # core (light)
uv pip install -e "../../common[audio,models,tracking]"   # with heavy extras
```

CI and release reproduction must not use the editable path: they install from the exact umbrella
commit pinned in the consuming study's migration manifest / lockfile.

## Test

```bash
pytest common/tests
```
