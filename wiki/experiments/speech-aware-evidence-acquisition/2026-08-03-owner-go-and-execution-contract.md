---
title: "Owner GO and execution contract: audio-aware evidence acquisition"
record_id: "AAEA-OWNER-GO-EXECUTION-CONTRACT-2026-08-03"
date: "2026-08-03"
status: "HISTORICAL_ISSUANCE__EFFECTIVE_IDENTITY_AND_SCOPE_SUPERSEDED_2026-08-04"
issued_by: "research owner (in-session dated directive, 2026-08-03)"
semantic_research_object: "audio-aware evidence acquisition"
source_candidate_provenance: "R2 (system-first-stage1c-v2)"
authorization: "OWNER_GO_AND_EXECUTION_CONTRACT"
entry_contract: "docs/superpowers/specs/2026-08-02-audio-aware-evidence-acquisition-stage2a-entry.md"
formal_opening: "wiki/audit/system-first-stage1c-v2/round-22/2026-08-02-audio-aware-evidence-acquisition-formal-opening-permission-note.md"
default_values_policy: "ADOPTED_AS_PROPOSED_DEFAULT__AMENDABLE_BY_DATED_AMENDMENT"
---

# Owner GO and execution contract — audio-aware evidence acquisition

> Historical issuance: this record evidences the 2026-08-03 owner GO and the original budget
> authorization. The current research name, the speech-only domain boundary, the remote/local
> paths, the package name, and the experiment namespace have been superseded self-containedly by
> `2026-08-04-owner-speech-domain-scope-and-identity-contract.md`; the old names and paths below are
> retained as facts of that date and must never be used as current routing.

## Decision

On 2026-08-03 the owner issued `OWNER_GO_AND_EXECUTION_CONTRACT`: the semantic research object
**audio-aware evidence acquisition** is approved to enter engineering, a standalone repository
`https://github.com/chaosxingxc-orion/audio-aware-evidence-acquisition.git` (private) is created and
checked out to `studies/audio-aware-evidence-acquisition/`, and execution follows the E0→R0→R1→X
sequence of the Stage-2A entry contract. Issued in the same batch: the data-acquisition line is
adjusted per the directory-reorganization resolution (receipt paths made semantic, the canonical
lock consolidated).

At issuance the owner did not specify the frozen values field by field; the values marked `DEFAULT`
in the table below take effect at the value the Fable5 adjudication recommended, and the owner may
change any row at any time by a dated amendment. This contract adjudicates no question of novelty;
innovation and the final method remain outputs of Stage-2A/2B.

## Frozen fields (freeze sheet)

