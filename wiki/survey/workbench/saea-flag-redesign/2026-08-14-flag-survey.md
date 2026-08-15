# Reference-free word-level ASR error detection, targeted at entity/rare-word errors

Survey note for the listen-score-replay flagging problem.
Date: 2026-08-14. Sources: arXiv API sweep (~55 queries, ~350 abstracts screened) plus
full-text reads of 7 papers. **Evidence marking:** claims tagged `[FT]` were verified against
paper full text (ar5iv/arXiv HTML); claims tagged `[ABS]` come from the abstract only.

Motivating observation being explained: on real earnings-call decodes from a frozen
Qwen3-Omni, token-logprob flags fired only on function-word/boundary text ("with a",
"for the", "increase by") with **zero** overlap against the actual rare-entity errors
(drug/person/company names) in 17/17 windows.

---

## Q1. Where raw token logprobs fail as error predictors

### 1.1 The headline mechanism: logprob measures *total predictability*, not *acoustic grounding*

The single strongest literature explanation for our failure mode is the decomposition made
explicit by the internal-language-model (ILM) line of work and, more recently and more
directly, by the contrastive-decoding-for-audio-LLM line.

An autoregressive speech model's token posterior `p(y_t | audio, y_<t)` implicitly contains an
internal LM prior over `y_t | y_<t`. ILME/HAT/density-ratio methods exist precisely because
that prior must be *subtracted* to recover the acoustic contribution
(Variani et al. 2020, HAT, arXiv:2003.07705 `[ABS]`; Meng et al. 2021, ILMT,
arXiv:2102.01380 `[ABS]`; Zheng et al. 2022, LODR, arXiv:2203.16776 `[ABS]`).
Zeineldeen et al. 2026 (arXiv:2607.05612) restate this for modern systems: "the decoder's
internal LM must be considered when interpreting the effect of external LM quality" `[ABS]`.

The consequence for error *detection* is direct and, in our setting, decisive:

- A **function word in fluent context** ("with a" / "for the") has a high LM prior but the
  prior is *split* across several near-equivalent continuations; posterior mass divides, the
  logprob drops, and the flag fires — yet no error exists, because the alternatives are
  semantically interchangeable.
- A **hallucinated common-word substitution for a rare entity** has a *concentrated* LM prior
  ("tears at a peptide" for "tirzepatide"); the prior alone can carry the posterior to high
  confidence with essentially zero acoustic support, so no flag fires.

The audio-LLM literature now states this as the governing failure mode in exactly these words:
LALMs "frequently hallucinate by **overriding acoustic evidence with language priors**"
(Grace, Huo & Wang 2026, arXiv:2607.00247 `[ABS]`); speech LMs have "a tendency to
**prioritize linguistic priors over acoustic features**" (Chen et al. 2026, CAAD,
arXiv:2606.23052 `[ABS]`); unified LALM decoders exhibit a "temporal smoothing bias" where
"transient acoustic cues may be underutilized in favor of temporally smooth context that is
**better supported by language priors**" (Li et al. 2026, TCD, arXiv:2604.15383 `[ABS]`).

**This is the strongest available answer to "why did logprobs miss the entities": the token
logprob is the wrong quantity. It scores predictability-given-context, and it is highest
exactly where the LM prior is strongest — which is where confidently-wrong entity
substitutions live.**

A closely related, independently-observed corollary from the ASR-error-detection literature:
LM-based error detectors and disfluency detectors collide because "both error detection and
disfluency detection tasks attempt to **identify tokens at statistically unlikely positions**"
(Park et al. 2021, arXiv:2108.01812 `[ABS]`). Statistical unlikeliness is not error-hood.
Our function-word flags are the textbook instance.

### 1.2 Softmax overconfidence is worst exactly in the high-confidence region

Li, Qiu, Zhang et al. 2020 (CEM, arXiv:2010.11428) `[FT]` analyse attention-based E2E softmax
confidence on LibriSpeech and report:

- Precision-recall curves for raw softmax show a **"sharp downward spike at the high-confidence
  region"** — i.e. the false positives (confident errors) concentrate precisely where
  confidence is highest — whereas a trained CEM degrades monotonically.
- Softmax AUC 0.976 / 0.912 (test-clean / test-other) vs CEM 0.990 / 0.958; NCE 0.166 / 0.172
  vs CEM 0.344 / 0.275. With LM fusion the softmax NCE collapses to 0.103 / 0.109 vs CEM
  0.337 / 0.263 — **LM fusion actively degrades softmax confidence**, the same prior-dominance
  effect as §1.1.
- Regularisation that improves WER worsens calibration: removing label smoothing improves AUC
  (0.985 vs 0.976) but hurts NCE; removing SpecAugment improves NCE but blows up WER
  (10.8% vs 7.5%). Calibration and accuracy are optimised against each other.
- **Deletions are explicitly outside the scope of softmax confidence** (their CEM targets are
  built by edit-distance alignment: correct = 1, substitution/insertion = 0, deletions excluded
  as future work). A deleted rare entity produces *no token to score at all*. This matters for
  us: some entity errors will be invisible to any per-token score by construction.

Quantitatively on modern models: Whisper assigns confidence > 0.7 to **10–20% of incorrectly
predicted tokens** at low SNR (Huo, Zhang & Tang 2025, arXiv:2509.07195 `[ABS]`).

Ogawa et al. 2023 (arXiv:2312.14609) `[ABS]` add the class-imbalance framing: at ~5% token
error rate you are "detecting infrequent incorrect tokens from mostly correct token sequences",
and they report that Transformer-based confidence models "**greatly underestimate incorrect
tokens**" — i.e. the default behaviour of a text-context-heavy scorer is to trust fluent output.

### 1.3 Entropy vs logprob, top-k margin, temperature

