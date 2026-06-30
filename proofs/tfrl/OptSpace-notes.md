# OptSpace — optimization-space adequacy for training-free RL (proof memo, living/POMDP)

> Proof memo for `TfrlProofs/OptSpace.lean` (NEW), extending **T1** (`Tilting.tilting_optimal`) and **T3**
> (`Suppression.qstar_eq_q0_of_const`). Companion: [[2026-06-30-agent-level-synthesis]] (axis **B8**).
> Built step-by-step (POMDP): a **Proof Belief-State** + a **Trajectory log** that records the proof-search
> path *including dead-ends and rollbacks*. Lean v4.31.0 + mathlib v4.31.0.

## The theoretical constraint (owner's hypothesis — what we formalize)
Training-free RL tilts `q*(z) ∝ q0(z)·exp(R(z)/β)`.
- **(a)** action space = only the model's **output fed back as context** (single-model self-loop) ⇒ achievable
  **reward spread ≈ 0** ⇒ tilt ≈ `q0` ⇒ RL ineffective.
- **(b)** lift into an **agent system** — **context isolation across agents** + skill/memory loading make the
  action space a **product/separable** structure ⇒ **positive, k-growing reward spread** ⇒ RL attainable.
- **(c)** the enlarged space is unstable: naive rollout need not converge (no monotone optimization path) ⇒
  convergence needs **algorithm-level** structure (credit assignment + trust region).

## Existing formalism reused (`Tilting.lean`)
`Z : Type* [Fintype Z]` (action space) · `q0 R : Z → ℝ` · `β : ℝ` · `Zpart q0 R β = ∑ w, q0 w * exp(R w/β)` ·
`qstar q0 R β z = q0 z * exp(R z/β) / Zpart` · `F q0 R β q = (∑ z, q z * R z) − β * KL(q‖q0)` ·
identity `F(qstar) − F(q) = β * ∑ z, q z * log(q z / qstar z)` (`F_sub_eq_beta_mul_kl`) · T1 `tilting_optimal`.

Define **`gain q0 R β := F q0 R β (qstar q0 R β) − F q0 R β q0`** (objective gain of the optimum over baseline).
By the identity with `q := q0`: `gain = β · KL(q0 ‖ qstar) = β·log(Zpart) − E_{q0}[R]  (= β·log E_{q0}[exp(R/β)] − E_{q0}[R])`.
Define **`spread R := (univ.sup' R) − (univ.inf' R)`** (max−min reward over the finite `Z`).

