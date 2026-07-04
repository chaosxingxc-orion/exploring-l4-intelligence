---
title: "Stage-1 Problem Definition — Ranked candidate problems for training-free RL on the semantic layer of frozen omni speech models"
date: 2026-07-04
stage: 1-problem-definition
status: "K2-RESOLVED 2026-07-04 — owner selected CP-1 + CP-3 + CP-8 + CP-4 for Stage-2"
source:
  - "wiki/2026-07-04-stage1-semantic-tfrl-survey.md (reviewed survey; S9 candidates CP-1..CP-8; §8.3 directional probe)"
  - "wiki/2026-07-04-sufficiency-yardstick-memo.md (ladder conditions a/b1/b2/c; failure routing)"
  - "wiki/2026-07-04-stage1-evidence-regrade.md (in-house number grades)"
  - "wiki/2026-07-03-omni-agentic-tfrl-go-no-go-decision.md (closure fence r1–r3; §10 closure sentence)"
role: "Distillation for the K2 owner discussion. RECOMMENDS a ranking; DECIDES nothing."
discipline: "Grade tags on every in-house number; the verbs confirms/establishes/demonstrates/significant are not used of in-house numbers; any candidate reducing to cross-session accumulation is flagged 'collides with closed question — owner amendment required' per the closure fence."
---

# Stage-1 Problem Definition — ranked candidate problems (semantic layer, frozen omni speech, training-free)

> **K2 verdict (owner, 2026-07-04).** The owner selected **CP-1 (quantify H_prompt − H_fix),
> CP-3 (measure ρ(ASR) properly), CP-8 (calibration + PMI on the SLU/MCQ surface), and CP-4
> (voice-agent pass@k + verifiable-reward best-of-N)** to advance to Stage 2 (solution validation).
> This is the full recommended top-3 plus the strongest reserve. Suggested sequencing on cost
> (a Stage-2 planning input, not a decision): CP-3 first (near-free re-scoring of on-disk C1 pools)
> → CP-1 SLU/SQA arms + CP-8 in parallel (cheap inference on schema-rich surfaces the probe weakly
> favors) → CP-4 last (needs an N-rollout agent harness). Per the methodology, Stage 2 opens with a
> fresh Research-Proposal-Template instance (pre-registered frozen criteria, powered n, full
> controls, adversarial review); the cross-session-accumulation variants stay behind the closure
> fence (owner amendment required). Stage-1 is closed.

> **What this document is.** The reviewed survey (`2026-07-04-stage1-semantic-tfrl-survey.md`) mapped the field and drafted **eight unranked** candidate research problems (CP-1..CP-8). This document does the one thing the survey deliberately withheld: it **ranks** them against a fixed rubric so the owner has a recommendation to react to at the Stage-1 closing discussion (K2). It recommends; the owner decides (survey §9.1; re-grade §3). Every in-house number carries its re-graded tag and is ledgered once in §4 (the single audit surface). The closure fence (r1–r3, NO-GO decision §9–§10) is applied throughout.

---

## 1. The answer to the owner's question, stated plainly

**The question** (owner, 2026-07-04, verbatim): *from the ICL perspective, is the optimization space of instruct-prompt-driven rollout on a frozen omni speech model sufficient for semantic tasks — and only if not, should an agentic system extend it?*

**The honest Stage-1 answer: sufficiency cannot be settled at Stage 1, because the central cell is unmeasured.**

