# SAEA standard scheme v1 — architecture freeze (B0)

Date: 2026-08-17. Status: owner-approved direction (capability-ladder GO, this date); field-level
contract draft for owner review. Carrier: `studies/speech-aware-evidence-acquisition`.
Supersedes the 2026-08-08 unified-agent-abstraction draft.

## 1. Why this document exists

Two owner findings, 2026-08-17: (a) the study over-anchored on earnings ASR, where a frozen omni
core has no structural advantage over dedicated ASR and knowledge supply has no leverage (measured:
whole-reference supply is a copy trap, 7/9 blind-copy; per-span routing recall 0.94%, no usable
operating point); (b) the agent scheme was never frozen — modules had no interface contracts, so
every experiment grew ad-hoc scripts. This document freezes the scheme so that exploration runs on
shared rails and "mounting a technique" becomes a config change, not a new pipeline.

## 2. Research object (as ratified)

A standard, fully-instrumented closed-loop scheme for speech-aware agents on a frozen omni core:
threshold-gated retrieval from legally-tiered knowledge stores, keyed by task-native queries, and
delivered as prompt-level supply (owner ruling 2026-08-17: no logit-level control anywhere). The
scheme reproduces published consumption findings as calibration, then serves as the testbed on
which text-agent techniques are mounted and their multimodal transfer measured (use/copy/ignore,
dose law, price of legality, allocation bound). Runtime memory writes are out of scope
(knowledge-only ruling 2026-08-16; memory research belongs to future studies): all knowledge
stores are built offline and are read-only at runtime. Speech-keyed multi-view retrieval
(content/speaker embedding keying) is likewise out of scope by owner ruling 2026-08-17 — that
line is deferred wholesale to the future memory-focused studies.

## 3. Capability ladder (task portfolio)

| Level | Task family | Carriers | Supply-leverage expectation |
|---|---|---|---|
| L1 | ASR / entity transcription | earnings21/22 (harvested; calibration substrate only) | ~0 (measured: copy trap; the zero anchor of the curve) |
| L2 | Context-conditioned entity ASR | contextasr-bench | transitional |
| L3 | SLU (slots/intent) | SLURP (acquisition pending) | medium |
| L4 | Spoken QA / meeting understanding | slue-sqa-5, librisqa, AMI | high |
| L5 | Agentic speech (tool use) | Audio2Tool (+ survey candidates) | measured headroom: tool-acc 84.6% vs EM 15.6% |

Primary claim surface: the supply-benefit-versus-task-level curve. L1 anchors it at zero; L5
anchors the headroom. Earnings work is never re-opened as a claim generator.

## 4. Modules and typed flow contracts

All artifacts are versioned, content-hashable (stable JSON + sha256), and ledger-addressable.
External responses, tool actions, model requests and derivatives remain individually versioned per
the study boundary.

```
            ┌── ORG (offline build) ───────────────────────────┐
            │ legal-tier KB: shipped docs / metadata rosters /  │
            │ lexicons; E1' tier fields stamped at build time   │
            └───────────────┬──────────────────────────────────┘
speech ─→ OBS ─→ SUPPLY gate ┴─→ prompt assembly ─→ frozen core ─→ answer
                   task-native-key retrieval,        (single answer │
                   threshold τ, dose D, form F        authority)    ▼
                                                         ConsumptionTrace
                                                          (USE|COPY|IGNORE)
                                                                 │
                                          TaskAdapter scoring ←──┘
```

### 4.1 ObsPacket (OBS output)
`audio_ref{path, sha256}`, `spans[]`, `first_pass` (optional core hypothesis; absent in
engineering tests), `obs_version`, `hash`. No embedding-view fields: speech-keyed retrieval is
out of scope for this study (owner ruling 2026-08-17; deferred to the memory studies).

### 4.2 EvidenceItem / EvidenceSet (ORG → SUPPLY)
`EvidenceItem{content, source_ref, span_source, reference_source, tier}` — legality fields reuse
`core/legality.py` (E1') verbatim; the either-field rule stays machine-enforced: any gold-derived
field forces ceiling tier, and deployment-tier arms reject ceiling items before flight.
`EvidenceSet{items[], query_ref, retrieval_params{key_kind, τ, k}, hash}` where `key_kind` names
the task-native query key (e.g. `task-context`, `first-pass-text`).

### 4.3 SupplyPacket (SUPPLY → core)
`form ∈ {roster, text, kv}`, `dose{n_items, token_count}`, `prompt_block`,
`assembly_template_id`, `hash`. Prompt-level supply only.

### 4.4 ConsumptionTrace (USE instrumentation)
Per-span `{supplied_item_id, outcome ∈ USE|COPY|IGNORE, evidence}`, `copy_rate`,
`dose_realized`. Semantics aligned with the P2 evaluator (byte-identical parroting = COPY).
Copy-rate is a first-class metric on every arm of every probe.

### 4.5 TaskAdapter (per-task plug-in)
`load_split(split_id)`, `build_query(sample, obs)`, `assemble_prompt(sample, supply|None)`,
`score(sample, response)`, `extract_consumption(sample, supply, response)`. One adapter per
carrier; the runner, contracts, exposure discipline and flight lock are shared.

### 4.6 Runner
One config schema (existing model/dataset/baseline/experiment composition), enforcing
`contracts.ExecutionPlan` + `assert_execution_scope` (fail-closed), the E0' flight lock, and
manifest finalization. Zero-supply and supplied arms differ only in `SupplyPacket`.

## 5. Per-edge beneficial-effect claims (each measurable)

| Edge | Claim | Status |
|---|---|---|
| ORG → SUPPLY | legal coverage bounds any supply gain (coverage → gain transfer) | T-NDL measuring (number/date three-way decomposition) |
| OBS → SUPPLY | aperture law: global compact supply works where per-span routing is structurally dead | measured (N1: routing recall 0.94%, no usable operating point; kb34: global 10/14 flips) |
| SUPPLY → USE | dose/form law: compact roster 10/14 flips vs whole-text 7/9 blind-copy | measured (P2, kb34) |
| USE | copy/use/ignore instrumentation with per-span provenance | built (P2 evaluator → rails) |
| task level | supply benefit grows with capability level | new primary; L1 anchor measured |

## 6. B0 acceptance criteria

Same config schema runs one ASR-family task and one agentic task end-to-end (mock core client in
tests; real core on first flight) with zero-supply and supplied arms, no hand-written glue; full
pytest green; legality gate demonstrably rejects a gold-derived EvidenceItem from a
deployment-tier arm; every inter-module artifact round-trips with a stable hash.

## 7. Out of scope

Runtime memory writes AND speech-keyed multi-view retrieval — both deferred to the future
memory-focused studies (owner rulings 2026-08-16/17); logit-level control (`logit_bias` ruled
out); any second answering LLM; paper-scale confirmatory campaigns (Stage-3, machine-enforced);
FSD50K/AudioSet/ESC-50 in any form.
