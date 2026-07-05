---
title: Eval Methodology for 2025+ Voice/Omni Agents — Task Success, Tool-Call Accuracy, Multi-Turn State, Duplex Timing, Safety, and the pass@k/Best-of-N Empty Cell
date: 2026-07-06
stage: 1-argumentation
lane: eval-methodology
---

# Lane: eval-methodology

Scope: evaluation METHODOLOGY for 2025+ voice/omni agents — task-success/completion, tool-call/argument
accuracy, multi-turn state retention, duplex latency/turn-taking, safety, LLM-judge vs verifiable-reward
reliability — with a targeted attempt to confirm or refute the archive's empty cells **N1/N2**: is there
ANY published pass@k / best-of-N / prompt-optimization result on ANY voice-agent benchmark?

**Headline answer: N1/N2 CONFIRMED, with an important refinement.** `pass@k`/`pass^k` terminology has now
entered the voice-agent eval literature (tau2-bench, EVA-Bench), but in every case found it is used as a
**reliability/consistency metric** across repeated trials of one frozen system — never as a **selection
mechanism** (an oracle/verifier picking the best of k outputs to raise a reported or deployed score). No
best-of-N, self-consistency, reranking, or prompt-optimization experiment was found on any of the nine
2025–2026 voice-agent/spoken-dialogue benchmarks checked, despite this being an actively thriving technique
in the text-LLM literature over the same window. EVA-Bench (May 2026) is the strongest piece of evidence:
it explicitly states its own system prompts were *not* optimized and flags prompt engineering as future
work that "would likely yield higher scores."

---

## Claims

### 1. τ²-bench (tau2-bench) carries the original τ-bench `pass^k` reliability metric (distinct from `pass@k`) forward into voice, and voice submissions are Pass^1-only for cost reasons

- **URL:** https://github.com/sierra-research/tau2-bench (see `docs/leaderboard-submission.md`,
  `docs/evaluation.md`, `RELEASE_NOTES.md`)
