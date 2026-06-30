# θ2 · CV1 — Output-level convergence theory of training-free RL

> Part of **θ2** (convergence survey) of [[2026-06-30-agent-level-synthesis]] / the OptSpace proof (`proofs/tfrl/OptSpace-notes.md`, lemma OSA-3). Run `wf_14ef3acb-2a3`, 2026-06-30. Per-lane adversarial verification; only `keep=true` archived; links real. Each claim tagged **convergence** (proven/empirical/none) · **open_source** · **scope** (no-gradient vs weight-updating).


**Lane summary.** Framing for OSA-3 (inner loop the agent level must preserve): at the model-OUTPUT level, training-free RL realizes the same unified objective q*(z) ∝ q0(z)·exp(R/β), and the literature now gives GENUINE convergence guarantees — but only for the *soft/tilted* family with an explicit trust region (temperature β / N budget). The hard, naive variants do NOT have a monotone true-reward path, and that is the exact inner-loop analog of the agent-level instability the program worries about.

THREE buckets:
(1) PROVEN convergence to the optimal tilted policy q* — Soft-Best-of-N converges at O(1/N) in KL and expected reward with a matching converse, and provably spans the optimal KL–reward Pareto frontier (2505.03156); Best-of-Poisson is a near-exact closed-form optimal-policy approximant (2506.19248); MBR converges at O(N^{-1/2}) to the utility-optimal output (2502.12685); blockwise Controlled Decoding has a KL bound inversely proportional to block size, interpolating BoN↔tokenwise-RL (2310.17022); Guided Speculative Inference provably approximates soft-BoN's optimal tilted policy (2506.04118); CarBoN proves a finite-sample lower-bound improvement on expected reward (2510.15674); Certified Self-Consistency gives anytime-valid concentration that majority vote = the mode of the terminal distribution (2510.17472).
(2) EXACT but NON-monotone: standard hard Best-of-N has an exact KL characterization (true KL ≤ log N − (N−1)/N; win-rate ≤ N/(N+1), 2401.01879) and Gao's scaling laws R_BoN(d)=d(α−βd) (2210.10760), yet under a PROXY reward the true reward rises then FALLS (the over-optimization "hump"/Goodhart). This non-monotonicity is the inner-loop counterexample mirroring naive-rollout non-convergence.
(3) The CURES that restore convergence = trust region + credit/value + over-optimization control: optimal temperature β* on the KL–reward Pareto frontier (soft-BoN), HedgeTune root-finding for the optimal N*/β* that recovers the hacking threshold (2506.19248), the smoothing-lens regret decomposition with a phase transition where soft-BoN provably beats hard-BoN under over-optimization (2507.05913), calibration (CarBoN), and certified/adaptive stopping (MMC, CGES). Weight-updating test-time methods (TTRL, 2504.16084) empirically surpass the maj@n ceiling but are collapse-prone (spurious-consensus mode collapse) — OUT of the no-gradient scope but a clean cautionary mirror of the instability the agent level must avoid. Net for OSA-3: the inner loop is convergent IFF a trust region (β/N) and an over-optimization controller (N*) are present; remove them and even the model-output level loses its monotone path.


**Adversarial verifier assessment.** Strong, well-grounded lane. All 14 claims resolve to REAL papers/repos that I web-verified, including the riskier future-dated 2026 arXiv IDs (ReASC 2601.02970 = Kim et al., Jan 2026; T3RL 2603.02203 = "Tool Verification for Test-Time RL", Mar 2026; CGES 2511.02603) and every open-source artifact (github.com/hskhalaf/hedging, github.com/j-geuter/GSI, github.com/yafuly/TPO, github.com/PRIME-RL/TTRL, HF Space TrustSafeAI/Test-Time-Calibration). Convergence tags are accurate and not overstated: the "proven" claims (CV1-01,02,03,04,05,07,08,09,10) each correspond to an actual theorem/bound in the cited paper, and the "empirical" claims (CV1-06,11,12,13,14) are correctly NOT inflated to proven. The lane's most aggressive theoretical claim (CV1-02: matching converse + Pareto-frontier spanning) initially looked unsupported from the abstract alone, but I confirmed it from the paper HTML (Theorem 2 lower bound; explicit "Soft Best-of-n can provably span the optimal KL-reward Pareto frontier"; Corollary 1 ε-close-in-KL). Scope discipline is clean: no-gradient methods dominate, and the one weight-updating method (CV1-14 TTRL) is explicitly tagged weight-updating / out-of-scope and used only as a cautionary mode-collapse mirror, which is appropriate. Minor non-load-bearing caveats only: a couple of venue attributions (TPO "ICML 2025", TTRL "NeurIPS 2025") and a couple of precise numeric figures (HedgeTune "20-40% gains") and the CGES title wording are approximate/unverified from abstracts, and CV1-09's open_source is a demo HF Space rather than a full code repo — none of which undermine the claims. Keep all 14.