Oneata, Caranica, Stan et al. 2021 (arXiv:2101.05525) `[FT]` is the cleanest benchmark:

- Features: `log max p` vs negative entropy `p·log p`; improvements via learned **temperature
  scaling**, MC **dropout** (64 passes), and 4-model ensembles.
- Token→word aggregation: **sum > min > average**, and the reason matters for us —
  "length-invariant measures are detrimental" since longer words are inherently more
  error-prone. Their Figure 2 shows error fraction rising with word length. **Entities are long
  words; average-pooling a rare entity's subtokens systematically hides its risk.**
  Min-pooling suits entropy features; sum-pooling suits log-prob features.
- Numbers (TED, 13.3% WER): baseline logprob+sum AUPR_err 39.97 / AUROC 79.95; best
  (neg-entropy + sum + temperature + dropout) AUPR_err 43.59 / AUROC 85.51. Log-prob features
  beat entropy features in-domain; comparable OOD (CommonVoice, 28.6% WER).
- **Caveat they state themselves:** they do *not* analyse substitutions vs deletions/insertions
  separately, and do *not* examine word frequency or function/content word effects. So the
  literature's flagship word-confidence benchmark is silent on exactly our question.

Laptev & Ginsburg 2022 (arXiv:2212.08703) `[ABS]` show normalised/aggregated per-frame
**entropy** measures are "up to 2 and 4 times better than confidence estimation based on the
maximum per-frame probability" at detecting incorrect words (Conformer-CTC / RNN-T), with a
"wider effective threshold range" — entropy separates the correct/incorrect distributions
better than max-prob at equal cost.

Score-and-**rank** features beat raw softmax on calibration: SR-CEM reports token-level MCE
4.50% / ECE 0.30% vs softmax 20.04% / 1.75%; word-level 8.17% / 0.35% vs 17.91% / 1.67%
(Jia & Van hamme 2026, arXiv:2607.29299 `[ABS]`). The relevant signal is *where the emitted
token sits in the top-k ordering and how far it is from its neighbours*, not its absolute prob.

From the LLM side, restricting entropy to **content-bearing** tokens is itself the trick:
normalised entropy of the top-K logits at the *first content-bearing answer token* of a single
greedy decode reaches mean AUROC 0.820, beating semantic self-consistency (0.793) and
surface-form self-consistency (0.791) (Gabriel 2026, arXiv:2605.05166 `[ABS]`). This is direct
support for gating the uncertainty read by token *type*.

### 1.4 Ceiling check: how hard is this, honestly

HALAS (Barański et al. 2026, arXiv:2606.23048) `[FT]` is the closest thing to our exact
setting — human span-level hallucination annotation on **real, unprocessed earnings-call
recordings**, 7 ASR systems, Cohen's κ = 0.87:

- Proxy metrics (WER/CER/insertion rate/BERTScore/SeMaScore) reach **AUC 0.7–0.8**;
  GPT-2 perplexity and length ratio reach **AUC ≤ 0.62** — text-LM surprisal is the *weakest*
  family, again consistent with §1.1.
- Best trained detectors (logistic regression on Whisper decoder-layer embeddings) reach only
  **F1 53.1%** (single layer) / **56.1%** (multi-layer); an XGBoost over proxy metrics reaches
  ROC-AUC 0.829–0.835.
- LLM judges *with ground-truth reference access* did worse: GPT-4o mini F1 40.7%
  (P 30.1 / R 62.6); Gemini 2.0 Flash F1 41.6% (P 50.0 / R 35.7).
- **"Hallucinations also occur for almost correctly transcribed speech (low WER)."**

Read this as a calibration of ambition: reference-free error flagging on earnings calls is a
~0.8 AUC / ~0.55 F1 problem for *trained* detectors. A training-free flagger that reaches
useful precision on a *narrow, targeted* class (entities) is a reasonable goal; a general
word-level error detector is not.

Supporting domain facts: Earnings-21 (Del Rio et al. 2021, arXiv:2104.11348) `[ABS]` was built
for exactly this — 39h of entity-dense earnings calls — and its finding is "ASR accuracy for
certain NER categories is poor". Borgholt et al. 2025 (arXiv:2509.24478) `[ABS]` note that
benchmark "gains are often driven by frequent words with limited semantic weight", while
"errors in rare terms, named entities, and domain-specific vocabulary ... remain hidden by
aggregate metrics". ProfASR-Bench (Piskala 2025, arXiv:2512.23686) `[ABS]` evaluates
**Qwen-Omni** alongside Whisper on finance/medical/legal entity-rich speech and reports a
"context-utilization gap": lightweight textual context changes average WER little **even with
oracle prompts** — relevant warning for any prompt-only correction stage downstream of our flag.

---

## Q2. Entity/rare-word-TARGETED error detection

### 2.1 Entity-first: find entity spans, then score only those

This is the dominant and best-validated pattern, and it inverts our current pipeline.

- **Lei et al. 2024** (arXiv:2409.15353) `[ABS]` is the canonical training-free-ish recipe:
  (1) let the LLM detect named entities in the speech *with no context*, (2) use each detected
  entity as a query to retrieve **phonetically similar** entities from a personal database,
  (3) re-decode context-aware. Up to **30.2% relative WER** and **73.6% relative named-entity
  error rate** reduction on a voice-assistant task, and "by design avoids prompting the LLM
  with the full named entity database". Precision/false-trigger analysis is not in the abstract.
- **Whisper: Courtside Edition** (Ron, Gilboa & Dubnov 2026, arXiv:2602.18966) `[ABS]` runs LLM
  agents for domain identification, NER, and *jargon detection* over the draft transcript, then
  feeds compact prompts back to the decoder: 17.0% relative WER reduction on NBA commentary
  (0.217→0.180, p<0.001), improving 40.1% of segments and degrading 7.1% — a usable
  precision/damage ratio for a re-decode loop.
