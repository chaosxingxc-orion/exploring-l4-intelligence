# Theory track — convergence proofs and the constraint terms that bound the problem

> **The rule (owner, 2026-07-04).** Every theoretical proposal is locked to a Lean 4 proof in
> `proofs/tfrl/` with a **correctness proof AND a convergence proof**; the engineering implementation
> is dual-tracked with the math (same operator). A static identity is not a result. Convergence
> usually needs **explicit constraint terms** to bound the problem's edges; the load-bearing content
> is those constraints. This doc is the working discussion of *where* the constraints go and *which
> theorems* to formalize — the owner invited a detailed discussion, so this is a live draft to react to.

## 1. What we already have in Lean (the starting point)

`proofs/tfrl/` (Lean 4 v4.31.0), the OUTPUT-level (fixed q₀, given R) theory — mostly **static
identities and bounds**, no iterative-process convergence:

- **Tilting.lean** — `tilting_optimal`, `F_sub_eq_beta_mul_kl`: the tilt q*(z) ∝ q₀(z)·exp(R(z)/β) is
  the KL-regularized optimum, and **gain = F(q*) − F(q₀) = β·KL(q₀‖q\*)** (sorry-free). This is the
  master identity.
- **BestOfN.lean** — `kl_best_of_n_le`: KL(BoN‖q₀) ≤ log N − (N−1)/N (one documented order-statistics
  `sorry`). A **bounded trust region** for the best-of-N approximation of the tilt.
  > **2026-07-11 更正**：该 `sorry`已于 2026-07-10（commit `9e999f7`）被消解——消解方式是引入具名的
  > imported axiom `beirami_thm_3_1`（作用于 opaque 的 `klBoNActual`），而不是给出一个真正证明。按
  > 2026-07-11 裁定，这属于 **imported-axiom 状态**，不是 Lean-proved theorem；`sorry`计数为零不等于
  > 该界已被机器验证证明。
- **Regret.lean** — `regret_O_sqrt_log`: best-of-N regret = O(√log N). A **rate**, but for a static
  selection, not an iterated process.
- **OptSpace.lean** — the OSA suite (`gain_eq`, `flat_no_gain`, `gain_le_of_hoeffding` = gain ≤
  spread²/8β, `gain_product`, `qstar_product`). They bound *selection on a fixed q₀*. Two are now
  load-bearing for Q1's branch 2.2: **`gain_pos_of_nonconstant`** (gain strictly positive iff the
  reward is non-degenerate — the (a)-support anchor) and **`gain_product`/`qstar_product`** (a
  context-isolated agent composition has gain = sum of component gains and optimum = monolithic optimum
  → *adding an isolated agent buys no headroom; extra gain requires a genuinely new non-degenerate
  reward*). The latter is the machine-checked statement that an agentic system helps only by enlarging
  the reward, not the agent count.
- **Realization.lean (NEW, 2026-07-04, sorry-free, VERIFIED)** — the **C4** constraint formalized:
  `realized_gap_le_two_tau` (R(oracle) − R(selector) ≤ 2·τ, τ = sup|R̂ − R|), `exact_estimator_is_oracle`
  (τ=0 ⇒ ρ=1), and the **convergence theorem** `realized_tendsto_oracle` (along any selector sequence
  with τ_n → 0, realized reward → oracle, by squeeze). This is the first genuine *convergence* result
  in the library, with τ as the explicit constraint term. It ties directly to the measured (c) gap.

**Diagnosis (updated 2026-07-04).** We have the static theory of condition (a) support (`OptSpace`,
`Tilting`), and now a **verified convergence theorem for condition (c) realization** (`Realization`:
C4, with τ→0 ⇒ ρ→1). Full `TfrlProofs` builds against Mathlib v4.31.0 (8568 jobs, success); all
cited theorems sorry-free (the only `sorry` is BestOfN's documented Beirami order-statistics
derivation).

> **2026-07-11 更正**：该 `sorry` 已于 2026-07-10（commit `9e999f7`）消解为具名 imported axiom
> `beirami_thm_3_1`（作用于 opaque 的 `klBoNActual`）；按 2026-07-11 裁定为 imported-axiom 状态，非
> Lean-proved theorem——"sorry-free"不应被读作"该界已证明"。

What remains: an *iterative-process* convergence theorem for a full training-free-RL scheme
(C1 monotone-improvement / C2 budget-cap as iterated processes — the pieces `F_sub_eq_beta_mul_kl`,
`gain_le_of_hoeffding`, `regret_O_sqrt_log` exist but are not yet assembled into an iterate), and
**no theorem at all** for condition (b) reachability — the survey's explicit gap. C1/C2 are the
natural next formalizations if branch 2.1 is taken; (b)'s absence is itself part of the 2.2 anchor.

