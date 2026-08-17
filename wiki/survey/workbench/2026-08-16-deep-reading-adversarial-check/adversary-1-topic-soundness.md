# ADVERSARY 1 — TOPIC SOUNDNESS (doctoral-endpoint lens)

Role: prosecute the question *after the P2 VOID, is "deployment-legal targeted evidence supply for a
frozen speech-omni core" still a defensible RESEARCH OBJECT, or has it collapsed into
engineering/prompt-craft?* — then argue the defense where the evidence genuinely supports it.

Author: Adversary-1 agent, 2026-08-16 night (local) / 2026-08-17 UTC.
Inputs: the four cluster digests (A RECOVER / B metrics / C biasing / D copying) supplied by the
parent, plus first-hand read-only inspection of the study and umbrella documents listed below, plus
three bounded web checks of my own. Nothing under `studies/` was modified; no git commands were run.
This file is the only file I created.

Standing caveat on inherited evidence: every prior-art number attributed to RECOVER / Siskos / ConEC /
DeRAGEC / Voice Memory / LOGIC / "Listen, Do Not Copy" / ProfASR below is **second-hand from clusters
A–D**, which read them first-hand. I re-verified none of them and none of my attacks depend on a
disputed digit — they depend on the *shape* of those results, which all four clusters agree on.

---

## 1. ACCESS LOG

All times local (UTC+8) on 2026-08-16 unless marked. Web queries: 3 searches + 1 fetch.

| # | time | kind | target | one-line result |
|---|---|---|---|---|
| 1 | 21:07 | ls | `wiki/survey/workbench/2026-08-16-deep-reading-adversarial-check/` | dir exists, 4 cluster digests present (A/B/C/D), 129KB total |
| 2 | 21:07 | ls | `studies/speech-aware-evidence-acquisition/docs/readiness/` | 46 readiness docs, 2026-08-05 → 2026-08-16 |
| 3 | 21:08 | read | `docs/readiness/2026-08-16-p2-rladder-verdict.md` | VOID confirmed: r1wrong 7 raw copies vs pin floor 2; r0wrong 7/9 vs r1wrong 7/9; RIR 0/54 and 0/53; one harmful splice accepted |
| 4 | 21:08 | ls | `docs/checks/.../2026-08-16-r0bias-guard-forensics/` | one file, `report.md`, 5297 B |
| 5 | 21:09 | read | `docs/checks/.../2026-08-16-r0bias-guard-forensics/report.md` | 49/53 byte-identical; 30 FALSE / 15 CORRECT rejections; 9/30 gains are gold-annotation artifacts; counterfactual ceiling −0.039pp macro / −0.28pp entity vs static supply −12pp |
| 6 | 21:09 | read | `wiki/Project-Thesis.md` | north star = training-free RL over a frozen black-box core; TF-Strict; "the first innovation hypothesis is the system itself"; metric is never the research object |
| 7 | 21:11 | read | `docs/readiness/2026-08-15-legality-doctrine.md` | three dimensions (gold red line incl. SELECTION / system capability is legal / deployment-shaped matching) + mandatory `span_source`+`reference_source` per-arm schema |
| 8 | 21:11 | read | `docs/readiness/2026-08-15-n10-block-verdict.md` | the N10 four-arm table (zero 12.38/32.01, matched 12.39/29.10, names 10.88/19.95, metadata 12.09/30.60); law 5: oracle-vs-legal gap is LABEL COVERAGE, not mechanism |
| 9 | 21:11 | read | `docs/readiness/2026-08-14-p1-ceiling-verdict.md` | re-listen B−A = +0.08 (nil); C flips 10/14 oracle terms; flag targeting misses entities 17/17; number-format axis swings >100 digit tokens per framing |
| 10 | 21:13 | read | `docs/readiness/2026-08-14-stage2-candidate-freeze.md` | Candidate B frozen hypothesis (now partly voided); Candidate A cross-call KB CLOSED by the reachability partition (stratum b = 37.1% mass, zero rare proper names) |
| 11 | 21:13 | read | `docs/readiness/2026-08-15-rectification-plan.md` | the D1–D7 rectification chain, MUST-NOT-FLY list, and the honest T3 note that the legal rung (12.09, n.s.) is currently CONSISTENT with ProfASR |
| 12 | 21:14 | read | `wiki/Research-Objective.md` | HOT page already updated to the VOID; OBS/ORG/SUPPLY/USE research object; three-part evaluation contract |
| 13 | 21:14 | read | `docs/readiness/2026-08-09-positioning-and-ablation-ladder.md` | the A0–A5 and L0–L5 ladders; **L3 self-supplied glossary / L4 "does external context add anything the system could not supply itself" — designed 2026-08-10, never run** |
| 14 | 21:16 | WebSearch | "training-free acoustic confidence estimation without logits frozen speech LLM API-only routing contextual biasing 2026" | surfaced arXiv 2604.12398 (IBM, speech-LLM contextual biasing with **bias word position prediction**) — direct threat to the C2 routing white space; fetched at #16 |
| 15 | 21:16 | WebSearch | "multi-hypothesis sampling disagreement as confidence for ASR entity error detection frozen model no logprobs" | no single matching paper; but decoder-**disagreement-based ASR error detection is long-standing prior art** (RNN-LM + complementary ASR; GMM/DNN disagreement regions) — relevant to how N1's proposed acoustic signal may be claimed |
| 16 | 21:17 | WebFetch | `https://arxiv.org/html/2604.12398v1` | **Decisive.** IBM Research, Novitasari/Fukuda/Kurata/Saon, 2026-04-14. Speech-conditioned bias-word POSITION prediction exists and works (bias-WER 5.8→4.4, 24.1% rel, 200-word list) but needs **LoRA fine-tuning of the LLM + a CTC-trained 9–11-layer FNN tagger over speech-encoder projector latents AND LLM causal hidden states** — i.e. full white-box + training. Tagger removed at inference. |
| 17 | 21:17 | WebSearch | "self-supplied glossary from own ASR transcript as bias list long-form contextual biasing training-free no external context 2026" | no occupying hit; dynamic-vocabulary biasing is an active area but the own-transcript-derived glossary on a frozen omni is not visibly taken. Weak evidence, not load-bearing. |

