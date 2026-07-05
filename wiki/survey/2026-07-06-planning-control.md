---
title: "Stage-1 Survey Lane: Planning / Orchestration / Control for Voice-Omni Agents"
date: 2026-07-06
stage: 1-argumentation
lane: planning-control
---

# Lane: planning-control

**Scope.** Planning/orchestration/control/routing architectures for voice-omni agents (2025–2026):
ReAct / plan-execute / reflexion / multi-agent-debate applied to speech, and specifically whether the
controller is a **text LLM** driving multimodal (audio) tools. Every item is classified on the
three-axis framework and tested against the thesis: *does planning over ONE frozen model ever cross a
capability boundary?* Cross-domain (text-LLM, VLM/GUI) references are included only as genealogy roots
or as the clearest available empirical/theoretical tests of the same question, since **no
speech-specific paper in this search directly ran the controlled "usage-pattern-only" ablation**
(itself a first-class negative — see below).

---

## Claims

### 1. AURA — cascaded ReAct agent, text-LLM controller over frozen speech tools
- **Problem addressed:** give a speech-only interface access to real-world APIs (calendar, email, web
  search) via multi-turn tool use, without any end-to-end speech-agent training.
- **Genealogy:** ReAct (Yao et al. 2022, text/LLM) → **ported natively, unmodified**, into a
  cascaded voice pipeline (ESPnet-OWSM/Whisper-v3 ASR → LLaMA-3.3-70B-Instruct reasoner via vLLM →
  VITS TTS). Origin domain: **LLM**. Transfer status: **ported**.
- **Training-free vs fine-tuned:** fully training-free / prompting-only. All three components (ASR,
  reasoner, TTS) are frozen off-the-shelf models; the "Thought / Action / Payload" ReAct loop is pure
  in-context structuring.
