# Task-Expansion Survey — References and Datasets for REFLECTION / Semantic-Leverage Phase

Date: 2026-08-15. Prepared for: speech-aware-evidence-acquisition (frozen Qwen3-Omni-30B, API-only, zero training).
Status: survey note only. No repo files touched, no datasets downloaded.

## Method and provenance

- `WebSearch` was budget-exhausted (200/200) at session start. Fallback used: **arXiv Atom API** swept directly
  (5 query batches, ~50 field-scoped queries), plus **DBLP API** for non-arXiv venue resolution, plus
  **WebFetch** for HuggingFace dataset cards and one ar5iv full text.
- For 17 papers the **PDF was downloaded and converted with `pdftotext`**, and the results sections were read.
  Those claims are tagged **[FT]**. Claims from abstract/card only are tagged **[ABS]**.
- Semantic Scholar API was rate-limited (429) and not used.
- Numbers below are quoted from the source; where a table was mangled by PDF column extraction, the
  narrative sentence is quoted instead and the table value is omitted rather than guessed.

---

## Question A1 — Knowledge/context injection for spoken QA and SLU on frozen models

### The closest published analogues to our roster injection

**Sun, Feng, Jiang, Zhang, Gales, Woodland (2023), "Speech-based Slot Filling using Large Language Models",
arXiv:2311.07418** — **[FT]. The single most transferable paper in this section.**
Frozen GPT-3.5/GPT-4/Vicuna prompted with task description + one-shot example + noisy Whisper transcripts on
SLURP. Introduces **LKI (linguistic knowledge injection)**: knowledge extracted from the N-best list is placed
in the prompt. LKI "almost doubled the SLU-F1" for Vicuna-13B under in-context learning; +3% absolute for
LLaMA-13B; best system +6.8% absolute SLU-F1 over a 1-best prompt. This is our exact architecture shape
(frozen LLM, prompt-side knowledge, no parameter change) on an SLU task with a slot ontology.

**Wang, Ma, Guo et al. (2025), "ContextASR-Bench: A Massive Contextual Speech Recognition Benchmark",
arXiv:2507.05727** — **[FT]. Already on our disk.**
Evaluates frozen LALMs (incl. **Qwen2.5-Omni-3B/7B**) under three matched settings: **Contextless /
Coarse-grained Context (summary + entity list) / Fine-grained Context (entity list)**. Metrics: WER,
**NE-WER** (WER restricted to entity spans, fuzzy match with edit-distance tolerance `ceil(n/2)-1`) and
**NE-FNR** (exact-match entity miss rate = 1 - recall). Two findings we should cite directly:
- Under Fine-grained Context, "LALMs show a significant reduction in NE-WER";
- but "although the NE-WER and NE-FNR metrics show big decreases, **the WER did not exhibit a similar
  reduction**." — This is the owner's dilution observation, already published. We are not the first to see it;
  we should cite it and then go past it to the *downstream* consequence, which they do not measure.

**Piskala (2025), "ProfASR-Bench: A Benchmark for Context-Conditioned ASR in High-Stakes Professional Speech",
arXiv:2512.23686** — **[FT]. Important negative result and a direct challenge to our claim.**
Builds a **"context ladder"**: matched `no-context / profile / domain+profile / oracle / adversarial`
conditions over finance, medicine, legal, tech. Reports a **"context-utilization gap (CUG)": "lightweight
textual context produces little to no" gain; oracle context yields "modest, model-dependent gains on
information-bearing tokens"**; systems are "nominally promptable yet" do not exploit the prompt. Evaluates
Whisper and **Qwen-Omni**. Caveat that matters: the audio is **TTS-synthesized (Kokoro voices)**, and the
release has a single `train` split, no held-out test. Our real-speech result (32%->20% entity-WER on
earnings calls) is a *counterexample* to their CUG conclusion and should be positioned against it explicitly.

**Huang, Yarmohammadi, Trmal, Liu, Raj, García, Ivanov, Ehlen et al. (2024), "ConEC: Earnings Call Dataset
with Real-world Contexts for Benchmarking Contextual Speech Recognition", LREC-COLING 2024,
aclanthology 2024.lrec-main.328** — **[FT]. This is the source of the corpus we just mined; cite it.**
It already quantifies the exact gap we independently rediscovered (see Q2 table). Contexts are slides,
earnings releases, **and participant names + affiliations**. Explicitly frames its own contexts as noisy:
"the real context contains only a limited coverage of named entities that are mentioned"; roughly 56%
coverage for PERSON and ORG from slides. License **CC BY-NC 4.0** (ELRA).

### Retrieval-augmented spoken QA (the RAG-for-speech line)

- **Min, Mundnich, Lapastora et al. (2024), "Speech Retrieval-Augmented Generation without Automatic Speech
  Recognition" (SpeechRAG), arXiv:2412.16500, ICASSP 2025** [ABS] — retrieves over speech embeddings to avoid
  ASR error propagation into retrieval; frozen-LLM-adjacent.
- **Lin, Lin, Chuang et al. (2024), "SpeechDPR: End-to-End Spoken Passage Retrieval for Open-Domain Spoken
  QA", arXiv:2401.13463, ICASSP 2024** [ABS] — the retriever side of open-domain SQA on NMSQA.
- **Hu, Li, Qi et al. (2025), "End-to-end Contrastive Language-Speech Pretraining for Long-form Spoken QA",
  arXiv:2511.09282, AAAI 2026** [ABS] — long-audio SQA via a speech retriever; relevant because our calls
  are long-form.
- **Chen, Ji, Wang et al. (2025), "WavRAG: Audio-Integrated Retrieval Augmented Generation for Spoken Dialogue
  Models", arXiv:2502.14727** [ABS].
- **Song, Shrestha, Lyu et al. (2026), "MedSpeak: A Knowledge Graph-Aided ASR Error Correction Framework for
  Spoken Medical QA", arXiv:2602.00981** [FT] — KG-retrieved semantic+phonetic entity context injected for
  correction *and* answer prediction. Caveat: audio is `pyttsx3` TTS; the headline system is **fine-tuned**
  (Llama-3.1-8B, 8xA100), so it is not a frozen-core precedent — only its zero-shot rows are.

### How the literature controls answer leakage (the owner's specific question)

There is **no single named "leakage control" protocol** in speech; there are four distinct practices, and we
should adopt a named combination of them:

1. **Distractor-padded biasing lists.** The canonical protocol is **Le, Jain, Keren et al. (2021),
   "Contextualized Streaming End-to-End Speech Recognition with Trie-Based Deep Biasing and Shallow Fusion",
   arXiv:2104.02194, Interspeech 2021** [ABS] — the biasing list contains the true rare words *plus* a large
   pool of distractors, so the list cannot be read as a cheat sheet and performance is reported as a function
   of list size. ConEC uses this system as its baseline row [FT]. **This is the control we should port**: our
   roster should be reported at several distractor levels, not only at the true-names-only level.
2. **Matched context ladder with an explicit oracle rung.** ConEC (`No biasing / real context / oracle`) and
   ProfASR-Bench (`no-context / profile / domain+profile / oracle / adversarial`) both make the oracle an
   explicit, separately reported condition rather than the headline. ProfASR-Bench additionally includes an
   **adversarial** rung (wrong context), which we currently do not have and should add.
3. **Deleting items the pipeline has made structurally unanswerable.** Spoken-SQuAD removes any QA pair whose
   answer span no longer appears in the ASR transcript [FT]; ODSQA and DRCD-TTS do the same. Note this is a
   *leakage-adjacent* control that biases the benchmark **toward optimism**, not pessimism (see Q2).
4. **Oracle-transcript upper bound as a separate system row.** SLUE phase-2 reports a "pipeline-oracle";
   Audio2Tool includes "an oracle setting in which Whisper transcripts are replaced with ground-truth queries
   to isolate the impact of ASR errors" [FT].

**Gap we can claim:** nobody in this set reports an entity-level *containment* audit — i.e. proving that the
injected text does not contain the answer string for semantic tasks. For our REFLECTION design on spoken QA,
supplying "the retrieved most-similar reference text" is exactly the operation that can trivialize the task,
and the literature does not give us a ready-made control. We should define one (answer-string exclusion +
distractor padding + adversarial rung) as a methodological contribution.

---

## Question A2 — ASR error propagation to downstream tasks, QUANTIFIED

This is the evidence base for the leverage hypothesis. Ranked by usefulness to us:

| # | Source | Speech | Task | ASR quality | Gold-text score | ASR score | Delta |
|---|---|---|---|---|---|---|---|
| 1 | **Spoken-SQuAD**, Li, Wu, Liu, Lee (2018), arXiv:1804.00320 [FT] | TTS | extractive QA | **22.73% WER** | F1 **74.54** / EM 64.41 (avg over SOTA models) | F1 **55.40** / EM 41.96 | **-19.1 F1 (-25.7% rel); -22.5 EM (-34.9% rel)** — *and see the structural finding below* |
| 2 | **ODSQA**, Lee, Wang, Chang, Lee (2018), arXiv:1808.02280 [FT] | **real human** (25.3 h, 20 spkrs, Chinese) | extractive QA | **19.11% WER** (doc), 18.57% (question) | F1 **81.05** (avg, 5 models) | F1 **63.67** | **-17.4 F1 (-21.5% rel)** |
| 3 | **SLURP slot filling**, Sun et al. (2023), arXiv:2311.07418 [FT] | real human | SLU slot filling (SLU-F1) | Whisper medium **14.6% WER** | GPT-4 in-context **53.6**; Flan-T5-base (tuned) **86.3** | GPT-4 **47.0**; Flan-T5 **66.5** | **frozen GPT-4: -6.6 (-12.3% rel); tuned model: -19.8 (-22.9% rel) ≈ 1.36 SLU-F1 points lost per WER point** |
| 4 | **SLUE phase-2**, Shon, Arora, Lin et al. (2023), ACL 2023, arXiv:2212.10525 [FT] | **real human** | spoken QA (frame-F1) | varies by ASR | pipeline-oracle "significantly outperforms all baseline models" | — | **Pearson r = -0.89 (p<0.01) between document WER and frame-F1** |
| 5 | **ConEC**, Huang et al. (2024) [FT] | **real human, earnings calls** | contextual ASR (entity WER) | Earnings-21 | PERSON-WER **45.9** no biasing | **39.8** with real ConEC documents; **13.0** with oracle entity list | real docs **-13% rel**; **oracle -71.7% rel** |
| 6 | **MedSpeak**, Song et al. (2026), arXiv:2602.00981 [FT] | TTS | medical multiple-choice QA | **7.72% WER** | base LLM on gold text **56.3%** | base LLM on ASR **50.2%** | **-6.1 pts (-10.8% rel)** |
| 7 | **Korean SQA cascade**, Jung & Choi (2026), arXiv:2605.17443 [FT] | TTS + noise | spoken QA | CER 0.07 -> 0.50 | — | — | baseline-relative F1 recovery **99% -> 96% -> 67%**; degradation "consistent across LLMs with different absolute performance" |
| 8 | **SD-QA**, Faisal, Keshava, Alam, Anastasopoulos (2021), EMNLP-Findings, arXiv:2109.12072 [FT] | **real human**, 24 dialects | passage selection / minimal answer | WER 11 - 49 by variety | Gold questions | ASR questions | **-0.3 to -13 F1 points** by dialect (Kiswahili avg -12.1; Bengali -0.8; Arabic -0.7) |
| 9 | **Semantic Distance**, Kim, Arora, Le et al. (2021), arXiv:2104.02138 [ABS] | real | intent/slot/semantic parsing | — | — | — | argues WER "is sometimes not a good indicator" for NLU; proposes SemDist |

### THE strongest quantified finding for the leverage hypothesis

**Spoken-SQuAD (arXiv:1804.00320) [FT], verbatim:** *"If the answer of a question did not exist in the ASR
transcriptions of the associated article, we removed the question-answer pair from the dataset."* The result:
SQuAD's ~87,599 train and ~10,570 dev QA pairs were reduced to **37,111 train and 5,351 test** — i.e. at
**22.7% WER, roughly half of all questions (≈58% of train, ≈49% of dev) became structurally unanswerable
because the answer span itself had been destroyed by ASR.**

This is the leverage hypothesis in its sharpest published form, and it is *stronger* than the headline F1
drop, because:
- the answer span is overwhelmingly a **content word / named entity**, so this is an entity-error effect, not
  a general-WER effect;
- 22.7% WER did not cost 22.7% of the task — it **eliminated the task outright for ~half the items**;
- every published F1 number for Spoken-SQuAD (74.5 -> 55.4) is measured **only on the surviving, easier
  half**, so the literature's own reported degradation is a systematic *under*-estimate of entity-error cost.

Corollary for our design: a benchmark that silently drops answer-destroyed items will hide exactly the effect
we are trying to demonstrate. **We should retain those items and score them as failures** — that alone should
produce the qualitative flips the owner predicts, and it is a defensible methodological difference from prior
work.

Supporting mechanism claim, from SLURP slot filling [FT]: *"the degradation in recall was more than the
degradation in precision when the ASR error rate increased, as important entities tended to be incorrectly
recognised by the generic Whisper systems"* — i.e. the downstream loss is entity-recall-driven, matching our
roster mechanism.

---

## Question A3 — Draft-then-verify / reflection paradigms in speech

### Beyond Voice Memory and RECOVER: what each actually does, and the hole they leave

**Voice Memory (Yang, Chen, Zelasko, Chen, Balam, Ginsburg, 2026), arXiv:2607.26410** [FT] — closer to our
design than the owner may realise, and it defines metrics we should adopt.
- Inference-only, frozen corrector, **act/abstain per utterance**, persistent `memory.md` revised offline by a
  score-gated optimizer. Explicitly **"no audio and no training, and runs entirely at inference."**
- Numbers: weighted WER **8.36% -> 7.52%** across 10 HyPoradise domains, no dataset regressed below 1-best;
  air-travel commands 8.40% -> 3.40%; CHiME-4 12.69% -> 10.46%.
- **The over-correction result is the one to quote:** unconstrained GER "breaks correct tokens on up to **64%**
  of its edits on financial news"; Voice Memory reduces that to **35%**.
- **Two importable metrics:** **Harmful Edit Rate (HER)** = fraction of token edits that break an
  already-correct token; **Recoverable Information Ratio (ρ)** = fraction of the 1-best-to-oracle WER gap
  closed. They report **ρ correlates with 1-best WER at r=+0.90** — i.e. correction helps where headroom is,
  which predicts that our REFLECTION gains will concentrate in the high-error spans we select.
- **The hole: no audio re-grounding.** This is precisely the axis our REFLECTION adds.

**RECOVER (Kumar & Sachdeva, 2026), arXiv:2603.16411** [FT] — the direct entity-repair competitor, and it
runs on our exact data.
- Whisper-small at 5 temperatures -> 5 hypotheses; entity candidates retrieved by exact + fuzzy + phonetic
  match (top-K=200); GPT-4o applies constrained edits. Strategies: 1-Best, Entity-Aware Select, ROVER
  Ensemble, LLM-Select.
- Evaluated on **Earnings-21 (2,086 segments, 38.8 h, 1,013 person/org/product entities, 6,535 entity tokens)**,
  **ATCO2-test-set-1h (560 segments, 1.1 h, 446 callsign entities)**, Eka-Medical, Common Voice, ContextASR-Bench.
- Results: **8-46% relative E-WER reduction**; Earnings-21 **33-35% RWERR** across all strategies; entity
  **recall +11.6 pp** on Earnings-21, +8.2 pp on ATCO2, +21.5 pp on Common Voice. Note ATCO2 fusion can
  *degrade* overall WER (48.63% -> 64-66%) via insertion noise.
- **Calibration for us:** our measured 32% -> 20% entity-WER is a **37.5% relative reduction on real
  earnings-call audio** — the same order as RECOVER's 33-35% on Earnings-21, but achieved with **prompt-side
  roster injection into a single frozen omni core**, with **no second LLM, no N-best ensemble, and no
  GPT-4o**. That framing is the paper.

**ClozeGER — Hu, Chen, Qin, Zhu, Chng, Li (2024), "Listen Again and Choose the Right Answer", ACL 2024,
arXiv:2405.10025** [ABS] — **the missing citation for the audio-re-grounding half of REFLECTION.** Diagnoses
exactly our risk: "LLMs are unaware of the source speech during GER, which may lead to results that are
grammatically correct but violate the source speech content." Fix: feed source speech to a multimodal LLM
(SpeechGPT) *and* reformat correction as a **cloze test with logits calibration** to strip N-best redundancy.
Our REFLECTION is the frozen-core, retrieval-grounded descendant of this.

**Two more that close the loop:**
- **PMF-CEC — He & Toda (2025), "Phoneme-augmented Multimodal Fusion for Context-aware ASR Error Correction
  with Error-specific Selective Decoding", TASLP 2025, arXiv:2506.11064** [ABS] — extends their ED-CEC
  (**error detection then context-aware correction**) with selective decoding. This is the *span-selection*
  half of REFLECTION (which spans are suspicious) done properly.
