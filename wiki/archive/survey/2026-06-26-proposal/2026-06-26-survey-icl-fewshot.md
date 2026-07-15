> **🗄 ARCHIVED (2026-07-11)** — 已收官战役过程件（2026-06-26 提案期调研），仅作历史，非现行真源。

# Lane 2 — ICL / few-shot / explicit task-definition & label-sensitivity in audio LLMs

> Part of the **Step-2 survey** for [[2026-06-26-training-free-rl-for-speech-omni-research-proposal]] (see [[Research-Proposal-Template]] §3). Produced by a multi-agent survey workflow (5 lanes -> per-lane adversarial verification -> synthesis), run `wf_d76b4901-23c`, 2026-06-26. Every source below was adversarially checked to resolve to a real paper; only `keep=true` claims are archived. Links are real and verifiable.


**Lane summary.** The published literature draws a sharp, falsifiable line that supports H1's GENERATIVE side while complicating the naive "demos activate suppressed skills" story. Classic text-ICL work shows demonstrations mainly supply the label-space, input distribution, and format — input-label correctness is largely irrelevant in small/medium models (Min et al.), but overriding semantic priors via flipped labels is an EMERGENT, scale-gated ability (Wei et al.) and can re-emerge under verbose templates (Yoo et al.); ICL forms a compact, injectable task vector in hidden states (Function/Task Vectors). For audio specifically, the most decisive new finding (ALICE, six LALMs) is that off-the-shelf in-context demonstrations reliably improve FORMAT COMPLIANCE but fail to improve — often degrade — core task accuracy, because models latch onto superficial formatting and lack cross-modal semantic grounding from audio-conditioned examples. Consistent with this, vanilla textless speech LMs have essentially NO ICL until warmup training (Hsu et al.), and genuine few-shot leverage appears only with massive scale as a phase transition (MiMo-Audio) or with RL post-training (FSA-GRPO on Qwen2.5-Omni) — i.e. NOT free in the base model, which directly motivates explicit task-definition + reward-selected conditioning over raw demos. VoxParadox explains the emotion failure mode (audio LLMs "read not listen", following language priors over acoustic truth), speaker identity is near-chance/suppressed and prompting barely helps it, and instruction-steerable embeddings require contrastive TRAINING — supporting H1's VECTOR-side label-insensitivity. One positive generative data point: few-shot enrollment utterance-LABEL pairs do improve SER personalization on a speech-LM, contrasting in-house evidence that few-shot HURTS emotion in the vector class.


**Adversarial verifier assessment.** Strong lane. All 15 cited sources resolve to real, correctly-identified arXiv papers (titles, IDs, and author lists all check out, including the recent/future-dated 2026 ones: ALICE 2603.20433, FSA-GRPO 2606.02615, Pouw 2604.06356, Thebaud 2603.10827, VoxParadox 2605.27772). No fabricated IDs found. The L4 "verbatim" ALICE quote ('in-context demonstrations reliably improve format compliance but fail to improve, and often degrade, the core task performance') matches the abstract word-for-word — a notably clean confirmation. The lane narrative is internally coherent and matches the literature: classic text-ICL (L1-L3, L10) is correctly characterized (label-space/format over label-correctness; scale-gated prior-override; task/function vectors), and the audio results (L4-L9, L11-L15) consistently show that off-the-shelf demos mostly fix format and that genuine few-shot leverage requires warmup/meta-training (L5, L14), RL post-training (L6), massive-scale emergence (L7), or representation bridges (L8) — directly supporting H1's "not free in the base model" framing. Two caveats keep this from a perfect score: (a) several claims lean on specific quantitative figures I could NOT independently confirm via search (L5 IEMOCAP 47.7%, L6 Table-3 deltas, L7 0.7T-token/69.1% figures, L12 17.40->65.20%), though each paper's qualitative core is verified; (b) L11 is the one mild overstatement — the cited Thebaud paper solidly supports "speaker verification weak/near-chance, fixed only by training augmentation," but the appended "gender 92-98%", "ICL/prompting gives modest gains", and "OLA/VITA1.5 near random" details are not confirmed from that single source and appear to blend in uncited material. All claims kept; none rest on a hallucinated source.


---

## Verified claims & sources (15 kept / 15 total)


### L1 · empirical · confidence: high

In classic text ICL, demonstrations work mainly by specifying the label space, the input-text distribution, and the sequence format; replacing gold labels with random labels barely hurts classification/multi-choice accuracy across 12 models incl. GPT-3 — i.e. canonical ICL is largely label-INSENSITIVE in correctness.


