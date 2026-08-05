# Speech-aware evidence acquisition R0 review — audit index

This is the cold audit router for the independent R0 review transaction. Current research authority
remains `wiki/Research-Objective.md`; execution authority remains the consolidated owner contract at
`wiki/experiments/speech-aware-evidence-acquisition/2026-08-04-owner-consolidated-execution-contract.md`.
The review is advisory: it claims no human signature, owner ruling or new execution authority.

| Round | Type | Artifact and registered Git blob | At-issue status |
|---|---|---|---|
| `independent-review-2026-08-05` | AI doctoral-supervisor + senior-engineer independent R0 assessment | `wiki/audit/speech-aware-evidence-acquisition-r0-review/independent-review-2026-08-05/2026-08-05-saea-r0-independent-review-assessment.md` @ `PENDING_FIRST_COMMIT` (candidate blob `ba8a54f34cfd27443c1ee38b210bcbacd3dd26bf`) | `R0_REPAIR__R1_MODEL_FACING_EXECUTION_WITHHELD_PENDING_P0_CLOSURE_AND_R0_SMOKE` |

`PENDING_FIRST_COMMIT` is deliberate. The owner requested the assessment as a working-tree artifact
but did not authorize a commit in this transaction. The candidate blob was computed with
`git hash-object` over the current report bytes; it is not yet registered evidence. On the first
reviewed commit that contains the report, verify the committed blob, replace the pending token with
that blob id, and treat the registered audit bytes as immutable under `wiki/AI-Collaboration.md`.
