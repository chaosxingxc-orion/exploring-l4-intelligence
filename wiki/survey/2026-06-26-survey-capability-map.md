# Lane 1 — Omni pretrained-capability map & the two model classes

> Part of the **Step-2 survey** for [[2026-06-26-training-free-rl-for-speech-omni-research-proposal]] (see [[Research-Proposal-Template]] §3). Produced by a multi-agent survey workflow (5 lanes -> per-lane adversarial verification -> synthesis), run `wf_d76b4901-23c`, 2026-06-26. Every source below was adversarially checked to resolve to a real paper; only `keep=true` claims are archived. Links are real and verifiable.


**Lane summary.** Omni/speech multimodal LLMs acquire a broad pretraining capability stack — ASR, speech translation, language-ID, VAD, intent/SLU, spoken-QA, audio reasoning, and (weakly) paralinguistics (emotion/SER, speaker-ID) — which the SUPERB/Dynamic-SUPERB taxonomies make explicit and which Whisper/SeamlessM4T/Qwen-Audio/SALMONN realize at scale. The two model classes diverge mechanistically: the GENERATIVE class (Qwen2.5/3-Omni Thinker-Talker, Qwen2-Audio, SALMONN, MiniCPM-o) is an autoregressive instruction-follower that keeps token-level, instruction-conditioned access to content AND paralinguistics, exhibits emergent few-shot/in-context learning (SALMONN activation tuning, MiMo-Audio), and is therefore steerable by Operator-B style conditioning. The VECTOR class (omni-embed-nemotron-3b = Qwen2.5-Omni Thinker + masked-mean → one L2-normalized 2048-d vector, trained with InfoNCE, like CLAP/NV-Embed) optimizes alignment+uniformity on a hypersphere, which provably discards features not needed to separate the contrastive positives — explaining why content/ASR semantics survive natively (~probe 1.0) while emotion is suppressed and ICL-insensitive, speaker collapses to chance (mean pooling cannot recover the higher-order statistics ECAPA/attentive-stats-pooling need), and intent is present but not instruction-steerable. This grounds H1 (ICL activates an under-exposed capability on the generative class but not on the label-free contrastive bi-encoder), supplies the H2 presence map per class, and supports the H3 decomposition (task-definition vs k-shot vs instruction richness) via the SALMONN/MiMo emergent-ICL evidence.


**Adversarial verifier assessment.** Strong, well-grounded lane. Every one of the 20 claims cites a real, verifiable source (arXiv id / ACL Anthology URL / TACL DOI), and in each case the source content supports the stated claim with no fabricated ids and no material overstatement. I verified the riskier/recent ids by direct search (2510.03458 Omni-Embed-Nemotron built on Qwen2.5-Omni-3B Thinker; 2512.23808 MiMo-Audio "over one hundred million hours" → emergent few-shot/phase transition; 2410.01162 frozen-LLM paralinguistics; 2601.03115 emotion-sensitive neurons in Qwen2.5-Omni/Kimi-Audio/Audio Flamingo 3; 2411.05361 Dynamic-SUPERB Phase-2 180 tasks; 2411.17666 cross-modal convergence over layers; 2406.10056 UniAudio 1.5 cross-modal ICL) and confirmed numeric specifics (Whisper 680k hrs; MMAU 10k clips/27 skills/18 models; Dynamic-SUPERB 33 tasks/22 datasets; Attentive Stats EER −7.5%/−8.1%; SeamlessM4T ~100 langs/1M hrs; NV-Embed latent-attention pooling + causal-mask removal). Two soft spots, both kept: (C8) SALMONN's "few-shot activation tuning" is the paper's own exact term, but it is a light LoRA-scaling training stage, not pure inference-time ICL — so analogizing it to inference-time Operator-B is a mild stretch in the relevance framing, though the statement itself is faithful; (C15) the quoted "lose the modulus-length features, retain orientation" phrasing is not in the two cited papers (Wang&Isola 2005.10242, SimCSE 2104.08821) — it is a generic L2-normalization fact, so that specific quote is mis-attributed, but the core alignment/uniformity-on-hypersphere mechanism the claim rests on IS supported by both real sources. The contrastive-suppression mechanism claims (C14–C16) are correctly hedged at med confidence and are analogical extensions (vision/text-domain theory applied to audio paralinguistics), which is reasonable but not directly proven on omni audio embedders. No claim should be dropped.


