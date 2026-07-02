# θ2 — Convergence of training-free RL (synthesis): grounding OSA-3

> Convergence survey for the OptSpace proof (`proofs/tfrl/OptSpace-notes.md`, lemma **OSA-3**) and
> [[2026-06-30-agent-level-synthesis]]. Run `wf_14ef3acb-2a3`, 2026-06-30; 3 lanes, per-lane adversarial
> verification, **43 verified claims / 54 sources**. Lanes:
> [output-convergence](2026-06-30-survey-agent-output-convergence.md) ·
> [agent-stability](2026-06-30-survey-agent-agent-stability.md) ·
> [stabilization](2026-06-30-survey-agent-stabilization.md). All links real; each claim tagged
> *convergence (proven/empirical/none) · open-source · scope (no-gradient vs weight-updating)*.

## OSA-3 grounding (the load-bearing finding)
OSA-3 is two-sided, and the literature joins the two sides by a **single mechanism — the trust region**:

- **OSA-3a — naive-rollout NON-convergence.** Documented across *every* axis of the enlarged action space:
  decode (hard Best-of-N true reward rises-then-**falls** under a proxy — *provably inevitable* for the
  BoN/SBoN/BoP family, arXiv:2506.19248; Goodhart curves arXiv:2210.10760); context-build (ACE "context
  collapse", arXiv:2510.04618, self-admits no convergence analysis); skill/self-improvement (Reflexion
  **plateaus** ~4 trials, arXiv:2303.11366); memory-recall (append-only error propagation arXiv:2505.16067;
  temporal memory contamination — violation rate **rises with exposure**, arXiv:2605.17830; poisoning persists,
  arXiv:2512.16962). So "keep rolling out + append memory + rewrite context" has multiple divergence/plateau
  modes and **no monotone path**.
- **OSA-3b — credit-assigned + trust-region CONVERGENCE.** **JitRL** (arXiv:2601.18510) Thm 4.1 proves the
  additive retrieval-advantage logit update `z' = z + β·Â` is the **exact closed-form** solution of
  `argmax E[Â] − (1/β)·KL(π'‖π_θ)`, i.e. `π* ∝ π_θ·exp(β·A)` — *precisely* `q*(z) ∝ q0·exp(R/β)` with reward `R`
  replaced by a **credit-assigned advantage `A`** and `β·KL` as the **trust region**; Thm 4.2/4.3 give
  kNN-estimator + policy **in-probability consistency** as memory grows.
- **The hinge (critical for the Lean statement).** JitRL's consistency is **asymptotic, NOT finite-time
  monotone**, and holds only under a **slow-policy-drift** precondition. Naive fast-drift rollout **violates**
  it (→ OSA-3a); the **β-KL trust region enforces** it (→ OSA-3b). ⇒ *the trust region is what makes credit
  assignment converge* — OSA-3 is one mechanism, not two disconnected claims.

**Consequence for `OptSpace.lean`:** OSA-3b should target **convergence-of-the-credit-assigned tilt under a
trust-region/separability precondition**, not finite-time monotonicity. In the idealised **finite separable**
setting of OSA-2, per-component tilting equals the global `qstar` **exactly** (T1) — the clean algebraic
backbone; the realistic version is JitRL's asymptotic-under-slow-drift consistency. OSA-3a is the
trust-region-removed (myopic/append-only) counterexample.

**The gap OSA-3 fills:** proven *finite-N* convergence exists only at the **output level** (soft-BoN O(1/N)
arXiv:2505.03156, MBR O(N^−1/2) 2502.12685, GSI 2506.04118, CarBoN 2510.15674, HedgeTune N* 2506.19248); the
**agent level** has *only* JitRL's asymptotic result. No method yet proves finite-time monotone improvement over
the full *memory·skill·context·decode* space.

