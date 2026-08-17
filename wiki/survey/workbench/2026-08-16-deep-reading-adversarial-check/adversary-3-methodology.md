# Adversary 3 — METHODOLOGY. Internal-design attack on the N1 / N2 / DEMO plan

Author: adversarial reviewer 3 (methodology lane), 2026-08-16 night / 2026-08-17 UTC.
Scope: internal validity of the surviving SAEA plan only. I take the four cluster digests
(A RECOVER, B metrics/memory, C biasing/supply, D copying/verification) as given and do not
re-litigate the prior-art positioning. Everything below is about whether the planned blocks
can support the inferences the plan wants to draw from them.

Repos were read read-only. Nothing under `studies/` was written or modified; no git command was
run. This file is the only file I created.

---

## 1. Fetch log

Local reads (read-only; recorded for provenance, not web fetches):

| # | time (local 2026-08-16) | source | one-line result |
|---|---|---|---|
| L1 | 21:12 | `studies/.../docs/p2-branch-rule-pins.md` | Seven pre-read pins; Pin 7 concedes n=6 cannot support significance; margins are implementer-chosen. |
| L2 | 21:12 | `studies/.../docs/readiness/2026-08-15-rectification-plan.md` | Phases 0–4 + MUST-NOT-FLY lines; the "oracle-flag-routing recall gate FIRST" clause lives in PHASE 3 (D3 ConEC full chain), not in a static-roster block. |
| L3 | 21:13 | `studies/.../docs/readiness/2026-08-16-p2-rladder-verdict.md` | VOID on r1wrong=7 copies; RIR 0/54; acceptance collapse 0–3 splices/arm; "screens are shape filters, not effect estimates". |
| L4 | 21:14 | `studies/.../docs/readiness/2026-08-15-n10-block-verdict.md` | zero 12.38 / matched 12.39 / names 10.88 (p=.027, 9/10) / metadata 12.09 (p=.19, 7/10); entity 5632 / 5873 / 6631 / 5749 of 8284. |
| L5 | 21:14 | `studies/.../docs/readiness/2026-08-15-legality-doctrine.md` | Dimension 1 bans gold-guided SELECTION; either-field rule (`span_source` / `reference_source`) makes an arm ceiling-tier. |
| L6 | 21:14 | `studies/.../docs/readiness/2026-08-14-deployment-legal-label-source.md` | Metadata roster = company + non-placeholder speakers, 1–16 terms/call, typos preserved. |
| L7 | 21:15 | `studies/.../docs/checks/.../2026-08-16-r0bias-guard-forensics/report.md` | 49/53 byte-identical parroting; 30 FALSE / 15 CORRECT rejections; 21 genuine recoveries; −0.039pp macro / −0.28pp entity counterfactual; **55 windows / 23 reachable entity mentions**; ceiling-tier oracle roster. |
| L8 | 21:16 | `studies/.../docs/readiness/2026-08-14-stage2-candidate-freeze.md` | kb-construction 34 frozen (67e32336/8572f5d6); cross-call KB route closed by the P0.1 reachability partition. |
| L9 | 21:17 | `studies/.../docs/readiness/2026-08-14-p1-ceiling-verdict.md` | Flag misses entities 17/17; **arm A was a REUSED zero from another block**; number-format axis swings >100 digit tokens and is instruction-controlled. |
| L10 | 21:17 | `studies/.../docs/receipts/splits.json` | discovery = earnings21 44 (fcc1b0bc); dev = earnings22 10 (89b178d6); confirmatory = earnings22 115 (18f8e1c9). |
| L11 | 21:18 | `studies/.../docs/exposure-ledger.md` (grep on `744c4b2e`, `67e32336`) | ≥20 arm reads on the frozen ten under one split-identity hash; `consumed` column stays "no" while results are appended as prose; kb34 read exactly once (np16 wide bare shape, 12.59% macro). |
| L12 | 21:19 | `wiki/experiments/speech-aware-evidence-acquisition/2026-08-16-owner-go-kb34-runtime-intersection.md` | Intersection prohibition superseded for discovery tier under two conditions; DEMO explicitly NOT pre-granted a legal tier. |
| L13 | 21:19 | `wiki/experiments/speech-aware-evidence-acquisition/README.md`, `wiki/Research-Objective.md` | "n=44 admitted pending N0 power and the N1 routing gate"; **no committed N1/N2/DEMO plan document exists anywhere in umbrella or study repo**. |
| L14 | 21:20 | `studies/.../docs/readiness/2026-08-09-conec-evidence-shape.md` | ConEC contexts are lowercased deduplicated unigram sequences, 102–2149 terms/call; distractor-only arm already designed but never flown. |

