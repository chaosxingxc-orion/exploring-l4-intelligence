---
check_id: "MMA-DIAR-ACQUISITION-2026-08-18"
status: "PASS"
authority: "model acquisition, integrity verification, deployment-runtime build and reference-venv preparation only; no diarization on corpus audio"
---

# Diarization tool acquisition receipt — Sortformer v2 pin materialised

Date: 2026-08-18. Owner ruling of the same day: **v2 locked, download authorized.** This receipt
closes the acquisition prerequisite (Section 6) of the registered smoke
(`papers/meeting-minutes-agent/docs/readiness/2026-08-18-diar-smoke-preregistration.md`). The pin
source is the selection ticket
(`papers/meeting-minutes-agent/docs/plans/2026-08-18-diarization-tool-selection.md`). The single
live source for asset identity is `docs/datasets.lock.json` (entry `diar-sortformer-4spk-v2`);
this file is the audit snapshot of how that entry was closed. **No diarization was run on
AMI/ICSI/any corpus audio; the smoke flight remains separately gated.**

## 1. Lock registration (before any download)

Entry `diar-sortformer-4spk-v2` (kind `model`, lifecycle `AUXILIARY`, new profile
`meeting-minutes-tools`) registered in `docs/datasets.lock.json` FIRST, then fetched via the
standard path. Live-verified identity (official `huggingface.co` API, observed 2026-08-18,
matching the selection ticket exactly):

| Field | Value |
|---|---|
| HF repo | `nvidia/diar_streaming_sortformer_4spk-v2` (ungated, `gated: false`) |
| Revision (API `sha`) | `5240a64075176943f677d30fa2171c780229f341` (last modified 2026-08-12) |
| License | CC-BY-4.0 |
| `diar_streaming_sortformer_4spk-v2.nemo` | 471,367,680 B; sha256 `b371afce2c4958186469df33d939936b9746c89f38b10a69cfd2c61254e83329` (HF LFS oid) |
| `diar_streaming_sortformer_4spk-v2.q8_0.gguf` | 147,075,776 B; sha256 `0679cfeb1ce356d0dea9470b31274f4bfc7eb927497d82005483770666da998a` (HF LFS oid) |

Gates run after registration: `python scripts/data/asset_lock.py validate` -> `OK 122 assets`;
`python scripts/data/test_asset_lock.py` -> 8/8 OK.

## 2. Download and byte verification

- Channel: the standard `asset_lock.py fetch diar-sortformer-4spk-v2` path (`hf_complete.py`
  pinned-revision manifest + `aria2c`, official endpoint). One round; wall-clock **376 s** for
  618,443,456 bytes (avg ~1.6 MiB/s).
- Landing: `$SPEECHRL_DATA_DIR/models/diar-sortformer-4spk-v2/` — the ONE working copy; a
  data-root sweep and the HF hub cache show no scatter copies.
- Post-download `sha256sum` of both payloads matches the lock/LFS oids exactly (hash pass 4 s).
- Machine check: `asset_lock.py inventory diar-sortformer-4spk-v2 --full --fail-on-drift` ->
  `COMPLETE`, drift=0 (full per-file hash verification). Local receipt:
  `models/diar-sortformer-4spk-v2/.speechrl-asset.json`.
- The v1 checkpoint (CC-BY-NC-4.0) was deliberately NOT downloaded; it is the smoke's contingent
  Arm C only.

## 3. NeMo-Speech.cpp deployment build (WSL2 ext4)

- Checkout: `/home/chao/nemo-speech.cpp`, pinned detached at
  **`4c749a700500e077d4732a539eb082bf2208dac7`** (main tip 2026-08-18; the repository has no
  tagged release yet). Submodules of record: ggml `c03b4e2bcece5134827881af90242086daf75be5`
  (the project's pinned CUDA patch series is applied by `scripts/configure.sh`, so ggml reports
  `c03b4e2b-dirty` by design), llama.cpp `560445bf34c87356ad0f8d80fb03ec5488850b65` (present,
  not linked by the diar preset).
