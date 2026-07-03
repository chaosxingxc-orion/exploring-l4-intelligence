---
title: "Pre-registration — Step 1 Rationality Analysis: Training-Free RL Direction & Omni Agentic Extension"
date: 2026-07-03
status: FROZEN-ON-COMMIT
owner_ack: "ACKED 2026-07-03 (owner, in-session; criteria unchanged from freeze commit b19bff2)"
null_hypothesis: "2026-07-02 deep-review NO-GO verdict (reviews/deep-review.md) — stands unless overturned by NEW information"
timebox: "10 working days from the freeze commit"
---

# Pre-registration: agentic-TFRL step-1 rationality analysis

**Freeze anchor.** The commit hash of this file is the freeze anchor. Every analysis lane, adversary, judge, and synthesis step is bound to the criteria below as of that commit. Amendments require owner sign-off plus a logged diff in `wiki/Decision-Log.md`; un-logged deviation invalidates the affected lane's output.

**Question under test.** (i) Is training-free RL for frozen omni speech models rational as a research direction? (ii) Should we build an omni agentic system — skills / memory / routing over frozen models, no weight updates — to extend it?

**Null hypothesis.** The 2026-07-02 hostile-review verdict that killed the agent-level framing. This campaign tests whether NEW information overturns it. **Inconclusive = NO-GO.** NO-GO is a fully valid outcome: it citably closes the converged paper's "deferred, not disproved" future-work question.

---

## 1. B0 delta gate

**What was killed on 7/02.** Agent-level TFRL as a *value-headroom-adding* mechanism on a *fixed* reward, inside the OSA formalism, targeting cross-session paralinguistics on data absent from the frozen manifest. The killed theorems bound selection on a fixed base distribution q0 under a fixed reward R:

> gain = β·KL(q0‖q\*) ≤ spread²/(8β), action-space agnostic.

These theorems are **airtight**. `qstar_product` shows that under separable reward and product base, decomposition into isolated contexts is a no-op — the isolated optimum equals the monolithic optimum. No lane may relitigate this.

**What is materially different today (the only admissible delta axes).** A GO-supporting argument is admissible **only** if it operates on an axis the killed formalism does not represent:

- **(a) Changing q0** — conditioning, memory injection, retrieval, support expansion. The killed theorems treat q0 as fixed; an operator that moves q0 (and hence the *oracle ceiling itself*) is outside the box.
- **(b) Estimating R** — deployment-time R is not reference-free computable. The C1 artifact quantifies this as the **realized-vs-headroom gap**: oracle selection +0.042 WER [0.029, 0.056] @ N=8, significant; label-free MBR null at every N; only ~10% of headroom realized. Closing the estimation gap is not bounded by any killed theorem, which assumes R is given.
- **(c) Sample complexity of realizing q\*** — the ceiling is unchanged, but the *cost* of hitting the optimum is not what the Gibbs identity speaks to. Decomposition may change realization complexity without changing headroom.

**Gate rule (B0).** Any GO-supporting claim that operates inside the killed box — fixed q0, given R, headroom-adding via context isolation — is **inadmissible a priori** and is struck without experiment. Every lane's first deliverable is a one-paragraph statement of which axis (a)/(b)/(c) it occupies and why it does not reduce to the killed object. A lane that cannot state this is closed at B0.

---

## 2. Pre-registered decision criteria (the frozen core)

### GO — build the scoped omni agentic system. ALL of G1–G4 required.

- **G1 (mechanism).** At least one mechanism lane M1–M5 survives, meaning BOTH:
  - **T-part:** a formal statement with explicitly stated assumptions that does NOT reduce to the tautology exp(a+b)=exp(a)·exp(b) under separability and does not contradict the spread lens; and
  - **E-part:** its cheap discriminating pilot meets its pre-registered threshold with paired-bootstrap **CI lower bound > 0**, AND the matched **no-agency control is null**.
- **G2 (VoI > 0).** A NAMED downstream decision that changes depending on the answer, plus pre-registered kill criteria for step 2. No named decision → U2 stands → no GO.
- **G3 (ingredients).** At least 2 of the paper's three ingredients concretely satisfied: **operator** (already resolved — S2, llama.cpp best-of-N on frozen Qwen3-Omni-30B); **corpus** (a named on-disk / pseudo-session / TTS path, or a planned-expansion path via lockfile regeneration); **theorem** (the G1 candidate).
- **G4 (budget).** Minimal build ≤ **3 person-weeks**, runs on the single 24 GB RTX 5090 Laptop GPU, no licensing/consent blockers.

### GO-minimal — build ONLY the selector-memory agent.

Granted iff: only **M5** passes, AND its shuffled-memory ablation shows accumulation is load-bearing (**shuffled control loses ≥ 50% of the gain**), AND G2/G4 hold for the reduced scope. This grade exists to stop a bounded agency role from being inflated into the full system.

### NO-GO.

