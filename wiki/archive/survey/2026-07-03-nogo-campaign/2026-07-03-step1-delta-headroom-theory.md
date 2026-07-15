> **🗄 ARCHIVED (2026-07-11)** — 已收官战役过程件（2026-07-03 NO-GO 战役），仅作历史，非现行真源。

# Step-1 delta scan D1 — agentic-vs-single-model headroom & decomposition theory

> Step-1 rationality campaign lane · 2026-07-03 · workflow `wf_68e2556d-7a7` ·
> pre-registration: [[2026-07-03-agentic-tfrl-step1-preregistration]] @ freeze b19bff2. Ground rules: the 2026-07-02 verdict is the null hypothesis;
> claims tagged `delta_vs_archive` against the 17-file survey archive; every URL adversarially
> verified (0-hallucination bar). 

### D1-01 — [new] axis: c-sample-complexity · bears on: P1, U1, S4, M2, M4

Tran & Kiela (2026-04-02) show that under EQUAL thinking-token budgets, single-agent LLMs consistently match or outperform multi-agent systems on multi-hop reasoning across three model families (Qwen3, DeepSeek-R1-Distill-Llama, Gemini 2.5), and give an information-theoretic argument grounded in the Data Processing Inequality that a single agent with perfect context utilization is more information-efficient at fixed budget. Their own theory predicts MAS becomes competitive only when the single agent's effective context utilization degrades or extra compute is spent — i.e., prior MAS advantages were largely unaccounted compute overhead. This is compute-normalized evidence FOR the null (agentic decomposition adds no headroom at matched cost), with the context-degradation carve-out being the only q0-adjacent escape it names.

