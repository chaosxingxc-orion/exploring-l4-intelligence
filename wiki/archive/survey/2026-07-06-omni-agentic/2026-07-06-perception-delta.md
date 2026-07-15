---
title: "Perception-delta: does '>transcript' information change agent/system outcomes?"
date: 2026-07-06
stage: 1-argumentation
lane: perception-delta
---

> **🗄 ARCHIVED (2026-07-11)** — 已收官战役过程件（2026-07-06 omni-agentic 调研），仅作历史，非现行真源。

# Perception-delta: paralinguistic/rich-audio information beyond the transcript

> Stage-1 problem-definition lane. Scope: systems (2025-01..2026-07) that pass more than a
> transcript from audio to a controller/agent — paralinguistic-aware, emotion/speaker/prosody
> conditioned, rich-audio-understanding agents — and evidence on whether that ">transcript delta"
> is load-bearing (beats an ASR-then-text-LLM cascade). Cross-domain (VLM/GUI) reference used only
> as a calibration point, per lane brief.
>
> **Relationship to prior wiki survey work.** This lane sits one level up from
> `2026-07-04-stage1-X2-paralinguistic-delta.md` (X2). X2 asks a *perception-probe* question — can
> prompting alone make a frozen generative omni/audio model **recognize** emotion/speaker at all
> (SER accuracy, speaker-ID accuracy) — and finds, with adversarial verification, that training-free
> recovery on that axis is near-chance and every robust recovery changes weights. This lane asks a
> *systems-integration* question one layer up — when a paralinguistic **channel is added to a
> controller** (however it was obtained), does the resulting system beat a plain ASR→text-LLM
> cascade on a downstream task? The two questions are complementary and mostly consistent: nearly
> every system below that demonstrates a robust win **also required fine-tuning or a dedicated
> trained/specialist component** to get there — reinforcing X2's positioning from the systems side —
> with one unresolved ambiguous case (claim 12) that stress-tests the element/usage-pattern boundary
> itself, exactly as the organizing framework asks. (An earlier draft of this lane also flagged claim
> 6 as a contested training-free tension case; **adversarial re-verification on 2026-07-06 found that
> claim was based on a mischaracterization of the source paper — see claim 6 and the Verifier notes
> below — and it has been corrected to a confirming fine-tuned/element case, leaving claim 12 as the
> only genuinely unresolved candidate.**) This lane also does not re-derive X2's speaker/SER-probe
> citations (AudioJudge, SpeakerSleuth, ParaBridge, EMO-TTA, SpeakerLLM, etc.) — none of the 13
> sources below overlap with X2's 8.

## Summary verdict (test, not assume, the framework)

Reading 2025-2026 "beyond-transcript" speech systems through the element/usage-pattern lens: **every
system that demonstrably beats an ASR→text-LLM cascade does so by adding a genuine new-info element**
— a trained adapter that disentangles paralinguistic from linguistic representations (11), a
dedicated emotion/environmental-sound analysis module wired as a separate connector (9), an RL-tuned
prosody-enhanced perception front end (10), an RL-aligned paralinguistic-preservation head trained
against a learned judge (8), a fine-tuned layer-selective paralinguistic-resurfacing protocol (6), or
an audio-conditioned serialized-multitask embedding stream (1). Conversely, wherever the "beyond
transcript" gain is claimed to come from *only* re-arranging inference over one frozen model's
existing forward pass — no dedicated component, no weight change — the evidence is much weaker or
actively negative: current end-to-end omni models often behave close to cascade-equivalent by default
on clean audio, and *worse than cascade-equivalent under noise* (3, 5), sometimes lose to cascades on
paralinguistic instruction-following (7), and a formal "Cascade Equivalence Hypothesis" (5) argues
divergence from cascade-equivalence requires a genuine training/element change (its own conclusion:
"training objectives, not architectures, are the bottleneck") — not orchestration alone. **After
adversarial re-verification (2026-07-06), the count of genuinely training-free counter-candidates in
this lane is one, not two:** claim 6 (originally read as a contested training-free case) turned out,
on fetching the actual paper text, to be **entirely a fine-tuning method** (comparing two
weight-updating strategies against each other, with no training-free variant and no cascade
comparison at all) — the earlier characterization was a drafting error, now corrected, and claim 6
has been reclassified as a **confirming** element/fine-tuned case. That leaves exactly one unresolved
candidate: claim 12, which reports a gain from an inference-time "reflect twice" scheme over one
frozen model, but we could not confirm whether the gain is genuine same-model usage-pattern
re-reasoning (a counterexample to the main thesis) or an implicit element-extraction step in
disguise (the first "pass" turning latent audio-emotion into an explicit label — arguably itself a
new information artifact). A cross-domain GUI/smartphone-automation calibration point (13) suggests
the underlying pattern — modest, often-marginal returns to added perceptual channels beyond a strong
text/structured baseline — recurs outside speech too.