- **ED-CEC / PMF-CEC** (He & Toda 2025, arXiv:2506.11064) `[ABS]` is the closest thing to an
  explicit error-detection-then-correct module for rare words, and it reports the failure mode
  we should expect: "the previous ASR error detection module suffers from **overdetection**",
  fixed by a retention-probability threshold that discards edits below a confidence floor.
- **Trinh, He & Whitehill 2025** (arXiv:2506.10779) `[ABS]`: LLM revision of NEs using both
  phonetic and semantic context, up to 30% relative WER reduction on NEs (MIT OpenCourseWare).
- **DeRAGEC** (Im et al. 2025, arXiv:2506.07510) `[ABS]` is explicitly **training-free**: it
  filters noisy retrieved NE candidates using phonetic similarity + augmented definitions via
  in-context learning, "requiring no additional training", 28% relative WER reduction vs raw ASR.

### 2.2 Lexical/OOV/frequency cues on the draft text

- OOV detection from an external LM is a classic, and the finding transfers: acoustic-to-word
  models "tend to **falsely recognize OOV words as words in the vocabulary**", and an external
  text-only LM detects them better than the recogniser itself (Inaguma et al. 2019,
  arXiv:1909.09993) `[ABS]`. Our analogue: a common-word substitution for a rare entity is the
  in-vocabulary shadow of an OOV event.
- Capitalisation is a usable free cue on LLM-decoded drafts: text injection improves
  capitalisation "for long-tail data" (Bijwadia et al. 2023, arXiv:2308.07395) `[ABS]`;
  entity-preserved context-aware transcription treats entity formatting/capitalisation as the
  same problem as entity recognition (Altinok 2025, arXiv:2506.22858) `[ABS]`.
- Error-aware TF-IDF (Jafari-Raddani 2026, arXiv:2606.24915) `[ABS]` builds a sparse diagonal
  penalty matrix over **historical misrecognitions** so retrieval prioritises documents
  containing known high-risk error forms — error-aware hit rate 53.7% → 90.9%. This is the
  "lexicon of draft-word occurrences" idea in retrieval form.

### 2.3 Phonetic-distance methods (G2P of draft vs candidate entity)

- **PED-NEC** (phonetic-edit-distance named entity correction) is the standard baseline family;
  **DANCER** (Wang et al. 2024, arXiv:2403.17645) `[ABS]` reports it degrades as the NE list
  grows because homophone ambiguity explodes, and adds entity *descriptions* + dense retrieval
  to disambiguate: −7% CER on AISHELL-1 NEs vs PED-NEC, and −46% relative on a
  high-phonetic-confusion Homophone set.
- Retraining-free NE customisation via **phoneme similarity estimation** improves target-NE CER
  by 35.7% relative (Sudo, Hata & Nakadai 2023, arXiv:2305.17846) `[ABS]`.
- **Articulatorily weighted phoneme edit distance** (Karhila et al. 2019, arXiv:1905.02639)
  `[ABS]` gives a white-box, per-substitution-attributable Levenshtein with articulatory error
  weights — directly reusable as our phonetic distance, and it produces a human-readable
  contribution list per mismatch (good for traceable flags).
- **Alternate-spelling prediction** (Fox & Delworth 2022, arXiv:2209.01250) `[ABS]` is the most
  domain-relevant: they *released the contextual biasing lists for Earnings21*, confirm E2E
  models "struggle in particular with words that are rarely or never seen during training", and
  improve rare-word recall by 34.7% relative and OOV recall by 97.2% relative with an alternate
  spelling model that needs **neither a pronunciation dictionary nor a TTS system**.
- Multi-pronunciation via TTS + Whisper-extracted variants gives −43/−44% B-WER on
  LibriSpeech test-clean/other with U-WER essentially unchanged (Liu, Peng & Chng 2025,
  arXiv:2508.17796) `[ABS]` — evidence that *pronunciation-variant expansion of the candidate
  side* is where the recall comes from.
- Generative-annotation NEC (Luo et al. 2025, arXiv:2508.20700) `[ABS]` names the exact limit of
  pure phonetic-edit triggers: "when the forms of the wrongly-transcribed word(s) and the
  ground-truth entity are significantly different, these methods often **fail to locate** the
  wrongly transcribed words in hypothesis".

### 2.4 How keyword-boosting systems decide a rare word was likely present

- **BR-ASR** (Gong et al. 2025, arXiv:2505.19179) `[ABS]`: speech-and-bias contrastive
  retrieval scales to 200k entries with 99.99% pruning and 20ms/query, and explicitly adds
  curriculum learning to fight **homophone confusion**. B-WER 2.8/7.1 on test-clean/other.
- **COALA** (Guo et al. 2026, arXiv:2607.08117) `[ABS]` maps SLM latent representations into a
  discriminative space "to quantify the matching intensity between audio segments and candidate
  entities" — i.e. an explicit audio↔entity match score, which is the ideal detector signal but
  requires internal representations.
- **KWS-Whisper** (Li et al. 2023, arXiv:2309.09552) `[ABS]` runs open-vocabulary keyword
  spotting on encoder hidden states and notes OV-KWS "can be a **plug-and-play module to enhance
  the ASR error correction methods and frozen Whisper models**".
- Trie-based biasing with **k-step lookahead** exists specifically because the "did this partial
  hypothesis lead to the rare word?" decision is otherwise made by expensive bonus-revocation
  (Kwok & Yip 2025, arXiv:2509.09196) `[ABS]`; keyword-aware losses add a **binary classifier
  term for detecting biased-word positions** (Kwok, Yip & Chng 2025, arXiv:2509.09197) `[ABS]`.
