# Meeting understanding — methods scan, 2024–2026

Workbench note. Date: 2026-08-17 (local, UTC-4). Web research only; no downloads, no installs, no
paid APIs. Fetch provenance is in `fetch-log.md` (sections L, C, D). English-only record.

Scope: the current engineering shape of meeting-understanding systems, for a meeting-minutes agent
built as a control plane outside a frozen, API-only speech-capable omni core (zero training, no
logit access, no second answering LLM, no gold labels at runtime).

Reading rule used throughout: an arXiv ID is written down only if an `abs` or `html` page was
actually fetched. Numbers taken from search snippets rather than a fetched table are marked
**unverified**. Two scout claims were checked against primary sources and corrected; the
corrections are kept visible rather than quietly fixed.

---

## 0. Bottom line up front

1. **The field is a cascade, decisively, and it is text-side.** The EMNLP 2025 speech-summarization
   survey states outright that "cascaded approaches remain the most widely adopted paradigm in
   SSum." Stronger still: across AutoMin 2021, 2023 and 2025 — the field's only minuting shared
   task — **no submission has ever consumed audio.** Every edition ran on gold manual transcripts.
2. **Our core loop has close priors, but none of them scoops it.** The nearest is **EGTA**
   (2607.17766, July 2026), which builds a terminology memory and re-injects it under a frozen
   model — but builds it **offline from an external document**, not from the episode's own speech,
   and leans on a **logit bias** we cannot use. The provenance of the term table is the whole of
   the remaining ground.
3. **There is a published, empirical warning aimed squarely at our design.** 2511.18774 shows that
   feeding a frozen model its own first-pass output back as raw context **made WER much worse**
   (29.01% vs a 15.79% no-context baseline). Our abstraction step — extract, normalise, dedupe,
   gate — is what would break that loop, and this is the evidence that it is load-bearing rather
   than cosmetic. The first probe must include the naive-reinjection arm.
4. **Two 2025–2026 works sit uncomfortably close to our framing** and must be addressed explicitly
   rather than discovered by a reviewer: **Audio-Mind** (2605.28480) describes "conditional
   evidence acquisition ... acquiring bounded external evidence", and **AudioToolAgent**
   (2510.02995) is a training-free planner outside frozen audio models. Neither touches meetings.
5. **The evaluation headline should be judge-free.** Speaker-attributed QA accuracy (M3-SLU) plus
   MeetingQA F1, backed by the **cpWER − ORC-WER** decomposition that isolates speaker confusion
   from recognition error. ROUGE is kept only as a labelled legacy row; three peer-reviewed sources
   support refusing it as a headline.
6. **A hard engineering constraint on our own core**: Qwen3-Omni's technical report states it
   accepts "audio recordings **up to 40 minutes per instance** for ASR and spoken-language
   understanding." ICSI meetings run ~1 h and **exceed it**; AMI meetings mostly fit. Chunking is
   forced, not optional, and the chunk boundary is exactly where an episode-local glossary has to
   carry state.

---

## 1. Topic 1 — speech-grounded meeting summarization and minuting pipelines

### 1.1 The cascade line (diarize → attribute → segment → summarize)

| Work | Venue / year | ID | Method shape | Data | Headline | Copy / avoid |
|---|---|---|---|---|---|---|
| Team Hitachi @ AutoMin | AutoMin 2021 (Interspeech satellite) | 2112.02741 | Topic-segment transcript → BART fine-tuned on chat-dialogue summarization → argument mining to restructure; reference-free | ELITR Minuting Corpus | Best **adequacy** of Task A submissions | **Copy** the segment→summarize→restructure spine — still the canonical minuting cascade. **Avoid** BART-scale summarizers. |
| AutoMin 2023 overview | INLG 2023 | `2023.inlg-genchal.19` | 5 teams, 2 domains (project meetings + EU Parliament); GPT-4 used both as a system baseline **and** as the automatic scorer | ELITR + EuroParl | No winner crowned | **Copy** the two-domain split. **Avoid** GPT-4-as-judge with no bias control — the organizers did exactly that. |
| Team Zoom | INLG 2023 | `2023.inlg-genchal.14` | Topic segmentation + LLM data augmentation, transformer summarizer | ELITR | — | Segmentation-first is the recurring win. |
| Team Synapse | INLG 2023 | `2023.inlg-genchal.15` | BART fine-tuned on mixed corpora; segment → summarize → concatenate → format | ELITR | — | The plain map-reduce baseline. |
| **Team Iterate** | INLG 2023 | `2023.inlg-genchal.16` | **Iterative minuting** — a running minute refined chunk by chunk | ELITR | — | **Closest AutoMin analogue to a carried-state loop.** Read in full before designing our state carry. |
| Team NTR | INLG 2023 | `2023.inlg-genchal.18` | Dolly LLM; explicit **negative** result on semantic segmentation | ELITR | Title states segmentation did *not* help | **Avoid** assuming segmentation is free money — one team reports it isn't. |
| Team Darbarer | INLG 2023 | `2023.inlg-genchal.17` | not inspected | — | — | unverified |
| **AutoMin 2025 findings** | SIGdial 2025 | 2509.13814 | Task A minuting (EN/CS); **Task B meeting QA, new** (monolingual + CS→EN cross-lingual) | ELITR Minuting Corpus + EuroParlMin + ELITR-Bench, **gold manual transcripts** | Task A: **one** team only (HallucinationIndexes — RL with an Entity Hallucination Index reward over BART/pegasus/T5); GPT-4 baseline best at 4.78±0.58 adequacy on EuroParlMin. Task B: GPT-4o **7.74** vs GETALP **4.55** vs HallucinationIndexes **2.28**; cross-lingual GPT-4o **7.69** vs GETALP 3.11 | **Copy** the sobering lesson: participation collapsed because a prompted frontier LLM beats bespoke systems. **That is our competitive floor.** **Avoid** GPT-family judges (organizers flag stylistic self-preference). Critically: **AutoMin has never evaluated from audio.** |
| GETALP @ AutoMin 2025 | SIGdial 2025 | 2508.00476 | RAG over transcripts + Abstract Meaning Representation for QA | ELITR | 4.55 vs GPT-4o 7.74 | **Avoid** — RAG+AMR lost badly to a plain long-context prompt. A cautionary result for over-engineering the retrieval layer. |
| **Training-free identity-aware diarization refinement** — Chen, Ho, Topaz, Hirschberg, Kostic | arXiv Sep 2025, v2 Aug 2026 | 2509.15082 | Off-the-shelf SD + ASR + **frozen** LLM, structured prompting; identity inferred from conversational semantics (self-introductions, direct address); no gold at runtime; fixes low-confidence labels and split speakers, assigns role identities | private patient–clinician corpus | **29.7% relative** error reduction over reconciled SD+ASR | **Copy this wholesale** — the closest published precedent for our speaker-decomposition module: zero training, frozen LLM, evidence-gated naming. **Avoid over-claiming**: private clinical data, no meeting corpus, no cpWER. "This, on meetings, with a public metric" is a legitimate contribution. |
| Interactive in-meeting speaker correction — He et al. (WPI) | arXiv Sep 2025, rev 2026-05-27 | 2509.18377 | Streaming ASR + diarization → speaker-attributed transcript → LLM summary surfaces attribution errors → user corrections fold back via transcript update + online speaker enrollment | **AMI headset-mix test set, 16 meetings, ~9 h, 3–4 spk** | **DER −31.99% relative; speaker substitution error −52.68%**; GPT-4o with prompt engineering reached **78.9%** simulated-feedback accuracy on 8 AMI training meetings | **Copy the metric pair** — DER *and* speaker substitution error reported separately is exactly the decomposition our OBS layer needs. **Avoid** the human-in-the-loop: our runtime is unattended. ⚠️ **Correction**: an earlier scout summary claimed this paper shows zero-shot LLMs *fail* at speaker correction. Direct read of the HTML says otherwise — the paper does not evaluate zero-shot, it uses GPT-4o with prompt engineering and reports it as "reasonably accurate". Do not cite the failure claim. |
| CMT-LLM | Interspeech 2025, DOI 10.21437/Interspeech.2025-943 | (ISCA) | Contextual multi-talker ASR: pretrained speech encoder + LLM, two-stage filter over large biasing lists → prompt | LibriMix, **AMI SDM** | 7.9% WER (LibriMix), **32.9% WER (AMI SDM)** with 1000-item bias lists | **Copy** the AMI-SDM number as a realistic far-field ceiling. Note it fine-tunes. |
| Unified speech LLM for diarization + ASR | arXiv Jun 2025 | 2507.02927 | Joint diarization + ASR, no oracle segmentation; sliding context of recent speaker turns **from its own predictions** | MLC-SLM Challenge | **54.87% relative** tcpWER/tcpCER improvement, ranked 8th | Carrying your own prior speaker turns forward is established practice — precedent for our state carry. |
| CHiME-7/8 DASR review — Cornell et al. | arXiv Jul 2025 | 2507.18161 | Review | CHiME-6/DiPCo/Mixer6/NOTSOFAR | "all best systems employ diarization refinement via target-speaker diarization"; speaker counting is the error-compounding bottleneck; **"even systems with over 50% time-constrained minimum permutation WER can perform roughly on par"** | **Copy that quote** to justify reporting more than tcpWER. **Copy** the DER budget into our error model — diarization error propagates into every downstream stage. |
| Summarizing Speech: A Comprehensive Survey — Retkowski, Züfle, Sudmann, Pfau, Watanabe, Niehues, Waibel | **EMNLP 2025** | 2504.08024 | Survey | AMI, ICSI, QMSum, MeetingBank, ELITR, SLUE-TED, NUTSHELL, YTSeg | — | The authority for the verdict in §1.3. |

