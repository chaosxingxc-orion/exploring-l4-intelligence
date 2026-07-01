# Deep adversarial review of W5 — PRINCIPLE · PURPOSE · FEASIBILITY (not syntax)

> The owner judged the prior 4-round review too shallow (syntax/semantic: KL directions, β-conventions, table
> consistency, verbatim signatures). This review attacks the three axes that matter — 原理 / 目的 / 可行 — via three
> independent hostile expert reads (blind to each other), plus a forensic provenance pilot. Verdict: **the agent-level
> / L4 framing does not survive; most flaws are not fixable by revision.** Owner decision → collapse to an honest
> single-model paper (Option A), executed as a POMDP (see `pomdp-restructure-log.md`).

## 原理 (principle) — the theory is tautology-where-proven, unmodellable-where-interesting
- **P1 (kills the central thesis).** `qstar_product` is literally `exp(a+b)=exp(a)·exp(b)` (`OptSpace.lean:257–259`).
  Separable reward + product base ARE the exact conditions under which decomposition is a no-op; the formalism cannot
  even *represent* a mechanism by which agentic decomposition helps (non-separable reward, cross-block dependence,
  support expansion, sampling intractability). **Smoking gun:** `OptSpace-notes.md:36` originally billed this theorem
  as the OPPOSITE ("context isolation ENLARGES the space ⇒ RL attainable & grows with #agents"); the paper silently
  inverted its own motivating hypothesis and reframed the refutation as the contribution. **Not fixable in this
  formalism** — needs a genuinely new non-separable decomposition bound.
- **P2.** OSA-1 = the Donsker–Varadhan / free-energy variational identity (1970s); a ceiling makes no falsifiable
  prediction. The one *certified* quantitative Lean theorem `gain_le_of_hoeffding` is "given X≤S and gain=X, conclude
  gain≤S" — `S` is an abstract real; `spread²/(8β)` is never formalized (discharged "on paper"). The machine-checked
  halo covers only trivial algebra.
- **P3.** Finite `Fintype Z` + `q0>0` ⇒ spread = global range ⇒ the certified bound is `gain ≤ 1/(8β)` for 0/1
  rewards — vacuous exactly for the concentrated, autoregressive omni models the paper targets.
- **P4 (self-contradiction).** Gibbs-tilt of a FIXED q0 cannot model ICL / prompt-conditioning / retrieval (which
  change q0 / its support). "Flat conditioning" is really the model IGNORING the instruction = a **model-class**
  effect — contradicting the slogan "the lever is reward structure, not model class." The hedge "spread is
  model-induced" destroys the slogan (spread partly *is* the model class).
- **P5–P8.** "Gain only from new non-degenerate rewards" is circular; strict positivity has no floor so the k-growth
  story is vacuous (and the floor, Conjecture 1, is falsified on the flagship); credit assignment (a separable
  observable Rᵢ) is the whole hard problem and is *assumed*; β is an exogenous knob so `spread²/(8β)` is about
  regularization, not the reward; the rollout-deficit "corollary" is the master identity relabeled.

## 目的 (purpose) — reject: reason-to-exist not established
- **U1 self-refuting:** advocates agent-level RL, then proves (`qstar_product`) the agent object is inert; the escape
  (add rewards) is a single-model act, not agentic. **U2 VoI≈0:** no decision changes on either answer; novelty is
  "an empty cell in a design matrix"; the authors concede the system is "not worth building now." **U3 no new
  knowledge:** C1 definitional, C2 open, C3 a null, C4 unbuilt, C5 a nonexistent benchmark. **U4:** the W4
  disentanglement north-star is refuted (paralinguistics) or trivial (a content encoder encodes content). **U5:** the
  "could-win" mechanism is conceded textbook PLDA/CUSUM; the agentic residual is bookkeeping pre-registered as null.
  **U6:** the two-class taxonomy carries no predictive weight. **U7:** "L4/agent-level" is undefined and voided by the
  paper's own theorem; candor is used as a shield.

