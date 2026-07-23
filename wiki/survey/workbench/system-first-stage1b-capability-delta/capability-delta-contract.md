---
artifact_id: "SF-STAGE1B-CAPABILITY-DELTA-CONTRACT-V1"
date: "2026-07-23"
status: "RELEASE_CANDIDATE_AWAITING_INDEPENDENT_REVIEW"
authorization: "AUTHORIZE_STAGE1B_CAPABILITY_DELTA_MAPPING"
requested_review_verdict: "SIGN_STAGE1B_CAPABILITY_DELTA_RELEASE"
frozen_stage1b_v5_release: "38fb9435d0c35e226ad62b16015a6dbee054e6c2"
---

# Capability-delta contract

## 1. Authority and non-authority

The owner token authorizes a bounded Stage-1B mapping transaction: exact identity and version lock,
full-text and asset locators, one-hop citation promotion, D0-D4 method paths, proximity, boundary,
falsifier and paper-reported experimental-setting extraction, plus deterministic checks and an
independent-review package.

It does not authorize:

- mutation or reinterpretation of the frozen Stage-1B v5 release;
- a project novelty, effectiveness or priority verdict;
- research-model/API calls, dataset metrics, reproduction, prototype or Stage-2A execution;
- Stage-1C family scale-out, branch formation, selection or ranking;
- self-signing `SIGN_STAGE1B_CAPABILITY_DELTA_RELEASE`.

## 2. Capability ontology

The primary research directions are causal intervention directions, not topical folders:

| ID | Primary intervention | Question |
|---|---|---|
| `D0_SYSTEM_HARNESS` | system topology, roles, tools or interaction loop | Does the carrier system improve the task without adding a K/S/M asset? |
| `D1_MULTIMODAL_KNOWLEDGE` | declarative facts, relations or grounded evidence | Does external or activated evidence improve the decision, and is non-text evidence necessary? |
| `D2_MULTIMODAL_SKILL` | reusable procedures with applicability and execution contracts | Does a state-conditioned procedure improve held-out execution rather than merely add context? |
| `D3_MULTIMODAL_MEMORY` | cross-step/session retention, retrieval, update, conflict and forgetting | Does persistence preserve decision-relevant evidence across time without staleness or noise? |
| `D4_TF_RL_ORCHESTRATION` | reward/value/advantage changes the next external action without core-weight updates | Does feedback improve selection, stopping, repair or K/S/M routing over static policies? |

K/S/M are not symmetric ontological types. Knowledge and skill are storable content; memory is a
persistence and update capability. Every record therefore separately codes:

- `asset_content_type`;
- `persistence_scope`;
- `primary_direction`;
- `system_carrier`;
- `control_status`.

This prevents a persistent skill library from being counted simultaneously as independent skill and
memory gains unless a factorial or matched ablation identifies both interventions.

## 3. Multimodality evidence gate

| Level | Contract |
|---|---|
| `MM0_TEXT_ONLY` | asset and decision are text-only; transfer comparator only |
| `MM1_MULTIMODAL_TASK_ONLY` | task has non-text input, but the K/S/M asset can remain text-only |
| `MM2_MULTIMODAL_ASSET` | the asset preserves image/audio/video/state evidence |
| `MM3_CAUSALLY_MULTIMODAL` | a same-run paired modality ablation establishes that non-text information changes the correct decision/outcome beyond a text shortcut |

No delta record is upgraded to MM3 merely because the benchmark is multimodal or a paper describes
images. H5-dependent generalizations remain prohibited before H5 closure.

## 4. Reference, borrowed protocol and reproduction

Every record has exactly one primary project-use relation:

| Relation | Meaning | Permitted claim |
|---|---|---|
| `REFERENCE_CONTEXT` | concept, failure taxonomy, boundary or explanatory evidence | “The work reports/defines/suggests …” |
| `BORROWED_PROTOCOL_ANALOGUE` | experiment structure, controls, ablations, evaluator or state contract is rebuilt for speech/omni | “The proposed protocol borrows these design elements …” |
| `REPRODUCTION_ANCHOR` | task, data revision/split, model/access, configuration, metric and evaluator are rebuilt with declared fidelity | exact, close-with-deviations or task-matched method reproduction only |

All 14 delta works are reference or borrowed-protocol evidence. None is a target speech/omni
reproduction anchor. This is a deliberate fail-closed result: task and modality changes are too large.

## 5. Citation boundary

The eight seed eprints underwent one-hop backward extraction of regex-resolvable arXiv IDs. Six works
were promoted because they changed a method path, supplied an instrument, established dataset
lineage or provided a material falsifier. The other 297 seen IDs do not enter the canonical denominator
and are neither reviewed nor excluded. DOI/title-only edges and forward citations remain open.

## 6. Paper-reported experiment contract

The 14 records capture only paper-reported settings and results with PDF page/table/section locators.
Numbers are interpreted within each paper and arm. They are not project results and are not combined
across papers. A cross-paper numerical comparison would require exact agreement on dataset revision,
split, core model/revision, access, input, prompt/system, metric/evaluator and budget.

## 7. Machine acceptance

The release-candidate checker must fail unless:

1. the exact 8-seed + 6-promotion identity set is present once each;
2. all 14 PDFs, eprints and extracted texts match 42 SHA-256 bindings;
3. every promoted work has a recorded parent edge in the bounded citation ledger;
4. identical retry events in the append-only full-text ledger are tolerated, but hash conflict fails;
5. D0-D4, content, persistence, MM level, role, disposition and use relation are complete;
6. reproduction subtype is absent for all non-reproduction records;
7. the census recomputes 226 frozen, 282 inherited and 296 release-candidate works;
8. 297 seen-not-promoted IDs do not inflate the denominator;
9. Stage-1B v5 remains fixed at `38fb9435d0c35e226ad62b16015a6dbee054e6c2`;
10. no Stage-1C activation, research execution, result or novelty field appears.

The checker writes a release-candidate report but has no code path for creating a reviewer signature.