| Field | Frozen value | Source |
|---|---|---|
| Repository | `https://github.com/chaosxingxc-orion/audio-aware-evidence-acquisition.git`, default branch `master`, local `studies/audio-aware-evidence-acquisition/` | owner GO |
| Core/runtime | lock key `qwen3-omni-30b-a3b-instruct-gguf` (Q8_0 GGUF + bf16 mmproj, 2 files, 34,691,959,904 B), llama.cpp llama-server resident at `-ngl 28`; **before the first model call an E0 runtime receipt must land: llama.cpp build commit + per-file sha256** (fail-closed) | DEFAULT |
| Carriers | lock keys `earnings21-original`, `earnings22-original` (rev `c05ab6fd8b4b627d123c922a22a39e993dd37635`), `conec` (rev `88440713d8b80dc4f19b225f6480237e78c379de`); D0 receipt `docs/checks/audio-aware-evidence-acquisition/2026-08-02-acquisition/`; the discovery/confirmatory dual split follows the v20 carrier-family contract, derivation seed `20260803`, the derivation script enters study-repo version control, and confirmatory is not read until the minimal confirmation path is triggered | DEFAULT |
| Information boundary | the immutable boundary of the entry contract: gold labels / reference transcripts / test annotations / future turns never cross the runtime boundary; each arm's visible fields are declared explicitly in the R0 config and hashed | entry contract |
| Baselines | the mandatory reduced set is frozen as {the ConEC context line (first reproduction target), the RECOVER 1-Best ladder (mandatory control arm), the Siskos entity-resolution line, the FlexCTC/TurboBias NeMo biasing group}; Corona 2017 / Raghuvanshi 2019 / Flemotomos 2024 / COALA 2026 are assessed as threat/reproduction candidates at step zero of R1; **the exact runnable revision is frozen by a dated amendment before the first reproduction run**; on failure report `INCONCLUSIVE_BASELINE_NOT_READY` and never silently substitute a weaker opponent | DEFAULT |
| Prompts/tools | the prompt hash and the frozen retriever/judge revision enter the trace on every run; source, date, and query are logged; final answer authority rests with the frozen core | entry contract |
| Metrics | per v20: task/entity metrics, correct-to-wrong and wrong-to-correct transitions, tail and cost reporting; the scoring stack is frozen at E0 D3 | entry contract |
| Resources | R0 first-slice ceilings: ≤3,000 frozen-core calls, ≤40 local GPU-hours (RTX 5090), ≤20 h of processed audio, paid API spend = 0 (any non-zero requires an amendment); the end-of-slice go/narrow/repair/stop memo is the stop-go checkpoint | DEFAULT |
| Exposure | one row per contact in the study repo's `docs/exposure-ledger.md` (registered before results are read); the exposure declaration carries four fields (scope/date/counts/inherited); inherited exposure: as of this date the three carriers have zero model contact (only the D0 model-free acquisition verification) | DEFAULT |
| Wiki | experiment ID namespace `AAEA-E-<nnn>` (carrying no candidate number); ledger `wiki/experiments/audio-aware-evidence-acquisition/README.md`; protocol/config hashes, MLflow/artifact routing, and the deviation process follow `wiki/Experiment-Assets.md` | owner GO |

## Scope of authorization, and what stays withheld

This contract authorizes: creating and pushing the study repository, E0 (the D1–D4 model-free data
closure), the R0 engineering vertical chain, R1 readiness-qualified closest-prior reproduction, and
X directional exploration — each step bound by the budget in the table above and by fail-closed
receipts.

Still not authorized: paid API spend, publishing a wiki mirror, a public release,
novelty/superiority conclusions, and any contact outside the budget band. Candidate numbers such as
R2 must never enter package names, the MLflow main namespace, or formal experiment IDs.

## Invalidation and rollback

Invalidation condition: the owner withdraws or revises this contract; or a STOP_THE_LINE trigger
fires (a stronger runnable mandatory prior on the same task and the same boundary; a carrier
licence/availability/label/metric contract lapsing; unregistered inherited exposure or a leak; the
researchability of the problem being overturned). Rollback: the study repository is archived
(registry lifecycle moves to `paused`/`sunset`); the umbrella governance layer and W1–W4 are
unaffected.

## Amendment 1 (2026-08-03) — rollback semantics clarified after the W1–W4 retirement

Registered under the post-reorganization architecture review proposal
(`PROGRAM-DIRECTORY-POST-MIGRATION-REVIEW-V1`); it is a clarifying amendment, creates no new
authorization, and does not rewrite the original text in place.

The preceding section's phrase "the umbrella governance layer and W1–W4 are unaffected" was issued
before that same day's W1–W4 retirement ruling. Clarification: the four W1–W4 work repositories were
retired on 2026-08-03 — the local checkouts were deleted and the remotes are kept as cold backups
outside the program (`wiki/archive/program/w1-w4-retirement/`). This contract's rollback therefore
affects only the study repository's lifecycle state and the umbrella registry/governance layer; a
rollback restores no W1–W4 local worktree, and changes nothing about the state of the retired cold
backups.

---

**Language conversion (2026-08-25).** Re-issued in English with terms, scope, budget, dates, and
authority unchanged; content is preserved throughout — this is a language conversion, not an edit.
Amendment 1's undertaking not to "rewrite the original text in place" is undisturbed: the
pre-conversion characters remain the authoritative original and stay addressable as Git blob
`e059b6257fad4be45f3014297a26c4a40257b9af`. The conversion is recorded in
`wiki/Decision-Log-2026-08.md` continuation entry 95.
