---
title: "Owner effective contract: speech-aware evidence acquisition"
record_id: "SAEA-OWNER-SPEECH-SCOPE-AND-IDENTITY-2026-08-04"
date: "2026-08-04"
issued_by: "research owner (in-session directives, 2026-08-04)"
semantic_research_object: "speech-aware evidence acquisition"
source_candidate_provenance: "R2 (system-first-stage1c-v2; audit provenance only)"
authorization: "OWNER_GO_AND_EXECUTION_CONTRACT"
entry_contract: "docs/superpowers/specs/2026-08-02-speech-aware-evidence-acquisition-stage2a-entry.md"
formal_opening: "wiki/audit/system-first-stage1c-v2/round-22/2026-08-02-audio-aware-evidence-acquisition-formal-opening-permission-note.md"
supersedes_effective_scope_of: "wiki/experiments/speech-aware-evidence-acquisition/2026-08-03-owner-go-and-execution-contract.md"
---

# Owner effective contract — speech-aware evidence acquisition

## 1. Effective decision

On 2026-08-04 the owner narrowed and renamed the research object that had already received GO, from
**audio-aware evidence acquisition** to **speech-aware evidence acquisition**. Stage-1C's R2 number
and the filename of the original formal-opening permission are retained for audit provenance only
and no longer carry engineering identity.

This contract is the current self-contained execution authority:

- GitHub: `https://github.com/chaosxingxc-orion/speech-aware-evidence-acquisition.git`;
- local checkout: `studies/speech-aware-evidence-acquisition/`;
- Python distribution/package: `speech-aware-evidence-acquisition` /
  `speech_aware_evidence_acquisition`;
- experiment namespace: `SAEA-E-<nnn>`;
- experiment ledger: `wiki/experiments/speech-aware-evidence-acquisition/README.md`.

The original 2026-08-03 contract remains the historical evidence of the owner GO, the budget, and
the authorization source as of that date; this contract inherits its GO and supersedes its old
research name, old paths, old remote, old namespace, and its over-broad audio-domain wording. It
does not write back to the formal-opening audit record, and it does not change the original ruling
that "innovation and the final method converge in Stage-2A/2B".

## 2. Domain boundary: speech is not general audio

The input this research handles may still be carried by audio files such as WAV/MP3, but the object
of study is confined to **human speech and its linguistic content**: ASR, entity
recognition/correction, contextual biasing, spoken QA, meeting speech, and the evidence use directly
related to speech understanding.

The following concepts must be kept apart:

| Concept | Meaning in this research | In scope |
|---|---|---|
| speech signal | the acoustic signal of human speech, carrying words, entities, speaker turns, and semantic content | Yes |
| speech task | ASR, spoken QA, meeting speech understanding, speech entity and context correction | Yes |
| general/environmental audio | recognition of, or question answering over, soundscapes, events, music, animal sounds, and non-linguistic sound sources | No |
| audio-model training | parameter training of an acoustic encoder, an adapter, or the core model | No; forbidden by TF-Strict |

Therefore FSD50K, AudioSet, and ESC-50 must never enter this study's training, development, testing,
baselines, ablations, or the extrapolation of its conclusions. The bytes already downloaded are not
deleted: `docs/datasets.lock.json` continues to record them as locally complete, cross-domain
retained assets, and if some future general-audio study passes its own owner GO those bytes may be
reused. Retention is not adoption by this research.

## 3. Research question and falsifiable structure

### 3.1 Main question

Under the condition that the parameters, internal structure, and training paradigm of the frozen
speech-capable omni core are not modified, and that no second answering LLM is introduced: can an
external reward-guided control plane reliably raise speech-domain task performance by improving the
organization, supply, and use of **speech observation** and **external knowledge evidence**, and
lower the systematic risk of "mishear an entity → retrieve related but wrong evidence → the error is
reinforced"?

### 3.2 The four objects that must be kept separate

