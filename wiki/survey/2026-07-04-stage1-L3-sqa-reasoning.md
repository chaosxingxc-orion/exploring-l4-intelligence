# Stage-1 lane L3 — Spoken-QA + audio reasoning

> Stage-1 problem-definition campaign lane · 2026-07-04 · workflow `wf_d7b939e9-c37` · methodology:
> CLAUDE.md three-stage section (Stage 1: survey-grounded argumentation; in-house numbers
> directional-only). Yardstick: [[2026-07-04-sufficiency-yardstick-memo]]. Every claim carries
> origin-domain (llm/vlm/speech), transfer-status, fence, ladder-condition and problem-anchor
> tags; every URL adversarially verified; P0 gate enforced (anchor-less claims struck).

## Open problems (P0-compliant: task-level, metric-named, literature-anchored)

### SQA-P1 — ladder: mixed

Speech-input reasoning gap: on reasoning content held identical, frozen speech interfaces lose massive accuracy versus text — GPT-4o scores 92% on the text version of Big Bench Audio but 66% in native speech-to-speech (26pp drop), while a training-free ASR->LLM pipeline shows minimal degradation. The deficit is at the audio interface, not in the reasoning backbone, and closing it natively has so far required gradient-trained audio reasoning models.

**Metric:** Accuracy on Big Bench Audio (1,000 Big-Bench-Hard-derived audio questions); the audio-vs-text gap in percentage points

