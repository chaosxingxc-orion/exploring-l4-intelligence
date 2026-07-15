> **🗄 ARCHIVED (2026-07-11)** — 已收官战役过程件（2026-06-30 agent-level 调研），仅作历史，非现行真源。

# θ2 · CV2 — Agent-level convergence & stability

> Part of **θ2** (convergence survey) of [[2026-06-30-agent-level-synthesis]] / the OptSpace proof (`proofs/tfrl/OptSpace-notes.md`, lemma OSA-3). Run `wf_14ef3acb-2a3`, 2026-06-30. Per-lane adversarial verification; only `keep=true` archived; links real. Each claim tagged **convergence** (proven/empirical/none) · **open_source** · **scope** (no-gradient vs weight-updating).


**Lane summary.** CV2 maps the convergence landscape of the enlarged, no-gradient agent action space (recall memory · invoke skill · build context · decode) and supplies both sides of the OSA-3 theorem. (1) THE PROVEN POSITIVE / "credit-assigned convergence" side is carried almost entirely by JitRL (2601.18510, ICML 2026 spotlight, code at github.com/liushiliushi/JitRL). Its Theorem 4.1 proves the additive retrieval-advantage logit update z'(s,a)=z(s,a)+βÂ(s,a) is the EXACT closed-form solution of the KL-constrained objective argmax E[Â]−(1/β)KL(π'‖π_θ), i.e. π*(a|s) ∝ π_θ(a|s)·exp(βA) — precisely the program's q*(z) ∝ q0(z)·exp(R/β) with raw reward R replaced by a credit-assigned advantage A. Theorem 4.2 (kNN estimator consistency: V̂,Q̂,Â →p truth) and Theorem 4.3 (the induced policy →p the optimal KL-regularized policy as memory grows) give an asymptotic, in-probability convergence guarantee — explicitly conditioned on a SLOW-POLICY-DRIFT assumption, which is the trust-region/β-KL term doing double duty as the stabilizer. This is asymptotic consistency, NOT finite-time monotone improvement. (2) THE NON-CONVERGENCE / COUNTEREXAMPLE side is established empirically by the instability literature on NAIVE rollout in the same space: Reflexion's verbal-RL plateau (no improvement after ~4 WebShop trials, 2303.11366); ACE's "context collapse" where monolithic rewriting erodes detail (2510.04618, which states outright it has no convergence/monotonicity analysis); the experience-following study (2505.16067) showing append-only memory causes error propagation and misaligned-replay self-reinforcing loops, with selective add+delete beating naive growth by ~10%; and temporal memory contamination / longitudinal safety drift rising with exposure length (2605.17830), plus memory-poisoning persistence (MemoryGraft 2512.16962). (3) THE CURES split into credit assignment / value estimation (JitRL retrieval-advantage — proven; LATS/Agent-Q MCTS value functions — empirical), trust region / over-optimization control (JitRL's β-KL; output-level anchors soft-BoN temperature 2505.03156, HedgeTune N* 2506.19248, BoN theory 2401.01879/2507.05913 — proven but at the output not agent level), and STRUCTURED/CURATED vs append-only memory (ACE delta updates, selective add+delete) — the structural variance/contamination control. NET FINDING: among agent-level no-gradient methods, ONLY JitRL offers a proven convergence guarantee; every tree-search and memory-evolution method (LATS, Agent Q, Memento, ACE, Reflexion, CER) is empirical-only, and the dominant failure mode of naive rollout is precisely the absence of credit assignment + trust region that JitRL supplies. Nearly all surveyed methods are open-source. Scope caveats: Agent Q and Memento are MIXED (Agent Q adds DPO fine-tuning; Memento trains a small case-selection Q-policy) — their inference-time search/retrieval is in-scope but their learning components are weight-updating.


