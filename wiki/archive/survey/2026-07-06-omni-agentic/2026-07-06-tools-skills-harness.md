---
title: "Stage-1 Survey Lane — Tool-Use / Skills / Harness for Voice & Omni Agents"
date: 2026-07-06
stage: 1-argumentation
lane: tools-skills-harness
---

> **🗄 ARCHIVED (2026-07-11)** — 已收官战役过程件（2026-07-06 omni-agentic 调研），仅作历史，非现行真源。

# Lane: tools-skills-harness

Scope: tool-use / function-calling, "skill" declaration formats (SKILL.md / MCP), and
evaluation harnesses for voice/omni agents, 2025-01 to 2026-07. This lane is the owner
"capability/skills" element axis and is asked to confirm/extend the archive's S2 finding
(a verifiable-reward ACCEPTANCE GATE is the shared control law for curated vs
self-generated skills/memory; curated +16pp vs self-generated ~0).

Every claim below was checked to resolve via WebSearch/WebFetch on 2026-07-06. Dates in
2026 are consistent with the current date and the survey's 2025-01..2026-07 window.

---

## 1. AURA — cascaded speech-native agent with real tool connectors

- **Problem**: existing voice assistants handle isolated intents; AURA targets
  goal-driven, multi-turn tasks requiring dynamic external tool invocation
  (calendar, contacts, email, web search) from speech.
- **Genealogy / origin**: cascaded ASR+LLM+TTS architecture; the *tool-calling*
  pattern itself is ported wholesale from text-LLM function-calling (native
  domain: LLM), applied to a speech front/back end (ported, not natively
  audio-in tool-calling).
- **Training-free**: yes — "combines open-weight ASR, TTS, and LLMs in a cascaded
  pipeline"; new tools are added "using natural language prompts and action
  classes," no fine-tuning of any component.
- **Axis / verdict**: **element** — the capability gain over a bare LLM is
  the tool/connector layer (real external actions the frozen LLM cannot reach
  alone: booking, contact lookup, email, search). The cascading itself
  (ASR→LLM→TTS) is architecture/usage-pattern, not new information; the tools are.
  90% human-rated task success on complex multi-turn tasks; 92.75% VoiceBench
  OpenBookQA, 4.39 AlpacaEval — "outperforming all open-weight systems, nearing
  GPT-4o."
- **Fence**: single-session (no persistent cross-session memory described).
- **Omni role**: n/a — no single audio-in/audio-out network; it is a cascade
  of specialist sensor (ASR) + brain (LLM) + actuator (TTS) models.
- **Delta vs archive**: NEW (first open-source speech-native agent explicitly
  benchmarked on multi-turn tool-use task success).
- URL: https://arxiv.org/abs/2506.23049 (submitted 2025-06-29; Maben, Ganesh
  Lakshmy, Radhakrishnan, Arora, Watanabe)

## 2. Speech-Copilot — genealogy root: LLM-orchestrated modular speech toolset

- **Problem**: instruction-oriented speech processing needs a toolset without
  hand-built integration per task; end-to-end audio-LLMs don't decompose or
  explain their steps.
- **Genealogy / origin**: directly ports the *program-synthesis-orchestrates-
  modular-tools* pattern from the text/vision-LLM agent literature (HuggingGPT/
  Visual-ChatGPT-style tool orchestration) into the speech domain — **ported**,
  origin domain LLM/VLM.
- **Training-free**: explicit quote — "Without additional training processes
  required by end-to-end approaches, our method provides a flexible and
  extendable solution." An LLM analyzes pre-collected instructions, modularizes
  components into a documented toolset, then generates programs that call them.
- **Axis / verdict**: **element** — SOTA on Dynamic-SUPERB comes from giving
  the LLM a constructed toolset of specialist speech modules (the connector),
  not from a prompting trick over one frozen audio model.
- **Fence**: single-session.
- **Omni role**: n/a (text LLM orchestrator + separate specialist speech modules;
  no omni model in the loop).
