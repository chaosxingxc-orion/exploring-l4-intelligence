# SAEA R0 repair design: trust boundary and run-transaction closure

## Status

This responds to the independent review
`wiki/audit/speech-aware-evidence-acquisition-r0-review/independent-review-2026-08-05/`
(verdict `R0_REPAIR__R1_MODEL_FACING_EXECUTION_WITHHELD_PENDING_P0_CLOSURE_AND_R0_SMOKE`).
All P0/P1 claims were **confirmed in full** by our own independent re-verification (a close reading of the
control-plane code plus executable probes from two verification agents; evidence in study
`.superpowers/sdd/r0-repair/verification.md`). This document freezes the repair scope and acceptance
criteria; it does not modify the owner contract and does not expand into R1/X/2B scope.

```yaml
record_kind: r0-repair-design
date: 2026-08-05
study: speech-aware-evidence-acquisition
reviewed_study_commit: b0635aa9736d2cbf3a581fc9295110172672c833
reviewed_umbrella_commit: 047cf39dcbb7b8cde56757d69eb63a98c9f86de0
verdict_accepted: true
```

## §1 Root causes (these determine the repair method, not just patching holes)

1. **The threat model was self-sourced.** The "governance invariants" list used by the first five
   adversarial rounds was derived by the implementer from their own diff: it covered file governance
   (frozen surface, forbidden datasets, no model contact, no committed bytes) and covered the
   **runtime trust boundary** not at all — whether receipts are self-consistent, whether payload values
   agree with the plan, whether the process answering a request is the one that was pinned. The reviewer
   attacked from inside the reviewed party's worldview, so everything was held.
2. **The verification anchor was misplaced.** Task-level review compared against the "authoritative code
   block in the plan", and literal agreement counted as PASS. When the plan itself is missing a check,
   nobody in the chain can discover it. Only the independent review, building a promise-evidence matrix
   from the **contract**, exposed "measurement integrity promised, wiring delivered".
3. **Self-attested artifacts were treated as verified artifacts.** A systematic pattern: hashing whatever
   could be hashed, without binding the hash to what actually happened (splits.json is self-attested; the
   runtime receipt attests the disk but not the server; outputs.text bears no relation to its own response
   hash).
4. **The budget was an in-process memory counter rather than a persisted transaction.** The exposure ledger
   was designed as a "human-written audit record", with no attempt semantics, no one-shot consumption, and
   no failure cost written to disk.
5. **The conclusion overstepped in its wording.** "These attacks found no defects" was written up as "zero
   defects".

### Method changes derived from the root causes (mandatory for this repair)

- The plan **no longer supplies an authoritative code block**: it supplies **invariants + regression
  probes**, the implementation is derived by the executor, and review compares against the invariants
  rather than literal code;
- Every repair task must carry an executable probe that **turns from ACCEPT to REJECT**;
- The final threat model comes from the **contract promises** and the **external-input trust boundary**,
  is generated from an independent perspective, and never reuses the implementer's list;
- Conclusions may only be phrased as "the following attack surfaces were not broken in X rounds", with the
  attack list attached.

## §2 Repair scope and out of scope

**In scope (P0):** split receipt authenticity, carrier/media/payload value-level binding, runtime session
identity, one-shot attempt budget.
**In scope (P1):** run-bundle hash closure and finalizer, formal configs for the three engineering controls,
the scorer seam end to end, completing cost accounting, CI and documentation alignment.
**Out of scope (legitimately deferred, as the review also confirmed):** X1/X3/X4 policy, the concrete oracle
algorithm, large-scale confirmatory validation, paper-scale work and manuscripts.

**Frozen-surface adjustment (stated explicitly):** the earlier "cannot be changed" status of `contracts.py`
was a self-imposed constraint of the R0 implementation plan, not an owner contract clause; gate hardening
must modify it. The E0 receipt does not cover `contracts.py` (D3 freezes only `scoring/`), and after any
modification the receipt verification and all contract tests must be rerun. `scoring/`, `e0/`, the existing
`docs/receipts/*.json` and `docs/exposure-ledger.md` remain unmodifiable.

## §3 Invariants that must hold (acceptance criteria)

