# Step-2 Survey Archive — TFRL Omni Capability Activation

> Part of the **Step-2 survey** for [[2026-06-26-training-free-rl-for-speech-omni-research-proposal]] (see [[Research-Proposal-Template]] §3). Produced by a multi-agent survey workflow (5 lanes -> per-lane adversarial verification -> synthesis), run `wf_d76b4901-23c`, 2026-06-26. Every source below was adversarially checked to resolve to a real paper; only `keep=true` claims are archived. Links are real and verifiable.


This directory archives the verified citations behind the **Survey & Positioning (§3)** of [[2026-06-26-training-free-rl-for-speech-omni-research-proposal]]. Five lanes, each adversarially verified; a claim is archived only if its source(s) resolved to a real paper (`sources_resolve=true`, `keep=true`).


## Lanes


| # | Lane | File | Kept claims |
|---|---|---|---|
| 1 | Omni pretrained-capability map & the two model classes | [capability-map](2026-06-26-survey-capability-map.md) | 20/20 |
| 2 | ICL / few-shot / explicit task-definition & label-sensitivity in audio LLMs | [icl-fewshot](2026-06-26-survey-icl-fewshot.md) | 15/15 |
| 3 | Training-free / inference-time RL methods & convergence theory | [tfrl-theory](2026-06-26-survey-tfrl-theory.md) | 15/15 |
| 4 | Verifiable rewards, evaluation & leakage/reproducibility pitfalls | [rewards-eval](2026-06-26-survey-rewards-eval.md) | 18/18 |
| 5 | Novelty-delta vs the closest prior work | [novelty-delta](2026-06-26-survey-novelty-delta.md) | 12/12 |

**Totals:** 80 kept claims · 93 unique verified sources.


## Agent-level survey — S1 (2026-06-30)

Strategic direction probe for [[2026-06-30-agent-level-synthesis]] (run `wf_8452c9ae-a11`). 41 verified
claims / 51 sources; verdict: **GO — add-new-layer, speech-grounded** (domain-transfer, not mechanism-novel).
Each claim is scope-tagged (no-gradient = in scope vs weight-updating = out).

| Lane | File | Kept |
|---|---|---|
| A4 — speech/omni agents & the moat (B3) | [agent-speech-agents](2026-06-30-survey-agent-speech-agents.md) | 15 |
| A5 — model classes as components + novelty (B5/B7) | [agent-components-novelty](2026-06-30-survey-agent-components-novelty.md) | 13 |
| A3-headroom — does it compound? (B1/B4) | [agent-does-it-compound](2026-06-30-survey-agent-does-it-compound.md) | 13 |

Living strategic memo: [agent-level-synthesis](2026-06-30-agent-level-synthesis.md).

## Agent-level survey — S2 deepening: memory + skills design (2026-06-30)

Design-oriented deepening (run `wf_a066da37-c09`); 43 verified claims / 70 sources. **Design synthesis:**
[agent-memory-skills-design](2026-06-30-agent-memory-skills-design.md).

| Lane | File | Kept |
|---|---|---|
| A1 — agent memory (deep design + speech) | [agent-memory](2026-06-30-survey-agent-memory.md) | 26 |
| A2 — agent skills (deep design + speech) | [agent-skills](2026-06-30-survey-agent-skills.md) | 17 |

Key finding: a **verifiable-reward acceptance gate** is the one control law for both components (SkillsBench:
curated skills +16.2pp vs self-generated ~0); θ2's β-KL trust region instantiates as Mem0 mutation-rate (memory)
+ GEPA Pareto non-regression (skills). Both run on existing frozen assets (Omni-Embed-Nemotron index + W1
verifiable speech rewards). Open contribution: no audio cross-session paralinguistically-keyed memory benchmark.

## Agent-level survey — θ2 convergence (2026-06-30)