Web accesses (all via WebSearch / WebFetch, no logins, no paid APIs):

| # | time (UTC 2026-08-17) | query / URL | one-line result |
|---|---|---|---|
| W1 | 01:12 | WebSearch: "negative demonstrations in-context learning contrastive examples do they help or hurt LLM" | Surfaces contrastive-ICL positives (2401.17390, contrastive CoT, LC-ICL 2606.29407) — all text classification/reasoning, none on copy suppression, none on speech. |
| W2 | 01:12 | WebSearch: "in-context demonstrations teach model to reject unreliable context counterfactual robustness RAG few-shot" | Surfaces "Why So Gullible?" (2305.01579, NAACL-F 2024), Knowledgeable-R1 (2506.05154), RbFT, Faithfulness-QA (2604.25313) — and **In-Context Fixation (2605.08295)**. |
| W3 | 01:14 | WebFetch: `arxiv.org/html/2605.08295v1` (In-Context Fixation) | Demonstrated labels become an exhaustive answer vocabulary: homogeneous opposing labels collapse accuracy to ≤12% (gaps 64–100pp); nonsense label sets take 42–67% of probability mass; **fixation STRENGTHENS with scale** (Qwen3-8B 93–100pp gaps); **recency dominates** — one corrective demo in the last slot fully reverses seven opposing demos, the same demo first has zero effect; contextual calibration leaves a 40pp residual. |
| W4 | 01:14 | WebSearch: "Why So Gullible enhancing robustness retrieval-augmented models counterfactual noise in-context learning results" | LMs "highly brittle to conflicting information in BOTH the fine-tuning and the in-context few-shot scenarios"; their fix needs a fine-tuned discriminator or a strong prompted model (GPT-3.5). |
| W5 | 01:16 | WebSearch: "few-shot demonstrations teaching abstention 'I don't know' in-context learning unanswerable does it work frozen model" | Abstention-by-ICL works *partially* on frozen models (1 unanswerable / 4 answerable is the reported sweet spot); RL still dominates the answerable/unanswerable trade-off (abstention surveys 2407.18418 / TACL 2025; Abstain-R1 2604.17073). |
| W6 | 01:16 | WebSearch: "audio LLM in-context demonstrations speech recognition few-shot copying hallucination Qwen omni 2026" | Surfaces FSA-GRPO (2606.02615) and **TICL (2509.13395)** — retrieved text-embedding-KNN speech ICL on frozen LMMs, i.e. the DEMO lane's mechanism, published. |
| W7 | 01:18 | WebFetch: `arxiv.org/html/2606.02615` (FSA-GRPO) | Frozen Qwen2.5-Omni 3-shot: RSR 35.42→27.29 but **MyST 23.05→22.72 (≈nil)**; no negative/contrastive/reject demonstrations tested anywhere; their SA reward explicitly bounds similarity "to avoid over-copying from the retrieved labels" — over-copying is a named hazard they had to *train* against. |
| W8 | 01:18 | WebFetch: `arxiv.org/pdf/2509.13395` (TICL) | Training-free retrieved demonstrations for ASR on frozen LMMs; no copying failure-mode analysis, no control for it, no negative demonstrations. (PDF extraction was thin on exact tables — re-verify numbers before citing.) |

---

## 2. The five strongest methodological attacks, ranked

### ATTACK 1 (fatal to the headline) — n=44 is not n=44: it is 10 tuning calls with ≥20 prior hypothesis reads, pooled with 34 calls whose *gold* already drove the design. The block as planned cannot produce an unbiased effect estimate, and the study's existing p-values do not survive their own exposure history.

**The evidence.** The exposure ledger shows one split-identity hash (`744c4b2e`, the seeded 10-of-44
`r4-e21-sub10`) carrying at least: R4 three arms, E-005 three arms, the E-005B framing family,
E-005B-N10 three arms, P1R-metadata10, the P1 fast-3 trio, the four D4 shape screens, and the five
P2 R-ladder arms — twenty-plus distinct hypotheses read on ten calls. Every design parameter N2
intends to fly was *selected on those reads*: the locked reference-only framing, the compact
small-N roster form, alphabetization, casing, verbatim typo preservation, the 90 s window era, the
v3 evidence shape. The pilot effect N2 is powered from (−0.30pp macro, +117 entity, 7/10) is an
in-sample effect on the tuning set. Pooling it into the primary statistic imports a winner's-curse
bias of unknown size and destroys the interpretation of the p-value.

