---
title: "Lane survey — other 2025+ speech/omni agent benchmarks (field survey, not on our disk)"
date: 2026-07-06
stage: 1-argumentation
lane: eval-benchmarks-field
---

# Eval-benchmarks-field lane — the wider 2025-2026 benchmark landscape

**Scope note:** this lane catalogs benchmarks as first-class objects (competence measured / metric /
human-vs-model gap), complementing sibling lanes that are problem-first
(`2026-07-04-stage1-L4-speech-agentic.md`, P1-P5) or system-first
(`2026-07-06-duplex-realtime.md`). Where a benchmark is already treated in depth elsewhere, this
entry is kept short and cross-references the deeper treatment rather than re-deriving it (per
instructions); the "OTHER" benchmarks the lane brief named that are **not yet covered anywhere else**
in the wiki (Full-Duplex-Bench-v2, MTR-DuplexBench, ADU-Bench, MMAU-Pro, SD-Eval, the
Talker-Reasoner/ConvFill line, SpeechR, MMAR, and the three jailbreak benchmarks) get the full
six-tag treatment.

**Headline cross-cutting finding (own synthesis, not from any single source):** across the ~17
benchmarks below, almost none report a genuine **human** topline next to the model scores — most
report only model-vs-model deltas, or an absolute pass-rate/ASR ceiling well below saturation with no
human anchor. Only MMAU-Pro reports a quantified human score (77.9%) and MTR-DuplexBench reports a
qualitative human > model naturalness gap without a number. This is itself a first-class
empty-measurement-cell: for most of this field, "how far below human" is currently unanswerable from
the published record, which is a different (weaker) evidentiary situation than "how far below a
frozen-model oracle ceiling" — the two are routinely conflated in reporting.

---

## Claims