- **Delta vs archive**: NEW (predates the survey window as a genealogy root,
  2024-07, tagged as such per the hard rules; establishes the pattern AURA and
  AudioToolAgent below both re-derive in 2025-2026).
- URL: https://arxiv.org/abs/2407.09886 (SLT 2024; Kuan, Yang, Huang, Lu, Lee)

## 3. τ²-Bench (tau2-bench) — verifiable dual-control tool-use benchmark (on-disk)

- **Problem**: prior tool-use benchmarks are single-control (only the agent
  calls tools); real support/troubleshooting needs both agent *and* user to
  act on a shared, verifiable world state.
- **Genealogy / origin**: LLM/text conversational-agent domain (native); this
  project already has it on disk as an eval lane.
- **Training-free**: yes — it is an evaluation harness/task generator over
  frozen agents, modeled as a Dec-POMDP with a compositional, programmatically
  verifiable task generator.
- **Axis / verdict**: **constraint** (defines the verifiable-reward acceptance
  criterion — DB-state pass@k — used to grade any tool-use claim); verdict n/a
  (methodology, not itself a capability-crossing claim). Directly the
  measurement substrate that S2's "acceptance gate" language describes.
- **Fence**: single-session (per-episode grading).
- **Omni role**: n/a (text-only agent/user simulator).
- **Delta vs archive**: CONFIRMS — reinforces that a verifiable, environment-
  checked pass@k is the field's real acceptance gate for tool-use claims, same
  control law S2 found for skills/memory.
- URL: https://arxiv.org/abs/2506.07982 (2025-06-09; Barres et al., Sierra)

## 4. τ-Voice — full-duplex voice extension exposes a large, uncrossed gap

- **Problem**: does τ²-bench-level tool-use capability survive the move from
  text to full-duplex spoken interaction (same task, same policy, voice
  interface)?
- **Genealogy / origin**: speech extension of an LLM-domain benchmark — mixed
  origin, **ported**.
- **Training-free**: evaluates frozen, deployed systems (GPT-5-class reasoning
  model, and voice front-ends) — training-free evaluation.
- **Axis / verdict**: **constraint** (perception/real-time-modality fidelity,
  a base-architecture property per this survey's own framework) with verdict
  **read-out**: GPT-5 (reasoning, text) reaches 85% task completion; the *same*
  capability, delivered only through a voice interface, reaches just 31-51%
  clean / 26-38% under noise+accent — "30-45% of text capability" retained, with
  79-90% of failures attributed to agent (not simulator) behavior.
- **Fence**: single-session.
- **Omni role**: hybrid (evaluates native S2S/full-duplex models where one
  network is both sensor and brain).
- **Delta vs archive**: CONFIRMS + EXTENDS L4's instruction/reasoning-gap (P2)
  specifically into the *agentic tool-use* setting, and is direct evidence for
  the MAIN THESIS: switching only the interaction modality/harness (no new
  element added) does not preserve, let alone cross, a capability boundary —
  it collapses it.
- URL: https://arxiv.org/abs/2603.13686 (submitted 2026-03-14; Ray, Dhandhania,
  Barres, Narasimhan)

## 5. VoiceAgentBench — a decorrelated ASR element beats one frozen SpeechLM

- **Problem**: no prior benchmark systematically stresses agentic tool-calling
  in realistic spoken settings (single/multi-tool, multi-turn, safety,
  adversarial robustness) for both cascaded and end-to-end systems.
- **Genealogy / origin**: speech-domain, native construction, drawing its
  tool-calling task format from LLM function-calling conventions (ported
  task format, native speech evaluation).
- **Training-free**: yes — evaluates frozen pretrained systems.
- **Axis / verdict**: **element** — verdict **new-info**: "ASR-LLM pipelines
  substantially outperform end-to-end SpeechLMs, achieving up to 60.6% average
  parameter-filling accuracy on English," while native SpeechLMs show "lower
  performance and sharper degradation on Indic languages." The win comes from
  *adding a second, decorrelated model* (a dedicated ASR system feeding a text
  LLM) — two elements — not from any prompt/role change on a single frozen
  omni SpeechLM.