- **LOGIC** (Wang 2026, arXiv:2601.15397) `[ABS]` reports the precision side properly: 9%
  average relative Entity-WER reduction across 11 locales at **+0.30% absolute false alarm
  rate**, and warns that GEC-style rewriting "frequently suffers from over-correction,
  introducing hallucinations of entities that were never spoken".

---

## Q3. Signal fusion for error localization beyond logprob

### 3.1 Audio-grounding contrast (the strongest transferable idea)

**Audio-Aware Decoding** (Hsu, Lu, Chiang & Lee 2025, arXiv:2506.07233) `[FT]`:

```
p_AAD(t) = softmax[ (1+α)·logit_with-audio(t) − α·logit_without-audio(t) ]
```

where "without audio" is operationally **a copy of the audio with all zeros** (same duration),
and the method "amplifies only those tokens whose probability increases when the actual audio is
present". Results: SALMONN-7B F1 0.233 → 0.737 at α=1.0; Clotho-AQA +5.4–10.3% accuracy. Their
own diagnostic is the telling one: the model's "yes" bias drops from ~90% to ~50% because the
blank-audio logits subtract equally, forcing commitment "only when the audio evidence is strong
enough".

Related variants that broaden the negative branch:
- **Whisper-CD** (Ahn et al. 2026, arXiv:2603.06193) `[ABS]`: training-free, contrasts clean
  audio against **three** acoustically-motivated negatives (Gaussian noise, silence, temporal
  shift), aggregated by log-sum-exp; up to −24.3pp WER on CORAAL long-form, 48% faster than
  beam search. Confirms the negative-branch machinery works on a *speech recognition* task, not
  just audio QA.
- **Adaptive perturbation selection** (Grace, Huo & Wang 2026, arXiv:2607.00247) `[ABS]`:
  optimal negative transform is task-dependent across temporal/spectral/frequency/amplitude
  families.
- **How Contrastive Decoding Enhances LALMs** (Lin et al. 2026, arXiv:2603.09232) `[ABS]` is
  the important caveat: CD "reliably rectifies errors in which models falsely claim an absence
  of audio or resort to **uncertainty-driven guessing**. Conversely, it **fails to correct
  flawed reasoning or confident misassertions**." A confidently-wrong entity substitution may be
  a confident misassertion — so use the contrast as a *detector score* (where the Δ is small,
  the token was not audio-driven) rather than trusting CD to fix it.

### 3.2 Attention-derived grounding (feasibility-blocked for us)

Waldendorf, Awwad Shiekh Hasan & Tsymbalov 2026 (arXiv:2604.19565) `[ABS]` define
AUDIORATIO / AUDIOCONSISTENCY / AUDIOENTROPY / TEXTENTROPY over SpeechLLM attention maps and
train logistic-regression classifiers, evaluated on **Qwen2-Audio** and Voxtral-3B: up to
+0.23 PR-AUC over uncertainty-based and prior attention baselines, generalising to OOD ASR;
~100 attention heads suffice. **But** it requires attention-map access *and* trains a
classifier — double-blocked under our API-only + no-task-trained-detector constraints. Keep as
the reference point for what we are giving up.

Same for HALAS's best detector (logistic regression on decoder-layer embeddings, F1 53–56%
`[FT]`) and Adaptive Vector Steering (Lin, Lee & Lee 2025, arXiv:2510.12851) `[ABS]`, which
finds "a strong correlation between output correctness and internal representations" — the
signal exists inside the model; we simply cannot reach it through llama-server.

### 3.3 Acoustic-discrepancy rescoring via a generative model

**READ** (Li, Wang & Guo 2026, arXiv:2606.04680) `[ABS]`: reference-free hypothesis evaluation
that "uses a pretrained auto-regressive TTS model to compute the **conditional likelihood of
speech tokens given a text hypothesis**", training-free, up to 20% relative error-rate
reduction when used for refinement, "particularly strong gains under noisy conditions", and it
"correlates with specific recognition errors". Conceptually ideal (it scores audio↔text
agreement in the *reverse* direction, immune to text-LM prior dominance) but requires a pinned
autoregressive TTS with speech-token likelihoods in the stack — a real integration cost.

### 3.4 Re-decode / sampling disagreement

- **Perturbation-based hallucination susceptibility** (Frieske & Shi 2024, arXiv:2401.01572)
  `[ABS]`: a test-time perturbation method that assesses ASR hallucination susceptibility
  "which does not require access to the training dataset", and distinguishes hallucinatory from
  non-hallucinatory models at matched WER. Directly reusable as a per-window instability probe.
- LLM-side: self-consistency detectors "perform nearly as well as a supervised (black-box)
  oracle", with a two-stage budget-friendly variant that only escalates inside an uncertainty
  interval (Xue et al. 2025, arXiv:2502.15845) `[ABS]`. SAC3 (Zhang et al. 2023,
  arXiv:2311.01740) `[ABS]` adds semantically-equivalent question perturbation + cross-model
  cross-check.
- Counterweight: Gabriel 2026 (arXiv:2605.05166) `[ABS]` finds first-content-token entropy from
  a **single** greedy decode matches or beats semantic self-consistency (AUROC 0.820 vs 0.793),
  and that combining them adds little. **Sampling is expensive; test cheap-entropy first.**
- Hierarchical voting over Monte Carlo samples, prioritising frequency with inference score as
  tie-break, is the concrete decoder-side recipe (Fu et al. 2026, UBG-Net/DUHV,
  arXiv:2607.06892) `[ABS]`.

### 3.5 Duration / forced-alignment anomaly

Weakest-supported branch in the literature; treat as a secondary feature, not a primary flag.

- **TeLeS** (Ravi, Raj T & Arora 2024, arXiv:2401.03251) `[ABS]` is the closest endorsement: it
  argues binary confidence targets discard "the **temporal alignment** between reference and
  hypothesis and whether the predicted word is entirely incorrect or contains spelling errors",
  and builds a Temporal-Lexeme Similarity target from exactly that. It validates temporal
  alignment as *information about* error type — but it uses it as a training target, not a
  reference-free signal.