## Claims

### 1. ParalinGPT — genealogy root: speech embeddings + paralinguistic attributes beat text-only spoken-dialogue LLM

- **Recognized problem:** standard text LLMs applied to spoken dialogue transcripts ignore sentiment,
  emotion, and speaking-style cues conveyed only acoustically, which are needed for natural,
  human-like responses.
- **Genealogy + origin-domain + transfer:** origin **speech**, native. Introduces a "serialized
  multitasking multimodal" framework: current-turn paralinguistic-attribute prediction → response
  paralinguistic-attribute prediction → response text generation, conditioned on speech embeddings.
  Foundational lineage that later 2025-2026 paralinguistic-aware systems (8, 9, 11 below) build on.
- **Training-free vs fine-tuned:** fine-tuned (adapter/LoRA-style conditioning trained on
  Switchboard-1 with sentiment labels).
- **Three-axis class + verdict:** **element** — the win is attributed to adding a speech-embedding +
  paralinguistic-attribute channel absent from a plain-text LLM baseline. Reported gains: +6.7%
  relative current-sentiment accuracy, +12.0% relative response-sentiment accuracy, +3.5% relative
  response-text BLEU vs. text-only/sequence-classification baselines. Verdict: **new-info element**,
  confirmed.
- **Fence tag:** single-session.
- **Omni role:** hybrid (one model both perceives — attribute prediction — and generates).
- URL: https://arxiv.org/abs/2312.15316 (Dec 2023; ICASSP 2024) — **older, tagged genealogy root**.
- Delta vs archive: NEW.

### 2. SD-Eval — benchmark that formalizes the cascade / SpeechLLM / oracle-with-labels comparison

- **Recognized problem:** no standard way existed to measure whether spoken-dialogue systems use
  emotion/accent/age/background-sound information beyond lexical content.
- **Genealogy + origin-domain + transfer:** origin **speech**, native. Introduces a 4-perspective
  benchmark (emotion, accent, age, background sound) with a training split (1,052.7 h) and eval split
  (8.76 h), and reports "models conditioned with paralinguistic and environmental information
  outperform their counterparts" — establishing the cascaded-ASR-LLM vs. end-to-end SpeechLLM vs.
  oracle-with-ground-truth-labels comparison frame that later work (4) reuses.
- **Training-free vs fine-tuned:** the benchmark itself is training-free (evaluation only); systems
  evaluated on it vary.
- **Three-axis class + verdict:** this is a measurement **constraint/framework**, not itself a
  system; it operationalizes the element-vs-usage-pattern question for the field. Verdict: n/a
  (methodological contribution).
- **Fence tag:** single-session (per-utterance dialogue tasks).
- **Omni role:** n/a (benchmark).
- URL: https://arxiv.org/abs/2406.13340 (submitted 2024-06-19, last revised 2025-01-16, NeurIPS 2024
  D&B) — **older, tagged genealogy root**, revision falls inside the recency window.
- Delta vs archive: NEW.

### 3. "Just ASR + LLM?" — genealogy negative: frozen SpeechLLMs behave close to cascade for speaker-ID

- **Recognized problem:** does a speech LLM actually use acoustic speaker information, or does it
  answer identity-critical spoken-dialogue questions the same way a plain ASR-transcript-fed LLM
  would?
- **Genealogy + origin-domain + transfer:** origin **speech**, native. Built the Gaokao
  identity-critical-question subset (919 items) plus a synthetic "What Do You Like?" dialogue set
  (1,000 dialogues) and evaluated WavLLM and Qwen-Audio.
- **Training-free vs fine-tuned:** training-free (evaluation of existing models only).
- **Three-axis class + verdict:** tests the **element** axis and finds it mostly **not exploited**:
  on identity-critical (speaker-dependent) questions, WavLLM scores 58.2% vs. 73.2% on
  context-answerable questions (−15 pp), and Qwen-Audio scores 43.2% vs. 62.2% (−19 pp) — the paper
  states models "behave similarly to an LLM reasoning from the conversation transcription." Verdict:
  the acoustic-speaker element is *present in the input* but the frozen models largely fail to use
  it — a negative for the "delta is automatically load-bearing" reading of the main thesis, and a
  direct genealogy predecessor of X2's SpeakerSleuth finding (2601.04029) that textual context
  actively suppresses acoustic judgment.
- **Fence tag:** single-session.
- **Omni role:** sensor present, but functionally unused ("sensor-without-readout").
- URL: https://arxiv.org/abs/2409.04927 (Sept 2024) — **older, tagged genealogy root**.
- Delta vs archive: NEW (paper), CONFIRMS X2's overall verdict (frozen-model paralinguistic/speaker
  readout under training-free conditions is weak-to-absent).