- **Fence**: single-session.
- **Omni role**: hybrid (for the SpeechLM condition); the cascade condition is
  n/a/two-model.
- **Delta vs archive**: NEW; also a direct, in-lane replication of the MAIN
  THESIS on the tool-calling axis specifically.
- URL: https://arxiv.org/abs/2510.07978 (submitted 2025-10-09, revised
  2026-02-13)

## 6. Audio2Tool — compositional/acoustic stress dataset for speech tool-calling

- **Problem**: existing speech tool-calling evals lack domain breadth, acoustic
  diversity, and compositional-reasoning difficulty.
- **Genealogy / origin**: speech-domain, native; 30k queries across Smart Car /
  Smart Home / Wearables with an 8-tier query curriculum and zero-shot voice
  cloning + noise profiles for realism.
- **Training-free**: yes — evaluates SotA SpeechLMs and ASR-LLM pipelines
  without any fine-tuning step in the benchmark itself.
- **Axis / verdict**: **constraint** (acoustic/compositional robustness);
  verdict **read-out** — "strong performance on simple commands but
  significant degradation under compositional and acoustic challenges" for
  every system type tested; no architecture choice alone closes this gap.
- **Fence**: single-session.
- **Omni role**: hybrid.
- **Delta vs archive**: NEW (extends L4's task-completion-collapse (P1) finding
  specifically to acoustic/compositional tool-calling stress).
- URL: https://arxiv.org/abs/2604.22821 (submitted 2026-04-17, v2 2026-04-28;
  Pahwa, Beedu, Priye, Gandhi, Takawale, Baijal, Yang)

## 7. Full-Duplex-Bench-v3 — real disfluent speech + chained tool calls

- **Problem**: prior full-duplex benchmarks test turn-taking OR tool use, not
  both together, and not on real (not synthetic) disfluent human speech.
- **Genealogy / origin**: speech-domain, native; extends Full-Duplex-Bench
  with 5 disfluency categories (fillers, pauses, hesitations, false starts,
  self-corrections) paired with chained-API-call scenarios across 4 domains.
- **Training-free**: yes — evaluates deployed frozen systems: GPT-Realtime,
  Gemini Live 2.5, Gemini Live 3.1, Grok, Ultravox v0.7, and a cascaded
  Whisper→GPT-4o→TTS pipeline.
- **Axis / verdict**: **element** (native single-model S2S vs. two-element
  cascade is exactly an element-count comparison) — GPT-Realtime leads Pass@1
  at 0.600 and interruption avoidance at 13.5%; Gemini Live 3.1 is fastest
  (4.25s latency). Verdict n/a (comparative benchmark, not a single crossing
  claim), but no system approaches saturation on tool-use accuracy under
  disfluency.
- **Fence**: single-session.
- **Omni role**: hybrid (for the S2S systems).
- **Delta vs archive**: NEW.
- URL: https://arxiv.org/abs/2604.04847 (submitted 2026-04; Guan-Ting Lin et al.)

## 8. Stream RAG — the one case that needed fine-tuning, not a prompt trick

- **Problem**: tool-call latency breaks conversational flow in speech-in/
  speech-out systems; users expect near-instant replies even when a tool call
  is needed.
- **Genealogy / origin**: speech-domain, native; "first framework to generate
  and issue tool queries in parallel as audio input is received," extending
  tool use directly into S2S systems (vs. text-mediated RAG, its LLM-domain
  ancestor) — ported pattern (streaming RAG), native S2S implementation.
- **Training-free**: **no** — explicitly a "post-training pipeline that
  teaches the model when to issue tool calls during ongoing speech and how to
  generate spoken summaries." This is the one item in this lane that
  **changes weights**.
