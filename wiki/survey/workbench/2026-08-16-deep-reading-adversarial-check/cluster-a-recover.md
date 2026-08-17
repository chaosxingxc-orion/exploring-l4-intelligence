# Cluster A — RECOVER deep read and adversarial check

Workbench note. Read-only survey pass; no repository state was modified outside this file.
Session UTC window: 2026-08-17T00:56Z – 2026-08-17T01:02Z. English only.

Target: **arXiv 2603.16411 — "RECOVER: Robust Entity Correction via agentic Orchestration of
hypothesis Variants for Evidence-based Recovery"**, Abhishek Kumar and Aashraya Sachdeva
(Observe.AI, India), submitted 17 March 2026, comments field "Under review. Submitted to
Interspeech 2026". Licence CC Zero on the HTML rendering. No code or data release found.

---

## 1. Fetch log

Timestamps are session-clock UTC. Access via WebSearch/WebFetch only; no logins, no paid APIs.

| # | Time | Query / URL | Result (one line) |
|---|------|-------------|-------------------|
| 1 | 00:56 | WebFetch `https://arxiv.org/abs/2603.16411` | Title, 2 authors, 17 Mar 2026, "Under review. Submitted to Interspeech 2026"; abstract; no code links. |
| 2 | 00:56 | WebSearch `RECOVER arXiv 2603.16411 ASR entity correction retrieval` | Confirmed ID, affiliation Observe.AI; surfaced HTML full text and adjacent priors (2409.06062 Apple RAG-NEC). |
| 3 | 00:57 | WebFetch `https://arxiv.org/html/2603.16411v1` (full-text extraction prompt) | Full method + setup + all result tables recovered, including Table 2 and Table 3 numbers. |
| 4 | 00:58 | WebFetch `https://arxiv.org/html/2603.16411v1` (provenance / cost / harm / audio / limitations prompt) | No cost analysis, no Limitations section, no audio after decode, no oracle or retrieval-recall study, no harmful-edit count. |
| 5 | 00:59 | WebSearch `"RECOVER" entity correction "hypothesis variants" agentic ASR 2026 citing` | No citing work found; surfaced newer adjacent 2607.26410, 2607.28175, 2606.13464, 2605.29430. |
| 6 | 00:59 | WebFetch `https://arxiv.org/html/2603.16411v1` (verbatim Section 2 + 3.1 request) | **Refused** by the fetch model on copyright grounds; re-planned as short-quote questions. |
| 7 | 01:00 | WebFetch `https://arxiv.org/html/2603.16411v1` (short-quote settle prompt: list provenance, calls, K, threshold, harm, coverage) | K=200 confirmed; Levenshtein threshold value not stated; 1 LLM call/segment for all four strategies; entity-list provenance NOT stated for Earnings-21 or Eka-Medical. |
| 8 | 01:00 | WebFetch `https://arxiv.org/abs/2607.28175` | AgenticASR (SJTU, 30 Jul 2026): disfluency/spoken-to-written refinement, not entity retrieval; low overlap with SAEA. |
| 9 | 01:00 | WebFetch `https://arxiv.org/abs/2607.26410` | **Voice Memory** (NVIDIA, 29 Jul 2026): inference-only, frozen corrector, per-utterance act-or-abstain, explicit overcorrection accounting 64%→35%, open source. High threat. |
| 10 | 01:01 | WebFetch `https://arxiv.org/abs/2607.26410` (detail prompt) | Abstain mechanism not detailed on abs page; 10 HyPoradise domains + ATIS-style air-travel + CHiME-4; memory-file provenance not stated on abs page; does not cite RECOVER. |
| 11 | 01:01 | WebFetch `https://arxiv.org/abs/2606.13464` | Ontology Memory-Augmented ASR Correction (11 Jun 2026): ontology memory retrieval, "selective and evidence-grounded corrections", RAMC-Corr; adjacent. |
| 12 | 01:01 | WebFetch `https://www.semanticscholar.org/arxiv/2603.16411` | HTTP 404 — no S2 citation graph reachable for this ID. |
| 13 | 01:01 | WebSearch `arXiv 2026 post-ASR entity correction retrieval agentic cites "RECOVER: Robust Entity Correction"` | No citing paper found; surfaced 2606.24915, 2506.07510 DeRAGEC, 2508.20700. |
| 14 | 01:02 | WebFetch `https://arxiv.org/html/2606.24915` | Error-Aware TF-IDF RAG (19 Jun 2026), Persian FLEURS, Gemini 2.0 Flash-Lite; no Earnings-21, no harm accounting. |
| 15 | 01:02 | WebFetch `https://arxiv.org/html/2603.16411v1` (reference list) | 35 references recovered in full; used for lane mapping below. |

