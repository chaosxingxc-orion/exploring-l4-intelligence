# Agentic / tool-use speech — candidate notes (2026-08-17)

Scope note: this family covers human speech carrying linguistic content that maps to a tool
call, an executed action, or a task outcome. General/environmental audio and music benchmarks
are out of scope and were not pursued. Every arXiv identifier below was opened on
`arxiv.org/abs/<id>` and confirmed to resolve to the claimed title; all thirteen supplied IDs
are real. Numbers not retrieved from an official surface are written "not retrieved" rather
than inferred.

Frozen-core context applied to every verdict: the study core is a turn-based llama.cpp server,
not a live full-duplex audio transport, and program spend must stay 0.

---

## Audio2Tool

- **Name / arXiv**: Audio2Tool: Speak, Call, Act — A Dataset for Benchmarking Speech Tool Use,
  arXiv:2604.22821 (v1 2026-04-17, v2 2026-04-28)
- **Official page**: https://audio2tool.github.io/ ; HF `RVtech/Audio2Tool`
- **already-local** (rev f1388da9a3189541ab82adac88824a0661670c43, 10.47 GB, 72,062 files) and
  already integrated in the study repo (`data/audio2tool.py`, `reproduction/a2t_scorer.py`).
- **DATA RELEASED?** Yes, downloadable eval data. HF dataset card enumerates tiers and file
  layout; the study already holds the bytes.
- **Task shape and I/O**: spoken utterance -> predicted structured tool call (tool name +
  argument slots). No execution, no backing database.
- **Evaluation level**: **A** (answer/structure-level). Published metrics are *Tool Accuracy
  (Acc)*, *Exact Match (EM)*, *Slot F1*.
- **Size — RECONCILED DISCREPANCY**:
  - Paper (arXiv HTML): "approximately 30,000 queries"; per-tier table gives Tier 1 = 1,080,
    Tier 2 = 5,800, Tiers 3–7 = 4,560 each, Tier 8 unspecified (≈29,680 for tiers 1–7).
  - HF README: **16,843 queries / 36,421 audio files / 59.6 hours**, per-tier 2,146 / 3,160 /
    2,146 / 2,132 / 2,146 / 2,146 / 2,146 / 821.
  - The HF layout is `public/<tier>_data/` and `public/<tier>_audios/`. The `public/` prefix plus
    the ~57 % ratio is consistent with the released artifact being a **public subset** of the
    ~30k paper corpus, but no official sentence states this. Treat as: **released ≈16.8k queries;
    the ~30k figure is a paper-only claim and must not be cited off the local copy.**
  - 152 tools across 23 categories, three domains (smart home, smart car, wearables).
- **Language**: English.
- **Speech provenance**: synthetic — zero-shot voice-cloning TTS (Qwen3TTS, CosyVoice-3) over
  30–100 donor speakers drawn from VoxPopuli, 3D-Speaker, ECAPA/YODAS, SPGISpeech 2.0. Noise
  injected at +15 / +5 / −5 dB SNR (automotive and indoor profiles). 16 kHz mono WAV.
- **License — DISCREPANCY**: HF README says verbatim "Creative Commons Attribution-NonCommercial
  4.0 International (CC BY-NC 4.0)"; the arXiv HTML carries a "License: CC BY 4.0" badge (that
  badge governs the *paper*, not the dataset). Operate under **CC BY-NC 4.0**.
- **Obtainability**: ungated HF (already local).
- **Size on disk**: 10.47 GB local.
- **Harness**: no duplex requirement. Pure offline turn-based scoring. No paid API.
- **Published omni baselines**: **Qwen-3-Omni-30B is benchmarked and is the best model reported,
  still under 55 % on F1 and EM**; Tiers 7–8 (multi-turn, intent blending) fall below 56 %.
  Also Qwen-2.5-Omni-7B, Step-Audio2-7B, Kimi-7B, Audio-Flamingo-8B, Whisper-3 + Qwen/Gemma.
- **Knowledge-coupling**: **HIGH**. Concrete field: the **tool registry (152 tools / 23
  categories) supplied in prompt context**, plus the **argument slot values** scored by Slot F1.
  A wrong slot value is a wrong call, and the needle-in-haystack / implicit / correction tiers
  are exactly where an externally supplied entity roster or argument-constraint table could move
  the number.
- **G1' verdict**: **ADMIT**. All five criteria pass; it is the family anchor and the only
  candidate already carrying a published Qwen3-Omni-30B baseline on an offline turn-based
  protocol.

---

## From Text to Voice / ToolVoice

- **Name / arXiv**: From Text to Voice: A Reproducible and Verifiable Framework for Evaluating
  Tool Calling LLM Agents, arXiv:2605.15104 (v1 2026-05-14, v2 2026-05-20)
- **Official repo**: https://github.com/talkiq/dialpad-ai-research/tree/main/toolvoice
  (Dialpad AI Research)
- **not-local**
- **DATA RELEASED?** **Partially confirmed — open question.** The repo README states "We release
  audio-converted versions of two tool-calling benchmarks" and the tree shows `data/` and
  `scripts/`. I could **not** confirm from the official surface whether pre-generated `.wav`
  files are committed in `data/` or whether `data/` holds only JSON manifests requiring
  regeneration through the TTS scripts (the `data/` tree URL returned 404 to WebFetch). **This
  single fact decides the verdict** — if audio must be regenerated, the official pipeline needs
  Gemini-2.5-Flash/Pro-TTS and GPT-4o-Mini-TTS, i.e. paid, and the study's zero-spend rule bites.
- **Task shape and I/O**: spoken query (+ multi-turn context) -> predicted function call; and for
  When2Call, the decision of whether to call at all.
- **Evaluation level**: **A**. Metrics as published: **AST-based soft accuracy** (Confetti),
  **F1-score** (When2Call).
- **Size**: Confetti 313 examples requiring explicit tool calls; When2Call 300 instances
  (non-MCQ subset). Paired text-audio instances across 5 audio conditions (clean + SNR 5/10/15/20
  dB) and multiple voices. Total hours not retrieved.
- **Language**: English.
- **Speech provenance**: TTS — Gemini-2.5-Flash-TTS, Gemini-2.5-Pro-TTS, GPT-4o-Mini-TTS; voices
  Kore/Coral (female), Orus/Ash (male). No human speech.
- **License**: "This project is licensed under CC BY 4.0".
- **Obtainability**: direct (public GitHub), pending the `data/` question above.
- **Rough size**: not retrieved (613 base instances × voices × 5 noise conditions; likely low
  single-digit GB if audio is committed).
- **Harness**: **no duplex requirement** — it is explicitly a paired text/audio offline protocol.
  Paid API required only to *regenerate* audio, not to score released audio.
- **Published omni baselines**: **Qwen3-Omni-30B-A3B-Instruct is a primary evaluated model** —
  our exact core, on our exact protocol shape. Also Gemini-3.1-Flash-Live (Confetti 70.4 best) and
  GPT-Realtime-1.5 (When2Call 71.9 best), plus Qwen3 0.6B–32B text-only scaling.
- **Knowledge-coupling**: **HIGH**. Concrete field: the **tool schema list injected into the
  prompt**, and for When2Call the **abstention decision** — When2Call is structurally a test of
  whether the supplied schema covers the request, which is a knowledge-supply question, not an
  acoustic one.
- **G1' verdict**: **CONDITIONAL** on one fact: whether `toolvoice/data/` ships pre-generated
  audio. If yes -> ADMIT (small but perfectly matched: turn-based, CC BY 4.0, free, AST-pinned
  metric, and a published Qwen3-Omni number to reproduce against). If no -> REJECT on criterion
  (2) zero-cost obtainable.

---

## tau-Voice (τ-Voice)

- **Name / arXiv**: τ-Voice: Benchmarking Full-Duplex Voice Agents on Real-World Domains,
  arXiv:2603.13686 (2026-03-14)
- **Official**: https://sierra.ai/blog/tau-voice-benchmarking-real-time-voice-agents-on-real-world-tasks ;
  code inside https://github.com/sierra-research/tau2-bench
- **not-local** (the tau2-bench *text* data is local; the voice layer is not a dataset)
- **DATA RELEASED?** **Code-only, no speech corpus.** Sierra states "Tasks, environment, voice
  user simulator, audio effects, turn-taking policy, and evaluation are all open source." There is
  no downloadable audio dataset — audio is synthesised live by the voice user simulator during a
  run.
- **Task shape and I/O**: live spoken customer-service conversation -> tool calls executed against
  a stateful domain environment -> **final database state** checked against expected actions.