---

## 2. THE EVIDENCE BASE, RESTATED IN THE FORM A COMMITTEE WILL SEE IT

The four numbers that decide topic soundness:

| quantity | value | source |
|---|---|---|
| deployment-legal supply, macro | 12.38 → **12.09** (−0.30pp = **2.4% rel**), p=.19, 7/10 | N10 verdict |
| deployment-legal supply, entity-WER | 32.01 → **30.60** (−1.41pp = **4.4% rel**), +117/8284 tokens | N10 verdict |
| oracle ceiling, entity-WER | 32.01 → 19.95 (−12.06pp = 37.7% rel), macro −1.50 p=.027 | N10 verdict |
| legal arm as a fraction of the ceiling | **~20% of the macro effect, ~12% of the entity effect** | N10 verdict, law 5 |

Against the closest comparators, as a reviewer will line them up (all second-hand, all with different
metrics/consumers — the point is the **order of magnitude a first-pass reader sees**):

| system | carrier | legal? | headline relative gain |
|---|---|---|---|
| SAEA metadata roster | Earnings-21 | yes | 2.4% macro / 4.4% entity |
| ConEC 2024 (shallow fusion) | Earnings-21 | yes | 1.2% macro / **13.3% PERSON** |
| Siskos 2509.19567 | Earnings21 + 2 | yes | **17% WER** (oracle 24.1%) |
| RECOVER 2603.16411 | Earnings-21 | **unstated** | **33.4% E-WER** |
| IBM 2604.12398 | CV/SPGI/Gigaspeech | n/a | 24.1% bias-WER (but LoRA + trained tagger + hidden states) |

We win the macro column against ConEC's legal rung and lose every other cell. That table is the
committee's first slide, and it is the frame every attack below is written against.

---

## 3. THE FIVE SURVIVING ATTACKS (ranked)

### ATTACK 1 — The only surviving differentiator is speech-conditioned routing, the study has measured it broken three separate times, and every published version of it is outside the study's own boundary. C2 is currently a *hope*, not a hypothesis with supporting evidence.