### 2026-07-11 — T-coverage: i.i.d.-Bernoulli coverage-model lemmas + empirical bridge (Coverage.lean; operator-linked count remains 0)

**2026-07-12 correction (RI item 3 / 续15 naming-correction finding):** this subsection's original
title called Coverage.lean "the FIRST operator-linked theorem" — that framing was a naming error and
has been retracted; see `docs/claim_ledger.yaml` entry `C-THEORY`, which is and remains the
authoritative status record: **the operator-linked theorem count is 0**, unchanged by this module.
What follows is corrected to match.

`proofs/tfrl/TfrlProofs/Coverage.lean` (new, `sorry`-free, **no new axiom** — verified below) formalizes
an **i.i.d.-Bernoulli coverage-probability model** for the best-of-N *pool-generation loop*, with code
citations to the actual generation loop of `scripts/repro_asr_best_of_n_v2.py` (lines 524–531) and to
the selector it feeds, `decode.best_of_n` (argmax reward) / `select_oracle_idx` (argmin-WER). It is
**not** a theorem about that selection rule itself (no result here is "operator-linked" in the ledger's
sense — see C-THEORY); it formalizes the independent-draws *sampling* step that feeds the selector, not
the reward-argmax *selection* step. **Status: verified algebra + empirical bridge** (the algebra is
machine-checked; the bridge is Stage-1 / hypothesis-grade evidence that the i.i.d. model fits the
stored pools — NOT a proof that the frozen model's draws are i.i.d., and not an operator-linked proof
of convergence for the selector). Operator-linked formalization of the selection rule itself remains
future work (Proposal-F).

**What is formalized** (honest object: a real-analysis identity on an independent-Bernoulli product,
docstring states this exactly): per-draw success prob `p` (a draw is *good* = strictly lower WER than
greedy), miss probability of `N` i.i.d. draws
* `missProb p N := (1 − p)^N`, `coverageProb p N := 1 − (1 − p)^N`;
* `missProb_eq_prod` — `= ∏_{i<N}(1 − p)` (the independence identity — makes `(1−p)^N` the *joint*
  all-miss probability, not a renamed answer);
* `missProb_antitone` (monotone ↓ in `N`, `0 ≤ p ≤ 1`) and `missProb_strictAnti` (strict ↓, `0<p<1`);
* `missProb_le_of_N_ge` — the sample-complexity corollary: `0<p<1`, `0<δ<1`,
  `N ≥ log δ / log(1 − p)` ⇒ `missProb p N ≤ δ`.

**Axiom gate.** New `scripts/lean_axiom_gate.sh` runs a `#print axioms`-style `Lean.collectAxioms`
audit over **every** `TfrlProofs.*` public declaration and fails on any axiom outside
`{propext, Classical.choice, Quot.sound, beirami_thm_3_1}`. Run 2026-07-11:
`AXIOM_GATE_OK checked 89 TfrlProofs declarations; only whitelisted axioms present` → **PASS**. So the
Coverage results depend on **no** named axiom (in particular they are independent of `beirami_thm_3_1`).

**Python/Lean parity vector** (first machine parity pair): `p=1/4, N=3` ⇒ miss `27/64`, coverage
`37/64` — checked in Lean (`example … norm_num`) AND in `coverage_bridge.py` (exact `fractions.Fraction`
assertion). Both agree.

**Empirical bridge** (`scripts/coverage_bridge.py` → `_repro/coverage_bridge_v1.json`, over the frozen
`asr_bon_v2_{snr5,clean}.json`, n=96, 24 stored candidates/utt, 3 pool seeds). Per-utterance
`p̂` = fraction of the 24 candidates strictly beating greedy; predicted oracle-coverage `1−(1−p̂)^N`
vs OBSERVED (best of the first `N` candidates beats greedy, averaged over the 3 pool seeds):

| cond | p̂ | N=1 pred/obs | N=2 pred/obs | N=4 pred/obs | N=8 pred/obs | max\|gap\| |
|---|---|---|---|---|---|---|
| snr5 | 0.135 | .135 / .139 | .207 / .222 | .285 / .299 | .349 / .361 | 0.015 |
| clean | 0.075 | .075 / .076 | .121 / .118 | .173 / .198 | .218 / .226 | 0.025 |

