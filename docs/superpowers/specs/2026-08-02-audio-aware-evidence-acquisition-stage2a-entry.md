# Audio-aware evidence acquisition: Stage-2A engineering entry contract

## Status

Entry contract prepared after `PASS_STAGE1C_FORMAL_OPENING` on 2026-08-02. The owner signed
`OWNER_GO_AND_EXECUTION_CONTRACT` on 2026-08-03; the dated decision record and frozen freeze-sheet
values live in
`wiki/experiments/audio-aware-evidence-acquisition/2026-08-03-owner-go-and-execution-contract.md`.
This specification remains the authoritative entry sequence (E0→R0→R1→X); execution stays bounded
by the contract's budgets and fail-closed receipts.

```yaml
semantic_research_object: audio-aware evidence acquisition
source_candidate_provenance: R2
stage1c_decision: PASS_STAGE1C_FORMAL_OPENING
authorization: OWNER_GO_AND_EXECUTION_CONTRACT
authorization_record: wiki/experiments/audio-aware-evidence-acquisition/2026-08-03-owner-go-and-execution-contract.md
novelty_status: NOT_YET_DETERMINED
method_status: EXPLORATION_SPACE_ONLY
repository_slug: audio-aware-evidence-acquisition
repository_url: https://github.com/chaosxingxc-orion/audio-aware-evidence-acquisition.git
experiment_index: wiki/experiments/audio-aware-evidence-acquisition/README.md
```

## Purpose

Enter Stage-2A without turning the full v20 research space into a single oversized first experiment.
The engineering sequence first proves that the carrier, information boundary, scorers and closest-prior
path are runnable. It then reproduces the nearest/strongest feasible prior before any self-authored
directional prototype. Stage-2A evidence determines the eventual method and innovation claim; this
contract does not predeclare either.

## Immutable research boundary

- Frozen Qwen3-Omni core accessed through an API-shaped serving boundary; no parameter modification.
- No task-trained model and no additional LLM with answer authority.
- Frozen tool-grade retrievers or judges are allowed only when pinned and logged; the frozen core retains
  final answer authority.
- No gold answer, reference transcript, test annotation or future turn may cross the runtime boundary.
- OBS re-resolution and external evidence supply remain separately traceable.
- Every external response, tool action, model request and derived artifact is versioned and hashable.
- Discovery and confirmatory items are disjoint; confirmatory decisions are frozen before reading results.

## Entry sequence

### E0 — Authorized model-free closure

Close data gates D1–D4 before any model touch:

1. verify cross-layer sample and segment identity for Earnings21, Earnings22 and ConEC;
2. materialize the information-boundary and leakage contract;
3. pin evaluation definitions, normalization and scorer behavior;
4. produce the ten-sample loader/provenance/trace receipt;
5. record license and redistribution constraints without copying restricted bytes into Git.

The canonical data authority is `docs/datasets.lock.json`; this study contract references it and does
not duplicate hashes that can drift.

### R0 — Reproduction-zero engineering slice (after owner GO)

Create the independent GitHub repository and local checkout only after authorization. The first bounded
slice should include:

- package skeleton, deterministic configuration composition, tests and CI;
- locked loaders and scorer adapters for one discovery carrier and one confirmatory carrier;
- frozen-core adapter with request/response and cost tracing;
- evidence schema covering provenance, OBS/SUPPLY separation, source admission and final use;
- MLflow/local artifact linkage through the umbrella experiment index;
- three engineering controls: bare frozen core, the carrier's canonical context form, and a simple
  fixed retrieval/context path.

These controls establish wiring and measurement integrity. They are not a final baseline set and cannot
support a novelty, superiority or causal claim.

### R1 — Closest/strongest-prior reproduction (after R0 integrity passes)

The owner execution contract must choose exact runnable revisions from the readiness-qualified prior
set. The initial reduction set includes ConEC/contextual ASR, RECOVER-style correction, the Siskos
entity-resolution line, and reproducible contextual-biasing groups. Corona 2017, Raghuvanshi 2019,
Flemotomos 2024 and COALA 2026 must be evaluated as threat/reproduction candidates before freezing the
mandatory list.

A prior may be excluded only by a recorded mismatch in task, information boundary, public artifact or
runtime feasibility. Failure of a frozen mandatory baseline is reported as
`INCONCLUSIVE_BASELINE_NOT_READY`; it is not silently replaced with a weaker opponent.

### X — Directional exploration and method convergence

Only after at least one closest/strongest-prior path is credibly reproduced may exploration test:

- OBS: whether audio re-resolution repairs entity-bearing observations;
- ORG/SUPPLY: whether organization, source choice and supply form change accessible evidence;
- USE/CONTROL: whether admission, ordering and reward-guided control reduce wrong corrections or improve
  stable utility.

RQ0's OBS × external-evidence factorial is the first discriminating experiment. Its result determines
whether later work retains all three pillars, merges them, narrows the study, or sunsets a branch. The
final technical method and innovation statement are outputs of this phase, not its inputs.

## Owner-GO freeze sheet

The following values must be concrete before `authorization` changes:

| Field | Required frozen value |
|---|---|
| Repository | remote URL, default branch, local `studies/<slug>/` checkout |
| Core/runtime | exact model files, runtime commit/build, quantization, device and API parameters |
| Carriers | exact lock entries, discovery/confirmatory splits, license and redistribution boundary |
| Information boundary | allowed runtime fields per arm; explicit gold/test/future-turn fence |
| Baselines | mandatory names and revisions, readiness checks, fallbacks and inconclusive behavior |
| Prompts/tools | prompt hashes, frozen retriever/judge revisions, source/date/query logging |
| Metrics | task metrics, entity metrics, correct-to-wrong/wrong-to-correct, tail and cost reporting |
| Resources | call/audio/GPU/annotation bands, first-slice cap and stop/go checkpoints |
| Exposure | inherited exposure exclusions plus per-run model/tool touch ledger |
| Wiki | experiment IDs, protocol/config hashes, MLflow/artifact routes and deviation process |

## First two-week deliverable after authorization

The first timebox delivers an executable and auditable reproduction-zero package, not a full v20 sweep:

- one end-to-end discovery path and one untouched confirmatory path;
- deterministic loaders, scoring tests and ten-sample trace audit;
- bare-core and fixed-context engineering controls;
- one readiness-qualified closest-prior smoke/reproduction attempt;
- call, latency, audio-seconds, GPU and artifact accounting;
- a go/narrow/repair/stop memo for the next Stage-2A slice.

The timebox stops immediately on information leakage, scorer disagreement, unstable sample identity,
unlicensed redistribution, irreproducible runtime pins or an undisclosed stronger runnable prior under
the same contract.

## Literature delta policy

After the 2026-08-02 cut, literature work is a bounded weekly delta lane running beside engineering.
New papers update the prior/threat queue; they do not reopen Stage-1C unless they invalidate the research
problem, carrier legality, information boundary or reproducibility contract. This prevents survey growth
from indefinitely delaying empirical convergence while retaining a fail-closed path for material evidence.