The 34 are not a clean remedy either. Their gold was read offline to build the P0.1 reachability
partition (which is what told the program that stratum a2 is the big one and that metadata covers
company+speakers), the confusion-pair extraction, and lexicon-v2. Model exposure on the 34 is one
bare decode; *analyst* exposure is substantial. So the earnings21 44 contains no stratum that is
clean in the pre-registration sense — only strata that are dirty in different ways.

The knock-on: the program's most-quoted number, names-roster p=.027, is uncorrected inside a family
of ≥20 reads on the same ten samples. Bonferroni over 20 puts it above 0.5. The T3 ProfASR rebuttal
and the "form dominates dose" keystone both currently lean on it.

**Design fix (concrete, all pre-registration-side, zero extra GPU except the last item):**
1. Declare the frozen ten a **TUNING SET** by name in the N2 registration. Its numbers are reported
   as descriptive; no p-value computed on it enters any claim sentence. Restate the keystone as
   "selected on the tuning set, magnitude to be estimated out of sample".
2. **Primary inference on the 34-call stratum only.** Pre-register the pooled 44 number as a
   secondary, descriptive figure with the strata printed side by side, and pre-commit to the rule
   "if the 34-stratum contrast and the pooled contrast disagree in sign or decisiveness, the
   34-stratum governs".
3. Pre-register a **strata-heterogeneity read** (34 vs 10 delta-of-deltas) as a diagnostic, not a
   test; a large gap is the measurable signature of tuning-set overfitting and is itself publishable.
4. Add the **earnings22 dev-10** as a mandatory cross-carrier companion arm-pair (zero + legal
   roster). It is the only sample identity in the study that has never been adapted to (one smoke
   read, SAEA-E-001). ~1.5 GPU-h. Without it, no claim in this study has ever been evaluated on
   material the design did not see.
5. Add a `prior_hypothesis_reads` counter to the exposure ledger keyed at **sample** level (see
   Attack 5) so the correction factor is auditable rather than reconstructed by grep.

---

### ATTACK 2 (fatal to attribution) — a two-arm zero-vs-roster design cannot distinguish "the model heard the entity because the roster named it" from "the model emitted the entity because the roster contained the string", and this study has already measured that its core copies supplied strings at 94–100% of opportunities.

**The evidence.** On this exact vehicle: 49 of 53 replay outputs byte-identical to the supplied
reference; 7/9 wrong-reference copies under *both* framings; one wrong-reference edit passed the
full guard chain into a final transcript. Cluster D adds the external replication (2607.21943:
Qwen3-Omni-30B blind-copy 94.2%). The r0bias forensics adds a concrete N2-shaped failure: a roster
PERSON name fuzzy-matched the ordinary word "fastest", cleared the flag floor, and was accepted; the
three accepted splices delivered zero gold tokens and ~4 spurious insertions.

A compact roster of correct in-call proper nouns is *exactly* the stimulus that makes copying and
listening indistinguishable: every roster term that appears in the output is scored as a win, whether
the model recognised it acoustically or simply spent tokens from the supplied vocabulary. The n=10
metadata result (~20 distinct names flipping) is fully consistent with both stories. The study has run
a mismatched control for the *full ConEC bag* (R4-mismatched, E-005-mismatched) and for the *replay
reference* (p1-oracle-v2-shuffled), but **never for the compact roster** — the one form the surviving
candidate is built on.

The plan's own precedent makes refusal indefensible: the P2 block was voided by exactly the control
that N2 currently omits.

**Design fix:**
1. **Length-stratified deranged-roster arm is mandatory, not optional.** Fixed derangement over the
   44 calls, each call receiving another call's metadata roster, with the derangement constrained to
   match roster length within a stratum (otherwise a 2-term call receiving a 16-term roster confounds
   content with dose). This arm is automatically cost-matched — same form, same token profile — so it
   discharges the "cost-matched control" requirement at the same time.