### 1.2 The end-to-end line (audio straight into an LLM)

| Work | Venue / year | ID | Method shape | Data | Headline | Copy / avoid |
|---|---|---|---|---|---|---|
| Prompting LLMs with Audio for General-Purpose Speech Summarization | Interspeech 2024 | 2406.05968 | Audio encoder → tokens into instruction-tuned LLM; trained for modality invariance | arbitrary-domain speech | Beats a cascade ASR→LLM baseline | The strongest "e2e beats cascade" claim — but at **utterance** scale, not meeting scale. |
| An End-to-End Speech Summarization Using LLM | Interspeech 2024 | ISCA (shang24) | Speech encoder + Q-Former → LLM | — | — | unverified numbers |
| BASS | 2023 | 2307.08217 | Block-wise adaptation, streaming long-input summarization | — | — | Precedent for block-state summarization. |
| Advancing Speech Summarization in MLLMs with RL | arXiv Sep 2025 | 2509.19631 | Multi-stage RL, direct audio→summary, controllable style | not stated in abstract | Outperforms larger MLLMs; narrows the gap to text LLMs | **Avoid** — requires RL training. Out of scope for a frozen core. |
| AudioMarathon | 2025 | 2510.07293 | Long-context audio benchmark, 10 sub-tasks | **90–300 s only** (2,250–7,500 audio tokens) | Clear degradation as audio length grows | **Copy as evidence**: the field's idea of "long" audio is five minutes. |
| **VoiceGiraffe** | arXiv May 2026 | 2605.27976 | **Hour-level** audio-language benchmark, 1500 triplets, single-hop + multi-hop | podcasts, long speeches | "Far from saturation"; **long-range memory persistence named as the bottleneck** — models fail at sustained tracking of sparse events | **Copy as the direct motivating citation for episode-local state.** |
| **AMUSE** — Chowdhury et al. (Apple + UMD) | arXiv Dec 2025 | 2512.16250 | Agentic multi-speaker audio-visual benchmark, six task families incl. spatio-temporal speaker grounding + multimodal dialogue summarization; zero-shot / guided / agentic modes; **CC BY 4.0** | multi-speaker dialogue | Abstract names **GPT-4o and Qwen3-Omni as struggling in multi-speaker, dialogue-centric settings**; RAFT alignment gives up to **39.52% relative** gain | **Copy the negative result** — it is our problem statement, in print, naming our exact model class. |

### 1.3 Verdict: cascade dominates, and the evidence is threefold

1. **The survey says so outright.** 2504.08024 (EMNLP 2025): *"Cascaded approaches remain the most
   widely adopted paradigm in SSum."* End-to-end is "increasingly explored", not established.
2. **The shared task is 100% cascade-side and 100% text-side.** AutoMin 2021, 2023, 2025 — no
   submission consumed audio; every edition ran on gold manual transcripts. End-to-end audio-LLM
   minuting has never been submitted to the field's only minuting benchmark.
3. **End-to-end hits a wall at meeting length.** AudioMarathon's "long context" tops out at 300 s.
   VoiceGiraffe, the only hour-level benchmark found, reports models far from saturation with
   long-range memory persistence as the named bottleneck. AMUSE shows Qwen3-Omni-class models fail
   at multi-speaker tracking before length is even a factor. And our own core caps at 40 minutes
   per instance.

Why cascade wins: mature ASR/diarization components, arbitrary length via chunking, inspectable
intermediate artifacts, and no training. Its known cost, stated by the survey, is that *"cascaded
models further propagate transcription errors into summarization"* — which is precisely the leak our
glossary loop targets.

**Two exploitable gaps.** (i) AutoMin's evaluation has never been speech-grounded, so an audio-in
minuting pipeline evaluated on ELITR-style material is genuinely under-occupied. (ii) The 2025
result that a bare GPT-4 prompt beat every bespoke system means **our baseline must be a strong
long-context prompt**, not a weak pipeline, or the gains will not be believed.

---

## 2. Topic 2 — terminology / glossary handling: the closest priors to our core loop

Ranking axis, applied uniformly: does the system (1) derive the term table **from the material
itself**, (2) at **episode/document scope**, (3) **re-inject as prompt**, (4) with the model
**frozen**, (5) **multi-pass**, (6) with **no gold/external list**?

