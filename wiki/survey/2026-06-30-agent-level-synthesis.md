# Agent-level training-free RL — strategic direction memo (living, survey-first)

> project: exploring-l4-intelligence · owner: Charmer · started: 2026-06-30 · status: **running** · version: **v0.2**
> companion: [[2026-06-26-training-free-rl-for-speech-omni-research-proposal]] · survey archive [README](README.md) ·
>   [[Project-Thesis]] · [[Decision-Log]]
> S1 lanes: [speech-agents](2026-06-30-survey-agent-speech-agents.md) ·
>   [components-novelty](2026-06-30-survey-agent-components-novelty.md) ·
>   [does-it-compound](2026-06-30-survey-agent-does-it-compound.md)

> **A _living_ memo, built step-by-step (POMDP), to answer one strategic question — not a thesis change.**
> Survey-first: the Project-Thesis and the proposal's H1/H2/H3 are **not** touched here.

**Central strategic question.** Is the natural **"L4 / Innovator" evolution** space **agent-system-level**
*no-gradient* optimization (accumulating **skills** + **memory**) rather than single-model instruct/output search;
is it **under-explored for speech/omni** (the moat); does it **compound**; and **how far should we commit?**

## Process model (POMDP, strategic level)
Belief `b(s)` = the table below. Actions = survey-probe (lane + adversarial verification) · synthesize ·
**rollback/redirect**. Policy = **VOI-ordered & adaptive**. Terminal = a defensible **go/pivot/kill** + commit-degree
recommendation. Each step = one commit; rollback is first-class.

## Strategic Belief-State `b(s)` — live (updated @ S1)
Status: `prior` · `lit` (survey-verified) · `resolved` · `refuted`.

| # | Axis / claim | Belief (post-S1) | Conf | Status | Source |
|---|---|---|---|---|---|
| B1 | Agent-level **compounds** beyond single-model output search | **Yes — but only with structured/curated memory + value-based credit assignment; append-only plateaus/reverses** | high | **resolved (conditional)** | Voyager 2305.16291; ExpeL 2308.10144; AWM 2409.07429; JitRL 2601.18510; ACE 2510.04618; "Remembering More" 2605.17830 |
| B2 | **No-gradient discipline holds** at agent level | yes (must fence MIXED cases, e.g. MemSkill PPO controller) | med→high | lit | Self-Evolving-Agents survey 2507.21046; MUSE-Autoskill 2605.27366 |
| B3 | **Speech/omni-agent is the moat** | **Open, uncrowded** — recipe mature in text/embodied, speech evals single-episode, the intersection unfilled | high | **resolved (moat open; "first-ness" med)** | A4 lane; EVA-Bench 2605.13841; AudioMC 2512.14865 |
| B4 | Same `q*∝q0·exp(R/β)` **extends** to agent action space | **Yes — JitRL proves `z'=z+β·Â` = exact KL-constrained solution; credit assignment no-gradient by retrieval** | high | **resolved** | JitRL 2601.18510 |
| B5 | Model classes = **memory (embedding) / policy (generative)** | **Supported; off-the-shelf audio components exist; nobody composes both** | high | **resolved (positive)** | RAG 2005.11401; Omni-Embed-Nemotron 2510.03458; WavRAG 2502.14727 |
| B6 | **Verifiable rewards** for agent-level speech tasks exist | yes (WER/ASR/ST/SER/SID + the W1 reward/eval machinery) | med | lit | in-house `rl/` |
| B7 | **COMMIT the pivot? how far?** | **GO · add-new-layer · speech-grounded** — frame as *domain-transfer + two-omni pairing + verifiable speech rewards*, NOT a new mechanism | med | **resolved (lean; owner confirms)** | S1 synthesis |

