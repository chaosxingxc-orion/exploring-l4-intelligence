# R2R1 typed compiler and freeze-integrity codebook

## Object identity

- Coders provide local IDs only; `object_match_key` remains forbidden in raw responses.
- A local ID must be unique within its object type. Reuse across different types is permitted because
  every map and reference is typed.
- A compatibility decision supplies both `target_object_type` and `target_object_id`. The target must
  exist in that exact typed map. Missing, untyped or cross-type fallback targets invalidate the whole
  response before agreement.
- Source anchors remain compiler-owned hashes over frozen rendition bytes and typed coordinates.

## Paper-visible reproduction support

The following ten facts are coded independently: task, dataset, dataset revision, split, official
repository, pinned revision, entrypoint, model access, license/terms and evaluator/ground truth.
Each fact has exactly one state:

- `OBSERVED_IN_SOURCE`;
- `NOT_STATED_IN_SOURCE`;
- `AMBIGUOUS_IN_SOURCE`; or
- `NOT_APPLICABLE_IN_SOURCE`.

`CLOSED_PAPER_SUPPORT` and `REPRODUCTION_CANDIDATE` require all ten states to be
`OBSERVED_IN_SOURCE`, no placeholder value, a non-ambiguous access regime, an immutable pinned
revision and zero blockers. `main`, `master`, `HEAD`, `latest` and equivalent moving targets are not
pinned revisions. `OPEN_WITH_BLOCKERS` requires at least one non-observed fact and at least one
explicit blocker. Local asset readiness remains separate and cannot promote an anchor.

## Response freeze

- A submission is one canonical UTF-8 JSON array in the exact frozen 56-paper order.
- The receiver validates all 56 completed responses, coder/transaction identity, unique paper and
  response IDs, canonical serialization, byte length and SHA-256 before issuing a submission receipt.
- Delivery receipts bind input bytes. Submission receipts independently bind output bytes.
- Runtime intake binds both receipt identities/hashes, both response byte lengths/hashes and a frozen
  response root derived from the static package root plus both submission receipts.
- Agreement accepts the two raw byte arrays, not caller-supplied parsed object lists. It recomputes
  every receipt and root binding before semantic validation or metrics.

## Authority

R2R1 is method-ready only. A fresh exact independent ACCEPT is mandatory before coder distribution.
The fixed agreement threshold remains 0.85, and no sample, source, anchor or result is changed.