- Recording-level: signal-to-noise ratio, spectral flatness, pause presence, sentence duration,
  and **speaking rate** are shown to identify divergent high-WER subgroups for Whisper
  (Koudounas & Giobergia 2024, arXiv:2404.07226) `[ABS]` — useful as a window-level prior,
  not a word-level flag.
- **Alignment-quality caveat that constrains us directly:** Rousso, Cohen, Keshet & Chodroff
  2024 (arXiv:2406.19363) `[ABS]` compare WhisperX and **MMS** against Montreal Forced Aligner
  on manually-aligned TIMIT and Buckeye — *restricted to words both systems recognised
  correctly* — and find **MFA outperformed both WhisperX and MMS**, "revealing a shortcoming of
  modern ASR systems". Our MMS_FA timestamps carry alignment error of the same order as the
  duration anomalies we would be hunting. Weight this signal accordingly, or add MFA.
- Repetition/looping hallucinations are the one duration-adjacent pattern with strong evidence:
  Whisper enters "catastrophic repetition loops (86% of 51,797 insertions)" under masking, while
  explicit-LLM decoders produce 38× fewer insertions (Ginjala et al. 2026, arXiv:2604.21276)
  `[ABS]`; HALAS annotates "Looping" as a first-class span label `[FT]`.

---

## Q4. What ASR-correction systems use as their TRIGGER, and with what precision

**The single most useful finding here: the state-of-the-art entity-correction system for our
exact domain has no confidence-based trigger at all.**

**RECOVER** (Kumar & Sachdeva 2026, arXiv:2603.16411) `[FT]` — "Robust Entity Correction via
agentic Orchestration of hypothesis Variants for Evidence-based Recovery":

- **Trigger:** *none in the confidence sense*. RECOVER applies correction universally per
  segment and instead performs **dynamic candidate retrieval**, scoring every phrase in the
  entity list against the ASR hypotheses with three signals:
  - exact token matches across all hypotheses (weight **1.0**),
  - fuzzy Levenshtein similarity within ±3 characters length (weight **1.2**),
  - phonetic prefix matching on a 5-character phonetic key (weight **0.6**).
  Top **K=200** candidates per segment. Fuzzy is weighted highest because "it is the primary
  mechanism for recovering corrupted entities (e.g., *sitiva → cytiva*)". Their stated rationale
  for retrieval over blanket correction: "Sending all phrases in the LLM prompt is wasteful and
  may degrade quality."
- **Four hypothesis strategies:** 1-Best (greedy only); **Entity-Aware Select** (pick the
  hypothesis with the most exact entity-candidate substring matches, ties broken by longer
  transcript = fewer deletions); **ROVER Ensemble** (entity-aware pivot, Needleman–Wunsch
  alignment, token-level majority vote, ≥3 of 5 hypotheses required for insertions, ties favour
  pivot); **LLM-Select** (all N hypotheses + top-K candidates in one call).
- **Numbers, on Earnings-21 (finance, 2,086 segments, 1,013 entities, 38.8h) — our domain:**
  **33.4% E-WER reduction, +10.6pp recall, +5.6pp F1**, best strategy **Entity-Aware Select**
  at 34.5%. Across five datasets: ATCO2 14.5% (LLM-Select), Eka-Medical 23.1% (LLM-Select),
  Common Voice 45.7% / +21.5pp recall (LLM-Select), ContextASR-Bench 20.8% (ROVER).
- **Error-type attribution:** "**Substitution reduction is the dominant correction mechanism,
  accounting for 63–93% of the total error reduction**" — the system fixes near-misses, not
  deletions.
- **Precision cost:** precision drops 7–9pp; insertions stay low (Earnings-21 baseline 15 →
  LLM-Select 12). No explicit false-positive rate reported.

Other trigger designs and their reported precision behaviour:

- **Confidence-embedded text detector — RED-ACE** (Gekhman et al. 2022, arXiv:2203.07172)
  `[ABS]`: adds an ASR Confidence Embedding layer so the AED model jointly encodes word-level
  confidence *and* text; the paper's finding is that confidence scores are **complementary to**,
  not a substitute for, the textual signal. They release an AED dataset over LibriSpeech.
- **Audio-transcript entailment** (Meripo & Konam 2022, arXiv:2207.10849) `[ABS]`: frames
  detection as bidirectional entailment between audio segment and transcript segment; classification
  error rate 26.2% on all transcription errors and **23.0% on medical terms specifically**
  (+12% / +15.4% over a strong baseline) — evidence that a *cross-modal* detector beats a
  text-only one on the domain-term class, which is our class.
- **Retention-probability threshold** (PMF-CEC, arXiv:2506.11064) `[ABS]`: an explicit
  confidence floor on edit operations, added specifically to fix over-detection.
- **Over-correction is the dominant practical risk, and it is quantified in our domain:**
  Voice Memory (Yang et al. 2026, arXiv:2607.26410) `[ABS]` reports that unconstrained
  generative error correction "**breaks correct tokens on up to 64% of its edits on financial
  news**", reduced to 35% by their memory-gated abstention; weighted WER 8.36% → 7.52% across
  ten HyPoradise domains "without regressing any dataset below its 1-best baseline". Their
  framing — a frozen corrector that "decides per utterance whether to act on the hypothesis or
  **abstain** and keep the 1-best" — is the correct architecture for a replay loop, and
  "restraint turns out to be the operative skill this loop discovers".
- **DARAG** (Ghosh et al. 2024, arXiv:2410.13198) `[ABS]` states the generalisation limit:
  GEC models "struggle to generalize beyond the specific types of errors encountered during
  training ... This phenomenon **amplifies with named entities**, where ... novel NEs keep
  emerging" — an argument for retrieval-triggered rather than learned-trigger designs.

