# Cluster B — Post-ASR Correction Metrics + Memory-Augmented Editing

Deep-reading and adversarial check, 2026-08-16 (evening session, local time UTC+8).
Scope: SAEA (speech-aware evidence acquisition). Read-only sweep; this file is the only artifact
written. No repository under `studies/` was touched. English only.

Headline for the impatient: **our metric names HER and RIR are already taken, with the same
acronyms and near-identical semantics, by NVIDIA's Voice Memory (arXiv 2607.26410, 2026-07-29).**
And **the "targeted supply vs zero-context, with an oracle ceiling, on Earnings21" experimental
frame is already published** (arXiv 2509.19567). Both are survivable, neither is ignorable, and
one of the parent brief's pinned assumptions (that the Edit Rate / Improve@Edit / Worsen@Edit
lineage lives in survey 2508.07285) is **factually wrong** and must be repaired before it reaches
a preregistration.

---

## 1. Fetch log

All access via WebSearch / WebFetch. No logins, no paid APIs. Times are local (UTC+8).

| # | Time | Type | Query / URL | One-line result |
|---|------|------|-------------|-----------------|
| 1 | 20:56 | mkdir | `wiki/survey/workbench/2026-08-16-deep-reading-adversarial-check/` | Created empty; this file is the sole content. |
| 2 | 20:57 | fetch | `https://arxiv.org/abs/2607.26410` | CONFIRMED: "Voice Memory for Agentic Speech Recognition", Yang, Chen, Zelasko, Chen, Balam, Ginsburg (NVIDIA), 2026-07-29. Inference-only frozen corrector + per-domain memory file + abstain. |
| 3 | 20:57 | fetch | `https://arxiv.org/abs/2508.07285` | CONFIRMED: "Non-Intrusive Automatic Speech Recognition Refinement: A Survey", Peyghan et al., v1 2025-08-10, v3 2026-05-19. Five-class taxonomy. |
| 4 | 20:58 | fetch | `https://arxiv.org/html/2607.26410v1` | Extracted rho and HER definitions, memory-file composition, abstain rule, optimizer accept rule, N-best-text-only input, HyPoradise setup. |
| 5 | 20:58 | fetch | `https://arxiv.org/html/2508.07285v3` | Taxonomy recovered in full; Sections 5 and 6 truncated by the renderer. |
| 6 | 20:59 | fetch | `https://arxiv.org/html/2508.07285v3#S5` | Still truncated; anchor does not change server-side content. |
| 7 | 20:59 | search | `"Improve@Edit" OR "Worsen@Edit" ASR error correction metric edit rate` | **Lineage correction:** these terms trace to arXiv 2606.13464 (Ontology Memory-Augmented ASR Correction), not to survey 2508.07285. |
| 8 | 20:59 | fetch | `https://arxiv.org/html/2607.26410v1#S3` | rho formula, oracle definition, benign-mass measure, helpful/harmful/missed alignment labelling; "audio-visual memory formation" appears only once, in Limitations, undefined. |
| 9 | 21:00 | fetch | `https://arxiv.org/abs/2606.13464` | Abstract + authorship (Li, Chen, Zhang, Li, Chen, Ren, Dong, Hu, Zhang), 2026-06-11. Ontology memory over conversation history; RAMC-Corr dataset. |
| 10 | 21:00 | fetch | `https://ar5iv.labs.arxiv.org/html/2508.07285` | **Sections 5 and 6 recovered** where arxiv.org/html failed. Full metric list and all three research gaps. |
| 11 | 21:00 | fetch | `https://arxiv.org/abs/2605.29430` | "Agentic ASR" (Jiang et al., 2026-05-28); introduces S2ER semantic error rate; no edit-quality metric. Peripheral. |
| 12 | 21:01 | fetch | `https://arxiv.org/html/2606.13464v2` | Edit Rate / Improve@Edit / Worsen@Edit operational definitions; ontology memory fields; training-free frozen backbones; text-only corrector; top-10 retrieval. |
| 13 | 21:01 | search | `training-free prompt-based contextual biasing entity list frozen speech LLM no fine-tuning named entity ASR 2026` | Surfaced 2309.00723 (ICASSP 2024 prompt biasing, no fine-tuning) and 2601.15397 (Beyond Prompting / LOGIC, 2026-01). |
| 14 | 21:01 | fetch | `https://arxiv.org/abs/2309.00723` | Sun et al., ICASSP 2024. Prompted LLM rescoring with a biasing list, no fine-tuning at rescoring; 17.8% rel WER with bias list. |
| 15 | 21:02 | fetch | `https://arxiv.org/abs/2601.15397` | Stream aborted (no content). |
| 16 | 21:02 | fetch | `https://arxiv.org/pdf/2601.15397v1` | LOGIC (Peidong Wang, 2026-01-23): logit-space biasing on a frozen speech LLM; states prompt biasing fails past ~50–100 bias entries (attention dilution, token budget). |
| 17 | 21:02 | search | `confidence-gated adaptive retrieval when to retrieve ASR correction contextual biasing trigger uncertainty speech entity 2026` | Prior art exists for confidence-activated / entity-detector-gated biasing (2306.00804 lineage); surfaced BR-ASR 2505.19179 and RAG context discovery 2509.19567. |
| 18 | 21:02 | fetch | `https://arxiv.org/abs/2505.19179` | BR-ASR (Gong et al., InterSpeech 2025): bias retrieval to 200k entries; retriever is **trained** (contrastive + curriculum); always retrieves, no gate. |
| 19 | 21:02 | fetch | `https://arxiv.org/pdf/2509.19567` | Retrieved but Earnings21 specifics not extractable from the PDF text layer. |
| 20 | 21:03 | fetch | `https://arxiv.org/abs/2509.19567` | **Verbatim abstract obtained. Evaluates on TED-LIUMv3, Earnings21, SPGISpeech; retrieval context −17% WER vs no-context; oracle context −24.1%.** |
| 21 | 21:03 | fetch | `https://arxiv.org/html/2509.19567v2` | Retrieval pool = generic 466,358-word public English vocabulary (Kaggle 479k + NLTK), not corpus-derived; conditioned on previous ASR segment text; oracle = non-stopword gold reference tokens; no entity metric, no harm accounting; frozen off-the-shelf MiniLM retriever. |