2. **Pre-register a false-alarm ledger on every arm**: count emissions of roster terms at positions
   where the reference has no such entity (this is LOGIC's FAR / the harmful half of the edit-quality
   lineage). Under the deranged roster this is a pure copy-rate measurement with a clean expectation
   of zero. Pre-declare a kill threshold (e.g. deranged-arm entity gain ≥ 40% of the true-roster gain
   ⇒ the gain is scored as vocabulary supply, not recognition, and the claim is withdrawn).
3. **Bounded audio-mismatch spot control** (cluster D calls this table stakes and they are right):
   three calls' slices run with the correct roster and *another call's audio*. Any roster term emitted
   there is copying with no acoustic support. Cheap, decisive, and its absence is the easiest
   desk-reject available to a reviewer who has read 2607.21943.
4. Report byte-level roster regurgitation (list-vomiting) as a first-class number, since the roster is
   a list and LOGIC documents prompt-supplied lists leaking verbatim.

---

### ATTACK 3 — N1 as specified measures the wrong conditional, gates the wrong block, and is (as currently built) a gold-derivative under the study's own doctrine.

Three separable defects.

**3a. Wrong conditional.** "Flag recall against oracle-reachable errors" estimates
`P(flagged | correctable-by-the-oracle-roster)`. The system being built supplies a *deployment-legal*
roster that carries company + speakers only — the N10 verdict states outright that the oracle-vs-legal
gap is **label coverage, not mechanism**. A flag optimised against oracle recall will therefore be
optimised to route spans the legal supply cannot fix, and the recall number will over-state routable
headroom by the coverage ratio (empirically ~12% of the oracle entity effect at n=10). The quantity
that governs a legal-supply system is `P(flagged | correctable-by-the-LEGAL-KB)` together with its
converse, `P(correctable-by-the-legal-KB | flagged)` — the fraction of a bounded routing budget that
is actionable at all.

**3b. Wrong block.** The registered MUST-NOT-FLY line ("no scaling past n=10 until the oracle-routing
gate shows S1 retains a usable fraction") was written in PHASE 3 for the **D3 ConEC full chain** —
a per-span, routed, splice-delivery design. N2 as it now stands is a **static whole-prompt roster**:
there is no runtime routing decision in it at all. Applying a routing gate to it is a category error
in both directions — it blocks a block it does not govern, and it lets that block fly without
measuring the thing that actually bounds it, which is *supply coverage*, not span recall.

**3c. Legality.** The S1 band flag's parameters (band [0.05,0.45], df-rarity smoothing, K=2/slice,
"proper-name P@1 0.252") were tuned with the **oracle roster** as the matching anchor — the r0bias
forensics labels its own material "ceiling-tier (oracle roster)". Doctrine dimension 1 states that
gold-guided *selection* is a leakage channel equal to content, and the either-field rule makes any
arm with a gold-derived `span_source` ceiling-tier. An oracle-tuned flag entering a deployment-tier
runtime path would therefore violate the study's own D2 standard. Compounding it: flag v2 will be
designed on offline traces from the same 44 calls it will then be evaluated on.

**Design fix — replace N1 with a two-part, zero-GPU supply-reachability audit, and demote routing:**
1. **N1a Coverage ledger (offline, all 44, no model contact).** For every entity error token in the
   frozen scoring layer, compute whether its correct surface form is present in that call's legal
   roster. Output: per-call and corpus coverage `C`, roster size distribution, per-entity-type
   coverage in ConEC's exact schema (PERSON/ORG/GPE/...). Commit it **before** the block flies. This
   is publishable on its own (nobody prints it), it is the honest analogue of ConEC Table 1, and it
   is the pre-run predictor of the block's effect: expected entity gain ≈ `C` × conversion, with
   conversion ≈ the n=10 measured value. If that product is below the block's minimum detectable
   effect (Attack 4), the block should not fly as designed.
2. **N1b Routing metrics, restated and reconditioned**, and only for the targeted variant: report the
   triple (recall over *legally*-reachable mass, precision, budget concentration across terms —
   45% of the r0bias window budget went to three terms and 25.5% of windows fired on already-correct
   spans; a recall-only gate passes that flag). All three pre-declared with floors.
3. **Re-tune the band against legal-roster matching only**, on a disjoint surface (the earnings22
   dev-10, or a held-out sub-fold of the 34), freeze it, and record `span_source` accordingly. If the
   flag stays oracle-anchored, label every arm using it ceiling-tier and remove it from the
   deployment claim entirely.
4. Keep routing out of N2's runtime path. A static roster needs no gate; introducing a tuned-on-eval
   flag into it would import a selection-on-test-set defect for no measured benefit.

