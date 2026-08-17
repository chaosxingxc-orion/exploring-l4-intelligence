# Cluster C — Contextual Biasing / Context-Supply ASR: deep read + adversarial check

Workbench note. Author: deep-reading agent (Cluster C). Date: 2026-08-16 (local, UTC-4).
Scope: prior art for SAEA's surviving N2 direction (compact legal roster supplied into a frozen,
API-only omni prompt), after the 2026-08-16 P2 VOID of the reflection/verification operator.
Read-only over all repositories; this file is the only artifact written.

**Bottom line up front.** N2's mechanism (compact entity roster → prompt → speech model) is
*published prior art*, twice over, and the compact-beats-full-bag dose result is *also published*
(Ren et al. 2025, Table III). SAEA's parroting/VOID finding was *independently published three
weeks ago* on Qwen3-Omni 30B (Zhang et al., 2026-07-24, "Listen, Do Not Copy"). What survives as
genuinely un-taken ground is narrow but real: **the API-only regime with no logit access, on real
long-form entity-dense earnings-call speech, with a provenance-audited supply chain and a paired
harmful-edit ledger** — i.e. a *deployment-legality and measurement* contribution, not a mechanism
contribution. The claim ladder must be re-cut accordingly. Details and three concrete attacks below.

---

## 1. Fetch log

All access via WebSearch/WebFetch. No logins, no paid APIs. Times are local (UTC-4); UTC offset
verified at 2026-08-17T01:06:44Z == 2026-08-16 21:06:44 local. Timestamps are to the minute and
were recorded per call in order.

| # | Time | Type | Query / URL | One-line result |
|---|------|------|-------------|-----------------|
| 1 | 20:57 | fetch | `arxiv.org/abs/2509.19567` | Siskos et al., "Retrieval Augmented Generation based context discovery for ASR", EMNLP 2025; TED-LIUM3/Earnings21/SPGISpeech; up to 17% rel WER, oracle 24.1%. |
| 2 | 20:57 | fetch | `arxiv.org/abs/2506.07510` | DeRAGEC, ACL 2025 Findings, POSTECH+Samsung+aiXplain; NE candidate denoising, code public. |
| 3 | 20:57 | fetch | `arxiv.org/pdf/2509.19567v2` | PDF text extraction lossy (tables unreadable); PDF cached locally. |
| 4 | 20:57 | fetch | `arxiv.org/pdf/2506.07510` | Same — lossy; PDF cached locally. |
| 5 | 20:58 | fetch | `arxiv.org/html/2509.19567v2` | HTML render gave full Table 2 + method; retrieval query = prior-k hypothesis text, not audio. |
| 6 | 20:58 | fetch | `arxiv.org/html/2506.07510v1` | HTML render gave Table 1 + method; top-10 phonetic candidates, o1-synthesised rationales. |
| 7 | 20:58 | bash/pdftotext (WSL) | local cache of #3, #4 | Verified all tables/numbers first-hand; HTML summaries confirmed accurate. |
| 8 | 20:59 | fetch | `arxiv.org/html/2509.19567v2` (targeted) | Confirmed ASR = trained CB module (Jalal et al. 2023); CB-LLM never sees audio; oracle = gold non-stopword tokens. |
| 9 | 21:00 | fetch | `aclanthology.org/2024.lrec-main.328/` | Confirmed = ConEC (LREC-COLING 2024, pp. 3700–3706). |
| 10 | 21:00 | search | "ConEC earnings call dataset contextual ASR LREC-COLING 2024 Huang" | Located ACL + Amazon Science mirrors; also surfaced ProfASR-Bench (2512.23686). |
| 11 | 21:01 | fetch | `assets.amazon.science/.../conec-....pdf` | 404. |
| 12 | 21:01 | fetch | `arxiv.org/html/2512.23686` | ProfASR-Bench: synthetic TTS, Whisper tiny/base/small + Qwen2.5-Omni 3B; oracle prompt only −0.06 pp. |
| 13 | 21:02 | fetch | `aclanthology.org/2024.lrec-main.328.pdf` | ConEC PDF retrieved (summary weak); cached locally. |
| 14 | 21:02 | fetch | `github.com/huangruizhe/ConEC` | Repo: PDFs, `participant_names`, extracted biasing word lists, corrected `.nlp` refs; no license stated. |
| 15 | 21:02 | bash/pdftotext (WSL) | local cache of #13 | Read ConEC Table 1 + Table 2 first-hand (all WER/entity numbers below). |
| 16 | 21:03 | search | "prompt-level contextual biasing frozen speech LLM audio LLM hotword prompt 2025 named entity" | Surfaced LOGIC (2601.15397), GLCLAP+GRPO (2512.21828), IBM (2604.12398), NIM4-ASR (2604.18105). |
| 17 | 21:04 | fetch | `arxiv.org/pdf/2601.15397v1` | LOGIC (Microsoft, 2026-01-21); summary weak; cached locally. |
| 18 | 21:04 | fetch | `arxiv.org/abs/2512.21828` | Kong et al.: GLCLAP audio-text hotword retrieval + GRPO fine-tuning of LLM-ASR. |
| 19 | 21:04 | read | local cache of #17 | Read LOGIC in full: "list-vomiting"/Context Leakage, GEC over-correction, Trie logit bonus, Phi-4-mini, 11 locales. |
| 20 | 21:05 | search | "audio few-shot in-context learning demonstrations speech LLM ASR entity 2026 frozen no training" | Surfaced FSA-GRPO (2606.02615), TICL, M2R-Whisper, SALSA. |
| 21 | 21:05 | fetch | `arxiv.org/html/2604.12398v1` | IBM Granite-Speech, prompt-supplied bias list, LoRA+Q-former fine-tuned, B-WER 5.8→4.4 @200 words. |
| 22 | 21:05 | search | "audio-conditioned retrieval select biasing entities from speech training-free frozen omni model 2026 contextual ASR routing" | Surfaced "Listen, Do Not Copy" (2607.21943), BR-ASR, PAC, RASST. |
| 23 | 21:06 | fetch | `arxiv.org/html/2607.21943v1` | **Direct scoop risk**: Qwen3-Omni 30B copies supplied context 94–99.8%; 100% "accuracy" on silent audio. |
| 24 | 21:06 | fetch | `arxiv.org/html/2606.02615` | FSA-GRPO: Qwen2.5-Omni 35.42 → 27.29 WER 3-shot (untrained ICL works but underused); fix = LoRA RL. |
| 25 | 21:06 | search | "bias list size ablation prompt speech LLM 'lost in the middle' contextual biasing degradation large list 2026 compact list better" | Surfaced Ren et al. 2506.06252 (EWER 1.80/4.16/5.61 dose ladder) and RLBR 2601.13409. |
| 26 | 21:06 | fetch | `arxiv.org/pdf/2506.06252` | Summary weak; cached locally. |
| 27 | 21:06 | fetch | `arxiv.org/abs/2601.13409` | RLBR (Microsoft, 2026-01-19): B-WER degrades 0.59/2.11 @100 → 1.36/4.04 @1000 words. |
| 28 | 21:07 | grep | local cache of #26 | **Confirmed dose table first-hand**: Exact 1.80 / Small 4.16 / Large 5.61 EWER; filtering → 4.04 / 4.95. |

