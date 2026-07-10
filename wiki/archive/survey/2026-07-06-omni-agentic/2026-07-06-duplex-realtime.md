---
title: "Lane survey — full-duplex / real-time / turn-taking / barge-in systems"
date: 2026-07-06
stage: 1-argumentation
lane: duplex-realtime
---

> **🗄 ARCHIVED (2026-07-11)** — 已收官战役过程件（2026-07-06 omni-agentic 调研），仅作历史，非现行真源。

# Duplex/real-time lane — landscape only

**Scope note (mandatory tag on every entry below):** every system in this lane **requires a
base-architecture change; it is out of a frozen-model research scope** as defined by this project's
thesis (no weight/no structure change over a single frozen omni model). This lane is landscape-only —
it is not a source of candidate training-free methods for W1/W4, only a boundary-map of what full-duplex
*costs* relative to that constraint.

## Up front: what full duplex needs from the base vs. the engine

Reading across 15 systems and 2 surveys, a load-bearing split emerges that maps directly onto this
project's element/usage-pattern/constraint framework:

- **Genuine simultaneous listen-while-speak generation** (the model updates its own output stream
  while continuously consuming the user's incoming audio, mid-generation, without a hard turn
  boundary) is produced only by changing the **base model's token/stream structure** — parallel
  codebook streams decoded jointly (Moshi's two-stream RQ-Transformer,
  [arXiv:2410.00037](https://arxiv.org/abs/2410.00037)), a dual-tower cross-attention architecture
  over two raw audio channels (dGSLM, [arXiv:2203.16502](https://arxiv.org/abs/2203.16502)), a
  synchronized-clock chunk generator retrained into the LLM's forward pass (SyncLLM,
  [arXiv:2409.15594](https://arxiv.org/abs/2409.15594)), or a continuous audio-embedding fusion
  layer injected into every transformer layer (LSLM middle-fusion,
  [arXiv:2408.02622](https://arxiv.org/abs/2408.02622)). None of these are addable to an already-frozen
  checkpoint by prompting or decoding tricks — they require retraining or a structurally different
  forward pass. This is the base layer.
- **Turn-taking *control*** (deciding when to yield, backchannel, or suppress speech — the "engine")
  is where a genuinely modular, bolt-on pattern appears: FlexDuo explicitly "decouples full-duplex
  control from the speech dialogue system, enabling the direct reuse of existing half-duplex
  dialogue systems" ([arXiv:2502.13472](https://arxiv.org/abs/2502.13472)), and SoulX-Duplug is a
  "plug-and-play streaming state prediction module" layered on top of a separate dialogue backbone
  ([arXiv:2603.14877](https://arxiv.org/abs/2603.14877)). These modules are trained *themselves* (a
  small semantic-VAD/turn-predictor), but the underlying dialogue LLM's weights are untouched — so
  the module reads as a genuinely new **element** (an external sensor/tool bolted onto a frozen
  brain), not a usage-pattern reframing of the same weights. The June-2026 survey's engineered- vs
  learned-synchronization split formalizes exactly this boundary ("Engineered Synchronization:
  modular architectures" vs "Learned Synchronization: end-to-end architectures",
  [arXiv:2509.14515](https://arxiv.org/abs/2509.14515)).
- **Net reading for the project's thesis:** full-duplex *generation* is a constraint
  (base-architecture/inference-substrate property, confirming the framework's a-priori
  classification) — it cannot be reached from a frozen model. Full-duplex *turn-management* is
  closer to an element (a new sensing/tool component) and could in principle sit in front of a
  frozen omni brain — but this only buys turn-taking hygiene (fewer false interruptions, better
  backchannel filtering), not the underlying simultaneous-generation capability itself. This lane
  therefore does not surface a frozen-model-compatible path to full duplex; it surfaces a
  frozen-model-compatible path to better **turn-taking policy** around a still-half-duplex core,
  which is a narrower, real but modest win.

---

## Claims

### 1. Moshi — first real-time full-duplex speech-text foundation model
- **Recognized problem:** cascaded ASR→LLM→TTS pipelines cannot be full-duplex (each stage
  serializes on the previous one finishing); Moshi targets sub-200ms two-way spoken dialogue
  with overlap/interruption. Source: [arXiv:2410.00037](https://arxiv.org/abs/2410.00037)
  (Défossez, Mazaré et al., Kyutai, Sept 2024; code
  [github.com/kyutai-labs/moshi](https://github.com/kyutai-labs/moshi)).
- **Genealogy:** speech-native architecture descended from neural-codec LMs (Mimi codec) +
  RQ-Transformer; origin-domain **speech**; **native** (not ported from text/vision).
- **Training-free vs fine-tuned:** fully trained/retrained end-to-end (7B Temporal Transformer +
  Depth Transformer over parallel semantic+acoustic streams, plus "Inner Monologue" text-token
  prefix) — **not weight-frozen**, not training-free.
- **Class + verdict:** **constraint** (base-architecture/inference-substrate). The full-duplex
  capability is produced by the two-parallel-stream architecture itself, not by a role/prompt
  usage pattern over an existing frozen LM — CONFIRMS the framework's a-priori tag.
- **Fence tag:** single-session (no cross-session memory/accumulation claimed).
- **Omni role:** hybrid (one architecture is simultaneously sensor — continuously consuming user
  audio — and brain — generating dialogue and its own inner-monologue text).
- **Delta:** NEW (archive does not cover duplex systems). (2024-09/10, outside the 2025-01..2026-07
  window; included per the same lineage rule as dGSLM/Mini-Omni2 below — Moshi is the field's
  founding full-duplex reference and is directly cited as ancestor by nearly every in-window entry.)

### 2. Freeze-Omni — frozen-LLM speech-to-speech with duplex state classifier
- **Recognized problem:** connecting speech I/O to an LLM while avoiding catastrophic forgetting
  of the LLM's text-domain intelligence, and adding duplex/interruption handling without full
  retraining. Source: [arXiv:2411.00774](https://arxiv.org/abs/2411.00774) (Wang, Li, Fu et al.,
  Nov 2024; site [freeze-omni.github.io](https://freeze-omni.github.io/)).
- **Genealogy:** speech-native adapter-based architecture; origin-domain **speech**, method
  (frozen-backbone + trainable adapters) is **ported** from the general frozen-backbone
  parameter-efficient-adaptation pattern common in LLM/VLM tuning.
- **Training-free vs fine-tuned:** the core **LLM's parameters are frozen**, but new adapters,
  input/output speech modules, and — critically — a **classification layer appended after the
  LLM's last layer to predict duplex/interrupt state** are all trained (~60k multi-round samples,
  8 GPUs). This is "frozen" in the narrower sense of *not fine-tuning the LLM checkpoint*, which is
  a different, weaker claim than this project's "no weight and no structure change to the whole
  system" — new structure (the classifier head, adapters) is added and trained. **Not
  training-free** under this project's definition.
- **Class + verdict:** **constraint at the system level** — even though the LLM backbone is
  frozen, duplex behavior requires adding and training new structure (classifier head + adapters),
  so the overall system is not reachable from a frozen checkpoint by prompting/decoding alone.
  Useful negative-space data point: "frozen LLM" branding in this literature usually means
  frozen-backbone-plus-trained-adapters, not the stricter frozen-whole-system sense this project
  uses — a terminology gap worth flagging.
- **Fence tag:** single-session.
- **Omni role:** hybrid (adapters = sensor/actuator; frozen LLM = brain; classifier head = a
  duplex-specific control signal bridging the two).
- **Delta:** NEW; also a useful terminology-precision note for future lane cross-referencing.
  (2024-11, outside the 2025-01..2026-07 window; included per the lineage rule — directly-cited
  immediate predecessor to the in-window frozen-backbone-adapter line.)

### 3. LSLM — Listening-while-Speaking Language Model
- **Recognized problem:** turn-based speech LMs cannot be interrupted mid-generation; LSLM targets
  real-time interruption via simultaneous listening and speaking channels. Source:
  [arXiv:2408.02622](https://arxiv.org/abs/2408.02622) (Ma et al., Aug 2024, Shanghai Jiao Tong
  Univ./ByteDance).
- **Genealogy:** speech-native dual-channel architecture (token-based decoder-only TTS + streaming
  SSL encoder); origin-domain **speech**, **native**.
- **Training-free vs fine-tuned:** fully trained architecture; three fusion strategies compared
  (early/middle/late), middle-fusion (injecting listening embeddings into every transformer layer)
  wins — this is a structural change to every layer, **not training-free**.
- **Class + verdict:** **constraint**. Interruption sensitivity (precision/recall/F1 ≥97% under
  noise reported) comes from architecture-level fusion depth, not from a prompting/role strategy —
  CONFIRMS the framework.
- **Fence tag:** single-session.
- **Omni role:** hybrid.
- **Delta:** NEW. (2024-08, outside the 2025-01..2026-07 window; included per the lineage rule —
  directly-cited immediate predecessor to the in-window fusion-depth line.)

### 4. dGSLM — dual-tower cross-attention, emergent turn-taking (genealogy root, pre-window)
- **Recognized problem (2022, tagged as genealogy root per recency rule):** generate naturalistic
  two-channel spoken dialogue (including laughter, backchannel, overlapping speech) without any
  text supervision. Source: [arXiv:2203.16502](https://arxiv.org/abs/2203.16502) (Nguyen et al.,
  Meta AI, March 2022; site [speechbot.github.io/dgslm](https://speechbot.github.io/dgslm/)).
- **Genealogy:** the foundational textless dual-tower architecture that essentially every
  2024-2026 full-duplex paper cites as ancestor; origin-domain **speech**, **native**.
- **Training-free vs fine-tuned:** trained from scratch on 2000h of raw two-channel Fisher
  conversational audio; **not training-free**.
- **Class + verdict:** **constraint** — turn-taking emerges from the dual-tower
  cross-attention architecture processing both channels jointly, an architectural property, not a
  prompted role.
- **Fence tag:** single-session.
- **Omni role:** hybrid (textless — codec-unit sensor and generator fused).
- **Delta:** NEW (genealogy root, outside 2025-01..2026-07 window, included per rule for lineage).

### 5. SyncLLM ("Beyond Turn-Based Interfaces") — clock-synchronized full-duplex over a text LLM
- **Recognized problem:** pretrained LLMs (e.g., Llama3-8B) have no sense of real-world time, so
  they cannot natively run synchronously with a live audio stream; solving this is required before
  an LLM backbone can support full-duplex turn-taking/overlap/backchannel. Source:
  [arXiv:2409.15594](https://arxiv.org/abs/2409.15594) (Sept 2024).
- **Genealogy:** origin-domain **LLM** (starts from a pretrained text Llama3-8B) **ported** into
  speech via a synthetic-data + chunked-generation training recipe (212k h synthetic + 2k h real
  dialogue); this is the strongest example in the lane of a text-LLM being pulled into full-duplex.
- **Training-free vs fine-tuned:** requires a **new training recipe and mechanism to inject time
  information into the model's forward pass** so it predicts an estimated user chunk before its own
  next chunk — this is retraining, not decoding-time or prompt-only. **Not training-free.**
- **Class + verdict:** **constraint**. Even starting from a strong pretrained text LLM, crossing
  into full-duplex synchronization required modifying the generation mechanism and retraining, not
  a role/prompt applied at inference — CONFIRMS the framework's constraint classification and
  additionally shows that "just add a system prompt to a frozen text LLM" does not get you duplex.
- **Fence tag:** single-session.
- **Omni role:** brain-only bootstrap (starts text-only) evolving into hybrid post-training.
- **Delta:** NEW; directly useful negative evidence against a "prompt a frozen text LLM into duplex"
  hope. (2024-09, outside the 2025-01..2026-07 window; included per the lineage rule — directly
  cited as ancestor by later text-LLM-into-duplex work in this lane.)

### 6. VITA-1.5 — GPT-4o-level real-time vision+speech interaction
- **Recognized problem:** open replication of GPT-4o-style real-time multimodal (vision+speech)
  interaction without relying on external ASR/TTS (which add latency and break flow). Source:
  [arXiv:2501.01957](https://arxiv.org/abs/2501.01957) (Jan 2025; code
  [github.com/VITA-MLLM/VITA](https://github.com/VITA-MLLM/VITA); NeurIPS 2025).
- **Genealogy:** origin-domain **VLM→speech** (vision-language MLLM extended to audio in/out);
  **ported** (vision-language training methodology extended progressively to speech).
- **Training-free vs fine-tuned:** three-stage progressive training (vision-language → audio input →
  end-to-end speech generation) that **replaces external ASR/TTS with trained internal speech
  modules**; **not training-free**.
- **Class + verdict:** **constraint** — end-to-end low-latency speech generation requires new
  trained output-side modules integrated with the LLM, not a decoding-time trick.
- **Fence tag:** single-session.
- **Omni role:** hybrid (vision+audio sensor fused with LLM brain and a trained speech-generation
  actuator).
- **Delta:** NEW.

### 7. VITA-Audio — MCTP module for near-zero first-token latency
- **Recognized problem:** even end-to-end speech LLMs have high first-audio-token latency because
  audio tokens are generated one at a time after a full LLM forward pass; needed for duplex-grade
  responsiveness. Source: [arXiv:2505.03739](https://arxiv.org/abs/2505.03739) (Long et al., May
  2025).
- **Genealogy:** origin-domain **speech**, method (lightweight auxiliary prediction heads for
  multi-token generation) is **ported** from the LLM speculative-decoding/multi-token-prediction
  literature.
- **Training-free vs fine-tuned:** adds a new **Multiple Cross-modal Token Prediction (MCTP)**
  module trained alongside a 4-stage progressive training strategy; reduces first-chunk latency
  236ms→53ms and gives 3-5x speedup at 7B scale — **not training-free**, new structure added.
- **Class + verdict:** **constraint** (an inference-substrate/latency property achieved by adding
  new predictive heads to the architecture, not a decoding-time prompt strategy over a frozen
  model).
- **Fence tag:** single-session.
- **Omni role:** hybrid.
- **Delta:** NEW. Useful as a "usage-pattern-only crossing" negative: multi-token-prediction-style
  latency wins are themselves ported *from* an LLM technique but still require adding/training new
  parameters — confirms that even LLM-genealogy tricks don't get you duplex for free at decode time.

### 8. Mini-Omni2 — open GPT-4o-style omni model with interruption mechanism
- **Recognized problem:** open-source replication of GPT-4o omni (vision+audio+text) interaction
  with duplex interruption capability, without external ASR/TTS. Source:
  [arXiv:2410.11190](https://arxiv.org/abs/2410.11190) (Oct 2024; code
  [github.com/gpt-omni/mini-omni2](https://github.com/gpt-omni/mini-omni2)).
- **Genealogy:** origin-domain **speech** (extension of Mini-Omni); **native**.
- **Training-free vs fine-tuned:** trained specifically for interruption based on input semantic
  information (the authors argue semantic — not just VAD-energy — interruption is needed for
  stable interaction); **not training-free**.
- **Class + verdict:** **constraint** — interruption handling is trained into the model's output
  generation loop.
- **Fence tag:** single-session.
- **Omni role:** hybrid.
- **Delta:** NEW. (2024-10, just outside the 2025-01 window; included as a directly-cited immediate
  predecessor to the in-window VITA/Mini-Omni line — tagged accordingly.)

### 9. OmniFlatten — flattening operation, three-stage post-training onto a text LLM
- **Recognized problem:** converting an existing text LLM backbone into a full-duplex speech-text
  dialogue model via a unified token-stream representation rather than a bespoke duplex
  architecture. Source: [arXiv:2410.17799](https://arxiv.org/abs/2410.17799) (Oct 2024).
- **Genealogy:** origin-domain **LLM** backbone, **ported** into speech duplex via a "flattening"
  data representation plus staged post-training (modality alignment → half-duplex → full-duplex).
- **Training-free vs fine-tuned:** notably, **no architectural change to the backbone LLM** is
  needed — but it still requires a **three-stage post-training (fine-tuning) regime** that changes
  the backbone's weights. This is the clearest example in the lane of "same architecture, different
  weights" — a useful boundary case for the project's "no weight AND no structure change"
  bar: OmniFlatten satisfies "no new structure" but fails "no weight change," so it still does not
  count as training-free by this project's stricter definition.
- **Class + verdict:** **constraint** (weight-level). Confirms that even without inventing new
  architecture, full-duplex still is not obtainable from a frozen checkpoint — it requires
  moving the weights via staged fine-tuning.
- **Fence tag:** single-session.
- **Omni role:** hybrid.
- **Delta:** NEW; important nuance for the framework: distinguishes "no new structure" from "no
  weight change" — full duplex fails the weight-change bar even when it passes the
  no-new-structure bar. (2024-10, outside the 2025-01..2026-07 window; included per the lineage
  rule — this weight-only boundary case is referenced by the lane's own synthesis above.)

### 10. FlexDuo — pluggable, decoupled full-duplex control module (boundary case)
- **Recognized problem:** every full-duplex model bakes turn-taking control into the dialogue
  backbone, so upgrading control logic requires retraining/rebuilding the whole system; FlexDuo
  asks whether duplex *control* can be decoupled from the dialogue *model*. Source:
  [arXiv:2502.13472](https://arxiv.org/abs/2502.13472) (Feb 2025, v2 May 2025).
  Also see: [emergentmind summary](https://www.emergentmind.com/topics/flexduo).
  Reported: an explicit Idle state (vs binary speak/listen) that filters irrelevant audio, cutting
  false interruptions by 24.9% and improving response accuracy by 7.6% (verified against the
  paper's abstract; corrected from an earlier draft's rounded 23%/8%).
- **Genealogy:** origin-domain **speech**; method (finite-state control decoupled from the model
  it controls) is **ported** from general modular-agent/tool-orchestration design (control-plane vs
  data-plane separation), applied natively to speech duplex.
- **Training-free vs fine-tuned:** the pluggable module itself is trained (a 3-state — Speak/
  Listen/Idle — controller), but the underlying **half-duplex dialogue backbone it wraps is reused
  unmodified** ("direct reuse of existing half-duplex dialogue systems").
- **Class + verdict — the important boundary case:** this is the closest thing in the lane to an
  **element** (a new sensing/control component bolted onto an unmodified dialogue model) rather
  than a constraint requiring backbone change. It still requires training a new small model, so it
  is not zero-shot/training-free in the strict sense, but it demonstrates that *turn-taking policy*
  (not simultaneous generation) is separable and modularizable, unlike the base-generation
  capability itself. This is a genuine nuance against a blanket "all duplex = constraint" reading,
  though FlexDuo does not give the underlying model new simultaneous-generation ability — it only
  gates when the still-half-duplex model is allowed to run.
- **Fence tag:** single-session.
- **Omni role:** sensor/controller wrapping a separate brain (the reused half-duplex backbone) —
  a hybrid decomposition rather than one fused hybrid model.
- **Delta:** NEW; flags the sharpest exception to "full duplex = pure constraint" found in this
  lane.

### 11. SoulX-Duplug — plug-and-play streaming semantic-VAD state predictor (on-disk benchmark note)
- **Recognized problem:** cascaded VAD/ASR/turn-detection modules are brittle and independently
  trained; catastrophic forgetting and limited scalability plague full-duplex retrofits. Source:
  [arXiv:2603.14877](https://arxiv.org/abs/2603.14877) (March 2026; code
  [github.com/Soul-AILab/SoulX-Duplug](https://github.com/Soul-AILab/SoulX-Duplug); eval set
  [SoulX-Duplug-Eval](https://huggingface.co/datasets/Soul-AILab/SoulX-Duplug-Eval)). Note: this
  project's benchmark inventory lists `soulx-duplug` as an on-disk asset for eval lanes — this
  entry is the source paper for that asset, recorded here as landscape, not as an eval-lane pick.
- **Genealogy:** origin-domain **speech**; folds VAD + streaming ASR + turn-detection into one
  jointly-trained streaming module — **native** speech method with a **ported** idea (joint
  multi-task streaming objective, common in LLM multi-task post-training) applied to the
  turn-detection problem.
- **Training-free vs fine-tuned:** the module is trained with a streaming-ASR objective for
  semantic supervision; it is "plug-and-play" **relative to the dialogue backbone** (no
  backbone retraining claimed) but the module itself is not training-free.
- **Class + verdict:** same boundary-case pattern as FlexDuo — an **element**-like bolt-on sensor
  for turn/state prediction, separable from the (unmodified) dialogue backbone; the underlying
  full-duplex *generation* capability is still supplied elsewhere.
- **Fence tag:** single-session.
- **Omni role:** sensor (explicitly framed as "serving as a semantic VAD").
- **Delta:** NEW.

### 12. Full-Duplex-Bench — turn-taking capability benchmark
- **Recognized problem:** no standardized, reproducible way to compare full-duplex spoken dialogue
  models on pause handling, backchanneling, turn-taking, and interruption management; ad hoc
  qualitative demos dominate. Source: [arXiv:2503.04721](https://arxiv.org/abs/2503.04721) (Lin,
  Lian, Li, Wang, Anumanchipalli, Liu, Lee; March 2025; code
  [github.com/DanielLin94144/Full-Duplex-Bench](https://github.com/DanielLin94144/Full-Duplex-Bench)).
  Follow-ons in the same family, found but not separately verified in depth here: Full-Duplex-Bench-v2
  (multi-turn, automated examiner, [arXiv:2510.07838](https://arxiv.org/html/2510.07838)) and
  Full-Duplex-Bench-v3 (tool-use under disfluency, [arXiv:2604.04847](https://arxiv.org/html/2604.04847)).
- **Genealogy:** origin-domain **speech**, evaluation-methodology idea **ported** from the general
  LLM-benchmark pattern of automatic, reproducible, task-decomposed scoring.
- **Training-free vs fine-tuned:** n/a — it is a benchmark/measurement tool, not a model.
- **Class + verdict:** n/a for element/usage-pattern axis (it is an evaluation instrument); relevant
  as the measurement layer that would be needed to check any future frozen-model-adjacent duplex
  claim.
- **Fence tag:** single-session (benchmark evaluates single conversational sessions).
- **Omni role:** n/a (evaluation harness, not a model).
- **Delta:** NEW.

### 13. Survey — "A Survey of Full-Duplex Spoken Dialogue Systems" (L0-L3 hierarchy, realization gap)
- **Recognized problem:** terminology and taxonomy for "full-duplex" are ambiguous across papers —
  unclear where duplex decisions are made, what interaction types are supported, or how systems
  behave moment-to-moment; the survey proposes L0-L3 Architectural Hierarchy, a T×I×R Interaction
  Ontology, and an IDLE/LISTEN/SPEAK/WAIT/DUAL Decision State Machine to standardize this. Source:
  [arXiv:2606.19453](https://arxiv.org/abs/2606.19453) (June 2026; authors from Zhejiang Univ.,
  Alibaba Qwen team, Tencent HunYuan, ByteDance).
- **Genealogy:** origin-domain **speech**; taxonomy methodology **ported** from general
  systems/HCI state-machine formalization.
- **Training-free vs fine-tuned:** n/a — meta-analysis/survey, not a trained system.
- **Class + verdict:** directly load-bearing for this lane's synthesis — the survey documents a
  **"realization gap"**: "although many architectures can in principle operate in full-duplex
  states, their observed behavior remains constrained by the interaction patterns represented in
  training and evaluation." This independently corroborates that full-duplex is bounded by what a
  base architecture was trained/architected for — CONFIRMS the constraint classification, and adds
  the sharper point that *architectural capacity for* duplex does not automatically yield duplex
  *behavior* without matching training data (i.e., even having the right base architecture is not
  sufficient without the right training distribution — a second constraint layer beyond
  architecture).
- **Fence tag:** n/a (survey).
- **Omni role:** n/a.
- **Delta:** NEW; the "capacity-without-training-data" nuance is new information not in the prior
  archive.

### 14. Survey — "From Turn-Taking to Synchronous Dialogue" (Engineered vs Learned Synchronization)
- **Recognized problem:** unify how the field categorizes full-duplex spoken language models
  (FD-SLMs) — modular/hand-engineered turn-taking control vs end-to-end learned synchronization —
  and unify evaluation across Temporal Dynamics, Behavioral Arbitration, Semantic Coherence, and
  Acoustic Performance. Source: [arXiv:2509.14515](https://arxiv.org/abs/2509.14515) (Sept 2025).
- **Genealogy:** origin-domain **speech**; taxonomy-building, methodology **native**.
- **Training-free vs fine-tuned:** n/a — survey.
- **Class + verdict:** this is the single clearest piece of literature-level corroboration of the
  base-vs-engine split used in this lane's synthesis above: **"Engineered Synchronization: modular
  architectures"** (control-layer approaches like FlexDuo/SoulX-Duplug) vs **"Learned
  Synchronization: end-to-end architectures"** (Moshi/dGSLM/SyncLLM-style base-model retraining).
  Also names three fundamental obstacles common to the whole field: **"synchronous data scarcity,
  architectural divergence, and evaluation gaps."**
- **Fence tag:** n/a.
- **Omni role:** n/a.
- **Delta:** NEW; the engineered/learned split is a useful, independently-sourced formalization of
  this lane's own base/engine distinction (triangulates it rather than being this lane's own
  invention).

### 15. TurnGuide — turn-level text-speech interleaving for meaningful dialogue
- **Recognized problem:** full-duplex spoken LMs, once trained, still generate semantically weak or
  incoherent responses over long speech sequences because of limited high-quality spoken dialogue
  training data; TurnGuide targets *dialogue quality*, not turn-taking timing per se. Source:
  [arXiv:2508.07375](https://arxiv.org/abs/2508.07375) (Aug 2025, "TurnGuide: Enhancing Meaningful
  Full Duplex Spoken Interactions via Dynamic Turn-Level Text-Speech Interleaving").
- **Genealogy:** origin-domain **speech**; method (interleaving discrete text tokens at turn
  boundaries to inject LLM-level semantic planning into a duplex audio stream) is **ported** from
  the "inner monologue"/chain-of-thought-adjacent idea of interleaving text reasoning into
  generation, seen originally in Moshi and in text-LLM CoT.
- **Training-free vs fine-tuned:** presented as a generation approach for existing end-to-end
  full-duplex models (FD-SLMs); abstract does not confirm it is decoding-only, but the design
  (dynamic turn segmentation of the assistant's own output) strongly implies it operates over/near
  an already-trained duplex model's generation loop rather than requiring a new base architecture —
  flagged as **plausible but not confirmed training-free at the base-model level**; regardless, it
  still presupposes a full-duplex base model already exists (obtained via the constraint-tier
  methods above), so it is not itself a route from a frozen non-duplex model to duplex.
- **Class + verdict:** most plausibly a **usage-pattern-like refinement** layered on top of an
  already-duplex-capable base — i.e., it optimizes dialogue quality *within* the duplex regime, not
  the crossing of the duplex boundary itself. Included as an illustration that most "improvements"
  in this space are refinements assuming the constraint has already been paid.
- **Fence tag:** single-session.
- **Omni role:** hybrid.
- **Delta:** NEW; marked lower-confidence ("plausible but not confirmed") per the hard rule against
  overclaiming from an abstract-only read.

---

## Negatives / empty cells (first-class)

- **No system found that adds full-duplex/turn-taking capability to a frozen omni model purely via
  prompting or decoding-time intervention (no new trained module, no weight change).** Every
  landscape entry either (a) retrains/fine-tunes the backbone (Moshi, LSLM, dGSLM, SyncLLM,
  VITA-1.5, VITA-Audio, Mini-Omni2, OmniFlatten), or (b) trains a small bolt-on control/sensor
  module even though it reuses an unmodified dialogue backbone (Freeze-Omni's classifier head,
  FlexDuo, SoulX-Duplug). Category (a) is a **constraint**; category (b) is the closest this lane
  gets to an **element**, but even that element must itself be trained — there is no zero-shot,
  training-free duplex-control module in the surveyed literature.
- **No published benchmark result showing a role/prompt-based "verifier" or "critic" pattern
  improving turn-taking or barge-in accuracy over a single frozen model** — consistent with the
  archive's L4 finding (N1/N2: no published pass@k or prompt-opt result on any voice-agent
  benchmark) and this project's broader usage-pattern-ceiling claim, but this lane found no direct
  duplex-specific test of that claim either way (an empty cell, not a refutation).
- **The two surveys ([arXiv:2606.19453](https://arxiv.org/abs/2606.19453),
  [arXiv:2509.14515](https://arxiv.org/abs/2509.14515)) do not report any case of full-duplex
  behavior being elicited from a model that lacks full-duplex training/architecture** — reinforcing
  the "realization gap" as a one-directional finding (architecture-without-training-data fails to
  produce duplex behavior; there is no counterexample of training-data/prompting-without-architecture
  succeeding).
- **OmniFlatten's "no new structure but new weights" case has no frozen-weight counterpart in the
  literature searched** — i.e., no one has published "same architecture, same weights, just a
  different flattening/scheduling of the same frozen LLM's decoding" that yields full duplex. This
  is a genuine empty cell worth flagging for future search (it is the exact frozen-model experiment
  this project's thesis would predict should fail).

---

## Verifier notes (adversarial pass, 2026-07-06)

**URLs spot-checked (15 of the lane's ~24 distinct sources, via WebFetch against the live
arXiv abstract/HTML pages and one GitHub repo):** arXiv:2410.00037 (Moshi, incl. GitHub repo),
2411.00774 (Freeze-Omni), 2408.02622 (LSLM), 2203.16502 (dGSLM), 2409.15594 (SyncLLM),
2501.01957 (VITA-1.5), 2505.03739 (VITA-Audio, incl. full-text latency figure), 2410.17799
(OmniFlatten), 2502.13472 (FlexDuo, incl. full-text conclusion for the "direct reuse" quote),
2603.14877 (SoulX-Duplug), 2604.04847 (Full-Duplex-Bench-v3), 2503.04721 (Full-Duplex-Bench),
2606.19453 (survey, incl. author-affiliation check), 2509.14515 (survey), 2508.07375
(TurnGuide). Two secondary links (`freeze-omni.github.io`, `emergentmind.com/topics/flexduo`)
could not be fetched from this session (sandbox domain-safety block on lesser-known hosts, not
evidence of a broken link) and were not independently confirmed; both are secondary/redundant to
already-verified arXiv sources for their respective claims, so this does not affect any verdict.

**Findings:**
1. **Fixed — numeric error.** FlexDuo's reported false-interruption-rate/accuracy deltas were
   given as a rounded "23%"/"8%"; the paper (arXiv:2502.13472 abstract) actually reports 24.9%/
   7.6%. Corrected in entry 10 above.
2. **Fixed — recency-window flagging inconsistency.** The lane's own convention (first applied to
   dGSLM and Mini-Omni2) is to tag pre-2025-01 entries as outside the stated 2025-01..2026-07
   window and justify inclusion via the genealogy/lineage rule. Five entries — Moshi (2024-09/10),
   Freeze-Omni (2024-11), LSLM (2024-08), SyncLLM (2024-09), OmniFlatten (2024-10) — were missing
   this tag even though they are equally out-of-window. Added the same flag to all five for
   consistency; no entry is dropped, since all five are defensible as directly-cited ancestors of
   in-window systems, but the window-membership bookkeeping was inconsistent before this pass.
3. **Verified, not fabricated.** The FlexDuo "enabling the direct reuse of existing half-duplex
   dialogue systems" quote is real but lives in the paper's Conclusion, not its Abstract — confirmed
   via the arXiv HTML full text. The survey's (2606.19453) claimed Zhejiang
   Univ./Alibaba-Qwen/Tencent-HunYuan/ByteDance affiliations are confirmed from the paper's author
   list. VITA-Audio's 236ms→53ms latency and 3-5x speedup figures are confirmed from the paper's
   §4.4 latency evaluation (not stated in the abstract alone, but present in the full text).
   SoulX-Duplug (2603.14877, March 2026) and Full-Duplex-Bench-v3 (2604.04847, April 2026) are both
   real, correctly-dated papers, not invented IDs.
4. **Framework verdicts (element vs usage-pattern, new-info vs read-out) — no wrong calls found.**
   FlexDuo and SoulX-Duplug are correctly classed as the lane's "element" boundary case (a
   separately-trained control/sensor module bolted onto an unmodified, reused dialogue backbone —
   i.e., two distinct trained systems, not a prompt/decoding usage-pattern over one frozen model,
   so "element" rather than "read-out" is the defensible call). TurnGuide is correctly hedged as a
   "usage-pattern-like refinement" over an already-duplex-capable base rather than confirmed
   training-free, since its abstract does not establish whether it adds trained components — the
   lane appropriately marks this "plausible but not confirmed" rather than overclaiming a read-out
   verdict. Freeze-Omni is correctly kept a system-level constraint despite the LLM backbone being
   frozen, since the duplex classifier head is new trained structure — this is the sharpest and
   correctly-drawn distinction in the lane between "frozen LLM" (weak, common usage in this
   literature) and this project's stricter "no weight and no structure change to the whole system."
   OmniFlatten is correctly kept a constraint on weight-change grounds alone, even though it adds no
   new structure — a good-faith stress test of the framework's "no weight AND no structure" bar that
   the lane passes correctly.
5. **Recency and negatives (per framework check d).** Excluding the two explicitly-tagged
   genealogy roots (dGSLM, 2022) and the five now-tagged 2024 ancestors above, the remaining 8
   entries plus both surveys fall inside 2025-01..2026-07, satisfying the recency requirement for
   the lane's core (non-ancestor) evidence. The "Negatives / empty cells" section is present and
   substantive (no zero-shot/training-free duplex-control module found; no role/prompt "verifier"
   result on turn-taking; no frozen-weight OmniFlatten counterpart) — this requirement is met.
6. **No invented claims found.** Every checked quote, statistic, and citation traced to a real,
   correctly-dated source; no dead or mismatched URLs among the 15 checked.