Search budget used: 3 WebSearch calls (the cap). All other retrieval was bounded WebFetch on
already-identified URLs.

---

## 2. RECOVER — what it actually is

### 2.1 Pipeline (exact)

Three components, orchestrated as a tool-using agent over a **black-box ASR**:

**(a) Multi-Hypothesis Generation.** N hypotheses per audio segment. In the experiments,
N = 5 from a *single* ASR model — Whisper-small via `faster-whisper` — by temperature sampling at
T ∈ {0.0, 0.2, 0.4, 0.6, 0.8}. Stated requirement: for N > 1 the hypotheses must carry
*complementary* errors. Beam-search diversity or a true multi-system ensemble are named as
alternatives but not run.

**(b) Dynamic Entity Candidate Retrieval.** The entity phrase list can be large (up to 6,198
phrases), so the whole list is never sent to the LLM. A three-signal lexical scorer selects
**top-K = 200** candidates per segment:

- exact token hits, weight `w_e = 1.0` — words of the candidate appearing as exact tokens across
  *all* hypotheses;
- fuzzy similarity, weight `w_f = 1.2` — normalised Levenshtein between any candidate word and any
  hypothesis token, restricted to a ±3-character length band; described as the primary mechanism
  for recovering corrupted entities (`sitiva → cytiva`);
- phonetic prefix match, weight `w_p = 0.6` — binary, phonetic keys sharing a 5-character prefix.

Note the weight ordering: fuzzy > exact > phonetic. The paper claims final ranking at K=200 is
robust to moderate weight perturbation, but reports no sensitivity table.

**(c) Agentic Orchestration — three tools, run in sequence.**

- **Tool 1 — Fuse Hypotheses.** Counts exact substring matches of the retrieved top-K candidates in
  each hypothesis, producing per-variant entity-hit counts that drive variant choice. Four
  strategies:
  1. **1-Best** — pass the greedy T=0 hypothesis unchanged (N=1).
  2. **Entity-Aware Select** — pick the hypothesis with maximum exact entity-candidate substring
     matches; transcript length is a weak tie-break (longer ⇒ fewer deletions).
  3. **ROVER Ensemble** — entity-aware pivot, Needleman–Wunsch global alignment of the remaining
     hypotheses to the pivot, majority-vote token merge; ties favour the pivot; insertions accepted
     only with ≥3-of-5 support.
  4. **LLM-Select** — hand all N hypotheses plus top-K candidates to the LLM, which picks the base
     variant *and* may propose entity-only corrections in the same call.
- **Tool 2 — Propose Corrections.** Strictly constrained LLM prompt emitting find/replace edits.
  Rules: the replacement must be *exactly* one of the entity-list phrases; generic rewrites
  (grammar, punctuation, fillers, casing) are forbidden; near-miss correction is encouraged
  (`citeva → cytiva`). Output is JSON with character offsets, original span, replacement span,
  entity type, confidence, and reason. **The prompt text itself is not reproduced in the paper.**
- **Tool 3 — Verify & Apply.** Fully deterministic, no model in the loop: (1) replacement must
  exist in the entity phrase list; (2) case-only changes discarded; (3) wrong LLM character offsets
  are relocated by the system; (4) normalised Levenshtein between original span and replacement
  must clear a floor (`citeva → cytiva` passes, `star → cytiva` rejected) — **the numeric threshold
  is never given**; (5) edits applied left-to-right, overlapping later edits skipped.

### 2.2 Frozen vs called — the architectural point that matters for SAEA

- **Whisper-small is the frozen recogniser**, called **5 times per segment** (one per temperature).
- **GPT-4o is a second, separate answering LLM**, called **once per segment** in every strategy
  (LLM-Select folds selection and correction into that same single call).
- Ablation swaps GPT-4o → GPT-4o-mini for LLM-Select only.
- Nothing is trained. No decoder internals are touched — the paper is explicit that decode-time
  biasing needs internals "unavailable when using production ASR systems as black boxes".

So RECOVER is training-free and black-box, **but it uses a second answering LLM**. Under SAEA's
own research boundary ("no second answering LLM", single frozen omni core answering) RECOVER is
*not a legal architecture inside this study*. It can be cited as prior; it cannot be reproduced as
a SAEA arm without breaking the boundary. This cuts both ways and is handled in §5.

