# Research Methodology

(Split out of CLAUDE.md on 2026-07-15 as part of "action C", the load-surface slimming. This page is
canonical; revisions go through dated supersession. CLAUDE.md keeps only a pointer and a one-line
summary.)

## Research process stages (Stage-1A/1B/1C → 2A/2B → 3; dated supersession 2026-07-18, owner ruling ①; Stage-2B/3 carrier binding, dated supersession 2026-08-04, continuation entry 91)

**The dividing line is the purpose of the activity and the use of its evidence**, not "whether Python
was ever started" or "whether the sample is small". Every deliverable states the stage it sits in.
**The current stage is authoritative in `wiki/Research-Objective.md`** (as of 2026-07-29: Stage-1C
direction-confirmation remediation, with Stage-1A/1B closed out); this page keeps only the semantic
definition of each stage. (Historical line: the Stage-1A survey-ready gate covered the problem and
the survey design; systematic discovery/mapping queries had not been executed, while targeted ID
dereference, raw provenance, fulltext preparation, and calibration trials had been; the first
systematic query after the Gate S1 signature plus owner approval enters Stage-1B.)

| Stage | Mission | Permitted | Forbidden (allowed only in the next stage) |
|---|---|---|---|
| **Stage-1A** | problem and survey design | problem tree, inclusion/exclusion criteria, search strings, seeds/sentinels, coding schema, known-item identity/routing and protocol-coverage checks, static and mutation testing of scripts | systematic mapping; any research-model call; conclusions about the novelty of a technical approach, or a prior-difference matrix |
| **Stage-1B** | **execution** of the systematic survey/mapping | search, deduplication, record screening, fulltext coding, citation closure, saturation analysis, evidence mapping, known-item carry-forward ledger, factual mapping of method paths and proximity | **smoke runs, task metrics, model/method comparison, headroom/accuracy/WER, and novelty verdicts — the research model must not be run at any point** (owner signature 2026-07-18) |
| **Stage-1C** | evidence synthesis and problem selection | produce 3–5 candidate problem/gap hypothesis cards and have the owner select the single problem; freeze the Stage-2A reproduction list and exploration constraints (without executing them, and without freezing an innovation) | using ad-hoc experiments to "campaign" for a candidate; writing a candidate gap up as an established technical innovation |
| **Stage-2A** | prior reproduction, approach exploration, and convergence of the technical innovation | **reproduce the closest and strongest public prior first**; only once that reproduction holds may an in-house directional prototype follow and converge the technical contribution (cheap small samples, explicit owner release, every attempt and failure registered, directional-only; **even a single item run purely as a smoke test counts as one experiment and one exposure**) | writing a directional result up as confirmatory; skipping prior reproduction and claiming to beat SOTA |
| **Stage-2B** | candidate qualification (converging a validated approach into a qualified paper candidate) | freeze the hypothesis, controls, and criteria; bounded validation and statistical design (a Research-Proposal-Template instance, pre-registration preparation, power estimation, a paired-bootstrap CI plan, adversarial review); freeze the candidate bundle and request paper GO | production-scale confirmatory work and final superiority conclusions (those belong to the Stage-3 paper repo); switching the primary metric after the fact, or selective reporting |
| **Stage-3** | publication-grade evidence (standalone paper repo, continuation entry 91) | through `OWNER_GO_AND_PAPER_EXECUTION_CONTRACT`, execute in the standalone `papers/<slug>` repo: large-scale pre-registered confirmatory runs and formal statistical inference, extensions, independent reproduction, paper-level audit, adversarial review to convergence, manuscript writing, and publication; positive, null, and negative results are equally legitimate | running a paper-scale campaign inside a study repo; substituting Stage-2A/2B small samples or probes for publication evidence |

