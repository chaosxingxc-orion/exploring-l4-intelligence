> **🗄 ARCHIVED (2026-07-11)** — 已收官战役过程件（2026-06-26 提案期调研），仅作历史，非现行真源。

# Lane 3 — Training-free / inference-time RL methods & convergence theory

> Part of the **Step-2 survey** for [[2026-06-26-training-free-rl-for-speech-omni-research-proposal]] (see [[Research-Proposal-Template]] §3). Produced by a multi-agent survey workflow (5 lanes -> per-lane adversarial verification -> synthesis), run `wf_d76b4901-23c`, 2026-06-26. Every source below was adversarially checked to resolve to a real paper; only `keep=true` claims are archived. Links are real and verifiable.


**Lane summary.** All five known anchors verified and extended (TTRL 2504.16084, TPO 2501.12895, MBR-ASR 2510.19471, BoN theory 2401.01879 & 2507.05913, JitRL 2601.18510). The lane's unifying result is that every weight-free inference-time RL method — best-of-N, soft/smoothed BoN, MBR, reward-guided (controlled) decoding, self-consistency, TTRL, TPO, JitRL — is a sampler or selector that tilts a BASE generative distribution q0 toward the Gibbs/exponential-tilting optimum q*(z) ∝ q0(z)·exp(R/β), the closed-form solution of KL-regularized RL (Korbak 2205.11275; Mudgal 2310.17022; BoNBoN 2406.00832). Convergence theory is now sharp: BoN's KL to base is upper-bounded by log N - (N-1)/N with win-rate ≤ N/(N+1) (Beirami 2401.01879); soft-BoN closes to the tilted optimum at O(1/n) (2505.03156); MBR is SLLN-consistent at O(n^{-1/2}) and beats MAP (2502.12685); the smoothing lens gives a regret-gap ~O(√log N) and an optimal temperature β* (2507.05913). Critically for H1: all of these require a stochastic base distribution over candidate sequences to tilt, so they natively steer the GENERATIVE class (Operator B) but have no purchase on a deterministic single-vector bi-encoder except via discrete Operator-A candidate selection — a theoretical mechanism for the predicted model-class asymmetry. Over-optimization is provably inevitable: gold reward peaks then falls with a single interior optimum N* (Gao 2210.10760; HedgeTune 2506.19248).


**Adversarial verifier assessment.** Strong lane. All 19 distinct arXiv IDs across the 15 claims resolve to real papers with matching titles/authors, including the 2026-dated anchor JitRL (2601.18510), which I scrutinized specifically and which genuinely proves its additive-logit update is the exact closed-form solution of the KL-constrained policy-optimization objective and reports SOTA among training-free methods. The unifying thesis (every weight-free inference-time RL method tilts a base q0 toward q* propto q0*exp(R/beta)) is well-grounded in verified foundations: Korbak (Bayesian-inference view of KL-RL), Mudgal (controlled decoding provably samples the RL solution on a frozen base), and the BoN/SBoN/MBR convergence results. Quantitative claims are accurate and several are honestly hedged (C2 correctly states the log N-(N-1)/N equality is disproven and only an upper bound; C10 flags that TTRL updates weights and only its reward mechanism is training-free; C7 is if anything understated). The only soft spots are interpretive/synthesis claims (C3 BoN-as-q*, C14 H1/H3 framing, C15 the no-q0-to-tilt mechanism for the vector class) and unverifiable exact algebra in C5 (Smoothing Lens) and the multi-objective-composition detail in C8 — all kept, but confidence-adjusted to med. No fabricated identifiers; nothing materially overstated. All 15 claims kept.


---

## Verified claims & sources (15 kept / 15 total)


### C1 · theoretical · confidence: high

The optimal policy of KL-regularized reward maximization has the closed form q*(z) ∝ q0(z)·exp(R(z)/β), i.e. an exponential tilt of the base distribution; equivalently, KL-penalized RL is Bayesian inference (prior q0 updated by reward 'evidence'). This is exactly the study's unified objective and the target that all inference-time tilting methods approximate.


