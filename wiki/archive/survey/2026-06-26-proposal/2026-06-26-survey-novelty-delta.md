> **🗄 ARCHIVED (2026-07-11)** — 已收官战役过程件（2026-06-26 提案期调研），仅作历史，非现行真源。

# Lane 5 — Novelty-delta vs the closest prior work

> Part of the **Step-2 survey** for [[2026-06-26-training-free-rl-for-speech-omni-research-proposal]] (see [[Research-Proposal-Template]] §3). Produced by a multi-agent survey workflow (5 lanes -> per-lane adversarial verification -> synthesis), run `wf_d76b4901-23c`, 2026-06-26. Every source below was adversarially checked to resolve to a real paper; only `keep=true` claims are archived. Links are real and verifiable.


**Lane summary.** No single published paper does the exact study proposed here: a controlled cross-MODEL-CLASS (generative autoregressive vs label-free contrastive bi-encoder) test of training-free, reward-selected ICL as a CAPABILITY-ACTIVATION lever on FROZEN omni models, with the falsifiable asymmetry that ICL activates suppressed capabilities on the generative class but not the vector class. The novelty is the specific combination; each constituent axis, however, has a clear closest prior. The two tightest competitors are bge-en-icl ("Making Text Embedders Few-Shot Learners", 2409.15700), which shows ICL helps an LLM-derived embedder but ONLY after contrastive fine-tuning that teaches it to use the demonstrations, and MiMo-Audio ("Audio Language Models are Few-Shot Learners", 2512.23808), which shows emergent few-shot ICL in audio LLMs but as a property instilled by large-scale PRETRAINING, not reward-selected activation of a frozen off-the-shelf model. The training-free-RL machinery (TTRL 2504.16084, TPO 2501.12895, JitRL 2601.18510) and the inference-time-tilting theory (best-of-N 2401.01879/2507.05913; the RLVR "sharpening-not-creating" debate 2506.14245/2602.08281) are mature but single-class, text-centric, and never framed as a cross-class ICL asymmetry. The honest residual delta is therefore the cross-class controlled design on a shared omni backbone plus the suppressed-capability map, not the individual ingredients.


**Adversarial verifier assessment.** Strong lane. Every cited closest-prior arXiv ID (12 claims, 19 distinct sources) resolves to a real paper with a matching title, including the future-dated 2025-2026 IDs (2512.23808 MiMo-Audio, 2601.18510 JitRL, 2602.08281, 2603.15981), and the stance attributed to each source is broadly accurate. The novelty-delta argument is honestly framed: the proposed contribution is the cross-model-class controlled ICL-activation test on a shared omni backbone plus the suppressed-capability map, not the individual ingredients, and each constituent axis is correctly mapped to its tightest prior (bge-en-icl for the vector negative, MiMo-Audio for the generative positive, TTRL/TPO/JitRL for the training-free machinery, best-of-N theory for the Gibbs tilting, LEACE for Operator-A erasure). All 12 claims are kept. Three items warrant correction rather than removal: (1) ND5 mis-groups 2506.14245 with the 'RLVR-sharpens-not-creates' camp - that paper in fact rebuts the pass@k/sharpening interpretation and argues RLVR extends the boundary; the canonical sharpening paper (Yue et al. 2504.13837) is the one that belongs there and is uncited. (2) ND7's 'final layers suppress speaker' framing is partially contradicted by its own second source (2501.05310 finds larger models recover speaker ID in deep layers). (3) ND12 is a genuinely useful correction - it fixes a real citation error in the project brief (2104.01767 is WhiteningBERT, not LEACE/RLACE; LEACE is 2306.03819, verified). No fabricated IDs were found in this lane.


---

## Verified claims & sources (12 kept / 12 total)


### ND1 · empirical · confidence: high