- **Axis / verdict**: element (retrieved tool results are new information);
  but the notable point for this survey is methodological: the authors did
  not reach for a prompting/harness solution — they fine-tuned. QA accuracy
  rises up to 200% relative (11.1%→34.2% absolute on AudioCRAG, built from
  CRAG) and tool-use latency drops 20%.
- **Fence**: single-session.
- **Omni role**: hybrid.
- **Delta vs archive**: NEW, and a **negative-for-training-free-scope** data
  point: this is a case where practitioners judged a training-free/prompt-only
  usage-pattern insufficient for a specific capability (streaming tool-call
  timing) and reached for gradient updates instead.
- URL: https://arxiv.org/abs/2510.02044 (submitted 2025-10-02)

## 9. AudioToolAgent — the verifier/coordinator-as-tool fork, empirically real

- **Problem**: large audio-language models (LALMs) understand audio well but
  lack multi-step reasoning/tool-calling; can a coordinator recover this
  without retraining any LALM?
- **Genealogy / origin**: speech+LLM mixed domain, native construction for
  audio; the "agent coordinates tools" pattern is ported from text-LLM
  agentic tool-use.
- **Training-free**: yes — "utilizing pretrained foundational models without
  data or fine-tuning."
- **Axis / verdict**: **element**, verdict **new-info** — and the cleanest
  in-lane test of this survey's verifier fork: the central coordinator is
  explicitly a **text-only LLM that cannot process audio directly** ("receives
  only the audio file path, a question or prompt, and possible answers"); the
  tools it calls are separate audio-language models. This is a genuinely
  decorrelated verifier-as-tool, not a same-weights role-prompt — and it wins:
  SOTA 77.50% MMAU, 77.00% MMAR, 61.90% MMAU-Pro.
- **Fence**: single-session.
- **Omni role**: **sensor** (the audio-LM tools are strictly perception
  components; reasoning/arbitration lives in the separate, decorrelated text
  LLM "brain" — the roles are architecturally split, not merely prompted
  apart within one model).
- **Delta vs archive**: NEW — direct, positive confirmation of the "verifier-
  as-tool = a real element" fork named in the organizing framework.
- URL: https://arxiv.org/abs/2510.02995 (submitted 2025-10; Wijngaard,
  Formisano, Dumontier, Jitsev)

## 10. AU-Harness — the "harness" itself, with function-calling as a task category

- **Problem**: existing audio-LLM eval toolkits are slow, non-standardized
  across prompting/metrics, and don't cover agentic/reasoning task types.
- **Genealogy / origin**: speech-domain infra, native.
- **Training-free**: it is an evaluation harness (not an agent); it evaluates
  frozen pretrained LALMs, up to 151% faster than prior toolkits via batching.
- **Axis / verdict**: n/a for element/usage-pattern (it is the harness/
  constraint layer itself: "standardized prompting protocols and flexible
  configurations for fair model comparison"). Covers 380+ subsets / 21 tasks
  across 6 categories, explicitly including **Spoken Language Reasoning
  (speech-to-coding, function calling, multi-step instruction following)** as
  one category, alongside Paralinguistics and Safety.
- **Fence**: single-session.
- **Omni role**: n/a.
- **Delta vs archive**: NEW — reveals "significant gaps ... particularly in
  temporal understanding and complex spoken language reasoning tasks," a
  negative capability finding specifically flagged under the function-calling
  category.
- URL: https://arxiv.org/abs/2509.08031 (submitted 2025-09-09, revised
  2026-05-11; Nguyen, Surapaneni, Kalkunte, et al., UT Austin + ServiceNow)

## 11. MCP for voice agents — a ported connector, still text-mediated, not audio-native

- **Problem**: voice agent platforms need a standard way to reach external
  tools/data, mirroring what MCP already does for text-based coding/chat
  agents.
- **Genealogy / origin**: Anthropic's Model Context Protocol (open standard,
  Nov 2024, LLM/coding-agent domain) — **ported** into voice: OpenAI's
  Realtime API added built-in remote-MCP-server support (`gpt-realtime`
  update, announced 2025-08-28 per OpenAI's "Introducing gpt-realtime" post
  and Realtime-API docs — **not** the cookbook URL below, which instead
  demonstrates a separate, chained Agents-SDK voice pipeline with no
  Realtime-API/MCP update mentioned); ElevenLabs and Vapi both ship MCP
  clients/servers for voice pipelines.
