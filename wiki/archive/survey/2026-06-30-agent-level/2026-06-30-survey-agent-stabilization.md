> **🗄 ARCHIVED (2026-07-11)** — 已收官战役过程件（2026-06-30 agent-level 调研），仅作历史，非现行真源。

# θ2 · CV3 — Algorithm-level stabilization techniques

> Part of **θ2** (convergence survey) of [[2026-06-30-agent-level-synthesis]] / the OptSpace proof (`proofs/tfrl/OptSpace-notes.md`, lemma OSA-3). Run `wf_14ef3acb-2a3`, 2026-06-30. Per-lane adversarial verification; only `keep=true` archived; links real. Each claim tagged **convergence** (proven/empirical/none) · **open_source** · **scope** (no-gradient vs weight-updating).


**Lane summary.** CV3 surveys the algorithm-level "cures" that restore convergence/stability when the training-free RL action space is enlarged from single-model output search (best-of-N/MBR) to the agent-system level (memory recall · skill invocation · context build · decode). I map each cure to the specific enlarged-space instability it addresses — plateau (Reflexion), context collapse (ACE), temporal memory contamination, and reward-hacking/over-optimization — and tag convergence guarantee + open-source availability + no-gradient/weight-updating scope.

Four cure families emerge, ordered by strength of guarantee:

(1) TRUST-REGION / β control with PROVEN convergence and no-gradient scope: Soft-BoN (2505.03156) provably converges O(1/n) to the tilted target q*∝q0·exp(R/β) and spans the optimal KL–reward Pareto frontier via temperature λ; JitRL (2601.18510) proves its additive logit update is the EXACT closed-form solution of the KL-constrained objective. These directly instantiate the program's q*(z) objective with a guaranteed monotone trade-off knob (β). Soft-BoN has no official repo (trivial to implement); JitRL is open (liushiliushi/JitRL, research-license).

(2) OVER-OPTIMIZATION CONTROL (N*/HedgeTune): 2506.19248 proves the increase-then-decline true-reward pattern is INEVITABLE for BoN/BoP and gives HedgeTune to compute the optimal inference parameter (the N* sweet spot), with open code (hskhalaf/hedging). Grounded by BoN KL theory (2401.01879, 2507.05913), scaling laws (2210.10760: BoN over-opt is quadratic in √KL), and MBR guarantees (2502.12685: O(n^-1/2)). These give the closed-form curves the OSA-3 Lean theorem can use to characterize where naive optimization over-shoots.

(3) VARIANCE REDUCTION + CREDIT ASSIGNMENT — the core of restoring a monotone path in the enlarged space: Twisted SMC (2404.17546, ICML'24 Best Paper, open Silent-Zebra/twisted-smc-lm) uses learned twists as per-step value/control-variate estimates with proven SMC consistency and log-Z bounds; FK-steering (2501.06848, open) and Particle-Gibbs PG-DLM (2507.08390, proven consistency+variance bounds) add resampling-based variance control. The control-variate/baseline idea is canonical: RLOO/GRPO leave-one-out group baselines (2402.14740) are unbiased variance reducers — weight-updating as algorithms, but the BASELINE technique transfers directly to no-gradient retrieval-advantage estimation (JitRL). Classical CRN/control-variates (Greensmith JMLR'04) reduce covariance between compared rollouts, stabilizing action comparison. JitRL's retrieval-advantage is the concrete no-gradient credit-assignment cure with a convergence proof — the program's anchor for "credit-assigned convergence vs naive-rollout non-convergence."

(4) STRUCTURED/CURATED MEMORY anti-collapse (empirical, no formal guarantee, but open-source): ACE (2510.04618, open ace-agent/ace) cures context collapse via incremental delta updates with dedup/prune instead of monolithic rewrite; AWM (2409.07429, open zorazrw) abstracts reusable workflows to fight append-only bloat. LATS (2310.04406, open lapisrocks) adds tree search + reflection + MC value backup (gradient-free credit assignment + restart/backtrack) curing the Reflexion plateau (2303.11366, open noahshinn, NO convergence guarantee). Temporal-memory-contamination cures (SSGM/constitutional reranking) are governance-layer and empirical-only.

