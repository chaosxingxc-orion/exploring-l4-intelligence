---
title: "Stage-1 lane — Verification / Verifiable-Reward / Self-Correction / Judges (2025-01 to 2026-07)"
date: 2026-07-06
stage: 1-argumentation
lane: verification-reward
---

> **🗄 ARCHIVED (2026-07-11)** — 已收官战役过程件（2026-07-06 omni-agentic 调研），仅作历史，非现行真源。

# Lane: verification-reward

> Stage-1 survey lane. Tests the organizing framework's fork — **verifier-as-role** (prompting a
> frozen model in a judge/critic role: no new information, a usage pattern) vs **verifier-as-tool**
> (an external, separately-trained reward model, or a symbolic/deterministic check: a genuine new-info
> element) — against the speech/audio verification, reward-model, self-correction and RLVR-for-agents
> literature, 2025-01 to 2026-07. Pre-2025 items are cited only as tagged genealogy roots. Every claim
> below carries the six-part per-item template: (1) recognized problem, (2) genealogy
> [origin-domain / transfer-status], (3) training-free vs fine-tuned, (4) three-axis class + verdict,
> (5) fence, (6) omni role. Delta-tagged against the prior archive (S1/S2/L4).

## Headline meta-finding (read before the claims)

**Every verification/reward-modeling *method* surveyed in this lane traces its genealogy to
text-LLM work — RLHF-style reward models, LLM-as-a-judge, generative verifiers (GenRM), rubric-based
judging, self-rewarding, and self-correction — none has a speech-native methodological origin.** Only
the *application substrate* (raw audio/speech content) is native to speech; the verification
*technique* is uniformly ported. This is itself evidence for the ELEMENTS framework: the "new
information" in every speech-domain judge/reward-model paper below is either (a) a newly trained
external model (a new element, transplanting the RLHF/GenRM recipe onto audio data), or (b) a
prompted, frozen, same-weights judge role (a usage pattern) that inherits the same bias/reliability
failure modes documented in the text-domain genealogy roots. No claim in this lane exhibits a
usage-pattern-only mechanism that cleanly crosses a capability boundary without a comparison to the
model's own ceiling (see C15's caveat).

Fork resolution observed empirically: wherever a **verifier-as-tool** (symbolic/deterministic, e.g.
database-state assertion) is used, reliability is ~100% by construction (C7, C8). Wherever a
**verifier-as-role** (prompted frozen model, same or different weights, judging) is used
training-free, measured reliability is well below usable thresholds (C2, C5, C10, C12). Every
speech-domain team that needed a *reliable* judge responded by training a new element (C1, C3, C4,
C6) rather than trusting the prompted role — a revealed-preference confirmation of the thesis by the
field's own engineering choices, even though none of the source papers frame it in exactly these
terms.

---

## Claims

### C1 — WavReward: a trained audio reward model closes the gap prompted judging leaves open