Search budget: 3 of 3 used (rows 7, 13, 17). Rows 14–21 are follow-up fetches of URLs those
searches returned, not new searches.

---

## 2. Voice Memory (arXiv 2607.26410) — deep read

**Identity.** Chao-Han Huck Yang, Zih-Ching Chen, Piotr Zelasko, Zhehuai Chen, Jagadeesh Balam,
Boris Ginsburg (NVIDIA). Submitted 2026-07-29. Code and demo released via Hugging Face.

**What it is.** A frozen corrector reads an N-best list `H` plus a short Markdown memory file `s`
and emits `y_hat = M(H, s)`, or abstains and keeps the 1-best. A background optimizer edits `s`
and accepts an edit only if it strictly improves a held-out score on a disjoint "selection" split.
No gradients, no weight updates, zero parameters added to the inference path. Their own framing:
"A better agent here is simply a better text file. The policy the file comes to encode is
restraint, knowing which tokens to leave alone."

### 2.1 Their metric definitions, verbatim where obtainable

**Recoverable Information Ratio (rho):**

```
rho = (WER_1-best  -  WER_y_hat) / (WER_1-best  -  WER_oracle)
```

with "rho=1 closes the gap exactly. rho<0 is the damage regime, where correcting is worse than
keeping h_1. rho>1 means the corrector recovers tokens present in no hypothesis." The oracle
"selects, per utterance, the hypothesis in H with the lowest WER against the reference."

**Harmful Edit Rate (HER):** "Align y_hat against h_1 and the reference, then label each token
edit as helpful (fixed a wrong token), harmful (broke a correct token), or missed. HER is the
fraction of all token edits that are harmful."

**Benign mass** (a third diagnostic, ours has no analogue): "the fraction of residual error mass
whose semantic distance falls below a small threshold" — they report 53–68% of residual errors
preserve meaning despite surface difference.

**Novelty posture.** Related Work does **not** attribute HER or rho to any predecessor. Both are
introduced in §3 as the paper's own diagnostic instruments. Limitations concedes only that "rho
and the benign-mass measure depend on the sentence encoder we use."