- **Three-axis class:** **usage-pattern** (prompting format over a frozen text LLM that treats ASR/TTS
  as black-box tools). **Verdict:** the paper reports 92.75% OpenBookQA (VoiceBench) and 90% human-rated
  task success, but **provides no ablation against a non-agentic single-call baseline on the same
  LLM** — so whether the gain traces to the ReAct *format* (usage-pattern) or to *tool access itself*
  (an element: APIs the LLM didn't have before) is explicitly unquantified in the paper. This is a
  methodological gap, flagged as a negative finding in its own right.
- **Fence tag:** single-session (per-dialogue ReAct loop; no persistent cross-session memory
  described).
- **Omni role:** **hybrid** — a text-only LLM is the "brain"/controller; ASR is a pure **sensor**;
  no single omni model is used at all (the controller literally never sees raw audio).
- **Delta vs archive:** **NEW** — the first concrete instance in this search of "controller is a text
  LLM, not the omni/audio model," matching the lane's core question directly.
- URL: https://arxiv.org/abs/2506.23049 (HTML: https://arxiv.org/html/2506.23049v1)

### 2. VoxMind — capability-boundary crossing required training, not prompting
- **Problem addressed:** give an *end-to-end* spoken dialogue model (not cascaded) agentic tool-use and
  multi-turn task-completion ability while preserving conversational/paralinguistic quality.
- **Genealogy:** "Think-before-Speak" reasoning-before-response (LLM-domain chain-of-thought pattern)
  + a "Dynamic Tool Management" multi-agent design, **ported** into a native audio→audio model.
- **Training-free vs fine-tuned:** **explicitly fine-tuned** — trained on a curated 470-hour
  "AgentChat" dataset; task completion rises from 34.88% → 74.57% (surpassing Gemini-2.5-Pro on
  spoken-agent tasks) only after this training, not from the "Think-before-Speak" prompting scaffold
  alone.
- **Three-axis class:** the *scaffold* (Think-before-Speak, dynamic tool routing) is a
  **usage-pattern**; the actual **+39.7pp** capability jump is attributed to an **element** (new
  curated training data — the AgentChat corpus that changes the model's weights). **Verdict: crossing
  the boundary here came from an element (training corpus), not the usage pattern.** This is a direct,
  well-quantified data point for the thesis: the architecture/orchestration idea is necessary
  scaffolding but not sufficient; the large gain is training-driven.
- **Fence tag:** cross-session in principle not evaluated; effectively single-session multi-turn.
- **Omni role:** **brain** (the omni model itself reasons, plans, and calls tools end-to-end — no
  separate text-LLM controller).
- **Delta vs archive:** **CONFIRMS** S1 (no-gradient self-improvement mature in text/embodied but not
  speech) and extends it: the paper that DOES cross the boundary in voice-agent task completion is
  precisely one that added training, not one that relies on inference-time orchestration alone.
- URL: https://arxiv.org/abs/2604.15710

### 3. OmniGAIA / OmniAtlas — tool-integrated reasoning over a frozen omni model needed SFT+DPO to move the needle
- **Problem addressed:** benchmark and improve omni-modal (vision+audio+language) agents on
  multi-hop, tool-integrated reasoning tasks (OmniGAIA benchmark).
- **Genealogy:** tool-integrated-reasoning agent loops (LLM domain, e.g. ReAct/Toolformer lineage) +
  DPO preference optimization (LLM domain) → **ported** to an omni-modal foundation agent
  (OmniAtlas, built on Qwen3-Omni).
- **Training-free vs fine-tuned:** OmniAtlas is **fine-tuned** — trajectory-level supervised
  fine-tuning on trajectories synthesized via "hindsight-guided tree exploration," followed by
  **OmniDPO** for fine-grained error correction. Not training-free.
- **Three-axis class:** the underlying "tool-integrated reasoning paradigm with active omni-modal
  perception" is a usage-pattern description, but the reported gain is training-attributed: baseline
  Qwen3-Omni scores **13.3% Pass@1** on OmniGAIA; OmniAtlas reaches **20.8% Pass@1** (+7.5pp
  absolute, ~56% relative) — via SFT+DPO, not prompting alone. For calibration, the strongest
  proprietary model (Gemini-3-Pro) reaches 62.5% Pass@1, so even the trained open agent leaves a huge
  residual gap. **Verdict: gain requires an element (new preference-optimization training on
  synthesized trajectories); pure orchestration/prompting over the frozen checkpoint is not shown to
  suffice for this jump.**
- **Fence tag:** single-session (benchmark tasks are single-episode agentic runs).
- **Omni role:** **brain** (native omni agent doing its own tool-integrated reasoning; no separate
  text controller).
- **Delta vs archive:** **CONFIRMS** the thesis's prediction that a usage-pattern/orchestration-only
  claim ("training-free tool-integrated reasoning") in practice bundles a training step once you read
  past the headline framing.
- URL: https://arxiv.org/abs/2602.22897 (code: https://github.com/RUC-NLPIR/OmniGAIA)

### 4. τ-Voice — end-to-end omni agents self-planning hit a hard ceiling text agents blow past, even under clean audio
- **Problem addressed:** benchmark full-duplex voice agents on the *same* verifiable, tool-using,
  multi-domain tasks as text agents (extends τ²-bench into voice), to isolate the voice-vs-text gap.
- **Genealogy:** τ²-bench (LLM domain, dual-control tool-use benchmark) → **ported** into full-duplex
  voice via a controllable voice user-simulator.
- **Training-free vs fine-tuned:** benchmark paper; evaluates production frozen models
  (GPT-Realtime-1.5, Gemini-Live-2.5/3.1, Grok-voice-agent) with no fine-tuning.
- **Three-axis class / verdict:** these are **end-to-end omni agents planning and acting entirely on
  their own** (no separate text controller) — the purest test of "usage-pattern/self-orchestration
  over one frozen (audio-native) model." Result: **best text agent scores 85%**; voice agents score
  **31–51% under clean audio and 26–38% under realistic audio** on **identical, verifiable
  (DB-state-checked) tasks**. Crucially, the paper finds "the voice-text gap is not purely a speech
  recognition problem — reasoning and grounding challenges persist independently of audio quality,"
  i.e. even where perception is clean, the self-directed omni agent's planning/reasoning under-performs
  the text-LLM baseline by ~35–55pp. **Verdict: no amount of the omni model's own orchestration closes
  this gap — the gap closes only by swapping in a different, stronger base model (an element swap),
  not by better usage of the same one.**
- **Fence tag:** single-session (per-call agent evaluation).
- **Omni role:** **brain** (native audio agents reasoning and acting on their own).
- **Delta vs archive:** **NEW** — sharpens L4's "instruction/reasoning gap" (P2) into a controlled,
  same-task, same-verifier text-vs-voice comparison with exact numbers, and is the single strongest
  piece of evidence in this lane that a usage pattern (self-directed planning) over one frozen omni
  model is bounded well below what a different (text) model reaches on the same task.
- URL: https://arxiv.org/abs/2603.13686 (HTML: https://arxiv.org/html/2603.13686v1)

### 5. Full-Duplex-Bench-v3 — where a text-LLM-controller usage pattern helps, and where a structural constraint (not planning) caps it
- **Problem addressed:** benchmark tool use in full-duplex voice agents under realistic disfluency
  (five disfluency categories) and chained API calls.
- **Genealogy:** cascaded ASR→LLM→TTS pattern (LLM-domain plan-execute over frozen tools) compared
  head-to-head against native end-to-end audio models.
- **Training-free vs fine-tuned:** benchmark of frozen production/open systems, no fine-tuning.
- **Three-axis class / verdict:** the **cascaded (Whisper→GPT-4o→TTS) baseline** — i.e. a **text-LLM
  controller usage pattern** — scores competitively on Easy single-step tasks (**Pass@1 0.639**,
  beating several end-to-end models) but collapses on Hard multi-step tasks (**0.233**) and especially
  self-correction handling (**0.176**, the lowest of all six configurations, vs GPT-Realtime's
  **0.588**). Overall Pass@1: GPT-Realtime 0.600, Gemini-Live-3.1 0.540, Gemini-Live-2.5 0.490,
  Grok 0.430, Ultravox 0.410, Cascaded 0.450. The paper attributes the cascaded system's
  self-correction failure to a **structural/architectural constraint, not a planning deficiency**:
  "Whisper may finalize the original (incorrect) transcription before the user's correction arrives, so
  the downstream LLM has no opportunity for state rollback" — an ASR-finalization/latency constraint
  that no amount of better prompting fixes. **Verdict: this is the clearest case where "usage pattern"
  (text-LLM-controller cascade) measurably helps on a subset of tasks, but the ceiling on the hardest
  slice is set by a base-architecture constraint (real-time/streaming ASR finalization), matching the
  framework's prediction that real-time/full-duplex behavior is a substrate property, not a usage
  pattern.**
- **Fence tag:** single-session.
- **Omni role:** hybrid (cascaded: text-LLM brain + ASR/TTS sensors) vs brain (end-to-end configs),
  compared directly.
- **Delta vs archive:** **NEW** — first controlled same-benchmark comparison found of cascaded
  (text-LLM-controller) vs end-to-end (omni-self-directed) planning, with a mechanistic explanation for
  where each wins/loses.
- URL: https://arxiv.org/abs/2604.04847 (HTML: https://arxiv.org/html/2604.04847)

### 6. From Text to Voice — the usage-pattern/modality "ceiling" is task-complexity-dependent
- **Problem addressed:** convert existing verified *text* tool-calling benchmarks (Confetti,
  When2Call) into controlled audio versions without re-annotating gold labels, to cleanly measure the
  text→voice tool-calling gap.
- **Genealogy:** text tool-calling benchmarks (LLM domain) → **ported** to audio via TTS + speaker/noise
  perturbation, evaluated on 7 omni-modal models.
- **Training-free vs fine-tuned:** benchmark-conversion methodology; evaluates frozen models only.
- **Three-axis class / verdict:** on these single/few-turn, schema-level tool-calling tasks, the
  **text-to-voice gap is only 1.8 points (Qwen3-Omni) to 4.8 points (GPT-Realtime-1.5)** — an order of
  magnitude smaller than τ-Voice's ~35–55pp gap on full multi-turn, multi-domain grounded tasks.
  Failure analysis shows degradations "most often reflect misunderstandings of argument values in the
  speech" (a perception-level issue), not a reasoning collapse. **Verdict:** this is a useful
  counterweight/negative-space finding — it shows the size of the "usage-pattern ceiling" is not fixed;
  it is small for simple, single-shot tool-argument extraction and large for extended, multi-turn,
  policy-constrained agentic tasks (τ-Voice), suggesting the planning/reasoning gap specifically (not
  perception) dominates as task horizon and multi-turn state-tracking increase.
- **Fence tag:** single-session.
- **Omni role:** sensor+brain evaluated jointly (omni models processing audio directly); no
  cascaded/hybrid variant tested in this paper.
- **Delta vs archive:** **NEW** — a dose-response data point (small gap on short-horizon structured
  tool calls vs large gap on long-horizon agentic tasks) refining L4's P1/P2 problems with quantified
  granularity.
- URL: https://arxiv.org/abs/2605.15104

### 7. EVA-Bench — orchestration/agentic voice systems show peak performance that does not compound into reliable performance
- **Problem addressed:** end-to-end evaluation of voice agents' task completion AND conversational
  experience together, across pass@1 / pass@k / pass^k (reliability) metrics.
- **Genealogy:** agent-benchmark methodology (LLM domain: pass@k reliability framing) ported to voice.
- **Training-free vs fine-tuned:** benchmark of 12 frozen production/open systems.
- **Three-axis class / verdict:** across 12 systems, **no system exceeds 0.5 on both EVA-A (accuracy)
  and EVA-X (experience) pass@1 simultaneously**, and the **median gap between peak (pass@k) and
  reliable (pass^k) performance is 0.44** on EVA-A. This is a first-class negative/empty-cell finding
  for planning-control: whatever orchestration/agentic scaffolding these systems use internally, it
  produces occasional success (peak) without turning into **consistent, repeatable** task completion —
  exactly the failure mode the archive's S1 flags as missing "compounding" infrastructure (curated
  memory + credit assignment), now measured directly on voice agents specifically.
- **Fence tag:** single-session (pass@k measured within repeated single-episode trials, not
  cross-session accumulation).
- **Omni role:** n/a (benchmark; evaluates whichever role each system uses internally).
- **Delta vs archive:** **CONFIRMS** S1/N1 (no published reliable pass@k success on a voice-agent
  benchmark) with a concrete, current (2026) number: 0.44 median peak-vs-reliable gap.
- URL: https://arxiv.org/abs/2605.13841 (HTML: https://arxiv.org/html/2605.13841v1)

### 8. LongShOTAgent — a "training-free agent framework" claim decomposes into multiple new elements, not a usage pattern over one model
- **Problem addressed:** omni-modal (video+audio+vision) reasoning and tool use over long videos.
- **Genealogy:** ReAct/orchestrator-agent pattern (LLM domain) ported to omni-modal long-video agents.
- **Training-free vs fine-tuned:** the *orchestration* is training-free/no-fine-tuning (a "compact
  orchestrator," Qwen3-4B, coordinating expert modules with no weight updates).
- **Three-axis class / verdict:** framed by its authors as "training-free," but decomposed it is
  **not a usage pattern over one frozen model** — it is (a) a **separate orchestrator LLM**
  (Qwen3.6-35B-A3B, ~10B active — a MoE agent-coding model, *not* the "compact Qwen3-4B" this claim
  originally and incorrectly stated) distinct from the perception models, (b) multiple **separate
  expert models** (Qwen2.5-VL-32B, Whisper Large-v3, Audio Flamingo 3) each contributing
  modality-specific information the orchestrator alone lacks, and (c) an explicit **retrieval
  element** — a SigLIP-embedding vector database populated once per video, enabling cross-modal
  video-segment retrieval. Every one of these is an **element** (a new model or a new
  information/tool source) under the lane's framework, not an orchestration trick applied to a single
  frozen checkpoint — this structural classification survives verification against the source paper.
  **However, the performance numbers originally logged here were fabricated/misattributed and the
  comparison direction was backwards; see Verifier notes.** Corrected, paper-verified numbers
  (arXiv:2512.16978, Table 2 and §4.1): LongShOTAgent scores the **highest overall score of all 105
  evaluated video-capable models on LongShOTBench, 66.64%**, beating both the strongest closed API
  (**Gemini 3.1 Pro Preview, 55.63%** — not "Gemini-2.5-Flash," which does not appear in the paper)
  and the strongest open-source end-to-end omni model (Qwen3-Omni 30B-Thinking, 64.05%). The
  "38.25% vs Gemini's 40.27% agentic-subset" figures do not exist anywhere in the source paper (40.27
  is a misattributed digit sequence from an unrelated Gemma-3-4B row) and have been removed. The paper
  *does* report an orchestrator ablation (Table 3: standalone single-pass score 27.17–34.22% vs full
  agentic-loop score 47.17–65.69%, Δ +12.95 to +38.52pp, held constant per orchestrator model) — this
  softens but does not fully overturn the "no ablation... is reported" sentence, since that ablation
  still bundles the retrieval/expert-model elements into the "agentic loop" condition and so does not
  isolate orchestration-format-alone from the added elements.
- **Fence tag:** single-session.
- **Omni role:** hybrid (controller = brain; VL/ASR/audio expert models = sensors; retrieval = a
  distinct memory-like element).
- **Delta vs archive:** **NEW / CONFIRMS** the axis-classification distinction itself (this remains an
  element-decomposed system, not a usage-pattern-alone one), but **REVISE vs original logging**: with
  corrected numbers, this is no longer a case of a "training-free" claim quietly underperforming a
  frozen baseline — it is a multi-element (extra models + retrieval), no-fine-tuning system that
  *currently tops the leaderboard*, ahead of the strongest single frozen omni/VLM checkpoint tested.
  That is a data point cutting the other way from a clean "usage-pattern claims are hollow" reading,
  and should be discussed with the owner alongside claim 9 (ThinkOmni) rather than treated as a
  matching confirmation.
- URL: https://arxiv.org/abs/2512.16978 (HTML: https://arxiv.org/html/2512.16978v1)

### 9. ThinkOmni — training-free "guidance decoding" gain traced to a second (reasoning) model, not the omni model reasoning about itself
- **Problem addressed:** lift strong *textual* reasoning ability into omni-modal (audio/vision)
  scenarios without retraining the omni model.
- **Genealogy:** guided/steered decoding techniques (LLM domain) ported to omni-modal LLMs.
- **Training-free vs fine-tuned:** inference-time only for the omni model itself (its weights are not
  updated); however the technique relies on a **separate text-reasoning model** that guides the omni
  model's decoding trajectory — i.e. a second model is introduced as the source of the improved
  reasoning signal.
- **Three-axis class / verdict:** despite the "training-free" framing, this is best classified as
  adding an **element** (a second, text-only reasoning model as controller/guide) rather than a
  usage-pattern manipulation of the single omni model alone. Reported gain: **Qwen2.5-Omni-7B improves
  by +7.9pp on MathVision (to 32.9%)** under ThinkOmni guidance.
- **Fence tag:** single-session.
- **Omni role:** **hybrid** — omni model executes/perceives, but a separate text model supplies the
  reasoning "brain" signal that steers it.
- **Delta vs archive:** **CONFIRMS** the same pattern as claim 8: a second finding of a "training-free"
  headline result whose actual gain source is a second model (an element), not orchestration alone
  over one frozen model.
- URL: https://arxiv.org/abs/2602.23306

### 10. Multi-agent debate over homogeneous (same-weights) agents underperforms isolated self-correction — cross-domain (text) confirmation
- **Problem addressed:** whether unguided multi-agent debate among identical LLM instances improves
  accuracy over simpler baselines (isolated self-correction).
- **Genealogy:** multi-agent debate (LLM domain, native — not a speech/omni transfer; included as the
  clearest available controlled test of "usage pattern over one frozen model," which no speech-domain
  paper in this search directly ran).
- **Training-free vs fine-tuned:** fully training-free; all agents are the *same* frozen model
  (Qwen2.5-7B / Llama-3.1-8B / Ministral-3-8B tested separately, N=10 homogeneous agents each).
- **Three-axis class / verdict:** textbook **usage-pattern** (debate/role orchestration over one
  frozen model, no new information element). **Verdict: does not cross a capability boundary** —
  isolated self-correction beats homogeneous debate at 2.1–3.4× lower token cost for equal-or-lower
  accuracy; failure decomposes into sycophantic conformity (modal adoption up to 85.5%), contextual
  fragility (vulnerability up to 70.0%), and consensus collapse discarding correct answers already
  present in the pool (oracle gap up to 32.3pp). Explicit conclusion: "homogeneous teams without
  structured roles do not benefit from unguided peer exchange."
- **Fence tag:** single-session.
- **Omni role:** n/a (text-only; included as cross-domain reference per the lane's transfer-reference
  allowance).
- **Delta vs archive:** **CONFIRMS** the archive's measured claim ("a same-weights model given a
  critic/verifier prompt never beats plain majority") and generalizes it from a 2-role
  critic/verifier setup to full N=10 multi-round debate.
- URL: https://arxiv.org/abs/2605.00914

### 11. "Debate or Vote" — a formal (martingale) proof that debate over the same model cannot improve expected correctness
- **Problem addressed:** disentangle *why* multi-agent debate (MAD) works when it appears to, across
  seven NLP benchmarks.
- **Genealogy:** multi-agent debate (LLM domain, native); NeurIPS 2025.
- **Training-free vs fine-tuned:** training-free; theoretical + empirical analysis of frozen-model
  ensembles.
- **Three-axis class / verdict:** **usage-pattern**, and uniquely in this lane the claim is backed by
  a **formal proof**, not just an empirical regularity: the authors "prove that [debate] induces a
  martingale over agents' belief trajectories, implying that debate alone does not improve expected
  correctness." Empirically, "Majority Voting alone accounts for most of the performance gains
  typically attributed to MAD" across the seven benchmarks; only "targeted interventions... biasing
  the belief update toward correction" (i.e., adding new, non-uniform information into the update, an
  element-like intervention) meaningfully help. **This is the strongest available formal statement in
  either domain of the thesis's core claim about usage patterns over one frozen model.**
- **Fence tag:** single-session.
- **Omni role:** n/a (text-only; cross-domain reference).
- **Delta vs archive:** **CONFIRMS**, and upgrades the archive's empirical "never beats plain
  majority" observation to a proved martingale result — worth citing in the project's theory track
  (`wiki/Theory-Convergence-and-Constraints.md`) as an existing convergence-style negative result for
  unconstrained usage-pattern iteration.
- URL: https://arxiv.org/abs/2508.17536

### 12. Origin-domain genealogy: text-LLM-controller-over-frozen-perception-tool is a native VLM/GUI-agent pattern, ported into voice by AURA-style systems
- **Problem addressed:** operate a smartphone/mobile UI via a text LLM planner that issues actions
  (tap/swipe) informed by a frozen vision-perception module, without any end-to-end training of a
  unified action model.
- **Genealogy:** AppAgent (Dec 2023) and Mobile-Agent (Jan 2024) establish the **plan-execute loop with
  a text-LLM controller treating perception (screenshots/OCR) as a black-box frozen tool** — the exact
  same shape as AURA's cascaded ReAct voice agent (claim 1), just VLM instead of speech. Origin domain:
  **VLM**. Transfer status into speech: **ported** (AURA, and the cascaded arms of Full-Duplex-Bench-v3
  and industry-standard STT→LLM→TTS production stacks, are the direct speech-domain analogues).
- **Training-free vs fine-tuned:** both AppAgent and Mobile-Agent are training-free/prompting-based
  agent loops over frozen vision/LLM components (AppAgent also supports an optional "autonomous
  exploration" self-generated documentation phase, itself a memory/skill element rather than a
  planning-format change).
- **Three-axis class:** **usage-pattern** (plan-execute/ReAct loop). Verdict on boundary-crossing:
  outside this lane's direct evidence, but its citation matters for genealogy-tagging: it establishes
  that "text LLM as controller/brain, frozen multimodal model as sensor/tool" is not a speech-specific
  invention — it is the dominant GUI-agent design pattern from 2023–2024, carried into voice largely
  unchanged in 2025–2026 (AURA, industry cascaded stacks).
- **Fence tag:** single-session.
- **Omni role:** hybrid (text-LLM brain + vision-perception sensor) — the VLM-domain precedent for
  the same hybrid role split seen in speech (claim 1, 5).
- **Delta vs archive:** **NEW** (genealogy root not previously logged in the archive for this lane).
- URLs: https://arxiv.org/abs/2312.13771 (AppAgent), https://arxiv.org/abs/2401.16158 (Mobile-Agent)

### 13. τ²-bench — the verifiable "verifier" in these benchmarks is an external DB/tool (an element), not a model role
- **Problem addressed:** measure agent tool-use correctness and reliability against real, mutable
  backend state (retail/airline/telecom), not an LLM's self-assessed judgment of its own output.
- **Genealogy:** original τ-bench (2024, LLM domain, root) → τ²-bench (2025, dual-control environment)
  → **ported** into voice as the substrate for τ-Voice (claim 4) and Full-Duplex-Bench-v3 (claim 5).
- **Training-free vs fine-tuned:** benchmark/evaluation methodology, model-agnostic.
- **Three-axis class / verdict:** this is the paper-level instantiation of the framework's
  "verifier-as-tool vs verifier-as-role" fork: pass/fail is decided by **checking actual database
  state** after the agent's tool calls — an external, ground-truth **element** (the environment/DB) —
  never by asking a same-weights model to judge its own or a peer's output. This is exactly why
  τ²-bench-derived voice benchmarks (τ-Voice, Full-Duplex-Bench-v3) produce trustworthy,
  non-self-referential pass@k numbers, in contrast to the fragile "critic/verifier prompt" usage
  pattern shown to fail in claims 10–11.
- **Fence tag:** single-session (benchmark methodology; each task episode independently verified).
- **Omni role:** n/a (evaluation infrastructure/tool, not a model).
- **Delta vs archive:** **CONFIRMS** the archive/framework's verifier fork distinction, giving it a
  concrete, on-disk benchmark instantiation (this project already owns tau2-bench for eval lanes).
- URL: https://arxiv.org/abs/2506.07982 (τ²-bench); root: https://arxiv.org/abs/2406.12045 (τ-bench,
  2024)