Declared if ANY of:
- B0 fails (no admissible delta survives the gate); OR
- all mechanism lanes hit their kill thresholds AND the M5 ablation shows accumulation is not load-bearing; OR
- the time-box (**10 working days from criteria freeze**) expires with criteria unmet.

**Inconclusive = NO-GO.** NO-GO receives a Decision-Log entry equally detailed as a GO would, PLUS explicit re-open conditions:
- **r1** — a public cross-session, same-speaker speech corpus appears;
- **r2** — a peer-reviewed non-separable decomposition bound appears;
- **r3** — a mechanism-lane kill is overturned by new literature.

Absent r1–r3, the question is **closed**.

### PIVOT (pre-named; choosing one is a success, not a failure).

- **P-A — selector-learning-without-agency.** Trigger: M5's E-part beats MBR with realized WER reduction ≥ **0.015**, CI-LB > 0, on a fresh confirmatory slice, BUT the accumulation ablation is negative. → Single-model paper #2 on closing the C1 realized-vs-headroom gap.
- **P-B — benchmark-first.** Trigger: G3 fails only on the corpus ingredient and B5 shows the benchmark is buildable. The dataset freeze is POLICY, not physics — planned expansion via lockfile regeneration is allowed.
- **P-C — theory-only.** Trigger: a surviving T-part with null E-parts. → Formal contribution extending `proofs/tfrl`.
- **P-D — condition-mapping.** Part-A continuation: clean-audio / corpora / N-scaling characterization of the C1 headroom.

---

## 3. Scope fence

- **OUT:** gradient-trained rerankers, learned reward models, LoRA/adapter anything — outside the training-free thesis by definition.
- **IN:** frozen-model memory / prompt-state selectors — no weights change, state lives in text/retrieval structures.
- Enforcement: every lane adversary checks each proposed mechanism against this fence before any experiment runs; a fence violation is struck, not "noted".

---

## 4. Statistical standard

- Paired bootstrap **95% CI on per-item deltas** for every comparative claim.
- **≥ 3 seeds** wherever sampling is stochastic (generation seeds pooled, per the SC-SEED control).
- **Dev/test separation:** the committed 144-utterance C1 pool is **DEV-SPENT** for selector purposes. Confirmatory numbers come from fresh test-other slices, each touched **once**.
- **Holm correction** whenever a lane compares > 2 configurations.
- Every number lands in a committed `_repro/` artifact with a `reproduce:` line, runnable in WSL2 Ubuntu-24.04 with `SPEECHRL_DATA_DIR` set.

---

## 5. Mechanism lanes and pre-registered kill/pass thresholds

### M3 — support expansion (runs FIRST; strongest lane)

- **Claim:** user-lexicon ASR personalization. Selection cannot create support; memory injection moves the **oracle ceiling itself**. Information-availability argument: the lexicon does not exist within a single session, so no single-session operator can supply it. Axis (a) — changing q0.
- **Phase-0 zero-support check (RUNS NOW):** sample **N = 32** without context on utterances containing recurring rare entities, via the local llama.cpp Qwen3-Omni operator. **KILL the lane if the correct entity already appears in > 1% of samples** (support already present → injection adds nothing the ceiling lacks).
- **Phase-1 four-arm pseudo-session pilot (DESIGNED and pre-registered now; run post-GO):** arms = no-memory / reward-gated memory / append-only memory / oracle-lexicon. GO-support threshold: with-memory oracle **entity-WER gain ≥ 10 points absolute**, CI-LB > 0, AND the gated-vs-append contrast reproduces the compounding condition.

### M5 — reward estimation / selector accumulation (runs SECOND; the un-taken C1 thread)

