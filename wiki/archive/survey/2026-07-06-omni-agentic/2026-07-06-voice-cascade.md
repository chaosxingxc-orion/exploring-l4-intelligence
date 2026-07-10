---
title: "Lane survey — cascaded/orchestrated voice-agent frameworks (ASR->LLM->TTS)"
date: 2026-07-06
stage: 1-argumentation
lane: voice-cascade
---

> **🗄 ARCHIVED (2026-07-11)** — 已收官战役过程件（2026-07-06 omni-agentic 调研），仅作历史，非现行真源。

# Voice-cascade lane — landscape only

**Scope note:** this lane covers the "omni-as-sensor + text-LLM-brain" class — production and
research systems that keep ASR, LLM, and TTS as three (or more) separately swappable components
wired together by an orchestration layer (Pipecat, LiveKit Agents, Vocode, TEN, NVIDIA ACE, and
commercial platforms Retell/Vapi/Bland/Deepgram Voice Agent API), plus the benchmarks and papers
that measure what this composition costs relative to a text-only oracle and relative to native
audio-native (omni) end-to-end systems.

## Up front: what this lane says about the elements/usage-pattern framework

Reading across 14 systems/papers, the cascade literature reads as a **strong, repeated
confirmation** of the elements/usage-pattern split, with one important nuance:

- **The orchestration layer itself (Pipecat's pipeline runner, LiveKit's agent session, Vocode's
  conversation loop, Deepgram's "bundling," Retell's proprietary runtime) is pure plumbing — a
  usage pattern.** It adds no information; swapping it (Pipecat → LiveKit → TEN) changes latency,
  vendor lock-in, and developer ergonomics, never task capability, because the same swappable ASR
  and LLM and TTS elements can be dropped into any of them. Vocode-core's stall (last release June
  2024, "actively looking for community maintainers" as of this survey) while Pipecat/LiveKit/TEN
  kept shipping through 2025-2026 is itself evidence that the orchestration layer is a commodity —
  what gets upgraded release-over-release is the plugged-in element (which STT/LLM/TTS vendor),
  not the pipeline shape.
- **The one recurring exception is turn-taking/endpointing.** LiveKit's "semantic turn detection"
  and TEN's dedicated `TEN_Turn_Detection` model (a transformer **fine-tuned from Qwen2.5-7B**,
  90.64% vs. 71.61% accuracy on English "finished-utterance" classification against comparable
  models) are not prompts to the dialogue LLM — they are separately trained small classifiers
  bolted onto the pipeline as their own element. This is a genuine new-information component, but
  note it is **not training-free** in this project's strict sense (a new small model is trained),
  even though the big dialogue LLM stays frozen — the same "frozen-backbone-but-new-trained-part"
  pattern flagged in the duplex-realtime lane.
- **Where the literature is sharpest against a naive "cascade = worse" prior:** "From Text to
  Voice" (arXiv:2605.15104) shows that when the ASR element is strong (GPT-4o-Transcribe), cascade
  tool-calling accuracy lands within ~1 point of, and sometimes above, the same backend's own
  native-audio path — "neither architecture uniformly dominates." The gap comes from the **ASR
  element's transcription fidelity**, not from cascading as a pattern per se — a clean confirmation
  that the element (which sensor model, how good it is) is the load-bearing variable, and the
  cascade/native choice is comparatively a usage-pattern/engineering decision once the ASR element
  is fixed to be good.
- **First-class negative:** the two purpose-built full-duplex voice-agent benchmarks this project
  tracks (τ²-bench/tau2-bench voice module, and the standalone τ-Voice paper) do **not** yet
  publish a head-to-head cascade-vs-native comparison on the same verifiable pass@k tasks, despite
  the harness supporting both agent types — an empty measurement cell worth flagging for Stage 2.

---

## Claims