- **Evaluation level**: **E** (executed end-to-end task success). Metric: **pass@1** (and the
  tau2-bench `pass^k` family), per-domain breakdown.
- **Size**: 278 tasks inherited from τ²-bench text; domains `mock`, `airline`, `retail`,
  `telecom`, `banking_knowledge`. No audio hours (synthesised per run). Speakers: simulator voices.
- **Language**: English.
- **Speech provenance**: TTS, bot-to-bot (ElevenLabs TTS for the simulated user; Deepgram/OpenAI
  for transcription).
- **License**: MIT (tau2-bench repo).
- **Obtainability**: direct code, but **PAID at runtime**.
- **Rough size**: 26 MB (text data, already local); audio 0 GB shipped.
- **Harness**: **FULL-DUPLEX REALTIME IS THE CORE MODE — ENTRY BARRIER.** `src/tau2/voice/README.md`
  supports only OpenAI Realtime, Google Gemini Live, xAI Grok Voice; no local/offline option, no
  llama.cpp/vLLM path. Sierra's blog says "The framework supports cascaded ASR→LLM→TTS pipelines
  as well as audio-native models, but we have not yet published a head-to-head comparison" — so a
  cascaded path is *claimed to exist* but is unpublished and still routes TTS/ASR through paid
  vendors.
- **Published omni baselines**: none for Qwen3-Omni. GPT-5 (reasoning, text) 85 %; voice agents
  31–51 % clean, 26–38 % noisy; 79–90 % of failures attributed to agent behaviour. Frontier moved
  30 % (gpt-realtime-1.0, Aug 2025) -> 67 % (grok-voice-think-fast-1.0, Apr 2026).
- **Knowledge-coupling**: **HIGH in principle** — the domain **policy document** and the
  **backing database** are literally injected knowledge artifacts, and `banking_knowledge` adds a
  configurable RAG pipeline. This is the best-designed coupling surface in the family.
- **G1' verdict**: **REJECT** on (2) zero-cost obtainable and (3) adapter-mappable for a
  turn-based core. No audio ships; every supported provider is a paid realtime service. Revisit
  only if Sierra publishes the cascaded path with a local-model adapter.

---

## tau2-bench (text), voice mode

- **Name / repo**: sierra-research/tau2-bench, MIT; modelscope `evalscope/tau2-bench-data` (26 MB)
- **already-local** (text data)
- **DATA RELEASED?** Yes for the text benchmark; the voice mode is a runtime layer, not data
  (see τ-Voice above).
- **Task shape and I/O**: text customer-service dialogue -> tool calls -> final DB state.
- **Evaluation level**: **E**. Metrics: `pass@k` / `pass^k`, `evaluation_criteria.actions`.
- **Size**: 278 tasks (per τ-Voice); domains mock/airline/retail/telecom/banking_knowledge;
  "75+ task fixes" in the latest release.
- **Language**: English. **Speech provenance**: n/a (text).
- **License**: MIT.
- **Obtainability**: direct / already local. **26 MB.**
- **Harness**: turn-based, but the reference runner routes models through LiteLLM with API keys;
  a local endpoint is straightforward to point at.
- **Published omni baselines**: none in speech.
- **Knowledge-coupling**: **HIGH** — the per-domain policy document is a first-class injected
  knowledge artifact and the DB is the ground truth.
- **G1' verdict**: **CONDITIONAL** — fails criterion (1) in-boundary as a *speech* task (it has no
  speech). Admissible only as a **text control / upper-bound arm** alongside a speech benchmark,
  never as a speech result. Named failing criterion: (1).

---

## VAmoS Bench

- **Name / arXiv**: VAmoS Bench: Voice Agent Simulation Bench, arXiv:2607.27453 (2026-07-29)
- **Official**: https://github.com/veris-ai/riley-agent (Veris AI)
- **not-local**
- **DATA RELEASED?** **Code-only — the scenarios and the backend are NOT released.** The repo
  contains "multiple voice agent implementations for a card-support workflow", explicitly "a
  simulation and reference project, not a production banking service". The paper says only "Agent
  implementations are available at [github]"; the 100 scenarios and the seeded PostgreSQL backend
  run on "the Veris simulation platform, developed and operated by the authors' affiliation" —
  i.e. proprietary infrastructure.
- **Task shape and I/O**: simulated caller with a private goal phones a credit-card support agent
  ("Riley"); the agent uses five tools that **execute real SQL** against the backend.
- **Evaluation level**: **E**. The paper's headline framing is **containment** (calls resolved
  without human handoff); the grader scores **task completion** against the full trace of speech
  and tool invocations, arguments, and returned rows. Also connection rate, latency, duration,
  turns, barge-in frequency, cost.
- **Size**: 100 scenarios. Hours / speakers not stated.
- **Language**: English.
- **Speech provenance**: bot-to-bot simulation (synthetic caller).
- **License**: repo "Except where otherwise noted, this project is available under the MIT
  License" (plus a BSD 2-Clause component); paper CC BY 4.0. **The license does not cover the
  unreleased scenario data.**
- **Obtainability**: **request/none** — no public path to the eval data.
- **Rough size**: n/a (nothing to download).
- **Harness**: **full-duplex over real phone calls (WebSocket PCM16 @ 24 kHz or telephony) —
  ENTRY BARRIER.** Cascaded pipelines are evaluated (Pipecat, LiveKit, Vapi, Nemotron) but still
  over live duplex transport, and most configurations require paid APIs (OpenAI, Deepgram,
  ElevenLabs); Pipecat can host open weights.
- **Published omni baselines**: 11 systems, none Qwen-family.
- **Knowledge-coupling**: **HIGH** conceptually (the SQL backend and the tool argument set), but
  unreachable.
- **G1' verdict**: **REJECT** on (2) zero-cost obtainable and (3) adapter-mappable. Data not
  released; duplex telephony transport mandatory.

---

## DuplexWorld

- **Name / arXiv**: DuplexWorld: Can voice agents help you get through the day?,
  arXiv:2608.10716 (2026-08-11) — the newest paper in this sweep.
- **Official page**: not retrieved (the arXiv abs page carries no repo/HF link).
- **not-local**
- **DATA RELEASED?** **Not retrieved / no evidence of release.** No GitHub or HuggingFace link is
  present on the abstract page. Given it is six days old at survey time, treat as unreleased until
  a repo appears.
- **Task shape and I/O**: speech-to-speech agent conversation across six domain environments
  (banking, insurance, travel, healthcare, logistics, Pathfinding), eleven conversation types.
- **Evaluation level**: **E** (Pass@1 over environments) with duplex-quality side metrics.
  Published: **Pass@1 0.490, turn-taking 0.653, DNSMOS 3.378**.
- **Size**: 156 scenarios, 350+ hours of conversation. Speakers not stated.
- **Language**: English (not explicitly stated; inferred from domains — treat as unconfirmed).
- **Speech provenance**: not retrieved.
- **License**: not retrieved.
- **Obtainability**: **unknown / no public path found.**
- **Rough size**: not retrieved.
- **Harness**: speech-to-speech / duplex framing (turn-taking and DNSMOS are reported) —
  **likely duplex entry barrier**; no cascaded path documented.
- **Published omni baselines**: not retrieved.
- **Knowledge-coupling**: not assessable without the artifact; the six domain environments imply a
  backing state, so plausibly HIGH.
- **G1' verdict**: **REJECT (for now)** on (2) zero-cost obtainable — nothing to obtain. Re-check
  in 4–8 weeks; this is the single most worth re-scouting item in the family.

---

## EVA-Bench

- **Name / arXiv**: EVA-Bench: A New End-to-end Framework for Evaluating Voice Agents,
  arXiv:2605.13841 (v1 2026-05-13, v2 2026-05-27), ServiceNow AI Research
- **Official**: https://github.com/ServiceNow/eva ; HF `ServiceNow-AI/eva`
- **already-local** (263 KB / 5 files)
- **DATA RELEASED?** **Scenario definitions only — the 263 KB is real, not a stub, and not
  audio.** The HF repo holds `data/airline.parquet` (261 kB) + README + .gitattributes. Content
  is structured scenario metadata: user goal with decision tree, user persona, expected
  conversation flow, scenario context, **ground-truth database state**, and **initial backend
  database state** (reservations, flight inventory). The README states this is **50 airline
  scenarios**, "the first in a planned series of domains". **The paper's 213 scenarios across
  three domains (airline CSM, healthcare HRSD, enterprise ITSM) are NOT all released — only the
  50 airline ones are.** No audio ships; audio is synthesised on the fly.