## Deferred decision (owner confirms after the survey)
**S1 lean → GO, `add-new-layer` (an agent outer loop nesting W1/W4), `speech-grounded`.** *Rationale:* B1/B3/B4/B5 all
resolved favorably, but the **mechanism is not novel** (crowded general-agent frontier) → a new layer, not a thesis
reframe; keep scope speech-grounded because the moat, the assets (frozen omni models, verifiable speech rewards), and
the novelty are all speech-specific. Two design risks to engineer against (both verified): **append-only memory does
NOT compound** (context collapse / drift / temporal contamination) → curated/structured memory + explicit credit
assignment; and the moat is **absence-of-evidence** → claim "first, to our knowledge" and move fast (fast-follower risk).

---

## S1 — Findings (decisive probe: **GO**)
*3 lanes, per-lane adversarial verification, 41 verified claims / 51 sources (`wf_8452c9ae-a11`). Scope discipline:
"training-free" = frozen base WEIGHTS + evolving external STATE (memory/skill), verifiable rewards, no gradient on the
base; weight-updating methods (fine-tune/LoRA/RLHF/trained PRM/trained controller) are OUT of scope.*

### 1. The no-gradient self-improving-agent recipe is mature — but text/embodied, not speech
**Reflexion** (verbal self-critiques into an episodic buffer; "not by updating weights," arXiv:2303.11366), **Voyager**
(executable, embedding-indexed skill library over a blackbox frozen GPT-4, arXiv:2305.16291), **ExpeL** (cross-task
insight pool, no parameter updates, arXiv:2308.10144), the composition layer **ADAS** (2408.08435) / **DSPy**
(2310.03714) / **TextGrad** (2406.07496), and the 2026 training-free skill-bank **MUSE-Autoskill** (2605.27366). The
**Self-Evolving Agents survey** (2507.21046) is the citable taxonomy (in-context/memory/tool/architecture evolution =
in scope; parameter evolution = out). *Caveat: MemSkill (2602.02474) trains a PPO controller → MIXED, ruled out.* None
are speech-native.

### 2. Speech/omni agents are densely benchmarked — but only single-episode / within-session
Capability: **URO-Bench** (first S2S, 2502.17810), **VoiceBench** (2410.17196), **VoiceAssistant-Eval** (2509.22651),
**VocalBench** (2505.15727). Tool-use: **tau2-bench voice** (on tau-bench 2406.12045), **Full-Duplex-Bench-v3**
(2604.04847). Turn-taking: **Full-Duplex-Bench** (2503.04721). Multi-turn memory: **AudioMC** (within-conversation,
2512.14865), **MULTI-Bench** (2511.00850). End-to-end: **EVA-Bench**, whose "Experience" metric is *within-conversation*
fluency/timing, not cross-episode learning (2605.13841). Cross-**session** memory is benchmarked richly but **entirely in
text** (Mem-PAL 2511.13410; VehicleMemBench 2603.23840; LoCoMo/LongMemEval/PrefEval/PersonaMem).

### 3. Speech-agent progress is mostly weight-updating; the no-gradient slot is unfilled
Out of scope: **CORTIS** text-only fine-tuning (2606.21453), **SoulX-Duplug** trained state predictor (2603.14877). The
few no-gradient speech contributions are narrow single-shot retrieval/personalization: **WavRAG** (native-audio RAG over
Qwen2-Audio embeddings, 2502.14727), **Expressive Speech Retrieval** bi-encoder (2508.11187), and the off-the-shelf
vector-omni encoders **Omni-Embed-Nemotron** (2510.03458) / **Omni-Embed-Audio** (2604.18360) — components, not closed
Reflexion/Voyager loops.