- **Training-free**: yes — MCP is a protocol/connector layer, no weight
  changes; works over frozen realtime/S2S models.
- **Axis / verdict**: **element** in principle (arbitrary external tool/data
  access) but implemented today as a **text/transcript-mediated bridge**
  ("capturing user's voice input... transcribed to text... Planner agent...
  synthesizes a response... converted to audio") rather than an audio-native
  tool-call — the audio itself never enters the MCP message. Verdict:
  new-info (the tools are real elements) but the *transport* is still a
  usage-pattern layer (ASR→MCP-call→TTS), not a native audio-in element.
- **Fence**: single-session (protocol calls are stateless per-session; any
  cross-session persistence lives in the external tool's own state, e.g. a
  calendar booking — a distinct accumulation channel from agent memory).
- **Omni role**: n/a (protocol-level).
- **Delta vs archive**: NEW, with a first-class **negative**: no native
  "audio-in MCP tool call" standard was found — every voice-MCP integration
  surveyed still routes through a text intermediary.
- URLs: https://openai.com/index/introducing-gpt-realtime/ (source for the
  2025-08-28 Realtime-API remote-MCP-server support claim),
  https://developers.openai.com/cookbook/examples/partners/mcp_powered_voice_agents/mcp_powered_agents_cookbook
  (source for the text-mediated-bridge quote; uses the Agents SDK "chained"
  voice pipeline, not the Realtime API),
  https://modelcontextprotocol.io/specification/2025-11-25 ,
  https://elevenlabs.io/blog/introducing-elevenlabs-mcp

## 12. Anthropic Agent Skills (SKILL.md) — a mature element format, absent from voice runtimes

- **Problem**: give general-purpose agents composable, reusable procedural
  knowledge ("skills") without per-use-case custom agents or fine-tuning.
- **Genealogy / origin**: LLM/coding-agent domain, native; announced 2025-10-16,
  released as an open standard 2025-12-18, since adopted by 32 tools (Claude
  Code, Codex, Cursor, VS Code, Gemini CLI, and others).
- **Training-free**: yes, explicitly — "a purely architectural innovation with
  no model weight changes," using progressive disclosure (metadata pre-loaded,
  full SKILL.md fetched on demand).
- **Axis / verdict**: **element** (a skill/tool connector format) — new-info
  within the LLM domain; but the founding announcement contains **zero**
  mentions of voice/speech/audio agents. ElevenLabs has published a
  `speech-engine/SKILL.md` — but on inspection it is a skill *for coding
  assistants* (Claude Code, etc.) that scaffolds building an ElevenLabs voice
  integration, i.e. a **dev-tooling meta-layer** artifact, not a capability
  declaration consumed at runtime by a deployed voice agent itself.