- **Task shape and I/O**: bot-to-bot spoken conversation -> agent tool calls -> **final database
  state** compared against ground truth.
- **Evaluation level**: **E** (with A-level components). Metrics as published: **EVA-A** (Task
  Completion, Speech Fidelity, Faithfulness) and **EVA-X** (Conciseness, Turn-taking, Latency,
  Progression), both reported as pass@1.
- **Size**: 50 scenarios released (213 in paper). 0 hours of shipped audio.
- **Language**: English.
- **Speech provenance**: **bot-to-bot** — a user simulator (ElevenLabs Agents, or OpenAI Realtime)
  converses with the agent over live WebSockets. No human speech.
- **License**: MIT.
- **Obtainability**: ungated HF for the scenarios; the *runnable* benchmark is paid.
- **Rough size**: 0.00026 GB.
- **Harness**: **turn-based, NOT full-duplex** — good news for us. But the official path requires
  a stack of **paid** services: OpenAI GPT-5.2 as text judge, Google Vertex/Gemini as audio judge,
  AWS Bedrock/Claude as faithfulness judge, ElevenLabs Agents as user simulator, Cartesia STT/TTS.
  Both cascade (STT→LLM→TTS) and audio-native agents are supported.
- **Published omni baselines**: 12 cascade and audio-native systems; no system exceeds 0.5 on both
  EVA-A pass@1 and EVA-X pass@1. Specific Qwen results not retrieved.
- **Knowledge-coupling**: **HIGH**. Concrete field: the **scenario database** that the agent's
  tools query and modify, plus `airline_tools.py` read/write **tool definitions**. This is a real
  supplied-evidence slot.
- **G1' verdict**: **CONDITIONAL**. Passes (1), (4), (5). Fails (2) as officially specified —
  every judge and the user simulator are paid. A self-built offline adapter (drive the 50 airline
  scenarios turn-by-turn with locally synthesised user audio and a local judge) would be a
  *re-implementation*, not EVA-Bench, and its numbers would not be comparable to the paper.
  Named failing criterion: (2), and (4) is weakened because the pinned metric depends on
  specific proprietary judge models.

---

## ProVoice-Bench

- **Name / arXiv**: From Reactive to Proactive: Assessing the Proactivity of Voice Agents via
  ProVoice-Bench, arXiv:2604.15037 (v1 2026-04-16, v3 2026-05-02), SJTU. Interspeech 2026 submission.
- **Official page**: none found.
- **not-local**
- **DATA RELEASED?** **Not released — no code or data URL in the paper (v3) or anywhere found.**
- **Task shape and I/O**: four tasks — Proactive Intent Capture (infer implicit intent), Latent
  Topic Monitor (detect user-defined semantic triggers), Context Fact Checking (interrupt when
  speech contradicts digital records), Environment Sound Sensing (acoustic events as cues).
  Output is an intervene/don't-intervene decision plus a response, some of it tool-shaped.
- **Evaluation level**: **A**. Metrics: Recall, False Positive Rate, Accuracy for interaction
  prediction; **Response Accuracy (Racc)** combining tool-call precision and semantic alignment
  via LLM-as-Judge.
- **Size**: 1,182 samples across the four tasks. Hours / speakers not stated.
- **Language**: not explicitly stated in the paper.
- **Speech provenance**: TTS (CosyVoice3). No human speech.
- **License**: only the arXiv perpetual non-exclusive license — i.e. **no dataset license**.
- **Obtainability**: **none / request the authors.**
- **Rough size**: n/a.
- **Harness**: turn-based/offline-compatible in principle; needs an LLM judge.
- **Published omni baselines**: **Qwen3-Omni (30B)** evaluated, alongside Mimo-Audio 7B,
  Step-Audio-R1 33B, Qwen2.5-Omni 7B and thinking variants. Headline finding: over-triggering.
- **Knowledge-coupling**: **MEDIUM**. Concrete field: the **digital records** the Context Fact
  Checking task checks speech against, and the **user-defined trigger list** in Latent Topic
  Monitor — both are supplied-evidence slots. But ESS is an environmental-audio task and is
  **out of this repository's scope**, so at most half the benchmark is admissible.
- **G1' verdict**: **REJECT** on (2) zero-cost obtainable (no release) and partially on (1)
  in-boundary (the ESS task is environmental audio). Worth an author email only if the CFC task
  becomes the study's target shape.

---

## IHBench

- **Name / arXiv**: IHBench: Evaluating Post-Interruption Recovery in Voice Agents with Structured
  Workflows, arXiv:2606.19595 (2026-06-17), Boson AI
- **Official**: HF `bosonai/IHBench`
- **already-local**
- **DATA RELEASED?** **Yes — audio ships.** HF card shows a `conversations` subset (45 rows) and a
  `baseline` subset (428 rows), with `user_turn_X_audio` fields, transcripts, interruption
  classifications and per-turn rubrics.
- **Task shape and I/O**: multi-step enterprise workflow interrupted mid-flow -> the agent must
  resume at the correct step without repeating information. Output is a spoken/textual response
  judged by rubric, not a tool call.
- **Evaluation level**: **A** (rubric/judge-scored response quality). Metrics as published:
  **Task Fulfillment Win Rate** (comparative, vs a GPT-4o baseline) and **Recovery Quality Pass
  Rate** (absolute, type-specific rubrics).
- **Size**: 45 conversations across 10 enterprise domains; 428 interruption points; avg 30.1
  messages/conversation (19–40). Total hours not stated. Under 1K rows total.
- **Language**: English.
- **Speech provenance**: **synthetic TTS**, per-conversation speakers drawn from Common Voice,
  verified with Whisper ASR.
- **License**: `cc-by-4.0`.
- **Obtainability**: ungated HF; already local.
- **Rough size**: small (<1K rows).
- **Harness**: **turn-based / offline — no duplex required.** Good structural fit. But the judge
  is **GPT-5.4-mini in high reasoning mode** — a paid judge on the official protocol.
- **Published omni baselines**: 27 configurations including **Qwen3-Omni-30B** and Qwen2.5-Omni,
  plus GPT-4o Audio, GPT Realtime 1/1.5/2, Gemini 2.5/3 lines, Gemma 4, Phi-4-Multimodal.
  Closed-weight models degrade ~3.3× more slowly as conversations lengthen.
- **Knowledge-coupling**: **MEDIUM**. Concrete field: the **structured workflow definition** (the
  step list the agent must resume into). That is supplied context and it does change the outcome —
  but it is episode-local procedure state, not external evidence, which sits close to the owner's
  knowledge-not-memory boundary.
- **G1' verdict**: **CONDITIONAL**. Passes (1), (2 for the data), (3). Fails (4) as officially
  specified because the pinned metric requires a specific paid judge, and (5) is only moderate —
  the coupling is procedural, not evidential. Good as a robustness side-arm, weak as the primary
  knowledge-coupling target.

---

## VoiceAgentBench

- **Name / arXiv**: VoiceAgentBench: Are Voice Assistants ready for agentic tasks?,
  **arXiv:2510.07978** (October 2025 — note this is *not* a 2026 paper), Krutrim AI Labs / Ola.
- **Official**: HF `krutrim-ai-labs/VoiceAgentBench` ; https://github.com/ola-krutrim/VoiceAgentBench
- **already-local** (5.83 GB, 7,665 files)
- **DATA RELEASED?** **Yes — audio ships, ungated.**
- **Task shape and I/O**: spoken query (+ tool specifications) -> predicted structured tool call.
  Six subsets: single tool-call with parameter filling; tool selection from a list then parameter
  filling; parallel multi-tool; sequential/chained; multi-turn dialogue tool calling; safety
  refusal.
- **Evaluation level**: **A**. LLM-as-a-judge over parameter correctness, multi-tool
  orchestration, sequential dependencies, multi-turn reasoning, and safety/refusal behaviour.
  Exact scalar metric names not retrieved beyond "parameter filling correctness" and "refusal
  behaviour".
- **Size — DISCREPANCY**: HF dataset card says **5,394 total queries**; the paper and the GitHub
  README say **"over 5,500 synthetic spoken queries"**. Hours not stated. Speakers not stated.
- **Language**: **seven languages — English, Hindi, Bengali, Marathi, Tamil, Telugu, Malayalam.**
  English is present, so the boundary is satisfiable by taking the English subset explicitly.
  Content is deliberately India-grounded, which is an entity-distribution consideration.