- **Sources:** [RL with KL penalties is better viewed as Bayesian inference](https://arxiv.org/abs/2205.11275)

- **Relevance:** Foundational unified objective for both model classes; defines the target q* that Operator-A and Operator-B both approximate.


### C2 · theoretical · confidence: high

Best-of-N sampling tilts the base policy toward q*; its KL to the base is UPPER-bounded (not equal) by log N - (N-1)/N, and its win-rate against the base is ≤ N/(N+1). The commonly quoted log N - (N-1)/N equality is only an upper bound on the true KL.


- **Sources:** [Theoretical guarantees on the best-of-n alignment policy](https://arxiv.org/abs/2401.01879)

- **Relevance:** Core convergence/budget theory for Operator-B best-of-N (token-level BoN already run in-house on Qwen3-Omni); quantifies KL trust-region cost of N.


### C3 · theoretical · confidence: med

Best-of-N is asymptotically optimal in the win-rate-vs-KL tradeoff and converges to the tilted Gibbs optimum: the BoN distribution lies in the same class of tiltings of the base model as the KL-RL optimum, and as N grows it approaches the reward-maximizing tilted policy. This justifies treating BoN as a discrete approximation of q*.


- **Sources:** [BoNBoN Alignment for Large Language Models and the Sweetness of Best-of-n Sampling](https://arxiv.org/abs/2406.00832) · [Asymptotics of Language Model Alignment](https://arxiv.org/abs/2404.01730)

- **Relevance:** Grounds the in-house Operator-B gains (SLURP +0.330, URO +0.335) as principled approximations of the unified objective, not heuristics.


### C4 · theoretical · confidence: high

Soft / smoothed Best-of-N adds a temperature that smoothly interpolates base↔reward-max and converges to the optimal tilted distribution at rate O(1/n) in both KL and expected reward — a sharper, controllable alternative to hard BoN.


- **Sources:** [Soft Best-of-n Sampling for Model Alignment](https://arxiv.org/abs/2505.03156)

- **Relevance:** Operator-B refinement: tunable KL trust-region for generative-class steering; β in q* maps to the SBoN temperature.


### C5 · theoretical · confidence: med

A unified smoothing analysis bounds SBoN KL by log(N/(1+(N-1)·exp(-βR_max))) (recovering BoN's KL ≤ log N as β→∞), and bounds the regret gap to the optimal policy with an N-dependence scaling roughly as O(√log N); when the proxy reward has estimation error there exists an optimal intermediate temperature β* where SBoN strictly beats hard BoN.


- **Sources:** [Best-of-N through the Smoothing Lens: KL Divergence and Regret Analysis](https://arxiv.org/abs/2507.05913)

- **Relevance:** Directly supplies the lane's regret/KL theory and motivates soft- over hard-BoN for noisy verifiable rewards in Operator B.


### C6 · theoretical · confidence: high

Sample-based Minimum Bayes Risk decoding is consistent: it converges to the Bayes-optimal hypothesis at rate O(n^{-1/2}) (a strong-law-of-large-numbers Monte-Carlo guarantee) and tends to converge faster than MAP/most-probable decoding in several regimes.


- **Sources:** [Theoretical Guarantees for Minimum Bayes Risk Decoding (ACL 2025)](https://arxiv.org/abs/2502.12685)

- **Relevance:** Convergence theory for MBR/self-consistency-style selection in Operator B; the verifiable-utility (WER/exact-match) reward fns in speechrl_common.rl are MBR utilities.


### C7 · empirical · confidence: high

MBR decoding empirically outperforms beam search for speech-to-text: on Whisper-family models it beats beam search in most ASR and ST settings (English and Japanese), making sample-based MBR a strong training-free decoder for the generative speech class.


- **Sources:** [Re-evaluating Minimum Bayes Risk Decoding for Automatic Speech Recognition](https://arxiv.org/abs/2510.19471)

- **Relevance:** Speech-specific Operator-B evidence (generative class); directly applicable to ASR/ST tasks in the disentanglement study.


### C8 · theoretical · confidence: med

Reward-guided (controlled) decoding provably samples from the KL-regularized RL solution at inference without weight updates: a frozen base LM is steered by a separate prefix scorer (value function) for the reward; blockwise control interpolates between tokenwise RL and best-of-K, and multiple prefix scorers compose for multi-objective control at inference time.


- **Sources:** [Controlled Decoding from Language Models](https://arxiv.org/abs/2310.17022)

- **Relevance:** Operator-B reward-guided decoding with a formal optimality guarantee; the blockwise knob spans the BoN↔tokenwise spectrum the study can sweep.


### C9 · empirical · confidence: high

Self-consistency = marginalize over sampled reasoning paths then take the majority/most-consistent answer; it is the exact-match-utility special case of MBR voting and yields large gains (e.g. GSM8K +17.9%). It is the reward-free (consensus) limit of the same selection machinery.


- **Sources:** [Self-Consistency Improves Chain of Thought Reasoning in Language Models](https://arxiv.org/abs/2203.11171)

- **Relevance:** Provides the label-free consensus baseline (vs verifiable-reward selection) for Operator B and the reward signal used by TTRL.


### C10 · empirical · confidence: high

Test-Time RL (TTRL) shows a self-generated, label-free reward — majority-vote consensus over sampled outputs — is an effective RL signal: it lifts Qwen2.5-Math-7B AIME-2024 pass@1 by ~211% using only unlabeled test data. The reward-estimation mechanism (voting) is the training-free part; it can drive selection without ground truth.


- **Sources:** [TTRL: Test-Time Reinforcement Learning](https://arxiv.org/abs/2504.16084)

- **Relevance:** Anchor verified; supplies the label-free reward estimator (consensus) usable as the verifiable-reward proxy when no labels exist in the speech setting. Note TTRL updates weights, so only its reward mechanism is 'training-free'.


### C11 · empirical · confidence: high

Test-Time Preference Optimization (TPO) performs inference-time alignment with NO weight update: it converts reward signals into textual critiques used as 'textual gradients' to iteratively refine outputs, and scales with both search width and depth; an unaligned Llama-3.1-70B-SFT surpasses its aligned Instruct counterpart after a few TPO steps.


- **Sources:** [Test-Time Preference Optimization: On-the-Fly Alignment via Iterative Textual Feedback](https://arxiv.org/abs/2501.12895)

- **Relevance:** Anchor verified; a purely weight-free Operator-B refinement loop directly compatible with the study's no-weight-change constraint.


### C12 · theoretical · confidence: high

JitRL realizes training-free continual RL by additively modulating the frozen LM's output logits with non-parametric advantage estimates, and proves this additive logit update is the EXACT closed-form solution of the KL-constrained policy-optimization objective — i.e. it instantiates q* ∝ q0·exp(R/β) at the logit level. It is SOTA among training-free methods on WebArena/Jericho.


- **Sources:** [Just-In-Time Reinforcement Learning: Continual Learning in LLM Agents Without Gradient Updates](https://arxiv.org/abs/2601.18510)

- **Relevance:** Anchor verified; the cleanest weight-free instantiation of the unified Gibbs objective for Operator B, generalizing BoN/CD to a logit-space tilt.


### C13 · theoretical · confidence: high

Inference-time reward optimization is provably subject to over-optimization (Goodhart/winner's curse): true reward rises then falls as N grows. The expected true reward has either monotone behavior or a single unique interior extremum N*, which HedgeTune locates via a root-finding problem — giving a principled stopping rule for BoN/SBoN.


- **Sources:** [Inference-Time Reward Hacking in Large Language Models](https://arxiv.org/abs/2506.19248) · [Scaling Laws for Reward Model Overoptimization](https://arxiv.org/abs/2210.10760)

- **Relevance:** Defines the over-optimization N* the study must respect when sweeping N for Operator B with imperfect/proxy verifiable rewards; motivates KL trust-region (β) control.


### C14 · empirical · confidence: med

On the generative speech class, instruction-conditioned reranking / generative error correction over ASR N-best is an effective training-free Operator-B lever, and prompting strategy matters: 'Task-Activating Prompting' (an explicit-task-definition prompt) improves zero/few-shot LLM correction — direct evidence that explicit task definition + in-context conditioning activates latent capability in generative models (supports H1/H3).


- **Sources:** [Generative Speech Recognition Error Correction with LLMs and Task-Activating Prompting](https://arxiv.org/abs/2309.15649) · [Can Generative Large Language Models perform ASR error correction?](https://arxiv.org/abs/2307.04172) · [ASR Error Correction using Large Language Models](https://arxiv.org/abs/2409.09554)

- **Relevance:** Bridges the methods lane to the central H1/H3 question — explicit-task-definition + in-context conditioning as the activation lever, demonstrated on the GENERATIVE speech class via reranking/GER.


### C15 · theoretical · confidence: med

All these inference-time RL methods (BoN, soft-BoN, MBR, controlled decoding, self-consistency, TPO, JitRL) operate by tilting a stochastic BASE distribution q0 over candidate sequences toward exp(R/β); they therefore have direct purchase only where a sampling distribution exists — the GENERATIVE/Thinker-Talker class (Operator B). A frozen contrastive bi-encoder emits one deterministic L2-normalized vector with no sequence distribution to tilt, so these methods cannot steer it except by discrete candidate selection over a finite pooled set (Operator A) — a mechanistic basis for the predicted H1 model-class asymmetry.


- **Sources:** [RL with KL penalties is better viewed as Bayesian inference](https://arxiv.org/abs/2205.11275) · [Controlled Decoding from Language Models](https://arxiv.org/abs/2310.17022) · [Soft Best-of-n Sampling for Model Alignment](https://arxiv.org/abs/2505.03156)

- **Relevance:** Theoretical mechanism for H1: the same inference-time RL machinery natively steers the generative class but is structurally inapplicable (beyond Operator-A selection) to the vector class.