- **Fence**: cross-session-accumulating (skills are persisted files, reused
  indefinitely across future sessions — this is the format's entire point).
- **Omni role**: n/a (text/coding-agent domain).
- **Delta vs archive**: NEW, with a first-class **negative**: the field's most
  mature, most widely adopted "skill declaration format" has not yet been
  ported to govern a deployed voice/omni agent's own runtime tool/skill set —
  only to the coding assistants that build voice software.
- URLs: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills ,
  https://github.com/anthropics/skills ,
  https://github.com/elevenlabs/skills/blob/main/speech-engine/SKILL.md

## 13. Agent Skills survey — formalizes a governance gate, but a security gate, not (yet) S2's reward gate

- **Problem**: as skill libraries scale (community-contributed, autonomously
  discovered), how should acquisition, composition, and admission be
  governed?
- **Genealogy / origin**: LLM/coding-agent domain survey (accepted at the
  "Agent Skills '26" workshop, AAMAS-adjacent).
- **Training-free**: yes for the skill mechanism itself ("dynamic capability
  extension without retraining"); separately covers RL-based skill
  *acquisition* (SEAgent, compositional synthesis) which is fine-tuned.
- **Axis / verdict**: **constraint** — proposes a "four-tier, gate-based
  permission model that maps skill provenance to graduated deployment
  capabilities" (a "Skill Trust and Lifecycle Governance Framework"), motivated
  by a measured **26.1% of community-contributed skills contain
  vulnerabilities**. Verdict n/a for voice (no audio/speech content at all).
- **Fence**: cross-session-accumulating (skill libraries growing over time).
- **Omni role**: n/a.
- **Delta vs archive**: **CONFIRMS with a caveat** — S2 found the load-bearing
  admission criterion was *verifiable-reward* utility (curated +16pp vs.
  self-generated ~0). This survey's real-world governance answer to "what
  gates a skill?" is instead **security/provenance trust**, not measured task
  utility — a partially orthogonal control law. Both may be needed; neither
  has been jointly instantiated for voice agents.
- URL: https://arxiv.org/abs/2602.12430 (Xu, Yan)

## 14. SAGE (skill-library self-improvement via GRPO) — S2's reward gate, reinvented, still fine-tuned, still text/GUI

- **Problem**: how should an agent's skill library grow so that skills are
  both high-quality and correctly reused, rather than accumulating noise?
- **Genealogy / origin**: LLM/GUI-agent domain (RL post-training), native to
  text/computer-use agents; untransferred to speech.
- **Training-free**: **no** — extends GRPO with "Sequential Rollout" (skills
  from prior tasks persist into later ones) and a "Skill-integrated Reward" =
  verifiable outcome-based reward + an extra reward for skill quality/
  utilization. This bakes the acceptance gate into the training objective
  itself, not an inference-time filter.
- **Axis / verdict**: **element** (skill library) governed by a **constraint**
  (the composite verifiable+quality reward, functioning exactly as S2's
  acceptance gate, just implemented as a training signal); verdict new-info
  within its own (text/GUI) domain.
- **Fence**: cross-session-accumulating.
- **Omni role**: n/a.
- **Delta vs archive**: **CONFIRMS** S2's core finding (a verifiable-reward-
  gated skill signal outperforms undifferentiated self-generation) in the
  clearest form found this lane — but via fine-tuning, and with no speech-
  domain analogue located.
- URL: https://arxiv.org/abs/2512.17102 (submitted 2025-12)

## 15. IHBench — a structured-workflow "skill" scaffold, and frozen models fail it

- **Problem**: voice agents following a structured, multi-stage workflow
  (skip conditions, failure handling, termination conditions — effectively a
  declared procedural "skill"/plan) get interrupted mid-execution by real
  users; do they recover and resume the plan?
- **Genealogy / origin**: speech-domain, native; 10 enterprise domains
  (SaaS, financial services, healthcare, telecom, ecommerce, travel,
  education, government, subscription media, professional services).
- **Training-free**: yes — evaluates off-the-shelf/frozen models.
- **Axis / verdict**: **usage-pattern** (the structured workflow is a
  prompted/declared plan, not a new-info element) — verdict **read-out**:
  "off-the-shelf models perform poorly at recovering from interruptions,"
  struggling to resume structured task execution after being interrupted —
  the workflow-scaffold usage pattern alone does not confer robustness.
- **Fence**: single-session.
- **Omni role**: hybrid.
- **Delta vs archive**: NEW; supports the MAIN THESIS by negative example — a
  pure prompting/orchestration pattern (declared workflow) over a frozen model
  does not cross the interruption-recovery capability boundary.
- URL: https://arxiv.org/abs/2606.19595 (submitted 2026-06-19; Salimi, Ma,
  Tang, Shen, Li, Smola)

---

## Cross-cutting synthesis

