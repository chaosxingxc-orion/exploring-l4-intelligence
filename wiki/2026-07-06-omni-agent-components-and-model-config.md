---
title: "Omni agentic system — component decomposition, per-component survey/gap, and the model-configuration (optimization-axis) decision"
date: 2026-07-06
stage: 1-argumentation
status: "Phase-A foundation doc (owner's 2026-07-06 redirect: anchor components + model config BEFORE building/optimizing). Discussion material for the model-axis decision; not locked."
---

> **LOG** — Stage-1 过程记录（hypothesis-grade），非现行真源；现行结论以 [[Decision-Log]] 与 [[Per-Work-Status]] 为准。

# Component decomposition + model configuration (foundation)

Owner redirect: I jumped too fast to optimization targets (the 7 GAPs). Those are *inside* components; the
foundation is (1) what components the system has + per-component design/eval/survey/gap, (2) which models
drive it + the optimization axis, (3) the training-free-RL optimization space, then (4) build + see
differentiated performance, then optimize. This doc is (1)–(3). **The one decision I need from you: the
model optimization axis (§2).**

## 1. Components (7 + the training-free-RL loop)
Reorganizes the D1 survey (`wiki/survey/2026-07-06-*.md`) by *component*. Lever type from D0 (which
components' optimization can actually cross the ceiling vs are read-out-bounded).

| # | Component | Design axis | How the field evaluates | Existing survey (D1) | Our training-free-frozen-omni gap | Lever |
|---|---|---|---|---|---|---|
| ① | **Perception** (audio→representation) | expose transcript vs >transcript delta | MMSU, CP-Bench, MMAU-Pro | yes (perception-delta lane) | train-free activation of >transcript for a *verifiable* decision | read-out (model quality) |
| ② | **Controller / planner** | omni vs text-LLM brain; ReAct vs workflow | task-completion, tool-call acc (τ²) | rich (ReAct/plan-execute) | none new — orchestration over one frozen model is oracle-bounded | read-out |
| ③ | **Memory** | key (audio-emb vs text); compression/retrieval/usage; single vs cross-session | AudioMC (multi-turn); cross-session (no bench) | rich (mem0/Letta/agent-memory) | audio/speaker-keyed **cross-session mutation** + verifiable admission | **new-info** |
| ④ | **Knowledge** | corpus, chunk-citation (deepsearch), audio-native RAG | QA acc, citation | rich (RAG/WavRAG) | audio-native knowledge for the **43% knowledge gap** (T5) | **new-info** |
| ⑤ | **Tools / skills** | SKILL.md/MCP; agent-tools/skillhub | tool-use success (τ²/eva) | rich (AURA, S2) | verifiable-reward **acceptance gate** for skills | **new-info** |
| ⑥ | **Verifier / reward** | verifier-as-tool (trained/symbolic) vs as-role (prompted) | judge reliability (SpeechJudge) | rich (WavReward/GenRM) | **omni decorrelated-verifier** (has convergence theory) | **new-info** |
| ⑦ | **Action / output** | streaming, TTS, style | naturalness (UTMOS) | rich | minimal (commodity) | — |
| + | **Training-free-RL loop** | best-of-N / reward-guided decoding / memory-strategy opt | optimization vs baseline (**vs oracle**) | our algorithm axis | spans ③–⑥ | — |

**Reading (my push-back on "no survey ⇒ innovation"):** all 7 components ARE surveyed in general/text/VLM.
The genuinely-empty cell is the *narrow* "training-free + frozen + omni/audio" intersection per component
(the gap column) — which D1 already located. So Phase-A is a **component re-organization + narrow-gap fill**,
not a from-scratch survey; and "no paper found" must be graded absence-of-evidence, not confirmed-vacant.
**Leverage lives in ③–⑥ (new-info); ①② are read-out-bounded** — this decides which components are worth
optimizing once built.

## 2. Model configuration — the optimization-axis decision (your point 2; the geba)

**Current config:** a single frozen **Qwen3-Omni-30B** (llama.cpp GGUF, `-ngl 28`, resident `llama-server`)
as the omni; W1 verifiable rewards (Python); a multilingual embedder for memory keys. **Hard fact from the
survey:** native omni hybrids retain only **31–51% of their backbone LLM's text capability** — so the omni
is a strong *ear/voice* but a *weak reasoner*. That fact forces the axis choice:

| Axis option | What we optimize | Pro | Con |
|---|---|---|---|
| **A. omni as end-to-end brain** | the omni's own rollouts (best-of-N/memory/prompt) for the whole task | purest "activate the frozen omni"; single model | optimizing toward a **weak-reasoner ceiling** (31–51%); and per D0 this is read-out-bounded (can't cross the omni's own knowledge gap) |
| **B. omni as sensor + text-LLM brain** | the text-LLM controller's orchestration/selection; omni feeds perception | strong reasoning axis | the axis is the **text LLM, not the omni** → "omni agentic" becomes "text-agent + omni-sensor"; and the omni's perception delta must be load-bearing (p6 **inconclusive**) or the omni is superfluous (M3 lesson) |
| **C. omni as the speech-task axis, augmented by new-info elements** (recommended) | the omni's rollouts **+ element calls** (verifier/knowledge/memory selection), under a verifiable reward | keeps the omni central (thesis-aligned) **and** gets the crossing-power from ③–⑥ elements (where D0 says the leverage is); doesn't bet on the omni's weak reasoning (A's flaw) nor demote it to a sensor (B's flaw) | more moving parts; the "axis" is the omni but the leverage is in the elements |

**My recommendation: C.** The omni stays the axis for the speech task (native audio, runs locally); we do
**not** rely on its weak reasoning alone (A) nor reduce it to a sensor whose value is unproven (B, p6
inconclusive). Instead the training-free-RL loop optimizes **selection over omni rollouts + element-augmented
candidates** (verifier ⑥, knowledge ④, memory ③). This is exactly where D0 locates the ceiling-crossing
leverage, and it keeps "omni agentic" honest. **Is Qwen3-Omni-30B reasonable?** Yes as the *speech-task*
axis; its weak reasoning is *why* the elements (not the omni's own orchestration) carry the crossing-power.
If a task needs heavy reasoning, add a text-LLM as a **tool/element**, not as a replacement axis.

*(This is the sensor-vs-brain fork D4 deferred to T9; your point 2 correctly pulls it forward because the
axis determines what we build and optimize. It is your call — I only recommend C.)*

## 3. Training-free-RL optimization space (your point 3), per component
Under axis C, the train-free-optimizable knobs (no weight change):
- **③ Memory:** compression / retrieval / usage strategies (the T6 design) — *new-info, can cross.*
- **④ Knowledge:** what to retrieve + how to inject — *new-info, can cross.*
- **⑤ Tools:** which tool/skill, when; acceptance gate — *new-info, can cross.*
- **⑥ Verifier/reward:** the selection reward (best-of-N); omni decorrelated-verifier (δ_corr) — *new-info,
  has convergence theory `BestOfNConvergence`.*
- **①② Perception/Controller:** prompt/representation/routing — *read-out, bounded by oracle@N* (optimize
  for efficiency, not ceiling).
So the RL loop's *ceiling-moving* knobs are ③–⑥; ①② are tuned but won't cross. This tells us **which
components to instrument first** when we build.

## 4. Build implication (your point 4) — once the axis is set
Minimal system on openJiuwen `agent-core-java` (omni-as-tool → llama-server; Java agent + Python eval):
axis-C means **omni (speech task) + one new-info element** (start with ⑥ verifier/best-of-N or ③ memory) +
WorkflowAgent orchestration. **Differentiated-performance discipline (my point C):** measure optimization
vs baseline **against the omni's own oracle@N, not greedy** — else a read-out gain masquerades as a system
win. Only after we *see* a real (vs-oracle) differentiated signal do we optimize a specific GAP.

## Open decision for you
**The model optimization axis (§2): A (omni-brain) / B (omni-sensor + text-LLM) / C (omni speech-axis +
elements, my rec).** Everything downstream (what to build, which components to instrument, which GAP) hangs
on it. Once you pick, I'll write the Phase-B minimal-build plan on openJiuwen around it.
