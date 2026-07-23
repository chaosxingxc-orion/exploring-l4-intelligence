# System-first Stage-1B capability-delta audit index

This is the cold router for the bounded capability-delta transaction. Current authority remains in
`wiki/Research-Objective.md` and `wiki/survey/current/status.md`.

| Round | Type | Artifact and registered Git blob | At-issue status |
|---|---|---|---|
| `owner-authorization` | owner authorization record | `wiki/audit/system-first-stage1b-capability-delta/owner-authorization/2026-07-23-owner-authorization.md` @ `09dd7f38847f4d501e11b6f9711bc8021bca95dd` | `AUTHORIZE_STAGE1B_CAPABILITY_DELTA_MAPPING` |
| `release-candidate-review-request` | independent review request | `wiki/audit/system-first-stage1b-capability-delta/release-candidate-review-request/2026-07-23-stage1b-capability-delta-review-request.md` @ `41b934adc4390d1576ed2f765030af50300bbbf2` | `RELEASE_CANDIDATE_AWAITING_INDEPENDENT_REVIEW` |

The owner token authorizes only the bounded Stage-1B mapping. The review request is not a signature.
`SIGN_STAGE1B_CAPABILITY_DELTA_RELEASE` remains absent until an independent reviewer supplies it in a
new immutable artifact. Stage-1C mapping and research execution remain separately gated.