- **I1 split authenticity:** before any model contact, the splits receipt must pass strict parsing (schema,
  exact key set, per-split carrier/role/count/ids sorted, unique and prefix-consistent, identity_hash
  recomputed from ids and equal, splits on the same carrier mutually exclusive), and must be bit-for-bit
  equal to a **live recomputation by the current loader**; any mismatch fails closed.
- **I2 carrier scope:** the plan carrier must belong to this study's speech-carrier allowlist (derived from
  the umbrella lock profile) and must not be on the general-audio denylist; the carrier column of the
  exposure row must be parsed and must agree with the plan.
- **I3 payload value-level binding:** the adapter must verify `payload.carrier_lock_key == plan.carrier_lock_key`,
  `speech_ref == f"{carrier}/{sample_id}"`, `sample_id ∈ frozen split ids`, and that `audio_seconds` agrees
  with the loader's facts.
- **I4 media confinement:** `media_relpath` accepts only a normalized POSIX relative path; after resolution
  it must lie inside that carrier's `local_subdir`; absolute paths, drive letters, backslashes, `..` and
  symlink escapes are all rejected (at both the adapter and transport layers).
- **I5 server identity:** the endpoint is restricted to the local machine; every run must have a session
  receipt binding the binary hash, PID, argv, port and the model/mmproj paths; contact is refused when there
  is no session receipt or the identity does not match.
- **I6 one-shot attempt:** `(run_id, attempt_id)` is a non-reusable primary key and the gate opens it
  atomically and exclusively; actual usage is persisted **before sending** and is not lost on failure; a
  retry must use a new attempt; the slice ceiling takes the conservative upper bound over both "registered
  reservation" and "actual usage".
- **I7 artifact closure:** every attempt produces a run manifest binding the study commit, the
  config/protocol/plan/split identities, the exposure row and attempt id, the hashes of outputs / raw trace /
  trace manifest / scores / session receipt, the actual cost and the final state; the scorer must go through
  the manifest entry point and complete full-chain verification first (response hash corresponds to text, the
  sample set equals the frozen split, no duplicates).
- **I8 accounting completeness:** beyond calls/tokens/latency/audio, add measured GPU/CPU/peak VRAM, evidence
  bytes, and the cost of failed attempts; anything that cannot be measured must be explicitly recorded as a
  deviation and referred to the owner, never silently omitted.
- **I9 CI authenticity:** CI reflects current R0 semantics; the clean-clone job installs the package first;
  active-tree lint is gated; the five probes become permanent regressions; if coverage/type-check are not
  configured they must be explicitly marked `NOT_CONFIGURED`.

## §4 Permanent regression probes (each must turn from ACCEPT to REJECT)

| # | Attack | Current | After repair |
|---|---|---|---|
| P1 | exposure row is earnings21, plan carrier=`fsd50k` | ACCEPT | REJECT |
| P2 | receipt ids replaced, identity_hash left at the old value | ACCEPT | REJECT |
| P3 | absolute media path outside the data root | READ/SEND | REJECT |
| P4 | same exposure row/plan opens the gate twice, count reset to zero | ACCEPT×2 | second one REJECT |
| P5 | submitting an `fsd50k` payload under an earnings21 plan | ACCEPT | REJECT |

## §5 Delivery order

H1 split closure → H2 carrier/media/payload binding → H4 attempt accounting → H3 session identity →
H5 bundle+finalizer → H6 config/scorer/cost → H7 CI/documentation → a final review from a completely fresh
independent perspective → submit the fresh rereview package. R0.3 smoke and R1 do not start until the final
review passes and the owner's dispositions are in place.

## §6 Items requiring owner disposition (the implementer must not interpret these unilaterally)

1. Whether the entity/QA scorer adapter belongs to the R0 deliverable (its reference-layer format is not yet
   frozen), or is explicitly moved out and accepted as such;
2. GPU/CPU/VRAM accounting: this design chooses **measured sampling** rather than deferral; if sampling is
   not obtainable on this machine, the owner must accept the deviation;
3. Execution authorization for R0.3 `SAEA-E-001` and its attempt pre-registration.

## Invalidation conditions

When the owner modifies the scope, criteria or authorization above, this document is superseded in place
and the dated record is retained.
