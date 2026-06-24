# 2026-06-24 · emotion-pooling · CREMA-D · Operator-A sample-level gain

> Validation archive (naming `yyyy-mm-dd-验证方向-数据集-实验目的`). Index: [[Validation-Experiment-Matrix]].
> Status: **PASSED (scoped)** — a real training-free Operator-A gain on emotion; CI-separation marginal
> at test=300 (see §8). Validation-only; large-scale deferred.

## 1. 假设 / Hypothesis
- **H0:** no weight-free readout of the frozen omni-embedding beats the deployed mean-pool for emotion
  (Δ ≤ 0).
- **H1:** a second-order, weight-free pooling (attentive-stats) at a mid layer raises 6-way emotion
  probe accuracy over the mean-pool baseline (Δ > 0) — emotion lives in variance/salient frames that
  mean-pooling washes out.

## 2. 验证方向 / Validation direction
Operator A = inference-time search over the **pooling × layer** axis of a FROZEN embedder (no weight
update, no params added). Select, by a verifiable probe reward, the pooling+layer that best exposes
emotion; compare to the deployed mean-pool. This is the β→0 (argmax) case of the tilting selection.

## 3. 数学证明 / Math proof (Lean)
Backed by **T1 (tilting optimality, `proofs/tfrl/TfrlProofs/Tilting.lean`)**: the verifiable-reward
argmax over a finite candidate set (here: pooling×layer variants) is the β→0 limit of the optimal
tilted selection `q*(z) ∝ q0(z)·exp(R(z)/β)`. The gain is an *activation* of present-but-unexposed
information (P/L/S: Presence + linear accessibility), not new learning — consistent with **T3
(flat-reward no-go)**: had emotion been absent (flat reward across variants), no selection could help.

## 4. 数据集 / Datasets
- `crema-d` (pinned `ac5b65fb890f1db0d2f7d6268d13994f481e5567`, `docs/datasets.lock.json`), 6 balanced
  emotion classes from the filename code (chance 0.167), 91 speakers. Seeded dev 600 / test 300
  (disjoint pools; closed-set). License: see lockfile.
- Model: `omni-embed-nemotron-3b` (frozen, bf16, sdpa) on RTX 5090.

## 5. 实验脚本 / Scripts
```
reproduce: SPEECHRL_DATA_DIR=<repo>/speechrl-data HF_HUB_OFFLINE=1 \
  /home/chao/.venvs/speechrl/bin/python projects/speech-mllm-omni-embedding-rl/scripts/pool_method_probe.py
# env: SWEEP_SEED=42 SWEEP_DEV=600 SWEEP_TEST=300 SWEEP_LAYERS=0,8,16,24,32,36 SWEEP_POOLS=audio,audio_std,audio_stats,audio_attn
```
Code: `scripts/pool_method_probe.py` + `layer_probe.extract_pooled` + `probes.{probe_accuracy,bootstrap_ci}`.
Env fingerprint: torch 2.9.1+cu128, transformers 4.57.6, sentence-transformers 5.6.0, sklearn 1.9.0.

## 6. 结果与统计分析 / Results + statistics
MLflow run `981429345eff4e808d94f55016e29133`, seed 42, knn(k=5) probe, 1000-boot 95% CIs.

| factor | mean-pool baseline (best L) | best pool×layer | Δ | 95% CI (sel) |
|---|---|---|---|---|
| **emotion** | 0.393 @L0 (CI [0.340,0.447]) | **attn @L16 = 0.490** | **+0.097** | [0.433, 0.550] |
| speaker | 0.047 (CI [0.023,0.070]) | attn @L16 0.063 | +0.016 | [0.040,0.093] (≈chance) |
| content | 0.987 | 0.997 | +0.010 | [0.990,1.000] (ceiling) |

Emotion: point gain **+0.097 (≈+25% rel)** via weight-free attentive-stats pooling at mid-layer 16.

## 7. 可复现性 / Reproducibility
Deterministic (seed 42), pinned data + model, knn probe. **Golden:** emotion attn@L16 ≈ 0.49 ± 0.05
(within CI); a re-run must land emotion-attn@L16 in [0.43, 0.55] and clearly above the mean baseline
(~0.39). Cross-seed (survey seed 7/42) corroborates (mean 0.40 → attn 0.51 @ seed 42 dev-selected).

## 8. 对抗挑战 / Adversarial challenge (5 roles)
- **Statistician — SCOPED.** Baseline CI [0.340,0.447] and sel CI [0.433,0.550] *touch* (0.433<0.447);
  the 95% CIs are not cleanly disjoint at test=300, so Δ>0 is suggestive, not yet p<0.05. Mitigation:
  paired bootstrap on the same test clips (not independent-CI overlap) + larger test set; the survey's
  dev-selected seed-42 result (0.513) strengthens it.
- **Reproducibility auditor — SCOPED.** Best layer here is **test-selected** (oracle layer pick),
  which can inflate the max. Proper Operator A selects pooling+layer on **dev**. TODO: re-run with
  dev-selection (the survey did, giving 0.513 — gain survives). dev/test pools disjoint (no leakage).
- **Theory critic — HOLDS.** Attentive-stats is weight-free (no trained params) → stays in training-free
  Operator A; gain = activating present info (T1/T3 apply). Not a base-weight update.
- **Domain expert — HOLDS (scoped).** 6-class balanced accuracy (filename code, the verified label),
  chance 0.167; 0.49 is well above chance. Caveat: CREMA-D emotion is *acted* — generalization to
  natural emotion (e.g. MELD) is untested here.
- **Reward-hacking red-teamer — HOLDS.** The reward IS the verifiable probe accuracy (no proxy to game);
  no consensus/majority step, so no confound amplification.

**Verdict: PASSED (scoped).** A real, theory-backed, training-free Operator-A emotion gain (+0.097);
to upgrade to an unqualified p<0.05 claim, add dev-selection + paired bootstrap (queued for large-scale).