---

## Negatives / empty-measurement-cells (first-class)

- **No speech-domain paper found in this search runs the clean ablation the thesis needs**: "same
  frozen omni/speech model, usage-pattern (ReAct/plan-execute/debate/reflexion) ON vs OFF, no added
  tools/retrieval/second-model, on a verifiable voice-agent benchmark." AURA (claim 1) is the closest
  candidate and explicitly lacks this ablation. This gap itself matches archive negatives N1/N2 (no
  published pass@k / prompt-opt result on a voice-agent benchmark) and should be logged as a candidate
  Stage-1→Stage-2 experiment design (cheap, directional-only) for W1/W4.
- **Every clearly-quantified "training-free agent" gain found in the omni-modal space (LongShOTAgent,
  ThinkOmni) decomposes into an added element** (second controller model, retrieval, external tools)
  on closer reading, despite "training-free" headline framing — none isolates a pure usage-pattern
  effect over one frozen model with all else held constant. **Caveat added at verification:** for
  LongShOTAgent specifically, correcting the previously-fabricated performance numbers (see claim 8
  and Verifier notes) shows this particular element-decomposed system is not a marginal or losing
  claim — it is the *top-scoring* system on its benchmark, ahead of the strongest frozen omni/VLM
  baseline tested. The structural point (real gain = added elements, not usage-pattern-alone) still
  holds, but the "training-free headline overstates itself" framing should not be read as implying the
  underlying system underperforms — it currently does not.