### 1. Full-Duplex-Bench v1 — turn-taking/backchannel/interruption metric suite
- **Recognized problem:** no standardized, reproducible way to compare full-duplex spoken dialogue
  models on pause handling, backchanneling, turn-taking, and interruption management. Source:
  [arXiv:2503.04721](https://arxiv.org/abs/2503.04721) (Lin et al., March 2025; code
  [github.com/DanielLin94144/Full-Duplex-Bench](https://github.com/DanielLin94144/Full-Duplex-Bench)).
  Already logged as claim #12 in `2026-07-06-duplex-realtime.md`; this entry adds the metric detail
  that lane left unverified: Takeover Rate (TOR) for pause handling and backchannel interruption
  (dGSLM 0.949/0.782, Moshi 1.000/1.000, Freeze-Omni 0.672/0.782), backchannel-timing
  Jensen-Shannon divergence to a human reference corpus, and a GPT-4o content-quality score for
  interruption responses (Moshi 0.765 vs dGSLM 0.201, despite dGSLM's lower TOR).
- **Genealogy:** origin-domain **speech**; evaluation-methodology idea **ported** from the general
  automatic/reproducible LLM-benchmark pattern.
- **Training-free vs fine-tuned:** n/a (benchmark, not a model) — but notable that the systems it
  ranks span both fully-retrained architectures (Moshi, dGSLM) and a frozen-LLM-plus-classifier
  design (Freeze-Omni), i.e. the benchmark itself is agnostic to whether the underlying policy is
  weight-frozen.
- **Class + verdict:** **constraint** — real-time/full-duplex turn-taking is a base-architecture/
  inference-substrate property per the framework's own a-priori tag; the TOR/latency spread tracks
  architecture family (parallel-stream vs cascaded-classifier), not a prompt or role choice on one
  frozen backbone. CONFIRMS the framework.
- **Fence tag:** single-session.
- **Omni role:** hybrid (systems under test both perceive continuous audio and generate speech).
- **Delta:** CONFIRMS (cross-reference to `2026-07-06-duplex-realtime.md` #12; new content here is
  the exact metric figures that lane flagged as unverified).

### 2. Full-Duplex-Bench-v2 — multi-turn duplex evaluation with an automated examiner
- **Recognized problem:** v1 scores isolated single-turn behaviors (one pause, one backchannel);
  real deployments need multi-turn duplex coherence, and manual multi-turn duplex evaluation does not
  scale. Source:
  [arXiv:2510.07838](https://arxiv.org/html/2510.07838v1) (Oct 2025).
- **Genealogy:** origin-domain **speech**; the "automated examiner" (an LLM/judge that drives a
  multi-turn conversation and scores it) is **ported** from the LLM-as-judge / dynamic-examiner
  pattern used in text-agent multi-turn evals.
- **Training-free vs fine-tuned:** n/a (benchmark/eval framework); the examiner itself is a
  prompted, training-free judge model.
- **Class + verdict:** **constraint** (extends the same real-time/full-duplex base-architecture
  property to a multi-turn setting) — but the *examiner* component is a genuine methodological
  instance of **usage-pattern** risk worth flagging: an automated judge scoring a duplex system is
  exactly the "verifier-as-role" fork the project's main thesis warns about (a same-class model
  judging another dialogue, not a verifiable ground-truth check) — no ground-truth DB-state assertion
  is used here, unlike tau-Voice/tau2-bench.
- **Fence tag:** single-session (each conversation is scored end-to-end within one session; no
  cross-session accumulation).
- **Omni role:** hybrid (systems under test); the examiner itself is "brain"-only (text/judgment
  role, does not directly emit the audio output being judged).
- **Delta:** NEW (not found in any other lane file in this wiki as of this survey).

### 3. Full-Duplex-Bench-v3 — tool use for full-duplex voice agents under real-world disfluency
- **Recognized problem:** prior duplex benchmarks (v1/v2) test conversational hygiene but not
  whether a full-duplex agent can *act* (chained API calls) while handling natural human disfluency
  (fillers, pauses, hesitations, false starts, self-corrections). Source:
  [arXiv:2604.04847](https://arxiv.org/abs/2604.04847) (April 2026; demo
  [daniellin94144.github.io/FDB-v3-demo](https://daniellin94144.github.io/FDB-v3-demo/)). Already
  named in `2026-07-04-stage1-L4-speech-agentic.md` P1/P3 and `2026-07-06-duplex-realtime.md`; this
  entry adds the full six-model result table.
- **Metric:** Pass@1 (task completion via chained tool calls), latency, turn-take rate, interruption
  avoidance.
- **Models evaluated & scores:** GPT-Realtime leads Pass@1 (0.600) and interruption avoidance
  (13.5%); Gemini Live 3.1 has the fastest latency (4.25s) but the lowest turn-take rate (78.0%);
  Gemini Live 2.5, Grok, and Ultravox v0.7 were also evaluated; a Cascaded baseline
  (Whisper->GPT-4o->TTS) reaches a perfect turn-take rate but the highest latency (10.12s). No human
  baseline reported.
- **Genealogy:** origin-domain **speech**; the chained-tool-call task design is **ported** from
  text-agent tool-use benchmarks (tau-bench lineage).
- **Training-free vs fine-tuned:** the top scorer (GPT-Realtime) is a frozen, API-only commercial
  endpoint — its Pass@1 lead is read out from an already-frozen model rather than any visible
  fine-tuning disclosed in the benchmark paper.
- **Class + verdict:** **element** — the axis under test is genuinely the tool/connector call itself
  (a new-info element), gated by real-time/disfluency robustness (a constraint); best Pass@1 is still
  only 0.600, showing the tool-connector element alone does not cross the capability boundary without
  matching perception/reasoning fidelity from the base model.
- **Fence tag:** single-session.
- **Omni role:** hybrid.
- **Delta:** CONFIRMS (cross-reference to L4 P1/P3 and duplex-realtime; adds the full per-model score
  table).

### 4. MTR-DuplexBench — multi-round conversation evaluation for full-duplex speech LMs
- **Recognized problem:** existing full-duplex evaluations (including FDB v1/v2) under-cover
  **multi-round** conversations specifically — sustained coherence, turn-taking, and voice-quality
  degradation compounding across many rounds rather than one exchange. Source:
  [arXiv:2511.10262](https://arxiv.org/pdf/2511.10262) (Nov 2025).
- **Metric:** a five-dimension suite — speech-recognition quality per turn, response relevance/
  contextual consistency, turn-taking behavior, dialogue coherence across turns, and voice
  quality/naturalness of synthesized output.
- **Models evaluated:** Moshi, NTPP, SpiritLM, GLM-4-Voice, Mini-Omni, LLaMA-Omni, Qwen3-Omni, plus
  additional proprietary/open baselines.
- **Human-vs-model gap:** qualitative only — "human evaluators demonstrate substantially higher
  turn-taking naturalness and contextual awareness than current models," with no single numeric gap
  reported in the abstract (first-class empty cell: the magnitude of the human/model gap is
  unquantified here).
- **Key finding:** multi-turn performance degrades progressively — speech-recognition accuracy,
  turn-taking appropriateness, and context retention all decline as conversations extend, i.e. the
  failure mode is compounding, not a fixed one-shot deficit.
- **Genealogy:** origin-domain **speech**; multi-round degradation methodology **ported** from
  long-context/multi-turn text-LLM evaluation practice.
- **Training-free vs fine-tuned:** n/a (benchmark); systems tested span both trained-from-scratch
  duplex architectures (Moshi, SpiritLM) and frozen-backbone-plus-adapter designs.
- **Class + verdict:** **constraint** (real-time/full-duplex substrate property, extended across
  rounds) — degradation compounds with conversation length regardless of prompting choices,
  consistent with a base-architecture ceiling rather than a fixable usage pattern.
- **Fence tag:** single-session (each multi-round conversation is one session; no cross-session
  memory claim is made or tested).
- **Omni role:** hybrid.
- **Delta:** NEW.

### 5. EchoChain — full-duplex state-update reasoning under interruption
- **Recognized problem:** voice assistants must revise task state when interrupted mid-response;
  existing benchmarks (including FDB v1/v2) evaluate turn-based interaction and miss this failure
  mode. Source: [arXiv:2604.16456](https://arxiv.org/abs/2604.16456) (April 2026). Already named
  (with the same 47.5%/40.2% figures) in `2026-07-04-stage1-L4-speech-agentic.md` P3; this entry adds
  the three-axis classification that lane does not perform, plus the genealogy/fence/omni-role tags.
- **Metric:** pass rate on interrupted conversations (200 scenario-driven conversations, standardized
  interruption injection point).
- **Models evaluated & scores:** GPT-realtime-2025-08-28 (45.0% mean pass rate) and Grok Voice Agent
  (48.5% mean pass rate) are the top two of the four models tested (Table 1; also includes Amazon Nova
  Sonic 2 at 26.5% and Gemini Live-2.5-flash-native-audio at 16.5%); none exceeds 50%. A paired
  half-duplex control (same scenarios, no interruption) shows total failures drop by 40.2% relative to
  interrupted runs, isolating interruption-handling itself (not raw task difficulty) as the dominant
  failure driver. **Verifier correction:** the previously-stated 44.0%/47.5% figures (also propagated
  into `2026-07-04-stage1-L4-speech-agentic.md` P3) do not match the paper's Table 1, which reports
  45.0%/48.5%; corrected here from a direct fetch of the source.
- **Failure taxonomy:** contextual inertia, interruption amnesia, objective displacement — three
  recurring patterns, not one.
- **Genealogy:** origin-domain **speech**; the controlled-injection methodology (standardized
  interruption point, paired control condition) is **ported** from the ablation/controlled-experiment
  design pattern common in NLP/robustness evaluation more broadly.
- **Training-free vs fine-tuned:** the two leaders are frozen commercial API endpoints (GPT-realtime,
  Grok Voice Agent) — the benchmark is measuring frozen-model behavior directly, with no fine-tuning
  step disclosed.
- **Class + verdict:** **constraint** — state-update-under-interruption is closest to the
  real-time/full-duplex base-architecture property (the 40.2% paired-control delta shows the deficit
  is specifically interruption-timing, an inference-substrate issue, not a general reasoning
  shortfall) — CONFIRMS the framework's a-priori tag, and CONFIRMS L4's P3 framing independently via
  a different classification lens (element/usage-pattern/constraint rather than problem-ladder).
- **Fence tag:** single-session (interruption happens within one ongoing exchange; no cross-session
  accumulation).
- **Omni role:** hybrid.
- **Delta:** CONFIRMS (cross-reference L4 P3; NEW content is the six-tag/three-axis classification).

### 6. ADU-Bench — open-ended audio dialogue understanding
- **Recognized problem:** most LALM evaluation uses closed-form (multiple-choice/transcription-style)
  tasks; open-ended, free-form spoken-dialogue responses (including ambiguity from intonation, pause
  position, and homophones) were not systematically benchmarked. Source:
  [arXiv:2412.05167](https://arxiv.org/abs/2412.05167) (ACL 2025; code
  [github.com/KuofengGao/ADU-Bench](https://github.com/KuofengGao/ADU-Bench)). Note on recency: the
  arXiv posting is Dec 2024 (just outside the 2025-01 window), but formal publication is ACL 2025 and
  it remains an actively cited 2025-era open-ended-dialogue reference; included with this caveat
  flagged rather than silently in-window.
- **Dataset:** 20,715 open-ended audio dialogues (8,000+ real recordings + synthetic) across 3
  scenarios, 12 skills, 9 languages, and 4 ambiguity categories (e.g. "Really!?" said with different
  intonations implying different intents).
- **Models evaluated:** 16 LALMs (BLSP, SALMONN, Qwen-Audio-Chat, and others, with GPT-4o as a
  reference point) — **verifier correction:** the abstract states "extensive experiments on 16 LALMs"
  verbatim; the figure of 13 previously in this entry does not match and has been corrected from a
  direct fetch of the source. No exact accuracy figures are reported in the available abstract/README —
  only qualitative failure categories (empty-measurement-cell: no single leaderboard number to cite).
- **Key finding:** LALMs struggle with mathematical symbols/formulas, roleplay/human-behavior
  understanding, multilingual comprehension, and disambiguating audio dialogues that carry different
  intent via the same literal wording (intonation/pause/homophone cues) — a perception-fidelity
  failure that a text-only LLM given the transcript could not, in principle, ever recover (the
  paralinguistic cue is not in the transcript).
- **Genealogy:** origin-domain **speech**; open-ended free-response grading methodology **ported**
  from open-ended text-LLM-as-judge evaluation.
- **Training-free vs fine-tuned:** n/a (benchmark); the 13 LALMs tested are evaluated as-shipped
  (training-free from the benchmark's point of view).
- **Class + verdict:** **constraint** (perception fidelity — the ambiguity-handling failure mode is
  explicitly about audio-only information the model must perceive correctly, not about
  orchestration).
- **Fence tag:** single-session.
- **Omni role:** hybrid (perceives audio, generates open-ended dialogue response in one pass).
- **Delta:** NEW.

### 7. MMAU-Pro — holistic benchmark for audio general intelligence
- **Recognized problem:** prior audio-understanding benchmarks (including the original MMAU) under-
  cover the full breadth of "auditory general intelligence" — speech, environmental sound, and music
  together, plus multi-audio reasoning, long-form audio (up to 10 min), spatial audio, and
  instruction-following. Source:
  [arXiv:2508.13992](https://arxiv.org/abs/2508.13992) (Aug 2025; AAAI paper
  [ojs.aaai.org/index.php/AAAI/article/view/39430](https://ojs.aaai.org/index.php/AAAI/article/view/39430)).
- **Metric:** accuracy (multiple-choice + open-ended), 5,305 expert-annotated instances across 49
  auditory skills.
- **Human-vs-model gap (quantified — rare in this field):** human baseline 77.9%; best model
  (Gemini-2.5-Flash) 59.2%; Gemini-2.0-Flash 55.7%; GPT-4o-Audio 52.5% — an **18.7 percentage-point**
  human-model gap at the top of the leaderboard, with 22 models evaluated total (LALMs, "Large Audio
  Reasoning Models," omni models, and cascaded systems) and several categories at
  "approaching random performance."
- **Genealogy:** origin-domain **speech** (with strong sound/music cross-domain content); the
  expert-annotated multi-skill taxonomy methodology is **ported** from broad multimodal-intelligence
  benchmarks in the VLM line (e.g. MMBench-style skill decomposition).
- **Training-free vs fine-tuned:** n/a (benchmark); "Large Audio Reasoning Models" are evaluated as a
  separate category, implying some use test-time reasoning/chain-of-thought (training-free
  inference-time compute) rather than a fine-tuning difference — a data point the project's
  usage-pattern-vs-element question could probe further (not resolved by the abstract alone).
- **Class + verdict:** **constraint** (perception/reasoning fidelity, a model-quality property) —
  the 18.7pp gap to human and the "random-performance" categories indicate the ceiling is bounded by
  the base model's auditory competence, not by how it is prompted or orchestrated.
- **Fence tag:** single-session.
- **Omni role:** hybrid (omni/LALM systems both perceive and answer); cascaded systems in the mix
  separate sensor (ASR/audio-tagging front end) from brain (text LLM).
- **Delta:** NEW.

### 8. SD-Eval — spoken dialogue understanding beyond words (paralinguistic/environmental)
- **Recognized problem:** spoken dialogue carries content, paralinguistic (emotion, accent, age), and
  environmental (background sound) information jointly; most spoken-dialogue evaluation scores only
  content correctness and ignores whether a system actually used the non-lexical signal. Source:
  [arXiv:2406.13340](https://arxiv.org/abs/2406.13340) (NeurIPS 2024 Datasets & Benchmarks Track; code
  [github.com/amphionspace/SD-Eval](https://github.com/amphionspace/SD-Eval)). Genealogy-root note:
  arXiv posting June 2024, outside the 2025-01 window — included as the still-cited foundational
  paralinguistic-eval reference that later 2025+ work (e.g. SpeechR's acoustic-feature track, MMAU-
  Pro's skill taxonomy) builds on; tagged as a root, not a current-window primary claim.
- **Dataset:** 7,303 utterances / 8.76 hours, aggregated from 8 public datasets across 4 perspectives
  (emotion, accent, age, background sound).
- **Metric:** objective + subjective (human) evaluation of generated responses, plus an LLM-based
  metric shown to correlate more with human judgment than traditional (e.g. BLEU-style) metrics.
- **Key finding:** models explicitly conditioned on paralinguistic/environmental information
  outperform unconditioned counterparts on both objective and subjective evaluation — i.e., giving
  the model the paralinguistic **element** (as extra conditioning input) measurably helps, though the
  paper does not test whether this could be obtained purely by better decoding/prompting of an
  already-paralinguistic-aware frozen model versus requiring architectural conditioning.
- **Genealogy:** origin-domain **speech**; native (not ported).
- **Training-free vs fine-tuned:** the conditioned-vs-unconditioned comparison in the source paper
  is a training-time architectural difference, not a training-free intervention — this benchmark's
  own headline finding is therefore **not** evidence for a frozen-model-compatible lever.
- **Class + verdict:** **constraint** (perception fidelity of paralinguistic/environmental signal).
- **Fence tag:** single-session.
- **Omni role:** sensor-leaning-hybrid (the paralinguistic/environmental cues are inputs the model
  must sense correctly before generating a response).
- **Delta:** NEW (genealogy root, tagged as such).

### 9. Talker-Reasoner architecture and its 2025 speech-domain evaluation (ConvFill / "Thinking While Speaking")
- **Recognized problem (genealogy root, text/LLM, Oct 2024):** a single LLM cannot be both
  fast/interactive and slow/deliberate at once; the Talker-Reasoner architecture splits a
  conversational agent into a fast "Talker" (System-1-like, fluid interaction) and a slower
  "Reasoner" (System-2-like, planning/verification) that can intervene in complex cases. Source:
  [arXiv:2410.08328](https://arxiv.org/abs/2410.08328) (Christakopoulou et al., Oct 2024, Google
  DeepMind; validated qualitatively on a sleep-coaching use case, not a public leaderboard
  benchmark). Origin-domain **LLM**, text-native.
- **2025+ speech-domain instantiation:** "Thinking While Speaking: Inference-Time Knowledge Transfer
  for Responsive and Intelligent Conversational Voice Agents" introduces the **ConvFill** dataset to
  evaluate conversational-infill capability for voice agents — generating coherent, contextually
  appropriate continuations mid-speech while a "reasoner" component contributes knowledge in real
  time. Source: [arXiv:2511.07397](https://arxiv.org/pdf/2511.07397) (Nov 2025).
- **Metric:** BERTScore (semantic similarity), a DeBERTa-based entailment classifier (logical
  coherence), plus human evaluation on naturalness/clarity/fluency.
- **Models evaluated (verifier-corrected):** a direct fetch of the source shows these are **two
  disjoint role-specific pools, not one interchangeable backbone list** as the entry previously implied.
  Reasoner pool (3 frontier models providing knowledge transfer): Claude Opus 4.7, GPT-5.5, Gemini 3.1
  Pro. Talker pool (7 small models, 135M-1.7B params, separately fine-tuned for the role, deployed
  INT8/MLX on Apple M2): Gemma 3 270M, Gemma 3 1B, Qwen3 0.6B, SmolLM2 135M/360M/1.7B, Llama 3.2 1B.
  No model appears in both pools.
- **Genealogy:** origin-domain **LLM** (text, Talker-Reasoner architecture); transfer status
  **ported** to speech via ConvFill.
- **Training-free vs fine-tuned:** **verifier correction — this is resolved, and resolved against the
  prior framing.** The prior version of this entry stated the same-weights-vs-different-model question
  was unresolved and flagged ConvFill as the sharpest available test of the thesis's ambiguity fork.
  Direct inspection of the source shows the opposite: Talker and Reasoner are explicitly **different,
  disjoint models** (frontier proprietary Reasoners vs small separately-fine-tuned Talkers, per the
  pools above) — not one frozen backbone wearing two roles. The Talker models are also fine-tuned for
  the role (a training-time step), so the pattern as published is not purely a training-free
  orchestration layer either.
- **Class + verdict:** **usage-pattern at the architectural-idea level** (the Talker/Reasoner
  split-and-route design is definitionally an orchestration pattern) — but **not** a valid instance of
  the project's "same frozen weights, different role" ambiguity fork, since the source confirms
  different models occupy the two roles. This benchmark/paper should be read as a genuine multi-model
  system (closer to a distillation-plus-knowledge-transfer pipeline than a same-model role split) and
  therefore does **not** serve as a test case for the thesis's single-frozen-model prediction in either
  direction — it is simply off-target for that specific question, not an open/unresolved instance of it.
- **Fence tag:** single-session.
- **Omni role:** n/a for the text-domain original (LLM only); hybrid for the ConvFill speech
  instantiation (Talker produces speech while sensing ongoing context).
- **Delta:** NEW.

### 10. SpeechR — benchmark for speech reasoning in large audio-language models
- **Recognized problem:** transcription accuracy (WER) does not indicate whether a model can reason
  over what it heard; no benchmark isolated factual, procedural, and normative reasoning specifically
  in the spoken (not just audio-perception) modality. Source:
  [arXiv:2508.02018](https://arxiv.org/html/2508.02018v1) (Aug 2025).
- **Reasoning types:** factual (retrieval/commonsense), procedural (multi-step deterministic
  inference), normative (moral/social judgment, more subjective).
- **Metric & versions:** multiple-choice (accuracy), generative (LLM-as-judge 0-5 scale on
  correctness/relevance/coherence), acoustic-feature (classification accuracy under prosodic stress
  and emotional variation).
- **Models evaluated & scores (multiple-choice, 11 models total):** Gemini-1.5-Pro 67.68%,
  GPT-4o-audio-preview 58.91%, LLaMA-Omni 39.28%, Qwen2-Audio-Instruct 33.90%, Qwen2-Audio-7B 12.83%
  — a roughly 55-point spread from smallest to largest/most-capable model, all with no human topline
  reported.
- **Human involvement:** limited to naturalness validation of synthesized audio (4.8/5 from 10 native
  English speakers), not an accuracy topline — another empty-measurement-cell for the "human-vs-model
  gap" the lane brief asks about.
- **Key finding:** high transcription accuracy does not translate into strong reasoning; models show
  a "marked performance drop" converting equivalent text tasks to speech, and struggle specifically
  with normative/pragmatic reasoning even when factual reasoning is strong.
- **Genealogy:** origin-domain **speech**; the factual/procedural/normative reasoning-type taxonomy
  is **ported** from text-LLM reasoning-benchmark design (e.g. commonsense/procedural/moral-reasoning
  splits used in text NLP).
- **Training-free vs fine-tuned:** n/a (benchmark); models tested as-shipped.
- **Class + verdict:** **constraint** (perception+reasoning fidelity) — the text-to-speech
  reasoning drop for the *same* underlying capability class shows the bottleneck is the audio
  modality's effect on a fixed model's own reasoning, not an orchestration choice.
- **Fence tag:** single-session.
- **Omni role:** hybrid.
- **Delta:** NEW.

### 11. MMAR — challenging benchmark for deep reasoning in speech, audio, music, and their mix
- **Recognized problem:** audio-reasoning benchmarks tend to isolate speech, sound, or music; real
  audio is frequently a mix, and reasoning about it requires layered inference (raw signal ->
  perception -> semantics -> cultural context) rather than single-hop QA. Source:
  [arXiv:2505.13032](https://arxiv.org/abs/2505.13032) (May 2025; NeurIPS 2025 accepted).
- **Dataset:** 1,000 curated audio-question-answer triplets from real-world internet videos,
  hierarchically labeled across four reasoning layers (Signal, Perception, Semantic, Cultural), each
  with a chain-of-thought rationale annotation.
- **Models evaluated:** ~30 audio-capable models spanning LALMs, "Large Audio Reasoning Models," and
  others.
- **Key finding:** the benchmark is "highly challenging," with open-source LALMs performing
  "negligibly better than random guessing" and a "notable performance gap between open-source and
  closed-source models" — but no exact best-model accuracy figure or human baseline was resolvable
  from the sources checked (another empty-measurement-cell; flagged rather than invented).
- **Genealogy:** origin-domain **speech** (cross-domain: sound + music + speech mixed); the
  layered Signal-Perception-Semantic-Cultural reasoning hierarchy is **ported** from cognitive-
  science-inspired perception-to-cognition stacks used more broadly in multimodal (VLM) reasoning
  benchmark design.
- **Training-free vs fine-tuned:** n/a (benchmark); "Large Audio Reasoning Models" category again
  implies some models under test use training-free inference-time reasoning (chain-of-thought/
  extended thinking) rather than fine-tuning differences.
- **Class + verdict:** **constraint** (perception/reasoning fidelity across a signal-to-culture
  hierarchy) — near-random open-source performance indicates a base-model ceiling problem, not a
  fixable usage pattern.
- **Fence tag:** single-session.
- **Omni role:** hybrid.
- **Delta:** NEW.

### 12. AJailBench / "Audio Jailbreak" — open comprehensive benchmark for jailbreaking LALMs
- **Recognized problem:** LALM safety alignment developed for text does not obviously transfer to
  audio input, and no open, comprehensive benchmark existed to measure how easily audio jailbreaks
  bypass it. Source: [arXiv:2505.15406](https://arxiv.org/abs/2505.15406) (May 2025; code
  [github.com/mbzuai-nlp/AudioJailbreak](https://github.com/mbzuai-nlp/AudioJailbreak)).
- **Dataset:** AJailBench-Base — 1,495 adversarial audio prompts across 10 policy-violating
  categories, converted from textual jailbreaks via TTS; AJailBench-APT extends this with an Audio
  Perturbation Toolkit (time/frequency/amplitude-domain perturbations that preserve semantic meaning).
- **Metric:** attack success rate (ASR) against tested LALMs' safety refusal behavior.
- **Key finding:** "none [of the evaluated LAMs] exhibit consistent robustness across attacks";
  small, semantically-preserving perturbations in time/frequency/amplitude are sufficient to degrade
  safety performance meaningfully — exact per-model ASR figures were not resolvable from the sources
  checked here (flagged, not invented).
- **Genealogy:** origin-domain **speech** for the audio-perturbation attack surface; the underlying
  jailbreak-prompt corpus is **ported** from text-LLM jailbreak-prompt datasets (via TTS conversion).
- **Training-free vs fine-tuned:** the attacks themselves are training-free (input perturbation, no
  weight change to the target model); this benchmark measures a frozen model's vulnerability
  surface directly.
- **Class + verdict:** **constraint** (alignment/safety — explicitly named as cross-cutting in the
  framework). Directly relevant to the thesis: safety here is being probed as a property of the
  frozen model's own weights responding to varied inputs, not defeated or defended by an
  orchestration change — i.e., the attack is itself input/element-level (a new adversarial audio
  element), and the paper does not report a usage-pattern-only defense (e.g. a "be careful" system
  prompt) succeeding.
- **Fence tag:** single-session.
- **Omni role:** hybrid (the LALM perceives the adversarial audio and generates the — potentially
  unsafe — response in one pass).
- **Delta:** NEW.

### 13. JALMBench — benchmarking jailbreak vulnerabilities in audio language models
- **Recognized problem:** LALM safety research lacked a unified evaluation framework and
  large-scale benchmark comparing attacks *and* defenses across many models and modalities (text-
  input, text-transferred-to-audio, and audio-originated attacks) on equal footing. Source:
  [arXiv:2505.17568](https://www.arxiv.org/pdf/2505.17568) (May 2025; ICLR 2026 accepted,
  [openreview.net/forum?id=DJkQ236C8B](https://openreview.net/forum?id=DJkQ236C8B)).
- **Dataset:** 11,316 text samples + 245,355 audio samples (>1,000 hours); 12 mainstream LALMs
  tested; 8 attack methods (4 text-transferred, 4 audio-originated); 5 defenses.
- **Metric & results (attack success rate, ASR):** non-adversarial harmful queries: audio-modality
  ASR 21.5% vs text-modality 17.0% (audio is the *easier* attack surface even without adversarial
  crafting). For crafted jailbreaks: text-input and text-transferred attacks average 49.7%/37.5% ASR
  (best single attack 95.2%/93.3%); audio-originated attacks average 72.9% ASR, with the strongest
  attack (AdvWave) reaching **96.2%** ASR.
- **Key finding, directly thesis-relevant:** "existing general-purpose moderation methods only
  slightly improve security" — i.e., a moderation-as-usage-pattern intervention (a guardrail/
  moderation prompt or filter layered on the same frozen model) buys little robustness against
  audio-originated attacks; text-based safety alignment "can partially transfer" to audio but
  "interleaved audio-text strategies enable more robust cross-modal generalization" — suggesting the
  gains that *do* exist come from a genuinely new training/architectural element (interleaving), not
  from a role/prompt usage pattern over the unchanged model.
- **Genealogy:** origin-domain **speech** (audio-originated attacks); text-transferred attacks are
  **ported** directly from text-LLM jailbreak literature.
- **Training-free vs fine-tuned:** attacks are training-free (input-level); of the 5 defenses tested,
  "general-purpose moderation" is training-free/usage-pattern-like and found weak, while
  cross-modal-interleaving defenses look training-time/architectural — the paper's own contrast is a
  clean empirical instance of usage-pattern (moderation prompt) underperforming a genuine element/
  architecture change (interleaved training), supporting the thesis's prediction.
- **Class + verdict:** **constraint** (alignment/safety, cross-cutting) with an explicit internal
  usage-pattern-vs-element contrast (moderation prompting = weak usage-pattern fix; interleaved
  audio-text training = stronger element-level fix) — CONFIRMS the thesis's prediction that a
  role/prompt-level intervention over one frozen model underperforms an actual new element.
- **Fence tag:** single-session.
- **Omni role:** hybrid.
- **Delta:** NEW.

### 14. Jailbreak-AudioBench — in-depth evaluation and analysis of jailbreak threats for LALMs
- **Recognized problem:** prior audio-jailbreak work explored isolated attack types; a systematic
  toolbox + dataset + benchmark combining diverse **hidden-semantic audio edits** (emphasis, speed,
  intonation, tone, background noise, celebrity-voice accent, emotion) with explicit/implicit
  jailbreak prompts was missing. Source:
  [arXiv:2501.13772](https://arxiv.org/abs/2501.13772) (Jan 2025; code
  [github.com/Researchtopic/Code-Jailbreak-AudioBench](https://github.com/Researchtopic/Code-Jailbreak-AudioBench)).
- **Components:** a Toolbox (text-to-audio conversion + hidden-semantic audio editing), a curated
  Dataset (explicit/implicit jailbreak audio, original + edited forms), and a Benchmark evaluating
  multiple SOTA LALMs — described by the authors as, at time of writing, the most comprehensive
  audio-modality jailbreak benchmark to date (a claim later superseded in scope by JALMBench and
  AJailBench, both larger).
- **Metric:** ASR-style ranking of edited-audio jailbreak prompts against tested LALMs (exact
  aggregate figures not resolved from the sources checked here — empty-measurement-cell, flagged).
- **Genealogy:** origin-domain **speech** (audio-editing attack surface: prosody/background/voice
  conversion); jailbreak-prompt corpus **ported** from text jailbreak literature.
- **Training-free vs fine-tuned:** training-free (input perturbation), same framing as AJailBench/
  JALMBench.
- **Class + verdict:** **constraint** (alignment/safety, cross-cutting) — same reading as the other
  two jailbreak benchmarks: the vulnerability is a property of the frozen model's own audio-safety
  alignment, exposed by input-level (element) manipulation.
- **Fence tag:** single-session.
- **Omni role:** hybrid.
- **Delta:** NEW.

### 15. VoiceAgentBench — are voice assistants ready for agentic tasks?
- **Recognized problem:** agentic voice-assistant evaluation (tool selection, multi-tool
  orchestration, adversarial/safety robustness) was fragmented and under-covered relative to
  text-agent tool-use benchmarks; also under-covered for non-English (Indic) languages. Source:
  [arXiv:2510.07978](https://arxiv.org/html/2510.07978v3) (Oct 2025). Already named in
  `2026-07-04-stage1-L4-speech-agentic.md` P4; kept short here as a cross-reference, with the
  ASR-LLM-vs-end-to-end split emphasized for this lane's element/constraint framing.
- **Dataset:** 6,000+ synthetic spoken queries: single-tool invocation, multi-tool workflows,
  multi-turn dialogue, and safety evaluations, in English + 6 Indic languages, with a
  speaker-embedding-based TTS voice-conversion sampling strategy for acoustic diversity.
- **Metric:** parameter-filling accuracy of tool invocations (tool name + argument correctness).
- **Scores & gap:** ASR-LLM cascade pipelines reach up to 60.6% average parameter-filling accuracy on
  English; end-to-end SpeechLMs score lower with sharper degradation on Indic languages. No human
  baseline reported.
- **Genealogy:** origin-domain **speech**; the tool-invocation-accuracy task design is **ported**
  from text-LLM function-calling benchmarks.
- **Training-free vs fine-tuned:** n/a (benchmark); systems evaluated as-shipped.
- **Class + verdict:** **element** (tool/connector fidelity is the direct object of measurement) —
  but the ASR-LLM-cascade-beats-end-to-end-SpeechLM finding is a useful negative for a naive
  "just add the tool element" story: routing the *same* new tool element through a
  perception-then-reasoning cascade (sensor separate from brain) outperforms giving a single
  end-to-end model the tool directly, implying the bottleneck is the frozen end-to-end model's own
  audio-to-intent grounding, not the tool element's availability per se.
- **Fence tag:** single-session.
- **Omni role:** for ASR-LLM cascades, sensor (ASR) + brain (text LLM) separated; for end-to-end
  SpeechLMs, hybrid.
- **Delta:** CONFIRMS (cross-reference L4 P4).

### 16. Audio2Tool — speak, call, act: a dataset for benchmarking speech tool use
- **Recognized problem:** speech-to-tool-call mapping (bypassing a cascaded ASR-LLM pipeline)
  had not been benchmarked under compositional, multi-intent, and multi-turn realistic conditions at
  scale. Source: [arXiv:2604.22821](https://arxiv.org/html/2604.22821v1) (April 2026). Already named
  in `2026-07-04-stage1-L4-speech-agentic.md` P4; kept short here, with the tier-degradation figures
  restated for this lane's element framing.
- **Dataset:** ~30,000 queries across Smart Car / Smart Home / Wearables domains, 152 verified
  functions in 23 categories, 8 complexity tiers from single commands to multi-turn/intent-blending.
- **Metric:** tool-name accuracy, exact match (tool + all arguments), and slot F1.
- **Scores & gap:** best model (Qwen-3-Omni-30B): Tier 1 (simple) 92.4% -> Tier 3 (multi-intent)
  74.7% -> Tier 8 (intent blending) 41.7% — a 50.7-point drop from simplest to hardest tier on the
  same model, with no human baseline reported.
- **Genealogy:** origin-domain **speech**; native (not ported) — this is a speech-first task design
  (audio-to-API-call), not a transcript-then-tool-call design.
- **Training-free vs fine-tuned:** n/a (benchmark); the 5 models tested (Qwen-3-Omni, Kimi Audio,
  Step-Audio-2, AudioFlamingo, Qwen-2.5-Omni) are evaluated as-shipped, frozen.
- **Class + verdict:** **element** (direct audio-to-tool-call grounding is the object under test) —
  the steep tier-wise degradation shows that once the tool element is available, success is gated by
  the frozen model's own compositional-reasoning and argument-grounding fidelity (a constraint),
  reinforcing the same negative as VoiceAgentBench: adding the element does not by itself cross the
  hard-tier capability boundary.
- **Fence tag:** single-session.
- **Omni role:** hybrid.
- **Delta:** CONFIRMS (cross-reference L4 P4).

### 17. tau-Voice — benchmarking full-duplex voice agents on real-world domains
- **Recognized problem/status:** this benchmark is already extensively covered elsewhere in this
  wiki (`2026-07-04-stage1-L4-speech-agentic.md` P1/C01/C02, plus `2026-07-06-s2s-proprietary.md`,
  `2026-07-06-voice-cascade.md`, `2026-07-06-verification-reward.md`); not re-derived here in depth.
  Source: [arXiv:2603.13686](https://arxiv.org/abs/2603.13686) (March 2026).
- **Why it belongs in this lane's ledger specifically:** the prior archive's negatives N1/N2 stated
  "no published pass@k or prompt-opt on any voice-agent benchmark." tau-Voice **partially updates**
  this: it is a published, verifiable-reward, **pass@1** result on a voice-agent benchmark (DB-state
  assertion, tau-bench-style), so the *metric infrastructure* for pass@k-style measurement on voice
  agents now publicly exists. It does **not**, however, refute the substantive part of N1/N2: the
  paper reports raw provider pass@1 (xAI 51%/38%, OpenAI 49%/35%, Google 31%/26% clean/realistic),
  not a training-free prompt-optimization or best-of-N *intervention* result against that metric — so
  "does prompt-opt/best-of-N move the needle on a voice-agent benchmark" remains, as of this survey,
  still unanswered in the published record. This distinction (metric now exists vs. intervention
  result still absent) is this lane's specific addition to the archive.
- **Class + verdict:** **element** (verifiable DB-state tool outcome is the object measured, same
  family as this project's on-disk tau2-bench).
- **Fence tag:** single-session.
- **Omni role:** hybrid.
- **Delta:** CONFIRMS + partial REFUTE-of-scope (the metric-infrastructure half of N1/N2 no longer
  holds; the intervention-result half still does).

---

## Negatives and empty-measurement-cells (first-class)

- **No human topline for most benchmarks.** Of the 17 entries above, only MMAU-Pro reports a
  quantified human score (77.9% vs 59.2% best model); MTR-DuplexBench reports a qualitative
  human > model gap with no number; ADU-Bench, SD-Eval, SpeechR, MMAR, and all three jailbreak
  benchmarks report no human baseline at all. "Human-vs-model gap" as asked by this lane's brief is
  frequently unanswerable from the current published record — most of the field instead reports
  model-vs-model deltas or an absolute ceiling well under 100% pass/accuracy.
- **No exact leaderboard numbers resolvable for ADU-Bench, AJailBench, MMAR, or Jailbreak-AudioBench**
  from the sources checked (abstracts/summaries describe qualitative findings — "struggle with,"
  "negligibly better than random" — without a single headline number); these are flagged rather than
  invented, per the hard rule against fabricating figures.
- **No benchmark in this lane isolates a same-weights-different-role ablation** for a dual-process
  (Talker-Reasoner-style) system. **Verifier correction:** the previous version of this entry named
  ConvFill / Thinking-While-Speaking as the clear candidate for such an ablation and called the
  same-vs-different-weights question "unresolved" there; a direct source check shows ConvFill's Talker
  and Reasoner are confirmed **different, disjoint models** (3 frontier proprietary Reasoners vs 7 small
  separately-fine-tuned Talkers, 135M-1.7B params) — so it is not actually a candidate for this ablation
  at all, resolved or not. The gap therefore stands as stated (no benchmark in this lane runs a
  same-weights-different-role ablation), but ConvFill should not be cited as the near-miss candidate for
  it.
- **JALMBench's "moderation only slightly improves security" finding is this lane's strongest
  positive evidence for the main thesis** applied to the safety/alignment constraint: a
  training-free, usage-pattern-style defense (a guardrail/moderation layer over the same frozen
  model) is measurably weaker than an architectural/training change (interleaved audio-text
  alignment) at closing the same gap.
- **tau-Voice partially closes N1/N2's infrastructure gap** (pass@1 metric now exists on a
  voice-agent benchmark) but leaves the substantive question (does a training-free intervention
  improve that pass@1) unanswered in the published record as of this survey.

---

## Verifier notes (adversarial pass, 2026-07-06)

**Scope:** direct WebFetch of ~14 of this lane's ~19 cited sources (abstract pages, arXiv HTML full
text, and PDF where needed), spot-checking headline figures, dataset-scale numbers, and the
new-info/read-out and element/usage-pattern framework calls. Two independent fetches were run on any
figure that looked load-bearing before treating a mismatch as confirmed.

**Confirmed exactly as stated (no changes needed):**
- Full-Duplex-Bench v1 (arXiv:2503.04721) — title/authors/scope match; TOR figures not independently
  re-derived (not present in the abstract-page extract) but not contradicted either.
- Full-Duplex-Bench-v3 (arXiv:2604.04847) — exists, title/authors/GPT-Realtime lead/Gemini Live 3.1
  latency framing all match.
- MMAU-Pro (arXiv:2508.13992) — **fully confirmed from Table 3 of the full text**: Human 77.9%,
  Gemini-2.5-Flash 59.2%, Gemini-2.0-Flash 55.7%, GPT-4o-Audio 52.5%, 18.7pp human-model gap, 5,305
  instances / 49 skills, 22 models evaluated. This is the lane's best-evidenced entry.
- JALMBench (arXiv:2505.17568) — confirmed from full text: non-adversarial ASR audio 21.5% vs text
  17.0%; AdvWave strongest audio-originated attack 96.2%; dataset scale exactly 11,316 text samples /
  245,355 audio samples / 12 LALMs / 8 attacks (4+4) / 5 defenses. The specific 49.7%/37.5%/95.2%/93.3%
  text-attack breakdown was not independently reproduced (extraction returned an approximate "42-43%"
  average instead) — plausible but not independently nailed down; not flagged as wrong given the core
  figures check out exactly.
- tau-Voice (arXiv:2603.13686) — confirmed exactly from Table 6: xAI 51%/38%, OpenAI 49%/35%, Google
  31%/26% clean/realistic; also confirms GPT-5 (reasoning) 85% and GPT-4.1 54% text baselines used in
  the paper's own framing (not previously in this entry, offered as extra corroboration).
- EchoChain (arXiv:2604.16456), Audio2Tool (arXiv:2604.22821), ADU-Bench (arXiv:2412.05167 modulo the
  correction below), Talker-Reasoner origin (arXiv:2410.08328), AJailBench (arXiv:2505.15406) — all
  confirmed to exist with title/scope/authors matching; AJailBench and MMAR's "no exact figure
  resolvable" empty-cells were independently checked and confirmed genuinely absent from the abstract
  (i.e., correctly flagged as empty rather than under-searched).

**Errors found and corrected in the entries above:**
1. **EchoChain (#5):** cited figures GPT-realtime-2025-08-28 44.0% / Grok Voice Agent 47.5% do not
   match the paper's Table 1 (45.0% / 48.5%, confirmed via two independent fetches). Corrected in the
   entry, with a note that the error likely also exists in `2026-07-04-stage1-L4-speech-agentic.md` P3
   (not fixed here — out of this lane file's scope, but worth a follow-up pass there).
2. **ADU-Bench (#6):** cited "13 LALMs"; the abstract states verbatim "extensive experiments on 16
   LALMs." Corrected.
3. **Talker-Reasoner/ConvFill (#9) — a framework-verdict error, not just a figure error:** the entry
   listed Claude Opus 4.6/4.7, GPT-5.5, Gemini 3.1, Qwen 3, Llama 3, Gemma 3, SmolLM2 as one
   undifferentiated backbone list and concluded the same-weights-vs-different-model question was
   "unresolved" — flagging ConvFill as the sharpest available candidate for testing the thesis's
   same-frozen-weights-different-role ambiguity fork. Direct inspection of the source (arXiv:2511.07397
   full text) shows this is wrong on both counts: (a) the paper does not use one undifferentiated pool —
   it uses two disjoint, non-interchangeable pools (3 frontier proprietary Reasoners: Claude Opus 4.7,
   GPT-5.5, Gemini 3.1 Pro; vs 7 small, separately fine-tuned Talkers, 135M-1.7B params: Gemma 3
   270M/1B, Qwen3 0.6B, SmolLM2 135M/360M/1.7B, Llama 3.2 1B); (b) the same-weights question is
   therefore not unresolved — it is resolved, and resolved as "different models," which means ConvFill
   does not serve as a test of the thesis's ambiguity fork at all (in either direction), rather than
   being an open/unresolved near-miss. Corrected in the entry and in the matching Negatives bullet.

**Not independently re-verified in this pass (time-boxed; flagged for a future pass, not assumed
wrong):** MTR-DuplexBench's five-dimension metric detail, SD-Eval's dataset/metric specifics, SpeechR's
per-model score table, MMAR's "~30 models" count, Jailbreak-AudioBench's toolbox description,
VoiceAgentBench's 60.6% figure, and Audio2Tool's per-tier accuracy figures (92.4%/74.7%/41.7%) — none
of these were fetched or were fetched but the source page did not surface the detailed table in the
extracted text; none showed any contradiction in what *was* surfaced, so they are left as-is rather
than corrected on speculation.

**Framework-verdict spot-check (new-info/read-out, element/usage-pattern):** aside from the ConvFill
correction above, the element-vs-constraint-vs-usage-pattern calls in entries #1-#8, #10-#17 hold up as
defensible on the evidence gathered — in particular #3 (FDB-v3), #15 (VoiceAgentBench), and #16
(Audio2Tool) correctly separate "the axis measured is a new element" from "the frozen model that wins
is a read-out," and #13 (JALMBench) correctly uses its own moderation-vs-interleaving contrast as
within-paper evidence for the thesis rather than over-claiming. No other verdict looked like a
usage-pattern-over-one-frozen-model case mis-labeled as element, or vice versa.

**Recency/negatives check:** all cited primary claims fall in 2025-01 through 2026-04, with two
explicitly-flagged pre-window roots (ADU-Bench, Dec 2024; SD-Eval, June 2024) correctly labeled as
such rather than silently included. The negatives section's core claim — that almost no benchmark in
this field reports a genuine human topline — holds up; MMAU-Pro's 77.9%/18.7pp gap is confirmed as the
one quantified exception.
