---
title: "Stage-1 problem definition v2 — the frozen-omni agentic construction plan + ranked research directions (for the K/T9 owner checkpoint)"
date: 2026-07-06
stage: 1-argumentation
status: "D4 — distilled from the D3-reviewed survey paper. This is decision material for the owner checkpoint (K/T9); it does NOT auto-advance to Stage-2. Ranking rubric frozen before ranking."
---

# Stage-1 problem definition v2

Distilled from the reviewed survey (`2026-07-06-omni-agentic-systems-survey.md`, D3 `sound-with-corrections`)
+ framework (`2026-07-06-omni-agent-elements-vs-usage-framework.md`) + in-house evidence + the Lean bound &
convergence theorem. **Terminal Stage-1 gate — the owner selects; no auto-rollover to Stage-2.**

## 1. The construction plan (what the omni agentic system IS)
The survey settles the *shape* (the omni-role architecture is left to the owner, §3):
- **A frozen text-capable brain + swappable elements (freeze-and-bolt-on).** This is the thesis's native
  architecture and is competitive-to-best on verifiable agentic tasks (element-quality-confounded, §7 of the
  paper). The brain may be the omni itself or a commodity text LLM (owner's Challenge-1); the omni's
  non-commodity role is **perception** (exposing >transcript) + **audio-keyed memory/knowledge**.
- **Capability comes only from adding new-info ELEMENTS** (tools, knowledge, memory, a complementary model)
  — or an **in-scope generative-law (decoding) edit**; orchestrating one frozen model more cleverly is
  oracle-bounded (machine-checked). Full-duplex is out (needs a base change).
- **The verification fork is load-bearing:** verifier-as-tool (trained/symbolic) is an element and works;
  verifier-as-role (prompted) is read-out and weak. Any reward/selection must use the former.

## 2. Ranking rubric (frozen before ranking)
Score each candidate 1–3 on: **(R1) thesis-decisiveness** (does the result settle a load-bearing question?);
**(R2) novelty/unoccupied** (is the cell genuinely empty, not a known-answer demo?); **(R3) frozen-contract
fit + boundary-cleanliness**; **(R4) Stage-1 cheapness** (a cheap directional validation exists); **(R5)
asset/W-line fit** (our on-disk benchmarks + W1/W4). Higher = better. Fence tag noted separately.

## 3. Candidate research problems (ranked)

| # | Candidate | axis | fence | R1 | R2 | R3 | R4 | R5 | Σ |
|---|---|---|---|---|---|---|---|---|---|
| **GAP-6** | oracle-controlled same-model self-check (does ② ever beat the model's *own* oracle@N?) | ② vs bound | single | 3 | 3 | 3 | 3 | 3 | **15** |
| **GAP-3** | omni-as-decorrelated-verifier for best-of-N; binding δ_corr | ① via decorrelation | single | 3 | 3 | 3 | 2 | 3 | **14** |
| **GAP-1** | training-free reward-guided best-of-N reaching pass^k on a voice-agent bench | ② gated by ① | single | 2 | 2 | 3 | 2 | 3 | **12** |
| **GAP-7** | in-scope contrastive/logit-surgery decoding as an info-free ceiling-raiser (speech) | ③ (in-contract) | single | 3 | 3 | 2 | 2 | 2 | **12** |
| **GAP-2** | audio/speaker-keyed cross-session memory mutation + verifiable admission gate | ① store + ④ gate | cross | 2 | 3 | 3 | 1 | 3 | **12** |
| **GAP-4** | active audio zoom/re-sensing as an input-transformation element | ① (new bits) | single | 2 | 3 | 3 | 2 | 2 | **12** |
| **GAP-5** | paralinguistic-conditioned agentic decision w/ verifiable reward | ① channel + ④ | single | 2 | 2 | 2 | 2 | 2 | **10** (precondition: perception delta real, §9 p6 inconclusive) |

## 4. Recommended (2–3, for owner discussion)
**GAP-6 (top) — the decisive falsification test.** *Does structured same-model self-check exceed the frozen
omni's own oracle@N, or merely recover it?* Cheapest, most decisive: it is the one experiment that could
**refute** the whole framework (if ② crosses, the thesis is wrong) or confirm it. Uses our on-disk
verifiable benchmarks; boundary-clean; single-session. **Run this first.**

**GAP-3 (co-flagship) — omni decorrelated-verifier, with theory in hand.** The genuinely-open positive
direction: two context-differentiated views of the same frozen omni as a verifier for best-of-N. It already
has its **convergence theory** (`TfrlProofs.BestOfNConvergence`: converges iff the estimation error / δ_corr
→ 0; the unconstrained non-decorrelated verifier provably does not — the E10/E10b regime). Directly reuses
W1's reward machinery and the W4 omni-embedding as a decorrelation lever. Its result *is* the achievable
δ_corr — a real Stage-2 number, not a known-answer demo.

**GAP-1 (flagship engineering) — voice-agent best-of-N to the pass^k ceiling.** The thesis-central empty
cell, but partly a **known-answer demo** of W1's lever (element-gated selection approaches pass@N by
construction); its new knowledge is the deployed-vs-ceiling gap on *interactive voice-agent* tasks
(τ²-voice/EVA-Bench), which no one has measured. Strong asset fit; medium novelty.

**Wildcard — GAP-7 (in-scope decoding edit).** The review-surfaced info-free ceiling-raiser the canonical
permits; novel and thesis-relevant (it is the one lever that raises the ceiling *without* an element), but
needs decoding-level tooling we have not built.

## 5. The omni-role architecture decision (T9's first fork)
Survey evidence (paper §7), for the owner to weigh — **not pre-locked**:
- **Sensor + text-LLM brain (A):** the frozen omni exposes the >transcript delta to a strong text-LLM
  controller. *Survey lean:* this is the freeze-and-bolt-on shape competitive on verifiable tasks and the
  thesis's native architecture; but the perception delta that justifies the omni-as-sensor is **not yet
  established** (§9 p6 inconclusive — the strong-external-ASR control is a precondition).
- **Omni end-to-end brain (B):** activate the frozen omni's own reasoning/knowledge. Closest to the project
  thesis; but native hybrids retain only 31–51% of text capability and give up the text-brain ceiling.
- **Hybrid/layered (C):** omni sensor + audio-keyed memory below, text-LLM planner above.

*Directional recommendation (for discussion): resolve the perception-delta precondition (GAP-5's control)
before committing to A; run GAP-6/GAP-3 (architecture-agnostic) first.* The choice is genuinely the owner's.

## 6. Fence & discipline
The 2026-07-03 closure was owner-amended (Decision-Log 2026-07-06) to re-open cross-session work; GAP-2 is
the only cross-session candidate and is covered by that amendment. All candidates carry the
[[Information-Boundary-Guard]] (no test-item leakage; deployable rewards only). All in-house numbers cited
are directional; small-n settles nothing. Selecting a candidate opens a fresh Stage-2 Research-Proposal
instance (pre-registered, powered-n, paired-bootstrap CIs) — this document does not start it.
