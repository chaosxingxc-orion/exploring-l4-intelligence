---
title: "What a Frozen Omni Agentic System Can and Cannot Gain: an elements-vs-usage survey of 2025+ multimodal/speech agents"
date: 2026-07-06
stage: 1-argumentation
status: "D2 (v2, post-D3-review). Formal Stage-1 survey substantiating the elements-vs-usage framework (D0). Revised per the 5-persona review (2026-07-06-review): thesis re-scoped contract-relative, decoding family confronted, 2505.24347 and p6 over-claims corrected, Lean reframed + a convergence theorem added. Feeds the owner problem-selection (K/T9)."
---

# What a Frozen Omni Agentic System Can and Cannot Gain

**An elements-vs-usage survey of 2025+ multimodal/speech agent systems, with a machine-checked structure and directional in-house evidence.**

## Abstract

Once a frozen model is capable enough to *do work*, from where can an *agentic* system add capability without
retraining it? We contribute a **classification**, not a discovered law. We sort training-free interventions
on a frozen model into four families — **elements** (new external information: tools, knowledge, memory, a
complementary model), **usage patterns** (roles / prompts / multi-agent / routing = *selection or
orchestration over a fixed generative law*), **inference-computation edits** (decoding-algorithm / forward-
pass changes = *a change to the generative law*), and **constraints** (perception fidelity, real-time/full-
duplex, alignment) — with an operational test for "element" (does it introduce conditioning bits not in the
model's inference-time input?). Two claims must be separated: **(A) elements are the only carriers of new
information** — this holds; and **(B) only elements can raise the achievable ceiling** — this is **false**: an
info-free decoding-law change can raise it, and the project's own canonical lists "decoding" as an in-scope
training-free lever. What *is* true, and near-definitional under its own bar, is that a **usage pattern
(selection over a fixed law) is bounded by the model's own oracle@N** — it can lift the deployed (greedy)
score toward that oracle, never past it. Our substantiation is therefore a **precise scoping** plus a 14-lane,
~120-system survey (2025-01→2026-07, speech/omni-centric) hardened by three literature-verification passes; a
machine-checked *definitional* structure for the usage-pattern bound, plus a *convergence* theorem for the
constrained selection process; and directional in-house probes on a frozen Qwen3-Omni-30B. Across ~120 systems
we find **zero confirmed** usage-pattern-only crossings of a hard verifiable boundary above the model's *own*
oracle; the strongest candidate (2505.24347) is **unresolved for lack of an oracle control**, not refuted —
and the negative is largely guaranteed by the bar and by element-oriented querying, so we report it as
absence-of-evidence, not a surprising discovery. The genuinely open, contract-compatible opportunities are:
training-free reward-guided selection reaching the verifiable **pass^k** ceiling on an interactive **voice-
agent** benchmark (currently unsearched/cost-gated); an omni-as-decorrelated-verifier; an oracle-controlled
test of same-model self-check; and an **in-scope decoding-law edit** as an info-free ceiling-raiser.

## 1. Introduction

A frozen model that performs well still fails in recurring ways an **agentic system** compensates: missing
*capabilities* (→ **skills**: standardized tool/API declarations behind a harness), *inconsistent/absent
knowledge* (→ a **knowledge** backbone), and *forgotten context* (→ **memory**). This paper asks which
compensations are realizable **training-free** — no change to weights *or* model structure (the project's
frozen contract, `Project-Thesis`, which nonetheless enumerates decoding and reward-guided decoding as
in-scope levers) — and, more sharply, *what class of intervention* can add capability under that contract.

This succeeds our Q1 conclusion (`2026-07-05-Q1-conclusion-corrected`): in-context learning and prompt-space
optimization are insufficient to realize a frozen omni model's headroom, because much of it is a
capability/knowledge gap the model cannot produce from prompts (`2026-07-05-t5-headroom-composition`). This
paper defines *what a beyond-ICL system is made of* and *where its leverage can come from*, surveying how the
field builds and evaluates 2025+ multimodal/speech agents.

**Contributions.** (1) A four-family classification of training-free interventions with an operational
element test (§2); the reclassification of perception/planning/verification/real-time as usage-patterns or
constraints is the organizing move. (2) A machine-checked *definitional* structure for the usage-pattern
bound and a *convergence* theorem for constrained selection (§2.4). (3) A 14-lane, ~120-system survey,
verifier-passed and adversarially hardened (§3–§6). (4) The sensor-vs-brain construction landscape (§7) and
the evaluation-methodology map with its empty cells (§8). (5) Directional in-house evidence (§9). (6) Seven
candidate Stage-1 research problems (§10).

## 2. The four-family classification

### 2.1 Families and the operational element test
| Family | What it is | Members | New information? | Can raise the ceiling? |
|---|---|---|---|---|
| **① Elements** | new external information | model(s); prompt; connectors {skills/tools, knowledge, memory}; a complementary model | **Yes** | Yes |
| **② Usage patterns** | selection/orchestration over a **fixed generative law** | roles, prompts, multi-agent, routing (planning, verifier-as-role) | No | **No** — bounded by oracle@N (definitional) |
| **③ Inference-computation edits** | a change to the **generative law** | contrastive/logit-surgery decoding; forward-pass restructuring (EGLR) | No | **Yes, info-free** — some are in-contract (§6) |
| **④ Constraints / qualities** | properties that bound the system | perception fidelity; real-time/full-duplex; alignment | No | No |

**Operational element test.** An intervention is an **element (①)** iff it *introduces conditioning bits not
present in the base model's inference-time input* (a tool result, a retrieved passage, a memory read, another
model's output, a higher-resolution re-sensed input). This test is applied uniformly and resolves the earlier
self-sealing case: RegionFocus's zoom **is** an element (new pixels enter the input); EGLR's layer-recursion
is **not** an element (no new bits) — it is a family-③ law-change. The owner's three deficits map to three
connector-type elements (capability→skills, knowledge→knowledge, memory→memory). Perception, planning,
verification, and real-time are **not** new elements: planning and verifier-as-role are usage patterns (②);
perception fidelity and real-time/duplex are constraints (④).

### 2.2 What is and is not claimed (contract-relative)
- **Claim A (holds).** Elements are the only carriers of *new information*.
- **Claim B (FALSE as an absolute).** "Only elements can raise the achievable ceiling" — an info-free
  **generative-law change (③)** can raise it, and the canonical lists decoding as in-scope.
- **The precise, defensible statement.** A **usage pattern — selection/orchestration over a *fixed* generative
  law — is bounded by the model's own oracle@N** (it can lift greedy toward that oracle, not past it).
  Crossing the ceiling requires **either** a new-info element (①) **or** a generative-law change (③); it
  cannot come from ② alone. This is *contract-relative*, not a discovered law: under our no-weight-and-no-
  structure contract the admissible ceiling-raisers are ① and the in-contract subset of ③.

### 2.3 The oracle-reading, and its compute-relativity
The bound is about the **ceiling**, not about whether prompting helps: a usage pattern *can* raise the
deployed (greedy) score toward the model's **oracle@N** — self-consistency/CoT do this on audio-understanding
QA (§8) — but not past it. The oracle is **compute-relative**: oracle@N *rises with N* (itself a usage move),
so an "empty cell" or a "gap" must always be stated at a fixed N (e.g. the T5 42.7% is *oracle@8 at N=8
prompt-space sampling, not a permanent floor*). We always adjudicate a candidate crossing against the model's
**own** best-achievable output at matched compute, never a naive baseline.

### 2.4 Machine-checked: a definitional structure and a convergence theorem
`TfrlProofs.InfoBoundary` / `AgenticElements` (Lean 4, Mathlib v4.31.0, sorry-free) formalize the
**definitional structure** of family ② over a *fixed* generative law — `readout_acc_le_oracle` (a selector
cannot beat the best of its N samples), `readout_error_ge_gap`, `single_model_gap_unreachable`. These are
**correctness-only static identities**; per the project's theory-track bar (a static identity is not a
theory-track result; correctness *and* convergence required), we present them as *formalizing the bound's
definitional structure*, **not** as an independent empirical corroboration of the survey's negative, and
**not** as a theory-track result. The missing dual-bar piece — a **convergence** result for the *constrained*
selection process — is supplied by `TfrlProofs.BestOfNConvergence` (`bestofn_regret_tendsto_zero`): a reward-
guided selector with a **bounded reward-estimation error** `τ_N → 0` (the constraint term) realizes the
oracle in the limit (regret `≤ B·τ_N → 0`). Family ③ changes the generative law and is out of the
definitional bound's scope by construction — correctly (§6).