### 2.3 Carriers, metrics, headline numbers

Five carriers. Entity-list sizes and entity reference-token counts:

| Dataset | Segments | Audio h | Entity phrases | Entity ref tokens |
|---|---|---|---|---|
| Earnings-21 | 2,086 (~1-min clips from 44 calls) | ~38.8 | 1,013 | 6,535 |
| ATCO2-test-set-1h | 560 | ~1.1 | 446 callsigns | 4,771 |
| Eka-Medical | 3,619 | ~8.4 | 6,198 | 42,449 |
| Common Voice 22 | 16,401 | ~27.1 | 3,098 (BERT NER, per Thorbecke et al.) | 7,889 |
| ContextASR-Dialogue | 5,273 | ~221.9 | 3,704 movie names (shipped) | 92,381 |

Metrics: WER via SCLITE; **E-WER** = WER computed only over reference tokens belonging to entity
phrases; **RWERR** = relative E-WER reduction vs the Whisper greedy T=0 no-correction baseline;
plus entity precision / recall / F1.

**Main table (all %; baseline = Whisper-small greedy, no correction):**

*Earnings-21* — baseline WER 13.59 / E-WER 23.81 / F1 80.02 (P 93.25 / R 70.07).
1-Best 13.51 / 15.90 (33.2 RWERR) / F1 84.54 (P 88.74 / R 80.71).
Entity-Aware Select 14.34 / 15.59 (34.5) / F1 83.83 (P 86.17 / R 81.62).
ROVER 13.88 / 15.90 (33.2) / F1 83.89 (P 87.57 / R 80.50).
LLM-Select GPT-4o 13.55 / 15.85 (33.4) / F1 85.60 (P 91.15 / R 80.69).
LLM-Select GPT-4o-mini 14.07 / 20.93 (12.1) / F1 82.19 (P 91.90 / R 74.33).

*ATCO2* — baseline 48.63 / 51.50 / F1 54.76 (P 70.77 / R 44.66). 1-Best 47.18 / 46.68 (9.4).
Entity-Aware Select 65.53 / 46.82 (9.1). ROVER 64.43 / 47.39 (8.0).
LLM-Select 4o 44.51 / 44.06 (14.5) / F1 62.11. 4o-mini 50.73 / 50.35 (2.2).

*Eka-Medical* — baseline 17.23 / 19.63 / F1 86.56. 1-Best 14.57 / 15.62 (20.4).
Entity-Aware Select 19.31 / 16.22 (17.4). ROVER 19.39 / 16.24 (17.3).
LLM-Select 4o 13.93 / 15.09 (23.1) / F1 90.21. 4o-mini 17.04 / 18.28 (6.9).

*Common Voice* — baseline 15.02 / 25.57 / F1 73.40. 1-Best 14.82 / 15.05 (41.2).
Entity-Aware Select 18.72 / 15.35 (40.0). ROVER 18.17 / 15.69 (38.6).
LLM-Select 4o 14.45 / 13.88 (45.7) / F1 84.13. 4o-mini 15.88 / 21.56 (15.7).

*ContextASR-Bench* — baseline 9.40 / 4.82 / F1 94.89. 1-Best 9.42 / 4.21 (12.7).
Entity-Aware Select 10.54 / 4.36 (9.6). ROVER 9.77 / 3.82 (20.8).
LLM-Select 4o 9.30 / 3.97 (17.8) / F1 95.17. 4o-mini 9.75 / 4.51 (6.6).

**Entity-level SCLITE alignment deltas (baseline → LLM-Select):**
Earnings-21 C 4,994→5,511 / S 1,248→781 / D 293→243 / I 15→12.
ATCO2 C 2,433→2,742 / S 1,694→1,470 / D 644→559 / I 119→73.
Eka-Medical C 35,258→36,989 / S 6,324→4,627 / D 867→833 / I 1,140→946.
Common Voice C 5,939→6,830 / S 1,811→952 / D 139→107 / I 67→36.
ContextASR C 88,056→88,838 / S 3,352→2,815 / D 973→728 / I 132→122.

Substitution reduction accounts for 63–93 % of total error reduction. Recall gains: +11.6 pp
(Earnings-21), +8.2 (ATCO2), +6.2 (Medical), +21.5 (Common Voice), +0.9 (ContextASR).

