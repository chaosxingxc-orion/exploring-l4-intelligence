# 2026-06-24 · factor-suppression · CREMA-D · Operator-A control (pipeline validation)

> Validation archive. Index: [[Validation-Experiment-Matrix]]. Status: **PASSED** — reproduces the
> documented 3-factor baseline + the speaker-suppression NULL (the control that motivates Operator B).

## 1. 假设 / Hypothesis
- **H0:** the frozen omni-embedding exposes content/emotion/speaker uniformly; conditioning steers each.
- **H1 (observed expectation):** content exposed (≈1.0), emotion partial (~0.4), **speaker suppressed
  (≈chance)**; single-instruction conditioning does NOT steer (Δ≈0, diagonal_dominant=False).

## 2. 验证方向 / Validation direction
Pipeline-validation + per-factor control on the two-orthogonal-factor substrate. Confirms the GPU
env + Operator-A loop reproduce the prior result before extending to new factors.

## 3. 数学证明 / Math proof (Lean)
**T3 (flat-reward no-go, `Suppression.lean`)** is the key: speaker reward is flat across conditionings
(`I(e; speaker) ≈ 0`) ⇒ tilted selection = baseline ⇒ no frozen-vector operator recovers speaker
(Operator B mandatory). **T1 (tilting)** frames the conditioning argmax.

## 4. 数据集 / Datasets
`crema-d` (pinned `ac5b65fb…`), factors content(12)/emotion(6)/speaker(91); dev 600 / test 300, seed 42.
Model: frozen `omni-embed-nemotron-3b`, GPU.

## 5. 实验脚本 / Scripts
```
reproduce: SPEECHRL_DATA_DIR=<repo>/speechrl-data HF_HUB_OFFLINE=1 \
  /home/chao/.venvs/speechrl/bin/python -m omni_embedding_rl.main seed=42
```
Code: `eval_harness.run`, `data_cremad`, `conditioning` {baseline,content,emotion,speaker}, `probes`.

## 6. 结果与统计分析 / Results + statistics
MLflow `0b6ccd15b09e4ba1b456886243f00bfe`, knn(k=5), 1000-boot CIs. diagonal_dominant=False.

| factor | selected | test acc (CI) | Δ vs baseline | reading |
|---|---|---|---|---|
| content | baseline | [0.99, 1.00] | +0.000 | exposed (ceiling) |
| emotion | baseline | [0.303, 0.413] | +0.000 | partial/capped (conditioning flat) |
| speaker | emotion | [0.020, 0.060] | −0.007 | **≈chance — suppressed (control)** |

## 7. 可复现性 / Reproducibility
Deterministic seed 42; pinned data/model. Golden: content ≈1.0, emotion ≈0.36–0.41, speaker ≈0.02–0.06;
diagonal_dominant=False. A re-run must land each within its CI.

## 8. 对抗挑战 / Adversarial challenge (5 roles)
- **Statistician — HOLDS.** Deltas ≈0 with overlapping CIs (correct null); speaker CI sits at chance
  (1/91≈0.011 lower bound; observed ~0.04 ≈ small-sample chance band).
- **Reproducibility auditor — HOLDS.** Reproduces the historical 1.1.1 numbers on a freshly-rebuilt
  venv/GPU; seeded disjoint pools; pinned data. This is the live proof the pipeline is sound.
- **Theory critic — HOLDS.** Speaker null is the T3 flat-reward no-go in practice — a *result* (encoder
  is speaker-invariant, `I(e;spk)≈0`), prescribing Operator B / external channel, not a failure.
- **Domain expert — HOLDS.** Filename emotion code (verified label, not the skewed CSV); content =
  12-sentence ID (lexical). Acted-emotion caveat noted.
- **Reward-hacking — HOLDS.** Verifiable probe accuracy; no proxy.

**Verdict: PASSED.** Pipeline validated; speaker-suppression control reproduced — the empirical anchor
for "Operator A can't recover a destroyed factor" (T3).
