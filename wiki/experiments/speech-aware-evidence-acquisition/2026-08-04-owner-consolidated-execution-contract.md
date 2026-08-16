---
title: "Owner consolidated execution contract: speech-aware evidence acquisition"
record_id: "SAEA-OWNER-CONSOLIDATED-EXECUTION-CONTRACT-2026-08-04"
date: "2026-08-04"
issued_by: "research owner (in-session directives, 2026-08-04)"
semantic_research_object: "speech-aware evidence acquisition"
source_candidate_provenance: "R2 (system-first-stage1c-v2; audit provenance only)"
authorization: "OWNER_GO_AND_EXECUTION_CONTRACT"
carrier_class: "Stage-2 study repository (Decision-Log-2026-08 continuation entry 91)"
paper_gate: "OWNER_GO_AND_PAPER_EXECUTION_CONTRACT"
entry_contract: "docs/superpowers/specs/2026-08-02-speech-aware-evidence-acquisition-stage2a-entry.md"
formal_opening: "wiki/audit/system-first-stage1c-v2/round-22/2026-08-02-audio-aware-evidence-acquisition-formal-opening-permission-note.md"
language_reissue: "2026-08-15 English re-issue under the program English-only first principle; terms unchanged"
---

# Owner consolidated execution contract: speech-aware evidence acquisition

This contract is the **single self-contained execution authority in force** for this study. It merges
the 2026-08-03 GO, the 2026-08-04 speech-only scope/identity contract, and the 2026-08-04 Stage-3
boundary contract into one independently readable specification in force; the three source contracts
are retained as historical/source records (§9) and their facts are never written back.

> **Language re-issue, 2026-08-15.** This record was re-issued in English under the program's
> English-only first principle. The terms, scope, budgets, bindings, and authority are unchanged
> from the 2026-08-04 acceptance; only the language of the text changed. The pre-translation bytes
> are Git blob `8ddd0cf2a96908befc8b49e69602185729ba17ba`, and
> `studies/registry.json:decision_record_blob` was re-pinned in the same commit.

## 1. Identity and authorization in force

The owner issued `OWNER_GO_AND_EXECUTION_CONTRACT` (2026-08-03), and the research object was
narrowed and renamed on 2026-08-04 to **speech-aware evidence acquisition**. This repository is the
**Stage-2 study carrier** (continuation entry 91).

- GitHub: `https://github.com/chaosxingxc-orion/speech-aware-evidence-acquisition.git`;
- local checkout: `studies/speech-aware-evidence-acquisition/`;
- Python distribution/package: `speech-aware-evidence-acquisition` /
  `speech_aware_evidence_acquisition`;
- experiment namespace: `SAEA-E-<nnn>`;
- experiment ledger: `wiki/experiments/speech-aware-evidence-acquisition/README.md`.

Candidate IDs such as R2 are audit provenance only and carry no engineering identity. The innovation
and the final method converge in Stage-2 into a qualified paper candidate, whose final validation
belongs to Stage-3 (§7).

## 2. Domain boundary: speech is not general audio

The research object covers **human speech and its linguistic content** only: ASR, entity
recognition/correction, contextual biasing, spoken QA, meeting speech understanding, and the
evidence use directly tied to speech understanding. Audio files such as WAV/MP3 are legitimate
carriers of the speech signal; general/environmental audio tasks — soundscape, event, music, animal
sound — are out of scope. Parameter training of the acoustic encoder, of an adapter, or of the core
model is forbidden by TF-Strict.

FSD50K, AudioSet, and ESC-50 must never enter this study's training, development, test, baseline,
ablation, or conclusion extrapolation; their already-downloaded bytes are recorded in
`docs/datasets.lock.json` as retained cross-domain assets, and retention does not mean adoption.

## 3. Research question and the four separated axes