| Rank | Work | ID | Self-derived? | Scope | Injection | Frozen? | Passes | External list? |
|---|---|---|---|---|---|---|---|---|
| **1** | EGTA — evidence-grounded terminology adaptation | 2607.17766 | Yes, but from an external doc | Document | Prompt **+ logit bias** | Yes (no fine-tuning) | 2-stage | External document |
| **2** | Zero-Shot Context-Aware ASR (Arabic) | 2511.18774 | **Yes — same audio** | Utterance | Decoder prompt only | **Yes, no param updates** | **2-pass** | Retrieval index external |
| **3** | CTC-Assisted LLM-Based Contextual ASR | 2411.06437 | Pass-1 *selects* from a given list | Utterance | Prompt | No (LLM-ASR trained) | **2-pass** | **External list** |
| 4 | BabelDOC | 2605.10845 | **Yes — same document** | Document | **Prompt only** | Yes (prompt steering, no adaptation) | 1 pre-pass | Optional user glossary |
| 5 | MARS | 2508.01166 | **Yes — same conversation** | Conversation | Encoder input | No (trained, 1.5 K h) | 1-pass + retrieval | Self history |
| 6 | BR-ASR | 2505.19179 | No | Utterance | Retrieved → ASR | ASR not fine-tuned | retrieve-then-decode | External, 200 k entries |
| 7 | Hotword retrieval + GRPO (Alibaba) | 2512.21828 | No | Utterance | Prompt | No (GRPO fine-tune) | 2-stage | External vocabulary |
| 8 | SAP² | 2511.11139 | No | Talk | Pooled embeddings | No | 2-stage | Slides |
| 9 | LCB-net | 2401.06390 | No | Talk | Bi-encoder | No | 1-pass | Slides |
| 10 | TCPGen + GNN | 2305.18824 | No | **Meeting series** | Decoder pointer | No | 1-pass | Slide OCR + rare-word list |
| 11 | PromptASR | 2309.07414 | Partly (preceding utterances) | Recording | Text encoder + cross-attn | No | 1-pass | Ground-truth preceding text |
| 12 | Metadata-driven reasoning chains | 2606.10838 | No | Video | CoT prompt | No (fine-tuned, 400 h) | 3-stage CoT | YouTube metadata |
| 13 | WCTC-Biasing | 2506.01263 | No | Utterance | **Inter-layer bias** | Retraining-free | 1-pass | External |
| 14 | LOGIC ⚠️ **WITHDRAWN 2026-02-04** | 2601.15397 | No | Utterance | **Logits** | not stated | 1-pass | External |
| 15 | Recognize New Words comparison | 2608.05759 | No | — | Prompt vs biasing | — | — | External |

### 2.1 Prior #1 — EGTA (closest overall)

*When to Use Extra Context: Evidence-Grounded Terminology Adaptation for Simultaneous Speech
Translation.* **arXiv 2607.17766**, Yang & Nakamura, submitted 2026-07-20 — verified by `abs` and
`html` fetch.

**Mechanism.** Converts document context *D* into a terminology memory `T_D = {t₁…t_m}` using a
**prompt-based Qwen3-30B-Instruct extractor (FP8)**, normalising case, punctuation, whitespace and
hyphens, filtering generic words while retaining acronyms, CamelCase and technical phrases. At
inference a term activates **only when its surface form, acronym, or tokenizer variant appears in
the current segment's ASR hypothesis or recent streaming history**, ranked by exactness, specificity
and recency under a fixed per-segment budget. Explicitly "a lightweight inference-time framework
rather than a full-model fine-tuning method." Data: MCIF-dev (scientific talks) En→Zh / En→De,
generalising to ACL60/60-dev. Numbers: BLEU **+1.05 / +0.59**; named-entity recall **+79% / +73%
relative**; acronym recall **+0.099 / +0.171**.

**How close.** This is the same *machine* as ours — automatic term extraction, surface-variant
normalisation, evidence-gated activation, budgeted re-injection, no fine-tuning. It is one month old.

**What differs, exactly.**
- The memory is built **offline, before inference, from the paper's title/abstract/metadata** — an
  external artifact, not the episode's own earlier speech. Verified directly: "document context *D*
  converted offline into a compact terminology memory", preparation stage precedes streaming. It is
  explicitly **not incremental**.
- It applies vocabulary-level **logit bias** `z'_t(v) = z_t(v) + B·1[v ∈ V(T_i)]`, B≈2.0 — which our
  API-only boundary forbids outright.
- Speech translation, not meeting minuting: no speakers, no coreference.

**Does it scoop us?** No. It scoops the *gating and budgeting* design, not the self-derivation and
not the frozen-API constraint. But it is the paper a reviewer will cite at us.

**Usefully, its ablation separates our channel from theirs.** EGTA-R = speech/prompt-side alone,
EGTA-G = decoder logit bias alone, EGTA-RG = both; recommended B=2, with B=3 giving diminishing
returns and a Global-G B=5 stress test collapsing (BLEU 43.31 → 41.21). So a prompt-only variant is
already named in the literature — **we must show the prompt-only path carries the gain on its own**,
because that is the only path open to us.

**Copy**: evidence-gated activation; surface/acronym/tokenizer-variant normalisation;
recency+specificity ranking under a per-segment budget. **Avoid**: any dependence on logit bias.

### 2.2 Prior #2 — Zero-Shot Context-Aware ASR for Diverse Arabic Varieties (the warning)

**arXiv 2511.18774**, Talafha, Abu Alhassan, Abdul-Mageed; 2025-11-24, rev 2026-01-10 — verified,
HTML read.

**Mechanism.** Two test-time mechanisms: (i) **decoder prompting with first-pass hypotheses** placed
after the `|PREV|` token; (ii) encoder/decoder prefixing with retrieved speech-text exemplars, plus
optional speaker-matched synthetic exemplars. *"Inference without dialect-specific supervised
adaptation or parameter updates."* Retrieval index built from the text side of ~500 K speech-text
pairs, fixed before evaluation, no ground-truth eval transcripts. Results: MSA **−22.29%** relative,
accented MSA −20.54%, dialectal −9.15%. On CV15+MGB2 MSA: Whisper-v3 baseline **15.79%** WER →
reversed prompting **13.57%**.

**How close.** The only work found combining all of: the same audio's own first-pass output as
context, prompt-only injection, and a genuinely frozen model with zero parameter updates.

**What differs.** Utterance-level, not episode-level; re-injects **raw hypothesis text**, never an
abstracted/deduplicated glossary; no speakers; prompt budget bounded to "on the order of a few
hundred tokens."

**The finding we must not ignore.** Their ablation isolates the two sources. Prompting with the
**own first-pass transcript alone scored 29.01% average WER on MSA — far worse than the 15.79%
no-context baseline.** The retrieval-prefixed variant scored 14.60%. The headline 13.57% required
*reordering* the prompt specifically to disrupt hallucination. (Exact label semantics carry some
uncertainty — their first-pass hypotheses appear to come partly from SeamlessM4T rather than Whisper
itself — so treat the magnitude as indicative; the direction is unambiguous.)