## 可行 (feasibility) — the escape route is unreachable on THIS disk
- **S1 FATAL (data).** The cross-session paralinguistic benchmark's precondition — same-speaker, cross-session /
  cross-channel, affect-varying audio — exists in **NONE** of the 28 **frozen** datasets (only CREMA-D: acted,
  single-session, 12 sentences, 91 spk once each). The set is FROZEN → cannot be acquired. The plan's own SV-EER
  admission band rejects the only thing CREMA-D can produce. **The headline benchmark cannot be built.**
- **S2 FATAL (tooling) + provenance mis-attribution.** No local generative operator exists (`grep llama_cpp|GGUF|
  vllm|.generate|logprob` across the committed W4 repo = 0). The only model loader is the omni-embed **bi-encoder**;
  the only "generation" code calls a **remote DeepSeek API**. → The load-bearing Table-opB content/intent gains,
  attributed to "a single frozen generative omni policy, best-of-N," were actually produced by **frozen bi-encoder
  cosine retrieval over static candidate-cards** (see Provenance pilot below).
- **S3 FATAL (unbuilt).** ECAPA / PLDA / AS-Norm / pyannote / CUSUM / BOCPD / SER-head / memory-graph / skill-library
  / the RL loop itself — all UNWRITTEN. Every pre-registered falsifier pits nonexistent code against nonexistent code.
- **S4–S7.** Best honest case even if S1–S3 solved = "reused single-model numbers + a null"; human SER annotation +
  spontaneous corpus + full stack = multi-person/multi-month; "≥2 backbones" conflates a bi-encoder with a 30B-A3B
  MoE whose GGUF logprob interface is unverified; the novel axis has measured-zero spread (loop optimizes a flat
  reward). Local compute is a **24 GB** RTX 5090 Laptop GPU.

## Provenance pilot (POMDP Step 1) — forensic trace of the three positive numbers
- **Finding:** SLURP +0.330, MInDS +0.132, URO +0.335 are produced by the **frozen omni-embed bi-encoder** doing
  cosine Acc@1 selection over hand-authored static text candidate-cards (`evaluation/tool_intent.py:237,247,258`;
  `SentenceTransformer(omni-embed-nemotron-3b)`), under a verifiable reward. They are **LOCAL-FROZEN and honestly
  keepable** — but **mis-attributed**: the paper sells them as "generative candidates … Operator-B … best-of-N," when
  the bytes show Operator-A-class **bi-encoder selection**, no generative policy, no decoding.
- **Caveats:** (i) the URO `+0.130` low-margin rerank IS **remote DeepSeek** (`uro_qa_low_margin_rerank.py:343`) — cut
  or re-run local; (ii) none of the three had a committed score file.
- **MInDS re-run (fresh, committed):** frozen bi-encoder, MInDS-14 en-US, n=182, seed 42 → naive 0.720, raw-schema
  0.857, **policy 0.984**; **policy vs raw-schema +0.126 [+0.077,+0.181] SIG**. This **vindicates** the paper's
  `0.852→0.984 (~+0.13)` with a committed paired-CI artifact (`_repro/minds14_toolintent_paired.json`). The number is
  real; only the mechanism label ("generative best-of-N" → "frozen bi-encoder verifiable selection") and the baseline
  arm label were wrong.

## Convergent verdict → the collapse
All three axes converge: the paper does not survive as an agent-level contribution, and the flaws are mostly not
fixable by revision. What IS real, local, and reproducible is **training-free RL as verifiable-reward SELECTION on a
single frozen speech model** (the bi-encoder content/intent gains) plus a **scoped paralinguistic negative**. The
agent theory (OSA-2/3), the cross-session benchmark, and the system move to honest future work. Owner decision:
**collapse to that honest single-model paper**, executed as a POMDP with probe-before-commit and rollback discipline
(`pomdp-restructure-log.md`).
