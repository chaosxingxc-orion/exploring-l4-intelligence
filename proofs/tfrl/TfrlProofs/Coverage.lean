import Mathlib

set_option linter.style.header false
set_option linter.style.longLine false

/-!
# T-coverage — best-of-N oracle coverage (the FIRST operator-linked theorem)

This module formalizes the coverage property of the **actual implemented best-of-N operator**
and is dual-tracked with the empirical bridge `coverage_bridge.py`.

## What object is formalized (read this first — honesty statement)

The engineering operator is `best_of_n` in
`common/src/speechrl_common/rl/decode.py` (lines 30–39): given a candidate set it returns the
`argmax_i R(z_i)` of a verifiable reward (here `R = -WER`). In the ASR reproduction, its candidate
pool is produced by the generation loop of
`projects/speech-mllm-training-free-rl/scripts/repro_asr_best_of_n_v2.py` (lines 524–531):

```
for ps in POOL_SEEDS:                 #  (pool-seed replicate)
    for i in range(POOL):             #  (candidate index)
        seed = ps * 100003 + j * 17 + i
        txt, lp = gen_with_retry(wav, seed, TEMP, TOP_P, MAXTOK)   # temp=0.8, top_p=0.95
```

Each inner draw is an **independent** sample from the SAME frozen sampling distribution (same audio,
same prompt/instruction, same temperature/top-p — only the RNG `seed` changes), so per draw the event
"this candidate is *good*" (strictly lower WER than the greedy `temp=0` decode; `select_oracle_idx`,
lines 286–289, is the argmin-WER selector that realizes this) has a fixed base probability `p`,
independent across draws. This is the textbook i.i.d. Bernoulli model.

We formalize the resulting **miss probability** — the probability that NONE of `N` independent draws
is good — as a **plain real-analysis object on an independent-Bernoulli product**:

* `missProb p N := (1 - p) ^ N`.

The independence content is not swept under the rug: `missProb_eq_prod` proves that this is exactly
the finite product `∏_{i<N} (1 - p)` of the `N` per-draw miss probabilities — i.e. the joint all-miss
probability of `N` independent Bernoulli(`p`) draws, which is the honest meaning of the definition.
`coverageProb p N := 1 - missProb p N` is the oracle-coverage (probability at least one draw is good),
the quantity `coverage_bridge.py` predicts as `1 - (1 - p̂)^N`.

We deliberately do NOT build the `(Fin N → Ω)` product-measure tower; the real-analysis form on the
Bernoulli product is a faithful, fully machine-checked model of the same i.i.d. loop, with no `sorry`
and no new axioms.

## Results

* `missProb_eq_prod`   — `missProb p N = ∏_{i<N} (1 - p)` (the independence identity).
* `missProb_antitone`  — miss probability is monotone (non-increasing) in `N` for `0 ≤ p ≤ 1`.
* `missProb_strictAnti` — strictly decreasing in `N` for `0 < p < 1` (more draws strictly help).
* `missProb_le_of_N_ge` — the sample-complexity corollary: for `0 < p < 1`, `0 < δ < 1`,
  `N ≥ log δ / log(1 - p)` suffices for `missProb p N ≤ δ`.
* the `example`s at the end are the **Python/Lean parity vector** (`p = 1/4`, `N = 3` ⇒ miss `27/64`,
  coverage `37/64`), checked here by `norm_num` and mirrored by an exact-fraction assertion in
  `coverage_bridge.py`.
-/

namespace TfrlProofs.Coverage

open Real
open scoped BigOperators

/-- **Best-of-N miss probability.** The probability that NONE of `N` independent draws is *good*,
each draw being good with base probability `p`. On the independent-Bernoulli model this is the product
of the `N` per-draw miss probabilities `(1 - p)`, i.e. `(1 - p) ^ N` (see `missProb_eq_prod`). -/
noncomputable def missProb (p : ℝ) (N : ℕ) : ℝ := (1 - p) ^ N

/-- **Best-of-N oracle coverage.** The probability that AT LEAST ONE of `N` independent draws is good
— exactly what the oracle / argmin-WER selector (`select_oracle_idx`) achieves, and what
`coverage_bridge.py` predicts as `1 - (1 - p̂)^N`. -/
noncomputable def coverageProb (p : ℝ) (N : ℕ) : ℝ := 1 - missProb p N

/-- **The independence identity.** `missProb p N` is the finite product over the `N` draws of the
per-draw miss probability `(1 - p)`. This is what makes `(1 - p) ^ N` the *joint* all-miss probability
of `N` independent Bernoulli(`p`) draws — the honest content behind the definition. -/
theorem missProb_eq_prod (p : ℝ) (N : ℕ) :
    missProb p N = ∏ _i ∈ Finset.range N, (1 - p) := by
  simp [missProb, Finset.prod_const, Finset.card_range]

/-- `coverageProb` unfolded. -/
theorem coverageProb_eq (p : ℝ) (N : ℕ) :
    coverageProb p N = 1 - (1 - p) ^ N := rfl

/-- With zero draws nothing can be good: the miss probability is `1`. -/
theorem missProb_zero (p : ℝ) : missProb p 0 = 1 := by simp [missProb]

