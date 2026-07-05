---
title: "What a Frozen Omni Agentic System Can and Cannot Gain: an elements-vs-usage survey of 2025+ multimodal/speech agents"
date: 2026-07-06
stage: 1-argumentation
status: "D2 — formal Stage-1 survey paper. Substantiates the elements-vs-usage framework (D0) with a 14-lane, ~120-system survey (2025-01→2026-07) hardened by three verification passes. To be reviewed by the D3 5-persona panel + citation-check before the owner problem-selection (K/T9)."
---

# What a Frozen Omni Agentic System Can and Cannot Gain

**An elements-vs-usage survey of 2025+ multimodal/speech agent systems, with a machine-checked bound and directional in-house evidence.**

## Abstract

We ask a problem-first question for training-free RL over a **frozen** omni speech model: once the base
model is capable enough to *do work*, from where can an *agentic* system add capability without changing
the model's weights or structure? We propose a taxonomy of four lever families — **elements** (new external
information: tools, knowledge, memory, a complementary model), **usage patterns** (roles / prompts /
multi-agent / routing over one frozen model), **inference-computation edits** (decoding-algorithm /
forward-pass restructuring), and **constraints** (perception fidelity, real-time/full-duplex, alignment) —
and defend a single thesis: **for a frozen model under a no-weight-and-no-structure-change contract, a
capability *boundary* can be crossed only by adding a new-information element; usage patterns are bounded by
the model's own oracle ceiling, and inference-computation edits are excluded by the contract.** We
substantiate this with a 14-lane survey of ~120 systems from January 2025 to July 2026 (speech/omni-centric,
VLM/GUI as transfer reference), hardened by three adversarial verification passes; a machine-checked bound
(`TfrlProofs.InfoBoundary`/`AgenticElements`, sorry-free); and directional in-house experiments on a frozen
Qwen3-Omni-30B. The survey finds **zero** usage-pattern-only crossings of a hard verifiable boundary that
survive scrutiny, and traces every genuine crossing to an element or a weight change. We correct two
tempting over-claims — training-free selection *does* raise deployed audio-QA scores (toward, never past,
the oracle), and a fourth lever family (decoding edits, e.g. EGLR) can expand a frozen oracle info-free but
falls outside our contract — and we localize the single open opportunity most aligned with the frozen
contract: **training-free reward-guided best-of-N reaching the verifiable pass^k ceiling on an interactive
voice-agent benchmark**, an empirically empty cell. We close with six candidate Stage-1 research problems.

## 1. Introduction

A frozen large model that already performs well on many tasks still fails in three recurring ways that an
**agentic system** is built to compensate: it lacks *capabilities* it never learned (addressed by **skills**
— standardized tool/API declarations behind a harness); it holds *inconsistent or missing knowledge*
(addressed by a **knowledge** backbone); and it forgets *task-specific context* (addressed by **memory**).
This paper asks which of these compensations can be realized **training-free** — with no change to the
model's weights *or* structure (the project's frozen contract; `wiki/Project-Thesis`) — and, more sharply,
*what class of intervention* can add capability at all under that contract.

This question is the successor to our Q1 conclusion (`2026-07-05-Q1-conclusion-corrected`): in-context
learning and prompt-space optimization are **insufficient** to realize a frozen omni model's headroom on the
semantic layer, because a large fraction of the headroom is a *capability/knowledge gap* the model cannot
produce from any prompt (up to ~43% on knowledge-QA; `2026-07-05-t5-headroom-composition`). That result
motivated a beyond-ICL system; this paper defines *what such a system is made of* and *where its leverage
can come from*, surveying how the field actually builds and evaluates 2025+ multimodal/speech agents.

**Contributions.** (1) A four-family lever taxonomy that separates *information* from *orchestration* from
*computation* from *substrate* (§2). (2) A machine-checked bound that usage patterns over a frozen model are
capped by its oracle ceiling (§2.4). (3) A 14-lane, ~120-system survey (2025-01→2026-07), verifier-passed
and adversarially hardened, testing whether any system violates the thesis (§3–§6). (4) The sensor-vs-brain
construction landscape (§7) and the evaluation-methodology map with its empty cells (§8). (5) Directional
in-house evidence on a frozen Qwen3-Omni-30B (§9). (6) Six candidate Stage-1 research problems (§10).

