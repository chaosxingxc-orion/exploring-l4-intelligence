---
title: "Adversarial review of the three-stage architecture proposal, and decision request"
date: "2026-08-04"
review_target: "docs/superpowers/specs/2026-08-04-umbrella-studies-papers-three-stage-architecture-remediation-proposal.md"
review_method: "multi-round adversarial analysis grounded in repository facts"
verdict: "ACCEPT_CORE_SEMANTICS__REJECT_PATH_RESTRUCTURING__RESEQUENCE_IMPLEMENTATION"
adjudication_status: "ADJUDICATED__OWNER_ACCEPTED_WITH_MINIMAL_FIRST_TRIM__DECISION_LOG_XU91_XU92"
execution_authority: "DOCUMENTATION_ONLY__NO_NEW_AUTHORITY"
companion_plan: "docs/superpowers/plans/2026-08-04-three-stage-workspace-remediation.md"
---

# Adversarial review of the three-stage architecture proposal, and decision request

The object under review is the 2026-08-04 "Umbrella → Studies → Papers three-stage research engineering
architecture remediation proposal" (hereafter "the proposal"). Review method: first attack its necessity with
maximum force (round 1), then mount the strongest defense (round 2), then test both sides' arguments point by
point against the repository's machine facts (round 3), and finally give the verdict and revisions (round 4).
Every factual assertion carries a source and can be re-checked with `rg`.

## 0. Verdict summary

**Accepted**: the three-stage carrier semantics, the two independent gates, "promotion = an evidence
transaction", all of §4's scientific-integrity principles, the flat topology, and the separate registry.

**Rejected**: every restructuring of existing paths (`wiki/experiments/` and `docs/checks/` stay as they are);
the `wiki/directions/` directory layer; renaming the study gate token; treating in-repository layout
(proposal §8.2/§8.3) as normative.

**Resequenced**: the confirmatory reservation / exposure ledger moves earlier, from "a paper promotion artifact"
to a **Stage-2 prerequisite**; the promotion checker and dry run are deferred until SAEA produces a real
candidate (made trigger-driven).

**Machine-fact veto items** (implementing the proposal literally would immediately FAIL existing gates, see
C9/C10): naming something a "dated amendment" under `wiki/experiments/` triggers
`new-audit-artifact-outside-audit-root`; changing the AI-Collaboration placement table without synchronizing
the `ai_context_surface_check.py` constants will FAIL.

## 1. Round 1 — prosecution: attacking necessity

- **A1 (scale mismatch / YAGNI)**. Program reality: 1 owner, 1 admitted study, **0 formal experiments**
  (the `wiki/experiments/speech-aware-evidence-acquisition/README.md` ledger is empty and E0 is not yet closed).
  The proposal demands: a second registry, a second gate, a 20-field promotion package, ≥3 new checkers, 2 new
  test suites. The program's real bottleneck is E0 D1–D4, not a missing papers directory. The
  governance-to-research hours ratio is already very high, and every hour spent on schemas is taken from E0.
- **A2 (the problem is imaginary)**. The core fear in proposal §2.1 — "exposure/release cross-contamination
  when a second paper appears" — requires a first paper to exist. Today none does. Exactly one gap **really**
  exists right now: SAEA's Stage-2A contract (E0→R0→R1→X) has no paper-scale stop line. One page of contract
  fixes one gap; an architecture is not needed.
- **A3 (the existing mechanism already generalizes)**. The admission mechanism "semantically named independent
  repository + owner GO + execution contract + registry registration" is generic. On the day a paper repository
  is genuinely needed, run the same mechanism again; why pre-build a parallel root directory and registry?
- **A4 (bundling fallacy)**. The proposal sells two things bundled together: scientific-integrity mechanisms
  (exposure inheritance, confirmatory reservation, legitimacy of negative results) and carrier architecture
  (the papers/ root, dual registries). The former is **orthogonal** to directory structure and far more urgent —
  SAEA's X phase is about to read discovery data; the latter can wait. Bundling hides the difference in priority.
