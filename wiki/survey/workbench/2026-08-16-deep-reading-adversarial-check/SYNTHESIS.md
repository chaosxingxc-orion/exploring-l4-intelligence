# Synthesis — elevated-dimension adversarial check (research-lead verdict)

Date 2026-08-16 night. Inputs: four deep-reading clusters (RECOVER / metrics-memory /
biasing-supply / copying-verification) + three adversaries (topic soundness / literature
positioning / methodology), all in this directory with per-fetch logs. This synthesis is the
operative verdict; the seven reports are the evidence.

## 1. The three findings that change the study

1. **The VOID phenomenon is scooped.** "Listen, Do Not Copy" (arXiv 2607.21943, 2026-07-24)
   reports 94.2% blind-copy on Qwen3-Omni-30B under wrong context with a silence control;
   2607.13477 shows frozen Qwen3-Omni judges follow wrong references; 2602.11488 runs a
   prompt-framing factorial on audio-text conflict. What remains OURS: (i) the verify-vs-bias
   framing contrast at fixed reference correctness (unrun anywhere), (ii) byte-identical
   parroting as an open-vocabulary copy metric, (iii) the pre-localized routing aperture on real
   long-form speech, and above all (iv) **the allocation bound** — guard-chain perfection worth
   ≤0.28pp entity-WER at the measured aperture vs −12pp for oracle supply, RIR 0/54 — which no
   prior computes. The bound is the headline; the copy parity is its explanation. A standalone
   negative-result paper is dead; the bound lives inside the supply/routing paper.
2. **HER/RIR is a naming collision.** NVIDIA Voice Memory (2607.26410, 2026-07-29, open source)
   uses the same acronyms with near-identical semantics. Our earlier lineage pin was also
   factually wrong (Edit Rate / Improve@Edit / Worsen@Edit come from arXiv 2606.13464, not the
   2508.07285 survey). Action: rename — keep only the denominator change (delivered-correct
   opportunities vs their N-best oracle gap) as a stated necessity, e.g. **DOR
   (Delivered-Opportunity Recovery)**; cite Voice Memory in the metrics section.