The survey's sufficiency yardstick reduces "sufficiency" to three measurable fractions per task family (yardstick memo §2; survey §2.2):
- **(a) support** — `H_fix`, oracle-over-sampling headroom under one fixed instruction;
- **(b) reachability** — `H_prompt − H_fix`, the *prompt-space contribution* (nonnegative by construction, the direct operationalization of the owner's question), split internally into **b1** (format/schema movement) and **b2** (genuinely audio-grounded accuracy movement, certified by label-sensitivity + acoustic-grounding controls);
- **(c) realizability** — `ρ`, the fraction of oracle headroom a *label-free* selector can actually harvest.

Read against that yardstick, the record says three things and no more:

1. **The central cell — the *magnitude* of `H_prompt − H_fix` — is unmeasured everywhere for audio-in models.** It was doubly zero at survey time (survey §8.2): zero in-house (the C1 best-of-N pipeline ran **one fixed instruction** end-to-end, so the strongest in-house anchor measures `H_fix`, not `H_prompt`), and zero-magnitude in the published literature (five lanes searched for any APE/OPRO/GEPA-class instruction search, any max-over-K oracle, or any FormatSpread-style spread interval on an audio-in model, all returned empty; the automatic-prompt-optimization field's own survey covers no audio, and its multimodal expansion stops one modality short of audio). Existence is *not* zero — PromptingWhisper is a two-point positive showing `H_prompt − H_fix > 0` on a frozen speech model (10–45% relative from prompt manipulation) — but a two-point existence positive **bounds nothing**.

2. **The one in-house directional probe read uninformative-to-weakly-fix-favoring, on ASR only.** The single pre-authorized Stage-1 probe (matched-budget, 8 task-definition instructions × 4 samples vs 1 fixed instruction × 32 samples; n=50 LibriSpeech test-other; +5 dB SNR) measured the *matched-budget diversity contrast* **Δ_BM = −0.00137** (descriptive CI [−0.0126, +0.0095], spans zero, slightly favoring the fixed arm), with the MBR readout weakly reversing (+0.0045, CI spans zero) — the two readouts disagree in sign. Crucially, this is **Δ_BM, not `H_prompt − H_fix`**: the probe's equal-budget design cannot estimate the budget-unconstrained nested-pool quantity the owner's question is about. It is graded `directional-only`; it ranks nothing and kills nothing.

3. **Therefore sufficiency is answerable but unanswered.** For (a) support is real where measured (ASR) and unmeasured elsewhere; for (c) realization rides on external/verifiable/modality-grounded signals and collapses when the model must assess itself; for (b) there is **no theorem and, for audio-in models, no published measurement** — the only honest statement is that prompt-space headroom on frozen omni speech models is an empirical parameter no published work has estimated (survey §8.5).

**What the survey does with an unanswerable question — and what this document does next.** The survey converts the sufficiency question into a **failure-routing problem generator**: each yardstick condition's *failure* opens a different, well-posed research-problem family, and the agentic question re-enters **only** as the conditional consequence of a measured (a)-support failure — never as the starting point (survey §2.7; yardstick memo §5). From that generator it drafted eight candidate problems, unranked. This document ranks them (§3) so the owner can choose which measurement to pre-register at Stage 2 — with the definitions fixed, the empty cells named, and the directional probe on the table as one input among the rest, not as a finding.

**No overclaim.** Nothing here declares the space sufficient or insufficient. The recommendation is *which problem to measure first*, not *what the answer is*.

---

## 2. Reading key (grades and fence)

**Grade tags** (re-grade §2): `[settled (vector class)]` · `[scoped]` (real but class/condition-limited) · `[hypothesis-grade]` (directionally consistent, not established) · `[directional / directional-only]` (single small-n signal). Every in-house number below carries one, and none is described with *confirms / establishes / demonstrates / significant*.

**Closure fence** (NO-GO decision §9): a prior NO-GO closed the question "build a cross-session accumulating agentic system now"; it re-opens **only** on exogenous conditions **r1** (a public cross-session same-speaker speech corpus appears), **r2** (a peer-reviewed non-separable decomposition bound appears), or **r3** (a mechanism-lane kill is overturned by new literature) — all re-verified absent as of 2026-07-03. The binding rule: **any candidate that reduces to cross-session accumulating memory is labeled "collides with closed question — owner amendment required"**, flagged in place, never silently ranked. Per-session, within-episode state (context injected for one interaction and discarded) is on the *open* side of the fence.

---

## 3. Ranked candidate problems

### 3.0 The ranking rubric (fixed — stated before the ranking)

Candidates are scored on five criteria, in this order of weight:

- **(i) Problem-openness evidence strength** — do *others* name the problem, and is the yardstick cell genuinely unoccupied? Occupied-cell *erosions* (a two-point existence positive; a curation-only artifact; a cascade already in measured use) are counted honestly as reducing openness, not ignored.
- **(ii) Asset fit** — concrete mapping onto our on-disk base: the semantic-layer datasets on disk (the caller's asset frame counts ~14 of the 28 pinned in `docs/datasets.lock.json`; all 28 are present as directories), the mature llama.cpp Qwen3-Omni-30B C1 best-of-N pipeline (`_repro/asr_bon_llamacpp_snr5.json`, `probe_hprompt_vs_hfix.json` already on disk), the `common/` verifiable rewards (WER/ASR/exact-match), and the MInDS-14 +0.126 `[scoped]` result. **The §8.3 directional probe informs THIS criterion only** (see §3.9), never the ranking as a whole.
- **(iii) Ladder-condition value** — attacking the **crux (b2) reachability** or the documented **(c) realization gap** outranks re-measuring already-real (a) support. First-ever measurement of (a) in an unmeasured family is worth more than re-measuring settled ASR (a), but still ranks below a (b2)/(c) attack.
- **(iv) Stage-2 measurability** — does a *pre-registrable* yardstick quantity exist (a number the owner could freeze a threshold against)?
- **(v) Fence compliance** — training-free, and no r1–r3 collision. A candidate with a compliant single-session core plus a tempting cross-session variant is admissible **only** with the variant flagged.

Two constraints bind the rubric: the probe's directional read may inform **(ii) only**; and any cross-session-accumulation reduction is flagged, not ranked away.

### 3.1 Ranking at a glance

| Rank | CP | One-line | Rung | Why it lands here (rubric) | Fence |
|---|---|---|---|---|---|
| **1** | **CP-1** | Quantify `H_prompt − H_fix` on a frozen omni model (ASR + SLU + SQA) via APE/OPRO/GEPA-shaped scored search | (b), b1/b2-split | **(i) maximal** (the doubly-zero cell; verified-empty across 4 lanes); **(iii) attacks the crux**; **(iv) the pre-registrable estimand is defined** | offline search in-fence; **cross-session prompt-evolver variant collides — owner amendment required** |
| **2** | **CP-3** | Selector/utility anatomy on frozen omni pools — measure `ρ(ASR)` properly | (c) | **(ii) best asset fit** (C1 pools already on disk → cheapest genuine measurement); **(iii) attacks (c)**; **(iv) `ρ_fix` pre-registrable on frozen pools** | clean; tests the house `ρ_fix ≈ 0` prior `[hypothesis-grade]` rather than assuming it |
| **3** | **CP-8** | Calibration + PMI rescoring on the frozen audio-LLM choice surface (SLU/MCQ) | (b2)/(c) | **(ii) cheapest instruments** (inference-only, no prompt changes) on **schema-rich surfaces the probe weakly favors**; **(iv) "how much of the deficit is scoring-surface artifact" is pre-registrable** | clean |
| **4** | **CP-4** | Voice-agent pass@k + verifiable-reward best-of-N on τ-Voice-class envs | (a)+(c) | **(i) highest raw openness** (whole family UNMEASURED; reward pre-exists) + **(iv) very measurable**; docked on **(ii) heavier rollout build** and **(iii) headline rung is (a)** | single-session only; **τ²-class cross-session variant collides — owner amendment required** (L4:N5) |
| **5** | **CP-5** | Audio-blind b1/b2 certification harness for spoken-QA gains (MMStar-style) | (b)-split instrument | **(iii) enabling value** (certifies CP-1's SQA arm) on a **probe-favored family**; docked because it yields an **instrument, not a headroom number** | clean |
| **6** | **CP-2** | Multi-prompt candidate pools + label-free selection for ASR/ST | (b)×(c) joint | solid joint (b)×(c); docked on **(i)** (MBR machinery already speech-native — Whisper MBR is an occupied-cell erosion) and the **probe weakly disfavors the ASR family** | clean |
| **7** | **CP-6** | "Re-listen before you rewrite" — acoustically grounded self-verification (LookBack transfer) | (b2)/(c) | clean empty cell attacking (b2); docked on **(ii) heavier mechanism build** and a **strong documented self-correction failure-mode risk** | within-episode in-fence; **Reflexion-style cross-session variant collides — owner amendment required** |
| **8** | **CP-7** | Audio-native Set-of-Mark — acoustic anchors as in-context tokens | (b2) input-space | novel input-space lever; docked on **(ii) segmenter-dependent infra** and **(i)** occupied-cell erosion (the full cascade is the re-grounding scaffold already in measured use) | clean; segmenter-quality caveat |

**Recommended top-3: CP-1, CP-3, CP-8** — with **CP-4 as the strongest reserve** (its openness is the highest of all; it is held at #4 only by build weight and the rubric's discount on (a)-rung measurement). One honest tension the owner should weigh directly: if the §8.3 probe's *schema-rich* signal is given weight (it may inform **(ii)** only), the SLU/SQA arms of CP-1, plus CP-8 and CP-5, rise relative to the ASR-family candidates (CP-2, CP-3) — see §3.9.

---

### 3.2 CP-1 — Quantify `H_prompt − H_fix` on a frozen omni model (ASR + SLU + SQA) · **RANK 1 (recommended)**

- **Problem statement (ladder-placed).** Run a K-instruction *scored* search — APE/OPRO/GEPA-shaped — directly on a frozen omni backbone against WER (ASR), intent accuracy (SLU), and MCQ exact-match (SQA), reporting the max-over-K oracle beside the fixed-instruction baseline, with PromptEval/FormatSpread estimation under budget and the mandatory b1 controls (random-instruction arm at equal K; format-spread floor; ALICE-style format-vs-accuracy split). **Ladder: (b), split b1/b2 by construction.** This is the *direct operationalization of the owner's question* — the single empty cell that made the survey necessary (survey §1.3, §2.2, §8.2).
- **Who else works on it + closest occupied-cell note.** The quantification exists **only in the text-LLM domain** (OPRO +8% GSM8K / +50% BBH; GEPA outperforming GRPO weight training by 6% avg at ≤35× fewer rollouts). Multimodal Prompt Optimization reaches images/videos/molecules and **stops one modality short of audio**. Occupied-cell erosions to state honestly: **PromptingWhisper** is a two-point existence positive (`H_prompt − H_fix > 0`, unbounded) on frozen Whisper; on the SQA arm, **AudioMCQ**-style per-sample audio-contribution filtering exists but only for *training-data curation*, not eval-side certification. So the distance is **not methodological but simply that nobody has run a closed-loop scored search on an audio-in model** — verified-empty across four lanes plus an adversarial re-sweep.
- **Our angle's viability (concrete asset mapping).** Directly reuses the mature llama.cpp Qwen3-Omni-30B C1 best-of-N pipeline (`_repro/asr_bon_llamacpp_snr5.json`) as the sampler; `common/` supplies WER + exact-match rewards as the scoring metrics. Data on disk covers all three arms: **librispeech** (ASR); **minds14 / slurp / speech-massive** (SLU intent+slots); **mmau-mini / mmar / mmsu / big-bench-audio** (SQA MCQ). The MInDS-14 +0.126 `[scoped; b1/b2-unsplit]` result is the in-house precedent that a prompt/schema-surface gain exists on the intent surface — and CP-1's random-descriptor control at equal K is exactly the ablation that would split its b1 from b2.
- **Stage-1 quick-validation sketch (already run, in part).** The §8.3 directional probe is a first budget-matched touch of the ASR arm: Δ_BM = −0.00137 `[directional-only]`, uninformative-to-weakly-fix-favoring — which is a *reason to prioritize the SLU/SQA arms over the ASR arm*, not a reason to drop CP-1 (see §3.9). A cheap additional Stage-1 touch: run the same 8-instruction pool on a 50-item MInDS-14 slice and report max-over-K vs fixed on intent accuracy, with a random-instruction control — half a GPU-day, single-touch, `directional-only` on arrival.
- **What Stage-2 would pre-register.** The nested-pool `H_prompt(T,K,N) − H_fix(T,N)` per family (the estimand §2.2 defines), with thresholds δ_T, δ′_T frozen in advance; the b1-floor subtraction (FormatSpread), the random-instruction control at equal K (WaffleCLIP discipline), label-sensitivity + acoustic-grounding checks, and held-out-task generalization against CoOp-style dev-slice overfitting. **Fence:** a per-task offline search is in-fence; a **continuously accumulating cross-session prompt-evolver collides with the closed question — owner amendment required** (flagged, not proposed).

### 3.3 CP-3 — Selector/utility anatomy on frozen omni pools: measure `ρ(ASR)` properly · **RANK 2 (recommended)**

- **Problem statement (ladder-placed).** Over *identical stored candidate pools*, compare self-certainty, the frozen-LM pseudo-log-likelihood MBR utility swap (the lone in-fence speech positive, ~9% rel. WER), and overlap-MBR against the pool oracle, to measure how much oracle mass a deployable label-free selector actually harvests. **Ladder: (c).**
- **Who else works on it + closest occupied-cell note.** The frozen-LM MBR utility positive exists on **CTC pools, not omni-instruct pools**; self-certainty has **no speech instance**. The occupied-cell erosion is the Whisper-MBR positive (MBR beats beam search for Whisper ASR/ST) — but the *tension* between that positive and the in-house omni-pool null is itself unexplained and may be pool-geometry-driven, which is a research question, not a settled fact.
- **Our angle's viability (concrete asset mapping).** **The single strongest asset lever in the set: the C1 candidate pools already exist on disk** (`_repro/asr_bon_llamacpp_snr5.json`), so this is inference-only re-scoring — the cheapest genuine yardstick measurement available. `common/` WER reward + the `mbr-for-asr` ref repo supply the utility scaffolding; **librispeech** references ground it. Optionally extend to SLU/SQA pools generated by the CP-1 sampler.
- **Stage-1 quick-validation sketch (already run, in part).** The house prior is `ρ_fix(ASR) ≈ 0` `[hypothesis-grade]` — overlap-MBR gain +0.0037 [−0.0082, 0.0170] (null) and a memory-based selector at exactly 0 (inert-instrument null). CP-3 is the problem that **tests this prior rather than assuming it**; a re-score of the existing pools with self-certainty + frozen-LM utility is a <1 GPU-day Stage-1 touch, `directional-only` on arrival.
- **What Stage-2 would pre-register.** `ρ_fix` (and, once CP-1/CP-2 pools exist, `ρ_prompt`) with a frozen threshold ρ_min; a mandatory acoustic-grounding control (the perception-blind-verifier risk — every candidate selector scores *text*, so a fluent-but-unfaithful transcription is systematically preferred) and a cap on N near the reward-hacking optimum N*. **Fence:** clean; no cross-session component.

### 3.4 CP-8 — Calibration + PMI rescoring on the frozen audio-LLM choice surface (SLU/MCQ) · **RANK 3 (recommended)**

- **Problem statement (ladder-placed).** Apply contextual calibration, Batch Calibration, and domain-conditional PMI scoring to LALM MCQ/intent surfaces, against the documented distractor-rephrasing sensitivity (accuracy std up to 13.7%). The measurable question: *how much of the SLU/MCQ deficit is scoring-surface artifact rather than missing task knowledge?* **Ladder: (b2)/(c) on the choice surface** (bias-correction re-reads apparent missing-headroom as a de-biasable reachability fact).
- **Who else works on it + closest occupied-cell note.** The instruments are text-only (contextual/Batch calibration; PMI-DC), with PromptBoosting's K-prompt classification ensembling as the nearest origin-domain shape; **transfer to audio is verified-empty**. No occupied-cell erosion of note on the generative audio-LLM choice surface.
- **Our angle's viability (concrete asset mapping).** These are **the cheapest instruments in the paper — inference-only, label-free, no prompt changes**. Data on disk: **minds14 / slurp / speech-massive** (intent choice surface), **mmau-mini / mmar / mmsu** (MCQ choice surface). No new sampler needed beyond a single forward pass per option.
- **Stage-1 quick-validation sketch (cheap proposed).** Run contextual calibration on a 100-item MInDS-14 intent slice and report the calibrated-vs-raw accuracy delta plus the distractor-rephrasing variance before/after — half a GPU-day, single-touch, `directional-only`. This surface is the one the §8.3 probe's directional read weakly favors (schema-rich), so it doubles as a partial cross-check of that signal.
- **What Stage-2 would pre-register.** The fraction of the SLU/MCQ deficit attributable to scoring-surface bias (a pre-registrable proportion with a frozen threshold), separated from genuine task-knowledge absence; label-free prompt-selection gain filed under (c). **Fence:** clean.

### 3.5 CP-4 — Voice-agent pass@k + verifiable-reward best-of-N on τ-Voice-class environments · **RANK 4 (strongest reserve)**

- **Problem statement (ladder-placed).** Sample N full agent rollouts per task, report **pass@k (the family's first `H_fix` number)**, then select by the environment's DB-state reward — label-free inside the env by construction. **Ladder: (a) measurement + (c) realization.**
- **Who else works on it + closest occupied-cell note.** The family is **UNMEASURED**: τ-Voice reports **pass@1 only**; no pass@k / best-of-N / oracle exists on any voice-agent benchmark (N1/N2 verified-empty). The origin recipe (BoN over agent rollouts, ~+8pp GAIA, list-wise verification best) is concrete and idle. Unique property: **the reward pre-exists the selector research** (DB-state assertion transfers natively from τ-bench).
- **Our angle's viability (concrete asset mapping).** Data on disk: **tau2-bench** (the DB-state-reward env), **voicebench / voiceassistant-eval / eva-bench / big-bench-audio** (voice-agent surfaces); ref repos **TTRL / TPO / JitRL** for reward machinery. Honest cost note: this needs an **N-rollout agent harness**, which is heavier infra than the ASR best-of-N pipeline — the reason it is docked on **(ii)** despite top-tier **(i)**.
- **Stage-1 quick-validation sketch (cheap proposed).** A 20-task pass@4 count on tau2-bench with the DB-state reward as label-free selector, reported against the cost-controlled scaffold-ablation baseline (plain prompting + retries on the accuracy-vs-cost Pareto frontier) — a genuinely cheap first `H_fix` number for the family, `directional-only`.
- **What Stage-2 would pre-register.** pass@k as `H_fix`, the DB-state-reward realized fraction as `ρ`, and — mandatory — the Kapoor-style cost-controlled scaffold-vs-plain-prompting Pareto ablation (simple retries match fancier scaffolds at up to ~50× lower cost). **Fence:** single-session only; a **τ²-class cross-session accumulating variant collides with the closed question — owner amendment required** (L4:N5).

### 3.6 CP-5 — An audio-blind b1/b2 certification harness for spoken-QA conditioning gains · **RANK 5**

- **Problem statement (ladder-placed).** Build per-sample audio-indispensability and leakage metrics (MMStar-style) on top of MMAU-Pro's benchmark-level shortcut controls, and apply the harness to any training-free conditioning result before crediting its gain as b2. **Ladder: (b)-split instrumentation rather than a method.**
- **Who else works on it + closest occupied-cell note.** MMAU-Pro supplies benchmark-level shortcut controls (text-only models drop to 16–30%); MMStar supplies the per-sample idea in the VLM domain; **AudioMCQ**-style per-sample filtering exists only for **training-data curation** — the **eval-side per-sample certification harness is verified-absent**. This family uniquely offers the ready-made splitter.
- **Our angle's viability (concrete asset mapping).** Data on disk: **mmau-mini / mmar / mmsu / air-bench / audiomc**. This is instrumentation (metric + filter), not a new sampler.
- **Stage-1 quick-validation sketch (cheap proposed).** Compute an audio-ablation drop per sample on a 100-item MMAU-mini slice and report the fraction of items whose "correct" answer survives audio removal (the leakage rate) — cheap, `directional-only`.
- **What Stage-2 would pre-register.** The harness itself as the deliverable (leakage + multi-modal-gain metrics), then its use as the b2 gate for CP-1's SQA arm. Docked from the top-3 because it produces an **instrument, not a headroom answer** — its highest value is as CP-1's enabler. **Fence:** clean.

### 3.7 CP-2 — Multi-prompt candidate pools for ASR/ST with label-free selection · **RANK 6**

- **Problem statement (ladder-placed).** Transfer multi-prompt MBR to frozen omni ASR/ST: sample across K instructions × N rollouts, select label-free, and report **both** the pool-oracle movement (does the K-dimension enrich support?) **and** the realized fraction. **Ladder: (b)×(c) joint** — it measures the K×N cell and condition (c) together.
- **Who else works on it + closest occupied-cell note.** The text-domain operationalization (multi-prompt MBR) is untransferred; **Whisper MBR** is the single-prompt speech baseline — and its being speech-native is an **occupied-cell erosion for the selection half** (the (c) machinery is not novel here; only the K-dimension is).
- **Our angle's viability (concrete asset mapping).** **librispeech** (ASR), **covost2 / fleurs-r** (ST); the `mbr-for-asr` ref repo + `common/` WER reward; the C1 sampler extended to K instructions. Honest note: this is the ASR/ST family where the §8.3 probe's directional read is weakly fix-favoring, which is why CP-2 sits below the schema-rich candidates despite a clean fence and a valuable joint measurement.
- **Stage-1 quick-validation sketch (already run, in part).** The §8.3 probe is effectively a K=8 single-touch of the joint quantity on ASR (Δ_BM = −0.00137, MBR +0.0045, both CIs span zero) — `directional-only`.
- **What Stage-2 would pre-register.** The K×N pool-oracle movement (`H_prompt` on the pool side) jointly with `ρ_prompt` for ASR and ST. **Fence:** clean.

### 3.8 CP-6 — "Re-listen before you rewrite": acoustically grounded self-verification · **RANK 7**

- **Problem statement (ladder-placed).** Transfer LookBack: before critiquing/correcting its own transcript or answer, the model **re-attends the audio** and verifies each claim against it, under a **do-no-harm gate** (accept a correction only when an external verifiable score does not worsen) and a matched-budget consensus baseline. **Ladder: (b2)/(c)** — it directly operationalizes b2 acoustic-grounding certification.
- **Who else works on it + closest occupied-cell note.** LookBack is the one VLM self-correction mechanism with a positive training-free delta (+13.5%) against the perception-critique failure mode. The named empty cell is exact: **no published frozen speech/omni model re-listens to correct itself** (the entire speech correction column delegates to text LLMs that never hear the signal); verification-first ASR pipelines are the nearest working shape.
- **Our angle's viability (concrete asset mapping).** **librispeech** (ASR self-correction); `common/` WER as the do-no-harm external score. Honest cost/risk note: heavier mechanism build (a re-attention loop + gate), and a **strong documented failure-mode risk** — intrinsic self-correction degrades reasoning accuracy, and modality-blind critics keep acoustic errors while fluently rewriting the text (VISCO's critique-bottleneck) — which is why it sits below the cheaper (c)/instrument candidates.
- **Stage-1 quick-validation sketch (cheap proposed).** On a 50-utterance slice, run one re-listen-then-revise pass under the do-no-harm gate and report the WER delta vs a matched-budget self-consistency baseline — `directional-only`; expect the gate to be load-bearing.
- **What Stage-2 would pre-register.** The gated re-listen WER delta vs a matched-budget consensus baseline, with the do-no-harm gate as a frozen acceptance rule. **Fence:** within-episode reflection is in-fence; a **Reflexion-style cross-session accumulating variant collides with the closed question — owner amendment required**.

### 3.9 CP-7 — An audio-native Set-of-Mark: acoustic anchors as in-context tokens · **RANK 8**

- **Problem statement (ladder-placed).** Surface diarization/VAD segment marks, spelled-entity spans, and timestamp scaffolds into the prompt of a frozen omni model, for long-audio SQA and voice-agent argument-value fidelity — the audio analog of the input-space intervention that let zero-shot GPT-4V beat fine-tuned grounding SOTA. **Ladder: (b2) input-space conditioning.**
- **Who else works on it + closest occupied-cell note.** Set-of-Mark is a VLM result; the audio cell (N4) is verified-empty. Occupied-cell erosion: the **full cascade is the only re-grounding scaffold in measured use** (it pays ~10s latency for its gains), and audio's weaker universal segmenters bound how far the analog can go (X3 caveat).
- **Our angle's viability (concrete asset mapping).** **big-bench-audio / spoken-squad / heysquad** (long-audio SQA), **tau2-bench** (argument-value fidelity). Honest cost note: requires diarization/VAD/timestamp infra whose quality bounds the result — the reason it ranks last on **(ii)**.
- **Stage-1 quick-validation sketch (cheap proposed).** On a 30-item long-audio SQA slice, prepend VAD/timestamp marks and report the exact-match delta vs no-marks — `directional-only`, with a segmenter-quality caveat attached.
- **What Stage-2 would pre-register.** The marked-vs-unmarked accuracy delta on long-audio SQA and argument-value fidelity, reported against segmenter quality as a covariate. **Fence:** clean; segmenter-quality caveat.

### 3.10 The probe as a criterion-(ii) signal (not a ranking input)

Per the rubric, the §8.3 directional probe informs **asset fit only**. Its honest content, carried grade-tagged: at a matched budget on **ASR**, spreading rollouts across 8 instructions did **not** beat depth under one instruction (Δ_BM = −0.00137, MBR readout +0.0045, both CIs spanning zero, readouts sign-disagreeing) `[directional-only | n=50 | single-touch | not significance-bearing]`. Two disciplined uses follow:

1. **It weakly argues the prompt-space crux is more promising on schema-rich tasks (SLU/SQA) than on ASR** — a *recommendation signal* for the owner, not a decision, and explicitly **not** a measurement of `H_prompt − H_fix` (it measured Δ_BM at a tiny budget, which the equal-budget design cannot convert to the nested-pool quantity). If the owner gives this signal weight, it shades asset-fit toward the **SLU/SQA arms of CP-1**, toward **CP-8** (SLU/MCQ), and toward **CP-5** (SQA), and away from the ASR-family CP-2 / CP-3 — as a criterion-(ii) refinement inside the ranking, never a reordering of the rubric itself.
2. **It does not lower CP-1's rank.** CP-1's #1 standing rests on criteria (i)/(iii)/(iv) — openness, crux-attack, and a defined pre-registrable estimand — none of which the probe touches. The probe's read is a reason to *sequence CP-1's arms* (SLU/SQA before ASR), not to demote the problem.

Nothing in this section is a finding. The probe decides nothing (survey §8.3, §8.5).

---

## 4. Numbers ledger (the single audit surface)

Reproduced from the survey's Appendix A — every in-house number, its grade, and its source. No number appears above without its grade tag; none is described with *confirms / establishes / demonstrates / significant*.

| # | Value | What it is | Cited above at | Grade tag | Artifact / doc source |
|---|---|---|---|---|---|
| 1 | WER 0.1183 | greedy decode, frozen Qwen3-Omni-30B, LibriSpeech test-other, +5 dB SNR (mild additive noise), one fixed instruction | §1, §3.2 | [scoped] | C1 best-of-N pipeline artifact (`_repro`, multi-seed best-of-N); re-grade §2 |
| 2 | WER 0.0765 | oracle-over-8-samples on the same pool | §1, §3.2 | [scoped] | same as row 1 |
| 3 | ΔWER +0.0418 [0.0289, 0.0564] | `H_fix` oracle headroom @ N=8 / +5 dB SNR (rows 1−2) | §1, §3.2, §3.3 | [scoped — one instruction, one model, one condition] | same as row 1; measures `H_fix`, not `H_prompt` (single fixed instruction) |
| 4 | +0.126 [0.077, 0.181] | MInDS-14 intent gain, frozen bi-encoder cosine selection over prompt/schema surface (paired CI) | §3.0, §3.2, §3.4 | [scoped; b1/b2-unsplit pending random-descriptor ablation] | forensic re-run per re-grade §2 |
| 5 | +0.0037 [−0.0082, 0.0170] | overlap-utility MBR gain at N=8 over the C1 pools (null) | §3.3 | [hypothesis-grade] | C1 selector runs, two evaluation slices; re-grade §2 |
| 6 | ~0–10% | fraction of the oracle headroom (row 3) realized by MBR | §3.3 | [hypothesis-grade] | derived from rows 3 + 5; re-grade §2 |
| 7 | exactly 0 | memory-based selector gain (inert-instrument null, frozen default) | §3.3 | [hypothesis-grade] | re-grade §2 (M5 relabeling) |
| 8 | ρ_fix(ASR) ≈ 0 | house prior for the ASR realization fraction (of `H_fix`) | §3.3 | [hypothesis-grade] | derived from rows 5–7; re-grade §2 |
| 9 | 0.0530 | probe fixed-arm oracle headroom (1 fixed instruction × 32 samples), n=50 fresh LibriSpeech test-other, +5 dB SNR | §1, §3.10 | [directional-only \| n=50 \| single-touch \| not significance-bearing] | `_repro/probe_hprompt_vs_hfix.json`; mini-prereg at bae2184 |
| 10 | 0.0516 | probe prompt-arm oracle headroom (8 task-definition instructions × 4 samples), same items/budget | §1, §3.10 | [directional-only \| n=50 \| single-touch \| not significance-bearing] | same as row 9 |
| 11 | Δ_BM = −0.00137, CI [−0.0126, +0.0095] | probe matched-budget diversity contrast (prompt-arm − fixed-arm oracle headroom; **NOT** the budget-unconstrained `H_prompt − H_fix`; spans zero, slightly favors the fixed arm) | §1, §3.2, §3.7, §3.10 | [directional-only \| n=50 \| single-touch \| not significance-bearing] | same as row 9 |
| 12 | 33/50 | utterances on which the fixed instruction produced the pool-best candidate | §1, §3.10 | [directional-only \| n=50 \| single-touch \| not significance-bearing] | same as row 9 |
| 13 | prompt-arm MBR 0.0884; fix-arm MBR 0.0929; delta +0.0045 [CI spans zero] | probe MBR readout, prompt-arm vs fix-arm (weak reversal) | §1, §3.7, §3.10 | [directional-only \| n=50 \| single-touch \| not significance-bearing] | same as row 9 |

**Qualitative in-house standings cited without numbers** (governed by the same re-grade / NO-GO records): the vector-class paralinguistic premise (speaker never written to the pooled vector; emotion present-but-unread) `[settled (vector class)]`; and the r1–r3 closure-fence standing `[settled (as of 2026-07-03)]`.

---

## 5. Explicit non-decisions (what this document deliberately does NOT decide)

1. **Problem selection is the owner's at K2.** This document *ranks and recommends* (top-3: CP-1, CP-3, CP-8; reserve: CP-4). It does **not** select. The ordering of effort across CP-1..CP-8 is handed to the owner discussion with the definitions fixed, the empty cells named, and the directional probe on the table as one input among the rest (survey §9.1, §9.3).
2. **Whether to proceed to Stage 2 at all is an owner call.** Per the survey's S9 revision and the re-grade (§3), Stage-2 justification and any commitment of resources are owner decisions. Nothing here authorizes a Stage-2 pre-registration; each candidate's "what Stage-2 would pre-register" is a *sketch for the owner to accept, amend, or reject*.
3. **The sufficiency verdict itself is not issued.** No cell of the yardstick is scored "sufficient" or "insufficient." Sufficiency is answerable-but-unanswered (§1); the recommendation is *which measurement to run first*, not *what the answer is*.
4. **The directional probe decides nothing.** Its ASR read informs asset-fit (criterion ii) and sequences CP-1's arms; it does not rank, kill, or measure `H_prompt − H_fix`.
5. **The closed agentic question stays closed.** This document does **not** re-open the NO-GO. Any candidate variant that reduces to cross-session accumulation (CP-1's prompt-evolver, CP-4's τ²-class accumulation, CP-6's Reflexion-style memory) is flagged **"collides with closed question — owner amendment required"** — re-opening remains gated on exogenous r1–r3, none met as of 2026-07-03. Amending the re-open clause to admit in-house successor evidence, if the owner wishes it, is an owner-level amendment, not a synthesis action (NO-GO decision §9 record note C12).

---

## 6. 中文摘要

**Owner 的问题**（2026-07-04）：从 ICL 视角，冻结全模态语音模型上"指令提示驱动 rollout"的优化空间，对语义任务（ASR/ST、SLU、口语问答、语音智能体）是否**充分**；仅当不充分时，才考虑用智能体系统扩展它？

**Stage-1 的诚实回答：充分性无法在 Stage-1 判定，因为核心单元格无人测量。** 充分性标尺把问题拆成三个可测分数：**(a) 支持**（`H_fix`，单固定指令下的 oracle 上限）、**(b) 可达性**（`H_prompt − H_fix`，即 prompt 空间贡献，构造上非负，是 owner 问题的直接操作化；内部再拆 b1 格式/b2 真实精度）、**(c) 可实现性**（`ρ`，无标签选择器能兑现的上限比例）。据此：

1. **核心单元格 `H_prompt − H_fix` 的量级对任何音频输入模型都无人测量**——in-house 双零（C1 管线全程一条固定指令，最强锚点 +0.0418 `[scoped]` 只测到 `H_fix`）、文献零量级（五个车道搜索 APE/OPRO/GEPA 类指令搜索、max-over-K oracle、FormatSpread 区间，全空；MPO 止步于音频之前）。存在性非零（PromptingWhisper 两点正例），但两点存在性**不界定任何量级**。
2. **唯一的 in-house 定向探针（等预算、仅 ASR）读数为"无信息至弱偏向固定臂"**：Δ_BM = −0.00137（CI 跨零），MBR 读数 +0.0045（符号相反、CI 跨零）。这测的是**等预算多样性对比 Δ_BM，不是 `H_prompt − H_fix`**，`[directional-only]`，不排序、不击杀任何东西。
3. **因此充分性可答但未答。** 于是本文把问题转成**排序的候选问题**（survey 只列不排，本文排）。

**排序规则（固定，五条）**：(i) 问题开放性证据强度（他人命名、单元格未占用，占用格侵蚀如实计入）；(ii) 资产契合（磁盘上语义相关数据集、成熟的 llama.cpp Qwen3-Omni C1 管线、`common/` 可验证奖励、MInDS +0.126 `[scoped]`；**探针只影响此条**）；(iii) 阶梯价值（攻 b2 可达性或 (c) 实现缺口 > 重测已确证的 (a)）；(iv) Stage-2 可测性（存在可预注册量）；(v) 围栏合规（训练无关、不碰 r1–r3）。

**推荐前三：CP-1、CP-3、CP-8**（CP-4 为最强候补）。
- **CP-1（排 1）**：直接量化 `H_prompt − H_fix`（ASR+SLU+SQA），开放性最强、直攻 crux、估计量已定义；离线搜索在围栏内，**跨会话 prompt 进化器变体碰撞关闭问题——需 owner 修正案**。
- **CP-3（排 2）**：在冻结 omni 池上做选择器解剖、测 `ρ(ASR)`；**资产契合最佳**（C1 池已在磁盘上，最便宜的真实测量），攻 (c)，围栏干净。
- **CP-8（排 3）**：在冻结音频 LLM 选择面上做校准 + PMI（SLU/MCQ）；纸中最便宜的仪器，落在探针弱偏向的 schema 丰富面上。
- **CP-4（候补）**：语音智能体 pass@k + 可验证奖励 best-of-N；原始开放性最高、奖励天然存在，但构建更重、(a) 档次被规则折价、**τ² 跨会话变体碰撞——需 owner 修正案**。

**明确的非决策**：问题选择归 owner（K2）；是否进入 Stage-2 归 owner；不发充分性裁决；探针不决策；关闭的智能体问题维持关闭（碰撞项一律标注、r1–r3 未满足）。**纪律**：每个 in-house 数字带分级标签；不对 in-house 数字使用 confirms/establishes/demonstrates/significant；一切碰撞跨会话累积的候选均标注"碰撞关闭问题——需 owner 修正案"。**本文只推荐，不决策。**
