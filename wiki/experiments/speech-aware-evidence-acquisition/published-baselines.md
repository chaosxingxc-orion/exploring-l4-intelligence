---
title: "Published baselines per carrier: speech-aware evidence acquisition"
study_slug: "speech-aware-evidence-acquisition"
source_surveys: "study repo docs/readiness/2026-08-07-*.md (R0.1, model-free)"
maintained: "living page — 'ours' rows filled in place after each probe's ledger row lands"
---

# Published baselines per carrier (living table)

Purpose: the **published numbers** extracted by the R0.1 survey, laid out as a comparison table by carrier.
After each small probe (study repo `docs/readiness/2026-08-07-r1-replan-reproduction-plan.md` P1–P2)
completes, the corresponding "ours" row is filled in place, and subsequent improvement work proceeds
against this table as its baseline surface.

Discipline: this page registers only summary values plus pointers; numeric authority lives in the study
repo receipts/MLflow and in each paper's original text. **Rows are not directly comparable across the
table** unless the protocol column matches — different papers use different front-end ASR, subsets and
scorers; an "ours" row is meaningful only against a comparison row sharing its protocol and sample.
Probe samples are always the discovery/dev split (split freeze receipt: discovery 44 / dev 10 /
confirmatory 115, study `docs/receipts/splits.json`).

Legend: `[abl]` = the difference is supported by an ablation/controlled comparison in the source paper;
`(t)` = obtained by training (outside our boundary, kept only as a structural-gap comparison);
**ours** rows start empty and carry a ledger row id when filled in.

## Comparability error budget (2026-08-09, measurement first; read before citing any ours number on this page)

When placing our WER alongside published numbers, **the error is not ±2% but the sum of the items below**;
the largest is sampling, and the most easily overlooked is the normalization convention.

| Item | Magnitude | Nature | Basis |
|---|---|---|---|
| Sampling (E-001 uses 10/125 calls) | **±2.5pp** | Random, the largest item | Measured per-call WER variance (SD≈3.6, SEM≈1.14) |
| Number-normalization convention | **1.3–1.8pp** | Systematic, against us | Measured: rescoring the same outputs with number expansion moves corpus-level WER 26.70%→24.93% (expanded to words) / 25.42% (collapsed to digits) |
| Aggregation (macro vs micro average) | 0.04pp | Negligible | Measured: 26.74% vs 26.70% |
| fstalign synonym transforms | Not measured, estimated <0.5pp | Systematic | The Earnings-21 paper reports an effect on roughly 0.3% of disputed tokens |
| Corpus difference (E-21 vs E-22) | Not quantified | Against us | Earnings-22's whole thesis is "accented speech is harder" |
| System class (dedicated ASR vs frozen omni + agentic loop) | Not quantifiable | — | — |

**Root cause**: this repository's frozen `normalize_text_v1` explicitly performs no number expansion
("no number expansion"), whereas the fstalign used by the Earnings-21/22 papers applies text-normalization
transforms (affecting roughly 5% of reference tokens, typically `2021 ↔ twenty twenty one`). The earnings
domain is number-dense and our core verbalizes numbers, so the frozen metric records **spelling-convention
differences** as recognition errors.

**Rules of use**: (1) this study's conclusions rest on **paired-arm comparisons at the same model and the
same protocol**, where only sampling limits them; (2) any comparison with published numbers must state the
table above; (3) when numeric comparability is needed, prefer the **same-metric calibration** below over
the paper numbers.

### Same-metric calibration: rescoring published systems with this repository's frozen scorer (2026-08-09)

The Earnings-21 release package ships locally with each system's **raw transcription outputs**
(`earnings21/output/{amazon,google,microsoft,rev,speechmatics,kaldi_org}`, `.nlp` format, isomorphic to the
reference). Rescoring them with **this repository's frozen `normalize_text_v1` + alignment**, over the same
10 calls as the R4 mini sample:

| System | Paper value (fstalign, all 44 calls) | This repository's metric (same 10 calls) | Difference |
|---|---|---|---|
| Amazon | 17.0% | **15.70%** | −1.3pp |
| Google | 17.8% | **16.36%** | −1.4pp |
| Microsoft | 15.8% | **17.95%** | +2.2pp |
| Speechmatics | 16.0% | **17.07%** | +1.1pp |

(Rev and Kaldi are not included: Rev's directory structure differs from the rest and Kaldi is in `.ctm`
format; 4 systems are enough to calibrate, and under the "take an approximate conclusion at the verification
step" policy this is not extended further.)

**Conclusion**: this repository's metric reproduces published numbers to within **±1.3–2.2pp** (which
already contains both the 10/44 sampling and the normalization sources). This repository's E-21 numbers
can therefore **be placed alongside published tables**, provided a ±2pp tooling-convention tolerance is
declared; that is far stronger than "ordinal comparison only". **Same-sample, same-metric target band:
15.70% (Amazon, best) – 17.95% (Microsoft).** The R4 no-context arm's output can be compared directly
against that band.

## earnings21 / earnings22 / conec (Family A)