| Axis | What is changed | Typical actions | Interpretation that must never be mixed in |
|---|---|---|---|
| OBS: speech observation | candidate transcripts, entity spans, time boundaries, or re-parsed results obtained from the same speech signal | re-decoding, candidate generation, re-listening to an entity segment | a gold transcript must never be treated as a runtime observation |
| ORG: form of knowledge organization | how external knowledge is segmented, indexed, linked, and annotated with source and confidence | passage/entity/graph, hierarchical granularity, time or speaker binding | "more text retrieved" must never be equated with better organization |
| SUPPLY: form of knowledge supply | which evidence enters the frozen core, in what quantity, in what order, in which context template, and at what moment | top-k, source selection, ordering, citation envelope | the model finally adopting evidence must never be equated with that evidence having been supplied |
| USE: form of knowledge use | how the controller admits, rejects, verifies, iterates, stops, and applies evidence to the final answer | accept/reject/re-query/abstain, reward-guided next action | a single rerank must never pass itself off as complete sequential control |

Every experiment trace must record the inputs, actions, results, versions, and hashes of `OBS`,
`ORG`, `SUPPLY`, and `USE` separately. Any experiment that changes all four axes at once yet reports
only a single aggregate score is insufficient to support a mechanism conclusion.

### 3.3 Why knowledge is introduced under black-box conditions

External knowledge is introduced neither because the frozen core "has no knowledge at all", nor in
order to replace the core model with a retriever. It serves three checkable gaps:

1. **Accessibility gap**: the model may have seen the relevant knowledge in pre-training, but the
   current speech observation and context fail to activate it reliably;
2. **Recency / proper-noun gap**: company names, person names, product names, and current-period
   meeting material may be absent from parametric memory, or may have no reliable speech-to-entity
   mapping;
3. **Verifiability gap**: external evidence supplies source, time, and citation boundaries, letting
   the system tell "the model guessed" apart from "this is evidence-supported".

It also introduces explicit risks: a wrong observation induces related but wrong retrieval, an
excess of evidence pollutes the context, and the controller may chase a proxy reward. So "the score
improved after knowledge was added" is not a sufficient conclusion; one must simultaneously show
that the evidence was relevant, that the information boundary was legal, and that the improvement
came from a pre-registered path — and report the correct-to-wrong regressions.

## 4. Data and baseline binding

The single current source of truth for data identity, on-disk state, revision, size, and checksum is
`docs/datasets.lock.json`; this contract freezes experimental roles only and never copies
drift-prone hashes.

| Tier | lock key | Stage-2 role | Current obligation |
|---|---|---|---|
| Core | `earnings21-original`, `earnings22-original`, `conec` | the primary carriers for entity-dense ASR / context correction, the dev/confirmatory splits, and the evidence layer | E0 must close identity, leakage, scoring, and trace |
| Diagnostic | `prism-public`, `rare5k-reconstruction`, `buzzword` | rare-word, proper-noun, and contextual-biasing diagnostics | answers only its own diagnostic question; never substitutes for a core conclusion |
| Secondary speech | `slue-sqa-5`, `contextasr-bench`, `ami-meeting-corpus` | spoken QA, bilingual contextual ASR, meeting-speech transfer / stress testing | enabled in pre-registered order once the core path holds |
| Optional speech | `ted-el-annotations`, `atco2-test-1h`, `eka-medical-asr-eval`, `librisqa-metadata` | entity annotation, domain speech, and low-cost adjacent validation | not a start-work gate; freeze the specific hypothesis before use |
| Retained cross-domain | `fsd50k`, `audioset-metadata-features`, `esc-50` | no experimental role in this study | retained locally; never loaded, never cited as a supporting experiment |

Closest-prior reproduction still takes its candidates from ConEC / contextual ASR, RECOVER-style
1-best correction, Siskos entity resolution, and same-boundary speech biasing lines such as
FlexCTC/TurboBias. Before its first run every baseline must freeze its runnable revision, its
visible fields, and its failure semantics; when it cannot be run, report
`INCONCLUSIVE_BASELINE_NOT_READY` and never silently substitute a weaker opponent.