## Target lemmas (OSA-1/2/3) — statements
- **OSA-1 (small/flat ⇒ ~0 gain, quantitative).** `0<β`, `q0>0`, `∑q0=1` ⇒ `gain q0 R β ≤ (spread R)^2 / (8*β)`.
  Route: `gain = β·log E_{q0}[exp(R/β)] − E_{q0}[R]` (identity) ≤ `spread^2/(8β)` by **Hoeffding's lemma** on the
  bounded variable `R/β` (range `spread/β`). *Corollary (recovers T3):* `spread R = 0 ⇒ gain = 0`.
  **Pre-planned rollback (T6 pattern):** if mathlib v4.31.0 lacks Hoeffding/log-sum-exp, take it as a hypothesis
  `hHoeffding : β·log(Zpart) − E_{q0}[R] ≤ spread^2/(8β)` and prove the chain (mirrors T6's `hPinsker`).
- **OSA-2 (product/isolated ⇒ additive, k-growing gain).** For `Z = Z₁ × Z₂`, `q0 = q0₁⊗q0₂`
  (`q0(z₁,z₂)=q0₁ z₁ * q0₂ z₂`), separable `R(z₁,z₂)=R₁ z₁ + R₂ z₂` (context isolation):
  `gain (q0₁⊗q0₂) (R₁⊞R₂) β = gain q0₁ R₁ β + gain q0₂ R₂ β`. (Proof: `Zpart` factorizes ⇒ `log Zpart` adds;
  `E[R]` adds ⇒ `gain` adds.) ⇒ over `k` isolated agents `gain = Σ gainᵢ ≥ k·minᵢ gainᵢ > 0` when each `Rᵢ`
  non-constant. *(Context isolation enlarges the space ⇒ training-free RL attainable & grows with #agents.)*
- **OSA-3a (rollout instability — finite counterexample).** Exhibit a concrete `Z`, `R`, and a naive
  myopic/append-only update `U` whose fixed point `q∞` satisfies `F(q∞) < F(qstar)` strictly (no monotone path).
  *(the owner's "无法rollout出优化路径".)* Concrete instance chosen at θ4. **(θ2-grounded):** naive
  non-convergence is documented across every action axis — Reflexion plateau (2303.11366), ACE context collapse
  (2510.04618), append-only error propagation (2505.16067), temporal contamination (2605.17830) — plus a *proven*
  output-level seed: the hard-BoN/BoP true-reward rise-then-decline is **inevitable** (2506.19248).
- **OSA-3b (credit-assigned convergence).** On the product structure, per-component tilting equals the global
  optimum: `(qstar q0₁ R₁ β) ⊗ (qstar q0₂ R₂ β) = qstar (q0₁⊗q0₂) (R₁⊞R₂) β`, which maximizes `F` (T1). So
  structured per-isolated-component credit assignment **reaches `qstar`** where naive joint rollout (OSA-3a) does
  not. **(θ2-grounded + scoping):** the realistic field version is JitRL (2601.18510): `z'=z+β·Â ⇒ π*∝π_θ·exp(βA)`
  = our `q*` with reward→credit-assigned advantage and `β·KL` the **trust region**; its convergence is *asymptotic*
  in-probability consistency under a **slow-policy-drift** precondition. **The hinge:** the trust region is what
  *enforces* slow-drift; naive fast-drift rollout (OSA-3a) violates it. The Lean lemma proves the **exact
  finite-separable backbone** (per-component tilt = global qstar, unconditional); the asymptotic-under-trust-region
  statement is the field version we cite, not prove.

## Proof Belief-State `b(proof)` — live (VOI-ordered)
| # | Axis | Belief | Conf | Status |
|---|---|---|---|---|
| P0 | Toolchain builds here (elan + mathlib cache + `lake build` existing `TfrlProofs` green) | unknown | low | **unprobed (θ1)** |
| P1 | OSA-1 chain provable via `F_sub_eq_beta_mul_kl`; Hoeffding hypothesis-isolated if needed | likely | med-high | unproven |
| P2 | mathlib v4.31.0 has the API (`Finset.sup'/inf'`, `Real.add_pow_le_pow_mul_pow_of_sq_le_sq`/Hoeffding, exp/log) | likely | med | unprobed (θ1) |
| P3 | OSA-2 product factorization (`Fintype.sum_prod_type`, `Finset.prod`, `Real.exp_add`, `Real.log_mul`) | likely | med | unproven |
| P4 | OSA-3a finite counterexample constructible | likely | med | unproven |
| P5 | OSA-3b reduces to OSA-2 + T1 | likely | med-high | unproven |
| C* | convergence survey: which open-source TFRL methods carry convergence proofs / instability cures | — | — | unprobed (θ2) |

## Trajectory log (proof-search path; newest at bottom)
| θ | Date | Belief before → action → observation → update | Rollback? |
|---|---|---|---|
| θ0 | 2026-06-30 | reflection + S1 GO → **scaffold proof memo; state OSA-1/2/3 in the existing formalism; seed Proof Belief-State** → (no obs) → highest-VOI = P0 (does the toolchain build here) gates everything; OSA-1 is the most-decisive lemma (recovers T3, validates approach) | no |
| θ1 | 2026-06-30 | P0 → **install elan; `lake exe cache get` + `lake build` existing `TfrlProofs` on ext4** → obs: elan 4.2.3 OK, `cache` exe built (25/25); **mathlib cache download slow/flaky (single-digit KB/s, retries) — build still running** → update: toolchain installs; P0 (local-verify) **pending** the slow cache fetch | — (in progress) |
| θ2 | 2026-06-30 | C* → **convergence survey (3 lanes, 43 claims / 54 sources, `wf_14ef3acb-2a3`)** → obs: **OSA-3 grounded** — naive rollout non-convergent across all axes (Reflexion plateau / ACE collapse / append-only error-prop / temporal contamination) + *proven* output seed (BoN hump inevitable, 2506.19248); OSA-3b = JitRL exact KL-opt (`z'=z+βÂ ⇒ π*∝π_θ·exp(βA)`) + **asymptotic** consistency under **slow-drift**, with the **trust region as the hinge**; proven *finite-N* convergence lives only at the output level → update: **C\* resolved**; OSA-3a/3b grounded + scoped (Lean proves the exact finite backbone, cites JitRL for the asymptotic field version) | no |