### 2.4 Evidence-use control present in RECOVER

- **Verification: yes, but deterministic and text-only.** Tool 3 is a rule filter (list membership,
  case guard, offset relocation, Levenshtein floor, overlap skip). There is no model-based
  self-check, no re-reading of the audio, no confidence calibration.
- **Abstention: no.** There is no per-segment decision to skip correction; every segment goes
  through Tool 2. Routing does not exist in this system — supply and correction are unconditional.
- **Harm accounting: absent as a first-class metric.** The paper never counts harmful edits, never
  reports an edit-level worsen rate, and has no Limitations section. The only harm evidence is
  indirect: precision drops of 7–9 pp on Earnings-21 (93.25 → 91.15) and Common Voice
  (96.39 → 87.74), the WER blow-up on ATCO2 under ROVER (48.63 → 64.43, +15.8 pp) and under
  Entity-Aware Select (→ 65.53), and the corpus-level C/S/D/I deltas of Table 3.
- **Audio after decode: never.** Purely post-ASR text.
- **Oracle / retrieval-recall analysis: absent.** The paper never asks whether the correct entity is
  inside top-200, and never reports a ceiling. There is no "what happens when the right answer is
  not retrieved" study.
- **Statistics: absent.** No confidence intervals, no significance tests, no seed variance, single
  run per cell.

### 2.5 Cost profile

Not reported anywhere — no token counts, no latency, no dollar figures, no API-call table.
Reconstructed from the method: **5 Whisper-small decodes + exactly 1 frontier-LLM call per
segment**, with a ~200-phrase candidate block plus 1–5 hypotheses in the prompt. Scale implied by
the carriers: ~27.9 k segments total across the five sets, i.e. of order 28 k GPT-4o calls for one
full sweep of one strategy. The GPT-4o-mini ablation is the cost signal in disguise: dropping to
the cheap model collapses Earnings-21 RWERR 33.4 → 12.1 and ATCO2 14.5 → 2.2. **The method is
stapled to a frontier proprietary LLM**; it degrades by roughly two-thirds without one.

### 2.6 Entity-list provenance — the paper's weakest joint

Settled by targeted quoting: provenance is stated for **only two of five** carriers.

- Common Voice: explicitly auto-derived — entities extracted with a BERT NER model following
  Thorbecke et al.; 3,098 phrases. Legal, no gold.
- ContextASR: 3,704 movie-name entities "provided in the dataset". Shipped metadata.
- ATCO2: 446 callsign entities, chosen because other entity types were "mostly general phrases" —
  reads as dataset metadata but the sourcing sentence is not given.
- **Earnings-21: no provenance sentence at all.** Only "The entity list of 1,013 phrases covers
  organisation names, person names, financial terms, and product names."
- **Eka-Medical: no provenance sentence at all.** Only the 6,198-phrase composition.

The paper also never discusses how a practitioner obtains the list at deployment time. This is a
live vulnerability for RECOVER and a live opportunity for SAEA — see §5, Attack 2. Earnings-21
ships entity-tagged reference transcripts, so a reader who assumes the 1,013 phrases were harvested
from the test-set references will read the whole Earnings-21 column as an oracle-supply result.
The paper does not rebut that reading.

---

## 3. What RECOVER already occupies of SAEA's surviving plan

Mapped against the surviving plan (N1 routing gate, N2 targeted legal supply at n=44, DEMO lane)
and the claim ladder C0–C5.

**Occupied, strongly.**

- **Targeted supply as a mechanism (part of C1/N2).** RECOVER's Tool 1 + retrieval is a
  *hypothesis-conditioned, error-aware* targeted supply: top-200 of a phrase list, ranked by exact
  + fuzzy-Levenshtein + phonetic-prefix signals. SAEA's N2 static compact metadata roster is a
  weaker, unconditioned instance of the same family. SAEA's own "full-bag supply = no gain at 4×
  tokens" finding is *precisely the premise* RECOVER states for building the retriever, so SAEA
  cannot present dose/form sensitivity as a novel observation — only as a measured quantity.