3. **The research object as worded has collapsed; the study has not.** "Deployment-legal targeted
   supply on a frozen omni" is ConEC (2024) + Siskos (2025) territory with a consumer swap. The
   defensible reformulated object is **the consumption law**:

   > What determines whether a frozen multimodal core USES, COPIES, or IGNORES supplied
   > evidence — as a function of supply form, dose, provenance tier, and routing aperture — and
   > why does the dose law invert between trained consumers (dose-robust to 15× oracle tokens)
   > and frozen prompt-readers (degrading past 50–100 entries) on the same corpus?

   Under this object: the earnings block becomes the frozen arm of a consumer contrast on
   ConEC's own corpus; legality becomes a measured **price-of-legality ladder** (zero /
   self-supplied glossary from own pass-1 / shipped metadata / pinned documents / gold) with a
   coverage→gain transfer function nobody has published; and the VOID becomes a mechanism claim
   about supply form ("whole-reference supply is a copy trap under which verification is
   unmeasurable" — RECOVER's constrained-vocabulary Tool-2/3 design is the corroborating prior).

## 2. Gap statement — collapsed from seven conjuncts to two plus one number

Dead or table stakes: training-free; audio-grounded verification (carry as measured negative
only); harmful-edit accounting (hygiene, no novelty); task conversion (known implication —
survives only as *controller transfer*); legal provenance (survives only as the measured ladder).
Live: **(1) speech-conditioned routing in the training-free × output-only × no-second-LLM cell**
(occupied when trained: CLAR, IBM 2604.12398, BR-ASR, GLCLAP; occupied white-box: streaming
CTC-WS; occupied text-conditioned: Siskos/DeRAGEC/RECOVER — the three-way intersection is empty
but must be DEMONSTRATED against a matched text-conditioned selector and a silence control);
**(2) single-core / no-second-answering-LLM** (every close prior calls a second LLM — RECOVER
GPT-4o, DeRAGEC Llama-70B, Voice Memory a separate corrector, EChO DeepSeek-V3 — promote this
conjunct). Plus the number: the aperture/allocation bound. The `logit_bias` problem must be
addressed before any registration: llama-server exposes logit_bias + n_probs, so "API-only" must
either be priced (a logit-bias upper-reference arm — also supplies the prompt-vs-logit table
LOGIC asserted without measuring) or honestly re-scoped to "prompt-level supply, per commercial
omni endpoints".

## 3. Operative plan revisions (adopted now)

1. **N1 is replaced**: N1a = **legal-coverage ledger** (offline, zero GPU, all 44 calls, per
   entity type in ConEC's schema, committed BEFORE any block; predicted effect = coverage ×
   measured conversion, with a do-not-fly rule vs the MDE). N1b = routing metrics restated
   against LEGALLY-reachable mass with precision and budget-concentration floors; any flag
   tuned on oracle anchors is ceiling-tier by the study's own doctrine and must be re-tuned on a
   disjoint surface before any deployment-tier use. The self-supplied glossary rung (the study's
   own L3/L4, designed 2026-08-10, never run) enters the ladder.
2. **Any future earnings block follows the Adversary-3 minimal design**: four arms (zero re-flown
   in-block / legal roster / length-stratified deranged roster / oracle ceiling) + earnings22
   dev-10 companion pair; frozen ten declared a TUNING SET (descriptive only; primary inference
   on the 34-stratum); entity-WER single primary with call×type cluster-robust bootstrap; macro
   as non-inferiority guardrail; format-normalized mandatory; fraction-of-oracle-headroom as the
   effect size; false-alarm/copy ledger on every arm; silence + audio-mismatch spot controls;
   per-sample exposure counters and a machine-readable consumed field. (The block itself remains
   shelved to Stage-3 per the owner's breadth-first ruling; this is its registered shape if ever
   promoted.)
3. **Probe network inherits the controls**: every probe (Audio2Tool, ContextASR, SLURP) carries
   copy-rate as a first-class metric, a distractor/deranged supply arm, and where audio-reading
   is claimed, a silence/mismatch control. The consumption-law framing unifies the probes: each
   measures use/copy/ignore under a different supply form and task coupling.
4. **DEMO lane demoted to a gated screen.** In-Context Fixation (2605.08295) predicts reject-case
   demonstrations SUPPLY the error vocabulary rather than immunize (effect strengthens with
   scale; recency dominates ordering); FSA-GRPO had to train a reward bound against over-copying;
   TICL publishes the positive-demonstration mechanism with no copy control. Also the
   construction split no longer exists inside earnings21 (kb34 was folded into the evaluation
   set by the intersection ruling) — only leave-one-call-out or earnings22-based construction
   satisfies owner condition 1. Before any WER block: a ≤16-request **copy-contamination screen**
   with a pre-declared kill threshold, ordering as a registered axis, legality tier registered at
   the screen.
5. **Metrics repair**: rename per §1.2; adopt prior vocabulary (perception bypass / blind-copy,
   reference-follow rate, TDR) instead of minting names; cite IBM 2604.12398, CLAR 2603.25460,
   Contextual Earnings-22 2604.07354 (GPT-5-NER-over-gold = the named illegal rung on our sister
   corpus; re-check its release before any registration), streaming CTC-WS 2605.18222.
6. **Exposure-accounting hardening** (engineering queue): per-sample prior-read counters; a
   machine-readable consumed field; a hypotheses-read-per-split multiplicity ledger; the standing
   rule that frozen-ten p-values are descriptive.

## 4. Honest bottom line

The study keeps three assets no prior matches: per-stage causal instrumentation above the
field's own standard, an enforced machine-carried legality construct that lands on a
four-for-four provenance hole in the closest priors (RECOVER unstated on Earnings-21; ConEC
unlicensed; Voice Memory gold-in-loop; DeRAGEC gold-derived rationales), and token-level
copy/dose instrumentation on the one consumer class nobody measures. Viability is conditional on
the routing/coverage question producing a positive selector OR a clean boundary law ("the signal
lives in the internals; here is what the API surface forfeits" — with three trained systems
proving the signal exists). Both outcomes are informative; neither is prompt-craft. The failure
mode to guard: running any block without pre-declared floors, so weak numbers get reinterpreted
post hoc.