---

## Verified claims (14 kept / 14 total)


### CV1-01-BoN-exact-KL-winrate · conv: **proven** · OSS: no · scope: no-gradient

Standard (hard) Best-of-N has an EXACT analytic characterization: the commonly-cited KL(BoN||ref)=log N−(N−1)/N is only an UPPER BOUND on the true KL, and the win-rate of the BoN policy over the reference is upper-bounded by N/(N+1). These are exact/tight bounds, but they characterize the policy's DRIFT, not any guarantee of improving the TRUE reward.


- **Sources:** [Theoretical guarantees on the best-of-n alignment policy](https://arxiv.org/abs/2401.01879)

- **Relevance (OSA-3):** Quantifies the inner-loop trust-region budget (KL vs N) that the agent level must also respect; the absence of a true-reward monotonicity guarantee here is the seed of the OSA-3 non-convergence counterexample.


### CV1-02-soft-BoN-O1overN-Pareto · conv: **proven** · OSS: no · scope: no-gradient

Soft Best-of-N (a temperature-λ generalization of BoN) PROVABLY converges to the optimal exponentially-tilted distribution q* ∝ q0·exp(R/λ) at rate O(1/N) in both KL and expected reward, with a matching converse showing the rate cannot be improved, and — unlike hard BoN — it provably spans the entire optimal KL–reward Pareto frontier.


- **Sources:** [Soft Best-of-n Sampling for Model Alignment (ISIT 2025)](https://arxiv.org/abs/2505.03156)

- **Relevance (OSA-3):** This is the cleanest model-output realization of the program's q*(z) objective with a PROVEN rate; it shows the trust-region temperature β/λ is what turns search into a convergent, Pareto-optimal procedure — the inner-loop guarantee the agent level should inherit.


### CV1-03-MBR-sqrtN-convergence · conv: **proven** · OSS: no · scope: no-gradient

Minimum Bayes Risk (MBR) decoding converges to the utility-optimal output at rate O(N^{-1/2}) with high probability in the size N of the reference hypothesis set, even though the output space is exponentially larger than N, and is shown to converge faster than MAP decoding in several regimes.


- **Sources:** [Theoretical Guarantees for Minimum Bayes Risk Decoding](https://arxiv.org/abs/2502.12685)

- **Relevance (OSA-3):** MBR is the consensus/aggregation arm of model-output search (the principled cousin of majority vote); its O(N^{-1/2}) rate gives a convergence baseline for memory/skill aggregation when the agent recombines multiple candidates.


### CV1-04-smoothing-lens-regret-phase-transition · conv: **proven** · OSS: no · scope: no-gradient

Under a PROXY (imperfect) reward, soft-BoN's regret decomposes into estimation error + finite-N term + a temperature term, and there is a PHASE TRANSITION: when over-optimization is present, soft-BoN achieves a strictly tighter regret bound than hard BoN. The KL bound is log(N/(1+(N−1)e^{−βR_max})), increasing in β toward log N (recovering hard BoN) as β→∞.


- **Sources:** [Best-of-N through the Smoothing Lens: KL Divergence and Regret Analysis](https://arxiv.org/abs/2507.05913)

- **Relevance (OSA-3):** Formalizes WHY a trust region (finite β*) cures over-optimization at the output level: hard BoN (β→∞) is worst-hit by proxy error. Directly supports OSA-3's 'credit-assigned/regularized rollout converges where naive rollout does not'.


### CV1-05-HedgeTune-BoP-Nstar-overopt-control · conv: **proven** · OSS: yes · scope: no-gradient

Inference-time reward hacking — true reward rising then DECLINING as N (or β) grows — is proven to be an INEVITABLE property of a broad class of inference-time mechanisms (BoN, soft-BoN, Best-of-Poisson). HedgeTune solves a root-finding problem to recover the optimal parameter N*/β* (the hacking threshold), and Best-of-Poisson gives a near-exact closed-form approximation of the optimal reward-KL policy with a single parameter.


- **Sources:** [Inference-Time Reward Hacking in Large Language Models (HedgeTune, BoP)](https://arxiv.org/abs/2506.19248) · [hskhalaf/hedging (official code)](https://github.com/hskhalaf/hedging)

- **Relevance (OSA-3):** The canonical N*/over-optimization controller. OSA-3's 'credit-assigned convergence' has a direct inner-loop instantiation: stop/temperature at N*/β* (root-finding) to stay on the monotone-improving side of the hump.


### CV1-06-Gao-scaling-laws-overopt · conv: **empirical** · OSS: no · scope: mixed

Empirical scaling laws for reward-model over-optimization: gold reward vs KL follows R_BoN(d)=d(α_BoN−β_BoN·d) for best-of-N and R_RL(d)=d(α_RL−β_RL·log d) for RL; BoN consumes far less KL than RL for the same proxy gain, and both eventually turn over (Goodhart). Coefficients scale smoothly with RM size/data.


- **Sources:** [Scaling Laws for Reward Model Overoptimization](https://arxiv.org/abs/2210.10760)

- **Relevance (OSA-3):** The empirical over-optimization 'hump' that motivates N*/trust-region control; BoN's KL-efficiency vs RL argues for no-gradient output search as the convergent inner loop, with the turnover as the instability to be controlled.


### CV1-07-controlled-decoding-blockwise-KL · conv: **proven** · OSS: no · scope: mixed

Controlled Decoding (CD) realizes KL-regularized alignment at inference via a learned prefix-scorer (value function); applied BLOCKWISE it bridges best-of-K and tokenwise RL, with the KL between the blockwise policy and the reference upper-bounded by a function inversely proportional to the block size.


- **Sources:** [Controlled Decoding from Language Models](https://arxiv.org/abs/2310.17022)

- **Relevance (OSA-3):** Shows the SAME q* objective with a value-function/credit-assignment view and a block-size trust region — a model-output template for the agent-level 'value estimation / credit assignment' cure (the scorer is trained, so tagged mixed).


### CV1-08-GSI-provable-soft-BoN-approx · conv: **proven** · OSS: yes · scope: no-gradient

Guided Speculative Inference (GSI) combines soft-best-of-N with a reward model and speculative drafts from a small auxiliary model, and PROVABLY approximates both the optimal tilted policy of soft-BoN under the base model and the expected reward under the optimal policy — while being cheaper than running soft-BoN on the base model.


- **Sources:** [Guided Speculative Inference for Efficient Test-Time Alignment of LLMs](https://arxiv.org/abs/2506.04118) · [j-geuter/GSI (official code)](https://github.com/j-geuter/GSI)

- **Relevance (OSA-3):** Open-source, provably-correct realization of q* at the output level with a cheaper proposal — a concrete pattern for making the convergent inner loop compute-efficient inside the agent.


### CV1-09-CarBoN-finite-sample-lower-bound · conv: **proven** · OSS: yes+repo · scope: no-gradient

CarBoN (Calibrated Best-of-N) adds a test-time calibration phase that learns an input-specific logit temperature T and additive shift δ (model weights FROZEN), with a theoretical guarantee that it improves the LOWER BOUND of the expected reward under finite sampling; empirically up to 4× fewer rollouts for the same accuracy on MATH-500 / AIME-2024.


- **Sources:** [CarBoN: Calibrated Best-of-N Sampling Improves Test-time Reasoning](https://arxiv.org/abs/2510.15674) · [Test-Time-Calibration (HF Space demo)](https://huggingface.co/spaces/TrustSafeAI/Test-Time-Calibration)

- **Relevance (OSA-3):** A monotone-LOWER-BOUND-improvement result at the output level (no weight updates) — the kind of guaranteed-improvement primitive OSA-3 needs; calibrating the proposal is an output-level analog of curating context/memory.


### CV1-10-certified-self-consistency-MMC · conv: **proven** · OSS: no · scope: mixed

Certified Self-Consistency proves majority voting is a statistical CERTIFICATE: under mild assumptions the aggregated answer equals the MODE of the model's terminal distribution with high probability, with finite-sample and anytime-valid concentration bounds; the Martingale Majority Certificate (MMC) is a sequential stopping rule, and test-time RL is shown to exponentially tilt toward the mode, reducing samples needed for certification.


- **Sources:** [Certified Self-Consistency: Statistical Guarantees and Test-Time Training for Reliable Reasoning in LLMs](https://arxiv.org/abs/2510.17472)

- **Relevance (OSA-3):** Gives a PROVEN, anytime-valid stopping rule for the self-consistency/majority arm — directly usable as an inner-loop convergence certificate and a model for when to stop accumulating rollouts at the agent level.


### CV1-11-self-consistency-plateau-adaptive-stopping · conv: **empirical** · OSS: no · scope: no-gradient

Plain self-consistency (majority vote over sampled CoTs) improves with more chains but PLATEAUS with diminishing returns and is blind when all samples share the same wrong answer (no convergence to truth). 2025-2026 adaptive variants add early stopping: CGES gives a Bayesian confidence-guided stopping rule with theoretical guarantees; ReASC aggregates by frequency AND confidence.


- **Sources:** [CGES: Confidence-Guided Early Stopping for Efficient Sampling](https://arxiv.org/abs/2511.02603) · [Reliability-Aware Adaptive Self-Consistency (ReASC)](https://arxiv.org/abs/2601.02970)

- **Relevance (OSA-3):** The plateau + all-wrong blind spot is a concrete inner-loop instability mode (vote can converge to a confident wrong mode); confidence-aware stopping is a cheap cure pattern reusable for agent-level rollout budgets.


### CV1-12-TPO-textual-no-guarantee · conv: **empirical** · OSS: yes+repo · scope: no-gradient

Test-Time Preference Optimization (TPO) aligns a frozen LLM at inference by turning numeric reward into TEXTUAL critiques and iteratively refining the response (no weight updates); it empirically improves alignment and scales with search width AND depth, but offers NO convergence guarantee and can plateau.


- **Sources:** [Test-Time Preference Optimization: On-the-Fly Alignment via Iterative Textual Feedback](https://arxiv.org/abs/2501.12895) · [yafuly/TPO (official code)](https://github.com/yafuly/TPO)

- **Relevance (OSA-3):** Closest output-level analog to the agent's iterative no-gradient refinement (textual 'gradient'); its lack of a convergence guarantee + plateau risk is precisely the Reflexion-plateau failure mode OSA-3 targets — motivates adding credit assignment / trust region.


### CV1-13-compute-optimal-TTS-difficulty-adaptive · conv: **empirical** · OSS: no · scope: mixed

Compute-optimal test-time scaling: allocating test-time compute ADAPTIVELY by prompt difficulty (search vs sequential revision) beats a fixed best-of-N baseline by >4×, and on easy/medium problems a small model + test-time compute can outperform a 14× larger model — but the optimal allocation is difficulty-dependent and empirically tuned, not guaranteed.


- **Sources:** [Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters](https://arxiv.org/abs/2408.03314)

- **Relevance (OSA-3):** Shows the convergent inner-loop strategy is DIFFICULTY-ADAPTIVE — a direct input to agent-level action selection (how many rollouts / which search mode); the lack of a uniform optimum is why a controller (not naive fixed rollout) is needed.


### CV1-14-TTRL-weight-updating-collapse · conv: **empirical** · OSS: yes+repo · scope: weight-updating

TTRL (Test-Time RL) does online RL with a majority-vote pseudo-reward on UNLABELED test data and empirically surpasses the maj@n ceiling (e.g., +211% pass@1 on AIME-2024 for Qwen2.5-Math-7B), but it UPDATES WEIGHTS and is collapse-prone: a spurious high-frequency unverified consensus becomes a self-reinforcing reward, causing incorrect mode collapse; stability depends heavily on reward quality, priors, and data difficulty.


- **Sources:** [TTRL: Test-Time Reinforcement Learning](https://arxiv.org/abs/2504.16084) · [PRIME-RL/TTRL (official code)](https://github.com/PRIME-RL/TTRL) · [Tool Verification for Test-Time Reinforcement Learning (T3RL)](https://arxiv.org/abs/2603.02203)

- **Relevance (OSA-3):** OUT of the no-gradient scope, but the cleanest documented cautionary mirror: a self-reinforcing pseudo-reward causes mode collapse (= the temporal/consensus contamination OSA-3 warns about). Argues for trust-region + verified credit assignment even when one does update; informs why the program prefers no-gradient with controlled rewards.