- **Sources:** [Rethinking the Role of Demonstrations: What Makes In-Context Learning Work?](https://arxiv.org/abs/2202.12837)

- **Relevance:** H1/H3 baseline for the label-sensitivity question; defines the null model (demos give format+label-space, not label-correctness) that audio results must be tested against.


### L2 · empirical · confidence: high

The label-insensitivity claim is conditional, not universal: ground-truth input-label correspondence DOES matter under more verbose prompt templates and for larger models, so label-sensitivity is a tunable property of template richness and scale rather than absent.


- **Sources:** [Ground-Truth Labels Matter: A Deeper Look into Input-Label Demonstrations](https://arxiv.org/abs/2205.12685)

- **Relevance:** H3 decomposition: instruction richness / template verbosity is a distinct lever from raw demos and modulates whether labels are used — directly informs the explicit-task-definition vs k-shot split.


### L3 · empirical · confidence: high

Overriding pretrained semantic priors with in-context input-label mappings (e.g. flipped or semantically-unrelated labels) is an EMERGENT ability of model scale: small models ignore flipped labels and fall back on priors, while large models can flip their predictions to follow the demonstrations.


- **Sources:** [Larger language models do in-context learning differently](https://arxiv.org/abs/2303.03846)

- **Relevance:** H1 generative side + label-sensitivity: predicts that genuine label-sensitive ICL activation is scale-gated on the generative class — a falsifiable test for whether a given omni model is large enough to be steered by demonstration labels.


### L4 · empirical · confidence: high

DECISIVE audio result: across six Large Audio-Language Models on four audio-understanding tasks, in-context demonstrations reliably improve FORMAT COMPLIANCE but fail to improve — and often DEGRADE — core task performance; models recognize superficial formatting patterns but cannot use cross-modal semantic grounding from audio-conditioned examples.


- **Sources:** [ALICE: A Multifaceted Evaluation Framework of Large Audio-Language Models' In-Context Learning Ability](https://arxiv.org/abs/2603.20433)

- **Relevance:** Central to the OPEN question (H1 generative): off-the-shelf few-shot demos do NOT activate suppressed capabilities in vanilla generative audio LLMs — they mostly fix format. Strongly motivates explicit task-definition + reward-selected conditioning over raw demos.


### L5 · empirical · confidence: high

Vanilla textless speech LMs have essentially NO in-context learning ability (near-random without warmup); a lightweight warmup/demonstration-learning training is required to unlock ICL, after which the model performs UNSEEN classification incl. emotion (IEMOCAP ~47.7% unseen), speech-command, language-ID, and sarcasm.


- **Sources:** [Exploring In-Context Learning of Textless Speech Language Model for Speech Classification Tasks](https://arxiv.org/abs/2310.12477)

- **Relevance:** H1/H2: demonstrates that few-shot activation of suppressed paralinguistic skills (emotion) is achievable on the generative/sequence class but is NOT free in the base model — it needs training to install the demonstration-conditioned format.


### L6 · empirical · confidence: high

RL post-training (FSA-GRPO) on Qwen2.5-Omni installs few-shot leverage and yields large held-out gains: child-ASR WER 23.05->11.23 and 35.65->16.32, MMAU audio understanding +7.0pp (65.8->72.8), MMAR +7.2pp, En->Ja ST +3.72 BLEU — but the paper includes NO shuffled/random-label ablation, so the label-sensitivity of these gains is untested.


- **Sources:** [FSA-GRPO: Teaching Auditory LLMs to Use Few-shot Demonstrations](https://arxiv.org/abs/2606.02615)

- **Relevance:** H1 generative side: confirms generative omni models CAN be made to exploit demonstrations, but the activation here costs weight updates (NOT training-free) — sharpens the contrast with the project's inference-time-only objective and leaves the label-sensitivity question open.


### L7 · empirical · confidence: med

Genuine emergent few-shot ICL in a generative speech LM appears as a sharp PHASE TRANSITION with massive next-token-prediction pretraining (>100M hours): below ~0.7T tokens performance is negligible, then surges; it then activates voice conversion, emotion/rate conversion, denoising, and speech-to-speech translation from paired speech exemplars.


- **Sources:** [MiMo-Audio: Audio Language Models are Few-Shot Learners](https://arxiv.org/abs/2512.23808)

- **Relevance:** H1/H2: capability-presence precondition — ICL only activates skills the model has actually learned at scale; supports treating ICL-activation as a probe of whether a frozen omni model already encodes the capability.


### L8 · empirical · confidence: med

Cross-modal ICL can make a FROZEN text LLM perform few-shot audio tasks without parameter updates by mapping audio into the LLM's own vocabulary via an LLM-driven codec, but this requires a specialized codec/representation bridge and is limited by context length.


- **Sources:** [UniAudio 1.5: Large Language Model-driven Audio Codec is A Few-shot Audio Task Learner](https://arxiv.org/abs/2406.10056)

- **Relevance:** H1 generative side: an existence proof of training-free, inference-time few-shot audio task adaptation on a frozen generative LLM — but mediated by representation engineering, underscoring that naive audio demos alone underperform.


### L9 · empirical · confidence: med

Speech-domain ICL is causally driven by INDUCTION HEADS (ablating top prefix-matching heads sharply degrades it), is modulated by ACOUSTIC features (fast demonstrations hurt, slow slightly help; pitch/intensity barely matter), can be triggered by a SINGLE demonstration, and benefits from lexical overlap but — unlike text — not from semantic similarity.


- **Sources:** [In-Context Learning in Speech Language Models: Analyzing the Role of Acoustic Features, Linguistic Structure, and Induction Heads](https://arxiv.org/abs/2604.06356)

- **Relevance:** Mechanism for H1 generative side and H3: the activation lever in audio ICL is partly acoustic-mimicry/copy (induction heads) rather than abstract label-mapping — predicts demos can leak acoustic style, a confound to control when attributing emotion/speaker lift.


### L10 · theoretical · confidence: high

ICL forms a compact, extractable TASK/FUNCTION VECTOR in the autoregressive model's hidden states that encodes the demonstrated mapping and can be injected to trigger the task zero-shot — giving a mechanistic, steerable handle unique to the generative class.


- **Sources:** [Function Vectors in Large Language Models](https://arxiv.org/abs/2310.15213) · [Task Vectors in In-Context Learning: Emergence, Formation, and Benefits](https://arxiv.org/abs/2501.09240)

- **Relevance:** H1 generative mechanism + Operator-B design: explains why generative omni models are conditioning-steerable (vector class is not) and suggests task-vector injection as an inference-time activation operator.


### L11 · empirical · confidence: med

Fine-grained SPEAKER identity is weak/near-chance in generative speech-aware/omni LLMs and prompting or ICL gives only modest gains; the models reliably capture only COARSE attributes (gender 92-98%), because training objectives prioritize linguistic/paralinguistic content over identity-specific representations.


- **Sources:** [Speaker Verification with Speech-Aware LLMs: Evaluation and Augmentation](https://arxiv.org/abs/2603.10827)

- **Relevance:** H2 capability-presence map: corroborates in-house 'speaker ~chance' finding ON THE GENERATIVE class too, and that ICL/prompting does not activate speaker ID — bounding H1 (some suppressed skills resist ICL even in generators).


### L12 · empirical · confidence: high

Audio LLMs 'read rather than listen': on adversarial paralinguistic items where transcript content contradicts acoustic style, they follow the language-implied (incorrect) answer, e.g. Audio-Flamingo-3 scores only 17.40% on paralinguistic ground truth (raised to 65.20% only after DPO + a Prompt-Conditioned Layer Mixer).


- **Sources:** [Do Audio LLMs Listen or Read? Analyzing and Mitigating Paralinguistic Failures with VoxParadox](https://arxiv.org/abs/2605.27772)

- **Relevance:** H1/H3 failure-mode mechanism: explains WHY few-shot emotion ICL can fail or even hurt on generators — any apparent lift may be linguistic-prior, not acoustic activation; argues for label-/acoustic-controlled ICL ablations and reward selection on acoustic grounding.


### L13 · empirical · confidence: med

Making an embedding model instruction/task-steerable requires CONTRASTIVE TRAINING on instruction-augmented data (INSTRUCTOR) or an answer-generation reformulation (InBedder); frozen vanilla contrastive bi-encoders do not follow task instructions zero-shot, supporting the vector class's label-/instruction-INSENSITIVITY.


- **Sources:** [One Embedder, Any Task: Instruction-Finetuned Text Embeddings (INSTRUCTOR)](https://arxiv.org/abs/2212.09741) · [Answer is All You Need: Instruction-following Text Embedding via Answering the Question (InBedder)](https://arxiv.org/abs/2402.09642)

- **Relevance:** H1 VECTOR side: external evidence that contrastive bi-encoders are not steerable by in-context instructions/labels without weight changes — consistent with in-house omni-embed results (ICL hurts emotion, label-insensitive) and the claimed model-class asymmetry.


### L14 · empirical · confidence: med

Few-shot ICL with target-speaker enrollment utterance-LABEL pairs improves Speech Emotion Recognition personalization on a speech-language model, beating conventional personalization — a positive generative-class data point that emotion ICL can help when demos carry both acoustic context and labels.


- **Sources:** [Few-shot Personalization via In-Context Learning for Speech Emotion Recognition based on Speech-Language Model](https://arxiv.org/abs/2509.08344)

- **Relevance:** H1 asymmetry (direct contrast): emotion ICL HELPS on the generative class here vs in-house evidence that few-shot ICL HURTS emotion (0.217->0.150) and is label-insensitive on the vector class — a concrete falsifiable contrast for the central claim.


### L15 · empirical · confidence: med

Instruction/task-definition prompting alone is necessary but not sufficient for omni models: instruction-tuned speech models handle SEEN tasks but drop sharply on UNSEEN tasks, indicating explicit task definitions activate capability only when the underlying skill was exposed in training.


- **Sources:** [Dynamic-SUPERB: Towards A Dynamic, Collaborative, and Comprehensive Instruction-Tuning Benchmark for Speech](https://arxiv.org/abs/2309.09510)

- **Relevance:** H3 (explicit-task-definition lever) + H2: bounds how far rubric/label-set prompting can activate suppressed skills — works as an activation lever for present-but-dormant skills, not for absent ones; supports pairing task-definition with reward-selected conditioning.