**When novelty is decided (owner ruling ②, 2026-07-21).** Stage-1A only guarantees that the problem,
identity, routing, protocol, and execution gates are correct; it does not compare "how our technical
approach differs from prior work". Stage-1B maps method paths, coverage, and proximity faithfully and
issues no novelty verdict. Stage-1C forms candidate problems and gap hypotheses from the complete
evidence and selects the topic, but does not freeze a hypothesis into a technical contribution. The
novelty of a technical approach must converge out of the closest-prior reproduction and approach
exploration in Stage-2A, converge into a qualified paper candidate in Stage-2B, and finally be
validated by the pre-registered confirmatory work in the standalone Stage-3 paper repo (continuation
entry 91). "We found a directly adjacent prior" is a routing and coverage fact in Stage-1A/1B; it
does not kill a direction and does not force an early differentiated design.

**Exposure accounting (four fields, reported alongside the stage declaration; an unscoped "0 times"
is forbidden):** `current_activity_stage` / `new_model_touches_since_gate_freeze` (with the commit it
counts from) / `cumulative_model_touches` (project cumulative; if it is non-zero, write the non-zero
number) / `legacy_experiments = INHERITED_PRIOR_EXPOSURE` (historical experiments are never deleted,
never downgraded, and never treated as if they had not happened; they are the exposure union that
later reproduction, data splitting, and hypothesis freezing must exclude or stratify — canonical in
[[2026-07-18-inherited-prior-exposure-union]]).

**Tombstone (for audit; do not cite as current semantics).** The pre-2026-07-18 reading of
"Stage-1B = directional prototype exploration" and the continuation-entry-40 ordering (1A → 1B probe
→ 1C dual-evidence closeout) are superseded by the dated supersession in this section — directional
prototypes belong to **Stage-2A** from that point on. The **purpose** of the 07-16 ruling that
"survey execution is still 1A" (forbidding a premature claim of stage advancement) is inherited and
strengthened by the new table, which pushes even a smoke run to 2A. Trigger: v4 doctoral re-review
§1.1 plus owner ruling ① (Decision-Log continuation entry 65).

**Evidence-grade discipline.** Evidence always keeps the grade of the stage that produced it:
Stage-1/2 numbers stay hypothesis-grade until they are re-established by pre-registered confirmatory
work in the Stage-3 paper repo (continuation entry 91; what Stage-2B produces is candidate-grade
design and bounded validation, not publication-grade evidence). Records are append-only — a
regrading goes through a dated reflection document and never a rewrite. Apply this lens when reading
anything written before 2026-07 (stage names of that era map through the tombstone).

## Three phases of resource posture (owner, 2026-07-15) — same name, different structure from the three research-process stages; do not conflate them

**Reach for the ceiling → consolidate continuously → drive cost down** (the third phase often
corresponds to a third kind of paper).

- Early on the **budget is not bounded** — first find out "how high this approach can push the
  capability ceiling". "How high it can go" is itself the scientific output of the first phase
  (record the budget faithfully, set no cap).
- **Do not use phase-③ criteria (equal-budget deltas, cost normalization) to judge the feasibility of
  a phase-① approach**; every equal-budget comparison is labelled `PHASE-3_TOOL` and deferred.
- Why: normalizing budget too early systematically kills ceiling exploration. Cutting a direction
  because it shows no gain at equal budget means never discovering the "expensive but reachable"
  high point; only once that high point is known do the consolidation and cost reduction of phases ②
  and ③ have a target to aim at. The rigorous use of attribution in phase ① is "record the budget and
  attribute afterwards", not "push the budget constraint forward into the design".

## Theory track — rebuilt per study in Stage-2 (from 2026-08-03)

The program-level Lean formal layer is retired (the former `proofs/tfrl/` survives only in Git
history): the analysis and survey stages no longer build a general formula library, which is the
retrospective conclusion on Stage-1B over-design. The formalization obligation moves into Stage-2 of
each admitted study, and **each research object builds its own proofs**: the proof object is limited
to that study's own load-bearing claims, giving a **correctness proof** and a **convergence proof**
(a static identity is not a result); the engineering implementation and the theorem must be the
**same object** (dual track: the operator in the code ⟷ the operator in the theorem); convergence
usually needs an **explicit constraint term** to hold the edge of the problem (trust region, budget
cap, slow-drift premise, reward error bound), proving first that the unconstrained process does not
converge and then that the constrained one does. The W-era theory-track records survive only in Git
history and the archive.