- **RAS — Huang, Qiu, Li et al. (2026), "RAS: a Reliability Oriented Metric for ASR", Interspeech 2026,
  arXiv:2604.24278** [ABS] — an **abstention-aware transcription framework** and metric, for systems that
  "produce confident yet incorrect transcriptions." This is the evaluation vocabulary for our abstention
  fallback; without it, abstention looks like a WER regression.

**The text-bias warning we must design against (two independent papers):**
- **Wang, Deng, Yang, Qiu, Zhang (2025), "When Audio and Text Disagree: Revealing Text Bias in Large
  Audio-Language Models" (MCR-BENCH), EMNLP 2025 Main, arXiv:2508.15407** [ABS] — when audio and text
  conflict, LALMs "display a significant bias toward textual input, frequently disregarding audio evidence,"
  with "persistent overconfidence even with contradictory inputs."
- **Hu, Qiu, Wang, Liu, Sang (2025), "VAPO: End-to-end Slide-Enhanced Speech Recognition with Omni-modal
  LLMs", ACL 2026 Main, arXiv:2510.08618** [ABS] — names the failure **"Visual Interference": OLLMs "show a
  bias towards visible text over auditory signals, causing them to hallucinate slide content that was never
  spoken."** Their fix is a **"Look-then-Listen"** decoupled inference chain (extract context priors in a
  `<think>` block, then transcribe in an `<answer>` block).
- **Wang, Ma, Luo et al. (2025), "MATA: Pay More Attention To Audio", arXiv:2509.18816** [ABS] — same
  phenomenon at the attention level.

**This is the single biggest risk to REFLECTION as specified.** Handing the model "the retrieved most-similar
reference text" alongside a suspicious span is *exactly* the MCR-BENCH conflict condition. Mitigations
available off the shelf: VAPO's ordered `<think>`(context) -> `<answer>`(transcribe) prompt structure; Voice
Memory's act/abstain gate; ProfASR-Bench's **adversarial context rung** as the test that proves we did not
just build a copy machine. **Recommendation: add a deliberately wrong-reference arm to the REFLECTION design
before running it.** If the model copies the wrong reference, the paradigm is measuring text-following,
not audio verification.

Also worth noting for the "own errored draft" element: no paper found supplies the model **its own errored
hypothesis + a retrieved reference + the audio simultaneously**. ClozeGER has audio + N-best; RECOVER has
N-best + retrieved entities (no audio); Voice Memory has N-best + memory (no audio). **The three-way
combination appears to be unclaimed.**

---

## Question A4 — Meeting-speech understanding with knowledge (AMI family)

Thinner than expected; the meeting-QA line is largely **transcript-only**, which weakens it for us.

- **Prasad, Bui, Yoon, Deilamsalehy, Dernoncourt, Bansal (2023), "MeetingQA: Extractive Question-Answering on
  Meeting Transcripts", ACL 2023, aclanthology 2023.acl-long.837** [ABS] — built on AMI; questions asked by
  participants inside the meeting.
- **Apel, Braude, Kantor et al. (2023), "MeeQA: Natural Questions in Meeting Transcripts", arXiv:2305.08502**
  [ABS] — 48K QA pairs from 422 transcripts; questions are real in-meeting questions, "not always clear."
  Released on GitHub only, **no license file**.
- **Shinde, Besacier, Bojar et al. (2025), "Findings of the Third AutoMin Challenge", arXiv:2509.13814** [ABS]
  — 2025 added a **QA-over-meeting-transcripts task**; a live shared-task baseline pool.
  **Kang, Vartampetian, Herron et al. (2025), "GETALP@AutoMin 2025", arXiv:2508.00476** [ABS] is a
  RAG-over-meeting-transcripts system paper from that task.
- **Zhong, Yin, Yu et al. (2021), "QMSum", NAACL 2021, arXiv:2104.05938** [ABS] — query-based meeting
  summarization over AMI/ICSI; **text only**.
- **Hu, Ganter, Deilamsalehy et al. (2023), "MeetingBank", ACL 2023, arXiv:2305.17529** [ABS] — 3,579 h of
  city-council meetings; the broader release includes **agenda and minutes PDFs**, which is the natural
  participant/agenda grounding source, though not exposed as HF columns.
- **Yang, Ni, Yang et al. (2026), "LongSpeech", ICASSP 2026, arXiv:2601.13539** [ABS] — long-form audio
  understanding benchmark explicitly motivated by "meeting transcription, spoken document understanding."
- **Yin, Chen, Deng et al. (2025), "SpeakerLM", AAAI 2026, arXiv:2508.06372** [ABS] — "who spoke when and
  what" end-to-end; relevant if speaker-roster grounding becomes an OBS-side variable.

**Assessment: the AMI-family entity-sensitivity question is under-studied.** No paper found measures meeting-QA
accuracy as a function of participant-name recognition accuracy. That is a real gap, but it is a *gap needing
new annotation*, not a cheap next experiment — the meeting QA sets ship without aligned audio.

---

## Question A5 — Spoken tool-calling / voice agents with knowledge injection

- **Pahwa, Beedu, Priye et al. (2026), "Audio2Tool: Speak, Call, Act", arXiv:2604.22821** [FT] — already on
  our disk. ~30,000 queries, 3 domains (Smart Car / Home / Wearables), **8 complexity tiers**. Metrics:
  **Tool Accuracy** (tool name / ordered tool sequence), **Exact Match** (tool + all arguments after
  deterministic normalization), **Slot F1** (micro-averaged over arguments). Includes an **oracle text
  condition "to isolate the impact of ASR errors."**
  **It benchmarks Qwen-3-Omni-30B — our exact core** — which achieves >75% on Tier-1 commands but
  **"under 55% on the F1 and EM metrics"** on Tiers 5-7, and accuracy "below 56%" on Tiers 7-8.
  Also: "end-to-end SpeechLMs do not yet consistently outperform strong ASR-LLM pipelines."
  **Caveat: all audio is zero-shot voice-cloning TTS (Qwen3TTS et al.) with injected noise; queries were
  generated by Claude Opus and filtered by an LLM-as-judge.**
- **Laskar, Fu, Sarfjoo et al. (2026), "From Text to Voice: A Reproducible and Verifiable Framework for
  Evaluating Tool Calling LLM Agents", arXiv:2605.15104** [ABS] — converts *verified text* tool-calling
  benchmarks into audio via TTS + speaker/noise variation **without re-annotating tool schemas or gold
  labels**. This is the methodologically cleanest way to get a spoken tool-calling task with trustworthy
  labels, and it is a recipe we could apply rather than a corpus we must download.
- **Bhosale, Rajgarhia, Pothanapalli et al. (2026), "DuplexWorld: Can voice agents help you get through the
  day?", arXiv:2608.10716** [ABS] — voice agents "shaped as tests of agentic tool calling **against a
  database**" — i.e. slot values come from a DB, which is the roster analogue.
- **Lin, Xu, Sun et al. (2025), "WearVox", arXiv:2601.02391** [ABS]; **Zhang, Chen, Wu et al. (2026),
  "DuplexSLA", arXiv:2605.20755** [ABS] — full-duplex/in-conversation tool calling; peripheral.

**Boundary note:** every strong spoken-tool-calling resource found is **TTS-synthesized**, and speech-to-action
is outside the study's currently enumerated scope (ASR / entities / biasing / spoken-QA / meeting). Anything
here is **"needs boundary amendment"**, and additionally needs a synthetic-speech validity argument.

---

## Question B — Dataset evaluation

Facts below are from HuggingFace cards / official repos fetched this session. "not stated" means the card does
not state it — not that the value is unknown to the world.