**Charge.** All four clusters independently converge on the same conclusion: after the VOID, the
differentiation load sits on **speech-conditioned targeting** (cluster A: "now a requirement not a
nicety"; cluster C: "speech-conditioned routing = strongest and unoccupied"; cluster B: "the
speech-conditioning claim must be *demonstrated*"). The study's own measurements of its routing stage
are:

- P1: logprob flags hit **0/17** real entity errors — every flagged span was function-word/boundary text.
- Offline S1 harness: roster-anchored band proper-name **P@1 = 0.252** (vs production 0/17).
- P2 forensics: the roster-band flag surfaced **55 windows / 23 reachable entity mentions**, i.e. an
  aperture whose *perfect* exploitation is worth **−0.28pp entity-WER against a −12pp static-supply
  ceiling (~2–3% of reachable error mass)**; **25.5% of fired windows were on already-correct spans**;
  **45% of the window budget went to three terms** with 7 total gold slots; and a roster PERSON name
  fuzzy-matched the ordinary word "fastest" and was *accepted*.

Meanwhile every published system that does succeed at speech-conditioned targeting sits outside the
API-only/no-training boundary: **BR-ASR** (trained retriever, speech-conditioned), **GLCLAP+GRPO**
(contrastive pretraining + GRPO), **LOGIC** (logit-space Trie, needs vLLM logit access), and — my own
find, not in the clusters — **IBM arXiv 2604.12398**, which predicts *bias-word position from the
acoustics* using a CTC-trained tagger over **speech-encoder projector latents and LLM causal hidden
states**, with LoRA fine-tuning of the LLM. Four independent teams got there with weights, gradients,
or logits. The study proposes to get there with a prompt and a string-similarity band.

**Why it survives.** The white space is real precisely *because* it is hard, and the study has no
positive evidence — none, at any scale — that any API-legal signal separates entity errors from the
rest. The tail risk is not "N1 returns a weak number"; it is that **N1 returns a second null on top of
the VOID**, at which point the study has two negative results, one of them scooped, and a 4.4%-relative
replication as its positive. Two nulls and a replication is not a Stage-2 qualified candidate; it is a
cautionary tale with a good methods section.

**What would have killed this attack.** A single measurement showing an API-legal signal (repeated-decode
disagreement, cross-offset instability, own-draft NER confidence) achieving non-trivial recall on true
entity errors. The study has never run one. The 0.252 P@1 offline number is the closest thing and it is
a *retrieval* precision, not an error-detection recall.

**Plan change demanded.**
1. **Reclassify N1 from a gate into the study's primary experiment**, with its own preregistration and a
   success floor declared *before* it runs. Set the floor by inverting the forensics arithmetic: declare
   the minimum flag recall × per-window oracle yield that would make routed supply reach some
   pre-stated fraction (e.g. ≥ 1/3) of the −12pp static ceiling. If the floor is unreachable in
   principle at any recall, the routed architecture is dead on arithmetic before a GPU turns.
2. **N1 must test at least one genuinely ACOUSTIC, API-legal signal**, not only "entity-aware flag v2".
   Text-side entity-aware flagging is DeRAGEC Appendix F prior art *and* the same appendix shows it
   degrades as WER rises — i.e. it fails exactly where it is needed. The only logit-free acoustic
   channels available are **multi-decode disagreement** (temperature and/or window-offset resampling —
   RECOVER's mechanism, which needs no internals) and **cross-window inconsistency of the same entity**.
   Note honestly (log row #15) that decoder-disagreement error detection is decades-old prior art: the
   contribution is that it is the *only* channel surviving the API-only boundary, not that it is new.
3. **Pre-commit the kill rule for C2.** If no API-legal speech-side signal clears the floor, C2 is
   retired the same day and the study's endpoint changes (see verdict) — it does not get quietly
   re-scoped into "entity-aware flagging" (a text signal) while keeping the speech-conditioned claim.
4. **Declare the no-logit/no-weights constraint explicitly and prominently** in every positioning
   document, so IBM 2604.12398, LOGIC, BR-ASR and GLCLAP read as *out-of-scope by construction* rather
   than as uncited stronger baselines. Add IBM 2604.12398 to the citation set now — it is the closest
   trained analogue of C2 and its absence would be a visible hole.
5. **Restate the −0.28pp forensic as aperture-conditional.** As written it reads "guard perfection is
   worthless"; what it actually says is "guard perfection is worthless *at 2–3% aperture*". If that
   number is to be load-bearing it must be reported as a monotone family over recall, not a point.

---

### ATTACK 2 — The measuring instrument is not sharper than the effect. On both co-primary ledgers the study has already measured nuisance terms equal to or larger than the entire deployment-legal effect. Statistical significance at n=44 would therefore not buy validity.

**Charge.** Three prongs, all from the study's own documents:

1. **Format nuisance ≥ effect, on the entity ledger.** The P1 verdict records that the number-format
   axis is "volatile, instruction-controlled": the `ctxinstr` instruction variant alone swings
   **>100 digit tokens** (E-005F −162 errors vs zero), and on 4366522, **59 of 68** arm-only reference
   misses were digit-form tokens. The metadata roster's *entire* entity gain is **+117 tokens**. The
   nuisance and the signal are the same size, and format-normalized reading is currently classified as
   "analysis-only secondary".
2. **Gold-annotation defects on the very ledger that is to be co-primary.** The forensics found that
   **9 of 30** apparent gains on the LOCALIZE channel were Earnings-21 annotation artifacts —
   possessive stripping (`SiTime's`→`SiTimes`) and inconsistent gold spellings (`Tribeca`/`Tribecca`,
   `Livingstone`/`Livingston`). That is a locally measured **30% artifact rate on an entity-gain
   channel**. The 8284-token entity ledger draws on the same gold and inherits the same defects at an
   **unmeasured** rate. A +117-token result with an unmeasured 0–30% artifact exposure is not evidence.
3. **The macro effect is inside the study's own declared tooling allowance.** The positioning document
   fixes a **±2pp** tooling allowance for placing this study's Earnings-21 numbers beside published
   ones. The legal arm's macro effect is **0.30pp**.

**Why it survives, and the honest concession.** The *power* prong does **not** survive and I withdraw
it: at the observed 7/10 favourable-sign rate, n=44 gives ≈31/44, sign-test p ≈ 0.005 one-sided. n=44
is very likely adequately powered. **That is exactly what makes this attack dangerous rather than
harmless** — the block will probably return a significant p-value on a 0.30pp effect that sits inside
two measured nuisance bands, and the study will then have to defend a significant result it cannot
distinguish from instruction-induced digit drift and annotation noise. A reviewer who reads the P1
verdict (which the study will have to cite, since the format artifact is one of its own findings) can
construct this attack in five minutes.

**Plan change demanded.**
1. **Entity-WER primary; macro demoted to a pre-registered non-inferiority guardrail.** (Clusters B and C
   both reach this independently; I concur and add that macro's demotion is now *forced* by prong 3, not
   merely tactical.)
2. **Promote the format-normalized read from secondary to a co-registered primary companion.** Any
   entity-ledger claim must be reported both raw and format-normalized, with the frozen scorer still
   the arbiter. If the effect does not survive normalization it is not an effect.
3. **Run an annotation-defect audit of the 8284-token entity ledger BEFORE N2 registers** — a purely
   offline, zero-GPU job. Measure the possessive/inconsistent-spelling artifact rate corpus-wide, then
   pre-register either an exclusion list or a declared sensitivity band. Until that number exists, the
   entity ledger's precision is unknown and every entity claim is uninsured.
4. **Report the effect as fraction-of-oracle-headroom-recovered** (metadata = ~12% of the oracle entity
   effect, ~20% of macro). It is dimensionless, comparable to ConEC row 5 / DeRAGEC Table 4, and — this
   is the point — it makes the *ceiling gap* the finding rather than the small absolute delta.
5. **N0 must state the power arithmetic honestly**, including the concession above, so no one later
   claims n=44 resolved a validity problem it cannot touch.

---

### ATTACK 3 — The "four-dimension control plane" defense has been falsified by the study's own measurements. Of OBS / ORG / SUPPLY / USE, one is measured nil, one is closed, one is voided, and one works. A four-dimension framing with one live dimension is a taxonomy wearing a system's clothes.

**Charge.** Tallied strictly from this study's own verdicts:

| dimension | status | evidence |
|---|---|---|
| OBS | **nil** | P1: re-listen effect B−A = +0.08pp; "targeted re-listening alone pays nothing" |
| ORG | **closed** (as cross-call KB) | Reachability partition: stratum (b) = 37.1% of error mass but **zero rare proper names**; "the cross-call error-pattern KB route is CLOSED by measurement" |
| SUPPLY | **positive** | 10/14 oracle flips; metadata roster −0.30/+117 |
| USE | **VOIDED** | P2 R-ladder: 7/9 vs 7/9, RIR 0/54, one harmful accepted splice |

The umbrella thesis states "the first innovation hypothesis is the system itself". The system has now
been measured, and three of its four organs do nothing on this carrier. A committee will ask, fairly:
if the decomposition were load-bearing, why did the study's own factorial reduce it to contextual
biasing?

**Why it survives.** Because it attacks the *strongest defense* (see Defense 1), not a weak one, and it
is built entirely from the study's own numbers. There is no external citation to argue with.

**The honest limits, which must be stated in the same breath.** (i) The OBS null is fast-3 era, 9
windows, 6 splices — that is not a scale-grade null and should not be cited as one. (ii) ORG's closure
is specific to the **cross-call error-pattern KB**, not to ORG generally: roster construction and
roster *hygiene* are ORG, and the forensics shows hygiene is worth real mass (25.5% false-positive
windows, 45% budget monopolization, oracle-roster contamination entering as authoritative forms).
Conflating "the KB route closed" with "ORG closed" would be the study's own error, and the documents
currently make that conflation easy.

**Plan change demanded.**
1. **Stop selling the four-dimension control plane as the contribution. Sell the factorial attribution
   as the contribution.** The honest and considerably stronger sentence is: *"On a frozen speech-omni
   core reached only through an API, we separately manipulated observation, organization, supply and
   use, with per-stage error-mass accounting, and only supply converts — here is why, in mass terms,
   for each of the other three."* That is a real result. "We built a four-dimension control plane" is a
   figure caption.
2. **Split ORG-as-KB (closed) from ORG-as-roster-hygiene (open) in every document**, and route the
   hygiene findings into WP1 as a measured axis rather than a footnote.
3. **Either re-run the OBS null at scale or explicitly label it underpowered** wherever it is cited.
   A 9-window null presented as a dimension-level finding is an attack surface.

---

### ATTACK 4 — The surviving positive is a consumer swap on ConEC's own corpus, with ConEC's own content class, reproducing ConEC's own result shape — published in 2024.

**Charge.** ConEC (LREC-COLING 2024) built per-call context on **Earnings-21** from slides, earnings
releases, and **participant names and affiliations**. The N2 arm supplies **company + speaker names
from dataset-shipped CSVs**. Same corpus, same content class, same legality posture. The result shapes
are near-identical:

| | ConEC (trained shallow fusion) | SAEA N2 pilot (frozen prompt) |
|---|---|---|
| no context | 10.41 | 12.38 |
| legal per-call context | 10.29 (−1.2% rel) | 12.09 (−2.4% rel, n.s.) |
| oracle | 9.69 | 10.88 |
| entity channel | PERSON 45.9 → 39.8, oracle 13.0 | entity-WER 32.01 → 30.60, oracle 19.95 |

ConEC also already published the **coverage ledger** (PERSON 82% / ORG 66% / GPE 61% / … / FAC 29%;
without the roster PERSON drops to 30%) and a **harmful-supply datapoint** (the shared-distractor row
degrading GPE/NORP/FAC below no-context). And ConEC beats us on the entity channel in relative terms
(13.3% vs 4.4%). So: the mechanism, the corpus, the content class, the coverage ledger, the oracle gap,
*and* the harm datapoint are all prior art. What is new is the consumer.

**Why it survives.** "Same finding, new substrate" is a replication. Replications are valuable and are
not doctoral research objects. The study must produce something that is *only* true of the new
consumer, and it has not yet measured one.

**The genuinely new thing that is available.** There is an unexplained **inversion of the dose law
across consumers, on this exact corpus**: trained consumers are dose-robust (Siskos: c=100→250 helps,
and 15.17× the oracle token count still wins), while frozen prompt-reading consumers are dose-fragile
(this study: full bag = zero macro gain at 4× tokens; Ren et al.: EWER 1.80 exact / 4.16 at ~50 / 5.61
at ~1800; DeRAGEC's U-shape at k=15; LOGIC: degrades past 50–100 entries). Nobody has run both
consumers on one substrate with one metric. Cluster C reached the same conclusion independently and
calls it "SAEA's most defensible framing". I agree, and I go further: **it is the only framing under
which N2 is not a replication.**

**Plan change demanded.**
1. **Run ConEC's published per-call context as an explicit arm on this vehicle at n=44 (= ConEC's own
   eval set).** The deliverable becomes a **consumer contrast**, not a re-derivation. Resolve the
   licensing question first — cluster C flags that the ConEC repo states **no license**; that is a
   blocking legal question, not a footnote.
2. **Register the dose ladder inside the same block** so the consumer-dependent dose law is *measured*
   rather than asserted from five heterogeneous citations.
3. **Compute and publish this study's roster coverage ledger, in ConEC's exact schema and per entity
   type, BEFORE the block runs** — including the open question cluster C flagged: whether the shipped
   Earnings-21 CSVs reach the fidelity ConEC needed a Seeking Alpha scrape to obtain. If they do not,
   the arms are not comparable and the whole contrast is compromised; that must be known first.
4. **Cite ConEC as the primary comparator in the candidate narrative from now on**, not as background.
   Currently the T3 positioning work is aimed at ProfASR-Bench (synthetic TTS, tiny models) — the
   weakest available opponent. Choosing the weakest opponent is itself a visible weakness.

---

### ATTACK 5 — Legality is currently a procurement problem, and the study's own law 5 says so. "Get better name lists" is sourcing, not science.

**Charge.** The N10 verdict, law 5, verbatim: *"The oracle-vs-legal gap is LABEL COVERAGE, not
mechanism: metadata carries only company + speakers; the names roster carries every error-prone
entity. The path to closing the gap is the pinned tier-3 document-label route."* Read plainly, the
study's own conclusion is that its remaining headroom is obtained by **acquiring more label sources** —
IR pages, filings, scraped participant lists. ConEC already did exactly that scrape in 2024 and
published the resulting coverage ledger. A research object whose next step is "obtain a better list
from a different URL" has, on that axis, become an engineering task.

**Why it survives.** Because the doctrine as written is a **constraint** — a thing arms must satisfy —
and constraints are not findings. Unfalsifiable-by-construction: no experimental outcome can make the
legality doctrine wrong. Cluster A raised this independently ("your legality constraint is unfalsified
— you never priced it") and cluster C rates legal provenance the **weakest** of the four candidate
deltas.

**What the study holds that partially answers it.** The four closest priors each have a provenance
hole, and the clusters documented them first-hand: **RECOVER** states entity-list provenance for only
2 of 5 carriers and is silent on Earnings-21 — whose references *ship entity tags* — leaving a
gold-harvest reading of its headline column unrebutted; **ConEC's** lists carry no license;
**Voice Memory's** memory is built with gold references in an offline accept/reject loop;
**DeRAGEC's** ICL rationales are synthesised offline by o1 *using ground truth*. Four for four. That is
a field-level hygiene finding, and it is genuinely citable — but only if the study converts the
doctrine from a rule into a measurement.

**Plan change demanded.**
1. **Promote legality to the measured independent variable** — the price-of-legality ladder, with every
   adjacent contrast pre-registered regardless of sign:
   `{ zero | self-supplied glossary from own pass-1 transcripts | dataset-shipped metadata roster |
   tier-3 pinned document labels | gold oracle }`. Deliverable = a **coverage → gain transfer
   function**, per provenance tier and per entity type. ConEC published coverage and one gain number;
   nobody published the transfer function.
2. **Put the self-supplied glossary rung in the ladder and run it.** This is the study's own **L3**
   rung, designed 2026-08-10 and never executed, and its **L4** question — *"does external context add
   anything the system could not supply itself?"* — is the sharpest question anywhere in this study's
   documents. It is maximally legal (zero procurement, zero external source, zero leakage surface); it
   is RECOVER's own legal recipe (auto-NER over the system's own hypotheses) in a form no one has run
   on a frozen omni; my search (log row #17) found nothing occupying it; and **both outcomes are
   informative**. If self-supplied ≈ procured metadata, the procurement framing dies and the study
   gains its best result. If procured wins, the coverage transfer function is the finding. Either way
   Attack 5 is answered by measurement rather than by doctrine.
3. **Publish the provenance-hole audit of the four closest priors as the doctrine's motivation.** That
   converts an unfalsifiable constraint into a critique with evidence — and it is the one place where
   this study is unambiguously ahead of the field.

---

## 4. ATTACKS I CONSIDERED AND DISMISSED (for the record)

- **"n=44 is underpowered."** Withdrawn — see Attack 2. 7/10 → ≈31/44 → sign-test p ≈ 0.005. Power is
  probably fine; validity is the exposure. Anyone repeating the power version of this attack is
  attacking the wrong thing and will lose.
- **"The negative finding cannot be a centerpiece."** True but already prosecuted to completion by
  cluster D, which established priority (2607.21943, three weeks earlier, same model family, stronger
  silence control, ships the remedy) and correctly recommended killing standalone negative
  publication. I add only one thing, in the verdict: the *category* distinction between a negative
  **outcome** and a negative **law**.
- **"The oracle ceiling merely restates contextual-biasing 101."** Half-true and not fatal on its own.
  The −12pp oracle entity result is indeed unsurprising as a direction. But the ceiling is being used
  as an *instrument* — the denominator for fraction-of-headroom-recovered and the arithmetic that made
  the routing choke point visible (−0.28pp vs −12pp) — and instruments do not need to be surprising.
  The attack only bites when combined with Attack 5 (the gap is coverage), which is where I put it.
- **"HER/RIR are metric-novelty claims."** Fully handled by cluster B (HER is Voice Memory's and is
  `1 − Precision` of the survey's §5.2 alignment; RIR's denominator change is the only defensible
  claim; the Edit Rate lineage citation was factually mis-pinned). Nothing to add.

**One liability I flag without ranking it:** the **DEMO lane** is, on the clusters' evidence, the
weakest surviving item and should not become the recovery plan if N1 disappoints. Its mechanism is
published (FSA-GRPO: frozen Qwen2.5-Omni 35.42 → 27.29 with 3-shot audio-text demos), its legality
posture is Voice Memory's executed at scale with an acceptance gate, and — decisively — answer-bearing
demonstrations are *exactly* the stimulus class that perception bypass copies. A study that has just
measured 49/53 byte-identical parroting should not next hand the model gold answers as exemplars
without a silence control and an answer-overlap screen registered in advance.

---

## 5. THE THREE STRONGEST DEFENSES

### DEFENSE 1 — The per-stage causal instrumentation is a genuine asset, it is unmatched in the read literature, and it answers a gap the field's own survey names.

The forensics report is the exhibit: 55 windows individually adjudicated into FALSE / CORRECT(save) /
CORRECT(neutral) / UNDET / N-A; a rejection taxonomy decomposed by guard stage; a counterfactual ceiling
computed on **both** ledgers (−0.039pp macro / −0.28pp entity) and set against a comparator (−12pp); a
proof that one guard is *unfixable by threshold tuning* (identical `(pass1, ref)` distance pairs appear
as a genuine fix at one occurrence and a hit-corrupting error at another, so the discriminator must be
per-occurrence acoustic support); and — the part that is hardest to fake — a **self-imposed honest
discount** of 9/30 gains as annotation artifacts.

Now the comparison. Cluster A: RECOVER has **no limitations section, no oracle/retrieval-recall study,
no harmful-edit count, no CIs, no seeds, no cost table**. Cluster C: LOGIC asserts the prompt-biasing
ceiling with **no prompt baseline table** — "assertion + anecdote + internal sets". Cluster B: Siskos
reports **no entity metric and no harm accounting**. ConEC publishes coverage but not a transfer
function. And survey 2508.07285's own Section 6, gap #3, says almost nobody classifies post-refinement
error types. **The study is above the field's standard on precisely the axis the field names as its own
gap.** That is a defensible doctoral asset: a thesis can be built on measuring what everyone else
asserts. It is also the asset that makes the negative results *interpretable* rather than merely
disappointing — the VOID comes with a mass accounting, which is why we can say what it costs.

### DEFENSE 2 — The legality doctrine is enforced, pre-emptive, and lands on a real, four-for-four hole in the closest prior art. It is not prompt-craft.

Three properties distinguish it from a hand-wave. (i) It is **specific in the non-obvious direction**:
gold-guided *selection* of terms, spans, or exemplars is banned as a leakage channel equal to content —
which is the exact trapdoor DeRAGEC falls through (o1-synthesised rationales built from ground truth)
and Voice Memory walks through deliberately (gold-reference accept/reject loops). (ii) It is
**machine-carried**: two mandatory per-arm fields (`span_source`, `reference_source`), either being
gold-derived forces a ceiling-tier label that propagates into the registration, every result table, and
every verdict — so a ceiling number can never be quietly read as a method number. (iii) It has already
**caught a real withdrawal** (the SAEA-SMOKE-mapflip round-c precedent) and it produced the correct
self-critical reading in the rectification plan, where the study writes down that its legal rung
(12.09, n.s.) is *currently consistent with* the counter-claim it wants to rebut. A construct that
makes its owner concede against interest is doing work.

And the hole is real: of the four closest priors, **all four** have a provenance defect (RECOVER 2/5
carriers documented and silent on the one corpus that ships entity tags; ConEC no license; Voice Memory
gold-in-the-loop; DeRAGEC gold-derived rationales). Under Attack 5's plan change — legality as a
measured ladder with a transfer function — this stops being a constraint and becomes a finding.

### DEFENSE 3 — There is a law-shaped question here, both of whose answers are informative, and the study is the only party positioned to answer it. Two of the three arms are already instrumented.

The question is not "does a legal roster help" (answered, 2024, ConEC). It is:

> **What determines whether a frozen multimodal core USES, COPIES, or IGNORES supplied evidence — as a
> function of supply form, dose, provenance tier, and routing aperture — and why does the dose law
> invert between trained and frozen consumers on the same corpus?**

That is a question, not a method. Supporting evidence already in hand: the dose inversion is real and
unexplained (trained consumers dose-robust to 15× oracle token count; frozen prompt readers degrade
past 50–100 entries, U-shape at k=15, zero macro gain at 4× tokens); the copy failure mode is
instrumented at the token level in a way no prior does (**49/53 byte-identical outputs** — all priors
use forced-choice or closed labels, so none of them can even *see* verbatim reproduction); and the
form-over-dose keystone is measured (compact cased roster beats the full bag by 1.51pp macro and +758
entity tokens at ~1/4 the tokens). Cluster A's reading sharpens it further and is, in my judgement, the
single most useful sentence produced by the four clusters: RECOVER supplies a **constrained vocabulary**
with offset-anchored edits and a rejection filter, whereas the voided chain supplied a **whole candidate
reference** — a complete fluent answer, for which emission is the cheapest available action. That
reframes the VOID from "verification does not work" to **"whole-reference supply is a copy trap under
which verification is unmeasurable"**, which is a *mechanism-bearing* claim about supply form.

And my own find strengthens this defense rather than weakening it: IBM 2604.12398 establishes that
speech-conditioned bias-word localization **does work** — with LoRA and hidden states. Together with
BR-ASR and GLCLAP, three independent teams show the signal exists in the internals. That makes N1's
question well-posed and its null informative: *is speech-conditioned error routing recoverable at the
API surface, or does it live only in the internals?* A clean negative answer to that, with the mass
accounting from Defense 1 attached, is a real boundary result about black-box control planes — which
is, word for word, this program's north star.

---

## 6. VERDICT ON TOPIC VIABILITY

**The research object as currently worded has collapsed; the study has not.** "Deployment-legal
targeted evidence supply for a frozen speech-omni core" is a method statement whose answer was
published on this exact corpus, with this exact content class, in 2024 (ConEC), and whose current
effect — 2.4% relative macro at p=.19, 4.4% relative entity, ~12% of its own oracle headroom — sits
inside two nuisance bands the study itself measured (an instruction-controlled format axis worth >100
digit tokens against a +117-token signal, and a locally-measured 30% gold-annotation artifact rate on
an entity-gain channel). Sharpened to a prompt pattern plus a string-similarity flag, that is
engineering, and a committee would say so. But three assets survive the VOID intact and none of them is
prompt-craft: per-stage causal instrumentation that exceeds the field's own standard on the axis its
survey names as a gap; an enforced, machine-carried legality construct that lands on a documented
four-for-four provenance hole in the closest prior art; and a token-level-instrumented corpus of
copy/dose behaviour on the one consumer class nobody else has measured. Those support a *different*
object — **the consumption law: what makes a frozen multimodal core use, copy, or ignore supplied
evidence, as a function of form, dose, provenance tier and routing aperture** — under which N2 stops
being a replication (it becomes the frozen arm of a consumer contrast on ConEC's own corpus), legality
stops being an unfalsifiable constraint (it becomes a measured ladder with a coverage→gain transfer
function), and the VOID stops being a scooped negative outcome (it becomes a mechanism-bearing claim
about *supply form*: whole-reference supply is a copy trap). On the negative-result question
specifically: a negative **outcome** ("our operator did not work") cannot be a Stage-2 centerpiece —
it is scooped by 2607.21943 with a stronger control and a shipped remedy, and 7/9 vs 7/9 on 9 windows
cannot carry a parity claim; a negative **law** ("the signal lives in the internals; here is the mass
accounting for what the API surface forfeits") can be, and is exactly what N1 is positioned to produce
given that three trained systems have established the signal exists. **Viability is therefore
conditional and the condition is N1, which must be promoted from gate to primary experiment with a
pre-declared floor, at least one genuinely acoustic API-legal signal, and a pre-committed C2 kill
rule.** If N1 clears its floor, the study has a doctoral-grade object and n=44 should run as a consumer
contrast rather than a supply demonstration. If N1 returns a second null, the honest endpoint is a
bounded boundary result at workshop scale — published with the instrumentation and the legality audit
as its contribution — and the study should close there rather than spend n=44 defending a 0.30pp
replication against ConEC, Siskos and RECOVER simultaneously. What must not happen is N1 being run
without a declared floor: an undeclared floor lets a weak recall number be reinterpreted after the
fact as "good enough to proceed", and that is the single failure mode that would convert a defensible
study into an indefensible one.
