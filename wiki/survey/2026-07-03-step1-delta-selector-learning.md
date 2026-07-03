# Step-1 delta scan D3 — inference-time selector learning & reference-free QE for ASR

> Step-1 rationality campaign lane · 2026-07-03 · workflow `wf_68e2556d-7a7` ·
> pre-registration: [[2026-07-03-agentic-tfrl-step1-preregistration]] @ freeze b19bff2. Ground rules: the 2026-07-02 verdict is the null hypothesis;
> claims tagged `delta_vs_archive` against the 17-file survey archive; every URL adversarially
> verified (0-hallucination bar). 

### D3-1 — [new] axis: b-estimate-R · bears on: M5

Self-certainty — a KL-divergence-based confidence computed from the frozen model's own token distributions — is a training-free, reward-model-free best-of-N selector that scales with N (akin to reward models, without their overhead) and generalizes to open-ended tasks; but the paper explicitly shows self-certainty and Borda-voting selection remain significantly below oracle selection at every N. This is a text-domain existence proof that a deployable label-free proxy for R can beat consensus baselines while a large realized-vs-headroom gap persists — the same structure as the C1 artifact.

**Sources:** [Scalable Best-of-N Selection for Large Language Models via Self-Certainty (arXiv:2502.18581)](https://arxiv.org/abs/2502.18581) (2025-02-25) · [OpenReview page (2nd AI for Math Workshop @ ICML 2025)](https://openreview.net/forum?id=nddwJseiiy) · verified: True

### D3-2 — [new] axis: b-estimate-R · bears on: M5

The Anatomy of the CTC Oracle Gap (Novosad, 2026-06-22) shows model-internal confidence is exhausted as a hypothesis selector: eleven CTC-internal/acoustic scoring strategies give no statistically significant WER gain over greedy at beam G=16 on LibriSpeech dev-other (all p>0.05), and the score-vs-WER Spearman correlation degrades from -0.574 (G=4) to -0.270 (G=128). External linguistic information from a FROZEN pretrained LM (RoBERTa pseudo-log-likelihood as MBR utility, no ground truth at deployment) breaks the bottleneck: 5.96%→5.42% WER on held-out test-other (9.0% relative, p<0.0001). Direct evidence that the deployable label-free selector gap can be partially closed with frozen-model external signals rather than internal confidence.

**Sources:** [The Anatomy of the CTC Oracle Gap: Acoustic Exhaustion and Linguistic Recovery (arXiv:2606.23306)](https://arxiv.org/abs/2606.23306) (2026-06-22) · verified: True

### D3-3 — [new] axis: a-change-q0 · bears on: M3, M5

RECOVER (2026-03-17) is a training-free agentic ASR entity-correction system: it treats multiple ASR hypotheses as evidence, retrieves relevant entities, and applies constrained frozen-LLM correction; across five datasets it reports 8-46% relative entity-WER reduction and up to +22pp entity recall, with an LLM-Select variant best overall while preserving global WER. It instantiates retrieval-conditioned hypothesis orchestration without gradients — retrieval injects entity support the hypothesis list lacks (q0-moving) and the LLM-Select stage is a deployable selector.

**Sources:** [RECOVER: Robust Entity Correction via agentic Orchestration of hypothesis Variants for Evidence-based Recovery (arXiv:2603.16411)](https://arxiv.org/abs/2603.16411) (2026-03-17) · verified: True

### D3-4 — [new] axis: a-change-q0 · bears on: M3

kNN-for-Whisper (Findings of NAACL 2025) adapts a fully frozen Whisper via token-level k-nearest-neighbor search over an external datastore at inference — no gradient updates — improving recognition analyzed by gender, accent, and age. It is a concrete gradient-free memory-injection operator for speech: an external retrieval structure changes the effective decoding distribution q0 of a frozen ASR model, precisely the operator class the killed formalism does not represent.

**Sources:** [kNN For Whisper And Its Effect On Bias And Speaker Adaptation (arXiv:2410.18850)](https://arxiv.org/abs/2410.18850) (2024-10-24) · verified: True

### D3-5 — [new] axis: a-change-q0 · bears on: M3, M5

ProGRes (SLT 2024) is a zero-shot, training-free prompted generative rescoring method on ASR n-best: an instruction-tuned frozen LLM both GENERATES new candidate hypotheses (expanding the n-best support beyond what the ASR sampler produced) and rescores via a combination of ASR confidence and frozen-LLM sequence scores, yielding 5-25% relative WER improvement across recognizers. Prompt-based hypothesis generation is a training-free support-expansion operator that moves the candidate-pool oracle ceiling itself.

**Sources:** [ProGRes: Prompted Generative Rescoring on ASR n-Best (arXiv:2409.00217)](https://arxiv.org/abs/2409.00217) (2024-08-30) · verified: True

### D3-6 — [new] axis: b-estimate-R · bears on: M5, S7, U4

Züfle et al. (2026-05-27) show current speech-translation quality metrics — including reference-free QE, speech-encoder-based metrics, and a state-of-the-art SpeechLLM evaluator — are blind to speech-specific phenomena (speaker gender, prosody, emphasis): models tend to ignore the audio signal even when given access, and their new SpeechCOMET matches standard performance but still fails to consistently assess speech phenomena. NEGATIVE evidence: deployment-time R for speech-to-speech remains not reliably reference-free-computable, and specifically not on the paralinguistic axis — consistent with the 7/02 verdict's S7 rather than overturning it.

**Sources:** [Why We Need Speech to Evaluate Speech Translation (arXiv:2605.28227)](https://arxiv.org/abs/2605.28227) (2026-05-27) · verified: True

### D3-7 — [update] axis: b-estimate-R · bears on: M5

BLASER 2.0-QE is a reference-free (quality-estimation) variant of the BLASER speech/text translation metric, scoring individual translations at sentence level from SONAR embeddings covering 57 speech languages — the standard deployable reference-free reward proxy for speech translation. Scope-fence note: it is a trained regression head on frozen embeddings, so it is context (quantifies what reference-free S2S QE achieves), not an in-scope mechanism; the archive already contains the Seamless paper that ships it, so this carries at most update weight.

**Sources:** [BLASER 2.0: a metric for evaluation and quality estimation of massively multilingual speech and text translation (Meta AI)](https://ai.meta.com/research/publications/blaser-2-0-a-metric-for-evaluation-and-quality-estimation-of-massively-multilingual-speech-and-text-translation/) (2023-12) · [Seamless: Multilingual Expressive and Streaming Speech Translation (arXiv:2312.05187)](https://arxiv.org/abs/2312.05187) (2023-12) · verified: True

### D3-8 — [new] axis: b-estimate-R · bears on: M5

Jasiński et al. (2026-06-22) find that the strongest label-free (no ground-truth reference at deployment) Whisper hallucination detection comes from probing the decoder's internal representations, beating text-metric heuristics (avg_logprob/compression-ratio/no-speech-prob, on which a classifier reaches only F1 23.6%) and LLM-based detection; a late-fusion meta-classifier is best overall. Scope-fence note: the probes are gradient-trained, so this is OUT as a thesis mechanism but quantifies the gap between training-free confidence signals and what supervised probes on the same frozen internals can achieve.

**Sources:** [From Text Metrics to Model Internals: A Study of Whisper ASR Hallucination Detection (arXiv:2606.23060)](https://arxiv.org/abs/2606.23060) (2026-06-22) · verified: True

### D3-9 — [new] axis: b-estimate-R · bears on: M5

Reference-free WER prediction for ASR is a maturing field but every instance found is gradient-trained: 'On the Robust Approximation of ASR Metrics' (Feb 2025, ACL 2025) approximates WER/CER label-free via multimodal embeddings + proxy references + trained regression over 40 models, and a 2026 Springer study (SPECOM 2025) predicts WER without ground truth from audio-quality and model-confidence features on Whisper/FastConformer. Context only (scope fence): these quantify achievable reference-free R-estimation quality for ASR, but none provides a training-free proxy the thesis could adopt directly.

**Sources:** [On the Robust Approximation of ASR Metrics (arXiv:2502.12408)](https://arxiv.org/abs/2502.12408) (2025-02-18) · [Ground Truth-Free WER Prediction for ASR via Audio Quality and Model Confidence Features (Springer, SPECOM 2025, LNCS 16188)](https://link.springer.com/chapter/10.1007/978-3-032-07959-6_3) (2026) · verified: True

### D3-10 — [new] axis: b-estimate-R · bears on: M5

LLM-Confidence Reranker (2026-02-14) is a training-free, plug-and-play retrieval reranker: black-box confidence from multinomial sampling + semantic clustering (Maximum Semantic Cluster Proportion) of a frozen 7-9B LLM's responses reranks retrieved documents, improving NDCG@5 by up to 20.6% with no training or internal parameter access. Text-RAG domain, but it is fresh evidence that sampling-consistency confidence of a frozen model is a workable training-free selection signal in retrieval-conditioned settings — the signal family M5 would extend with cross-session accumulation.

**Sources:** [LLM-Confidence Reranker: A Training-Free Approach for Enhancing Retrieval-Augmented Generation Systems (arXiv:2602.13571)](https://arxiv.org/abs/2602.13571) (2026-02-14) · verified: True

### D3-11 — [new] axis: b-estimate-R · bears on: M5, P6

MemReward (v1 2026-03-13) stores rollouts in a heterogeneous graph experience memory and propagates rewards from labeled to unlabeled samples, reaching 96.6-97.3% of oracle-reward performance with only 20% ground-truth labels (math/QA/code, Qwen2.5 1.5B/3B; no speech). Scope-fence note: the propagation network is a gradient-trained GNN inside an RL fine-tuning pipeline, so OUT as mechanism — but it is the closest published quantification of how well memory-based reward propagation can approximate a sparse oracle R, i.e., a trained upper reference for M5's no-gradient ambition.

**Sources:** [MemReward: Graph-Based Experience Memory for LLM Reward Prediction with Limited Labels (arXiv:2603.19310)](https://arxiv.org/abs/2603.19310) (2026-03-13) · verified: True

### D3-12 — [new] axis: background · bears on: 

Dang, Gao & Jia (2025-03-30) propose five training-free test-time-compute methods that significantly improve auditory cognition (comprehension, recall, recognition under noise/overlap) across five audio LLMs without retraining — claimed as the first systematic TTC study specific to audio language models. Background support for Part-A direction rationality (inference-time compute activates latent capability in frozen speech/omni models); it contains no selector-gap or agentic content.

**Sources:** [Scaling Auditory Cognition via Test-Time Compute in Audio Language Models (arXiv:2503.23395)](https://arxiv.org/abs/2503.23395) (2025-03-30) · verified: True

## Negative findings (verified empty searches — decision-relevant)

- Post-freeze window empty: searched 2026-07-03 for arXiv items dated 2026-06-27 through 2026-07-03 on best-of-N / ASR hypothesis selection / speech reward proxies — nothing surfaced; the newest relevant speech items found are arXiv:2606.23306 and arXiv:2606.23060, both 2026-06-22 (pre-dating the 06/26 novelty line but absent from the archive, so admissible under criterion (i)).
- M5's exact object is unoccupied in the literature as of 2026-07-03: no published no-gradient, cross-session/accumulating selector or reward estimator for ASR hypothesis selection (retrieval credit assignment over speech experience) was found. All near misses are text-domain and/or gradient-trained: JitRL (already archived), ExpRAG arXiv:2603.18272 (LoRA SFT — weight-updating), MemReward arXiv:2603.19310 (trained GNN), Memory-T1 arXiv:2512.20092 (RL-trained memory-selection policy). Consequence: no scoop risk for M5, and also no r3-triggering literature that would overturn a lane kill.
- No gradient-free reference-free WER predictor exists anywhere in the searched literature: every reference-free ASR quality-estimation metric found (NoRefER arXiv:2306.13114, arXiv:2502.12408, the 2026 Springer ground-truth-free WER predictor, arXiv:2606.23060 decoder-state probes) trains a regressor/probe. The only training-free label-free ASR selection signals remain model-internal confidence — shown statistically null as a selector at G=16 by arXiv:2606.23306 — and consensus/MBR, which is C1's committed null.
- No oracle-vs-deployable best-of-N selector-gap study found for speech-to-speech generation: BLASER 2.0-QE exists as a reference-free S2S metric, but no work was found that samples N speech outputs and quantifies oracle-vs-deployable selection gaps on them; arXiv:2605.28227 additionally shows current speech QE metrics ignore the audio signal, so the S2S estimating-R gap is unmeasured, not closed.
- Training-free retrieval-conditioned contextual biasing for speech LLMs is thinning, not growing: recent 2026 biasing work found (LOGIC arXiv:2601.15397 logit-space integration; hotword-retrieval + GRPO arXiv:2512.21828; bias-word position prediction arXiv:2604.12398) is predominantly gradient-trained; kNN-for-Whisper (arXiv:2410.18850) remains the main verified gradient-free retrieval-adaptation instance for frozen ASR.
- Verifier note: openreview.net is unfetchable from this environment (enterprise network block), so the D3-1 OpenReview source was confirmed by web search (forum id nddwJseiiy resolves to the self-certainty paper, 2nd AI for Math Workshop @ ICML 2025) rather than direct fetch; the arXiv source was fetched directly and fully supports the claim including the oracle-gap sentence.