- **Ontology pinned:** with fixed q0 and fixed oracle R, any learned selector's realized gain ≤ oracle headroom. M5 NEVER raises the ceiling; it closes the realization gap. Zero conflict with the killed theorems. Axis (b) — estimating R.
- **Falsifiable question:** does no-gradient cross-session accumulation (retrieval credit assignment) estimate R better than the best single-shot reference-free proxy?
- **Re-scoring pilot (RUNS NOW)** on the committed candidate pools — dev iterations on dev slices, confirmatory on a fresh slice touched once.
- **PASS:** beats MBR with CI-LB > 0 AND realized reduction ≥ **0.015** WER (~35% of headroom, vs MBR's ~10%).
- **Dispositive ablation — shuffled memory:** gain survives shuffling ⇒ agency not load-bearing ⇒ route to **P-A**; accumulation load-bearing (shuffled loses ≥ 50% of gain) ⇒ input to **GO-minimal**.
- **Goodhart guard:** report the true-WER trajectory as N grows; a proxy that improves while true WER degrades is a fail regardless of proxy score.

### M2 — cross-block dependence & M4 — sampling intractability relieved by isolation (construct/refute + full DESIGN only; fresh-sampling experiments post-GO)

- **M4 honest content:** decomposition changes **realization complexity** (hit cost ∏ 1/pᵢ vs Σ 1/pᵢ), not headroom. The T-part is an order-statistics hitting-probability lemma, NOT the Gibbs identity — it dodges P1 by construction. Axis (c).
- **M2 kill threshold (pre-registered for post-GO):** oracle-headroom delta **CI-UB < +0.01 WER kills** the lane.

### M1 — non-separable reward (conditional)

- Opened ONLY if M4 leaves a residue; M1's live content **is** M4's residue. Before opening, the lane must pre-register in writing the re-blocking attack it must answer (the adversary's demonstration that any proposed non-separable reward re-blocks into separable components).

**Ordering rule:** M3 → M5 → M2/M4 (design) → M1 (conditional). Cheapest killer runs first within each lane; a hit kill threshold stops the lane immediately — no "one more experiment".

---

## 6. Anti-motivated-reasoning safeguards (all structural)

1. **Null hypothesis + inconclusive = NO-GO + time-box.** The 7/02 verdict is the default; ambiguity resolves against GO; 10 working days hard stop.
2. **B0 delta gate.** Claims inside the killed box are struck a priori (§1).
3. **Prosecution/defense split.** The prosecution owns the objection ledger verbatim; defense answers are classified **ANSWERS** or **ROUTES-AROUND** only — "reinterprets" is not a permitted category.
4. **Novelty-of-information rule.** Every GO claim cites ≥ 1 item unavailable on 7/02: post-06/30 literature, a new theorem, a new pre-registered measurement, or a new analysis of the C1 artifact (the last is pre-registered here as exempt because the paper explicitly left the realized-vs-headroom thread un-taken).
5. **Criteria freeze by commit hash.** Amendments require owner sign-off + a logged diff.
6. **Fresh-adversary review** blind to lane deliberations before synthesis.
7. **Standing steelman-NO-GO.** The final recommendation must rebut it point-by-point or concede.
8. **Kill-first ordering.** Cheapest killer first; a kill threshold stops the lane; no post-hoc extensions.
9. **Language discipline.** "Deferred, not disproved" is scoping, not evidence. "First, to our knowledge" always carries the fast-follower caveat.
10. **Role separation.** Mechanism-defense authors do not write the criteria-application section; roles are logged.
11. **Test-set hygiene.** The 144-utterance C1 pool is dev-spent; confirmatory slices touched once (§4).
12. **Outcome-symmetric pre-writing.** GO and NO-GO decision-doc skeletons are drafted **before** any lane runs — included as Appendix B of this document.

---

## 7. Campaign topology (brief)

Phases 1–6 as approved:

1. **Delta scan** — 3 lanes, `delta_vs_archive` tags against the 17-file wiki/survey archive; 0-hallucination URL verification.
2. **Part-A memo** — direction-rationality (single-model TFRL) consolidated.
3. **Mechanism lanes** — M3 → M5 → M2/M4 (design), M1 conditional (§5).
4. **B3/B4/B5** — ingredients check, VoI/named-decision check, benchmark-buildability check.
5. **Steelman-NO-GO + 6-charge defense/prosecution panel** — 2 blind judges (disagreement defaults to *stands*) + ledger-holding meta-chair.
6. **Mechanical synthesis** — criteria applied mechanically + integrity check + fresh adversary.

Decision-doc front-matter: `recommended:` + `owner_verdict: PENDING`. **Owner gate** before any publication and before WF-2.

---

## 8. Appendix A — Objection ledger (frozen)

The prosecution owns this table verbatim. Defense answers are classified ANSWERS or ROUTES-AROUND per item.

| id | axis | statement | status | what_would_overturn |
|----|------|-----------|--------|---------------------|
| P1 | principle | [reviews/deep-review.md lines 10-16 (原理 P1)] The central theorem `qstar_product` is literally exp(a+b)=exp(a)·exp(b) (OptSpace.lean:257-259): separable reward + product base are exactly the conditions under which agentic decomposition is a no-op, so the formalism cannot even represent a mechanism by which decomposition helps (non-separable reward, cross-block dependence, support expansion, sampling intractability). Smoking gun: OptSpace-notes.md:36 originally billed the theorem as the OPPOSITE (isolation ENLARGES the space), and the paper silently inverted its own motivating hypothesis, reframing the refutation as the contribution. Not fixable within this formalism. | standing | A genuinely new non-separable irreducibility theorem — a formal statement that (i) does NOT reduce to exp(a+b)=exp(a)·exp(b) under separability, and (ii) operates on an axis the killed formalism does not represent: changing q0 (support expansion / conditioning as a q0-operator), estimating R (credit assignment / cross-block reward dependence), or the sample complexity of realizing q\* (sampling intractability) — proving that decomposing a task into isolated contexts adds optimization headroom a single model lacks. This is exactly the paper's own stated precondition (10-discussion.tex ~119-125). |
| P2 | principle | [deep-review.md lines 17-20 (原理 P2)] OSA-1 is the 1970s Donsker–Varadhan / free-energy variational identity, and a ceiling makes no falsifiable prediction. The only certified quantitative Lean theorem, `gain_le_of_hoeffding`, proves 'given X≤S and gain=X, conclude gain≤S' with S an abstract real; spread²/(8β) is never formalized (discharged 'on paper'), so the machine-checked halo covers only trivial algebra. | standing | A Lean formalization in which the quantitative content is DERIVED, not assumed: spread²/(8β) (or a variance/Bernstein refinement) proved inside Lean from the Gibbs tilt and concentration, plus at least one falsifiable numeric prediction (measured spread and β yielding a bound that an experiment could in principle violate and does not). |
| P3 | principle | [deep-review.md lines 21-22 (原理 P3)] Under finite `Fintype Z` with q0>0 everywhere, spread collapses to the global range, so the certified bound degenerates to gain ≤ 1/(8β) for 0/1 rewards — vacuous exactly for the concentrated, autoregressive omni models the paper targets. | standing | A concentration-aware bound in which the ceiling depends on q0's actual mass distribution (variance under q0, effective support, or a Bernstein-type bound) rather than the global range, formalized and shown non-vacuous (numerically informative) on a peaked autoregressive model's sampled candidate distribution. |
| P4 | principle | [deep-review.md lines 23-26 (原理 P4)] Gibbs-tilting a FIXED q0 cannot model in-context learning, prompt-conditioning, or retrieval, all of which change q0 or its support; and 'flat conditioning' is really the model IGNORING the instruction — a model-class effect — contradicting the slogan 'the lever is reward structure, not model class.' The hedge 'spread is model-induced' destroys the slogan, since spread partly IS the model class. | standing | An extended formalism where conditioning is a first-class q0-changing operator (a family q0(c) with a theorem cleanly separating reward-tilt gain from conditioning gain), together with an empirical decomposition showing measured spread differences are attributable to reward structure after controlling for model class (e.g., same reward, multiple frozen backbones, spread and gain co-varying as the theory predicts). |
| P5 | principle | [deep-review.md lines 27-30 (原理 P5-P8 bullet, clauses 1-2)] The claim 'gain comes only from new non-degenerate rewards' is circular, and strict positivity (`gain_pos_of_nonconstant`) has no quantitative floor, so the gain-grows-with-k story is vacuous — an arbitrarily small ε per block proves nothing; the proposed floor (Conjecture 1) is itself falsified on the flagship paralinguistic axis. | standing | A non-circular, task/data-level criterion (stated independently of the gain itself) that predicts which decompositions expose non-degenerate new reward components, PLUS a proven per-block lower bound (floor) with verifiable premises — i.e., Conjecture 1 replaced by a theorem whose hypotheses are empirically checked and satisfied on the flagship axis. |
| P6 | principle | [deep-review.md lines 27-30 (原理 P5-P8 bullet, clause 3)] Credit assignment — the existence of a separable, verifiable per-block observable Rᵢ — is the whole hard problem of agent-level RL, and the formalism simply ASSUMES it as a hypothesis rather than deriving or constructing it. | standing | A constructive credit-assignment method — extracting verifiable per-block rewards Rᵢ from a scalar joint return in a real agentic speech task — with either a correctness guarantee or strong pre-registered empirical validation (per-block rewards shown to drive block-level selection gains that compose into the joint gain), making Rᵢ an output of the theory instead of an assumption. |
| P7 | principle | [deep-review.md lines 27-30 (原理 P5-P8 bullet, clause 4)] β is an exogenous knob chosen by the experimenter, so the ceiling spread²/(8β) is a statement about regularization strength, not about the reward or the task; the theory's quantitative content can be tuned to say anything. | standing | A formulation in which β is ENDOGENOUS — derived from the actual procedure's budget (e.g., the effective β of best-of-N as a function of N, or a trust-region constraint of the deployed selector) — so that the ceiling becomes a reward- and budget-dependent prediction testable against measured realized gains. |
| P8 | principle | [deep-review.md lines 27-30 (原理 P5-P8 bullet, clause 5)] The rollout-deficit 'corollary' is the master identity gain = β·KL(q0‖q\*) relabeled — it has no independent mathematical content beyond the variational identity it restates. | standing | A rollout-deficit result with independent content: an inequality or characterization that is provably NOT an algebraic relabeling of the master identity (e.g., relating finite-sample rollout count to realized-versus-headroom gap with a rate), yielding a prediction the identity alone cannot make and that data could refute. |
| U1 | purpose | [deep-review.md lines 33-35 (目的 U1)] The paper is self-refuting: it advocates agent-level training-free RL, then proves via `qstar_product` that the agent object is inert (isolated optimum = monolithic optimum); the only escape — adding new rewards — is a single-model act, not an agentic one. | standing | A demonstration that some gain is realizable ONLY through decomposition: either the P1-style non-separable theorem, or an executed experiment where a new verifiable reward is constructible/computable only in the decomposed (multi-agent, isolated-context) configuration and the resulting gain survives a paired-CI test against the strongest single-model arm given the same reward. |
| U2 | purpose | [deep-review.md lines 35-36 (目的 U2)] Value-of-information ≈ 0: no decision changes regardless of which way the central question resolves; the claimed novelty is 'an empty cell in a design matrix'; the authors themselves concede the system is 'not worth building now.' | standing | A concrete decision that hinges on the outcome — e.g., a deployment or architecture choice with real cost stakes where the pre-registered agentic arm beating (or losing to) the strongest classical+single-model baseline changes what gets built, demonstrated by actually running that decision-relevant experiment. |
| U3 | purpose | [deep-review.md lines 36-37 (目的 U3)] No new knowledge is produced: C1 is definitional, C2 is open, C3 is a null, C4 is unbuilt, and C5 is a nonexistent benchmark. | standing | At least one contribution converted from plan to finding: the pre-registered Phase-2 agentic test executed with a significant, isolable surplus; or the cross-session benchmark actually built, validated (IAA, admission bands), and released. |
| U4 | purpose | [deep-review.md line 37 (目的 U4)] The W4 disentanglement north-star is refuted where it is interesting (paralinguistics: speaker ~chance, emotion null on the frozen content read-out) and trivial where it holds (a content encoder encodes content). | standing | Committed evidence that a frozen omni model's representations carry recoverable, non-trivial paralinguistic structure that training-free selection can exploit — e.g., speaker/emotion probes well above chance on a generative omni model's internal states (not the bi-encoder content read-out) plus a significant paired-CI training-free selection gain on that axis. |
| U5 | purpose | [deep-review.md lines 37-38 (目的 U5)] The only 'could-win' mechanism is conceded to be textbook PLDA multi-enrollment / CUSUM change detection; the agentic residual on top (curation/decay/trust-region bookkeeping) is pre-registered as an expected null. | standing | The isolating ablation coming back positive: arm (iii) (agentic curation/decay/trust-region/change-handling) showing a significant paired-CI surplus over arm (ii) (ECAPA+PLDA full multi-enrollment for identity; CUSUM/BOCPD over the SER-posterior stream for affect), attributing real gain to the agentic components specifically. |
| U6 | purpose | [deep-review.md line 39 (目的 U6)] The two-class taxonomy (label-derived vs model-dependent verifiable rewards) carries no predictive weight — it organizes nothing that changes an experiment or a design. | standing | The taxonomy making a risky, pre-registered, out-of-sample prediction that is then confirmed — e.g., predicting the sign/magnitude of training-free selection gain from measured reward spread and reward class on new tasks/datasets BEFORE running the selector, with the predictions surviving. |
| U7 | purpose | [deep-review.md lines 39-40 (目的 U7)] 'L4/agent-level' is never defined and is voided by the paper's own theorem; the paper's extensive candor is used as a shield rather than a fix. | standing | A precise, falsifiable definition of agent-level gain — an observable that provably separates agentic operation from single-model operation — together with a theorem or executed experiment showing the separating class is non-empty on a real task. |
| S1 | feasibility | [deep-review.md lines 43-46 (可行 S1 FATAL data)] The cross-session paralinguistic benchmark's precondition — same-speaker, cross-session/cross-channel, affect-varying audio — exists in NONE of the 28 frozen datasets (only CREMA-D: acted, single-session, 12 sentences, 91 speakers once each), and the set is FROZEN so it cannot be acquired; the plan's own SV-EER admission band rejects the only thing CREMA-D can produce. The headline benchmark cannot be built. | contingent (see note 1) | A committed inventory entry + validation artifact showing such a corpus in hand: N speakers each with ≥2 temporally separated sessions across ≥2 channels with verified affect variation, and a measured SV-EER inside the admission band. |
| S2 | feasibility | [deep-review.md lines 47-51 (可行 S2 FATAL tooling + provenance) and provenance pilot lines 59-71] No local generative operator existed anywhere in the committed repo (grep for llama_cpp/GGUF/vllm/.generate/logprob = 0 hits); the only model loader was the omni-embed bi-encoder and the only 'generation' called a remote DeepSeek API. The load-bearing Table-opB gains attributed to 'a single frozen generative omni policy, best-of-N' were actually produced by frozen bi-encoder cosine retrieval over static candidate cards — a provenance mis-attribution. | resolved (see note 2) | Already overturned (note 2). It would UN-resolve only if the artifact failed to reproduce from its committed command, or forensics showed the llama.cpp run did not actually drive the local GGUF model. |
| S3 | feasibility | [deep-review.md lines 52-53 (可行 S3 FATAL unbuilt)] The entire proposed stack is unwritten: ECAPA, PLDA, AS-Norm, pyannote, CUSUM, BOCPD, the SER head, the memory graph, the skill library, and the RL loop itself; every pre-registered falsifier pits nonexistent code against nonexistent code. | contingent (see note 3) | Committed, tested code for the baseline arms (ECAPA+PLDA multi-enrollment, CUSUM/BOCPD) and the agentic arm (memory graph, curation/decay, skill library, RL loop) plus at least one end-to-end run emitting its committed artifact. |
| S4 | feasibility | [deep-review.md line 54 (可行 S4-S7 bullet, clause 1)] Even if S1-S3 were solved, the best honest case for the agent-level paper is 'reused single-model numbers + a null' — the execution ceiling of the program, as designed, adds nothing beyond what the single-model results already show. | standing | An executed agent-level experiment whose result is NOT expressible as reused single-model numbers plus a null: a significant, pre-registered, isolable agentic surplus (arm iii over arm ii) on either the identity or the affect factor, with committed artifacts. |
| S5 | feasibility | [deep-review.md lines 54-57 (可行 S4-S7 bullet, clause 2 + closing compute sentence)] The required human SER annotation, spontaneous (non-acted) affect corpus, and full system stack constitute a multi-person, multi-month effort; local compute is a single 24 GB RTX 5090 Laptop GPU. | contingent (see note 4) | A committed budget/plan actually executed — annotated spontaneous corpus delivered with IAA-survival stats, the stack built (see S3), and the runs completed within the available or procured compute. |
| S6 | feasibility | [deep-review.md line 56 (可行 S4-S7 bullet, clause 3)] The '≥2 backbones' generality claim conflates a bi-encoder with a 30B-A3B MoE generative model — two incomparable operator classes — and the MoE's GGUF logprob interface was never verified to work at all. | resolved (see note 5) | Fully closed (including the residual) by a committed artifact extracting per-token logprobs from the GGUF 30B through llama.cpp and using them in reward-guided decoding; it would UN-resolve only if a revived paper re-asserted cross-backbone generality over incomparable operator classes. |
| S7 | feasibility | [deep-review.md lines 56-57 (可行 S4-S7 bullet, clause 4)] The novel (paralinguistic) axis has measured-zero reward spread on the frozen content read-out, so the proposed agent loop would be optimizing a flat reward — which by the paper's own flat_no_gain lemma yields exactly zero gain. | standing | A committed measurement of non-zero reward spread on the paralinguistic axis under a usable reward channel — e.g., a purpose-built speaker/SER encoder (ECAPA-TDNN, dedicated SER head) or a generative omni model's own outputs exposing a verifiable paralinguistic reward with measured spread, followed by a significant paired-CI training-free selection gain on that axis. |

**Resolution notes.**

1. **S1 (contingent — data, not theory):** resolved only by acquiring/collecting a spontaneous, same-speaker, multi-session, cross-channel, affect-varying corpus passing the pre-registered SV-EER admission band — requires an unlock/extension of the frozen `datasets.lock.json` manifest. Maps to ingredient (a) of 04-related-b.tex §3.4 and the corpus half of the paper's deferred-not-disproved precondition (10-discussion.tex ~119-121).
2. **S2 (resolved):** genuine local generative operator committed — reward-driven best-of-N on frozen Qwen3-Omni-30B-A3B (Q8_0 GGUF) via llama.cpp; W1 commits b7b4b0d / cd6aa92 / f9d111a; artifact `_repro/asr_bon_llamacpp_snr5.json` (verified on disk). Result: WER 0.118→0.077 at N=8, +0.042 [0.029, 0.056], 3 generation seeds pooled, n=144. The provenance mis-attribution is also fixed in the converged paper: the bi-encoder MInDS number is relabeled a zero-shot-classification/card ablation ("not best-of-N, not Gibbs tilting, not reward-driven RL"), the SLURP figure is dropped for lack of a committed artifact, and the two frozen models/operators are explicitly not conflated (10-discussion.tex ~6-14, 74-85).
3. **S3 (contingent — engineering, not theory):** resolved by committing runnable implementations of each named component with reproducer commands and committed artifacts, so the arm-(ii)/arm-(iii) falsifiers compare real code against real code.
4. **S5 (contingent — resources, not theory):** resolved by allocated person-months (annotation, corpus collection, engineering) and/or rented compute sufficient to run the pre-registered protocol end-to-end.
5. **S6 (resolved, with residual):** (i) the conflating "≥2 backbones" claim was CUT — the converged paper states the two results live on "different frozen models and different operators — a generative best-of-N selector versus a static embedding probe — and we are careful throughout not to conflate them" (10-discussion.tex ~6-14, ~87-98); (ii) the 30B GGUF is verifiably drivable as a local generative operator (commits above). **Residual:** per-token logprob extraction was not exercised (best-of-N used sampled candidates + external WER reward); any future reward-guided DECODING claim still needs that interface verified.

**The paper's precondition sentence** (10-discussion.tex, Future-work paragraph, ~118-125, exact wording):

> "A larger agent-level program (one frozen model routing and rewarding another across sessions) remains deferred, not disproved: it would require a cross-session, same-speaker corpus we do not have, and a genuinely new non-separable irreducibility theorem showing that decomposing a task into isolated contexts can add optimization headroom a single model lacks. Absent such a theorem, the spread lens is explicit that context isolation adds \emph{nothing} on a fixed reward --- no new non-constant reward component, no new spread, and by the identity below no new gain --- so that theorem is the precondition for any agent-level claim, and it is exactly what our present data do not supply."

**Four candidate mechanisms named in deep-review P1** (deep-review.md lines 12-13), none representable in the killed formalism: (1) non-separable reward → lane M1; (2) cross-block dependence → lane M2; (3) support expansion → lane M3; (4) sampling intractability → lane M4. Any overturning theorem must operate on changing q0, estimating R, or the sample complexity of realizing q\* (= the B0 axes).

**Three required ingredients** (04-related-b.tex §3.4, "Cross-Session Agent Memory and Skills"): (a) cross-session same-speaker corpus → S1, contingent; (b) locally-driven generative operator → S2, **now resolved** by the W1 llama.cpp best-of-N; (c) genuinely new non-separable irreducibility result → P1, standing. **Staleness note:** §3.4(b) still reads "we run only a frozen bi-encoder over candidate cards, never a local generative model," contradicting the converged paper's own C1 headline (genuine llama.cpp best-of-N on Qwen3-Omni-30B). Ingredient (b) is satisfied as of commits b7b4b0d/cd6aa92/f9d111a; the deferred program's genuinely missing ingredients reduce to (a) corpus [S1] and (c) theorem [P1]. The §3.4 sentence should eventually be updated for consistency.

**ID-mapping caveat:** deep-review.md compresses P5–P8 into one bullet (lines 27-30, five semicolon-separated clauses) and S4–S7 into one bullet (lines 54-57, five clauses). Mapping used here — P5 = circularity + no positivity floor (both attack the same positivity claim; Conjecture 1 falsified on the flagship); P6 = credit assignment assumed; P7 = β exogenous; P8 = rollout-deficit relabeled. S4 = best-honest-case thinness; S5 = multi-person/multi-month resources (the trailing "24 GB RTX 5090 Laptop GPU" sentence folded in as the compute constraint); S6 = ≥2-backbones conflation + unverified GGUF logprob interface; S7 = measured-zero spread on the novel axis. An alternative alignment shifting clauses by one is possible; the statements quote all clauses so no content is lost.

**Cross-check against the proposal-era ledger** (reviews/ledger.md): OSA2-RECOVERY-UNSUPPORTED (R1, reframed) and R3 AC-major-2 are ancestors of P1/U1 — the deep review re-opened them as unfixable-by-reframing, so they are STANDING here, not resolved. LEAN-QUANTITATIVE-WRAPPERS and OSA1-RANGE-NOT-VARIANCE (R1) are ancestors of P2/P3 (proposal-era "relabelled/scoped" deemed insufficient — standing). SPREAD-BETA-UNFALSIFIABLE (R1, deleted claims) is the ancestor of P7 (surviving β-dependence re-attacked — standing). F6/NM3 (emotion NULL, artifact-emitted) supply the "Conjecture 1 falsified on the flagship" evidence inside P5. REPRO-DISCREPANCY-AND-ARTIFACTS (R1, partial) and F9 (R2) are ancestors of S2's provenance prong, fully resolved only by the post-collapse relabeling + llama.cpp artifact. N3/NM4 (PLDA / CUSUM-BOCPD baseline upgrades) define the arm-(ii)-vs-arm-(iii) overturn tests cited in U5/S4. From the provenance pilot: the MInDS number itself was VINDICATED by a fresh committed re-run (policy 0.984, +0.126 [+0.077, +0.181], `_repro/minds14_toolintent_paired.json`) — only its mechanism label was wrong; the URO +0.130 low-margin rerank was remote DeepSeek (uro_qa_low_margin_rerank.py:343); the converged paper drops SLURP entirely (no committed artifact) and headlines MInDS only as a confounded zero-shot-classification ablation.

**Status summary:** 8 P standing, 7 U standing (all theory/purpose objections stand — the collapse conceded rather than answered them); S1 contingent (data), S2 resolved, S3 contingent (engineering), S4 standing, S5 contingent (resources), S6 resolved (per-token-logprob residual noted), S7 standing (committed empirical negative). **Net: any revival of the agent-level framing is gated on P1's non-separable irreducibility theorem (the paper's own precondition) plus S1's corpus; everything else is downstream.**

---

## 9. Appendix B — Outcome-symmetric decision-doc skeletons (pre-written before any lane runs)

### B.1 GO skeleton

```
# Decision: GO (or GO-minimal) — build the scoped omni agentic system
front-matter: recommended: GO|GO-minimal, owner_verdict: PENDING, freeze_anchor: <this file's commit hash>

1. B0 gate: the admissible delta axis/axes used, and the new-information items
   (each with its novelty-of-information citation per safeguard 4).
2. Surviving lane(s): lane id; T-part formal statement + stated assumptions +
   why it does not reduce to exp(a+b)=exp(a)exp(b); E-part numbers with paired
   95% CI and the null no-agency control; artifact paths + reproduce: lines.
3. G2: the named downstream decision and the pre-registered step-2 kill criteria.
4. G3: which >=2 ingredients are satisfied, with evidence pointers.
5. G4: person-week estimate (<=3), 24GB-GPU fit, licensing/consent check.
6. Ledger disposition: every P/U/S item classified ANSWERS or ROUTES-AROUND.
7. Steelman-NO-GO: rebutted point-by-point or conceded per point.
8. Build scope (full system, or GO-minimal selector-memory agent only).
```

Decision-Log entry it would produce:
`2026-MM-DD — GO(-minimal) agentic TFRL step 1: lane <id> survived (T: <statement>, E: <delta> [CI], control null); VoI decision = <name>; ingredients = <list>; build scoped to <scope>, <=3 pw; step-2 kill criteria = <list>; criteria frozen at <hash>; owner_ack: <...>.`

### B.2 NO-GO skeleton

```
# Decision: NO-GO — agent-level question closed
front-matter: recommended: NO-GO, owner_verdict: PENDING, freeze_anchor: <this file's commit hash>

1. Outcome per lane: B0 strikes; each kill threshold hit, with the measured
   number vs the pre-registered threshold; time-box status.
2. Ledger disposition: standing items unanswered or ROUTES-AROUND only;
   contingent items still contingent.
3. Strongest surviving GO argument (steelman-GO) and why it fails the frozen
   criteria (not why it is unpersuasive — which criterion it misses).
4. Pivot disposition: whether P-A / P-B / P-C / P-D triggered; if so, that is
   the successor project, recorded as a success.
5. Re-open conditions restated verbatim: r1 public cross-session same-speaker
   corpus; r2 peer-reviewed non-separable decomposition bound; r3 a lane kill
   overturned by new literature. Absent these, closed.
6. Citable closure sentence for the converged paper's "deferred, not disproved"
   future-work question.
```

Decision-Log entry it would produce:
`2026-MM-DD — NO-GO agentic TFRL step 1: lanes <ids> killed at <numbers vs thresholds>; inconclusive items defaulted to NO-GO per pre-registration <hash>; pivot <P-x|none> adopted; question closed absent r1-r3; owner_ack: <...>.`

---

## 10. 中文摘要

本文件在任何分析车道运行之前，冻结「训练无关 RL 方向是否合理、是否应构建全模态 agentic 系统」的全部判定标准；提交后的 commit hash 即冻结锚点，修改须经 owner 签署并记录 diff。

**零假设与 B0 增量门槛。** 2026-07-02 深度评审的 NO-GO 裁决为零假设；被否定的对象是「固定奖励下、通过上下文隔离增加价值上限」的 agent 级 TFRL（gain = β·KL ≤ spread²/8β，已证无懈可击，不得重审）。支持 GO 的论证只允许落在被否定形式体系无法表达的三条轴上：(a) 改变 q0（条件化/支持集扩张/记忆注入）；(b) 估计 R（C1 已实现-上限差距：oracle +0.042 [0.029,0.056]@N=8 显著，无标签 MBR 全 N 为零，仅实现约 10% 上限）；(c) 实现最优解的采样复杂度（上限不变、成本改变）。落在被否定框内的论证一律先验不可采。

**判定标准。** GO 须 G1–G4 全部满足：至少一条机制车道（M1–M5）的 T 部分（不退化为 exp(a+b)=exp(a)exp(b) 的形式命题）与 E 部分（预注册阈值、配对 bootstrap 95% CI 下界>0、无 agency 对照为零）同时过关；VoI>0（指名的下游决策 + 第二步 kill 标准）；论文三要素中至少两项落实；最小构建 ≤3 人周、单卡 24GB 可跑。GO-minimal 仅当 M5 过关且乱序记忆消融证明累积承重（乱序损失 ≥50% 增益）——只建 selector-memory agent。NO-GO：B0 失败、或全部车道触发 kill 且累积不承重、或 10 个工作日时限到期；**不确定即 NO-GO**，并记录同等详尽的决策日志与重启条件 r1–r3（公开跨会话同说话人语料 / 同行评审的非可分分解界 / 新文献推翻某车道 kill），否则问题关闭。预命名转向 P-A/P-B/P-C/P-D，选中任一视为成功。

**关键阈值。** M3 先行：Phase-0 零支持检查（N=32 无上下文采样，正确实体出现率 >1% 即杀）；Phase-1 四臂中 oracle 实体 WER 增益 ≥10 个绝对点且 CI 下界>0。M5 次行：胜过 MBR 且实现降幅 ≥0.015（约 35% 上限）；乱序记忆消融为决定性判据。M2 杀线：oracle 上限差 CI 上界 <+0.01 WER。M1 仅在 M4 留有残余时开启。

**防动机性推理。** 12 项结构性防护：零假设+时限、B0 门槛、控辩分离（辩方回答仅限 ANSWERS/ROUTES-AROUND）、新信息引用规则、hash 冻结、盲评新对手、常设 steelman-NO-GO、先杀后试、语言纪律、角色分离、测试集卫生（144 条池已为 dev-spent）、GO/NO-GO 决策文档骨架对称预写（见附录 B）。Owner 在任何发表及 WF-2 之前拥有最终闸门。
