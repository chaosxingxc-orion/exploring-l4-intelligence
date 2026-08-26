# Speech-aware evidence acquisition R0 review — audit index

This is the cold audit router for the independent R0 review transaction. Current research authority
remains `wiki/Research-Objective.md`; execution authority remains the consolidated owner contract at
`wiki/experiments/speech-aware-evidence-acquisition/2026-08-04-owner-consolidated-execution-contract.md`.
The review is advisory: it claims no human signature, owner ruling or new execution authority.

| Round | Type | Artifact and registered Git blob | At-issue status |
|---|---|---|---|
| `independent-review-2026-08-05` | AI doctoral-supervisor + senior-engineer independent R0 assessment | `.../independent-review-2026-08-05/2026-08-05-saea-r0-independent-review-assessment.md` @ `ba8a54f34cfd27443c1ee38b210bcbacd3dd26bf` | `R0_REPAIR__R1_MODEL_FACING_EXECUTION_WITHHELD_PENDING_P0_CLOSURE_AND_R0_SMOKE` |
| `independent-review-2026-08-05` | Implementation-side response (verdict accepted in full; findings independently re-verified; root causes; method change) | `.../independent-review-2026-08-05/2026-08-05-implementation-response.md` @ `efd9ff4739d03293e15efaf38944468f0d214c1c` | `ACCEPTED_IN_FULL` |
| `independent-review-2026-08-05` | Repair submission package after five external adversarial rounds (round 5 = ZERO_DEFECTS_CONFIRMED at Critical/Important) | `.../independent-review-2026-08-05/2026-08-05-repair-submission-package.md` @ `3ebe00ca018632fdf7305ef80c0753f4f8c19830` | `FINAL__AWAITING_FRESH_REREVIEW` |
| `independent-rereview-2026-08-07` | AI doctoral-supervisor + script-engineering independent rereview under the owner-stated simplicity/idempotent-capability rubric | `.../independent-rereview-2026-08-07/2026-08-07-saea-r0-script-engineering-review-assessment.md` @ `257cc0493302c9c156bcc301066e37ea2df468b4` | `R0_OVERALL_INCOMPLETE__R0_2_REPAIR_REQUIRED_FOR_BROKEN_OPERATOR_PATH__R1_MODEL_FACING_EXECUTION_WITHHELD` |
| `verdict-closure-2026-08-25` | Status closure record: every condition the 2026-08-07 verdict withheld on is closed at source, and the HOT endpoint token it wrote is superseded | `.../verdict-closure-2026-08-25/2026-08-25-r0-verdict-closure-and-endpoint-token-supersession.md` @ `a28d3c6a53d0cfb7d2fcf11b8a065b7e6f961412` | `AT_ISSUE_STATUS_CLOSED` |

The original assessment and repair submission blobs are registered from their committed bytes. The
2026-08-07 rereview initially read `PENDING_FIRST_COMMIT` because it was registered in the same
worktree change that first contains it; that standing instruction — verify the committed blob after
its first commit and replace the token — was carried out on 2026-08-25, and the row now reads the
verified blob `257cc0493302c9c156bcc301066e37ea2df468b4`
(`git rev-parse HEAD:wiki/audit/speech-aware-evidence-acquisition-r0-review/independent-rereview-2026-08-07/2026-08-07-saea-r0-script-engineering-review-assessment.md`,
re-derived with `git hash-object` over the committed bytes). Completing that deferred registration
changes no round artifact and no verdict.
Registered audit bytes are immutable under `wiki/AI-Collaboration.md`; corrections append a new round
artifact rather than editing one.

**Closure of the 2026-08-07 at-issue status (appended 2026-08-25).** The `verdict-closure-2026-08-25`
round records that `R0.1`, `R0.2`, `R0.3` and the withheld `R1` model-facing execution are each closed,
with the source for each, and that the program endpoint field pair moved from
`…STAGE2A_R0_INCOMPLETE__R1_WITHHELD` to `…STAGE2A_R0_CLOSED__R1_RELEASED` on the HOT page. It amends
no round artifact: the 2026-08-07 assessment and implementation response keep their bytes and remain
correct as of their date. It carries no owner signature and grants no execution authority; the release
of the `R1` withholding rests on the owner record cited inside it, and every per-contact gate the
verdict relied on stays in force.

**Owner action arising from this campaign, filed as execution authority (not an audit artifact):**
`wiki/experiments/speech-aware-evidence-acquisition/2026-08-06-owner-budget-caps-retirement-contract.md`
retires the first-slice numeric budget caps of the consolidated contract §6 (signed 2026-08-06). It
lives with the other owner contracts because it *is* execution authority; audit-iteration naming
(`…-amendment-<n>.md` under `epoch-<n>/`) is reserved for amendments to audit artifacts themselves.
Consequence for reviewers: absence of numeric-cap enforcement is an owner scope reduction, not a
defect; the one-time attempt semantics of finding P0-4 remain in force.