**Translated to our design: naively feeding a frozen model its own earlier output back as context
amplifies its own errors and induces copy/hallucination loops.** Our glossary abstraction step —
extract, normalise, dedupe, threshold, gate on evidence — is exactly what would break that loop.
**Design the first probe with a naive-reinjection arm so the gap is measured, not asserted.**

### 2.3 Prior #3 — CTC-Assisted LLM-Based Contextual ASR

**arXiv 2411.06437**, Yang, Ma, Gao, Zhang, Chen; 2024-11-10, **SLT 2024** — verified.

**Mechanism.** Run a coarse CTC decode first, use those results to **filter relevant hotwords out of
a large list**, then inject the survivors into the LLM prompt. LibriSpeech: test-clean **1.27% WER /
3.67% B-WER**; test-other **2.72% / 8.02%**; still works at **2000 biasing words**.

**How close.** The canonical "pass-1 output determines what pass-2 sees" architecture, and its
injection channel is a **text prompt**, not logits — structurally the same plumbing as ours.

**What differs.** The hotword list is **given externally** (LibriSpeech rare-word lists plus
distractors). Pass-1 only *selects from* a supplied list; it never *creates* one. And the LLM-ASR is
trained, not frozen.

**Does it scoop us?** No — and the list-provenance difference is the whole of our contribution: they
filter a gold list, we manufacture the list from the episode with no external source.

### 2.4 Honourable mention — BabelDOC (structurally near-identical, wrong domain)

**arXiv 2605.10845**, ACL 2026 system demonstration — verified via HTML. The system "scans the
[intermediate representation] to extract domain-specific terminology and build a dynamic glossary",
which "is then injected into the LLM prompt to improve terminological consistency." Prompt injection,
**not** constrained decoding; model steered without adaptation. Ablation: removing glossary/context
control drops terminology consistency **5.00 → 3.00**; human TC 4.47 vs 3.34 for the baseline.

This is our loop, in document translation: self-built from the material, prompt-injected, frozen
model. It differs in being **one-shot pre-pass rather than incremental**, text rather than speech,
and evaluated by a 1–5 human terminology-consistency rating rather than WER or entity recall. Worth
citing precisely because it shows the mechanism is domain-general and already published outside
speech — which sharpens rather than weakens the case for testing it where the input is *noisy ASR
output about itself*.

### 2.5 Cross-cutting cautions

- **2608.05759** (Huber & Waibel, 2026-08-06) is the single most consequential paper for our risk
  model. Comparing two Whisper-based context-biasing methods against three speech LLMs: biasing
  **cuts biased WER by up to 88% relative** while leaving other words alone; speech LLMs "excel on
  read speech but generalize less well to **non-read speech**" and are **sensitive to distractor
  count and prompt word order**. Meetings are non-read speech and prompt-based biasing is our only
  lever. Budget accordingly: **glossary precision matters more than recall** (every false term is a
  distractor), and **ordering within the injected block is a real experimental variable.**
- **LOGIC (2601.15397) was WITHDRAWN on 2026-02-04.** Do not cite it as a result. Its failure
  taxonomy for prompt-based biasing — context-window limits, latency growth, **lost-in-the-middle as
  lists grow**, and generative error correction that **over-corrects and hallucinates entities** —
  is still worth internalising as hypothesis. Its metric pair (**Entity WER + False Alarm Rate**) is
  reusable even though the paper is not citable.
- **Whisper's `initial_prompt` caps at 224 tokens** and later tokens receive disproportionate
  attention. Qwen3-Omni is not so capped, but the attention-position effect is the same phenomenon
  the Arabic paper fought with prompt reordering. **Plan a glossary-size sweep.**
- **Meeting-scoped lists already exist, but externally sourced.** TCPGen+GNN (2305.18824) builds
  per-**meeting-series** biasing lists of 175–576 words from slide OCR and applies them to every
  utterance in that series (>60% WER reduction on rare/unseen words). That is the shape of our
  object, sourced from slides instead of the meeting's own earlier speech — **our natural
  upper-bound oracle comparison.**
- **A hard recall ceiling on self-derivation.** Classical ICSI-era keyword extraction found that
  only **59.74%** of human-annotated keywords survive into ASR output at all. Whatever we mine from
  pass-1, roughly 40% of the gold key terms are simply not there to be mined. This bounds the
  achievable gain and should be stated up front rather than discovered in ablation.

### 2.6 The search negatives (these are evidence)

Four deliberately targeted queries returned **zero research hits**, only marketing glossaries and
blog posts:

- "glossary automatically built from meeting transcript injected into LLM prompt" (C40)
- "two-pass lecture transcription glossary from first pass output" (C53)
- "'episode-local' OR 'meeting-specific glossary' self-built re-injected frozen" (C59)
- "meeting minutes agent frozen omni no fine-tuning glossary control plane 2026" (C67)

Combined with the fact that AutoMin has never run on audio, the specific combination — **self-built,
episode-local, meeting-scoped, prompt-only, frozen API-only core** — appears unoccupied.

**Bottom line on the scoop question: nothing found scoops us.** The three nearest priors each fail a
different defining constraint — EGTA is self-built but from an external document and needs logits;
the Arabic work is self-derived, frozen and prompt-only but utterance-scoped with raw text and a
documented failure when used alone; CTC-assisted is two-pass and prompt-injected but filters a gold
list and trains. The convergence is close and recent (EGTA is one month old), so **speed matters**,
and the novelty claim must be stated on the **provenance of the term table** and the **API-only
frozen boundary** — never on "we do contextual biasing for meetings."

---

## 3. Topic 3 — LLM / omni meeting agents (2024–2026)

### 3.1 Which frozen audio/omni LLMs actually publish meeting-corpus numbers

**Blunt finding: almost none, and none publishes a speaker-attributed one.**

| Model | Meeting number in its own report | Metric | Audio length limit |
|---|---|---|---|
| **Phi-4-multimodal** (2503.01743, Table 4) | **AMI 11.69**, **Earnings22 10.16** | plain WER, no attribution | "theoretically … maximum 2.8 hours" |
| **Qwen3-Omni** (2509.17765, Table 6) | WenetSpeech `test_meeting` only | CER, Chinese, single stream | **"up to 40 minutes per instance for ASR and spoken-language understanding"** |
| **Qwen2.5-Omni** (2503.20215, Table 2) | WenetSpeech `test_meeting` **7.7** | CER | not stated |
| **Step-Audio 2** (2507.16632) | WenetSpeech meeting **4.73** | CER | not stated |
| **Kimi-Audio** (2504.18425) | WenetSpeech test-meeting **6.28** *(unverified — snippet)* | CER | not stated |
| **Qwen2-Audio** (2407.10759) | none | — | **30-second cut-off** (per the Phi-4 report) |
| **Qwen3.5-Omni** (2604.15804) | **no AMI/AliMeeting table** — verified directly; ASR section is Fleurs/CV/LibriSpeech/WenetSpeech | — | 256k tokens / **10 h audio**, chunked prefilling |
| SALMONN / Gemini-audio / GPT-4o-audio | no first-party meeting numbers found | — | — |

