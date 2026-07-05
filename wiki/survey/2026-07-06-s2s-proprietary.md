---
title: Stage-1 lane — Proprietary S2S / realtime voice agents (OpenAI, Google, xAI, Amazon, Microsoft)
date: 2026-07-06
stage: 1-argumentation
lane: s2s-proprietary
---

> Stage-1 problem-definition lane. Method: literature/vendor-documentation argumentation only;
> every claim below was fetched or search-verified live (WebSearch/WebFetch) on 2026-07-06.
> Scope: publicly disclosed architecture, tool-use, and memory design of proprietary
> speech/omni realtime-voice agent stacks shipped or updated 2025-01 through 2026-07:
> OpenAI Realtime API / gpt-realtime / ChatGPT Voice, Google Gemini Live API (native audio),
> xAI Grok Voice Agent, Amazon Nova Sonic, Microsoft Copilot Voice / MAI-Voice-2. Tests the
> project's ELEMENT / USAGE-PATTERN / CONSTRAINT framework against what vendors actually built
> and disclosed, and tags each vendor's disclosure quality (paper/system-card vs blog vs docs-only).

## Per-item template legend
(1) recognized problem it addresses; (2) genealogy — origin-domain [LLM|VLM|speech], transfer
[native|ported|untransferred]; (3) training-free vs fine-tuned (does it change weights?);
(4) three-axis class [element|usage-pattern|constraint] + verdict (new-info element vs
usage-pattern-over-one-model); (5) fence [single-session|cross-session-accumulating];
(6) omni role [sensor|brain|hybrid|n/a]. Delta vs archive tag on every claim.

---

### C1 — OpenAI gpt-realtime: native audio-in/audio-out model replacing the cascaded "Standard Voice Mode"

