---
title: "Research Objective & Current State"
role: "HOT single current-state entry; supersede in place"
last_refresh: "2026-07-22 — Stage-1B v4 P0 repair frozen; narrow transition rereview pending"
---

# Research Objective & Current State

> Default reading order: client guide → this page → `wiki/Project-Thesis.md`. Load audit history only through a targeted campaign index.

## Current gate and authority

The project is in **late Stage-1B closeout**. The fixed Stage-1B v4 scientific release is commit
`f11a2b1fd0b6d81b08caefc5d576fe13ed579883`. Its 60-artifact manifest replays 60/60: 52 Git blobs and eight external hash-bound artifacts, with zero missing or mismatched entries.

Formal Stage-1C problem comparison still requires an independent reviewer signature. Model/API use,
dataset metrics, smoke tests, reproduction, prototypes, problem ranking, owner selection and technical
implementation remain unauthorized. Stage-1B maps method paths, proximity, contradictions,
instruments and feasibility; it does not decide novelty. Technical-approach innovation remains deferred
to reproduction-first Stage-2A and validation in Stage-2B.

## Research north star

Develop an external, reward-guided control plane for frozen speech/omni foundation models. The control
plane may manage candidates, tools, evaluators, selection, routing, budgets, stopping and repair without
changing core model weights.

## Current evidence

- Frozen D0 remains exhausted at 20,727/20,727 abstracts, 319 D2 full texts and 226 retained works.
  This is closure of the declared frozen surface, not closure of the literature universe.
- The 81-work speech/omni coverage ledger has 70 `FULLTEXT_ROUTED` rows and 11
  `ABSTRACT_ROUTED` rows. All 70 full-text rows now resolve to a successful ledger entry, local bytes
  and matching SHA-256; the seven false full-text labels identified by review were repaired by exact-ID
  PDF/e-print acquisition.
- The known-prior reconciliation routes nine pre-existing works to canonical work IDs. Every decision
  is `REUSE_CANONICAL_WORK_ID`; no duplicate claim work or new duplicate seed was created.
- The strict speech/omni supplement now has 39 rows: 25 direct methods, 13 measurement instruments and
  one boundary. The direct control basis separates nine external-orchestration, nine state/event-gated
  and seven evaluator/verifier-gated systems; **zero are coded as reward-guided selection**.
- Stage-1C inputs remain unranked. Budget/stop/repair, evaluator reliability and
  interactive/full-duplex are `ELIGIBLE_NON_H5`. Evidence-state and tool/agent arbitration remain
  `INELIGIBLE_FOR_STAGE_1C_SELECTION` while H5 is withheld.
- Asset facts are layered: 31/31 frozen baseline entries are present; exact candidate assets are kept
  outside Git under `SPEECHRL_DATA_DIR`; public VoiceAgentBench, Full-Duplex-Bench v3, Audio2Tool,
  Omni-DeepSearch and IHBench assets are locally pinned. Exact tau-Voice data, LALM recordings,
  EchoChain code/data and the generated From Text to Voice corpus remain honestly unavailable or
  unverified.
- This repair ran no research model, API evaluation, dataset metric, reproduction or prototype.

## Current route

- Survey router: `wiki/survey/current/README.md`
- Short gate: `wiki/survey/current/status.md`
- Stage-1B map: `wiki/survey/current/tables/stage1b-mapping-release.md`
- Unranked Stage-1C inputs: `wiki/survey/current/tables/stage1c-eligible-inputs.md`
- v4 release and replay: `docs/checks/stage1b-closeout/2026-07-22-v4/`
- Reviewer transaction index: `wiki/audit/system-first-stage1b/INDEX.md`
- Long-lived records: `wiki/survey/registry/README.md`

## Next action

Request one narrow independent rereview of commit `f11a2b1fd0b6d81b08caefc5d576fe13ed579883`.
The reviewer should decide whether P0-R1 through P0-R4 are repaired and whether Stage-1C may begin
common-rubric comparison only. Do not reopen broad D0, create duplicate claim seeds, discuss technical
novelty, or begin experimental execution while this signature is pending.

## Supersession rule

If release identity, evidence depth, asset identity, exposure, H5 status, reviewer verdict or owner
authority changes, supersede this page in place. Keep old proposals, responses and reviews in cold
audit; do not stack amendments into HOT/CURRENT context.
