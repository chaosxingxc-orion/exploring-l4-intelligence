---
check_id: "SAEA-QWEN3EMB-ACQUISITION-2026-08-20"
status: "PASS"
authority: "model acquisition, integrity verification and a bounded server sanity check only; no corpus audio contact"
---

# Text-embedder acquisition receipt — Qwen3-Embedding-0.6B GGUF pinned + materialised

Date: 2026-08-20. Owner-approved P-EMB-3M cascade arm (umbrella
`wiki/experiments/speech-aware-evidence-acquisition/2026-08-15-owner-go-dual-track-agentic.md`;
CASCADE construction and retriever-clause ruling in the study's
`docs/readiness/2026-08-20-embedder-charter-adjudication.md` and
`docs/readiness/2026-08-20-omni-embedding-selection.md`). This receipt closes acquisition only:
umbrella `docs/datasets.lock.json` (entry `qwen3-embedding-0.6b-gguf`) is the single live source
of asset identity; this file is the audit snapshot of how that entry was closed. **No corpus audio
or study dataset was touched; the frozen Qwen3-Omni core was never started.**

## 1. Lock registration (before any download)

Entry `qwen3-embedding-0.6b-gguf` (kind `model`, lifecycle `AUXILIARY`, new profile
`speech-aware-tools`) registered in `docs/datasets.lock.json` FIRST, then fetched via the
standard path. Live-verified identity (official `huggingface.co` model API, observed 2026-08-20):

| Field | Value |
|---|---|
| HF repo | `Qwen/Qwen3-Embedding-0.6B-GGUF` (`private: false`, `gated: false`) |
| Revision (API `sha`) | `370f27d7550e0def9b39c1f16d3fbaa13aa67728` (last modified 2025-07-14) |
| License | `apache-2.0` (`cardData.license`, and `license:apache-2.0` tag) |
| GGUF metadata | architecture `qwen3`, total params **595,776,512**, context length 32,768 |
| Chosen file | `Qwen3-Embedding-0.6B-Q8_0.gguf` — 639,150,592 B; sha256 `06507c7b42688469c4e7298b0a1e16deff06caf291cf0a5b278c308249c3e439` (HF LFS oid, from the repo tree API) |
| Sibling NOT fetched | `Qwen3-Embedding-0.6B-f16.gguf` — 1,197,629,632 B (larger single-file variant; Q8_0 is the smaller variant sufficient for an encode-only text tool and matches the ~639 MB target) |

The repo carries exactly four files (`.gitattributes`, the two GGUFs, `README.md`); no other
quantizations are published in this repo. Gates run after registration:
`python scripts/data/asset_lock.py validate` -> `OK 123 assets`;
`python scripts/data/test_asset_lock.py -v` -> 8/8 OK.

## 2. Download and byte verification

- Channel: the standard `asset_lock.py fetch qwen3-embedding-0.6b-gguf` path (`hf_complete.py`
  pinned-revision manifest + `aria2c`, official `https://huggingface.co` endpoint, single
  connection per file as pinned by the shared fetch defaults). One round; wall-clock **~309 s**
  (`time` real 5m8.853s) for 639,150,592 bytes (avg ~2.0 MiB/s).
- Landing: `$SPEECHRL_DATA_DIR/models/qwen3-embedding-0.6b-gguf/` — the ONE working copy. A scoped
  scan of the data root's `models/` directory, `$HOME` (excluding `.venvs`), and the Hugging Face
  hub cache shows no scatter copies (the `hf_complete.py`/`aria2c` path never populates the hub
  cache, so none exists).
- Post-download `sha256sum` of the payload matches the lock/LFS oid exactly:
  `06507c7b42688469c4e7298b0a1e16deff06caf291cf0a5b278c308249c3e439`.
- Machine check: `asset_lock.py inventory qwen3-embedding-0.6b-gguf --full --fail-on-drift` ->
  `COMPLETE`, `drift=0`, exit code 0. Local receipt:
  `models/qwen3-embedding-0.6b-gguf/.speechrl-asset.json`.

## 3. Sanity check — pinned llama-server, encode-only, zero corpus contact

- Binary: the study's pinned `llama.cpp-featcache` build,
  `/home/chao/llama.cpp-featcache/build/bin/llama-server`, sha256
  `097c96ec5a3f576f378d4d5e103928bf070647fdcc1f015eacb839503e121c68`, build commit
  `5d9dfcb58ea860295da8fc93c7b5bed9e2c71151` (`--version` reports `version: 5 (5d9dfcb58)`) — the
  same binary already on record in `docs/receipts/runtime-q4km-featcache.json`, reused unmodified.
- GPU was idle before the check (114 MiB used, 0% util, `clocks.sm` 1200 MHz — not P-state
  stuck), so the server was started on GPU (`-ngl 99`) rather than falling back to CPU; a spare
  port (8092) was used. Invocation:
  `llama-server -m Qwen3-Embedding-0.6B-Q8_0.gguf --embedding --pooling last -ngl 99 --port 8092`.
  Server reported healthy after 31 s (model load).
- `/props` confirms `modalities: {vision:false, video:false, audio:false}` and
  `total_slots: 4` — a text-only encode server, no audio path, no chat/generation exercised.
- One synthetic string (`"the quick brown fox jumps over the lazy dog: synthetic sanity string
  20260820"`, not corpus text) was POSTed to `/embedding` twice, back to back, on the same warm
  server.
- **Dimension**: both calls returned a **1024-d** vector (`emb["embedding"]`, last-token pooled),
  L2 norm ≈ 1.0 (0.99999997) — matches the Qwen3-Embedding-0.6B card's published embedding
  dimension.
- **Determinism**: **not bit-exact** across the two identical-input calls under GPU batched
  serving. cosine similarity **0.999910**, mean |Δ| **3.28e-4**, max |Δ| **1.40e-3**. This is
  consistent with known llama.cpp CUDA batched-inference float non-determinism (slot/KV-cache
  scheduling and reduction-order jitter across concurrent server slots), not with a broken or
  misconfigured pooling path — the two vectors are near-identical, not divergent. Recorded here
  as an observed fact for any downstream construction that assumes exact reproducibility from this
  server path; a CPU-only or single-slot re-check is left to the P-EMB-3M smoke's own registration
  if bit-exactness turns out to matter there.
- Teardown: server process terminated cleanly (`SIGTERM`, confirmed by the server's own "cleaning
  up before exit" log line); GPU memory returned to the pre-check baseline (114 MiB, 0% util)
  after exit.
- **Zero corpus contact**: no SLURP/Audio2Tool/Earnings/AMI or any other study dataset audio or
  text was sent to the server; the only input was the one synthetic string above, sent twice.

## 4. Boundary statement

Zero frozen-core contact; the Qwen3-Omni llama-server was never started. Zero corpus-audio and
zero corpus-text contact — only one synthetic string, embedded twice, against the new tool model.
The shared `~/.venvs/speechrl` was not modified (only its already-installed `asset_lock.py`/`aria2c`
tooling and the pre-existing pinned `llama.cpp-featcache` binary were exercised; no `pip install`
ran). No other `docs/datasets.lock.json` entries were touched. Paid spend: 0. Any subsequent use of
this embedder on study data (the P-EMB-3M cascade arm itself) requires its own registered
exposure-ledger row in the study repository, per the study's charter; this receipt closes
acquisition and a bounded machinery sanity check only.