- **The Earnings-21 entity-repair carrier itself.** RECOVER runs 44 calls / 2,086 one-minute
  segments / 38.8 h — the same corpus SAEA's n=44 block targets, with a published E-WER ledger
  (6,535 entity reference tokens vs SAEA's 8,284-token ledger). "First black-box LLM entity repair
  numbers on Earnings-21" is gone.
- **Constrained-edit use discipline (narrowed C3).** Tool 2's "replacement must be exactly a
  list phrase, no generic rewrites" is the deployment-grade version of constrained evidence use.
- **Deterministic post-hoc verification.** Tool 3 covers list membership, span relocation, and a
  similarity floor.

**Partly occupied.**

- **C1 legal coverage.** RECOVER supplies from lists whose legality is asserted nowhere for the two
  most impressive columns. SAEA's *auditable* provenance (dataset-shipped CSV metadata, zero gold,
  ledgered) is not occupied — but the *idea* of a non-gold list is, via the Common Voice
  BERT-NER recipe.
- **Edit-quality accounting.** Table 3's corpus-level C/S/D/I deltas belong to the Edit
  Rate / Improve@Edit / Worsen@Edit lineage. SAEA's HER/RIR must now cite **both** survey
  arXiv 2508.07285 **and** RECOVER's Table 3 as precedent for aggregate entity-alignment deltas.
  What is *not* occupied is per-edit harm attribution and any harm-vs-gain frontier.

**Not occupied at all — the surviving white space.**

1. **Routing / N1.** RECOVER corrects every segment unconditionally. There is no flag, no gate, no
   recall-of-flag measurement, no cost-of-routing argument. SAEA's C2 ("speech-aware routing") and
   the N1 offline flag-recall measurement have no counterpart here.
2. **Speech-conditioned targeting.** RECOVER's targeting is conditioned on *ASR text*
   (token overlap, character Levenshtein, phonetic key of the *written* form). Nothing is
   conditioned on the acoustic signal. SAEA's "speech-aware" framing survives intact — but only if
   SAEA's routing signal is genuinely acoustic rather than a text proxy, which is now a
   *requirement*, not a nicety.
3. **Audio-grounded verification.** Zero audio contact after decode. SAEA's negative finding
   (audio-grounded verification fails; the model parrots the supplied reference) is unclaimed
   territory, and RECOVER's design silently agrees with it (see §4).
4. **Ceiling / oracle forensics.** No retrieval-recall, no upper bound, no "how much error mass is
   reachable" analysis. SAEA's −12 pp static-oracle ceiling and the −0.28 pp guard-chain-perfection
   forensic have no analogue and are a genuine methodological contribution.
5. **Adversarial / wrong-reference stress.** Nothing.
6. **Statistical discipline.** Paired co-primary ledgers with p-values vs RECOVER's single-run
   point estimates.
7. **Single-core architecture.** RECOVER needs Whisper + GPT-4o. SAEA's one-frozen-omni-core
   constraint is strictly harder and unoccupied.
8. **Task conversion (C4, SLURP slot-SLU).** Untouched — RECOVER is transcription-only.

---

## 4. Does RECOVER report anything like copy-parity / parroting, or any wrong-reference control?

**Directly: no.** There is no experiment in which a deliberately wrong, deranged, or adversarial
reference or candidate is supplied and copy behaviour measured. There is no parroting metric, no
byte-identity check between output and supplied evidence, no measurement of the model's ability to
reject bad evidence. There is no adversarial arm of any kind.

**Indirectly: RECOVER is built on the assumption that the frozen LLM will copy, and hard-codes the
defence rather than measuring the failure.** Three converging signals:

1. **Tool 2's central constraint — "the replacement must be exactly one of the entity-list
   phrases" — is copy-by-design.** The system *wants* parroting; it treats the LLM as a slot-filler
   over supplied text, not as a judge of supplied text. This is the same behaviour SAEA measured
   (49/53 replay outputs byte-identical to the supplied reference), reframed as a feature.
2. **Tool 3 exists precisely because the LLM will substitute a wrong reference.** The Levenshtein
   floor with the worked example `star → cytiva rejected` is an admission that the model proposes
   semantically unjustified copies from the candidate block and must be stopped by a *non-model*
   filter. The authors did not trust an LLM to verify an LLM; they trusted a rule. **This is
   independent corroboration of SAEA's VOID**, from a team that hit the same wall and engineered
   around it without naming it.
3. **The GPT-4o-mini ablation is a capability-graded copy result.** Same constraints, weaker model,
   RWERR collapses (Earnings-21 33.4 → 12.1; ATCO2 14.5 → 2.2). Discrimination over supplied
   candidates, not correction ability, is what the frontier model buys — consistent with SAEA's
   read that copy behaviour is a model-capability regime, not a prompt-framing regime (SAEA showed
   four framings, including explicit verify framing, moved the raw copy rate not at all: 7/9 vs
   7/9 windows).