| system / condition | protocol | metric | value | source |
|---|---|---|---|---|
| ConEC conventional ASR, no-bias floor | ConEC LREC-COLING 2024 | WER | 10.41 (bias conditions span 10.29–10.66; insensitive to aggregation) | ConEC paper |
| Siskos black-box ASR, no-context | Siskos EMNLP-F 2025, E21 | WER | 35.9 | arXiv:2509.19567 |
| Siskos + CB-RAG context `[abl]` | same as above | WER | 31.1 | same as above |
| Siskos + CB-LLM context `[abl]` | same as above | WER | 31.8 | same as above |
| Siskos + oracle context `[abl]` | same as above | WER | 29.7 | same as above |
| RECOVER correction (t? — LLM correction pipeline, claimed black-box) | RECOVER preprint, E21 among 5 sets | rel. E-WER ↓ / recall ↑ | 8–46% rel / up to +22pp | arXiv:2603.16411 (not peer-reviewed, no code) |
| **ours: SAEA-E-001 bare-core reference floor (e22 dev subset10, 10 calls)** | obs-agent-loop segmentation protocol (60s buffer, model segmentation + VAD snapping + bounded stepping), INT4 Qwen3-Omni, openJiuwen executor, frozen asr-wer | WER | **0.2674** (per call 0.2157–0.3252; 795 slices / 47,393 audio-s / 2.53 GPU-hours) | filled in 2026-08-09; ledger row SAEA-E-001; **comparison evidence**: the same model under the whole-call protocol produced only 2–106 words (retired), while after segmentation it produces 7,556–11,036 words |
| **ours: no-context / matched-ConEC / mismatched (R4=P2b=SAEA-E-002; T4 extension = ConEC bias-list entity-class injection)** | 3-arm, a frozen 10-of-44 mini subset of earnings21-discovery (sample-once receipt, manifest-bound); each of the three arms has 610 slices with exactly identical audio seconds (paired design) | WER (entity-level WER pending an owner-pinned wer_tags adapter) | running (2026-08-09) | the analysis convention was pre-registered before results were seen: paired exact Wilcoxon + median difference + bootstrap CI, unit = call |
| **ours: Earnings-21 full 44-call direct baseline (ALIGNED)** | `bare-core`, no context, fixed 90-s windows, no VAD, greedy, Q4_K_M on build 04ccc72a, audio through the GPU-resident bf16 mmproj; all 44 discovery calls (39.26 h, 1,593 windows, 0.97 GPU-h); Whisper `EnglishTextNormalizer` both sides, corpus-level (359,765 reference words) | WER | **8.200** (mean of calls 8.004; `saea-scoring-v1` 12.588, not comparable; call 4346923 18.94, corpus without it 7.888; entity WER 30.36 mention-level over 38,366 mentions) | `SAEA-E21-FULL44-DIRECT-BASELINE-V2`, 2026-09-04; verdict `studies/speech-aware-evidence-acquisition/docs/readiness/2026-09-04-e21-full44-direct-baseline-v1-verdict.md`. ALIGNED under the study's 3-point rule against `openai/whisper-large-v3` 9.71 (ASR Leaderboard long-form) and Whisper large-v2 9.7, TRADE 9.75; every degraded floor cleared (medium.en 10.2, small.en 10.8, base.en 12.5). Caveats: Whisper's own decoding heuristics move this set by 1.1; we do not apply `merge_compounds`; the fstalign family (Rev ESPNet 11.3) is a different metric and is not compared |
| **ours: Earnings-22 ESB short-form test (NOT ALIGNED)** | the ESB 6-call test subset (2,735 published utterances, cut locally at the published boundaries), one utterance per contact, the verbatim-transcription instruction the sealed flight sent (quoted in its verdict), greedy, Q4_K_M on build 04ccc72a, bf16 mmproj; Whisper normalizer, corpus-level | WER | **15.937** (per call 14.1 to 22.2; insertions 59 % of errors, hypothesis 1.075x reference length; an oracle length cut alone gives 10.456) | `SAEA-E22-ESB-SHORTFORM-ALIGNMENT-V1`, 2026-09-05; verdict `studies/speech-aware-evidence-acquisition/docs/readiness/2026-09-04-e22-esb-shortform-alignment-v1-verdict.md`. Against the same frozen model's published zero-shot 9.79 (NVIDIA NeMo AutoModel doc) and 12.3 (Nemotron 3 Nano Omni Table 8): NOT ALIGNED (+6.15 / +3.64); floors whisper-large-v3 11.59 and base.en 15.09 not cleared. Diagnosis: output discipline against cleaned sentence references (continuation past the clip, verbatim stutters), i.e. the verbatim instruction and the context-free clip, not recognition; the one-time confirmatory read is spent |
| **ours: Earnings-22 dev prompt A/B (diagnostic, dev split)** | the ten dev calls cut at the ESB train-split boundaries (6,038 utterances, 10.9 h, cleaned references), two arms differing only in the instruction text: A = the flown verbatim instruction, B = the Qwen3-Omni model card's default ASR prompt "Transcribe the English audio into text."; Whisper normalizer, corpus-level | WER | A **17.565**, B **18.394** (paired B minus A -0.83, CI90 -1.65 to -0.17, sign test p 0.00055; insertions 62 % of errors and hypothesis 1.09x reference length under BOTH prompts, rising to 1.21x under one second) | `SAEA-E22-DEV-ESB-PROMPT-AB-V1`, 2026-09-05; verdict `studies/speech-aware-evidence-acquisition/docs/readiness/2026-09-05-e22-dev-esb-prompt-ab-v1-verdict.md`. The prompt text is excluded as the cause of the short-form gap; the verbatim instruction stays. Next suspect under test: the model card's evaluation shape (no system message, text after the audio) |
| **ours: Earnings-22 dev official request shape, arm C (diagnostic, dev split)** | same 6,038 dev utterances; the Qwen3-Omni model card's evaluation shape (no system message, instruction text after the audio, default prompt), proven through the rendered template (16 text tokens, no system block); everything else as arms A/B | WER | **17.890** corpus (A 17.565); per-utterance mean 31.31 (A 33.12); length ratio 1.040 (A 1.086), insertions 49 % of errors (A 62 %), zero CJK hypotheses (A 14) | `SAEA-E22-DEV-ESB-SHAPE-C-V1`, 2026-09-05; verdict `studies/speech-aware-evidence-acquisition/docs/readiness/2026-09-05-e22-dev-esb-shape-c-v1-verdict.md`. Shape EXCLUDED as the cause: it removes 2,176 insertions and pays 2,605 deletions; over-generation was a symptom. Next suspects, model-free first: the cleaned ESB reference layer's own conventions (e.g. `merge_compounds`), then a self-run whisper-large-v3 anchor, context-free clipping, quantization |
| **ours: Earnings-22 dev semantic error scan and clip-boundary audit (diagnostic, dev split, 2026-09-06)** | the three sealed dev arms (10 calls, 6,038 ESB utterances) aligned raw and Whisper-normalized, 32-rule taxonomy, three-level semantic impact; the clip cut audited against the published timestamps and the ESB released arrays (durations only) | agentic error rate (HIGH-impact reference-word mass / reference words) beside corpus WER | arm A: WER 17.56, agentic **1.92** (9x apart); 42.6 % of error mass semantically inert; 47.6 % of the mass is boundary speech (868 of 2,828 tail insertions reproduce the next utterance); scoring conventions with authority are worth 0.25 points; the published segments overlap each other (77.7 % of adjacent pairs, cap 0.18 s) and the ESB released arrays carry the same overlap, so a boundary-exact number is never an alignment argument | `SAEA-E22-MF-SEMANTIC-ERROR-SCAN-V1`, `SAEA-E22-MF-CLIP-BOUNDARY-AUDIT-V1`, `SAEA-E22-MF-ESB-ARRAY-DURATIONS-V1`; notes under `studies/speech-aware-evidence-acquisition/docs/readiness/2026-09-06-e22-*.md`. Remaining E22 alignment suspects: decode/stop behaviour, quantization, the audio front-end. |
| **ours: Earnings-21 full-44 direct baseline under the agentic metrics (2026-09-06)** | the sealed all-44-call direct baseline re-scored, zero contacts, through byte-identical re-scoring bundles: ConEC per-entity WER mirrored from fstalign `RecordTagWer` ((S+D)/tagged reference words, insertions never attributed; `official_tool_run: false`), numeric-value accuracy (digit-bearing reference words after the Whisper normalizer), corpus WER as the anchor | ConEC entity WER (ours / ConEC Table 2 Whisper-large / no-biasing / oracle) | PERSON **22.5** / 28.9 / 45.9 / 13.0; ORG 17.2 / 19.6 / 29.5 / 17.7; GPE 18.7 / 17.0 / 18.8 / 12.9; PRODUCT 19.2 / 18.7 / 24.2 / 19.2; corpus WER 8.200 reproduced to the digit; numeric-value accuracy 90.73 (construction 34 calls 90.22, evaluation 10 calls 92.43) | `SAEA-E21-MF-AGENTIC-METRIC-BASELINE-V1`, 2026-09-06; note `studies/speech-aware-evidence-acquisition/docs/readiness/2026-09-06-earnings-agentic-metric-baseline-v1.md`; literature `.../2026-09-06-earnings-agentic-metric-literature.md`. PERSON is the room a pre-meeting brief can take; ORG is already below the ConEC oracle. |