## 3. Method

Fourteen survey lanes (2025-01→2026-07), each a researcher agent that URL-verified every claim, delta-tagged
it against the prior archive (S1/S2/L4), and classified it by family + verdict + fence + omni-role; each
lane then adversarially verified. Full ledger (~120 systems): `wiki/survey/2026-07-06-synthesis.md`; per-lane
files `2026-07-06-<lane>.md`. **Literature-verification passes:** (a) citation *existence + topic* verified
for 21 load-bearing IDs (all resolve, on-topic; this did **not** re-verify per-claim numbers/mechanisms — the
2505.24347 case below shows why that matters); (b) an adversarial counterexample-hunt; (c) a positive-search
for a training-free selection win on a voice benchmark. We flag one methodological limit up front: every lane
queried for *element* cases, so "no usage-pattern crossing found" is **absence-of-evidence under element-
oriented querying**, not confirmed absence; §10 adds a thesis-hostile probe as a remedy.

## 4. Usage patterns are oracle-bounded (the central, near-definitional result)

Across 14 lanes, **no usage-pattern-only lever is *confirmed* to cross a hard verifiable boundary above the
model's own oracle**. This is largely *guaranteed by the bar* (§2.2): a selector over N samples cannot beat
the best of them. Candidates are adjudicated mostly by **reclassification** (no third-party study reports the
oracle@N control), not empirical refutation. The strongest candidate does **not** dissolve:

- **2505.24347** (*"Fewer Hallucinations, More Verification: a three-stage LLM framework for ASR error
  correction"*) — a single frozen GPT-4o runs detect→correct→verify. Its gains (9–21% rel. CER/WER) are
  measured vs a **naive** baseline, with **no oracle@N control**. Status: **UNRESOLVED, parked as GAP-6** —
  *not* "dissolved into an element." (An earlier draft mislabeled it an external-GPT-4o element, contradicting
  our own ledger; corrected here.) So the honest verdict is **zero *confirmed* crossings; the strongest is
  unresolved for lack of an oracle control.**

Direct positive confirmations of the bound (element or weight change required to cross): homogeneous
multi-agent debate **empirically ≤ majority-voting** (2502.08788, 2605.00914 — empirical, not a martingale
proof); τ²-bench **pass^k decay** 90%→57% (resampling exposes inconsistency, no new info); **CoT hurts audio**
until weight-level RL (Step-Audio-R1 2511.15848; test-time scaling inverse-scales, 2510.20867); a **harness
change alone retains 31–51% clean / 26–38% noisy** of text capability (τ-Voice); **Memory-R1** — a
*weight-updated* role beats the *identically prompted* role +28% F1.

**Usage patterns do raise deployed scores (toward the oracle).** On audio-**understanding** QA, training-free
selection *wins*: Audio-CoT (2501.07246: 55.6→58.1 via CoT + self-consistency), AQA-TTRL's 64-vote baseline
(2510.05478), and Scaling-Auditory-Cognition (2503.23395; on a **self-collected** auditory-cognition set,
*not* MMAU; the "verifier" variant may be the model's own scoring vs a trained RM — verify before Stage-2
use). These are **read-out** gains (vs greedy, ≤ oracle@N) — consistent with §2.2. The bound survives; the
empty-cell claim narrows (§8).

## 5. The element families that cross

- **Verifier-as-tool ≫ verifier-as-role.** Trained reward models/judges lift capability (WavReward 53.4→91.5%
  2505.09558; GenRM +16–40% over prompted judges 2408.15240; symbolic DB-state checks ≈100%). Prompted
  zero-shot audio judges are unreliable (AudioJudge bias; SpeechJudge <70% human agreement).
- **Retrieval / knowledge.** CB-RAG (2509.19567: frozen ASR + retrieval, ≤17% WER↓) is a clean training-free
  element positive; audio-native RAG (WavRAG 2502.14727, MoshiRAG, VoxRAG) supplies external knowledge.
  "Knowledge fusion" across models is a terminology trap — the field's realizations are weight merging / RLVR
  (FuseChat 2408.07990, KCR), not training-free.
- **Memory.** Mem0/Letta/Zep/A-MEM (2504.19413 et al.) are persistent stores; their reflection/routing are
  usage patterns. No system yet combines audio/speaker-keyed keys, cross-session mutation, and a verifiable
  admission gate on real multi-session data (AFA closest; keys route to text on synthetic data; 2604.25022) —
  a mechanism-level gap (GAP-2).
- **Tools.** AudioToolAgent (2510.02995): a text-only coordinator over audio-LM tools reaches SOTA (77.5
  MMAU) — the capability is the tool elements. AURA (2506.23049) reports 90% task success but **lacks a
  non-agentic ablation**, so ReAct-vs-tool attribution is unquantified.

## 6. The constraint and decoding families

- **Perception fidelity (④).** The bottleneck of native hybrids is the audio-facing interface + modality-fused
  reasoning, not orchestration (τ-Voice; Cascade-Equivalence-Hypothesis 2602.17598: "training objectives, not
  architectures, are the bottleneck"; E2E ≈ cascade by default, worse under noise). CP-Bench (2509.16589): the
  beyond-transcript channel is load-bearing for *contextual* paralinguistic reasoning (67–69% vs 51–56%),
  weak for *direct* recognition.
- **Real-time / full-duplex (④).** Requires a purpose-built dual-stream base (Moshi 2410.00037, dGSLM, LSLM);
  prompting a frozen turn-based LLM into duplex fails (SyncLLM). Making a frozen omni full-duplex changes the
  base → outside our contract; landscape only.
- **Inference-computation edits (③) — confronted, not defined out.** The canonical lists **decoding** as
  in-scope, so ③ cannot simply be excluded. We adjudicate **per edit**: **contrastive / self-contrastive
  decoding** (logit surgery over the frozen forward pass — no weight or structure change) is **in-contract**
  and is a *live, info-free ceiling-raiser* — surfaced as **GAP-7**; **EGLR** (Entropy-Gated Latent Recursion,
  2606.16620 — recursively re-runs top decoder layers = forward-pass **restructuring**) is **plausibly out**
  of the no-structure clause. EGLR *demonstrates* (empirical oracle-pool result, needs a verifier to realize)
  a frozen model's oracle expanding +8.2pp beyond the temperature-only oracle (MATH-500, **text**). The audio
  analog (Temporal Contrastive Decoding, 2604.15383) is asserted, not yet substantiated in-body — the in-
  domain ③ evidence is **thinner** than the text case. Bottom line: **③ is where an info-free ceiling
  expansion is most plausible, and its in-contract subset (contrastive decoding) belongs on the owner's
  menu**, not defined away.

## 7. Systems construction: the sensor-vs-brain landscape

Every 2025+ omni system is either **fuse-and-retrain (hybrid)** — one weight set reasons and emits audio
(Moshi, GLM-4-Voice, Kimi-Audio, Qwen2.5-/Qwen3-Omni, MiniCPM-o, Step-Audio 2; all proprietary stacks): the
whole model is the element, never training-free, lowest latency, paralinguistics preserved, but the text-brain
ceiling is given up (catastrophic forgetting; a capability tax) — or **freeze-and-bolt-on (sensor/brain
split)** — a frozen LLM brain + separately-trained speech modules (Freeze-Omni) or chained ASR→LLM→TTS + tools
(Unmute, cascades, AudioToolAgent): the text-brain ceiling is inherited unchanged; elements are swappable.

**Which wins? (element-quality-confounded).** On verifiable agentic tasks the sensor/brain-split cascade is
often ahead, but the comparison is confounded by *element quality*, not the wiring: VocalBench Cascade(GPT-4o)
82.7 > Qwen3-Omni 78.8 is a *stronger brain vs a weaker omni* on a partly GPT-judge-scored bench. The cleanest
matched comparison — *From Text to Voice* with a shared strong ASR — finds "neither architecture uniformly
dominates," localizing the residual gap to **sensor-element fidelity**. The honest reading: **capability
tracks element quality, not the wiring** — and the freeze-and-bolt-on shape *is* the thesis's native
architecture (a frozen brain + added elements) where the oracle bound bites and the training-free opportunity
lives. The **omni-sensor-vs-omni-brain** choice is left open for the owner checkpoint (D4/T9).

## 8. Evaluation methodology and the empty cells

The **verification fork is an adopted design choice**: τ²-bench/EVA-Bench/VoiceBench each mix a deterministic
verifier-as-tool (DB-state diff, SHA-256 hash, exact-match) with an LLM-judge verifier-as-role in one
instrument; reliability tracks the fork (symbolic ≈100%; trained judges reliable; prompted judges not).

**The empty cell — absence-of-evidence, cost-gated.** Training-free best-of-N is **occupied** on
audio-understanding QA (Audio-CoT, AQA-TTRL). On interactive **voice-agent** verifiable tasks it is empty **as
a selector reaching the pass^k ceiling**: EVA-Bench reports pass@k only as a *reliability lens* and disclaims
prompt optimization; τ²-voice is Pass^1-only **by cost convention**. So the cell is empty partly for **cost**
reasons and partly because no one searched for the positive under a non-element query — we label it
**absence-of-evidence**, not confirmed absence. L4-N1/N2 are re-graded: occupied on audio-understanding QA,
unsearched-empty on voice-agent verifiable tasks. Other empty cells: no cross-session benchmark; no human
topline except MMAU-Pro (77.9%, 18.7pp gap); no matched cascade-vs-native head-to-head on live verifiable
tasks.

## 9. In-house directional evidence (frozen Qwen3-Omni-30B)

Boundary-clean (`Information-Boundary-Guard`), Stage-1 **directional** (small-n, single-model, single-touch —
per CLAUDE.md, small-n settles nothing; verbs below are "directionally consistent with," never "validates"):
- **Usage patterns don't cross (E10/E10b, T2, T3).** Two-system verifier never beats majority; proper
  task-def few-shot never beats plain; iterative prompt-opt gives no gain — directionally consistent with §4.
- **The gap at N=8 is not prompt-space-addressable (T5).** The *oracle@8 gap* (no correct sample in 8) is up
  to 42.7% on knowledge-QA **at N=8 prompt-space sampling** — *not* a permanent floor (a family-③ decoding
  change or larger N could shrink it, §2.3). It marks the element-addressable target *at fixed N=8*.
- **A unified compressed memory key is feasible (T6).** Retrieval precision@5 0.62 vs 0.08 chance; unified
  index task-purity 1.0.
- **The perception "delta" is confounded (p6) — an open question, not a validated element.** omni(audio) vs
  omni(its **own** ASR transcript): SQuAD-zh +0.283 CI[0.13,0.43], mmau +0.117 (n.s.), vocalbench 0. The
  baseline is the omni's **own lossy Chinese ASR**, and the pattern — largest on Chinese content-QA (where
  word-errors dominate), **zero on paralinguistic VocalBench (where a genuine >transcript signal would live)**
  — is at least as consistent with "own-ASR is lossy" as with a real perception delta, and arguably the
  *opposite* of what a perception element predicts. So this is **directionally consistent with, but not
  sufficient for**, an omni perception element; a **strong-external-ASR control is a precondition** (GAP-5),
  not a Stage-2 nicety.

## 10. Open problems (candidate Stage-1 research directions)

Seven candidates; all `directional-only` at Stage-1; the owner (K/T9) selects. Fence: the 2026-07-03 closure
was amended by the owner (Decision-Log 2026-07-06) to re-open cross-session work. The **decisive not-yet-run
test** of the thesis is GAP-6 (does a same-model self-check beat the model's *own* oracle@N?).

- **GAP-1.** Training-free reward-guided best-of-N *reaching the measured pass^k ceiling* on an interactive
  voice-agent benchmark (τ²-voice / EVA-Bench). *Single-session; ② selection gated by ① a decorrelated/
  symbolic reward.* **Expected outcome:** element-gated selection approaches pass@N *by construction* — so
  this is partly a **known-answer engineering demo of W1's lever**; the NEW knowledge is the *achievable*
  δ_corr and the deployed-vs-ceiling gap on voice-agent tasks, beyond the Lean bound + the MMAU precedent.
- **GAP-3 (co-flagship, genuinely open).** Omni-as-decorrelated-verifier: can two context-differentiated views
  of the *same* frozen omni act as a genuine element, and what error-decorrelation δ_corr is the binding
  constraint? Directly tests the self-preference-bias cell; the convergence theorem (§2.4) is its theory.
- **GAP-6 (decisive falsification test).** Oracle-ceiling-controlled re-test of same-model self-check on a
  frozen omni (no second model): does structured self-verification exceed the frozen model's *own* best
  output, or merely recover it? Settles whether ② ever crosses. The one experiment that could refute the
  thesis.
- **GAP-7 (in-scope decoding lever).** A training-free **contrastive/logit-surgery decoding** edit (family ③,
  in-contract) as an *info-free* ceiling-raiser on a speech task — the family the review showed the canonical
  admits and the thesis must confront rather than exclude.
- **GAP-2.** Audio/speaker-keyed **cross-session memory mutation** under a verifiable admission gate on real
  multi-session data. *Cross-session; ① store + ④ gate.* The most decision-relevant surface for W4.
- **GAP-4.** Active audio "zoom"/re-sensing as a training-free **input-transformation element** (introduces
  new conditioning bits by the §2.1 test) — the audio analog of RegionFocus.
- **GAP-5.** Paralinguistic-conditioned **agentic decision** with a verifiable-reward pass@k — but only after
  the strong-external-ASR control (§9) establishes the perception delta is real.

## 11. Limitations

Stage-1 grade throughout; in-house numbers directional (illustrative, not settling). The thesis's usage-
pattern bound is **near-definitional under its own oracle-bar** — its value is the precise *scoping* and the
~120-system classification, not a surprising negative; the negative is reported as absence-of-evidence under
element-oriented querying. Claim B (only elements raise the ceiling) is **false**; the in-contract decoding
family (③) is a live ceiling-raiser we surface rather than exclude. Coverage debts: some systems appear only
as beaten baselines (Kimi-Audio, MiniCPM-o, GLM-4-Voice, Doubao, Hume EVI, Sesame CSM); some benches are
un-entered (AIR-Bench, AudioBench, SpokenWOZ); the Chinese-ecosystem literature is under-searched. Citation
verification confirmed *existence + topic* for 21 IDs, not per-claim numbers/mechanisms — the 2505.24347 case
shows a resolved ID can still be mechanism-mischaracterized; verdict-flipping classifications deserve a
second-reader mechanism check before Stage-2.

## 12. Conclusion

A frozen omni agentic system gains *new information* only by adding an **element**; and a usage pattern that
merely selects/orchestrates over a fixed generative law **reads out** the model's existing oracle and cannot
exceed it (a machine-checked definitional structure; corroborated across ~120 systems with **zero confirmed**
counterexamples and the strongest one unresolved for lack of an oracle control). But raising the ceiling is
**not** the exclusive province of elements: an in-scope, info-free **decoding-law change** can do it too, and
the survey surfaces it (GAP-7) rather than defining it away. The field's verifiable-agentic evidence favors
the **freeze-and-bolt-on** architecture that is the thesis's native shape, and leaves genuinely open — for the
owner checkpoint — a small menu: element-gated selection reaching the voice-agent pass^k ceiling (GAP-1), an
omni decorrelated-verifier (GAP-3), the oracle-controlled self-check falsification (GAP-6), an in-scope
decoding edit (GAP-7), and the audio-keyed memory / perception surfaces (GAP-2/4/5).

## References

Existence + topic verified for 21 load-bearing IDs (citation pass): 2410.00037 Moshi · 2411.00774 Freeze-Omni
· 2412.02612 GLM-4-Voice · 2503.20215 Qwen2.5-Omni · 2509.17765 Qwen3-Omni · 2504.18425 Kimi-Audio · 2505.02625
LLaMA-Omni2 · 2507.16632 Step-Audio 2 · 2511.15848 Step-Audio-R1 · 2506.07982 τ²-bench · 2603.13686 τ-Voice ·
2605.13841 EVA-Bench · 2510.07978 VoiceAgentBench · 2505.09558 WavReward · 2408.15240 GenRM · 2502.08788 /
2605.00914 multi-agent-debate (empirical) · 2510.02995 AudioToolAgent · 2506.23049 AURA · 2509.19567 CB-RAG ·
2502.14727 WavRAG · 2508.19828 Memory-R1 · 2504.19413 Mem0 · 2604.25022 AFA · 2505.00684 RegionFocus ·
2606.16620 EGLR · 2604.15383 Temporal Contrastive Decoding · 2510.20867 test-time inverse-scaling · 2602.17598
Cascade-Equivalence · 2509.16589 CP-Bench · 2501.07246 Audio-CoT · 2503.23395 Scaling-Auditory-Cognition
(self-collected set, not MMAU) · 2510.05478 AQA-TTRL · 2603.14877 SoulX-Duplug · 2604.04847 Full-Duplex-Bench-v3
· 2508.13992 MMAU-Pro. Full ledger with per-claim URLs/tags: `wiki/survey/2026-07-06-synthesis.md`; review
record: `wiki/survey/2026-07-06-review.md`.