**i.i.d. adequacy.** Because `p̂` is per-utterance, between-utterance difficulty is already absorbed;
the gap measures only within-pool departure from conditional independence among the temp=0.8 draws
(which share the prompt+audio). It is small (max |gap| ≤ 0.025) and mostly slightly *negative*
(observed marginally exceeds the i.i.d. prediction — sampling diversity, not the strong positive
clustering that would make the model over-state coverage). So `1−(1−p)^N` is an adequate
operator-level description of the real pools to within ~1–2.5 coverage points at every `N`. This is the
dual-track anchor for best-of-N: the Lean `coverageProb` operator ⟷ the stored-pool oracle selector.

## 2. Where convergence fails — and the constraint term that fixes each failure

Any scheme that *iterates* (prompt-refinement rounds, conditioning updates q₀→q₀(c_t), agentic
decomposition, accumulated context) is an iterative process q_t → q_{t+1}. Unconstrained, it does NOT
converge — the documented failure modes (ACE context collapse, Reflexion plateau, best-of-N
over-optimization) are non-convergence. Four constraint terms recover it; each is a candidate theorem.

| # | Failure mode (unconstrained) | Constraint term | Convergence theorem to formalize |
|---|---|---|---|
| **C1** | Policy drifts too far per step → oscillation / collapse | **KL trust-region** KL(q_{t+1}‖q_t) ≤ ε (equivalently the β in the exp-tilt bounds step size) | *If every step's KL ≤ ε and per-step reward gain ≥ δ(ε) > 0, the process is monotone and converges to a fixed point; gain telescopes to Σδ.* Builds on `F_sub_eq_beta_mul_kl`. |
| **C2** | Over-optimization: proxy reward ↑ while gold reward ↓ | **Budget cap N ≤ N\*** (the HedgeTune / Best-of-Poisson interior optimum) | *Realized gold-gain(N) is unimodal with a provable interior max N*; for N > N* the gold gain strictly decreases.* Extends `regret_O_sqrt_log` from monotone-bound to unimodal-with-cap. |
| **C3** | Conditioning/memory drifts faster than the estimator can track → inconsistency | **Slow-drift / Lipschitz** ‖q₀(c_{t+1}) − q₀(c_t)‖ ≤ L·η_t, Σηₜ = ∞, Σηₜ² < ∞ (Robbins–Monro) | *Under the drift bound, the reward-estimate is consistent and the iterate converges a.s. to the constrained optimum.* This is the rigorous form of JitRL's asymptotic-consistency-under-slow-drift. |
| **C4 ✅ DONE** | Deployment reward is estimated R̂ ≠ R → Goodhart; realized gain unbounded-below | **Estimation-error bound** ‖R̂ − R‖∞ ≤ τ (or a calibration/KL penalty on the selector) | **FORMALIZED & VERIFIED** in `Realization.lean` (sorry-free): `realized_gap_le_two_tau` (R(oracle)−R(selector) ≤ 2τ), `realized_tendsto_oracle` (τ_n→0 ⇒ realized→oracle). Ties the theory to the measured ρ gap (E3/E4: ρ≈0 because τ large — confidently wrong). |

**Why this is real content, not tautology.** Each theorem has the two-part structure the review
demanded: (i) a **negative result** — the unconstrained process provably does not converge (or is
unbounded-below in gold reward); (ii) a **positive result** — under the explicit constraint it
converges, with a rate. The constraint term is the load-bearing hypothesis, not a relabeling. C1–C4
are the standard trust-region / budget / drift / estimation quartet from stochastic-approximation and
RLHF over-optimization theory, specialized to the training-free tilt — finitary enough to Lean-formalize
(discretize the iterate space; the per-step KL and Hoeffding pieces already exist).

## 3. How this serves the Q1 decision tree

- **Branch 2.1 (space sufficient).** Any proposed training-free-RL scheme ships with its C1/C2
  convergence theorem (does the iterated prompt/selection scheme provably improve and converge, capped
  at N*?) and the dual-tracked implementation. "Continuous improvement over baseline" becomes a
  *provable* monotone-improvement claim, not a hope.
