# speechrl-common

Shared library for the **chaos speech-multimodal-LLM RL** research series (4 works).
Each work repo depends on this package as an editable install.

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
| `speechrl_common.configs` | `base.yaml` Hydra config the works compose on top of |

Optional extras: `audio`, `models`, `embed` (sentence-transformers, the W4 omni-embed backbone),
`probe` (scikit-learn), `metrics` (sacrebleu), `tracking`, `dev`. Heavy deps stay lazy-imported.

## Design note

Importing `speechrl_common` is cheap: heavy deps (torch, transformers, librosa, mlflow, jiwer)
are **lazy-imported** inside functions, so the package imports and its smoke tests pass before the
full ML stack (verl/torch) is installed.

## Install (from a work repo's venv, in WSL2)

```bash
uv pip install -e ../../common            # core (light)
uv pip install -e "../../common[audio,models,tracking]"   # with heavy extras
```

## Test

```bash
pytest common/tests
```
