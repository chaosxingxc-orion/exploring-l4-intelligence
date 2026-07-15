---
title: On-disk agent-eval benchmarks — what each measures, how it scores, and what it says about elements vs. usage-patterns
date: 2026-07-06
stage: 1-argumentation
lane: eval-benchmarks-ondisk
---

> **🗄 ARCHIVED (2026-07-11)** — 已收官战役过程件（2026-07-06 omni-agentic 调研），仅作历史，非现行真源。

> Stage-1 survey lane. Catalogs the eval instrumentation this project already has on disk
> (`docs/data.md`, `docs/datasets.lock.json`) against the ELEMENTS / USAGE-PATTERNS / CONSTRAINTS
> framework. Delta-tagged against the prior archive, principally
> [[2026-07-04-stage1-L4-speech-agentic]] ("L4"), which already treats several of these benchmarks
> from a *problem-definition* angle (P1–P5, negatives N1–N5); this lane instead catalogs the
> *instruments themselves* — what each one measures, how it scores (judge vs. verifiable), and what
> its own published results say about the element/usage-pattern boundary. Every URL below was
> fetched or found via WebSearch/WebFetch this session and resolved.

## 1. τ²-bench / tau2-bench (base, text) — dual-control tool-agent benchmark

**(1) Recognized problem.** Prior tool-agent benchmarks (τ-bench) are single-control: only the
agent calls tools against a shared DB while the "user" is a passive information source. Real
domains (telecom troubleshooting, joint account changes) need **dual-control**, where the user
must also act on the shared environment — τ²-bench formalizes this as a Dec-POMDP and adds a
compositional task generator that programmatically creates diverse, **verifiable** tasks across
retail/airline/telecom(+mock) domains.

**(2) Genealogy.** Origin-domain: **LLM** (direct descendant of τ-bench, arXiv 2406.12045).
Transfer status: **native** (still text/tool-calling, no modality change) — τ²-bench itself doesn't
cross into speech; that crossing is a separate paper (τ-Voice, item 1b below).

**(3) Training-free vs. fine-tuned.** The benchmark evaluates frozen, prompted agents (no gradient
step); it is itself pure measurement infrastructure, not a method.

**(4) Three-axis class + verdict.** **Constraint** (verifiable-reward measurement infrastructure —
this is exactly the L4 archive's P5 concern, "speech-robust-verifiable-reward," instantiated on the
text side where it already works cleanly). Within the benchmark's own design, two sub-components
sit on opposite sides of the main thesis's verification fork: the DB-state-diff reward is
**verifier-as-tool** (a real element — deterministic, no LLM judgment involved) while the "user" is
an **LLM prompted into a role** (verifier/actor-as-role — a usage pattern, since the user simulator
is just another instance of an LLM playing a persona, not a new information source). **Verdict:**
CONFIRMS the framework's fork — the part of τ²-bench that gives reliable signal (DB diff) is the
tool-verifier, not the role-played user.

**(5) Fence tag.** single-session (each task is one self-contained conversation; no state persists
across tasks).

**(6) Omni role.** n/a (base τ²-bench is text-only, no audio).

**Sources:** [τ²-Bench: Evaluating Conversational Agents in a Dual-Control Environment](https://arxiv.org/abs/2506.07982) (2025-06, arXiv 2506.07982) · [sierra-research/tau2-bench (GitHub)](https://github.com/sierra-research/tau2-bench) · on-disk record: `docs/datasets.lock.json` → `tau2-bench`, source `evalscope/tau2-bench-data` (ModelScope). **Delta:** CONFIRMS L4's C02 (τ²-bench/τ-bench reward genealogy already archived).

## 1b. τ-Voice — the full-duplex voice extension of τ²-bench

**(1) Recognized problem.** No benchmark combined verifiable, grounded dual-control tasks with
*full-duplex, realistic* audio; text-only τ²-bench can't test whether voice-channel noise (accents,
environment, VAD/turn-taking) itself causes task failure independent of reasoning ability.

**(2) Genealogy.** Origin-domain: **speech** (the paper's contribution is the audio/full-duplex
layer); transfer status: **ported** from τ²-bench's env+reward design, decoupling simulation time
from wall-clock so an LLM-driven user simulator can run without real-time constraint.

**(3) Training-free vs. fine-tuned.** Evaluates frozen commercial realtime models (GPT-Realtime,
Gemini Live, Grok Voice per L4); no weight changes.