---

### ATTACK 4 — the analysis plan is simultaneously under-powered (call-level macro WER) and anti-conservative (token-level entity ledger), the two co-primaries are unadjusted and mutually dependent, and the macro metric is contaminated by a known instruction-controlled artifact of the same magnitude as the effect.

Five compounding statistical defects, all fixable on paper.

**4a. Under-power on the macro co-primary.** The pilot effect is −0.30pp with per-call deltas
spanning at least −? to +1.27 (one regression) and +2.20 observed on the names arm. With a per-call
delta SD near 1pp, n=44 gives SE ≈ 0.15pp and a true −0.30pp effect lands at t ≈ 2 — the block is
*designed to return an ambiguous p*, on a pre-tuned effect, on a partly contaminated sample. And the
power calculation itself is being derived from the tuning set that will be re-used in the test, which
inflates apparent power.

**4b. Anti-conservative entity ledger.** The 8284-token denominator is heavily pseudo-replicated: the
n=10 "+117 tokens" was produced by roughly **20 distinct name types** (Nextar 4→15 is one type
flipping eleven times; Culp 1→9 is one type flipping eight). Any test that treats the 8284 tokens as
independent units will manufacture significance out of a handful of roster hits. Conversely a
call-level test throws away the structure that carries the effect.

**4c. Unadjusted, dependent co-primaries.** Two co-primary ledgers with an "either fires" reading
doubles the family-wise error rate, and they are not independent — they are two functions of the same
output strings.

**4d. Contaminated macro metric.** The P1 verdict measured that number formatting is a volatile,
**instruction-controlled** axis: one instruction variant swung >100 digit tokens; 59 of 68 arm-only
misses on one call were digit-form. Adding a roster *is* an instruction change. A −0.30pp macro
delta is the same order as the artifact, and the artifact does not cancel across calls because it is
systematically induced by the treatment.

**4e. Estimand mismatch.** The headline numbers (12.38, 12.09) are token-weighted corpus WERs; the
test (paired Wilcoxon over calls) is unweighted per call. They are different estimands, and a 75-min
call counts the same as a 20-min call in the test but four times as much in the headline. Wilcoxon's
location reading also assumes symmetric differences, which heavy-tailed WER deltas violate.

**Design fix:**
1. **Hierarchical, not co-primary.** Entity-WER is the single primary (largest relative effect,
   uncontested by the closest priors — Siskos reports no entity metric). Macro WER becomes a
   pre-registered **non-inferiority guardrail** with a declared margin (e.g. the claim fails if the
   macro delta exceeds +0.25pp), tested only if the primary fires. No alpha spent twice.
2. **Two-way cluster-robust inference on the entity outcome**: paired bootstrap resampling **calls**
   and **entity types** (the naive token test is anticonservative, the naive call test is
   underpowered; resampling both clusters is the honest middle). Report the number of distinct types
   moved alongside the token delta — always both, never tokens alone.
3. **Format-normalized macro as a mandatory co-reported secondary**, plus a per-call digit-token-share
   diagnostic, so a macro null or regression can be attributed rather than argued.
4. **Effect size as fraction-of-oracle-headroom recovered** (dimensionless, comparable to ConEC row 5
   and DeRAGEC Table 4, survives small n) — this requires the oracle-names ceiling arm at n=44, see
   the arm set below.
5. **Pre-register the minimum detectable effect and an explicit INCONCLUSIVE branch**, with the
   consequence spelled out in advance (what the candidate wording becomes if the block returns
   directional-but-not-decisive, which on these numbers is the modal outcome).
6. **Intention-to-treat vs per-protocol.** The roster is 1–16 terms per call and is *null by
   construction* on calls whose metadata yields only a company name. Pre-register roster size as a
   stratifier, declare a "roster-eligible" subset (≥3 terms) as the per-protocol primary and the full
   44 as the ITT secondary, and report the dose-response. Otherwise a null is uninterpretable —
   dilution and mechanism failure look identical.
7. Name **one** primary contrast (legal roster vs zero); every other arm-pair is secondary and
   descriptive.

---

### ATTACK 5 — the DEMO lane's central mechanism (reject-case demonstrations steering copy behavior) has no supporting evidence in any modality, the published evidence points the other way, and its construction/evaluation split does not exist.