**Headline numbers.** Unconstrained generative error correction breaks correct tokens in up to
**64%** of edits on financial news (WSJ); Voice Memory reduces this to **35%**. Weighted WER
across ten HyPoradise domains 8.36% -> 7.52%; ATIS 8.40% -> 3.40%; CHiME-4 far-field 12.69% ->
10.46%. Per-domain rho: ATIS 0.96, CV 0.59, WSJ 0.48, CHiME-4 0.21. Correctors: MiniMax-M3 (428B
total / 23B active) primary, Qwen3-30B-A3B breadth, Claude-4.6-Sonnet transfer. Whisper 5-best.
16,108 test samples.

### 2.2 Collision analysis against our pinned HER / RIR

| Axis | Voice Memory | SAEA as pinned | Verdict |
|---|---|---|---|
| Name | Harmful Edit Rate (HER) | Harmful Edit Rate (HER) | **Identical string and acronym** |
| Name | Recoverable Information Ratio (rho) | Recoverable Information Ratio / RIR | **Identical concept, near-identical name** |
| HER denominator | all token edits | our edit aperture | Same family |
| RIR numerator/denominator | 1-best-to-oracle WER gap over N-best | delivered-correct opportunity recovery | **Different denominator** — ours is opportunity-based, theirs is oracle-gap-based |
| Publication date | 2026-07-29 | our pin post-dates it | We are second |

Our reported "RIR 0" on the replay chain and their "rho<0 is the damage regime" are the same
instrument pointed at the same failure. Our VOID result (49/53 replay outputs byte-identical to a
supplied deranged reference) is the extreme case of the phenomenon they quantify at 64% HER for
unconstrained GER.

**This is not a citation footnote. It is a naming conflict.** Publishing "HER/RIR" as local
variants without foregrounding 2607.26410 would read, to any speech reviewer who has seen the
NVIDIA release, as appropriation of an acronym pair from a paper three weeks older than ours.

### 2.3 What its memory does that our episode-local boundary forbids

Four things, and they matter differently:

1. **Cross-utterance accumulation.** `s` is optimized over many training utterances and persists
   across the whole domain. Our supply is assembled per episode from static dataset-shipped
   metadata; nothing an episode learns propagates to the next. Their memory is a *learned*
   artifact; ours is a *looked-up* one.
2. **Gold-supervised offline construction.** The optimizer scores candidate memories against
   **reference transcripts** on train and selection splits. That is gold in the loop — offline,
   but gold. Our N2 rosters use zero gold at any stage.
3. **Held-out acceptance gating.** Edits to `s` are accepted only on strict improvement of a
   held-out score. We have no analogue; our roster content is fixed by provenance, not selected
   by measured benefit.
