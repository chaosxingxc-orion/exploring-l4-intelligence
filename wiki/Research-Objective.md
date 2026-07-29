---
title: "Research Objective & Current State"
role: "HOT single current-state entry; supersede in place"
last_refresh: "2026-07-29 — R1 sunset owner-confirmed; R2–R9 marked owner-unverified; direction criterion recorded"
---

# Research Objective & Current State

> Default reading order: client guide → this page → `wiki/Project-Thesis.md`. Load campaign detail only through the CURRENT router.

## Current gate and authority

Stage‑1C is in owner-directed remediation. Endpoint:
`STAGE1C_R1_SUNSET_OWNER_CONFIRMED_20260729_R2R9_UNVERIFIED_OWNER_COWORK_PENDING`.

The five dimensions and original R1–R9 remain an audit frame, not nine guaranteed Stage‑2 projects.
R1 sunset is owner-confirmed (2026-07-29, Decision-Log 续76): it lacked standalone direction potential.
R2–R9 are executor drafts the owner has not verified (`OWNER_UNVERIFIED`).
Owner direction criterion (2026-07-29): sufficient survey plus in-domain prior work as a methodological
baseline, or cross-domain-informed design where the field is empty; both must compare against incumbent
SOTA on a concrete task. Core = Qwen3-Omni-30B via local llama.cpp; ASR mainline = general ASR.
This stage only analyzes/summarizes. Model/API execution, acquisition, metric runs, reproduction,
prototypes, novelty verdicts, Stage‑2A, push and wiki publication remain withheld.

## Final research object

For an API-only frozen speech/omni core, build an external reward-guided control plane that uses
system-level in-context control to construct, select and update knowledge, memory, skills and evidence
state, so that task capability improves reliably across runs and conditions without changing model
parameters or internals.

The original candidates are R1 context methods; R2 external retrieval; R3 memory; R4 skills; R5 evidence-state
architecture; R6 within-instance control; R7 cross-instance evolution; R8 reliable control; R9 integration.
Candidate numbering is preserved for provenance even when a direction sunsets.

The prior `C1_DECISION_CALIBRATED_REWARD` primary selection is superseded; evaluator, headroom,
stop/repair/abstain and reward-hacking tests are shared measurement components, and fixed-pool headroom
gates no new system-created contexts.

R1 = `NO_GO_AS_STANDALONE_DIRECTION__SUNSET_BEFORE_STAGE2`; its literature/baseline matrix remains
reusable. R2 is a type-(a) candidate (AudioRAG, Omni-DeepSearch, VoiceAgentRAG are in-domain prior
work); its withdrawn merge recommendation is an executor draft opinion awaiting owner co-review.

## Formal and evidence boundary

Lean is used to audit explicit assumptions and operator-level implications, not to prove empirical
effectiveness. The old finite-pool read-out bound cannot be generalized to an all-contexts ICL limit.
The runtime-reliability lemma shows only that a `2ε` estimated margin implies true non-regression under a
uniform reward-error bound `ε`, which still needs empirical calibration. Implementation-to-theorem
conformance remains open.

Stage‑1B v5 `38fb9435d0c35e226ad62b16015a6dbee054e6c2` and its 320-work union remain fixed. The portfolio adds
35 speech/omni fulltexts, 73 cross-domain donors and T1/T2/T3; R1 separately registers six hash-bound ICL/
example-selection neighbors. Donor effects do not cross modality boundaries.

## Stage-2A next action

The first vertical slice is R5 + R6 + R8: an incumbent-preserving evidence-state controller over one
frozen API core, with actions `keep / branch-context / acquire / repair / stop`, black-box runtime signals,
equal-cost baselines and robust task-utility reporting. MMAU-mini/MMAR are the proposed carriers, but their
CURRENT local-status discrepancy must be resolved before any run.

Next action: owner co-review of R2–R9 under the 2026-07-29 criterion. The R5+R6+R8 contract binding and
the `AUTHORIZE_STAGE2A_CAPABILITY_CONTROL_VERTICAL_SLICE` request stay frozen until it completes. R1 has
no Stage‑2B slot; the Stage‑2D question stays open pending the R2 co-review.

## Legacy and routing

R1 agreement remains `FAIL`. R2R1 passed 22 focused implementation tests but was never distributed or
independently accepted and remains `RETIRED_WITHOUT_DISTRIBUTION_OR_INDEPENDENT_ACCEPTANCE`; no calibration
claim follows. H5 remains `WITHHOLD_NON_LOAD_BEARING`, so cross-modality effectiveness conclusions remain
prohibited. Specialized Duplex-model development remains outside the primary branch.

Current router: `wiki/survey/current/README.md`; effective direction contract:
`wiki/survey/current/research-directions.md`; portfolio evidence:
`wiki/survey/workbench/stage1c-portfolio/`; prior calibration audit:
`wiki/audit/system-first-stage1c-v2-calibration/INDEX.md`.

## Supersession rule

Supersede this HOT page in place when Stage‑2A authority, the five-dimension scope, API-only boundary,
reliability objective, formal assumptions or direction priority changes. Preserve transactions in cold audit.