- **Branch 2.2 (space insufficient → agentic expansion).** The insufficiency anchor needs a
  **capping theorem**: fixed-q₀ instruct-prompting has gain ≤ spread²/8β on the reachable set (we have
  `gain_le_of_hoeffding`; the new part is proving the *prompt-reachable* spread is itself bounded — the
  (b) theorem that does not yet exist). Then the agentic expansion needs a **non-separable
  irreducibility + convergence theorem**: decomposition/tool-injection creates a NEW verifiable
  sub-reward or enlarges support such that the constrained (C1–C4) iterated process converges to
  gain **strictly greater** than the fixed-q₀ cap. **This is exactly the deep-review's precondition P1
  and the closure's re-open condition r2** — a peer-reviewed non-separable decomposition bound —
  produced in-house and machine-checked. The constraint terms C1–C4 are what make that expansion
  *converge* rather than diverge (the θ2-survey's "trust-region is the hinge", now formalized).

## 4. Open questions for the detailed discussion (owner)

1. **Which constraint term is primary for our setting?** For frozen-omni + best-of-N the natural
   knobs are β (trust-region) and N (budget cap) — both already in `proofs/tfrl`. Do we formalize C1+C2
   first (they're closest to done) and treat C3/C4 as the agentic-expansion additions?
2. **What is the reachable-spread bound for (b)?** The missing (b)-theorem needs a model of how
   conditioning moves q₀. Candidate: bound the prompt-reachable spread by the mutual information between
   the instruction and the output distribution — a constraint that makes "prompt-space is capped"
   provable. Worth a dedicated design pass.
3. **Discretization for Lean.** The iterate space must be finitary for a machine-checked convergence
   proof. Do we prove convergence on a finite candidate pool (best-of-N is already finite) and state the
   continuous case as the documented limit?
4. **Dual-track binding.** Each theorem names the exact code object (e.g. `mbr_utils`,
   `best_of_n`, the CP-1 instruction search). Do we add a CI check that the Lean operator and the Python
   selector stay in sync (a test that the code's update rule matches the theorem's hypotheses)?

## Parked — filling the shared-knowledge floor via the omni-embedding system (deferred, owner 2026-07-05)

The corrected omni-verifier theory (TH2a, 2026-07-05) reframes the omni-as-reward as a **two
context-differentiated systems** (generator-agent + verifier-agent, same frozen weights, distinct
system-prompt/context) — an agentic composition, NOT self-reward. The load-bearing constraint is the
**achievable error-decorrelation δ_corr** between the two systems (context differentiation elicits
functionally different behavior from the same weights), and convergence → oracle as δ_corr → 0. The one
**irreducible residual floor** is the **shared knowledge blind-spot**: items where no context
differentiation of the frozen M helps because M genuinely lacks the information (both systems necessarily
fail). **Owner note (2026-07-05):** this residual floor is real and is **deferred** — out of scope for
the current Q1 study. The plan to fill it: **supplement the knowledge blind-spot via the omni-embedding
system (W4 flagship)** — the embedding system is precisely the *independent-of-M* signal the
C4/decorrelation theory says you need to beat the floor. This requires **defining new omni agentic
tasks**, so it will be discussed only when we reach that stage. This is the concrete bridge from the
(c)-realization floor (this study) to W4 and branch 2.2.

## 中文摘要

**规则:** 所有理论 proposal 锁定到 `proofs/tfrl/` 的 Lean 证明,必须同时有**正确性证明 + 收敛性证明**,
工程实现与定理同指一个算子(双轨),静态恒等式不算结果;收敛通常需要**约束项**界定边界,承重内容就是
这些约束。**现状:** 已有 Tilting(gain=β·KL)、BestOfN(KL 界)、Regret(O(√log N))、OptSpace(OSA
恒等式——正是被判同义反复的部分);**无任何迭代过程的收敛定理,(b) 可达性无定理**。**四个约束项**修四种
不收敛:C1 KL 信赖域(步长)、C2 预算上限 N*(过优化)、C3 慢漂移 Lipschitz(估计一致性)、C4 奖励估计
误差界(Goodhart)。每个都有"无约束不收敛 + 有约束收敛"的两段结构——是真内容不是相义反复。**服务 Q1:**
2.1 每个方案带 C1/C2 收敛定理(基线可证单调提升);2.2 先证"固定 q₀ 的 prompt 空间受限"(缺的 (b) 定理),
再证 agentic 扩展在 C1–C4 约束下收敛到严格更高的增益——**这正是 deep-review 的前置 P1 与关闭的重开条件 r2
(同行评审级非可分分解界),在内部机器验证完成**。§4 四个待议问题请你定夺。

---

> **命名注记（2026-07-14，修正案 №1）**：本文 TH2a 处的字面名「achievable error-decorrelation
> δ_corr」与其极限语义（δ_corr→0 ⇒ 收敛向 oracle）存在命名方向张力——该量实为**残余误差相关**
> （越小越好）。第三轮博导复审裁定后，δ_corr 仅保留此原义，其经验估计对象=`error_corr`；
> 「选择重合」永久移出该符号语义。拆名四量与 strict-I2 kill-if 重写见
> `2026-07-14-identity-contracts-amendment-1.md`（本注为 dated 追加，原文未改）。