Primary question: without modifying the parameters, structure, or training paradigm of the frozen
speech-capable omni core, and without introducing a second answering LLM, can an external
reward-guided control plane raise speech-domain task performance reliably by improving how speech
observation and external knowledge evidence are organized, supplied, and used — and reduce the
systematic risk of "misheard entity → retrieve related but wrong evidence → the error is reinforced"?

Four objects that must stay separated: `OBS` (speech observation and re-parsing), `ORG` (knowledge
organization/indexing/sourcing), `SUPPLY` (evidence selection, quantity, order, timing), and `USE`
(evidence admission, verification, iteration, stopping). Every experiment trace records the input,
action, result, version, and hash of each of the four axes separately; an experiment that changes all
four at once and reports only a total score cannot support a mechanism conclusion. External knowledge
services introduce three testable gaps — accessibility, currency/proper nouns, and verifiability —
and the report must also cover the correct-to-wrong regression, context contamination, and reward
hacking risk that related-but-wrong evidence brings.

## 4. Data and baseline binding

The single current source of dataset identity, on-disk state, revision, size, and checksum is
`docs/datasets.lock.json`; this contract freezes experiment roles only and never copies
drift-prone hashes.

| Tier | Lock key | Stage-2 role | Current obligation |
|---|---|---|---|
| Core | `earnings21-original`, `earnings22-original`, `conec` | primary carrier for entity-dense ASR / contextual correction, plus the dev/confirmatory and evidence layers | E0 must close identity, leakage, scoring, and trace |
| Diagnostic | `prism-public`, `rare5k-reconstruction`, `buzzword` | rare words, proper nouns, and contextual-biasing diagnostics | answers only its own diagnostic question and never substitutes for a core conclusion |
| Secondary speech | `slue-sqa-5`, `contextasr-bench`, `ami-meeting-corpus` | spoken QA, bilingual contextual ASR, meeting-speech transfer and stress testing | enabled in the pre-registered order once the core path holds |
| Optional speech | `ted-el-annotations`, `atco2-test-1h`, `eka-medical-asr-eval`, `librisqa-metadata` | entity annotation, domain speech, and low-cost adjacent validation | not a start gate; freeze the concrete hypothesis before use |
| Retained cross-domain | `fsd50k`, `audioset-metadata-features`, `esc-50` | no experiment role in this study | kept locally, never loaded, never cited as a supporting experiment |

Closest-prior reproduction takes ConEC / contextual ASR, RECOVER-style 1-best correction, Siskos
entity resolution, and same-boundary speech-biasing lines such as FlexCTC/TurboBias as candidates.
Before the first run of each baseline, freeze its runnable revision, visible fields, and failure
semantics; when it cannot be run, report `INCONCLUSIVE_BASELINE_NOT_READY` and never silently
substitute a weaker opponent.

## 5. Evaluation contract

- **Validity**: pre-registered WER/CER, entity-WER/recall/F1, QA EM/F1, or the carrier's native
  metric; wrong-to-correct / correct-to-wrong / unchanged state transitions; mean, variance, tail,
  and confidence interval split by speaker/domain/entity-frequency/noise condition; retrieval
  recall/precision, evidence coverage, and citation correctness.
- **Soundness**: a pre-registered minimal `OBS × ORG × SUPPLY × USE` factorial control, changing one
  attributable axis at a time; bare core, fixed legitimate context, random/mismatched evidence,
  oracle evidence (as an upper bound only), and a no-use negative control; gold, reference, test, and
  future-turn material never crosses the runtime boundary; evidence being supplied and evidence being
  used are judged separately; discovery and confirmatory stay isolated, with thresholds and selection
  rules frozen before any confirmatory result is read.
- **Efficiency**: report absolute cost and unit gain together — frozen-core and tool call counts,
  tokens, end-to-end latency, GPU/CPU-hours, peak VRAM, speech seconds processed, evidence supplied
  versus adopted, incremental cost per metric point, and the Pareto frontier. Reporting only "how
  many percent was saved" is forbidden.

## 6. Frozen fields, budget, and execution sequence