⚠️ **Attribution correction.** A search snippet claimed Qwen3.5-Omni reports AMI-SDM cpWER 33.46 and
AliMeeting cpWER 14.71. Direct fetch of the technical report HTML shows **no such table exists**
there. The snippet conflated it with a third-party paper. Discarded; do not propagate.

**Third-party numbers on the same frozen models — the useful positioning source:**

- **Phi-4 Table 4 cross-model column** is the best published head-to-head on a real English meeting
  corpus. AMI: Phi-4-MM 11.69, Canary-1B 13.90, Qwen2-audio 15.24, Whisper-v3 15.95,
  Gemini-2.0-Flash 21.58, SeamlessM4T-v2 56.1, **GPT-4o 57.76**. Earnings22: Phi-4-MM 10.16,
  Whisper-v3 11.29, Canary 12.19, Gemini-2.0-Flash 13.13, Qwen2-audio 14.09, GPT-4o 20.94.
  *(Version caveat: another version reported 11.45 / 10.50 for Phi-4-multimodal-instruct. Cite the
  version fetched.)*
- **Dixtral — Grounding Spoken LLMs in Multi-Speaker Audio via Diarization Conditioning** (Polok,
  Cornell, Udupa, Černocký, Watanabe, Burget; **Interspeech 2026**, 2606.18134) reports **cpWER** on
  **AMI + NOTSOFAR-1 + LibriSpeechMix + Mixer6** against **Gemini 3.0 Flash, VibeVoice, Voxtral Mini
  Transcribe V2** — +29.0 / +19.8 / +16.0 absolute cpWER — and ships a **new long-form multi-speaker
  QA benchmark**. This is the only paper found putting current frozen commercial audio models on a
  speaker-attributed meeting metric. **It is the direct competitor result.**
- **Open ASR Leaderboard** (2510.06961, v4 Mar 2026): long-form English track = **CORAAL,
  Earnings21, Earnings22, TED-LIUM v3** (AMI sits in the *short-form* track). Aggregate long-form
  WER: Cohere Transcribe 9.73 → Distil-Whisper v3.5 11.7. Per-dataset breakdowns live on the HF
  Space, not in the paper. This is the accepted reference frame for Earnings21/22, which our program
  already pins.

**Consequences for us.** The reviewer-acceptable comparison surface is **AMI** (Phi-4 table +
Dixtral cpWER) and **Earnings21/22** (Open ASR Leaderboard) — *not* WenetSpeech `test_meeting`,
which is Chinese, single-stream and speaker-blind, and tells a reviewer nothing about speaker
decomposition. And **ICSI meetings run ~1 h, exceeding Qwen3-Omni's stated 40-minute window**, while
AMI mostly fits. That is a protocol-forcing fact.

### 3.2 Agentic pipelines over meeting audio/transcripts

| Work | Venue / year | ID | Shape | Verdict |
|---|---|---|---|---|
| **Overhearing LLM Agents: A Survey, Taxonomy, and Roadmap** — Zhu, Callison-Burch | arXiv Sep 2025 | 2509.16325 | First framing of agents that "continuously monitor ambient activity and intervene only when they can provide contextual assistance" | **Copy this framing.** The cleanest published name for what our meeting agent is — gives us a paradigm label without a competing method. |
| **Summaries, Highlights, and Action Items** — LLM-powered meeting recap | CHI 2025 / PACMHCI `10.1145/3711074` | 2307.15793 | Deployed recap system; studies user add/edit/delete behaviour | **Copy the output taxonomy** (summary / highlight / action item) — a peer-reviewed decomposition of "minutes". **Avoid** its evaluation: HCI qualitative, no reusable automatic metric. |
| **AudioToolAgent** — Wijngaard et al. | arXiv Oct 2025, rev Feb 2026 | 2510.02995 | **Training-free** central LLM agent + tool adapters; **the agent never accesses audio**; arbitrates conflicting tool outputs | **Closest architectural sibling.** Same "control plane outside frozen models, planner has no audio access" shape. MMAU 77.50 / MMAR 77.00 / MMAU-Pro 61.90. **Avoid assuming transfer**: zero meeting or long-form content. Cite as architectural prior art, never as evidence it works on meetings. |
| **Audio-Mind: An Auditable Agentic Framework for Audio Understanding** | arXiv May 2026 | 2605.28480 | Planner-guided tool decomposition with **auditable reasoning traces exposing uncertainty and tool evidence**; describes "**conditional evidence acquisition — preserving frontend judgment when initial evidence is sufficient while acquiring bounded external evidence**" | ⚠️ **Read in full before writing anything.** That quoted sentence is our SUPPLY/USE thesis in someone else's words, published May 2026. **Nearest-neighbour risk to the novelty claim.** MMAR 80.4, MSU-Bench 82.8. Not meeting-scoped — that is our remaining room. |
| **Interspeech 2026 Audio Reasoning Challenge** — Ma et al. | arXiv Feb 2026 | 2602.14224 | Single-Model vs **Agent** tracks; introduces **MMAR-Rubrics**, instance-level scoring of reasoning-chain factuality and logic; agent systems lead; 156 teams | **Copy the track distinction** for positioning: external evidence that a tool-orchestrating control plane over frozen audio models is a recognized category that *wins*. |
| **MIMIC / FAME** — Kirstein et al. | ACL 2025 Findings | 2502.13001 | Multi-agent synthesis of meeting transcripts (profiles → outline → LLM debate); 500 EN + 300 DE | **Avoid as data for any claim** — synthetic transcripts, no audio. Relevant only as privacy-safe transcript-side dev data. |
| **Meeting Delegate** — Hu, Yuan et al. (Northeastern + Microsoft) | ACL 2025 HCI+NLP, `2025.hcinlp-1.24` | 2502.04376 | LLM attends meetings on the user's behalf; benchmark from real transcripts; active vs cautious engagement strategies | ~60% of responses address at least one ground-truth key point; authors flag irrelevance, repetition, and poor tolerance of transcription errors. **Copy** the transcription-error-tolerance framing — it is the same leak our glossary targets. |
| **MeetBench-XL** — Hu et al. | arXiv Feb 2026 | 2602.03285 | MeetAll corpus + 5-dimension protocol + **MeetMaster XL dual-policy agent** (fast/slow query routing + tool invocation: retrieval, cross-meeting aggregation, web search) | MeetMaster 6.59/10 vs 3.30–6.56 for Llama/Qwen/DeepSeek/Phi/ChatGLM. **Copy the fast/slow routing idea** — it is a control-plane decision, implementable against a frozen core. Dataset detail in `datasets.md`. |
| **AR Secretary Agent** | arXiv May 2025 | 2505.11888 | Real-time memory augmentation via LLM-powered AR glasses | Peripheral; noted for completeness. |

### 3.3 Speaker-aware / diarization-aware prompting of audio LLMs