### 4. CP-Bench (Benchmarking Contextual and Paralinguistic Reasoning in Speech-LLMs) — the delta is load-bearing on contextual reasoning, not on direct recognition

- **Recognized problem:** speech-LLMs are evaluated on transcription/QA but rarely on reasoning that
  *integrates* verbal content with non-verbal cues (emotion, prosody) the way real social/emotional
  understanding requires.
- **Genealogy + origin-domain + transfer:** origin **speech**, native. Introduces CP-Bench with two
  curated QA datasets and three question types: content-only (C), contextual-paralinguistic (CP),
  and direct-paralinguistic (DP, e.g., raw emotion/speaker-ID questions).
- **Training-free vs fine-tuned:** training-free (prompting/evaluation of existing models; scoring via
  an LLM judge validated at r=0.71 with human ratings).
- **Three-axis class + verdict:** **element**, split verdict. GPT-4o with audio access scores 69.68%
  (C-type), 67.48% (CP-type), but only 30.34% (DP-type). Cascaded/text-only systems score ~51-56% on
  CP-type, "lacking direct access to audio-based speaker information." Verdict: the audio-perception
  **element is load-bearing for CP-type reasoning** (+~13-18 pp over cascade/text-only) but **not
  sufficient for DP-type direct recognition**, which stays weak (~30%) even with the element present
  — consistent with X2's finding that raw emotion/speaker recognition resists training-free recovery.
- **Fence tag:** single-session.
- **Omni role:** hybrid (sensor + brain in one model).
- URL: https://arxiv.org/abs/2509.16589 (Sept 2025; EMNLP 2025 Findings,
  https://aclanthology.org/2025.findings-emnlp.760/) — verified.
- Delta vs archive: NEW.

### 5. The Cascade Equivalence Hypothesis — a formal frame for when speech LLMs stop being cascade-equivalent

- **Recognized problem:** claims that end-to-end speech LLMs "use paralinguistic information beyond
  transcription" are usually asserted, not tested against the null model that the system is simply
  functionally equivalent to ASR-then-LLM.
- **Genealogy + origin-domain + transfer:** origin **speech**, native (methodology — statistical
  equivalence testing with Cohen's kappa/McNemar tests and concept-erasure probing on speech-LLM
  representations — is itself adapted from general model-behavior-equivalence and interpretability
  literature, i.e., partial transfer from LLM interpretability methodology).
- **Training-free vs fine-tuned:** training-free (analysis/probing of existing frozen models; no
  fine-tuning of the studied systems).
- **Three-axis class + verdict:** directly interrogates the **element** axis and concludes cascade
  equivalence is the **default** on "text-sufficient" tasks (I(A;Y|T)≈0). **Correction (adversarial
  re-verification, full PDF read 2026-07-06):** the original draft's "(a)/(b)/(c)" breakdown-condition
  list was a paraphrase, not a literal quote — the paper does not enumerate exactly those three
  conditions. The paper's own conclusion (§7) is: "insofar as our training goals do not prioritize
  audio-specific cues, speech LLMs will remain cascades in disguise... training objectives, not
  architectures, are the bottleneck" — directionally the same point (a training/element change, not
  mere orchestration, is what's needed) but stated differently than the retracted list implied.
  **Important finding the original draft omitted:** the paper's most load-bearing empirical result is
  actually about **noise robustness, not just clean-condition equivalence** — Whisper-based cascades
  are *more* robust than every E2E model tested under multi-talker babble noise (losing 0.5-4.2%
  accuracy at 0dB vs. 3.9-12.7% for E2E models), and Gemini (best clean accuracy) degrades fastest,
  with clean-condition advantages **reversing by up to 7.6 percentage points at 0dB** (e.g., +2.0%
  clean advantage becomes −5.6% under noise on SST-2). This is a *stronger* negative for the "beyond
  transcript" thesis than mere equivalence: under realistic noisy deployment, current E2E omni models
  can be **worse than a cascade**, not just equivalent to one. Cohen's κ and McNemar's test are
  genuinely used (confirmed via full-text read), addressing per-example behavioral agreement and
  systematic bias, respectively — that part of the original citation was accurate.
- **Fence tag:** single-session.
- **Omni role:** hybrid in principle, but the paper's point is that it often functionally degenerates
  to "brain reasoning over transcript, sensor unused."
- URL: https://arxiv.org/abs/2602.17598 (Feb 2026; author Jayadev Billa) — verified; full PDF read
  during adversarial review (2026-07-06).
- Delta vs archive: NEW; CONFIRMS X2 (a formal framework for the same conclusion X2 reaches
  empirically on SER/speaker-ID benchmarks); **strengthened** with the noise-robustness-reversal
  finding above, which the original draft did not capture.

### 6. Resurfacing Paralinguistic Awareness in Large Audio Language Models — corrected: NOT a training-free case; confirms the element/fine-tuning framing