Net: PROVEN convergence exists ONLY for output-level/value-augmented samplers (soft-BoN, twisted SMC, PG-DLM, MBR) and JitRL's closed-form logit update; agent-level memory/search cures (ACE, AWM, LATS) are open-source but EMPIRICAL — exactly the gap OSA-3 targets. Reflexion-style naive rollout has NO guarantee and plateaus (the counterexample side); JitRL-style retrieval credit assignment is the proven-convergence side.


**Adversarial verifier assessment.** CV3 ("stabilization") is well-grounded and survives adversarial verification: all 14 claims' sources resolve to REAL arXiv papers and REAL public GitHub repos. I directly verified the existence of every cited repo (liushiliushi/JitRL, hskhalaf/hedging, ace-agent/ace, Silent-Zebra/twisted-smc-lm, zacharyhorvitz/Fk-Diffusion-Steering, zorazrw/agent-workflow-memory, lapisrocks/LanguageAgentTreeSearch, noahshinn/reflexion) and confirmed the future-dated papers are genuinely indexed, not fabricated (JitRL 2601.18510, MemoryGraft 2512.16962, SSGM 2603.11768, all real). The convergence-tag stratification is honest and matches the program's central thesis: 'proven' is reserved for output-level/value-augmented samplers with genuine mathematical results (soft-BoN O(1/n) confirmed in abstract; 2401.01879 KL-upper-bound + win-rate ≤ n/(n+1) confirmed; MBR O(n^-1/2) confirmed; JitRL closed-form KL-optimum confirmed; PG-DLM asymptotic consistency confirmed), while agent-level memory/search cures (ACE, AWM, LATS) are correctly tagged 'empirical' and Reflexion + temporal-contamination correctly 'none' — exactly the missing-guarantee gap OSA-3 formalizes. All 14 kept.

Corrections/caveats the survey should fold in (none rise to keep=false): (1) FACTUAL ERROR — twisted SMC 2404.17546 was an ICML 2024 ORAL, not a 'Best Paper'; remove the award label in both the CV3 summary and the claim evidence. (2) Soft-BoN's 'matching converse lower bound' and 'spans the optimal KL-reward Pareto frontier' are body-level claims not in the abstract — verify against the full PDF before presenting as established. (3) JitRL's 'proven' is solid for the closed-form KL-constrained optimum, but the broader 'policy converges to the optimal policy' is CONDITIONAL on retrieval/coverage assumptions — state it as conditional. (4) cv3-fk-pg's 'proven' rests entirely on PG-DLM (2507.08390); FK steering itself is the empirical half. (5) cv3-baselines-controlvariates is correctly scoped weight-updating and its 'proven' denotes unbiased variance-reduction, not an agent-loop convergence rate — keep that distinction explicit. Net: the proven-convergence-vs-naive-rollout dichotomy the lane draws (JitRL/soft-BoN/twisted-SMC/HedgeTune proven; Reflexion/ACE/LATS empirical-or-none) is accurate and load-bearing for the OSA-3 theorem.


---

## Verified claims (14 kept / 14 total)


### cv3-softbon-trustregion · conv: **proven** · OSS: no (no official repo located; algorithm is a few-line reweighting; reference toy BoN at https://github.com/saschaschramm/best-of-n-sampling) · scope: no-gradient

Soft Best-of-N replaces hard argmax selection with a temperature-λ tilt, provably converging at rate O(1/n) (in both KL and expected relative reward, with a matching converse lower bound) to the optimal tilted distribution q*∝q0·exp(R/β), and unlike hard BoN it can span the entire optimal KL–reward Pareto frontier — making λ an inference-time trust-region/β knob.