(1) Problem: STT→LLM→TTS cascades lose paralinguistic signal (tone, emphasis, non-verbal cues)
and add 1-3s of round-trip latency per exchange; OpenAI's fix is a single model trained to
consume and emit audio directly. (2) Genealogy: origin **LLM** (GPT-4o, announced May 2024,
[system card](https://arxiv.org/abs/2410.21276) Aug 2024 — "a single neural network trained
end-to-end across text, vision, and audio" — this is the pre-window genealogy root, tagged);
transfer **native** into the Aug-2025 production `gpt-realtime` release. (3) **Fine-tuned**
(the base model itself is pretrained/fine-tuned — not training-free; recorded here only as
architecture background for the frozen-model layer this project sits above). (4) Axis:
**element** — the gain over the old cascade comes from a differently-trained model (more
audio-centric pretraining data), not a prompting/orchestration change over the old model:
OpenAI attributes the jump from 65.6% to 82.8% on Big Bench Audio to being "extensively
pretrained on specialized audio-centric datasets." Verdict: **new-info element** (new training
data, not usage pattern). (5) n/a (base-model property, not a session feature). (6) **hybrid**
(same network is both sensor — audio understanding — and brain — response generation).
Disclosure quality: **medium** — vendor blog + API model card, reuses the 2024 GPT-4o system
card for safety evaluation rather than publishing a new one for gpt-realtime; no architecture
diagram or audio-encoder/decoder technical detail published.
Sources: [Introducing gpt-realtime](https://openai.com/index/introducing-gpt-realtime/) (2025-08) ·
[GPT-4o System Card](https://arxiv.org/abs/2410.21276) (2024-08, genealogy root) ·
[Realtime and audio guide](https://developers.openai.com/api/docs/guides/realtime).
Delta: **NEW** (vendor-architecture disclosure angle not previously catalogued in the archive).

### C2 — OpenAI Realtime API remote-MCP tool support (Aug 2025)

(1) Problem: voice agents need live access to external systems (CRMs, DBs, calendars) without
each developer hand-wiring every integration. (2) Genealogy: origin **LLM** (MCP is Anthropic's
protocol, ported into a speech runtime); transfer **ported**. (3) Training-free (weights
unchanged; this is a runtime/session-config feature — "point the session to a different MCP
server, and those tools become available right away" — with tool calls executed by the Realtime
API itself, not the client). (4) Axis: **element** (connector/tool) — this is the cleanest
proprietary-vendor demonstration in this lane of the thesis's central claim: capability is added
by plugging in an external system (a remote MCP server), not by re-prompting the same frozen
model. Verdict: **new-info element**. (5) cross-session-accumulating only if the remote MCP
server itself has persistent state (the Realtime session itself is not persistent — see C3).
(6) **hybrid** (model decides when to call the tool; the tool is the new-info surface).
Disclosure quality: **medium-high** — dedicated docs page with request/response schema, plus an
independent trade-press confirmation.
Sources: [Realtime with tools (MCP) guide](https://developers.openai.com/api/docs/guides/realtime-mcp) ·
[OpenAI adds MCP and SIP support to gpt-realtime — InfoWorld](https://www.infoworld.com/article/4048375/openai-adds-mcp-and-sip-support-to-gpt-realtime-for-smarter-voice-based-agents.html) (2025-08).
Delta: **NEW**.

### C3 — OpenAI Realtime API is stateless server-side; persistent "Memory" lives only in the ChatGPT consumer product, not the developer API

(1) Problem: cross-session personalization/continuity vs. per-call statelessness. (2) Genealogy:
**LLM**-domain pattern (RAG-style external memory store) ported into voice. (3) Training-free
(external key-value/vector store bolted onto a frozen model; no weight change). (4) Axis:
**element** — but the important negative finding is that the *developer* Realtime API explicitly
does **not** provide this element: "the real-time session itself does not persist memory...
long-term identity, preferences, and cross-session memory are left to the application" (max
session **60 minutes** as of the Sept-2025 GA update — up from 30 minutes just before GA and 15
minutes in the original 2024 beta, per [OpenAI developer notes](https://developers.openai.com/blog/realtime-api)
2025-09-12 — corrected by verifier pass 2026-07-06, was misstated as 15 min; 128k-token context
window is current per the May-2026 `gpt-realtime-2` update, up from 32,768 tokens at Sept-2025 GA). The
*consumer* ChatGPT product instead ships an
explicit memory element — "saved memories" (user-asked-to-remember facts) plus "chat history"
(model-mined insights referenced across all past chats) — which OpenAI itself frames as a
distinct, controllable, inspectable store, i.e., a genuine new-info element layered outside the
frozen conversational weights. Verdict: **new-info element**, but note it is **not** part of the
proprietary voice-*agent* (developer) stack surveyed elsewhere in this lane — a first-class
negative/empty cell: no vendor in this lane ships persistent cross-session memory *in the voice
developer API itself* as of 2026-07. (5) API session = **single-session**; ChatGPT product
memory = **cross-session-accumulating**. (6) n/a (memory is a connector, not sensor/brain).
Disclosure quality: **high** for the consumer feature (dedicated OpenAI blog posts + Help Center
FAQ); **medium** for the API limitation (stated plainly in docs, no dedicated writeup).
Sources: [OpenAI Realtime API docs — session/memory](https://developers.openai.com/api/docs/guides/realtime-conversations#function-calling) ·
[Memory and new controls for ChatGPT](https://openai.com/index/memory-and-new-controls-for-chatgpt/) (2025) ·
[Memory FAQ — OpenAI Help Center](https://help.openai.com/en/articles/8590148-memory-faq).
Delta: **NEW** (the API-vs-product memory split is not in the archive).

### C4 — OpenAI Realtime API safety: a decorrelated, separately-weighted moderation/classifier layer runs alongside the frozen conversational model

(1) Problem: content-safety enforcement over live audio without relying on the conversational
model to police itself. (2) Genealogy: **LLM**-domain moderation-classifier pattern
(`omni-moderation`), ported to run continuously over Realtime sessions. (3) Training-free from
the conversational model's point of view (the classifier is a separate trained artifact).
(4) Axis: **element** — "the Realtime API leverages the same audio safety infrastructure built
for Advanced Voice Mode" via "active classifiers over Realtime API sessions" that can halt a
session; this is a genuinely different-weights second system monitoring the first, i.e. the
**verifier-as-tool** fork of the project's verification thesis (a real element), not the weak
**verifier-as-role** fork (same model re-prompted as "critic"). Verdict: **new-info element**,
consistent with (not merely read-out of) the project's prior mem0 note on omni-verifier
decorrelation. (5) n/a. (6) **sensor**-like (the classifier only flags; it doesn't generate the
reply). Disclosure quality: **low-medium** — described only in prose in safety-best-practices
docs and OpenAI's Realtime-API launch materials; no published architecture or accuracy numbers
for the audio-classifier component specifically (the general `omni-moderation` model card covers
text/image, not audio, so exactly how audio-session classification works is not itself
documented — a disclosure gap, first-class negative).
Sources: [Safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices) ·
[omni-moderation model card](https://developers.openai.com/api/docs/models/omni-moderation-latest) (audio not covered — gap noted).
Delta: **NEW**.

### C5 — Gemini Live API: unified native-audio model plus explicit built-in tool chaining (Google Search grounding, code execution, custom functions)

(1) Problem: same STT→LLM→TTS-cascade-latency problem as C1, plus grounding hallucination-prone
answers in live search/computation. (2) Genealogy: origin **LLM+VLM** (Gemini's native
multimodality) with the Search/code-execution tools ported from the standard `generateContent`
Gemini API. Transfer: **native** (audio path) / **ported** (tool layer, reused verbatim from
text Gemini). (3) Training-free at the session layer (tools and grounding are runtime-config,
not weight changes); the underlying native-audio *model itself* is a separately trained/released
checkpoint (`gemini-2.5-flash-native-audio-preview`) — fine-tuned relative to the base LLM.
(4) Axis: **element** for the tools (Search = knowledge element, code-execution = tool element)
— Google's own docs give a concrete multi-tool chain example: "Plot Denis Villeneuve movies"
triggers Search then code-execution in sequence, i.e., two decorrelated external elements
composed, not a usage-pattern trick over one frozen model. Verdict: **new-info element**.
(5) single-session (each Live session; see C6 for cross-session extension). (6) **hybrid**.
Disclosure quality: **medium** — detailed API/tools docs, but no dedicated technical-report
section found for the native-audio path specifically (the general Gemini 2.5 report,
[arXiv:2507.06261](https://arxiv.org/abs/2507.06261), covers the model family broadly; audio
encoder/decoder specifics are not broken out in available search/fetch).
Sources: [Live API capabilities guide](https://ai.google.dev/gemini-api/docs/live-guide) ·
[Tool use with Live API](https://ai.google.dev/gemini-api/docs/live-api/tools) ·
[Gemini 2.5 Technical Report](https://arxiv.org/abs/2507.06261) (2025-07).
Delta: **NEW**.

### C6 — Gemini Live context-window compression ("infinite" sessions): a usage-pattern budget trick, not a new-info element

(1) Problem: native-audio tokens accumulate at ~25 tokens/sec against a 128k-token context cap,
so an uncompressed session hard-terminates (15 min audio-only, 2 min audio+video). (2) Genealogy:
**LLM**-domain sliding-window/summarization context management, ported to voice. (3)
Training-free (pure inference-time context management). (4) Axis: **usage-pattern** — this is
the clean negative/confirmatory case for the thesis: "the server uses a sliding-window mechanism
to automatically discard the oldest turns or summarize them to maintain the context size" — no
new information is added; old information is thrown away or lossily compressed to fit the same
frozen model's fixed context budget. It manages an inference-substrate CONSTRAINT (see C6b) but
does not cross a capability boundary — it only postpones running out of room. Verdict:
**usage-pattern**, bounded by (does not exceed) what the uncompressed session could already do.
(5) session-level only — "resumption tokens are valid for 2 hr," and after that the state is
discarded, so this is explicitly **not** cross-session-accumulating memory; it is time-boxed
continuity within one logical conversation. (6) n/a. Disclosure quality: **medium-high** —
precise, mechanism-level docs (token math, sliding-window behavior, resumption-token TTL all
stated numerically).
Sources: [Session management with Live API](https://ai.google.dev/gemini-api/docs/live-session) ·
[Live API capabilities guide](https://ai.google.dev/gemini-api/docs/live-guide).
Delta: **NEW** (this specific usage-pattern-vs-element distinction is not in the archive).

### C6b — Real-time token-budget vs. continuous audio stream is a CONSTRAINT (inference-substrate), not an element or usage pattern

(1) Problem: full-duplex/real-time operation is fundamentally rate-limited by how fast tokens
accumulate versus context capacity, independent of model quality. (2) Genealogy: **speech**-domain
(no text-LLM analog: text sessions don't continuously consume tokens merely by the clock ticking).
(3) n/a (architectural property, not a trainable/promptable lever). (4) Axis: **constraint** —
this directly supports the project's organizing framework's claim that real-time/full-duplex
is a base-architecture/inference-substrate property: Gemini Live's 128k window at ~25 tok/s
audio gives a hard ceiling of roughly 85 minutes of raw audio tokens regardless of prompt or
orchestration; OpenAI's Realtime session cap (**60 min** as of the Sept-2025 GA update, up from
30/15 min pre-GA; resettable only via reconnect/SIP — corrected by verifier pass 2026-07-06, was
misstated as 15 min) is the same class of constraint expressed as a wall-clock limit instead of a
token-budget limit.
Verdict: **constraint**, not element/usage-pattern. (5) n/a. (6) n/a.
Disclosure quality: **high** for Google (explicit numeric limits published); **medium** for
OpenAI (limit stated, less numeric derivation shown).
Sources: [Live API capabilities guide](https://ai.google.dev/gemini-api/docs/live-guide) ·
[Session management with Live API](https://ai.google.dev/gemini-api/docs/live-session) ·
[OpenAI Realtime session guide](https://developers.openai.com/api/docs/guides/realtime-conversations#function-calling).
Delta: **NEW**.

### C7 — xAI Grok Voice Agent: fully in-house native audio stack, tool connectors, weakest architecture disclosure of the five vendors surveyed

(1) Problem: same cascade-latency problem; xAI's stated fix is training every stack component
(VAD, tokenizer, audio model) in-house rather than composing off-the-shelf components. (2)
Genealogy: **speech**-domain, claimed **native** ("processes incoming audio and generates
responses simultaneously... largely eliminating the pauses between turns"). (3) Fine-tuned
(base model); tool/session layer is training-free runtime config. (4) Axis: **element** for the
server-side tool connectors (web search, X search, file search, MCP — xAI's own docs list these
as server-executed tools distinct from client-side custom functions) — same connector-element
pattern as C2/C5, now confirmed across a third independent vendor. Verdict: **new-info element**
(tools) / model itself not evaluable as element-vs-pattern from public disclosure. (5) Session
resumption caches turns and replays prior context on reconnect ("the model stays conditioned on
what was said earlier"), with history expiring after 30 minutes — **single-session**
(time-boxed), same class as Gemini's C6, not durable cross-session memory. (6) **hybrid**.
Disclosure quality: **low** — direct inspection of xAI's own Voice Agent API technical docs
(`docs.x.ai`) found **no architecture diagram, no reference to native-vs-cascaded implementation
detail beyond marketing prose, and no technical paper or system card**. Corrected by verifier pass
2026-07-06: an earlier draft of this entry additionally claimed "no benchmark numbers," which is
not accurate — the companion launch announcement (already cited below) does self-report one bare
headline figure ("ranks #1 on Big Bench Audio," 92.3%, sub-1-second average time-to-first-audio),
independently corroborated by Artificial Analysis (see C11). But that number arrives with no
methodology, no per-category breakdown, and no architecture detail attached — a self-reported
marketing headline, not a technical disclosure. Net verdict unchanged: xAI is still the thinnest
disclosure of the vendors in this lane on *architecture* (no diagram/paper/system-card) — contrast
Amazon C8 and OpenAI's reused GPT-4o system card C1 — but the precise gap is "one unmethodologized
self-reported number," not "zero numbers."
Sources: [Voice Agent API — xAI Docs](https://docs.x.ai/developers/model-capabilities/audio/voice-agent) ·
[Grok Voice Agent API — xAI announcement](https://x.ai/news/grok-voice-agent-api).
Delta: **NEW**.

### C8 — Amazon Nova Sonic: unified single-model architecture with a named companion technical report — the highest-disclosure vendor in this lane

(1) Problem: same cascade problem, solved via "a single integrated model" unifying speech
understanding and generation ("without requiring a separate model") rather than composing ASR +
LLM + TTS. (2) Genealogy: **speech**-domain native claim. (3) Fine-tuned (base model); function
calling/RAG is training-free runtime config. (4) Axis: **element** for tool use ("function
calling (also known as tool use) and agentic workflows to interact with external services and
APIs... including knowledge grounding with enterprise data using RAG" — RAG is explicitly a
knowledge-connector element). Nova 2 Sonic adds *asynchronous* tool calling ("doesn't pause but
continues to respond to new user input while tools run in the background") — this specific
async-dispatch behavior is a **usage-pattern**/orchestration refinement layered on top of the
tool element (it changes how the existing element's results are surfaced mid-dialogue, adding no
new information source itself), and it converges with materially the same design independently
adopted by Gemini Live (`NON_BLOCKING` function behavior, C5) and OpenAI gpt-realtime
("long-running function calls will no longer disrupt the flow of a session") — three
independent vendors converging on the same non-blocking-tool-call pattern is itself a notable
cross-vendor engineering convergence claim. Verdict: tool = **new-info element**; async dispatch
= **usage-pattern**. (5) single-session (bidirectional stream API for one call); no cross-session
memory disclosed. (6) **hybrid**. Disclosure quality: **medium-high** — Amazon publishes a
named ["Amazon Nova Sonic: Technical Report and Model Card"](https://assets.amazon.science/86/bb/4316d28940bd9a719abb28f45aaf/amazon-nova-sonic-technical-report-and-model-card-6-12.pdf)
PDF (title/existence confirmed; full text not machine-extractable in this pass, so its
architecture-diagram/ablation depth is **unverified** and excluded from the verdict above — a
first-class disclosure-quality gap: a report exists but this survey could not confirm its
technical depth).
Sources: [Introducing Amazon Nova Sonic](https://aws.amazon.com/blogs/aws/introducing-amazon-nova-sonic-human-like-voice-conversations-for-generative-ai-applications/) (2025-04) ·
[Introducing Amazon Nova 2 Sonic](https://aws.amazon.com/blogs/aws/introducing-amazon-nova-2-sonic-next-generation-speech-to-speech-model-for-conversational-ai/) ·
[Nova Sonic Technical Report and Model Card (PDF, title verified, depth unverified)](https://assets.amazon.science/86/bb/4316d28940bd9a719abb28f45aaf/amazon-nova-sonic-technical-report-and-model-card-6-12.pdf).
Delta: **NEW**.

### C9 — Microsoft Copilot Voice / MAI-Voice-2: publicly disclosed as separately-named ASR and TTS models, not confirmed as a native end-to-end S2S stack

(1) Problem: same latency/fidelity problem, but Microsoft's own disclosure (Build 2026,
2026-06-02) names **MAI-Transcribe-1.5** (ASR: "turn noisy audio into precise, domain-specific
transcripts," 43 languages) and **MAI-Voice-2** (TTS: "expressive, natural-sounding speech
generation," 15 languages) as *separate, individually-branded* models feeding "Azure Copilot,"
with a reasoning/orchestration layer (implied to be a Microsoft Foundry-hosted LLM, model
unspecified) in between. (2) Genealogy: **speech**-domain, transfer status **untransferred**
w.r.t. the native-single-model claim other vendors make — Microsoft's own materials, unlike
OpenAI/Google/xAI/Amazon, do not claim (and, per direct inspection, do not deny) an end-to-end
audio-to-audio model; they describe a modular stack. (3) Fine-tuned (each named component).
(4) Axis: this is the one vendor in the lane whose public disclosure most resembles the
**cascaded** architecture the others explicitly claim to have replaced — worth flagging as a
negative/uncertain case rather than assuming convergence: **not all 2025-2026 proprietary voice
stacks are native S2S**; at least one major vendor's public messaging is consistent with (though
does not explicitly confirm) a still-modular ASR+LLM+TTS pipeline. Verdict: **unclear/insufficient
disclosure** — excluded from a definitive element/pattern verdict; recorded as a first-class
disclosure gap. (5) n/a (undisclosed). (6) MAI-Transcribe = **sensor**, MAI-Voice-2 = output
component (not brain). Disclosure quality: **low** for the integration architecture (component
models are named and demoed; how they compose into "Copilot Voice" is not documented in any
source found, including the dedicated MAI launch article, which explicitly omits this).
Sources: [Introducing MAI-Voice-2 — Microsoft AI](https://microsoft.ai/news/mai-voice-2/) ·
[Building a hill-climbing machine: launching seven new MAI models](https://microsoft.ai/news/building-a-hillclimbing-machine-launching-seven-new-mai-models/) (2026-06) ·
[Azure OpenAI GPT-4o-Realtime-Preview announcement](https://azure.microsoft.com/en-us/blog/announcing-new-products-and-features-for-azure-openai-service-including-gpt-4o-realtime-preview-with-audio-and-speech-capabilities/) (Copilot Voice's separately-documented OpenAI-based path, for contrast).
Delta: **NEW**.

### C10 — τ-Voice cross-vendor benchmark: all three native-audio proprietary APIs retain only 30-45% of their own text-mode tool-use capability

(1) Problem: does the proprietary vendors' "native S2S, no info loss" architecture claim (C1,
C5, C7, C8) actually hold up on verifiable, tool-using agentic tasks, not just audio-reasoning
QA? (2) Genealogy: **speech**-domain benchmark directly extending **LLM**-domain τ²-bench
(Sierra) into full-duplex voice; transfer **native** (same DB-state verifiable-reward protocol,
new audio-realistic user simulator with accents/noise/packet-loss). (3) n/a (evaluation, not a
method). (4) Axis: this is an evaluation finding that **bounds the element claims above** —
across three independently-built, independently-disclosed "native audio" proprietary systems,
task-completion pass@1 is: OpenAI gpt-realtime-1.5 49%/35% (clean/realistic), Google
gemini-live-2.5-flash-native-audio 31%/26%, xAI Grok Voice Agent 51%/38% — versus the **same
underlying task family's text-mode** GPT-5-reasoning baseline at 85% pass@1 — with 79-90% of
voice-agent failures being agent-behavior failures (hallucinated tool completions, silent
non-response) rather than transcription errors. This says the C1/C5/C7/C8 "no information lost
by going native-audio" architecture claims are not supported at the tool-use/task-completion
level: whatever new-info element (native audio training) each vendor added, it has not closed
the modality gap on agentic tasks. (5) single-session (τ-Voice evaluates one episode at a time).
(6) n/a (evaluation, not a deployed role). Disclosure quality: **high** — peer-reviewable arXiv
paper with a public methodology, per-vendor breakdown, and an accent-ablation (-18pp on xAI's
Retail domain vs near-zero for Google).
Sources: [τ-Voice: Benchmarking Full-Duplex Voice Agents on Real-World Domains](https://arxiv.org/abs/2603.13686) (2026-03) ·
[τ-Voice, HTML full text](https://arxiv.org/html/2603.13686v1).
Delta: **CONFIRMS** — this exact benchmark and these exact per-model numbers are already
recorded in the archive's `2026-07-04-stage1-L4-speech-agentic.md` (P1/C01); this lane
**reproduces it deliberately** to anchor it to the vendor-architecture-disclosure side of the
story (the vendors whose "native, no cascade" claims are being tested) rather than re-deriving
new numbers. No new measurement claimed here beyond the cross-referencing itself.

### C11 — Benchmark leaderboard churn (Big Bench Audio) measures single-turn audio *reasoning*, not agentic *task completion* — an evaluation-target gap that itself explains why C1/C5/C7 "wins" coexist with C10's collapse

(1) Problem: vendors race each other on Big Bench Audio (xAI Grok Voice Agent reported 92.3%,
"surpassing Gemini 2.5 Flash Native Audio and GPT Realtime," per Artificial Analysis) while
τ-Voice shows the same systems collapsing on tool-use tasks — these are not contradictory, they
are measuring different things. (2) Genealogy: **LLM**-domain origin (Big Bench Hard questions
adapted to audio by Artificial Analysis/HF); transfer **ported**, single-turn QA-style, no
environment/tool-call verification. (3) n/a (evaluation methodology note). (4) Axis: not itself
an element/pattern claim — it is a **methodology/scope gap**: reasoning-QA benchmarks and
agentic/tool-use benchmarks are measuring disjoint capability slices, and the proprietary
vendors' public benchmark claims (Big Bench Audio) are silent on the slice where they actually
struggle (τ-Voice). First-class negative: **no proprietary vendor in this lane publishes its own
pass@k/tool-use agentic benchmark number** — all such numbers (τ-Voice) come from independent
third-party/academic evaluation, not vendor self-report. (5)/(6) n/a.
Disclosure quality: **medium** (Artificial Analysis is an independent benchmarking vendor, not
the model vendors themselves, publishing on X/its own site with a stated methodology page).
Sources: [Artificial Analysis on X — Grok Voice Agent Big Bench Audio 92.3%](https://x.com/ArtificialAnlys/status/2001388724987527353) ·
[Speech Reasoning Benchmarking Methodology — Artificial Analysis](https://artificialanalysis.ai/methodology/speech-to-speech-benchmarking) ·
[Evaluating Audio Reasoning with Big Bench Audio](https://huggingface.co/blog/big-bench-audio-release) (2024-12, genealogy root).
Delta: **NEW**.

### C12 — Gemini 2.5 Flash Native Audio "Thinking" variant: disclosure too thin to classify as element vs. usage-pattern (first-class negative)

(1) Problem: Google offers native-audio dialog "with or without thinking capabilities," trading
latency (0.63s → 3.87s time-to-first-audio) for a claimed reasoning/quality gain. (2) Genealogy:
**LLM**-domain (extended reasoning/chain-of-thought before answering), ported to voice. (3)
**Unknown/unverified** — public material variously describes the Thinking variant as "an
advanced variant" (implying a separately trained/tuned checkpoint = element) and elsewhere as
the same model given a reasoning budget (implying usage-pattern/test-time compute over one
frozen model) — this survey could not find a primary Google source that disambiguates whether
`gemini-2.5-flash-native-audio-preview` (Thinking) is a distinct set of weights from the
non-Thinking variant or the identical weights with a longer inference budget. (4) Axis:
**deliberately left unclassified** — recorded as a first-class empty-measurement-cell per the
task's hard rules rather than guessed. If it is the same weights, it is a **usage-pattern** case
supporting the thesis (test-time compute is bounded by the oracle ceiling of the same weights);
if it is separately trained, it is an **element** case. This ambiguity is itself worth flagging
for Stage-2: it is exactly the kind of vendor disclosure gap that blocks clean element/pattern
attribution. (5)/(6) n/a pending disambiguation.
Disclosure quality: **low** for this specific question (marketing copy only; no model card
distinguishing the two variants' training provenance found).
Sources: [Advanced audio dialog and generation with Gemini 2.5 — Google blog](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-2-5-native-audio/) ·
[Gemini 2.5 Flash Native Audio Preview model page](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash-native-audio-preview-12-2025).
Delta: **NEW** (negative/gap finding).

---

## Negatives / empty-measurement-cells (first-class)

- **No vendor's developer voice API ships persistent cross-session memory as a native session
  feature** (C3): OpenAI Realtime, Gemini Live, and Grok Voice Agent all cap continuity at
  minutes-to-hours via resumption tokens, not indefinite memory; only OpenAI's *consumer* ChatGPT
  product layers a genuine persistent-memory element outside the voice-agent developer stack.
- **No proprietary vendor self-reports a pass@k/tool-use agentic voice benchmark number** (C11);
  all such numbers in this lane come from independent academic work (τ-Voice), confirming the
  archive's N1 (no published pass@k on voice-agent benchmark) held at the *vendor-disclosure*
  level even as the *independent-evaluation* level has since produced exactly such a number
  (τ-Voice, 2026-03) — a nuance worth carrying into Stage 2 framing.
- **xAI's Voice Agent API documentation contains no architecture diagram or technical paper**
  (C7) — the weakest architecture disclosure among the five vendors surveyed, though (corrected
  2026-07-06) its launch announcement does self-report one unmethodologized Big Bench Audio
  headline number.
- **Amazon's Nova Sonic "Technical Report and Model Card" PDF exists but its content could not be
  machine-extracted in this pass** (C8) — recorded as unverified rather than assumed; the title
  and existence of a dedicated report is itself a disclosure-quality signal relative to vendors
  that publish only blog posts.
- **Whether Gemini's "Thinking" native-audio variant is a separate checkpoint or a prompt/budget
  toggle on the same weights is not disclosed anywhere found** (C12) — blocks a clean
  element-vs-usage-pattern verdict for that one feature.
- **Microsoft's Copilot Voice integration architecture (how MAI-Transcribe-1.5, an unspecified
  reasoning LLM, and MAI-Voice-2 compose) is not documented** (C9) — the only vendor in this lane
  whose disclosure does not confirm a native single-model claim.

## Cross-vendor summary table

| Vendor / system | Claimed architecture | Tool/connector element | Session memory | Disclosure quality |
|---|---|---|---|---|
| OpenAI gpt-realtime / Realtime API | native S2S (reused GPT-4o lineage) | function calling + remote MCP | stateless server-side; 60 min cap (corrected; was 15 min) | medium (blog+docs, reused 2024 system card) |
| OpenAI ChatGPT Voice (consumer) | same model, product-layer memory | n/a | persistent "saved memories" + chat-history mining | high (dedicated blog posts + Help Center) |
| Google Gemini Live (native audio) | native S2S, separate Thinking variant | function calling + Search grounding + code execution | session resumption (2h token, ~10min window) + context-window compression | medium (numeric docs, no dedicated audio architecture paper) |
| xAI Grok Voice Agent | native S2S, fully in-house stack | function calling + web/X/file search + MCP | 30-min resumption cache | low (no diagram, no paper; one unmethodologized self-reported benchmark headline) |
| Amazon Nova Sonic / Nova 2 Sonic | native unified model | function calling + RAG, async tool calls (Nova 2) | not disclosed beyond one bidirectional stream | medium-high (named technical report + model card exists, depth unverified) |
| Microsoft Copilot Voice / MAI-Voice-2 | undisclosed — named separate ASR/TTS models | (inherits Azure OpenAI/Foundry tool layer where used) | not disclosed | low (integration architecture not documented) |

## Notes for synthesis

This lane's strongest contribution to the project's central thesis is **C2/C5/C7/C8**: across
four independent vendors, every genuine capability addition that is legible from public
disclosure is a **connector/tool element** (MCP, RAG, Search, code execution) bolted onto a
frozen-at-inference-time base model — never a role/prompting trick over one model. The clearest
**usage-pattern** case is Gemini's context-window compression (C6): it manages a real constraint
(C6b) but adds no information and cannot cross a capability boundary — exactly the framework's
prediction. **C10 (τ-Voice)** is the load-bearing empirical anchor showing that none of these
vendors' native-audio "element" (better audio pretraining) has closed the modality gap on
agentic/tool-use tasks specifically — reinforcing archive L4-P1 rather than contradicting it,
now traced back to the vendor side. **C9 (Microsoft)** and **C12 (Gemini Thinking)** are flagged
as genuine open disclosure gaps rather than forced into a verdict — Stage 2 should not assume
convergence on "native S2S" across all proprietary vendors without confirming Microsoft's actual
integration architecture, and should not assume Gemini's Thinking mode is pure test-time compute
without vendor confirmation.

## Verifier notes (adversarial pass, 2026-07-06)

An independent verification pass spot-checked 10+ of this lane's citations by direct WebFetch
(where reachable) or WebSearch corroboration, re-derived the framework verdicts, and checked
recency/negatives coverage. Two errors were found and corrected in place above; everything else
checked out.

**Fixed:**
- **C3 / C6b / summary table — OpenAI Realtime session cap was stated as 15 minutes; the current
  (2026-07) limit is 60 minutes.** OpenAI's own [developer notes](https://developers.openai.com/blog/realtime-api)
  (2025-09-12) show the cap moved 15 min (2024 beta) → 30 min → **60 min** at Sept-2025 GA; live
  re-fetch of `developers.openai.com/api/docs/guides/realtime-conversations` on this pass confirms
  "the maximum duration of a Realtime session is 60 minutes" verbatim. The 128k-token context-window
  figure the lane paired with it is separately correct but only as of the May-2026 `gpt-realtime-2`
  update (per [OpenAI's May-2026 voice-models post](https://openai.com/index/advancing-voice-intelligence-with-new-models-in-the-api/),
  confirmed via search: 128k tokens, "four times larger than its predecessor" 32,768); the original
  gpt-realtime (Aug 2025) context window was 32,768 tokens, not 128k. Both the session-cap and the
  context-window figures are now corrected/dated in place; this does not change any element/pattern
  verdict, only the numeric constraint values in C3/C6b's constraint discussion.
- **C7 — "no benchmark numbers" was an overstatement.** xAI's own launch announcement
  (`x.ai/news/grok-voice-agent-api`, already cited as a C7 source) self-reports "ranks #1 on Big
  Bench Audio" at 92.3% with sub-1-second time-to-first-audio (confirmed via WebSearch snippets of
  that exact URL, and independently corroborated by the Artificial Analysis post already used as a
  C11 source). The technical-docs page (`docs.x.ai/.../voice-agent`) genuinely lacks any benchmark
  numbers, architecture diagram, or paper — that part of the disclosure-quality verdict stands —
  but the blanket claim across both cited xAI sources was too strong. Corrected in place; the
  overall "low disclosure" verdict for xAI is unchanged (still weakest on architecture/paper
  relative to Amazon C8 and OpenAI C1), only the "zero benchmark numbers" specific claim was fixed.

**Confirmed accurate (no change needed), spot-checked directly:**
- C1: OpenAI's own materials do state the 65.6%→82.8% Big Bench Audio jump and the
  "extensively pretrained on specialized audio-centric datasets" framing (confirmed via WebSearch
  of `openai.com/index/introducing-gpt-realtime/` content, since direct WebFetch returned HTTP 403).
- C2: `developers.openai.com/api/docs/guides/realtime-mcp` confirmed verbatim that remote MCP tools
  are "executed by the Realtime API itself" — client does not run them. (The specific quoted phrase
  "point the session to a different MCP server..." was not found verbatim on this exact page in
  this pass; likely paraphrased from a companion page. Minor, does not affect the verdict.)
- C5/C6: `ai.google.dev/gemini-api/docs/live-guide` confirmed the 15-min audio-only / 2-min
  audio+video session caps and the 128k-token (native-audio) / 32k-token (other) context windows
  verbatim.
- C8: AWS's Nova Sonic post (2025-04-08) confirmed verbatim: "unifies speech understanding and
  generation into a single model," function calling + RAG for enterprise knowledge grounding. Nova
  2 Sonic's async-tool-calling quote and its 2025-12-02/12 date were confirmed via search.
- C9: Both Microsoft-cited pages (`microsoft.ai/news/mai-voice-2/`, 2026-06-02, and the
  hill-climbing-machine post) confirmed MAI-Transcribe-1.5 (43 languages) and MAI-Voice-2 (15
  languages) as named separately and confirmed the integration architecture is *not* documented in
  either piece. Neither source page's fetched text used the literal phrase "Azure Copilot" — that
  detail is corroborated instead by independent trade coverage (e.g. windowsnews.ai) reporting
  MAI-Voice-2 "integrates directly into Azure Copilot." Not treated as an error since the underlying
  claim holds via secondary sourcing, but the primary-source citations in C9 don't themselves say
  "Azure Copilot" verbatim — worth tightening sourcing at Stage 2 if this claim becomes load-bearing.
- C10: Full-text re-fetch of `arxiv.org/html/2603.13686v1` reproduced the lane's per-vendor pass@1
  numbers **exactly** — clean 51/49/31 and realistic 38/35/26 for xAI/OpenAI/Google respectively,
  the −18pp (xAI Retail, accents) vs −1pp (Google) accent-ablation contrast, and the 79%/90%
  agent-attributed-failure rates for the Voice-Fragile/Noise-Fragile cohorts. No changes needed;
  this is the most rigorously verified claim in the lane.
- C11: The exact cited X/Twitter status (`x.com/ArtificialAnlys/status/2001388724987527353`) exists
  and its text matches the lane's paraphrase precisely ("xAI's new Grok Voice Agent... surpassing
  Gemini 2.5 Flash Native Audio and GPT Realtime... 92.3%").
- InfoWorld MCP/SIP article (C2 source): confirmed 2025-08-29 date and content.

**Framework-verdict check (task c):** re-derived each element/usage-pattern/constraint call
independently; found no case where a usage-pattern-over-one-frozen-model was mislabeled as a
new-info element. C2/C4/C5(tools)/C7(tools)/C8(tools) = element calls are all genuine external
connectors (MCP, RAG, Search, code-exec, moderation classifier), not prompting tricks over the same
weights — correctly classified. C6 (Gemini context compression) and C8's Nova-2-Sonic async-dispatch
= usage-pattern calls are both correctly scoped (no new information source, only how/when existing
results surface). C9 and C12 are correctly left as first-class unclassified negatives rather than
forced into a verdict — this is the right call given the disclosure gaps found.

**Recency gap flagged (task d, not fixed in place — informational only):** this lane's C10 anchors
to the March-2026 τ-Voice snapshot (xAI Grok Voice Agent 51%/38%). A WebSearch during this pass
surfaced a newer xAI model, `grok-voice-think-fast-1.0` (announced ~2026-04-25 per MarkTechPost),
self-reporting 67.3% on a benchmark also branded "τ-voice Bench" — materially higher than the
paper's 51% figure for xAI's earlier model. It is **not confirmed** whether this is the same
independently-run methodology as the peer-reviewed arXiv paper or a vendor-adjacent re-branding of
the benchmark name for a self-reported number (which would itself be notable, since C11's negative
claim is precisely that no vendor self-reports pass@k agentic voice numbers). This is within the
lane's stated 2025-01–2026-07 recency window and predates this lane's 2026-07-06 writing date, so
it is a genuine coverage gap rather than an out-of-window item — flagged for Stage 2 to
investigate and resolve, not corrected in C10 itself since C10 is explicitly framed as reproducing
the existing archived anchor number rather than asserting the current state of the art.

**Access limitations this pass:** `docs.x.ai` could not be reached by direct WebFetch (network
policy blocked the domain) and several `openai.com`/`x.ai` pages returned HTTP 403 to direct
WebFetch; those claims were instead corroborated via WebSearch snippets quoting the same URLs.
Recommend a follow-up pass with direct browser access to re-confirm C7's `docs.x.ai` page content
verbatim if this lane is promoted to Stage 2.
