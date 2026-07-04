# Stage-1 lane X1 — prompt-space quantification methods

> Stage-1 problem-definition campaign lane · 2026-07-04 · workflow `wf_d7b939e9-c37` · methodology:
> CLAUDE.md three-stage section (Stage 1: survey-grounded argumentation; in-house numbers
> directional-only). Yardstick: [[2026-07-04-sufficiency-yardstick-memo]]. Every claim carries
> origin-domain (llm/vlm/speech), transfer-status, fence, ladder-condition and problem-anchor
> tags; every URL adversarially verified; P0 gate enforced (anchor-less claims struck).

## Open problems (P0-compliant: task-level, metric-named, literature-anchored)

### P-X1-1 — ladder: mixed

Audio-LLMs suffer significant instruction sensitivity that degrades task performance: the same audio task under paraphrased or reformatted instructions swings WER/accuracy and instruction-following rates, up to full task flips (SALMONN performing phoneme recognition or translation when prompted for ASR), and no single prompt performs best across cases in LLM-based ASR. The literature's mitigations are gradient-side (instruction-variant fine-tuning, which induces catastrophic forgetting; learned prompt projectors), while the sensitivity is measured but its exploitable headroom is never quantified.

**Metric:** task-performance spread and instruction-following rate across instruction variants (ISA-Bench 3-axis protocol; AudioBench >=20-template robustness; WER variation across prompts in LLM-based ASR)