**5a. No evidence for the mechanism; the closest evidence is adverse.** I could not find a single
published result showing that in-context contrastive or reject-case demonstrations *reduce* a frozen
model's propensity to copy supplied strings. What exists:
- **In-Context Fixation (2605.08295)**: demonstrated labels become an exhaustive answer vocabulary.
  Homogeneous opposing demonstrations collapse accuracy to ≤12% (64–100pp gaps); nonsense label sets
  capture 42–67% of probability mass. **The effect strengthens with model scale** (strongest at 8B,
  the largest tested). Post-hoc contextual calibration leaves a 40pp residual. A reject-case
  demonstration puts the *wrong* string into the context of a model that this study has measured
  reproducing supplied wrong strings at 7/9, and that 2607.21943 measures at 94.2% on the same core.
  The default prediction from the literature is that reject demonstrations *supply* the error
  vocabulary rather than immunise against it.
- **Recency dominates position**: one corrective demonstration in the final slot fully reverses seven
  opposing ones; the same demonstration first has zero effect. Any DEMO design is therefore an
  ordering experiment as much as a content experiment, and an unordered bank is under-specified.
- **FSA-GRPO (2606.02615)**: frozen Qwen2.5-Omni gains 35.42→27.29 on RSR from 3-shot audio-text
  demonstrations but only 23.05→22.72 on MyST — the frozen benefit is real on one carrier and nil on
  the other, i.e. not a dependable prior. They tested **no** negative/contrastive/reject
  demonstrations, and their reward explicitly bounds similarity "to avoid over-copying from the
  retrieved labels" — over-copying is a hazard they had to *train* against with GRPO.
- **Abstention-by-ICL** works only partially on frozen models (best reported mix ≈ 1 unanswerable /
  4 answerable) and is dominated by RL; **Why So Gullible? (2305.01579)** finds LMs "highly brittle
  to conflicting information in both fine-tuning and in-context few-shot" and needed a fine-tuned
  discriminator or a frontier prompted model to fix it.
- **TICL (2509.13395)** already publishes training-free retrieved demonstrations for ASR on frozen
  LMMs — the DEMO lane's positive-demonstration mechanism is prior art, and it reports no copying
  control either.

**5b. The construction split does not exist.** DEMO is to be built from a "gold-permitted
construction split". The only gold-permitted split is the kb-construction 34 — which the 2026-08-16
owner GO has just folded into the n=44 evaluation set. Owner condition 1 forbids any artifact built
from those 34 calls' gold from entering the runtime path of a block that evaluates on them. Inside
earnings21 there is therefore **no construction split disjoint from the evaluation split**.

**5c. Exposure/legality accounting is unresolved by construction.** The owner GO explicitly refuses
to pre-grant DEMO a legality tier; the bank contains gold text verbatim, so under the either-field
rule a bank-consuming arm is ceiling-tier unless the bank's labels come from a legal source.

**Design fix:**
1. **Do not run DEMO as a WER block.** Run a **copy-contamination screen** first, at ≤16 requests,
   whose only readout is a leak rate: how often the demonstration's *error* strings appear in outputs
   on items where they do not belong. Pre-declare a kill threshold. This is the direct analogue of
   the wrong-reference control that voided P2, applied *before* spending a block rather than after.
2. **Make ordering an explicit registered axis** (reject-case first vs last), because the only strong
   published mitigation is recency, and an unordered bank is not a specified treatment.
3. **Leave-one-call-out construction** is the only design that satisfies owner condition 1 on
   earnings21: for each evaluated call, the bank is built from the other 43. Register it that way or
   move construction to earnings22 dev-10 and accept the cross-corpus shift.
