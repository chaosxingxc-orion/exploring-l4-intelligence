> **🗄 ARCHIVED (2026-07-11)** — 已收官战役过程件（2026-06-26 提案期调研），仅作历史，非现行真源。

# Lane 4 — Verifiable rewards, evaluation & leakage/reproducibility pitfalls

> Part of the **Step-2 survey** for [[2026-06-26-training-free-rl-for-speech-omni-research-proposal]] (see [[Research-Proposal-Template]] §3). Produced by a multi-agent survey workflow (5 lanes -> per-lane adversarial verification -> synthesis), run `wf_d76b4901-23c`, 2026-06-26. Every source below was adversarially checked to resolve to a real paper; only `keep=true` claims are archived. Links are real and verifiable.


**Lane summary.** Verifiable, ground-truth-derived rewards (WER/exact-match/MCQ-accuracy/retrieval hit@k) used as best-of-N or MBR selection utilities are the right reward backbone for an Operator-B capability-activation study because, unlike model-judged rewards, the proxy equals the gold objective and so over-optimization is bounded; the published over-optimization literature (Gao et al.; Skalse et al.) and the unified Gibbs/best-of-N theory (Beirami et al.; smoothing-lens) show why, and quantify the KL/budget trade-off the study's q*(z)∝q0·exp(R/β) objective rests on. The most dangerous failure mode for THIS design is not weight-level reward hacking but EVALUATION artifacts: "Spurious Rewards" shows apparent RL/selection lifts can be optimization artifacts that do not transfer across model families, so a measured ICL "activation" must be defended with random-reward and cross-model controls. On the reproducibility side, a study evaluated on SAMPLED dev/test is exposed to four compounding hazards — (i) single-split / single-seed ranking instability (Gorman & Bedrick; Henderson et al.), (ii) underpowered small test sets and uncorrected multiple comparisons across k-shot/prompt/config grids (Card et al.; Dror et al.; Bisani & Ney bootstrap CIs), (iii) selection/winner's-curse inflation when demos, prompts, or the best-of-N winner are chosen on the same data used to report the lift (Perez et al.; Dodge et al.; Dwork reusable holdout), and (iv) leakage/contamination of the frozen model's pretraining or of ICL demos into the test split (Li & Flanigan; contamination survey; tinyBenchmarks for safe subset sizing). The actionable protocol: report verifiable-reward lifts with bootstrap/paired CIs and a power/MDE check, separate demo-selection data from evaluation data, run random-reward and cross-model null controls, deduplicate/date-check demos vs test for contamination, use multiple resampled splits and seeds, and follow the NeurIPS reproducibility checklist.