- Build: CMake preset **`cuda-diar`** (Ninja, Release, `GGML_CUDA=ON`,
  `CMAKE_CUDA_ARCHITECTURES=120` -> `120a`), nvcc from `/usr/local/cuda-12.8`, GCC 13.3.0,
  cmake 4.3.4 (shared-venv `bin` on PATH, read-only use). The sentencepiece dependency was built
  as a private static archive with the repo's own helper
  (`scripts/build_sentencepiece_static.sh`, google/sentencepiece
  `17d7580d6407802f85855d2cc9190634e2c95624`, under the checkout's `.deps/`;
  `CMAKE_POLICY_VERSION_MINIMUM=3.5` required under cmake 4.x) — no system package was
  installed. Build wall-clock 207 s (227 targets).
- Binary: `build/cuda-diar/bin/nemo-speech`, 366,048 B, sha256
  **`1a3e3f4fe7db4c48e5d6e44a76d5adf2bbfef80024c023b0eab2766eb61aca78`**; `--version` reports
  `nemo-speech 1.0.0`.
- Proof the CUDA path loads the pinned GGUF — exactly ONE bundled-sample run, as authorized:
  `nemo-speech diarize test_files/asr/wav/test/jfk.wav --model <pinned q8_0 GGUF> --offline
  --format rttm` on CUDA0 (RTX 5090 Laptop, compute 12.0). All 971 GGUF tensors loaded; a
  plausible single-speaker RTTM (3 segments, speaker_1) was emitted; 19.48 s wall including
  model load. The input is the 11 s JFK clip that ships inside the runtime repository — it is
  not program corpus audio.

## 4. Reference venv `~/.venvs/diar`

- Fresh Python 3.12.3 venv on WSL2 ext4; the shared `~/.venvs/speechrl` was never modified
  (post-check: its torch is still 2.9.1+cu128, site-packages mtimes unchanged).
- Torch first, from the cu128 index, mirroring the shared venv's proven build:
  **torch 2.9.1+cu128 + torchaudio 2.9.1+cu128** (27-wheel set resolved by pip against
  `download.pytorch.org/whl/cu128`, fetched resumably with aria2c to
  `/home/chao/tmpops/diar-wheels/`, installed offline in 55 s).
- Then **`nemo_toolkit[asr]==3.0.0` PLAIN** — the `cu12`/`cu13` extras were NOT used (verified
  against PyPI metadata: those extras pin `torch==2.12.0+cu126`/`+cu132` and would have replaced
  the cu128 build). Install wall-clock 309 s. **pip did not attempt to replace torch**: the
  install log contains no torch download or uninstall, and `torch.__version__` after the install
  is still `2.9.1+cu128`. The documented 2.7.0 fallback pin was NOT needed.
- Load test (model load only, CPU, zero audio): `import nemo.collections.asr` OK (13 s);
  `SortformerEncLabelModel.restore_from(<pinned .nemo>)` restored successfully —
  **117,693,960 parameters** (matches the card's 117M) in 38.4 s.
- Version pins of record: nemo-toolkit 3.0.0, torch 2.9.1+cu128, torchaudio 2.9.1+cu128,
  lightning 2.4.0, pytorch-lightning 2.6.5, numpy 2.5.2, lhotse 1.33.0, librosa 1.0.0,
  hydra-core 1.3.2, omegaconf 2.3.0, plus `pyannote.metrics` 4.1 (DER scoring, ungated PyPI,
  per the selection ticket's Route A; torch re-checked intact afterwards). Full 151-line
  `pip freeze` snapshot at `/home/chao/tmpops/diar-wheels/diar-venv-freeze-2026-08-18.txt`
  (ext4).

## 5. Boundary statement

Zero frozen-core contact; the Qwen3-Omni server was never started. Zero corpus-audio contact.
The shared `~/.venvs/speechrl` was not modified (its cmake/ninja binaries were only executed).
Paid spend: 0. First diarization on AMI dev audio requires the registered smoke's own flight
gate, not this receipt.