| # | Dataset | Task + metric | Entity-dependence (why injection should matter) | Size / practicality | License | Port to our machinery |
|---|---|---|---|---|---|---|
| 1 | **SlideASR-Bench** `RUIH/SlideASR-Bench` (VAPO, arXiv:2510.08618) | entity-rich ASR; WER + entity errors | **`entity_list` field, 5-14 entities per example** — the roster is literally shipped per item | **10.8 GB**, 8,467 rows (train 6,410 synthetic / **test 2,057 real-world**) | **MIT** | Best structural match on the list. Use the **real-world test split only**; consume `entity_list` as text roster, **ignore the slide images** (keeps us inside the speech+language boundary). Gives a published frozen-model baseline (VAPO) to compare against. |
| 2 | **SLUE-SQA-5** `asapp/slue-phase-2`, config `sqa5` | spoken QA, **frame-F1** | ships **`document_audio` + `raw_document_text`/`normalized_document_text`** per question, plus `word2time` and `answer_spans` | test **7.00 GB**, **verified_test 1.18 GB** (408 items) — *train is 135 GB, do not fetch* | **cc-by-4.0** (confirmed on the `asapp/slue-phase-2` card; HVB inherits Harper Valley's CC-BY-4.0) | The cleanest spoken-QA target: real human speech, per-question document, and a published **WER<->frame-F1 correlation of -0.89** to anchor the leverage claim. `verified_test` (408) is a perfect bounded-probe size. |
| 3 | **HALAS** `MatBar99/HALAS` (arXiv:2606.23048) | ASR hallucination span detection | 44 columns; **span-level human hallucination annotations** for 9-10 ASR systems | **~3.8 MB total** (train 2,866 / test 745) | **"unknown" on card** — resolve before use | **Nearly free, and it joins to Earnings-22, which we already hold** (`e22_reference_text`, join key `audio_id`). This is ground truth for **which spans are suspicious** — the REFLECTION trigger — on our own audio. Highest value-per-byte on this list. |
| 4 | **SLURP** `qmeeus/slurp` (official: github.com/pswietojanski/slurp, Zenodo 4274930) | SLU intent (91 classes) + slot filling, **SLU-F1** | `entities` (span+type), `sentence_annotation`, 18-domain ontology; recordings carry **precomputed `wer` and `ent_wer`** | **6.75-6.8 GB**, 141,649 rows (train 50.6k / devel 8.69k / test 13.1k) | text **CC BY 4.0**, **audio CC BY-NC 4.0** (Zenodo labels it "Other (Non-Commercial)") | Real human speech; the slot ontology is a naturally-available inference-time knowledge source; and **arXiv:2311.07418 gives us a frozen-GPT-4 baseline table on this exact split** to compare against. The best "qualitative flip" testbed we can get cheaply. |
| 5 | **HeySQuAD** `yijingwu/HeySQuAD_human` | spoken QA, EM/F1 | per-example **`context`** (full SQuAD passage) + `transcription` | human **14.6 GB** / 76.1k rows; machine 10.4 GB / 98.2k | **CC BY 4.0** | Real *human-spoken questions* (rare); passage is the natural context. Weakness: the passage contains the answer by construction — needs our answer-exclusion control. |
| 6 | **ConEC** (already on disk) | contextual ASR; WER, entity-WER | real slides, releases, **participant names + affiliations** | already held | **CC BY-NC 4.0** | Incumbent. Cite its oracle-vs-real gap as our motivation. |
| 7 | **ContextASR-Bench** (already on disk) | contextual ASR; **NE-WER, NE-FNR** | entity list as context; 3-rung context ladder | already held | see card | Incumbent. Its NE-WER/NE-FNR definitions should become our metric standard. |
| 8 | **Spoken-SQuAD** github.com/chiahsuan156/Spoken-SQuAD; mirror `AudioLLMs/spoken_squad_test` | spoken QA, EM/F1 | SQuAD `context` passage | full audio zip **~50 GB**; **test-only mirror 3.4 GB / 5,351 rows** | **CC BY-SA 4.0** | Fetch the **test-only mirror**. Value is as the *reference point for the strongest leverage finding*, plus its two noise conditions (WER 44.22% / 54.82%). **TTS audio.** |
| 9 | **MSNER** `qmeeus/MSNER` (arXiv:2405.11519) | speech NER on VoxPopuli | `unified_entities` / `raw_entities` (BIO, 105 raw types) | **3.33 GB**, 6,254 rows (de/es/fr/nl only) | **not stated** | Multilingual entity stress test with audio included. Non-English only in practice — deprioritize unless we want a generalization arm. |
| 10 | **ProfASR-Bench** `prdeepakbabu/ProfASR-Bench` | context-conditioned ASR; entity-aware scores | **`prompt`** (1-3 context prompts) + **`profile`** (speaker context) — mirrors our deployment-legal metadata condition | 3,200 rows; single `train` split, **no test split** | **Apache-2.0** | Cheap, and its **CUG negative result is the claim we would be rebutting**. But **TTS (Kokoro voices)** and no held-out split — use as a *secondary* comparison, never as a headline. |
| 11 | **NMSQA** `voidful/NMSQA` | spoken QA | SQuAD `context` | 98.3k rows; **audio only as `nmsqa_audio.tar.gz`, must extract and join** | **not stated** | Extra plumbing for no extra leverage over SLUE-SQA-5. Skip for now. |
| 12 | **MeetingBank** `huuuyeah/meetingbank` + `huuuyeah/MeetingBank_Audio` | meeting summarization | agenda/minutes PDFs exist in the broader release but **not as HF columns** | text 115 MB; **audio 198 GB** | **CC BY-NC-SA 4.0** | Audio cost is prohibitive relative to payoff. Defer. |
| 13 | **QMSum** `pszemraj/qmsum-cleaned` | query-based meeting summarization, ROUGE | query is embedded in `input`, not a column | 49.1 MB, 3,620 rows | Apache-2.0 | **Text only; no audio, and the card gives no AMI/ICSI alignment help.** Not usable as a speech task without work we should not do now. |
| 14 | **ATCO2-test-1h** `Jzuluaga/atco2_corpus_1h` (already on disk); **`Jzuluaga/uwb_atcc`** | ATC ASR; WER, callsign accuracy | **Negative result: the HF ports expose only `id/audio/text/timestamps` — no callsign column, no NER column.** The surveillance-derived callsign lists require the full ATCO2 distribution under an End-User Data Agreement | atco2-1h 113 MB / 871 rows; **uwb_atcc 711 MB, 14,113 rows, ~20 h** | atco2: **End-User Data Agreement** (non-standard); uwb_atcc: **CC BY-NC-SA 4.0** | The callsign-roster story is real (**RECOVER used 446 callsign entities on this exact 1-h set**) but **the roster is not in the HF port** — we would have to reconstruct it from RECOVER's setup or obtain the full ATCO2 release. Downgrade from "naturally available roster" to "roster requires acquisition." |
| 15 | **SD-QA** `WillHeld/SD-QA` | dialectal spoken QA | **no passage/context column** on the mirror (TyDi-QA open-retrieval derived) | 2.03k rows | **not stated** (GitHub repo Apache-2.0) | Question-side ASR noise only; effect sizes small (-0.3 to -13 F1). **No naturally available roster.** Low priority. |
| 16 | **PriMock57** github.com/babylonhealth/primock57 | medical consultation ASR | **clinician-written consultation notes** per consultation — a genuine real-document context, but as files not columns | 57 consultations; Git LFS; hours not stated | **CC BY 4.0** | Attractive ConEC-analogue in a second domain (real speech + real per-session documents). Small. Worth a look after the earnings-call work lands. |
| 17 | **VoxPopuli** `facebook/voxpopuli` | multilingual ASR | `speaker_id/gender/accent` only — **no document, entity list, or ontology** | **673 GB**, 1,791 transcribed h | **CC0-1.0** | Entity-rich but **no naturally available roster**, and huge. Skip; take MSNER instead if we want its entities. |
| 18 | **SPGISpeech 2.0** `kensho/SPGISpeech2.0` | speaker-tagged financial ASR | speaker breaks via `\|`; word-level alignments | **421 GB**, 3,780 h | **gated, `kensho-research`, noncommercial-research only, contact info required** | Same domain as us, but gated + enormous + no entity roster. Skip. |
| 19 | **Audio2Tool** (already on disk) | spoken tool calling; Tool Acc / EM / Slot F1 | slot values from tool schemas | already held | see card | **Needs boundary amendment** (speech-to-action). Also **TTS audio**. Its value is that it already benchmarks Qwen-3-Omni-30B, giving us a same-model baseline for a semantic task. |
| 20 | **Earnings25** (arXiv:2607.23813) | finance ASR, 498 h + 46 h | promises "speaker roles, industry labels, and call structure" metadata | **not released** — no URL on the arXiv page, not on HF | n/a | Watch item. If released, it is the natural scale-up of our current corpus. |
| 21 | **MeeQA** github.com/reutapel/MeeQA | meeting QA | transcript-only | ~41.6 MB | **no license file** | Licence-blocked; transcript only. Skip. |
| 22 | **LongSpeech** `ATH-MaaS/Marco_Longspeech` | long-audio transcription/understanding | chat-format `messages`; no dedicated context field | **2.03 TB** | Apache-2.0 | Size disqualifies it for a bounded probe. |

---

## Final ranked recommendations

### Top 5 papers to read deeply this week

1. **Voice Memory — arXiv:2607.26410 (Yang et al., 2026)** [already partly read; read in full].
   Despite being known to the team, it is the paper whose *methods* we most need: the act/abstain formulation,
   the **Harmful Edit Rate**, and the **Recoverable Information Ratio ρ** with its r=+0.90 correlation to
   1-best WER. Adopting HER and ρ gives REFLECTION an over-correction guardrail and a headroom-normalized
   effect size, which is exactly what a reviewer will demand when our entity gains dilute in WER. And its
   explicit "no audio" scope statement is the cleanest possible articulation of the hole we fill.

2. **Sun, Feng, Jiang, Zhang, Gales, Woodland (2023), "Speech-based Slot Filling using LLMs" —
   arXiv:2311.07418.** The best available template for our next experiment: frozen LLM, prompt-side knowledge
   injection, a real-speech SLU task, and a full WER-vs-SLU-F1 grid (0% / 14.6% / 19.8% / 26.4% / 33.4%). It
   supplies both the leverage curve (≈1.36 SLU-F1 points per WER point) and the causal attribution (recall
   loss from entity misrecognition). It is also directly reusable: SLURP is cheap and its baselines are public.

3. **ConEC — Huang et al., LREC-COLING 2024 (aclanthology 2024.lrec-main.328).** We are already consuming
   this corpus; we should not run another experiment on it without having read its Table 2. It quantifies our
   own finding before us: real documents move PERSON-WER 45.9 -> 39.8, oracle entity lists move it to 13.0.
   That single row pair defines the headroom our REFLECTION delivery is trying to capture and tells us exactly
   how much of the gap is coverage versus delivery.

4. **MCR-BENCH — Wang, Deng, Yang, Qiu, Zhang, EMNLP 2025, arXiv:2508.15407**, read together with
   **VAPO — Hu et al., ACL 2026, arXiv:2510.08618.** These two are the strongest threat to REFLECTION's
   validity: audio-language models prefer text over audio under conflict, with persistent overconfidence, and
   omni models specifically hallucinate provided context that was never spoken. Read before finalizing the
   prompt, because VAPO's `<think>`-context-then-`<answer>`-transcribe ordering is a ready mitigation and
   MCR-BENCH's conflict protocol is a ready diagnostic.

5. **RECOVER — arXiv:2603.16411 (Kumar & Sachdeva, 2026)** [known to the team; read the results section].
   It is the number our result will be compared to (33-35% relative E-WER reduction on Earnings-21, entity
   recall +11.6 pp), on the same corpus family. Reading it precisely tells us which claims are already taken
   and which framing is still ours — namely single frozen core, no second LLM, no N-best ensemble.

*Runner-up if time allows:* **ClozeGER, arXiv:2405.10025** (ACL 2024) — the prior art for "listen again"
correction, and the paper that first named the failure mode REFLECTION is designed around.

### Top 5 datasets to download first

1. **HALAS (`MatBar99/HALAS`) — ~3.8 MB.** Download first, today. It is span-level human hallucination
   annotation over **Earnings-22, which we already hold**, joining on `audio_id`. REFLECTION's first
   unsolved subproblem is *which spans are suspicious*; this is labelled ground truth for that decision on our
   own audio, at essentially zero acquisition cost. Resolve the "unknown" license before any publication use.

2. **SLUE-SQA-5 `verified_test` (1.18 GB) + `test` (7.00 GB) from `asapp/slue-phase-2`.** The cleanest route
   from ASR to a semantic task on **real human speech** with a **per-question document** already in the
   corpus — the structural analogue of our ConEC discovery, but for spoken QA rather than ASR. The published
   document-WER-to-frame-F1 correlation of -0.89 gives us a prior to test our leverage hypothesis against, and
   the 408-item `verified_test` is right-sized for a bounded discovery probe. **Do not pull the 135 GB train
   split.** Confirm licensing before use.

3. **SLURP (`qmeeus/slurp`, 6.75 GB; or Zenodo 4274930).** Real human speech, an explicit 18-domain slot
   ontology usable as an inference-time knowledge source, per-recording `ent_wer` already computed, and — the
   decisive factor — **an existing frozen-GPT-4 in-context baseline table on this exact test set**
   (arXiv:2311.07418) that we can drop Qwen3-Omni into for a same-protocol comparison. This is where the
   "entity fix -> qualitative flip" claim can be demonstrated most cheaply. Note the audio is **CC BY-NC 4.0**.

4. **SlideASR-Bench test split (`RUIH/SlideASR-Bench`, 10.8 GB total, MIT).** The only corpus found that ships
   a **per-example `entity_list`** — a roster, by construction — with **real-world audio in its test split**
   and a published frozen/RL-tuned omni baseline (VAPO). Consume the audio and `entity_list` text only and
   leave the slide images unused, which keeps it inside the human-speech-and-language boundary. It is the
   fastest way to show our roster machinery transfers off earnings calls.

5. **Spoken-SQuAD test mirror (`AudioLLMs/spoken_squad_test`, 3.4 GB, CC BY-SA 4.0).** Small, and it is the
   substrate of the strongest quantified leverage finding we have. Two things to do with it: reproduce the
   74.5 -> 55.4 F1 gap with our frozen core, and — the novel move — **restore the ~50% of QA pairs the
   original authors deleted** because the answer span was destroyed, and score them as failures. That single
   protocol change should surface the qualitative flips the leverage hypothesis predicts, on a benchmark
   everyone already knows. Caveat: TTS audio, so it is a mechanism demonstration, not a deployment claim.

*Deliberately not recommended now:* VoxPopuli (673 GB, no roster), SPGISpeech 2.0 (gated, 421 GB),
MeetingBank audio (198 GB), LongSpeech (2.03 TB), QMSum/MeeQA (no audio), SD-QA (no context field),
Audio2Tool expansion (boundary amendment + TTS), Earnings25 (not released).

### Boundary flags for the owner

- **Needs boundary amendment:** Audio2Tool, "From Text to Voice" (arXiv:2605.15104), DuplexWorld, WearVox —
  all speech-to-action. Language content, but outside the enumerated ASR/entities/biasing/spoken-QA/meeting scope.
- **Synthetic-speech validity flag (in scope by content, but not real human speech):** ProfASR-Bench (Kokoro
  TTS), Spoken-SQuAD, MedSpeak's corpus (pyttsx3), Audio2Tool (voice-cloning TTS), SlideASR-Bench **train**
  split (its test split is real). Every one of these should carry an explicit "synthetic speech" caveat if it
  appears in a claim.
- **Not applicable / correctly excluded:** no general-audio corpora (AudioSet/FSD50K/ESC-50 class) appear
  anywhere in this survey. SlideASR-Bench is the only borderline case and is handled by consuming text+audio
  only, never the images.
- **SLUE phase-2 licence RESOLVED: cc-by-4.0** (confirmed on card) — it is no longer a blocker.
- **License blockers to resolve before any published claim:** HALAS ("unknown"),
  MSNER (not stated), `WillHeld/SD-QA` (not stated), MeeQA (no license), ATCO2 (End-User Data Agreement),
  SPGISpeech 2.0 (gated). SLURP audio and ConEC are **NC** — fine for research, flag for any commercial claim.

---

# EXTENSION — Agentic-Era Task System (owner scope extension, 2026-08-15)

## E1. Citation-task matrix: what every cited work actually evaluates

Columns: **Eval tasks/benchmarks** | **Metric family** | **Level**. Level codes:
**T** = transcript-level (WER / B-WER / E-WER / NE-WER / NE-FNR / HER);
**A** = answer- or label-level (EM / F1 / accuracy / judge score / AST match);
**E** = **end-to-end task success** (executed action, final database state, call containment).

### Program anchors (the owner's existing stack)

| Work | Eval tasks / benchmarks | Metric family | Level |
|---|---|---|---|
| **Huber & Waibel 2026**, arXiv:2608.05759 [ABS] | read + non-read speech ASR; 2 Whisper context-biasing methods vs 3 speech LLMs | biased WER / unbiased WER / overall WER | **T** |
| **RECOVER**, arXiv:2603.16411 [FT] | Earnings-21, ATCO2-1h, Eka-Medical, Common Voice, ContextASR-Bench | WER, E-WER, RWERR, entity P/R/F1 | **T** |
| **Entity-Aware Select** (a RECOVER fusion strategy, not a separate paper) [FT] | same five datasets | same as RECOVER | **T** |
| **BR-ASR**, arXiv:2505.19179 (Interspeech 2025) [ABS] | LibriSpeech test-clean / test-other biasing, 2k -> 200k bias entries | B-WER (2.8% / 7.1%), WER, latency/pruning rate | **T** |
| **SICL family** — SICL-AED arXiv:2409.19757 [ABS]; COSMIC arXiv:2311.02248 [ABS] | long-form ASR, test-time speaker adaptation, test-time contextual biasing; COSMIC adds speech QA + instruction following | WER; SQA answer metrics | **T** (+A) |
| **Voice Memory**, arXiv:2607.26410 [FT] | HyPoradise v0 (10 domains), Robust HyPoradise (CHiME-4, NOIZEUS), X->En speech translation | weighted WER, **HER**, **ρ (recoverable info ratio)**, BLEU | **T** |
| **HALAS**, arXiv:2606.23048 [ABS] | earnings-call recordings, 7 ASR systems | human-annotated hallucination spans (detection) | **T** |
| **AAD (Audio-Aware Decoding)**, arXiv:2506.07233 [ABS] | **object-hallucination datasets + Clotho-AQA** | F1 (+0.046 to +0.428), audio-QA accuracy (+5.4 to +10.3%) | **A** |
| **T2-RAGBench**, arXiv:2506.12071, EACL 2026 [ABS] | 23,088 question-context-answer triples over financial text+table filings; **text only, no speech** | retrieval + answer accuracy | **A** |

### Works added by this survey (condensed)

| Work | Eval tasks / benchmarks | Metric family | Level |
|---|---|---|---|
| ConEC (LREC-COLING 2024) [FT] | Earnings-21 contextual ASR | WER, common/rare WER, per-type entity WER | T |
| ContextASR-Bench, arXiv:2507.05727 [FT] | own benchmark, 3-rung context ladder | WER, **NE-WER**, **NE-FNR** | T |
| ProfASR-Bench, arXiv:2512.23686 [FT] | own 4-domain corpus, 5-rung context ladder | WER, SER, entity-aware, CUG | T |
| Spoken-SQuAD [FT] / ODSQA [FT] / HeySQuAD [FT] / SD-QA [FT] / NMSQA | extractive spoken QA | EM / F1 | A |
| SLUE + SLUE phase-2 [FT] | NER, NEL, DAC, spoken QA, SUMM | NER F1, frame-F1, word-F1 | A |
| Sun et al. slot filling, arXiv:2311.07418 [FT] | SLURP | SLU-F1 (P/R) | A |
| MedSpeak, arXiv:2602.00981 [FT] | MMLU-Med / MedQA / MedMCQA read aloud | MC accuracy + WER | A+T |
| Korean SQA cascade, arXiv:2605.17443 [FT] | KorQuAD spoken | EM / F1, CER | A+T |
| ClozeGER [ABS] / PMF-CEC [ABS] / DeRAGEC [ABS] / DANCER [ABS] | GER + entity correction | WER, entity WER | T |
| RAS, arXiv:2604.24278 [ABS] | abstention-aware ASR | reliability metric w/ abstention | T |
| MCR-BENCH, arXiv:2508.15407 [ABS] | audio-text conflict tasks | accuracy under conflict, confidence | A |
| VAPO, arXiv:2510.08618 [ABS] | SlideASR-Bench | WER + entity errors | T |
| Le et al. 2021, arXiv:2104.02194 [ABS] | LibriSpeech biasing w/ distractors | WER / B-WER | T |
| SpeechRAG [ABS] / SpeechDPR [ABS] | open-domain spoken QA + retrieval | answer F1, retrieval recall | A |

### Agentic-era works (where the level column finally changes)

| Work | Eval tasks / benchmarks | Metric family | Level |
|---|---|---|---|
| **Audio2Tool**, arXiv:2604.22821 [FT] | own 30k spoken queries, 8 tiers, 3 domains | Tool Accuracy, **EM**, **Slot F1** — *structural comparison to a reference call, not executed* | **A** |
| **From Text to Voice**, arXiv:2605.15104 [FT] | Confetti + When2Call, TTS-converted | **AST-based soft accuracy**, F1 — structural | **A** |
| **BFCL v4** (Patil et al.) [ABS] | Berkeley Function Calling Leaderboard; **text-only** | **AST accuracy** (structural), **executable accuracy** (runs the call), state-transition eval for Agentic/Multi-Turn | A + E (sandbox state, not a transaction) |
| **τ-bench / τ²-bench** (arXiv:2406.12045, Yao et al.) [ABS] | retail (115 tasks) / airline (50) / telecom / banking; **text**, plus a **full-duplex audio-native voice mode in τ²-bench** | **r = r_action x r_output ∈ {0,1}** — final DB identical to gold outcome DB AND required info communicated; reliability as **pass^k** (all k trials succeed) | **E** |
| **VoiceBench**, arXiv:2410.17196 [FT] | 8 sub-tasks incl. SD-QA, MC knowledge, instruction following, safety | GPT-judge 1-5, accuracy, loose/strict IF accuracy | **A** |
| **AIR-Bench (audio)**, arXiv:2402.07729 [ABS] | foundation + **chat** benchmarks over speech/sound/music | GPT-judge generative comprehension score | **A** |
| **AudioBench**, arXiv:2406.16020 [ABS] | 8 tasks, 26 datasets | model-as-judge scores | **A** |
| **VoxEval**, arXiv:2501.04962 [ABS] | spoken MC knowledge QA | MC accuracy | **A** |
| **URO-Bench**, arXiv:2502.17810 [ABS] | end-to-end spoken dialogue, cognitive + paralinguistic | multi-dimension judge scores | **A** |
| **τ-Voice**, arXiv:2603.13686 [FT] | **τ²-bench Retail / Airline / Telecom, 278 tasks, full-duplex audio** | **pass@1 = final database state vs gold** + voice-interaction quality | **E** |
| **VAmoS Bench**, arXiv:2607.27453 [FT] | 100 bank card-operations scenarios, live audio phone calls, seeded PostgreSQL | **containment** + per-scenario binary assertions graded on the full trace | **E** |
| **DuplexWorld**, arXiv:2608.10716 [FT] | 6 worlds, 156 scenarios, 3,825 scored conversations, 350+ h | 12 metrics / 3 pillars incl. **Pass_k vs authored gold end-state** | **E** |
| **EVA-Bench**, arXiv:2605.13841 [ABS] | 213 scenarios, 3 enterprise domains, bot-to-bot audio, 12 systems across 3 architectures | **EVA-A** (task completion + faithfulness + **speech fidelity**) and **EVA-X** (experience), reported as **pass@1 / pass@k / pass^k**; plus an accent+noise perturbation suite | **E** |
| **IHBench**, arXiv:2606.19595 [ABS] | post-interruption recovery in structured workflows | workflow progress / recovery | E (partial) |
| **ProVoice-Bench**, arXiv:2604.15037 [ABS] | 4 proactive-agent tasks, 1,182 synthesized samples | over-triggering / reasoning gap | A |
| **AURA**, arXiv:2506.23049 [ABS] | speech-to-speech multi-turn agent w/ tool use | task completion (reported) | E (system paper) |
| **Stream RAG**, arXiv:2510.02044 [ABS] | speech-in/speech-out w/ streaming tool use | factuality + latency | A |

### Verdict on the owner's suspicion

**Confirmed for the program's own anchor stack — with one nuance, and refuted as a claim about the field.**

1. **Confirmed:** every one of the nine program anchors scores at level **T** or **A**. Not one grades an
   executed action, a database state, or a completed task. Huber & Waibel, RECOVER, BR-ASR, SICL, Voice
   Memory, HALAS all stop at WER/B-WER/E-WER/HER; AAD and T2-RAGBench stop at answer F1/accuracy. There is
   **zero end-to-end task-success evaluation anywhere in the current reference stack.**
2. **Two anchors have an additional scope problem, worth flagging separately:**
   - **AAD (2506.07233)** is evaluated on **object-hallucination datasets and Clotho-AQA**, i.e.
     general/environmental audio — **outside this study's stated boundary.** Its *method* (inference-time
     contrastive decoding, no training) is in-scope and attractive, but it also requires **token-level logit
     access**, which an API-only frozen core may not expose. Both facts should be recorded before it is
     leaned on.
   - **T2-RAGBench (2506.12071)** contains **no speech at all**; it is a text-and-table financial RAG
     benchmark. It is a useful analogy for evidence retrieval over filings, not a speech citation.