**Problem:** Existing evaluators for spoken-dialogue models (e.g. GPT-4o-audio) are text-based LLMs
that cannot capture non-textual acoustic/emotional signal in speech, and no reward model existed
specifically for end-to-end speech-to-speech dialogue.
**Genealogy:** origin-domain **LLM** (the scalar/preference reward-model recipe from RLHF), transfer
**ported** into an audio-native architecture that consumes raw speech-to-speech dialogue directly.
**Training-free vs fine-tuned:** the reward model itself is explicitly **trained/post-trained**
(reinforcement-learning-based "nonlinear reward mechanism," ChatReward-30K preference data) — NOT
training-free to build — but once built it is a **frozen external module** applied to a separately
frozen dialogue policy at BoN/RL-reward time.
**Class + verdict:** **element** (a new trained artifact = new information source distinct from the
policy) used as verifier-as-tool. Verdict: **new-info**. Objective evaluator accuracy on Qwen2.5-Omni
rises from 53.4% (prompted baseline) to 91.5% once the dedicated reward model replaces prompting — a
number that lines up with, and CONFIRMS, the archive's L4-P5 framing (prompted Qwen2.5-Omni ≈53.4%
objective accuracy) while showing the fix is an added element, not better prompting.
**Fence:** single-session (scores one dialogue turn/episode; no persistent state).
**Omni role:** hybrid (ingests raw audio directly = sensor; emits a graded judgment = brain).
**Delta:** NEW (system itself is post-archive) / CONFIRMS the archive's P5 diagnosis and its
resolution mechanism.
**Source:** [WavReward: Spoken Dialogue Models With Generalist Reward Evaluators](https://arxiv.org/abs/2505.09558) (2025-05)

### C2 — AudioJudge: training-free audio-LLM judging inherits text-LLM-judge biases

**Problem:** Whether large audio models (LAMs) can serve as unified, training-free judges across many
audio characteristics (pronunciation, speaking rate, speaker identity, quality) without task-specific
systems, and how well they align with human preference.
**Genealogy:** origin-domain **LLM** (LLM-as-a-judge paradigm), transfer **ported** to audio.
**Training-free vs fine-tuned:** **training-free** — zero/few-shot prompting of off-the-shelf LAMs
(audio concatenation + in-context learning is the most effective single technique); no fine-tuning of
judge or policy.
**Class + verdict:** **usage-pattern** (prompting an existing frozen model into a judge role, whether
the judge instance is the same or a different frozen model — no new training happens). Verdict:
**read-out**. Reliability is measurably limited: the paper explicitly finds "significant verbosity and
positional biases that require careful mitigation" — the same failure modes documented in the
text-domain genealogy root (C10) transferred wholesale into audio. A multi-aspect ensemble
(decomposing into lexical/quality/paralinguistic sub-judges) raises correlation with human preference
to 0.91 Spearman, but this is prompt/pipeline engineering over the same frozen weights, not new
information.
**Fence:** single-session. **Omni role:** hybrid.
**Delta:** CONFIRMS archive L4-P5 (training-free audio judges are unreliable) and extends it with the
specific bias mechanism (verbosity/position) inherited from the text-LLM-judge lineage.
**Source:** [AudioJudge: Understanding What Works in Large Audio Model Based Speech Evaluation](https://arxiv.org/abs/2507.12705) (2025-07)

### C3 — SpeechLLM-as-Judges (SQ-LLM): a fine-tuned multi-task judge, deepfake detection as the one objectively-verifiable sub-task

**Problem:** Existing speech-quality evaluation gives uninterpretable scalar/binary scores that do not
generalize across tasks or languages; need a structured, explanation-based judge spanning quality
assessment, pairwise comparison, improvement suggestion, and deepfake detection.
**Genealogy:** origin-domain **LLM** (LLM-as-judge + chain-of-thought reasoning-judge paradigm),
transfer **ported** to speech via the 32,207-clip / 128,754-annotation SpeechEval dataset.
**Training-free vs fine-tuned:** **fine-tuned** — SQ-LLM is explicitly trained with CoT reasoning and
reward optimization (SFT + RL) on SpeechEval; the judge's own weights change, though the policies it
evaluates stay frozen.
**Class + verdict:** **element** (a new, purpose-built trained judge = new information source).
Verdict: **new-info**.
**Fence:** single-session. **Omni role:** hybrid.
**Delta:** NEW — deepfake detection is notable as the one sub-task across this whole lane with an
objective, non-subjective ground truth (real vs. fake), unlike naturalness/quality scoring elsewhere.
**Source:** [SpeechLLM-as-Judges: Towards General and Interpretable Speech Quality Evaluation](https://arxiv.org/abs/2510.14664) (2025-10)

### C4 — AnyAudio-Judge: decomposing a holistic judge score into binary verifiable rubric items

**Problem:** Audio-instruction-following evaluation lacks fine-grained, verifiable per-item scoring;
a single scalar caption-alignment score is too coarse and uninterpretable.
**Genealogy:** origin-domain **LLM** (rubric-based LLM-judge evaluation, the "Learning to
Judge"/RubricEval text-domain lineage), transfer **ported** to audio.
**Training-free vs fine-tuned:** **fine-tuned** — the evaluator is trained via SFT + GRPO on a 105K
Corpus with hard negatives and CoT rationales; benchmarked on the held-out 7,920-sample AnyAudio-Judge
Bench (>84% accuracy).
**Class + verdict:** **element** — and structurally the *closest thing to a verifiable reward* in the
subjective-quality-judging half of this lane: complex audio instructions are decomposed into a
variable number of independent, binary, individually-checkable rubric items (rather than one holistic
score), then aggregated. Verdict: **new-info**. Explicitly used as a dense reward model for downstream
RL of instruction-following audio generation — verifier-as-tool.
**Fence:** single-session. **Omni role:** hybrid.
**Delta:** NEW — an audio-domain instance of turning a holistic judge into a set of verifiable
sub-claims, directly analogous to rubric-decomposition work in text (RubricEval).
**Source:** [AnyAudio-Judge: A Dynamic Rubric-Based Benchmark and Evaluator for Audio Instruction Following](https://arxiv.org/abs/2606.03116) (2026-06)

### C5 — SpeechJudge: zero-shot AudioLLM judges hit a hard reliability ceiling on naturalness (<70% human agreement)

**Problem:** TTS/speech-naturalness evaluation lacks large-scale human-preference data; before training
a dedicated judge, the paper first asks whether existing AudioLLMs can already do the job zero-shot.
**Genealogy:** origin-domain **LLM** (RLHF preference-model/reward-model lineage), transfer **ported**
to speech-naturalness judging.
**Training-free vs fine-tuned:** the **key finding is about the training-free baseline**: prompting
frontier AudioLLMs zero-shot (best: Gemini-2.5-Flash) as naturalness judges achieves **<70% agreement
with human judgment** — motivating the authors to then train SpeechJudge-GRM on the 99K-pair
SpeechJudge-Data human-feedback corpus.
**Class + verdict:** the headline empirical result is about the **usage-pattern** (zero-shot prompted
judging, same or different frozen weights, no new info beyond the prompt). Verdict: **read-out** — and
explicitly *insufficient*: <70% agreement is well below what a reliable reward signal needs. The
paper's own remedy (SpeechJudge-GRM, a generative reward model built on Qwen2.5-Omni-7B) is again a
trained element.
**Fence:** single-session. **Omni role:** hybrid.
**Delta:** CONFIRMS and *quantifies* the archive's L4-P5 claim with an apples-to-apples number distinct
from WavReward's (53.4% objective accuracy) and AudioJudge's (bias, not raw agreement) — three
independent papers converging on the same conclusion: training-free audio judging is measurably
unreliable, and every fix found in this lane is a trained element.
**Source:** [SpeechJudge: Towards Human-Level Judgment for Speech Naturalness](https://arxiv.org/abs/2511.07931) (2025-11)

### C6 — Dual-Axis Generative Reward Model: closing the L4-P3 reward gap for full-duplex turn-taking

**Problem:** Automated metrics for full-duplex interaction quality (turn-taking, timing) are superficial
proxies (behavioral statistics, timing-prediction accuracy); human evaluation is costly and
inconsistent — no dependable reward signal existed for RL of full-duplex spoken dialogue models.
**Genealogy:** origin-domain **LLM** (GenRM-style generative reward modeling, C14), transfer **ported**
and specialized to turn-taking dynamics.
**Training-free vs fine-tuned:** **fine-tuned** — trained on an annotated interaction-dynamics taxonomy
to output dual (semantic + timing) scores; used as an external RL reward signal for a separately
frozen policy at reward-computation time.
**Class + verdict:** **element** (a new dedicated reward model). Verdict: **new-info**, used as
verifier-as-tool for online RL.
**Fence:** single-session. **Omni role:** hybrid.
**Delta:** NEW — the first item surfaced in this lane that targets the archive's L4-P3
(dialog-state-under-interruption) problem specifically from the reward-design side, previously an
unoccupied cell.
**Source:** [Dual-Axis Generative Reward Model Toward Semantic and Turn-taking Robustness in Interactive Spoken Dialogue Models](https://arxiv.org/abs/2604.14920) (2026-04)

### C7 — τ-Voice: the cleanest verifier-as-tool exemplar — reliability is highest exactly where judgment is replaced by a symbolic check

**Problem:** No benchmark jointly measured whether full-duplex voice agents can complete consequential,
verifiable tasks (database mutations, correct tool calls) *while* managing real-time turn-taking under
realistic audio conditions.
**Genealogy:** origin-domain **LLM/agentic** (extends tau2-bench's Dec-POMDP verifiable-DB-state
design), transfer **native** — the DB-state assertion machinery transfers to full-duplex voice
unchanged.
**Training-free vs fine-tuned:** **training-free** — pure evaluation harness over frozen agents.
**Class + verdict:** the clean **verifier-as-tool** exemplar of this entire lane: task success is
decided by a **deterministic database-state comparison** against a gold standard — not by any model
judgment. An LLM is used only narrowly, to parse spoken-utterance *content* for the
"communicate-to-user" sub-check (because speech lacks punctuation and has disfluencies) — a bounded,
auxiliary usage-pattern layered on top of the real element. Verdict: **new-info** for the DB-state
element itself; the narrow content-parsing role is where residual unreliability concentrates. Measured
gap: text SOTA (GPT-5 reasoning) 85% pass@1 vs. voice agents 31-51% (clean audio) / 26-38% (realistic
audio), 79-90% of failures agent-driven (not benchmark artifacts), and up to -18pp from accent alone
for one provider while another is unaffected.
**Fence:** single-session (episode-scoped correctness check). **Omni role:** n/a for the verifier
itself (symbolic, not a model); the auxiliary content-parsing sub-check is text-only (brain, no direct
audio sensing).
**Delta:** CONFIRMS and sharpens archive P1 (task-completion collapse) and P5 (half-verifiable reward);
sharpens the mechanism — reliability is maximal exactly where an LLM-judge role is replaced by a
symbolic tool, and degrades exactly where an LLM must still play a judging role.
**Source:** [τ-Voice: Benchmarking Full-Duplex Voice Agents on Real-World Domains](https://arxiv.org/abs/2603.13686) (2026-03)

### C8 — τ²-bench + pass^k: even with a perfectly reliable non-model verifier, repeated sampling is bounded, not new information

**Problem:** Benchmarks checking only final-turn correctness overstate reliability; need a metric for
whether an agent is *consistently* correct across repeated independent attempts, on top of a verifiable
(non-LLM-judge) ground truth for agentic tool use.
**Genealogy:** origin-domain **LLM/agentic**, transfer **native** (this is the origin paper; τ-Voice
extends it to speech, C7).
**Training-free vs fine-tuned:** **training-free** evaluation.
**Class + verdict:** the ground-truth check is **element** (symbolic DB-state assertion, no model
judgment) — new-info, maximally reliable by construction. The **pass^k metric itself is a
usage-pattern diagnostic**: it measures what happens when you resample the *same frozen model* more
times on the *same task*. Verdict: **read-out** — pass^1 90% collapses to pass^8 57% on retail,
demonstrating that repeated sampling (a usage pattern, no new information) does not raise the
reliability ceiling; it merely exposes the model's own inconsistency. Directly load-bearing for the
MAIN THESIS. Caveat: even this "verifiable" benchmark needed a corrected release
(`tau2-bench-verified`) fixing task/DB-annotation errors in the original — a reminder that
"verifiable" ground truth is not automatically trustworthy out of the box.
**Fence:** single-session. **Omni role:** n/a (symbolic verifier).
**Delta:** CONFIRMS the archive's usage-pattern-bounded-by-oracle-ceiling framing with a concrete
agentic (not math/code) verifiable-reward number.
**Sources:** [τ²-Bench: Evaluating Conversational Agents in a Dual-Control Environment](https://arxiv.org/abs/2506.07982) (2025-06) · [tau2-bench (sierra-research, GitHub)](https://github.com/sierra-research/tau2-bench) · [tau2-bench-verified (amazon-agi, GitHub)](https://github.com/amazon-agi/tau2-bench-verified)

### C9 — Delay, Plateau, or Collapse: verifier noise is a hard constraint on any reward-driven method, untested for training-free audio judges

**Problem:** Real-world verifiers (including LLM-judges used as RL reward) are imperfect and noisy;
how does verifier error actually propagate into RL training dynamics?
**Genealogy:** origin-domain **LLM/agentic**, transfer **untransferred** to speech — no speech-specific
replication surfaced despite a targeted search.
**Training-free vs fine-tuned:** n/a (studies RL training dynamics) — but directly bears on how
reliable a training-free verifier must be before it is safe to use as a selection/RL signal.
**Class + verdict:** best classified as a **constraint** — a reward-estimation-error bound on RLVR,
matching exactly the "explicit constraint terms" (reward-estimation-error bound) the project's own
theory track requires for a convergence proof. Verdict: **n/a** (a boundary condition, not itself an
element or usage-pattern instance). Finding: as systematic verification error rises, RL training shows
three distinct failure modes in sequence — **delay**, then **plateau**, then outright **collapse**.
**Fence:** n/a. **Omni role:** n/a.
**Delta:** NEW to this lane; flagged as an **empty measurement cell** — no paper has yet fit this
delay/plateau/collapse curve using an actual measured training-free audio-judge error rate (e.g.
AudioJudge's verbosity/position bias, or SpeechJudge's <70% agreement) feeding a real RL loop over a
frozen omni model.
**Source:** [Delay, Plateau, or Collapse: Evaluating the Impact of Systematic Verification Error on RLVR](https://arxiv.org/abs/2605.02909) (2026-04; arXiv-confirmed submission 2026-04-06 — note the `2605.` ID prefix does not match its own submission month, an arXiv-side numbering quirk, not a citation error)

### C10 — Self-Preference Bias in LLM-as-a-Judge: the text-domain root showing same-weights judging is confounded, not new information (genealogy root, pre-window)

**Problem:** Does a same-model judge systematically favor its own outputs, and why?
**Genealogy:** origin-domain **LLM**, pre-2025 (2024-10) — cited only as a genealogy root per the
survey's recency exception.
**Training-free vs fine-tuned:** **training-free** (pure prompting-based judging).
**Class + verdict:** **usage-pattern** (same-weights judge role). Verdict: **read-out** — GPT-4 shows a
self-preference range of -38% to +90% on ArenaHard, tied to the *perplexity/familiarity* of the
evaluated text rather than genuine quality: the judge's signal is confounded with the generator's own
prior, i.e. it carries no information beyond what the generator already "knows."
**Fence:** single-session. **Omni role:** n/a (text).
**Delta:** NEW to this lane (genealogy root); **untransferred** to speech — no dedicated
self-preference-bias study for an audio-native judge scoring its own omni model's outputs was found,
an empty measurement cell directly relevant to this project's own reward-driven best-of-N designs over
a single frozen omni model.
**Source:** [Self-Preference Bias in LLM-as-a-Judge](https://arxiv.org/abs/2410.21819) (2024-10)

### C11 — Self-Rewarding Language Models: gains are attributable to weight updates, not to the frozen verifier-as-role itself (genealogy root, pre-window)

**Problem:** Reward models trained from static human preference are bottlenecked by human-level
feedback and stay frozen during LLM training; can a single model supply and improve its own reward
signal?
**Genealogy:** origin-domain **LLM**, pre-2025 (2024-01) — genealogy root for the verifier-as-role
side of the fork.
**Training-free vs fine-tuned:** explicitly **NOT training-free** — the same-model "LLM-as-a-Judge"
signal is used inside an **Iterative DPO training loop that updates weights**. This is a scope
boundary for this survey: the paradigm's compounding gains are fine-tuning gains, not evidence that a
frozen-weight verifier-as-role usage pattern alone crosses a capability boundary.
**Class + verdict:** **usage-pattern** (LLM-as-judge prompting) that is then folded into a
weight-updating loop. Verdict: **read-out** for the frozen-model claim specifically — the "new
information" here is the act of gradient training, which is out of scope for a training-free,
frozen-weight study.
**Fence:** cross-session-accumulating (iterative rounds compound across training iterations — but via
weight updates, not inference-time state).
**Omni role:** n/a (text).
**Delta:** NEW to this lane (genealogy root); clarifies scope. No speech-native
self-rewarding-with-weight-updates system surfaced (untransferred).
**Source:** [Self-Rewarding Language Models](https://arxiv.org/abs/2401.10020) (2024-01)

### C12 — "Large Language Models Cannot Self-Correct Reasoning Yet": the single most direct genealogy root for this lane's central prediction (pre-window)

**Problem:** Can an LLM, using only its own intrinsic judgment (no external feedback or tools), detect
and fix its own reasoning errors?
**Genealogy:** origin-domain **LLM**, pre-2025 (2023-10) — the genealogy root that most directly
matches the archive's stated "a same-weights model given a critic/verifier prompt never beats plain
majority" measurement.
**Training-free vs fine-tuned:** **training-free** (pure prompting; no fine-tuning).
**Class + verdict:** **usage-pattern** (self-verification/self-correction role, same weights, zero
external element). Verdict: **read-out** — intrinsic self-correction *fails* on reasoning: GPT-3.5
corrects only 7.6% of wrong GSM8K answers while breaking 8.8% of previously-correct ones (net
negative); performance does not reliably improve, and sometimes degrades, without EXTERNAL feedback
(human, training-data-derived, or tool-based).
**Fence:** single-session. **Omni role:** n/a (text).
**Delta:** NEW to this lane; **CONFIRMS** the archive's main-thesis negative (a usage pattern over one
frozen model, with no new information, does not cross a capability boundary). **Untransferred** to
speech: no equivalent controlled ablation (same-weights self-correction vs. externally-fed correction)
was found for a speech/omni model's reasoning or ASR output — an empty measurement cell, though C15
below is an adjacent, weaker speech-domain data point that complicates a naive reading.
**Source:** [Large Language Models Cannot Self-Correct Reasoning Yet](https://arxiv.org/abs/2310.01798) (2023-10)

### C13 — Scalable Best-of-N via Self-Certainty: the text-domain same-weights baseline the speech field has skipped past (2025, untransferred to speech)

**Problem:** Trained external reward models for best-of-N selection are expensive; can a reward-*free*
signal derived purely from the generator's own output-distribution confidence select comparably well?
**Genealogy:** origin-domain **LLM** (2025-02, within window) — genealogy root for the usage-pattern
side of the fork; **untransferred** to speech/omni (no audio-domain replication found).
**Training-free vs fine-tuned:** **training-free** — no reward model is trained at all; the selection
signal is computed purely from the SAME frozen model's own logits.
**Class + verdict:** **usage-pattern** (a same-weights signal carrying zero information beyond the
generator's own output distribution). Verdict: **read-out**. Self-certainty scales with N "akin to
reward models... without the computational overhead" and beats self-consistency on open-ended tasks —
but it is explicitly presented as a substitute *for* an external reward model, not shown to exceed one,
consistent with the thesis that a same-weights signal can approach, but is not demonstrated to
surpass, a genuinely external element's ceiling.
**Fence:** single-session. **Omni role:** n/a (text).
**Delta:** NEW to this lane; **untransferred** to speech/omni — no paper surfaced applying an
audio-omni model's own token-probability self-certainty as a training-free BoN selector for spoken
output, despite this lane's speech-domain judges (C1, C3, C4, C5, C6) all jumping straight to trained
external reward models without first benchmarking this weaker same-weights baseline that the text
domain used as its own point of comparison. Directly relevant to this project's own log-prob/
perplexity-based best-of-N work.
**Source:** [Scalable Best-of-N Selection for Large Language Models via Self-Certainty](https://arxiv.org/abs/2502.18581) (2025-02)

### C14 — Generative Verifiers (GenRM): a trained element beats a prompted judge role at matched task (genealogy root, pre-window)

**Problem:** Discriminative scalar verifiers and prompted LLM-as-judge underperform at best-of-N
verification for math/reasoning; can casting verification as next-token prediction (with
chain-of-thought) do better?
**Genealogy:** origin-domain **LLM**, pre-2025 (2024-08) — genealogy root; transfer **ported**
(AnyAudio-Judge C4 and SpeechLLM-as-Judges C3 are its speech-domain, trained descendants).
**Training-free vs fine-tuned:** **NOT training-free** — GenRM is an explicitly trained verifier (via
next-token prediction on labeled-correctness data), distinct from prompting a frozen model as a judge.
**Class + verdict:** **element** (a separately trained verifier model). Verdict: **new-info** — GenRM
outperforms LLM-as-a-Judge (untrained, prompting-based, usage-pattern) by **16-40% more problems
solved** on best-of-N math/reasoning tasks — direct, matched-task evidence that a trained external
verifier beats a prompted judging usage pattern.
**Fence:** single-session. **Omni role:** n/a (text).
**Delta:** NEW to this lane (genealogy root); **CONFIRMS** the thesis ranking (element > usage-pattern
for verification quality); its speech-domain descendants (C3, C4) close the genealogy loop.
**Source:** [Generative Verifiers: Reward Modeling as Next-Token Prediction](https://arxiv.org/abs/2408.15240) (2024-08)

### C15 — Training-free same-model self-check for ASR correction: a measured gain, but against a weak baseline, not a demonstrated ceiling crossing

**Problem:** LLM-based ASR error correction hallucinates — it over-corrects text that was already
right; a verification stage is needed to catch this without extra training or external tools.
**Genealogy:** origin-domain **LLM** (chain-of-thought self-verification pipelines), transfer
**ported** to the ASR-correction application.
**Training-free vs fine-tuned:** **training-free**, explicitly — "no additional information or
fine-tuning"; the verification stage is the **same LLM performing a self-check** (not an external
verifier, not a second model, not a confidence score).
**Class + verdict:** **usage-pattern** (same-model self-check, structured into error pre-detection →
chain-of-thought iterative correction → verification). Verdict: **read-out**, with an important caveat:
the paper reports real relative CER/WER reductions of 21%, 11%, 9%, and 11.4% across AISHELL-1,
AISHELL-2, and LibriSpeech from this purely training-free, no-new-info pipeline — the lane's clearest
*apparent* tension with the main thesis. Read carefully, the reported gain is against a naive
**direct-correction baseline** (which itself over-hallucinates), not against the frozen model's own
best-achievable (oracle) output — i.e. the structured self-check plausibly moves the operating point
*closer to the model's own ceiling* (fewer self-inflicted false corrections) rather than demonstrably
exceeding a capability boundary the plain model could never reach. No comparison to an actual external
verifier (confidence-based, or a second model) is reported, so whether a real element would do even
better remains untested in this specific paper.
**Fence:** single-session. **Omni role:** brain (operates over the ASR hypothesis text, not raw audio,
within the correction module itself).
**Delta:** NEW to this lane; flagged as a **requires-nuance** case rather than a clean CONFIRMS/REFUTES
— logged for a Stage-2 oracle-ceiling-controlled re-test rather than treated as a counter-example.
**Source:** [Fewer Hallucinations, More Verification: A Three-Stage LLM-Based Framework for ASR Error Correction](https://arxiv.org/abs/2505.24347) (2025-05)

---

## Negatives and empty measurement cells (first-class)

- **N1.** No paper fits the delay/plateau/collapse verifier-noise curve (C9) using an *actual measured*
  training-free audio-judge error rate (e.g. AudioJudge's bias, C2; SpeechJudge's <70% agreement, C5)
  feeding a real RL loop over a frozen omni model. The theory and the speech-judge-reliability
  measurements exist independently; nobody has connected them.
- **N2.** No dedicated self-preference-bias study (cf. C10) exists for a same-weights audio/omni judge
  scoring its own model's outputs — meaning any project doing reward-driven best-of-N reranking on a
  single frozen omni model (using that same model, or a same-family model, as the reward source) sits
  in an empirically unstudied risk zone for this specific bias.
- **N3.** No paper applies a same-weights, no-external-reward-model signal (self-certainty/log-prob
  confidence, cf. C13) as a training-free best-of-N selector for spoken/omni generation. Every
  speech-domain judge/reward paper in this lane (C1, C3, C4, C5, C6) jumped straight to a trained
  external reward model without first benchmarking this weaker, cheaper same-weights baseline that the
  text domain used as its own comparison point.
- **N4.** No published ablation isolates "self-check within the same model" (C15) from "a true external
  verifier" for the ASR self-correction loop — so it cannot yet be said whether same-weights
  self-verification in speech is fundamentally capability-bounded (per the text-domain root C12) or a
  genuine exception to it.
- **N5.** No pass^k / repeated-attempt reliability metric (cf. C8) is published for *any* voice-agent
  benchmark — even τ-Voice (C7), which otherwise directly extends τ²-bench, reports only pass@1 for
  voice, not pass^k. This confirms and extends the archive's N1/N2 (no published pass@k or prompt-opt on
  any voice-agent benchmark) specifically into the reliability-of-repeated-attempts dimension.
- **N6.** No speech-native analog of Self-Rewarding Language Models (C11) — i.e. no system that folds a
  same-weights (or same-family) audio/omni judge's verdicts into an iterative *weight-updating* loop —
  was found; this paradigm remains untransferred to speech (and would in any case fall outside a
  training-free frozen-weight scope if it appeared).

## Fork verdict for this lane

Across every clean **verifier-as-tool** instance found (τ-Voice/τ²-bench's deterministic database-state
check, C7/C8), reliability is effectively 100% by construction and it is exactly the mechanism this
project's own on-disk eval lanes (tau2-bench, eva-bench) already rely on. Across every
**verifier-as-role** instance found in speech (AudioJudge C2, SpeechJudge's zero-shot baseline C5), or
in its text-domain genealogy roots (self-preference bias C10, failed self-correction C12,
self-certainty C13), measured reliability is non-trivially degraded relative to a genuine external
element (trained reward model C1/C3/C4/C6, or a trained verifier C14, or a symbolic check C7/C8). No
claim surveyed demonstrates a usage-pattern-only mechanism crossing a capability boundary without a
comparison to the same model's own ceiling (C15 is the closest apparent counter-example, and it lacks
that control).

## Verifier notes

Adversarial pass (2026-07-06): spot-checked 9 of this lane's cited sources directly (arXiv abstract
pages + the export.arxiv.org Atom API for one), plus two targeted web searches against the N2/N3
negatives.

**Checked and confirmed accurate** (title, authors/claim substance, and the specific numbers cited in
the lane all matched the live source): C1 WavReward (arXiv:2505.09558 — 53.4%→91.5% confirmed), C2
AudioJudge (arXiv:2507.12705 — verbosity/positional bias + 0.91 Spearman confirmed), C4 AnyAudio-Judge
(arXiv:2606.03116 — 105K corpus / 7,920-sample bench / SFT+GRPO confirmed), C6 Dual-Axis GRM
(arXiv:2604.14920 — semantic+timing dual reward confirmed), C7 τ-Voice (arXiv:2603.13686 — 85% vs.
31–51%/26–38% pass@1 numbers confirmed exactly), C8 τ²-Bench (arXiv:2506.07982 — pass^k 90%→57% retail
decay confirmed via web search corroboration), C9 Delay/Plateau/Collapse (arXiv:2605.02909 — three-regime
finding confirmed), C13 Self-Certainty (arXiv:2502.18581 — authors, mechanism, and framing as a
reward-model substitute rather than a demonstrated superior confirmed).

**Two fixable errors found and corrected in place:**
1. **C5 SpeechJudge** — the lane twice named the trained remedy model "SpeechJudge-RM"; the paper
   (arXiv:2511.07931) names it **SpeechJudge-GRM** (a generative reward model built on Qwen2.5-Omni-7B).
   Fixed both occurrences. The substantive claim (<70% zero-shot agreement, motivating the trained
   remedy) is otherwise accurate.
2. **C9 date tag** — cited as "(2026-05)" from reading the arXiv ID prefix (`2605.`), but both the
   abstract page and the export API's `<published>` field independently give 2026-04-06. This is an
   arXiv-side numbering quirk (the ID month doesn't match the announced submission month for this one
   paper) rather than a wrong link — the URL, title, and findings are correct. Corrected the date tag
   and left a note so a future reader doesn't re-flag the same ID/date mismatch as a dead/wrong link.

**Framework-verdict check (part c):** re-derived each claim's element-vs-usage-pattern and
new-info-vs-read-out call independently from the confirmed source content (not just re-reading the
lane's own prose). All 15 calls are defensible under the stated rule (a usage pattern applied to one
frozen model — same or different weights, no gradient update — is read-out; a separately trained
artifact or a deterministic/symbolic check is new-info). Notable correct edge-case handling: C7 and C11
each correctly split a single paper into two verdicts (tool-vs-role sub-mechanism in C7; prompting-role
vs. the weight-updating DPO loop it feeds in C11) rather than forcing one label on a mixed system; C9 is
correctly kept out of the element/usage-pattern binary as a "constraint" class since it studies RL
training dynamics, not a verification mechanism itself.

**Recency/negatives check (part d):** all in-window claims (C1–C9, C13, C15) fall inside 2025-01 to
2026-07; pre-window items (C10–C12, C14) are explicitly tagged genealogy roots per the survey's stated
exception, consistent with the rule. The negatives section (N1–N6) is present and first-class (not an
afterthought); two of its "untransferred" claims (N2 self-preference bias for a same-weights audio
judge; N3 self-certainty as a training-free audio/omni BoN selector) were independently re-searched and
no contradicting paper surfaced — both empty cells hold up.

**No invented or unsupported claims found.** Every numeric claim spot-checked (accuracy deltas, sample
counts, pass@1/pass^k figures, Spearman correlations) matched the live source on the first or second
fetch; the only discrepancies were the two cosmetic errors above, now fixed.