**Named by:** [ISA-Bench: Benchmarking Instruction Sensitivity for Large Audio Language Models](https://arxiv.org/abs/2510.23558) (2025-10-27) · [AudioBench: A Universal Benchmark for Audio Large Language Models (NAACL 2025)](https://arxiv.org/abs/2406.16020) (2024-06-23) · [Reducing Prompt Sensitivity in LLM-based Speech Recognition Through Learnable Projection](https://arxiv.org/abs/2601.20898) (2026-01-28)

### P-X1-2 — ladder: b1

Single-prompt evaluation misestimates model capability and flips model rankings: semantically-equivalent format changes alone move accuracy by up to 76 points, rankings across 20 models / 39 tasks are unstable under instruction paraphrase, and exhaustive multi-prompt evaluation is unaffordable without budgeted estimators. Any claimed prompt-optimization gain that does not subtract this spread floor is uninterpretable — the same defect transfers directly to every published single-prompt audio-LLM benchmark number.

**Metric:** accuracy spread across plausible formats/paraphrases (points); model-ranking instability; distribution-estimation error at fixed evaluation budget

**Named by:** [Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design (FormatSpread, ICLR 2024)](https://arxiv.org/abs/2310.11324) (2023-10-17) · [State of What Art? A Call for Multi-Prompt LLM Evaluation (TACL 2024)](https://arxiv.org/abs/2401.00595) (2023-12-31) · [Efficient multi-prompt evaluation of LLMs (PromptEval, NeurIPS 2024)](https://arxiv.org/abs/2405.17202) (2024-05-27)

### P-X1-3 — ladder: b2

RL post-training for task adaptation is sample-inefficient — GRPO-class methods often require thousands of rollouts, frequently impractical — and how much of that adaptation is reachable in prompt space on a frozen model is unresolved: GEPA shows prompt evolution beats GRPO by 6% on average and up to 20% with up to 35x fewer rollouts on text tasks, but this prompt-vs-weights headroom comparison exists ONLY for text LLMs; for audio-in omni models the origin-domain strongest baseline (GEPA-vs-GRPO) has no speech counterpart at all.

**Metric:** task accuracy at matched rollout budget (accuracy-per-rollout); prompt-optimized vs RL-fine-tuned score gap

**Named by:** [GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning](https://arxiv.org/abs/2507.19457) (2025-07-25) · [A Systematic Survey of Automatic Prompt Optimization Techniques](https://arxiv.org/abs/2502.16923) (2025-02-24)


## Approach genealogy & evidence claims (cross-domain mandatory)

### X1-01 — [new] origin: **llm** · transfer: untransferred · fence: training-free · ladder: b2 · anchor: P-X1-3

The founding prompt-space quantification template is search-and-score: sample K LLM-generated instruction candidates from demonstrations, score each by execution accuracy on a labeled dev set, take the argmax. APE's selected instructions match or beat human-written instructions on 19/24 instruction-induction tasks; Honovich et al. define the execution-accuracy metric underneath it and show instruction quality is a measurable distribution (InstructGPT reaches 65.7% of human performance, GPT-3 only 9.8% — instruction-induction ability is scale/alignment-emergent). Operationally this protocol IS a labeled estimate of H_prompt(K), making APE the direct transfer template for the omni-speech H_prompt − H_fix probe.

**Sources:** [Large Language Models Are Human-Level Prompt Engineers (APE, ICLR 2023)](https://arxiv.org/abs/2211.01910) (2022-11-03) · [Instruction Induction: From Few Examples to Natural Language Task Descriptions](https://arxiv.org/abs/2205.10782) (2022-05-22) · verified: True

*Origin-domain evidence:* APE ≥ human instructions on 19/24 of the 24-task instruction-induction suite; execution-accuracy metric defined on the same suite (InstructGPT 65.7% of human, GPT-3 9.8%). Both abstracts re-verified verbatim 2026-07-04.
*Speech-domain evidence:* none found — no APE-style K-instruction search-and-score published on any audio-in model (verified-empty searches, re-confirmed by adversarial re-sweep 2026-07-04)

### X1-02 — [new] origin: **llm** · transfer: untransferred · fence: training-free · ladder: b2 · anchor: P-X1-3

OPRO makes the LLM itself the optimizer via a meta-prompt carrying the (prompt, score) trajectory; optimized instructions beat human-designed prompts by up to 8% on GSM8K and up to 50% on Big-Bench Hard — the widest published gains-over-default distribution across tasks. Transfer caveat for the omni setting: Zhang et al. show OPRO collapses on small-scale LLMs (the LLaMA-2 family and Mistral-7B) because limited inference capability constrains optimization ability — so if the frozen omni model must serve as its own optimizer/scorer, headroom realized by OPRO-class loops may be far below headroom that exists.

**Sources:** [Large Language Models as Optimizers (OPRO, ICLR 2024)](https://arxiv.org/abs/2309.03409) (2023-09-07) · [Revisiting OPRO: The Limitations of Small-Scale LLMs as Optimizers](https://arxiv.org/abs/2405.10276) (2024-05-16) · verified: True

*Origin-domain evidence:* Up to +8% GSM8K and up to +50% BBH over human prompts (OPRO abstract, re-verified verbatim 2026-07-04); 'OPRO shows limited effectiveness in small-scale LLMs, with limited inference capabilities constraining optimization ability' (Revisiting OPRO abstract, re-verified).
*Speech-domain evidence:* none found — no OPRO-style meta-prompt optimization on audio-LLMs (verified-empty, re-confirmed 2026-07-04)

### X1-03 — [new] origin: **llm** · transfer: untransferred · fence: training-free · ladder: b2 · anchor: P-X1-3

Evolutionary search over discrete prompt populations — LLMs as crossover/mutation operators inside GA/DE loops — yields up to 25% gains over both human-engineered prompts and prior automatic prompt generation on Big-Bench Hard, evaluated across 31 datasets (EvoPrompt, ICLR 2024); PromptBreeder adds self-referential evolution (mutating the mutation-prompts too) and outperforms Chain-of-Thought and Plan-and-Solve on arithmetic and commonsense benchmarks. Population-based results give the empirical picture of the prompt-fitness landscape whose max defines H_prompt: multimodal, non-smooth, with large gains still uncaptured by single hand prompts.

**Sources:** [EvoPrompt: Connecting LLMs with Evolutionary Algorithms Yields Powerful Prompt Optimizers (ICLR 2024)](https://arxiv.org/abs/2309.08532) (2023-09-15) · [Promptbreeder: Self-Referential Self-Improvement Via Prompt Evolution](https://arxiv.org/abs/2309.16797) (2023-09-28) · verified: True

*Origin-domain evidence:* Up to 25% over prior automatic prompt generation on BBH, 31 datasets, hand-crafted prompts significantly surpassed (EvoPrompt abstract, re-verified 2026-07-04); PromptBreeder outperforms CoT and Plan-and-Solve on arithmetic/commonsense benchmarks and self-referentially improves mutation-prompts (abstract, re-verified verbatim).
*Speech-domain evidence:* partial cousin only: EvoPrompt applied to post-ASR error correction, but on a text LLM over N-best lists (see X1-10)

### X1-04 — [new] origin: **llm** · transfer: untransferred · fence: training-free · ladder: b2 · anchor: P-X1-3

APO/ProTeGi performs textual 'gradient descent': natural-language critiques of the current prompt derived from error batches drive beam search over prompt edits, with bandit-based best-arm selection among candidates; it improves an initial prompt's performance by up to 31% across three NLP benchmarks plus jailbreak detection. Yardstick relevance: it explicitly formalizes candidate-prompt selection as best-arm identification under a fixed evaluation budget — the same statistical problem a budgeted H_prompt estimate on ≤200 speech items must solve.

**Sources:** [Automatic Prompt Optimization with 'Gradient Descent' and Beam Search (EMNLP 2023)](https://arxiv.org/abs/2305.03495) (2023-05-04) · verified: True

*Origin-domain evidence:* Up to 31% improvement over initial prompts on three benchmark NLP tasks plus LLM jailbreak detection; 'beam search and bandit selection procedure' quoted from abstract (re-verified verbatim 2026-07-04).
*Speech-domain evidence:* none found

### X1-05 — [update] origin: **llm** · transfer: untransferred · fence: training-free · ladder: b2 · anchor: P-X1-3

GEPA (reflective Genetic-Pareto prompt evolution) is the literature's only head-to-head quantification of prompt-space vs weight-space headroom: it outperforms GRPO by 6% on average and up to 20% while using up to 35x fewer rollouts, and beats the prior prompt optimizer MIPROv2 by >10% — establishing that for text LLMs a large fraction of RL-post-training gains is reachable in prompt space alone on a frozen model. NEW reading vs archive (A2-09 archived it as a skill-text optimizer / Pareto trust-region instrument): GEPA-vs-GRPO is the measured H_prompt-vs-gradient-headroom ratio, and the exact experiment shape the omni-speech question needs replicated with audio-in tasks.

**Sources:** [GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning](https://arxiv.org/abs/2507.19457) (2025-07-25 (rev 2026-02-14)) · verified: True

*Origin-domain evidence:* Current (rev 2026-02-14) abstract quoted verbatim: 'GEPA outperforms GRPO by 6% on average and by up to 20%, while using up to 35x fewer rollouts'; 'outperforms the leading prompt optimizer, MIPROv2, by over 10% (e.g., +12% accuracy on AIME-2025)' (re-verified 2026-07-04).
*Speech-domain evidence:* none found — no GEPA application to any audio-in model; DD-GEPA (arXiv:2606.07894) is text dialogue disentanglement

### X1-06 — [new] origin: **llm** · transfer: untransferred · fence: training-free · ladder: b1 · anchor: P-X1-2

Semantically-equivalent prompt FORMAT changes alone (spacing, separators, casing) move task accuracy by up to 76 points on LLaMA-2-13B-class models, and sensitivity persists when increasing model size, few-shot examples, or after instruction tuning; FormatSpread is a budgeted bandit-style algorithm that estimates the interval of expected performance over a sampled space of plausible formats without weight access. For the yardstick this is the b1 floor: any measured H_prompt − H_fix on speech tasks must first subtract format-induced spread, which FormatSpread proves can dominate the signal.

**Sources:** [Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design (FormatSpread, ICLR 2024)](https://arxiv.org/abs/2310.11324) (2023-10-17) · verified: True

*Origin-domain evidence:* 'performance differences of up to 76 accuracy points when evaluated using LLaMA-2-13B'; sensitivity 'remains even when increasing model size, the number of few-shot examples, or performing instruction tuning'; FormatSpread 'reports the interval of expected performance without accessing model weights' (abstract re-verified verbatim 2026-07-04).
*Speech-domain evidence:* partial cousin: ISA-Bench includes an output-format axis for audio-LLMs but reports degradation only, never a spread interval or oracle max

### X1-07 — [new] origin: **llm** · transfer: untransferred · fence: training-free · ladder: background · anchor: P-X1-2

The statistical machinery for estimating H_prompt under budget already exists and is task-agnostic: Mizrahi et al. (6.5M instances, 20 models, 39 tasks, 3 benchmarks) show single-prompt evaluation is brittle and flips model rankings across instruction paraphrases, proposing multi-prompt metrics tailored to use cases; PromptEval (NeurIPS 2024) estimates the FULL performance distribution — demonstrated across 100 prompt templates on MMLU — at a budget equivalent to two single-prompt evaluations, with proven consistency, yielding arbitrary quantiles. A max-over-K quantile of that distribution is exactly H_prompt(K) — so a budgeted speech H_prompt probe needs no new estimator, only audio-task instantiation.

**Sources:** [State of What Art? A Call for Multi-Prompt LLM Evaluation (TACL 2024)](https://arxiv.org/abs/2401.00595) (2023-12-31) · [Efficient multi-prompt evaluation of LLMs (PromptEval, NeurIPS 2024)](https://arxiv.org/abs/2405.17202) (2024-05-27) · verified: True

*Origin-domain evidence:* 6.5M instances, 20 LLMs, 39 tasks from 3 benchmarks with ranking instability (Mizrahi abstract, re-verified 2026-07-04); PromptEval 'accurately estimate[s] performance quantiles across 100 prompt templates on MMLU with a budget equivalent to two single-prompt evaluations' and 'consistently estimates the performance distribution' (abstract, re-verified verbatim).
*Speech-domain evidence:* none found — no PromptEval/FormatSpread-style distribution estimation run on any audio-LLM benchmark (verified-empty, re-confirmed 2026-07-04)

### X1-08 — [new] origin: **vlm** · transfer: untransferred · fence: training-free · ladder: b2 · anchor: P-X1-3

Prompt-space optimization has crossed one modality boundary already — vision: an LLM used as a black-box optimizer over CLIP text prompts (conversational hill-climbing on scored prompt history) beats the gradient-trained soft-prompt method CoOp by 1.5% average across 11 datasets in one-shot classification and outperforms human- and LLM-generated prompts, with prompts that transfer across VLM architectures (CVPR 2024); IPO (NeurIPS 2024) likewise improves on gradient-based prompt learning while keeping prompts human-readable and generalizing better. Two lessons for speech: the training-free variant can beat the gradient-trained one, and absolute headroom on contrastive/perception models is smaller (~1-3%) than on generative-LLM reasoning tasks (8-50%).

**Sources:** [Language Models as Black-Box Optimizers for Vision-Language Models (CVPR 2024)](https://arxiv.org/abs/2309.05950) (2023-09-12) · [IPO: Interpretable Prompt Optimization for Vision-Language Models (NeurIPS 2024)](https://arxiv.org/abs/2410.15397) (2024-10-20) · verified: True

*Origin-domain evidence:* 'surpasses the white-box continuous prompting method (CoOp) by an average of 1.5% across 11 datasets' in 1-shot classification, beats human- and LLM-generated prompts, prompts 'transfer well across different VLM architectures' (abstract re-verified 2026-07-04; CVPR 2024 venue confirmed via openaccess.thecvf.com); IPO improves accuracy of gradient-descent-based prompt learning with human-comprehensible prompts and better generalization across 11 datasets (re-verified).
*Speech-domain evidence:* none found — no analogous LLM-as-optimizer prompt search over an audio-in model

### X1-09 — [new] origin: **speech** · transfer: native · fence: training-free · ladder: b2 · anchor: P-X1-3

Hand-crafted prompt engineering on FROZEN Whisper — no weight updates — improves zero-shot audio-visual speech recognition, code-switched ASR, and unseen-pair speech translation by 10% to 45% relative over default prompts, in some cases beating supervised SOTA. This is the strongest native speech-domain evidence that prompt space carries genuine (b2) task headroom on a frozen speech model; but it is a two-point comparison (default vs designed prompt), not a K-instruction distribution, so it demonstrates H_prompt − H_fix > 0 without bounding it.

**Sources:** [Prompting the Hidden Talent of Web-Scale Speech Models for Zero-Shot Task Generalization](https://arxiv.org/abs/2305.11095) (2023-05-18) · verified: True

*Origin-domain evidence:* 10-45% improvement over default prompts on the three zero-shot tasks (AVSR, code-switched ASR, unseen-pair ST) on frozen Whisper, 'even outperform SotA supervised models on some datasets' (abstract re-verified 2026-07-04).
*Speech-domain evidence:* native — this IS the speech-domain evidence; Whisper-class encoder-decoder, not an instruct omni-LLM

### X1-10 — [new] origin: **llm** · transfer: partial · fence: training-free · ladder: b2 · anchor: P-X1-3

The only published automatic prompt OPTIMIZER inside a speech pipeline is evolutionary prompt design for LLM-based post-ASR generative error correction (SLT 2024 GenSEC challenge, CHiME-4 subset of Task 1): EvoPrompt-class evolution of the correction prompt. But the optimized model is a TEXT LLM consuming ASR N-best hypothesis lists — the audio-in prompt space of the recognizer itself is untouched. It therefore quantifies H_prompt of the text corrector, not of the speech model, and the omni audio-in cell remains empty.

**Sources:** [Evolutionary Prompt Design for LLM-Based Post-ASR Error Correction (SLT 2024 GenSEC)](https://arxiv.org/abs/2407.16370) (2024-07-23) · verified: True

*Origin-domain evidence:* Abstract re-verified 2026-07-04: 'evolutionary prompt optimization algorithm to refine the initial prompts', evaluated on 'the CHiME-4 subset of the Task 1 of the SLT 2024 GenSEC challenge', in-context prompting of LLMs over an N-best list of ASR hypotheses. EvoPrompt method origin: arXiv:2309.08532.
*Speech-domain evidence:* partial — applied in the ASR pipeline (CHiME-4 GenSEC) but on text N-best input; abstract states 'effectiveness and potential' without WER deltas (re-confirmed: no numbers in abstract; full-text fetch blocked)

### X1-11 — [new] origin: **speech** · transfer: native · fence: training-free · ladder: b1 · anchor: P-X1-1

AudioBench (NAACL 2025) is the first audio-LLM benchmark to institutionalize multi-prompt evaluation: at least 20 diverse prompt templates per task (for tasks lacking native diversity), after a 3-template probe showed instruction sensitivity is 'even more severe in AudioLLMs' than in text LLMs — under some ASR prompts SALMONN flips task entirely (performs phoneme recognition on LibriSpeech/Tedlium, or speech translation on CommonVoice, instead of transcription) while Qwen-Audio stays stable across all three templates. Crucially it reports robustness/spread only, never the max-over-templates oracle — sensitivity is measured, headroom is not. The task-flip finding also shows the b1/b2 split is confounded at the task-activation level in audio models.

**Sources:** [AudioBench: A Universal Benchmark for Audio Large Language Models (NAACL 2025)](https://arxiv.org/abs/2406.16020) (2024-06-23) · [AudioBench NAACL 2025 camera-ready (prompt-robustness section)](https://aclanthology.org/2025.naacl-long.218/) (2025-04) · verified: True

*Origin-domain evidence:* Quoted from arXiv HTML v5 (re-verified verbatim 2026-07-04): 'it is even more severe in AudioLLMs due to the complexity of processing multiple modalities'; 'we incorporate at least 20 diverse prompt templates into our evaluation framework for the tasks without diverse prompts originally'; SALMONN 'tends to conduct phoneme recognition' (LibriSpeech/Tedlium) and 'tends to perform speech translation' (CommonVoice) under certain ASR prompts while 'Qwen-Audio's performance remains stable across all three prompt templates'. ACL Anthology entry confirmed as NAACL 2025, pp. 4297-4316.
*Speech-domain evidence:* native

### X1-12 — [new] origin: **speech** · transfer: native · fence: training-free · ladder: b1 · anchor: P-X1-1

ISA-Bench (2025-10) is the first dedicated instruction-sensitivity benchmark for large audio-language models: instructions varied along three axes — description phrasing, output format, task composition — with description variants spanning punctuation, case, robustness (syntax/lexical errors), and three semantic-complexity levels (simple/neutral/complex), and format variants including case transforms, tag-wrapped and JSON-style outputs; it measures both instruction-following rate and task performance. Even SOTA LALMs suffer significant sensitivity with degraded performance on fundamental audio tasks. The gradient-side mitigation — fine-tuning Qwen2-Audio on a complex instruction-variant set — improves compliance but triggers catastrophic forgetting, a documented cost a training-free prompt-side solution would not pay. It measures sensitivity only; no prompt optimization or oracle headroom.

**Sources:** [ISA-Bench: Benchmarking Instruction Sensitivity for Large Audio Language Models](https://arxiv.org/abs/2510.23558) (2025-10-27) · verified: True

*Origin-domain evidence:* Three-axis sensitivity protocol (instruction description, output format, task composition) affecting 'both (i) instruction-following rates and (ii) task performance'; fine-tuning Qwen2-Audio on instruction variants 'induces nontrivial catastrophic forgetting' (abstract + HTML re-verified 2026-07-04; VERIFIER CORRECTION: 'seven variants per task' unsupported — Table 3 shows five description-axis and four format-axis variation subclasses; three semantic-complexity levels confirmed as 'simple, neutral, complex').
*Speech-domain evidence:* native

### X1-13 — [new] origin: **speech** · transfer: native · fence: trained-head-on-frozen · ladder: b2 · anchor: P-X1-1

For LLM-based ASR, prompt choice 'significantly affects ASR performance and introduces instability, with no single prompt performing best across all cases' (2026-01); the proposed fix is a gradient-TRAINED prompt-projector module that learns to project prompt embeddings to more effective regions of the LLM input space, model-agnostic and without modifying the underlying LLM-based ASR model. This is the fine-tuned-side answer to speech prompt sensitivity — and indirect evidence that better prompt regions EXIST for speech tasks (they are reachable by a learned projection), i.e., H_prompt − H_fix is nonzero in embedding space even where discrete-prompt search has not been tried.

**Sources:** [Reducing Prompt Sensitivity in LLM-based Speech Recognition Through Learnable Projection](https://arxiv.org/abs/2601.20898) (2026-01-28) · verified: True

*Origin-domain evidence:* Abstract re-verified verbatim 2026-07-04: 'prompt choice significantly affects ASR performance and introduces instability, with no single prompt performing best across all cases'; module 'learns to project prompt embeddings to more effective regions of the LLM input space, without modifying the underlying LLM-based ASR model'; consistent improvements across four datasets.
*Speech-domain evidence:* native


## Training-free vs fine-tuned SOTA positioning

## Positioning: training-free vs fine-tuned for prompt-space quantification

**Training-free side (in-fence).** The entire quantification apparatus is training-free by construction: APE search-and-score (19/24 tasks >= human), OPRO meta-prompt optimization (+8% GSM8K / +50% BBH), EvoPrompt/PromptBreeder evolutionary search (up to 25% BBH), APO textual gradients + bandit selection (up to 31%), GEPA reflective Pareto evolution (+6% avg / +20% max over GRPO at up to 35x fewer rollouts), FormatSpread budgeted spread intervals, PromptEval consistent distribution estimation at ~2x single-prompt cost. In vision, the training-free LLM-as-black-box-optimizer *beats* the gradient-trained soft-prompt baseline CoOp (+1.5% avg, one-shot, 11 datasets), and IPO repeats the result with better generalization — the one modality-transfer precedent, and it favored training-free. In speech, the only in-fence headroom datum is hand-crafted: prompting frozen Whisper +10–45% relative on three zero-shot tasks.

**Fine-tuned side (out-of-fence, positioning only).** Speech responses to prompt sensitivity are so far all gradient-side: ISA-Bench fine-tunes Qwen2-Audio on instruction variants (compliance improves, catastrophic forgetting appears); the 2026 learnable prompt-projector trains a small projection module in front of a frozen LLM-based ASR backbone (trained-head-on-frozen) to stabilize WER across prompts; soft-prompt tuning (SpeechPrompt lineage, arXiv:2203.16773) trains continuous prompts on frozen speech LMs. Notably, the fine-tuned side's *existence* concedes the training-free side's premise: better prompt regions exist on frozen speech models — they are currently reached by trained projections rather than searched discrete prompts.

**The gap this lane certifies.** Sensitivity measurement on audio-LLMs EXISTS (ISA-Bench 3-axis protocol; AudioBench >=20 templates; both 2024–25); optimization-headroom measurement DOES NOT — no APE/OPRO/GEPA-class search, no max-over-K oracle, no FormatSpread-style interval has ever been published for an audio-in model. The prompt-optimization field's own modality expansion confirms the hole from the other side: Multimodal Prompt Optimization (MPO, arXiv:2510.09201, rev 2026-02) extends APO-class search to images, videos, and even molecules — audio is absent from both its experiments and its framing (full-text verified). Meanwhile every estimator needed to fill the cell (PromptEval quantiles, FormatSpread intervals, APE/APO budgeted selection) is published, task-agnostic, and training-free. Scale caveat for Stage-2 design: Revisiting-OPRO shows self-optimization collapses below a capability threshold, so the probe should score prompts by task metric (WER/accuracy), not rely on the omni model optimizing itself.

## Negative findings (verified-empty searches & P0 strikes — first-class results)

- VERIFIED EMPTY (4 query formulations 2026-07-04, plus 2 independent adversarial re-sweep searches by the verifier, same date): no APE/OPRO/GEPA/EvoPrompt/PromptBreeder-class automatic prompt optimization has been applied to any audio-in LLM (Qwen2-Audio, SALMONN, Qwen2.5/3-Omni class). Nearest neighbors are a text-LLM-over-N-best GER prompt evolution (arXiv:2407.16370) and hand-crafted frozen-Whisper prompting (arXiv:2305.11095). H_prompt(T,K,N) has never been published for an omni speech model — the yardstick memo's 'zero published quantification' verdict SURVIVES this sweep and the adversarial re-sweep.
- NEAREST MISS, strengthens the empty cell (verifier addition, 2026-07-04): Multimodal Prompt Optimization (MPO, arXiv:2510.09201, rev 2026-02-19) extends automatic prompt optimization beyond text to images, videos, and molecules (PlantVillage, CUB, SLAKE, RSVQA, DrivingVQA, Drive&Act, VANE-Bench, molecular property tasks; Qwen2.5-VL/Qwen3/Gemma3/InternVL backbones) — full text checked: NO audio or speech task, dataset, or model anywhere in experiments or appendix. The modality frontier of prompt optimization has crossed vision and molecules while leaving audio empty.
- REFINEMENT of the expected-empty: prompt-SENSITIVITY quantification on audio-LLMs DOES exist — ISA-Bench (arXiv:2510.23558, 3-axis instruction-sensitivity benchmark) and AudioBench (arXiv:2406.16020, >=20 prompt templates per task) — but both report spread/robustness only and never the max-over-K oracle, and neither optimizes prompts. The sensitivity-to-headroom step (spread is measured, the exploitable maximum is not) is the precise unoccupied cell between ISA-Bench and the APE/OPRO literature.
- The systematic survey of automatic prompt optimization (arXiv:2502.16923, 2025, 5-part unifying framework) covers no audio or speech domain — confirming from the prompt-optimization side of the fence that the field has not crossed into audio.
- No FormatSpread/PromptEval-style budgeted spread-interval or performance-distribution estimation has been run on any audio-LLM benchmark (searched 2026-07-04, empty) — multi-template audio evaluations (AudioBench, ISA-Bench) average over templates rather than estimate the distribution or its quantiles.
- Full-text WER numbers for arXiv:2407.16370 (evolutionary GER prompts) could not be verified — the abstract states 'effectiveness and potential' without numbers (re-confirmed by verifier 2026-07-04); the claim (X1-10) is therefore stated without effect sizes.
- VERIFIER CORRECTIONS applied to the input set: (1) X1-12/P-X1-1's 'seven variants per task' for ISA-Bench is unsupported by the paper (Table 3 shows five description-axis + four format-axis variation subclasses; three semantic-complexity levels 'simple, neutral, complex' confirmed) — reworded. (2) X1-02's 'LLaMA-2-7B/13B' over-specified vs the abstract's 'LLaMA-2 family and Mistral 7B' — softened. (3) X1-07's '100+ prompt templates' corrected to PromptEval's demonstrated 100 templates on MMLU. (4) X1-13's fence retagged gradient-trained -> trained-head-on-frozen (projector trained, LLM-ASR backbone explicitly unmodified). (5) GEPA numbers (+6% avg) confirmed against the CURRENT rev 2026-02-14 abstract — note the original v1 abstract circulated with different figures, so downstream citations should pin the revision. All 19 unique source URLs resolve; X1-05 'update' delta confirmed (GEPA already archived in agent-skills lane A2); all other sources absent from wiki/survey archive, 'new' deltas confirmed by grep.