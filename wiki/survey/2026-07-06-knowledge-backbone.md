---
title: Knowledge Backbone — Multi-Model Knowledge Fusion, Conflict Reconciliation & RAG-for-Speech
date: 2026-07-06
stage: 1-argumentation
lane: knowledge-backbone
---

# Lane: knowledge-backbone

**Driving question:** over a frozen omni model, is a *second model* a new-information ELEMENT (per the
project's closed-set framework: model(s) | prompt | connectors{tools, knowledge, memory}), or is
"multi-model" just another USAGE PATTERN that stays bounded by the single-model oracle ceiling? This
lane surveys 2025–2026 RAG-for-speech, multi-model knowledge fusion/routing, knowledge-graph backbones,
and conflict-reconciliation work to test that fork empirically and conceptually, per
`wiki/Project-Thesis.md`.

**Headline answer (argued below, claims 5–7, 9–10):** the literature draws a clean line. A second
model is a genuine new-info ELEMENT only when it is *actually* a different model — different
pretraining data/weights, hence different, only-partially-correlated parametric knowledge. When the
"second model" is the same weights relabeled into a different conversational role (debater, critic,
verifier), it is a USAGE PATTERN and stays bounded by the shared oracle ceiling — directly CONFIRMING
the archive's "same-weights critic never beats plain majority" axiom. Routing/ensembling machinery
itself (which model to ask) is a usage pattern; the thing it selects among (distinct models' distinct
knowledge) is the element. For SPEECH specifically, the clean training-free positive case (a frozen
ASR backbone + an external retrieval connector) exists and works (claim 2); but nearly every other
speech-RAG or agentic-speech knowledge system found in this search window still trains some component
(retriever contrastive loss, LoRA, RLVR, or full SFT) — meaning a genuinely training-free, multi-model
knowledge backbone for a frozen omni speech model is largely **unbuilt**, not merely unproven.

---

## Claims

### 1. WavRAG — audio-native retrieval, bypassing ASR
**Problem:** text-RAG pipelines for spoken dialogue transcribe with ASR first, discarding
paralinguistic/acoustic information, risking transcription-error propagation, and adding latency.
**Genealogy:** ports the text-RAG paradigm (Lewis et al. 2020 root, LLM domain) natively into audio;
origin domain **LLM**, transfer status **ported** (the RAG concept is directly carried over; the novel
part is a unified audio-text embedding space built on Qwen2-Audio).
**Training-free vs fine-tuned:** **mixed** — the "WavRetriever" component is trained (contrastive,
audio-text pairs) to build the shared embedding space; the base generative LLM is used as a frozen
backbone at answer time.
**Class + verdict:** **ELEMENT** — the audio-text knowledge base + retriever is a genuine external
knowledge connector (not a reprompting of the same model); reports ~10x speed vs an ASR-then-text-RAG
pipeline at comparable retrieval quality. Verdict: **new-info**.
**Fence:** single-session (per-query retrieval, no persistence demonstrated).
**Omni role:** hybrid (the omni encoder is both the retrieval "sensor" and part of the "brain" that
conditions generation on retrieved chunks).
[NEW] — https://arxiv.org/abs/2502.14727 (WavRAG, ACL 2025; also aclanthology.org/2025.acl-long.613.pdf)

### 2. CB-RAG — training-free contextual-biasing retrieval for ASR
**Problem:** ASR systems mistranscribe rare/OOV/domain-specific terms (names, jargon); need automatic
context discovery without touching the ASR model.
**Genealogy:** ports classic pre-LLM contextual biasing + the RAG retrieval paradigm (LLM domain) into
frozen ASR; origin **LLM** (retrieval mechanism)/**speech** (target task); transfer status **ported**.
**Training-free vs fine-tuned:** **training-free**, explicitly — the paper states it uses "black-box
models" and a "plug-and-play" method "without fine-tuning the ASR model." MiniLM-embedding retrieval
over a 466,358-word vocabulary feeds retrieved words into ASR context at inference only.
**Class + verdict:** **ELEMENT** — a pure external-knowledge connector bolted onto an otherwise
untouched frozen backbone. Verdict: **new-info**. This is the cleanest *positive* proof point in this
lane that a training-free ELEMENT crosses a real capability boundary: up to **17% relative WER
reduction** (24.1% at oracle context), at only 1.02–1.36× baseline latency (vs 4.66–6.16× for
LLM-prompting alternatives — corrected from an earlier "3–6×" approximation per direct paper text).
**Fence:** single-session (per-segment retrieval).
**Omni role:** n/a (ASR-only pipeline in the reported experiments, not a full omni reasoning loop).
[NEW] — https://arxiv.org/abs/2509.19567 ("Retrieval Augmented Generation based context discovery for ASR")

### 3. MARS / "Hearing More with Less" — retrieval-and-selection over one's own dialogue history
**Problem:** conversational LLM-ASR needs relevant *prior-turn* context; fixed windows miss relevant
turns, full history is computationally wasteful and redundant.
**Genealogy:** ports LLM-domain retrieval-and-selection refinements into multi-turn speech ASR, adding
a novel acoustic (FastDTW) retrieval channel; origin **LLM**, transfer status **ported+extended**.
**Training-free vs fine-tuned:** **fine-tuned** — requires jointly training a projector and LoRA
parameters with a 50%-random-masking curriculum; not training-free.
**Class + verdict:** the retrieved "knowledge" is the model's *own* prior conversation turns, not an
external source — so this is better classified as a **usage-pattern** (a smarter memory-access
pattern over the same session) than a new-info element, and tellingly it required weight changes
(LoRA) to pay off, undercutting a pure training-free story for even same-session self-context reuse.
Verdict: **read-out** (re-surfacing the model's own prior turns, not new information). Reports 8.35%
Mixed Error Rate vs 9.60% SOTA baseline, using 1.5K vs 179K training hours.
**Fence:** single-session (bounded to one multi-turn call).
**Omni role:** hybrid.
[NEW] — https://arxiv.org/abs/2508.01166 ("Hearing More with Less")

### 4. RASST — retrieval-augmented simultaneous speech translation
**Problem:** streaming speech-to-text translation mistranslates domain terminology (names, jargon)
under incomplete/partial speech input.
**Genealogy:** ports phrase-dictionary/terminology-biasing (classic MT technique) + retrieval into a
streaming Speech LLM; origin **LLM/MT**, transfer status **ported**.
**Training-free vs fine-tuned:** **fine-tuned** — the paper explicitly synthesizes training data "that
teaches the Speech LLM to decide whether and when to apply each retrieved term"; not training-free.
**Class + verdict:** the retrieved terminology-translation pairs ARE an external-knowledge **ELEMENT**
in principle, but current instantiations need fine-tuning to consume that element well. Verdict:
**new-info** (element exists) but **not training-free** — a recurring pattern in this lane (see also
claim 3): speech-LLMs today mostly can't yet *consume* a new retrieval element purely at inference
time; they need weight adaptation to use it. Reports ~40% relative gain in terminology accuracy and up
to +3 BLEU vs no-retrieval, with "negligible" compute overhead.
**Fence:** single-session (per-chunk retrieval).
**Omni role:** hybrid.
[NEW] — https://arxiv.org/abs/2601.22777 (RASST)

### 5. "Stop Overvaluing Multi-Agent Debate" — model heterogeneity is what matters, not the debate structure
**Problem:** multi-agent debate is widely claimed to boost LLM reasoning; is the reported gain real, or
an artifact of unfair evaluation and (implicit) model homogeneity?
**Genealogy:** LLM domain, direct critique of the multi-agent-debate lineage (Du et al. 2023, Liang et
al. 2023); origin **LLM**; transfer status **untransferred to speech** — no equivalent
heterogeneity-vs-homogeneity debate study was found for speech/omni agents in this search window.
**Training-free vs fine-tuned:** **training-free** — pure inference-time orchestration/prompting; no
weight changes to any participant.
**Class + verdict — the central test for this lane:** **homogeneous** debate (same weights, different
role prompts) is a pure **USAGE PATTERN** and the paper finds it does *not* reliably beat simple
single-model self-consistency once compute is matched — directly **CONFIRMING** the archive/framework
axiom that a same-weights "critic" prompt is bounded by that model's own oracle ceiling. **Heterogeneous**
debate (genuinely different models) is where gains concentrate — because a different model literally
is a different, only partially-correlated knowledge source, which is what an **ELEMENT** is defined to
be in this project's framework. Verdict: **read-out** for homogeneous debate; **new-info** for
heterogeneous debate (the "new info" is which *different* model is speaking, not the debate format).
**Fence:** single-session.
**Omni role:** n/a (text-reasoning domain; untransferred to speech — a concrete gap for W4 to test:
does the same homogeneous/heterogeneous split hold for an omni speech model's "critic" prompts?).
[NEW/CONFIRMS] — https://arxiv.org/abs/2502.08788 ("Stop Overvaluing Multi-Agent Debate — We Must
Rethink Evaluation and Embrace Model Heterogeneity")

### 6. "Don't Always Pick the Highest-Performing Model" — an information-theoretic proof of when a second model is a real element
**Problem:** when building an LLM ensemble, is it always best to add the single highest-accuracy
model, or can a weaker model contribute more?
**Genealogy:** LLM domain, formalizing classic ML ensemble theory (bias-variance / ambiguity
decomposition, Krogh & Vedelsby 1994 root) for LLMs; origin **LLM**; transfer status **untransferred**
to speech/omni.
**Training-free vs fine-tuned:** **training-free** (model selection/ensembling at inference; no weight
changes to constituents).
**Class + verdict:** formal proof that when model errors are *independent*, picking the top-k most
accurate models is optimal — but under realistic **correlated** errors, a lower-accuracy model from a
*different family* can contribute more decodable information than a same-family stronger model,
because its error pattern is structured and complementary (mutual-information argument, Theorem 4.3).
Concrete evidence: on MEDMCQA at ensemble size k=3, greedy mutual-information selection picked
Qwen3-235B (77.4% acc, ranked 5th by raw accuracy) precisely because its errors came from a
different model family with complementary failure patterns to the already-selected models —
achieving cross-family diversity *without* sacrificing accuracy. By contrast, a redundancy-only
baseline (mRMR) picked a far weaker model (GPT-4.1-nano, 66.8% acc, ranked 11th) chasing diversity
indiscriminately. (Corrected from an earlier draft that reversed which method picked which model —
Greedy MI is the strong-and-diverse pick; mRMR is the diversity-at-any-cost, accuracy-sacrificing
pick.) **ELEMENT**, verdict **new-info** — this is the theoretical backbone for "a second model is a
new-info element, conditioned on it being a genuinely different model."
**Fence:** single-session.
**Omni role:** n/a (text/MCQA; untransferred to speech).
[NEW] — https://arxiv.org/abs/2602.08003

### 7. InferenceDynamics — routing across LLMs by capability *and* knowledge profile
**Problem:** naive LLM routers optimize a single scalar performance score per model; real queries need
routing that accounts for which model *knows* the relevant domain, not just which is "strongest."
**Genealogy:** LLM domain, routing/mixture-of-models lineage (RouteLLM 2024 root); origin **LLM**;
transfer status **untransferred to speech** (no equivalent knowledge-aware omni-model router found,
e.g. "which omni checkpoint knows this accent/dialect/domain best").
**Training-free vs fine-tuned:** **mixed** — the candidate LLMs stay frozen (training-free); the router
itself is a small, separately-trained capability/knowledge profiler sitting on top.
**Class + verdict:** the routing mechanism is a **USAGE PATTERN** (deciding *which* model to query) —
it creates no new knowledge itself. What it operationalizes is that each candidate model's distinct
pretraining IS a distinct addressable **ELEMENT**; the router's whole value proposition is selecting
the right element per query rather than generating information. Verdict: **read-out** for the
routing layer itself; the elements it accesses are new-info by construction. Reports gains on
MMLU-Pro/GPQA/BigGenBench/LiveBench from identifying and leveraging top-performing models per query
(exact deltas not confirmed beyond the abstract).
**Fence:** single-session (per-query routing decision).
**Omni role:** n/a (text; untransferred to speech).
[NEW] — https://arxiv.org/abs/2505.16303

### 8. FusionFactory — three tiers of multi-LLM fusion, only some of them training-free
**Problem:** organizations accumulate large multi-LLM interaction logs (which model answered what, how
well); how to systematically turn that log data into better answers.
**Genealogy:** LLM domain; origin **LLM**; transfer status **untransferred to speech**.
**Training-free vs fine-tuned:** **spans all three** — (a) query-level fusion via trained routers
(training-free at inference, router itself trained), (b) thought-level fusion via *retrieved* abstract
reasoning templates (training-free, a genuine retrieval connector), (c) model-level fusion via
**distillation from top-ranked responses into one model** (explicitly changes weights — fine-tuning,
out of this project's training-free scope).
**Class + verdict:** (a) usage-pattern/read-out, (b) **ELEMENT** (retrieved reasoning templates =
external knowledge, new-info), (c) weight-change, **n/a** for training-free purposes. Reports
FusionFactory beats the best individual constituent LLM across all 14 LLMFusionBench tasks, but the
best-performing tier varies by benchmark — i.e., the *distillation* (fine-tuned) tier is often what
wins, not the training-free tiers.
**Fence:** **cross-session-accumulating** — explicitly designed to accumulate multi-LLM logs over
time, the rare case in this lane of an accumulating (not single-session) knowledge asset.
**Omni role:** n/a (text; untransferred to speech).
[NEW] — https://arxiv.org/abs/2507.10540

### 9. KARMA — nine-agent, frozen-LLM knowledge-graph enrichment with conflict resolution
**Problem:** knowledge-graph curation from unstructured scientific text doesn't scale manually; need
automated enrichment that also reconciles conflicting extracted facts.
**Genealogy:** LLM domain multi-agent orchestration applied to knowledge-graph construction (a
pre-LLM KG-curation lineage); origin **LLM**; transfer status **untransferred to speech** — no
audio/spoken-source KG-enrichment analogue was found.
**Training-free vs fine-tuned:** **training-free** for the orchestration — nine role-agents (entity
discovery, relation extraction, schema alignment, conflict resolution, etc.) built from a frozen
off-the-shelf LLM backbone; the actual new knowledge comes from ingesting external PubMed documents,
not from the model weights. **Correction (verified against the paper's Section 4.2):** the nine
agents are **not** a heterogeneous mix of GPT-4/ChatGLM/DeepSeek running together in one pipeline —
each experiment runs all nine agents on a *single, shared* LLM backbone, with GLM-4, GPT-4o, and
DeepSeek-v3 evaluated as three **separate** ablations, not combined. This actually sharpens rather
than weakens the usage-pattern call below: the nine-role structure is genuinely homogeneous
(same-weights, different role prompts) per run, exactly the "usage pattern over one frozen model"
case the framework predicts stays bounded on its own.
**Class + verdict:** the external document corpus is the **ELEMENT** (new information); the nine-role
pipeline structure (same frozen backbone in nine different role prompts) is the **USAGE PATTERN**
that extracts and reconciles it. Verdict: **new-info** (the corpus) mediated by a usage-pattern (the
multi-agent pipeline) — the framework's prediction (untested in the paper) is that ablating the input
documents while keeping the nine-agent structure would collapse the gains, which would further
confirm the thesis. Reported results: up to 38,230 new entities identified, 83.1% LLM-verified
correctness, 18.6% reduction in conflicting edges via multi-layer conflict assessment, NeurIPS 2025
spotlight.
**Fence:** **cross-session-accumulating** — the enriched KG persists and grows across runs, a genuine
shared knowledge backbone.
**Omni role:** n/a (text-only; untransferred to speech/omni — a notable gap given this lane's brief).
[NEW] — https://arxiv.org/abs/2502.06472

### 10. Youtu-GraphRAG — a persistent knowledge-graph backbone for frozen-LLM agents
**Problem:** standard vector RAG fails badly on schema-bound/multi-hop queries; complex reasoning needs
an explicit structured backbone, not a flat document store.
**Genealogy:** LLM domain GraphRAG lineage (Microsoft "GraphRAG Manifesto" 2024 root); origin **LLM**;
transfer status **untransferred to speech**.
**Training-free vs fine-tuned:** **training-free** — a "vertically unified agent system" of
hierarchically organized agents built on frozen, unmodified pretrained LLMs, reasoning over an explicit
graph schema.
**Class + verdict:** **ELEMENT** — the persistent knowledge graph itself is the new-info carrier; the
hierarchical agents are the usage-pattern that navigates it. Verdict: **new-info**. Independently,
2025 FalkorDB benchmarking (vendor-grade, not peer-reviewed) found vector RAG scoring 0% on
schema-bound queries (KPIs/forecasts) vs >90% for an optimized GraphRAG SDK (up from 56.2% in
Diffbot's original benchmark) — a large real capability crossing attributable to the graph element,
not to agent orchestration alone. Source (missing in the original draft, added on verification):
https://www.falkordb.com/blog/graphrag-accuracy-diffbot-falkordb/
**Fence:** **cross-session-accumulating** (a persistent graph is definitionally the "backbone").
**Omni role:** n/a (text; untransferred to speech/omni).
[NEW] — https://arxiv.org/abs/2508.19855

### 11–12. Knowledge-conflict taxonomy (genealogy root) and KCR (fine-tuned "solution") — the field's default answer to conflict-reconciliation is to retrain the backbone
**Problem:** when multiple knowledge sources disagree — context vs the model's own parametric memory
("context-memory conflict"), disagreement across multiple retrieved contexts ("inter-context
conflict"), or inconsistency within the model's own learned parameters ("intra-memory conflict") — how
should the system reconcile them? (Taxonomy from the 2024 survey, still the field's reference frame in
2025–2026.)
**Genealogy:** the survey is a **genealogy root** (2024, LLM domain, pre-dates this lane's 2025-01
window but is the load-bearing taxonomy every 2025–2026 conflict paper cites); KCR (2025) is a concrete
2025-era "solution" instance. Both origin **LLM**; transfer status **untransferred to speech** — no
equivalent taxonomy or method was found for spoken multi-source conflict (e.g., ASR hypothesis vs an
external KB vs dialogue memory disagreeing).
**Training-free vs fine-tuned:** the survey spans both categories of solution in principle; but the
concrete 2025 instance found (**KCR**) is **fine-tuned** — it explicitly uses "Reinforcement Learning
with Verifiable Rewards (RLVR)" to retrain the backbone's policy to prefer logically-consistent
reasoning over conflicting contexts, reporting a 7B RLVR-tuned model out-adjudicating GPT-4o/GPT-5.1 on
complex conflict-adjudication tasks.
**Class + verdict:** KCR is a **weight-change** approach — it illustrates that the current default
answer in the LLM literature to "how do we reconcile conflicting knowledge" is to fine-tune/RL-tune the
backbone, not to orchestrate frozen models/elements. Verdict: **n/a** for training-free purposes —
recorded as a **negative**: no training-free conflict-reconciliation method (of the kind this project's
thesis would need) surfaced in this search.
**Fence:** single-session (both).
**Omni role:** n/a (both).
[NEW] — https://arxiv.org/abs/2403.08319 (survey) and https://arxiv.org/abs/2508.01273 (KCR)

### 13. FuseChat / "Knowledge Fusion of Large Language Models" — the mainstream meaning of "knowledge fusion" is weight merging, not a training-free element
**Problem:** combine the complementary capabilities of several structurally-different chat models into
one deployable model.
**Genealogy:** LLM domain; origin **LLM**; transfer status **untransferred to speech** (no
speech/omni-specific weight-merging "FuseChat" analogue found).
**Training-free vs fine-tuned:** explicitly **fine-tuned**, confirmed by direct read of the paper — two
stages: (1) lightweight continual **fine-tuning** of each source model into a common intermediate
target structure via statistics-based token alignment, then (2) **parameter-space merging** of those
intermediates with fusion coefficients set by parameter-update magnitude. Both stages change weights.
**Class + verdict:** **weight-change**, entirely outside this project's training-free scope — but a
critical **terminology-boundary finding** for this lane: when the mainstream LLM literature says
"multi-model knowledge fusion," it overwhelmingly means merging/distilling weights into a single
checkpoint (FuseChat-7B approaches GPT-3.5-Turbo on MT-Bench this way), not a training-free
element/connector. A training-free reading of "knowledge fusion" (retrieval, routing, KG-backbone) is
the minority, more specialized sense this project must keep explicitly separate to avoid conflating the
two literatures. Verdict: **n/a**.
**Fence:** n/a. **Omni role:** n/a.
[NEW] — https://arxiv.org/abs/2408.07990 (FuseChat) and https://arxiv.org/abs/2401.10491 (Knowledge
Fusion of LLMs)

### 14. Production voice-agent RAG platforms (Vapi, Retell AI, Deepgram) — knowledge base as a bolt-on connector, in practice
**Problem:** deployed commercial voice agents need to answer from a business's own documents/FAQs
without hallucinating, and to do so within call-latency budgets.
**Genealogy:** directly ports commodity text-LLM RAG (vector DB + embeddings) into the voice-agent
product layer; origin **LLM**, transfer status **ported** (implementation, not research novelty).
**Training-free vs fine-tuned:** **training-free** as described — documents are uploaded to a vector
store queried at runtime by an off-the-shelf LLM inside a cascaded STT→LLM→TTS pipeline; no
fine-tuning described.
**Class + verdict:** **ELEMENT** (external document knowledge base) bolted onto an otherwise frozen
cascaded pipeline — corroborates, at the level of shipped products, that the industry treats the
"knowledge" axis as a bolt-on retrieval connector, not as a second reasoning model. Verdict: **new-info**,
but evidentiary weight is **low** — these are vendor blog posts/buyer's guides, not peer-reviewed or
benchmarked; no controlled pass@k numbers are reported. Marked directional-only, not admissible above
Stage-1 hypothesis grade.
**Fence:** single-session (per-call retrieval; a few vendors separately advertise, but do not
substantiate with numbers, an emerging "cross-call memory" feature).
**Omni role:** n/a (cascaded STT/LLM/TTS component pipelines, not native omni models).
[NEW, low-rigor] — https://vapi.ai/, https://www.retellai.com/blog/best-ai-voice-agent-services-businesses,
https://deepgram.com/learn/best-voice-ai-agents-2026-buyers-guide

### 15. "Building Enterprise Realtime Voice Agents from Scratch" — a 2026 training-free reference architecture that has *no* knowledge backbone at all
**Problem:** a from-scratch, pedagogical account of how a production-style voice-agent architecture is
actually wired together.
**Genealogy:** engineering tutorial, LLM/speech-systems domain; transfer status n/a (implementation
guide, not a novel method).
**Training-free vs fine-tuned:** **training-free**, explicit — "frozen pretrained models orchestrated
together": Deepgram (STT) + a vLLM-served LLM (text generation) + ElevenLabs (TTS), wired via a
"sentence buffer," with tool use via OpenAI-style function calling for grounding (e.g. database
queries, appointment scheduling). Quote: "Unlike the frameworks above which provide ready-made
components, our contribution is educational: a from-scratch implementation that explains how each
piece works internally." No fine-tuning anywhere.
**Class + verdict — first-class negative:** this reference architecture has **no knowledge-base/RAG
component at all**. Grounding is achieved purely via function-calling to live databases/APIs (a
TOOL/connector element), not via a retrieval-augmented knowledge store. Recorded as an **empty
measurement cell**: a rigor-focused, training-free voice-agent reference design, written in 2026,
still treats tool-calling as the default connector for grounding — RAG-for-speech has not yet made it
into even the field's own "how to build this from scratch" canon. Verdict: **n/a** (negative finding).
**Fence:** single-session. **Omni role:** n/a (cascaded, not omni).
[NEW, negative] — https://arxiv.org/abs/2603.05413

### 16. VoxMind — a 2026 agentic omni speech model that still needs SFT (and an auxiliary model) to "extend its knowledge boundary"
**Problem:** end-to-end omni-modal spoken dialogue models are conversational but lack agentic tool use,
which the authors frame explicitly as needed to "extend their knowledge boundaries and better solve
real-world tasks."
**Genealogy:** speech domain, built natively for E2E spoken dialogue models but the framing ("extend
knowledge boundary via tool use") is ported from the text-agent literature; origin **speech**
(construction) with a **ported** concept; transfer status **native+ported hybrid**.
**Training-free vs fine-tuned:** **fine-tuned** — trained via SFT on a curated 470-hour "AgentChat"
dataset, with a trained "Think-before-Speak" mechanism (ablation shows it is load-bearing for robust
performance), plus "a parallel dynamic tool update mechanism driven by an auxiliary language model" to
decouple inference latency from toolset size.
**Class + verdict:** the base omni model is retrained (weight-change), so this is **not** a clean
training-free test case; but the **auxiliary language model** driving tool-selection is itself a
genuine second **ELEMENT** in the architecture (a different model contributing complementary
capability), consistent with claims 5–7's finding that heterogeneous second models are where real
information comes from. Verdict: **n/a** for training-free purposes; recorded as a **negative** — the
most recent (2026) agentic omni-speech system found still reaches for full SFT to cross its knowledge
boundary rather than pure frozen-model orchestration, which is exactly the gap this project's
training-free approach must fill differently.
**Fence:** single-session (tool use is per-dialogue; the AgentChat corpus is consumed at train time,
not accumulated at inference).
**Omni role:** hybrid (the omni model is the dialogue "brain"; the auxiliary LM is a tool-routing
assist — a hybrid, two-model architecture, but built via fine-tuning, not training-free orchestration).
[NEW, negative] — https://arxiv.org/abs/2604.15710

---

## Cross-cutting synthesis

1. **Is a second model a new-info element? — Yes, conditioned on genuine heterogeneity.** Claims 5, 6,
   and 7 converge on the same answer from three independent angles (a critique-of-debate paper, an
   information-theoretic ensemble-selection proof, and a knowledge-aware router): a second model
   contributes new information exactly to the degree that its parametric knowledge is
   *uncorrelated/complementary* with the first model's — i.e., to the degree it is actually a
   *different* element in the closed set, not merely the same weights under a different role prompt.
   Same-weights "critic"/"debater" framing is a usage pattern and stays bounded by the shared oracle
   ceiling (claim 5's homogeneous-debate finding directly **CONFIRMS** the archive/framework axiom).
2. **Routing/selection machinery itself never generates knowledge — it only allocates access to
   elements.** InferenceDynamics (7) and the query-level tier of FusionFactory (8) are usage-patterns
   (read-out) whose entire value is in choosing which frozen model (element) to consult; they are not
   themselves a source of new information.
3. **For speech specifically, the one clean training-free positive is ASR + an external retrieval
   connector (CB-RAG, claim 2)** — frozen backbone, no fine-tuning, and a real WER reduction. Almost
   every *other* speech-RAG system found in this window (WavRAG's retriever, MARS, RASST) still trains
   some component to consume the retrieved element usefully, and the newest agentic omni-speech system
   (VoxMind) still leans on full SFT. **A genuinely training-free, multi-model knowledge backbone for a
   frozen omni speech model is largely unbuilt** in the literature surveyed — this is squarely in W4's
   opportunity space rather than a solved problem elsewhere.
4. **Terminology trap:** the mainstream LLM-literature sense of "knowledge fusion" (FuseChat, Knowledge
   Fusion of LLMs, claim 13) means merging/distilling weights — explicitly out of this project's
   training-free scope — while the KG-backbone/GraphRAG sense (claims 9, 10) and the retrieval-connector
   sense (claims 1, 2, 4, 14) are training-free. Both are called "knowledge fusion"/"knowledge backbone"
   in different papers; care is needed not to conflate them when writing the Stage-1 argument.
5. **No usage-pattern-only capability-boundary crossing was found.** Every attempted crossing in this
   lane either (a) added a genuine external knowledge connector/graph (claims 1, 2, 4, 9, 10, 14 — all
   ELEMENT), (b) added a genuinely different model (claims 5, 6, 7 heterogeneous case — ELEMENT), or
   (c) required retraining the backbone (claims 3, 4, 12, 13, 16 — weight-change, out of scope). The one
   pure usage-pattern case examined in depth (homogeneous multi-agent debate, claim 5) did *not* cross
   the ceiling — consistent with, and adding a second independent confirmation of, the archive's central
   axiom.

## Negatives / empty measurement cells

- No published training-free multi-omni-model knowledge-fusion system was found evaluated on any of
  this project's owned benchmarks (tau2-bench, eva-bench, soulx-duplug, audiomc,
  voiceassistant-eval, voicebench, uro-bench, vocalbench) — an empty cell, not merely a negative result.
- A 2026 "from-scratch" training-free voice-agent reference architecture (claim 15) omits a
  knowledge-base/RAG component entirely; tool-calling is the default grounding connector instead.
- The most recent omni agentic speech system found (VoxMind, claim 16, 2026) crosses its "knowledge
  boundary" via SFT + an auxiliary model, not training-free orchestration — no training-free omni
  analogue was found.
- Homogeneous (same-weights) multi-agent debate does not reliably beat single-model self-consistency
  (claim 5) — no verified case of a usage-pattern-only crossing of a capability ceiling was found
  anywhere in this lane's search.
- KCR and the one concrete 2025 conflict-resolution method found (claim 12) train/RL-tune the backbone;
  no training-free conflict-reconciliation method surfaced across searches.
- "Knowledge fusion" in mainstream LLM literature (claim 13) denotes weight merging/distillation, not a
  training-free element — a terminology trap for this project's writing.
- No speech-domain equivalent of InferenceDynamics- or FusionFactory-style multi-LLM knowledge-aware
  routing was found (claims 7, 8) — untransferred gap.
- No knowledge-graph-backbone (GraphRAG-style) system was found that ingests or reasons over
  AUDIO-sourced knowledge — all KG-backbone work found (claims 9, 10) is text-only.

## Note on evidence grade

All numeric claims above are Stage-1/hypothesis-grade per the project's methodology (argumentation from
literature, not this project's own large-sample validation). Claim 14 (vendor blogs) is explicitly
lower-rigor than the arXiv-sourced claims and should not be cited at the same evidentiary weight in any
Stage-2 write-up.

## Verifier notes (adversarial pass, 2026-07-06)

**URL spot-check (15 of the lane's ~19 distinct URLs fetched, exceeding the 5–8 sample size):**
all 15 resolved and matched their claimed titles/authors/abstracts: claim 1 WavRAG (2502.14727),
claim 2 CB-RAG (2509.19567, full text), claim 4 RASST (2601.22777), claim 5 Stop Overvaluing MAD
(2502.08788), claim 6 (2602.08003, full text), claim 7 InferenceDynamics (2505.16303), claim 8
FusionFactory (2507.10540), claim 9 KARMA (2502.06472, full text), claim 10 Youtu-GraphRAG
(2508.19855), claim 11 knowledge-conflict survey (2403.08319), claim 12 KCR (2508.01273), claim 13
FuseChat + Knowledge Fusion of LLMs (2408.07990, 2401.10491), claim 15 (2603.05413), claim 16 VoxMind
(2604.15710), plus claim 3 MARS (2508.01166). No dead links, no wrong-paper mismatches. The three
claim-14 vendor URLs (vapi.ai, retellai.com blog, deepgram.com buyer's guide) also resolved and
broadly support a knowledge-base/RAG bolt-on pattern, though the Vapi *homepage itself* doesn't
mention RAG (the retellai.com blog is what attributes "RAG knowledge base" to Vapi) — a minor
citation-precision gap, not a fabrication, and already appropriately tagged low-rigor/directional-only
in the lane.

**Fixed on this pass (edited in the lane file directly):**
1. **Claim 9 (KARMA) — factual error, corrected.** The paper's Section 4.2 runs all nine agents on
   ONE shared LLM backbone per experiment, testing GLM-4/GPT-4o/DeepSeek-v3 as three *separate*
   ablations — not a heterogeneous GPT-4+ChatGLM+DeepSeek pipeline as the original text implied. Fixed
   to state this precisely; the correction *strengthens* the lane's own usage-pattern verdict for the
   nine-role structure (genuinely same-weights, multi-role — the cleanest possible instance of "usage
   pattern over ONE frozen model").
2. **Claim 10 (Youtu-GraphRAG / FalkorDB) — missing citation, added.** The FalkorDB 0%-vs-90%+
   benchmark claim had no URL in the original draft. Verified via web search and direct fetch
   (https://www.falkordb.com/blog/graphrag-accuracy-diffbot-falkordb/) — numbers confirmed accurate
   (0% on schema-bound queries; >90% post-SDK vs 56.2% in Diffbot's original benchmark) — URL now
   added.
3. **Claim 6 ("Don't Always Pick...") — reversed comparison, corrected.** The original "concrete
   evidence" sentence implied Greedy MI chose the *lower*-accuracy, different-family model
   (Qwen3, 77.4%) over a higher-accuracy option (GPT-4.1-nano, 66.8%). Direct paper text (Section
   6.1/Table 1) shows the opposite pairing: Greedy MI picked the *higher*-accuracy, different-family
   model (Qwen3-235B, 77.4%, rank 5) precisely to get diversity without sacrificing accuracy; it was
   the mRMR *baseline* that picked the much weaker model (GPT-4.1-nano, 66.8%, rank 11) by chasing
   redundancy-reduction indiscriminately. Fixed. Net effect: the underlying ELEMENT/new-info verdict
   for claim 6 is still correct and still well-supported (Theorem 4.3 exists, confirmed by fetch), but
   the illustrative anecdote was backwards and is now accurate.
4. **Claim 2 (CB-RAG) — imprecise number, corrected.** "vs 3–6× for LLM-prompting alternatives" was
   loosely rounded; the paper's exact figure is 4.66–6.16×. Fixed.

**Framework-verdict spot-check (element vs usage-pattern, new-info vs read-out):** cross-checked the
lane's calls against the sibling `wiki/survey/2026-07-06-memory-components.md` lane, which applies the
identical element/usage-pattern axis to persistence/retrieval mechanisms and gives a directly
comparable ruling for WavRAG ("element (KB), not personal memory... hybrid... CONFIRMS") — matching
this lane's claim 1 verdict exactly, a good cross-lane consistency signal. Claim 3 (MARS)'s
"usage-pattern/read-out" call for within-session dialogue-history retrieval is likewise consistent
with the memory-components lane's own convention (a frozen model recombining information already
inside its own accessible context, within one continuous session, is usage-pattern; only
persistence *surviving past* what a single session/context could hold is scored as element). Claim 5's
homogeneous/heterogeneous debate split and claim 7/8's "routing machinery is usage-pattern, the
model pool it draws from is the element" split are both textbook-correct applications of "usage
pattern over ONE frozen model = read-out" and were not found to be misapplied anywhere in the lane.
No verdict call was found to be indefensible; the KARMA fix above is the only case where a verdict's
*factual premise* (not its logic) needed correcting.

**Recency (2025-01 to 2026-07) and negatives:** all 16 numbered claims cite 2025–2026 primary sources
(2502–2604 arXiv IDs, i.e. Feb 2025 through Apr 2026) except claims 11/13, which explicitly and
correctly flag their 2024 sources as pre-window genealogy roots (consistent with how the sibling
`2026-06-30-survey-agent-components-novelty.md` lane tags its own genealogy roots — not a deviation).
Negatives are well represented: a dedicated "Negatives / empty measurement cells" section lists 7
distinct empty/negative findings (no training-free multi-omni knowledge-fusion system evaluated on
project benchmarks; a 2026 from-scratch reference architecture with no RAG component at all; VoxMind
still needs SFT; homogeneous debate failing to beat single-model baselines; no training-free
conflict-reconciliation method; the "knowledge fusion" terminology trap; no speech-domain routing/KG
analogue). This satisfies the recency and negatives-inclusion checks.

**Not independently re-derived (would need full-PDF/appendix access, flagged but not blocking):**
claim 8's exact "beats the best individual constituent LLM across all 14 tasks" framing and claim 12's
"7B RLVR-tuned model out-adjudicating GPT-4o/GPT-5.1" — both confirmed at the abstract level (see
fetches above) but the underlying per-task/per-benchmark tables were not opened.