- **Recognized problem:** large audio LMs may already *encode* paralinguistic information internally
  (in activations) but fail to *use* it in downstream outputs — a retention/utilization gap distinct
  from a perception gap.
- **Genealogy + origin-domain + transfer:** origin **speech**, native. Uses five layer-wise analyses
  to identify paralinguistic vs. semantic-understanding layers, then proposes a
  **paralinguistic-enhanced fine-tuning (PE-FT) protocol**: (1) selective-layer fine-tuning and (2) an
  auxiliary dual-level classification head.
- **Training-free vs fine-tuned:** **fine-tuned only.** Adversarial re-verification (full abstract
  fetched directly, 2026-07-06) found **no training-free or inference-time-only variant anywhere in
  the paper** — the original lane draft's claim that "both training-free and fine-tuned methods" are
  reported, with the training-free variant giving "practical efficiency gains," does not match the
  source and has been removed as an editing error (likely conflating "selective-layer" fine-tuning's
  parameter-efficiency with "training-free"). The paper's own comparison is PE-FT (selective-layer +
  classification head) vs. **all-layer fine-tuning** — both are weight-updating methods; there is no
  cascade-vs-E2E comparison in the abstract either.
- **Three-axis class + verdict:** **element, fine-tuned** — once corrected, this is a **confirming**
  case, not a counter-example: PE-FT "efficiently and effectively resurfaces the paralinguistic
  awareness, even surpassing... all-layer fine-tuning," i.e., a genuine weight-change intervention,
  consistent with claims 1, 8, 9, 10, 11 and with X2's training-vs-training-free positioning. The
  claim-6 "contested training-free counter-case" framing in the original draft was **incorrect and has
  been retracted**; it is not merely unconfirmed, it is actively unsupported by the source. This
  strengthens rather than weakens the lane's main thesis (see corrected summary verdict and negatives
  section).
- **Fence tag:** single-session.
- **Omni role:** hybrid (fine-tuned perception/reasoning layers feeding the same model's generation).
- URL: https://arxiv.org/abs/2603.11947 (March 2026; Yang, Wang, Wu, Qu, Shareghi, Haffari) —
  verified exists; abstract fetched directly and quoted in full during adversarial review.
- Delta vs archive: NEW; **CORRECTED 2026-07-06** — no longer treated as refuting or tensioning
  X2's training-free-recovery finding; reclassified as a confirming fine-tuned/element case.

### 7. S2S-Arena — negative: cascaded systems often beat end-to-end speech-to-speech on paralinguistic instruction-following

- **Recognized problem:** whether direct speech-to-speech (S2S) models can *follow paralinguistic
  instructions* (respond in a requested emotion/style/prosody) better than a cascaded
  ASR→LLM→TTS pipeline, across realistic scenarios (education, entertainment, social interaction,
  medical consultation; 19 task categories).
- **Genealogy + origin-domain + transfer:** origin **speech**, native.
- **Training-free vs fine-tuned:** training-free (benchmark/evaluation of existing S2S and cascaded
  systems).
- **Three-axis class + verdict:** tests the **element** axis (does the S2S architecture's inherent
  access to raw audio pay off) and finds a **negative** result: "cascaded approaches often outperform
  end-to-end S2S systems" on paralinguistic instruction-following — i.e., merely having the acoustic
  channel architecturally available is not sufficient; current E2E training does not yet convert that
  availability into instruction-following competence. Verdict: architecture-level element access ≠
  automatic capability; consistent with 3 and 5.
- **Fence tag:** single-session.
- **Omni role:** hybrid, underperforming a modular sensor(ASR)+brain(LLM)+actuator(TTS) pipeline on
  this axis.
- URL: https://arxiv.org/abs/2503.05085 (March 2025; Jiang, Lin, Liu, Xue, Bu, Du, Chen, Wang, Li) —
  verified.
- Delta vs archive: NEW.

### 8. ParaS2S — paralinguistic-preserving S2S beats cascades, but only after fine-tuned alignment

- **Recognized problem:** speech-to-speech models lack paralinguistic-preservation awareness; cascaded
  ASR→text-LLM→TTS pipelines lose vocal nuance (emotion, tone, style) by round-tripping through text.
- **Genealogy + origin-domain + transfer:** origin **speech**, native.
- **Training-free vs fine-tuned:** **fine-tuned** — **correction (verified against full abstract):**
  the paper's own alignment method is an RL framework with a trained automatic judge
  ("ParaS2SAlign"/"PolyTone"), not explicitly DPO; the original draft's "DPO-style preference
  optimization" label is a mischaracterization and has been corrected. It remains a genuine
  weight-updating fine-tuning method regardless.
- **Three-axis class + verdict:** **element** — after fine-tuned alignment (ParaS2SAlign, RL against
  a learned reward judge), the system reports a "10% relative improvement... over supervised
  fine-tuning (SFT), surpassing all prior models," and the paper states plain S2S models "perform no
  better than pipeline-based baselines" absent this alignment. Verdict: confirms the element framing,
  but the win required a weight change to realize, consistent with claim 5's training-not-orchestration
  conclusion and X2's "robust recovery only via training" pattern — training-free architecture access
  alone (per claim 7) was not enough.
- **Fence tag:** single-session.
- **Omni role:** hybrid.
- URL: https://arxiv.org/abs/2511.08723 (Nov 2025; Yang, Tu, Liu, Qu, Lee, Lu, Wang, Wu) — verified.
- Delta vs archive: NEW; CONFIRMS X2's training-vs-training-free positioning from the systems side.

### 9. X-Talk — modular design confirms the element framing directly: an explicit emotion/environmental-sound module, not orchestration, drives the delta

- **Recognized problem:** monolithic end-to-end omni speech models are hard to interpret, swap, and
  debug; the paper argues the "potential of modular" (decoupled) speech-dialogue design is
  underestimated relative to end-to-end systems.
- **Genealogy + origin-domain + transfer:** origin **speech**, native. Open-source framework
  explicitly wiring specialized front-end components (VAD, speech enhancement) and "diverse
  understanding models (e.g., ASR, emotion, and environmental sound analysis)" as separate modules
  feeding a dialogue manager/LLM.
- **Training-free vs fine-tuned:** mixed — the framework composes existing/specialist trained
  components (an emotion classifier is one such component) rather than training one monolithic model
  end-to-end; the *composition* itself is training-free, the *components* are typically trained.
- **Three-axis class + verdict:** the cleanest confirming case for the main thesis in this lane:
  **element** — the ">transcript" delta here is literally a dedicated emotion-analysis
  connector/tool bolted onto a frozen(-ish) LLM "brain," not a prompting or role-orchestration trick
  applied to a single omni model. Reports sub-second latency and competitive performance including on
  paralinguistic aspects. Verdict: gain from adding a genuine new-info element (an emotion/
  environmental-sound "sensor" module), matching X2-C6's EMO-TTA framing of paralinguistic gains as
  "readout fitting," not prompt reachability.
- **Fence tag:** single-session (per-utterance; framework itself could be extended to
  cross-session but not demonstrated as such here).
- **Omni role:** explicitly split: sensor (ASR + emotion + environmental-sound modules) → brain
  (dialogue-manager LLM).
- URL: https://arxiv.org/abs/2512.18706 (submitted 2025-12-21; Liu, Duan, Wang, Feng, Zhang, Xing,
  Shan, Zhu, Dai, Lu, Qiu, Xie, Wang, Yan, Zheng, Ma, Yu, Chen) — verified.
