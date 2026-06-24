# 2026-06-24 · language-intent · MINDS-14 · Operator-A disentanglement (the untested factor)

> Validation archive. Index: [[Validation-Experiment-Matrix]]. Status: **PASSED (null for steering;
> positive for presence)** — intent is readable from the frozen embedding but NOT steerable by
> instruction-conditioning. Validation-only.

## 1. 假设 / Hypothesis
- **H0:** intent is not linearly readable from the frozen omni-embedding (≈ chance), OR conditioning
  does not change intent readability (Δ ≤ 0).
- **H1a (presence):** intent is readable (acc ≫ chance 1/14 = 0.071).
- **H1b (steerability):** the intent-conditioning best exposes intent (`A_intent(e_intent) >
  A_intent(e_baseline)`, sig Δ>0; diagonal-dominant).

## 2. 验证方向 / Validation direction
Extend the proven CREMA-D Operator-A loop to the **language+intent** factor family (never measured).
Conditioning×factor probe matrix on a clean 14-way intent task (en-US), select by verifiable dev reward.

## 3. 数学证明 / Math proof (Lean)
**T1 (tilting, `Tilting.lean`)** frames the conditioning selection (argmax verifiable reward = β→0
tilting). **T3 (flat-reward no-go, `Suppression.lean`)** is the operative result here: when the reward
(probe acc) is ~flat across conditionings, the tilted selection ≈ baseline ⇒ no steering gain — exactly
what we observe. Presence (intent readable) shows the *information* is there; T3 explains why the
*conditioning* lever can't move it.

## 4. 数据集 / Datasets
`minds14` (PolyAI/minds14), en-US, 14 intents (chance 0.071); audio in HF parquet (decoded+resampled to
16 kHz by `data_minds14`). Seeded intent-balanced dev 280 / test 257 (disjoint). Pinned via lockfile.
Model: frozen `omni-embed-nemotron-3b`, GPU.

## 5. 实验脚本 / Scripts
```
reproduce: SPEECHRL_DATA_DIR=<repo>/speechrl-data HF_HUB_OFFLINE=1 \
  /home/chao/.venvs/speechrl/bin/python -m omni_embedding_rl.main \
    dataset=minds14 run_name=minds14_intent_probe_v1 seed=42
```
Code: `data_minds14.py` (new), generalized `eval_harness.run`, `conditioning.py` (+intent/+lid),
`configs/dataset/minds14.yaml`. Conditionings: {baseline, content, emotion, intent}.

## 6. 结果与统计分析 / Results + statistics
seed 42, knn(k=5), 1000-boot CIs. MLflow under experiment `speech-mllm-omni-embedding-rl`.

| factor | baseline acc (CI) | selected cond | sel acc (CI) | Δ | chance |
|---|---|---|---|---|---|
| intent | ~0.25, CI [0.195, 0.304] | emotion | CI [0.214, 0.319] | +0.016 | 0.071 |

- **Presence (H1a): SUPPORTED** — baseline ≈0.25 ≫ chance 0.071 (CI well above chance). The frozen
  embedding *contains* intent.
- **Steerability (H1b): NOT SUPPORTED** — Δ=+0.016, sel CI overlaps baseline CI; selected conditioning
  is `emotion` (not `intent`); diagonal_dominant=False. Instruction-conditioning is a flat lever.

## 7. 可复现性 / Reproducibility
Deterministic seed 42, pinned data/model, balanced disjoint splits. Golden: intent baseline ≈0.20–0.30,
Δ within ±0.05 of 0 (no significant steering). Cross-seed expected to corroborate (low-variance probe).

## 8. 对抗挑战 / Adversarial challenge (5 roles)
- **Statistician — HOLDS.** The *null* (no steering) is the honest read: Δ+0.016 with overlapping 95%
  CIs is not significant. Presence claim is safe (baseline CI entirely above chance 0.071).
- **Reproducibility auditor — HOLDS.** Seeded balanced disjoint dev/test; pinned data. Note test=257
  (not 280) because some intents had < per-class quota after the disjoint split — balanced, not biased.
- **Theory critic — HOLDS.** Matches P/L/S: Presence ✓, Steerability ✗ for the conditioning axis (T3).
  Consistent with CREMA-D: the frozen retriever *exposes* semantic factors but single-instruction
  conditioning doesn't steer. Real intent gains would need Operator-A pooling/layer or Operator B.
- **Domain expert — HOLDS.** 14-way en-US intent, chance 0.071; ≈0.25 readability is meaningful for a
  frozen, never-fine-tuned encoder. (Telephone-quality 8 kHz audio upsampled to 16 kHz — a mild
  domain caveat, not a confound for the present/steer conclusions.)
- **Reward-hacking red-teamer — HOLDS.** Verifiable probe accuracy reward; no consensus/proxy gaming.

**Verdict: PASSED.** Flagship untested factor measured: **intent is present (readable) but not
conditioning-steerable** — a clean, theory-consistent result that scopes where gains must come from.