**Sources:** [Single-Agent LLMs Outperform Multi-Agent Systems on Multi-Hop Reasoning Under Equal Thinking Token Budgets](https://arxiv.org/abs/2604.02460) (2026-04-02) · verified: True

### D1-02 — [new] axis: c-sample-complexity · bears on: P1, U1, M2, M5

Choi, Zhu & Li (NeurIPS 2025 Spotlight) prove that multi-agent debate, modeled as a stochastic belief-update process WITHOUT bias-corrective intervention, induces a martingale over agents' belief trajectories — so debate alone does not improve expected correctness; majority voting accounts for most of the gains attributed to MAD. They also prove a majority-vote limit theorem (Theorem 1): with N agents exceeding K/Delta^2, success probability is lower-bounded by 1-exp(-N(Delta/sqrt(K)-1/sqrt(N))^2). This is a peer-reviewed formal NULL for interaction-based headroom on a fixed base distribution — the inverse of what re-open condition r2 requires.

**Sources:** [Debate or Vote: Which Yields Better Decisions in Multi-Agent Large Language Models? (NeurIPS 2025 Spotlight)](https://arxiv.org/abs/2508.17536) (2025-08-24) · verified: True

### D1-03 — [new] axis: c-sample-complexity · bears on: M5, M4, P8

Huang, Li, Wu, Yang, Talwalkar, Ramchandran, Jordan & Jiao (2025-06-05) prove a sample-complexity SEPARATION between selection paradigms on a fixed base distribution: self-consistency (label-free consensus) needs Theta(1/Delta^2) samples to output the correct answer while best-of-n with a reward signal needs only Theta(1/Delta), where Delta is the probability gap between the correct answer and the second most likely answer; they further prove self-correction with verifier feedback lets a single Transformer simulate online expert learning multi-task. This formalizes exactly the C1 pattern (MBR/consensus null at small N while oracle-reward selection is significant) and gives the sample-complexity axis a real, non-tautological theorem: access to R changes the realization cost quadratically, without moving the ceiling.

**Sources:** [Sample Complexity and Representation Ability of Test-time Scaling Paradigms](https://arxiv.org/abs/2506.05295) (2025-06-05) · verified: True

### D1-04 — [new] axis: b-estimate-R · bears on: M5, P6, P8

Di, Ji, Li, Zhao & Gu (2025-10-03) prove Best-of-Majority (filter candidates by frequency, then take top-k by reward) is MINIMAX-OPTIMAL for pass@k inference scaling with an imperfect reward model: regret O(eps_opt + sqrt(eps_RM^2 * C*/k)) at sampling budget N=Omega-tilde(C*), with a matching lower bound, and unlike plain majority voting or plain best-of-N its performance provably does not degrade as N grows. This is finite-sample theory for selection under ESTIMATED reward (eps_RM explicit) — the regime M5 occupies — and is not derivable from the Gibbs identity.

**Sources:** [Best-of-Majority: Minimax-Optimal Strategy for Pass@k Inference Scaling](https://arxiv.org/abs/2510.03199) (2025-10-03) · verified: True

### D1-05 — [new] axis: c-sample-complexity · bears on: P1, M2

Chen & Peng, 'Multi-agent Markov Entanglement' (v3 2025-11-13, arXiv-only, no peer-reviewed venue noted), prove a multi-agent MDP admits EXACT additive value decomposition if and only if its transition kernel is separable ('unentangled'), and for non-separable systems the decomposition ERROR is upper-bounded by a Markov-entanglement measure (distance to the nearest separable kernel), with index policies achieving O(sqrt(N)) sublinear error. This is the nearest existing thing to a 'non-separable decomposition bound', but it runs in the OPPOSITE direction to re-open condition r2: it bounds the cost of decomposing a non-separable system, mirroring qstar_product's separability-implies-no-op structure at the MDP level, and it is not peer-reviewed — so r2 remains unmet.

**Sources:** [Multi-agent Markov Entanglement](https://arxiv.org/abs/2506.02385) (2025-06-03 (v3 2025-11-13)) · verified: True

### D1-06 — [new] axis: c-sample-complexity · bears on: P1, M2, M4

Rizvi-Martel, Bhattamishra, Rathi, Rabusseau & Hahn (2025-10-14) give a formal expressivity framework for multi-agent transformer reasoning (state tracking, recall, k-hop reasoning) with bounds on how many agents and how much inter-agent communication are needed, identifying regimes where communication is PROVABLY beneficial and proving intrinsic limitations when agent count or bandwidth is constrained. This is a genuine formal decomposition-helps result, but on the resource-constrained expressivity/parallelism axis (bounded per-agent capacity) — it changes realization cost under constraints, not the optimization ceiling on a fixed q0 with given R, so it occupies B0 axis (c) and does not overturn the killed theorems.

**Sources:** [Benefits and Limitations of Communication in Multi-Agent Reasoning](https://arxiv.org/abs/2510.13903) (2025-10-14) · verified: True

### D1-07 — [new] axis: a-change-q0 · bears on: P4, M3

Wakayama & Suzuki (submitted 2025-10-13, revised 2026-06-14) prove in-context learning IS Bayesian inference in a meta-learning generalization theory: total ICL risk decomposes orthogonally into a model-dependent Bayes Gap (with a non-asymptotic bound in number of pretraining prompts and context length) and a model-independent Posterior Variance, and task-mixture uncertainty vanishes EXPONENTIALLY fast in the number of in-context examples. This is quantitative theory treating conditioning as a first-class operator that moves the effective task posterior (the model 'selects the optimal algorithm at test time') — the formal template P4's what-would-overturn asks for on the q0-changing axis, though proven for uniform-attention Transformers in a meta-learning setup, not for frozen omni speech models.

**Sources:** [In-Context Learning Is Provably Bayesian Inference: A Generalization Theory for Meta-Learning](https://arxiv.org/abs/2510.10981) (2025-10-13 (rev 2026-06-14)) · verified: True

### D1-08 — [update] axis: a-change-q0 · bears on: M3, P4

Wu et al., 'The Invisible Leash' (2025-07-20), formalize RLVR as support-constrained optimization: on-policy reward tilting cannot place mass outside the base model's initial support, so it sharpens precision but cannot discover solutions the base assigns zero probability — escaping requires explicitly seeding probability mass into underrepresented regions (i.e., changing q0). This independently corroborates M3's information-availability premise (selection/tilting cannot create support; only injection moves the ceiling); tagged UPDATE because the archive already adjudicated the RLVR support-boundary debate via 2510.04028 and 2602.08281, though this specific formal statement is not archived.

**Sources:** [The Invisible Leash: Why RLVR May or May Not Escape Its Origin](https://arxiv.org/abs/2507.14843) (2025-07-20) · verified: True

### D1-09 — [new] axis: b-estimate-R · bears on: M5, P6, U5

Elasky, Nakasako & Goyal (2026-05-26) show empirically on code/logic tasks that debate improves a WEAK judge's reward accuracy over stronger models only when the critic's verification ability demonstrably exceeds the judge's and the judge can treat critic claims as verifiable (significant in 3/5 model pairings, null when critic≈judge); a single independent critique recovers the bulk of debate's benefit at lower inference cost. Axis-(b) relevance: interaction can improve deployment-time R estimation, but the mechanism needs a capability gap and the cheapest one-shot-critique variant suffices — cutting against any claim that a multi-round agentic apparatus is load-bearing for reward estimation.

**Sources:** [Debate Helps Weak Judges Reward Stronger Models](https://arxiv.org/abs/2605.27483v1) (2026-05-26) · verified: True

### D1-10 — [new] axis: c-sample-complexity · bears on: M4, M2, U1

Wunderlich, Kaesberg, Wahle, Ruas & Gipp (2026-05-02, SRW at ACL 2026) benchmark inference strategies at MATCHED compute budgets and find multi-agent debate and mixture-of-agents beat single-model self-consistency by 1.3 and 2.7 points (MMLU-Pro, BBH; +7.1 over CoT at the highest budgets), with self-consistency saturating earlier — an empirical, no-theory counterpoint to D1-01 on different tasks. Note the beaten baseline is label-free consensus (the weak selector per D1-03's Theta(1/Delta^2) bound), not verifier-based best-of-N, so the matched-compute agentic-efficiency question is empirically CONTESTED, not settled either way.

**Sources:** [Multi-Agent Reasoning Improves Compute Efficiency: Pareto-Optimal Test-Time Scaling](https://arxiv.org/abs/2605.01566) (2026-05-02) · verified: True

## Negative findings (verified empty searches — decision-relevant)

- r2 CHECK — EMPTY as of 2026-07-03: no peer-reviewed theorem found proving that decomposing an LLM inference task into isolated contexts ADDS optimization headroom under a fixed reward (searched: 'non-separable/irreducibility theorem multi-agent decomposition reward headroom context isolation LLM'; 'exponential tilting Gibbs KL-regularized multi-agent pipeline composition theorem'). The two nearest formal results run the OPPOSITE direction: Multi-agent Markov Entanglement (arXiv 2506.02385, NOT peer-reviewed) proves separability iff exact decomposition and bounds decomposition ERROR under non-separability, and Debate-or-Vote (NeurIPS 2025) proves interaction without bias correction is a martingale (no expected-correctness gain). Re-open condition r2 is NOT met.
- No extension of the Gibbs/exponential-tilt KL-regularized formalism from single-model output selection to multi-agent PIPELINE COMPOSITION was found beyond JitRL (2601.18510, already in the 6/30 archive); a targeted search for such a composition theorem (July 2026) returned only single-policy KL-RLHF theory (multiple reference models 2502.01203, tail-aware bounds 2604.10727) and empirical pipeline systems.
- No formal SUPPORT-EXPANSION theorem for in-context/retrieval memory injection in frozen LLMs was found — i.e., no theorem quantifying how much context injection moves the oracle ceiling (the M3 T-part candidate does not yet exist in the literature); RAG theory hits are token-level harmonization (2406.00944) or empirical knowledge-injection systems. The closest formal object is the ICL-as-Bayesian-inference line (D1-07), which changes the task posterior but does not state a headroom/ceiling-movement result.
- No provable TASK-SEPARATION theorem found of the form 'solvable by a multi-agent LLM system but unsolvable by a single model at equal total context/compute'; the closest is the resource-constrained expressivity analysis of 2510.13903 (bounded per-agent capacity), which is an axis-(c) tradeoff result, not a fixed-resource separation. Compute-normalized empirics are contested (2604.02460 says single-agent wins on multi-hop reasoning; 2605.01566 says debate/MoA beat self-consistency on MMLU-Pro/BBH).
- Post-2026-06-26 sweep (publication window since the archive freeze, searched 2026-07-03): no NEW theory paper on agentic-vs-single-model optimization headroom appeared in the last week; June-July 2026 agentic test-time-compute items found (ATLAS 2606.01667, ARTIS 2602.01709, FutureWeaver 2512.11213, AgentArk 2602.03955) are empirical systems papers without headroom theorems.
- VERIFIER NOTE (D1-08 delta check): arXiv 2507.14843 itself appears nowhere in the wiki archive; the 'update' tag rests on the archive's existing adjudication of the RLVR support-boundary debate (2510.04028, 2602.08281, 2506.14245 all present in the consolidated bibliography). No other claim's arXiv ID or title matches any archived file — all 'new' tags were grep-confirmed against wiki/survey and the full wiki tree.