- **Every clearly-quantified *large* capability-boundary crossing found in agentic voice/omni systems
  (VoxMind +39.7pp, OmniAtlas +7.5pp) required fine-tuning** (SFT/DPO on curated trajectories), not
  prompting/orchestration alone — consistent with, and sharpening, the thesis.
- **Cascaded (text-LLM-controller) vs end-to-end (self-directed omni) architecture comparison on
  identical benchmarks exists in only one paper found** (Full-Duplex-Bench-v3, claim 5); τ-Voice
  (claim 4) evaluates only end-to-end systems and explicitly flags the cascaded comparison as *future
  work*. This is a real empty cell: the field has not yet published a broad, controlled cascaded-vs-
  end-to-end comparison on the project's specific on-disk benchmarks (tau2-bench, eva-bench,
  soulx-duplug, audiomc, voiceassistant-eval, voicebench, uro-bench, vocalbench).

---

## Verifier notes (adversarial pass, 2026-07-06)

**Method:** WebFetch against the arXiv abstract/HTML/PDF pages for every claim (PDF tables cross-checked
via `pdftotext -layout` + grep when abstract text was insufficient), covering all 13 claims' primary
URLs (14 distinct arXiv IDs) plus both genealogy-root URLs.

**Confirmed accurate on close inspection** (numbers/quotes verified against full text, not just the
abstract summary): claim 1 AURA (title/authors/92.75%/90%, LLaMA-3.3-70B-Instruct/OWSM+Whisper-v3/VITS
components, and the "no ReAct-vs-single-call ablation" negative finding — all confirmed verbatim);
claim 2 VoxMind (title/authors/34.88%→74.57%/470h AgentChat/ACL 2026); claim 3 OmniGAIA/OmniAtlas
(13.3 / 20.8 / 62.5 Pass@1 and the SFT+OmniDPO recipe — confirmed exactly via PDF table, e.g. "Our
approach significantly boosts Qwen-3-Omni from 13.3 to 20.8 (+7.5 absolute)"); claim 4 τ-Voice (85% /
31–51% / 26–38%, and the "not purely a speech recognition problem" sentence confirmed **verbatim** in
§5.2, plus the 79%/90% agent-behavior-attributed failure breakdown); claim 5 Full-Duplex-Bench-v3
(**every number** — 0.639/0.233 Easy/Hard, 0.176/0.588 self-correction, and the full six-way overall
Pass@1 ranking — confirmed exactly against Tables 2–4, plus the Whisper-finalization quote verbatim);
claim 6 From Text to Voice (1.8/4.8-point gap, Confetti/When2Call, 7 omni models — confirmed); claim 7
EVA-Bench (12 systems, no-system->0.5-on-both, 0.44 median pass@k–pass^k gap — confirmed); claim 9
ThinkOmni (Qwen2.5-Omni-7B 25.0%→32.9% on MathVision, +7.9pp, and the separate-LRM logit-fusion
mechanism — confirmed exactly via full text, correctly classified as an added element); claim 10
homogeneous multi-agent debate (title, N=10 agents, 2.1–3.4×, 85.5%/70.0%/32.3pp, verbatim conclusion
sentence — confirmed); claim 11 Debate-or-Vote (martingale proof, majority-voting-explains-most-of-MAD
finding — confirmed); claim 12 AppAgent/Mobile-Agent (both real, correctly described, appropriately
hedged as genealogy-only); claim 13 τ²-bench (dual-control telecom framing confirmed, and — checked
specifically since the first fetch only surfaced telecom — **retail and airline domains are also
present**, confirmed via full-text search: "Verified Airline and Retail policies," per-domain failure-mode
appendices for both).