## 2. The elements-vs-usage framework

### 2.1 Four lever families
An agentic system is assembled from a small set of **elements** and wields them via **usage patterns**,
under **constraints**, optionally editing **inference computation**:

| Family | What it is | Members | Adds information to a frozen model? |
|---|---|---|---|
| **① Elements** | new external information | model(s); system/user prompt; connectors {skills/tools, knowledge, memory}; a complementary model | **Yes** — the only carriers of new information |
| **② Usage patterns** | orchestration over one frozen model | roles, prompts, multi-agent, routing (planning, verifier-as-role) | **No** — read-out; bounded by the model's oracle@N |
| **③ Inference-computation edits** | decoding / forward-pass restructuring | contrastive decoding, entropy-gated latent recursion (EGLR) | **No new info**, but changes the model's output *distribution* → can expand the oracle; **excluded by the no-structure-change contract** |
| **④ Constraints / qualities** | properties that bound the system | perception fidelity (model quality), real-time/full-duplex (base-architecture/substrate), alignment | **No** — bound or gate, not supply |

The owner's three deficits map to three **connector-type elements**: capability→skills/tools,
knowledge→knowledge connector, memory→memory connector. Perception, planning, verification, and real-time —
first proposed as additional "missing pieces" — are **not** new elements: planning and verifier-as-role are
usage patterns (②); perception fidelity and real-time/duplex are constraints (④). This reclassification is
the paper's organizing move.

### 2.2 The main thesis
> For a frozen model under a **no-weight-and-no-structure-change** contract, a capability **boundary** is
> crossed **only** by adding a new-information **element** (①). Usage patterns (②) read out the model's
> existing distribution and cannot exceed its oracle ceiling; inference-computation edits (③) can, but are
> excluded by the contract; constraints (④) bound the system without supplying capability.

### 2.3 The oracle-reading (stated precisely)
The thesis is about the **ceiling**, not about whether prompting ever helps. A usage pattern *can* raise the
**deployed (greedy)** score up toward the model's own **oracle@N** — self-consistency and chain-of-thought
do exactly this on audio-understanding QA (§8) — but it *cannot exceed* that oracle. Conflating "beats
greedy" with "crosses a boundary" would wrongly read the thesis as false; we therefore always measure a
candidate crossing against the **model's own best-achievable/oracle output**, never a naive baseline.

### 2.4 Machine-checked bound
`TfrlProofs.InfoBoundary` and `TfrlProofs.AgenticElements` (Lean 4, Mathlib v4.31.0, sorry-free) formalize
family ②:
- `readout_acc_le_oracle`: any selector returning one of the model's N samples has accuracy ≤ oracle@N.
- `readout_error_ge_gap`: the *no-correct-sample* set (the capability/knowledge gap) is an irreducible error
  floor for the whole selector class.
- `single_model_gap_unreachable`: a usage pattern emits an answer the model can produce under *some* context;
  on an item where no context yields a correct answer, it necessarily fails — the ∀-context quantifier is
  what role/prompt engineering cannot escape.
- `newinfo_can_cross_gap` / `external_element_can_escape`: an element can be correct where the gap holds.

These theorems bound ② over a **fixed** inference computation; family ③ changes the distribution and is out
of their scope *by construction* — which is exactly why the frozen contract's "no structure change" clause
is the boundary that makes the bound bite. (E10/E10b measured ② on a frozen omni: a same-weights
"verifier-role" never beats plain majority.)

## 3. Method