Searches used for the "2025–2026 prompt-level biasing on speech-LLMs" allowance: #16, #20, #22, #25
(four). #10 was a target-locating lookup for a named assigned work.

---

## 2. Per-work extraction (the four assigned works)

### C-1. Siskos et al., "Retrieval Augmented Generation based context discovery for ASR" (arXiv 2509.19567v2, EMNLP 2025; CERTH + Samsung R&D UK)

- **What context is supplied**: a per-segment list of *context words* `C_t` (unigrams), sized c ∈ {100, 250}.
- **How selected**: **text-conditioned, not speech-conditioned.** Query `q_t = f(Ŷ_{t−1})` = MiniLM
  (`all-MiniLM-L6-v2`) embedding of the concatenated ASR hypotheses of the previous k ∈ {10, 100}
  VAD segments; top-N cosine over a **static global vocabulary of 466,358 English non-stopwords**
  (+ definitions), FAISS-indexed. The audio never touches the selector. Alternative CB-LLM: same
  text window prompted into Llama3.2-3B ("You are the master of knowledge… provide a huge number of
  relevant words") — also blind to audio.
- **To what model**: a **trained contextual-biasing ASR** (CB mechanism of Jalal et al., ASRU 2023),
  Samsung-internal. Not a prompt to an LLM; the paper is careful to call this "plug-and-play" only
  in the sense that *this study* does not re-fine-tune. Post-hoc `LLM_fix` (Llama3.2-3B) is an
  optional transcript rewriter.
- **Results (Earnings21, ~5 h)**: No-context **35.9** → CB-RAG[250,10] **31.1** (−4.8 pp, 13.4 % rel);
  CB-LLM 31.8; CB-LLM+LLM_fix 31.7; **Oracle 29.7** (gold non-stopword tokens of the current segment).
  TED-LIUMv3: 18.9 → 16.4, oracle 15.4. SPGISpeech: 22.4 → 18.7, oracle 17.0.
- **Dose/quality response**: **more context helped**, monotonically over the tested range
  (c = 100 → 250: 32.5 → 31.1 on E21; 17.6 → 16.4 on TED). Retrieval count reaches **15.17× the
  oracle token count** and still wins. Shorter lookback (k = 100 → 10) helps.
- **Sharpest usable finding for SAEA**: **contextual overlap does not predict WER.** CB-LLM attains
  52.9–79.1 % overlap with the oracle context on E21 but *worse* WER than CB-RAG at 8.8–21.4 %
  overlap. Recall of the right context is not the objective function.
- **Harmful-edit accounting**: none. No entity-level metric at all — only aggregate WER, an
  overlap proxy, a count ratio, and latency. Limitations admit lexical sensitivity and
  `LLM_fix` degradation on noisy transcripts, without measuring either.
- **Code/data**: no release statement; internal ASR; **not reproducible**.

### C-2. DeRAGEC (arXiv 2506.07510v1, ACL 2025 Findings; POSTECH + Samsung MX + aiXplain)

- **What context is supplied**: top-10 phonetically similar **named-entity candidates**, each
  serialised as `<n_i | phonetic-score:PS_i | def: Def_i>` (one-line Wikipedia definition), plus the
  NEs already present in the 5-best hypotheses, into the LLM prompt.
- **How selected**: **hypothesis-conditioned, phonetically targeted; not audio-conditioned.**
  GLiNER-large-v2 tags NEs on the 1-best `h_1`; Epitran + Panphon phonemise and score articulatory
  similarity; top-k over a **3,003,462-entry NE database** (CommonVoice train + a media-entity
  dataset + Wikipedia). The correction stage never sees audio (the paper cites multimodal GEC as
  related work but does not do it).
- **To what model**: **frozen LLMs, prompt-level, no training** — Llama-3.1-70B and GPT-4o-mini via
  ICL; ASR is frozen Whisper-large-v3-turbo (beam 5). `o1` synthesises the denoising rationales
  **offline using the ground-truth transcription** `r_syn ← M_r(h_1, a, N, PS, Def)`; those become
  the few-shot demonstrations.
- **Results (WER ↓ / NE hit ratio ↑, Llama-3.1-70B)**: CommonVoice 7.7/0.751 (ASR) → 6.8/0.782 (GEC)
  → 6.5/0.804 (RAGEC) → **6.0/0.831 (DeRAGEC)** → 5.8/0.837 (oracle NE). STOP 8.9/0.787 → 5.9/0.838,
  oracle 5.7/0.857. Appendix Table 4: a *true* oracle where the correct NE is always retrieved gives
  **4.1 WER / 0.922 hit** vs 7.7 baseline — i.e. the retrieval stage, not the LLM, is the ceiling.
- **Dose/quality response (Table 2, CV/Llama)**: top-k = 1 → 7.2 WER (recall .823, prec .137);
  k = 5 → 6.6 (.835/.084); **k = 10 → 6.5 (.841/.056)**; k = 15 → **6.7** (.843/.032). **U-shaped:
  more candidates past 10 hurt despite marginally higher recall.** Over-filtering hurts symmetrically
  (PS threshold 0.9 → recall .126, WER 7.2). Form also matters: adding definitions *without*
  phonetic scores collapsed STOP hit ratio 0.807 → **0.697** and WER 6.5 → 7.2.
- **Harmful-edit accounting**: partial — denoising precision/recall is measured (prec 0.139 vs 0.166
  bound; recall 0.839 vs 0.841), but no worsened-utterance / harmful-edit ledger.
- **Directly relevant to SAEA's N1**: Appendix F shows **NER performance on the 1-best degrades as
  ASR WER rises** — "the bottleneck in extracting phonetic queries from `h_1`". This is SAEA's
  routing-choke-point finding, already published, for *text-side* routing.
- **Code**: `github.com/solee0022/deragec` (public).

### C-3. ConEC (LREC-COLING 2024, pp. 3700–3706; JHU + Amazon Alexa + Xiaomi + AMD + VoiceBrain)

**This is the closest prior art to N2 that exists, and it is on the same dataset.**

- **Corpus**: Earnings-21 (44 calls, mean 54 min; 17 min–1 h 34) as eval; Earnings-22 (119 h,
  125 files) as train/dev. Transcripts repaired against S&P Capital IQ (`<unk>`/`<inaudible>`/
  misspellings replaced by Levenshtein alignment); sentence-level segmentation added.
- **What context is supplied**: per-call biasing lists built from (1) presentation slides and
  earnings releases from company IR pages (PDF → `pdftotext`, stop-words / non-alphanumerics /
  numerics / legal-disclaimer pages removed), and (2) **meeting participants' names and affiliations
  scraped from Seeking Alpha**. Treated as a bag of uncased unigrams. **~100–2000 words per call.**
- **How selected**: **global per call. No per-utterance selection, no speech conditioning, no
  filtering.** The entire call-level bag is active for every utterance.
- **To what model**: a **zipformer transducer, 71.5 M params, trained on SPGISpeech**, with
  **shallow fusion** biasing (`log P(W|X) + λ log P_C(W)`) in `icefall` — zero-shot in the sense of
  needing no biasing-specific training, but requiring **beam-search score access**.
- **Results (Earnings-21, WER overall (common/rare); per-entity WER)**:

  | Row | Context | WER (Com/Rare) | non-entity | PERSON | ORG | GPE | LOC | PROD | EVENT | NORP | FAC |
  |---|---|---|---|---|---|---|---|---|---|---|---|
  | 1 | none | 10.41 (8.71/26.02) | 9.40 | 45.9 | 29.5 | 18.8 | 5.85 | 24.2 | 43.1 | 9.55 | 28.7 |
  | 2 | Le et al. 2021 synth (per-utt gold rare words + 500 distractors) | 10.08 (8.62/23.43) | 9.18 | 40.7 | 25.6 | 17.8 | 5.26 | 20.2 | 42.3 | 8.04 | 25.4 |
  | 3 | Fox & Delworth 2022 synth (gold PERSON+ORG for all calls + Fortune-500/CEO distractors, one shared 3066-word list) | 10.22 (8.62/24.80) | 9.35 | 38.9 | 25.3 | **19.2** | 5.65 | 23.5 | 41.9 | **10.1** | **29.8** |
  | 4 | **ConEC real** (slides + release + participant roster) | 10.29 (8.70/24.84) | 9.39 | 39.8 | 26.1 | 18.4 | 5.65 | 21.9 | 43.1 | 9.55 | 28.7 |
  | 5 | ConEC oracle (row-1 output, entity words replaced by correct ones **if present in the context**) | 9.69 (8.71/**18.72**) | 9.25 | **13.0** | **17.7** | 12.9 | 5.46 | 19.2 | 35.6 | 5.53 | 16.6 |
  | 8 | Whisper-large, no biasing | 7.98 (6.94/17.43) | 7.50 | 28.9 | 19.6 | 17.0 | 5.85 | 18.7 | 2.78 | 8.54 | 21.6 |

- **Dose/quality**: row 3 is the harmful-supply datapoint — a *shared* distractor-heavy list improves
  PERSON/ORG but **degrades GPE, NORP and FAC below the no-context baseline**. Row 4 (real, provenance-
  clean context) beats row 3 on the non-target types but is weaker than row 2 (per-utterance,
  gold-derived) overall. The authors state real contexts are noisier and that "such distractors may
  be too simple" in the synthetic setups.
- **Legal-coverage ledger already exists (Table 1)**: fraction of *spoken* entity tokens covered by
  ConEC contexts — PERSON 82 % (3340 tokens), ORG 66 % (6362), GPE 61 % (1605), LOC 48 % (532),
  PRODUCT 39 % (671), EVENT 39 % (575), NORP 39 % (201), FAC 29 % (181). Without the participant
  roster, PERSON/ORG coverage falls to 30 %/56 % — **the roster is what carries PERSON coverage.**
- **Availability**: `github.com/huangruizhe/ConEC` — PDFs, `participant_names`, pre-extracted biasing
  word lists, corrected `.nlp` references, timestamps; **no license stated in the repo**; the paper
  is CC BY-NC 4.0. Baselines in `k2-fsa/icefall`.

### C-4. ProfASR-Bench (arXiv 2512.23686, skim)

- Synthetic TTS speech (Kokoro-82M) over LLM-drafted entity-dense text in Finance/Medicine/Legal/Tech;
  four voice variants. **Not real speech.**
- Ladder: no-prompt / profile / domain+profile / **oracle (gold normalised transcript as prompt)** /
  **adversarial (deliberately wrong domain)**. All supplied as natural-language prompt prefixes.
- Models: Whisper tiny/base/small + **Qwen2.5-Omni-3B**.
- Headline: Whisper-small 9.98 (no prompt) / 9.95 (profile) / 9.95 (domain+profile) / **9.92 (oracle)**
  / 9.95 (adversarial). Adversarial context **does not reliably degrade**; oracle gains ~0.06 pp.
  Claim: a "context-utilization gap" — nominally promptable models that ignore side information.
- Has **NE-WER and Entity-F1**. Data on HF (`prdeepakbabu/ProfASR-Bench`), repo promised post-acceptance.
- **Weight**: low. Synthetic speech, sub-1 B models plus a 3 B omni, a preprint. But it is a direct
  published claim on SAEA's axis, and it points in the *opposite* direction from SAEA's oracle
  measurement (SAEA: oracle 10.88 vs zero 12.38 = −1.5 pp on real speech with a 30 B omni). That
  contrast is itself worth owning: **model scale and real vs synthetic speech decide whether
  prompt-level context is used at all.**

---

## 3. The wider 2025–2026 prompt-level biasing landscape (bounded sweep)

| Work | Supply mechanism | Frozen? | Key number | Why it matters to N2 |
|---|---|---|---|---|
| **LOGIC** (P. Wang, Microsoft, arXiv 2601.15397, 2026-01-21) | Trie bonus **in logit space** (vLLM LogitsProcessor) | model weights frozen, **needs logit access** | Phi-4-mini, 11 locales, PNAME sets of ~460–2100 entities: **−9 % rel EWER, FAR +0.30 pp**; aggressive λ → −17 % | States flatly that prompting "cannot support large phrase lists, even for the 460 de-DE entities… the output is unpredictable and may leak the whole phrase list. This phenomenon happens to not only Phi-4-mini but also other speech LLMs such as GPT-4o." Documents **"list-vomiting"** (model recites the roster instead of transcribing) and **GEC over-correction** ("I like algorithms" → "I like Al Gore"). Metrics: EWER, Entity Recall, **FAR = incorrect entity insertions per utterance**. |
| **Ren, Shi & Li, "Lightweight Prompt Biasing"** (arXiv 2506.06252, 2025) | bias list as decoder **prompt** with `<hit>/<miss>` task tokens | **trained** multi-task Transformer ASR | in-house domain set: **Exact 1.80 / Small(~50) 4.16 / Large(~1800) 5.61 EWER**; WER 4.60/4.54/4.80; **+ entity filtering → 4.04 / 4.95**; general set 6.91 (base) / 6.95 (no list) / 6.97 (noisy list) | **This is the full-bag-vs-compact dose result, already published.** Explicit conclusion: "the more targeted and relevant the biasing list, the greater the improvement"; filtering narrows to "10–20 highly relevant candidates". |
| **RLBR** (Ren, Fan, Shen, Chen, Li, arXiv 2601.13409, 2026-01-19) | prompt + RL fine-tuning with biasing-word reward | **RL fine-tuned** | LibriSpeech B-WER **0.59/2.11 @100 words → 1.36/4.04 @1000 words** | Second published dose ladder; degradation with list size is the accepted background fact, not a discovery. |
| **IBM Granite-Speech** (Novitasari, Fukuda, Kurata, Saon, arXiv 2604.12398, 2026-04-14) | bias list concatenated into the **text prompt** of a speech LLM | **LoRA + Q-former fine-tuned** | B-WER 5.8 → 4.4 @200-word lists (−24.1 %); U-WER stable 2.1–2.3 | Prompt-level supply to a speech LLM with B-WER/U-WER paired ledger — the exact metric pair SAEA plans, in a fine-tuned regime. |
| **GLCLAP + GRPO** (Kong et al., arXiv 2512.21828, 2025-12-26) | **audio-conditioned** hotword retrieval (contrastive language-audio), candidates injected as text prompt | LLM-ASR **GRPO fine-tuned** | substantial KER reductions, sentence accuracy preserved | **Speech-conditioned targeting is not unclaimed.** It exists; it just costs training. |
| **"Listen, Do Not Copy"** (Zhang, Tian, Xie, Yang, Li, Liu, arXiv 2607.21943, 2026-07-24) | full transcript vs "audio-grounded scaffold context" (partial, shuffled, distractor-laced clues) | fix requires **LoRA SFT + GDPO** | **Qwen3-Omni 30B / MiniCPM-o 4.5 / Ming-flash-omni 2.0 copy wrong supplied answers 94–99.8 % of the time (weakest 47 %); with silent audio all three score 100 % on the primary-transcript task**; post-training mpWER Qwen3 24.7 → 9.2 | **Near-scoop of SAEA's P2 VOID.** Same model family, same failure, published 3 weeks before SAEA's read. Their **silent-audio control** and **answer-overlap screening** are the control arms SAEA's design needs — and are now citable prior art, not SAEA inventions. |
| **FSA-GRPO** (Zheng, Wang, Fan, Jin, Hasegawa-Johnson, arXiv 2606.02615, 2026-05-26) | few-shot **audio→text demonstrations** in context | base model frozen for the ICL baseline; fix = LoRA RL | **Qwen2.5-Omni RSR child ASR: 35.42 zero-shot → 27.29 with 3-shot demos → 16.32 after FSA-GRPO** | **The DEMO lane's mechanism is published.** Training-free audio-text ICL already yields −8 pp; the paper's thesis is that auditory LLMs "are not explicitly trained to perform inference in this demonstration-conditioned format", limiting the benefit. |

---

## 4. Central question 1 — after the VOID, is N2 distinguishable from published prompt-level biasing?

**Honest answer: not on mechanism. Only on regime, provenance and measurement.**

Decomposing the four candidate deltas:

**(a) Legal provenance discipline — weakest surviving delta, partially pre-empted.**
ConEC already supplies exactly SAEA's content (company/product names from slides and releases +
**speaker names and affiliations**) on **exactly SAEA's dataset** (Earnings-21), and already publishes
the coverage ledger (PERSON 82 %, ORG 66 %, …). What ConEC does *not* do: state a license for the
context artifacts (Seeking Alpha scrape, IR-page PDFs — provenance that a deployment-legality claim
cannot lean on), define a machine-checkable admissibility rule, or separate "legal at deployment
time" from "available in the research corpus". SAEA's roster from **dataset-shipped metadata CSVs**
is a *cleaner* provenance story than ConEC's scrape, and SAEA can pre-register an admissibility
predicate. But "we used cleaner sources" is a paragraph, not a paper. To carry weight it must become
a *measured* axis: coverage/gain as a function of provenance tier (dataset-shipped metadata ⊂ IR-page
public documents ⊂ scraped third-party ⊂ gold), with the ledger showing what each tier buys.

**(b) Speech-conditioned routing — the strongest surviving delta, and it is exactly what N1 is for.**
Every work read here selects context from **text**: prior-segment hypotheses (Siskos), 1-best NER +
phonetics (DeRAGEC), or nothing at all (ConEC: global per-call bag). The one audio-conditioned
selector found (GLCLAP, 2512.21828) requires contrastive pre-training **and** GRPO fine-tuning of the
LLM-ASR. **No work in this sweep does training-free, audio-conditioned selection against an API-only
core.** DeRAGEC's Appendix F even names the bottleneck SAEA hit — text-side routing degrades exactly
where WER is worst — without escaping it. That is a real, defensible gap. It also means **N1 is not
preparatory work for N2; N1 is the contribution.** If N1 only produces "flag recall = X %" and N2 is
a static roster, the paper has no delta.

**(c) Harmful-edit accounting — dead as novelty, mandatory as hygiene.**
Beyond the Edit Rate / Improve@Edit / Worsen@Edit lineage already flagged (survey arXiv 2508.07285),
the biasing literature has its own: LOGIC's **FAR** (incorrect entity insertions per utterance),
IBM's **U-WER**, ConEC's non-entity-WER column, Ren et al.'s general-set WER control. SAEA must
report a paired ledger and must not claim it as novel. The one thing SAEA can still claim is
*completeness*: nobody in this set reports harmful edits, dose, provenance tier, and routing recall
in a single pre-registered ledger on real long-form speech.

**(d) The omni / audio-native API-only core — real, and it is the load-bearing frame.**
LOGIC's response to prompt-level fragility is to **leave prompt space entirely** and inject at the
logit layer — which presupposes vLLM-level access. IBM's, RLBR's and GLCLAP's responses all
presuppose weight access. SAEA's constraint (frozen, API-shaped, no logits, no training) forecloses
every published fix. **That makes SAEA's question the residual one: given only the prompt channel,
what supply *form* and *dose* actually converts on real entity-dense speech, and where does it
collapse into copying?** LOGIC asserts prompt-level biasing is unusable but reports **no prompt
baseline table** — it is an assertion backed by an anecdote (the "Aaron, Aarthy, Alex…" example) and
internal, unreleased test sets. SAEA can supply the missing measurement.

**Publishability verdict.** Not as "we did contextual biasing on a frozen omni" — that is C-1/C-3/
C-4 territory and reviewers will say so. Publishable as one of:

1. **A negative/boundary result with a mechanism**: "prompt-channel evidence supply on frozen omni
   cores: where it converts, where it collapses into copying" — SAEA's parroting data + dose curve +
   harmful-edit ledger, positioned as the empirical backing LOGIC asserted without measuring, and as
   the entity-dense real-speech counterpart to "Listen, Do Not Copy" (which studies overlap/noise,
   not entity supply) and ProfASR-Bench (synthetic, small models). Venue-realistic: Interspeech /
   ICASSP short, or an ACL-style resource/analysis paper.
2. **A routing paper**: training-free, audio-conditioned selection of which legal evidence to supply,
   measured against text-conditioned selection (DeRAGEC-style) and against no selection (ConEC-style
   global bag), on Earnings-21 where the ConEC baseline is public. This is the only one of the four
   deltas with no direct occupant.

Option 2 is the higher-value bet and it depends entirely on N1 producing a *selector*, not a metric.

---

## 5. Central question 2 — does any of these works already show the full-bag-vs-compact dose result?

**Yes. Three times, and SAEA's version is the weakest of the four by evidence standards.**

- **Ren, Shi & Li 2025 (2506.06252)** is the direct match: EWER **1.80 (exact) → 4.16 (~50) → 5.61
  (~1800)**, with WER also worsening at the large list (4.54 → 4.80), and entity filtering to
  "10–20 highly relevant candidates" recovering 5.61 → 4.95. Explicit conclusion that targeting
  beats volume. Caveat: a *trained* prompt-biasing ASR, in-house data.
- **RLBR 2026 (2601.13409)**: B-WER 0.59/2.11 @100 → 1.36/4.04 @1000 on LibriSpeech. Trained.
- **DeRAGEC (Table 2)**: U-shaped in k — 7.2 (k=1) / 6.6 (k=5) / **6.5 (k=10)** / 6.7 (k=15) — with
  precision collapsing 0.137 → 0.032 across that range. Frozen LLM, prompt-level, training-free.
  This is the closest match *in regime* to SAEA (frozen LLM consuming a prompt-level candidate list),
  and it already shows over-supply hurting.
- **Counterexample worth respecting**: Siskos et al. show the *opposite sign* — c = 100 → 250 helps,
  and 15.17× the oracle token count still wins on Earnings21. The reconciling variable is the
  **consumer**: a *trained* biasing module learns to ignore distractors and is dose-robust; a
  *frozen LLM reading a prompt* is dose-fragile and, past some length, starts copying. That
  mechanistic contrast — same dataset (Earnings-21), same context content, two consumers, opposite
  dose responses — is the single most defensible framing available to SAEA, because SAEA can
  measure the frozen-prompt arm on the dataset where the trained-CB arm is already published.
- Also relevant: ConEC row 3 is a *harmful-dose* result at the entity-type level (shared 3066-word
  distractor list degrades GPE/NORP/FAC below no-context), and DeRAGEC's Def-without-PS row is a
  *harmful-form* result (STOP hit 0.807 → 0.697).

**Consequence for SAEA's registration**: "full bag = no gain at 4× tokens" must be written as a
*replication under a new regime*, with these four citations in the same sentence, or a reviewer will
find them. What is not yet published is that curve **on a frozen, API-only omni, on real long-form
earnings-call speech, with the harmful-edit ledger attached** — measure it there and say so precisely.

---

## 6. Central question 3 — three attacks on N2's design, and the control arms that neutralise them

### Attack A — "Your roster gain is a prompt-copying artifact, not listening."
The strongest attack, and it now has a published weapon: Zhang et al. (2607.21943) show Qwen3-Omni
copies supplied context 94–99.8 % of the time and scores 100 % on the primary-transcript task **with
silent audio**. SAEA's own P2 already found 49/53 byte-identical replay outputs. A reviewer will
therefore assume any N2 roster gain is the model laundering supplied tokens into the transcript —
especially for PERSON entities, where roster tokens *are* the answer. Worse, the metadata roster
contains speaker names that the call's own turn-taking makes locally predictable, so copying is
*rewarded* by entity-WER.

**Control arms that neutralise it (all cheap, all mandatory):**
1. **Silent/shuffled-audio control** — identical roster prompt, audio replaced by silence or by a
   different speaker's clip from another call. Any entity-WER gain that survives is pure copying.
   Pre-register a kill threshold (e.g. gain under silent audio must be ≤ 10 % of the gain under true
   audio, else the arm is void). Adopt the framing and cite Zhang et al.
2. **Distractor-roster arm** — supply a roster from a *different, matched* earnings call (same
   sector, same quarter). If entity-WER improves, or if non-entity WER degrades by the same amount as
   under the true roster, the effect is prompt-conditioning, not evidence use.
3. **Copy-rate instrument as a first-class metric** — report, per output, the fraction of roster
   tokens emitted that were *not* in the reference (this is LOGIC's FAR, and it is the precise
   counterpart to the 49/53 byte-identity statistic). A gain with rising FAR is not a gain.

### Attack B — "This is ConEC row 4 with a chat wrapper."
ConEC already supplied slides + release + participant roster on Earnings-21 and got 10.41 → 10.29
overall / 26.02 → 24.84 rare. SAEA's n = 10 prior evidence (12.09 vs 12.38 macro, p = .19, +117
entity tokens) is a smaller effect at a smaller n, with a different decoder. A reviewer asks: what
did we learn that ConEC did not already publish in 2024?

**Control arms:**
1. **Run the ConEC context as an explicit arm.** The lists are public in `huangruizhe/ConEC`
   (`participant_names` + extracted biasing word lists). Three supply arms — zero / ConEC-public bag
   (~100–2000 words) / SAEA compact dataset-shipped roster — on the identical frozen-omni vehicle,
   at n = 44 (the full Earnings-21 file count, which is also ConEC's eval set). That converts
   "we did ConEC again" into "we measured what the same context is worth through a prompt channel
   instead of a shallow-fusion channel", a comparison nobody has run.
2. **Report the per-entity-type breakdown in ConEC's exact schema** (PERSON/ORG/GPE/LOC/PRODUCT/
   EVENT/NORP/FAC, plus non-entity WER). Direct commensurability with ConEC Table 2 is worth more
   than any novel metric, and it exposes the row-3-style harmful redistribution if it happens.
3. **Report the ConEC-style coverage ledger for the SAEA roster** (fraction of spoken entity tokens
   present in the supplied roster, by type). This is the honest denominator for the C1 legal-coverage
   claim and it is the number that tells you whether N2's ceiling is 12.09 or 10.88.

### Attack C — "Your n = 44 co-primary design cannot detect the effect you're claiming."
Prior effect is 12.38 → 12.09 macro WER (−0.29 pp) at n = 10 with p = .19; ConEC's real-context arm
moved overall WER by −0.12 pp; the forensics say guard-chain perfection is worth −0.28 pp on the
current aperture. Macro WER at n = 44 long-form calls is a low-power instrument for a sub-0.5 pp
effect with per-call variance dominated by call length and speaker mix. A reviewer (or the owner)
will say the co-primary macro ledger is decoration and the study is powered only for the entity
ledger — and if the entity ledger is the real primary, the harmful-edit ledger must bound the cost.

**Control arms:**
1. **Pre-register the entity-WER ledger as primary and macro WER as a non-inferiority guardrail**,
   not a co-primary. Non-inferiority margin fixed in advance (e.g. macro WER must not worsen by more
   than 0.15 pp), which is exactly what ConEC's non-entity column and Ren et al.'s general-set row
   are doing informally.
2. **Paired, within-call analysis with the call as the unit** — every arm decodes the identical
   windows; report paired differences with a bootstrap over calls (n = 44) *and* over the 8284-token
   entity ledger, and pre-register which is decisive. Report the per-call scatter, not just the mean;
   ConEC's own gains are the sum of a few big PERSON wins.
3. **Power the routing claim separately.** The forensic result (flag surfaced ~3 % of reachable error
   mass; oracle static supply = −12 pp entity-WER) says the interesting quantity is not "does the
   roster help" but "what fraction of the oracle-supply headroom does a given selector recover".
   Pre-register **fraction-of-oracle-headroom-recovered** as the reported effect size, with oracle
   supply as a run arm in the same block. That metric is dimensionless, comparable to ConEC row 5 and
   DeRAGEC Table 4, and stays interpretable at n = 44 where raw pp differences do not.

---

## 7. Consequences for the claim ladder (recommendation, not a decision)

- **C1 (legal coverage)** — reframe from "we supply legally obtainable evidence" to "coverage and
  conversion as a function of provenance tier". ConEC Table 1 is the baseline to beat/cite.
- **C2 (speech-aware routing)** — promote to the *primary* claim. It is the only one of the four
  deltas with no direct occupant in the training-free API-only regime. If N1 cannot produce a
  selector, the study has no headline.
- **C3 (verified use)** — treat as externally corroborated and largely pre-empted by
  arXiv 2607.21943. Retain SAEA's data as a *replication on a different task family* (entity-dense
  long-form ASR supply vs overlapped-speaker understanding) and stop treating it as a novel finding.
  Cite Zhang et al. and adopt their silent-audio control.
- **DEMO lane** — the mechanism is published (FSA-GRPO Table 1: 35.42 → 27.29 with 3-shot audio-text
  demos on frozen Qwen2.5-Omni; DeRAGEC's gold-built rationale demonstrations are the same
  construction pattern, offline-gold, ACL-published). Only **reject-case demonstrations** and the
  provenance-clean construction split remain unclaimed. Gate it behind N1 as planned, and
  pre-register it against the FSA-GRPO/DeRAGEC baselines explicitly.
- **Metric novelty** — claim none. HER/RIR must cite Edit Rate / Improve@Edit / Worsen@Edit
  (arXiv 2508.07285) **and** LOGIC's FAR, IBM's U-WER, ConEC's non-entity WER, ProfASR-Bench's
  NE-WER/Entity-F1.

## 8. Open items this read did not close

- Whether Earnings-21's dataset-shipped metadata CSVs actually contain the speaker roster at the
  fidelity ConEC obtained from Seeking Alpha (ConEC needed the scrape to lift PERSON coverage from
  30 % to 82 %; if the shipped CSVs are thinner, N2's compact roster is weaker than ConEC row 4 by
  construction, and the coverage ledger must be computed before the block runs).
- Ren et al. 2506.06252 uses an in-house domain corpus; its dose ladder is not reproducible, so it
  can be cited as prior claim but not as a comparable baseline.
- LOGIC reports no prompt-level baseline table; its "prompting is unusable" claim rests on internal
  sets and one qualitative example — worth stating explicitly when SAEA positions against it.
- `github.com/huangruizhe/ConEC` states no license. If SAEA runs the ConEC-context arm, the license
  question must be resolved before the artifact is consumed, and it belongs in the provenance ledger.