**(4) Three-axis class + verdict.** Constraint (real-time/full-duplex measurement, explicitly one of
the three constraint categories named in this survey's organizing framework). **Verdict: CONFIRMS
L4's N1, corrected by verifier (2026-07-06) —** τ-Voice reports **pass@1 only** — the paper defines
it explicitly as "the proportion of tasks completed successfully on a single attempt" — and does
**not** define or report a pass^k (all-k-trials-pass reliability) metric anywhere in the text
(checked against the full arXiv HTML, 2603.13686v1: no mention of multi-trial reliability). *An
earlier draft of this entry claimed τ-Voice reports pass@1 **and** pass^k; that claim was
unsupported by the source and has been corrected.* τ-Voice therefore does **not** nuance the L4
archive's N1 ("no published pass@k / best-of-N / oracle-over-sampling measurement on any
voice-agent benchmark") — it simply doesn't measure in that family. EVA-Bench (item 2 below) remains
the sole benchmark in this lane that defines **and** populates a pass@k/pass^k oracle-over-sampling
metric with real numbers.

**(5) Fence tag.** single-session. **(6) Omni role.** hybrid (the audio-native agent under test both
perceives (sensor) and decides/acts (brain) in one frozen model, or splits across a cascade).

**Sources:** [τ-Voice: Benchmarking Full-Duplex Voice Agents on Real-World Domains](https://arxiv.org/abs/2603.13686) (2026-03, arXiv 2603.13686) · [τ-Voice HTML](https://arxiv.org/html/2603.13686v1). **Delta vs L4:** CONFIRMS C01 (same paper, same numbers: GPT-5 text 85% pass@1 vs voice 26–51%).

## 2. EVA-Bench — end-to-end voice-agent task-success + user-experience framework

**(1) Recognized problem.** Existing voice-agent evals either measure task completion (DB-diff) OR
subjective conversational quality, never jointly, and never with an explicit reliability metric —
so a system's "peak" demo performance can silently hide unreliable typical-case behavior.

**(2) Genealogy.** Origin-domain: **speech**, built by ServiceNow-AI (confirmed via HF org match:
on-disk source is HF `ServiceNow-AI/eva`, `docs/data.md` line 124). Transfer status: native
(automated bot-to-bot audio-conversation harness purpose-built for voice agents), though its
task-completion metric is a direct descendant of τ-bench/τ²-bench's DB-diff idea (ported from LLM
origin).

**(3) Training-free vs. fine-tuned.** Evaluates 12 frozen systems across 3 architectures (7 cascade,
2 hybrid, 3 speech-to-speech) — no weight updates in the loop.

**(4) Three-axis class + verdict.** This is the clearest concrete instance of the framework's
**verifier fork** anywhere in this lane: **Task Completion** = a deterministic SHA-256 hash
comparison of final scenario-DB state vs. gold (**verifier-as-tool / element**, no LLM in the
scoring loop) vs. **Faithfulness** (policy adherence/tool-grounding) and **Conversation
Progression/Conciseness** = **LLM-as-Judge** and **LALM-as-Judge** (**verifier-as-role / usage-pattern,
weak per this survey's thesis**). **Verdict: NEW, and important —** EVA-Bench (verified verbatim,
Section 4.1 / Appendix A) runs **k=5 trials per scenario under clean conditions and k=3 under
perturbation** across 213 scenarios (airline, healthcare-HR, IT-service) and reports real **pass@1 /
pass@k ("≥1 of k trials passes," ceiling) / pass^k ("all k trials pass," reliability)** numbers with
confidence intervals — e.g. top system GPT-Realtime-1.5: EVA-A pass@1 0.467, pass@k 0.710±0.061,
pass^k 0.283±0.056. **This is a genuine oracle-over-sampling measurement on a voice-agent
benchmark, populated with real numbers** — it directly refutes the letter of the L4 archive's
negative N1 ("no published pass@k / best-of-N / oracle-over-sampling measurement on any
voice-agent benchmark," re-confirmed empty by L4's verifier on 2026-07-04). Because EVA-Bench's
arXiv id (2605.13841 → May 2026) predates that 2026-07-04 verification pass, this reads as a **miss
in the prior sweep rather than a genuinely new paper** — worth flagging back to the L4 lane owner
for a correction, since it changes the "condition (a) is an unoccupied measurement cell" claim from
absolute to "the metric now exists and is measured, but no one has yet used it to *select* — i.e.
best-of-N is measured as a ceiling, not exploited as an inference-time RL policy."

**(5) Fence tag.** single-session (each of the 213 scenarios is one bot-to-bot conversation with no
persistence across scenarios). **(6) Omni role.** hybrid across the evaluated systems (cascade
architectures split sensor/brain across separate ASR+LLM+TTS models; the 3 speech-to-speech systems
are single frozen omni models doing both).

**Sources:** [EVA-Bench: A New End-to-end Framework for Evaluating Voice Agents](https://arxiv.org/abs/2605.13841) (2026-05, arXiv 2605.13841) · [HTML](https://arxiv.org/html/2605.13841v1) · [ServiceNow-AI/eva HF blog](https://huggingface.co/blog/ServiceNow-AI/eva). On-disk: `docs/data.md` line 124, HF `ServiceNow-AI/eva`. **Delta vs L4:** REFUTES (qualified, see above) N1's "no pass@k measurement" claim; CONFIRMS L4's P1 task-completion-collapse pattern (no system exceeds 0.5 on both EVA-A and EVA-X pass@1 jointly).

## 3. SoulX-Duplug / SoulX-Duplug-Eval — full-duplex turn-taking state-prediction

**(1) Recognized problem.** Full-duplex spoken dialogue needs a turn-taking/state-prediction
front-end; naive VAD is too crude (no semantic understanding) and running a full dialogue LLM on
every audio chunk is too slow for streaming.

**(2) Genealogy.** Origin-domain: **speech** (native). Transfer status: native — SoulX-Duplug
introduces a plug-and-play streaming module (text-guided: it first runs streaming ASR, then uses
that transcript to predict 5 dialogue-state tokens: user idle/non-idle, backchannel,
semantic-completeness), evaluated on **SoulX-Duplug-Eval**, which extends Full-Duplex-Bench with
better bilingual (EN/ZH) coverage.

**(3) Training-free vs. fine-tuned.** The module itself is a small trained component (not
training-free), but it is designed to be **added in front of a frozen dialogue LLM without
retraining that LLM** — i.e., it is a genuine new connector/element bolted onto an otherwise-frozen
brain, not a change to the brain's weights.

**(4) Three-axis class + verdict.** The *eval harness* (SoulX-Duplug-Eval) is a **constraint**
instrument — it operationalizes exactly the framework's "real-time/full-duplex is a
base-architecture/inference-substrate property" claim, with four measurable interaction scenarios:
Turn-Taking (155 samples), Pause Handling (239), User Backchannel (199), User Interruption (161),
plus a bilingual Easy-Turn set (318 complete / 299 incomplete EN utterances). The *module under
test* is best read as a new **element** (a semantic-VAD connector) — **Verdict: CONFIRMS** the main
thesis's element/constraint split: crossing the full-duplex-turn-taking capability boundary here
comes from adding a genuinely new small perception component (a connector), not from prompting the
existing dialogue LLM differently.

**(5) Fence tag.** single-session (turn-taking decisions are made per-utterance/per-conversation,
no cross-session accumulation). **(6) Omni role.** **sensor** (it is explicitly a front-end
streaming state predictor / semantic VAD feeding a separate downstream dialogue brain, not the
reasoning component itself).

**Sources:** [SoulX-Duplug: Plug-and-Play Streaming State Prediction Module for Realtime Full-Duplex Speech Conversation](https://arxiv.org/abs/2603.14877) (2026-03, arXiv 2603.14877) · [HTML](https://arxiv.org/html/2603.14877v1) · [Soul-AILab/SoulX-Duplug-Eval (HF dataset)](https://huggingface.co/datasets/Soul-AILab/SoulX-Duplug-Eval). On-disk: `docs/data.md` line 122. **Delta:** NEW (not previously in the archive under this name).

## 4. AudioMC / Audio MultiChallenge — multi-turn instruction retention

**(1) Recognized problem.** Existing spoken-dialogue evals use short, synthetic-TTS, clean-speech
interactions; none test whether E2E spoken systems retain instructions, prior context, and
self-consistency across *natural, human, disfluent* multi-turn conversation — the everyday failure
mode of production voice assistants.

**(2) Genealogy.** Origin-domain: **LLM** (built on Scale AI's text MultiChallenge framework, which
scores Inference Memory / Instruction Retention / Self-Coherence). Transfer status: **ported** to
audio, adding a new axis (**Voice Editing** — robustness to mid-utterance speech repairs/backtracking)
and an audio-specific "Audio-Cue" variant of Inference Memory (recalling ambient sound/paralinguistic
cues, not just semantic content) that has no text analog.

**(3) Training-free vs. fine-tuned.** Evaluates frozen commercial and open E2E systems (both
speech-to-speech and audio-input) — no gradient step.

**(4) Three-axis class + verdict.** Scoring is via **1,712 instance-specific rubrics** over 452
human conversations (47 speakers) — this is a hybrid measurement design (per-instance rubrics
suggest structured/graded judgment, likely LLM-assisted rather than a single global judge), so it
sits closer to **usage-pattern-adjacent measurement** (multi-turn orchestration/context retention)
but its key finding cuts the other way: **performance degrades with cumulative audio duration, not
with turn count** ("model performance remains stable across 3–8 turns... degrades steadily as total
duration of user audio increases"). **Verdict:** this is evidence *against* a naive usage-pattern
story (more turns = more orchestration failure) and *for* classifying long-audio-context robustness
as a **constraint** (perception-fidelity / context-length property of the model), i.e. NEW evidence
refining where the real bottleneck sits.

**(5) Fence tag.** single-session (each conversation, however long, is one self-contained episode;
no cross-conversation memory tested). **(6) Omni role.** hybrid.

**Sources:** [Audio MultiChallenge: A Multi-Turn Evaluation of Spoken Dialogue Systems on Natural Human Interaction](https://arxiv.org/abs/2512.14865) (2025-12, arXiv 2512.14865) · Scale AI leaderboard pages (`labs.scale.com/leaderboard/audiomc*`, `scale.com/blog/audiomc` — found via WebSearch, domain not directly fetchable this session due to a network policy block, so treated as corroborating-only, not load-bearing). On-disk: `docs/data.md` line 118, HF `ScaleAI/audiomc`. **Delta vs L4:** CONFIRMS L4's C12 (same paper, "54.65% pass rate," Self-Coherence degrading with longer audio context) — L4 already has this under P3/C12; this lane adds the duration-vs-turn-count nuance and the rubric-count/speaker-count detail.

## 5. VoiceAssistant-Eval — listening/speaking/viewing omni-assistant benchmark

**(1) Recognized problem.** No benchmark jointly covered audio *and* visual perception with the
speaking-specific concerns (roleplay voice imitation, safety, personalization) that a true
"omni" assistant needs; prior work siloed ASR/TTS-style eval from agentic/persona eval.

**(2) Genealogy.** Origin-domain: **speech/mixed** (VLM-adjacent — the "Viewing" axis pulls in
multi-disciplinary image understanding, so this benchmark is itself a small-scale test of VLM→omni
transfer). Transfer status: native construction, 10,497 curated examples across 13 categories
(4 Listening, 8 Speaking, 1 Viewing).

**(3) Training-free vs. fine-tuned.** Evaluates 21 open-source models plus GPT-4o-Audio, all
frozen.

**(4) Three-axis class + verdict.** **Constraint** — this benchmark is a direct operationalization
of two constraints this survey's framework names explicitly: **perception fidelity** (Listening +
Viewing) and **alignment/safety** (a dedicated Safety task, explicitly called out as "cross-cutting"
in the organizing framework). **Verdict:** its own results CONFIRM the framework's claim that safety
and persona-consistency are cross-cutting constraints that don't track general capability: safety
performance is highly size-dependent (Qwen2.5-Omni-7B 71.9% vs. smaller models <50%), and roleplay
voice-imitation is uniformly hard (GPT-4o-Audio leads at 13.72 on some scale, most open models <6) —
i.e., neither is fixed by "more model," consistent with a distinct-constraint reading rather than a
side-effect of the reasoning/perception elements improving.

**(5) Fence tag.** single-session. **(6) Omni role.** hybrid (listening=sensor, viewing=sensor,
speaking/reasoning=brain — evaluated jointly).

**Sources:** [VoiceAssistant-Eval: Benchmarking AI Assistants across Listening, Speaking, and Viewing](https://arxiv.org/abs/2509.22651) (2025-09, arXiv 2509.22651) · [project site](https://mathllm.github.io/VoiceAssistantEval/) · [HTML](https://arxiv.org/html/2509.22651v1). On-disk: `docs/data.md` line 117, HF `MathLLMs/VoiceAssistant-Eval` (matches `docs/datasets.lock.json` hf_id exactly — CONFIRMS on-disk identity). **Delta:** NEW to this lane (not in L4, which is agentic-task-focused rather than assistant-capability-focused).

## 6. VoiceBench — multi-faceted LLM voice-assistant benchmark

**(1) Recognized problem.** Prior voice-assistant evals were narrow (ASR accuracy or clean-speech
general knowledge only), ignoring realistic speaker/environment/content variation and giving no
unified multi-task view.

**(2) Genealogy.** Origin-domain: **LLM** (each subset is a spoken-audio port of an existing text
benchmark family: AlpacaEval, CommonEval, IFEval, BBH, AdvBench). Transfer status: **ported**
(TTS-synthesized or human-recorded spoken versions of text benchmarks).

**(3) Training-free vs. fine-tuned.** Evaluates 41 frozen models across 5 architecture classes
(Cascaded, Audio-LLM, Vision+Audio+LLM, Omni, S2S/full-duplex).

**(4) Three-axis class + verdict.** VoiceBench is the cleanest single instance in this lane of the
**verification fork co-existing within one benchmark**: MCQ subsets (mmsu, openbookqa) use
**exact-match** scoring and AdvBench uses a **rule-based harm/refusal classifier** — both
**verifier-as-tool (element)** — while open-ended subsets (alpacaeval_full, commoneval, wildvoice)
use **GPT-4o-mini as an LLM judge** — **verifier-as-role (usage-pattern), the weak fork per this
survey's thesis**. **Verdict:** CONFIRMS the fork's existence as a real, already-adopted design
choice (not a hypothetical), though the *leaderboard results* complicate a simple
"cascade-always-wins" story: NVIDIA Nemotron-3-Nano-Omni-30B-A3B (a unified omni model, 89.39
overall) tops the public leaderboard just ahead of a Whisper-v3-large+GPT-4o cascade (87.80) and
well ahead of GPT-4o-Audio (86.75) — while a different omni model, Qwen2-Audio, lags far behind at
55.80 (#29). **This is a NEW negative/caveat:** the cascade-beats-omni pattern found on VocalBench
(item 8 below) is not universal — it is architecture/model-specific, not a fixed property of
"cascade = added elements always wins."

**(5) Fence tag.** single-session. **(6) Omni role.** hybrid.

**Sources:** [VoiceBench: Benchmarking LLM-Based Voice Assistants](https://arxiv.org/abs/2410.17196) (2024-10, arXiv 2410.17196; TACL'26) · [matthewcym/voicebench (GitHub)](https://github.com/matthewcym/voicebench) · [leaderboard](https://matthewcym.github.io/VoiceBench/). On-disk: `docs/data.md` line 116, ModelScope. **Delta:** CONFIRMS L4's C04 (cascade-beats-open-source finding, same paper); adds the NEW leaderboard nuance (Nemotron omni model topping the board) that L4 did not capture.

## 7. URO-Bench — Understanding/Reasoning/Oral-conversation S2S benchmark

**(1) Recognized problem.** No S2S benchmark jointly covered multilingualism, multi-round dialogue,
and paralinguistics, or explicitly measured whether speech fine-tuning erodes a backbone LLM's
pre-existing instruction-following/reasoning.

**(2) Genealogy.** Origin-domain: **mixed** (Understanding/Reasoning subsets port LLM-style QA/IFEval-
style tasks; Oral-conversation is speech-native paralinguistics). Transfer status: **ported** +
**native**. Two difficulty tiers (basic/pro), 20 test sets each, EN+ZH paired (40 datasets total,
plus a 1,000-sample URO-Bench-mini for quick iteration).

**(3) Training-free vs. fine-tuned.** The systems under test (GLM-4-Voice, Freeze-Omni, LLaMA-Omni,
etc.) are **fine-tuned** SDMs — speech-modality-adapted versions of a text backbone, i.e. exactly
the weight/structure-changing family this survey's thesis is positioned against, contrasted against
a **training-free cascade baseline** (Whisper ASR → frozen GPT-4o).

**(4) Three-axis class + verdict.** Scoring mixes WER/CER (ASR-native element check), UTMOS (speech
quality, model-quality constraint), and GPT-based judge/binary-accuracy scoring per task (usage-
pattern-adjacent for open tasks, element-like exact-match for closed tasks). **Verdict — the
strongest single finding in this lane for the training-free thesis:** the training-free
Whisper+GPT-4o cascade baseline scores **89.33 (EN) / 79.27 (ZH)** overall, well above the *best
fine-tuned* end-to-end SDM, GLM-4-Voice (**69.09 EN / 66.90 ZH**), with weaker fine-tuned models
(Freeze-Omni 48.28, LLaMA-Omni 48.14) further behind still; and open-source SDMs "lag behind their
backbone LLMs in terms of instruction-following ability and also suffer from catastrophic
forgetting." This is direct evidence that **fine-tuning to fuse a new modality can degrade or
destroy a pre-existing element (the backbone's reasoning/instruction-following) rather than cleanly
adding a new one**, while **chaining two untouched frozen elements (ASR + text LLM) training-free
preserves both** — a CONFIRMS of this project's overall training-free framing, independent of the
element/usage-pattern axis narrowly construed.

**(5) Fence tag.** single-session. **(6) Omni role.** hybrid for the fine-tuned SDMs; the cascade
baseline splits sensor (Whisper) from brain (GPT-4o) as two separate frozen elements.

**Sources:** [URO-Bench: Towards Comprehensive Evaluation for End-to-End Spoken Dialogue Models](https://arxiv.org/abs/2502.17810) (2025-02, arXiv 2502.17810; EMNLP Findings 2025) · [Ruiqi-Yan/URO-Bench (GitHub)](https://github.com/Ruiqi-Yan/URO-Bench) · [HF dataset Honggao/URO-Bench](https://huggingface.co/datasets/Honggao/URO-Bench). On-disk: `docs/data.md` line 115, HF `Honggao/URO-Bench` (matches lock-file `hf_id` — CONFIRMS on-disk identity). **Delta:** CONFIRMS L4's P2/C04 (URO-Bench catastrophic-forgetting quote is already archived verbatim); this lane adds the specific EN/ZH numeric leaderboard (GLM-4-Voice 69.09/66.90, cascade reference 89.33/79.27) that L4 did not tabulate.

## 8. VocalBench (+ VocalBench-zh) — vocal conversational-ability benchmark

**(1) Recognized problem.** Existing speech-interaction evals score only the *textual content* of
responses (via ASR-then-text-judge), ignoring vocal-specific performance: acoustic quality, emotional
empathy, robustness to noise/reverberation, and speech-instruction-following (e.g. "answer in a
whisper").

**(2) Genealogy.** Origin-domain: **speech** (native construction; **9,400** instances across 4
dimensions — Semantic, Acoustic, Chat/conversational, Robustness — per the original May-2025
preprint (v1); the paper was revised in January 2026 (v3) and the abstract now live at the cited
arXiv page states **~24,395 ("around 24k")** instances, so a reader following the link today sees
the larger, current count rather than 9,400 — flagged by verifier, 2026-07-06, not corrected
in-place since 9,400 is what the benchmark reported at its original release). Transfer status: native, with a
same-team Mandarin port (**VocalBench-zh**, arXiv 2511.08230 — 10 subsets, >10K instances, 12
user personas, 14 models evaluated) — an explicit EN→ZH ported extension.

**(3) Training-free vs. fine-tuned.** Evaluates 20+ frozen models across tiny/base/large scale
tiers, plus a "Cascade(GPT-4o)" configuration.

**(4) Three-axis class + verdict.** **Element** — the leaderboard is the clearest positive evidence
in this lane *for* the main thesis's "new element crosses the boundary" reading: **Cascade(GPT-4o)
achieves the top overall score (82.68%)**, ahead of the unified omni model **Qwen3-Omni (78.78%)**
and **VocalNet2-8B (76.63%)**. Since a cascade is literally chaining in *separate, specialized*
ASR and TTS elements around a frozen text brain (rather than relying on one frozen omni brain to do
sensing, reasoning, and vocalizing itself), this is direct evidence that **adding distinct
high-fidelity element components (specialized connectors) still beats a single integrated frozen
omni brain**, on this benchmark's mix of semantic/acoustic/robustness axes. **Verdict:** NEW,
supports the main thesis, but must be read alongside VoiceBench's leaderboard (item 6), where the
opposite ranking holds for a different unified omni model (Nemotron) vs a different cascade — i.e.
the "cascade > omni" pattern is real but **not universal**, and is sensitive to which specific
models are compared.

**(5) Fence tag.** single-session. **(6) Omni role.** hybrid across the leaderboard (cascade entries
split sensor/brain; omni entries are hybrid single-model).

**Sources:** [VocalBench: Benchmarking the Vocal Conversational Abilities for Speech Interaction Models](https://arxiv.org/abs/2505.15727) (2025-05, arXiv 2505.15727) · [SJTU-OmniAgent/VocalBench (GitHub)](https://github.com/SJTU-OmniAgent/VocalBench) · [VocalBench-zh](https://arxiv.org/abs/2511.08230) (2025-11, arXiv 2511.08230). On-disk: `docs/data.md` lines 119–120, HF `VocalNet/VocalBench` + `VocalNet/VocalBench-zh` (matches lock-file). **Delta:** NEW to this lane (not previously archived in L4, which predates a detailed VocalBench leaderboard read).

## Cross-cutting observations

**A. The verification fork (element vs. usage-pattern verifier) is already a live, adopted design
choice, not just a hypothesis.** Three of the eight benchmarks explicitly mix a deterministic/
rule-based verifier (**verifier-as-tool**) with an LLM-judge verifier (**verifier-as-role**) *within
the same instrument*: EVA-Bench (Task Completion hash-diff vs. Faithfulness LLM-judge), VoiceBench
(MCQ exact-match/AdvBench rule-classifier vs. GPT-4o-mini judge on open-ended subsets), and
τ²-bench/τ-Voice (DB-diff reward vs. LLM-simulated user role). This gives concrete, citable grounding
for the survey's "verification forks" clause rather than a purely theoretical distinction.

**B. Architecture (cascade vs. unified omni) is a recurring but non-universal fault line.**
VocalBench: cascade(GPT-4o) beats unified omni (Qwen3-Omni). VoiceBench: a unified omni model
(Nemotron-3-Nano-Omni) tops the board just ahead of a cascade, while a different omni model
(Qwen2-Audio) trails badly. URO-Bench: a training-free cascade (Whisper+GPT-4o) beats every
fine-tuned end-to-end SDM by a wide margin. EVA-Bench: cascade and speech-to-speech systems fail
*differently* (cascades degrade more under accents; S2S degrades more under noise) rather than one
architecture dominating. **Reading:** "does capability come from adding a separate specialized
element vs. relying on one frozen omni's own usage of its perception+reasoning" is empirically
contested and model-specific — a caution against overgeneralizing either direction of the main
thesis from any single leaderboard.

**C. Empty measurement cell — cross-session accumulation.** None of the eight benchmarks test
**cross-session** memory/skill accumulation (fence tag: all eight are single-session). Even the
explicitly "multi-turn" ones (AudioMC, τ²-bench, URO-Bench, EVA-Bench) reset all state between test
items/scenarios; AudioMC's turns are within one continuous conversation, not across separate
sessions. This CONFIRMS the prior archive's S1 finding (no-gradient self-improvement / compounding
memory mature in text/embodied agents, not in speech) at the level of the *evaluation
infrastructure itself*: as of 2026-07, the speech-agent benchmark landscape has not yet built the
harness that would even let a cross-session, curated-memory method be scored.

**D. EVA-Bench's k=5/k=3-trial pass@k / pass^k results (item 2) are the most important single delta
in this lane** — they show a genuine oracle-over-sampling measurement now exists and is populated
with real numbers on a voice-agent benchmark, which the prior L4 archive's negative N1 states does
not exist (as of a 2026-07-04 verification pass). Recommend the L4 lane owner re-run N1's search
including "EVA-Bench" and "ServiceNow-AI/eva" explicitly, since this benchmark's own arXiv id
(2605.13841) predates that verification date.

## Negatives / empty cells (first-class)

- No benchmark in this lane runs an actual **best-of-N selection experiment** (choosing the best of
  N sampled rollouts via a reward model or self-consistency and reporting the *achieved* accuracy
  lift) — **EVA-Bench** measures the pass@k/pass^k *ceiling* (what an oracle *could* achieve; verified
  numbers, item 2) but no one has yet built a training-free selector that *reaches* that ceiling on
  these specific benchmarks. (τ-Voice, corrected above, reports single-attempt pass@1 only — it is
  not a multi-trial oracle metric and does not belong in this ceiling-measured set.) This narrows
  (but does not close) L4's N1.
- No cross-session / same-speaker accumulating benchmark exists among these eight (see C above) —
  consistent with L4's closure-fence N5 and the prior archive's S1.
- No published prompt-optimization (APE/GEPA-class) result was found run against any of these eight
  benchmarks specifically during this lane's search (consistent with L4's N2, not independently
  re-verified beyond a repeat of the same search terms — treat as a repeat-confirmation, not a fresh
  finding).

## Verifier notes (2026-07-06)

Adversarial pass over this lane: re-fetched the arXiv abstract (and, for the higher-stakes claims,
the full HTML) for all 8 primary sources, plus the ServiceNow-AI HF blog, the VoiceBench and
VocalBench leaderboards/GitHub repos, and the VoiceAssistant-Eval project site; cross-checked the
TACL'26 and EMNLP-2025-Findings venue tags by web search since arXiv abstract pages don't surface
venue acceptance for these two.

**Confirmed accurate (no changes needed):** τ²-bench (2506.07982, dual-control/Dec-POMDP, domains
list matches, GitHub repo confirms telecom/retail/airline); EVA-Bench (2605.13841, ServiceNow
Research affiliation confirmed via the paper's own correspondence address *and* the HF blog, 213
scenarios, k=5 clean/k=3 perturbation, and the exact GPT-Realtime-1.5 pass@1/pass@k/pass^k numbers
all verified verbatim); SoulX-Duplug (2603.14877, module + SoulX-Duplug-Eval sample counts and the
explicit "Full-Duplex-Bench" extension claim all verified verbatim); AudioMC (2512.14865, rubric/
speaker/conversation counts and the duration-not-turn-count finding verified verbatim); VoiceBench
(2410.17196, TACL'26 acceptance confirmed via MIT Press TACL page and the GitHub repo's own
"[TACL'26]" tag; full leaderboard incl. Nemotron-3-Nano-Omni 89.39, Whisper+GPT-4o cascade 87.80,
GPT-4o-Audio 86.75, Qwen2-Audio 55.80/#29 all verified verbatim on the live leaderboard); URO-Bench
(2502.17810, EMNLP 2025 Findings acceptance confirmed by web search); VoiceAssistant-Eval
(2509.22651, 10,497/13-category breakdown, Qwen2.5-Omni-7B 71.9% safety score, and GPT-4o-Audio
13.72 roleplay score all verified verbatim on the project site); VocalBench leaderboard numbers
(Cascade-GPT-4o 82.682, Qwen3-Omni 78.775, VocalNet2-8B 76.633) verified verbatim on both the paper
HTML and the GitHub repo.

**Errors found and corrected in place:**
1. **τ-Voice pass^k claim was unsupported (item 1b) — fixed.** The lane originally claimed τ-Voice
   "reports pass@1 (average) and pass^k (reliability across k trials)." The actual paper (arXiv
   2603.13686, abstract and full HTML both checked) defines and reports **only pass@1** ("the
   proportion of tasks completed successfully on a single attempt") and contains no mention of
   pass^k or any multi-trial reliability metric anywhere in the text. This was a materially wrong
   verdict — it inverted the lane's own conclusion that EVA-Bench is the *sole* benchmark in this
   set with a populated oracle-over-sampling metric. Corrected inline (item 1b's verdict paragraph)
   and in the Negatives section (which had also incorrectly listed τ-Voice alongside EVA-Bench as
   measuring a pass@k ceiling).
2. **VocalBench instance count is version-dependent (item 8) — flagged, not overwritten.** The lane
   cites "9,400 instances," which matches the v1 (May 2025) abstract verbatim, but the paper was
   revised in January 2026 (v3) and the abstract now live at the cited arXiv URL states "around 24k"
   (~24,395) instances. A reader clicking through today sees the larger number. Left both figures in
   the entry with an explanation rather than silently swapping one wrong number for another.

**Framework-verdict check (element vs. usage-pattern, new-info vs. read-out):** the eight
per-benchmark verdicts were checked against the "usage pattern over one frozen model = read-out"
rule. All eight hold up: SoulX-Duplug's module is a genuine new trained sub-component bolted onto a
frozen brain (element, not a prompting trick over one frozen model); VocalBench's and URO-Bench's
cascade-beats-single-model findings are read as "separate specialized elements beat one frozen omni
model's own usage of its built-in perception" — correctly on the "element" side, since a cascade by
construction adds components rather than re-prompting one frozen model; the τ²-bench/EVA-Bench/
VoiceBench verifier forks (tool-verifier=element vs. LLM-judge/role-played-user=usage-pattern) are
textbook-correct applications of that split. No verdict was found treating a single frozen model's
differently-prompted behavior as if it were evidence of a new element — the one correction above
(τ-Voice) was a source-fidelity error, not a framework-application error.

**Recency:** 7 of 8 primary papers fall inside 2025-01..2026-07 (Jun 2025 – May 2026). The one
exception, VoiceBench, originally posted 2024-10, predates the window; it is retained because the
*evidence used* (the TACL'26 acceptance and the current 41-model leaderboard, which includes 2025–
2026-era models like GPT-Realtime and Nemotron-3-Nano-Omni) is itself within-window — worth an
explicit caveat that the origin preprint itself is outside the stated recency band. Negatives are
present and substantive (cross-cutting C/D and the closing Negatives section), not pro-forma.

**Not independently re-checked this pass** (lower stakes / already narrow claims, time-boxed):
Scale-AI leaderboard pages for AudioMC (the lane itself already flags these as fetch-blocked and
non-load-bearing); the exact wording of L4's own N1/C02 entries (taken as given from this lane's
citations, not re-opened); the SoulX-Duplug-Eval HF dataset page and the Honggao/URO-Bench,
MathLLMs/VoiceAssistant-Eval, ServiceNow-AI/eva HF dataset pages (on-disk identity match against
`docs/datasets.lock.json` was accepted from the lane's own on-disk citation, not re-fetched).