**Adversarial verifier assessment.** All 18 sources resolve to real, correctly-attributed papers and every statement is faithfully supported with no hallucinated ids or overstated findings; I keep all 18. Verification highlights: every arXiv id checked out to the exact titled paper (Tulu3 2411.15124, MBR-ASR 2510.19471, TTRL 2504.16084, Gao 2210.10760, Skalse 2209.13085, Spurious-Rewards 2506.10947, Beirami 2401.01879, Smoothing-Lens 2507.05913, judge-bias 2406.07791/2410.21819, Card 2010.06595, Perez 2105.11447, Dodge 1909.03004, contamination 2406.04244, tinyBenchmarks 2402.14992, Henderson 1709.06560, Pineau 2003.12206), and the non-arXiv sources resolve too (Gorman&Bedrick P19-1267, Dror P18-1128, Bisani&Ney ICASSP'04, Li&Flanigan AAAI'24, Dwork Science 2015 DOI 10.1126/science.aaa9375, Roelofs NeurIPS'19). The two quotes most worth adversarial scrutiny both held: C4's directional 'RL consumes much more KL than best-of-n' is a genuine Gao et al. finding (distinct BoN vs RL functional forms), and C6's Spurious-Rewards cross-model non-transfer is a documented core result. The lane's framing is internally honest in one important way: where it imports findings from text-LLM/RL/POS/Kaggle literature to a speech/omni best-of-N setting (C1 reward family extension, C10 MInDS-14, C13/C17 BoN analogies), it presents them as applied reasoning rather than claiming the cited paper studied speech — so no source is overstated. Minor caveats that do not warrant dropping any claim: (a) C8's 'lower perplexity than human evaluators' is a slight paraphrase of the self-preference mechanism but directionally faithful; (b) C15 is correctly held at med because the overfitting-hazard magnitude is genuinely contested (Dwork worst-case vs Roelofs empirical-mild) and the lane acknowledges this. Net: a well-sourced, appropriately hedged lane; verifiable-reward backbone, over-optimization/BoN-KL theory, and the leakage/winner's-curse/power/seed reproducibility hazards are all correctly grounded.


---

## Verified claims & sources (18 kept / 18 total)


### C1 · definitional · confidence: high

A 'verifiable reward' replaces a learned reward model with a deterministic verification function for tasks whose outputs can be checked against ground truth (math answer, exact string match, instruction-format compliance); this is the RLVR formulation and is exactly the family that makes WER, exact-match, MCQ-accuracy and retrieval hit@k usable as best-of-N / GRPO reward callables.


- **Sources:** [Tulu 3: Pushing Frontiers in Open Language Model Post-Training](https://arxiv.org/abs/2411.15124)

- **Relevance:** Defines the reward class for H1/H2/H3 best-of-N; verifiable speech rewards (WER/EM/MCQ/hit@k) are the principled choice over model-judged rewards.


### C2 · empirical · confidence: high

Selecting among sampled hypotheses by a verifiable/utility metric is effective for speech: minimum-Bayes-risk (MBR) decoding, which picks the hypothesis minimizing expected error (e.g., -WER) over sampled candidates, outperforms beam search in most ASR and speech-translation settings on Whisper-family models.


- **Sources:** [Re-evaluating Minimum Bayes Risk Decoding for Automatic Speech Recognition](https://arxiv.org/abs/2510.19471)

- **Relevance:** Empirical precedent that best-of-N/MBR over generations lifts ASR/ST (the 'content native' axis) — distinguishes consensus-utility (label-free) from gold-verifiable selection.


### C3 · empirical · confidence: high

When ground-truth labels are unavailable, a majority-vote / self-consistency pseudo-reward can drive test-time selection or RL, but this consensus reward reinforces the model's own prior and can be systematically wrong, so it is a weaker and potentially self-confirming substitute for a verifiable label-derived reward.


- **Sources:** [TTRL: Test-Time Reinforcement Learning](https://arxiv.org/abs/2504.16084)

- **Relevance:** Bounds the validity of label-free best-of-N selection; argues for gold-verifiable rewards when measuring whether ICL truly activates a capability (H1).


### C4 · empirical · confidence: high

Optimizing any imperfect proxy reward (RL or best-of-N) eventually DECREASES the true objective — Goodhart-style over-optimization — and the effect is a smooth, predictable function of the KL spent; best-of-N spends far less KL than RL for the same optimization, so BoN over-optimizes more slowly but still over-optimizes.


- **Sources:** [Scaling Laws for Reward Model Overoptimization](https://arxiv.org/abs/2210.10760)

- **Relevance:** Central caution + justification: verifiable rewards minimize over-optimization risk for Operator-B; KL-as-budget framing matches the study's q*(z)∝q0·exp(R/β) trust region.


### C5 · theoretical · confidence: high

Reward hacking is formally generic: 'unhackability' (raising proxy return can never lower true return) is an extremely strong condition that, for the full set of stochastic policies, holds only if one of the two reward functions is constant — i.e., essentially every non-trivial proxy reward is hackable in the limit.


- **Sources:** [Defining and Characterizing Reward Hacking](https://arxiv.org/abs/2209.13085)

- **Relevance:** Theoretical backbone for preferring verifiable over model-judged rewards across H1/H2/H3.


### C6 · empirical · confidence: high

An apparent capability 'lift' from reward-driven optimization can be an OPTIMIZATION ARTIFACT, not a real signal: RLVR produces large gains on Qwen2.5-Math even with random/spurious rewards (via a GRPO clipping bias that amplifies pretrained behaviors), and these spurious-reward gains FAIL to transfer to Llama3/OLMo2 — so single-model lifts must be validated with null-reward and cross-model controls.


- **Sources:** [Spurious Rewards: Rethinking Training Signals in RLVR](https://arxiv.org/abs/2506.10947)

- **Relevance:** Critical control for H1 (model-class asymmetry): rules out optimizer/clipping artifacts masquerading as ICL activation on the generative class.


### C7 · theoretical · confidence: high

Best-of-N selection has a closed-form KL/win-rate budget that matches the study's exponential-tilting objective: KL(best-of-n ‖ reference) ≤ log n − (n−1)/n (the classic expression is an upper bound, not equality), and win-rate of the BoN policy against the reference is ≤ n/(n+1).


- **Sources:** [Theoretical guarantees on the best-of-n alignment policy](https://arxiv.org/abs/2401.01879) · [Best-of-N through the Smoothing Lens: KL Divergence and Regret Analysis](https://arxiv.org/abs/2507.05913)

- **Relevance:** Theoretical anchor for the unified Gibbs objective and for reporting BoN lifts at a fixed KL/compute budget (Operator B).


### C8 · empirical · confidence: high

Model-judged rewards inject systematic, reproducible biases that confound capability measurement: LLM judges exhibit position bias (favoring answers by their location in the prompt) and self-preference bias (scoring lower-perplexity / more familiar text higher than humans do). These biases are absent from deterministic verifiable rewards.


- **Sources:** [Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge](https://arxiv.org/abs/2406.07791) · [Self-Preference Bias in LLM-as-a-Judge](https://arxiv.org/abs/2410.21819)

- **Relevance:** Justifies verifiable over model-judged rewards for clean H1/H3 measurement; if a judge is unavoidable (open-ended spoken QA), biases must be controlled.


### C9 · empirical · confidence: high

System rankings obtained on a single standard/held-out split frequently do NOT reproduce under randomly resampled train/test splits; reproducible conclusions require multiple random splits plus significance testing — directly relevant to a study reporting lifts on ONE sampled dev/test split.


- **Sources:** [We Need to Talk about Standard Splits](https://aclanthology.org/P19-1267/)

- **Relevance:** Test-set-selection pitfall: motivates multiple resampled dev/test draws before claiming an activation lift.


### C10 · empirical · confidence: high

Small sampled test sets make most comparisons UNDERPOWERED, so a modest measured lift can be statistical noise; a power / minimum-detectable-effect analysis should precede claiming an activation effect.


- **Sources:** [With Little Power Comes Great Responsibility](https://arxiv.org/abs/2010.06595)

- **Relevance:** Single-seed/small-sample noise: argues for power analysis and adequately sized sampled test sets for H1/H2 effect claims.


### C11 · definitional · confidence: high

Significance testing in NLP/speech must be chosen for the metric and account for dependent observations and multiple comparisons; for WER specifically, a bootstrap (and block/paired bootstrap) gives directly interpretable confidence intervals on the error-rate difference between systems.


- **Sources:** [The Hitchhiker's Guide to Testing Statistical Significance in NLP](https://aclanthology.org/P18-1128/) · [Bootstrap estimates for confidence intervals in ASR performance evaluation (Bisani & Ney, ICASSP 2004)](https://ieeexplore.ieee.org/document/1326009)

- **Relevance:** Concrete reporting standard for verifiable-reward lifts (bootstrap/paired CIs; multiple-comparison correction across k-shot/prompt/layer grids).


### C12 · empirical · confidence: high

Choosing the best prompt / demonstrations / hyperparameters on held-out examples drawn from the evaluation pool dramatically OVER-estimates few-shot ability ('winner's curse' of selection); in genuinely true-few-shot settings, principled selection (CV, MDL) barely beats random and can pick worse-than-random configs.


- **Sources:** [True Few-Shot Learning with Language Models](https://arxiv.org/abs/2105.11447)

- **Relevance:** ICL-demo / config selection leakage: the central evaluation pitfall for measuring an ICL activation lift cleanly (H1/H3).


### C13 · theoretical · confidence: high

Best-of-N reporting inherits an upward selection bias: the MAX of N noisy candidate scores is an upward-biased estimator of true performance, and reported results swing with the tuning/sampling budget — so the SELECTED output must be re-scored on held-out labels, and lifts reported as a function of budget N (expected-max curve), not at the single best draw on the selection metric.


- **Sources:** [Show Your Work: Improved Reporting of Experimental Results](https://arxiv.org/abs/1909.03004)

- **Relevance:** Winner's-curse / multiple-comparison pitfall intrinsic to best-of-N; prescribes budget-aware reporting for Operator B.


### C14 · empirical · confidence: high

A frozen pretrained omni/speech LLM may have seen the speech benchmark (or its transcripts) during pretraining, so an apparent few-shot 'activation' can be partial memorization; few-shot scores are inflated for datasets released before the model's training cutoff (task contamination).


- **Sources:** [Task Contamination: Language Models May Not Be Few-Shot Anymore](https://ojs.aaai.org/index.php/AAAI/article/view/29808) · [Benchmark Data Contamination of Large Language Models: A Survey](https://arxiv.org/abs/2406.04244)

- **Relevance:** Pretraining-leakage confound for H1/H2: an 'activated' capability could be recalled contaminated test data, not in-context activation.


### C15 · theoretical · confidence: med

Repeatedly iterating best-of-N configurations against the SAME sampled dev set causes adaptive overfitting of the holdout (validity degrades with repeated adaptive queries); the risk is worst on small sampled sets, though large-scale empirical studies show the effect is often smaller than feared when test sets are large and queries limited.


- **Sources:** [The reusable holdout: Preserving validity in adaptive data analysis (Dwork et al., Science 2015)](https://doi.org/10.1126/science.aaa9375) · [A Meta-Analysis of Overfitting in Machine Learning (Roelofs et al., NeurIPS 2019)](https://papers.nips.cc/paper/9117-a-meta-analysis-of-overfitting-in-machine-learning)

- **Relevance:** Multiple-comparisons / test-reuse pitfall: motivates a reusable-holdout discipline or fresh test draws when sweeping k-shot/prompt/N on a small dev set.


### C16 · empirical · confidence: high

Evaluating on a SMALL sampled subset is acceptable only if the subset is curated/anchored and variance is quantified: ~100 well-chosen (IRT-anchored) examples can estimate a large benchmark within a few points, but naive small random subsets carry high variance that must be reported as confidence intervals.


- **Sources:** [tinyBenchmarks: evaluating LLMs with fewer examples](https://arxiv.org/abs/2402.14992)

- **Relevance:** Sampled dev/test sizing: how to make a small sampled speech eval reliable for H1/H2 effect estimates.


### C17 · empirical · confidence: high

Single-seed results are not reproducible: holding hyperparameters fixed and varying only the random seed yields non-overlapping learning curves and can reverse algorithm rankings, so sampling/seed variance must be reported with multiple seeds and significance tests.


- **Sources:** [Deep Reinforcement Learning that Matters](https://arxiv.org/abs/1709.06560)

- **Relevance:** Single-seed-noise pitfall: report multiple seeds/sampling runs for Operator-B lifts.


### C18 · definitional · confidence: high

A recognized community standard exists for reporting the above: the NeurIPS reproducibility program / ML Reproducibility Checklist requires disclosing data splits, number of runs/seeds, compute, hyperparameter-selection procedure, and code — the checklist a best-of-N activation study should satisfy.


- **Sources:** [Improving Reproducibility in Machine Learning Research (NeurIPS 2019 Reproducibility Program)](https://arxiv.org/abs/2003.12206)

- **Relevance:** Recognized standard tying together the lane's recommendations (splits, seeds, selection disclosure) for the study's reporting.
