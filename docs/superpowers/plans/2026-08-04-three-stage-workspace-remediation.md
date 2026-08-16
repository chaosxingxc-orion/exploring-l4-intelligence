# Three-Stage Workspace Remediation Plan (minimal-first, owner-trimmed)

**Goal:** move the Stage‑3 mission (large-scale empirical work and publication) out of the study repo's
default authorization, and stand up the `umbrella → studies → papers` three-stage carrier architecture with
the smallest possible placeholder surface; every machine-enforced component is deferred until real content
appears.

**Ruling:** Owner 2026-08-04 (Decision-Log-2026-08 continuation entry 91): the three carrier layers are
exactly the carrier bindings of the existing Stage‑1/2/3; "take it slowly, stand the architecture up first,
and do not over-design before there is content to fill in". Review basis:
`docs/superpowers/specs/2026-08-04-three-stage-architecture-critique-and-decision-request.md`
(all of that document's accept/reject/re-prioritize rulings on GPT-5.6's original proposal are in force).

## Phase A — executed (2026-08-04)

- [x] Decision-Log-2026-08 gains the continuation entry 91 ADR: carrier binding, freezing the
  `OWNER_GO_AND_PAPER_EXECUTION_CONTRACT` token, the paper success criterion (positive/zero/negative results
  equally legitimate), the minimal-implementation and deferral lists, and upholding the review's rejections.
- [x] Conceptual-layer HOT updates: `Project-Thesis` (repo model table + the study-endpoint sentence),
  `Architecture` (directory tree + three-stage pipeline + the cadence sentence in both languages),
  `Research-Objective` (the carrier-binding sentence, 4994/5120B), `CLAUDE.md`/`AGENTS.md` (all umbrella-owned
  surfaces + the cadence sentence, mirrored consistently, 8558/8545B ≤12KB), `Experiment-Assets` (the Paper
  project registry subsection, admitted **0**).
- [x] papers placeholder surface: `papers/README.md` (promotion rule + empty registry legal / empty repo
  illegal + the deferral statement), `papers/registry.json` (`paper-repository-registry-v1`, `papers: []`),
  and `papers/*/` added to `.gitignore`. **No checker** — machine verification lands with the first admission.
- [x] SAEA Stage‑3 boundary contract:
  `wiki/experiments/speech-aware-evidence-acquisition/2026-08-04-owner-stage3-boundary-and-paper-gate-contract.md`
  (retains E0/R0/R1/bounded X; the study endpoint = a qualified paper candidate; paper-scale forbidden by
  default; historical exposure/budget never written back); experiment-index routing and front matter updated;
  `studies/registry.json` decision_record re-pinned (blob `5f91226f25d6bfd5c5cd427c57fecc635eb43066`);
  `experiment-asset-inventory.json` re-rendered; the AI context manifest rebuilt.
- [x] Verification: the five umbrella gates PASS; `pytest scripts/checks` 143 passed/2 skipped;
  WSL `pytest common/tests` 21 passed/1 skipped.

## Phase A′ — implementation review remediation (2026-08-04, continuation entry 92; review: specs/2026-08-04-three-stage-architecture-implementation-review-assessment.md)

- [x] **R0 complete replacement of current truth** (P0-1/P1-3/P2-1/P2-2): Research-Methodology Stage‑2B/3
  redefined; the old "all work stays in the study" sentence replaced everywhere in
  README/README_CN/CONTRIBUTING(+CN)/docs/architecture/wiki-Architecture/the client guides;
  Per-Work-Status stop line; Experiment-Assets made carrier-aware (carrier type/split role/split identity
  hash/consumed); AI-Collaboration gains the Paper registry row + the surface-check constants and tests in the
  same commit; ruling banners on the proposal/review documents.
- [x] **R1 self-contained authority** (P1-1, review option A): `2026-08-04-owner-consolidated-execution-contract.md`
  merges GO + identity + scope + budget + execution scope + the Stage‑3 stop line + the source blob table;
  registry/index/HOT all re-pinned (blob `8ddd0cf2a96908befc8b49e69602185729ba17ba`).
- [x] **R2 adoption in the independent study repo** (P0-2): study commit
  `6c4b37e9ff90becde3df934fa2b87e136f1354eb` — guides/README/engineering routing point at the new contract;
  `contracts.assert_execution_scope` fail-closed (only model-free-check/baseline-reproduction/bounded-discovery-probe;
  paper-scale always refused); `FrozenCoreGate.assert_model_touch_allowed(execution_profile)` must declare a
  profile; 76 tests green.
- [x] **R3 zero-state paper gate** (P1-2): `paper_workspace_check.py` (strict empty registry / zero children /
  ignore rule / count consistency; any paper entry fails closed) + 1 positive and 10 negative cases; inventory
  raised to v3, incorporating the paper registry sha256.