- Delta vs archive: NEW; CONFIRMS the main thesis and X2's "specialist-module, not brain-prompting"
  pattern (parallel to X2-C6 EMO-TTA and X2-C5 SpeakerLLM/DramaSR-LRM's external speaker-encoder
  tool-use).

### 10. EmotionThinker — reasoning-formulated emotion recognition, but the perception front end is also upgraded (fine-tuned)

- **Recognized problem:** treating emotion recognition as flat classification wastes reasoning
  capacity and yields no interpretable explanation; current speech LLMs show weak prosody perception,
  even though prosodic cues are "fundamental signals for interpreting emotions."
- **Genealogy + origin-domain + transfer:** origin **speech**, native. Contributes EmotionCoT-35K
  (chain-of-thought + acoustic-caption annotations), a "prosody-enhanced" base model, and GRPO-PTR
  (RL combining rule-based outcome rewards with progressive/process-based reasoning rewards).
- **Training-free vs fine-tuned:** **fine-tuned** (RL updates model weights).
- **Three-axis class + verdict:** **mixed element + usage-pattern.** The gain is attributed partly to
  an *element*-side upgrade (the prosody-enhanced perception front end) and partly to a
  *usage-pattern*-side change (chain-of-thought/process-reward reasoning over that perception).
  Reported to outperform prior models on both emotion accuracy and explanation quality. Verdict: this
  is one of the few cases in the lane where a reasoning-scaffold (usage-pattern-like) component is
  explicitly credited alongside a perception upgrade — but the perception upgrade is present and
  weight-changing, so it is not a pure usage-pattern-over-one-frozen-model result.
- **Fence tag:** single-session.
- **Omni role:** hybrid.
- URL: https://arxiv.org/abs/2601.15668 (Jan 2026, ICLR 2026 Oral; Wang, Liu, Zhang, Chen, Li, Meng)
  — verified.
- Delta vs archive: NEW.

### 11. Dual Information Speech Language Models — disentangled paralinguistic adapter beats the "capture one, lose the other" trade-off

