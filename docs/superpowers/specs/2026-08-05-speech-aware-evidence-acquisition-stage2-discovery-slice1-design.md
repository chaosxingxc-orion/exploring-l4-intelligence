# Speech-aware evidence acquisition: exploration structure for the Stage-2 discovery first slice

## Status

This document refines the exploration structure of the discovery first slice **within** the framework of
the 2026-08-02 entry contract (`docs/superpowers/specs/2026-08-02-speech-aware-evidence-acquisition-stage2a-entry.md`)
and the 2026-08-04 consolidated execution contract
(`wiki/experiments/speech-aware-evidence-acquisition/2026-08-04-owner-consolidated-execution-contract.md`);
it modifies no contract-frozen value (boundary, budget caps, execution profile, the E0→R0→R1→X order).
E0 and the runtime receipt were closed on 2026-08-04 and verified by gate dry-run (study repo
`docs/receipts/`).

```yaml
record_kind: stage2-discovery-slice-design
date: 2026-08-05
study: speech-aware-evidence-acquisition
scope: discovery slice 1 (E0 closed; R0 + R1 + X1-X3)
decided_by: owner in-session answers, 2026-08-05
amends_contracts: none
```

## Decision record (owner ruled in session, 2026-08-05)

1. The claim type of the paper candidate is **left open for now and decided by discovery evidence**;
2. The first slice's thin probes cover **X1–X3**; X4 (reward-guided vs fixed policy) and X5 (secondary-carrier
   transfer) are deferred to the second slice because they depend on the results of the first three (a budget
   renewal at that point requires a dated amendment);
3. For the R1 baseline, **a per-axis readiness comparison memo comes first and the owner then rules**; no
   preferred candidate is presumed;
4. Work **overlaps within the slice**: the model-free readiness memo runs in parallel with R0 engineering wiring;
5. Each validation point **embeds the strongest runnable published method for that axis as a reproduction arm**
   (a matrix structure, see §1);
6. This design **makes no budget allocation**; the first slice's total cap is frozen by consolidated contract §6,
   and per-run usage is declared in each `ExecutionPlan` and pre-registered through exposure.

## §1 Organizing dimension: validation points as the skeleton, paper reproductions as comparison columns

Stage-2 exploration is not a choice between "paper reproduction" and "technical validation point"; it is a
matrix:

- **Rows (skeleton)**: single-axis validation points of the contract's X sequence. The first slice runs three
  minimal factor experiments: X1 (OBS), X2 (ORG/SUPPLY), X3 (USE);
- **Columns (calibration and comparison)**: R1 performs a full-protocol end-to-end reproduction of one strongest
  same-task/same-carrier/same-boundary prior, answering "is our measurement pipeline trustworthy?"; at the same
  time, each validation point's factor table embeds the strongest runnable published method for that axis as a
  mandatory arm, answering "how far do existing methods get at our boundary, and where do they fail?".

Paper reproduction is therefore not a one-off calibration action but a comparison column running through every
validation point, and simultaneously the evidence source for innovation points (§6).

## §2 What is validated: three falsifiable hypotheses and their arm sets

Each point is a minimal factor experiment with "every other axis frozen, only one axis moved"; all three gates
(effectiveness / reasonableness / efficiency) are reported together; gold/reference/test annotations/future turns
never enter runtime; oracle evidence serves only as an upper-bound interface and never enters formal runtime.

- **X1 (OBS)** hypothesis: re-parsing entity-dense segments (re-transcription / multiple hypotheses / confidence
  localization) reduces entity mishearing without degrading overall WER. Arm set: bare core / prior reproduction
  arm (a published approach feasible within the API boundary, with the specific paper fixed by the readiness memo)
  / this repository's OBS variant. Decision metrics: entity recall/F1, entity-WER, correct-to-wrong transitions.
- **X2 (ORG/SUPPLY, OBS frozen)** hypothesis: the organization and supply form (granularity/quantity/order) of legal
  evidence (ConEC supplementary contexts) changes evidence accessibility, raising wrong-to-correct without raising
  correct-to-wrong. Arm set: no-context / a verbatim reproduction of the ConEC paper's context-injection method /
  this repository's organized supply variant / a random-mismatched negative control.
- **X3 (USE, supply frozen)** hypothesis: evidence admission/verification control reduces correct-to-wrong regression
  when the supply contains incorrect evidence. Arm set: no-verification / a published correction or evidence-verification
  approach (RECOVER-style 1-best correction or a QA verification line, fixed by the readiness memo) / this repository's
  admission-verification control; the supply contains controlled contaminated evidence.

## §3 Carrier and split allocation

- **discovery** = `earnings21-original` + `conec` contexts (the ConEC contexts hang off Earnings21; used directly by
  the R1 reproduction and X2);
- **dev** = the Earnings22 upstream-curated subset10 (already exposed as dev by E0 D4; continues to carry
  smoke/debugging);
- **confirmatory** = the remainder of `earnings22-original` after removing subset10: kept unread and never touched in
  the first slice; before any confirmatory read, the frozen split identity hash is registered in the experiment ledger
  and the exposure ledger and marked consumed (consolidated contract §7).

## §4 Decision and promotion rules (pre-registered before results are read)

At the close of each thin probe, one of three states is assigned:

- **PROMOTE**: the gain is real, attributable to a single axis, and the negative control is clean;
- **PARK**: no gain, or not attributable;
- **REPAIR**: a measurement or wiring problem, rerunnable after repair (does not count toward the axis conclusion).

Selection criterion for an axis to be deep-dived in the second slice: that axis PROMOTEs **and** the innovation
candidate ledger (§6) already holds a falsifiable delta claim targeting that axis. If everything PARKs, a narrow/stop
memo is issued. A zero/negative result is a legitimate way for a slice to complete. The decision rules are frozen
before any confirmatory result is read; the first slice uses only the discovery and dev splits.