**Named by:** [Evaluating Audio Reasoning with Big Bench Audio (Artificial Analysis / Hugging Face blog)](https://huggingface.co/blog/big-bench-audio-release) (2024-12-20) · [Speech Reasoning Benchmarking Methodology — Artificial Analysis](https://artificialanalysis.ai/methodology/speech-to-speech-benchmarking) (2025)

### SQA-P2 — ladder: b2

Text-shortcut contamination (answers-without-listening) in audio reasoning benchmarks: Omni-R1 showed much of its GRPO gain on MMAU is attributable to better text-only reasoning — fine-tuning WITHOUT audio improves audio-benchmark scores — and MMAU-Pro was explicitly constructed because text-only models score non-trivially on prior audio benchmarks (its shortcut controls drop text-only models to 16-30%). Any claimed audio-reasoning lift is uninterpretable without audio-blind controls; this is the audio instance of the VLM MMStar problem.

**Metric:** Audio-blind (text-only/caption-only) accuracy vs full-input accuracy on MMAU/MMAR/MMAU-Pro; multi-modal gain and leakage metrics

**Named by:** [Omni-R1: Do You Really Need Audio to Fine-Tune Your Audio LLM?](https://arxiv.org/abs/2505.09439) (2025-05-14) · [MMAU-Pro: A Challenging and Comprehensive Benchmark for Holistic Evaluation of Audio General Intelligence](https://arxiv.org/abs/2508.13992) (2025-08-19)

### SQA-P3 — ladder: b2

Multi-hop reasoning fails over correctly perceived audio: SAKURA (Interspeech 2025 oral) shows LALMs answer single-hop attribute questions (gender, language, emotion, animal sound) but fail multi-hop questions built on the SAME attribute even when extraction was correct — reasoning remains text-driven and latent speech/audio representations are not integrated into the chain. MMAR extends this: every item demands multi-step reasoning and models are weakest at the Signal layer despite it having the highest random-guess baseline.

**Metric:** Multi-hop vs single-hop accuracy gap on SAKURA (500 MCQs per sub-track, 4 tracks, 4,000 questions total); layer-stratified accuracy on MMAR (1,000 items)

**Named by:** [SAKURA: On the Multi-hop Reasoning of Large Audio-Language Models Based on Speech and Audio Information](https://arxiv.org/abs/2505.13237) (2025-05-19) · [MMAR: A Challenging Benchmark for Deep Reasoning in Speech, Audio, Music, and Their Mix (NeurIPS 2025)](https://arxiv.org/abs/2505.13032) (2025-05-19)

### SQA-P4 — ladder: b2

CoT inverted scaling / textual surrogate reasoning: chain-of-thought prompting on audio LLMs helps easy/medium tasks but degrades hard ones (Audio-CoT), R1-AQA reports explicit reasoning gives no significant AQA benefit ('how to efficiently utilize deep thinking remains an open question'), and Step-Audio-R1 names the root cause — audio models initialized on text CoT produce 'textual surrogate reasoning' grounded in transcripts/captions rather than acoustics, so performance degrades as chains lengthen. The VLM analog (MME-CoT: CoT harms perception-heavy tasks) confirms this is a cross-modal pattern.

**Metric:** Accuracy delta with vs without CoT prompting on MMAU/MMAR, stratified by difficulty; accuracy as a function of reasoning-chain length

**Named by:** [Audio-CoT: Exploring Chain-of-Thought Reasoning in Large Audio Language Model](https://arxiv.org/abs/2501.07246) (2025-01-13) · [Reinforcement Learning Outperforms SFT: A Case Study on Audio Question Answering (R1-AQA)](https://arxiv.org/abs/2503.11197) (2025-03-14) · [Step-Audio-R1 Technical Report](https://arxiv.org/abs/2511.15848) (2025-11-19)

### SQA-P5 — ladder: mixed

Spoken-QA robustness collapse under speaker/environment/content variation: VoiceBench shows novel accents, environmental noise, and mispronunciations sharply degrade LLM voice assistants, with end-to-end models less resilient than ASR+LLM pipelines (pipelines lead by >20 points on speech instructions); HeySQuAD quantifies a 12.51% improvement in answering human-spoken questions when training includes transcribed human-spoken questions — a margin lost absent spoken-question training; MELD-Hard1k shows >50% relative accuracy collapse under acoustic perturbation. This is the modern successor of the Spoken-SQuAD ASR-error-cascade problem, now at the end-to-end audio-LLM level.

**Metric:** Accuracy/F1 drop from clean to perturbed speech (VoiceBench robustness suites, HeySQuAD human-spoken split, MELD-Hard1k)

**Named by:** [VoiceBench: Benchmarking LLM-Based Voice Assistants](https://arxiv.org/abs/2410.17196) (2024-10-22) · [HeySQuAD: A Spoken Question Answering Dataset](https://arxiv.org/abs/2304.13689) (2023-04-26)

### SQA-P6 — ladder: a

Fine-grained acoustic-linguistic perception bottleneck: on MMSU (5,000 triplets, 47 tasks; ICLR 2026) the best of 14 SpeechLLMs (Gemini-1.5-Pro) reaches 60.68% vs best-human 89.72%, with phonology at 53.60% — and models show the INVERTED profile vs humans (humans find perception easier than reasoning, 91.24% vs 86.77%; models fail perception harder than semantic reasoning). Near-homophone, consonant/vowel, and syllable perception are the weakest cells, questioning whether the perceptual mass exists in frozen models at all.

**Metric:** MMSU accuracy overall and per dimension (phonetics/prosody/rhetoric/syntactics/semantics/paralinguistics), model vs human

**Named by:** [MMSU: A Massive Multi-task Spoken Language Understanding and Reasoning Benchmark](https://arxiv.org/abs/2506.04779) (2025-06-05)


## Approach genealogy & evidence claims (cross-domain mandatory)

### L3-C01 — [new] origin: **llm** · transfer: partial · fence: training-free · ladder: b2 · anchor: SQA-P4

Chain-of-thought prompting — eliciting intermediate reasoning steps at inference — is the origin-domain (text-LLM) mechanism for reasoning activation without weight changes, producing large gains on arithmetic/symbolic/commonsense benchmarks in sufficiently large models (few-shot CoT, Wei et al. 2022).

**Sources:** [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903) (2022-01-28) · verified: True

*Origin-domain evidence:* Wei et al. 2022 abstract (verified): 540B model with eight CoT exemplars achieves SOTA on GSM8K, surpassing finetuned GPT-3 with a verifier; abilities 'emerge naturally in sufficiently large language models'; pure prompting, no weight updates.
*Speech-domain evidence:* Audio-CoT (arXiv 2501.07246, Tables 1-2 verified) transfers ZS-CoT to Qwen2-Audio-7B-Instruct: MMAU test-mini 55.60% -> 57.80%; gains confined to easy/medium items, degradation on hard items.

### L3-C02 — [update] origin: **llm** · transfer: partial · fence: training-free · ladder: c · anchor: SQA-P4

Self-consistency (sample diverse reasoning paths, majority-vote the answer) is the canonical text-LLM label-free selector over rollouts; its audio transfer exists but is thin — Audio-CoT's SC@5 on Qwen2-Audio adds only +0.30pp over ZS-CoT on MMAU (57.80 -> 58.10), a small realized fraction relative to text-domain gains.

**Sources:** [Self-Consistency Improves Chain of Thought Reasoning in Language Models](https://arxiv.org/abs/2203.11171) (2022-03-21) · [Audio-CoT: Exploring Chain-of-Thought Reasoning in Large Audio Language Model](https://arxiv.org/abs/2501.07246) (2025-01-13) · verified: True

*Origin-domain evidence:* Wang et al. 2022 abstract (verified): samples diverse reasoning paths, selects most consistent answer by marginalization; GSM8K +17.9% absolute; decoding strategy, no training.
*Speech-domain evidence:* Audio-CoT Table 2 (verified in arXiv HTML v1): SC with 5 samples on Qwen2-Audio-7B-Instruct, MMAU test-mini — baseline 55.60, ZS-CoT 57.80, ZS-CoT+SC 58.10; Manual-CoT+SC 57.50.

### L3-C03 — [new] origin: **llm** · transfer: partial · fence: training-free · ladder: b2 · anchor: SQA-P4

Audio-CoT is the first systematic transfer of CoT prompting to a frozen audio LLM: on Qwen2-Audio-7B-Instruct/MMAU, all CoT variants beat baseline (best ZS-CoT 57.80 vs 55.60), but on hard questions reasoning chains fail to improve and even degrade accuracy; the paper also reports a positive reasoning-length/accuracy correlation on tractable items.

**Sources:** [Audio-CoT: Exploring Chain-of-Thought Reasoning in Large Audio Language Model](https://arxiv.org/abs/2501.07246) (2025-01-13) · verified: True

*Origin-domain evidence:* Method genealogy is text-LLM zero-shot/manual/desp-CoT prompting (Kojima/Wei class), applied unchanged; abstract (verified): 'the first exploration into integrating Chain-of-Thought (CoT) reasoning into LALMs'.
*Speech-domain evidence:* Native speech-domain measurement (verified): MMAU test-mini (1,000 items), Qwen2-Audio-7B-Instruct, training-free prompting only; 'CoT methods significantly improve performance on easy and medium tasks but encounter challenges with hard tasks, where reasoning chains can confuse the model'; positive correlation between reasoning path length and accuracy.

### L3-C04 — [new] origin: **llm** · transfer: partial · fence: training-free · ladder: c · anchor: SQA-P5

Five training-free test-time-compute methods — CoT prompting, temperature-based majority voting, weighted beam search, and two frozen-LLM-verifier best-of-N selectors — lift five audio LLMs (Qwen2-Audio, Audio-Flamingo-2, Gemini-1.5-Pro, Gemini-2.0-Flash, GPT-4o) on escalating auditory-cognition tasks (noisy comprehension, overlapping-speech recall) by 9-150% relative; the strongest gains come from external-verifier selection on the weakest models.

**Sources:** [Scaling Auditory Cognition via Test-Time Compute in Audio Language Models](https://arxiv.org/abs/2503.23395) (2025-03-30) · verified: True

*Origin-domain evidence:* All five methods are text-LLM test-time-compute mechanisms (verified in HTML: CoT, temperature-based majority voting, BS-W weighted beam search, LLM-Top1 and LLM-W verifier selection).
*Speech-domain evidence:* Native audio measurement (verified in HTML), but on a small self-collected dataset (10 participants: 6M/4F aged 20-55; 3 escalating task tiers) — NOT on MMAU/MMSU/BBA-class standard benchmarks; Qwen2-Audio beam search +63.8%/+66.8% rel on Tasks 2/3, Audio-Flamingo-2 verifier +150.2%/+133.2% rel; overall TTC gains 9-150%.

### L3-C05 — [new] origin: **vlm** · transfer: partial · fence: training-free · ladder: b2 · anchor: SQA-P4

MME-CoT (ICML 2025, PMLR 267) — the closest VLM transfer reference for audio-context CoT — finds CoT prompting often DEGRADES large multimodal model performance on perception-heavy tasks ('harmful overthinking'), while reflection-capable models gain CoT quality at heavy efficiency cost; 1,130 questions across six domains with key-step annotations scoring quality/robustness/efficiency.

**Sources:** [MME-CoT: Benchmarking Chain-of-Thought in Large Multimodal Models for Reasoning Quality, Robustness, and Efficiency](https://arxiv.org/abs/2502.09621) (2025-02-13) · verified: True

*Origin-domain evidence:* First systematic CoT-impact study in LMMs (abstract verified): 'CoT prompting often degrades LMM performance on perception-heavy tasks, suggesting a potentially harmful overthinking behavior'; Kimi k1.5 > GPT-4o on CoT quality; reflection models 'exhibit significant inefficiency'. Venue verified: PMLR 267:27793-27830 (ICML 2025). 1,130 questions verified via HF dataset viewer (1.13k rows); the paper's key-step-annotation total was not independently verifiable and is omitted.
*Speech-domain evidence:* The same signature replicates in audio: Audio-CoT hard-task degradation (2501.07246) and Step-Audio-R1's 'inverted scaling' diagnosis (2511.15848) — but no audio benchmark yet scores CoT quality/robustness step-wise like MME-CoT.

### L3-C06 — [new] origin: **vlm** · transfer: partial · fence: training-free · ladder: background · anchor: SQA-P2

MMStar (NeurIPS 2024) named and metricized the modality-shortcut problem in VLM evaluation: many benchmark answers are derivable without images (GeminiPro 42.7% on MMMU with no visual input) and leakage lets LVLMs beat their own LLM backbone image-free (Sphinx-X-MoE 43.6% on MMMU without images, +17.9pp over its backbone), motivating per-sample vision-indispensability curation plus multi-modal-gain/leakage metrics — the direct template for audio-blind controls in spoken-QA.

**Sources:** [Are We on the Right Way for Evaluating Large Vision-Language Models? (MMStar)](https://arxiv.org/abs/2403.20330) (2024-03-29) · verified: True

*Origin-domain evidence:* 1,500 human-curated vision-indispensable samples; two metrics for leakage and actual multi-modal gain (verified). 42.7% figure verified against the NeurIPS 2024 camera-ready abstract (proceedings.neurips.cc); note the arXiv v2 abstract states 42.9% for the same datum. NeurIPS 2024 acceptance verified (GitHub + proceedings).
*Speech-domain evidence:* Audio adoption is partial: MMAU-Pro (2508.13992) applies coarse text-only-shortcut controls (text-only models fall to 16-30%), but no audio benchmark yet publishes per-sample audio-indispensability curation with leakage metrics.

### L3-C07 — [new] origin: **speech** · transfer: native · fence: gradient-trained · ladder: background · anchor: SQA-P2

Omni-R1 (GRPO on Qwen2.5-Omni) reached then-SOTA on MMAU and MMAR, but its ablations show much of the gain comes from improved TEXT-side reasoning: fine-tuning on a text-only dataset (no audio) improved audio-benchmark performance — direct gradient-side evidence that MMAU-class scores move without acoustic grounding.

**Sources:** [Omni-R1: Do You Really Need Audio to Fine-Tune Your Audio LLM?](https://arxiv.org/abs/2505.09439) (2025-05-14) · verified: True

*Origin-domain evidence:* GRPO lineage is text-LLM RLVR (DeepSeek-R1 class); applied here to an omni model on AQA with with/without-audio test ablations.
*Speech-domain evidence:* Native (abstract verified): 'new State-of-the-Art performance on the recent MMAU and MMAR benchmarks'; 'much of the performance improvement from GRPO could be attributed to better text-based reasoning'; 'fine-tuning without audio on a text-only dataset was effective at improving the audio-based performance'.

### L3-C08 — [new] origin: **speech** · transfer: native · fence: gradient-trained · ladder: background · anchor: SQA-P4

R1-AQA (GRPO on Qwen2-Audio-7B-Instruct, only 38k samples) hit 64.5% on MMAU test-mini — the gradient-trained reference point on the same frozen backbone where training-free CoT+SC reaches 58.10% — while explicitly reporting that the explicit reasoning process showed NO significant benefit for AQA and that LALMs 'still lag far behind humans' in auditory-language reasoning.

**Sources:** [Reinforcement Learning Outperforms Supervised Fine-Tuning: A Case Study on Audio Question Answering (R1-AQA)](https://arxiv.org/abs/2503.11197) (2025-03-14) · verified: True

*Origin-domain evidence:* GRPO transferred from text-LLM RLVR; abstract quotes verified verbatim: 'The explicit reasoning process has not shown significant benefits for AQA tasks'; 'LALMs still lag far behind humans auditory-language reasoning'; 'how to efficiently utilize deep thinking remains an open question for further research'.
*Speech-domain evidence:* Native (verified): 64.5% MMAU test-mini SOTA at publication; RL significantly outperforms SFT with only 38k post-training samples.

### L3-C09 — [new] origin: **speech** · transfer: native · fence: gradient-trained · ladder: background · anchor: SQA-P4

Step-Audio-R1 names the CoT-for-audio failure mode — 'inverted scaling' caused by 'textual surrogate reasoning' (chains grounded in transcripts/captions, not acoustics) — and shows it is fixable with weight updates: Modality-Grounded Reasoning Distillation plus RL yields acoustically-grounded chains that surpass Gemini 2.5 Pro across speech/sound/music reasoning benchmarks. This fixes the fine-tuned ceiling for SQA-P4; no training-free counterpart of modality-grounded CoT exists.

**Sources:** [Step-Audio-R1 Technical Report](https://arxiv.org/abs/2511.15848) (2025-11-19) · verified: True

*Origin-domain evidence:* R1-style long-CoT RL from text LLMs, adapted with MGRD; pipeline verified in HTML: MGRD -> multimodal SFT -> on-policy PPO RL (0.8 accuracy + 0.2 format reward, 16 samples/prompt); frozen Qwen2 audio encoder + Qwen2.5-32B decoder.
*Speech-domain evidence:* Native (body verified): 'existing audio language models engage in textual surrogate reasoning rather than acoustic reasoning... models systematically reason from the perspective of transcripts or textual captions'; performance previously degraded as reasoning length increased; final model surpasses Gemini 2.5 Pro across speech, environmental sound, and music benchmarks.

### L3-C10 — [new] origin: **speech** · transfer: native · fence: training-free · ladder: background · anchor: SQA-P3

SAKURA measures frozen LALMs zero-shot and finds they fail multi-hop questions even when the single-hop attribute extraction succeeds: reasoning is predominantly text-driven and latent speech/audio representations are not incorporated into the reasoning chain — the sharpest published localization of WHERE audio-context reasoning breaks (integration, not perception).

**Sources:** [SAKURA: On the Multi-hop Reasoning of Large Audio-Language Models Based on Speech and Audio Information (Interspeech 2025)](https://arxiv.org/abs/2505.13237) (2025-05-19) · verified: True

*Origin-domain evidence:* Benchmark design genealogy is text-LLM multi-hop QA (HotpotQA class) and VLM attribute-then-reason probes, instantiated on speech/audio attributes; Interspeech 2025 (Oral) verified.
*Speech-domain evidence:* Native (structure verified in HTML): 4 tracks (gender, language, emotion, animal sound) x (single-hop, multi-hop) x 500 MCQs = 4,000 human-verified questions; abstract verified: 'LALMs struggle to integrate speech/audio representations for multi-hop reasoning, even when they extract the relevant information correctly'.

### L3-C11 — [new] origin: **vlm** · transfer: untransferred · fence: training-free · ladder: c · anchor: SQA-P4

LLaVA-CoT (v1, as LLaVA-o1) demonstrates VLM-side inference-time selection over structured reasoning: stage-level beam search (generate candidates per reasoning stage, self-select the best, continue) outperforms both best-of-N and sentence-level beam search at comparable compute, with accuracy improving monotonically in candidate count — a label-free, process-level selector family with no published speech instance.

**Sources:** [LLaVA-CoT: Let Vision Language Models Reason Step-by-Step](https://arxiv.org/abs/2411.10440) (2024-11-15) · verified: True

*Origin-domain evidence:* Verified in arXiv v1: abstract proposes 'an inference-time stage-level beam search method'; Table 5 (MMVet, comparable compute): best-of-N(10) 60.9, sentence-level beam(2) 58.4, stage-level beam(4) 62.9; Table 6: monotone 60.3 -> 61.7 -> 62.3 -> 62.9 as beams increase. Caveats: base model is SFT-trained on LLaVA-CoT-100k structured traces (selection mechanism itself is training-free but demonstrated on that trained base); later arXiv revisions replace/rename the test-time method as SWIRES (stage-wise retracing search). Secondary OpenReview source dropped by verifier — bot-walled and unverifiable this session.
*Speech-domain evidence:* none found — no stage-level / process-level selection over audio reasoning chains located (verified-empty this session)

### L3-C12 — [new] origin: **speech** · transfer: native · fence: training-free · ladder: background · anchor: SQA-P1

The Big Bench Audio release quantifies that a training-free system composition (Whisper ASR -> GPT-4o -> TTS) shows minimal reasoning degradation vs text (≈92%), while the same backbone natively speech-to-speech drops to 66% — locating the 26pp audio reasoning gap at the audio interface rather than in reasoning capacity, and establishing the pipeline as the training-free reference ceiling for spoken reasoning.

**Sources:** [Evaluating Audio Reasoning with Big Bench Audio (Hugging Face blog)](https://huggingface.co/blog/big-bench-audio-release) (2024-12-20) · [Speech to Speech Models and Providers Analysis — Artificial Analysis](https://artificialanalysis.ai/speech-to-speech) (2026) · verified: True

*Origin-domain evidence:* Benchmark derives from text-LLM Big Bench Hard (4 categories x 250 questions, 23 synthetic voices — all verified against the blog) — the text origin is what makes the audio-vs-text gap attributable.
*Speech-domain evidence:* Native (verified): GPT-4o text 92% vs speech-to-speech 66%; 'traditional pipeline approaches... show minimal performance degradation compared to pure text processing'. Current AA leaderboard (fetched 2026-07-04) shows the native gap since closed only via gradient-trained audio reasoning models: Gemini 2.5 Flash Native Audio Thinking 91%; Step-Audio R1.1 (Realtime) 98%, GPT-Realtime-2 97%, Qwen3.5 Omni Plus Realtime 99%. (Earlier-snapshot figures GPT-Realtime 82.8% / Gemini 92% no longer displayed — refreshed by verifier.)

### L3-C13 — [new] origin: **speech** · transfer: native · fence: training-free · ladder: background · anchor: SQA-P5

VoiceBench (TACL 2026) is the first multi-facet robustness evaluation of LLM voice assistants and names the deficiency profile: novel accents, environmental noise, and mispronunciations cause the strongest degradation; weak speech encoders make models highly vulnerable; and end-to-end voice assistants trail ASR+LLM pipeline systems in resilience to input variation.

**Sources:** [VoiceBench: Benchmarking LLM-Based Voice Assistants](https://arxiv.org/abs/2410.17196) (2024-10-22) · [VoiceBench (TACL publication, MIT Press)](https://direct.mit.edu/tacl/article/doi/10.1162/TACL.a.628/136245/VoiceBench-Benchmarking-LLM-Based-Voice-Assistants) (2026) · verified: True

*Origin-domain evidence:* Perturbation-suite methodology descends from text-LLM robustness evaluation (content noise, instruction variation) plus classic ASR noise robustness, unified over spoken instructions. TACL record verified via search (repo badge '[TACL'26]'; MIT Press URL is bot-blocked 403 to direct fetch but confirmed real). Year corrected 2025 -> 2026 by verifier.
*Speech-domain evidence:* Native (body verified in HTML): low-resource accents (Indian English, Philippines) cause 'notable performance degradation'; 'all voice assistants show strong resilience to grammatical errors but are much more vulnerable to mispronunciations'; 'Pipelines outperform E2E models' by 'a large margin exceeding 20 points' on speech instructions, in both overall performance and robustness; speech-encoder choice hypothesized critical for robustness.

### L3-C14 — [new] origin: **speech** · transfer: native · fence: training-free · ladder: background · anchor: SQA-P2

MMAU-Pro (AAAI 2026) fixes the audio-blind artifact by construction and re-measures the human-model gap under shortcut controls: humans 77.9% vs best model 59.2% (Gemini 2.5 Flash; Audio Flamingo 3 51.7%, approaching random performance in multiple categories), with text-only models dropping to 16-30% — simultaneously the cleanest current gap statement and the instrument template for b2 (acoustic-grounding) certification in spoken-QA.

**Sources:** [MMAU-Pro: A Challenging and Comprehensive Benchmark for Holistic Evaluation of Audio General Intelligence](https://arxiv.org/abs/2508.13992) (2025-08-19) · verified: True

*Origin-domain evidence:* Shortcut-control design imported from VLM eval hygiene (MMStar-class vision-indispensability); 5,305 expert QA instances, 49 skills, multi-audio/spatial/long-form axes (all verified). AAAI 2026 verified (ojs.aaai.org article 39430; presented January 2026, Singapore).
*Speech-domain evidence:* Native (body verified in HTML v1): human 77.9%; Gemini 2.5 Flash 59.2%, Audio Flamingo 3 51.7% with spatial 26.8% / multi-audio 26.0% vs random baseline 23.4%; text-only performance 'drops sharply to 16-30%'; motivation verified: prior benchmarks' 'questions can often be addressed through text reasoning and language priors'.

### L3-C15 — [new] origin: **speech** · transfer: native · fence: training-free · ladder: a · anchor: SQA-P6

MMSU (ICLR 2026) shows the spoken-QA bottleneck is perceptual SUPPORT, not only reasoning: best of 14 SpeechLLMs (Gemini-1.5-Pro) scores 60.68% vs best-human 89.72%; phonology perception is worst (top model 53.60%; near-homophone, consonant/vowel, syllable perception poorest), and models invert the human profile — relatively better at semantic reasoning than at fine-grained acoustic perception (humans: perception 91.24% > reasoning 86.77%).

**Sources:** [MMSU: A Massive Multi-task Spoken Language Understanding and Reasoning Benchmark](https://arxiv.org/abs/2506.04779) (2025-06-05) · [MMSU paper page (Hugging Face)](https://huggingface.co/papers/2506.04779) (2025-06-05) · verified: True

*Origin-domain evidence:* MMLU/MMMU-style massive-multitask MCQ format from text/VLM evaluation, instantiated over 47 spoken-language phenomena across phonetics, prosody, rhetoric, syntactics, semantics, paralinguistics; ICLR 2026 verified in arXiv comments.
*Speech-domain evidence:* Native (body verified in arXiv HTML v2): 5,000 audio-question-answer triplets; best human 89.72% avg vs Gemini-1.5-Pro 60.68%; phonology best-model 53.60%; human perception 91.24% vs reasoning 86.77% while models show the sharp inverse ('fundamental deficiency in fine-grained acoustic perception, which contrasts sharply with human performance'); 'near-homophone perception, consonant and vowel perception, and syllable perception generally show poor performance across the models'.

### L3-C16 — [new] origin: **vlm** · transfer: native · fence: training-free · ladder: b2 · anchor: SQA-P5

Thinking-with-Sound (TwS) is the strongest published training-free accuracy movement in this family: interleaving linguistic CoT with on-the-fly audio manipulation (denoising, source separation, spectral analysis via tool calls, no weight updates) recovers +24.73 to +36.61pp ABSOLUTE on MELD-Hard1k, where baseline frozen models lose >50% relative under acoustic perturbation (Qwen2.5-Omni-7B 47.65% -> 12.36%); the paper reports superlinear scaling of improvements with model size.

**Sources:** [Thinking with Sound: Audio Chain-of-Thought Enables Multimodal Reasoning in Large Audio-Language Models](https://arxiv.org/abs/2509.21749) (2025-09-26) · verified: True

*Origin-domain evidence:* The interleaved 'thinking with the modality' CoT paradigm originates in vision (thinking-with-images / tool-augmented visual CoT, o3-style), which TwS explicitly parallels for audio.
*Speech-domain evidence:* Native audio instantiation (body verified in HTML v1): Qwen2.5-Omni-3B +24.73pp (27.44 -> 52.17), Qwen2.5-Omni-7B +36.61pp (12.36 -> 48.97), Voxtral-24B +24.94pp (24.55 -> 49.49) on MELD-Hard1k; baseline 7B drop 47.65 -> 12.36 (73.9% relative); paper wording verified: 'superlinear scaling of improvements with model size'; tools: denoising/enhancement/normalization/analysis incl. source separation, voice extraction, spectral analysis, pitch tracking; denoising ablation largest (-15.80 when removed); training-free, tool-calling only.


## Training-free vs fine-tuned SOTA positioning

# Positioning — spoken-QA / audio reasoning: training-free vs fine-tuned SOTA

**Same-backbone anchor (cleanest comparison in the family).** On Qwen2-Audio-7B-Instruct at MMAU test-mini: baseline 55.60% -> best published training-free conditioning (ZS-CoT + self-consistency@5) 58.10% (+2.5pp, Audio-CoT arXiv:2501.07246) vs GRPO with 38k samples 64.5% (+~9pp, R1-AQA arXiv:2503.11197). Gradient RL currently captures roughly 3-4x more of the gap than the best training-free conditioning — and both remain far below humans (MMAU-Pro humans 77.9% vs best model 59.2%).

**But the fine-tuned SOTA is partially text-shortcut inflated.** Omni-R1 (arXiv:2505.09439) shows much of the GRPO gain on MMAU is text-side reasoning; text-only fine-tuning improves 'audio' scores. Under MMAU-Pro's shortcut controls the whole field compresses (best 59.2%, text-only 16-30%). So the training-free-vs-trained gap on shortcut-controlled audio reasoning is effectively unmeasured — a live positioning opening for the house.

**Where gradient training is currently unmatched:** modality-grounded CoT. Step-Audio-R1 (arXiv:2511.15848) fixes 'inverted scaling'/'textual surrogate reasoning' with distillation+RL (MGRD -> SFT -> PPO) and surpasses Gemini 2.5 Pro; no training-free counterpart of acoustically-grounded chains exists (verified-empty this session).

**Where training-free is strong:** (i) system composition — the ASR->LLM pipeline nearly erases the 26pp Big Bench Audio native reasoning gap (HF blog 2024-12-20), and pipeline systems are also more perturbation-robust than end-to-end models (VoiceBench: pipelines lead E2E by >20 points on speech instructions); native parity arrived only via gradient-trained audio reasoning models (per the Artificial Analysis leaderboard fetched 2026-07-04: Gemini 2.5 Flash Native Audio Thinking 91%; Step-Audio R1.1 98%, GPT-Realtime-2 97%). (ii) Tool-augmented audio CoT — TwS (arXiv:2509.21749) gains +24.7-36.6pp absolute on perturbed emotion QA with zero weight updates. (iii) Test-time compute — five TTC methods give 9-150% relative on auditory-cognition tasks (arXiv:2503.23395), though on a small non-standard self-collected dataset (10 participants).

**House yardstick mapping.** For this family the MCQ format makes H_fix (condition a) near-trivially measurable as calibrated non-degenerate mass — yet no oracle pass@k/best-of-N headroom numbers exist on MMAU/MMAR/MMSU/BBA (verified-empty). H_prompt - H_fix (the campaign's center of gravity) is doubly unmeasured: no APE/OPRO/GEPA-class instruction search has ever been run on an audio LLM (verified-empty). The only deployed label-free selector datum, SC@5 = +0.30pp over ZS-CoT, suggests ρ is small but nonzero here — better than the house ASR ρ≈0 prior, and cheap to measure properly. MMAU-Pro-style audio-blind controls are the ready-made b1/b2 splitter this family uniquely offers.

## Negative findings (verified-empty searches & P0 strikes — first-class results)

- No APE/OPRO/GEPA-class automatic prompt/instruction optimization has been applied to any frozen audio-LLM on spoken-QA or audio-reasoning benchmarks: two targeted searches (2026-07-04) returned only text-domain hits (OPRO, APE, APO, GAAPO, DD-GEPA on text dialogue); H_prompt−H_fix is unquantified for this family, consistent with the yardstick memo's cross-family zero.
- No oracle best-of-N / pass@k headroom (condition (a), H_fix) quantification found for frozen audio LLMs on the standard audio reasoning benchmarks (MMAU, MMAR, MMSU, Big Bench Audio, MMAU-Pro): the closest published numbers are deployable-selector results — Audio-CoT SC@5 (+0.30pp over ZS-CoT on MMAU) and the auditory-cognition TTC paper (arXiv:2503.23395), which uses a small self-collected 10-participant dataset, not a standard benchmark. Oracle-vs-selector decomposition is entirely absent in this family.
- No speech-domain instance of process-level / stage-level inference-time selection (LLaVA-CoT-style stage-level beam search, or step-wise verifier selection over reasoning chains) on audio reasoning tasks was found — the VLM selector family is untransferred to audio.
- No audio benchmark publishes per-sample modality-indispensability curation with explicit leakage metrics in the MMStar sense: MMAU-Pro (2025-08) applies benchmark-level text-only-shortcut controls (text-only models 16-30%) but no per-sample audio-indispensability certification or leakage/multi-modal-gain metric pair exists for spoken-QA.
- VERIFIER RECORD (2026-07-04): 0 P0 strikes — all 16 claims anchor to listed problems. All 23 unique source URLs resolved or were confirmed real; fidelity corrections applied: (1) L3-C05 — unverifiable '3,865 key-step annotations' removed (1,130 questions confirmed via HF dataset viewer; ICML 2025 / PMLR 267 confirmed); (2) L3-C11 — OpenReview source dropped (bot-walled, unverifiable); stage-level beam-search numbers confirmed against arXiv v1, with note that later revisions rename the method SWIRES; (3) L3-C13 — VoiceBench TACL year corrected 2025->2026 (repo badge TACL'26; MIT Press URL 403-blocked to direct fetch but confirmed real via search); (4) L3-C12 — stale Artificial Analysis leaderboard figures (GPT-Realtime 82.8% / Gemini 92%) replaced with currently displayed values (Gemini 2.5 Flash Native Audio Thinking 91%; native reasoning models 97-99%); (5) SQA-P5 — HeySQuAD 12.51% direction corrected to an improvement-from-training framing per the abstract; (6) SQA-P6/L3-C15 — MMSU dimension list corrected to include syntactics; inverted-profile numbers 91.24%/86.77% confirmed in arXiv HTML v2; (7) L3-C06 — 42.7% retained per NeurIPS 2024 camera-ready abstract (arXiv v2 abstract shows 42.9%).