3. **Refuted as a field-level claim:** the 2026 literature *does* have genuine end-to-end task-success
   evaluation for voice — **τ-Voice, VAmoS Bench, and DuplexWorld all grade final database state or call
   containment.** The stack is not behind the field on *metrics*; it is simply **disconnected from that half
   of the field.**
4. **The actual whitespace, stated precisely:** no contextual-biasing / knowledge-injection paper is
   evaluated on any level-**E** benchmark, and no level-**E** benchmark tests knowledge injection as an
   intervention. The two literatures cite each other zero times in the works read here. **"Does entity
   knowledge injection raise end-to-end task success?" is, on this evidence, an unasked question.**

## E2. Agentic speech task-system enumeration

### Audio2Tool: origin confirmed

The local dataset matches **arXiv:2604.22821, Pahwa, Beedu, Priye et al. (2026), "Audio2Tool: Speak, Call,
Act — A Dataset for Benchmarking Speech Tool Use"** [FT].
**Canonical public release: HF `RVtech/Audio2Tool`** (RVtech = Rivian & Volkswagen Technologies), public, not
gated, created 2026-04-28, `license: cc-by-nc-4.0` — matching the local copy's licence. The author-named ids
(`ramitpahwa/…`, `apoorvabeedu/…`) do not exist; HF search returns exactly one repo.
Structure: 8 configs (`tier1_direct` … `tier8_intent_blending`), each **single `test` split**; domains
**smart_car / smart_home / wearables**; 16 kHz mono WAV.
**Release totals: 16,843 queries, 36,421 audio files, 59.6 hours** (~2.16 speaker renditions per query).
**Discrepancy to record:** the paper says "approximately 30,000 queries" while the HF README totals 16,843;
everything sits under a `public/` prefix, which hints at a subset, but the card does not say so.
Audio is **zero-shot voice-cloning TTS (Qwen3TTS + CosyVoice-3)** over reference speech from VoxPopuli /
3D-Speaker / YODAS, with automotive and indoor noise mixed in; queries were generated by Claude Opus and
filtered by an LLM-as-judge (GPT-5.1 + Gemini-2.5-pro). It already reports **Qwen-3-Omni-30B** — our core.
**The knowledge asset:** repo-level **`tools_registry.csv` with 152 tools**, columns
`tool_id, domain, category, tool_name, signature, description, argument_defaults, argument_constraints`, plus a
per-example `functions` field carrying the inline spec, and per-example `expected_tool_call` /
`extracted_params`. **Typed signatures plus argument constraints are exactly a roster in schema form** — this
is the naturally-available inference-time knowledge source, already shipped.
**Closest published relatives:** "From Text to Voice" (arXiv:2605.15104, same task shape via TTS conversion of
*verified* text benchmarks), BFCL v4's audio tier, and — at the executed end — τ-Voice / VAmoS / DuplexWorld.