---

## Verified claims & sources (20 kept / 20 total)


### C1 · definitional · confidence: high

The GENERATIVE omni class is defined by the Thinker-Talker architecture: a Transformer-decoder 'Thinker' (with audio/vision encoders) autoregressively produces high-level representations and text, and a 'Talker' streams speech tokens from those representations; the whole model is end-to-end autoregressive and instruction-conditioned.


- **Sources:** [Qwen2.5-Omni Technical Report](https://arxiv.org/abs/2503.20215) · [Qwen3-Omni Technical Report](https://arxiv.org/abs/2509.17765)

- **Relevance:** Defines model class (B) for H1/H2; the autoregressive instruction-follower is the substrate Operator-B / ICL steers.


### C2 · definitional · confidence: high

The in-house VECTOR omni model (omni-embed-nemotron-3b) is built from ONLY the Qwen2.5-Omni-3B Thinker, used as a contrastive bi-encoder that masked-mean-pools token states into a single ~2048-dimensional L2-normalized embedding trained with InfoNCE-style query/positive/negative contrast — i.e., the same generative backbone repurposed into a label-free vector space.


- **Sources:** [Omni-Embed-Nemotron: A Unified Multimodal Retrieval Model for Text, Image, Audio, and Video](https://arxiv.org/abs/2510.03458)

- **Relevance:** Defines model class (A); the exact in-house vector model. Same backbone as the generative class isolates pooling+objective (not the encoder) as the cause of the H1 asymmetry.


### C3 · definitional · confidence: high

The contrastive-bi-encoder design pattern of the vector class is the audio-domain instance of CLAP: two encoders mapped into a shared space with InfoNCE and L2 normalization, optimized for cross-modal/semantic retrieval alignment rather than per-utterance reconstruction.


- **Sources:** [CLAP: Learning Audio Concepts From Natural Language Supervision](https://arxiv.org/abs/2206.04769)

- **Relevance:** Generalizes class (A) beyond the specific in-house model; the InfoNCE+L2 objective is the shared mechanism behind paralinguistic suppression.


### C4 · empirical · confidence: high

Turning a decoder LLM into an embedding model is governed by the pooling+objective, not the backbone: NV-Embed shows a latent-attention pooling layer beats mean-pooling and last-token pooling, and that the causal mask is removed during contrastive training — evidence that the masked-mean pooling step (not the pretrained knowledge) bottlenecks what an embedding can expose.


- **Sources:** [NV-Embed: Improved Techniques for Training LLMs as Generalist Embedding Models](https://arxiv.org/abs/2405.17428)

- **Relevance:** Mechanistic support for H1/H2: the masked-mean pooling in class (A) is a lossy aggregator; the capability ceiling is set by pooling+objective, which is why in-house pooling sweeps move emotion but not speaker.


### C5 · empirical · confidence: high

Large-scale weakly-supervised pretraining endows a single speech model with multiple capabilities at once — multilingual ASR, speech translation, spoken language identification, and voice activity detection — establishing ASR/ST/LID/VAD as natively pretrained, content-side capabilities.


- **Sources:** [Robust Speech Recognition via Large-Scale Weak Supervision (Whisper)](https://arxiv.org/abs/2212.04356)

- **Relevance:** H2 capability map: content/linguistic tasks (ASR, ST, LID) are pretraining-native and thus the capabilities the vector class probes near-saturate (~1.0) while paralinguistics is not part of this supervised signal.


### C6 · empirical · confidence: high

Speech translation (S2T, S2S) and ASR for up to ~100 languages are acquired as unified pretrained capabilities in a single multimodal-translation foundation model, confirming translation as a content-side capability the generative class exposes directly.


- **Sources:** [SeamlessM4T: Massively Multilingual & Multimodal Machine Translation](https://arxiv.org/abs/2308.11596) · [Seamless: Multilingual Expressive and Streaming Speech Translation](https://arxiv.org/abs/2312.05187)

- **Relevance:** H2 map: ST is content-native (survives in class A), and the expressive/streaming variant shows paralinguistic preservation is an explicit extra objective, not a default of the contrastive route.


### C7 · empirical · confidence: high

The generative class is explicitly an instruction-follower over audio: Qwen2-Audio handles voice-chat and audio-analysis modes, follows free-form natural-language/voice instructions, and was made SOTA on audio-centric instruction-following via natural-language task prompts + DPO — the property Operator-B/ICL exploits.


- **Sources:** [Qwen2-Audio Technical Report](https://arxiv.org/abs/2407.10759) · [Qwen-Audio: Advancing Universal Audio Understanding](https://arxiv.org/abs/2311.07919)

- **Relevance:** H1/H3: explicit instruction-conditioning is a built-in affordance of class (B), so explicit-task-definition + instruction-richness are plausibly the largest levers in the H3 decomposition.


### C8 · empirical · confidence: high

A frozen-LLM-plus-encoder generative speech model (SALMONN) natively performs ASR, speech translation, emotion recognition, speaker verification and audio QA, AND exhibits emergent untrained abilities (untrained-language ST, slot filling, spoken-QA, audio co-reasoning) that are *activated* by a few-shot activation-tuning procedure — direct precedent that few-shot/ICL conditioning unlocks dormant capabilities on the generative class.


- **Sources:** [SALMONN: Towards Generic Hearing Abilities for Large Language Models](https://arxiv.org/abs/2310.13289)

- **Relevance:** Strongest published anchor for H1/H3 on class (B): few-shot conditioning ACTIVATES under-exposed capabilities in a generative omni model — exactly the in-house SLURP/URO/MInDS Operator-B lifts.


### C9 · empirical · confidence: high

Audio language models exhibit emergent in-context / few-shot learning that arises non-linearly with pretraining scale: crossing a data threshold triggers a 'phase transition' into GPT-3-style few-shot generalization across ASR, audio reasoning (MMAU), voice conversion, and emotion/rate conversion — establishing ICL as a real, scale-emergent property of the generative class.


- **Sources:** [MiMo-Audio: Audio Language Models are Few-Shot Learners](https://arxiv.org/abs/2512.23808) · [UniAudio 1.5: LLM-driven Audio Codec is a Few-shot Audio Task Learner](https://arxiv.org/abs/2406.10056)

- **Relevance:** H1/H3: confirms k-shot demonstrations are a genuine activation lever on class (B); the generative lift the in-house study measures has an emergent-ICL mechanism, not just prompt formatting.


### C10 · definitional · confidence: high

The canonical capability taxonomy for speech representations (SUPERB) spans content (phoneme recognition, ASR, keyword spotting, query-by-example), semantics/SLU (intent classification, slot filling), and paralinguistics/speaker (speaker verification, diarization, emotion recognition) — fixing the per-capability axes along which the two classes can be compared.


- **Sources:** [SUPERB: Speech processing Universal PERformance Benchmark](https://arxiv.org/abs/2105.01051)

- **Relevance:** H2: provides the standardized capability list (content vs SLU vs speaker vs emotion) used to build the presence map per class.


### C11 · empirical · confidence: high

Instruction-following speech benchmarks explicitly separate capability dimensions into content, speaker, semantics, degradation, and paralinguistics — and find instruction-tuned spoken models perform reasonably on seen content/semantics tasks but struggle on unseen and on paralinguistic/speaker dimensions, matching the asymmetry that content survives while paralinguistics is fragile.


- **Sources:** [Dynamic-SUPERB: A Dynamic, Collaborative, Comprehensive Instruction-Tuning Benchmark for Speech](https://arxiv.org/abs/2309.09510) · [Dynamic-SUPERB Phase-2 (180 tasks)](https://arxiv.org/abs/2411.05361)

- **Relevance:** H2: empirical capability map showing content/semantics > paralinguistics/speaker on instruction-tuned generative models; frames which capabilities are 'under-exposed' and candidates for ICL activation.


### C12 · definitional · confidence: high

Intent/SLU and spoken-QA are recognized pretrained capabilities with dedicated benchmarks (SLURP: 18 domains, ~69 intents, intent-detection + slot-filling; AIR-Bench: open-ended audio QA / generative comprehension), giving the verifiable-reward targets the in-house Operator-B intent lifts use.


- **Sources:** [SLURP: A Spoken Language Understanding Resource Package](https://aclanthology.org/2020.emnlp-main.588/) · [AIR-Bench: Benchmarking Large Audio-Language Models via Generative Comprehension](https://arxiv.org/abs/2402.07729)

- **Relevance:** H1/H2: intent/SLU is the capability where in-house Operator-B yields the +0.330 SLURP lift on class (B) yet is present-but-not-steerable (~0.25) on class (A).


### C13 · empirical · confidence: high

Audio reasoning is a distinct, harder pretrained-capability axis (expert knowledge + multi-step inference over speech/sound/music) that current audio-language models find genuinely difficult, marking it as under-exposed and a prime target for reward-guided generative activation.


- **Sources:** [MMAU: A Massive Multi-Task Audio Understanding and Reasoning Benchmark](https://arxiv.org/abs/2410.19168)

- **Relevance:** H2/H1: audio reasoning is under-exposed even on class (B); a candidate where explicit task-definition + k-shot (H3 levers) could yield large measurable lift.


### C14 · theoretical · confidence: med

MECHANISM (paralinguistic suppression in the vector class): contrastive objectives learn invariances dictated by the positive-pair construction and therefore *discard* any feature not needed to separate positives from negatives — provably harming downstream tasks that rely on the discarded factor. For a content/semantic-positive contrastive omni embedder, speaker timbre and emotional prosody are exactly such discarded nuisance factors.


- **Sources:** [What Should Not Be Contrastive in Contrastive Learning](https://arxiv.org/abs/2008.05659)

- **Relevance:** Core mechanistic explanation for H1/H2: class (A) discards paralinguistics by construction, so no inference-time conditioning can recover speaker (chance) and emotion is intrinsically suppressed/ICL-insensitive.


### C15 · theoretical · confidence: med

MECHANISM (geometry of the vector class): the contrastive InfoNCE objective drives representations toward alignment (positives close) and uniformity on the unit hypersphere, and L2-normalization plus LayerNorm map text/audio onto a hypersphere that retains orientation while discarding modulus/magnitude — so per-utterance style/intensity information is geometrically removed from the single pooled vector.


- **Sources:** [Understanding Contrastive Representation Learning through Alignment and Uniformity on the Hypersphere](https://arxiv.org/abs/2005.10242) · [SimCSE: Simple Contrastive Learning of Sentence Embeddings](https://arxiv.org/abs/2104.08821)

- **Relevance:** H1/H2 mechanism: explains why a single L2-normalized masked-mean vector (class A) is structurally unable to expose magnitude/style-coded paralinguistics, regardless of conditioning.


### C16 · theoretical · confidence: high

MECHANISM (speaker collapses to chance under mean pooling): recovering speaker identity from frame features requires higher-order temporal statistics — speaker-verification SOTA explicitly pools weighted MEANS *and* weighted STANDARD DEVIATIONS (attentive statistics / ECAPA channel-attentive stats pooling); plain (masked) mean pooling discards the second-order statistics that carry speaker characteristics, so a mean-pooled bi-encoder is expected to be near-chance on speaker.


- **Sources:** [Attentive Statistics Pooling for Deep Speaker Embedding](https://arxiv.org/abs/1803.10963) · [ECAPA-TDNN: Emphasized Channel Attention, Propagation and Aggregation in TDNN Based Speaker Verification](https://arxiv.org/abs/2005.07143)

- **Relevance:** Directly explains the in-house finding that speaker is ~chance across all 37 layers and every pooling in class (A): masked-mean throws away the std/higher-order stats speaker-ID needs.


### C17 · empirical · confidence: high

MECHANISM (capability stratified by layer): self-supervised / encoder speech models encode information in a layer-wise hierarchy — acoustic/low-level features in early blocks, phonetic then word-identity/word-meaning in middle-to-late blocks — so paralinguistic/acoustic content is concentrated in specific (often mid) layers rather than the final layer a default embedder pools.


- **Sources:** [Layer-wise Analysis of a Self-supervised Speech Representation Model](https://arxiv.org/abs/2107.04734) · [Comparative layer-wise analysis of self-supervised speech models](https://arxiv.org/abs/2211.03929) · [What Do Self-Supervised Speech Models Know About Words?](doi:10.1162/tacl_a_00656)

- **Relevance:** Explains the in-house result that mid-layer attentive pooling lifts emotion 0.39->0.49 in class (A): the emotion signal is layer-localized, so Operator-A layer selection helps where final-layer mean pooling under-exposes it.


### C18 · empirical · confidence: high

MECHANISM (the generative class RETAINS paralinguistics): paralinguistic information (emotion, sentiment, pitch, speaking rate) is present in the speech-to-LLM token interface and can be perceived by a FROZEN LLM when the encoder exposes it — i.e., the autoregressive route preserves paralinguistics in its token stream rather than collapsing it, unlike the pooled-vector route.


- **Sources:** [Frozen Large Language Models Can Perceive Paralinguistic Aspects of Speech](https://arxiv.org/abs/2410.01162)

- **Relevance:** Core H1 asymmetry evidence: paralinguistics is recoverable on the generative (token-stream) class even when weights are frozen, whereas it is geometrically discarded on the pooled-vector class.


### C19 · empirical · confidence: med

Paralinguistic capability (emotion) is PRESENT but UNDERWEIGHTED in large audio-language models: LALMs prioritize linguistic semantics and underrepresent cues like pitch, rate, jitter, intensity; yet emotion is causally encoded — emotion-sensitive neurons can be localized and causally validated in LALMs — consistent with 'present but suppressed/needs activation' rather than 'absent'.


- **Sources:** [Benchmarking Contextual and Paralinguistic Reasoning in Speech-LLMs](https://arxiv.org/abs/2509.16589) · [Discovering and Causally Validating Emotion-Sensitive Neurons in Large Audio-Language Models](https://arxiv.org/abs/2601.03115)

- **Relevance:** H2/H3: on class (B) emotion is present-but-suppressed (localized neurons), making it the canonical 'under-exposed capability' for testing whether explicit task-definition + k-shot ICL activates it (H1's generative arm).


### C20 · empirical · confidence: med

MECHANISM (cross-modal encoding inside omni LLMs): in multimodal foundation models, text and speech representations converge to a shared space over depth except in early modality-specialized layers, and for models not explicitly trained for modality-agnostic representations the modality gap dominates — so where (which layer) and how speech is injected determines what downstream conditioning can access.


- **Sources:** [How do Multimodal Foundation Models Encode Text and Speech? An Analysis of Cross-Lingual and Cross-Modal Representations](https://arxiv.org/abs/2411.17666)

- **Relevance:** Supports Operator-A layer/subspace steering for class (A) and frames why injection layer matters; contextualizes why pooling at the final converged layer over-emphasizes content semantics over modality-specific paralinguistics.