/-- The miss probability is a genuine probability: `0 ≤ missProb p N` when `p ≤ 1`. -/
theorem missProb_nonneg {p : ℝ} (hp1 : p ≤ 1) (N : ℕ) : 0 ≤ missProb p N := by
  simp only [missProb]
  exact pow_nonneg (by linarith) N

/-- ... and `missProb p N ≤ 1` when `0 ≤ p ≤ 1`. -/
theorem missProb_le_one {p : ℝ} (hp0 : 0 ≤ p) (hp1 : p ≤ 1) (N : ℕ) :
    missProb p N ≤ 1 := by
  simp only [missProb]
  exact pow_le_one₀ (by linarith) (by linarith)

/-- **Monotone decreasing in `N`.** For a valid success probability `0 ≤ p ≤ 1`, adding draws never
increases the miss probability: `missProb p` is antitone. -/
theorem missProb_antitone {p : ℝ} (hp0 : 0 ≤ p) (hp1 : p ≤ 1) :
    Antitone (missProb p) := by
  intro M N hMN
  simp only [missProb]
  exact pow_le_pow_of_le_one (by linarith) (by linarith) hMN

/-- **Strictly decreasing in `N`.** For a non-degenerate success probability `0 < p < 1`, each extra
draw *strictly* lowers the miss probability. -/
theorem missProb_strictAnti {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) :
    StrictAnti (missProb p) := by
  intro M N hMN
  simp only [missProb]
  have h1p0 : 0 < 1 - p := by linarith
  have h1p1 : 1 - p < 1 := by linarith
  -- (1-p)^N = (1-p)^M · (1-p)^(N-M) with (1-p)^(N-M) < 1 and (1-p)^M > 0
  have hsplit : N = M + (N - M) := by omega
  rw [hsplit, pow_add]
  have hlt1 : (1 - p) ^ (N - M) < 1 := pow_lt_one₀ (le_of_lt h1p0) h1p1 (by omega)
  have hMpos : 0 < (1 - p) ^ M := pow_pos h1p0 M
  calc (1 - p) ^ M * (1 - p) ^ (N - M)
      < (1 - p) ^ M * 1 := mul_lt_mul_of_pos_left hlt1 hMpos
    _ = (1 - p) ^ M := by ring

/-- **Sample-complexity corollary.** For a non-degenerate per-draw success probability `0 < p < 1`
and a target miss rate `0 < δ < 1`, taking
`N ≥ log δ / log(1 - p)` draws guarantees `missProb p N ≤ δ`.

(Note `log(1 - p) < 0`, so the threshold `log δ / log(1 - p) = log(1/δ) / log(1/(1-p)) > 0` is the
expected positive number of draws; the bound is tight in the continuous limit. The hypothesis
`δ < 1` is carried to match the operative regime `0 < δ < 1` — it is not needed for THIS direction of
the bound, since `δ ≥ 1` makes `missProb p N ≤ 1 ≤ δ` vacuous; hence it is bound as `_hd1`.) -/
theorem missProb_le_of_N_ge {p delta : ℝ} {N : ℕ}
    (hp0 : 0 < p) (hp1 : p < 1) (hd0 : 0 < delta) (_hd1 : delta < 1)
    (hN : Real.log delta / Real.log (1 - p) ≤ (N : ℝ)) :
    missProb p N ≤ delta := by
  have h1p0 : 0 < 1 - p := by linarith
  have h1p1 : 1 - p < 1 := by linarith
  have hlogneg : Real.log (1 - p) < 0 := Real.log_neg h1p0 h1p1
  have hne : Real.log (1 - p) ≠ 0 := ne_of_lt hlogneg
  -- Multiply the sample-count hypothesis through by the negative `log (1 - p)` (flips the sign).
  have key : (N : ℝ) * Real.log (1 - p) ≤ Real.log delta := by
    have h2 : (Real.log delta / Real.log (1 - p)) * Real.log (1 - p) = Real.log delta := by
      field_simp
    rw [← h2]
    exact mul_le_mul_of_nonpos_right hN hlogneg.le
  -- Take logs of `missProb p N ≤ delta` (both positive) and reduce to `key`.
  have hpos : 0 < missProb p N := by
    simp only [missProb]; exact pow_pos h1p0 N
  have hlog : Real.log (missProb p N) ≤ Real.log delta := by
    simp only [missProb, Real.log_pow]; exact key
  have hexp := Real.exp_le_exp.mpr hlog
  rwa [Real.exp_log hpos, Real.exp_log hd0] at hexp

-- ------------------------------------------------------------------------------------------------
-- Python/Lean parity vector (first machine parity pair): p = 1/4, N = 3.
-- Mirrored by an exact-`Fraction` assertion in `coverage_bridge.py`.
-- ------------------------------------------------------------------------------------------------

/-- Parity: miss probability at `p = 1/4`, `N = 3` is `27/64`. -/
example : missProb (1 / 4 : ℝ) 3 = 27 / 64 := by
  unfold missProb; norm_num

/-- Parity: oracle coverage at `p = 1/4`, `N = 3` is `37/64`. -/
example : coverageProb (1 / 4 : ℝ) 3 = 37 / 64 := by
  unfold coverageProb missProb; norm_num

end TfrlProofs.Coverage
