# speechrl-common

Shared library for the **chaos speech-multimodal-LLM RL** research series (4 works).
Each work repo depends on this package as an editable install.

## Layout

| Module | Purpose |
|---|---|
| `speechrl_common.audio` | audio load/resample (`io`), log-mel features (`features`) |
| `speechrl_common.models` | speech-LLM loaders (`qwen2_audio`), prompt templates (`prompts`) |
| `speechrl_common.rl` | verifiable reward fns for GRPO/PPO (`reward`: WER/ASR/exact-match) |
| `speechrl_common.data` | dataset registry + data-root resolution (`registry`) |
| `speechrl_common.tracking` | local-MLflow run helper (`mlflow_logger`) |
| `speechrl_common.utils` | `seed`, `logging`, `checkpoint` path helpers |
| `speechrl_common.configs` | `base.yaml` Hydra config the works compose on top of |

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