**On the MAIN THESIS (element vs. usage-pattern crossing).** Every clear,
positive capability-crossing result found in this lane traced to a
**decorrelated added element** — a second model (VoiceAgentBench's dedicated
ASR system; AudioToolAgent's separate audio-LM tools behind a text-only
coordinator), or a genuine external tool/connector (AURA's calendar/email/
search APIs; Speech-Copilot's modularized toolset). Every case where *only*
the usage pattern/harness changed and no new element was added — τ-Voice
(same model class, moved from text to voice modality), IHBench (added a
structured-workflow prompt, no new model/tool) — showed the capability
**collapse or stay bounded**, never cross a new boundary. No counter-example
(a usage-pattern-only crossing) was found in this lane.

**On S2 (verifiable-reward acceptance gate).** τ²-bench/τ-Voice supply the
measurement substrate (DB-state-verifiable pass@k) the rest of the field's
tool-use claims lean on. Two 2025-12/2026 threads independently re-derive
S2's shape outside speech: SAGE (2512.17102) bakes a "verifiable outcome +
skill-quality" reward directly into GRPO training — the closest match to
S2's finding, but fine-tuned and text/GUI-only; the Agent Skills survey
(2602.12430) instead proposes a **security/provenance** gate (motivated by a
measured 26.1% vulnerability rate in community skills), which is a different
control law than reward-verified utility. **No work in this lane combines a
verifiable-reward acceptance gate with a skill library for a speech/voice
agent** — this remains open, extending L4's N1/N2 negatives (no published
pass@k or prompt-opt on any voice-agent benchmark) specifically to the
skill-library axis.

**On "harness/MCP/SKILL.md" as elements.** MCP and Agent Skills are both
mature, training-free, standardized connector formats — but both are
text/coding-agent-native and **not yet ported to govern a deployed voice/omni
agent's own runtime capability set**: MCP-for-voice is real but still
text-transcript-mediated (no audio-native tool-call message format found);
Agent Skills' one voice-adjacent adoption (ElevenLabs) operates at the
dev-tooling layer (skills *for* Claude Code to scaffold voice products), not
the runtime layer (skills *consumed by* the deployed voice agent). AU-Harness
is the one genuinely voice-native "harness" found, and it is an eval toolkit,
not a skill/tool runtime — it does, however, formally include function-calling
as a first-class evaluated task category and reports it as a weak point.

---

## Verifier notes (2026-07-06 adversarial pass)

**Method**: WebFetch'd 17 of the lane's cited URLs (all 15 items' primary
sources, plus the two supplementary MCP-ecosystem sources) and cross-checked
author lists, dates, quoted numbers, and paraphrased mechanisms against the
fetched abstracts/pages; ran 3 WebSearches to corroborate facts not settled by
a single fetch (Sierra affiliation for τ²-bench, the OpenAI Realtime-API MCP
update date, the "32 tools" Agent Skills adoption figure, and the P1/P2 anchor
IDs cross-referenced against `2026-07-04-stage1-L4-speech-agentic.md`).

**Findings**:

1. **Fixed — citation/attribution mismatch (item 11, MCP for voice agents).**
   The claim "OpenAI's Realtime API added built-in remote-MCP-server support
   (Aug 2025 update, per the OpenAI cookbook)" attributed a true fact to the
   wrong source. The cited cookbook URL (`mcp_powered_agents_cookbook`) uses
   the **Agents SDK** with a **chained** STT→agent→TTS pipeline and contains
   no mention of the Realtime API, remote MCP, or August 2025 — it is good
   evidence for the "text-mediated bridge" quote used two paragraphs later,
   but not for the Realtime-API-update claim it was parenthetically pinned
   to. The underlying fact is real and independently well-documented
   (OpenAI's "Introducing gpt-realtime" announcement, 2025-08-28, corroborated
   by MarkTechPost/InfoWorld coverage) — I corrected the attribution in the
   Genealogy bullet and added the correct supporting URL
   (`openai.com/index/introducing-gpt-realtime/`) to the URL list, keeping the
   cookbook URL (relabeled) since it does support the transport-mediation
   quote.