**Error found and fixed — claim 8, LongShOTAgent (arXiv:2512.16978).** The original entry's headline
statistics were fabricated/misattributed and the empirical direction was backwards:
- Claimed "44.66% overall" vs actual paper result **66.64%** — which the paper states is the
  **highest score of all 105 evaluated video-capable models** (not an underperforming number).
- Claimed comparator "Gemini-2.5-Flash's 52.95%" — no model named "Gemini-2.5-Flash" appears anywhere
  in the paper; the only Gemini baseline evaluated is **Gemini 3.1 Pro Preview at 55.63%**, which
  LongShOTAgent *beats*, reversing the comparison direction the original claim implied.
- Claimed "agentic-subset tasks 38.25% vs Gemini's 40.27%" — neither figure nor any "agentic subset"
  scoring section exists in the paper; "40.27" traces to an unrelated Gemma-3-4B row in a different
  table (grep-confirmed, no other occurrence).
- Claimed orchestrator "Qwen3-4B (compact)" — the paper's orchestrator LLM is **Qwen3.6-35B-A3B**
  (~10B active parameters), not a 4B model.
- The claim's blanket "no ablation... is reported" is too strong: the paper's Table 3 reports a
  standalone-vs-agentic-loop ablation per orchestrator (Δ +12.95 to +38.52pp) — it does not isolate
  orchestration-format-alone from the bundled retrieval/expert-model elements, so the narrower reading
  survives, but the claim now says so explicitly instead of overstating an absence.