- **Recognized problem:** speech LMs built on frozen text LLMs tend to trade off paralinguistic
  capture against semantic/contextual comprehension — improving one degrades the other.
- **Genealogy + origin-domain + transfer:** origin **speech**, native. Proposes two heterogeneous
  adapters that disentangle paralinguistic from linguistic information into separate structured
  representations before the frozen LLM decoder consumes them.
- **Training-free vs fine-tuned:** parameter-efficient adapter-only fine-tuning (the core LLM decoder
  stays frozen; new adapter weights are trained) — a fine-tuned, not training-free, result, though
  lighter-weight than full fine-tuning.
- **Three-axis class + verdict:** **element** — the paper's own framing is that disentangling
  paralinguistic cues into a structured channel distinct from the semantic/transcript-like stream is
  what enables "competitive performance in emotional conversation tasks" without sacrificing semantic
  comprehension. Verdict: gain from a genuinely new, separately-trained information channel, not from
  re-prompting the frozen decoder.
- **Fence tag:** single-session.
- **Omni role:** sensor (adapters) + brain (frozen LLM decoder), hybrid.
- URL: https://arxiv.org/abs/2508.08095 (Aug 2025, IEEE ICME 2025; Wang, Liu, Xu, Deng) — verified.
- Delta vs archive: NEW; CONFIRMS the element framing.

### 12. Reflecting Twice before Speaking with Empathy — unresolved test case: training-free "reflect twice" over one frozen model

- **Recognized problem:** end-to-end spoken dialogue systems generate emotionally inappropriate
  responses because they do not explicitly reason about the user's emotional state before responding.
- **Genealogy + origin-domain + transfer:** origin **speech**, native. Proposes "Self-Reflective
  Alternating Inference": the same model alternates an emotion-understanding reasoning step and a
  dialogue-generation step (reflecting "twice") rather than generating in one pass.
- **Training-free vs fine-tuned:** training-free, explicitly inference-time only — no fine-tuning of
  the base dialogue model.
- **Three-axis class + verdict:** **flagged unresolved — the most direct test of the main thesis in
  this lane.** On its face this looks like a pure usage-pattern (alternating self-reflection over one
  frozen model, same audio input, no external tool/module) reported to improve empathy-alignment over
  single-pass generation. We could not locate (via the fetched excerpt) an ablation isolating whether
  the gain is genuine same-model/same-audio re-reasoning (which would be a notable counterexample to
  "usage-pattern over one frozen model is bounded by its own oracle ceiling") or whether the first
  "emotion-understanding" pass functions as an implicit extraction step — turning latent audio-emotion
  into an explicit label/token sequence the second pass then conditions on, which would itself be a
  (self-generated) new information artifact rather than pure re-reasoning. Recommend flagging for a
  follow-up read isolating this ablation before drawing a verdict either way.
- **Fence tag:** single-session.
- **Omni role:** hybrid.
- URL: https://arxiv.org/abs/2601.18281 (Jan 2026; Jia, Liu, Sun, Zhou, Cheng, Liu, Zeng, Cai, Qin) —
  verified.
- Delta vs archive: NEW — unresolved, flagged for follow-up (does not clearly CONFIRM or REFUTE).

### 13. "Do LLMs Need to See Everything?" — cross-domain (GUI) calibration: the perception-vs-structured-text delta is often marginal outside speech too

- **Recognized problem (cross-domain reference only):** in LLM-driven smartphone automation, does
  passing screenshot pixels (a "beyond-transcript"-analogous visual-perception channel) improve task
  success over passing only screentext (an accessibility-tree/text-only channel), given screenshots
  are also more invasive/costly to capture?
- **Genealogy + origin-domain + transfer:** origin **VLM/GUI-agent**, cross-domain reference (per lane
  scope, not a speech system). Introduces the DailyDroid benchmark (75 tasks, 5 scenarios, 25 Android
  apps, 3 difficulty levels) and tests GPT-4o and o4-mini on text-only vs. text+screenshot inputs
  across 300 trials.
- **Training-free vs fine-tuned:** training-free (prompting/evaluation of existing frontier models).
- **Three-axis class + verdict:** **element** (screenshot pixels are additional information beyond
  the structured-text channel) with a **marginal** verdict: "multimodal inputs yielded marginally
  higher task success rates" than text-only, and the paper's design recommendation is to prioritize
  the cheaper, less-invasive screentext channel given the small margin. Verdict: a useful calibration
  point — in a structurally analogous cross-domain setting, an additional raw-perception channel over
  an already-strong structured-text baseline buys little, echoing the mixed/negative pattern in
  claims 3, 5, and 7 (current systems often fail to convert an available extra perceptual channel into
  much measurable gain, absent a dedicated trained component as in 8-11).