### The landscape, grouped by what they actually measure

**Group 1 — surface-accuracy voice-assistant benchmarks (level A).** VoiceBench (2410.17196), AIR-Bench audio
(2402.07729), AudioBench (2406.16020), VoxEval (2501.04962), URO-Bench (2502.17810), Big Bench Audio.
Task shape: spoken instruction -> spoken/text response, scored by GPT-judge or multiple-choice accuracy.
**No tool execution, no environment state.** Entity-dependence is incidental. A frozen omni core is a valid
entrant everywhere. **Boundary caution:** AIR-Bench and AudioBench both include **sound and music** subsets —
only their speech subsets are in scope for us.

**Group 2 — structural spoken tool-calling (level A, tool-shaped).** Audio2Tool (2604.22821), From Text to
Voice (2605.15104), BFCL v4 audio tier. Task shape: spoken query -> predicted function call; scored by
comparing the *predicted call structure* against a reference (Tool Acc / EM / Slot F1 / AST soft accuracy).
**Entity-dependence is direct and mechanical: a wrong slot value is a wrong call.** Frozen omni + prompt-side
knowledge injection is a clean, valid entrant — no training, no duplex requirement, no environment.

**Group 3 — executed task success (level E).** τ-Voice (2603.13686), VAmoS Bench (2607.27453), DuplexWorld
(2608.10716), IHBench (2606.19595), ProVoice-Bench (2604.15037), FOCAL (2601.07367).
Task shape: multi-turn live audio conversation against a stateful backend; scored by final database state,
binary trace assertions, or containment. **Entry barrier: most assume a real-time full-duplex audio agent.**
Our core is turn-based over a llama.cpp server, so entry requires either the framework's cascaded
ASR->LLM->TTS path (τ-Voice explicitly supports this) or an offline turn-based harness.

