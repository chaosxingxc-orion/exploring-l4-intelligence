---
artifact_id: SF-STAGE1A-READINESS-CORRECTION-2026-07-20-01
date: 2026-07-20
campaign: system-first-stage1a
round: 12
document_role: immutable audit correction and independent re-review request
stage: Stage-1A survey-ready gate
execution_authorized: false
supersedes_claims: v10 E1-E5 closure and readiness/signature wording
---

# Stage-1A readiness correction — round 12

<!-- release_binding: {"source":"docs/checks/system-first-stage1a/evidence-v6/identity-taxonomy-v6-test.json","reward_guided":"6/11","rq_sys_compatible":"5/11","method_candidate":"0/11","reward_guided_selection":"4/11","trajectory_pool":"2/11"} -->

## Correction and withdrawal

The v10 statement that the E1–E5 remediation was fully closed is withdrawn. In particular, v10 §0,
§2.4, and §7 exceeded the then-implemented contract and do not establish readiness, reviewer
signature, or execution authority. The current effective rules are consolidated in
`wiki/survey/current/protocol.md`; this correction records the false-greens and the bounded repair
without creating another amendment dependency.

The first exact false-green was the reviewer's weak PDF locator counterexample. Before this repair, a
PDF method path with `source_locator = "p1 the"` produced:

```text
validate(...)  -> []
reconcile(...) -> []
```

The second false-green followed the legitimate new-row flow: change a load-bearing signal source
from `learned_rm_prm` to `llm_judge`, recompute the adjudication row hash, then validate the newly
stamped row. Before this repair, that value change likewise produced:

```text
validate(...)  -> []
reconcile(...) -> []
```

The row hash correctly protected an already-adjudicated row from later drift, but it was not a
generic value validator. Neither false-green was evidence of malicious hash rewriting; both modeled
ordinary Stage-1B first encoding and therefore had to fail through the evidence contract itself.

## Bounded repair and adjudication

Schema v3 now binds all **16 row-level fields**, every signal's **4 fields** (`form`, `source`,
`lifecycle`, `uses`), and every control edge's **2 fields** (`signal_use`, `decision_right`). Missing
bindings and bound-value mismatches fail before derivation. The locator contract now rejects bare,
weak, absent, or document-frequent anchors: a PDF anchor needs at least two lexical tokens, at least
twelve alphanumeric characters, a hit in the declared page window, and no more than three hits in
the complete PDF.

The adjudication artifact is
`wiki/survey/current/data/schema-v3-adjudication.json`. Its recorded reviewer identity is
`/root/a6_adjudicator`, role `fresh non-implementer`; the final record is `ALL_AGREE` with 70/70
binding verdicts and 6/6 anchor-rule verdicts. This is an evidence adjudication, not the independent
Gate-S1 re-review requested below.

The canonical v6 report is
`docs/checks/system-first-stage1a/evidence-v6/identity-taxonomy-v6-test.json`. The two platform
snapshots are:

- Windows: `docs/checks/system-first-stage1a/evidence-v6/identity-taxonomy-v6-test.nt.json`
  (`nt`, Python 3.14.3, PASS).
- WSL2 Ubuntu-24.04: `docs/checks/system-first-stage1a/evidence-v6/identity-taxonomy-v6-test.posix.json`
  (`posix`, Python 3.12.3, PASS).

Their occupancy objects are byte-structure equal. The repaired report keeps the frozen denominators
and claims at Stage-1A directional-only / hypothesis-grade; it does not upgrade them to systematic
mapping findings.

<!-- generated_headline_begin -->
| 派生量 | method-path 分母 | unique-work 分母 |
|---|---|---|
| is_reward_guided | 6/11 | 4/8 |
| is_rq_sys_control_compatible | 5/11 | 4/8 |
| is_project_method_candidate | 0/11 | 0/8 |
| reward_guided_selection | 4/11 | 3/8 |
| strict∧reward∧pool (trajectory) | 2/11 | 1/8 |
<!-- generated_headline_end -->

## Protocol, context, and execution boundary

Protocol v2 compiles to 65 records that are byte-identical to the frozen
`wiki/survey/2026-07-15-sf-queries.jsonl`; no query term, ordering, record hash, or output byte was
changed. The consolidated AI surface contains 19 active entries, exactly three default entries, and
passes every configured file budget plus the 30-entry ceiling. Seven eligible unregistered
amendments were moved with Git as byte-identical renames; registered audit artifacts and retained
path-pinned exceptions were not moved or rewritten.

Exposure for this repair is: **zero discovery queries**, **zero research-model runs**, and **zero
smoke runs**. Inherited exposure remains `INHERITED_PRIOR_EXPOSURE` and is unchanged. No discovery
output, model rollout, or experiment result is created by this transaction.

## Re-review request and authority boundary

Please independently re-review the v6 field-binding and strong-anchor contract, the equal
Windows/WSL occupancy, protocol-v2 byte equivalence, and the context/archive gates. Until that review
returns an eligible verdict and the owner separately authorizes execution, the state remains
**Stage-1A**.

This correction is **not** an independent reviewer signature, **not** owner Stage-1B execution
approval, and **not** evidence that Stage-1B has begun. The first systematic discovery query remains
forbidden by this transaction.