4. **Behavioural rules, not entity facts.** The memory contains suppression rules ("keep the
   verbatim ASR token; do not normalize", "place 'dollars' after the amount, not '$' before it"),
   explicitly **not** keyword lists, entity rosters, or domain glossaries. Confirmed: the paper
   contains no contextual-biasing injection and no entity roster in the memory.

Item 4 is the single most useful finding in this cluster. **Voice Memory and SAEA-N2 supply
different things.** They supply a learned restraint policy; we supply factual entity evidence.
Item 2 is the second most useful: their legality posture (gold offline, none at inference) is
exactly the posture our **DEMO lane** was proposing, which means the DEMO lane is the part of our
plan most eroded by this paper, while N2 is the part least eroded.

---

## 3. Survey (arXiv 2508.07285) — deep read

**Identity.** Peyghan, Soleimani Roudi, Zouashkiani, Amini, Rajabi, Ghaemmaghami. v1 2025-08-10,
v3 2026-05-19. Title: *Non-Intrusive Automatic Speech Recognition Refinement: A Survey*.
Note: `arxiv.org/html` truncates this paper badly; `ar5iv.labs.arxiv.org` renders Sections 5–6.

### 3.1 Taxonomy — five classes

- **Fusion** — shallow (inference-only log-linear interpolation), deep (gating, partial
  retraining), cold (full ASR retraining).
- **Rescoring** — first-pass (lattice / word-graph), second-pass (n-best re-ranking).
- **Correction** — rule-based & n-gram; NLM-based (encoder-based; decoder-inclusive AR/NAR);
  **LLM-based**; **RAG-integrated**.
- **Distillation** — retraining ASR with external LM knowledge.
- **Training adjustment** — internal LM training, MWE training, label smoothing.

Training-free members of the Correction class: LLM-based prompting in constrained mode ("select
the most probable hypothesis from the n-best list") and unconstrained mode ("rewrite a correct
transcript"), plus PROGRES-style instruction prompting. Everything encoder-based (BERT, FASPell,
SpellGCN, Soft-Masked BERT) and every AR/NAR decoder (FastCorrect 1/2, SoftCorrect, PATCorrect,
PhVEC, PC-MLM) requires training.

**Where SAEA sits.** Correction / RAG-integrated, in the training-free prompting sub-branch, with
one property the taxonomy has no cell for: the corrector *is* the recognizer. Every class in this
survey presumes a separable ASR whose output text is then refined non-intrusively. A frozen omni
core that consumes audio and emits the answer directly is not "non-intrusive refinement of an ASR
model" — it is single-stage conditioning. That is a genuine, statable taxonomic gap, and the
survey's own vocabulary can be used to name it.

### 3.2 The survey's standardized metrics (Section 5), as recovered

- **5.1 Error-rate**: WER `(S+D+I)/N x 100`; **WERR** `(WER_before - WER_after)/WER_before x 100`;
  **CER**, **CERR**; **MC-WER** (medical concept as one atomic "word"); **swf-WER** (stop-word
  filtered); **cpWER** — "measures the fraction of originally erroneous words that are corrected".
- **5.2 Entity**: **EER (Entity Error Rate)**, "the proportion of incorrectly identified
  entities"; **Precision = better/(better+fp)**; **Recall = better/(better+missed)**; **F1**.
- **5.3 Language quality**: LA (Language Acceptability, LM-judged), BLEU, GLEU, Perplexity.
- **5.4 Qualitative**: expert evaluation, side-by-side (SxS).

**The `better / fp / missed` triple in 5.2 is the edit-quality lineage** the brief was reaching
for. It is the same three-way edit labelling Voice Memory calls helpful / harmful / missed.
Precision `better/(better+fp)` is, on the same alignment, `1 - HER`. So HER is not merely
*adjacent* to a surveyed metric — it is the complement of one, under a different name.

**Edit Rate / Improve@Edit / Worsen@Edit do not appear anywhere in this survey.** See §4.

### 3.3 Section 6 research gaps — all three

1. **Text-only limitation.** "A key limitation in the current literature is the predominant use of
   text-only data in refinement methods." ASR text diverges from the formal structures LMs expect,
   causing "overcorrection that inadvertently increases the error rate."
2. **High-error-rate regimes.** Need for approaches that better guide correction "particularly in
   scenarios with high WER, frequent insertions and deletions, and out-of-domain evaluations."
3. **Error classification.** "Only a small number of studies have evaluated the post-refinement
   error types"; the field needs classification of error distributions before and after refinement.

This is materially good news and should change how the VOID is written up. Gap 1 names *text-only
refinement* as the field's central limitation and *overcorrection* as its consequence. Our VOIDED
arm is the direct test of the field's own preferred remedy: we gave the corrector the audio, and
the overcorrection did not go away — the model copied deranged references at identical raw rates
under verify and bias framings (7/9 vs 7/9 windows). **A negative result answering a survey's
first-listed open gap is a publishable object**, and it is far stronger positioned as "we tested
the community's stated fix and it failed under these conditions" than as "our operator did not
work." Gap 3 additionally licenses our harmful-edit accounting as responsive to a named need.

---

## 4. Metric-lineage correction (repair before preregistration)

The brief pins: *"HER/RIR must cite the existing post-ASR edit-quality lineage (Edit Rate /
Improve@Edit / Worsen@Edit, survey arXiv 2508.07285)."* Two errors:

1. **Those three terms are not in 2508.07285.** They originate in **arXiv 2606.13464**, *Ontology
   Memory-Augmented ASR Correction for Long Text-Speech Interleaved Conversations* (Li, Chen,
   Zhang, Li, Chen, Ren, Dong, Hu, Zhang; 2026-06-11). Definitions there, at correction-record
   level: **Edit Rate** = proportion of records where output differs from the ASR hypothesis;
   **Improve@Edit** = "among edited records, the proportion of edits that decrease CER";
   **Worsen@Edit** = "among edited records, the proportion of edits that increase CER".
2. **The nearest prior is neither of those.** It is Voice Memory's HER/rho (§2), which shares our
   acronyms outright, and the survey's `better/fp/missed` Precision/Recall (§3.2), of which HER is
   the complement.