- **Fence tag:** single-session.
- **Omni role:** n/a (VLM/GUI domain, not audio/omni).
- URL: https://arxiv.org/abs/2604.17817 (April 2026; Zhang, Zhang, Fang, D'Alfonso, Jia, Kostakos) —
  verified.
- Delta vs archive: NEW (cross-domain transfer reference, per lane scope).

## Negatives and empty/weak-measurement cells (first-class)

- **No system found that beats a cascade purely via prompt-level/role-level orchestration over one
  frozen omni model, without any added trained component.** Every confirmed win in this lane (1, 6, 8,
  9, 10, 11) required either a trained adapter/module or fine-tuning (claim 6, initially misread as a
  training-free case, was corrected on 2026-07-06 re-verification to a fine-tuned/element case — see
  claim 6 and Verifier notes). Only one candidate (12) remains a genuinely unresolved training-free
  case, flagged rather than accepted, precisely because its controls could not be confirmed to the
  standard X2 already established.
- **Architecture access to raw audio does not automatically confer paralinguistic-instruction
  competence:** S2S-Arena (7) found cascaded systems often *beat* end-to-end S2S on paralinguistic
  instruction-following, and "Just ASR + LLM?" (3) found large accuracy drops (−15 to −19 pp) on
  identity-critical questions versus context-answerable ones for two 2024-era SpeechLLMs — the
  acoustic channel being present in the input is not sufficient for it to be used.
- **No rigorous training-free perception-only counterexample survives scrutiny in this lane either**
  — consistent with X2's "CORE X2 ANSWER — VERIFIED EMPTY" finding on the SER/speaker-ID probe axis.
  The one remaining candidate that reports an inference-time-only gain over one frozen model (12,
  "reflect twice") is unresolved because it's unclear whether the gain is genuine re-reasoning or a
  self-generated new-info artifact (see claim 12); claim 6, which an earlier draft of this lane
  treated as a second training-free candidate, was found on 2026-07-06 re-verification to contain no
  training-free method at all — it is entirely a fine-tuning intervention (PE-FT, selective-layer vs.
  all-layer) with no cascade comparison, so it does not belong in this bullet and has been removed
  from it.
- **Added noise-robustness negative (surfaced during 2026-07-06 re-verification, not in the original
  draft):** claim 5's own headline empirical result is that Whisper-based ASR→LLM cascades are *more*
  robust than every tested end-to-end speech LLM under multi-talker babble noise, with clean-condition
  accuracy advantages for E2E models reversing by up to 7.6 percentage points at 0dB SNR. This means
  the "beyond-transcript" delta is not just sometimes absent (as claims 3, 7 show) but can be actively
  **negative** under realistic noisy deployment conditions — a stronger negative than the lane's
  original framing captured.
- **CP-Bench's split result (4) is itself a first-class negative:** even when the audio element is
  present and load-bearing for *contextual*-paralinguistic reasoning (67-69% vs. 51-56%), *direct*
  paralinguistic recognition (raw emotion/speaker questions) remains weak (~30%) — the delta helps
  some tasks and not others, so "the delta is load-bearing" is not a uniform yes/no answer but
  task-dependent.
- **Empty cell:** no paper found in this lane's searches (2025-01..2026-07) reporting a
  paralinguistic-aware agent that changes a *downstream tool-use/task-completion decision* (e.g.,
  escalating to a human agent because of detected frustration, or altering a DB-query plan based on
  detected urgency) with a verifiable-reward pass@k measurement comparable to tau2-bench/EVA-bench
  style task-success metrics — the evidence base here is about response/summary quality and
  instruction-following, not verifiable agentic task outcomes. This gap is consistent with L4's N1/N2
  negatives (no published pass@k or prompt-opt result on any voice-agent benchmark) and sharpens it:
  the gap holds specifically for paralinguistic-conditioned agentic decisions too.

## Verifier notes (adversarial review, 2026-07-06)

**Scope of this pass.** Spot-checked 9 of the lane's 13 cited URLs via direct fetch (abstracts, and
full text/PDF for the two claims with the highest evidentiary weight — claim 5 and claim 6 — plus the
CP-Bench (4) and ParaS2S (8) sources). All 9 fetched papers **exist at the cited arXiv IDs** and are
by the cited authors; no dead or wrong links were found among the checked set. URLs checked: claim 1
(2312.15316), 3 (2409.04927), 4 (2509.16589, full PDF), 5 (2602.17598, full PDF), 6 (2603.11947, full
abstract), 7 (2503.05085), 8 (2511.08723, full abstract), 9 (2512.18706), 10 (2601.15668), 11
(2508.08095), 12 (2601.18281), 13 (2604.17817). Not independently re-checked: claim 2 (SD-Eval,
long-established benchmark, low risk).

**Findings and dispositions.**