| Work | Venue / year | ID | Training-free? | Verdict |
|---|---|---|---|---|
| **Modular Training-free Identity-Aware LLM Refinement of Speaker Diarization** — Chen, Ho, Topaz, Hirschberg, Kostic | arXiv Sep 2025, v2 Aug 2026 | 2509.15082 | **YES — fully training-free** | **The single closest published method to our ORG/OBS layer.** 29.7% relative error reduction. Uses semantic continuity to fix low-confidence labels, corrects split speakers, assigns role identities. **Avoid over-claiming**: private clinical data only, no meeting corpus, no cpWER. |
| **Dixtral** — Polok et al. | **Interspeech 2026** | 2606.18134 | **NO** — conditions the acoustic encoder on diarization masks, decoder frozen | **The direct competitor result.** It modifies the encoder; we cannot (API-only). That is our defensible difference — and also why our numbers will be worse. Plan for that explicitly. |
| Diarization-Aware Multi-Speaker ASR via LLMs — Lin, Cheng, Li et al. | ASRU 2025 submission | 2506.05796 | trained | Structured diarization input + frame-level speaker/semantic embeddings → segment transcripts, preserving absolute timing. **Copy the input format idea** (structured diarization as text) — doable through an API boundary. |
| **DM-ASR** — Li et al. | arXiv Apr 2026 | 2604.22467 | trained | Reformulates transcription as **multi-turn dialogue generation** with speaker- and time-conditioned queries. **Copy the multi-turn query decomposition** — directly implementable as prompts against a frozen core. |
| Speaker Attributed ASR Using Speech Aware LLMs — Aronowitz, Kons, Dekel, Saon, Hoory (IBM) | arXiv Apr 2026 | 2604.11269 | fine-tuned | Introduces `[Speaker 1 cluster 42]:` **speaker cluster tags**, jointly trained. **Copy the tag surface form** as a prompt convention; avoid the training claim. |
| **SpeakerLM** — Yin et al. | **AAAI 2026** | 2508.06372 | trained, multi-stage | End-to-end joint SD+ASR with a **flexible speaker registration mechanism** — registration is our episode-local speaker glossary. Cite as the trained upper bound. |
| SoulX-Transcriber (2606.02400), TagSpeech (2601.06896), G-STAR (2603.10468), DNCASR (2506.01916), JEDIS-LLM (2511.16046) | 2025–2026 | — | trained | The trained SA-ASR frontier on AliMeeting / AISHELL-4 / AMI. Track for baseline numbers; not method competitors to a zero-training control plane. Numbers for the last three **unverified**. |

### 3.4 Industry reference — NON-ACADEMIC, no evidentiary weight

Recorded only to show the conventional pipeline shape; no claims rest on this.

- **NVIDIA developer blog (adam.ai case study)**: ingest → Riva ASR → LLM summarization → action
  items. Diarization not mentioned; no chunking discussion; **no evaluation methodology of any kind.**
- **Gladia blog**: diarization present; speaker labels mapped to participant names by **timestamp
  overlap**; domain vocabulary supplied via prompt-side "context" to the recognizer; **no chunking
  strategy, no evaluation method** stated.
- An AssemblyAI post returned 404 (log D61).

**Net**: the commercial shape is a three-stage cascade (ASR + diarization → prompt-assembled
transcript → single LLM summarization pass), speaker labels passed as text into the prompt,
glossaries injected at the recognizer, and **neither vendor publishes any evaluation protocol**.
That absence is itself the useful datum: there is no industry standard to defer to, which is exactly
why a reviewer will hold us to the academic protocol in §4.

---

## 4. Topic 4 — evaluation practice, and the protocol we should adopt

### 4.1 What the literature establishes

**The AutoMin lineage, and its own admission of failure.** AutoMin 2021 used ROUGE-1/2/L plus manual
adequacy / fluency / grammaticality. AutoMin 2022 (`2022.inlg-genchal.1`) made *"devise efficient
metrics for evaluating the quality of minutes"* **an explicit shared-task objective** — the
organizers themselves declared the metric problem unsolved. AutoMin 2023 added "more fine-grained
manual evaluation" and used GPT-4 outputs as a benchmark. AutoMin 2025 (2509.13814) used
ROUGE + BERTScore + BARTScore plus a Chain-of-Thought LLM judge scoring Adequacy, Fluency,
Grammaticality and Relevance on 1–5 Likert scales.

**AutoMin 2025's own correlation numbers are damning and were read first-hand**: GPT-2025-CoT
Adequacy and Relevance correlated with manual judgements at only **0.17 and 0.13**; the older
GPT-2023 scheme reached Pearson ≤ 0.3; BART-F1 showed a **negative** correlation (−0.69) between the
2023 and 2025 computations on EuroParlMin; and Adequacy and Relevance turned out nearly synonymous
in GPT evaluations (Pearson 0.97–0.99), i.e. the judge was not actually scoring four dimensions.
**No human evaluation was run in 2025 at all**, for funding reasons. One mitigating datum: on 45
deliberately misaligned EuroParlMin minutes, GPT-based evaluation *did* separate adversarial from
regular minutes — except Grammaticality (p = 0.41). So the judge detects gross corruption but does
not track quality.

*Marked unverified:* the widely repeated AutoMin-2021 correlation figures (≈0.42–0.544 on averaged
scores) came from a snippet; the ISCA PDF would not extract. Do not use them without re-reading
`isca-archive.org/automin_2021/ghosal21_automin.pdf`.

**ROUGE's validity — three peer-reviewed grounds to refuse it as a headline.**
1. **EMNLP 2025 speech survey** (2504.08024), read directly: *"The presence of disfluencies,
   multiple speakers, and the lack of structure in spontaneous speech diminish the correlation
   between ROUGE scores and human judgment"*; and structurally, *"current evaluation methods for
   SSum remain grounded in TSum approaches, which may overlook the distinct challenges of spoken
   content."* It also notes BERTScore's **512-token limit**, frequently exceeded by meeting
   transcripts, and — decisively for us — that **"no models evaluate the SSum content directly from
   raw audio signals."**
2. **CADS** (Kirstein, Wahle, Gipp, Ruas; **JAIR Vol. 82, 2025**; 2406.07494): *"The ROUGE metric is
   the most used"*, and *"human evaluation is frequently reported without sufficient detail on
   inner-annotator agreement and annotation guidelines."*
3. **Dai, Karimi, Fang** (**EMNLP 2024 Findings**, 2409.19507): summarization metrics are
   meta-evaluated almost exclusively on **news**, so their meeting-domain validity is untested by
   construction.

Add **Kirstein et al., EMNLP 2024** (2404.11124): on QMSum, automatic metrics show weak-to-mid
correlations against a meeting-specific error taxonomy (speaker dynamics, contextual turn-taking,
missing information, linguistic inaccuracy), and **about a third of the correlations show error
masking**.

**LLM-judge protocols specific to meeting summaries.**
- **MESA** (Kirstein, Ruas, Gipp; **COLING 2025 Industry Track**, 2411.18444) — three-step
  per-error-type assessment → multi-agent discussion → feedback-based self-training, GPT-4o backbone.
  Mid-to-high point-biserial on error detection, mid Spearman/Kendall, **~+0.25 over prior methods**.
  Adapts to custom error guidelines with little labelled data.
- **CREAM** (Gong, Ai, …, Hirschberg; 2409.10883) — **reference-free**, CoT + key-fact alignment,
  **ELO ranking** over conciseness and completeness. A ranking instrument, not an absolute scorer.
