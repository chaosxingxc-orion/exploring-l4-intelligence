# Stage-1 lane X3 — LLM/VLM test-time methodology map

> Stage-1 problem-definition campaign lane · 2026-07-04 · workflow `wf_d7b939e9-c37` · methodology:
> CLAUDE.md three-stage section (Stage 1: survey-grounded argumentation; in-house numbers
> directional-only). Yardstick: [[2026-07-04-sufficiency-yardstick-memo]]. Every claim carries
> origin-domain (llm/vlm/speech), transfer-status, fence, ladder-condition and problem-anchor
> tags; every URL adversarially verified; P0 gate enforced (anchor-less claims struck).

## Open problems (P0-compliant: task-level, metric-named, literature-anchored)

### PR-X3-1 — ladder: c

Intrinsic self-correction deficit: LLMs cannot reliably detect or correct their own reasoning errors without external feedback; post-correction accuracy frequently drops below the initial answer, and the failure is localized in error DETECTION, not revision. Speech instantiation already visible: LLM-based ASR correctors fabricate content absent from the audio unless a verification stage is added.

**Metric:** accuracy delta (post-correction minus initial answer) and error-detection F1; speech: WER/entity-error delta of corrector vs pass-through plus hallucination rate

**Named by:** [Large Language Models Cannot Self-Correct Reasoning Yet (ICLR 2024)](https://arxiv.org/abs/2310.01798) (2023-10-03) · [When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey (TACL 2024)](https://arxiv.org/abs/2406.01297) (2024-06-03) · [Fewer Hallucinations, More Verification: A Three-Stage LLM-Based Framework for ASR Error Correction](https://arxiv.org/abs/2505.24347) (2025-05-30)

### PR-X3-2 — ladder: c

Critique bottleneck in multimodal self-improvement: across 24 LVLMs, human-written critiques substantially raise post-correction accuracy while model-generated critiques are less helpful and sometimes detrimental — critique, not correction, is the bottleneck. No audio-LLM critique/correction benchmark exists at all (verified-empty), so the speech version of this deficiency is unmeasured.

**Metric:** VISCO critique F1 and post-correction accuracy gain (human-critique vs self-critique arms); audio analog undefined — itself the gap

**Named by:** [VISCO: Benchmarking Fine-Grained Critique and Correction Towards Self-Improvement in Visual Reasoning (CVPR 2025)](https://arxiv.org/abs/2412.02172) (2024-12-03) · [Self-Correction is More than Refinement: A Learning Framework for Visual and Language Reasoning Tasks (ACL 2025 Findings)](https://arxiv.org/abs/2410.04055) (2024-10-05)

### PR-X3-3 — ladder: mixed

Multimodal ICL is text/format-driven, not perceptually grounded: in VLMs, in-context demonstrations act almost entirely through the text modality (images in demos contribute little; retrieval-based demo selection collapses to majority voting over context labels); in audio-LLMs, demos improve format compliance but degrade task accuracy (ALICE). The b1(format)/b2(accuracy) split of any demo-driven lift is uncontrolled in standard evaluations.

**Metric:** accuracy delta of multimodal demos vs text-only/format-only/shuffled-label controls (b1/b2 split ablation); ALICE-style format-compliance vs task-accuracy divergence

**Named by:** [What Makes Multimodal In-Context Learning Work? (CVPRW 2024)](https://arxiv.org/abs/2404.15736) (2024-04-24) · [ALICE: A Multifaceted Evaluation Framework of Large Audio-Language Models' In-Context Learning Ability](https://arxiv.org/abs/2603.20433) (2026-03-25)

### PR-X3-4 — ladder: mixed

Prompt/instruction-space headroom is quantified only in text: semantically-equivalent formats spread accuracy by up to 76 points (FormatSpread), and optimized instructions beat human prompts by 8-50% (OPRO) or beat GRPO fine-tuning outright (GEPA). Audio-LLM instruction sensitivity is documented only as seen/unseen task drops (Dynamic-SUPERB); no spread- or headroom-style measurement (H_prompt-type) exists for any audio/omni model — the owner question's operationalization has zero published data points.

**Metric:** task-metric max-gain and spread over K semantically-equivalent or search-optimized instructions at fixed sampling budget (H_prompt vs H_fix)

**Named by:** [Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design (FormatSpread, ICLR 2024)](https://arxiv.org/abs/2310.11324) (2023-10-17) · [Large Language Models as Optimizers (OPRO)](https://arxiv.org/abs/2309.03409) (2023-09-07) · [GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning (ICLR 2026 Oral)](https://arxiv.org/abs/2507.19457) (2025-07-25) · [Dynamic-SUPERB: instruction-tuning benchmark for speech](https://arxiv.org/abs/2309.09510) (2023-09-18)

### PR-X3-5 — ladder: b2

Test-time compute helps reasoning, not perception: CoT's gains concentrate on math/symbolic tasks (meta-analysis over 100+ papers, 20 datasets, 14 models); on VLMs, test-time scaling improves multi-step reasoning but yields only limited gains on perception-focused benchmarks, with iterative refinement often DEGRADING open-source VLMs; the audio replication shows CoT helps easy/medium tasks and hurts hard ones in LALMs. Perception-shaped speech tasks (ASR, SER) therefore lack a demonstrated TTC lever.

**Metric:** per-task-category accuracy delta from CoT/test-time-compute at matched budget (reasoning-shaped vs perception-shaped task families)

**Named by:** [To CoT or not to CoT? Chain-of-thought helps mainly on math and symbolic reasoning](https://arxiv.org/abs/2409.12183) (2024-09-18) · [Limits and Gains of Test-Time Scaling in Vision-Language Reasoning](https://arxiv.org/abs/2512.11109) (2025-12-11) · [Audio-CoT: Exploring Chain-of-Thought Reasoning in Large Audio Language Model](https://arxiv.org/abs/2501.07246) (2025-01-13)

### PR-X3-6 — ladder: c

Coverage-realization gap: repeated sampling grows pass@N coverage log-linearly over four orders of magnitude, but in domains without automatic verifiers, label-free selection (majority voting, reward models) plateaus far below coverage; in text-math the gap is closed mostly by TRAINED verifiers. In speech, house measurements put deployable label-free capture at ~0% of real oracle headroom (stage-1 directional, in-repo), and the strongest published audio counter-evidence (frozen-GPT-4o-verifier selection) exists only on synthetic auditory-cognition tasks.

**Metric:** realized fraction rho = label-free selector gain / oracle(pass@N or best-of-N) gain, per task family

**Named by:** [Large Language Monkeys: Scaling Inference Compute with Repeated Sampling](https://arxiv.org/abs/2407.21787) (2024-07-31) · [On the Self-Verification Limitations of Large Language Models on Reasoning and Planning Tasks](https://arxiv.org/abs/2402.08115) (2024-02-12) · [Scaling Auditory Cognition via Test-Time Compute in Audio Language Models](https://arxiv.org/abs/2503.23395) (2025-03-30)


## Approach genealogy & evidence claims (cross-domain mandatory)

### X3-01 — [update] origin: **llm** · transfer: native · fence: training-free · ladder: a · anchor: PR-X3-6

Test-time scaling family, support side: repeated sampling makes coverage (pass@N) grow log-linearly over four orders of magnitude of N (modelable as an exponentiated power law), and compute-optimally allocated test-time compute can outperform a ~14x larger model — establishing (a)-type SUPPORT headroom as a generic property of frozen samplers. Speech transfer column: maps NATIVELY to the 30-year ASR/ST n-best oracle-gap literature and to pass@k on SQA; the frozen-omni analog is the house best-of-N oracle headroom. VLM failure column: coverage converts to realized accuracy only where answers are automatically checkable; on perception-focused VLM benchmarks TTS gains are limited (Limits-and-Gains study).

**Sources:** [Large Language Monkeys: Scaling Inference Compute with Repeated Sampling](https://arxiv.org/abs/2407.21787) (2024-07-31) · [Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters](https://arxiv.org/abs/2408.03314) (2024-08-06) · verified: True

*Origin-domain evidence:* Coverage scales log-linearly across SWE-bench Lite/MATH/coding over 4 orders of magnitude of samples (2407.21787); compute-optimal test-time strategy beats best-of-N baseline at ~4x less compute and can beat a 14x larger model (2408.03314).
*Speech-domain evidence:* House: greedy WER 0.1183 -> oracle@8 0.0765 (+0.0418, CI [0.0289,0.0564]) on frozen Qwen3-Omni-30B at SNR-5 (stage-1 directional, in-repo _repro/asr_bon_llamacpp_snr5.json; numbers re-verified against the artifact 2026-07-04); archive: MBR-ASR beats beam search on Whisper (arXiv:2510.19471).

### X3-02 — [new] origin: **llm** · transfer: untransferred · fence: trained-head-on-frozen · ladder: c · anchor: PR-X3-6

Verifier-guided selection: the realized fraction of best-of-N coverage in text-math comes overwhelmingly from TRAINED verifiers — outcome verifiers (Cobbe) and process reward models (Lightman: PRM-reranking solves ~78% of a MATH subset, beating ORM and majority voting) — and PRM-guided tree/beam search beats plain BoN at low budgets (Snell). Speech transfer column: trained ASR rerankers exist but are out-of-fence for the house thesis; the in-fence transfer candidates are frozen-judge rescoring for ASR/SLU and verifiable-reward selection for speech-agentic tasks (the named untried Part-A selector families). VLM failure column: multimodal verifiers must be separately trained; VLM self-verification exhibits agreement bias, so the text recipe does not transfer for free.

**Sources:** [Training Verifiers to Solve Math Word Problems](https://arxiv.org/abs/2110.14168) (2021-10-27) · [Let's Verify Step by Step](https://arxiv.org/abs/2305.20050) (2023-05-31) · [Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters](https://arxiv.org/abs/2408.03314) (2024-08-06) · verified: True

*Origin-domain evidence:* GSM8K verifier-reranked sampling beats a ~30x larger unverified model (6B+verification vs 175B, 2110.14168); process supervision 78%+ on MATH-subset best-of-N reranking (2305.20050).
*Speech-domain evidence:* none found — no process/outcome reward model for audio-LLM candidate selection surfaced; WavReward (arXiv:2505.09558) is an outcome-level spoken-dialogue evaluator, not a selection PRM

### X3-03 — [new] origin: **llm** · transfer: untransferred · fence: gradient-trained · ladder: background · anchor: PR-X3-5

Budget forcing / sequential test-time scaling (s1): appending 'Wait' to force longer reasoning lifts competition-math accuracy (s1-32B exceeds o1-preview by up to 27% on MATH/AIME24) — but the recipe requires 1k-sample reasoning SFT first; no training-free budget-forcing result on frozen non-reasoning models exists. Speech transfer column: audio reasoning models (Audio-Reasoner, Step-Audio-R1) install thinking via gradient training (Step-Audio-R1 via Modality-Grounded Reasoning Distillation), so the training-free cell for frozen omni models is empty; SQA/agentic are the only plausible targets given PR-X3-5. VLM failure column: thinking-with-images exhibits the named 'grounding paradox' — the model must decide where to attend BEFORE it has the visual evidence needed to make that decision correctly, leaving long reasoning chains brittle at fine-grained grounding (TTSP resolves it by scaling perception, not thought) — a direct caution for long audio-reasoning chains over acoustic evidence.

**Sources:** [s1: Simple test-time scaling](https://arxiv.org/abs/2501.19393) (2025-01-31) · [Test-time Scaling over Perception: Resolving the Grounding Paradox in Thinking with Images](https://arxiv.org/abs/2604.11025) (2026-04-13) · [Step-Audio-R1 Technical Report](https://arxiv.org/abs/2511.15848) (2025-11-19) · verified: True

*Origin-domain evidence:* s1-32B + budget forcing scales with thinking tokens and exceeds o1-preview by up to 27% on competition math (2501.19393).
*Speech-domain evidence:* gradient-trained only: Audio-Reasoner (arXiv:2503.02318), Step-Audio-R1 (arXiv:2511.15848); no training-free budget forcing on frozen audio/omni models found

### X3-04 — [update] origin: **llm** · transfer: native · fence: training-free · ladder: c · anchor: PR-X3-6

Self-consistency family extension: Universal Self-Consistency (USC) replaces exact-match majority voting with LLM-selection of the most mutually-consistent candidate, matching SC on math and extending consensus selection to free-form generation (open-ended QA, summarization, and code without execution). Speech transfer column: closed-form SLU/SQA voting is native; ASR's native analog is MBR; free-form spoken-QA via USC-style frozen-judge consensus is a direct untried candidate on omni models. VLM failure column: USC inherits LLM-judge position/self-preference biases (archived), and on VLMs consensus gains concentrate on reasoning, not perception benchmarks; Baldassini shows demo-retrieval 'advanced ICL' collapses to majority voting over context labels — consensus can be a label-prior artifact rather than perceptual evidence.

**Sources:** [Universal Self-Consistency for Large Language Model Generation](https://arxiv.org/abs/2311.17311) (2023-11-29) · [Self-Consistency Improves Chain of Thought Reasoning in Language Models](https://arxiv.org/abs/2203.11171) (2022-03-21) · [Scaling Auditory Cognition via Test-Time Compute in Audio Language Models](https://arxiv.org/abs/2503.23395) (2025-03-30) · verified: True

*Origin-domain evidence:* USC matches standard SC on math without answer extraction and improves open-ended QA/summarization/code (2311.17311); SC +17.9% GSM8K (archived 2203.11171).
*Speech-domain evidence:* temperature-based majority voting is one of five TTC methods validated on five frozen audio LLMs with 9-150% relative gains on auditory-cognition tasks (2503.23395); house caveat: MBR null on two deployment ASR slices (stage-1 directional, MBR n.s. at N=8 in _repro/asr_bon_llamacpp_snr5.json)

### X3-05 — [new] origin: **llm** · transfer: partial · fence: training-free · ladder: c · anchor: PR-X3-1

The critical self-correction literature: intrinsic self-correction (no external feedback) largely fails and often DEGRADES accuracy (Huang, ICLR 2024); the TACL survey isolates when it works — reliable external/verifiable feedback, tasks where errors are detectable, and decomposing detection from revision. Speech transfer column: LLM-based ASR correction already exhibits the predicted pathology — correctors hallucinate content absent from the audio, and the working fixes are verification-first pipelines (error pre-detection + verification stages, e.g., RLLM-CF), i.e., exactly the external-feedback condition; SLU/SQA self-correction on frozen omni models is unmeasured. VLM failure column: identical signature amplified — self-critique detrimental (VISCO), and VLMs fail to self-correct during iterative inference without fine-tuning or external feedback.

**Sources:** [Large Language Models Cannot Self-Correct Reasoning Yet (ICLR 2024)](https://arxiv.org/abs/2310.01798) (2023-10-03) · [When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs (TACL 2024)](https://arxiv.org/abs/2406.01297) (2024-06-03) · [Fewer Hallucinations, More Verification: A Three-Stage LLM-Based Framework for ASR Error Correction](https://arxiv.org/abs/2505.24347) (2025-05-30) · verified: True

*Origin-domain evidence:* GPT-4-class models degrade after intrinsic self-correction on GSM8K/CommonSenseQA/HotpotQA (2310.01798); survey verdict: no successful self-correction with self-generated feedback except on exceptionally suited tasks; reliable external feedback is the working condition (2406.01297).
*Speech-domain evidence:* generative ASR correctors introduce hallucination errors absent from audio; three-stage verification framework (RLLM-CF: error pre-detection, CoT iterative correction, reasoning verification) mitigates — 9-21% relative CER/WER reductions with GPT-4o (2505.24347) — partial replication of the text failure mode in speech

### X3-06 — [new] origin: **llm** · transfer: untransferred · fence: training-free · ladder: c · anchor: PR-X3-1

Self-verification asymmetry: on Game-of-24, graph coloring, and STRIPS planning, GPT-4 iterative self-critique does not improve and can hurt performance; gains reappear only with external SOUND verifiers — self-improvement presumes verification is easier than generation, which holds only for formally checkable tasks. Speech transfer column: ASR possesses cheap near-sound external verifiers (forced-alignment/CTC consistency scores, acoustic re-synthesis match) that could play the sound-verifier role training-free, and speech-agentic tasks with programmatic success checks are the (c)-easiest habitat (yardstick §6) — both untried on frozen omni. VLM failure column: MLLM verifiers over-validate agent behavior (named 'agreement bias'); Self-Grounded Verification — generating expectations BEFORE seeing the actor's output — recovers +25pp failure detection, replicating the asymmetry cross-modally.

**Sources:** [On the Self-Verification Limitations of Large Language Models on Reasoning and Planning Tasks](https://arxiv.org/abs/2402.08115) (2024-02-12) · [Let's Think in Two Steps: Mitigating Agreement Bias in MLLMs with Self-Grounded Verification](https://arxiv.org/abs/2507.11662) (2025-07-15) · verified: True

*Origin-domain evidence:* Systematic GPT-4 study across three formal domains: self-critique loops fail; external sound verification restores gains (2402.08115).
*Speech-domain evidence:* none found — no study using acoustic external verifiers (forced alignment/CTC) as the sound-verifier arm of a self-correction loop on audio-LLMs

### X3-07 — [update] origin: **llm** · transfer: untransferred · fence: training-free · ladder: b2 · anchor: PR-X3-1

Refinement-with-external-feedback family: Self-Refine gains ~20% average over one-step generation using self-feedback on preference-shaped tasks (weaker on reasoning); CRITIC shows tool-grounded critique (search engines, interpreters) reliably improves while critique-only does not; Reflexion converts sparse environment reward into verbal memory across retries. Speech transfer column: the direct candidate is speech-agentic tasks with verifiable rewards (tool-use, tau2-style envs) where feedback is external by construction; within-session retry loops are in-fence, but Reflexion-style CROSS-SESSION accumulation collides with the closed NO-GO question (r1-r3) and is flagged, not proposed. VLM failure column: intrinsic refinement amplifies hallucination; Woodpecker-style correction works only by importing external expert models (grounding tools).

**Sources:** [Self-Refine: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.17651) (2023-03-30) · [CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing](https://arxiv.org/abs/2305.11738) (2023-05-19) · [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) (2023-03-20) · [Woodpecker: Hallucination Correction for Multimodal Large Language Models](https://arxiv.org/abs/2310.16045) (2023-10-24) · verified: True

*Origin-domain evidence:* ~20% absolute average improvement across 7 tasks with GPT-3.5/4 (2303.17651); CRITIC: tool-interactive critique improves QA/program/toxicity while self-only critique stagnates (2305.11738).
*Speech-domain evidence:* none found — no refinement-loop study with verifiable speech rewards on frozen audio/omni models

### X3-08 — [update] origin: **llm** · transfer: untransferred · fence: trained-head-on-frozen · ladder: c · anchor: PR-X3-6

Inference-time alignment family: frozen LLMs are aligned at decoding time — ARGS scores each token with a reward model during search (+19.56% average reward vs baseline, 64.33% GPT-4 preference/tie); DeAL frames decoding as heuristic-guided search over programmable alignment objectives (ACL 2025); RAIN self-evaluates and rewinds with NO reward model and no training. These generalize sequence-level BoN (archived Controlled Decoding) to token/segment-level tilts of q0. Speech transfer column: token/segment-level reward-guided decoding with verifiable speech rewards (entity match, WER-proxy) on a frozen omni model is unoccupied — W1's machinery is sequence-level BoN only; this is the natural instrument for the named S6-residual per-token-logprob selector family. VLM failure column: value-guided decoding needs calibrated per-token rewards; multimodal reward models are scarce and judge biases transfer, so the guidance signal is the bottleneck.

**Sources:** [ARGS: Alignment as Reward-Guided Search (ICLR 2024)](https://arxiv.org/abs/2402.01694) (2024-02-02) · [RAIN: Your Language Models Can Align Themselves without Finetuning (ICLR 2024)](https://arxiv.org/abs/2309.07124) (2023-09-13) · [DeAL: Decoding-time Alignment for Large Language Models (ACL 2025)](https://arxiv.org/abs/2402.06147) (2024-02-05) · verified: True

*Origin-domain evidence:* ARGS +19.56% average reward and 64.33% GPT-4 preference-or-tie on HH-RLHF-style eval (2402.01694); RAIN aligns frozen LLMs via self-evaluation+rewind with zero training (2309.07124).
*Speech-domain evidence:* none found — no reward-guided decoding or rewind-style inference alignment on frozen speech/audio LLMs

### X3-09 — [update] origin: **llm** · transfer: partial · fence: training-free · ladder: background · anchor: PR-X3-3

ICL theory: in-context learning is implicit Bayesian task inference — demonstrations LOCATE latent tasks acquired in pretraining rather than teach new ones (Xie et al.), consistent with label-insensitivity (Min, archived) and compact task/function vectors (archived). Consequence for the yardstick: the K-instruction space in H_prompt operationalizes task-posterior sharpening, not capability injection, so (b)-headroom is upper-bounded by pretrained support — prompting cannot move mass that q0 lacks. Speech transfer column: ALICE plus the induction-heads analysis (archived) match the theory — audio demos trigger copy/format mechanisms, not semantic grounding — so SLU/SQA task-definition prompting should sharpen posteriors only over trained task families. VLM failure column: the task posterior is dominated by text tokens (Baldassini), predicting exactly the observed image-agnostic M-ICL.

**Sources:** [An Explanation of In-context Learning as Implicit Bayesian Inference](https://arxiv.org/abs/2111.02080) (2021-11-03) · [What Makes Multimodal In-Context Learning Work? (CVPRW 2024)](https://arxiv.org/abs/2404.15736) (2024-04-24) · verified: True

*Origin-domain evidence:* ICL emerges from pretraining-distribution inference over latent concepts; demos serve to infer the shared latent task (2111.02080, proven in a synthetic HMM setting).
*Speech-domain evidence:* consistent: ALICE format-vs-accuracy split (arXiv:2603.20433, archived) and induction-head-driven speech ICL (arXiv:2604.06356, archived)

### X3-10 — [new] origin: **llm** · transfer: native · fence: training-free · ladder: b2 · anchor: PR-X3-3

Demonstration selection transfers NATIVELY to speech and moves genuine accuracy: kNN retrieval-based demo selection (KATE, text-origin) applied to frozen Whisper (SICL, explicitly 'without gradient descent') cuts isolated-word Chinese-dialect WER by 32.3% relative on average, rising to 36.4% with kNN example selection; TICL extends this to modern multimodal LLMs via text-embedding kNN over ASR pseudo-labels (up to 84.7% relative WER reduction on accented/multilingual/children's speech). This is the strongest published (b2)-type context-selection evidence on frozen speech models and directly qualifies ALICE's format-only null: WER movement is label/content-sensitive. Speech transfer column: ASR is proven; SLU/SQA via kNN demo pools are direct candidates. VLM failure column: RICES demo retrieval reduces to majority voting over context labels (Baldassini) — retrieval helps only insofar as demo labels carry the answer distribution, a confound the speech results must be screened for (acoustic-mimicry/lexical-overlap effects, archived induction-heads finding).

**Sources:** [Can Whisper perform speech-based in-context learning? (SICL)](https://arxiv.org/abs/2309.07081) (2023-09-13) · [TICL: Text-Embedding KNN For Speech In-Context Learning Unlocks Speech Recognition Abilities of Large Multimodal Models](https://arxiv.org/abs/2509.13395) (2025-09-16) · [What Makes Good In-Context Examples for GPT-3? (KATE)](https://arxiv.org/abs/2101.06804) (2021-01-17) · verified: True

*Origin-domain evidence:* kNN semantic retrieval of demos substantially beats random selection for GPT-3 across NLU/generation (2101.06804).
*Speech-domain evidence:* SICL: 32.3% avg relative WER reduction (36.4% with kNN selection) on frozen Whisper, no gradient descent (2309.07081); TICL: text-embedding kNN demo retrieval, up to 84.7% relative WER reduction without fine-tuning (2509.13395)

### X3-11 — [update] origin: **llm** · transfer: untransferred · fence: training-free · ladder: b2 · anchor: PR-X3-4

Prompt optimization is the only literature that QUANTIFIES prompt-space headroom (the yardstick's H_prompt-H_fix): APE reaches human-level instructions; OPRO-discovered prompts beat human prompts by up to 8% (GSM8K) and up to 50% (BBH); GEPA reflective prompt evolution outperforms GRPO weight-tuning by 6% average (up to 20%) with up to 35x fewer rollouts, and beats MIPROv2 by >10% (ICLR 2026 Oral; the 6%-average figure is the current v2 abstract). Speech transfer column: verified-empty — no APE/OPRO/GEPA-class instruction search on audio/omni-speech LLMs exists; transfer candidates are instruction search for SLU intent accuracy and SQA exact-match under W1's verifiable rewards, giving a direct H_prompt lower bound. VLM failure column: prompt optimizers act only through the text channel, so optimized-prompt gains cap at the text-driven fraction of a multimodal task — image(audio)-side conditioning stays untouched.

**Sources:** [Large Language Models Are Human-Level Prompt Engineers (APE, ICLR 2023)](https://arxiv.org/abs/2211.01910) (2022-11-03) · [Large Language Models as Optimizers (OPRO)](https://arxiv.org/abs/2309.03409) (2023-09-07) · [GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning (ICLR 2026 Oral)](https://arxiv.org/abs/2507.19457) (2025-07-25) · verified: True

*Origin-domain evidence:* OPRO: up to +8% GSM8K / +50% BBH over human prompts (2309.03409); GEPA: +6% avg (up to +20%) over GRPO with up to 35x fewer rollouts, +10% over MIPROv2 incl. +12% on AIME-2025 (2507.19457, v2 abstract; ICLR 2026 Oral confirmed).
*Speech-domain evidence:* none found (verified-empty search 2026-07-04; only text-domain applications, e.g., DD-GEPA on text dialogue disentanglement)

### X3-12 — [new] origin: **llm** · transfer: untransferred · fence: training-free · ladder: b1 · anchor: PR-X3-4

Prompt-format sensitivity: semantically-EQUIVALENT prompt formats spread accuracy by up to 76 points (LLaMA-2-13B few-shot), and the spread persists under model scaling, more demos, and instruction tuning (FormatSpread) — first-order evidence that prompt-space variance is huge, but b1/b2-unsplit (format artifacts vs genuine accuracy movement are not separated). Speech transfer column: no FormatSpread-style spread measurement exists for audio-LLMs; running K-format spread on a frozen omni for ASR/SLU is the cheapest instantiation of an H_prompt-H_fix lower bound and a pre-registrable Stage-2 target. VLM failure column: format sensitivity replicates in multimodal models, and perception-task metrics move less than reasoning-task metrics under prompt/TTC variation — variance concentrates where text carries the task.

**Sources:** [Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design (FormatSpread, ICLR 2024)](https://arxiv.org/abs/2310.11324) (2023-10-17) · [Limits and Gains of Test-Time Scaling in Vision-Language Reasoning](https://arxiv.org/abs/2512.11109) (2025-12-11) · verified: True

*Origin-domain evidence:* Up to 76 accuracy-point spread across plausible equivalent formats; recommendation to report performance spread over formats (2310.11324).
*Speech-domain evidence:* none found for spread-style measurement; nearest: Dynamic-SUPERB seen/unseen instruction drops (arXiv:2309.09510, archived)

### X3-13 — [new] origin: **vlm** · transfer: partial · fence: training-free · ladder: b1 · anchor: PR-X3-3

VLM ICL failure reference: multimodal ICL in IDEFICS/OpenFlamingo relies dominantly on TEXT-driven mechanisms with little-to-no influence from images in the demonstrations, and advanced demo-retrieval (RICES) performs no better than majority voting over context labels — the canonical cross-modal evidence that ICL's activation lever does not reach the perceptual channel. Speech transfer column: already replicated in audio by ALICE (demos fix format, degrade accuracy — archived), so transfer status of the FAILURE is partial-confirmed; the actionable lesson for ASR/SLU/SQA is that any demo-driven lift must pass label-sensitivity and acoustic-grounding controls before being credited as b2. VLM failure column: this IS the failure mode — visual grounding breaks the text-native ICL recipe.

**Sources:** [What Makes Multimodal In-Context Learning Work? (CVPRW 2024)](https://arxiv.org/abs/2404.15736) (2024-04-24) · verified: True

*Origin-domain evidence:* M-ICL analysis across IDEFICS/OpenFlamingo on a wide task range: 'M-ICL primarily relies on text-driven mechanisms, showing little to no influence from the image modality'; RICES not better than majority voting over context examples (2404.15736).
*Speech-domain evidence:* ALICE: six LALMs, demos improve format compliance but degrade core accuracy (arXiv:2603.20433, archived)

### X3-14 — [new] origin: **vlm** · transfer: untransferred · fence: training-free · ladder: b2 · anchor: PR-X3-3

Modality-native prompting existence proof: Set-of-Mark overlays SAM/SEEM segmentation marks directly on the INPUT image and unlocks zero-shot GPT-4V grounding that beats the fully-finetuned RefCOCOg state of the art — a training-free, input-space (not text-space) intervention that fixed a reachability failure text prompts could not. Speech transfer column: the audio cell is EMPTY — no training-free acoustic-native input intervention (segment/boundary marks, per-region tags, timestamp scaffolds inserted into the waveform or its presentation) for frozen audio-LLMs was found; candidates: diarization/VAD-derived segment marking for long-audio SQA and agentic 'which-speaker/which-segment' grounding. VLM failure-inverse column: SoM works because mature off-the-shelf segmenters exist; audio's weaker universal segmenters (VAD/diarization) bound how far the analog can go.

**Sources:** [Set-of-Mark Prompting Unleashes Extraordinary Visual Grounding in GPT-4V](https://arxiv.org/abs/2310.11441) (2023-10-17) · [Acoustic Prompt Tuning: Empowering Large Language Models with Audition Capabilities](https://arxiv.org/abs/2312.00249) (2023-11-30) · verified: True

*Origin-domain evidence:* Zero-shot SoM-prompted GPT-4V outperforms fully-finetuned referring-expression SOTA on RefCOCOg (2310.11441).
*Speech-domain evidence:* none found training-free; nearest neighbor is gradient-trained soft prompting via an instruction-aware audio aligner on a frozen LLM (Acoustic Prompt Tuning, 2312.00249)

### X3-15 — [new] origin: **llm** · transfer: partial · fence: training-free · ladder: b2 · anchor: PR-X3-5

CoT/test-time-compute task-boundary: quantitative meta-analysis (100+ papers; own evals on 20 datasets x 14 models) shows CoT helps mainly math/symbolic reasoning — on MMLU, direct answering matches CoT unless the item contains an '='. VLM failure column: TTS on VLMs improves multi-step reasoning but gives only limited gains on perception-focused benchmarks, and iterative self-refinement often DEGRADES open-source VLMs while external verification is the most reliable option (Limits-and-Gains). Speech transfer column: replicated — CoT on LALMs helps easy/medium tasks and HURTS hard ones where reasoning chains confuse the model (Audio-CoT); mapping: expect CoT/TTC lift on SQA and agentic speech tasks, expect null-to-negative on perception-shaped ASR/SER — matching the house observation that BoN headroom on ASR lives in sampling diversity, not reasoning length.

**Sources:** [To CoT or not to CoT? Chain-of-thought helps mainly on math and symbolic reasoning](https://arxiv.org/abs/2409.12183) (2024-09-18) · [Limits and Gains of Test-Time Scaling in Vision-Language Reasoning](https://arxiv.org/abs/2512.11109) (2025-12-11) · [Audio-CoT: Exploring Chain-of-Thought Reasoning in Large Audio Language Model](https://arxiv.org/abs/2501.07246) (2025-01-13) · verified: True

*Origin-domain evidence:* Meta-analysis: CoT gains concentrate on math/logic, near-zero elsewhere (2409.12183).
*Speech-domain evidence:* Audio-CoT: CoT significantly improves easy/medium LALM tasks, degrades hard ones where reasoning chains confuse the model; positive reasoning-length/accuracy correlation (2501.07246)

### X3-16 — [new] origin: **vlm** · transfer: untransferred · fence: training-free · ladder: c · anchor: PR-X3-2

VLM self-correction/critique failure reference: VISCO (1,645 QA pairs, 5,604 step-wise annotations, 24 LVLMs) shows human-written critiques substantially improve post-correction performance while MODEL-generated critiques are less helpful and sometimes detrimental — critique is the bottleneck; complementary ACL-Findings work shows VLMs struggle to self-correct during iterative inference without additional fine-tuning and external feedback, and Woodpecker rescues correction only via external expert models. Speech transfer column: no VISCO-analog audio critique/correction benchmark exists (verified-empty) — before any speech self-refine pipeline, build the b1/b2-controlled audio critique probe with external acoustic verifiers playing the human-critique surrogate role. VLM failure column: this IS the nearest cross-modal failure lesson — perceptual grounding breaks intrinsic critique first.

**Sources:** [VISCO: Benchmarking Fine-Grained Critique and Correction Towards Self-Improvement in Visual Reasoning (CVPR 2025)](https://arxiv.org/abs/2412.02172) (2024-12-03) · [Self-Correction is More than Refinement: A Learning Framework for Visual and Language Reasoning Tasks (ACL 2025 Findings)](https://arxiv.org/abs/2410.04055) (2024-10-05) · [Woodpecker: Hallucination Correction for Multimodal Large Language Models](https://arxiv.org/abs/2310.16045) (2023-10-24) · verified: True

*Origin-domain evidence:* 24-LVLM evaluation over 1,645 QA pairs / 5,604 step annotations: human critiques help, self-critiques sometimes detrimental; critique identified as the crucial bottleneck; LookBack (image-revisiting) recovers up to +13.5% (2412.02172).
*Speech-domain evidence:* none found — no audio critique/correction benchmark; nearest pathology evidence is ASR-corrector hallucination (arXiv:2505.24347)

### X3-17 — [update] origin: **llm** · transfer: partial · fence: training-free · ladder: c · anchor: PR-X3-6

The first systematic audio test-time-compute study transfers five LLM-origin TTC methods (CoT, temperature majority vote, weighted beam search, GPT-4o-verifier top-1, verifier-weighted) to five FROZEN audio LLMs (Qwen2-Audio, Audio-Flamingo-2, Gemini-2.0-Flash, Gemini-1.5-Pro, GPT-4o) on three auditory-cognition tasks: 9-150% relative gains, largest on the hardest task (overlapping dual-speaker digit recall with calculations) and for weaker models (Audio-Flamingo-2 +150.2%/+133.2% rel via LLM verifier; Qwen2-Audio +63.8-66.8% rel via beam search). Significance for the ladder: an external POSITIVE for (c)-type label-free realization on frozen audio models via a strong frozen judge — but on synthetic cognition tasks, NOT standard ASR/SLU/SQA benchmarks, not omni models, and with the best method model-dependent; the transfer to deployment speech-semantic tasks remains open (house ASR nulls are the counter-datum).

**Sources:** [Scaling Auditory Cognition via Test-Time Compute in Audio Language Models](https://arxiv.org/abs/2503.23395) (2025-03-30) · [Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters](https://arxiv.org/abs/2408.03314) (2024-08-06) · verified: True

*Origin-domain evidence:* TTC method suite (BoN, majority voting, verifier selection) established in text (2408.03314 and the SC/BoN lineage, archived).
*Speech-domain evidence:* 9-150% relative gains across five frozen audio LLMs on three auditory-cognition tasks (event recognition; noisy speech comprehension; overlapping dual-speaker digit recall); GPT-4o-verifier and consensus selection both effective; gains grow with task difficulty; model-level numbers verified against the paper HTML 2026-07-04 (2503.23395)


## Training-free vs fine-tuned SOTA positioning

## Positioning: training-free test-time methods vs gradient-trained SOTA (X3 LLM/VLM lane)

**Where training-free wins or ties the fine-tuned alternative (origin domains):**
- **GEPA** (ICLR 2026 Oral, arXiv:2507.19457): reflective prompt evolution beats **GRPO weight-tuning by 6% avg (up to 20%) with up to 35x fewer rollouts** (current v2 abstract) — the sharpest published training-free-vs-RL head-to-head, and the cross-domain anchor for the (b)-condition since prompt-space headroom is quantified nowhere else.
- **TPO** (archived, arXiv:2501.12895): an unaligned Llama-3.1-70B-SFT surpasses its RLHF-aligned Instruct counterpart after a few test-time preference-optimization steps.
- **Set-of-Mark** (arXiv:2310.11441): zero-shot marked-input GPT-4V beats the fully-FINETUNED RefCOCOg SOTA — a modality-native input intervention outperforming gradient training.
- **Speech-native**: SICL on frozen Whisper cuts dialect WER 32.3-36.4% relative *without gradient descent* (arXiv:2309.07081), where the gradient route to the same capability is FSA-GRPO weight updates (archived).

**Where trained components still dominate:**
- Realized best-of-N gains in text-math ride on **trained verifiers** (ORM arXiv:2110.14168; PRM ~78% MATH-subset reranking, arXiv:2305.20050); training-free self-verification measurably fails (Huang arXiv:2310.01798; Stechly arXiv:2402.08115; VISCO arXiv:2412.02172 in VLM).
- Reasoning-length control (s1 budget forcing, arXiv:2501.19393) presupposes reasoning-SFT'd models; audio reasoning models (Audio-Reasoner, Step-Audio-R1) are all gradient-trained.
- VLM critique/correction needs trained critics or external expert tools (Woodpecker); intrinsic refinement degrades open-source VLMs (arXiv:2512.11109).

**Regime rule the map supports:** training-free matches or beats fine-tuning when (i) an external verifiable signal or a modality-native grounding intervention exists, AND (ii) the task is reasoning-shaped; it lags when intrinsic self-assessment is the bottleneck or the task is perception-shaped (CoT/TTS limited on perception in both VLM, arXiv:2512.11109, and audio, arXiv:2501.07246). Speech-semantic tasks split accordingly: **SQA/agentic sit in the favorable regime** (verifiable rewards, reasoning-shaped — where (c) may be easiest, matching yardstick §6); **ASR/SER sit in the unfavorable regime**, consistent with the house MBR/selector nulls (stage-1 directional) and with audio-TTC gains appearing on cognition-style rather than transcription tasks (arXiv:2503.23395).

**Fence bookkeeping:** training-free = SC/USC, MBR, RAIN, TPO, SoM, SICL/TICL, APE/OPRO/GEPA, FormatSpread probes; trained-head-on-frozen = ARGS, DeAL, Controlled Decoding, ORM/PRM-guided BoN; gradient-trained (positioning only) = s1, FSA-GRPO, Audio-Reasoner, Step-Audio-R1, Acoustic Prompt Tuning.

## Negative findings (verified-empty searches & P0 strikes — first-class results)

- No APE/OPRO/GEPA-class automatic instruction/prompt optimization applied to audio or omni-speech LLMs found (searched 2026-07-04: 'automatic prompt optimization OPRO APE audio language models speech LLM instruction optimization' — hits are text-domain only, incl. DD-GEPA which is text dialogue disentanglement). The yardstick §4 statement that text prompt-optimization is the only quantified prompt-space literature stands confirmed.
- No inference-time alignment work (ARGS/RAIN/DeAL-class reward-guided, value-guided, or rewind decoding) on frozen speech/audio LLMs found (searched 2026-07-04: 'inference-time alignment reward-guided decoding frozen speech LLM audio language model' — zero speech-domain hits; token/segment-level reward-guided decoding on omni models is an unoccupied cell).
- No training-free audio-native analog of Set-of-Mark input-overlay prompting found (searched 2026-07-04: visual-prompting audio-analog / acoustic markers queries); nearest neighbors are gradient-trained soft prompts (Acoustic Prompt Tuning, arXiv:2312.00249, verified: instruction-aware audio aligner trained to produce soft prompts for a frozen LLM) — the modality-native input-intervention cell for audio is empty.
- No FormatSpread-style quantification of prompt-format performance spread for audio-LLMs found; audio instruction sensitivity exists only as seen/unseen task drops (Dynamic-SUPERB, archived), never as a spread-over-equivalent-formats measurement.
- No VISCO-analog critique/correction benchmark for audio LLMs found (searched 2026-07-04: audio LLM self-correction/self-refinement queries); audio self-correction evidence exists only as ASR-corrector hallucination pathology plus verification-stage fixes (arXiv:2505.24347) — the audio critique-bottleneck measurement does not exist.
- No process-reward model or step/candidate-level trained verifier for audio-LLM output selection surfaced in the searches run; WavReward (arXiv:2505.09558) is an outcome-level spoken-dialogue evaluator — the PRM-for-speech cell appears empty (bounded claim: from this lane's searches, not an exhaustive sweep).
- Verifier corrections this pass (2026-07-04): GEPA's GRPO margin fixed from ~10% to 6% avg per the current arXiv v2 abstract; the 2604.11025 'grounding paradox' clause rewritten to the source's actual definition (decide-where-to-look-before-evidence circular dependency); 'defensive justification' claims softened to abstract-supported wording (2410.04055); four delta flips new->update where sources were already archived (2408.03314 in CV1-13, Reflexion in agent lanes, GEPA in agent-skills, 2503.23395 in D3-12).