2. **Flagged, not changed — item 7 (Full-Duplex-Bench-v3) axis call looks
   inconsistent with the lane's own pattern.** Items 3 (τ²-bench), 6
   (Audio2Tool), and 10 (AU-Harness) are all benchmarks/harnesses and are
   correctly axis-tagged **constraint** (measurement substrate, not itself a
   capability-crossing claim). Item 7 is likewise a benchmark/harness (six
   frozen systems compared on tool-use-under-disfluency), yet is axis-tagged
   **element** on the reasoning that "native single-model S2S vs. two-element
   cascade is exactly an element-count comparison." That reasoning retrofits
   an element/usage-pattern label onto the benchmark itself rather than onto
   any single crossing claim the benchmark supports, and the verdict is
   already correctly hedged to n/a ("comparative benchmark, not a single
   crossing claim"). Recommend re-tagging item 7's axis to **constraint** for
   consistency with items 3/6/10 — left as-is pending owner call since it is
   a judgment call, not a factual error.
3. **Confirmed, no change needed.** All 15 items' primary arXiv/URL citations
   resolve to the paper/page described, with authors, dates, and every
   quoted/paraphrased number (AURA's 90% task success, 92.75%
   VoiceBench-OpenBookQA, 4.39 AlpacaEval; τ-Voice's 85% text vs. 31-51%/26-38%
   voice and 79-90%-agent-attributed failures; VoiceAgentBench's 60.6%; Stream
   RAG's 11.1%→34.2% AudioCRAG; AudioToolAgent's 77.50/77.00/61.90 MMAU/MMAR/
   MMAU-Pro and text-only-coordinator design; the Agent Skills survey's 26.1%
   vulnerability figure and four-tier governance model; SAGE's GRPO +
   Sequential Rollout + Skill-integrated Reward design) verified against the
   fetched source. The τ²-bench "Sierra" affiliation (not stated in the arXiv
   abstract itself) is corroborated by the `sierra-research` GitHub org and
   Sierra's own blog post. The MCP 2025-11-25 spec version and the Agent
   Skills "32 tools" adoption figure both check out against independent
   sources, though the latter isn't directly evidenced by any of the three
   URLs item 12 cites (Anthropic's own post doesn't state a tool count) — a
   minor sourcing gap, not a wrong number. No invented papers, no dead links,
   no wrong-paper links found among the checked set.
4. **Framework-verdict spot check (new-info vs. read-out, element vs.
   usage-pattern).** Items 1, 2, 5, 8, 9 (element/new-info via a genuinely
   decorrelated added model or external tool/connector), 4, 6, 15
   (usage-pattern-or-modality-only change → read-out/collapse, no crossing),
   and 3, 10, 13 (constraint/methodology, verdict n/a) all read as defensible
   applications of the framework once checked against the underlying papers'
   actual designs — in particular item 9's "text-only coordinator that never
   touches the audio" and item 5's "decorrelated ASR beats one frozen
   SpeechLM" calls both survive a close read of the source abstracts. Item 7
   is the one call flagged above as inconsistent, not wrong per se.
5. **Recency and negatives.** All dated items fall in 2025-01..2026-07 except
   item 2 (Speech-Copilot, 2024-07), which is explicitly and correctly flagged
   as a pre-window genealogy root rather than smuggled in as an in-window
   result. Negatives are well represented and not cherry-picked away: item 4
   (large text→voice capability collapse), item 6 (compositional/acoustic
   degradation), item 8 (training-free judged insufficient, fine-tuning used
   instead), item 11 (no audio-native MCP tool-call format exists), item 12
   (Agent Skills not yet ported to any deployed voice-agent runtime), and item
   15 (frozen models fail interruption-recovery) together substantiate the
   "no counter-example found" claim in the cross-cutting synthesis rather than
   just asserting it.

**Net**: lane holds up well. One real (now-fixed) citation-attribution error;
one defensible-but-debatable axis classification flagged for owner judgment;
everything else checked out.