Convergence-focused survey grounding the OptSpace proof **OSA-3** (`proofs/tfrl/OptSpace-notes.md`; run
`wf_14ef3acb-2a3`). 43 verified claims / 54 sources. **Synthesis + convergence map:**
[agent-convergence](2026-06-30-survey-agent-convergence.md).

| Lane | File | Kept |
|---|---|---|
| CV1 — output-level convergence theory | [output-convergence](2026-06-30-survey-agent-output-convergence.md) | 14 |
| CV2 — agent-level convergence & stability | [agent-stability](2026-06-30-survey-agent-agent-stability.md) | 15 |
| CV3 — algorithm-level stabilization | [stabilization](2026-06-30-survey-agent-stabilization.md) | 14 |

Key finding: proven *finite-N* convergence lives at the **output level** (soft-BoN O(1/N), MBR, GSI, HedgeTune
N*); the **agent level** has only **JitRL**'s *asymptotic* consistency under a trust-region/slow-drift
precondition — the trust region is the hinge that links naive non-convergence (OSA-3a) to credit-assigned
convergence (OSA-3b). Open-source: [JitRL](https://github.com/liushiliushi/JitRL), HedgeTune, GSI, ACE, AWM, LATS.

## Step-1 rationality campaign — agentic-TFRL GO/NO-GO (2026-07-03/04)

> Pre-registered decision campaign (freeze anchor b19bff2), null hypothesis = the 2026-07-02
> deep-review verdict. Outcome: **NO-GO ratified by owner 2026-07-04** — the agent-level question is
> CLOSED absent re-open conditions r1-r3. Decision doc: [[2026-07-03-omni-agentic-tfrl-go-no-go-decision]];
> pre-registration: [[2026-07-03-agentic-tfrl-step1-preregistration]]. Runs: wf_a68f9164-b3c (Phase 0),
> wf_68e2556d-7a7 (delta/Part-A/mechanisms), wf_f6d37987-df5 (B-lanes/panel/synthesis),
> wf_e5dd317b-9cb (/ars-reviewer fresh-adversary panel).

- [[2026-07-03-step1-delta-headroom-theory]] — D1: decomposition/headroom theory delta (10 verified claims; r2 EMPTY)
- [[2026-07-03-step1-delta-speech-agent-memory]] — D2: speech agent memory/skills delta (11 claims; r1 NOT MET, 12 empty searches)
- [[2026-07-03-step1-delta-selector-learning]] — D3: selector learning / reference-free QE delta (12 claims)
- [[2026-07-03-step1-part-a-memo]] — Part-A: single-model TFRL rationality (RATIONAL-AND-CONTINUING)
- [[2026-07-03-step1-mechanism-support-expansion]] — M3 dossier + Phase-0 KILL (F=0.38108 vs 0.01)
- [[2026-07-03-step1-mechanism-selector-accumulation]] — M5 dossier + confirmatory NO-PASS (exact zero, inert instrument)
- [[2026-07-03-step1-mechanism-cross-block-dependence]] — M2 dossier (design-only)
- [[2026-07-03-step1-mechanism-sampling-isolation]] — M4 dossier (design-only)
- [[2026-07-03-step1-blanes-memos]] — B3 task-family / B4 VoI / B5 feasibility memos (post-outcome compilation)
- [[2026-07-03-step1-hostile-panel-verdicts]] — 6-charge panel: all stands; steelman-NO-GO; briefs record
- [[2026-07-03-step1-ars-reviewer-panel]] — /ars-reviewer 5-persona panel: sound-with-corrections (C1-C12 applied)

W1-repo pilot artifacts: `_repro/m3_phase0_selection.json`, `_repro/m3_phase0_zero_support.json`,
`_repro/m5_selector_dev.json`, `_repro/m5_confirmatory_slice_ids.json`, `_repro/m5_selector_confirmatory.json`,
`_repro/m5_memo_censuses.json` (12/12 memo numbers reproduced).

## Consolidated bibliography (Step-2 model-output survey; all verified, deduplicated)

- [A Large-Scale Probing Analysis of Speaker-Specific Attributes in Self-Supervised Speech Representations](https://arxiv.org/abs/2501.05310)
- [A Meta-Analysis of Overfitting in Machine Learning (Roelofs et al., NeurIPS 2019)](https://papers.nips.cc/paper/9117-a-meta-analysis-of-overfitting-in-machine-learning)
- [AIR-Bench: Benchmarking Large Audio-Language Models via Generative Comprehension](https://arxiv.org/abs/2402.07729)
- [ALICE: A Multifaceted Evaluation Framework of Large Audio-Language Models' In-Context Learning Ability](https://arxiv.org/abs/2603.20433)
- [Aligning Paralinguistic Understanding and Generation in Speech LLMs via Multi-Task Reinforcement Learning](https://arxiv.org/abs/2603.15981)
- [Answer is All You Need: Instruction-following Text Embedding via Answering the Question (InBedder)](https://arxiv.org/abs/2402.09642)
- [ASR Error Correction using Large Language Models](https://arxiv.org/abs/2409.09554)
- [Asymptotics of Language Model Alignment](https://arxiv.org/abs/2404.01730)
- [Attentive Statistics Pooling for Deep Speaker Embedding](https://arxiv.org/abs/1803.10963)
- [Benchmark Data Contamination of Large Language Models: A Survey](https://arxiv.org/abs/2406.04244)
- [Benchmarking Contextual and Paralinguistic Reasoning in Speech-LLMs](https://arxiv.org/abs/2509.16589)
- [Best-of-N through the Smoothing Lens: KL Divergence and Regret Analysis](https://arxiv.org/abs/2507.05913)
- [BoNBoN Alignment for Large Language Models and the Sweetness of Best-of-n Sampling](https://arxiv.org/abs/2406.00832)
- [Bootstrap estimates for confidence intervals in ASR performance evaluation (Bisani & Ney, ICASSP 2004)](https://ieeexplore.ieee.org/document/1326009)
- [Can Generative Large Language Models perform ASR error correction?](https://arxiv.org/abs/2307.04172)
- [CLAP: Learning Audio Concepts From Natural Language Supervision](https://arxiv.org/abs/2206.04769)
- [Comparative layer-wise analysis of self-supervised speech models](https://arxiv.org/abs/2211.03929)
- [Controlled Decoding from Language Models](https://arxiv.org/abs/2310.17022)
- [Deep Reinforcement Learning that Matters](https://arxiv.org/abs/1709.06560)
- [Defining and Characterizing Reward Hacking](https://arxiv.org/abs/2209.13085)
- [Diffusion vs. Autoregressive Language Models: A Text Embedding Perspective](https://arxiv.org/abs/2505.15045)
- [Discovering and Causally Validating Emotion-Sensitive Neurons in Large Audio-Language Models](https://arxiv.org/abs/2601.03115)
- [Do Audio LLMs Listen or Read? Analyzing and Mitigating Paralinguistic Failures with VoxParadox](https://arxiv.org/abs/2605.27772)
- [Do Audio LLMs Really LISTEN, or Just Transcribe? Measuring Lexical vs. Acoustic Emotion Cues Reliance](https://arxiv.org/abs/2510.10444)
- [Dynamic-SUPERB Phase-2 (180 tasks)](https://arxiv.org/abs/2411.05361)
- [Dynamic-SUPERB: A Dynamic, Collaborative, Comprehensive Instruction-Tuning Benchmark for Speech](https://arxiv.org/abs/2309.09510)
- [ECAPA-TDNN: Emphasized Channel Attention, Propagation and Aggregation in TDNN Based Speaker Verification](https://arxiv.org/abs/2005.07143)
- [EmoSLLM: Parameter-Efficient Adaptation of LLMs for Speech Emotion Recognition](https://arxiv.org/abs/2508.14130)
- [Exploring In-Context Learning of Textless Speech Language Model for Speech Classification Tasks](https://arxiv.org/abs/2310.12477)
- [Few-shot Personalization via In-Context Learning for Speech Emotion Recognition based on Speech-Language Model](https://arxiv.org/abs/2509.08344)
- [Frozen Large Language Models Can Perceive Paralinguistic Aspects of Speech](https://arxiv.org/abs/2410.01162)
- [FSA-GRPO: Teaching Auditory LLMs to Use Few-shot Demonstrations](https://arxiv.org/abs/2606.02615)
- [Function Vectors in Large Language Models](https://arxiv.org/abs/2310.15213)
- [Generative Speech Recognition Error Correction with LLMs and Task-Activating Prompting](https://arxiv.org/abs/2309.15649)
- [Ground-Truth Labels Matter: A Deeper Look into Input-Label Demonstrations](https://arxiv.org/abs/2205.12685)
- [How do Multimodal Foundation Models Encode Text and Speech? An Analysis of Cross-Lingual and Cross-Modal Representations](https://arxiv.org/abs/2411.17666)
- [Improving Reproducibility in Machine Learning Research (NeurIPS 2019 Reproducibility Program)](https://arxiv.org/abs/2003.12206)
- [In-Context Learning in Speech Language Models: Analyzing the Role of Acoustic Features, Linguistic Structure, and Induction Heads](https://arxiv.org/abs/2604.06356)
- [Inference-Time Reward Hacking in Large Language Models](https://arxiv.org/abs/2506.19248)
- [INSTRUCTIR: A Benchmark for Instruction Following of Information Retrieval Models](https://arxiv.org/abs/2402.14334)
- [Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge](https://arxiv.org/abs/2406.07791)
- [Just-In-Time Reinforcement Learning: Continual Learning in LLM Agents Without Gradient Updates](https://arxiv.org/abs/2601.18510)
- [Larger language models do in-context learning differently](https://arxiv.org/abs/2303.03846)
- [Layer-wise Analysis of a Self-supervised Speech Representation Model](https://arxiv.org/abs/2107.04734)
- [LEACE: Perfect linear concept erasure in closed form](https://arxiv.org/abs/2306.03819)
- [Making Text Embedders Few-Shot Learners (bge-en-icl)](https://arxiv.org/abs/2409.15700)
- [MiMo-Audio: Audio Language Models are Few-Shot Learners](https://arxiv.org/abs/2512.23808)
- [MMAU: A Massive Multi-Task Audio Understanding and Reasoning Benchmark](https://arxiv.org/abs/2410.19168)
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595)
- [New Skills or Sharper Primitives? A Probabilistic Perspective on the Emergence of Reasoning in RLVR](https://arxiv.org/abs/2602.08281)
- [NV-Embed: Improved Techniques for Training LLMs as Generalist Embedding Models](https://arxiv.org/abs/2405.17428)
- [Omni-Embed-Nemotron: A Unified Multimodal Retrieval Model for Text, Image, Audio, and Video](https://arxiv.org/abs/2510.03458)
- [One Embedder, Any Task: Instruction-Finetuned Text Embeddings (INSTRUCTOR)](https://arxiv.org/abs/2212.09741)
- [Qwen-Audio: Advancing Universal Audio Understanding](https://arxiv.org/abs/2311.07919)
- [Qwen2-Audio Technical Report](https://arxiv.org/abs/2407.10759)
- [Qwen2.5-Omni Technical Report](https://arxiv.org/abs/2503.20215)
- [Qwen3-Omni Technical Report](https://arxiv.org/abs/2509.17765)
- [Re-evaluating Minimum Bayes Risk Decoding for Automatic Speech Recognition](https://arxiv.org/abs/2510.19471)
- [Rethinking the Role of Demonstrations: What Makes In-Context Learning Work?](https://arxiv.org/abs/2202.12837)
- [RL with KL penalties is better viewed as Bayesian inference](https://arxiv.org/abs/2205.11275)
- [RLVR Implicitly Incentivizes Correct Reasoning in Base LLMs](https://arxiv.org/abs/2506.14245)
- [Robust Speech Recognition via Large-Scale Weak Supervision (Whisper)](https://arxiv.org/abs/2212.04356)
- [SALMONN: Towards Generic Hearing Abilities for Large Language Models](https://arxiv.org/abs/2310.13289)
- [Scaling Laws for Reward Model Overoptimization](https://arxiv.org/abs/2210.10760)
- [Seamless: Multilingual Expressive and Streaming Speech Translation](https://arxiv.org/abs/2312.05187)
- [SeamlessM4T: Massively Multilingual & Multimodal Machine Translation](https://arxiv.org/abs/2308.11596)
- [Self-Consistency Improves Chain of Thought Reasoning in Language Models](https://arxiv.org/abs/2203.11171)
- [Self-Preference Bias in LLM-as-a-Judge](https://arxiv.org/abs/2410.21819)
- [Show Your Work: Improved Reporting of Experimental Results](https://arxiv.org/abs/1909.03004)
- [SimCSE: Simple Contrastive Learning of Sentence Embeddings](https://arxiv.org/abs/2104.08821)
- [SLURP: A Spoken Language Understanding Resource Package](https://aclanthology.org/2020.emnlp-main.588/)
- [Soft Best-of-n Sampling for Model Alignment](https://arxiv.org/abs/2505.03156)
- [Speaker Verification with Speech-Aware LLMs: Evaluation and Augmentation](https://arxiv.org/abs/2603.10827)
- [Spurious Rewards: Rethinking Training Signals in RLVR](https://arxiv.org/abs/2506.10947)
- [SUPERB: Speech processing Universal PERformance Benchmark](https://arxiv.org/abs/2105.01051)
- [Task Contamination: Language Models May Not Be Few-Shot Anymore](https://ojs.aaai.org/index.php/AAAI/article/view/29808)
- [Task Vectors in In-Context Learning: Emergence, Formation, and Benefits](https://arxiv.org/abs/2501.09240)
- [Test-Time Preference Optimization: On-the-Fly Alignment via Iterative Textual Feedback](https://arxiv.org/abs/2501.12895)
- [The Debate on RLVR Reasoning Capability Boundary: Shrinkage, Expansion, or Both?](https://arxiv.org/abs/2510.04028)
- [The Hitchhiker's Guide to Testing Statistical Significance in NLP](https://aclanthology.org/P18-1128/)
- [The reusable holdout: Preserving validity in adaptive data analysis (Dwork et al., Science 2015)](https://doi.org/10.1126/science.aaa9375)
- [Theoretical Guarantees for Minimum Bayes Risk Decoding (ACL 2025)](https://arxiv.org/abs/2502.12685)
- [Theoretical guarantees on the best-of-n alignment policy](https://arxiv.org/abs/2401.01879)
- [tinyBenchmarks: evaluating LLMs with fewer examples](https://arxiv.org/abs/2402.14992)
- [True Few-Shot Learning with Language Models](https://arxiv.org/abs/2105.11447)
- [TTRL: Test-Time Reinforcement Learning](https://arxiv.org/abs/2504.16084)
- [Tulu 3: Pushing Frontiers in Open Language Model Post-Training](https://arxiv.org/abs/2411.15124)
- [Understanding Contrastive Representation Learning through Alignment and Uniformity on the Hypersphere](https://arxiv.org/abs/2005.10242)
- [UniAudio 1.5: LLM-driven Audio Codec is a Few-shot Audio Task Learner](https://arxiv.org/abs/2406.10056)
- [We Need to Talk about Standard Splits](https://aclanthology.org/P19-1267/)
- [What do self-supervised speech and speaker models learn? New findings from a cross model layer-wise analysis](https://arxiv.org/abs/2401.17632)
- [What Should Not Be Contrastive in Contrastive Learning](https://arxiv.org/abs/2008.05659)
- [With Little Power Comes Great Responsibility](https://arxiv.org/abs/2010.06595)