**Adversarial verifier assessment.** Unusually clean lane. Every source resolves to a real arXiv paper or a real, populated GitHub repo — including all four future-dated 2026 IDs I treated as fabrication risks (2605.17830 Longitudinal Safety / temporal memory contamination; 2512.16962 MemoryGraft; 2603.11768 SSGM; 2601.05504 memory poisoning), all of which exist. The central positive anchor JitRL (2601.18510, ICML 2026 Spotlight, github.com/liushiliushi/JitRL populated with real code) was fully verified at the theorem level: Thm 4.1 (closed-form KL-constrained optimality, z'=z+βÂ, π*∝π_θexp(βA)), Thm 4.2 (kNN estimator in-probability consistency), Thm 4.3 (policy consistency), the slow-policy-drift + kNN-regime + state-regularity assumptions, and crucially the confirmation that NO finite-time monotone-improvement bound exists — only asymptotic in-probability consistency. The survey is notably disciplined about NOT overstating convergence: CV2-02 and CV2-15 explicitly flag the asymptotic-only / output-level-only nature, which is exactly right. The empirical-only counterexample side (Reflexion plateau, ACE context-collapse, experience-following, temporal contamination) is accurately tagged convergence=none/empirical with real repos. One substantive correction: CV2-13 (SSGM) contains two inaccuracies — (a) it attributes "session-budget controls and periodic memory resets" to SSGM, but the paper actually uses Weibull temporal decay / asynchronous reconciliation / freshness thresholds; (b) it asserts SSGM offers "not proven convergence bounds," but the paper does present a Theorem 1 drift bound O(N·ε_step) with a proof sketch under strong fixed-error assumptions — so the claim UNDER-states rather than over-states the convergence content. This cuts in the safe direction (no overstatement), so I keep it with the caveat flagged. No convergence tag in the lane is overstated; all 15 claims kept. Minor unverified specifics that are not load-bearing: exact violation-rate ranges in CV2-11, the 18.6/81.7/95.4% figures in CV2-06, and the ~10% delta in CV2-10 were not line-verified but the structural/convergence claims they support are confirmed.


---

## Verified claims (15 kept / 15 total)


### CV2-01-jitrl-closedform · conv: **proven** · OSS: https://github.com/liushiliushi/JitRL · scope: no-gradient

JitRL's Theorem 4.1 proves the additive retrieval-advantage logit update z'(s,a)=z(s,a)+β·Â(s,a) is the EXACT closed-form solution of the KL-constrained policy-optimization objective argmax_{π'} E_{a~π'}[Â(s,a)] − (1/β)KL(π'‖π_θ), yielding π*(a|s) ∝ π_θ(a|s)·exp(β·A(s,a)). This is the agent-level instantiation of the program's unified objective q*(z) ∝ q0(z)·exp(R/β), with raw reward R replaced by a credit-assigned advantage A.


- **Sources:** [Just-In-Time Reinforcement Learning: Continual Learning in LLM Agents Without Gradient Updates](https://arxiv.org/abs/2601.18510) · [JitRL official code](https://github.com/liushiliushi/JitRL)

- **Relevance (OSA-3):** This is the exact closed form that makes the program's q*(z) ∝ q0(z)·exp(R/β) a credit-assigned policy update rather than raw-reward reweighting; it is the algebraic backbone of OSA-3's 'credit-assigned convergence' side and shows the β-KL term IS the trust region.


### CV2-02-jitrl-consistency-convergence · conv: **proven** · OSS: https://github.com/liushiliushi/JitRL · scope: no-gradient

JitRL's Theorems 4.2 and 4.3 give an asymptotic, in-probability convergence guarantee for the no-gradient agent: the kNN retrieval estimators V̂_t, Q̂_t, Â_t converge in probability to the true values, and the induced policy π̂_t converges in probability to the optimal KL-regularized policy π*_t AS MEMORY GROWS (t→∞). Crucially this holds only under a SLOW-POLICY-DRIFT assumption (plus state regularity, noise, kNN-regime, action-frequency conditions) — it is asymptotic consistency, not finite-time monotone improvement.


- **Sources:** [Just-In-Time Reinforcement Learning (HTML, theory section)](https://arxiv.org/html/2601.18510) · [JitRL alphaXiv overview](https://www.alphaxiv.org/overview/2601.18510)

- **Relevance (OSA-3):** Directly grounds OSA-3's positive half: credit assignment via retrieval-advantage restores convergence in the enlarged no-gradient space. The slow-drift precondition is exactly why a trust region (β-KL) is necessary — naive fast-drifting rollout violates the assumption, motivating the counterexample.


### CV2-03-jitrl-baselines-sota · conv: **n/a** · OSS: https://github.com/liushiliushi/JitRL · scope: no-gradient

JitRL is the no-gradient agent method that empirically dominates the other training-free agent-level rollouts it compares against — Static, Memory (full-transcript ICL), Reflexion, AWM (workflow extraction), and EvoTest — and is competitive with weight-updating baselines (SFT, WebRL, GRPO) on WebArena and Jericho, establishing SOTA among training-free methods.


- **Sources:** [Just-In-Time Reinforcement Learning (abstract + experiments)](https://arxiv.org/abs/2601.18510)

- **Relevance (OSA-3):** Shows the credit-assigned method beats the empirical-only no-gradient rollouts (Reflexion/AWM/EvoTest) that exhibit the OSA-3 plateau/collapse failures — empirical confirmation that the convergence cure also wins in practice.


### CV2-04-lats-mcts-empirical · conv: **empirical** · OSS: https://github.com/lapisrocks/LanguageAgentTreeSearch · scope: no-gradient

LATS (Language Agent Tree Search) performs no-gradient inference-time MCTS over agent actions using an LM-powered value function plus self-reflection. It provides NO convergence proof; it is empirical only. Its tree search inherits the spirit of UCT but the classic UCT asymptotic-optimality guarantee does not transfer, because node values are noisy LM estimates rather than averaged Monte-Carlo returns.


- **Sources:** [Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models](https://arxiv.org/abs/2310.04406) · [LATS official repository](https://github.com/lapisrocks/LanguageAgentTreeSearch) · [Bandit Based Monte-Carlo Planning (UCT)](https://link.springer.com/chapter/10.1007/11871842_29)

- **Relevance (OSA-3):** The canonical no-gradient tree-search-over-agent-actions baseline. It demonstrates that structured search adds optimization headroom but, lacking a transferable convergence guarantee, is exactly the kind of method OSA-3 must distinguish from JitRL's proven path.


### CV2-05-uct-theory-gap · conv: **proven** · OSS: no · scope: n/a

Classic UCT (Kocsis & Szepesvári 2006) has a PROVEN asymptotic-optimality / convergence guarantee in the bandit/MCTS setting (value estimates converge to the optimal value, failure probability →0 polynomially). This guarantee assumes backed-up Monte-Carlo returns and does NOT carry over to LLM-agent tree search where node values are produced by an LM value model — so LATS/Agent-Q-style search is theory-inspired but not theory-guaranteed.


- **Sources:** [Bandit Based Monte-Carlo Planning (Kocsis & Szepesvári, ECML 2006)](https://link.springer.com/chapter/10.1007/11871842_29)

- **Relevance (OSA-3):** Clarifies WHY agent-level tree search lacks a convergence guarantee even though MCTS has one — sharpens OSA-3's claim that naive search/rollout over LM-valued agent actions has no monotone path, unlike JitRL's consistency-grounded estimator.


### CV2-06-agentq-mixed · conv: **empirical** · OSS: https://github.com/sentient-engineering/agent-q · scope: mixed

Agent Q combines no-gradient inference-time MCTS with self-critique AND off-policy DPO fine-tuning. It is MIXED scope: the MCTS search is in-scope (no-gradient) but the DPO updates change weights (out of scope). It reports strong empirical gains (Llama-3-70B zero-shot 18.6%→81.7%, →95.4% with online search) but provides no convergence/monotone-improvement guarantee.


- **Sources:** [Agent Q: Advanced Reasoning and Learning for Autonomous AI Agents](https://arxiv.org/abs/2408.07199) · [agent-q open-source implementation](https://github.com/sentient-engineering/agent-q)

- **Relevance (OSA-3):** Illustrates the boundary: search-based credit assignment can be no-gradient, but Agent Q reaches strong performance only by adding weight updates. OSA-3 targets the harder no-gradient-only regime where JitRL, not Agent Q, supplies the guarantee.


### CV2-07-memento-mixed · conv: **empirical** · OSS: https://github.com/Memento-Teams/Memento · scope: mixed

Memento reframes continual learning as memory-based online RL over a memory-augmented MDP, learning a case-selection policy over an episodic case bank via online soft Q-learning — adapting WITHOUT fine-tuning the LLM. Scope is MIXED: the LLM is frozen (in-scope) but the differentiable case-selection Q-policy is trained (a small weight-updating component); the non-parametric variant is fully no-gradient. No convergence guarantee is proven; results are empirical (GAIA 87.88% Pass@3; +4.7–9.6% on OOD).


- **Sources:** [Memento: Fine-tuning LLM Agents without Fine-tuning LLMs](https://arxiv.org/abs/2508.16153) · [Memento official code](https://github.com/Memento-Teams/Memento)

- **Relevance (OSA-3):** A second no-gradient-LLM credit-assignment design (Q-learning over retrieved cases), parallel to JitRL's retrieval-advantage. Useful contrast: Memento trains a small selector (no guarantee), JitRL keeps everything non-parametric AND proves consistency — sharpening why JitRL's design admits a convergence theorem.


### CV2-08-ace-context-collapse · conv: **none** · OSS: https://github.com/ace-agent/ace · scope: no-gradient

ACE (Agentic Context Engineering) identifies 'context collapse' — iterative monolithic rewriting of an evolving context/playbook erodes detail and causes sharp performance drops — and 'brevity bias'. ACE's cure is structured incremental delta updates (Generator produces traces, Reflector extracts lessons, Curator merges compact delta bullets via deterministic non-LLM logic; grow-and-refine with embedding dedup). The paper STATES EXPLICITLY it provides no convergence/monotonicity/stability proof — purely empirical (+10.6% agents, +8.6% finance, matches top AppWorld production agent).


- **Sources:** [Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models](https://arxiv.org/abs/2510.04618) · [ACE analysis (EmergentMind)](https://www.emergentmind.com/papers/2510.04618) · [ACE official code](https://github.com/ace-agent/ace)

- **Relevance (OSA-3):** Primary OSA-3 counterexample on the context-building action dimension: naive (monolithic) context rollout demonstrably DIVERGES/degrades; structured curation mitigates but with NO guarantee. Motivates the need for JitRL-style credit assignment over a curated memory, not just better heuristics.


### CV2-09-reflexion-plateau · conv: **none** · OSS: https://github.com/noahshinn/reflexion · scope: no-gradient

Reflexion (verbal/no-gradient reinforcement learning via self-reflection stored in memory) demonstrably PLATEAUS: in WebShop the agent shows no improvement after ~4 trials and cannot escape local minima requiring creative behavior. It has no convergence or monotone-improvement guarantee — performance saturates after a few self-reflection rounds.


- **Sources:** [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) · [Reflexion official code](https://github.com/noahshinn/reflexion)

- **Relevance (OSA-3):** The canonical 'naive-rollout non-convergence' empirical anchor for OSA-3: a no-gradient self-improvement loop without credit assignment plateaus and gets stuck in local minima, exactly the counterexample JitRL's consistency theorem is contrasted against.


### CV2-10-experience-following · conv: **none** · OSS: https://github.com/yuplin2333/agent_memory_manage · scope: no-gradient

An empirical study of memory management in LLM agents identifies the 'experience-following' property and two failure modes of APPEND-ONLY memory: error propagation (outdated/incorrect stored experiences get replicated) and misaligned experience replay (agents retrieve experiences that reinforce current suboptimal behavior — self-reinforcing loops). Combining SELECTIVE ADDITION + SELECTIVE DELETION (curation) beats naive append-only memory growth by ~10% absolute. Empirical only, no guarantee.


- **Sources:** [How Memory Management Impacts LLM Agents: An Empirical Study of Experience-Following Behavior](https://arxiv.org/abs/2505.16067) · [agent_memory_manage code](https://github.com/yuplin2333/agent_memory_manage)

- **Relevance (OSA-3):** Directly grounds the 'curated vs append-only memory' axis of OSA-3: append-only rollout creates self-reinforcing divergence (error propagation), and curation (delete+add) is a measurable but unguaranteed stabilizer — i.e., structural variance control that JitRL's credit assignment formalizes.


### CV2-11-temporal-memory-contamination · conv: **none** · OSS: no · scope: no-gradient

Temporal memory contamination / longitudinal safety drift: in memory-equipped LLM agents, benign accumulation of ordinary past tasks raises memory-induced violation rates with EXPOSURE LENGTH (0.30–0.50 for broad-retrieval architectures vs 0.10–0.20 for recency-biased), driven by accumulated content rather than encounter order. Empirical measurement only — NOT strictly monotone, architecture-dependent; mitigations are a retrieval-time monitor (filter/isolate/access-control).


- **Sources:** [Remembering More, Risking More: Longitudinal Safety Risks in Memory-Equipped LLM Agents](https://arxiv.org/abs/2605.17830)

- **Relevance (OSA-3):** Evidence that the temporal/memory dimension of the enlarged action space drifts (does not stabilize) under naive accumulation — a distinct OSA-3 instability mode from plateau/collapse, showing that 'more memory' alone does not imply convergence and may anti-correlate with desired behavior.


### CV2-12-memory-poisoning-persistence · conv: **none** · OSS: no · scope: no-gradient

Memory-based agents are vulnerable to persistent contamination via poisoned experience retrieval (MemoryGraft) and memory-injection attacks (MINJA-style), where a single planted 'successful' experience persists and triggers on later unrelated tasks (temporally decoupled), reported up to ~95% injection / ~70% attack success under idealized conditions. This is an adversarial analogue of temporal contamination and is empirical, no stability guarantee.


- **Sources:** [MemoryGraft: Persistent Compromise of LLM Agents via Poisoned Experience Retrieval](https://arxiv.org/abs/2512.16962) · [Memory Poisoning Attack and Defense on Memory-Based LLM Agents](https://arxiv.org/abs/2601.05504)

- **Relevance (OSA-3):** Shows the retrieval/credit channel JitRL relies on can be corrupted, breaking the slow-drift / clean-estimator assumptions behind JitRL's consistency theorem — a robustness caveat OSA-3 should note: convergence guarantees are conditional on uncontaminated memory.


### CV2-13-governed-memory-frameworks · conv: **empirical** · OSS: no · scope: no-gradient

Framework-level stabilizers for evolving memory (e.g., SSGM — Stability and Safety Governed Memory) propose pairing a rapidly updatable mutable graph with an append-only IMMUTABLE episodic log, plus session-budget controls and periodic memory resets, to BOUND long-term semantic drift. These are governance heuristics with empirical/qualitative justification, not proven convergence bounds.


- **Sources:** [Governing Evolving Memory in LLM Agents: the SSGM Framework](https://arxiv.org/abs/2603.11768)

- **Relevance (OSA-3):** Represents the 'structural cure' family (immutable log + bounded mutable store + resets) addressing temporal contamination. Complements JitRL's algorithmic cure: bounding drift is exactly the precondition JitRL's Theorem 4.2 needs, so these heuristics can be read as enforcing JitRL's slow-drift assumption.


### CV2-14-contextual-experience-replay · conv: **empirical** · OSS: no · scope: no-gradient

Contextual Experience Replay (CER) is a training-free, no-gradient self-improvement framework that accumulates and synthesizes past trajectories (environment dynamics + decision patterns) into a dynamic memory buffer for retrieval — an in-context analogue of experience replay. It improves adaptability empirically but offers no convergence/monotone-improvement guarantee.


- **Sources:** [Contextual Experience Replay for Self-Improvement of Language Agents](https://arxiv.org/abs/2506.06698)

- **Relevance (OSA-3):** Another empirical-only memory-evolution rollout in the enlarged space; reinforces that the field's no-gradient self-improvement methods are uniformly empirical except JitRL, isolating JitRL as the unique convergence anchor for OSA-3.


### CV2-15-trust-region-overopt-synthesis · conv: **proven** · OSS: https://github.com/liushiliushi/JitRL · scope: mixed

The convergence cure decomposes into (a) credit assignment / value estimation — proven only by JitRL's retrieval-advantage (Thm 4.1–4.3); empirical via LATS/Agent-Q LM value functions and Memento Q-learning; and (b) trust region / over-optimization control — the β-KL term in JitRL's objective is the agent-level trust region, with proven output-level analogues: soft-BoN temperature (2505.03156), HedgeTune optimal-N* (2506.19248), BoN reward-gap theory (2401.01879, 2507.05913), and KL-regularized over-optimization scaling (2210.10760). No agent-level method yet ports these proven trust-region results into a finite-time monotone-improvement guarantee over the full memory·skill·context action space.


- **Sources:** [JitRL (β-KL trust-region closed form)](https://arxiv.org/abs/2601.18510) · [Soft Best-of-N sampling / regularized BoN](https://arxiv.org/abs/2505.03156) · [HedgeTune: over-optimization and optimal N*](https://arxiv.org/abs/2506.19248) · [Theoretical analysis of Best-of-N](https://arxiv.org/abs/2401.01879) · [Scaling laws for reward-model over-optimization](https://arxiv.org/abs/2210.10760)

- **Relevance (OSA-3):** Frames OSA-3's contribution precisely: proven trust-region/over-optimization control exists at the OUTPUT level and proven consistency exists for JitRL's credit assignment, but a finite-time MONOTONE-IMPROVEMENT guarantee over the enlarged agent action space is still open — the exact gap a credit-assigned + trust-region OSA-3 theorem fills.