### Where entity fidelity maps directly to action success

Ranked by directness of the mapping:

1. **τ-Voice Retail** — the paper *designates Retail primary* **"due to its heavy reliance on slot
   filling—collecting names, emails, order IDs, and addresses—where end-to-end speech systems are known to
   struggle."** Its current mitigation is a prompt instruction to **"ask customers to spell letter-by-letter"**
   — i.e. the field's incumbent answer to entity fidelity is *spelling out loud*, not knowledge injection.
2. **VAmoS Bench** — bank card operations gated on caller **authentication**; a misheard verification field
   fails the call and breaks containment.
3. **Audio2Tool Tier 2** — parametric slot filling; Slot F1 is literally entity-value fidelity.
4. **DuplexWorld** — tool calls against a database across banking/insurance/travel/healthcare/logistics.
5. **SLURP** (non-agentic but slot-shaped) — entity spans are the label.

### Key quantified result for the agentic layer

**τ-Voice, arXiv:2603.13686 [FT]:** text GPT-5 (reasoning) reaches **85% pass@1**; the best voice agent
reaches **51% under clean conditions and 38% under realistic conditions** — voice agents retain only
**30-45% of text capability**. Acoustic ablation on the slot-filling-heavy Retail domain (averaged over three
providers): Clean **55%** -> +Noise **51%** (-6.4% rel) -> **+Accents 44% (-10 pp, -18.7% rel)** ->
+Turn-taking 47% -> Realistic **38% (-17 pp, -31.0% rel)**.
**Accent alone — a pure recognition-fidelity axis, and the defining property of Earnings-21/22 — costs 10
points of end-to-end task success.**
Honest caveat that must travel with this number: the authors attribute **79-90% of failures to agent
behaviour** rather than transcription, and all speech is **ElevenLabs TTS with simulated telephony
degradation**, not real human speech.

## E3. Ranked agentic-era benchmarks we could enter with the frozen-core knowledge plane

| Rank | Benchmark | Why it fits / what blocks it |
|---|---|---|
| **1** | **Audio2Tool** (held locally) | Zero entry cost, already benchmarks Qwen-3-Omni-30B, Slot F1 is entity fidelity by construction, includes an oracle-text condition to isolate ASR error. Turn-based, no duplex requirement. **Blockers:** TTS audio; **needs boundary amendment** (speech-to-action). |
| **2** | **From Text to Voice** (Confetti + When2Call, converted; arXiv:2605.15104) | Converted datasets + eval scripts publicly released; gold tool schemas inherited from *verified text* benchmarks, so labels are trustworthy; **reports Qwen3-Omni at 60.4% AST soft accuracy** as a ready comparison point. Recipe is reusable on our own data. **Blockers:** TTS; boundary amendment. |
| **3** | **EVA-Bench** (arXiv:2605.13841) | **The most enterable level-E benchmark found.** Framework, evaluation suite *and* benchmark data released **open-source**; metrics explicitly **"apply to all major agent architectures, enabling direct cross-architecture comparison"**, so a turn-based cascaded entrant is anticipated by design. Its **EVA-A** composite already fuses task completion with **audio-level speech fidelity** — the exact linkage our thesis argues for — and it ships an **accent + noise perturbation suite** (mean Δ up to 0.314) that is a ready-made fidelity axis. Reliability is reported as pass@k vs **pass^k** (median gap 0.44), so a knowledge plane that improves *consistency* would show up. **Blockers:** synthetic bot-to-bot audio; boundary amendment. |
| **4** | **τ-Voice Retail** (arXiv:2603.13686) | The sharpest entity->action mapping in existence, true level-E metric, code released, and an explicit cascaded ASR->LLM->TTS path we could enter through. **Blockers:** built for real-time full-duplex; heavy harness; TTS; boundary amendment. |
| **5** | **τ²-bench voice mode** (`sierra-research/tau2-bench`, MIT) | τ²-bench ships **"Voice Full-Duplex (Audio Native)"** (`uv sync --extra voice`, `src/tau2/voice/`) with the canonical reward **r = r_action x r_output** and **pass^k**. MIT-licensed, self-hostable, domains retail/airline/telecom/banking. This is the substrate τ-Voice was built on, available directly. **Blockers:** realtime-provider transport assumes duplex audio endpoints; boundary amendment. |
| **6** | **BFCL v4** (`gorilla-llm/Berkeley-Function-Calling-Leaderboard`, Apache-2.0) | Canonical function-calling leaderboard with **AST**, **executable**, and state-transition evaluation. **Unresolved discrepancy:** arXiv:2605.15104 refers to "BFCL-v4's audio tier", but the V4 leaderboard composition retrieved this session (Agentic 665 / Multi-Turn 800 / Live 1,351 / Non-Live 1,150 / Hallucination 1,122, + 5,200 non-scoring Format-Sensitivity entries) shows **no audio category** and the HF repo is text-only. **Do not plan around a BFCL audio tier until it is confirmed to exist.** |
| **7** | **VoiceBench** (`hlt-lab/voicebench`, Apache-2.0, ~28.7 GB) | Cheapest credible entry, widely cited. Better than assumed on provenance: **commoneval, wildvoice, sd-qa and bbh are human recordings** (sd-qa across 11 accents), only the rest is Google TTS. **Blockers:** level-A only (GPT-4o-mini judge + MCQ accuracy) — a credibility baseline, not a task-success demonstration. |
| — | **VAmoS / DuplexWorld** | Best-designed level-E metrics (containment; Pass_k vs authored end-state) but heaviest infrastructure (live phone-call transport, seeded PostgreSQL) and unclear scenario-data release — VAmoS releases *agent implementations*, not confirmed scenario data. **Watch, do not enter now.** |