We ran a 14-lane survey (2025-01→2026-07), each lane a researcher agent that web-verified every claim
against a real URL, delta-tagged it against the prior archive (S1 `agent-level-synthesis`, S2
`agent-memory-skills-design`, L4 `stage1-L4-speech-agentic`), and classified it by family + verdict
(read-out vs new-info) + fence (single vs cross-session) + omni-role (sensor/brain/hybrid); followed by an
adversarial verifier per lane. Lanes: open/proprietary S2S, cascade frameworks, tools-skills-harness,
full-duplex, memory, knowledge-backbone, planning-control, verification-reward, perception-delta,
cross-domain VLM/GUI, and three evaluation lanes. Full claim ledger (~120 systems):
`wiki/survey/2026-07-06-synthesis.md` §1; per-lane files `2026-07-06-<lane>.md`.

**Three verification passes** hardened the central claims (synthesis §8): (a) *citation integrity* — all 21
load-bearing arXiv IDs resolve to real, on-topic papers (0 hallucinations); (b) *adversarial
counterexample-hunt* — a red-team that tried to break the thesis; (c) *positive-search* — a dedicated hunt
for a training-free selection win on a voice benchmark. We report their corrections inline (§4, §6, §8),
because they materially changed two claims.

## 4. Usage patterns are oracle-bounded (the central result)

Across 14 verifier-passed lanes, **no usage-pattern-only lever crosses a hard verifiable boundary above the
model's own oracle**. The adversarial pass confirmed this at HIGH confidence: every candidate fails at least
one of four gates (usage-pattern-only; one frozen model, no smuggled element; hard verifiable metric; above
the model's *own* ceiling). The strongest apparent candidate, a same-model self-check ASR-correction paper
(2505.24347), **dissolved on inspection**: it uses an external GPT-4o in a detect→correct→verify loop — a
second model (element), not same-model self-check. Direct positive confirmations:

- **Homogeneous multi-agent debate does not beat self-consistency** (2502.08788, 2605.00914): same-weights
  debate is capped by the strongest single agent; heterogeneous debate helps only because a *different*
  model is an element.
- **τ²-bench pass^k decay** 90%→57% (2506.07982): resampling the same model exposes inconsistency, adds no
  information.
- **Chain-of-thought *hurts* audio** on Step-Audio-R1 until weight-level RL fixed it (2511.15848); test-time
  scaling often inverse-scales on audio and needs GRPO to recover (2510.20867).
- **A harness change alone retains only 30–45% of text-mode capability** (τ-Voice / L4-P1): orchestration
  does not restore what the audio interface loses.
- **Memory-R1** (2508.19828): a *weight-updated* memory-manager role beats the *identically prompted* role
  by +28% F1 — the element (RL) crosses where the usage pattern (prompt) does not.

**Correction — usage patterns do raise deployed scores (toward the oracle).** The positive-search refuted a
too-strong reading: on audio-**understanding** QA (MMAU), training-free selection *wins* — Audio-CoT
(2501.07246: 55.6→58.1 via CoT + 5-vote self-consistency), Scaling Auditory Cognition via Test-Time Compute
(2503.23395: +9–150% via majority / beam-reranking / verifier on frozen ALMs), AQA-TTRL's 64-vote baseline
(2510.05478). These are **read-out** gains — measured vs greedy, bounded above by pass@N oracle — fully
consistent with §2.3. The thesis survives; the empty-cell claim narrows (§8).

## 5. The element families that *do* cross

Every genuine capability crossing traces to an element (or a weight change):
- **Verifier-as-tool** ≫ verifier-as-role. A *trained* reward model / judge is reliable and lifts
  capability: WavReward 53.4→91.5% (2505.09558), GenRM +16–40% over prompted judges (2408.15240), symbolic
  DB-state checks ≈100% (τ²-bench). *Prompted* zero-shot audio judges are not reliable (AudioJudge bias;
  SpeechJudge <70% human agreement) — the fork is real and adopted.
- **Retrieval / knowledge connectors.** CB-RAG (2509.19567): a frozen ASR + retrieval gives ≤17% WER
  reduction — a clean training-free element positive. Audio-native RAG (WavRAG 2502.14727, MoshiRAG,
  VoxRAG) supplies static external knowledge. "Knowledge fusion" across models, however, is a **terminology
  trap**: the field's realizations (FuseChat, KCR) are *weight merging / RLVR*, not training-free (2408.07990,
  2508.01273).