---

## Candidate methods table

Feasibility is judged against: frozen Qwen3-Omni via llama.cpp (API-level), zero parameter
updates, no task-trained detector, pinned frozen tools OK (NER, G2P, MMS_FA), signals =
per-token logprobs + top-k, draft text, MMS_FA word timestamps, duration/rate stats, same-domain
draft-word lexicon with timestamps, call-metadata rosters.

| # | Method | Signals needed | Training-free feasibility | Expected precision: entity vs function words | Implementation sketch (≤3 sentences) | Key citation |
|---|---|---|---|---|---|---|
| M1 | **Entity gate** (NER + capitalisation + lexicon-rarity + OOV cues on draft) | draft text, domain lexicon, roster | **High** — frozen NER tagger is explicitly permitted; no model call | Entity recall high; **function-word precision 100% by construction** (they are never scored) | Run a pinned NER tagger over the draft; union its spans with capitalised non-sentence-initial tokens and tokens whose draft-lexicon frequency is below a percentile; emit only these spans as flag candidates. | Lei et al. 2024, arXiv:2409.15353; Ron et al. 2026, arXiv:2602.18966 |
| M2 | **Roster/lexicon phonetic-neighbour trigger** | draft text, G2P, roster + domain lexicon | **High** — pure CPU, no model call | High precision on *near-miss substitutions*; blind to errors whose surface form diverges far from the entity | G2P both the draft span and every roster/lexicon entity; score with articulatorily-weighted phoneme Levenshtein plus a phonetic-prefix key; flag spans that are *close but not equal* to a roster entity (a band, not a threshold). | RECOVER, arXiv:2603.16411 `[FT]` (weights 1.0/1.2/0.6, K=200); Karhila et al. 2019, arXiv:1905.02639 |
| M3 | **Audio-grounding contrast (AAD-as-detector)** | per-token logprobs under two conditions (real audio, zeroed audio) | **Medium-high** — needs a second forced-score pass with blank audio; no training | Directly separates LM-driven from audio-driven tokens; expected to *demote* function-word flags and *promote* ungrounded entities | Force-score the draft tokens twice — once with the window audio, once with an all-zeros buffer of identical duration — and take Δ_t = logp_audio − logp_blank; flag words whose min- or sum-pooled Δ falls below a percentile within the window. | AAD, arXiv:2506.07233 `[FT]`; Whisper-CD, arXiv:2603.06193; CAAD, arXiv:2606.23052 |
| M4 | **Content-token-restricted entropy / top-k margin** | per-token logprobs + top-k | **High** — already have the signal | Modest lift over raw logprob; needs M1 gating or it reproduces the current failure | Compute normalised top-K entropy and the top1−top2 margin per subtoken; aggregate to words by **sum for logprob features and min for entropy features** (never average); apply a learned-free fixed temperature and score only M1-gated spans. | Oneata et al. 2021, arXiv:2101.05525 `[FT]`; Laptev & Ginsburg 2022, arXiv:2212.08703; Gabriel 2026, arXiv:2605.05166 |
| M5 | **Re-listen instability (sampling + audio perturbation)** | repeated decodes at T>0 and/or perturbed audio | **Medium** — N× decode cost; no training | Good recall on genuinely ambiguous entity spans; poor on *confident* misassertions | Re-decode the window k times at temperature and with 2–3 acoustic negatives (noise, shift), align hypotheses by Needleman–Wunsch, and score each word by disagreement rate across the ensemble. | Frieske & Shi 2024, arXiv:2401.01572; Whisper-CD, arXiv:2603.06193; Xue et al. 2025, arXiv:2502.15845 |
| M6 | **Intra-call lexicon self-consistency** | draft-word lexicon with timestamps, G2P | **High** — CPU only | High precision when an entity recurs; zero coverage for single-occurrence entities | Cluster all draft word forms in the call by phonetic distance; within each cluster, flag the *minority* surface variants as likely errors of the majority form, weighted by cluster size and speaker. | RECOVER fuzzy-retrieval rationale, arXiv:2603.16411 `[FT]`; error-aware TF-IDF, arXiv:2606.24915 |
| M7 | **N-best / ROVER entity-aware selection** | N-best or k sampled hypotheses, roster | **Medium** — needs N-best from llama.cpp | Reported as the single best arm on Earnings-21 (34.5% E-WER reduction) | Generate 5 hypotheses, pick the pivot with the most exact roster-candidate substring matches (ties → longer transcript), align the rest by Needleman–Wunsch, and treat positions where the pivot loses the ≥3/5 vote as flags. | RECOVER, arXiv:2603.16411 `[FT]` |
| M8 | **Duration/rate plausibility from forced alignment** | MMS_FA timestamps, G2P phone counts, rate stats | **Medium** — cheap, but signal quality is the concern | Weak standalone; usable as a tie-breaker and for looping/repetition detection | Convert each flagged word to a phone count via G2P, divide MMS_FA duration by phone count, and z-score against the speaker's own rate distribution; flag implausible per-phone durations and repeated identical spans. | TeLeS, arXiv:2401.03251; Rousso et al. 2024, arXiv:2406.19363 (**alignment-error caveat**); Koudounas & Giobergia 2024, arXiv:2404.07226 |
| M9 | **TTS-likelihood acoustic discrepancy (READ)** | pinned autoregressive TTS with speech-token likelihoods | **Low-medium** — new heavy dependency | Strong in principle (reverse-direction scoring, immune to text-LM prior) | Score P(speech tokens \| hypothesis text) under a pinned AR TTS and localise the low-likelihood region against MMS_FA word boundaries. | READ, arXiv:2606.04680 |
| M10 | **Attention-derived grounding metrics** | decoder attention maps + a trained classifier | **Infeasible** — violates API-only *and* no-task-trained-detector | Best reported reference-free detector family (+0.23 PR-AUC) | (Reference point only.) | Waldendorf et al. 2026, arXiv:2604.19565; HALAS decoder-embedding detectors, arXiv:2606.23048 `[FT]` |