- **(1) Recognized problem:** single-trial success rate hides how often an agent is *reliably* correct on
  repeat attempts; `pass@k` = "at least one of k attempts succeeds" (widely used, optimistic), `pass^k` =
  "all k attempts succeed." **Verifier correction:** `pass^k` was *not* introduced by tau2-bench — it
  originates in the original text-only τ-bench paper (Yao et al., "τ-bench," arXiv:2406.12045, June 2024,
  pre-dating this lane's 2025+ window; e.g. it reports empirical `pass^8` < 25% in the retail domain),
  which tau2-bench (and now its voice extension) carries forward — this matches the claim's own genealogy
  line (2) below and the header has been corrected accordingly. The illustrative "90%-pass@1 model falls to
  57% pass^k at k=8" pairing in an earlier draft of this claim could not be located in any fetched source
  (github docs, the τ-bench HTML/PDF, or the τ²-bench/τ-Voice papers) and is mathematically inconsistent
  with the stated `pass^k = pᵏ` definition under an i.i.d. assumption (0.9⁸ ≈ 0.43, not 0.57) — it has been
  removed rather than repeated as an unverified number. The qualitative point (pass^k decays sharply and
  faster than pass@1 suggests) remains supported by the τ-bench paper's own pass^8 < 25% figure.
- **(2) Genealogy:** origin-domain **LLM** (customer-service tool-use agents; τ-bench text → τ²-bench
  dual-control) [ported], now extended natively to voice full-duplex mode via realtime-API providers
  (OpenAI, Gemini, xAI).
- **(3) Training-free:** yes — pure evaluation harness over frozen models.
- **(4) Axis: constraint** (a reliability/over-optimization-adjacent measurement construct, not itself a
  capability-crossing device). **Verdict: n/a** (measurement infrastructure).
- **(5) Fence:** single-session (each trial independent; no cross-session accumulation).
- **(6) Omni role:** brain (the audio-native model must reason over dialogue state and call tools).
- **Delta vs archive: NEW** — the archive did not have the pass^k reliability-decay formalism or the
  documented cost-driven Pass^1-only convention for voice leaderboard submissions ("Voice submissions
  typically only report Pass^1 scores since multi-trial evaluation with audio-native models is expensive").

### 2. EVA-Bench (ServiceNow, May 2026) reports `pass@1/pass@k/pass^k` as a *reliability* gap, and explicitly did NOT attempt prompt optimization — direct first-party confirmation of N1

- **URL:** https://arxiv.org/abs/2605.13841 (HTML: https://arxiv.org/html/2605.13841v1)
- **(1) Recognized problem:** single-trial voice-agent scores "systematically overstate deployment-grade
  quality." EVA introduces two composite metrics — **EVA-A** (Accuracy: task completion, faithfulness,
  audio-level speech fidelity) and **EVA-X** (Experience: conversation progression, spoken conciseness,
  turn-taking timing) — and documents an **accuracy–experience tradeoff** plus a median **pass@k − pass^k
  gap of 0.44 on EVA-A**, i.e., peak and reliable capability diverge substantially.
- **(2) Genealogy:** origin-domain **speech** (native benchmark construction: 213 scenarios, 3 enterprise
  domains, accent/noise perturbation suite), with the `pass@k`/`pass^k` terminology itself **ported from
  LLM** reasoning-eval literature [LLM→speech, ported].
- **(3) Training-free:** yes, eval-only. Task Completion is **deterministic** (SHA-256 hash of scenario-DB
  final state vs gold state); Faithfulness/Speech-Fidelity/Progression/Conciseness are **LLM-as-judge**
  (and LALM-as-judge for audio-native speech fidelity), with explicit threshold cutoffs (≥0.5, ≥0.95).
- **(4) Axis: usage-pattern** (pass@k/pass^k concern repeated sampling of one frozen model). **Verdict:
  read-out** — the paper measures variance/consistency of the *same* system; it explicitly does **not**
  deploy a selection mechanism, and states: *"agent system prompts were not optimized for
  performance—we constructed prompts to convey necessary guidelines and policies without correcting for
  model-specific errors,"* adding that *"targeted system parameter tuning and prompt engineering would
  likely yield higher scores than those reported here"* — i.e., prompt optimization is named explicitly as
  unexplored future work, not as a demonstrated result.
- **(5) Fence:** single-session.
- **(6) Omni role:** brain.
- **Delta vs archive: CONFIRMS** L4 N1/N2, and upgrades it from "not found" to "explicitly disclaimed as
  not attempted" by the benchmark's own authors, one month before this survey.

### 3. τ-Voice (Sierra, March 2026) shows voice agents retain only 30–45% of text-agent task-completion capability on identical grounded tasks — no best-of-N, no prompt optimization

- **URL:** https://arxiv.org/abs/2603.13686 (HTML: https://arxiv.org/html/2603.13686v1)
- **(1) Recognized problem:** prior evals treat conversational dynamics and task completion in isolation.
  τ-Voice extends τ²-bench into a full-duplex voice-agent benchmark combining **verifiable** grounded-task
  completion (DB-state comparison against gold), full-duplex interaction, and realistic audio, enabling a
  direct voice-vs-text comparison on identical tasks.
- **Result:** OpenAI `gpt-realtime-1.5`, Google `gemini-live-2.5-flash-native-audio`, and xAI
  `grok-voice-agent` score **31–51% pass@1 under clean audio** and **26–38% under realistic
  noise/accents**, vs **85%** for the best **text** agent on the same tasks — "no voice agent in this
  cohort reaches even 50% of text capability under realistic conditions."
- **(2) Genealogy:** origin-domain **LLM** (τ²-bench) [ported to voice].
- **(3) Training-free:** yes. Tool-call/task correctness is **deterministic** ("comparing the end state of
  the environment... against a gold standard"); agent *communications* are graded by an **LLM judge**
  (chosen explicitly over string-matching "to handle spoken output variability"). Turn-taking is measured
  via four aggregate scores: Responsiveness = avg(Response-Rate, Yield-Rate), Latency = avg(Response-
  Latency, Yield-Latency), plus an Interruption rate and a Selectivity score (correctly ignoring
  backchannels/vocal tics). **No pass@k, pass^k, best-of-N, or reranking is reported — pass@1 only** —
  and **no prompt optimization was attempted**: "All models receive identical system prompts with
  voice-specific guidance."
- **(4) Axis: constraint** (real-time/full-duplex audio substrate — the gap persists under *identical*
  prompts across voice/text, i.e., it is not closed by a usage-pattern/orchestration change). **Verdict:
  n/a** (constraint-axis documentation, not a lever).
- **(5) Fence:** single-session.
- **(6) Omni role:** hybrid (audio front-end as sensor; dialogue/tool reasoning as brain).
- **Delta vs archive: CONFIRMS** L4 P1 (task-completion collapse) with fresh, precise 2026 numbers, and
  independently **CONFIRMS N1/N2** (no best-of-N/prompt-opt attempted on this benchmark either).

### 4. Audio MultiChallenge (Dec 2025) extends text MultiChallenge to audio; best model reaches only 54.65% pass rate, with a new Voice-Editing axis

- **URL:** https://arxiv.org/abs/2512.14865
- **(1) Recognized problem:** existing spoken-dialogue benchmarks evaluate mostly synthetic speech and
  single-turn tasks; realistic multi-turn conversational ability (natural disfluency, mid-utterance
  repair) is underexplored.
- **(2) Genealogy:** origin-domain **LLM** (text MultiChallenge: Inference Memory, Instruction Retention,
  Self-Coherence — aclanthology.org/2025.findings-acl.958) [ported to audio], adding a genuinely
  speech-native **Voice Editing** axis (robustness to mid-utterance speech repairs/backtracking) and an
  **Audio-Cue** variant of Inference Memory (recalling ambient sounds/paralinguistic signals beyond
  semantic content).
- **Result:** 452 conversations, 47 speakers, 1,712 instance rubrics via a hybrid audio-native agentic +
  human-in-the-loop pipeline; even **Gemini 3 Pro Preview (Thinking)**, the top model, achieves only
  **54.65% pass rate**; Self-Coherence degrades further with longer audio context.
- **(3) Training-free:** yes, eval-only.
- **(4) Axis: element** (the ceiling is bounded by the frozen model's own long-context/attention
  capability — the same model fails identically regardless of any orchestration). **Verdict: read-out.**
- **(5) Fence:** single-session (multi-turn *within* one conversation; no cross-session claim).
- **(6) Omni role:** brain.
- **Delta vs archive: CONFIRMS** L4 P2 (instruction/reasoning gap) with a fresh, precise December-2025
  number and a new speech-native failure axis (Voice Editing) not previously catalogued.

### 5. EchoChain (April 2026) is a benchmark built directly around dialog-state-under-interruption; no system exceeds 50% pass rate

- **URL:** https://arxiv.org/abs/2604.16456
- **(1) Recognized problem:** "Real-time voice assistants must revise task state when users interrupt
  mid-response, but existing spoken-dialog benchmarks largely evaluate turn-based interaction and miss
  this failure mode." Identifies three concrete failure patterns: **contextual inertia**, **interruption
  amnesia**, and **objective displacement**.
- **(2) Genealogy:** **speech-native** — full-duplex mid-generation interruption has no direct text-LLM
  analog [speech, native].
- **(3) Training-free:** yes, eval-only; deterministic comparison between full-duplex interrupted runs and
  half-duplex (no-interruption) control conditions.
- **Result:** the half-duplex control shows total failures **drop 40.2%** relative to interrupted runs;
  across real-time voice models, **no system exceeds a 50% pass rate** on interrupted scenarios.
- **(4) Axis: constraint** (real-time/full-duplex base-architecture property — exactly the framework's
  named constraint category). **Verdict: n/a.**
- **(5) Fence:** single-session.
- **(6) Omni role:** brain (dialogue-state management under interruption).
- **Delta vs archive: CONFIRMS** L4 P3 (dialog-state-under-interruption) — this benchmark is essentially a
  dedicated instrument for exactly that archived problem, with fresh, strong quantitative backing.

### 6. VoiceAssistant-Eval (CUHK MMLab/SenseTime, Sept 2025) covers Safety and Roleplay with a hybrid LLM-judge + deterministic scoring stack; no pass@k/best-of-N reported

- **URL:** https://arxiv.org/abs/2509.22651 (HTML: https://arxiv.org/html/2509.22651v1)
- **(1) Recognized problem:** need a comprehensive AI-assistant benchmark across Listening/Speaking/
  Viewing; 10,497 examples, 13 task categories including Safety (SFT), Roleplay (RLP), Emotion (EMO),
  Instruction-Following (IF), Multi-Round (MR), Robustness (RBT).
- **(2) Genealogy:** origin-domain **speech** (native construction), judge methodology **ported from LLM**
  literature.
- **(3) Training-free:** yes, eval-only. Content quality uses **LLM-judge** (`gpt-oss-20b`, 13 evaluator
  prompts, plus emotion2vec-extracted emotion probabilities injected into judge prompts). Speech quality
  is **deterministic** (UTMOS). Consistency (e.g., multiple-choice tasks) is **deterministic** (Whisper
  transcription → modified WER with a length threshold). Roleplay speaker similarity is **deterministic**
  (WeSpeaker embedding similarity); the **Roleplay score is a multiplicative composite** — content ×
  speech-naturalness × speaker-consistency — deliberately exposing the semantic-accuracy vs audio-fidelity
  tension.
- **Result:** large **safety-alignment variance across frozen models on identical items** — the Moshika
  family scores **below 28** on safety while **Freeze-Omni reaches 79.8**; notably **GPT-4o-Audio (74.5)
  underperforms Freeze-Omni (79.8) on safety** despite broader general competence; a **16.3-point accuracy
  drop** for image+audio vs image+text queries on Qwen2.5-Omni-7B (59.2% → 42.9%).
- **No pass@k, pass@1-vs-k, best-of-N, or prompt-optimization is reported** — each model gets a single
  evaluation run.
- **(4) Axis: element** (the safety-score spread tracks *which frozen model* is evaluated on identical
  items — a model/weights difference, not an orchestration difference). **Verdict: read-out** (the
  benchmark reads out an existing element-level property; it does not itself add new information).
- **(5) Fence:** single-session.
- **(6) Omni role:** hybrid (audio+visual sensor fusion feeding a judged "brain" response).
- **Delta vs archive: NEW** (safety-variance numbers, multiplicative roleplay-scoring design) and
  **CONFIRMS** N1/N2 (no pass@k/best-of-N/prompt-opt reported here either).

### 7. VocalBench (May 2025) provides a rare direct LLM-judge-vs-human reliability number for speech (~88% agreement) — instantiating "verifier-as-role is a usage pattern, bounded"

- **URL:** https://arxiv.org/abs/2505.15727 (HTML: https://arxiv.org/html/2505.15727v2)
- **(1) Recognized problem:** need fine-grained vocal conversational-ability evaluation (12 abilities
  across Semantic / Acoustic / Chat [incl. Safety alignment, refusal rate, latency] / Robustness) plus
  validated confidence that an **LLM-as-judge** (`Qwen2.5-Max`) tracks human judgment.
- **(2) Genealogy:** origin-domain **LLM** (LLM-as-judge methodology) [ported to speech-chat evaluation].
- **(3) Training-free:** yes, eval-only.
- **Result — reliability calibration:** *"consistency rate"* is defined as "the proportion of cases where,
  for two model responses that receive different scores from the LLM, the human annotator selects the same
  better response as the LLM judge" — measured at **above 88%** agreement with human annotators (a second
  measure reports 90.64% average agreement across multiple LLM judges when they disagree with each other).
  **No pass@k, best-of-N, or self-consistency sampling is reported.**
- **(4) Axis: usage-pattern** (LLM-as-judge is precisely a *role* imposed on a model to evaluate another
  model's output — the framework's "verifier-as-role = usage pattern/weak" fork). **Verdict: read-out** —
  the ~88% (not 100%) agreement is a concrete, quantified bound on how much a role-based verifier can be
  trusted versus a genuinely new-info element (e.g., a human, or a deterministic DB-state check); it
  neither adds new information nor crosses a capability ceiling, it approximates human judgment with a
  measured error rate.
- **(5) Fence:** single-session.
- **(6) Omni role:** n/a (the judge is a separate text LLM, not the omni model under test).
- **Delta vs archive: NEW** — a concrete, citable LLM-judge-vs-human reliability figure for the speech
  domain, useful as a quantitative anchor for the "verifier-as-role = weak" claim in the framework.

### 8. URO-Bench (Feb 2025) exemplifies the recurring three-way hybrid eval stack: LLM-judge + rule-based WER + a separately fine-tuned emotion-aware probe

- **URL:** https://arxiv.org/abs/2502.17810
- **(1) Recognized problem:** need a comprehensive speech-to-speech (S2S) benchmark spanning
  multilingualism, multi-round dialogue, and paralinguistics (Basic/Pro tracks × Understanding/Reasoning/
  Oral-Conversation).
- **(2) Genealogy:** origin **speech** (native benchmark), judge methodology **ported from LLM**.
- **(3) Training-free:** eval-only for the systems under test; but the "fine-grained emotion-aware model"
  component used as part of the scoring stack is itself a separately trained probe, not the frozen system
  under evaluation.
- **Methodology:** transcribe spoken output via Whisper-large-v3, then score with (a) **LLM-as-judge** for
  semantic correctness/task alignment, (b) **rule-based WER**, and (c) a **fine-tuned emotion-aware model**
  for emotional coherence — a three-way hybrid stack that recurs across nearly every 2025–2026 voice
  benchmark surveyed in this lane (cf. VoiceAssistant-Eval, VocalBench above).
- **(4) Axis: n/a** (methodology-pattern reference, not itself a capability claim).
- **(5) Fence:** single-session.
- **(6) Omni role:** n/a.
- **Delta vs archive: NEW** — documents the *recurring hybrid eval-stack pattern* (deterministic WER +
  LLM-judge + a small trained auxiliary probe) as the field's emerging default methodology, worth citing
  as a design convention rather than a one-off result.

### 9. Talking Turns (Apple/CMU, ICLR 2025) judges turn-taking with a trained CLASSIFIER, not a generative LLM-judge — a clean instance of "verifier-as-tool = a real element"

- **URL:** https://arxiv.org/abs/2503.01174
- **(1) Recognized problem:** audio foundation models are rarely evaluated on fluent turn-taking (turn
  change, backchannel, interruption) despite this being central to natural conversation.
- **(2) Genealogy:** origin **speech**, native; but the *pattern* of substituting a small discriminative
  judge for a generative LLM-judge has broader ML-metrics lineage [speech, native].
- **(3) Training-free:** the systems under test are evaluated training-free; the **judge itself is a
  separately supervised/trained model** (predicts turn-taking events from human-human conversation
  data) — i.e., a genuinely new **element** is added to the evaluation pipeline, not a role prompted onto
  the same frozen model being tested.
- **Focus:** three turn-taking events — turn change, backchannel, interruption.
- **(4) Axis: element** (verifier-as-tool: a distinct trained component, not a role over the tested model).
  **Verdict: new-info** — this is a concrete, dated (Feb/Mar 2025, pre-dating most 2026 benchmarks in this
  lane) instantiation of the framework's own predicted "verifier-as-tool is a real element" fork, as
  opposed to the weaker "verifier-as-role" pattern seen in LLM-judge setups (cf. claim 7).
- **(5) Fence:** single-session.
- **(6) Omni role:** n/a (external judge component).
- **Delta vs archive: NEW** — a genealogy root for the "verifier-as-tool" fork specifically for duplex/
  turn-taking metrics, and the earliest (2025-03) benchmark found in this lane.

### 10. SoulX-Duplug (March 2026) crosses a duplex-turn-management capability by adding a new trained streaming-state-prediction module, not by prompting

- **URL:** https://arxiv.org/abs/2603.14877 (companion eval set: SoulX-Duplug-Eval,
  https://huggingface.co/datasets/Soul-AILab/SoulX-Duplug-Eval — the on-disk `soulx-duplug` benchmark)
- **(1) Recognized problem:** real-time full-duplex conversation needs low-latency streaming state
  prediction (a "semantic VAD") that leverages textual/intent information, not just acoustic VAD.
- **(2) Genealogy:** **speech-native**.
- **(3) Training-free:** **no** for the module itself — SoulX-Duplug is a **fine-tuned 0.6B streaming
  state-prediction model**, plugged in front of (or alongside) a frozen dialogue backbone ("plug-and-play").
  The companion **SoulX-Duplug-Eval** benchmark extends prior full-duplex evaluation sets with improved
  bilingual coverage.
- **Result:** the system built on this module "outperforms existing full-duplex models in overall turn
  management and latency performance."
- **(4) Axis: element** (a literal new trained connector/component added to the pipeline — matches the
  framework's "connectors" sub-category of elements). **Verdict: new-info** — directly supports the
  MAIN THESIS: the duplex-turn-management capability boundary here was crossed by **adding a new-info
  element** (a trained module), not by any usage-pattern/prompting change over a frozen backbone.
- **(5) Fence:** single-session.
- **(6) Omni role:** hybrid (a sensor-like semantic-VAD front end feeding the dialogue "brain").
- **Delta vs archive: NEW** — traces the project's on-disk `soulx-duplug` benchmark to its source paper and
  confirms it is a real, resolvable, recent (2026-03) release with an explicit element-vs-usage-pattern
  reading.

### 11. HalluAudio (ACL 2026) isolates PERCEPTION-fidelity hallucination as a distinct constraint-axis failure, separate from agentic task-success failure

- **URL:** https://arxiv.org/abs/2604.19300
- **(1) Recognized problem:** hallucination in Large Audio-Language Models (semantically incorrect or
  acoustically unsupported responses) is underexplored relative to text/vision hallucination benchmarks;
  spans speech, environmental sound, and music domains (acoustic grounding, temporal reasoning, music-
  attribute understanding).
- **(2) Genealogy:** **speech-native**, methodologically adjacent to text/vision hallucination-benchmark
  lineage [ported pattern, native content].
- **(3) Training-free:** yes, eval-only — human-verified QA pairs plus adversarial prompts to induce
  hallucination; standard automated metrics, no retraining.
- **Result:** "significant deficiencies in acoustic grounding, temporal reasoning, and music attribute
  understanding" across evaluated LALMs.
- **(4) Axis: constraint** (perception fidelity — explicitly the framework's named "a model quality"
  constraint category, distinct from agentic/task-success axes covered by claims 3–6). **Verdict: n/a.**
- **(5) Fence:** single-session.
- **(6) Omni role:** sensor (the failure mode is at the acoustic-grounding/perception layer, not the
  agentic-reasoning layer measured by tau-Voice/EchoChain/VoiceAssistant-Eval).
- **Delta vs archive: NEW** — useful boundary case showing the field is already stratifying
  perception-fidelity failures (constraint axis) from agentic-capability failures (element/usage-pattern
  axes) in its benchmark design — itself indirect evidence *for* the survey's three-axis organizing
  framework.

### 12. The empty cell, confirmed by systematic negative search: text-domain best-of-N/self-consistency/verifier-reliability research is thriving in 2025–2026; zero instances found applied to any voice-agent benchmark

- **URLs (text-domain best-of-N/verifier research confirmed active, none touching voice):**
  https://arxiv.org/pdf/2604.12196 ("Beyond Majority Voting: Efficient Best-Of-N with Radial Consensus
  Score"), https://arxiv.org/pdf/2502.18581 ("Scalable Best-of-N Selection for Large Language Models via
  Self-Certainty"), https://arxiv.org/pdf/2604.07666 ("An Imperfect Verifier is Good Enough: Learning with
  Noisy Rewards")
- **(1) Recognized problem (meta-level):** whether the mature text-LLM toolkit of best-of-N sampling,
  self-consistency/majority voting, reward-model reranking, and automatic prompt optimization has been
  demonstrated to raise task success on any voice-agent benchmark.
- **(2) Genealogy:** all three cited works are **origin-domain LLM**, reasoning/math/code focused,
  **untransferred** to speech as far as this search could determine.
- **(3) Training-free vs fine-tuned:** mixed within the text-domain literature (some use frozen models
  with sampling-only selection — training-free; others train reward/verifier models) — irrelevant here
  since none apply to voice.
- **(4) Axis: usage-pattern** (best-of-N/self-consistency are, by construction, usage patterns — repeated
  sampling + selection — over one frozen model). **Verdict: read-out** — per the framework's own
  prediction, such usage-pattern-only techniques over a single frozen model are bounded by that model's
  oracle ceiling and add no new information; consistent with why none of the nine voice-agent benchmarks
  surveyed in this lane (τ²-bench, τ-Voice, EVA-Bench, VoiceAssistant-Eval, VocalBench, URO-Bench, Audio
  MultiChallenge, EchoChain, and SoulX-Duplug) report such an experiment. (**Verifier correction:** an
  earlier draft also named "VoiceBench" here and in the summary list below, but VoiceBench — a real, live
  benchmark, arXiv:2410.17196, Oct 2024 — is never introduced as its own dated claim/URL anywhere in this
  lane and pre-dates the 2025-01+ recency window; removed from both lists rather than left as an uncited
  reference. If VoiceBench's own pass@k/best-of-N status is wanted for completeness it should get its own
  dated claim with a fetched citation in a future revision.)
- **(5) Fence:** n/a (cross-cutting meta-observation across many papers/benchmarks).
- **(6) Omni role:** n/a.
- **Delta vs archive: CONFIRMS** L4 N1/N2 — and strengthens it from "not found in our prior pass" to
  "actively searched for across 9 named 2025–2026 voice-agent/spoken-dialogue benchmarks plus 3 confirmed
  live text-domain best-of-N papers, with zero crossover instances located, and one benchmark author
  (EVA-Bench) explicitly disclaiming having tried prompt optimization."

### 13. SDiaReward / ESDR-Bench (March 2026): a genuine trained reward-model ELEMENT for spoken dialogue exists, but is benchmarked only on its own preference accuracy — not yet shown closing a voice-AGENT capability gap via best-of-N

- **URL:** https://arxiv.org/abs/2603.14889 (project page: https://sdiareward.github.io/, code:
  https://github.com/MM-Speech/SDiaReward)
- **(1) Recognized problem:** spoken-dialogue response quality has a "modality gap" (prosody/emotion) and
  a "colloquialness gap" (written-script vs natural speech) that text-only reward models miss; SDiaReward
  is an end-to-end multi-turn reward model trained on ~13k episode-level pairwise-preference samples
  (SDiaReward-Dataset), benchmarked for pairwise-preference accuracy on **ESDR-Bench**, where it
  outperforms general-purpose audio LLMs used zero-shot as judges.
- **(2) Genealogy:** origin-domain **LLM** (RLHF/DPO reward-modeling lineage — Ouyang et al., Rafailov et
  al. DPO are cited precedents) [ported to speech, with two speech-specific axes added].
- **(3) Training-free:** **no** — SDiaReward is itself a fine-tuned reward model, i.e., a genuinely new
  **element** (a trained verifier/connector), not a usage pattern over a frozen model.
- **(4) Axis: element.** **Verdict: new-info** *for the reward model as a component* — but **flagged
  unverified/hedged** for any downstream claim that it was deployed in a best-of-N loop to raise task
  success on a task-oriented voice-**agent** benchmark: full-text extraction of the paper was partially
  obstructed (PDF compression prevented clean quoting of the experiments section), and corroborating
  sources (arXiv abstract, project page, GitHub description) describe it only as being benchmarked for its
  **own pairwise-preference accuracy** on ESDR-Bench, not as a reranker demonstrated to improve pass@k on
  an agentic benchmark such as τ²-bench/τ-Voice. This is the closest candidate found to an element that
  *could* close the N1/N2 empty cell, but as published it does not yet do so — excluded from key findings
  as a "best-of-N result," retained here as a hedged/partial claim per the hard rule to mark uncertain
  claims rather than invent specifics.
- **(5) Fence:** single-session (per-episode reward).
- **(6) Omni role:** hybrid (external reward model consuming audio+text of the dialogue episode; not the
  omni model under test).
- **Delta vs archive: NEW**, hedged.

---

## Summary of negatives / empty cells (first-class)

1. **No benchmark among the nine checked** (τ²-bench, τ-Voice, EVA-Bench, VoiceAssistant-Eval, VocalBench,
   URO-Bench, Audio MultiChallenge, EchoChain, SoulX-Duplug) reports a best-of-N-with-selection or
   automatic-prompt-optimization result that raises reported/deployed task success.
2. **EVA-Bench explicitly disclaims prompt optimization** as unattempted future work, in its own words —
   the strongest first-party confirmation of N1 found in this pass.
3. **τ²-bench voice submissions are Pass^1-only** by documented convention (multi-trial audio-native
   evaluation is "expensive"); this is a *cost* barrier, not a demonstrated impossibility — leaves the
   empty cell open rather than closed.
4. **pass@k/pass^k terminology, where it exists in voice-agent papers (EVA-Bench, τ²-bench), is strictly a
   reliability/consistency lens** on one frozen system across repeated trials — never a selection
   mechanism to boost a score. This is a definitional refinement the archive's N1/N2 statement did not
   yet have evidence to draw.
5. **The identical technique (best-of-N / self-consistency / reward-model reranking) is a thriving,
   multi-paper 2025–2026 text-LLM research area** (confirmed: arXiv 2604.12196, 2502.18581, 2604.07666),
   with **zero confirmed crossover** into any voice-agent or spoken-dialogue benchmark found by targeted
   search.
6. **SDiaReward/ESDR-Bench is the closest candidate element** (a trained spoken-dialogue reward model)
   that *could* be used for best-of-N reranking on a voice-agent task, but as published it is benchmarked
   only for its own preference accuracy, not deployed in a best-of-N pipeline against an agentic benchmark
   — so even this candidate does not close the cell.
7. **No usage-pattern-only technique surveyed in this lane crossed a capability boundary over one frozen
   model.** Every genuine capability-boundary crossing found (SoulX-Duplug's streaming-state module,
   Talking Turns' trained turn-taking judge, SDiaReward's trained reward model) required adding a new
   **element** (a trained component), consistent with — not contradicting — the survey's MAIN THESIS.

---

## Verifier notes (adversarial pass, 2026-07-06)

**Scope:** spot-checked 12 of the lane's cited URLs with WebFetch (exceeding the 5–8 minimum) — EVA-Bench
(abs + HTML), τ-Voice (abs + HTML), the tau2-bench GitHub repo (root, `docs/leaderboard-submission.md`,
`docs/evaluation.md`, `README.md`), Audio MultiChallenge, EchoChain, VoiceAssistant-Eval (HTML), VocalBench
(HTML), URO-Bench, Talking Turns, SoulX-Duplug (abs + HTML), HalluAudio, SDiaReward (abs + project page),
plus all three text-domain best-of-N papers (2604.12196, 2502.18581, 2604.07666) and the out-of-lane
VoiceBench paper (2410.17196). No dead links; every fetchable arXiv ID and the GitHub repo resolved to the
real, correctly-titled paper/page claimed.

**Findings and dispositions:**

1. **(Fixed) Mis-attributed genealogy in Claim 1's header.** The original header said tau2-bench
   "introduces" `pass^k`. WebFetch of the original τ-bench paper (arXiv:2406.12045, June 2024) confirms
   `pass^k` originates there ("pass^8 < 25% in retail"), pre-dating this lane's window; tau2-bench and its
   voice extension carry the metric forward, they did not invent it — this also matches the claim's own
   genealogy line, so the header was internally inconsistent with its own body. Reworded; body now cites
   the origin paper explicitly.
2. **(Fixed) Unverifiable/inconsistent illustrative number in Claim 1.** "A 90%-pass@1 model falls to 57%
   pass^k at k=8" could not be located in any fetched source (tau2-bench docs, τ-bench HTML/PDF, τ-Voice/
   EVA-Bench papers) and is arithmetically inconsistent with the claim's own `pass^k = pᵏ` definition under
   an i.i.d. reading (0.9⁸ ≈ 0.43, not 0.57). Removed rather than repeated as fact; the qualitative
   "decays sharply" point is retained, now anchored to the verified `pass^8 < 25%` figure instead.
3. **(Fixed) Uncited "VoiceBench" in two summary lists.** "VoiceBench" was named as the 10th of "ten
   voice-agent benchmarks checked" in the headline, Claim 12, and the negatives summary, but never
   appears as its own dated claim with a URL anywhere in the document — a real benchmark (confirmed live,
   arXiv:2410.17196) referenced without having actually been checked/cited in this pass, and it pre-dates
   the 2025-01+ recency window in any case. Removed from all three lists; counts corrected from "ten" to
   "nine" throughout (headline, Claim 12 body, Claim 12 delta line, negatives-summary item 1) to match the
   nine benchmarks that actually have dedicated, cited claims in this lane.
4. **(Confirmed, no change) All other spot-checked quotes/numbers matched their sources closely**,
   including exact-string matches for: EVA-Bench's "system prompts were not optimized..." disclaimer and
   its 0.44 median pass@k−pass^k gap; the tau2-bench leaderboard doc's "Voice submissions typically only
   report Pass^1 scores..." line; Audio MultiChallenge's 54.65% Gemini 3 Pro figure, 452/47/1,712 dataset
   stats, and Voice Editing axis; EchoChain's three failure patterns, 40.2% control delta, and <50%
   pass-rate ceiling; VoiceAssistant-Eval's 10,497/13-category scale, Moshika-vs-Freeze-Omni safety spread,
   and Qwen2.5-Omni-7B 59.2%→42.9% drop; VocalBench's Qwen2.5-Max judge, >88% and 90.64%/87.11% consistency
   figures; SoulX-Duplug's Qwen3-0.6B LoRA-fine-tuned backbone with frozen tokenizer; SDiaReward's
   ESDR-Bench pairwise-preference framing with its best-of-N-deployment hedge independently corroborated
   (its own project page describes only preference-accuracy evaluation, no reranking pipeline); Talking
   Turns' trained-classifier-as-judge method; HalluAudio's ACL 2026 acceptance and three-domain scope; and
   all three text-domain best-of-N papers' real titles/authors and text-only scope.
5. **(Minor, not edited) VocalBench's "90.64% average agreement across multiple LLM judges when they
   disagree with each other"** (Claim 7) is loosely worded — the fetched source ties 90.64% specifically to
   the Qwen2.5-Max judge's own consistency rate (vs. 87.11% for GPT-4.1-Mini), not to inter-judge agreement
   "when they disagree with each other." Low severity (doesn't change the ~88–91% reliability-bound
   conclusion the claim draws); flagged here rather than edited since the core number and its use are sound.
6. **Framework-verdict audit (element/usage-pattern × new-info/read-out):** all 13 claims' axis/verdict
   calls were checked against the framework and found defensible. The two contrastive pairs the lane leans
   on hold up: "verifier-as-role" (LLM-as-judge, Claim 7 VocalBench; usage-pattern → read-out, bounded by a
   measured ~88% human-agreement ceiling) vs. "verifier-as-tool" (a separately trained component, Claim 9
   Talking Turns and Claim 10 SoulX-Duplug; element → new-info). Claim 13 (SDiaReward)'s split verdict —
   new-info for the reward model as a component, but explicitly hedged/unverified for any best-of-N
   deployment claim — is appropriately cautious and is the one place a real gap (a trained spoken-dialogue
   reward model existing) could plausibly close N1/N2 but, as published and as independently re-checked
   here, does not. No instance was found where a usage-pattern-over-one-frozen-model claim was mis-labeled
   new-info.
7. **Recency/negatives check:** all claims fall inside 2025-01–2026-07 except the (now-removed) VoiceBench
   mention and the necessarily-earlier genealogy citations (τ-bench 2024-06, MultiChallenge-text
   2025-findings-ACL) used only to trace lineage, not as fresh evidence. Negatives are first-class
   throughout — the lane's entire structure is a negative-result confirmation (N1/N2), with an explicit,
   itemized "Summary of negatives / empty cells" section; this was not found to be softened or buried.
8. **Overall verdict:** the lane's headline claim — pass@k/pass^k terminology has entered voice-agent eval
   but strictly as a reliability lens, never as a best-of-N selection mechanism, and no voice-agent
   benchmark among those checked reports best-of-N/prompt-optimization raising task success — holds up
   after independent re-fetching of its sources, modulo the three fixes above (none of which reverse the
   headline conclusion; they tighten attribution and remove one uncited/unverifiable number and one
   uncited benchmark name).
