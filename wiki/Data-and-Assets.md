# Data & Assets

Model weights and datasets (~281 GB) are **deliberately out of git** — GitHub holds only code, docs,
and download scripts. The authoritative asset list (every model & dataset, sources, mirrors, env
knobs) is the repo's
[`docs/data.md`](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/blob/master/docs/data.md).

**Where it lives.** `speechrl-data/` under the repo root by default, resolved as
`${SPEECHRL_DATA_DIR:-<repo>/speechrl-data}`. On WSL2 prefer ext4 (`~/speechrl-data/`). Layout:
`models/`, `datasets/`, `repos/`, `manifests/`, `checkpoints/`, `mlruns/`, `hf-cache/`.

**Fetch / audit.**

```bash
source ~/.venvs/speechrl/bin/activate
bash scripts/data/probe-access.sh   # read-only reachability (HF / ModelScope)
bash scripts/data/fetch-data.sh     # models + datasets (skips already-complete)
bash scripts/data/inventory.sh      # COMPLETE / PARTIAL / MISSING per asset
```

Per-asset control uses the engine `projects/speech-mllm-training-free-rl/scripts/wave0_fetch.sh`
(e.g. `bash scripts/wave0_fetch.sh m_omni_embed_nemotron`, `… d_librispeech`; run `… help`).

**Mirrors.** China-mainland mirrors (hf-mirror.com + ModelScope) are the default
(`SPEECHRL_CN_MIRROR=1`); force a source with `SPEECHRL_MODEL_SOURCE` / `SPEECHRL_DATASET_SOURCE`.
Default fetch pulls four generation models + the W4 omni-embedding model
(`SPEECHRL_SKIP_OMNI_EMBED=1` to skip); `baichuan-omni-1d5` / `kimi-audio-7b-instruct` run
individually. Full model/dataset tables and all env knobs: `docs/data.md`.

---

## 中文

模型权重与数据集（≈281 GB）**有意不进 git**——GitHub 只放代码、文档和下载脚本。权威的资产清单（每个
模型与数据集、来源、镜像、环境变量）是仓库的
[`docs/data.md`](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/blob/master/docs/data.md)。

**放在哪：** 默认 `speechrl-data/` 在仓库根，按 `${SPEECHRL_DATA_DIR:-<repo>/speechrl-data}` 解析；
WSL2 上优先 ext4（`~/speechrl-data/`）。目录：`models/`、`datasets/`、`repos/`、`manifests/`、
`checkpoints/`、`mlruns/`、`hf-cache/`。

**拉取/审计：** 见上方命令（`probe-access.sh` 只读探测、`fetch-data.sh` 下载、`inventory.sh` 审计）。
逐项下载用引擎 `projects/speech-mllm-training-free-rl/scripts/wave0_fetch.sh`（如
`m_omni_embed_nemotron`、`d_librispeech`，`… help` 看全部）。

**镜像：** 默认中国大陆镜像（hf-mirror.com + ModelScope，`SPEECHRL_CN_MIRROR=1`）；用
`SPEECHRL_MODEL_SOURCE` / `SPEECHRL_DATASET_SOURCE` 强制来源。默认拉四个生成模型 + W4 omni 嵌入模型
（`SPEECHRL_SKIP_OMNI_EMBED=1` 跳过）；`baichuan-omni-1d5` / `kimi-audio-7b-instruct` 单独跑。完整
模型/数据表与全部环境变量见 `docs/data.md`。