4. **Register the legality tier at the screen**, not after: gold-text demonstration labels ⇒
   ceiling-tier, full stop, unless the label side is re-sourced legally (metadata / pinned documents /
   the core's own truecasing).
5. Cite TICL and FSA-GRPO in the registration as the positive-demonstration prior art so the lane's
   contribution is stated as the *reject-case* half, which is the only unoccupied part — and which
   the fixation literature predicts will fail.

---

## 3. Answers to the specific questions asked

**(a) Is a routing gate measured under oracle knowledge the right gate for a legal-supply block?**
No — see Attack 3. It measures `P(flag | oracle-reachable)` when the system's behaviour is governed
by `P(flag | legal-KB-reachable)` and by `P(legal-KB-reachable | flag)`. The legal-roster-conditioned
routing question is: *of the error mass whose correct surface form the deployment-legal KB actually
contains, what fraction does the flag surface, at what precision, and how concentrated is the budget
across terms?* For the static-roster N2 there is no runtime routing at all, so the binding pre-run
quantity is **coverage**, not recall: what fraction of entity error mass is legally supply-reachable.
That is computable offline on all 44 calls at zero GPU cost and should replace N1 as the gate.

**(b) N2 composition, two-arm design, paired test.** See Attacks 1, 2, 4. Summary: the composition is
10 tuning-contaminated + 34 analyst-contaminated calls presented as one exchangeable sample; the
two-arm design omits the derangement control that this program's own void demonstrates is mandatory
and omits any false-alarm accounting; the paired plan mixes estimands, leaves two dependent
co-primaries unadjusted, uses a macro metric contaminated by an instruction-controlled format axis of
the same magnitude as the effect, and is powered from the sample it will re-test.

**(c) Does −0.28pp bound what a better flag could route?** **No — it is aperture-conditional and is
being over-generalized.** It is triple-conditioned:
- *on the aperture*: 55 windows / 23 reachable entity mentions surfaced by one oracle-anchored S1
  band at K=2/slice, over 6 effective calls. The same ten calls' static oracle roster moved **999
  entity tokens**. The denominators differ by ~43× *before* any guard question is asked.
- *on oracle reference content*: the counterfactual "accept every false rejection" is only benign
  because 49/53 replay outputs were byte-identical to the *correct* supplied reference. Under a legal
  roster the same acceptances splice whatever the roster says; the harmful branch of the
  counterfactual was never computed, so −0.28pp is an oracle-conditioned upper bound whose legal-tier
  analogue could be negative.
- *on unblinded post-hoc adjudication*: 30/15/5-undetermined FALSE/CORRECT/UNDET labels assigned by an
  analyst after the fact, with 9 of 30 "gains" conceded as gold-annotation artifacts. No interval is
  reported, and the report prints percentages without the 6-call entity-token denominator, so nobody
  downstream can recompute the figure.

What the number *does* license, and the only form in which it should ever be quoted: **a yield/cost
statement.** 21 genuine recoveries / 55 windows ≈ 0.38 entity tokens per replay window; matching
static supply's ~999 tokens through this path needs ~2,600 windows per ten calls (~47× the aperture,
≈1 extra model call each), and per-window yield must be assumed **non-increasing** as the band widens
because these 55 were the top of the band and 25.5% of them already fired on correct spans. That
argument survives; "the replay ceiling is −0.28pp" does not. Fixes: always print the denominator
(55 windows / 23 reachable mentions / 6 calls); publish an interval; re-adjudicate blind if the number
becomes load-bearing; and never state it without the monotonicity assumption named.

**(d) Reject-case demonstrations.** See Attack 5. No published evidence either way in speech; the
adjacent text evidence (In-Context Fixation) predicts the opposite of the intended effect and says the
effect grows with scale; the one audio-ICL paper that engaged with over-copying had to train a reward
bound against it. Treat the mechanism as unsupported and gate it behind a contamination screen.

**(e) Statistical / exposure-accounting flaws.** Beyond Attack 4:
- **Exposure is tracked at split level, not sample level.** Every frozen-ten row registers the
  identity hash `744c4b2e` while describing itself as "discovery split (44)". When N2 registers the
  real 44 (`fcc1b0bc`) any inheritance check keyed on the hash will treat it as a *new, unexposed*
  split — while 10 of its 44 members are the most-read samples in the study. **Fix: per-sample
  exposure counters, and a mandatory registration field stating the max and median prior-read count
  across the block's samples.**
- **The `consumed` flag is not machine-readable.** Rows say "consumed stays no" in the column and then
  carry "CONSUMED 2026-08-15: <results>" appended as prose in the same cell. The one field that
  enforces one-shot semantics is maintained as free text. **Fix: a real field with read timestamp and
  reading commit, plus a gate refusal for plans naming a split whose rows are consumed without an
  explicit re-read authorization.**
- **No multiplicity ledger exists.** One-shot semantics prevent re-running an arm until it wins; they
  do nothing about testing twenty hypotheses on one sample. **Fix: a `hypotheses_read_on_this_split`
  counter and a standing rule that frozen-ten p-values are descriptive.**