## §5 Execution order (overlapping)

- **Parallel track A (model-free)**: a per-axis prior readiness list — for the contract §4 candidate lines
  (ConEC/contextual ASR, RECOVER-style 1-best correction, Siskos entity resolution, the FlexCTC/TurboBias biasing line)
  and for same-boundary methods newly identified during readiness research, record item by item the runnable revision,
  license, API-boundary compatibility, scorer alignment method, and any reason it cannot run. All three outcomes are
  useful: runnable ones become reproduction arms at the corresponding validation point; the strongest and closest one is
  ruled by the owner to be the target of the R1 full-protocol reproduction; those not runnable within the boundary
  (expected to include biasing lines needing logit access) are filed under `INCONCLUSIVE_BASELINE_NOT_READY` semantics as
  structural-gap evidence (§6 source 3).
- **Parallel track B**: R0 engineering wiring (the entry contract's seven deliverables: deterministic loader,
  frozen-core adapter, four-axis trace, scorer adapters, the three engineering controls, the negative control and oracle
  upper-bound interface, and MLflow/ledger linkage plus cost accounting). R0 verifies wiring and measurement integrity only.
- **Serial after the tracks converge**: owner rules the R1 baseline → R1 reproduction → X1 → X2 → X3 → the three-gate joint
  table + a go/narrow/repair/stop memo, closing the first slice.

The model-contact order remains strictly E0 (closed) → R0 → R1 → X; every contact carries a valid `ExecutionPlan`, is
pre-registered first in the study repo `docs/exposure-ledger.md`, and is enforced fail-closed by
`contracts.FrozenCoreGate`.

## §6 Innovation-discovery mechanism

Innovation points arise from three controlled sources, all landing in the study repo `docs/innovation-candidates.md`
(an append-only innovation candidate ledger, each row carrying an evidence pointer: receipt / ledger row / memo path):

1. **Reproduction failure modes**: at the close of each validation point, issue a gap memo — on which entities and under
   which conditions the prior method fails, whether it introduces correct-to-wrong, and whether the failure is attributable
   to an axis. The standard form of an innovation claim: "prior P has failure mode F at this boundary, and axis control C
   eliminates F" — naturally falsifiable and carrying its own baseline.
2. **The three capability gaps pre-registered in the contract** (accessibility, timeliness/proper nouns, verifiability):
   each validation point's results fill in the degree to which that gap is covered by priors.
3. **Structural boundary gaps**: method lines judged NOT_READY in the readiness memo, demonstrating that no published
   feasible approach yet exists for that capability on an API-only frozen core; if this repository's external control plane
   achieves the same effect, it is the first feasible approach within the boundary.

The ledger serves Stage-2B: a qualified paper candidate (improvement claim + null hypothesis + mechanism + baseline receipts
+ an unread-confirmatory declaration) may only arise from an axis that already holds a falsifiable delta claim in the ledger.

## §7 Stage-2 decomposition (added 2026-08-05; aligned with the Stage-1A/1B/1C split)

Model contact occurs only at four places — 2A-R0.3, 2A-R1, 2A-X and the 2B deep dive — each with its own `ExecutionPlan`
budget and exposure row; everything else is model-free.

- **2A-E0** closure (closed on 2026-08-04): the D1–D4 receipts + runtime receipt + gate dry-run.
- **2A-R0.1** scaffolding + memo (model-free): the per-axis readiness list + the innovation candidate ledger; exit = the
  owner rules the R1 baseline.
- **2A-R0.2** engineering baseline (model-free, fake-transport tests): a **two-layer structure** — Layer 1 is reusable
  foundation engineering (a single `core/` package: unified registry, unified driver `run_experiment()`, five abstraction
  seams: carrier/split, evidence source, transport, scoring adapter, execution policy; the governance layer
  contracts/gate/D2 arm shape/frozen scoring is not abstracted and leaves no seam); Layer 2 is configuration-driven
  experiments (each experiment = four config fragments + at most one newly registered component + pre-registration).
  Exit = all tests pass, both repositories' gates green.
- **2A-R0.3** smoke (first model contact, SAEA-E-001, dev subset10, ~12 calls): exit = trace complete, budget matches,
  hashes all present (a wiring memo, not a result claim).
- **2A-R1** reproduction calibration (model contact, discovery split): full-protocol reproduction of the selected prior;
  exit = metrics land within an explainable deviation band, or `INCONCLUSIVE_BASELINE_NOT_READY` is filed.
- **2A-X1–X3** thin probes (model contact, each containing a prior reproduction arm): a factor table + gap memo + ledger
  entry per point; exit = PROMOTE / PARK / REPAIR per point (§4).
- **2A close** (model-free): the three-gate joint table + a go/narrow/repair/stop memo.
- **2B deep dive** (model contact; budget requires a dated amendment): a second slice on the PROMOTEd axis + X4/X5.
- **2B qualification → freeze** (model-free): improvement claim + null hypothesis + mechanism + baseline receipts +
  experiment/statistical design + unread-confirmatory declaration → a qualified paper candidate, the study endpoint;
  zero/negative results are legitimate.
- **Stage-3**: not in this repository; promoted to `papers/<slug>` through `OWNER_GO_AND_PAPER_EXECUTION_CONTRACT`.

## Invalidation conditions

When the owner modifies the claim-type decision, validation-point coverage, split allocation or promotion criteria, this
document is superseded in place per `wiki/AI-Collaboration.md` with the dated record retained; the stop-the-line triggers
carry over from the entry contract.