- **Sources:** [Soft Best-of-n Sampling for Model Alignment](https://arxiv.org/abs/2505.03156)

- **Relevance (OSA-3):** Directly supplies a PROVEN-convergent, monotone β/temperature trust region for the q* target; the cure for over-optimization/reward-hacking at the OUTPUT level that OSA-3 extends to the agent level.


### cv3-jitrl-creditassignment · conv: **proven** · OSS: yes (https://github.com/liushiliushi/JitRL — research-only license; runnable Jericho + WebArena agents, retrieval+advantage logic in src/jitrl_agent.py & cross_episode_memory.py) · scope: no-gradient

JitRL performs no-gradient test-time policy optimization by retrieving past <state,action,reward> trajectories (Jaccard/N-gram similarity), estimating action advantages on-the-fly, and additively modulating output logits; the paper proves this additive logit update is the EXACT closed-form solution of the KL-constrained policy-optimization objective and that the retrieval value estimates converge to true values, so the policy converges to the optimal policy.


- **Sources:** [Just-In-Time Reinforcement Learning: Continual Learning in LLM Agents Without Gradient Updates](https://arxiv.org/abs/2601.18510) · [JitRL official code (liushiliushi/JitRL)](https://github.com/liushiliushi/JitRL)

- **Relevance (OSA-3):** THE core CV3 cure: a no-gradient credit-assignment mechanism with a closed-form KL-trust-region update and a convergence proof — the 'credit-assigned convergence' half of the OSA-3 theorem, contrasted against Reflexion's non-convergent naive rollout.


### cv3-hedgetune-nstar · conv: **proven** · OSS: yes (https://github.com/hskhalaf/hedging — BoN/SBoN/BoP implementations, HedgeTune, demos) · scope: no-gradient

Inference-time reward hacking (true reward rises then declines as the proxy is over-optimized) is proven INEVITABLE for a broad class of mechanisms including BoN and Best-of-Poisson; HedgeTune computes the optimal inference-time parameter (the N*/temperature sweet spot) that hedges the proxy and prevents true-reward degradation, with minimal overhead.


- **Sources:** [Inference-Time Reward Hacking in Large Language Models (HedgeTune, BoP)](https://arxiv.org/abs/2506.19248) · [HedgeTune / hedging code (hskhalaf/hedging)](https://github.com/hskhalaf/hedging)

- **Relevance (OSA-3):** Cures reward-hacking/over-optimization by computing N* analytically; the inevitability proof is a ready-made ingredient for the OSA-3 'naive optimization overshoots' counterexample, and HedgeTune is the matching corrective control.


### cv3-bon-kl-theory · conv: **proven** · OSS: no (theoretical; KL estimator is a short formula, no dedicated repo located) · scope: no-gradient

Best-of-N KL/regret theory gives the closed forms needed to size the over-optimization headroom: the popular KL(BoN‖ref)=log n−(n−1)/n is only an UPPER bound (2401.01879 disproves equality, gives a tighter estimator and win-rate ≤ n/(n+1)); the smoothing-lens analysis (2507.05913) derives KL-divergence and regret bounds for BoN as a function of n.


- **Sources:** [Theoretical guarantees on the best-of-n alignment policy](https://arxiv.org/abs/2401.01879) · [Best-of-N through the Smoothing Lens: KL Divergence and Regret Analysis](https://arxiv.org/abs/2507.05913)

- **Relevance (OSA-3):** Supplies exact KL/regret closed forms that bound the enlarged action space's optimization headroom; load-bearing math for the OSA-3 trade-off characterization (how much R one can buy per unit KL/β).


### cv3-mbr-guarantee · conv: **proven** · OSS: no (theory; MBR-BoN baseline code exists in various decoding libs but no single canonical repo verified here) · scope: no-gradient

MBR decoding (and regularized MBR-BoN) selects the consensus/expected-utility candidate rather than the proxy argmax, and is proven to approach the optimal solution with high probability at rate O(n^-1/2) even though the output space is far larger than n — a variance-reducing, reward-hacking-resistant alternative to hard BoN.


- **Sources:** [Theoretical Guarantees for Minimum Bayes Risk Decoding](https://arxiv.org/abs/2502.12685) · [Regularized Best-of-N Sampling with Minimum Bayes Risk Objective for LM Alignment](https://arxiv.org/abs/2404.01054)

- **Relevance (OSA-3):** An output-level cure that trades argmax for consensus/utility, reducing proxy-reward variance and resisting reward-hacking with a convergence rate; complements HedgeTune as the aggregation-based over-optimization control.


### cv3-twisted-smc-varreduction · conv: **proven** · OSS: yes (https://github.com/Silent-Zebra/twisted-smc-lm) · scope: mixed

Twisted Sequential Monte Carlo casts inference-time alignment as sampling the unnormalized target q*∝q0·exp(R/β) and learns per-timestep 'twist' functions that estimate the expected future potential (a value function / control variate), focusing computation on promising partial sequences; SMC gives asymptotic consistency and the method provides bidirectional bounds on log-Z to evaluate inference accuracy.


- **Sources:** [Probabilistic Inference in Language Models via Twisted Sequential Monte Carlo](https://arxiv.org/abs/2404.17546) · [twisted-smc-lm official code (Silent-Zebra)](https://github.com/Silent-Zebra/twisted-smc-lm)

- **Relevance (OSA-3):** Principled variance-reduction + partial-sequence credit assignment for the exact q* target; the twist-as-value idea is the bridge from output-level sampling to the value-guided credit assignment OSA-3 needs in the enlarged space.


### cv3-fk-pg-resampling · conv: **proven** · OSS: yes for FK steering (https://github.com/zacharyhorvitz/Fk-Diffusion-Steering); PG-DLM — no public repo located · scope: no-gradient

Particle/resampling samplers add variance control and anti-degeneracy at inference time: Feynman-Kac steering (2501.06848) runs interacting particles, scores them with reward potentials, and resamples at intermediate steps to steer toward arbitrary (non-differentiable) rewards; Particle-Gibbs PG-DLM (2507.08390) builds a Markov chain over full trajectories via a conditional-SMC kernel with PROVEN asymptotic consistency and variance bounds, mitigating particle degeneracy/collapse.


- **Sources:** [A General Framework for Inference-time Scaling and Steering of Diffusion Models (FK steering)](https://arxiv.org/abs/2501.06848) · [FK-Diffusion-Steering code (zacharyhorvitz)](https://github.com/zacharyhorvitz/Fk-Diffusion-Steering) · [Inference-Time Scaling of Diffusion Language Models with Particle Gibbs Sampling (PG-DLM)](https://arxiv.org/abs/2507.08390)

- **Relevance (OSA-3):** Resampling-based variance reduction + diversity/restart that targets reward-tilted distributions with consistency guarantees; the anti-degeneracy mechanism cures the 'particle/sample collapse' analogue of agent-space context collapse.


### cv3-baselines-controlvariates · conv: **proven** · OSS: yes (RLOO/GRPO in TRL https://github.com/huggingface/trl and verl https://github.com/volcengine/verl) · scope: weight-updating

Leave-one-out / group-relative baselines (RLOO, GRPO) are unbiased control-variate variance reducers — each sample's reward is compared against the average of the other k−1 samples, an on-the-fly parameter-free value function that lowers advantage variance without bias; the classical control-variate and common-random-number (CRN) results underpin this and CRN additionally reduces COVARIANCE between compared rollouts to stabilize action comparison.


- **Sources:** [Back to Basics: Revisiting REINFORCE Style Optimization (RLOO)](https://arxiv.org/abs/2402.14740) · [Variance Reduction Techniques for Gradient Estimates in RL (Greensmith, Bartlett, Baxter, JMLR 2004)](https://www.jmlr.org/papers/volume5/greensmith04a/greensmith04a.pdf)

- **Relevance (OSA-3):** Identifies the variance-reduction primitive (leave-one-out baseline + CRN) that a no-gradient agent loop should adopt for stable advantage estimates; clarifies what part of GRPO/RLOO is in-scope (the baseline) vs out-of-scope (the gradient step).


### cv3-overopt-scalinglaws · conv: **empirical** · OSS: no (synthetic-setup study, no public reference implementation located) · scope: mixed

Reward-model over-optimization follows characteristic functional forms: as the proxy is optimized, gold reward rises then falls (Goodhart), with BoN over-optimization fitting a QUADRATIC in √KL and RL a logarithmic form; RL consumes far more KL than BoN for the same optimization — quantifying the over-optimization the trust-region/N* cures must bound.


- **Sources:** [Scaling Laws for Reward Model Overoptimization](https://arxiv.org/abs/2210.10760)

- **Relevance (OSA-3):** Empirical backbone for why over-optimization control is needed; the BoN-quadratic-in-√KL form is a concrete curve OSA-3 can cite when arguing naive optimization in the enlarged space overshoots the true objective.


### cv3-ace-deltamemory · conv: **empirical** · OSS: yes (https://github.com/ace-agent/ace and ACE+AppWorld https://github.com/ace-agent/ace-appworld) · scope: no-gradient

ACE cures 'context collapse' (iterative monolithic rewriting that erodes detail and drops domain insight) by treating context as an evolving playbook updated with STRUCTURED INCREMENTAL DELTA entries (Generator→Reflector→Curator), each with helpful/harmful counters and deterministic merge/dedup/prune — preserving detail instead of overwriting it.


- **Sources:** [Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models](https://arxiv.org/abs/2510.04618) · [ACE code (ace-agent/ace)](https://github.com/ace-agent/ace)

- **Relevance (OSA-3):** The canonical CURE for the context-collapse instability of the enlarged agent space; open-source but EMPIRICAL-only — precisely the missing-guarantee gap OSA-3 aims to formalize (structured/curated memory vs append-only).


### cv3-awm-structuredmemory · conv: **empirical** · OSS: yes (https://github.com/zorazrw/agent-workflow-memory) · scope: no-gradient

Agent Workflow Memory cures append-only memory bloat by INDUCING reusable abstract workflows (routines) from past trajectories and selectively injecting them to guide future actions, applicable offline and online — a curated/structured-memory alternative that compounds skill reuse.


- **Sources:** [Agent Workflow Memory](https://arxiv.org/abs/2409.07429) · [AWM code (zorazrw/agent-workflow-memory)](https://github.com/zorazrw/agent-workflow-memory)

- **Relevance (OSA-3):** Structured-memory cure that partially addresses plateau/contamination by abstracting and curating skills (the 'which skill to invoke' axis of the agent action z); open-source, empirical-only.


### cv3-lats-treesearch · conv: **empirical** · OSS: yes (https://github.com/lapisrocks/LanguageAgentTreeSearch; also LangGraph and LlamaIndex implementations) · scope: no-gradient

LATS adds MCTS-style tree search to LLM agents — action sampling, an LM value function, self-reflection, UCB-balanced exploration, and Monte-Carlo value backpropagation with backtracking/restart — providing gradient-free credit assignment and structured search that outperforms ReAct/Reflexion/ToT; performance is empirical (UCT heuristics, no convergence proof for LM value functions).


- **Sources:** [Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models](https://arxiv.org/abs/2310.04406) · [LATS official code (lapisrocks/LanguageAgentTreeSearch)](https://github.com/lapisrocks/LanguageAgentTreeSearch)

- **Relevance (OSA-3):** The restart/beam/tree-search + MC-value credit-assignment cure for the plateau instability; demonstrates structured search restores improvement where linear rollout stalls, but lacks the guarantee OSA-3 seeks.


### cv3-reflexion-plateau · conv: **none** · OSS: yes (https://github.com/noahshinn/reflexion) · scope: no-gradient

Reflexion (verbal RL) converts feedback into textual self-reflection appended to episodic memory as a 'semantic gradient' over trials; it is no-gradient and open-source but has NO formal convergence guarantee — feedback quality varies and there is no assurance the iterative loop steers toward correct outcomes, exhibiting the plateau the program cites.


- **Sources:** [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) · [Reflexion code (noahshinn/reflexion)](https://github.com/noahshinn/reflexion)

- **Relevance (OSA-3):** The canonical NON-CONVERGENT naive-rollout baseline (plateau) that motivates the OSA-3 counterexample; the foil that credit-assigned methods (JitRL/LATS/twisted SMC) are measured against.


### cv3-temporal-contamination · conv: **none** · OSS: no (no public reference implementation of the defenses located) · scope: no-gradient

Temporal memory contamination — benign accumulation, later retrieval at a trigger, then unsafe transfer via the agent's tendency to imitate retrieved successful traces — degrades long-horizon agent stability; proposed cures are governance-layer (constitutional-consistency reranking that penalizes traces diverging from a safety constitution, cryptographic provenance attestation, and stability/safety-governed memory frameworks), and are empirical only.


- **Sources:** [How Memory Management Impacts LLM Agents: Empirical Study of Experience-Following](https://arxiv.org/abs/2505.16067) · [Governing Evolving Memory in LLM Agents (SSGM Framework)](https://arxiv.org/abs/2603.11768) · [MemoryGraft: Persistent Compromise of LLM Agents via Poisoned Experience Retrieval](https://arxiv.org/abs/2512.16962)

- **Relevance (OSA-3):** Names and partially cures the 'temporal memory contamination' instability of the enlarged memory-recall action axis; reranking/curation that penalizes divergent retrieved traces is the contamination analogue of curated-memory anti-collapse, but lacks any convergence guarantee — another gap OSA-3 can target.