## 5. Evaluation contract

### 5.1 Effectiveness: does it improve the task result

- task metrics: pre-registered WER/CER, entity-WER / entity recall / F1, QA EM/F1, or the carrier's
  native metric;
- state transitions: wrong-to-correct, correct-to-wrong, unchanged-wrong, unchanged-correct;
- stability: report mean, variance, tail, and confidence interval broken down by speaker / domain /
  entity frequency / noise condition;
- evidence metrics: retrieval recall/precision, evidence coverage, citation correctness, and the
  support rate of the final answer.

### 5.2 Reasonableness: why it improved, and whether improving that way is permitted

- pre-register the minimal factorial control over `OBS × ORG × SUPPLY × USE`, changing only one
  attributable axis at a time;
- bare core, fixed legal context, random/mismatched evidence, oracle evidence (as an upper bound
  only), and a no-use negative control;
- gold / reference / test / future-turn must never cross the runtime boundary; every source, query,
  time, and version stays traceable;
- evidence-supplied and evidence-used are judged separately, and the regressions caused by related
  but wrong evidence are reported;
- discovery/confirmatory isolation; thresholds, stopping conditions, and selection rules are frozen
  before any confirmatory result is read.

### 5.3 Efficiency: what was paid for the improvement

Report absolute cost and unit benefit together; reporting only "how many percent was saved" is
forbidden:

- frozen-core call count, tool/retrieval call count, input/output tokens;
- end-to-end latency, GPU-hours, CPU-hours, peak VRAM, speech-audio seconds processed;
- number of retrieval candidates, number/bytes of evidence actually supplied, number of evidence
  items the model actually adopted;
- the incremental cost per absolute point of WER/entity-WER, or per point of QA score;
- the Pareto frontier: task utility, correct-to-wrong risk, latency, and call cost.

## 6. Frozen fields and execution sequence

| Field | Current frozen value |
|---|---|
| Core/runtime | `qwen3-omni-30b-a3b-instruct-gguf`; the llama.cpp build commit and the per-file GGUF SHA-256 land in a runtime receipt before the first model call |
| Information boundary | gold / reference / test annotation / future turn never enter the runtime; each arm's visible fields and its prompt/config hash are booked |
| Resources | first slice ≤3,000 frozen-core calls, ≤40 GPU-hours, ≤20 hours of speech audio, paid API = 0; non-zero spend requires a dated amendment |
| Exposure | `docs/exposure-ledger.md` is registered before results are read; the declaration contains scope/date/counts/inherited |
| Sequence | E0 (D1–D4) → the R0 vertical chain → R1 closest-prior reproduction → X directional exploration |
| Stop line | a leak, scorer inconsistency, sample-identity drift, a lapsed licence, unregistered exposure, or an unaddressed stronger runnable prior on the same boundary |

No model may be contacted before E0 and the runtime receipt are closed. The weekly literature delta
updates only the prior/threat queue; unless new evidence overturns the research question, the
legality of the data, the information boundary, or the reproducibility contract, an unbounded
Stage-1 sweep must never be reopened to block engineering.

## 7. Data retention and deletion rules

This identity migration deletes no verified data under `SPEECHRL_DATA_DIR`. Nor, in future, may a
complete asset be deleted merely because "it did not enter the current study"; deletion requires a
separate owner instruction, an exact target, a recoverability statement, and a lock amendment. Only
the experimental binding changes here: speech-domain data enters the verifiable list, and
general-audio data enters the cross-domain retention list.

---

**Language conversion (2026-08-25).** Re-issued in English with terms, scope, budget, dates, and
authority unchanged; content is preserved throughout — this is a language conversion, not an edit.
Pre-conversion bytes are Git blob `57bf8e23f7282162d06936b5ea484ea6fb5bdea8`; the conversion is
recorded in `wiki/Decision-Log-2026-08.md` continuation entry 95.