- **A5 (waterfall rigidity)**. Requiring a frozen 20-field bundle before a repository may be created assumes the
  candidate's outline is already clear at promotion time. ML research is iterative; if every backflow requires a
  dated decision, friction eventually grows until the executors (owner + AI) start routing around the ledger —
  over-heavy governance manufactures violations.

## 2. Round 2 — defense: the strongest case

- **D1 (defining boundaries at zero experiments is cheapest)**. With the ledger empty today, this is the
  historically lowest-cost moment to fix stage boundaries. Coming back to add boundaries after confirmatory data
  has been read means contamination is already irreversible. Proposal §11.3 makes this point itself.
- **D2 (a stop line must name what lies beyond it)**. A2 says "one page of contract is enough", but a stop line
  must state "what is on the other side, who owns it, and on what basis it is resumed". Without defining the
  paper-stage carrier, the stop line is only prose and no machine can check it. Precisely defining what lies
  beyond the line is exactly what this proposal is.
- **D3 (this repository's operating mode requires machine gates)**. The executing parties are the owner plus LLM
  collaborators. This repository's own history proves prose rules drift while machine gates do not: the G1 lesson
  (commit c9c9f6f "legacy validator now proves bindings, not formats") is exactly a case where prose claimed
  something was proven and a machine check found it was not. The target of scope-creep defense is the AI executor
  itself, so a fail-closed checker is not bureaucracy but a defense already validated in this repository.
- **D4 (multiple candidates are the stated intent)**. The SAEA research question (the four axes OBS/ORG/SUPPLY/USE)
  naturally produces several separately testable improvement points; in the three-stage formulation the owner
  explicitly says "one study produces one or more paper candidates". The risk of mixing several papers into one
  repository is not imaginary but an inevitable consequence of the established route.
- **D5 (mixing breaks machine checks)**. A3 says "just register papers as another study" — but studies and papers
  differ in lifecycle vocabulary, exit gate and exposure semantics; forcing them into one registry makes the
  precise validations of `study_workspace_check.py` (exact-key, lifecycle allowlist) ambiguous. A parallel root
  directory plus a parallel registry is in fact the **cheaper** machine-separable solution.
- **D6 (each of the 20 fields maps to an incident)**. Every field of the bundle maps to a class of real failure
  (baseline not runnable, exposure missing, power not computed, samples reused, …). Filling in the table takes
  hours; rework from any one of those failure classes takes weeks.

## 3. Round 3 — prosecution's rebuttal: testing against the repository's machine facts

The defense wins on "whether to do it" (D1–D3 hold), but the proposal's "how to do it" fails in several places
against repository facts:

- **C1 (path restructuring is net negative — rejected)**. Proposal §7 would move the experiment index to
  `wiki/experiments/studies/<slug>/` and check receipts to `docs/checks/studies|papers|promotions/`.
  Facts: (i) `study_workspace_check.py:148` hardcodes
  `expected_index = f"wiki/experiments/{slug}/README.md"`; (ii) registry v2 applies a **blob pin** to
  decision_record (`_validate_study_entry` recomputes the sha1 on the spot and compares); (iii) that path is
  referenced HOT in at least four places — Research-Objective, Experiment-Assets, studies/README, CLAUDE.md — so
  moving it must pass the five-step safety gate of AI-Collaboration §4; (iv) the current
  `docs/checks/<campaign>/<release-id>/` is already campaign-generic — paper receipts can use
  `docs/checks/<paper-slug>/<release-id>/` and promotion receipts `docs/checks/promotion-<paper-slug>/<release-id>/`,
  with zero migration. Expressing the stage in the path is entirely unnecessary; the registry field already
  expresses it. **Ruling: grandfather everything; migrate no existing path.**
- **C2 (the reservation ledger is misplaced in both time and space — resequenced)**. The proposal puts confirmatory
  reservation into the promotion package (the Stage-3 entrance), but the X phase of the Stage-2A contract already
  consumes discovery data and R0 already requires an "unread confirmatory carrier"; moreover the same conflict
  arises when **two studies** share Earnings21, long before any paper. Additionally the reservation ledger has no
  place in the §7 topology diagram — the risk table treats it as a BLOCKER mitigation while the body never gives it
  a file path. **Ruling: create the program-level ledger
  `docs/integrity/confirmatory-reservation-ledger.json` immediately with a fail-closed checker, and write the
  lookup obligation into the SAEA boundary contract.**
- **C3 (the v3 migration is unspecified and would explode if taken literally)**. `study_workspace_check.py:47`
  has `ADMITTED_LIFECYCLES = {"engineering", "validation", "paused", "complete", "sunset"}`, and `:105` enforces
  exact-key. The proposal's v3 vocabulary (`topic-analysis | baseline-qualification | ...`) is incompatible with the
  current value `engineering`, and no mapping is given. **Ruling: v3 takes a superset vocabulary (keep the existing
  five values, add `candidate-development` and `paper-candidate-ready`), SAEA's current value is untouched, and
  registry + checker + tests land in one transaction.**
- **C4 (multi-machine degradation conflict)**. `--require-installed` is primary-dev-machine mode (owner 2026-08-03);
  if the candidate bundle lives inside the study repository, promotion validation must read child-repository
  contents, which must degrade rather than FAIL on a machine without that checkout. Proposal §9.3 does not handle
  this. **Ruling: every validation that reads child contents is gated behind `--require-installed`, mirroring the
  handling of the existing origin/branch checks.**
- **C5 (the HOT budget is unaccounted)**. `wiki/Research-Objective.md` is currently 4763 bytes against a 5120
  budget, leaving **357 bytes**; manifest active entries are ≤30 (hardcoded at `ai_context_surface_check.py:1709`).
  Proposal T6 says "HOT only becomes a compact router" but never counts the bytes the new text would consume.
  **Ruling: every HOT edit states a byte budget, and over-budget edits trim old text first.**
- **C6 (renaming the gate token is pure liability)**. `OWNER_GO_AND_EXECUTION_CONTRACT` is already validated by the
  registry fixed-field check (`study_workspace_check.py:28`) and referenced by CONTRIBUTING, the AI-Collaboration
  table and signed contracts. Renaming it to `OWNER_GO_AND_STUDY_CONTRACT` would touch all of these and create a
  dual old/new vocabulary. **Ruling: the study gate keeps its current token; only add
  `OWNER_GO_AND_PAPER_EXECUTION_CONTRACT`.**
- **C7 (overreach into an independent repository's internal layout)**. Proposal §8.2/§8.3 prescribe the src/docs
  directory tree of study/paper repositories. CONTRIBUTING's first discipline is "commit each change to the repo it
  belongs to"; SAEA has its own CLAUDE.md and governance. The umbrella may require an **interface** by contract
  (for example the exposure ledger path and the candidate bundle path declared in the registry), but it cannot
  prescribe another repository's internal structure. **Ruling: §8 is demoted to a non-normative template.**
- **C8 (the 20 fields are treated uniformly)**. The fields all have value (D6 holds) but not the same strength.
  **Ruling: grade them — a missing BLOCKER field (13 of them) refuses promotion; a missing RECOMMENDED field
  requires an explicit owner waiver.**
- **C9 ("amendment" naming trips a machine gate — a literal implementation would FAIL)**.
  The `AUDIT_NAME_RE` at `ai_context_surface_check.py:81` matches basename tokens such as
  `proposal|amendment|review|report|response|correction|sign-off|adjudication|submission`; `:1831-1838` reports
  `new-audit-artifact-outside-audit-root` for any `.md` under `wiki/` matching that name and not under
  `wiki/audit|archive/`. If the "dated amendment" that proposal §11.3/T3 repeatedly demands were created literally
  as `wiki/experiments/.../*-amendment.md`, the surface check would FAIL outright. The currently legal form is the
  **owner contract naming** SAEA already uses (`...-contract.md`, as in the 2026-08-04 one), or going through the
  `wiki/audit/<campaign>/epoch-N/` state machine. **Ruling: name the SAEA narrowing document
  `...-owner-study-stage-boundary-and-paper-gate-contract.md`.**
- **C10 (the AI-Collaboration placement table is machine-pinned)**. `ai_context_surface_check.py:516-539` validates
  the placement table's row order and semantic tokens against the hardcoded
  `POLICY_TABLE_HEADERS / POLICY_ROLE_ORDER / POLICY_ROLE_SEMANTICS`. Adding a "Paper repository registry" row
  requires updating the checker constants and tests in the same commit. Proposal T1 never mentions this coupling.
- **C11 (manifest sha256 pin)**. Active entries of the AI context manifest contain `sha256` (`ENTRY_KEYS`), so any
  HOT file edit requires rebuilding the manifest and passing `build_ai_context_manifest.py --check`. The
  implementation steps must treat "edit → rebuild → verify" as one transaction; the proposal does not say so.

Also recorded, as the honesty obligation of an adversarial review, are the proposal's assertions **verified true**:
§2.2 papers infrastructure is zero (true); §9.3 a shared validator can be extracted (true, supported by the function
decomposition of `study_workspace_check.py`); §11.3 "no formal experiments yet, migration cost at its lowest"
(true, the ledger is empty); the `studies/*/` pattern in `.gitignore` can be carried over (true).

## 4. Round 4 — verdict synthesis

| Proposal content | Ruling | Basis |
|---|---|---|
| Three-stage carrier semantics, two gates | **Accept** | D1/D2/D4/D5 |
| §4 scientific-integrity principles (negative results legitimate, no chasing positive gains, monotonic exposure) | **Accept verbatim** | No valid rebuttal |
| Promotion = frozen bundle + bidirectional receipt + six-step non-atomic transaction | **Accept** | Isomorphic to this repository's blob-pin style |
| Flat topology, separate registry, umbrella tracks only README+registry | **Accept** | D5 |
| Restructuring the `wiki/experiments/` and `docs/checks/` paths | **Reject** | C1 |
| The `wiki/directions/` directory layer | **Reject** (keep a `direction` string field in the registry) | C5, no gate definition |
| Renaming the study gate token | **Reject** | C6 |
| §8.2/§8.3 in-repository layout | **Demote to a non-normative template** | C7 |
| Reservation/exposure ledger | **Move earlier to a Stage-2 prerequisite, placed in docs/integrity/** | C2 |
| The 20-field bundle | **Accept but split into BLOCKER/RECOMMENDED** | C8 |
| registry v3 | **Accept, superset vocabulary + single-transaction migration** | C3 |
| The "dated amendment" carrier | **Change to owner contract naming** | C9 |
| Implementing T1–T4 as one immediate package | **Split**: ruling + boundary contract + ledger + minimal papers surface immediately; promotion checker/dry run put behind a trigger | Balancing A1/A4 against D1 |

## 5. Revised answers to the proposal's eight questions in §16 (owner to rule point by point)

1. Accept the `umbrella → studies → papers` three-stage carrier; but the topology only adds a `papers/` root and
   restructures no existing path.
2. Accept "the study endpoint = a qualified paper candidate".
3. Accept "paper success = making a reliable judgment on a pre-registered claim, not necessarily a positive
   improvement" (verbatim).
4. Accept the two independent gates; the study gate keeps `OWNER_GO_AND_EXECUTION_CONTRACT`, and
   `OWNER_GO_AND_PAPER_EXECUTION_CONTRACT` is added.
5. Accept that SAEA remains a study; the narrowing document is a dated **owner contract** (named so as to avoid the
   audit token), retaining the existing E0/R0/R1/bounded-X authorization and all historical exposure facts.
6. Accept one `primary_study` per paper, plus zero or more `supporting_studies`.
7. Accept the program-wide confirmatory reservation and inherited exposure hard gates, with **the effective point
   moved earlier to Stage-2** (before the X phase), the ledger living in `docs/integrity/`.
8. **Amended approval**: implement immediately = the ruling ADR + the SAEA boundary contract + the reservation
   ledger + the minimal papers working surface + shared validator extraction + registry v3 + the promotion schema
   validator (with no consumer); trigger-driven implementation (any SAEA candidate entering
   `paper-candidate-ready`) = the promotion graph checker + a synthetic dry run + the first repository admission.

The implementation decomposition is in the companion plan:
`docs/superpowers/plans/2026-08-04-three-stage-workspace-remediation.md`.
Neither this document nor that plan grants authority for model calls, experiments, remote repository creation,
pushing or publication.