- [x] **R4 exposure minimal prerequisite** (P1-4): this round completed only the **umbrella experiment index**
  column additions, the checker enforcement, and changing the trigger to the earliest of the four events; the
  contract fields of the study-side exposure ledger were completed in Phase A″ after the second review round
  pointed them out (the earlier checkbox was too strong and is corrected here to match the facts).

## Phase A″ — second review round remediation (2026-08-04, continuation entry 93; review: specs/2026-08-04-three-stage-architecture-remediation-rereview-assessment.md)

- [x] **P1-1 stage semantics on the default surface**: the AGENTS/CLAUDE three-sentence form (2A converges →
  2B qualifies a candidate → Stage‑3 final validation); RO/EA candidate-method wording; the
  `validate_stage_truth` forbidden-phrase gate (scoped to only the four default/control-plane files — audit and
  archive records legitimately retain historical phrasing and are not scanned) + positive and negative tests.
- [x] **P1-2 exposure ledger interface closure**: the study `docs/exposure-ledger.md` header gains
  execution profile/scope/split role/split identity hash/consumed/inherited exposure together with their
  semantic rules (consumed=yes is irreversible); both the study tests and the umbrella checker now parse the
  real header; the "keep the word in the body, delete the header column" regression case is covered in both
  repositories.
- [x] **P1-3 semantic scope gate**: `ExecutionPlan` (saea-execution-plan-v1, every field a contract-frozen
  value); the gate validates the plan first (confirmatory split refused, first-slice budget cap, 64-hex hash),
  then requires exposure pre-registration and the lock carrier, and finally validates the receipt; bare profile
  strings retired; the study suite is 82 green.
- [x] **P2-1/2/3**: README_CN layout + gate list, CONTRIBUTING dual-index routing, per-carrier summaries in the
  guides, the AI-Collaboration Paper experiment index row (surface constants in the same commit), papers/README
  and this plan's wording brought in line with the facts, and the contracts module's authority comment changed
  to the consolidated id.
- [x] Study adoption commit: `db284ae6e9a664c262640d93d83bfa873f01516b` (registered in place in the experiment index).

## Phase B — deferred (the trigger was revised per continuation entry 92: the earliest of the four events below, or the owner starting the first paper admission — before the first bounded X reads a discovery result / before a second shared-carrier study / before the first confirmatory split is materialized or read / before any candidate applies for paper-candidate-ready)

When the trigger fires, **write a fresh execution plan against the repository as it stands then** (the details
are redesigned at that time; this section fixes only the acceptance semantics and the constraints already ruled
on, to prevent a loss of coverage):

1. **Promotion schema** (candidate bundle + promotion receipt): BLOCKER/RECOMMENDED grading (review C8); the
  bundle is frozen as a study-repo Git blob, and the umbrella receipt binds bidirectionally to the paper's
  initial commit.
2. **Extend the zero-state `paper_workspace_check.py` into admitted-entry mode** (the zero-state version landed
  in A′): entry schema, candidate tokens forbidden in slug/package/namespace, primary_study must resolve,
  origin/branch/blob verification; the part that reads child contents is gated behind `--require-installed`
  (review C4); extracting the shared validator happens in step with this (the review confirmed it is feasible).
3. **Program-wide confirmatory reservation ledger**: a machine ledger under `docs/integrity/` + a fail-closed
  checker; it takes effect before any confirmatory read (review C2). Until then the responsibility is carried by
  the boundary contract + the study repo `docs/exposure-ledger.md` + the 2026-08-03 program visibility discipline
  (split hash / consumed marker).
4. **study registry v3**: a superset lifecycle vocabulary (adding candidate-development/paper-candidate-ready) +
  provenance fields; registry + checker + tests in a single transaction (review C3).
5. **AI-Collaboration placement table**: the Paper repository registry row (A′) and the Paper experiment index
  row (A″) have both landed; any further added or modified row must still ship in the same commit as the
  `POLICY_ROLE_ORDER`/`POLICY_ROLE_SEMANTICS` constants of `ai_context_surface_check.py` and their tests
  (review C10).
6. **First-repository admission runbook**: semantic naming, explicit authorization for remote creation, the
  six-step non-atomic promotion transaction, initial CI, the
  `docs/checks/promotion-<paper-slug>/<release-id>/` receipt, and fail-closed cases for a synthetic dry run.

## Permanent constraints (already ruled on; not reopened by Phase B)

- Do not reorganize the existing paths of `wiki/experiments/` and `docs/checks/` (grandfathered, review C1);
- Do not create `wiki/directions/`; the study gate keeps `OWNER_GO_AND_EXECUTION_CONTRACT` (review C5/C6);
- The basename of a new file under `wiki/` must not use an `AUDIT_NAME_RE` token
  (amendment/proposal/review/…, review C9);
- The umbrella does not prescribe the internal layout of a study/paper repo, only the interface agreed by
  contract (review C7);
- Paper success is not conditional on a positive improvement; the HARKing defenses (pre-registration, unread
  confirmatory, monotonic exposure) must never be weakened.