- **Speech provenance**: **fully synthetic** — English via ElevenLabs + Coqui-TTS voice
  conversion; Hindi and Indic via Krutrim-TTS for both generation and voice conversion.
- **License — THIS IS THE PROBLEM**: "Krutrim Community License Agreement Version 1.0". Verbatim
  clauses retrieved from the repo LICENSE: §3 "Free to use, modify, and distribute for academic,
  educational, research, and personal purposes, provided proper attribution to Krutrim is
  included"; §3 "Commercial Use: Allowed only through a separate commercial license agreement with
  Krutrim"; §5 the software "may not be used to develop, market, sell, or support competing
  products or services", with "Violation results in immediate termination and potential legal
  action"; §14 "Sub-licensing is strictly prohibited"; §10 "Must provide visible attribution to
  'Krutrim' in all publications, software metadata, and related outputs"; §1 defines commercial
  use as involving "more than 1 million monthly active users".
  **Assessment**: academic research use and non-commercial redistribution are explicitly
  permitted, so the study can use it. The live hazards are (a) the mandatory visible-attribution
  clause in any publication, and (b) the §5 competing-products clause, which is vague enough that
  a Stage-3 paper positioning a voice-agent method could be argued into it. **Flag to the owner
  before any paper-scale use; it is not a blocker for Stage-2 research.**
- **Obtainability**: ungated HF; already local.
- **Rough size**: 5.83 GB.
- **Harness**: **turn-based, no duplex requirement.** But the reference evaluation instructs the
  user to set an `OPENAI_API_KEY` for the LLM-as-a-judge; **no local/free judge is documented**.
- **Published omni baselines**: the repo lists Qwen omni among supported models but **no published
  Qwen3-Omni baseline numbers were retrieved.**
- **Knowledge-coupling**: **HIGH**. Concrete fields: (a) the **candidate tool list** the model must
  select from — a directly injectable registry; (b) the **argument/parameter values**, which for
  India-grounded entities are exactly the kind of rare named entity that an externally supplied
  entity roster fixes. The "tool selection from a list" subset is a purpose-built evidence-supply
  slot.
- **G1' verdict**: **CONDITIONAL**. Passes (1) via the English subset (state it explicitly), (2)
  for the bytes, (3), (5). Fails (4) as officially specified: the pinned metric needs a paid
  OpenAI judge. Substituting a local judge makes the numbers non-comparable to the paper. Second
  condition: owner review of the Krutrim license §5/§10 before any paper-scale claim.

---

## AURA

- **Name / arXiv**: AURA: Agent for Understanding, Reasoning, and Automated Tool Use in
  Voice-Driven Tasks, arXiv:2506.23049 (2025-06-29), CMU / Watanabe group.
- **not-local**
- **DATA RELEASED?** **Not a dataset at all — it is a system.** AURA is an open-source
  cascaded voice assistant (open-weight ASR + TTS + LLM) with tools for calendar booking, contact
  lookup, web search, email, associated with the ESPnet ecosystem. No new evaluation corpus is
  released; it *reports on* VoiceBench.
- **Task shape and I/O**: spoken multi-turn request -> tool invocation -> spoken response.
- **Evaluation level**: **E** for its own human eval (90 % task success on complex multi-turn
  speech tasks), **A** for the borrowed benchmarks.
- **Size**: no new dataset. Reported numbers: 92.75 % OpenBookQA (VoiceBench), 4.39 AlpacaEval.
- **Language**: English. **Speech provenance**: n/a (system).
- **License**: paper CC BY 4.0; code license not retrieved.
- **Obtainability**: code direct; **no data to obtain.**
- **Rough size**: n/a.
- **Harness**: cascaded ASR→LLM→TTS, turn-based, open weights — architecturally the friendliest
  thing in this family, and free.
- **Published omni baselines**: none (it is compared against open-weight systems).
- **Knowledge-coupling**: **LOW as a dataset** (there is no dataset). Its tool-registration
  design ("easy integration of new tools using natural language prompts and action classes") is
  interesting as a *reference implementation* of a tool-schema injection surface.
- **G1' verdict**: **REJECT as a task/dataset candidate** on (4) pinnable metric and (5) — it
  supplies neither. Retain as an **engineering reference** for the cascaded adapter, not as an
  evaluation target.

---

## Stream RAG / AudioCRAG

- **Name / arXiv**: Stream RAG: Instant and Accurate Spoken Dialogue Systems with Streaming Tool
  Usage, arXiv:2510.02044 (2025-10-02), Meta + CMU. ICML 2026 poster.
- **not-local**
- **DATA RELEASED?** **NOT RELEASED — release is promised and conditional.** The paper's
  conclusion states verbatim: "we will open source our training code and AudioCRAG-Human
  benchmark, supporting future research". No download link or repository URL exists in the paper.
  Note the promise covers **AudioCRAG-Human only**, not AudioCRAG-Synthetic.