---

## Ranked shortlist: 5 flagging designs implementable from current signals

**Ranking principle:** the measured failure is not "the score was miscalibrated", it is "we
scored the wrong tokens". Every design below therefore *first restricts the candidate set to
entity-like spans* and only then applies a score. The literature is unanimous that this is the
working architecture (RECOVER, Lei et al., Courtside, DeRAGEC, ED-CEC).

### S1 — Roster-anchored entity gate + phonetic near-miss band (`M1 × M2`)
Highest expected precision per unit of engineering, and it needs **zero additional model calls**.
NER + capitalisation + draft-lexicon rarity produces the candidate span set; G2P + weighted
phoneme Levenshtein against the call roster and domain lexicon scores each span, and the flag
fires in a *band* — close enough to a roster entity to be a plausible corruption, far enough to
not be an exact match. This is precisely RECOVER's retrieval stage, whose weights are published
(exact 1.0 / fuzzy 1.2 / phonetic-prefix 0.6, top-K=200) and whose Earnings-21 result is a 33.4%
E-WER reduction with +10.6pp recall `[FT]` — the same corpus family as our decodes. Function
words cannot be flagged because they are not in the candidate set and have no roster neighbours,
which by construction eliminates our 17/17 failure. The known blind spot, stated by the NEC
literature itself, is entity errors whose surface form diverges far from the truth
(arXiv:2508.20700) — S2 and S4 exist to cover that.

### S2 — Blank-audio grounding contrast over gated spans (`M1 × M3`)
The highest-value *new* signal, and the one that most directly attacks the mechanism identified
in Q1. Force-score the draft tokens twice under the frozen model — once with the window audio,
once with an all-zeros buffer of the same duration — and take the per-token delta
Δ_t = logp(y_t | audio) − logp(y_t | blank), min-pooled over each gated word's subtokens. Where
Δ is near zero the token was produced by the language prior with no acoustic contribution, which
is the signature of a confidently-wrong entity substitution; where Δ is large the token is
audio-driven and should be left alone. AAD's formula, blank-audio construction, and the
observation that blank-audio logits "subtract equally" so the model must "commit only when the
audio evidence is strong enough" are verified from full text (arXiv:2506.07233 `[FT]`), and
Whisper-CD shows the same negative-branch machinery transfers to long-form ASR
(arXiv:2603.06193). Cost is one extra forced-score pass per window. **Caveat to design around:**
contrastive decoding "fails to correct flawed reasoning or **confident misassertions**"
(arXiv:2603.09232) — so use Δ as a detector score and never as an auto-corrector.

### S3 — Entity-aware N-best pivot disagreement (`M1 × M7`)
The best-performing arm on Earnings-21 in the only paper that evaluates on Earnings-21
(Entity-Aware Select, 34.5% E-WER reduction `[FT]`), and it reuses machinery we would want
anyway for the replay stage. Generate 5 hypotheses for the window, select as pivot the one with
the most exact roster-candidate substring matches (ties broken toward the longer transcript,
since length correlates with fewer deletions), align the remainder by Needleman–Wunsch, and flag
positions where the pivot loses a ≥3/5 majority vote. This gives a *localised* flag with an
attached correction candidate for free, which is exactly what the replay loop consumes.
Substitutions are where the payoff is — RECOVER attributes 63–93% of its total error reduction
to substitution repair — so calibrate expectations away from recovering deleted entities.

### S4 — Intra-call lexicon self-consistency (`M6`)
Cheapest high-precision signal we are not currently using, and it exploits a property of our
data that generic benchmarks lack: an earnings call names the same drug, executive, and
subsidiary repeatedly, so the same acoustic event is decoded many times. Cluster all draft word
forms in the call by phonetic distance, and flag minority surface variants within a cluster
against the majority form, weighting by cluster size and speaker consistency. The retrieval-side
analogue is validated (error-aware TF-IDF lifts hit rate 53.7% → 90.9%, arXiv:2606.24915), and
HALAS independently reports "strong cross-model vocabulary overlap" among hallucinations,
implying error forms are systematic rather than random `[FT]`. The honest limitation is
coverage: single-occurrence entities get nothing, so S4 is a precision booster layered on S1,
not a standalone flagger.

### S5 — Content-restricted entropy/top-k margin as the fallback score (`M1 × M4`)
Keep a purely-logprob score, but fix the two things the current implementation gets wrong:
score **only** M1-gated spans, and aggregate with **min-pooling for entropy features / sum for
logprob features, never averaging** — Oneata et al. verify that "length-invariant measures are
detrimental" because longer words are more error-prone, which is exactly backwards for entities
if you average `[FT]`. Add the top1−top2 margin and top-K rank features, which cut token-level
maximum calibration error from 20.04% to 4.50% versus raw softmax (arXiv:2607.29299). Entropy
aggregation is reported 2–4× better than max-per-frame probability at detecting incorrect words
(arXiv:2212.08703), and single-decode top-K entropy at *content-bearing* tokens reaches AUROC
0.820, beating multi-sample self-consistency (arXiv:2605.05166). This is the cheapest design to
ship and the right ablation baseline against S2 — if S2 does not beat S5, the contrast pass is
not earning its cost.

**Suggested fusion for a first implementation:** hard gate on S1; final score =
`max(normalised Δ-deficit from S2, phonetic-proximity from S1, minority-variant score from S4)`;
S3 supplies the correction candidate; S5 as ablation baseline. Add an **abstention floor** on
the downstream corrector — Voice Memory's finding that unconstrained GER breaks correct tokens on
up to 64% of edits *on financial news* (arXiv:2607.26410) is the clearest warning in this
literature that recall bought at the cost of over-correction is negative value.

