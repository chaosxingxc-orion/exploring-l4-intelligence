# Speech-aware evidence acquisition R0 review — audit index

This is the cold audit router for the independent R0 review transaction. Current research authority
remains `wiki/Research-Objective.md`; execution authority remains the consolidated owner contract at
`wiki/experiments/speech-aware-evidence-acquisition/2026-08-04-owner-consolidated-execution-contract.md`.
The review is advisory: it claims no human signature, owner ruling or new execution authority.

| Round | Type | Artifact and registered Git blob | At-issue status |
|---|---|---|---|
| `independent-review-2026-08-05` | AI doctoral-supervisor + senior-engineer independent R0 assessment | `.../independent-review-2026-08-05/2026-08-05-saea-r0-independent-review-assessment.md` @ `ba8a54f34cfd27443c1ee38b210bcbacd3dd26bf` | `R0_REPAIR__R1_MODEL_FACING_EXECUTION_WITHHELD_PENDING_P0_CLOSURE_AND_R0_SMOKE` |
| `independent-review-2026-08-05` | Implementation-side response (verdict accepted in full; findings independently re-verified; root causes; method change) | `.../independent-review-2026-08-05/2026-08-05-implementation-response.md` @ `efd9ff4739d03293e15efaf38944468f0d214c1c` | `ACCEPTED_IN_FULL` |
| `independent-review-2026-08-05` | Repair submission package after five external adversarial rounds (round 5 = ZERO_DEFECTS_CONFIRMED at Critical/Important) | `.../independent-review-2026-08-05/2026-08-05-repair-submission-package.md` @ `PENDING_FIRST_COMMIT` | `FINAL__AWAITING_FRESH_REREVIEW` |

The assessment's blob is now registered from its committed bytes. The submission package still reads
`PENDING_FIRST_COMMIT` because it is registered in the same commit that first contains it; on the next
reviewed commit, verify its committed blob and replace the token. Registered audit bytes are immutable
under `wiki/AI-Collaboration.md`; corrections append a new round artifact rather than editing one.

**Owner action arising from this campaign, filed as execution authority (not an audit artifact):**
`wiki/experiments/speech-aware-evidence-acquisition/2026-08-06-owner-budget-caps-retirement-contract.md`
retires the first-slice numeric budget caps of the consolidated contract §6 (signed 2026-08-06). It
lives with the other owner contracts because it *is* execution authority; audit-iteration naming
(`…-amendment-<n>.md` under `epoch-<n>/`) is reserved for amendments to audit artifacts themselves.
Consequence for reviewers: absence of numeric-cap enforcement is an owner scope reduction, not a
defect; the one-time attempt semantics of finding P0-4 remain in force.