- **Baseline-reuse precedent.** The P1 verdict's "arm A = reused SAEA-E-005B-zero (14.48)" shows the
  house habit. The 34 already have a zero decode (kb34 floor, 12.59%) — but under `np16` wide bare
  shape, an older commit, and a different block. **Reusing it as N2's zero arm would confound the
  primary contrast with serving shape, harness commit and date. The zero arm must be re-flown inside
  the same block, same config hash, same night.** Budget for it explicitly.
- **The plan itself is not committed.** There is no N1/N2/DEMO plan document anywhere in the umbrella
  or study repo — the owner GO cites "plan doc §7" for a file that is not hash-addressable. A
  pre-registration that cannot be shown to predate the read is not a pre-registration. **Fix: commit
  the plan doc, with the arm set, the analysis plan, the thresholds and the branch rules, before the
  block launches — the P2 pins file (`b5fb51c`) is the correct precedent and should be repeated.**

---

## 4. The minimal N2 block I would sign off

**Arms** (all on the full frozen discovery 44, identical commit / config hash / serving shape /
instruction lock, flown in one block; the zero arm re-flown, never reused):

| # | arm | tier | why it is minimal |
|---|---|---|---|
| A0 | **zero** (locked reference-only framing, no roster) | legal | The paired baseline. Non-negotiable that it flies in-block. |
| A1 | **legal compact roster** (per-call metadata: company + non-placeholder speakers, verbatim, typos preserved) | legal | The claim. |
| A2 | **length-stratified deranged roster** (each call gets another call's roster, roster length matched within stratum) | legal | The only arm that separates content-relevance from vocabulary supply; automatically cost-matched. After the P2 void, omitting it is indefensible. |
| A3 | **oracle names roster** | ceiling | Anchors "fraction of oracle headroom recovered" — the dimensionless effect size that survives small n and is the study's answer to "Siskos got 17%, you got 2.3%". Also completes the coverage/conversion decomposition that is the block's actual contribution. |

Four arms is the floor. If a fifth is affordable, it should be **A4 self-derived roster** (rare-word /
NER extraction over the system's own pass-1 hypotheses — a dimension-2 legal system product, zero
gold, and the rung RECOVER and most competitors silently occupy). A4 is worth more than a ConEC-bag
arm: the ConEC comparison can be made honestly from the already-measured full-bag result plus the
published ConEC table, whereas nobody has measured whether "legal" even needs external metadata.

**Companion pair** (mandatory, ~1.5 GPU-h): **A0' + A1' on earnings22 dev-10** — the only sample
identity the design has not been fitted to.

**Controls that cost no GPU and must be committed BEFORE launch:**
1. **Coverage ledger** — per-call and corpus fraction of entity error mass whose correct surface form
   is in that call's legal roster, plus roster size distribution and per-entity-type coverage in
   ConEC's schema. With the predicted effect derived from coverage × the n=10 conversion rate, and a
   pre-declared "do not fly" rule if that prediction is below the block's MDE.
2. **Committed plan document with the analysis plan**: entity-WER primary with a two-way
   (call × entity-type) cluster-robust paired bootstrap; macro WER as a non-inferiority guardrail at
   a declared margin; format-normalized macro and digit-token-share as mandatory secondaries;
   token-weighted and per-call estimands both reported with the primary named; one primary contrast
   (A1 vs A0); MDE and an explicit INCONCLUSIVE branch with its consequence for the candidate wording.
3. **Stratified reporting rule**: 34 (primary) vs 10 (tuning, descriptive) printed separately, pooled
   figure descriptive only, with the disagreement rule pre-committed.
4. **Per-protocol/ITT rule**: roster-eligible (≥3 terms) per-protocol primary, full 44 ITT secondary,
   dose-response reported.
5. **False-alarm / copy ledger on every arm**: roster-term emissions without gold support; verbatim
   list-regurgitation count; pre-declared kill threshold on the deranged arm's share of the true
   arm's gain.
6. **Bounded audio-mismatch spot control** (3 calls, roster correct, audio from another call) — a few
   GPU-minutes, and the cheapest insurance against the "you replicated perception bypass and called it
   a gain" desk-reject.
7. **Exposure-registration fields**: per-sample prior-read counts (max/median) for the block's 44, and
   the machine-readable `consumed` field.

**What I would explicitly refuse to sign off:** a two-arm zero-vs-roster block; any block whose zero
arm is composed from the kb34 floor decode; any block whose primary p-value is computed on the pooled
44 without the strata rule; any arm whose runtime path contains an oracle-tuned flag while claiming
deployment-legal tier; and any DEMO arm scheduled before its copy-contamination screen returns.