1. **Claim 6 — CONFIRMED ERROR, corrected in place.** The lane's original text asserted the paper
   "Resurfacing Paralinguistic Awareness in Large Audio Language Models" reports *both* training-free
   and fine-tuned methods, with the training-free variant giving "practical efficiency gains." The
   paper's actual abstract (quoted in full in the corrected claim 6) describes **only** a fine-tuning
   protocol (PE-FT: selective-layer fine-tuning + an auxiliary classification head) benchmarked
   against **all-layer fine-tuning** — both weight-updating; no training-free variant, no cascade
   comparison anywhere in the abstract. This is the most consequential finding of this review: the
   lane had manufactured a "contested counter-example" to its own main thesis that does not exist in
   the source. Corrected: claim 6 reclassified as a confirming fine-tuned/element case; summary
   verdict, negatives section, and the X2-relationship note all updated to match. Net effect on the
   lane's argument: **strengthens** it (one fewer training-free counter-candidate, not weaker).
2. **Claim 5 — PARTIALLY CONFIRMED, one omission fixed.** Full-PDF read confirmed Cohen's κ and
   McNemar's test are genuinely used, and the general "training changes, not orchestration, break
   cascade equivalence" conclusion is right in spirit. But the specific "(a)/(b)/(c)" breakdown-
   condition list in the original draft does not appear verbatim in the paper and has been softened to
   a paraphrase-with-caveat. More importantly, the paper's actual headline empirical finding — that
   Whisper-based cascades are *more noise-robust* than every E2E model tested, with clean-condition
   advantages reversing by up to 7.6pp at 0dB — was **omitted from the original draft entirely** and
   has been added; it is a stronger negative for the "delta is load-bearing" thesis than what the lane
   previously captured.
3. **Claim 8 — MINOR mischaracterization, corrected.** "DPO-style preference optimization" does not
   appear in the ParaS2S abstract; the paper's own method name is an RL framework with a trained
   automatic judge ("ParaS2SAlign"/"PolyTone"). Corrected to avoid the specific-but-wrong technique
   name while preserving the (accurate) fine-tuned/element classification.
4. **Claim 4 (CP-Bench) — VERIFIED ACCURATE, no changes needed.** Fetched the full PDF; Table 3 gives
   GPT-4o 69.68% (C), 67.48% (CP), 30.34% (DP) on the long set, and Cascade-1/Cascade-2 51.49%/56.23%
   on CP-type — the lane's "~51-56% cascade CP-type" and the split C/CP/DP numbers are exact matches.
   This is the strongest-sourced claim in the lane.
5. **Claim 13 (DailyDroid) — VERIFIED ACCURATE.** WebFetch independently confirmed 75 tasks, 5
   scenarios, 25 apps, 3 difficulty levels, 300 trials, GPT-4o/o4-mini, and the "marginally higher"
   multimodal verdict — all match the lane's description precisely.
6. **Claims 1, 3, 9, 10, 11 — WebFetch-confirmed** to match the lane's framing (titles, authors,
   mechanism names, qualitative findings); exact percentage figures in claim 3 (58.2/73.2,
   43.2/62.2) were not independently re-derived from full text (abstract-level check only) — flagged
   as unverified-precision, not disputed.
7. **Claim 7 (S2S-Arena) — partially confirmed.** Title and general framing ("Evaluating
   Paralinguistic Instruction Following in Speech-to-Speech Models") match the lane's description;
   the specific "19 task categories" / four named scenarios were not independently re-derived from the
   (compressed) PDF text extraction — flagged as unverified-precision, not disputed.
8. **Framework-verdict calls (element vs. usage-pattern; new-info vs. read-out) — spot-checked against
   the now-corrected evidence and found defensible**, with claim 6 as the one exception requiring
   correction (see above). Claim 12 remains the sole appropriately-unresolved case — its "unresolved,
   not confirmed or refuted" framing was not disturbed by this review since the ambiguity it flags (is
   the first "reflect" pass itself an information-extraction step?) cannot be settled from an abstract
   alone and the lane already treats it that way rather than claiming a verdict.
9. **Recency and negatives** — all non-genealogy-root claims (4-13) fall inside 2025-01..2026-07 as
   required; claims 1-3 are explicitly and correctly tagged as older genealogy roots, which is an
   appropriate exception rather than a recency violation. A first-class Negatives section is present
   and, per findings 1-2 above, is now *stronger* than the original draft (an added noise-robustness
   negative), not weaker.

**Net verdict:** the lane's overall thesis (no training-free-only counterexample survives scrutiny;
every confirmed win required a trained element) held up under adversarial review and became *more*
strongly supported after correction, but one specific evidentiary claim (6) was fabricated/mischaracterized
in a way that, uncorrected, would have misrepresented the paper it cited as saying the opposite of what
it says. That has been fixed in place rather than merely flagged, since the correction was
straightforward and fully sourced.