**The load-bearing asymmetry — and the most actionable finding in this cluster.**

RECOVER supplies a **constrained vocabulary** (≤200 phrases, no per-slot commitment) and demands
**offset-anchored find/replace edits with a rejection filter**. SAEA's voided replay chain supplied
a **whole candidate reference string** and asked the model to verify or repair it. These are
different supply *forms* with different failure geometries:

- Whole-reference supply gives the model a complete, fluent, plausible answer. The
  cheapest-likelihood action is emission. Copy parity under adversarial derangement is then close
  to the *expected* result, not a surprising one.
- Constrained-vocabulary supply gives no complete answer. There is nothing to emit wholesale; the
  model must locate a span and commit an edit, and every commitment is externally checkable.

**Implication for the claim ladder.** The C3 VOID should be narrowed further than "verification
operator does not work". The evidence supports: *whole-reference supply is a copy trap under which
verification is unmeasurable*, and the failure may be an artifact of supply form rather than a
capability limit. A constrained-edit supply form is **untested** in SAEA and is the form the only
close prior actually deploys. Recommend the parent consider whether the VOID's scope statement
should say "reference-form supply" rather than "the verification operator", and whether a cheap
constrained-edit screen is worth one bounded arm before C3 is retired. Recorded here as an
observation for the parent's decision, not as a proposal to reopen a closed read.

---

## 5. Three attacks on SAEA's N2 design from RECOVER's vantage, with neutralising control arms

### Attack 1 — "Your static roster is a strictly dominated ablation of our Tool 1."

*The reviewer's line.* SAEA supplies the same compact metadata roster in every window regardless of
what was heard. RECOVER shows that a trivial lexical retriever (exact hits 1.0 + fuzzy Levenshtein
1.2 + phonetic prefix 0.6, top-200) conditioned on the hypothesis converts a 1,013-phrase
Earnings-21 list into a 33–35 % relative E-WER reduction. SAEA's own null — "full-bag supply, no
gain at 4× tokens" — is exactly why RECOVER retrieves instead of dumping. So SAEA's N2 contrast
(zero vs static roster, 12.38 → 12.09 macro, +117 entity tokens, p = .19) is not a new method; it
is the unranked control cell of a published system, reported without the ranked cell.

*Neutralising control arm.* Add a **retrieval-ranked roster arm at matched token budget** to the
N2 block: identical roster source (dataset-shipped CSV metadata, zero gold), but per-window ranked
and truncated by RECOVER's three-signal score computed against the *locked zero-baseline
hypothesis*, with the same token count as the static roster arm. Pre-register the four-cell ladder
{zero, static roster, ranked roster @ matched tokens, static oracle} on the identical paired
co-primary ledgers. Either outcome is publishable: ranked > static strengthens the supply claim and
pushes the story onto routing; ranked ≈ static is a **matched-cost null that RECOVER never ran** and
establishes that in this regime supply *form and dose* dominate *ranking* — a real finding with a
control the prior lacks.

### Attack 2 — "Your legality constraint is unfalsified: you never priced it."

*The reviewer's line.* RECOVER never states where the Earnings-21 or Eka-Medical entity lists came
from, and a reader will assume gold-adjacent harvesting. Against that backdrop, SAEA's legal roster
buys +117 entity tokens at p = .19 while SAEA's own oracle buys −12 pp — so a reviewer concludes
the legality constraint costs essentially the entire effect, and that SAEA is reporting a negative
result dressed as a governance contribution. Worse: "deployment-legal" is asserted, not measured.