| Field | Current frozen value |
|---|---|
| Core/runtime | `qwen3-omni-30b-a3b-instruct-gguf`; the llama.cpp build commit and the per-file GGUF SHA-256 land in a runtime receipt before the first model call |
| Information boundary | gold, reference, test annotation, and future turns never enter runtime; each arm's visible fields and its prompt/config hash are recorded |
| Resources | first slice ≤3,000 frozen-core calls, ≤40 GPU-hours, ≤20 hours of speech audio, paid API = 0; any non-zero spend needs a dated amendment |
| Exposure | the study repo's `docs/exposure-ledger.md` is written before any result is read; a declaration carries scope/date/counts/inherited; a formal ledger row must carry the split role, the split identity hash, and the consumed mark |
| Sequence | E0 (D1–D4) → R0 vertical chain → R1 closest-prior reproduction → X bounded directed exploration |
| Execution scope | this repository accepts only the `model-free-check` / `baseline-reproduction` / `bounded-discovery-probe` execution profiles; `paper-scale-confirmatory` always fails closed (§7) |
| Stop line | leakage, scorer inconsistency, sample identity drift, licence expiry, unregistered exposure, or an unaddressed stronger runnable prior at the same boundary |

No model may be touched before E0 and the runtime receipt close. The weekly literature delta updates
only the prior/threat queue; unless new evidence overturns the research question, the legality of the
data, the information boundary, or the reproducibility contract, an unbounded Stage-1 rescan must not
be reopened to block engineering.

## 7. Study endpoint and the Stage-3 stop line (continuation entry 91)

This study's Stage-2 endpoint is one or more falsifiable, reproducible **qualified paper candidates**
(improvement claim and null hypothesis, mechanism, baseline receipts, experimental and statistical
design, and an unread-confirmatory declaration) — not finished final paper experiments. The following
actions are forbidden by default and require promotion through
`OWNER_GO_AND_PAPER_EXECUTION_CONTRACT` into a standalone `papers/<slug>` repository first:

- production-scale method implementation and large-scale confirmatory campaigns;
- final superiority or generalization conclusions; a bounded probe result must never be written up as
  a paper-level claim;
- manuscript, submission, or publication release.

A null or negative result is a legitimate completed form of this study; candidates must not share
unregistered test exposure; and paper GO for one candidate does not authorize any other candidate of
this study. Until the program-level confirmatory reservation ledger exists (trigger: continuation
entry 92), every confirmatory sample must have its split identity hash registered in the experiment
ledger and the exposure ledger and be marked consumed before it is read; inherited exposure across
studies and papers is monotonically non-decreasing.

## 8. Data retention and deletion rules

This contract deletes no verified data under `SPEECHRL_DATA_DIR`; "it did not enter the current
study" is not a reason to delete. Deletion requires a separate owner instruction, an exact target, a
recoverability statement, and a lock amendment.

## 9. Source records (historical, never written back)

| Record | Path | Git blob |
|---|---|---|
| 2026-08-03 GO contract (source of budget and authorization) | `2026-08-03-owner-go-and-execution-contract.md` | `e059b6257fad4be45f3014297a26c4a40257b9af` |
| 2026-08-04 speech-only scope/identity contract | `2026-08-04-owner-speech-domain-scope-and-identity-contract.md` | `57bf8e23f7282162d06936b5ea484ea6fb5bdea8` |
| 2026-08-04 Stage-3 boundary / paper-gate contract | `2026-08-04-owner-stage3-boundary-and-paper-gate-contract.md` | `5f91226f25d6bfd5c5cd427c57fecc635eb43066` |

This contract supersedes the "in force" status of those three contracts (their issuance facts,
historical exposure, budget, and authorization facts are all inherited and never written back).
Invalidation condition: the owner changes the study scope, identity, budget, carrier binding, or
paper gate.

## Owner acceptance

Accepted by owner on 2026-08-04 (session direction; recorded in Decision-Log-2026-08 continuation
entries 91/92). Re-issued in English on 2026-08-15 by owner direction, with terms unchanged.