Correct lineage to cite, in priority order: **Voice Memory 2607.26410 (HER, rho) > survey
2508.07285 §5.2 (Precision/Recall over better/fp/missed) > ontology memory 2606.13464 (Edit Rate,
Improve@Edit, Worsen@Edit)**. Any preregistration carrying the old pin is citing the wrong paper
for the wrong terms and missing the one paper that actually collides.

Bonus proximity, worth logging: 2606.13464 is training-free and inference-only across Qwen2.5-7B/
14B/72B, Qwen3.5-4B/9B, Gemma-4-26B-128K, with Qwen2-Audio-7B-Instruct as the ASR; its ontology
memory stores `name, alias, noise, syn, hyp, tag, meta` — i.e. entities, surface variants and
predicted ASR confusions — retrieved top-10 per record via inf-retriever-v1. Its Table 6 finding
is that records with retrieved evidence show "lower Edit Rate and Worsen@Edit than those without
retrieval." That is the same mechanism our N2 hopes for: **supply makes editing more conservative,
not more aggressive.** It is built online from causally accessible dialogue history, explicitly
"not a predefined static knowledge base" — which is the one axis where our static
metadata-provenance roster differs from it.

---

## 5. Answers to the three commissioned questions

### Q1. Is our HER/RIR positioning sufficient, or does an existing metric make ours redundant?

**Not sufficient as pinned. Not redundant either — but the names must go or be explicitly ceded.**

- **Redundancy check on HER.** Our HER and Voice Memory's HER are the same measurement. Under
  the survey's 5.2 framing, both equal `1 - Precision` on the `better/fp/missed` alignment. There
  is no daylight. Claiming any novelty for HER is untenable and was never worth defending.
- **Redundancy check on RIR.** Here there *is* daylight, and it is worth keeping. Voice Memory's
  rho is normalized by the **1-best-to-oracle gap within an N-best list** — it can only measure
  what reranking could in principle have reached. Ours is normalized by **delivered-correct
  opportunities**: cases where the correct evidence was actually supplied to the model. These
  differ whenever supply carries information present in *no* hypothesis; their own note that
  "rho>1 means the corrector recovers tokens present in no hypothesis" shows their denominator
  breaks precisely in the regime our method operates in. **Our RIR is the well-posed instrument
  for supply-conditioned correction; theirs is well-posed for N-best-conditioned correction.**
  That is a real, defensible, small contribution — and it is only visible if we state the contrast.
- **Required action.** (a) Rename to avoid acronym collision — e.g. `HER_edit` cited as
  "Harmful Edit Rate, after Yang et al. 2026" and, for the supply-normalized quantity,
  **Supplied-Evidence Recovery Rate (SERR)** or **Delivered-Opportunity Recovery (DOR)**, defined
  against delivered-correct opportunities and explicitly contrasted with Voice Memory's
  oracle-gap rho. (b) Cite all three lineage sources per §4. (c) State "no metric-novelty claim"
  for the harmful-edit family, and make the *only* metric claim the change of denominator, framed
  as necessary rather than better.

### Q2. Does any surveyed method already do deployment-legal targeted supply WITHOUT training?

**Partially yes — and one paper does it on our own dataset. Our differentiation survives, but it
has moved.** Five relevant precedents, ordered by threat:

1. **arXiv 2509.19567 — RAG-based context discovery for ASR** (Siskos et al., 2025-09-23, rev
   2025-11-19). **Evaluated on Earnings21.** Frozen off-the-shelf MiniLM + FAISS, no training.
   Retrieval pool is a **generic public 466,358-word English vocabulary** (Kaggle 479k + NLTK
   232k) with definitions — no gold, fully deployment-legal. Retrieval is conditioned on the
   **previous k ASR segment transcripts**. Reports **−17% WER vs no-context, oracle context
   −24.1%**, oracle defined as non-stopword gold reference tokens. This is our N2 skeleton —
   supply vs zero baseline with an oracle ceiling, on our corpus — already in the literature, with
   a *larger* relative gain than our n=10 pilot (2.3% rel; 12.38 -> 12.09). Also evaluates the two
   alternatives we care about: LLM-prompted context generation, and post-recognition LLM
   correction.
   **What it does not do:** conditions on *text*, never on the speech signal; injects into a
   classical CB decoder, not an omni core prompt; uses a generic dictionary, not entity-typed
   provenance metadata; reports **no entity-level metric**; performs **no harm/degradation
   accounting** for wrong context.