The closest VECTOR-class prior is bge-en-icl ('Making Text Embedders Few-Shot Learners'), which demonstrates that few-shot in-context examples on the query side improve an LLM-initialized embedder (Mistral-7B) on MTEB (71.67 few-shot). DELTA: their ICL ability is INSTILLED by contrastive fine-tuning with few-shot examples, not present training-free; the proposed study tests a FROZEN, label-free omni bi-encoder whose masked-mean pooling collapses the conditioning channel, and finds ICL does NOT activate (and even hurts emotion 0.217->0.150, label-insensitive). bge-en-icl thus corroborates H1's mechanism rather than refuting it: ICL in embedders requires explicit training.


- **Sources:** [Making Text Embedders Few-Shot Learners (bge-en-icl)](https://arxiv.org/abs/2409.15700)

- **Relevance:** H1 (vector-class negative) — closest prior; sharpens the delta that frozen, label-free contrastive pooling cannot be ICL-activated


### ND2 · empirical · confidence: high

The closest GENERATIVE-class audio prior is MiMo-Audio ('Audio Language Models are Few-Shot Learners'), which shows large-scale lossless audio pretraining yields emergent few-shot ICL across diverse speech tasks via a non-linear 'phase-transition' emergence. DELTA: MiMo-Audio is about PRETRAINING a model so ICL emerges; the proposed study activates ICL on a FROZEN off-the-shelf omni model via REWARD-SELECTED conditioning (verifiable-reward best-of-N / MBR over instruction-conditioned generations), and does so as a controlled cross-class comparison rather than a single-model capability demo.


- **Sources:** [MiMo-Audio: Audio Language Models are Few-Shot Learners](https://arxiv.org/abs/2512.23808)

- **Relevance:** H1 (generative-class positive) / H3 — closest prior; delta is frozen-model reward-selected activation vs pretraining-induced emergence


### ND3 · empirical · confidence: high

The closest TRAINING-FREE / TEST-TIME RL priors are TTRL (test-time RL with majority-vote rewards on unlabeled data), TPO (test-time preference optimization via iterative textual feedback), and JitRL (gradient-free test-time policy optimization that modulates output logits, proven to be the closed-form solution of a KL-constrained objective). DELTA: all three are TEXT-only, single-model-class (generative LLMs), and frame the lever as reward optimization, NOT as in-context conditioning; none compares a generative model against an embedding model, none touches speech/omni, and none poses a capability-activation asymmetry.


- **Sources:** [TTRL: Test-Time Reinforcement Learning](https://arxiv.org/abs/2504.16084) · [Test-Time Preference Optimization: On-the-Fly Alignment via Iterative Textual Feedback](https://arxiv.org/abs/2501.12895) · [Just-In-Time Reinforcement Learning: Continual Learning in LLM Agents Without Gradient Updates](https://arxiv.org/abs/2601.18510)

- **Relevance:** Operator-B machinery / unified Gibbs objective — closest training-free-RL priors; delta is cross-class + ICL-as-lever + omni


### ND4 · theoretical · confidence: high

The closest THEORY priors give the exact objective q*(z) ∝ q0(z)·exp(R/β) machinery: best-of-N alignment theory (KL upper bound log n − (n−1)/n is only an upper bound; win-rate bound n/(n+1)) and the smoothing-lens KL/regret analysis. DELTA: these are class-agnostic generative-decoding results; the proposed work OPERATIONALIZES the tilting view as a cross-model-class falsifiability test — the operator can only amplify a conditioning channel the architecture PRESERVES, which generative decoding does and contrastive masked-mean pooling does not.


- **Sources:** [Theoretical guarantees on the best-of-n alignment policy](https://arxiv.org/abs/2401.01879) · [Best-of-N through the Smoothing Lens: KL Divergence and Regret Analysis](https://arxiv.org/abs/2507.05913)

- **Relevance:** Unified objective (Gibbs/exponential tilting) — closest theory; delta is cross-class operationalization


### ND5 · theoretical · confidence: med

The 'activation-not-addition' boundary that explains the asymmetry has a closest prior in the RLVR-elicitation debate: RLVR/inference-time selection SHARPENS the base distribution and amplifies pre-existing competencies rather than injecting new capability (base model often overtakes RL variants at large pass@k). DELTA: that debate is confined to text reasoning within ONE model; the proposed study uses the same principle to PREDICT a cross-class outcome — a capability absent from a model class's recoverable base distribution (e.g. speaker ~chance, emotion suppressed in the vector class) cannot be activated by any training-free operator, whereas the generative class preserves the channel and is activable.


- **Sources:** [RLVR Implicitly Incentivizes Correct Reasoning in Base LLMs](https://arxiv.org/abs/2506.14245) · [New Skills or Sharper Primitives? A Probabilistic Perspective on the Emergence of Reasoning in RLVR](https://arxiv.org/abs/2602.08281) · [The Debate on RLVR Reasoning Capability Boundary: Shrinkage, Expansion, or Both?](https://arxiv.org/abs/2510.04028)

- **Relevance:** Theoretical bridge for H1/H2 — why the asymmetry exists; delta is cross-class prediction vs single-model debate


### ND6 · definitional · confidence: high

The proposed vector model (omni-embed-nemotron-3b, a bi-encoder built on the Qwen2.5-Omni-3B Thinker, masked-mean -> single L2-normalized vector) and the generative class (full Qwen2.5-Omni Thinker-Talker) SHARE a backbone family, making the asymmetry a near-clean architectural ablation rather than a confound. DELTA vs prior cross-class embedding studies (e.g. diffusion-vs-autoregressive text-embedding comparisons): those compare embedding QUALITY across architectures; none isolates ICL-activation under a frozen reward-guided operator on a shared omni backbone where one branch keeps the Talker/decoder channel and the other discards it via contrastive pooling.


- **Sources:** [Omni-Embed-Nemotron: A Unified Multimodal Retrieval Model for Text, Image, Audio, and Video](https://arxiv.org/abs/2510.03458) · [Diffusion vs. Autoregressive Language Models: A Text Embedding Perspective](https://arxiv.org/abs/2505.15045)

- **Relevance:** Study design / H1 cleanliness — shared-backbone ablation is the novel control; delta vs cross-class embedding-quality studies


### ND7 · empirical · confidence: med

The closest CAPABILITY-PRESENCE priors are layer-wise probing studies of frozen self-supervised speech encoders showing speaker/emotion live in intermediate layers while final layers suppress speaker to abstract linguistic content. DELTA: these probe SSL encoders (HuBERT/WavLM-style) with linear probes only; the proposed H2 map probes a frozen omni-LLM embedder AND its generative twin, and adds the reward-guided ICL-activation layer on top — explaining the in-house finding (vector speaker ~chance across all 37 layers/poolings; emotion liftable by mid-layer attentive pooling 0.39->0.49) as a presence-vs-activability distinction.


- **Sources:** [What do self-supervised speech and speaker models learn? New findings from a cross model layer-wise analysis](https://arxiv.org/abs/2401.17632) · [A Large-Scale Probing Analysis of Speaker-Specific Attributes in Self-Supervised Speech Representations](https://arxiv.org/abs/2501.05310)

- **Relevance:** H2 capability-presence map — closest probing priors; delta is omni-LLM embedder + activation layer vs SSL-encoder probing


### ND8 · empirical · confidence: high

The closest SPEECH-LLM-RL-for-paralinguistics prior aligns paralinguistic understanding and generation in speech LLMs via multi-task RL (and parameter-efficient SER adapters like EmoSLLM). DELTA: these UPDATE WEIGHTS (RL fine-tuning / LoRA); the proposed work is strictly training-free and frozen — same target capability (emotion/paralinguistics) but achieved purely by inference-time reward-guided conditioning, which is exactly what makes the negative vector-class result interpretable (no weights move, so any lift must come from the preserved conditioning channel).


- **Sources:** [Aligning Paralinguistic Understanding and Generation in Speech LLMs via Multi-Task Reinforcement Learning](https://arxiv.org/abs/2603.15981) · [EmoSLLM: Parameter-Efficient Adaptation of LLMs for Speech Emotion Recognition](https://arxiv.org/abs/2508.14130)

- **Relevance:** Contrast for the training-free constraint — delta is frozen/no-weight-change vs RL fine-tuning


### ND9 · empirical · confidence: high

The vector-class negative is independently supported by instruction-following benchmarks showing embedding models barely follow even explicit task instructions, let alone few-shot demonstrations. DELTA: prior work (INSTRUCTIR, FollowIR, MMTEB's instruction-following tasks) measures instruction-following deficits as a benchmark problem to be FIXED by more training; the proposed study reframes the same deficit as evidence for a CLASS-LEVEL ceiling on training-free ICL activation, and pairs it with the generative class where the same instructions DO activate capability.


- **Sources:** [INSTRUCTIR: A Benchmark for Instruction Following of Information Retrieval Models](https://arxiv.org/abs/2402.14334) · [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595)

- **Relevance:** H1 vector-class negative — corroborating evidence; delta is class-ceiling reframing vs benchmark-to-fix


### ND10 · empirical · confidence: med

For H3 (decomposing the generative lift into explicit-task-definition vs k-shot demos vs instruction richness), the closest priors are the ICL-mechanism literature on label sensitivity: demonstrations help largely via format/label-space/input-distribution rather than correct input-label mapping ('labels barely matter'), with a counter-line showing ground-truth labels DO matter under some conditions. DELTA: that debate is text-classification ICL within one generative model; the proposed H3 ports the same label-sensitivity decomposition to a FROZEN omni model under a verifiable reward, and contrasts it against the in-house vector-class result that ICL there is label-INSENSITIVE (representation move 0.336 vs label-sensitivity 0.047) — i.e. the decomposition itself becomes a cross-class diagnostic.


- **Sources:** [Ground-Truth Labels Matter: A Deeper Look into Input-Label Demonstrations](https://arxiv.org/abs/2205.12685)

- **Relevance:** H3 decomposition — closest mechanism prior; delta is cross-class label-sensitivity as a diagnostic on a frozen omni model


### ND11 · empirical · confidence: high

The MBR-for-ASR and audio-cue-reliance priors anchor the verifiable-reward operator and the capability-presence caveat. MBR decoding outperforms beam search for ASR/ST (Whisper) — a training-free reranking gain — while 'Do Audio LLMs Really LISTEN?' shows audio LLMs often lean on lexical rather than acoustic cues. DELTA: MBR-ASR is a single-task quality method, not a capability-activation framework; combined with the lexical-vs-acoustic finding, it predicts the proposed generative lifts will be strongest for content/intent (lexical-recoverable) and weakest for purely acoustic capabilities — a falsifiable refinement of H2 that neither prior states.


- **Sources:** [Re-evaluating Minimum Bayes Risk Decoding for Automatic Speech Recognition](https://arxiv.org/abs/2510.19471) · [Do Audio LLMs Really LISTEN, or Just Transcribe? Measuring Lexical vs. Acoustic Emotion Cues Reliance](https://arxiv.org/abs/2510.10444)

- **Relevance:** Operator-B reward / H2 refinement — delta is capability-activation framing + lexical/acoustic boundary prediction


### ND12 · definitional · confidence: high

Anchor-id correction relevant to the concept-erasure subspace tooling (Operator A linear-subspace projection): the canonical LEACE paper ('Perfect linear concept erasure in closed form') is arXiv:2306.03819, not the 2104.01767 listed in the brief; RLACE (Linear Adversarial Concept Erasure, Ravfogel et al.) is a separate paper. Verifying these IDs matters because the vector-class steering claims (linear-subspace projection / concept scrubbing) should cite the correct closed-form erasure result, which LEACE provides (oblique projections proven optimal; ~2 orders faster than RLACE, no gradient optimization).


- **Sources:** [LEACE: Perfect linear concept erasure in closed form](https://arxiv.org/abs/2306.03819)

- **Relevance:** Operator-A linear-subspace projection citation hygiene — corrects a brief anchor id