## Convergence map — output level (the convergent inner loop OSA-3 must preserve)
| Method | Convergence | Open-source | Cures | Scope |
|---|---|---|---|---|
| Soft Best-of-N (2505.03156) | **proven** O(1/N) to `q*`, Pareto-optimal via β | — | over-optimization via β trust region | no-grad |
| Best-of-Poisson + HedgeTune (2506.19248) | **proven** rise-then-decline inevitable; N*/β* root-find | [hedging](https://github.com/hskhalaf/hedging) | the Goodhart hump (N* sweet spot) | no-grad |
| Hard BoN theory (2401.01879) | **proven** KL ≤ log N−(N−1)/N; win-rate ≤ N/(N+1) | — | trust-region drift cost; *no* reward monotonicity | no-grad |
| BoN smoothing-lens (2507.05913) | **proven** regret + phase transition (soft beats hard) | — | why finite β* cures over-optimization | no-grad |
| MBR (2502.12685) | **proven** O(N^−1/2) | — | variance/aggregation, hack-resistant | no-grad |
| Guided Speculative Inference (2506.04118) | **proven** approximates soft-BoN optimum | [GSI](https://github.com/j-geuter/GSI) | cheap realization of `q*` | no-grad |
| Twisted SMC (2404.17546) | **proven** consistency + log-Z bounds | [twisted-smc-lm](https://github.com/Silent-Zebra/twisted-smc-lm) | variance + partial-seq credit (twist=value) | mixed |
| TTRL (2504.16084) | empirical; collapse-prone | [TTRL](https://github.com/PRIME-RL/TTRL) | consensus mode collapse (cautionary) | **weight-updating (OUT)** |

## Convergence map — agent level (enlarged no-gradient action space)
| Method | Convergence | Open-source | Cures | Scope |
|---|---|---|---|---|
| **JitRL (2601.18510)** | **proven** (Thm 4.1 exact KL-opt; Thm 4.2/4.3 *asymptotic* consistency, slow-drift) | [JitRL](https://github.com/liushiliushi/JitRL) | credit assignment + β-KL trust region; **OSA-3b anchor** | no-grad |
| LATS (2310.04406) | empirical (UCT guarantee does *not* transfer to LM-valued nodes) | [LATS](https://github.com/lapisrocks/LanguageAgentTreeSearch) | Reflexion plateau; restart/backtrack | no-grad |
| ACE (2510.04618) | **none** (self-admits no analysis) | [ace](https://github.com/ace-agent/ace) | context collapse (delta-update curation) | no-grad |
| AWM (2409.07429) | empirical | [AWM](https://github.com/zorazrw/agent-workflow-memory) | append-only bloat (workflow abstraction) | no-grad |
| Reflexion (2303.11366) | **none** (plateaus) | [reflexion](https://github.com/noahshinn/reflexion) | **OSA-3a anchor** | no-grad |
| Experience-following (2505.16067) | **none** (append-only → error propagation) | [agent_memory_manage](https://github.com/yuplin2333/agent_memory_manage) | curated vs append-only (selective add+delete) | no-grad |
| Memento (2508.16153) | empirical | [Memento](https://github.com/Memento-Teams/Memento) | no-grad-LLM credit (trains a selector) | mixed |

**Net.** Proven agent-level convergence = **JitRL alone** (asymptotic only). All proven finite-N convergence is
output-level. Curation (ACE/AWM/selective-delete) + a β-KL trust region are the empirical cures that *enforce*
the slow-drift precondition JitRL's theorem needs — and that an enlarged speech-agent must adopt.

## Open-source shortlist (training-free, convergence-bearing, usable)
**JitRL** (OSA-3b backbone; exact KL-opt + asymptotic consistency) · **HedgeTune/BoP** (N* over-optimization
controller) · **GSI** (provable cheap soft-BoN) · **Twisted-SMC** (twist=value credit assignment) · **ACE**
(anti-context-collapse curation, *empirical*) · **AWM** (skill-axis curation) · **LATS** (no-grad MCTS, *empirical*).
Caveat: JitRL's convergence is conditional on **uncontaminated memory** — poisoning (2512.16962) / temporal
drift (2605.17830) break the clean-estimator premise; curation is the enforcing mechanism.