2. **arXiv 2309.00723 — Contextual Biasing of Named-Entities with LLMs** (Sun et al., ICASSP
   2024). Prompted biasing list + few-shot at second-pass rescoring, "without fine tuning during
   rescoring"; 17.8% rel WER from the bias list, 9.6% from few-shot. Prompt-supplied entity lists
   with a non-fine-tuned LLM are five-year-old prior art. Their multi-task and dynamic-prompting
   variants do train.
3. **arXiv 2606.13464 — Ontology memory** (§4). Fully training-free, frozen prompted backbones,
   retrieved entity/alias/confusion evidence, and the conservatism effect we predict. Built from
   in-conversation history rather than external metadata.
4. **arXiv 2505.19179 — BR-ASR** (Gong et al., InterSpeech 2025). Scales bias retrieval to 200k
   entries, SOTA B-WER 2.8%/7.1% at 2000 bias words. **Retriever is trained** (speech-and-bias
   contrastive learning + dynamic curriculum), so it fails our training-free constraint — but note
   its retriever is **speech-conditioned**, which is the same idea as our C2 routing claim,
   realized with training.
5. **arXiv 2601.15397 — LOGIC** (Peidong Wang, 2026-01-23). Frozen speech LLM, bias injected in
   **logit space** via a dedicated encoder. Requires logit access, which our API-only boundary
   forbids — a clean exclusion. Independently corroborates our full-bag finding: prompt-based
   biasing "scales poorly beyond moderate list sizes", degrading past **50–100 entries** from
   "token budget constraints and attention dilution", and GEC approaches fail there.

**Net.** Training-free targeted supply exists. Deployment-legal supply pools exist. Frozen
speech-LLM biasing exists. What no single reachable prior combines: **(a) supply selected by
conditioning on the speech signal itself rather than on prior text or a trained retriever,
(b) provenance-typed metadata rosters as the legal supply pool, (c) an API-only frozen omni core
with no logit access, (d) co-primary entity-WER accounting, and (e) harmful-edit accounting of
what the supply breaks.** (b)+(e) are where the differentiation load now sits, exactly as the
brief anticipated — but (a) must be demonstrated, not asserted, because 2509.19567 already owns
the text-conditioned version and BR-ASR already owns the trained speech-conditioned version.

### Q3. Three attacks on our plan from this vantage, and neutralizing controls

**Attack 1 — "Your metrics are NVIDIA's, three weeks late."**
A reviewer who knows 2607.26410 sees HER and RIR, in a frozen-corrector zero-parameter
inference-time paper, and concludes we lifted the instrument panel. The VOID narrative makes it
worse, not better: their 64% -> 35% HER result *is* the over-correction story, and our parroting
result looks like a special case they already framed.
*Controls.* (i) Rename per Q1 and cite 2607.26410 in the metrics section, not the related work
tail. (ii) State the denominator contrast explicitly — oracle-gap vs delivered-opportunity — and
show a case where the two diverge; their own "rho>1" caveat hands us the argument. (iii) Reframe
the VOID as a *replication under a modality they did not test*: their corrector never sees audio
("frozen corrector reads H and an optional memory s"), ours does, and the harm persists. Same
instrument, different modality, independent finding. (iv) Pre-empt the DEMO lane comparison
in-text, since Voice Memory is the stronger version of that idea (§2.3 items 2–3).

**Attack 2 — "Retrieval-vs-oracle on Earnings21 is done, and they beat you."**
2509.19567 reports −17% WER from automatic context vs −24.1% oracle. Our pilot reports 12.38 ->
12.09 (2.3% rel) with oracle 10.88 (12% rel), p=.19 at n=10, going to n=44. A reviewer asks why
the newer method with a frozen omni core recovers less than a 2025 FAISS-plus-CB-decoder pipeline.
*Controls.* (i) Do not let effect-size comparison be apples-to-apples by default — their oracle is
*non-stopword gold reference tokens* (a far richer, gold-derived context than any deployment-legal
roster) while ours is a legal roster ceiling; report both ceilings and make the ceiling difference
the point. (ii) Make **entity-WER the headline, not macro WER** — they report no entity metric at
all, our 8284-token entity ledger and the +117 entity tokens at n=10 are on ground they never
covered; macro WER is where we lose and entity-WER is where we are uncontested. (iii) Add their
generic-vocabulary retrieval as a **named comparator arm** in the N2 registration if budget
allows, or at minimum as a documented non-run comparator with the reason stated. (iv) Cite them as
prior art establishing the frame; being second on the frame while first on the legality axis and
the entity axis is defensible, being silent about them is not.