### 1. Pipecat — open-source Python orchestration framework for real-time voice pipelines
- **Recognized problem:** reduce the engineering burden of wiring streaming STT, an LLM, and
  streaming TTS into a single low-latency, interruptible real-time loop, without locking into one
  vendor. Source: [docs.pipecat.ai/getting-started/introduction](https://docs.pipecat.ai/getting-started/introduction);
  [github.com/pipecat-ai/pipecat](https://github.com/pipecat-ai/pipecat); PyPI
  [pipecat-ai](https://pypi.org/project/pipecat-ai/).
- **Genealogy:** speech-native orchestration framework (Daily.co); origin-domain **speech**;
  **native** (frame-based pipeline concept built for this exact problem, not ported from a text-LLM
  agent framework).
- **Training-free vs fine-tuned:** training-free — Pipecat contains no model weights of its own; it
  is a message-passing/frame-routing runtime around externally hosted STT/LLM/TTS services (40+
  vendor integrations).
- **Class + verdict:** **usage-pattern** (pure orchestration/plumbing). The pipeline shape adds no
  new information; capability is entirely a function of which STT/LLM/TTS elements are plugged in.
  CONFIRMS the framework's a-priori tag for orchestration layers.
- **Fence tag:** single-session by default (no built-in cross-session memory; would need an added
  memory/knowledge element).
- **Omni role:** n/a — the framework is agnostic to whether the plugged-in STT/TTS are separate
  models (sensor/actuator) or replaced by a single omni model.
- **Delta:** NEW (archive has no cascade-framework entries).

### 2. LiveKit Agents — production voice-agent SDK with native MCP and semantic turn detection
- **Recognized problem:** production-grade realtime voice orchestration with reliable turn
  detection, barge-in handling, and first-party telephony (SIP), reducing the "VoicePipelineAgent"
  integration tax. Source: [github.com/livekit/agents](https://github.com/livekit/agents);
  [docs.livekit.io/agents](https://docs.livekit.io/agents/); went 1.0 in April 2025, on Python
  1.5.x as of April 2026 per [livekit.com/voice-agents](https://livekit.com/voice-agents).
- **Genealogy:** speech-native STT→LLM→TTS orchestration (origin **speech**); the **native MCP
  tool support** is a direct **port** of the Model Context Protocol pattern from the general
  text-LLM tool-use/agent ecosystem into the voice pipeline [ported, origin-domain **LLM**].
- **Training-free vs fine-tuned:** the orchestration layer is training-free; the **semantic turn
  detection** component is itself a small trained transformer classifier consulted per-utterance
  (a distinct trained element, not a prompt to the dialogue LLM).
- **Class + verdict:** mixed — the pipeline sequencing and MCP tool-wiring are **usage-pattern**
  (routing logic, no new information); the semantic-turn-detection model and the MCP-exposed
  tools/knowledge sources are genuine **elements** (a new sensor for dialogue-state and new
  connectors for tools/knowledge respectively). VERDICT: any capability gain here traces to the
  swapped-in element (tool via MCP, or the turn-detector model), not to the sequencing pattern
  itself.
- **Fence tag:** single-session (session resumption on reconnect is a continuity feature, not
  cross-session learning/accumulation).
- **Omni role:** hybrid — STT/TTS are sensor/actuator, the turn-detection model is an auxiliary
  sensor, and the plugged-in LLM (typically a text model) is the brain.
- **Delta:** NEW.

### 3. LiveKit "sequential pipeline architecture" — latency composition as a constraint
- **Recognized problem:** documenting why a 5-stage cascade (Audio→VAD→STT→LLM→TTS→Audio) can hit
  400-800ms round-trip despite each stage individually taking 100-800ms, and how streaming changes
  the composition math. Source:
  [livekit.com/blog/sequential-pipeline-architecture-voice-agents](https://livekit.com/blog/sequential-pipeline-architecture-voice-agents).
- **Genealogy:** speech-native systems-engineering analysis; origin-domain **speech**; native.
- **Training-free vs fine-tuned:** n/a (an architecture/latency analysis, not a model).
- **Class + verdict:** **constraint** (inference-substrate/real-time property). The key claim —
  "streaming transforms total latency from roughly `VAD+STT+LLM+TTS` to something much closer to
  `max(VAD,STT,LLM,TTS)`" — is a property of how the pipeline stages are scheduled/overlapped, not
  of any single model's capability; it bounds what any cascade can achieve regardless of which
  elements are chosen. CONFIRMS "real-time/full-duplex is a constraint," per the organizing
  framework.
- **Fence tag:** n/a.
- **Omni role:** n/a.
- **Delta:** CONFIRMS (aligns with duplex-realtime lane's constraint classification of real-time
  behavior).

### 4. Deepgram Voice Agent API — "bundled" vs. "assembled" cascade, with function calling
- **Recognized problem:** reduce cascade integration/latency overhead while preserving reliable
  mid-stream function-calling (tool use) — positions itself against the "assembled" DIY-cascade
  pattern (separate STT/LLM/TTS vendors). Sources:
  [deepgram.com/product/voice-agent-api](https://deepgram.com/product/voice-agent-api);
  [developers.deepgram.com/docs/voice-agents-function-calling](https://developers.deepgram.com/docs/voice-agents-function-calling);
  [deepgram.com/learn/voice-agent-api-architecture-bundled-vs-assembled](https://deepgram.com/learn/voice-agent-api-architecture-bundled-vs-assembled).
- **Genealogy:** speech-native product engineering (Flux STT + BYO/OpenAI LLM + Aura-2 TTS);
  origin-domain **speech**; native. Function-calling message protocol (`FunctionCallRequest`/
  `FunctionCallResponse`) is a direct **port** of LLM tool-calling conventions [origin-domain
  **LLM**].
- **Training-free vs fine-tuned:** training-free at the integration level (off-the-shelf frozen
  LLM + Deepgram's own STT/TTS models).
- **Class + verdict:** **usage-pattern** — "bundled" (single vendor owns orchestration + lets you
  BYO LLM/TTS but not swap STT) vs. "assembled" (you wire three independent vendors yourself) is a
  packaging/engineering-ownership choice, not a capability difference; per Deepgram's own
  comparison, "streaming vs. batch transcription matters more than architecture choice" for
  latency. Does not cross a capability boundary — trades integration effort for vendor flexibility.
- **Fence tag:** single-session (function calls execute per-turn; no built-in cross-session
  memory).
- **Omni role:** sensor (Flux STT) + actuator (Aura-2 TTS) framing a text-LLM brain.
- **Delta:** NEW.

### 5. TEN Framework + TEN Turn Detection — dedicated trained classifier beyond VAD
- **Recognized problem:** silence-based VAD cannot distinguish "utterance complete, respond now"
  from "speaker paused mid-thought" or "speaker explicitly wants the agent to wait" — causing false
  interruptions in cascade agents. Sources:
  [github.com/TEN-framework/ten-framework](https://github.com/TEN-framework/ten-framework);
  [github.com/TEN-framework/ten-turn-detection](https://github.com/TEN-framework/ten-turn-detection);
  [huggingface.co/TEN-framework/TEN_Turn_Detection](https://huggingface.co/TEN-framework/TEN_Turn_Detection).
- **Genealogy:** speech-native full-duplex turn-taking research, **ported into** a production
  cascade pipeline as a bolt-on classifier; origin-domain **speech**.
- **Training-free vs fine-tuned:** **not training-free** — TEN Turn Detection is a transformer
  **fine-tuned from Qwen2.5-7B** specifically for multilingual (English/Chinese) three-way
  utterance-state classification (finished / unfinished / wait). The big dialogue LLM behind it
  remains frozen, but this auxiliary classifier is itself trained.
- **Class + verdict:** **element** — a genuinely new, separately trained sensing component
  inserted between STT and the LLM. Reported accuracy: 90.64% (English, "finished" class) vs.
  71.61% for "comparable models," per the model card. VERDICT: the gain is attributed to adding a
  dedicated small trained model, not to a prompting/role trick over the existing dialogue LLM —
  supports the framework's claim that crossing even a narrow capability boundary (accurate
  endpointing) needed a new element, not a usage pattern over the frozen brain, though note the
  new element is small and separately trained rather than training-free.
- **Fence tag:** single-session.
- **Omni role:** sensor (auxiliary dialogue-state classifier feeding the brain's decision to
  speak).
- **Delta:** NEW; nuance vs. duplex-realtime lane's FlexDuo/SoulX-Duplug finding (same "trained
  bolt-on module + frozen brain" shape) — CONFIRMS that pattern recurs in the (half-duplex) cascade
  world too, not only full-duplex systems.

### 6. NVIDIA ACE / voice-agent-examples — Pipecat + Riva/NIM/NeMo Agent Toolkit stack
- **Recognized problem:** give enterprises a GPU-accelerated, swappable-element cascade with
  built-in RAG and agent-toolkit connectors on top of a Pipecat orchestration core. Sources:
  [github.com/NVIDIA/voice-agent-examples](https://github.com/NVIDIA/voice-agent-examples);
  [github.com/NVIDIA/voice-agent-examples/blob/main/docs/NVIDIA_PIPECAT.md](https://github.com/NVIDIA/voice-agent-examples/blob/main/docs/NVIDIA_PIPECAT.md).
- **Genealogy:** speech-native product line (Riva Parakeet ASR, Magpie TTS NIMs); the NeMo Agent
  Toolkit (NAT) and RAG service are **ported** from the general text-LLM agent-tooling ecosystem
  [origin-domain **LLM**] into the voice cascade.
- **Training-free vs fine-tuned:** training-free at the composition level — each NIM (ASR/LLM/TTS)
  is a pretrained, frozen served model; RAG adds a retrieval connector without fine-tuning anything.
- **Class + verdict:** **element composition** orchestrated by a **usage-pattern** layer (the ACE
  Controller / Pipecat pipeline itself). Each swappable NIM is an element; RAG is a
  knowledge-connector element; the controller's speculative-processing/response-cacher logic for
  turn-timing is usage-pattern engineering with no informational content of its own.
- **Fence tag:** single-session unless the RAG/knowledge connector is configured to persist across
  calls (then cross-session-accumulating at the knowledge-store level, not the model level).
- **Omni role:** sensor (Parakeet ASR) + actuator (Magpie TTS) framing a text-LLM brain (NIM LLM).
- **Delta:** NEW.

### 7. "Building Enterprise Realtime Voice Agents from Scratch" — measured cascade latency + tool use
- **Recognized problem:** give a reproducible, quantified recipe for a production-grade cascade
  (with full function calling) and argue explicitly against self-hosting an end-to-end omni model
  for this use case. Source: [arXiv:2603.05413](https://arxiv.org/abs/2603.05413) (Qiu, Chen, Yang,
  Zhu, Liu, Tan, Zhao, Murthy, Ram, Prabhakar, Heinecke, Xiong, Savarese, Wang — Salesforce AI
  Research).
- **Genealogy:** speech-native systems paper; origin-domain **speech**; native (a direct
  engineering study, not a transfer).
- **Training-free vs fine-tuned:** training-free — Deepgram STT + vLLM-served frozen LLM +
  ElevenLabs TTS, no fine-tuning of any component.
- **Class + verdict:** **usage-pattern**/deployability argument. The paper's explicit finding —
  "the cascaded streaming pipeline (STT→LLM→TTS) therefore remains the practical architecture for
  self-hosted realtime voice agents" versus Qwen3-Omni end-to-end, which the authors find
  impractical to self-host at low latency — is a **constraint** (deployability/inference-substrate)
  argument, not a capability claim: measured time-to-first-audio of 755ms (best case 729ms) with
  full function calling support. Confirms the "omni-as-sensor + text-LLM-brain" pattern definition
  used by this lane.
- **Fence tag:** single-session.
- **Omni role:** n/a for the paper's own recommended architecture (sensor=Deepgram,
  actuator=ElevenLabs, brain=vLLM-served text LLM); the paper explicitly evaluates and rejects a
  true omni (Qwen3-Omni) alternative on practicality grounds.
- **Delta:** NEW.

### 8. VoiceAgentRAG — dual-agent architecture solving the RAG-latency bottleneck
- **Recognized problem:** a synchronous RAG lookup (vector DB query) breaks real-time conversational
  flow in a voice cascade because retrieval latency stacks on top of STT+LLM+TTS latency. Source:
  [arXiv:2603.02206](https://arxiv.org/abs/2603.02206) (Qiu, Zhang, Chen, Yang, Zhu, Tan, Chen,
  Zhao, Murthy, Ram, Prabhakar, Heinecke, Xiong, Wang — Salesforce AI Research).
- **Genealogy:** the predictive-prefetch/background-agent pattern is **ported** from text-LLM
  agentic-RAG research [origin-domain **LLM**] into the voice-cascade front end.
- **Training-free vs fine-tuned:** training-free — both the "Slow Thinker" (background prediction/
  pre-fetch) and "Fast Talker" (foreground, cache-served) agents use frozen LLMs; the mechanism is
  a caching/scheduling layer, not fine-tuning.
- **Class + verdict:** the "dual-agent" framing is a **usage pattern** (two roles/two LLM calls,
  one foreground one background), but the actual latency fix comes from a genuine new **element** —
  a predictive knowledge-prefetch cache sitting between the retriever and the foreground LLM.
  VERDICT: this is a clean instance of the thesis's key discriminator — the multi-agent
  choreography alone would not fix latency without the added caching/knowledge connector; the gain
  is element-attributable (the cache), with the two-role split being the scheduling mechanism that
  lets the element populate in time, not itself a source of new information.
- **Fence tag:** single-session (predictive pre-fetch operates within a conversation; no evidence
  of cross-session cache persistence/accumulation in the reported design).
- **Omni role:** n/a (text-domain RAG pattern applied to a voice front end; ASR remains the sensor,
  the two LLM roles are both "brain").
- **Delta:** NEW.

### 9. tau2-bench voice module — cascade and native agents supported, comparison not yet published
- **Recognized problem:** give a single verifiable-DB-state pass@k harness that can score both
  cascaded agents (e.g., Deepgram STT + an LLM, LiveKit-style pipelines) and native audio-native
  agents (Nova Sonic, Qwen, OpenAI/Gemini/xAI realtime) on identical tool-use tasks. Sources:
  [github.com/sierra-research/tau2-bench](https://github.com/sierra-research/tau2-bench);
  [github.com/sierra-research/tau2-bench/blob/main/src/tau2/voice/README.md](https://github.com/sierra-research/tau2-bench/blob/main/src/tau2/voice/README.md);
  [sierra.ai/blog/tau-voice-benchmarking-real-time-voice-agents-on-real-world-tasks](https://sierra.ai/blog/tau-voice-benchmarking-real-time-voice-agents-on-real-world-tasks).
- **Genealogy:** **ported** from tau-bench, a text tool-agent-user benchmark [origin-domain
  **LLM**], into full-duplex voice.
- **Training-free vs fine-tuned:** n/a (evaluation harness).
- **Class + verdict:** n/a as a system; structurally the harness treats cascade-vs-native as an
  **element-level swap** (same tasks/DB, swap only the audio-facing element), which validates this
  project's element cut as the natural unit of comparison for voice-agent architecture research.
- **Negative / empty measurement cell:** per Sierra's own blog, "we have not yet published a
  head-to-head comparison" of cascaded vs. audio-native architectures on tau2-bench-voice, despite
  both being technically supported — a first-class gap for Stage 2 to fill.
- **Fence tag:** n/a.
- **Omni role:** n/a.
- **Delta:** NEW (confirms and sharpens the archive's N1/N2 negative — "no published pass@k... on
  any voice-agent benchmark" — by showing the gap persists specifically for the
  cascade-vs-native axis even where the harness exists).

### 10. τ-Voice paper — native-audio-only numbers, and the frozen-LLM oracle ceiling
- **Recognized problem:** quantify how much of a frozen LLM's own text-mode task-completion
  capability survives when it is accessed via audio-native APIs, on 278 realistic
  retail/airline/telecom tool-use tasks. Source:
  [arXiv:2603.13686](https://arxiv.org/html/2603.13686v1) (Ray, Dhandhania, Barres, Narasimhan —
  Sierra).
- **Genealogy:** speech-native benchmark, direct extension of tau-bench [origin-domain **LLM**,
  ported to full-duplex voice].
- **Training-free vs fine-tuned:** n/a (benchmark); tested systems (Gemini-live-2.5-flash-native-audio,
  gpt-realtime-1.5, grok-voice-agent) are frozen served APIs.
- **Class + verdict:** **constraint**/measurement claim. Pass@1: Gemini-live 31%/26%
  (clean/realistic), gpt-realtime-1.5 49%/35%, grok-voice-agent 51%/38%, vs. **GPT-5 (reasoning)
  text baseline 85%** — voice retains only 30-45% of text capability. This paper tests **no
  cascaded agents at all** — a second, independent negative-cell confirmation that published
  cascade-vs-native numbers on verifiable tasks remain absent. The 85% text ceiling is useful
  context for this lane: it is the same frozen LLM's own oracle ceiling, far above every voice
  condition, consistent with the thesis that the bottleneck sits at the audio-facing
  element/interface, not at agent orchestration.
- **Fence tag:** n/a.
- **Omni role:** n/a for the paper; the tested systems are hybrid (native-audio LLM fuses
  sensor+brain).
- **Delta:** CONFIRMS archive negatives N1/N2 (no published pass@k for voice-agent benchmarks) —
  extends them to show the gap holds even in a 2026 purpose-built full-duplex benchmark, and even
  before any cascade-vs-native comparison exists.

### 11. "From Text to Voice" — element-level diagnosis of the cascade-vs-native gap
- **Recognized problem:** build a reproducible, dataset-agnostic way to convert existing text
  tool-calling benchmarks (Confetti, When2Call) into paired audio versions (via TTS + speaker/noise
  variation) so that text-oracle, direct-voice (omni), and ASR-cascade conditions can be measured
  on identical items. Source: [arXiv:2605.15104](https://arxiv.org/abs/2605.15104) (Laskar, Fu,
  Sarfjoo, McNamara, Robertson, Bhushan TN).
- **Genealogy:** **ported** from LLM tool-calling evaluation methodology [origin-domain **LLM**]
  into voice via TTS augmentation.
- **Training-free vs fine-tuned:** training-free (evaluation only); also demonstrates open-source
  Qwen3 (8B+) LLM-judges reaching >80% agreement with proprietary judges — a "verifier-as-tool"
  element usable for scalable, privacy-preserving evaluation.
- **Class + verdict:** **element**-attributable. On Confetti (Table 4): Gemini-3.1-Flash-Live
  73.0% (text) / 70.4% (direct voice) / 71.3% (cascade, ASR=GPT-4o-Transcribe); GPT-Realtime-1.5
  64.0% / 59.2% / 58.8%; Qwen3-Omni 62.2% / 60.4% / 58.9%. "Neither architecture uniformly
  dominates" — cascade beats direct-voice for Gemini (+0.9pp) but trails slightly for the other two
  models. VERDICT: this REFUTES a naive "cascade is inherently worse than native audio" prior —
  when the ASR element (GPT-4o-Transcribe) is strong, cascade performance tracks the same backend's
  native-audio path closely; the residual gap is attributable to which audio-facing element is used
  and how good it is, not to cascading as an architectural pattern per se. Strong support for this
  project's element-centric framing over an architecture-centric one.
- **Fence tag:** single-session (benchmark tasks, no cross-session state).
- **Omni role:** hybrid across conditions — ASR is sensor + text-LLM is brain in the cascade
  condition; the omni model fuses sensor+brain in the direct-voice condition.
- **Delta:** NEW; refines the τ-Voice/tau2-bench negative by showing that where a controlled
  head-to-head *does* exist (on text-derived, TTS-synthesized audio rather than a live full-duplex
  benchmark), cascade is competitive rather than categorically worse.

### 12. X-Talk — a position paper explicitly arguing the modular/cascade case
- **Recognized problem:** counter the assumption that monolithic end-to-end omni models are the
  necessary endpoint for spoken dialogue, by arguing systematically-composed modular pipelines are
  "underestimated." Source: [arXiv:2512.18706](https://arxiv.org/abs/2512.18706) (Liu, Duan, Wang,
  Feng, Zhang, Xing, Shan, Zhu, Dai, Lu, Qiu, Xie, Wang, Yan, Zheng, Ma, Yu, Chen — Fudan/SJTU/
  Shanghai AI Lab/NPU and collaborators, Dec 2025).
- **Genealogy:** speech-native, direct (not a transfer paper).
- **Training-free vs fine-tuned:** mixed — the modular-composition thesis itself is training-free
  (compose existing pretrained/specialized models), though several sub-modules referenced
  (dedicated emotion-recognition, environmental-sound understanding models) are themselves
  fine-tuned/specialized models in their own right.
- **Class + verdict:** the paper's own thesis is a direct **CONFIRMS** of this lane's elements
  framing: it explicitly decomposes the system into front-end (VAD, speech enhancement),
  understanding models (ASR, emotion, environmental-sound — each a distinct sensing element), LLM
  capabilities (RAG, tool use), and TTS, arguing the modular approach's advantage is precisely the
  ability to swap/upgrade each element independently, achieving sub-second latency "without
  sacrificing modular flexibility" versus omni models that "struggle to balance competing
  objectives within a single network." VERDICT: gain is attributed to element composition and
  swappability, explicitly not to a single orchestration trick or to joint end-to-end training.
- **Fence tag:** single-session.
- **Omni role:** n/a (this is the cascade side by construction), though its ASR module is scoped to
  include paralinguistic sensing (emotion, environment) beyond bare transcription — an expanded
  sensor role.
- **Delta:** NEW.

### 13. Vocode-core — a stalled 2023-2024 cascade framework, market consolidation signal
- **Recognized problem:** same as Pipecat/LiveKit (build voice-based LLM apps quickly, modular
  STT/LLM/TTS). Source: [github.com/vocodedev/vocode-core](https://github.com/vocodedev/vocode-core).
- **Genealogy:** speech-native orchestration framework; origin-domain speech; native.
- **Training-free vs fine-tuned:** training-free (pure orchestration, no owned weights), same as
  Pipecat/LiveKit.
- **Class + verdict:** **usage-pattern** (identical classification to Pipecat/LiveKit) — but the
  **negative** finding is the interesting data point: latest release v0.1.113 (June 18, 2024), and
  the repository explicitly states it is "actively looking for community maintainers," while
  Pipecat/LiveKit/TEN kept shipping through 2025-2026 (LiveKit 1.0 in April 2025, on 1.5.x by April
  2026). This is evidence that the orchestration layer commoditizes/consolidates over time — the
  thing that matters for staying relevant is which elements a framework can plug in (new vendor
  STT/LLM/TTS APIs, new turn-detection models), not orchestration novelty itself, consistent with
  its "carries no durable new information" classification.
- **Fence tag:** n/a.
- **Omni role:** n/a.
- **Delta:** NEW.

### 14. Commercial cascade platforms (Retell AI, Vapi, Bland AI) — latency/flexibility tradeoff
- **Recognized problem:** package a cascade into a deployable product for non-ML teams, trading off
  latency consistency against provider flexibility. Sources:
  [retellai.com/blog/retell-vs-bland-vs-vapi-vs-elevenlabs](https://www.retellai.com/blog/retell-vs-bland-vs-vapi-vs-elevenlabs)
  (vendor comparison, Retell AI); [bland.ai/blog/retell-vs-vapi](https://www.bland.ai/blog/retell-vs-vapi).
- **Genealogy:** speech-native product engineering; origin-domain speech; native.
- **Training-free vs fine-tuned:** training-free at the product level — each platform's backend LLM
  is typically an off-the-shelf frozen model (e.g., GPT-4o/Claude/Gemini) selected per deployment;
  Bland additionally runs "self-hosted models on dedicated GPUs" for its own STT/TTS stack.
- **Class + verdict:** **usage-pattern** — measured latency: Retell 580-800ms (avg ~620ms, via its
  own proprietary turn-taking runtime rather than chaining public APIs), Bland ~800ms, Vapi 500ms
  tuned / 800-1200ms default (14+ pluggable providers), ElevenLabs low TTS latency but higher
  full-loop. These differences are entirely about how tightly/loosely the same class of elements
  (STT/LLM/TTS/telephony) is integrated — "bundled" (Retell, Bland) vs. "assembled" (Vapi,
  ElevenLabs) — and trade off latency/cost/flexibility, never task capability, since the underlying
  LLM element is swappable and typically identical across platforms for a given customer's choice.
  CONFIRMS that usage-pattern/integration-tightness variance is bounded to latency/UX, not
  capability.
- **Fence tag:** single-session for the core voice loop (some platforms layer CRM/call-history as a
  business feature, which is a product-level memory connector, not a model-level element in the
  RL-relevant sense).
- **Omni role:** sensor (STT) + actuator (TTS) framing a brain (customer-selected LLM, usually
  text-mode).
- **Delta:** NEW.

---

## Summary for cross-lane synthesis

The cascade literature is unusually rich confirmation of the elements/usage-pattern split because
the industry itself has already converged on treating ASR/LLM/TTS as separately swappable elements
around an orchestration layer that everyone (Deepgram, LiveKit, industry blogs) explicitly frames
as commodity plumbing. The one place a cascade adds a genuinely new trained component is
turn-detection/endpointing (TEN, LiveKit semantic turn detection) — small, separately trained
classifiers, not prompts to the frozen dialogue LLM, and not training-free themselves. The sharpest
capability-boundary evidence is "From Text to Voice" (arXiv:2605.15104): holding the same frozen
backend fixed and varying only the ASR element shows cascade performance tracking native-audio
performance closely, localizing the residual gap to ASR-element fidelity rather than to the
cascade-vs-native architectural choice — i.e., swapping the **sensor element** is what moves the
needle, not the orchestration pattern around it. The most consequential empty cell for Stage 2 is
that neither purpose-built full-duplex voice-agent benchmark this project tracks (tau2-bench-voice,
τ-Voice) has yet published a cascade-vs-native head-to-head on live verifiable tool-use tasks —
only a text-synthesized-audio benchmark (arXiv:2605.15104) has done this comparison so far.

---

## Verifier notes (adversarial pass, 2026-07-06)

**Spot-checked 13 sources** (WebFetch on 11 URLs + `gh api` on 6 GitHub repos, some overlapping):
arXiv:2605.15104, arXiv:2603.05413, arXiv:2603.02206, arXiv:2603.13686, arXiv:2512.18706 (all five
papers exist, correct titles/authors, correct venue-appropriate dates within the 2025-01..2026-07
window), huggingface.co/TEN-framework/TEN_Turn_Detection, livekit.com/blog/sequential-pipeline-
architecture-voice-agents, github.com/vocodedev/vocode-core, sierra.ai's τ-Voice blog post,
deepgram.com's bundled-vs-assembled article, retellai.com's vendor-comparison blog, and
github.com/livekit/agents (release history + in-repo `mcp.py`).

**One fixed error — wrong URL (corrected in claim #1 above).** The Pipecat source list cited
`github.com/daily-co/nimble-pipecat`. That repo is real but is an 88-star NVIDIA-NIM "blueprint
notebook" demo (Jupyter Notebook, created Dec 2024) that merely *uses* Pipecat — its own README
says "Pipecat AI... developed by Daily... [is] fully vendor neutral." The actual Pipecat framework
repo the claim describes (Python, 40+ integrations, 13k+ stars, pushed same day as this survey) is
`github.com/pipecat-ai/pipecat`. Replaced the link; no other change needed since the surrounding
prose already described the real framework correctly.

**Numeric claims verified exact, not just "plausible":**
- "From Text to Voice" (arXiv:2605.15104) Table 4 Confetti numbers — Gemini-3.1-Flash-Live
  73.0/70.4/71.3, GPT-Realtime-1.5 64.0/59.2/58.8, Qwen3-Omni 62.2/60.4/58.9 (text/direct-voice/
  cascade) — match the lane's Claim #11 figures exactly, including the "neither architecture
  uniformly dominates" quote and the per-model text-to-voice gaps (1.8pp Qwen3-Omni, 4.8pp
  GPT-Realtime-1.5) cross-checked against the paper's own abstract.
- τ-Voice (arXiv:2603.13686) pass@1 figures (31/26, 49/35, 51/38 clean/realistic; GPT-5 reasoning
  85% text ceiling) match Claim #10 exactly, and the paper's own §6.1 Limitations explicitly flags
  cascaded ASR→LLM→TTS baselines as *not yet added*, confirming the "tests no cascaded agents at
  all" claim verbatim.
- TEN Turn Detection's 90.64%/71.61% figures and Qwen2.5-7B fine-tune basis (Claim #5) confirmed on
  the model card.
- Sierra's blog confirms verbatim the "we have not yet published a head-to-head comparison" quote
  (Claim #9's negative), and `gh api search/code` over sierra-research/tau2-bench turned up both a
  `nova-sonic.md` doc and a LiveKit adapter path, corroborating that the harness genuinely supports
  both native and cascaded agent types as claimed.
- LiveKit Agents (Claim #2): `gh api repos/livekit/agents/releases` confirms 1.5.x tagged releases
  ran 2026-03-19 through 2026-05-29 — "on Python 1.5.x as of April 2026" is accurate — and
  `livekit-agents/livekit/agents/llm/mcp.py` exists in-tree, confirming native MCP support is real
  (not invented).
- Retell/Bland/Vapi latency figures (Claim #14) match retellai.com's own comparison post
  word-for-word; correctly labeled in the lane as a vendor's own comparison (self-serving source,
  appropriately hedged).
- Deepgram's "streaming vs. batch transcription matters more than architecture choice" (Claim #4)
  confirmed near-verbatim ("the bigger variable is streaming versus batch STT, not bundled versus
  assembled").
- Vocode-core's stall (v0.1.113, June 18 2024, "actively looking for community maintainers") — Claim
  #13 — confirmed verbatim on the live repo.

**No invented claims found** among the checked set; every quantitative figure spot-checked resolved
to a real, matching number in a real source.

**Framework-verdict check (new-info/read-out, element/usage-pattern):** all 14 verdicts are
defensible. TEN Turn Detection and LiveKit's semantic-turn-detector are correctly kept out of
"usage-pattern" despite sitting inside an orchestration framework, because each is a separately
*trained* classifier (new information), not a prompt/role trick over the frozen dialogue LLM — the
lane is careful not to let "it's bundled inside a pipeline" collapse into "therefore read-out."
VoiceAgentRAG (#8) and NVIDIA ACE (#6) correctly separate the multi-role/controller *scheduling*
(usage-pattern) from the actual capability-bearing addition (cache, RAG connector — elements). One
soft nit, not an error: Claim #7's header ("Class + verdict: **usage-pattern**/deployability
argument") and its body ("is a **constraint**... argument, not a capability claim") use two
different taxonomy labels for the same claim without picking one — the body's reasoning is sound
(this is a deployability/inference-substrate constraint, matching Claim #3's clean "constraint"
classification), but the compound header label is confusing on a re-read. Not changed in-place since
it's a wording ambiguity rather than a substantive misclassification, but worth tightening if this
lane is revised.

**Recency and negatives:** all dated sources fall inside 2025-01..2026-07 (Vocode-core's June-2024
last release is the sole out-of-window date, and it is cited *as* a negative/stall signal, which is
the correct use of an older data point, not a recency violation). Three first-class negatives are
present and substantiated: tau2-bench-voice's and τ-Voice's absent cascade-vs-native comparisons
(#9, #10, both confirmed against primary sources above), and Vocode-core's maintainer stall (#13).