- **What's Wrong? Refining Meeting Summaries with LLM Feedback** (**COLING 2025**, 2407.11919 /
  `2025.coling-main.143`) — releases **QMSum Mistake**: 200 summaries (169 erroneous + 31 controls)
  human-annotated over **nine error types**, spanning **ICSI, AMI and parliament** meetings.
  Annotation reached **Krippendorff's α = 0.793**.
- **P-MESA / Re-FRAME** (2509.15901) — personalized extension, 7 dimensions, ≥89% balanced accuracy
  against human annotations, severity correlation r ≥ 0.70.
- **Adverse evidence.** **TofuEval** (**NAACL 2024**, 2402.13249) is blunt: LLMs including GPT-4 are
  **poor binary factuality evaluators on dialogue and are outperformed by specialized non-LLM
  factuality metrics**, which also track the error-type distribution better. LLM judges correlate
  weakly with human preference and show self-bias on long-context dialogue summaries.
- **Bias controls.** MT-Bench (**NeurIPS 2023 D&B**, 2306.05685) is the canonical source for
  position / verbosity / self-enhancement bias (GPT-4 judge >80% human agreement on short-form).
  G-Eval (2303.16634) reaches Spearman **0.514** on summarization and its own authors flag bias
  toward LLM-generated text.
- **Counter-example to avoid imitating**: 2604.21345 (Apr 2026) runs a judge-only cross-domain
  pipeline over 114 meetings with GPT-family judges, reports **no human agreement at all**, and
  finds accuracy differences **not statistically significant** (p 0.053–0.448). That is what a
  judge-only protocol produces.

**Meeting QA protocols.** **MeetingQA** (ACL 2023, `2023.acl-long.837`) — extractive QA from
questions actually asked by participants; answers **multi-span and distributed across speakers**;
scored by **F1**; models 57.3 vs human 84.6. **MeetingBank** (ACL 2023) scores content with a
**QA-based metric** rather than text overlap *(QAEval originates with Deutsch et al., TACL 2021 —
one snippet conflated it with MeetingBank; do not mis-cite)*. **M3-SLU** (2510.19358) — accuracy +
LLM-judge over speaker-attributed QA. **ELITR-Bench** (2403.20262, COLING 2025) — 271 QA pairs,
GPT-4-judge scored, with answer-position annotation (beginning/middle/end/several) and WER-perturbed
transcript variants. **QMSum** — still scored primarily by ROUGE-L F1, the practice we are refusing.

**Attribution metrics — exact definitions and sources.**
- **DER** — NIST RT lineage; false alarm + missed speech + speaker confusion over total speech time,
  with a forgiveness collar. Timing-based, **content-blind**.
- **SA-WER** — Kanda et al., **Interspeech 2020, 2006.10930**; WER against each speaker's reference
  conditioned on speaker identification, charging recognition and speaker-ID errors jointly.
- **cpWER** — CHiME-6 lineage; concatenate all utterances per speaker in hypothesis and reference,
  take the speaker permutation minimizing WER.
- **ORC-WER** — MeetEval; **ignores speaker attribution entirely**, giving the WER achievable with
  perfect speaker labels.
- **tcpWER** — MeetEval; cpWER plus a temporal constraint so "only words are identified as correct
  when the temporal alignment is plausible". Standard for CHiME-7/8 DASR and NOTSOFAR-1.
  *(⚠️ the toolkit's `tcpwer.md` returned HTTP 503; the **default collar value is unverified** and
  must be read before being pinned in config.)*
- **MIMO-WER** — MeetEval; multi-input multi-output generalization.
- **Toolkit**: **MeetEval** — von Neumann, Boeddeker, Delcroix, Haeb-Umbach, **CHiME-7 workshop
  2023, arXiv 2307.11394**, `github.com/fgnt/meeteval`, SegLST as default I/O format.

**The single most useful fact in this report: `cpWER − ORC-WER` is exactly the cost of speaker
confusion**, isolated from recognition error. Reporting both is how we prove the OBS/ORG layer did
something rather than the core just transcribing better.

**"Was this summary sentence attributed to the right speaker?" — NO STANDARD METRIC EXISTS.** A
direct search found only cpWER (transcript-level) and AttrScore (citation-to-document attribution, a
different problem). The closest published pairing is 2509.18377's **DER + speaker substitution
error**, still transcript-level. This is a real, defensible gap — but it means we must *define* the
metric ourselves, with a written, pre-registered protocol.

**Factuality / hallucination metrics.** Entity-level precision/recall (Nan et al., **EACL 2021**,
`2021.eacl-main.235` / 2102.09130) — cheapest, most speech-relevant, directly coupled to our
glossary layer. **QAFactEval** (**NAACL 2022**, `2022.naacl-main.187`) — QG → QA → answerability →
overlap; +14% over prior QA-based metrics. **SummaC** (**TACL 2022**, `2022.tacl-1.10`) — sentence-pair
NLI with aggregation; SummaC_Conv 74.4 balanced accuracy. **AlignScore** (**ACL 2023**, 2305.16739) —
355M unified alignment model over 22 datasets, matching or beating GPT-4-based metrics.

### 4.2 Recommended protocol

Constraints honoured: frozen API-only core, zero training, no logit access, no gold labels at
runtime, discovery/confirmatory isolation, everything hashable.

**Tier 0 — substrate quality (deterministic, mandatory, never the headline).**
1. **tcpWER** via **MeetEval** — primary speaker-attributed transcription metric; fix and record the
   collar explicitly after reading the toolkit doc.
2. **cpWER** — secondary, for comparability with Dixtral and the CHiME/AliMeeting literature.
3. **ORC-WER** — **required**, reported alongside cpWER, with **cpWER − ORC-WER** as an explicit line
   item. Without it a reviewer cannot separate our speaker decomposition from plain ASR gains.
4. **DER + speaker substitution error**, as a pair, following 2509.18377. Diagnostic only.
5. **Glossary efficacy**: **B-WER vs U-WER** split plus **false-alarm rate**. The false-alarm term is
   non-negotiable — prompt-injected glossaries hallucinate entities never spoken, and a recall-only
   number hides it. Evaluate on **Contextual Earnings-22** (2604.07354) so "keyword prompting" is a
   published baseline rather than a strawman.

**Tier 1 — task accuracy (deterministic; THIS IS THE HEADLINE).**
6. **M3-SLU** (2510.19358) — speaker-attributed QA accuracy + speaker-attribution-via-utterance-
   matching accuracy. AMI-derived, audio-bearing, exactly our claim surface, and its stated finding
   ("models capture what was said but often fail to identify who said it") is our thesis restated by
   a third party.
7. **MeetingQA F1** — multi-span cross-speaker extractive QA; human ceiling 84.6, model floor 57.3
   gives an interpretable band.
8. **ELITR-Bench** or **AutoMin 2025 QA** — optional third surface; keep supplementary.

Lead with Tier 1: it needs no judge, no reference summary, and no human panel.