### 4. Does no-gradient self-improvement compound? Yes — conditionally
Positive (verified): Voyager compounds compositionally (3.3× items, 15.3× faster milestones, zero gradient); ExpeL beats
Reflexion's third retry with one attempt; **Agent Workflow Memory** (+24.6%/+51.1% relative; gains widen 8.9→14.0 pts as
distribution drifts, 2409.07429); **LATS** rivals fine-tuning with gradient-free MCTS (2310.04406). Linchpin **JitRL**
(2601.18510): the additive-logit update is the exact closed-form KL-constrained solution (= q* over agent actions),
credit assignment by retrieval, beats every training-free baseline on WebArena and even weight-update WebRL (60.0 vs
46.06) at ~30× lower cost, with the per-episode gap **widening**. Bounds: Reflexion plateaus by trials 6–7; **ACE**
"context collapse" drops accuracy *below* the no-memory baseline (2510.04618); **SSGM** catalogs memory drift/poisoning
(2603.11768); "**Remembering More, Risking More**" shows memory-equipped frozen agents exceed the stateless violation
rate, rising with exposure (2605.17830). ⇒ compounding requires **structured/curated memory + explicit value-based
credit assignment**, not append-only logs.

### 5. The moat & the novelty delta
The MECHANISM is not novel (crowded text/code/embodied frontier). Unoccupied: a frozen **vector-omni bi-encoder as
MEMORY** + a frozen **generative thinker-talker omni as POLICY**, accumulating skills/memory across episodes under
**verifiable SPEECH rewards** (WER/ASR/ST/SER/SID) with **paralinguistic state** (speaker/emotion/turn-taking) as both
memory keys and reward signals. No surveyed audio work closes {frozen omni policy + frozen omni embedding memory +
episodic self-evolution + verifiable speech reward}. Frame as "**first, to our knowledge**, to instantiate the
no-gradient self-evolving-agent recipe in speech/omni," citing general-agent prior art to bound mechanism novelty.

*(Full per-claim registry with verified links: the three S1 lane files linked in the header.)*

## S2 — Conditional deepening (gated on S1) — **planned, owner-gated**
S1 = `deepen: true`. Priority (adaptive): **(1) agent-RL-formalization** — specialize JitRL's q*→agent-action proof +
retrieval credit assignment to the SPEECH action space (`z` = which speech memory · which skill · build context · decode
S2S) with verifiable speech rewards as `R` (the load-bearing formal contribution). **(2) agent-memory** — curated/
structured episodic memory keyed by paralinguistic state via a frozen vector-omni bi-encoder; the failure-mode literature
(context collapse / drift / temporal contamination) and what a *speech cross-session memory benchmark* would need (none
exists — a moat-enabler). **(3) agent-skills** (least new work) — what a speech "skill" is (a verified S2S/tool-use
behavior) + cross-episode transfer, reusing the resolved general-agent precedent. **Skip:** model-output level (prior
survey), general-domain mechanism novelty (resolved crowded), weight-updating speech/PRM methods (out of scope).

## S3 — Synthesis & deferred-decision recommendation  **[TBD — after S2]**

---

## Trajectory log (POMDP path; newest at bottom)
| Step | Date | Belief before → action → observation → update | Rollback? |
|---|---|---|---|
| S0 | 2026-06-30 | reflection → **scaffold the living memo; seed Belief-State** → (no obs) → high-VOI open axes = B1 (compound) + B3 (moat) gate the commit B7 | no |
| S1 | 2026-06-30 | `b₀` → **decisive probe: 3 lanes (speech-agents · components+novelty · does-it-compound) + adversarial verify, 41 claims / 51 sources** → **obs: B1 compounds *conditionally* (needs structured memory + credit assignment; append-only plateaus/reverses); B3 speech moat OPEN (no speech-native self-improving no-gradient agent; speech evals single-episode); B4 q* *extends* (JitRL closed-form proof); B5 components map cleanly + off-the-shelf audio parts exist, none composed; mechanism NOT novel** → **update: B1/B3/B4/B5/B7 resolved; pivot lean = GO · add-new-layer · speech-grounded (domain-transfer, not mechanism-novel). S2 deepen, priority RL-formalization > memory > skills.** | no (refines, no contradiction) |