*Neutralising control arm.* Promote provenance from a constraint to a **measured experimental
axis** — the *price-of-legality ladder* — run on the identical n=44 vehicle, identical supply form,
matched token budget, four levels:
(a) zero; (b) dataset-shipped metadata roster (SAEA's legal level, zero gold);
(c) auto-NER-over-baseline-hypotheses roster — RECOVER's own Common Voice recipe, still zero gold,
still deployment-legal, and the level most competitors sit at implicitly;
(d) gold-entity roster (oracle upper bound, discovery-only, never a claim).
Report the (d)−(b) and (c)−(b) gaps as pre-registered quantities regardless of sign. This converts
"we obeyed a rule" into "we are the only people who measured what the rule costs", and it forces
every prior — RECOVER included — to declare which rung it is standing on. Level (c) is also the
cheapest real upgrade path if (b) stays underpowered.

### Attack 3 — "Your supply gain is confounded with hypothesis diversity you never harvested."

*The reviewer's line.* RECOVER's stated premise is that a single 1-best decode destroys the signal —
"if an entity is deleted or heavily corrupted in the 1-best ASR output, the LLM often lacks the
signal to recover the term" — and that N=5 temperature-sampled hypotheses restore it; their gains
are recall-driven (+11.6 pp on Earnings-21). SAEA's zero baseline is a *single greedy decode*. A
reviewer will say the roster gain is really an evidence-starvation artifact: five sampled decodes
from the frozen core, fused with no external supply at all, would recover most of it for free and
require no acquisition plane.

*Neutralising control arm.* Add a **multi-hypothesis-only control and a crossed cell**: (i) N
sampled decodes from the frozen omni core fused by an entity-agnostic rule (majority-vote /
longest-hypothesis), no external supply, at matched compute; (ii) multi-hypothesis + roster. If the
roster gain survives on top of (i), the supply claim is additive and defensible; if it does not,
SAEA learns it before the n=44 block is spent.

*Pre-armed rebuttal, from RECOVER's own numbers.* On **Earnings-21 specifically**, RECOVER's four
fusion strategies land at E-WER 15.59 / 15.85 / 15.90 / 15.90 — a spread of 0.31 pp — and plain
**1-Best already achieves 33.2 % RWERR against LLM-Select's 33.4 %**. On the exact carrier SAEA
uses, hypothesis diversity buys ~0.2 pp of a 33 pp effect; the constrained retrieval-plus-edit
supply is doing essentially all the work. SAEA can quote this to close Attack 3 cheaply, while
still running control (i) to make the rebuttal its own rather than borrowed. (Caveat: this holds on
Earnings-21; on ATCO2 and ContextASR the fusion choice matters a lot, and on ATCO2 merge-based
fusion is actively destructive, +15.8 pp WER.)

### Cross-cutting head-to-head hazard (not an attack, a framing risk)

RECOVER's Earnings-21 LLM-Select reaches **33.4 % relative E-WER reduction with a non-oracle
list**, while SAEA's *oracle* supply reaches entity-WER 32 → 20 (~37.5 % relative). A reviewer who
does not read carefully will place SAEA's ceiling next to RECOVER's operating point and conclude
SAEA is dominated. The defences must be stated up front, not in rebuttal: (i) different core —
Whisper-small + GPT-4o (two models, one of them frontier proprietary) vs a single frozen local
Qwen3-Omni GGUF with **no second answering LLM**; (ii) different E-WER definitions and
segmentation (RECOVER: ~1-min clips, 6,535 entity reference tokens; SAEA: 8,284-token entity
ledger); (iii) RECOVER reports no CIs, no significance tests, single-run cells; (iv) RECOVER's
Earnings-21 list provenance is unstated. Recommend SAEA never print a bare cross-paper number
comparison without all four caveats attached.

---

## 6. Newer work citing or extending RECOVER

**No citing work found.** Three bounded searches plus a Semantic Scholar lookup (404 for this ID)
returned nothing that cites arXiv 2603.16411. Expected: it is a March 2026 preprint, under review,
with no code release and no institutional amplification.

Newer *adjacent* work in the same lane, ranked by threat to SAEA's surviving differentiation:

1. **arXiv 2607.26410 — "Voice Memory for Agentic Speech Recognition"** (Chao-Han Huck Yang,
   Zih-Ching Chen, Piotr Zelasko, Zhehuai Chen, Jagadeesh Balam, Boris Ginsburg — NVIDIA),
   29 Jul 2026. Preprint + technical report, **open source on Hugging Face**. Inference-only, no
   weight changes; a **frozen corrector** reads one per-domain `memory.md` and decides
   **per utterance whether to act or abstain**; an asynchronous optimiser revises the memory file
   through **bounded edits** gated on measured improvement; listener–thinker architecture coupled
   only through the memory. Headline: unconstrained generative error correction breaks correct
   tokens in **up to 64 % of its edits**, reduced to **35 %**; WER 8.40 → 3.40 on air-travel
   commands, 12.69 → 10.46 on CHiME-4 far-field; ten HyPoradise domains plus financial news.
   **This is the single biggest threat identified in this cluster.** It occupies, simultaneously:
   training-free frozen-core correction, an explicit **abstention/routing** decision, **bounded
   edits**, and — critically — **harmful-edit accounting as a headline metric**. Harmful-edit
   accounting was one of the two remaining pillars of SAEA's differentiation after the C3 VOID.
   It does not appear to be speech-conditioned in its routing, does not do provenance/legality, and
   its memory-file provenance (gold vs unlabeled dev) is unresolved from the abstract page.
   **Recommend a dedicated deep-read cluster on this paper before N2 is finalised**, with
   memory-file provenance and the exact abstention mechanism as the two must-answer questions.
2. **arXiv 2606.13464 — "Ontology Memory-Augmented ASR Correction for Long Text-Speech Interleaved
   Conversations"** (Xinxin Li, Huiyao Chen, Meishan Zhang et al.), 11 Jun 2026. Dynamically
   updatable ontology memory of entities / terminology / variants / relations as retrievable nodes;
   claims "more selective and evidence-grounded corrections"; RAMC-Corr (from MAGIC-RAMC); improves
   9 of 10 backbone-setting combinations. Adjacent on *organisation* (ORG) and selectivity; not
   speech-conditioned, not legality-aware.
3. **arXiv 2607.28175 — "AgenticASR"** (Zixuan Jiang et al., SJTU), 30 Jul 2026. Audio-to-clean-text
   disfluency and self-correction resolution with continual revision over streams; AASR-Bench.
   Different problem (readability, not entity recovery); low overlap, but it does establish
   "agentic ASR" as a crowded 2026 term — SAEA should avoid leaning on that word for novelty.
4. **arXiv 2606.24915 — "Error-Aware TF-IDF Retrieval-Augmented Generation for ASR Error
   Correction"** (Jafari-Raddani, Qom Univ. of Technology), 19 Jun 2026. TF-IDF with a sparse
   diagonal penalty from historical errors; Gemini 2.0 Flash-Lite; Persian FLEURS
   (3,000 train / 873 test); EA-HR 53.7 → 90.9, WER 23.06 → 18.83. No Earnings-21, no harm
   accounting. Low overlap, but another instance of error-aware retrieval ranking (relevant to
   Attack 1's ranked-roster arm).
5. **arXiv 2605.29430** — "Towards Human-Like Interactive Speech Recognition with Agentic Correction
   and Semantic Evaluation" — surfaced in search, not fetched this session. Flag for a later pass.

Older direct priors in RECOVER's lane, useful for SAEA's related-work map:
Apple's **arXiv 2409.06062** "Retrieval Augmented Correction of Named Entity Speech Recognition
Errors"; **DeRAGEC** arXiv 2506.07510 (denoising NE candidates with synthetic rationale);
**arXiv 2508.20700** "Generative Annotation for ASR Named Entity Correction". Note RECOVER's own
bibliography does **not** cite Apple 2409.06062 or DeRAGEC — its related-work coverage of
retrieval-augmented entity correction is thin, which is both a weakness of the prior and a reason
SAEA should not rely on RECOVER's reference list as a survey.

---

## 7. Bottom line for the SAEA plan

- **N1 (routing gate) survives cleanly.** RECOVER has no routing at all and cannot argue against it;
  but SAEA must now answer "why route when unconditional supply is 1 call/segment?" — the answer has
  to be harm-bounding and token cost, which makes N1 and harmful-edit accounting one argument, not
  two. Voice Memory (2607.26410) is already making a version of that argument.
- **N2 survives but must grow two cells** — a ranked-roster arm at matched tokens (Attack 1) and a
  multi-hypothesis-only control (Attack 3) — and should reframe provenance as a measured
  price-of-legality ladder (Attack 2). Without these, N2 reads as the unranked control cell of a
  published system.
- **The C3 VOID gains an independent corroborator** (RECOVER refuses to let an LLM verify an LLM and
  hard-codes a deterministic filter instead) **and a scope correction** (the failure may be specific
  to whole-reference supply form, not to verification as such).
- **"Audio-grounded verification" and "ceiling/oracle forensics" are the two cleanest unoccupied
  areas** relative to RECOVER; "harmful-edit accounting" is contested as of 29 Jul 2026 and needs
  the Voice Memory read before SAEA leans on it.
- **HER/RIR lineage citation must now include RECOVER's Table 3** (corpus-level entity C/S/D/I
  deltas) alongside survey arXiv 2508.07285. No metric-novelty claim remains available.
- **RECOVER is not reproducible inside SAEA** (second answering LLM, frontier proprietary
  dependency, no code). It is a citation and a comparison hazard, not an implementable baseline.