Fixed in place (see claim 8 and the Negatives section above) with paper-verified numbers and an
explicit note that this changes the claim from "a hollow training-free headline" to "a genuine
element-decomposed system that currently tops its leaderboard" — flagged for owner discussion since it
changes the claim's evidentiary valence, not just its numbers.

**Framework-call spot-check (usage-pattern vs. element; new-info vs. read-out):** all 13 verdicts were
re-examined against the "usage pattern over ONE frozen model = read-out" test. No other misclassification
found. Notable defensible edge cases, correctly hedged in the source text itself: claim 1 (AURA) treats
ASR/TTS as tool/sensor I/O rather than as "elements," which is arguable, but the lane explicitly flags
this as an open, unquantified question rather than asserting it — appropriate epistemic hygiene, not an
error. Claim 8's element decomposition (separate orchestrator + separate expert models + retrieval
store) holds up as correctly classified even after the numeric fix.

**Recency:** all 13 primary claims fall inside 2025-01..2026-07 (earliest AURA/Debate-or-Vote 2025-06/08,
latest EVA-Bench/Full-Duplex-Bench-v3/debate 2026-04..05). The two pre-2025 URLs (AppAgent 2023-12,
Mobile-Agent 2024-01) are explicitly scoped as "genealogy roots," per the lane's own stated allowance,
not primary evidence — acceptable.

**Negatives:** the lane's first-class Negatives section is present and substantive (4 distinct
empty-cells/gaps), satisfying the requirement that negatives be included rather than only positive
hits.