### Logistics for the level-A voice-assistant group (fetched this session)

| Benchmark | HF id | License | Size | Speech provenance | Metric |
|---|---|---|---|---|---|
| VoiceBench | `hlt-lab/voicebench` | apache-2.0 | ~28.7 GB, 12 configs | **mixed**: human (commoneval, wildvoice, sd-qa, bbh), Google WaveNet TTS (rest) | GPT-4o-mini judge; MCQ accuracy; IF metrics |
| AIR-Bench (audio) | `qyang1021/AIR-Bench-Dataset` | **cc-by-nc-4.0** (data); Apache-2.0 (code) | ~46 GB; 19 foundation tasks / ~19k MCQs + ~2k chat | real corpora (Common Voice, Fisher, SpokenWOZ, IEMOCAP, SLURP…) | MCQ accuracy; GPT-4 judge |
| AudioBench | **no aggregate repo** — ~40 `AudioLLMs/*_test` repos | "Creative Commons NonCommercial" + per-dataset licences | not stated (spread) | mixed; new sets TTS with ~90% human-filtered out | WER, BLEU, METEOR, **Llama-3-70B/GPT-4o judge 0-5 rescaled to 100** |
| Big Bench Audio | `ArtificialAnalysis/big_bench_audio` | mit | ~612 MB, 1,000 examples | TTS (23 voice configs, OpenAI/Azure/Amazon) | accuracy vs `official_answer` |
| VoxEval | `qqjz/VoxEval` | cc-by-4.0 | **~86.5 GB**, 13,938 SpeechQA pairs x 6 voices | TTS (OpenAI TTS, 6 voices) + linguistic/paralinguistic/quality perturbations | MCQ accuracy via whisper-large-v3 + string match |
| URO-Bench | `Honggao/URO-Bench` | mit | ~22.7 GB, 40 configs, ~7,000 items (mini = 1,000) | mostly TTS (CosyVoice, F5-TTS, GPT-4o-Audio-Preview) | GPT-4o-mini 100-pt judge; UTMOS; WER(text-vs-spoken); latency |

**Boundary flags confirmed with evidence:** AIR-Bench's Chat half includes `music_QA_musiccaps`,
`sound_QA_clotho`, `music_generation_analysis_QA_musiccaps` etc.; AudioBench includes MuChoMusic, WavCaps,
AudioCaps and Clotho-AQA. **Both carry substantial music/environmental-audio subsets that fall outside this
repo's prohibition — only their speech subsets may be consumed.** Both are also non-commercial-only.
Useful side-finding: AudioBench's per-task repos include `AudioLLMs/earnings21_test`,
`AudioLLMs/earnings22_test`, `AudioLLMs/slue_p2_sqa5_test` and `AudioLLMs/spoken_squad_test` — i.e. several
of the Question-B recommendations are already packaged there in evaluation-ready form.

## E4. Which single benchmark most sharply demonstrates "entity knowledge injection flips end-to-end task success"

**Audio2Tool, Tier 2 (parametric) and Tier 3 (multi-intent) — as the demonstration we run now; τ-Voice Retail
as the confirmatory target we grow into.**

Reasoning. The claim has three requirements: (i) the outcome must be an *action*, not a transcript;
(ii) entity fidelity must be the binding constraint on that action; (iii) we must be able to enter with a
frozen, turn-based, API-only omni core plus a prompt-side roster, with no training and no second answering LLM.
Audio2Tool is the only candidate that satisfies all three **today**: it is already on disk, its Slot F1 and
Exact Match are computed over argument values so a single wrong entity flips EM from 1 to 0 with no dilution,
it ships **`tools_registry.csv` — 152 tools with typed `signature`, `argument_defaults` and
`argument_constraints`**, which *is* the naturally-available inference-time knowledge source (the roster
analogue: legal device names, entity values and enumerated parameter ranges are readable straight off the
schema, exactly as the ConEC per-call word-lists were readable off the slides), it already contains an
**oracle-text vs Whisper condition** that isolates ASR-induced loss, and it reports **Qwen-3-Omni-30B** so the
comparison is same-model rather than cross-paper. It is also the **only** speech benchmark in this entire
survey that carries typed tool signatures as a per-example structured field. Its published headroom is exactly
where a knowledge plane should bite: >75% on Tier-1 commands but **under 55% EM/F1 on Tiers 5-7**.
The experiment is a two-by-two we can run without new infrastructure: {roster injected, not injected} x
{clean, noisy}, reporting **EM as the primary outcome and WER as a secondary** — which is the exact inversion
of the reference stack's habit, and the point the paper would make.

For the confirmatory destination, **EVA-Bench (arXiv:2605.13841) is the better target than τ-Voice**, despite
τ-Voice having the sharper entity->action story. EVA-Bench releases framework, suite *and* data open-source;
its metrics are explicitly architecture-agnostic, so a turn-based cascaded entrant is anticipated rather than
retrofitted; its **EVA-A** composite already fuses task completion with **audio-level speech fidelity**, which
is our thesis expressed as someone else's metric; and its **accent + noise perturbation suite** supplies the
degradation axis for free. Its **pass@k vs pass^k** gap (median 0.44) also gives us a second, subtler claim to
test — that a knowledge plane buys *reliability*, not just peak capability. τ-Voice Retail remains the
sharpest demonstration in principle and the right thing to cite, but it demands a full-duplex real-time
harness we do not have; proposing it as this quarter's experiment would be over-reach.

Two caveats to state up front rather than have raised in review: **both are TTS**, so a positive result is a
mechanism demonstration on synthetic speech and must be labelled as such; and **both require the study's
boundary to be amended** to admit speech-to-action, since the current boundary enumerates only
ASR / entities / biasing / spoken-QA / meeting understanding. The honest framing is that our real-speech
earnings-call result establishes the entity-repair effect on human speech, and the agentic benchmark
establishes that the repair *changes actions* — neither alone carries both properties.

### What this survey could not establish

- **No paper quantifies entity-error -> meeting-QA accuracy.** The AMI-family QA sets ship without aligned
  audio, so the question is open but expensive.
- **No paper reports an answer-string containment audit** for injected context in spoken QA. Our leakage
  control will have to be defined rather than cited.
- **No paper supplies a model its own errored hypothesis + a retrieved reference + the source audio together.**
  ClozeGER has audio+N-best, RECOVER has N-best+retrieved entities, Voice Memory has N-best+memory. The
  three-way combination that REFLECTION specifies appears unclaimed.
- Audio2Tool's oracle-text-vs-Whisper delta (which would be a direct leverage number on our own model) exists
  in the paper's Table 3 but the PDF's column extraction was unreliable; the number was deliberately not
  quoted. Worth re-reading from the published version.
- **Whether BFCL v4 has an audio tier is unresolved.** arXiv:2605.15104 cites one; the V4 leaderboard
  composition and the HF repo retrieved this session are text-only. Resolve before citing.
- **Audio2Tool's query count is inconsistent** between the paper ("approximately 30,000") and the HF release
  README (16,843 queries / 36,421 audio files / 59.6 h). The `public/` prefix suggests the release is a
  subset, but no card text says so. Check what the local copy actually contains before quoting a size.
- **VAmoS Bench scenario data release is unconfirmed** — the paper links agent implementations only.
- No level-**E** benchmark was found that uses **real human speech**; τ-Voice, VAmoS, DuplexWorld, EVA-Bench
  and Audio2Tool are all synthesized or bot-simulated. A real-speech agentic task-success benchmark does not
  appear to exist, which is itself a finding worth recording.