**Evaluation caution:** HALAS establishes that on real earnings-call audio, *trained* detectors
reach only F1 53–56% and proxy metrics 0.7–0.8 AUC `[FT]`. Judge these designs on
**entity-class precision at fixed flag budget**, not on general error-detection F1.

---

## Bibliography (arXiv ids)

**Confidence / calibration.** Li, Qiu, Zhang et al. 2020, 2010.11428 `[FT]` · Oneata, Caranica,
Stan et al. 2021, 2101.05525 `[FT]` · Qiu, Li, He et al. 2021, 2103.06716 · Qiu, He, Li et al.
2021, 2104.12870 · Wang, Soltau, El Shafey et al. 2021, 2110.15222 · Li, Zhang, Qiu et al. 2021,
2110.03327 · Laptev & Ginsburg 2022, 2212.08703 · Ogawa, Tawara, Kano 2023, 2312.14609 · Ravi,
Raj T, Arora 2024 (TeLeS), 2401.03251 · Aggarwal, Nair, Verma et al. 2025, 2502.13446 · Huo,
Zhang, Tang 2025, 2509.07195 · Liang, Ballier, Levow, Wright 2025, 2509.25516 · Jia & Van hamme
2026 (SR-CEM), 2607.29299 · Li, Ness, Ragni 2018, 1810.13024 · Futami et al. 2021 (P-ELECTRA),
2110.01857.

**Internal LM / prior-vs-acoustics.** Variani et al. 2020 (HAT), 2003.07705 · Meng et al. 2021
(ILMT), 2102.01380 · Zheng et al. 2022 (LODR), 2203.16776 · Yang et al. 2023, 2309.14130 ·
Zeineldeen et al. 2026, 2607.05612 · Meng et al. 2023 (JEIT), 2302.08583.

**Contrastive / audio-aware decoding.** Hsu, Lu, Chiang, Lee 2025 (AAD), 2506.07233 `[FT]` ·
Ahn et al. 2026 (Whisper-CD), 2603.06193 · Lin et al. 2026, 2603.09232 · Chen et al. 2026
(CAAD), 2606.23052 · Grace, Huo, Wang 2026, 2607.00247 · Li et al. 2026 (TCD), 2604.15383 ·
Jung, Jang, Chung 2025 (AVCD), 2505.20862 · Chung et al. 2026 (MAD), 2601.21181.

**ASR error detection / hallucination.** Gekhman et al. 2022 (RED-ACE), 2203.07172 · Meripo &
Konam 2022, 2207.10849 · Park et al. 2021, 2108.01812 · Frieske & Shi 2024, 2401.01572 ·
Barański et al. 2026 (HALAS), 2606.23048 `[FT]` · Koudounas et al. 2025 (SHALLOW), 2510.16567 ·
Atwany et al. 2025, 2502.12414 · Waldendorf et al. 2026, 2604.19565 · Koenecke et al. 2024,
2402.08021 · Li, Wang, Guo 2026 (READ), 2606.04680 · Ginjala et al. 2026, 2604.21276.

**Entity / rare-word correction and biasing.** Kumar & Sachdeva 2026 (RECOVER), 2603.16411
`[FT]` · Lei, Na, Xu, Pusateri 2024, 2409.15353 · Im et al. 2025 (DeRAGEC), 2506.07510 · He &
Toda 2025 (PMF-CEC), 2506.11064 · Wang et al. 2024 (DANCER), 2403.17645 · Luo et al. 2025,
2508.20700 · Sudo, Hata, Nakadai 2023, 2305.17846 · Trinh, He, Whitehill 2025, 2506.10779 · An
et al. 2026 (A-STAR), 2602.12287 · Ghosh et al. 2024 (DARAG), 2410.13198 · Yang et al. 2026
(Voice Memory), 2607.26410 · Wang 2026 (LOGIC), 2601.15397 · Fox & Delworth 2022, 2209.01250 ·
Liu, Peng, Chng 2025, 2508.17796 · Gong et al. 2025 (BR-ASR), 2505.19179 · Guo et al. 2026
(COALA), 2607.08117 · Li et al. 2023 (KWS-Whisper), 2309.09552 · Kwok, Yip, Chng 2025,
2509.09197 · Kwok & Yip 2025, 2509.09196 · Jafari-Raddani 2026, 2606.24915 · Bekal et al. 2021,
2109.05092 · Ron, Gilboa, Dubnov 2026, 2602.18966 · Inaguma et al. 2019, 1909.09993 · Yamashita
et al. 2025, 2505.17410.

**Domain / evaluation.** Del Rio et al. 2021 (Earnings-21), 2104.11348 · Piskala 2025
(ProfASR-Bench), 2512.23686 · Borgholt et al. 2025, 2509.24478 · Afonja et al. 2024, 2406.12387 ·
Zhou et al. 2026, 2602.12249 · Manohar et al. 2026 (SCRIBE), 2605.20712.

**Alignment / duration.** Rousso, Cohen, Keshet, Chodroff 2024, 2406.19363 · Weber et al. 2026,
2606.10675 · Bain et al. 2023 (WhisperX), 2303.00747 · Wagner, Thallinger, Zusag 2024
(CrisperWhisper), 2408.16589 · Koudounas & Giobergia 2024, 2404.07226 · Karhila et al. 2019,
1905.02639.

**LLM-side uncertainty.** Kuhn, Gal, Farquhar 2023, 2302.09664 · Zhang et al. 2023 (SAC3),
2311.01740 · Xue et al. 2025, 2502.15845 · Gabriel 2026, 2605.05166 · Chen et al. 2024 (INSIDE),
2402.03744 · Fu et al. 2026 (UBG-Net), 2607.06892.