## slurp (Family B)

| system / condition | protocol | metric | value | source |
|---|---|---|---|---|
| Multi-ASR + HerMiT pipeline (t) | SLURP EMNLP 2020 official | IC-comb / SLU-F1 | 76.68 / 69.53 | arXiv:2011.13205 |
| Best adapted pipeline (t) | same as above | same as above | 78.33 / 70.84 | same as above |
| gold-transcript NLU upper bound (t) | same as above | same as above | 84.84 / 78.19 | same as above |
| CTI E2E (t) | CTI 2021 | IC / SLU-F1 | 82.93 / 71.12 | arXiv:2104.07253 |
| SFT Qwen2-Audio-7B (t) | ICASSP 2026 | IC / SLU-F1 | 88.13 / 76.75 | arXiv:2509.15389 |
| UniverSLU (t) | NAACL 2024 | IC | ~90.3 (attributed via retrieval; re-verify before freezing) | arXiv:2310.02973 |
| zero-shot SF: ZS-Whisper-SLU → WHISMA (t) | respective papers | SLU-F1 | 50.0 → 63.3 (supervised reference 69.9) | arXiv:2408.16423 |
| AIR-Bench direct answering (8 systems, best Qwen-Audio-Chat) | AIR-Bench 1k subset, GPT-4 judge | acc | 77.8 (worst NExT-GPT 25.6) | arXiv:2402.07729 |
| AIR-Bench cascade Whisper+GPT-4 `[abl]` | same as above | acc | 87.7 | same as above |
| **ours: direct vs self-cascade (R3=P2a)** | AIR-Bench 200 paired questions, deterministic scoring | acc | — | to be filled in |
| **ours: prompt-only slot filling (T3, the plan P3 analogue track)** | official scorer, samples registered through the sample-once manifest | SLU-F1 | — (no precedent in the literature; the corresponding ZS line is 50.0→63.3) | to be filled in |
| **ours: SLURP closed-list direct baseline (the study's direct baseline from 2026-09-05)** | DEV-1000 devel roster (equal-stratum, headset + far-field natural mix), zero-shot, one contact, the M0 instruction plus the 60 TRAIN-observed scenario_action pairs; official `evaluate.py` micro, 1,000 / 1,000 predicted, 0 skipped; Q4_K_M on build 04ccc72a | scenario / action / intent / SLU-F1 | **81.00 / 73.90 / 71.40 / 35.80** (sealed M0: 70.00 / 61.50 / 53.60 / 36.90; locked BLEND knowledge cell: 83.90 / 77.60 / 75.70 / 41.69) | `SAEA-SLURP-DEV1000-CLOSED-LIST-DIRECT-V1`, 2026-09-05; verdict `studies/speech-aware-evidence-acquisition/docs/readiness/2026-09-05-slurp-closed-list-direct-baseline-v1-verdict.md`. Intent is within 3 points of the weak commercial pipeline (72.06) and of ChatGPT-on-Whisper-ASR (72.89); SLU-F1 stays 28 points under the weakest trained pipeline (64.02), no prompt-only published counterpart exists. BLEND's intent margin over the direct baseline shrinks from +22.1 (vs M0) to +4.3 pooled and +2.6 (CI90 -0.2 to +5.6) on the unexposed 500: 80 % of the locked cell's intent gain was the missing pairing list; slot filling is the open target |
| **ours: KC-S1b, a separate slot contact with the per-intent TRAIN schema (mechanism, ADMITTED)** | DEV-1000; the sealed closed-list intent prediction is the input; one added contact asks only for entities, with the TRAIN per-intent slot schema block (types at >= 2 % share, up to 5 lowercase fillers; 42 rows fall back to the full schema); intent identical by construction; official `evaluate.py` | SLU-F1 (entity strict / Word-F1 / Char-F1) | **44.35** (31.37 / 41.58 / 47.51) vs the closed-list baseline 35.80 and the locked BLEND knowledge cell 41.69; paired on the unexposed 500: +10.11 (CI90 +8.11 to +12.19, 60 saves / 2 harms); the contact-count control KC-S1a (no schema) +0.09 (CI90 -0.20 to +0.38) | `SAEA-SLURP-KC-S1B-SLOTS-SCHEMA-DEV1000-V1`, 2026-09-05; verdict `studies/speech-aware-evidence-acquisition/docs/readiness/2026-09-05-slurp-slot-stage-kc-s1-v1-verdict.md`. First admitted mechanism of the three-dimension program; precision and recall rise together (29.98 -> 37.54, 17.26 -> 26.95); still 19.7 points under the weakest published trained pipeline (64.02); devel only, rung 1 |
| **ours: KU-S1c, the two-contact draft-revise control (no knowledge; reported, not decided)** | DEV-1000; phase 1 = the closed-list task, phase 2 = "revise if needed, else repeat", the closed-list instruction as the system message in both phases; two contacts per row; official `evaluate.py` | intent (SLU-F1) | **72.90** (35.92) vs the closed-list baseline 71.40 (35.80); paired on the unexposed 500: +1.60 (CI90 -0.20 to +3.40, includes zero); revise over its own draft +0.30 (CI90 -0.40 to +1.00); the second contact buys nothing on its own | `SAEA-SLURP-KU-S1C-DRAFT-REVISE-DEV1000-V1`, 2026-09-06; verdict `studies/speech-aware-evidence-acquisition/docs/readiness/2026-09-05-slurp-consumption-ku-s1-v1-verdict.md`. Every two-contact SLURP delta is stated net of this control. KU-S1 (alpha-blend with the closed-list instruction) was REFUSED before registration by the snapshot-containment rule (unread, zero contacts): supply must travel the traced typed-content channel, which the phase-program base cannot yet emit; enabler E6 (traced supply) precedes every knowledge-supplying phase cell. |
| **ours: SLURP closed-list direct baseline, RE-LOCKED with legal-label projection v2 (local optimization, 2026-09-06)** | the same sealed DEV-1000 outputs re-scored with a deterministic post-processor (an illegal scenario that equals a legal action name is promoted to its owning scenario; otherwise nearest legal intent by edit distance inside the scenario, TRAIN prior on ties); zero model contacts; official `evaluate.py` | intent (SLU-F1) | **73.10** (35.80) vs 71.40 unprojected: +1.70 pooled (17 saves / 0 harms, CI90 +1.1 to +2.3), NEW500 +2.00; the whole gain is the recommendation scenario (46.67 to 71.67); entities unchanged row by row | `SAEA-SLURP-MF-LEGAL-LABEL-PROJECTION-RELOCK-V1` (v1, +0.20) and `SAEA-SLURP-MF-LEGAL-LABEL-PROJECTION-V2-V1` (v2), 2026-09-06; verdict `studies/speech-aware-evidence-acquisition/docs/readiness/2026-09-06-slurp-legal-label-projection-v2-verdict.md`; scorer `slurp-slu-official-projected-v2`. Every later SLURP mechanism pairs against 73.10 / 35.80. |
| **ours: MF-7 / MF-7b retrieval-key audit; neighbour retrieval on SLURP intent CLOSED (2026-09-06)** | DEV-1000 recordings as queries, the 11,514 TRAIN utterance texts as keys, k = 5, corrective net (saves - harms) vs the re-locked comparator on NEW500, CI90; embedders GLAP (CPU), LCO-Embedding-Omni-3B (llama.cpp), Omni-Embed-Nemotron-3B (transformers); queries speech alone, speech + draft as one multimodal input, rank-level speech + prior | intent net corrective power (pp of NEW500 rows) | best speech-containing query = Nemotron fused **+0.60** (CI90 -2.40 to +3.60, echo 74.8 %), gate was >= 2.0 with lower bound > 0; Nemotron speech alone -3.40, GLAP -34.60, LCO -71.20; transcript-text ceiling +11.00 and the draft-text key -11.40 are diagnostics only (owner rule: a query must contain speech). The omni embedder nearly closes the cross-modal gap (recall@5 87.4 vs the 93.8 text ceiling) but its vote ties the baseline; filler recall@5 +7.90 over the draft key is handed to the slot side | `SAEA-SLURP-MF-RETRIEVAL-KEY-AUDIT-V1`, `-V2`, `SAEA-SLURP-MF7B-LCO-EMBEDDING-V1`, `SAEA-SLURP-MF7B-NEMOTRON-EMBEDDING-V1`; notes `studies/speech-aware-evidence-acquisition/docs/readiness/2026-09-06-slurp-retrieval-key-audit-v{1,2}.md`. KU-S1 (alpha-blend with the closed-list instruction) stays unflown by rule; retrieval is re-scoped to slots (KU-S3) and Audio2Tool (KU-A1). |
| **ours: EVO-S1 round 1, the SLURP slot-schema evolution loop (system evolution, REJECT; 2026-09-06)** | TRAIN folds of 60 utterances per scenario (fold A 1,080 / fold B 1,080), K_1 = 5 candidates per scenario (three proposer rewrites on the text-only construction arm, a shares-only control, a token-matched form twin), stage-one admission saves >= 4 / harms <= 2 per 60 rows / net >= 3 on the per-row strict slot F1, confirmation on fold B (pooled targeted CI90 lower bound > 0, per-scenario harm bound, unadmitted pooled >= -1.0 pp) | per-row strict slot F1 (reward); official SLU-F1 reported | stage one admitted 2 of 18 scenarios (news, social); fold-B assembly +2.50 pp on the 120 targeted rows (6 saves / 2 harms / 112 ties) with a CI90 lower bound of exactly 0 against a strict > 0: REJECT, A_1 = A_0. Instrument finding: 1,019 of 1,080 fold-B rows were asked byte-identical prompts and 28.1 % of them returned different text (greedy nondeterminism), moving 15 saves / 16 harms on unchanged prompts, so a 60-row count gate sits below the noise floor; one admitted "winner" rendered byte-identical to the incumbent | `SAEA-SLURP-EVO-S1-{PROPOSER,FOLD-A,FOLD-B}-V2` round-1 attempts (rows stay consumed = no), 2026-09-06; verdict `studies/speech-aware-evidence-acquisition/docs/readiness/2026-09-06-slurp-evo-s1-round-1-verdict.md`. Round 2 waits on the owner: a paired null-control re-fly to calibrate the gate, a bootstrap-CI admission rule, or 120 rows per scenario. |

## speech-massive (Family B)

| system / condition | protocol | metric | value | source |
|---|---|---|---|---|
| Cascade Whisper+mT5, cross-lingual zero-shot (t) | Interspeech 2024 official | IC avg / slot-F1 avg | 69.10 / 43.15 | arXiv:2408.03900 |
| Cascade, full fine-tuning (t) | same as above | same as above | 83.04 / 61.21 | same as above |
| gold-NLU upper bound (full fine-tuning) (t) | same as above | IC avg | 86.73 | same as above |
| E2E Whisper FR (t) | same as above | IC (FR) | 85.87 | same as above |
| SFT Qwen2-Audio FR (t) | ICASSP 2026 | IC / SLU-F1 | 87.39 / 74.86 (metric definition ≠ slot-micro-F1) | arXiv:2509.15389 |
| **ours (if a probe is opened)** | — | — | — (prompt-only multilingual SLU is a gap in the literature) | — |

## minds14 (Family B — diagnostic carrier)

| system / condition | protocol | metric | value | source |
|---|---|---|---|---|
| LaBSE translate-to-EN + MLP (t) | Gerz 2021, 3-fold random 60/40 (**no canonical split**) | acc avg | 95.9 | arXiv:2104.08524 |
| MAEB embedding probe | MAEB 2026 | probe score | Qwen2-Audio 25.51 / Whisper-medium 48.30 | arXiv:2602.16008 |

## slue-sqa-5 / spoken-squad / heysquad (Family C)

| system / condition | protocol | metric | value | source |
|---|---|---|---|---|
| SLUE-SQA-5 pipeline-oracle: gold transcript + DeBERTa (t) | SLUE Phase-2 ACL 2023 | frame-F1 (test/verified) | 62.3 / 70.3 | arXiv:2212.10525 |
| SLUE-SQA-5 best real pipeline (NeMo ASR+DeBERTa) (t) | same as above | frame-F1 (test/verified) | 43.3 / 45.9 (w2v2 39.6/40.1; whisper 32.7/35.7) | same as above |
| SpeechDPR (t) | ICASSP 2024 | Top-20 retr. / OpenSQA frame-F1 | 19.73 / 0.558 (cascaded teacher-student 19.94-19.90 / 0.561-0.565; SpeechDPR is clearly ahead when WER>40% `[abl]`) | arXiv:2401.13463 |
| Spoken-SQuAD 2018 floor: best FusionNet (t) | Interspeech 2018, ASR WER 22.7 | EM / F1 | 46.51 / 60.06 (clean-text mean upper bound 64.41/74.54) | arXiv:1804.00320 |
| Su & Fung 2020 literature ceiling (t) | ICASSP 2020 | F1 | 77.67 | IEEE 9053979 |
| HeySQuAD fine-tuning (t) | arXiv:2304.13689 | relative gain | +12.51% (human-voice transcripts included in training) / +2.03% (evaluated on higher-quality transcripts) `[abl]`; absolute EM/F1 from the source table still to be recorded (optional) | same as at left |
| AudioBench direct-answering row (slue_p2_sqa5) | AudioBench, LLM-judge 0-100 | judge score | SALMONN 83.92; Qwen2-Audio-Inst 82.99; Qwen-Audio-Chat 80.05; WavLLM 76.12; **cascade Whisper+Llama3 76.12 — here direct answering > cascade (a counter-direction data point for closed-book document QA)**; the spoken_squad row is not in the paper's v4 table (leaderboard side; re-verify at freeze time) | arXiv:2406.16020 |
| **ours: AudioBench protocol rerun (A1, scorer replacement)** | sampling + pinned open-source judge | judge/EM-F1 | — | to be filled in |
| **ours: T1 SpeechDPR analogue (training-free retrieval)** | core transcript + pinned BM25, bounded pool (not proportionally comparable to the paper's full corpus) | Top-N / frame-F1 | — (directional comparison 19.73 / 0.558) | to be filled in |
| **ours: T2 SpeechRAG analogue (retrieval ladder closed-book/retrieved/oracle)** | core-transcribed passages + pinned retriever (spoken-squad) | EM/F1 | — (compared against the "no degradation" claim; doubles as the Family C SUPPLY sensitivity ladder) | to be filled in |

## ami-meeting-corpus (Family E)

| system / condition | protocol | metric | value | source |
|---|---|---|---|---|
| QMSum training baseline (t) | NAACL 2021 | ROUGE | values still to be extracted (archival only; the metric is insensitive to evidence `[abl]` MS-AMI) | Yale-LILY/QMSum |
| MeetingQA fine-tuned extractor (t) | ACL 2023 | span-F1 | 57.3 (human 84.6) | adobe/meetingqa |
| CMT-LLM (t) | Interspeech 2025 | WER (AMI SDM, 1k distractors) | 32.9 | arXiv:2506.12059 |
| PlanRAG-Audio | ACL-F 2026, no code released | ROUGE-L / DER (self-defined task) | cannot be independently scored | arXiv:2605.20414 |

## audio2tool (Family D)

| system | protocol | Tier1 | Tier3 multi-intent | Tier8 blending | source |
|---|---|---|---|---|---|
| **Qwen-3-Omni-30B (the same core) direct answering** | paper protocol, deterministic metric | 92.4 | 74.7 | 41.7 | arXiv:2604.22821 |
| Whisper-v3 + Gemma-27B cascade | same as above | 87.9 | — | 50.5 | same as above |
| **ours: GGUF runtime rerun** | 50×8 frozen split, registered `a2t-toolcall` scorer (tool-name multiset), build 04ccc72a Q4_K_M, n=400 | 64.0 | 50.0 | 26.0 | `SAEA-A2T-DIRECT-CALIBRATION-V1`, 2026-09-04 |
| **ours: official-protocol replication** | the paper code's own protocol string for string (github.com/audio2tool/Audio2Tool @ b9d5383c: full 152-tool registry as compact text in the system prompt, `tool_name(k=v)` output, greedy, 256 tokens) scored with the vendored official `metrics.py` (`a2t-toolcall-official`, primary-tool accuracy), 50x8 frozen split, build 04ccc72a Q4_K_M, n=400 | 60.0 | 72.0 | 34.0 | `SAEA-A2T-OFFICIAL-PROTOCOL-REPLICATION-V1`, 2026-09-04 |
| **ours: tier-1 official population** | same official protocol and scorer, 500 tier-1 queries drawn uniformly (seed 20260803) with the release's first successful speaker each, i.e. the paper code's own population rule; by domain wearables 93.41 (n=91), smart_car 92.68 (n=41), smart_home 55.71 (n=368); equal-domain 80.60 | 65.6 | — | — | `SAEA-A2T-TIER1-OFFICIAL-POPULATION-V1`, 2026-09-04 |
| **ours: tiers 2/5/8 official population** | same official protocol and scorer, 500 queries per tier, first successful speaker each; natural mixture: tier 2 79.6 [76.5, 82.4] vs 84.6 (FAIL by 5.0), tier 5 80.8 [77.7, 83.5] vs 90.6 (FAIL by 9.8), tier 8 46.8 [43.2, 50.5] vs 41.7 (ALIGNED, +5.1); equal-domain: tier 2 85.4, tier 5 89.8, tier 8 47.9; smart_home is the weak stratum on every tier (74.6 / 75.0 / 29.7); EM tier 2 31.2 vs 15.6, tier 8 22.4 vs 12.4 (better), tier 5 22.8 vs 36.0 | — | — | 46.8 | `SAEA-A2T-TIER258-OFFICIAL-POPULATION-V1`, 2026-09-04 |
| **ours: tiers 3/4/6/7 official population** | same official protocol and scorer, 500 queries per tier, first successful speaker each (tier 7 = first user turn, the released loader's rule); natural mixture: tier 3 65.0 [61.4, 68.4] vs 74.7, tier 4 28.2 [25.0, 31.6] vs 33.4, tier 6 75.8 [72.5, 78.8] vs 81.5, tier 7 49.4 [45.7, 53.1] vs 54.6, all FAIL outside CI; equal-domain 73.9 / 35.2 / 83.8 / 58.5, all inside the band; every tier clears the Qwen-2.5-Omni-7B floor; eight-tier table complete: natural mixture 1 of 8 aligned, equal-domain 7 of 8 (tier 1 80.6 vs 92.4 the exception) | — | 65.0 | — | `SAEA-A2T-TIER3467-OFFICIAL-POPULATION-V1`, 2026-09-04 |
| **ours: Q8_0 quantization probe (Factor C, excluded)** | the frozen 400 (50 per tier), byte-identical request to the official-protocol cell, Q8_0 decoder from the umbrella lock served with `--n-cpu-moe 24` expert offload (21,930 MiB VRAM, 20.6 GB host RSS), same bf16 mmproj; official scorer, paired against the sealed Q4_K_M cell | tool acc | Q8 63.25 vs Q4 61.00 (+2.25, CI90 +0.25 to +4.25, two thirds from tier 8); tier 1 60.0 vs 60.0 with 50 of 50 ties; wearables identical on 95 of 95 rows; decision tiers 1/2/5/6 pooled +0.50 (CI90 -1.50 to +2.50) | `SAEA-A2T-Q8-QUANTIZATION-PROBE-V1`, 2026-09-05; verdict `studies/speech-aware-evidence-acquisition/docs/readiness/2026-09-04-a2t-q8-quantization-probe-v1-verdict.md`. QUANTIZATION-EXCLUDED: the Q4_K_M core stays the operating core (Q8 is 7.85x slower per call for +2.25 pp). Closed suspects on Audio2Tool: the reconstruction (-5.5), whitespace (+1.0), roster (+5.6), quantization (0.0 on tier 1). Open: the llama.cpp audio front-end vs the HF processor, and the published tier-1 row itself, unreproduced by five sealed cells |
| **ours: A2T-ORG-1 domain-grouped registry (mechanism, HARMFUL)** | the released code's own `format_tools_for_prompt` (domain-grouped, constraints withheld) in place of the compact rendering, everything else the official protocol; 4,000 sealed official-population rows, paired | tool acc | 61.40 -> 58.17 (-3.23, CI90 -4.15 to -2.33; all eight tiers and all three domains negative); cross-domain twin misses 621 -> 521, same-domain 898 -> 1,118 | `SAEA-A2T-ORG1-DOMAIN-GROUPED-V1`, 2026-09-05; verdict `studies/speech-aware-evidence-acquisition/docs/readiness/2026-09-05-a2t-org1-domain-grouped-registry-v1-verdict.md`. Dropped: the domain cue stops cross-domain reaches but the misses become same-domain; distinguishability, not structure, is the missing knowledge |
| **ours: KC-A1 / KC-A1c, inline contrast notes on the lighting cluster with a token-matched form twin (mechanism, NULL)** | the union 4,000 official-population rows, official protocol, Q4_K_M raw audio; KC-A1 = eight registry-column notes appended inline (+44 text tokens, 152 lines unchanged), KC-A1c = category-only lines padded to the same tokens per line; both paired against the sealed official-protocol outputs, tier-stratified bootstrap CI90 | official tool accuracy (pooled) | **61.82** (KC-A1) and 61.65 (KC-A1c) vs the sealed baseline 61.40: total +0.42 (CI90 -0.12 to +0.97), form +0.25 (-0.30 to +0.80), content +0.17 (-0.38 to +0.70); the notes halve the cross-domain `-> setAmbientLighting` misses (88 -> 44) but the freed rows land on same-domain neighbours; 44 added tokens in the same shape cost nothing (ORG-1 lost 3 pp on structure) | `SAEA-A2T-KC-A1-CONTRAST-NOTES-V1`, `SAEA-A2T-KC-A1C-CATEGORY-ONLY-V1`, 2026-09-06; verdict `studies/speech-aware-evidence-acquisition/docs/readiness/2026-09-05-a2t-kc-a1-contrast-notes-v1-verdict.md`. Same-domain distinction is the open Audio2Tool problem; the evolution loop starts from the compact registry. |

**NOT ACCEPTED.** The row above is cell A0'-legacy-raw (legacy registry contract, raw audio through the bf16 mmproj), the closest of four calibration cells to the paper across all eight tiers (summed absolute gap 142.3 pp). **No cell passed the preregistered acceptance rule** (per-tier tool-accuracy |delta| <= 5 pp on tiers 1, 2, 5 and 6 with the tier rank order preserved); the tier-1 gap is 28.4 pp for this cell and 42.4 pp for the native-contract cells. All eight tiers, both other cells, the paired contrasts and the acceptance evaluation are in `studies/speech-aware-evidence-acquisition/docs/readiness/2026-09-04-a2t-direct-baseline-calibration-v1-verdict.md`. Two protocol factors were varied and neither closes the gap: the native OpenAI-format `tools` contract is significantly WORSE for tool accuracy (−5.75 pp raw, −8.75 pp packets), and the mmproj-free packet audio path is statistically null against raw audio. This row must not be used as an accepted baseline for mechanism work. **Update 2026-09-04 (official-protocol replication, still NOT ACCEPTED):** the second row mirrors the paper's released code and is the closest measurement to the paper this study has (summed absolute per-tier gap 77.3 pp against 116.3 pp for the reconstruction; the published protocol is worth +5.50 pp of pooled tool accuracy, paired CI90 +1.75 to +9.25). Seven tiers now sit between -12.6 and +3.4 pp of the paper row (tiers 3, 4, 6, 7, 8 with the paper value inside the Wilson CI90 at n=50); tier 1 sits at 60.0 against 92.4 and is the single unexplained gap. Remaining suspects, in the verdict's order: the roster (50 mixed-speaker rows per tier versus the release's first successful speaker of every query), Q4_K_M quantization (probe preregistered as `SAEA-A2T-Q8-QUANTIZATION-PROBE-V1`, not flown), and the whitespace variant of the system prompt. Verdict: `studies/speech-aware-evidence-acquisition/docs/readiness/2026-09-04-a2t-official-protocol-replication-v1-verdict.md`. Neither row is an accepted baseline for mechanism work. **Update 2026-09-04 (tier-1 official population, still NOT ACCEPTED):** the roster suspect is closed (worth +5.6 pp), the whitespace-variant suspect is null (+1.0 pp, 380 of 400 ties). Tier 1 is a smart_home gap: wearables and smart_car sit on the published 92.4, smart_home sits at 55.7, and 161 of its 163 misses name another real registry tool (82 the smart_car twin, e.g. rebootDevice -> restartDevice, setColor -> setAmbientLighting). Remaining suspects: Q4_K_M quantization (probe preregistered, not flown), a narrower internal tool taxonomy behind the paper's run, and the paper's internal 25-speaker cleaned tier-1 corpus (1,080 queries in the paper vs 2,146 public). Verdict: `studies/speech-aware-evidence-acquisition/docs/readiness/2026-09-04-a2t-tier1-official-population-v1-verdict.md`. No row is an accepted baseline for mechanism work.

## voiceagentbench (Family D)

| system | protocol | EN PF avg | Indic PF avg | source |
|---|---|---|---|---|
| Whisper + Llama3-70B (t backend) | VAB official | 60.64 | 39.21 | arXiv:2510.07978 |
| Whisper + Gemma3-27B | same as above | 59.28 | 35.28 | same as above |
| KimiAudio-7B direct answering | same as above | 57.57 | 28.21 | same as above |
| Qwen2.5-Omni-7B direct answering | same as above | 1.70 (format collapse) | 0.29 | same as above |
| one-shot gain `[abl]` | ablation in the same paper | +10–17pp (complex tasks) | — | same as above |
| **ours: zero-shot vs one-shot (R5=P2c)** | 150 EN complex questions, paired | — | — | to be filled in |

## full-duplex-bench-v3 (adjacent to Family D)

| system | Pass@1 | self-correction Pass@1 | source |
|---|---|---|---|
| GPT-Realtime | 0.600 | 0.588 | arXiv:2604.04847 |
| Cascade Whisper→GPT-4o→TTS | 0.450 | 0.176 (counter-example `[abl]`) | same as above |

## voicebench / voiceassistant-eval / uro-bench / big-bench-audio (Family F)

| system / condition | protocol | metric | value | source |
|---|---|---|---|---|
| VoiceBench #1 Nemotron-3-Nano-Omni (t) | VoiceBench full suite | overall | 89.39 | official leaderboard |
| VoiceBench cascade Whisper-v3+GPT-4o | same as above | overall | 87.80 (rank 4) | same as above |
| GPT-4o-Audio | same as above | overall | 86.75 | same as above |
| Qwen2-Audio | same as above | overall | 55.80 | same as above |
| URO-Bench EN-basic cascade Whisper+GPT-4o | URO-Bench | overall | 89.33 | Ruiqi-Yan/URO-Bench |
| URO-Bench EN-basic best open-source E2E GLM-4-Voice (t) | same as above | overall | 69.09 | same as above |
| VoiceAssistant-Eval GPT-4o-Audio | VAE, gpt-oss-20b judge | listening / speaking | 39.78 / 51.26 | arXiv:2509.22651 |
| VoiceAssistant-Eval Qwen2.5-Omni-7B | same as above | listening / speaking / viewing | 33.56 / 41.27 / 34.27 | same as above |
| BBA GPT-4o text upper bound | BBA, Claude judge | acc | 92 | HF blog 2024-12 |
| BBA GPT-4o-Realtime speech direct answering `[abl]` | same as above | acc | 66 | same as above |
| BBA Whisper→GPT-4o cascade `[abl]` | same as above | acc | ≈ the text level | same as above |
| BBA Gemini-2.5 Native-Audio-Thinking (t) | same as above | acc | 92 (2025-10) | Artificial Analysis |
| **ours: BBA direct vs self-cascade (R2=P2a)** | 200 paired questions, pinned scoring | acc | — | to be filled in |
| **ours: VoiceBench deterministic subset (A2)** | MCQ/rule subset sampling | per-subset | — | to be filled in |

## P0 number-backfill list (the bulk was completed 2026-08-07)

Already added: SLUE-SQA-5 frame-F1 (including the oracle upper bound); the two levels of SpeechDPR
values; the Spoken-SQuAD 2018 floor; the HeySQuAD relative gain; the AudioBench slue_p2_sqa5 row.
Remaining (low priority, to be handled before freezing): re-verifying UniverSLU 90.3 against the source
table; the AudioBench spoken_squad leaderboard row; HeySQuAD absolute EM/F1; (optional) the QMSum ROUGE
archival values. The counter-direction data point that was found is already in the table: in the
AudioBench closed-book document-QA setting, direct answering > cascade, which together with the FDB-v3
self-correction counter-example is evidence that "cascading is not superior everywhere".

## Backfill rules

1. Land the study-repo exposure-ledger row and receipt first, then edit this page;
2. An "ours" row must state: the ledger row id, the sample size, the split role, the protocol hash short
   prefix, and the scorer (deterministic / pinned judge and its hash);
3. A result under a protocol different from a published row **starts a new row** and must never overwrite
   the comparison row;
4. This page is updated in place row by row; history is preserved through git.