- **Memory connectors.** Mem0/Letta/Zep/A-MEM (2504.19413 et al.) are persistent stores (elements); their
  *reflection/routing* sub-steps are usage patterns. No system yet combines audio/speaker-keyed keys with
  cross-session *mutation* under a verifiable admission gate on *real* multi-session data (AFA is closest but
  keys route to text objects on synthetic data; 2604.25022) — a mechanism-level gap (§10, GAP-2).
- **Tool-use frameworks.** AudioToolAgent (2510.02995): a text-only coordinator arbitrating over audio-LM
  tools reaches SOTA (77.5 MMAU) — the coordinator never touches the audio; the capability is the tool
  elements. AURA (2506.23049) reports 90% task success but lacks a non-agentic ablation, so its ReAct-vs-tool
  attribution is unquantified.

## 6. The constraint and decoding families

- **Perception fidelity (④).** The bottleneck of native hybrids is the audio-facing interface and
  modality-fused reasoning, not orchestration (τ-Voice; Cascade-Equivalence-Hypothesis 2602.17598: "training
  objectives, not architectures, are the bottleneck"; E2E ≈ cascade by default, worse under noise). CP-Bench
  (2509.16589): the beyond-transcript channel is load-bearing for *contextual* paralinguistic reasoning
  (67–69% vs 51–56% cascade) but weak for *direct* recognition.
- **Real-time / full-duplex (④).** Full-duplex requires a purpose-built dual-stream base (Moshi 2410.00037,
  dGSLM, LSLM); prompting a frozen turn-based LLM into duplex fails (SyncLLM). Making a frozen omni
  full-duplex changes the base → outside our contract; we treat it as landscape, not a research lever.
- **Inference-computation edits (③) — the honest fourth family.** The adversarial pass surfaced a lever
  class the taxonomy first missed: **EGLR** (Entropy-Gated Latent Recursion, 2606.16620) is training-free,
  single-model, info-clean, yet *provably expands* a frozen model's verifiable oracle by +8.2pp beyond the
  temperature-only oracle (MATH-500) by recursively re-running top decoder layers; the audio analog is
  temporal contrastive decoding (2604.15383). This is neither element (no new info) nor usage pattern (not a
  prompt) — it changes inference **structure**, so it is **excluded by our no-structure-change contract**.
  We name it because "the element set is closed" holds only for prompt/orchestration usage patterns over a
  *fixed* inference computation; ③ is the most plausible site of an info-free ceiling expansion for anyone
  who relaxes the structure clause.

## 7. Systems construction: the sensor-vs-brain landscape

Every 2025+ omni system is one of two shapes:
1. **Fuse-and-retrain (hybrid).** Continue-pretrain/fine-tune one weight set so the same weights reason and
   emit audio (Moshi, GLM-4-Voice, Kimi-Audio, Qwen2.5-/Qwen3-Omni, MiniCPM-o, Step-Audio 2; all proprietary
   stacks). The whole model is the element; never training-free; lowest latency; paralinguistics preserved;
   but the text-brain ceiling is given up (catastrophic forgetting; a measurable capability tax).
2. **Freeze-and-bolt-on (sensor/brain split).** Keep the LLM frozen and attach separately-trained
   speech modules (Freeze-Omni), or chain ASR→LLM→TTS + tools (Unmute, all cascade frameworks,
   AudioToolAgent). The frozen LLM is the **brain**; speech modules are **sensor + actuator**; the text-brain
   ceiling is **inherited unchanged**; elements are swappable.

**Which wins?** Bifurcated. Prestige is dominated by hybrids, but on **verifiable agentic tasks the
sensor/brain-split cascade is competitive-to-superior**: VocalBench Cascade(GPT-4o) 82.7 > Qwen3-Omni 78.8;
URO-Bench Whisper+GPT-4o 89.3/79.3 ≫ best fine-tuned SDM 69.1/66.9; VoiceAgentBench/Audio2Tool cascade beats
one frozen SpeechLM on tool-calling. But it is model/benchmark-specific, not a law (VoiceBench has a unified
omni topping the board). The honest reading: **capability tracks element quality, not the wiring** — and the
freeze-and-bolt-on shape *is* the thesis's native architecture (a frozen brain + added elements), where the
provable oracle ceiling exists and the training-free opportunity lives. The **omni-sensor-vs-omni-brain**
choice is left open for the owner checkpoint (D4/T9), with this survey as its evidence base.

## 8. Evaluation methodology and the empty cells

The **verification fork is an adopted design choice**, not a hypothesis: τ²-bench/EVA-Bench/VoiceBench each
mix a deterministic verifier-as-tool (DB-state diff, SHA-256 hash, exact-match) with an LLM-judge
verifier-as-role *inside one instrument*; reliability tracks the fork exactly (symbolic ≈100%; trained
judges reliable; prompted judges not).

**The empty cell, corrected (§4).** Training-free best-of-N is **occupied** on audio-understanding QA
(MMAU). It is **empty on interactive voice-agent verifiable tasks**: EVA-Bench measures pass@1/pass@k/pass^k
(0.44 median peak-vs-reliable gap) but **as a reliability lens over one frozen system, never as a selector**
reaching the ceiling; EVA-Bench explicitly disclaims prompt optimization; τ²-voice submissions are Pass^1-
only by cost convention. The identical text-LLM toolkit (best-of-N, self-consistency, reward reranking) is a
thriving 2025–26 area with **zero confirmed crossover to any voice-agent benchmark**. Other first-class
empty cells: no cross-session benchmark; no human topline except MMAU-Pro (77.9%, 18.7pp gap); no
cascade-vs-native head-to-head on live verifiable tasks. **L4-N1/N2 must be re-graded**: occupied on
audio-understanding QA, empty on voice-agent verifiable tasks.

## 9. In-house directional evidence (frozen Qwen3-Omni-30B)

All boundary-clean (`Information-Boundary-Guard`), Stage-1 directional (small-n, single-model, single-touch —
illustrative, not settling):
- **Usage patterns don't cross (E10/E10b, T2, T3).** Two-system verifier never beats majority; proper
  task-definition few-shot never beats plain; iterative prompt-opt gives no gain — consistent with §4.
- **The gap is knowledge, not decoding (T5).** Own-sample decomposition: the *capability/knowledge gap*
  (no correct sample in 8) is up to 42.7% on knowledge-QA — the element-addressable target.
- **A unified compressed memory key is feasible (T6).** Retrieval precision@5 0.62 vs 0.08 chance; unified
  index task-purity 1.0, no pooling penalty.
- **The perception delta is real and task-dependent (p6).** omni(audio) vs omni(own ASR transcript),
  same frozen model, model-produced transcript: **SQuAD-zh +0.283 (significant)**, mmau +0.117 (n.s.,
  borderline), vocalbench 0. The omni's direct-audio path carries information its own transcript loses —
  validating omni-as-perception-element — but the strong-external-ASR control is the Stage-2 target.

## 10. Open problems (candidate Stage-1 research directions)

Six candidates, each tagged single/cross-session and mapped to a family; all `directional-only` at Stage-1;
the owner discussion (K/T9) selects. Fence: the 2026-07-03 closure was amended by the owner (Decision-Log
2026-07-06) to re-open cross-session work.

- **GAP-1 (flagship).** Training-free reward-guided best-of-N that *reaches the measured pass^k ceiling* on
  an **interactive voice-agent** benchmark (τ²-voice / EVA-Bench). *Single-session; ② selection gated by ①
  a decorrelated/symbolic reward.* The one axis both thesis-central and empirically empty (§8); directly
  W1's lever. A same-model self-reward is bounded (②); a symbolic DB-state check or trained/decorrelated
  reward is the allowed element.
- **GAP-2.** Audio/speaker-keyed **cross-session memory mutation** under a verifiable admission gate on real
  multi-session data. *Cross-session; ① store + ④ gate.* The most decision-relevant surface for W4.
- **GAP-3.** Omni-as-decorrelated-verifier for training-free best-of-N: can two context-differentiated views
  of the *same* frozen omni act as a genuine element, and what error-decorrelation δ_corr is the binding
  constraint? *Single-session; ① via decorrelation vs bounded ② self-reward.*
- **GAP-4.** Active audio "zoom"/re-sensing as a training-free **input-transformation element** (re-segment
  / source-separate / re-sample a span, then re-query) — the audio analog of RegionFocus; distinguishes a
  smuggled element from a hollow re-query.
- **GAP-5.** Paralinguistic-conditioned **agentic decision** with a verifiable-reward pass@k (e.g. escalate
  on detected frustration) — bridges the perception-delta (§9, p6) and eval lanes with a verifiable ground
  truth.
- **GAP-6.** Oracle-ceiling-controlled re-test of same-model self-check on a frozen omni (no second model):
  does structured self-verification exceed the frozen model's own best output, or merely recover it? Settles
  whether ② ever crosses at Stage-2.

## 11. Limitations

Stage-1 grade throughout (argumentation + literature; in-house numbers directional). Second-pass debts: some
notable systems appear only as beaten baselines (Kimi-Audio, MiniCPM-o, GLM-4-Voice, Doubao, Hume EVI,
Sesame CSM); some benches are un-entered (AIR-Bench, AudioBench, SpokenWOZ); the Chinese-ecosystem literature
is under-searched. The thesis's strict verdict is near-tautological under its own oracle-bar — its value is
the *precise scoping* (§2.3, §8) and the ③-family caveat (§6), not a surprising negative. The frozen-contract
excludes family ③, which is where an info-free ceiling expansion is most plausible; a future relaxation of
"no structure change" would reopen it.

## 12. Conclusion

A frozen omni agentic system gains capability only by adding **new-information elements**; orchestrating one
frozen model more cleverly reads out its existing ceiling but never crosses it (machine-checked; corroborated
across ~120 systems with zero surviving counterexamples). The field's own verifiable-agentic evidence favors
the **freeze-and-bolt-on** architecture that is the thesis's native shape, and leaves exactly one
thesis-central, contract-compatible cell empty: **training-free reward-guided selection reaching the pass^k
ceiling on a voice-agent benchmark.** That, with the audio-keyed memory and perception-delta surfaces, is the
Stage-1 problem space handed to the owner checkpoint.

## References

Verified arXiv IDs (all resolved, on-topic; citation-integrity pass): 2410.00037 Moshi · 2411.00774
Freeze-Omni · 2412.02612 GLM-4-Voice · 2503.20215 Qwen2.5-Omni · 2509.17765 Qwen3-Omni · 2504.18425
Kimi-Audio · 2505.02625 LLaMA-Omni2 · 2507.16632 Step-Audio 2 · 2511.15848 Step-Audio-R1 · 2506.07982
τ²-bench · 2603.13686 τ-Voice · 2605.13841 EVA-Bench · 2510.07978 VoiceAgentBench · 2505.09558 WavReward ·
2408.15240 GenRM · 2502.08788 / 2605.00914 multi-agent-debate · 2510.02995 AudioToolAgent · 2506.23049
AURA · 2509.19567 CB-RAG · 2502.14727 WavRAG · 2508.19828 Memory-R1 · 2504.19413 Mem0 · 2604.25022 AFA ·
2505.00684 RegionFocus · 2606.16620 EGLR · 2602.17598 Cascade-Equivalence · 2509.16589 CP-Bench · 2501.07246
Audio-CoT · 2503.23395 Scaling-Auditory-Cognition · 2510.05478 AQA-TTRL · 2603.14877 SoulX-Duplug · 2604.04847
Full-Duplex-Bench-v3 · 2601.18281 Reflecting-Twice · 2508.13992 MMAU-Pro. Full ledger with per-claim URLs and
tags: `wiki/survey/2026-07-06-synthesis.md`; per-lane files `wiki/survey/2026-07-06-<lane>.md`.