- **Task shape and I/O**: spoken factual query -> tool/retrieval query issued (predicted in
  parallel with the user's speech) -> spoken answer grounded in retrieved evidence.
- **Evaluation level**: **A** (answer correctness) with latency as a co-primary. Metrics:
  **Accuracy** on a 3-way scale (1 / −1 / 0), **first-token and last-token latency (P50, P90)**.
  Judge: Llama-4-Maverick; speech outputs transcribed with Whisper.
- **Size**: **AudioCRAG-Synthetic 1,862** spoken queries (TTS, filtered to zero Whisper WER and
  UTMOS ≥ 3.5); **AudioCRAG-Human 618** human-recorded queries from a diverse participant pool.
  Hours not stated.
- **Language**: English.
- **Speech provenance**: **both** — a real human subset (618) and an in-house TTS subset (1,862).
  The human subset would be genuinely valuable; it is the unreleased half.
- **License**: not stated for the data.
- **Obtainability**: **none today.** Derived from the public CRAG dataset, so a re-derivation is
  conceivable but would not be AudioCRAG.
- **Rough size**: not retrieved.
- **Harness**: the *method* is streaming, but the *benchmark* is a query→answer protocol that maps
  cleanly to a turn-based core. No paid API strictly required if a local judge is substituted.
- **Published omni baselines**: **Qwen-OMNI evaluated**, plus OpusLM and Kimi-Audio. Tool
  integration more than doubles factual QA accuracy (11.1 % → 34.2 % absolute, up to 200 %
  relative).
- **Knowledge-coupling**: **HIGH — the highest conceptual match in the family.** Concrete field:
  the **retrieved evidence passages from the CRAG web/KG corpus**. This is exactly the SAEA
  SUPPLY axis: the paper's own headline is that supplying retrieved evidence doubles accuracy on
  spoken queries. If it were released it would be a top-two candidate.
- **G1' verdict**: **REJECT** on (2) zero-cost obtainable — the data is not downloadable today.
  **This is the highest-value blocked item in the family; recommend an author contact and a
  re-check after ICML 2026 (the release was framed as acceptance-contingent).**

---

## WearVox

- **Name / arXiv**: WearVox: An Egocentric Multichannel Voice Assistant Benchmark for Wearables,
  arXiv:2601.02391 (2025-12-25). Accepted at ICLR 2026.
- **Official**: HF `zlinao/WearVox` (confirmed live)
- **not-local**
- **DATA RELEASED?** **YES — fully downloadable, ungated, and large.** This was the most valuable
  discovery of the sweep: the arXiv abstract page shows no link, but the paper body gives
  `https://huggingface.co/datasets/zlinao/WearVox`, and the HF page resolves.
- **Task shape and I/O**: egocentric spoken query captured on AI glasses -> five task types:
  **Tool Calling** (generate a JSON function call over 8 predefined tools: calendar, web search,
  local search, music player, etc.), **Search-Grounded QA**, Closed-Book QA, **Side-Talk
  Rejection** (device-directed vs background speech), Speech Translation.
- **Evaluation level**: **A**. Tool Calling is scored by **Abstract Syntax Tree (AST)** match over
  predicted tool call structure and content — a hard, pinnable, judge-free metric.
- **Size**: paper says **3,842 multichannel egocentric recordings**; HF viewer reports **4,000
  rows** (discrepancy, record don't resolve). **Tool Calling subtask = 1,125 samples.** Hours not
  stated. Speaker count not stated ("diverse native speakers recruited").
- **Language**: paper implies English-centric with a Speech Translation task; the HF card lists
  **English, Italian, Spanish + 3 more**. English coverage is satisfied.
- **Speech provenance**: **REAL HUMAN, recorded on real AI-glasses hardware, multichannel,
  including noisy outdoor conditions.** Both a single-channel beamformed field (`audio_query`) and
  the raw multichannel field (`audio_query_mc`) are shipped. This is the only candidate in the
  family with genuine device-captured human speech at scale.
- **License — DISCREPANCY**: the paper states **CC BY-NC-SA 4.0**; the HF card tag is
  **`cc-by-nc-4.0`**. Both are non-commercial; the SA (share-alike) obligation is the open
  question. Operate under the stricter reading (CC BY-NC-SA 4.0) until clarified.
- **Obtainability**: **ungated HF** (no access request reported).
- **Rough size**: **59.4 GB.**
- **Harness**: **no duplex requirement. Fully offline turn-based.** No paid API on the Tool
  Calling subtask (AST match needs no judge). Search-Grounded QA needs a join with the public
  CRAG dataset for search results — the HF card states "search results can be obtained by joining
  the dataset with the CRAG dataset", which is a documented free path.
- **Published omni baselines**: **Qwen2.5-Omni evaluated** (underperformed, attributed to model
  size); also GPT-4o Audio, Gemini 2.5 Flash, GPT-5+Whisper, Gemma 3n, Kimi-Audio, and custom
  SC/MC WearLlama on Llama-4-Scout. Overall accuracies 29–59 %. **No Qwen3-Omni number** — that is
  a gap we could fill rather than a gap that blocks us.
- **Knowledge-coupling**: **HIGH, and unusually well-separated across our axes.** Concrete fields:
  (a) **the 8-tool registry + argument slots** on Tool Calling (SUPPLY/USE); (b) **the CRAG
  evidence join** on Search-Grounded QA (SUPPLY — a literal external evidence slot with a
  free public corpus); (c) **the multichannel vs beamformed audio choice** on Side-Talk Rejection
  (OBS — an observation-control lever that is rare to find as an explicit dataset field).
  Very few benchmarks hand you OBS and SUPPLY levers in the same corpus.
- **G1' verdict**: **ADMIT.** (1) human speech, linguistic content, device-directed — in boundary.
  (2) ungated free HF, no paid harness. (3) offline turn-based, ideal for the frozen core.
  (4) AST match is judge-free and pinnable. (5) high, with three distinct coupling fields.
  Only caveats: 59.4 GB acquisition cost, the license discrepancy, and NC terms that must be
  respected. **Recommended as the top not-yet-local acquisition in this family.**

---

## DuplexSLA / DuplexSLA-Bench

- **Name / arXiv**: DuplexSLA: A Full-Duplex Spoken Language Model with Synchronized Speech,
  Language, and Action, arXiv:2605.20755 (v1 2026-05-20, v2 2026-06-11).
- **Official**: https://github.com/hyzhang24/DuplexSLA ; https://hyzhang24.github.io/DuplexSLA/
- **not-local**
- **DATA RELEASED?** **NO — "coming soon".** The paper claims "the project page, interactive
  demos, and the DuplexSLA-Bench evaluation suite are publicly available", but the repository
  itself marks **inference code, model checkpoints, and DuplexSLA-Bench as coming soon**. This is
  a direct paper-claim-vs-repo-state contradiction; record it, do not resolve it.
- **Task shape and I/O**: full-duplex conversation with a structured action stream decoded
  alongside assistant audio on a shared 160 ms chunk timeline; in-conversation planning and tool
  calling without interrupting speech generation.
- **Evaluation level**: **A** (turn-taking and tool-call correctness cases), not executed task
  success.
- **Size**: **2,100 turn-taking and tool-call cases** covering pause/interrupt/backchannel plus
  three styles of in-conversation tool calling. Hours / speakers not stated.
- **Language**: not retrieved.
- **Speech provenance**: not retrieved (model is initialised from Step-Audio-2-mini ~7B).
- **License**: paper CC BY 4.0; benchmark license not retrieved.
- **Obtainability**: **none today.**
- **Rough size**: not retrieved.
- **Harness**: **full-duplex is intrinsic — the benchmark is defined on a 160 ms chunk timeline
  with turn-taking semantics. ENTRY BARRIER.** There is no meaningful turn-based projection of
  a backchannel/interrupt test.
- **Published omni baselines**: not retrieved.
- **Knowledge-coupling**: **LOW-MEDIUM** — the tool-call cases have argument slots, but the
  benchmark's centre of gravity is timing and turn-taking, which is orthogonal to evidence supply.
- **G1' verdict**: **REJECT** on (2) not released and (3) duplex-intrinsic, not adapter-mappable
  to a turn-based core.

---

## FOCAL

- **Name / arXiv**: FOCAL: A Novel Benchmarking Technique for Multi-modal Agents,
  arXiv:2601.07367 (v1 2026-01-12, v2 2026-03-02), Sprinklr.
- **not-local**
- **DATA RELEASED?** **NO — and there is no dataset to release.** FOCAL is a benchmarking
  *technique*, evaluated on a proprietary internal Sprinklr RAG shopping-support agent. No public
  dataset or code. The paper ships only demonstration conversations and judge outputs in an
  appendix.
- **Task shape and I/O**: simulated spoken customer-support conversation (GPT-4o persona
  simulator) against a synthetic retail knowledge base -> agent responses and tool calls.
- **Evaluation level**: **A** (judge-scored dimensions). Metrics — the **R-E-S-T** scheme:
  **Reasoning (R)**, **Efficiency (E)**, **Semantic (S)**, **Tool-Calling (T)** (correct tool
  usage ratio), plus WER, contextual similarity, voice similarity, MOS estimates.
- **Size**: 6 customer journeys (store locator, damaged items, payment issues, order tracking,
  returns, cancellations). No corpus size stated.
- **Language**: English. **Speech provenance**: TTS (NeuTTS) + Whisper-v3-large ASR in the loop.
- **License**: not stated for any artifact.
- **Obtainability**: **none.**
- **Rough size**: n/a.
- **Harness**: cascaded, turn-based — architecturally compatible, but requires **GPT-4o /
  GPT-4o-mini / GPT-4.1 (all paid)** as agent, simulator, and judge.
- **Published omni baselines**: none.
- **Knowledge-coupling**: **MEDIUM in design** (a synthetic retail KB backs the RAG agent) but
  **unmeasurable** — the KB is proprietary.
- **G1' verdict**: **REJECT** on (2) nothing obtainable and (4) no pinnable public metric.

---

## BFCL v4 — and the audio-tier question, RESOLVED

- **Name**: Berkeley Function Calling Leaderboard V4, https://gorilla.cs.berkeley.edu/leaderboard.html ,
  https://github.com/ShishirPatil/gorilla/tree/main/berkeley-function-call-leaderboard ,
  HF `gorilla-llm/Berkeley-Function-Calling-Leaderboard`. ICML 2025 paper (OpenReview 2GmDdhBdDk).
- **already-local**: no (text BFCL data is public but not held).

### The resolution

**BFCL v4 has NO audio tier. The prior survey's lead was based on a loosely worded sentence in
arXiv:2605.15104, and the citation behind that sentence points somewhere else entirely.**

Evidence chain, in order:

1. arXiv:2605.15104 (v2) contains the phrase verbatim: *"Recent work has begun evaluating tool
   calling from speech, including \"BFCL-v4's audio tier\", as well as benchmarks like
   VoiceAgentBench."* — with citations [32] and [42].
2. Reference **[32]** is Patil et al. (2025), *The Berkeley Function Calling Leaderboard (BFCL):
   from tool use to agentic evaluation of large language models*, ICML — the text BFCL paper.
3. Reference **[42]** is **"Salesforce AI Research and Berkeley (2025) BFCL Audio: a benchmark for
   audio-native function calling. Note: https://www.salesforce.com/blog/bfcl-audio-benchmark/
   Last Accessed: May 11, 2026"** — a **Salesforce blog post**, not a Gorilla release.
4. The official Gorilla blog index (`gorilla.cs.berkeley.edu/blog.html`) lists exactly six posts:
   BFCL V4 Agentic Part 1 (Web Search), Part 2 (Memory), Part 3 (Prompt Variation) — all
   2025-07-17 — plus BFCL V3 (2024-09-19), BFCL V2 (2024-08-14), and the original (2024-02-26).
   **There is no audio or speech post.**
5. The V4 leaderboard page enumerates no audio/speech category; the published V4 composition is
   Agentic (web search, memory, format/prompt sensitivity), Multi-Turn, Live, Non-Live, and
   Hallucination Measurement.
6. Searches of the gorilla GitHub and of HuggingFace for a BFCL audio dataset returned nothing.

**Conclusion**: "BFCL Audio" is a **separate companion artifact** announced by Salesforce AI
Research in collaboration with Berkeley on **2025-08-22**, not a tier of the BFCL v4 leaderboard.
The prior survey's observation that "the V4 leaderboard and HF repo appeared text-only" was
**correct**; arXiv:2605.15104's phrasing is imprecise.

### BFCL Audio itself

- **DATA RELEASED?** **No public dataset located.** The canonical Salesforce blog URL returns
  HTTP 403 to automated fetching; secondary coverage (StartupHub, MarketScreener) describes the
  methodology but **states no repository, no HuggingFace org, no license, and no availability
  statement**. Nothing on the gorilla GitHub, nothing under gorilla-llm on HF.
- **Task shape**: existing BFCL text queries paraphrased into conversational speech, synthesised
  by multiple TTS engines (Qwen, OpenAI, Gemini, ElevenLabs, Cartesia). End-to-end models receive
  the waveform; pipelined models receive transcripts pre-generated by three ASR systems (OpenAI,
  ElevenLabs, Deepgram) and are scored separately per transcript.
- **Evaluation level**: **A** (AST/execution/relevance accuracy inherited from BFCL).
- **Size / languages / license / speakers**: **not retrieved** (blocked by the 403).
- **Published finding**: pipelined systems drop **~10–20 % relative to text-mode BFCL, "largely
  because models fail to correctly handle entity dictation over the pipeline."**
- **Knowledge-coupling**: **HIGH — and the published failure mode is precisely our thesis.**
  Concrete field: **entity dictation over the ASR boundary**, i.e. rare named entities landing in
  tool arguments. An externally supplied entity roster is the textbook fix for exactly that
  failure. If the data ever becomes downloadable this is a first-rank candidate.
- **G1' verdict**: **REJECT (blocked)** on (2) zero-cost obtainable — no public artifact found.
  **Cite the ~10–20 % entity-dictation drop as motivating prior evidence, not as a target.**

---

## Full-Duplex-Bench-v3 (FDB-v3)

- **Name / arXiv**: Full-Duplex-Bench-v3: Benchmarking Tool Use for Full-Duplex Voice Agents Under
  Real-World Disfluency, arXiv:2604.04847 (2026-04-06), Guan-Ting Lin, Chen Chen, Zhehuai Chen,
  Hung-yi Lee.
- **Official**: https://github.com/DanielLin94144/Full-Duplex-Bench ;
  https://daniellin94144.github.io/FDB-v3-demo/
- **already-local**
- **DATA RELEASED?** **Yes, but via an unpinnable channel.** The repo README says: "Download the
  benchmark data [here]" pointing at a **Google Drive file** (`1SO_4MTazWQ_jvCx0dtmpQ-t40bdd07yz`).
  Code + data went public 2026-05-20. There is **no HuggingFace mirror and no content hash** —
  a Drive link is not a pinnable evidence source, which matters for this program's asset lock.
- **Task shape and I/O**: naturally disfluent spoken request -> **chained API calls** across a
  domain toolset -> task completion.
- **Evaluation level**: **A + E mixed**. Metrics as published: **Tool Selection F1**, **Argument
  Accuracy**, **Task Completion (Pass@1)**, **Response Quality**, **Turn-take rate**, **Latency**
  (first response / tool call / task completion), **Interruption rate**, **Filler rate**.
- **Size**: **100 scenarios from 12 speakers**, three difficulty tiers (Easy single-step, Medium
  two-step, Hard multi-step), four domains: Travel & Identity, Finance & Billing, Housing &
  Location, E-Commerce Support. 21 scenarios specifically test self-correction. Total hours not
  stated. Includes 30 s of **real ambient environment** trailing each clip rather than digital
  silence.
- **Language**: English, including non-native speakers (Korean and Russian L1) with varying accent
  strength.
- **Speech provenance**: **REAL HUMAN — the dataset "consists entirely of real human audio"**,
  recorded on everyday built-in microphones in uncontrolled environments, annotated across five
  disfluency categories (fillers, pauses, hesitations, false starts, self-corrections). Speakers
  were given scenario context and performed prompts organically.
- **License**: CC BY-SA 4.0.
- **Obtainability**: direct (Google Drive), free.
- **Rough size**: not retrieved.
- **Harness**: the *reference* runs use LiveKit Realtime with paid cloud realtime models — but
  **a cascaded baseline (Whisper → GPT-4o → TTS) is a published, first-class row in the results
  table** (Tool Sel 0.803, Arg Acc 0.562, Pass@1 0.450, turn-take 100.0 %, latency 10.12 s).
  That establishes a documented turn-based/cascaded path. Ultravox v0.7 (open weights) is also a
  published row, so an open-weight comparison point exists.
- **Published omni baselines**: GPT-Realtime (Pass@1 0.600, best), Gemini Live 2.5 (0.490),
  Gemini Live 3.1 (0.540, fastest at 4.25 s), Grok (0.430), Ultravox v0.7 (0.410), Cascaded
  (0.450). **No Qwen-family baseline.**
- **Knowledge-coupling**: **HIGH**. Concrete fields: the **per-domain callable tool set** and the
  **argument values** (Argument Accuracy is a standalone published metric, so evidence supply is
  directly measurable). The disfluency dimension is an OBS-axis lever on the same corpus.
- **G1' verdict**: **CONDITIONAL — but the most interesting conditional in the family.** Passes
  (1) real human speech, (3) a cascaded path is published and reproducible, (4) Tool Selection F1
  and Argument Accuracy are hard pinnable metrics, (5) high. The condition is (2)/pinnability of
  the *asset*: 100 scenarios is small, and a Google Drive link with no hash cannot be locked into
  `docs/datasets.lock.json` the way the program requires. **Recommend: keep, and ask the authors
  for a HuggingFace mirror or publish our own SHA-256 of the retrieved archive.**

---

## EchoChain (NEW — not in any prior survey)

- **Name / arXiv**: EchoChain: A Full-Duplex Benchmark for State-Update Reasoning Under
  Interruptions, arXiv:2604.16456 (2026-04-08), Smit Nautambhai Modi et al. (Labelbox).
  Announcement: https://labelbox.com/blog/introducing-echochain-an-audio-benchmark-for-reasoning-under-pressure-in-full-duplex-dialogue/
- **not-local**
- **DATA RELEASED?** **No release statement found.** Neither the arXiv page nor the Labelbox blog
  states that the dataset or code is open-sourced; no GitHub or HF link located.
- **Task shape and I/O**: a full-duplex assistant is interrupted mid-generation and must revise
  task state; scored on whether the continuation reflects the update.
- **Evaluation level**: **A** (pass rate on state revision) plus three named failure modes:
  **contextual inertia**, **interruption amnesia**, **objective displacement**.
- **Size**: "a cultivated data set of 200 rows" for the reported results; DSR seed library covers
  voice support calls, interview coaching, multi-constraint planning. Scenario count not stated.
- **Language**: English (implied). 
- **Speech provenance**: **TTS via a "Persona Voice Engine" and a voice-cloning TTS engine**,
  A/B validated against human recordings.
- **License**: not stated.
- **Obtainability**: **none.**
- **Rough size**: n/a.
- **Harness**: **requires streaming audio input and full-duplex models — ENTRY BARRIER.** No
  cascaded path described. Tool calls are **not** part of the task.
- **Published baselines**: no system exceeds 50 % pass. GPT-realtime-2025-08-28 44.0 %, Grok Voice
  Agent 47.5 %; also Gemini Live-2.5-flash-native-audio and Amazon Nova Sonic 2. No Qwen.
- **Knowledge-coupling**: **LOW**. There is no external evidence slot; the task is about revising
  episode-local state, which sits on the far side of the owner's knowledge-not-memory boundary.
- **G1' verdict**: **REJECT** on (2) not released, (3) duplex-intrinsic, and (5) low coupling.
  Recorded for completeness.

---

## AudioAgentBench / audio-agent-bench-suite (NEW — not in any prior survey)

- **Name**: Audio Agent Bench Suite, Arcada Labs, 2026. HF `arcada-labs/audio-agent-bench-suite`.
  No arXiv ID; BibTeX citation offered on the card but **no paper**.
- **not-local**
- **DATA RELEASED?** **Announced but effectively EMPTY.** The dataset card is fully written —
  six sub-datasets, domains, per-turn schema — but **the repository shows ~9.78 kB total with no
  uploaded data files**. This is a card-without-bytes situation. Treat as **not released**.
- **Task shape and I/O**: multi-turn spoken conversation -> per-turn judgement across instruction
  following, knowledge-base grounding, **function-call accuracy**, long-range conversational
  memory, and state tracking.
- **Evaluation level**: **A** (per-turn scoring dimensions with reference responses and
  function-call specifications).
- **Size (claimed)**: six domains — AI conference assistant (75 turns), laptop sales (31), grocery
  ordering (30), dental scheduling (25), event planning (29), personal assistant with
  flights/hotels/calendar/email (31). ~221 turns total. Tiny.
- **Language**: English only.
- **Speech provenance**: **REAL HUMAN — "Audio files are recordings of 2 human English-speaking
  voice actors reading the scripted user inputs"**, with consent. Only 2 speakers, so speaker
  diversity is nil.
- **License**: Creative Commons Attribution 4.0.
- **Obtainability**: ungated HF **in principle**; nothing to download **in practice**.
- **Rough size**: ~0.00001 GB (empty).
- **Harness**: turn-based; no duplex requirement.
- **Published baselines**: none.
- **Knowledge-coupling**: **HIGH by design** — the card names **knowledge-base grounding** and
  **function-call specifications** as explicit per-turn scoring dimensions. Very small, though.
- **G1' verdict**: **REJECT (blocked)** on (2) — the bytes are not there. Worth a re-check in a
  few weeks; if it fills in, the CC BY 4.0 + real-human + KB-grounding combination is attractive
  despite the size.

---

## aiewf-eval (NEW — not in any prior survey)

- **Name / repo**: https://github.com/kwindla/aiewf-eval — "A long-context eval" (Kwindla Hultman
  Kramer, Daily/Pipecat). Discussed at
  https://www.ultravox.ai/blog/why-speech-to-speech-is-the-future-for-ai-voice-agents-unpacking-the-aiewf-eval
  and https://www.daily.co/blog/benchmarking-llms-for-voice-agent-use-cases/ . No arXiv paper.
- **not-local**
- **DATA RELEASED?** **Yes — code and audio ship in the repo.** Audio files for turns are included
  and the runner produces WAV conversation recordings.
- **Task shape and I/O**: a scripted **30-turn ordering call** -> per-turn tool calls + responses
  grounded in an injected knowledge base.
- **Evaluation level**: **A** (per-turn judged dimensions). Metrics as published: **Turn Pass** =
  `tool_use_correct && instruction_following && kb_grounding` all passing on the same turn;
  **Pass Rate** = Turn Pass / total_turns; plus **TTFT** and **voice-to-voice (V2V) latency**.
  Two benchmark configs: `aiwf_long_context` (~40K-token KB) and `aiwf_medium_context` (~12K-token KB).
- **Size**: 30 turns per conversation, 2 KB-size variants. **Very small** — this is a probe, not a
  corpus.
- **Language**: English.
- **Speech provenance**: pre-recorded scripted turns (human/TTS provenance **not retrieved**).
- **License**: **MIT.**
- **Obtainability**: direct, free.
- **Rough size**: not retrieved; small.
- **Harness**: supports "text, realtime audio, and speech-to-speech models"; **a local CLI path
  exists** (`uv run multi-turn-eval run <benchmark> --model <model> --service <service>`, results
  written to `runs/`), and **self-hosted deployment is explicitly supported (local RTX 5090,
  open-source checkpoints via Baseten)**. Paid APIs are needed only for hosted models.
- **Published baselines**: various hosted LLMs and speech-to-speech models; no Qwen3-Omni number
  retrieved. Practitioner heuristic quoted: TTFT above ~700 ms is unusable for voice agents.
- **Knowledge-coupling**: **HIGH and unusually explicit.** Concrete field: **`kb_grounding` is a
  first-class judged dimension against an injected 12K/40K-token knowledge base**, scored jointly
  with `tool_use_correct`. This is the cleanest ready-made "does supplied evidence change the
  outcome" instrument found in the sweep — it literally scores KB grounding and tool correctness
  on the same turn.
- **G1' verdict**: **CONDITIONAL**. Passes (1), (2) MIT + local path, (3) turn-based capable,
  (5) high and explicit. Fails (4) at scale: a single 30-turn script gives ~30 scored units, far
  too few for a statistically meaningful claim, and the judged dimensions imply an LLM judge whose
  identity is not pinned. **Best used as a design reference for the KB-grounding × tool-correctness
  joint metric rather than as a headline benchmark.**

---

## VoiceAgentEval / OutboundEval-Xbench (NEW — not in any prior survey)

- **Name / arXiv**: VoiceAgentEval: A Dual-Dimensional Benchmark for Expert-Level Intelligent
  Voice-Agent Evaluation of Xbench's Professional-Aligned Series, arXiv:2510.21244 (v2).
  Repo: https://github.com/LVYUERLVR/OutboundEval-Xbench
- **not-local**
- **DATA RELEASED?** GitHub repository indicated in the paper; **contents not verified** in this
  sweep (no fetch of the repo tree was completed). Treat as "code indicated, data unverified".
- **Task shape and I/O**: expert-level **outbound calling** scenarios; a simulated user (GPT-4.1
  backbone) converses with the agent, which must follow a task flow.
- **Evaluation level**: **A** (judged dimensions). Metrics: dual-dimensional **Task Flow
  Compliance** and **General Interaction Capability** across 8 dimensions (naturalness, coherence,
  hallucination handling, ...), plus 15 voice metrics. Human agreement >95 % / 90 %.
- **Size**: 150 evaluation instances, 6 business domains, 30 sub-scenarios, 5 personality types each.
- **Language**: **primarily Chinese** business scenarios (Chinese character error rates,
  Chinese bank examples) with some English. **English coverage is weak — a boundary risk for a
  repository whose model-context rule is English-only.**
- **Speech provenance**: personas modelled from "real-world online conversation data" seeds;
  runtime speech is simulator-generated.
- **License**: only the arXiv perpetual non-exclusive license stated.
- **Obtainability**: GitHub (unverified).
- **Rough size**: not retrieved.
- **Harness**: turn-based simulation; requires GPT-4.1 as simulator and LLM evaluators — **paid**.
- **Published baselines**: 12 LLMs including GPT-4.1, Claude, Gemini, DeepSeek, Qwen, Doubao —
  **text LLM backbones, not omni speech models.**
- **Knowledge-coupling**: **MEDIUM** — task-flow scripts are injected context, but there is no
  external evidence corpus.
- **G1' verdict**: **REJECT** on (1) English coverage insufficient for this repository's
  English-only context rule, (2) paid simulator + judge, and (4) subjective judged dimensions.

---

## Should We Type or Talk to LLM Agents? (NEW — adjacent, not a dataset)

- **Name / arXiv**: Should We Type or Talk to LLM Agents? A Comprehensive Study of Voice and
  Keyboard Input Perturbations, arXiv:2608.03970 (2026-08-04), Zizhao Hu, Nathan Elijah Segura,
  Mohammad Rostami, Jesse Thomason (USC).
- **not-local**
- **DATA RELEASED?** No release links on the abstract page; the artifact is a tool, **HIVE**
  (Human Input-Variation Engine), which injects **voice transcription perturbations** and QWERTY
  keyboard perturbations. Underlying benchmarks not named in the abstract.
- **Task shape**: perturbation study over LLM agent inputs — not a spoken-agent corpus.
- **Evaluation level**: n/a (methodology paper).
- **Knowledge-coupling**: **LOW as a dataset**; **HIGH as a methodological warning** — it is direct
  2026 evidence that the *transcription-error channel* is the dominant modality effect on agent
  performance, which is the mechanism our knowledge-injection hypothesis targets.
- **G1' verdict**: **REJECT as a dataset candidate**; **retain as a citation** for the
  "speech input degrades tool-calling via transcription error" premise.

---

## Family summary

| Candidate | Local? | Data released? | Level A/E | Real speech? | Size | License | Duplex required? | Knowledge-coupling | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| Audio2Tool | already-local | Yes (public subset) | A | No (voice-cloned TTS) | 16,843 q / 36,421 files / 59.6 h / 10.47 GB | CC BY-NC 4.0 (HF) | No | HIGH — tool registry + arg slots | **ADMIT** |
| From Text to Voice (ToolVoice) | not-local | Yes-ish; audio-vs-script unconfirmed | A | No (Gemini/GPT TTS) | 613 base instances × 5 noise conds | CC BY 4.0 | No | HIGH — tool schema + abstention | **CONDITIONAL** (2) |
| τ-Voice | not-local | Code only, no audio corpus | E | No (bot-to-bot) | 278 tasks | MIT (code) | **YES** | HIGH — policy doc + DB | **REJECT** (2)(3) |
| tau2-bench (text) | already-local | Yes | E | n/a (text) | 278 tasks / 26 MB | MIT | No | HIGH — policy doc + DB | **CONDITIONAL** (1) |
| VAmoS Bench | not-local | Code only; scenarios proprietary | E | No (simulated) | 100 scenarios | MIT (code only) | **YES** (telephony) | HIGH but unreachable | **REJECT** (2)(3) |
| DuplexWorld | not-local | Not retrieved / none found | E | not retrieved | 156 scenarios / 350+ h | not retrieved | Likely YES | not assessable | **REJECT (recheck)** (2) |
| EVA-Bench | already-local | Scenarios only (50 of 213), no audio | E | No (bot-to-bot) | 50 scenarios / 263 KB | MIT | No | HIGH — scenario DB + tools | **CONDITIONAL** (2)(4) |
| ProVoice-Bench | not-local | Not released | A | No (CosyVoice3) | 1,182 samples | none stated | No | MEDIUM — records + trigger list | **REJECT** (1 partial)(2) |
| IHBench | already-local | Yes (audio ships) | A | No (TTS/Common Voice) | 45 convs / 428 points | cc-by-4.0 | No | MEDIUM — workflow state | **CONDITIONAL** (4)(5) |
| VoiceAgentBench | already-local | Yes | A | No (ElevenLabs/Coqui/Krutrim TTS) | 5,394–5,500+ q / 5.83 GB | Krutrim Community License v1.0 | No | HIGH — tool list + params | **CONDITIONAL** (4) + licence |
| AURA | not-local | System, not a dataset | E (human eval) | n/a | no dataset | CC BY 4.0 (paper) | No | LOW | **REJECT** (4)(5) |
| Stream RAG / AudioCRAG | not-local | **Not released** (promised) | A | **Yes, 618 human** + 1,862 TTS | 2,480 queries | not stated | No | **HIGH — retrieved evidence** | **REJECT (blocked)** (2) |
| WearVox | not-local | **Yes, ungated HF** | A (AST) | **Yes — real human, AI-glasses, multichannel** | 3,842–4,000 recs (1,125 tool-calling) / 59.4 GB | CC BY-NC-SA 4.0 (paper) vs cc-by-nc-4.0 (HF) | No | **HIGH — 8-tool registry + CRAG evidence join + multichannel OBS lever** | **ADMIT** |
| DuplexSLA-Bench | not-local | **No — "coming soon"** | A | not retrieved | 2,100 cases | not retrieved | **YES** (160 ms clock) | LOW-MEDIUM | **REJECT** (2)(3) |
| FOCAL | not-local | No dataset exists | A | No (NeuTTS) | 6 journeys | none stated | No | MEDIUM but proprietary | **REJECT** (2)(4) |
| BFCL v4 | not-local | Yes (text) | A | **n/a — NO AUDIO TIER** | text only | Apache-2.0 (gorilla repo) | No | HIGH (text) | **REJECT** (1) — no speech |
| BFCL Audio | not-local | **No public artifact found** | A | No (multi-engine TTS) | not retrieved | not retrieved | No | HIGH — entity dictation | **REJECT (blocked)** (2) |
| Full-Duplex-Bench-v3 | already-local | Yes, via Google Drive (no hash) | A + E | **Yes — real human, disfluent, 12 spk** | 100 scenarios | CC BY-SA 4.0 | Reference yes; **cascaded baseline published** | HIGH — tool set + Argument Accuracy | **CONDITIONAL** (2 pinnability) |
| EchoChain | not-local | Not released | A | No (voice-cloned TTS) | 200 rows | not stated | **YES** | LOW | **REJECT** (2)(3)(5) |
| AudioAgentBench (arcada-labs) | not-local | **Card exists, bytes empty** | A | **Yes — 2 human voice actors** | ~221 turns | CC BY 4.0 | No | HIGH — kb grounding + fn-call spec | **REJECT (blocked)** (2) |
| aiewf-eval | not-local | Yes (code + audio) | A | not retrieved | 30 turns × 2 KB sizes | **MIT** | No (local CLI path) | **HIGH — `kb_grounding` is a scored dimension** | **CONDITIONAL** (4 scale) |
| VoiceAgentEval / OutboundEval | not-local | Repo indicated, unverified | A | Seeded from real calls | 150 instances | none stated | No | MEDIUM | **REJECT** (1)(2)(4) |
| Should We Type or Talk (HIVE) | not-local | No links found | n/a | n/a | n/a | not stated | No | LOW (dataset) / HIGH (citation) | **REJECT as dataset** |

---

## New in 2026

Items below post-date, or were absent from, prior surveys of this family. Ordered by how much
they change the picture.

1. **WearVox data is actually downloadable — `zlinao/WearVox`, 59.4 GB, ungated.** The arXiv
   abstract page shows no link, which is almost certainly why prior surveys missed it; the HF id
   appears only in the paper body. It is the only real-human, device-captured, multichannel
   spoken tool-calling corpus in the family, with a judge-free AST metric and a 1,125-sample Tool
   Calling subtask. Accepted at ICLR 2026.
2. **The BFCL "audio tier" is a citation artifact.** arXiv:2605.15104's reference [42] is a
   **Salesforce blog post** ("BFCL Audio", Salesforce AI Research + Berkeley, 2025-08-22), not a
   Gorilla leaderboard tier. BFCL v4 itself remains text-only. Full evidence chain is in the BFCL
   section above.
3. **arXiv:2605.15104 (ToolVoice) benchmarks Qwen3-Omni-30B-A3B-Instruct — our exact core — on an
   offline paired text/audio tool-calling protocol, and releases under CC BY 4.0.** This is the
   closest published protocol match to what this study needs, and no prior survey appears to have
   noted the exact-core baseline.
4. **DuplexWorld (arXiv:2608.10716, 2026-08-11)** — six days old at survey time. 156 scenarios,
   350+ hours, six domains, Pass@1 0.490. No release found yet. The single best re-scout target.
5. **EchoChain (arXiv:2604.16456, Labelbox)** — full-duplex state-update reasoning under
   interruption; no system exceeds 50 % pass. Not released, duplex-only, low coupling — recorded
   so it does not have to be rediscovered.
6. **aiewf-eval (github.com/kwindla/aiewf-eval, MIT)** — a practitioner benchmark that scores
   `tool_use_correct && instruction_following && kb_grounding` **jointly on the same turn** over
   an injected 12K/40K-token knowledge base, with a documented local/self-hosted path. Too small
   to headline, but its metric design is the most direct existing operationalisation of
   "did supplied evidence change the tool call".
7. **arcada-labs/audio-agent-bench-suite (HF, 2026, CC BY 4.0)** — real human voice actors,
   explicit KB-grounding and function-call scoring dimensions, but the repository is currently
   **empty despite a complete dataset card**. A card-without-bytes case worth re-checking.
8. **Full-Duplex-Bench-v3 data went public on 2026-05-20** via Google Drive, and its results table
   includes a **published cascaded (Whisper → GPT-4o → TTS) baseline** — which means a turn-based
   path through this benchmark is documented, not merely hypothetical.
9. **Audio2Tool's released set is ~16.8k queries, not the ~30k the paper claims**, under a
   `public/` prefix, and the HF license (CC BY-NC 4.0) is stricter than the paper's CC BY 4.0
   badge. Both discrepancies matter for how the local copy may be cited and used.
10. **DuplexSLA (arXiv:2605.20755) claims DuplexSLA-Bench is "publicly available" while the repo
    marks it "coming soon"** — a paper-claim vs repo-state contradiction, recorded not resolved.
11. **arXiv:2608.03970 "Should We Type or Talk to LLM Agents?" (2026-08-04)** introduces HIVE and
    isolates voice-transcription perturbation as an input channel for agents — useful as premise
    evidence for why knowledge injection should help spoken tool calling.
12. Also surfaced and logged for completeness, outside this family's core: **PredAct-Bench**
    (arXiv:2608.02372, tool-augmented dialogue under controlled tool noise), **The Bitter Lesson
    of Tool Calling** (arXiv:2608.06370, programmatic vs JSON tool calling over BFCL v4, 14
    models), **Benchmarking the Benchmarks** (arXiv:2608.06329, reference-free benchmark quality
    assessment for conversational agents), and **VoiceAgentEval / OutboundEval-Xbench**
    (arXiv:2510.21244, predominantly Chinese outbound calling).