**Attack 3 — "Your routing gate is confidence-gated biasing, which is old, and your prompt supply
is known to break past 100 entries anyway."**
Confidence-activated decoders and entity-detector gating that enable/disable biasing per utterance
are established (2306.00804 lineage; surfaced directly in search 17). Meanwhile LOGIC states
prompt biasing fails past 50–100 entries, and BR-ASR reaches 200k entries with a trained
speech-conditioned retriever. So N1 risks reading as a reinvention of confidence gating, and N2
risks being capped at a list size the field already routes around — with the field's two answers
(logit access, trained retriever) both forbidden to us.
*Controls.* (i) Make N1's contribution **measurement, not mechanism** — the brief's own forensics
(guard-chain perfection worth −0.28pp vs static oracle supply −12pp; roster-band flag surfacing
~3% of reachable error mass) is a *flag-recall-vs-error-mass* accounting that none of these papers
report. Publish the recall curve and the error-mass aperture; that is the novel object, and prior
gating work is the baseline it measures. (ii) Gate on **speech-side evidence** (acoustic/entity
cues from the signal) rather than text confidence, and say so — that is the C2 claim and the only
axis BR-ASR takes with training and 2509.19567 does not take at all. (iii) Turn the 50–100-entry
ceiling from a threat into a **registered prediction**: our full-bag null (no gain at 4x tokens)
already reproduces LOGIC's attention-dilution claim independently, so preregister a roster-size
sweep and cite the convergence. Compact rosters are then a *principled consequence of a known
scaling law*, not a convenient choice. (iv) Record the API-only/no-logit-access constraint as an
explicit scope declaration so LOGIC reads as out-of-reach-by-construction rather than as an
uncited stronger baseline.

---

## 6. Actions this cluster forces

1. **Repair the metric pin** in any live registration: wrong source paper, wrong terms, missing the
   colliding paper. §4 has the corrected lineage.
2. **Rename HER/RIR** and add 2607.26410 to the metrics section. Keep the
   delivered-opportunity denominator; that part is genuinely ours.
3. **Add 2509.19567 to N2's related-work and comparator design** before the n=44 block registers.
   It shares our corpus and our experimental frame.
4. **Re-scope the DEMO lane.** Voice Memory is the same legality posture executed at scale with an
   acceptance-gated optimizer. If DEMO proceeds, it needs a stated delta against it — most
   plausibly the mandatory reject-case demonstrations plus audio in the demonstration, neither of
   which Voice Memory has.
5. **Rewrite the VOID as a response to survey gap 1.** "Text-only refinement causes
   overcorrection" is the field's stated open problem; we tested the audio-grounded remedy and it
   failed. That framing is stronger, better cited, and independently corroborated by Voice
   Memory's 64% harmful-edit baseline and LOGIC's attention-dilution result.

---

## 7. Reliability notes

- `arxiv.org/html/2508.07285v3` truncates before Section 5. Sections 5–6 in this digest come from
  `ar5iv.labs.arxiv.org/html/2508.07285`; treat the metric strings as high-confidence but re-verify
  exact formulas against the PDF before quoting them in a submission.
- Voice Memory per-domain HER values are read off Figure 2 and are approximate (WSJ ~0.64 -> 0.35);
  the 64% / 35% figures are stated in the abstract and are exact.
- "audio-visual memory formation" appears exactly once in Voice Memory (Limitations) with no
  definition; do not build an argument on it without re-reading the released artifacts.
- Voice Memory Table 3 rho values beyond ATIS/WSJ/CHiME-4/CV were not enumerated in the extraction.
- 2601.15397's "50–100 entries" threshold and "40–60% token overhead reduction" come from a PDF
  text extraction; re-verify before citing a number.
- One earlier extraction of 2509.19567 (fetch 19/PDF) returned a plausible-sounding but
  unsupported description of its retrieval corpus; the §5 account here uses the HTML rendering
  (fetch 21), which is specific and internally consistent (466,358 words; Kaggle+NLTK; MiniLM;
  FAISS). Prefer fetch 21 wherever the two disagree.