**Tier 2 — minutes content coverage (reference-based, secondary).**
9. QA-based content overlap in the MeetingBank protocol against reference minutes.
10. **ROUGE-1/2/L and BERTScore** in a clearly labelled **"legacy comparability"** row only, with a
    footnote citing the survey critique. Present so reviewers can situate us; never used to support
    a claim.

**Tier 3 — faithfulness and attribution correctness (reference-free; our contribution).**
11. **Entity-level precision/recall** (Nan et al.) of minute entities against the speaker-attributed
    reference transcript.
12. **Faithfulness ensemble: AlignScore + SummaC + QAFactEval** — an ensemble because TofuEval shows
    individual metrics capture different error types, and because these specialized models beat
    GPT-4 at exactly this judgement.
13. **SAER-M (Speaker-Attribution Error Rate for minutes) — we must define it, because nothing
    published does.** Proposal: for each minute bullet carrying a speaker claim, align its supporting
    span to the reference speaker-attributed transcript; the bullet is correct iff the claimed
    speaker matches the reference speaker of the majority-support span. Report as (attributed
    bullets, correct attributions, **unattributable bullets**), exposing the unattributable count
    rather than dropping it. **Pre-register the alignment rule and tie-breaking policy before any
    run, publish the scorer, hash it.** Otherwise a reviewer reads it as a metric tuned to our output.

**Tier 4 — judged quality (last, heavily fenced, never load-bearing alone).**
14. Error-typed rubric judging in the **MESA** shape over the **QMSum Mistake** nine-error taxonomy
    (which already spans ICSI + AMI + parliament).
15. **Mandatory guardrails, all of them:**
    - **Judge model must be outside the Qwen/omni family under test** — self-enhancement bias. This
      is structural for us: the core under test *is* Qwen3-Omni class.
    - **Position swap** on every pairwise comparison; report both orders.
    - **Reference-guided grading** where a reference exists; length-controlled comparisons.
    - **A human-annotated calibration subset is required.** Report **Krippendorff's α** or weighted
      κ against it. **If agreement is not reported, the judge number is not reported.** QMSum
      Mistake's α = 0.793 is the bar.
    - Judge scores explicitly flagged as long-context-unreliable, citing AutoMin 2025's own 0.17/0.13
      correlations.
16. **CREAM ELO** for **system ranking only** — ordering our own variants; never an absolute score.

**Metrics we explicitly refuse.**

| Refused | Why |
|---|---|
| **ROUGE as headline** | Three peer-reviewed grounds (EMNLP 2025 survey, CADS/JAIR 2025, EMNLP 2024 Findings) plus AutoMin's own 2022 admission that metric design was an open problem. Legacy row only. |
| **Bare WER on meeting audio** | Charges nothing for speaker confusion — it cannot see the thing we claim to improve. ORC-WER exists precisely to expose this. |
| **DER as headline** | Timing metric, content-blind. A system can win DER and still mis-attribute the one sentence the minutes turn on. |
| **BERTScore as a factuality claim** | Similarity, not entailment; plus a 512-token limit meetings routinely exceed. |
| **Reference-free LLM-judge as sole quality evidence** | TofuEval (GPT-4 loses to specialized metrics); AutoMin 2025's 0.17/0.13 correlations; 2604.21345 shows the judge-only endgame — no agreement reported, non-significant differences. |
| **Same-family self-judging** (Qwen judging Qwen) | Self-enhancement bias; structurally indefensible here. |
| **WenetSpeech `test_meeting` as our meeting evidence** | The only "meeting" set most omni reports publish — and it is Chinese, single-stream and speaker-blind. Cite only when characterizing what the field currently reports. |
| **MMAU / MMAR / MMAU-Pro as our benchmark** | Where AudioToolAgent and Audio-Mind live, but short-clip audio QA. Using them concedes the meeting framing that is our only defensible ground. |
| **Any metric needing gold labels, reference transcripts, or future turns at runtime** | Blocked by our own research boundary, and the first thing a reviewer probes on a training-free claim. |

**Sequencing.** Run Tier 0 and Tier 1 first and let them stand alone. If Tier 1 does not move, no
amount of Tier 4 judging will make the claim reviewable — and given Dixtral's Interspeech 2026 cpWER
results against Gemini 3.0 Flash and Voxtral, a reviewer will already have a strong trained baseline
in mind when reading our zero-training numbers.

---

## 5. Risk register for the direction

| Risk | Source | Mitigation |
|---|---|---|
| **Self-reinjection amplifies the model's own errors** | 2511.18774: self-prompt alone 29.01% vs 15.79% baseline | Abstract + normalise + dedupe + evidence-gate the glossary; run the naive-reinjection arm as a measured control, not an assumption |
| **Glossary false alarms** — injected entities hallucinated into output | LOGIC (withdrawn) taxonomy; 2608.05759 distractor sensitivity | Report B-WER, U-WER **and false-alarm rate**; prefer precision over recall |
| **Prompt order and list size effects** | 2608.05759; Whisper 224-token cap; lost-in-the-middle | Pre-planned glossary-size sweep and order-randomisation control |
| **~40% of gold key terms never appear in pass-1 output** | classical ICSI keyword extraction: 59.74% survival | State the recall ceiling up front; treat it as the headroom bound |
| **EGTA convergence (one month old)** | 2607.17766 | Claim on term-table *provenance* + API-only boundary; show prompt-only path carries the gain |
| **Audio-Mind "conditional evidence acquisition"** | 2605.28480 | Read in full; address explicitly in any novelty argument |
| **Dixtral is a strong trained baseline on our exact metric** | 2606.18134, Interspeech 2026 | Scope explicitly to the API-only regime; expect worse absolute numbers and say so |
| **40-minute audio cap on our own core** | Qwen3-Omni TR | Chunking is forced; ICSI (~1 h) exceeds it, AMI mostly fits — make the chunk boundary the glossary carry point |
| **Frontier-LLM baseline beats bespoke systems** | AutoMin 2025 collapse | Baseline must be a strong long-context prompt, never a weak pipeline |

## 6. Verification debts (do not write these into a paper unchecked)

1. **AutoMin-2021 ROUGE–human correlation coefficients** — snippet-only; the ISCA PDF would not
   extract. Re-read `isca-archive.org/automin_2021/ghosal21_automin.pdf`.
2. **MeetEval tcpWER default collar** — GitHub returned 503. Read `fgnt/meeteval/doc/tcpwer.md`
   before pinning it in config.
3. **Qwen3-Omni WenetSpeech `test_meeting` cell** — an extraction returned an implausible
   "English 4.69 / Chinese 5.89" split for a Chinese-only test set. Re-read Table 6. The 40-minute
   limit, by contrast, is a direct quote and is solid.
4. **Kimi-Audio 6.28** — snippet, not table-verified.
5. **TagSpeech / SoulX-Transcriber / G-STAR / DNCASR / JEDIS-LLM numbers** — abstract pages carried
   no tables; all numbers unverified.
6. **CHiME-8 baseline tcpWER/DER table** — extracted by automated page summarization; the DiPCo
   dev 98.3 / eval 56.6 asymmetry looks anomalous. Re-verify against the paper's own tables.
